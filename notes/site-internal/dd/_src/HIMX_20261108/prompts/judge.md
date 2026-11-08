你是 stock-analyst **v20 判斷 agent**，標的 HIMX（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"HIMX","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":246.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Himax Q3 2026 新聞稿（2026-11-05）"}},{"id":"f_kpi1_gaap","label":"GAAP 毛利率","value":34.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Himax Q3 2026 新聞稿"},"note":"公司指引約 34%，符合"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":9.2,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"%（營業利益 22.7m USD）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Himax Q3 2026 新聞稿；營業費用 61.8m（QoQ +21.9%，含員工獎金 11.9m 對 Q2 的 0.2m）"}},{"id":"f_kpi3_ads","label":"稅後淨利／每 ADS 盈餘","value":18.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m；EPS 10.7 美分／ADS","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Himax Q3 2026 新聞稿"},"note":"高於公司指引 8.0–10.0 美分"},{"id":"f_kpi5_q4_2026","label":"管理層指引：Q4 2026","value":"營收 QoQ −22% 至 −26%（約 182.6–192.5m USD，由 Q3 回推）；毛利率持平至微升；EPS 4.5–6.5 美分／ADS（不含預計 Q4 完成的出售利益，稅前約 23–24m、稅後約 19–20m）","period":"Q3 2026（公告於 2026-11-05）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（公告於 2026-11-05）","citation":"Himax Q3 2026 新聞稿"}},{"id":"f_kpi6","label":"現金及其他金融資產","value":285.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Himax Q3 2026 新聞稿（期間派發股利 44m）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_himx_gross_margin_pct","label":"HIMX 毛利率","value":31.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HIMX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_himx_operating_margin_pct","label":"HIMX 營業利益率","value":4.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HIMX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_himx_fcf_margin_pct","label":"HIMX FCF 利潤率","value":3.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HIMX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3034_tw_gross_margin_pct","label":"3034.TW 毛利率","value":39.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3034.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3034_tw_operating_margin_pct","label":"3034.TW 營業利益率","value":19.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3034.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_3034_tw_fcf_margin_pct","label":"3034.TW FCF 利潤率","value":14.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3034.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_simo_gross_margin_pct","label":"SIMO 毛利率","value":50.54,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIMO.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_simo_operating_margin_pct","label":"SIMO 營業利益率","value":21.3,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIMO.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_simo_fcf_margin_pct","label":"SIMO FCF 利潤率","value":-24.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIMO.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amba_gross_margin_pct","label":"AMBA 毛利率","value":58.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMBA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amba_operating_margin_pct","label":"AMBA 營業利益率","value":-14.9,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMBA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amba_fcf_margin_pct","label":"AMBA FCF 利潤率","value":2.33,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMBA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_lscc_gross_margin_pct","label":"LSCC 毛利率","value":68.62,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LSCC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lscc_operating_margin_pct","label":"LSCC 營業利益率","value":13.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LSCC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lscc_fcf_margin_pct","label":"LSCC FCF 利潤率","value":24.71,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LSCC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_23_9m_3_9m","label":"自由現金流（營業現金流 23.9m − 資本支出 3.9m，推算值，公司未報）","value":20.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-11-05）","citation":"Himax Q3 2026 新聞稿（OCF、capex）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":8.49,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-51.44,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":28.68,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.47 → 0.47）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.3 → 1.3）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.45 → 2.45）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":0.47,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.3,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":2.45,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 0.47 → 0.47（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":40.43,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.69,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.09,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":18.06,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 0.47，分子＝快照價 8.49","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.968,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":351.51,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 636.83、現金 285.32（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":174.43,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1832.39,"period":"2026-11-08","unit":"USD m","basis":"市值 1480.88 ＋ 淨負債 351.51","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":949.39,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（2 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":1230.6,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（2 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.93,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 8.49 / W52 11.71 / W104 9.87 / W250 7.58 / W250 13週斜率 0.2%"},{"id":"f_ma_w52","label":"52 週均線","value":11.71,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":9.87,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":7.58,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.2,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F 風險因素：中國大陸面板廠扶植本土 IC 供應商的政策對 Himax 構成重大挑戰且可能加劇競爭；部分對手隸屬面板客戶，具早期取得產品藍圖與 design-in 優先權的優勢。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Also in recent years, policies adopted by Chinese mainland panel manufacturers to actively introduce domestic IC suppliers have posed significant challenges to our business and may continue to intensify competition in the markets in which we operate.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"車用領域 Himax 為全球龍頭：車用 DDIC 約 40% 份額、TDDI 過半、local dimming TCON 更高；in-cell TDDI 對手含 Novatek、Synaptics、FocalTech、ESWIN、Chipone、OmniVision、Ilitek。","source":"SEC EDGAR 20-F FY2025 Item 5 / Item 4.B","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Himax continues to lead the global automotive display driver IC market, holding approximately 40% market share in DDIC, well over half of market share in TDDI, and an even higher share in local dimming TCON.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"20-F FY2025 揭露：最大客戶 A（含關係企業）占營收 28.7%/26.4%/24.0%（2023/2024/2025），客戶 C 為 11.0%/8.3%/7.8%；前十大客戶占 71.3%（2025）。","source":"SEC EDGAR 20-F FY2025 Item 4 Customers","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Our ten largest customers together accounted for approximately 74.1%, 73.6% and 71.3% of our revenues in 2023, 2024 and 2025, respectively. In 2023, 2024 and 2025, our two largest customers accounted for 10% or more of our net revenue: customer A and its affiliates accounted for 28.7%, 26.4% and 24.0% of our revenues, respectively; and customer C accounted for 11.0%, 8.3% and 7.8%, respectively.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"20-F 風險因子：數家面板廠具自行設計能力，若客戶自研可替代產品將減少或停止採購。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Moreover, several Panel Manufacturers have in-house design capabilities and therefore may not need to source semiconductor products from us. If our customers successfully develop in-house capabilities to design and develop semiconductors that can substitute for our products, they would likely reduce or stop purchasing our products.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025年Customer A（含關係企業）占營收24.0%（2023年28.7%、2024年26.4%）；Customer C 占7.8%；前兩大合計逾33%，前十大合計71.3%。","source":"SEC EDGAR 20-F FY2025, Item 4 Customers","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Our ten largest customers together accounted for approximately 74.1%, 73.6% and 71.3% of our revenues in 2023, 2024 and 2025, respectively. In 2023, 2024 and 2025, our two largest customers accounted for 10% or more of our net revenue: customer A and its affiliates accounted for 28.7%, 26.4% and 24.0% of our revenues, respectively; and customer C accounted for 11.0%, 8.3% and 7.8%, respectively.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025年底對Customer A應收帳款5,780萬美元，占應收帳款淨額約28.8%；公司自述集中度提高信用風險，且曾對部分客戶延長付款條件。","source":"SEC EDGAR 20-F FY2025, Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"As of December 31, 2025, our accounts receivable from Customer A and its affiliates were $57.8 million, which represented approximately 28.8% of our accounts receivable, net. The concentration of our accounts receivable exposes us to increased credit risk. Moreover, we have at times agreed to extend the payment terms for certain of our customers.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025年約73.8%營收來自總部在中國的客戶（2024年73.4%）。","source":"SEC EDGAR 20-F FY2025, Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"In 2024 and 2025, approximately 73.4% and 73.8% of our revenues, respectively, were from customers headquartered in the PRC.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 報導：記憶體三大廠下一波新產能多自 2028 起才釋出；DRAM 新供給自 2027 起分波釋出（記憶體缺貨為主，非 HIMX 直接產品）","source":"TrendForce, Global DRAM Capex Surge: Phase-In Capacity from 2027","url":"https://www.trendforce.com/research/download/RP260826IN","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Astute Group（2026-05）預期封測產能於 2026 年底逐步緩解，晶圓供給在新廠量產前仍吃緊","source":"Astute Group, 05 May 2026","url":"https://www.astutegroup.com/?p=59281","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Himax 管理層表示 AI 需求使成熟製程的晶圓代工、封裝、測試產能吃緊，推升製造與採購成本、拉長交期","source":"Himax Q4 2025 / 2026 earnings call coverage (MarketBeat)","url":"https://www.marketbeat.com/earnings/reports/2026-2-12-himax-technologies-inc-stock/","excerpt":null,"as_of":"2026-02-12","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Himax Q2 2026：毛利率 33.1%（Q1 30.4%、去年同期 31.2%），車用 TCON 需求強勁，Q3 營收指引季增 7%–11%","source":"MarketBeat, Himax Q2 earnings call highlights 2026-08-06","url":"https://www.marketbeat.com/instant-alerts/himax-technologies-q2-earnings-call-highlights-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Himax Q1 2026 營收年減 7.5% 至 1.99 億美元，近兩年營收年均下滑 5.2%（StockStory 式分析）","source":"Barchart, Himax Q1 coverage","url":"https://www.barchart.com/story/news/1821662/himax-technologies-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"WSTS 春季預測 2027 全球半導體市場再成長 27% 至約 1.9 兆美元；SEMI 預估 300mm 設備支出 2026 $116B、2027 $120B、2028 $138B","source":"WSTS / SEMI via search results (Tom's Hardware, eeNews Europe)","url":"https://www.eenewseurope.com/en/semi-300mm-fab-equipment-spending-worldwide-to-hit-374b-by-2028","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 20-F：公司稱截至年報日，未涉及、也未知悉任何經管理層判斷可能對業務、財務或營運造成重大不利影響的法律程序、調查或求償；一手紀錄無反壟斷調查。","source":"SEC EDGAR 20-F FY2025 Item 8.A.7 Litigation","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"we are not currently a party to, nor are we aware of, any legal proceeding, investigation or claim which, in the opinion of our management, is likely to have a material adverse effect on our business, financial condition or results of operations.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"20-F 提及部分產品或技術對特定客戶可能需額外出口許可，受美國商務部 BIS 的 EAR 管轄（出口管制屬產業特定監管風險）。","source":"搜尋摘要（轉述 Himax FY2025 20-F）","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Extra export license may be needed for certain product or technology for certain customers. These licenses are regulated by Export Administration Regulations (EAR) which is administered by the U.S. Department of Commerce's Bureau of Industry and Security (BIS).","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Himax 20-F 風險因子：產品／技術對部分客戶可能需額外 EAR 出口許可；若客戶或晶圓代工、封測供應商被列入 BIS Entity List，公司可能須暫停銷售或服務，並可能出貨延遲。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Extra export licenses may be needed for certain product or technology for certain customers. These licenses are regulated by Export Administration Regulations (EAR) which are administered by the U.S. Department of Commerce’s Bureau of Industry and Security (BIS).","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Himax 20-F 風險因子：美國或他國可能對台灣公司產品課新關稅，並可能促使客戶將半導體供應鏈移出高地緣風險地區。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Changes in U.S. and international trade policies, including the possibility that new tariffs could be imposed by the U.S. or other countries on Taiwanese company products, may adversely impact our business and operating results.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 大尺寸驅動 IC 營收年減 28.0% 至 $90.7M，公司歸因於關稅與地緣不確定性等弱總體環境；中小尺寸年減 8.0% 至 $575.1M，智慧手機與平板受關稅相關不確定性影響。","source":"SEC EDGAR 20-F FY2025 Item 5","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Amid slowing end-market sell-through and tariff-related uncertainties, smartphone and tablet sales were particularly impacted.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Himax 20-F(FY2019)揭露 TSMC 與 Vanguard 歷來製造其絕大部分晶圓，晶圓代工集中於台灣。","source":"Himax Form 20-F FY2019 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465920037959/tm206809-1_20f.htm","excerpt":"Limited, or TSMC, and Vanguard International Semiconductor Corporation, or Vanguard, historically manufactured substantially all of its wafers","as_of":"2020-03-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Himax 20-F(FY2017)揭露部分產品只在單一晶圓廠生產，更換晶圓廠或製程需數季驗證。","source":"Himax Form 20-F FY2017 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001342338/000114420418017279/tv488580_20f.htm","excerpt":"certain of our products are manufactured at only one of these foundries","as_of":"2018-03-31","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Himax 2025 Q1 財報稱正深化台灣供應鏈並擴展至中國、韓國、新加坡，以降低地緣風險。","source":"Himax Q1 2025 results (GlobeNewswire via researchpool)","url":"https://app.researchpool.com/provider/globenewswire/himx-himax-technologies-inc-reports-first-quarter-2025-financial-results-pr-XJfXLbLkeB","excerpt":"Himax is deepening its well-established Taiwan supply chain and strengthening into CN, KR, SG to enhance production flexibility, cost competitiveness and mitigate geopolitical risks.","as_of":"2025-05-08","retrieved_at":"20261108","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 指引：營收季增 7–11%；大尺寸驅動 IC 預期季減個位數%，中小尺寸驅動 IC 季增高個位數 %，車用驅動 IC 季增兩位數 %","source":"MarketBeat, Himax Q3 2026 guidance / Q2 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/himax-technologies-q2-earnings-call-highlights-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"CPO：Himax 與 FOCI 於 Q3 2026 開始支援 1.6T/3.2T/6.4T 的 CPO 產品工程量產爬坡（WLO 數字未查到）","source":"MarketBeat, Himax Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/himax-technologies-q2-earnings-call-highlights-2026-08-06/","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"市佔：公司稱車用 DDIC 全球約 40%、車用 TDDI 逾五成；Q2 2026 車用驅動銷售季增兩位數；已與客戶協商調價分攤成本，部分漲價 Q2 生效；金價與成熟製程產能偏緊為成本壓力；Novatek 與新進者加劇競爭","source":"MarketChameleon / Himax Q1-Q2 2026 coverage","url":"https://marketchameleon.com/articles/b/2026/5/8/himax-growth-2026-automotive-ai","excerpt":null,"as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"WSTS 2026 春季預測：2026 全球半導體市場約 1.51 兆美元，2027 約 1.9 兆美元（+26.6%）；記憶體 2027 約 1.06 兆（+32.1%）；類比 +6.6%、感測器 +6.9%","source":"TelecomLead, WSTS Raises Semiconductor Forecast","url":"https://telecomlead.com/?p=126102","excerpt":null,"as_of":"2026-06-04","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"20-F 風險因素：數家面板廠具自行設計能力，若客戶成功自研可替代本公司產品的半導體，將減少或停止採購。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"Moreover, several Panel Manufacturers have in-house design capabilities and therefore may not need to source semiconductor products from us. If our customers successfully develop in-house capabilities to design and develop semiconductors that can substitute for our products, they would likely reduce or stop purchasing our products.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"20-F 競爭章節：產業特徵為持續技術變遷、標準演進與平均售價下滑。","source":"SEC EDGAR 20-F FY2025 Item 4 Competition","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"The market characteristics for our products are, in general, intensely competitive, characterized by continuous technological change, evolving industry standards, and declining average selling prices.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"二手評論稱 Largan 成立 CPO 緊急產線、定位為 Himax 在光學元件上的替代者；FOCI 稱 Himax 目前是其 FAU 唯一供應商，長期不排除第二來源","source":"hntrbrk.com Himax: Stealth Supplier for Nvidia's Optics Revolution","url":"https://hntrbrk.com/?p=3901","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 20-F：Himax 主要透過台灣、中國、南韓的直銷團隊銷售，並對重要客戶設專屬業務團隊；特定產品或地區才透過代理商或經銷商。一手文件未載明通路結構性轉變；本軸搜尋亦未找到通路轉移或訂閱／平台化的來源。","source":"SEC EDGAR 20-F FY2025 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"We primarily sell our products through our direct sales teams located in Taiwan, China, South Korea. We also have dedicated sales teams for certain of our most important current or prospective customers.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"公司 2026-11-05 公布 Q4 指引：營收季減 22%～26%、毛利率持平至略升、EPS 每 ADS 4.5～6.5 美分（不含 7 月宣布之擬議資產出售可能利得）","source":"Himax Form 6-K Exhibit 99.1 (Q3 2026 results)","url":"https://www.sec.gov/Archives/edgar/data/0001342338/000117184326007146/exh_991.htm","excerpt":"Decrease 22% to 26% QoQ","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"StockAnalysis 引 S&P Global 3 位分析師：平均目標價 $30.2、低 $17.4、高 $43，共識 Buy；頁面更新 2026-11-06","source":"stockanalysis.com HIMX forecast","url":"https://stockanalysis.com/stocks/himx/forecast/","excerpt":"an average price target of $30.2","as_of":"2026-11-06","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 2026 營收 2.468 億美元、季增 8.5%，高於彙整站共識 2.387 億；CEO 指車用 Q4 預測因客戶短期急改單轉弱（共識 Q4 數字查無）","source":"Himax Form 6-K Exhibit 99.1 / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001342338/000117184326007146/exh_991.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"+","claim":"2026-07-01 公司公告擬出售約31%權益法被投資公司持股，總價約8,000萬美元現金，預期稅前利益約2,300–2,400萬美元，預計2026Q4交割（待主管機關核准）；為處分非併購","source":"ChinaTechNews: Himax Technologies Inc. announces proposed disposal of investment in equity method investee","url":"https://www.chinatechnews.com/2026/07/01/124732-himax-technologies-inc-announces-proposed-disposal-of-investment-in-equity-method-investee","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 20-F 載明公司目前非任何預期對業務、財務狀況或經營成果有重大不利影響之訴訟、調查或索賠之當事方","source":"SEC EDGAR 20-F FY2025 Item 8.A.7","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"However, as of the date of this annual report, we are not currently a party to, nor are we aware of, any legal proceeding, investigation or claim which, in the opinion of our management, is likely to have a material adverse effect on our business, financial condition or results of operations.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"TSMC 預計 2028 年前將 Fab14 12 吋成熟製程產能減少 15–20%（Counterpoint 估約 5 萬片/月），騰出空間給先進封裝；VIS 承接部分成熟製程","source":"rallies.ai: TSMC to Slash Fab14 Capacity by 15–20% and Deploy $52–56 B Capex Overseas","url":"https://rallies.ai/news/taiwan-semiconductor-cuts-15-20-of-fab14-mature-nodes-funds-52-56b-capex","excerpt":"TSMC to Slash Fab14 Capacity by 15–20% and Deploy $52–56 B Capex Overseas - TSM News | Rallies","as_of":"2026-01-25","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"Himax 管理層表示成熟製程晶圓代工、封裝、測試產能吃緊，限制平板 IC 出貨並推升成本","source":"Himax Q2 2026 Earnings Call Transcript (Webull)","url":"https://www.webull.com/news/15395663482414080","excerpt":"It has rippled across the broader semiconductor supply chain, resulting in capacity constraints at foundry, packaging and testing facilities on the mature process nodes where many of our products are manufactured.","as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"BNP Paribas：工業類半導體在長期庫存修正後進入廣泛回補週期；車用客戶庫存低但尚無信心回補；2026 市場成長主要來自價格而非數量","source":"BNP Paribas CIB — Semiconductor market 2026: it is not solely about AI","url":"https://cib.bnpparibas/semiconductor-market-2026-it-is-not-solely-about-ai/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Gartner 摘要：3Q26 半導體庫存水位季減 2.1%，與記憶體、AI 半導體、先進製程運算持續短缺有關","source":"Gartner Insights Abstract","url":"https://www.gartner.com/en/documents/8515377","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"DRAM 合約價 1Q26 季增約 90–95%、2Q 已鎖定約 +30%；TrendForce 稱 AI 擠壓成熟製程產能，8/12 吋晶圓代工價可能高檔到 2027（未找到現貨價序列，最新資料約 2026-06）","source":"iconnect007 / TrendForce — AI Server Demand to Drive Memory Contract Price Increases in 2Q26","url":"https://iconnect007.com/article/149414/ai-server-demand-to-drive-memory-contract-price-increases-in-2q26-as-csps-secure-supply-via-longterm-agreements/149411/ein","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Himax 2026-03-31 庫存 $151.7M（前季 $152.7M、去年同期 $122.9M）；管理層約一年前選擇性放寬庫存控管；Q1 車用驅動 IC 因客戶庫存控管（先前連兩季回補）而下滑；Q2 營收指引季增 10–13%","source":"Himax Q1 2026 Earnings Call Transcript (MarketBeat)","url":"https://www.marketbeat.com/earnings/reports/2026-5-7-himax-technologies-inc-stock/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.H","triggers"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Himax 2023 全年毛利率 27.9%，前一年 40.5%；2023 Q2 單季毛利率 21.7%（Q1 28.1%），Q4 回升至 30.3%（來源為搜尋摘要轉述，未讀原頁）","source":"Himax Q4 2023 earnings call / press release (alphaspread, SEC 6-K exh_991)","url":"https://alphaspread.com/security/nasdaq/himx/earnings-calls/q4-2023","excerpt":null,"as_of":"2024-02-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"SOX 2022 年自年初高點跌約 36%（盤中最深約 42–44%），高點約 2022 年 1 月初、谷底約 2022 年 10 月，約 9 個月","source":"247wallst, Chip Stocks Are Bleeding Today. The 2018 and 2022 Selloffs","url":"https://247wallst.com/investing/2026/05/12/chip-stocks-are-bleeding-today-the-2018-and-2022-selloffs-tell-you-exactly-what-comes-next/","excerpt":null,"as_of":"2026-05-12","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"TechInsights（Hutcheson）：1963 年來 14 次半導體下行，平均每 4.4 年一次；半導體平均衰退約 -8%、設備約 -20%；WSTS 資料平均週期 52 個月（37–82 個月）","source":"TechInsights, The Chip Insider – Cyclical History of the Semiconductor Industry; ECIA Semiconductor Cycle Outlook 2019","url":"https://www.techinsights.com/blog/chip-insiderr-cyclical-history-semiconductor-industry","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Himax 2023 Q2 毛利率 21.7%、全年 27.9% vs 40.5%","source":"SEC 6-K exhibit 99.1 Q4 2023","url":"https://www.sec.gov/Archives/edgar/data/1342338/000117184324000605/exh_991.htm","excerpt":"Gross margin in 2023 was 27.9%, decreasing from 40.5% in 2022. As a reminder, in Q2, the Company strategically terminated high-cost foundry capacity agreements, leading to a depressed Q2 gross margin of just 21.7%.","as_of":"2024-02-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"+","claim":"2026-07-01 公告出售約31%權益法被投資公司持股（約8,000萬美元現金），未見近12個月收購","source":"ChinaTechNews","url":"https://www.chinatechnews.com/2026/07/01/124732-himax-technologies-inc-announces-proposed-disposal-of-investment-in-equity-method-investee","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"經查20-F，公司無預期有重大不利影響之訴訟；搜尋僅見2007–2009已和解舊案","source":"SEC EDGAR 20-F FY2025 Item 8.A.7","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"we are not currently a party to, nor are we aware of, any legal proceeding, investigation or claim which, in the opinion of our management, is likely to have a material adverse effect on our business, financial condition or results of operations.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"經查20-F，公司不知有重大調查；近12個月8份6-K標題均為一般FORM 6-K，搜尋未見SEC調查或重編","source":"SEC EDGAR 20-F FY2025 Item 8.A.7","url":"https://www.sec.gov/Archives/edgar/data/1342338/000110465926035507/himx-20251231x20f.htm","excerpt":"we are not currently a party to, nor are we aware of, any legal proceeding, investigation or claim which, in the opinion of our management, is likely to have a material adverse effect on our business, financial condition or results of operations.","as_of":"2026-03-27","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"HIMX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.07,"operating_margin_pct":4.94,"fcf_margin_pct":3.25,"rd_intensity_pct":19.88},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HIMX","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"3034.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.1,"operating_margin_pct":19.03,"fcf_margin_pct":14.97,"rd_intensity_pct":17.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.3034.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"SIMO","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.54,"operating_margin_pct":21.3,"fcf_margin_pct":-24.9,"rd_intensity_pct":23.7},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIMO","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"AMBA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":58.52,"operating_margin_pct":-14.9,"fcf_margin_pct":2.33,"rd_intensity_pct":54.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMBA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"LSCC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.62,"operating_margin_pct":13.05,"fcf_margin_pct":24.71,"rd_intensity_pct":30.76},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LSCC","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"HIMX"},"financial_history":{"ticker":"HIMX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":1201339000.0,"revenue_yoy_pct":null,"gross_margin_pct":40.55,"operating_margin_pct":21.44,"net_income":236982000.0,"diluted_eps":1.356,"free_cash_flow":70780000.0,"fcf_margin_pct":5.89,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":945428000.0,"revenue_yoy_pct":-21.3,"gross_margin_pct":27.87,"operating_margin_pct":4.57,"net_income":50616000.0,"diluted_eps":0.29,"free_cash_flow":129348000.0,"fcf_margin_pct":13.68,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":906802000.0,"revenue_yoy_pct":-4.09,"gross_margin_pct":30.46,"operating_margin_pct":7.52,"net_income":79755000.0,"diluted_eps":0.456,"free_cash_flow":102769000.0,"fcf_margin_pct":11.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":832173000.0,"revenue_yoy_pct":-8.23,"gross_margin_pct":30.57,"operating_margin_pct":5.3,"net_income":43937000.0,"diluted_eps":0.504,"free_cash_flow":119505000.0,"fcf_margin_pct":14.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HIMX/HIMX_Q3_2026_Earnings_Call_20261105.md）

# Q3 2026 Earnings Call
**Himax Technologies, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Ladies and gentlemen, welcome to Himax Technologies, Incorporation Third Quarter 2026 Earnings Conference Call. 
[Operator Instructions] 
As a reminder, this conference call is being recorded. I would now like to turn the conference over to Ms. Karen Tiao, Head of IR/PR at Himax. Ms. Tiao, please go ahead.

**Karen Tiao** (Executives):
Welcome, everyone. My name is Karen Tiao, Head of IR at Himax. Joining me today are Jordan Wu, President and Chief Executive Officer; and Jessica Pan, Chief Financial Officer. After the company's prepared comments, we have allocated time for questions in the Q&A section.
If you have not yet received a copy of today's results release, please e-mail hx_ir@himax.com.tw or download a copy from Himax's website. Before we begin the formal remarks, I would like to remind everyone that some of the statements in this conference call, including statements regarding expected future financial results and industry growth, are forward-looking statements.
They involve a number of risks and uncertainties that could cause actual events or results to differ materially from those described in the conference call. A list of the risk factors can be found in the company's latest SEC filings, Form 20-F in the section entitled Risk Factors as may be amended.
Except for the company's full year of 2025 financials, which were provided in the company's 20-F and filed with the SEC on March 27, 2026, the financial information included in this conference call is unaudited and consolidated and prepared in accordance with the IFRS accounting. Such financial information is generated internally and has not been subjected to the same review and scrutiny and may vary materially from the audited consolidated financial information for the same period.
On today's call, I will first review Himax's consolidated financial performance for the third quarter of 2026, followed by our fourth quarter outlook. 
Jordan will then give an update on the status of our business, and after which, we will take questions. You can submit your questions online through the webcast or by phone. We will review our financials on an IFRS basis.
We are pleased to report that our Q3 profit exceeded the guidance range announced on August 6, while revenues and gross margin were both in line with the guidance. Third quarter revenue registered $246.8 million, representing a sequential increase of 8.5%. Gross margin was at 34.2%, in line with our guidance of around 34% and up from 33.1% in the previous quarter. Q3 profit per diluted ADS was $0.107, exceeding the guidance range of $0.08 to $0.10, attributable to lower-than-expected operating expenses.
Revenue from large display driver IC came in at $19.0 million, a slight decline of 1% from the previous quarter. Both monitor and notebook IC sales declined quarter-over-quarter as customers had already pulled forward inventory purchases in the prior quarters. In contrast, sales for TV IC products increased sequentially due to higher legacy product shipments to key customers. 
Sales of large panel driver IC accounted for 7.7% of total revenue for the quarter compared to 8.4% last quarter and 9.5% a year ago.
Revenue from small and medium-sized display driver IC segment totaled $176.8 million, reflecting an increase of 8.9% sequentially. Q3 automotive driver sales, including both the traditional DDIC and TDDI, increased by solid double-digit quarter-over-quarter, marking the second consecutive quarter of strong growth. This was primarily driven by the broad customer demand for DDIC and TDDI products.
Some panel makers also accelerated IC purchases in response to a surge in orders from Chinese automakers, which are expanding overseas amid slowing demand in their domestic market. The mass production of multiple LTDI projects across the automotive brands worldwide also contributed to the quarter-over-quarter growth.
Q3 smartphone IC sales covering LCD and OLED products increased sequentially, driven by continued shipment of a leading smartphone brand's mainstream model and inventory buildup for its new premium models. In contrast, tablet IC sales decreased sequentially as expected, primarily reflecting customers' accelerated purchases in the first half of the year against the backdrop of the rising memory price sentiment in the market.
The small and medium-sized driver IC segment accounted for 71.6% of total sales for the quarter compared to 71.4% in the previous quarter and 70.8% a year ago. Q3 non-driver sales reached $51.0 million, an 11.2% increase from the previous quarter, attributable to robust automotive Tcon shipment that extended the strong momentum from Q2.
This growth was supported by the continued legacy product shipment to a broad diversified customer base as well as the several new projects entering mass production. Tcon business accounted for over 10% of the total sales with more than half contributed by automotive Tcon. Himax continued to hold undisputed leadership position with a dominant market share in automotive Tcon, particularly in solutions featuring local dimming functionality.
We expect the strong growth momentum to continue into next year, and non-driver product accounted for 20.7% of total revenues as compared to 20.2% in the previous quarter and 19.7% a year ago. Third quarter operating expenses were $61.8 million, an increase of 21.9% from the previous quarter and 1.7% compared to the same period last year.
The sequential increase was mainly attributed to the annual bonus compensation, which we award employees at the end of September each year and result in a much higher employee compensation expense compared to other quarters of the year. Our annual bonus compensation grant for 2026 was $13.3 million, slightly higher than the guidance of $13 million as the bonus amount determined by the expected full year profit was revised upward following an improved Q3 profit.
Of the $13.3 million, $11.8 million was immediately vested and expensed in the Q3. Including a portion of the award granted in the prior year, the total bonus expenses for the Q3 2026 amounted to $11.9 million, higher than the $8.1 million recorded in the Q3 2025. 
For reference, the annual bonus granted for the 2025 and 2024 were $7.7 million and $12.5 million, respectively, of which $7.5 million and $11.2 million were vested and expensed immediately.
We continue to exercise prudent cost management while prioritizing strategically investment in non-driver IC business that offer attractive long-term growth opportunity. Third quarter operating income was $22.7 million, representing an operating margin of 9.2% compared to 10.8% in the previous quarter and negative 0.3% for the same period last year.
The sequential decline was primarily attributable to the higher employee bonus expense, which, as I mentioned earlier, totaled $11.9 million compared to $0.2 million last quarter. Meanwhile, the year-over-year increase was primarily driven by higher revenue and improved gross margin. Third quarter after-tax profit was $18.6 million or $0.107 per diluted ADS compared to $19.9 million or $0.114 per diluted ADS last quarter and up from $1.1 million or $0.006 in the same period last year.
Turning to our balance sheet. We had $285.3 million cash, cash equivalents and other financial assets as of September 30, 2026. This compares to $278.2 million at the same time last year and $298.7 million a quarter ago. The sequential decline in cash balance mainly reflected the $44 million dividend and $11.9 million employee bonus payout.
Q3 operating cash inflow was $23.9 million compared to an inflow of $17.5 million in Q2. The employee bonus paid out this year included $11.4 million for the immediately vested portion of this year's award and $0.5 million for vested awards granted over the past 3 years. Our quarter end inventory as of September 30, 2026, were $159.8 million, up from $151.5 million last quarter and higher than the $137.4 million in the same period last year.
Our inventory level remained healthy, particularly considering extended manufacturing lead time across the industry. Accounts receivable at the end of September was $228.4 million, up from $220.3 million last quarter and $200.7 million a year ago. DSO was 93 days at the quarter end, the same as last quarter and 87 days a year ago.
Third quarter capital expenditures, primarily on R&D-related equipment for our IC design business was $3.9 million versus $4.3 million last quarter and $6.3 million a year ago. As of September 30, 2026, Himax had 174.5 million ADS outstanding, little changed from last quarter. On a fully diluted basis, the total number of ADS outstanding for the third quarter was 174.4 million.
Regarding the proposed divestiture of our stake in an equity method investee announced in July, the transaction is progressing as planned and expected to close in Q4, subject to customary closing conditions and regulatory approvals. Upon closing, we expect to recognize a pretax gain of approximately $23 million to $24 million and an after-tax gain of approximately $19 million to $20 million. We will provide further update as appropriate.
Now turning to our Q4 2026 guidance. We expect Q4 revenue to decrease 22% to 26% sequentially. Gross margin is expected to be flat to slightly up depending on the product mix. 
Q4 profit attributable to shareholders is estimated to be in the range of $0.045 to $0.065 per fully diluted ADS. This estimate does not yet include the potential gain from the proposed divestiture just mentioned earlier. I will now turn the call over to Jordan to discuss our Q4 outlook. Jordan, the floor is yours.

**Jordan Wu** (Executives):
Thank you, Karen. Demand for data center AI applications remains robust with no signs of slowing. Notably, AI-related demand extends beyond advanced process nodes to a wide range of supporting applications involving legacy process nodes such as Photonic ICs or PICs, interposers, power management ICs and MOSFETs.
As the supply-demand imbalance continues to intensify, capacity at legacy process nodes is expected to tighten further in 2027. Against this backdrop, foundries as well as packaging and testing providers, including those in China, have recently announced significant price increases for 2027. In the face of these mounting supply chain pressures, securing sufficient capacity has become our top priority, particularly as automotive now accounts for most of our revenues.
Automotive customers have far more stringent requirements for supply stability, long-term capacity assurance and delivery reliability than consumer electronics customers do. Through a series of recent proactive measures, we have fully secured capacity commitments for 2027 from our key suppliers and for key product areas. In terms of costs, we continue to work closely with customers to share the impact of rising costs.
As just mentioned, our Q4 revenue is projected to decline sequentially. This is primarily due to an abrupt and significant correction in automotive driver IC orders covering both TDDI and DDIC. Automotive Tcon sales, on the other hand, are expected to continue growing sequentially. It is worth highlighting that our automotive IC sales recorded a decent 16% year-over-year increase in the first 9 months of 2026.
Despite the sharp correction in Q4, we still expect full year automotive IC revenue to grow by approximately 10% year-over-year, outperforming the global automotive market with worldwide vehicle production expected to decline this year. Now let me elaborate on what we are seeing in automotive demand lately. The year started on a soft note in Q1, followed by robust inventory replenishment in Q2 and Q3 as certain panel makers accelerated IC purchases to meet surging orders from Chinese automakers expanding overseas.
In Q4, however, shortly after China's National Day holidays in early October, we saw a sudden and sizable decline in demand among the customers that had purchased aggressively in prior quarters. In recent weeks, certain panel makers with high exposure to Chinese automakers' export programs have significantly scaled back their Q4 forecast.
For context, after years of solid growth, China's domestic automotive market has experienced a substantial decrease in demand amid intensifying competition this year, prompting Chinese automakers to increasingly rely on exports. According to data released by the China Association of Automobile Manufacturers, or CAAM, in October, China's domestic sales for locally made vehicles declined by 22.4% year-over-year in the first 9 months of 2026, while exports of locally manufactured vehicles surged by 65.8% in the same period.
We believe the recent significant reduction in our Q4 forecast reflects in part Chinese automakers' earlier overly aggressive export expectations along with their growing concerns over inventory levels across distribution channels, including shipments in transit, following 3 quarters of extraordinary export growth. Adding to the uncertainty, there is mounting pressure from various countries, including the European Union, to tighten trade barriers on Chinese vehicle imports.
Compounding these headwinds in October, the Chinese government announced reductions in export tax rebates for new energy vehicles. Together, these factors may have contributed to the recent reduction in our Q4 automotive sales outlook and are limiting our near-term order visibility. By contrast, panel makers primarily serving non-China customers have maintained steady forecast with some posting slight sequential increases in their fourth quarter orders.
We believe the sharp decline in the fourth quarter automotive forecast reflects abrupt short-term order adjustments by certain customers, while our market leader position remains firmly intact. Himax has long maintained a dominant position with strong long-standing relationships with not just the panel makers, but also carmaker brands worldwide as well as leading Tier 1 suppliers across the U.S., Europe, Japan and Korea.
More recently, fueled by the rapid expansion of Chinese automakers in both domestic and export markets, we have also witnessed the rise of Chinese Tier 1 players, which are quickly emerging as a force to be reckoned with. In the process, these suppliers have significantly expanded their manufacturing capabilities, gained extensive mass production experience, strengthened their cost competitiveness and achieved rapid product development capabilities.
These Chinese Tier 1 players are located across a broad geographic area in China, enabling them to serve automakers across multiple regions effectively. 
With our deep automotive experience, comprehensive automotive display IC portfolio spanning both LCD and OLED technologies, best-in-class customer service and an extensive global network providing timely localized technical support, we have attracted a great number of Chinese automotive Tier 1s to our customer base in recent years.
Moreover, their eagerness to embrace new technologies and ability to bring them rapidly into mass production create additional opportunities for us to expand adoption of our advanced automotive display IC solutions across a growing number of vehicle programs. This has already translated into a substantial number of design wins and a rapidly growing pipeline of new projects.
Looking ahead, we remain optimistic about the long-term growth prospects of our automotive display IC business, supported by rapid advancements in smart vehicle interiors, a trend characterized by more displays per vehicle, larger and higher resolution screens and increasingly complex display configurations. These trends are driving growing demand for advanced display technologies as exemplified by our fast-growing LTDI solutions for large-format automotive displays, which continue to gain traction and demonstrate resilience amid broader automotive market fluctuations.
Meanwhile, the accelerating adoption of automotive OLED displays represents another significant long-term growth opportunity, supported by our comprehensive IC portfolio and numerous design wins secured through years of close collaboration with leading OLED panel makers in Korea and China. In addition to conventional in-cabin displays, head-up displays, or HUDs, are also gaining traction, evolving into an increasingly important application for new generation smart vehicles as automakers seek to bring advanced driver assistance information, AI-powered interactive features and real-time driving data directly into the driver's field of view.
This creates additional opportunities for our HUD IC solutions, where we hold a commanding market position. As these trends continue to unfold, we see significant opportunities to further increase our IC content value both per panel and per vehicle. EPD, or Electronic Paper Display, is another area where we see meaningful growth opportunities heading into 2027.
In e-Readers, we expect growing sales through newly secured project wins and a larger share of a leading global end brand's products. In addition, we continue to expand our presence in the electronic shelf label, or ESL, market, a sizable and growing market with significant potential. We are expanding our sales coverage to address diverse customer requirements and broaden our market reach.
Meanwhile, our WiseEye technology continues to gain traction across a growing range of applications, particularly in the rapidly expanding smart wearables market. During the quarter, we were pleased to announce that Alibaba adopted our WiseEye AI processor for its latest Qwen Glasses. Just 1 quarter after another leading global technology heavyweight announced their latest smart glasses incorporating our WiseEye. The retail sales of these glasses are already or soon to be in place.
These recent developments further validate WiseEye's technological strength in ultra-low power consumption, always-on visual sensing and on-device AI processing. In addition to smart glasses, we are making progress in other emerging wearable applications, including smart pendants and earbuds. Numerous smart wearable projects are underway, several involving global tech names.
This growing design-in momentum underscores WiseEye's strong fit for next-generation smart wearables, which are evolving towards proactive context-aware AI experiences that require continuous on-device AI without compromising battery life. I will elaborate further on this in a few minutes. Lastly, turning to our CPO business. We continue to work closely with our strategic partner, FOCI, focusing on further improving manufacturing yields and establishing stable mass production capabilities to support the next phase of production scaling.
We are pleased that as part of these ongoing efforts, FOCI announced earlier today that its Board of Directors approved capital expenditures in the amount of NT$3.33 billion or approximately USD 100 million for the expansion of both fab space and manufacturing equipment in preparation for FAU mass production. Engineering ramps are already underway with shipments expected to expand quarter-by-quarter from this point onward.
While the timing of mass production is ultimately a call to be made by our end customers, we remain confident that our CPO business will begin making a meaningful contribution to both our top and bottom lines starting in 2027. At the same time, we continue to engage with a growing number of customers and advance the joint development of next-generation optical solutions featuring higher fiber count, enhanced optical precision and increasingly sophisticated designs, including WDM or Wavelength Division Multiplexing, targeting the surging bandwidth demand of HPC and AI data centers.
Himax is uniquely positioned to drive further advancements in FAU technology and performance, leveraging the fundamental strengths of our proprietary WLO technology. Unlike other optical technologies available in the market, our WLO technology offers distinct competitive advantages in nanometer level optical precision, optical performance, manufacturing consistency and scalability.
These capabilities make it particularly well suited for the evolving requirements of future generation CPO applications, enabling reliable, highly repeatable and scalable mass production of high-precision optical components. Beyond CPO, Himax has been at the forefront of high-precision optics technology for nearly 2 decades, having worked on various designs across a wide range of applications with some of the world's most prominent technology names.
We are pleased to share that a leading global technology company has selected Himax's WLO technology to enable its advanced optical sensing solution to support autonomous driving. Our technology delivers high optical efficiency, precision, cost competitiveness and a solid volume production track record. These advantages, together with our proven manufacturing expertise, enable us to meet the stringent performance and reliability requirements of automotive applications.
Shipments are expected to commence in upcoming quarters. This adoption by a leading global technology company not only validates our technical strengths, but also demonstrates the versatility of our WLO technology, further expanding its applications beyond consumer electronics, wearable devices and AI data centers to include automotive. With that, I will now begin with an update on the large panel driver IC business.
In Q4, large display driver IC sales are expected to increase by low teens from last quarter. Both TV and monitor sales are poised for sequential increases driven by higher shipments of legacy products to key customers. This growth, however, is expected to be partially offset by a decline in notebook IC sales as a leading customer has pushed back mass production of a new high-end notebook model to early 2027.
Looking ahead in the notebook market, we are seeing increasing adoption of OLED displays in premium notebooks, supported by notebook makers' growing focus on higher-end models amid rising memory prices and the ramp-up of new Gen 8.6 OLED fabs in China starting later this year and into 2027. Himax is well positioned to capitalize on these favorable industry trends with our comprehensive portfolio of notebook OLED display ICs spanning DDICs, Tcon, power management ICs and touch controllers.
We have also completed development of our Tcon solution supporting the eDP 1.5 interface applicable to both LCD and OLED panels. This interface supports high refresh rates, low-power panel replay, adaptive-sync and high-resolution displays, enabling enhanced visual performance and improved power efficiency. Our comprehensive product portfolio allows us to offer customers a one-stop solution while increasing our content value per device.
Turning to the small and medium-sized display driver IC business. In Q4, our small and medium-sized display driver IC business is expected to decrease by double digits sequentially, following 2 consecutive quarters of robust growth. Automotive, tablet and smartphone driver IC sales are set to decrease quarter-over-quarter in Q4. As noted earlier, the anticipated decline in automotive sales reflects order reductions from certain panel makers following 2 quarters of strong sales.
These panel maker customers have been aggressively scaling back their Q4 projections in recent weeks as the outlook for Chinese automakers' export growth began to reverse significantly. Despite the recent slowdown, we expect our full year 2026 automotive display IC revenue to grow by approximately 10% year-over-year, outperforming the projected decline in global vehicle shipments. This growth is driven by the continued expansion of our automotive TDDI, wider adoption of our Tcon solutions and growing contributions from LTDI.
Looking ahead, we remain confident in the long-term trajectory of our automotive IC business with multiple growth drivers in place, starting with the rebound in automotive DDIC. Following several years of modest decline driven by gradual displacement by TDDI, DDIC is poised for a recovery backed by the anticipated volume growth of relatively new non-touch display applications such as HUD and e-mirror, where we have built a strong pipeline of design win projects accumulated over the last few years as well as mainstream displays such as dashboards and in-vehicle infotainment systems.
Our automotive TDDI business, meanwhile, should keep expanding on the back of additional customer vehicle model ramps and broader adoption across automotive display applications. To round out the picture, LTDI and OLED solutions are also set to contribute more meaningfully from 2027 onwards as more project ramps following years of design developments with customers. Himax continues to introduce innovative technologies that reinforce our market leadership and expand our opportunities across diverse automotive display applications.
Our LTDI technology is a prime example, particularly suited for large-format displays exceeding 30 inches, which typically require 4 or more chips per panel and in some cases, more than 10 as well as at least 1 local dimming Tcon. This translates into significantly higher IC content value on a per panel and per vehicle basis. Reflecting the widening adoption of this emerging display technology, Q4 LTDI revenue is expected to grow by single digits quarter-over-quarter and account for over 5% of total sales during the quarter.
Integrating a high-speed eDP interface, touch controller and display driver into a single chip, our recently introduced industry-leading automotive eDP TDDI solution is another example. Supporting displays of up to 30 inches, this highly integrated solution delivers high resolution, superior display quality and responsive touch performance.
Customers can also opt for an IC configuration that further integrates our industry-leading local dimming technology, eliminating the need for a separate Tcon while enhancing contrast and image detail in both bright and dark areas as well as reducing overall system costs and display power consumption. Together, these technologies broaden our automotive display portfolio, giving customers greater flexibility to select solutions that best meet their specific display needs, performance requirements and cost targets.
Building on our leadership in automotive LCD, we are also well positioned to capture the accelerating shift to OLED in premium automotive displays, which we expect to become another key growth driver. Working closely with leading OLED panel makers in Korea and China, we have developed a comprehensive portfolio of DDICs, Tcons, touch controller ICs and customized ASIC solutions to address diverse customer needs and display requirements. Our extensive offerings and early customer engagements have led to a strong pipeline of design wins.
We are also expanding our OLED portfolio with innovative, highly integrated solutions such as our TED, or Tcon Embedded Driver IC, technology, which combines DDIC and Tcon into a single chip to deliver a cost-effective and flexible solution, particularly suited for smaller lower-resolution automotive displays. Our TED technology continues to gain traction across a diverse range of applications, including automotive, robotics and IT.
Shortly after its introduction, the TED solution achieved its first mass production milestone with a leading global brand in the robotics market with production commencing in Q4. Several additional design win projects are also underway with customers for their upcoming vehicle models. I would like to now turn to our non-driver IC business update, where we expect Q4 revenue to be flat to slightly down sequentially. First, for an update on our Tcon business.
We anticipate Q4 Tcon sales to increase by high single digit quarter-over-quarter. Our automotive Tcon business is expected to deliver low teens growth in Q4, marking the third consecutive quarter of strong quarter-over-quarter growth despite subdued demand in the broader automotive market. The sequential growth is supported by continued shipments of our legacy products to a broad and diversified customer base, along with the ramp-up of several new projects.
Notably, one is for a U.S. Big Tech for its robotaxi offering, underscoring the broadening application of our automotive Tcon solutions beyond conventional passenger vehicles. Our full year 2026 automotive Tcon sales are on track to grow by over 40% with another strong growth expected next year. With automotive Tcon adoption still largely concentrated in premium vehicles, we see significant room for broader market penetration.
At the same time, we hold a leading market position in the growing adoption of advanced HUDs, where our automotive Tcon solutions are widely adopted to address complex issues of de-warping and post card effect elimination, which are unique to HUDs. Together, these trends position us well to deliver another year of strong automotive Tcon growth in 2027 and beyond.
During the quarter, we also introduced our groundbreaking multi-output Tcon solution designed to support next-generation free-form ultra-wide and high-resolution automotive displays, featuring a high-speed eDP input and up to 8 LVDS outputs. The solution supports resolutions of up to 12K and incorporates advanced image enhancement capabilities, including local dimming and HDR, or High Dynamic Range.
It also integrates built-in automotive safety features such as failure detection and on-screen display, or OSD, for safety alerts and fault notifications. The solution simplifies system architecture, enhances design flexibility and reduces overall costs, making it a compelling choice for next-generation automotive display applications ranging from HUDs to pillar-to-pillar displays. Its strong market appeal is already reflected in the design momentum with leading panel makers and Tier 1 players globally.
This new solution demonstrates our continued execution of our technology roadmap and reinforces our leadership in advanced automotive display solutions. Switching gears to the WiseEye product line, a cutting-edge ultra-low power AI sensing total solution targeting battery-powered endpoint devices. WiseEye has demonstrated its versatility through growing adoption across diverse applications, including notebooks, smart door locks, surveillance systems, access control, Palm Vein authentication, smart offices and more recently, smart glasses with design activities continuing to expand.
At the core of WiseEye's competitive advantage is its industry-leading ultra-low power architecture, consuming only a few milliwatts while enabling on-device AI inference, 24/7 always-on visual and voice sensing all in an exceptionally compact form factor. These capabilities enable customers to incorporate AI sensing into their products while minimizing power consumption, extending battery life and reducing reliance on host processors, creating further opportunities across emerging edge AI and endpoint AI markets.
As mentioned earlier, during the quarter, we announced another significant milestone in the smart glasses market with Alibaba adopting our WiseEye AI processor for its Qwen Glasses. The Qwen Glasses feature a 3-chip architecture with dedicated processors handling image processing, everyday tasks and ultra-low power visual sensing. Himax's WiseEye AI processor featuring the compact form factor and integrated into the temple of the glasses near the ear serves as the always-on ultra-low power AI vision engine.
It enables continuous outward-facing environmental sensing and real-time understanding of the surroundings while consuming only a few milliwatts of power. This division of processing tasks allows the glasses to handle functions such as photography and audio processing while maintaining continuous environmental awareness without keeping the main processor constantly active, helping reduce overall system power consumption and extend battery life.
Beyond outward-facing environmental sensing for AI glasses, WiseEye also supports inward-facing eye tracking, enabling intuitive gaze-based interaction. In addition, it supports iris recognition for secure user authentication. Together, these capabilities lay the foundation for new generation physical AI agent applications, enabling devices to proactively understand their surroundings, anticipate user needs and provide timely context-aware assistance rather than simply responding to user commands.
In the smart glasses market, we continue to expand our WiseEye engagements with platform providers, ODMs and consumer electronics names worldwide with numerous projects poised to enter mass production starting in 2027. On the WiseEye module front, design activities continue to expand, supported by its plug-and-play offering, ultra-low power consumption and on-device AI capabilities.
A recent example is the adoption of our Palm Vein recognition module by WAFERLOCK, a Taiwan-based smart door lock brand powered by WiseEye. The door lock features fast, secure and contactless Palm Vein authentication with biometric processing performed on device to safeguard sensitive biometric data and enhance user privacy. Several additional Palm Vein module projects are underway with customers, including certain global leaders in door lock, access control and security, reflecting growing demand for biometric authentications across residential, commercial and smart building applications.
Finally, we continue to see growing design activities for our WiseEye AI solution with applications extending to capsule endoscopy, spanning both human and veterinary health care. Leveraging WiseEye's ultra-low power AI capabilities, our solution enables compact swallowable capsule endoscopes to continuously capture and transmit images while consuming negligible power.
This approach offers a less invasive and more convenient examination experience compared with conventional endoscopy, which typically requires the insertion of an endoscope tube. We are pleased to share that one of our capsule endoscopy projects for human health examinations is slated to enter mass production this quarter, following an extensive and lengthy review and approval process by China's National Medical Products Administration, under its Class III medical device classification.
This marks an important milestone for WiseEye in health care and further demonstrates its versatility across industries. That concludes my report for this quarter. Thank you for your interest in Himax. We appreciate you joining today's call and are now ready to take questions.

**Operator** (Operator):
[Operator Instructions]

**Jordan Wu** (Executives):
We do receive online quite a few questions, mainly regarding our overall market projection, particularly in relation to automotive market and also CPO. I think I will start with this combination of a few questions. Is the auto big down continue to next year? Is there anything to do with China market share decline impact GM next year? Okay. I think this is a combination of a few questions.
Well, thank you, guys, for the question. As you know, we don't usually provide guidance beyond 1 quarter. So I'm not going to give specific financial projections for next year. However, based on our current internal assessment, we are actually quite confident about our growth prospect for next year, which is now looking to enjoy double-digit growth.
Starting with revenue, we believe the sudden and substantial correction of revenues for Q4 this year is a temporary short-term setback, reflecting our customers' overly aggressive inventory buildup in the previous 2 quarters. I guess, in light of the extraordinary growth of the export markets for Chinese carmakers.
What we have seen over the last 3 or 4 weeks or so right after the Chinese National Day holidays right after some of our major customers perhaps sensing early signals for the market conditions to take a turn for the worst. They decided to hit the brake hard, very hard. And actually, that kind of surprised us as well.
But as I pointed out earlier in the prepared remarks, our full year automotive sales forecast for this year still stands at around 10% growth. 
This has accounted for the Q4 pretty drastic correction in sales numbers already. So this 10% sales growth is still achieved notwithstanding the sharp decline of the fourth quarter, outperforming the overall automotive shipment, which is projected for decline this year.
So we believe, again, we are well positioned to achieve double-digit year-over-year growth -- revenue growth in 2027, driven primarily by automotive business with growth across DDIC, TDDI, LTDI and Tcon. I'm not going to go through the details again because we have covered a lot of those in our prepared remarks.
What I want to say is that our positive outlook is not built on the growth of the global car shipment next year. It's not built on the growth of global car shipments next year. Rather, we are building our projection based on a flattish global automotive shipment next year. So our positive sales projection is supported by a strong pipeline of design wins accumulated over the past few years with customers' new project mass production timetable already set for the coming quarters.
So contrary to total vehicle shipment, which can swing one way or the other based on various economic and political factors, and it's actually harder to predict. The gradual increase of number of displays per vehicle and the IC dollar content inside each display are, however, quite certain. Again, we have demonstrated this year, we are still able to grow 10% year-over-year despite the global car shipments -- decline of global car shipments.
So this is also evidenced by the aggressive adoption of our DDIC display solutions for automotive by Tier 1s and OEMs globally. So that is the first area, the main area, global automotive display driver IC, which is now almost half of our total sales. And the next area to cover is EPD or electronic paper display business, including DDIC and Tcon for e-readers and e-tag.
And this is another area of display ICs where growth prospects for next year looks quite positive, supported by recent mass production of a major e-reader brand's, mainstream products where our ICs are adopted and the broader coverage of customer base for the e-tag business. So I guess that's my short-term summary for a quick summary for DDIC sales outlook for next year.
Now turning to non-driver businesses, which are expected to outgrow driver ICs in next year with revenue contribution approaching 30% next year, up from 20% of today. So non-driver IC will outgrow driver IC next year. And the non-driver IC growth will be driven primarily by automotive Tcons, which are expected to deliver another year of very strong growth following this year's projected growth of 40%, supported by our robust design pipeline.
Our WiseEye product line is set to be another key growth driver with very strong momentum across emerging applications, including smart glasses, WiseEye modules and Palm Vein authentication. I've highlighted all those in my prepared remarks. In smart glasses, in addition to the Alibaba Qwen Glasses and another global technology titan's, AI glasses, we are quite confident that more product launches from various customers incorporating our WiseEye are actually on the way, and they will be announced along the way in the next few quarters.
All these developments, together with growing opportunities in WiseEye modules and Palm Vein authentication position us well for continued growth in 2027. I want to highlight though the revenue outlook I just mentioned, meaning double-digit growth expected for next year. This does not include CPO, which is expected to start MP from 2027. And this will certainly add to our 2027 revenue as well.
But because CPO is a new business, we still don't have a good grasp of how the business ramp-up will look like in its first year of mass production. So it's -- I think it's prudent that we don't include it as part of our next year sales discussion for the time being. And certainly, hopefully, we'll be able to give you concrete updates as we move along in the next few quarters. So that's -- again, that's a quick summary of next year's top line projection.
People asked about gross margin. We do see some challenges ahead on gross margin because, as I pointed out earlier, foundries and back-end suppliers, including those in China, have announced significant price increases starting from the very beginning of next year. 
This is an industry-wide issue, and we are working closely with our suppliers and customers to manage the impact.
I mentioned earlier that sales contribution from non-driver IC product line will be higher next year, approaching 30% from the current 20%. This will be accretive for gross margin because all major non-driver IC products such as I highlighted earlier, Tcon and WiseEye offer better gross margin than driver ICs. I said earlier, our current outlook does not factor in potential contribution from CPO, which does offer much better gross margin than our corporate average, and it will certainly help enhance our gross margin rather meaningfully once ramping gets started.
But again, even excluding CPO, we still expect gross margin to remain relatively stable compared to this year or hopefully improve slightly next year despite the challenging condition on the supply side. Okay. I hope that kind of covers all these questions. Let me see if I miss anything. Our market share decline, no, well, again, I pointed out earlier, right? We actually outgrow the global car shipment data.
So I think that's a strong evidence that we are not losing market share. Rather, it is a very sudden short-term customer order correction. Anything to do with China, I've said it quite clearly, both in my response to questions in prepared remarks that the Chinese export over the first 3 quarters of this year grew almost 70% year-over-year. And this is very new and so strong.
So I think -- and logistics for export is a lot more complicated than domestic sales. So I think some of our customers with a big exposure to Chinese car exports are still getting used to this new market. And in light of the very strong growth, they probably overbuilt and they sensed something early signals that they decided to stand on the brake. So yes, it does have a lot to do with China, in particular, Chinese car exports, okay?
There's quite a few questions. Again, I try to combine them together. They are all about CPO. Many new players entering CPO, your market share got eroded? Your position is still solid. How you compare with them, meaning the newcomers exclusively with FOCI for now? 
And are we facing pressure in light of the new competition? Okay. So that's the question about CPO.
So CPO or more specifically FAU, right, FAU targeting the CPO application, okay? That's our market specifically, right, FAU targeted CPO application. It's a greenfield market for everyone. And that is a market which is super exciting, technically very, very challenging and with enormous potential, right? So it is no surprise that more players are entering the race and different players approaching the market with different competing technology.
So that is, I mean, kind of expected, right? And we did expect that all along. So first off, as far as we know, we are probably the only company offering optical solutions for FAU based on WLO technology, wafer-level optics technology with products already in pretty advanced stage of engineering validation by some of the largest and leading end customers, okay? So that kind of sets us apart from the so-called new competition.
We are in very advanced stage and we use WLO. 
Before I continue, I'd like to point out that there are various optical and mechanical components inside an FAU, right? And since day 1, Himax has focused our efforts on only a select number of optical components, which are of the highest technical challenge, right? And that is why we chose them because we feel we are, will be of the best value if we succeed.
We don't -- what I want to say is we don't cover all optical components, every single piece of optical component inside FAU. And we certainly don't intend to enter the field of mechanical components inside FAU, right? We don't do mechanical components. And we noticed certain press reports have mistakenly compared other companies' solutions with those of ours while we are actually working on different things.
So that is one clarification what I wish to make, taking the advantage of the Q&A session. Having said that though, there are some other competition -- competitors who are, in fact, competing head-on with us on the optical components that we chose to develop. While I won't comment on competing players or the technologies, we are very confident. 
We are very, very confident in the competitive advantage of our unique WLO approach.
We have developed our solution from the ground up with extensive feedback from our customers and partners along the way over the last 4 or 5 years, during which time we have actually accumulated extensive know-how and experience, and we have filed numerous, in some cases, very critical patents, which is an advantage only unique to pioneers such as us and FOCI. I can say -- what I can say is the latest feedback we have received from customers has been both encouraging and very promising.
Although we are -- again, we are -- we haven't really officially entered mass production stage. We are in hopefully, last stages of engineering validation. Our technology offers distinct advantages. Our WLO technology or WLO technology offers very unique advantages in nanometer level optical precision optical precision, down to nanometer level. We offer outstanding optical performance and manufacturing consistency.
Compared with conventional optical approaches, our WLO technology is particularly well suited for highly repeatable and reliable big volume production. Once the manufacturing process is established, we can repeatedly produce high-precision optical structures or components with consistent quality and stable yields. I want to emphasize this because -- this is one thing to be able to produce samples with good quality or good precision.
But the real challenge is maintaining that same level of quality consistently while shipping at scale. So right now, our worry is not really exactly on competition. Our focus is on execution, establishing reliable mass production capabilities, positioning ourselves among the early suppliers to serve leading customers. So again, engineering sample, engineering ramps are already underway, and we expect shipments to gain strong momentum over the coming quarters with driving revenue contribution quarter-by-quarter in the next foreseeable quarters.
And that is something we have confidence about. And lastly, in my prepared remarks, I mentioned that FOCI coincidentally announced earlier today that its Board of Directors approved capital expenditure in the amount of about $100 million for the expansion of fab space and manufacturing equipment. So I believe that is an illustration of our strategic partners' strong confidence in bringing the technology to volume production soon.
So in summary, we are -- we remain very confident our CPO business will begin making a meaningful contribution to both our revenue and profitability starting from some point next year. Whether our market share or market position will be eroded, I believe we are still clearly the market leader. I think it's way too early to talk about anybody's market share. And if anything, I think the market is so big that -- well, first off, I don't believe anybody going forward in the long term will enjoy a monopoly in this huge market, right?
It's impossible. So it's reasonable that there will be competition. So I think we are still ahead in the race. And market share erosion, I think it's really too early to tell because nobody has really a market share to speak of to begin with. But again, is our position still solid? Yes, still very solid because, as I said, we are in the most advanced stage of validation, and we are getting very, very close. And FOCI just announced a major capital expansion, right?
So I think all these are strong evidence of our position. Are we still exclusively for FOCI for now? Yes, we still are, although we've been approached by others. But for the time being, I think it is to the best of our interest, our shareholders' interest that we focus on FOCI and bring it up for mass production, get it really nailed down because having 1 partner is already quite exhaustive engineering resource wise.
So I think it is a good idea that we focus on our strategic partner and nail it down, start mass production before we think of anything else. I think that's my summary of my response to all these different questions.

**Karen Tiao** (Executives):
Operator, if there are any other questions?

**Operator** (Operator):
Yes. We don't have further questions at the moment. We thank you for all your questions, and I'll pass the call back to Mr. Jordan Wu for closing comments.

**Jordan Wu** (Executives):
As a final note, Karen, our Head of IR/PR, will maintain investor marketing activities and continue to attend investor conferences. And we'll announce the details as they come about. Thank you, and have a nice day.

**Operator** (Operator):
Ladies and gentlemen, this concludes the third quarter 2026 earnings conference. You may now disconnect. Thank you again. Goodbye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HIMX_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Karen Tiao｜guidance：Q3 營收季增 7% 至 11% 的財測（原話："We expect Q3 revenue to increase 7% to 11%"）
- 2026-08-06｜Karen Tiao｜guidance：Q3 毛利率財測約 34%，視產品組合而定（原話："Gross margin is expected to be around 34%, depending on the"）
- 2026-08-06｜Karen Tiao｜guidance：Q3 每稀釋 ADS 獲利財測 0.08 至 0.10 美元（原話："attributable to shareholders is estimated to be in the"）
- 2026-08-06｜Karen Tiao｜margin：Q3 員工獎金費用估 1,180 萬美元、每 ADS 稅前 0.068 美元，已含在 EPS 財測內；前三季每季約 20 萬（原話："be $11.8 million, representing $0.068 per diluted ADS"）
- 2026-08-06｜Karen Tiao｜margin：Q2 毛利率 33.1%，高於財測約 32%（原話："Gross margin was 33.1%,"）
- 2026-08-06｜Karen Tiao｜margin：Q2 營業利益率 10.8%（前季 5.1%），管理層歸因於營收與毛利率提高（原話："representing an operating margin of 10.8%"）
- 2026-08-06｜Jordan Wu｜margin：管理層與客戶協商調價以分攤成本，部分已在 Q2 生效（原話："Some adjustments took effect in the second quarter"）
- 2026-08-06｜Jordan Wu｜margin：2027 毛利率方向：管理層相信今年改善的趨勢明年可能延續（非正式財測）（原話："and we believe the trend is likely to continue next year."）
- 2026-08-06｜Jordan Wu｜risk：成熟製程晶圓代工、封測產能吃緊，成本上升（原話："we are experiencing higher manufacturing and procurement"）
- 2026-08-06｜Jordan Wu｜risk：管理層預期供應環境近期仍具挑戰（原話："We expect the supply environment to remain challenging in"）
- 2026-08-06｜Jordan Wu｜risk：明年晶圓廠仍將漲價，管理層稱需持續管理（原話："indicating further price hikes next year, certainly all"）
- 2026-08-06｜Karen Tiao｜risk：Q2 營運現金流含台灣新政策遞延約 1,100 萬美元稅款一年；不含遞延約 650 萬美元（原話："defer approximately $11.0 million of this payment for 1 year"）
- 2026-08-06｜Karen Tiao｜capital_allocation：Q3 現金將因 7/10 支付 4,400 萬美元年度股利而下降（原話："the payment of the $44 million for the annual dividend to"）
- 2026-08-06｜Karen Tiao｜capital_allocation：擬處分一家權益法被投資公司，預計稅前利得約 2,300 萬至 2,400 萬美元，預計 Q4 完成，尚待法規核准（原話："recognize a pretax gain of approximately $23 million to $24"）
- 2026-08-06｜Karen Tiao｜capital_allocation：約一年前調整庫存策略，選擇性備貨；庫存 1.515 億美元，與前季持平（原話："selectively building inventory in anticipation of the"）
- 2026-08-06｜Jordan Wu｜guidance：Q3 大尺寸驅動 IC 預期季減個位數（原話："driver IC sales are expected to decline by single digit"）
- 2026-08-06｜Jordan Wu｜guidance：Q3 中小尺寸驅動 IC 預期季增高個位數（原話："display IC business is expected to increase by high single"）
- 2026-08-06｜Jordan Wu｜guidance：2026 全年車用驅動 IC 預期雙位數成長（原話："We expect our full year 2026 automotive IC sales"）
- 2026-08-06｜Jordan Wu｜guidance：管理層表示不提供超過一季的正式財測，但對明年營收成長有信心（原話："robust sales growth for next year with continuously"）
- 2026-08-06｜Jordan Wu｜guidance：2027 展望明確排除 CPO 貢獻（原話："So what I'm about to say below does not include"）
- 2026-08-06｜Jordan Wu｜guidance：2027 非驅動 IC 占營收預期由約 20% 升至接近 30%（不含 CPO）（原話："revenue contribution approaching 30% from around 20% at"）
- 2026-08-06｜Jordan Wu｜guidance：2027 車用展望的前提假設：全球車輛出貨持平（原話："we are assuming a flattish year for global vehicle shipment"）
- 2026-08-06｜Karen Tiao｜margin：數字口徑：車用事業（DDIC、TDDI、Tcon、OLED IC）占 Q2 營收超過 50%（原話："representing well over 50% of total"）
- 2026-08-06｜Jordan Wu｜commitment：CPO 2027 出貨預期顯著高於 2026（原話："we expect our shipments in 2027 to be significantly higher"）
- 2026-08-06｜Jordan Wu｜commitment：CPO 2026 下半年主要目標為量產準備與客戶認證，Gen 1、Gen 2 於 Q3 開始工程量產爬坡（原話："have begun engineering production ramps as scheduled in the"）
- 2026-08-06｜Jordan Wu｜commitment：CPO 2027 成長基期低；即使最保守情境仍有實質貢獻，貢獻幅度取決於客戶量產時程（原話："significant growth next year, but we'll be comparing with"）
- 2026-08-06｜Jordan Wu｜commitment：CPO 最保守情境下 2027 起對財務（尤其獲利）有實質貢獻（原話："make a meaningful contribution to our financials"）
- 2026-08-06｜Jordan Wu｜guidance：CPO 2026 全年營收貢獻仍有限（原話："revenue contribution during this year will still be limited."）
- 2026-08-06｜Jordan Wu｜product：CPO 敘事：管理層稱對量產成功的信心較一季前又升一級（原話："It has surely risen to another level compared to even just"）
- 2026-08-06｜Jordan Wu｜competition：CPO 競爭：管理層稱自己據其所知是唯一採晶圓級光學的供應商（原話："providing optics using wafer-level optics or wafer-based"）
- 2026-08-06｜Jordan Wu｜competition：管理層認為 CPO 市場夠大，數年後不會只有 Himax 與 FOCI 一家供應商（原話："and FOCI will be the only player, the only vendor in the"）
- 2026-08-06｜Jordan Wu｜competition：車用 HUD Tcon 等進階功能被管理層稱為對抗競爭者的護城河（原話："strong moat that helps fend off competitors."）
- 2026-08-06｜Jordan Wu｜competition：Q&A 稱 Himax 是 LTDI 解決方案目前市場上的獨家供應商（原話："exclusive supplier of the solution in the market right now"）
- 2026-08-06｜Jordan Wu｜product：準備稿口徑：超大尺寸車用面板每片 LTDI 用量（Q&A 另稱至少 5 顆含 1 顆 Tcon）（原話："4 or more LTDI chips and in some cases, more than 10"）
- 2026-08-06｜Jordan Wu｜product：車用 OLED 大量放量預期落在明年下半年起並延伸至 2028（原話："major ramping expected starting from probably second half"）
- 2026-08-06｜Jordan Wu｜product：LCoS 目前仍在爭取設計案，管理層稱明年不會是量產題材；WiseEye 才是明年題材（原話："win. So that is not going to be a mass production story for"）
- 2026-08-06｜Jordan Wu｜customer：一家全球領導品牌已推出採用 WiseEye 的智慧眼鏡（原話："Recently, a leading global brand just launched a smart"）
- 2026-08-06｜Jordan Wu｜customer：含超大規模雲端業者在內的新客戶進入智慧眼鏡，部分專案 2027 量產（原話："are now entering smart glasses market with some projects"）
- 2026-08-06｜Jordan Wu｜commitment：智慧眼鏡營收量化時程：管理層稱再給 2 季以上才能較好量化（原話："give us 2 or more quarters, we should be able to quantify"）
- 2026-08-06｜Jordan Wu｜customer：Q3 平板 IC 預期季減，原因為產能限制（原話："are expected to decrease sequentially as capacity"）
- 2026-08-06｜Karen Tiao｜customer：Q2 大尺寸驅動 IC 下滑，管理層歸因於面板廠先前提前拉貨（原話："panel makers pulling forward their inventory purchases for"）

### 問答異常語氣（迴避／改口／保留）
- HIMX_Q2_2026_Earnings_Call_20260806.md｜問：Nomura 追問『2027 CPO meaningful 如何定義』並請提供 2027 整體展望｜答法：不給 CPO 數字，稱 meaningful 即 meaningful、非低個位數百分比；2027 整體展望只給定性、並將 CPO 排除在外；稱公司通常不提供超過一季的財測
- HIMX_Q2_2026_Earnings_Call_20260806.md｜問：Morgan Stanley 追問 CPO 競爭者與 Himax 的關鍵優勢｜答法：稱公司政策是不評論競爭，並稱不公開談技術優劣比較；改談市場夠大、聚焦自身驗證與量產
- HIMX_Q2_2026_Earnings_Call_20260806.md｜問：線上問題：2027 智慧眼鏡營收走勢與量｜答法：稱主要客戶尚未回饋晶片需求數量，不給量化；表示需 2 季以上才能量化

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
{"date":"20260703","verdict":"觀望","role":"候選/追蹤池","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"車用顯示領先（TDDI 50%+）維持，單車搭載量成長帶動基本盤溫和復甦","columns":{"2Y 驗證點":"車用 IC FY26 YoY &gt; +10%；Q2-Q4 26 GM 回升至 32%+","5Y 驗證點":"車用 IC 占比 ≥ 55%；OLED/LTDI TDDI 接棒第二成長曲線","具體數字門檻":"車用 IC FY26 &gt; $460M（+10% YoY）；GM FY27 ≥ 33%","漂移觸發（QC-35 分級）":"車用 IC 連 4 季 YoY &lt; +5% → 削弱（5Y 假設連 4 季）"}},{"id":"H2","text":"WLO/LCoS/CPO/WiseEye AI 期權至少一項變現（binary、時程未證實）","columns":{"2Y 驗證點":"2H26 AR 眼鏡量產客戶點名 + WLO/LCoS 季營收 &gt; $10M；或 CPO 進 Nvidia 供應鏈","5Y 驗證點":"2028-30 光學/CPO 段占營收 ≥ 15%","具體數字門檻":"2026 光學/CPO 占比 ≥ 3%；2028 ≥ 10%","漂移觸發（QC-35 分級）":"連 3 季量產時程再滑動 + 無客戶點名 → 期權折現率上調（Bull 機率下修）"}},{"id":"H3","text":"正常化毛利率結構性 ~31-33%（不回 40% 峰值），正常化 ROIC 8-10%","columns":{"2Y 驗證點":"循環中段 GM 穩定 31-33%、OM 回到 10-12%","5Y 驗證點":"穿越週期 GM 中樞 ~32%、ROIC ~9%","具體數字門檻":"FY27 GM &gt; 32%；正常化 OM &gt; 10%","漂移觸發（QC-35 分級）":"連 4 季 TTM GM &lt; 30% 且同業持平 → 結構性侵蝕（Bear 上調）"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":5.2,"ev5y_pct":30.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"候選/追蹤池","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.9,"ev5y_pct":30.0,"irr_base_pct":5.2,"max_dd_pct":-55.0,"bull_5y_price":27.0,"bear_5y_price":6.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":13.15,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
