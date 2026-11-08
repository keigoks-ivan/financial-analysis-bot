你是 stock-analyst **v20 判斷 agent**，標的 COR（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"COR","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap_q4","label":"Revenue (GAAP) Q4","value":"88.4","period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf"},"note":"共識營收未查（報導稱營收與調整後EPS均優於共識）；YoY +5.5%；QoQ 未取得"},{"id":"f_kpi1_gaap_operating_income_ma","label":"GAAP operating income / margin Q4","value":906.8,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf"},"note":"n/a；margin 1.03%（去年同季 18.5M、0.02%，含 PharmaLex 商譽減損 723.9M）"},{"id":"f_kpi2_adjusted_non_gaap_operat","label":"Adjusted (non-GAAP) operating income / margin Q4","value":1248.9,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf"},"note":"n/a；YoY +22.1%（去年同季 1,023.1M）；margin 1.41%（去年 1.22%，+19bp）"},{"id":"f_kpi3_adjusted_diluted_eps_q4","label":"Adjusted diluted EPS Q4","value":4.66,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf"},"note":"共識 4.57（來源：247wallst／Nasdaq 轉述，非 IR）；YoY +21.4%（去年 3.84）；GAAP EPS 2.71"},{"id":"f_kpi4_free_cash_flow_fy2026_op","label":"Free cash flow FY2026 (operating CF − capex)","value":3881,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf"},"note":"n/a；營運現金流 4,790M、資本支出 910M；調整後 FCF 3,808M（扣除反托拉斯和解收益 73M）；僅提供全年，未提供單季"},{"id":"f_kpi5_guidance_fy2027_adjusted","label":"Guidance FY2027 adjusted diluted EPS","value":"19.40–19.75","period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf"},"note":"共識 FY1 EPS 19.70（來源：consensus_revision 20261107 快照，財報後）；成長 8–10%；調整後營業利益成長 4–6%、淨利息 490–510M、稅率約 20%、股數約 190M、調整後 FCF 約 3.5B、資本支出約 1.0B"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cor_gross_margin_pct","label":"COR 毛利率","value":4.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cor_operating_margin_pct","label":"COR 營業利益率","value":1.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cor_fcf_margin_pct","label":"COR FCF 利潤率","value":0.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cah_gross_margin_pct","label":"CAH 毛利率","value":3.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cah_operating_margin_pct","label":"CAH 營業利益率","value":1.26,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cah_fcf_margin_pct","label":"CAH FCF 利潤率","value":1.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mck_gross_margin_pct","label":"MCK 毛利率","value":3.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mck_operating_margin_pct","label":"MCK 營業利益率","value":1.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mck_fcf_margin_pct","label":"MCK FCF 利潤率","value":1.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_gross_margin_pct","label":"HSIC 毛利率","value":31.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_operating_margin_pct","label":"HSIC 營業利益率","value":5.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_fcf_margin_pct","label":"HSIC FCF 利潤率","value":3.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":333.56,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":28.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":51.57,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.3,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.76 → 19.7）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（21.93 → 21.93）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（24.27 → 24.27）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":19.7,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":21.93,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":24.27,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":10.3,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 17.86 → 19.7（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":18.58,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.19,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.21,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":16.93,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 19.7，分子＝快照價 333.56","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.72,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":6385.82,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 11266.15、現金 4880.33（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":190.83,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":70038.13,"period":"2026-11-08","unit":"USD m","basis":"市值 63652.31 ＋ 淨負債 6385.82","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":352568.91,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（6 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":368784.58,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（6 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.2,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 333.56 / W52 322.29 / W104 298.89 / W250 229.74 / W250 13週斜率 1.46%"},{"id":"f_ma_w52","label":"52 週均線","value":322.29,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":298.89,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":229.74,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.46,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列主要對手為 McKesson、Cardinal、UPS Logistics；另與製造商直銷、連鎖藥局自設倉儲、專科經銷商、包裝與醫療科技公司競爭；競爭因素為價格、產品、加值服務、配送、信用條件與客戶支援。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"Our largest competitors are McKesson Corporation (“McKesson”), Cardinal Health, Inc. (“Cardinal”), and UPS Logistics, among others.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素稱產業整併（製造商、零售藥局、醫療提供者、保險人結盟）可能加大競爭壓力，持續整併可能降低議價力或造成客戶流失。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"Continued consolidation within the healthcare industry could adversely affect our results of operations, to the extent we experience reduced negotiating power or possible customer losses.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"CSIMarket 營收基準同業群占比 Q2 2026 約 31.97%，去年同期 32.86%（聚合站、方法不明）","source":"CSIMarket COR Competitors","url":"https://csimarket.com/stocks/COR-Competitors","excerpt":"31.97 % vs 32.86 % a year ago Revenue Growth Y/Y 3.85 % Peers: 8.12 % Net Margin 2.08 % Peers: 2.36 % Key Findings: Cencora Inc vs Its Competitors","as_of":"2026-08-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Simply Wall St 敘事：專科經銷競爭、大客戶擴張自有專科業務與產業整併可能侵蝕議價力與市占","source":"Simply Wall St narrative","url":"https://simplywall.st/community/narratives/us/healthcare/nyse-cor/cencora/innovating-pharma-commercialization-and-efficiency-to-propel-revenue-and-margins","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露客戶集中：Walgreens 與 Boots 合計約占營收 25%、Evernorth 約 13%、前十大客戶約 66%；並警告關鍵客戶或 GPO 合約可能到期未續、被終止或以較差條件續約。一手文件未載明客戶導入第二供應商或自製。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"Walgreens and Boots together accounted for approximately 25% of our revenue in fiscal 2025 and, as of September 30, 2025, accounted for approximately 38% of our accounts receivable, net. Evernorth Health Services accounted for approximately 13% of our revenue in fiscal 2025. Our top ten customers, including governmental agencies, represented approximately 66% of revenue in fiscal 2025.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025：前十大客戶約占營收 66%；Walgreens 與 Boots 合計約 25%、Evernorth 約 13%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"Our top 10 customers, including governmental agencies and group purchasing organizations (“GPO”), represented approximately 66% of revenue in fiscal 2025. In fiscal 2025, Walgreens and Boots together accounted for approximately 25% of revenue and Evernorth Health Services accounted for approximately 13% of revenue.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025-09-30 Walgreens 與 Boots 合計占應收帳款淨額約 38%，Evernorth 約 5%；公司揭露最大客戶破產或信用失敗可能造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"As of September 30, 2025, our two largest trade receivable balances due from customers (Walgreens and Boots together and Evernorth Health Services) represented approximately 38% and 5% of our accounts receivable, net.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"自 2026-07-01 起，部分 Walgreens 量體移出 Cencora；主供應商協議不變，占與 Walgreens 業務絕大部分。","source":"Cencora Form 8-K (2026-08-12)","url":"https://www.sec.gov/Archives/edgar/data/0001140859/000110465926094676/tm2622984d1_8k.htm","excerpt":"The prime vendor agreement, which remains unchanged, constitutes the vast majority of the Company's business with Walgreens.","as_of":"2026-08-12","retrieved_at":"20261108","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Walgreens 於 2025-08-28 被 Sycamore 私有化，評等機構撤銷評等；私有化前 S&P 為 BB- 並列負面 CreditWatch。查無 2026 年新降評。","source":"investing.com／InvestmentGrade.com 搜尋摘要","url":"https://ng.investing.com/news/stock-market-news/walgreens-acquisition-by-sycamore-partners-leads-to-sp-negative-creditwatch-93CH-1804147","excerpt":null,"as_of":"2025-08-28","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cencora FY2027 guidance (issued 2026-11-04): adjusted EPS $19.40–19.75 (+8–10%), revenue growth 3–5%; specialty segment revenue growth 9–14%.","source":"finviz/finchannel coverage of Cencora Q4 FY26 release","url":"https://finviz.com/news/415659/cencora-closes-fy26-above-raised-guidance-but-a-divestiture-diluted-fy27-outlook-resets-expectations-lower","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"GLP-1 volume lifts US revenue (FY26 GLP-1 revenue growth $2.8B YoY) but at lower gross margin, partly offsetting gross-margin improvement.","source":"Cencora Q4 FY26 earnings coverage (search summary)","url":"https://finviz.com/news/415659/cencora-closes-fy26-above-raised-guidance-but-a-divestiture-diluted-fy27-outlook-resets-expectations-lower","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Drug Channels Institute 2026-27 Economic Report on wholesalers: industry transitioning toward a Net Pricing Drug Channel.","source":"Drug Channels","url":"https://www.drugchannels.net/2026/10/now-available-dcis-new-2026-27-economic.html?hl=en","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因素：藥品供應鏈受 FTC、DEA、FDA、HHS 及英國／歐盟等多層監管，供應鏈安全新規可能大幅增加配送成本與負擔；業務可能涉及反壟斷等政府調查。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"In recent years, some governments have passed or proposed laws and regulations intended to protect the safety and security of the supply chain that could substantially increase the costs and burden of pharmaceutical distribution.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K Item 3 法律程序僅指向附註 12（法律事項）與附註 13（反壟斷訴訟和解），公司為反壟斷和解的受益方（原告端）；MD&A 列示反壟斷和解收益 236,372（千美元）對前年 170,904。","source":"SEC EDGAR 10-K FY2025 Item 3 / Item 7","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"Gains from antitrust litigation settlements 236,372 170,904 LIFO credit 76,876 52,168","as_of":"2025-11-25","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Cencora MWI Animal Health 與 Covetrus 合併案（2026-02-18 宣布）被報導受 FTC 審視；聚合站標題，未核一手。","source":"myvetcandy.com 經搜尋聚合引述","url":"https://www.sec.gov/Archives/edgar/data/0001140859/000114085926000034/cor-20260630.htm","excerpt":"concluded that the MWI Animal Health disposal group met the held for sale criteria and classified its assets and liabilities as held for sale. On May 20, 2026, the Company received a request for additional information and documentary materials from the Federal Trade Commission (the “FTC”) in connection with the FTC’s review of MWI Animal Health’s proposed merger with Covetrus, Inc.","as_of":"2026-08-06","retrieved_at":"20261108","affects":["triggers","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Cencora FY2025 10-K 風險因素：公司可能因美國關稅或其他保護措施而面臨供應中斷、短缺或額外成本（含包裝、材料、設備），並點名既有芬太尼關稅、對等關稅、對印度／巴西產品的次級關稅，以及 Section 232 對藥品與原料的威脅性關稅；公司稱無法預測其實施或調整方式。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"During fiscal 2025, we continued to experience increased costs, including for fuel, and it is possible that we could experience supply disruptions, shortages, or additional costs (including with respect to packaging, materials, and other equipment) resulting from U.S. tariffs or other protective measures.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 載明所購藥品受價格通膨／通縮及已威脅與已實施關稅影響；學名藥價格通縮加速會加重對經營結果的負面衝擊。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"The pharmaceutical products that we purchase are also subject to price inflation and deflation, as well as the threatened and enacted tariffs described above.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 載明公司受美國出口管制與貿易制裁法規約束，違反可能導致罰款及喪失出口許可；未提及已發生的出口管制事件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"we are subject to the U.S. Foreign Corrupt Practices Act (the “FCPA”), U.S. export control and trade sanction laws, and similar anti-corruption and international trade laws in certain foreign countries","as_of":"2025-11-25","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Cencora 就關鍵藥品成分戰略 API 儲備（SAPIR）行政命令發表媒體聲明","source":"Cencora newsroom: Media statement SAPIR","url":"https://www.cencora.com/newsroom/sapir-with-critical-drug-components-media-statement","excerpt":"Media Statement on the Executive Order to Fill the Strategic Active Pharmaceutical Ingredients Reserve (SAPIR) with Critical Drug Components","as_of":"2025-08-13","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q4 營收 $88.4B、年增約5.5%；U.S. Healthcare Solutions 營收 $78.3B、年增5.4%；OneOncology（2026-02收購）提升該段毛利率，GLP-1 銷售增加（毛利較低）部分抵銷。","source":"Cencora FY2026 Q4 8-K Exhibit 99.1 / 新聞稿 (2026-11-04)","url":"https://www.sec.gov/Archives/edgar/data/0001140859/000114085926000038/exhibit991-q42026.htm","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"FY27 指引：營收成長3–5%、調整後營業利益成長4–6%、調整後EPS $19.40–$19.75（+8–10%）；因出售（divestiture）稀釋，標題指引低於市場預期（二手來源）。","source":"finviz: Cencora closes FY26 above raised guidance but a divestiture diluted FY27 outlook resets expectations lower","url":"https://finviz.com/news/415659/cencora-closes-fy26-above-raised-guidance-but-a-divestiture-diluted-fy27-outlook-resets-expectations-lower","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Specialty 段 FY27 營收成長 9–14%、營業利益成長 18–21%；PDS 營業利益成長 2–4%","source":"Finchannel: Cencora earnings rise as specialty growth reshapes 2027 outlook","url":"https://finchannel.com/cencora-earnings-rise-as-specialty-growth-reshapes-2027-outlook/140504/american-business-trends/2026/11/","excerpt":"Cencora expects specialty-segment revenue growth of 9%–14% and operating-income growth of 18%–21%. Those forecasts include the continuing contribution from OneOncology, acquired in February 2026.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"2026年6月 PharmExec 報導：製造商直接對病患（DTP）配銷已從試點變成策略優先項目，潛在繞過傳統批發通路","source":"PharmExec: rise of direct-to-patient models, bypassing traditional distribution channels","url":"https://www.pharmexec.com/view/rise-direct-to-patient-models-pharma-opportunities-risks-bypassing-traditional-distribution-channels","excerpt":null,"as_of":"2026-06-25","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Drug Channels 2026年10月：三大批發商2026年藥品配銷營收預估 $933 billion，且持有 MSO 保護其通路角色","source":"Drug Channels: 10 crucial trends facing US drug channels","url":"https://www.drugchannels.net/2026/10/10-crucial-trends-facing-us-drug.html?m=0","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Cencora 重整營運模式，自 FY2027 Q1 起改報 Pharmaceutical Distribution and Services、Specialty Pharmaceutical and Provider Services、Other 三組；MWI Animal Health、Profarma、PharmaLex 等列入策略選項檢討","source":"SEC EDGAR 8-K（2026-11-04）","url":"https://www.sec.gov/Archives/edgar/data/0001140859/000114085926000040/abc-20261104.htm","excerpt":"Beginning in the first quarter of fiscal 2027, the Company’s reporting structure will be comprised of Pharmaceutical Distribution and Services, Specialty Pharmaceutical and Provider Services, and Other.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Cencora 策略轉向專科藥、AI 與醫師診所網絡；傳統配送受藥價改變、生物相似藥轉換與客戶採購模式演變壓力","source":"Distribution Strategy Group：Cencora Doubles Down on AI, Specialty Care and Physician Networks","url":"https://distributionstrategy.com/2026/06/cencora-doubles-down-on-ai-specialty-care-and-physician-networks-as-growth-strategy-evolves/","excerpt":"Cencora Doubles Down on AI, Specialty Care and Physician Networks as Growth Strategy Evolves Timon – stock.adobe.com","as_of":"2026-06-05","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ3（2026-08-05）公司把 FY2026 調整後 EPS 指引上調至 $17.75–$17.95（原 $17.70–$17.90）；營收成長 4–6%、調整後營業利益成長 13–14% 維持，調整後自由現金流約 $3B。","source":"Cencora 8-K Q3 FY2026 exhibit 99.1 / MyChesCo","url":"https://www.sec.gov/Archives/edgar/data/0001140859/000114085926000032/exhibit991-q32026.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"指引中點約 $17.85，與市場共識 EPS（$17.79–$17.85，來源間略有差異）大致持平，無明顯落差；5 月曾下修營收成長指引至 4–6%，股價當日跌 17.4%。","source":"MarketBeat FY2026 earnings guidance 2026-08-14 / Barchart","url":"https://www.marketbeat.com/instant-alerts/cencora-nysecor-releases-fy-2026-earnings-guidance-2026-08-14/","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"最近一則有日期的目標價動作：Baird 於 2026-10-12 把目標價由 $370 調至 $373、評等 outperform；同文列共識目標價約 $365.69、評等 Moderate Buy。","source":"MarketBeat analyst alert 2026-10-12","url":"https://www.marketbeat.com/instant-alerts/analyst-cencora-nyse-cor-price-target-raised-to-37300-2026-10-12/","excerpt":null,"as_of":"2026-10-12","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Barchart 報 14 位分析師中 11 Strong Buy、3 Hold，平均目標價 $349.46；StockAnalysis 12 個月目標價 $353.5。兩者抓取日期未標示，與 MarketBeat 的 $365.69 並存，來源間分布不一致。","source":"Barchart earnings preview / StockAnalysis COR","url":"https://stockanalysis.com/stocks/COR/","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Cencora 2026-01 簽訂定期貸款，為收購其尚未持有的 OneOncology 多數股權融資；交易於 2026-02-02 生效（持股約由 35% 升至 92%，聚合來源）。","source":"SEC EDGAR 8-K（2026-01-16, Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1140859/000110465926004524/tm263332d1_8k.htm","excerpt":"in connection with the previously announced proposed acquisition (the “Acquisition”) of the majority of the outstanding equity interests that the Company does not currently own in OneOncology.","as_of":"2026-01-16","retrieved_at":"20261108","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-05-06 公司下修財測後股價單日跌 17.3%，Rosen、Pomerantz 等律所宣布調查潛在證券詐欺請求（調查公告，非已提起之集體訴訟）。","source":"Barchart／AccessNewswire：Rosen Law Firm、Pomerantz 調查公告","url":"https://www.barchart.com/story/news/1967631/rosen-law-firm-encourages-cencora-inc-investors-to-inquire-about-securities-class-action-investigation-cor","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"鴉片類藥物訴訟：第三方付款人與醫院集體和解 2025 年生效／獲最終核准。","source":"SEC EDGAR 10-K FY2025 Note 12","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"The settlement became effective on April 4, 2025.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"收購 OneOncology 多數剩餘股權，2026-02-02 生效；以新債融資。","source":"SEC EDGAR 8-K（2026-01-16, Item 1.01）","url":"https://www.sec.gov/Archives/edgar/data/1140859/000110465926004524/tm263332d1_8k.htm","excerpt":"in connection with the previously announced proposed acquisition (the “Acquisition”) of the majority of the outstanding equity interests that the Company does not currently own in OneOncology.","as_of":"2026-01-16","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-05 股價大跌後多家律所宣布調查證券詐欺請求；搜尋未見已提起之證券集體訴訟。","source":"Barchart：Rosen Law Firm 調查公告","url":"https://www.barchart.com/story/news/1967631/rosen-law-firm-encourages-cencora-inc-investors-to-inquire-about-securities-class-action-investigation-cor","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"鴉片類藥物醫院集體和解於 2025-04-04 生效。","source":"SEC EDGAR 10-K FY2025 Note 12","url":"https://www.sec.gov/Archives/edgar/data/1140859/000114085925000131/cor-20250930.htm","excerpt":"The settlement became effective on April 4, 2025.","as_of":"2025-11-25","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"COR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":4.12,"operating_margin_pct":1.44,"fcf_margin_pct":0.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CAH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":3.9,"operating_margin_pct":1.26,"fcf_margin_pct":1.9,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MCK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":3.67,"operating_margin_pct":1.67,"fcf_margin_pct":1.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HSIC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.59,"operating_margin_pct":5.79,"fcf_margin_pct":3.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"COR"},"financial_history":{"ticker":"COR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-09-30","revenue":238587006000.0,"revenue_yoy_pct":null,"gross_margin_pct":3.48,"operating_margin_pct":1.15,"net_income":1698820000.0,"diluted_eps":null,"free_cash_flow":2206770000.0,"fcf_margin_pct":0.92,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-09-30","revenue":262173411000.0,"revenue_yoy_pct":9.89,"gross_margin_pct":3.42,"operating_margin_pct":1.02,"net_income":1745293000.0,"diluted_eps":8.53,"free_cash_flow":3452975000.0,"fcf_margin_pct":1.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":293958599000.0,"revenue_yoy_pct":12.12,"gross_margin_pct":3.37,"operating_margin_pct":1.07,"net_income":1509120000.0,"diluted_eps":7.53,"free_cash_flow":2997512000.0,"fcf_margin_pct":1.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":321332819000.0,"revenue_yoy_pct":9.31,"gross_margin_pct":3.57,"operating_margin_pct":1.22,"net_income":1554169000.0,"diluted_eps":7.96,"free_cash_flow":3207139000.0,"fcf_margin_pct":1.0,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/COR/COR_Q4_2026_Earnings_Call_20261104.md）

# Q4 2026 Earnings Call
**Cencora, Inc.** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to the Cencora, Inc. Fiscal 2026 Fourth Quarter Earnings Call. [Operator Instructions] I will now hand the conference over to Bennett Murphy. Bennett, please go ahead.

**Bennett Murphy** (Executives):
Good morning, good afternoon, and thank you all for joining us for this conference call to discuss Cencora's fiscal 2026 Fourth Quarter and Full Year Results. I am Bennett Murphy, Senior Vice President, Investor Relations and Enterprise Productivity. Joining me today are Bob Mauch, President and CEO; and Eva Boratto, Executive Vice President and CFO. On today's call, we will be discussing non-GAAP financial measures. Reconciliations of these measures to GAAP are provided in today's press release, which is available on our website at investor.cencora.com. We've also posted a slide presentation to accompany today's press release on our investor website. Alongside these materials, we are providing recast financials in our new segments for fiscal 2025 and fiscal 2026 in a Form 8-K that will also be available on our Investor Relations website. 
During this conference call, we will discuss forward-looking statements about our business and financial expectations on an adjusted non-GAAP basis, including, but not limited to, EPS, operating income and income taxes. Forward-looking statements are based on management's current expectations and are subject to uncertainty and change. For a discussion of key risks and assumptions, we refer you to today's press release and our SEC filings, including our most recent 10-Q. Cencora assumes no obligation to update any forward-looking statements, and this call cannot be rebroadcast without the permission of the company. You have an opportunity to ask questions after today's remarks by management. We ask you limit your questions to one per participant in order for us to get to as many as possible within the hour. With that, I'll turn the call over to Bob.

**Robert Mauch** (Executives):
Thank you, Bennett. Hi, everyone, and thank you for joining Cencora's fiscal 2026 Fourth Quarter and Full Year Earnings Call. I want to begin by thanking our team members. Throughout the fiscal year, their commitment to our purpose and dedication to our customers fueled our performance as we delivered adjusted operating income growth of 14% and adjusted diluted EPS of $17.97, up 12%. Our fiscal 2026 performance demonstrates the strength of our business and the progress we've made with leadership in specialty and a portfolio increasingly aligned to the areas where we can create the greatest long-term value. We enter fiscal 2027 with momentum and greater operational and strategic focus. The outlook reflects our confidence and is aligned with our long-term targets when excluding the businesses and Other. 
This morning, I will focus on 2 areas: the strategic progress delivered in fiscal 2026 and how our updated operating model will strengthen execution, customer focus and visibility for investors. I'll begin with the strategic progress delivered in fiscal 2026. Two years ago, we introduced a refined strategy to lead with market leaders, strengthen our position in specialty and enhance patient access to pharmaceuticals. In fiscal 2026, we advanced each priority, delivered another year of record results and expanded capabilities that support patient access to innovation in the specialty pharmaceutical market, where growth has been twice that of the broader market over the past 5 years. 
Our MSO platform is one important example. In February, we completed our acquisition of OneOncology, expanding our position in one of health care's fastest-growing areas. Together, OneOncology and Retina Consultants of America deepen our relationships with community-based specialists and strengthen our ability to support pharmaceutical-centric care closer to where patients live. During the fiscal year, we continued to build the MSO platform, including the announced acquisition of EyeSouth's retina business in March and most recently, our agreement to acquire a majority interest in American Oncology Network. These additions will expand the capabilities and reach of a platform built to help independent specialty practices thrive, improve patient access to high-quality care and create opportunities to support pharmaceutical companies across the product life cycle. 
In fact, at RCA, we participate in the vast majority of retina clinical trials, completing over 40,000 research-related visits annually, and OneOncology has supported more than 130 pharmaceutical partners with their clinical trials to date. As we've invested in the businesses aligned with our pharmaceutical-centric strategy, we've also taken decisive action on businesses that do not align, concentrating our capital and leadership attention where Cencora is most differentiated. Over the course of the year, we entered into agreements or completed divestitures for all the businesses within other. While these actions can cause near-term financial headwinds, they allow us to direct our resources towards the areas where we can create the greatest value for customers and shareholders over the long term. The same discipline guiding our portfolio informs how we operate. This morning, we introduced an updated operating model aligned with our strategy and the customers we serve. Our pharmaceutical-centric strategy is focused on strengthening our leadership in specialty and delivering greater value across pharmaceutical services. 
As the needs of manufacturers and providers evolve, we're adapting our organization to better support them while preserving the benefits of Cencora's scale, infrastructure and expertise. I believe this operating model will make Cencora more effective in 3 ways: enhancing our strategic and operational execution, further elevating the voice of our customers and providing increased visibility for our shareholders. Informed by our updated operating model, we've created 2 new reporting segments. Specialty Pharmaceutical and Provider Services brings together our specialty capabilities in an integrated growth platform, supporting innovation from pharmaceutical manufacturers to physician providers. 
Pharmaceutical Distribution and Services organized around our broad portfolio of customers and the services we provide, while leveraging our scale to deliver sustained growth and strong cash flow generation, powering investments across the enterprise. Now I'll share a bit more about each segment. Starting with Specialty Pharmaceutical and Provider Services. We are connecting capabilities across clinical trial logistics, commercialization, specialty distribution, GPO and practice management to support innovative therapies from development to delivery to patient. That role is becoming more important with specialty biologics now accounting for more than half of all pharmaceutical spending in the United States, up 80% in 5 years. 
With over 100 new products expected to launch through 2030, oncology illustrates the growing need for specialized clinical logistics, distribution and provider support as the pipeline expands and therapies become more complex. These are capabilities Cencora has built at scale through focused investments with specialty logistics operations across more than 50 countries and multinational 3PL solutions in the United States and Europe. We can support pharmaceutical partners as they bring complex therapies to patients across markets. Our role does not end when a therapy reaches its destination. As more specialty care is delivered in community settings, providers are managing increasing clinical and administrative demands. Through our MSOs, we help independent specialty physicians, manage clinical and administrative complexity, expand access to research and remain focused on patient care. 
Our agreement to acquire a majority interest in AON extends the platform through a physician-led network and a long-standing Cencora partner. Bringing these businesses together deepens our relationships with manufacturers and providers while giving investors a clearer view of the growth potential of our specialty platform. Within pharmaceutical distribution and services, our scale provides us with deep understanding of trends across the health care ecosystem, which we use to drive differentiated value to customers. We deliver over 100 million packages annually, shipping nearly 5 million units each day, giving our leaders firsthand insight into the needs of manufacturers, providers, pharmacies and patients. 
Combining our scale, our sourcing expertise and customer-centric partnerships with pharmacies and health systems, large and small, we strengthened their operations, support their growth and ensure continued patient access. Two recent customer events illustrate how the perspective shape our priorities. At our Health Systems National Summit, health systems leaders discussed how connecting pharmacy, supply chain, technology and care delivery leads to better decisions for patients and their organizations. These are all areas where our Accelerate Pharmacy solutions help our health systems customers. At ThoughtSpot, our annual trade show for good neighbor independent pharmacies, we came together with more than 3,000 attendees, introducing novel solutions, including AI-powered tools designed to help pharmacies run more efficiently, free up time for patient care and create new growth opportunities. 
At both our Health Systems National Summit and ThoughtSpot, I heard customers emphasize that specialty is becoming a larger and more complex part of patient care, reinforcing the importance of specialty growth and solutions across both reporting segments. The scale of this opportunity is increasingly visible in our results. We expect specialty distribution revenue to reach approximately $100 billion in fiscal 2027. Combined with our broader manufacturer and provider capabilities, this makes specialty a central driver of Cencora's long-term growth. In summary, we exit fiscal 2026 with record results and a stronger platform for growth, supported by our scale, specialty capabilities and an operating model aligned to how we create value. With that, I'll turn the call over to Eva to discuss our fourth quarter and fiscal 2026 results as well as our fiscal 2027 guidance. Eva?

**Eva Boratto** (Executives):
Thanks, Bob. Good morning, everyone. As Bob highlighted and we shared in our press release this morning, we have introduced a new organizational and financial reporting structure designed to strengthen our execution and provide additional performance visibility to our shareholders. Through our new segments, we will highlight the significant opportunity we have to utilize our end-to-end specialty capabilities to deliver value up and downstream while driving sustainable growth powered by our scale and efficient pharmaceutical distribution foundation. 
In addition to reiterating Cencora's long-term growth algorithm of 7% to 10% operating income growth and 10% to 14% EPS growth, we are introducing targets for our new segments. For the Pharmaceutical Distribution and Services segment, we expect long-term operating income to grow in the mid-single digits. And for the Specialty Pharmaceutical and Provider Services segment, we expect long-term operating income growth in the mid-teens. Now I'll provide an overview of our fiscal 2026 fourth quarter and full year results and our fiscal 2027 financial guidance. Unless otherwise stated, my remarks will focus on adjusted non-GAAP financial results. For further discussion of our GAAP results, please refer to our earnings press release and presentation. 
Beginning with fourth quarter, consolidated revenue was $88.4 billion, up 6%, driven by growth in both reportable segments and in Other, which I'll describe in more detail when discussing segment level results. Consolidated adjusted gross profit was $3.6 billion, up 23%, primarily due to growth in the U.S. Healthcare Solutions segment. Consolidated adjusted gross margin expanded by 57 basis points to 4.04%, largely due to our acquisition of OneOncology in February. Consolidated adjusted operating expenses were $2.3 billion, an increase of 23%, again, largely driven by the impact of the February 2026 acquisition of OneOncology. Excluding both OneOncology and RCA, operating expense growth was less than 3% as we lapped an easier expense comparison. 
Consolidated adjusted operating income was $1.2 billion, an increase of 22% compared to the prior year quarter, with another quarter of double-digit growth across both reportable segments and other. Moving now to below-the-line items. Net interest expense was $136 million, an increase of $58 million compared to the prior year quarter, primarily due to debt raised to finance the OneOncology acquisition. Our effective tax rate was 20.2% compared to 20.6% in the prior year quarter. Finally, diluted share count was 191.7 million shares, a 1.8% decrease compared to the prior year quarter, largely due to the $1 billion of opportunistic share repurchases we completed in the June quarter. Taken together, this resulted in adjusted diluted earnings per share of $4.66, an increase of 21%. 
Turning to our segment results for the fourth quarter. U.S. Healthcare Solutions revenue was $78.3 billion, an increase of 5%. Strength in specialty sales to health systems and physician practices and continued growth in GLP-1s, which increased by $2.8 billion year-over-year, drove the growth. The growth was partially offset by manufacturer list price reductions that represented a $2.8 billion headwind to revenue growth as well as lower sales to our large mail order customer, consistent with the past 2 quarters. U.S. Healthcare Solutions segment operating income was $998 million, up 22%, representing our strongest growth quarter of the fiscal year. This was driven by continued momentum in specialty across both health systems and physician practices, the contribution from OneOncology and focused execution across our other pharmaceutical distribution businesses. 
The quarter also benefited from an easier expense comparison. Turning now to our International Healthcare Solutions segment. Revenue was $7.8 billion, up 5%, driven by growth in all business units. International Healthcare Solutions operating income was $152 million, up 16% on an as-reported basis and up 19% on a constant currency basis. In the quarter, our Canadian business delivered excellent performance driven by high program win rates. Our global specialty logistics and 3PL business continued to drive strong performance with double-digit operating income growth. As Bob mentioned, we have been investing in these businesses to capitalize on the increasing complexity in the innovation pipeline and have been winning in these areas. 
Moving to Other, which reflects the businesses for which we are pursuing strategic alternatives. Revenue in Other was $2.3 billion, up 10%, largely due to growth at Profarma and MWI Animal Health. Operating income was $101 million, up 36% due to operating income growth at MWI Animal Health, also including the benefit from being accounted for as held for sale. This completes the review of our fourth quarter results. Now I'll turn to a discussion of our full year fiscal 2026 results. Our consolidated revenue was $337 billion, up 5%, driven by U.S. Healthcare Solutions segment growth of 5% and International Healthcare Solutions segment growth of 8%. Consolidated operating income was $4.8 billion, an increase of 14%, driven by growth in both reportable segments. 
In the U.S. Healthcare Solutions segment, we benefited from strength in specialty volumes and our strategic investments in MSOs. In the fiscal year, MSOs represented approximately 10% of enterprise operating income. When excluding the impact of our 2 large MSO acquisitions and the loss of an oncology customer, our core U.S. segment growth was about 13%, nicely ahead of our long-term growth algorithm. In the International Healthcare Solutions segment, we were pleased with the business' return to growth this fiscal year, driven by operational improvements at our Global Specialty Logistics business and increased demand. 
Finally, as it relates to free cash flow and our balance sheet, during the fiscal year, we generated $3.8 billion of adjusted free cash flow, stronger than our guidance due to a combination of year-end stronger volume, mix and timing. We ended the year with a cash balance of $4.9 billion. Our strong free cash flow generation gives us significant flexibility to pursue our balanced capital deployment strategy while maintaining our strong investment-grade credit ratings. During the fiscal year, we were pleased to return $1.5 billion to shareholders through a combination of opportunistic share repurchases and our dividend. And this morning, we announced a 10% increase to our quarterly dividend, our 22nd consecutive increase. 
Turning now to our fiscal 2027 expectations. There are a few items I'll highlight before we get into the details of our guidance. First, our guidance excludes the acquisitions of EyeSouth retina business and American Oncology Network, which we will incorporate upon the close of each transaction. Second, our guidance contemplates a mid-fiscal year close of the MWI merger with Covetrus. The operating income headwind is expected to be partially offset by 2 below-the-line income items associated with the transaction, which would be approximately $40 million in the second half of fiscal 2027. This contribution is expected to bring our other income loss line to approximately $90 million compared to the approximate $26 million in fiscal 2026. 
Third, as we announced this morning, we reached an agreement to sell our equity stake in Profarma with the close expected to occur in our fiscal first quarter. Given the nature of our ownership, we consolidate the full Profarma income statement and eliminate our noncontrolling interest in the company, making it a much less meaningful contributor at the EPS level, which is fully reflected in our revenue, operating income and EPS guidance. With that as context, we expect adjusted diluted EPS to be in the range of $19.40 to $19.75, reflecting headline growth of 8% to 10%, excluding the assumed $0.35 impact of the mid-fiscal year merger of MWI and Covetrus, adjusted EPS growth would be 10% to 12%. We expect consolidated revenue growth to be in the range of 3% to 5%. 
Operating income growth is expected to be in the range of 4% to 6%. The businesses in Other are expected to have an approximate 5 percentage point negative impact on our growth, largely due to the assumed mid-fiscal year closing of the merger of MWI and Covetrus. Excluding the businesses in Other, our guidance would reflect adjusted operating growth of 8.5% to 11%, ahead of our long-term targets. We expect interest expense to be in the range of $490 million to $510 million, reflecting debt we raised in connection with the OneOncology transaction. We expect to pay $1 billion on the remaining OneOncology term loan at the end of fiscal year 2027. 
We expect our effective tax rate to be approximately 20% for fiscal 2027. We expect full year diluted average shares outstanding to be approximately 190 million shares. This reflects the annualization of opportunistic share repurchases we completed in the third quarter of fiscal 2026 and an expectation of an additional $1.25 billion in repurchases in fiscal 2027. We expect capital expenditures to be approximately $1 billion in fiscal 2027, which reflects continued investments in our supply chain, digital and MSO infrastructure. We expect adjusted free cash flow to be approximately $3.5 billion. That completes the review of our consolidated fiscal 2027 expectations. I'll now turn to segment level expectations. 
In the Pharmaceutical Distribution and Services segment, we expect revenue growth to be in the range of 4% to 6%. We expect Pharmaceutical Distribution and Services segment operating income growth to be 2% to 4%, which includes the wraparound impact of a certain customers' volume shift as previously disclosed. The segment operating income growth expectations also include an approximate $20 million headwind related to our European distribution business resulting from the strengthening of the U.S. dollar. Moving now to the Specialty Pharmaceutical and Provider Services segment. We expect revenue growth to be in the range of 9% to 14% and segment operating income growth to be in the range of 18% to 21%, ahead of our segment-level long-term operating income growth expectations of mid-teens, reflecting the wraparound contribution from the OneOncology acquisition that we closed in February 2026. 
Moving now to Other. We expect revenue in other to be approximately $3.5 billion and operating income in Other to be approximately $200 million. We are pleased with the significant progress we have made to simplify our portfolio, allowing us to better capitalize on growth opportunities aligned with our pharmaceutical-centric strategy. Before turning to my closing remarks, as you think about quarterly cadence, we expect adjusted diluted EPS in our first quarter to be approximately $4.55. In closing, fiscal 2026 marked a year of significant progress on our strategy as we delivered strong financial performance. As we look to fiscal 2027 and beyond, we are well positioned to deliver on our long-term targets and drive sustainable shareholder value creation, supported by our differentiated footprint in the high-growth specialty market, scaled and efficient foundation in pharmaceutical distribution and strong free cash flows. I'll turn the call back to Bob for some closing remarks before moving to Q&A. Bob?

**Robert Mauch** (Executives):
Thank you, Eva. Our fiscal 2027 guidance reflects our confidence in the strength of the business in our team, our strategy and our ability to deliver sustainable growth and long-term value for customers and shareholders. With that, we'll open the call for questions. Operator?

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Elizabeth Anderson with Evercore ISI.

**Elizabeth Anderson** (Analysts):
Thanks for all the details about the operating performance. I guess my question is maybe a little bit more philosophical in nature. Can you talk a little bit more about like why the resegmenting at this point makes sense? You've obviously had many specialty assets on the medical side for a while, but why is this the right opportunity to kind of do that? And what does that provide for the business that the old setup did not?

**Robert Mauch** (Executives):
Elizabeth, thank you very much for that important question. It starts with the market. As you mentioned, we've been in the specialty market for a long time. We have significant capabilities that we've been building over decades, frankly. But when you look at the growth in the market, the 80% growth that's happened in biologics over the last 5 years. In fact, there's going to be 100 new oncology products between now and 2030. That says to us that we need to be even more focused on that area. And so the first place to start there is our operating model and the way that we approach our business, the way that we approach our customers, both upstream to manufacturers and downstream to providers. 
And while we did that very well, our specialty services assets were in different parts of the company and under different leaders. And so what we've done with the operating model change is taken all of those assets and put them under one leader. By doing that, that allows us to discuss a new external segmentation, but it's driven by optimizing our performance. The 3 things that I called out in prepared remarks that are advantages that I see is one, which I just mentioned, is our enhanced ability to execute both strategically and operationally. It brings us closer to the customers for all of the reasons that I just described. And last but not least, it provides increased visibility to shareholders, which we also think is important. 
So the Specialty Pharmaceutical and Provider Services business puts everything under one leader, as I said, all the way from manufacturer to physician, and they deal with one team at Cencora, which will make things easier and faster for the customers. It will also allow us to innovate even more quickly, which will be important as we go into the future and as products get more and more complex. Importantly, our Pharmaceutical Distribution and Services segment, that's the foundation of all of this. It's servicing health systems, pharmacies, alternate sites, wholesale and Europe with significant scale, demonstrated efficiency over decades and cash flow that allows us to invest across the enterprise. So while we are separating the 2, it's an important takeaway for everyone that both are critically important to the growth platform of Cencora. So I think that's the rationale, Elizabeth. I appreciate the question, and we're excited to be able to talk about it today.

**Operator** (Operator):
Your next question comes from the line of Lisa Gill with JPMorgan.

**Lisa Gill** (Analysts):
Bob, I want to follow up on specialty just from a couple of different perspectives. One, I absolutely appreciate the visibility that you're giving us and shareholders around the specialty business. And clearly, this is an important growth engine as we move forward. I want to understand really a couple of things. One, when we think about specialty going into next year, Eva laid out the numbers. Can you talk about what the organic growth rate is? I know there's a number of transactions that impact the number. And then secondly, you talk about health systems, you talked about the MSO, community practices, et cetera. How do you think about changes in reimbursement and the impact that, that has in '27 or even on a go-forward basis, we obviously had a big election last night. Any incremental thoughts on how you see the future around reimbursement and any impact it would have on you as you continue to serve these -- from a specialty perspective, serving these practices?

**Robert Mauch** (Executives):
Thanks, Lisa, for the question. Yes, but maybe I'll start with the end. And as you mentioned, we did have an election last night. It's most important to note that through multiple cycles of administrations and leadership in Congress and leadership in the regulatory agencies, we have a long history of advocacy and making sure that Cencora is present and educating everyone about the services that we provide, the value, the very high-quality, low-cost services that we provide at Cencora. But also importantly, we have visibility end-to-end to the pharmaceutical supply chain. So we're someone who can advise on what the outcomes might be, the consequences might be of any policy changes. 
So the way things look today, there'll be lots of opportunity for conversations as we get the new Congress and Senate in place, and we'll be right there to help them with that. I think a second piece, Lisa, is just the overall scale of our specialty business. And we broke out the specialty pharmaceutical and provider services, but it's also important to note that there's significant specialty distribution products that go into the pharmaceutical distribution and services segment. 
So the number that we had in our prepared remarks that more than $100 billion is the combination of the 2. So we -- very importantly, whether an oncology product, for example, is going into a community specialist setting or it's going into a clinic within a health system, Cencora is very well positioned to support that patient wherever they may present and support that clinician in caring for that patient. So I'll pause there and hand it over to Eva to ask the other part of your question -- answer the other part of your question.

**Eva Boratto** (Executives):
Sure. Lisa, the Specialty and Pharmaceutical Distribution and Provider Services segment, as you saw in our materials, expected operating income growth of 18% to 21%. That's above our long-term growth algorithm. And I would remind you, we have the wraparound of OneOncology for the first 4 months of the fiscal year. So outside of that impact, our underlying growth would have been in line with our algorithm of mid-teens growth that we outlined today.

**Operator** (Operator):
Your next question comes from the line of Glenn Santangelo with Barclays.

**Glen Santangelo** (Analysts):
I also wanted to follow up on specialty. Bob, when I think about that mid-teens sort of long-term growth rate in specialty and in your prepared remarks, you just suggested there's 100 new oncology products coming between now and 2030. So is it really volumes that are the primary driver of that mid-teens growth? I just want to separate organic from inorganic. And then just sort of related to that, you generated a 3.7% margin in specialty this year. Maybe help us think about the puts and takes on that margin given all the upcoming biosimilar conversions?

**Eva Boratto** (Executives):
Sure, Glen. It's Eva. I'll start in the Specialty Pharmaceutical and Provider Services. First, if you take a step back, this segment consists of end-to-end specialty businesses from our specialty distribution to practice management platforms to global clinical trials, multinational 3PL businesses. So that's what's encompassed in that segment. And as you think about our long-term growth algorithm of mid-teens, one, it reflects the fast-paced growth in the market and as Bob outlined; two, continued growth at our MSOs through both organic physician acquisition as well as tuck-in M&A on these platforms.

**Operator** (Operator):
Your next question comes from the line of Charles Rhyee with TD Cowen.

**Charles Rhyee** (Analysts):
Maybe I could ask the other side in the pharmaceutical distribution and services. In the assumptions you kind of give for long-term segment growth, can you talk about how you're thinking about the cycle of small molecule generics coming over the next several years? How much do you incorporate that? And obviously, small molecule generics were a huge driver of growth back in the 2000s and the 2010. When we look at this next cycle coming up, it looks significantly bigger in terms of dollar volumes. Maybe you could help us understand, have there been changes in that part of the market that should either make us be more excited, maybe we should be a little bit more cautious on it? Just trying to get a better sense on the dynamics in this part, given what looks to be a big cycle, particularly as we get to the back half of next calendar year. Any comments there on helping us size that would be helpful.

**Robert Mauch** (Executives):
Thanks for the question, Charles. I'll start and I'll hand it to Eva if she wants to add anything as I finish up. So I think, just take a step back, whether it's a small molecule generic or whether it's a biosimilar, we keep a very close eye on all of those. Those launches of both types would be contemplated in our guidance. But I think the takeaway is just a reminder that, that's positive for Cencora. So whether it's a small molecule generic or biosimilar, that's positive. They're different in different segments. The Part B biosimilar is the sweet spot for us. That's where the services that we provide allow us to earn a higher margin. Within Part D, it's much less impactful. That would be a revenue impact and not really a profit gain. 
And oral generics, small molecule oral generics are positive. They absolutely are. So to the extent that we have more or less launches, that has an impact. But you'll note, Charles, not -- you mentioned the historical driver of generic launches. They're not that. So we're not calling either a significant increase or a decrease in launches as a driver of our performance. So I think the takeaway is that the assumptions are contemplated in our guidance, and we keep a very close eye on it.

**Operator** (Operator):
Your next question comes from the line of Allen Lutz with Bank of America.

**Allen Lutz** (Analysts):
Bob, you spoke a lot about upstream services in your prepared remarks. RCA and OneOncology are active in clinical trials. You also own the World Courier business. Could you take a moment to expand on the synergies between those 2 businesses? And then more broadly, as we think about the resegmentation, how should we think about capital deployment and the strategy? Is there any evolution here as you've done that resegmenting?

**Robert Mauch** (Executives):
Yes. Thanks for the question, Allen. I'll speak to strategic synergy. Part of the purpose of bringing those businesses together was to be more effective, to be more efficient, and I'm sure some of that will come. But that's not the financial synergy was not necessarily the thesis for putting them together. It's really a growth thesis. And what we have, as you said, so if you take the pharmaceutical company facing view, we have the very specialized global logistics to support them and clinical trials. We have commercialization consulting services that can help them think about how they're going to bring their product to market in multiple countries as they're getting ready to launch. 
We have 3PL services that are going to be important as they launch in Europe. And then we have our specialty distribution and full-line distribution in the United States. And then as that continues to go downstream, as I follow that through, then you have -- as I kind of transition from specialty distribution, you have the GPO, you have the MSO, all of that supporting the physician. And the purpose of all of that is to make sure that the physician has optimal opportunity to care for patients, to make the right clinical decisions and to care for patients. So there's a strong thesis there of value from the manufacturer all the way to the provider and to the patient. And the purpose of putting these businesses together inside the Specialty Pharmaceutical and Provider Services segment is for us to continue to build that platform and innovate over the long term.

**Eva Boratto** (Executives):
And Bob, I'll take the capital allocation part of the question. I would say there is no change in our capital deployment strategy. We remain focused in 4 key areas: internal investments in the business, strategic M&A, opportunistic share repurchases and maintaining a reasonable and growing dividend. And I think you've seen us deliver on that this morning, we announced we're increasing our dividend 10% for fiscal year 2027 and $1.25 billion in share repurchases. And I think the portfolio optimization that's been done with some of the divestitures will enable us to execute on these priorities.

**Operator** (Operator):
Your next question comes from the line of Eric Percher with Nephron Research.

**Eric Percher** (Analysts):
I want to dig a little bit deeper into the Pharma Distribution and Services new segmentation, and thank you for that segmentation. So in '27, 4% to 6% growth, we would assume that there is a headwind from IRA and GLP-1s. And then seeing the op profit growth at 2% to 4% I think we've been taught by you that the reductions to top line don't necessarily translate at the op profit line. But can you just help us on the factors impacting top line versus the op profit headwinds we're seeing for '27 specifically?

**Eva Boratto** (Executives):
Yes. Sure, Eric. As you see -- I'm going to start at the op profit line. As you look at the 2% to 4% growth being below the long-term algorithm that we provided today, I would highlight 2 things. One, we have the wraparound impact of a customer volume shift that we talked about earlier in the year as well as about 1 point impact from FX now that our international distribution is part of that segment. Outside of those impacts, we expect to perform within our long-term targets. 
On your revenue question, I'm going to go to the consolidated revenue at growth of 3% to 5%. What I would say the differentiator as you look at '27 fiscal guidance versus the 5% we delivered in fiscal '26 is really the headwind from the pro forma divestiture that we announced today as well as the assumed midyear merger of Covetrus. And those 2 combined drive about 150 basis point headwind to growth. I'd say the WACC decreases and is pretty comparable is our estimate. You get a little bit more from the wraparound impact, but pretty comparable to what we experienced in '26.

**Operator** (Operator):
Your next question comes from the line of Erin Wright with Morgan Stanley.

**Erin Wilson Wright** (Analysts):
So a competitor of yours recently announced a transaction in the infusion space with Option Care. I guess, is that an area that is interested to you? Did you look at that asset? How do you think about, I guess, other areas outside of oncology and retina? I mean you're really weighing in on oncology, obviously. But are you still entertaining those other ideas? Or how do you think about that in terms of the context of what you were just talking about from a capital deployment standpoint?

**Robert Mauch** (Executives):
Thanks very much for the question. I'll start with where it's clear that we are focused because I do want to emphasize that. We've made it very clear that we're going to be focused in expanding our specialty capabilities. We've made it clear that we're going to focus our portfolio in areas that we can create long-term customer and shareholder value. And you're seeing us do that. That is our investments in the MSOs, the builds of the MSOs that we're doing, and we're going to continue to do that. It's important to note something that we've said a few times, which is our pharmaceutical-centric strategy keeps us focused in the MSO space on -- right now on oncology and retina. 
And we don't see other therapeutic areas as areas that would be pharmaceutical-centric and therefore, would have us interested in expanding into a different MSO outside of those 2. Getting to your question, which is infusion specific, we support infusion customers across our portfolio. We have that in our health systems business, we support infusion customers. We expect to continue to support them as customers, but that doesn't mean that we need to own that capability. We're a strong provider to them, and we'll continue to do that.

**Operator** (Operator):
Your next question comes from the line of George Hill with Deutsche Bank.

**George Hill** (Analysts):
I'm going to delve a little bit more into the new Specialty segment a little bit. I'm wondering if there's a chance that you guys would either -- would tell us maybe the dollar percentage contribution from like the MSO segment versus wholesaling versus GPO. Would you talk at all about -- are there any significant margin differences by therapeutic category? And should we think of like what is a target margin profile for this segment given that operating earnings growth is expected to outpace revenue growth in the long-term algo?

**Eva Boratto** (Executives):
George, it's Eva. So on your first question around breaking out the MSO contribution, for 2026, we indicated the MSOs were about 10% of our consolidated operating income. So that should give you a framework to think about that. On the margin side, right, our specialty is our higher margin, higher growth business. I would point out that it's not just the specialty distribution. We have the World Courier, the 3PL, the MSOs and the consulting businesses in there. So they're carrying a higher margin profile. And I'd remind you that we consolidate RCA, so think about that as additive to margin.

**Operator** (Operator):
Your next question comes from the line of Eric Coldwell with Baird.

**Eric Coldwell** (Analysts):
I was hoping for a little more framing on the CapEx. I understand the drivers of the heightened CapEx, the $1 billion target. I'm hoping to put that in context of a figure that is effectively a double or more than a double over the last couple of years. And the 3% to 4% growth in the long-term growth targets, should we read that as start at $1 billion and then grow that 3% to 4% per year thereafter? I assume that's a forward-looking basis. I just want to make sure that there's not a bit of a onetime spike, if you will, in fiscal '27.

**Eva Boratto** (Executives):
Yes. Eric, this is Eva. Regarding our CapEx, as you said, we expect to spend approximately $1 billion. And you're right, the dollar spend is elevated to recent years. As a percentage of gross profit, it aligns with historical periods when we've made significant investments in our infrastructure. So I would just remind you, we're making investments in our U.S. supply chain infrastructure. We're continuing to make investments in IT to support our digital transformation as well as SAP as well as some investments in our MSO. And the 3% to 4% that you're referring to, I believe, is capital deployment. It was not intended to be CapEx growing at 3% to 4%.

**Operator** (Operator):
Your next question comes from the line of Kevin Caliendo with UBS.

**Kevin Caliendo** (Analysts):
Just a couple of things. I just want to understand the inputs into 2027. OneOncology profitability that the run rate that you had for fiscal 4Q, is that the run rate going forward? Did you assume there would be improving OneOncology profitability in fiscal '27 versus the run rate we saw exiting? And then is there anything that you contemplated around Cigna's new sort of wholesale distribution business that they announced? We don't really know exactly what it's going to be, but the perception was it could potentially impact you. I'm wondering if there was anything in when you thought about guidance that was an input relative to that business? And then the last input is the Option Care relationship that you currently have. We don't know when that contract expires, but is there anything built into fiscal '27 for potentially losing the distribution part of the Option Care business, if that's even an issue?

**Eva Boratto** (Executives):
Yes. Thanks for the question. I'm going to go in reverse order, Kevin. On Option Care, you're right, they are Cencora customer and have been for some time. As it relates to the financial impact, I would think about it, it would move us within our guidance range of our Pharmaceutical Distribution and Services segment. Your point on MSOs, OneOncology more specifically, what I would say is, first, I want to reiterate that OneOncology and RCA are both continuing to perform well. They performed well in the quarter. We expect they'll be significant contributors to our specialty growth. They have been in the past, and we look forward to those continuing to grow nicely.

**Robert Mauch** (Executives):
Yes. And Kevin, I would just add, I think your question was how we have thought about kind of our customer relationships in terms of guidance. You mentioned one specific one, but I'll just say that all of our customer relationships are contemplated in our fiscal '27 guidance, and we wouldn't comment any further than that.

**Operator** (Operator):
This concludes the Q&A session. I will now turn the call back to Bob Mauch for closing remarks.

**Robert Mauch** (Executives):
Thank you, operator. Our fiscal 2026 performance demonstrates the strength of our business. We move into fiscal 2027 with significant momentum, and Cencora is focused on execution and advancing our strategy to continue creating long-term value for our customers and shareholders. Thanks, everyone, for your time today.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### COR_Q3_2026_Earnings_Call_20260805.md
- 2026-08-05｜Eva Boratto｜guidance：CFO 上調 FY2026 調整後 EPS 財測至 17.75–17.95 美元（前次 17.70–17.90）（原話："adjusted EPS guidance range to $17.75 to $17.95"）
- 2026-08-05｜Eva Boratto｜guidance：美國營收預期落在 4%–6% 成長區間的下半段（原話："we would expect revenue to be in the"）
- 2026-08-05｜Eva Boratto｜guidance：合併營業利益成長財測下限上調至 13%–14%（原話："now expect growth to be in the range of 13% to 14%."）
- 2026-08-05｜Eva Boratto｜guidance：美國醫療解決方案營業利益成長財測 14.5%–15.5%（原話："income growth to be in the range of 14.5% to 15.5%."）
- 2026-08-05｜Eva Boratto｜guidance：國際部門營收成長降至約 8%（區間低端），原因為下半年美元走強（原話："we now expect revenue growth to be approximately 8%"）
- 2026-08-05｜Eva Boratto｜guidance：全年調整後自由現金流財測約 30 億美元不變（原話："guidance of approximately $3 billion remains unchanged."）
- 2026-08-05｜Eva Boratto｜guidance：FY2027 完整財測將於 11 月財報電話會提供；提供 MWI 與 Covetrus 合併的建模參考（營業利益逆風 1.5 億、EPS 逆風約 0.35 美元，假設年中交割）（原話："would have a $150 million operating income"）
- 2026-08-05｜Eva Boratto｜guidance：EyeSouth Retina 收購時點無更新，不建議納入模型（原話："we would not suggest incorporating that into the models"）
- 2026-08-05｜Eva Boratto｜guidance：Q4 隱含財測為各報告部門強勁雙位數成長；排除 OneOncology 後預期為全年最強有機成長（原話："we expect to"）
- 2026-08-05｜Eva Boratto｜margin：合併毛利率擴張 61bp 至 4.16%，管理層歸因於 2 月收購 OneOncology（原話："expanded by 61 basis points to 4.16%, largely due to our"）
- 2026-08-05｜Eva Boratto｜margin：營業費用成長 27% 反映 OneOncology；排除兩家 MSO 後固定匯率成長 5%（原話："Excluding both MSOs, operating"）
- 2026-08-05｜Eva Boratto｜margin：美國核心業務排除 OneOncology 與流失腫瘤客戶後營業利益雙位數有機成長（上季為 7%）（原話："a meaningful acceleration from the 7% last quarter."）
- 2026-08-05｜Eva Boratto｜margin：Other 部門營業利益成長多數來自待售會計處理，MWI 本身約成長 10%（原話："Underlying MWI delivered about 10% growth and"）
- 2026-08-05｜Eva Boratto｜margin：國際部門歐洲分銷受惠於新興市場國家製造商調價時點，Q4 預期不再有此效應（原話："Now we wouldn't expect that impact in Q4, given some of"）
- 2026-08-05｜Eva Boratto｜margin：OneOncology 因 UUG 子公司非控制權益會計判斷，Q3 起不加回非控制權益損失，對營業利益無影響（原話："we determined that there should not be a"）
- 2026-08-05｜Eva Boratto｜margin：營收口徑：美國營收受 24 億美元廠商降價拖累，GLP-1 年增 23 億美元，另有 2025 年流失腫瘤客戶與大型郵購客戶銷售下降（原話："manufacturer list price"）
- 2026-08-05｜Eva Boratto｜commitment：OneOncology 以 12 個月計、扣除融資後對調整後 EPS 預期中性（原話："we continue to expect OneOncology to be"）
- 2026-08-05｜Eva Boratto｜commitment：已全數償還 RCA 融資相關 8 億美元定期貸款（6 月季 4 億、7 月 4 億）（原話："fully paid off our RCA financing-related term loan balance"）
- 2026-08-05｜Robert Mauch｜commitment：CEO 對 FY2027 不給數字，只重申對長期財測有信心、將落在該區間內（原話："I'm not going to take it any further than that."）
- 2026-08-05｜Robert Mauch｜commitment：CEO 稱下半年成長加速是「機械性、非願景式」，並稱第二季為最低成長季度，進展符合計畫（原話："It was mechanical, not aspirational"）
- 2026-08-05｜Eva Boratto｜commitment：CFO 表示財測哲學為依內部紀律流程設定，並延續交付或超越預期的紀錄（原話："Cencora's long track record of delivering or exceeding"）
- 2026-08-05｜Eva Boratto｜capital_allocation：本季以均價 268 美元回購 10 億美元股票，稀釋股數 1.939 億股（原話："an average price of $268 per share."）
- 2026-08-05｜Eva Boratto｜capital_allocation：CFO 列出資本配置優先順序：內部投資、策略併購、機會式回購、合理且成長的股息，並提到要「增強彈性」（原話："opportunistic share repurchase, as we just did in the"）
- 2026-08-05｜Robert Mauch｜capital_allocation：MSO 投資聚焦於 RCA（眼底）與 OneOncology（腫瘤）的小型併購，不進入其他專科（原話："accretive tuck-in acquisitions within the retina"）
- 2026-08-05｜Eva Boratto｜capital_allocation：利息費用財測上調至約 4.9 億美元，主因 10 億回購減少利息收入；全年稀釋股數約 1.94 億股（原話："primarily reflecting lower interest"）
- 2026-08-05｜Robert Mauch｜product：MSO 價值創造三階段：整合、共享能力（臨床試驗）、開發新服務；管理層稱仍屬早期（原話："3 phases to the value creation thesis"）
- 2026-08-05｜Robert Mauch｜product：RCA 臨床試驗平台已屬成熟後段，OneOncology 仍處早期（原話："In OneOncology, it's in the earlier innings"）
- 2026-08-05｜Robert Mauch｜product：管理層對 Part B 與 Part D 生物相似藥的利潤區分：Part B 因加值服務較多而利潤機會較大，Part D 營收承壓但利潤增幅有限（原話："Part B will always be good"）
- 2026-08-05｜Eva Boratto｜product：GLP-1 銷售成長 25%，管理層稱大致符合預期（原話："In terms of the GLP-1s, up 25%, that was generally in line"）
- 2026-08-05｜Eva Boratto｜product：World Courier 與歐洲 3PL 雙位數營業利益成長；3PL 有強勁續約，World Courier 在 FY25 艱困後市場趨穩（原話："In 3PL, we"）
- 2026-08-05｜Robert Mauch｜competition：回應分析師對 3PL／特殊物流競爭加劇的提問，CEO 承認有可信的對手，但稱自身定位於高端且廠商偏好製藥專注者（原話："there certainly are"）
- 2026-08-05｜Robert Mauch｜risk：340B 新試辦指引仍在評估，管理層稱不同業務受影響不同，未量化，且不應假設全是負面（原話："I wouldn't assume that, that's all negative."）
- 2026-08-05｜Robert Mauch｜risk：對 ASP 規則變動風險，CEO 稱政策無意影響醫師給付，並預期到 2028 年 IRA 與 Part B 時醫師給付不會受負面影響（原話："physicians will not be negatively impacted."）
- 2026-08-05｜Robert Mauch｜risk：管理層稱市場仍在消化並滿一年的廠商降價影響（原話："As the market continues to digest and annualize list price"）
- 2026-08-05｜Robert Mauch｜customer：CEO 對客戶組合表示滿意，稱大小客戶關係良好，續約無需特別提出（原話："nothing to call out in terms of renewals."）
- 2026-08-05｜Eva Boratto｜customer：大型郵購客戶銷售下降，管理層稱符合預期且與第二季一致；前一季提及該客戶可能自行內部化（原話："lower sales to our large mail order customer as expected"）

### 問答異常語氣（迴避／改口／保留）
- COR_Q3_2026_Earnings_Call_20260805.md｜問：Lisa Gill 問 FY27 市場共識約 14% 成長是否落在範圍內、除兩項建模因素外還有無其他須考量｜答法：CEO 未直接確認或否認 14%，僅重申長期財測信心並稱不會再多說
- COR_Q3_2026_Earnings_Call_20260805.md｜問：Eric Percher 問 340B 對公司業務的影響與價值主張｜答法：CEO 未回答公司在 340B 的具體業務與價值主張，稱各業務影響不同、未曾說明、實施前不會量化
- COR_Q3_2026_Earnings_Call_20260805.md｜問：Kevin Caliendo 問 ASP 規則變動對 MSO／GPO 的潛在影響並請求量化｜答法：CEO 談政策意圖與信心，未提供任何量化
- COR_Q3_2026_Earnings_Call_20260805.md｜問：George Hill 問 World Courier／3PL 競爭是否升溫，及腫瘤市場放緩是否影響 Q4 財測｜答法：CEO 談能力與差異化未直接回應競爭加劇程度；CFO 以通用語氣稱趨勢良好，未直接回答腫瘤放緩問題

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
{"date":"20260525","verdict":"B 觀望偏進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Specialty/RCA 業務貢獻 OI 45%+","columns":{"2Y 驗證點":"RCA OI margin ≥ 10%；Specialty 整體 OI YoY ≥ 12%","5Y 驗證點":"Specialty + MSO OI ≥ 50% 全公司","10Y 驗證點":"Specialty + MSO + 國際 OI ≥ 60% 全公司","具體門檻":"FY26 Specialty OI 占比 ~40%；mgmt 預估 FY28 達 45%+","來源":"FY25 10-K、Q2 FY26 8-K","漂移觸發":"連 4 季 TTM 偏離 ≥ 5% → 削弱"}},{"id":"H2","text":"Pharma 段 OI margin 穩定在 1.20%+","columns":{"2Y 驗證點":"連 4 季 OI margin ≥ 1.15%","5Y 驗證點":"5Y 滾動均 OI margin ≥ 1.20%","10Y 驗證點":"10Y 平均 OI margin ≥ 1.10%","具體門檻":"FY25: Pharma OI margin ~1.25%","來源":"FY25 10-K、Q2 FY26 8-K","漂移觸發":"連 4 季 TTM 偏離 ≥ 5% → 削弱"}},{"id":"H3","text":"Walgreens 客戶結構保持穩定（無 Chapter 11 / 大規模分拆）","columns":{"2Y 驗證點":"WBA 不公告 Chapter 11；WBA store closure","5Y 驗證點":"Walgreens 30% client share 保持（不流失至 MCK/CAH）","10Y 驗證點":"無美國 retail pharmacy 結構性 disruption","具體門檻":"WBA 2025 公告 1,200 stores 關閉 (10%)；Sycamore 談判進行中","來源":"WBA 季度報表、媒體公開","漂移觸發":"WBA 任一重大公告 → 立即重評（不需連兩季）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Walgreens 結構性問題（Sycamore 失敗 / Chapter 11 / 拆分）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（任何 WBA 8-K 揭露立即觸發）","監測指標":"WBA 季度 cash burn、store closure 公告、Sycamore 談判進度","警戒閾值":"WBA 公告 Chapter 11 / 出售 / >20% store closure → 立即清倉"}},{"id":"R2","text":"RCA 整合失敗（physician retention 不足）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"RCA OI margin（季度）、physician retention 率（年度）","警戒閾值":"連 4 季 OI margin 15% → 減倉 1/3"}},{"id":"R3","text":"Pharma margin 結構性壓縮（manufacturer 議價權惡化 + 關稅）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Pharma segment OI margin（季度趨勢）、產業 PE 倍數","警戒閾值":"連 4 季 OI margin ≤ 1.10% → 結構性破壞，減倉 1/2"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":274.91,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
