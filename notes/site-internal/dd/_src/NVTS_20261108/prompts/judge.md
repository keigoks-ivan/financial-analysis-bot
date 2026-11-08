你是 stock-analyst **v20 判斷 agent**，標的 NVTS（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"NVTS","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVTS_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVTS_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":14.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益","value":-10.9,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi2_non_gaap","label":"Non-GAAP 營業利益率","value":-78.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi3_gaap","label":"GAAP 營業利益","value":-34.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":-245.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi5_non_gaap","label":"Non-GAAP 毛利率","value":40.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi7_q4_2026","label":"管理層 Q4 2026 指引","value":"營收 16.0M ± 0.5M；Non-GAAP 毛利率 40.5% ± 100bps；Non-GAAP 營業費用 25.0M ± 1.0M（含 Claros）","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi8_backlog","label":"Backlog","value":"record，延伸至 2027 年中；新聞稿未給金額","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi9_book_to_bill","label":"Book-to-bill","value":"well above one（新聞稿未給數字）","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_kpi10","label":"期末現金","value":531.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_nvts_gross_margin_pct","label":"NVTS 毛利率","value":38.61,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVTS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nvts_operating_margin_pct","label":"NVTS 營業利益率","value":-272.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVTS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nvts_fcf_margin_pct","label":"NVTS FCF 利潤率","value":-189.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVTS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_powi_gross_margin_pct","label":"POWI 毛利率","value":53.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.POWI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_powi_operating_margin_pct","label":"POWI 營業利益率","value":7.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.POWI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_powi_fcf_margin_pct","label":"POWI FCF 利潤率","value":16.61,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.POWI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mpwr_gross_margin_pct","label":"MPWR 毛利率","value":55.26,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mpwr_operating_margin_pct","label":"MPWR 營業利益率","value":29.5,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mpwr_fcf_margin_pct","label":"MPWR FCF 利潤率","value":16.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_on_gross_margin_pct","label":"ON 毛利率","value":38.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_on_operating_margin_pct","label":"ON 營業利益率","value":19.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_on_fcf_margin_pct","label":"ON FCF 利潤率","value":25.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_wolf_gross_margin_pct","label":"WOLF 毛利率","value":-34.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WOLF.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wolf_operating_margin_pct","label":"WOLF 營業利益率","value":-74.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WOLF.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wolf_fcf_margin_pct","label":"WOLF FCF 利潤率","value":-46.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WOLF.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi6_sbc","label":"SBC 占營收","value":64.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":8.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-52.69,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":44.08,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-0.15 → -0.15）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-0.12 → -0.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-0.1 → -0.1）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-0.15,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":-0.12,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":-0.1,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS -0.15 → -0.15（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":57.42,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":44.43,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-524.88,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 6.6、現金 531.48（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":269.51,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1795.58,"period":"2026-11-08","unit":"USD m","basis":"市值 2320.46 ＋ 淨負債 -524.88","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":48.67,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（6 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":78.38,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（7 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":36.89,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 8.61 / W52 12.38 / W104 8.71 / W250 7.1 / W250 13週斜率 -0.99%"},{"id":"f_ma_w52","label":"52 週均線","value":12.38,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":8.71,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":7.1,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.99,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出主要 GaN 對手（Infineon、Power Integrations、TI、Innoscience、Renesas、EPC）與 SiC 對手（Infineon、Wolfspeed、onsemi、ROHM、Qorvo、ST）；多數對手財力遠大於公司。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"Our primary GaN competitors include Infineon Technologies AG, Power Integrations, Inc., Texas Instruments Incorporated, Innoscience (Suzhou) Semiconductor Co., Ltd., Renesas Electronics Corp., and Efficient Power Conversion Corporation (EPC). Our primary SiC competitors include Infineon, Wolfspeed, Inc., ON Semiconductor Corporation, ROHM Co., Ltd., Qorvo, Inc., and STMicroelectronics International N.V.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：可能出現新競爭者或傳統大廠推出 GaN／高壓 SiC 方案；設計一旦被採用，客戶通常要到下一代才換，失去設計案將損失份額。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"Unpredictable Competitive Dynamics: To the extent new and emerging products and technologies reshape or create new market landscapes, the competitive environment may evolve in unexpected ways. For example, new competitors may emerge, or traditional competitors with established R&D and manufacturing resources, and long-standing customer relationships, may choose to offer competitive GaN or high-voltage SiC solutions.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K：營收受份額得失與設計案進展影響，且行動／消費市場受競爭與定價壓力，與公司轉向高功率有關。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"gains and losses in market share and design win traction, including the Company’s ability to ramp new high-power products; •pace at which technology is adopted in our end markets; •the stage of our products in their respective life cycles; •the effects of competition and competitive pricing strategies, particularly in the mobile and consumer markets impacted by our announced transition to high-power markets","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"onsemi 2026-06 推出面向 AI 資料中心的 GaN 產品組合 GaNEXUS；ST 2026-05 推出 700V GaN 供 AI 伺服器，大廠加入 GaN 競爭。","source":"Nasdaq/Zacks: NVTS Shifts to 8-Inch GaN","url":"https://www.nasdaq.com/articles/nvts-shifts-8-inch-gan-will-it-help-return-growth-trajectory","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 10-K風險因子：end customer可能延遲、變更或取消產品計畫、更換供應商；失去design win或關鍵客戶會嚴重影響營收；美國出口管制可能促使客戶自行開發替代方案或轉向不受限的競爭對手。為一般性風險揭露，未點名特定客戶導入第二供應商或自製。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"the end customer may ultimately delay, change or cancel our product plans, change suppliers, or our end customers’ efforts to market and sell our product may not be successful.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K風險因子：美國法規與制裁可能促使end customers自行開發解決方案取代NVTS產品，或向不受限制的競爭對手取得替代品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"may also encourage end customers to develop their own solutions to replace 26 TABLE OF CONTENTS our products, or seek to obtain a greater supply of similar or substitute products from competitors that are not subject to these restrictions","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Q3 2026 10-Q顯示客戶集中於經銷商，Distributor C占營收29%（Q1 2026 10-Q為Distributor A 59%）；經銷商背後的終端客戶未點名。本次搜尋未找到2026年任何最大客戶導入第二供應商或自製的公開來源。","source":"SEC EDGAR 10-Q 2026-09-30（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069551/nvts-20260930.htm","excerpt":"Distributor C 1,692 | 29%","as_of":"2026-09-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：2025 年無單一經銷商占比揭露於 Distributor A 欄（*），Distributor B 占營收 46%、Distributor C 占 11%（2024 年 Distributor A 占 56%）；Distributor A 經銷協議於 2024 年底終止，2024 年認列 750 萬美元呆帳費用；2025 年底應收帳款 Distributor A1 44%（2024）、B 26%、C 18%、D 13%、E 12%（欄位對應依表格原文）。","source":"SEC EDGAR 10-K FY2025 Item 8 Note 12","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"Customer 2025 2024 Distributor A * 56 % Distributor B 46 % * Distributor C 11 % * At the end of 2024, the Company terminated its distribution agreement with Distributor A. As a result of this termination, the Company incurred a bad debt expense of $7.5 million included in Selling, general, and administrative expenses for the year ended December 31, 2024.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026 Q3 10-Q：經銷商客戶集中度與應收帳款集中度（Distributor A 應收 33%、Distributor C 29%）","source":"SEC EDGAR 10-Q Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069551/nvts-20260930.htm","excerpt":"The following customers represented 10% or more of the Company’s accounts receivable (in thousands). Customer September 30, 2026 December 31, 2025 Distributor A $ 1,875 33 % $ 860 26 % Distributor C","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Wolfe Research 分析師 Chris Caso 認為半導體供過於求最早要到 2028 年，因新廠需數年興建；SEMI 預估設備支出 2026 年 1450 億美元、2027 年 1560 億美元。","source":"247wallst: Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce：AI 需求使 3nm 與 CoWoS 產能到 2027 年仍吃緊；NAND 供給短缺預期 2027 下半年緩解（週期性成分）。這些是 AI 先進邏輯與記憶體，非 NVTS 所處的功率半導體市場。","source":"pulse.bot / TrendForce: AI Demand Keeps 3nm and CoWoS Capacity Tight Through 2027","url":"https://www.pulse.bot/semiconductors/news/ai-demand-keeps-3nm-and-cowos-capacity-tight-through-2027-e5620591-33aa-4cad-824a-f7944c516c7a/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"WSTS 2026 春季預測：全球半導體市場 2027 年再成長 27%、約 1.9 兆美元；SEMI 預估先進製程產能到 2028 年成長 69%；BofA 預期 2027 訂單簿近乎滿載、2028 仍偏緊；Deloitte 警告 2027–2028 可能與預期大幅分歧。","source":"WSTS / SEMI / Bank of America / Deloitte（經 WebSearch 彙整）","url":"https://iconnect007.com/article/145906/semi-forecasts-69-growth-in-advanced-chipmaking-capacity-through-2028-due-to-ai/145903/ein","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"NVTS：Q1 2026 營收季增 18% 至 860 萬美元，主因高功率需求；公司指引 2026 年續季增；Zacks 評論稱 AI 資料中心的實質營收預期在 2027 年，2026 為轉型年；其 GaN/高壓 SiC 與 NVIDIA 800V 架構相關；一篇獨立分析稱供給並非限制，其他 GaN 廠可擴產（意見文）。","source":"Can AI Infrastructure Demand Accelerate NVTS' Long-Term Growth? (Chartmill/Zacks)","url":"https://www.chartmill.com/news/external/85350/can-ai-infrastructure-demand-accelerate-nvts-long-term-growth","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261108","affects":["thesis.H","thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce：Micron 看記憶體供給到 FY28 仍緊，Samsung/SK hynix 新產能 2028 年後才到；SK hynix CEO 稱短缺可能持續到 2030。","source":"TrendForce News","url":"https://www.trendforce.com/news/?p=64868","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：公司認為其 GaN/SiC 產品一般不受美國 EAR 管制，但受出口法規限制，進一步行動可能對含特定技術產品（含售予中國終端客戶）增加限制。","source":"SEC EDGAR 10-K FY2025 風險因子","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"our company to additional regulatory restrictions or scrutiny, including by CFIUS, in connection with past or future transactions that involve investments in us or by us. Although we believe all of our GaN and SiC products are generally not subject to export controls under the U.S. Export Administration Regulations, CFIUS could choose to review proposed or past investments in us by foreign","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：公司明列受美國出口管制與制裁法規約束，可能限制對中國終端客戶的產品出口；美中關稅或貿易戰可能對財務與營運結果造成重大不利影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"These actions could lead to additional restrictions on the export of products that include or enable certain technologies, including products we provide to China-based end customers. The institution of trade tariffs both globally and between the U.S. and China specifically could materially and adversely affect our business, financial condition and results of operations.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 指出美國法規已將化合物半導體與寬能隙半導體（GaN、SiC）歸類為「對國家安全關鍵」，涉及 CFIUS 審查與出口許可風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"U.S. regulatory initiatives over the past several years have classified certain semiconductor technologies as “critical to national security,” including compound semiconductors and wide bandgap semiconductors. Both GaN and SiC are compound semiconductors and wide bandgap semiconductors.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 指出出口限制可能促使終端客戶自研替代方案或轉向不受限制的競爭對手。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"may also encourage end customers to develop their own solutions to replace 26 TABLE OF CONTENTS our products, or seek to obtain a greater supply of similar or substitute products from competitors that are not subject to these restrictions","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 Q1 10-Q：中國報復性關稅或非關稅壁壘可能在未來 12–18 個月侵蝕 SiC 產品定價競爭力，因目前依賴單一美國來源。","source":"SEC EDGAR 10-Q Q1 2025","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176925000068/nvts-20250331.htm","excerpt":null,"as_of":"2025-05-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K：Navitas 營運據點含美、愛爾蘭、中國、台灣、德國、南韓、菲律賓；絕大多數產品由美國境外第三方製造、組裝、測試與封裝。","source":"Navitas Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：部分前段製造依賴單一來源，無晶圓代工長期供貨合約。","source":"Navitas Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2022 10-K：GaN 晶圓代工廠位於台灣，大量第三方分包商與供應商在台灣；FY2024 10-K 為 GaN 單一代工廠、SiC 另一單一代工廠。","source":"Navitas Form 10-K FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176925000021/nvts-20241231.htm","excerpt":null,"as_of":"2025-03-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"二手來源稱 TSMC 宣布 2027 年 7 月停止 GaN 生產，Navitas 轉往 Powerchip(台灣)與 GlobalFoundries(佛蒙特，預計 2026 年底投產)；細節來自第三方，未經 10-K 核實。","source":"Panabee / briefglance 摘要（搜尋摘要轉述）","url":"https://www.panabee.com/idea/is-navitas-semiconductor-nvts-a-buy-03112026","excerpt":null,"as_of":"2026-03-11","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收約 $14M，季增 33%、年增 38%，由高功率市場帶動；Q4 指引中位 $16.0M，AI 基礎設施占比預計 >40%、mobile <5%；管理層預期 2027 AI 基礎設施營收約 3 倍，2030 可服務市場 >$8B","source":"24/7 Wall St. Navitas Semiconductor Q3 2026: AI Data Center Pivot Takes Hold（搜尋摘要，引 SEC 8-K）","url":"https://247wallst.com/cards/navitas-semiconductor-q3-2026-earnings-nvts-01m6hm399mnvq0rwktwa20sb3q","excerpt":"Total revenue grew 33% sequentially and 38% year-over-year, driven by high-power markets","as_of":"2026-11-03","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"mobile 營收占比預期於 2026 年底趨近「insignificant」；消費型 GaN 充電器被認為加速商品化，Q3 2025 提及中國 mobile 價格壓力","source":"搜尋摘要彙整（Q1 2026 財報摘要、Q3 2025 業績）","url":"https://www.marketbeat.com/earnings/reports/2026-5-4-navitas-semiconductor-corp-stock/","excerpt":null,"as_of":"2026-05-04","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Yole 預期 GaN 於 800V HVDC 首批商用約 2027 年，NVIDIA Kyber 機櫃預計 2027；2026 GaN 功率元件市場約 USD 0.8–1.3B（各家口徑差異大）","source":"Meticulous Research Next Brief: GaN Power Devices Outlook 2026-2034（搜尋摘要）","url":"https://www.meticulousresearch.com/meticulous-next/gan-power-devices-outlook-2026-2034","excerpt":"The GaN power devices market... is valued at USD 0.8–1.3 billion","as_of":"2026-07-01","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：新產品、新或替代技術的市場接受度或新產業標準，可能使公司現有或未來產品失去競爭力、過時；高功率市場下尤其明顯。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"The introduction of new products by our competitors, the delay or cancellation of any of our end customers’ product offerings for which our solutions are designed, the market acceptance of products based on new or alternative technologies, or the emergence of new industry standards could render our existing or future products uncompetitive, obsolete, and otherwise unmarketable.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K：美國出口限制與制裁可能促使終端客戶自行開發方案取代公司產品，或轉向不受限制的競爭對手之類似／替代品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"may also encourage end customers to develop their own solutions to replace 26 TABLE OF CONTENTS our products, or seek to obtain a greater supply of similar or substitute products from competitors that are not subject to these restrictions","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K：TSMC 宣布 2027 年 7 月停止 GaN 生產，公司改與力積電及 GlobalFoundries 合作；新替代代工的驗證與量產有延遲風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"On July 1, 2025, TSMC announced its intention to cease GaN production in July 2027.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 稱與精選全球經銷夥伴合作提供額外現場工程資源，直銷團隊在焦點市場建立新策略關係（精簡後的通路策略）。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000007/nvts-20251231.htm","excerpt":"We collaborate with select global distribution partners for additional field engineering resources, while our direct sales team builds new strategic relationships in our focus markets.","as_of":"2026-02-27","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Navitas 2.0 轉型：退出行動與低階消費市場，轉向 AI 資料中心與電網高功率；搜尋摘要稱 2026 為過渡年，營收在轉型期下滑（二手評論）。","source":"Zacks/MetaTrader 新聞：Can NVTS' Pivot to High-Power AI Markets Fuel Long-Term Growth?","url":"https://www.metatrader.com/en/news/1159671-can-nvts-pivot-to-high-power-ai-markets-fuel-long-term-growth","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Navitas 整併亞洲通路，與 WT Microelectronics 簽策略經銷合作，以對齊高功率成長市場。","source":"Navitas Consolidates Asian Distribution, Signs Strategic Distribution Partnership with WT (GlobeNewswire)","url":"https://www.itiger.com/news/2586648227","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Avnet 成為 Navitas 全球特許策略經銷夥伴，屬經銷夥伴整併一環。","source":"Navitas Expands Global Distribution Network with Avnet","url":"https://www.itiger.com/hans/news/2590541596","excerpt":"gallium nitride (GaN) and GeneSiC™ silicon carbide (SiC), today announced an expansion of its distribution agreement with Avnet (Nasdaq: AVT), making Avnet a globally franchised strategic distribution partner for Navitas. The deal is part of the ongoing consolidation of Navitas’ franchised distribution partners and represents a significant expansion of the company’s channel presence with","as_of":"2025-12-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 彙整：8 位分析師共識 Hold（2 賣、4 持有、2 買），平均目標價約 $14.74，最高 $21.00、最低 $6.00（頁面無明確發布日，as_of 為估計）","source":"MarketBeat NVTS price-target page","url":"https://www.marketbeat.com/stocks/NASDAQ/NVTS/price-target/","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com 12 個月平均目標價約 $14.08；Morgan Stanley Sell 評級目標價 $13.70（2026-07-28）","source":"Investing.com NVTS","url":"https://uk.investing.com/equities/live-oak-acq","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-11-03 公司公布 Q3：營收 $13.991M（+38% YoY）；Q4 guidance 中位 $16.0M±$0.5M，高於 Q4 賣方共識約 $15.1M（Benzinga）","source":"Navitas 8-K Ex.99.1 (Q3 2026 earnings)","url":"https://www.sec.gov/Archives/edgar/data/0001821769/000162828026069489/exhibit991-navitassemicond.htm","excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-24 Navitas 簽署與 Claros, Inc. 的合併協議（兩段式合併，Claros 併入 Merger Sub 2）；搜尋摘要稱作價約 2.33 億美元，10 月完成。","source":"SEC EDGAR 8-K Item 1.01（2026-08-25）","url":"https://www.sec.gov/Archives/edgar/data/1821769/000110465926100478/tm2623854d1_8k.htm","excerpt":"On August 24, 2026, Navitas Semiconductor Corporation (“Navitas” or the “Company”) entered into an Agreement and Plan of Merger (the “Merger Agreement”), by and among the Company, Claros, Inc., a Delaware corporation (“Claros”)","as_of":"2026-08-25","retrieved_at":"20261108","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-09 Navitas 以 500 萬美元認購 Magnachip 1,461,988 股普通股（每股 3.42 美元）。","source":"SEC EDGAR 8-K Item 1.01（2026-09-21）","url":"https://www.sec.gov/Archives/edgar/data/1821769/000110465926109227/tm2625807d2_8ka.htm","excerpt":"Navitas Semiconductor Corporation (the “Company”) entered into a Stock Purchase Agreement (the “Purchase Agreement”) with Magnachip Semiconductor Corporation (“Magnachip”), pursuant to which Magnachip agreed to issue and sell to the Company 1,461,988 shares","as_of":"2026-09-21","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2026-07 Wolfspeed 在德拉瓦聯邦地院對 Navitas 提起專利侵權訴訟，Navitas 稱指控無理由（搜尋摘要）。","source":"Barchart / Webull 報導","url":"https://www.barchart.com/story/news/3244113/navitas-semiconductor-stock-is-on-the-ropes-it-faces-a-new-patent-infringement-lawsuit","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"unprofitable_nrr_rule40_band#0","axis":"unprofitable_nrr_rule40_band","section":"coverage","direction":"-","claim":"multiples.vc 列示 NVTS Rule of 40 分數約 -129%（LTM 營收成長約 -7%、EBITDA 率約 -65%）","source":"multiples.vc Navitas Semiconductor valuation multiples","url":"https://multiples.vc/public-comps/navitas-semiconductor-valuation-multiples","excerpt":"Navitas Semiconductor's Rule of 40 is (75%) (metric relevant for SaaS companies only, counted as combined revenue growth rate and EBITDA margin).","as_of":"2025-10-26","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_nrr_rule40_band#1","axis":"unprofitable_nrr_rule40_band","section":"coverage","direction":"-","claim":"Trefis 同業比較（QCOM、FSLR、SLAB、POWI）：NVTS 營業利益率 -181.4% 為最低、近 12 個月營收成長 -38.1% 落後","source":"Trefis How Does Navitas Semiconductor Stock Compare With Peers?","url":"https://www.trefis.com/stock/nvts/articles/582366/how-does-navitas-semiconductor-stock-compare-with-peers/2025-11-11","excerpt":"NVTS’s operating margin of -181.4% is negative, lowest among peers; FSLR has 31.3%. NVTS’s revenue growth of -38.1% in the last 12 months is negative, lagging QCOM, FSLR, SLAB, POWI.","as_of":"2025-11-11","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#0","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"StockAnalysis 列 NVTS 流通股 230.79M，一年增 17.17%、QoQ +3.44%（資料未標日期）","source":"StockAnalysis - Navitas Semiconductor Statistics","url":"https://stockanalysis.com/stocks/nvts/statistics/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#1","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"2026-06-04 8-K：發行 3,283,844 股 Class A，主要用於 2021 年 5 月合併協議 Triggering Event II 的 earnout；原股東仍可再領至多 1,000 萬股","source":"quiverquant / stockti 新聞摘要（引 8-K）","url":"https://stockti.com/navitas-stock-rally-faces-dilution-threat-as-spac-earnout-shares-vest","excerpt":null,"as_of":"2026-06-04","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#2","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"2026-05-11 簽訂 ATM 銷售協議，可分次賣最多 1.25 億美元 Class A 股（來源間金額不一，TIKR 稱 5 億美元，待核 SEC 文件）","source":"Quiver Quant / TIKR 報導","url":"https://www.quiverquant.com/news/Navitas+Semiconductor+Slides+as+Dilution+Overhang+and+Chip-Sector+Weakness+Pressure+Shares","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#3","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"Trefis 列 SBC/營收 LTM 約 44%；Business Quant 列 2026Q2 SBC 8.4M、TTM 27.1M；Digrin 列 2026-06-30 SBC 18.7M，聚合站數字互相矛盾，須以 10-Q 為準","source":"Trefis / Business Quant / Digrin","url":"https://businessquant.com/metrics/nvts/share-based-compensation","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#4","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"稀釋後股數長期上升：約 39M → 206M（頁面 2026-03），年增 12.67%／8.01%／15.91%；AlphaQuery 2025Q3 加權稀釋股數 212.68M","source":"AlphaQuery weighted average shares outstanding diluted","url":"https://www.alphaquery.com/stock/NVTS/fundamentals/quarterly/weighted-average-shares-outstanding-diluted","excerpt":null,"as_of":"2025-09-30","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#5","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"0","claim":"Q1 2026 財報 8-K 含 SBC 調節項，可核 SBC 金額","source":"SEC 8-K Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/1821769/000182176926000003/exhibit991-navitassemicond.htm","excerpt":"RECONCILIATION OF NET LOSS PER SHARE GAAP Net loss $ (31,815) $ (39,860) $ (116,953) $ (84,599) Adjustments to GAAP Net loss Restructuring and impairment expense 16,580 1,223 18,049 1,223 Loss (Gain) from change in fair value of earnout liabilities (8,271) 6,276 12,424 (36,644) Total stock-based compensation 7,958 5,020 14,484 43,031","as_of":"2026-05-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_path_to_profitability#0","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"0","claim":"公司表示季營收高 30 百萬美元級可在目前毛利率與費用結構下支撐營運獲利；FY2025/2026 仍無 FCF 為正年度","source":"Zacks/Nasdaq: Is Navitas Finally Building a Path Toward Operating Breakeven?","url":"https://www.nasdaq.com/articles/navitas-finally-building-path-toward-operating-breakeven","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"unprofitable_path_to_profitability#1","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"-","claim":"Q3 後損益兩平門檻上移，Q3 營收13.99M、Q4指引16.0M，Claros 支出使損益兩平更遠","source":"Finviz/Earnings Whispers: Navitas matches the whisper... breakeven further out","url":"https://finviz.com/news/415056/navitas-matches-the-whisper-as-ai-driven-revenue-accelerates-but-claros-spending-pushes-breakeven-further-out","excerpt":"**Breakeven.** The implied breakeven moved from quarterly revenue in the \"high 30s\" (millions) to the \"low 60s,\" roughly four times the fourth-quarter guide.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_path_to_profitability#2","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"0","claim":"2025 年底現金與投資 236.9M、2025 營運現金流 -42.9M","source":"AlphaStreet: NVTS Q4 2025 earnings flash","url":"https://news.alphastreet.com/blog/2026/03/11/nvts-q4-2025-earnings-flash","excerpt":null,"as_of":"2026-03-11","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-08-24 簽署收購 Claros 合併協議（約 2.33 億美元，10 月完成，搜尋摘要）。","source":"SEC EDGAR 8-K Item 1.01（2026-08-25）","url":"https://www.sec.gov/Archives/edgar/data/1821769/000110465926100478/tm2623854d1_8k.htm","excerpt":"On August 24, 2026, Navitas Semiconductor Corporation (“Navitas” or the “Company”) entered into an Agreement and Plan of Merger (the “Merger Agreement”), by and among the Company, Claros, Inc., a Delaware corporation (“Claros”)","as_of":"2026-08-25","retrieved_at":"20261108","affects":["valuation","moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-07 Wolfspeed 專利侵權訴訟（德拉瓦）；搜尋未見證券集體訴訟。","source":"Barchart 報導","url":"https://www.barchart.com/story/news/3244113/navitas-semiconductor-stock-is-on-the-ropes-it-faces-a-new-patent-infringement-lawsuit","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"NVTS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.61,"operating_margin_pct":-272.56,"fcf_margin_pct":-189.08,"rd_intensity_pct":136.57},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVTS","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"POWI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.32,"operating_margin_pct":7.67,"fcf_margin_pct":16.61,"rd_intensity_pct":23.53},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.POWI","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MPWR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.26,"operating_margin_pct":29.5,"fcf_margin_pct":16.29,"rd_intensity_pct":12.18},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MPWR","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ON","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.68,"operating_margin_pct":19.12,"fcf_margin_pct":25.38,"rd_intensity_pct":8.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"WOLF","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":-34.9,"operating_margin_pct":-74.77,"fcf_margin_pct":-46.38,"rd_intensity_pct":16.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WOLF","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"NVTS"},"financial_history":{"ticker":"NVTS","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":37943000.0,"revenue_yoy_pct":null,"gross_margin_pct":31.49,"operating_margin_pct":-325.85,"net_income":73913000.0,"diluted_eps":0.51,"free_cash_flow":-49141000.0,"fcf_margin_pct":-129.51,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":79456000.0,"revenue_yoy_pct":109.41,"gross_margin_pct":39.1,"operating_margin_pct":-148.68,"net_income":-145433000.0,"diluted_eps":-0.86,"free_cash_flow":-46161000.0,"fcf_margin_pct":-58.1,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":83302000.0,"revenue_yoy_pct":4.84,"gross_margin_pct":34.02,"operating_margin_pct":-155.4,"net_income":-84599000.0,"diluted_eps":-0.46,"free_cash_flow":-65594000.0,"fcf_margin_pct":-78.74,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":45916000.0,"revenue_yoy_pct":-44.88,"gross_margin_pct":31.03,"operating_margin_pct":-195.39,"net_income":-116953000.0,"diluted_eps":-0.57,"free_cash_flow":-44369000.0,"fcf_margin_pct":-96.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/NVTS/NVTS_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Navitas Semiconductor Corporation** | Earnings Calls | 2026-11-03

**Operator** (Operator):
Good afternoon, and welcome to Navitas Semiconductor's Third Quarter 2026 Financial Results Conference Call. [Operator Instructions] As a reminder, this conference call is being recorded today, Tuesday, November 3, 2026.
I would now like to turn the call over to Brett Perry of Shelton Group Investor Relations. Brett, please go ahead.

**Brett Perry** (Attendees):
Thank you, and good afternoon. Welcome to Navitas Semiconductor's Third Quarter 2026 Financial Results Conference Call. Joining us today are Navitas President and CEO, Chris Allexandre; and CFO, Tanya Stevens. 
I'd like to remind listeners that management's prepared remarks contain forward-looking statements, which are subject to risks and uncertainties, and management may make additional forward-looking statements in response to your questions. Therefore, the company claims the protection of the safe harbor for forward-looking statements that's contained in the Private Securities Litigation Reform Act of 1995. 
Additional results may differ from those discussed today, and therefore, we refer you to a more detailed discussion of the risks and uncertainties in the company's filings with the Securities and Exchange Commission, including the company's filings on Forms 10-K and 10-Q. 
In addition, any projections as to the company's future performance represent management's estimates as of today, November 3, 2026. Navitas assumes no obligation to update these projections in the future as market conditions may or may not change, except to the extent required by applicable law. 
Additionally, the company's press release and management statements during this conference call will include discussions of certain measures and financial information in GAAP and non-GAAP terms. Included in the company's press release are definitions and reconciliations of GAAP to non-GAAP items, which provide additional details. 
For those of you unable to listen to the entire call at this time, a recording will be available via webcast for 90 days in the Investor Relations section of Navitas' website at www.navitasseemi.com. 
And now it's my pleasure to turn the call over to Navitas President and CEO. Chris, please go ahead.

**Chris Allexandre** (Executives):
Good afternoon, and thank you for joining us on today's third quarter 2026 earnings call. We appreciate your continued interest and support as we near completion of our strategic transformation and begin executing as Navitas 2.0. 
Our third quarter results reflect another period of solid financial performance and accelerated momentum. Total revenue was on the high end of guidance at $14 million, up 33% sequentially and 38% year-over-year, marking the company's first quarter of year-over-year growth since 2024. This revenue growth was driven by high-power markets, which increased more than 50% sequentially and grew by triple digits year-over-year. 
As anticipated, mobile and low-end consumer continued to decline as a percentage of revenue and remains on path to becoming insignificant in the fourth quarter. By year-end, high-power will essentially represent the entire company, and we will have substantially exceeded mobile and low-end consumer markets. 
In fact, as we now delivered multiple quarters of double-digit sequential revenue growth and gross margin expansion, driven by high-power market and an acceleration in AI infrastructure, our core focus. Gross margin expanded sequentially and was above the midpoint of guidance, reflecting the continued benefits of favorable revenue mix and increasing scale. 
Notably, third quarter non-GAAP gross margin of 40% was 130 basis points higher than the third quarter of 2025 when we began the Navitas 2.0 journey. Book-to-bill remains well above 1 and has been for the last several months, and we currently have solid backlog extending into mid-2027. 
We also expect continued revenue growth and margin expansion in the fourth quarter, which will represent the fourth consecutive quarter of double-digit sequential revenue growth and margin increase with the company exceeding 2026 as a high per company. Briefly stepping back, roughly a year ago, we made a deliberate decision to pivot away from mobile and low-end consumer and focus our resources on the high-power market where GaN, high-voltage SiC and ultrahigh-voltage SiC provide greater differentiation and stronger long-term growth. 
We labeled AI data center, energy and grid infrastructure, high-performance computing and industrial electrification high-power market as clear focus and AI infrastructure as North Star. The success of this pivot is now clearly visible in our revenue mix. At the beginning of 2026, Navitas 2.0 was only a strategy, and now it is ready. 
By the fourth quarter, we expect mobile revenue to be effectively gone, as stated earlier, and the company revenue to be essentially all high power. More than offsetting our exit from lower-margin mobile and low-end consumer has been the tremendous growth of AI infrastructure, our North Star. AI data centers plus the grid and energy infrastructure required to power them. We anticipate AI infrastructure to represent more than 40% of our total revenue exiting this year, and we believe this business is poised to triple in the calendar 2027. 
Over the last few months, it has become clear and broadly accepted that power is now the #1 constraint on AI compute. The question is no longer only how many GPUs or XPUs can be manufactured and deployed, but how many can realistically be powered. In other words, power efficiency is becoming capacity. When access to power is constrained, every watt saved in conversion and delivery can become another watt available for compute. It increases the scale of compute that can be deployed inside a given power envelope, not only the energy cost.
Together with our high and ultra-high voltage SiC, GaN and recently acquired Claros IVR technology stack serving both vertical and embedded power delivery architectures further positions us to break the AI infrastructure power wall by addressing the efficiency, power density and performance bottlenecks across the full power chains from grid to XPU. 
With our strategic acquisition of Claros in early October, Navitas has now a complete platform that is capable of addressing the final stage of delivering efficient power all the way to the XPU. I want to emphasize that there is a growing number of processor sites, CPU, GPU, TPU, XPU and other custom processors as well as companies developing them, each requiring a specific power implementation for the last step of power conversion to core voltage.
This requires a modular approach, which is one of the key differentiators of Claros IVR technology stack as it allows several IVR to be combined very flexibly in a power array to deliver the required power level and density. Navitas was already unique by having both GaN and SiC. And now with Claros, we are even more so. 
We are now an enabler of efficient power delivery from the source of energy, starting in a modernized grid with our ultra-high-voltage SiC, then high-density and high-efficiency centralized AC-DC and DC-DC conversion with our high-voltage SiC and GaN. And finally, the power delivery to the XPU with the Claros IVR technology stack. 
Going one step deeper, IVR technology solves a real-world scaling problem. Processor power demands are increasing faster than lateral delivery can support with package power moving from roughly the mid-1 kilowatt range towards several kilowatts at sub-1 volt core and several thousand ramp.
By moving conversion closer to the XPU with vertical power delivery directly beneath the processor and embedded power delivery ultimately in the PCB package or substrate, the path is shortened from centimeters towards millimeters or even less. This reduced resistance, inductance, drop and heat. 
As an integrated IVR platform, not another power FET, we are combining digital control, power transistors, high-density capacitors, embedded inductors and packaging in one architecture. The platform is also designed to scale with processor currently through a repeatable building block of the order of 40 amp through larger chips and a modular power array into multiple kilo amp system packaged and embedded. 
In simple terms, the Cloud IVR technology stack with its ability to serve both future VPD and EPD architectures give us a complete power solution platform. Together with the addition of GFS, it doubles our 2030 SAM to over $8 billion and represent a multiyear content growth opportunity that layers on top of the existing inflection points we are pursuing with our high-voltage SiC and GaN. 
The ultimate benefit is Navitas's ability to help customers convert more of every available megawatt into useful AI compute. While our transformation to a high-power company is effectively complete, our go-forward strategy remains grounded in multiple key pillars of transformation that we have discussed over the last 12 months, market focus, technology leadership, operational efficiency and financial discipline. 
On market focus and technology leadership, we continue to advance a series of customer and technology proof points. Since our previous conference call, we announced our collaboration with NVIDIA on an 800-volt to 12-volt power delivery board for next-generation AI infrastructure. This builds on our previously announced 800-volt 6 and 800-volt 250-volt DC-DC conversion board, further highlighting the breadth of our system knowledge and capability. 
We also licensed GeneSiC technology to Microchip, underscoring the strength of our trench assisted planner process foundation and supporting expanded SiC adoption, particularly in Asia, while also creating long-term potential for additional foundry source. We recently partnered with Microchip to deliver an 800-volt reference design for next-generation AI data center. 
Then in late September, Navitas was selected by the U.S. government to develop next-generation 10 kV SiC power semiconductor, reinforces both technology superiority and domestic supply chain resilience. And we also announced the first shipments of our U.S. manufactured fifth-generation GaNFast technology as part of our long-term strategic partnership with GlobalFoundries. 
Following shipments of the first wafers in September for the initial product family, including 650-volt GaNFast, we expect to have strategic customers sample very soon. On a related note, we previously talked about pursuing a Foundry plus model. Going forward, we've renamed and we refer to the strategic operating model as Integrated Fabless Manufacturing or ISM, a deliberate alternative to the traditional IDM approach.
The core difference and principles are that we choose what to own, where to invest and who to partner with, allowing us to retain the capabilities that differentiate product while leveraging partners for manufacturing at scale. Importantly, we remain ownership of critical technology IP, selected manufacturing equipment together with targeted co-investment, not purely supplier collaboration. 
For purpose of today's call, I want to briefly take this opportunity to clearly define and lay the foundation of our IFM model as I expect it to play a strategic role in our go-forward strategy. Looking more near term, I will also note that we are actively taking advantage of our strengthened balance sheet to strategically build inventory buffers, including raw materials and secure future capacity to support unexpected strong and consistent mid- to long-term growth. 
Turning to an update in our progress towards the four inflection points that I introduced in our last conference call, which I intend to keep using to map our growth to architecture change in AI infrastructure. Today, the transition to 800-volt architecture for next-generation AI data center is now certain. The debate is no longer whenever 800 volt is happening, but instead how it will unfold. 
As previously outlined, the transition will have a series of inflection points that will drive increasing momentum and growing need for higher power solutions. Navitas's unique combination of high-power GaN, high-voltage SiC and our IVR capabilities will allow us to capitalize on each of these inflections. I want to emphasize that we are not dependent on one architectural transition and that we are not waiting for the final data center architecture to emerge.
These inflection points represent successive opportunities, each of which can increase content per system as the overall market continue to grow and expand. The first inflection, pre-800 volt, is already well underway. We are seeing an acceleration of silicon replacement for any ACDC above a few kilowatt. Products based on our SiC technology addressing this opportunity are in production and driving accelerated growth in the fourth quarter and the first half of 2027 across multiple hyperscalers and OEM ODM. 
We are seeing an acceleration of demand, in particular for 1.2 kV SiC, where our previously mentioned Gen 5 is gaining strong traction. The second inflection, the SiC AR rack and the first rollout of plus or minus 400-volt and/or 800 volt is also accelerating. We discussed this in our last earnings call, and it was clear at the OCP Summit in October that this is coming and now definitely coming in 2027. 
We are seeing broader design conversion and program across more customers and applications, including AC-DC, DC-DC and battery backup units or BBU, all with more dollar content. Large orders already in place and slated to ramp in the first half of next year. This will drive growth in 2027 on top of the first inflection point continuing across AI data centers that not yet to adopt high-voltage DC. The power level and density acceleration of AC-DC PSUs is really stunning and driving this content jump. 
On the DC-DC side, the same is true. We are currently progressing through the final stage of designing and qualification with many customers and orders already in place, which will give us additional programs in support of continued growth over the coming year. What is very interesting about the second inflection point is the variety of applications in both, DC-DC, AC-DC, BBUs and others and the use of different technologies between SiC and GaN, which reinforce Navitas's strategic positioning.
The third inflection point or Nive 800 volt continues to progress. We all know by now, and it was reconfirmed again at OCP that this is the only path to achieving really high-density, high-power rack. I mean 500 kilowatt and plus and up to megawatt racks. We are advancing design and preparation for this high-density rack across multiple vendors depending on the XP. Everyone is looking at it. We continue to believe Native 800-volt solution will be in production before the end of 2027 and be material in 2028. 
Today, we are sampling and progressing with customers on more than a dozen programs and are currently in final stage with certain leading OEM ODM for 800-volt power DC-DC conversion board. One existing customer targeting hyperscalers has already placed a large order for significant system test, which reinforce Navitas's strong market position.
The fourth inflection point the complete modernization of energy and grid infrastructure, while further out, it is also moving forward, driven by the speed and energy requirement of AI data centers. We are continuing to work to secure initial design wins with our ultra-high-voltage modules in solid-state transformers, which is really more of a 2028 and beyond growth driver.
In the interim, we're also seeing an acceleration of engagement for shorter-term revenue opportunities battery with battery energy storage system, or BSS and other power grid-related applications, which are driving high demand for ultra-high voltage SC. A portion of these opportunities are expected to continue to grow in calendar 2027, layering on top of the first and second inflection point with AI data center. 
In closing, I'm very pleased with the progress. Navitas 2.0 is no longer a plan, but a reality. The results are demonstrated by the revenue mix, growth and margin expansion. By year-end, we will be a high-power company with mobile and low-end consumer essentially eliminated. The market rationale has sharpened. Power is the immediate constraints on increased compute.
Therefore, power efficiency is the solution to expanding capacity. The architecture of AI infrastructure is in the early stage of being rebuilt from the grid to the XP. The acquisition of Cloud completes Navitas' platform and our grid to XPU strategy. With SiC Gallium IVR, we are positioned not only to participate but to enable the multiyear transition with more than one monetization point. The timing of our complete transformation is ideal as we are at the intersection of 2 secular trends, the growth of AI compute and the rearchitecture required to it. 
From the grid to the XPU, our end goal is to help customers put more of every available megawatt into useful AI compute. Specific to the fourth quarter, the midpoint of our guidance represents another consecutive quarter of double-digit sequential growth and more than 100% growth year-over-year, driven by high power and AI infrastructure and contributing to further gross margin expansion. 
Our expectations for the fourth quarter also represent a return to growth for the full year, increasing approximately 7% in '26 with high-power growth more than offsetting our exit from the mobile business. We believe this is only the beginning as we remain committed on the path of delivering continued growth, incremental gross margin expansion and ultimately profitability. 
With that, I'll pass the call to Tonya to review our third quarter financial results and outlook for the fourth quarter.

**Tonya Stevens** (Executives):
Thank you, Chris. Before I begin, please note, unless otherwise indicated, I will focus my comments on non-GAAP results. A detailed reconciliation of all non-GAAP to GAAP financial measures can be found in our press release published earlier today. 
Revenue in the third quarter of 2026 was at the high end of guidance, increasing 33% sequentially to $14.0 million, an acceleration from the 22% sequential growth we delivered last quarter. This represents an increase of approximately $3.5 million from the $10.5 million in the second quarter. 
As Chris highlighted, the double-digit growth was driven by increased traction in high-power markets, which grew more than 50% sequentially and by triple digits year-over-year, reflecting our nearly complete shift in revenue composition away from our historical mobile and low-end consumer business. 
We continue to expect revenue contribution from mobile to become insignificant as in low single digits by year-end. As a result of improved product mix and higher quarterly revenue, gross margin expanded by another 50 basis points sequentially to 40.0%. This represented our third consecutive quarter of sequential gross margin expansion. 
Our accelerating shift in overall revenue mix toward higher-value, high-power markets and away from mobile and low-end consumer remains fundamental to our gross margin expansion strategy. We expect further gradual expansion of gross margin over the coming quarters as we continue to drive top line growth in high-power markets. 
Operating expenses for the third quarter were $16.5 million compared to $15.5 million in the prior quarter and $15.4 million in the same quarter a year ago. Consistent with the guidance we provided last quarter, OpEx increased by approximately $1.0 million as we began making targeted incremental investments in the business, particularly in new R&D programs to support accelerated growth. 
Having diligently maintained effectively flat OpEx through the first half of the year, we are increasingly focused on deploying resources and investments in a deterministic way to support the longer-term success and sustained growth of the transformed company. OpEx for the quarter increased roughly 6% sequentially, which was meaningfully lower than our top line growth rate of 33%. 
This and future incremental OpEx, including expenses related to Claros IVR technology stack and product development will be allocated to scaling the business, including investments to accelerate new product development, strengthen our engineering and application support for key committed programs and reinforce operational readiness in advance of expected growth in ramping shipments. 
Loss from operations for our third quarter was $10.9 million compared to a loss of $11.4 million in the prior quarter and $11.5 million in the third quarter of 2025. In Q3, weighted average basic and diluted shares outstanding were approximately $261.5 million, resulting in a Q3 loss per share of $0.03 compared to a $0.04 per share loss in the prior quarter and a loss of $0.05 per share in the year ago third quarter.
Turning to the balance sheet. Cash and cash equivalents at the end of the third quarter 2026 were $531.5 million compared to $557.4 million at the end of the second quarter. The decrease in cash and cash equivalents primarily reflects our ongoing build of TSMC buffer inventory. Also note, the quarter end cash balance was prior to the payment of the cash portion of the Claros transaction, which closed on October 5. 
Our effective pro forma cash balance adjusted for approximately $126 million payment for Claros subsequent to the quarter end would have been approximately $405 million. As a reminder, the company continues to have no debt. Also of note, I want to briefly highlight that we did not utilize any of our ATM facility during the third quarter and are comfortable with our current cash position following the Claros acquisition. 
Post Claros transaction, we continue to have ample capital resources to further accelerate and scale as a high-power company. This includes further anticipated strategic investments in support of advancing our integrated fabless manufacturing or IFM model initiatives, potential capacity expansion and supply reservation agreements with our U.S.-based Foundry partners as well as potential pursuit of selective strategic opportunities. With respect to inventory, we ended the third quarter with $32.4 million of inventory, including $11.2 million of inventory classified as long term on the balance sheet. This compared to $19.5 million in the prior quarter and reflects our previously planned build of appropriate buffers of TSMC wafers to ensure a smooth transition for our customers as well as other supply chain-related investments.
Similar to the previous quarter, the sequential $12.9 million increase in Q3 inventory primarily reflects our measured investment to support AI data center customers' future anticipated long-term growth. More broadly, channel and distributor inventory remains healthy. 
Moving to guidance for the fourth quarter of 2026. We expect continued sequential growth with revenue increasing 14% to $16.0 million, plus or minus $0.5 million. At the midpoint, this represents 119% growth year-over-year and what will be our fourth consecutive quarter of sequential growth, driven by high-power markets and specifically AI infrastructure. 
Also based on this guidance, we anticipate achieving revenue growth of 7% for the full year 2026 with our core high-power business continuing to deliver triple-digit growth even with our mobile business dropping to effectively zero after representing a large majority of total revenue last year. 
Exiting the year, we expect high-power markets to represent almost all of our business with over 40% of total revenue coming from AI infrastructure, which includes both our AI data center business and the grid and energy infrastructure business needed to support AI data centers.
Lastly, I would also add that we closed out the third quarter with very strong book-to-bill ratio, well above one, and we currently have solid backlog that extends into mid-2027. Non-GAAP gross margin is expected to expand to 40.5%, plus or minus 100 basis points, which at the midpoint represents a 50 basis point increase, reflecting our fourth consecutive quarter of margin expansion and the continued favorable shift in the revenue mix toward high-power markets and marginal incremental benefit from improved scale.
As previously discussed, OpEx will step up in the fourth quarter as we take on the overhead operating expenses associated with Claros as well as continue to make incremental investments organically, primarily focused on R&D and operational readiness in advance of our anticipated growth over the coming year. Non-GAAP operating expenses for the fourth quarter, which again will include Claros, are anticipated to be $25.0 million, plus or minus $1 million. 
That concludes our formal remarks. Operator, please open the call for questions.

**Operator** (Operator):
[Operator Instructions] And your first question comes from the line of Quinn Bolton with Needham & Company.

**Shadi Mitwalli** (Analysts):
This is Shadi Mitwalli on for Quinn. Congrats on the results. I think you guys mentioned that backlog is extending into mid-2027. And as these high-power markets start to inflect, it would be great to get a sense on how we should be thinking about growth heading into next year.

**Chris Allexandre** (Executives):
Thank you, Shadi, for the question, and I appreciate you giving us a platform to talk about the outlook for next year, right? So as we talked about in the last two earnings, we've seen consistent increase in book-to-bill. As a matter of fact, the book-to-bill last quarter or Q3 was actually two and has been consistently way above one for the last two quarters, right? 
So the way we see '27 with the inflection point unfolding on top of each other is the path for us to be a double-digit growth quarter-over-quarter fueled by the acceleration of AI infrastructure, which we mentioned in the earlier remarks that will triple from the baseline in '26. And that double-digit growth will continue to accelerate as each of the inflection point comes on top of each other. 
So basically, the message today is we've done the first part of the transformation of the company, which is the financial pivot we talked about, consumer to high power, as you mentioned. And now we're entering the other phase of the company where the growth is just starting driven by the AI infrastructure will give us multiple years of double-digit quarter-over-quarter growth.

**Shadi Mitwalli** (Analysts):
Great. That was helpful. And then maybe just on the Claros acquisition. We see a number of IVR acquisitions we announced over the past few months. So I was just curious, can you guys talk about what you guys saw in Claros and maybe some of the advantage of their technology versus competing IVR technology?

**Chris Allexandre** (Executives):
Thank you. Very good question. So the first thing before I answer specifically your question, what I would say is the fact that other MOSFET and silicon companies are acquiring IVR is a confirmation that what we talked about, which is the architecture has to change, okay? 
The way lateral power delivery today moving to vertical power delivery using the same technology kind of put together in a vertical package is not going to sustain the density and the amount of current that those processors need, right? What we saw in Claros, and I'll put aside the culture, the very similar to -- and the quality of the engineering team is a real IVR technology stack designed for XPUs. 
Instead of IVR that was designed for computing converted, okay, to AI data center like we've seen in some of the companies that just got acquired, right? A true 3.3-volt starting point, allowing to do a 3:1, everything integrated in the stack, the capacitors, the inductors, the controllers, the FinFET, basically allowing you to do real high density because you don't need external component, right? 
And that's what we saw. And the modularity, which I mentioned in the webcast, is also important. What we see is, of course, everybody talks about the lead GPUs, but there's as many processors now that we have use case. And all those processes, call it CPU, XPU, NPU, LPU,PU customs, right? They all need super high density, high current type of IVR and power delivery. And I think the flexibility and the modularity that we saw in Claros is unique, and that's why we made that move.

**Operator** (Operator):
Your next question comes from the line of Kevin Garrigan with Jefferies.

**Kevin Garrigan** (Analysts):
Chris, congrats on the great results and all the progress. Going off of Shadi's question, can you just give us a sense of how much of the 2027 growth is supported by awarded programs and what is already in your backlog today versus expected design conversions?

**Chris Allexandre** (Executives):
I'll start and Tonya can add some comments, right? So, we have backlog way into '27 already. So we cannot say the whole year is done, right? But what I would tell you is we are very surprised, and I mean, positively by the acceleration of the Inflection 1, which we saw really in Q3 and Q4 this year, but Inflection 2, right, which is the sidecar where we see an accelerated conversion of the number of programs across AC-DC, DC-DC and BBUs. 
So more programs converting faster into higher power, converting from design into design win into backlog. And last but not least, because we talked about inflection in Inflection 3 in the last call, now we start to see -- and we mentioned it in the remarks, right, we've actually got a pretty large order, 1 million units of GaN devices for an 800-volt DC-DC high-density brick for Inflection 3, right? So things are really coming into shape. I would tell you, Kevin, slightly faster than I even expected six months to three months ago.

**Tonya Stevens** (Executives):
Yes. And I would just go on top of that. That's exactly what I see and how I think about it. The Inflection 1, like Chris talked about, it's in our revenue. We saw it in our revenue last quarter. We see it in our revenue this quarter accelerating. Inflection 2 in our backlog, that's helping us fill out 2027. And even Inflection 3, we're starting to see that move beyond just high-volume orders and sampling. He talked about the one million units. That's a significant amount of volume that we're looking at for Inflection 3. So that's exactly what we're seeing.

**Kevin Garrigan** (Analysts):
Yes. Got it. Okay. That's perfect. And then just on gross margins, congrats on the continued expansion. Can you just give us a sense about how we should think about the gross margin profile between silicon carbide, GaN and IVR as each business scales? So, we don't really kind of give detail on the split on gross margin between the different technology. What I would tell you is, if you look at the gross margin expansion in '26, right?

**Chris Allexandre** (Executives):
So, let's go back. A year ago, to this day, we talked about transforming this company from consumer to high power. Basically, the gross margin has increased, if you look at the guidance for Q4 by two points. That was essentially moving from consumer to high power. The next phase of the expansion of gross margin is coming from scale as we continue to grow double digit, but also with the AI infrastructure, which is now 40% of the company in Q4 and poised to triple next year. 
And that part of the business is actually much also on a higher margin, right? So what you're going to see is I just got the question before, how do we see growth, right? I mentioned double-digit quarter-over-quarter with that double-digit kind of accelerating over time. 
I think you're going to see the same on the gross margin, consistent gross margin expansion quarter after quarter as we scale. And of course, as we continue to make fundamental transformation moving to 18-inch on the GaN, continue to work with our foundries on cost reduction and so forth. But I mean, look at this as a continuous gross margin expansion organically with the migration to high power and now to AI infrastructure.

**Tonya Stevens** (Executives):
Yes. And I would just confirm that the way we think about it is not relative to the technology, but complexity. And we've given you sort of the insight before that the higher power, higher complexity, it is, the higher the ASP and margin tend to be. And that includes more difficult technology problems to solve, including the IVR technology stack. Those tend to contain higher margins. versus splitting that between GaN and SiC.

**Chris Allexandre** (Executives):
Yes, Kevin, one thing I would add is, I mean, Tonya is spot on, right? Margin comes with value, value comes from the complexity you're solving the customer problems. What we see is look at Inflection 1 and Inflection 2, right, or even going to Inflection 3. 
We are talking about multiple x of density of power on the AC/DC front, moving from silicon to silicon carbide, then moving to GaN when the add-on become native. Those complex problems, customers are basically retributing with good margin if we solve their problem with speed. And I think this is what kind of goes back to the core of what we are trying to do as a company.

**Operator** (Operator):
Your next question comes from the line of Kevin Cassidy with Rosenblatt.

**Kevin Cassidy** (Analysts):
And I'll echo the congratulations on the steady progress. In the IVR market, that's a new market. How early on in the XPU or GPU design do you have to be to define the IVR? Do you have to work with them as they're designing the XPU?

**Chris Allexandre** (Executives):
So it's a very good question, Kevin. Thanks for asking it. So first of all, I think what you need is what we call an IVR technology stack. That's what we got with Cloud, right? So, integration of the FinFETs, the controller, the inductors, the capacitors all together into the same technology. 
Then you apply that to either vertical power delivery, which is basically a chip that you put on the backside of the PCB or in the PCB, right, in the form of an array, as we talked about, to deliver the power then to the customer or even going one step further where it's not a chip anymore, you embed the full system or a subpart of the system into the substrate and the XPU. In both ways, you have to work with the XPU vendors. 
In both ways, you have to work with the OEM or power OEM that serve the last step of our delivery to the XPUs to basically fit the right architecture. And that's what I got the question from Sean earlier on, I think it was Kevin. What did we like about Claros, right? Well, I liked beyond the best density in my opinion, because there's no caps outside is this modularity. So every customer needs a different type of shape of the Power VRM and a different level of voltage and current, right? And that's kind of where you have to work with those. 
The other thing I would say is keep in mind that many customers are becoming vertically integrated. So we used to have GPU companies. Now we have hyperscalers doing their own processors. We also have processor companies that become rack company, right? So the answer to your question is the technology stack is the same, but you have to work with the processor company, which are becoming rack company or even hyperscaler company to basically deliver the power delivery.

**Kevin Cassidy** (Analysts):
That's great. Yes, it's getting to be a complicated design cycle. And which brings me to an interesting strategy you brought up is integrated service manufacturing where you're going to buy the equipment. And I guess, is that going to be in the back end? Like, as you're describing the IVR could all be different shapes and packages for different designs. Is that where you're bringing in the equipment? Or will it be on the front end, too?

**Chris Allexandre** (Executives):
So, let me just correct you for a minute, right? We talk about integrated fabless manufacturing for IFM, right? Primarily on the foundry side. So the best way to think about this is if you look at both SiC and GaN, -- we actually own the technology stack, same on the IVR, right? So, on the SiC side, we have GenSiC, which is a full stack high-voltage, high-voltage technology. 
On the GaN side, we overlay on top of TSMC in the past, now GF, our own IP to differentiate in reliability and other figure of merits and same with the IVR when we own the full stack, right? So, what we want to do is to own the stack but partner with foundries where we invest capital to basically secure capacity and supply to enable cost predictability and competitiveness. 
So, the best way to think about this is a bit of the similar kind of we announced with GF on the GaN side and other foundry we work with, can we put the best of both together. We don't want to be an IDM. We don't want to be a fabless, we're somewhere in the middle, and we believe this is the best capital-effective way to deliver the high growth while controlling our technology.

**Operator** (Operator):
Your next question comes from the line of John Tantan with CJS Securities.

**Jonathan Tanwanteng** (Analysts):
Congrats on a nice quarter and outlook. I was wondering I think I heard pretty clearly that you expect to grow data center infrastructure revenue by 3x going into next year. What do you think the non-data center portion contributes? If you can tell us what's involved there and what the contribution might be?

**Chris Allexandre** (Executives):
Yes. Jon, thanks for asking that question. As I talked about, we have backlog way into '27. As a matter of fact, the visibility we have in AI infrastructure is much longer and much extended compared to other markets, right? So what we've modeled for next year is anything non-AI infrastructure is more or less flat. 
We see some growth in industrial. We see some flattish in the computing. Remember, we addressed the super high-end computing market, not the computing market as a whole, right? So we've assumed that flat because we don't have a full year or even two quarters type of visibility. 
But on the AI infrastructure, as you pointed, because of the visibility we have, because of the accelerated momentum in Inflection 1, Infelction 2, because of number of design win converting, we are clearly seeing a potential for that business to more than triple next year, right? 
So the best way to think about it is '26 was a year of high power basically compensating the exit of mobile. This is done. This even allowed us to get higher than when we started this journey from a revenue standpoint and getting 2026 with $16 million. Next year is really the growth is coming from AI infrastructure, and we assume the rest being flat.

**Jonathan Tanwanteng** (Analysts):
Okay. Great. And then more interestingly, as you head into '28, I think you've got multiple accelerations, right? You have the NVIDIA 800-volt products ramping. You have the SST products ramping, you have Claros ramping. Do you see further acceleration in '28? Or is it hard to comp against the growth you're going to see in '27 or maybe it's a smaller base that you can still accelerate from there?

**Chris Allexandre** (Executives):
Of course, it's more difficult to predict as you get longer in the horizon, right? What I would tell you is we see based on the product we have, the technology we have, the engagement we have, the inflection points, double digit, and that double-digit quarter-over-quarter is going to accelerate as each of those inflections overlay with each other. So it's not inconceivable to see the quarter-over-quarter compound growth to start to accelerate late '27 into '28 into '29. As each of those technology, SiC, GaN and even IVR overlay on top of each other and each of those inflections come on top of each other.

**Jonathan Tanwanteng** (Analysts):
Great. If I could ask one more, just, Tonya, how do you see OpEx scaling with all this revenue growth? Do you have a number as maybe as a percentage of revenue growth? Or is there another way to think about it over the next year or 2?

**Tonya Stevens** (Executives):
Yes, that's a great question. So the step-up you saw in Q4, we talked about that was our normal run rate of our guidance as well as Claros taking on Claros. And the way we think about that is still what we've talked about before, OpEx increasing at a percent of revenue. So after that initial step-up, we see that happening in '27, so as a fraction of our revenue growth. We're not really giving the full year out, but that's how we're thinking about that.

**Chris Allexandre** (Executives):
John, I think one thing I would add on top of what Tonya said is we've been very clear since the beginning of this transformation that our eyes are on getting to a profitability. Profitability will come from scale. We have two vectors. One is scale and consistently growing double-digit the revenue, as we talked about. 
Number two is gross margin expansion and the gross margin expansion will continue as we just talked about. And when IVR comes in play, we see also a step function in the combined gross margin of the company. But we remain focused on making sure we do that by increasing OpEx at a fraction of the revenue growth, so we can get to profitability at the horizon, right, which remains a very important focus for us.

**Operator** (Operator):
[Operator Instructions] And your next question comes from the line of Richard Shannon with Craig-Hallum.

**Richard Shannon** (Analysts):
I'm going to follow up on the last question and answer, especially taking to the obvious angle here, which is thinking about a breakeven model here. Not asking for the time frame you might hit this, but how do we think about that model here? 
And I presume that it would -- I guess I'd prefer an answer that would include IVR with the gross margin dynamic you described here, but kind of scale and what's the margin structure or I guess, maybe I'll just let you answer of how we can look at the breakeven model. And I have a follow-up.

**Chris Allexandre** (Executives):
So thank you, Richard, and good to hear from you. I think the best way to think about this is I think we're going to continue organically to grow the consistent gross margin. We see the company gaining a couple of points over time. And then it's not inconceivable, as I said, once we have IVR I think that the blend of the gross margin is north of 50%. 
Once you get there, if you take our OpEx in Q4 of this year, kind of multiply by four annualize it and increase -- apply a yearly increase, which is less than revenue, you're basically getting OpEx in the low 30s, right, which at 50% gross margin would basically make the breakeven point around the low 60s. So that's kind of -- if you ask me about the model, that would be kind of the model you have to keep in mind.

**Richard Shannon** (Analysts):
Okay. Perfect. That's very helpful. Chris, maybe just ask a very high-level question here since we've seen some activity both with Navitas as well as across the industry, but some patent arguments, I guess, we'll call it there, and you've -- you're on both sides of this. Maybe you can help us understand where you sit here and how you expect kind of the industry to evolve over the next couple of years in this dynamic.

**Chris Allexandre** (Executives):
Richard, I think I kind of got the question in the last earning about the litigation. I think I was fairly explicit, okay, on the last earning on my view of this. If you don't mind, I would defer to what I said before. We'll continue to defend our IP and we'd expect IP, but we'll continue to defend our IP. And I would defer to what I said on the last earnings, if you don't mind.

**Richard Shannon** (Analysts):
No problem there. Maybe let me ask another question, a replacement of that one here, Chris. Maybe you can talk about the inflections here, and obviously, you're gaining some real traction in backlog here in inflections numbers one and two here. Maybe if you can talk about your share in any kind of qualitative terms here in any way that you think is interesting, like SiC versus GaN or any specific pieces within those inflections, that would be helpful.

**Chris Allexandre** (Executives):
It's hard to give you a blended market share, right, of the Inflection 1, but a couple of data points, right? Number one is Inflection 1 is essentially replacing as you move to 3, 5, 10 or 8, 10-kilowatt density of PSU, right? You're replacing silicon with silicon carbide. And the beauty of this is this is replacing with 1.2 kV.
 So, the content is pretty nice. And usually, you have two to three vendors, right? So, some program, we are first source, some program we are second source. And when you have 3 vendors, right, one gets 40, the other one gets 30, the last one gets 30. So, I would say, over time, it trends to a good 30% to 40% share of the market -- of the PSU we participate in. 
What is interesting in the inflection 2 is, number one, it's a lot more application. So there is AC/DC, which is basically now taking it to 15, 18, 25, 27, 30 kilowatt. There is also DC-DC with 15, 30-kilowatt DC-DCs and BBU, which start to use both SiC and GaN. So, the beauty of Inflection 2 is not just a SiC play. It's also a GaN play, right? And here, we've seen, in some cases, we're sole source. In some cases, we are gain sharing, right? 
So, for me, the way I view it is what you want is to be first on the print, okay, and give customers a secured path from availability standpoint and execution standpoint, so they can ramp the production because I talked about it earlier, we see an acceleration. If you would have asked me six months ago, do you see Inflection 2 and sidecar coming that fast, I would have said it's coming, but it's definitely coming faster than we expected. 
Same with Inflection 1, okay? That's why you saw us kind of coming on top of the estimates, okay, that we had set for ourselves that you have set for ourselves, right? So, I think the speed is helping because if you are first and speed is core to our values, if you first, you can command more share, right? But it's difficult to give you kind of how much market share of that market we own. 
What I would tell you is if you remove mobile, we grew in '26 based on the midpoint of the guidance for Q4, right? We grew 125%. I believe this is faster than the market. If you look at GaN and SiC serving highpower/AI infrastructure, it's faster than the market. So the momentum is there for us to gain share, okay? And we are not here to participate, as I mentioned. We here to gain share. 
So, I think we have with our speed and the technology and the focus that we have. We're not a company that does EV on Monday, industrial on Tuesday and AI data center on Wednesday and Thursday, right? That's the only thing we do. And that focus helps us to secure more share than our competitors.

**Operator** (Operator):
Your next question comes from the line of John Tanwanteng with CJS Securities.

**Jonathan Tanwanteng** (Analysts):
I was wondering if you could talk a little bit more about Claros. I think you disclosed on the update call you gave a week or two ago that they have an anchor customer for the IVR product. What is the potential scale of that one customer, number one? And number two, what is the pipeline of additional customers behind that? And how quickly could those come into play over the '28 to '29 timeframe?

**Chris Allexandre** (Executives):
Thank you, John, for that follow-up question. So, the anchor customer is a vertically integrated customer that look at processor up to the system level. Claros has been working with them from the beginning. To Kevin's point earlier, it has helped to shape the technology because it's not just about the technology stack is how do you put that into a chip, into an array, into a system that delivers density, right? 
So that customer, as we mentioned at the acquisition, is going to ramp in a meaningful way really late '28 and '29. Since -- and Claros before the acquisition was essentially focused on that customer to prove their technology and get scale, right? Since we combined the two companies, we've met pretty much everybody out there doing an IVR program. And we're starting to see good feedback, but also good momentum in the technology that we had. 
And again, what -- the consistent feedback we have is this is a race for density, okay? And then you're going to get into argument into Claros versus Ferric versus Empower versus Parlattice and others, who has the best density and who has the best approach, right? And I don't want to bore you with details, but density without caps outside or density with caps outside is different. 
But this is not what customers tell me. Customers love the modularity of Claros. Let say this is something which has been though through with the system in mind, not even the XPU in mind with the system in mind. And that is getting a lot of traction. And I think we'll, under Navitas, be able to scale that to more customers. A bit too early to declare victory, right? There's a lot of work to do.

**Operator** (Operator):
That concludes our question-and-answer session. I will now turn the call back over to Mr. Chris Allexandre for closing remarks.

**Chris Allexandre** (Executives):
So thank you, everybody, for listening to us. I'll leave you with something which I said, but I think it's very important that you crystallize that in your mind, right? A year ago, to this day, we said we're going to transform this company from a consumer-centric company to a high-power company. We've done that at the same OpEx, more or less. 
We gained two points of gross margin and while we have been able to deliver consistent double-digit growth for the last few quarters despite the headwind of conscious moving away from mobile. Now we're entering into the second phase of the company. We've focused ourselves into AI infrastructure. We have the technology stack that we need from the ultra high-voltage SiC, high-voltage SiC, GaN and IVR. AI infrastructure, which is data center and the grid that power infrastructure is 40% of our sales at the end of Q4 is going to drive the growth in the future. 
And I think we just got started. And I feel -- now there's a lot of work to do. This market is very demanding in reliability and speed, but I think we have the right team, the right technology. And I think now you have to think about us as a consistent double-digit growing company, leveraging the inflection points that come on top of each other. That's what I want to leave you with. 
And I also want to take this opportunity to thank our employees. It's a lot of work to transform the company, and they've been very resilient and determined to do this. And now we are just can scale Navitas to the next level. So, my closing remark goes to them and all the work they've done for the last 12 months and what they're going to do in the future. Thank you.

**Operator** (Operator):
Ladies and gentlemen, that concludes today's call. Thank you all for joining. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NVTS_Q2_2026_Earnings_Call_20260727.md
- 2026-07-27｜CFO Tonya Stevens｜guidance：CFO 給 Q3 營收財測：季增 28% 至 13.5M，±0.5M。（原話："revenue increasing 28% to $13.5 million, plus or minus $0.5 million"）
- 2026-07-27｜CFO Tonya Stevens｜guidance：Q3 non-GAAP 毛利率財測 39.7%±100bp。（原話："Non-GAAP gross margin is expected to be 39.7%, plus or minus 100 basis points"）
- 2026-07-27｜CFO Tonya Stevens｜guidance：Q3 non-GAAP 營業費用財測區間 15.5M–17.5M。（原話："Non-GAAP operating expenses are anticipated to range between $15.5 million to $17.5 million."）
- 2026-07-27｜CEO Chris Allexandre｜guidance：CEO 表示下半年持續季度雙位數成長，全年達中個位數營收成長，Q3 回到年增。（原話："This also translates to achieving mid-single-digit revenue growth for the full year"）
- 2026-07-27｜CEO Chris Allexandre｜guidance：CEO 預期年底 AI 基礎設施占總銷售超過三分之一。（原話："We expect AI infrastructure market will represent more than 1/3 of our total sales by year-end"）
- 2026-07-27｜CEO Chris Allexandre｜guidance：管理層不給 2027 財測，只方向性說明 Q4。（原話："Of course, we're not going to guide '27."）
- 2026-07-27｜CFO Tonya Stevens｜margin：Q2 non-GAAP 毛利率 39.5%，季增 50bp、年增 100bp，管理層歸因於產品組合與規模。（原話："gross margin expanded by 50 basis points sequentially and 100 basis points year-over-year to 39.5%"）
- 2026-07-27｜CFO Tonya Stevens｜margin：Q2 營收 10.5M、季增 22%，高功率市場年增超過 50%，數字口徑為 non-GAAP。（原話："increasing 22% sequentially to $10.5 million"）
- 2026-07-27｜CFO Tonya Stevens｜margin：Q2 營業費用 15.5M（Q1 為 15.0M），位於財測高端；營業虧損 11.4M。（原話："Operating expenses for the second quarter were $15.5 million compared to $15.0 million in the prior quarter"）
- 2026-07-27｜CFO Tonya Stevens｜margin：CFO 說明 Q3 起季度 OpEx 增加約 1.0–1.5M（約 10%），並稱低於營收成長率。（原話："a prudent increase of approximately $1.0 million to $1.5 million in quarterly OpEx beginning in the third quarter"）
- 2026-07-27｜CFO Tonya Stevens｜margin：GAAP 含 2.03 億美元非現金 earn-out 費用，稱已全數認列、不再發生。（原話："a noncash charge of $203 million related to the October 2021"）
- 2026-07-27｜CFO Tonya Stevens｜margin：存貨 19.5M（前季 14.9M），另預付款項增加約 15M，為 TSMC 晶圓緩衝庫存。（原話："we ended the second quarter with $19.5 million of inventory compared to $14.9 million in the prior quarter"）
- 2026-07-27｜CEO Chris Allexandre｜commitment：CEO 承諾毛利率逐步擴張並維持邁向獲利的路徑。（原話："gradual gross margin expansion through improving mix and scale"）
- 2026-07-27｜CEO Chris Allexandre｜commitment：CEO 強調獲利目標未變，OpEx 增幅為營收成長的一部分。（原話："our focus and eyes on getting this company to get profitable has not"）
- 2026-07-27｜CEO Chris Allexandre｜commitment：管理層預期年底行動與低階消費業務變得微不足道，且稱比原預期早一季。（原話："we are 1 quarter ahead of my expectation in terms of mobile being gone"）
- 2026-07-27｜CEO Chris Allexandre｜commitment：GlobalFoundries 8 吋 GaN：年底前送樣與驗證，2027 初有合格產品。（原話："we expect to have initial qualified product in early"）
- 2026-07-27｜CEO Chris Allexandre｜commitment：計畫 Q3 發表 6.5 kV SiC 技術，並預告數週內公布 10 kV 開發。（原話："planned third quarter release of our new 6.5 kV SiC technology"）
- 2026-07-27｜CFO Tonya Stevens｜capital_allocation：季內募資約 3.73 億美元，均價 21.89 美元，無負債。（原話："additional capital raised during the quarter of approximately $373"）
- 2026-07-27｜CFO Tonya Stevens｜capital_allocation：現金數字口徑不一：CFO 說 557M，CEO 說 567M（原文如此）。（原話："Cash and cash equivalents at the end of the second quarter 2026 were"）
- 2026-07-27｜CEO Chris Allexandre｜capital_allocation：CEO 稱現金 567M，列出資金用途含 Foundry Plus、產能擴張與潛在併購。（原話："with $567 million of cash at quarter end"）
- 2026-07-27｜CEO Chris Allexandre｜capital_allocation：CEO 說明提前加碼投資的決定：成長來得比預期早，是有意識的決定。（原話："we decided to pull"）
- 2026-07-27｜CEO Chris Allexandre｜product：CEO 描述 800V 四個拐點，第一個為 2026 下半年起、2027 上半年加速的 AC/DC PSU 以 SiC 取代矽，與 800V 無關。（原話："SiC adoption in AC/DC PSUs is being driven by power scaling and density requirement independent of the 800V DC initiatives."）
- 2026-07-27｜CEO Chris Allexandre｜product：CEO 稱 800V 架構轉換預計 2027 年發生。（原話："the transition to 800V architecture for next-generaton AI data"）
- 2026-07-27｜CEO Chris Allexandre｜product：新 1.2kV JFET 產品線預計明年初推出，稱增加約 10 億美元 2030 年 TAM。（原話："opens door to address an additional $1 billion of"）
- 2026-07-27｜CEO Chris Allexandre｜product：授權 Magnachip GeneSiC Gen 4/5 技術，CEO 稱主要目的為擴大 SAM 與第二晶圓來源，授權收入非首要目標。（原話："this is not so much about the licensing."）
- 2026-07-27｜CEO Chris Allexandre｜product：高效能運算電源升級，筆電充電器 280W，單機 GaN 含量約 5–6 美元。（原話："you have about $5 to $6 of content of GaN"）
- 2026-07-27｜CEO Chris Allexandre｜customer：CEO 敘事變化：成長不再只靠單一大 GaN 插槽，而是數十個專案、多客戶。（原話："it's 10s and 20s of programs, different programs, different board, different customers"）
- 2026-07-27｜CFO Tonya Stevens｜customer：CFO 稱 AI 基礎設施 Q1、Q2 皆季增超過 50%，預期持續加速。（原話："AI infrastructure is growing at over 50% quarter-on-quarter, both in Q1 and in Q2"）
- 2026-07-27｜CEO Chris Allexandre｜customer：CEO 稱第二拐點已進入大量系統級測試，非原型階段。（原話："this is not anymore prototype, right?"）
- 2026-07-27｜CEO Chris Allexandre｜competition：CEO 稱優先 AI 基礎設施而非車用，與部分競爭者不同。（原話："prioritize AI infrastructure over automotive, unlike some of our"）
- 2026-07-27｜CFO Tonya Stevens｜competition：CFO 稱同時擁有 GaN 與 SiC 的競爭者很少。（原話："A few competitors have both and having both allows us to participate"）
- 2026-07-27｜CEO Chris Allexandre｜competition：價格：CEO 稱核心市場漲價目前不是公司重點，不給具體說法。（原話："has not been so far a focus on our side."）
- 2026-07-27｜CEO Chris Allexandre｜risk：Wolfspeed 專利訴訟（GaN 與 SiC）；CEO 不評論細節，並稱 Wolfspeed 訴訟是騷擾與恫嚇。（原話："a campaign of harassment and intimidation through litigation"）
- 2026-07-27｜CEO Chris Allexandre｜risk：Renesas 於法說前一週另提訴訟；CEO 指其持有 Wolfspeed 最多 39%。（原話："Renesas sued us."）
- 2026-07-27｜CEO Chris Allexandre｜risk：分析師問 800V 延遲與 NVIDIA Kyber 機櫃傳聞對 2027 的影響，CEO 答不改變展望。（原話："do we see that as a change in the outlook of [indiscernible]? The answer is no."）

### 問答異常語氣（迴避／改口／保留）
- NVTS_Q2_2026_Earnings_Call_20260727.md｜問：Quinn Bolton 問 NVIDIA Kyber 機櫃傳聞與 800V 延遲是否影響 2027 營收展望｜答法：CEO 表示不評論 NVIDIA 與 Kyber，改談多個拐點與 GaN/SiC 兩種技術；僅回答對展望的影響為「no」，無數字
- NVTS_Q2_2026_Earnings_Call_20260727.md｜問：Madison de Paola 問 2027 成長中已承諾專案與仍在驗證專案的比例｜答法：CFO 稱不拆分已承諾或積壓訂單比例，改談拐點疊加與驗證階段專案數；CEO 稱不給 2027 財測
- NVTS_Q2_2026_Earnings_Call_20260727.md｜問：Tristan Gerra 團隊問年底高端運算與資料中心的營收組合｜答法：CFO 與 CEO 皆稱不拆分數字，只重述 AI 基礎設施年底占 1/3 以上
- NVTS_Q2_2026_Earnings_Call_20260727.md｜問：分析師問 Wolfspeed 訴訟機率與風險｜答法：CEO 稱無法評論，但長篇陳述訴訟背景與時機，未回答勝算與可能損失
- NVTS_Q2_2026_Earnings_Call_20260727.md｜問：Jonathan Tanwanteng 問 Magnachip 交易是按量或固定費用、何時貢獻營收｜答法：CEO 未回答計價結構與貢獻時點，只稱授權非首要目的
- NVTS_Q2_2026_Earnings_Call_20260727.md｜問：分析師問產品是否漲價｜答法：CEO 稱不談與客戶的具體漲價，只說目前焦點在客戶採用新技術

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

## ⑥ 條件附卡（archetype_hint='未獲利高成長' 命中）：judge_addendum_archetype.md

<!-- source: .claude/skills/stock-analyst/references/archetype-gatesets.md sha256:d173785f92087f36 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary ∈ {金融，未獲利高成長，轉機/特殊情境，受監管公用/穩定內需} -->

# archetype 換尺 gate-set 附卡（QC-44/45/46）

## QC-44 金融（bank／insurer／broker）
archetype=金融時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：ROTCE(替FCF Margin) >15%穿越循環｜ROE且>COE~10%(替ROIC) ROE>12-15%｜跨信用循環ROTCE穩定含2008/2020壓力年(替10Y ROIC穩定) 壓力年仍正/不破底｜NIM趨勢+效率比cost/income(替毛利率定價) 效率比<~60%｜Capex/Rev不適用→operating leverage/效率比改善｜EPS+TBVPS複合+股息總回報(替EPS CAGR>20%) ~10-12%即優｜P/TBV vs ROTCE(替PEG)：Warranted P/TBV=(ROTCE−g)/(COE−g)，實際P/TBV≤warranted｜CET1 ratio(替D/E<0.7) >監管要求+緩衝(~11-13%)｜NPL/NCO趨勢+撥備覆蓋+CET1緩衝(替負債安全性)：信用品質穩、撥備足。[§QC-44]
§10估值主錨：P/TBV分位+P/E，用Warranted P/TBV判貴賤；EV/EBITDA拿掉。QC-31 signal：X改ROTCE跨循環<COE／CET1跌破監管／NPL·NCO結構惡化／重大舞弊，移除FCF·NI、EV-EBITDA、Capex觸發。§6跑道：放款·存款·AUM成長+費收業務+市佔，非TAM滲透。[§QC-44]
子型：bank＝CET1/NIM/效率比/NPL·NCO/ROTCE/P-TBV｜insurer(注意US掛牌ALV=Autoliv汽車安全件循環工業，非保險，勿誤歸)＝combined ratio<100%/float/Solvency II ratio/book value/ROE，不看NIM/CET1｜broker·交易所＝ARPU/AUC/take rate/活躍戶，常與未獲利高成長blend｜支付網絡不歸金融，走品質複利。[§子型]
batch補搜：`[ticker] CET1 ratio NIM efficiency ratio ROTCE`(bank)／`[ticker] combined ratio Solvency II book value`(insurer)；yfinance .info 給不出 CET1/NIM/效率比/NPL/ROTCE/TBV。[§batch]

## QC-45 未獲利高成長
archetype=未獲利高成長時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：Rule-of-40(營收成長%+FCF margin%，替EPS CAGR>20%) ≥40｜EV/S÷營收成長growth-adjusted或EV/gross-profit(替PEG<2)｜NRR+毛利率+增量OI margin改善軌跡(替ROIC>15%，GAAP負無意義) NRR>110%/GM>65-70%｜FCF margin+轉正軌跡(替FCF Margin>15%；已正看margin升，未正看跑道+轉正路徑)｜NI負時FCF/NI比無意義→改看FCF margin絕對值+淨現金+跑道，FCF正或跑道>12個月。[§QC-45]
§10估值主錨：EV/S(+EV/gross-profit)+Rule-of-40-adjusted，轉正後接forward P/E；trailing PE/PEG拿掉。**情境樹同步改走EV/S（2026-10-12）**：FY1共識EPS≤0時程式自動切`valuation_basis=sales_multiple`，`scenario_inputs`填營收路徑×終端EV/S×終端淨負債×終端股數（形狀見尾段），不再用EPS×本益比；負債重者(淨負債/EV>30%)Bear的`net_debt_y5`須如實反映融資缺口，股權價值為負即歸零。QC-31 signal：不因GAAP NI負觸發X；X改NRR跌破100%／Rule-of-40<20連2季／毛利結構崩／現金跑道<12個月無轉正路徑／SBC稀釋失控(股數>10%/yr無營收槓桿)。§6跑道：NRR+淨增客戶+TAM滲透+SBC-adjusted轉正時程。blend：fintech broker常＝金融×未獲利，兩套都跑、標背離。[§QC-45]

## QC-46 轉機／受監管公用（輕量尺，不展開大表）
轉機/特殊情境：§4/§10主錨→資產重估/SOTP/normalized earning power/P-TBV，非成長外推；EPS-CAGR/PEG不適用。Single Thing→轉機觸發(債務重組完成/出售虧損部門/新管理層/catalyst里程碑)，非「moat擴張」。§6/§5→「為何現在會轉」catalyst+下行保護(資產底/清算價值)。QC-31 X→流動性危機(跑道<12個月+無再融資)/重整失敗/治理舞弊。[§QC-46轉機]
受監管公用/穩定內需：§4/§10主錨→DDM/殖利率+股息成長/regulated ROE(rate base×allowed ROE)/P/B；PEG/高成長門檻不適用。§6成長→rate base成長+費率案(rate case)+准許ROE，非TAM滲透。§5護城河→監管特許/天然獨佔(single-axis)。QC-31 X→准許ROE結構下調/費率案連敗/監管轉敵/過度槓桿(利率敏感)。[§QC-46受監管]
此兩類不強制長表，但換尺與catalyst/下行保護須sourced。[§QC-46]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260524","verdict":"X 迴避：估值 🔴 P/S 163x（同業 8x 的 20 倍）+ MA 動能末段（4 週 +144% 漂移）+ 體質 veto 4 項不過 + 共識目標 .88 隱含 −56% 下行。NVIDIA 800V HVDC thesis 真實但已透支；等回測 Bollinger 中軌  區或 2027H1 Rubin Ultra Kyber 量產驗證後再重評。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Navitas 2.0 high-power 業務翻轉成功，2027 high-power 占營收 &gt; 70%","columns":{"2Y 驗證點":"2026Q3 high-power 占比 &gt; 55%；Q4 達 &gt; 65%；FY26 revenue ≥ $41M guide 下緣","5Y 驗證點":"FY27 revenue ≥ $72M consensus（high-power 主導）；FY28 ≥ $120M","10Y 驗證點":"FY30 revenue ≥ $300M（SAM 10% 滲透）","具體數字門檻":"FY26 $41M guide / FY27 $72M sell-side / FY30 $300M = 公司 SAM 推估的 10% 滲透","信息來源":"FY26 公司 guidance + yfinance 8 位分析師共識 + Navitas IR 2025-08 AI 數據中心 SAM deck","漂移觸發條件":"連 2 季 TTM revenue &lt; consensus −10% → H1 削弱；連 3 季 → H1 反轉"}},{"id":"H2","text":"NVIDIA 800V HVDC 中 NVTS 維持 ≥ 25% BoM share（GaN 高功率 + SiC reference）","columns":{"2Y 驗證點":"2027H1 Rubin Ultra Kyber 系統第一波量產，NVTS 公告 design win / shipment 數據；2027Q1 報季 high-power 中 data center 占比可拆","5Y 驗證點":"2028-29 Vera Rubin + 後續代次規模化期間，NVTS share 不被 POWI / Infineon / ST 擠至 &lt; 20%","10Y 驗證點":"2030 800V HVDC 成為 hyperscaler 主流時 NVTS 仍是 top 3 GaN / SiC 高功率供應商","具體數字門檻":"NVIDIA Kyber rack BoM 中 GaN + SiC 含量 ≥ $300/GPU；NVTS share ≥ 25% = $75/GPU；Rubin Ultra 年產量假設 200K-500K GPU → NVTS data center 年營收 $15-37.5M（單一架構）","信息來源":"NVIDIA 官方文件 + 第三方 teardown（ChipRebel / TechInsights）+ NVTS 法說會揭露","漂移觸發條件":"連 2 季 NVIDIA data center revenue 占比 NVTS 總營收 &lt; 30% → H2 削弱；2027H1 Kyber 量產確認 NVTS BoM share &lt; 15% → H2 反轉"}},{"id":"H3","text":"估值倍數從現價 P/S 95-165x 收斂至 25-30x 同業溢價區間之前不再大幅向上（前提：基本面兌現速度 = 倍數壓縮速度，股價橫盤或溫和回測）","columns":{"2Y 驗證點":"2026H2 股價回測 $15-20 區間（從 $29.25 −30% 至 −48%），對應 P/S 50-70x","5Y 驗證點":"2027-28 隨 FY27/28 revenue 兌現至 $72M/$120M，P/S 自然壓至 30-50x 區","10Y 驗證點":"2030 估值 reset 至 $200M+ revenue × 15-20x P/S = 市值 $3-4B（−40-55%）","具體數字門檻":"P/S 在 FY+2 = 30x 是 NVTS pure-play GaN 溢價合理上緣；&gt; 50x 需要敘事繼續放大、&gt; 80x 不可持續","信息來源":"POWI / WOLF / IFNNY 同業比較 + Navitas 自身 IPO 後估值區間","漂移觸發條件":"連 2 季 P/S（FY+2 基礎）維持 &gt; 80x → 估值倍數脫鉤；單季回測 &lt; 50x → 倍數壓縮如預期"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Q2/Q3 2026 high-power 業務 ramp 不如預期（client design-in 延後、distributor 庫存堆積）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Q2 revenue 實際 vs guide 中緣 $10M；high-power 占比；distributor inventory days","警戒閾值":"單季 miss &gt; 10% + 連 2 季 high-power 占比未升 &gt; 5%pt → R1 觸發"}},{"id":"R2","text":"POWI / Infineon / Innoscience 在 NVIDIA 800V HVDC 中拿走更大 BoM share，NVTS 被擠到 &lt; 15%","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"NVIDIA Rubin Ultra 量產時 NVTS 公告 design win 數量、shipped units、ASP 揭露；POWI 揭露 NVIDIA data center revenue","警戒閾值":"2027H1 Kyber 量產確認 NVTS share &lt; 15% → R2 觸發；POWI 公告 NVIDIA AI revenue &gt; $200M / 年 → R2 觸發"}},{"id":"R3","text":"800V HVDC 範式被 ±400V bipolar（Vicor 主推）或其他替代架構分流，hyperscaler 標準分裂","columns":{"對應假設":"H1 + H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"OCP（Open Compute Project）標準制定動向；Meta / Microsoft / Google 對 ±400V vs 800V 表態；NVIDIA + AMD 對立路線","警戒閾值":"2028 之前若 OCP 接受多架構並存且 hyperscaler &gt; 1 家公開選 ±400V → R3 進入觀察；&gt; 50% 機率時才大動作 — 短期單一公告不觸發"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"X","val":"🔴","ma":"🟠","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":29.25,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名中除程式欄以外的每一個**（程式稍後才會算的 p_bull_pct／p_bear_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；`asym_ratio`／`ev5y_pct`／`irr_base_pct`／`bull_5y_price`／`bear_5y_price` 的漂移歸因同樣由程式生成條目（程式用本次情境、依先換情境後換股價的順序拆量），你不要為它們開條目；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 `competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 `fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。

---

## 尾段：scenario_inputs 形狀與回覆格式

**本檔 FY1 共識 EPS ≤ 0（虧損），程式已把估值口徑定為 `sales_multiple`：情境樹用營收路徑 × 終端 EV/S，不用 EPS × 本益比。** 口徑由程式決定，你填什麼 `valuation_basis` 都會被覆寫。`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：

```json
{
  "valuation_basis": "sales_multiple",
  "terminal_label": "FY20XXE",
  "start": {"rev": <FY+1 共識營收，百萬，報告幣別；抄事實表 f_rev_consensus_fy1_m>, "ev_s": <目前 EV/S（EV÷FY+1 共識營收）；抄事實表 f_ev_s_fwd>, "basis": "<起點口徑一句話：營收取哪一年、EV/S 的分母是哪一年，須與終端 EV/S 分母同口徑>"},
  "rev": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "ev_s": {"bull": <終端 EV/S>, "base": <倍數>, "bear": <倍數>},
  "net_debt_y5": {"bull": <終端年淨負債，百萬，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "shares_y5": {"bull": <終端年稀釋股數，百萬股，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>
}
```

（**不要**填 `eps`、`pe`、`second_stage`、`peer_max_fpe`；`eps_meta` 仍照常寫共識三年 EPS。現價、目前淨負債（`f_net_debt_m`）、目前股數（`f_shares_diluted_m`）由程式從事實表帶進 `scenario.json`。）

**終端每股價＝max(0, (終端營收 × 終端 EV/S − 終端淨負債) ÷ 終端股數)**，股權價值為負就是 0（Bear 情境債務吃光股權時，要如實寫出讓它歸零，不要為了好看調高倍數）。`net_debt_y5` 要反映該情境下的現金流與融資（虧損公司的淨負債通常會變大，不是沿用目前值）；`shares_y5` 要反映該情境下的增資與稀釋；兩者填 null 才是沿用目前值，不是預設答案。`ev_s` 是終端年 EV ÷ 終端年營收，須與 `start.ev_s` 同口徑（前瞻 vs trailing 不可混）。

`dd_scenario.py` 會擋：`rev` 各路徑長度 ≠ 5、終端營收非 Bear＜Base＜Bull、三機率加總 ≠ 100、`p.bear` ＜ 20、`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘：Bull 前兩年營收不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一情境終點跌幅。機率與路徑是你的判斷，算術（IRR／倍數貢獻／AR）全由腳本算，不要自己填結果欄。

**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, separators=(",", ":"))` 等效格式），陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 `scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，由腳本從 scenario 機械算回。

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVTS_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
