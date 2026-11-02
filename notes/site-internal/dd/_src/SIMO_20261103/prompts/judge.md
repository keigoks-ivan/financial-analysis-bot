你是 stock-analyst **v20 判斷 agent**，標的 SIMO（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SIMO","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":560.2,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益","value":180.0,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益率","value":32.1,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":162.6,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":29.0,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi5_non_gaap","label":"Non-GAAP 毛利率","value":53.7,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi9","label":"期末現金（含受限）","value":953.6,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi10_q4_2026","label":"Q4 2026 營收指引","value":"588–616","period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi11","label":"全年指引（定性）","value":"2026 營收創新高、年增 >100%","period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_simo_gross_margin_pct","label":"SIMO 毛利率","value":50.54,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIMO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_simo_operating_margin_pct","label":"SIMO 營業利益率","value":21.3,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIMO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_simo_fcf_margin_pct","label":"SIMO FCF 利潤率","value":-24.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIMO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_8299_two_gross_margin_pct","label":"8299.TWO 毛利率","value":56.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8299.TWO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_8299_two_operating_margin_pct","label":"8299.TWO 營業利益率","value":30.89,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8299.TWO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_8299_two_fcf_margin_pct","label":"8299.TWO FCF 利潤率","value":-8.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8299.TWO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mrvl_gross_margin_pct","label":"MRVL 毛利率","value":52.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_operating_margin_pct","label":"MRVL 營業利益率","value":16.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_fcf_margin_pct","label":"MRVL FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_sndk_gross_margin_pct","label":"SNDK 毛利率","value":76.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_sndk_operating_margin_pct","label":"SNDK 營業利益率","value":68.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_sndk_fcf_margin_pct","label":"SNDK FCF 利潤率","value":61.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi6","label":"營業現金流","value":-256.1,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi7_ocf_capex_23_0","label":"自由現金流（OCF－capex 23.0，推算）","value":-279.1,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"},{"id":"f_kpi8_sbc","label":"SBC","value":17.3,"period":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）","citation":"公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm"},"note":"查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":196.49,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-13.15,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":38.07,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":19.72,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.36 → 13.6）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":20.45,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.28 → 19.61）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":12.3,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.24 → 22.73）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.6,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":19.61,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":22.73,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":56.14,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 8.71 → 13.6（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":21.13,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝36.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":36.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.08,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.25,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":14.45,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 13.6，分子＝快照價 196.49","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.018,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":280.58,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 1126.51、現金 845.93（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":33.91,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":6943.21,"period":"2026-11-03","unit":"USD m","basis":"市值 6662.63 ＋ 淨負債 280.58","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":1957.4,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":2746.91,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.55,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 189.82 / W52 192.76 / W104 128.6 / W250 90.31 / W250 13週斜率 2.1%"},{"id":"f_ma_w52","label":"52 週均線","value":192.76,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":128.6,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":90.31,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.1,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F FY2025 列出主要競爭者為 Microchip、Phison、客戶內部自研與中國小型控制器廠；稱中國競爭者受惠於政府半導體在地化政策，預期競爭加劇，並預期未來有新興或既有公司、客戶可能取得顯著份額","source":"SEC EDGAR 20-F FY2025 Item 4 Competition","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"We face competition from multiple competitors, including Microchip and Phison, our flash memory customers’ internal captive developments and small Chinese merchant controller suppliers.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F 風險因素：部分快閃記憶體客戶可能自行開發產品取代對公司產品的需求；中國競爭者受在地化政策受益","source":"SEC EDGAR 20-F FY2025 Item 4 Competition","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"our competitors in China have benefited from the government’s semiconductor localization policies.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q2 2026 法說：管理層稱持續取得份額、預期 2026 營收年增逾一倍，且企業級儲存暫未見 NAND 廠或模組廠顯著競爭","source":"Nasdaq: SIMO Q2 Earnings Call Highlights AI Storage Expansion","url":"https://www.nasdaq.com/articles/simo-q2-earnings-call-highlights-ai-storage-expansion","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q4 2025 法說：CEO 稱中國控制器廠難取得 TSMC 12nm 以下先進製程","source":"Motley Fool: Silicon Motion Q4 2025 earnings transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/04/21/silicon-motion-simo-q4-2025-earnings-transcript/","excerpt":"the Chinese controller vendors have really struggled to compete technically. So would you mind just talking a little bit about competitive dynamics, whether anything is changing in that market and some of the structural dynamics that might make it hard for the domestic Chinese players to compete? Chia-Chang Kou: I think the Chinese controller maker, they will have tough time to secure TSMC","as_of":"2026-04-21","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 法說：NAND 廠由整合方案轉向外部控制器夥伴","source":"Motley Fool: Silicon Motion Q1 2026 earnings transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/04/30/silicon-motion-simo-q1-2026-earnings-transcript/","excerpt":"Kou highlighted that UFS controller growth remains closely tied to handsets, but eMMC controllers are diversified across automotive, smart TV, IoT, and industrial applications, mitigating the impact of smartphone unit declines. MonTitan PCIe Gen5 and upcoming Gen6 controllers have already secured multiple Tier 1 design wins, including both NAND makers and cloud service providers, with","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"20-F 披露：所有主要 NAND 原廠都有內部自製（captive）控制器；若原廠擴大自製，merchant 市場可能縮小，過去 SIMO 營運結果曾因客戶自製而受負面影響。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"All the major NAND flash makers also have internal captive sources of controllers. The merchant market for controllers could shrink if the NAND flash makers were to expand their usage of captive sources of controllers. In the past, our operating results were negatively affected when NAND flash customers chose to insource controllers.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"20-F 披露客戶集中：前五大客戶占 2025 年營收約 66%，>10% 客戶合計 58%（PHISEMI、Kioxia、AFASTOR、Micron）；未點名單一最大客戶正在導入第二供應商。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"Sales to our five largest customers represented approximately 61%, 66% and 66% of our net revenue in 2023, 2024 and 2025, respectively. Our customers constituting more than 10% of our net revenue were (i) Micron, SK Hynix and AFASTOR in 2023, (ii) Micron, Kioxia, PHISEMI and AFASTOR in 2024 and (iii) PHISEMI, Kioxia, AFASTOR, and Micron in 2025.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 前五大客戶占營收約66%（2023:61%、2024:66%）；>10%客戶合計58%（四家：PHISEMI、Kioxia、AFASTOR、Micron）；前十大客戶82%。","source":"SEC EDGAR 20-F FY2025 Item 3 / 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"Sales to our five largest customers represented approximately 61%, 66% and 66% of our net revenue in 2023, 2024 and 2025, respectively. Sales to our customers constituting more than 10% of our net revenue represented, in the aggregate, 45%, 57% and 58% of our net revenue in 2023, 2024 and 2025, respectively.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"公司稱應收帳款信用集中風險受信用評估、短收款期及客戶高信用度緩解；前十大客戶占比 2023-2025 為75%、84%、82%。","source":"SEC EDGAR 20-F FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"The Company believes that the concentration of credit risk in its accounts receivable is substantially mitigated by the Company’s credit evaluation process, relatively short collection terms and the high level of credit worthiness of its customers.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未見SIMO主要客戶信用降評或財務惡化報導；Benzinga 稱 2026-07-29 給 Q3 2026 營收指引 $519M-$541M，較先前區間上調。","source":"Benzinga SIMO earnings forecasts（搜尋摘要）","url":"https://www.benzinga.com/quote/SIMO/earnings-forecasts","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 2026年7月更新：NAND 2026年供給缺口4–5%，供應商主要靠製程轉進增產（廠房空間受限、DRAM優先）；2027年供給成長超過需求，預期2H27緩解。","source":"TrendForce Press Center 2026-07-21","url":"https://www.trendforce.com/presscenter/news/20260721-13148.html","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SIMO管理層（Q2 2026法說）預期NAND供給吃緊持續，CEO稱稀缺可能延續至2028新廠投產；同時預期2026智慧型手機出貨衰退10–15%。","source":"Nasdaq: SIMO Q2 Earnings Call Highlights AI Storage Expansion","url":"https://www.nasdaq.com/articles/simo-q2-earnings-call-highlights-ai-storage-expansion","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Micron CEO：記憶體與儲存2027、2028年比2026年更緊，需求超過供給；約75%的2027年產出已被承諾。","source":"Northeast Times: Micron CEO says memory supply will stay tight through 2028","url":"https://northeasttimes.com/2026/10/02/micron-ceo-says-memory-supply-will-stay-tight-through-2028-keeping-prices-high/","excerpt":null,"as_of":"2026-10-02","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"分析師觀點分歧：TrendForce預期2H27 NAND緩解；Kuo預期缺口2027擴大、最早2H27新產能才緩解；TrendForce亦稱NAND需求為AI儲存帶動的結構性需求。","source":"iTiger: NAND Flash Supply Shortage Expected to Ease in Second Half of 2027","url":"https://www.itiger.com/news/1168527958","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Silicon Motion被分析師指出：控制器廠不像NAND原廠直接受惠NAND漲價，且NAND景氣為劇烈榮枯循環，營收可能隨循環反轉快速下滑。","source":"Nasdaq/Walnut Invest 摘要（SIMO bull-bear）","url":"https://walnutinvest.com/stocks/simo/is-it-a-buy-or-sell","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"SIMO 與 MaxLinear 已於 2023-07-26 取得中國 SAMR 反壟斷批准；其後 MaxLinear 片面終止合併，SIMO 在新加坡 SIAC 仲裁求償 1.6 億美元終止費，聽證已結束、等待終局裁決。","source":"SEC EDGAR 20-F FY2025 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"On July 26, 2023, the Company and MaxLinear received antitrust approval from the State Administration for Market Regulation of the People’s Republic of China (“SAMR Approval”).","as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"20-F 法律程序章節：管理層認為一般訴訟不致造成重大不利影響；唯一點名的重大程序為對 MaxLinear 的 SIAC 仲裁，未列反壟斷調查。","source":"SEC EDGAR 20-F FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"management does not believe that the outcome of any of these matters will have a material adverse effect on our business, results of operations, financial position or cash flows.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"SIMO 20-F 揭露國際營運面臨政府貿易限制、實體清單、制裁、關稅與配額風險；川普政府已對公司營運所在的部分東亞國家加徵關稅，關稅可能衝擊需求與成本；NAND 等原料供應亦受貿易限制與關稅影響。","source":"SEC EDGAR 20-F FY2025 Item 3 風險因素","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"The Trump administration has imposed and/or increased tariffs on imported goods from several geographic regions, including certain East Asian nations where we operate. The imposition of such tariffs and the threat of additional increases and/or retaliatory tariffs may strain international trade relations or impact our costs.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"SIMO 為無晶圓廠，晶圓由兩家外部晶圓代工廠製造，主要為台積電、次要為中芯（SMIC）；與這些代工廠及次承包商無長期合約，依客戶訂單與預測下單。","source":"Silicon Motion Form 20-F FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001329394/000119312526197184/d17718d20f.htm","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 20-F 提示基板（substrate）供應若吃緊，可能造成交貨延遲與毛利壓力。","source":"Silicon Motion Form 20-F FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001329394/000119312526197184/d17718d20f.htm","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"SIMO 總部與核心研發位於台灣；其申報文件承認因兩岸區域地緣緊張而在台灣營運有重大風險（二手 PESTLE 分析轉述）。","source":"dcf-analysis.com SIMO PESTLE Analysis [Apr-2026]","url":"https://dcf-analysis.com/products/simo-pestel-analysis","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"SIMO 2026Q3 淨銷售 $560.2M，季增 24%、年增 131%，高於財測區間 $519–541M；SSD controller 銷售季增 20–25%、年增 55–60%（來自搜尋摘要轉述，未逐字核對）","source":"SIMO Form 6-K 2026Q3 press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"SIMO Q2 call：MonTitan 企業級 SSD 已與兩家 Tier 1 客戶進入量產，預期下半年另五家 Tier 1 客戶開始放量","source":"MarketBeat Q2 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/silicon-motion-technology-q2-earnings-call-highlights-2026-07-30/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"TrendForce 預期 NAND 供需 2027 下半年趨於平衡，2026 供給缺口約 4–6%；伺服器為主要需求成長來源","source":"Guru3D: NAND flash supply expected to return to market balance in 2027","url":"https://www.guru3d.com/story/nand-flash-supply-expected-to-return-to-market-balance-in-2027/","excerpt":null,"as_of":"2026-09-15","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"SIMO 表示 NAND 短缺下 SSD 廠可能縮減容量以滿足出貨量，仍需採購控制器；預期 2027 供給更緊","source":"Tom's Hardware: Silicon Motion increases sales of SSD controllers amid NAND shortage","url":"https://www.tomshardware.com/pc-components/ssds/silicon-motion-increases-sales-of-ssd-controllers-amid-nand-shortage-but-expects-nand-shortages-to-get-worse-in-2027-supply-conditions-will-become-even-worse","excerpt":"SSD makers may reduce the capacity of their drives to meet unit demand, which means that they will still buy SSD controllers and, in some cases, even increase their controller purchases.","as_of":"2026-06-04","retrieved_at":"20261103","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"20-F 風險因子：若固態儲存改用 NAND 以外的非揮發記憶體而公司無具競爭力的控制器技術，控制器可及市場可能縮小；NAND 演進可能帶來公司相對不利的新型儲存裝置與市場區隔。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"If solid state storage devices were to use other types of non-volatile memory technologies other than NAND flash and we do not have relevant and competitive controller technology, our addressable market for controllers could shrink.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"20-F 風險因子：市場競爭激烈、技術快速變遷，中國競爭對手受惠於政府半導體在地化政策。","source":"SEC EDGAR 20-F FY2025 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"our competitors in China have benefited from the government’s semiconductor localization policies.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"SK hynix 與 Sandisk 於 FMS 2026 透過 OCP 發布 High Bandwidth Flash(HBF)首版規格，定位介於 HBM 與 SSD 之間；Sandisk 規劃 2027 初出推論裝置樣品。HBF 透過基底控制器晶粒與加速器介接（搜尋摘要，未讀原頁）。","source":"搜尋結果：StorageReview / Guru3D / hwbusters HBF 報導","url":"https://www.storagereview.com/news/sandisk-tapes-out-its-first-hbf-memory-die-targets-2027-for-inference-product-samples","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"HBF 規格發布：最高 512GB、頻寬 0.4–3.0TB/s","source":"Guru3D","url":"https://www.guru3d.com/story/sk-hynix-and-sandisk-hbf-standard-reaches-512gb-and-3tb-s-through-ucie/","excerpt":"SK Hynix and Sandisk HBF Standard Reaches 512GB and 3TB/s Through UCIe Published 2026-08-04 09:00 by Hilbert Hagedoorn News Comments 1","as_of":"2026-08-04","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"直銷占銷售比重由 2023/2024 的 65% 降至 2025 的 53%，其餘為經銷商，即經銷通路占比上升至約 47%","source":"SEC EDGAR 20-F FY2025 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"Approximately 65% of our sales in 2023, 65% of our sales in 2024, and 53% of our sales in 2025 were attributable to our direct sales force while the remainder was attributable to distributors.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Computex 2026：公司副總稱零售 SSD 市場上半年近乎消失，量直接流向 PC 品牌與模組廠","source":"Geeknetic：Silicon Motion confirma un giro en el mercado SSD","url":"https://www.geeknetic.es/Noticia/39093/Silicon-Motion-confirma-un-giro-en-el-mercado-SSD-el-canal-retail-se-hunde-mientras-los-fabricantes-de-PC-absorben-cada-vez-mas-unidades.html","excerpt":"El canal retail se debilita, pero el volumen sigue moviéndose hacia el mercado OEM. Desde el punto de vista de Silicon Motion, eso incluso tiene un lado positivo, porque la compañía continúa vendiendo muchas controladoras SSD a fabricantes de módulos, aunque esos productos ya no terminen en la estantería de una tienda o en el","as_of":"2026-06-16","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 列出最近一次 guidance 於 2026-07-29 發布，Q3 2026 營收區間 $519M-$541M，高於前次 $393M-$411M","source":"Benzinga SIMO earnings forecasts","url":"https://www.benzinga.com/quote/SIMO/earnings-forecasts","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Investing.com 12個月平均目標價 369.70、高 450、低 325，10 Buy 1 Hold","source":"Investing.com SIMO","url":"https://www.investing.com/equities/silicon-motion-te","excerpt":null,"as_of":"2026-09-04","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Tickflow（資料至 2026-08-07）4位分析師共識 Buy，均值目標價 $251.25，高 275 低 230","source":"Tickflow SIMO forecast","url":"https://www.tickflow.io/stock/SIMO/forecast","excerpt":null,"as_of":"2026-08-07","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Nasdaq 文章：Q1'26 指引上調至 $292-306M 後，分析師將 FY2026 營收共識調至 $1.27B（+43%）","source":"Nasdaq Bull of the Day: Silicon Motion","url":"https://www.nasdaq.com/articles/bull-day-silicon-motion-simo","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"SIMO 於 2023-10-05 向 SIAC 對 MaxLinear 提起仲裁，求償 1.6 億美元終止費及其他損害；2025-10 與 2026-03 聽證後程序結束，等待終裁（FY2025 20-F）。","source":"SEC EDGAR 20-F FY2025 Item 8 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"Following hearings conducted in October 2025 and March 2026, the arbitration proceedings have concluded, and the parties are awaiting the issuance of the final award.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2023-08-31 起的 Water Island 證券集體訴訟（S.D. Cal.）於 2024-09 修訂訴狀，新增 SIMO 與兩位高管為被告，主張 10b-5 與 20(a)；20-F 未預期重大不利影響。","source":"SEC EDGAR 20-F FY2025 Item 8 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"On September 18, 2024, the Plaintiff filed an amended complaint against the MaxLinear Defendants, and also added Silicon Motion and two of our officers, Messrs. Kou and Lai (the “Silicon Motion Defendants”), asserting substantially similar claims under the Exchange Act.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"與 MaxLinear 合併案已於 2023 終止，目前僅剩 SIAC 仲裁待終裁，求償 1.6 億美元終止費。","source":"SEC EDGAR 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"the Company is seeking payment of the termination fee of US$160 million, together with further substantial damages, interests, and costs.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Water Island 證券集體訴訟仍在 S.D. Cal. 審理，SIMO 與兩位高管為被告。","source":"SEC EDGAR 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/1329394/000119312526197184/d17718d20f.htm","excerpt":"On September 18, 2024, the Plaintiff filed an amended complaint against the MaxLinear Defendants, and also added Silicon Motion and two of our officers, Messrs. Kou and Lai (the “Silicon Motion Defendants”), asserting substantially similar claims under the Exchange Act.","as_of":"2026-04-30","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SIMO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.54,"operating_margin_pct":21.3,"fcf_margin_pct":-24.9,"rd_intensity_pct":23.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIMO","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"8299.TWO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.85,"operating_margin_pct":30.89,"fcf_margin_pct":-8.12,"rd_intensity_pct":21.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.8299.TWO","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MRVL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.21,"operating_margin_pct":16.81,"fcf_margin_pct":18.23,"rd_intensity_pct":25.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"SNDK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":76.84,"operating_margin_pct":68.43,"fcf_margin_pct":61.63,"rd_intensity_pct":5.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNDK","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"SIMO"},"financial_history":{"ticker":"SIMO","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":945921000.0,"revenue_yoy_pct":null,"gross_margin_pct":49.25,"operating_margin_pct":22.66,"net_income":172510000.0,"diluted_eps":5.168,"free_cash_flow":50950000.0,"fcf_margin_pct":5.39,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":639142000.0,"revenue_yoy_pct":-32.43,"gross_margin_pct":42.31,"operating_margin_pct":6.44,"net_income":52873000.0,"diluted_eps":1.58,"free_cash_flow":98770000.0,"fcf_margin_pct":15.45,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":803552000.0,"revenue_yoy_pct":25.72,"gross_margin_pct":45.89,"operating_margin_pct":11.47,"net_income":89249000.0,"diluted_eps":2.69,"free_cash_flow":32744000.0,"fcf_margin_pct":4.07,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":885627000.0,"revenue_yoy_pct":10.21,"gross_margin_pct":48.27,"operating_margin_pct":10.51,"net_income":122635000.0,"diluted_eps":3.64,"free_cash_flow":6295000.0,"fcf_margin_pct":0.71,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SIMO/SIMO_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Silicon Motion Technology Corporation** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good day, and thank you for standing by. Welcome to Silicon Motion Technology Corporation's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please be advised that today's conference is being recorded. This conference call contains forward-looking statements within the meaning of Section 27A of the Securities Act of 1933 and Section 21E of the Securities Exchange Act of 1934 as amended. 
Such forward-looking statements include, without limitation, statements regarding trends in the semiconductor industry and our future results of operations, financial condition and business prospects. Although such statements are based on our own information and information from other sources we believe to be reliable, you should not place undue reliance on them. These statements involve risks and uncertainties, and actual market trends and our results may differ materially from those expressed or implied in these forward-looking statements for a variety of reasons.
Potential risks and uncertainties include, but are not limited to, continued competitive pressure in the semiconductor industry and the effect of such pressure on prices, unpredictable changes in technology and consumer demand for multimedia consumer electronics, the state of and any change in our relationship with our major customers and changes in political, economic, legal and social conditions in Taiwan. 
For additional discussion of these risks and uncertainties and other factors, please see the documents we file from time to time with the Securities and Exchange Commission. We assume no obligation to update any forward-looking statements, which apply only as of the date of this conference call. And with that, I'll now hand you over to Mr. Tom Sepenzis, Vice President of Investor Relations and Strategy. Please go ahead.

**Thomas Andrew Sepenzis** (Executives):
Good morning, everyone, and welcome to Silicon Motion's third quarter 2026 financial results conference call and webcast. Joining me today is Wallace Kou, our President and CEO, and Jason Tsai, our CFO. Wallace will first provide a review of our key business developments, and then Jason will discuss our third quarter results and outlook. Following our prepared remarks, we will conclude with a Q&A session. 
Before we begin, I would like to remind you of our safe harbor policy, which was read at the start of this call. For a comprehensive overview of the risks involved in investing in our securities, please refer to our filings with the U.S. Securities and Exchange Commission. For more details on our financial results, please refer to our press release, which was filed on Form 6-K after the close of the market yesterday.
This webcast will be available for replay in the investor relations section of our website for a limited time. To enhance investors' understanding of our ongoing economic performance, we will discuss non-GAAP information during this call. We use non-GAAP financial measures internally to evaluate and manage our operations. We have therefore chosen to provide this information to enable you to perform comparisons of our operating results in a manner consistent with how we analyze our own operating results. The reconciliation of the GAAP to non-GAAP financial data can be found in our earnings release issued yesterday. We ask that you review it in conjunction with this call. With that, I will turn the call over to Wallace.

**Chia-Chang Kou** (Executives):
Thank you, Tom. Hello. Thank you for joining us to the call today. I am pleased to report that we delivered another quarter of strong growth with revenue of $560 million and gross margin of 53.7%, driven by the growth in Ferri for automotive, Edge AI, and boot drive storage, our Edge SSD business, and our emerging MonTitan controller for enterprise SSD. We drove another quarter of higher operation performance, delivering the second consecutive quarter of record earnings per ADS, as we continue to capitalize on our product and market diversification strategy. We are on track to deliver record revenue in 2026 with over 100% top-line growth. Our strategy is simple, deliver real value to customers and focus where we are uniquely differentiated so we can generate strong ROI for shareholders. For our edge controllers, we have become the de facto standard for mobile, IoT, and PC controller solutions.
For NAND makers and virtually every module maker with outsourcing become a much more meaningful portion of the market. Our matched controller technology and design expertise deliver solutions that are better performing, consume less power, and are more cost-efficient than either in-house or other merchant solutions. Our strong share gains are driving significant growth despite end market weakness, and we expect this to continue. 
Our MonTitan enterprise SSD controllers are winning across the ecosystem with leading NAND makers, hyperscalers, and CSPs, and with the module makers that supply AI server to hyperscale and enterprise customers. Our success is based on our unique combination of two decades of controller and firmware design experience and our history of managing more NAND than anyone in the industry.
This has created an incredible, solid foundation for our leading enterprise controller products. And then we expect our MonTitan revenue ramp to accelerate as we introduce our next generation PCIe 6 controller next year. And lastly, for our storage solution segment, our strategy has always been to focus in areas that are underserved by NAND makers. We are rapidly growing share in this vital low density, smaller volume market that require more design and customization work. We have spent more than a decade building one of the industry's broadest automotive-grade portfolio, supported by dedicated quality and supporting team. Today, that foundation positions us to capture fast-growing compute and storage demand across cars, drones, and increasingly robotics.
For our enterprise boot drive solution, our unique combination of broad controller platforms, best-in-class firmware, technical know-how, NAND suppliers relationship, and manufacturing capability put us in an ideal position to serve the growing need of AI infrastructure market. As a result, we are rapidly evolving to much more balanced and profitable company as a new enterprise in AI product enhance our leading consumer controller share, strengthening our competitive position from AI infrastructure to the edge to deliver long-term sustainable revenue and earning growth. I would like to take a moment to address the current market environment. The AI super cycle has driven robust demand of HBM, DRAM, NAND, HDDs for the past several quarters, with no sign of slowing down. Prices have risen sharply over the past year and the strained substrate supply across memory and storage enterprise market remain relatively insensitive to price.
For PC, smartphone, and other consumer device OEM are struggling to bring affordable product to market, given today's memory and storage cost, and the consumer unit volume are declining as a result. We expect conditions to stay difficult until bit supply come back into balance with demand. New NAND fabs are planned for 2028, and NAND makers continue to add bit through higher layer count. So we do not see this changing the current supply-demand imbalance to any great degree. Flash makers continue to prioritize enterprise and high-capacity solution, creating new and expanding opportunity for Silicon Motion. Our growth is benefiting from more outsourcing and larger opportunity in enterprise and the storage solution market that we are uniquely positioned to win. We are at the beginning of the journey in the enterprise and AI market, and our early success will drive accelerating demand for our next generation storage technologies.
Let me now detail our embedded eMMC and UFS business, which include controller for smartphone IoT connected devices. Our eMMC, UFS business was up over 100% year-over-year in the first half of 2026 as the NAND makers are shifting their resources toward DRAM and HBM solutions, allowing module makers to take share in the mobile market. This has helped drive our market share gains as module makers look to third-party controller partner to make their mobile solution. 
In the third quarter, eMMC and UFS revenue declines modestly from the prior quarter, reflecting customer launch timing and the challenging smartphone OEM face in offering affordable device amid the higher NAND and DRAM prices. We expect the headwind to persist in the near to midterms, until additionally memory and storage supply comes online.
Across the markets that we sell our eMMC, UFS controller, OEM are reducing specification to try to offset the rising memory and storage cost. We expect our eMMC, UFS business to remain relatively flat in the near term given the current market challenging, but I do believe we can return to growth next year and beyond as our new UFS 4.1 controller and UFS 5 controller ramp and driving higher ASPs. 
Now turning to our SSD controller business, which include Edge and MonTitan enterprise SSD controllers. This business delivers strong sequential and year-over-year growth. In SSD, our PCIe 5 investment continue to pay off, with growth in both our four-channel and eight-channel controllers. PCIe 5 currently represent approximately 10% of the PC market, and we expect this will grow to 20%-25% of market by the end of 2027.
Providing a strong runway for further growth. Our leading position in PCIe 5 is driving greater market share gains within the PC market. And as the industry transition from PCIe 4 to PCIe 5, we expect to see further top-line improvement given the higher ASP associated with these next-generation products. We are currently working with all the major NAND makers and most of the leading module makers to deliver compelling SSD solutions that leverage PCIe 4 and PCIe 5 controllers. We are tracking well ahead of expectation to achieve our market share goals of 40% through Apple by 2028, and believe we will continue to improve our position. While PC unit headwinds associated with the higher memory and storage prices present challenges, we believe we will drive further top-line growth through the market share gains and ASP increases as the market shift to PCIe 5 continues.
I would now like to provide you with an update on our new MonTitan enterprise SSD business. NAND remains a critically important technology across enterprise and AI storage ecosystem, and MonTitan is positioned for rapid growth in the coming years. This eSSD solution delivers high speed, low latency storage that targets compute and data storage application for enterprise AI platforms. 
Our first two customers began shipping TLC eSSD for compute that leverage our MonTitan controller in the second quarter. All seven of our announced customers are on track to begin commercial ramp in 2026 with both TLC-based compute and QLC-based data storage products. TLC-based compute eSSD using MonTitan are expected to grow more quickly than QLC-based data storage eSSD in the near term, until greater supply of 2 terabit die become available.
Encouragingly, four of our six NAND makers have started production of 2 terabit QLC die to date, and we expect all NAND makers to begin shipping 2 terabit QLC by end of 2027. So momentum will accelerate through next year. During the third quarter, we taped out our next-generation 4nm PCIe 6 MonTitan controller targeting hyperscalers and CSPs, and expect to begin sampling in the first quarter of 2027. We have one design with multiple tier one customers, including NAND flash makers, hyperscalers, and CSPs. The new controller was designed for both compute application using TLC and data storage using QLC NAND as a performance shaping and multi-tenancy service architecture extremely well suited for a Gen AI infrastructure. We continue to see increased inbound interest in our MonTitan controllers, and expect this new enterprise controller segment will help us deliver long-term sustainable top and bottom-line growth.
And finally, I would like to provide an update on our Ferri automotive, edge, and enterprise boot drive storage business. Our solution business, which includes Ferri and boot drives, delivered the strongest result in the third quarter, with revenue up over 75% sequentially, representing over 40% of our revenue. Our automotive business has been a particularly strong source of strength, delivering better-than-expected top-line results and higher gross margins. We continue to scale this business quickly as we know automotive market, its customers, and the supply chain extremely well, which has driven significant backlog for long-term growth as we accelerate our share gains. We have since spent more than a decade developing our automotive products and certifications. Today, our storage controller and firmware offer the broadest portfolio of solution to serve every part of the automotive market.
Our success in automotive has drawn interest in Ferri for other large growing markets, including robotics, drones, and advanced networking. In the emerging robotic market, we are actively engaged with several companies that want to use our storage product. We are seeing multiple opportunities in humanoid robots and other physical AI systems, including vision, LiDAR, and compute storage. 
Our early conversation suggests robotic opportunity may be larger than automotive, and we believe Ferri is ideally suited to address it. Our fast-growing boot drive business is also gaining momentum. We estimate that the market will be approximately $3 billion in 2026, growing to over $5 billion by 2030. In the third quarter, we won design with several new Tier one customers for networking and AI infrastructure products. These programs are expected to ramp over the next 2 years and will substantially improve our backlog visibility.
As the average capacity of enterprise boot drives is much smaller than compute and data storage SSD drives, the NAND makers no longer prioritize this market. Additionally, our DRAMless controller delivers the performance, reliability, endurance this drive needs with lower power consumption requirements, smaller form factor, and the lower cost than DRAM-based design. Boot drive handles the operation system, logging, and system management rather than heavy data workload, so they do not need the expense of onboard DRAM for DPU, router, and switch products. As AI infrastructure builds out at large numbers of servers, the networking and DPU equipment shipments are increasing rapidly, each needing reliable boot storage, driving the growing demand for DRAMless boot drives. We have been the primary supplier for DRAMless boot drive controllers to the NAND maker that have historically served this market, but they are moving on the higher density opportunity.
Silicon Motion are uniquely positioned with the right technology, the right support, the leading security firmware, and proven ability to procure NAND, making us the best partner for those needing a boot drive solution. Looking ahead, however, we are seeing significant new opportunity for boot drive with onboard DRAM. Given the strong demand of AI inference and agentic AI, near CPU boot drive with DRAM provide lower latency and open compute project features that are in increasingly high demand. As the NAND maker have shifted resources toward HBM, DRAM, and higher capacity compute and data storage SSD, there is a growing shortage of near CPU boot drives with DRAM. We estimate that this market will reach over $10 billion by 2030, making a significant new opportunity for Silicon Motion.
We are already in discussion with multiple potential customers for boot drive that leverage our industry-leading eight-channel and PCIe 5 controller that can serve the near CPU market to further expand our market opportunity, and expect to begin ramping product for this market in the second half of 2027. 
Our Ferri automotive, edge AI, and boot drive solution business are performing especially exceptional well, and these are many large and growing opportunity for our product in this segment. 
Our backlog has increased significantly in just the past three months, and we expect many additional customer design wins in automotive, edge AI, and boot drive solution to deliver significant future growth. We continue to benefit from our proven ability to secure NAND in a difficult environment from multiple NAND suppliers, and this continues to be a powerful differentiator for our company.
In conclusion, Silicon Motion delivered its fourth consecutive quarter of record revenue as we executed across a rapidly diversifying business. We are a fundamentally stronger company today with a stronger balance sheet, broadest range of solution and product, and more opportunity ahead than at any time in our history. Our broad portfolio serves surging AI demand from the data center to the edge. That breadth gives us balance across our market and the flexibility to seize growing opportunity while navigating challenge like those we face today in PC and smartphones. I am extremely proud of our teams. Together, we have built a durable, diversified business powered by best-in-class technology, expanding share and new end markets, strengthened by two decades of relationship with OEMs, module makers, and NAND makers. I am more confident than ever that we will continue to deliver broad-based, sustainable growth long term. Now let me turn the call to Jason to go over our financial performance and outlook.

**Jason Tsai** (Executives):
Thank you, Wallace, and good morning to everyone joining us today. I will discuss additional details of our third quarter results and then provide our outlook. Please note that my comments today will focus primarily on our non-GAAP results, unless otherwise specifically noted. A reconciliation of GAAP to non-GAAP data is included with our earnings release issued yesterday. Before I get into the results, I would like to comment briefly on our convertible bond issuance on August 13th. We raised an aggregate $1.15 billion with net proceeds to the company of $1.127 billion. This successful raise was increased from the initial offering of $800 million. This new CB at 0% interest and an initial conversion price of $380.50 represents a conversion premium of 65% over the last reported sale price of SIMO on August 10th, the day the deal was announced.
This additional capital significantly strengthens our balance sheet and will help fuel our growth and enhance our working capital to scale our business. Now, turning to our results. We delivered an outstanding third quarter, surpassing our expectations, driven by stronger execution and demand trends. In the September quarter, sales increased 24% sequentially and 131% year-on-year to $560 million, coming in well above the high end of our guided range of $519 million to $541 million, delivering our fourth consecutive quarter of record revenue. We experienced strong growth across most of our businesses in the third quarter, with standout growth in Ferri for automotive, enterprise boot drives, and SSD controllers, including Edge and MonTitan for enterprise. Gross margins of 53.7% was significantly better than guidance as we capitalize on new product introductions and benefited from better mix and better-than-expected margins in our Ferri automotive products.
Operating expenses slightly decreased sequentially to $120.7 million and operating margin increased 32.1%, well exceeding our guidance, driven by higher-than-expected revenue and gross margin in the quarter. Earnings per ADS was $4.35, a 79% increase sequentially and a 333% increase compared to same quarter last year. Total stock-based compensation, which we exclude from non-GAAP results, was $17.3 million in the September quarter. We had $953.6 million in cash equivalents, and restricted cash at the end of the third quarter, compared to $181.8 million at the end of the second quarter. Cash increased in the third quarter due to the successful $1.15 billion convertible notes offering that we executed in the quarter, offset by the increase in working capital, dividend payment, and the repayment of the short-term bank loan. 
Our strategy, as Wallace outlined at the start of this call, continues to drive growth and expand our opportunities. Our experience, our customers and partners, and our unmatched technology and development of NAND controllers and solutions has driven a significant transformation of the company. While the NAND market continues to be dynamic, our investments across consumer, enterprise, data center, and AI applications are the foundation of our rapidly growing business.
As a result, we believe the momentum in our business will continue in the fourth quarter and now expect revenue to grow 5% to10% sequentially to $588 million to $616 million, with growth across nearly all our product segments led by Ferri for automotive, enterprise boot drive solutions, and MonTitan enterprise SSD controllers. We believe our SSD controller business will be flat to slightly down given the current memory and storage environment and typical seasonality. Gross margins are expected to increase sequentially to 54% to 55% in the December quarter, given the continuing improvement in product mix.
Operating margin is expected to grow to 36%-37% as continued strong revenue growth and higher profitability drives the leverage to the bottom line. Our effective tax rate is expected to be 20%, and stock-based comp and dispute-related expenses are expected to be in the range of $34.6 million to $35.6 million. 2026 is on track to deliver record revenue for Silicon Motion, with top line expected to more than double year-over-year. While we continue to invest heavily in R&D this year to expand our portfolio of leading-edge solutions, we are confident that along with the higher revenue and improved gross profitability, our operating margins will exceed 30% exiting this year. We expect this momentum to carry into 2027.
Our strong backlog across all of our businesses gives us confidence that we can grow revenue by at least 40% next year, with gross profitability to be in the low to mid 50% range. Our mix is improving. With more contribution from enterprise controllers and Ferri automotive solutions, we should be able to sustain this higher margin level. It is also worth emphasizing that these new enterprise opportunities represent larger addressable markets than our consumer segments. 
And because they are greenfield opportunities for Silicon Motion, we can grow significantly by gaining share without depending on further market growth. Any market expansion would only add to our potential upside. We set out to diversify beyond consumer applications into automotive and enterprise, and that strategy is now producing outsized results. Our longstanding leadership in merchant controllers and our multiyear investments in enterprise and AI SSDs are beginning to bear fruit.
The solutions we are winning in these markets offer far greater visibility, much longer product cycles, and significantly higher barriers to entry, which together underpin sustained growth in revenue and profitability. As these wins ramp across a broad mix of end markets, consumer cycles will have less influence on our results. Our visibility is improving significantly, and our business will become meaningfully more resilient and predictable. Our balance sheet has never been stronger, and we are well-positioned to capitalize on the fundamental drivers at our foundation of the transformation that Wallace spoke about earlier. I look forward to sharing more on our progress next quarter. This concludes our prepared comments. I would like to open up the questions now. Operator?

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Neil Young of Needham & Company.

**Neil Young** (Analysts):
First question, just given that you just gave us the expecting revenue to grow by at least 40% next year and gross margin in the low 50% range, curious if you could sort of dive into maybe the main drivers of that. I mean, the given that gross margin, you expect sort of resetting the long-term target, it sounds like now. I would expect more of the growth to be driven by sort of the higher margin business like Ferri and MonTitan, but any comments that you can add further on to '27?

**Jason Tsai** (Executives):
Yes, I think that is right. I think we are seeing significant traction with MonTitan. We are seeing the automotive, Ferri for automotive, ramping very aggressively as well. A lot of these Ferri projects, especially in automotive, these are multi-year engagements where, once we are qualified in, we have got a really long-standing position with that socket, with that customer. We are working with virtually every automaker in the world for a variety of solutions going into a significant amount of their portfolio, but significant room for growth still. So based upon our backlog, based upon the growth we anticipate from MonTitan, as well as other SSD controllers and Ferri for automotive, we believe that we can sustain these low to mid 50% gross margins.

**Neil Young** (Analysts):
Okay, great. That is helpful. Just in this quarter, bringing it back, looking at the Ferri and boot drive, obviously the growth continuing is really great. Could you, by any chance, give us some more detail? It sounds like Ferri might have outgrew boot drive in the quarter. Obviously, beyond automotive, I should say, in Ferri, curious to learn more about the robotics and where you guys play in that.

**Chia-Chang Kou** (Executives):
I think because of Ferri for automotive been for a long time, so we see the custom base are very strong. For this year, definitely it is Ferri for automotive, it grows stronger. However, our boot drive also gaining momentum with the diversified customers, more than just GPU customer and our TPU customer. We recently winning all the networking and server customers. We see our enterprise boot drive will grow even much faster next year. 
In robotics, I think it is still very early stage, and the total volume is still very small, but we try to make sure we will be in when the market take a boom.

**Jason Tsai** (Executives):
And keep in mind, a lot of the features within the Ferri for automotive products are the same features that the robotics requires, right? Which is high temp, vibration, all of the things that go into a car largely go into the robotics as well. So having that certification already, having those products already, puts us in a significant advantage to penetrate this market as it grows.

**Operator** (Operator):
We will now take our next question from the line of Craig Ellis of B. Riley Securities.

**Craig Ellis** (Analysts):
Congratulations on the tremendous momentum that it seems you have in the business. I wanted to start with a question for you, Wallace. Very exciting to hear about the engagement that you have got with near CPU boot drives, because the performance gains, given reduced latency with the way that can implement are really quite profound, and it seems like that could be a very significant market. The question is this: Do you see this implementing on more of a custom basis across customers, or is JEDEC going to move super quickly and get standards out here in another quarter or two? Then, can you just talk a little more about how you would see the early part of the ramp for Silicon Motion?

**Chia-Chang Kou** (Executives):
Now we see opportunity come from the early third quarter, because conventionally, this near CPU boot drive with DRAM belong to NAND makers. Because all NAND makers are busy and try to produce at least eight terabyte, 16 terabyte Compute SSD. They have less interest of resource on NAND allocation for the low capacity near CPU boot drive. The near CPU boot drive primary density is about one terabyte, two terabyte, and some also 512 gigabyte. four terabytes, very, very few. I think because we can see it will be probably a very, very big gap of shortage supply for 2027. Many, many customers come to Silicon Motion. We are preparing discussion, and I think the solution, definitely need to have a customized sum feature and tailored for individual server and leading hyperscalers. So this is not a simple work.
We will try to focus on select the NAND and make sure we follow the OCP requirement and provide the firmware. I think we will be ready for the firmware and solution by early Q1, and production ramp will be second half 2027.

**Craig Ellis** (Analysts):
That is really helpful. The second question is really a higher level question for you and Jason. The team has done a phenomenal job operationally this year, putting the business in a position to grow 100% plus year-on-year. Can you help us understand the positioning that you feel like you are in with wafer supply, packaging, et cetera, to support the 40% growth? If demand is greater, given some reports that things like agentic AI, CPUs could grow 47% next year, can you just help us understand if there is upside potential in the supply chain to meet greater demand than that 40%?

**Chia-Chang Kou** (Executives):
As you know very well, in semiconductor industry today, everything is in shortage, right? From substrate, from material, from wafer, from NAND, from memory, from even test capacity. But I think our manufacturing operating team did a very good job. We secured our 2027 wafer with TSMC primarily. And also, we also secured the test capacity and assembly capacity and the substrate material. So we believe we are able to support our growth for 2027. Jason mentioned we see we definitely can grow minimum 40% year-over-year. I think in next quarter earning call, we will provide more meaningful guidance for our 2027.

**Operator** (Operator):
We will now take our next question from the line of Sebastien Naji of William Blair.

**Sebastien Cyrus Naji** (Analysts):
Congrats on another record quarter here. My first question is maybe a little bit higher level and strategic. As your SSD solution business continues to grow as a share of revenue hit over 40% in Q3, it is driving greater NAND pricing exposure into Silicon Motion's model. And that is a little bit of a shift for a company that was largely tied to volume growth historically. So maybe just how do you think about managing this new pricing dynamic and how it could impact your growth and margins, particularly if NAND pricing starts to come down?

**Chia-Chang Kou** (Executives):
I think we definitely manage the NAND price increase and negotiate with the customer to pass through the cost to customers, so we benefit from the sale revenue growth. So we believe the NAND price increase will come to moderate because the spot price for module maker now has become challenging. We see the Q3, Q4 NAND pricing are rather similar. For next year, we also see the, although will be a single digit growth quarter, but it will be moderate. For our business, why we focus on automotive and boot drive, because the end customer want to have a long-term contract and support and supply. Our contract with customers and price will stay with at least two quarter, and we negotiate price every 6 months.
We are able to manage the price and the cost, and that is why we can see through the demand, and we can manage our gross margin continually. We see the NAND wafer price will be more stable in comparison last year.

**Jason Tsai** (Executives):
One more thing, Sebastien. I think certainly there is a fear that, if NAND flash prices begin to come down, how does that affect our growth? I think one of the things that we are seeing in automotive, even in boot drives, is that there is some just despeccing going on. I think all things being equal, if NAND availability was better, if pricing was better, our customers would double their density or more in some cases. I think between a combination of kind of respecing to normal specs as well as additional opportunities, additional customers that is coming online over the next 12 months, 18 months, 24 months, I think we are well positioned to continue to grow even as the NAND market stabilizes over the next 2 years.

**Sebastien Cyrus Naji** (Analysts):
Got it. Great. That's helpful. Maybe just as a related follow-up around the funding that you raised and the working capital needs, I just wanted to get maybe a better sense for your ability to continue funding all of your working capital and inventory build with the cash that you have on hand. Can you maybe just talk a little bit about how quickly you expect inventory, particularly around NAND, to flow through the model and what it would take to maybe potentially need further capital down the line?

**Jason Tsai** (Executives):
Yes. For us, we're targeting about two quarters turnaround time between when we get the NAND and when we generate the cash flow. So, our expectation is to be able to turn that inventory relatively quickly, and generate the cash flow to support ongoing growth of our business. But when we did the raise, we talked about the raise being sufficient to fund our working capital needs for the next couple of years, based upon today's expectations. Obviously, as the business continues to grow and hopefully as it exceeds expectations, we'll continue to reevaluate that. But that's, at least right now for our visibility, we believe we're in a good spot.

**Operator** (Operator):
Our next question comes from the line of Suji Desilva of ROTH Capital.

**Sujeeva De Silva** (Analysts):
Congratulations on the progress here. The MonTitan product, the higher KV cache density you're expecting, are there innovations coming from HBM and DRAM that might offset the opportunity for SSDs and KV cache? I'd love to get your thoughts there. What's a good concept of the number of MonTitan and SSDs needed per GPU for KV cache?

**Chia-Chang Kou** (Executives):
I think the MonTitan demands from very wide range, not only from the AI server and for hyperscaler and also for the CSP, but also for NVIDIA ecosystem. I think we don't know the percentage how, but we see the demand for Compute SSD this year is bigger due to the NAND price is very expensive. But we also see the momentum for high capacity QLC coming for next year. I believe, when Samsung, Hynix, 2TB QLC can move to production, we'll see more QLC demand for data storage. MonTitan itself can handle both the Compute SSD and the Storage SSD. For KV cache, particularly for CMX, for NVIDIA structure, I think they will redefine and try, because the price is very expensive, they try to reduce the minimum capacity for each of their route and trade.
I think this will be probably, they will announce it early next year, and I think the related ecosystem will help him provide. I think as well as the CMX KV cache demand is growing, as well as demand additional eSSD. That's good for us, for MonTitan, because it increase our controller demand.

**Sujeeva De Silva** (Analysts):
Okay. Very helpful. The other question's for Jason, perhaps. 40% plus revenue growth next year, you talked about an operating margin guide in the 30s. Just how are you managing the OpEx and R&D growth, given that you have so many different end markets and projects you're focusing on? What's a kind of a growth rate for OpEx versus revenue that would be kind of a framework for us to think about?

**Jason Tsai** (Executives):
Yes. We'll get into more specific guidance around 2027 in January. This year we taped out a number of 6 nano meters and as well as 4 nano products. So, we're spending a lot of money on tape-out and design this year already. We anticipate continuing to invest next year. And again, we'll talk more about the specific OpEx guidance next year in January, but our expectation is that we will continue to be able to deliver operating margin leverage next year as well.

**Operator** (Operator):
Our next question comes from the line of Mehdi Hosseini of Susquehanna International Group.

**Mehdi Hosseini** (Analysts):
Yes. A couple of follow-ups from me. Wallace, Jason, can you quantify what percentage of your total revenue were attributable to Ferri, boot drive, and PCIe SSD, and how each percentage would change into next year? I have a couple of follow-ups.

**Chia-Chang Kou** (Executives):
So I would say we cannot party about detail, but about 40% our total revenue is around the solution from Boot Drive and Automotive, 60% from controller.

**Mehdi Hosseini** (Analysts):
Would those mixes change dramatically next year?

**Chia-Chang Kou** (Executives):
Next year, the solution Boot Drive Automotive might grow to 50%, but so far we didn't accurate, but I think that we see probably will be balanced next year, 50/50 between controller and solutions.

**Mehdi Hosseini** (Analysts):
Okay. Given how your exposure to the consumer end market is less looking forward compared to prior years, should I assume that there is no more seasonality from Q4 to Q1?

**Jason Tsai** (Executives):
Again, Mehdi, we will get into more specific Q1 and 2027 guidance in January.

**Mehdi Hosseini** (Analysts):
Okay, I was hoping to get a preview. You mentioned you are more driven by enterprise, and I am just trying to, maybe qualitatively, you can help us to.

**Jason Tsai** (Executives):
No, I can. Certainly, I think the enterprise becoming a bigger portion of the mix, Ferri becoming a bigger portion of the mix, I think certainly normal consumer seasonality will certainly be more muted going forward as consumer business becomes a smaller percentage of our business.

**Mehdi Hosseini** (Analysts):
Okay. And then is there any update on arbitration? It would be great to tell us whether the key milestone and how we track into those.

**Jason Tsai** (Executives):
Yes. We did the closing arguments in Singapore arbitration in March, and we are still anxiously awaiting the results. We don't have any other updates at this point, but certainly once the results come out, we'll be talking about those things quite a bit. But right now, there's no additional comments we're making around the arbitration.

**Operator** (Operator):
[Operator Instructions] Our next question comes from the line of Gokul Hariharan of JPMorgan.

**Gokul Hariharan** (Analysts):
The first question is on the near CPU boot drive opportunity. Wallace, I think you said you will start your solutions in the second half of next year. Could you talk a little bit about how big that opportunity can scale into? Because your enterprise boot drive partnership with NVIDIA, it scaled up very rapidly. But could you talk a little bit about how the opportunity is and how fresh that opportunity is, given that there are already a fair number of incumbents there? I just wanted to understand, the TAM is big, but how quickly can you scale this business?

**Chia-Chang Kou** (Executives):
I think that 10, will be a minimum $10 billion by 2030, because the density is bigger than the DRAMless boot drive. Because the NAND maker did not pay attention, but this business belonged to a NAND maker in the past, because especially the three NAND maker have DRAM. But because all the NAND makers, they focus on high capacity compute SSD, and the data storage SSD. So there is lack of resource and attention in the near CPU boot drive with DRAM. So that's why the supply becomes shortage, and many tier one customer come to Silicon Motion. We see the great opportunity. We also work with the leading NAND maker to see how we can work together to resolve the issue. So whether they will support more NAND. And, also we need to resolve manufacturing and also including some DRAM supply, too.
But we believe we'll start to ramp in the second half of this year. We also work with some module maker partner, because they will use our controller in the firmware, but we will have a different business model to work with them to benefit some financial results. Anyway, this is a new opportunity, and we just really don't have enough R&D resources. There's a great opportunity for Silicon Motion to grow, and they could grow even faster in '28 and '29. Because we have the great idea controller and fitting very well, and we have the firmware technology, and suddenly the controller, very lucky, have a certain OCP feature built in, so we don't need to redo the new ASIC. I think a lot of our NAND makers, they don't have a such controller today. So that's why we are in a great position to expand to the new market.

**Gokul Hariharan** (Analysts):
Got it. Just to follow up there. When you win business, do you have to win by individual server customer, or you just design into a chip platform and you kind of become the de facto in that chip platform, similar to what you do for the current enterprise boot drive?

**Chia-Chang Kou** (Executives):
All the near CPU boot drive today is M.2 form factor, 22 by 80.

**Gokul Hariharan** (Analysts):
Yes. Yes.

**Chia-Chang Kou** (Executives):
They need a low power, because our controller, Silicon Motion controller, our SM8000A, is ideal to fitting very well. This controller needs just a DDR4, or LPDDR4. So well-positioned into fitting this searching. So there is some NAND maker also want to work with us, but we have limited resources. We just have to make sure the firmware is ready. We will support two different NAND, by Q1 next year, and hopefully ramping smoothly in second half of next year.

**Gokul Hariharan** (Analysts):
As long as it is M.2 standard, you can start shipping. There is no additional qualification by individual server customer, et cetera, which takes time.

**Chia-Chang Kou** (Executives):
We are already working with our module maker, our customer, and they will support the leading tier one server maker. They may ship earlier by Q2 next year. It is only with support controller. Our own solution, total solution, will probably be ready shipping in second half next year.

**Gokul Hariharan** (Analysts):
Understood. Second question is for Jason. Jason, first on gross margins. Historically, we have seen Ferri and any NAND solution business operate in the probably lower than 40% or 40% kind of gross margin levels. Now, obviously, you have made a meaningful step up in gross margins for solution business as well. As NAND price starts to stabilize or not really go up a lot, how should we think about the margins? Are these the steady state margins that you expect the solution business to earn, given it is more enterprise related? And secondly, could you also talk a little bit about next year looks like, based on Wallace's comment, the SSD solutions business will grow faster than 40%? What is the support that you need from an inventory perspective? Inventory already has gone up to about $800 million or so.
Could you talk a little bit about how you think about how much working capital support you would need to support that kind of additional probably 50% plus growth in the solution business?

**Jason Tsai** (Executives):
Yes. So in terms of the gross margin question on the solutions business, as Wallace pointed out, we are negotiating 6-month pricing contracts with our customers, and we expect to turn our inventory here within that period as well. Maintaining very tight controls around working capital and price protection and margin protection for our products and our P&L. We anticipate that, certainly with automotive, these are qualified products going into projects that are multi-year, 3 years to 5 years in length. Pricing as well as supply agreements are agreed upon at the beginning of these engagements. And so we are confident that we can maintain better margins, especially as the solution complexity, the design, the support becomes more onerous. And so having the higher margin supports all of that.
In terms of the working capital, as I said, with the raise that we have done, we are confident that we can support the next couple of years' worth of business based upon what current forecasts look like. So we will continue to grow inventory, but obviously in anticipation of a 40% plus year, we have grown inventory now. We will continue to grow inventory in the next quarter, in the fourth quarter, and then we will start seeing obviously the turns of that inventory come back into cash flow as we progress.

**Operator** (Operator):
Next question comes from the line of Daniel Yen of Morgan Stanley.

**Daniel Yen** (Analysts):
Congratulations on a great result. I want to switch gears to a very different question. Wallace, you just mentioned about some opportunities, for example, for your boot drive, for example, enterprise SSD. But I want to ask what will be your strategy right now in China. I think China is still the important region, and I think in China, we also have CSPs, we have NAND supplier, NAND makers. We also have a lot of module houses there. But at the same time, I think competition is still there. So I want to consult you on Silicon Motion's strategy right now in China both with the NAND makers, with the competitors, and also how should we address maybe the future demand from the CSP in China.

**Chia-Chang Kou** (Executives):
I think that we really want the balance between China and also the rest of world. China has YMTC, NAND maker, they are very strong. They grow very fast. We also support and collaborate with the YMTC directly or indirectly with the module maker. I think the enterprise portion, we see they will become stronger in 2027. I think we definitely work closely for China CSP for hyperscaler. Believe us, and I think that is why we try to grow China local R&D. Eventually, we want China, our local R&D can support China customer. In Taiwan, we support the rest of world, especially for U.S. customers. And secondly, I think the China, they are growing enterprise controller company, but in the past, they also like to make enterprise C drive. In the past, as you know, NAND pricing is cyclical.
They have a downside, they have upside. So some enterprise controller company, they buy the NAND in the downside, they are selling the drive in the upside. But nowadays, there is no longer the cyclical price going up or stable, right? So very hard for enterprise controller company, you use it converting to selling the whole solution if you do not win hyperscaler or even NAND maker of the CSP customer. So I think our strategy is very simple. We winning NAND maker business and designing directly. We win hyperscaler customer in both U.S. and China. We also win CSP directly. But we do not make enterprise solution. We only sell controller and our firmware. We enable the module maker and the NAND maker. They sell and utilize our controller and the firmware, make enterprise solution, and selling to the customer. So this is where we are. We think -- we -- that is why building Silicon Motion ecosystem, working together and supporting the growing opportunity in both China and U.S.

**Daniel Yen** (Analysts):
I see. Very clear. Wallace, if I may follow up, how should we think about the overall competitive landscape on a controller in China right now? Just want to get your opinion.

**Chia-Chang Kou** (Executives):
So for enterprise, we really do not even. There is one or two basic company move to the IPO, but we do not see they are strong enough to compete in the long term, not just one technology or business model, right? I do not really see any threat from them. Even some also want to go overseas. Today, we feel pretty comfortable for our position and with our technology, and we have a very strong developing pipeline for both our PCIe Gen 5 as well as Gen 6.

**Daniel Yen** (Analysts):
I see. Yes. The second question from me is that since right now I think you are issuing the convertible bond, I want to ask if there is any change on your dividend policy potentially in the future? Also I think just overall, how should we think about your capital structure going forward? Do you have a target, any ratio you are looking at? I think this question is actually coming from some of the investors who subscribe your convertible bond, yes.

**Jason Tsai** (Executives):
Yes. Dividend and capital allocation certainly continues to be a priority. We increased our dividend a couple of weeks ago from $2 to $2.30 per ADS per year. We have had a history of increasing our dividend over the last 10 years or so, and our expectation is that we can continue to look at that strategically over time and continue to look at opportunities to raise that. The 3 priorities for us on capital return is dividend, share buybacks opportunistically, and then M&A as it makes sense, and that is unchanged. But certainly right now, working capital needs continue to increase as well. The CB raise puts us in a much better position to drive growth in our business with better working capital as well.

**Operator** (Operator):
Thank you. We have now reached the end of the question and answer session. I will now turn the conference back to Mr. Wallace Kou for closing comments.

**Chia-Chang Kou** (Executives):
Thank you everyone for joining us today and for your continuing interest in Silicon Motion. We will be attending several investor conferences over the next few months. The schedule of these events will be posted on the investor relationship section of our corporate website, and we look forward to speaking with you at these events. Goodbye for now.

**Operator** (Operator):
Thank you for your participation in today's conference. This does conclude the program. You may now disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SIMO_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 給 Q3 2026 營收指引：季增 15–20%，$519–541 百萬。（原話："we now expect revenue to grow 15% to 20% sequentially"）
- 2026-07-30｜CFO Jason Tsai｜guidance：Q3 毛利率指引 50–51%，理由為產品組合（MonTitan、PCIe 5 控制器貢獻增加）。（原話："increase sequentially to 50% to 51% in the September quarter"）
- 2026-07-30｜CFO Jason Tsai｜guidance：Q3 營業利益率指引 27.5–28.5%。（原話："grow substantially to 27.5% to 28.5%"）
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 稱年底退出時營業利益率可超過 30%。（原話："our operating margins can exceed 30% exiting this year"）
- 2026-07-30｜CEO Wallace Kou｜guidance：CEO 預期 2026 全年營收創高、年增逾 100%。（原話："record revenue in 2026, up more than 100% year-over-year"）
- 2026-07-30｜CEO Wallace Kou｜guidance：CEO 仍預期 2026 年智慧手機出貨下滑 10–15%，但自家行動業務預期強勁成長。（原話："smartphone unit to be down 10% to 15% in 2026"）
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 表示年底退出時 MonTitan 占營收 5–10%（分析師問的是 10%）。（原話："getting to that 5% to 10% coming from MonTitan"）
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 表示只指引未來一季，不評論 2027。（原話："We're not going to comment on '27 yet at this time."）
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 對 Ferri＋Boot Drive 2027 年占營收至少 1/3 的說法，答稱有此可能。（原話："I think that's certainly a possibility."）
- 2026-07-30｜CFO Jason Tsai｜margin：Q2 毛利率 50.2%，高於指引區間 48.5–49.5%，歸因新產品導入。（原話："as we capitalize on new product introductions."）
- 2026-07-30｜CFO Jason Tsai｜margin：Q2 營業利益率 23.1%，高於指引 21–22%，歸因營收與毛利率高於預期。（原話："margin was 23.1% and exceeded our guided range of 21% to 22%"）
- 2026-07-30｜CFO Jason Tsai｜margin：Q2 營收年增 127%、超出指引高標（$393–411 百萬）。（原話："coming in well above the high end of our guided range"）
- 2026-07-30｜CFO Jason Tsai｜margin：Q2 營業費用季增至 $122.1 百萬，原因為新控制器與解決方案開發、tape-out 費用、人力。（原話："Operating expenses increased sequentially to $122.1 million"）
- 2026-07-30｜CFO Jason Tsai｜margin：管理層對毛利率拆解：MonTitan 毛利率為加分（accretive），抵銷解決方案業務的毛利壓力。（原話："offset some of the margin pressure that we see from the"）
- 2026-07-30｜CFO Jason Tsai｜margin：長期毛利率目標維持 48–50%，Q2、Q3 因組合暫時高於此區間。（原話："I think we're still comfortable with the 48% to 50%."）
- 2026-07-30｜CFO Jason Tsai｜margin：CFO 提醒解決方案（Boot Drive）為控制器加 NAND，ASP 比純控制器高；MonTitan ASP 較低。（原話："it's controller plus NAND."）
- 2026-07-30｜CEO Wallace Kou｜margin：Ferri＋Boot Drive 解決方案 Q2 季增逾一倍，占總營收近 30%（去年同期 4%）。（原話："more than doubled sequentially and represent near 30%"）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 表示有信心達成今年 MonTitan 營收目標，並預期 2027 年顯著成長。（原話："I expect to see significant growth in 2027 and beyond"）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 預期 MonTitan 2026 下半年再增五家 Tier 1 客戶量產。（原話："ramp five additional Tier 1 customers in the second half"）
- 2026-07-30｜CEO Wallace Kou｜commitment：PCIe Gen 6 4nm 控制器預定今年 8 月完成 tape-out。（原話："completing the tape-out of our next-generation 4-nanometer"）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 表示 Gen 6 控制器預期為 2028 年重要成長動能。（原話："we're going to ramp much more revenue growth than this year."）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 表示 MonTitan 明年營收成長將明顯高於今年。（原話："we're definitely going to see much stronger growth in 2027."）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 稱 R&D 資源吃緊但會持續投資，2027 年成長將更強。（原話："proceeding more slowly than we anticipated 6 months"）
- 2026-07-30｜CEO Wallace Kou｜product：PCIe 4 到 PCIe 5 的轉換比六個月前預期的慢（OEM 以新 NAND 搭 PCIe 4 降 BOM）。（原話："QLC to become more meaningful until probably late '27"）
- 2026-07-30｜CEO Wallace Kou｜product：Edge SSD Q2 年增 40–45%。（原話："delivering 40% to 45% year-over-year growth."）
- 2026-07-30｜CFO Jason Tsai｜product：CFO 稱 QLC 要到 2027 年底至 2028 年才變得有份量，等 2Tb die 成本下降。（原話："This is an industry availability issue of the NAND."）
- 2026-07-30｜CFO Jason Tsai｜product：CFO 稱 QLC 延遲是 NAND 供應問題，非控制器問題。（原話："more than a dozen Tier 1 customers waiting for MonTitan"）
- 2026-07-30｜CEO Wallace Kou｜product：CEO 稱有逾十二家 Tier 1 客戶等待 MonTitan Gen 6 樣品。（原話："we set the market just a minimum 15% to 20%"）
- 2026-07-30｜CEO Wallace Kou｜product：被問 Gen 6 可觸及市場比例，CEO 答初始設定至少 15–20%。（原話："the opportunity in robotics may be larger"）
- 2026-07-30｜CEO Wallace Kou｜product：CEO 稱機器人的機會初步看可能大於車用；明年量仍小，2029–2030 才放大。（原話："the opportunity in robotics may be larger"）
- 2026-07-30｜CEO Wallace Kou｜competition：CEO 稱目前未見 NAND 原廠進入 Boot Drive 市場競爭。（原話："We do not see more competition and really to"）
- 2026-07-30｜CEO Wallace Kou｜competition：CEO 稱也未見模組廠進入競爭。（原話："we also don't see the competition from module maker either."）
- 2026-07-30｜CEO Wallace Kou｜competition：CEO 稱 NAND 原廠沒有 DRAM-less PCIe SSD 控制器，也不太可能為小市場投入研發。（原話："they do not have DRAM-less PCIe SSD controller"）
- 2026-07-30｜CEO Wallace Kou｜customer：CEO 稱 NVIDIA BlueField 的 Boot Drive 供應份額相當大，BlueField-4 時程不評論。（原話："a pretty large share for BlueField supply for the Boot"）
- 2026-07-30｜CEO Wallace Kou｜customer：CEO 稱 Boot Drive 客戶不只一家，與領先 GPU 公司的業務將更強。（原話："But definitely with the leading GPU company, it will go even"）
- 2026-07-30｜CEO Wallace Kou｜customer：CEO 稱低階智慧機份額不高，中國手機疲弱對自家影響相對小。（原話："That's why the impact for our business is relatively small."）
- 2026-07-30｜CEO Wallace Kou｜risk：CEO 預期 NAND 供給稀缺持續到約 2028 年新廠投產。（原話："We expect this scarcity to persist likely until 2028"）
- 2026-07-30｜CEO Wallace Kou｜risk：CEO 稱中國智慧手機市場因 LPDDR5 與儲存漲價而相當艱困。（原話："China smartphone market is very challenging due to the price"）
- 2026-07-30｜CEO Wallace Kou｜risk：CEO 表示 Boot Drive 成長的前提是能確保 NAND 供應。（原話："as long as we can secure the NAND supply"）
- 2026-07-30｜CFO Jason Tsai｜capital_allocation：Q2 現金由 $210.9 百萬降至 $181.8 百萬，原因含股利 $16.9 百萬與存貨增加。（原話："dividend payments of $16.9 million and an increase in"）
- 2026-07-30｜CFO Jason Tsai｜capital_allocation：CFO 稱新市場讓公司較不受消費性景氣循環影響。（原話："less subject to consumer cyclicality as these new wins scale"）

### 問答異常語氣（迴避／改口／保留）
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Neil Young 問 Q2 Boot Drive 與 Ferri 的營收拆分及 Q3 指引內含比重｜答法：CFO 明說不提供該細節，改談兩者都強勁與 backlog、訂單狀況
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Neil Young 問是否仍指引 MonTitan 年底 10% 營收 run rate｜答法：CFO 答仍在軌道上，但改述為 5% 至 10%，未直接確認 10%
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Sebastien Naji 問 Q2/Q3 是否已有 BlueField-4 貢獻｜答法：CEO 稱無法評論具體時程，只說跟隨客戶公布、對 BlueField 供應份額大
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Matthew Bryson 問 MonTitan 成功是否應上調長期毛利率（約 48–50%）｜答法：CFO 說仍 comfortable 於 48–50%，未鬆口上調，稱近期因組合高於此區間
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Suji Desilva 問 2027–2028 年季節性是否趨緩｜答法：CFO 稱不評論 2027，只指引一季

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
{"date":"20260710","verdict":"觀望","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"NAND 結構性短缺推動的高盈餘可延續至 2027–2028，且 SIMO GM 由 controller mix（非純 NAND 價）驅動、可守 48%+","columns":{"2Y 驗證點":"Q2–Q4 26 GM ≥ 48.5%（guide 中位）；契約價續漲","5Y 驗證點":"2027–2028 GM 未跌破 44%（正規化底）","具體數字門檻":"Q2 26 guide GM 48.5–49.5% 已上修；契約價 1H26 +100%、Q2 +70–75% QoQ","信息來源":"SIMO Q1 26 earnings call；TrendForce 2026-06；Phison CEO（2026 產能售罄）","漂移觸發":"連 2 季 GM &lt; 47% 且歸因 NAND 價回落 → 削弱；連 4 季 &lt; 46% → 反轉"}},{"id":"H2","text":"MonTitan 企業 eSSD 成為第二成長曲線，退出 2026 占營收 5–10%、2027–2028 放大","columns":{"2Y 驗證點":"Q3–Q4 26 enterprise SSD 占比爬坡","5Y 驗證點":"2028 MonTitan + boot drive 貢獻具規模、Gen6 客戶鎖定","具體數字門檻":"退出 2026 ≥ 5% floor；5 家 CSP 量產爬坡","信息來源":"Q1 26 call；SM8366/SM8388 產品頁；NVIDIA BlueField boot 設計贏","漂移觸發":"Q3 26 占比 &lt; 3% 連 2 季，或口徑改「2028 才有意義規模」→ 削弱"}},{"id":"H3","text":"市場維持成長股倍數（Fwd PE &gt; 25x）不 de-rate 回週期股倍數（Phison ~11x）","columns":{"2Y 驗證點":"Fwd PE FY+2 維持 ≥ 20x","5Y 驗證點":"倍數未收斂至歷史 7–22x 中樞","具體數字門檻":"FPE FY+2 ≥ 20x = 仍以 AI 儲存成長股定價","信息來源":"yfinance forward PE；分析師目標價追蹤","漂移觸發":"FPE FY+2 連 2 個月 &lt; 18x → 削弱（市場改以週期股定價）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"循環反轉 × 倍數壓縮：NAND 新產能 2027–2028 放量 → SIMO EPS 與 GM 回落 ＋ 市場改以週期股倍數定價（雙殺）","columns":{"對應假設":"H1 / H3","時間尺度":"🔥 中期（4–6 季，2027–2028）","監測指標":"TrendForce NAND ASP 月報、契約 vs 現貨價差；Fwd PE 相對歷史","警戒閾值":"NAND 現貨價領先鬆動 ＋ FPE FY+2 &lt; 18x 連 2 月"}},{"id":"R2","text":"客戶端量價背離：PC 出貨 −11.3%、機型降規 + OEM 庫存去化壓縮 client controller 出貨量","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1–2 季，2026H2）","監測指標":"client controller 出貨量 QoQ；OEM SSD 庫存週數；NB 出貨","警戒閾值":"client controller 出貨量連 2 季 QoQ 下滑"}},{"id":"R3","text":"中國自製化 × 出口管制：Maxio/InnoGrit 份額侵蝕 + 中國品牌轉本土控制器 + YMTC 實體清單合規風險","columns":{"對應假設":"H1 / H2","時間尺度":"🐢 長期（2+ 年，2027–2030）","監測指標":"中國客戶群份額；InnoGrit Gen6 進展；YMTC 出口管制狀態","警戒閾值":"任一大客戶 in-house/轉本土 ≥ 30% SIMO 份額；或 YMTC 供貨受出口管制限制"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE FY27 回落至 ≤18x（約 $180）；或 MonTitan 退出 2026 占營收 ≥7% 且 FY27 共識續上修確認第二曲線；或 through-cycle EPS 站穩 $10+","irr_base_pct":-4.9,"ev5y_pct":-16.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"衛星","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.6,"ev5y_pct":-16.8,"irr_base_pct":-4.9,"max_dd_pct":-70.0,"bull_5y_price":480.0,"bear_5y_price":120.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE FY27 回落至 ≤18x（約 $180）；或 MonTitan 退出 2026 占營收 ≥7% 且 FY27 共識續上修確認第二曲線；或 through-cycle EPS 站穩 $10+","price_at_dd":324.26,"archetype":"品質複利成長","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
