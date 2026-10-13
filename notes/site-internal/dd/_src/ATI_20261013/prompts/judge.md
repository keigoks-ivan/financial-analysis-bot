你是 stock-analyst **v20 判斷 agent**，標的 ATI（20261013）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ATI","date":"2026-10-13","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261013/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261013/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_sales_gaap","label":"Sales (GAAP)","value":1261.1,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）"},"note":"未取得"},{"id":"f_kpi1_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代之）","value":284.4,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M（利益率 22.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）"},"note":"超出公司自家 Q2 指引上緣（標題：Exceeds the High End of Q2 Guidance）；分析師共識數字未取得"},{"id":"f_kpi2_operating_income_gaap","label":"Operating income (GAAP)","value":220.0,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M（利益率 17.4%，由新聞稿數字推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）；含 9.9M 廠房出售利得、23.6M 特殊項目稅前費用"},"note":"未取得"},{"id":"f_kpi3_adjusted_free_cash_flow","label":"Adjusted free cash flow","value":68.6,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）；營業現金流 131.8M，capex 68.6M"},"note":"未取得"},{"id":"f_kpi5_backlog","label":"Backlog","value":4400,"period":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","unit":"USD M（YoY +18%，創高）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026（季末 2026-06-28，公告 2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）"},"note":"不適用"},{"id":"f_kpi6_guidance_q3_2026","label":"Guidance：Q3 2026","value":"Adj EBITDA 305–315M；Adj EPS 1.31–1.37","period":"Q2 2026 新聞稿（2026-08-06）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 2026 新聞稿（2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）；未提供營收指引"},"note":"未取得"},{"id":"f_kpi7_guidance_fy2026","label":"Guidance：FY2026（上修）","value":"Adj EBITDA 1,135–1,185M；Adj EPS 4.90–5.18；Adj FCF 550–600M","period":"Q2 2026 新聞稿（2026-08-06）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 2026 新聞稿（2026-08-06）","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）"},"note":"本站 FY1 EPS 共識 5.12（2026-10-08 快照，位於指引區間內）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-06","period":"2026-08-06","unit":"date","basis":"距今 48 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-06"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ati_gross_margin_pct","label":"ATI 毛利率","value":23.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ati_operating_margin_pct","label":"ATI 營業利益率","value":15.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ati_fcf_margin_pct","label":"ATI FCF 利潤率","value":11.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hwm_gross_margin_pct","label":"HWM 毛利率","value":36.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hwm_operating_margin_pct","label":"HWM 營業利益率","value":27.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hwm_fcf_margin_pct","label":"HWM FCF 利潤率","value":19.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_crs_gross_margin_pct","label":"CRS 毛利率","value":30.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_operating_margin_pct","label":"CRS 營業利益率","value":22.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crs_fcf_margin_pct","label":"CRS FCF 利潤率","value":11.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cstm_gross_margin_pct","label":"CSTM 毛利率","value":16.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSTM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cstm_operating_margin_pct","label":"CSTM 營業利益率","value":8.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSTM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cstm_fcf_margin_pct","label":"CSTM FCF 利潤率","value":2.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSTM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtrn_gross_margin_pct","label":"MTRN 毛利率","value":16.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtrn_operating_margin_pct","label":"MTRN 營業利益率","value":6.35,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mtrn_fcf_margin_pct","label":"MTRN FCF 利潤率","value":1.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_0_6","label":"SBC（上半年累計，占上半年營收約 0.6%）","value":14.1,"period":"2026 上半年（至 2026-06-28，公告 2026-08-06）；新聞稿未單列 Q2","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"2026 上半年（至 2026-06-28，公告 2026-08-06）；新聞稿未單列 Q2","citation":"公司 Q2 2026 新聞稿（8-K EX 99.1）；占比 = 14.1 ÷ (1,261.1+1,151.5)"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":187.98,"period":"2026-10-12（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.12 → 5.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.37 → 6.37）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.5 → 7.5）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.12,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.37,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.5,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":14.54,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 4.47 → 5.12（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":55.13,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.43,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.73,"period":"2026-10-12（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-12（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-12（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-12（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":37.47,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 5.12，分子＝快照價 191.84","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-10-13","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-13"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":1409.0,"period":"2026-10-13","unit":"USD m","basis":"yfinance 最新一季：總債務 2192.0、現金 783.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":136.17,"period":"2026-10-13","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":27006.31,"period":"2026-10-13","unit":"USD m","basis":"市值 25597.31 ＋ 淨負債 1409.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":5143.96,"period":"2026-10-13","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":5651.62,"period":"2026-10-13","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（8 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.25,"period":"2026-10-13","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"ATI FY2025 10-K 列示 HPMC 主要競爭者：鈦合金對 Howmet Aerospace、傳統鎳基與特殊鋼對 Carpenter Technology，另有 Precision Castparts（Berkshire）與 Aubert & Duval（精密鍛件）。","source":"ATI Inc Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":null,"as_of":"2025-12-28","retrieved_at":"20261013","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Argus 報導（Farnborough 展期間）：2026 上半年引擎 OEM 交付顯著增加，拉動熔煉、鑄造、鍛造廠材料需求；引擎 OEM 與特殊合金廠過去一年大幅投資擴充熔煉、鑄造、鍛造產能或鎖定既有供應。as_of 為展期（2026 年 7 月）近似日，頁面未逐字確認。","source":"Argus Media (Farnborough 2026 report)","url":"https://www.argusmedia.com/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"ATI 宣布約 7,000 萬美元鎳基超合金粉末擴產，其中相當部分用於滿足與噴射引擎 OEM 延續至下個十年的長約。","source":"ATI to expand nickel-based superalloy powder capabilities (metal-am.com / metal-powder.tech)","url":"https://www.metal-am.com/ati-to-expand-nickel-based-superalloy-powder-capabilities-for-additive-manufacturing-sector/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Carpenter Technology 預期 2026 資本支出 2.2–2.4 億美元，投向自有引擎合金與高毛利機會，訂單連續數季成長（Zacks）。","source":"Zacks: ATI vs. CRS: which specialty metals stock should you invest in now","url":"https://www.zacks.com/stock/news/2889540/ati-vs.-crs:-which-specialty-metals-stock-should-you-invest-in-now","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"ATI FY2025 10-K 揭露：任何年度皆無單一客戶占銷售超過 10%，核心終端市場為航太國防、特殊能源、電子、醫療。","source":"ATI Inc. Form 10-K FY2025 (period ended 2025-12-28)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":"No single customer accounted for more than 10% of sales for any year presented. The core end markets for ATI's products are customers in the aerospace & defense, specialty energy, electronics, and medical markets.","as_of":"2025-12-28","retrieved_at":"20261013","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"ATI 與 Airbus 簽多年期鈦板／片／billet 合約（2025 年 5 月）；Boeing 鈦協議延長且非排他。搜尋結果未找到任一客戶導入第二供應商或將鈦材自製（in-house）的來源。","source":"ATI IR press release: ATI signs multi-year agreement with Airbus for titanium plate, sheet and billet","url":"https://ir.atimaterials.com/news-events/news-details/2025/ATI-signs-multi-year-agreement-with-Airbus-for-titanium-plate-sheet-and-billet/default.aspx","excerpt":null,"as_of":"2025-05-01","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"ATI FY2025 10-K 指出 HPMC 分部約 92% 營收來自航太與國防市場，並點名 Boeing、Airbus、Embraer（機身）與 GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran（發動機）為少數大型客戶群；搜尋摘要未取得單一客戶占營收百分比。","source":"ATI INC - Form 10-K - FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"GE Aerospace 2026 Q2 業績優於預期並上調全年調整後 EPS 指引至 $7.65-$7.85（原 $7.10-$7.40）；CEO 稱主要限制在供應端而非需求。另有報導稱 2026 年初 GE 因中東衝突下調全年航班起降展望。","source":"WebSearch 摘要（GE Aerospace Q2 2026 results 報導）","url":null,"excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Argus（Farnborough 後報導）：引擎 OEM 2026 上半年出貨大增，拉動熔煉、鑄造、鍛造端訂單；航空級(PQ)鈦 billet 需求強，供應商報價交期 3–6 個月；新合金產能預期 2027 後半至 2030 陸續投產。","source":"Argus Media, Jet engines driving nickel, PQ titanium demand","url":"https://www.argusmedia.com/en/news-and-insights/latest-market-news/2860247-jet-engines-driving-nickel-pq-titanium-demand","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261013","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ATI 稱其最差異化產品（超合金鎳、PQ 鈦、等溫鍛件、特殊合金）交期正在拉長。","source":"ATI Q2 2026 earnings call (MarketBeat 摘要)","url":"https://www.marketbeat.com/instant-alerts/ati-q2-earnings-call-highlights-2026-08-07/","excerpt":"lead times are extending for our most differentiated products, super alloy nickels, premium quality titanium, isothermal forgings and exotic alloys","as_of":"2026-08-07","retrieved_at":"20261013","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ATI Q2 2026 積壓訂單創高 $4.4B（年增 18%），約 70% 預計 12 個月內轉為營收；2026 指引上調至調整後 EBITDA $1.135–1.185B、EPS $4.90–5.18、FCF $550–600M；航太與國防銷售 +13%，國防 +36%，海軍核能協議續約約 5 年 $1B。","source":"MarketBeat ATI Q2 earnings call highlights／Zacks","url":"https://www.marketbeat.com/instant-alerts/ati-q2-earnings-call-highlights-2026-08-07/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ATI 增建鎳合金熔煉／VIM 產能，約 80% 已簽約，目標 2028 年中增加約 $350M 鎳營收；2026 年 6 月啟用墨西哥 Chihuahua 引擎零件廠。","source":"MarketBeat ATI Q4 2025 earnings call highlights；Metalnomist","url":"https://www.marketbeat.com/instant-alerts/ati-q4-earnings-call-highlights-2026-02-03/","excerpt":null,"as_of":"2026-02-03","retrieved_at":"20261013","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Argus 引 ATI 特殊材料事業總裁：轉子級材料消耗量未來五年預計增加 26%（約至 2030）。","source":"Argus Media（ATI 特殊材料總裁談話，早期報導）","url":"https://www.argusmedia.com/ja/news-and-insights/latest-market-news/2737772-ti-demand-rebound-dependent-on-inventory-draws","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Airbus 將 A320 月產 75 架目標延至 2027（因供應商爬坡不足、引擎短缺），A350 目標 2028 年月產 12 架；Airbus 2025 年底積壓 8,754 架。","source":"搜尋結果彙整（Hexcel Q3 2025 earnings／eplaneai 等）","url":"https://finance.yahoo.com/markets/stocks/articles/hexcel-hxl-q3-2025-earnings-160357040.html","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261013","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Argus 稱引擎瓶頸正在緩解（Airbus 與 Pratt & Whitney GTF 交付爭議為例外）；ATI 集中於少數大型航太 OEM 為風險；HPMC 約 $30–40M 出貨因認證時程遞延至下半年。","source":"Argus Media 2860247；Panabee／MarketBeat 彙整","url":"https://www.argusmedia.com/en/news-and-insights/latest-market-news/2860247-jet-engines-driving-nickel-pq-titanium-demand","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"ATI 2025 年 Q1 法說：年化關稅暴露約 5,000 萬美元，管理層稱透過轉嫁、關稅退稅（duty drawback）與供應鏈調整，全年獲利影響極小，維持 2025 EBITDA 指引。","source":"MarketBeat, ATI Q1 2025 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2025-5-1-allegheny-technologies-incorporated-stock","excerpt":"Despite $50 million of annual tariff exposure, management expects minimal impact on full-year earnings thanks to supply‐chain mitigation, pass‐throughs, duty drawback programs, and cost efficiencies.","as_of":"2025-05-01","retrieved_at":"20261013","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"ATI 稱生產基地多在美國本土，但部分原料因美國無法供應須進口。","source":"MarketBeat, ATI Q1 2025 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2025-5-1-allegheny-technologies-incorporated-stock","excerpt":"ATI is a US based producer with the majority of our production footprint located domestically... certain raw materials must be imported due to the lack of domestic availability","as_of":"2025-05-01","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"ATI 持有中國合資 STAL 60% 股權（寶武 40%），產品為精密軋製不鏽鋼帶，主要供亞洲電子與汽車市場；另 Section 232 對不鏽鋼板胚的排除申請曾遭商務部否決、25% 關稅仍在（舊案，非 2026 新事件）。","source":"ATI Form ARS FY2022","url":"https://www.sec.gov/Archives/edgar/data/1018963/000119312523079059/d472766dars.pdf","excerpt":null,"as_of":"2023-03-01","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026 年未搜到 ATI 被列入實體清單或出口管制的報導；搜尋亦未找到 ATI 2026 年關稅影響的最新數字（最新公司數據為 2025 年）。","source":"WebSearch 查無結果","url":null,"excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261013","affects":["triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ATI 10-K FY2025 揭露：鎳、海綿鈦、鈷、鉻鐵等原料多來自可能政經不穩的外國；鎳來源列加拿大、挪威、日本、芬蘭、南非；海綿鈦來源列日本、哈薩克、沙烏地、中國；公司稱原料可由多家供應商取得、目前供給足夠。","source":"ATI INC Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":null,"as_of":"2025-12-28","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"ATI 已終止與俄羅斯 VSMPO-AVISMA 的 Uniti 合資（原用於行銷商用純鈦產品）；10-K 警告烏克蘭衝突與現行或未來制裁可能中斷供應或影響材料價格。","source":"ATI INC Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":null,"as_of":"2025-12-28","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ATI 年報（FY2024 ARS）警告中國已實施且未來可能續行出口管制，可能限制或顯著延遲取得相關材料。","source":"ATI INC Form ARS FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000119312525065239/d942872dars.pdf","excerpt":null,"as_of":"2024-12-29","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026（截至 2026-06-28）HPMC 營收 $637.1M，Q1 2026 為 $614.3M、Q2 2025 為 $608.8M；HPMC 營收中航太與國防占 93%；管理層稱 $30–40M HPMC 出貨因認證時程遞延至下半年","source":"ATI Q2 2026 results（SEC 8-K Ex.99.1 / 搜尋摘要整理）","url":"https://www.sec.gov/Archives/edgar/data/0001018963/000162828026053856/form8-kq22026ex991.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261013","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 AA&S 營收年增約 17%（+$92.4M），主因航太與國防及傳統能源；AA&S 航太國防銷售年增 34%；公司整體營收年增 11% 至約 $1.3B；AA&S 單季營收總額未確認","source":"ATI Q2 2026 press release / MarketBeat call summary","url":"https://www.marketbeat.com/instant-alerts/ati-q2-earnings-call-highlights-2026-08-07/","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261013","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"ATI 2026 全年指引：噴射引擎營收中段十位數成長、國防低至中段十位數成長；Q1 2026 維持引擎中段十位數成長，驅動為高機隊使用率、進廠維修增加與 LEAP、GTF 平台成長；機身復甦預期 2026 下半年加速；新平台 ATI 單機含量約高 2 倍","source":"ATI Q1 2026 earnings call（Motley Fool 逐字稿／Yahoo 摘要）","url":"https://www.fool.com/earnings/call-transcripts/2026/04/30/ati-ati-q1-2026-earnings-call-transcript/","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"高階鈦與等溫鍛件交期延伸近兩年；ATI 鎳產能擴充目標為 2028 年初較 2025 年底增加 15–20%","source":"ATI Q1 2026 earnings call 摘要","url":"https://finance.yahoo.com/markets/stocks/articles/ati-ati-q1-2026-earnings-174636311.html","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261013","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"IMARC 2026 版報告列北美鈦價 2026 年 3 月 6.71 USD/kg，較前期下降 3.0%；未找到現行鎳價與 ATI 自身定價趨勢的一手來源","source":"IMARC Titanium Prices report 2026 edition","url":"https://www.imarcgroup.com/titanium-pricing-report","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"ATI 10-K 列出『替代材料使用增加或價格下降』為影響其市場地位與獲利波動的因子之一（FY2022–FY2025 10-K 皆有）；未見具體量化的替代技術威脅。","source":"ATI INC Form 10-K FY2025 (ati-20251228.htm)","url":"https://www.sec.gov/Archives/edgar/data/1018963/000162828026010140/ati-20251228.htm","excerpt":"increases in use or decreases in prices of substitute materials","as_of":"2025-12-28","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"GKN Aerospace 與美國空軍研究實驗室啟動 TITAN-AM（840 萬美元），推進線材雷射金屬沉積用於大型鈦機身結構的工業化，屬鈦鍛件的近淨形替代/補充路徑。","source":"aeromorning.com: GKN Aerospace and U.S. Air Force advance additive manufacturing","url":"https://aeromorning.com/en/gkn-aerospace-and-u-s-air-force-advance-additive-manufacturing/","excerpt":null,"as_of":"2026-04-13","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"投資人撰寫的敘事（非公司揭露/非分析師研究）主張複合材料、陶瓷、奈米材料與積層製造長期可能侵蝕 ATI 合金與鈦產品需求。","source":"Simply Wall St community narrative: additive manufacturing and composite substitutes will disrupt future prospects","url":"https://simplywall.st/community/narratives/us/capital-goods/nyse-ati/ati/0ow7usxr-additive-manufacturing-and-composite-substitutes-will-disrupt-future-prospects","excerpt":"requiring costly and sustained R&D just to maintain relevance and pressuring both top-line revenue growth and margins over time","as_of":"2025-05-01","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08 Q2 後公司將 FY2026 調整後 EPS 指引由 $4.20–4.48 上調至 $4.90–5.18，高於 MarketBeat 所載事前共識 $4.44；Q3 EPS 指引 $1.31–1.37 對共識 $1.12。","source":"MarketBeat: ATI updates FY 2026 earnings guidance (2026-08-06)","url":"https://www.marketbeat.com/instant-alerts/ati-nyseati-updates-fy-2026-earnings-guidance-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261013","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 指引全面上調：調整後 EBITDA $1,135M–1,185M（前 $1,010M–1,060M）、調整後 FCF $550–600M（前 $465–525M）；Q2 營收 $1.26B（+11% YoY）、調整後 EPS $1.23 對共識 $1.03；backlog $4.4B（+18% YoY）；董事會另批 $500M 回購授權。","source":"ATI press release: ATI Exceeds the High End of Q2 Guidance and Raises Full-Year Outlook (Barchart)","url":"https://www.barchart.com/story/news/3688858/ati-announces-second-quarter-2026-results","excerpt":"Prior Guidance Full Year 2026 Adjusted EBITDA $1,010M - $1,060M","as_of":"2026-08-05","retrieved_at":"20261013","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布因來源而異：Benzinga 10 位分析師平均 $177（高 $270／低 $81，頁面日期 2026-09-04，疑似含過時目標）；Investing.com 9 位全 Buy、平均約 $200.33（高 $231／低 $175，2026-09 快照）；MarketBeat 2026-09 初報平均 $232。KeyBanc 2026-08-12 升至 $258、Susquehanna 2026-08-07 升至 $265。","source":"Benzinga price-targets page; Investing.com ATI consensus estimates","url":"https://www.investing.com/equities/allegheny-tech-consensus-estimates","excerpt":"Analyst Consensus— Overweight and Analyst Consensus — 10 Analysts with Consensus PT$177.","as_of":"2026-09-04","retrieved_at":"20261013","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"共識 EPS 上修趨勢：Q1（2026-04-30）調整後 EPS $1.00 對共識 $0.88；Yahoo 快照 2026 共識 4.14（90 天前 3.83）；Seeking Alpha（2026-03）過去三個月 7 次上修 0 次下修。Q2 後 MarketBeat 九月初稱分析師預期本年 EPS 5.11（不確定是否為真共識）。","source":"Nasdaq/Zacks: ATI Up 26.9% Since Last Earnings Report; MarketBeat","url":"https://www.nasdaq.com/articles/ati-ati-269-last-earnings-report-can-it-continue","excerpt":null,"as_of":"2026-09-05","retrieved_at":"20261013","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"ATI 與 State Street Global Advisors Trust Co. 在賓州西區聯邦法院面臨兩宗與 2023 年退休金義務轉移相關的集體訴訟（2:24-cv-01109、2:24-cv-01214），2024 年底合併、ATI 已提動議駁回；2026 年 Q2 10-Q 仍列為進行中。搜尋摘要未見結果。","source":"ATI Inc. Form 10-Q (period ended 2026-06-28)","url":"https://www.sec.gov/Archives/edgar/data/0001018963/000162828026054233/ati-20260628.htm","excerpt":null,"as_of":"2026-06-28","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"退休金義務轉移相關的兩宗集體訴訟（ERISA 性質參與人訴訟）在賓州西區進行中，被告含 ATI 與 State Street Global Advisors Trust Co.；2026 年 Q2 10-Q 仍列示。非證券詐欺案。","source":"ATI Inc. Form 10-Q (period ended 2026-06-28)","url":"https://www.sec.gov/Archives/edgar/data/0001018963/000162828026054233/ati-20260628.htm","excerpt":null,"as_of":"2026-06-28","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ATI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.36,"operating_margin_pct":15.19,"fcf_margin_pct":11.16,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ATI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HWM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.03,"operating_margin_pct":27.31,"fcf_margin_pct":19.64,"rd_intensity_pct":0.41},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HWM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"CRS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":30.58,"operating_margin_pct":22.47,"fcf_margin_pct":11.6,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRS","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CSTM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.3,"operating_margin_pct":8.5,"fcf_margin_pct":2.28,"rd_intensity_pct":0.55},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSTM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MTRN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.01,"operating_margin_pct":6.35,"fcf_margin_pct":1.55,"rd_intensity_pct":1.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MTRN","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"ATI"},"financial_history":{"ticker":"ATI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3836000000.0,"revenue_yoy_pct":null,"gross_margin_pct":18.62,"operating_margin_pct":10.86,"net_income":323500000.0,"diluted_eps":0.96,"free_cash_flow":94000000.0,"fcf_margin_pct":2.45,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":4173700000.0,"revenue_yoy_pct":8.8,"gross_margin_pct":19.23,"operating_margin_pct":11.37,"net_income":410800000.0,"diluted_eps":2.81,"free_cash_flow":-114800000.0,"fcf_margin_pct":-2.75,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":4362100000.0,"revenue_yoy_pct":4.51,"gross_margin_pct":20.59,"operating_margin_pct":12.74,"net_income":367800000.0,"diluted_eps":2.55,"free_cash_flow":168100000.0,"fcf_margin_pct":3.85,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":4587400000.0,"revenue_yoy_pct":5.16,"gross_margin_pct":21.95,"operating_margin_pct":13.99,"net_income":404300000.0,"diluted_eps":2.85,"free_cash_flow":333700000.0,"fcf_margin_pct":7.27,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ATI/ATI_Q2_2026_Earnings_Call_20260806.md）

# Q2 2026 Earnings Call
2026-08-06

Q2 2026 Earnings Call
ATI Inc. | Earnings Calls | 2026-08-06
Operator (Operator)
Thank you for joining us, and welcome to the ATI Second Quarter 2026 Results Conference Call.
[Operator Instructions] I will now hand the conference over to Rob Rengel, Vice President of Investor
Relations. Please go ahead.
Rob Rengel (Executives)
Good morning, and welcome to ATI's Second Quarter 2026 Earnings Call. I'm excited to step into this
role, and I want to begin by recognizing Dave Weston and the significant contributions he made to ATI
before his retirement. Today's discussion is being webcast at atimaterials.com. Joining me are Kim
Fields, Board Chair, President and CEO; and Rob Foster, Senior Vice President and CFO.
Before starting our prepared remarks, I would like to draw your attention to the supplemental
presentation that accompanies this call. Those slides provide additional color and details on our results,
capabilities and outlook and can also be found on our website. As a reminder, all forward-looking
statements are subject to various assumptions and caveats. These are noted in the earnings release and
in the accompanying presentation. After our prepared remarks, we'll open the line for questions.
Now I'll turn the call over to Kim.
Kimberly Fields (Executives)
Thanks, Rob, and welcome to the team, and good morning, everyone. Thank you for joining us. Turning
to Slide 3. ATI delivered another strong quarter, demonstrating the increasing earnings power of our
business. Second quarter adjusted EBITDA was $284 million, $29 million above the high end of our
prior guidance. Excluding a $10 million asset sale gain, underlying performance still exceeded the high
end of our guidance by $19 million. Adjusted EBITDA increased 37% year-over-year, making this ATI's
strongest quarterly EBITDA performance since 2007. Second quarter adjusted EBITDA margins
expanded 440 basis points year-over-year to 22.6%, reflecting stronger commercial terms, favorable
mix, disciplined execution and operational improvements through Elevation.
Revenue this quarter increased 11% year-over-year to $1.3 billion, an annualized run rate of more than
$5 billion. That expanding revenue was supported by another record backlog of $4.4 billion, up 18%
from a year ago and 7% sequentially. Importantly, that backlog increasingly reflects long-term
agreements, sole-source positions and strategic programs that provide meaningful multiyear visibility
into future shipments and earnings. Adjusted free cash flow in the quarter was $69 million, bringing
first half free cash flow to $143 million, an improvement of $193 million versus the first half of last
year. Cash generation will accelerate meaningfully in the second half, putting us on track to generate
positive free cash flow in every quarter of 2026. Our second quarter performance was led by our AA&S
segment, and it's one of the most important stories from the quarter.
Over the last several years, we've transformed AA&S. What was once viewed as a more cyclical, lower-
margin business has become a second durable earnings engine for ATI. We've improved the portfolio,
strengthened our commercial discipline and focused our investments where ATI's differentiated

capabilities create the greatest value. The result is a fundamentally different business. Excluding the
asset sale gain, AA&S generated an underlying EBITDA margin of approximately 22% compared with
14% a year ago. That's not simply the result of stronger markets. It's the result of better mix, better
pricing and better execution.
We built the transformation on 3 key priorities. First, we've optimized the portfolio, shifting AA&S
toward higher-value aerospace, defense and specialty energy applications, while at the same time,
exiting lower-value products. Today, aerospace and defense accounts for approximately 44% of AA&S
revenue, more than double their share 5 years ago. Second, we've leveraged ATI's unique technical
capabilities in high-purity hafnium and zirconium. ATI is 1 of 3 qualified producers in the Western
world capable of manufacturing these materials to the purity standards required for aerospace and
nuclear energy applications. With China limiting exports to these markets, our capabilities have
become even more valuable.
And third, we've translated that scarcity into stronger commercial performance. Improved pricing for
high-purity hafnium and zirconium benefits our defense and specialty energy businesses and also flows
through to our jet engine alloy materials, where hafnium and zirconium are critical alloy additions.
Combined with better product mix and disciplined commercial execution, that has materially increased
the earnings power of AA&S.
Now let me be equally clear about HPMC. Nothing about this quarter changes our long-term strategy.
HPMC remains ATI's largest long-term growth platform and the foundation of our aerospace strategy.
For HPMC, performance in the quarter was within our expectations, although qualification timing at
both our new facility in Mexico and our new titanium electron-beam furnace or EB2, shifted some
shipments into future periods. The important point is that our confidence in HPMC's growth trajectory
remains intact. Commercial terms and operational productivity are improving, and we're systemically
increasing the productive output of the manufacturing system through Elevation and targeted
investments. Those improvements support sequentially stronger performance through the second half
and position HPMC for additional growth into 2027.
Taken together, these results show a stronger, more balanced ATI. We are not benefiting from just one
favorable market or one strong quarter. We now have 2 businesses capable of generating durable
earnings growth supported by differentiated products, stronger commercial performance, operational
excellence and a record backlog that provides meaningful multiyear visibility into the future.
Turning to Slide 4. Based on our first half performance and improved visibility into the balance of the
year, today, we are meaningfully raising our full year outlook across every key financial metric. As a
result, our updated outlook now includes an adjusted EBITDA midpoint of $1.160 billion, representing
35% year-over-year growth, and adjusted EPS midpoint of $5.04, an increase of 56% year-over-year
and an adjusted free cash flow midpoint of $575 million, an increase of 51% year-over-year.
Importantly, these increases reflect a sustainable step change in AA&S performance and our ongoing
confidence in the HPMC ramp.
Turning to Slide 5. ATI's operating model is helping convert strong demand, improved commercial
terms and targeted investments into higher earnings, margins and cash flow. Elevation is the
foundation of that operating system. Let me give you some insight into how we operate. First, we
increase the productivity of the assets we own. Second, we make targeted investments where ATI has
differentiated technology, committed customer demand and the highest returns. And third, we embed

our operating system to make those improvements repeatable across the enterprise. That combination
is increasing ATI's earning power, strengthening cash generation and creating long-term shareholder
value.
Most importantly, we're seeing measurable results through Elevation. We've increased year-over-year
throughput by 30% in ultrasonic inspection, 15% in isothermal forgings and 15% in primary nickel melt.
Those aren't isolated improvements. When combined with our targeted capacity investments, we'll
realize higher productive output from our manufacturing network. Every major investment we're
making supports existing customer demand and expands ATI's differentiated capabilities.
Moving to Slide 6. Let me remind you about our capacity investments. Our new Chihuahua, Mexico
facility supports next-generation aerospace engine testing and inspection, and our EB2 furnace
expands premium quality titanium capability and capacity. Our nickel re-melt expansion remains on
schedule with our new VIM furnace coming online by the end of 2027. Together, these investments are
targeted to increase nickel capacity by approximately 15% to 20% by early 2028 compared with year-
end 2025. Across these combined nickel investments, we will deliver approximately $350 million of
incremental annual revenue by 2028. The important point is that these investments, combined with
Elevation, progressively increase the productive output of the manufacturing system.
Turning to Slide 7. Across all of our end markets, we're seeing the same underlying dynamics.
Customers have increasing need for qualified capacity, differentiated technology and certainty of
supply. Those are areas where ATI has built durable competitive advantages through proprietary
materials, unique manufacturing capabilities and decades-long customer qualifications. That
competitive position supports stronger commercial terms, long-term agreements and attractive growth
opportunities across our portfolio. Jet engines remains ATI's largest and most important growth
market. Revenue increased 13% year-over-year and 8% sequentially, reflecting ongoing strength across
both OEM production and aftermarket. The industry is transitioning toward next-generation engine
platforms, and ATI is exceptionally well positioned to benefit. Our content on these engines is more
than double that of legacy platforms, reflecting our differentiated materials in the hottest, most
demanding section of the engine.
Industry forecasts project next-generation engines will grow from about 35% today to over 50% of the
installed fleet by 2030. Currently, we support every major next-generation commercial engine platform
and produce 6 of the 7 most advanced nickel-based super alloys, including 5 where we are the sole
source supplier. That differentiation translates into stronger pricing, richer product mix and long-term
growth opportunities. Market conditions are developing largely as we anticipated. We continue to see
high teens jet engine revenue growth for the full year. In airframe, supply chain inventories have largely
normalized and customer order patterns are now aligning with announced OEM build rates. Our
planned production for the balance of the year is supported by firm customer orders. Landing gear
alloys remain our strongest airframe product category, while plate demand is improving. As a result, we
continue to see mid- to high single-digit full year airframe revenue growth weighted towards the second
half.
Defense delivered another outstanding quarter as one of our fastest-growing markets. Revenue
increased 36% year-over-year, reaching an all-time high as demand accelerated across naval nuclear,
missile and missile defense applications. Our recently announced naval nuclear renewal extends
through 2030 with improved pricing and product mix. It more than doubles annual revenue compared

to the prior contract. We're also seeing strength build across titanium, nickel and niobium products,
supporting strategic missile platforms, including Tomahawk, THAAD and PAC-3. We've already begun
receiving orders in support of the Tomahawk program.
As a result, we've increased our expectation for full year defense growth to the high teens, reflecting
growing momentum across the portfolio. Specialty Energy declined in the quarter as we prioritize
production toward defense orders with more immediate delivery requirements. That mix will rebalance
in the second half, supported by nuclear shipments and durable industrial gas turbine demand. We
continue to see mid-teens Specialty Energy revenue growth for the full year. In closing, we're building
the ATI of the next decade, a stronger company with durable demand, better execution, expanding
margins and greater cash generation.
With that, I'll turn the call over to Rob.
James Foster (Executives)
Thanks, Kim. I'll start with the second quarter performance, explain the different profiles of HPMC and
AA&S and close with the supporting details for our updated guidance. As shown on Slide 8, we
delivered strong overall results. Adjusted EBITDA and EPS exceeded the high end of our guidance,
while we expanded our consolidated margins and generated strong cash flow. These results
demonstrate the strength of ATI's differentiated portfolio and the earnings power of our business
model. Second quarter revenue was $1.3 billion, up 11% year-over-year, driven by 13% growth in
aerospace and defense. Within that market segment, jet engine sales increased by 13%, reflecting
increasing strength in high-temperature nickel alloys and favorable pricing.
Airframe revenue declined slightly, consistent with our expectations with growth accelerating in the
second half of the year. Defense-related revenue grew by 36% compared with the prior year, driven by
robust demand and meaningful price gains supported by new long-term contracts. Specialty Energy
revenue declined 6%, reflecting our decision to prioritize available production capacity toward higher-
value naval nuclear demand during the quarter. Second quarter adjusted EBITDA was $284 million, up
37% year-over-year. This was $34 million above the midpoint and $29 million or 11% above the high
end of our guidance. Excluding a $10 million asset sale gain in AA&S, underlying operating
performance still exceeded the high end of our guidance by nearly $20 million, reflecting stronger
pricing and mix.
Second quarter consolidated adjusted EBITDA margin was 22.6%, up 440 basis points year-over-year.
First half free cash flow improved significantly to $143 million compared with a use of $50 million in
the first half of 2025. Managed working capital as a percentage of sales at the end of Q2 was 34%. We
see further opportunities to improve inventory performance. For example, we are implementing a
customer consignment strategy for forging input material to improve working capital efficiency. Capital
expenditures were $69 million, including $23 million funded directly by customers. All key growth
projects remain on schedule and on budget.
Now on Slide 9, I'll review segment performance. HPMC sales increased 5% year-over-year to $637
million, primarily driven by growth in nickel products for jet engines. Segment margins expanded 40
basis points from the same period last year to 24.1%. Demand remains strong, while the timing of
customer qualifications related to our new facility in Mexico and the EB2 titanium furnace shifted
certain deliveries into future periods. These are timing effects and were partially offset in Q2 by higher

volume and pricing on rotating jet engine nickel alloys. We see the deferred demand converting in the
second half.
In AA&S, sales increased 17% year-over-year to $624 million. Growth reflected multiple drivers,
including pricing, mix and defense performance. Segment margin expanded 930 basis points to an all-
time high of 23.7%, reflecting stronger pricing, execution and a more favorable mix. As Kim mentioned,
AA&S is a fundamentally different business today. Through portfolio optimization, including 80/20, we
have shifted this segment toward higher-value applications. We've been building an integrated
interconnected business as our unique alloys are used across both HPMC and AA&S. Looking ahead, we
see AA&S EBITDA margins consistently above 20%. This improvement in AA&S means both segments
will now contribute to durable profitable growth.
We are raising our full year outlook across every key financial measure. Our confidence is supported by
contracted pricing, committed customer schedules, a higher structural earnings base in our AA&S
segment and HPMC shipments that moved from Q2 to the second half. In AA&S, our renewed nuclear
agreements, accelerated defense deliveries and shipments and improved hafnium and zirconium
pricing provides support for sustained performance through the balance of the year. In HPMC,
completed contract renewals are providing improved pricing and mix for jet engine materials. While
customer qualification timing affected the second quarter, the associated demand remains a strong
element in our second half production plan. Momentum will build in the third quarter carrying into the
fourth quarter and next year. Our improved outlook reflects not only supportive end markets, but a
stronger and more balanced ATI.
As shown on Slide #10, in the third quarter of 2026, we anticipate adjusted EBITDA of $305 million to
$315 million, translating to adjusted EPS of $1.31 to $1.37. At the midpoint, adjusted EBITDA would
increase 38% compared with the third quarter of 2025 and 9% sequentially. We anticipate sequential
profit improvement driven by AA&S pricing and mix strength, particularly in aerospace and defense.
HPMC performance will strengthen as deliveries build through the second half with momentum
starting in the third quarter and building into the fourth quarter. We see consolidated adjusted EBITDA
margins expanding in the third quarter compared to the second quarter of 2026.
Turning to Slide 11. Our higher full year outlook reflects the second quarter outperformance in AA&S
and a better second half baseline. The increase versus our prior outlook is primarily supported by
stronger AA&S pricing, mix and defense performance. Our full year HPMC outlook continues to reflect
sequential improvement in performance as we previously anticipated. Specifically, we have committed
contracts in place. This is not speculative. In addition, we will capture the second quarter timing effects
during the second half.
We are raising our full year adjusted EBITDA guidance to the range of $1.135 billion to $1.185 billion.
The midpoint of the range represents 35% increase over prior year. This outlook translates to full year
adjusted EPS range of $4.90 to $5.18. We see margin expansion in 2026 with full year consolidated
adjusted EBITDA margins now projected in the low 20% range. We now expect full year consolidated
incremental margins in the range of 50%. This is an improvement over the 40% we previously
communicated, driven by additional strength in our AA&S segment.
We anticipate second half performance to build sequentially. In the third quarter, the primary drivers
are continued pricing and mix strength in aerospace and defense for both segments. We see the fourth
quarter as our strongest quarter of 2026 for sales and profit. Our midpoint guidance implies

approximately $335 million of EBITDA in Q4. That translates to roughly $1.350 billion annualized exit
rate. While we are not providing 2027 guidance today, the commercial and operational drivers
supporting that performance extend into next year. At a segment level, we see full year EBITDA margin
for HPMC in the mid-20% range, consistent with our outlook from previous quarters. AA&S full year
EBITDA margin will be in the low 20% range, an improvement over the upper teens level we
communicated last quarter. The uplift is supported by stronger pricing and mix shifting towards
aerospace and defense, as we've discussed. Note that the performance of our segments is increasingly
driven by similar market dynamics.
Turning to adjusted free cash flow. We are raising the midpoint of our range by $80 million, setting the
range between $550 million and $600 million. The $575 million midpoint is $195 million higher than
the 2025 free cash flow, a 51% increase year-over-year. This implies adjusted free cash flow generation
of $430 million in the second half, driven by higher earnings, inventory conversion associated with
scheduled shipments and customer-funded capital. Our capital deployment strategy is unchanged. Our
gross CapEx range remains consistent with prior guidance at $280 million to $300 million.
This includes the greenfield expansion facility in Mexico, which Kim mentioned. Customer-funded
CapEx of $55 million to $65 million will be a partial offset. Share repurchases remains a priority for
deploying incremental free cash flow. We view them as the most efficient way to return capital to
shareholders. As of today, after our $50 million repurchase in Q2, we have $495 million remaining
under our current repurchase authorization. Overall, we delivered a strong first half and expect even
better second half. Our increased outlook is supported by contracted pricing, a record backlog,
committed customer schedules and planned shipment timing.
Kim, back to you.
Kimberly Fields (Executives)
Thanks, Rob. As we look ahead, our priorities remain clear: continue improving execution through
Elevation, bring differentiated capacity online and allocate capital where returns are highest. We are
confident in our ability to convert strong demand into sustained growth, higher earnings and cash flow.
Now let's open the line for questions.
Operator (Operator)
[Operator Instructions] Your first question comes from the line of Richard Safran from Seaport
Research Partners.
Richard Safran (Analysts)
I have one question and one quick follow-up. On the guidance raise, if I did the math right, you did -- at
the midpoint, you took EBITDA up by $125 million, but you took up your free cash flow guide by $80
million. So I just wanted to know if you could go over what drove that and how we should be thinking
about cash and cash conversion going forward?
Kimberly Fields (Executives)
Thanks, Rich. It's -- I appreciate the question. So yes, I'll start -- I'll share a little bit on the guide, and
then I'll hand it over to Rob. He can talk a little bit about the free cash flow and the outlook. I'll say our
guide and our raise is really based on the strong performance we've had this quarter, and it's based on

things that are already in place. So this is the contracted pricing improvements that we're seeing flow
through, recently committed long-term agreements and customer orders that are already committed.
And so we have high confidence that this is based on all those things I just mentioned, committed
orders and a stronger business and the structural improvement that I shared in the prepared remarks
around AA&S. You add in there some of the timing changes for HPMC, and that's what drives our
confidence as far as our outlook. And to your point around cash flow, typically, we start the first half off
-- we started from $143 million this year. It typically accelerates as we go through the year, and we
anticipate that continuing as we go forward. But Rob, do you want to add any more color on that?
James Foster (Executives)
Yes, Rich, when I think about the cash flow, if you think about the increase in the EBITDA really, we're
talking about higher shipments in the second half. And essentially, the reason why that's not all going
to convert is really 2 things. One, it's the timing of conversion through accounts receivable. So we'll
expect some of that higher volume with those late Q4 shipments to be in receivables. And the second
piece is we do plan on a little bit more inventory as we prepare for the early part of 2027.
So I think it's important to call out that when you look at our full year cash flow and the guide of the
midpoint of $575 million, that represents an increase of over 51% from the full year 2025. And when I
think about the free cash flow conversion, that assumes a high 80%, and as we've stated several times,
our goal is to drive well over 90% free cash flow conversion. So I think we're trending in the right
direction. And as I think about going forward into 2027, I'm not going to give updated guidance here
today on 2027, but the free cash flow conversion at 90% or greater is where we're thinking about the
target.
Richard Safran (Analysts)
Okay. And then just a quick follow-up on AA&S and at the risk of pressing you on something. So given
your remarks about transforming the business, your comments about 20% EBITDA margins, would
you be willing to talk a bit more about the EBITDA margin potential at AA&S, how we should be
thinking about it if growth and mix continues to improve? Would you be willing to give out a bit more
specific on that?
Kimberly Fields (Executives)
Sure. Yes, from -- as you said, fantastic performance in the quarter by AA&S in the segment, and it's a
transformation that we've been working on for several years. You've heard me talking about it. As we
look out, we anticipate we can see AA&S in the mid-20% range going forward. And really because this is
based on structural changes that we've been making in this segment for, as I said, the last few years.
One, it started with the transformation in our Flat Rolled business, exiting the standard stainless and
focusing our resources on that highest value products through 80/20. And here most recently, we've
strengthened our commercial model and restructured long-term agreements, improved pricing and
mix.
And now we're benefiting from the acceleration around defense and nuclear demand as we look
forward. I mentioned in my prepared remarks that A&D is more than double where we were 5 years ago
at 44%. And maybe even more impressive, if I look year-over-year at the AA&S segment, A&D is up
34% year-over-year. And so as you said, really focused on structural change, both from a market mix,

pricing and contractual agreements. I think the last thing just to mention here that we're also benefiting
from is that our business, SA&C on the West Coast is 1 of 3 qualified Western producers of high-purity
hafnium and zirconium.
And that provides another durable competitive advantage, especially given, as I mentioned in my
remarks, supply chain continue to tighten and trade continues to change and create more demand,
which allows us to capture that value. So as we think about it and look at AA&S today, we're talking
about a business that's fundamentally different from an earnings profile than it was a year ago. And
that gives me the confidence to say that we're going to be in that mid-20% range going forward.
Operator (Operator)
Your next question comes from the line of Seth Seifman from JPMorgan.
Seth Seifman (Analysts)
I wanted to ask about the outlook in HPMC in the second half. You talked about catching up on some of
the revenue. And to the extent that you also see margin expansion, I think the first half margin is kind
of in the range -- mid-20s type of range that you've talked about, but had also been thinking about some
LTA rollovers and mix improvement driving second half margin expansion there and if that's still part
of the outlook?
Kimberly Fields (Executives)
Yes. Seth, so as I think about it and we look at HPMC, we've been talking about through this year, we
had a step-up coming in the back half of the year, so here in third quarter. And it is based on a couple of
things. Some I talked about. One is the work we're doing through Elevation and the improvements
around productivity and taking cost out of our operation. But more importantly, as you mentioned,
we've got contractual renewals that are kicking in and step up in pricing, and we are still expecting to
see that. In addition, as you said, we had some timing changes with our 2 new facilities that we are in
qualifications, one in Mexico and then the EB premium quality titanium. So those are also moving out.
As I look at the quarter, we had probably around $30 million to $40 million of revenue that moved
from the first half into the second half, where the margins were maybe 40% to 50% shifting into the
future periods. And that will accelerate as those facilities continue to ramp and come online. But we do
continue to see sequential improvements through the balance of the year based on those new contract
pricing. And these are the same drivers that underpin our confidence in that stronger half outlook and
the improvement in our HPMC outlook as well.
Seth Seifman (Analysts)
And just one clarification, that 40% to 50%, that's kind of an incremental margin cadence that we're
discussing there.
James Foster (Executives)
Yes.
Operator (Operator)
Your next question comes from the line of David Strauss from Wells.

David Strauss (Analysts)
Rob, you touched on kind of the implied Q4 EBITDA as an exit rate into next year. I guess, is there
anything unusual in that number? Is there anything -- any reason as to why we wouldn't kind of -- or
you guys wouldn't kind of grow off of that level as we head into '27? And kind of within that, are you
thinking as we look at '27 is 50% incrementals for the overall business with what you're talking about
for AA&S now? Is that a sustainable kind of run rate to use for incrementals from here?
James Foster (Executives)
Yes. Thanks, David. Well, when I look at Q4 and you think about what that implies for the exit rate for
the full year, it implies $1.350 billion of EBITDA. And while I'm not going to give 2027 guidance today,
I think I can say that it kind of directionally makes sense. And when you look at those incrementals, we
have increased our incrementals from 40% to 50%. So I think it's fair to think about this business from
all the structural changes that we've made to be a business that can deliver margins in that 40% to 50%
incremental range. But again, we're not going to put a fine point on the 2027 today, but we do expect to
give some additional guidance here coming forward.
David Strauss (Analysts)
Okay. And a quick follow-up. Kim, you talked about kind of mid-20s EBITDA margin for AA&S. What
are you assuming kind of on a go-forward basis, the mix of A&D is within total AA&S sales? I think
you're at 44% now. What do you assume going forward?
Kimberly Fields (Executives)
Yes. So as I look forward, we're assuming that mix of A&D continues to stay at that level and it will
continue to rise as we renegotiate contracts. I do believe that the tightness in the hafnium and
zirconium markets that go into both defense and specialty energy are going to continue to become tight,
especially given some of the trade restrictions we're seeing out of China. So I could see that percentage
continue to increase as we look across the segment, and that will help support that mid-20s percent
from a structural standpoint.
Operator (Operator)
Your next question comes from the line of Myles Walton from Wolfe.
Myles Walton (Analysts)
Could you touch on the still high -- mid- to high single-digit outlook for airframe that you talked about?
Obviously, the first half of the year down and implying you need to get to something closer to mid-teens
to get to the back half of the year. Is that predicated on the facilities coming online or any risk to that?
Kimberly Fields (Executives)
I think you were asking about airframe and our guide and outlook there. From our perspective, as I
look at the airframe market, the inventories have largely normalized now, and that's consistent with
what we've been expecting and what we've been seeing in our customer order patterns. And so as we
look into the second half, as we shared in the last quarter, we anticipate acceleration as we go through
this year, and that does seem to be what is lining up. It's important to remember, our orders don't
directly align one-for-one with that aircraft build rate, but we're encouraged to hear about the step rate

changes in build rates and both airframers are doing well. Our material is getting ordered well ahead of
that assembly.
And so that confidence for that mid- to high single-digit range is really based on a couple of things. One
is our fully committed order book is in place, and we've got order books now extending into 2027. We
are seeing, from both airframers, emergent demand in addition to that starting to come in as we go into
the fourth quarter here. And we're seeing some pull around widebody as they're starting to prepare for
those programs as well. So from where I sit, the inventory normalization is largely behind us. The
business is increasing as we expected and we shared with you early in the year, and the underlying
production demand is now aligned with their order rates.
Operator (Operator)
Your next question comes from the line of Scott Deuschle from Deutsche Bank.
Scott Deuschle (Analysts)
Kim, can you share an update on the lead times you're now seeing across the different product lines the
business has? And then also share what drove the sequential backlog growth in the quarter?
Kimberly Fields (Executives)
Sure, sure. So as we think about lead times, I think it's best to look at both backlog and lead time
together because they tell the same story and they work together. On the backlog side, I shared in the
remarks, we finished the quarter at another record $4.4 billion. That's up 18% year-over-year and 7%
sequentially. About 70% of that backlog we expect to convert into revenue over the next 12 months. So
we have good visibility into the business.
As you look at lead times, and that's where we see those lead times starting to extend for our most
differentiated proprietary products. Right now, we're at about 12 months on nickel alloys. We've moved
out to 20 months on the premium quality titanium as that tightness continues to expand. And we've
been running above 24 months on isothermal forgings here for a little while. So taking together, those
are both a really good indicator that demand continues to exceed the available capacity to support these
programs and these differentiated materials.
Operator (Operator)
Your next question comes from the line of Andre Madrid from U.S. Bancorp.
Andre Madrid (Analysts)
I wanted to see if you could break down the margin impact specifically in the quarter related to the
recently signed naval nuclear agreement.
Kimberly Fields (Executives)
Yes. I'll let Rob take that one and share a little bit more color on it.
James Foster (Executives)
Yes. So the naval nuclear contract is essentially a contract and a relationship that we've had for many
decades. And essentially, the new contract that just recently began here effective in the second quarter
is essentially a $1 billion revenue contract over 5 years. And that is essentially kind of double what the

previous 5-year contract was. And so a majority of that increase is price mix with some smaller, I'll call
it, 2/3 price mix, 1/3 volume in that contract. And essentially, we saw some of that volume and price
recognized in our AA&S segment financials a bit earlier than we were anticipating. So while it wasn't a
full quarter of shipments under the new contract, it was a majority of the second quarter was shipping
under that new contract. So those are some of the dimensions.
Rob Rengel (Executives)
Operator, we're ready for our final question.
Operator (Operator)
Your last question comes from the line of Seth Seifman from JPMorgan.
Seth Seifman (Analysts)
I like the slide that you added with the various capacity additions and kind of how they come online. It
feels like as we progress through the quarters, we hear more about incremental demand, whether that's
in the defense area. We got the missile frameworks this year and now people talking about lots of low-
cost cruise missiles and CCAs. IGT market remains pretty hot. How are you thinking about -- or how
are you evaluating -- I assume there are demands for incremental capacity increases beyond what you
have on Slide 6. How are you kind of approaching those decisions now?
Kimberly Fields (Executives)
Yes, that list -- as you said, there's demand coming from all of our core markets, and it just continues to
ramp, as you mentioned, missiles is another great one. That revenue is up 4x in the quarter. And so yes,
we're seeing continued demand. One of the things that we shared was more details around Elevation,
our operating system. And so the way we approach this is Elevation is really about making sure that we
get as much out of the assets that we already own before we invest in new capacity. And so that is a
continuous improvement activity that the teams continue to work on at improving throughput,
increasing yields, shortening those cycle times to create that additional capacity and expand margin
and generate cash.
So once we've captured those and as we start to look out -- and again, our long-term contracts I've
shared this in the past, provide a lot of visibility and sharing with our customers, especially around
those hot section alloys, where we are producing 6 of 7 and 5 of them, we're the sole source supplier.
We have a lot of discussions around that long-term demand and outlook. And we take that then into
account as we start to prioritize where do we make investments, where -- what is the timing. And of
course, all of these projects have to meet our 30% return thresholds internally. You mentioned our
newest facility in Mexico. That is really an important part of our downstream growth strategy.
So we've talked a lot about the upstream with melt capacities in titanium and in nickel. But
downstream, we've talked about from a bottleneck standpoint, is where the industry continues to have
tightness as increasing requirements around quality and testing come into play. And so that facility is
going to be a key part of strengthening our ability to support the increased production rates, enhance
our position in those programs for the next-generation engine. So there is, as you said, a lot of demand
coming in. We are aligning and using Elevation to help us maximize the asset portfolio we have today
and then working closely with our customers to align on their future demands on those investments.

A great example just to end with is the customer funding that we continue to receive as they support not
just the new asset investments, but also those qualifications, which can be very, very long and very
involved to get to that qualified product. So a lot of great new assets coming online this quarter and in
the back half of the year. We see continued growth and confidence in the outlook, not just for 2026, but
as we go into '27 and beyond. So you'll continue to hear from us as we share those results and the great
work from the team.
Operator (Operator)
We have reached the end of the Q&A session. I will now turn the call back to Kim Fields for closing
remarks.
Kimberly Fields (Executives)
Thank you, operator, and thank you, everyone, for joining today. ATI is significantly transformed from
a company that it was 5 years ago. We're more differentiated, more concentrated in attractive markets
and capable of stronger margins and cash generation. We are building the ATI of the next decade, and
we are only beginning to capture that opportunity in the results you saw in Q2. We look forward to
sharing more at our Investor Day later this year. Thank you for joining us, and have a great day.
Operator (Operator)
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ATI_Q1_2026_Earnings_Call_20260430.md
- 2026-04-30｜CEO Kim Fields｜guidance：全年調整後 EBITDA 財測上調至 10.1–10.6 億美元（原話："adjusted EBITDA of $1.01 billion to $1.06 billion"）
- 2026-04-30｜CFO Rob Foster｜guidance：Q2 調整後 EBITDA 財測 2.45–2.55 億美元（原話："adjusted EBITDA of $245 million to $255 million"）
- 2026-04-30｜CFO Rob Foster｜guidance：全年自由現金流區間中點上調 3,500 萬美元（原話："We are raising the midpoint of our range by $35 million"）
- 2026-04-30｜CFO Rob Foster｜guidance：全年資本支出區間維持不變（原話："Our CapEx range remains consistent with our prior guidance."）
- 2026-04-30｜CFO Rob Foster｜guidance：CFO 對 2027 既有財測區間的信心與偏向，並預告 Q4 時段更新（原話："I have a bias towards the upper end of that 2027 guide"）
- 2026-04-30｜CFO Rob Foster｜guidance：國防成長指引為低至中十位數，CFO 偏向區間上緣（原話："my bias is towards the upper end of that guide"）
- 2026-04-30｜CEO Kim Fields｜guidance：特殊能源全年成長指引為中十位數，且接單與出貨呈塊狀（原話："lumpy as the orders come in, in an intermittent"）
- 2026-04-30｜CFO Rob Foster｜guidance：工業、醫療、電子市場全年預期下滑（原話："Sales for our industrial, medical and electronics"）
- 2026-04-30｜CEO Kim Fields｜guidance：機身（airframe）上半年持平、下半年加速，更大增幅在 2027（原話："is going to be flattish as that inventory"）
- 2026-04-30｜CFO Rob Foster｜margin：全年合併 EBITDA 利潤率指引 20% 以上（原話："year consolidated margins in the range of 20% plus"）
- 2026-04-30｜CFO Rob Foster｜margin：Q2 利潤率與 Q1 相近，下半年擴大至 20% 以上（原話："Q2 margins are tracking to be similar"）
- 2026-04-30｜CFO Rob Foster｜margin：全年合併增量利潤率平均 40%，下半年高於上半年（原話："Full year consolidated incremental margins will average 40%"）
- 2026-04-30｜CFO Rob Foster｜margin：分部全年利潤率口徑：HPMC 中 20%、AA&S 高 10%（原話："full year margins for HPMC will be in the range of mid-20s"）
- 2026-04-30｜CFO Rob Foster｜margin：Q1 利潤率優於預期的歸因為 80/20 與投資組合精簡帶來的較佳組合（原話："we realized a richer mix from 80/20 initiatives"）
- 2026-04-30｜CFO Rob Foster｜margin：管理層稱 2026 增量利潤率 40% 高於歷史指引區間（原話："pretty confident in that 40% year-over-year incremental"）
- 2026-04-30｜CEO Kim Fields｜margin：管理層預期加速效果更多體現在利潤與 EBITDA 而非營收（原話："our margin and EBITDA line more so than the revenue line"）
- 2026-04-30｜CEO Kim Fields｜product：訂單積壓季增 10% 創新高（原話："order backlog growing by 10% sequentially to an all-time"）
- 2026-04-30｜CEO Kim Fields｜product：飛彈相關營收年增超過一倍（原話："revenue in missiles and missile systems more than doubled"）
- 2026-04-30｜CEO Kim Fields｜product：ATI 供應七種最先進噴射引擎鎳合金中的六種（原話："We supply 6 of the 7"）
- 2026-04-30｜CEO Kim Fields｜product：預期明年鈦的銷售成長更強（原話："titanium sales growth in '27"）
- 2026-04-30｜CEO Kim Fields｜customer：與 Cameco 新簽五年協議，金額 2.5 億美元（原話："This $250 million agreement includes meaningful improvements"）
- 2026-04-30｜CFO Rob Foster｜customer：Cameco 合約 Q1 貢獻有限，屬未來效益（原話："There wasn't much benefit accrued into the Q1."）
- 2026-04-30｜CEO Kim Fields｜customer：海軍核動力計畫五年續約，預計營收 10 億美元（原話："This agreement is projected to generate $1 billion in"）
- 2026-04-30｜CEO Kim Fields｜customer：管理層稱 Middle East 衝突目前對需求與訂單無實質影響（原話："We've seen no material impact on demand or order activity."）
- 2026-04-30｜CEO Kim Fields｜competition：管理層稱定價屬長期合約內建，非僅短期稀缺（原話："but it's long term and contractual"）
- 2026-04-30｜CEO Kim Fields｜competition：管理層對 OE 與 MRO 不作價格區分，回應 OE 放量期價格不降反升的提問（原話："we don't really see a differentiation between OE versus"）
- 2026-04-30｜CEO Kim Fields｜competition：新世代引擎的 ATI 含量約為舊引擎的兩倍（原話："We've got twice the content, as I've shared"）
- 2026-04-30｜CFO Rob Foster｜capital_allocation：Q1 回購 7,500 萬美元股票（原話："we repurchased $75 million in shares"）
- 2026-04-30｜CFO Rob Foster｜capital_allocation：Q1 增加 5 億美元回購授權（原話："We increased our share authorization by $500 million in Q1"）
- 2026-04-30｜CEO Kim Fields｜capital_allocation：目前不宣布新的重大產能專案（原話："announce any new significant projects today"）
- 2026-04-30｜CEO Kim Fields｜capital_allocation：產能調配：降低工業、醫療、電子比重，轉往高利潤市場（原話："we are deemphasizing those and moving the capacity"）
- 2026-04-30｜CEO Kim Fields｜risk：噴射引擎仍為最高利潤業務，但差距快速縮小（原話："although that's been rapidly shrinking"）
- 2026-04-30｜CFO Rob Foster｜risk：Q1 機身營收年減 9%（原話："airframe revenue declined by 9%"）
- 2026-04-30｜CEO Kim Fields｜risk：關稅全數透過合約轉嫁，退稅政策進展不大（原話："there has not been a lot of progress in that regard"）
- 2026-04-30｜CEO Kim Fields｜risk：通膨成本透過合約轉嫁（原話："we do pass through all of those"）
- 2026-04-30｜CFO Rob Foster｜commitment：CFO 承諾 2026 年每季自由現金流為正（原話："generate positive cash flow in every quarter of 2026"）
- 2026-04-30｜CEO Kim Fields｜commitment：管理層稱 50 億美元營收、20% 以上利潤率在望（原話："$5 billion of revenue at 20%-plus margins is in clear sight"）
- 2026-04-30｜CEO Kim Fields｜commitment：管理層稱 A&D 占比將持續提高並高於 70%（原話："A&D mix is going to continue to go higher"）
- 2026-04-30｜CEO Kim Fields｜commitment：明年初鎳產能約增 5% 產量釋出（原話："where we really unleash, call it, 5% or so more volumes"）

### ATI_Shareholder_Analyst_Call_ATI_Inc_20260514.md
- 2026-05-14｜Robert S. Wetherbee｜risk：執行董事長 Wetherbee 表示這是他擔任董事長的最後一次正式行動（領導層交接）。（原話："This is my last official act as the Executive Chairman"）
- 2026-05-14｜Robert S. Wetherbee｜risk：Kim Fields 自即日起兼任董事會主席，並仍為總裁暨 CEO。（原話："Fields as President, CEO, and, as of now, Board Chair."）
- 2026-05-14｜Robert S. Wetherbee｜competition：Wetherbee 稱團隊已轉型並成為有差異化的市場領導者（無數字佐證）。（原話："differentiated itself as a market leader."）
- 2026-05-14｜Robert S. Wetherbee｜product：Wetherbee 以航空應用說明 ATI 產品的重要性（無細節）。（原話："And you can't fly without ATI either."）

### ATI_Morgan_Stanley_s_14th_Annual_Laguna_Conference_20260917.md
- 2026-09-17｜Kimberly Fields｜margin：CEO 引述第二季 AA&S 與全公司利潤率（AA&S 一年前為 14%）（原話："about 22% margin in AA&S segment, 23% across the business"）
- 2026-09-17｜Kimberly Fields｜margin：CEO 表示目前增量利潤率約 50%，並預期全年持續（原話："we're at 50% incrementals today, and that's phenomenal"）
- 2026-09-17｜Kimberly Fields｜guidance：CEO 提到進入 2027 的隱含 EBITDA run rate 為 13.5 億美元（原話："run rate of going into 2027 at $1.35 billion of EBITDA"）
- 2026-09-17｜Kimberly Fields｜guidance：2027 年將有今年價格與合約重設的全年效應（原話："a full year of these price and contractual resets"）
- 2026-09-17｜Kimberly Fields｜guidance：今年 CapEx 區間 2.8–3.0 億美元，約 20% 為客戶出資（原話："between $280 million to $300 million"）
- 2026-09-17｜Kimberly Fields｜commitment：CEO 說 11 月將舉辦投資人日，屆時分享前瞻細節（原話："we've got an Investor Day that's going to be in November"）
- 2026-09-17｜Kimberly Fields｜commitment：內部資本專案報酬率門檻為 30% IRR（未計客戶出資前）（原話："So that's a 30% IRR target."）
- 2026-09-17｜Kimberly Fields｜commitment：合約續約／重設預定在年底前進行（原話："resetting and renewing these contracts"）
- 2026-09-17｜Kimberly Fields｜capital_allocation：鎳超合金重熔設備已進入試車，初熔設備明年底試車（原話："we are in commissioning for the remelt assets today"）
- 2026-09-17｜Kimberly Fields｜capital_allocation：擴產順序：先以 Elevation 擠出現有資產產能，再與客戶談新產能（原話："First thing we do is we start with Elevation."）
- 2026-09-17｜Kimberly Fields｜customer：客戶出資換取工程資源優先排序，加速新資產認證（原話："the scarce resource they have is their engineering talent"）
- 2026-09-17｜Kimberly Fields｜customer：客戶為搶產能願意接受漲價；噴射引擎與其他市場的獲利差距在縮小（原話："narrowing of the gap between jet engine and our"）
- 2026-09-17｜Kimberly Fields｜customer：客戶分散供應商而要求 ATI 認證，仍見市占與 mix 改善（原話："still seeing share gains, mix improvements"）
- 2026-09-17｜Kimberly Fields｜customer：國防上季成長 36%，飛彈成長 4 倍，Tomahawk 與 THAAD 開始下單（原話："Defense, defense has been a bright spot."）
- 2026-09-17｜Kimberly Fields｜customer：噴射引擎業務目前 50% 為 MRO（原話："jet engine being 50% MRO today for us"）
- 2026-09-17｜Kimberly Fields｜competition：熱區 7 種專有合金中 ATI 獨家供應 5 種（原話："We make 5 of them sole-source providers"）
- 2026-09-17｜Kimberly Fields｜competition：ATI 是全球兩家具等溫鍛造能力之一（原話："We're 1 of 2 globally that have that capability."）
- 2026-09-17｜Kimberly Fields｜competition：鉿鋯為三家西方合格供應商之一，且是唯一無自有商用核能業務者（原話："We're the only independent."）
- 2026-09-17｜Kimberly Fields｜competition：對 GE 收購 CPP 的看法：ATI 不做鑄件、不供貨 CPP，影響很小（原話："we don't really supply to CPP at all"）
- 2026-09-17｜Kimberly Fields｜product：Richland 新鈦資產正在認證（原話："qualifying our new asset that we just brought online"）
- 2026-09-17｜Kimberly Fields｜product：太空應用目前占比仍小，管理層預期大幅成長（原話："Small today, still a very small part."）
- 2026-09-17｜Kimberly Fields｜risk：中國貿易限制（含鉿鋯）被管理層視為價格與 mix 的背景因素（原話："trade restrictions with China"）
- 2026-09-17｜Kimberly Fields｜product：管理層稱現有 HPMC 與 AA&S 兩個利潤結構相近的成長引擎（原話："Now we have 2 that are very similar in margin profiles"）

### 問答異常語氣（迴避／改口／保留）
- ATI_Q1_2026_Earnings_Call_20260430.md｜問：Strauss：EBITDA 財測上調的來源為何（分部利潤率指引幾乎未變）｜答法：CFO 回答對財測有信心，稱終端市場成長指引未改、偏向國防與噴射引擎區間上緣，未量化 3,500 萬美元上調的拆解
- ATI_Q1_2026_Earnings_Call_20260430.md｜問：Safran：規劃中的產能擴充與上線時程｜答法：僅重述既有鈦與鎳投資按期，表示未到可宣布新重大專案的階段，不給新增產能數字
- ATI_Q1_2026_Earnings_Call_20260430.md｜問：Khanna：2027 年增量利潤率框架｜答法：CFO 不談 2027 細節，僅表示偏向既有 2027 指引區間上緣，更新留待 Q4
- ATI_Q1_2026_Earnings_Call_20260430.md｜問：Walton：向 CFO 詢問 2026 關稅展望為正或負｜答法：由 CEO 接話答「status quo」與全數轉嫁，未給正負或金額

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
{"date":"20260518","verdict":"B（衛星候選·thesis 完整 Q1 26 Adj EPS $1.00 +39% Beat / HPMC margin 24.9% +250bp / AA&S 18.1% +320bp / FY26 guide raised Adj EBITDA $1.010-1.060B + Adj EPS $4.20-4.48 / Bakers South VIM 2H 2027 +8-10% / $1.20B buyback expanded；但 HPMC margin vs CRS SAO 35.6% 差距 11pp 反映議價權較弱 + AA&S 非純航太業務拖累；估值🟡 Fwd PE 28.4x（FY27, 5Y 分位 64%）+ PEG 1.29 合理 + Pure MA ✅ 強勢進場 W250 +14.2%；R:R 短期負追高風險；等回測 BB 中軌 $146 再加碼）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"HPMC adj segment margin 達 normalised 25%+ baseline（從 FY22 ~8% 升至 FY26 Q1 24.9%）","columns":{"2Y 驗證點":"FY27-28 HPMC margin TTM 維持 23-27%","5Y 驗證點":"FY30 HPMC margin ≥ 22%（Bakers South 上線後產能稀釋 ~2-3pp）","10Y 驗證點":"FY35 normalised HPMC margin ≥ 18%","具體數字門檻":"2Y: 連 4 季 TTM ≥ 23%；5Y: 滾動 8 季均 ≥ 22%","信息來源":"Q1 FY26 法說 + Bernstein 2025 投資人簡報 + mgmt guidance","漂移觸發條件":"連 4 季 TTM"}},{"id":"H2","text":"Bakers South VIM 2H 2027 commission on schedule + 80% LTA 鎖定不變","columns":{"2Y 驗證點":"2026 Q2-Q4 commission ETA 維持 2H 2027 + LTA 比例 ≥ 75%","5Y 驗證點":"FY28-30 Bakers South ramp 達 management guided rate（+8-10% capacity = +$300-400M Rev）","10Y 驗證點":"2030+ 新容量在下次 cycle 仍 ≥ 70% utilization","具體數字門檻":"2Y: 季度 capex 維持 $70-90M/qtr (FY26 high $300s annual)；5Y: incremental Rev ≥ $300M","信息來源":"2026-04 metalnomist 確認 +9,000 tonnes/yr + 2H 2027 + 80% LTA secured","漂移觸發條件":"commission 延後 > 6 個月 或 LTA 比例"}},{"id":"H3","text":"AA&S margin 維持 ≥ 15%（從 FY22 ~5% 升至 FY26 Q1 18.1%）— 不會在 cycle 反轉時急轉直下","columns":{"2Y 驗證點":"FY27-28 AA&S margin TTM 維持 15-18%","5Y 驗證點":"FY30 AA&S margin ≥ 13%（即使工業景氣放緩）","10Y 驗證點":"FY35 AA&S 或被分拆 / 維持 ≥ 10%","具體數字門檻":"2Y: 連 2 季 TTM","信息來源":"Q1 FY26 法說 + 10-K 細分","漂移觸發條件":"連 2 季 TTM"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Pratt & Whitney GTF 供應問題持續影響 Airbus（2026/02/05 仍無 2026-27 供應協議）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Airbus monthly A320neo delivery + Pratt GTF resolution timeline","警戒閾值":"連 2 季 Airbus monthly delivery"}},{"id":"R2","text":"HPMC margin reversion + AA&S margin 雙重壓縮","columns":{"對應假設":"H1 + H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"HPMC 季度 adj margin + AA&S 季度 adj margin（TTM 化避免季節 noise）","警戒閾值":"HPMC 連 4 季"}},{"id":"R3","text":"下一輪航太 cycle 反轉（FY29-32 期間 EPS 可能下修 40-60%）","columns":{"對應假設":"H1 + H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"Boeing/Airbus order intake + IATA RPK growth + 全球商用機 backlog","警戒閾值":"需 ≥ 50% 機率才砍倉；backlog 從 14 年降至"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":153.55,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261013/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
