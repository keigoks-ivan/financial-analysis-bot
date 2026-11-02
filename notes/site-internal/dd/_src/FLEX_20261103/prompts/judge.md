你是 stock-analyst **v20 判斷 agent**，標的 FLEX（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"FLEX","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":8491,"period":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿（Exhibit 99.1，investors.flex.com 託管）https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf"},"note":"consensus 約 $8.18B（單一聚合頁、無日期，僅供參考；來源：web_search）"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":7.1,"period":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿（Exhibit 99.1，investors.flex.com 託管）https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf"},"note":"未取得可靠共識值"},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":4.9,"period":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿（Exhibit 99.1，investors.flex.com 託管）https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf"},"note":"未取得"},{"id":"f_kpi3_non_gaap_eps_adjusted","label":"Non-GAAP EPS (adjusted)","value":1.18,"period":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿（Exhibit 99.1，investors.flex.com 託管）https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf"},"note":"Zacks consensus $1.05（來源：web_search，Zacks 報導）；GAAP EPS $0.70"},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow","value":261,"period":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿（Exhibit 99.1，investors.flex.com 託管）https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf"},"note":"未取得"},{"id":"f_kpi6_q3_fy2027_guidance","label":"Q3 FY2027 guidance","value":"Net sales $8.87–9.17B；adj. operating income $685–715M；adj. EPS $1.19–1.25","period":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","unit":"mixed","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿（Exhibit 99.1，investors.flex.com 託管）https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf"},"note":"未取得"},{"id":"f_kpi7_fy2027_guidance","label":"FY2027 guidance（更新）","value":"Net sales $34.9–35.9B；adj. operating margin 7.6–7.8%；adj. EPS $4.84–5.16","period":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","unit":"mixed","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿（Exhibit 99.1，investors.flex.com 託管）https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf；不含計畫中的 CPI 分拆"},"note":"consensus FY1 EPS 5.07（來源：consensus_revision）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_flex_gross_margin_pct","label":"FLEX 毛利率","value":9.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_operating_margin_pct","label":"FLEX 營業利益率","value":5.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_flex_fcf_margin_pct","label":"FLEX FCF 利潤率","value":3.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cls_gross_margin_pct","label":"CLS 毛利率","value":11.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cls_operating_margin_pct","label":"CLS 營業利益率","value":8.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cls_fcf_margin_pct","label":"CLS FCF 利潤率","value":2.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_jbl_gross_margin_pct","label":"JBL 毛利率","value":9.23,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_jbl_operating_margin_pct","label":"JBL 營業利益率","value":5.11,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_jbl_fcf_margin_pct","label":"JBL FCF 利潤率","value":3.82,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_sanm_gross_margin_pct","label":"SANM 毛利率","value":9.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_operating_margin_pct","label":"SANM 營業利益率","value":5.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sanm_fcf_margin_pct","label":"SANM FCF 利潤率","value":4.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2317_tw_gross_margin_pct","label":"2317.TW 毛利率","value":6.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2317_tw_operating_margin_pct","label":"2317.TW 營業利益率","value":3.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2317_tw_fcf_margin_pct","label":"2317.TW FCF 利潤率","value":-0.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_gaap","label":"SBC 占非 GAAP 營業利益","value":7.1,"period":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2027（季末 2026-09-25，公告於 2026-10-28）","citation":"公司 IR 新聞稿（Exhibit 99.1，investors.flex.com 託管）https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf（SBC $43M ÷ 非 GAAP 營業利益 $607M；占營收 0.51%）"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":87.03,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-5.24,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":39.88,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.6,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.04 → 5.07）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.42,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.72 → 7.83）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.22 → 10.22）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.07,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":7.83,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.22,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":9.74,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 4.62 → 5.07（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":31.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.04,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.13,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":17.16,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 5.07，分子＝快照價 87.03","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":2900.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 5983.0、現金 3083.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":369.46,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":35052.33,"period":"2026-11-03","unit":"USD m","basis":"市值 32152.33 ＋ 淨負債 2900.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":35484.95,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":46370.83,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（9 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.99,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 86.25 / W52 95.07 / W104 70.07 / W250 41.09 / W250 13週斜率 2.87%"},{"id":"f_ma_w52","label":"52 週均線","value":95.07,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":70.07,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":41.09,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.87,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：Flex 與全球 EMS、區域/專項小型 EMS 及 ODM 競爭，亦與現有及潛在客戶競爭；過去曾有客戶把部分製造移回自有產能，未來客戶可能自製、雙供應商、區域化或重分配量；部分競爭者成本結構較低或資源更大。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"In the past, some of our customers moved a portion of their manufacturing away from us in order to more fully utilize their excess internal manufacturing capacity, and customers could in the future decide to in-source, dual‑source, regionalize, or otherwise reallocate manufacturing volumes among suppliers.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K：前十大客戶占淨銷售 FY2026 45%、FY2025 44%、FY2024 37%；無單一客戶超過 10%。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"Our ten largest customers accounted for 45%, 44% and 37% of net sales in fiscal years 2026, 2025 and 2024, respectively. No customer accounted for more than 10% of net sales in fiscal year 2026, 2025 or 2024.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"CSIMarket 估計 Flex 在其同業集合內 2026 Q1 份額下滑（營收仍成長）","source":"CSIMarket FLEX Competitors","url":"https://csimarket.com/stocks/FLEX-Competitors","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2026 10-K：無單一客戶超過 10% 淨銷售，前十大客戶占 45%（FY2025 44%、FY2024 37%）。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"In fiscal year 2026, our ten largest customers accounted for 45% of net sales. No customer accounted for greater than 10% of the Company's net sales in fiscal year 2026.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因子：部分超大規模客戶已發展或可能發展內部設計/工程/製造能力與 Flex 競爭，垂直整合、in-source 或轉單競爭者可能重大不利影響；Cloud 與 Power 業務集中度尤高。屬風險揭露，未點名具體客戶已自製。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"certain hyperscale customers have developed, or may develop, internal design, engineering, or manufacturing capabilities that compete with our offerings. These customers may choose to reduce their reliance on third-party providers like us over time, which could result in reduced order volumes, loss of programs, or increased pricing pressure.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 前十大客戶占淨銷售 45%（FY2025 44%、FY2024 37%），無單一客戶超過 10%；Cloud 與 Power Infrastructure 集中度尤高，由少數超大規模雲端業者主導，且可能自製或轉單。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"Our ten largest customers accounted for 45%, 44% and 37% of net sales in fiscal years 2026, 2025 and 2024, respectively. No customer accounted for more than 10% of net sales in fiscal year 2026, 2025 or 2024.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"截至 2026-03-31，單一客戶占應收帳款淨額 16%，幾乎全在 CPI 部門；前兩年無客戶超過 10%。","source":"SEC EDGAR 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"A single customer accounted for 16% of the Company's total balance of accounts receivable, net as of fiscal year ended March 31, 2026, which is almost entirely within the CPI segment.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"S&P 2024-11 對 Flex 評級報告，列失去關鍵客戶為可能降評因素之一","source":"S&P Global Ratings Nov 2024","url":"https://s202.q4cdn.com/732614612/files/doc_downloads/2024/11/06/Flex-Ltd-S-P-Global-Ratings-Nov-2024.pdf","excerpt":null,"as_of":"2024-11-06","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Flex 預期 FY26 資料中心營收約 65 億美元、年增至少 35%、占總營收約 25%；資料中心不是獨立申報部門，全年指引只在年初給、年底更新","source":"Nasdaq/Zacks: How is Flex Accelerating Its Expansion in the Data Center Market?; Seeking Alpha: Flex signals at least 35% data center revenue growth for FY26","url":"https://www.nasdaq.com/articles/how-flex-accelerating-its-expansion-data-center-market","excerpt":"The company is on track to generate roughly $6.5 billion in data center revenue this year, representing at least 35% year-over-year growth and accounting for 25% of its total revenues.","as_of":"2026-02-04","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Flex 同期消費相關終端市場疲弱，部分抵銷資料中心成長","source":"Flex 財報摘要（搜尋結果彙整，Q2/Q3 FY26）","url":"https://www.fool.com/earnings/call-transcripts/2026/02/04/flex-flex-q3-2026-earnings-call-transcript/","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q4 2026 零組件市場分析稱產業呈結構性分化而非 2021 式全面缺料；另有來源稱 2026 缺料為選擇性、特定 SKU，記憶體（AI 驅動）最可能延續到 2027 以後，被動元件交期拉長到 26–40 週","source":"Utmel: 2026 Q4 Electronic Components Market Analysis Report","url":"https://www.utmel.com/blog/categories/semiconductor/2026-q4-electronic-components-market-analysis-report-supply-pricing-and-procurement-outlook","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Benchmark 稱近期不需新增大型廠房，僅擴建現有廠址（EMS 同業產能紀律訊號；日期不明）","source":"Circuits Assembly: No expansion plans for Benchmark","url":"https://circuitsassembly.com/ca/editorial/menu-news/18525-no-expansion-plans-for-benchmark.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K 風險因子僅以一般性語言提及可能面臨含反壟斷在內的訴訟、調查與監管程序；未點名任何具體反壟斷調查或拆分命令。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"We are, from time to time, subject to claims, lawsuits, investigations, and regulatory or administrative proceedings across the jurisdictions where we operate. These matters may involve commercial disputes, regulatory compliance, intellectual property, antitrust, product liability, employment and labor, privacy and data protection, securities laws, governance, and tax.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2026（截至2026-03-31）關稅成本支付與客戶回收使營收與銷貨成本約變動1%，對獲利影響可忽略；公司以轉嫁給客戶為原則。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"During the fiscal year ended March 31, 2026, tariff costs paid and recoveries from our customers impacted our revenues and costs of goods by approximately one percent and had a negligible impact on our profitability.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"最高法院2026-02-20推翻IEEPA關稅，美國政府2026-04-20開放退稅機制；公司考慮申請退稅，預期不具重大影響。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"On February 20, 2026, the U.S. Supreme Court struck down tariffs imposed under the International Emergency Economic Powers Act (\"IEEPA\") and on April 20, 2026 the U.S. government opened a system to facilitate refunds for IEEPA tariffs paid.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"風險因子：公司因關稅與貿易行動在成本回收時點與營運複雜度上持續受影響。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"As a global manufacturing and supply chain services partner with operations, suppliers, and customers across multiple jurisdictions, we have been, and expect to continue to be, impacted by tariffs and trade actions through the timing and mechanics of cost recovery and operational complexity.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"公司在中國有重大營運，受中國相關法規與地緣政治發展影響。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"We have significant operations in China, which have been, and could continue to be, affected by evolving laws, regulations, and geopolitical developments involving China.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"USMCA於2026年進行聯合檢討，公司揭露協定可能被修改、暫停或終止的風險。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"The USMCA is subject to a joint review process in 2026, and there can be no assurance 25 Table of Contents that the agreement will not be amended, suspended, or terminated","as_of":"2026-05-20","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2026 10-K：Flex 產地以墨西哥最大（約 25% 淨銷售、$6,994M），美國 19%、中國 16%、馬來西亞 11%；墨西哥也占最大比重淨固定資產（36%，中國 12%）","source":"Flex Ltd Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000866374/000086637426000012/flex-20260331.htm","excerpt":"Mexico $6,994 25%","as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K：部分零組件來自少數供應商、有時僅單一供應商，監管、地緣與貿易限制事件可能中斷供應鏈","source":"Flex Ltd Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000866374/000086637426000012/flex-20260331.htm","excerpt":"Certain components that we use are sourced from a limited number of suppliers, and in some cases from a single supplier, which increases the risk that regulatory actions, geopolitical developments, trade restrictions or other events affecting those suppliers could disrupt our supply chain.","as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K：客戶指定供應商可能是單一來源或地理集中，Flex 合格化替代來源與轉嫁成本的能力有限","source":"Flex Ltd Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000866374/000086637426000012/flex-20260331.htm","excerpt":"Customers may direct or require purchases from specified suppliers, and these may be sole sources or geographically concentrated.","as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K：烏克蘭、中東衝突、荷莫茲海峽與紅海航運受攻擊已造成運輸延誤與成本上升","source":"Flex Ltd Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000866374/000086637426000012/flex-20260331.htm","excerpt":"Problems suffered by any of these common carriers, whether due to geopolitical issues, such as conflicts in Ukraine and the Middle East, disruptions in the Strait of Hormuz and the Red Sea, including as a result of attacks on shipping vessels have resulted in shipping delays and higher costs.","as_of":"2026-03-31","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Flex FQ2 FY2027 營收 $8.5B、年增 25%；CPI 段 +54% 至 $2.5B（電力、雲與散熱需求）；RMS +9% 至 $2.7B（工業需求）；CPI 預計於 2027 年初分拆為 Axiom（待核准）","source":"Flex Q2 FY2027 results / MarketBeat 法說摘要（2026-10-28）","url":"https://www.marketbeat.com/instant-alerts/transcript-flex-q2-earnings-call-highlights-2026-10-28/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Flex 將 FY2027 營收指引上調至 $34.9B–$35.9B（中點年增約 27%）；FQ3 指引 $8.87B–$9.17B（中點年增約 28%）","source":"Zacks: Flex Q2 earnings beat estimates on CPI strength, outlook raised","url":"https://www.zacks.com/stock/news/3017125/flex-q2-earnings-beat-estimates-on-cpi-strength-outlook-raised","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"FQ1 FY2027 ITS 段營收 $3.1B、年增 20%，由通訊帶動，消費相關市場疲弱部分抵銷","source":"MarketBeat: Flex Q1 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/flex-q1-earnings-call-highlights-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"全球 EMS 市場 2026 年規模約 $680–690B，多家機構預估 CAGR 約 6.1%–6.8%（定義不同，區間 4.3%–7.6%）","source":"Fortune Business Insights / Persistence Market Research EMS 市場報告","url":"https://www.persistencemarketresearch.com/market-research/electronics-manufacturing-services-market.asp","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Flex FQ2 FY2027 新聞稿：各段營收與成長","source":"Flex PR 27Q2","url":"https://s202.q4cdn.com/732614612/files/doc_earnings/2027/q2/earnings-result/FLEX_PR_27Q2.pdf","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Flex 10-K risk factor: new technologies, standards or customer requirements may render existing power delivery systems, cooling solutions, integration capabilities, inventory or manufacturing processes less competitive or obsolete; failure to keep pace could cause inventory write-downs.","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"The emergence of new technologies, industry standards, or customer requirements may render our existing power delivery systems, cooling solutions, integration capabilities, inventory, or manufacturing processes less competitive or obsolete.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Flex agreed to acquire EPC Power (~$4.4B) to address the shift to 800V DC architecture and solid-state transformers (SST roadmap), indicating Flex is itself positioning on the replacement technology; search summary noted no analyst threat commentary found.","source":"Data Center Knowledge: Flex Pays $4.4B for EPC Power as AI Data Centers Push 800V Architecture","url":"https://datacenterknowledge.com/energy-power-supply/flex-pays-4-4b-for-epc-power-as-ai-data-centers-push-800v-architecture","excerpt":null,"as_of":"2026-09-03","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K 描述 Flex 提供增值履約與正向物流，服務企業、零售、D2C 與市集通路；為既有服務敘述，未見通路結構性轉變的揭露","source":"SEC EDGAR 10-K FY2026 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"We provide extensive value-added fulfillment and logistics capabilities to reduce lead times while serving the needs of enterprise, retail, direct-to-consumer, and marketplace channels globally.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"搜尋未找到 Flex 2026 年銷售通路／分銷層面的結構性變化報導；第三方摘要僅描述商業模式由傳統代工朝資料中心電力與 AI 基礎設施（EMS+Products+Services）移動，屬產品組合轉移而非通路轉移","source":"Nasdaq/Zacks 'How is Flex Accelerating Its Expansion in the Data Center Market?'","url":"https://www.nasdaq.com/articles/how-flex-accelerating-its-expansion-data-center-market","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Flex 2026-07-29 給 FY2027 EPS 指引 4.42–4.74、Q2 FY27 EPS 1.00–1.07，共識 0.98","source":"MarketBeat: Flex issues Q2 2027 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/flex-nasdaqflex-issues-q2-2027-earnings-guidance-2026-07-29/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"聚合站顯示 FLEX 平均目標價 $170.70、中位數 $170、區間 $150–$203（10 位分析師，2026-07）","source":"Walnut: Flex Ltd (FLEX) Stock Forecast and Price Target (2026)","url":"https://walnutinvest.com/stocks/flex/forecast","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Investing.com 共識目標價約 $160.50，11 買進 0 持有；JPMorgan 2026-07-30 維持 Buy、目標 160","source":"Investing.com Flex consensus estimates","url":"https://www.investing.com/equities/flextronics-intl-ltd-consensus-estimates","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-02-04 Flex 上調 FY2026 調整後 EPS 指引由 3.09–3.17 至 3.21–3.27，高於分析師 3.15","source":"daytraders.com: Flex raises outlook after record quarter","url":"https://daytraders.com/news/2026/02/04/flex-raises-outlook-after-record-quarter-fueled-by-ai-data-centers","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Flex 於 2026-09-03 簽約、2026-10-14 完成收購 EPC Power Corp. 全部股權（Item 2.01）","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/866374/000119312526421058/d147467d8k.htm","excerpt":"On October 14, 2026, the Company completed the Transaction.","as_of":"2026-10-14","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Flex 計畫 2027 年第一季將 Cloud and Power Infrastructure 事業分拆為獨立上市公司 Axiom Solutions International","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/866374/000119312526413173/d123485d8k.htm","excerpt":"intends to separate its Cloud and Power Infrastructure business into an independent publicly traded company, Axiom Solutions International, Inc., a Texas corporation and currently a wholly owned subsidiary of Flex (the “Spin-Off”), in the first quarter of 2027","as_of":"2026-10-05","retrieved_at":"20261103","affects":["valuation","thesis.H","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026-09-29 簽訂 33 億美元 364 天優先定期貸款信用額度（Citibank 為行政代理），尚未動用","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/866374/000110465926113282/tm2626870d1_8k.htm","excerpt":"provides a senior term loan credit facility (the “Credit Facility”) in an aggregate committed amount of $3.3 billion. The Credit Facility was not drawn on the Closing Date.","as_of":"2026-10-02","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"10-K 風險因素僅概述性提及訴訟與調查，未見具名重大訴訟；Item 3 擷取僅有標題","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"We are, from time to time, subject to claims, lawsuits, investigations, and regulatory or administrative proceedings across the jurisdictions where we operate.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ems_utilization_capex_cycle#0","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"0","claim":"Q2 FY2026 財報摘要：Flex 預期未來 2–5 年為資料中心成長進行 meaningful capex；新產能含 Dallas、Fontana、Colombia 擴建與 Poland 廠（歐洲電源產能倍增）","source":"Fintool Flex Q2 2026 earnings summary","url":"https://fintool.com/app/research/companies/FLEX/earnings/Q2 2026","excerpt":null,"as_of":"2025-11-06","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"ems_utilization_capex_cycle#1","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"-","claim":"Barchart 報導 Flex FY2027 capex 目標中點約 $1.5B，全數由內部現金流支應","source":"Barchart: dear flex stock fans mark your calendars for june 22","url":"https://www.barchart.com/story/news/2408974/dear-flex-stock-fans-mark-your-calendars-for-june-22","excerpt":null,"as_of":"2026-06-15","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"ems_utilization_capex_cycle#2","axis":"ems_utilization_capex_cycle","section":"coverage","direction":"+","claim":"Lincoln International 2026 Q2 EMS 季報：資料中心/AI、關鍵電力等領域支撐高可靠度業者稼動率；客戶組合、執行與稼動率比規模更決定獲利","source":"Lincoln International 2026 Q2 EMS Quarterly Review","url":"https://www.lincolninternational.com/wp-content/uploads/2026-Q2_EMS-Quarterly-Review_vF.pdf","excerpt":"Data center and AI-related infrastructure, critical power, aerospace & defense and other mission-critical programs remained key areas of strength, supporting utilization and mix for providers with","as_of":"2026-07-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#0","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"opencapital.sh 聚合站 Q1 2026 ROIC：Flex 19.2%（年增自 13.9%）、Jabil 29.8%、Celestica 39.5%、Sanmina 11.3%；Flex 在四家中排第三","source":"opencapital.sh Flex/Sanmina ROIC metrics pages","url":"https://www.opencapital.sh/stocks/flex/metrics/roic","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#1","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"-","claim":"opencapital.sh Q1 2026 資產週轉：Flex 1.4x、Jabil 1.6x、Celestica 2.0x、Sanmina 約 1.5x（另站 peer panel）；Flex 四家中最低。聚合站定義未對齊，Flex 頁另有 6.3x→5.5x 多年數字與 1.4x 矛盾，未對 10-K 核實","source":"opencapital.sh asset_turnover pages (flex/jbl/cls)","url":"https://www.opencapital.sh/stocks/flex/metrics/asset_turnover","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"ems_roic_asset_turnover_benchmark#2","axis":"ems_roic_asset_turnover_benchmark","section":"coverage","direction":"0","claim":"GuruFocus：Flex 2026 年 3 月季度現金轉換週期 30.80 天（DSO 51.97、DIO 76.73、DPO 97.9）；FY2026 CCC 38.13 天；TipRanks 至 2025-12 TTM CCC 56.39 天，來源間差異大","source":"GuruFocus Flex Cash Conversion Cycle","url":"https://www.gurufocus.com/term/cash-conversion-cycle/ FLEX","excerpt":"The Cash Conversion Cycle for the quarter that ended in Mar. 2026 is calculated as: 51.97+76.73-97.9 = 30.80.","as_of":"2026-03-31","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-14 完成收購 EPC Power","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/866374/000119312526421058/d147467d8k.htm","excerpt":"On October 14, 2026, the Company completed the Transaction.","as_of":"2026-10-14","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"計畫 2027Q1 分拆 Cloud and Power Infrastructure 為 Axiom","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/866374/000119312526413173/d123485d8k.htm","excerpt":"intends to separate its Cloud and Power Infrastructure business into an independent publicly traded company, Axiom Solutions International, Inc.","as_of":"2026-10-05","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K FY2026 風險因素僅一般性提及訴訟；搜尋僅見 2018 年證券集體訴訟（已於 2021-12 第九巡迴上訴法院維持駁回），近12個月未見新案","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/866374/000086637426000012/flex-20260331.htm","excerpt":"We are, from time to time, subject to claims, lawsuits, investigations, and regulatory or administrative proceedings across the jurisdictions where we operate.","as_of":"2026-05-20","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"FLEX","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.5,"operating_margin_pct":5.44,"fcf_margin_pct":3.32,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FLEX","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CLS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":11.46,"operating_margin_pct":8.29,"fcf_margin_pct":2.99,"rd_intensity_pct":0.93},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CLS","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"JBL","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.23,"operating_margin_pct":5.11,"fcf_margin_pct":3.82,"rd_intensity_pct":0.08},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JBL","as_of":"TTM ending 2026-08-31（4季加總）"}},{"name":"SANM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":9.01,"operating_margin_pct":5.49,"fcf_margin_pct":4.66,"rd_intensity_pct":0.26},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SANM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2317.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.12,"operating_margin_pct":3.51,"fcf_margin_pct":-0.46,"rd_intensity_pct":1.31},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2317.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"FLEX"},"financial_history":{"ticker":"FLEX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-03-31","revenue":28502000000.0,"revenue_yoy_pct":null,"gross_margin_pct":6.93,"operating_margin_pct":3.58,"net_income":793000000.0,"diluted_eps":1.72,"free_cash_flow":315000000.0,"fcf_margin_pct":1.11,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-03-31","revenue":26415000000.0,"revenue_yoy_pct":-7.32,"gross_margin_pct":7.06,"operating_margin_pct":3.3,"net_income":1006000000.0,"diluted_eps":2.28,"free_cash_flow":796000000.0,"fcf_margin_pct":3.01,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-03-31","revenue":25813000000.0,"revenue_yoy_pct":-2.28,"gross_margin_pct":8.36,"operating_margin_pct":4.59,"net_income":838000000.0,"diluted_eps":2.11,"free_cash_flow":1067000000.0,"fcf_margin_pct":4.13,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-03-31","revenue":27914000000.0,"revenue_yoy_pct":8.14,"gross_margin_pct":9.2,"operating_margin_pct":5.18,"net_income":880000000.0,"diluted_eps":2.33,"free_cash_flow":1052000000.0,"fcf_margin_pct":3.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/FLEX/FLEX_Q2_2027_Earnings_Call_20261028.md）

# Q2 2027 Earnings Call
**Flex Ltd.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Greetings, and welcome to Flex's Second Quarter Fiscal Year 2027 Earnings Conference Call. [Operator Instructions] As a reminder, this conference is being recorded. [Operator Instructions] It's now my pleasure to turn the call over to Michelle Simmons, Senior Vice President, Global Investor Relations and Public Relations. Michelle, please go ahead.

**Michelle Simmons** (Executives):
Good morning, and thank you for joining us today for Flex's Second Quarter Fiscal 2027 Earnings Conference Call. With me today is Revathi Advaithi, our Chief Executive Officer; Kevin Krumm, our Chief Financial Officer; Michael Hartung, our Chief Commercial Officer; and Amy Schwetz, who we previously announced as the expected CFO of Flex post-spin. We'll give brief remarks followed by Q&A.
Slides for today's call, as well as a copy of the earnings press release, are available on the Investor Relations section at flex.com. This call is being recorded and will be available for a replay on our corporate website. Today's call contains forward-looking statements, which are based on our current expectations and assumptions. These statements involve risks and uncertainties that could cause actual results to differ materially. These statements reflect expected results for the full fiscal year and do not give effect to the planned spin-off of the Cloud and Power Infrastructure segment. 
Any references to the planned spin-off, including its timing, Form 10 status and the leadership of each company following the separation, are forward-looking and remain subject to applicable approvals and completion of the spin-off. For a full discussion of these risks and uncertainties, please see the cautionary statements in our presentation, press release or in the Risk Factors section in our most recent filings with the SEC. Note, this information is subject to change, and we undertake no obligation to update these forward-looking statements. 
Please note, all growth metrics will be on a year-over-year basis, unless stated otherwise. Additionally, all results will be on a non-GAAP basis, unless we specifically state it's a GAAP result. The full non-GAAP to GAAP reconciliations can be found in the appendix slides of today's presentation as well as in the summary financials posted on the Investor Relations website. Now I'd like to turn the call over to our CEO. Revathi?

**Revathi Advaithi** (Executives):
Thank you, Michelle. Good morning, and thank you for joining us to discuss Flex's second quarter fiscal 2027 results. Before I begin, I'd like to start by welcoming Amy Schwetz to the team, who will become the Chief Financial Officer of Flex after the spin-off. I look forward to working with both her and Michael Hartung, who will lead Flex as CEO through this transition and to seeing Flex continue to excel under their leadership. 
Now I'll start with our performance for the quarter. We delivered another fantastic quarter in Q2. Revenue growth accelerated. We expanded margin across all 3 segments, and earnings reached a new record of $1.18 per share. Our results reflect continued execution across the portfolio and demonstrate the strength of our strategy, our diversified end markets and our ability to help customers navigate an increasingly dynamic environment. At the same time, we continue to make significant progress on one of the most important milestones in our company history, the planned spin-off of our Cloud and Power Infrastructure segment, now known as Axiom. 
Since our last earnings call, we have reached several important milestones as we've moved from announcing the transaction to building 2 focused industry-leading companies. Last month, Axiom filed a Form 10 registration statement, providing a more detailed view of Axiom's strategy, financial profile, leadership team and growth opportunities. That filing marked an important step forward and reflects the tireless work our teams have been doing behind the scenes to prepare for the separation. We also announced the expected leadership teams for both Flex and Axiom. 
One of the things that gives me great confidence in this next chapter is the strength of our leadership bench. Across both organizations, we have experienced leaders with deep expertise in technology, in manufacturing, operations, customer engagement and innovation who are ready to lead from day 1. Perhaps most exciting for me, we officially unveiled the Axiom name and brand. Building a new company is a rare opportunity. Over the past several months, we have spent a great deal of time defining not only what Axiom will do, but what it will stand for. For me personally, the name reveal was a meaningful milestone because it made something we've been building become more tangible.
Axiom is no longer just an idea. It's taking shape as a company with its own identity, leadership team, culture and purpose. It has been incredibly rewarding to share that vision with employees, customers, partners and our investors. As we've discussed before, we believe Axiom is uniquely positioned to lead the next generation of critical digital and electrical infrastructure. By bringing together power, thermal management and compute expertise, Axiom helps customers deploy increasingly complex infrastructure with greater speed and scale as AI demands more of the physical infrastructure behind it. 
The future of AI infrastructure goes beyond the chip itself. It depends on power, cooling, compute and the ability to deploy and operate infrastructure at scale. Those are the capabilities we've spent years building and honing, and they're the reason we believe the company is uniquely positioned for the opportunities ahead. We have outlined our strategy for Axiom, and we are working diligently through the spin-off to position the company for further success. Earlier this month, we announced the closing of our acquisition of EPC Power, which further strengthens Axiom's portfolio of end-to-end solutions, and EPC's engineering expertise complements our existing research and development into 800-volt architecture and solid-state transformers, technologies that will define the next-generation data center. 
The success of this strategy is evident in the results we are producing even before the spin. Our CPI segment grew 54% year-over-year in Q2 and delivered margin expansion of over 200 basis points. At OCP, earlier this month, we introduced prefabricated AI Modules, which help accelerate AI factory deployment by up to 50%. The work we're doing leading up to the spin is building upon the strength of what is already an incredibly successful business. The spin is about creating 2 stronger companies with distinct identities, focused strategies and ability to pursue their respective opportunities. 
While Axiom will be purpose-built to help power the AI infrastructure revolution, Flex will emerge as a more focused industrial technology, manufacturing and supply chain leader. I'm extremely excited about what Flex will become after the spin. Flex enters this next chapter from a position of strength with leadership position in attractive end markets and a proven track record of profitable growth and cash generation. In Q2, our RMS and ITS segments together grew 16%, representing the fourth consecutive quarter of year-over-year growth. 
Over the last several years, we have transformed Flex into a stronger, more focused company with higher margin, improved returns and a more attractive portfolio. Under Michael's leadership, Flex will build on that transformation. The company will be focused on markets where its engineering, vertically integrated manufacturing and supply chain capabilities create meaningful competitive advantage and long-term value for customers. As a stand-alone company, Flex will have greater ability to continue evolving its portfolio and allocating capital towards its highest return opportunities. Many of the markets where Flex has been investing and building leadership position over time sit at the intersection of long-term technology and industrial trends, including health care, energy infrastructure and communication. 
We believe these are attractive markets where complexity, reliability and speed matter, and where our capabilities can continue to drive differentiated growth and returns over time. These businesses are supported by durable, secular growth drivers, strong customer relationships and capabilities that are difficult to replicate. Combined with our financial discipline, our cash generation ability, productivity culture and commitment to shareholder returns, we believe Flex is exceptionally well positioned for its next chapter. At Innovation Day, you will directly hear from the Flex leadership team where they will take Flex from here. 
What excites me most is that we're not creating 2 companies searching for their future. We are creating 2 industry leaders, each with clear purpose, differentiated capabilities and substantial opportunities to create value. As we look ahead, I believe both companies are entering some of the most exciting periods in their history. And we're looking forward to sharing much more on November 10 at our Innovation Day, where investors will hear directly from the expected leadership teams of both Flex and Axiom, and we'll provide a deeper look at the strategies, the market opportunities and long-term plans that will guide both companies going forward, including how each intends to strengthen its competitive position and create long-term shareholder value. 
Most importantly, we'll show why we believe both companies are built to win, built with clear purpose, built with the right capabilities and leadership, and built to create long-term value for customers, employees and shareholders. With that, I'll turn the call over to Kevin, who will walk through the financials in more detail.

**Kevin Krumm** (Executives):
Thank you, Revathi, and good morning, everyone. Before I go through the quarter, I'd also like to welcome Amy Schwetz to the team. I'm confident in her leadership and her impact, and I'm excited to be working with her through the remainder of the spin-off process. I'll now review our results for the second quarter of fiscal year '27. We are continuing to execute well. We've got a great group of businesses and a great team, and all are performing at a high level as we approach the spin-off in early 2027. 
I'll start with our key financials on Slide 8. Second quarter revenue came in at $8.5 billion, up 25% versus the prior year. Adjusted gross profit totaled $842 million, and adjusted gross margin improved to 9.9%, up 60 basis points year-over-year. Adjusted operating profit was $607 million, up 48% from the prior year, with adjusted operating margins at 7.1%, up 110 basis points year-over-year, driven by continued productivity improvements as well as business mix. Finally, adjusted earnings per share for the quarter increased to $1.18 per share, up 49% versus the prior year. 
Turning to our quarterly segment results on the next slide. Regulated Manufacturing Solutions revenue was $2.7 billion, an increase of 9% versus the prior year driven by industrial. Adjusted operating income was $172 million, and adjusted operating margin was 6.4%, up 50 basis points year-over-year, primarily driven by industrial. Revenue from our Integrated Technology Solutions segment totaled $3.3 billion, up 22% versus the prior year, driven by continued strong growth in communications. 
Adjusted operating income was $181 million, and adjusted operating margin was 5.5%, an increase of 20 basis points year-over-year driven by communications and offset by weakness in consumer-related end markets. Finally, Cloud and Power Infrastructure revenue totaled $2.5 billion, up 54% versus the prior year, driven by continued strength in both power and cloud and cooling. 
Adjusted operating income was $268 million, and adjusted operating margin was 10.7%, up 240 basis points year-over-year, driven by margin expansion in both power and cloud and cooling as well as favorable mix impacts from power growth. Power segment operating margin increased to approximately 16%, up roughly 550 basis points year-over-year driven by strong volume growth and the benefits of scaling the investments we made last year. 
Moving to cash flow on Slide 10. Free cash flow in the quarter was $261 million and was negatively impacted by onetime cash costs of $61 million, driven by activity related to the announced spin-off. Q2 inventory was up 13% sequentially and 39% year-over-year, driven by revenue growth. Inventory net of working capital days was 60 days, an increase of 5 days from the prior year. The increase in inventory is primarily mix related, reflecting the inventory required to support our higher growth, higher value programs. Second quarter net CapEx totaled $240 million or approximately 3% of revenue.
Turning to our updated outlook on Slide 11. For fiscal year '27, our expectations are the following. Revenue to be between $34.9 billion and $35.9 billion, up 27% at the midpoint. Specifically, we expect CPI revenue to increase between 75% and 85%, while we expect combined RMS and ITS revenue to increase between 8% and 11%. Adjusted operating margin is expected to be between 7.6% and 7.8%, an increase of approximately 140 basis points year-over-year at the midpoint. For CPI, we expect adjusted operating margin to be between 11.5% and 11.7%. And for combined RMS and ITS, we expect adjusted operating margins to be between 5.9% and 6.1%. We expect an adjusted tax rate of approximately 21%. We expect adjusted EPS to be between $4.84 and $5.16 per share, up 52% at the midpoint. 
Finally, we expect CapEx to be in the range of $1.5 billion to $1.6 billion, and we expect free cash flow conversion of approximately 40%. As previously announced, we completed our acquisition of EPC Power on October 14. We also announced on October 5 an agreement to sell $2 billion of Axiom convertible preferred stock, the net proceeds of which will repay approximately $2 billion of the $4.4 billion in debt incurred as part of the EPC acquisition. As such, we expect elevated interest expense associated with debt from the acquisition in the short term, which will be reduced upon completion of the convertible preferred equity transaction. Despite the increased interest expense, we expect the EPC Power acquisition to be accretive in fiscal 2027.
Moving to our updated FY '27 segment outlook. For RMS, we expect revenue to be up mid-single digits to high single digits, driven by strength in industrial, including energy infrastructure, warehouse automation and robotics. For ITS, we expect revenue to be up low double digits to low teens on continued strong growth in communications. As previously referenced for CPI, we expect revenue to be up 75% to 85%, driven by both power and cloud and cooling, with power growing faster than cloud. This guidance now includes our acquisition of EPC Power, which closed on October 14. We now expect CPI operating margins to expand approximately 240 basis points year-over-year, assuming the midpoint of our guidance, up from our prior expectation of approximately 100 basis points. Looking ahead, we expect continued margin improvement supported by volume growth, productivity gains and the contribution from EPC Power. 
Finishing off with our guidance for the third quarter on Slide 13. We expect RMS to be up low single digits to mid-single digits, driven primarily by industrial and health care. We expect ITS revenue to be up mid-single digits to high single digits as strong growth in communications is offset by weakness in consumer-related end markets. We expect CPI revenue to be up 105% to 115%, as recent investments in both cloud and cooling and power contribute to strong growth. For total Flex, we expect revenue in the range of $8.87 billion to $9.17 billion, up 28% at the midpoint, with adjusted operating income between $685 million and $715 million.
Interest and other expense, which now includes debt associated with the EPC acquisition, is estimated to be around $120 million, and the adjusted tax rate to be around 21%. Lastly, we anticipate adjusted EPS to be between $1.19 and $1.25 per share, up 40% at the midpoint, based on approximately 375 million weighted average shares outstanding. In summary, we delivered a strong first half of fiscal year '27, and we are carrying that momentum forward into the second half of the year. With that, I will now turn the call back over to the operator to begin Q&A.

**Operator** (Operator):
[Operator Instructions] Our first question today is coming from Ruben Roy from Stifel.

**Ruben Roy** (Analysts):
Kevin, maybe we could start with some of the guidance commentary and the fiscal '27 guide. You've got a $950 million increase from the prior guide. Can you help us out with organic growth embedded in that increase versus the acquisitions, EPC and others, et cetera?

**Kevin Krumm** (Executives):
Yes, Ruben. So for the full year, we increased -- I'll talk first with CPI because that's where the line -- all the acquisitions this year have happened. So we guided to an increased range of 75% to 85% for the year. And inside of that, I would say about 10 percentage points of that is going to be growth related to acquisitions we've completed during the year. So you can -- the 2 that we've completed are the EP² acquisition, which we announced in the first quarter and then EPC recently.

**Ruben Roy** (Analysts):
Right. But I was wondering if you could kind of split that. I guess what you're saying is that there's not a lot of...

**Revathi Advaithi** (Executives):
I think, Ruben, your question is only EPC Power, right?

**Ruben Roy** (Analysts):
Yes. I guess, is there any way to think about the contribution from EPC?

**Kevin Krumm** (Executives):
Okay. So we've talked about EPC next year in our announcement and the growth that we were going to have, which was approximately $800 million this year, growing next year. Inside of our guide, increased guide to guide, if that's your question...

**Ruben Roy** (Analysts):
Yes.

**Kevin Krumm** (Executives):
We increased about $950 million, of which, I would say, approximately half of that is underlying improvement in Flex, and the other half would -- approximately would be the EPC acquisition we brought in.

**Ruben Roy** (Analysts):
Perfect. And Revathi, for a follow-up, let me ask sort of a bigger picture question here. You've done a few acquisitions now. You're spanning the embedded to critical power. Now you've got power conversion, and a lot of investors ask us about the power strategy longer term, but there's a lot of other things going on, cooling, compute, et cetera. How are you thinking about sort of having a broader set of technologies combined with power? Is that showing up in your win rates and customer economics from a margin perspective? Or should we still focus mostly on power as sort of the key area of the strategy going forward?

**Revathi Advaithi** (Executives):
Yes, Ruben, I'd say we'll talk a lot more about this on November 10 in our Innovation Day. But when I think about CPI or Axiom moving forward, I'd say all 3, compute, cooling and power, all 3 are important in terms of how we are building up the overall systems capability. Today, our areas of strength, where we are market share leaders and are technology leaders are both in compute and in power. 
I'd say cooling, our presence is still nascent. It is something that we are growing into with new product launches that are planned over the next 6 months. So that, I believe, will accelerate in our overall capability. But both compute and power are pretty integral to our overall strategy, both from where we stand today as market share leaders and where we move forward with in terms of our overall capability.

**Operator** (Operator):
Our next question is coming from Mark Delaney from Goldman Sachs.

**Mark Delaney** (Analysts):
I'm going to start on the power business and putting the EPC deal aside for the moment. Can you share more on the competitive positioning of Flex within the power portfolio, and has there been any meaningful change in the company's market share for either fiscal '27 or beyond? And then more broadly on CPI, how is that segment tracking relative to the prior 80% plus revenue growth outlook for fiscal '28?

**Revathi Advaithi** (Executives):
Yes, I'll start off, Mark. I would say, if you think about power overall, both our embedded power and our critical power business are both fantastically positioned from a technology perspective and a growth perspective. If you think about our power segment growth this year and even what we'll share later in Innovation Day, I'd say well above its peers in our existing segments. And it's a good indication of where our technology stands and kind of how the teams are performing with our capacity execution we talked about that happened last year. 
So it feels really good about our positioning, both in embedded power and in critical power. As you know well, embedded is all about technology and where we are positioned in the technology. So right now, embedded is all about continuing to execute on capacity and additions to drive the growth. CPI, I would say, performing extremely well. So both businesses I feel really good about overall in terms of the position. I'd say for your second part of your question on CPI for next year, Kevin, you want to handle that in terms of the 80%?

**Kevin Krumm** (Executives):
Yes, sure. So as we move through -- we started the year, Mark, 65% to 75%. We increased that. So underlying there, there is -- even excluding the EPC acquisition, we've been performing well. And our momentum this year has been north of our original expectations in CPI. While we're not going to offer a new guide for FY '28 right now, I would just say that momentum we expect it to carry through. And of course, as time has passed, we have better line of sight into next year, and we'll update you on that at Investor Day.

**Mark Delaney** (Analysts):
Understood. My other question was also on CPI. I mean the incremental EBIT margins in the just completed quarter were very strong and accelerated. I don't know if you could double-click a bit more on what was driving the strong incremental margins and just how you see the potential for CPI organic EBIT margins going forward.

**Kevin Krumm** (Executives):
So yes, in the quarter, we talked about a strong quarter. We finished with power margins in the mid-teens. The power growth is a big piece of the incremental margins you're seeing there. Although our cloud business continues to perform with different expectations, with good incrementals as well. Across the board, we saw mix favorability, pricing and volume leverage. We talked about investments we made last year. We're scaling through those, and we're seeing that volume leverage pull through from an incremental perspective as well. So those are really the big drivers. 
As we go forward here, again, expectations on the power side of the business continue to drive margins up. Cloud and cooling, as we've talked about it, we have expectations there. We just don't expect them to move sequentially at the same rate as power as we continue to climb towards industry averages.

**Operator** (Operator):
Your next question is coming from Ruplu Bhattacharya from Bank of America.

**Ruplu Bhattacharya** (Analysts):
I have 2. Revathi, it was interesting to hear Chris and Rob at OCP. I think their presentation was stressing that you can achieve 97% power efficiency to the rack even without SSTs. So as you start off as a new company, where do you see Axiom focusing on in terms of R&D and development? Is 800-volt and SST development a priority for you? And just as you look at your competitors, which are larger companies, how do you see yourself attacking this market? And how do you see yourself focusing on R&D versus acquisitions?

**Revathi Advaithi** (Executives):
Yes. I'd say, Ruplu, first is, we are very, very committed to and focused on both the 800-volt technology. We're the market leaders in that. As we have talked about before, there's a couple of players who are very strong in this space, and Flex or Axiom is definitely one of them. Solid-state transformers, we've talked about. We had our own organic program that was going on, which will now get added on to with the EPC Power acquisition, with their own organic technology development program that was going on. 
But the way I think about this, having done this for a very long time, Ruplu, is that it is important to drive incremental efficiency in the overall power chain value without waiting for the SST transition to happen. And I think that's important to really have the focus on that because as most of you know, electrical transitions take a long time because of the regulatory and safety environment associated with it. 
So our view is, in the meantime, you can achieve the 97% power efficiency with digital rectifiers that exist in the marketplace today, which is a huge part of the reason why we bought the EPC acquisition, because it provides a transition technology solution that is very strong and can get deployed today while we wait for things like SSTs and all of that to show up. So feel very good about both, but feel even strongly about the fact that we can deploy that power efficiency today, which a lot of customers are very excited about, Ruplu.

**Ruplu Bhattacharya** (Analysts):
My follow-up is for Kevin or Michael. RMS revenues were flat sequentially, but margins declined 20 bps sequentially. Can you maybe just talk about the puts and takes and which segments, which end markets are coming back, Michael? And what levers do you have for margin improvement going forward?

**Michael Hartung** (Executives):
Thanks for the question, Ruplu. Probably the easiest place to start is to really look at the business overall when you think about RMS and ITS combined. So as Revathi mentioned in her prepared remarks, Q2 actually represents the fourth consecutive quarter where both RMS and ITS delivered year-on-year growth. Because that growth was driven by our higher value markets, we were also able to expand margins at a higher rate than we were growing revenue. So the business is in very good shape and positioned from strength.
When you think about Q2, very strong result. High-value markets driving that growth across both RMS and ITS. As Kevin mentioned, on the ITS side, communications continues to be strong. On the RMS side, industrial continues to be strong. And so when you think about where we were at the beginning of the year, a couple of things are important to note. In the first half, we performed better than we expected across both ITS and RMS. Again, in ITS, communications driving that strength, but primarily from our advanced networking business, which is one of our high-value markets and are tied to those AI-related trends for data center build-out. RMS also over-delivered in the first half. 
Automotive performed as expected in a stable environment. Health care grew as expected, which should be no surprise. These are longer product life cycle businesses that perform on a consistent, steady basis. And then as mentioned, industrial over delivered primarily on the strength in our energy infrastructure business, where those businesses are tied to the AI and data center build-out, but also our robotics business was strong. And those things are tied to the deployment of physical AI and regionalization of the supply chain. 
Now as you look forward into the second half, keep in mind, we also highlighted that we're going to be lapping stronger comparables, given that the second half of last year is really where that momentum started to build. And so in the second half, we're still delivering growth on top of growth. Now there is some nuance to that, and underlying that, we are seeing incremental weakness in lifestyle, but that is being offset by communication in the ITS business. And in RMS, we are continuing to see consistent performance, and although it might not be linear in every single quarter, you can rest assured that when we think about the guide for the year, we expect both revenue growth and margin expansion.

**Operator** (Operator):
Your next question today is coming from Tim Long from Barclays.

**Timothy Long** (Analysts):
Two questions, if I could as well. First, maybe a little bit more generic thinking about the strong growth in CPI, specifically for fiscal '27 and '28, I guess both 80% at this point. Could you just touch a little bit on kind of capacity components, CapEx needed, power availability, things like that, that give you confidence that we can meet those numbers in what still could be a tight supply area? 
And then secondly, I was hoping you could just touch on the cloud-related business. Maybe you could just give us a little sense on some of the subparts there that might be more driving growth, whether it's rack assembly or custom ASIC programs or the growth in liquid cooling that you mentioned as a nascent business. So if you could just give us a little color there, that would be helpful.

**Revathi Advaithi** (Executives):
Yes, Tim, I'll start off. I'd say in CPI, for the guide we gave for FY '27, which is the 65% to 75% midpoint of 70%. And then the one for next year, which is 80% that we'll update here in Investor Day. The capacity plans were already in place starting last year. And for the 80% guide, obviously, capacity plans have been in place this year. So that we have been putting in place for a bit. The power requirements required for that also have been ongoing for a while. 
In some cases, you have to connect utilities and substations into these factories for the power requirements. So these have been very, very stringent project planning by our teams to get the capacity in place for the CPI ramps that we have been talking about. So it'll be -- it's a couple year journey for this kind of growth, right? So I feel good about the things we control, that is capacity, power availability. And our teams are very good at standing up these types of facilities and ramping them up. So that is going really well. 
I'd say on the component side, I mean, the shortage issue, I think you all know extremely well. We are going into -- we have been in a situation in the last 12 months, which will continue over the next, I think, few years in terms of component shortage and availability. The supply-demand equation is definitely tilted. But again, Flex is very good at being able to chase suppliers, look at open market availability. That's why customers come to us. And we take some of that into account, Tim, as we give our guidance. We estimate what kind of shortages we think we'll have, and we plan for that. You know very well how our guiding process works, and you guys give me a lot of pushback about being conservative. So I'd say component shortage, it definitely plays into how we think about the guide, and we have included that in how we -- all the forecasts that we have. 
On the cloud-related business, I would say, Tim, our focus always in the cloud-related business has been more in the custom configuration. We have been very clear before that our focus is around where there is specialty work, where there's complicated work, highly technical in terms of testing capability. So while it is around rack integration and things like that, it is in the custom space. We don't do standard configurations in general. 
The places we are, I would say, pushing further into this space is more in terms of vertical integration. I've talked before about we like to be able to be the ones who are cutting metal and doing all of that. So doing most of the rack work is really important to us, so we can take that from industrial players who tend to do it today. So I would say vertical integration into that. The other big play is the service side, which is fairly nascent in some cases. We have a big ramp going on in Memphis as a result of that. So really doubling down into the aftermarket service because a lot of these racks are going to get pulled out over the next couple of years and need to get reconfigured and put back in. 
And then I'd say on the cooling side, like I said, nascent for us, but we have big product lines coming out that is really going to position us extremely well. It'll take a few months to get all the testing done and to deploy them, but feel really good about being able to ramp into the cooling business. So cloud overall, strong growth. And like Kevin said, we feel good about the incrementals in that business and how we are delivering. And for us, it's never been about just go get volume. We want the volume to come with great operating margins that are incremental to what we do, and we want it to have good working capital metrics. Only those are the kinds of business we go pursue in cloud, which is a very high ROIC business, as all of you know.

**Operator** (Operator):
Next question is coming from Steven Fox from Fox Advisors.

**Steven Fox** (Analysts):
First question I had was, you guys mentioned in the prepared remarks, focus on the legacy business with health, energy and comms on difficult to replicate capabilities. I was wondering if you could just sort of dig into that a little bit, give us an idea of what you're thinking about when you make that statement? And then I had a follow-up.

**Revathi Advaithi** (Executives):
Michael?

**Michael Hartung** (Executives):
Steven, thank you for the question. I'd say when you think about the high-value markets and where we intend to emphasize, they're really based on 2 underlying principles. One, the end market growth enables us to grow at double digits, and also those markets tend to require complex solutions that enable us to earn margins above the company average. And those types of things include everything from, call it, regulatory environment. So in our health care business, we have an extensive footprint that is FDA certified that can not just ramp new programs, but sustain those over the long term, and that provides us with a certain amount of protection over the long term because the switching costs tend to be so high and the investments tend to be more considerable when you start up those businesses. So regulatory was one aspect. 
When you think about automotive, I think was also part of your question, similar things, highly regulated environments, long product life cycles and those things create a moat for competitive advantage over the long term. When you think about communications, what we think about is this really unique offering that we now have when you consider both our communications business that we've built over years, our recently talked about advanced networking business and our satellite communications business. So we now have a portfolio of solutions that scales from space to Earth to end user, and those combined capabilities are truly differentiated in the marketplace when you consider that they operate at scale in multiple regions across the globe. So those are the types of things, whether they be regulatory, technology or scale related items that provide us with that protection, that long-term competitive advantage.

**Steven Fox** (Analysts):
Great. That's helpful. And then as a follow-up, Revathi, I think one of the things people have been sort of dialing in on is just going to be the customer concentration of Axiom post-spin. And I was just curious, maybe you can give us a little bit more color on how diversified you are with your top 2 customers, how maybe that business flow gives you sort of confidence in the visibility, things like that, to get comfortable with the idea that you have 2 customers that could be like 60%, 70% of sales.

**Revathi Advaithi** (Executives):
Yes, Steven, I think as I've talked about diversity and customer concentration in the light of, first is who's investing in this build-out that is happening. So if you start with that, it is clear, obviously, that of the $1 trillion expansion that is going on, a significant portion of that comes from a few hyperscalers. And within those hyperscalers, it's very clear in terms of who do custom configuration, where we can win, and where the spend is coming from. So our focus around hyperscalers is we want to be very diversified in these hyperscalers. So we just -- we don't want to do only cloud compute integration. We want to be able to do everything from designing your power modules to designing your custom embedded power to your 800-volt rack, to your entire distributed power, now all the way to beyond the meter with our solutions around Crown, our EP² and our EPC Power capability. 
So we want to start all the way from utility substation to be able to take it to the chip itself, and we want to be fully diversified inside each hyperscaler. So I think about customer concentration, can't walk away from the fact that hyperscalers are spending the most amount of money. If you want to be able to grow your market share, you have to grow with these hyperscalers. So that is important, but we want to be diversified in our full portfolio across all of them, and each of the business units have to have multiple programs for each of these hyperscalers, not just individually one program that they're working on. 
I would say, it's interesting, I've been in the electrical space for a very, very long time, Steven, as you know, even the very traditional electrical players are now ending up with more concentration around hyperscalers because that's where the spend is. Even power spend is more concentrated towards hyperscalers. So I think this is a good story because if you're not concentrated towards hyperscalers, you're going to be losing market share in this space. So -- and our focus is across multiple products, multiple programs with these hyperscalers.

**Operator** (Operator):
[Operator Instructions] Our next question is coming from Luke Junk from Baird.

**Luke Junk** (Analysts):
Kevin, want to circle back to supply chain. It's been topical recently, especially in CPI. Just hoping you can walk us through some of the levers that you're pulling there in terms of inventory investment, getting support from some of the larger customers or similar dynamics, and just maybe speak to your level of confidence as well, or maybe some specific buffers that you've included in guidance for supply chain.

**Kevin Krumm** (Executives):
Luke, thanks for the question. As we looked towards our guide in Q1, when we gave our full year guide, we had understood it was going to be a difficult year from a supply chain sourcing standpoint. So that's been reflected in our guide through the year and is, of course, reflected in our current guide. As Revathi talked about it, we have a unique capability here in this organization to manage through those elements in a year like this year, and our team is doing a fantastic job. Our customers, as you know, as we think about inventory and the ramps that we have in place, of course, our inventory build is not going to be linear. 
As we move through the year, we've seen some inventory increases. Generally, our model requires our customers to participate in that. So we have -- we generally talk about inventory, net of working capital advances. But we've been working -- when you look at working capital across the board, our teams have been doing a good job to stay really well balanced from a working capital investment standpoint. At rates specifically, our teams have managed well too. So a rocky environment, it's been in our guide. We're going to see it in inventory, especially as we ramp these programs, but we don't expect it longer term to have any negative impact from a rate standpoint.

**Luke Junk** (Analysts):
Got it. And then for my follow-up, Revathi, just be great to get your perspective on the power portfolio margins and CPI now that the Form 10 is out. Just how you think about the embedded portfolio today relative to critical and some of the major chunks moving towards industry averages, I'm sure we'll get into that more at Investor Day as well.

**Revathi Advaithi** (Executives):
Yes. Look, we'll share a lot more at the Investor Day, but I'd say that, if you think about embedded power and critical power, they both play, and then now EPC, they all have different roles to play in the power chain. But why it makes more sense to build this out end-to-end is when you think about all the step-up, step-down that happens in power conversion, starting all the way from utilities to the chip itself, having an end-to-end kind of 800-volt transition seamlessly is what will drive maximum power efficiency someday, right? 
And so when we are working with kind of the semiconductor and the chip providers 2, 3 years ahead, when they're developing their chip and developing the right kind of future power technology for the chip itself, then we can start getting ready with our critical power business and now with our EPC Power business to be way ahead of the game compared to where everyone else is at in terms of driving the right technology. So that's why building this out end-to-end has been very important, because if you do it piecemeal, you're still going to lose out on power efficiency because you'll have all the step-up, step-down that will happen through the power chain. 
And that's why EPC Power is a good addition because we add more to the end of the line where we were -- didn't have as much product, and then having all the digital rectifier, we can get to that power efficiency today. So Luke, we'll show this in great detail in terms of Innovation Day, you'll be able to see this end-to-end and why it makes sense as a complete portfolio.

**Operator** (Operator):
Our next question is coming from Steve Barger from KeyBanc Capital Markets.

**Steve Barger** (Analysts):
Revathi, I think the prior question mentioned CapEx, and maybe I missed the answer. Can you talk about capital intensity to support growth over the next year or 2 for Axiom? And then same question for Michael, any change to CapEx to revenue for Flex from here?

**Revathi Advaithi** (Executives):
Okay. Kevin, you'll talk CapEx?

**Kevin Krumm** (Executives):
Yes, sure. I'm happy to. So Steve, thanks for the question. From a CapEx standpoint, we talked about this year being a year of outsized investment. We've guided to a number about $1.5 billion to $1.6 billion. The work we've done with respect to CapEx in the first half of the year was largely to secure the capacity we needed to perform at the levels we are this year. So that's the work that's largely been done. As we go into the back half of the year, Revathi mentioned it earlier, that CapEx is largely focused on building out the capacity and the requirements we need, power included, to deliver the results that we're guiding towards or looking towards, I'll say, in FY '28. 
So that's really how it's stacked up. We also have talked about the outsized investment this year being largely for CPI. So I'd say, rough numbers, about 1/3 of the investment this year is related to ITS and RMS and about 2/3 of that is related to CPI. And you can see in the first half of the year, we've done about 1/3 of it. So about 1/3 of it this year was related to FY '27 and about 2/3 is related to securing capacity for FY '28.

**Revathi Advaithi** (Executives):
Michael?

**Michael Hartung** (Executives):
Yes. And then on the Flex side post-spin, you should see RMS and ITS revert back to historical levels, which should mean we should be at that 2% or below level for the foreseeable future.

**Steve Barger** (Analysts):
Got it. And then, Michael, you mentioned the robotics business has been a growth driver for industrial this year. Does that feel like the beginning of a multiyear production ramp? And can you talk about trends across cobot, robot, AMR and maybe humanoids if you're seeing any inquiry or prototype activity there?

**Michael Hartung** (Executives):
Yes, great question, and thanks for it. So when you think about robotics, we've named robotics as one of the 6 high-value markets that we're emphasizing, and that's because we do believe that, that industry is tied to these longer-term secular trends that our capabilities are well aligned against. When you think about robotics, think about it on a spectrum of opportunities, and they range from, call it, warehouse automation and fixed automation all the way through humanoids. And when we think about that range of possible, we also think about the unique role that we play in the industry as a consumer, as a supplier and as an innovator.
So let me build on what we're seeing there. So inside of Flex, we've already deployed our own manufacturing automation platform, which is standard automation that we can deploy across our network. To make sure that we've got not only standardized platform, but also that we're automating what were previously manual processes to set the stage, not just for automation, but also for physical AI deployment. 
In the industry, we're starting with warehouse automation that tends to be more fixed in nature, but still provides the benefit of automation and lays the groundwork for physical AI. We are also not just a consumer of, but a supplier of cobots. These cobots we've talked about in our relationship with Teradyne, as an example, where we utilize their equipment on our production floor and where we build elements of that cobot for them that they in turn bring to the market. 
And then when you think about humanoids, although I don't envision that we'll deploy humanoid-type technologies in the next year or 2, we are on road maps developing that technology, and we're in a position where we can leverage both the capability that we've developed in automotive with our centralized compute capability, with our actuation capability, combine that with our mechanical aptitude to actually help customers bring those solutions to market more quickly than they could otherwise do on their own. So short answer, yes, we believe this is the beginning of a long-term trend, and we're looking forward to participate in that over the next years.

**Operator** (Operator):
We've reached the end of our question-and-answer session. I'd like to turn the floor back over for any further closing comments.

**Revathi Advaithi** (Executives):
Thank you, everyone. We had a strong first half for the fiscal year, and we're carrying that momentum forward to the second half and the spin-off. I want to thank our customers and our shareholders, and then a big shout-out to the global Flex team for executing so well in this environment as they work through kind of the spin and everything else that's going on. I also want to encourage all of you to join us for Innovation Day, where you can take all this from seeing it in PowerPoints and slides to touching and feeling and seeing how the products really work. So I'd like to see all of you at Innovation Day, November 10. Thank you.

**Operator** (Operator):
Thank you. That does conclude today's teleconference. You may disconnect your line at this time, and have a wonderful day. We thank you for your participation today.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FLEX_Q1_2027_Earnings_Call_20260729.md
- 2026-07-29｜Kevin Krumm (CFO)｜guidance：FY27 營收區間與中點成長（原話："Revenue to be between $33.7 billion and $35.2 billion, up 23"）
- 2026-07-29｜Kevin Krumm (CFO)｜guidance：FY27 調整後 EPS 區間（原話："adjusted EPS to be between $4.42 and $4.74 a share, up 39%"）
- 2026-07-29｜Kevin Krumm (CFO)｜guidance：FY27 CPI 營收成長指引，power 成長快於 cloud（原話："with power's growth rate exceeding cloud's."）
- 2026-07-29｜Kevin Krumm (CFO)｜guidance：FY27 CapEx 指引區間（原話："we expect CapEx to be in the range of $1.5"）
- 2026-07-29｜Kevin Krumm (CFO)｜guidance：FCF 轉換率指引納入分拆成本後調為約 40%（原 60% 不含分拆成本）（原話："costs associated with the spin-off, we now expect free"）
- 2026-07-29｜Kevin Krumm (CFO)｜guidance：Q2 CPI 營收成長指引（原話："We expect CPI revenue to be up 45% to 55% as new programs"）
- 2026-07-29｜Kevin Krumm (CFO)｜guidance：Q2 EPS 指引（原話："adjusted EPS to be between $1 and $1.07 per share, up 32%"）
- 2026-07-29｜Kevin Krumm (CFO)｜margin：FY27 調整後營業利益率指引（原話："Adjusted operating margin to be between 7% and 7.2%"）
- 2026-07-29｜Kevin Krumm (CFO)｜margin：管理層對 Q1 營業利益率改善的歸因（原話："business mix and underlying productivity improvements."）
- 2026-07-29｜Kevin Krumm (CFO)｜margin：CPI Q1 營業利益率數字（原話："adjusted operating margin was 9.7%, up 20 basis points year-"）
- 2026-07-29｜Kevin Krumm (CFO)｜margin：ITS 利益率歸因：通訊強、消費端弱（原話："and offset by weakness in consumer-related end markets."）
- 2026-07-29｜Revathi Advaithi (CEO)｜margin：CEO 解釋 power 利益率低於同業的原因（原話："slightly muted compared to our peers"）
- 2026-07-29｜Revathi Advaithi (CEO)｜commitment：CEO 重申 CPI 全年利益率至少改善 100bp（原話："at least 100 basis points improvement in margin in the CPI"）
- 2026-07-29｜Revathi Advaithi (CEO)｜commitment：CEO 稱 power 利益率會朝同業水準移動（原話："we're very comfortable with moving it in the"）
- 2026-07-29｜Revathi Advaithi (CEO)｜commitment：CEO 稱 CPI 今年做到 70% 或更好（原話："track for it, definitely to do the 70% or better than that."）
- 2026-07-29｜Revathi Advaithi (CEO)｜commitment：分拆時程：2027 第一曆季完成免稅分拆（原話："tax-free spin-off in the first quarter of calendar 2027."）
- 2026-07-29｜Revathi Advaithi (CEO)｜commitment：Investor Day 將提供分拆後兩家公司細節（原話："November 10, where we will provide additional details"）
- 2026-07-29｜Kevin Krumm (CFO)｜guidance：CFO 稱 CPI 未來三季已預訂 90% 以上（原話："90% plus booked business at this point for the next 3"）
- 2026-07-29｜Revathi Advaithi (CEO)｜guidance：CEO 稱除產能建置外無重大限制，並提及 FY28 CPI 80% 指引（原話："Don't see any significant constraints per se"）
- 2026-07-29｜Revathi Advaithi (CEO)｜guidance：CEO 稱 Q1 CPI 成長高於原指引的 30%（原話："We said 30%, we came in higher than"）
- 2026-07-29｜Revathi Advaithi (CEO)｜product：高壓（400V/800V）轉換：CEO 稱可能有上行空間（原話："there should be some upside to that, I would say, as"）
- 2026-07-29｜Revathi Advaithi (CEO)｜product：冷卻業務自述仍屬早期（原話："it's still nascent"）
- 2026-07-29｜Revathi Advaithi (CEO)｜product：冷卻擴張尚待工作（原話："to be done in terms of scaling that business"）
- 2026-07-29｜Revathi Advaithi (CEO)｜competition：CEO 回應其他 EMS 進入同領域：認為有誤解（原話："having true IP and product capability."）
- 2026-07-29｜Revathi Advaithi (CEO)｜competition：CEO 稱未見他人同時具備這些能力（原話："I haven't seen anybody just have that capability yet."）
- 2026-07-29｜Revathi Advaithi (CEO)｜customer：多家超大規模客戶就電力/冷卻/矽晶片有高層策略對話（原話："several hyperscaler customers at a very high level"）
- 2026-07-29｜Revathi Advaithi (CEO)｜customer：Cerebras 合作被描述為分散超大規模客戶的例子（原話："a good example of us diversifying our hyperscaler involvemen"）
- 2026-07-29｜Kevin Krumm (CFO)｜customer：Amazon 協議：無更新，效益橫跨各業務（原話："there's really nothing to update."）
- 2026-07-29｜Revathi Advaithi (CEO)｜capital_allocation：SpinCo 需要為快速成長設計的資本配置框架（原話："SpinCo requires a capital allocation framework designed for"）
- 2026-07-29｜Michael Hartung (CCO)｜capital_allocation：RemainCo 持續優化組合、淡化低價值市場（原話："deemphasizing low-value markets along the way."）
- 2026-07-29｜Michael Hartung (CCO)｜risk：工業需求被描述為長期結構性而非循環復甦（原話："We see this tied very much to an ongoing infrastructure"）
- 2026-07-29｜Kevin Krumm (CFO)｜risk：Q1 自由現金流數字（原話："Free cash flow in the quarter was $41 million."）

### 問答異常語氣（迴避／改口／保留）
- FLEX_Q1_2027_Earnings_Call_20260729.md｜問：Ruben Roy 問 CPI 已安裝產能及客戶認證/待調試的比例（要百分比或高層概況）｜答法：CEO 未給百分比或已認證/待調試比例，改答對全年計畫感覺良好、產能建置進行順利
- FLEX_Q1_2027_Earnings_Call_20260729.md｜問：Mark Delaney 問冷卻市場對 Flex 的規模有多大｜答法：CEO 未給市場規模數字，改以定性描述（市場成長、仍屬早期、有工作待做）
- FLEX_Q1_2027_Earnings_Call_20260729.md｜問：Steven Fox 問 Amazon 合作更新及分拆後歸屬｜答法：CFO 稱無更新、將於今年評估該安排，未給細節

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

## ⑥ 條件附卡（archetype_hint='EMS/ODM' 命中）：judge_addendum_cyclical.md

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
{"date":"20260518","verdict":"B（觀望·thesis 完整 — Q4 FY26 beat + SpinCo 公告 + FY27 guide raise + AI infra 訂單 verified；但估值 🟡 救援後 PEG 0.87 / Fwd PE 31x（5Y 分位 92%）+ Pure MA ✅ 極端拉伸 4.5x W250、12 週 +119% 動能末段，等回測 W52 $63 / BB 中軌 $76 分批進場）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"CPI segment 高速成長持續 + OPM 擴張至 10%+（AI infra 訂單兌現 + spinoff 純 play 後 margin unlock）","columns":{"2Y 驗證點":"FY27/FY28 CPI rev YoY ≥ 50%（管理層 guide 65-80%）；OPM 從 9.2% 升至 10%+","5Y 驗證點":"SpinCo standalone 後 FY29-FY30 revenue 累計達 $15-18B（vs FY26 $6.6B base = ~14% CAGR sustained）；OPM 12%+","10Y 驗證點":"SpinCo 在 2031-2035 成為 AI infra 平台地位（如 NVIDIA-tier vendor），revenue $25B+，OPM 15%+ 接近 ARSL（特殊半導體設備）水準","驗證指標":"CPI rev YoY %；OPM%；top 3 customer concentration%；新客戶數（hyperscaler / colo / sovereign AI）","資料來源":"2Y: §6 季度財報；5Y: §8.A Runway + §11 產業 TAM；10Y: §8.A' S 曲線位置"}},{"id":"H2","text":"SpinCo 分拆順利 + 估值 unlock（pure play multiple expansion）","columns":{"2Y 驗證點":"2027 Q1 完成分拆（S-1 申報、SEC 過審、上市）；SpinCo IPO 估值 ≥ $30B","5Y 驗證點":"SpinCo standalone 2 年後（2029）合計 sum-of-parts 市值 ≥ 當前 FLEX 市值 1.6x（$80B+）","10Y 驗證點":"SpinCo 進入 S&P 500 / Russell 1000，成為 AI infra tier-1 reference name；分拆證明可複製","驗證指標":"SpinCo / RemainCo 上市後市值；analyst sum-of-parts target；index inclusion","資料來源":"2Y: §12 治理 / §6 8-K filings；5Y: §13.4 同業重新分類；10Y: §9 生態地位"}},{"id":"H3","text":"估值倍數從 31x re-rate 至「結構升級後 fair」22-28x（非崩塌至 15x）","columns":{"2Y 驗證點":"2027-2028 Fwd PE 收斂至 25-30x，EPS 持續上修支撐 PEG ≤ 1.0","5Y 驗證點":"2029-2030 SpinCo 估值穩定在 35-40x（pure AI infra play），RemainCo 18-20x（成熟 EMS）；加權 25-28x","10Y 驗證點":"2033-2036 估值收斂回 EMS / specialty industrial 自然倍數 18-22x；EPS 已超 $12+ 補償估值收斂","驗證指標":"Fwd PE; PEG; 5Y 分位; sum-of-parts valuation","資料來源":"2Y: §13.1; 5Y: §13.5; 10Y: §8.E 壓力測試 5Y/10Y"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Hyperscaler 自研 manufacturing 全面 in-house（Google / Meta / Microsoft / Amazon 任一）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（2-3 年）","監測指標":"top 3 hyperscaler 公開 in-house manufacturing 計畫；FLEX CPI 客戶集中度變化","警戒閾值":"連 4 季 CPI 客戶集中度 top 3 客戶 share 下滑 ≥ 10pp，或任一 hyperscaler 公開 in-house 計畫"}},{"id":"R2","text":"SpinCo 分拆延後 / 監管阻擋 / 內部執行卡關","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（12 月內）","監測指標":"SpinCo S-1 申報時程；SEC review 進度；management 公開時間表變化","警戒閾值":"2027 Q1 未完成分拆（管理層 guide 是 Q1 2027），延至 H2 = 黃燈，延至 FY28 = 紅燈"}},{"id":"R3","text":"AI capex super-cycle 提前見頂（hyperscaler capex YoY 跌入負成長）","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期結構（5+ 年）","監測指標":"top 5 hyperscaler 季度 capex YoY%；NVDA data center revenue YoY%","警戒閾值":"top 5 hyperscaler 連 2 季 capex YoY -10%+，或 NVDA DC revenue YoY 連 2 季 &lt; 20%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":137.86,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
