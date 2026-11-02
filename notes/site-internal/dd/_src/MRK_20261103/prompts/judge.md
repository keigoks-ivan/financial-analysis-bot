你是 stock-analyst **v20 判斷 agent**，標的 MRK（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MRK","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_total_worldwide_sal","label":"營收（GAAP，Total Worldwide Sales）","value":16607,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司新聞稿 merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/；細項損益表引自 SEC 8-K exhibit 99.1（sec.gov/Archives/edgar/data/0000310158/000110465926090045/tm2621496d1_ex99-1.htm）"},"note":"consensus 約 $16.41B，實際 $16.607B 為 beat（來源：web_search 彙整分析師預估，非官方一手數字）"},{"id":"f_kpi1_non_gaap_non_gaap_operat","label":"Non-GAAP 稅前利益率（無法拆出獨立 non-GAAP operating income，新聞稿只揭露 non-GAAP pretax income）","value":3.3,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"SEC 8-K exhibit 99.1 reconciliation 表：non-GAAP pretax income $550M / 營收 $16,607M"},"note":"查無官方逐項 consensus 對照"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":-2.6,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"yfinance quarterly_income_stmt（Operating Income -$433M / Revenue $16,607M）"},"note":"查無官方逐項 consensus 對照"},{"id":"f_kpi5_2026_guidance","label":"管理層全年 2026 guidance","value":null,"period":"公告於 2026-08-04（隨 Q2 FY2026 財報同步更新）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"公告於 2026-08-04（隨 Q2 FY2026 財報同步更新）","citation":"公司新聞稿 merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/"},"note":"營收 guidance 上調：$66.3B–$67.3B（前次 $65.8B–$67B）；Non-GAAP EPS guidance 大幅下修：$2.66–$2.76（前次 $5.04–$5.16），下修原因為 Terns（$2.43/股）與 Cidara 收購一次性費用認列，非營運惡化","needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mrk_gross_margin_pct","label":"MRK 毛利率","value":71.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_operating_margin_pct","label":"MRK 營業利益率","value":0.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_fcf_margin_pct","label":"MRK FCF 利潤率","value":18.72,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_pfe_gross_margin_pct","label":"PFE 毛利率","value":73.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pfe_operating_margin_pct","label":"PFE 營業利益率","value":26.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pfe_fcf_margin_pct","label":"PFE FCF 利潤率","value":17.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bmy_gross_margin_pct","label":"BMY 毛利率","value":69.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bmy_operating_margin_pct","label":"BMY 營業利益率","value":29.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bmy_fcf_margin_pct","label":"BMY FCF 利潤率","value":18.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abbv_gross_margin_pct","label":"ABBV 毛利率","value":71.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_operating_margin_pct","label":"ABBV 營業利益率","value":33.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_fcf_margin_pct","label":"ABBV FCF 利潤率","value":28.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":4477,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"yfinance quarterly_cashflow（Operating Cash Flow $5,370M − CapEx $893M）；FCF margin = 4477/16607 = 27.0%"},"note":"查無官方逐項 consensus 對照"},{"id":"f_kpi4_sbc","label":"SBC 占營收 %","value":1.79,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"yfinance quarterly_cashflow（Stock Based Compensation $298M / Revenue $16,607M）；因 GAAP 營業利益為負，改以占營收表示"},"note":"查無官方逐項 consensus 對照"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":148.56,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":33.08,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":55.33,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.64,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.65 → 2.72）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.98,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.23 → 9.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.78,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.2 → 10.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.72,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.14,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.12,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-0.73,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 2.74 → 2.72（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":150.06,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝18.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":18.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.44,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.13,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":54.62,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 2.72，分子＝快照價 148.57","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.289,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":46770.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 53911.0、現金 7141.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":2467.17,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":413280.67,"period":"2026-11-03","unit":"USD m","basis":"市值 366510.67 ＋ 淨負債 46770.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":67186.2,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":69584.64,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.15,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 148.66 / W52 121.86 / W104 102.52 / W250 98.98 / W250 13週斜率 1.28%"},{"id":"f_ma_w52","label":"52 週均線","value":121.86,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":102.52,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":98.98,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.28,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Keytruda/Keytruda Qlex 合併銷售 2026Q1 年增 12%、2026Q2 為 83.6 億美元年增 5%，仍是 PD-1 領域龍頭；對手 BMS Opdivo 2026Q1 銷售 21.5 億美元年減 5%，AstraZeneca Imfinzi 2026Q1 銷售 16.9 億美元年增 30%","source":"Yahoo Finance - Can Keytruda Sustain Merck's Growth in the Second Half of 2026?","url":"https://finance.yahoo.com/healthcare/articles/keytruda-sustain-mercks-growth-second-140000696.html","excerpt":"Combined global sales of Keytruda/Keytruda Qlex grew 12% in the first quarter of 2026... Keytruda/Keytruda Qlex sales were $8.4 billion (5% growth) in the second quarter of 2026... Opdivo generated sales of $2.15 billion in the first quarter of 2026, down 5% year over year... AstraZeneca's Imfinzi generated sales of $1.69 billion in the first quarter of 2026, up 30% year over year","as_of":"2026-08-01","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Keytruda 生物相似藥已於 2025 年在阿根廷等小型國際市場上市，2026 年將擴大至更多小型市場，但公司預期 2026 年生物相似藥侵蝕影響輕微；美國複方專利到 2028 年 12 月到期，兩項組成物專利延至 2029 年，歐洲市場專屬權到 2031 年，實質性衝擊預期在 2028-2029 年才會出現","source":"综合搜尋摘要（含 Merck 10-K FY2025、Pharmacy Times）","url":"https://www.pharmacytimes.com/view/soaring-off-the-patent-cliff-preparing-for-the-next-wave-of-oncology-biosimilars","excerpt":null,"as_of":"2026-02-24","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","triggers"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Gardasil 2026Q1 銷售暴跌 22% 至 10.7 億美元，中國市場（佔美國以外銷量 60-70%）需求因經濟放緩疲弱，且面臨中國本土 HPV 疫苗以十分之一價格搶市；Merck 已暫停對中國經銷夥伴智飛生物的出貨以消化通路庫存","source":"BioPharma Dive / Fierce Pharma / Yahoo Finance 綜合搜尋摘要","url":"https://www.fiercepharma.com/pharma/merck-puts-temporary-kibosh-gardasil-shipments-china-local-demand-hpv-vaccine-nosedives","excerpt":"Gardasil sales plunged 22% to $1.07 billion in the first quarter of 2026... China... accounting for 60% to 70% of all sales outside the U.S.... The shot is also facing competition from Chinese companies that sell HPV vaccines at one-tenth of Gardasil's price.","as_of":"2026-05-01","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"皮下劑型卡位戰：BMS 的 Opdivo Qvantig 皮下劑型於 2024 年 12 月搶先上市，早於 Merck 的 Keytruda Qlex（2025 年 9 月上市）；2026Q1 Opdivo Qvantig 營收年增逾 200%（主因 2025 年上市後需求墊高），Keytruda Qlex 則在 2026 上半年貢獻 5.9 億美元","source":"Yahoo Finance / BioPharma Dive 綜合搜尋摘要","url":"https://www.biopharmadive.com/news/merck-keytruda-subcutaneous-cancer-sales-drug-delivery/801889/","excerpt":"Merck launched its subcutaneous Pembrolizumab/Hyaluronidase formulation in September 2025, while BMS launched its Nivolumab/Hyaluronidase-nvhy SC formulation in December 2024... Opdivo Qvantig revenues increased more than 200% during the first quarter of 2026... Keytruda Qlex... contributed $590 million during the first half of 2026.","as_of":"2026-08-01","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Merck 的三大藥品批發商客戶（McKesson、AmerisourceBergen、Cardinal Health）合計占應收帳款相當高比重，屬產業結構性集中，非新增惡化","source":"Merck & Co., Inc. Form 10-K FY2022","url":"https://www.sec.gov/Archives/edgar/data/310158/000162828023005061/mrk-20221231.htm","excerpt":"The Company's customers with the largest accounts receivable balances are: McKesson Corporation, AmerisourceBergen Corporation and Cardinal Health, Inc., which represented approximately 21%, 20% and 13%, respectively, of total accounts receivable at December 31, 2022.","as_of":"2022-12-31","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Gardasil 在中國因通路庫存偏高＋需求疲軟，Merck 自2025年2月暫停出貨，管理層預期2026年銷售不會回升；文章判斷中國經濟放緩屬暫時性因素，但同時提到日本需求下滑趨勢會持續，顯示週期性與結構性因素並存","source":"Yahoo Finance - Will Weak Gardasil Sales Continue to Weigh on MRK's Top Line in 2026?","url":"https://finance.yahoo.com/news/weak-gardasil-sales-continue-weigh-133500094.html","excerpt":"Lower demand in China resulted in above-normal channel invent","as_of":"2026-03-09","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Merck 2025年2月起暫停對中國出貨；2026年4月與中國經銷夥伴（智飛）簽署修訂後供貨合約；2026年第2季開始恢復有限出貨，但該合約相關營收預期2026年內仍不重大——顯示去化庫存＋需求回補為多季期的結構性過程，非單一季度週期性波動","source":"Merck & Co., Inc. Form 10-Q FY2026 Q2 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Keytruda（占公司腫瘤營收核心）美國組成物專利2028年到期、用法專利至2029年11月，這是結構性、時程明確的懸崖，非週期性問題；公司揭露此為重大風險因子","source":"Merck & Co., Inc. Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/310158/000031015826000063/mrk-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","valuation","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"參議員 Hassan（參院財政委員會健保小組資深議員）對 Merck 的 Keytruda 專利策略與 product hopping（劑型轉換）發起國會質詢，指控其藉此延遲低價競爭產品上市","source":"Senator Hassan press release / ICIJ 'Cancer Calculus' investigation","url":"https://www.hassan.senate.gov/news/press-releases/-senator-hassan-presses-big-pharma-company-on-anti-competitive-practices-that-boost-profits-at-the-expense-of-cancer-patients","excerpt":"delay other companies from selling lower cost versions","as_of":"2026-09-13","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Merck 於 2024年6月收到 DOJ 依 False Claims Act 發出的民事調查要求(CID)，就 Steglatro、Januvia 在 Medicaid 藥物回扣計畫下的價格申報，以及病患協助計畫的反回扣法遵規範進行調查","source":"Merck & Co. Form 10-Q (FY2026)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":null,"as_of":"2024-06","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"巴爾的摩市於2023年3月對 Merck 子公司提起反壟斷集體訴訟，指控其利用小兒疫苗市場的壟斷力進行搭售，維持 RotaTeq（輪狀病毒疫苗）市場的壟斷地位並收取超額定價","source":"Merck & Co. Form 10-Q / SEC filings (litigation disclosure)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":null,"as_of":"2023-03","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Merck 對 HHS 提起訴訟，主張 IRA（降低通膨法案）的 Medicare 藥價強制議價機制違憲；Januvia／Janumet 已分別於2023年、2025年被選入該議價名單","source":"The Philadelphia Inquirer","url":"https://www.inquirer.com/business/merck-inflation-reduction-act-lawsuit-20231130.html","excerpt":null,"as_of":"2023-11-30","retrieved_at":"2026-09-29","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"默克與美國商務部達成協議，將 Section 232 關稅延後三年課徵，換取默克在美國增加投資、把製造遷回美國。","source":"Merck 8-K exhibit 99-1 (SEC filing)","url":"https://www.sec.gov/Archives/edgar/data/310158/000110465926009495/tm264564d1_ex99-1.htm","excerpt":"The Company reached an understanding with the U.S. Department of Commerce to delay Section 232 tariffs for three years","as_of":"2026-02-03","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"川普政府於 2026-04-02 發布 Section 232 公告，對專利藥品及其原料進口課高達 100% 關稅；默克（Merck Sharp & Dohme）被列在 Annex III 的 17 家指名大廠名單中，適用公告發布後 120 天生效（即 2026-07-31），其餘廠商則自 2026-09-29 生效。","source":"白宮 Section 232 藥品關稅公告 Annex 分析（法律事務所/貿易媒體報導彙整，如 McDermott Will & Emery、Mallory Group）","url":"https://www.mcdermottlaw.com/insights/section-232-pharmaceutical-tariffs-what-importers-need-to-know/","excerpt":null,"as_of":"2026-04-02","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"默克執行長 Rob Davis 向國會與川普政府示警，若對美中藥廠交易（dealmaking）設限過嚴，恐使美國自身承受後果；顯示默克在中國授權/併購交易上有政策限制風險暴露。","source":"Endpoints News","url":"https://endpoints.news/merck-ceo-cautions-congress-on-imposing-limits-on-chinese-dealmaking/","excerpt":null,"as_of":"2026-07-22","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"美國眾議院中國問題特別委員會主席 Moolenaar 於 2026-06-30 去函 Merck 與 AbbVie，要求說明在中國（含新疆與解放軍附屬醫院）進行臨床試驗的場址審查、資料保護與安全標準，7/17 前需回覆。","source":"Investing.com (Reuters) — US House committee opens investigation into Merck, AbbVie China drug trials","url":"https://www.investing.com/news/stock-market-news/exclusiveus-house-committee-opens-investigation-into-merck-abbvie-china-drug-trials-4767250","excerpt":"Rep. John Moolenaar, a Michigan Republican who chairs the House Select Committee on China, signed the Monday-dated letters calling on both companies to submit information by July 17 covering how they vet trial locations, protect data, and uphold safety standards — with particular scrutiny on sites in Xinjiang and at hospitals connected to China's military.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Merck 自 2005 年起在中國贊助或參與 224 項臨床研究，其中至少 31 項位於新疆、40 項在解放軍附屬醫院或醫療機構進行，成為本次國會調查的具體規模依據。","source":"GuruFocus — Merck (MRK) Faces National Security Scrutiny Over China Trials","url":"https://www.gurufocus.com/news/8938913/merck-mrk-faces-national-security-scrutiny-over-china-trials?mobile=true","excerpt":"Merck has sponsored or collaborated on 224 clinical studies in China since 2005, including at least 31 in Xinjiang and 40 at military-affiliated hospitals and medical centers.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Keytruda(腫瘤免疫藥)為Merck最大營收段，H1 2026 銷售 $16.40B，年增約4.2%；Q1 +8%、Q2 +5%","source":"Yahoo Finance - Can Keytruda Sustain Merck's Growth in the Second Half of 2026?","url":"https://finance.yahoo.com/healthcare/articles/keytruda-sustain-mercks-growth-second-140000696.html","excerpt":"Keytruda recorded sales worth $16.40 billion in the first half of 2026, up almost 4.2% year over year.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Gardasil(HPV疫苗)段H1 2026合併銷售年減9%，主因中國、日本需求疲弱","source":"SEC 10-Q FY2026 Q2 (Merck & Co.)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":"Combined worldwide sales of Gardasil and Gardasil 9 declined 9% in the first six months of 2026 primarily driven by lower demand in China and in Japan.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"管理層不預期Gardasil在2026年好轉，2026全年財測未計入任何中國出貨（因中國合作夥伴智飛通路庫存過高，先前已暫停出貨至2025年底）","source":"Fierce Pharma - Merck halts Gardasil shipments to China","url":"https://www.fiercepharma.com/pharma/merck-puts-temporary-kibosh-gardasil-shipments-china-local-demand-hpv-vaccine-nosedives","excerpt":"Merck decided to temporarily halt shipments of Gardasil in China to allow Zhifei to burn down existing inventory. The company didn't assume any Gardasil shipments to China in its 2026 full-year guidance, after previously pausing them through the end of 2025.","as_of":"2026-02-01","retrieved_at":"2026-09-29","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"動物保健段H1 2026營收 $3.566B，年增10%（剔除匯率影響+6%）；畜牧+12%、寵物用藥+8%，主要靠Bravecto系列及新品","source":"Merck.com - Our Q2 2026 financial results","url":"https://www.merck.com/stories/our-q2-2026-financial-results/","excerpt":"For the first half of 2026, total Animal Health revenue was $3.566 billion, representing 10% growth, or 6% excluding foreign exchange effects.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Winrevair（肺動脈高壓新藥）H1 2026銷售年增81%、Q2單季+75%，美國滲透持續、日本歐洲剛起步放量；分析師共識峰值銷售估$8-8.5B","source":"SEC 10-Q FY2026 Q2 (Merck & Co.)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":"Winrevair sales rose 75% and 81% in the second quarter and first six months of 2026, respectively, largely due to continued uptake in the U.S. and early launch uptake in certain international markets, particularly in Japan and Europe.","as_of":"2026-06-30","retrieved_at":"2026-09-29","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"Keytruda 2028年專利懸崖：美國核心化合物專利2028到期，涉及逾$25B年化腫瘤營收；2026年生物相似藥侵蝕預期輕微（僅阿根廷等小型市場上市），但Medicare藥價協商新折扣價將於2028年1月生效，市場預期Keytruda美國銷售2027-28見頂後轉降","source":"Patsnap - Keytruda patent cliff 2028: Merck's strategy","url":"https://www.patsnap.com/resources/blog/articles/keytruda-patent-cliff-2028-mercks-strategy/","excerpt":"Keytruda's 2028 patent cliff puts more than $25 billion in annual oncology revenue at risk, with the drug's core composition-of-matter patent in the United States expected to expire in 2028.","as_of":"2026-01-01","retrieved_at":"2026-09-29","affects":["thesis.R","valuation","triggers","moat_trend"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"PD-1/PD-L1（Keytruda所屬的免疫檢查點抑制劑類別）全球市場規模預估2026年約$73.87B，至2033年成長到$245.25B，CAGR約18.7%","source":"Future Market Insights - PD-1/PDL-1 Inhibitor Market Size, Share & Forecast to 2036","url":"https://www.futuremarketinsights.com/reports/pd1-pdl1-inhibitors-market","excerpt":"the market is estimated to be valued at USD 73.87 billion in 2026 and is expected to reach USD 245.25 billion by 2033, exhibiting a CAGR of 18.7% from 2026 to 2033.","as_of":"2026-01-01","retrieved_at":"2026-09-29","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"中國 Akeso 與 Summit Therapeutics 合作開發的 PD-1xVEGF 雙特異性抗體 ivonescimab，在晚期肺癌頭對頭試驗中擊敗 Keytruda，是 Keytruda 上市十年來首次在此類試驗中落敗。","source":"BioPharma Dive - \"Merck, facing threat to Keytruda, buys into new kind of cancer immunotherapy\"","url":"https://www.biopharmadive.com/news/merck-lanova-pd1-vegf-bispecific-cancer-drug-deal/732906/","excerpt":"This year, one such drug, ivonescimab, from China-based Akeso and development partner Summit Therapeutics, bested Merck's Keytruda in a late-stage trial in lung cancer — the first time that's happened since Keytruda's arrival a decade ago.","as_of":"2024-11-14","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Merck 支付 5.88 億美元現金收購中國 LaNova Medicines 的同類 PD-1xVEGF 雙特異性抗體技術，作為 Keytruda 面臨替代技術與專利懸崖前的下一代免疫療法布局。","source":"BioPharma Dive - \"Merck, facing threat to Keytruda, buys into new kind of cancer immunotherapy\"","url":"https://www.biopharmadive.com/news/merck-lanova-pd1-vegf-bispecific-cancer-drug-deal/732906/","excerpt":"Merck is paying China-based biotech LaNova Medicines $588 million for the same type of bispecific antibody drug that recently bested Keytruda in a clinical trial.","as_of":"2024-11-14","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"FDA 於 2025 年 9 月核准 Keytruda Qlex（皮下注射固定劑量合併 pembrolizumab + berahyaluronidase alfa），涵蓋原 Keytruda 已核准的實體瘤適應症，為 Merck 因應生物相似藥與替代療法威脅的產品調整策略之一。","source":"PharmaVoice / Patsnap coverage of Merck's Keytruda strategy (via search synthesis)","url":null,"excerpt":"Keytruda Qlex, which was initially approved by the FDA in September 2025, is approved in the U.S. in solid tumor indications approved for Keytruda.","as_of":"2025-09","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Cipla 美國子公司已取得 Qilu Pharmaceutical pembrolizumab 生物相似藥 QL2107 的美國獨家銷售權，搶在 Keytruda 核心專利於 2028 年 12 月到期前卡位；報導指出 Keytruda 的生物相似藥倒數計時聲量正在變大。","source":"GuruFocus - \"Merck's $8.4 Billion Keytruda Fortress Gets a 2028 Warning\"","url":"https://www.gurufocus.com/news/9066847/mercks-84-billion-keytruda-fortress-gets-a-2028-warning","excerpt":"Cipla's U.S. subsidiary secured exclusive American commercialization rights to Qilu Pharmaceutical's proposed pembrolizumab biosimilar, QL2107, ahead of Keytruda's expected 2028 core patent expiration.","as_of":"2026-09-03","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"0","claim":"產業分析指出，單株抗體（含次世代 ADC、雙特異性抗體、CAR-T）在 2026 年管線營收預測持續強勁成長，反觀部分被視為顛覆性替代技術的基因療法、mRNA 與其他細胞療法管線營收預測已「停滯」，尚未撼動抗體類藥物的主導地位。","source":"BioPharm International - \"The New BioPharma Playbook: Seven Technologies Defining Drug Development in 2026\"","url":"https://www.biopharminternational.com/view/the-new-biopharma-playbook-seven-technologies-defining-drug-development-in-2026","excerpt":"The dominance of monoclonal antibodies and other therapeutic proteins is likely to continue in 2026 and beyond, however new modalities, such as cell and gene therapies, are getting traction and may eventually dethrone the more \"classic\" biologics. However, analysis of projected pipeline revenues reveals that established new modalities (mAbs, ADCs, BsAbs, recombinants, and CAR-T) continue to demonstrate robust growth, whereas some emerging modalities (gene, mRNA, and other cell therapies) have stalled.","as_of":"2026","retrieved_at":"2026-09-29","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#5","axis":"substitute_technology","section":"coverage","direction":"-","claim":"新創公司 Crescent Biopharma 正開發 PD-1xVEGF 雙特異性抗體 CR-001，其定位明確是要取代 pembrolizumab 作為免疫腫瘤療法的新骨幹用藥，相關臨床試驗於 2026 年啟動。","source":"DIMA Biotechnology - \"2026 ASCO Target Review (Part II): Bispecific and Multispecific Antibodies and Immunotherapy Combinations\"","url":"https://www.dimabio.com/blog/2026-asco-bispecific-antibody-targets","excerpt":"Crescent Biopharma is developing CR-001, a PD-1 x VEGF bispecific antibody designed to bind both PD-1 and VEGF, which has potential to replace pembrolizumab (Keytruda) as the foundational immuno-oncology backbone. Clinical trials for CR-001, CR-002 and CR-003 were anticipated to initiate in 2026 along with the first ADC combination trial.","as_of":"2026","retrieved_at":"2026-09-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Merck 與美國政府達成協議，計畫在美國推出「直接對病人銷售」(direct-to-patient) 通路，以平價提供關鍵產品給符合資格的病人，屬 2026年2月與川普政府藥價協議的一部分。","source":"Merck & Co., Inc. SEC Form 8-K, Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/310158/000110465926009495/tm264564d1_ex99-1.htm","excerpt":"the Company plans to provide key products through a direct-to-patient program at affordable prices for eligible patients in the U.S.","as_of":"2026-02-03","retrieved_at":"2026-09-29","affects":["thesis.H","thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"美國衛生部 (HHS) 於2026年1月27日發布新指引，釐清藥廠如何在不違反聯邦反回扣法的前提下，直接對病人（含 Medicare／Medicaid 參保人）提供低價處方藥，為產業性的直接對消費者(DTC)通路轉移提供法規基礎；聯邦政府另於2026年2月5日上線 TrumpRx.gov 作為導流入口，把病人導向藥廠自營 DTC 網站。","source":"HHS.gov press release; TrumpRx (Wikipedia); Galen Growth analysis","url":"https://www.hhs.gov/press-room/oig-clears-path-for-lower-cost-prescription-drugs.html","excerpt":null,"as_of":"2026-01-27","retrieved_at":"2026-09-29","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Merck Q3 2026 上調全年 non-GAAP EPS 指引至 $2.77–2.82，營收指引收窄","source":"Finviz: Merck reports Q3 revenue of $18.1 billion, raises 2026 earnings guidance","url":"https://finviz.com/news/411712/merck-reports-q3-revenue-of-181-billion-raises-2026-earnings-guidance","excerpt":"Merck increased its 2026 earnings per share forecast to a range of $2.77 to $2.82, compared with its previous guidance of $2.66 to $2.76. The revised range is above analysts’ consensus estimate of $2.65 per share.","as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 載 MRK 分析師平均目標價約 $134.56，Moderate Buy（2026-08 初）","source":"MarketBeat: Guggenheim forecasts strong price appreciation for Merck","url":"https://www.marketbeat.com/instant-alerts/guggenheim-forecasts-strong-price-appreciation-for-merck-co-inc-nysemrk-stock-2026-08-05/","excerpt":"Analyst's Opinion2.7 / 5Analyst RatingModerate Buy Consensus Rating Merck & Co., Inc. has received a consensus rating of Moderate Buy. The company's average rating score is 2.59, and is based on no strong buy ratings, 17 buy ratings, 9 hold ratings, and 1 sell rating. Upside/Downside The consensus price target for Merck & Co., Inc.","as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Merck 2026-03 同意以約 67 億美元收購 Terns Pharmaceuticals，5 月完成；後續申報總額 68 億美元，認列 57 億美元 R&D 費用（主要為收購的 IPR&D）。另 2026-01 收購 Cidara、2026-07 以約 6.5 億美元收購 TARGAN。","source":"Merck 10-Q FY2026（搜尋摘要）／Merck Terns tender offer 新聞稿","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露 Cronin v. Merck 證券集體訴訟（Gardasil 中國需求陳述），期間 2023-10-26 至 2025-02-03；修正訴狀 2026-02-20 提出，駁回動議 2026-05-01 到期。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/310158/000031015826000063/mrk-20251231.htm","excerpt":"Plaintiff alleges that Merck violated federal securities laws by making materially false and misleading statements and material omissions regarding demand for Gardasil/Gardasil 9 in China.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"Q2 2026 財報：FDA 核准 Lipfendra（enlicitide，口服 PCSK9）；Keytruda+Keytruda Qlex Q2 銷售 84 億美元；Winrevair Q2 5.88 億美元。","source":"Merck Q2 2026 業績新聞稿（搜尋摘要）","url":"https://www.merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"Emend（aprepitant）口服懸液 125mg 單劑套組 Class II 召回 D-0241-2026，原因為可能含金屬微粒，2025-12-12 起、仍進行中。","source":"recallcheck.net 召回清單（搜尋摘要）","url":"https://recallcheck.net/drug-recalls/2647","excerpt":null,"as_of":"2025-12-12","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 8 份，含重大項目者 2 份（5.02 董事／高管異動未計入該統計外之項目，2025-12 與 2026-05 為 8.01 發債）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000310158&type=8-K","excerpt":"2025-11-03 至 2026-11-03 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Merck 2026-03 同意以約 67 億美元收購 Terns Pharmaceuticals，5 月完成；另 2026-01 收購 Cidara、2026-07 以約 6.5 億美元收購 TARGAN。","source":"Merck 10-Q FY2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Cronin v. Merck 證券集體訴訟（Gardasil 中國需求），另有 Daniel 與 Kistenmacher 兩件衍生訴訟；駁回動議 2026-05-01 到期。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/310158/000031015826000063/mrk-20251231.htm","excerpt":"Plaintiff alleges that Merck violated federal securities laws by making materially false and misleading statements and material omissions regarding demand for Gardasil/Gardasil 9 in China.","as_of":"2026-02-24","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"FDA 核准 Lipfendra（enlicitide）；Keytruda+Padcev MIBC 優先審查中；Winrevair sBLA 2026-02 受理；Welireg+Keytruda PDUFA 2026-06-19 結果未查到。","source":"Merck Q2 2026 業績新聞稿／10-Q（搜尋摘要）","url":"https://www.merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"Emend 口服懸液套組 Class II 召回 D-0241-2026（可能含金屬微粒），2025-12-12。未見 2026 警告信。","source":"recallcheck.net 召回清單（搜尋摘要）","url":"https://recallcheck.net/drug-recalls/2647","excerpt":null,"as_of":"2025-12-12","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單中未見 Item 4.02（財報不可信賴／重編）；搜尋亦未見近期 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000310158&type=8-K","excerpt":"2025-11-03 至 2026-11-03 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MRK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.31,"operating_margin_pct":0.87,"fcf_margin_pct":18.72,"rd_intensity_pct":53.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"PFE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":73.18,"operating_margin_pct":26.72,"fcf_margin_pct":17.25,"rd_intensity_pct":17.35},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFE","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"BMY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.24,"operating_margin_pct":29.19,"fcf_margin_pct":18.56,"rd_intensity_pct":21.1},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ABBV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.48,"operating_margin_pct":33.94,"fcf_margin_pct":28.28,"rd_intensity_pct":15.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"MRK"},"financial_history":{"ticker":"MRK","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":59283000000.0,"revenue_yoy_pct":null,"gross_margin_pct":70.63,"operating_margin_pct":30.84,"net_income":14519000000.0,"diluted_eps":5.71,"free_cash_flow":14707000000.0,"fcf_margin_pct":24.81,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":60115000000.0,"revenue_yoy_pct":1.4,"gross_margin_pct":73.17,"operating_margin_pct":4.91,"net_income":365000000.0,"diluted_eps":0.14,"free_cash_flow":9143000000.0,"fcf_margin_pct":15.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":64168000000.0,"revenue_yoy_pct":6.74,"gross_margin_pct":76.32,"operating_margin_pct":31.51,"net_income":17117000000.0,"diluted_eps":6.74,"free_cash_flow":18096000000.0,"fcf_margin_pct":28.2,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":65011000000.0,"revenue_yoy_pct":1.31,"gross_margin_pct":74.8,"operating_margin_pct":34.01,"net_income":18254000000.0,"diluted_eps":7.28,"free_cash_flow":12360000000.0,"fcf_margin_pct":19.01,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MRK/MRK_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Merck & Co., Inc.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Welcome to the Merck & Co., Inc., Rahway, N.J., USA Third Quarter Sales and Earnings Conference Call. [Operator Instructions] This call is being recorded. If you have any objections, you may disconnect at this time.
I would now like to turn the call over to Mr. Peter Dannenbaum, Senior Vice President, Investor Relations. Sir, you may begin.

**Peter Dannenbaum** (Executives):
Thank you, Julie, and good morning, everyone. Welcome to the Third Quarter 2026 Conference Call for Merck & Co., Inc., Rahway, N.J., USA. Speaking on today's call will be Rob Davis, Chairman and Chief Executive Officer; Caroline Litchfield, Chief Financial Officer; and Dr. Dean Li, President of Research Labs.
Before we get started, I'd like to point out that we have items in our GAAP results, such as acquisition-related charges, restructuring costs and certain other items, that we have excluded from our non-GAAP results. There is a reconciliation in our press release. I will also remind you that some of the statements that we make today may be considered forward-looking statements within the meaning of the safe harbor provision of the U.S. Private Securities Litigation Reform Act of 1995. Such statements are made based on the current beliefs of our company's management and are subject to significant risks and uncertainties. If our underlying assumptions prove inaccurate or uncertainties materialize, actual results may differ materially from those set forth in the forward-looking statements.
Our SEC filings, including Item 1A in the 2025 10-K, identify certain risk factors and cautionary statements that could cause the company's actual results to differ materially from those projected in any of our forward-looking statements made this morning. Merck & Co., Inc. Rahway, N.J., USA, undertakes no obligation to publicly update any forward-looking statements.
During today's call, a slide presentation will accompany our speakers' prepared remarks. These slides, along with the earnings release, today's prepared remarks and our SEC filings, are all posted to the Investor Relations section of our company's website.
With that, I'd like to turn the call over to Rob.

**Robert Davis** (Executives):
Thank you, Peter. Good morning, and thank you for joining today's call. 2026 continues to be a year of substantial progress for our company. We're executing well on all fronts, demonstrated particularly by the many new product launches now successfully underway and the important clinical milestones we're achieving that are further derisking the substantial long-term opportunity of our late-phase pipeline. This momentum extends across multiple therapeutic areas and modalities, and there is much more to come with numerous significant readouts still to occur over the coming years.
I'm very pleased that the disciplined execution of our strategy over the past several years is increasingly translating into meaningful clinical, regulatory and commercial results. The breadth of these achievements strengthens my confidence in the future of our company and our ability to deliver long-term value for patients and shareholders.
Turning to our third quarter results. We delivered solid performance with revenue of $18.1 billion, reflecting increased contributions from new products as well as strength in Oncology and Animal Health. Caroline will discuss our results and the full year outlook in greater detail in a moment.
We also achieved several important clinical and regulatory milestones. In Oncology, last weekend's ESMO meeting showcased potential practice-changing advances for several innovative programs, highlighted by the first positive Phase III results from our expansive global TroFuse program for sac-TMT in advanced or recurrent endometrial cancer. Additional data shared at the meeting from our partner, Kelun, further support the potential of sac-TMT in lung cancer and other tumor types. And we are encouraged by the landmark validation of a therapeutic cancer vaccine with positive Phase III data presented for intismeran autogene as an adjuvant treatment for certain patients with melanoma. This new approach may offer a tangible opportunity to change the trajectory of a patient's cancer. In Ophthalmology, we presented results from the BRUNELLO study evaluating remigromig in diabetic macular edema, a significant milestone for our rapidly advancing retinal disease portfolio. And finally, in Immunology, we presented encouraging Phase IIb results in HS and look forward to advancing our TL1A development program.
This year's clinical and commercial progress underlines the ongoing transformation of our business and provides us with greater visibility into the trajectory of our emerging and expansive new product portfolio. The opportunity we have to drive strong long-term growth beyond the KEYTRUDA LOE period is becoming increasingly clear as we achieve these scientific and commercial milestones. As we look ahead, we'll remain focused on successfully executing our launches, broadening and advancing our pipeline and making meaningful investments to realize the full potential of these opportunities. I want to recognize and thank our dedicated global teams for their ongoing commitment to delivering value for patients, shareholders and all of our stakeholders.
And now I'll turn the call over to Caroline.

**Caroline Litchfield** (Executives):
Thank you, Rob. Good morning. As Rob noted, we delivered solid performance in the quarter, driven by increasing contributions from our compelling array of important new products and continued strength in Oncology and Animal Health. Strong commercial and operational execution continues to propel our near-term performance, while we invest to optimize our launches and advance our broad and deep pipeline to create long-term value for patients, customers and shareholders.
Now turning to our third quarter results. Total company revenues were $18.1 billion, an increase of 5%, or 4% excluding the impact of foreign exchange. The following revenue comments will be on an ex-exchange basis. In Oncology, sales of the KEYTRUDA family of products, which includes KEYTRUDA and KEYTRUDA QLEX, increased 6% to $8.6 billion, with global growth driven by strong uptake in earlier-stage cancers and continued robust demand for metastatic indications. Key contributors to growth included strong utilization in tumors that primarily affect women, particularly cervical and breast cancers, as well as increased use of KEYTRUDA plus PADCEV in urothelial cancer. We also saw continued uptake in earlier-stage head and neck cancer.
As expected, the timing of U.S. customer purchases last year created a headwind to growth, but this was largely offset by an increase in channel inventory, which we expect to unwind in the fourth quarter. Sales of KEYTRUDA QLEX were $830 million. We continue to see adoption increase, which supports our confidence in the trajectory of the product. In our broader Oncology portfolio, WELIREG sales increased 58% to $307 million, driven by increased use in previously treated patients and as adjuvant treatment for certain patients with renal cell carcinoma in the U.S., as well as continued uptake from ongoing launches in international markets.
In Vaccines and Infectious Diseases, GARDASIL sales were $2 billion, an increase of 14%. In the U.S., sales grew 18%, benefiting from a significant CDC purchase and price, while international markets increased 6%. In pneumococcal, CAPVAXIVE sales were $263 million, an increase of 7%, driven by ongoing launches in certain international markets. In the U.S., sales declined 13% as increased market share was more than offset by lower adult pneumococcal vaccination rates. In RSV, ENFLONSIA sales of $187 million reflects seasonal demand and associated inventory build. In Cardiometabolic and Respiratory, WINREVAIR continued its momentum with global sales of $694 million, an increase of 94%, reflecting strong demand from adults with pulmonary arterial hypertension, as well as a benefit from channel inventory.
In the U.S., nearly 1,600 new patients received a prescription, approximately 30% of whom were on background therapies that did not include a prostacyclin. Outside the U.S., we continue to progress with ongoing launches. OHTUVAYRE sales were $184 million, reflecting continued demand from adults with COPD, partially offset by a small headwind from the timing of Specialty Pharmacy purchases. While early, we are encouraged by the initial launch of LIPFENDRA. Prescription trends and physician feedback has been positive. Additionally, we have established programs to support access and affordability for eligible patients. As expected, broad access will take time to build, and we remain confident in the long-term opportunity for this important treatment option for adults with elevated LDL cholesterol. Our Animal Health business delivered growth of 3%. Companion animal sales increased 6%, driven by new product launches. Livestock sales grew 2% due to higher demand for poultry products.
I will now walk you through the remainder of our P&L, and my comments will be on a non-GAAP basis. Gross margin decreased slightly to 81.4%. Operating expenses increased 12% to $7.4 billion, reflecting increased investments to support our launches and advance our diverse early and late-phase pipeline. This increase was partially offset by benefits from our ongoing multiyear optimization effort and the recognition of a portion of the external funding for sac-TMT development.
There was also a $400 million upfront charge related to the license agreement with SciBrunch compared with a $300 million business development charge a year ago. Other expense increased to $420 million, primarily reflecting financing costs related to recent business development transactions. Our tax rate was 10.9%, reflecting a benefit from certain discrete items. Taken together, earnings per share were $2.49, which includes a charge of $0.12 per share related to the SciBrunch license agreement.
Now turning to our 2026 non-GAAP guidance. We have narrowed the range and raised the midpoint of both our full year revenue and EPS guidance. We now expect revenue to be between $66.8 billion and $67.3 billion, representing growth of 3% to 4%, including a positive impact from foreign exchange of approximately 1 percentage point using mid-October rates. Our gross margin assumption remains approximately 81%. Operating expenses are expected to be between $42.4 billion and $42.9 billion. Other expense is still expected to be approximately $1.4 billion. We now expect a full year tax rate between 32% and 33%. We assume approximately 2.48 billion shares outstanding. Taken together, we expect EPS of $2.77 to $2.82, including a positive impact from foreign exchange of approximately $0.15 using mid-October rates. This range also includes the SciBrunch charge.
As you consider your models, there are a few items to keep in mind. Third quarter sales benefited by approximately $550 million from favorable purchase timing in the U.S. We expect that the benefit related to KEYTRUDA and WINREVAIR to fully unwind in the fourth quarter, while the majority of the benefit to vaccines, primarily related to GARDASIL, is expected to unwind next year. As we look forward to 2027, we recently noted an expectation for modest revenue growth. For KEYTRUDA, moderating growth reflects the success we have had in reaching the eligible patients as we now approach peak revenues for certain approved indications. Additionally, we expect the German market to be impacted by policy dynamics.
For BRIDION, we expect competition from multiple generics that have now entered the market. For vaccines, we are watching broader market trends given increased hesitancy and reduced utilization. Finally, we also expect underlying operating expenses to increase at a mid- to high single-digit rate, reflecting our conviction in the significant opportunity from our expanding pipeline and the growing portfolio of new product launches.
Now turning to capital allocation, where our priorities remain unchanged. We will continue to invest in value-creating opportunities that drive both near- and long-term growth. We remain committed to the dividend with the goal of increasing it over time. Business development remains an important priority, and we retain financial flexibility within a strong investment-grade credit rating to pursue additional science-driven, value-enhancing transactions. We remain on track for approximately $3 billion in share repurchases this year.
To conclude, as we head into the fourth quarter, we remain confident in the outlook for our business. Demand for our diverse portfolio of human and animal health products remains strong, and our recent launches are making increasingly meaningful contributions to growth. Our compelling innovative portfolio of pipeline assets continues to progress, leaving us very well positioned to deliver outstanding value for patients, customers and shareholders now and into the future.
With that, I'd like to turn the call over to Dean.

**Dean Li** (Executives):
Thank you, Caroline. Good morning, everyone. The third quarter was marked by a number of significant clinical and regulatory milestones. Today, I will provide updates in Oncology, Cardiometabolic and Respiratory, Immunology, and Ophthalmology. I will close by highlighting upcoming milestones.
Starting with Oncology, as Rob noted, data from several pivotal studies were presented at ESMO, which exemplify our clinical development approach and reflect how KEYTRUDA is informing our pipeline progress. ESMO marked the first presentation of detailed Phase III findings from our expansive global TroFuse development program for sac-TMT, our TROP2-directed ADC with a unique bifunctional linker. The TroFuse program is guided by a two-prong development strategy.
First, we are moving with speed and rigor to establish early leadership in multiple disease and treatment setting. Many of these first-mover opportunities are in gynecologic cancers, where there remains significant unmet need. The TroFuse-005 study presented at ESMO evaluated sac-TMT in patients with endometrial cancer whose disease has progressed following platinum chemotherapy and anti-PD-1/L1 immunotherapy, demonstrating a remarkable near 7-month improvement in median overall survival compared to chemotherapy alone. Endometrial cancer is one of the few cancers with increasing incidence and mortality rates worldwide. These patients currently face a very poor prognosis, and we look forward to continuing to work with the FDA to deliver this potential new option as quickly as possible.
Second, we are exploring the potential of sac-TMT in certain types of breast and lung cancers where we believe we can be differentiated. In first-line PD-L1 negative non-squamous non-small cell lung cancer, results from the OptiTROP-Lung06 study conducted by our partner, Kelun, showed a meaningful improvement in progression-free survival for sac-TMT plus KEYTRUDA over KEYTRUDA plus chemotherapy, raising the possibility that novel combinations may improve upon the high bar set by KEYTRUDA plus chemotherapy. Our Global TroFuse program includes 5 ongoing Phase III studies in various non-small cell lung cancer setting. We plan to investigate sac-TMT in combination with MK-2010, our PD-1 VEGF bispecific, in first-line non-small cell lung cancer. Engagement with the FDA has been productive, and we anticipate Phase III studies in this setting in the first half of 2027.
Now turning to intismeran. Our deep understanding of tumor biology continues to inform the next generation of our Oncology pipeline, including the development of an mRNA therapeutic cancer vaccine based on the unique mutational signature of a patient's tumor. ESMO marked the unveiling of landmark results for intismeran, an investigational individualized neoantigen therapy developed in collaboration with Moderna, plus KEYTRUDA as adjuvant therapy for melanoma. Results of the INTerpath-001 study demonstrated clinically meaningful improvements in recurrence-free survival and distant metastasis-free survival for intismeran plus KEYTRUDA over standard of care KEYTRUDA in patients with completely resected Stage IIb to IV melanoma. These results, building on the body of evidence from the Phase IIb study, strengthen our confidence in the curative potential of intismeran when given in combination with KEYTRUDA. We are actively engaged with the FDA on regulatory submission.
Additionally, we are progressing a robust INTerpath clinical development program across a range of immune-sensitive tumors, including indications in earlier stages of disease where KEYTRUDA has established efficacy. Phase III studies are ongoing in melanoma and non-small cell lung cancer, which are characterized by high mutational burden. Ongoing Phase II studies are also evaluating tumors with lower mutational burden, including certain bladder and renal cancers, to inform potential future expansion. I look forward to sharing further updates on these and other Oncology programs.
Now to a few regulatory updates. Subcutaneous pembrolizumab and berahyaluronidase alfa was approved by regulatory authorities in Japan and China. In Europe, we received approval for KEYTRUDA plus PADCEV as a perioperative treatment for resectable muscle-invasive bladder cancer. And in the U.S., the FDA approved WELIREG plus LENVIMA for the treatment of patients with previously treated renal cell carcinoma. Regarding ifinatamab deruxtecan, together with Daiichi Sankyo, we made the decision to withdraw the biologic license application seeking accelerated approval. Multiple studies of I-DXd are ongoing in small cell lung cancer, prostate cancer and other tumor types.
Next, in Cardiometabolic and Respiratory, recently, the FDA approved the label update for WINREVAIR, incorporating results from the Phase III HYPERION study, providing further evidence to support its use earlier in the treatment journey for adults with pulmonary arterial hypertension. With WINREVAIR, we introduced activin signaling inhibition, a novel mechanism targeting the underlying vascular remodeling that drives disease progression. Building on the findings from the Phase II CADENCE trial, we are taking an important step to extend the application of activin signaling inhibition beyond Group 1 PAH. The upcoming Phase III CHORUS study will evaluate patients with combined post and pre-capillary pulmonary hypertension associated with heart failure with preserved ejection fraction. This distinct population within Group 2 pulmonary hypertension has similar vascular characteristics to PAH and no currently approved treatment options.
Next, in Immunology. Last month at EADV, positive Phase IIb results were presented for tulisokibart in patients with hidradenitis suppurativa, making it the first anti-TL1A antibody to demonstrate positive clinical data in a dermatology indication. The study demonstrated promising clinical responses and encouraging safety profile. Based on these findings, we plan to advance tulisokibart into Phase III development in HS.
Finally, to Ophthalmology, as Rob mentioned, earlier this month, results were presented from the Phase IIb/III BRUNELLO study, the first of two pivotal studies evaluating remigromig, a novel Wnt agonist in adults with DME. BRUNELLO achieved its primary endpoint with both doses of monthly remigromig, demonstrating non-inferior best-corrected visual acuity compared to monthly 0.5 milligram ranibizumab at 1 year. While anti-VEGF therapies have transformed the treatment of DME, disease activity persists in many patients, highlighting the need for new therapeutic options.
BRUNELLO provides clinical evidence that activation of the Wnt pathway can achieve non-inferior efficacy to an anti-VEGF agent in DME. If confirmed in the companion BAROLO trial, remigromig could introduce a promising new and orthogonal mechanism and help advance the field of ophthalmology toward therapeutic strategies involving multiple pathways.
In closing, the breadth of these milestones reflects our progress in translating novel advances in the understanding of disease biology into potentially significant medicines across diverse therapeutic areas. Over the next 12 months, we anticipate several important clinical and regulatory milestones, including in Immunology for tulisokibart, we are compiling data from the Phase III ATLAS-UC study and expect to share the results in the near term.
In Ophthalmology, the readout of the BAROLO study of remigromig; in Cardiometabolic and Respiratory, the initiation of the Phase III CHORUS study; in Infectious Disease, anticipated regulatory filings for islatravir plus lenacapavir, the potential first once-weekly oral two-drug treatment regimen for HIV, data from the Phase III ANCHOR study evaluating MK-1406, our investigational long-acting and strain-agnostic antiviral designed to prevent influenza, and the data from the Phase III EXPrESSIVE program of our investigational once-monthly oral HIV PrEP option, alimatravir. And finally, in Oncology, the potential approval of sac-TMT in endometrial cancer and additional Phase III readouts, the anticipated regulatory filing of intismeran, and additional readouts in multiple other programs.
And now I will turn the call back to Peter.

**Peter Dannenbaum** (Executives):
Thanks, Dean. Before we get started with Q&A, I'm very pleased to introduce Jannie Oosthuizen and Brian Foard, who are with us this morning to help address questions. And as a reminder, Jannie serves as President of our Oncology business unit as well as MSD International, and Brian serves as President of our Specialty Pharma and Infectious Diseases business unit.
I'd also like to request that analysts limit themselves to a single question today, so that we can get to as many questioners as possible in the time that we have.
So Julie, if you could please start the Q&A session. Thank you.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Chris Schott with JPMorgan.

**Christopher Schott** (Analysts):
Congrats on all the progress. I guess my question, you recently made some comments on 2027, both top line and spend. And maybe just a two-part question. Just interested, do you feel that, that's now appropriately reflected in consensus estimates?
And then just given the R&D spend we are seeing for the company in the near term, as well as the longer-term pipeline derisking we've seen, is it now fair to think about earnings growing off of this type of level as we move through the KEYTRUDA LOE? I guess, asked a different way, does this R&D spend effectively pull forward your trough earnings so we can think more about earnings growth for Merck as we look out to the 2030s?

**Caroline Litchfield** (Executives):
Chris, thank you for the question. First, if I can maybe provide everybody the headlines around our comments on 2027, and then I'll answer the specific questions.
For 2027, we see it as another year of investment as we invest behind our expansive pipeline and our new product launches to drive long-term growth. Specifically in 2027, we expect moderate top line growth, and that's as a result of the strong contributions we expect from our new product launches as well as Animal Health that will be partially offset by more than $2 billion of headwinds as a result of generic competition and LOE impacting BRIDION, JANUVIA family of products, as well as Adempas.
We do expect KEYTRUDA to continue to be an important contributor to our overall revenues, although we do see growth moderating, and that's as we've reached peak penetration in a number of indications. While we also expect headwinds to price in our ex-U.S. market and we are watching the policy dynamics in Germany. From a vaccines perspective, we have seen a benefit of a CDC buy-in in 2026 of approximately $250 million that will unwind in 2027.
Now as we look at the rest of the P&L, gross margin will increase given the roll-off of a royalty on KEYTRUDA. As you've noted, we expect expenses to increase because we are fully investing behind our strong pipeline as well as our launches. And we do expect slightly higher interest expense and a slightly higher tax rate. But all in all, '27 marks a year of investment for strong growth in our future, which is all in part to drive our strategy of how our company grows beyond the KEYTRUDA LOE.
Now as we look at that, we see the KEYTRUDA LOE as really more of a hill on the overall revenues of our company as we will, in short order, then return to strong growth. As we look at consensus estimates for 2027, there are a number of different estimates from the different analysts and some have incorporated the messaging that we've given, many have not yet. So hopefully, this will provide clarity as to our expectations for 2027.
And as we look at earnings as we move forward, we do expect to see our company have earnings as we move towards the LOE period grow. We do expect, as I've noted, a shallow dip in revenues in the initial period post the price setting through IRA and the LOE, but to quickly return to growth. And we would expect the earnings profile to probably mirror that given the expansive pipeline that we have and the continued studies that we will be doing and supporting as well as the launches that are coming through year-over-year.
So headline, confident in our future, confident in our pipeline that will drive long-term growth and patient benefit and enable us to offset over time the KEYTRUDA LOE.

**Operator** (Operator):
Our next question comes from Vamil Divan with Guggenheim Securities.

**Vamil Divan** (Analysts):
Congrats on the progress with the pipeline. Maybe just on WINREVAIR, if I could ask a couple. One, if you could quickly just quantify the onetime benefit you saw specifically for WINREVAIR this quarter. I know you kind of grouped it into the $550 million you saw overall for the Pharma business.
And then Dean, I specifically wanted to ask you on the CHORUS trial. We did go through the listing there on clinical. If you can discuss how it's similar or different than what you did with the Phase II CADENCE trial in terms of the endpoint, in terms of the inclusion criteria, just to give us a sense of how the patients and the study will compare to each other?

**Caroline Litchfield** (Executives):
Thank you, Vamil, for the question. In terms of the timing benefits that we saw in the quarter, if I may give the full picture, inclusive of WINREVAIR, so that we have it out there for all. We had a benefit in the third quarter of $550 million as a result of the timing of purchases. $200 million of that relates to KEYTRUDA, which we will expect to unwind in full in the fourth quarter. $50 million relates to WINREVAIR, which we expect to unwind in the fourth quarter.
A further $300 million relates to our vaccines business, which is predominantly GARDASIL. We expect $50 million to unwind in the fourth quarter and the remaining $250 million to unwind in 2027.

**Dean Li** (Executives):
Yes. Vamil, thank you very much for the questions. I'll just answer it in two parts. The first is I just want to call out for PAH Group 1, not Group 2, that the field is increasingly moving to a concept of with activin signaling inhibitor, the potential of remission. And you've seen that in the European guidelines that have come out, and we are hopeful that the similar sort of standard will take. This is really important because it suggests similar to ACE inhibition in left heart failure that in this right heart failure with PAH Group 1 that physicians in the field can think differently about the treatment paradigm.
The reason I want to bring that up is that you've asked me now about Group 2, which is a heart failure study. We have the CADENCE study. And what we're going to be doing in the CHORUS study, and I just want it to be pretty clear, we're not expanding the patient population in any substantive way.
There are details in relationship to how we're going to execute on the trial. But we really think that "This patient population that was seen in the CADENCE has an incredibly high unmet need, there's no approved treatment, it's really poor prognosis, and it's also an orphan indication." And so from CADENCE, we met primary endpoints, reduction in PVR and important secondary endpoints. And we're going to initiate the Phase III CHORUS this year with a 0.3 milligram per kilogram dose and with time to clinical worsening in the endpoints. And we expect that this will be a very attractive trial for patients with Group 2 pulmonary hypertension.

**Operator** (Operator):
Our next question comes from Michael Yee with UBS.

**Michael Yee** (Analysts):
Maybe, Dean, if I could just follow up on, obviously, the very busy ESMO conference. Maybe here you could offer a view about the fact that you have greater confidence in China studies being further replicated across all of your global TroFuse studies. And since I think we've discussed lung cancer enough, maybe you could just comment on where the one or two other sac-TMT indications you think are most notable and that we may not be paying attention to.

**Dean Li** (Executives):
Okay. So I had a hard time hearing, but I think the gist of your question relates to the TROP2 ADC that we have, our sac-TMT. And I would just highlight what was said in the remarks, which is we've always had a two-part strategy.
The first part is we had recognized that when we got into this field that there were two TROP2s that were ahead of us, but we were actually surprised that they did not move quickly to indications outside of breast and lung, and we thought that there would be an enormous opportunity to do so. And you see that in our clinical trials as we move very fast outside of lung and breast. There are trials that we have in lung and breast, but we've moved very fast outside of that. And this most recent TroFuse-005 is an evidence of that.
The reason why that's important is if you look at that TroFuse-005 as a proof point, I would just call your attention to, I think it was a presentation, I think, in 2025 or 2026, with MK-2870-001 or Kelun-264-01. That's the Phase I/II endometrial cohort. That was the informative information for us looking at Chinese data that allowed us to figure out how to translate that in a TroFuse-005.
So the bottom line is that experience working closely with Kelun, it isn't like you're going to translate them exactly, but it gives you the signal as to how you might translate it into global. So that gives us confidence that the Kelun data is a really important signal for us and that we are confident that we can translate it into the global trials. And we hope to replicate that in other indications outside of lung and breast. But clearly, as Marjorie and Eliav have talked recently, we plan to go quite aggressively in lung.

**Operator** (Operator):
Our next question comes from Courtney Breen with Bernstein.

**Courtney Breen** (Analysts):
I just wanted to zoom into the subcutaneous or KEYTRUDA QLEX litigation that is ongoing around the hyaluronidase component of that product. We're seeing kind of obviously reports out of Europe and kind of infringement claims that are being made. Can you just contextualize where we're at in Europe relative to the U.S.? Is this a definitive call? Are there likely paths to moving back towards the launch in these European countries? And is there any risk in the U.S. as we move forward given the path and the intentions and the litigation that is ongoing?

**Robert Davis** (Executives):
Maybe I'll start, Courtney, and then I'll turn it over to Jannie. Overall, I just want to emphasize, we feel very strongly that we have IP that gives us freedom to operate as it relates to QLEX. That's why we actually pursued action against others in the field to ensure we could do that. So nothing has changed to our confidence we see long term. The injunction you're seeing in Europe is just an injunction until the hearing is held. It doesn't speak to the merits of our belief. We continue to feel very good that we have a position both in the U.S. and in Europe. But maybe I'll let Jannie speak specifically to the implications of Europe and how we see that potentially resolving.

**Jannie Oosthuizen** (Executives):
Yes. Thank you, Rob, and thank you for the question, Courtney. In relation to the U.S., as Rob said, we feel really strong about our position in the U.S. And in fact, you saw the number, $830 million of QLEX in the quarter or KEYTRUDA subcu in the quarter, which is the majority is the U.S. Since we received the permanent J-code on April 1, it's really been a very positive trajectory, and we feel good about the objective of getting to that 30% to 40% adoption in the United States by the end of 2027. So the United States, we're really on a good path.
In terms of ex-U.S., we've always talked about a range of adoption from high adoption markets to much lower adoption. In our high adoption markets, which is the U.K., Canada, Austria, we're actually able to supply. We're waiting for the launch in Canada, but these are the high adoption markets, and we actually see a high level of adoption in the U.K. already. So that is also very positive and not challenged by the injunction out of the Netherlands.
In terms of Japan and China, also no issue from a supply and launch perspective, and we're waiting to launch in those 2 markets where there's significant volume, and we have an ambition to get a high level of subcutaneous use. In Europe, where the Dutch ruling is valid for now, as Rob said, we do not disagree with the Dutch court, and we will continue to work to overturn this. So for now, we will not supply in Italy, Denmark, the Netherlands, France, Belgium and Ireland. These, in general, are smaller volume markets, so it's immaterial in terms of our overall volume of subcu. But again, given that we have longer IP, if we would turn this decision positive, we will have time to get back and make this convenient formulation available to patients in these markets as well. So overall, we feel we're in a really good place in terms of subcutaneous adoption and trajectory of where we want to be.

**Operator** (Operator):
The next question comes from Akash Tewari with Jefferies.

**Akash Tewari** (Analysts):
It looks like the primary endpoint for your KRAS G12C first-line NSCLC trial was changed from PFS and OS to PFS-only back in September, which cut your target enrollment and moved up your primary completion. Do you think this is a part of a larger stance that maybe the FDA is taking here where hitting on OS is important, but not gating towards initial filing? And how could that maybe apply to the design for your first-line sac-TMT PD-1 VEGF bispecific trial you're aiming to start in first half of next year?

**Dean Li** (Executives):
Yes. Thank you very much for actually calling out calderasib. I'll just step back so that other people who are listening understand. That's our KRAS G12C inhibitor. And we think that MK-1084 or calderasib is a very important molecule. It has the profile that we wish that any RAS molecule would have. It's extremely potent, it's extremely selective, and it can be well combined, for example, with KEYTRUDA in the lung situation and with something like cetuximab in the CRC, and we've seen really strong data.
In relationship to our moving forward in relationship to this, I think part of that is discussions and feedback with the FDA. I do believe that all of those endpoints will be important. PFS, OS eventually will all be important. But yes, we are moving with speed and rigor to get this calderasib in first-line lung with KEYTRUDA, but especially subcu KEYTRUDA moving quite fast.
I should also emphasize that there is a difference of how we might have a philosophy in terms of clinical development versus others in this space. And for us, what's really important is, again, this is a place where we're thinking about KEYNOTE-189, KEYNOTE-407 and asking ourselves, well, how do we displace that with those patients who have a KRAS G12C mutation, which is the dominant mutation for RAS in that patient population. And our strategy is not to add it on top of pembro plus chemo, but to use a pembro plus that inhibitor by itself without the chemo, so that we can create a chemo-free option for patients.

**Operator** (Operator):
The next question comes from Daina Graybosch with Leerink Partners.

**Daina Graybosch** (Analysts):
I might have a follow-up that is right on RAS. You have two other RAS assets, one that you licensed out of China. I wonder if you could just step back, Dean, and talk about how you're thinking about the full portfolio across indications and combinations beyond calderasib.

**Dean Li** (Executives):
Yes. So thank you very much for that question. I think it shares a lot of similarities. So our interest in, for example, KRAS G12D is whether we could, for example, replicate what we see in lung with a KRAS G12D in a very similar strategy. But as I said, we're using calderasib and 1084 as a way to sort of measure what we do.
The other place that we have, we think, quite good data is calderasib in relationship to CRC, especially in first-line CRC. Now in calderasib in CRC, KRAS G12C is a really important target, but it's the minority. It's the distinct minority of RAS mutations. KRAS G12D is the sort of more dominant mutation. And so our hope is that this KRAS G12D that we should have important clinical data in the next year or so will replicate what we've done in KRAS G12C in, for example, lung and CRC.
And also, we would clearly look to see what it does in pancreas. But our focus has been how do we use calderasib and how do we look at the other isoforms of RAS or the other subtypes of RAS and how do we recreate what we believe is a really good profile for KRAS G12C and how do we replicate it for the other subtypes.

**Operator** (Operator):
The next question comes from Mohit Bansal with Wells Fargo.

**Mohit Bansal** (Analysts):
Congrats on all the progress. So just trying to stick to TL1A or tulisokibart. So it does look like the field of IBD is moving towards combinations as we try to push remission rate higher in earlier lines of setting. So in that backdrop, how are you thinking about building a combination strategy around TL1A? Do you think it is strategically important to have all the complementary mechanisms in-house? Or would you be comfortable partnering with some established marketed products at this point to find the best combination?

**Dean Li** (Executives):
Yes. So you broke up a little bit, but I'll just answer in a more general way, because I think you're asking a question that's a broader question in immunology, how do you think about combinations and as such. Combinations have been done quite a lot in immunology. They were done back, I think, in the 2018 -- I can't remember, 2020 range. And those combinations have not generally given that much benefit. So you do not see that combination strategy play out.
I do have to give our credit to a company who has more recently advanced sort of combinations, and we'll see how that data comes through. But the bottom line is, combinations could be important. We believe combinations, for example, in oncology are really important. We think combinations of different mechanisms in ophthalmology is really important, and combinations could be really important throughout immunology. However, I think each indication and each sort of compounds that are there will have to play out and will have to all do as a field the work to determine how important and how effective combination therapies are throughout immunology and the different indications.

**Robert Davis** (Executives):
And maybe I'd just add because I think you had a business development angle to that question as well. So starting with, we have several assets coming through early development in-house. So we actually have a range of internal assets that could be potential combination partners, but we also remain open on the business development front, both in terms of products in development as well as commercialized products. So we're looking at all fronts and remain confident that we are positioned to move depending on how we see the field evolve, as Dean said.

**Operator** (Operator):
The next question comes from Steve Scala with TD Cowen.

**Steve Scala** (Analysts):
I'm curious what LIPFENDRA sales were in the quarter and what percent of prescriptions are free drug. Despite lots of competitors, Lipitor generated over $800 million in its first year on the market. And I can't think of any reasons why LIPFENDRA shouldn't do at least that well. And I'm wondering if you agree.

**Robert Davis** (Executives):
So appreciate the question. We are -- as we highlighted in the opening comments, as Caroline laid out, we are focused on affordability and access in the way we structured this. So we are using couponing and other means. I'll let Brian speak to it. I think what you're going to see right now is the script data is quite strong. We're not going to give specifics on our revenue forecast at the moment, but I'll let Brian maybe give comments just so you can get a sense of how we're seeing the scripts evolve.

**Brian Foard** (Executives):
Yes, Steve, thank you so much for your question. It sounds like you have similar excitement as we do in this particular space as well. We are seeing really early positive uptake, actually, and I'll speak to a couple of the numbers. In spite of the fact that we know that this is a marketplace, but there is a significant amount of inertia. And we said that it will be a gradual ascent as the prescriptions come in. But I'll give you a couple of metrics to think about.
So in the third quarter, we saw more than 11,000 prescriptions, and this is coming from over 6,500 prescribers. And those prescribers are broken down. We're actually seeing not just in cardiologists, but also in general practitioners, which is really encouraging. But probably what's even a little bit more encouraging than that is we're seeing the signs of actually expanding beyond the PCSK9 marketplace. The vast majority of prescriptions are coming from patients on other background lipid-lowering therapies rather than switches off of injectable PCSK9, which is exactly what we had hoped for.
Now keep in mind, I think as Rob had mentioned, we have sampling and coupon programs that are out there today. That will affect revenue in the short term. But we're also actively in discussions with payers and the whole goal there is to get as rapid access as possible. Commercial, we expect, as we have mentioned before, large coverage of the access in the commercial space in the 2027 time frame. And then for Medicare, it's actually in the 2028 time frame as well.
Now our teams are working really diligently to expedite that and bring it forward. But as we said before, this is a place that there is natural inertia in the marketplace. And so we're cautious about the early uptake, but early signs are positive for us, and we see this, again, as we said, as a meaningful growth driver for us in the future, a multibillion opportunity.

**Operator** (Operator):
The next question comes from Umer Raffat with Evercore ISI.

**Umer Raffat** (Analysts):
Dean, I was thinking about the recently presented melanoma data for the cancer vaccine. And my question is, how does that efficacy break down for patients that had a lower number of neoantigens, and perhaps even more importantly, patients that did not have a major driver mutation like NRAS or BRAF, et cetera. I'm just trying to think through the implications for the upcoming RCC readout.

**Dean Li** (Executives):
Yes. So I want to be a little bit cautious of getting ahead of the data that was presented and the data that we are examining and will likely provide in sometime, I think some people have said in the next year or so. So I don't want to get ahead of that. But I would just emphasize, and if you don't mind, I'm going to take a little bit of time here in relationship to that, which is there was a press conference or investor meeting that Moderna sponsored. And I would just call out the 2 really important experts that they had there, which was Georgina Long, who was important for this trial and Antonio Ribas.
And the reason I want to call that out is, I've seen some reports about melanoma and all of this. I just want to call out that Georgina Long was a senior investigator of NADINA, and Antonio Ribas was the senior author of SWOG 1801. And I would just quote Antonio Ribas saying, "This is a landmark in cancer drug development." And so we are eager to present that to the FDA. And I do think the data, as interpreted by those people who are scientific leaders, is that this is a landmark study in its own right. And because of that, we would expect that -- or we would hope, I should say, that upon approval that the NCCN guidelines would potentially define this as a new standard of care. So that's the melanoma question.
The other question is melanoma itself you can have a spectrum of TMB within melanoma. But in general, the spectrum of TMB in melanoma is just shifted. It's just shifted totally in favor of being high TMB. So I would be a little bit cautious for me to overinterpret any data in, for example, lower TMB in melanoma as a signal for RCC. I think the fundamental issue is that what you've seen is that at least in our hands, checkpoint inhibitors and IO agents, not just ours, but for example, IL-2 have worked.
That has been a place that RCC has been a good tumor in relationship to what you would call immune responses. And I think TMB is important, but I also think TMB is not the only determinant of immune responsiveness. And if you take that view, that's how I look at our upcoming study with RCC. I'm not so sure that parsing the TMB within melanoma will give me any increased or decreased confidence in relationship to RCC.

**Operator** (Operator):
The next question comes from Asad Haider with Goldman Sachs.

**Asad Haider** (Analysts):
A lot of mine have been asked, but maybe one big picture zooming out for you, Rob. Just given the developments over the course of this year, it would be great to get any updated framing on how you see the $70 billion revenue opportunity you've talked about by the mid-2030s. You've obviously had a lot of pipeline success over the course of the year. The company continues to transform its portfolio. Things are moving in the right direction to derisk that number. So maybe just double-click on the pushes and pulls that have occurred to influence that and remind us on what wasn't incorporated into that framing and what surprised you to the positive side and what's still underappreciated.

**Robert Davis** (Executives):
Yes. No, I appreciate that. So overall, the pride I have in what we've done as a company and how we're moving forward given the fact that we've seen so much of our clinical data readout positive to date. Obviously, these are studies. So every card is a new card and you have to wait to see until the next card is overturned. But that said, what we've seen so far gives me great confidence and increased confidence in that $70 billion. And as such, as we've indicated, we expect now to be raising that number, not only because of what we're seeing confidence in what we have, but what wasn't included, which is, I think, part of your question.
And I would just remind you that when we gave that number, we did not have the Terns acquisition included. That is going to be addition to that number. In addition to that, we really put nothing in for the PD-1 VEGF, which now, given what you've heard coming out of several different conferences and other meetings, we have growing confidence in that as a combination agent for us as we think about that with sac-TMT and with everything else. So a lot of excitement there. sac-TMT itself is probably going to have broader indications as we look forward, given the fact that we're kicking off new studies there as well.
And then lastly and importantly, intismeran.  Intismeran was in our initial expectation, but it was based on a product profile that, frankly, given the data we have seen, we actually see a better commercial profile than what we expected. So the targeted product profile now is stronger. And so that in and of itself would drive some upside.
So as we look across the portfolio, I feel very good about where we are and our ability to navigate the KEYTRUDA LOE. And importantly, we have a lot more catalysts coming as you look out over the next 12 to 24 months. So I think we need to continue to see those cards, but I feel very good about where we're sitting right now.

**Operator** (Operator):
The next question comes from Terence Flynn with Morgan Stanley.

**Terence Flynn** (Analysts):
Maybe a follow-up to a prior one. Dean, I recognize your comments on melanoma and what it means for other tumor types. What about the implications of the INT PDAC poster that were presented at ESMO? Maybe you could just help put that into context for us and the importance of that as you think about other tumor types.

**Dean Li** (Executives):
Yes. So I did not enjoy the balmy weather in Spain, and I had Eliav and Marjorie out there. But I listened very carefully to some of the questions that were placed before them and also to our Moderna colleagues. So I will just answer just in a more broad way. We have like four Phase III INTerpath, and we have five Phase IIs. There is a strategy to broaden it from melanoma to lung to bladder to RCC within the conservative point of view in relationship of where we know that those are immune responsive and specifically our checkpoint inhibitor responsive and specifically our KEYTRUDA responsive and specifically KEYTRUDA responsive in early stage.
When you look at our trials, I think it's very important because people have asked different questions, and I'll get to your pancreatic study, but we have laid it out that what could it do without an IO agent. And so you see in Stage I non-small cell lung cancer in INTerpath-014, that's what we're doing. In NMIBC, we're asking -- in the absence of checkpoint inhibitor, we're asking what happens in metastatic, that's first-line melanoma, that's INTerpath-012 and first-line squamous non-small cell lung cancer, INTerpath-013.
Specifically, your question of something that's IO nonresponsive, that's not where we've placed most of our Phase III, Phase II, but there are data from our -- other people moving field that suggests that we should look at it. And we're testing whether or not with a checkpoint inhibitor or even IO nonresponsive tumors, how to think about it. But I also just want to make sure that everyone understands that there were questions in relationship to perioperative and all of this for melanoma. We also have questions of perioperative. We're not asking that question so much in melanoma, but we're asking that in non-small cell lung cancer, which is INTerpath-009.
So I just want to give a sense that some of the questions that were asked that I've seen. We don't have every trial, but I hope that gives you a general sense of we have melanoma, and we're trying to broaden the scope, and we're trying to do the experiments that will teach us not just what tumor type, but how to think about the indication and the mechanism of action.

**Peter Dannenbaum** (Executives):
Great. Thank you, Terence. And we know it's a busy day for all of you, and we're at the top of the hour. So we're going to end it there. Thank you all for the very good questions, and please follow up with the IR team for any follow-ups.

**Operator** (Operator):
Thank you for your participation. You may disconnect at this time.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MRK_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Caroline Litchfield｜guidance：CFO 說全年營收財測上修並收窄至 663–673 億美元（成長 2%–4%）（原話："to be between $66.3 billion and $67.3 billion"）
- 2026-08-04｜Caroline Litchfield｜guidance：全年 non-GAAP EPS 財測 2.66–2.76 美元，中點 2.71（原話："we expect EPS of $2.66 to $2.76 with a midpoint of $2.71"）
- 2026-08-04｜Caroline Litchfield｜margin：全年毛利率假設約 81%，反映較高的存貨提列（原話："Gross margin is now assumed to be approximately 81%"）
- 2026-08-04｜Caroline Litchfield｜margin：Q2 non-GAAP 毛利率 81.1%，年減 1.1 個百分點，管理層歸因於存貨提列（原話："Gross margin was 81.1%, a decrease of 1.1 percentage"）
- 2026-08-04｜Caroline Litchfield｜margin：數字口徑：剔除 Terns 收購費用後，營業費用成長 7%（原話："Excluding these charges, operating expenses grew 7%"）
- 2026-08-04｜Caroline Litchfield｜guidance：全年稅率預期上調至 35%–36%，因 Terns 一次性費用不可抵稅（原話："We now expect a full year tax rate between 35% and 36%"）
- 2026-08-04｜Caroline Litchfield｜guidance：EPS 財測含 Terns 一次性每股 2.31 美元費用（原話："an upfront charge of $2.31 per share related to the"）
- 2026-08-04｜Caroline Litchfield｜guidance：營業費用財測不含其他重大潛在 BD 交易（原話："This guidance does not assume"）
- 2026-08-04｜Caroline Litchfield｜guidance：OHTUVAYRE 第三季銷售將受第二季專業藥局進貨回沖影響（原話："unwind of specialty pharmacy purchases in the second"）
- 2026-08-04｜Caroline Litchfield｜commitment：管理層預期 OHTUVAYRE 相關投入將帶動 2027 年加速成長（原話："expect these actions to lead to accelerated growth in 2027"）
- 2026-08-04｜Caroline Litchfield｜guidance：下半年美國 KEYTRUDA 年增率預期趨緩（原話："total U.S. KEYTRUDA year-over-year growth will moderate"）
- 2026-08-04｜Caroline Litchfield｜guidance：數字口徑：2025 年第三季約 2.5 億美元批發商進貨時點效益今年不會重複（原話："approximately $250 million due to the timing of wholesaler"）
- 2026-08-04｜Caroline Litchfield｜competition：BRIDION 美國銷售預期下滑速度較先前預期慢，因學名藥競爭低於預期（原話："decline at a slower pace than previously expected"）
- 2026-08-04｜Caroline Litchfield｜guidance：下半年其他營收預期明顯高於去年同期，來源為營收避險計畫與第四季授權里程碑（原話："expected to be significantly higher than the second half"）
- 2026-08-04｜Caroline Litchfield｜capital_allocation：今年約 30 億美元庫藏股如先前所述（原話："approximately $3 billion in share repurchases this year"）
- 2026-08-04｜Caroline Litchfield｜commitment：管理層承諾維持股利並以逐步提高為目標（原話："We remain committed to the dividend with the goal of"）
- 2026-08-04｜Caroline Litchfield｜capital_allocation：BD 仍為高優先，維持強投資等級信評下可再做交易（原話："development remains a high priority, and we maintain"）
- 2026-08-04｜Caroline Litchfield｜product：KEYTRUDA QLEX 本季 4.63 億美元，管理層對採用軌跡有信心（原話："confident in the trajectory of KEYTRUDA QLEX adoption"）
- 2026-08-04｜Caroline Litchfield｜product：WINREVAIR 美國已有逾 1,800 名新病人開立處方（原話："1,800 new patients having received a prescription"）
- 2026-08-04｜Caroline Litchfield｜customer：GARDASIL 美國持平，需求較低與 CDC 採購時點被價格大致抵銷（原話："the U.S. was roughly flat as lower demand and timing of CDC"）
- 2026-08-04｜Robert Davis｜risk：CEO 描述 KEYTRUDA 專利到期期間為淺坑而非懸崖（原話："the LOE period is more of a hill than a cliff"）
- 2026-08-04｜Robert Davis｜commitment：CEO 稱預期淺幅下滑後快速回到成長，並以未風險調整基礎仍期望成長穿越（原話："a shallow dip with a fast return back to growth"）
- 2026-08-04｜Robert Davis｜risk：CEO 就 700 億美元機會的最大風險被問及，稱難以指出擔心之處（原話："It's hard to frankly point to anything I'm worried about"）
- 2026-08-04｜Robert Davis｜product：敘事變化：CEO 稱信心高於 1 月，因讀數提前（原話："my confidence is higher than it was in January"）
- 2026-08-04｜Robert Davis｜product：CEO 說 1 月時 sac-TMT 與 I-DXd 預計 2027 才有讀數，現已都有正面讀數（原話："we had highlighted sac-TMT as well as I-DXd as not having"）
- 2026-08-04｜Robert Davis｜product：LIPFENDRA 上市初期節奏預期不會一開始就很快，但長期仍預期為重磅（原話："expecting to see the pace not be as fast out of the gate"）
- 2026-08-04｜Robert Davis｜commitment：依 MFN 協議，公司承諾將 LIPFENDRA 上架 TrumpRx（原話："in our MFN agreement, we did commit to"）
- 2026-08-04｜Robert Davis｜competition：LIPFENDRA 定位為市場擴張而非搶注射型 PCSK9 份額（原話："we are not focusing this market on how do we"）
- 2026-08-04｜Caroline Litchfield｜customer：CFO 稱需把學術領袖的正面回饋轉化到基層醫療端（原話："What we need to do is to translate that to the primary care"）
- 2026-08-04｜Dean Li｜risk：LIPFENDRA 目前沒有 CVOT，進行中的試驗 2029 年讀數（原話："we have an ongoing trial that will read out in 2029"）
- 2026-08-04｜Dean Li｜product：LIPFENDRA 與 rosuvastatin 固定複方，管理層希望 LDL 降幅可達 80%（原話："we think that we could get up to 80%"）
- 2026-08-04｜Dean Li｜risk：流感藥 MK-1406 第三期延長至第二個北半球流感季，仍稱 2029 年可能核准（原話："potential approval in 2029"）
- 2026-08-04｜Robert Davis｜risk：CEO 被問延長試驗是否因數據，回答信心沒有改變，純為申報強度（原話："there's no change in our confidence"）
- 2026-08-04｜Dean Li｜product：tulisokibart 在 SSc-ILD 第二期未達主要終點（原話："the study did not meet its primary end point"）
- 2026-08-04｜Dean Li｜product：tulisokibart 在化膿性汗腺炎第二期達主要與關鍵次要終點（原話："the study met its primary and key secondary endpoints"）
- 2026-08-04｜Dean Li｜product：Dean Li 稱不會因 SSc-ILD 結果放棄免疫纖維化假說（原話："I would not throw out the immunofibrosis"）
- 2026-08-04｜Dean Li｜product：sac-TMT 子宮內膜癌第三期 TroFuse-005 在 OS 與 PFS 皆顯著改善（原話："statistically significant and clinically meaningful"）
- 2026-08-04｜Dean Li｜competition：敘事變化：sac-TMT 肺癌一線將重新思考 KEYNOTE-189 設計，不限 PD-L1 表現（原話："So yes, we are going to rethink KEYNOTE-189"）
- 2026-08-04｜Dean Li｜competition：AVANZAR 讀數後再決定 sac-TMT 是否需要生物標記（原話："You can always have a biomarker, but that doesn't mean"）
- 2026-08-04｜Dean Li｜competition：PD-1/VEGF 策略：關注 Summit/Akeso 數據（原話："We are very interested in following the Summit Akeso data"）
- 2026-08-04｜Dean Li｜commitment：alimatravir 兩項第三期預計明年讀數（原話："Phase III studies anticipated to read out next year"）
- 2026-08-04｜Dean Li｜commitment：WINREVAIR 標示更新 PDUFA 日為 9 月 21 日（原話："September 21 PDUFA date for WINREVAIR"）
- 2026-08-04｜Dean Li｜commitment：10 月 26 日 ESMO 投資人活動預告（原話："Monday, October 26, where we will host an investor event"）

### MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜commitment：MK-2010 第一線非小細胞肺癌（含與 sac-TMT 合用）Phase III 預計 2027 上半年啟動（原話："we anticipate initiating Phase III development for MK-2010"）
- 2026-10-26｜Eliav Barr (CMO)｜guidance：sac-TMT 子宮內膜癌 FDA PDUFA 日期為 6/15（原話："The FDA has granted a PDUFA date of June 15."）
- 2026-10-26｜Eliav Barr (CMO)｜guidance：管理層指明明年有兩個重要腫瘤藥核准潛力（sac-TMT、intismeran）（原話："we see the potential of 2 important oncology approvals"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：TroFuse 計畫有 18 項進行中全球 Phase III（原話："Our TroFuse program currently includes 18 ongoing global"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：TroFuse-005 降低進展或死亡風險 41%（原話："reduced the risk of disease progression or death by 41%"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：INTerpath-001 降低復發或死亡風險 42%（原話："significantly reduced the risk of recurrence or death by 42%"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：INT 前 6 個月曲線重疊（非比例風險）（原話："During the first 6 months, the curves are largely"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜risk：管理層強調該敏感度分析不取代 ITT 分析（原話："does not replace the ITT analysis"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜risk：輔助黑色素瘤檢查點抑制劑尚未改善整體存活（原話："have not yet improved overall survival"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：MK-2010 為 Phase III-ready 資產（原話："MK-2010 is a Phase III-ready asset"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜competition：新輔助 NADINA 研究約 30% 發生 3 級以上毒性（原話："about 30% of people get very significant grade 3 or higher"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜competition：管理層稱 INTerpath-001 與 NADINA/SWOG 無法直接比較（原話："they are very apples and oranges in their approach"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：INT 製程週轉時間約 6 週（原話："the turnaround time is around 6 weeks"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜commitment：管理層稱 INT 已備妥商業化（原話："So we're ready for commercialization."）
- 2026-10-26｜Eliav Barr (CMO)｜product：已與監管機關接觸討論 intismeran（原話："we are already engaging with regulatory authorities"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜competition：sac-TMT+MK-2010 vs 與 pembro 組合的設計未揭露，目標取代 KEYNOTE-189（原話："if your goal is really to displace KEYNOTE-189"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：sac-TMT 全球研究劑量 4 mg/kg，無誘導加維持的前瞻計畫（原話："There isn't a current prospective plan"）
- 2026-10-26｜Eliav Barr (CMO)｜customer：新輔助黑色素瘤不會成為主流，輔助為多數病人的路徑（原話："I don't see neoadjuvant becoming the rage."）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜capital_allocation：與 Moderna 的 INT 製造合作（原話："Moderna has been amazing partners to work with"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：生物標記策略未揭露主要假設（原話："where we might have a primary hypothesis about a biomarker"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜risk：與 FDA 就非比例風險的討論內容未揭露（原話："we have not talked about our discussions with the FDA"）
- 2026-10-26｜Eliav Barr (CMO)｜product：INT 單藥與 KEYTRUDA 外組合的探索（AE 考量）（原話："still has an AE profile that requires careful attention"）
- 2026-10-26｜Eliav Barr (CMO)｜commitment：預期 2027 年有 INT 相關研究讀數（原話："I anticipate that 2027 will have some really interesting"）
- 2026-10-26｜Eliav Barr (CMO)｜risk：RCC 為 Phase II，不預設監管結果（原話："we don't want to get ahead of the regulatory authorities"）
- 2026-10-26｜Marjorie Green (SVP Oncology Clinical Dev)｜product：TroFuse-010 為第一線研究（原話："It is a frontline study, yes."）

### 問答異常語氣（迴避／改口／保留）
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Geoff Meacham（Citi）問 LIPFENDRA 初期可及性節奏、報銷預期與是否需要 CVOT 作為商業轉折｜答法：Dean Li 先轉給 CEO；Rob 談標示乾淨、需時間建立可及性、初期速度較慢，未給報銷預期或數字，也未直接回答 CVOT 問題
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Chris Schott（JPMorgan）問 2028 至 2030 年代初 KEYTRUDA LOE 過渡期的獲利輪廓｜答法：CEO 以「hill than a cliff」「shallow dip」作答，未給 EPS 或營收數字，並說「still potential more to do」
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Courtney Breen（Bernstein）問 LIPFENDRA 何時上架 TrumpRx｜答法：Rob 說待初始上市後上架，只說 more to come on timing，未給時點
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Luisa Hector（Berenberg）問標示文字對支付方的影響，以及 GLP-1 使用下降是否影響 LIPFENDRA CVOT｜答法：Dean Li 先說須小心談 FDA 意圖，只答標示與 CVOT 2029 時點，未回應 incretin 使用下降對試驗的影響
- MRK_Q2_2026_Earnings_Call_20260804.md｜問：Michael Yee（UBS）問 tulisokibart UC 第三期輪廓（稱公告內容不多）及纖維化論點｜答法：Dean Li 未談 UC 第一項試驗的療效數字，轉述等待第二項試驗讀數；SSc-ILD 部分以「沒有抗細胞激素藥有效」及安慰劑組為由解釋
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md｜問：TroFuse-010 規模與讀數時間是否不變｜答法：未直接回答，改請看 ct.gov
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md｜問：sac-TMT 是否使用 CNPV、PDUFA 能否提前｜答法：未回答是否使用 CNPV，只說提交後都會拿到 PDUFA 日期
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md｜問：是否以 MK-2010+sac-TMT 對戰 KEYNOTE-189、適用組織型｜答法：稱問題為 leading question，只說 stay tuned
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20261026.md｜問：Phase III 非比例風險分析與 FDA 討論｜答法：拒絕透露與 FDA 討論，答 stay tuned

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
{"date":"20260929","verdict":"迴避","role":"不持有","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤120 美元（約 FY2027 共識 12.6 倍）","irr_base_pct":-1.0,"ev5y_pct":-8.9,"drift_watch_prior":{"dca_verdict":"迴避","dca_role":"不持有","signal":"C","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":"↓","runway_post_y5":"🟡","asym_ratio":0.5,"ev5y_pct":-8.9,"irr_base_pct":-1.0,"max_dd_pct":-48,"bull_5y_price":198.4,"bear_5y_price":83.6,"p_bull_pct":20,"p_bear_pct":30,"rearm_trigger":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤120 美元（約 FY2027 共識 12.6 倍）","price_at_dd":148.69,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
