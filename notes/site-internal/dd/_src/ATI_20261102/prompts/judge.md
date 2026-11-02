你是 stock-analyst **v20 判斷 agent**，標的 ATI（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ATI","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_sales_gaap","label":"Sales (GAAP)","value":1261.1,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）"},"note":"未取得"},{"id":"f_kpi1_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代之）","value":284.4,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M（利益率 22.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）"},"note":"超出公司自家 Q2 指引上緣（標題：Exceeds the High End of Q2 Guidance）；分析師共識數字未取得"},{"id":"f_kpi2_operating_income_gaap","label":"Operating income (GAAP)","value":220.0,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M（利益率 17.4%，由新聞稿數字推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）；含 9.9M 廠房出售利得、23.6M 特殊項目稅前費用"},"note":"未取得"},{"id":"f_kpi3_adjusted_free_cash_flow","label":"Adjusted free cash flow","value":68.6,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）；營業現金流 131.8M，capex 68.6M"},"note":"未取得"},{"id":"f_kpi5_backlog","label":"Backlog","value":4400,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M（YoY +18%，創高）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）"},"note":"不適用"},{"id":"f_kpi6_guidance_q3_2026","label":"Guidance：Q3 2026","value":"Adj EBITDA 305–315M；Adj EPS 1.31–1.37","period":"Q2 2026 新聞稿（2026-08-06）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 2026 新聞稿（2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）；未提供營收指引"},"note":"未取得"},{"id":"f_kpi7_guidance_fy2026","label":"Guidance：FY2026（上修）","value":"Adj EBITDA 1,135–1,185M；Adj EPS 4.90–5.18；Adj FCF 550–600M","period":"Q2 2026 新聞稿（2026-08-06）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 2026 新聞稿（2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）"},"note":"本站 FY1 EPS 共識 5.12（2026-10-08 快照，位於指引區間內）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ati_gross_margin_pct","label":"ATI 毛利率","value":24.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ati_operating_margin_pct","label":"ATI 營業利益率","value":16.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ati_fcf_margin_pct","label":"ATI FCF 利潤率","value":8.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hwm_gross_margin_pct","label":"HWM 毛利率","value":36.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hwm_operating_margin_pct","label":"HWM 營業利益率","value":28.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hwm_fcf_margin_pct","label":"HWM FCF 利潤率","value":19.83,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_crs_gross_margin_pct","label":"CRS 毛利率","value":31.21,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_operating_margin_pct","label":"CRS 營業利益率","value":23.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_fcf_margin_pct","label":"CRS FCF 利潤率","value":10.69,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cstm_gross_margin_pct","label":"CSTM 毛利率","value":16.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSTM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cstm_operating_margin_pct","label":"CSTM 營業利益率","value":8.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSTM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cstm_fcf_margin_pct","label":"CSTM FCF 利潤率","value":3.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSTM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mtrn_gross_margin_pct","label":"MTRN 毛利率","value":16.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtrn_operating_margin_pct","label":"MTRN 營業利益率","value":6.35,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtrn_fcf_margin_pct","label":"MTRN FCF 利潤率","value":1.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_0_6","label":"SBC（上半年累計，占上半年營收約 0.6%）","value":14.1,"period":"2026 上半年（至 2026-06-28，公告 2026-08-06）；新聞稿未單列 Q2","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"2026 上半年（至 2026-06-28，公告 2026-08-06）；新聞稿未單列 Q2","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）；占比 = 14.1 ÷ (1,261.1+1,151.5)"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":165.59,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":6.65,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":38.52,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":1.56,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.13 → 5.21）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.63,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.39 → 6.43）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.52 → 7.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.21,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.43,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.52,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":16.82,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 4.46 → 5.21（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":41.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝98.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":98.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.49,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.77,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":31.78,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.21，分子＝快照價 165.59","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1415.2,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 1857.5、現金 442.3（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":135.82,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":23906.08,"period":"2026-11-02","unit":"USD m","basis":"市值 22490.88 ＋ 淨負債 1415.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5296.83,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（4 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5763.39,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（9 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.51,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 165.59 / W52 160.1 / W104 114.41 / W250 71.17 / W250 13週斜率 3.67%"},{"id":"f_ma_w52","label":"52 週均線","value":160.1,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":114.41,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":71.17,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.67,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"ATI FY2025 10-K 列示 HPMC 主要競爭者：鈦合金對 Howmet Aerospace、傳統鎳基與特殊鋼對 Carpenter Technology，另有 Precision Castparts（Berkshire）與 Aubert & Duval（精密鍛件）。","source":"ATI Inc Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":null,"as_of":"2025-12-28","retrieved_at":"2026-10-13","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Argus 報導（Farnborough 展期間）：2026 上半年引擎 OEM 交付顯著增加，拉動熔煉、鑄造、鍛造廠材料需求；引擎 OEM 與特殊合金廠過去一年大幅投資擴充熔煉、鑄造、鍛造產能或鎖定既有供應。as_of 為展期（2026 年 7 月）近似日，頁面未逐字確認。","source":"Argus Media (Farnborough 2026 report)","url":"https://www.argusmedia.com/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"ATI 宣布約 7,000 萬美元鎳基超合金粉末擴產，其中相當部分用於滿足與噴射引擎 OEM 延續至下個十年的長約。","source":"ATI to expand nickel-based superalloy powder capabilities (metal-am.com / metal-powder.tech)","url":"https://www.metal-am.com/ati-to-expand-nickel-based-superalloy-powder-capabilities-for-additive-manufacturing-sector/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Carpenter Technology 預期 2026 資本支出 2.2–2.4 億美元，投向自有引擎合金與高毛利機會，訂單連續數季成長（Zacks）。","source":"Zacks: ATI vs. CRS: which specialty metals stock should you invest in now","url":"https://www.zacks.com/stock/news/2889540/ati-vs.-crs:-which-specialty-metals-stock-should-you-invest-in-now","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"ATI FY2025 10-K 揭露：任何年度皆無單一客戶占銷售超過 10%，核心終端市場為航太國防、特殊能源、電子、醫療。","source":"ATI Inc. Form 10-K FY2025 (period ended 2025-12-28)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":"No single customer accounted for more than 10% of sales for any year presented. The core end markets for ATI's products are customers in the aerospace & defense, specialty energy, electronics, and medical markets.","as_of":"2025-12-28","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"ATI 與 Airbus 簽多年期鈦板／片／billet 合約（2025 年 5 月）；Boeing 鈦協議延長且非排他。搜尋結果未找到任一客戶導入第二供應商或將鈦材自製（in-house）的來源。","source":"ATI IR press release: ATI signs multi-year agreement with Airbus for titanium plate, sheet and billet","url":"https://ir.atimaterials.com/news-events/news-details/2025/ATI-signs-multi-year-agreement-with-Airbus-for-titanium-plate-sheet-and-billet/default.aspx","excerpt":null,"as_of":"2025-05-01","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"ATI FY2025 10-K 指出 HPMC 分部約 92% 營收來自航太與國防市場，並點名 Boeing、Airbus、Embraer（機身）與 GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran（發動機）為少數大型客戶群；搜尋摘要未取得單一客戶占營收百分比。","source":"ATI INC - Form 10-K - FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"GE Aerospace 2026 Q2 業績優於預期並上調全年調整後 EPS 指引至 $7.65-$7.85（原 $7.10-$7.40）；CEO 稱主要限制在供應端而非需求。另有報導稱 2026 年初 GE 因中東衝突下調全年航班起降展望。","source":"WebSearch 摘要（GE Aerospace Q2 2026 results 報導）","url":null,"excerpt":null,"as_of":"2026-07-21","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Argus（Farnborough 後報導）：引擎 OEM 2026 上半年出貨大增，拉動熔煉、鑄造、鍛造端訂單；航空級(PQ)鈦 billet 需求強，供應商報價交期 3–6 個月；新合金產能預期 2027 後半至 2030 陸續投產。","source":"Argus Media, Jet engines driving nickel, PQ titanium demand","url":"https://www.argusmedia.com/en/news-and-insights/latest-market-news/2860247-jet-engines-driving-nickel-pq-titanium-demand","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ATI 稱其最差異化產品（超合金鎳、PQ 鈦、等溫鍛件、特殊合金）交期正在拉長。","source":"ATI Q2 2026 earnings call (MarketBeat 摘要)","url":"https://www.marketbeat.com/instant-alerts/ati-q2-earnings-call-highlights-2026-08-07/","excerpt":"lead times are extending for our most differentiated products, super alloy nickels, premium quality titanium, isothermal forgings and exotic alloys","as_of":"2026-08-07","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ATI Q2 2026 積壓訂單創高 $4.4B（年增 18%），約 70% 預計 12 個月內轉為營收；2026 指引上調至調整後 EBITDA $1.135–1.185B、EPS $4.90–5.18、FCF $550–600M；航太與國防銷售 +13%，國防 +36%，海軍核能協議續約約 5 年 $1B。","source":"MarketBeat ATI Q2 earnings call highlights／Zacks","url":"https://www.marketbeat.com/instant-alerts/ati-q2-earnings-call-highlights-2026-08-07/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ATI 增建鎳合金熔煉／VIM 產能，約 80% 已簽約，目標 2028 年中增加約 $350M 鎳營收；2026 年 6 月啟用墨西哥 Chihuahua 引擎零件廠。","source":"MarketBeat ATI Q4 2025 earnings call highlights；Metalnomist","url":"https://www.marketbeat.com/instant-alerts/ati-q4-earnings-call-highlights-2026-02-03/","excerpt":null,"as_of":"2026-02-03","retrieved_at":"2026-10-13","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Argus 引 ATI 特殊材料事業總裁：轉子級材料消耗量未來五年預計增加 26%（約至 2030）。","source":"Argus Media（ATI 特殊材料總裁談話，早期報導）","url":"https://www.argusmedia.com/ja/news-and-insights/latest-market-news/2737772-ti-demand-rebound-dependent-on-inventory-draws","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Airbus 將 A320 月產 75 架目標延至 2027（因供應商爬坡不足、引擎短缺），A350 目標 2028 年月產 12 架；Airbus 2025 年底積壓 8,754 架。","source":"搜尋結果彙整（Hexcel Q3 2025 earnings／eplaneai 等）","url":"https://finance.yahoo.com/markets/stocks/articles/hexcel-hxl-q3-2025-earnings-160357040.html","excerpt":null,"as_of":"2025-11-01","retrieved_at":"2026-10-13","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Argus 稱引擎瓶頸正在緩解（Airbus 與 Pratt & Whitney GTF 交付爭議為例外）；ATI 集中於少數大型航太 OEM 為風險；HPMC 約 $30–40M 出貨因認證時程遞延至下半年。","source":"Argus Media 2860247；Panabee／MarketBeat 彙整","url":"https://www.argusmedia.com/en/news-and-insights/latest-market-news/2860247-jet-engines-driving-nickel-pq-titanium-demand","excerpt":null,"as_of":"2026-08-07","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 列示的訴訟為一般性訴訟與一宗合併的退休金年金購買集體訴訟（ERISA 類，2024-08 起），未列反壟斷調查或拆分事項；管理層認為未決事項不太可能對財務狀況或流動性造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":"While we cannot predict the outcome of any lawsuit, claim or proceeding, our management believes that the disposition of any pending matters is not likely to have a material adverse effect on our financial condition or liquidity.","as_of":"2026-02-20","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"ATI 2025 年 Q1 法說：年化關稅暴露約 5,000 萬美元，管理層稱透過轉嫁、關稅退稅（duty drawback）與供應鏈調整，全年獲利影響極小，維持 2025 EBITDA 指引。","source":"MarketBeat, ATI Q1 2025 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2025-5-1-allegheny-technologies-incorporated-stock","excerpt":"Despite $50 million of annual tariff exposure, management expects minimal impact on full-year earnings thanks to supply‐chain mitigation, pass‐throughs, duty drawback programs, and cost efficiencies.","as_of":"2025-05-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"ATI 稱生產基地多在美國本土，但部分原料因美國無法供應須進口。","source":"MarketBeat, ATI Q1 2025 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2025-5-1-allegheny-technologies-incorporated-stock","excerpt":"ATI is a US based producer with the majority of our production footprint located domestically... certain raw materials must be imported due to the lack of domestic availability","as_of":"2025-05-01","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"ATI 持有中國合資 STAL 60% 股權（寶武 40%），產品為精密軋製不鏽鋼帶，主要供亞洲電子與汽車市場；另 Section 232 對不鏽鋼板胚的排除申請曾遭商務部否決、25% 關稅仍在（舊案，非 2026 新事件）。","source":"ATI Form ARS FY2022","url":"https://www.sec.gov/Archives/edgar/data/1018963/000119312523079059/d472766dars.pdf","excerpt":null,"as_of":"2023-03-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026 年未搜到 ATI 被列入實體清單或出口管制的報導；搜尋亦未找到 ATI 2026 年關稅影響的最新數字（最新公司數據為 2025 年）。","source":"WebSearch 查無結果","url":null,"excerpt":null,"as_of":"2026-10-13","retrieved_at":"2026-10-13","affects":["triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ATI 10-K FY2025 揭露：鎳、海綿鈦、鈷、鉻鐵等原料多來自可能政經不穩的外國；鎳來源列加拿大、挪威、日本、芬蘭、南非；海綿鈦來源列日本、哈薩克、沙烏地、中國；公司稱原料可由多家供應商取得、目前供給足夠。","source":"ATI INC Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":null,"as_of":"2025-12-28","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"ATI 已終止與俄羅斯 VSMPO-AVISMA 的 Uniti 合資（原用於行銷商用純鈦產品）；10-K 警告烏克蘭衝突與現行或未來制裁可能中斷供應或影響材料價格。","source":"ATI INC Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":null,"as_of":"2025-12-28","retrieved_at":"2026-10-13","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ATI 年報（FY2024 ARS）警告中國已實施且未來可能續行出口管制，可能限制或顯著延遲取得相關材料。","source":"ATI INC Form ARS FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000119312525065239/d942872dars.pdf","excerpt":null,"as_of":"2024-12-29","retrieved_at":"2026-10-13","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026（截至 2026-06-28）HPMC 營收 $637.1M，Q1 2026 為 $614.3M、Q2 2025 為 $608.8M；HPMC 營收中航太與國防占 93%；管理層稱 $30–40M HPMC 出貨因認證時程遞延至下半年","source":"ATI Q2 2026 results（SEC 8-K Ex.99.1 / 搜尋摘要整理）","url":"https://www.sec.gov/Archives/edgar/data/0001018963/000162828026053856/form8-kq22026ex991.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 AA&S 營收年增約 17%（+$92.4M），主因航太與國防及傳統能源；AA&S 航太國防銷售年增 34%；公司整體營收年增 11% 至約 $1.3B；AA&S 單季營收總額未確認","source":"ATI Q2 2026 press release / MarketBeat call summary","url":"https://www.marketbeat.com/instant-alerts/ati-q2-earnings-call-highlights-2026-08-07/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"ATI 2026 全年指引：噴射引擎營收中段十位數成長、國防低至中段十位數成長；Q1 2026 維持引擎中段十位數成長，驅動為高機隊使用率、進廠維修增加與 LEAP、GTF 平台成長；機身復甦預期 2026 下半年加速；新平台 ATI 單機含量約高 2 倍","source":"ATI Q1 2026 earnings call（Motley Fool 逐字稿／Yahoo 摘要）","url":"https://www.fool.com/earnings/call-transcripts/2026/04/30/ati-ati-q1-2026-earnings-call-transcript/","excerpt":null,"as_of":"2026-04-30","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"高階鈦與等溫鍛件交期延伸近兩年；ATI 鎳產能擴充目標為 2028 年初較 2025 年底增加 15–20%","source":"ATI Q1 2026 earnings call 摘要","url":"https://finance.yahoo.com/markets/stocks/articles/ati-ati-q1-2026-earnings-174636311.html","excerpt":null,"as_of":"2026-04-30","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"IMARC 2026 版報告列北美鈦價 2026 年 3 月 6.71 USD/kg，較前期下降 3.0%；未找到現行鎳價與 ATI 自身定價趨勢的一手來源","source":"IMARC Titanium Prices report 2026 edition","url":"https://www.imarcgroup.com/titanium-pricing-report","excerpt":null,"as_of":"2026-03-31","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"ATI 10-K 列出『替代材料使用增加或價格下降』為影響其市場地位與獲利波動的因子之一（FY2022–FY2025 10-K 皆有）；未見具體量化的替代技術威脅。","source":"ATI INC Form 10-K FY2025 (ati-20251228.htm)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":"increases in use or decreases in prices of substitute materials","as_of":"2025-12-28","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"GKN Aerospace 與美國空軍研究實驗室啟動 TITAN-AM（840 萬美元），推進線材雷射金屬沉積用於大型鈦機身結構的工業化，屬鈦鍛件的近淨形替代/補充路徑。","source":"aeromorning.com: GKN Aerospace and U.S. Air Force advance additive manufacturing","url":"https://aeromorning.com/en/gkn-aerospace-and-u-s-air-force-advance-additive-manufacturing/","excerpt":null,"as_of":"2026-04-13","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"投資人撰寫的敘事（非公司揭露/非分析師研究）主張複合材料、陶瓷、奈米材料與積層製造長期可能侵蝕 ATI 合金與鈦產品需求。","source":"Simply Wall St community narrative: additive manufacturing and composite substitutes will disrupt future prospects","url":"https://simplywall.st/community/narratives/us/capital-goods/nyse-ati/ati/0ow7usxr-additive-manufacturing-and-composite-substitutes-will-disrupt-future-prospects","excerpt":"requiring costly and sustained R&D just to maintain relevance and pressuring both top-line revenue growth and margins over time","as_of":"2025-05-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 管理層稱投資組合持續轉向更差異化、較高毛利，以長期客戶協議為核心，集中於航太、國防與特殊能源","source":"ATI Q2 2026 8-K ex99.1","url":"https://www.sec.gov/Archives/edgar/data/0001018963/000162828026053856/form8-kq22026ex991.htm","excerpt":"\"This quarter reflects the continued evolution of ATI's portfolio toward a more differentiated, higher-margin business, anchored by long-term customer agreements and concentrated exposure in aerospace, defense and specialty energy.","as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08 Q2 後公司將 FY2026 調整後 EPS 指引由 $4.20–4.48 上調至 $4.90–5.18，高於 MarketBeat 所載事前共識 $4.44；Q3 EPS 指引 $1.31–1.37 對共識 $1.12。","source":"MarketBeat: ATI updates FY 2026 earnings guidance (2026-08-06)","url":"https://www.marketbeat.com/instant-alerts/ati-nyseati-updates-fy-2026-earnings-guidance-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-10-13","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 指引全面上調：調整後 EBITDA $1,135M–1,185M（前 $1,010M–1,060M）、調整後 FCF $550–600M（前 $465–525M）；Q2 營收 $1.26B（+11% YoY）、調整後 EPS $1.23 對共識 $1.03；backlog $4.4B（+18% YoY）；董事會另批 $500M 回購授權。","source":"ATI press release: ATI Exceeds the High End of Q2 Guidance and Raises Full-Year Outlook (Barchart)","url":"https://www.barchart.com/story/news/3688858/ati-announces-second-quarter-2026-results","excerpt":"Prior Guidance Full Year 2026 Adjusted EBITDA $1,010M - $1,060M","as_of":"2026-08-05","retrieved_at":"2026-10-13","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布因來源而異：Benzinga 10 位分析師平均 $177（高 $270／低 $81，頁面日期 2026-09-04，疑似含過時目標）；Investing.com 9 位全 Buy、平均約 $200.33（高 $231／低 $175，2026-09 快照）；MarketBeat 2026-09 初報平均 $232。KeyBanc 2026-08-12 升至 $258、Susquehanna 2026-08-07 升至 $265。","source":"Benzinga price-targets page; Investing.com ATI consensus estimates","url":"https://www.investing.com/equities/allegheny-tech-consensus-estimates","excerpt":"Analyst Consensus— Overweight and Analyst Consensus — 10 Analysts with Consensus PT$177.","as_of":"2026-09-04","retrieved_at":"2026-10-13","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"共識 EPS 上修趨勢：Q1（2026-04-30）調整後 EPS $1.00 對共識 $0.88；Yahoo 快照 2026 共識 4.14（90 天前 3.83）；Seeking Alpha（2026-03）過去三個月 7 次上修 0 次下修。Q2 後 MarketBeat 九月初稱分析師預期本年 EPS 5.11（不確定是否為真共識）。","source":"Nasdaq/Zacks: ATI Up 26.9% Since Last Earnings Report; MarketBeat","url":"https://www.nasdaq.com/articles/ati-ati-269-last-earnings-report-can-it-continue","excerpt":null,"as_of":"2026-09-05","retrieved_at":"2026-10-13","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露 2024-08 起的退休金年金合約（Athene）集體訴訟；2025-08 聽證後 magistrate judge 建議以無訴訟資格駁回，待主審法官裁定；公司無法估計損失範圍。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":"Following an August 2025 hearing on the motion to dismiss, the magistrate judge covering the Motion issued a report recommending that all of the plaintiffs’ claims be dismissed for lack of standing. The recommendation remains subject to review and disposition by the presiding judge.","as_of":"2026-02-20","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 中的重大項目為 2026-06 發行 $450M 5.875% 2033 年到期優先無擔保債券（Item 1.01），非併購。","source":"SEC EDGAR 8-K 2026-06-08","url":"https://www.sec.gov/Archives/edgar/data/1018963/000119312526261769/d163250d8k.htm","excerpt":"On June 8, 2026, ATI Inc. (the “Company”) completed its offering and sale of $450 million aggregate principal amount of the Company’s unsecured 5.875% Senior Notes due 2033 (the “Notes”).","as_of":"2026-06-08","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"ATI 增建鎳熔煉/VIM 產能，新產能預計 2027 下半年投產，管理層稱約 80% 已有合約；目標 2028 年中增加約 3.5 億美元鎳營收","source":"MarketBeat, ATI Q4 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/ati-q4-earnings-call-highlights-2026-02-03/?.tsrc=rss","excerpt":null,"as_of":"2026-02-03","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"同業 Carpenter Technology 的 Athens 棕地擴建（約 9,000 噸、含新 VIM 爐）預計於 FY2028 開始前完成，進度與預算符合預期","source":"Nasdaq/Zacks 與 MarketBeat Carpenter Q2 call highlights","url":"https://www.marketbeat.com/instant-alerts/carpenter-technology-q2-earnings-call-highlights-2026-01-29/?.tsrc=rss","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Argus 報導：ATI 在 Monroe NC 第五座 VIM 爐約增 9,000 噸/年，2027 下半年啟用；另提 Doncasters 5,000 萬美元超合金廠及 SMP 增爐增壓機；合金業者預期新產能 2027 末至 2030 逐步爬坡","source":"Argus Media, Jet engines driving nickel, PQ titanium demand","url":"https://www.argusmedia.com/en/news-and-insights/latest-market-news/2860247-jet-engines-driving-nickel-pq-titanium-demand","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"ATI Q2 2026 call：鎳再熔擴產按計畫、新 VIM 爐 2027 年底前上線；全年 2026 調整後 EBITDA 指引上調至 11.35–11.85 億美元","source":"Nasdaq, Is ATI Positioned for Further Adjusted EBITDA Improvement?","url":"https://www.nasdaq.com/articles/ati-positioned-further-adjusted-ebitda-improvement","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"ATI Q3 2026 銷售年增約26%至14.2億美元，來源稱由定價與航太國防需求推動","source":"ATI 10-Q (Q3 FY2026) 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001018963/000162828026068145/ati-20260927.htm","excerpt":"Third quarter 2026 sales increased approximately 26% to $1.42 billion, compared to $1.13 billion of sales for the third quarter 2025.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"ATI Q2 2026 銷售年增約11%至12.6億美元，主因較高定價與航太國防需求強勁","source":"ATI 10-Q (Q2 FY2026) 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001018963/000162828026054233/ati-20260628.htm","excerpt":"Second quarter 2026 sales increased approximately 11% to $1.26 billion, compared to $1.14 billion of sales for the second quarter 2025, primarily due to higher pricing and strong demand in the aerospace & defense markets.","as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Argus 2026年4月報告：結構件端仍在去庫存、引擎端具韌性，次要金屬供給緊俏延後持續放量","source":"Argus Aerospace minor metals titanium market outlook 2026-2027（搜尋摘要轉述，非逐字）","url":"https://www.argusmedia.com/ja/news-and-insights/market-insight-papers/aerospace-minor-metals-titanium-market-outlook-2026-2027","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261102","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"Argus：空巴波音去庫存拖累 ATI 2Q 鈦銷售（2025 Q2，預期2026年復甦）","source":"Argus Media","url":"https://www.argusmedia.com/metals-platform/newsandanalysis/article/2717004-Airframers--destocking-dents-ATI-s-2Q-Ti-sales","excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2020疫情下行期：Q3 2020 HPMC航太國防銷售年減55%（商用航太-64%），Q3 ATI調整後EBITDA僅16.6百萬美元、占銷售2.8%。","source":"ATI Q3 2020 results / 10-Q (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828020015070/ati-20200930.htm","excerpt":"Sales to the aerospace & defense markets, which represented 78% of third quarter 2020 HPMC sales, were 55% lower, primarily resulting from a 64% decrease in sales to the commercial aerospace market","as_of":"2020-10-30","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2020全年銷售29.8億美元，調整後EBITDA 196.3百萬美元（6.6%）；Q4 HPMC商用航太銷售-68%，HPMC段EBITDA率3.4%（前年同期18.7%）；管理層稱Q4營收季增10%為最差已過的跡象。","source":"ATI Q4/FY2020 results (metal-am.com)","url":"https://www.metal-am.com/ati-announces-q4-and-full-year-2020-results/","excerpt":"Q4 revenue increased 10% to $658 million versus Q3 levels. We see this as a further indication of stabilization in our key end markets and a sign that the worst of the lingering aerospace downturn is behind us.","as_of":"2021-01-28","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月 8-K 共11份，未見 Item 2.01 併購完成；重大項目為債券發行。10-Q 僅見出售已關閉廠房（AA&S）等小型處分。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001018963&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"退休金年金合約集體訴訟（W.D. Pa.），已提駁回動議，magistrate 建議駁回，待主審法官裁定。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":"These lawsuits, which were consolidated in late 2024, assert various claims associated with the Company’s October 2023 purchase of group annuity contracts to transfer a portion of its U.S. qualified defined benefit pension plan obligations to Athene Annuity and Life Company and Athene Annuity & Life Assurance of New York. We filed a Motion to Dismiss the consolidated claims in January 2025.","as_of":"2026-02-20","retrieved_at":"20261102","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ATI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":24.46,"operating_margin_pct":16.52,"fcf_margin_pct":8.4,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HWM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.63,"operating_margin_pct":28.01,"fcf_margin_pct":19.83,"rd_intensity_pct":0.39},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"CRS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.21,"operating_margin_pct":23.36,"fcf_margin_pct":10.69,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CSTM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.06,"operating_margin_pct":8.66,"fcf_margin_pct":3.17,"rd_intensity_pct":0.53},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSTM","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MTRN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.01,"operating_margin_pct":6.35,"fcf_margin_pct":1.55,"rd_intensity_pct":1.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"ATI"},"financial_history":{"ticker":"ATI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3836000000.0,"revenue_yoy_pct":null,"gross_margin_pct":18.62,"operating_margin_pct":10.86,"net_income":323500000.0,"diluted_eps":2.23,"free_cash_flow":94000000.0,"fcf_margin_pct":2.45,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":4173700000.0,"revenue_yoy_pct":8.8,"gross_margin_pct":19.23,"operating_margin_pct":11.37,"net_income":410800000.0,"diluted_eps":2.81,"free_cash_flow":-114800000.0,"fcf_margin_pct":-2.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":4362100000.0,"revenue_yoy_pct":4.51,"gross_margin_pct":20.59,"operating_margin_pct":12.74,"net_income":367800000.0,"diluted_eps":2.55,"free_cash_flow":168100000.0,"fcf_margin_pct":3.85,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":4587400000.0,"revenue_yoy_pct":5.16,"gross_margin_pct":21.95,"operating_margin_pct":13.99,"net_income":404300000.0,"diluted_eps":2.85,"free_cash_flow":333700000.0,"fcf_margin_pct":7.27,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ATI/ATI_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**ATI Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to ATI's Third Quarter 2026 Results Conference Call. [Operator Instructions] I will now hand the conference over to Rob Rengel, Vice President of Investor Relations. Please go ahead.

**Rob Rengel** (Executives):
Good morning, and welcome to ATI's Third Quarter 2026 Earnings Call. Today's discussion is being webcast at atimaterials.com. Joining me are Kim Fields, Board Chair, President and CEO; and Rob Foster, Senior Vice President and CFO. 
Before beginning our prepared remarks, I would like to draw your attention to the supplemental presentation that accompanies this call. Those slides provide additional color and details on our results, capabilities and outlook. They can also be found on our website. As a reminder, all forward-looking statements are subject to various assumptions and caveats. These are noted in the earnings release and presentation. After our prepared remarks, we'll open the line for questions. Now I'll turn the call over to Kim.

**Kimberly Fields** (Executives):
Thank you, Rob. Good morning, everyone, and thank you for joining us. ATI delivered another strong quarter, exceeding the high end of our adjusted EBITDA guidance by $13 million. Today, we are raising our adjusted EBITDA guidance by $35 million for the year, which includes an improved fourth quarter outlook. This is the third increase this year following last quarter's $125 million increase. Our continued outperformance reflects the growing contribution of the structural improvements we've made across the business. 
Demand remains strong across all of our key end markets with sales growth both year-over-year and sequentially this quarter. Slide 4 highlights our key results. Revenue increased 26% year-over-year to $1.4 billion, up 13% sequentially. Within that increase, jet engine revenue grew 39% year-over-year and 19% sequentially, driven by higher production of next-generation engines and continued demand for our differentiated products. Adjusted EBITDA was $328 million, up 46% year-over-year. This was our highest quarterly result since 2007. Adjusted EBITDA margin expanded 300 basis points to 23%. Adjusted EPS increased 72% to $1.46. Backlog was near an all-time record at $4.3 billion, up 20% from a year ago. Combined with extended lead times for our most differentiated products, backlog provides visibility and confidence in our outlook. Adjusted free cash flow was $80 million in the quarter, bringing year-to-date cash flow to $223 million, up $73 million or 49% from the same period last year. 
For the second quarter in a row, AA&S delivered record performance with EBITDA margin of 25.8%, up 850 basis points from a year ago. This durable performance reflects a full quarter of improved contracts and a richer A&D mix. The segment's jet engine sales increased 45% sequentially, reflecting the benefit of ATI's interconnected jet engine flow path. AA&S' performance reflects the transformation of the business. We exited lower-value commodity stainless steel products and applied 80/20 to focus resources on higher-value aerospace, defense and specialty energy products. Aerospace and Defense now accounts for approximately 45% of AA&S sales compared with 18% in 2021. Along with long-term agreements and improved pricing, these changes have created a more durable earnings profile and position AA&S for profitable growth. 
Turning to Slide 5. HPMC sales grew approximately 20% year-over-year, supported by strong demand for nickel and titanium. Third quarter segment margin was 23.2%. At the beginning of this year, HPMC began ramping production of a new alloy following a contract win. This is the sixth of 7 advanced alloys used in the hot section of the jet engine. We qualified the alloy and moved it into production in just 9 months, a strong example of the technical expertise that helps us win business and expand our share. ATI is now one of only two producers worldwide making this alloy. The additional costs from the production ramp reduced HPMC's third quarter margin by approximately 200 basis points versus our plan. We've made meaningful progress through the ramp, and we expect the remaining impact to be behind us by year-end. This is a near-term cost of bringing a valuable new product into production. In return, this alloy expands our content on next-generation engines and positions HPMC for meaningful growth and improved profitability over time. 
Now on Slide 6. Based on our year-to-date performance and strong backlog, we are raising our full year adjusted EBITDA and adjusted EPS outlook. We now expect full year adjusted EBITDA of $1.19 billion to $1.2 billion with a midpoint of $1.195 billion. That is a $35 million increase from our prior outlook and represents 39% full year adjusted EBITDA growth from 2025. The higher outlook reflects continued strength in AA&S and stronger fourth quarter profit expectations in both segments. AA&S is benefiting from durable contract pricing and a stronger aerospace and defense mix. We are also seeing improved pricing for differentiated hafnium and zirconium products. HPMC is expected to improve sequentially as production efficiencies increase and the new alloy's production process matures. We continue to expect full year consolidated adjusted EBITDA margins in the low 20% range and consolidated incremental margins of approximately 50%. The fourth quarter will be our strongest quarter of 2026 for sales and profit. Our outlook reflects committed customer schedules, contracted pricing and planned shipment timing. 
Turning to Slide 7. Elevation is our operating model for converting strong demand, improved commercial terms and targeted investments into higher earnings, margins and cash flow. It helps us increase output from the assets we already own and apply expertise across ATI. One recent example is a project to recover and reuse a critical raw material that has become increasingly difficult to source. Historically, this material could not be reclaimed and reused. Our team brought together ATI's melting and manufacturing capabilities, metallurgical expertise and processing assets to develop a solution. We are now recovering enough material to support most of our ongoing operating needs. That lowers costs and helps secure supply for our customers. We expect this project to generate several million dollars in annual savings beginning in 2027. This is the kind of benefit Elevation enables, combining capabilities across ATI to solve emerging industry challenges and improve our performance. 
Slide 8 gives a summary of our core markets. All four key end markets show strong growth, both year-over-year and sequentially. These customers need qualified capacity, differentiated technology and certainty of supply. ATI has built durable advantages in each of these areas through proprietary materials, specialized manufacturing processes and complex customer qualifications. Those advantages support stronger commercial terms, long-term agreements and attractive opportunities to invest in additional capabilities and capacity. Jet engines remains ATI's largest and most important growth market. Revenue increased 39% year-over-year and 19% sequentially, reflecting strength in both OEM production and aftermarket. There has been some discussion about whether retirements of older aircraft could pressure MRO demand. ATI serves both demand streams. The disk forgings we make go into new engines and are also used as replacement parts in MRO with comparable margins across both. The fleet transition from legacy engines to next-gen engines creates a significant growth opportunity for ATI. Next-generation engines use our differentiated materials to operate at higher temperatures and pressures, and our content on these platforms is more than double our content on legacy engines. We're seeing that opportunity in our results. Demand for our jet engine products continues to strengthen. We now expect full year jet engine revenue growth in the low to mid-20% range, up from our prior expectation of high teens growth. Just last week, a key engine OEM told us that if we doubled our current production for them today, they would take it all. We hear that kind of demand signal consistently. 
In airframe, revenue increased 11% year-over-year and 14% sequentially. At the beginning of the year, we expected airframe demand to build as the year progressed with stronger growth in the second half. That is exactly how the year is unfolding. We saw a clear uptick in demand in the third quarter, and momentum is building into the fourth. Our committed backlog and strong orders for Q4 support our confidence in continued growth through year-end. We remain confident in our full year outlook for mid- to high single-digit airframe revenue growth. 
Defense delivered another strong quarter and remains one of ATI's most important long-term growth opportunities. Revenue increased 6% year-over-year and 6% sequentially, building on the 36% year-over-year growth of the second quarter. This was our highest ever revenue in defense. Missile demand is strengthening with multiple inquiries for our titanium, nickel and niobium products to support strategic platforms, including Tomahawk, THAAD and PAC-3. We continue to expect high teens defense revenue growth for the full year. 
Specialty Energy revenue increased 49% year-over-year and 36% sequentially as we shifted production to meet customer needs. As we discussed last quarter, our flexible assets allow us to balance production between Defense and Specialty Energy demand. Specialty Energy is largely driven by commercial nuclear demand, which continues to outpace supply. Demand for industrial gas turbines also remains strong. We continue to expect mid-teens Specialty energy revenue growth for the full year. Overall, demand remains strong across all our markets, and our differentiated positions are translating into growth. ATI delivered another strong quarter, and we've raised our full year outlook for the third time this year. We expect the fourth quarter to be even stronger. Rob will walk through the financial results and our updated outlook.

**James Foster** (Executives):
Thanks, Kim. I'll start with the third quarter performance, dig into segment results and close with the supporting details for our updated guidance. As shown on Slide 9, we delivered strong overall results. Adjusted EBITDA exceeded the high end of our guidance. We also expanded consolidated margins and generated solid cash flow. These results reflect the strength of ATI's differentiated portfolio and the earnings power of our business model. Third quarter revenue was $1.4 billion, up 26% year-over-year. Aerospace and Defense led the revenue growth and accounted for nearly 70% of our total revenue in the quarter. Within A&D, jet engine sales increased significantly, reflecting the next-generation production ramp, supported by our high-temperature nickel superalloys and favorable pricing. 
Third quarter adjusted EBITDA was $328 million, up 46% year-over-year. This was $18 million above the midpoint and $13 million above the high end of our guidance, reflecting stronger pricing and mix in our AA&S segment. The step change we are seeing in AA&S margins was partially supported by the naval nuclear contract award and strength in Specialty Energy, contracted revenue streams that are durable and sustainable. 
Third quarter consolidated adjusted EBITDA margin was 23%, up 300 basis points year-over-year. Year-to-date adjusted free cash flow was $223 million, an improvement of $73 million from the prior year period. Third quarter adjusted free cash flow was $80 million, reflecting strong cash generation while continuing to fund our growth investments. We're achieving our objective of generating positive adjusted free cash flow in every quarter this year. Managed working capital was 32.9% of sales at quarter end, 140 basis points improvement sequentially. Capital expenditures were $93 million in the quarter. Through the third quarter year-to-date, total CapEx was $217 million. Customer-funded capital was $48 million over the same period. All key growth projects remain on schedule and on budget. 
Now on Slide 10, I'll review segment performance. AA&S sales increased 34% year-over-year to $702 million, driven by several factors, including stronger demand, price and mix, primarily in Aerospace and Defense and Specialty Energy. Segment margin expanded by 850 basis points to a record 25.8%, reflecting stronger pricing and volumes and a more favorable mix. On pricing, we continue to see a favorable pricing environment for our hafnium and zirconium products. Our AA&S segment once again led the outperformance in the quarter. AA&S is fundamentally a different business today. Our results over the past 2 quarters are a strong proof point of our progress. The results reflect the improved earnings profile of AA&S, supported by long-term contracts, stronger pricing and a favorable mix of aerospace and defense sales. 
HPMC sales increased 20% year-over-year to $721 million, supported by strong demand for our differentiated jet engine materials. Segment margin was 23.2%, impacted by the costs associated with ramping commercial production of our sixth nickel-based superalloy. The impact was about 200 basis points in the quarter versus our target. We view these near-term costs as a worthwhile investment in an alloy that will support next-generation engine platforms for decades. We made meaningful progress through the learning curve for our new superalloy in the third quarter with only a modest residual impact anticipated in the fourth quarter. Our confidence in HPMC's long-term margin potential remains unchanged. 
Moving to Slide 11 for our forward-looking assumptions. In the fourth quarter of 2026, we anticipate adjusted EBITDA of $345 million to $355 million, translating to an adjusted EPS of $1.51 to $1.57. At the midpoint, adjusted EBITDA increases 51% compared with the fourth quarter of 2025 and 7% sequentially. We anticipate consolidated adjusted EBITDA margin to expand in the fourth quarter compared to the third quarter with sequential profit improvement in both segments. In AA&S, we expect fourth quarter margins to remain in the mid-20% range, supported by durable contracted pricing and mix, especially in aerospace and defense. In HPMC, we see margin improvement compared to the third quarter level as we anticipate sequential cost improvements related to the production efficiencies I discussed. 
Turning to Slide 12. Our full year outlook reflects the third quarter outperformance led by AA&S and stronger fourth quarter profit expectations in both segments. We see stronger volume overall and a more favorable mix, mainly from jet engines. We are raising our full year adjusted EBITDA guidance to a range of $1.190 billion to $1.200 billion. The midpoint of the range represents a 39% increase over prior year and a $35 million increase versus our prior full year EBITDA guidance. Keep in mind that this raise follows the $125 million raise to our full year outlook from just a quarter ago. This outlook translates to a full year adjusted EPS range of $5.17 to $5.23. We continue to see full year consolidated adjusted EBITDA margins in the low 20% range, and we continue to expect full year consolidated incremental margins in the range of 50% year-over-year. We see the fourth quarter as our strongest quarter of 2026 for both sales and profit. To be clear, we are converting durable demand into margin expansion and cash generation. At the segment level, we now see AA&S full year EBITDA margin in the low to mid-20% range, an increase versus last quarter. The uplift is supported by stronger volume with mix shifting towards aerospace and defense, as we've discussed. We continue to see full year EBITDA margin for HPMC in the mid-20% range, and we remain as confident as ever in the upside potential for HPMC's future margin. 
Turning to adjusted free cash flow. We are maintaining the midpoint at $575 million with a range of $550 million to $600 million. The midpoint is $195 million higher than the 2025 free cash flow, a 51% increase year-over-year. In this period of growth, our inventory levels will be temporarily elevated given the new assets we are bringing on to support capacity. We expect inventory to normalize over time. Let me emphasize, our technical expertise allows us to ramp more efficiently than others. Already in the fourth quarter, we are seeing improved inventory velocity as we work up the learning curve with our new alloys and facilities. We also see strong profit conversion in the fourth quarter. Our capital deployment strategy is unchanged. Our gross CapEx range remains consistent with prior guidance at $280 million to $300 million. Customer-funded CapEx of $55 million to $65 million will be a partial offset. Share repurchases remain a priority for deploying incremental free cash flow. We view them as the most efficient way to return capital to shareholders. As of the end of the third quarter, we deployed $70 million for repurchases with $425 million remaining under our current repurchase authorization. 
Overall, we delivered a strong third quarter and expect an even better fourth quarter and full year. We look forward to seeing you at Investor Day on November 12, where we'll share how ATI's differentiated capabilities, specialized manufacturing processes and organic investments position us for sustained profitable growth. Kim, back to you.

**Kimberly Fields** (Executives):
Thanks, Rob. ATI delivered another strong quarter. We raised our full year outlook for the third time this year, and we expect an even stronger fourth quarter. Growth is broad-based with record AA&S margins and strengthening demand in jet engines and airframe. We're focused on executing against that demand and carrying our momentum into 2027. Now let's open the line for questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Richard Safran with Seaport Research Partners.

**Richard Safran** (Analysts):
I have a question, and if it's okay, I have a follow-up. But this could be for both of you. But Kim, optically, there seems to be a bit of a contradiction between what I heard about from your opening remarks and about demand signals. And yet we have a slower-than-expected ramp at Airbus, and we all know Boeing recently just did a reset. So I think that destocking is on the minds of a lot of people and the impact to ATI. So I mean, simply put, do you see the potential here for destocking or an OE inventory correction? If no, maybe you could discuss why the difference between what the OEs are saying and what you're saying about demand signals.

**Kimberly Fields** (Executives):
Thanks, Rich. Yes, I have read some of that -- heard some of that. And from our perspective, we are not seeing any change or impact to our demand or order book, including going into 2027. And as you said, from ATI's perspective, we stay very closely aligned with our customers on their schedules and their material needs. We've talked earlier in the year, the airframe inventories are largely normalized at this point. Customer orders are very closely aligned right now with their production schedules. And I don't see any signs of any kind of inventory changes that are coming. I'd say, if I just will go back at the beginning of the year, we talked about this is going to be a story of two halves and the first half being relatively flat and then accelerating as we go into the second half. And that's what we're seeing with our material -- our materials order well in advance of it being used in the production. And so, again, that alignment is really important, and those orders are already on our books. And we're seeing that acceleration. As you saw, airframe was up 11% year-over-year, but maybe more importantly, up 14% sequentially. And so, I do think that the normalization of inventory is largely behind us. We do have good alignment with the production rates. And maybe the other thing to point out is our materials go and feed into multiple programs at these airframers and there are some other 87 and other platforms that are continuing to step up and ramp. And so, what I see as I look forward is opportunities for continued growth as we go through the rest of this year into next year.

**Operator** (Operator):
[Operator Instructions] Your next question comes from the line of Seth Seifman with JPMorgan.

**Seth Seifman** (Analysts):
I wanted to ask about within AA&S, we've seen some really outstanding performance. When we think about the sustainability of that over time and both -- any headwinds that might be coming from unique goodness in this year as well as tailwinds from the good performance in the business and the new contracts that you're signing. We've seen significant increases in the margin guidance for this year. So how do we think about the sustainability of that?

**James Foster** (Executives):
Thanks, Seth. Yes. So let me remind you that we fundamentally structurally change that segment. And that transformation started a couple of years ago when we exited the commodity standard stainless business. And over time, we've transformed that business. And we've really done that through kind of three different pillars. Number one, from a pricing and commercial contract standpoint, we've really worked to lock in some of that, specifically aerospace and defense work and some of those other markets that were more core to ATI. So we've done a good job from a pricing and commercial standpoint to really align ourselves with some of these LTA and these long-term durability opportunities. 
We've also transformed from a mix standpoint. When I think about the transformation, if you look back in 2021, AA&S was 18% aerospace and defense compared to 45% aerospace and defense here as we exited Q3. So we've done a lot of mix shift work to that segment. In addition, we've worked a lot on the productivity and efficiency enabled through our Elevation operating model. So we've really, kind of, transformed that business. And if you look at where we were just last year, kind of, in that high teens and then where we've transformed most noticeably here in the second quarter when we stepped up to that mid-20s. The business has structurally transformed, and we now see the full year 2026 margins in that low to mid-20% range with Q4 in the mid-20s. So overall, I feel that this segment is sustainable and durable and will remain in that, kind of, mid-20s range for the foreseeable future.

**Operator** (Operator):
Your next question comes from the line of Gautam Khanna with TD Cowen.

**Gautam Khanna** (Analysts):
I was wondering if you could give us some color this year, next year or the following year on pricing opportunities at HPMC given what you described as a pretty tight supply-demand environment. And then just relatedly on the ramp of these alloys that you mentioned dampened margins by 200 bps relative to your plan. I just wanted to be clear on what the actual plan was for the quarter, just so we can calculate what the normal underlying should be. Was it just 200 basis points higher? Or was it -- would it have been 200 basis points higher or even more than that?

**Kimberly Fields** (Executives):
Sure, sure. Thanks. So yes, as I look at pricing, this quarter, the uplift was about 2/3 price -- about -- and mix and about 1/3 volume. So, we are starting to see the benefit of those contract resets and some of the other work that we were talking about earlier in the year. I do see that continuing as we go forward. We do have several contracts that will come up for renewal. I think the other important thing, as you mentioned, in this quarter, we're continuing to win new business as well. And that sixth alloy in the hot section that we won earlier this year, and we've already increased our share on that continues to expand our content in these markets and give us opportunity to capture both volume as well as mix and price uplift. 
As you said, this quarter, they had a solid -- we had a solid quarter in HPMC. It was up 20% year-over-year, an EBITDA increase. But, as you said, that margin came in about 200 basis points below what our plan was. So that would have been about another $15 million to $20 million of additional EBITDA that we would have saw if we had ramped quicker. But I think the important thing to remember, as I mentioned, is we won this business at the beginning of this year, moved that alloy from qualification into production in just 9 months. And that really speaks to the technical capabilities of the team and the hard work that's going on there because qualifying these advanced engine alloys are very demanding. And that's what creates a significant barrier to entry and the moat competitive advantage around our business. For that alloy in particular, we're one of only two that are producing that worldwide. And today, we now produce all six of those advanced alloys in the hot section that are coming from non-captive suppliers. No other company can make that claim. So these engines are designed for decades of service, and that ramp impact is really a temporary impact for -- that's supporting a growth opportunity that spans decades.

**James Foster** (Executives):
And, Gautam, the way I think about it is that 200 basis points of margin compression was really, kind of, costs associated with the inefficiencies of, kind of, that ramping. And so, as we think about it transitioning into the fourth quarter, we expect that to be less than a quarter. It's going to be fully behind us as we exit 2026. So we do think that these are, kind of, near term. And as Kim mentioned, this is going to enable us to be in a position that's going to have 3-plus decades of profitable growth opportunities. So there are some near-term costs here in Q3, significantly abating here as we go into Q4 and then getting fully behind us. That's going to be a good thing, though, overall. It's a good investment. Unfortunately, it is causing some near-term margin compression. But as I said, we expect that to be fully behind us as we exit Q4.

**Operator** (Operator):
Your next question comes from the line of Myles Walton with Wolfe Research.

**Myles Walton** (Analysts):
Kim, you made a comment about an anecdote with an engine OEM saying that they would take twice your capacity if you had it today. I guess, is there a specific area where your engine products, the pull is the highest? And if I just look at your engine products in aggregate, taking you 5 years to double your output. So I'm not trying to take the comments literally, but more from a perspective of how quickly do you think you grow your engine products sales? And do you actually think it accelerates from the pace that you've had over the last 5 years, which is what it took to double the sales?

**Kimberly Fields** (Executives):
Yes. So that comment, our materials and our forgings go into both MRO and new engine production. Today, it's about 50-50 between the 2, and that's been consistent since the pandemic. And just to share with folks, for us, when we make a forging, we -- and send that to the customer, we don't know if it's going into a new engine build or into the MRO stream. And so, for us, it's the same part, it's the same price, it's the same margin. And so, to your point, I'm thinking here around the 5-year growth standpoint. I do see continued growth as we go forward. We've got very strong positions. Rob just made that point with this sixth alloy several -- many of those, five of those were sole source supply. 
So as these next-gen engines continue to grow, continue to hit their shop visits and those major shop visits where they're replacing the disks and the hot section parts, we'll see that continued growth. This quarter, very strong growth, 39% year-over-year. We do -- we did raise our guide that we anticipate low to mid-20% as we go through the rest of this year. But I do think that continues to grow as we go forward just based on the conversations I'm having with our customers, their expectation both of upgrade packages and shop visits of that next-generation alloy and engines coming in. 
So I'd have to take a look at it. We don't have -- we're not providing any forward guidance today on that growth. But I would say that this growth that we've had over the last year, we don't see that abating and demand continues to be very strong as we look at next year. We'll share some more of that, and I'll take that question when we get to Investor Day, and we'll share more of our outlook over the next 3 to 5 years, and we'll answer that question more fully.

**Operator** (Operator):
Your next question comes from the line of David Strauss with Wells Fargo.

**David Strauss** (Analysts):
Now with AA&S margins at these levels in a similar range as HPMC, could you just talk about kind of margin differential between jet engine and kind of airframe or structural? I mean I was under the impression engine is much higher margin, but maybe that's not the case. If you could just touch on that. And any thoughts, Rob, maybe on the CapEx plan from here? Is it -- as we look beyond this year, should we think relatively stable as a percent of sales? Or any framing you could do there?

**Kimberly Fields** (Executives):
Great. Well, I'll take the first half as we think about the margin differentials, and I'll let Rob talk a little bit about the capital and our outlook there. Historically, what you said would be true. Engine has been the most accretive and the highest value products for us. But what I would say has happened since we came out of the pandemic is those margin differentials have compressed. And a lot of it comes down to -- we're seeing strong demand, as you mentioned, in airframe. We're seeing strong demand in defense. We're seeing strong demand in specialty energy. And those products are made on the same assets, those fungible assets that can be directed towards different product flows. And so customers recognize that. And I think that's unusual. It's different than it's been in the past that they've had to think about these other market demands coming into these assets. And early on, I think I shared that story that some of our customers were a little caught off guard when they heard our lead times, which are very extended. I shared some of that. PQ titanium is out 20 months and iso forgings are out more than 2 years. 
So they recognize that if they want that capability and that capacity that they have to look at higher pricing to get on those assets and get that capacity. Now, that said, that is also what's helping to drive, and I'll let Rob get into the capital, but that's also driving this investment and focus by customers at bringing customer capital, co-funding to that capital. So they have access to that limited differentiated capabilities that we provide. 
And so you've seen we've announced several of those projects. We haven't announced all of those projects. I think that's continuing with the recent acquisition announcement where customers are looking at that differentiated important capacity and products to help support their ramp, and they're investing in that. And that's what we've been talking about here for the good part of a year now. But, Rob, I'll let you talk a little bit about our outlook as we think about capital.

**James Foster** (Executives):
Yes. So we're not going to be doing formal, kind of, updated guidance for the longer term. I'll be giving some additional color and context here at the upcoming Investor Day on November 12. But what I can say is how I'm thinking about it. And the way I'm thinking about organic growth is I definitely see a pipeline of really interesting projects for us -- but we're going to be very disciplined as we go through our approach. 
First, we're going to be looking to unlock efficiencies that already exist. Elevation is going to be that business model that we use to unlock all of the capacity that already exists on our existing footprints and assets. The second part of that discipline is we're going to be looking for alignment with our customers. And generally, that comes through either capital commitments and customer-funded capital or contracts. So we're going to be very disciplined as we go through the organic growth process. And I can say the areas that are the most intriguing to us right now are the areas that ATI has a differentiated moat and differentiated capability, such as nickel superalloys, premium quality titanium, hafnium and zirconium areas, isothermal forging. 
So we've already announced CapEx projects within the nickel superalloys and the PQ titanium. The areas that are interesting, as I said, would be those differentiated moats. So more information to come, but I can say that we don't have any plans for any monolithic assets. We're going to be very disciplined. We're going to be very rational and aligned with our customers and more information to come.

**Operator** (Operator):
Your next question comes from the line of Pete Skibitski with Alembic Global.

**Peter Skibitski** (Analysts):
Kim, can you maybe update us on how things are progressing at the new facility in Mexico and then also the new -- with the new furnace in Richland, I think they were kind of -- you had some sticking points there last quarter. I don't think they're related to the issue this quarter with the nickel alloys. But can you maybe update us on how things are progressing there productivity-wise?

**Kimberly Fields** (Executives):
Sure, Pete. Yes. And, you're right, they're not related to each other. This quarter was really around that ramping of that new product line that we won earlier this year. But both of those are making good progress, and we remain on plan to our milestones. On the Mexico side, we shipped about 25% of the deferred revenue that I talked about in Q3 and we expect to ship the balance of that in Q4. If you remember, the revenue was around $30 million to $40 million that we deferred from the second quarter. So that's about $10 million last quarter and third quarter and then the rest of it this year. I think the positive thing is that we'll leave this year at a run rate that matches or exceeds -- slightly exceeds what our original footprint was as we enter 2027. 
And so, the team has done a fantastic job. They tripled output since last quarter. They are, like I said, well on track to our plan. As we look at EB2 in Richland, the furnace in Richland that you talked about, we're making progress there, but not all of those qualifications are complete. We expect the qualification of the standard or most of our standard quality products to be done by the end of the year and will be in production as we go into next year. 
Those more technically demanding engine alloys are going to continue through qualification into 2027 with us completing those qualifications as we get into the mid-2027 time frame. And, again, just to remind everybody, this is important because we built that furnace in Richland to give us flexibility to allow us to make both standard quality as well as that very highly differentiated premium quality titanium and gives us flexibility to be able to meet the needs of engine products as well as defense. And so, those go into defense products, too. 
And so, I think the bottom line, though, is they're on track. They're making good progress. We'll leave this year with the majority of that behind Mexico will completely be at run rate. In fact, it will be higher than our original footprint. And then our titanium qualifications in Richland will be well ahead.

**Operator** (Operator):
Your next question comes from the line of Scott Deuschle with Deutsche Bank.

**Scott Deuschle** (Analysts):
Can you comment on whether the forging business has much wide-body exposure? And then if so, what you're seeing in terms of wide-body forging lead times and the progress you're making on ramping output there? And then for Rob, can you be any more precise on the margin you're expecting at HPMC for the fourth quarter?

**Kimberly Fields** (Executives):
Sure, Scott. Yes, wide-body is starting to pick up. I think I talked about last quarter that we started to see some emergent orders with materials going into the airframers, in particular, opportunities to grow our product content and our share around those landing gear alloys that are very complex and difficult to produce and allow us to use our differentiated capabilities. 
On the forging side, we do have wide-body exposure primarily through the engine side. Just to remind you, engines of our A&D segment, our A&D revenues is about 40% of our overall company. And so, most of our exposure is going to come from those large engines for the widebodies.

**James Foster** (Executives):
And Scott, in terms of how we see the HPMC Q4 margins, we see that mid-20s range. So we're going to see a sequential step-up from Q3 to Q4 that would land us in the mid-20s for the HPMC segment in Q4.

**Operator** (Operator):
Your next question comes from the line of Samuel McKinney with KeyBanc Capital Markets.

**Samuel McKinney** (Analysts):
The AA&S margins took another meaningful step upward. First, can you just confirm that the third quarter represents the first full quarter of shipping under the new naval nuclear contract? And second, any more color you can provide us around the incremental margin impact that, that had on overall AA&S given the continued segment mix shift to A&D?

**Kimberly Fields** (Executives):
Yes. So yes, this is the first full quarter we have on that new contract. But I'd say the step-up also encompassed demand coming from our commercial nuclear customers as well. You saw a significant step-up year-over-year in our specialty energy of 49%. That was being driven by both gas turbines as well as those commercial nuclear customers. And so, both of those as well as increased demand exceeding supply around that zirconium and hafnium products that we talked about last quarter.

**James Foster** (Executives):
Yes. And as you think about the margins there, as we talked earlier, the sustainability of these, we expect the kind of mid-20s for Q4. And from an incremental, we guided the full year incrementals to about 50%, but seeing the AA&S segment a bit above the 50% level for the full year. So overall, AA&S is very well positioned for sustainable profitability in this kind of mid-20s range.

**Rob Rengel** (Executives):
Operator, we have time for one final question before Kim closes the call.

**Operator** (Operator):
Your final question comes from Andre Madrid with BTIG.

**Andre Madrid** (Analysts):
Real quick, I kind of wanted to stick on Specialty Energy. How -- can you maybe just parse out the bigger moving pieces there for us to really understand what's driving growth? I understand commercial energy is -- nuclear energy is probably the largest moving piece there right now. But also, can you talk more to the IGT contributions in the quarter and maybe in the long term as well as you see it moving out? And then I guess, beyond that, I want to kind of go back to jet engine and maybe talk about some of the demand trends you've been seeing. Obviously, it looks pretty robust. It remains around half of what you guys are doing on jet engine. But is there any kind of flattening related to higher fuel prices from the Iran war? Or are you not seeing that as upstream yet?

**Kimberly Fields** (Executives):
Okay. Great, Andre. Yes. So on Specialty Energy, as you said, I mentioned they had a great quarter, up 49% year-over-year, 36% sequentially. So strong customer demand. As you said, the majority of that is the nuclear energy, but demand remains healthy in both the commercial nuclear and the industrial gas turbines. So we're seeing demand coming from both sides. I think part of what you saw in this quarter is that our fungible flexible assets allow us to balance production between specialty energy and defense as our customer orders and their needs evolve. So that can lead to some quarter-to-quarter variability in shipments. We talked a little bit about that last quarter as we manage that capacity based on customer orders and priorities. But Specialty Energy growth continues, and our underlying demand view of the market has not changed. So we continue to expect mid-teens growth for the full year there. 
Now on the jet engine side, as you said, we can talk a little bit more about that. We haven't seen any impact from those fuel prices, something that clearly that we're paying attention to. But as I mentioned, that comment from the customer that we had just last week, engine demand continues to grow and be strong. And what I'm seeing is coming from both the new engine as well as the MRO. As I said, for us, those forgings that we make and those materials that we send go into both demand streams. And so, we don't necessarily know any specific part or shipment, which direction that's going. So it's -- for us, it's the same part, same price, same margin. And we have not seen a step down in those -- in demand as we're looking at that. As we're talking with our customers, it's -- they're looking at both the MRO. And even if aircraft start to be retired because of higher fuel costs, the next-gen engines are actually -- that transition is beneficial for ATI because those next-gen engines have 2x the content of those legacy engines. And so, those really pull into those differentiated materials as well as those isothermal forgings, which are two of those highly differentiated spaces that Rob just talked about.

**Operator** (Operator):
We have reached the end of the Q&A session. I will now turn the call back to Kim Fields for closing remarks.

**Kimberly Fields** (Executives):
Great. Thank you, everyone, for joining us and for your questions. As we've been talking about today, we see strong demand across the markets that we serve and the differentiated capabilities really position ATI to capture that demand. And I think that's what you saw with that strong lift across all of our markets. We're focused on executing well and converting that demand into earnings and cash and finishing 2026 strong and then continuing to build on that progress in 2027. Thank you.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ATI_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：CFO 公布上調後全年調整後 EBITDA 區間（原話："range of $1.135 billion to $1.185 billion."）
- 2026-08-06｜CFO｜guidance：CFO 給 Q3 調整後 EBITDA 區間 305–315 百萬美元與 EPS 區間（原話："$315 million, translating to adjusted EPS of $1.31 to $1.37."）
- 2026-08-06｜CFO｜guidance：CFO 說明財測中點隱含 Q4 EBITDA 約 3.35 億美元（原話："approximately $335 million of EBITDA in Q4."）
- 2026-08-06｜CFO｜guidance：CFO 稱 Q4 為 2026 年銷售與獲利最強的一季（原話："as our strongest quarter of 2026 for sales and profit"）
- 2026-08-06｜CFO｜guidance：CFO 表示不提供 2027 財測（原話："While we are not providing 2027 guidance today"）
- 2026-08-06｜CFO｜guidance：CFO 給全年調整後自由現金流區間（中點調升 8,000 萬）（原話："range between $550 million and $600 million."）
- 2026-08-06｜CFO｜guidance：CFO 給全年總資本支出區間不變（原話："prior guidance at $280 million to $300 million."）
- 2026-08-06｜CEO｜guidance：CEO 維持噴射引擎全年營收高十位數成長（原話："high teens jet engine revenue growth for the full year."）
- 2026-08-06｜CEO｜guidance：CEO 維持機身全年中至高個位數成長、下半年加重（原話："mid- to high single-digit full year airframe revenue growth"）
- 2026-08-06｜CEO｜guidance：CEO 將國防全年成長預期上調至高十位數（原話："expectation for full year defense growth to the high teens"）
- 2026-08-06｜CEO｜guidance：CEO 維持特殊能源全年中十位數成長（原話："mid-teens Specialty Energy revenue growth for the full year."）
- 2026-08-06｜CFO｜margin：CFO 給全年合併 EBITDA 利潤率落在 20% 出頭（原話："adjusted EBITDA margins now projected in the low 20% range."）
- 2026-08-06｜CFO｜margin：CFO 將全年合併增量利潤率預期由 40% 提高到 50%（原話："in the range of 50%. This is an improvement over the 40%"）
- 2026-08-06｜CFO｜margin：CFO 將 AA&S 全年利潤率由上季的高十幾%上調至 20% 出頭（原話："an improvement over the upper teens level we"）
- 2026-08-06｜CFO｜margin：CFO 稱 HPMC 全年 EBITDA 利潤率維持 20% 中段（原話："for HPMC in the mid-20% range, consistent with our outlook"）
- 2026-08-06｜CFO｜margin：CFO 於備稿中稱 AA&S EBITDA 利潤率前瞻為持續高於 20%（原話："we see AA&S EBITDA margins consistently above 20%"）
- 2026-08-06｜CEO｜margin：CEO 於問答中稱 AA&S 往後可達 20% 中段（原話："we can see AA&S in the mid-20% range going forward."）
- 2026-08-06｜CEO｜margin：CEO 說明剔除資產出售利益後 AA&S 的底層利潤率口徑（原話："an underlying EBITDA margin of approximately 22%"）
- 2026-08-06｜CEO｜margin：管理層拆解 Q2 EBITDA 超標數字時扣除 AA&S 資產出售利益（原話："Excluding a $10 million asset sale gain"）
- 2026-08-06｜CFO｜margin：CFO 報告 AA&S Q2 利潤率年增 930 bp（原話："Segment margin expanded 930 basis points to an all-"）
- 2026-08-06｜CFO｜margin：CFO 報告 HPMC Q2 利潤率 24.1%（原話："basis points from the same period last year to 24.1%."）
- 2026-08-06｜CEO｜margin：CEO 量化 HPMC 由上半年遞延到下半年的營收規模（原話："around $30 million to $40 million of revenue that moved"）
- 2026-08-06｜CFO｜margin：CFO 說明海軍核能新合約拆分為 2/3 價格組合、1/3 數量（原話："2/3 price mix, 1/3 volume in that contract."）
- 2026-08-06｜CFO｜margin：CFO 稱新合約的量價較預期早入帳於 AA&S（原話："financials a bit earlier than we were anticipating."）
- 2026-08-06｜CFO｜commitment：CFO 稱 HPMC 展望建立在已簽約訂單上（原話："contracts in place. This is not speculative."）
- 2026-08-06｜CFO｜commitment：CFO 重申自由現金流轉換率目標在 90% 以上（原話："free cash flow conversion at 90% or greater"）
- 2026-08-06｜CEO｜commitment：CEO 承諾各項新增產能投資須達內部 30% 報酬門檻（原話："have to meet our 30% return thresholds internally"）
- 2026-08-06｜CEO｜commitment：CEO 稱先榨取既有資產再投資新產能（原話："before we invest in new capacity"）
- 2026-08-06｜CEO｜commitment：CEO 預告今年稍後召開投資人日（原話："We look forward to sharing more at our Investor Day"）
- 2026-08-06｜CEO｜commitment：CEO 說明鎳熔煉擴產新 VIM 爐時程（原話："new VIM furnace coming online by the end of 2027"）
- 2026-08-06｜CEO｜commitment：CEO 稱鎳投資將於 2028 前帶來約 3.5 億美元增量年營收（原話："we will deliver approximately $350 million of"）
- 2026-08-06｜CFO｜capital_allocation：CFO 稱庫藏股是增量自由現金流的優先用途（原話："We view them as the most efficient way to return capital to"）
- 2026-08-06｜CFO｜capital_allocation：CFO 報告庫藏股剩餘授權額度（原話："we have $495 million remaining"）
- 2026-08-06｜CFO｜capital_allocation：CFO 報告 Q2 資本支出中客戶直接出資的部分（原話："including $23 million funded directly by customers."）
- 2026-08-06｜CFO｜capital_allocation：CFO 報告 Q2 管理營運資金占營收比（原話："percentage of sales at the end of Q2 was 34%"）
- 2026-08-06｜CFO｜capital_allocation：CFO 提到推動鍛造原料客戶寄售以改善營運資金（原話："customer consignment strategy for forging input material"）
- 2026-08-06｜CEO｜risk：CEO 說明 HPMC 因墨西哥新廠與 EB2 認證時程使部分出貨遞延（原話："qualification timing at"）
- 2026-08-06｜CFO｜risk：CFO 解釋 EBITDA 上調幅度大於自由現金流上調的兩個原因之一為應收帳款時點（原話："it's the timing of conversion through accounts receivable."）
- 2026-08-06｜CFO｜risk：CFO 表示為 2027 年初備貨而增加庫存（原話："we do plan on a little bit more inventory as we prepare"）
- 2026-08-06｜CEO｜customer：CEO 報告記錄訂單餘額與年增、季增（原話："another record $4.4 billion. That's up 18% year-over-year"）
- 2026-08-06｜CEO｜customer：CEO 稱約 70% 在手訂單預期於未來 12 個月轉為營收（原話："About 70% of that backlog we expect to convert"）
- 2026-08-06｜CEO｜customer：CEO 給鎳合金交期（原話："about 12 months on nickel alloys"）
- 2026-08-06｜CEO｜customer：CEO 給優質鈦交期（原話："20 months on the premium quality titanium"）
- 2026-08-06｜CEO｜customer：CEO 給等溫鍛件交期（原話："above 24 months on isothermal forgings"）
- 2026-08-06｜CFO｜customer：CFO 說明海軍核能新合約規模與期限（原話："essentially a $1 billion revenue contract over 5 years."）
- 2026-08-06｜CEO｜customer：CEO 稱海軍核能續約延至 2030 並改善價格與組合（原話："through 2030 with improved pricing and product mix."）
- 2026-08-06｜CEO｜customer：CEO 稱已開始收到戰斧飛彈計畫訂單（原話："receiving orders in support of the Tomahawk program."）
- 2026-08-06｜CEO｜customer：CEO 稱飛彈相關營收季成長 4 倍（原話："That revenue is up 4x in the quarter."）
- 2026-08-06｜CEO｜customer：CEO 稱機身訂單簿已延伸到 2027（原話："we've got order books now extending into 2027"）
- 2026-08-06｜CEO｜competition：CEO 稱 ATI 是西方僅三家合格高純度鉿鋯生產商之一（原話："1 of 3 qualified producers in the Western"）
- 2026-08-06｜CEO｜competition：CEO 提到中國限制出口與 ATI 能力價值的關聯（原話："With China limiting exports to these markets"）
- 2026-08-06｜CEO｜competition：CEO 稱 ATI 生產 7 種最先進鎳基超合金中的 6 種（原話："produce 6 of the 7 most advanced nickel-based super alloys"）
- 2026-08-06｜CEO｜product：CEO 稱新世代引擎上的 ATI 含量為舊平台兩倍以上（原話："than double that of legacy platforms"）
- 2026-08-06｜CEO｜product：CEO 報告 Elevation 帶來的產能提升（原話："throughput by 30% in ultrasonic inspection, 15% in"）
- 2026-08-06｜CEO｜product：CEO 稱 AA&S 的 A&D 占比往後維持並可能上升（原話："mix of A&D continues to stay at that level and it will"）

### ATI_Shareholder_Analyst_Call_ATI_Inc_20260514.md
- 2026-05-14｜Robert S. Wetherbee｜risk：執行董事長 Wetherbee 表示這是他擔任董事長的最後一次正式行動（領導層交接）。（原話："This is my last official act as the Executive Chairman"）
- 2026-05-14｜Robert S. Wetherbee｜risk：Kim Fields 自即日起兼任董事會主席，並仍為總裁暨 CEO。（原話："Fields as President, CEO, and, as of now, Board Chair."）
- 2026-05-14｜Robert S. Wetherbee｜competition：Wetherbee 稱團隊已轉型並成為有差異化的市場領導者（無數字佐證）。（原話："differentiated itself as a market leader."）
- 2026-05-14｜Robert S. Wetherbee｜product：Wetherbee 以航空應用說明 ATI 產品的重要性（無細節）。（原話："And you can't fly without ATI either."）

### 問答異常語氣（迴避／改口／保留）
- ATI_Q2_2026_Earnings_Call_20260806.md｜問：David Strauss 問 2027 是否可沿用 50% 增量利潤率、Q4 運行率是否有一次性因素｜答法：CFO 未給 2027 數字，稱「directionally makes sense」並說 40–50% 增量區間合理，但明說不給 2027 細部指引
- ATI_Q2_2026_Earnings_Call_20260806.md｜問：Richard Safran 追問 AA&S 利潤率潛力是否願給更具體數字｜答法：備稿中 CFO 稱「consistently above 20%」，問答中 CEO 改稱「mid-20% range going forward」，同一場說法由 20% 以上變為 20% 中段
- ATI_Q2_2026_Earnings_Call_20260806.md｜問：Seth Seifman 問是否會在 Slide 6 之外增加產能投資及決策方式｜答法：CEO 談 Elevation 與 30% 報酬門檻，未點名 Slide 6 以外的新增產能項目或金額

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
{"date":"20261013","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤ 153 美元（FY2027 共識 6.37 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","irr_base_pct":3.5,"ev5y_pct":12.4,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.2,"ev5y_pct":12.4,"irr_base_pct":3.5,"max_dd_pct":-65,"bull_5y_price":348.0,"bear_5y_price":79.5,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤ 153 美元（FY2027 共識 6.37 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","price_at_dd":187.98,"archetype":"循環/商品","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
