你是 stock-analyst **v20 判斷 agent**，標的 GS（20261017）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GS","date":"2026-10-17","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GS_20261017/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GS_20261017/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenues_gaap","label":"Net revenues（GAAP）","value":18679,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"US$ million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 earnings results 8-K（sec.gov，公司正式財報稿）"},"note":"YoY +23%（3Q25: 15,184）；QoQ -8%（2Q26: 20,338）"},{"id":"f_kpi1_pre_tax_earnings_pre_tax","label":"Pre-tax earnings／pre-tax margin（銀行無 non-GAAP 營業利益；以稅前利益代營業利益）","value":7003,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"US$ million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K；pre-tax margin 37.5% 為由 7,003/18,679 自算"},"note":"未取得"},{"id":"f_kpi2_total_operating_expenses","label":"Total operating expenses","value":11308,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"US$ million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K"},"note":"未取得"},{"id":"f_kpi3_net_earnings","label":"Net earnings","value":5294,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"US$ million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K"},"note":"未取得"},{"id":"f_kpi4_diluted_eps","label":"Diluted EPS","value":17.01,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"US$","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K"},"note":"第三方報導 consensus 約 $13.02（非公司來源，僅供參考）"},{"id":"f_kpi5_compensation_benefits_ra","label":"Compensation & benefits ratio（自算：5,122/18,679）","value":27.4,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K 數字自算"},"note":"未取得"},{"id":"f_kpi6_provision_for_credit_los","label":"Provision for credit losses","value":368,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"US$ million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K"},"note":"未取得"},{"id":"f_kpi7_annualized_roe","label":"Annualized ROE","value":18.7,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K"},"note":"9M26 ROE 20.7%"},{"id":"f_kpi8_cet1_ratio_standardized_","label":"CET1 ratio（standardized，preliminary）","value":12.4,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K"},"note":"advanced 13.6%（持平）"},{"id":"f_kpi9_assets_under_supervision","label":"Assets under supervision（期末）","value":4097,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"US$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K"},"note":"YoY 對 3Q25 3,452"},{"id":"f_kpi10_share_repurchases_divide","label":"Share repurchases／dividends","value":3.0,"period":"3Q26（季末 2026-09-30，公告於 2026-10-13）","unit":"US$ billion（回購；股利 1.49B）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"3Q26（季末 2026-09-30，公告於 2026-10-13）","citation":"GS 3Q26 8-K（回購 2.9M 股、均價 $1,048.73；4Q26 股利 $5.00／股）"},"note":"注意：稿載均價 $1,048.73 高於 price_at_dd 881.26，需核對是否為抽取誤差"},{"id":"f_kpi11_management_guidance","label":"Management guidance","value":"無明確財測","period":"3Q26（公告於 2026-10-13）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"3Q26（公告於 2026-10-13）","citation":"GS 3Q26 8-K：未提供營收／獲利／費用指引；僅提及 investment banking fees backlog 較 2Q26 下降、較 2025 年底略降"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-13","period":"2026-10-13","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-13"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_gs_fcf_margin_pct","label":"GS FCF 利潤率","value":-62.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jpm_fcf_margin_pct","label":"JPM FCF 利潤率","value":-83.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JPM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ms_fcf_margin_pct","label":"MS FCF 利潤率","value":-25.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bac_fcf_margin_pct","label":"BAC FCF 利潤率","value":73.37,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wfc_fcf_margin_pct","label":"WFC FCF 利潤率","value":22.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WFC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":881.26,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-3.94,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":34.33,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-3.67,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（70.36 → 67.78）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-1.2,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（73.55 → 72.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.1,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（76.81 → 76.73）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":67.78,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":72.67,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":76.73,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-5.43,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 71.67 → 67.78（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":12.67,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝30.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":30.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.61,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝48.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":48.1,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.22,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":13.21,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 67.78，分子＝快照價 895.32","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.043,"period":"2026-10-17","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-17"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-169999.99,"period":"2026-10-17","unit":"USD m","basis":"yfinance 最新一季：總債務 839000.0、現金 1008999.99（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":291.17,"period":"2026-10-17","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":86597.71,"period":"2026-10-17","unit":"USD m","basis":"市值 256597.7 ＋ 淨負債 -169999.99","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":72675.61,"period":"2026-10-17","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":73812.04,"period":"2026-10-17","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.19,"period":"2026-10-17","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"2026年上半年 Goldman 在 EMEA M&A 份額為2018年以來同期最高，對 JPMorgan 的領先幅度較2025上半年的11個百分點縮小；全球 M&A 份額38%。","source":"BusinessDay: Goldman Sachs claims biggest EMEA M&A market share in eight years","url":"https://www.businessday.co.za/world/international-companies/2026-07-05-goldman-sachs-claims-biggest-emea-ma-market-share-in-eight-years/","excerpt":null,"as_of":"2026-07-05","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Dakota 投行排行：Goldman 2Q26 顧問案件數64件仍居第一，較1Q26的73件下降12.3%；Jefferies升至第二，前三名合計案件數由175降至148。","source":"Dakota 2Q26 Investment Bank League Table","url":"https://www.dakota.com/reports-blog/investment-banks-league-table-2q26","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"3Q26 股票交易營收 Goldman 64.4億美元（年增72%），Morgan Stanley 58億美元（年增41%），JPMorgan約50億美元（年增49%）；Goldman 為三者最高。此為營收非份額。","source":"Beinsure: Goldman Sachs Q3 earnings beat as equities jump 72%","url":"https://beinsure.com/news/goldman-sachs-nyse-gs-stock-price-forecast-q3-earnings-beat-as-equities-jump-72/","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"GS 2026 年 6 月 10-Q 載明 Fitch 在第二季將集團母公司展望由穩定調為正面；優先股展望在 DBRS、Moody's、R&I、S&P 為穩定，Fitch 為正面。","source":"Goldman Sachs Group Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000297/gs-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261017","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026-05-12 Fitch 將 Goldman Sachs International（GSI）長期發行人評等由 A+ 升至 AA-，展望維持正面（子公司，非母公司）。","source":"JSE SENS notice on Goldman Sachs International (sharedata.co.za, id=547692)","url":"https://sharedata.co.za/v2/scripts/SENS.aspx?id=547692","excerpt":null,"as_of":"2026-05-12","retrieved_at":"20261017","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 的信用風險集中度揭露為放款組合依類型與地區拆分：約 81% 的約 2,400 億美元放款總額在美洲；搜尋結果未見單一客戶營收集中度揭露。","source":"Goldman Sachs Group Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/886982/000088698226000091/gs-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261017","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2025 年 12 月 Zacks 報告列 GS 長期評等 Fitch A、Moody's A2、S&P BBB+，展望皆穩定（2026 年前基準）。","source":"Zacks research report GS, 2025-12-05","url":"https://advisortools.zacks.com/proxy/ResearchReport/GS/report?d=20251205","excerpt":null,"as_of":"2025-12-05","retrieved_at":"20261017","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"GS Q3 2026 投行費 $3.22B、年增 21%，來自顧問（完成 M&A 增加）與股權承銷（IPO、增發）；公司稱投行費用 backlog 較 2026 Q2 末下降、較 2025 年底略降。","source":"SEC 8-K, Goldman Sachs Q3 2026 earnings results","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000529/a3q26gsearningsresults.htm","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261017","affects":["thesis.H","decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"GS 2026 上半年投行費年增 52% 至 $6.24B（二手來源，需對照申報文件）；股權承銷改善特別明顯。","source":"yourwyominglink.com, Goldman's IB fees jump 52% in 1H26","url":"https://www.yourwyominglink.com/goldmans-ib-fees-jump-52-in-1h26-will-the-uptrend-continue/article_0a820192-75ad-5988-b2e1-192e1ae5fca0.html","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261017","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Solomon 預期 2026 有創紀錄規模的大型 IPO，並指私募股權有逾 $2 兆乾火藥與 AI 融資需求；此為管理層/賣方樂觀看法。","source":"roic.ai, David Solomon forecasts 2026 IPOs unprecedented in size","url":"https://www.roic.ai/news/goldman-sachs-ceo-predicts-unprecedented-ipo-surge-in-2026-fueled-by-private-equity-and-ai-investments-02-13-2026","excerpt":"We're going to see potentially, some very, very large IPOs, unprecedented in size this year","as_of":"2026-02-13","retrieved_at":"20261017","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"2026 年 4 月 Reuters：六大美銀 Q1 投行費平均增約 27%；風險為中東衝突可能延後交易執行；交易由科技/AI、醫療、金融服務領先。","source":"Reuters via Kitco, Wall Street still betting on 2026 deal boom but Middle East unrest adds caution","url":"https://www.kitco.com/news/off-the-wire/2026-04-15/wall-street-still-betting-2026-deal-boom-middle-east-unrest-adds","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"GS 2026年6月30日 10-Q 揭露：2021年起的信用違約交換（CDS）結算價格反壟斷集體訴訟仍在進行，最新列示步驟為被告於2025-10-10提出的判決於訴狀動議；另稱集團內單位面臨其他未具名的監管調查與審查。","source":"SEC EDGAR, Goldman Sachs Group 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000297/gs-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"法院案件列表顯示一件私人反壟斷訴訟 Simon v. The Goldman Sachs Group 於2026-04-30提起；列表未載明實質指控。未查到政府機關（DOJ/FTC/EU）對GS的新反壟斷調查。","source":"案件列表（api.ai-analytics.org/case/73273024）","url":"https://api.ai-analytics.org/case/73273024","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261017","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#none","axis":"reg_tariff_export","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"geo_supply_chain#none","axis":"geo_supply_chain","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"GS 2026Q3 淨營收 186.8 億美元，年增 23%、季減 8%","source":"Goldman Sachs 8-K 3Q26 earnings results","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000529/a3q26gsearningsresults.htm","excerpt":"Net revenues were $ 18.68 billion for the third quarter of 2026, 23% higher than the third quarter of 2025 and 8% lower than the second quarter of 2026.","as_of":"2026-10-13","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Global Banking & Markets 營收 134.6 億美元，年增 32%；權益 64.4 億年增 72%，FICC 34.7 億大致持平","source":"Goldman Sachs 3Q26 earnings (as reported)","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000529/a3q26gsearningsresults.htm","excerpt":"Global Banking & Markets reported net revenues of $13.46bn, up 32% from the third quarter of 2025 and down 13% from the preceding quarter.","as_of":"2026-10-13","retrieved_at":"20261017","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Asset & Wealth Management 營收 50.5 億美元，年增 14%","source":"Goldman Sachs 3Q26 earnings (as reported)","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000529/a3q26gsearningsresults.htm","excerpt":"Asset & Wealth Management recorded net revenues of $5.05bn, 14% above the third quarter of 2025.","as_of":"2026-10-13","retrieved_at":"20261017","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Platform Solutions 營收 1.7 億美元，年減 72%，主因 Apple Card 貸款組合markdown","source":"Goldman Sachs 3Q26 earnings (as reported)","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000529/a3q26gsearningsresults.htm","excerpt":"Platform Solutions net revenues fell to $170m, down 72% year on year.","as_of":"2026-10-13","retrieved_at":"20261017","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"GS 2026上半年投行費用年增52%至62.4億美元","source":"Zacks via yourwyominglink: Goldman's IB fees jump 52% in 1H26","url":"https://www.yourwyominglink.com/goldmans-ib-fees-jump-52-in-1h26-will-the-uptrend-continue/article_0a820192-75ad-5988-b2e1-192e1ae5fca0.html","excerpt":"IB fees jumped 52% year over year to $6.24 billion","as_of":"2026-07-01","retrieved_at":"20261017","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"2026Q3 全球 M&A 量較前三個月下滑41%至9,930億美元，美國IPO自夏季後動能減弱","source":"The Star: Wall Street banks see strong pipeline amid volatility","url":"https://www.thestar.com.my/business/business-news/2026/10/16/wall-street-banks-see-strong-pipeline-amid-volatility","excerpt":"global M&A volumes fell 41% from the prior three months to US$993bil in 3Q","as_of":"2026-10-16","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"2025年GS在LSEG投行費用排名第二（82億美元，JPM 101億居首），M&A顧問金額全球第一","source":"LSEG data via search summary (investmentexecutive/others)","url":"https://www.investmentexecutive.com/?p=116399","excerpt":"Goldman Sachs ranked second with US$8.2 billion.","as_of":"2025-10-01","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"GS 已透過與 BNY Mellon 共建的 GS DAP 平台向機構客戶提供代幣化貨幣市場基金；CEO Solomon 在 Q4 財報電話會稱 GS 不需領先每個新技術趨勢，但要準備好部署；內部團隊正評估代幣化與穩定幣的試驗方向","source":"The Block / Unlock BC 報導 GS CEO 探索代幣化與預測市場","url":"https://www.theblock.co/post/385937/goldman-sachs-ceo-tokenization-stablecoins-prediction-markets-us-regulation","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Citi 報告預估全球代幣化證券市場 2030 年達 5.5 兆美元，稱發行為既有業者的近期機會，預期傳統系統與區塊鏈長期並存；Citi 並推出私人公司代幣化股份平台（WSJ 報導），Morgan Stanley 亦把 RWA 代幣化列為重點（後者來源為 KuCoin 部落格，可信度較低）","source":"The Block 轉述 WSJ：Citigroup to offer tokenized shares of private companies","url":"https://theblock.co/post/404422/citigroup-to-offer-tokenized-shares-of-private-companies-for-wealthy-and-institutional-clients-wsj","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"高盛持續縮減 Platform Solutions 內的消費金融業務（Apple Card 轉予 JPMorgan、GM 卡轉 Barclays），維持三個報告分部","source":"Goldman Sachs Form 10-Q (quarter ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000297/gs-20260630.htm","excerpt":"continued to narrow its strategic focus with respect to consumer-related activities within Platform Solutions","as_of":"2026-06-30","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"高盛以合計 24 億美元收購 Industry Ventures 與 Innovator Capital Management，擴大資產管理與主動型 ETF 能力（二手報導，細節待 10-Q/8-K 核對）","source":"Nasdaq/Zacks 與 Goldman Q2 2026 報導彙整（搜尋摘要）","url":"https://www.nasdaq.com/articles/goldman-or-citigroup-which-transformation-story-more-compelling","excerpt":"The high-profile Apple Card partnership is in the final stages of being offloaded to JPMorgan Chase","as_of":"2026-07-01","retrieved_at":"20261017","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"高盛推行多年期 OneGS 3.0，把 AI 嵌入全公司營運模式，首批工作流含客戶開戶/KYC、企業風險管理、監管報告、銷售支援；量化細節尚未找到公開來源","source":"Fortune, Goldman Sachs CFO on the company's AI reboot","url":"https://fortune.com/2025/12/10/goldman-sachs-cfo-on-the-companys-ai-reboot-talent-and-growth","excerpt":null,"as_of":"2025-12-10","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"GS 2026Q3（10/13公布）稀釋EPS 17.01美元，高於LSEG共識13.02美元","source":"beinsure.com 報導 GS Q3 2026 財報","url":"https://beinsure.com/news/goldman-sachs-nyse-gs-stock-price-forecast-q3-earnings-beat-as-equities-jump-72/","excerpt":"Goldman Sachs reported Q3 2026 earnings of $17.01 per share, exceeding the $13.02 LSEG consensus.","as_of":"2026-10-13","retrieved_at":"20261017","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3投行費3.22億。..實為32.2億美元，年增21%，高於分析師預期約29.7億美元","source":"GS Form 8-K Q3 2026 earnings results／beinsure.com","url":"https://www.sec.gov/Archives/edgar/data/0000886982/000088698226000529/a3q26gsearningsresults.htm","excerpt":"Investment banking fees were $ 3.22 billion, 21% higher than the third quarter of 2025","as_of":"2026-10-13","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"財報前30天內EPS預估17次下修、0次上修（IG／LSEG 財報預覽）","source":"IG 'Goldman Sachs stock Q3 2026 earnings preview'","url":"https://www.ig.com/en-ch/news-and-trade-ideas/goldman-sachs-stock-q3-2026-earnings-preview-261012","excerpt":"17 downward EPS revisions and no upgrades over the past 30 days","as_of":"2026-10-12","retrieved_at":"20261017","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"管理層既有指引：AWM營收高個位數成長、另類募資全年逾1250億美元；Q3非薪酬費用較Q2增約5億美元（財報前評論）","source":"beinsure.com／Hudson Labs Q3 2026 preview","url":"https://www.hudson-labs.com/research/goldman-sachs-q3-2026-earnings-gs-results-preview","excerpt":"Management continues to target high single-digit revenue growth in Asset & Wealth Management, 30% margins, and high teens returns. Alternatives fundraising expected to exceed $125B for the year.","as_of":"2026-10-12","retrieved_at":"20261017","affects":["thesis.H","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布（TickerLeague，14位分析師，近期動作表至2026年7月）：低995、共識1197.33、中位1222、高1325；共識評等Hold（55筆）。與4月Zacks等來源數字差距大，來源品質不一","source":"TickerLeague GS estimates","url":"https://tickerleague.com/companies/GS/estimates","excerpt":"Low $995.00, Consensus $1,197.33, Median $1,222.00, High $1,325.00. Consensus: Hold — based on 55 analyst ratings.","as_of":"2026-07-28","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FN2評等分布：看多22(40.0%)、中立30(54.5%)、看空3(5.5%)，資料截至2026-07-28","source":"fn2.ai GS Analyst Consensus","url":"https://fn2.ai/earnings/gs/analysts","excerpt":"Bullish 22 (40.0%), Neutral 30 (54.5%), Bearish 3 (5.5%)","as_of":"2026-07-28","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"高盛以 6.65 億美元現金與股權收購創投平台 Industry Ventures，另有至多 3 億美元績效或有對價（至 2030）；已完成交割。交割日期搜尋摘要未載明。","source":"AJ Bell: Goldman Sachs closes Industry Ventures acquisition","url":"https://streaming1.beta.ajbell.co.uk/articles/latestnews/295448/goldman-sachs-closes-industry-ventures-acquisition","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"高盛 2025 年 12 月宣布收購 Innovator Capital Management（約 20 億美元），預計 2026 年 Q2 完成；搜尋未找到交割確認。","source":"Sewkis IM Deals Blog: Goldman Sachs to Acquire Innovator","url":"https://imdealsblog.sewkis.com/goldman-sachs-to-acquire-innovator","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"1MDB 證券集體訴訟（Sjunde AP-Fonden v. Goldman Sachs）仍在審理；SDNY 於 2025-09-04 裁定認證集體，適用 2016-12-22 至 2018-11-08 買入普通股的投資人；搜尋未見和解或實質裁決。","source":"KTMC court-approved class notice (Feb 2026)","url":"https://www.ktmc.com/wp-content/uploads/2026/02/Goldman-Notice-FINAL.pdf","excerpt":null,"as_of":"2025-09-04","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"高盛以 6.65 億美元現金與股權收購 Industry Ventures，另有至多 3 億美元或有對價（至 2030）；已完成交割。","source":"AJ Bell: Goldman Sachs closes Industry Ventures acquisition","url":"https://streaming1.beta.ajbell.co.uk/articles/latestnews/295448/goldman-sachs-closes-industry-ventures-acquisition","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2025 年 12 月宣布收購 Innovator Capital Management（約 20 億美元），預計 2026 Q2 完成；未見交割確認。","source":"Sewkis IM Deals Blog: Goldman Sachs to Acquire Innovator","url":"https://imdealsblog.sewkis.com/goldman-sachs-to-acquire-innovator","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"1MDB 證券集體訴訟仍待審；SDNY 2025-09-04 裁定認證集體（買入期間 2016-12-22 至 2018-11-08），2026 年 2 月有法院核定的集體通知。","source":"KTMC court-approved class notice (Feb 2026)","url":"https://www.ktmc.com/wp-content/uploads/2026/02/Goldman-Notice-FINAL.pdf","excerpt":null,"as_of":"2025-09-04","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：gross_margin_pct、operating_margin_pct、rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"GS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-62.71,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GS","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"JPM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-83.39,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JPM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-25.44,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MS","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"BAC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":73.37,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WFC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":22.09,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WFC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"GS"},"financial_history":{"ticker":"GS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":47365000000.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":11261000000.0,"diluted_eps":30.06,"free_cash_flow":4960000000.0,"fcf_margin_pct":10.47,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":46254000000.0,"revenue_yoy_pct":-2.35,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":8516000000.0,"diluted_eps":22.87,"free_cash_flow":-14903000000.0,"fcf_margin_pct":-32.22,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":53512000000.0,"revenue_yoy_pct":15.69,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":14276000000.0,"diluted_eps":40.54,"free_cash_flow":-15303000000.0,"fcf_margin_pct":-28.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":58283000000.0,"revenue_yoy_pct":8.92,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":17176000000.0,"diluted_eps":51.32,"free_cash_flow":-47218000000.0,"fcf_margin_pct":-81.02,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GS/GS_Q3_2026_Earnings_Call_20261013.md）

# Q3 2026 Earnings Call
**The Goldman Sachs Group, Inc.** | Earnings Calls | 2026-10-13

**Operator** (Operator):
Good morning. My name is Katie, and I will be your conference facilitator today. I would like to welcome everyone to The Goldman Sachs Third Quarter 2026 Earnings Conference Call. On behalf of Goldman Sachs, I will begin the call with the following disclaimer. The earnings presentation can be found on the Investor Relations page of The Goldman Sachs website and contains information on forward-looking statements and non-GAAP measures.
This audiocast is copyrighted material of The Goldman Sachs Group, Inc., and may not be duplicated, reproduced or rebroadcast without consent. This call is being recorded today, October 13, 2026. I will now turn the call over to Chairman and Chief Executive Officer, David Solomon; and Chief Financial Officer, Denis Coleman. Thank you. Mr. Solomon, you may begin your conference.

**David Solomon** (Executives):
Thank you, operator. Good morning, everybody. Thank you for joining us. We delivered very strong performance in the third quarter, generating net revenues of $18.7 billion, the second highest in our history, earnings per share of $17.01, an ROE of 18.7% and an ROTE of 20.5%. Our quarterly results included the impact of an accelerated charitable contribution. Excluding that contribution, quarterly EPS would have been approximately $18, and ROE and ROTE would have been approximately 20% and 21.5%, respectively. For the year-to-date, we delivered record revenues driving an ROE of 20.7% and an ROTE of 22.4%. 
While the third quarter began with optimism around a potential resolution of the conflict in the Middle East, renewed geopolitical tensions and continued disruption of energy flows added complexity to the outlook, increasing oil prices, reigniting inflation concerns and driving bond yields higher. 
Against this backdrop, the Fed raised rates in September for the first time in 3 years, with markets pricing in approximately 75 basis points of additional tightening in this cycle across the U.S., U.K. and Europe. Despite these crosscurrents, the health of the underlying U.S. economy has remained solid, with strong corporate earnings growth, GDP growth of 2.2% and a very resilient labor market. In complex environments such as these, clients rely on the advice, execution and intermediation expertise of Goldman Sachs to navigate uncertainty and advance their most important strategic priorities. 
In Global Banking & Markets, we generated the second highest revenues in our history. Within Investment banking, advisory revenues were a record, and we maintained our longstanding #1 position in M&A, advising on $1.5 trillion of announced transactions for the year. We maintained our year-to-date lead over our closest peer of approximately $430 billion, the largest lead we've ever had, as clients turn to us for advice on significant transactions, including Hugging Face's $13 billion sale to NVIDIA and Integer Holdings' $6 billion sale to KKR. As you'll remember, we entered the quarter with our highest backlog in 5 years. And even with exceptionally strong revenue production in the quarter, our backlog remains very robust, reflecting the strength and breadth of client engagement across our leading Investment banking franchise. 
In Equities, we delivered our second-best performance after last quarter's record results, with strength across both intermediation and financing. In FICC, we remain steadfast in supporting our clients' global risk intermediation needs across asset classes amid sharp moves in rates and increased volatility in commodities. Importantly, financing activities have become a larger and more durable component of our markets businesses, representing over 40% of FICC and Equities revenues year-to-date. 
This progress reflects strong client demand, prudent balance sheet deployment and continued execution against our strategic priorities, including deliberate multiyear investments in Asia, which we highlighted earlier this year as an opportunity to drive further share gains. This dynamic market backdrop has also reinforced the importance of trusted advice and diversified investment solutions for Asset & Wealth Management clients. Our scaled and durable platform brings together leading investment capabilities across public and private markets and delivers them through deep institutional relationships, our ultra-premier high net worth Wealth Management franchise and our expanding third-party distribution network. The strength of this platform continues to drive exceptional growth at scale. 
In the third quarter, management and other fees increased 22% year-over-year to a record $3.6 billion and surpassed $10 billion for the year-to-date. Our assets under supervision reached another record of $4.1 trillion, supported by $97 billion of long-term net inflows, representing our 35th consecutive quarter of inflows. In Wealth Management, $47 billion of long-term net inflows contributed to record client assets of $2.1 trillion. For 2026, Wealth Management long-term net inflows are annualizing at 12%, well ahead of our 5% target, which underscores the strength of our client relationships built on trust and long-term performance. 
In alternatives, we are driving strong growth, with alternative assets under supervision up 26% year-over-year to a record $491 billion. We continue to see strong momentum in fundraising, with $37 billion raised in the quarter, driving a total of $122 billion in fundraising for the year-to-date, reflecting investor demand for experienced investment managers. Considering the strength, we now expect full year fundraising of roughly $150 billion. 
Given the sustained levels of investment performance for clients, our leading Asset & Wealth Management business remains very well positioned for continued growth amid attractive secular tailwinds. At the same time, we are also inorganically accelerating growth and building a stronger platform with a better product offering for clients. In August, we announced agreements to acquire NEOS, a market leading -- a market leader in derivative income ETFs with approximately $35 billion in AUS at quarter end, and LCN Capital Partners, a leading triple net lease investment manager. The NEOS acquisition would bring our global active ETF assets under supervision to over $90 billion, establishing Goldman Sachs among the top 8 providers by assets under supervision and top 6 by revenue, while LCN broadens the range of private real estate investment solutions we can offer. Importantly, these acquisitions also bring talented and entrepreneurial teams to Goldman Sachs. 
We remain focused on opportunities that enhance distribution, deepen investment capabilities and add products to strengthen Asset & Wealth Management. Our bar for strategic financial and cultural fit remains very high, and we will continue to allocate capital dynamically and with discipline as we drive growth. All in, our record year-to-date revenues are the result of years of focused execution that have strengthened our market-leading businesses and increased connectivity across the firm as we harness the power of One Goldman Sachs. 
Importantly, we have created a higher revenue base with our more durable revenues having more than doubled since 2020 Investor Day, and now representing approximately 45% of revenues for the year-to-date. The increased durability, coupled with our expense discipline and prudent capital management, enhances the resilience of our earnings and supports higher returns through the cycle, providing Goldman Sachs with an even stronger foundation for growth.
Looking forward, though uncertainty persists, corporates and investors recognize that standing still can be a competitive disadvantage. Clients are taking action to modernize operations, secure critical capabilities and reallocate capital towards their highest return opportunities. All of this is driving demand for M&A, capital formation, financing, risk management and advice, playing directly to the strength of our franchise. An ongoing theme has been the growth in AI infrastructure investment. Recent studies estimate that the U.S. data center build-out could require north of $10 trillion in investment through 2032, averaging roughly 3.6% of U.S. GDP annually.
In our conversations with clients, demand for compute significantly exceeds supply at the moment, creating opportunities to help develop financing structures to meet that capacity shortfall. Our differentiated financing, distribution and investing capabilities position us to play a meaningful role in the mobilization of capital and supporting client activity. While we are proud of the privileged position we play in the AI investment cycle, no one knows how the demands for capital and compute will evolve as the broader AI ecosystem matures. That will only become clearer as technology and markets continue to develop. 
This uncertainty reinforces the importance of remaining vigilant around the types of activity we finance and how we manage risk as we support our clients. We are highly selective about the risk we underwrite and the capital we commit, particularly as client financing needs become larger and more complex. Beyond these financial risks, we also recognize the broader concerns around the accelerating pace of AI technology and the unchecked advancement of frontier models.
Like other transformative technologies, AI presents significant opportunities, but also significant risks that must be carefully assessed and managed. However, the choice is not between halting progress and moving forward without guardrails. We must enable innovation and also demand responsibility. The experience of the financial services industry has demonstrated the value of rigorous testing, independent review and continuous monitoring and clear human accountability. These principles, applied in ways that reflect the unique characteristics of AI, can help build the trust and confidence needed to deploy the technology responsibly at scale while companies, developers and governments work together to establish appropriate safeguards.
All in, we continue to see meaningful opportunities ahead of us. We are incredibly well positioned given our relentless focus on serving our clients while remaining vigilant to emerging risks in this dynamic environment. Our culture of teamwork, excellence and partnership remains a key differentiator that has enabled us to adapt, innovate and execute through a range of environments. I've never been more confident in our ability to create long-term value for shareholders by making the right investments to grow the firm and generate sustainable earnings growth. With that, I'll turn it over to Denis to walk through our financial results in more detail.

**Denis Coleman** (Executives):
Thank you, David. Good morning, everyone. Let's start with our results on Page 1 of the presentation. In the third quarter, we generated net revenues of $18.7 billion, earnings per share of $17.01, which drove a quarterly ROE of 18.7% and ROTE of 20.5%. 
Turning to segment performance, starting on Page 3. Global Banking & Markets revenues were $13.5 billion in the third quarter, our second highest quarterly revenues, contributing to a segment ROE of 23.5% for the year-to-date.
Moving to Page 4. Advisory revenues of $1.7 billion reached a quarterly record and rose 18% year-over-year, driven by higher volumes. For the year-to-date, we maintained our #1 league table position for announced and completed M&A volumes. In equity underwriting, revenues of $666 million rose 43% year-over-year on strong IPO and secondary offerings activity. In debt underwriting, revenues were $904 million, up 15% year-over-year, driven primarily by stronger investment-grade activity. Year-to-date, we ranked #1 in equity underwriting, #2 in leveraged loans and #3 in high-yield debt underwriting. 
Even amid very strong accruals in the quarter, our Investment banking backlog remains very robust, as strong revenue realizations in advisory were largely offset by solid replenishment in equity underwriting. Year-to-date sponsor share of announced M&A remains below historical averages, presenting further upside when activity picks up. FICC net revenues were essentially unchanged year-over-year. Intermediation revenues declined 7%, as lower results in mortgages, rates and credit were largely offset by strong performance in currencies and commodities. Financing revenues increased 14% to their second highest level, driven by strength in mortgages and structured financing. 
Equities net revenues were $6.4 billion, up 72% year-over-year, representing our second best quarter, driven by strong performance in both intermediation and financing. Equities intermediation revenues rose 52% to their second highest level driven by strength in derivatives. Equities financing revenues rose 96% to a record, driven primarily by elevated average prime balances and strong activity across Asia. Demand for Equities financing continues to exceed available industry capacity, supporting attractive pricing and allowing us to remain selective in deploying resources. 
Following significant multiyear investment, our focus is increasingly on optimizing a diversified global portfolio, guided by our risk management framework, client relationships and returns. More broadly, we continue to see structural tailwinds for the growth in tradable assets and the increasing financing needs associated with those assets, which have helped to support sustained industry growth in Equities financing over time. Year-to-date, total financing revenues of $12.7 billion were a record and represented over 40% of combined FICC and Equities revenues. As David mentioned, growth in financing revenues has contributed to greater durability in FICC and Equities, and is underpinned by a robust risk framework that includes diversified exposures, limits, concentration management and comprehensive stress testing.
Let's turn to Page 5. Asset & Wealth Management revenues were $5.1 billion, up 14% year-over-year. Management and other fees rose 22% year-over-year to a record $3.6 billion, reflecting the impact of higher average assets under supervision. Incentive fees were $587 million. Through our ultra-high net worth Wealth Management franchise, we provided clients early access to a high-growth investment opportunity and recognized incentive fees following the company's IPO. Based on our current outlook, we expect incentive fees to remain elevated in the fourth quarter. Private banking and lending revenues were $827 million, up 20% sequentially, driven by higher net interest from consumer deposits. Loan balances were up 6% to $51 billion. Investments revenues were $50 million, given the timing of certain monetizations following a strong second quarter and certain markdowns.
Now moving to Page 6. Total assets under supervision ended the quarter at a record $4.1 trillion, supported by $97 billion of long-term fee-based net inflows, marking our 35th consecutive quarter of long-term fee-based net inflows. Wealth Management client assets reached another record of $2.1 trillion, with $47 billion of long-term net inflows.
Turning to Page 7. Alternative assets under supervision totaled $491 billion at the end of the third quarter, driving $860 million in management and other fees, the best performance since our 2020 Investor Day. Gross third-party alternatives fundraising was $37 billion for the quarter and $122 billion for the year-to-date.
On Page 9, firm-wide net interest income was $3.8 billion. Our total loan portfolio increased 6% from the prior quarter to $276 billion, reflecting broad-based growth across the portfolio. Our provision for credit losses was $368 million. While overall credit quality and portfolio performance have remained strong, our provisions reflected certain impairments across our portfolio as well as overall growth in lending.
Turning to expenses on Page 10. Total operating expenses were $11.3 billion for the quarter. For the year-to-date, total operating expenses were $33.4 billion for an efficiency ratio of 59.4%, improving 270 basis points from the prior year and in line with our target. Our year-to-date compensation ratio net of provisions was reduced to 30%. We remain committed to paying for performance and delivering operating leverage for shareholders. Quarterly non-compensation expenses were $6.2 billion, 30% higher year-over-year, driven largely by higher transaction-based expenses. 
Additionally, given the strong pull-through of incentive fees this quarter, we made a tax efficient charitable contribution of approximately $450 million as part of a planned acceleration of our philanthropic efforts. We also expect to make a meaningful contribution in the fourth quarter. Together, these actions will pull forward at least 5 years of planned charitable giving. The impact of our charitable contributions on quarterly EPS was approximately $1, while the impact on ROE and ROTE was approximately 1.1 percentage points each. Our effective tax rate for the year-to-date was 20.4%. And for the full year, we continue to expect an effective tax rate of approximately 20%.
Now on to Slide 11. Our common equity Tier 1 ratio was 12.4% at the end of the third quarter under the standardized approach, 100 basis points above our current capital requirement of 11.4%. Regarding recent regulatory developments, we welcome the Federal Reserve's rule finalization to enhance the transparency and accountability of the CCAR stress test and reduce the volatility of capital requirements. We also recognize the progress of the Basel III endgame and G-SIB reproposals and are hopeful for finalization by the end of the year. Collectively, these developments represent meaningful progress towards a more balanced and risk-sensitive regulatory capital framework that preserves the strength and resilience of the banking system.
As the rules are finalized, we support appropriately calibrated requirements that are aligned with the risks firms actually take and look forward to the timely completion of these reforms. We expect regulatory focus to soon shift towards liquidity regulation reform. We currently have over $570 billion in average global core liquid assets, representing approximately 25% of our total assets, and our liquidity coverage ratio is among the highest in our peer group. In the quarter, we repurchased $3 billion of our common stock and paid $1.5 billion in dividends. We continue to have significant capacity to deploy capital prudently in service of clients while maintaining an appropriate buffer.
In conclusion, our third quarter performance reflects the strength of our client franchise, which has been bolstered by years of strategic execution. We've built market-leading franchises, deep relationships and a higher and more durable revenue base. We remain focused on delivering strong returns while continuing to invest in our people, technology and client franchises to drive long-term earnings growth and deliver for our shareholders. With that, we'll now open up the line for questions.

**Operator** (Operator):
[Operator Instructions] We'll take our first question from Glenn Schorr with Evercore ISI.

**Glenn Schorr** (Analysts):
First one on trading and markets, the results are nothing short of awesome. There's a short-term and long-term question I have. The short term is just simple. Is there anything unique in the quarter like related situational awareness or anything like that would contribute to the quarter such that we don't over model in the fourth quarter?
But the bigger picture question I want to ask you is, there's so many developments going on, tokenization, agentic trading, DeFi vaults, prediction markets. All these theoretically would nip at the core of your great markets business, but obviously you're not standing still. So maybe you could talk about where you're making investments and how you see some of those things, how we should think about that in conjunction with your markets platform.

**David Solomon** (Executives):
Sure. Thanks, Glenn. On the first point, I don't see anything that I would call out. Denis, do you...

**Denis Coleman** (Executives):
No. I agree with that.

**David Solomon** (Executives):
Yes. I don't see anything I'd call out just on the first thing, just to put that aside. On your second question, obviously we've seen market structure evolve with technological advancements over long periods of time. We've talked about that for a long time, and as a leading market maker and risk intermediary, we have to continue to invest in technologies, infrastructure capabilities to make sure we're supporting our clients at the cutting edge, and I think we continue to do that. I know you'll remember, Glenn, that it was not too long ago that people were concerned about electronification in Equities trading and its impact on our business. But as we sit here today, the opportunity set for us is greater than what anyone could have contemplated when you look at our equity revenues and the way we adjusted and the way the business has evolved. 
Today, tokenization is obviously an important trend. We see it across asset classes. We were publicly supportive of CLARITY passing. It wasn't perfect, but we thought it would be good to give the market more clarity, no pun intended, and ensure investor protection. But in the absence of that, we're already seeing agencies take steps to provide clearer rules for the market, and we're very engaged in those dialogues. We continue to invest and closely monitor the developments, both for opportunities but also for risks. The developments are obviously creating more products, greater activity, potentially new clients, broader distribution channels. And naturally, when you look at these things, they expand the TAM for our business, and that's one of the things that's interesting and exciting.
At the same point, we remain very focused on ensuring that we're well positioned to serve our clients as these markets evolve. We've been investing in companies in the digital asset, broader market infrastructure space for years and remain very focused on that. We've been building capabilities such as the GS DAP, where we were early in building our own rails for digital assets. We've tokenized bonds. We have a number of money market funds that are tokenized, real estate for certain clients, and so we've been focused on trying to be at the edge of some of those activities, although I'd say broadly, those activities are very small at this point.
And we're participating in a range of market developments. In July, we participated in the launch of DTCC's tokenization service, and we're now actively assessing scalable use cases that we could put within it. We expect over time, the underlying technology can drive greater efficiency, automation, streamline processes, reduce costs, take away friction, improve liquidity across asset classes. And so we're going to remain focused on this. I think you're right to raise it as something that requires attention, but I'd say the activity so far is small and at the margin. But we're going to continue to have real resources thinking about how these changes can evolve over time. I think it's one of the reasons when you think about, for example, electronification, we've managed to manage disruption and change in the equity business so well. And so we use that as a little bit of a guideline. So I hope that's some helpful color.

**Glenn Schorr** (Analysts):
Yes, you haven't put any thought into it. No, I'm kidding. That was very helpful. So I've covered you guys since, I guess, the IPO. I've seen some transitions in management, and Goldman just gets stronger each step of the way. This one seems to be being managed pretty methodically. There were just some articles recently that talked about an acceleration. So I don't know, David, if you want to address any of that just to keep the record straight. I appreciate it.

**David Solomon** (Executives):
No, sure. And I appreciate the question because some of the articles, the articles create noise. And I'd just start with, Glenn, I'm super pleased with the progress the firm has made since we laid out our strategy at our Investor Day. The execution, this team has worked to really grow the firm significantly, and I think we've really made it increasingly durable. And I have to say, at the point we're at now where we see the benefits of the effort that the broad team has made, I'm really enjoying the job. 
But more importantly, as a team, we're super excited about what's in front of us in the coming years and how we can continue to grow the franchise and really accelerate the earnings potential of the firm. So I just want to be clear, there is no succession transition or time line underway at Goldman Sachs. The Board and I are singularly focused on our strategy to grow the firm and continue to serve our clients with excellence.

**Operator** (Operator):
We will take our next question from Erika Najarian with UBS.

**L. Erika Penala** (Analysts):
David, you answered this question in your prepared remarks, so maybe the more nuanced way to ask it is, there has been a lot of fears in the investor community that the bond market rout globally was going to have a chilling effect on activity levels. And given sort of how you framed the pipeline, maybe talk about how discussions have evolved or take into account higher long-end rates and if that's a factor.
And just a compound question because I have to be on TV in 5 seconds. If we think about the capital consumption in the fourth quarter, clearly, capital came in 50 basis points lighter. You still have plenty of excess. JPMorgan mentioned that the fourth quarter should be super active in trading and should not have a seasonal slowdown. How should we think about capital consumption going forward?

**David Solomon** (Executives):
Well, just quickly on capital consumption. We talk about running with a 50 to 100 basis point buffer. We're at 100 basis point buffer. The firm has very good earnings momentum, so we generate capital. We feel comfortable with the fact that we have adequate capital to deploy in an active quarter in the fourth quarter. And so we feel like we're managing that well. We continue to feel very nimble about our ability to manage our capital allocation effectively, clients first, then when we can't deploy back to shareholders.
On the first topic, just around rates and the effect on activity, we did see in the quarter a very meaningful move in rates. I think from the beginning of July to now, we've seen a 75 basis point move on the 10-year, approximately, don't hold me exactly to that, but a 75 basis point move on the 10-year. But I think one of the things that's lost is that historical perspective on term Treasury premium because we've really operated since the financial crisis in a rate -- in an environment where rates are fundamentally low. As a 64-year-old guy, I, kind of, look back at the last 64 years, and a 5% 10-year Treasury doesn't scare me in terms of an operating environment. In fact, the overwhelming periods of time in my life, the 10-year Treasury has been higher than the level that it's in. And so we can have very, very effective capital markets with that.
What creates headwind for markets is when you have very, very abrupt moves. Yes, we had a meaningful move in the quarter. There were probably some days when it was abrupt, but you've got a lot of other things going on that are very, very important. We have a very, very strong underlying economy. The economy continues to be very, very resilient despite some of the headwinds. We have an extraordinary tech super cycle. I think we have a regulatory environment that is really encouraging strategic activity to continue to grow scale. And you put these things all together and you balance it, and I think it's a pretty good environment. So I know people looked at the quarter and felt that it felt a little different than it did in the second quarter. And I think that's fair.
I would say that if I go back to the end of May or June, I would call it like a top, top decile environment for, kind of, market activity and capital markets activity. But now we're in a top quartile environment, and that's still really, really good when you think about long periods of time. So we feel quite good about the activity levels. Obviously, if there was a lot more interest rate volatility, that could create headwinds, but we'll watch markets carefully. And at the moment, as we look at activity levels, they feel good.

**Operator** (Operator):
We will take our next question from Ebrahim Poonawala with Bank of America.

**Ebrahim Poonawala** (Analysts):
I guess first question, David, I think Hock Tan from Broadcom, I think he was speaking overnight, and he, kind of, questioned the sustainability of like the AI CapEx financing. And just -- you are obviously part of the group with Jensen during the quarter. One, do you share that concern that the real choke point for AI CapEx will be financing, especially given rates moving higher, it's unclear what the returns look like. Frame that for us, given you probably have one of the best visibilities on what the appetite looks like.

**David Solomon** (Executives):
I think, Christian, it's -- I mean it's a very, very good question -- Ebrahim, I'm sorry. Yes, I apologize. I'm looking at a screen here...

**Ebrahim Poonawala** (Analysts):
I've been called a lot worse in life, so it's okay.

**David Solomon** (Executives):
I apologize because Christian's next. And so I looked at the screen quickly, I apologize. So Ebrahim, it's a really good question, and I'm probably going to disappoint you in my answer, which is I don't know, and nobody knows. What I would say, and you saw it in our remarks, we are extremely conscious of the fact that the expectations for the quantum of financing that's necessary to build out the data center infrastructure in the United States, based on what people are predicting, is quite significant. And over time, there is risk. There is risk to pressure on crowding out the size of scale. Not every project's going to be received as well.
And so we feel very lucky, and I said this in the prepared remarks, we sit in the center of that ecosystem, but we also recognize we have an extraordinary obligation to be very disciplined about what we underwrite. And I just -- I think generalized comments about the direction of travel and what will happen, I think we've got to be very cautious about that. There is going to be a lot of financing to do, and we're going to be in the middle of that. It may be over time, as the financing needs grow, that there's pressure on rates, and that will affect the returns and the viability of certain projects. It's our job as an intermediary, as an asset manager, as a capital provider, to sort through that and make prudent decisions. And I think we're very good at that, and we will.
But one thing's for clear, there's a lot of demand for compute at the moment. The supply has not come into balance. More is going to get built. More financing is going to be necessary. There will be a point in time when this recalibrates, resets, for sure. And when that does happen, of course, there'll be some bumps. But it's very, very hard to predict that. And I think broad assertions that any of us know the direction of travel, how the technology will be evolved, how it will be deployed, that's just an unknown we have to live with. But it's an exciting time because there's going to be a lot of really interesting things to do around that.

**Ebrahim Poonawala** (Analysts):
Got it. And I guess one other question. Improving and durable earnings have been a big focus for you. Help me solve for this, like when we look at the growth in prime and equities financing, you could make the argument that it's adding to the cyclicality of the business, if there's like deleveraging among hedge funds, et cetera. And sure, like I'm not talking about quarter-to-quarter volatility, but how should we think about equity financing actually making these earnings more durable versus adding to the cyclicality? Like how would you sort of think through that, if you could help us?

**David Solomon** (Executives):
Yes, sure, Christian. I mean, Ebrahim, again...

**Ebrahim Poonawala** (Analysts):
You must love Christian, I guess.

**David Solomon** (Executives):
No, I actually love Ebrahim and Christian. I love everybody. So I think the way to think about this is we all have to -- this is the way we think about running the firm. You have to step out of quarter-to-quarter, okay? None of us here, as we risk manage in our prime business, are confused. Equity markets go up. Equity markets come down. Okay, when equity markets come down, okay, there's a deleveraging, okay? And the size of the prime business because of the needs that our clients have to be financed with a smaller equity market, a smaller market cap, there's going to be some cyclicality to that. However, if you step back and you get out of quarter-to-quarter movements and you fundamentally believe in growth in the world, and therefore GDP growth in the world, and therefore growth in market cap and technology innovation over any 3- to 5-year period, the durability of the growth of that business at some baseline is going to be very attractive for Goldman Sachs.
And so when you step out of the quarter and you think over 3, 5, 7 years, and you've really seen this, look, we've grown our revenues over the last 5 years since 2022 by 11% compounded on the top line. I do not believe we're going to grow our revenues by 11% compounded on the top line for the next 5 years. There will be stops and starts as equity markets move around. But what we're trying to prove out is that the durable base is much bigger. It's a much more diverse business. And fundamentally, it's very correlated to GDP growth and equity market cap growth over time. And if we stop looking quarter-to-quarter and stop looking and start looking at 3- to 5-year periods and look at the earnings growth that's driven, you get a very, very constructive result.

**Operator** (Operator):
We'll take our next question from Christian Bolu with Autonomous Research.

**Chinedu Bolu** (Analysts):
And feel free to call me Ebrahim...

**David Solomon** (Executives):
I was going to call you Ebrahim. I was going to call you Ebrahim, just to level the playing field.

**Chinedu Bolu** (Analysts):
Yes. I guess first one, David, just on the IB cycle here. I'd love to get some color on where you think we are in the cycle. The macro seems to be marginally more challenging, higher rates. We've seen a bunch of IPOs get pulled. We probably get a change in the political climate post-U.S. midterm elections. Your backlog seem impressive, but they did pull back a little bit. So just give me a sense of where you think we are in the cycle. Have we peaked or is there more to go?

**David Solomon** (Executives):
I know everybody wants to call the peak. It's hard to call the peak, but let's just step back. And I want to go back to something I said just a little bit earlier, I still think for capital markets activity, it's a top quartile environment. For strategic M&A, there's an enormous amount of dialogue that continues. Our backlog is incredibly robust. It's fair to say that we had enormous accruals in the quarter, but if you listen to our prepared remarks, we were very forward about how robust the backlog remains. 
Capital markets activity is still good. I think one of the things that gets lost, there are obviously a handful of IPOs that didn't move forward. But when you look at ECM revenues for the quarter and for the last few quarters, they're running meaningfully above both 5-year and 10-year averages. So that's a good environment. 5-year and 10-year averages would be a 50%, kind of, capital markets environment. Running meaningfully above 5- and 10-year averages is a better environment. 
And so I think we're still in a very good capital markets environment. I think one of the things that happened with a handful of the IPOs, when people do IPOs, they make a decision months in advance to move forward, and they have a discussion around what the valuation expectation is. And the investors have an expectation. And so IPOs that came in September were really the result of conversations in May and June around valuation expectations. Things got a little bit softer in September. The IPO market was wide open. It's just if you expected a valuation and you got something 10% to 15% less, you might choose not to go forward, you might choose to wait. But the IPO market is still in pretty good shape.
I'd say capital markets activities are strong. There's no question the overall macro environment is a little bit more complicated. The rates environment, a little bit more complicated, but the activity levels that we're seeing are still pretty good, but we'll obviously have to watch through the quarter. I think all the technology innovation and the AI infrastructure activity is a real good ballast for capital markets activity on a go-forward basis. That doesn't mean there won't be bumps in the quarter ahead. But when I look, we're certainly operating in a very good environment for capital markets and Investment banking activity at the moment.

**Chinedu Bolu** (Analysts):
Okay. Very helpful. Maybe just on balance sheet and capital management. Clearly, you're seeing tremendous balance sheet demand as evidenced by the robust growth in your financing business. I am a little bit surprised that you are still buying back a ton of stock at 3x tangible, especially as your SLR is lower than peers. So maybe just talk through how we should think about capital management priorities as you move into 2027.

**Denis Coleman** (Executives):
So Ebrahim, thank you. Thank you for the question. Times 2.

**David Solomon** (Executives):
That's a good CFO.

**Denis Coleman** (Executives):
So look, this is all taken against the backdrop that David's outlined. We're optimistic about the opportunity set. We made decisions over the course of this year following some of the regulatory capital relief to expand our deployment into the client franchise. We also happened to buy a bunch of stock as well. We were generating significant earnings that enabled us both to buy back the stock, buy down our share count, give us capacity to continuously and sort of systematically buy down our shares outstanding over time. Gives us more capacity on the follow, but we were also able to make decisions to fuel the client franchise, which ultimately is delivering the results that we're talking about here in the third quarter.
And I think as we head forward into 2027, I think our -- you should expect our approach to be similar. We will deploy into the franchise as a matter of priority. We do expect to continue to invest in the sustainable growth of our dividend. It's obviously up 25% year-over-year. It's now at $5 a share. It was $4 a year ago. Five years ago, it was $2 a share. So we've been consistently investing in the growth of our dividend. That remains important. And obviously, with excess, we'll return it to shareholders and make sure we have the right buffer to operate the firm. So I think it's a consistent approach to our deployment, including into 2027.

**Operator** (Operator):
We will take our next question from Mike Mayo with Wells Fargo Securities.

**Michael Mayo** (Analysts):
I guess there's been more talk about a headwind to what you described as an extraordinary tech super cycle as it relates to power, labor rates. CapEx has gone from billions to trillions, the climate. And so is funding a constraint for this tech super cycle? And do you -- and is your conviction as strong as it was, say, 3 or 6 months ago? And then on the positive side, you talk about the growth in tradable assets globally. You're expanding in Asia. What has been that growth? What are your numbers around that?

**David Solomon** (Executives):
So on the first part, Mike, you're talking about just enough capital in the markets to fund the growth of all this technology expansion? Or were you talking about our funding? I assume you're talking about just general capital availability to fund the significant AI infrastructure growth?

**Michael Mayo** (Analysts):
Yes. I mean, if bond markets go on strike or if rates go up too much, or just the hiccup, the political hiccups, the pushback against data centers, I know it's not a straight line up, but you still describe it as a tech super cycle. Do you think this is as strong a tech super cycle as you did 6 months ago, for example, given just some of the headlines that we see and the reaction from the technology companies?

**David Solomon** (Executives):
Yes. I do think it's a very strong technology super cycle, Mike, and there's no way to step away from that, okay? The things that you highlight, obviously if there are other factors that create significant interest rate volatility and push rates higher, that will have an impact on the pace of build-out and what projects get done and how they get done. If there's more geopolitical volatility in the world, that can have an impact. Localized political volatility around data centers. We've got an election coming up. It will be interesting to see. Obviously, there's a lot of political discussion coming into an election, but then you also have to see how states and localities act coming out of elections. All these things can create volatility, and there's uncertainty around them.
So no one knows the exact line of travel. But at its base, this technology is real. It's going to accelerate in terms of its deployment. There's going to be infrastructure built around it that's going to be quite significant. Hopefully, also, and I think this is the case, there's going to be guardrails and government processes that help build trust around it. There's a lot of responsibility that goes to enterprises that are deploying it around making sure it's deployed correctly. But all of that is generally constructive for our business. 
Now I can tell you lots of things that can go wrong and slow it down. But there's uncertainty around that, but that's, kind of, part of our job and the market's job is to, kind of, intermediate that and decide, as time goes on, the trajectory of that line. But this is real and it's significant, and it's not going away, in my opinion.

**Denis Coleman** (Executives):
And then Mike, I think on the second part of your question, as the world continues to expand, as we expand our opportunity set in Asia, something we've been strategically getting after for a number of years, you're seeing some of the results of that investment and the expansion of clients and markets in places that we can actually trade and finance different assets. If you look in our earnings release, you can see the geographic mix of our revenues. 
You could look back a year, you could look at the second -- you could look at the year-over-year, you could look at the sequential for the firm, and there's a very meaningful change in Asia's representation of aggregate firm-wide revenues. And I think it's fair to say a lot of that change in the geographic mix of revenues in the firm is being driven by equities activity, equity financing activity. So those numbers give you a decent picture for the expansion of that opportunity set.

**Michael Mayo** (Analysts):
And then completely separately, just there are a lot of articles, headlines written about you, David, and succession. And clearly, there's nothing that came out from Goldman Sachs, but what are your plans for staying around at Goldman as CEO?

**David Solomon** (Executives):
I think you might not have been on when -- earlier when Glenn Schorr asked that question, Mike. And the way I answered it, I'll just repeat what I said. I mean I talked a little bit about the work we've done, the progress we've made, how much I'm enjoying it and also the excitement of the leadership team we have about the years ahead. And I said, to be clear, there's no succession transition or time line underway at Goldman Sachs. The Board and I are singularly focused on growing the firm, growing our earnings, serving our clients. So that's what I said earlier on the call.

**Operator** (Operator):
We will take our next question from Steven Chubak with Wolfe Research.

**Steven Chubak** (Analysts):
So David, I wanted to double-click a little bit further into the revenue opportunity tied to the financing of the digital infrastructure build-out. Your firm is actually uniquely positioned to underwrite financing activity both in the private IG market as well as the public debt market. As we get deeper into the AI CapEx cycle, wanted to get your perspective as to how you see activity migrating from the public to private markets, how you're positioned competitively to compete in that private IG space? And how does that impact some of the revenue considerations or economics if that activity does, in fact, migrate away from the public debt space and into the private sphere?

**David Solomon** (Executives):
Yes. I mean I'll make a couple of comments, and Denis might have a couple of comments here, too. But again, I know everyone wants an absolutely clear answer on the direction of travel of all of this. The capital demands are significant, and it's going to require significant capital deployment from the public markets, both equity and debt, and from the private markets, both equity and debt. And we're seeing that. 
I think one of the things that makes Goldman Sachs so unique is we're the only firm that sits, kind of, at the epicenter of having an ability to advise on these projects and the financings and how they should come together, an ability to be an originator and a structurer of these transactions and distribute them to other institutional sources of capital. And in addition, have a very broad Asset Management platform that includes both public and private pools of capital that can be coordinated into these transactions. And there's nobody else that has that positioning. 
So we feel as a firm that we're seeing a lot, and we sit in a very privileged place in the ecosystem. There's a significant amount of activity. It's different for different entities. It depends on who the customers and the offtakes are in a lot of the projects, which has a significant impact on the financing rates as to where you can go. There's a big difference from something that's really generated to serve a hyperscaler versus some of the neo clouds. And so all of this goes into the equation, but we feel very well positioned to bring the full range of services and participate actively. And we still see an enormous amount of activity. And Denis, do you want to add to that at all?

**Denis Coleman** (Executives):
No, I think it's well said. The only thing I would add is if you step back and you also think about our banking franchise, the coverage footprint that we have, this cycle is different from prior cycles in that the largest, biggest companies driving the cycle have significant capacity to use free cash flow to finance this. And so there's lots of discussions with how you advise those large companies themselves, how much debt they should issue, how much equity they should issue, what's their rating appetite, what are the structures of the financing facilities. 
So you have to start with those people that are actually driving the investment super cycle, then you move into the public and private debt and equity markets. We obviously, through Capital Solutions, have the capacity to underwrite and distribute. To also put certain types of financing structures on our own balance sheet. And then we've been growing our AWM business, our private IG business, as you referenced, quite substantially. That also can participate in the overall growth. 
And then if you think about the entire ecosystem, the supply chain is super complicated. There are tremendous number of different companies that operate, and you can finance the different companies at each point in the supply chain across different markets around the world. And given the scale of capabilities that we have, we just feel that we're well positioned to assist all across the supply chain in driving growth of the investment cycle.

**Steven Chubak** (Analysts):
I appreciate really all that detail and the perspective that you offered. Maybe just a quick follow-up on the SLR. Given financing activity is much more leverage intensive, you guys have obviously seen outsized gains on the financing side. Speak to where you're comfortable running under the SLR constraint while supporting continued balance sheet expansion and specifically your appetite to grow in more nascent financing areas such as tax aware strategies, just given your leading position in wealth in the RIA custody space would be a natural extension of your current financing capabilities.

**Denis Coleman** (Executives):
Sure. So you've obviously seen the change in how we've run our SLR ratio on a year-to-date basis. I think it's fair to say that the biggest delta, the largest sort of balance sheet extension, is behind us. We're now migrating to a zone where we run a buffer in SLR much like we run in CET1 ratio. So we feel like we have the requisite capital we need to support the growth in client activity as we head into the fourth quarter, but I wouldn't expect a significant movement from here. And then in terms of other strategies that we have across the overall AWM franchise, we're exploring and working on a number of those different strategies that you referenced.

**Operator** (Operator):
We'll take our next question from Manan Gosalia with Morgan Stanley.

**Manan Gosalia** (Analysts):
Earlier in the call, you spoke about the year-to-date sponsor share for announced M&A being below the historical average. I guess what's your outlook for that business given the uptick in rates? Are you seeing any pullback, any reluctance for some of those deals to come through into the market?

**David Solomon** (Executives):
Yes. I appreciate the question, Manan. The sponsors have been slow to monetize and turn over the capital portfolios from the 2020 and 2021 vintages. I think we all feel we would have seen more activity by now. I know there's a lot of questions around the fact in a higher rate environment, is that more constraining? I think the bigger constraint is that a lot of this stuff is still marked higher than where it can be monetized in the market, and the sponsors are taking the optionality to wait longer because that's the way the incentive system works.
They obviously have tools such as continuation funds and other vehicles to extend life of funds, and so they're taking advantage of those. This will come out, though. This activity will come. And I think the thing I'd look at, I look at the M&A levels and just recognizing the capital markets levels and just recognize it's been very light on sponsor activity. That sponsor activity's going to come. And when it comes, that'll be a tailwind, but it has been slower than we would have expected at this point. But I'm not overly concerned with how the interest rate environment affects it in the short term.

**Manan Gosalia** (Analysts):
Got it. And are the midterms factoring into your conversations with clients at all? Like are clients waiting on the sidelines to get more clarity on that? Or maybe on the flip side, if there's a greater sense of urgency to get deals done?

**David Solomon** (Executives):
I don't sense that people are sitting on the sidelines because of the midterms. I think from a strategic M&A perspective, the window is we have an administration for 2.25 more years. And this is an administration where strategically to achieve scale, there's a general point of view that unlike in the prior administration where whatever the question was the answer was no. In this administration, whatever the question is the answer is very significant maybe. And so strategically, companies are very front-footed, and I think they feel comfortable that they've got a window regardless of the midterms. They've, kind of, got a window that presses through the administration. I think people are watching the midterms carefully to see what happens and what that means, kind of, for activity in government over the course of the next couple of years. But I don't see it at the moment affecting activity significantly.

**Operator** (Operator):
We will take our next question from Brennan Hawken with BMO.

**Brennan Hawken** (Analysts):
I had one on financing. You've spoken to both pricing and strength in Asia. You said that there's no one-timers there. But the third quarter was perceived as a bit of a degrossing period. So curious whether or not you saw that? And is it possible to break down some of the growth that you've seen in those trading revenues between how much is tied to average balances growing versus the pricing benefits that you've highlighted?

**Denis Coleman** (Executives):
So Brennan, I appreciate the question. I mean the growth rate for financing, in particular, on a sequential basis was about 3%. So I think there was deleveraging in the quarter. I think there was some disruption over the course of the quarter, and so the trajectory did not sustain substantial growth. It's still very healthy. And as we pointed out in the prepared remarks, it does remain an environment that sort of supply of financing constrained. And so one of the levers that we have in terms of driving sustainable growth in that activity is as there can be pullbacks, we can assess expanding the funnel of activity that we take on board with existing clients and/or new clients as a bit of a valve as aggregate market levels adjust. But I think most of what would explain the sequential performance does relate to the overall backdrop of the market. There was not significant change in the composition of the book away from that.

**Brennan Hawken** (Analysts):
Great. Okay. And then you spoke to the year-to-date comp ratio, 30%. Is that the best way we should be thinking about your expectation for the full year? And have we seen -- a few investors noted this morning about the strong performance on the comp ratio. Is there something to do with like revenue mix? Equities revenue has been really, really strong. That's generally considered a lower comp ratio business. Has that -- has it been like business mix that has helped the comp ratio? Or are you just seeing lower competition for talent?

**Denis Coleman** (Executives):
Sure. So I'd say there's a couple of things in terms of how we think about the comp ratio. First, it is our best estimate at the moment for what we expect for the year, but I'd say that we are applying a strategic lens to it. And your question does get after this. As we look at ways that we can invest to grow the firm, grow the earnings of the firm, scale the firm, we are building durable platform-connected types of businesses. And over time, we should not have the same degree of head count-related expenses that we might have historically to grow and scale the firm. And certain of the more durable activities, including the financing activities, we're using a lot of the firm's financial resources and risk appetite to drive that activity. And so there can be favorable compensation ratio benefits with respect to the growth of those activities.
I would not say that we're seeing any diminution in terms of the market for talent, frankly, quite the opposite. I think for the very, very best people in this environment, business professionals, engineering professionals across the firm, there's a very, very strong bid for the very, very best people, and we make sure that we're in a position to compensate them appropriately. But we are focused over the longer term on sustainably delivering operating leverage to our shareholders as we grow the firm, and this is one step in that direction.

**Operator** (Operator):
We will take our next question from Dan Fannon with Jefferies.

**Daniel Fannon** (Analysts):
So one more on expenses, Denis, and shifting to noncomp. Obviously, excluding the charitable numbers in this quarter and I think next quarter, as you highlighted, could you just talk about the growth rate or outlook for noncomp expense as you think about the AI benefits you might be seeing in other areas of investment that could be growing or shrinking as we look ahead?

**Denis Coleman** (Executives):
Sure. So first and foremost, you can see it in the numbers, both aggregate and the deltas. By far, the biggest component is transaction-based expenses. That story remains the same for so long as we continue to see strong levels of client activity, particularly in equities and particularly in Asia, we'd expect that we'll continue to see growth in the transaction-based expenses. You're right, by the end of this year, based on our current expectations, we'll have made contributions to support go-forward charitable giving that hopefully should carry us through about 5 years or so on our best estimate. So you won't see that -- you're unlikely to see that in the future periods as a result. 
The other area of strategic growth is across technology, generally speaking, in comms and tech. We're going to continue to make sure that we have -- our people have access to the cutting-edge technology. We're making investments in our data infrastructure, our migrations to cloud. We're obviously making investments with respect to the models. And we're also making talent investments, all to make sure that we can support the firm's scaled growth over time. So I would call those out as the areas of focus.

**Daniel Fannon** (Analysts):
Understood. And then just as a follow-up, Wealth Management organic growth more than accelerated $47 billion in the quarter in terms of net inflows. Anything onetime in there or chunky that you would call out? Or maybe just talk to the, kind of, components, whether it was new adviser adds, recruiting, same-store sales with existing clients? What was the driver there?

**Denis Coleman** (Executives):
So I would not call out a particular onetime. I would say that we have now a multiyear sustained investment in expanding our adviser footprint. That's a decision that was made a number of years ago. We continue to ramp up. Advisers continue to expand our geographic footprint and our reach around the world. And we continue to have very, very strong investment performance, which is really important, and we continue to invest in the overall quality of our people and in terms of the client experience that our clients have with our people. It's a big area of strategic focus for the firm. It is performing substantially ahead of the targets that we put out earlier this year of 5%, but we're very pleased, and it's a huge opportunity for the firm.

**Operator** (Operator):
We will take our next question from Devin Ryan with Citizens Bank.

**Devin Ryan** (Analysts):
A couple here on Asset Management and really on the alts business, just been incredibly impressive fundraising. You started the year at a $75 billion to $100 billion target. Now you're kind of targeting $150 billion. So clearly, a lot of incremental capital coming in here. Just curious if you could give us a little more color around how much of that is just being, kind of, opportunistic in the market with some of these themes, like the volatility in private credit, or whether there's something maybe bigger structurally that's been changing around your ability to distribute or even add capacity to that business.

**David Solomon** (Executives):
Yes. I mean, just I appreciate the question, Devin, but there's nothing opportunistic about it. This is a concerted strategy that started 6-plus years ago to really scale the platform. And when you look across the platform, it's a scaled platform. We've got managers across a variety of the different categories of private capital raising that have a lot of experience, good performance. And we've been very, very good to institutional allocators at customizing solutions that work for them with a long-term view. And in addition, we have very, very good demand for these products and services from our ultra-high net worth channel, which is a very, very important component. 
And so this has been a strategic decision that we've made real scaled progress on over a period of time that has meaningfully increased our capacity to compete at the highest level in the space. And I think we've got good runway. When you look at private credit, for example, one of the things we've benefited from is we've been in this business for 40 years and institutional allocators, despite the noise in the media around private credit, as spreads have normalized to more attractive levels, institutional allocators have thought this is a more attractive time in the last 3 to 6 months to bring capital into experienced private credit managers, and we've benefited from that. So there's nothing opportunistic. This is a long-term strategy to have one of the largest and broadest private alts platforms, and you're seeing the benefit of our scaled position start to come through.

**Devin Ryan** (Analysts):
Appreciate that, David. And then just a follow-up just on the acquisition front in Asset Management. So clearly, it's been an area of you doing ETFs. Are there any other areas you feel like you're subscale in Asset Management, or where a few additional capabilities or investments could, kind of, like you just said on the alt side, similarly really, kind of, improve the capacity or make you more relevant with institutional or retail clients?

**David Solomon** (Executives):
Yes, there's no question. We still have gaps across the platform. We have a presence across all the variety of private assets broadly, but there are some places where we're not as scaled as we'd like to be. That doesn't mean that we'll take a -- we'll make an acquisition in that space because there's got to be fit, there's got to be the right team. But we continue to look for places where we're not scaled, where there are opportunities, both across private and the public side of our Asset Management business to increase our scale. And I think there'll be other opportunities. I'm not going to call out something specifically, but we're not at scale everywhere. And if we see an opportunity that fits and accelerates our scale position, we're certainly going to consider it, but always with a very high bar around culture fit and the specific people we're bringing into the firm.

**Operator** (Operator):
We'll take our next question from Gerard Cassidy with RBC.

**Gerard Cassidy** (Analysts):
Denis, you touched on in your comments about the provision being higher, that you gave us guidance earlier in the quarter about it being higher. So there's no real surprise. And the outlook for credit from your comments still is strong. But can you elaborate a little bit on the marks that you took to -- that drove that provision?

**Denis Coleman** (Executives):
Sure. So there's 2 drivers this quarter that are worth taking note of. One, which is the secondary driver, but yet it's important, which is overall growth in the portfolio. So we continue to deploy capital to expand the opportunities to lend to more clients. And frankly, that's an outgrowth of a strategic decision earlier in the year when we found ourselves with more excess capital that we wanted to fuel growth in our overall Investment banking coverage suite of relationships. 
So a component of the provision number is aggregate growth in the portfolio. But it is the case as well that the impairment numbers were elevated. We looked very carefully, as we always do, at the entire complexion of the portfolio. Our conclusion is they're highly idiosyncratic and noncorrelated set of names, but we had a couple of different names that we ended up taking incremental impairments against in the quarter. We don't think it's necessarily the signal of something else to come. But it was appropriate for those individual names, and so we took the impairments and put it through in the third quarter.

**Gerard Cassidy** (Analysts):
Very good. And then as a follow-up, you talked about it earlier in the year about the leaning into Asia and the success that you've had, and you touched on it again today, the Asian markets and the equity financing when the execution, you guys obviously benefit from. Are there any other opportunities globally where you can lean into new markets and get the benefits that you're seeing similar to what you did with Asia?

**Denis Coleman** (Executives):
So I think there are opportunities all over the world where we can continue to lean in. What we found particularly attractive about Asia is that we felt that we were quite under scale, and the opportunity was available with clients on attractive economic and risk terms. And so it was the most place -- the most attractive place geographically to drive incremental penetration and scale, and that's why we made it a priority. But there are plenty of other places around the world that we could continue to choose to drive incremental growth as well.

**Operator** (Operator):
We'll take our next question from Chris McGratty with KBW.

**Christopher McGratty** (Analysts):
Great. David, more of a high-level question. Your outperformance on your ROE to targets, maybe a comment or 2 on your views on how much is cyclical versus structural.

**David Solomon** (Executives):
I appreciate the question, Chris. I think a lot of it is we're structurally running the firm as a broader, more durable franchise with higher fundamental returns. I'm not going to speculate on -- through the cycle as to how the returns balanced out. But what I will say when I go back over the last 5 years, I remember sitting on this call for multiple years, including as recently as a couple of years ago, when we were very confident that we could get the firm running through our targets through the cycle, and there was a lot of skepticism about that.
The reason the returns are significantly elevated is because we've significantly grown the breadth and the base of the firm. We've significantly changed the operational structure and the durability of the firm, and that's led to higher structural returns. And so there's a big strategic result of an investment over a long period of time. I will say, at the moment, and I've said it on the call 3 times, we're in a very good environment. We're in a top quartile environment. And so does that flatter the -- what will be the average returns through the cycle? Absolutely. But structurally, the base returns of the firm have been meaningfully uplifted over the last 5 years.

**Christopher McGratty** (Analysts):
Perfect. And then second follow-up would be the midterms. I think there's a divided view of whether it's -- a divided government is good for activity or perhaps a headwind. Where do you stand on -- if the futures markets are right about a divided government, how that could play into your capital markets business?

**David Solomon** (Executives):
I don't really -- first of all, the election doesn't occur for another month. And in politics, a month is an eternity. So we'll see how the election plays out. And I'm not a good pundit, nor are the prediction markets or the futures markets a good pundit of exactly what the environment will bring after the election as we head into '27. So we'll watch that and be prepared for whatever comes our way.

**Operator** (Operator):
Thank you. At this time, there are no additional questions. Ladies and gentlemen, this concludes The Goldman Sachs Third Quarter 2026 Earnings Conference Call. Thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GS_Q2_2026_Earnings_Call_20260714.md
- 2026-07-14｜Denis Coleman｜guidance：全年另類募資預期上修至超過1,250億美元（原話："we now expect full-year fundraising to exceed $125 billion"）
- 2026-07-14｜Denis Coleman｜guidance：Platform Solutions 下半年各季營收預期與第二季大致持平（原話："for the remainder of the year to be broadly consistent with"）
- 2026-07-14｜Denis Coleman｜guidance：績效費預期下半年大幅增加（原話："We expect these fees to increase materially for the"）
- 2026-07-14｜Denis Coleman｜guidance：全年有效稅率仍預期約20%（原話："we continue to expect an effective tax rate of"）
- 2026-07-14｜Denis Coleman｜guidance：投行前景樂觀，贊助商業務仍低於歷史均值（原話："We remain optimistic on the investment banking outlook"）
- 2026-07-14｜Denis Coleman｜margin：上半年效率比58.8%，較去年同期改善320bp（原話："with an efficiency ratio of 58.8%, improving 320 basis"）
- 2026-07-14｜Denis Coleman｜margin：薪酬比（扣除撥備）降至31%（原話："decline in our compensation ratio net of provisions to 31%."）
- 2026-07-14｜Denis Coleman｜margin：營收成長約40%，薪酬費用成長30%、非薪酬22%（原話："We've been able to grow our revs at about 40%"）
- 2026-07-14｜Denis Coleman｜margin：管理層稱費用基礎無結構性變化（原話："any structural change in our expense base at this point"）
- 2026-07-14｜Denis Coleman｜margin：FICC與股票融資營收45億美元，占兩者合計37%（原話："revenues of $4.5 billion rose 62% versus the prior year and"）
- 2026-07-14｜Denis Coleman｜capital_allocation：CET1 12.9%，高於現行要求150bp（原話："Common equity Tier 1 ratio was 12.9% at the end of the"）
- 2026-07-14｜David Solomon｜capital_allocation：季股息提高至每股5美元，年增25%（原話："quarterly dividend to $5 a share, representing a 25%"）
- 2026-07-14｜David Solomon｜capital_allocation：本季回購40億美元普通股（原話："We also repurchased $4 billion of common stock in the"）
- 2026-07-14｜David Solomon｜capital_allocation：無法部署資本時會快速還給股東（原話："going to nimbly get it back to shareholders as quickly as"）
- 2026-07-14｜Denis Coleman｜capital_allocation：資產負債表擴張的意願有上限（原話："Ultimately, there will be a limit to our appetite to expand"）
- 2026-07-14｜Denis Coleman｜capital_allocation：管理層稱對監管改革方向表示期待 Basel III 定案（原話："we look forward to swift progress towards Basel III"）
- 2026-07-14｜Denis Coleman｜commitment：CET1營運模式維持高於要求50至100bp（原話："sort of, call it, plus 50 to 100 basis points. We're"）
- 2026-07-14｜Denis Coleman｜commitment：另類募資年度目標750億至1,000億美元（原話："have a target of $75 billion to $100 billion of annual"）
- 2026-07-14｜David Solomon｜commitment：承諾持續達成AWM成長目標（原話："you can expect us to continue to deliver on those growth"）
- 2026-07-14｜David Solomon｜commitment：AWM併購：門檻高但會持續尋找（原話："The bar is always high to do anything inorganic."）
- 2026-07-14｜David Solomon｜risk：AI投資週期不會直線前進，短期可能有重新調整（原話："not there can be recalibrations, in the short term"）
- 2026-07-14｜David Solomon｜risk：管理層承認週期必有重置與回落（原話："you will have a recalibration, a reset, a drawdown, and"）
- 2026-07-14｜Denis Coleman｜risk：金融需求超過公司願意提供的量（原話："are outstripping what we think is the appropriate quantum."）
- 2026-07-14｜David Solomon｜risk：IPO量僅在十年均值或以下（原話："IPO volumes in this quarter were kind of at or below"）
- 2026-07-14｜David Solomon｜risk：另類產業部分區塊承壓（原話："despite some pressure in segments of the industry, investor"）
- 2026-07-14｜Denis Coleman｜competition：亞洲股票業務過去被視為競爭短板，已投資補強（原話："capture what we viewed as a competitive shortcoming in Asia"）
- 2026-07-14｜Denis Coleman｜competition：主經紀業務存在定價槓桿，部分同業更節制（原話："opportunities for pricing leverage."）
- 2026-07-14｜David Solomon｜customer：贊助商交易尚未加速，是潛在上行（原話："has not accelerated, and candidly, it's going to come at"）
- 2026-07-14｜David Solomon｜customer：大型併購量上半年成長90%（原話："corporate M&A volumes up 90% through the first half of 2026."）
- 2026-07-14｜David Solomon｜customer：獲任管理Lockheed Martin等退休金計畫（合計700億美元）（原話："and Lockheed Martin's retirement plans, which collectively"）
- 2026-07-14｜David Solomon｜product：投行積壓訂單創五年新高（原話："our backlog increased to its highest level in 5 years"）
- 2026-07-14｜David Solomon｜product：加速投資超高淨值財富業務（原話："We've accelerated our investment."）
- 2026-07-14｜Denis Coleman｜product：人力策略：目前不是結構性重整人力的時刻（原話："structural rework of our human capital footprint."）
- 2026-07-14｜David Solomon｜product：AI不會取代公司的核心人才（原話："change how work gets done, it will not replace what matters"）

### GS_Shareholder_Analyst_Call_The_Goldman_Sachs_Group_Inc_20260429.md
- 2026-04-29｜David Solomon｜margin：管理層列示2025年全年財務結果（原話："grew our earnings per share by 27% to $51.32 and"）
- 2026-04-29｜David Solomon｜margin：管理層列示2025年營收與ROE變化（原話："improved our return on equity by 230 basis points to 15%."）
- 2026-04-29｜David Solomon｜margin：管理層對2019–2025累計成果的口徑（原話："grown earnings per share by 144%"）
- 2026-04-29｜David Solomon｜capital_allocation：管理層稱2019–2025總股東報酬率居同業之首（原話："total shareholder return of over 340%"）
- 2026-04-29｜David Solomon｜product：宣布One GS 3.0以AI驅動的營運模式（原話："launch of One Goldman Sachs 3.0, our operating model"）
- 2026-04-29｜David Solomon｜guidance：管理層對One GS 3.0長期效益的表述，無量化目標（原話："One GS 3.0 will drive stronger operating leverage,"）
- 2026-04-29｜David Solomon｜risk：管理層點名的外部環境風險（原話："uncertainty in parts of private credit"）
- 2026-04-29｜David Solomon｜competition：管理層稱不確定時期客戶轉向高盛（原話："clients turn to Goldman Sachs as a trusted adviser"）
- 2026-04-29｜David Solomon｜commitment：管理層稱持續投資於人才（原話："we remain focused on continuing to invest in them."）
- 2026-04-29｜David Solomon｜customer：管理層稱2026年第一季為史上第二高的營收、盈餘與EPS（原話："second highest net revenues, net earnings and earnings"）
- 2026-04-29｜Drew Jorgensen｜risk：股東提案方稱25%召開特別股東會門檻不可達成（原話："the current 25% figure is unattainable."）
- 2026-04-29｜Yumi Narita｜capital_allocation：NYC審計長提案要求揭露能源供給比率；稱JPMorgan與Citi已揭露（原話："Goldman peers JPMorgan and Citi disclosed their ESR,"）
- 2026-04-29｜Yumi Narita｜commitment：第7項提案稱高盛游說揭露落後同業（原話："existing disclosures lag peers and can be enhanced."）
- 2026-04-29｜Jamie Greenberg｜risk：say-on-pay支持率約70%（原話："received the support of votes representing approximately 70%"）
- 2026-04-29｜Jamie Greenberg｜risk：特別股東會門檻提案獲約37%支持而未通過（原話："received the support of approximately 37% of the"）

### 問答異常語氣（迴避／改口／保留）
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Mayo：併購領先帶來的跨業務乘數效應是多少？｜答法：Solomon 明說不給百分比，改談框架
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Fannon：績效費大幅增加的量化與依據｜答法：Coleman 只說與已知特定交易有關，未給金額
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Cassidy：交易業績中 OneGS 與市場波動各占多少｜答法：Solomon 稱無法以單季量化，改引2020年起前百大客戶排名
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Cassidy：與網路泡沫／2021年比較AI貢獻｜答法：Solomon 稱不確定能給好答案，改談公司更多元
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Bolu：SLR已為同業最低，能壓多低｜答法：Coleman 未給數字，稱多重限制動態管理
- GS_Q2_2026_Earnings_Call_20260714.md｜問：Erika Penala：亞洲超大型股交易貢獻占比與回檔是否擔憂｜答法：Coleman 未回答占比，改談廣泛基礎的活動

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
{"date":"20260615","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"GBM（投行+交易）維持 league-table 前二、through-the-cycle 市占不流失","columns":{"2Y 驗證點":"FICC+Equities 合計市占持平/微升","5Y 驗證點":"顧問費市占穩居前二","10Y 驗證點":"做市規模優勢維持","具體數字門檻":"Equities 連續創 record；Advisory 市占前二","信息來源":"Coalition Greenwich 市占榜 + 公司法說","漂移觸發":"市占連 2 季流失 → 削弱（2Y 假設連 2 季）"}},{"id":"H2","text":"AWM 把波動投行收入逐步換成可預期管理費，ROTCE 結構性墊高至 mid-teens","columns":{"2Y 驗證點":"管理費 YoY &gt; +8%；AWM pre-tax margin 維持 mid-20s","5Y 驗證點":"替代資產 AUS &gt; $800B；through-cycle ROTCE ≥ 15%","10Y 驗證點":"費用收入占比 &gt; 30%","具體數字門檻":"AUS $3.7T（Q1'26 record）；alt $625B；募資 $75-100B/年","信息來源":"公司 Q1'26 法說 + Investor Day target","漂移觸發":"管理費 YoY &lt; +5% 連 2 季 → 削弱（5Y 假設連 4 季才反轉）"}},{"id":"H3","text":"市場願意維持「轉型後」估值溢價（P/TBV 不回到 1x 時代）","columns":{"2Y 驗證點":"P/TBV 維持 &gt; 2x","5Y 驗證點":"5Y 均 P/TBV &gt; 1.8x","10Y 驗證點":"估值中樞高於 2015-2020 的 1.0-1.3x","具體數字門檻":"當前 P/TBV 3.10x（史上最高）","信息來源":"GuruFocus/YCharts 5Y P/TBV band","漂移觸發":"P/TBV 跌破 1.5x 連 2 季 → 反轉（估值 thesis 破裂）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"資本市場週期反轉，交易/IB 從 record 回落（Q1'26 record trading 是「市場混亂」的週期峰值）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"GBM 季度淨收入 YoY","警戒閾值":"連 2 季 YoY &lt; −15% → 減倉"}},{"id":"R2","text":"管理層再次「為成長」進入低 ROIC 領域（消費金融前科），或 AWM 募資不及 $75B 目標","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"替代資產年度募資；新業務 capital 投入","警戒閾值":"年度募資 &lt; $60B 連 2 年，或啟動新非核心擴張"}},{"id":"R3","text":"估值倍數結構性重估（P/TBV 從 3.1x 回歸歷史中段），即使 EPS 不跌股價也跌","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"P/TBV 5Y 中樞","警戒閾值":"P/TBV 跌破 1.5x（需 ≥ 50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":1082.57,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GS_20261017/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
