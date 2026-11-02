你是 stock-analyst **v20 判斷 agent**，標的 EBAY（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"EBAY","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EBAY_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EBAY_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":3206,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"}},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":26.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":19.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"}},{"id":"f_kpi3_free_cash_flow_continuin","label":"Free cash flow (continuing ops)","value":749,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"}},{"id":"f_kpi5_guidance_q4_2026_revenue","label":"Guidance Q4 2026 revenue","value":null,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"},"needs_sonnet":true},{"id":"f_kpi6_guidance_fy2026","label":"Guidance FY2026","value":null,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"},"needs_sonnet":true},{"id":"f_kpi7_gmv","label":"GMV","value":23166,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"}},{"id":"f_kpi8_active_buyers","label":"Active buyers","value":147,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ebay_gross_margin_pct","label":"EBAY 毛利率","value":72.81,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EBAY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ebay_operating_margin_pct","label":"EBAY 營業利益率","value":20.2,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EBAY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ebay_fcf_margin_pct","label":"EBAY FCF 利潤率","value":19.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EBAY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etsy_gross_margin_pct","label":"ETSY 毛利率","value":72.62,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETSY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etsy_operating_margin_pct","label":"ETSY 營業利益率","value":16.91,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETSY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etsy_fcf_margin_pct","label":"ETSY FCF 利潤率","value":19.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETSY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amzn_gross_margin_pct","label":"AMZN 毛利率","value":50.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_operating_margin_pct","label":"AMZN 營業利益率","value":12.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_fcf_margin_pct","label":"AMZN FCF 利潤率","value":-0.82,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_meli_gross_margin_pct","label":"MELI 毛利率","value":42.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MELI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_meli_operating_margin_pct","label":"MELI 營業利益率","value":8.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MELI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_meli_fcf_margin_pct","label":"MELI FCF 利潤率","value":35.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MELI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc","label":"SBC","value":173,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm；IR 頁 investors.ebayinc.com 同稿，未能直接抓取"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":121.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":11.74,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":64.2,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":1.3,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.17 → 6.25）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":2.08,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.74 → 6.88）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":2.76,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.6 → 7.81）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":6.25,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.88,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.81,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.12,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 6.12 → 6.25（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":26.51,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.72,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.42,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 6.25，分子＝快照價 121.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.005,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":5234.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 7209.0、現金 1975.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":439.0,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":58528.6,"period":"2026-11-03","unit":"USD m","basis":"市值 53294.6 ＋ 淨負債 5234.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":12646.65,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（27 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":13554.98,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.63,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 121.33 / W52 100.6 / W104 87.33 / W250 62.82 / W250 13週斜率 1.62%"},{"id":"f_ma_w52","label":"52 週均線","value":100.6,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":87.33,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":62.82,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.62,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"eBay 10-K 列出競爭來源包含傳統零售、電商、直播商務、搜尋、社群與 AI 工具（agents、chatbots）；並稱進入門檻低，專業型對手在 Focus Categories 可能比 eBay 更快滿足社群需求。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"The barriers to competition are low – Competitors can easily launch their own platforms at nominal cost by using commercially available software or partnering with successful ecommerce, search, advertising or social media companies.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 揭露 eBay 依賴 Google 搜尋導流，Alphabet 演算法調整曾減少導流，且若未獲足夠 AI 轉介，買賣家可能轉向其他平台。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"If we fail for any reason to receive sufficient AI referrals to our platforms, or to build, license or acquire the AI technology capabilities that matter to our buyers and sellers, our buyers and sellers or both may choose alternatives to eBay","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"英國 CMA 估計 Vinted 占英國 C2C 服飾 GMV 50-60%，eBay 與 Depop 流失份額。","source":"Value Added Resource: CMA Puts Vinted At 50-60% Of UK C2C Apparel GMV As eBay, Depop Lost Share","url":"https://www.valueaddedresource.net/cma-vinted-leads-uk-apparel-gmv/","excerpt":"CMA Puts Vinted At 50-60% Of UK C2C Apparel GMV As eBay, Depop Lost Share Liz Morton Published: Aug 17 2026 Updated: Aug 23 2026 Comments Share on Twitter","as_of":"2026-08-17","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"eBay Q2 2026 GMV 年增 15%（德國產業站報導，未對照官方）。","source":"onlinemarktplatz.de: eBay Quartalszahlen Q2 2026","url":"https://onlinemarktplatz.de/270838/ebay-quartalszahlen-q2-2026/","excerpt":"eBay Quartalszahlen Q2 2026: GMV steigt um 15 Prozent 6. August 2026 • Veröffentlicht von Frank • ⏱ 7 Min. • 🏷️ eBay, Retail Media, Unternehmenszahlen","as_of":"2026-08-06","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"eBay 10-K 揭露 2023–2025 各年度皆無單一客戶占淨營收超過 10%。","source":"SEC EDGAR 10-K FY2025（申報 2026-02-19）財報附註 Concentration of credit risk","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"In each of the years ended December 31, 2025, 2024 and 2023, no customer accounted for more than 10% of net revenues.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 營收地理分布：美國 52%（$5,789M）、國際 48%（$5,311M），依客戶所在國歸屬。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A Net Revenues by Geography","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"United States $ 5,789 11 % $ 5,238 3 % $ 5,073 % of net revenues 52 % 51 % 50 % International 5,311 5 % 5,045 — % 5,039 % of net revenues 48 % 49 % 50 %","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"eBay 管理層稱 Q1 2026 收藏品為 GMV 成長最大貢獻類別，且金銀條需求為暫時性、預期 Q2 回到歷史水準","source":"Digital Commerce 360, eBay sales GMV AI Q1 FY26","url":"https://www.digitalcommerce360.com/2026/05/01/ebay-sales-gmv-ai-q1-fy26/","excerpt":"transitory benefit to GMV growth from gold and silver bullion","as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"eBay Q2 2026 上調全年財測；Q3 GMV 指引 $22.0–22.4B，FX 中性年增 10%–12%（含 Depop）","source":"eBay Inc. Reports Second Quarter 2026 Results (West Valley View)","url":"https://www.westvalleyview.com/online_features/press_releases/ebay-inc-reports-second-quarter-2026-results/article_5eaa1cb5-826e-5497-b674-c37738175d4e.html","excerpt":"increasing our full-year top- and bottom-line outlook","as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"eBay 聚焦類別、C2C 與二手轉售約占總 GMV 70%","source":"Digital Commerce 360 / eBay Q1 FY26","url":"https://www.digitalcommerce360.com/2026/05/01/ebay-sales-gmv-ai-q1-fy26/","excerpt":"Focus categories, C2C and recommerce now represent approximately 70% of total eBay GMV","as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"EMARKETER 系列預測全球電商 2027 年約 $7.57T（+7.2%）、2028 年約 $8.09T（+6.9%），成長放緩但持續","source":"Oberlo, Global Ecommerce Sales Growth (2022–2028)","url":"https://oberlo.com/statistics/global-ecommerce-sales-growth","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Forrester 預測全球電商年增約 8.9% 至 2028","source":"Talk Business, Forrester","url":"https://talkbusiness.net/?p=274851","excerpt":null,"as_of":"2024-01-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K FY2025 風險因子：DOJ 曾追究 eBay 對第三方銷售的責任；依 2024 年與 DOJ 和解，eBay 付 5,900 萬美元並強化違規刊登監控；公司亦常態面臨反壟斷與不公平競爭相關訴訟與政府調查。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"pursuant to our 2024 settlement agreement with the DOJ, we paid $59 million and agreed to implement enhanced processes regarding our monitoring of listings that violate our terms of service to fully resolve the DOJ’s allegations of noncompliance with the Controlled Substances Act.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"英國競爭監管機關 CMA 對 eBay 擬以 12 億美元收購 Etsy 旗下 Depop 展開調查","source":"PYMNTS eBay tag page","url":"https://www.pymnts.com/cpi_tag/ebay/","excerpt":"UK Regulator Opens Investigation Into eBay’s $1.2 Billion Depop Acquisition By CPI | Jun 8, 2026","as_of":"2026-06-01","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"美國 2025 年取消 US$800 de minimis 免稅額：中國／香港 2025-05-02 起，全部包裹 2025-08-29 起；所有進口件皆須課關稅並補報關資料，可能降低跨境量。","source":"eBay 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"The exemption was first eliminated for shipments originating in China and Hong Kong on May 2, 2025, and then for all parcels effective August 29, 2025. As a result, all imports, regardless of value, are now subject to applicable duties, taxes, fees and standard customs compliance procedures.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"跨境貿易是營收與利潤的重要來源，且為大中華區等市場的主要（或唯一）業務；貿易政策變動可對買賣家造成重大影響。","source":"eBay 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"Cross-border trade is an important source of both revenue and profits for us. Cross-border trade also represents our primary (or in some cases, only) presence in certain important markets, such as Greater China, and various other countries.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"歐盟宣布 2026 年 7 月取消 €150 de minimis 並徵每件 €3 費用，英國預期跟進；2025 年關稅變動已改變消費者支出。","source":"eBay 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"the E.U. has announced it will remove its €150 “de minimis” exemption in July 2026 and require a €3 fee per parcel, and the U.K. is expected to follow with eliminating its £135 “de minimis threshold” for low-value imports.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"eBay 風險因素提及制裁與出口管制合規風險：客戶可能以虛報、轉運等方式規避，公司對客戶行為控制有限。","source":"eBay 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"We have limited control over our customers’ conduct, and some may attempt to circumvent sanctions or export controls through misrepresentation, transshipment, use of intermediaries, or false product descriptions, increasing compliance and enforcement risk.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Jefferies 曾因中國跨境貿易潛在逆風調降 eBay 評等（2025 年報導）","source":"Value Added Resource","url":"https://valueaddedresource.net/ebay-stock-downgraded-as-tariff-worries-mount","excerpt":"downgrades eBay from “hold” to “underperform”, citing concerns about slowing ad revenue growth & possible headwinds to China business. Value Added ResourceLiz Morton Iannone has previously said much of eBay's China inventory is forward deployed with stock stored and shipped from US warehouses. That may slightly delay the initial impact of executive orders that have increased tariffs on","as_of":"2025-04-28","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"美國 $800 de minimis 免稅於 2025-05-02 對中國/香港包裹終止、2025-08-29 對所有包裹終止；eBay 國際業務（英、德及大中華跨境賣家）近年貢獻近半淨營收（摘自風險追蹤站對 eBay 申報文件的整理）","source":"policyrisk.com EBAY company page","url":"https://policyrisk.com/world/company/EBAY","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"CRS 報告（2026-08-07 更新）：CBP 於 2026 年 7 月啟動 $800 以下郵政包裹的報關流程，9 月規劃至 $2,500 的自願電子試行","source":"CRS via everycrsreport, China's E-Commerce Exports and U.S. De Minimis Policies","url":"https://www.everycrsreport.com/files/2026-08-07_IF12891_c01460d13e4142a16bbb301803b1a4f6c049a8a0.html","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"eBay 非自有製造；搜尋未見其核心市集依賴單一第三方雲的證據，歷史上有自有資料中心單點故障事件（2001 硬體故障、2015 與 PayPal 共用機房停電）；2026-04 有一次 eBay 中斷事件被廠商部落格評為賣家 API 單點風險（來源可信度低）","source":"novadata.io; ecommercebytes.com","url":"https://novadata.io/resources/news/ebay-april-2026-outage-multi-channel-api-fragility","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收 $3.2B（+14%，FX-neutral +13%）、GMV $23.2B（+15%，FX-neutral +16%）；成長主要來自收藏品、C2C、eBay Live；Depop 貢獻約 3pp GMV 成長（二手分析）。","source":"eBay Q3 2026 earnings release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 2026 指引：營收 $3.19–3.24B、GMV $23.7–24.1B；全年 2026 GMV $91.5–91.9B。","source":"eBay Q3 2026 earnings release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 2026 GMV 成長由收藏品領軍（Pokémon 30 週年、運動卡加速）；金銀條為暫時性助力於 Q1 末起正常化；焦點品類+C2C+再商務約占 GMV 70%；美國消費需求具韌性、歐洲較疲弱。","source":"Digital Commerce 360, eBay Q1 FY26","url":"https://www.digitalcommerce360.com/2026/05/01/ebay-sales-gmv-ai-q1-fy26/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 take rate 13.84%（去年同期 14.03%）；九個月 13.91% vs 13.94%；下降主因 eBay Live 與 C2C 成長較快及品類/ASP 組合，運送方案與第一方廣告部分抵銷。","source":"eBay Form 10-Q (Sep 30, 2026)","url":"https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000212/ebay-20260930.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"eMarketer 預測 2026 全球零售電商約 $6.88T（+7.2%），2027 約 $7.38T；Forrester 2027 約 $7.6T（二手聚合站轉述，未核原報告）。","source":"SaleHoo eCommerce Statistics 2026 (aggregator citing eMarketer/Forrester)","url":"https://www.salehoo.com/blog/ecommerce-statistics","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"eBay FY2025 10-K 風險因素自述：可能跟不上技術變化（含新興 AI 技術）與消費者期待變化；若未能預見技術趨勢或未投入適當資源，業務可能受損。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"Our industry is subject to rapid technological change, and the demands and expectations of our consumers can change quickly. Predicting the changes that our consumers want, learning new technologies and developing new products and services can be complex, time-consuming and costly, and our investments in new innovations may not yield the expected business or financial benefits.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"eBay 2026 年 1 月更新用戶協議，禁止未經授權的第三方 AI 代購（buy-for-me）代理下單；同時與 OpenAI 合作並測試自家 AI 購物代理。","source":"The Register: eBay updates legalese to ban AI-powered shop-bots","url":"https://www.theregister.com/2026/01/22/ebay_updates_legalese_to_ban/","excerpt":"The company’s decision emerged in an update to its user agreement posted on January 20th, which insists users must not use “buy-for-me agents, LLM-driven bots, or any end-to-end flow that attempts to place orders without human review” on the site, unless eBay grants approval.","as_of":"2026-01-22","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"分析師認為 OpenAI、Google、Perplexity 等 LLM 代理可能顛覆市集模式，市集可能淪為後端履約供應商。","source":"Retail Dive: How AI commerce threatens eBay, Amazon","url":"https://www.retaildive.com/news/how-ai-commerce-threatens-ebay-amazon-retail-sales-merchants/811618","excerpt":"For marketplaces like Amazon and eBay, the large language models that are moving swiftly into agentic commerce – including Perplexity AI, OpenAI and Google – are potentially disruptive to their model, said Adam Behrens, the CEO of New Generation.","as_of":"2026-02-11","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K 描述 eBay 營收來源為 Marketplace 佣金與 Advertising 廣告費，以 GMV 抽成（take rate）為主，策略聚焦 enthusiasts 與 AI；未見訂閱化或 D2C 轉型表述。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"We generate net revenues through two activities, Marketplace activities which primarily consist of commissions from the service of connecting buyers and sellers on our secure and trusted Marketplace platforms and Advertising activities, which primarily consist of fees charged to sellers to promote their listings.","as_of":"2026-02-19","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"eBay 用戶協議自 2026-02-20 起禁止 buy-for-me 代理／LLM 機器人未經人工審核下單，同時自建 agentic 購物","source":"Resultsense: eBay bans AI shopping agents","url":"https://www.resultsense.com/news/2026-01-23-ebay-bans-ai-shopping-agents/","excerpt":"Effective 20 February 2026, eBay’s updated terms specifically prohibit “buy-for-me agents, LLM-driven bots, or any end-to-end flow that attempts to place orders without human review” without platform permission.","as_of":"2026-01-23","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"eBay 2026-10-20 宣布重組，裁員約9%，成本 1.3–1.5 億美元","source":"eBay Form 10-Q (Q3 2026)","url":"https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000212/ebay-20260930.htm","excerpt":"On October 20, 2026, we announced a restructuring plan (the “Plan”) intended to align our teams and resources with our strategic priorities to drive long-term sustainable growth. The Plan includes a reduction of our current global workforce by approximately 9%. In connection with the Plan, we currently estimate costs of $130 million to $150 million, substantially all of which are","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"eBay 於 2026-10-28 公布 Q3：營收 $3.2B(+14%)、GMV $23.2B(+15%)、non-GAAP EPS $1.51（8 月 Q3 指引 EPS $1.36–1.42、營收約 $3.07–3.12B；Newsquawk 列當時共識 EPS 1.41/營收 3.12B 之類預期）；Q4 指引營收 $3.19–3.24B、GMV $23.7–24.1B、diluted EPS $0.82–0.87；FY26 營收 $12.62–12.67B。","source":"eBay 8-K Exhibit 99.1 Q3 2026 / finviz 轉載","url":"https://www.sec.gov/Archives/edgar/data/0001065088/000106508826000209/exhibit991erebayq32026.htm","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師共識評等 Hold，平均目標價約 $109.87–$112.59（依來源），Investing.com 11 Buy/18 Hold/2 Sell；Benzinga 高 $135(Wedbush)、低 $64(TD)；來源日期為 7–8 月，屬 Q3 財報前。","source":"Investing.com / Tickflow / Benzinga 搜尋摘要","url":"https://www.investing.com/equities/ebay-inc-consensus-estimates","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-03 共識目標價 $97.97；之後上升至約 $110（8 月）。","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/ebay-inc-nasdaqebay-receives-average-rating-of-hold-from-analysts-2026-03-13/","excerpt":null,"as_of":"2026-03-13","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-08-05 Q3 指引 EPS $1.36–1.42 對共識約 1.39，營收指引高於前一區間 $2.97–3.03B，報導描述營收指引高於共識、EPS 大致持平；Wells Fargo 與 Citizens JMP 財報前降評。","source":"MarketBeat Q3 2026 guidance","url":"https://www.marketbeat.com/instant-alerts/ebay-nasdaqebay-issues-q3-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-05-12 eBay 董事會就 GameStop 主動提出、不具約束力的收購提案發布回應新聞稿（8-K Item 8.01）；搜尋摘要顯示提案約每股 $125、估值約 $555 億，待核","source":"SEC EDGAR 8-K 2026-05-12 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1065088/000155278126000322/e26249_ebay-8k.htm","excerpt":"On May 12, 2026, the Company issued a press release disclosing the response of its Board of Directors to the unsolicited, non-binding acquisition proposal from GameStop.","as_of":"2026-05-12","retrieved_at":"20261103","affects":["valuation","triggers","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-10-20 宣布重組計畫，全球員工約減 9%，預估稅前費用 $1.3–1.5 億，多數於 2026 Q4 認列，2027 Q1 底前大致完成","source":"SEC EDGAR 8-K 2026-10-22 Item 2.05","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000205/ebay-20261020.htm","excerpt":"On October 20, 2026, the Company announced the Plan, which includes a reduction of the Company’s current global workforce by approximately 9%.","as_of":"2026-10-22","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Steiner 跟蹤騷擾民事案在和解破裂後重啟，據 2026-06 更新審理排定 2027-01-04（eBay 已於 2024-01 與麻州聯邦檢察署達成延後起訴協議）","source":"Value Added Resource: eBay Cyberstalking Suit Reopened","url":"https://www.valueaddedresource.net/ebay-cyberstalking-suit-reopened/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-05-12 eBay 董事會回應 GameStop 主動、不具約束力的收購提案（8-K Item 8.01，附 TD Securities highly confident letter）","source":"SEC EDGAR 8-K 2026-05-12","url":"https://www.sec.gov/Archives/edgar/data/1065088/000155278126000322/e26249_ebay-8k.htm","excerpt":"On May 12, 2026, the Company issued a press release disclosing the response of its Board of Directors to the unsolicited, non-binding acquisition proposal from GameStop.","as_of":"2026-05-12","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FY2025 10-K 揭露公司經常面臨集體訴訟等各類訴訟與政府調查，結果可能對單一期間營運成果產生重大影響；本次搜尋未找到 2026 年針對 eBay 的證券詐欺集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1065088/000106508826000027/ebay-20251231.htm","excerpt":"We are also regularly subject to claims, lawsuits (including class actions and individual lawsuits), government investigations, enforcement actions and other proceedings","as_of":"2026-02-19","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Steiner 民事案重啟，審理排定 2027-01-04","source":"Value Added Resource","url":"https://www.valueaddedresource.net/ebay-cyberstalking-suit-reopened/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"0","claim":"英國 OPSS 2026-02-23 公告 Sand Art Activity Kit 召回（經 eBay 與 Amazon 銷售，沙可能含石棉），屬第三方賣家商品，非 eBay 自有產品","source":"UK OPSS Product Recall 2602-0208","url":"https://www.gov.uk/product-safety-alerts-reports-recalls/product-recall-sand-art-activity-kit-sold-via-ebay-and-amazon-2602-0208","excerpt":null,"as_of":"2026-02-23","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 10 份 8-K 中，重大項目 3 份（2.05、8.01 等），清單未見 Item 4.02 非依賴先前財報；搜尋亦未見 SEC 調查或重編報導","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001065088&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"EBAY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.81,"operating_margin_pct":20.2,"fcf_margin_pct":19.46,"rd_intensity_pct":15.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EBAY","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"ETSY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.62,"operating_margin_pct":16.91,"fcf_margin_pct":19.65,"rd_intensity_pct":14.8},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETSY","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"AMZN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.01,"operating_margin_pct":12.36,"fcf_margin_pct":-0.82,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MELI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":42.68,"operating_margin_pct":8.26,"fcf_margin_pct":35.27,"rd_intensity_pct":7.33},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MELI","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"EBAY"},"financial_history":{"ticker":"EBAY","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":9795000000.0,"revenue_yoy_pct":null,"gross_margin_pct":72.64,"operating_margin_pct":23.99,"net_income":-1269000000.0,"diluted_eps":-2.27,"free_cash_flow":1805000000.0,"fcf_margin_pct":18.43,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":10112000000.0,"revenue_yoy_pct":3.24,"gross_margin_pct":71.98,"operating_margin_pct":19.2,"net_income":2767000000.0,"diluted_eps":5.19,"free_cash_flow":1970000000.0,"fcf_margin_pct":19.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":10283000000.0,"revenue_yoy_pct":1.69,"gross_margin_pct":71.99,"operating_margin_pct":22.54,"net_income":1975000000.0,"diluted_eps":3.94,"free_cash_flow":1956000000.0,"fcf_margin_pct":19.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":11100000000.0,"revenue_yoy_pct":7.95,"gross_margin_pct":71.45,"operating_margin_pct":20.51,"net_income":2031000000.0,"diluted_eps":4.34,"free_cash_flow":1434000000.0,"fcf_margin_pct":12.92,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/EBAY/EBAY_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**eBay Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Good day, everyone. My name is Kate and I will be your conference operator today. At this time, I would like to welcome you to the eBay Third Quarter 2026 Earnings Call. [Operator Instructions]
At this time, I would like to turn the call over to John Egbert, Vice President of Investor Relations.

**John Egbert** (Executives):
Good afternoon. Thank you all for joining us for eBay's Third Quarter 2026 Earnings Conference Call. Joining me today on the call are Jamie Iannone, our Chief Executive Officer; and Peggy Alford, our Chief Financial Officer. We're providing a slide presentation to accompany our commentary during the call, which is available through the Investor Relations section of the eBay website at investors.ebayinc.com.
Before we begin, I'll remind you that during this conference call, we will discuss certain non-GAAP measures related to our performance. You can find the reconciliation of these measures to the nearest comparable GAAP measures in our accompanying slide presentation. All growth rates noted in our prepared remarks will reflect organic FX-neutral year-over-year comparisons and all earnings per share amounts reflect earnings per diluted share unless indicated otherwise. Additionally, all year-over-year growth rates versus 2025 are also based on recast financials, reflecting our adoption of the new internally developed software accounting guidance in 2026. And all Depop comparisons will be pro forma FX-neutral year-over-year comparisons unless noted otherwise. 
During this conference call, management will make forward-looking statements, including, without limitation, statements regarding our future performance and expected financial results. These forward-looking statements involve known and unknown risks and uncertainties. Our actual results may differ materially from our forecast for a variety of reasons. You can find more information about risks, uncertainties and other factors that could affect our operating results in our most recent periodic reports on Form 10-K, Form 10-Q and our earnings release from earlier today. You should not rely on any forward-looking statements. All information in this presentation is as of October 28, 2026. We do not intend and undertake no duty to update this information. 
With that, I'll turn the call over to Jamie.

**Jamie Iannone** (Executives):
Thanks, John. Good afternoon and thank you all for joining us today. We delivered strong results in Q3 as our key financial measures exceeded consensus expectations and the high end of our respective guidance ranges. Gross merchandise volume grew by 13% to more than $23 billion. Revenue grew 11% to $3.2 billion. We also delivered 11% year-over-year growth in non-GAAP operating income and nearly 12% growth in non-GAAP earnings per share, even as we continue to invest behind our highest priority growth opportunities. 
Our outperformance was once again broad-based across categories, geographies and customer segments. Our key strategic priorities, including focus categories, consumer-to-consumer or C2C and recommerce grew GMV by approximately 20% in aggregate and now represents 72% of our total GMV, excluding Depop. eBay's results also benefited from the continued scaling of emerging growth vectors like eBay Live and vehicles, which are contributing more meaningfully each quarter as well as Depop, which accelerated materially and contributed to total FX-neutral GMV growth of nearly 16% year-over-year in Q3. Focus category GMV grew 24% in Q3, led by collectibles, eBay Motors, fashion and refurbished goods. Our continued momentum reflects years of strategic investment in category-specific innovation, trust, selection, community and tailored selling and buying experiences for our customers. Starting with collectibles, trading cards maintained strong GMV growth even as we lapped increasingly difficult year-over-year comparisons. 
Pokémon's 30th anniversary releases supported continued growth in collectible card games, while major summer events and the fall sports calendar drove healthy demand for sports trading cards. Excitement for eBay collectibles was on full display at The National Sports Collectors Convention in Chicago, which drove record usage of our AI-powered card scanning tool. The tool has now surpassed 130 million scans. And in Q3, we expanded card scanning to the U.K. and began adding proprietary transaction data from TCGplayer and Goldin to the tool's price guide, giving collectors a broader view of market pricing. In Q3, we expanded authenticity guarantee to lower-priced trading cards in the U.S. and U.K. In the U.S., the change increased the number of sold items eligible for authenticity guarantee by more than 20% and also made those items eligible for grading add-on and vault storage services offered through our partnership with PSA. 
In August, we launched Authenticity Guarantee for collectible coins in the U.S. in partnership with Professional Coin Grading Service. This program covers eligible graded coins from around the world and raw U.S. coins priced at $500 or more at no additional cost to buyers or sellers. Authenticity Guarantee surpassed 20 million cumulative items inspected across categories in July, reinforcing our commitment to building trust and confidence across our marketplace. Our off-platform collectibles marketplaces also continued to thrive. TCGplayer surpassed $1 billion in trailing 12-month GMV for the first time and opened seller registration in the U.K. and Canada, extending the reach of its specialized collectible card game marketplace. Our Goldin subsidiary had another record GMV quarter and continues to attract some of the world's rarest and most valuable collectibles. 
In Q3, Goldin hosted an auction commemorating the United States 250th anniversary, highlighted by a rare copy of the Declaration of Independence that sold for over $3.6 million. By bringing together the core eBay marketplace, eBay Live, TCGplayer and Goldin, we're serving enthusiasts across all major categories, price points and transaction formats. Turning to eBay Motors, which remained a material contributor to GMV growth across Parts & Accessories and Vehicles. In P&A, we launched easy and free returns in Germany in Q3, following successful rollouts in the U.S. and U.K. that drove increased conversion and incremental GMV with stable return rates. We also introduced certified recycled badging in the U.S., helping buyers identify high-quality recycled OEM parts from qualified sellers. In vehicles, we continue to simplify the end-to-end transaction experience and expand the range of customers and vehicles we can serve. 
In Q3, we launched Secure Purchase Express to provide a streamlined path to checkout for C2C sellers who do not require our full suite of services. We onboarded hundreds of independent dealers to our new Trusted Dealer Program, allowing them to use Secure Purchase within their existing workflows. And we increased vehicle purchase protection coverage to $500,000 to support more high-value transactions. These protections and our differentiated buyer reach supported several vehicle sales above $1 million in Q3, including a 2005 Porsche Carrera GT that sold for $5 million from a trusted dealer in Arkansas to a buyer located in Texas. eBay's fashion business continues to be a source of growth, led by luxury, which delivered another quarter of healthy double-digit GMV growth. In Q3, we significantly expanded Authenticity Guarantee across Europe, enabling buyers in 23 European Union countries to shop for authenticated luxury fashion inventory from sellers in Germany, France and Italy. 
In Australia, we launched Authenticity Guarantee for watches and continued broadening eligible brands across apparel, footwear and accessories. This trust infrastructure has helped make eBay the leading online marketplace for secondhand luxury fashion sales in the U.S. and U.K. Depop complements eBay's broader fashion business and expands our reach with younger consumers through its discovery-led experience optimized for desirable, affordable secondhand fashion. Q3 was Depop's first quarter as part of eBay and its results reinforce the strength of the business and gave us even more conviction in the opportunity ahead. Depop's GMV growth outperformed our expectations in Q3, including U.S. GMV, monthly active users and sold items more than doubling year-over-year on a pro forma basis. And the quality of that growth is encouraging. New cohorts are buying and selling more than prior cohorts, while repurchase, relist and resell rates all improved year-over-year. 
Customers who both buy and sell remain several times more valuable than one-sided users, demonstrating the strength of Depop's C2C flywheel. Depop continued to improve its product experience in Q3 as it enabled faster personalized discovery on the homepage, simplified its AI-assisted listing flow and deployed new AI models to prioritize the visibility of higher-quality listings. We also introduced new Depop Balance features in Q3, allowing customers to keep their sales proceeds in the app and use them for future purchases. This makes it easier for sellers to become buyers as well, encouraging the 2-sided engagement we see among Depop's most valuable customers. Marketing and shipping play complementary roles in Depop's growth model. Full funnel marketing has proven effective at raising awareness and bringing more customers into the marketplace. 
Our investments to lower shipping costs have made lower-priced items economical, increased purchase frequency and improve seller velocity. Access to eBay's preferred carrier rates has lowered average parcel cost, making shipping investments more efficient. We are also increasingly targeting those investments toward customer moments we believe are most predictive of long-term value. Beyond shipping, we continue to explore supply and demand synergies between eBay and Depop. In Q3, we tested a dedicated module of relevant Depop listings adjacent to eBay search results for select fashion queries. We are currently testing the next phase of our inventory integration by exploring how users respond to individual Depop listings directly in eBay's search results for relevant queries. 
Over time, we believe eBay's scale of demand and shopping intent signals can connect more fashion consumers with relevant Depop listings and drive incremental GMV and velocity for Depop sellers. Overall, we are managing eBay and Depop as a portfolio, preserving each brand's distinct experience and allocating investment toward opportunities that generate the strongest long-term returns for the combined company. Depop's growth builds upon the strong consumer selling momentum on eBay, where global C2C GMV grew by more than 20% in Q3, including healthy double-digit growth across the U.S., U.K. and Australia. Artificial intelligence has an outsized impact on our C2C business as it reduces friction that prevents consumers from listing and selling successfully. We continue to see strong results from the latest generation of our AI-powered magical listing experience, which is now available to all new and reactivated listers across 6 major markets. 
We've also rolled out Magical Listing to all nonprofessional sellers in Australia, France and Italy and we are in the midst of ramping to active seller groups in the U.S., U.K. and Germany. In Australia, active sellers are creating more than 1/3 more listings per attempter with Magical Listing, while their average listing time has been reduced by approximately 1/3, which is similar to the benefits we have observed with new sellers. As we began ramping active seller groups, we upgraded Magical Listing's pricing guidance, including an improved user experience and new AI models with smarter price recommendations, driving measurable improvements in conversion and sell-through. In September, we launched comprehensive improvements to the C2C value proposition in France and Italy, bringing together free selling, buyer protection, Magical Listing, enhanced local discovery, eBay balanced and simplified shipping. These launches have driven meaningful uplift in leading indicators such as new and reactivated listers and lay the foundation for a more connected European marketplace overall. 
We are also giving sellers new ways to connect directly with buyers and grow their businesses, which brings me to eBay Live. eBay Live delivered another record quarter and is generating GMV at a multibillion-dollar annualized run rate. GMV growth remained well into the triple digits year-over-year, similar to recent quarters as sellers, buyers, content hours and viewership continued to expand across all 7 markets. In Q3, we expanded self-service onboarding to more markets and broadened eligibility beyond established eBay sellers, creating a more scalable path for sellers to join Live. We also launched multi-streaming through Live Studio, which allows sellers to broadcast simultaneously to YouTube, Facebook, Instagram and Twitch, drawing buyers to eBay from their existing social audiences. 
For buyers, we redesigned the Live Hub with updated search, filters, personalized recommendations and a feed-based experience while integrating Live more prominently into services across eBay. This should make relevant events, inventory and communities easier to discover as Live scales. Trust remains foundational to eBay Live. During Q3, we launched AI-powered moderation across chat, audio and video, added pre-event screening and strengthened host controls for moderation. We also deployed real-time multimodal AI agents to extract structured item details directly from video streams. These agents were initially focused on trust and over time, support automated listing creation tools and more intelligent item discovery. Taken as a whole, these advances are expanding seller access and reach, strengthening buyer discovery and embedding AI and trust throughout the experience, helping us scale eBay Live as a differentiated commerce platform. 
In shipping, we are using eBay's scale and carrier relationships to lower cost and simplify fulfillment, helping sellers reach more buyers and making more inventory economical to transact. In Q3, we launched eBay International Shipping in both the U.K. and Germany. Sellers will now be able to ship domestically to an eBay hub and seamlessly tap into buyer demand in more than 190 markets, while eBay handles transportation, customs, returns and post-purchase support. Customer feedback has been extremely positive and the cost savings from these programs are significant. For instance, in the U.K., we estimate eIS can be up to 30% cheaper for customers than our previous Global Shipping Program. In Q3, we also deployed an improved AI delivery date model across 6 major export markets, expanding the inventory we can show with a fast delivery promise while maintaining reliability. 
During the quarter, we completed the nationwide rollout of U.S. managed shipping to all new and reactivated listers. Within the Magical Listing flow, eBay now estimates the package size and weight with AI generates a prepaid label and provides tracking. Sellers are automatically protected against loss or damage and early results show a double-digit percentage reduction in listing time and strong customer satisfaction. In the U.K., we are making pickup and drop-off or PUDO services more visible and economical across more than 50,000 carrier options at lockers and parcel shops with approximately 95% of U.K. buyers living within 1 mile of a PUDO location. We are simplifying the experience and using targeted promotions to build adoption, giving sellers convenient drop-off options and buyers a lower cost alternative to home delivery, which can increase velocity for lower-priced inventory. 
In Q4, we are beginning a limited seller drop-off test in several large U.S. metropolitan areas. Our objective is to learn whether greater shipping choice and structurally lower cost delivery options can improve listing activity, conversion and transaction velocity. We are assessing customer adoption, service quality and unit economics throughout the test. 
Before closing, I'd like to share a few highlights from eBay's 2026 Recommerce Report, which we published earlier this month. The report points to a secular shift in recommerce as 47% of consumers surveyed now buy secondhand at least monthly, up from 35% last year and 89% expect to spend the same or more on secondhand goods in 2027. It also highlights seller economics. Roughly 85% of sellers source secondhand inventory from their own belongings and nearly 30% say selling secondhand helps them earn extra income. Younger consumers are accelerating this shift. 53% of 18- to 29-year-olds expect to buy more secondhand in 2027. That reinforces the long-term opportunity for eBay as secondhand becomes a larger part of how people shop. 
In closing, we are building on strong marketplace momentum with strategic investments that improve the customer experience and strengthen eBay for the long term. Collectibles remained our largest growth contributor. eBay Motors and fashion also contributed materially and eBay Live delivered another record quarter. Depop's first quarter with eBay reinforced its strategic fit as U.S. GMV more than doubled year-over-year on a pro forma basis with healthy new cohorts and growing engagement from customers who both buy and sell. 
Shipping is becoming a more strategic portfolio capability as we expand our domestic and cross-border services and extend eBay's carrier scale and infrastructure to Depop, lowering costs, reducing friction and increasing velocity. AI is delivering measurable gains in listing productivity and conversion while improving discovery, trust and reliability across the marketplace. And we delivered all of this progress while growing non-GAAP operating income and earnings per share at double digits year-over-year, demonstrating our ability to invest behind long-term growth and still deliver significant value for shareholders. 
With that, I'll turn the call over to Peggy to provide more details on our financial performance and outlook. Peggy, over to you.

**Peggy Alford** (Executives):
Thank you, Jamie and hello, everyone. In the third quarter, we once again exceeded expectation across all of our key financial metrics. GMV grew by nearly 16% year-over-year to $23.2 billion on an FX-neutral basis or 13% organically. Revenue grew 13% year-over-year to $3.21 billion on an FX-neutral basis or 11% organically. Non-GAAP operating income grew 11% year-over-year to $843 million. Non-GAAP earnings per share grew nearly 12% year-over-year to $1.51 and we returned nearly $830 million of capital to shareholders through repurchases and cash dividends in Q3. 
Now let's take a closer look at the drivers of our strong performance. GMV grew nearly 16% to $23.2 billion on a total FXN basis and increased 13% on an organic FXN basis as Depop added nearly 3 points of growth. Foreign exchange was a headwind of 30 basis points to spot GMV growth. We saw broad-based momentum across our established strategic priorities as focus categories, C2C and Recommerce each grew GMV by more than 20%, while eBay Live and vehicles each grew well into the triple digits in the quarter. Focus category GMV grew 24%, outpacing the remainder of our marketplace by 19 percentage points with collectibles, motors, fashion and refurbished all contributing materially to growth. 
Moving on to our major geographies. Our U.S. GMV grew 22% on an organic basis with positive growth contributions from all of our major categories. Collectibles GMV growth remained strong in the U.S. but decelerated moderately as we lapped last year's robust growth. Growth in our trading cards business remained broad-based across multiple sports and collectible card game genres. Beyond trading cards, we also saw healthy growth across collectible coins, comics and sports memorabilia. Electronics became a larger contributor to U.S. growth in Q3, driven by strong demand for computer hardware, consoles and video games. The growth in these subcategories was also fueled by a combination of transactions and ASP increases, which reinforces eBay's strength as a leading destination for preowned and refurbished products at more accessible price points. eBay's fashion GMV in the U.S. was healthy with continued strength in luxury. Depop added to our momentum in fashion as its U.S. GMV more than doubled year-over-year on a pro forma basis. 
Combined, eBay and Depop generated approximately $9 billion in fashion GMV over the trailing 12 months in the U.S. alone, growing in the mid-20% range year-over-year on a pro forma basis. International GMV grew nearly 4% year-over-year in Q3 on an organic FXN basis, with foreign exchange representing a 60 basis point headwind to spot growth. Our investments in strategic priorities continue to yield attractive returns in these markets despite a challenging macro backdrop. Specifically, focus category and C2C GMV each grew double digits in the U.K. and each drove high single-digit growth in Germany. Furthermore, our organic year-over-year growth also improved sequentially in Canada, Australia, France and Italy. 
Shifting to our buyer metrics. Trailing 12-month active buyers grew 4% to 147 million on a pro forma basis, which includes buyers from recently acquired Depop and Tise. Excluding Depop and Tise, global active buyers grew by over 1%. U.S. active buyer growth remained strong at 6% year-over-year organically or 13% on a pro forma basis, including Depop. Our 16 million enthusiast buyers who are our most loyal customers visit the core eBay marketplace more than once a day on average and contribute over 70% of the GMV on our marketplace. Our investments in key strategic priorities continue to drive higher engagement and spending, helping grow trailing 12-month enthusiast buyers by over 2% year-over-year in Q3. In the U.S., enthusiast buyer growth was especially strong, up 9% year-over-year. Global spend per enthusiast buyer continues to show strong growth, increasing to approximately $3,700 on a trailing 12-month basis. 
Next, let's take a look at our income statement. Revenue grew 13% to $3.21 billion on a total FXN basis and increased 11% on an organic FXN basis as Depop contributed nearly 2 points of growth in the quarter. Foreign exchange was a 70 basis point tailwind to spot revenue growth. Our overall take rate declined by 20 basis points year-over-year, reflecting faster growth in eBay Live and C2C, ongoing category and ASP mix shifts and the inclusion of Depop. As a reminder, Depop's revenue contribution is lower than GMV, primarily because a significant portion of our velocity driving shipping investments are recognized as contra revenue. These pressures were partially offset by tailwinds from shipping, advertising and financial services. 
Next, I'll discuss highlights within our value-added services portfolio, which continues to benefit our marketplace by strengthening trust, reducing transactional friction and driving sales velocity. Total advertising revenue was $607 million in the third quarter, growing 16% year-over-year. Excluding Depop, ads revenue was nearly 2.7% of GMV. First-party ads grew 16% to $575 million. Promoted Listings comprise nearly 1.3 billion of the nearly 2.7 billion total listings on eBay, excluding Depop, and 6 million sellers adopted at least 1 Promoted Listing product during the quarter. 
We delivered several key product innovations during the quarter to strengthen our performance ads engine. We introduced an AI-powered placement engine that uses machine learning to dynamically optimize ad density in search based on shopper context and expected value. We also expanded our video ad formats across Promoted Listings and Promoted Stores. Video ads create a much more dynamic engaging discovery experience for buyers while giving sellers a powerful new tool to showcase their items. Additionally, we rolled out new personalized ad prompts for C2C sellers that are more relevant and efficient. Financial services was a modest contributor to our take rate as we continue to expand our buyer and seller products to reduce friction on our marketplace. Following a successful U.K. launch, we recently expanded Pay by Bank to Germany and France, which offers more choice for customers and attractive economics for eBay. Similar to the U.K., Pay by Bank transactions in Germany generate high average order values and carry lower processing costs than other forms of payment. 
Moving on to our profitability and earnings. Non-GAAP gross margin was 73.1% in the third quarter, up 60 basis points year-over-year. Our non-GAAP operating income grew 11% year-over-year to $843 million. Sales and marketing expense increased in the third quarter, driven by targeted investments in our strategic priorities, including Depop, based on the strong results we are seeing. Given the upside in our overall performance this quarter, we were able to create more capacity to invest in these areas. In addition, marketing efficiencies in the core eBay marketplace enabled us to redeploy more resources to capitalize on Depop's extraordinary momentum and expand our reach with a younger customer demographic. Transaction losses as a percentage of revenue decreased for a second straight quarter in Q3 as expected and was roughly in line with the year ago period as teams delivered on multiple initiatives to optimize our shipping programs and customer experiences. We delivered non-GAAP earnings per share of $1.51, up nearly 12% year-over-year and GAAP earnings per share of $1.11. 
Turning to our balance sheet and capital allocation. In the third quarter, we generated free cash flow of $749 million and ended the period with cash and fixed income investments of $3.3 billion and gross debt of $6.7 billion on our balance sheet. Our equity investments were valued at $800 million. We repurchased approximately $690 million of eBay shares in Q3 at an average price of roughly $106 and we paid a quarterly cash dividend of $138 million in September or $0.31 per share. Now I will share some thoughts on our outlook, starting with the fourth quarter. Please reference the earnings presentation accompanying our release for our outlook in spot growth terms and foreign exchange implications. 
For Q4, we expect consolidated GMV between $23.7 billion and $24.1 billion, including Depop, which represents total FXN growth between 12% and 14% year-over-year or organic growth between approximately 8% and 10%. Our guidance implies Depop would contribute 4 percentage points to total FXN GMV growth. This guidance contemplates strong broad-based momentum across the core eBay marketplace driven by our strategic priorities in eBay Live, partially offset by lapping dynamics from a very robust fourth quarter last year due in part to trading cards and bullion strength. 
Furthermore, we are forecasting another quarter of extraordinary growth from Depop with Q4 year-over-year growth similar to Q3 on a pro forma basis, driven by effective customer acquisition and engagement. We forecast consolidated revenue to be between $3.19 billion and $3.24 billion in Q4, which represents total FXN growth between 7% and 9% year-over-year or organic growth between 5% and 7%, with Depop contributing 2 percentage points to total FXN revenue growth. We expect GMV growth to outpace revenue growth in Q4 due to a few factors, some of which are temporary. First, Depop is operating at a lower take rate than our core marketplace and its year-over-year take rate pressure is elevated until we lap the acquisition date. Second, the transition of U.K. managed shipping from a gross to net revenue model has impacted our take rate in 2026 and is more significant in Q4 as we lap the completed rollout in the prior year. 
And third, ongoing business, ASP and category mix shifts continue to apply pressure to our take rate, though we are pleased with the incremental GMV, revenue and operating income contributions from these transactions. We expect consolidated non-GAAP operating income growth to be between 6% and 10% year-over-year in Q4, which implies non-GAAP operating margin between 25.7% and 26.2%. Our better-than-expected top line growth in the first 3 quarters of this year has generated the capacity to further invest behind our strategic priorities even as we anticipate strong full year operating income growth well ahead of our initial expectations. As we have consistently noted, our goal is to strike the optimal balance between funding long-term growth and delivering healthy flow-through to the bottom line. Our strategy is clearly working. We see tremendous runway ahead across numerous initiatives, including eBay Live, C2C, as well as Depop, which are significantly expanding our addressable market. 
At the same time, we remain disciplined on costs and continue to drive operational efficiency across the business. With this in mind, last week, we announced the difficult decision to reduce our workforce by approximately 9% to better align our talent and resources, streamline our operations and help create the capacity required to invest in our highest growth initiatives. We recognize the significant impact this decision has on our colleagues and their families and we are deeply grateful for their contributions to eBay. 
For the fourth quarter, we expect consolidated non-GAAP earnings per share between $1.48 and $1.53, which implies year-over-year growth between approximately 5% and 9%. In addition, we continue to target roughly $2 billion of stock repurchases for the full year and our Board declared a quarterly cash dividend of $0.31 per share for the fourth quarter to be paid in December. And finally, I'd like to share our preliminary views on 2027. While we are still in the midst of our annual budgeting process, we are planning our business around healthy consolidated year-over-year growth across GMV, revenue, non-GAAP operating income and non-GAAP earnings per share. We anticipate continued broad-based GMV growth across our strategic initiatives, including focus categories, eBay Live, C2C and Depop. While we expect the performance of our trading cards business to remain strong, our planning assumes growth will naturally moderate as we lap the extraordinary levels we experienced in 2026. 
With regard to profitability, we will continue to strike a balance between funding prudent investments in long-term growth and ensuring healthy flow-through from top line growth to earnings in 2027. Our take rate and margin trends in any given quarter will depend on the mix of our portfolio of businesses, lapping considerations as well as the timing of various business initiatives. Below the operating income line, we forecast modest headwinds to net interest income on a year-over-year basis given our lower cash balance and interest rate assumptions. And we expect our non-GAAP tax rate to remain relatively stable. Our long-term capital return framework remains unchanged. In a normal year, we plan to target repurchases and cash dividends totaling between 90% to 100% of normalized free cash flow, absent organic or inorganic needs for that capital. 
In closing, we delivered another set of strong results in Q3 with double-digit top and bottom line growth. Our sustained marketplace momentum and disciplined operating efficiencies enabled us to drive strong earnings, all while funding compelling long-term opportunities like eBay Live and Depop. Looking ahead, our conviction in eBay's long-term trajectory has never been stronger. We see tremendous runway to expand our total addressable market and drive durable growth, creating compounding multiyear value for our shareholders. 
With that, Jamie and I will now take your questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Michael Morton with MoffettNathanson.

**Michael Morton** (Analysts):
My first one would be following up on what Peggy just spoke about and sorry to kind of hammer this point home. But there's a lot of moving parts in the business right now. You have live commerce, Depop and autos are all growing at significantly faster rates than the core business. And as you've mentioned, they come in at lower take rates and in theory, require higher incremental investments than the core business. So I fully appreciate you're not guiding to 2027. But how should investors think about your ability to reinvest but then also just the competing forces within the P&L of these businesses that are doing so well? And is the restructuring, does that give you enough capacity to do it without a noticeable impact to margins longer term? And I have a follow-up.

**Peggy Alford** (Executives):
Great. Thank you so much for your question. So first of all, we're very focused on pursuing opportunities overall that can add GMV and operating income dollars even if they carry a lower percentage take rate. You mentioned that. The vehicles business is a perfect example. We've got high-value transactions growing at triple-digit growth and it taps into a very large addressable market that complements P&A. So when we look at picking which strategic priorities we think are going to drive the best balance between top line and bottom line, we really evaluate the opportunities and the earnings overall that they can generate, not really looking at optimizing for take rate because we really believe that investing in a variety of businesses both provides durability overall to the business and also enables us to really drive top line and bottom line growth.

**Michael Morton** (Analysts):
That's really helpful. And then maybe a quick one for Jamie. The live commerce opening up to more sellers during the summertime, I would love your big picture thoughts on the addressable categories for live commerce. There's a perception that it's highly targeted towards things like pack breaking. But when you talk to industry participants, it seems to be effective in categories we might not have expected. Can you talk about your long-term ambitions to see live commerce touch a lot of aspects of eBay's offering?

**Jamie Iannone** (Executives):
Yes. We believe eBay Live has a broad appeal across a lot of different categories and segments. And so when you look at it, it's definitely strong in collectibles but that's across trading cards, coins, et cetera. But we see a lot of strength from a lot of other areas, fashion, handbag, watches, Home & Garden. I mean I think just going on to the Live Hub, you can see kind of the breadth of things that are on the platform. And as it gets more popular and more mainstream, you see kind of even more different types of sellers coming on to the platform to drive Live because they really feel like it can drive velocity. Over time, what we're excited by is that we see the Live business and our core business as highly synergistic. 
So if I look over the trailing 12 months, eBay Live sellers, live sellers generate roughly twice as much GMV on the core marketplace as they sold in live events. And we're also seeing higher engagement and spending among live buyers and much of that is incremental outside of live events. So overall, we think it's got obviously a large and rapidly growing addressable market. And we don't think it's bound by categories. We're seeing it continue to expand into new categories as more of our core sellers realize what live can do. It helps them build a better reputation. It helps them build community. It helps introduce buyers into their product. And that's why you're seeing kind of more and more categories of sellers adopt live.

**Operator** (Operator):
Your next question comes from the line of Nathan Feather with Morgan Stanley.

**Nathaniel Feather** (Analysts):
Congrats on the strong results here. One follow-up on live there. Exciting to see the incremental traction. Like, how do you think what are the major gating factors that you see today in order to unlock additional growth in that category? And then any way to think about or quantifying some of the relationship between core GMV growth and live growth?

**Jamie Iannone** (Executives):
Yes. Thanks for the question. So, look, we're excited. Live had another record quarter and it's at a multibillion-dollar annualized GMV run rate with growth well into the triple digits, similar to recent quarters. I think self-service is a big part of that. Previously, it had been gated by how we were bringing on sellers. Now we're able to really open the live up to more sellers and bring them onto the marketplace. We've been driving demand in new and compelling ways. We launched multi-streaming that allows sellers to leverage their social audiences to bring into their lives on eBay. We've redesigned the Live Hub to help buyers find more. So we continue to expand in terms of countries and categories that we're going after. 
And I would say every week or 2, we're adding new features at the request of sellers. So this quarter, we added flash deals, which has been well received. We built new AI-powered moderation tools for host and that gives kind of more protection and more trust in the platform, which has been important for us. And overall, what we see is that we see this halo effect with core. And it makes a lot of sense, right, which is that if I find you during live, that's going to help accelerate the core business. And if I'm already a core seller and you're doing lives or a core buyer and doing lives, you see that synergy. And that's why I was saying when you look over the trailing 12 months, our live sellers did twice as much GMV on core as they did on live events. And I talked last quarter about what we were seeing from buyers, which is buyers are spending 70% more when they get involved with live versus comparable buyers. So it really is kind of this halo effect of core and live working together that's exciting for our sellers and exciting for the growth potential of live.

**Nathaniel Feather** (Analysts):
Great. That's really helpful. And then on Depop, help us think through how you're determining the appropriate level of marketing spend to allocate to that business? And any metrics you're keenly watching as it goes through that hyper growth phase?

**Jamie Iannone** (Executives):
Yes. Look, we're feeling great about the strong Q3 results. We saw U.S. GMV, monthly active users and sold items more than double year-over-year on a pro forma basis. And our trailing 12-month active buyers reached 11 million in Q3, which is up from 9 million and they also reached 5 million active sellers. So really good kind of traction across the base. I think the other thing that we're seeing is that the quality of the buyers that are coming on to the marketplace are very strong. The new cohorts that we're seeing are buying and selling more than prior cohorts. And the repurchase, the relist and the resell rates are all improved year-over-year. So across the board, we're seeing the metrics that we want to see. 
Peggy, anything you want to add on that?

**Peggy Alford** (Executives):
Yes. I would just add that the investments that we're making in marketing and shipping and affordability are really supported by the strong customer engagement that we're seeing. And we're managing these investments across eBay and Depop, allocating resources towards the opportunities with the strongest returns while also continuing to drive efficiencies across both businesses. And then we're increasing -- increasingly leveraging synergies between eBay and Depop, particularly in areas like shipping. So the distinction between the investments we're making in each one is starting to become a little more blurred because we're really seeing the complementary nature of the 2 platforms together.

**Operator** (Operator):
Your next question comes from the line of Deepak Mathivanan with Cantor Fitzgerald.

**Deepak Mathivanan** (Analysts):
Jamie, when ChatGPT was growing fast, you made it a priority to improve AI capabilities at eBay, both in terms of user experience, seller tools and also in several other places. Now with Muse, how are you thinking about the product priorities for the agentic era on eBay for buyers and sellers? Maybe also talk a little bit related to it, specifically on recommerce, right? Like now it seems like with agentic tools like Muse growing, the friction in inventory cataloging, listing, transacting can be eliminated meaningfully. Do you see this already in consumer behavior at this time in these categories? And how is eBay planning to tap into this opportunity?

**Jamie Iannone** (Executives):
Yes. Thanks for the question. I would start by saying that I agree AI is meaningfully contributing even to the growth we're seeing today on the marketplace. You talked about listing and cataloging, part of the reason why we're expanding Magical Listing. I talked about we're now in 6 major markets. We're expanding into seller cohorts in U.S., U.K. and in Germany is because of the results of what we're seeing. I talked about Australia seeing 30% more listings per attempter and reduced listing time. 
We're seeing the same type of thing with our own internal tests as agentic, as it relates to search and discovery and buying behavior. And we think as a leading destination of recommerce, we're uniquely positioned to be one of the biggest beneficiaries of AI because it's really helping us reduce that transactional friction in a scalable way, especially because we're primarily a non-new-in-season inventory marketplace, very different than inventory that's generally out there. As it pertains to third-party experiences, we're continuing to test and learn. We're open to approaches that improve discovery of our unmatched inventory while preserving the trusted end-to-end experience that customers have come to expect from eBay.

**Operator** (Operator):
Your next question comes from the line of Ken Gawrelski with Wells Fargo.

**Kenneth Gawrelski** (Analysts):
Two, if I may, please. First, could you talk about your live distribution strategy? You talked about allowing or enabling your sellers to market their offerings elsewhere. But is there any thought about -- if you think about live, it's not just a commerce experience but it's an entertainment experience as well. Are there opportunities to syndicate your listings and still capture a lot of the economics and really benefit some of your sellers across other properties that are more known for short-form entertainment? That's question one. And question two, could you just talk about early learnings from the consumer-to-consumer side, what you've seen out of Depop? Could you talk about the competitive environment in the U.S.? Vinted has continued to be quite aggressive in the market and it seemingly is growing quite nicely but Depop as well. Could you just talk about what you see there, what you've learned in the next quarter and how that informs your view over the, say, next maybe 12 to 15 months?

**Jamie Iannone** (Executives):
Yes, sure. Great. So this is one of the things that we're excited by with live distribution is the ability to put it out there, both having our sellers do so and to do it in cooperation with our sellers. So you may see across Facebook or Instagram, our sellers highlighting upcoming streams to targeted audiences. That's work we're doing together with them. The reason we launched the multi-streaming capability was, it was a highly requested feature from our sellers. A lot of them have large followings across TikTok or Instagram or Twitch or other platforms and they want to be able to drive as much demand to it. And so to be able to not only highlight your upcoming shows on eBay Live but to multi-stream them. And that's great for us because that brings new buyers to eBay from all of those areas. So we're going to continue to look at more services and more avenues. 
What's been great is as we've done self-service, we've opened up a lot more streaming hours. And that's really, as you talk about the entertainment factor of eBay Live has been important. And so we're excited by what that growth has just done to the overall kind of streaming hours and number of lives on the platform. As it relates to your question on C2C, we've really strengthened our competitive position over the last several years by sharpening our focus and scale in a really beneficial way. You've seen us do that with the multiyear growth that we have in focus categories. And similarly, we see U.S. C2C fashion as a large and underpenetrated market and one that's not a winner take all. 
So we're really building from a position of strength with 2 well-established brands between Depop and eBay. And in Q3, eBay's U.S. C2C GMV grew faster than overall U.S. eBay GMV. And as we talked about, Depop's U.S. GMV more than doubled. I think what's interesting, Ken, is when you look at them together, which is how we look at it, eBay and Depop generated approximately $9 billion of fashion GMV in the U.S. alone over the trailing 12 months and that's growing in the mid-20 percentage range year-over-year on a pro forma basis. So we're really focused on building on that momentum and investing where we see the strongest returns. As Peggy talked about, we're building on Depop's strong foundation with eBay's demand, our carrier relationships, our technology and our marketplace expertise.

**Operator** (Operator):
Your next question comes from the line of Colin Sebastian with Baird.

**Colin Sebastian** (Analysts):
Great. Maybe a couple for me covering other parts of the business. First off, on advertising, curious if you're seeing any change in seller demand there or how you'd frame the opportunity to increase adoption or penetration rate over time, if that's changed at all? And then secondly, on international, I was hoping maybe you could separate the macro pressures on GMV from the progress you're making through C2C and focus categories in those markets, maybe to help us understand that dynamic a little bit better.

**Peggy Alford** (Executives):
Sure. I can take those. Nice to talk to you, Colin. So on advertising, advertising delivered really healthy growth in Q3. Total revenue increased 16% year-over-year or 15% on a pro forma basis despite tougher year-over-year comps. In Q3, we began lapping last year's attribution changes across several international markets. Marketplace mix is also a factor with some of the faster growth in areas that have lower advertising penetration. We do continue to see a lot of growth opportunities through broader seller adoption, increased listings penetration and even the expansion of priority, off-site and other products. So our confidence in the long-term opportunity remains very strong. We're really focused on improving returns for sellers and growing advertising in a way that supports sustainable revenue and operating income growth across the entire marketplace.

**Jamie Iannone** (Executives):
I would say as it relates to your question on the macro, it's definitely uneven between U.S. and international at this point. In Europe, though, we have seen some improvement in consumer sentiment, particularly in the U.K. but customers, I would say, remain selective. I think Germany continues to face a more challenging spending environment. I think the positive thing is despite these macro pressures, our strategic initiatives continue to perform well. Our differentiated chain of selection, our value proposition almost become a little bit more relevant in this environment. So when you look at preloved or refurbished or other non-new-in-season inventory, it's really giving customers more ways to find what they want at attractive prices. 
It's why you've seen us continue to expand more things into our European businesses. We expanded eIS that we talked about recently. Obviously, we're there with Live. We brought some new C2C capabilities to Italy and France this quarter, ones that we had done in Australia. And we're seeing really healthy double-digit growth in our C2C business, for example, in the U.K. So that makes us confident that as the macro environment improves, the strategy that we have that's working will really continue to drive growth in that market.

**Operator** (Operator):
Your next question comes from the line of Bernard McTernan with Needham.

**Bernard McTernan** (Analysts):
Maybe just to start, coins became a focus category in the U.S. Can you talk about this market a little bit, maybe early uptake of authenticity guaranteed and maybe how it differs from the trading card market?

**Jamie Iannone** (Executives):
Yes. It's another one of these huge enthusiast categories on the platform where these coins enthusiasts, what's important to them is the same type of thing, which is they want to have kind of Authenticity Guarantee. So we launched that in August of this year through a partnership with PCGS. We introduced the program at the ANA's World Fair of Money and then we completed the rollout to all sellers in September. A fun stat. There's the first coin authenticated was the 2026 Cooks Island Thunder Dragon (sic) [ 2026 Cook Islands Thunder Dragon ] silver coin for $900. And I'd say the best way to learn about this industry is actually just go on eBay Live and watch the coin sellers. You'll see in the commentary, et cetera, there's just a lot of enthusiasm for this as a -- as another collectible area. And I would just say coins is the next of what are many interesting areas in collectibles that we can continue to drive the playbook on and where we're seeing excitement across both the core platform and across live.

**Bernard McTernan** (Analysts):
Understood. And just to follow up on all the commentary and discussion on Depop so far. I thought the Recommerce Report had a really interesting stat in terms of the jump in monthly purchasing from 35% last year to 47% this year. That's a really significant jump. Anything in terms of why you think this is happening right now in the U.S.? I know it's a couple of years at least behind Europe but why it's happening now in the U.S.?

**Jamie Iannone** (Executives):
Yes. Look, I think I'm seeing this with my own kids and their friends with that increasing behavior. And I think it's a secular shift. I think when you look at it, the younger generation specifically is much more focused on sustainability and driving recommerce. I think initiatives like what Depop is doing is really unlocking stuff that's sitting in the closets. I'd like to say that the average household has $4,000 of stuff that could be online and less than 20% of it is online. If you talk to Gen Zs, they'll tell you everything that you ever want already exists in this world. And what we're doing through magi and Depop -- Magical Listings and Depop is really unlocking that, creating less friction and driving that kind of secondhand. 
I guess the last thing I would say is that I think all the work that we've done in AG has helped build trust in secondhand, specifically in categories like watches and handbags and that type of thing. And the last is value. We're seeing strength in our electronics business right now. And I find it hard to not buy a refurbished product on eBay because it's coming at a value, it's coming with a 2-year warranty, et cetera. And I'd say the last factor of that increase is just people are realizing the value that they can get from secondhand.

**Operator** (Operator):
Your next question comes from the line of Brian Pitz with BMO Capital Markets.

**Brian Pitz** (Analysts):
Maybe starting with active buyers, up to 147 million, 10% growth. But if you actually exclude Depop and Tise acquisitions, I think growth was closer to 1%. Can you talk about the plans to really accelerate organic buyer acquisition for the core marketplace beyond these inorganic additions? And then maybe a quick one on Depop. I know you're going to operate this as a separate business. But given the size of the investment, can you maybe talk about specific back-end synergies you may realize in search or AI or payments that could be realized without compromising the social forward brand experience for the Gen Z audience?

**Peggy Alford** (Executives):
Great. Thanks so much for your question. I'll start and answer your question on the buyers. So we've been encouraged by both the growth of our buyer base as well as the quality of the engagement across the marketplace. On a pro forma basis, the trailing 12-month active buyers grew 4% to 147 million, including Depop and Tise. If you exclude those businesses, to your point, active buyers grew by over 1%. And -- but that's led by 6% organic growth in the U.S., partially offset by softer trends in international markets. So that's one factor I'd point out with regard to the difference between U.S. and outside of the U.S. 
On the core eBay marketplace, we had trailing 12-month enthusiast buyers that grew by over 2% with U.S. enthusiast buyers up 9%. We also focus a lot on the spend per buyer and we saw enthusiast buyers increasing to approximately $3,700. It's been increasing quarter-over-quarter for the last several years. So we're really focused on our C2C initiatives, better listing tools and discovery, eBay Live, which Jamie talked a lot about and targeted marketing, all helping us attract customers and giving them more reasons to return to buy more frequently and to deepen their relationship with eBay. I'd also just remind that the active buyers is a trailing 12-month metric. So it takes time for the stronger GMV momentum that we're seeing to fully translate into buyer growth.

**Jamie Iannone** (Executives):
Yes. And on your question on Depop and leveraging kind of core parts of eBay, I think we're already seeing the benefits of having these businesses together. I'd start with shipping. Access to eBay's carrier rates has already lowered Depop's shipping and parcel rates, making shipping investments more efficient and there's a lot more work for us to do there. We've also been leveraging eBay's traffic and testing a dedicated module of relevant Depop listings in eBay's search for select fashion queries, which is really connecting our existing shopping demand with Depop's inventory. 
I think all the ones that you mentioned, Brian, are areas that, over time, we will be able to leverage eBay's capability with Depop, things like our regulatory compliance, all the work we've done in authenticity, our payment solutions and frankly, all the work that we've done with AI to make products -- make listings easier to bring on to the marketplace. We think all of those over time are opportunities. And we have a really robust road map and we're excited to continue to unlock more of the potential through those synergies in Q4 in 2027 and beyond.

**John Egbert** (Executives):
Operator, can we do one last question, please?

**Operator** (Operator):
Yes. Your final question comes from the line of Mark Mahaney with Evercore ISI.

**Mark Stephen Mahaney** (Analysts):
I'll just ask one question on agentic. We've had a couple of interesting public data points on how big commerce activities are underlying some of these consumer agents, the Instinct and Muse. How do you view the rise of these? I assume there's going to be more kind of in the freemium model space. I think Google hinted at that in its earnings call tonight. How do you think that -- how do you think about those, as kind of additional platforms, more opportunities to acquire customers? Anything that suggests to you that it makes it more challenging or less challenging to acquire, retain customers?

**Jamie Iannone** (Executives):
Yes. We believe that this traffic will be largely incremental to eBay. While it's -- I would say it's very, very small today, it does bring over new and reactivated buyers at a higher rate than other similar channels on the platform. I think what's great about eBay is, we have a very strong and loyal base of buyers on the platform. 85% of our traffic is organic. Enthusiast buyers represent over 70% of our GMV. They visit us more than once a day. And as Peggy talked about, they spend $3,700. But we've got a track record of using other channels to bring new buyers to eBay and then turn them into enthusiast buyers on the platform. 
Importantly, even though the traffic is small today, we're seeing that roughly half of the new buyers from those referrals come directly to eBay for their subsequent purchases. So we're open to ways to find opportunities to bring new traffic in, convert them to enthusiast buyers. And as I've said upfront, what's really, I think, important is that the AI, what we've already seen is the AI that our sellers are using and the AI tools that we're giving to buyers are really having a big impact on the business today through Magical Listing, through other tests that we're doing, et cetera. So excited to keep kind of leveraging those. We think it's going to be a big structural tailwind for eBay.

**Operator** (Operator):
Thank you for joining. This concludes today's call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### EBAY_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：Q3 合併 GMV 財測區間（含 Depop）（原話："We expect consolidated GMV between $22 billion and $22.4"）
- 2026-08-05｜CFO｜guidance：Q3 non-GAAP 營業利益成長財測 1%–5%（原話："We expect consolidated non-GAAP operating income growth to"）
- 2026-08-05｜CFO｜margin：Q3 隱含 non-GAAP 營業利益率區間（原話："which implies non-GAAP operating margin between 25.1% and"）
- 2026-08-05｜CFO｜margin：Depop 對 Q3 營業利益成長的拖累幅度（原話："3- to 4-point headwind to non-GAAP operating income growth"）
- 2026-08-05｜CFO｜guidance：全年 FX-neutral GMV 成長財測 11.5%–12.5%（原話："GMV growth between 11.5% and 12.5% on an FX-neutral basis"）
- 2026-08-05｜CFO｜guidance：全年 non-GAAP 營業利益成長財測 10%–12%（原話："expect consolidated non-GAAP operating income growth between"）
- 2026-08-05｜CFO｜guidance：全年 non-GAAP EPS 成長財測 10%–12%（原話："full year consolidated non-GAAP earnings per share growth"）
- 2026-08-05｜CFO｜guidance：全年營收成長財測 11%–12%，較 GMV 低約 0.5 點（原話："growth to be roughly 0.5 point below GMV growth on an"）
- 2026-08-05｜CFO｜guidance：Depop 對 Q3 GMV 成長貢獻約 2.5 個百分點（原話："contribute approximately 2.5 percentage points to total"）
- 2026-08-05｜CFO｜guidance：全年 non-GAAP 稅率假設 17.5%（原話："non-GAAP tax rate of 17.5% for the full year"）
- 2026-08-05｜CFO｜margin：Q2 take rate 持平 14%，管理層拆解正負因素（原話："rate was flat year-over-year at 14%."）
- 2026-08-05｜CFO｜margin：Q2 non-GAAP 毛利率 74.1%（原話："Non-GAAP gross margin was 74.1% in Q2, up 1 point"）
- 2026-08-05｜CFO｜margin：Depop 營收貢獻低於 GMV 貢獻的原因（運費投資記為 contra revenue）（原話："primarily because a significant portion of our planned"）
- 2026-08-05｜CFO｜margin：交易損失較上季下降（原話："we also saw a moderation in transaction losses sequentially"）
- 2026-08-05｜CFO｜margin：下半年起開始對上年度行銷效率提升的基期（原話："notable step-up in efficiency in the prior year midway"）
- 2026-08-05｜CFO｜commitment：全年約 20 億美元庫藏股目標維持（原話："We continue to target roughly $2 billion of share"）
- 2026-08-05｜CFO｜commitment：計畫提高季度回購速度（原話："plan to increase our quarterly repurchase rate from Q2"）
- 2026-08-05｜CFO｜commitment：Depop 預計 2028 年對合併 non-GAAP 營業利益轉為增益（原話："Depop is going to become accretive to consolidated non-GAAP"）
- 2026-08-05｜CEO｜commitment：美國目前無調整 eBay 費用的計畫（原話："we have no current plans to change the fees as it relates to"）
- 2026-08-05｜CFO｜commitment：下半年將把部分超額營收再投資（原話："also plan to reinvest more of our top line performance in"）
- 2026-08-05｜CFO｜capital_allocation：Q2 回購 3.1 億美元及均價（原話："We repurchased $310 million of eBay shares in the second"）
- 2026-08-05｜CFO｜capital_allocation：管理層說明 Q2 回購速度受股價波動影響（原話："The pace of repurchases in Q2 was influenced by share price"）
- 2026-08-05｜CFO｜capital_allocation：Depop 收購於 7/30 完成，現金 14 億美元（原話："On July 30, we closed the acquisition of Depop for $1.4"）
- 2026-08-05｜CEO｜competition：被問競爭強度（含新進者）時管理層對自身競爭地位的描述（原話："we feel like we're in a very strong competitive position."）
- 2026-08-05｜CFO｜competition：Q3 需對上年度行銷效率提升（有利競爭環境）的基期（原話："We also will continue to lap last year's marketing"）
- 2026-08-05｜CFO｜risk：下半年財測已內含 Pokémon 成長減速（原話："we expect, and this is baked in a deceleration in Pokémon"）
- 2026-08-05｜CFO｜risk：Q4 起開始對上年度黃金/白銀需求強勢的基期（原話："start to lap the strength in the bullion demand"）
- 2026-08-05｜CEO｜risk：德國策略轉向可能短期壓抑整體 GMV 與買家（原話："That transition may create some near-term pressure on"）
- 2026-08-05｜CFO｜risk：國際市場總經環境仍偏弱（原話："continued weaker macroeconomic conditions in these regions."）
- 2026-08-05｜CEO｜risk：貴金屬對 Q2 GMV 的貢獻較前兩季溫和（與前季說法對照用）（原話："Gold and silver bullion remained a positive contributor to"）
- 2026-08-05｜CEO｜product：eBay Live 開放美國賣家自助上架（原話："launched self-service onboarding for eligible U.S. sellers"）
- 2026-08-05｜CEO｜product：新一代 Magical Listing 在澳洲對所有 C2C 賣家開放（原話："Australia is our first market where we have released the"）
- 2026-08-05｜CEO｜product：核心搜尋導入更多自然語言能力（原話："We are now working to bring more natural language"）
- 2026-08-05｜CFO｜customer：國際 GMV 成長 4%（organic FX-neutral）（原話："International GMV growth improved to 4%"）
- 2026-08-05｜CFO｜customer：活躍買家 Q2 成長近 2%（原話："Active buyers grew nearly 2% to 136 million on a trailing"）
- 2026-08-05｜CFO｜customer：Depop 買家數將自 Q3 起計入 eBay 活躍買家（原話："we're excited to include them in our buyer count starting in"）
- 2026-08-05｜CEO｜product：廣告滲透率 3% 為中期目標而非上限的說法（原話："we've always said that, that 3% is just a midterm"）

### 問答異常語氣（迴避／改口／保留）
- EBAY_Q2_2026_Earnings_Call_20260805.md｜問：Morton（MoffettNathanson）問美國與國際 C2C 的競爭強度，且多家對手在積極投資｜答法：Jamie 回答談 C2C 時尚的未滲透機會與 Depop 的互補性，未直接談競爭強度或對手；Motors 問題（有機成長 vs Caramel 整合帶來的可衡量性）Peggy 只答涵蓋範圍，未回答成長率拆解
- EBAY_Q2_2026_Earnings_Call_20260805.md｜問：Sandler（Barclays）問核心 eBay 剔除 Depop 後，Q3/Q4 對基期的更新與下半年成長信心｜答法：Peggy 說明基期因素並稱 2 年疊加基礎下 Q3 成長 'still quite healthy'，未給核心不含 Depop 的具體 Q4 數字
- EBAY_Q2_2026_Earnings_Call_20260805.md｜問：Deepak（Cantor）問核心哪些市場的行銷費用屬可裁量、可轉配給 Depop｜答法：Peggy 回覆談 OpEx 紀律與協同，未指出具體市場或金額
- EBAY_Q2_2026_Earnings_Call_20260805.md｜問：Champion（Piper）問長期 GMV 成長機會的框架或粗估｜答法：Jamie 談成長廣泛、2 年疊加、策略重點占比提升，未給長期成長數字或經驗法則
- EBAY_Q2_2026_Earnings_Call_20260805.md｜問：Devnani（Bernstein）問 GMV 成長中訂單量與 ASP 的貢獻拆解，以及核心是否已提前投資｜答法：Jamie 僅稱買家、頻率、售出件數與 ASP 'balanced'、ASP 變動來自組合，未給量化拆解

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
{"date":"20260516","verdict":"觀望（B，thesis 完整但估值偏貴+MA stretched，QC-22 漂移 +13.3% 追高警示）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"FCC + AI 工具 + Ad business 三策略支撐 underlying GMV 維持 5-8% organic FX-neutral 成長（vs 2019-23 平均 ~0%）","columns":{"2Y 驗證點":"FY26-27 GMV organic FX-neutral ≥ 6%（Q1 26 +14% 含 ~3-4pp 高基期效應 + ~1-2pp Depop 預期，underlying ~7-9%）","5Y 驗證點":"FY28-30 GMV organic ≥ 5%；FCC 占比 ≥ 50%（vs 2025 ~30%）","10Y 驗證點":"FY31-35 GMV organic ≥ 4%（成熟 e-commerce 加快二手循環）","具體數字門檻 + 信息來源":"FCC 占比 ≥ 50%（Investor Day 2024 公開目標）；信息來源：Q1 2026 法說會 + 2024 Investor Day 簡報","漂移觸發條件":"連 4 季 TTM organic GMV YoY"}},{"id":"H2","text":"Capital return engine 維持：FCF ≥ $1.5B/yr 支撐 ~$2-2.5B 回購 + $550M 股利，share count -3-4% / yr","columns":{"2Y 驗證點":"FY26-27 FCF ≥ $1.5B；buyback ≥ $2B/yr；share count 從 444M → 410M","5Y 驗證點":"FY28-30 累計 FCF ≥ $7B；累計回購 ≥ $10B；share count → 380M","10Y 驗證點":"FY31-35 維持低槓桿（D/E ratio ≤ 1.7x），capital return yield 維持 5%+","具體數字門檻 + 信息來源":"FCF ≥ $1.5B（FY24 為 $1.96B 高點，FY25 為 $1.43B 低谷，5Y 均應 ~$1.7B）；Net Debt / EBITDA ≤ 2.5x；信息來源：FY25 10-K + Q1 26 法說會","漂移觸發條件":"連 4 季 TTM FCF"}},{"id":"H3","text":"AI agentic commerce 結構威脅可控；eBay 透過 ToS 防守 + 自家 AI agent + selective partnership 維持 marketplace 中介角色","columns":{"2Y 驗證點":"OpenAI / Anthropic 的 buy-for-me agent 不能繞過 eBay ToS 完成交易；eBay 自家 AI shopping agent pilot 啟動 ≥ 1M MAU","5Y 驗證點":"eBay GMV 不因 agentic commerce 滲透下降（即使 LLM 直購率達 5-10%，eBay GMV 仍能 +5%/yr）","10Y 驗證點":"eBay 找到與 agentic commerce 共存模式（例：成為 LLM 推薦的 trusted recommerce backend），長期市佔不再下滑","具體數字門檻 + 信息來源":"Agentic commerce 美國消費者滲透率","漂移觸發條件":"連 2 季 ChatGPT shopping MAU > 15M 且 transactional 完成率 > 40% → 削弱（短期假設用 2 季基準）；OpenAI / Anthropic 與 Amazon / Walmart 簽 marketplace API deal 而 eBay 缺席 → 反轉（單一事件可觸發）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Q2/Q3 26 GMV miss：Q1 大 beat 是 cyclical bounce + FX 順風 + 高基期效應，underlying organic 僅 7-8%；Q2 管理層指引 8-10% 已 set high bar，若 Q2 actual 6-7% → 急速反轉 narrative","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Q2 26（7 月公布）+ Q3 26（10 月公布）GMV FX-neutral 成長率","警戒閾值":"Q2"}},{"id":"R2","text":"Depop 整合執行失敗：Etsy 5 年前 $1.62B 買、現以 $1.2B 賣（虧 $420M）已是警示；eBay 整合需處理 brand 獨立性 vs synergy 兩難；若 18 個月後出現 GMV 衰退 / 高 talent attrition / brand confusion → goodwill impairment","columns":{"對應假設":"H2（間接）","時間尺度":"🔥 中期（4-6 季）","監測指標":"Depop 季度 active buyer 成長率（vs 收購前 baseline）；eBay 自家 GMV 是否含 Depop 後出現異常稀釋；2027 H1 是否提列商譽減損","警戒閾值":"Depop active buyer 連 2 季"}},{"id":"R3","text":"AI agentic commerce 結構性 disintermediation：ChatGPT / Perplexity / Anthropic 的 buy-for-me agent 滲透率達臨界後，繞過 eBay 直接連接 Amazon / Walmart / 大型賣家；eBay marketplace 中介估值集體下調","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"(a) ChatGPT shopping / Comet / Computer Use MAU；(b) OpenAI / Anthropic 是否與 Amazon / Walmart 簽 marketplace API；(c) eBay 自家 agent pilot 進度","警戒閾值":"需 ≥ 50% 主觀機率才砍倉。當前評估：OpenAI marketplace API 機率 12-18 個月內 30%、24 個月內 50%。若 Amazon / Walmart marketplace API 公告 + eBay 缺席 = 立即觸發 H3 反轉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":116.13,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EBAY_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
