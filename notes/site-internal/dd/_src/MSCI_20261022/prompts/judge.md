你是 stock-analyst **v20 判斷 agent**，標的 MSCI（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MSCI","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_operating_revenue_","label":"Total operating revenue (GAAP)","value":867.0,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com「MSCI Reports Financial Results for Second Quarter and Six Months 2026」"},"note":"consensus 約 $864.08M，實際 $867.0M 略勝（來源：web_search 彙整市場預期，非本站 dd_numbers_extra 結構化欄）"},{"id":"f_kpi1_adjusted_ebitda_margin_n","label":"Adjusted EBITDA margin (non-GAAP)","value":62.1,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release（Adjusted EBITDA $538.5M，YoY +13.5%）"},"note":"未查得 sell-side 對 Adj. EBITDA margin 的共識數字"},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":56.2,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"10-Q（SEC EDGAR msci-20260630.htm）與公司新聞稿一致：營業利益 $487.5M／營收 $867.0M"},"note":"未查得共識數字（GAAP operating margin 非 sell-side 常態追蹤指標）"},{"id":"f_kpi3_free_cash_flow_non_gaap","label":"Free cash flow (non-GAAP)","value":326.4,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release"},"note":"未查得共識數字"},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation as % of revenue（推算）","value":2.93,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21，推算值）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21，推算值）","citation":"推算：Q2 10-Q 現金流量表揭露 H1 FY2026 SBC 累計 $73.1M，減去 Q1 10-Q（三個月至2026-03-31）揭露的 Q1 SBC $47.7M，得 Q2 單季 SBC ≈ $25.4M；MSCI 10-Q 現金流量表僅揭露年初至今累計數，未單獨揭露單季數字"},"note":"不適用"},{"id":"f_kpi5_retention_rate","label":"Retention Rate","value":95.3,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release"},"note":"不適用（公司自報營運指標，非 sell-side 財務預估項目）"},{"id":"f_kpi6_index_analytics_organic_","label":"Index／Analytics organic recurring subscription Run Rate growth","value":"Index 11.1% / Analytics 6.6%","period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release"},"note":"不適用"},{"id":"f_kpi7_fy2026_guidance_q2","label":"FY2026 全年財測（管理層 guidance，於Q2財報會議重申／更新）","value":"Opex $1,535–1,575M；Adjusted EBITDA Expense $1,340–1,370M；Capex $160–170M；Free Cash Flow $1,485–1,545M","period":"隨 Q2 FY2026 財報發布（2026-07-21）","unit":"USD millions（區間）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"隨 Q2 FY2026 財報發布（2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_msci_gross_margin_pct","label":"MSCI 毛利率","value":82.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSCI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msci_operating_margin_pct","label":"MSCI 營業利益率","value":55.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSCI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msci_fcf_margin_pct","label":"MSCI FCF 利潤率","value":44.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSCI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_spgi_gross_margin_pct","label":"SPGI 毛利率","value":70.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPGI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_spgi_operating_margin_pct","label":"SPGI 營業利益率","value":41.56,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPGI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_spgi_fcf_margin_pct","label":"SPGI FCF 利潤率","value":34.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPGI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_gross_margin_pct","label":"MCO 毛利率","value":74.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_operating_margin_pct","label":"MCO 營業利益率","value":46.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_fcf_margin_pct","label":"MCO FCF 利潤率","value":36.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fds_gross_margin_pct","label":"FDS 毛利率","value":51.38,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FDS.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fds_operating_margin_pct","label":"FDS 營業利益率","value":29.55,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FDS.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fds_fcf_margin_pct","label":"FDS FCF 利潤率","value":29.05,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FDS.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":604.46,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":0.13,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":69.5,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.76,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.67 → 19.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.18,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.39 → 22.35）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.2,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（25.4 → 25.35）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":19.52,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":22.35,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":25.35,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":33.03,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":13.18,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":15.04,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":30.97,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 19.52，分子＝快照價 604.46","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.315,"period":"2026-10-22","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-22"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":6191.5,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 6544.2、現金 352.7（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":72.7,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":50135.74,"period":"2026-10-22","unit":"USD m","basis":"市值 43944.24 ＋ 淨負債 6191.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":3524.32,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":3838.57,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":14.23,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 604.46 / W52 568.26 / W104 564.05 / W250 518.06 / W250 13週斜率 0.03%"},{"id":"f_ma_w52","label":"52 週均線","value":568.26,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":564.05,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":518.06,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.03,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列名指數對手：S&P Dow Jones Indices、FTSE Russell、Nasdaq、Bloomberg、Solactive；分析對手含 Axioma、BlackRock Solutions、Bloomberg、FactSet。","source":"SEC EDGAR MSCI 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"Among our Index competitors are S&P Dow Jones Indices LLC (a joint venture of S&P Global Inc. and CME Group Inc.); FTSE Russell, a subsidiary of the London Stock Exchange Group plc; Nasdaq Inc; Bloomberg Finance L.P. (“Bloomberg”); and Solactive AG.","as_of":"2026-02-06","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"風險因子：對手與新進入者可能用 AI 以較低價格推出競爭產品，客戶也可能以 AI 自建客製指數、風險分析等取代 MSCI 產品；競爭可能造成降價或失去份額。","source":"SEC EDGAR MSCI 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"Competitors and new market entrants may use AI to develop products that compete with our offerings at lower price points, with faster time-to-market or with additional or better capabilities, which could impair our ability to compete effectively and put pressure on our revenues and subscriptions.","as_of":"2026-02-06","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"最大客戶之一 BlackRock 同時是競爭者／分銷商，可能終止部分或全部關係。","source":"SEC EDGAR MSCI 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"Certain of our clients are also significant shareholders, competitors or distributors of our content, including some of our largest clients, such as BlackRock.","as_of":"2026-02-06","retrieved_at":"20261022","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"MSCI's FY2023 10-K discloses BlackRock as its largest client organization by revenue, at 9.8% of consolidated operating revenues, with 95.4% of BlackRock's revenue to MSCI coming from asset-based fees on ETFs/non-ETF products using MSCI indexes — a concentration/single-client dependency risk factor.","source":"MSCI Inc. Form 10-K FY2023 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819824000030/msci-20231231.htm","excerpt":"our largest client organization by revenue, BlackRock, accounted for 9.8% of our consolidated operating revenues","as_of":"2023-12-31","retrieved_at":"2026-09-29","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"BlackRock is MSCI's largest client, accounting for 10.8% of consolidated operating revenues for FY2025; 96.5% of that BlackRock-derived revenue comes from asset-based fees on BlackRock's ETFs and non-ETF products tracking MSCI indexes.","source":"MSCI Inc. 10-K FY2025 (filed 2026)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"For the year ended December 31, 2025, our largest client organization by revenue, BlackRock, accounted for 10.8% of our consolidated operating revenues, with 96.5% of the operating revenues from BlackRock coming from fees based on the assets in BlackRock's ETFs and non-ETF products that are based on our indexes.","as_of":"2025-12-31","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"MSCI discloses risk that its largest clients (including BlackRock) may negotiate lower asset-based fees, stop using MSCI indexes, or cancel/reduce usage, which could have a material adverse effect on results.","source":"MSCI Inc. 10-K FY2025 (filed 2026), Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"The possibility that our clients seek to negotiate lower asset-based fees or cease using our indexes as the basis for indexed investment products / Cancellations or reductions by our clients or reduced demand for our products or services","as_of":"2025-12-31","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"BlackRock accounted for 18.7% of MSCI's Index segment operating revenues for FY2025 (vs. 17.4% in FY2022), indicating rising within-segment concentration over time.","source":"MSCI Inc. 10-K FY2025 (filed 2026)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"BlackRock's own balance sheet/credit shows no distress: its March 2026-amended $6.3B revolving credit facility (extended to March 2031) requires a max leverage ratio of 3.5x, and BlackRock's actual leverage was under 1x as of June 30, 2026, with nothing drawn on the facility.","source":"BlackRock, Inc. 10-Q filings for Q1 and Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0002012383/000119312526337177/blk-20260630.htm","excerpt":"In March 2026, the 2026 Credit Facility was amended to increase the aggregate commitment amount by $400 million to $6.3 billion and extend the maturity date to March 2031. The 2026 Credit Facility requires the Company not to exceed a maximum consolidated leverage ratio of 3.5 to 1, which was satisfied with a ratio of less than 1 to 1 at June 30, 2026, with no amount outstanding under the 2026 Credit Facility.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MSCI Q2 2026 organic recurring subscription Run Rate growth was 8.1%; retention rate rose to 95.3% from 94.4% a year earlier, indicating durable recurring demand rather than a cyclical spike.","source":"MSCI Inc. Q2 2026 earnings release","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-second-quarter-and-six-months-10","excerpt":"Organic recurring subscription Run Rate growth was 8.1%. Retention Rate in second quarter 2026 was 95.3%, compared to 94.4% in second quarter 2025.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MSCI saw record ETF inflows linked to its indexes in Q1 2026 (north of $100B), with $2.4T in ETF AUM and over $21T total benchmarked to MSCI indices, reflecting continued structural growth in passive/index-linked demand.","source":"Foreign Policy Journal, citing MSCI Q1 2026 earnings materials","url":"https://www.foreignpolicyjournal.com/2026/04/18/msci-approaches-q1-earnings-with-index-division-running-at-record-7-trillion-in-etf-linked-assets/","excerpt":"MSCI saw record inflows into ETFs linked to its indexes in the first quarter of 2026, with inflows north of $100 billion... over $21 trillion benchmarked to MSCI indices, including $2.4 trillion in ETF products.","as_of":"2026-03-31","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"查無 MSCI Inc（指數/資料商）遭 DOJ、FTC 或 EU 反壟斷調查或拆分風險之報導；搜尋結果中提及的反壟斷案例為 ISS/Glass Lewis（代理投票顧問）及 Microsoft/Google 等科技公司，非 MSCI。","source":"WebSearch aggregate (no direct hit)","url":null,"excerpt":null,"as_of":"2026-09-29","retrieved_at":"2026-09-29","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"MSCI 10-K 揭露：2024 年 11 月歐盟通過 ESG 評等透明度與誠信規範 (EU) 2024/3005，要求在歐盟境內營運的 ESG 評等提供者須於 2026 年 7 月 2 日起取得 ESMA 授權或註冊；MSCI 表示其部分永續與氣候相關產品預期將受此規範管轄。","source":"MSCI Inc. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"In November 2024, the European Union adopted Regulation (EU) 2024/3005 on the transparency and integrity of ESG rating activities, which will require ESG rating providers operating in the European Union to be authorized by, or registered with, ESMA beginning July 2, 2026.","as_of":"2026-02-01","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"MSCI 10-K 一般性風險揭露：全球指數/標竿業持續面臨來自 EU、美國及其他地區監管者、政策制定者與媒體對指數業角色與影響力的高度關注，可能帶來負面輿論或新規；MSCI Limited 為 UK FCA 授權之標竿管理機構，MSCI Deutschland GmbH 亦持有德國 BaFin／ESMA 授權。","source":"MSCI Inc. Form 10-K FY2025 (SEC EDGAR) / MSCI Benchmark Regulations page","url":"https://www.msci.com/indexes/index-resources/benchmark-regulations","excerpt":null,"as_of":"2026-02-01","retrieved_at":"2026-09-29","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MSCI FY2025 10-K 風險因素：關稅、報復性關稅與貿易緊張可能影響投資人配置與客戶預算、延後或取消訂閱；地緣與貿易政策變動可能限制其在特定司法管轄區提供產品、取得營運所需技術，或降低需求；亦受出口管制、制裁等法規約束。","source":"SEC EDGAR｜MSCI 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"Our business is impacted by economic conditions, including economic uncertainty, market downturns and volatility in the global capital markets and evolving investment trends (including volatility and trends resulting from geopolitical events and trade policy changes, including tariffs, retaliatory tariffs and related trade tensions).","as_of":"2026-02-06","retrieved_at":"20261022","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"台灣占 MSCI 新興市場指數(EM Index)權重達 24.8%（2026-04-30 資料），為指數內最大權重國家，主因 AI 驅動半導體需求；同期資訊科技板塊權重由 31.8% 升至近 37%。此為 MSCI 旗艦指數產品在地緣風險區域（台灣/中國）的集中曝險。","source":"MSCI - Markets in Motion: Taiwan at the Top, EM Weight Breakdown","url":"https://www.msci.com/indexes/markets-in-motion/visualizations/taiwan-at-the-top-msci-em-weight-breakdown","excerpt":"Taiwan held 24.8% of the index as of April 30, 2026.","as_of":"2026-04-30","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Index 營收段 H1 2026 營收年增17.6%，資產基礎費(asset-based fees)年增26.6%為主動能，訂閱型營收年增10.3%；掛鉤MSCI股票指數的ETF資產年增34.6%，但平均基點費率下滑部分抵銷成長。","source":"MSCI Reports Financial Results for Second Quarter and Six Months 2026 (IR新聞稿)","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-second-quarter-and-six-months-10","excerpt":"Index operating revenues increased 17.6% for the six months ended June 30, 2026, primarily driven by growth from asset-based fees as well as recurring subscriptions... Operating revenues from asset-based fees increased 26.6%... ETFs linked to MSCI equity indexes and non-ETF indexed funds linked to MSCI indexes increased by 34.6% and 12.2%, respectively, primarily driven by an increase in average AUM, partially offset by a decrease in average basis point fees.","as_of":"2026-07-21","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Analytics 營收段 Q1 2026 營收$190.0M年增10.3%(organic 10.5%)；Q2 2026原guidance約5%成長，訂閱銷售成長因lumpiness與高基期而放緩；成長動能來自Multi-Asset Class與Equity Analytics產品，避險基金、銀行/券商、資產管理客群為主要貢獻。","source":"MSCI Reports Financial Results for First Quarter 2026 (IR新聞稿)","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-first-quarter-2026","excerpt":"Analytics operating revenues were $190.0 million, up 10.3%, with organic operating revenue growth for Analytics at 10.5%... The increase was driven by growth in both Multi-Asset Class and Equity Analytics products, and reflected growth across all regions, primarily led by hedge fund managers, banking and brokerages and asset managers client segments.","as_of":"2026-03-31","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Sustainability and Climate（原ESG and Climate）營收段 Q2 2026 Climate Run Rate跨產品線年增近12%；First Street收購案預期為該營收段增加約$10M訂閱Run Rate。","source":"MSCI Inc (MSCI) Q2 2026 Earnings Call Highlights - GuruFocus","url":"https://www.gurufocus.com/news/8970269/msci-inc-msci-q2-2026-earnings-call-highlights-strong-growth-amid-market-challenges","excerpt":"Climate Run Rate Growth reached nearly 12% across MSCI product lines in Q2 2026. Additionally, the First Street Acquisition was expected to add about $10 million of subscription run rate to the Sustainability and Climate segment.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"All Other–Private Assets 營收段 Q1 2026營收$72.6M年增7.9%(organic 5.3%)；Q2 2026營收$74.7M年增4.9%(organic 4.4%)，organic訂閱Run Rate年增8.3%；成長動能來自Private Capital Solutions（Total Plan Manager、Private Capital Transparency Data、Private Capital Intel）。成長率較其他三段明顯放緩。","source":"MSCI Reports Financial Results for Second Quarter and Six Months 2026 (IR新聞稿)","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-second-quarter-and-six-months-10","excerpt":"All Other – Private Assets operating revenues were $72.6 million, up 7.9%, with organic operating revenue growth of 5.3%... All Other – Private Assets operating revenues were $74.7 million, up 4.9%, with organic operating revenue growth of 4.4%... organic recurring subscription Run Rate growth for All Other – Private Assets was 8.3% in Q2 2026.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"被動ETF市場2026年估值達$16.8兆，但主動型ETF數量已在2025年6月超越被動型ETF；主動ETF資產達$1.47兆、近三年CAGR 59%，顯示主動策略在ETF資金流結構性搶佔份額，對MSCI核心被動指數授權/資產基礎費成長模型構成潛在逆風。","source":"Active vs. Passive ETFs: How the 2026 Active Surge Changes the Math - etf.com","url":"https://www.etf.com/sections/etf-basics/active-vs-passive-etfs-how-2026-active-surge-changes-math","excerpt":"The number of active ETFs surpassed the number of passive ETFs in June 2025, with 2,187 passive ETFs and 2,741 active ETFs available by year-end. Active ETF assets have crossed $1.47 trillion, growing at a 59% compound annual rate over the last three years.","as_of":"2025-12-31","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AI/LLM 工具可低成本自動解析企業永續揭露、複製部分 ESG 評等結果；若機構投資人認為 MSCI ESG Ratings 與 AI 生成替代品區隔不足，MSCI 的評等定價溢價可能被侵蝕","source":"PitchGrade Research - \"MSCI: Index Licensing and ESG Data Franchises in the Age of AI-Powered Analytics\"","url":"https://pitchgrade.com/research/msci-ai-margin-pressure","excerpt":"If institutional investors conclude that MSCI ESG Ratings are insufficiently differentiated from AI-generated alternatives, the pricing premium erodes","as_of":"2026-01-29","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"新興自助式指數設計平台（如 S&P SPICE、Merqube 的 Garage）讓客戶自行客製指數規則，不再依賴指數商內部量化團隊人力；MSCI 已於 2024 年併購 Foxberry F9 平台因應此一產業趨勢","source":"Panta.ai - \"Will Self-Service Indexing Gain Wide Adoption?\"","url":"https://panta.ai/self-service-indexing-adoption/","excerpt":"custom index design is no longer constrained by how many quants or product people a provider can throw at a request","as_of":"2025-11-19","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"MSCI 10-K 稱優先發展開放、可擴展的分銷，讓客戶透過 API、資料商與第三方通路、雲端工具把 MSCI 內容整合進自家平台與工作流程","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"We are prioritizing open, scalable distribution that allows clients to access and integrate MSCI content and analytical tools into their own platforms and workflows, including through APIs, data vendors and third-party distribution partners, as well as cloud-based tools.","as_of":"2026-02-06","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"MSCI 推出 AI connectors，客戶可經 MSCI ONE 或 ChatGPT／Claude 等第三方 AI 服務存取專有資料","source":"MSCI press release: MSCI unveils new AI connectors transforming access to proprietary data","url":"https://www.msci.com/discover-msci/media-room/msci-unveils-new-ai-connectors-transforming-access-to-proprietary-data","excerpt":"Clients can access MSCI’s insights via the MSCI ONE cloud-based platform or through leading AI providers, including the MSCI app in OpenAI’s ChatGPT and the MSCI connector in Claude.","as_of":"2026-02-01","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師共識維持 Buy／Strong Buy，平均目標價約 $692–$713（不同彙整站數字略有差異），最低 $570、最高 $760；平均目標價較現價估計有約 24.5% 上行空間","source":"stockanalysis.com / wallstreetzen.com 分析師預測彙整頁","url":"https://stockanalysis.com/stocks/msci/forecast/","excerpt":"According to 18 analysts polled by S&P Global, MSCI Inc. stock has a consensus rating of \"Buy\" and an average price target of $692.06. The lowest analyst price target is $570 (+2.57%) and the highest is $760 (+36.76%).","as_of":"2026-09","retrieved_at":"2026-09-29","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"MSCI 2026 Q2 財報後上修 2026 全年費用 guidance：營運費用上修至 $1,535M–$1,575M（原 $1,490M–$1,530M），Adjusted EBITDA 費用上修至 $1,340M–$1,370M（原 $1,305M–$1,335M），主因近期併購（含 First Street）及 AUM 動能超過先前假設","source":"MSCI Reports Financial Results for Second Quarter and Six Months 2026 (businesswire/ir.msci.com)","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-second-quarter-and-six-months-10","excerpt":"the company updated operating expense guidance to $1,535M–$1,575M (up from $1,490M–$1,530M) and adjusted EBITDA expense guidance to $1,340M–$1,370M (up from $1,305M–$1,335M)","as_of":"2026-07-21","retrieved_at":"2026-09-29","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 2026 財報後，JPMorgan（Alexander Hess）維持 Overweight 但目標價由 $742 下修至 $700；Evercore ISI（David Motemeden）維持 Outperform 但目標價由 $746 下修至 $722，理由是費用上升軌跡導致估值重新校準","source":"BigGo Finance: \"MSCI Beats Q2 Estimates but Analysts Slash Price Targets on Rising Costs\"","url":"https://finance.biggo.com/news/3aadede8-eb80-4fd1-b4a1-bbfd3f98f59e","excerpt":"JP Morgan analyst Alexander Hess kept an Overweight rating on MSCI but cut the price target to $700 from $742. Evercore ISI Group analyst David Motemeden maintained an Outperform rating and lowered the target to $722 from $746","as_of":"2026-07-22","retrieved_at":"2026-09-29","affects":["valuation","thesis.R","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MSCI Q2 2026 每股盈餘與營收數字在不同彙整站出現不一致版本：部分來源稱 EPS $4.94 優於共識 $4.90（小幅超預期），另有來源稱 EPS $4.94 不及共識 $5.03（不如預期）；營收 $867M 亦分別被稱為優於／不如共識 $864M vs $883.8M。無法從搜尋摘要判定哪個共識基準正確，需查證交易所申報或原始財報稿","source":"Investing.com transcript vs 247wallst.com/basisreport.com 對照矛盾","url":null,"excerpt":null,"as_of":"2026-07-21","retrieved_at":"2026-09-29","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"10-K FY2025 Item 3：管理層認為目前未決事項整體不會對業務、營運結果、財務狀況或現金流產生重大影響。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"However, based on facts currently available, we believe that the disposition of matters that are currently pending or asserted will not, individually or in the aggregate, have a material effect on MSCI’s business, operating results, financial condition or cash flows.","as_of":"2026-02-06","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-01-27 與 BlackRock 簽署 ETF 指數授權修約，期限延至 2035-03-31，並自 2026-01-01 起調整部分基金授權費。","source":"SEC EDGAR 8-K Item 1.01 (2026-01-28)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000008/msci-20260127.htm","excerpt":"The Amendment extends the term of the Existing ETF Agreements until March 31, 2035","as_of":"2026-01-28","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026 年完成三筆小型收購：Compass Financial（3/3）、ApeVue（4/7）、First Street（8/3，現金 1.2 億美元，氣候風險資料）。","source":"WebSearch 彙整（Nasdaq／Zacks／MSCI IR）","url":"https://www.nasdaq.com/articles/msci-acquires-compass-financial-expand-multi-asset-indexes","excerpt":null,"as_of":"2026-03-03","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026 年完成 Compass Financial（3/3）、ApeVue（4/7）、First Street（8/3，現金 1.2 億美元）三筆小型收購；8-K 清單近 12 個月無 Item 2.01。","source":"WebSearch 彙整（Nasdaq／Zacks／MSCI IR）","url":"https://www.nasdaq.com/articles/msci-acquires-compass-financial-expand-multi-asset-indexes","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261022","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K Item 3：未決訴訟預期不會有重大影響；搜尋僅見原告律所 2025 年調查徵求稿，未見已提起之集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"However, based on facts currently available, we believe that the disposition of matters that are currently pending or asserted will not, individually or in the aggregate, have a material effect on MSCI’s business, operating results, financial condition or cash flows.","as_of":"2026-02-06","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單無 Item 4.02（重編）；10-K Item 3 未列重大調查。","source":"SEC EDGAR 8-K 清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001408198&type=8-K","excerpt":"2025-10-22 至 2026-10-22 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MSCI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":82.97,"operating_margin_pct":55.66,"fcf_margin_pct":44.77,"rd_intensity_pct":5.45},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSCI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"SPGI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":70.9,"operating_margin_pct":41.56,"fcf_margin_pct":34.57,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPGI","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MCO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.98,"operating_margin_pct":46.1,"fcf_margin_pct":36.36,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"FDS","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.38,"operating_margin_pct":29.55,"fcf_margin_pct":29.05,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FDS","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MSCI"},"financial_history":{"ticker":"MSCI","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":2248598000.0,"revenue_yoy_pct":null,"gross_margin_pct":82.02,"operating_margin_pct":53.71,"net_income":870573000.0,"diluted_eps":10.72,"free_cash_flow":1022474000.0,"fcf_margin_pct":45.47,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":2528920000.0,"revenue_yoy_pct":12.47,"gross_margin_pct":82.34,"operating_margin_pct":54.75,"net_income":1148592000.0,"diluted_eps":14.39,"free_cash_flow":1145178000.0,"fcf_margin_pct":45.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2856128000.0,"revenue_yoy_pct":12.94,"gross_margin_pct":81.99,"operating_margin_pct":53.52,"net_income":1109128000.0,"diluted_eps":14.05,"free_cash_flow":1386509000.0,"fcf_margin_pct":48.55,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":3134459000.0,"revenue_yoy_pct":9.75,"gross_margin_pct":82.44,"operating_margin_pct":54.67,"net_income":1202305000.0,"diluted_eps":15.69,"free_cash_flow":1458585000.0,"fcf_margin_pct":46.53,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MSCI/MSCI_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**MSCI Inc.** | Earnings Calls | 2026-10-20

**Operator** (Operator):
Good day, ladies and gentlemen, and welcome to the MSCI Third Quarter 2026 Earnings Conference Call. As a reminder, this call is being recorded. [Operator Instructions]
I would now like to turn the call over to Jeremy Ulan, Head of Investor Relations and Treasurer. You may begin.

**Jeremy Ulan** (Executives):
Thank you, operator. Good day, and welcome to the MSCI Third Quarter 2026 Earnings Conference Call. Earlier this morning, we issued a press release announcing our results for the third quarter 2026. This press release, along with an earnings presentation, are available on our website, msci.com, and under the Investor Relations tab. 
Let me remind you that this call contains forward-looking statements, which are governed by the language on the second slide of the presentation. You are cautioned not to place undue reliance on forward-looking statements, which speak only as of the date on which they are made, are based on current expectations and current economic conditions and are subject to risks and uncertainties that may cause actual results to differ materially from the results anticipated in these forward-looking statements. For a discussion of additional risks and uncertainties, please see the risk factors and forward-looking statements disclaimer in our most recent Form 10-K and in our other SEC filings. 
During today's call, in addition to results presented on the basis of U.S. GAAP, we also refer to non-GAAP measures. You'll find a reconciliation of our non-GAAP measures to the equivalent GAAP measures in the appendix of the earnings presentation. We will also discuss operating metrics such as run rate and retention rate. Important information regarding our use of operating metrics such as run rate and retention rate are available in the earnings presentation. 
On the call today are Henry Fernandez, our Chairman and CEO; Andy Wiechmann, our Chief Financial Officer; and Alvise Munari, our Chief Product Officer and Head of Client Segments, who will be joining for the Q&A session.
With that, let me now turn the call over to Henry Fernandez. Henry?

**Henry Fernandez** (Executives):
Thank you, Jeremy. Good day, everyone, and thank you for joining us. In the third quarter, MSCI delivered strong financial and operating metrics including historic net new sales in Index, Analytics and Private Capital Solutions plus another record quarter for asset-based fees. We have built impressive momentum across these three product lines. 
While Sustainability and Climate continue to face challenges, we believe that our recent acquisition of First Street will help accelerate a return to higher growth in Climate. These results show that MSCI is expanding our mission-critical role in global investing, even as we transform our business to an AI-first company. 
Since our IPO 19 years ago, MSCI has demonstrated a strong and consistent track record of execution. This foundation positions us well to capture expanding opportunities, both across client segments and a growing range of solutions. We have multiple dimensions of growth and a compelling opportunity to compound over the long term. Financially, our strong Q3 performance included total revenue growth of 12.4%, ABF revenue growth of 25%, subscription revenue growth of 8%, adjusted EBITDA growth of 12% and adjusted EPS growth of 14%.
From July 1st through October 19th, we repurchased $627 million of MSCI shares at an average price of $562 per share. Since the beginning of 2024, we have opportunistically repurchased nearly 8 million shares for $4.4 billion. During the same period, I have personally purchased an additional 57,000 shares for $30.1 million. These purchases unequivocally demonstrate our strong belief in the potential of the MSCI franchise. 
Operationally, in Q3, MSCI achieved total run rate growth of 12%, fueled by a record ABF run rate of almost $1 billion. Our ABF performance reflected record AUM levels in ETF and non-ETF products linked to MSCI indices, including inflows of $76 billion. There are now nearly $23 trillion of AUM benchmarked to MSCI indices. Of that $23 trillion, roughly $15 trillion is actively managed, while $8 trillion is indexed. 
We also posted subscription run rate growth of 9% after adding nearly $55 million in recurring net new sales. And we delivered a retention rate of 95%, an improvement of 30 basis points from Q3 of last year. MSCI is a long-term compounder driven by both ABF and subscription growth. On the overall subscription side, Q3 was our best ever quarter for recurring net new sales in Analytics and Private Capital Solutions, along with our best ever Q3 for recurring net new sales in Index. 
Compared with a year earlier, recurring net new sales grew by 88% in PCS, 63% in Analytics and 40% in Index. Notably, MSCI saw robust demand by both our traditional and newer solutions. In fact, we continue to see consistent growth in recurring sales from our newer products. And importantly, our higher pace of innovation is strengthening sales of our existing products as we continue to deliver greater value to clients. Virtually all those newer products are powered by artificial intelligence. 
Q3 also showed our diversified strength across regions. Recurring net new sales grew by 74% in EMEA, 36% in APAC and 26% in the Americas. Indeed, we achieved our best ever quarter in APAC, driven by Analytics. MSCI is unlocking additional growth layers through our recently announced partnerships and acquisitions. In Q3, for example, we formalized the landmark agreement with UBS that we first announced back in July. This agreement will extend the reach of our private asset solutions, strengthen connections between GPs and wealth managers and promote greater transparency across private markets. 
Similarly, our acquisition of the AI-native platform, Vantager, now the MSCI's private asset diligence platform, enabled us to complete a major deal with a large U.S. bank. At the client segment level, MSCI achieved a record quarter with asset owners, more than tripling our recurring net new sales from a year earlier, driven by demand for our total portfolio solutions and our integrated risk and portfolio management analytics.
Our largest deal of the quarter moved MSCI from a vendor relationship to a strategic portfolio analytics partner for one of Asia's biggest and most sophisticated sovereign wealth funds. We also closed a number of major Analytics and Index deals with top hedge funds, including deals for our equity models and custom index modules. Finally, we maintained our steady performance with asset managers globally while achieving a strong quarter in EMEA, where we posted 35% recurring net new sales growth. 
Despite the ongoing retention pressures in Sustainability and Climate, we entered Q4 with solid momentum and a strong client engagement across the whole MSCI franchise. We are incredibly excited about the expansion of MSCI's offerings through new use cases for newer client segments such as wealth managers, banks as lenders, GPs and insurance companies in their underwriting processes. We are delivering and expanding MSCI by leveraging what we already do for our more traditional clients, such as asset managers, asset owners, traders and hedge funds. MSCI truly is a one-of-a-kind company that is uniquely positioned to benefit from the biggest transformations reshaping the global investment and finance industry.
And with that, let me turn things over to Andy.

**Andrew Wiechmann** (Executives):
Thank you, Henry. Hi, everyone. Our strong results reflect our rapid pace of innovation, our effective go-to-market execution and the growing ecosystem around our tools. We believe this momentum is sustainable, and we continue to have an attractive pipeline of opportunities. MSCI is a powerful compounder and the run rate algorithm was on full display with continued double-digit subscription growth in Index, high single-digit growth in Analytics, accelerating growth in Private Assets and outsized secular growth in asset-based fees. 
Across client segments, we saw double-digit growth with non-asset manager segments and mid- to high single-digit growth among asset managers. This algorithm, combined with inherent operating leverage and ongoing capital optimization allows us to fuel consistent compounding value creation. And the momentum in the business is evident with LTM recurring net new subscription sales up 26%. 
Drilling down into Index, organic subscription run rate growth accelerated further to 11.7%. Powerful indexation trends drove double-digit subscription growth across hedge funds, banks and brokers, wealth managers and asset owners, of 32%, 15%, 10% and 10%, respectively. And the retention rate was over 97% across index, including a retention rate of 98% with asset managers. Additionally, asset-based fees were fueled by $76 billion of equity ETF cash inflows concentrated in developed markets ex U.S. and emerging markets. This was our second highest quarter of inflows behind only the first quarter of this year. 
Within Analytics, we had organic subscription run rate growth of 7.5%, driven by several large strategic client wins with asset owners and wealth managers. These clients are seeking to modernize their investment platforms, integrate risk and portfolio management workflows and enhance investment decision-making alongside sustained demand for our factor content. As we have mentioned, Analytics operating metrics will be lumpy quarter-to-quarter, but the trend has been encouraging with LTM recurring net new up 18% over the prior LTM period, driven by strong momentum in key areas. 
In Private Capital Solutions, subscription run rate growth accelerated to 19%. We see growing demand across existing solutions like our Transparency, Private Capital Intel and Total Plan offerings, and we are building momentum in newer offerings like our data and diligence platforms. Additionally, we are seeing good traction in landing benchmark wins across asset owners. 
In Real Assets, organic subscription run rate growth was 2%, supported by improving client retention and clients seeking broader data access through Snowflake. In the Sustainability and Climate reportable segment, we executed over $5 million of new recurring sales in Sustainability and over $2 million of new recurring sales in Climate. We saw elevated cancels with one sizable downsell related to a client rightsizing its sustainability spend.
Meanwhile, in Climate, run rate growth across MSCI product lines was 8%, excluding the impact of First Street. Demand for our physical risk solutions, including from recently acquired First Street, is growing. The integration of First Street remains on track and client engagement has been very strong. As we mentioned last quarter, the pressures on parts of the sustainability franchise are expected to continue through the fourth quarter. We expect the Sustainability and Climate reporting segment to have recurring net new sales that are roughly flat to slightly positive in the fourth quarter. 
Turning to our guidance. Adjusted EBITDA expenses in the third quarter were in line with the level we indicated in September, driven by the impact of recent acquisitions, higher performance stock-based compensation and higher severance as we unlock efficiencies ahead of schedule. Given these items, which enhance the franchise heading into 2027 and the strong top line momentum this year, we expect to be at the top end of our expense guidance ranges for 2026. 
To provide more color on the elevated expense items in 2026, acquisitions are expected to add roughly $20 million of additional expenses this year. The incremental accruals of performance stock options, which are mostly driven by higher-than-expected AUM growth in products linked to our indexes and the strong business momentum, are expected to add roughly $15 million to $20 million of noncash expenses, and severance is expected to be roughly $10 million to $15 million higher than originally planned, reflecting the acceleration of efficiencies and the AI transformation across the organization.
Despite our high level of investment and the addition of 4 acquisitions, headcount has remained roughly flat compared to a year ago. This reflects our ability to leverage AI to transform the company for the future, accelerate the pace of innovation and drive faster growth. Additionally, we increased the interest expense guidance as a result of higher revolver balances to support our opportunistic share repurchases. We also narrowed the tax rate guidance for the full year to 18% to 19.5%. Overall, we remain well positioned for and committed to delivering very attractive profitability growth while investing for the long term.
In summary, our Q3 results show consistent execution across product lines and client segments. We are pairing continued investment in growth areas with strong financial discipline, and we have the flexibility to adjust as conditions evolve. We look forward to keeping you posted as we deliver on our priorities.
And with that, operator, please open the line for questions.

**Operator** (Operator):
[Operator Instructions] First question coming from the line of Toni Kaplan with Morgan Stanley.

**Toni Kaplan** (Analysts):
Henry, I wanted to ask a longer-term question on Analytics. I was wondering how you're thinking about the future in terms of the product platform and distribution, just given the advancements in AI. How do you think customers will be interacting with your data, with your platform? Just trying to think of from a long-term perspective over the next few years, how you think that this is going to change?

**Henry Fernandez** (Executives):
Thank you for the question, Toni. The first thing to keep in mind that you know well is at MSCI, we run a fully integrated company, in which each product line feeds off and feeds into other product lines. In the past, maybe more distant past, we viewed Analytics, especially our risk management platform -- risk and performance management platform, as one of the more important product line. In the recent past, we have begun to develop a strategy that help us take this extremely important product line and make it much more strategic and much more value added. So for example, in our risk management platform, we get enormous amount of portfolio data that, in general, we have rights to anonymize and aggregate and things like that, that could develop new products.
Secondly, in a risk management and performance platform, we know what the clients are doing every single day by them having their portfolios and running reports in our platform. So we're developing plans to propose to the clients, "Why don't you do this? Why don't you look at this? Why don't you think of this new product, this new idea, this new this, this new that?" And AI is going to help us do that because otherwise, we'll have to have humans do that. 
So anyhow, so the last point that I will make, therefore, is MSCI is an analytics company. In totality, by history, we're a modeling company therefore, an analytics company. Models, the index methodologies are models, the factor models, the other risk models, the ESG ratings are models, all of that. So we are in the process of integrating the company into a more holistic analytics shop with proprietary data and very advanced new AI technology to gather the data, process the data and help our clients consume the content, the data and the models much more effectively. So that's the vision of analytics at MSCI.

**Operator** (Operator):
Our next question in the queue coming from the line of Alex Kramm with UBS.

**Alex Kramm** (Analysts):
You talked about strong momentum in the business continuing. So maybe you can be a little bit more specific. I know we're only 20 days into the quarter, but if you think across the business, you talked about Sustainability being weak again in the 4Q. But where are you seeing strong momentum as it relates to maybe last year because the 4Q is the strongest sales quarter usually in the year. So just any more color around pipelines to give us some comfort for the momentum into year-end, please?

**Andrew Wiechmann** (Executives):
Sure. Alex, it's Andy. So as I mentioned in the prepared remarks, we see an attractive pipeline here. We've got tremendous momentum across the business. If you look at where that momentum is, we saw an acceleration in Index, saw an acceleration in PCS. We saw a pickup in Analytics, and we've seen it across non-asset manager client bases. And so those are all things that are sustainable trends, and we see good momentum. 
Obviously, the third quarter was a very solid quarter. We continue to expand and do more for clients, and as a result of that, we're having many large deals. These types of deals are reflective of repeatable types of strategic sales that I think we're going to see more and more across the business are going to be a key component of growth into the future. 
There will be some inherent lumpiness related to the timing of these deals. And as we've alluded to, I wouldn't overly focus on one quarter, but I would say the overall pipeline is quite robust. The momentum is there. Q4, as you said, is a very strong quarter for us for a number of reasons. Notably, there are things like concentration of contract renewals, client budgets at the year-end for our sales organization. And so yes, we're looking at an important fourth quarter here, and we've got the opportunities and the momentum to deliver. And I think we're seeing good momentum not only into the fourth quarter, but heading into next year across those key growth engines for the firm.

**Operator** (Operator):
Our next question in queue coming from the line of Manav Patnaik with Barclays.

**Manav Patnaik** (Analysts):
I guess I just wanted to follow up on that in terms of the big -- you called out a bunch of large contracts this quarter. It sounded like, Andy, you just said you expect more of those to continue. So we shouldn't treat these as timing perhaps? Just trying to get kind of a level check on the growth rate there. And then I just wanted to clarify your comments around how First Street is going to help the growth on the Sustainability side, please.

**Henry Fernandez** (Executives):
Manav. So look, I think that as we expand MSCI into new use cases, new client segments, there is an incredible amount of innovation and new product launches at MSCI. And as we engage with clients, the number of large deals is going to increase. Now each quarter, we're going to have a lot of large deals, and it will make it a great quarter like this one. And some deals will slip to the next quarter. And it may appear that the quarter wasn't that great. It will be a mistake to interpret it that way. 
The best way to analyze our performance is on a multi-quarter basis because these large deals are going to create differences quarter-by-quarter. And therefore, when we have a great quarter, everyone is going to get really excited. When the quarter is a little less -- is a little softer because a few deals, large deals slip to the next quarter, it's going to look less exciting and everyone is going to start worrying. 
The trend here is very positive. The trend is that we're picking up growth a little bit in asset managers. We're stable in asset managers with slightly higher growth, but importantly, in the non-asset manager segments, of course, asset-based fees within Index and ETF and all that, but in traders and in hedge funds, in GPs, for sure, in asset owners, as you saw in this quarter, et cetera.
So I think that my best advice to all of you is to evaluate not the financial metrics, the financial metrics get smoothed out by the accounting process. But the operating metrics in recurring new sales and retentions and cancels, you need to evaluate them on a multi-quarter basis. Otherwise, you're going to go crazy, you're going to feel very good one quarter, and you're going to feel not as good the next.

**Operator** (Operator):
Our next question in queue coming from the line of Alexander Hess with JPMorgan.

**Alexander EM Hess** (Analysts):
Just wanted to see if we can get you both to elaborate on the qualitative and the quantitative and something in your prepared remarks in the press release. You noted robust demand for both traditional and newer solutions. Maybe we could have Andy start off with dimensioning how much are newer solutions contributing to the net new number? And then maybe from Alvise or Henry, how we should think about what's resonating in market right now? And then also, if you don't mind me tacking on, any comments you can offer on the largest deal you closed and what was different about that specific transaction?

**Andrew Wiechmann** (Executives):
Alex, so let me give some color on the quantitative side. And as you said, I'll turn it over to Alvise to give some color on types of products where we're getting traction. He can comment on that big win we had, which is very exciting for us. As you know, we have seen, not just this quarter, but this year, we've seen a meaningful increase in the contribution from new products to sales. That is something that is a key driver of growth, and we expect that to continue. 
In the third quarter here, that contribution to new sales from new products increased more than 50% compared to a year ago. And so we have seen a significant step-up in new products launched this year, but importantly, the monetization of those new products. I would also highlight beyond just the monetization of the products themselves, that innovation, that development, the enhancements that we are making are also critical in driving improved retention. 
They also help to support price increases, and they are key enablers for broadening the relationship with many clients. So this innovation is a key part of our growth algorithm on many fronts, not just the new sales contribution, but it's something that we think is really helping to fuel the repositioning of the company and opening up additional use cases in new client segments, new parts of the market and new solutions for us. 
So with that, why don't I turn it to Alvise to give some more color.

**Alvise Munari** (Executives):
Thank you, Andy, and thank you, Alex, for the question. So we see a continued sustained demand for new solutions for portfolio construction. The demand from all angles of the market for more customized, more bespoke portfolio solutions continues, and that allows us to continue accelerating the success of our custom index franchise. We're also helping accelerate our model franchise, so we launched a custom model service. 
We're also building new factor models at pace. And we're also accelerating the new specialized data sets we are making available to our clients in the market. These are on a range of different aspects of portfolio constructions. There are some very specific new type of signals that we're putting out through our signal library effort on crowding, on specifics of factor models. And there is also new solutions to help people build the objects of the basket, build the solutions. So this is all driving this continued growth of the portfolio ecosystems and is offering us, frankly, a very, very positive environment for the next several quarters to continue this expansion. 
The other area that I would highlight is portfolio solutions. So on the one hand, a significant appetite for new total portfolio solutions, and we have very successfully gone to market in Q3 with a new total portfolio management offering for asset and wealth managers and also a new offering specifically for wealth managers. These, again, are solutions which we see getting more traction in the quarters to come and will continue supporting our growth. 
We also delivered a substantial innovation in the multi-asset class risk space namely by enabling a substantially lower latency intraday capability that will transform how complex multi-asset class investment organization can bring risk to the front office to inform decision-making. 
Finally, I want to highlight what we're doing in the PCS space, the Private Market Solutions, where as it was alluded in the introductory remarks, thanks to the Vantager acquisition, we've brought to market a highly differentiated and valuable fund diligence and document management solution that is getting a lot of traction, and we also see that continuing and massively expanding its appeal to investors.

**Operator** (Operator):
Our next question in queue coming from the line of Scott Wurtzel with Wolfe Research.

**Scott Wurtzel** (Analysts):
A similar question on the product side, maybe switching to more of a kind of AI-focused topic. Wondering if in your conversations with customers or any of the deals that you're seeing with customers who are adopting AI products, are you seeing any uplift in deal size associated with that? Any color on that would be great.

**Alvise Munari** (Executives):
So the solution I alluded to in my earlier answer, especially in the private market space, these are all natively agentic solutions. And it is not that people are buying them more because they are agentic, it is that they couldn't be delivered and built without the support of latest-gen LLM technology simply because the amount of syntactic analysis that has to be done, it's only possible, thanks to the usage of latest-gen LLM technology with the right training in the right context, specifically for the analysis and understanding of private asset object. 
So additionally, in the portfolio construction space, all the newest data sets we are releasing, again, are only buildable and can be delivered at scale with the right consistency because of a massive use of agentic capabilities, and clients understand that. So they see that this is intel, it's IP with a transformative value that we couldn't have created beforehand. 
Look, there is another step, which is, that we also are agentifying the way the clients can actually use some of these capabilities. So we delivered within our solution, agents that are specialized in actually doing some of this portfolio construction capabilities for clients, we see this as being a game changer. The biggest limit, frankly, will be not our ability to build, but it will be the ability for the clients to accept this solution in their environment, given that we are building the agents.

**Operator** (Operator):
Our next question coming from the line of Faiza Alwy with Deutsche Bank.

**Faiza Alwy** (Analysts):
I actually wanted to ask about operating leverage and profitability going forward. I know you've historically talked about reallocation of expenses and maybe AI-related efficiencies that are being reinvested in the business. I'm curious if your thoughts have evolved around, is there a time where we can start to see higher operating leverage, maybe more margin expansion and potentially a decline in expenses?

**Henry Fernandez** (Executives):
The answer is no margin expansion. MSCI is a company with incredible opportunities in a new world, which is a world of large amounts of data, huge number of models to help people understand portfolios, either investment portfolios, loan portfolios, insurance risk portfolios and of course, the use of technology to do all of that. So in the past, one of the biggest problems of MSCI is that we've had an enormous number of very attractive organic investments that we haven't been able to fund because we didn't want to touch the margin. 
So now with AI, which I call it a godsend, we have an incredibly positive algorithm, which is we're applying AI to the -- we divided up MSCI into running the existing business and the enhancements of the existing business and what we call growing the business, a lot of the new innovations, new products and in the running of the existing business and the enhancement of the existing business, we're applying AI significantly to gradually lower the growth rate of EBITDA expenses from mid- to high single digits to the low single digits and eventually to negative growth. 
And then we want to put all that money into the growing of the business with all these opportunities that I mentioned earlier in order to expand into new use cases, new client segments, of course, new solutions powered by more data, more models and more technology. So we believe that we're going to have probably a triple benefit of AI. 
The first benefit is the ability to free up capital to invest. The second benefit is that the products that we're creating, as Alvise described, we couldn't do them without agentic processes. And therefore, we can now do that, and we can expand faster and the payoff is going to be larger per product. That's the second benefit. 
And the third benefit is that we think that eventually, we'll be able to disrupt the SaaS software, the SaaS industry, by which our clients consume content from us, content means data and models and analytics, with agentic processes rather than this incredible investment in SaaS software that needs to be made and the like. If you allow me an analogy here, I used to be a media investor in my private equity firm, and in cable, I mean, in media, the transformations went from over-the-air transmission of media to cable transmission of media to streaming media. 
So the SaaS industry is the equivalent of cable. It is an incredible investment to wire every house, every building, everything with copper wires and fiber optic wires, et cetera. So there came a streaming technology that for anybody who has access to an Internet connection, you can have access to all the content in the planet. So we believe that the cable TV type of industry is the equivalent of SaaS and the streaming technology is the agentic technology that could bypass all of that, and we could then get a big benefit as well and increase the number of users of our content all over the world. Instead of having hundreds, we now have maybe tens of thousands of users in our client organizations, we can have hundreds of thousands and eventually millions of users of our content and significantly expand our white space.

**Operator** (Operator):
Our next question coming from the line of Kelsey Zhu with Autonomous Research.

**Kelsey Zhu** (Analysts):
Could you talk a little bit more about your investment into agentic-based AI solutions? And I know you've just talked a little about that in the private market space earlier, but what new products and features are you building in the other segments? And how do you see that changing the competitive landscape for you?

**Alvise Munari** (Executives):
Thank you for the question. So as I alluded to, another area that is being completely revolutionized by agentic capabilities is our model creation factory. So it used to take us several weeks to build and fully calibrate a new model, we can now do it in the space of a couple of hours. At some point, we'll be able to do it in the space of minutes. That transforms what these models can do because we will be literally capable of creating models on demand targeted exactly to the needs of a specific user in a way that it was never possible before. And this done with the same level of quality, integrity and dependability that the MSCI factor model has had for decades. 
Another area is the creation of new specialized data sets. So the ability to do fundamental analysis of not even companies, assets, both asset pointing to public companies and private companies through the use of different artificial intelligence technology is completely transformational. And this allows us to create product offerings that are completely different from what we used to do before. So for instance, our geospatial offering is an example of that. We have just launched a few specialized data sets to help understand the AI value chain. And all of this depends on the agentic ability to basically map companies' characteristics, companies' revenues, companies' assets to very specific characteristics that it would be impossible to do just with humans.

**Operator** (Operator):
Our next question in the queue coming from the line of Owen Lau with Clear Street.

**Owen Lau** (Analysts):
I have a question about your free cash flow guidance. It's being maintained even though you beat the results by quite a bit. I saw that interest expense raised by $6 million. And Andy, you also mentioned higher investments, and we had lots of conversation about these investments already. But I'm just wondering, like are these the main drivers of maintaining the free cash flow guidance or there are some conservatism baking into your guidance? And also, do you expect some kind of incremental revenue or maybe lower expense in 2027 or beyond because of these investments?

**Andrew Wiechmann** (Executives):
Sure. So I would highlight a couple of things. So free cash flow, as you know, can be a little lumpy quarter-to-quarter. So what we saw in the third quarter was heavily driven by one factor in particular, which was interest payments. So we had a significant increase, so $50-plus million of additional interest, cash interest payments in the third quarter related to the financings that we did last year. There can also be lumpiness related to tax payments, even timing of collections, other payment items.
And so I wouldn't focus too much on any given quarter. The reason why we keep the full year guidance and we're confident about the outlook is the collections have been strong, so business growth to put it front and center. So as we continue to grow the top line, as we continue to expand with clients, that translates through to cash collections, and that is what's powering the overall free cash flow for us, even though we do have, as you alluded to, higher expenses in areas. 
I would highlight one of those items that I called out that's leading to higher expenses this year, namely the performance stock options and the additional accruals related to those as our financial performance improves. That's a noncash item. So there are some noncash items in those expenses that aren't going to impact cash flows. Punchline is, as I said, there will be some lumpiness quarter-to-quarter. The timing of some of those items can push swings, but we continue to be confident about the momentum of the business and the top line growth, and that will, over time, translate through to better cash flows for the business. 
As you know, that's a key part of our financial algorithm. We are always focused on driving very compelling EPS growth and free cash flow growth and particularly free cash flow per share growth over time.

**Operator** (Operator):
Our next question coming from the line of George Tong with Goldman Sachs.

**Keen Fai Tong** (Analysts):
You mentioned double-digit growth across your non-asset manager segments. Can you put a finer point on where within the double-digit range that growth is running and whether that year-over-year growth accelerated from the prior quarter?

**Andrew Wiechmann** (Executives):
Yes. And listen, I don't want to get too specific because the amounts can move around a little bit quarter-to-quarter here. But if you look on an organic basis across the organization, we saw solid double-digit growth with asset owners, as we alluded to, so north of 12%. Hedge funds, we continue to see as our highest growth client segment. So I think it was roughly 18% growth with hedge funds, see roughly 10% growth in areas like broker dealers and banks and elevated growth in other pockets as well. 
And so that collection of opportunities is being fueled by innovations that we've been making. As we've alluded to before, we've continued to develop new products and solutions that are fit for purpose for many of these client segments. We're also enhancing our go-to-market efforts around many of these client segments. Those are translating through to elevated growth, and that's going to be a key part of our financial algorithm driving that overall double-digit top line growth is continuing to fuel the opportunities across these client segments.

**Operator** (Operator):
Our next question in queue coming from the line of Curtis Nagle with Bank of America.

**Curtis Nagle** (Analysts):
Maybe a 2-parter. Just going back to how to think about sort of the expense structure. So appreciating you're not making any changes to, I guess, the net savings, right, because you're going to be reinvesting and it sounds like an accelerating rate. But in terms of the time line, Henry, to your point, getting to a rate closer to low singles, right, and maybe even negative on a gross basis. Is that something we should be contemplating for next year? Or is that perhaps a longer time line? Just trying to think through, again, how to think through the reinvestment cadence and when that starts to maybe even accelerate further.

**Andrew Wiechmann** (Executives):
And just to be specific on Henry's comment, I think you got this, but to be totally clear, the low single digit and potentially negative in the future referred to our run-the-business expenses. So these are the expenditures in the business that are supporting the existing franchise and existing products as they are today that's an area where AI is being transformative for us. 
So in our production environments, within our data operations, our technology organization, these are areas where AI is dramatically enhancing productivity and efficiency, and that is what's enabling us to take down the rate of growth on the run-the-business expenses. As Henry alluded to, we intend to reinvest those savings. So those productivity enhancements are going into fueling these very attractive organic opportunities that we have in front of us. And so we do intend to reinvest. 
And so the overall expense trajectory and the financial algorithm is not changing per se. It's just AI is enabling us to invest more. And that is, if you will, I guess, I could say, supercharging that algorithm. So it allows us to invest more, which is going to fuel more top line growth, as Henry said, with the same inherent operating leverage or inherent margin dynamics, and that's going to fuel over time higher profitability growth for us. And so it's kind of supercharging what we've done in the past. 
As we head into next year, there are some items that are positioning us well. So things like the severance, which is running higher than we anticipated at the beginning of the year. A lot of the transformations that we've talked about are happening quickly and will continue to happen. Those are things that will help position our expense base for next year. There are also a number of broader initiatives that are positioning us well for next year. 
Now we do intend to, as I said, reinvest a lot of those savings and productivity enhancements, but we've got the levers in our business to make sure in all environments, all dynamics, we've got the ability to flex up and down and continue to drive not only those investments, but also fuel very attractive profitability growth going into next year. And so I don't want to comment specifically on expenses or any targets for next year other than to say we're very confident in our position and the momentum we have in the business, and we think we are setting up well nicely for next year.

**Operator** (Operator):
Our next question in queue coming from the line of David Motemaden with Evercore ISI.

**David Motemaden** (Analysts):
I just had a question on the MSCI connectors and what you guys are seeing so far as clients are building agentic workflows with embedded MSCI data. I'm just wondering if you have any insight into MSCI data consumption by agents and how that compares to human users? And then maybe how we should think about that playing out as agentic use cases continue to gain traction here?

**Alvise Munari** (Executives):
Thank you for the question, David. Look, it's early stages. So we have built connectors for all the main LLM providers. And we've also agentified the experience through our own applications. And for the time being, the evidence is the clients prefer to use our content through our own directly trained and curated capabilities. 
And look, there's 2 reasons for that. Reason number one is that the convergence rate is actually higher, not massively higher, but it's a few points higher. And so you get the better experience going directly via the MSCI application. And the other one is that the client space only has, by and large, limited capabilities at this point. Look, most of our clients only have access to Microsoft Copilot, right? And so this will naturally make for a relatively slow rate of adoption via the mainstream connectors and a faster rate of adoption for the directly controlled connectors because you just connect into MSCI as you've always done historically. That said, that will change. 
And so, look, we're doing 3 things. On the one hand, we are accelerating our connectivity to all the main platforms, whether they are large LLM companies or large cloud data provider companies like Snowflake and Databricks. We are also, as I explained, continuing to invest in our direct agentified access capabilities. And then we're also building own agent capabilities to enable the content on the client side, as Henry alluded to, to transform the experience. Look, we don't know which one of these 3 will prevail, but we are preparing to support all 3. And then gradually, the market will show us what works best. As I said, it's very early stages right now for the reason I said, the MSCI conduits are the most prevalent.

**Operator** (Operator):
Our next question in queue coming from the line of Craig Huber with Huber Research Partners.

**Craig Huber** (Analysts):
I want to talk about Index recurring subscription run rate growth. It's obviously accelerated here in recent quarters, I guess, 10.7% in the first quarter this year, 11.5% second quarter, now it's 12% here in the third quarter, obviously, up from 8.5% to 9.5% the prior 8 quarters. Can you talk about what's going on there in terms of how much AI is potentially helping those revenue growth numbers there? It's quite impressive acceleration there.

**Andrew Wiechmann** (Executives):
Craig, so it has been encouraging. We've got good momentum there. As you said, we continue to see an acceleration. I'd say the themes at this point are consistent with what we've talked about recently. So we have a huge focus on building the trading and liquidity ecosystem around our indexes. And correspondingly, we have very strong traction with hedge funds and traders. 
Within Index, we saw a 32% growth with hedge funds on the subscription run rate side. We saw a 15% growth with banks and brokers. A lot of that success was on the heels of many of the new modules that we have released. And as Alvise and I indicated earlier, our ability to develop these modules, these content sets is enabled by AI. Our ability to get to market faster is enabled by AI. So AI is definitely helping on the pace of innovation, the productivity front, and that is helping to enable the sales. 
I would say more generally across Index, we are seeing good momentum, including areas like asset owners and wealth managers, where we're seeing 10% plus growth. And so we're seeing momentum across the board. Asset managers have been reasonably steady for us, but they are licensing more content from us. We're helping them by licensing solutions that help them in, as you know, active ETFs, help them move to be more systematic in their investment processes. And so we've seen pretty steady momentum with asset managers. And a lot of that is fueled by innovation, better services, access to more content that is fueled by underlying AI. 
I would say looking forward here, there are dynamics that can even enhance that further. So I know we've talked about this a little in the past, but many clients are starting to want to have access to our content to be able to train models, to use more content involved in an agentic investment process. This is very early days. And so the impact has been small to us at this point, but those are things that can create additional demand on top of all the great things we're doing today. 
The last thing I would highlight, and we've talked about this a lot in the past, custom indexes, which are a reflection of that move towards systematic investing, and we are best positioned to be able to help clients make that transition. We saw 26-plus percent growth in custom index run rate -- subscription run rate. And so we continue to have very strong momentum on that front. 
Our capabilities there are enabled by AI, and we continue to broaden our ability to do more custom indexes with a faster turnaround, and that's something that's enhanced by AI. So listen, we're very encouraged overall by the momentum in Index subscription. It is fueled by the innovations we've been making and AI is an accelerant on that. So all good things for us on that front.

**Henry Fernandez** (Executives):
Let me add one other comment. When we sort of sit back and look at the totality of our Index subscription business, in addition to the significant growth that we see in the focus on indices on the assets, a lot of our business on Index has been focused on monetizing the amount of assets that are in the ecosystem of our index, $23 trillion, of which more than $8 trillion is passively managed. 
In addition to that, we have found huge white space in developing products on the trading of the assets, the trading of the assets, not just the assets, but the trading of the assets. So what data sets are going to help traders, market makers, broker dealers, exchanges, help facilitate the flow of trading of that -- of those assets. And that's why you see this significant growth in Index in traders and hedge funds, for example. And we're not even yet penetrating the market makers. We're working on that, but that's not yet even on the numbers. So we believe that this white space is going to create another layer of growth in our Index subscriptions.

**Operator** (Operator):
Our next question in queue coming from the line of Ashish Sabadra with RBC Capital Markets.

**Ashish Sabadra** (Analysts):
I just wanted to circle back to an earlier question from Faiza on operating leverage. Henry, if I understood your comment that no margin expansion, did I hear that right? And is that just for -- I was just wondering if you could provide some time line around that no margin expansion. And maybe just a follow-up there. Obviously, you've had a great track record of these investments. How should we think about the ROIC on these investments, but also how quickly do these investments translate into revenue growth?

**Henry Fernandez** (Executives):
That's a great question, Ashish. Look, as one of the largest shareholders in the company, I would love to see high valuations today in the next couple of years. But I'd rather see a company double or triple the size in 10 years compared to what it would otherwise be if we let the margin rise. So we, for sure, have a huge inherent pressure, if you want to call it, in the operating leverage increasing. And it's not easy when you see that and having to mobilize to invest the additional sort of revenues -- additional cash flows coming from the operating leverage. 
When we sit down every year to analyze all the investments that we have, we have to stop. We have to draw the line on organic investments in places that have sometimes triple-digit returns, high double-digit IRRs with relatively short payoff because we don't have the organic capital to do that, meaning we do have the capital, it's just that you got to expense it first before you get generate the revenues, and we do not want to lower the margin. That's for sure. 
But what we can do is not let it increase. There will probably be a marginal increase in the margin because every time we budget something, we build a cushion and the cushion typically doesn't get eaten. And therefore, there is 20, 30, 50 basis points of increases. But that is just because of the nature of our budgeting process and our conservatism, not because we're targeting an increase in the margin. So the end result is our strategy is that we're going to like this company a lot better if it's 2x, 3x bigger than it would otherwise be if we let the margin rise because of the opportunities we have. So that's the process of doing all of this. 
Now as I mentioned to you, we have a huge installed base of customers. We're gradually moving into new customers and new client segments. Everything we built is on top of an already existing infrastructure. So the larger the infrastructure like an Index, the higher the payoff relative to a lower infrastructure. So the profitability of these organic investments are huge because as the sort of sum cost of the infrastructure is built, the incremental money required or capital for a particular amount of payoff the incremental capital goes down for the same payoff. So it's going to increase the operating leverage even more than before.

**Operator** (Operator):
Our next question in queue coming from the line of Alex Kramm with UBS.

**Alex Kramm** (Analysts):
Just a quick follow-up from my part. On the asset manager customer base, first of all, Andy, I don't think you gave a specific number about the run rate growth. You usually do that, so it would be great to have that. But then more importantly, it sounds like a lot of the momentum, and this is a good thing, is coming from some of the new products and the newer customer bases. I think in the past, you may have talked about some of these newer products also applying to asset managers. So I'm just wondering, are sales cycles longer there? Are you still confident that some of these newer products can, at some point, also click into gear? And do you have to change anything to maybe do a better job on the sales front with that customer base?

**Andrew Wiechmann** (Executives):
Sure. So yes, just for reference, Asset Manager organic subscription run rate growth was around 6%. I mentioned within Index, it was around 8%. As I alluded to, that's been reasonably steady for us. Retention is pretty steady as well, maybe slightly up, very slightly up from a year ago. Listen, there has been some benefit from several years of equity markets rising. We see reasonably healthy dynamics in many areas with asset managers. And you can tell from the op metrics and solid retention rate. 
There are still those secular pressures on asset managers, and those are likely to continue. But as you alluded to, we are in a position to help them. And so we are innovating. We're enhancing our servicing model. We're helping them transition to those areas where they see asset growth and fee stability. And so we are in a good position to help them overall. And so we think asset managers are going to be an important part of our client base. They're an important part of the investment ecosystem, but they're going to be more of a steady grower, and we're expecting outsized growth from other areas. 
And if you look at the environment and the backdrop for other client segments, we see it being pretty constructive in areas like hedge funds, banks, traders, asset owners, wealth managers. It's a pretty constructive backdrop with them. And obviously, Index managers have been doing exceptionally well, and we've been doing well with them. So overall, it's a pretty good environment. We've seen steady progress with asset managers, and we think we're in a good position to help them continue to evolve and adapt to changes in the investment process and the investment industry.

**Operator** (Operator):
Our next question coming from the line of Jason Haas with Wells Fargo.

**Keegan Antico** (Analysts):
This is Keegan Antico, on for Jason. I'm curious what you're seeing from your hedge fund end market and particularly quant funds that have been consuming more of your data and new product launches. Do you think that there's a potentially cyclical component to this and some of this growth could moderate in fiscal year '27? Or are you seeing these funds remain highly profitable with continued inflows that could potentially lead to more funds emerging that you can sell into?

**Alvise Munari** (Executives):
Thank you. Very important question. We see this as being a structural trend in the market, especially in the equity market, but we believe that the fixed income market at some point will also follow the same path. And the path is the following. The unit of conversation in the market has gone from being the single stock to being the portfolio. The portfolio in all possible ways, possible logic, possible definitions. This is something which intrinsically requires a heightened ability to make markets in complex objects at scale, at speed. 
And this is why in the face of capital limitations from the traditional players, i.e., the broker-dealers and the massive, massive increase of the demand from this portfolio ecosystem is making a very big opportunity get even bigger for the most sophisticated market makers and the hedge funds that effectively play the role of market makers to create an investment function. Because this primacy is supported by very significant investment in the technology capabilities and superior access to the market, I think this is a trend that is there to stay. 
Now can there be short-term reversal? Yes, of course, it can be, right? Market never goes in just one way all the time, but this is a structural transformation. And because, let's say, the unit of conversation is the portfolio, and we are the portfolio guys, we're going to be a massive beneficiary of this continued trend.

**Operator** (Operator):
Our next question coming from the line of Alexander Hess with JPMorgan.

**Alexander EM Hess** (Analysts):
Maybe just a quick follow-up on 2 initiatives that were pretty prominent for you and the story maybe a year ago. I would like to hear a bit more about the latest on active ETFs. And then has anything changed with respect to the Moody's private credit ratings partnership? I know they had an announcement out there with a third firm. So I would be interested to know on latest updates on both those fronts.

**Alvise Munari** (Executives):
So on the active ETF front, as Andy alluded, we've seen significant growth because essentially, the vast majority of asset management firms or traditionally active asset management firms are converting many of the products at an accelerated pace into ETFs. 
The process of doing so entails a couple of ingredients. One, most of the time, the conversion takes the products to be closer to being systematically built products, which, of course, creates a lot of opportunities for our tools and capabilities to help the managers do the transition. 
So Alex asked Andy earlier if some of the tools we built for the broker-dealer trading and hedge fund and market making communities at some point will be usable for asset managers. The answer is absolutely yes because the growth of this active ETF market will entail these objects being managed more systematically at greater scale with greater level of customization. And the platforms we've built to help traders, hedge funds, broker-dealers market makers to do that will absolutely be fungible for asset managers. And so we see that continuing and being a trend which we also facilitate. 
Same for a lot of the capabilities we're building in portfolio creation, basket creation and the specialized data set that can be used to create specific flavors for these new active ETF objects. So as I said, I see the trend continuing and I see the trend being very positive for us.

**Operator** (Operator):
And I'm showing there are no further questions in the Q&A queue at this time. I will now turn the call back over to Mr. Henry Fernandez for any closing remarks.

**Henry Fernandez** (Executives):
Thank you, operator. Before we sign off, I would like to share that this is the final earnings call in which Jeremy Ulan will be serving as MSCI's Head of Investor Relations. At the end of this month, Jeremy will move to a new and exciting role at MSCI as the Lead Finance Director for Client Segments and Solutions. And as we expand into a variety of new client segments, we needed better financial management for that, and Jeremy will provide that leadership in addition to his current role as Treasurer of the firm. Craig Carter, currently our Head of Corporate Development, will take over as Head of IR. I want to thank Jeremy for all his incredible contributions to the IR team and welcome Craig to his new position. 
Looking ahead, MSCI continues to expand our footprint with client segments, traditional client segments and newer client segments across the investment ecosystem as we accelerate our product innovation using AI and other advanced modeling and technologies. We have a great franchise for the age of AI. AI is the most useful in places where you have large amounts of data, big number of modeling and the use of a lot of technology, and that's what MSCI is. We remain intensely focused on delivering long-term compound growth and long-term value creation for our shareholders. 
Thank you for listening, and we'll keep you posted throughout the quarter.

**Operator** (Operator):
Ladies and gentlemen, this concludes today's conference call. Thank you for your participation, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MSCI_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO Andrew Wiechmann｜guidance：永續與氣候合併板塊未來兩季 recurring net new sales 預期約零到小幅為負（原話："roughly zero to slightly negative"）
- 2026-07-21｜CFO Andrew Wiechmann｜guidance：First Street 交割（Q3）後預期增加約 $10M 訂閱 run rate（原話："add about $10 million of subscription run rate"）
- 2026-07-21｜CFO Andrew Wiechmann｜guidance：費用指引上調；4 月曾說會落在高端區間（原話："towards the high end of the expense guidance ranges"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：費用指引上調原因之一：績效股票薪酬與獎金應計（原話："performance stock-based comp and bonus accruals"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：利息費用上調歸因於循環信貸餘額上升（原話："driven by the higher revolver balances"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：自由現金流指引上調歸因於收款增加（原話："it's driven by a pickup in collections"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：ABF 費率下滑：Q2 主因為資產成長與組合轉移（原話："it was heavily mix shift driven"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：BlackRock 協議延長後，部分大型產品底價（floor）降低（原話："we do now have lower floors on certain large products"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：Analytics 利潤率：管理層不看單一板塊或單季利潤率（原話："we don't focus heavily on the margin in any specific segment"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：Analytics 費用年比受去年或有對價回沖影響（原話："contingent consideration reversal"）
- 2026-07-21｜CEO Henry Fernandez｜capital_allocation：本季至昨日回購 $147M 股份（原話："repurchasing $147 million of MSCI shares"）
- 2026-07-21｜CEO Henry Fernandez｜capital_allocation：管理層稱費用上調是自願加碼投資而非被迫（原話："we voluntarily feel that we will want to invest more"）
- 2026-07-21｜CEO Henry Fernandez｜commitment：CEO 表示對看淡者的賣盤願意接手（原話："we're prepared to put a bid on the other side of that trade"）
- 2026-07-21｜CFO Andrew Wiechmann｜commitment：承諾可彈性調整投資與費用（原話："levers to flex investments up and expenses down"）
- 2026-07-21｜CFO Andrew Wiechmann｜competition：永續市場整合中，MSCI 稱在取得市佔（原話："we are capturing share gains in a consolidating market"）
- 2026-07-21｜CEO Henry Fernandez｜competition：CEO：客戶向 MSCI 集中，將是最後倖存的大型業者（原話："we're going to be the last big entity standing"）
- 2026-07-21｜CFO Andrew Wiechmann｜risk：永續取消（尤其美洲）為顯著逆風（原話："cancels, particularly in the Americas"）
- 2026-07-21｜CEO Henry Fernandez｜risk：CEO 稱永續為長期循環性下行而非結構性（原話："protracted cyclical downturn on the use of sustainability"）
- 2026-07-21｜CEO Henry Fernandez｜risk：CEO 改口：先前預期約兩年（原話："going to be like a couple of year process"）
- 2026-07-21｜CEO Henry Fernandez｜risk：主動型管理人資金流仍受抑（原話："the flows are still muted"）
- 2026-07-21｜CEO Henry Fernandez｜risk：管理層預告逐季變異將增加（原話："there will be more variability quarter-by-quarter"）
- 2026-07-21｜CEO Henry Fernandez｜product：兩季內推出 80 多項新產品（原話："80-plus in the last 2 quarters"）
- 2026-07-21｜CFO Andrew Wiechmann｜product：上半年新產品對新銷售貢獻年增約 40%（原話："it's up around 40% compared to a year ago"）
- 2026-07-21｜CFO Andrew Wiechmann｜product：推出主動 ETF 專用授權（原話："we actually recently launched our active financial product"）
- 2026-07-21｜CFO Andrew Wiechmann｜product：簽下首份模型訓練授權，目前貢獻小（原話："we actually very recently signed our first training license"）
- 2026-07-21｜CEO Henry Fernandez｜product：IndexAI Insights 2 月推出，已逾千客戶使用（原話："We already have over 1,000 clients using IndexAI Insights"）
- 2026-07-21｜CEO Henry Fernandez｜product：與 UBS 的合作目前僅是條款書層級，未計入數字（原話："which is not in the numbers, by the way"）
- 2026-07-21｜CEO Henry Fernandez｜customer：避險基金與交易商 index 新銷售增逾三倍（原話："more than tripled our index recurring net new sales"）
- 2026-07-21｜CEO Henry Fernandez｜customer：避險基金本季為紀錄最佳（原話："best quarter on record with 19% subscription run rate growth"）
- 2026-07-21｜CEO Henry Fernandez｜customer：CEO 稱大型避險基金的指數套利付費偏低（原話："getting paid too little for the index arbitrage"）
- 2026-07-21｜CFO Andrew Wiechmann｜customer：非 ETF 被動型 AUM 約 $5 兆（原話："the non-ETF passive AUM is around $5 trillion as of June 30"）
- 2026-07-21｜CFO Andrew Wiechmann｜customer：價格上調對新銷售貢獻近幾季穩定（原話："the overall contribution has been pretty consistent"）
- 2026-07-21｜CFO Andrew Wiechmann｜customer：Q3 迄今 ETF 資金流仍強（原話："continued to see exceptional cash flows in the ETFs"）
- 2026-07-21｜CEO Henry Fernandez｜customer：CEO 稱避險基金與交易商處於前 2、3 局（原話："the first 2, 3 innings would be my guess"）
- 2026-07-21｜CEO Henry Fernandez｜customer：Analytics 銷售偏弱，CEO 歸因為不規則（原話："It's all lumpiness."）
- 2026-07-21｜CEO Henry Fernandez｜competition：CEO 與一年前口徑對比：當時說情況不佳，現在相反（原話："telling you things were not looking that great"）

### 問答異常語氣（迴避／改口／保留）
- MSCI_Q2_2026_Earnings_Call_20260721.md｜問：Manav Patnaik：本季訂閱銷售略低於預期，前瞻動能如何｜答法：CEO 未直接回應低於預期的數字，轉談新產品管線、過去三季優於共識及逐季變異
- MSCI_Q2_2026_Earnings_Call_20260721.md｜問：Owen Lau：ABF 費率下滑的來源（分級定價 vs 競爭）及未來費率｜答法：CFO 歸因組合轉移與底價調整，稱費率為路徑依賴，未給前瞻費率，也未正面回應競爭因素
- MSCI_Q2_2026_Earnings_Call_20260721.md｜問：Kelsey Zhu：Analytics 利潤率偏軟及下半年軌跡｜答法：CFO 稱不看單季或單板塊利潤率，未提供下半年利潤率軌跡
- MSCI_Q2_2026_Earnings_Call_20260721.md｜問：Toni Kaplan：MCP 資料銷售的牽引力與未來基期波動｜答法：CEO 只談避險基金波動，未回答 MCP 問題

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
{"date":"20260929","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回到 474 美元以下（FY1 本益比 24 倍），且 Index 有機訂閱 run rate 年增仍在 10% 以上","irr_base_pct":8.7,"ev5y_pct":45.1,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.8,"ev5y_pct":45.1,"irr_base_pct":8.7,"max_dd_pct":-45,"bull_5y_price":1185.0,"bear_5y_price":401.4,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價回到 474 美元以下（FY1 本益比 24 倍），且 Index 有機訂閱 run rate 年增仍在 10% 以上","price_at_dd":542.72,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
