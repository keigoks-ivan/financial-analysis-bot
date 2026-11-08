你是 stock-analyst **v20 判斷 agent**，標的 MPWR（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MPWR","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MPWR_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MPWR_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":1202.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income","value":464.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi2_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":38.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi3_gaap_operating_income","label":"GAAP operating income","value":357.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi4_gaap_operating_margin","label":"GAAP operating margin","value":29.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi6_operating_cash_flow","label":"Operating cash flow","value":289.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi7_gaap_diluted_eps","label":"GAAP diluted EPS","value":5.51,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi8_non_gaap_diluted_eps","label":"Non-GAAP diluted EPS","value":8.19,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi9_inventory_days","label":"Inventory days（以當季營收計）","value":130,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"days","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_kpi10_q4_fy2026_guidance_reven","label":"Q4 FY2026 guidance: revenue","value":"1315～1385","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mpwr_gross_margin_pct","label":"MPWR 毛利率","value":55.22,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mpwr_operating_margin_pct","label":"MPWR 營業利益率","value":29.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mpwr_fcf_margin_pct","label":"MPWR FCF 利潤率","value":15.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_adi_gross_margin_pct","label":"ADI 毛利率","value":65.8,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_adi_operating_margin_pct","label":"ADI 營業利益率","value":35.72,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_adi_fcf_margin_pct","label":"ADI FCF 利潤率","value":35.57,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_txn_gross_margin_pct","label":"TXN 毛利率","value":60.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_txn_operating_margin_pct","label":"TXN 營業利益率","value":41.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_txn_fcf_margin_pct","label":"TXN FCF 利潤率","value":35.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_vicr_gross_margin_pct","label":"VICR 毛利率","value":60.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VICR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_vicr_operating_margin_pct","label":"VICR 營業利益率","value":24.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VICR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_vicr_fcf_margin_pct","label":"VICR FCF 利潤率","value":9.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VICR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ifx_de_gross_margin_pct","label":"IFX.DE 毛利率","value":39.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IFX.DE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ifx_de_operating_margin_pct","label":"IFX.DE 營業利益率","value":14.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IFX.DE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_ifx_de_fcf_margin_pct","label":"IFX.DE FCF 利潤率","value":8.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IFX.DE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_and_related_expenses","label":"SBC and related expenses","value":106.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1296.22,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-17.34,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":53.74,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（27.55 → 27.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（35.27 → 35.27）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（41.1 → 41.1）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":27.55,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":35.27,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":41.1,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":13.98,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 24.17 → 27.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":71.02,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝96.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":96.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":16.91,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":16.62,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":47.02,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 27.55，分子＝快照價 1295.43","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.583,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1091.23,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 0.0、現金 1091.23（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":48.79,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":62115.39,"period":"2026-11-03","unit":"USD m","basis":"市值 63206.62 ＋ 淨負債 -1091.23","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":4335.75,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":6425.61,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":14.33,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 1271.73 / W52 1241.74 / W104 972.4 / W250 719.04 / W250 13週斜率 1.77%"},{"id":"f_ma_w52","label":"52 週均線","value":1241.74,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":972.4,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":719.04,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.77,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"公司 10-K 列出十家主要對手（ADI、Infineon、NXP、ON、Power Integrations、Renesas、ROHM、Semtech、ST、TI），並明言預期持續面對既有對手與半導體市場新進入者的競爭。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"We consider our primary competitors to include Analog Devices, Infineon Technologies, NXP Semiconductors, ON Semiconductor, Power Integrations, Renesas Electronics, ROHM Semiconductor, Semtech, STMicroelectronics and Texas Instruments.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：對手規模與資源多數大於公司，且因公司為 fabless 不適用 CHIPS Act 補助，對手藉補助擴產、縮短交期並取得份額。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"Because we operate a fabless business model, we are not eligible for such investments. Many of our competitors benefit from these and other investments, which helps increase their production capacities, shorten their lead times and gain market share.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素：競爭者數量因公司所處細分市場擴張而增加，公司承認無法保證產品持續勝出。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"The number of our competitors has grown due to the expansion of the market segments in which we participate.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"CSIMarket 稱 MPWR 在 Q2 2026 於某區隔份額下滑（儘管整體營收成長 47.68%），區隔與方法論不明。","source":"CSIMarket MPWR Competitors","url":"https://csimarket.com/stocks/MPWR-Competitors","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因子：公司可能面臨客戶內部自行開發產品的競爭，且未來銷售前景取決於客戶接受第三方供應來源取代自製；客戶可能增加自製元件使用。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"We may face competition from customers developing products internally. Our customers generally have substantial technological capabilities and financial resources. Some customers have traditionally used, and continue to use, these resources to develop their own products internally.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 載明公司與 OEM/ODM 客戶無採購承諾，即使取得 design win 也不保證客戶持續採用其 IC。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"we do not have purchase commitments from these customers. Therefore, there can be no assurance that the OEMs and ODMs will continue to incorporate our ICs into their products, even if we may have secured a design win with them.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"搜尋彙總（聚合站）稱無其他直接客戶單一年度占營收超過 10%；未點名最大客戶，亦未見 2026 年第二供應商或自製的具體事件。","source":"Web 搜尋摘要（聚合站，未讀頁面）","url":"https://csimarket.com/stocks/MPWR-Customers","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#3","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Edgewater 稱 MPWR VRM 效能問題可能大幅限縮或消除其 Nvidia Blackwell 配額，Renesas 與 Infineon 被視為取得 B200/GB200 配額。","source":"TipRanks/The Fly: Monolithic Power slides as Edgewater says allocation in Blackwell at risk","url":"https://www.tipranks.com/news/the-fly/monolithic-power-slides-as-edgewater-says-allocation-in-blackwell-at-risk","excerpt":null,"as_of":"2025-06-01","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 三大客戶（皆為經銷商）占營收 26%、18%、10%；2024 年兩家占 31%、20%；2023 年三家占 26%、19%、10%。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"In 2025, three distributors accounted for 26%, 18% and 10% of our total revenue. In 2024, two distributors accounted for 31% and 20% of our total revenue. In 2023, three distributors accounted for 26%, 19% and 10% of our total revenue.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"前三大客戶（皆經銷商）合計占營收 2025 年 54%、2024 年 61%、2023 年 55%；10-K 風險因子明載集中度提高對其信用狀況、庫存作法的曝險。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"our top three customers, all of which are distributors, accounted for an aggregate of 54%, 61% and 55% of our revenue in the years ended December 31, 2025, 2024 and 2023, respectively. Concentration in a small number of distributors increases our exposure to their credit profiles, inventory practices, covenant constraints, and strategic priorities","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Wolfe Research 分析師 Chris Caso 認為 2028 年前半導體幾乎不可能出現供過於求（廠房建置需時長）","source":"247wallst: Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 預估 NAND 供給 2026 年落後需求 4–5%，2027 下半年供給位元成長轉為超過需求（記憶體為主的缺貨，非 MPWR 直接品項）","source":"TrendForce via Webull: NAND Flash supply shortage expected to ease in 2H 2027","url":"https://www.webull.com/news/15263956714857472","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 2026年10月：新增記憶體產能多自 2028 年起釋出，SK hynix CEO 稱缺貨可能延續至 2030；Samsung 傳聞將 Yongin 首座廠提前至 2029","source":"TrendForce News / Herald Corp","url":"https://www.trendforce.com/news/?p=64868","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MPWR Q2 2026 財報電話會議：通路庫存低、訂單趨勢強、book-to-bill 高於 1；成長來自客戶放量、模組含量提升、平台更新與 CPU 相關需求；擴充前後段產能","source":"Chartmill: MPWR Q2 Earnings Call Highlights AI Data Center Expansion","url":"https://www.chartmill.com/news/external/102515/mpwr-q2-earnings-call-highlights-ai-data-center-expansion","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Broadcom 預期 AI 晶片營收 FY2027 約 1150 億美元、FY2028 約 2300 億美元；Gartner 預測 2027 非記憶體半導體營收 8640 億美元（單一廠商/機構預測，非共識）","source":"Bernstein / Gartner via search summary (aicoin, techinsights)","url":"https://www.aicoin.com/en/article/553989","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner：全球半導體庫存指數 2Q26 進入中度缺貨，預期供不應求延續至 2027","source":"Gartner Insights Abstract","url":"https://www.gartner.com/en/documents/8208429","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：公司涉一般商業訴訟（智財、僱傭）及證券集體訴訟與衍生訴訟，未列反壟斷調查；管理層認為已知事項不太可能造成重大損失。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"Based on current information and management assessment, we do not believe that a material loss from known matters is probable as of December 31, 2025.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因子僅提及併購可能受適用反壟斷政策限制，及 FCPA 執法不確定；非針對公司的調查。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"we may be unable to identify or complete prospective acquisitions for various reasons, including competition from other companies or financial investors, the valuation expectations of acquisition candidates and applicable antitrust or other policies, laws or regulations.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MPWR 10-K FY2025：2025 年營收 92% 來自亞洲客戶，風險因子列明貿易法規變動、出口許可、關稅與中美報復性關稅風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"For the year ended December 31, 2025, 92% of our total revenue was from customers in Asia.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"MPWR 10-K FY2025：出口管制與關稅至申報日止未對營收與營運造成重大影響，公司稱供應鏈設計可降低關稅衝擊，但限制可能快速且意外頒布。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"For the year ended December 31, 2025 and through the date we filed this Annual Report, no restrictions or requirements have had a material impact on our revenue and operations.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026 年 1 月 Section 232 對先進半導體及含其產品課 25% 關稅（2026-01-15 生效），含多項豁免（如美國資料中心用晶片）；搜尋結果未載明 MPWR 產品是否適用。","source":"Sec 232 Tariffs on Semiconductors & Their Derivatives Effective Jan 15, 2026 (valexander.com)","url":"https://www.valexander.com/2026/01/16/sec-232-tariffs-on-semiconductors-their-derivatives-effective-jan-15-2026/","excerpt":null,"as_of":"2026-01-16","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K風險因子列出中國生產營運風險、美中關稅與出口管制、台灣與香港緊張局勢，以及倚賴中國關鍵供應商之產能短缺風險","source":"MPWR Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"and uncertainties with respect to China’s legal system, on us and our manufacturing partners and suppliers; • changes in international trade policy, such as tariffs on imports of foreign goods and regulations restricting the export of goods and services, between the U.S. and China or other countries; • political and other risks in Taiwan and Hong Kong due to their tense relationships with","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2022-12 與 Vanguard International (VIS) 簽foundry協議，使用新加坡與台灣8吋晶圓廠，補強既有韓國、台灣、新加坡、中國供應商","source":"Vanguard Foundry Announcement (MPS press release)","url":"https://www.stocktitan.net/news/MPWR/monolithic-power-systems-signs-agreement-with-vanguard-international-vogonjlm0qvx.html","excerpt":"high-performance power solutions, today announced that MPS and Vanguard International Semiconductor Corporation (VIS), a leading specialty IC foundry service provider, have entered into a foundry agreement to produce power semiconductors. MPS will utilize VIS’s 8-inch (200mm) wafer fabrication capabilities in its Singapore and Taiwan manufacturing facilities.","as_of":"2022-12-12","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 分市場：Enterprise Data $506.7M（QoQ +33.2%、YoY +164.6%、占 42.1%）；Automotive $180.7M（YoY +19.2%、占 15.0%，首批 48V 訂單，預期 48V／區域架構設計定案驅動 2027 成長）；Communications $187.4M（YoY +134.7%）；Industrial $71.4M（YoY +29.0%）；Storage and Computing $192.2M（YoY +3.0%）；Consumer $64.0M（YoY -11.6%）","source":"MPWR 8-K Exhibit 99.1 (Q3 2026 earnings release), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 WSTS 預測全球半導體市場成長約 89.9% 至 1.51 兆美元，2027 年再成長約 27% 至約 1.9 兆；8 月 Q2 更新後 2026 約 1.7 兆、2027 約 2.1 兆（成長約 29%）；成長主要由記憶體帶動","source":"WSTS Spring 2026 forecast / Q2 2026 release (via telecomlead, wsts.org)","url":"https://www.wsts.org/76/Global-Semiconductor-Market-records-exceptional-growth-in-Q2-2026","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Nvidia 平台份額有分歧：KeyBanc 預期 MPWR 在 VR200 NVL144 與 R200 HGX 平台約 70% 份額；舊有報導稱 Blackwell 可能轉單 Renesas／Infineon，Deutsche Bank 認為完全失去份額不太可能，約 15% 營收有風險（較舊的 note，未經公司證實）","source":"TipRanks/TheFly: Monolithic Power price target raised to 1250 from 1050 at KeyBanc; Nasdaq: Monolithic Power selling off on report of Nvidia loss says Deutsche Bank","url":"https://www.tipranks.com/news/the-fly/monolithic-power-price-target-raised-to-1250-from-1050-at-keybanc-thefly","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K FY2025 風險因子：客戶可能自行開發或收購與本公司產品類似或可替代的元件／技術，對業務與經營結果構成重大不利影響；未列出特定新興替代技術。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"Customers may continue to increase their use of internally developed components. They may also decide to develop or acquire components, technologies or products that are similar to, or that may be substituted for, our products, or acquire companies that compete with us.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K FY2025 Item 1：公司預期現有競爭者及新進者持續競爭，不保證產品持續具競爭力。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"However, there is no assurance that our products will continue to compete favorably or that we will be successful in the face of increasing competition from new products introduced by existing competitors or new companies entering our markets.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Nasdaq 文章（2026-02）稱 800V DC 資料中心架構為 MPWR 的大機會（非替代威脅）","source":"Nasdaq: Monolithic Power Systems surging, has valuation caught up","url":"https://www.nasdaq.com/articles/monolithic-power-systems-surging-has-valuation-caught","excerpt":null,"as_of":"2026-02-15","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：MPS 主要透過第三方經銷商與加值轉售商銷售，2025 年三家經銷商分占營收 26%、18%、10%（2024 年兩家 31%、20%）；經銷協議為非獨家，未見通路結構性轉變的揭露。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"In 2025, three distributors accounted for 26%, 18% and 10% of our total revenue. In 2024, two distributors accounted for 31% and 20% of our total revenue. In 2023, three distributors accounted for 26%, 19% and 10% of our total revenue.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"二手摘要稱 Q2 2026 營收年增 48%，經銷商通路占營收 88%（未對公司文件核實）。","source":"Panabee Q2 2026 earnings summary","url":"https://www.panabee.com/news/monolithic-power-earnings-q2-2026-report","excerpt":"Operational risks also include high reliance on third-party channels, with 88% of sales flowing through distributors. This structure requires careful monitoring of inventory levels to avoid mismatches between channel supply and end-market demand.","as_of":"2026-08-05","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 記載公司 2026-07-30 給 Q3 2026 營收指引 $1.14B–$1.16B（前一季 Q2 指引 $890–910M）；Benzinga 列的 Q3 共識亦約 $1.14B（未對公司新聞稿核實）","source":"Benzinga MPWR earnings forecasts","url":"https://www.benzinga.com/quote/MPWR/earnings-forecasts","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 實績營收 $980.6M、非 GAAP EPS $6.50，高於預估（營收 $901.9M、EPS $5.65）；Q2 指引 $890–910M 當時高於 Street 共識約 $816M","source":"Benzinga MPWR earnings forecasts","url":"https://www.benzinga.com/quote/MPWR/earnings-forecasts","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Chartmill：FY2026 EPS 共識 $27.83（21 位分析師，截至 2026-10-25）；Q3 預期 EPS $7.91、營收 $1.168B（10-29 公布前）；次季營收預估 3 個月內上修約 17.6%","source":"Chartmill MPWR estimates","url":"https://www.chartmill.com/stock/quote/MPWR/estimates","excerpt":null,"as_of":"2026-10-25","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"KeyBanc 2026-10-19 將 FY2026 EPS 預估由 $21.05 上修至 $24.51、FY2027 由 $29.54 上修至 $34.92，維持 Overweight、目標價 $2,100；MarketBeat 當時引用共識 FY2026 EPS $23.95","source":"MarketBeat: KeyCorp analysts lift earnings estimates for MPWR","url":"https://www.marketbeat.com/instant-alerts/estimates-keycorp-analysts-lift-earnings-estimates-for-mpwr-2026-10-19/","excerpt":null,"as_of":"2026-10-19","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"StockAnalysis：12 個月平均目標價 $1,829.54，15 位分析師、Strong Buy；近期 KeyBanc 目標 $2,100、Needham $2,000；另 Truist 2026-07-31 目標升至 $1,889。目標價 vs 現價須引 numbers.price_at_dd（日期未標）","source":"StockAnalysis MPWR; StreetInsider Truist PT","url":"https://stockanalysis.com/stocks/MPWR","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 統計 2022-10-27 至 2026-07-30 共 17 次指引更新，上調 12 次、下調 4 次；搜尋結果未見 2026 年指引下調。另有來源提及管理層點出下半年毛利率壓力、目前在指引區間低端","source":"Benzinga MPWR earnings forecasts","url":"https://www.benzinga.com/quote/MPWR/earnings-forecasts","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2025-02-04 證券集體訴訟（Waterford Twp. v. MPWR, W.D. Wash.）指控公司與高管違反 10(b)/20(a)；衍生訴訟已合併並暫停；公司稱訴訟無理由。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"On February 4, 2025, a class action lawsuit was filed against us and certain of our executives. The lawsuit is captioned Waterford Twp. Gen. Emps. Ret. Sys. v. Monolithic Power Systems, Inc., et al., No. 25-cv-220 (W.D. Wash.) (the “Securities Action”)","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-02-26 審計委員會判定 FY2024 10-K 與 2025 各季 10-Q 不可再信賴並重編（外國租稅優惠遞延所得稅處理錯誤）；8-K Item 4.02 於 2026-02-27 申報。","source":"SEC EDGAR 8-K Item 4.02","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006112/mpwr20260225_8k.htm","excerpt":"should no longer be relied upon due to the impact of an unintentional error and will be restated as described below.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"搜尋未見 2025-2026 年重大併購公告；最近明確收購為 2024-02 Axign（超出 12 個月窗口）。搜尋亦未見 SEC 調查或 FDA 召回/警告函。","source":"WebSearch 結果彙整","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2025-02-04 證券集體訴訟與兩件衍生訴訟（已合併為 Miller v. Hsing，暫停）。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"On February 4, 2025, a class action lawsuit was filed against us and certain of our executives. The lawsuit is captioned Waterford Twp. Gen. Emps. Ret. Sys. v. Monolithic Power Systems, Inc., et al., No. 25-cv-220 (W.D. Wash.) (the “Securities Action”)","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"2026-02-27 8-K Item 4.02：FY2024 與 2025 各季財報重編；搜尋結果未見 SEC 調查。","source":"SEC EDGAR 8-K Item 4.02","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006112/mpwr20260225_8k.htm","excerpt":"should no longer be relied upon due to the impact of an unintentional error and will be restated as described below.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#1","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"10-K 風險因子指出重編原因為外國一次性租稅優惠的遞延所得稅處理不當，並提示訴訟與監管詢問風險升高。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1280452/000143774926006113/mpwr20251231_10k.htm","excerpt":"we restated our audited consolidated financial statements for the fiscal year ended December 31, 2024 and our unaudited condensed consolidated financial statements for the quarterly periods ended March 31, 2025, June 30, 2025 and September 30, 2025 after we determined that we had not appropriately accounted for deferred income taxes associated with a one-time tax incentive granted by a certain foreign jurisdiction.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MPWR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.22,"operating_margin_pct":29.38,"fcf_margin_pct":15.31,"rd_intensity_pct":12.41},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"ADI","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.8,"operating_margin_pct":35.72,"fcf_margin_pct":35.57,"rd_intensity_pct":14.24},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"TXN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.24,"operating_margin_pct":41.12,"fcf_margin_pct":35.24,"rd_intensity_pct":10.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"VICR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.57,"operating_margin_pct":24.9,"fcf_margin_pct":9.07,"rd_intensity_pct":15.6},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VICR","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"IFX.DE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.42,"operating_margin_pct":14.9,"fcf_margin_pct":8.18,"rd_intensity_pct":15.88},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IFX.DE","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"MPWR"},"financial_history":{"ticker":"MPWR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1794148000.0,"revenue_yoy_pct":null,"gross_margin_pct":58.44,"operating_margin_pct":29.36,"net_income":437672000.0,"diluted_eps":9.05,"free_cash_flow":187831000.0,"fcf_margin_pct":10.47,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":1821072000.0,"revenue_yoy_pct":1.5,"gross_margin_pct":56.07,"operating_margin_pct":26.45,"net_income":427374000.0,"diluted_eps":8.76,"free_cash_flow":580635000.0,"fcf_margin_pct":31.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":2207100000.0,"revenue_yoy_pct":21.2,"gross_margin_pct":55.32,"operating_margin_pct":24.44,"net_income":1592058000.0,"diluted_eps":36.59,"free_cash_flow":624117000.0,"fcf_margin_pct":28.28,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":2790459000.0,"revenue_yoy_pct":26.43,"gross_margin_pct":55.18,"operating_margin_pct":26.11,"net_income":621483000.0,"diluted_eps":12.75,"free_cash_flow":663261000.0,"fcf_margin_pct":23.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MPWR/MPWR_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Monolithic Power Systems, Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to the Monolithic Power Systems Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please be advised that today's conference is being recorded. I would now like to hand the conference over to your speaker today, Arthur Lee. Please go ahead.

**Arthur Lee** (Executives):
Earlier today, MPS released a written commentary on the results of its operations for the third quarter ended September 30, 2026. This document can be found on our website. 
Before we begin, I would like to remind everyone that in the course of today's presentation, we may make forward-looking statements and projections within the meaning of the Private Securities Litigation Reform Act of 1995 that involve risks and uncertainties. The risks, uncertainties and other factors that could cause actual results to differ from these forward-looking statements are identified in the safe harbor statements contained in the Q3 2026 earnings commentary and in our SEC filings, including our Form 10-K and Form 10-Q, which can be found on our website. 
Our statements are made as of today, and we assume no obligation to update this information. Now I would like to turn the call over to Tony.

**Tony Balow** (Executives):
Thanks, Arthur. Good afternoon, and for us, good morning from Shanghai, and welcome to our Q3 2026 earnings call. In Q3, MPS achieved another significant milestone, exceeding $1 billion in quarterly revenue for the first time. Q3 revenue of $1.2 billion was 22% higher than the second quarter of 2026 and 63% higher than the third quarter of 2025. 
During the quarter, our capacity surpassed $6 billion in annual revenue support. We expect to have $8 billion of capacity in place by the second half of 2027 on our way to $10 billion in support of our rapidly expanding business. In our enterprise data end market, we saw strong demand across existing customers, which we expect to continue into 2027. In addition, using our in-house developed AI design tools, we significantly expanded our customer base in traditional areas as well as landing new wins in applications such as desktop AI designs. 
Beyond our strong enterprise data growth in automotive, we received first orders for our 48-volt power solutions and expect design wins for 48-volt and zonal architectures to be a driver of growth in 2027. We started ramping robotic solutions with sensor and motor control products across multiple geographies. We continue to increase our SAM with the ramp of our high-speed memory products. 
We landed our first large data converter design win, which we expect to ramp next year. And we continue to build out our high-voltage portfolio and began sampling GaN-based solutions for use in 800-volt data center architectures, complementing our existing silicon carbide-based designs. And finally, in Q3, we repurchased over $450 million of our own stock. Overall, we see accelerated growth. Our diversified growth strategy is paying off. 
Operator, you may now open the webinar for questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Tore Svanberg with Stifel.

**Tore Svanberg** (Analysts):
Michael and Tony, congratulations on that $1 billion milestone. And to you, Tony, congratulations on your CFO appointment. I guess for my first question, you talked about accelerated growth. I was hoping you can maybe elaborate a little bit of that. I mean I'm sure you're not going to give us calendar '27 guidance, but you are on track to growing 50%, 60% this year. And especially in light of your $8 billion capacity and then $10 billion, when could we potentially see $10 billion capacity in place?

**Michael R. Hsing** (Executives):
Yes. Thanks, Tore. See as Tony mentioned is only a few items, so we see beyond that. And I see this explosive growth period in the next few years. And even this year, you see the first 9 months, okay? And we don't see anything -- any signs of the slowdown.

**Tony Balow** (Executives):
Yes. The other thing I'd add is I think as we've come into the second half, you started to see growth across multiple of our end markets, including like auto, which the ramp started here in Q3, and we've talked about continuing here through the second half. 
And then as we start to see applications like robotics begin to ramp, we'd expect that then to continue into the future. So I think it's not just the existing businesses, it's adding on the additional growth areas over time, which is really giving us confidence going forward.

**Tore Svanberg** (Analysts):
Very good. And as my follow-up, you mentioned the 800-volt GaN product sampling. Now that you are sampling GaN, could you maybe elaborate a little bit more, help us understand a little bit more the positioning there? Is this vertical GaN? Is it horizontal GaN? Is it your own process? Any more color you can help us there? And when do you expect to start to see some 800-volt GaN revenue?

**Michael R. Hsing** (Executives):
Yes. We let -- it is based on MPS own development, which is later than we developed silicon carbide device. And we start to sampling that this type of solutions. We let our customers choose in either using GaN, the GaN is a new technology for everyone, okay? And for everyone adopting it in the data centers and the industrial automotive type of applications, okay? This is the first time. 
And we are always very cautious about the reliability. We want to achieve below 1 ppm failures and for these modules. And we let our customers choose, okay? GaN or silicon carbide. Silicon carbide is known, we know the data. And so that's a very high reliability product and GaNs we have to ship somewhere 50 million units before we can say this is a good -- this is a new one for GaN, but we let our customers choose.

**Tony Balow** (Executives):
Yes. I'll just add on it, I think all of the experience -- I was just going to add a few things there. This is just the experience we've already gained in data center, I think, puts us in a really good position to do what Michael is talking about in terms of making sure we can meet all the standards that customer requires. 
You asked a question on the timing of it. I think right now, we're still -- we've always kind of been late in '27 for I think kind of the 800-volt kind of architecture ramps with probably more in '28. I don't think our thinking on that has changed. We're just obviously getting ahead of that design work now.

**Michael R. Hsing** (Executives):
Even for our customers, they use both. They don't want to have a failure either. They use both solutions.

**Operator** (Operator):
Our next question comes from Rick Schafer with Oppenheimer & Co.

**Richard Schafer** (Analysts):
Congratulations to you guys and congratulations, Tony, on the appointment. If I could ask a question on storage and compute for my first one, I was hoping maybe you could level set us on some of the moving parts in there. I mean, how does that segment split now if you look at SSD, HDD, DDR5, PMIC versus the PC, the VCore power piece? Because I know we all see PC units tracking down about 20% here in the second half. So I'm just curious, is that kind of what you guys are seeing on the PC side of that segment? And then how much is the storage piece growing? And what's it contributing?

**Tony Balow** (Executives):
Yes, Rick, let me start, and then I'll let Michael come in. I think just kind of mechanically, if you look at it, the big driver of growth in that segment has been the DDR5, primarily on the PMIC solution. As we said, we're just starting the high-speed journey on the DDR5. We have seen pretty healthy growth over the past year or so on the hard disk drive and SSD part of that storage business as well. But clearly, DDR5 is the biggest portion of that. 
On notebook, sort of tactically, yes, I think we're -- we've been talking about this, and that's what we're seeing as well, right? We're seeing not the same strength on notebook due to what's happening downstream with some of the memory constraints. But I think, if you look forward, I think we're still pretty bullish on notebook in the long term because we have really good technology and good share -- and then I think there's applications around AI that will continue to build out over time at the edge, of which notebook will play a part. So I think what you're seeing in the short term around notebook tracks with what you're seeing, Rick. But I think long term, I think we're still pretty high on what notebook could be for the company.

**Michael R. Hsing** (Executives):
Yes. For that segment, we have a new products like a clock drivers and RCD. These all lined up and other than in addition to our power management product. These will be lined up for revenue in 2027 or '28. And we see even '28, these products will really ramping up, okay? So that's part of a TAM is much bigger than power management. 
And the notebooks, as Tony mentioned it, we will see this as a very fast growing market segments because after the manufacturing capacity opens up, that the segment will grow along with the desktop.

**Tony Balow** (Executives):
If you sum that up a little bit, what we said for kind of the segment overall is with the puts and takes, it could be kind of flattish, up a couple of points year-over-year is kind of how we positioned it, but it's really a tale of 2 cities, as we've talked about with really strong storage and then the TAM just being limited on the notebook side.

**Richard Schafer** (Analysts):
Got it. And then if I could -- this is your first call with the CFO moniker. And I'm curious how you look at OpEx growth going forward? I mean, any meaningful changes to the prior targets that you guys have laid out? I mean, at these type of top line growth rates that Tore called out, 50%, 60% type top line, how fast can you actually scale R&D, et cetera? It seems like we're -- it seems like you guys are set for some pretty material operating leverage to be flowing through the model. Is that the right way to be thinking about it? Any rules of thumb in there?

**Michael R. Hsing** (Executives):
Let me answer that part of the question, Rick. I never believe the big dollars R&D equivalent to a bigger result. It's -- for our business, it's inversely proportional to that. We just need some good ideas, good people that we're going to make everything happen.

**Tony Balow** (Executives):
So yes, I think, Rick, you're not going to see us necessarily change our model. What we've seen pragmatically, though, as we start to get to higher levels of growth that we start to fall below our model range in terms of we just can't spend money that fast. But I completely can agree with Michael on that. It's about the efficiency of the R&D and the people that you get versus just spending more. But in general, I'd say at the growth rates that we've seen, for example, this year, you're going to fall below the model from an OpEx perspective.

**Operator** (Operator):
Our next question comes from Quinn Bolton with Needham & Company.

**Quinn Bolton** (Analysts):
I'll echo my congratulations and Tony, congratulations on the new role. I guess I want to start with the enterprise data. Last quarter, you gave us a floor of 130%. With September results and December guidance, it kind of looks like you're tracking to maybe 150% growth. But wondering, Tony, if you might be able to level set us what a new floor growth for enterprise data might be? And then I know it's early, but any sort of thoughts on that segment as you look into 2027, what kind of growth rate you might be looking at in the forward case? And then I've got a follow-on in the comms business.

**Tony Balow** (Executives):
Sure. Let me start just kind of with the -- to answer your question, straight. I think at this point, given what we've seen in Q3 and Q4, we're comfortable raising the floor from -- we were at 130% year-over-year. But to your point, I think we're comfortable with a floor of 150% year-over-year now going forward. 
On 2027, I think it's a little early for us to go put a percentage out at this time, but I'll start and Michael, I'm sure, will follow up in that. Structurally, the growth drivers that we're seeing this year are all intact, right, whether you see the diversification of customers, the growth in modules, the content gains as new platforms roll out. And I think over time, as you start to see even stronger growth in GPU potentially driven by the Agentic AI workloads, that's going to be even a further tailwind out in time. So while a little early to call next year, I feel really good about the growth drivers.

**Michael R. Hsing** (Executives):
Well, I see in the next years and beyond next years, and I'm very excited to see that we build our own data centers. And as Tony mentioned earlier, the result is a tremendous improvement. And so this is not in the data centers, but in MPS own servers. And all these server, we believe -- I believe it will change and change to a  a GaN type of servers, and again the hardware will change and that will trickle down to desktops and even the notebook I said earlier. 
And this type of growth, it will trickle down in the next year and the year after. We see those trends, these design activities is really happening. And so this is not only this year, not only in the data centers, it will trickle down to all other areas.

**Tony Balow** (Executives):
Do you have a follow-up on comms?

**Quinn Bolton** (Analysts):
Yes. It's obviously congrats on the nice growth. I think it was 43% sequentially. It really looks like it was a breakout quarter in September. Wondering if that was primarily driven by optical modules? Or are you seeing a broader set of contributors to that growth? And just any thoughts into the December quarter? Does that sort of pace of growth continue into December?

**Tony Balow** (Executives):
It's a great question. And to take us back here, obviously, coming into the year, we obviously had very strong growth in optical modules. And what we added beginning of the year is what we've been calling the switch business. And I know I've talked about this before. But to answer your question, why are you starting to see the accelerated growth in that particular end market is because you are adding both of those growth drivers together, and we saw the effect really in Q3. 
And I think for the year, we've been positioning it is it's -- I think comms is going to be our second fastest-growing end market for sure. It won't be quite as fast as enterprise data, but certainly won't be far behind. And just like enterprise data, I think if you go into next year, all of those growth drivers are intact. On optical modules, you see the transition to 1.6. That's not just a volume play, but there's a content play there as well. 
And then certainly, as we continue to build out additional sockets in the switch business, that's going to be a driver of growth as well. So I think right now, we really like the comms business, not just this year, but going into next year.

**Michael R. Hsing** (Executives):
And on the macro economy and market segment predictions, I only care what is the design activity and what our customers are excited about it, what we're excited about it, all these new technology, new product introductions. And as I said earlier to [ market ], all these segments, we introduced the new product and all the design activities that give us an indication clearly the growth for even beyond next year.

**Operator** (Operator):
Our next question comes from Joshua Buchalter with TD Cowen.

**Joshua Buchalter** (Analysts):
Congrats on the results and echoing the congrats to Tony on the CFO gig. Best of luck. I'll stick with policy and ask one on enterprise data and then one on another segment. Maybe can you comment on the diversity of enterprise data? Like how has that business evolved over the last year or 2 and looking into 2027? I would just be curious to hear how much you see coming from GPUs versus ASICs or even any comments you can help us on how much is coming from modules versus discrete at this point and expectations into '27?

**Michael R. Hsing** (Executives):
Yes. Modules versus the chip design, chip power supplies, and then ICs on the chip all of them, okay? I mean even for the server side, and okay, we see some -- many activities and going through using modules because of the high current high-power demand. That's my comment, okay? And it's all segments -- from growth -- the real growth percentage, I'll let Tony to...

**Tony Balow** (Executives):
Yes, I think -- and that -- I think it's an important point around this customer diversity that starting in the middle of 2025 until now, what we've seen is a really rapid growth in a lot of ASIC customers, which again are primarily using modules over time. And so that's benefited from a revenue diversity perspective as those carry the higher ASP associated with that. 
I think furthermore, what Michael was talking about in terms of how we've been using AI to create scale to allow us to go address even a longer tail of small customers over time, which may be big customers in the future. And that's really what we try to do, go in every socket, not knowing who ultimately in the long term might grow into a sizable customer.

**Michael R. Hsing** (Executives):
Yes. All we clearly see is that we have the huge beneficial from these artificial environment, these artificial intelligence based on these large language model. Of course, MPS [indiscernible] is internal. And it benefit us, it will benefit for everybody. And that's where I'm very optimistic about this and our growth trend will continue.

**Joshua Buchalter** (Analysts):
Maybe in the same theme of starting with small sockets that become big opportunities. Any context you can provide on how much revenue contribution we can expect from the initial high-speed data converter design win? And how big is that TAM as we think about you growing into this new market?

**Michael R. Hsing** (Executives):
Yes. This is -- we can't tell because we have -- we just counted, these are over -- conservatively well over 6,000 products, okay? And we continue to develop newer products. So what we do is we do every segment in our best, far better than -- or to meet the new market demand. And we are much faster than any of our competitors. 
And as long as we do, the segments do the best and the revenue will come. And we don't -- we just don't know what -- which segment. 7, probably 8 years ago, we look at our product lines, look at the optical market segment, one of the perfect example. We didn't know today was that high demand. And we got it in there. We serve our customers regardless of the large or small. And that's what happened today. I cannot predict next 10 years, next 5 years, we will be bigger, and we serve our small customers well.

**Tony Balow** (Executives):
Yes. I think -- and again, to Michael's point, we're not ready to call the long term. We're just beginning that process. So I wouldn't necessarily say it moves the needle here in 2026. And I think as we get into next year, we'll talk more and see how that ramp goes.

**Operator** (Operator):
Our next question comes from Will Stein with Truist Securities.

**William Stein** (Analysts):
First, on data center vertical power. I think there's still one meaningful customer doing lateral and I'm wondering if you can comment as to whether you think that converts to vertical in the coming year and whether that would necessarily require a module from you instead of some other sort of solution.

**Michael R. Hsing** (Executives):
Certainly, okay, I don't want to speak for our customers, in particular that one customer. But I said earlier, and you know that what we did in the -- we predicted in the 2016 -- and for the server market, MPS solution is so small, and we have to use the adapter to meet the common footprint. And so when -- for the server market segment, we predicted and if you go above 600, 700 watts and you run out of peripheral and you have to use a smaller footprint. 
But the server GPU never get that never get to the 600, 700 watts, but the GPU did it, okay? And as GPU power increase, I don't have a generalized numbers, okay? It will -- the power goes up, you run out of peripheral, you have to do vertical. And we said this many years earlier, okay? I still believe that very logical to me.

**Tony Balow** (Executives):
Yes. I mean I'm just going to echo Michael. I think that we won't speak for that. Most of the industry has already moved to modules, right? And that's what we've seen in terms of content gains as well as the volume gains as we've gone through enterprise data. And I think that will be a great question for our customers. Yes, take a last jump [indiscernible].

**William Stein** (Analysts):
Great. And a different topic. Someone asked about the OpEx leverage. And I guess I understand that for the time being, with the rapid growth, you're going to sort of undershoot on spending, overshoot on margins. What about gross margin? I think the company has talked for a long time about 10 to 20 bps per quarter gross margin expansion. There was a time when you weren't in that range, and it seems like you are today. Any likelihood that because of the growth, you could exceed that expansion rate? Or should we still think about 10 bps to 20 bps is likely? Or any update there would be helpful.

**Tony Balow** (Executives):
No. And thanks for calling out. Yes, you saw that we obviously did increase 10 basis points here in Q3. The midpoint of our guide in Q4 is kind of another 10 basis points. So I think we're kind of squarely in the model that we like, right? 55% to 60% is the sweet spot for sure. And within that being kind of slow, methodical about expansion. I think we're going to continue on that path. 
Structurally, I feel pretty good about that. We'll see what happens in the future. But remember, what we don't want to do ever is put a bunch of gross margin in one quarter and then take it away the next quarter and move it around a bunch...

**Michael R. Hsing** (Executives):
During the capacity constraint, we don't gouge our customers. And so we want to deliver to you guys a very consistent story. And I don't want to answer a question when the margins drops? And I want our MPS to keep it same business, same performance year-over-year -- quarter-over-quarter, year-over-year.

**Tony Balow** (Executives):
That's right. So I think the model still holds. I'm very comfortable with that. And I think you called it out, but I'll highlight it again. I think if you look at the flow-through to operating margin, we've been growing operating margin, it's kind of a point a quarter almost. So we've seen a lot of expansion on the operating margin line.

**Michael R. Hsing** (Executives):
We are in a making money business. And that's all I would point here.

**Operator** (Operator):
Next question comes from Chris Caso with Wolfe Research.

**Christopher Caso** (Analysts):
Just following from the prior discussion, maybe you could talk about how you're dealing with rising costs. And obviously, costs are going up a lot of different places. There's a lot of talk of foundry wafer prices going higher. So to what extent are you passing that along? And as you go forward, does any of that result in pricing or any kind of revenue tailwind as you have to absorb some of those costs and pass them along to customers?

**Michael R. Hsing** (Executives):
We definitely absorb some of the cost increase. And not that we don't increase the price, okay? And we some -- we share the cost with -- the cost increase with our customers.

**Tony Balow** (Executives):
Yes, I think that's right, Chris. And I think if what you're asking is from some of the results, how much of that is from pricing, it's really not a significant contributor to the revenue growth that we've had. We are more just making sure that we don't dilute ourselves on the gross margin line.

**Michael R. Hsing** (Executives):
Yes. Our customers have a very long memory.

**Christopher Caso** (Analysts):
Right. Okay. As a follow-up, it's a question on the 800-volt transition. And I know there's a lot of noise out there with regard to the pace of that transition. What -- in terms of MPS, how important is that to you in '27? And I guess maybe the question is, is it really 800 volts a very material driver of content in the EV segment? Or is the majority of that still going to wind up in the existing low power -- I'm sorry, low-voltage designs?

**Michael R. Hsing** (Executives):
Yes, we don't want to add more voices, okay? We don't talk about it until the revenue for sure will come, okay? I do see the revenue for sure will come. Not this quarter, not next quarter, probably end of the '27 and 2028. And it's clearly the DC supply for high power demand and will be the trend, will be the data center, all will convert it to that. And the power savings is, I think, beyond like single digit -- single-digit percentage improvement versus the traditional power supply. 
I see this is even beyond the data center. And if the data center can improve, let's say, 5%, where do you get the 5% money returns? And all the commercial building, even residential, they all can be like this, 400 volt these are in -- there will be -- in Europe will be 800 volts in U.S. will be 400 volts. And that these will be a significant power savings across the board. That's what I'm excited about this opportunity now.

**Tony Balow** (Executives):
Yes. I mean I'll even try to just address the question the other way, which is when we talked about our -- how we are excited about growth in enterprise data, it's not because we're -- we have a big built-in ramp on 800 volt. It's really around the existing customers, the new customers, transition to modules, all the things that we've been talking about, Chris. So if you're kind of trying to figure out how much of that excitement was just at 800 volt, I really think the business we have today is what we're confident in.

**Michael R. Hsing** (Executives):
Yes. MPS now we're using our own building do a lot experiment, using these 800 volts and using the technology and see what the power saving is.

**Operator** (Operator):
Our next question comes from Sebastien Naji with William Blair.

**Sebastien Cyrus Naji** (Analysts):
Congratulations, Tony, on your appointment. I wanted to maybe just ask my first question, given some of the news around integrated voltage regulators and the acquisition of Empower by Analog Devices, maybe could you just give us your view on this technology and whether you see it as a competitive risk in the AI data center or the larger data center?

**Michael R. Hsing** (Executives):
Yes, we don't comment on other companies' activities. And we have our own solutions. We have our own and we can deliver whatever customer wanted. And this is not BS talks, we do have multiple beyond what you guys beyond the noise levels. And we have those technologies and we can deliver. And the GPU evolves very quickly, the power levels, the architecture and in terms of the power delivery. And we don't talk about those until we have -- we see -- clearly see where the revenue will come.

**Sebastien Cyrus Naji** (Analysts):
Okay. Okay. Great. That's helpful. We'll look forward to those announcements when those products are ready. Maybe moving to something that's a little bit closer to your heart, Michael, which is the building automation opportunity. I think last quarter, you talked about $40 billion to $50 billion in size, but that the real bottleneck was the software still needed to catch up. Can you maybe just talk a little bit about the progress that's been made here as we get to the end of the year?

**Michael R. Hsing** (Executives):
Well, good questions, okay? That's my baby project. And we just have installed in our 1 million square feet building. That's in China. And we -- as I said just a minute ago, we're experimenting our own AC to DC power. These are for 800-volt supply. And for across the building, -- and that project -- these projects just started. But in terms of turning to a $50 billion revenue will take some time. We don't know how to get there yet, but the goal is very clear. 
And we will get there. There's a lot of software involved in it, okay? But on the hardware side, we pretty much have every single component. And our single -- our components, our chips, our module technology is far better than -- sorry to say these are the current existing technology. These are 50-year old, and we will do some significant improvement on it.

**Operator** (Operator):
Our next question comes from Kelsey Chia with Citi.

**Wei Chia** (Analysts):
Congrats on the great results again. And Tony, congrats on your well-deserved appointment. So my question is on the switching business. So to what extent is that contributing to the strong communications growth that we saw in third quarter? And how should we think about the ramp as we head into 2027 and if that business is accretive to gross margins?

**Tony Balow** (Executives):
Yes, I'll start on that one. So we're obviously not going to start guiding sub end markets a little bit. But certainly, from just a percentage basis, it's been growing very quickly, probably on a percentage basis, the fastest-growing sub end market inside of communications just because it started from a very low amount at the beginning of the year. As we go forward, again, I still think that and optical modules are going to be significant growth drivers for communications into 2027. 
On the margin side, I think if you look at all of our end markets, plus or minus, they'll all operate around the corporate average because to Michael's point, we have north of 6,000, 7,000 products. And so if you look at the distribution of that, basically, what we said is as we grow this, we don't think growing one end market over another will necessarily take us out of our model. And so right now, I would still take MPS as a total kind of in that 55% to 60% range with sort of the slow methodical expansion when we can provide it versus worrying about whether growth in one end market would take you out of model.

**Wei Chia** (Analysts):
And my second question is on the industrial end market. I mean, very strong growth this quarter as well. What drove that strong growth this quarter? And if you could talk about the ramp of the robotic solutions? And how do you see that ramping in '27?

**Michael R. Hsing** (Executives):
The robotics, we -- I tried to enter the robotics in 2016. On the Analyst Day, we talked about robotics, that's the area we're focused on. We have a product for these sensors and motor controls -- and I didn't know what I was talking about, the revenue didn't come, okay? And now it shows up. 
And I think this is still at the very beginning, once the vision for the recognition and visual recognition and improved from using the AI-based vision improvement technology. These robots, as you know, they will propagate in everyday life. So I see this -- that's the future. And the revenue would be significantly higher than that.

**Tony Balow** (Executives):
Yes. I think the only thing I'd add kind of on the overall segment is, I think this year, we still look at it as just piling up design wins in robotics and other places and really look for more of that in 2027. The growth in the quarter was fairly broad-based, but I think you start to see a lot of these other design wins come to turn into revenue in the future. So I think that in kind of consumer and industrial, 2026, I think, really does still remain mostly about winning all the designs that support future growth.

**Operator** (Operator):
Our next question comes from Joe Quatrochi with Wells Fargo.

**Joseph Quatrochi** (Analysts):
My congrats as well, Tony. Maybe just kind of a finer point on the expansion of capacity to $8 billion. I can appreciate that you can't grow OpEx as fast and you don't need to grow as fast. But how do we think about like maybe some of the investments you have to make on the working capital side or go-to-market side to support that?

**Tony Balow** (Executives):
Yes. I think on -- one of the nice things about being in a fabless model, right, is we don't have to dig a hole and pour concrete into it.

**Michael R. Hsing** (Executives):
We don't make it and it will wake our brain generally.

**Tony Balow** (Executives):
That's right. So we -- I don't anticipate at this point seeing a large increase in capital intensity just to go ramp this capacity, right? So it gives us a lot of flexibility. As a matter of fact, I am personally just amazed at the amount of capacity we've been able to put on just even over the last year. 
And I think the operations team has done a tremendous job. But I don't see it necessarily reflecting the overall OpEx at this point or any kind of change to our capital structure just to put on that extra capacity.

**Joseph Quatrochi** (Analysts):
Okay. And then maybe as a follow-up, I think auto is continuing to see some inflection. Can you just talk about the breadth of demand you're seeing there from a geographic perspective and how we think about like the design pipeline looking into '27?

**Michael R. Hsing** (Executives):
It's of course, geographic in U.S. side, Europe side and also in Asia, China. We see -- in China, particularly, we see a lot of activities. And so that's probably the world. And we -- as we said -- as I said earlier, we can't predict which market segment. And that's our diversified growth strategy. 
And some years, one segment is good, even with a mature market and some years, one market segment is good and the other one is not so good, okay? And in the last few years, all of a sudden, the GPU market happened or the optical market and the revenue happened. And so we didn't anticipate it. We just provide the best highest performance product. Our customers will realize it.

**Tony Balow** (Executives):
Yes. The only thing I'd add is I think the reason we've been pretty confident on the ramp in the second half is because it is so diverse amongst customers and regions and not dependent just on one. You've seen that same level of customer diversity grow in auto over the past several years, like we've been talking about in enterprise data. And the pipeline is similar, right? It's very geographically diverse and very customer diverse. We were just very excited to start seeing some of the architectural transitions that we've been talking about in sort of 48-volt and zonal because those sort of form the next wave of growth for us.

**Michael R. Hsing** (Executives):
We're not predicting what the market is.

**Operator** (Operator):
Our last question comes from Gary Mobley with StoneX.

**Gary Mobley** (Analysts):
Congrats Tony, again. I wanted to ask about what you might be signaling in your capacity milestones. You're currently at $6 billion in production capacity, which I assume supports your 2027 outlook. It doesn't take much to get there, just extrapolating out Q4 revenue guidance. And you're expected to be at $8 billion in capacity exiting fiscal year '27. So should we think about that in terms of the revenue velocity exiting fiscal year '27?

**Michael R. Hsing** (Executives):
It doesn't take much to get there, oh, come on, this is the market that move the numbers. There's a lot of work behind it.

**Tony Balow** (Executives):
Yes. I'll add, so right now, I think what we're trying to strongly signal is that just like we've been doing in the past 20 years, we're making sure that capacity stays ahead of the business. And in a world where there's a lot of narrative around there being tightness, we wanted to be very clear to you and our customers how we're growing capacity to support that business. 
So I think, again, it's too early to go right into a quarterly revenue ramp and what that means for 2027. But we wanted to make sure it was loud and clear was that we see the demand coming, and we're going to make sure capacity is there to deal with it.

**Gary Mobley** (Analysts):
And on inventory, I just want to confirm that the distribution inventory is still within that normal 5- to 8-week range. And then it looks like your internal inventory is down to 117 days based on a forward revenue guide basis, and that's been trickling down. Are you inventoried properly to support sales, I guess, is really the question.

**Tony Balow** (Executives):
I think right now, we're still on the channel side, certainly in the lean end of our range like we've been for some time now. And internally, I think we grew dollars on a gross basis, right? But obviously, as the revenues ramp, that's come down from a days perspective. So I think that our range certainly hasn't changed, and it's something that as we increase our capacity and our wafer starts, we'll make sure that we're positioned for the business. But right now, it's not limiting us on the business.

**Operator** (Operator):
This concludes the question-and-answer session. I would now like to turn it back to Tony Balow for closing remarks.

**Tony Balow** (Executives):
All right. Thank you, operator, and thank you all for joining us for this conference call today. I look forward to speaking with you on the next call for the fourth quarter and full year '26 revenue guidance. Thank you again, and have a great day.

**Operator** (Operator):
This concludes today's conference call. Thank you for participating. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MPWR_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Tony Balow｜guidance：Enterprise Data 全年下限由 85% 上調至 130%（管理層用語 raise the floor）（原話："willing to raise the floor for that particular end market"）
- 2026-07-30｜Tony Balow｜guidance：Q2 營收創單季新高 $981M（原話："record quarterly revenue of $981 million"）
- 2026-07-30｜Tony Balow｜guidance：Enterprise Data 單季成長 45%（原話："with Enterprise Data growing 45%"）
- 2026-07-30｜Tony Balow｜guidance：Auto 全年預期年增約中段十幾%（原話："could be in the mid-teens kind of year-over-year."）
- 2026-07-30｜Tony Balow｜guidance：Auto 上半年持平、下半年爬坡的說法延續（原話："we thought the first half would be flat"）
- 2026-07-30｜Tony Balow｜guidance：RCD 不會是 2026 年營收的關鍵（原話："that's not going to be a needle-mover in 2026 for"）
- 2026-07-30｜Robert Dean｜margin：Rob 稱強勁訂單讓毛利率指引小幅上調（原話："incrementally expand our guidance"）
- 2026-07-30｜Robert Dean｜margin：毛利率仍在目標區間低端，但對 Q3 有信心（原話："but we're feeling comfortable about where we're at for Q3."）
- 2026-07-30｜Michael R. Hsing｜margin：Hsing 稱毛利率仍在模型內但在低端（原話："we're still in the model, although in the low end"）
- 2026-07-30｜Michael R. Hsing｜margin：Hsing 稱近期毛利率大致持平或略高（原話："in the near future, we'll probably stay similar or"）
- 2026-07-30｜Tony Balow｜margin：Tony 說明營收提高後費用難以同步擴張，帶來營業利益率槓桿（原話："difficult to keep the levels of spending up to that model"）
- 2026-07-30｜Tony Balow｜margin：Tony 說明漲價的三類情境之一，與維持毛利有關（原話："We have raised some prices, but it's primarily"）
- 2026-07-30｜Michael R. Hsing｜margin：Hsing 否認本季成長來自漲價（原話："gouges prices when the supply chain is tight."）
- 2026-07-30｜Tony Balow｜commitment：宣布增加 $500M 庫藏股授權，總額 $1B（原話："additional $500 million for stock repurchases"）
- 2026-07-30｜Tony Balow｜commitment：產能目標擴大至遠超 $6B（原話："extended our capacity goals significantly beyond $6 billion"）
- 2026-07-30｜Michael R. Hsing｜commitment：Hsing 稱提到的新事業歷來都會變成營收（原話："when we mention something, it will turn into a revenue."）
- 2026-07-30｜Michael R. Hsing｜commitment：Hsing 稱 RCD 有信心轉成營收（原話："we're confident that it will be turning to a revenue"）
- 2026-07-30｜Michael R. Hsing｜commitment：Hsing 稱建築控制軟體預計今年底前完成（原話："we should be able to complete it, complete everything"）
- 2026-07-30｜Michael R. Hsing｜commitment：Hsing 稱持續追求穩定成長（原話："investors a very consistent way of growing MPS."）
- 2026-07-30｜Tony Balow｜product：DDR5 記憶體元件取得初期訂單，預期擴大 SAM（原話："which we expect to grow our SAM into next year."）
- 2026-07-30｜Tony Balow｜product：DDR5 營收爬坡時點管理層不給（原話："early for us to call any kind of revenue ramp on our side."）
- 2026-07-30｜Tony Balow｜product：開始送樣 800V 資料中心高壓 AC-DC 產品（原話："We began sampling high-voltage AC to DC products"）
- 2026-07-30｜Michael R. Hsing｜product：800V 方案營收時點管理層不給（原話："when, we don't know -- we know as much as you know."）
- 2026-07-30｜Michael R. Hsing｜product：Hsing 承認先前不看好 GaN，現已自研（原話："I openly say I don't believe GaN"）
- 2026-07-30｜Michael R. Hsing｜product：48V 垂直電源模組客戶超過兩家（原話："Well, it's more than a couple of customers."）
- 2026-07-30｜Tony Balow｜product：Tony 說明 Comms 成長來自光模組與交換器兩塊，光模組較大（原話："the bigger portion just because it's had a longer runway"）
- 2026-07-30｜Michael R. Hsing｜product：建築自動化軟體尚落後（原話："we're still lagging of the software."）
- 2026-07-30｜Michael R. Hsing｜product：Hsing 稱建築自動化市場規模 $40–50B（原話："it's about $40 billion to $50 billion."）
- 2026-07-30｜Tony Balow｜product：Tony 稱模組後段製程更複雜（原話："a more complicated back-end process as well."）
- 2026-07-30｜Tony Balow｜customer：Auto 今年已出貨超過 1,500 個新 socket（原話："we have shipped products for over 1,500 new sockets"）
- 2026-07-30｜Tony Balow｜customer：Enterprise Data 通路庫存仍很低（原話："that remains very low, so we believe that's continuing"）
- 2026-07-30｜Tony Balow｜customer：book-to-bill 本輪週期明顯大於 1（原話："cycle was again well above 1."）
- 2026-07-30｜Tony Balow｜customer：2027 年數字管理層不給（原話："it's too early to put a number on it."）
- 2026-07-30｜Michael R. Hsing｜customer：Hsing 稱不把貨硬塞給客戶，雖有 NCNR（原話："even though we have NCNR"）
- 2026-07-30｜Michael R. Hsing｜customer：Hsing 稱 CPU 市占已超過自設 30% 門檻（原話："we're comfortable there now. We're past that."）
- 2026-07-30｜Tony Balow｜customer：Tony 稱難以區分純 AI 與 CPU 銷售（原話："separate sometimes a pure AI sale from a CPU sale"）
- 2026-07-30｜Tony Balow｜customer：Tony 稱 ED 以外業務去年 Q2 雙位數成長（原話："the rest of the businesses saw double-digit"）
- 2026-07-30｜Tony Balow｜customer：Tony 稱資料中心相關曝險未細分儲存與筆電（原話："we haven't broken out Storage and Compute versus notebook"）
- 2026-07-30｜Michael R. Hsing｜competition：Hsing 稱功率密度全球最高（原話："we're the highest power density company in the world now"）
- 2026-07-30｜Tony Balow｜competition：Tony 稱光模組市占不給確切數字（原話："quote the exact percentage of share at this time."）
- 2026-07-30｜Tony Balow｜competition：Tony 稱 Comms 仍有成長空間（原話："there's still room for us to grow."）
- 2026-07-30｜Michael R. Hsing｜risk：Industrial 偏弱（原話："Industrial is kind of lagging a little bit"）
- 2026-07-30｜Tony Balow｜risk：Tony 對 Consumer 與筆電端儲存/運算持謹慎（原話："Compute, we'll continue to remain cautious on that one"）
- 2026-07-30｜Tony Balow｜risk：Industrial 今年定位為設計導入年（原話："we've primarily said that's a design win"）
- 2026-07-30｜Michael R. Hsing｜capital_allocation：新增產能多在既有節點（原話："I think it's mostly the existing."）
- 2026-07-30｜Michael R. Hsing｜capital_allocation：產能地理分布比重尚難估計（原話："what is the percentage in the end, it's hard."）
- 2026-07-30｜Tony Balow｜capital_allocation：持續擴充並分散全球供應鏈（原話："continuously expand and diversify our global supply chain"）

### MPWR_Shareholder_Analyst_Call_Monolithic_Power_Systems_Inc_20260611.md
- 2026-06-11｜Saria Tseng｜commitment：股東會議程：提名兩位董事（Victor Lee、Jeff Zhou）任期至 2029 年股東會（純程序性陳述，非財務承諾）（原話："nominated by the Board of Directors, Victor Lee"）
- 2026-06-11｜Saria Tseng｜commitment：兩位董事獲連任（原話："Both directors are reelected."）
- 2026-06-11｜Saria Tseng｜risk：董事會指派 Ernst & Young 審計 2026 會計年度財報，交付股東追認（治理程序）（原話："appointed Ernst & Young independent auditors to audit"）
- 2026-06-11｜Saria Tseng｜risk：會計師追認案獲 4,540 萬股贊成（原話："45.4
million shares were in favor of the appointment."）
- 2026-06-11｜Saria Tseng｜risk：薪酬諮詢投票（say-on-pay）通過，4,220 萬股贊成（出席 4,540 萬股）（原話："The executive compensation is approved."）
- 2026-06-11｜Saria Tseng｜risk：Jeff Zhou 獲 4,110 萬股贊成（同場 Victor Lee 為 3,930 萬股）（原話："41.1 million shares were in favor of the appointment"）
- 2026-06-11｜Saria Tseng｜risk：出席股數 4,540 萬股，占記錄日流通股 92%（原話："comprising
92% of the outstanding common stock"）
- 2026-06-11｜Unknown Executive｜risk：開放提問時無人提問（原話："Saria, there's no question."）

### 問答異常語氣（迴避／改口／保留）
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Buchalter 問 ED 有無庫存堆積與可見度｜答法：Hsing 先談過去工業缺貨，未直接回答庫存；Tony 補上通路庫存低與上調下限
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Buchalter 問 DDR5 控制器 SAM 擴大幅度｜答法：Tony 稱太早、不給營收爬坡數字
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Svanberg 問 800V 營收時點｜答法：Hsing 稱不知道，由資料中心轉換時點決定
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Bolton 問光模組市占與競爭對手｜答法：Hsing 改談功率密度；Tony 不給市占百分比
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Bolton 問新增產能中國與非中國比重｜答法：Hsing 稱尚未定、難估；Tony 改談後段製程
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Chia 問 ED 2027 展望｜答法：Tony 稱 2027 太遠不給數字；Hsing 補述不推貨給客戶

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
{"date":"20260731","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"企業數據段的成長是「分散客戶 × 內容價值躍升」的結構性成長，不是單一 socket 押注"},{"id":"H2","text":"模組化（chip → semiconductor-based solution）提升每個 socket 的內容價值，且不以毛利率為代價"},{"id":"H3","text":"市場願意為「EPS 從 $27.51 複利到 $68」付出 30x 以上的終端倍數，倍數壓縮幅度不超過 47.4x → 32x"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"旗艦 AI 插槽二度失守：繼 Blackwell B200／GB200 主要配額落入 Infineon（60–70%）與 Renesas 之後，Vera Rubin（VR200）再度失守。"},{"id":"R2","text":"AI capex 消化期：企業數據段 +164% 的年增基期在 2027 變成高基期，若 hyperscaler capex 增速由 +100% 降到 +20%，本段成長可能一次掉到個位數，且 TAM 遮羞布撤走後暴露真實份額。"},{"id":"R3","text":"定價權自願放棄的長期代價：管理層政策性不趁緊俏漲價，加上模組化把電感、電容等外購料帶進成本結構，毛利率由 58.4%（2022）走到 55.2%（2025），若續探則「高毛利無晶圓廠類比 IC」的估值框架不再適用。"},{"id":"R4","text":"同業溢價收斂：本檔 Fwd PE 47.4x 相對同 tier 中位 25.6x 溢價 +85%，遠超 50% 門檻。若對手（TXN／ADI）在 AI 電源上補上、或本檔成長率向同業靠攏，溢價收斂本身即可造成 −23% 的價格衝擊（§11.4 情境 B），與基本面惡化無關。疊加 headline 脆弱性：本檔對「NVIDIA 插槽份額」類新聞極度敏感，過去一年曾因單一 sell-side 份額傳言單日重挫近 9–10%，re-rate 可在無財報的情況下被消息面逆轉。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已建 starter 1/2；加碼觸發＝Rubin VR200 插槽定案，或企業數據單季 YoY ≥+80% 連兩季","irr_base_pct":9.2,"ev5y_pct":54.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.3,"ev5y_pct":54.7,"irr_base_pct":9.2,"max_dd_pct":-60.0,"bull_5y_price":3458.0,"bear_5y_price":889.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"已建 starter 1/2；加碼觸發＝Rubin VR200 插槽定案，或企業數據單季 YoY ≥+80% 連兩季","price_at_dd":1450.0,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MPWR_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
