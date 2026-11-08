你是 stock-analyst **v20 判斷 agent**，標的 PH（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"PH","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":5992,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm"}},{"id":"f_kpi1_adjusted_segment_operati","label":"Adjusted segment operating margin (non-GAAP)","value":28.6,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm"}},{"id":"f_kpi2_total_segment_operating_","label":"Total segment operating margin (GAAP)","value":24.4,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm"}},{"id":"f_kpi3_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":8.9,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm"},"note":"consensus 約 8.17–8.23（二手來源 web_search，新聞稿未載，非 IR 來源）"},{"id":"f_kpi4_free_cash_flow_derived","label":"Free cash flow (derived)","value":643,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm"}},{"id":"f_kpi6_backlog","label":"Backlog","value":13.7,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm"}},{"id":"f_kpi7_fy2027_guidance_filtrati","label":"FY2027 guidance（上調，已含 Filtration Group）","value":"調整後 EPS 36.45–37.25；GAAP EPS 29.65–30.45","period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm"},"note":"FY1 共識 EPS 35.59（財報前快照，dd_numbers_extra.py consensus_revision）；指引中點 36.85"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ph_gross_margin_pct","label":"PH 毛利率","value":37.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ph_operating_margin_pct","label":"PH 營業利益率","value":21.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ph_fcf_margin_pct","label":"PH FCF 利潤率","value":17.2,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hon_gross_margin_pct","label":"HON 毛利率","value":38.04,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hon_operating_margin_pct","label":"HON 營業利益率","value":16.2,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hon_fcf_margin_pct","label":"HON FCF 利潤率","value":4.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rok_gross_margin_pct","label":"ROK 毛利率","value":49.35,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rok_operating_margin_pct","label":"ROK 營業利益率","value":19.74,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_rok_fcf_margin_pct","label":"ROK FCF 利潤率","value":16.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_emr_gross_margin_pct","label":"EMR 毛利率","value":53.61,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EMR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_emr_operating_margin_pct","label":"EMR 營業利益率","value":20.85,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EMR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_emr_fcf_margin_pct","label":"EMR FCF 利潤率","value":19.0,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EMR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":11.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_share_based_compensa","label":"SBC (share-based compensation)","value":82,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 Q1 FY27 新聞稿（8-K Exhibit 99.1）https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":917.79,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":4.64,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":46.88,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（35.59 → 35.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（39.77 → 39.77）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（44.14 → 44.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":35.59,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":39.77,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":44.14,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.66,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 35.01 → 35.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":31.53,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝80.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":80.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.16,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝82.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":82.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":5.91,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝93.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":93.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":25.79,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 35.59，分子＝快照價 917.79","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.632,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":16767.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 17478.0、現金 711.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":126.1,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":132497.37,"period":"2026-11-08","unit":"USD m","basis":"市值 115730.37 ＋ 淨負債 16767.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":25304.16,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":27065.02,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.24,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 917.79 / W52 931.5 / W104 804.64 / W250 559.07 / W250 13週斜率 1.79%"},{"id":"f_ma_w52","label":"52 週均線","value":931.5,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":804.64,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":559.07,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.79,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"FY2026 10-K：Parker 稱在多數主要市場為市場領導者之一，對手數以百計，Diversified Industrial 主要對手含 Bosch Rexroth、Danfoss、Festo、SMC、Gates 等；沒有任何單一對手涵蓋全部產品線。10-K 未點名特定新進入者。","source":"SEC EDGAR 10-K FY2026 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"Although each of our segments has numerous competitors, given our market and product breadth, no single competitor competes with the Company with respect to all the products we manufacture and sell.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：全球、區域及在地競爭者可能造成降價壓力與毛利率或市占下滑；公司也提到因應措施（如漲價）可能衝擊市占。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"Our operations are subject to competition from a wide variety of global, regional and local competitors, which could adversely affect our results of operations by creating downward pricing pressure and/or a decline in our margins or market shares.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"經查：搜尋未找到第三方對 PH 份額增減的量化資料，也無對手設計勝出（design win）公告或明確新進入者報導；僅有投資社群敘事主張電氣化可能削弱液壓／氣動長期需求（低權威來源，未讀原文）。","source":"WebSearch 4 次結果彙總（Simply Wall St 社群敘事）","url":null,"excerpt":null,"as_of":"2026-11-08","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Simply Wall St 社群敘事：電氣化與數位化可能降低 PH 液壓／氣動核心零件長期需求（社群意見，低權威）","source":"Simply Wall St community narrative","url":"https://simplywall.st/community/narratives/us/capital-goods/nyse-ph/parker-hannifin/mdp0t5kz-global-electrification-will-challenge-legacy-markets-despite-robust-backlogs","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"PH FY2026 10-K 揭露無單一客戶占淨銷售比重過高（客戶集中度）","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000105/ph-20260630.htm","excerpt":null,"as_of":"2026-08-21","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 10-K 載明因客戶遍布全球，公司不認為暴露於任何信用集中風險。","source":"SEC EDGAR 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"Due to our diverse group of customers throughout the world, we do not consider ourselves exposed to any concentration of credit risks.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2024 10-K 稱無單一客戶占總淨銷售超過 4%","source":"Parker-Hannifin FY2024 10-K","url":"https://investors.parker.com/sec-filings/annual-reports/content/0000076334-24-000044/0000076334-24-000044.pdf","excerpt":"No single customer accounted for more than four percent of our total net sales for the year ended June 30, 2024. Reportable Segments We have two reportable segments: Diversified Industrial and Aerospace Systems.","as_of":"2024-08-16","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"美國機械業產能利用率自 2024 年底起持續上升；AMT 經濟學家解讀機械製造商資本投入升高代表新產能將進場（引文被截斷，無具體時程）","source":"Third Wave / AMT, Machinery Orders Run 32% Ahead of 2025, but Shipments Cannot Keep Up","url":"https://twbs.com/resources/blog/machinery-orders-run-32-ahead-of-2025-but-shipments-cannot-keep-up-the-week-in-industrial-equipment/","excerpt":"Since the end of 2024, capacity utilization for machinery manufacturers has steadily trended upward.","as_of":"2026-07-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"VDMA 預期德國機械 2026 年產出 -2%（第四年下滑），2027 年實質產出 +3%，屬週期性復甦預期","source":"Devdiscourse, Germany's Machinery Industry: A Turning Point Ahead?","url":"https://www.devdiscourse.com/article/business/3978270-germanys-machinery-industry-a-turning-point-ahead","excerpt":"Positive forecasts for 2027 show real production growth of 3%, driven by improved orders, but weak domestic demand continues to challenge the sector.","as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"PH Aerospace Systems 積壓訂單 FY2026 年底 $8,498M，高於前一年 $7,389M，因訂單超過出貨（商用 OEM 與售後）","source":"Parker-Hannifin FY2026 Annual Report (Form ARS)","url":"https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000142/phfy26ararscompliant.pdf","excerpt":"Backlog June 30, 2026 Backlog $ 8,498 2025 $ 7,389 Aerospace Systems Segment backlog increased in 2026 primarily due to orders exceeding shipments in all market","as_of":"2026-08-15","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素揭露公司營運受美國與歐洲反壟斷／競爭法規範，違反可能對盈餘、現金流與財務狀況造成重大不利影響（一般性風險揭露，非具體調查）。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"Further, our operations are subject to certain antitrust and competition laws in the jurisdictions in which we conduct our business, in particular the United States and Europe.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Davidson Instruments 對 Parker 提起私人壟斷訴訟；Parker 於 2026-01 向聯邦法官主張修正後起訴狀未構成可信的壟斷或企圖壟斷主張，並聲請駁回；搜尋未見裁決結果。非政府調查。","source":"MLex 報導（經搜尋摘要）","url":"https://www.mlex.com/mlex/articles/2437065","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未見 2026 年 DOJ、FTC 或歐盟對 Parker-Hannifin 的反壟斷調查；結果僅有 2017 年 Clarcor 併購之 DOJ 舊案。","source":"WebSearch 結果彙整","url":null,"excerpt":null,"as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：非美國銷售地點占淨銷售約 36%；列出關稅、進出口管制、制裁及可能的對中國貿易限制為風險；美中關係與 USMCA 重新談判不確定可能衝擊業務。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"government import and export controls, embargoes, sanctions or trade restrictions, including possible restrictions on trade and/or obstacles to conducting business in China","as_of":"2026-08-21","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026 年 2 月美國最高法院裁定 IEEPA 關稅無授權；PH 於 FY2026 第四季認列 8,400 萬美元 IEEPA 關稅退款，沖減銷貨成本，另已申請較小額退款但未入帳。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"During the fourth quarter of fiscal 2026, the Company recognized a reduction to cost of sales of $84 million related to IEEPA tariff refunds received from the U.S. government. We have applied for additional refunds under the same program, though for lesser amounts.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：ITAR／EAR 管制清單範圍變動可能迫使 PH 調整營運、取得額外許可或限制業務；違規可能失去出口特權。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"Changes in export control lists or the scope of ITAR-controlled items may require us to modify our operations, obtain additional licenses or restrict certain business activities.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2026 10-K：非美國銷售地點的淨銷售約占 36%（FY2024-26 各年）；風險因素提到中國貿易限制、貿易壁壘、USMCA 重談；以『local for local』製造策略對沖","source":"Parker-Hannifin FY2026 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000105/ph-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 Q3 10-Q：最高法院裁定 IEEPA 關稅未獲授權，公司因退款不確定未認列應收；中東衝突（含伊朗）可能影響全球供應鏈並推升大宗、能源、物流成本","source":"Parker-Hannifin 10-Q (period ended 2026-03-31)","url":"https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000073/ph-20260331.htm","excerpt":"Economic Powers Act (\"IEEPA\") on goods imported into the U.S. were unauthorized. We will continue to monitor developments; however, given the uncertainty surrounding potential refunds, we have not recorded a receivable for IEEPA tariffs paid as of March 31, 2026. Additionally, geopolitical tensions in the Middle East, including the ongoing conflict involving Iran, could adversely affect","as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27 Q1（截至2026-09-30）銷售年增18%至創紀錄60億美元，內生成長11.5%、併購貢獻約7點；北美工業部門銷售24.45億美元、內生成長9.4%；國際工業部門17.07億美元、內生成長11.6%（亞太+23%、EMEA +4%、拉美-1%）。","source":"Parker-Hannifin 8-K Exhibit 99.1 Q1 FY27","url":"https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000170/exhibit991q1fy27.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"航太部門：各業務訂單率雙位數、記錄在手訂單137億美元；有報導稱航太訂單率由前季+18%放緩至+14%（第三方，未核原文）。","source":"Parker-Hannifin Q1 FY27 results / panabee.com","url":"https://www.panabee.com/news/parker-hannifin-earnings-q1-2027","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27全年指引上調，納入Filtration Group後有機成長7.5%至10.5%、調整後EPS 36.45至37.25美元；公司稱所有市場垂直領域需求增加。8月原指引有機成長5.5%至8.5%。","source":"Parker FY27 Q1 release (finviz)","url":"https://finviz.com/news/416828/parker-delivers-record-fiscal-2027-first-quarter-results-raises-full-year-outlook","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子承認所服務市場技術快速變動、新產品頻繁推出，並點名 AI 技術與資料中心基礎設施需求是需successfully整合/定位的領域；未點名特定替代技術取代核心產品。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"The markets we serve are characterized by rapidly changing technologies and frequent introductions of new products and services. Our ability to develop new products based on technological innovation and to position our existing products in new markets can affect our competitive position and often requires the investment of significant resources.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"第三方分析稱行動設備電動化可能以機電系統取代液壓，時間尺度約 10–15 年；液壓約占 Industrial 部門 25–30%（第三方估計）。","source":"PitchGrade research: parker hannifin ai margin pressure","url":"https://pitchgrade.com/research/parker-hannifin-ai-margin-pressure","excerpt":"The company is the world's leading diversified manufacturer of motion and control technologies — hydraulics, pneumatics, electromechanical systems, filtration, and fluid management products — with over 100,000 SKUs serving industrial, mobile, and aerospace markets across virtually every geography and end market.","as_of":"2026-03-04","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Simply Wall St 社群敘事：看空者擔心電動化與軟體化自動化侵蝕傳統液壓。","source":"Simply Wall St narrative: global electrification will challenge legacy markets","url":"https://simplywall.st/community/narratives/us/capital-goods/nyse-ph/parker-hannifin/mdp0t5kz-global-electrification-will-challenge-legacy-markets-despite-robust-backlogs","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K 描述的通路仍是現場業務員＋獨立經銷商，OEM 與經銷商（售後替換市場）並行；未見訂閱化、D2C 或平台化的結構性轉變描述。搜尋也未找到公司對通路策略改變的說法。","source":"SEC EDGAR 10-K FY2026 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"We market our Diversified Industrial Segment products primarily through field sales employees and independent distributors located throughout the world.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 報導 PH 2026-08-06 給 FY2027 指引：調整後 EPS 34.25–35.25 美元、營收 22.68–23.33B，高於共識 34.09","source":"Benzinga earnings forecasts","url":"https://www.benzinga.com/quote/PH/earnings-forecasts","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Walnut：23 位分析師平均目標價 1039.70、中位數 1,057，區間 680–1269；Truist 2026-07-02 由 1147 調至 1269","source":"Walnut Invest PH forecast","url":"https://walnutinvest.com/stocks/ph/forecast","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"TickFlow：截至 2026-08-01 10 位分析師 Buy 共識，平均目標價 1047.25","source":"TickFlow PH forecast","url":"https://www.tickflow.io/stock/PH/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill：FY2027 EPS 共識最新紀錄 36.54（2026-10-18，31 位分析師），高於公司指引區間上緣 35.25","source":"Chartmill PH estimates","url":"https://www.chartmill.com/stock/quote/PH/estimates","excerpt":null,"as_of":"2026-10-18","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 FY26 8-K（2026-04-30）：公司上調 FY26 指引","source":"SEC 8-K exhibit 99.1 Q3 FY26","url":"https://www.sec.gov/Archives/edgar/data/0000076334/000007633426000070/exhibit991q3fy26.htm","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025-11-10 簽約、2026-08-13 完成以現金 92.5 億美元收購 Filtration Group（無現金無負債基礎，扣營運資金調整）","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/76334/000119312526349148/d105152d8k.htm","excerpt":"On August 13, 2026, Parker completed the Merger.","as_of":"2026-08-13","retrieved_at":"20261108","affects":["valuation","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"收購資金安排：2025-12-10 簽 52.5 億（364 天）與 25 億（三年）延遲提款定期貸款，供 Filtration Group 收購部分對價","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/76334/000119312525314164/d25389d8k.htm","excerpt":"which 364-Day Credit Agreement provides for a delayed draw term loan facility in the aggregate principal amount of $5.25 billion","as_of":"2025-12-10","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"10-K Note 17 稱訴訟屬一般營運範圍，管理層認為不會有重大不利影響","source":"SEC EDGAR 10-K FY2026 Note 17","url":"https://www.sec.gov/Archives/edgar/data/76334/000007633426000105/ph-20260630.htm","excerpt":"management believes that any liabilities that may result from these proceedings will not have a material adverse effect on our liquidity, financial condition or results of operations.","as_of":"2026-08-21","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-08-13 完成收購 Filtration Group，現金 92.5 億美元","source":"SEC EDGAR 8-K Item 2.01","url":"https://www.sec.gov/Archives/edgar/data/76334/000119312526349148/d105152d8k.htm","excerpt":"Pursuant to the Merger Agreement, Parker agreed to acquire Filtration Group via a merger transaction (the “Merger”) on a cash-free, debt-free basis for a cash purchase price of $9.25 billion, subject to a net working capital adjustment (the “Purchase Price”).","as_of":"2026-08-13","retrieved_at":"20261108","affects":["valuation","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"PH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.74,"operating_margin_pct":21.4,"fcf_margin_pct":17.2,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PH","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HON","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.04,"operating_margin_pct":16.2,"fcf_margin_pct":4.95,"rd_intensity_pct":5.37},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ROK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.35,"operating_margin_pct":19.74,"fcf_margin_pct":16.51,"rd_intensity_pct":7.89},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROK","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"EMR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.61,"operating_margin_pct":20.85,"fcf_margin_pct":19.0,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EMR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ETN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.05,"operating_margin_pct":17.32,"fcf_margin_pct":11.87,"rd_intensity_pct":2.75},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"PH"},"financial_history":{"ticker":"PH","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":19065000000.0,"revenue_yoy_pct":null,"gross_margin_pct":33.72,"operating_margin_pct":16.13,"net_income":2083000000.0,"diluted_eps":16.04,"free_cash_flow":2599000000.0,"fcf_margin_pct":13.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":19930000000.0,"revenue_yoy_pct":4.54,"gross_margin_pct":35.77,"operating_margin_pct":19.13,"net_income":2844000000.0,"diluted_eps":21.84,"free_cash_flow":2984000000.0,"fcf_margin_pct":14.97,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":19850000000.0,"revenue_yoy_pct":-0.4,"gross_margin_pct":36.85,"operating_margin_pct":20.41,"net_income":3531000000.0,"diluted_eps":27.12,"free_cash_flow":3341000000.0,"fcf_margin_pct":16.83,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":21499000000.0,"revenue_yoy_pct":8.31,"gross_margin_pct":37.69,"operating_margin_pct":21.55,"net_income":3648000000.0,"diluted_eps":28.48,"free_cash_flow":3905000000.0,"fcf_margin_pct":18.16,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/PH/PH_Q1_2027_Earnings_Call_20261105.md）

# Q1 2027 Earnings Call
**Parker-Hannifin Corporation** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good morning, everyone. Welcome to Parker-Hannifin Corporation's Fiscal 2027 First Quarter Earnings Conference Call and Webcast. [Operator Instructions] Please be advised that today's conference is being recorded. [Operator Instructions] I would now like to turn the call over to our host, Mr. Todd Leombruno, Chief Financial Officer. Please go ahead, sir.

**Todd Leombruno** (Executives):
Thank you so much, Bo. Good morning, everyone, and welcome to Parker's Fiscal Year 2027 First Quarter Earnings Release Webcast. This is Todd Leombruno, Chief Financial Officer, speaking. And, as usual, with me today is Jenny Parmentier, our Chairman and Chief Executive Officer. As always, we appreciate your interest in Parker, and we thank you all for joining us today.
On Slide 2, we're going to address our disclosures on forward-looking projections and non-GAAP financial measures. The items we have listed here could cause actual results to vary from what we have forecasted. Our press release, this presentation and reconciliations for all the non-GAAP measures were released this morning and are available under the Investors section on our website at parker.com.
Today, we have Jenny starting with an overview of our record FY '27 first quarter performance, and she's also going to provide some details on the recently completed acquisition of the Filtration Group Corporation. Following Jenny, I will go a little bit more in depth on the details for our first quarter financial results. And then we're both going to give a little color on the increase to our FY '27 full year guide that we increased this morning.
We will conclude the call with the normal question-and-answer session, and we will try to address as many calls as we possibly can. So now, if I could move your attention to Slide 3. Jenny, I will turn it over to you.

**Jennifer Parmentier** (Executives):
Thank you, Todd, and thank you to everyone for attending the call today. Our global teams delivered impressive first quarter performance. We achieved top quartile safety performance with a 9% reduction in our recordable incident rate. Safety is our top priority every day, and we remain focused on being the safest industrial company in the world.
Q1 sales increased 18% to a record $6 billion. Organic growth accelerated to 11.5%, and adjusted segment operating margin expanded 120 basis points to a record 28.6%. Adjusted earnings per share increased 23% to a record $8.90. This marks the first quarter we've delivered double-digit organic sales growth in over 3 years. And in the quarter, we completed the acquisition of Filtration Group Corporation, continuing our track record of disciplined capital deployment to compound performance. I'd like to thank our team members around the world for a great start to fiscal year 2027.
Moving to Slide 4, we are experiencing increased demand across our key market verticals. Demand is broad-based, and rolling 12-month order rates increased to 13% this quarter. This broad-based strength is evidenced by our backlog, which continues to climb higher, setting a new record of $13.7 billion in Q1. Aerospace, Industrial and Filtration Group all contributed to this increase in backlog.
Parker's portfolio is profoundly different today than it was 10 years ago when we began our portfolio transformation. Our portfolio has been shaped by our strategic positioning initiatives in The Win Strategy and has been transformed by acquisitions. Acquisitions have more than doubled the size of our Aerospace and Engineered Materials businesses, and we have more than tripled the size of our filtration business. This is clearly a different Parker, one with greater visibility and backlog, resulting in more consistent growth. Slide 5, please.
We've been looking forward to welcoming the very talented Filtration Group team members to Parker ever since we announced the transaction nearly 1 year ago. We were thrilled to complete the transaction in Q1 and continue our long-standing practice for a Parker leader to personally welcome the new team at every location. This slide shows pictures from just a few of our Day 1 events held around the world, welcoming the Filtration Group team to Parker. This is a great day for all of us, and we are excited to have Filtration Group in the Parker portfolio.
I'm on Slide 6. Filtration Group brings a diverse portfolio with strong brands, material science capabilities, highly engineered products, embedded application engineers and multiple R&D centers. Filtration Group has a global presence with sales split approximately 60% North America and 40% international. And they have a robust aftermarket business, increasing Parker's overall filtration aftermarket sales by 500 basis points.
This acquisition enhances and expands our exposure in markets we know well, including life sciences, HVAC and refrigeration, in-plant and industrial and transportation. Within life sciences, we have solutions for medical, diagnostic and test applications that include consumable separation technologies, pharmaceutical protection, special chemistry and material science solutions. In HVAC and refrigeration, we're adding complementary products and advanced media capabilities that ensure indoor air quality in places like hospitals, schools, museums and airports.
Moving to in-plant and industrial. We're adding proprietary media for liquid air and gas filtration, increasing safety and productivity. And within transportation, Filtration Group brings on-vehicle filters and desiccants engineered to an application-specific form factor, increasing cleanliness and efficiency.
With this acquisition, we are creating one of the largest industrial filtration businesses in the world with approximately $5 billion in annual revenue. Much like our previous acquisitions, this is highly complementary, brings new capabilities in existing applications as well as near adjacencies, thus expanding our addressable market and opportunities to create value for customers globally.
Moving to Slide 7. Our dedicated integration team is leveraging the Parker integration playbook with Filtration Group. We have a proven process and one that we continuously improve with each acquisition. We know from experience that cultural alignment is key to a successful integration, and we see this once again with the combination of Parker and Filtration Group.
Our integration teams are currently focused on the first pillar of The Win Strategy: Engaged People. In less than a quarter, our teams have already begun Kaizen events focused on safety improvements. This is the first step in building a culture of Kaizen that will later drive lead time reductions that drive customer experience and increase productivity.
The chart on the right shows for the first time, our expected cumulative cost synergies by year. Our fiscal year '27 guidance now includes Filtration Group and $40 million of synergies this fiscal year. Acquisition integration is a core competency here at Parker, and we are confident in delivering $220 million of cost synergies as we target taking Filtration Group's adjusted EBITDA margin to greater than 30%.
Now on Slide 9, many of you on the call today have seen this slide before, why we win. First, The Win Strategy is our business system. We have a decentralized operating structure. Divisions run by general managers with full P&L responsibility, acting like owners, close to their customers and executing The Win Strategy every day.
Next, we have innovative products to solve customer problems, 85% covered by intellectual property. Our application engineers provide the expertise that allows us to have a competitive advantage with our interconnected technologies that provide efficient solutions for our customers. 2/3 of our revenue comes from customers who buy 4 or more technologies.
And finally, our distribution network is the best in the world. It is truly an extension of our engineering team, providing solutions to all those small to midsized OEMs that are participating in capital spending and investments. These partners are experts at applying our interconnected technologies.
Todd, I'll pass it over to you for some first quarter highlights.

**Todd Leombruno** (Executives):
Thank you, Jenny. We always talk about finishing strong. Well, this is a quarter where we started the year strong. As Jenny said, I'm on Slide 10, and I'm just going to go through a real quick review of the first quarter results. It was a strong quarter, double-digit sales growth, resulting in strong margin expansion and 23% EPS growth.
Sales were up 18% versus prior year. We reached $6 billion for the first time in the history of the company. Organic growth, as Jenny mentioned, was 11.5%. Acquisitions, all in, added 7%. Most of that was from the Filtration Group Corporation, but we do have one last partial quarter of Curtis sales in there that totaled to 7% for all acquisitions.
Segment operating margins are up 120 basis points from the prior year, finished at 28.6%. That obviously is a record. Adjusted EBITDA margin was also a record at 28.5%. That's also up 120 basis points from prior year. And adjusted net income was a little bit over $1 billion, $1.1 billion, which is 18.9% return on sales, and that's how we get to $8.90 in adjusted earnings per share. That is up 23% versus prior. Like I said, it was just a really strong start. It's great to start the year with double-digit organic growth and 23% EPS growth. Really glad to see that.
On Slide 11, this is the walk. You can see it was just a really clean quarter. Essentially, all of our EPS growth came from strength across our operations. Segment operating income dollars are up by $327 million. That happens to also be 23%. That added nearly $2 of EPS to our EPS growth for the quarter. Lower shares outstanding was favorable by $0.04. Income tax was also slightly favorable, just $0.01.
And interest expense, as expected, was higher. That is really related to the newly issued debt that we took out to acquire the Filtration Group. Corporate G&A and other was negative $8 million, and that was really driven by higher market-based benefits, nothing really out of the ordinary there. And that's really how we get the $8.90 in adjusted earnings per share. So really just a great quarter. Thanks to our teams for converting 11.5% organic growth into 23% EPS growth. Just a great operating performance across the company.
Now if we move to Slide 12 and look at segment performance. Rolling orders on a 12-month basis accelerated for the company to plus 13% versus prior year. And as you can see, there's double-digit growth across all reported businesses on the 12/12 order report. Organic growth, like I said, was 11.5%. That did exceed our guide. We were guiding 8%. Margins are up 120 basis points, and that is a new record.
If we look at the North American businesses, sales are up 20%. That is a record $2.4 billion. Organic growth in North America was 9.4%. We saw positive growth across all market verticals, and that includes distribution. Margins were up 60 basis points versus prior. That finished at a record 27.6% for the North American businesses, and we continue to see margin expansion from executing The Win Strategy and really leveraging higher productivity on that sales volume. Orders in North America also increased 200 basis points to 11% compared to prior year. And as Jenny said, strength across all market verticals in the North American business. It's just a great way to start the year for North America.
If we slide into the Diversified Industrial International businesses, what a quarter here. Sales were a record $1.7 billion. That's up 22% versus prior year. Organic growth was 11.6%, and that was really led by outstanding growth in our Asia Pacific businesses. Organic growth in Asia Pacific was 23.4%. It was also great to see the EMEA region go positive at plus 4%. And as you can see, Latin America is just a slight drag at minus 1%.
Margins here are the standout, 270 basis points of margin expansion versus prior year. The 27.7% is a record for the international businesses. Really seeing results from a lot of restructuring activities over the past year or 2, some growth from new business wins and obviously, executing The Win Strategy over and over and over again. On the order front, international orders increased 400 basis points to 14% with sequential increases in both Asia Pacific and EMEA. It was a record quarter across multiple metrics from our international team, and they did a great job starting the year. So thanks to all of our international team members.
Moving over to Aerospace, just another exceptional quarter of double-digit organic growth. Sales were a record at $1.9 billion. That's up 14% versus prior year. All 14% of that is organic and really strength across both the OEM and aftermarket businesses. You look at margins, they expanded margins 70 basis points versus prior year. They also achieved a new record of 30.7%. And that margin performance is really a result of great productivity, those higher volumes and stronger-than-expected commercial aftermarket growth. Order rates continue to be elevated in Aerospace at plus 14%, and we continue to see strong mid-teen commercial aftermarket order growth. Another great performance from our Aerospace team. Thank you.
On Slide 13, we talk about cash flow. Cash flow from operations was $752 million; that's 12.6% of sales. Free cash flow came in at $643 million. That's 10.7% of sales. That is slightly lower than last year. All of it is related to just bringing in the Filtration Group acquisition. If you remember last week, our Board approved our quarterly dividend of $2 per share. That is the company's 306th consecutive quarterly dividend.
And on cash flow, we are committed to achieving 100% conversion for the year. If you remember, our cash flow is second half weighted. We issued the new debt this quarter to acquire the Filtration Group. Those interest rates on average, are just slightly over 4.5%, and that pushed our net debt to adjusted EBITDA to just 2.7. So those are the details on Q1. 
Jenny, I'll turn it over to you, and we can start guidance.

**Jennifer Parmentier** (Executives):
Thank you, Todd. I'm on Slide 15. Our fiscal year '27 organic growth forecast by key market vertical. As previously mentioned, with strong and broad-based demand, we are raising our midpoint organic growth guidance 200 basis points from 7% to 9%. For aerospace and defense, our largest vertical, we are raising guidance to approximately 10% organic growth. Commercial aftermarket orders accelerated and OEM continued strong.
We are also raising our growth outlook for in-plant and industrial to high single-digit growth. We continue to see demand broaden and strong orders from our distributors. For our transportation vertical, we now forecast high single-digit growth, led by continued strength in heavy-duty truck, which has been driven by production rate increases.
Moving to off-highway. We are guiding mid-single-digit growth. We see continued strong nonresidential growth driving construction. Mining strength continues as well, which is supported by commodity prices. We also expect mid-single-digit growth for energy. We see sustained growth from our businesses supporting gas turbine power generation, while we are still expecting oil and gas to be flat this year. Lastly, we are guiding mid-single-digit growth in HVAC and refrigeration. This growth is led by commercial HVAC followed by refrigeration.
So in summary, we are raising the organic growth forecast for our 3 largest market verticals and still expect positive sales growth across all market verticals, resulting in an organic growth forecast of 9% at the midpoint. 
I'll hand it back to Todd to share more details on guidance.

**Todd Leombruno** (Executives):
Well, thanks, Jenny. I'm on Slide 16. And as Jenny said, we are raising our full year guidance. That's obviously based off the strong performance we had in Q1, the robust order levels and then, of course, including the Filtration Group in our numbers. On reported sales, we're increasing the range of growth to 16% to 19% or roughly 17.5% at the midpoint. Specifically, for the Filtration Group, we are including $1.85 billion of sales to the guide for FY '27. That's obviously a stub year. It's roughly 10.5 months of ownership. If you take that $1.85 billion plus the little bit that's left over from Curtis, acquisitions will account for roughly 9% of the sales change. Currency is really just a slight drag at 0.5% and that is based on September 30 spot rates.
Jenny mentioned this, but we are increasing organic growth to a range of 7.5% to 10.5%. That's 9% at the midpoint. Aerospace organic growth, we are increasing that 150 basis points to now 10% at the midpoint. The Industrial North American businesses organic growth is being raised by also 150 basis points to 8% at the midpoint. And the Industrial International businesses are being raised by 400 basis points to 9.5% organic growth at the midpoint.
For the full year, adjusted segment margins are expected to increase by 20 basis points versus the prior guide, that would go to 27.9% for the year, and that includes raises in all 3 reported businesses. That would be a 60 basis point increase versus prior year all in, and that would include incorporating the Filtration Group into Parker-Hannifin numbers.
Just a few items to note. Corporate G&A is just up slightly by $10 million. It was $200 million. We now expect it to be $210 million. Other expense is down by $10 million. It was $100 million. Now we expect it to be $90 million. And interest expense has been increased. This is all really related to the Filtration Group debt. We now expect $690 million of interest for the year. Previously, that was $340 million without the Filtration Group acquisition. And really no change to tax rate, 22.5% tax rate.
Adjusted EPS has been raised to $36.85, which I will break down a little bit further in the next slide. The range on that is plus or minus $0.40 and the split is, as usual, 48% first half, 52% second half. And as I mentioned before, we are also raising our free cash flow guidance to a range of $3.5 billion to $4 billion. That is $3.75 billion at the midpoint and conversion will be approximately 100% for the year.
If we look specifically at Q2, reported sales are forecasted to be nearly $6.2 billion. That is a 19.5% increase versus prior. Organic growth, we expect to be about 10% for Q2. For adjusted segment operating margins, we are forecasting 27.6%, that is all in. And adjusted EPS is now expected to be $8.82 for the quarter.
On Slide 17, we provided this just to kind of show the increase. Just with a couple of moving pieces with Filtration Group coming in. You can see our previous guidance here was $34.75 for the year. We are increasing that to $36.85. I just want to point out that $1.70 of that increase is coming from increased segment operating income dollars based on the higher organic growth and great incrementals in our legacy business. Just a great quarter to start the year, and we expect that to continue throughout the year.
For Filtration Group, in FY '27, we expect this to be adjusted EPS accretive of $0.50. That is for the first 10.5 months of ownership. There was really no impact in Q1. The segment operating margin was offset by the interest expense. But for the next 3 quarters, we're expecting $0.50 of accretion. That includes the $40 million of synergies that Jenny mentioned earlier. 
And then lastly, just corporate interest and other, just a slight bit higher, $0.10 higher, and that brings the total raise for the year to $2.10 or 6% from what we just initiated 3 months ago. As usual, we've got additional guidance details in the appendix. Just in summary, FY '27 is off to a fantastic start. We're excited to welcome the Filtration Group team members to Parker-Hannifin. 
And with that, Jenny, I'll hand it back to you.

**Jennifer Parmentier** (Executives):
Thanks, Todd. I'm on Slide 19. Today, we are excited to announce our 2027 Investor Meeting on May 13, 2027. Similar to our last investor meeting 3 years ago, this meeting will be in person and webcast from New York City. Please save the date, and we look forward to sharing more details as we get closer to the event.
And moving to our final slide, a reminder of what drives Parker. Safety, engagement and ownership are the foundation of our culture. It is our team members living up to our purpose every day that drives top quartile performance and allows us to be great generators and deployers of cash.

**Todd Leombruno** (Executives):
Okay. Well, we are ready for the Q&A portion of the call.

**Operator** (Operator):
[Operator Instructions] We'll go first this morning to Andrew Obin of Bank of America.

**Andrew Obin** (Analysts):
Just a question, Jenny, congratulations. We've been in meetings for, I think, what seems like eternity where the team was hoping for the industrial recovery that sort of never seemed to come. It does seem -- finally seems to be here. What has changed that we now seem to have like 2 quarters of recovery? And how much visibility and comfort do you have going forward? And obviously, you've raised the guide, but maybe expand a little bit.

**Jennifer Parmentier** (Executives):
Andrew, thank you. Yes, I feel like I've been saying positive sentiment and a gradual recovery for quite some time. And obviously, in Q1, what we saw was a broadening recovery across all the markets. I would tell you that it's been robust electronics and semiconductors growth, double-digit growth. We've been able to raise in-plant and transportation market verticals. Obviously, it's just really been great in all aspects of the markets that we raise.
So I think that it's just been that the orders that we've seen and the positive sentiment has turned into some momentum here in shipments and increased orders as demonstrated through the quarter. I would tell you that there's nothing that we see right now that would cause us to be concerned about the outlook. Obviously, we've raised the guide here. We feel confident in this guide. And we're real pleased with the orders and how the team executed throughout the quarter. We've been talking about all the work we do no matter what's going on, and the volume really turned into some nice bottom line performance.

**Andrew Obin** (Analysts):
Yes. Great to hear. And maybe a follow-up. You highlighted that in aerospace, commercial aftermarket was a positive surprise. I know a lot of concerns about that starting in the summer. Maybe clearly, you talk to your customers, what's driving the upside there?

**Jennifer Parmentier** (Executives):
Yes. I mean we saw double-digit growth. We saw plus 14% in both OEM and aftermarket. It was really the second highest quarter of order bookings for us ever. And we do expect this strong demand to continue. So we're not seeing a lot of retiring aircraft, right? So aftermarket continues to be strong.

**Operator** (Operator):
We'll go next now to Mig Dobre with Baird.

**Mircea Dobre** (Analysts):
Appreciate all the commentary on growth and orders things seem to be going well, but just sort of acknowledging what's going on in the capital markets here, especially post election, there's obviously concerns about the AI infrastructure build-out. And I'm not really asking you to forecast how that's going to go because who knows. But really, can you help us better understand what your exposure is as you kind of look at your business because you obviously have some direct exposure, but there's also probably some indirect exposure. So as you sort of think about this vertical and the risk that, that poses on a go-forward basis, it would be great to hear your thoughts. And specifically in your Asia business, where we've seen really very, very strong growth, how much of that do you think is related to this particular vertical?

**Jennifer Parmentier** (Executives):
So just a couple of points to make. So data centers does continue to be a high-growth driver for us with double-digit growth in the quarter. We're continuing to get business in this space and orders and backlog are strong. We have nice exposure and growth, but this is not yet large enough for its own vertical. We finished the fiscal year with data centers making up approximately 1.5% of Parker sales.
So this is a great interconnected technology story from all the products that have been in the Parker portfolio for quite some time. And we are working with industry leaders. We have the ability to provide the liquid cooling systems and subsystem components. And the Asia Pacific orders are strong in electronics and semicon, and that was just a really strong area for the quarter. So as I previously mentioned, we feel good about the orders that are out there. And we think this is going to continue to be a growth area. But again, not quite a market vertical for us.

**Mircea Dobre** (Analysts):
That's helpful. And then my follow-up, just to maybe double-click on your comments on commercial aftermarket. If you were to kind of think about it by region and think about the Middle East specifically, I'm wondering 2 things, how that specific region has progressed or [indiscernible]? And is there potential for some sort of a catch-up if maybe conditions in the Middle East change sometime in 2027?

**Jennifer Parmentier** (Executives):
I think commercial aftermarket has been strong, and it continues to be strong. So I wouldn't note any dip related to anything that we saw with that conflict. Our -- we're raising our guide to high single-digit growth for fiscal year '27. So it's strong orders in Q1. As I mentioned before, we're just not seeing a lot of the aircraft retiring. So that aging fleet is driving the growth. But I wouldn't say that it went down enough to say there was a reaction to anything going on. And obviously, orders in Q1 were strong.

**Operator** (Operator):
We'll go next now to David Raso with Evercore ISI.

**David Raso** (Analysts):
I was curious if we can dive into the international guide, the 400 bps increase. Which geographies drove that? And obviously, if you can help us a bit how you think about the geography guide within the total international organic? And also the margins, they're obviously very high in the first quarter. And while you raised the margin guide, they're still lower than the first quarter. Just curious how you're thinking about that, why the first quarter would be that much higher than the full year guide?

**Jennifer Parmentier** (Executives):
All right. Well, I'll dive into what's going on with the international guidance for you. So full year organic growth is now 9.5%. As Todd said, that's a large increase to the initial guide and Q2 guide is approximately 11%. So in EMEA, we have guidance at low single-digit to mid-single-digit growth for the year. That's really mixed market conditions, David. Strong growth in energy, mining and defense and what we see as a gradual recovery in heavy-duty truck and construction.
In Asia Pacific, this has been very strong. We're raising guidance to mid-teens organic growth. This was previously high single digit, and we're really seeing continued strong electronics and semicon demand. In-plant orders and shipments progressed. In Q1, we saw double-digit distribution growth, and we're seeing the orders and the shipments continue to progress. And then mining and energy strength continues in Asia Pacific. Latin America, guidance is at low single-digit organic growth, and we're still seeing a broad-based softness across that region.

**Todd Leombruno** (Executives):
David, this is Todd. I would just add a little bit. Q1 was stellar, absolutely stellar. And if you look at what we're doing, we have increased the margins really for all businesses, North America, International and Aerospace for the remainder of the year. We did have Filtration Group for basically 1.5 months in Q1. We're obviously going to have it for 3 [ quarters ] (sic) [ months ] in Q2. Those jumping off margins are lower than our existing businesses. So there's a little bit of a drag there until those synergies really start rolling in there. But if you look at incrementals outside of all of that, we are high 30s, low 40s on incrementals in the guide here. So we feel like we're being pretty aggressive here on the forward outlook. Just -- Q1 was just stellar.

**David Raso** (Analysts):
And a quick follow-up. The meeting, I know it's many months out. But can you give us a little framework of what prompted calling the meeting and how we should think about -- obviously, things are operating pretty well right now. Just curious the reason behind the meeting, we're always happy to meet with you, but just curious what we should expect broadly speaking and why we called the meeting.

**Jennifer Parmentier** (Executives):
Well, we usually in the past, have done a meeting every 2 years. This will be 3 years. And we expect that we're going to be able to share some information with you and some news with you. But it is a ways out yet. So we're really not in a position today to talk too much about the details of that meeting.

**Operator** (Operator):
We'll go next now to Jamie Cook with Truist Securities.

**Jamie Cook** (Analysts):
Congratulations on another nice quarter. I guess just 2 questions. One, just given Filtration Group is closed and we understand what the implied guide is for 2027. But can you just give us an update on how that business had been performing in terms of organic growth, margins? And then, I guess, any incremental insights you have on potential upside to synergies?
And then my second question, Jenny, just relates to, obviously, industrial demand is very strong. Everyone is very -- we're seeing that in your numbers. I think people are questioning sort of to the durability of the cycle. So in an environment where potentially industrial demand tempers, how do you think about your ability to, in a less robust market, achieve the 4% to 6% organic growth that you target, just given some of the changes in your portfolio with M&A and the portfolio more positioned towards secular growth, just your confidence in the 4% to 6%, assuming doomsday and industrial demand tempers.

**Jennifer Parmentier** (Executives):
Okay, Jamie. So starting out with Filtration Group. So their Q1 performance was what we had expected. Historically, they've performed at a positive mid-single-digit growth CAGR. Life science business is one of their fastest-growing markets right now. As Todd said, the guide includes $1.85 billion of sales and Q1 actual was $285 million. We expect this to be accretive, as Todd said, the 10.5 months, an accretion of $0.50.
So these -- this is a good business. It's a business with complementary technologies to what we have, markets that we know, and we expect that this is going to be a good growth business and fit nicely, especially with the additional 500 basis points of aftermarket. We feel very confident in the $220 million in synergies, that's 11%, $40 million for this fiscal year. The integration team has been working very hard. They've been -- they were planning ahead of the close, and they've worked very closely with Filtration Group. And as I mentioned, Kaizen events are in full swing, and we really, really have had success in the past by focusing on that first pillar of The Win Strategy, and we're off and running there.
Now as far as international demand and our confidence about the targets that we put out there, 4% to 6% organic growth, we feel very confident about hitting those targets. We have transformed this portfolio very, very much on purpose to be able to do that. I think when you look at the durability of the short-cycle businesses right now, there's clear signs of positive short-cycle demand through orders and shipments. Both OEM and distribution short-cycle orders were positive double digits, and this acceleration is just continuing on a broadening recovery.
And as I already mentioned, we raised our forecast on in-plant industrial as well as transportation to high single digits. And the rest of the market verticals remain positive. It's very encouraging, as I mentioned at the very beginning to see the distributor purchases to really increase, and they're driven by strong end demand. And again, as I've said for a long time, the sentiment is very positive, and now it is really supported not only by the orders, but by the shipments.

**Operator** (Operator):
We'll go next now to Scott Davis with Melius Research.

**Scott Davis** (Analysts):
Congrats on the good -- great start -- not a good start, a great start. There's not a lot to pick on or ask, frankly; things are so clean. But I'm kind of curious to what extent you're willing to share with us where Filtration Group kind of stands today as it relates to on-time delivery, quality, kind of the key metrics that you guys obviously care about. Even if you're not willing to share the exact numbers, some sense of kind of where the opportunity lies, I think, would be helpful for us.

**Jennifer Parmentier** (Executives):
Yes. So obviously, part of the integration is integrating everything into a lot of the Parker metrics and indicators. But the thing that we've obviously been most focused on is safety, right? What's very important to us is that people come to work every day and feel safe in their environment and that we have a culture where we're taking care of each other and making sure everyone is safe. That is the foundation for everything when it comes to high-performance teams, successful Kaizen events. And then obviously, as we know, leads to taking care of the customer and growing profitably.
So safety is a big focus. We're not ready to disclose any specific numbers. I don't know that we really ever do talk about those metrics with the acquisitions. But we will be putting them into our metrics that are really about making sure that we're on time to the customers' request date and that we're continuously improving upon how we serve the customer. They have -- these are good businesses. They have a lot of evidence of having the basics of some of the visual management that Parker believes is key to running any operation. But again, we also see a lot of upside with the Parker Lean system and implementing all the tools and The Win Strategy.

**Scott Davis** (Analysts):
And thanks for that, Jenny. But my understanding, the Filtration Group was kind of built over time with a bunch of acquisitions and bolt-ons itself. And so how heavy of a lift is it to integrate? I imagine there's a number of different ERP systems. And obviously, you're going to want to integrate it to some extent, I would think, but I'll ask that as part of the question as well. But how heavy of a lift is it overall? And then to what extent do you plan to integrate, I guess, is my question.

**Jennifer Parmentier** (Executives):
Yes. I mean, obviously, you are correct. That's the way it was built over time. These are very decentralized, which is a positive, though, because the leaders of these businesses very used to being held accountable to their P&L statement. So that's a positive, and that feeds right into the Parker culture. So we like that about it. But none of these integrations are "easy", right? I would say that there's a heavy lift component to each acquisition. And we obviously will want to bring those together and integrate them. 
And one thing to remember here, too, is that we've taken these filtration businesses and put them into existing Parker divisions, right? And within those leadership teams, you'll wind up with legacy Parker leaders and Filtration Group leaders. So that really does help with getting The Win Strategy ingrained into the division and bringing everybody on board with the work that needs to be done. So heavy lift, yes, but this is a core competency for us. And we feel very confident about being able to integrate all these locations and really make this a successful acquisition.

**Operator** (Operator):
We'll go next now to Julian Mitchell with JPMorgan.

**Julian Mitchell** (Analysts):
Maybe just my first question around the Aerospace segment organic sales growth outlook for the balance of the year. Maybe just help us understand kind of how you're thinking about commercial, aero, OE and aftermarket versus the same for defense and just flesh out sort of how Q1 started for those pieces, please.

**Jennifer Parmentier** (Executives):
Yes. So if you want to just talk about the guidance for Aerospace. So just starting out, the OE aftermarket split for the fiscal year is guided to 53% OE and 47% aftermarket. We did have a mix of 52% and 48% in Q1. So as we said, stronger commercial aftermarket than we expected. And I would tell you, too, one of the things that is really contributing to our Aerospace group's ability to deliver is the team has worked very hard on demand and capacity planning in aerospace as well as partnering with the supply chain and really investing in the supply chain over the last several years. So this full year guide of approximately 10%, we're very confident about that with the initial guide being 8.5%.
We are seeing commercial OEM guide remains at mid-teens growth for fiscal year '27. Commercial transport build rates are increasing. And as we all know, aircraft demand still is greater than supply. For commercial MRO, we are raising guide to positive high single-digit growth for fiscal year '27. So as I mentioned already, there's an aging fleet driving aftermarket growth. We're not seeing a lot of retirements. Engine repair shop visits and component demand continues. And we're clearly, again, seeing the benefits of our team really working closely with the customers, understanding what the demand is, seeing the increases come, knowing about them before they come and making sure that we're able to help them achieve their production rates.
On defense OEM, we're raising the guide to high single-digit growth for fiscal year '27. We see strong demand for global fighter jets. The orders continued strong in the quarter, and we're raising this guide based on firm demand from our customers. And defense MRO, guide remains at mid-single-digit growth for fiscal year '27. We're still seeing fleet upgrades and service extensions, a focus on retrofits and upgrades as the fleet ages. And again, I would say with both of these, this is a long-cycle business, but we're raising guidance on the demand we see today, and we're focused on making sure that we serve these customers.

**Julian Mitchell** (Analysts):
That's very helpful. And then maybe just a quick follow-up on the second quarter EPS guide. I think it implies a slight tiny decline sequentially on EPS. Normally, that number is up sequentially. I understand maybe some margin effect from Filtration Group. Is there anything else beyond that? And is there something with Filtration Group where the margins in International are particularly sort of dilutive to that segment?

**Todd Leombruno** (Executives):
No, it's not so much, Julian, the mix between North America and international. I would say the -- a full quarter of interest has got a little bit of a drag on EPS there. But we look at our incrementals, the incrementals that we're guiding to for the total company is above 30%. If you look at the legacy business, it's much higher. The math gets a little wonky because we don't have Filtration Group in the prior year. But I would say there's nothing out of the ordinary other than maybe the additional interest.

**Operator** (Operator):
And we'll go next now to Joe O'Dea with Vertical Research.

**Joseph O'Dea** (Analysts):
You made a couple of references to seeing some improving demand out of the distribution channel. And so I was looking for a little bit more color there. I think you've talked for quite some time about the indications of interest being better, but actually now seems like you're -- just any perspective on the growth rate you saw in North America and international out of that channel how that compares to some of the recent quarters, just to get a better understanding of acceleration there?

**Jennifer Parmentier** (Executives):
I would say that we started to see this in Q4. We talked about it during the last call about seeing increased orders from distribution. And what we saw in Q2 was positive double digits, right? So we saw stronger orders in Q2 (sic) [ Q1 ]. Now I wouldn't call this a restock. That's not what we're hearing from the channel. But obviously, the orders have increased and they're increasing to real demand. They're participating in a lot of capital investments, a lot of infrastructure, automation. So I would say that it truly is a broadening recovery and distribution is playing very well in it.

**Joseph O'Dea** (Analysts):
And then on the inflationary side of things, when we think about the 200 basis point increase in organic growth guidance, any contribution to that from pricing that you've had to do? And then as you think about the full year, is the anticipation that price/cost is both dollar and margin positive?

**Jennifer Parmentier** (Executives):
Yes. So on inflation, we definitely are still seeing increases across a range of material cost inputs as well as logistics. But this is a strong muscle for us. We're experts at managing this. Our Win Strategy supply chain tools, they're the best. We work closely with -- everybody in the organization is working closely with our pricing team. And we've taken some action where we needed to. We'll do that in the future, if needed, but we are really, for the most part, back to a very normal pricing environment on the industrial side of the business.

**Todd Leombruno** (Executives):
Joe, I would say the increase in the organic growth is really demand related. It's not price related, it's demand related.

**Operator** (Operator):
We'll go next now to Brett Linzey with Mizuho.

**Brett Linzey** (Analysts):
I wanted to come back to the industrial margins, obviously moved structurally higher here. As volume recovers and orders are picking up, you're generating these new project wins, is there any additional required capacity investment or reallocations in some of those divisions that would influence the path to those long-term targets?

**Jennifer Parmentier** (Executives):
We have done a really nice job over the last couple of years of increasing capacity where we needed to. We have been able to generate additional capacity through use of Kaizen and the Parker Lean system. That's a very strong muscle for us as well. So there is not what I would call any significant investment that will need to be made. We will continue to increase our productivity. We'll continue to use all these tools. And on the higher volume in Q1, obviously, the teams were able to deliver that. And we see that, that will be the case for the rest of the fiscal year in the foreseeable future.

**Brett Linzey** (Analysts):
That's great. And then just one more on OE within Aerospace. So on Boeing and Airbus, just wanted to better understand how much of the production rate normalization is actually in the plan versus maybe upside to the guide? Like what are the build rate cadence that you're thinking about or effectively assuming in the framework?

**Jennifer Parmentier** (Executives):
Well, as I mentioned before, listen, our teams are working very closely with these big customers. And the production rates that they're sharing with us and the demand capacity planning we're doing, that's what's in our guidance. So we don't specifically talk about customer build rates. But we don't expect any surprises there, and we know what their plans are.

**Operator** (Operator):
We'll go next now to Andy Kaplowitz with Citigroup.

**Andrew Kaplowitz** (Analysts):
Todd, maybe just focusing on the energy piece of your portfolio. It's one of the slower growing portions of your portfolio even with that power gen business in there. So maybe just are you seeing any signs of life in oil and gas, given the higher sustained energy prices and what seems like energy security type work? And could you talk about the underlying strength of your power gen business at this point?

**Jennifer Parmentier** (Executives):
Well, it is positive mid-single-digit growth. And as you know, energy, the vertical is about 7% of our sales. So we see robust long-cycle power gen demand. That's been very strong. But with oil and gas, the forecast is flat. Upstream remains constrained. There's some benefit in midstream from some infrastructure build-outs. But right now, the best view we have is that mid-single-digit growth.

**Andrew Kaplowitz** (Analysts):
Tough one. I think, Jenny, one of the main reasons why you bought Filtration Group was its aftermarket business. So it's obviously early days in terms of your ownership. But what did they do, if at all, differently than Parker that could help you? And then I think just you mentioned life sciences their biggest business. Are they seeing any improvements in that business? Or can you see above mid-single-digit growth in that business going forward?

**Jennifer Parmentier** (Executives):
Yes. Well, there's many reasons why Filtration Group was very attractive to us and why we had watched this business for quite some time. And it's not just one thing. It's very nice to have higher aftermarket, right? That is something that plays right into Parker's success. But really, the complementary and proprietary technologies is really one of those things that we look for in an acquisition. And it does expand our presence in life science. Life science is an area that is growing higher than the rest for them right now.
But it also brings a lot of proprietary media for markets that we already play in. So this is -- Andy, this is just a good performing business that we're going to just improve upon. And we think that there's plenty to learn here. I would say it's still early days about learning all of how they go to market and how they handle their channels, but we think that we can learn from that, and we also think that there's some things that we do that might fit well within Filtration Group.

**Operator** (Operator):
We'll go next now to Steve Tusa with Wells Fargo.

**Charles Stephen Tusa** (Analysts):
Just on this, I guess, any sort of color on -- I know you don't disclose price, but any directional color on how that may have impacted the incrementals? I mean is it the neutral to the margin? Just any kind of high-level color on the price/cost situation.

**Todd Leombruno** (Executives):
Yes, Steve, I'll start. If Jenny has got anything to add, I'll let it go there. Really no impact on the incrementals on price. This is something -- Jenny mentioned it earlier, this is something we do all the time. We try to remain margin neutral. So there's no like levers that we're pulling to try to make it so that we're improving our incrementals on that. The result was based off great demand, great volumes and unbelievable execution across every single one of our businesses.

**Charles Stephen Tusa** (Analysts):
Yes. And then just on the meeting, Jenny, I think you said -- I mean, you said expect some news. I know it was -- I don't know, it was kind of cryptic.

**Jennifer Parmentier** (Executives):
I changed my words around. I said we'll have some news for you.

**Charles Stephen Tusa** (Analysts):
Okay. But I mean, is that -- obviously, like the long-term targets can be reset. Is there any thought or consideration to like a more holistic portfolio evaluation from that perspective?

**Todd Leombruno** (Executives):
Steve, I wouldn't go that deep. I would say, hey, it's a few months out from now. We obviously just closed the Filtration Group. We will have closed CIRCOR. By the time that comes, the company will be over $25 billion in total revenue. We're going to give you some color on what the company looks like today and what we're planning on doing over the next 5 years.

**Jennifer Parmentier** (Executives):
Yes, well said.

**Operator** (Operator):
We'll go next now to Varun Govindaraj with Bernstein.

**Varun Govindaraj** (Analysts):
Linked a little bit to what we just talked about. I mean, as you continue to get larger, do you see a big enough pipeline of complementary M&A assets out there that can materially move the needle like Meggitt and Filtration Group are expected to? Or should we think about this as more bolt-ons going into the future?

**Jennifer Parmentier** (Executives):
So Varun, there are deals, assets of all sizes in the acquisition pipeline, right? And one of the things that we often talk about is making sure that, that pipeline stays active and healthy, and that's something that we've done for quite some time. So we think a lot of times, we're not -- most of the time, we're not in control of the timing of those, but we do believe that the pipeline is still robust and that there are assets out there that we are interested in, definitely.

**Varun Govindaraj** (Analysts):
Perfect. Appreciate the color. And then just as a follow-up, could you remind us on backlog conversion in general, how much of that revenue tends to convert to revenue over the course of the next 12 months? And should we expect any changes there just given the shift in mix of the business?

**Todd Leombruno** (Executives):
We don't expect any dramatic change to that conversion rate over the next year or so. It's roughly 75% of the backlog converts to sales in a 12-month period. But there's always a lot of move-ins and moves out of there. So that's not something that we really look at when we're looking at forecasting, but it's roughly 75%. 
Bo, this is Todd. I think we maybe have time for 1 more today.

**Operator** (Operator):
Understood. Mr. Leombruno. We'll take that final question today from Jeff Hammond of KeyBanc.

**Jeffrey Hammond** (Analysts):
Maybe just last one on Filtration Group, a lot of good color there, Jenny. And I know you don't include revenue synergies. But as you look at the portfolio early on, just any clear opportunities, whether it be distribution complements, market complement, geographic, where there's some clear revenue synergies to think about?

**Jennifer Parmentier** (Executives):
Yes. Jeff, you're right. We don't model any revenue synergies, but we are definitely seeing areas of opportunity, areas where we can leverage Parker technologies to Filtration Group customers and then leverage Filtration Group technologies to Parker customers. So we are -- the integration team, although they're focused on obviously integrating the businesses and achieving the synergies, our sales and marketing teams are working closely together to identify those opportunities. And we definitely believe that there are some there.

**Todd Leombruno** (Executives):
Yes, Jeff, we also have real early days here, but we found some capacity opportunities where we've been able to utilize the existing filtration capacity within our legacy businesses to help some of those Filtration Group Businesses.

**Jennifer Parmentier** (Executives):
Yes -- that was discovered early on, like 3 weeks in. And so a lot there.

**Todd Leombruno** (Executives):
Super happy to get it closed. Team is working hard, and we're going to do it again, just like we've done in the last couple of deals.
Excellent. Okay. So that concludes our FY '27 Q1 earnings release webcast. Thank you all for joining us today. As usual, our team of Investor Relations, Jeff Miller and Jenna Stuckey will be available for any follow-ups or clarifications if anyone has any. Thank you again, and have a wonderful day.

**Operator** (Operator):
Thank you, Mr. Leombruno, and thank you, Ms. Parmentier. Again, ladies and gentlemen, that will conclude Parker-Hannifin Corporation's earnings conference call. We'd like to thank you all so much for joining us today and wish you all a great remainder of your day. Goodbye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PH_Q4_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 銷售成長指引區間 5.5%–8.5%，中點 7%（原話："Reported sales growth for the year is going to be in the"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 調整後 EPS 指引中點 $34.75（原話："full-year adjusted EPS is going to be $34.75 at the midpoint"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 調整後部門營業利益率指引中點 27.7%（原話："On adjusted segment operating margins, we're guiding 27.7%"）
- 2026-08-06｜CFO Todd Leombruno｜margin：FY27 增量利潤率預期接近 30%–35% 區間上緣（原話："we're forecasting that near the top end of our stated 30%"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：指引不含待完成的 Filtration Group 與 CIRCOR 收購（原話："does not yet include any impact from the pending Filtration"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 第一季 EPS 指引中點 $8.07（原話："adjusted EPS is expected to be just over -- a little over"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 自由現金流指引 34–39 億美元，轉換率約 100%（原話："range of $3.4 billion to $3.9 billion. That is free cash"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：航太 FY27 有機成長中點 8.5%（原話："Aerospace, we expect 8.5% organic growth at the midpoint."）
- 2026-08-06｜CEO Jennifer Parmentier｜guidance：首度所有終端市場指引皆為正成長（原話："first time ever, we are guiding positive sales growth"）
- 2026-08-06｜CFO Todd Leombruno｜guidance：FY27 EPS 橋接含非美元匯兌有利因素不再重現的 $0.14 不利（原話："due to the non-repeat of some favorable foreign currency"）
- 2026-08-06｜CEO Jennifer Parmentier｜commitment：新利潤率目標：FY31 調整後部門營業利益率 30%（提高 300bp）（原話："We are raising it by 300 basis points to 30% by fiscal year"）
- 2026-08-06｜CEO Jennifer Parmentier｜commitment：維持循環期有機成長 4–6%、FCF 利潤率 17% 等長期目標（原話："we remain committed to organic growth of 4% to 6% over the"）
- 2026-08-06｜CEO Jennifer Parmentier｜commitment：新目標已納入尚未完成的收購（原話："Obviously, in these targets, we've included the"）
- 2026-08-06｜CFO Todd Leombruno｜margin：CFO 說明 FY31 利潤率提升在五年間大致平均分布（原話："spread pretty equally across those years, each of the five"）
- 2026-08-06｜CFO Todd Leombruno｜margin：CFO 個人判斷工業部門利潤率擴張幅度會大於航太（原話："would say the North American or the industrial businesses"）
- 2026-08-06｜CFO Todd Leombruno｜margin：第四季調整後部門營業利益率 28.0%，年增 110bp（原話："segment operating margin for the quarter was 28.0%. That is"）
- 2026-08-06｜CFO Todd Leombruno｜margin：定價面：管理層表示要回到正常定價環境（原話："we want to return to a normal pricing environment."）
- 2026-08-06｜CEO Jennifer Parmentier｜guidance：北美工業成長指引全為量、無價格貢獻（原話："We're back to a normal pricing environment here, and this"）
- 2026-08-06｜CEO Jennifer Parmentier｜margin：航太仍有定價空間，部分談判仍在進行（原話："normal pricing environment. And in Aerospace, there's still"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：訂單口徑改變：FY27 起工業部門改用滾動 12 個月訂單率（原話："we are announcing a move to rolling 12-month order rates"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：管理層對改口徑的解釋之一：國際訂單過去波動大（原話："international orders have been very choppy in the past"）
- 2026-08-06｜CFO Todd Leombruno｜customer：第四季積壓訂單年增 16%，創紀錄 128 億美元（原話："Backlog increased 16% versus prior year and is now a new"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：敘事變化：經銷商復甦由「漸進」說法改稱「擴大中」（原話："a broadening recovery instead of what we've just been"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：管理層明言不認定通路已全面補庫存（原話："Still not calling a restock though."）
- 2026-08-06｜CEO Jennifer Parmentier｜risk：農業與汽車需求仍疲弱（原話："remain where it's been pretty soft and automotive pretty"）
- 2026-08-06｜CFO Todd Leombruno｜risk：下半年比較基期變高，工業有機成長百分比較集中於第一季（原話："the comps in the second half get a little bit tougher."）
- 2026-08-06｜CEO Jennifer Parmentier｜product：資料中心占營收約 1.5%，先前說法為 1%（原話："It's about 1.5% of our sales, and we've been previously"）
- 2026-08-06｜CEO Jennifer Parmentier｜customer：電子業國際訂單強於預期，並預期持續強勁（原話："I think it's going to remain strong. I mean, obviously, it"）
- 2026-08-06｜CEO Jennifer Parmentier｜product：FY27 航太指引假設 OE 占比提高至 52%（原話："So we're planning on higher OE mix here."）
- 2026-08-06｜CEO Jennifer Parmentier｜guidance：油氣預期持平，發電成長更強（原話："Oil and gas, we think it's going to be flat."）
- 2026-08-06｜CFO Todd Leombruno｜capital_allocation：FY26 回饋股東：10 億美元回購加近 10 億美元股利（原話："That is $1 billion in share repurchases and nearly $1"）
- 2026-08-06｜CEO Jennifer Parmentier｜capital_allocation：兩筆收購預計日曆年下半年完成，無重大障礙（原話："We still anticipate closing both of them during the second"）
- 2026-08-06｜CEO Jennifer Parmentier｜capital_allocation：槓桿可能升至約 3 倍，約需 6 季回到 2 倍（原話："It will take us about 6 quarters to get that back down to 2."）
- 2026-08-06｜CEO Jennifer Parmentier｜capital_allocation：CIRCOR 未模擬營收綜效（原話："We have not modeled any revenue synergies."）
- 2026-08-06｜CEO Jennifer Parmentier｜capital_allocation：資本支出不預期超出現有指引（原話："but we're not expecting anything more than we've guided to"）
- 2026-08-06｜CEO Jennifer Parmentier｜commitment：管理層確認將有 Win 4.0，並討論下次投資人日（原話："So there will be a Win 4.0. Definitely, there will be."）
- 2026-08-06｜CFO Todd Leombruno｜customer：管理層否認第四季訂單有拉貨（原話："No. We never really experienced that."）

### PH_Hannifin_Corporation_Shareholder_Analyst_Call_Parker_Hannifin_Corporation_20261028.md
- 2026-10-28｜CEO Jennifer Parmentier｜margin：FY26 營收首度超過 200 億美元，並提前三年超越 FY29 調整後部門營業利益率目標（原話："segment operating margin target 3 years ahead of schedule"）
- 2026-10-28｜CEO Jennifer Parmentier｜margin：FY26 營收首次突破 200 億美元（原話："we also exceeded $20 billion in sales for the first time"）
- 2026-10-28｜CEO Jennifer Parmentier｜product：收購 Curtis Instruments 強化電氣化能力（2025 年 9 月）（原話："acquisition of Curtis Instruments in September 2025"）
- 2026-10-28｜CEO Jennifer Parmentier｜capital_allocation：2026 年 5 月宣布收購 CIRCOR 商用與國防航空業務（待完成）（原話："pending acquisition of CIRCOR's Commercial and Defense"）
- 2026-10-28｜CEO Jennifer Parmentier｜capital_allocation：2026 年 8 月宣布收購 Filtration Group，擴大專有過濾技術（原話："in August 2026, Filtration Group Corporation"）
- 2026-10-28｜CEO Jennifer Parmentier｜guidance：管理層表示 FY27 第一季業績將於 11 月 5 日財報電話會議更新，本場未給數字（原話："our fiscal year '27 first quarter performance"）
- 2026-10-28｜CEO Jennifer Parmentier｜commitment：管理層對延續動能表達信心，未給量化目標（原話："confident in Parker's ability to build on this momentum"）
- 2026-10-28｜CEO Jennifer Parmentier｜risk：管理層稱將在各種條件下專注執行（原話："executing through whatever conditions lie ahead"）
- 2026-10-28｜CEO Jennifer Parmentier｜product：將 FY26 成果歸因於 Win Strategy、投資組合轉型、分權營運與連網技術（原話："disciplined execution of The Win Strategy"）
- 2026-10-28｜CEO Jennifer Parmentier｜customer：提及與客戶的深度關係為 FY26 成果來源之一（原話："connected technologies and deep customer relationships"）

### 問答異常語氣（迴避／改口／保留）
- PH_Q4_2026_Earnings_Call_20260806.md｜問：Nicole DeBlase 問訂單在季內的進展及 7 月是否持續強勁｜答法：未給 7 月訂單數字或趨勢，只說沒有任何事情令其擔憂到不支持指引
- PH_Q4_2026_Earnings_Call_20260806.md｜問：Jeff Sprague 問滾動 12 個月訂單出口 9–10% 與工業成長指引 4–7% 之間的落差｜答法：未解釋落差大小，改說訂單是領先指標但不是精確預測，並提 10% 航太國防占比
- PH_Q4_2026_Earnings_Call_20260806.md｜問：Nathan Jones 問指引是否假設國際與北美訂單強勢持續或趨緩｜答法：未直接回答假設方向，只說指引反映目前訂單進展，並希望隨年度推進能上調

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
{"date":"20260518","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Aerospace supercycle 至 2030s：Boeing 737 + Airbus A320 雙寡頭增產 + 老化機隊 retrofit + Meggitt aftermarket monopoly → PH Aerospace 業務 2025-2030 CAGR &gt; 10%","columns":{"2Y 驗證點":"Aerospace 有機 +12% (FY26 guide) 達成，backlog &gt; $9B","5Y 驗證點":"Aerospace 5Y CAGR ≥ 10%，aerospace 占比從 33% → 38%；OEM build rates A320 75/月 + 737 52/月 達成","10Y 驗證點":"Aero aftermarket revenue 占 aerospace 60%+；穩定 OEM 平台轉換週期（2030s 進入下一代 narrowbody R&D 階段）","驗證指標":"季度有機營收 + backlog QoQ","來源":"2Y: §6, 5Y: §8.A Runway, 10Y: §8.A + §9"}},{"id":"H2","text":"Win Strategy 3.0 持續 margin expansion：Adjusted Segment OI Margin 從 FY25 26.0% → FY28 28%+，提前達標 5Y 目標","columns":{"2Y 驗證點":"FY26 OI margin 27.2% guide 達成，Industrial NA &gt; 22%","5Y 驗證點":"FY28 整體 segment OI margin ≥ 28%，FCF margin ≥ 17%","10Y 驗證點":"OI margin 維持 28%+ 跨越 10Y 不退讓（even in industrial downturns）","驗證指標":"季度 segment OI margin + FCF/Revenue trend","來源":"2Y: §6, 5Y: §8 + §10, 10Y: §8.A' S 曲線"}},{"id":"H3","text":"Filtration Group 整合成功：$9.25B 收購 $220M cost synergy 兌現 + EBITDA margin 維持 23.5%+ + 12 個月內 EPS accretive","columns":{"2Y 驗證點":"2026 H2-2027 Q1 close；首 12 個月 synergy ≥ 50%","5Y 驗證點":"5Y 後 filtration 占比 8-12%；synergy 完全兌現 → group OI margin +50bps","10Y 驗證點":"Filtration 結構性轉變 PH 為 aftermarket-recurring 模式 (50%+)","驗證指標":"季度 segment reporting + Filtration 揭露","來源":"2Y: §6 + §12, 5Y: §8.B 成長品質, 10Y: §9"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"商用航太 OEM 增產延後 / Boeing 安全事件再起（如 737 MAX、787 quality issues）→ A320 / 737 production rate 跑不到 guidance","columns":{"對應假設":"H1","時間尺度":"中期（2-3 年）","監測指標":"Boeing 737 月產量、Airbus A320 月產量；Boeing safety incidents","警戒閾值":"737 月產量 &lt; 35/月 連 2 季；A320 月產量無法在 2027 達 70/月（當前路徑 55-60/月）"}},{"id":"R2","text":"美中關稅 / supply chain re-shoring 推高 Industrial 業務成本 → Industrial OI margin 收窄 -2pp","columns":{"對應假設":"H2","時間尺度":"短期（12 月內）","監測指標":"Tariff policy；PH 在中國 / 墨西哥工廠占比；Industrial gross margin","警戒閾值":"整體 GM 連 2 季 YoY -1pp；Industrial NA segment OI margin 跌破 22%"}},{"id":"R3","text":"Filtration Group 收購 regulatory block 或 integration synergy 兌現 &lt; 50%","columns":{"對應假設":"H3","時間尺度":"中期（2-3 年）","監測指標":"FTC / 歐盟反壟斷進度；close timeline；首 12 個月 synergy disclosure","警戒閾值":"close 延後超過 2027 Q1；首年 synergy &lt; $100M（vs $220M target）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":33,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":33,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":862.72,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
