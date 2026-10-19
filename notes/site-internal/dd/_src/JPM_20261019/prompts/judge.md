你是 stock-analyst **v20 判斷 agent**，標的 JPM（20261019）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"JPM","date":"2026-10-19","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JPM_20261019/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JPM_20261019/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenue_reported","label":"Net revenue (reported)","value":50172,"period":"Q3 2026（公告於 2026-10-13）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"JPM 3Q26 Earnings Press Release（8-K Ex.99.1）"},"note":"共識約 $51.23B，低於預期（來源：web_search 二手報導，未經 IR 驗證）"},{"id":"f_kpi1_net_income_reported","label":"Net income (reported)","value":15305,"period":"Q3 2026（公告於 2026-10-13）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"JPM 3Q26 Earnings Press Release"}},{"id":"f_kpi2_diluted_eps","label":"Diluted EPS","value":5.57,"period":"Q3 2026（公告於 2026-10-13）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"JPM 3Q26 Earnings Press Release"},"note":"排除 $658M 證券損失後 EPS $5.75，對共識 $5.92 差約 2.9%（二手報導，共識數字各源 $5.90–5.93 不一）"},{"id":"f_kpi3_noninterest_expense","label":"Noninterest expense","value":27295,"period":"Q3 2026（公告於 2026-10-13）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"JPM 3Q26 Earnings Press Release"}},{"id":"f_kpi4_pre_provision_profit","label":"Pre-provision profit（營收減費用，自算）","value":22877,"period":"Q3 2026（公告於 2026-10-13）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"自算：50,172 − 27,295，依 JPM 3Q26 press release"}},{"id":"f_kpi5_provision_for_credit_los","label":"Provision for credit losses","value":2743,"period":"Q3 2026（公告於 2026-10-13）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"JPM 3Q26 Earnings Press Release"}},{"id":"f_kpi6_rotce","label":"ROTCE","value":20,"period":"Q3 2026（公告於 2026-10-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"JPM 3Q26 Earnings Press Release"}},{"id":"f_kpi7_cet1_ratio_standardized","label":"CET1 ratio (Standardized)","value":13.9,"period":"Q3 2026（公告於 2026-10-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"JPM 3Q26 Earnings Press Release"}},{"id":"f_kpi8_significant_item_corpora","label":"Significant item：Corporate 淨投資證券損失","value":658,"period":"Q3 2026（公告於 2026-10-13）","unit":"USD m（稅後 498）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（公告於 2026-10-13）","citation":"JPM 3Q26 Earnings Press Release"}},{"id":"f_kpi9_guidance_fy2026_nii_nii_","label":"Guidance：FY2026 NII／NII ex-Markets／調整後費用","value":"NII 約 $106.2B（原 $105.5B）；ex-Markets 約 $97.2B（原 $96.5B）；調整後費用約 $108.6B（原 $107.5B）","period":"Q3 2026 法說（2026-10-13）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026 法說（2026-10-13）","citation":"二手報導 money365.market 等，未對照 IR 逐字稿，使用前須查證"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-13","period":"2026-10-13","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-13"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_jpm_fcf_margin_pct","label":"JPM FCF 利潤率","value":-83.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JPM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bac_fcf_margin_pct","label":"BAC FCF 利潤率","value":73.37,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wfc_fcf_margin_pct","label":"WFC FCF 利潤率","value":22.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WFC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_c_fcf_margin_pct","label":"C FCF 利潤率","value":-26.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.C.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gs_fcf_margin_pct","label":"GS FCF 利潤率","value":-62.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":339.72,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":10.53,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":52.35,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":24.07,"period":"2026-10-19","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-19","citation":"yfinance earnings_estimate"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":25.5,"period":"2026-10-19","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-19","citation":"yfinance earnings_estimate"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":14.25,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝71.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":71.3,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.73,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝92.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":92.3,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.82,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝14.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":14.4,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.81,"period":"2026-10-19","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-19"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-555218.89,"period":"2026-10-19","unit":"USD m","basis":"yfinance 最新一季：總債務 1326255.05、現金 1881473.94（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":2655.6,"period":"2026-10-19","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":346941.56,"period":"2026-10-19","unit":"USD m","basis":"市值 902160.45 ＋ 淨負債 -555218.89","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":207953.21,"period":"2026-10-19","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（13 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":216308.18,"period":"2026-10-19","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.67,"period":"2026-10-19","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"JPM 全球投銀費用錢包份額維持第一：1Q26 為 9.8%，3Q26 年初至今為 9.2%（2Q26 YTD 9.3%）；3Q 投銀費用年增 14%、季減 8%，較 1Q 的年增 28% 放緩","source":"JPMorgan Chase 8-K 3Q26 earnings release narrative exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/0000019617/000162828026065582/a3q26erfexhibit991narrative.htm","excerpt":"Investment Banking fees up 14% YoY, down 8% QoQ; #1 ranking for Global Investment Banking fees with 9.2% wallet share YTD","as_of":"2026-10-14","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"1Q26 投銀費用年增 28%，全球投銀費用第一、錢包份額 9.8%","source":"JPMorgan Chase 8-K 1Q26 earnings release narrative exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/19617/000162828026024990/a1q26erfexhibit991narrative.htm","excerpt":"Investment Banking fees up 28% YoY, up 23% QoQ; #1 ranking for Global Investment Banking fees with 9.8% wallet share in 1Q26","as_of":"2026-04-14","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Dimon 2026 年 4 月股東信點名穩定幣發行者與代幣化專案為對支付與放貸業務的新興競爭威脅；JPM 自身同步發展存款代幣與穩定幣","source":"techloy: Are stablecoins and tokenization becoming a threat to banks like JPMorgan","url":"https://www.techloy.com/are-stablecoins-and-tokenization-becoming-a-threat-to-banks-like-jpmorgan.md","excerpt":"In JPMorgan Chase's April 2026 letter to shareholders, he flagged blockchain-based competitors including stablecoin issuers and tokenization projects as an emerging threat to the bank's traditional payments and lending businesses.","as_of":"2026-04-30","retrieved_at":"20261019","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"JPM Q3 2026 財報電話會議（2026-10-13）給 2027 年初步 NII（不含 Markets）約 $107B，較 Q4 2026 年化指引多約 $5B，主要來自資產負債表擴張與存放款組合，約四分之一來自殖利率曲線；預期 2027 消費存款溫和成長、批發存款續增但可能放緩、卡貸大致穩定。","source":"TIKR: JPMorgan Chase Raises Full-Year Net Interest Income Outlook Despite Missing Q3 Revenue Expectations","url":"https://www.tikr.com/blog/jpmorgan-chase-stock-raises-net-interest-income-outlook-q3-2026","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261019","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026 ex-Markets NII 年增 6% 至 $24.7B，平均放款年增 10%、平均存款年增 8%；2026 全年 NII 指引上調至約 $106.2B（ex-Markets $97.2B）。","source":"TIKR: JPMorgan Chase Raises Full-Year Net Interest Income Outlook","url":"https://www.tikr.com/blog/jpmorgan-chase-stock-raises-net-interest-income-outlook-q3-2026","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261019","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"有分析指出聯準會降息快於預期可能壓低 NII。","source":"TIKR / Zacks（JPM NII target 分析）","url":"https://www.tikr.com/blog/jpmorgan-chase-stock-raises-net-interest-income-outlook-q3-2026","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"UBS 預期大型銀行回購在 2027 年續強，涵蓋銀行平均回購約市值 5%；並預測 GSIB 投行收入年增約 23%，但提醒不宜全面外推 Dealogic 資料。","source":"iTiger 轉載 UBS 銀行研究","url":"https://www.itiger.com/news/1171346389","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261019","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"JPM 於 2026-01-01 提前採用強化版補充槓桿比率（eSLR）最終規則，槓桿緩衝改為 BHC 美國 Method 1 G-SIB 附加費的 50%。","source":"JPMorgan Chase 10-Q (period ended 2026-03-31)","url":"https://www.sec.gov/Archives/edgar/data/0000019617/000162828026029344/jpm-20260331.htm","excerpt":"the Firm early adopted the enhanced Supplementary Leverage Ratio (\"eSLR\") final rule. The final rule amended the eSLR requirements for GSIB BHCs and their insured depository institution (\"IDI\") subsidiaries by revising the previous static leverage buffers at the BHC and IDI levels to 50% of the BHC's U.S. Method 1 GSIB Surcharge","as_of":"2026-03-31","retrieved_at":"20261019","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"管理層估計 Basel III endgame 與 G-SIB 再提案使 JPM CET1 需求增加約 4%，而 Fed 對大型銀行的估計為降低約 5%；G-SIB 附加費預計 2028 年前由 4.5% 升至 5.2%，約增 200 億美元資本（其中 130 億來自短期批發融資方法修訂）。仍為提案，未見最終規則。","source":"JPMorgan Chase 10-Q (period ended 2026-06-30) 及 Q1 2026 財報電話會議（經 Yahoo Finance 摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000019617/000162828026054343/jpm-20260630.htm","excerpt":"Management estimates these regulations will require a 4% increase in CET1 capital for JPMorgan Chase, compared to the Federal Reserve's projection of a 5% capital reduction for peers.","as_of":"2026-06-30","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"JPM FY2025 10-K 風險因素：營運依賴第三方系統，含提供安全、技術、資料與雲端運算的供應商；內外部營運系統失效可能對公司與客戶造成不利影響。","source":"JPMorgan Chase & Co. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/19617/000162828026008131/jpm-20251231.htm","excerpt":"JPMorganChase also depends on its ability to access and use the operational systems of third parties, including vendors that provide security, technology, data and cloud computing services. The inaccessibility, failure or other disruption of an internal or external operational system upon which JPMorganChase's businesses depend could adversely affect JPMorganChase and its clients.","as_of":"2026-02-28","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"JPM CISO Patrick Opet 2025 年 4 月公開信批評 SaaS 模式的集中風險，指出可能有系統性後果。","source":"Plenitude Consulting, 'JP Morgan warns suppliers of SaaS risks in open letter'","url":"https://www.plenitudeconsulting.com/news-insights/jp-morgan-warns-suppliers-of-saas-risks-in-open-letter","excerpt":"IT security issues and concentration risk can have systemic consequences, Chief Information Security Officer Patrick Opet has warned.","as_of":"2025-04-30","retrieved_at":"20261019","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Dimon 2026 年股東信將烏克蘭與伊朗戰爭、中東衝突及對中國緊張列為主要關切，稱公司不能免於其影響。","source":"Yahoo Finance, Jamie Dimon's JPMorgan shareholder letter warns of 2026 risks","url":"https://finance.yahoo.com/economy/policy/articles/jamie-dimon-jpmorgan-shareholder-letter-124026235.html","excerpt":null,"as_of":"2026-04-06","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Dimon 2023 年表示若美國政府下令，JPM 會退出中國；並稱台灣戰事將使一切押注失效。中國業務含投資與企業銀行、支付、資產管理。","source":"CNBC, Jamie Dimon says JPMorgan Chase would exit China if ordered to","url":"https://www.cnbc.com/2023/11/29/jamie-dimon-says-jpmorgan-chase-would-exit-china-if-ordered-to.html","excerpt":null,"as_of":"2023-11-29","retrieved_at":"20261019","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"3Q26 CCB 營收 $21.2B、年增 9%；Card Services & Auto 營收年增 15% 至 $8.3B","source":"pulse2.com JPMorgan Chase Q3 2026 results","url":"https://pulse2.com/jpmorgan-chase-q3-2026-results","excerpt":"revenue increased 9% to $21.2 billion","as_of":"2026-10-13","retrieved_at":"20261019","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"3Q26 CIB：Markets 營收年增 15% 至 $10.3B（權益強、固收據報降 4% 至 $5.4B，兩年多來首降）；Payments 營收年增 14% 至 $5.6B","source":"JPMorgan Q3 earnings coverage (kucoin / pulse2)","url":"https://www.kucoin.com/news/flash/jpmorgan-q3-earnings-miss-expectations-amid-fixed-income-slump","excerpt":"fixed-income markets revenue declined 4% to $5.4 billion","as_of":"2026-10-13","retrieved_at":"20261019","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"3Q26 AWM 淨利年增 11% 至 $1.843B（未取得 AWM 營收數字）","source":"pulse2.com JPMorgan Chase Q3 2026 results","url":"https://pulse2.com/jpmorgan-chase-q3-2026-results","excerpt":"Asset & Wealth Management net income rose 11% to $1.843 billion","as_of":"2026-10-13","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"JPM 2026 上半年全球投行費用排名第一（Dealogic）；Morningstar 頁面稱市佔 8.4%；2Q26 投行費 $3.21B 年增 28%","source":"JPMorgan 2Q26 coverage / Morningstar quote page","url":"https://www.morningstar.com/quotes/0P0000031C","excerpt":"top global ranking in investment banking fees with an 8.4% market share","as_of":"2026-07-14","retrieved_at":"20261019","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Morningstar 稱當前投行景氣主要屬循環性而非結構性；UBS 預估 GSIB 投行營收 2026 年增約 23%；未找到 2027 共識","source":"Morningstar US Investment Banks: 2026 Q3","url":"https://www.morningstar.com/business/insights/research/us-investment-banking-and-trading-pulse","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子載明：金融機構面臨新技術（如分散式帳本上的代幣化證券）繞過中介而衝擊支付處理與其他產品的風險；落後於生成式 AI 可能流失客戶與市占。","source":"JPMorgan Chase Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/19617/000162828026008131/jpm-20251231.htm","excerpt":"risk of disruption to payments processing and other products and services from the use of new technologies that may not require intermediation","as_of":"2026-02-18","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"2026 年 1 月 Q4 財報電話會議，CFO Barnum 稱生息穩定幣若形同存款，會形成無審慎保障的平行銀行體系，是對現有商業模式的威脅（二手報導）。","source":"Techloy: Are stablecoins and tokenization becoming a threat to banks like JPMorgan","url":"https://www.techloy.com/are-stablecoins-and-tokenization-becoming-a-threat-to-banks-like-jpmorgan/","excerpt":null,"as_of":"2026-01-13","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"二手報導稱 Dimon 2026 年 4 月股東信點名穩定幣發行商與代幣化專案是對支付與放貸業務的新興威脅；同時 JPM 自建 Kinexys／JPMD 代幣化存款試點（多數專案尚無確定上線日）。","source":"Techloy: Are stablecoins and tokenization becoming a threat to banks like JPMorgan","url":"https://www.techloy.com/are-stablecoins-and-tokenization-becoming-a-threat-to-banks-like-jpmorgan/","excerpt":null,"as_of":"2026-04-08","retrieved_at":"20261019","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Q3 2026 財報會議：Dimon 表示不會讓任意外部 AI agent 進入公司；The Paypers 報導 JPM 目前封鎖外部 AI agent 代表零售客戶操作，agent 僅能經 Plaid 等聚合器讀取餘額，不能轉帳或付款，無直接開放時程。","source":"Webull transcript Q3 2026 call; The Paypers","url":"https://thepaypers.com/fintech/news/jpmorgan-chase-blocks-external-ai-agents-from-customer-accounts","excerpt":"We're not going to allow just any outside agent to come inside the company because that's just too risky","as_of":"2026-10-14","retrieved_at":"20261019","affects":["moat_trend","triggers"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Chase 計畫 2026 年新開 160 家以上分行、橫跨 30 餘州，並翻新約 600 家既有據點；屬 2024 年起三年擴張計畫（500+ 新分行）的一環，通路方向為擴充實體分行而非縮減。","source":"Axios, JPMorgan Chase to open 160 new bank branches in 2026","url":"https://www.axios.com/2026/02/18/jpmorgan-chase-bank-branches","excerpt":null,"as_of":"2026-02-18","retrieved_at":"20261019","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"分行擴張目標為取得全美零售存款 15% 市占；管理層稱分行密度與存款市占高度相關，分行投資不到四年回本。另有 2026 年 9 月報導稱 1 月至 7 月累計新開 77 家、翻新 218 家（次級來源，未對照一手文件）。","source":"Banking Dive / Fintool 分行擴張報導（搜尋摘要）","url":"https://www.bankingdive.com/news/jpmorgan-chase-160-branch-openings-2026/812460/","excerpt":null,"as_of":"2026-02-18","retrieved_at":"20261019","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"JPMorgan 旗下 Kinexys 推出機構客戶用的許可制美元存款代幣 JPMD，部署於 Base（Coinbase）；公司稱其為穩定幣之外的替代方案。屬支付／結算軌道的商業模式延伸，搜尋未找到資料存取收費相關報導。","source":"Fortune, JPMorgan Chase partners on deposit token with Coinbase","url":"https://fortune.com/crypto/2025/06/18/jpmorgan-chase-partners-deposit-token-crypto-institutional-clients-coinbase-partnership","excerpt":null,"as_of":"2025-06-18","retrieved_at":"20261019","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"搜尋未發現 2026 年 JPM 通路遭去中介化或 D2C 衝擊的具體報導；既有評論稱銀行因大舉投入科技，去中介化疑慮已降溫（次級評論，非一手）。","source":"Fidelity Australia, How are the banks fighting disruption","url":"https://fidelity.com.au/insights/investment-articles/how-are-the-banks-fighting-disruption","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261019","affects":["decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 後公司把 2026 全年 NII 指引上調至約 $106.2B（原 $105.5B），不含 Markets 約 $97.2B（原 $96.5B）；2027 不含 Markets NII 初步中心情境約 $107B","source":"Hudson Labs / tradingnews 等 Q3 2026 報導彙整（搜尋摘要）","url":"https://www.tradingnews.com/news/jpm-reverses-3-percent-premarket-drop-to-336-usd-as-20-percent-rotce-and-107b-usd-2027-nii-outlook","excerpt":"JPMorgan raised its full-year 2026 net interest income outlook to about $106.2 billion from $105.5 billion, and its NII excluding Markets to about $97.2 billion from $96.5 billion.","as_of":"2026-10-14","retrieved_at":"20261019","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q3 2026 EPS $5.57（淨利 $15.3B）低於 LSEG 共識 $5.85；與公司指引上調並存，EPS 落差為未達預期","source":"tradingnews：JPM Reverses 3% Premarket Drop ... $0.33 Miss","url":"https://www.tradingnews.com/news/jpm-reverses-3-percent-premarket-drop-to-336-usd-as-20-percent-rotce-and-107b-usd-2027-nii-outlook","excerpt":"JPM Reverses 3% Premarket Drop to $336.40 as 20% ROTCE and $107B 2027 NII Outlook Offset a $0.33 Miss","as_of":"2026-10-14","retrieved_at":"20261019","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"全年費用指引：Q2 後調高至約 $107.5B；Q3 是否再調整未能確認（none for Q3 change）","source":"Hudson Labs JPM Q3 2026 Earnings Preview","url":"https://www.hudson-labs.com/research/jpmorgan-q3-2026-earnings-preview-revenue-guidance-outlook","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261019","affects":["thesis.R","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布（13 位）：共識約 $366.50、中位 $370、低 $305、高 $420，比較基準價 $348.21（該站基準，非 DD 現價）","source":"Tickerleague JPM estimates","url":"https://tickerleague.com/companies/JPM/estimates","excerpt":"Based on price targets from 13 analysts. Low $305.00, Consensus $366.50, Median $370.00, High $420.00","as_of":"2026-09-30","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 16 位分析師平均目標價約 $340，10 買 6 持有；另 Wells Fargo 8/14 升至 $390、UBS 8/3 升至 $400","source":"Benzinga JPM price targets","url":"https://www.benzinga.com/quote/JPM/price-targets","excerpt":"Analyst Consensus — 16 Analysts, 10 Buy, 6 Hold, Consensus Rating Outperform. Avg. Consensus PT $340","as_of":"2026-09-08","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"EPS 共識近 30 天上修：2026 由 $23.87 升至 $24.21、2027 由 $24.45 升至 $25.01（Yahoo，8/28 數據，早於 Q3 未達）","source":"Yahoo Finance JPM analysis","url":"https://uk.finance.yahoo.com/quote/JPM/analysis","excerpt":"The 2026 consensus was $24.21 and 2027 was $25.01, up from $23.87 and $24.45 thirty days earlier.","as_of":"2026-08-28","retrieved_at":"20261019","affects":["valuation"],"status":"ok"},{"id":"major_events#none","axis":"major_events","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"JPM 3Q26 撥備約$2.7B（去年同期$3.4B），含淨提列準備$539M（主要在批發放款）與淨沖銷$2.2B（去年同期$2.6B）；二手來源彙整","source":"Beinsure / Pulse2 / RTTNews 對 JPM 3Q26 財報之報導（搜尋摘要）","url":"https://pulse2.com/jpmorgan-chase-q3-2026-results","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261019","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"管理層預估 4Q26 信用卡淨沖銷率約3.2%（Benzinga 財報電話會議摘要）","source":"Benzinga JPM Q3 2026 earnings call transcript summary","url":"https://www.benzinga.com/node/62318283","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261019","affects":["triggers"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"2Q26 10-Q：總信用損失準備$31.5B；放款損失準備/留存放款覆蓋率1.79%，去年同期1.85%；不良資產降6%至$9.8B","source":"JPMorgan Chase Form 10-Q（期間 2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0000019617/000162828026054343/jpm-20260630.htm","excerpt":"The total allowance for credit losses was $31.5 billion at June 30, 2026. The Firm had an allowance for loan losses to retained loans coverage ratio of 1.79%, compared with 1.85% in the prior year.","as_of":"2026-06-30","retrieved_at":"20261019","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#3","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"1Q26：放款損失準備覆蓋率1.82%（去年同期1.94%）；不良資產年增10%至$10.0B；淨提列準備$191M（批發+$327M、消費-$139M），淨沖銷$2.3B","source":"JPMorgan Chase Form 10-Q（2026-03-31）及 1Q26 8-K 簡報","url":"https://www.sec.gov/Archives/edgar/data/19617/000162828026025013/a1q26_earningsxpresentat.htm","excerpt":"Net reserve build of $191mm included a $327mm net build in Wholesale and a $139mm net release in Consumer 1Q26.","as_of":"2026-03-31","retrieved_at":"20261019","affects":["decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#4","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"產業面：2026年被描述為循環後段，違約/沖銷大致持平或略降；信用卡拖欠6月上升而沖銷率微降；Fed商業銀行30天拖欠率1Q 2.92%（低於去年高於3%的高點）","source":"S&P Global Market Intelligence 2026-05-15 研究及彙整報導（搜尋摘要）","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/05/us-bank-fundamentals-returns-stand-up-to-market-volatility","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261019","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"JPM 現行標準化 CET1 要求 11.5%（含 GSIB 附加 4.5% Method 2＋SCB 2.5%）；SCB 2.5% 維持至 2027-09-30，2027 年起以修訂後壓力測試模型重算。","source":"JPMorgan Chase 10-Q（截至 2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0000019617/000162828026054343/jpm-20260630.htm","excerpt":"The Firm's current SCB requirement is 2.5% and will remain in effect through September 30, 2027, based on the current rules.","as_of":"2026-06-30","retrieved_at":"20261019","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"financial_regulatory_capital_rules#1","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"+","claim":"美國三大銀行監管機關於 2026-03-19 重新提出 Basel III endgame 草案，意見期至 2026-06-18；機關估計 Category I/II 銀行 CET1 要求約降 4.8%，GSIB 附加費平均降約 40bp。","source":"Simpson Thacher：Basel III Endgame Evolution (2026-03-20)／Learnsignal 摘要","url":"https://www.stblaw.com/about-us/publications/view/2026/03/20/basel-iii-endgame-evolution-banking-agencies-propose-major-capital-overhaul-again","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261019","affects":["thesis.H","valuation"],"status":"ok"},{"id":"financial_regulatory_capital_rules#2","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"-","claim":"JPM 10-Q 估計依 2025-12-31 部位，Basel III 草案將使其所需 CET1 資本增加約 6%；Q1 財測會議稱 Basel 與 GSIB 兩案合計需多約 $20B 資本；GSIB 附加費提案改為年度平均計算、級距由 50bp 縮至 10bp。JPM 於 2026-06-18 提出意見書。","source":"JPMorgan 10-Q 2026-06-30；MarketBeat Q1 2026 earnings call；Bloomberg Government","url":"https://www.sec.gov/Archives/edgar/data/0000019617/000162828026054343/jpm-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261019","affects":["decision_inputs.bear","thesis.R","valuation"],"status":"ok"},{"id":"financial_regulatory_capital_rules#3","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"2026-06-18 參議院銀行委員會成員來信要求撤回提案，主張將使大型銀行吸損資本降至少 6%。最終規則狀態搜尋結果未載明。","source":"Senate Banking Committee letter 2026-06-18","url":"https://www.banking.senate.gov/imo/media/doc/20260618_letter_to_financial_regulators_re_basel_iii_proposalpdf.pdf","excerpt":null,"as_of":"2026-06-18","retrieved_at":"20261019","affects":["triggers"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：gross_margin_pct、operating_margin_pct、rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"JPM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-83.39,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JPM","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"BAC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":73.37,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WFC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":22.09,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WFC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"C","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-26.88,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.C","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-62.71,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GS","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"JPM"},"financial_history":{"ticker":"JPM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":127727000000.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":37676000000.0,"diluted_eps":12.09,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":154952000000.0,"revenue_yoy_pct":21.31,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":49552000000.0,"diluted_eps":16.23,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":169439000000.0,"revenue_yoy_pct":9.35,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":58471000000.0,"diluted_eps":19.75,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":181847000000.0,"revenue_yoy_pct":7.32,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":57048000000.0,"diluted_eps":20.02,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/JPM/JPM_Q3_2026_Earnings_Call_20261013.md）

# Q3 2026 Earnings Call
**JPMorgan Chase & Co.** | Earnings Calls | 2026-10-13

**Operator** (Operator):
Good morning, ladies and gentlemen. Welcome to JPMorgan Chase's Third Quarter 2026 Earnings Call. This call is being recorded. [Operator Instructions] We will now go live to the presentation. Information concerning forward-looking statements and non-GAAP financial measures included in this presentation can be found in JPMorgan Chase's earnings press release and investor presentation posted on the Investor Relations website. Please stand by. At this time, I would like to turn the call over to JPMorgan Chase's Chairman and CEO, Jamie Dimon; and Chief Financial Officer, Jeremy Barnum. Mr. Barnum, please go ahead.

**Jeremy Barnum** (Executives):
Thank you very much, and good morning, everyone. The firm delivered net income of $15.3 billion, EPS of $5.57 and a ROTCE of 20%. These results included $658 million of net investment securities losses in corporate. Revenue of $50.9 billion was up 8% year-on-year. Excluding the net investment securities losses, revenue was up 9% year-on-year, largely driven by markets revenue, higher deposit balances and higher asset management fees in AWM and CCB. Expenses of $27.3 billion were up 12% year-on-year, largely driven by higher volume and revenue-related expense as well as front office hiring and wage inflation. And credit costs were $2.7 billion with net charge-offs of $2.2 billion and a net reserve build of $539 million. In terms of the balance sheet, we ended the quarter with a standardized CET1 ratio of 13.9%, down 30 basis points versus the prior quarter as net income was more than offset by OCI losses, higher RWA and capital distributions. 
You'll note that we've updated the categories on the RWA walk to make it a bit more useful. This quarter's standardized RWA increase of about $52 billion is predominantly driven by an increase in lending across Banking, Markets and AWM as well as the impact of higher energy prices and increased market volatility. Now moving to our businesses. CCB reported net income of $5.7 billion. Revenue of $21.2 billion was up 9% year-on-year, predominantly driven by higher balances and yield in card, asset management fees, deposit balances and auto lease income. 
A few points to highlight. Debit and credit spend grew 10% year-on-year with continued momentum across spending categories, including gas and travel, supported by consumer demand. Deposit growth of 4% year-on-year was stronger this quarter as we continue to grow our customer base across consumer and business banking, and we retained our #1 position in retail deposit share based on FDIC data. And client investment assets crossed $1.4 trillion, up 15% year-on-year, driven by market performance and strong flows. Next, the CIB reported net income of $8.2 billion. Revenue of $22.7 billion was up 14% year-on-year on strong performance across the businesses. 
IB fees were up 14% year-on-year, reflecting strong performance across products, notably in advisory. While our outlook remains constructive, supported by ongoing client engagement, evolving market conditions have recently slowed activity a bit, so we'll have to see how the quarter develops. In Markets, fixed income was down 4% year-on-year with lower revenues in commodities, rates and credit, largely offset by higher client flows in currencies and emerging markets. Equities was up 49% year-on-year with continued outperformance across the franchise, notably in prime and derivatives. Turning to Asset & Wealth Management. AWM reported net income of $1.8 billion with a pretax margin of 36%. Revenue of $6.9 billion was up 14% year-on-year, predominantly driven by growth in management fees on higher average market levels and strong net inflows as well as higher loan balances. 
Long-term net inflows were $51 billion, largely driven by continued strength in fixed income. AUM of $5.2 trillion, was up 13% year-on-year, and client assets of $7.9 trillion, were up 15% year-on-year, driven by continued net inflows and higher market levels. Finally, Corporate reported a net loss of $455 million, which included the net investment securities losses mentioned earlier on revenue of $93 million. Turning to the outlook. I'm going to update the full year guidance by giving you the fourth quarter. The implied full year numbers are on the page. We expect fourth quarter NII ex markets to be approximately $25.5 billion and fourth quarter total NII to be about $28 billion. And as we've done for a couple of years, you'll note we gave you a central case for 2027 NII ex markets of approximately $107 billion, which we'll refine further next quarter. 
It's important to remember that this central case is based on a series of assumptions that are obviously highly uncertain even under the best of circumstances. On expense, we expect the fourth quarter to be about $27.5 billion with the implied full year increase reflecting higher volume and revenue-related expense driven by continued elevated activity levels. Finally, we continue to expect the card net charge-off rate to be approximately 3.2%.
With that, we're now happy to take your questions. So let's open the line for Q&A.

**Operator** (Operator):
[Operator Instructions]  Our first question comes from Ebrahim Poonawala with Bank of America.

**Ebrahim Poonawala** (Analysts):
I guess maybe one question, just -- there's been a lot of discussion around all things AI over the last couple of months. And maybe if there are 2 things that you can address specifically, one, when we think about the disruption risk to agentic AI, I know you've talked about in the past. Maybe just frame that given your visibility into the technology, how you think about that? And also the challenge of implementing agentic AI inside a bank given the emergence of all the rogue agents? And does that make it harder for a bank to actually deploy agentic AI as we think about just competitive challenges?

**Jeremy Barnum** (Executives):
I'll start and you want to jump in? Yes, okay. So on the disruption point, a couple of things. There's obviously been a lot of focus on the Smart Cash solution, which I think is a small piece of the overall story. But that is live now actually as of the last couple of weeks, very, very early days, and it remains kind of a targeted pilot type thing. But it is interesting to learn some things about what clients care about and sort of see how it works to kind of sell a product like this in the field. So I mean more to come on that in the future. Early days, interesting so far. I think the bigger picture here is around -- there have been a couple of releases of personal agents this quarter, which have really gotten a bunch of attention in the market and we saw a little bit of a response in bank stocks around those releases. 
And I guess the way we think about that from our perspective is that on the one hand, it's nothing new, and that -- but that doesn't mean that we're complacent about it. So if you think about what is the nature of the competition that comes from these agents, it's really the intersection of 2 things that we've been talking about for a long time. One is yield-seeking flows. So obviously, we deal today and have dealt with all the various rate cycles with a lot of competition from yield-seeking flows. And our strategy remains focusing on primary bank share, not chasing every dollar of yield-seeking money. So that doesn't mean that competitive pressure isn't real. It just means it's not particularly new. The other piece is competition from fintechs who are innovating and providing great customer experiences. And we've also been talking about that for a long time and the criticality of ensuring that we have parity with them and that we're leaning in enough to make sure that we're giving people the experiences that they want through all the various channels including digital. 
And so in that sense, the kind of agentic personal agents, whatever stuff is just the intersection of those 2 things, and it's not new. As I said, that doesn't mean we're complacent about it. We're spending a lot of time on it, and it's going to be interesting to see how the space develops and what we ourselves offer there at some point. But when you take a really big step back from a competitive position, I think we really like our hand in no small part because of the sort of multiple decades of investment in the branch network, the value proposition and not least trust that our customers have in us.

**James Dimon** (Executives):
I would just add, internally, we use agents to do good things here, and we're going to continue to do that. And we do -- we'll use it for customers, but our focus will always be do a great job for customers. And so we're not against agents or for agents something like that. There are tools you use them for the customers. There is a defensive side, which is you got to make sure our customers are not hurt by it. And so that is of concern. But that's -- think of it as an AI agentic concern, which is heightened because you don't want rogue agents and there could be thousands of them. 
And so we've always been literally on the side of the client. The people are using them, they should understand the risk. There's a liability transfer, they should understand the liability transfer. If that is being misused, they should understand it's being misused. So we have to make sure we protect our customer in the right kind of way. So we're building tools to do that, too. In the meantime, we're not going to allow just any agent to come -- outside agent to come in inside the company because that's just too risky for clients and for JPMorgan.

**Ebrahim Poonawala** (Analysts):
Got it. That's good color. And just separately, I think as we assess the risk of interest rates may be moving even higher than what we saw in the third quarter, maybe your latest thoughts around how you assess the resiliency of the economy to handle maybe a 6% rate on 10-year and just the Fed hiking a few times. Do you think the risk of a market event or just stress on the economy is meaningful as we kind of discount that?

**James Dimon** (Executives):
I think we have to -- we always prepare for all different events. And that's not the same as predicting them because we want to be a strong company, helping our clients, our communities, countries around the world through thick or thin. So of course, things like that can happen. We never take it off the table. And they can happen for good reason, which is a lot of demand for capital, a lot of productivity and things are fine. They can happen for a bad reason, sticky inflation around the world, they can happen not because it's in the United States, they can happen because what happens overseas. So we're not predicting it. I've always thought there's a higher chance than other people. I still kind of think that, but that's not a prediction. That's just a -- think of that as cautious preparation.

**Operator** (Operator):
Our next question comes from John McDonald with Truist.

**John McDonald** (Analysts):
I was hoping, Jeremy, you could unpack the new outlook for 2027 NII, the central case that you gave, including some of the assumptions around the balance sheet growth, deposit pricing and the impact of higher rates.

**Jeremy Barnum** (Executives):
Yes. Sure, John. No problem. So if you start with what we've given you as the NII ex Markets guide for fourth quarter, which is $25.5 billion and you annualize that, you get something like $102 billion. So we're essentially giving you guiding to $5 billion of growth from that to the $107 billion. That $5 billion, probably about 1/4 of that, I would say, is related to the yield curve. So we remain asset sensitive and probably a little bit more asset sensitive than the EAR shows just because of the lower than modeled consumer deposit betas. So about 1/4 of that is the hikes that are currently in the forward curve. I think there's 1 in December and then 2 through the first half of the year. And the rest of it, I would actually describe pretty straightforwardly as just the continuation of the balance sheet growth and mix trends that we've seen this year. 
So both continued modest consumer deposit growth, continued wholesale deposit growth, probably wholesale a bit weaker than what was very strong this year, but we don't actually know. And then Card loans, which obviously can be a big driver of NII continued at comp levels. So actually a pretty straightforward story, I would say. I gave you caveats, but -- I gave you the caveats on the prepared remarks.

**James Dimon** (Executives):
I will add one more thing. I think there's more uncertainty around that number than normal because of all the things going on around the world. So -- and obviously, it also relates to what we do, which we can change at any point in time.

**John McDonald** (Analysts):
Okay. That's helpful. And Jeremy, on expenses, if we move over to there, do you have any preliminary thoughts on your investment spend plans for next year, the other drivers of expenses and how those might line up with the current Street forecast for expenses next year?

**Jeremy Barnum** (Executives):
Yes. So we try to draw a little bit of a distinction between NII and expenses in the sense that despite Jamie's comments, which are obviously true that we can modify the structure of the balance sheet to change the NII, in general, undisturbed the NII is kind of a property of the balance sheet at any given point in time, and it is not that sensitive to the budget cycle. And therefore, we feel like we don't have a very good excuse at this point in the year for pretending that we don't have an opinion about 2027. Expenses are a little different in the sense that they are still sensitive to the budget cycle, and there are a lot of discretionary decisions to get made in there. And while we have some preliminary views, we're kind of not done with that. And you will remember, obviously, John, last year, we did point out that our preliminary read on expenses suggested that the market's consensus was a bit off. 
That seems to be quite a bit less true this year. So we see the consensus right now for 2027 expenses being around $114 billion, and our current preliminary read isn't too far from that. So kind of no news on that front, I would say. And let's see how the budget cycle finishes. And as Jamie points out, I think the uncertainty isn't just about the macro environment. It's also about how dynamic the investment picture is and the effects of AI, et cetera, et cetera, et cetera. So a lot of moving parts. But for now, the consensus doesn't seem too far off.

**Operator** (Operator):
Our next question comes from Erika Najarian with UBS.

**L. Erika Penala** (Analysts):
My first question just is on capital management. We were fielding a lot of inbound questions from investors in terms of the $1 billion buyback versus the normal cadence of around $7 billion. And I know that there's no normal cadence, and I know that buyback is the last priority. But perhaps take us through how you should think -- we should think about your capital priorities, particularly given that we're hearing that Basel III endgame and G-SIB should be finalized at year-end.

**James Dimon** (Executives):
Yes. So I think we've told you all that we have probably $30 billion or something of excess capital roughly, just estimating what all those end games are, which we don't know, but that's plenty. But the capital hierarchy has always been the same. I mean after you pay a dividend, which hopefully will be steady, we'd like -- we really like investing in organic growth. That is the highest and best use of capital for our shareholders. And obviously, buyback comes after that, particularly when stock prices are up. So the positive news is the main reason the buyback is down, and it's got nothing to do with AOCI or guessing about the environment or even Basel III. 
We believe now, which is different than we told you in the past that we can redeploy that capital at very good returns over time. And redeploying that capital at very good returns over time is far better than buying stock at a 6% or whatever the earnings yield would be if you bought it today. And that's simple. I mean that's good. That's good for shareholders. And I'll give you one example, and I think there are many more, but the security resiliency initiative, we told you all we deployed $1.5 trillion over 10 years. And we haven't -- I don't think we disclosed the number, but the first year is probably over $200 billion already, and we'll disclose that and do some work on it. But I guess it will be considerably more than that. And the world needs capital, the world needs advice, the world is becoming more complex, assets under management around the world are bigger. And so we think there's good news in the long run. And we can't tell you what it means for the next 6 months, but that's why we're doing it. We hope to deploy it very well for our shareholders.

**Jeremy Barnum** (Executives):
Yes. And the only thing I would add to that, Erika, is just that if you notice what the journey has been on the CET1 ratio, I want to say that we started at something like 15.7%, and we're now at 13.9% during a period during which we've done a ton of internal deployment. So there's been a lot of organic growth in RWA and some of the investments that Jamie alludes to. And during that period, we've also done a bunch of buybacks. So -- but at this point, as Jamie says, the speed with which we've been able to deploy organically relative to the amount of excess that we have and the environment seems pretty clear that it makes sense to keep dry powder.

**James Dimon** (Executives):
I want to brag on the investment bank a little bit. So they've hired a tremendous amount of very talented people in SRI, and we're lucky to have Todd Combs here investing some of the capital. They've had a lot of ideas. It's not just meeting at this point. They've helped fund some interesting types of things. We have more ideas. They're doing a really great policy around it, too, which is what can you do to accelerate security resilience in the United States around shipbuilding or we had a big announcement in Philadelphia. So I just -- I'm proud of them. We've had a bunch of people who retired, who raised their hand. They're coming back more for patriotism than anything else. And so -- it's just a great effort for the company. 
As we pointed out, it's global and the global response has also been exceptional. I have something across my desk, which is alone over $10 billion or $20 billion of financing in one country. So a lot more to come. And I would put in the same category, the American Dream Initiative, the Innovation Economy Initiative, the Commercial Banking Initiative around the world. These things are working. We think we're doing the right kind of good business and good returns.

**L. Erika Penala** (Analysts):
So as a follow-up here, that all sounds very positive for activity levels going forward in a very broad way. And Jamie, I know you did some media over the past few weeks and talked about the pipeline. And maybe in that context, especially given market fears, that the bond market rout around the world has a chilling effect on activity levels. Maybe talk about what the pipeline looks like for activity levels in both the investment -- both Wall Street and Main Street.

**James Dimon** (Executives):
Well, first, before I do that, the bond volatility in the market, the fear is not going to change what we do. We serve clients through thick or thin. We know that -- I call some of the economic winds. It's the weather. That's not exactly referred to. The pipeline is fine. But I pointed out many times before, the pipeline is like an accordion. It can open close pretty quick. You've seen in the United States, it's been, as Jeremy says, the word delayed, probably, we don't really know, and we'll see. And I was in Europe recently, and the pipeline there is actually quite healthy and even more so in IPOs than we would have thought. So we just don't know and -- but serving the clients and doing a good job is the most important thing. Pipelines, we always forecast the pipeline, as you call the probability...

**Jeremy Barnum** (Executives):
The probability adjustment.

**James Dimon** (Executives):
And we know one thing for sure. It will be wrong.

**Jeremy Barnum** (Executives):
It's important to emphasize, like when Jamie and I talk about not knowing, I think we mean we don't obviously know exactly what investment banking fee revenue is going to be in the fourth quarter. I think that we do know that the overall environment is robust and supportive, and there's a lot of business that wants to get done and needs to get done. And as you point out, Erika, not surprisingly, given the rate sell-off, you're going to have the market take a little bit of a breath and a pause to make sure buyers and sellers can meet on valuation terms. And so we did see a little bit of that slowdown in the second half of September basically, and we'll see how that plays out into December, but -- I mean, sorry, into the fourth quarter. But the big picture, I think, is pretty clear.

**Operator** (Operator):
Our next question comes from Chris McGratty with KBW.

**Christopher McGratty** (Analysts):
Just following up on the capital allocation. Maybe a comment or 2 on where you're less comfortable allocating capital to. It seems like there's plenty of opportunities to deploy it. Where are you pulling back? Where are you seeing structures or peers maybe doing something you may not want to do?

**James Dimon** (Executives):
I'm not going to give you very specific stuff, but we're tightening up a little bit on credit. I think some of the credit terms have gotten a little bit loose. And you've heard us talk about that before and other people, a little too much PIK, a little too weak covenants, a little too much priming good assets, little too much, pushing on it. We just don't feel you have to chase that kind of stuff anymore.

**Christopher McGratty** (Analysts):
Okay. Great. And then secondarily, the health of the consumer is getting a lot of attention. I guess the question is durability to withstand these kind of rates. I think you talked about 10% year-on-year spend in debit and credit. If we're a year from now and we still have rates where we are, what's your expectation for the ability for the consumer to hold on?

**Jeremy Barnum** (Executives):
I mean, obviously, if you keep real rates very, very high for a long time, at some level, that's designed to slow down economic activity to fight inflation. And it's hard to imagine that, that wouldn't have an impact on the consumer. So far, what we see in the current data and what's been true, I would say, for the last few years is that the consumer has been quite resilient in the face of a number of headwinds that under different circumstances you might have expected would present a challenge. But I think the conditional expectation of consumer credit health as a function of higher rates is a fairly nuanced question. But fundamentally, the picture is pretty simple. Like the consumer is currently very healthy, primarily because of a healthy labor market. But the Central Bank needs things to cool off and that involves an aggressive extended rate cycle, almost by definition, that's going to involve higher unemployment, which will produce weaker consumer credit results.

**Operator** (Operator):
Our next question comes from Ken Usdin with Autonomous Research.

**Kenneth Usdin** (Analysts):
On the consumer side, it's nice to see the 4% year-over-year CCB deposit growth. I just wondering, aside from agentic, just what are you seeing in terms of either rate-seeking behavior? Is it the deposit margin has been up for the last few quarters, which is also good to see. And I'm just wondering any change in your expectations for either growth or how you're adjusting to the current marketplace and competition for deposits?

**Jeremy Barnum** (Executives):
Sure. Yes, it's an important question. It's a good question. I think the simple answer is no significant change to our core expectations here. I think we've seen kind of the reassertion of consumer deposit growth over the last couple of quarters as the yield-seeking flows have faded and that continues to be our basic expectation. So that's the big picture. I do think that since that outlook was shaped, we have seen a somewhat higher rate environment, and that does raise the question of what will be the impact of that on consumer deposits. So in the normal course, you will obviously have higher rate paid from the high beta products from CDs and premium deposits. And all else equal, you would probably expect some amount of additional internal migration out of checking and savings into CDs or simplicity, resulting in higher weighted average rate paid. 
And maybe you see a little bit of additional outflow pressure, which results in, therefore, slightly weaker deposit growth. So that's all totally speculative. And it's very much a function of which side of the argument you land on in terms of some people believe, well, all the cash sorting that's going to happen has already happened and therefore, these things are relatively insensitive to slightly higher rates. I don't personally believe that. I think it's probably a little bit more on a continuum than that. And therefore, I would expect a little bit of additional pressure. But in the end, it's a matter of degree. No one really knows. And the good news, I would say, is that the core franchise performance is exceptionally strong, driven in no small part by the net new checking account acquisition, which I think we had like 650,000 this quarter or something. 
So it's really been very, very strong, and it's proof of kind of the value proposition and the engagement that we're seeing through our marketing efforts and the power of the brand. So from a long-term perspective, that's the most important thing and the impact of rates in the near term will just be what it is.

**Kenneth Usdin** (Analysts):
Excellent. One follow-up on the markets business. Obviously, we're seeing quite a bifurcation of just the continued strength in equities. And as you mentioned earlier, there are some tougher comps, I guess, and the impact of higher rates on FICC. Any change to just client demand for balance sheet usage? Is it kind of insatiable as it seems to be in the equities business? Just the state of things in the markets business in terms of activity and kind of your willingness to provide balance sheet, but more so the demand side, too.

**Jeremy Barnum** (Executives):
Yes. So at a high level, I think the simple answer is no real change. Yes, I like your insatiable -- yes, exactly. I like your insatiable demand for capital point that feels about right. I haven't heard anything to the contrary, frankly, recently. But to Jamie's point about tightening up credit, that's a little bit of an overall point about just making sure we're really scrubbing everything. And in this moment where AI is such an overwhelming theme, it's producing so much innovation and so many different pockets. There's capital being tapped through all kinds of different mechanisms. We just need to be really, really on top of things to make sure that nothing slips through.

**Operator** (Operator):
Our next question comes from Mike Mayo with Wells Fargo Securities.

**Michael Mayo** (Analysts):
Can you say the degree that AI helps out JPMorgan? I saw you were ranked highly in a recent AI and bank poll. But I squint and I look at the earnings release, I'm trying to find the benefits, and I'm not sure if I can. I think -- and you can update these numbers. You spend, what, $2 billion in AI and you have like $2 billion of benefits or maybe that stale, if you could update that. And then also address the risk that AI agents will take deposits out of JPMorgan. And as far as that answer, maybe you can talk about that value proposition and the trust and the way you protect customers' privacy and the value they place on that.

**Jeremy Barnum** (Executives):
Yes. So Mike, let me just tidy up a couple of things. So first of all, on the AI expense, you're right. I think we did say that in some media setting at some point. I think it's not exactly right, and I think we corrected it later. I think the -- at the time, and I think it is a little stale at this point, the AI expense number was significantly less than that. I want to say something like $700 million annually or something like that. But more importantly, like there's a lot of counting effects there, right? If you sort of price out the amount of time we're all spending thinking about it, you can probably get a higher number, too. So it's, at this point, like not really something that you can ring fence. It's pretty well diffused inside the whole institution, and it's obviously like a very, very high priority. 
On the question of benefits, you're right, we have quantified that in the past. I'm really trying to move away from that. I think that old quantification was accurate and correct as far as it went, but it included a lot of, what you might call, pre-generative AI, machine learning type stuff that's particularly significant in consumer fraud prevention and so on. And that -- while that's relevant, I think when you and others ask about AI in the current moment, you're really asking about the impact of generative and agentic AI on productivity, on the expense line across a range of places, especially software engineering, but also other places. And maybe you're asking about new exciting revenue opportunities at the margin. And so that, I think, is the more relevant focus right now. And I'm just very reluctant to spend a lot of energy quantifying it because it winds up wasting a lot of people's time inside the institution when we actually need to get them to focus on doing things. 
So on that point, and in terms of the visibility of the benefits, I think you're right to point out that the benefits aren't observable in our current quarterly earnings. And I think that's probably not that surprising because as much -- as important and dramatic and exciting as this theme is, it takes a long time to really do things that are visible at an institution of our size. I can tell you that just anecdotally for me personally, the types of use cases and benefits that I'm starting to see even in my own technology organization that supports finance are increasingly exciting. 
We've done some experiments of some minor legacy tools that need to be rewritten and trying to see if we could essentially one shot the rewrite in like a couple of weeks and it didn't work perfectly, but you're starting to see some really exciting opportunities for acceleration and productivity change. So how long it's going to take for that to show up, we'll see. And obviously, some of those benefits are going to be offset with token costs, which is a whole other conversation, but we're excited. There's a lot going on. And I guess your other question was the agentic question and the trust question. I think I addressed some of that earlier already. But at a high level, as Jamie pointed out, the true north here is protecting the client -- and the company, obviously, but narrowly focusing on agents giving customers access to money movement in their accounts. 
I think right now, some of the services that offer that do it through credential sharing, and we have a long record of being against that way of doing things, screen scraping, et cetera. It's not secure. And so to the extent that we're able to block those, we are blocking them to protect customers and protect ourselves. And it's important that customers understand that if they give up their credentials to the agent and the agent does something that they don't want, that's going to be on them. And that's sort of not an ideal state of things. We are working on being able to do this correctly. So that's a piece of the puzzle. And in the big picture, trust is clearly an asset, and we've spent decades building it. And as I said previously, we like our hand in that respect. But we need to be clear that the fact that we're trusted is not an excuse for complacency or a reason to provide mediocre customer experiences. So we really need to do both at the same time.

**Michael Mayo** (Analysts):
And one short follow-up on the token costs. Do you get a benefit from scale with the token cost, say, versus a small bank? And are you also transitioning more toward kind of open model AI systems that can cost a lot less?

**Jeremy Barnum** (Executives):
It's a little bit of everything. I would say our strategy is quite focused on minimizing lock-in and maximizing optionality and the ability to manage costs. So part of the strategy is model agnosticism, harness agnosticism and ability to run both proprietary models, but also open weight and open source models, some of which we run in our data center. So it's very much an all of the above strategy designed to get the best of what's available at the best price and control our own destiny.

**James Dimon** (Executives):
And there are tools coming that model routing but send it to the best, quickest, cheapest, you don't need the most expensive thing for every query you have and very often people just see the one they're comfortable with. So that's all coming to have that cost under control.

**Operator** (Operator):
Our next question comes from Gerard Cassidy with RBC.

**Gerard Cassidy** (Analysts):
Can you guys share with us the deposit beta outlook? Obviously, interest rates are starting to go up. The Fed fund futures are suggesting more rate increases over the next 3 to 6 months. And with your growth in your consumer deposit base since the last tightening cycle in '22, '23, how are you guys thinking about what you might see this time around? And also, obviously, we're starting from a much higher interest rate level than we did in '22. So could that mean deposit betas may not be as high this time around for you folks?

**Jeremy Barnum** (Executives):
So it's a very good question, Gerard, actually. And I think it is an important thing for people to be thinking about because this particular rate cycle, this latest rate cycle is arguably even more unprecedented than the last one. We just don't have a lot of historical data about how people behave when you see rate hikes from the launch point that we've seen in this cycle. So it's been an unusual 10-plus years, I would say. 
And I think it's quite important for people to realize, especially people who are doing this by training models on historical data that the historical data set is just not that rich. So it's very important to be kind of thinking out of the box. In that context, though, I think locally, our beta story is pretty easy actually in the sense that you can almost think about the franchise as pretty barbelled between a bunch of very high beta deposits like most of wholesale as well as CDs and premium deposit and consumer and then a stack of very low beta deposits. And the question is probably less the pricing of any given product, although that's always going to respond to competition and to market conditions and more the sort of migration behaviors across products in this cycle. And I don't think we have -- like our local expectations are that it's going to behave roughly the way it has been behaving. But I do think it's right to note that this is a different cycle, and therefore, we have to be thinking about all scenarios as we always do.

**Gerard Cassidy** (Analysts):
Very good. And then pivoting over to a different question. The IMF came out very recently this month with the global stability report, and they have talked about how the hedge fund industry has grown dramatically and it's now in their eyes, a systemic risk. Leveraged finance, in particular, was highlighted as another high risk. Obviously, that's in your guys' wheelhouse as with your peers and competitors. Can you share with us your insights on how you're managing these risks? And what do you worry about since these businesses now are so much bigger today than they were 10 or 15 years ago?

**James Dimon** (Executives):
We worry about a lot of stuff, not what the IMF thinks about it.

**Gerard Cassidy** (Analysts):
Got it.

**James Dimon** (Executives):
They aren't wrong because there's a lot of leverage in some of this stuff.

**Jeremy Barnum** (Executives):
Yes, yes. I mean it's not wrong, but it's also a little bit obvious. And I would also say it's not really new, right? I mean the hedge fund industry has been relevant to our franchise for decades now and a source of risk for the system for a long time now, and everyone knows that, including the hedge funds themselves that are increasingly institutionalized with very professional risk management and control over their margin relationships and stuff like that. So there is risk. Obviously, that's the business is knowing it and managing it and preparing for the unknown. But I would say that hedge fund leverage as a contributor of risk to the system is very much in the category of known unknowns. It doesn't mean it's riskless, but we kind of know what it is.

**James Dimon** (Executives):
There are a couple of unwinds that happened recently, not huge, some on the equity side, some on the fixed income arbitrage type of side, and they were handled pretty easily by the Street.

**Operator** (Operator):
Our next question comes from Glenn Schorr with Evercore ISI.

**Glenn Schorr** (Analysts):
One quick follow-up on the whole Agentic and AI impact across the deposit portfolio. My question is your comfort level and ability to protect from the standpoint of how you and the regulators thinking about liquidity stress testing and liquidity risk management and just by the nature of the technology existing, do things change? I don't know if I'm being too much into the future here, but...

**Jeremy Barnum** (Executives):
Yes. No, I understand the question, Glenn. I mean you can argue that it's sort of downstream of the narrative that the SVB run was a sort of social media phenomenon. And we were never big buyers of that idea. I think the better way to understand that situation was an extremely concentrated and undiversified deposit base that was wholesale non-op and kind of monoculture in terms of who was shaping the thinking around that. And so arguably, in a world with TV and fax machines, I think you probably would have gotten essentially the same answer in terms of the speed of the run. It might have been the processing of the fax machines into wires might have taken an additional 8 hours, but the core ingredients there were the same. So I think everyone is pretty eager to tell a sort of fast deposit run story in this new technology-enabled world. 
I'm just a little bit less persuaded that you really have cliff effects there. And sure, therefore, like in a world with agentic consumer cash movement, it's easy to create a story where it becomes even easier to move cash under certain types of crises. But I think the right way to sort of ensure that your deposits are stable is to run the company with fortress principles so that people are confident in you. And the ease -- you're probably not supposed to be hoping that your deposits are stable because the money is difficult to move, I guess, is what I would say.

**Glenn Schorr** (Analysts):
I think that's fair. I appreciate that. One...

**James Dimon** (Executives):
You take a big step back, we have $1.5 trillion of cash in marketable securities, so not worried about JPMorgan liquidity. But if you take a big step back, banking services are necessary, credit cards and debit cards and moving money and insured deposits and need of branches. And one of the ways you earn that is NII from money that sits there idle. But if you couldn't do it that way, over time, you do something different. Subscription, of course, you're getting investment accounts combined with checking accounts. And so over time, it will adjust. We want to do a great job for our clients. It will cost a lot of money to run these banking systems. Most of it is a fixed cost. 
So I'm not worried about over time. But in the short run, of course, you got to figure out how you want to handle that kind of stuff. And I do think you raised an issue, which is different, which is should regulators be thinking about what they're going to do with some of these things. Yes, of course, they should. It's a new world and with all these bots and agents and stuff like that, could someone get hurt and cause a problem? Maybe. If I was a regulator, I try to be prepared for that.

**Glenn Schorr** (Analysts):
Got you. I have one question on concentration risk. The public equity markets don't know anything about that and don't care. But bank loan books and bond books and insurance portfolios do. So I guess my question is this amazing hyperscaler race to expand compute power and everybody wants to finance it, the money and capital is there. But from your vantage point, can we finance it without breaking some concentration limit issues? Like can the market digest what the compute power suggests for the spend?

**Jeremy Barnum** (Executives):
Yes, it's a really good question, right? Because I mean, we think a lot about our current exposure to that. But arguably, the more important question is our appetite for future exposure in light of the kind of announced amount of CapEx that needs to happen in this ecosystem and the associated demands or requirements for capital from the financial system. So I guess a couple of things. One, clearly, single issuer concentration is a thing that's going to get managed. And clearly, given the nature of these structures, you have to be sophisticated about assessing both your indirect exposure, your direct exposure, where you sit in the capital structure, the value of the collateral, like there's a lot of nuanced credit analysis that needs to be done correctly to assess your individual issuer exposure across the ecosystem. 
And you can assume that institutions are going to contain that. And I guess one thing that we've seen over the last year is just increasing usage of different parts of the capital markets ecosystem to get as much diversified financing of this build-out as possible. And there is a lot of capital out there waiting to be deployed. So some of it will be from the banking system, some of it will be from elsewhere. But I think at the system level, I don't know, some people are talking about crowding out effects, so that will be interesting to see. But anyway, I think for us, we need to focus on our institutional risk appetite and institutional [ exposure ]. And I think there, in addition to the obvious single name focus, the other thing to be very careful about is just the AI theme because the AI theme is so broadly diffused into the marketplace, it's not just traditional construction lending.
Now increasingly, it's working capital revolvers. You also see it in the equity markets. It's kind of everywhere. And so you really need to be running stresses that test your resilience to a meaningful change in the overall theme across the entire enterprise. And that's something that we spend a lot of time thinking about. Currently, our exposures are still quite modest in the context of our overall wholesale exposure, but that's not the same as saying that we would be immune to a major change in sentiment in the AI space. I think I would be surprised if anyone, frankly, was immune to that at this point.

**Operator** (Operator):
Next, we will go to the line of Manan Gosalia from Morgan Stanley.

**Manan Gosalia** (Analysts):
I wanted to check in on the commercial banking side. What are you seeing with your core middle market clients? Is there an insatiable demand for capital there, too? Or as short-end rates move higher, the belly of the curve moves higher, are you seeing any pullback in demand there?

**Jeremy Barnum** (Executives):
Yes. I don't think that when we talk about the insatiable demand for capital, we're talking about our core middle market clients. I think there, the theme for some time now has been people worried about other people while doing fine themselves. The theme is always like, Oh, we run these surveys and they're also like, Oh, I'm worried about this. I'm worried about that. And it's like, how are you doing? I'm doing great. So it's kind of an interesting dynamic there. No question that higher rates, I think input costs, inflation, the diesel narrative, like these things are tough for middle market clients. And so we see them trying to manage that to the best of their ability. And I think it does create a little bit of caution in that space. But I think balance sheets are strong. People have been through a lot over the last few years, and so they're well prepared. But yes, I don't think insatiable demand for capital applies to that subset of the client base.

**Manan Gosalia** (Analysts):
Got it. And then separately, Jeremy, on the liquidity side, in the past, you've noted that you need to see changes in the liquidity rules to fully realize the impact of freeing up excess capital. As we get closer to the regulators coming out with new liquidity proposals and if you do get more credit for discount window readiness, how would that change how you manage the balance sheet and over what time frame?

**James Dimon** (Executives):
I think it's right for the regulators to look at all these things again. And it's not just the discount window, it's FHLB, the inconsistencies between resolution and recovery. It's what counts as HQLA to start with, how you do LCR. I think they should look at all that with the view that I think you can create safer banks with more deployed capital and more liquidity you can use to intermediate markets. And that should be the goal. But you really -- it's hard to answer the question because this is going to be up to them. Either way, JPMorgan will serve our clients and do a good job and take care of and do what we're supposed to do. But I think they should be doing that. So we'll see. We don't speculate what they're going to do with a lot of proposals out there, part of the international rules, but I applaud them for looking at it.

**Jeremy Barnum** (Executives):
Yes. No, I think I agree with everything Jamie said, and it's really particularly complicated across a range of dimensions. I will note that at company update, we actually talked about this and in some sense, kind of gave you the answer because what we said at the time was that the problem with the situation where the system has a healthy amount of capital is relatively liquidity constrained is that just at the margin, it leads you to have your asset deployment be in much higher risk density instruments essentially. And so a place where you're a little bit more balanced would tend to move you towards lower risk density, and it just enables you to serve broader part of the economy, including mortgages, consumer lending, but also some of the more secured C&I type structures.

**James Dimon** (Executives):
If they want to reduce the size of the Fed balance sheet, they're going to have to make some changes.

**Operator** (Operator):
Our next question comes from Matt O'Connor with Deutsche Bank.

**Matthew O'Connor** (Analysts):
I was hoping you could talk more about how you're growing noninterest-bearing deposits when a number of peers aren't. And then just how you're thinking about that specific bucket of deposits in a higher rate environment if you can continue to grow them?

**Jeremy Barnum** (Executives):
Yes. I mean I think I've sort of addressed that point to some degree in connection with, I think, my answer to John's question on the 2027 NII outlook and how we're feeling about consumer deposit growth. But I guess just to reiterate a couple of points, like number one, our net new checking account growth has been exceptionally strong, 650,000 this quarter. So people are reacting. They're responding well to the marketing. They're responding well to the brand, the value proposition to the sort of multi-decade investment in the product bundle that we offer our consumers. 
So I think that's really good news and has been a contributor to the kind of reassertion of consumer deposit growth. As I noted, the question a little bit in this rate hiking cycle is going to be how those balances behave and how pricing pressure behaves and how much migration we see to higher beta products and so on. And we'll see. I think we're relatively optimistic right now, and we wouldn't expect radical changes for like small local moves. But we do think a lot about the different rate regimes and how that can affect deposit beta. I think that's part of just being prepared for everything.

**Matthew O'Connor** (Analysts):
Okay. And I guess I was thinking more specifically the noninterest-bearing deposits, which I think are more kind of in the commercial corporate side of things. So I was just trying to see if there's any color there in terms of like cash management products, things that have been a key driver.

**James Dimon** (Executives):
The cash, most of the noninterest-bearing is consumer, and that's just because we're growing the business and you have different products for different types of consumers. And I think the wholesale side, commercial is much more competitive than that.

**Jeremy Barnum** (Executives):
Yes. No, I think to be honest, the reporting is a little confusing in part because of the famous ECR product that sometimes makes it look like on the wholesale side, there are more noninterest-bearing deposits than there actually are. That's just an artifact of the rules for how we have to report. So if you want a bit more color on that, Matt, you can follow up with IR. But at a high level, I would say that wholesale deposits have been -- continue to be and in fact, at the margin are a little bit more competitive, but the way to think about that is not that the product offering allows us to grow noninterest bearing deposits. It's -- there's an overall margin that you earn on your deposits as part of the bundle of products, and that's a function of how good your service offering is. And we have quite a good track record there of winning share and winning mandates as a function of quality of our products.

**Operator** (Operator):
Our next question comes from David Chiaverini with Jefferies.

**David Chiaverini** (Analysts):
So JPMorgan's ROTCE target through the cycle is 17% versus the 21% today. Is there anything you're seeing either in the macro environment or competitive environment that could accelerate a path to 17%? Or is that not anywhere on the horizon?

**James Dimon** (Executives):
We've always talked about 17% being through the cycle. I think times are pretty good now with high volumes and high asset prices and fairly low credit losses and all that. So if you can earn 17% consistently for a long period of time, that's a really good return for shareholders. That's our goal. And I don't want to change every time something happens in the marketplace. And so far, so good. And hopefully, we enjoy a good environment for a while. We just don't know when it's going to stop.

**Jeremy Barnum** (Executives):
And we don't want to be pointlessly negative, and I won't sort of bore you with the speech. But if you just look across the entire franchise, every single business is performing exceptionally well. The conditions have just been exceptionally favorable.

**James Dimon** (Executives):
It was every company.

**Jeremy Barnum** (Executives):
Yes. It's not just us. And so that hasn't historically been true. Historically, you've tended to see a bit more internal diversification in high rate environment, some businesses do better than others and vice versa. So the conditions that we've had recently where essentially every part of the franchise is beating records are not typical by historical standards.

**David Chiaverini** (Analysts):
Makes sense. And then shifting to credit quality. You addressed the consumer side. Could you talk about the corporate credit health? It looks like you built some reserves on the wholesale side. Curious on your comments there.

**Jeremy Barnum** (Executives):
Sure. Yes, the wholesale build is actually just from new activity. So it's not downgrades or change in the outlook or anything like that. So I would say that the corporate credit outlook is currently pretty stable. But obviously, there are issues out there, and we'll have to see how those flow through the performance of our borrowers, energy prices, fuel inputs, higher rates. These are all things that will create challenges in different pockets of the economy in the C&I space as well as the CRE space for that matter. So we'll see. But so far, I mean, it's very early, obviously. But in general, we think corporate balance sheets are in quite good shape. And so there's been resilience, but there are a lot of pressures building up. So we'll have to see what happens.

**Operator** (Operator):
Our final question comes from Kunpeng Ma from China Securities.

**Kunpeng Ma** (Analysts):
I have a question on the revenue of the market business because we've seen some volatilities in the market revenue across quarters. So I don't know whether we have a meaningful estimate of the -- through the quarter market business revenue. And also if you can provide us with some of your thoughts on the key business momentum supporting such kind of estimates, that will be very helpful.

**Jeremy Barnum** (Executives):
Yes. So I had trouble exactly following your question, but I think you're asking me for a fourth quarter outlook for the markets revenue. And so as you know, we don't actually guide to that. It's obviously very, very hard to predict and essentially a function of outside and forces. But just a reminder that you do tend to see significant seasonal decline between the third and the fourth quarter. And also a reminder that in recent years, we've had some slightly unusual seasonal patterns between the third and the fourth quarter. So our base case assumptions right now, all else being equal, are normal seasonal declines between the third and fourth quarter and make sure that you interpret normal with the right amount of historical context and all the usual caveats apply. We've seen a lot of volatility. There's a lot going on and anything can happen.

**James Dimon** (Executives):
I think the fourth quarter will have not the same seasonal decline first...

**Jeremy Barnum** (Executives):
Interesting.

**James Dimon** (Executives):
It's too much going on in the world.

**Operator** (Operator):
That's all the time we have for questions today.

**James Dimon** (Executives):
Thank you very much.

**Jeremy Barnum** (Executives):
Thank you very much. See you all next quarter.

**Operator** (Operator):
Thank you all for participating in today's conference. You may disconnect at this time, and have a great rest of your day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### JPM_Q2_2026_Earnings_Call_20260714.md
- 2026-07-14｜Jeremy Barnum｜guidance：全年 NII ex Markets 與總 NII 財測上調，Markets NII 升至約 90 億（原話："we now expect NII ex Markets to be about $96.5 billion"）
- 2026-07-14｜Jeremy Barnum｜guidance：全年調整後費用財測上調至約 1,075 億，主因與量及營收相關的費用（原話："the new adjusted expense outlook is about $107.5 billion"）
- 2026-07-14｜Jeremy Barnum｜guidance：卡片淨沖銷率財測調整為約 3.2%，理由是消費信用優於預期（原話："Card net charge-off rate to be approximately 3.2%"）
- 2026-07-14｜Jeremy Barnum｜guidance：NII ex Markets 上調的最大單一因素是存款餘額，利率只是小部分（原話："the biggest single factor is deposit balances"）
- 2026-07-14｜Jeremy Barnum｜guidance：消費端存款今年低個位數成長的預期不變（原話："we talked about expecting low single-digit growth this year"）
- 2026-07-14｜Jeremy Barnum｜margin：管理層拆解費用上調 25 億：15 億已在上半年入帳，另隱含下半年 10 億（原話："of the $2.5 billion that we increased guidance, $1.5 billion"）
- 2026-07-14｜Jeremy Barnum｜margin：上半年資本市場相關營收超出當初預期 65 億，並帶來 15 億額外費用（原話："outperformed our then expectations by $6.5 billion"）
- 2026-07-14｜Jeremy Barnum｜margin：Markets NII 上調來自資產負債表組成變化，非利率；另有約 1.5 億由股權配置從 Corporate 移到 CIB（原話："it's probably like $150 million"）
- 2026-07-14｜James Dimon｜margin：Dimon 說明營收增加時邊際報酬高於平均，營運槓桿觀點（原話："since you're not adding all the overhead"）
- 2026-07-14｜Jeremy Barnum｜margin：Barnum 說明 Q2 營收年增 15%、費用年增 15% 及淨沖銷/準備金數字（原話："Expenses of $27.3 billion were up 15% year-on-year"）
- 2026-07-14｜James Dimon｜margin：Dimon 認為 AI 效益會歸客戶而非銀行，不會讓利潤率無限上升（原話："If that were true, our margins would be 80% today"）
- 2026-07-14｜Jeremy Barnum｜margin：Barnum 提到存款 beta 優於模型，實際利率敏感度可能高於 EaR 顯示（原話："outperformance of the Consumer betas relative to the model"）
- 2026-07-14｜Jeremy Barnum｜margin：Token 費用上半年微不足道，預期下半年明顯加速，但全年仍屬微小（原話："it is a trivial number for the first half of the year"）
- 2026-07-14｜James Dimon｜commitment：Dimon 預期費用成長可能在 2027 或 2028 放緩，但表示無法預測（原話："maybe a slowdown in '27 or '28"）
- 2026-07-14｜James Dimon｜commitment：Smart Cash 工具仍屬測試，Dimon 承諾今年會看到動作（原話："Yes, you'll see something this year."）
- 2026-07-14｜James Dimon｜commitment：對支出的態度：持續投資、與前幾年一致，無改變（原話："a complete continuation of what we've been doing for years"）
- 2026-07-14｜Jeremy Barnum｜commitment：董事會將季度股利提高至每股 1.65 美元，第三季生效（原話："increase the quarterly dividend to $1.65 per share"）
- 2026-07-14｜James Dimon｜commitment：接班時程：Dimon 稱與上次所說相同，約幾年，由董事會決定（原話："Several years, you can use a few years"）
- 2026-07-14｜James Dimon｜capital_allocation：Dimon 更正上次提到的 200 億回購說法，並說可以多於此數或完全不做（原話："I made a mistake last time mentioning $20 billion."）
- 2026-07-14｜James Dimon｜capital_allocation：Dimon 表示股價越高越少買回；多餘資本傾向部署於有機成長（原話："we want to buy back less stock as the price goes up"）
- 2026-07-14｜James Dimon｜capital_allocation：資本部署目標為 17% 報酬（原話："the goal is to deploy our capital at a 17% return"）
- 2026-07-14｜Jeremy Barnum｜capital_allocation：CET1 比率 14.1%，較上季下降 20bp，RWA 增加約 1,030 億（原話："standardized CET1 ratio of 14.1%, down 20 basis points"）
- 2026-07-14｜Jeremy Barnum｜capital_allocation：CIB 資本配置是回應客戶需求，另有波動與股價上漲帶來的被動效應（原話："you've got active and passive effects"）
- 2026-07-14｜James Dimon｜capital_allocation：Dimon 表示對併購保持開放，並承認今年有些交易不特別好（原話："most were good, a couple weren't particularly good"）
- 2026-07-14｜James Dimon｜competition：Dimon 點名競爭對手包括 Goldman 與多家金融科技公司（原話："you've got Stripe and PayPal and Cash and Block and Chime"）
- 2026-07-14｜Jeremy Barnum｜competition：Barnum 指出 G-SIB 短期批發融資修改對同時有市場與消費業務的銀行負擔較重（原話："increase the burden on banks like us and Bank of America"）
- 2026-07-14｜James Dimon｜competition：Dimon 認為 AI 也會經由 Fiserv、FIS 等提供給較小的競爭者（原話："this will be offered to smaller competitors, too"）
- 2026-07-14｜Jeremy Barnum｜competition：Barnum 說同業資料中心放款有放寬，JPM 婉拒部分交易，整體屬正常競爭壓力（原話："we passed on some deals"）
- 2026-07-14｜Jeremy Barnum｜product：投行費用年增 30%，股權承銷特別強，部分來自大型 ECM 案與併購提前完成（原話："IB fees were up 30% year-on-year"）
- 2026-07-14｜Jeremy Barnum｜product：股票業務營收年增 86%（原話："revenue up 86% year-on-year"）
- 2026-07-14｜James Dimon｜product：Chase UK 約 250–300 萬客戶，德國已開業但尚未獲利（原話："it's not quite profitable yet"）
- 2026-07-14｜James Dimon｜product：Dimon 描述 AI 使用案例數與其對效率的預期（原話："almost 1,000 use cases today"）
- 2026-07-14｜Jeremy Barnum｜product：AWM 長期淨流入 500 億，AUM 5.1 兆（原話："Long-term net inflows were $50 billion"）
- 2026-07-14｜James Dimon｜risk：Dimon 回答是否已是高點：接近最佳但不知道能維持多久（原話："It's getting close to as good as it gets."）
- 2026-07-14｜Jeremy Barnum｜risk：Barnum 說股票業務本季特殊組合難以重複（原話："a little bit hard to imagine that being repeated"）
- 2026-07-14｜Jeremy Barnum｜risk：投行本季有提前與大型交易貢獻，管理層承認有 pull-forward 但管線仍強（原話："clearly, there was some pull-forward"）
- 2026-07-14｜James Dimon｜risk：Dimon 指出同業承銷標準出現輕微弱化（PIK、契約、展期風險）（原話："you've seen a little bit of weakness"）
- 2026-07-14｜Jeremy Barnum｜risk：Barnum 指出存款利率支付的負凸性遲早會出現，高利率情境並非單純有利（原話："you have to believe that at some point, that kicks in"）
- 2026-07-14｜Jeremy Barnum｜risk：對消費者：K 型敘事支持不多，但有實質薪資為負的族群值得觀察，信用主要看勞動市場（原話："it's just about the labor market"）
- 2026-07-14｜James Dimon｜risk：Dimon 批評監管資本計算有重複計算，列出四項應修改處（原話："get rid of the double count in operating risk capital"）
- 2026-07-14｜Jeremy Barnum｜customer：消費者與小企業展現韌性，支出強勁，淨新增支票帳戶逾 50 萬（原話："net new checking account growth of over 500,000 accounts"）
- 2026-07-14｜Jeremy Barnum｜customer：批發存款上半年優於預期，部分來自 NBFI 與資料中心放款創造存款（原話："loans creating deposits"）
- 2026-07-14｜Jeremy Barnum｜customer：管理層對 CapEx 與放款成長是否與 AI 相關無法明確區分（原話："might still be, but on the other hand, it might not"）
- 2026-07-14｜Jeremy Barnum｜customer：消費端 15% 零售份額被描述為策略執行的結果而非目標改變（原話："the 15% will be an outcome of that"）

### 問答異常語氣（迴避／改口／保留）
- JPM_Q2_2026_Earnings_Call_20260714.md｜問：Usdin/Penala：領導層異動（Marianne Lake 退休、兩位共同總裁）與 Dimon 任期、接班特徵｜答法：Dimon 回「No mystery」「timing is essentially the same」，被追問時只說「幾年、plus or minus、由董事會決定」，未給明確時間
- JPM_Q2_2026_Earnings_Call_20260714.md｜問：Mitchell：未來幾年費用成長是否放緩、營運槓桿是否可能為正｜答法：Dimon 稱追求更高營運槓桿是「crazy notion」，只說「we can't project」並提 27/28 年可能放緩；Barnum 轉談邊際營運槓桿
- JPM_Q2_2026_Earnings_Call_20260714.md｜問：Poonawala：為何在 3 倍帳面價值時仍回購、是否多留資本｜答法：Dimon 同意原則，但稱不會告訴市場要做什麼（'not going to tell you what they are'），並更正上次 200 億說法，不給數字
- JPM_Q2_2026_Earnings_Call_20260714.md｜問：Gosalia：CIB 資本配置是否已達高點、是否有內部上限｜答法：Barnum 明說不討論內部限額管理，改談客戶需求與主被動效應，未回答是否已到高點
- JPM_Q2_2026_Earnings_Call_20260714.md｜問：Usdin：投行與市場業績可持續性｜答法：Barnum 表示「don't want to get into guiding」，稱只是猜測，承認有 pull-forward 但稱管線強健

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

## ⑥ 條件附卡（archetype_hint='金融' 命中）：judge_addendum_archetype.md

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
{"status":"no_prior_dd"}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JPM_20261019/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
