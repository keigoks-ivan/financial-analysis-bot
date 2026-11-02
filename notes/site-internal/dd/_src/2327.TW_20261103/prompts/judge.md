你是 stock-analyst **v20 判斷 agent**，標的 2327.TW（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"2327.TW","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2327.TW_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2327.TW_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP，合併）","value":495.32,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"億元 TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"國巨法說報導 https://uanalyze.com.tw/articles/1516757975（IR 新聞稿未取得）"},"note":"查無 Q3 共識"},{"id":"f_kpi1","label":"毛利率","value":41.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"https://uanalyze.com.tw/articles/1516757975"},"note":"查無"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益","value":146.03,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"億元 TWD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"https://uanalyze.com.tw/articles/1516757975"},"note":"查無"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益率","value":29.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"https://uanalyze.com.tw/articles/1516757975"},"note":"查無"},{"id":"f_kpi4_eps","label":"稅後純益（歸屬母公司）／EPS","value":5.83,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"元 TWD／股（純益 119.81 億元）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"https://uanalyze.com.tw/articles/1516757975"},"note":"查無"},{"id":"f_kpi5_q4_2026","label":"管理層下一季指引（Q4 2026）","value":"營收、毛利率、營業利益率皆較 Q3「微幅成長」（無數字區間）","period":"Q3 2026 法說（2026-10-29）","unit":"qualitative","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026 法說（2026-10-29）","citation":"https://uanalyze.com.tw/articles/8967257977"},"note":"查無"},{"id":"f_kpi6_book_to_bill","label":"訂單出貨比（book-to-bill）","value":"接近 2（鉭質電容、MLCC 等 AI 相關產品更高，無精確數字）","period":"Q3 2026（公告於 2026-10-29）","unit":"倍","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（公告於 2026-10-29）","citation":"https://uanalyze.com.tw/articles/8967257977"},"note":"不適用"},{"id":"f_kpi7","label":"產能利用率","value":"特殊品與標準品皆接近 95%","period":"Q3 2026（公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（公告於 2026-10-29）","citation":"https://uanalyze.com.tw/articles/8967257977"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-14","period":"2026-08-14","unit":"date","basis":"距今 57 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-14"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_2327_tw_gross_margin_pct","label":"2327.TW 毛利率","value":37.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2327.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2327_tw_operating_margin_pct","label":"2327.TW 營業利益率","value":24.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2327.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2327_tw_fcf_margin_pct","label":"2327.TW FCF 利潤率","value":18.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2327.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2492_tw_gross_margin_pct","label":"2492.TW 毛利率","value":18.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2492.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2492_tw_operating_margin_pct","label":"2492.TW 營業利益率","value":7.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2492.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2492_tw_fcf_margin_pct","label":"2492.TW FCF 利潤率","value":6.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2492.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_6981_t_gross_margin_pct","label":"6981.T 毛利率","value":42.32,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6981.T.gross_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"}},{"id":"f_peer_6981_t_operating_margin_pct","label":"6981.T 營業利益率","value":15.39,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6981.T.operating_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"}},{"id":"f_peer_6981_t_fcf_margin_pct","label":"6981.T FCF 利潤率","value":9.45,"period":"TTM ending 2026-03-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6981.T.fcf_margin_pct","as_of":"TTM ending 2026-03-31（4季加總）"}},{"id":"f_peer_6762_t_gross_margin_pct","label":"6762.T 毛利率","value":31.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6762.T.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6762_t_operating_margin_pct","label":"6762.T 營業利益率","value":11.15,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6762.T.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_6762_t_fcf_margin_pct","label":"6762.T FCF 利潤率","value":3.93,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6762.T.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_009150_ks_gross_margin_pct","label":"009150.KS 毛利率","value":21.74,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.009150.KS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_009150_ks_operating_margin_pct","label":"009150.KS 營業利益率","value":9.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.009150.KS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_009150_ks_fcf_margin_pct","label":"009150.KS FCF 利潤率","value":1.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.009150.KS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":498.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"TWD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":59.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^TWII","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":39.07,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.19 → 20.19）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.04,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（31.59 → 31.92）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":2.87,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（45.59 → 46.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":20.19,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":31.92,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":46.9,"period":"2026-10-31","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":5.76,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 19.09 → 20.19（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":33.57,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.77,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.07,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":24.86,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 20.19，分子＝快照價 502.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.203,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":46858.83,"period":"2026-11-03","unit":"TWD m","basis":"yfinance 最新一季：總債務 247410.95、現金 200552.12（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":2058.46,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1073001.53,"period":"2026-11-03","unit":"TWD m","basis":"市值 1026142.7 ＋ 淨負債 46858.83","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":184179.38,"period":"2026-11-03","unit":"TWD m","basis":"yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":248773.08,"period":"2026-11-03","unit":"TWD m","basis":"yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.83,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 502.0 / W52 457.62 / W104 296.09 / W250 184.16 / W250 13週斜率 3.98%"},{"id":"f_ma_w52","label":"52 週均線","value":457.62,"period":"2026-11-03","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":296.09,"period":"2026-11-03","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":184.16,"period":"2026-11-03","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":3.98,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"摩根士丹利法說前報告：日韓 MLCC 供應商可能將產能轉向高階產品，並列同業競爭為風險；下修國巨 EPS 預估、目標價 1515 元調為 1465 元","source":"工商時報 wantrich","url":"https://wantrich.chinatimes.com/news/20260723900144-420101","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"國巨法說：AI 營收比重達 2 成、產能吃緊，2027 年擴產 10-15%","source":"uanalyze 〈國巨法說〉","url":"https://uanalyze.com.tw/articles/4227657979","excerpt":"〈國巨法說〉AI營收比重達2成 產能吃緊明年擴產10-15% 2026年10月29日 17:06 - 優分析產業數據中心 圖片來源：由鉅亨網提供 被動元件大廠國巨*(2327-TW)今(29)日召開法說會，由於 AI 需求持續成長，第三季營收占比已上升至約 2 成，公司規劃2027年擴充鉭質電容及多層陶瓷電容(MLCC)產能，預計較目前水準增加10%至15%，部分新增產能將於明年第二季開出，其餘於下半年陸續到位。","as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"國巨在鉭電容界無對手（兆豐投顧看法）；2026Q1 毛利率 38.1% 創三年新高","source":"鉅亨網","url":"https://news.cnyes.com/news/id/4844680","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"國巨114年股東會年報「最近二年度主要銷貨客戶資料」填「無」，即年報未列出占營收10%以上的單一客戶。","source":"公開資訊觀測站電子書件 114年股東會年報（2025_2327_20260527F11.pdf）主要銷貨客戶表，PDF第85頁","url":"https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id=2327&year=115&seamon=&mtype=F&dtype=","excerpt":"2.最近二年度主要銷貨客戶資料：無。","as_of":"2026-10-29","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"國巨2026-10-29法說：2027年擴充鉭質電容與MLCC產能10-15%，部分新產能2027Q2開出；Q3 AI相關營收占比近2成；長期稼動率目標85-90%保留彈性（來源為搜尋摘要轉述，未取得逐字原文）","source":"uanalyze〈國巨法說〉AI營收比重達2成 產能吃緊明年擴產10-15%","url":"https://uanalyze.com.tw/articles/4227657979","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce預期高階MLCC短缺延續至2027上半年；新產能2026Q4至2027陸續開出，產線建置需1-2年（搜尋摘要轉述，未取得逐字原文）","source":"TrendForce Press Center 2026-06-17","url":"https://www.trendforce.com/presscenter/news/20260617-13105.html","excerpt":null,"as_of":"2026-06-17","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"大摩悲觀情境（目標價685元）假設非AI需求自2026下半年大幅下滑且併購效益不如預期；法說前關注非AI需求能見度（搜尋摘要轉述，未取得逐字原文）","source":"技術新報/經濟日報等外資報導彙整","url":"https://money.udn.com/money/story/5607/9647152","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"國巨2026Q2訂單出貨比季末達2.2，Q3稼動率預估90%以上，AI/記憶體客戶以長約溢價鎖料","source":"富果研究 2026-07-29法說摘要","url":"https://blog.fugle.tw/post/earnings-call-2327-2026-07-29","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"公平會處分書資料庫以「國巨」全文搜尋共 2 筆；唯一案名含公司名者為 2008 年結合應申報而未申報處分案，另一筆（2021 鉭質電容器卡特爾案）僅文內提及國巨，非被處分對象。","source":"公平交易委員會 處分書及決議書全文搜尋「國巨」","url":"https://www.ftc.gov.tw/uploadDecision/2005787-0970213_001_097d018.pdf","excerpt":"2008/02/13 處分書及不處分決議書［公平交易法第11條］國巨股份有限公司因結合應申報而未申報之行為，違反公平交易法處分案。（案名含公司名）","as_of":"2008-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"證交所 ESG 揭露：報告年度 114 因反競爭行為法律訴訟造成的金錢損失總額為 N/A。","source":"證交所 OpenAPI t187ap46_L_20","url":"https://openapi.twse.com.tw/v1/opendata/t187ap46_L_20","excerpt":"報告年度 114，因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)＝N/A。","as_of":"2026-11-02","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋 2026 年國巨反壟斷／競爭調查，未見相關報導；僅見 2019 年中國市場監管總局對國巨未申報收購 BrightKing 之處分（舊事）。","source":"Concurrences 2019-06 bulletin: Chinese SAMR fines a Taiwan-based company","url":"https://www.concurrences.com/en/bulletin/news-issues/june-2019/the-chinese-state-administration-for-market-regulation-fines-a-taiwan-based","excerpt":null,"as_of":"2019-06-25","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"國巨董事長陳泰銘預期關稅對公司影響輕微；公司因收購普思與基美在美國有布局，可就近供應客戶","source":"Yahoo股市 焦點股/國巨3月、Q1營收創高!不敵關稅風暴 摔破400元大關","url":"https://tw.stock.yahoo.com/news/%E7%84%A6%E9%BB%9E%E8%82%A1-%E5%9C%8B%E5%B7%A83%E6%9C%88-q1%E7%87%9F%E6%94%B6%E5%89%B5%E9%AB%98-%E4%B8%8D%E6%95%B5%E9%97%9C%E7%A8%85%E9%A2%A8%E6%9A%B4-%E6%91%94%E7%A0%B4400%E5%85%83%E5%A4%A7%E9%97%9C-042207339.html","excerpt":"不料關稅風暴澆息利多，今（9）日國巨股價不漲反跌，盤中重摔逾8%，失守400元大關，寫下自2022年12月、近兩年半來新低；國巨繼前兩日連挫跌停後，今日股價持續走低，合計跌幅達近27%。 國巨3月營收轉為正成長，月增13.8%、年增10.8%，來到111.01億元，重返百億元大關，並登上歷史單月新高；累計第一季合併營收達311.04億元，季增3.7%、年增9.1%，創下歷年同期最佳表現。國巨分析，3月營收上月增加，主要是受惠3月工作天數回復正常，加上高階應用產品出貨穩健，推升動能所致。 廣告 廣告 展望未來，國巨指出，雖然地緣政治風險仍存在高度不確定性，但客戶庫存已逐漸達到健康水準，因此公司對後市抱持審慎樂觀態度，並將密切關注全球關稅變化，以因應後續挑戰。 川普揮出關稅大刀，各界力拚「美國製造」，而國巨早已於2018年、2020年分別收購普思（Pulse）、基美（KEMET）兩","as_of":"2025-04-09","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"外資 2023-02 報告：國巨集團台灣產能比重預期衝上三成；墨西哥、日本、泰國、馬來西亞、波蘭、奧地利等海外產能合計約五成（依搜尋摘要，未讀全文，數字為舊資料）","source":"財經新報 technews：外資：國巨集團業績拚 1,500 億元，台灣產能比重衝三成","url":"https://finance.technews.tw/2023/02/23/yageo-1500-tw-30percent/","excerpt":"外資：國巨集團業績拚 1,500 億元，台灣產能比重衝三成","as_of":"2023-02-23","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2024-10 法說會：鉭質電容與 MLCC 生產基地分布亞洲及墨西哥，非單一地區（依搜尋摘要轉述）","source":"富果研究：國巨 2024-10-29 法說會","url":"https://blog.fugle.tw/post/earnings-call-2327-2024-10-29","excerpt":null,"as_of":"2024-10-29","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2026-07-29 法說會備忘錄：Q2營收445億元創高，Q3稼動率目標提高（可能含產能地區資訊）","source":"富果研究：國巨 2026-07-29 法說會","url":"https://blog.fugle.tw/post/earnings-call-2327-2026-07-29","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026-10-29 法說：AI 營收比重達約 2 成，產能吃緊，2027 年擴產 10-15%","source":"UAnalyze〈國巨法說〉AI營收比重達2成 產能吃緊明年擴產10-15%","url":"https://uanalyze.com.tw/articles/4227657979","excerpt":"〈國巨法說〉AI營收比重達2成 產能吃緊明年擴產10-15%","as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 9 月合併營收 170.68 億元，月增 4.5%、年增 46.1%，累計前 9 月 1,321.54 億元年增 36.3%","source":"TechNews 國巨*(2327)公布 9 月營收","url":"https://finance.technews.tw/2026/10/08/yageo-2327-202609-financial-report/","excerpt":"國巨*(2327)今(7)日公布 9 月營收，達 170.68 億元，較 8 月成長 4.5%,較去年同期成長 46.1%,累計前 9 月營收為 1,321.54 億元，年增 36.3%。","as_of":"2026-10-07","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 年 8 月營收 163.32 億元，年增 51.8%","source":"TechNews 國巨*(2327)公布 8 月營收","url":"https://finance.technews.tw/2026/09/08/yageo-2327-202608-financial-report/","excerpt":"國巨*(2327)今(8)日公布 8 月營收，達 163.32 億元，較 7 月成長 1.2%,較去年同期成長 51.8%,累計前 8 月營收為 1,150.85 億元，年增 35.0%。","as_of":"2026-09-08","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026-07-29 法說：第二季獲利 94.18 億元季增 17.7%；上半年獲利創高 EPS 8.48 元","source":"UAnalyze〈國巨法說〉Q2純益季增17.7% 上半年獲利創高EPS8.48元","url":"https://uanalyze.com.tw/articles/2544252424","excerpt":"〈國巨法說〉Q2純益季增17.7% 上半年獲利創高EPS8.48元","as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"國巨法說提及 2028 年計畫推出嵌入式基板的電感解決方案（磁性元件技術世代變化）","source":"富果研究 國巨 2026-04-30 法說會整理","url":"https://blog.fugle.tw/post/earnings-call-2327-2026-04-30","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"設計端建議關鍵電源軌同時驗證 MLCC 與聚合物電容等替代技術，保留佈局彈性","source":"Passive Components Blog 2026 passive components design parameter","url":"https://passive-components.eu/passive-components-in-2026-from-invisible-commodity-to-design-parameter/?amp=1","excerpt":"least two manufacturers or technologies for critical positions, such as key MLCC nodes on power rails, makes it significantly easier to rebalance sourcing if one vendor, technology or region becomes constrained. Layout choices also play a role: maintaining reasonable margin in footprint and creepage or clearance distances can allow a later change between, for example, MLCC and polymer","as_of":"2026-06-02","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"董事長陳泰銘稱國巨已由標準品為主轉向客製化與高階特殊品；Q1 2026 約75%營收來自AI、車用、工規、醫療與國防航太，高階電容占比由17%升至45%，大中華區客戶占比降至25%以下","source":"technews 財經 國巨 AI 高峰會拚轉型高階客製化","url":"https://finance.technews.tw/2026/04/30/high-end-customization/","excerpt":"峰會拚轉型高階客製化！陳泰銘：AI 所有應用「絕不缺席」 作者 姚 惠茹 | 發布日期 2026 年 04 月 30 日 17:19 | 分類 AI 人工智慧 , 公司治理 , 材料、設備 Loading... 被動元件大廠國巨今日舉辦「2026 國巨集團人工智慧高峰會」，董事長陳泰銘表示，國巨已從過去以標準品為主的營運模式，成功轉型為專注客製化與高階特殊品，未來將營運重心將放在高門檻、高客製，以及具有成長性的高端市場，並強調國巨在 AI 所有的應用領域絕對不會缺席。 陳泰銘表示，國巨透過持續的海內外併購達成轉型里程碑，包含 2000 年併購飛利浦先進陶瓷材料元件部門、2018 年普思、2019 年基美，以及 2023 年併購兩家歐洲感測器公司與 2025 年併購日本芝浦溫度感測器公司，目前營運版圖成功分散至歐洲、美國、日本等高端應用市場。 陳泰銘指出，國巨今年第一季已有 75%","as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"法說會摘要：轉型期間自2018年起八年，大中華區客戶占比已降到25%以下","source":"富果研究 國巨 2026-04-30 法說會","url":"https://blog.fugle.tw/post/earnings-call-2327-2026-04-30","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"高盛、花旗於國巨7月法說後同步調降目標價：高盛1490→1280元、花旗1500→1450元，皆維持買進；報導稱主因產業本益比壓縮而非國巨獲利轉弱。","source":"聯合新聞網〈國巨目標價 兩外資調降〉","url":"https://money.udn.com/money/amp/story/5607/9661459","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"摩根士丹利於法說前將國巨目標價由1515元降至1465元，評等維持買進；以2028年EPS與31倍本益比推算，樂觀情境2075元、悲觀情境685元。","source":"自由財經〈外資第1槍!國巨高點腰斬 大摩目標價降至1465元〉","url":"https://ec.ltn.com.tw/article/breakingnews/5515845","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-29法說：Q2稅後EPS 4.59元，上半年EPS 8.48元；公司展望Q3單季營收預估季比中位數成長，毛利率、營益率可望微幅季增（未給具體區間）。","source":"工商時報（wantrich.chinatimes.com）2026-07-29 法說報導","url":"https://wantrich.chinatimes.com/news/20260729900529-420101","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年8月營收163.32億元，月增1.2%、年增51.8%，累計前8月1150.85億元、年增35.0%（本軸未查得9、10月月營收）。","source":"TechNews 國巨8月營收","url":"https://finance.technews.tw/2026/09/08/yageo-2327-202608-financial-report/","excerpt":null,"as_of":"2026-09-08","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"外資調升國巨目標價（40倍本益比，預估2026-2028 EPS 17.8/31.4/43.2元）","source":"聯合新聞網 外資點名調升目標價","url":"https://money.udn.com/money/amp/story/5607/9554786","excerpt":"最新預估2026-2028年每股稅後盈餘（EPS）為17.8/31.4/43.2元，以40xPE評價，同步升目標。 美系券商認為，金像電5月營收優於預期，顯示第2季還有上修空間。美系券商表示，持續擴產以追上需求，既有ASIC客戶第3季將顯著貢獻，市占率提升中，而第4季也有機會取得新的ASIC客戶。最新預估2026-2028年EPS為39.2/66/90元，以明年26xPE評價。","as_of":"2026-06-09","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"國巨公開收購日本芝浦電子，競價勝出，最終接受率87.3%，芝浦2025年11月納入合併報表（來源為搜尋摘要轉述，未讀頁面原文）","source":"UAnalyze：國巨(2327)完成收購日本芝浦電子 持股達87.3% 拚2026年整併","url":"https://uanalyze.com.tw/articles/5222935937","excerpt":null,"as_of":"2025-11-07","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"國巨以公開收購（非合意）取得茂達約28.5%股權，公司視為財務性投資（來源為搜尋摘要轉述）","source":"聯合新聞網：陳泰銘再出手 國巨擬砸48億元非合意併購茂達","url":"https://udn.com/news/story/7240/8999863","excerpt":null,"as_of":"2025-09-09","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"公開資訊觀測站近12個月重大訊息121則，標題含關鍵字8則，皆為理財商品處分、資訊更正與鄰廠火災說明，無訴訟、裁罰、重編類標題","source":"公開資訊觀測站 歷史重大訊息清單","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2327","excerpt":"標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 8 則，未含者 113 則。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"國巨規劃2027年擴充鉭質電容與MLCC產能，較目前增加約10%至15%，部分新產能2027年第二季開出，其餘下半年陸續到位；長期目標稼動率85%至90%；Q3稼動率近95%","source":"uanalyze〈國巨法說〉AI營收比重達2成 產能吃緊明年擴產10-15%","url":"https://uanalyze.com.tw/articles/4227657979","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"國巨2026年前九月資本支出約57億元，全年預計高於去年；2027年資本支出規模尚未定案","source":"uanalyze 國巨法說（搜尋摘要彙整）","url":"https://uanalyze.com.tw/articles/4227657979","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"村田2026-10-30宣布2026至2030財年約1兆日圓MLCC投資，FY2027–2028產能年增約20%，岡山新廠2027年4月動工、2028年底完工","source":"EE Times Japan 村田製、MLCCに1兆円投資","url":"https://eetimes.itmedia.co.jp/ee/spv/2610/30/news084.html","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"傳京瓷計劃將日本MLCC產能擴增至3倍（報導，未證實）","source":"TechNews 京瓷傳計劃將日本MLCC工廠產能擴增至3倍","url":"https://technews.tw/2026/07/13/kyocera-reportedly-plans-to-triple-japan-mlcc-capacity/","excerpt":null,"as_of":"2026-07-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"2026年7月法說會：國巨稱截至6月底訂單出貨比升至2.2，客戶庫存降至約2個月的健康水準；終端客戶主動洽談長期供貨協議(LTA)（搜尋摘要轉述，未取得原文）","source":"TechNews 財經 2026/07/29 國巨法說報導","url":"https://finance.technews.tw/2026/07/29/bb/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"花旗7/24報告：國巨自7/1起對MLCC、鉭質電容、鋁質電容全面調價，ASP漲幅約15%~25%，這些產品約占營收一半；維持買進、目標價1,500元（搜尋摘要轉述，未取得原文）","source":"TechNews 2026/07/24 電容全面漲價效應將現","url":"https://finance.technews.tw/2026/07/24/price-increase-effect/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"國巨2026年初陸續調價：1/1磁珠約一成、2/1晶片電阻約15%~20%，理由為白銀、釕、鈀等貴金屬大漲（搜尋摘要轉述，未取得原文）","source":"uanalyze 貴金屬大幅上漲 國巨傳2/1起調漲部分電阻產品報價","url":"https://uanalyze.com.tw/articles/4836745578","excerpt":null,"as_of":"2026-01-20","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce 2026年9月MLCC報價：市場分化，消費級價格轉軟、高階維持強勁；Murata退出低毛利消費與車規品項（搜尋摘要轉述，未取得原文，無價格表）","source":"TrendForce MLCC Price Sep. 2026","url":"https://www.trendforce.com/research/download/RP260930PG","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#4","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"國巨3月營收創新高，客戶庫存達健康水平","source":"Yahoo 股市 《電零組》國巨3月營收締新猷","url":"https://tw.stock.yahoo.com/news/%E9%9B%BB%E9%9B%B6%E7%B5%84-%E5%9C%8B%E5%B7%A83%E6%9C%88%E7%87%9F%E6%94%B6%E7%B7%A0%E6%96%B0%E7%8C%B7-%E5%AE%A2%E6%88%B6%E5%BA%AB%E5%AD%98%E9%81%94%E5%81%A5%E5%BA%B7%E6%B0%B4%E5%B9%B3-235100259.html","excerpt":null,"as_of":"2026-04-08","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2019 Q1 國巨毛利率 44.8%，年減 6.6 個百分點、季減 14.3 個百分點，大中華區需求疲弱","source":"technews 國巨 Q1 獲利寫近 6 季新低","url":"https://finance.technews.tw/2019/04/25/yaego-financial-reporting-q1-2019/","excerpt":"國巨第一季毛利率為 44.8%，年減 6.6 個百分點，季減 14.3 個百分點；營業利益 29.99 億元，營業利益率為 26.3%，年減 16.1 個百分點，季減 1.8 個百分點；非營業項目淨收入為 1.31 億元，包括已實現及未實現外幣兌換淨損失 0.44 億元、權益法認列轉投資收益 0.43 億元、利息淨收入 1.37 億元及其他淨損失 0.05 億元。","as_of":"2019-04-25","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2019 Q3 稅後淨利季增44%、年減85.9%，前三季 EPS 14.26 元，庫存回復正常","source":"technews 國巨 Q3 獲利季增 44%","url":"https://finance.technews.tw/2019/11/08/yageo-financial-reporting-q3-2019/","excerpt":"國巨 Q3 獲利季增 44%，前 3 季 EPS 14.26 元；Q4 庫存料續降 作者 MoneyDJ | 發布日期 2019 年 11 月 08 日 9:30 | 分類 財報 , 財經 Loading... 被動元件大廠國巨公布今年第三季合併稅後淨利 20.44 億元，季增 44%、年減 85.9%，每股盈餘 4.81 元；","as_of":"2019-11-08","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2023 Q3 法說：Q4 2023 與 Q1 2024 為此波景氣循環谷底；2023 全年毛利率 33.5%","source":"富果研究 國巨 2023-10-26 法說會","url":"https://blog.fugle.tw/post/earnings-call-2327-2023-10-26","excerpt":null,"as_of":"2023-10-26","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"2023 全年毛利率 33.5%，年減 4.5 個百分點","source":"富果研究 國巨 2024-02-29 法說會","url":"https://blog.fugle.tw/post/earnings-call-2327-2024-02-29","excerpt":null,"as_of":"2024-02-29","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"國巨公開收購日本芝浦電子，競價勝出，最終接受率87.3%，芝浦2025年11月納入合併報表（來源為搜尋摘要轉述）","source":"UAnalyze：國巨(2327)完成收購日本芝浦電子 持股達87.3% 拚2026年整併","url":"https://uanalyze.com.tw/articles/5222935937","excerpt":null,"as_of":"2025-11-07","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"國巨以公開收購（非合意）取得茂達約28.5%股權，公司視為財務性投資（來源為搜尋摘要轉述）","source":"聯合新聞網：陳泰銘再出手 國巨擬砸48億元非合意併購茂達","url":"https://udn.com/news/story/7240/8999863","excerpt":null,"as_of":"2025-09-09","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"經查公開資訊觀測站近12個月重大訊息，標題無訴訟、仲裁類；網路搜尋亦無國巨訴訟或投保中心案件","source":"公開資訊觀測站 歷史重大訊息清單","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2327","excerpt":"標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 8 則，未含者 113 則。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"0","claim":"2025-12-16 高雄大發三廠鄰近工廠火災，火勢未延燒本廠區，無人員受傷，未損及生產設備及貨物；搜尋無國巨產品召回或品質異常報導","source":"公開資訊觀測站 重大訊息：國巨高雄大發三廠鄰近工廠火災事件說明","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2327","excerpt":"目前確認，上述火災火勢並未延燒至本廠區，未造成人員受傷，亦未對生產設備及貨物造成損害。","as_of":"2025-12-16","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月重大訊息標題無裁罰、重編；僅有資金貸與明細表與iXBRL申報資訊更正，搜尋無金管會／證交所處分或保留意見報導","source":"公開資訊觀測站 歷史重大訊息清單","url":"https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2327","excerpt":"標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 8 則，未含者 113 則。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"2327.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.61,"operating_margin_pct":24.8,"fcf_margin_pct":18.86,"rd_intensity_pct":2.32},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2327.TW","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"2492.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":18.55,"operating_margin_pct":7.64,"fcf_margin_pct":6.72,"rd_intensity_pct":2.55},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2492.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"6981.T","period":"TTM ending 2026-03-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":42.32,"operating_margin_pct":15.39,"fcf_margin_pct":9.45,"rd_intensity_pct":8.68},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6981.T","as_of":"TTM ending 2026-03-31（4季加總）"}},{"name":"6762.T","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.05,"operating_margin_pct":11.15,"fcf_margin_pct":3.93,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.6762.T","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"009150.KS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":21.74,"operating_margin_pct":9.8,"fcf_margin_pct":1.82,"rd_intensity_pct":5.97},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.009150.KS","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"2327.TW"},"financial_history":{"ticker":"2327.TW","currency":"TWD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":121086925000.0,"revenue_yoy_pct":null,"gross_margin_pct":38.0,"operating_margin_pct":23.94,"net_income":22730465000.0,"diluted_eps":9.046881,"free_cash_flow":19119579000.0,"fcf_margin_pct":15.79,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":107609336000.0,"revenue_yoy_pct":-11.13,"gross_margin_pct":33.48,"operating_margin_pct":18.99,"net_income":17427068000.0,"diluted_eps":8.48,"free_cash_flow":14210638000.0,"fcf_margin_pct":13.21,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":121667329000.0,"revenue_yoy_pct":13.06,"gross_margin_pct":34.36,"operating_margin_pct":19.32,"net_income":19356484000.0,"diluted_eps":9.41,"free_cash_flow":24236198000.0,"fcf_margin_pct":19.92,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":132930016000.0,"revenue_yoy_pct":9.26,"gross_margin_pct":36.21,"operating_margin_pct":22.42,"net_income":23634229000.0,"diluted_eps":11.48,"free_cash_flow":24556280000.0,"fcf_margin_pct":18.47,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/2327.TW/2327.TW_Q3_2024_Earnings_Call_20241029.md）

# Q3 2024 Earnings Call
2024-10-29

Q3 2024 Earnings Call
Yageo Corporation | Earnings Calls | 2024-10-29
Howard Kao (Analysts)
Hello. Good afternoon, everyone, and thank you for joining us today for Yageo's Third Quarter Result
Webcast.
Yageo is the world's largest supplier of chip resistor and tantalum capacitors as well as a top 3 supplier
for MLCCs and inductors. My name is Howard Kao, and I'm the coverage analyst here at Morgan
Stanley.
We are very honored again to have Mr. David Wang, CEO; Mr. Eddie Chen, CFO; and Mr. Claudio
Lollini, Head of Global Sales and Marketing of Yageo here with us today. And we look forward to their
insights and comments on the company as well as the market.
The management team will first walk us through third quarter results and also provide some forward-
looking commentary. [Operator Instructions]
And I would now like to turn it over to Yageo's, Eddie and David for opening remarks.
Eddie Y.S. Chen (Executives)
Good afternoon, investors. Thank you for joining our third quarter earnings conference.
As usual, I'll kick off with a quick update on the third quarter financials and then followed by David,
and then questions.
Okay. So first, let's look at the third quarter financials. Basically, the third quarter has been a pretty
stable quarter compared to the previous one. You see from the selected items here, we have a pretty flat
sales in the third quarter coming in at $31.7 billion, about 1% growth from the previous quarter. Gross
margin pretty stable as well at 35.2% versus 35.1% in the previous or TWD 11.1 billion.
We're seeing very stable order in a very controlled fashion on the OpEx spending. So you see the OpEx
dollar third quarter come in at about TWD 4.5 billion roughly on the same level as the previous one. So
the operating profit at TWD 6.6 billion, 20.9%, slightly up from the previous quarter. On the non-op
front, we're generating about TWD 556 million in the third quarter largely due to the weakness in U.S.
dollar. So we've seen that level of non-op benefits slightly off than the previous quarter, but still
maintained at about 1.8% of sales.
Income before tax comes in at TWD 7.2 billion or 22.7%, slightly less than the previous quarter because
of the lower nonoperating performance, but then the income tax in the third quarter comes in at TWD
1.5 billion versus TWD 1.9 billion in the previous quarter, largely because we don't really have the
retained earning tax impact in the third quarter. So net income for the third quarter comes in at $5.7
billion or close to 18%, slightly better than the previous one.
And looking at the EPS in the third quarter is at TWD 11.01 per share. And this is on the -- after the
expanded capital base due to the [indiscernible] dividend distribution as well as some of the ECB
conversion. So we're talking about TWD 5 billion capital base in third quarter. So that EPS TWD 11,
slightly better than previous one at TWD 10.85.

EBITDA TWD 8.8 billion or TWD 8.9 billion were close to 28%, also slightly better than the previous
quarter as well. If we compare that to third quarter last year, you can see that the revenue is up almost
16%. This is largely because of the acquisition of the sales business that we completed October last year.
So it was not included in the third quarter of last year's results. You see the gross margin percentage
expanded a little bit as well due to the accretion of the acquisition, so 33.2% gross margin percentage
last year.
The OpEx was at 13.6% against 14.3% this quarter because the consolidation or the innovations going
on, we're seeing quarter-over-quarter improvement on the OpEx front. So we continue to have the
OpEx in a very controlled manner. So going down to the EBITDA margin percentage last year 27.3%
versus 27.9% this quarter. So again, accretion on the margin performance there as well.
Next page. Let's take a look at the year-to-date financials and compare that with last year, you can see
the year-to-date, we generated TWD 91.7 billion or a 14.2% increase over same period last year. And
gross margin overall improved from 33.1% to 34.7% year-to-date. OpEx 14% versus 15% this year. But
again, I think we're continuing to doing our best efforts to integrate the acquired business here. The
operating margin as well as the EBITDA margin were all showing some increments this year versus
same period last year.
Next. Let me walk you through some of the sales breakdown by different aspects for the third quarter.
You can see the quarter-over-quarter, I think the change is relatively marginal basically just plus/minus
1 percentage across the board. So MLCC, tantalum is just our magnetic sensor, maybe you are seeing a
marginal shift from quarter-to-quarter in the products.
Looking at the region, it's a pretty similar fashion as well. You can see Europe is showing a slight win
mix there, so marginally down by 1%. But then that's met by the Brazil and the rest of the Asia by about
1 percentage growth. So the mix by region hasn't really shifted that much.
Next slide. By channel, you can see that there's a swap between the EMS and direct sales by about 3%.
But all in all, the global distributors are still our main channel of recording ourselves at about 40%
there. Segment-wise, again, we're seeing more weakness in industrial sector in general, but that was
compensated by the resilience that we're seeing in computing and the enterprise systems there. So PC,
smartphones are all showing some improvements there.
Next. And here's an overview on the balance sheet. So as of the end of the third quarter, you can see the
cash balance for the company is at about TWD 94 billion, slightly up from the previous quarter. And the
-- basically, the balance sheet is fairly flat quarter-over-quarter at about TWD 358 billion. Inventory in
control as well; you can see that balance $26.8 billion versus the previous quarter, only showed about
1.3% increments there.
And on the liability front, we're able to continue to deleverage a little bit with the total liability comes in
at about TWD 203 billion and the net borrowing or the net financial debt of the company also came up
a little bit slightly less than TWD 23 billion versus TWD 24.5 billion in the previous quarter.
So if you look at the ratio of the net financial debt over equity at 14.7%, it's down by about 2.1
percentage points than previous quarter. Although we are now really back to below 10% net debt to
equity gearing level. Prior to the acquisitions last year, but then I think we're on the right track in terms
of continuing to see this trend in the balance sheet.

A similar fashion in the net financial debt over EBITDA as well, you can see the multiple is at 0.7x
versus 0.8x in the previous quarter. And the ROE is pretty stable. We're looking at annualized 14.5% as
of the end of third quarter. That compares to 13.1% of same period last year, it is a mild increment
there.
Next. So I'll leave David to comment on the outlook for the fourth quarter.
Deng-Rue Wang (Executives)
So as reported by Eddie. So we just saw the quarter 3 results in terms of revenue, gross margin and the
operating income percentage. And they were pretty much all as guided. So I have no particular
comments to comment here. If we see the quarter 4, first, let's take a look at the revenue, we have a
couple of highlights here.
And from the market, we still see that computing, communication are still in a good shape. And we also
see in the market, the pricing is pretty much stable. And internally, when we see the book-to-bill ratio,
the last 3 months average is also close to 1. But usually, in the quarter 4, traditionally, this is low
season. This is why we give you the guidance that next quarter, the revenue would be a single-digit
percentage decline quarter-on-quarter.
And in terms of gross margin percentage and the operating income percentage, we guide the low single-
digit percentage decline quarter-on-quarter. This is mainly because of the lower revenue than we just
guided in Q4. But internally, we will try to maintain the utilization, and this is mainly prepared for the
Chinese New Year inventory operation. And we also have a number of costs and OpEx control
programs. And this is why that we gave the low single-digit percentage decline quarter-on-quarter in
gross margin and the operating income percentage.
Thank you, Howard.
Howard Kao (Analysts)
[Operator Instructions] So before we get to the questions online, and while we wait for more questions
to come in, maybe I can ask the first question.
So maybe this is for Eddie. But can you just talk a little bit about your third quarter. Again, I think when
you guys were guiding for Q3, you guys were guiding for margins up low single digit quarter-on-
quarter, but it seems like both gross margin and Op margin ended up being a little bit more flattish. So
has there been any change maybe versus 3 months ago that caused margins to come in a little bit more
flattish than up low single-digit Q-o-Q.
Eddie Y.S. Chen (Executives)
Yes, if I may. I think I can pretty much tell from the sales mix that we just demonstrated in the quarter,
some decline in the industrial sector. Some of those declines are probably in better margin area. So I
think it's really the product mix shift quarter-on-quarter. That's probably the main reason.
Howard Kao (Analysts)
Got it. And speaking of product mix, and there's a question here online as well. I remember 3 months
ago, you guys mentioned industrial and automotive will continue to be weak until year-end. And maybe
we will see automotive recover first before industrials will recover. And so I guess it seems like both of
these segments, especially industrials have gone a little bit worse. So can you talk about the recovery in

terms of timing for both of these 2 end segments? And when can we expect things to stabilize and
maybe start to see some recovery?
Eddie Y.S. Chen (Executives)
We can touch base a little bit, and maybe let Claudio comment more on the marketplace. In terms of
quarter-over-quarter shipment, I think we're seeing the auto actually increased [ on our ] part by about
1 percentage, so just a mild growth there. But then I think the weakness in the industrial exposure is
probably weaker than we had expected.
This is why you're seeing in the guidance or not really live up to the guidance that we had in the
previous quarter. So I think the direction in general, it's pretty much on quarters as we expected in the
last session, but then I think magnitudes probably vary a little bit from second sector or maybe let
Claudio comment on that.
Claudio Lollini (Executives)
Yes, I will. So automotive, there is also a regional mix that plays an important role. What we observed is
areas of weaknesses for the automotive industry, particularly the EV part for the Western brands. But
actually, the opposite is true in Asia, in China, and the EV market is still quite dynamic at least for us,
we still record growth when it comes to EV presence in China for our product quarter-over-quarter and
year-over-year.
So when you -- and we do have a good engagement and good penetration in both markets. So when you
combine both together, as Eddie said. The net result has been flattish, slightly up. Now moving forward,
we don't expect next year to be a particularly exciting year at least for the traditional internal
combustion engine, number of units for EV, I think there will be growth, but maybe a little bit more
slow than previously anticipated.
Moving to industrial, it's true. Industrial is the segment that I think is the most challenging now. It's
mostly in Europe. That is a little bit of North America and a little bit of Asia and Great China, but
Europe is definitely the area where most of the industrial customers are. And they continue to have
themselves lower bookings, a bit of inventory. There has not been a whole lot of CapEx investment yet,
and you read the news of the German economy, in particular, in Europe, and not particularly positive.
So we expect another 6 months at least before we can see a significant recovery. So we are budgeting
the first half of next year for our industrial segment also cautiously.
Howard Kao (Analysts)
Got it. And in terms of outlook for Q4, there's a question if you're asking about the outlook by different
end product segments. For example, MLCC resistors, tantalum capacitor or I guess by technology, I
should say. Any color here?
Claudio Lollini (Executives)
Yes, I can give some color. In general, as Eddie and David already mentioned, Q4 is a seasonal softer
quarter than Q3 for us. Asia is a big driver for that. There is a lot of build in Q3 in preparation for the
end of the year. There are inventory correction dynamics. Europe and North America have long
holidays in Q4. There is some holiday in Asia in Q4 as well in the month of October.

So all of that said, within the product mix, we -- there are pockets of growth mostly for products that is
involved in the AI server production. We had an AI summit a few weeks ago here in Taipei. We
showcased our technology in our inductor space with our NANOMET technology, that product
continue to have positive development. But in general, all the products are looking for a softer Q4
compared to Q3, and segments as well.
Howard Kao (Analysts)
Got it. And is there any preliminary comments that you can provide in terms of 2025, either first
quarter or the full year now that we're getting closer to next year.
Deng-Rue Wang (Executives)
Well, very high level, I got to say, as we're in the middle of preparing the budget for next year, like
Claudio just said. And basically, I think we're cautiously optimistic. Some sectors are -- have been
experiencing certain weakness throughout several quarters. And we're seeing some support there. And
if you take away the seasonality, I think from '25, we're still optimistic about the potential growth.
But again, I think the market is such that we were not being hopeful that we will be bouncing back a lot
from what we have been experiencing in the past several years. So we're cautiously, but then we are
seeing signs of recovery in different elements or sectors. To that part, I think we are still relying on
certain growth in '25.
Howard Kao (Analysts)
I see. If we can just drill down a little bit on specifics on the consumer electronics space. Going to next
year, do you have any relative bullishness or cautiousness, if you compare like the PC market versus the
smartphone market? Is there any particular end segment where you're looking more optimistic going
into 2025 versus the other?
Deng-Rue Wang (Executives)
Definitely, the computing and enterprise segment is the one that we believe will have the highest
growth rate compared to the other segments. Then we do have a positive expectation out of our
defense, aerospace, medical although it's a small base, it's about 5% of what -- our business, but we
think it will develop nicely as well.
Automotive will continue to be a mix, it would be important to see if there is somewhat a recovery from
the Western branded carmakers and both EV and traditional. Industrial, I think, will be an area where
we are mostly cautious at this moment. And then we have telecom, which in fact also benefits from the
AI introduction. So that will be positive, maybe not as much as the computing and enterprise.
And consumer, we think will be positive, driven by higher discretionary spending. Mobile phones are --
hopefully are going to do a little bit better. There is introduction of new PCs, AI PCs. So all of this,
hopefully, will have to generate some revenue there. The most bullish one definitely computing an
enterprise.
Howard Kao (Analysts)
Got it. And maybe just some question on Q1 specifically. I guess Q4 now, we're seeing top line
momentum to be down seasonally, which is in line with historical Q4. But looking to Q1, are you

expecting first quarter to be similar with historical seasonality as well. So we're expecting Q1 to be up
on a sequential basis? Is that a fair kind of statement?
Claudio Lollini (Executives)
I'll be cautious to this your first quarter guidance at this junction. But then I think -- we think it will
more or less follow the seasonality pattern. Fourth quarter I think you're still seeing the guidance here,
so we're hoping there will be some balancing act in the first quarter, '25.
Howard Kao (Analysts)
Got it. And in terms of utilization rate, can you please remind us what is your utilization rate in Q3 for
both standard and premium? And what is the expectation for Q4?
Eddie Y.S. Chen (Executives)
In Q3, the utilization for standard was around 65%, and premium product 75%. And basically, although
the -- we expect a lower revenue in Q4, we will try to maintain the similar utilization in Q4. This is
mainly because we want to prepare for the Chinese New Year, because Chinese New Year in January
will be a very low month. So we need to prepare some inventory there. So the [indiscernible] is try to
maintain the same utilization in Q4.
Howard Kao (Analysts)
Got it. And in terms of your inventory turnover days, I don't know if I missed this in your prepared
remarks, but can you remind us what is your inventory turnover days for Q3?
Deng-Rue Wang (Executives)
Yes. We're sitting at around 120 days, slightly better than the previous quarter.
Howard Kao (Analysts)
And in terms of 120 days, is this a comfortable number for you guys? Or...
Deng-Rue Wang (Executives)
Yes. This is probably by far the lowest point in the year. So I think we do have a certain level of
confidence in that inventory control. And given the fact that the fourth quarter is going to be slightly
slower and then we're maintaining the utilization rate. So maybe we're seeing certain uptick of the
inventory, but there's nothing to shift majorly the turnover days. I think the content of the inventory,
for the different components of the inventory could be managed to weather through the inventory loop.
So yes, I think we're pretty comparable with that level.
Howard Kao (Analysts)
Got it. There's a question here that's a little bit more specific. But in terms of your revenue breakdown
in the third quarter by geography, Asia revenues were up 1% sequentially. Is there any color on what
specific country that this revenue was mainly coming from? Was it Taiwan, Japan?
Claudio Lollini (Executives)

Yes, rest of Asia, there's been a lot of movement of manufacturing footprint from Great China or mostly
China out to Thailand, Vietnam, Southeast Asia in general, so there's a lot of -- EMS in particular, are
doing the exact same program as before, but now they are shifting some of the assembly out of China.
So there is a little bit of that.
And that is particularly true in the computing and enterprise segment, where some of the programs,
some of the largest programs that we participate in happen to be built there. And we drive that growth
in Southeast Asia as opposed to China.
Howard Kao (Analysts)
Got it. And just to follow up on this slightly more positive outlook for computing and enterprise
segment. Will that only be for MLCC capacitor and resistor, or will we see benefits on your tantalum
business as well? Because if I remember correctly, tantalum is -- for you guys, is used quite a bit in PCs
and maybe the networking segments.
Claudio Lollini (Executives)
Yes. Indeed, most of our tantalum product is in computing and enterprise. So the -- it's no coincidence
that all the growth that we experienced -- most of the growth, I should say, that we experienced in
tantalum this year has been directly linked to computing and enterprise.
So we -- our polymer is utilized in laptop notebooks, server, AI servers. So there is a lot of benefits as
those programs ramp up and continue to grow. Our inductor product from our [ token ] brand is largely
used in some AI server program. And then, of course, MLCC resistors and capacitor in general. So a lot
of products that are benefiting from this.
Howard Kao (Analysts)
In terms of your tantalum business, is there any comment on where utilization rate is right now?
Because I remember you guys have expanded quite a lot of capacity in the past maybe 2 years in your --
for your tantalum business.
Claudio Lollini (Executives)
Yes, we have 3 main sites, which is quite exciting actually because we have capability to produce large
volumes in China, in Thailand and in Mexico. So that gives us a lot of options, a lot of proximity to
customers and utilization rate has been running now between 70%, 75% of the polymer line. So we're in
a good place. We like to have that buffer, and we are ready for some upside, should upside come, so
pretty content on that.
Howard Kao (Analysts)
Got it. And recently, there has been a lot of -- and thank you for mentioning the multiple production
facilities that you guys have. Recently, there's been a lot of concerns on potential tariffs, and how that
would impact, I guess, different businesses. How do you guys view this going forward? And do you guys
think this will have an impact on your business if there is any potential tariffs that are implemented
post the U.S. election.
Deng-Rue Wang (Executives)

Basically, I think for all the product lines we have there, we maintain multiple production lines over the
world, like for the Claudio just mentioned that like tantalum we have multiple factories like in China or
in Mexico. If you see MLCC, we have the similar things. We have the production in Mexico. We also
have the production in Taiwan and China.
So across all the product lines, we have multiple factories there. So I think when we communicate with
the customer, most of them -- almost all of them are very satisfied with this setup. So I think we can
manage the situation quite well today.
Howard Kao (Analysts)
Got it. And just to follow up on that, do you think customers are more willing or more keen to do
business with you because you guys have multiple production sites globally versus maybe some of your
peers who isn't as well diversified in terms of their production footprint geographically?
Deng-Rue Wang (Executives)
Yes. We think so, that we hope so.
Howard Kao (Analysts)
Got it. Okay. And maybe, Eddie, 1 question for you on FX. Can you remind us because right now, there's
been a lot of volatility, but any color on FX sensitivity between the U.S. dollar and Taiwan dollar on
margins?
Eddie Y.S. Chen (Executives)
Yes. You can see that impact in this quarter, in particular, honestly, what we have been doing in the
past quarter or so is trying to capitalize on the prior position that we had in early -- first 2 quarters of
the year. So we actually realized some of the positions benefits, but there are continued build up
exposures throughout the quarter. So it's kind of [ wishwash ]. So net-net, we're able to balancing that
dollar weakness during that particular quarter.
So I think year-to-date performance, I'm still pretty proud of that achievement by the team towards
volatility of the dollar throughout the year. So I think we're pretty lean right now in terms of the
exposure, particularly with regards to TWD. I think we're managing it quite well. We're okay if the
dollar continues to weaken from here. I don't think we would get to much hit from that in that trend.
Howard Kao (Analysts)
Got it. And just staying on margins. Any impact because of higher utility costs that we're seeing maybe
in Q3 or expected in Q4?
Eddie Y.S. Chen (Executives)
If you're referring to the electricity costs in Taiwan, yes, there will be some effect on some of our
operations here in Taiwan. But then I think we have taken some internal review on that. And it's -- the
impact is still marginal given the scale and the operational environment right now. But then I think the
team is working on it to try to withstand that increment of utility cost. I think it's still manageable right
now.
Howard Kao (Analysts)

Okay. Got it. And in terms of revenue mix for servers specifically, is there any update on what that is as
a percentage of revenues at the end of Q3. I remember, I think maybe second quarter or first half server
revenues were around 6% of total revenue. I was just wondering if that has changed for the third
quarter.
Eddie Y.S. Chen (Executives)
Yes, I have to say that it's kind of a high level. But then given the fact that we probably have no control
whatsoever with regards to the product that gets applied in different devices or system. But then our
best guess is -- we're still around that level, probably slightly higher than that given the momentum
we're seeing from the customer activities. So probably that high single-digit percentage is still pretty
much what we're exposed to right now.
Howard Kao (Analysts)
Okay. Got it. In terms of the China market, have you guys seen any significant pickup in terms of why
good demand recently, like household electronics?
Deng-Rue Wang (Executives)
So thanks for the question. Actually, our China market, as you know, we have an extensive local
distribution network in China, is one of our biggest strengths. We commend more than 60, 65 local
distributors that can really help us to reach and penetrate a lot of customers in a lot of geographies and
provinces in China.
And last year was a challenging year. But this year, our China business is up year-over-year double
digit, and it's been up since January. And we kept that momentum up until now, slowing down only
slightly really. So for us, that geography, which is -- in that distribution business, there is a lot of
consumers, so what goods are in there, it's been pretty good so far this year.
Howard Kao (Analysts)
Okay. Got it. Maybe can we just come back to inventory. I remember 3 months ago on your third
quarter -- sorry, second quarter earnings call, you mentioned your global distributor inventory is 7 to 8
months, a little bit higher than the average of 4 to 6. Is there any updates here on where global
distributor inventory is? And maybe some color on China distributor -- Greater China distributor
inventory as well.
Claudio Lollini (Executives)
Yes, I can cover that. The global distribution inventory, we separate into 2 portions. One is the high
service channel, which tends to run with a much larger inventory and that has been stable. And then
the other portion is the volume, large global distributors. And that inventory came down steadily over
the last year.
Now it's still sitting probably a little bit higher for our liking maybe a month too much. It's about 5
months on hand based on their last 3-month average POS 5, 5.5. We think that the right number there
should be more like between 4 to 5. So it's not too far. And if POS were to pick up just slightly then you
are there in terms of months on hand.

When it comes to China distribution, actually, they built a little bit of inventory. They were down to less
than 3 months on hand a few months ago, and that was way too low. And as I said, that business in
China has been growing double digits. So now they build a little bit of inventory and they are sitting on
about 3, 3.5 months on hand, up about a month versus a couple of quarters ago.
Howard Kao (Analysts)
Got it. So with that inventory up to 3 to 3.5 months in China, I guess that's not something that you guys
are too worried about given the strength of your China business that you've seen in the past couple of
quarters?
Claudio Lollini (Executives)
No, no, no. It's very dynamic, and we respond very quickly there in either direction. So not a concern at
all.
Howard Kao (Analysts)
Got it. In terms of your product portfolio, this is a question here on where you see higher growth
especially now that we have a larger inductor business post the consolidation of Chilisin. So I guess, in
terms of just overall portfolio, again, by end segments, where do you see growth to be higher from here
maybe in the next 1, 2 years.
Deng-Rue Wang (Executives)
Going back to the principle of having a computing and enterprise segment that is going to lead the way,
then you cascade down the main product in that segment, a combination of tantalum polymer capacitor
and inductors, yes. So there will be growth in inductors as well. And then other capacitor and resistor,
mostly MLCC directory or chip and resistors.
Now when it comes to products like our film and aluminum electrolytic capacitor as an example, or a
portion of our portfolio in ceramic in particular, the KEMET brand, those products are also used in
industrial and automotive as well as some of the legacy past portfolio. And for those products, then
growth will be delayed a little bit depending on the end market.
Howard Kao (Analysts)
Got it. I guess I have to -- I've been asking every single quarter. So I'm going to stick to the tradition,
but AI revenue mix, right? I know you guys don't really talk about this, but I think Pierre mentioned to
maybe some reporter post your AI Summit that revenue is around 5%. So I won't specifically ask on
this. But just wondering, within your product portfolio capacitors and MLCC, tantalum resistor,
inductor, which segment is bigger geared towards AI maybe or just by ranking, any color you could
provide here?
Deng-Rue Wang (Executives)
Yes. Computing and enterprise has the biggest exposure towards AI. After that -- and we put laptop and
notebook within computing and enterprise. So you also have AI notebook would be in there. Then after
that, I would say the 2 segments where you will see AI presence the most after computing and
enterprise will be telecom and then consumer, consumer products. Not necessarily this translate into

the same growth of componentry that you might have in computing and enterprise, but you will have it
there.
And then eventually, you will have AI also in industrial and automotive, of course -- actually,
automotive is the second segment where I think the AI play is the biggest, right, because of the
autonomous vehicle and all the assistant driving elements that you have in a car these days.
So it's really permeating across all segments. If you were to rank, I would put computing and
automotive first, telecom and consumer second, and then industrial being perhaps the last one to
benefit from AI.
Howard Kao (Analysts)
Got it. Very helpful. But in terms of what product technology like capacitor versus resistor versus
inductor, any comment on which one is bigger geared towards AI, would inductor be more geared
towards...
Deng-Rue Wang (Executives)
But they all are used in a lot of segments, but I'm sure you've seen the news. If you just zoom in into the
growth of the AI server, the growth in the bond around MLCC is significant, high capacitance
componentry is, in particular, the one with the biggest growth.
For us, the way we look at it, capacitors, tantalum polymer because we have that in our portfolio, high
capacitance MLCC and resistors and inductors will all benefit first. And then behind that, there will be
film, aluminum electrolytic, other type of magnetic componentry maybe larger, mostly for industrial
and automotive.
And then MLCC in general, is used in any application. So that will benefit every time there is increase of
electronic content, you will see that benefit.
Howard Kao (Analysts)
Got it. And lastly, maybe just a quick follow-up and update on your progress regarding active
components now that we've talked about passive components for the majority of this call. So any
updates on active components, either in terms of synergies or any updated progress that you guys have
for the next couple of quarters.
Deng-Rue Wang (Executives)
We continue to explore opportunities. In particular, we have been, as you know, co-working with [
APAC ] and uPI, we have been selectively approaching our distribution channel for some stocking
packages of selected product. For example, we've been looking at MOSFET's product offering in various
voltages, and we've been doing some crossing.
So far, a lot of preliminary activity and market study. And then we'll have to -- it's mostly a plan for the
following years, not something that we look for growth in this particular calendar year yet.
Howard Kao (Analysts)
Got it. So I think we are finished with the questions that we have online. Maybe I will hand it over back
to Eddie or David to see if you guys have any closing remarks?

Deng-Rue Wang (Executives)
Yes. Thank you, Howard. So basically, we think Q4 is our low season. So that's why we give this
guidance. But the -- actually, there's nothing to worry. And for the growth trend like computing or
telecom segment, I think we are following this trend by the way. And maybe we need to be a little bit
more patient in the industrial, so it's -- got to say that it might take another 3 to 6 months to come back.
So I think we -- for the current situation, we still can maintain and deliver a relatively good, stable
performance, and product and the capacity-wise, we are ready. We are ready to win the market and
bounce back.
Thank you, Howard.
Howard Kao (Analysts)
Great. Thank you, David, for your closing remarks. This concludes our webcast today. Thank you,
everyone, for joining us, and thank you, again, David, Eddie and Claudio for your time and sharing your
thoughts with us. We will see you all next time.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2327.TW_Q2_2024_Earnings_Call_20240730.md
- 2024-07-30｜CEO Deng-Rue Wang｜guidance：CEO 給 Q3 營收低個位數成長，理由為 AI/運算/通訊/消費動能與通路庫存健康。（原話："we will guide the low single-digit growth."）
- 2024-07-30｜CEO Deng-Rue Wang｜guidance：CEO 表示不預期 V 型反彈，需求為溫和回補。（原話："we don't see that there will be a V"）
- 2024-07-30｜CFO Eddie Chen｜margin：Q2 毛利率 35.1%，較上季高 1.3 個百分點，為兩年來首度回到 35%。（原話："The gross margin also improved to 35.1% or TWD 11 billion."）
- 2024-07-30｜CFO Eddie Chen｜margin：Q2 營收 314 億台幣，季增 10.2%，優於前次財測，主因 AI 相關動能與部分消費性產品。（原話："the company has reported TWD 31.4 billion sales"）
- 2024-07-30｜CEO Deng-Rue Wang｜margin：Q3 毛利率財測：價格穩定、稼動率微升、持續成本改善（原文為 below single-digit，實為低個位數改善之意）。（原話："we see the utilization in quarter 3 was slightly improved."）
- 2024-07-30｜CEO Deng-Rue Wang｜margin：CEO 給出稼動率：Q3 premium 產品由 70% 升至 75%。（原話："from quarter 2, 70% to next"）
- 2024-07-30｜CEO Deng-Rue Wang｜margin：分析師確認稼動率提高降低單位成本，CEO 回答正確；並說明提高 commodity 稼動率是為補自家庫存。（原話："So that's why we want to increase the utilization"）
- 2024-07-30｜CEO Deng-Rue Wang｜margin：OpEx 口徑：僅配銷成本隨營收變動，約占 2%~3%，其餘為相對固定成本，故不給 OpEx 比率目標。（原話："Around 2% to 3%. This is the distribution cost."）
- 2024-07-30｜CFO Eddie Chen｜margin：CFO 稱 OpEx 預期隨收購相關交易成本消退而逐步改善，但無長期目標。（原話："But I don't have a long-term targets per se for that matter."）
- 2024-07-30｜CFO Eddie Chen｜margin：CFO 拆解 Q2 OpEx：金額 45 億，占營收 14.5%（Q1 為 16.4%）。（原話："So TWD 4.5 billion spending OpEx dollars"）
- 2024-07-30｜CFO Eddie Chen｜margin：CFO 拆解非本業：Q1 含日本投資處分的資本利得，剔除後季對季相近。（原話："divestitures of our investments in Japan"）
- 2024-07-30｜CFO Eddie Chen｜product：產品別：MLCC、感測器季對季動能放緩，鉭質電容升溫。（原話："So we've seen tantalum is picking up the momentum."）
- 2024-07-30｜CEO Deng-Rue Wang｜product：鉭質電容訂單：book-to-bill 為正、接單穩定、積壓訂單小幅增加，與去年多數時間不同。（原話："Booking is stable and backlog is slightly building."）
- 2024-07-30｜CEO Deng-Rue Wang｜product：鉭質電容最大宗為筆電，另含 SSD、伺服器與 EV。（原話："Largest portion was notebook."）
- 2024-07-30｜CFO Eddie Chen｜customer：區域別：歐洲占比季減 3%，美中升溫。（原話："Europe is probably suffering more than the rest"）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：終端排序：消費、筆電、手機、SSD、伺服器強；工業（尤其歐洲）偏弱，Q3 趨勢相同。（原話："We probably rank Q3 in a similar way as year-to-date."）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：工業需求：下半年大致與上半年相同，期待明年需求轉強。（原話："we'll probably look at next year for the stock to digest"）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：管理層不追蹤 AI 營收，不提供 AI 占比。（原話："We do not track revenue linked to AI"）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：Q2 優於預期來自整體需求，非未預期的單一新專案。（原話："nothing unexpected in terms of a particular design that we"）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：通路庫存下降趨勢已穩定逾一年，Q3 預期延續；EMS/直接客戶庫存能見度較低。（原話："where we have less visibility."）
- 2024-07-30｜CEO Deng-Rue Wang｜customer：Q2 book-to-bill 約 1 或略高，部分來自通路補庫，Q3 預期同趨勢。（原話："The ratio was positive in Q2, around one or slightly better"）
- 2024-07-30｜Deng-Rue Wang（逐字稿標註）｜competition：車用相對同業跌幅較小，歸因於 KEMET 帶來的車廠關係與設計導入，稱在特定技術上取得份額。（原話："we were gaining share for sure in certain technologies"）
- 2024-07-30｜CEO Deng-Rue Wang｜competition：MLCC 與各終端未偵測到顯著價格變動；電感未跟隨日系同業漲價。（原話："We haven't really detected any significant price change"）
- 2024-07-30｜CEO Deng-Rue Wang｜competition：電感成本：該領域未遭受大幅成本衝擊。（原話："We haven't really suffered a large cost impact"）
- 2024-07-30｜CFO Eddie Chen｜competition：電源 IC 佈局仍在早期，自稱未與大廠並列。（原話："I would say this is still very initial stage, right?"）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：CapEx 約占 EBITDA 15%~20%，以維持性為主，不積極擴產。（原話："still spending about a 15%, 20% of our EBITDA"）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：廣州新廠第一期持續爬坡，為市場回溫預先備產能。（原話："So that Phase 1 expansion is still on that."）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：持有 UPI 約 20%，視為投資策略延伸，以權益法認列於非本業。（原話："So right now, we're having about 20% in UPI."）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：資產負債表：現金 920 億，淨負債/權益 16.7%，仍高於收購 Telemecanique 前的 11.2%。（原話："The net debt to equity"）
- 2024-07-30｜CFO Eddie Chen｜capital_allocation：庫存週轉天數降至約 120 天，為過去 5~6 季最低；預期庫存動態無大變化。（原話："So right now, we're saying about 120 days."）
- 2024-07-30｜CFO Eddie Chen｜risk：關稅影響難預測，需保持彈性。（原話："it's hard to predict, honestly."）
- 2024-07-30｜CEO Deng-Rue Wang｜risk：地緣政治：客戶討論供應韌性，部分客戶要求特定原產地，電信/5G 客戶最在意。（原話："Some customers are being more forward in requesting specific"）
- 2024-07-30｜CEO Deng-Rue Wang｜risk：成本轉嫁政策：過去曾在無法吸收成本時向客戶反映，目前不在該情況。（原話："But we are not in that"）
- 2024-07-30｜CEO Deng-Rue Wang｜commitment：CEO 表示稼動率是否達 90% 取決於終端需求與庫存，不給前瞻預測，僅承諾需求改善時逐步拉升。（原話："I cannot give you an outlook"）
- 2024-07-30｜CEO Deng-Rue Wang｜commitment：CEO 結語：認為景氣已落底、逐步復甦，正向動能延伸至下一季。（原話："still see this positive momentum extended into next quarter"）

### 問答異常語氣（迴避／改口／保留）
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：AI 占營收是否約個位數中段百分比？｜答法：未回答占比，改稱不追蹤 AI 營收並指出消費/個人電腦亦貢獻。
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：OpEx 比率是否有可追蹤的新目標（如 13%~13.5%）？｜答法：拒絕給數字目標，改談逐步改善與變動成本結構。
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：稼動率何時可達 90% 以上？｜答法：不給前瞻預測，僅稱取決於終端需求與庫存。
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：是否有庫存跌價回沖的機會？｜答法：CFO 先稱不知如何重述問題，未直接回答是否有沖銷回沖，改談投資組合與庫存週轉。
- 2327.TW_Q2_2024_Earnings_Call_20240730.md｜問：高稼動率 vs 低個位數營收財測，混合 ASP 是否下降？｜答法：未回答 ASP，改談自身庫存重建與可供應量。

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

## ⑥ 條件附卡（archetype_hint='循環/商品' 命中）：judge_addendum_cyclical.md

<!-- source: .claude/skills/stock-analyst/references/cyclical-lens.md sha256:b13d95972edd47ea git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary 或 secondary ∈ {循環/商品，EMS/ODM}（QC-43 判定，含 capex 建設循環／需求量循環子型） -->

# QC-42 循環交易讀數（附錄 B）附卡

循環股的錢在 Game 2（投降買、延伸賣）。本附卡是平行、明標投機的交易讀數，不改長抱裁決。[§WHY]

## 一、觸發與子型判定
無循環 sleeve（純成長 mis-route）→ 整段省略。[§①]
商品子型（下列≥2命中→用商品 through-cycle 錶）：近5-7年≥1個GAAP虧損年｜peak-to-trough毛利率擺動>~20pp｜營收主由商品ASP驅動(price-taker)｜產業∈{記憶體/DRAM/NAND、礦業/材料/稀土、化工、航運、鋼鐵、太陽能、油氣E&P、部分晶圓/設備}｜capex/rev結構性>15%且ROIC高度擺動。未達≥2仍判循環→依驅動來源選capex建設循環錶或需求量循環錶。[§商品子型]

## 二、循環位置錶族（三選一，錨自身 through-cycle 區間非動能；位置落 深谷投降/早循環/中循環/晚循環/過熱頂部，多數決+sourced 裁決）
商品 through-cycle（MU 型，6 訊號）：P/B vs 自身區間(近1x/下緣=買，>中位2x/上緣=賣)｜量 vs 價(量增領先=買，ASP-only量平降=賣)｜GM vs自身區間(近谷/負=買，近峰=賣)｜供給紀律(減產=買，新產能洪水=賣)｜庫存(去化乾淨=買，通路+公司堆積=賣)｜情緒/部位(投降PT>價=買，狂熱PT<價=賣)。[§B.1商品]
capex 建設循環（ORCL 型，6 訊號）：capex/折舊比(低/正常化=買，遠高於1=賣)｜產能利用率爬坡(低基期回升=買，滿載見頂=賣)｜RPO(backlog)vs capex覆蓋(backlog領先=買，capex超前需求=賣)｜交易對手信用(客戶分散信用強=買，集中燒錢客戶=賣)｜情緒/部位(同上)｜量vs價(量增領先=買，ASP承壓量見頂=賣)。[§B.1capex]
需求量循環（EMS/ODM，JBL 型，5 訊號）：book-to-bill/需求量拐點(>1拐點向上=買，<1量見頂=賣)｜客戶庫存去化(去化乾淨=買，通路+客戶堆積=賣)｜倍數vs自身歷史re-rate均值回歸(近下緣=買，>5Y中位×1.5/貼峰=賣)｜終端·hyperscaler capex週期位置(早週期=買，晚週期見頂=賣)｜情緒/部位(同上)。[§B.1需求量]

## 三、交易姿態 + 反動能硬閘（跨子型通用，逐條檢查，觸發即 override 向保守）
位置→姿態：深谷投降→積極分批建立｜早→分批建立｜中→持有不加｜晚→分批了結｜頂→清光不碰。[§B.2]
閘1 位置=晚/頂→姿態不得為任何「建立」。閘2 成長=ASP-only+量持平/降→最多「持有」。閘3 P/B>自身中位2x→禁新建立。閘4 訊號矛盾→標「位置不明，觀望」不硬給姿態。閘5 TTM/Fwd本益比或EV倍數>自身歷史高區(>5Y中位×1.5、或貼/破歷史峰)→禁新建立。[§閘1-5]

## 四、落欄與 §13 row 8b 接線
`cycle_position`(深谷投降｜早循環｜中循環｜晚循環｜過熱頂部)＋`cycle_verdict`(右側可追蹤｜等回踩｜頂部觀望｜未觸發)；非循環 archetype 不填，整欄省略。[§落欄]
接 §13 row 8b：位置∈{深谷投降，早循環}+五閘全過+moat底線+獨立critic冷讀通過→落「進場・條件式(循環衛星)」(倉位上限3%)；任一不成立→只落研究提名，§13維持觀望。驗證失敗不得升級，只能降回觀望。`trade_stance`僅進HTML不入dd-meta。[§row8b]

## 五、雙制度與兩軌背離
有 secular sleeve + commodity sleeve → 循環鏡頭只套 commodity sleeve，secular sleeve 一句話另計(不隨循環賣)。[§⑤]
投資軌(§13長抱視角) vs 交易軌(本鏡頭位置)：底部背離(長抱視角迴避 + 循環位置深谷投降/早循環)是本鏡頭獨門訊號；頂部多收斂(皆遠離)。[§B.3]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260526","verdict":"B 觀望（thesis 完整：產業 🟢 + A 級護城河 8.5 + AI 🟢；但 4W +110.7% 動能極端過熱、短中期 R:R 失效（雙負）、Pure MA ✅ 但 BB 上軌 +18.6% stretched；等回測 BB 中軌 NT$328 或 W52 NT$235 + Q3 26 AI 占比 ≥ 16% 三條件後試倉 3-5% 衛星）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI server MLCC 滲透率上升 → AI 占營收比結構性擴大","columns":{"2Y 驗證點":"2026 Q4 AI 占比達 18%+；2027 達 22%+","5Y 驗證點":"2030 AI 占比達 30%+，AI 業務 GM ≥ 45%","10Y 驗證點":"2035 後 AI MLCC 成為主流業務","具體數字門檻":"Q2 2026 法說 AI 占 ≥ 16%；FY26 末 ≥ 20%","信息來源":"Yageo Q1 26 法說、TrendForce","漂移觸發":"連 2 季 AI 占比未達門檻 → 削弱"}},{"id":"H2","text":"MLCC pricing 漲價週期持續 + Yageo 無新擴產 → margin 擴張","columns":{"2Y 驗證點":"2026 全年 GM ≥ 38%（vs FY25 36.2%）；OM ≥ 26%","5Y 驗證點":"2027-28 cycle 平穩期 GM 維持 35-38%；OM 24-27%","10Y 驗證點":"2030+ cycle peak 後 normalize GM 32-35%","具體數字門檻":"2026 H2 spot pricing 環比 +5%+；GM YoY 持續擴張","信息來源":"TrendForce、Digitimes、Yageo 法說","漂移觸發":"連 2 季 GM YoY 下滑 &gt; 1.5pp → 反轉"}},{"id":"H3","text":"Shibaura 整合 + 多元化降低 cycle 波動","columns":{"2Y 驗證點":"2026 H2 Shibaura full integration；2027 感測器業務貢獻 EPS ≥ 5%","5Y 驗證點":"2028-30 多元化業務（感測器 + EMC + 工業）占比達 30%+","10Y 驗證點":"2031+ 國巨成為 「multi-component diversified passives leader」","具體數字門檻":"FY26 感測器業務 Revenue ≥ NT$8B；2027 occupy ≥ 8% Rev","信息來源":"Yageo FY25 年報、Schaffner / Shibaura 整合進度","漂移觸發":"2027 H1 仍未產生 synergy → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"4 週 +111% 動能 mean reversion + 股價短期 -30 至 -50%","columns":{"對應假設":"H2 / 估值","時間尺度":"⚡ 短期（1-2 月）","監測指標":"股價 vs BB 中軌 / 漲跌幅","警戒閾值":"5/27 起 5-10 日內回檔 &gt; -15% → 動能消化開始；&gt; -30% → 短期支撐測試"}},{"id":"R2","text":"Murata Izumo 全速量產 → 供給轉鬆 → 漲價週期反轉","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Murata 月度產能利用率 / spot pricing","警戒閾值":"2026 Q4 spot price 環比 &gt; -10% → 削弱；2027 H1 連 2 季 -10%+ → 反轉"}},{"id":"R3","text":"AI hyperscaler capex 結構性下修 + AI server 出貨放緩","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年）","監測指標":"Microsoft / Amazon / Google capex guidance / NVDA DC Rev","警戒閾值":"2027-28 top 4 hyperscaler capex YoY 連 3 季 &lt; +10% → 警戒；&lt; 0% → 結構反轉（≥ 50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"加深","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":668,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2327.TW_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
