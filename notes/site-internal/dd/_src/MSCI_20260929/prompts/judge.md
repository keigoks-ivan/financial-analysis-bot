你是 stock-analyst **v20 判斷 agent**，標的 MSCI（20260929）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
  *eps
    *bull[]: arr ≥1 num
    *base[]: arr ≥1 num
    *bear[]: arr ≥1 num
  *pe
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
- `counter_evidence.blind_spots[].view`：論點失敗｜論點成功但股東經濟變差｜價格已反映太多
- `decision_inputs.signal`：A+｜A｜B｜C｜X
- `decision_inputs.ma`：🟢｜✅｜🟡｜🟠｜❌｜-
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
{"meta":{"ticker":"MSCI","date":"2026-09-29","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20260929/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20260929/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_operating_revenue_","label":"Total operating revenue (GAAP)","value":867.0,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com「MSCI Reports Financial Results for Second Quarter and Six Months 2026」"},"note":"consensus 約 $864.08M，實際 $867.0M 略勝（來源：web_search 彙整市場預期，非本站 dd_numbers_extra 結構化欄）"},{"id":"f_kpi1_adjusted_ebitda_margin_n","label":"Adjusted EBITDA margin (non-GAAP)","value":62.1,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release（Adjusted EBITDA $538.5M，YoY +13.5%）"},"note":"未查得 sell-side 對 Adj. EBITDA margin 的共識數字"},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":56.2,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"10-Q（SEC EDGAR msci-20260630.htm）與公司新聞稿一致：營業利益 $487.5M／營收 $867.0M"},"note":"未查得共識數字（GAAP operating margin 非 sell-side 常態追蹤指標）"},{"id":"f_kpi3_free_cash_flow_non_gaap","label":"Free cash flow (non-GAAP)","value":326.4,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release"},"note":"未查得共識數字"},{"id":"f_kpi4_stock_based_compensation","label":"Stock-based compensation as % of revenue（推算）","value":2.93,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21，推算值）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21，推算值）","citation":"推算：Q2 10-Q 現金流量表揭露 H1 FY2026 SBC 累計 $73.1M，減去 Q1 10-Q（三個月至2026-03-31）揭露的 Q1 SBC $47.7M，得 Q2 單季 SBC ≈ $25.4M；MSCI 10-Q 現金流量表僅揭露年初至今累計數，未單獨揭露單季數字"},"note":"不適用"},{"id":"f_kpi5_retention_rate","label":"Retention Rate","value":95.3,"period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release"},"note":"不適用（公司自報營運指標，非 sell-side 財務預估項目）"},{"id":"f_kpi6_index_analytics_organic_","label":"Index／Analytics organic recurring subscription Run Rate growth","value":"Index 11.1% / Analytics 6.6%","period":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（季末 2026-06-30，公告 2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release"},"note":"不適用"},{"id":"f_kpi7_fy2026_guidance_q2","label":"FY2026 全年財測（管理層 guidance，於Q2財報會議重申／更新）","value":"Opex $1,535–1,575M；Adjusted EBITDA Expense $1,340–1,370M；Capex $160–170M；Free Cash Flow $1,485–1,545M","period":"隨 Q2 FY2026 財報發布（2026-07-21）","unit":"USD millions（區間）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"隨 Q2 FY2026 財報發布（2026-07-21）","citation":"公司新聞稿 ir.msci.com Q2 FY2026 press release"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-07-21","period":"2026-07-21","unit":"date","basis":"距今 50 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-07-21"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_msci_gross_margin_pct","label":"MSCI 毛利率","value":82.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSCI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msci_operating_margin_pct","label":"MSCI 營業利益率","value":55.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSCI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_msci_fcf_margin_pct","label":"MSCI FCF 利潤率","value":44.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSCI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_spgi_gross_margin_pct","label":"SPGI 毛利率","value":70.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPGI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_spgi_operating_margin_pct","label":"SPGI 營業利益率","value":41.56,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPGI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_spgi_fcf_margin_pct","label":"SPGI FCF 利潤率","value":34.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPGI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_gross_margin_pct","label":"MCO 毛利率","value":74.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_operating_margin_pct","label":"MCO 營業利益率","value":46.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mco_fcf_margin_pct","label":"MCO FCF 利潤率","value":36.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fds_gross_margin_pct","label":"FDS 毛利率","value":51.38,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FDS.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fds_operating_margin_pct","label":"FDS 營業利益率","value":29.55,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FDS.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_fds_fcf_margin_pct","label":"FDS FCF 利潤率","value":29.05,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FDS.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":542.72,"period":"2026-09-28（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":2.77,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":41.21,"period":"2026-09-28（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.74 → 19.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.5 → 22.5）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.08,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（25.52 → 25.54）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":19.74,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":22.5,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":25.54,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":29.64,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":11.84,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":13.69,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":27.49,"period":"2026-09-26","unit":"x","basis":"分母＝FY1 EPS 19.74，分子＝快照價 542.72","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-26"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-09-29","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 542.72 / W52 565.73 / W104 564.28 / W250 517.85 / W250 13週斜率 -0.08%"},{"id":"f_ma_w52","label":"52 週均線","value":565.73,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":564.28,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":517.85,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.08,"period":"2026-09-29","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#none","axis":"competitive_share_entrants","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"MSCI's FY2023 10-K discloses BlackRock as its largest client organization by revenue, at 9.8% of consolidated operating revenues, with 95.4% of BlackRock's revenue to MSCI coming from asset-based fees on ETFs/non-ETF products using MSCI indexes — a concentration/single-client dependency risk factor.","source":"MSCI Inc. Form 10-K FY2023 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819824000030/msci-20231231.htm","excerpt":"our largest client organization by revenue, BlackRock, accounted for 9.8% of our consolidated operating revenues","as_of":"2023-12-31","retrieved_at":"20260929","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"BlackRock is MSCI's largest client, accounting for 10.8% of consolidated operating revenues for FY2025; 96.5% of that BlackRock-derived revenue comes from asset-based fees on BlackRock's ETFs and non-ETF products tracking MSCI indexes.","source":"MSCI Inc. 10-K FY2025 (filed 2026)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"For the year ended December 31, 2025, our largest client organization by revenue, BlackRock, accounted for 10.8% of our consolidated operating revenues, with 96.5% of the operating revenues from BlackRock coming from fees based on the assets in BlackRock's ETFs and non-ETF products that are based on our indexes.","as_of":"2025-12-31","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"MSCI discloses risk that its largest clients (including BlackRock) may negotiate lower asset-based fees, stop using MSCI indexes, or cancel/reduce usage, which could have a material adverse effect on results.","source":"MSCI Inc. 10-K FY2025 (filed 2026), Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"The possibility that our clients seek to negotiate lower asset-based fees or cease using our indexes as the basis for indexed investment products / Cancellations or reductions by our clients or reduced demand for our products or services","as_of":"2025-12-31","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"BlackRock accounted for 18.7% of MSCI's Index segment operating revenues for FY2025 (vs. 17.4% in FY2022), indicating rising within-segment concentration over time.","source":"MSCI Inc. 10-K FY2025 (filed 2026)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"BlackRock's own balance sheet/credit shows no distress: its March 2026-amended $6.3B revolving credit facility (extended to March 2031) requires a max leverage ratio of 3.5x, and BlackRock's actual leverage was under 1x as of June 30, 2026, with nothing drawn on the facility.","source":"BlackRock, Inc. 10-Q filings for Q1 and Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0002012383/000119312526337177/blk-20260630.htm","excerpt":"In March 2026, the 2026 Credit Facility was amended to increase the aggregate commitment amount by $400 million to $6.3 billion and extend the maturity date to March 2031. The 2026 Credit Facility requires the Company not to exceed a maximum consolidated leverage ratio of 3.5 to 1, which was satisfied with a ratio of less than 1 to 1 at June 30, 2026, with no amount outstanding under the 2026 Credit Facility.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MSCI Q2 2026 organic recurring subscription Run Rate growth was 8.1%; retention rate rose to 95.3% from 94.4% a year earlier, indicating durable recurring demand rather than a cyclical spike.","source":"MSCI Inc. Q2 2026 earnings release","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-second-quarter-and-six-months-10","excerpt":"Organic recurring subscription Run Rate growth was 8.1%. Retention Rate in second quarter 2026 was 95.3%, compared to 94.4% in second quarter 2025.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MSCI saw record ETF inflows linked to its indexes in Q1 2026 (north of $100B), with $2.4T in ETF AUM and over $21T total benchmarked to MSCI indices, reflecting continued structural growth in passive/index-linked demand.","source":"Foreign Policy Journal, citing MSCI Q1 2026 earnings materials","url":"https://www.foreignpolicyjournal.com/2026/04/18/msci-approaches-q1-earnings-with-index-division-running-at-record-7-trillion-in-etf-linked-assets/","excerpt":"MSCI saw record inflows into ETFs linked to its indexes in the first quarter of 2026, with inflows north of $100 billion... over $21 trillion benchmarked to MSCI indices, including $2.4 trillion in ETF products.","as_of":"2026-03-31","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"查無 MSCI Inc（指數/資料商）遭 DOJ、FTC 或 EU 反壟斷調查或拆分風險之報導；搜尋結果中提及的反壟斷案例為 ISS/Glass Lewis（代理投票顧問）及 Microsoft/Google 等科技公司，非 MSCI。","source":"WebSearch aggregate (no direct hit)","url":null,"excerpt":null,"as_of":"2026-09-29","retrieved_at":"20260929","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"MSCI 10-K 揭露：2024 年 11 月歐盟通過 ESG 評等透明度與誠信規範 (EU) 2024/3005，要求在歐盟境內營運的 ESG 評等提供者須於 2026 年 7 月 2 日起取得 ESMA 授權或註冊；MSCI 表示其部分永續與氣候相關產品預期將受此規範管轄。","source":"MSCI Inc. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1408198/000140819826000011/msci-20251231.htm","excerpt":"In November 2024, the European Union adopted Regulation (EU) 2024/3005 on the transparency and integrity of ESG rating activities, which will require ESG rating providers operating in the European Union to be authorized by, or registered with, ESMA beginning July 2, 2026.","as_of":"2026-02-01","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"MSCI 10-K 一般性風險揭露：全球指數/標竿業持續面臨來自 EU、美國及其他地區監管者、政策制定者與媒體對指數業角色與影響力的高度關注，可能帶來負面輿論或新規；MSCI Limited 為 UK FCA 授權之標竿管理機構，MSCI Deutschland GmbH 亦持有德國 BaFin／ESMA 授權。","source":"MSCI Inc. Form 10-K FY2025 (SEC EDGAR) / MSCI Benchmark Regulations page","url":"https://www.msci.com/indexes/index-resources/benchmark-regulations","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20260929","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"台灣占 MSCI 新興市場指數(EM Index)權重達 24.8%（2026-04-30 資料），為指數內最大權重國家，主因 AI 驅動半導體需求；同期資訊科技板塊權重由 31.8% 升至近 37%。此為 MSCI 旗艦指數產品在地緣風險區域（台灣/中國）的集中曝險。","source":"MSCI - Markets in Motion: Taiwan at the Top, EM Weight Breakdown","url":"https://www.msci.com/indexes/markets-in-motion/visualizations/taiwan-at-the-top-msci-em-weight-breakdown","excerpt":"Taiwan held 24.8% of the index as of April 30, 2026.","as_of":"2026-04-30","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Index 營收段 H1 2026 營收年增17.6%，資產基礎費(asset-based fees)年增26.6%為主動能，訂閱型營收年增10.3%；掛鉤MSCI股票指數的ETF資產年增34.6%，但平均基點費率下滑部分抵銷成長。","source":"MSCI Reports Financial Results for Second Quarter and Six Months 2026 (IR新聞稿)","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-second-quarter-and-six-months-10","excerpt":"Index operating revenues increased 17.6% for the six months ended June 30, 2026, primarily driven by growth from asset-based fees as well as recurring subscriptions... Operating revenues from asset-based fees increased 26.6%... ETFs linked to MSCI equity indexes and non-ETF indexed funds linked to MSCI indexes increased by 34.6% and 12.2%, respectively, primarily driven by an increase in average AUM, partially offset by a decrease in average basis point fees.","as_of":"2026-07-21","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Analytics 營收段 Q1 2026 營收$190.0M年增10.3%(organic 10.5%)；Q2 2026原guidance約5%成長，訂閱銷售成長因lumpiness與高基期而放緩；成長動能來自Multi-Asset Class與Equity Analytics產品，避險基金、銀行/券商、資產管理客群為主要貢獻。","source":"MSCI Reports Financial Results for First Quarter 2026 (IR新聞稿)","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-first-quarter-2026","excerpt":"Analytics operating revenues were $190.0 million, up 10.3%, with organic operating revenue growth for Analytics at 10.5%... The increase was driven by growth in both Multi-Asset Class and Equity Analytics products, and reflected growth across all regions, primarily led by hedge fund managers, banking and brokerages and asset managers client segments.","as_of":"2026-03-31","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Sustainability and Climate（原ESG and Climate）營收段 Q2 2026 Climate Run Rate跨產品線年增近12%；First Street收購案預期為該營收段增加約$10M訂閱Run Rate。","source":"MSCI Inc (MSCI) Q2 2026 Earnings Call Highlights - GuruFocus","url":"https://www.gurufocus.com/news/8970269/msci-inc-msci-q2-2026-earnings-call-highlights-strong-growth-amid-market-challenges","excerpt":"Climate Run Rate Growth reached nearly 12% across MSCI product lines in Q2 2026. Additionally, the First Street Acquisition was expected to add about $10 million of subscription run rate to the Sustainability and Climate segment.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"All Other–Private Assets 營收段 Q1 2026營收$72.6M年增7.9%(organic 5.3%)；Q2 2026營收$74.7M年增4.9%(organic 4.4%)，organic訂閱Run Rate年增8.3%；成長動能來自Private Capital Solutions（Total Plan Manager、Private Capital Transparency Data、Private Capital Intel）。成長率較其他三段明顯放緩。","source":"MSCI Reports Financial Results for Second Quarter and Six Months 2026 (IR新聞稿)","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-second-quarter-and-six-months-10","excerpt":"All Other – Private Assets operating revenues were $72.6 million, up 7.9%, with organic operating revenue growth of 5.3%... All Other – Private Assets operating revenues were $74.7 million, up 4.9%, with organic operating revenue growth of 4.4%... organic recurring subscription Run Rate growth for All Other – Private Assets was 8.3% in Q2 2026.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"被動ETF市場2026年估值達$16.8兆，但主動型ETF數量已在2025年6月超越被動型ETF；主動ETF資產達$1.47兆、近三年CAGR 59%，顯示主動策略在ETF資金流結構性搶佔份額，對MSCI核心被動指數授權/資產基礎費成長模型構成潛在逆風。","source":"Active vs. Passive ETFs: How the 2026 Active Surge Changes the Math - etf.com","url":"https://www.etf.com/sections/etf-basics/active-vs-passive-etfs-how-2026-active-surge-changes-math","excerpt":"The number of active ETFs surpassed the number of passive ETFs in June 2025, with 2,187 passive ETFs and 2,741 active ETFs available by year-end. Active ETF assets have crossed $1.47 trillion, growing at a 59% compound annual rate over the last three years.","as_of":"2025-12-31","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AI/LLM 工具可低成本自動解析企業永續揭露、複製部分 ESG 評等結果；若機構投資人認為 MSCI ESG Ratings 與 AI 生成替代品區隔不足，MSCI 的評等定價溢價可能被侵蝕","source":"PitchGrade Research - \"MSCI: Index Licensing and ESG Data Franchises in the Age of AI-Powered Analytics\"","url":"https://pitchgrade.com/research/msci-ai-margin-pressure","excerpt":"If institutional investors conclude that MSCI ESG Ratings are insufficiently differentiated from AI-generated alternatives, the pricing premium erodes","as_of":"2026-01-29","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"新興自助式指數設計平台（如 S&P SPICE、Merqube 的 Garage）讓客戶自行客製指數規則，不再依賴指數商內部量化團隊人力；MSCI 已於 2024 年併購 Foxberry F9 平台因應此一產業趨勢","source":"Panta.ai - \"Will Self-Service Indexing Gain Wide Adoption?\"","url":"https://panta.ai/self-service-indexing-adoption/","excerpt":"custom index design is no longer constrained by how many quants or product people a provider can throw at a request","as_of":"2025-11-19","retrieved_at":"20260929","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師共識維持 Buy／Strong Buy，平均目標價約 $692–$713（不同彙整站數字略有差異），最低 $570、最高 $760；平均目標價較現價估計有約 24.5% 上行空間","source":"stockanalysis.com / wallstreetzen.com 分析師預測彙整頁","url":"https://stockanalysis.com/stocks/msci/forecast/","excerpt":"According to 18 analysts polled by S&P Global, MSCI Inc. stock has a consensus rating of \"Buy\" and an average price target of $692.06. The lowest analyst price target is $570 (+2.57%) and the highest is $760 (+36.76%).","as_of":"2026-09","retrieved_at":"20260929","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"MSCI 2026 Q2 財報後上修 2026 全年費用 guidance：營運費用上修至 $1,535M–$1,575M（原 $1,490M–$1,530M），Adjusted EBITDA 費用上修至 $1,340M–$1,370M（原 $1,305M–$1,335M），主因近期併購（含 First Street）及 AUM 動能超過先前假設","source":"MSCI Reports Financial Results for Second Quarter and Six Months 2026 (businesswire/ir.msci.com)","url":"https://ir.msci.com/news-releases/news-release-details/msci-reports-financial-results-second-quarter-and-six-months-10","excerpt":"the company updated operating expense guidance to $1,535M–$1,575M (up from $1,490M–$1,530M) and adjusted EBITDA expense guidance to $1,340M–$1,370M (up from $1,305M–$1,335M)","as_of":"2026-07-21","retrieved_at":"20260929","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 2026 財報後，JPMorgan（Alexander Hess）維持 Overweight 但目標價由 $742 下修至 $700；Evercore ISI（David Motemeden）維持 Outperform 但目標價由 $746 下修至 $722，理由是費用上升軌跡導致估值重新校準","source":"BigGo Finance: \"MSCI Beats Q2 Estimates but Analysts Slash Price Targets on Rising Costs\"","url":"https://finance.biggo.com/news/3aadede8-eb80-4fd1-b4a1-bbfd3f98f59e","excerpt":"JP Morgan analyst Alexander Hess kept an Overweight rating on MSCI but cut the price target to $700 from $742. Evercore ISI Group analyst David Motemeden maintained an Outperform rating and lowered the target to $722 from $746","as_of":"2026-07-22","retrieved_at":"20260929","affects":["valuation","thesis.R","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MSCI Q2 2026 每股盈餘與營收數字在不同彙整站出現不一致版本：部分來源稱 EPS $4.94 優於共識 $4.90（小幅超預期），另有來源稱 EPS $4.94 不及共識 $5.03（不如預期）；營收 $867M 亦分別被稱為優於／不如共識 $864M vs $883.8M。無法從搜尋摘要判定哪個共識基準正確，需查證交易所申報或原始財報稿","source":"Investing.com transcript vs 247wallst.com/basisreport.com 對照矛盾","url":null,"excerpt":null,"as_of":"2026-07-21","retrieved_at":"20260929","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"+","claim":"MSCI 於 2026-03-03 宣布收購 Compass Financial Technologies，強化其在另類與多資產（含商品、加密貨幣）指數編算能力","source":"MSCI Media Room press release","url":"https://www.msci.com/discover-msci/media-room/msci-expands-multi-asset-and-alternative-index-capabilities-with-acquisition-of-compass-financial-technologies","excerpt":"MSCI Inc. (NYSE: MSCI) is enhancing its index calculation capabilities in alternative and multi-asset classes, including commodities and cryptocurrencies, through the acquisition of index services provider, Compass Financial Technologies.","as_of":"2026-03-03","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"MSCI 於 2026年4月宣布收購 PM Insights，取得私募市場（private markets）每日次級市場參考數據與分析能力","source":"MSCI Investor Relations press release: \"MSCI Advances Transparency in Private Markets With Acquisition of PM Insights\"","url":"https://ir.msci.com/news-releases/news-release-details/msci-advances-transparency-private-markets-acquisition-pm-0","excerpt":null,"as_of":"2026-04","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"+","claim":"MSCI 於 2026-03-03 宣布收購 Compass Financial Technologies，強化另類與多資產指數編算能力","source":"MSCI Media Room press release","url":"https://www.msci.com/discover-msci/media-room/msci-expands-multi-asset-and-alternative-index-capabilities-with-acquisition-of-compass-financial-technologies","excerpt":"MSCI Inc. (NYSE: MSCI) is enhancing its index calculation capabilities in alternative and multi-asset classes, including commodities and cryptocurrencies, through the acquisition of index services provider, Compass Financial Technologies.","as_of":"2026-03-03","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"+","claim":"MSCI 於 2026年4月宣布收購 PM Insights，取得私募市場每日次級市場參考數據與分析能力","source":"MSCI Investor Relations press release","url":"https://ir.msci.com/news-releases/news-release-details/msci-advances-transparency-private-markets-acquisition-pm-0","excerpt":null,"as_of":"2026-04","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 1 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MSCI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":82.97,"operating_margin_pct":55.66,"fcf_margin_pct":44.77,"rd_intensity_pct":5.45},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSCI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"SPGI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":70.9,"operating_margin_pct":41.56,"fcf_margin_pct":34.57,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPGI","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MCO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.98,"operating_margin_pct":46.1,"fcf_margin_pct":36.36,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCO","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"FDS","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.38,"operating_margin_pct":29.55,"fcf_margin_pct":29.05,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FDS","as_of":"TTM ending 2026-05-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MSCI"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MSCI/MSCI_Q2_2026_Earnings_Call_20260721.md）

# Q2 2026 Earnings Call
**MSCI Inc.** | Earnings Calls | 2026-07-21

**Operator** (Operator):
Good day, ladies and gentlemen. Welcome to the MSCI Second Quarter 2026 Earnings Conference Call. As a reminder, this call is being recorded.
[Operator Instructions]
I would now like to turn the call over to Jeremy Ulan, Head of Investor Relations and Treasurer. You may begin.

**Jeremy Ulan** (Executives):
Thank you. Good day, and welcome to the MSCI second quarter 2026 earnings conference call. Earlier this morning, we issued a press release announcing our results for the second quarter 2026. This press release along with an earnings presentation are available on our website, msci.com, under the Investor Relations tab. Let me remind you that this call contains forward-looking statements, which are governed by the language on the second slide of the presentation. You are cautioned not to place undue reliance on forward-looking statements, which speak only as of the date on which they are made, are based on current expectations and current economic conditions and are subject to risks and uncertainties that may cause actual results to differ materially from the results anticipated in these forward-looking statements.
For a discussion of additional risks and uncertainties, please see the risk factors and forward-looking statements disclaimer in our most recent Form 10-K and in our other SEC filings. During today's call, in addition to results presented on the basis of U.S. GAAP, we also refer to non-GAAP measures. You'll find a reconciliation of our non-GAAP measures to the equivalent GAAP measures in the appendix of the earnings presentation. We will also discuss operating metrics such as run rate and retention rate, important information regarding our use of operating metrics such as run rate and retention rate are available in the earnings presentation. On the call today are Henry Fernandez, our Chairman and CEO; and Andy Wiechmann, our Chief Financial Officer.
With that, let me now turn the call over to Henry Fernandez. Henry?

**Henry Fernandez** (Executives):
Thank you, Jeremy. Good day, everyone, and thank you all for joining us. In the second quarter, MSCI delivered very strong financial results along with an acceleration in run rate growth in both index and private assets, our 2 key engines of growth in the company. We also showed strength in recurring net new sales across client segments and geographies despite continued challenges in sustainability. Meanwhile, record ETF and non-ETF AUM balances in products linked to MSCI indices, help us achieve our best ever asset-based fee run rate. MSCI is building momentum in the second half of 2026 with a strong pipeline of opportunities and exciting AI-fueled innovation. AI is enabling MSCI to move even faster in building new products, enhancing our existing solutions and strengthening our foundational mission-critical role in global investing and a rapidly growing ecosystem around our solutions.
MSCI's Q2 financial metrics included organic revenue growth of over 12%, adjusted EPS growth of nearly 19% and adjusted EBITDA growth of 14%. We further demonstrated our commitment to driving attractive shareholder returns and our confidence in MSCI by repurchasing $147 million of MSCI shares at an average price of about $558 per share during the quarter and through yesterday. Our Q2 operating metrics included total run rate growth of 12%, fueled by ABF run rate of $948 million, growing 25%. This reflected record AUM levels in both ETF and non-ETF products linked to MSCI indices, supported by another quarter of solid inflows of nearly $40 billion in ETF linked to MSCI indices. Over the past 15 months, total ETF AUM linked to MSCI indices has grown by more than $1 trillion. The incredible scale of MSCI's ABF franchise, and the recent volumes of inflows into products linked to MSCI indices is the ultimate endorsement of trust in our IP, research and standards.
Turning back to our Q2 performance. MSCI achieved organic subscription run rate growth of over 8% with a retention rate of over 95%. This growth is enabled by our success in scaling our footprint across key client segments. Among traders and hedge funds, a category that collectively includes market makers, hedge funds, broker-dealers and exchanges, MSCI delivered subscription run rate growth of 15%. Among hedge funds, specifically, we posted our best quarter on record with 19% subscription run rate growth and nearly $15 million in recurring new sales and recurring net new sales for a growth of 75%, including 3 separate 7-figure deals in index analytics.
So for example, MSCI won a 7-figure index deal with one of the world's largest multi-strategy hedge funds, covering our ETF-linked and non-ETF linked custom index modules along with our constituent AUM packages. All told, we more than tripled our index recurring net new sales with hedge funds from a year earlier reaching $8.6 million in total. These results highlight 4 overlapping trends in the segment of traders and hedge funds for us. First, MSCI's indices are becoming increasingly embedded in the core trading and liquidity infrastructure used by active and passive investors alike. Second, the growth of systematic and quantitative investing has contributed to rising demand for our index content. Third, as traders and hedge funds have expanded their role in global investing, MSCI has gained new opportunities to make our index franchise more diversified and resilient. And fourth, as clients demand faster more specialized indices and structured products and derivatives in larger volumes, AI is helping us accelerate our index production and deliver customization at scale.
Shifting from traders and hedge funds to asset owners, we delivered 9% subscription run rate growth, along with our best Q2 on record for recurring net new sales at $8.4 million and growing 43%. For example, one of the world's largest pension funds -- public pension funds, signed a major new agreement for MSCI's private capital indices and expanded access to our Private Capital Intel solution.
We also completed a 7-figure deal with a large sovereign wealth fund for our total portfolio solution which includes private assets and analytics. Among asset managers, we posted 6% organic subscription run rate growth, along with 9% recurring net new sales growth. This includes a large deal with one of the world's largest asset managers for our enterprise risk and performance tools to support their ongoing initiatives to incorporate factors and enhance the risk reporting across asset classes. In addition, we continue making steady progress with our ETF and other tradable product solutions for active managers.
During the quarter, we signed a handful of clients to support their launch of active ETF strategies leveraging MSCI's Index universe, research and IP. Overall, some of the biggest themes of Q2 included the rapidly expanding ecosystem around MSCI indices, our momentum in private assets and a rapid pace of innovation enabled by our AI transformation and laser targeted acquisitions to unlock additional layers of growth.
Turning more specifically to our product lines. In index, we delivered 41% growth in recurring net new sales, 17% growth in total run rate, more than 11% growth in subscription run rate and a retention rate of more than 97%. In Private Assets, MSCI achieved 57% recurring net new sales growth with more and more pension funds and sovereign wealth funds embracing our total portfolio solutions. Earlier this month, we announced a new strategic partnership with UBS that will extend the reach of our private asset solutions and enable wealth managers to better connect high net worth clients with GP opportunities while promoting greater transparency for the entire investment ecosystem.
By combining MSCI's independent data, analytics, models and AI-powered platforms with UBS's global client insights and expertise in alternative investments, we can help make private markets more understandable, more accessible and enable stronger connectivities between GPs and the wealth channel. This private asset platform for wealth channels is only one example of how we are using AI to improve our solutions and the client experience. We already have over 1,000 clients using IndexAI Insights, which we just launched in February.
Meanwhile, hundreds of companies and end users are now accessing our Total Plan Manager and Private Capital Intel solutions through their preferred AI models. Innovation remains the lifeblood of MSCI's product development, but we're also expanding our capability through highly strategic acquisitions. Last month, for example, we announced that MSCI would acquire First Street, a leading provider of physics-based climate risk data and analytics enabling physical risk assessment across over 2 billion building infrastructure. Combining our respective tools will help us deliver the insight clients need as physical risk becomes a more immediate priority. We're also addressing the broader category of emerging risks, along with issues such as energy access, tariffs and supply chains and AI. Much of our product innovation in sustainability and climate is now focused on this emerging risks which have become increasingly significant to investors.
At the same time, MSCI's work in climate is separate and distinct from our work in sustainability as we are seeing the opportunities there. Sustainability faces persisting market challenges, and we do not expect that to change in the near future. Even still, MSCI remains the provider of choice in this industry and our sustainability tools continue to help us in other business areas, most notably in Index. There are now close to $1.3 trillion in index fund assets benchmarked to MSCI Sustainability and Climate indices with over 1/3 of those assets benchmarked to our Climate indices.
MSCI also took several other steps to advance our AI transformation. In Q1, we brought into the firm Dinesh Gupta from Goldman Sachs to serve as our new Chief Data Officer and Global Head of Operations. In Q2, we welcome Kashi Kakarla from Intuit as our new Chief Technology Officer and Head of Product Engineering, and we announced that Kashi will lead the creation of a new MSCI office in Silicon Valley focused on AI, product engineering and technology. Given his background, Kashi is the perfect leader to help us maximize the benefits of AI across client segments, product lines and asset classes. We have also established a technology and data committee of our Board of Directors.
Looking ahead, we remain confident in our pipeline. In our resource allocation, and in our ability to leverage AI. MSCI plays a key role in virtually every stage of the global investment process, and we are well positioned to seize new opportunities for growth.
And with that, let me turn things over to Andy.

**Andrew Wiechmann** (Executives):
Thank you, Henry. And hi, everyone. We're excited to see the large pipeline and strong momentum in key growth areas across the business with further accelerations in our index and private asset segments. As Henry mentioned, we have had several large client wins that reaffirm the growing ecosystem around our frameworks and solutions. Index subscription run rate growth accelerated to over 11% driven by a strong quarter for recurring net new subscription sales of over $28 million, which was up nearly 41% year-over-year. This reflected some large deals with traders and hedge funds across numerous modules, including our custom index modules. These helped power the custom index organic subscription run rate growth to 23%, excluding contributions from the Compass acquisition. And the retention rate among hedge funds within our index product line was in line with the overall index retention rate at more than 97%.
Additionally, we saw another quarter of very strong growth in asset-based fees, with the ABF run rate reaching nearly $950 million and growing 25% year-over-year. This growth was fueled by close to $40 billion of cash inflows in the quarter, driving AUM and ETFs linked to our indexes up to more than $2.8 trillion. The asset growth and cash inflows predominantly occurred in clients' products linked to our developed markets ex U.S. and all country indexes, some of which carry lower fees. Within Analytics, we had organic subscription run rate growth of 7% driven by demand for our factor content and factor solutions, where we continue to innovate rapidly.
We are also seeing steadily growing demand for multi-asset class total portfolio solutions, including for front office use cases. Analytics organic revenue growth was 7% tracking with run rate growth. In Private Capital Solutions, subscription run rate growth accelerated to over 16%. During the quarter, we had solid traction across existing solutions like our transparency, Private Capital Intel and Total Plan offerings. We also see growing demand with new offerings like our data platform and our asset and deal level metrics. The acceleration is supported by both our deep private asset insights and our strong multi-asset class total portfolio capabilities.
Additionally, we are seeing success with Vantager having already closed a few sales of our Diligence solutions offering. In real assets, organic subscription run rate growth accelerated modestly as we benefited from recent product and service enhancements. And we won a large deal to be the exclusive provider to a large property technology firm that will leverage RCA content and our global index intel offering delivered through Snowflake. In the Sustainability and Climate reportable segment, we drove nearly $6 million of new recurring sales in sustainability in Q2 and over $3 million of new recurring sales in Climate.
However, cancels, particularly in the Americas, were a significant headwind as clients are rightsizing their sustainability spend. As Henry mentioned, we are capturing share gains in a consolidating market and are strongly positioned from a competitive standpoint based on our trusted reputation for quality, depth and breadth of coverage as well as the broad suite of interoperable solutions that we offer. Meanwhile, in Climate, run rate growth across MSCI product lines was nearly 12%. And we are seeing significant demand for physical risk solutions, which are increasingly woven into the investment process.
In the quarter, we won several physical risk deals, including a large deal for a geo-spatial and asset location solution with the European bank. And MSCI's announced acquisition of First Street, a company which has developed truly unique climate forecasting models, enables us to capture the increasing demand for physical risk and broader climate solutions across a wider range of client segments and use cases.
Upon the close of the acquisition in Q3, we would expect First Street to add about $10 million of subscription run rate to the S&C reporting segment. Between the significant emerging opportunities and the pressure on parts of the Sustainability franchise, we expect recurring net new sales to be roughly zero to slightly negative for the combined Sustainability and Climate reporting segment across the next 2 quarters. As always, we remain intensely focused on driving strong capital returns to shareholders, and we will continue driving value creation through capital allocation, as we have done year-to-date between our disciplined repurchases and acquisitions.
On expense guidance, we've seen strong AUM growth within investment products linked to MSCI indexes. These AUM levels have been higher than the assumption we noted last quarter. When we released earnings in April, we indicated that we would be towards the high end of the expense guidance ranges based on the assumption of relatively flat markets in Q2. Given the strong top line momentum and very attractive opportunities, we've been investing in key growth areas.
Additionally, there are a few notable factors driving the increased expense guidance range. Firstly, the impact of the recent acquisitions with the largest impact expected from First Street. Secondly, performance stock-based comp and bonus accruals related to the significant increase in AUM and products linked to MSCI indexes. The adjustment to the D&A guidance is driven by the First Street acquisition and the increase in the interest expense is driven by the higher revolver balances related to the First Street acquisition and recent share repurchases. Importantly, we have the levers to flex investments up and expenses down based on the environment and business performance, which allows us to consistently deliver strong results.
We remain well positioned and committed to delivering attractive profitability growth in all environments while investing for the long term. Overall, I'm incredibly excited by our growing momentum and a strong pipeline across the business. We are only just starting to see the benefits of the new and enhanced solutions that we've recently introduced and which are adding to our momentum. We look forward to keeping you posted on our progress.
And with that, operator, please open the line for questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Manav Patnaik with Barclays.

**Manav Patnaik** (Analysts):
Henry, I guess, in your commentary, you talked about a lot of record new sales and categories and so forth. So just broadly, in terms of the environment for subscription sales, like looking forward, how would you characterize the momentum there versus maybe the numbers this quarter, I guess, fell a little short of expectations. Just curious on anything seasonal or any other characteristics you would call out?

**Henry Fernandez** (Executives):
We are pretty bullish on our outlook and you know me well, Manav, that I speak my mind and I basically tell exactly what I believe. And we have introduced a very large number of new products, 80-plus in the last 2 quarters compared to 40-plus in all of '24. Many of those new products are just beginning to show traction in sales because in our business, it takes time. It's an institutional budget, it's an institutional setting. So it takes time to go showcase it, discuss it, go through the use cases, go through the approval processes in our clients, et cetera.
So that is why I have -- Andy and I have made the specific comments a few times in our remarks about a very good pipeline in the next few quarters. I think we need to look at this quarter in the context of the progression that we have seen in the last few quarters, starting mid last year, and I think we had 3 quarters of outperformance relative to consensus. And the feeling by us that our prospects and the pipeline are pretty good. And therefore, one quarter -- in a process like ours of reigniting much higher growth in the run rate, we're selling what we got and also with a lot of new products being launched, I think we need to be cognizant that there will be more variability quarter-by-quarter because many of the new products we're launching have high ticket items, high value items. So they may -- if they fall in one line versus another line of the day, at the end of the quarter, they may flip from one place to another.
Lastly, Manav, what I would say is, we're very aggressive risk takers but we're very prudent financial managers, extremely prudent financial managers. The reason why we are indicating a higher expense guidance is not because things are being forced upon us, is because we voluntarily feel that we will want to invest more in the business because we remain more positive than we have in the past. Alvise Munari, one of our key senior managers was telling us this morning is if we have the pipeline that we have to -- if we had the pipeline that we have today, last year, would have felt a lot better, right? Meaning, it's -- a lot of things have changed. And of course, the overall environment is pretty positive among hedge funds and traders and even the active managers, I think we are making more progress than in the last few years because we're putting in new products.

**Operator** (Operator):
Our next question comes from the line of Toni Kaplan with Morgan Stanley.

**Toni Kaplan** (Analysts):
I wanted to follow up, Henry, on you just mentioned maybe higher volatility because of the higher ticket price products -- higher-priced products. I was wondering if you could maybe talk about you're having really good success selling to hedge fund clients. You mentioned the tripling of net new sales there. Does that inherently lead to revenue volatility in the future? I know right now, it seems like that's not an issue, but does that lead to volatility? And then maybe also MCP, like are you getting traction and adoption on selling data through MCP and does that lead to increased pricing this year, but then when you lap it in the future, does that sort of add some volatility as well?

**Henry Fernandez** (Executives):
Toni, I believe that there will be some, not a lot, but some volatility quarter-by-quarter as we ramp up growth. But I don't think that, that volatility will necessarily come from traders and hedge funds. Historically, when you go back quite a few years, there was a meaningful amount of volatility in that segment. And a lot of it was because there was a long tail of hedge funds that we were selling into, which would disappear or go out of business or they would cancel.
Our strategy today is much more focused on the largest hedge funds that are multi-strategy, much more stable than has been in the past. So that is one factor that I don't think will lead to volatility. The other strategic factors that I would want to mention is, for a very long period of time, we had MSCI in our index franchise, we're very focused on the assets, the AUM levels of our clients. Our price increases with the active managers were kind of correlated to that, our solutions were correlated to that. And of course, the ABF fees were highly correlated to the level of assets. What we have discovered in the last few years that there is a large trading and liquidity ecosystem around the AUM, which we were not strategically focused on as much. And that's what we've started to do in the last year or so, and we have started launching new products and the like.
So I think that, that is a secular and consistent source of profitability of sales, of course, but profitability for us, and it's not like a yo-yo, it doesn't go up and down. It's very secular, very structural.

**Operator** (Operator):
Our next question comes from the line of Ashish Sabadra with RBC Capital Markets.

**Ashish Sabadra** (Analysts):
I wanted to drill down further on the analytics front. Particularly, you talked about really strong demand for factor content and factor solutions, but if you look at the subscription sales growth there, that was a bit soft. So I was just wondering any particular puts or takes that you would call out? Is it mostly around tougher comps? And how do we think about the pipeline and analytics going forward?

**Henry Fernandez** (Executives):
It's all lumpiness. The pipeline going into the second half of the year is pretty strong in analytics. And therefore, I would really advise you not to focus too much attention in this quarter's softness, so to speak, in the analytics results because it's very, very largely lumpiness from one quarter to the next.

**Operator** (Operator):
Our next question comes from the line of Alex Kramm with UBS.

**Alex Kramm** (Analysts):
Hopefully, this is not a repeat, my phone just dropped. But I wanted to come back to the index sales, in particular from hedge funds because you did point out strong demand, and I think you just mentioned again just now in terms of the multi-managers, but there's obviously been a bunch of articles around how much money some of these firms are minting in terms of index arbitrage strategies, et cetera. So just wondering, do you think there's a large TAM for this? Do you think there's a lot of firms that you're talking to that want to get bigger in that space because clearly there's money to be made? Or do you think it's a very concentrated group of folks that you can sell to here? And then hopefully, at some point, you meet that demand, but maybe it's finite.

**Henry Fernandez** (Executives):
Alex, I think it's both. Definitely both as I was saying, probably when your phone dropped, the very strategic sort of breakthrough that we have had in the last kind of 12, 18 months of MSCI is that we used to sell to the traders and hedge funds as a derivative almost like we would take the products that we would sell to the active managers and sell it to them. And we started recognizing that in addition to the very large AUM levels of active and passive manager AUM linked to our indices, there is a very large ecosystem around that. The trading ecosystem, liquidity ecosystem around that, that needs lubrication, that needs products, data products and models and all of that to make it flow better, and we're the ones that can provide that because we help create that AUM levels. 
So I think the large hedge funds, we're definitely getting paid too little for the index arbitrage, right? That's for sure. And there are a number of other hedge funds that are obviously wanting to get into that, especially given the recent good news about the profitability there. But there are a lot of other venues for growth in terms of custom index. One of the things we've been highlighting to our hedge fund clients is, they are focused very much on the market cap index arbitrage, but 30-plus percent of the AUM of the ETFs linked to MSCI indices are nonmarket cap. They are factors and ESG and climate and many of them are more customized.
So we're creating those data sets for them to do the index arbitrage. Now remember, the index arbitrage also helps the active managers and passive managers, particularly passive managers because somebody's got to supply the shares in that one last hour of trading in the quarter when people are rebalancing. And the people that do that are the hedge funds and the broker dealers. So there is a big ecosystem that we're just beginning to scratch the surface here.

**Operator** (Operator):
Our next question comes from the line of Owen Lau with Clear Street.

**Owen Lau** (Analysts):
Could you please add more color on the drivers of the fee compression for the asset-based fee in the last 2 quarters. The drop was quite meaningful for 2 quarters compared to last year. How much of that was because of your kind of like the tier pricing structure? And how much of it is driven by competitive dynamics? And how should we think about this fee rate going forward?

**Andrew Wiechmann** (Executives):
Sure, sure. Yes. So Owen, first and foremost, it is important to keep in mind that our primary focus is on driving overall run rate growth and revenue growth and maximizing the AUM capture with our ETF partners. And you've seen tremendous success on that front with nearly $1 trillion of AUM growth and 30% growth in ETF run rate over the last year, 25% overall growth in asset-based fee run rate and so that is our predominant focus. As we commented on with the year-end earnings, around the new BlackRock agreement, the extension of the BlackRock agreement. There was a change to the floors on certain products, which caused the drop in the first quarter of basis points.
When you look at the second quarter, it was predominantly driven by tremendous asset growth and mix shift. And so we saw significant growth in AUM skewed towards developed markets outside the U.S. and all country products where we tend to have a wider range of pricing schedules, particularly relative to emerging market exposure. Correspondingly, you saw far less cash flows in emerging markets in the second quarter relative to what we've seen in the past year recently. And so there were a number of dynamics at play. In this case, it was heavily mix shift driven. I do want to highlight, and we mentioned this at year-end, we do now have lower floors on certain large products and we've got a somewhat dynamic framework built around the pricing.
So the overall basis points are going to be dynamic and a function of how much growth we see and where we see that growth. And if you do see significant growth in lower fee products, you can see a higher contribution from mix shift as we saw in the second quarter here. The opposite can be true as well, where when you see a higher contribution from the higher fee products. You can see stability or even increases in the basis points. So it really is path-dependent here, but overall, our focus is on driving overall run rate growth and we continue to be very bullish about the opportunity here. And even over the last few weeks in the third quarter, we've continued to see exceptional cash flows in the ETFs linked to our indexes. And so continue to believe there's a long trajectory of upward movement there.

**Operator** (Operator):
Our next question comes from the line of Alex Hess with JPMorgan.

**Alexander EM Hess** (Analysts):
Could you briefly refresh us how much -- what is your AUM level to end the quarter in non-ETF products? And then shifting to the active ETF discussion. I know you guys threw out some points there. But just maybe give us an update on how active ETF penetration is going. Should we expect more attach of subscription products in the back half of the year or nascent active ETFs? Any sort of dynamics about how that should flow through your P&L in the back half of the year and just the momentum in that business would be really helpful.

**Andrew Wiechmann** (Executives):
Sure. Sure. Yes. Thanks, Alex. So the non-ETF passive AUM is around $5 trillion as of June 30. It continues to be an area where we see tremendous growth across a number of dimensions. The revenue growth can deviate from ETF growth because of a number of factors, including different AUM growth dynamics, less impact from inflows, contract adjustments, true-ups, true-downs in certain cases, we can have mandates that shift their assets, which can cause impact to run rate and revenue, which is why you've seen some lower growth in non-ETF passive relative to the ETF growth, but we do expect this to continue to be an attractive longer-term growth opportunity for us.
On the active ETF front, this is an exciting area for us. As you know, we've got a notable presence as a benchmark provider to many of the -- actually, most of the managers that are launching active ETFs, and we are increasingly having dialogues with them about how we can help them beyond just being the benchmark and play an integral role in the active portfolio construction through using our content sets, our tools, our analytics.
And so we have started to get traction there. So we actually recently launched our active financial product license, which is a specific license to an active ETF manager where they have the ability to use our content as a key input into the active management of their strategies. And so we have had some wins on that front in the second quarter, and we are in active dialogues with many organizations to do more for them on that front. So this is something that's benefiting us both on the subscription side and we believe over time should help play a role on the asset-based fee side of the equation as well.

**Operator** (Operator):
Our next question comes from the line of Kelsey Zhu with Autonomous.

**Kelsey Zhu** (Analysts):
Analytics margin was a bit softer than expected this quarter. Could you maybe talk about the main drivers there? And how we should think about the margin trajectory in the second half of the year?

**Andrew Wiechmann** (Executives):
Yes. As you know, firstly, I would say we don't focus heavily on the margin in any specific segment or even in a quarter. Our overall goal is allocating our investment dollars and our resources towards the highest returning areas. So I wouldn't read too much into one quarter's margin or expense growth just to provide a bit more color on analytics expenses. I would highlight that a year ago in the second quarter, we had a sizable contingent consideration reversal associated with the contingent consideration on the Fabric acquisition. That skews a little bit the year-over-year expense comparison and ultimately, the margin comparison.
We did also have, as I mentioned in the prepared remarks, we had elevated comp accruals and performance stock expense impacts, a chunk of those end up hitting analytics. And beyond that, there are factors like FX and capitalization in any given quarter that can cause the margin to swing around. But within analytics, as Henry alluded to, we continue to see very attractive opportunities, we continue to invest behind areas like our factor franchise areas like our total portfolio solutions integrating our private asset capabilities. But there are parts of the analytics where we are much more measured on our investments. But overall, as I said, I wouldn't focus too much on the margin or expense growth in any one quarter.

**Operator** (Operator):
Our next question comes from the line of Craig Huber with Huber Research Partners.

**Craig Huber** (Analysts):
I want to focus on all other private assets segment. What do you guys think needs to change here to sort of get out of this? You have about 8% subscription run rate growth this last quarter, yes, that's an acceleration from recent quarters. Although it's not as strong as I think, do you think the potential is long term or what it used to grow historically, some quarters. What needs to change in the marketplace? Is it more the product? Is it the sales effort and sales team size or something that to change in the marketplace? Is it an education to the marketplace? What do you think needs to change or to accelerate that even further?

**Henry Fernandez** (Executives):
So Craig, in sum, much higher growth rate and all of the above. We're just getting started on the acceleration of private assets. And we took control of Burgiss some 3-plus years ago. It took us maybe 1.5 years to make sure that we were totally comfortable with the data sets, with the collection processes, with the existing client base and all of that. And then it took another year or so to change the management team of the business. These kinds of people are not easy to find. So over the last, say, 18 months, we put a new management team and with, let's say, half a dozen to a dozen senior leaders there, we started innovating significantly launching a lot of new products. And all of that, at the moment, it's only beginning to show -- only beginning to show in the growth rate of what we call PCS.
On real estate, I think that the approach we have been taking before, which was not the right one was, we had a management team there and it was basically focused on all places, all things and all that. So we've brought in a great new leader to that space about maybe 3, 4 months ago. We're beginning to show the results of that to revamp the strategy. Real estate is a huge asset class, and there are a lot of subsegments of real estate, some of which are growing pretty fast, like private debt into real estate and infrastructure and some of which are challenged like center city office space, right? So it's a question of picking your spots and creating new products for that. So overall, we feel that the growth rate -- so in saying all of the above is new products, new management team, expansion into new client segments.
So for example, in PCS, the old Burgiss business, we were very much focused on the institutional LP, you saw our announcement on -- with UBS on focusing on the wealth LP. One of the biggest contributions we can make is creating transparency and valuations and private asset funds for the wealth segment, the wealth channel, that will significantly increase the allocations in wealth, and we will do that starting with our lead client, UBS, and talking to all the -- talking and subscribing all the big wealth managers in the world. So that's a significant opportunity. And then we have also taken significant steps of creating products and penetrating the GPs in which our run rate for private assets and GPs is extremely small compared to the potential that exists there, which is very, very large.

**Operator** (Operator):
Our next question comes from the line of Faiza Alwy with Deutsche Bank.

**Faiza Alwy** (Analysts):
I wanted to ask about new product traction. I know historically, you've given us some metrics around the percentage contribution from new products. And I was hoping if you could get some metrics like that. But I guess more broadly, I'm trying to understand the new product traction from maybe your non-hedge fund trading ecosystem. And just trying to disaggregate sort of how much of your growth is really being driven by, again, that hedge fund ecosystem versus kind of incremental new products?

**Henry Fernandez** (Executives):
So let me answer the second part, and then Andy will give you the second -- the first part, which is the more quantitative answer. As you know, every quarter, we try to focus attention on specific area so that we don't diffuse the whole effort, right? So this quarter, obviously, we've been focused on traders and hedge funds especially index analytics products in order for you to see the potential of that. But there is a very large potential that -- on index across the whole spectrum. I mean we're doing a lot of -- we're ramping up significantly the custom index factory for institutional investors that want customized indices or portfolios and the like. So obviously, we're customizing indices for ETFs and all of that. So that's an area that we are only beginning to see the fruits of the expansion in custom indices.
On analytics, we've talked a lot about AI in analytics, which has been very successful. We are pushing pretty hard the total portfolio solutions capabilities with the TPA approach, the total portfolio approach that the Canadians have advocated, a lot of pension funds are coming to us and discussing what are the ways that our infrastructure, our models and our data and our technology can help them achieve that TPA approach to investing for pension funds and sovereign wealth funds.
So we're only beginning to see traction there. It takes time, as I said. And on private capital solutions and real estate solutions, we launched a lot of new products that have not yet started contributing because it's early. I mean the launching of these new products have been in the last 6 to 9 months. So it's just beginning -- we're beginning to obviously discuss with our clients to do testing, do a lot of trials and it will help the user convince their management that they should spend a lot more on this, et cetera. It's very early days on that for both what we call PCS and what we call real estate or real assets. Andy?

**Andrew Wiechmann** (Executives):
Faiza, just to dimension it, when we look at the contribution to new sales from new products in the first half of this year, it's up around 40% compared to a year ago. And so we have seen a bigger and bigger contribution from new products. As Henry alluded to and you're asking about the area we've seen the most impact is with the traders and hedge funds scenario where there is generally a shorter sales cycle and path to monetization but we are seeing traction across a broader range of index areas, particularly custom indexes as well as on the private asset front, we are seeing some good traction and there are a whole host of really impactful new solutions that we are just -- have just rolled out recently and are coming out with in the near future across both private assets and index as well as within analytics.
So things like -- we've talked about before, Basket Builder, Signal Library, Advanced Factor Insights. These are areas where it's very fertile new product introduction. They do oftentimes have a longer sales cycle, as Henry said earlier, but these are areas where we're very encouraged and bullish about the opportunity set on the impact of new products moving forward here.

**Operator** (Operator):
Our next question comes from the line of Scott Wurtzel with Wolfe Research.

**Scott Wurtzel** (Analysts):
I just want to ask a more high-level question. We have seen this elevated level of subscription run rate growth and traction from the hedge funds and the traders. I'm just wondering if you can maybe share your thoughts on what inning you believe we are in sort of the kind of demand and product uptake cycle with these 2 end markets and if and how long we could potentially see this elevated level of growth for?

**Henry Fernandez** (Executives):
In a 9-inning baseball game, the first 2, 3 innings would be my guess. Now I can translate that into 90 minutes of soccer, but I won't do that. You can do the math, right? But we're very -- on that segment, we're very bullish, but it's not the only segment we're very bullish. We're very bullish on wealth managers as it relates to private assets. As I said, we're only getting started with and that's the UBS announcement, of course, which is not in the numbers, by the way. The announcement is just the agreement -- the sort of term sheet agreement to proceed, which we thought it was important to publicize so that we can get traction with other wealth managers in the world. So we feel very good about that. We feel very good about the custom index ecosystem. We feel very good about analytics of accelerating the growth rate of analytics gradually.
Nothing comes suddenly and the like. We feel very good about physical risk in climate, we -- what ESG and transition risk and then physical risk did to us with a major sort of strategic breakthrough what all these things are, are nontraditional sources of risk and return. So we started focusing on that because they have significant effects on portfolios, tariffs, energy supplies, energy dependence, energy transition, obviously, AI impact on companies, other supply chain impacts and the like. Our client base is clamoring for datasets and models that help them understand. So for example, with the closure of the Strait of Hormuz, clients have come to us and say, can you get us data set to understand the electric utilities in East Asia that depend on gas coming from Qatar or oil coming from Kuwait and therefore try to assess the risk and the opportunity associated with the shares of those companies or the debt of those companies.
So of course, one of the highest products in demand right now is can we use a ranking of companies that are going to have a good positive impact from AI and the companies that are going to have a negative impact on AI. Well, the first thing that I told them is MSCI is in the category of very positive impact from AI. But they're looking for the broader sets across all securities.
So we're very busy at work, extremely busy trying to do that. So I mean, look, I think that one other thing that I would say is that we try not to have company speak or in my case, CEO speak. We try to tell you like it is, like we see. I stood here almost a year ago exactly and telling you things were not looking that great because we haven't launched a lot of new products, the active management segment was a little more challenged, and we were not in a great trajectory in sustainability. But we have taken a lot of big steps.
Well, those big steps began to show the way in the third quarter, in the fourth quarter and in the first quarter of this year, and I'm, therefore, telling you the opposite right now. The opposite is that we see a big trajectory here. And I know and respect people that have a different view and they want to sell their shares. And that's capitalism and free markets and listed company operandi. But given our conviction and our franchise and the growth prospects that we see, we're prepared to put a bid on the other side of that trade.

**Operator** (Operator):
Our next question comes from the line of Surinder Thind with Jefferies.

**Surinder Thind** (Analysts):
For the sustainability segment regarding the challenges that you're seeing, is this something that we can get through mostly this year? Or is this something that you're going to have to digest maybe over a longer period of time? And then maybe related to that, can Europe and maybe the rest of the world just continue to offset here? Or how should we think about the longer-term dynamics?

**Henry Fernandez** (Executives):
Well, I used to think that it was going to be like a couple of year process. Overreaction is not panning out to be that. I think the -- we're in a protracted cyclical downturn on the use of sustainability, but I want to emphasize cyclical, not secular. I think sooner or later, there will be more demand for these factors that create opportunities and risk in portfolios, but it's only logical. I mean think about -- let us think about this. Who is going to say that in the future, government is going to be less important. Who is going to think that in the future environmental matters are going to be less important. Who is going to think that in the future, social issues where most developed market economies in the world, their local white population is declining and they need to bring people of color and people of other religions in order to create economic growth and the adaptability of companies to a social system of multicultural society needs to be taken into account and the return of security.
So I think we just -- we're seeing an overreaction, which is prolonged and protracted. I don't know how long it will take, but it will take long. And right now, for us, it's a consolidation play. We are consolidating -- our clients are consolidating to us because we're the committed player, we're the one putting some investment, we're the one servicing them. So our market share is increasing in this space, in some cases, rapidly. And we're going to be the last big entity standing when this all settle in this space and benefit from the upswing when it comes.
The other part of this, as I said before, is sustainability of the old ESG terminology open our eyes to climate initially transition and then physical and it opened our eyes to this whole field of emerging risks. Most of what MSCI has done has helped clients understand traditional sources of risk and return, market risk, credit risk, in some cases, operational risk, whether it's factor risk or stress testing risk or all of that. And what we have begun to realize is that the world is changing fast and therefore, there are nontraditional and emerging sources of risk and return that need to be captured into portfolios, and we are the player to help them do that.

**Operator** (Operator):
Our next question comes from the line of Curtis Nagle with Bank of America.

**Curtis Nagle** (Analysts):
Great. Maybe just a quick one on the cash flow. So EBIT expenses up a little bit, but you did raise the free cash flow guide. So just wondering, I guess, what the offsetting stronger conversion is related to?

**Andrew Wiechmann** (Executives):
Yes. So I mean it's driven by a pickup in collections. So we've seen really good traction across the business, as you know, some good top line momentum, and we've seen strong collection activity. That is somewhat offset by higher cash taxes, some higher comp-related expenses as we've talked about with the expense guide. But overall, we're seeing strong business momentum, and that's trickling through to free cash flow. As you know, free cash flow can be a bit lumpy because of items like tax, timing of expenses and collections. But overall, we see good momentum and continue to be confident about driving attractive trajectory of both free cash flow growth and free cash flow conversion and free cash flow per share are all things that we're confident in.

**Operator** (Operator):
Our next question comes from the line of Jason Haas with Wells Fargo.

**Keegan Antico** (Analysts):
This is Keegan on for Jason. I've got another one on the traction you're seeing with hedge funds. Has there been any step change in the underlying demand? Or would you categorize all of this acceleration as coming from your new product developments. And what I'm really trying to understand is, you mentioned that your product development in 2026 has already doubled that of 2024, but you're only starting to see the benefits. So should we expect this to continue to accelerate as you continue to benefit from the accelerating new products on a lag?

**Andrew Wiechmann** (Executives):
So the impact from new products, we expect to continue to grow, as Henry alluded to earlier, specifically within the hedge fund and trader community, that's the area where we've actually seen probably the most notable impact from new products so far. Those are areas where there is oftentimes a quicker path to monetization and shorter sales cycles. But as Henry alluded to earlier, we're in early innings there. And so these organizations are both growing, the areas where they are growing and accelerating, we can help them, which is index rebalance strategies, systematic, more systematic strategies, things like basket trades, understanding factors and signals in more detail coming up with custom factors.
These are all areas where we're just releasing new capabilities and plan to release new capabilities in coming quarters. So as Henry alluded to, we've got a long way to go. But hedge funds and traders is probably the area where we've already seen the most notable impact from new products. I think the comments generally were across many other areas as well where there's longer sales cycles and many of the products that we've released, we should be monetizing going forward here, but haven't seen as big of an impact to this point.

**Operator** (Operator):
Our next question comes from the line of George Tong with Goldman Sachs.

**Keen Fai Tong** (Analysts):
You mentioned asset managers grew 6% in subscription run rate this quarter. Can you elaborate on the demand environment among active managers and whether you're seeing any catalysts that could drive an acceleration in growth?

**Henry Fernandez** (Executives):
Yes, George. I mean I think there is not a huge amount that has changed in active managers. Obviously, their AUM levels have risen, but the flows are still muted. And with indices like ours, of course, right, performing well because of concentration in countries like the U.S. or concentrations in technologies like what was the technology in emerging markets and things like that, they will tend to underperform and have more pressure. So not a huge amount, it's stable. It's a stable kind of client base, but it's not a huge amount of change. I think the approach that we have taken is that this client segment, which we know very well needs our help in transforming themselves.
And that is where we're extremely focused on. It needs our help in active ETFs, 80-plus percent of the active ETFs are actually quantitative -- not quantitative, I would say systematic type of ETFs as opposed to stock-picking ETF. So we have a lot to add there for them and help them with that. We are -- a lot of them are gingerly going into parts of the private asset space like growth equity in private or private credit and the like, and we're helping them there as well.
A lot of them are trying to penetrate the wealth channel in addition to the institutional channel. So we have a lot of sales enablement tools there, et cetera. So I think you're going to see a gradual increase in the growth rate on this client segment because of the new strategies we're putting into place.

**Operator** (Operator):
Our next question comes from the line of David Motemaden with Evercore ISI.

**David Motemaden** (Analysts):
So last quarter, you guys were talking about some of the clients -- some of your clients wanting to license more content through AI-enabled deliveries. So I'm wondering three months later, how those conversations are progressing? Are you seeing any signs of monetization of that content licensing. And is that -- is any of that showing up here in the run rate yet? Or is that coming here in the next few quarters? Or how do you think about the progression of that?

**Andrew Wiechmann** (Executives):
Yes, yes. So it is showing up. It's little today. We do expect this to be a nice tailwind for us. And so we actually very recently signed our first training license. So this has actually given a client the right to train a model using certain content of ours. We think that's something and we see the demand across a wider range of clients that want to do the same thing, and that can be very attractive for us even beyond the training needs. We know, as Henry alluded to, our clients are becoming more quantitative. They are leaning on AI-driven tools and want broader access to more content sets across broader parts of their organizations. And so that piece has been fueling some of the growth across numerous client segments and fueling some of the demand for more content. But in both cases, we're early in that journey. Those AI-driven investment processes are at a formative stage and we can play a critical role in helping our clients develop those and give them the key inputs that need to be more risk-aware, systematic, thoughtful and clear about what they're doing to create better outcomes. And so it's an area we are excited about, but it's been a relatively small contributor to this point.

**Operator** (Operator):
We have a follow-up question from the line of Alex Hess with JPMorgan.

**Alexander EM Hess** (Analysts):
Just real quick. Can you give any color on pricing dynamics year-to-date and maybe what you expect prospectively, just to round out the picture on net new.

**Andrew Wiechmann** (Executives):
Yes, sure, Alex. So I would say, overall, the contribution from price increases to new recurring sales has been relatively stable for us. It fluctuates a bit up and down in different parts of the business, different client segments, but the overall contribution has been pretty consistent with what we've seen in recent quarters. I'd say the puts and takes relate to things like client health, usage, innovations, and importantly, we are taking a long-term view with our clients.
And so in many areas where we could increase price more, we want to be a constructive partner to our clients and position ourselves to do a lot more with them going forward here and the enhancements, innovations that we are making are helping add additional value to our clients as well as supporting price increase here. And so we're confident about the trajectory of price increases. We think it's going to be a strategic and sustainable part of the growth algorithm for us. 
But overall, it's been pretty stable, and we're being pretty measured around it, although in some areas where we are dramatically enhancing the value we're providing, we can use price as a mechanism to capture that value.

**Operator** (Operator):
Thank you. Ladies and gentlemen, I'm showing no further questions in the queue. I would now like to turn the call back over to Henry Fernandez for closing remarks.

**Henry Fernandez** (Executives):
Thank you, everyone, for joining us. As we described, our footprint is growing across client segments in the investment ecosystem as we accelerate innovation to position us for higher levels of growth in the future. We have a tremendous franchise and are only in the early stages of unlocking the full potential of that franchise and especially through AI. We, of course, remain intensely focused on delivering compounding growth and long-term value creation for our shareholders. We are not a company that makes or break every quarter. We're a company that would like to focus on the addition of every single quarter over the year and over the years in order to create compounding growth year in, year out, year in, year out.
In the short term, our sales pipeline seems strong, in terms of the number of opportunities, including some large potential deals that could benefit us in the second half of the year. We are very excited about all the opportunities in front of us, and we're laser-focused on capitalizing them. And again, thank you for joining us. And obviously, please reach out to our team in case you have other questions or comments. And we keep -- we look forward to keeping you posted on the tremendous progress we're making on the transformation of MSCI into a higher-growth company.

**Operator** (Operator):
Ladies and gentlemen, this concludes today's conference call. Thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MSCI_Q1_2026_Earnings_Call_20260421.md
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 給 Q2 Analytics 營收年增率指引，因大型 implementation 認列的 nonrecurring 收入不會重複，預期回落到中個位數（原話："Analytics year-over-year revenue growth to be roughly 5%"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 表示因 ABF（asset-based fee）表現強勁及假設下半年市場溫和上漲，全年費用預計落在guidance區間的上半段（原話："in the top half of our expense guidance range."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 給出 Q2 有效稅率區間指引（原話："we expect to have an effective tax rate between 18% and 20%."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 重申全年自由現金流展望維持不變，但提醒 Q2 是季節性現金稅支出最高的季度（原話："The free cash flow outlook for the full year is unchanged"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 說明因收購案的無形資產攤銷，上修全年 D&A（折舊攤銷）guidance（原話："we updated our full year outlook on D&A by $5 million"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜margin：CFO 定義 Q1 asset-based fee（依資產規模計費）run rate 成長率為 25%，並說明是被指數連結資金流帶動（原話："Asset-based fee run rate growth was 25%"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜margin：CFO 說明 Analytics 收入成長逾 10%，是因本季認列較高的 implementation 一次性（非經常性）收入（原話："implementations recognized in nonrecurring revenues"）
- 2026-04-21｜Henry Fernandez (CEO)｜competition：CEO 被問及 AI 是否改變 Analytics 業務的競爭態勢時，回答目前尚未看到來自傳統對手或新創的激烈競爭（原話："haven't seen any kind of competition or intense competition"）
- 2026-04-21｜Henry Fernandez (CEO)｜competition：CEO 補充公司並未因此放鬆，仍在密切監控該競爭動態（原話："We're not relaxed, we're monitoring and focused on that"）
- 2026-04-21｜Henry Fernandez (CEO)｜competition：CEO 表示在 sustainability（永續評等）領域正從競爭對手手中搶下顯著市占（原話："taking away from competitors on sustainability."）
- 2026-04-21｜Henry Fernandez (CEO)｜capital_allocation：CEO 揭露年初至今的庫藏股買回金額（原話："we repurchased more than $464 million of MSCI shares"）
- 2026-04-21｜Henry Fernandez (CEO)｜capital_allocation：CEO 提到近期完成三筆小型併購案（bolt-on acquisition），鎖定關鍵成長領域（原話："small bolt-on acquisitions in key growth areas"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜capital_allocation：CFO 說明三筆併購案（Vantager、Compass、PM Insights）對 run rate 與費用的貢獻相對有限（原話："a relatively modest contribution to run rate"）
- 2026-04-21｜Henry Fernandez (CEO)｜product：CEO 表示 IndexAI Insights 連接器自二月底推出以來，已有數百家客戶使用（原話："used IndexAI Insights since our launch in late February"）
- 2026-04-21｜Henry Fernandez (CEO)｜product：CEO 提到收購 Compass Financial Technologies，把客製化指數能力延伸到商品、數位資產、股票衍生品等新資產類別（原話："acquisition of Compass Financial Technologies"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜product：CFO 提到公司已推出 active financial product license，讓客戶用 MSCI 指數運算能力做主動型 ETF，能同時挹注訂閱與 ABF 兩種收入（原話："we have launched our active financial product license."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜risk：CFO 預期 Sustainability 與 Climate 產品線的需求壓力與成長趨緩會持續到近期（原話："Sustainability and Climate to continue in the near term."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜risk：CFO 提到 Real Assets 產品線的不動產交易解決方案仍面臨逆風（原話："headwinds with our property transaction solutions"）
- 2026-04-21｜Henry Fernandez (CEO)｜risk：CEO 被問及市場動盪是否影響業務時，表示除了波灣地區的商談與展示放緩，其他地區未見伊朗戰爭的影響，客戶維持正常營運節奏（原話："effect of the Iran war anywhere else in the world."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜customer：CFO 說明 Index 產品線在對沖基金客群的訂閱 run rate 成長率達 27%（原話："run rate growth within index with hedge funds"）
- 2026-04-21｜Ashish Sabadra (Analyst)｜customer：分析師指出資產管理公司客群訂閱 run rate 成長率從上季 7% 降到本季 6%，詢問後續動能（原話："it moderated a bit from 7%, I believe, last quarter to 6%"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜customer：CFO 回應資產管理公司成長率變動時，提到匯率因素會影響任一客群的成長率數字（原話："FX factors at play with the growth rates"）
- 2026-04-21｜Henry Fernandez (CEO)｜customer：CEO 回答私募信貸市場的信用風險疑慮對 PCS（私募資產解決方案）業務是順風而非逆風（原話："It's definitely a tailwind for us."）
- 2026-04-21｜Henry Fernandez (CEO)｜commitment：CEO 重申公司致力於透過紀律化部署超額資本來極大化價值創造（原話："we are committed to maximizing value creation"）
- 2026-04-21｜Henry Fernandez (CEO)｜commitment：CEO 透露約一年半前公司已把使用 AI 列為聘用員工的條件之一，藉此推動全公司 AI 採用（原話："we made AI a condition of employment at MSCI."）

### MSCI_Barclays_24th_Annual_Global_Financial_Services_Conference_20260914.md
- 2026-09-14｜Andrew Wiechmann (CFO)｜guidance：CFO 給出第三季 adjusted EBITDA 費用區間，因遣散費及 AUM 連動薪酬墊高（原話："the high $330 million"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜guidance：CFO 預告全年費用可能落在原先財測區間的高端（原話："the higher end of our expense ranges"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜guidance：CFO 說明年初至今 recurring net new 較去年同期成長幅度（原話："up 24%, 25% over last year"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜guidance：CFO 量化 BlackRock 新約對基點費率的兩階段調整幅度（原話："to the basis point fees was 0.1 basis point adjustment"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜margin：CFO 定義 AI 帶來的效益是把 run-the-business 費用成長率壓到低個位數（原話："bring that down to low single-digit type of growth rates"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜margin：CFO 拆解 Q1 到 Q2 基點費率下滑的口徑，歸因於低費率大型 ETF 產品的資產成長（原話："extraordinary growth in lower fee hyperscale ETFs"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜competition：CFO 表示公司在爭取新流入 ETF 資產的市佔上具備獨特位置（原話："capture a significant amount of the market share"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜capital_allocation：CFO 定調併購策略聚焦於加速既有業務的小型收購，不追求新事業線（原話："will likely be bolt-on accelerators"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜capital_allocation：CFO 重申會持續在具吸引力價位大力執行庫藏股買回（原話："buy our stock back at attractive prices"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜product：CFO 給出新產品對今年上半年新增經常性銷售的貢獻比例（原話："40% from new products"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜product：CFO 指出 Index 部門經常性訂閱成長率因新產品加速（原話："accelerate from mid-8% to over 11%"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜product：CFO 說明 Private Assets 旗下 PCS（原 Burgiss）業務訂閱成長率最新一季的加速幅度（原話："up to north of 16% in the most recent quarter"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜risk：CFO 針對 Analytics 與 Sustainability 業務被 AI 顛覆的疑慮，明確表態 AI 現階段是機會而非威脅（原話："we don't today see AI as a threat but more of an opportunity"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜customer：CFO 列舉過去一年在 broker-dealer 客群也出現成長加速（原話："We've seen acceleration with broker-dealers."）
- 2026-09-14｜Andrew Wiechmann (CFO)｜customer：CFO 描述傳統主動式資產管理客群是預算壓力最集中之處（原話："is kind of the epicenter of that pressure"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜commitment：CFO 承諾公司財務目標是加速獲利與自由現金流成長，而非單純衝高利潤率（原話："drive faster profitability and free cash flow growth"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜commitment：CFO 說明即使完成多筆併購，過去一年整體人力仍維持大致持平（原話："our headcount has been roughly flat"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜commitment：CFO 承諾把 AI 節省下來的費用再投資，而不是直接讓利潤率跳升（原話："to reinvest them and accelerate that algorithm"）

### 問答異常語氣（迴避／改口／保留）
- MSCI_Barclays_24th_Annual_Global_Financial_Services_Conference_20260914.md｜問：分析師追問遣散費是否集中在特定事業部門，還是廣泛分布｜答法：CFO 先說主要落在 data/technology 與 Analytics、Index 等大部門，但隨即表示「I don't want to be too specific at this point」，未給出具體部門別數字或比例

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

`scenario_inputs`（EPS路徑五年、終端倍數、機率、yield、second_stage、Max DD範圍與依據）——你不寫`scenario.json`，那份由程式跑`dd_scenario.py`產生。Bear機率5Y不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬≥50%；Base機率不應>50%；bear機率須註明依據，sourced結構性durability仍硬套bear需說明「為何不採信」否則不得高於base [§3]。
- 內生天花板sanity check：Base情境EPS CAGR貢獻vs§5.R內生天花板(同組數字不重算)→天花板內✅/超出⚠(⚠→Bear機率強制≥30%)。成長熄火：3年後成長率降至15%/10%/5%三情境×Forward P/E壓縮→估值跌幅，作Bear PE錨。三分量拆解(≤80字，Base IRR多少來自EPS複利/re-rate/股息淨回購)：re-rate貢獻≥Base合計IRR的40%→標記「估值依賴型」(`decision_inputs.valuation_dependent=true`) [§3]。
- IRR落點：<8%/yr弱、8-12%中、>12%強、>15%罕見，不作跨檔排序依據。AR=`(P_bull×|Bull5Y%|)÷(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著，非放鬆機率防線理由。年期硬規則：①表頭終端年=主時距終端年②終端倍數EPS分母年期與現價倍數同源③終端倍數必附≥1個同業現值comp對照 [§3]。10Y二段延伸(`runway_post_y5`=🟢且終端倍數承重，或Base IRR實質來自Y5後)：Y5→Y10 EPS CAGR/10Y累積倍數/IRR。R:R數學假象：下行>15%正常使用；5-15%警示「已接近定價」；<5%失效標「數學假象」禁引用進場判定，改極端Bear(Bear PE×0.8+Bear EPS×0.85)重算(Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境) [§3]。

**Max DD**(`premortem.max_dd`)：填範圍`lo`/`hi`(禁單點，寬度≥10pp)+`path_risk`(🟢0～−30%/🟡−30～−50%/🔴<−50%)；推導依據須寫`reasoning.premortem`。硬接線：🔴且thesis脆弱(`moat.trend`↓或`runway_post_y5`🔴或估值依賴型)→倉位上限下修(6%→≤3%)；🔴但thesis完整→不因波動砍倉，註記「深回撤心理準備」[§2問六]。

**必答項**：`scenario_inputs`三支EPS路徑、終端倍數、Bear/Base/Bull機率、`premortem.max_dd.lo/hi`、`path_risk`。

---

## ④反證裁定

**`premortem.blind_spots[]`（反證唯一居所，違例即無效輸出）**：每條`view`(擇一)｜`evidence`｜`assumption`｜`consequence`｜`ruling`(採納或反駁+理由)｜`watch`(＋`evidence_refs`)。三視角(enum)至少各一條：`論點失敗`(5年後虧50%最可能的故事)／`論點成功但股東經濟變差`／`價格已反映太多`；不適用寫`not_applicable_reason`。steelman、自我攻擊(寫檔前一次inner monologue「最強3個反駁點」，觸及核心論據者併進本紀錄)、trap判斷依據一律引用本紀錄不重寫(`trap_analysis`本欄只交`verdict`🟢/🟡/🔴+`label`，`evidence_for/against`不要填)。視角①與Single Thing對帳(撞上不動/部分重疊回補/獨立則重寫)。**降位不得安靜刪門檻**：前份反證帶指標門檻，本輪降位仍須保留「指標＋門檻＋資料來源」，取不到值標「資料缺口」，確實不成立才退休並在`contradictions[]`寫理由 [§0.5(一)][§2問六]。

**`contradictions[]`**：先列一致判斷，再列矛盾(矛盾點/A側/B側/性質：可調和=程度差異、不可調和=方向相反)；⚖不可調和矛盾必填裁決：選哪邊/依據(非「直覺」)/硬數據點/執行路徑(≥1 if-then＋1反向條件，動作具體如加碼至X%/清倉，禁「再評估」)；Steelman義務：觀望迴避寫「現在就買的最強論證」，進場寫「現在就賣的最強論證」。前份漂移歸因：`drift_watch`20欄按`cause`三選一(`價格變動`/`新證據`/`方法變動`)分組，`prior_field`填涵蓋欄名陣列，漏一欄＝FAIL；門檻或Single Thing與前份不同須歸因「舊→新＋理由」，`rearm_trigger`不得寫「相同」；觀望須點名binding constraint，`rearm_trigger`=該約束的否定，多因素模糊觀望=重寫 [§5]；前次觀望/迴避且報酬>+30%須明寫翻面理由；前份在90天內：`decision_inputs.qc49_inherit_prior`答一題——前份觸發器全部沒發火填`true`，有任一條已發火填`false`並在contradictions引用那條；`prior_verdict`／`prior_role`由程式帶入，不要填 [§4]。

**負向證據強制處置（硬擋）**：`findings_digest[]`每條`direction="-"`的finding必落於`contradictions[]`/`blind_spots[]`/`triggers[]`/`moat.threats[]`/`thesis.R[]`之`evidence_refs`，或寫進`evidence_dismissed[]`(`{"ref":…,"reason":…}`，理由需指出證據本身問題，禁「影響不大」)。`triggers[]`每列`n`/`text`/`type`/`maps_to`/`metric`/`threshold`/`action`/`source_freq`/`date`；type僅八值(假設驗證/風險/Single Thing/估值rearm/加碼/減碼/清倉/複審日期)，H1-H3或R1-R3寫`maps_to`不塞`type`。`kill_metrics[]`陣列，每條`metric`/`bear_threshold`/`window`＋`source`；`rearm_trigger`=估值rearm/進場首倉列；`catalysts[]`type英文六值`product`/`regulatory`/`capacity`/`guidance`/`macro`/`other`(禁中文)。QC-39產業態勢三軸(必填一句)：A競爭惡化/B結構轉好與durability/C其他結構變數(法規/關稅/反壟斷/通路/商模/替代技術/客戶結構)→裁決=競爭惡化中/結構性轉好中/其他結構變動中(指名哪軸)/雙向拉鋸/靜態＋一句sourced依據，禁只報單向 [§6]。重大事件：M&A(>市值5%)/集體訴訟/臨床或FDA讀數/CEO或CFO離職或SEC調查/客戶流失皆🔴，涉核心假設或護城河須入`thesis.R`或`moat.threats` [§5][§6]。

**必答項**：三視角blind_spots各至少一條、不可調和矛盾的⚖裁決、`evidence_dismissed[]`(若有負向finding未落點)、`kill_metrics[]`、`rearm_trigger`。

---

## ⑤決策輸入與行動條件

**`decision_inputs`**（值可`null`，`dd_decision.py`機械路由裁決）七欄：`thesis_irreconcilable`(§4不可調和)｜`valuation_dependent`(re-rate貢獻≥Base IRR 40%；程式依你的情境算後覆寫，你填的僅供對照)｜`market_wrong_reason_given`(市場錯在哪的具體理由)｜`week26_return_pct`(26週漲幅)｜`momentum_overheated`(RSI 14d>70或4週漂移>+10%)｜`cycle_gates_pass`(反動能五閘全過，循環股)｜`consensus_rev_3m_pct`(FY1/FY2共識近3月上修%)，缺值`null`。覆寫層：`val_denominator_disputed`/`qc49_inherit_prior`+`prior_verdict`+`prior_role`/`held_now`(bool三態不可`"unknown"`代`null`)；`asym_ratio`/`irr_base_pct`/`ev5y_pct`一律`null` [§5]。

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
{"status":"no_prior_dd"}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名的每一個**（含程式稍後才會算的 asym_ratio／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct／ev5y_pct／irr_base_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20260929/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
