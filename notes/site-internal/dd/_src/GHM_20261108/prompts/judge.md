你是 stock-analyst **v20 判斷 agent**，標的 GHM（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GHM","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":69.76,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 ir.grahamcorp.com Q2 FY27 press release"},"note":"未取得可驗證的共識數字，省略"},{"id":"f_kpi1_gaap","label":"毛利率（GAAP）","value":28.2,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q2 FY27"},"note":"n/a"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":5.83,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M（利益率 8.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q2 FY27"},"note":"n/a"},{"id":"f_kpi3_non_gaap","label":"Non-GAAP 營業利益／利益率","value":null,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"公司未揭露；改列 Adjusted EBITDA 10.30M／14.8%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q2 FY27（Adjusted EBITDA 調節表；公司不報 adjusted operating income）"},"note":"n/a","needs_sonnet":true},{"id":"f_kpi6_fy2027_2026_11_05","label":"管理層 FY2027 指引（2026-11-05 更新）","value":"營收 285–295M（維持）；Adj. EBITDA 35–40M（維持）；毛利率 25.0–26.0%（由 24.5–25.5% 上調）","period":"Q2 FY2027（公告於 2026-11-05）","unit":"USD M／%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2027（公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q2 FY27"},"note":"FY1 營收共識 290.82M（yfinance，位於指引中點附近）"},{"id":"f_kpi7_backlog","label":"Backlog","value":561.3,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q2 FY27"},"note":"n/a"},{"id":"f_kpi8_book_to_bill","label":"Book-to-bill／訂單","value":1.1,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"x（訂單 73.7M）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q2 FY27"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ghm_gross_margin_pct","label":"GHM 毛利率","value":23.29,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GHM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ghm_operating_margin_pct","label":"GHM 營業利益率","value":5.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GHM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ghm_fcf_margin_pct","label":"GHM FCF 利潤率","value":-2.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GHM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cw_gross_margin_pct","label":"CW 毛利率","value":38.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cw_operating_margin_pct","label":"CW 營業利益率","value":19.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cw_fcf_margin_pct","label":"CW FCF 利潤率","value":15.78,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_ese_gross_margin_pct","label":"ESE 毛利率","value":42.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ESE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ese_operating_margin_pct","label":"ESE 營業利益率","value":15.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ESE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ese_fcf_margin_pct","label":"ESE FCF 利潤率","value":15.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ESE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dco_gross_margin_pct","label":"DCO 毛利率","value":27.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DCO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dco_operating_margin_pct","label":"DCO 營業利益率","value":10.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DCO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_dco_fcf_margin_pct","label":"DCO FCF 利潤率","value":-1.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DCO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_ocf_capex","label":"自由現金流（OCF 減 capex，推算，公司未報）","value":44.5,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q2 FY27：OCF 46.7M、capex 2.2M；FCF 為自行相減"},"note":"n/a"},{"id":"f_kpi5_sbc_equity_based_compens","label":"SBC（equity-based compensation）占營收","value":1.12,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"%（0.782M；占 GAAP 營業利益 13.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 Q2 FY27 Adjusted EBITDA 調節表"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":78.02,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-20.54,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":54.81,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.81 → 1.81）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.28 → 2.28）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.81,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.28,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.12,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.79 → 1.81（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":67.84,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝88.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":88.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.46,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝91.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":91.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.21,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝81.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":81.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":43.1,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.81，分子＝快照價 78.02","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-65.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 6.43、現金 71.43（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":11.74,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":850.8,"period":"2026-11-08","unit":"USD m","basis":"市值 915.8 ＋ 淨負債 -65.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":290.82,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（6 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":322.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（6 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.93,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 78.02 / W52 86.01 / W104 65.16 / W250 36.75 / W250 13週斜率 2.58%"},{"id":"f_ma_w52","label":"52 週均線","value":86.01,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":65.16,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":36.75,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.58,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K 風險因子自述：公司在部分國防產品的市占提升，使部分對手處於不利份額位置；對手可能反應，客戶也可能擔憂供應商集中。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"In addition, our increased market share has caused an adverse share position for some of our competitors for these products. Competitor response to our market penetration is possible. Our customers may also raise concerns about their supplier concentration issues and the risk exposure related to this concentration.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：公司在所有市場面臨競爭，部分對手資源更大或因地理／匯率具成本優勢，可能因低成本對手而失去份額、價格轉變。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"Certain competitors may also have a cost advantage compared to us due to their geography or changes in relative currency values and may compete against us based on price.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出主要對手：國防含 DC Fabricators、PCC、Triumph Aerospace、Xylem；能源與製程含 Croll Reynolds、Gardner Denver、GEA Wiegand 等；未見搜尋到具名新進入者。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"Defense DC Fabricators; PCC; Triumph Aerospace; Xylem Energy & Process Croll Reynolds Company, Inc.; Gardner Denver, Inc.; GEA Wiegand GmbH; Korting Hannover AG; Schutte & Koerting","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2026 10-K 風險因子載有客戶集中與海軍曝險揭露，未見第二供應商或 in-house 的具體說明","source":"GRAHAM CORP Form 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/0000716314/000119312526260688/ghm-20260331.htm","excerpt":"Navy that have a long conversion cycle (up to six years). Outlook We are providing the following fiscal 2027 outlook ($ in thousands): Fiscal 2027 Net Sales","as_of":"2026-05-30","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 前十大客戶占合併營收 60%（FY2025 60%、FY2024 57%），公司預期少數客戶仍將占大部分營收；FY2026 有兩家客戶各占逾 10%。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"sales to our top ten customers, who can vary each year, accounted for 60%, 60%, and 57% of consolidated net sales in fiscal 2026, fiscal 2025, and fiscal 2024, respectively. We expect that a limited number of customers will continue to represent a substantial portion of our sales for the foreseeable future.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"國防占營收 60%（FY2025 58%、FY2024 54%），分散於多個承包商但最終客戶同為美國海軍，公司自述有資金中斷風險。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"While these projects are spread across multiple contractors and programs, the end customer for these projects, primarily the U.S. Navy, is the same. This concentration of business could add additional risk to us should there be a disruption, short or long term, in the funding for these projects or our participation in these Defense programs.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K 附註：應收帳款信用集中度有限，2026/2025 年 3 月底無重大信用集中。","source":"SEC EDGAR 10-K FY2026 Note 10","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"Concentrations of credit risk with respect to trade accounts receivable are limited due to the large number of customers comprising the Company's customer base and their geographic dispersion. At March 31, 2026 and 2025, the Company had no significant concentrations of credit risk.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"GHM FY2026 結束時訂單 $359M、積壓訂單 $533M 創高；FY2027 營收指引 $285–295M；約 35–40% 積壓預期 12 個月內轉為營收（二手摘要）","source":"Barchart/Nasdaq, Graham Q4 earnings call highlights","url":"https://www.barchart.com/story/news/2383495/graham-q4-earnings-call-highlights","excerpt":null,"as_of":"2026-05-20","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY2027 Q1 訂單 $95.9M、book-to-bill 1.3x、積壓 $557.2M 創高；約 84% 積壓屬國防（截至 2026-06-30）；新建 Arvada 30,000 平方呎廠房擴產，FY2027 capex $18–22M","source":"Barchart, Graham Corporation Reports First Quarter Fiscal 2027 Results","url":"https://www.barchart.com/story/news/3686680/graham-corporation-reports-first-quarter-fiscal-2027-results","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"競爭對手近期獲 General Dynamics 與 Huntington Ingalls 獎項，管理層表示有信心；Batavia 新 ERP 於 FY27 Q3 上線有暫時性生產／開票中斷風險（二手摘要）","source":"Nasdaq, Graham Q1 earnings call highlights","url":"https://www.nasdaq.com/articles/graham-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"GIPL（印度子公司）吹哨者調查已自願通報印度主管機關、美國 DOJ 與 SEC，公司持續配合；公司認為剩餘影響不重大。屬反貪腐性質，非反壟斷。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"We have voluntarily reported the findings of our investigation to the appropriate authorities in India, the U.S. Department of Justice, and the SEC and will continue to cooperate with those authorities.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 法規段僅將反托拉斯列為一般適用法規，搜尋未發現針對 GHM 的反壟斷調查、拆分風險或產業特定新規。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"These laws, rules and regulations cover several diverse areas including government contracting rules, environmental matters, employee health and safety, data and privacy protection, foreign anti-corruption practices, anti-bribery, and anti-trust provisions.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 10-K：關稅使毛利增加約 $1,000 千美元的額外成本（相對 FY2025）；毛利率 23.5%，下滑主因為產品組合（國防比重較高）。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"The impact of increased tariffs for fiscal 2026 was approximately an incremental $1,000 compared to fiscal 2025.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"公司稱訂單到手才下原料採購以鎖價，且大部分國際銷售在當地製造，以隔離關稅影響。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"we place orders for raw materials when the purchase orders are received from the customer to lock-in raw material pricing and manufacture a large portion of our international sales in-country which helps isolate us from the impacts of tariffs.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"風險因子：關稅可能影響電子元件、高階鋼材等原料成本，並使產品對海外客戶較不具吸引力。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"Tariffs affecting our products and product components, including raw materials we use, particularly electronic components, high-end steel and steel related products, may add significant costs to us and make our products more expensive.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"受 ITAR、EAR、OFAC 規範；FY2026 15% 營收來自美國以外客戶，在中國與印度設有銷售與工程支援辦公室。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"For fiscal 2026, 15% of our revenue was from customers located outside of the U.S. Moreover, through our subsidiaries, we maintain sales and engineering support offices in China and India.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"管理層對關稅衝擊的估計逐季上調：FY2026 全年增量約 $1.0–1.5 百萬美元（Q3 財報）；Q1 時稱不重大。","source":"Barchart/BusinessWire: Graham Corporation Reports Third Quarter Fiscal 2026 Results","url":"https://www.barchart.com/story/news/67667/graham-corporation-reports-third-quarter-fiscal-2026-results","excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2026 10-K 風險因素提到中國、加拿大、歐盟、印度、墨西哥已提議或課徵對美出口報復性關稅；公司在中國設銷售子公司、印度設銷售與市場開發辦公室（搜尋摘要來自 10-K 歷年版本，非逐字）。","source":"Graham Corp Form 10-K FY2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0000716314/000119312526260688/ghm-20260331.htm","excerpt":null,"as_of":"2026-05-31","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"10-K 原料供應來自多元國內外供應商","source":"Graham Corp Form 10-K FY2022","url":"https://www.sec.gov/Archives/edgar/data/716314/000095017022011403/ghm-20220331.htm","excerpt":null,"as_of":"2022-05-31","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27 Q1（截至2026-06-30）：Defense 銷售 +40%（+$11.8M）、Energy & Process +5%；期末積壓訂單創高 $557.2M（+15%），其中約84%為國防","source":"Graham Corporation Reports First Quarter Fiscal 2027 Results (Business Wire/Barchart, 2026-08-05)","url":"https://www.barchart.com/story/news/3686680/graham-corporation-reports-first-quarter-fiscal-2027-results","excerpt":"Backlog at quarter end was a record $557.2 million, a 15% increase over the prior-year period, driven by strong bookings in the Defense and Space markets, and contributions from the FlackTek acquisition.","as_of":"2026-08-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"FY27 營收指引 $285–295M 維持；Q1 毛利率降至25.0%（前年26.5%），公司歸因於較高比重的低毛利國防銷售","source":"Graham Corporation Reports First Quarter Fiscal 2027 Results (Business Wire/Barchart, 2026-08-05)","url":"https://www.barchart.com/story/news/3686680/graham-corporation-reports-first-quarter-fiscal-2027-results","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q2（截至2025-09-30）：營收 +23% 至 $66.0M，毛利率降220bp至21.7%；積壓訂單 $500.1M，約85%為國防；新增 Space 訂單約$14.8M","source":"Graham Corporation Reports Second Quarter Fiscal 2026 Results (Business Wire, 2025-11-07)","url":"https://www.businesswire.com/news/home/20251107661669/en","excerpt":null,"as_of":"2025-11-07","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27 Q1 銷售與訂單細節","source":"Business Wire FY27 Q1 release","url":"https://secure.businesswire.com/news/home/20260805783838/en/Graham-Corporation-Reports-First-Quarter-Fiscal-2027-Results","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子載明：競爭者可能開發性能更佳的新技術，若 Graham 跟不上，產品可能過時、需求下降、失去份額或面臨價格壓力（該段寫的是 bladeless mixer 產業）。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"Competitors may develop new technologies or enhanced product features that outperform or otherwise diminish the attractiveness of our current offerings.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 載明：公司計畫把非客戶出資的新產品研發提高到營收 1%～2%，目的包括維持技術競爭優勢；FY2026 新產品研發 $1,204 千美元（總研發 $6,354 千美元）。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"Going forward we expect our new product development R&D spend, that is not customer funded, to gradually increase to 1% to 2% of revenue","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"2024 年 10 月 Graham 推出 NextGen 蒸汽噴射器噴嘴，研發測試顯示比標準噴嘴節能 5%～10%（公司自述）；搜尋未見任何取代蒸汽噴射器的替代技術報導。","source":"Digital Refining: Graham Corporation launches NextGen steam ejector nozzle","url":"https://www.digitalrefining.com/news/1008080/graham-corporation-launches-nextgen-steam-ejector-nozzle","excerpt":null,"as_of":"2024-10-15","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"+","claim":"NextGen 噴嘴比標準噴嘴節能 5%～10%","source":"Business Wire Graham NextGen nozzle release","url":"https://www.businesswire.com/news/home/20241015763765/en","excerpt":null,"as_of":"2024-10-15","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FlackTek 收購（2026-01）帶入國際經銷網路與耗材型營收，管理層稱可拓寬銷售通路；搜尋未見 Graham 自身通路結構性轉變（訂閱／D2C／平台化）的來源","source":"Panabee／quantisnow 對 GHM FY2026 及 FlackTek 收購之報導摘要","url":"https://www.panabee.com/news/graham-corporation-earnings-2026-annual","excerpt":"FlackTek maintains a strong domestic manufacturing footprint complemented by an established international distribution network.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Investing.com 頁面列示 12 個月平均目標價約 125.60 美元，高 135、低 115；含 Oppenheimer 115 美元（2026-08-10）。分布窄，覆蓋家數少。","source":"Investing.com Graham Corp (GHM)","url":"https://uk.investing.com/equities/graham-corp","excerpt":"The average 12-month price target for Graham is 125.60 USD, with a high estimate of 135 USD and a low estimate of 115 USD.","as_of":"2026-08-10","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Fintel 平均一年目標價修正為 102.34 美元，較 2026-02-01 的 85.00 美元上調 20.40%（Fintel 頁面當時日期未載明）。","source":"Fintel GHM","url":"https://fintel.io/s/us/ghm","excerpt":"The average one-year price target for Graham (NYSE:GHM) has been revised to $102.34 / share. This is an increase of 20.40% from the prior estimate of $85.00 dated February 1, 2026.","as_of":"2026-04-20","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 2026-04 共識評級 Moderate Buy，六家機構（2 持有、3 買進、1 強力買進），平均目標價約 81.67 美元；各來源目標價時點不一致，彼此差距大。","source":"MarketBeat 2026-04-26","url":"https://www.marketbeat.com/instant-alerts/graham-corporation-nyseghm-receives-average-recommendation-of-moderate-buy-from-analysts-2026-04-26/","excerpt":null,"as_of":"2026-04-26","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"公司於 2026-08-06 Q1 FY2027 重申全年 FY2027 guidance（營收 2.85–2.95 億美元、調整後 EBITDA 3,500–4,000 萬美元）；Q1 營收 7,130 萬美元年增 29%，毛利率 25.0% 低於去年同期 26.5%，因國防占比較高。未見下修。","source":"Graham Corporation Q1 FY2027 release via Channelchek","url":"https://dashboard.channelchek.com/release-graham-corporation-reports-first-quarter-fiscal-2027-results/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"RTTNews 報導 Graham 看 FY27 營收成長（guidance 更新）","source":"RTTNews","url":"https://www.rttnews.com/3658633/graham-sees-revenue-growth-in-fy27-update.aspx","excerpt":"(GHM) initiated its revenue guidance for the full-year 2027 between $285 million and $295 million. \"As we enter fiscal 2027, we remain focused on disciplined execution, integrating FlackTek, and continuing to invest in our people, processes, and technology to enable future growth and","as_of":"2026-06-08","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-01-26 Graham 公告收購 FlackTek Manufacturing 與 FlackTek Sales（先進混合與材料處理）；1月23日同時把 Wells Fargo 循環信貸額度由 $50M 增至 $80M。","source":"SEC EDGAR 8-K Item 1.01/7.01 (2026-01-26)","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526021705/d47192d8k.htm","excerpt":"On January 26, 2026, the Company issued a press release announcing the acquisition of FlackTek Manufacturing, LLC and FlackTek Sales, LLC, pioneers in advanced mixing and material processing solutions.","as_of":"2026-01-26","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-04-14 Graham 與 T. Rowe Price 旗下帳戶簽 PIPE：以每股 $83.36 售出 599,808 股，總額 $50M。","source":"SEC EDGAR 8-K Item 1.01 (2026-04-15)","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526155977/d147885d8k.htm","excerpt":"the Company agreed to sell an aggregate of 599,808 shares of its common stock, par value $0.10 per share (the “Shares”) for $83.36 per share for aggregate gross proceeds of $50 million (the “PIPE”).","as_of":"2026-04-15","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"10-K 披露 Graham 為多起石棉暴露人身傷害訴訟的共同被告，公司認為不會有重大不利影響；為既有長期訴訟，非集體訴訟。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"We believe that the resolution of these asbestos-related lawsuits will not have a material adverse effect on our financial position or results of 35 operations.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-01 收購 FlackTek Manufacturing/Sales。","source":"SEC EDGAR 8-K (2026-01-26)","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526021705/d47192d8k.htm","excerpt":"On January 26, 2026, the Company issued a press release announcing the acquisition of FlackTek Manufacturing, LLC and FlackTek Sales, LLC, pioneers in advanced mixing and material processing solutions.","as_of":"2026-01-26","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"僅有石棉人身傷害訴訟（共同被告），公司預期無重大不利影響；搜尋未見證券集體訴訟。","source":"SEC EDGAR 10-K FY2026 Item 7","url":"https://www.sec.gov/Archives/edgar/data/716314/000119312526260688/ghm-20260331.htm","excerpt":"We believe that the resolution of these asbestos-related lawsuits will not have a material adverse effect on our financial position or results of 35 operations.","as_of":"2026-06-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GHM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.29,"operating_margin_pct":5.44,"fcf_margin_pct":-2.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GHM","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.07,"operating_margin_pct":19.06,"fcf_margin_pct":15.78,"rd_intensity_pct":2.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CW","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ESE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":42.01,"operating_margin_pct":15.66,"fcf_margin_pct":15.23,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ESE","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"DCO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":27.9,"operating_margin_pct":10.51,"fcf_margin_pct":-1.55,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DCO","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"GHM"},"financial_history":{"ticker":"GHM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-03-31","revenue":157118000.0,"revenue_yoy_pct":null,"gross_margin_pct":16.17,"operating_margin_pct":0.8,"net_income":367000.0,"diluted_eps":-0.05,"free_cash_flow":10165000.0,"fcf_margin_pct":6.47,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-03-31","revenue":185533000.0,"revenue_yoy_pct":18.09,"gross_margin_pct":21.87,"operating_margin_pct":3.73,"net_income":4556000.0,"diluted_eps":0.42,"free_cash_flow":18894000.0,"fcf_margin_pct":10.18,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-03-31","revenue":209896000.0,"revenue_yoy_pct":13.13,"gross_margin_pct":25.18,"operating_margin_pct":7.24,"net_income":12230000.0,"diluted_eps":1.11,"free_cash_flow":5359000.0,"fcf_margin_pct":2.55,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-03-31","revenue":245293000.0,"revenue_yoy_pct":16.86,"gross_margin_pct":23.54,"operating_margin_pct":6.12,"net_income":12500000.0,"diluted_eps":1.12,"free_cash_flow":-121000.0,"fcf_margin_pct":-0.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GHM/GHM_Q2_2027_Earnings_Call_20261105.md）

# Q2 2027 Earnings Call
**Graham Corporation** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Greetings, and welcome to the Graham Corporation Fiscal Second Quarter 2027 Earnings Call. [Operator Instructions] As a reminder, this conference is being recorded. It is now my pleasure to introduce your host, Tom Cook, Investor Relations. Thank you. You may begin.

**Tom Cook** (Executives):
Thank you, Sachi, and good morning, everyone. Welcome to Graham's Second Quarter Fiscal 2027 Earnings Call. With me on the call today are Matt Malone, President and CEO; and Chris Thome, Chief Financial Officer. This morning, we released our second quarter fiscal 2027 financial results. Our earnings release and accompanying presentation to today's call are available on our website at ir.grahamcorp.com. 
You should be aware that we may make forward-looking statements during the formal discussion as well as during the Q&A session. These statements apply to future events that are subject to risks and uncertainties as well as other factors that could cause actual results to differ materially from what is stated here today. These risks and uncertainties and other factors are provided in the earnings release as well as with other documents that are filed by the company with the Securities and Exchange Commission. You can find these documents on our website or at sec.gov. 
During today's call, we will also discuss non-GAAP financial measures. We believe these will be useful in evaluating our performance. However, you should not consider the presentation of this additional information in isolation or as a substitute for results prepared in accordance with GAAP. We have provided reconciliations of non-GAAP measures with comparable GAAP measures in the tables that accompany today's release and slides. We also use key performance indicators to help gauge the progress and performance of the company. These key performance metrics are ROIC, orders, backlog and book-to-bill ratio. These are operational measures and a quantitative reconciliation of each is not required or provided. You can find a disclaimer regarding our use of KPIs at the back of today's presentation. So with that, if you'll please advance to Slide 3, I'll turn the call over to Matt to begin. Matt?

**Matthew Malone** (Executives):
Thank you, Tom, and good morning, everyone. We appreciate you joining us to review our second quarter fiscal 2027 results. We have continued to execute on our strategic priorities with growth in Defense and space, significant improvement in profitability, another quarter of record backlog and continued momentum in our FlackTekbusiness. Second quarter revenue was $69.8 million, up 6% from the prior year. Adjusted EBITDA increased 64% to $10.3 million. representing a margin of 14.8%. Orders totaled $73.7 million and backlog reached a record $561 million. This performance reflects the sustained demand for our mission-critical technologies, the contributions of FlackTek and better execution across our entire business platform. 
We are excited by the improvement in profitability while we continue to invest in our people, processes and technology. Operational improvements on new and existing programs, a more favorable mix in defense and space work and the addition of FlackTek are all additive to our results. Program mix and the timing of material receipts also affect our margins, and Chris will discuss those factors in more detail in a few minutes. The investments we have made across our organization to support capacity, automation, testing and systems are increasingly supporting the business. FlackTek's integration is translating into stronger results, and we completed our first customer test at our new cryogenic test facility this quarter. 
We also broke ground on our new Arvada facility in Colorado to support our continued growth. Based on our first half performance and expectations for the remainder of the year, we are reaffirming our fiscal 2027 revenue and adjusted EBITDA guidance. We have also increased our gross margin outlook to reflect better execution and mix. We remain focused on our 3-year framework that we outlined at our June Investor Day, targeting 8% to 10% organic revenue growth and adjusted EBITDA margins of 14% to 16% by fiscal 2029. This quarter demonstrates progress towards those objectives as we work towards becoming a top quartile performer over time. 
Turning to our markets on Slide 4 and starting with defense. Revenue increased 12% from the prior year quarter and represented 66% of total sales. Growth reflected project milestone timing, new programs, expansion of existing programs and the addition of FlackTek, partially offset by the approximately $10 million lower in material receipts than the prior year's quarter. Defense orders were up $41.8 million and defense backlog increased 10% from a year ago. Our primary naval positions include the Columbia and Virginia-class submarine programs and the Mark 48 Mod 7 heavyweight torpedo, which are both bipartisan supported. We also supply the Mark 19 Mod 2 air turbine pump assemblies to support submarine fleet spares. These positions give us exposure to both new production and the reoccurring requirements of the installed fleet. 
Additionally, our thermal management and cooling technologies position us well for growth in radar and directed energy platforms, where we are seeing continued progress from development towards production. These systems are becoming increasingly more important as war is reshaped by proliferation of drones and other new technologies. From a margin perspective, we are seeing the benefits of operational excellence and a more profitable mix of work. Better execution on existing programs, together with pricing discipline on new opportunities supports our long-term margin goals. 
Before turning to space, I want to spend a minute discussing the defense budget in framing Graham's interplay. The vast majority of our programs we support have requirements that extend well beyond any individual budget or political cycle. Shipbuilding, for example, is a multi-decade cycle with strong bipartisan support and one where America's adversaries are making strides ahead of the United States. We have appropriations and while funding timing still matters, the multiyear nature of these programs provides visibility as we plan capacity and investments alongside our customers. Our defense backlog is 85% funded, and we are excited about the continued momentum. 
Moving to space. Growth continues to build. Revenue increased 59% from the prior year quarter, reflecting commercialization, higher launch cadences and the ramp of existing programs and contributions from FlackTek. Orders were $10.6 million, representing a book-to-bill ratio of 1.7x. For the first half, space orders totaled $25 million or 2x sales, and the space backlog was up 108% from a year ago. As customers advance their programs, demand is growing for turbomachinery, cryogenic systems, pumps and related technologies that we provide. FlackTek adds advanced materials processing capabilities that broaden our participation in space and defense applications, including missiles. 
Our testing investments are also strengthening our offering. We successfully completed the first customer test at our new cryogenic facility in Florida this quarter. Together with our liquid nitrogen testing capabilities in Colorado, this allows us to validate performance under demanding conditions and deliver fully tested solutions. That is valuable to our customers as they work through qualification and scale production. 
Turning to Energy and Process. Revenue declined 17% from prior year quarter. Large capital projects remained soft amid global uncertainty and sales to customers outside the United States were lower. Growth in the new energy and contributions from FlackTek partially offset those pressures, and we continue to manage the business with that large project environment in mind. Aftermarket remains strong and important opportunity across Energy and Process and defense. Combined, aftermarket sales were $8.6 million, down 3% from prior quarter, while orders increased 91% to $18.3 million. Sales remained a high level and the strength in our bookings supports future activity. 
With a more than $1 billion installed base of Graham equipment around the world, we have a substantial group of customers who need ongoing maintenance, replacement parts and performance improvements. Expanding that life cycle remains a key priority. In new energy, we continue to see opportunities in development programs, supporting micro reactors, small modular reactors and other technologies. These markets are still developing, and we will continue to pursue opportunities where our engineering capabilities can solve specific customer needs. 
Turning now to FlackTek, which I want to highlight and I am very excited about. The integration has gone exceptionally well, and that is showing up in the business results. Revenue increased to $9.5 million from $6.6 million in the first quarter, and the business is contributing margins that are accretive to the portfolio. A key focus has been sales excellence. The team is following a more rigorous process to help customers understand the technology, validate its application and move towards an order. We are seeing the time from request for quotation to order shorten alongside greater demand for larger machines and higher-value purchase orders. The key message is the shift towards production. As customers move from evaluating the technology to using it in production, the scale and the opportunity expands. 
That is why we remain particularly excited about the mega platform and the potential to introduce FlackTek's advanced materials processing technologies to the world. FlackTek is also a useful example of how we approach M&A. We look for differentiated engineer-led businesses with proprietary technology that can expand our addressable markets and create opportunities for profitable growth. Alongside our investments in technologies such as XDOT, our focus is on turning technical differentiation into commercial results. 
Turning to operational excellence on Slide 5. Our focus continues to move from not only building capabilities, but to getting more out of those capabilities as well. The Navy and X-ray facilities in Batavia, automated welding, expanded assembly and testing in Colorado and the cryogenic testing facility in Florida give us a stronger base from which to serve our customers. We are also continuing to modernize our systems through our ERP initiatives. The next step is to translate those capabilities into higher utilization, shorten cycle times and improve throughput. The operational improvements contributing to this quarter's gross margin are encouraging, and we see further opportunity as we repeat that execution across more programs. 
During the quarter, we broke ground on our new 30,000 square foot facility at our Arvada campus. This expansion is intended to support increasing demand and provide additional capacity for our turbomachinery applications. It is an investment in our ability to execute the work ahead of us and support future growth. We continue to evaluate special projects, special capital projects against our 20% ROIC hurdle rate. Our focus is on investments that expand capacity, improve productivity and strengthen differentiated capabilities. 
The change in our capital expenditure outlook reflects the timing of major projects, which Chris will discuss in more detail. These investments support the execution and visibility of our backlog, which increased 12% from a year ago and represents our seventh consecutive quarter of record backlog. Approximately 83% is in defense with many programs extending over multiple years. Our year-to-date book-to-bill is of 1.2x, together with our active pipeline, supports our confidence in the fiscal 2027 outlook and our longer-term framework. 
As we move into the second half, we will build on these opportunities in space, defense and expand aftermarket support, commercialize our proprietary technologies and improve profitability through disciplined pricing. We also remain selective as we pursue acquisitions that complement our organic growth strategy and offer attractive returns. The foundation we have built is contributing more meaningful to our results. 
We are pleased with our progress through the first half of the fiscal year and recognize there is more work ahead as we continue improving execution and creating value for our customers and shareholders. I want to thank every one of our employees for their continued commitment to our customers and seeing our vision come to life. With that, I'll turn the call over to Chris for a detailed review of our financial results and outlook. Chris?

**Christopher Thome** (Executives):
Thanks, Matt, and good morning, everyone. Turning to our second quarter results, starting on Slide 6. We delivered another solid quarter with continued growth in Defense and Space, meaningful gross margin expansion and strong cash generation. Our results reflect the benefits of operational execution, the investments we have made to support our long-term growth strategy and the acquisition of FlackTek. Second quarter revenue increased 6% to $69.8 million compared with $66 million in the prior year period. FlackTek contributed $9.5 million of revenue during the quarter. 
Defense revenue increased 12% year-over-year, primarily driven by the timing of project milestones, new programs and continued expansion of existing programs, along with the contributions from FlackTek. This growth was partially offset by approximately $10 million of lower material receipts compared with the extraordinarily high level of the prior year quarter. Defense represented 66% of quarterly sales. Base revenue increased 59% year-over-year and reflects the commercialization, accelerated launch cadences and the ramp of existing programs as well as the addition of FlackTek. 
Within Energy and Process, revenue decreased 17% from the prior year period, reflecting softness in large capital project investments amid geopolitical uncertainty and lower sales to customers outside the United States, partially offset by growth in new energy and FlackTek. Aftermarket sales across Energy and Process and Defense were $8.6 million, down 3% year-over-year but remained at high levels. 
Turning to Slide 7. Gross profit increased 38% to $19.7 million compared with $14.3 million in the prior year period. Our gross margin expanded 650 basis points to 28.2% compared with 21.7% a year ago. This increase reflects operational improvements from the investments we have made, contributions from FlackTek and a more favorable sales mix, particularly within Space and Defense. The comparison also benefited from lower material receipts in the second quarter of fiscal '27 as compared to the prior year, which had lower margins. 
Moving to Slide 8. Selling, general and administrative expenses, including intangible amortization, increased $3.4 million or 34% compared with the prior year period. Approximately $2.3 million of the increase reflected incremental SG&A associated with FlackTek and acquisition and integration expenses contributed $0.7 million to the increase. We also continue to invest in our people, our processes and our technology. These investments are expected to total approximately $2.5 million of incremental costs in fiscal 2027 to support future growth and accelerate commercialization. 
These increases were partially offset by the end of the Barber-Nichols performance bonus in fiscal 2026. The prior year quarter included $1.1 million of expense related to that bonus with no corresponding expense in the current quarter. Net income increased 50% to $4.6 million compared with $3.1 million in the prior year quarter. Net income per diluted share increased 39% to $0.39 compared with $0.28 a year ago. 
On an adjusted basis, net income increased 80% to $6.2 million compared with $3.4 million a year ago. Adjusted net income per diluted share increased 68% to $0.52 compared with $0.31 in the prior year quarter. Adjusted EBITDA increased 64% to a record $10.3 million compared with $6.3 million in the prior year period. Adjusted EBITDA margin expanded 530 basis points to 14.8% from 9.5% a year ago. For the first half of fiscal 2027, revenue increased 16% to $141 million and adjusted EBITDA increased 45% to $19.1 million, representing an adjusted EBITDA margin of 13.5%. Overall, we are pleased with the improvement in profitability while continuing to invest to support future growth. 
Turning to Slide 9. Orders totaled $73.7 million during the quarter, resulting in a book-to-bill ratio of 1.1x. For the first 6 months of fiscal 2027, our book-to-bill ratio was 1.2x, and our pipeline of opportunities remains strong. With that said, orders can be lumpy given the nature of our business, particularly large capital projects and multiyear defense orders. Defense orders totaled $41.8 million in the quarter. As Matt discussed earlier, the vast majority of the programs we support have requirements that extend well beyond any individual budget or political cycle. Shipbuilding is a multi-decade cycle with strong bipartisan support.
While funding timing can be impacted, the multiyear nature of these programs provides visibility as we plan capacity and investments alongside our customers. Our defense backlog is 85% funded, and we are excited about the continued momentum. Space orders were $10.6 million, representing a book-to-bill ratio of 1.7x for the quarter. For the first half of fiscal '27, space orders totaled $25 million or 2x sales. Aftermarket orders across Defense and Energy and Process increased 91% to $18.3 million. And finally, our FlackTek business continues to build momentum as book-to-bill was 1.3x for the first half of the year. Backlog reached another record of $561 million, up 12% from the prior year period, marking our seventh consecutive quarter of record backlog. 
Defense backlog increased 10% and space backlog increased 108% from a year ago. Defense represented approximately 83% of backlog at quarter end. We currently expect approximately 30% to 35% of quarter end backlog to convert to revenue within the next 12 months and another 20% to 25% within 1 to 2 years and the remainder beyond 2 years. This backlog continues to provide meaningful visibility into future revenue. 
Turning to Slide 10. Our balance sheet remains strong and provides significant flexibility to support our strategic priorities. Net cash provided by operating activities was $34.1 million for the first 6 months of fiscal 2027. The strong cash generation primarily reflects the timing of accounts receivable collections and customer deposits, along with higher cash net income. Net capital expenditures totaled $4.9 million for the first half of 2027 as we continue to invest in growth and productivity improvements. We ended the quarter with $71 million of cash, no outstanding debt and $75 million available under our revolving credit facility. This financial flexibility positions us to pursue both organic and inorganic growth plans. 
Turning to guidance on Slide 11. We are reaffirming our fiscal 2027 revenue and adjusted EBITDA outlook while updating our gross margin, SG&A and capital expenditure assumptions based on first half performance and our expectations for the remainder of the fiscal year. We continue to expect revenue to be between $285 million and $295 million, representing an increase of 18% over the prior year at the midpoint and our adjusted EBITDA to be between $35 million to $40 million, representing a 44% increase at the midpoint. I should remind everyone that our fiscal third quarter is typically our lowest revenue quarter of the year given the holidays and the dependence of our business on direct labor. 
Before concluding, I would like to remind everyone of the 3-year financial framework that we laid out at our Investor Day in June. Our objectives remain to achieve 8% to 10% organic revenue growth per year and adjusted EBITDA margins of 14% to 16% by fiscal 2029, supported by higher volumes, operational improvements, a more commercial mix and continued leverage from our business investments. That framework implies approximately $340 million to $350 million in revenue and $50 million to $55 million of adjusted EBITDA by fiscal 2029. We remain focused on disciplined capital allocation and targeting returns above our 20% ROIC hurdle rate for our CapEx investments. 
Overall, we are pleased with our results through the first half of fiscal 2027. Our record backlog, continued execution and strong balance sheet position us well to deliver on our full year outlook. With that, operator, we are now ready for questions.

**Operator** (Operator):
[Operator Instructions] The first question is from Russell Stanley from Beacon Securities.

**Russell Stanley** (Analysts):
Maybe just starting with defense orders. Not sure what you can share on this front, but we generally assume, I think, that subs and carriers drive the vast majority of that number along with torpedoes. Wondering what you can say as to the share of defense orders that are from non-Navy applications or opportunities, and just trying to understand what your objectives might be for that component as a share of the order book going forward.

**Christopher Thome** (Executives):
Yes. Thanks, Russ. So again, another great quarter of orders, 1.1 book-to-bill, 1.2 for the full year. So that's impressive given that last year's book-to-bill ratio was 1.5. So we continue to see very good momentum in our backlog and our orders. As mentioned on the call today, -- our aftermarket orders were up 91% for the year. Our orders in space were up very significantly as well. So we're just seeing health growth across all of the portfolios. We did mention we did have some larger Navy orders that are within defense. But as you know, those can be very lumpy in nature.

**Russell Stanley** (Analysts):
Got it. Maybe moving on to Batavia. Just wondering how the facility has performed, the expansion facility, how that's performed relative to expectations. And understanding you just broke ground on the Arvada expansion facility. I'm wondering what your appetite might be for additional expansion facilities in New York.

**Matthew Malone** (Executives):
Yes, Russ, we're definitely seeing the facility come online here. The machining centers are full during day shift, and I say that in reference to where I'm going to go after this. We continue to see the automated welders come online and all of the welding procedures get approved as we move forward. We're approaching a stance of utilization that I'd say is a critical milestone, which means we're reaching targets that are consistent with the other parts of our business. But we're not there. We've got work to go do. 
The RT facility is also online, and we're using it. It's been fantastic. I mean to not have to drive an asset and then go through in an iterative cycle outside of the facility. These things are large. And so it was driving quite a bit of churn into our business. So that investment has paid off on the defense side. And obviously, we can utilize it as well more broadly. The last thing I'll note on the first part of the question is, and we have the opportunity to bring on a second shift if we get to that point. And so it's going well, the Batavia facility. I'm going to stick Batavia for a second. We had mentioned early on that we laid the foundation for 15, building 14 with 2 additional days next door, which are basically exactly the same facility. And we're seeing our backlog continue to expand an opportunity for potential growth and need for growth on this campus as we move forward in the defense sector. 
Moving to the Colorado facility. Yes, that 30,000 square foot facility, we have great confidence. That's really to support our increasing backlog. So it's not so much, I'll say, acceleration of backlog conversion. It really is more out in supporting our future growth. Look, we've already got plans for it, and the team is working out in the facility, laying out the facility. It utilizes the majority of new equipment, so we don't have to relocate from an existing building. So it really -- it's coming along nicely. Ground is being moved and concrete should be poured here in the next few weeks. So progressing.

**Russell Stanley** (Analysts):
That's great. Maybe one more for me, and I'll get back in the queue, just around space. Congrats on the significant growth there. It looks great. A lot of media reports and media attention around the shortage of launch vehicle access. And I'm just wondering if you're seeing that as a potential headwind to your growth here either directly or perhaps a little further down the chain.

**Matthew Malone** (Executives):
Yes. With respect to space, I don't see it as a headwind. I see it more as a continued tailwind. We did not have content on Falcon. So what that allows us to do is continue to expand with that particular customer on their larger asset as well as the assets that will replace the backfill for Falcon. We're seeing continued increase in opportunities, not only with the large rocket -- I'll just say, large rocket customers, but we're also seeing continued interest from the folks that are going to replace that smaller fleet of launch. So I would say that it's a tailwind at this point, which is what's being reflected in our order pipeline, our orders and pipeline.

**Operator** (Operator):
The next question is from Tomo Sano from JPMorgan.

**Tomohiko Sano** (Analysts):
Maybe just on gross margins, which improved significantly to 28.2%, 650 basis points. While your first year full year guidance is 25% to 26%. Could you unpack a little bit about more the margin expansion behind by several factors? And how should we think about the margins going forward into the back half to stay at the high level?

**Christopher Thome** (Executives):
Yes. Thanks for the question. Margins were a little bit higher than our normal run rate for the quarter, and that really was a function of mix as well as higher volumes. But primarily the impact on the margin was lower material receipts. If you recall, in the second quarter of last year, we had about $10 million of extraordinarily high material receipts, which carry with them lower margins. So you have a little bit lower than normal margin in the prior year quarter. We have a little bit higher than normal margin in the current quarter. So we would expect that to more normalize as the year progresses. However, it was ahead of our expectations, which is why we bumped our gross margin guidance by about 50 basis points on the bottom and top end.

**Matthew Malone** (Executives):
Yes. And what we're seeing there is we're seeing improved execution. We're seeing more favorable pricing start to come out of the backlog. So we had talked before about we had to get lower margin jobs out of the backlog, and that process has been unwinding. So it's a little bit of pricing. It's a little bit of improved execution, as though Chris mentioned. And then it's a little bit of just mix versus material receipts.

**Christopher Thome** (Executives):
And more specifically on the mix, right? Space obviously is a lot higher in the current year, which carries with it higher margins, as you know. Additionally, FlackTek was higher this quarter versus the prior year and versus the sequential quarter, and they have a higher-margin business as well. So -- and then one thing that may not be intuitive, within our defense business, we are starting to enter into some higher-margin programs now that we have some of the older orders off the books. So it's not only the mix within the markets, but within defense itself as well.

**Tomohiko Sano** (Analysts):
And then on cash flow, please. Operating cash flow was very strong in Q2, partially reflecting the timing of the receivable collections and customer deposits. But what level of cash generation should we expect in the future quarters? And also just related to that, any comments on M&A pipelines and any areas or comments, appreciated.

**Christopher Thome** (Executives):
Yes, sure. Yes, we had an exceptionally strong cash flow quarter. The teams did a great job on receivables collections. As you know, our business is very cash flow positive as many of our contracts, we were able to bill for the materials ahead of time before we actually have to pay for them. With that said, they can also be very lumpy. We had some receivables push out from the first quarter to the second quarter, which is why the second quarter was so high. 
As you know, we typically like to speak to EBITDA as far as our cash flow generation just because of the lumpiness of our cash and our working capital. We literally can have a $5 million or a $10 million payment that shifts from first quarter or one year to the next, which can kind of skew the results from quarter-to-quarter, which is why we don't provide cash flow guidance and prefer to talk to adjusted EBITDA.

**Matthew Malone** (Executives):
When we look at what we're going to -- I'll just say what we're prioritizing with the cash that we have since we have no debt. First priority is continued investment in our organic growth. We see that as the highest avenue for return for our shareholders. And specifically, we continue to have that 20% hurdle rate. The next in line is M&A or it would be debt, but we don't have any. So the third in line is M&A. And I'll just say pipeline remains full. We're only focused on extremely strategic opportunities that meet the criteria that we've laid out in our investor slide deck. And yes, the pipeline remains full. Conversations are active, and we're excited about potential opportunities on the horizon.

**Operator** (Operator):
[Operator Instructions] The next question is from Robert Brooks from Northland Capital Markets.

**Robert Brooks** (Analysts):
As we think of the increasing needs for more power dense items in high stress environment, that really kind of plays right into your favor and what you guys special, right, specialize in, right? So I was just curious to hear any new orders you'd like to highlight so far in year-to-date for your fiscal '27 that exemplifies that the in action?

**Matthew Malone** (Executives):
Yes. Something that just gets me jazzed. So Bobby, I'll talk through a few examples at a high level. The first Specifically, I want to hone in on even a subsector of nuclear. If you look at micro reactors, so I'm talking containerized reactors that could be deployed at a hyperscale level. And look, like it's not going to happen overnight, but we do still feel optimistic. Barber-Nichols does design some of the most and produce some of the most power dense rotating machines on the market. And with the micro reactor, power density matters. You got to be able to fit the rotating machine that cools the reactor within the shipping container. 
And so we are seeing a number of opportunities that have entered into our design environment and now production environment that meet those needs. And so that's one example in the microreactor space. The next area where we're seeing it is on the defense side. If you look specifically, you hone in and you say radar, we've had some opportunities this year that have converted that have to do with increasing the visibility on the battlefield from a directional radar platform to 360 degrees. And I would specifically say we've talked about that at our Investor Day, but what's happening is it's starting to scale to low rate and now rate production. And so we're starting to see the scaling effect of that. 
Lastly, on the space side, Barber-Nichols has had heritage on the space side with complex rotating machines and more specifically powered dense rotating machines for now 20-plus years. And we're seeing opportunities in space to cool -- I'll say, we have had bookings and opportunities to cool launch vehicles as well as satellite systems as well as astronaut backpacks. So some of that's been a long conversation. Some of it's converted more recently. So I would just say it's an area that power dense electrified rotating machines is the differentiator, and we're seeing it connect with the market need.

**Robert Brooks** (Analysts):
That's really helpful color there. And then just as we like maybe step back or expand the view, obviously, you have a really strong position within like supplying U.S. naval programs. I was just curious to get a sense of maybe what are the key hurdles for you guys to clear to win defense business with American Allied naval programs? Or is that something that's not really on the table and you've kind of focused -- there's better opportunities domestic?

**Matthew Malone** (Executives):
No, it's a great question. We do it today. The nice thing is we do it through the folks that buy it. So our integrator, our prime or upstream is actually the one that then regulates it to where it goes to foreign allies. And so we basically have increased content, use shipbuilding as an example. It gets integrated at a prime and then it could go to AUKUS, which is other different avenues for usage. Other examples of that, we do supply spare parts for different submarine solutions globally. So I would just say it is a part of our business today, and we continue to see opportunity there for growth.

**Robert Brooks** (Analysts):
That's great to hear. And then maybe just the last one for me. So it seems like you're not necessarily capacity constrained today, but then the Arvada expansion is more about better -- not about throughput, but about growing the business in the future. I was a little confused there. I just want to clear up my understanding.

**Matthew Malone** (Executives):
Okay. So think of it this way. We're not capacity constrained today. But when you overlay the backlog that's been growing for seven straight quarters, you get to a situation in the future where the current capacity doesn't meet it. So you essentially have to build ahead to meet the capacity constraints because you can't build a facility overnight. And so it's just leveling up to meet the backlog overlay in our portfolio, and that's what we've done really well for the last number of years.

**Operator** (Operator):
This concludes the question-and-answer session. I would like to turn the floor back over to Matthew Malone for closing comments.

**Matthew Malone** (Executives):
Thank you. Overall, we are pleased with the solid start to the first half of the year. With that said, we recognize there is still significant work ahead, and we remain focused on disciplined execution, profitable growth and getting better every day as we work towards becoming a top quartile performer and creating value for our customers and shareholders. As always, please reach out with any questions. Thank you, everyone, for joining us today and your interest in Graham.

**Operator** (Operator):
This concludes today's teleconference. You may disconnect your lines at this time. Thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GHM_Q1_2027_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：FY27營收財測$285–295M，與上季相同（原話："revenue to be in the range of $285 million to $295 million"）
- 2026-08-06｜CFO｜guidance：FY27財測整體維持不變（原話："which remains unchanged from last quarter"）
- 2026-08-06｜CFO｜guidance：FY27毛利率財測24.5%–25.5%（原話："We continue to expect gross margin to be between 24.5%"）
- 2026-08-06｜CFO｜guidance：SG&A占營收16.5%–17.5%（原話："to be between 16.5% and 17.5% of sales"）
- 2026-08-06｜CFO｜guidance：FY27調整後EBITDA財測$35–40M（原話："adjusted EBITDA to be between $35 million and $40 million,"）
- 2026-08-06｜CFO｜guidance：FY27資本支出財測$18–22M（原話："expenditures to be between $18 million and $22 million"）
- 2026-08-06｜CFO｜guidance：積壓訂單35–40%於未來12個月轉營收（原話："approximately 35% to 40% of backlog to convert into revenue"）
- 2026-08-06｜CFO｜guidance：CFO稱太空營收當季水準為新常態（原話："revenue for the quarter is the new norm."）
- 2026-08-06｜CFO｜guidance：第三財季因假日通常最低（原話："typically the third quarter is the lowest"）
- 2026-08-06｜CFO｜guidance：三年框架：有機營收年增8–10%（原話："organic revenue growth of approximately 8% to 10% annually"）
- 2026-08-06｜CFO｜guidance：FY2029調整後EBITDA利潤率14–16%（原話："margins to expand into the 14% to 16% range by fiscal 2029"）
- 2026-08-06｜CFO｜margin：毛利率年減，管理層歸因於產品組合（原話："decline in gross margin primarily reflects the mix of sales"）
- 2026-08-06｜CFO｜margin：毛利率較上季增加230bp（原話："our gross margin percentage increased 230 basis points."）
- 2026-08-06｜CFO｜margin：國防占營收58%（上季60%、去年53%），毛利率與國防占比直接相關（原話："about 58% of our revenue this quarter was in Defense"）
- 2026-08-06｜CFO｜margin：管理層欲將國防與商業組合拉近50-50（原話："we want to get closer to that 50-50 mix"）
- 2026-08-06｜CFO｜margin：調整後EBITDA利潤率12.3%與去年同期持平（原話："representing an adjusted EBITDA margin of 12.3%,"）
- 2026-08-06｜CFO｜margin：GAAP淨利減少至$3.9M、每股$0.33（原話："$3.9 million or $0.33 per diluted share"）
- 2026-08-06｜CEO｜margin：雷達／雷射專案以市場定價而非認證成本定價（原話："market-bearing prices on those programs"）
- 2026-08-06｜CEO｜margin：競爭性標案允許較高毛利（原話："competitive and they allow for healthier margins"）
- 2026-08-06｜CEO｜margin：潛艦主力為單一來源、TINA成本定價（原話："That's sole sourced and under TINA cost and pricing."）
- 2026-08-06｜CEO｜commitment：管理層稱強勁開局使達成FY27目標處於有利位置（原話："2027 positions us well to achieve those targets."）
- 2026-08-06｜CEO｜commitment：重申FY27營收成長18%、EBITDA成長44%的指引（原話："18% revenue growth and 44% adjusted EBITDA growth"）
- 2026-08-06｜CEO｜commitment：重心由建置產能轉向運用產能（原話："building capabilities to leveraging those capabilities."）
- 2026-08-06｜CEO｜capital_allocation：新投資以高於20% ROIC門檻為目標（原話："target returns above our 20% ROIC hurdle rate"）
- 2026-08-06｜CFO｜capital_allocation：Arvada興建新廠房（原話："a new 30,000-square-foot manufacturing facility in"）
- 2026-08-06｜CFO｜capital_allocation：T. Rowe Price $50M策略投資，約$13M償債（原話："previously announced $50 million strategic investment"）
- 2026-08-06｜CFO｜capital_allocation：季末無負債（原話："million of cash on hand, no outstanding debt"）
- 2026-08-06｜CFO｜capital_allocation：營運現金流為負$12.7M（原話："operating activities during the quarter was $12.7 million"）
- 2026-08-06｜CEO｜customer：國防營收年增40%（原話："Defense revenue increased 40% during the quarter"）
- 2026-08-06｜CEO｜customer：MK48為單一來源續約選項年，非新增範圍（原話："MK48 is a sole sourced award and that is a follow-on"）
- 2026-08-06｜CEO｜customer：MK19為競爭性標案勝出，範圍擴大（原話："was a competitive solicitation and it was a good win"）
- 2026-08-06｜CEO｜customer：MK19與MK48合計約$43M（原話："totaled approximately $43 million."）
- 2026-08-06｜CEO｜customer：潛艦管線仍強（原話："the pipeline remains strong"）
- 2026-08-06｜CEO｜customer：執行力為擴大業務關鍵（原話："Just execution, period."）
- 2026-08-06｜CFO｜customer：售後市場訂單出貨比1.1（原話："aftermarket was 1.1 during the quarter."）
- 2026-08-06｜CFO｜customer：售後成長多來自國防售後（原話："growth though was driven by our Defense aftermarket."）
- 2026-08-06｜CEO｜risk：煉油與石化大型資本專案持續延後（原話："ongoing pushouts in large capital"）
- 2026-08-06｜CFO｜risk：太空訂單可能起伏，不預期每季維持此水準（原話："So we don't expect this level every quarter."）
- 2026-08-06｜CEO｜risk：北美煉油廠稼動率約96%（原話："about 96% utilization in refineries in North America"）
- 2026-08-06｜CEO｜risk：新能源市場仍處商業化早期（原話："remain relatively early in their commercialization"）
- 2026-08-06｜CEO｜product：太空訂單$14.4M，出貨比2.3x（原話："representing a book-to-bill of 2.3x"）
- 2026-08-06｜CEO｜product：FlackTek為第三大核心技術平台（原話："processing as Graham's 3rd core technology platform"）
- 2026-08-06｜CEO｜product：飛彈領域：Graham原非傳統市場（原話："Missiles had not been a conventional market for Graham."）
- 2026-08-06｜CEO｜product：透過FlackTek進入飛彈生產（原話："our early entry into missiles was through FlackTek"）
- 2026-08-06｜CEO｜product：MEGA平台涉及固態火箭發動機關鍵開發（原話："the MEGA being involved in some critical developments on"）
- 2026-08-06｜CEO｜competition：在過去有競爭對手的標案中亦獲勝（原話："we're also today winning opportunities where we did"）
- 2026-08-06｜CFO｜guidance：有機營收年增17%（原話："On an organic basis, revenue was up an impressive 17%."）
- 2026-08-06｜CFO｜guidance：當季訂單$96M，出貨比1.3x（原話："First quarter orders were $96 million"）

### GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 重申 FY27 營收財測區間（約 +18% at midpoint，含全年 FlackTek）（原話："be in the range of $285 million to $295 million"）
- 2026-06-18｜CFO Christopher Thome｜guidance：FY27 營收財測中點對應的成長幅度（原話："$285 million to $295 million, which represents an 18%"）
- 2026-06-18｜CFO Christopher Thome｜margin：FY27 毛利率財測區間，並列舉改善來源（原話："gross margin to be between 24.5% to 25.5%"）
- 2026-06-18｜CFO Christopher Thome｜guidance：FY27 SG&A 占營收比財測（原話："SG&A expense is expected to be between 16.5% and 17.5%"）
- 2026-06-18｜CFO Christopher Thome｜margin：SG&A 財測內含約 250 萬美元人員、技術、商業化的增量投入（原話："approximately $2.5 million of incremental investments"）
- 2026-06-18｜CFO Christopher Thome｜guidance：FY27 調整後 EBITDA 財測區間（原話："adjusted EBITDA to be between $35 million and $40 million"）
- 2026-06-18｜CFO Christopher Thome｜margin：CFO 說明 FlackTek 目前調整後 EBITDA 利潤率低於公司平均（原話："currently, FlackTek is a 10% adjusted EBITDA margin business"）
- 2026-06-18｜CFO Christopher Thome｜guidance：三年長期目標：有機營收成長 8%–10%（原話："growth continuing at the 8% to 10% rate for the next"）
- 2026-06-18｜CFO Christopher Thome｜guidance：三年長期目標：FY2029 調整後 EBITDA 利潤率 14%–16%（原話："EBITDA margin to continue to expand to the 14% to 16%"）
- 2026-06-18｜CFO Christopher Thome｜guidance：FY29 營收規模目標（連同約 $50–55M 調整後 EBITDA）（原話："$340 million to $350 million revenue company"）
- 2026-06-18｜CFO Christopher Thome｜margin：FY29 之後的終極目標：同業前四分之一，EBITDA 利潤率 17%–18%（原話："margins in the 17% to 18% range"）
- 2026-06-18｜CEO Matthew Malone｜margin：CEO 說明利潤率目標從追平同業進一步邁向同業前四分位（敘事升級）（原話："the top quartile within our peer group"）
- 2026-06-18｜CEO Matthew Malone｜margin：CEO 說明 Barber-Nichols 收購使利潤率承受約 200 基點的衝擊（earn-out 全額支付，回饋 1,200 萬美元給員工）（原話："and it's a tough 200-point basis hit"）
- 2026-06-18｜CEO Matthew Malone｜margin：CEO 提到 earn-out 全額支付的金額（原話："give back $12 million by hitting the max earn-out"）
- 2026-06-18｜CEO Matthew Malone｜guidance：CEO 重申 8%–10% 有機成長，並稱有機會加速就會加速（原話："focus on 8% to 10% organic investment -- organic growth"）
- 2026-06-18｜CEO Matthew Malone｜guidance：管理層訂 ROIC 目標：單案 >20%、公司整體層級 14%（原話："when I say 14%, that's at the aggregated corporate level"）
- 2026-06-18｜CEO Matthew Malone｜guidance：三年目標未納入併購（原話："we have not built in M&A"）
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 回答分析師：新計畫（商業化、售後等）的貢獻大部分已納入長期目標；FY26 約 1,000 萬、FY29 預期超過 5,000 萬（原話："expecting that to grow to north of $50 million"）
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 說明納入目標的口徑：只納入有相當把握的專案，其餘為潛在上檔（原話："ones where we felt fairly certain that we were going to get"）
- 2026-06-18｜CEO Matthew Malone｜guidance：CEO 說明新計畫納入目標時採加權方式，馬達控制器能否放量尚待驗證（原話："taken a weighted approach to how we're factoring that in"）
- 2026-06-18｜CFO Christopher Thome｜guidance：積壓訂單規模與國防占比（原話："85% of our $533 million backlog is to the defense industry"）
- 2026-06-18｜CFO Christopher Thome｜guidance：積壓訂單轉營收的時程（原話："35% to 40% of our backlog is expected to convert to"）
- 2026-06-18｜CFO Christopher Thome｜guidance：回應分析師：約 30% 積壓訂單要 2 年以上才到期，管理層稱不擔心 5.33 億積壓（原話："roughly 30% of our backlog isn't due until 2-plus years out"）
- 2026-06-18｜CFO Christopher Thome｜guidance：年度 book-to-bill 目標口徑為 1.1x（原話："goal is to achieve a book-to-bill ratio of 1.1x each year"）
- 2026-06-18｜CFO Christopher Thome｜risk：CFO 說明單季 book-to-bill 波動很大（原話："ranging from 0.5x to 2.4x in any given quarter"）
- 2026-06-18｜CFO Christopher Thome｜customer：CFO 給的 FY26 太空訂單成長數字（原話："our space orders increased 76% over the prior year"）
- 2026-06-18｜CFO Christopher Thome｜customer：CFO 給的 FY26 新能源（SMR、氫能）訂單成長數字（原話："energy orders were up 185%."）
- 2026-06-18｜Charlie Straka (BN Engineering Director)｜customer：Barber-Nichols 工程總監給的太空訂單成長數字（FY25 到 FY26），口徑與 CFO 的 76% 不同（原話："a 70% increase just from FY '25 to FY '26"）
- 2026-06-18｜CEO Matthew Malone｜customer：CEO 說明太空營收占比與訂單／營收脫節的解釋（原話："why is revenue flat? Well, orders are not"）
- 2026-06-18｜CEO Matthew Malone｜customer：CEO 說明國防占公司業務約六成（原話："60% of the portfolio today"）
- 2026-06-18｜Michael Dixon (BN GM)｜customer：國防營收 5 年成長軌跡（約 6,200 萬到 1.47 億，CAGR 24%）（原話："grown from approximately $62 million to $147"）
- 2026-06-18｜Michael Dixon (BN GM)｜competition：國防營收中獨家供應或有顯著競爭優勢的占比（原話："more than 80% of our defense revenue is sole sourced"）
- 2026-06-18｜Michael Dixon (BN GM)｜guidance：管理層列出潛在營收機會 18 億美元（至 2056）（原話："platforms shown here represent approximately $1.8 billion"）
- 2026-06-18｜Michael Dixon (BN GM)｜guidance：管理層稱 18 億機會數字被低估（原話："we believe it understates the future"）
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 說明 18 億機會的計算口徑（以當前價格，未計通膨）（原話："$1.8 billion is at today's prices without any inflation"）
- 2026-06-18｜CEO Matthew Malone｜guidance：CEO 回應分析師：未給數字，僅稱高於簡報所列（原話："it's a number north of what we presented"）
- 2026-06-18｜CEO Matthew Malone｜product：宣布取得 Virginia-class 新增內容的 2,200 萬美元 PO（尚未定價）（原話："$22 million PO, and that PO is undefinitized at this time"）
- 2026-06-18｜CEO Matthew Malone｜competition：此新增內容過去由單一供應商獨家供應，Graham 現在成為競爭者（原話："this has been sole sourced with a single vendor"）
- 2026-06-18｜Michael Dixon (BN GM)｜customer：Dixon 說明 Virginia-class 後續兩艘船訂單已下（原話："Virginia-class subs for orders for the next 2 boats already"）
- 2026-06-18｜CEO Matthew Malone｜customer：CEO 說明目前新內容的量體（2 艘船、4 個冷凝器）（原話："we have 2 boats, which ends up being 4 condensers"）
- 2026-06-18｜Michael Dixon (BN GM)｜capital_allocation：客戶補助金額（供應商開發資金）（原話："our customers of over $29 million"）
- 2026-06-18｜Charlie Straka (BN Engineering Director)｜competition：太空市場競爭節奏：不再是 NASA 式長週期開發（原話："it's a competitive market now. These aren't NASA programs."）
- 2026-06-18｜Charlie Straka (BN Engineering Director)｜product：太空推進市場規模說法（原話："propulsion market alone, $30 billion by 2030"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜product：SMR 對 Graham 的可取得市場規模：大型核電（1GW）（原話："$15 million to $30 million per reactor"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜product：SMR 對 Graham 的可取得市場規模：300MW SMR（原話："somewhere between $5 million and $15 million"）
- 2026-06-18｜CEO Matthew Malone｜guidance：CEO 對 SMR 貢獻時程的說法（原話："that's sort of 5 to 10 years out before it's a"）
- 2026-06-18｜CEO Matthew Malone｜competition：CEO 稱 Graham 在美國真空系統的市占（原話："80% market share in the U.S. on vacuum systems"）
- 2026-06-18｜Royce Roemisch (customer, Delek)｜competition：客戶（煉油專家）估計 Graham 在美國主要真空塔的裝機占比（原話："Graham probably has 85% to 90% installed base"）
- 2026-06-18｜Royce Roemisch (customer, Delek)｜product：客戶描述把競爭對手舊真空系統改裝成 Graham 新技術的成果（原話："was able to get about 25% more capacity going from a"）
- 2026-06-18｜Royce Roemisch (customer, Delek)｜customer：客戶描述美國煉油業的需求型態：以改裝取代新建（原話："They're not building any new refineries in the"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜customer：Will 引用煉油資本支出中用於升級與維護的占比（原話："85% of the capital budgets over the next 20 years are"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜commitment：Will 描述售後市場模式轉變：從被動等電話改為主動出擊（原話："we wait for the phone to ring, we say, what do you need"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜product：新世代噴嘴（NextGen Nozzle）已有安裝（原話："we have the NextGen Nozzle out there"）
- 2026-06-18｜CEO Matthew Malone｜commitment：Malone 稱階段轉換：穩定期結束，進入改善與成長期（敘事）（原話："the stabilized phase is behind us"）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 稱過去四年皆達成對股東的期望（原話："delivered on every expectation that we set for our"）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 稱除 Batavia ERP 外，過去五年計畫項目皆按時按預算完成（原話："which is coming online in August"）
- 2026-06-18｜CIO Keith Oufnac｜commitment：CIO 稱 IT 投資已納入 CapEx 財測並預期報酬率高於 20%（原話："we expect them to generate returns exceeding 20% ROI"）
- 2026-06-18｜CIO Keith Oufnac｜commitment：CMMC 合規時程承諾（原話："We are on track to be compliant by year-end"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CFO 說明 FY26 營運現金流的調整口徑（一次性交易獎金視為購買價格的減項）（原話："operations for fiscal '26 was closer to $20 million"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：FlackTek 原股東交易獎金由 Graham 代付（原話："$4 million of transaction bonuses that were awarded"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：四年財務成長率口徑（營收 CAGR 19%、調整後 EBITDA CAGR 45%）（原話："achieving 19% revenue compounded growth, 45% adjusted"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CFO 說明資本支出投資原則：確信贏得營收才投（原話："only invest in new buildings and equipment"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：FY27 CapEx 財測區間，主因是 Barber-Nichols 新廠（原話："$18 million to $22 million of CapEx spend"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：將在 Arvada 動工興建新廠（原話："break ground on a new 30,000 square foot manufacturing"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：4 月 5,000 萬美元 PIPE 完成並還清負債（原話："the recent $50 million PIPE transaction"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：目前無負債（原話："we are now debt-free as the proceeds from the transaction"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：流動性規模（原話："provides us with over $100 million in liquidity"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CapEx 占營收比的長期原則（原話："spend 7% to 10% of revenue on capital expenditures"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：R&D 占營收比將逐步提高（原話："current 0.5% of revenue to the 1% to 2% of revenue level"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CFO 稱不需要併購就能達成成長目標（原話："need acquisitions to grow"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CFO 描述過去併購節奏（原話："a strategic acquisition every 12 to 18 months"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 說明資本部署的限制：決定因素在領導團隊的承載量，成長若超出 10% 會失去資本部署的紀律（原話："if we exceed that 10% number"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 表示 ROIC 高於 20% 的專案一律執行（原話："the answer is we're going to go do"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 稱限制在於領導團隊承載量而非資本或點子（原話："think it is the capacity of the leadership team to go do"）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 描述 CEO／CFO／董事會的分工，作為資本紀律的說明（原話："I'm the gas. Chris is the break."）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 說明未來將增聘售後加速與全球銷售職位（原話："We have opened the position for the aftermarket"）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 說明銷售策略從被動接單轉為主動出擊（商業化）（原話："we are going to go on the offensive with the"）
- 2026-06-18｜Paul Nistler (Motor Controller BU leader)｜product：馬達控制器業務目標：五年內成為獨立事業單位的規模（原話："turn into a $30 million to $50 million business unit"）
- 2026-06-18｜CEO Matthew Malone｜product：電力電子與控制器業務將從 Barber-Nichols 分拆成獨立板塊（原話："controller business out of Barber-Nichols"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜product：FlackTek Mega 機型產能，作為可跟客戶進入量產的新能力（原話："2,000 kilos an hour in our mega machine"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜customer：FlackTek Mega 機型的客戶 Anduril（原話："centerpiece of Anduril's rocket motor production facility"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜customer：FlackTek 裝機基數（原話："over 2,500 machines in the field already"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜competition：FlackTek 稱客戶一旦指定其系統，轉換成本很高（原話："a really high switching cost to get out of that system"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜customer：FlackTek 耗材（容器）的出貨量（原話："shipped over 3 million containers last year"）
- 2026-06-18｜Daniel Thoren (Business Development)｜risk：國際擴張中的風險：民族主義趨勢與品牌／品質管控（原話："The nationalistic trends are a challenge in some areas."）
- 2026-06-18｜Daniel Thoren (Business Development)｜risk：Thoren 提到在海外營運可能失去品牌、流程與品質掌控（原話："control of our brand and our process and our quality"）
- 2026-06-18｜Daniel Thoren (Business Development)｜commitment：Thoren 稱未來必須在當地設廠（原話："We're just going to have to build in those markets"）
- 2026-06-18｜CEO Matthew Malone｜customer：CEO 說明全球化策略重心在能源與製程（原話："strategy is most focused around energy and process"）
- 2026-06-18｜CFO Christopher Thome｜customer：CFO 說明國防占比偏高的原因，並指出能源與製程的大型資本專案偏慢（原話："large capital projects in our Energy and Process business"）
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 的長期結構目標：國防與商用各半（原話："have a 50-50 split between defense and commercial"）
- 2026-06-18｜CEO Matthew Malone｜risk：CEO 說明採預收款降低新開發案風險，不先投入自有資本（原話："we're asking for more payment upfront"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 說明目前專案選擇性很高，需求超出可承接量（原話："highly selective of what opportunities we pursue"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 說明事業單位組織願景：5 到 7 個利基事業單位（原話："5 to 7 business units, niche, world-class at what they do"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 提到 Xdot 軸承收購補強 Barber-Nichols 能力（原話："we made the Xdot Bearing acquisition"）

### 問答異常語氣（迴避／改口／保留）
- GHM_Q1_2027_Earnings_Call_20260806.md｜問：Russell Stanley問上週GD與HII大型潛艦合約有多少已在Graham積壓訂單中｜答法：回答「some of them in, some of them not」，未給數字，並表示「I'll keep it high level there」
- GHM_Q1_2027_Earnings_Call_20260806.md｜問：Russell Stanley問彈藥短缺帶來的機會與對Graham的順風程度｜答法：未量化，改談魚雷與FlackTek，稱「I can't talk in too much detail」、「I'll keep it kind of high level」
- GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md｜問：William Blair 的 Jed Dorsheimer 問是否像 GE Vernova 採較高訂金與里程碑付款，以避免閒置產能風險｜答法：CEO 稱「exact same strategy」並說明方向（預收款、國防專案當銀行），未給訂金比例或具體條款數字
- GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md｜問：Northland 的 Bobby Brooks 問若再納入現有能力可承接的其他內容，國防機會（簡報 18 億美元）粗估會多大｜答法：CEO 未給數字，稱「north of what we presented」，並表示需靠執行、數字交給 Will 的團隊去實現；CFO 補充 18 億是以現價、未計通膨
- GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md｜問：Bobby Brooks 追問 FlackTek Mega 機型是否價格很高｜答法：CEO 改談 ROI 與客戶價值（「price is all relative」），未給價格或單台金額，也稱無法談 Anduril 產線的生產數字
- GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md｜問：Bobby Brooks 問 FlackTek 加入後的近期訂單勝利如何加速、具體是什麼｜答法：CEO 說「I can't get into the exact specifics」，列出招聘與關閉管線中的案子，未給金額或客戶名

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
{"date":"20260714","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"國防（Navy）多年 backlog 提供高能見度成長","columns":{"2Y 驗證點":"book-to-bill ≥ 1.0x、backlog 維持 &gt; $450M","5Y 驗證點":"Columbia/Virginia 量產件持續轉收入，國防營收 CAGR ≥ 10%","10Y 驗證點":"下一代平台（SSN(X)/DDG(X)）承接首件","具體數字門檻":"backlog $532.6M、orders $359.4M、book-to-bill 1.5x（FY26）","信息來源":"FY26 8-K（2026-06-08）；10-K FY2026","漂移觸發":"連 2 季 book-to-bill &lt; 1.0x → 削弱（QC-35 2Y 假設）"}},{"id":"H2","text":"Margin 沿多年路徑爬向 mid-teen Adj EBITDA","columns":{"2Y 驗證點":"FY27 Adj EBITDA 12-14% 兌現","5Y 驗證點":"FY29 Adj EBITDA 14-16%（管理層 3 年計畫）","10Y 驗證點":"結構性穩定於 15%+，operating leverage 兌現","具體數字門檻":"FY27 指引 $35-40M（12.1-13.8%）；FY29 目標 14-16%；FY27 GM 指引 24.5-25.5%","信息來源":"FY2027 guidance 8-K；法說（2026-06-08）","漂移觸發":"連 2 季 Adj EBITDA ≤ 10% → 削弱；連 4 季 TTM 偏離 ≥ 5% → 反轉（5Y 假設）"}},{"id":"H3","text":"市場願意為國防超級週期＋margin 兌現維持溢價倍數（估值假設）","columns":{"2Y 驗證點":"Fwd PE 維持 &gt; 35x","5Y 驗證點":"倍數隨成長成熟 de-rate 但守住 &gt; 22x","10Y 驗證點":"穩定於工業複利 20-25x","具體數字門檻":"現價 Fwd PE 45.6x（FY28）；同業/歷史 96th 分位","信息來源":"yfinance 2026-07-13；valueinvesting.io EV/EBITDA 分位","漂移觸發":"倍數壓縮至 &lt; 25x 且 margin 未兌現 → thesis H3 破（估值假設是本案最脆弱一環）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"估值均值回歸：45x → 22-25x 校準（不需基本面惡化）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Fwd PE / EV-EBITDA 分位、共識修正方向","警戒閾值":"共識連 2 季下修 + 倍數破 35x → 減碼訊號（若已持有）"}},{"id":"R2","text":"margin 兌現落後：FlackTek ~10% 稀釋 + 國防 mix 拉低 GM，FY27 Adj EBITDA 停在 10-11%","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 Adj EBITDA margin、GM 軌跡","警戒閾值":"連 2 季 Adj EBITDA ≤ 10% → 大動作重評"}},{"id":"R3","text":"Navy 造艦排程延遲外溢：Columbia 12-16 月、Virginia 24-36 月延遲（CBO/GAO 2026）拖慢 backlog 轉換節奏；及能源大型專案續軟","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"12M-forward 營收 / backlog 比、能源新訂單","警戒閾值":"轉換率 &lt; 35% 且能源訂單連 2 季負 → 下修成長軌跡"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE 回落≤30x（約$68）或 Adj EBITDA margin 連2季≥14% 兌現","irr_base_pct":-0.9,"ev5y_pct":-7.6,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.7,"ev5y_pct":-7.6,"irr_base_pct":-0.9,"max_dd_pct":-62.0,"bull_5y_price":147.0,"bear_5y_price":46.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE 回落≤30x（約$68）或 Adj EBITDA margin 連2季≥14% 兌現","price_at_dd":102.7,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
