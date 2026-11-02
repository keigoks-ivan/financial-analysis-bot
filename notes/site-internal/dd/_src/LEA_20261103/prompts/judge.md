你是 stock-analyst **v20 判斷 agent**，標的 LEA（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"LEA","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_net_sales","label":"營收（GAAP net sales）","value":5773.0,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}},{"id":"f_kpi1_core_operating_earnings_","label":"Core operating earnings（Non-GAAP 營業利益）","value":255.7,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}},{"id":"f_kpi2_core_operating_margin_no","label":"Core operating margin（Non-GAAP）","value":4.43,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（255.7÷5,773.0）"}},{"id":"f_kpi3_gaap_net_sales_cogs_sg_a","label":"GAAP 營業利益（net sales−COGS−SG&A−無形資產攤銷，自損益表推算）","value":197.0,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（損益表推算；公司未單列營業利益）"}},{"id":"f_kpi4_gaap","label":"GAAP 營業利益率","value":3.41,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm（197.0÷5,773.0，推算）"}},{"id":"f_kpi6_eps","label":"調整後 EPS","value":3.71,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}},{"id":"f_kpi7_2026_net_sales","label":"2026 全年財測：Net sales","value":"23,350–23,750","period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}},{"id":"f_kpi8_2026_core_operating_earn","label":"2026 全年財測：Core operating earnings","value":"1,080–1,200","period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}},{"id":"f_kpi10_adjusted_ebitda","label":"Adjusted EBITDA 全年財測","value":"1,700–1,820","period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}},{"id":"f_kpi11_content_per_vehicle","label":"Content per vehicle（北美／歐非）","value":"682／505","period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-30","period":"2026-10-30","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-30"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_lea_gross_margin_pct","label":"LEA 毛利率","value":6.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_operating_margin_pct","label":"LEA 營業利益率","value":3.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lea_fcf_margin_pct","label":"LEA FCF 利潤率","value":3.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_adnt_gross_margin_pct","label":"ADNT 毛利率","value":6.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADNT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_adnt_operating_margin_pct","label":"ADNT 營業利益率","value":2.83,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADNT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_adnt_fcf_margin_pct","label":"ADNT FCF 利潤率","value":1.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADNT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_gross_margin_pct","label":"APTV 毛利率","value":19.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_operating_margin_pct","label":"APTV 營業利益率","value":9.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aptv_fcf_margin_pct","label":"APTV FCF 利潤率","value":3.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_gross_margin_pct","label":"MGA 毛利率","value":14.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_operating_margin_pct","label":"MGA 營業利益率","value":5.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mga_fcf_margin_pct","label":"MGA FCF 利潤率","value":7.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_fcf_329_3_170_9","label":"自由現金流（FCF = 營運現金流 329.3 − 資本支出 170.9）","value":158.4,"period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}},{"id":"f_kpi9_2026_fcf","label":"2026 全年財測：FCF／營運現金流／重組成本","value":"FCF 565–665；OCF 1,225–1,325；重組 ≈200","period":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-10-03，公告於 2026-10-30）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99.1，與 IR 稿同文）https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":123.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-3.55,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":60.51,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.07,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（14.98 → 14.99）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.3,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.68 → 16.73）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.62,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.4 → 19.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":14.99,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":16.73,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":19.52,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.47,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 14.92 → 14.99（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":10.78,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝7.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":7.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.25,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝25.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":25.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.36,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝54.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":54.3,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":8.26,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 14.99，分子＝快照價 123.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.488,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":2612.2,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 3507.7、現金 895.5（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":48.19,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":8578.37,"period":"2026-11-03","unit":"USD m","basis":"市值 5966.17 ＋ 淨負債 2612.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":23661.24,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":23891.57,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.36,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 123.36 / W52 124.57 / W104 108.65 / W250 116.29 / W250 13週斜率 -0.59%"},{"id":"f_ma_w52","label":"52 週均線","value":124.57,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":108.65,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":116.29,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.59,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Lear 10-K：Lear為全球兩大整椅供應商之一，2025年全球份額26%；主要對手含Adient、Forvia、Magna、Jifeng/Grammer、Toyota Boshoku、TS Tech、延鋒，另有車廠自製（比亞迪旗下FinDreams等）","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"we believe we are one of the two largest suppliers of complete seat systems globally on the basis of revenue with strong positions in all major markets and a 26% global market share in 2025.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Lear 10-K風險因子：新進入者與中國本土供應商（財務報酬要求較低）正在挑戰傳統供應商份額","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"Chinese domestic suppliers that may have lower financial return expectations are also challenging traditional automotive suppliers for market share.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Lear 10-K風險因子：中國本土車廠擴張份額，使傳統車廠（Lear大客戶）營收與份額下滑","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"Chinese domestic automakers, in particular, continue to expand their market share in China (through electric vehicles) and outside of China with both innovative designs and attractive pricing. As a result, several traditional automakers have experienced declines in revenue and market share.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Lear 2026 Q3 業績新聞稿：整椅新單含北美車廠替代與未來專案、Mahindra最大印度整椅單、BYD與中國豪華EV廠專案；E-Systems歐洲商用車conquest電子單","source":"Lear 8-K Ex.99.1 (2026-10-30)","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm","excerpt":"automaker in North America, our largest complete seat award in India with Mahindra & Mahindra, an award with a Chinese luxury EV automaker in China and awards with BYD in Indonesia and Thailand; a ComfortFlex™ award with Mercedes; and ComfortMax SeatTM and FlexAir® awards with JLR •Continued to grow our core E-Systems products with a conquest award on a commercial and passenger van with a","as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Lear 2026 Q2 業績新聞稿：Audi新單與conquest整椅單（歐、北美）、Leapmotor南美整椅單","source":"Lear 8-K Ex.99.1 (2026-07-31)","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000065/lear-2026jul31_8xkxex991.htm","excerpt":"•Expanded our Seating leadership position through significant new and conquest awards with Audi for complete seats, ComfortFlex™ and FlexAir® in Europe and North America, a complete seat award with Leapmotor in South America (an important award with a Chinese automaker outside of China) and being named the 2025 General Motors Supplier","as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"+","claim":"GM 授予 Lear Orion 廠大型 SUV 與全尺寸皮卡整椅（2027 起量產），非減量","source":"Lear Q4 2025 earnings call transcript (roic.ai)","url":"https://www.roic.ai/quote/LEA/transcripts/2025-year/4-quarter","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"Lear 2026 年累計約 29 億美元新訂單，過半為新增或搶單（conquest）專案，含 Renault 原由他家供應之替換案","source":"MarketBeat Lear Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/lear-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025年GM占Lear淨銷售22%，Ford 12%，Mercedes-Benz與Volkswagen各10%，Stellantis 9%（前五大合計約63%）","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"In 2025, General Motors, one of the largest automotive and light truck manufacturers in the world, accounted for 22% of our net sales. In addition, Ford accounted for 12%, Mercedes-Benz and Volkswagen each accounted for 10% and Stellantis accounted for 9% of our 2025 net sales.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K風險因子載明主要客戶產量下滑或財務困境可能損害Lear財務表現；傳統車廠（Lear最大客戶）受中國車廠擴張侵蝕市占","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"As these traditional automakers are among our largest customers, our business and financial results may be adversely affected by decreases in their businesses or market share.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"一次網搜未找到2026年Lear或其主要客戶的信評降級、破產或財測下修相關來源；搜尋結果中的信評行動皆為2000年代中期舊資料","source":"WebSearch 結果彙整","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"S&P Global Mobility 5月更新將北美2027輕型車產量預測下調33.9萬輛，理由是油價情境持續影響至2027年（需求、生產成本、供應鏈承壓）","source":"autoinformed.com - May 2026 Light Vehicle Production Forecast is Down Again (S&P Global Mobility)","url":"https://autoinformed.com/?p=103293","excerpt":"North America's vehicle production outlook was reduced by 13,000 units for 2026 and 339,000 units for 2027.","as_of":"2026-05-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"ITR Economics預期北美輕型車產量2027約-2.1%、2028約+4.6%，維持在約1,500萬至1,560萬輛區間","source":"heattreat.net - Automotive and Heavy-Duty Truck Forecasts Point to Two Different Paths Through 2028","url":"https://www.heattreat.net/news/automotive-and-heavy-duty-truck-forecasts-point-to-two-different-paths-through-2028","excerpt":"ITR expects annual production to remain in a relatively narrow range of approximately 15.0 million to 15.6 million units through 2028.","as_of":"2026-07-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"GlobalData 8月下調2027全球輕型車產量預測30萬輛，主因中國","source":"just-auto - China weighs down on global light vehicle production forecast","url":"https://www.just-auto.com/features/china-weighs-down-on-global-light-vehicle-production-forecast/","excerpt":"GlobalData has reduced its 2027 LV production forecast by 300k.","as_of":"2026-08-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Lear 10-Q：座椅產品同時適用ICE與電動化架構；全球逾500個車款有Lear內容","source":"SEC Lear Corp 10-Q (FY2026)","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000092/lear-20261003.htm","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Lear FY2025 10-K Item 3 未列出重大反壟斷程序，僅稱涉及一般商業、產品責任、環境等法律程序；細節見 Note 12。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"We are involved from time to time in various legal proceedings and claims, including, without limitation, commercial or contractual disputes, product liability claims, and environmental and other matters.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因子將反壟斷列為一般性風險類別（普通營運過程中可能出現的訴訟），未指認具體調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"These claims typically arise in the normal course of business, including, without limitation, commercial or contractual disputes, including disputes with our customers, suppliers or competitors, intellectual property matters, personal injury claims, environmental matters, tax matters, employment matters and antitrust matters.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Lear 10-K FY2025 discloses that US tariffs apply to countries (China, Mexico, Canada) and materials (steel, aluminum, auto parts) it buys or produces, and could raise costs or hurt customers' production; export controls and sanctions also noted.","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"many of the tariffs announced, implemented or threatened by the current U.S. administration apply to (a) the countries in which we do business or from which we purchase, either directly or indirectly, materials or components, including China, Mexico and Canada, and (b) the materials or components that we purchase, either directly or indirectly, or produce, including steel, aluminum and automobile parts, among others","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Lear states US tariffs did not have a material impact on 2025 operating performance, but policies continue to evolve.","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"Although U.S. tariffs did not have a material impact on our operating performance in 2025, the policies relating to these tariffs continue to evolve","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Q3 2026 10-Q (period ended 2026-10-03) tariff and USMCA disclosure","source":"SEC EDGAR 10-Q Q3 2026","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000092/lear-20261003.htm","excerpt":"2025 tariff amounts are now recoverable from the government and no longer due from our customers, which resulted in lower first half 2026 sales and cost of sales corresponding to certain of our 2025 auto parts and all of our 2025 IEEPA tariff costs. In addition to tariffs, during the mandatory joint review on the six-year anniversary of the United States-Mexico-Canada Agreement (\"USMCA\") on","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Lear 年報稱美國現行關稅適用於其營運或採購所在國（含中國、墨西哥）及鋼鋁等材料，可能推高營運成本或迫使更換供應商","source":"SEC Form ARS FY2025 (Lear)","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000027/lear-2025dec31_10xkfinal.pdf","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026 年 10-Q 稱與客戶有合約可回收迄今絕大部分關稅成本但無法保證客戶持續同意；並提及伊朗戰事與區域緊張可能造成能源與供應鏈中斷，迄今無重大影響","source":"SEC Form 10-Q (period ended 2026-10-03)","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000092/lear-20261003.htm","excerpt":null,"as_of":"2026-10-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"PolicyRisk 摘要稱 2026 年 USMCA 檢討可能衝擊 Lear 高度集中於墨西哥的製造布局","source":"PolicyRisk company page LEA","url":"https://policyrisk.com/world/company/LEA","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Lear 68% 製造設施位於低成本國家","source":"MarketScreener","url":"https://www.marketscreener.com/news/lear-corporation-sitting-on-growth-ce7e51d2dc8ffe24","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 Seating 淨銷售約 $4.3B，年增約 2%（+$76M），新業務貢獻 $172M；segment earnings $238M，利潤率 5.5% vs 5.6%；Lear 平台產量下降使獲利減少 $14M","source":"Lear 8-K Ex.99.1 Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 E-Systems 淨銷售 $1,446.9M vs $1,430.2M（+1%），商業回收部分被售價下調抵銷；segment earnings $50.0M vs $41.0M，利潤率 3.5% vs 2.9%","source":"Lear 8-K Ex.99.1 Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"S&P Global Mobility 2026年6月更新：全球輕型車銷售 2026 年 89.4M、2027 年 91.6M（2025 年 91.9M），因中國需求疲弱與伊朗戰爭下修","source":"S&P Global Mobility rapid-impact analysis（經搜尋摘要轉述）","url":"https://www.spglobal.com/automotive-insights/en/rapid-impact-analysis/china-domestic-market-weakness-lowers-global-vehicle-forecast","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Lear 稱 Q3 2026 總公司成長超越市場 4 個百分點；Q2 Seating 超越市場約 3 個百分點；年初至 Q2 取得約 $2.9B 業務獎項（Seating >$2.3B、E-Systems >$500M）；Q1 中國車廠新業務獎項 $280M","source":"Lear Q3 2026 release / Q2 earnings call 摘要（MarketBeat、Lear 新聞稿）","url":"https://www.marketbeat.com/instant-alerts/lear-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：產業正經歷電動化與數位化的重大技術變革，新進者與中國本土供應商（財務報酬要求較低）挑戰既有供應商市佔；若無法差異化或維持低成本，可能失去市佔或被迫降價。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"Chinese domestic suppliers that may have lower financial return expectations are also challenging traditional automotive suppliers for market share. Further, the global automotive industry is experiencing a period of significant technological change, including in the areas of electrification and digitization.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 列示自家替代性產品：FlexAir 為傳統發泡的 100% 可回收替代、SoyFoam 為部分石油基產品替代；經查搜尋未見有具名的外部替代技術取代 Lear 座椅核心產品之來源。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"We have developed products such as FlexAir®, a 100% recyclable alternative to traditional foam, ReNewKnit®, a sustainable sueded alternative material that is fully recyclable at its end of life","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Lear 10-K 說明客戶傳統上硬體與軟體一併採購；E-Systems 正轉向 zonal 架構、並退出部分電子產品線（音響、燈光、車載充電器、telematics、利基控制器）。屬產品組合調整，非銷售通路（D2C／訂閱／平台）轉變；直接賣給全球 OEM 的模式未變。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"we are de-emphasizing and exiting certain electronics product lines, including audio modules, lighting modules, on-board chargers, telematics control units and niche electronic controllers, where we do not see a path to sustainable risk-adjusted financial returns.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Lear 於 2026-07-31 公布 Q2 並上調全年財測：Q2 營收 $6.2B（年增 3%）、調整後 EPS $4.28（去年同期 $3.47）；搜尋中未見 2026 年下調財測。","source":"Lear Reports Second Quarter 2026 Results; Raises Full-Year Guidance (Seeking Alpha PR)","url":"https://seekingalpha.com/pr/20602647","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 後全年營收財測區間 $23.54B–$24.01B（Benzinga 稱僅低端自 $23.21B 上移）；MarketBeat 稱中點由約 $23.6B 升至約 $23.8B，並預期客戶今年對中國車廠流失約 3% 份額（原 1.5%）。","source":"Benzinga LEA earnings-forecasts；MarketBeat Lear Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/lear-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"共識 vs 財測：Chartmill 稱全年營收共識 $24.02B、非 GAAP EPS $14.99；MarketBeat 引述分析師預期營收 $23.7B，兩來源共識營收不一致。MarketBeat 稱投資人可能預期更大幅上調，股價盤中走低。","source":"Chartmill: Lear Corp Rallies as Q2 Earnings Beat and Full Year Guidance Raised；MarketBeat","url":"https://www.chartmill.com/news/LEA/Chartmill-52410-Lear-Corp-NYSELEA-Rallies-as-Q2-Earnings-Beat-and-Full-Year-Guidance-Raised","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布（as-of 不一）：Bullstory 截至 2026-08-21 為 14 位分析師 Buy 共識、均價 $150.50（低 $130／高 $179）；Tickflow 截至 2026-08-01 為 20 位 Hold、均價 $135.57；MarketBeat 2026-08-03 共識 Hold、均價 $144.62（7/24 資料）。各家分析師家數與均價不同。","source":"Bullstory LEA analyst rating；Tickflow LEA forecast；MarketBeat 2026-08-03","url":"https://www.marketbeat.com/instant-alerts/lear-corporation-nyselea-given-consensus-rating-of-hold-by-analysts-2026-08-03/","excerpt":null,"as_of":"2026-08-21","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"個別評等動作：TD Cowen 2026-05-26 由 Hold 升 Buy、目標價 $165；BNP Paribas Exane 2026-08-03 降至 Hold。","source":"Nasdaq: TD Cowen upgrades Lear；MarketBeat","url":"https://www.nasdaq.com/articles/td-cowen-upgrades-lear-lea","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 新聞稿：上調全年財測（營收、營業利益、自由現金流）","source":"SEC 8-K Ex.99.1","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000065/lear-2026jul31_8xkxex991.htm","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"SEC EDGAR 近12個月（2025-11-03至2026-11-03）共7份8-K，含重大項目者1份（2026-09-24 Item 8.01，內容為庫藏股授權增至15億美元並延至2029-12-31），清單中無1.01/2.01/4.02等併購或重編項目。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000842162&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"唯一重大8-K為2026-09-24 Item 8.01：董事會批准庫藏股授權增至15億美元，期限延至2029-12-31。","source":"SEC EDGAR 8-K（2026-09-24）","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000080/lear-20260924.htm","excerpt":"On September 24, 2026, Lear Corporation (the \"Company\") announced that its Board of Directors approved an increase to the Company's share repurchase authorization to $1.5 billion and extended the term of such authorization to December 31, 2029.","as_of":"2026-09-24","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Adient 於 2026-04-27 收購密西根 Romulus 泡棉廠，美洲泡棉廠增至 10 座、全球 30 座，屬垂直整合擴張（購併既有廠，非綠地新產能）","source":"Pulse2: Adient acquisition of Romulus, Michigan foam plant","url":"https://pulse2.com/adient-acquisition-of-romulus-michigan-foam-plant-expands-automotive-seating-manufacturing-footprint-in-americas/amp/","excerpt":null,"as_of":"2026-04-27","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Lear 2026 年資本支出指引自 Q1 至 Q2 維持約 $660M（未削減），FCF 指引 Q2 上調至 $590–690M","source":"Lear Q2 2026 results (Seeking Alpha PR)","url":"https://seekingalpha.com/pr/20602647","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"Lear Orion, Michigan 整椅工廠預計 2027 初投產（供應 GM Orion 組裝廠）","source":"Lear 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000084216226000090/lear-2026oct30_8xkxex991.htm","excerpt":"and complete seats for future programs with a Chinese luxury EV automaker and with BYD. We continue to grow in E-Systems with a conquest electronics award on a commercial and passenger van in Europe, and both conquest and new wire awards with multiple customers in China,” said Ray Scott, Lear’s President and Chief Executive Officer. “Our complete seat facility in Orion, Michigan, is on track to","as_of":"2026-10-30","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Lear Q2 2026 財報電話會議摘要，可能含 OEM 庫存調整評論","source":"MarketBeat: Lear Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/lear-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Lear 2009 gross margin 3.7% (gross profit $360M) vs 5.5% ($748M) in 2008; Q1 2009 gross margin was -3.5% (gross loss $76M); 9M2009 sales fell 36.2% YoY to $7.0B.","source":"Lear Corp Form 10-K FY2009 / 10-Q FY2009 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000842162/000095012310017521/k48869e10vk.htm","excerpt":"gross profit and gross margin of $360 million and 3.7% in 2009, as compared to $748 million and 5.5% in 2008","as_of":"2010-03-01","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"Genuine Parts (distributor, not a pure supplier) fell 50.8% peak-to-trough Sep 2007 to Mar 2009 (recovered Dec 2010) and 52.7% in Jan-Mar 2020 (recovered Jan 2021); no Lear-specific stock drawdown or cycle length found.","source":"Trefis, Genuine Parts Stock Drop Looks Sharp, But How Deep Can It Go?","url":"https://www.trefis.com/stock/gpc/articles/592964/genuine-parts-stock-drop-looks-sharp-but-how-deep-can-it-go/2026-03-10","excerpt":null,"as_of":"2026-03-10","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單中無Item 1.01/2.01等併購類項目（僅1份重大項目為庫藏股8.01）；網搜亦未見2026年Lear併購案（搜尋僅見2024 WIP、2025年2月StoneShield等較舊交易）。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000842162&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K Item 3 僅概述一般性法律程序（商業糾紛、產品責任、環境），未點名重大個案；網搜未見近期證券集體訴訟（搜到的訴訟均為2006–2014年舊案）。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"We are involved from time to time in various legal proceedings and claims, including, without limitation, commercial or contractual disputes, product liability claims, and environmental and other matters.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"0","claim":"FY2025 10-K 附註揭露客戶可就保固與召回向公司求償且已有客戶提出此類主張，未點名具體召回事件；網搜未見2026年Lear專屬召回。","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/842162/000084216226000011/lear-20251231.htm","excerpt":"The Company is party to agreements with certain of its customers, whereby these customers may pursue claims against the Company for contribution of all or a portion of the amounts sought in connection with warranty and recall matters, and certain of the Company's customers have asserted such claims against the Company.","as_of":"2026-02-13","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月8-K清單中無Item 4.02（財報不可依賴／重編）項目；網搜僅見2004–2006年舊SEC事項，無近期調查。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000842162&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 7 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"LEA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.86,"operating_margin_pct":3.67,"fcf_margin_pct":3.58,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LEA","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ADNT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":6.32,"operating_margin_pct":2.83,"fcf_margin_pct":1.95,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADNT","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"APTV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.63,"operating_margin_pct":9.75,"fcf_margin_pct":3.65,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APTV","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MGA","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":14.71,"operating_margin_pct":5.48,"fcf_margin_pct":7.52,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MGA","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"LEA"},"financial_history":{"ticker":"LEA","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":20891500000.0,"revenue_yoy_pct":null,"gross_margin_pct":6.75,"operating_margin_pct":3.13,"net_income":327700000.0,"diluted_eps":5.47,"free_cash_flow":383200000.0,"fcf_margin_pct":1.83,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":23466900000.0,"revenue_yoy_pct":12.33,"gross_margin_pct":7.29,"operating_margin_pct":3.98,"net_income":572500000.0,"diluted_eps":9.68,"free_cash_flow":622800000.0,"fcf_margin_pct":2.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":23306000000.0,"revenue_yoy_pct":-0.69,"gross_margin_pct":7.03,"operating_margin_pct":3.81,"net_income":506600000.0,"diluted_eps":8.97,"free_cash_flow":561400000.0,"fcf_margin_pct":2.41,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":23259100000.0,"revenue_yoy_pct":-0.2,"gross_margin_pct":6.47,"operating_margin_pct":3.34,"net_income":436800000.0,"diluted_eps":8.15,"free_cash_flow":527200000.0,"fcf_margin_pct":2.27,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/LEA/LEA_Q3_2026_Earnings_Call_20261030.md）

# Q3 2026 Earnings Call
**Lear Corporation** | Earnings Calls | 2026-10-30

**Operator** (Operator):
Good morning, and welcome to the Lear Corporation Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please also note today's event is being recorded. At this time, I'd like to turn the floor over to Tim Brumbaugh, Vice President, Investor Relations. Please go ahead.

**Tim Brumbaugh** (Executives):
Thanks, Jamie. Good morning, everyone, and thank you for joining us for Lear's Third Quarter 2026 Earnings Call. Presenting today are Ray Scott, Lear President and CEO; Jason Cardew, Senior Vice President and CFO; and Jared Fedele, Vice President of Finance for Seating and E-Systems, who will succeed Jason as CFO starting in March. Other members of Lear's senior management team have also joined us on the call. Following the prepared remarks, we will open the call for Q&A. You can find a copy of the presentation that accompanies these remarks at ir.lear.com.
Before Ray begins, I'd like to take this opportunity to remind you that as we conduct this call, we will be making forward-looking statements to assist you in understanding Lear's expectations for the future. As detailed in our safe harbor statement on Slide 2, our actual results could differ materially from these forward-looking statements due to many factors discussed in our latest 10-K and other periodic reports. I also want to remind you that during today's presentation, we will refer to non-GAAP financial metrics. You are directed to the slides in the appendix of our presentation for the reconciliation of non-GAAP items to the most directly comparable GAAP measures.
The agenda for today's call is on Slide 3. First, Ray will review highlights from the quarter and provide a business update. Jason will then review our third quarter results, and Jared will provide an update on our full year guidance. Finally, Ray will offer some concluding remarks. Following the formal presentation, we would be happy to take your questions. 
Now I'd like to invite Ray to begin.

**Raymond Scott** (Executives):
Thanks, Tim. Before I begin, I want to touch on the upcoming important change to the leadership of our finance organization. After more than 34 years of dedicated service to Lear, Jason Cardew has elected to retire. I want to thank Jason for his leadership, his commitment, and his many contributions to Lear. Jason and I have worked closely together for many years. And not only has he been a trusted partner, but he is also a dear friend. Jason, your next chapter is incredibly well deserved, and I wish you and your family all the best.
Jared Fedele will succeed Jason as the CFO effective March 1. Jared has been with Lear for 23 years and has a broad global financial and operational experience. He has been working closely with Jason and me for many years and is more than ready to assume the role. Jared, congratulations. I look forward to continuing to work closely with you, and I know you will continue to execute our strategy to deliver improved financial performance and value to our shareholders.
Okay. With that, please turn to Slide 5, which highlights our key financial metrics for the third quarter. They continued delivering meaningful year-over-year improvements across all metrics in the third quarter. Sales increased 2% to $5.8 billion despite global industry production declining by 2% on a Lear-weighted basis. Core operating earnings were $256 million, a 6% increase and the fourth straight quarter of year-over-year improvement. Adjusted earnings per share reached $3.71, a 33% increase from the third quarter of 2025, accelerated by our robust share repurchases this quarter. We generated operating cash flow of $329 million and free cash flow of $158 million in the quarter.
Slide 6 summarizes our key business and financial highlights for the quarter. Our 4 strategic priorities continue to drive our focused execution, extending our global leadership in Seating, expanding E-Systems margins, growing our competitive advantage and operational excellence through IDEA by Lear, and supporting sustainable value creation with disciplined capital allocation.
During the quarter, we continued our momentum of winning key awards in both segments, generating approximately $3.9 billion of net business awards year-to-date with approximately $3.1 billion in Seating and approximately $800 million in E-Systems. This represents an increase of $1 billion during the quarter, with E-Systems on track for another year of over $1 billion of business awards. Key Seating wins in the quarter include the complete seat, foam, and heat for two programs with a North American automaker. One award is the replacement of a program we currently supply, and the second is a new award for a future program to support this customer's expansion of their product portfolio for the North American market.
Our IDEA by Lear capabilities were instrumental in winning these awards. Lear is the #1 seat supplier in India. During the quarter, we were awarded the largest complete seat program in our long history with Mahindra & Mahindra. The award includes both replacement and incremental new business. Our new awards for ComfortFlex, ComfortMax, and FlexAir applications this quarter bring our modular and innovative seat product total to 47. Program with Mercedes is a conquest award, replacing current lumbar and massage components with a ComfortFlex modular solution. Awards with Jag Land Rover include a FlexAir application as well as a ComfortMax solution integrating heat into the trim cover. Five modular projects launched during the third quarter, and 7 additional programs will be launching during the fourth quarter, accelerating the adoption of our modular solutions in the marketplace.
Our momentum with the Chinese automakers continued in both segments. In Seating, we were awarded an upcoming program with a Chinese luxury EV automaker projected to launch in 2028. This program is currently projected to be sold in China and exported to other markets. BYD also awarded us 2 key programs as they expand their production in Thailand and Indonesia. We currently supply those programs in China. In E-Systems, we won a conquest award with JMC Ford joint venture, new wiring business with FAW VW, and 2 nonconsolidated wire awards with BAIC, all in China.
We continue to drive growth in our core E-Systems products by securing electronics and wire conquest awards. The electronics award is for power distribution box on a commercial and passenger van in Europe with a North American automaker. An additional conquest wire award is with Honda in China. As we continue to grow with Japanese customers, we are also retained -- we also retained an important wire program with Jag Land Rover in Europe. During the quarter, we released our annual sustainability report, providing an update on our IDEA by Lear initiatives as well as progress towards achieving our environmental stewardship, social responsibility, and governance goals.
Our strategic focus continues to drive improved financial performance despite challenging industry conditions. Total company revenue increased 2% compared to the third quarter of 2025, reflecting growth over market of approximately 4 percentage points. Both segments outperformed the market despite headwinds from the roll-off of programs such as the Escape and Corsair and the wind-down of our noncore E-Systems products. With Seating growing approximately 4 percentage points above market and E-Systems approximately 2 percentage points above market, excluding the impact of the wind-down business, E-Systems growth over market was 5 percentage points. Operating margins expanded 20 basis points year-over-year for the total company, with E-Systems margins expanding 60 basis points, driven by another strong quarter of 120 basis points of net performance. Seating margins grew 20 basis points, driven by 40 basis points of net performance, keeping us on track to deliver our full year target.
Our strong free cash flow generation allowed us to further accelerate our share repurchases. We repurchased $175 million of shares in the third quarter, completing our full year repurchase target of $350 million. As a result of our strong earnings growth and accelerated share repurchases, our third quarter EPS increased 33% year-over-year. With our current authorization set to expire in 3 months, we increased our share repurchase authorization to $1.5 billion and extended it through 2029, reinforcing our commitment to returning capital to shareholders.
Slide 7 provides a further breakdown of our progress on delivering long-term revenue growth and margin expansion, providing confidence we will achieve our full year targets. Over half of our year-to-date seating awards have been for new or conquest programs, providing a strong foundation of future growth. In the quarter, we were awarded conquest programs with Stellantis in Europe and with Honda in Thailand as we continue to build our relationships with Japanese customers. In E-Systems, approximately 70% of our year-to-date business awards have been for new or conquest programs, continuing the trend from the first half of the year. During the quarter, wire conquest awards included programs in China with JMC Ford and Honda. The rollout of our Thermal Comfort modular solutions continues to gain momentum with the modularity and FlexAir wins in the quarter.
The pace of business awards with Chinese automakers continues to accelerate. In Seating, our year-to-date awards are estimated to generate over $600 million of average annual revenue, up almost 90% from where we were tracking at the end of the second quarter. This reflects the growing momentum of our global wins with Chinese automakers, including with BYD in Thailand and Indonesia, following our second quarter award with Leapmotor in South America. In E-Systems, approximately 25% of our year-to-date awards are with Chinese domestic automakers, up significantly from 2025.
We remain on track to deliver $75 million of IDEA savings this year with approximately $55 million achieved year-to-date, accelerating through the end of the year and are on track to significantly exceed our targeted restructuring savings. Our net performance continues to drive increased adjusted operating margins in both segments. Despite rising commodity and other input costs, Seating has generated 30 basis points of net performance through the first 3 quarters, and we expect a step up in the fourth quarter to deliver our full year target of 40 basis points. In E-Systems, we delivered a very strong 105 basis points of net performance through the first 3 quarters. We expect E-Systems to deliver positive net performance in the fourth quarter despite increasing copper and launch costs, a testament to our team's ability to execute.
I want to spend a moment on Slide 8, which provides an overview of our Orion, Michigan facility that will support 3 of GM's most important nameplates, the Cadillac Escalade, Chevrolet Silverado, and the GMC Sierra. The Orion facility, which represents a critical milestone in the execution of IDEA by Lear technology road map, is the most tangible demonstration of how our strategy is redefining JIT seat assembly, reinforcing Lear's position as the clear leader in seating, and creating a path to future market share gains and sustainable profitable growth. 
IDEA by Lear is our framework for reimagining how we operate, embedding innovation, digital tools, engineering, and automation into every layer of the processes. We've been building towards this facility, which integrates the technology and talent we have compiled through our targeted acquisitions and significant internal development to deliver something that, quite frankly, doesn't exist in the seating world outside of Lear.
Production in the state-of-the-art just-in-time seating facility begins next year. This facility is designed from the ground up with a digital foundation and automation embedded throughout from day 1, not retrofitted. The financial impact is meaningful and immediate. We expect automation to reduce the conversion cost requirements by 10% to 15% -- the more important story is what this represents strategically. Orion is the blueprint we intend to scale across our global seating footprint to support our future key programs such as the Ford Super Duty. Each of the key technologies we are developing reflects a deliberate capability we've built or acquired. And together, they tell the story of what IDEA by Lear looks like in practice.
The first is what we call integrated intralogistics. I want to be precise about the term because it goes well beyond traditional automated warehousing. Intelligent intralogistics is the connected intelligence layer of the entire factory. It ties together inventory, material management, storage, and real-time decision-making from the moment a component arrives at our dock to the moment a finished seat leaves our facility. We really think about -- we think about it across 3 dimensions.
The first one is connected. This is about end-to-end visibility and control. Nothing moves without us knowing about it. At Orion, that means our overhead suspended material storage and delivery system is fully integrated into the production floor to track parts in real time. Our automated guided vehicles, or AGVs, keep the lines continuously fed with complete traceability. Our automated trailer loading and sequencing closes the loop, connecting finished goods all the way through to the customer's shipment with precision and without manual intervention. From inbound components to outbound delivery, we see everything.
The second dimension is intelligent. Visibility alone isn't enough. The system has to think and react. Advanced analytics are continuously driving decisions around inventory positioning, replenishment, and flow. Our 4D 4-directional storage system utilizes autonomous mobile robots, or AMRs, that navigate dynamically within the racking structure itself to optimize in real time based on production demand. Our raw component automated storage and retrieval systems, or ASRS, manage foam and trim storage, while our finished goods ASRS are both continuously informed by analytics and anticipating needs before they become disruptions. 
Both of these ASRS systems were developed internally by our ASI team, which is the company we acquired. We own the IP, we control the road map, and we can scale it across our global footprint. That is a genuine competitive advantage that cannot be easily replicated. Not only is our material handling intelligent, but so is our balancing of human capital. We are utilizing proprietary tools like cycle time deviation and dynamic line scheduling to make real-time adjustments to optimize the efficiency of our employees.
The last one is autonomous. This is where the financial impact becomes most tangible. We are moving towards automated execution, meaning our people are focused on solving problems, not performing routine tasks. Robotic part loading is actively in production today, feeding our lines and installing components with a level of consistency and repeatability that manual processes simply cannot match. Our AGV network operates without human direction. Our ASRS systems retrieve and position material without manual intervention. The factory increasingly runs itself, allowing our teams to focus on more value-added adjustments. Our automated smart ovens, robotic fines, and end-of-line testing improve our process consistency, cycle time, and quality.
They also improve the job satisfaction of our team. Interconnectedness is what is new at Orion. We've been adding independent systems in our existing location, but the interconnectedness across multiple processes driven off demand will improve efficiency and inventory management due to real-time monitoring, analysis, and adjustments. Built by Lear's team and leveraging historical knowledge, our systems don't just reduce costs. They create a factory that sees everything, decides intelligently, and executes autonomously. What we built at Orion will become the blueprint for scaling productivity across our complete seating footprint. 
And with that, I'm going to turn the call over to Jason and Jared for the financial review.

**Jason Cardew** (Executives):
Thanks, Ray. Slide 10 shows vehicle production and key exchange rates for the third quarter. Global production was down 2% compared to the same period last year. Production volumes declined by 5% in North America and 7% in China, while volumes in Europe were up 1%. The U.S. dollar strengthened against the euro but weakened against the RMB.
Turning to Slide 11, I will highlight our financial results for the third quarter of 2026. Our sales increased 2% year-over-year to $5.8 billion. Organic sales were also up 2%, primarily reflecting the addition of new business in Seating. Core operating earnings were $256 million compared to $241 million last year, driven primarily by strong net operating performance. Adjusted earnings per share were $3.71 as compared to $2.79 a year ago, reflecting higher earnings and the benefit of our share repurchase program. Third quarter operating cash flow was $329 million compared to $444 million last year due to higher tooling and engineering investments and the timing of working capital. Year-to-date, operating cash flow is higher compared to 2025, driven by improvements in inventory management through our IDEA by Lear initiatives as well as the timing of tariff payments and recoveries.
Slide 12 explains the variance in sales and adjusted operating margins for the third quarter in the Seating segment. Sales for the third quarter were $4.3 billion, an increase of $76 million or 2% from 2025. Organic sales were also up 2%, reflecting the addition of new business, including the BMW iX3, Mercedes GLC EQ, and Audi Q7 in Europe, the Seres M6 in China, and the Jeep Cherokee in North America, and higher volumes on JLR platforms, which were negatively impacted by the cybersecurity attack during the third quarter last year, partially offset by lower volumes on Lear platforms in China and North America. Adjusted earnings were $274 million, up $13 million or 5% compared to 2025, with adjusted operating margins of 6.3%. Higher operating margins were driven by strong net performance and our margin-accretive backlog, partially offset by lower volumes on Lear platforms.
Slide 13 explains the variance in sales and adjusted operating margins for the third quarter in the E-Systems segment. Sales for the third quarter were $1.4 billion, an increase of $17 million or 1% from 2025. Organic sales were up less than 1%, driven by higher volumes on Lear platforms, including several JLR programs in Europe, partially offset by the build-out of the Ford Escape, Focus, and Lincoln Corsair reflected in our backlog as well as the wind-down of discontinued product lines. 
Adjusted earnings were $69 million or 4.8% of sales compared to $60 million and 4.2% of sales in 2025. Higher operating margins were driven by strong net performance and higher volumes on Lear platforms, partially offset by the build-out of the programs in our backlog and the wind-down of discontinued product lines. 
Jared will now provide an update on our full year outlook.

**Jared Fedele** (Executives):
Thanks, Jason. Slide 14 provides global vehicle production volume and currency assumptions that form the basis of our 2026 full year outlook. Our production assumptions are based on several sources, including internal estimates, customer production schedules, and mobility global forecast. At the midpoint of our guidance range, we assume that global industry production will be down 1% on a Lear sales-weighted basis compared to 2025, a slight improvement from down less than 2% in our prior outlook, primarily due to higher volumes in Europe, partially offset by lower production assumptions for China. We have adjusted our currency estimate, which now assumes an average euro exchange rate of $1.15 per euro and an average Chinese RMB exchange rate of RMB 6.80 to the dollar.
Slide 15 provides an update to our full year 2026 outlook. Our current outlook assumes no changes to current tariff policies or significant industry-wide disruptions. In recent weeks, we have seen reductions in production schedules across several customers, particularly in China. We have reduced our full year 2026 outlook for net sales to reflect these changes. However, our strong operational execution, savings from our additional restructuring actions, and anticipated resolution of ongoing commercial negotiations are expected to offset the impact of lower volumes as well as rising costs from commodities and other inputs. 
Therefore, we are maintaining our full year outlook for core operating earnings. We increased our outlook for restructuring costs by $25 million, reflecting additional actions we are taking to further optimize our cost structure and position Lear for stronger long-term profitability. We adjusted our outlook for operating cash flow and free cash flow to support this investment. As we move through the remainder of the year, we will continue to monitor the China domestic market, where consumer demand and production schedules continue to deteriorate.
Slide 16 compares our October 2026 outlook to the midpoint of our prior 2026 outlook. We reduced our revenue midpoint by approximately $225 million, driven by lower production volumes on Lear programs, particularly in China, and the impact of foreign exchange, partially offset by increasing supplier pass-through due to the rising commodity costs and commercial recoveries. [Audio Gap] core operating earnings outlook as savings from our restructuring actions and improved net performance is expected to offset the impact of lower production volumes on Lear platforms.
Moving to Slide 17, we highlighted our balanced capital allocation strategy. Our balance sheet and liquidity profile continues to be a significant competitive advantage for us. Our cost of debt is low, averaging less than 4%, and our debt structure has a weighted average maturity of approximately 11 years. In addition, we have $2.9 billion of available liquidity. Our capital allocation priorities remain consistent. We are focused on generating strong cash flow, investing in the core business to drive profitable growth, and returning excess cash to shareholders. 
During the third quarter, our strong cash flow enabled us to take advantage of our undervalued share price and repurchased $175 million worth of stock. This brought year-to-date repurchases to $350 million, achieving our increased full year target ahead of schedule. Since initiating the share repurchase program in 2011, we have repurchased $6.3 billion worth of shares and returned over 85% of free cash flow to shareholders through repurchases and dividends. In September, Lear's Board increased the share repurchase authorization to $1.5 billion and extended the authorization period through December 31, 2029, reinforcing our commitment to return cash to our shareholders. 
Now I'll turn it back to Ray for some closing thoughts.

**Raymond Scott** (Executives):
Nice job, Jared. Sounds great. Thank you. Q3 was another strong quarter, continuing our track record of consistent execution and progress. Despite a global production environment that contracted 2% on a Lear-weighted basis, our team delivered $5.8 billion in sales, expanded margins in both segments, and grew core operating earnings for the fourth consecutive quarter. Our resilience is the result of a focused strategy and a team that knows how to execute.
The breadth of our business wins in this quarter demonstrates our global reach and competitiveness. From our largest complete seat award in India to BYD programs in Thailand and Indonesia, and modular seating solutions with Mercedes and Jag Land Rover, we are winning in the markets with the customers that matter the most for our long-term growth. Our year-to-date net business awards now stand at approximately $3.9 billion, and the pipeline of new opportunities remains very robust.
In E-Systems, the transformation of our portfolio is evident with approximately 70% of our year-to-date awards coming from new or conquest programs and Q3 margins expanding 60 basis points year-over-year. We are demonstrating that our focused portfolio strategy is working. The wind-down of our noncore products is nearly behind us. And what remains is a stronger business with a significant runway ahead.
And perhaps the most exciting development this quarter is what we shared about our Orion facility. This is IDEA by Lear in action, not a pilot, not a concept, but a fully integrated purpose-built manufacturing environment that reduces the conversion cost requirements by approximately 10% to 15% and sets a new standard for what a seating facility can be. The technologies we are deploying at Orion, from intelligent intralogistics to autonomous material handling to AI-powered quality inspection, are proprietary, scalable, and represent a genuine competitive moat that will be difficult for others to replicate.
And we continue to return meaningful capital to our shareholders. Completing our $350 million repurchase target ahead of schedule and expanding our authorization to $1.5 billion through 2029 reflects both the strength of our cash generation and our conviction in the long-term value of this company. As we head into the fourth quarter, we recognize the challenges ahead, from commodity pressures to softness in the China market. These are dynamics we've successfully navigated throughout the year, and our team has the tools, talent, and track record to continue to execute. We are maintaining our full year outlook for operating income and remain confident in our ability to finish the year strong. 
And now we'll go ahead and open up the call to questions.

**Operator** (Operator):
[Operator Instructions] Our first question today comes from Dan Levy from Barclays.

**Dan Levy** (Analysts):
Jason, congratulations. Jared, congratulations to you as well. I wanted to start with a question on the sales outlook and particularly with what's happening in China. There's been a number of quarters now where you've underperformed. And I think this is similar to some of your other peers out there. But maybe you can give us a sense of, within China, what the path is to finally starting to see growth in line with the market? I know you're saying that you're targeting 50% domestic mix, but the issue is industry is at, call it, 75%-plus. I know you talked about some -- winning some programs here. But at what point do you finally start to have China be in line? And maybe you could just unpack the underperformance? Is it just this customer mix? Is it competition? What's going on in China? And how is this fixed?

**Jason Cardew** (Executives):
Yes. Thanks, Dan. I think, first, I think it's important to point out that as we look out to next year and beyond, the strategy that we put in place over the last several years will really improve the profile of our business in China and with the Chinese OEMs globally. In terms of what happened in the third quarter, there's a couple of factors that weighed on that growth or growth under market in China. A significant portion of our revenue in China with the Chinese OEMs is in our nonconsolidated joint ventures. And so if you account for that, that business actually grew in the quarter, and that would eliminate more than half of the negative growth over market in the quarter. So there are parts of the business there that are performing in line or even better than the market.
And I think the other point that's weighed on our business in the near term is the level of exports out of the China market as the domestic demand has weakened this year. And we've talked about this in the past. We're under-indexed on exports. And that's primarily because the exports to date have really focused on primarily the lower end of the market where we're underrepresented. We have a very strong business, particularly in luxury in China and the higher ends of the market. And I think over time, as the export mix shifts to higher ends of the market, we will better reflect the market overall in terms of the ratio of exports in our business.
And I think that there's a lot of evidence that we've shared this year that, again, that our strategy for growing with the Chinese automakers and in China and globally is working. We had $900 million of our $3.9 billion of new business awards this year, 23% of the new business awards this year with the Chinese automakers. Only 8.5% of our revenue today, consolidated and nonconsolidated with the Chinese OEMs. So we are clearly seeing a growth inflection point with the Chinese automakers that will benefit the business longer term. We've talked about this year and last year, our share of revenue within China that's with the Chinese OEMs, 44%. So yes, we're under-indexed there. That grows to 50% or a little bit above that next year. We see a path to 55% and beyond if you look out 2 or 3 years and include the benefit of the new awards that we've announced this year.
And so all signs point to our business more closely reflecting the mix that is represented in the market in China. And I think that there are some regulatory changes that are coming over the next several years that will encourage more localization for the Chinese. And we're seeing good performance in terms of our wins with the Chinese OEMs as they localize. We had Leapmotor in South America we announced last quarter, and then we had the 2 wins with BYD this quarter. But, Jared, why don't you talk about some of those regulatory changes that we think will change the composition of exports going forward?

**Jared Fedele** (Executives):
Yes. Sure, Jason. Yes, you're correct. There are a few factors and potential regulations that have come up that are -- we look at favorably from our standpoint. And first is the potential regulation. We've talked about it on the Industrial Accelerator Act. That's the IAA and something we've been monitoring closely. And this is that Made in Europe Act. And that's being discussed in the EU that would potentially put a threshold on local content rules. Second, there's that hybrid export cap in Europe, where China and the EU are expected to agree to limit hybrid exports out of China up to 350,000 vehicles annually starting on December 1 of this year, which could help aid in the acceleration of the localization with the C-OEMs in Europe. 
So -- and then -- and finally, there's one more starting in April 1, 2027. China is going to lower the value-add tax export rebate for new energy vehicles to 9%, down from the 13%. So in simple terms, China is lowering the rebate in which they give to the OEMs for exporting NEVs. And so all these regulations, it plays to our favor and mixed with our strategy in China, winning with the C-OEMs and the relationships we've built over the last 30 years, it's going to be a positive as we continue to grow and gain market share within and now outside, as Jason mentioned, with Leapmotor and BYD already outside of China.

**Dan Levy** (Analysts):
So just the net of that, do you feel confident that, given everything that we're seeing in China, that eventually, when your larger backlog comes online, that you can eventually return to more meaningful growth? I know '27, you've sort of talked that down. But in the '28, '29 period, I think you've given some upside numbers there.

**Jason Cardew** (Executives):
Yes. As we said on the last call, we see 2029, this business returning to significant growth above market with both segments getting back to the historical targeted range, 3% to 4% in Seating and 4% to 6% in E-Systems. And one of the updates we want to provide today is on the backlog. Just this continued progress we're making with new business awards is increasing the confidence level we have in the strength of that 3-year backlog. Jared, why don't you provide an update on that?

**Jared Fedele** (Executives):
Sure. And you're correct. We do feel good about the trajectory of our backlog. And now, obviously, we're not giving official backlog update on the call. The recent wins we've communicated, it really reinforces our confidence in the long-term growth outlook. And I'll shed some color on this. In Seating, the most notable awards include significant conquest awards. We've talked about Audi in Europe, North America with the Ford Super Duty, along with complete seat awards. We just mentioned Leapmotor in South America and additional wins with the C-OEMs and awards in India now with Mahindra. Over half of those year-to-date awards have been for new or conquest programs in Seating, providing kind of that foundation for future growth. Then in E-Systems, we secured important new awards with Renault, Stellantis, BAIC, General Motors, and multiple Chinese automakers. And more importantly, over 70% of our year-to-date E-Systems awards come from the conquest business, from new or conquest business.
And based on what we know right now, knowing that the timing of launches can move and, more importantly, new awards can be sourced from now until when we report, our 3-year core backlog is about $2.25 billion. The key is with our backlog, we've been very, very selective on the profile and the quality of the business we're going after and winning. Every program has been scrutinized to make sure it's returning in excess of its cost of capital. And we're not chasing business to win business. If you look at the Ford Super Duty JIT and wire business, the Audi JIT business, the T1 SUV wire, the JIT in Orion, just these handful of programs taken together, Dan, between Seating and E-Systems, it makes up more than 70% of our backlog that's rolling out over the 3 years. So these are programs has a long history of success in the market. We have a high degree of confidence that those are going to launch on time at the volumes that we've embedded in our backlog. So the momentum is building, and, more importantly, the quality of the awards is there, and the pipeline remains robust as we sit here today. So the team is doing a really good job.

**Raymond Scott** (Executives):
Let me weigh in on this, Dan, because this is important, and I know we're focused on China. But we've laid out a plan, and we've talked about it for some time now. And we've been looking at the domestic Chinese and what was going on with market share gains throughout the world. But we said, "Listen, we can still win with the traditional OEMs as they're shrinking," and we've done that. I mean it's remarkable. I sit here and I have an enormous amount of confidence when I hear from the team, both Nick and Frank, the conquest wins we're getting. And to Jared's point, how we're being very selective after, I'll say, high-quality wins, programs that we have a high confidence that they're going to run. They're not a one-and-done program that we've all experienced over the last several years, but the high confidence that the OEs, the customers are putting a tremendous amount of effort and energy and money, and that's where we're betting and then putting our dollars.
The second thing is I was just in China last week. It was incredibly remarkable different in respect of what's going on, on the ground in China. They're looking for companies that are -- and have profitability, technology, innovation. They're taking the next step. They're concerned about some of the domestic Chinese around their profitability and because they're not profitable. And so a strong company that has a global footprint like we have, man, was just really attractive. Every meeting that we had, every dinner that we had, every event that we went to was another reassurance of our technology capabilities really mirror well as they increase into the upper ends of the luxury markets. And that's where we participate. That's where we play really nice.
And the third leg of this thing that we've been talking about for years now is the continuation of the Japanese customers. We've been somewhat limited. I love to see that door opening. What we're talking about here is you have the traditional OEMs that we're gaining and conquesting and gaining market share, which is beautiful. The Chinese that now they're starting to get into luxury and technology-focused type of components around E-Systems and Seating, you're seeing that accelerate. And then we have the Japanese growth that we mentioned on the call.
So I'm very confident. I love where we're at. It's all been about tracking net performance. The team is doing a remarkable job in net performance. That's important to really show the sustainability we have despite whatever challenges we have. But equally as important is how we look at that backlog. And that's one of our strong points right now. I'm very, very confident in our backlog. I mean I feel really good. And I got Nick and Frank in here, too, and we got more work to do. We've got a robust pipeline right now of quotes, and we're going to push through it and continue to gain more market share across those 3 different elements I mentioned. So I think it was a good question. I don't want to overly focus on China because we're hitting on all different cylinders when we talk about those 3 different areas.

**Operator** (Operator):
Our next question comes from Joe Spak from UBS.

**Joseph Spak** (Analysts):
I echo the congrats to both Jason and Jared. Maybe one just shorter term and then one longer term. You didn't really tighten your operating income range for this year. And if we sort of look like up versus down, it's like 22% for the fourth quarter. So just given that we've seen some changes to schedules recently here in the fourth quarter, I was wondering if you could try to hone in on sort of where you think you're tracking at least for the year within that range? And then on those -- if we continue that into sort of like at least early '27 where we have also seen some maybe revisions to schedules, how you're thinking about '27 right now?

**Jason Cardew** (Executives):
Yes. Starting with the outlook for the fourth quarter, it is a little bit wider range than we ordinarily would have, and we just decided to leave it intact sort of from the prior guidance at this stage. The factors that will determine where we fall within that range and what we're focused on is really continued flawless execution operationally as we've seen over the last really 2 years in both Seating and E-Systems, very strong operating performance. 
We have a number of commercial negotiations, as you might imagine, that could swing the number one way or the other, and that's another reason for the range. And the deterioration in the demand in the China market is the other key factor. And really, that change in our production outlook on our platforms in the China market is what drove the revision of our revenue guidance. 90% of the $256 million shown on the slide is in China, and then there's a little bit in Europe. So it is a dynamic market. It has been -- there has been very weak domestic demand in China throughout the year. It's accelerated a bit over the last several months, and we try to protect for that with that wider range. As we sit here today, our best estimate is right at the midpoint. But the factors I outlined will ultimately determine where we fall within that range. And then we have an investor conference in December where we'll provide an update on how the quarter is tracking at that point.
In terms of '27, we provided a lot of color on the last earnings call. We were probably a little bit early relative to others, and I know others have provided updates in this reporting cycle. And the building blocks that we outlined in terms of what would drive revenue growth and what some of the challenges were on specific platforms, nothing has changed. Nothing in the outlook for this year really has an impact on our view on '27 on the revenue side. 
And on the earnings side, the 40 and 80 basis points of net performance that we articulated for Seating and E-Systems, respectively, are still tracking -- are right on track. We do expect to do a little bit better than that in both segments this year. We did a little better than that last year. So the momentum is clearly there operationally, and we're increasingly confident in being able to deliver that net performance next year as well. So between now and February, we'll work through the final assumptions around production volumes and the timing of launches and solidify guidance and provide that in February.

**Joseph Spak** (Analysts):
And then, Ray, the Orion commentary is super interesting. And you mentioned it's a blueprint for global seating. So maybe just some commentary on how easy or how long you think you could sort of scale that across the enterprise? And is there -- are there any parts of the world where there might be something structural that would actually prevent you from accomplishing what you're doing in Orion?

**Raymond Scott** (Executives):
I think I'm glad you're asking this question because it is, I think, one of the most significant part of our strategy that we've been developing over 10 years to have that footprint. And we're obviously learning along the journey, but how we can scale that. We have been through IDEA by Lear, implementing in production environments, changes to our manufacturing plants. So we have been getting at some of it, but to have a full-scale ground-up facility like what we're doing in Orion is very unique. And I think as we set up the next plants like we talk about with the heavy duty with Ford Motor Company, will be exactly, but probably at another level. And so I focus when I say scaling, particularly around the brand-new plants on the new plants that we're putting up for our customers.
There are elements that we continue to learn that we are going to continue to improve our net performance. I think the foundation of what we talk about with sustainable margin and how we're offsetting some of these external costs is through what we're doing. And so some of them are very easily replicatable, cycle time deviation, for example. We were able to scale that across the majority of our manufacturing plants and get at a significant opportunity and savings within our plants globally. So there's some that are very easy, and there's no -- I think you mentioned a roadblock -- or an ability for us to get at. Some of them are more, I think, around the ability to get at it because production is running and having the time -- the downtime to get in and make the capital adjustments. And so they're all somewhat different in how we look at it. But the majority of them, we can get at. We already have plans to get at. That's all part of our -- how we're looking at capital, how we're looking at investments, the payback time frame, those type of things.
But one thing that I mentioned, what's great about this is when we acquired these companies, for example, like ASI and the others, we're manufacturing, becoming a manufacturing integrator leader. And we can control our own destiny when it comes to capital. So we manufacture our own capital, which is very unique. And we can design it just like we design products with a cost savings intent. 
And so we're seeing significant reductions in how we look at our capital and invest in our capital and how we get a much better cost of our capital. So I said a lot there, but I'm glad you brought the Orion facility and why I want to get that out there because we have been differentiating ourselves. It is very unique. No one has it. In my narrative, it says, "hard to replicate." I think it's almost near impossible to replicate unless you go buy the companies we bought, and that's been a 10-year. Boy, Jason, we've been at this for...

**Jason Cardew** (Executives):
10 years.

**Raymond Scott** (Executives):
10 years. And so it's great to see what's going. I was just out at the Orion facility a couple of weeks ago. I can't wait to have you out there and others because you're going to see a game-changing event when it comes to how you think about just-in-time and how we think about modularity. You have to buy the companies, particularly as you vertically integrate, you have to own the lumbar company. You have to -- well, our acquisitions have been intentional. And now we're starting to see it. 47 contracts when we talk about ComfortFlex, ComfortMax, FlexAir. It's not where I want to be. I'm never happy. I want to sell more. Frank is sitting here. And some of it's been delayed programs, things that are going on with our customers. But, man, this thing is starting to take off. And I remember 2 years ago, 3 years ago, when investors and analysts were saying, "Man, you're going to have to change the whole model." And that's exactly what we're doing. We're changing the model around how you think about sourcing a seat system and how you manufacture a seat system. So yes, I could talk about this for hours, but I'll leave it at that.

**Operator** (Operator):
Our next question comes from James Picariello from BNP Paribas.

**James Picariello** (Analysts):
How can we start to think about the commodities bridge for next year, both from a top line recovery and net EBIT perspective? I know it's early, but just curious on your prelim thoughts there regarding Seating metals exposure and E-Systems index copper. And then for this year's tariff reversal impacts to revenue, can you confirm the portion that was truly onetime and represents a static tailwind to revenue next year?

**Jason Cardew** (Executives):
Yes. I guess if you want to start with the last part of that question, I think we provided the nonrecurring portion of the tariff revenue that's embedded in the guidance for this year, and it's $200 million or so. So that would be nonrecurring, the refunds from last year. And our go-forward tariff costs are very modest because most of our tariffs are avoided through the customer offset credits. And so we don't see it as a significant issue going forward.
In terms of commodities, it's been a significant issue for us this year in terms of the gross impact. But we have a long history of indexing and back-to-back agreements that we put in place going back 6, 7, 8 years. And so the vast majority of that has been passed through. We have over $300 million in gross impact this year, and the net impact is only about $10 million. Looking out to next year, certainly, copper has run up continuously throughout the year. And we benefited a little bit in terms of the revaluation of our inventory as that has increased, and that will be nonrecurring. So that will be a little bit of a headwind for next year. 
But all of those components that we've -- that are embedded in commodities are part of the 40 and 80 basis points of net performance. So whatever we see in terms of leakage on commodities, we're offsetting through our performance activity, and we remain confident in meeting or exceeding the 40 and 80 basis points of net performance again next year in Seating and E-Systems, respectively.

**James Picariello** (Analysts):
That's really helpful. And then just as we think about restructuring savings that are clearly showing through this year, is there a sizing of what that restructuring savings number could be for next year? I know we already have the automation savings in place for '27.

**Jason Cardew** (Executives):
Yes. I think we increased the level of savings we're going to achieve this year in restructuring, I think, from $80 million to $95 million in the guidance here. And the investments we're making here in the fourth quarter will continue to benefit next year. The paybacks continue into next year. If you just look at restructuring overall, there are projects that have no payback because the program has ended production and you're restructuring capacity out with no future benefit. And then there are projects where we're embarking on labor arbitrage or other cost reduction opportunities. And those typically have about a 1.5- to 2.5-year payback. And those are the projects that we're really focused on in the fourth quarter here and into next year to ensure that we have the most competitive footprint for the long term. And in the meantime, it remains a key contributor to that net performance narrative that we've seen this year and expect to continue to see next year.

**Operator** (Operator):
And our final question today comes from Rajat Gupta from JPMorgan.

**Rajat Gupta** (Analysts):
Just wanted to touch on like the 2027 outlook or just preliminary outlook. I know you've given a lot of color on the revenue dynamics, some of the China pressures, also like some of the performance benefits that expect to remain on track. I'm just curious if there are any offsets we should think about, particularly from like some of the wind-down business that you're seeing. If you look at the E-Systems bridge this quarter, the decrementals seemed pretty high on some of the backlog and the wind-down. I'm just curious how we should think about those puts and takes in the 2027 margin bridge? And I have a quick follow-up.

**Jason Cardew** (Executives):
Yes. Again, Rajat, we've provided a lot of color on our view on '27 on the last earnings call, and we'll wait until February to provide the full guidance. But what we typically see on the wind-down is that's converting in the 20% range. It depends on the particular program within that. Backlog typically is converting in the 10% range, and volume and mix on both Seating and E-Systems tend to be 15% to 25% in that rate of conversion, depending on the level of vertical integration of the program, the underlying profitability of the program. So there -- that's -- but that is the typical range. And I think those ranges in terms of how we convert on the backlog growth into next year and the wind-down impact for next year as well as the production changes on our platform should basically hold within that range.

**Rajat Gupta** (Analysts):
Understood. And then -- and just anything we should keep in mind when it comes to just available capital for return this year versus next? From a restructuring standpoint, I know CapEx is a bit heavy this year with Orion and the automation build. I'm curious like any meaningful changes we should expect as we head into '27?

**Jason Cardew** (Executives):
Yes. Again, we'll save the pinpoint guidance for next year on that. But what I will say is that our priorities around capital allocation remain consistent. We're going to focus on investing in the business first through CapEx and tuck-in acquisitions if they become available. We don't see anything of scale in terms of the -- on the M&A side. And we're going to continue returning our excess cash to shareholders through share repurchases and dividends. I think 80% of the free cash flow we generated this year will be returned to shareholders through share repurchases and dividends. I see that level of capital return to shareholders continuing into next year, and we look forward to providing more color on the specific guidance on the fourth quarter earnings call.

**Raymond Scott** (Executives):
Just again, well, it was -- you're still around, we're still going to see you. So I won't get into this. I don't want to get emotional right now. But just to the team, I think probably Lear members are still on the phone. I just want to say thank you. Another outstanding quarter going on, a lot of dynamics in the marketplace, but we continue to stay focused on what we can control. Great job, Nick, Frank. To the teams and the operations, great wins. I appreciate all the hard work, and, Jared, nice job with the narrative today. I tried to mess you up, but you did a great job anyway. So...

**Jared Fedele** (Executives):
Thank you.

**Raymond Scott** (Executives):
Thanks to the team. Appreciate all the hard work.

**Operator** (Operator):
And with that, we'll conclude today's conference call and presentation. We do thank you for joining. You may now disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LEA_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CFO｜guidance：CFO 說全年營收中點上調至約 238 億美元，前次為 236 億。（原話："Revenue is now expected to be approximately $23.8 billion"）
- 2026-07-31｜CFO｜guidance：CFO 說全年核心營業利益中點約 11.4 億美元，前次為 11.15 億。（原話："$1.14 billion or 2% higher than our prior guidance"）
- 2026-07-31｜CFO｜guidance：CFO 說全年營業現金流中點約 13 億美元。（原話："expected to be approximately $1.3 billion"）
- 2026-07-31｜CFO｜guidance：CFO 給下半年營業利益中點 5.29 億美元，營業利益率 4.5%。（原話："second half operating income outlook is $529 million"）
- 2026-07-31｜CFO｜guidance：CFO 說全年展望假設關稅政策不變、無產業性大幅中斷。（原話："current tariff policies or significant industry-wide"）
- 2026-07-31｜CFO｜guidance：CFO 說全年全球產量假設中點為年減不到 2%，前次為減 1%，主因中國下修。（原話："than 2% on a Lear sales weighted basis compared to 2025"）
- 2026-07-31｜CFO｜guidance：CFO 給第三季營收區間 58～59 億美元。（原話："revenues to be $5.8 billion to $5.9 billion in the quarter"）
- 2026-07-31｜CFO｜margin：CFO 給第三季座椅利益率區間。（原話："We expect Seating margins in the low to mid-6s"）
- 2026-07-31｜CFO｜margin：CFO 給第三季 E-Systems 利益率區間。（原話："Systems in the low 4s."）
- 2026-07-31｜CFO｜margin：CFO 說第三季利益率低於第四季，原因含歐洲夏季停工與銅價回收時間差。（原話："Q3 margins will be lower than the"）
- 2026-07-31｜CFO｜margin：CFO 說上半年 E-Systems 受惠於銅庫存重估，第三季出現回收落差。（原話："where we benefited in the first half of the year"）
- 2026-07-31｜CFO｜commitment：CFO 說會在九月投資人會議給第三季中期更新。（原話："provide a mid-quarter update at an investor conference"）
- 2026-07-31｜CFO｜margin：CFO 說座椅第二季營業利益率 6.7%，與去年持平。（原話："with adjusted operating margins of 6.7%"）
- 2026-07-31｜CFO｜margin：CFO 說 E-Systems 第二季調整後利益 9100 萬美元、利益率 5.8%（去年 4.9%）。（原話："Adjusted earnings were $91 million or 5.8%"）
- 2026-07-31｜CEO｜margin：CEO 說 E-Systems 第二季淨績效貢獻 155 bps。（原話："driven by a strong 155 basis points of net performance"）
- 2026-07-31｜CEO｜margin：CEO 說 E-Systems 上半年淨績效約 100 bps，已超過全年目標。（原話："having generated approximately 100 basis points"）
- 2026-07-31｜CFO｜margin：CFO 拆解上半年到下半年：銷貨減少約 6.64 億美元、下行轉換率 25%（1.67 億），並自承偏重。（原話："still a bit heavy at 25% or $167 million"）
- 2026-07-31｜CFO｜margin：CFO 說關稅退款使下半年營收較上半年多 1.9 億美元但無盈餘對應。（原話："you have $190 million higher revenue in the second half"）
- 2026-07-31｜CFO｜margin：CFO 說下半年展望含較上半年 55 bps 的淨營運績效改善。（原話："outlook with 55 basis points of improvement sequentially"）
- 2026-07-31｜CFO｜commitment：CFO 說今年座椅與 E-Systems 淨績效預計達成或超過 40 與 80 bps。（原話："meet or exceed the 40 and 80 basis points"）
- 2026-07-31｜CFO｜guidance：CFO 說明年座椅與 E-Systems 預期再各貢獻 40 與 80 bps 淨績效。（原話："we expect another 40 and 80 basis points in C and E-Systems"）
- 2026-07-31｜CFO｜margin：CFO 表示 E-Systems 利益率明年不太可能明顯改善，2027～2029 逐步改善。（原話："it's not likely in '27, but as you progress through that '27"）
- 2026-07-31｜CFO｜margin：CFO 對 E-Systems 現階段利益率表達不滿意。（原話："We're not happy with where margins are right now"）
- 2026-07-31｜CFO｜commitment：CFO 說公司計畫恢復提供三年 backlog，時點為第四季財報與 2027 初步財測。（原話："historical practice of providing a 3-year backlog"）
- 2026-07-31｜CFO｜customer：CFO 說客戶選商節奏已趨穩定，近似電動車急轉彎之前。（原話："has stabilized. It more closely resembles what we"）
- 2026-07-31｜CFO｜guidance：CFO 說 2029 年 backlog 很穩，可能優於 2027、2028。（原話："a very robust 2029 backlog, very likely better than"）
- 2026-07-31｜CFO｜guidance：CFO 重申 2026～2028 backlog 較年初合約改善 4 億美元，偏重 2028。（原話："our 2026 to '28 backlog had improved by $400 million"）
- 2026-07-31｜CFO｜guidance：CFO 說非核心電子產品退場今年少 9000 萬美元營收，明年少 2.35 億。（原話："$90 million of revenue that goes away this year"）
- 2026-07-31｜CFO｜guidance：CFO 在被問及 2027 時表示預期成長有限，即使 backlog 逾 7 億美元。（原話："we do expect limited growth in ' 27 despite the more than"）
- 2026-07-31｜CFO｜risk：CFO 預期 JLR、Ford Explorer、Jeep Grand Wagoneer 三個平台明年回落。（原話："we expect those 3 platforms to pull back a bit"）
- 2026-07-31｜CFO｜risk：CFO 引述通用說明年全尺寸卡車與 SUV 量大致持平。（原話："full-size truck and SUV volumes being sort of flat next year"）
- 2026-07-31｜CFO｜guidance：CFO 說 2028～2030 有機會回到高於市場 3～4 個百分點的成長。（原話："return to our historical growth above market profile"）
- 2026-07-31｜CFO｜guidance：CFO 說資本支出預期不會有明顯變化，今年約 2.8% 營收。（原話："We don't see a meaningful change in our CapEx footprint."）
- 2026-07-31｜CFO｜capital_allocation：CFO 說併購製造整合商使設備成本下降 20% 以上。（原話："We've reduced the cost of our equipment by 20% or"）
- 2026-07-31｜CEO｜capital_allocation：CEO 說全年買回目標上調至至少 3.5 億美元。（原話："year repurchase target to at least $350 million"）
- 2026-07-31｜CFO｜capital_allocation：CFO 說現有買回授權剩餘約 6 億美元，可買到 2026 年底。（原話："approximately $600 million remaining"）
- 2026-07-31｜CFO｜capital_allocation：CFO 說自 2011 年起以買回與股利返還超過 85% 自由現金流。（原話："returned over 85% of free cash flow to"）
- 2026-07-31｜CFO｜capital_allocation：CFO 說可用流動性 30 億美元。（原話："we have $3 billion of available liquidity"）
- 2026-07-31｜CFO｜risk：CFO 說上半年中國內需銷售下滑 20%，下半年假設弱勢持續。（原話："domestic sales in China, they're down 20%"）
- 2026-07-31｜CFO｜guidance：CFO 說若非中國疲弱，本次財測可能上調更多。（原話："have raised guidance a little bit more today"）
- 2026-07-31｜CFO｜risk：CFO 說財測區間低端是為防範伊朗衝突等引發的需求疲弱。（原話："the low end of the range is in place to protect against"）
- 2026-07-31｜CFO｜risk：CFO 提到伊朗衝突為北美與歐洲購車需求下行風險。（原話："stemming from the continued conflict in Iran"）
- 2026-07-31｜CFO｜guidance：CFO 說 301 與 122 條款關稅影響較先前假設少約 4000 萬美元，僅影響營收。（原話："301 tariffs and 122 tariffs were -- are about $40 million"）
- 2026-07-31｜CFO｜competition：CFO 說財測內已把傳統客戶讓給中國車廠的份額假設由約 1.5% 升至 3%。（原話："went from roughly 1.5% this year to 3%"）
- 2026-07-31｜CFO｜customer：CFO 說中國車廠占其新訂單近 20%，但占營收不到 10%。（原話："less than 10% of our revenue"）
- 2026-07-31｜CFO｜customer：CFO 說公司營收與中國車廠的比例將於 2027 達 50%（此句口徑為「revenue」，同場稍後問答改稱「China revenues」）。（原話："We're well on track to get to 50% of our revenue"）
- 2026-07-31｜CFO｜customer：CFO 說目前中國營收中 44% 來自中國車廠，明年 50% 以上。（原話："we're at 44% of our China revenues"）
- 2026-07-31｜CFO｜commitment：CFO 說對中國車廠成長以保護報酬為優先。（原話："but we're protecting returns"）
- 2026-07-31｜CFO｜competition：CFO 說出口導向的中國車廠專案占比偏低，短期是風險、長期可能是機會。（原話："we're a bit under-indexed on the export front"）
- 2026-07-31｜CEO｜customer：CEO 說今年累計新訂單約 29 億美元（座椅逾 23 億、E-Systems 逾 5 億）。（原話："approximately $2.9 billion of business awards year-to-date"）
- 2026-07-31｜CFO｜customer：CFO 說 Audi 訂單約為去年底最大 conquest 訂單的 75%，投產於 2028 年底。（原話："it's about 75% as large as our largest conquest award"）
- 2026-07-31｜CFO｜customer：CFO 說 Audi 專案 2028 年底起量產，2029～2030 爬坡。（原話："launches towards tail end of '28 and programs ramp up"）
- 2026-07-31｜CEO｜capital_allocation：CEO 說 Leapmotor 南美訂單不需大額投資。（原話："No, there's not major investment required."）
- 2026-07-31｜CEO｜commitment：CEO 說下半年預期還有更多好消息，待鎖定合約。（原話："more good news in the second half"）
- 2026-07-31｜CEO｜commitment：CEO 說今年 IDEA by Lear 節省目標 7500 萬美元。（原話："deliver $75 million in IDEA savings this year"）
- 2026-07-31｜CEO｜commitment：CEO 說重組節省上半年已達 5000 萬美元，全年目標 8000 萬。（原話："we have generated $50 million in savings"）
- 2026-07-31｜CEO｜product：CEO 稱自動化與數位工具使公司領先同業數年。（原話："positioning Lear years ahead of our competition"）

### 問答異常語氣（迴避／改口／保留）
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Dan Levy 問 E-Systems 8% 利益率路徑（先前說與量相關）是否還成立、淨績效能否壓過量價組合。｜答法：CFO 回答未提 8%，改談 2027～2029 backlog、40/80 bps 淨績效，並說 E-Systems 利益率明年不太可能明顯改善。
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Joe Spak 問先前財測上下各 4 億美元緩衝，如今低端上調後剩多少緩衝。｜答法：CFO 說明高低端情境（中國政策、北美卡車、伊朗衝突），未給剩餘緩衝金額。
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Itay Michaeli 問下半年財測中中國內需與產量假設的量化程度。｜答法：CFO 說沒有具體數字可提供，改給份額轉移假設與新訂單比重。
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Colin Langan 問第三季至第四季利益率走勢。｜答法：CFO 先說不提供按季精確財測，隨後仍給第三季營收與兩部門利益率區間，並說商業談判是最大變數。
- LEA_Q2_2026_Earnings_Call_20260731.md｜問：Emmanuel Rosner 問 2027 營收成長是否被下修，以及 Audi 訂單規模。｜答法：CFO 確認 2027 成長有限（與前文偏重 backlog 的說法相比語氣轉保留）；Audi 規模拒給確切數字，只說約最大 conquest 訂單的 75%。

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
{"date":"20260524","verdict":"B 觀望偏進場（衛星，等回測）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Seating margin 結構性回升至 7.0%+（vs Q2 25 6.4%）","columns":{"2Y":"FY27 Seating margin ≥ 7.0%","5Y":"FY29 Seating margin ≥ 7.5%","10Y":"FY35 維持 7%+","具體門檻":"FY26 全年 ≥ 6.8%；FY27 ≥ 7.0%","來源":"Q1 2026 8-K + 法說會","漂移觸發":"連 2 季 &lt; 6.5% → 削弱"}},{"id":"H2","text":"E-Systems 段占比擴張至 28%+ + 持續 .0B+ 新 awards/年","columns":{"2Y":"FY27 E-Sys 占比 ≥ 27%","5Y":"FY29 ≥ 30%","10Y":"FY35 ≥ 35%","具體門檻":"FY26 E-Sys Rev ≥ .2B；FY26 全年 awards ≥ .0B","來源":"2025 awards 公告 .4B","漂移觸發":"FY27 全年 awards &lt; .8B → 削弱"}},{"id":"H3","text":"市場估值倍數均值回歸至 11-12x（vs 5Y 均 25.95x 折讓 55%）","columns":{"2Y":"Fwd PE 24 月內 ≥ 11x","5Y":"5Y 內 PE 至少觸及 14x","10Y":"10Y 區間 8-22x","具體門檻":"Fwd PE 24 月內 ≥ 11x","來源":"Macrotrends 5Y PE 數據","漂移觸發":"連 2 季維持 &lt; 9x → 結構性 de-rating"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"GM 罷工或 production miss（GM 占 LEA 22%）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"UAW 2027 談判進度、GM Q-on-Q production","警戒閾值":"單季 Seating margin &lt; 5.5% 或 GM production -10% 連 2 季"}},{"id":"R2","text":"Seating 段 commoditization 持續（BWA / Adient / 中國 Yanfeng 壓價）","columns":{"對應假設":"H1 + H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Seating margin 季度走勢；新 awards 流向","警戒閾值":"Seating margin 連 4 季 &lt; 6.0% → 大動作"}},{"id":"R3","text":"OEM in-source + 中國新勢力擠壓 → 全球市佔結構性流失","columns":{"對應假設":"H1 + H2 + H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"LEA organic growth vs LVP；新 awards 量","警戒閾值":"連 8 季 organic growth underperform LVP &gt; 200bps"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":139.8,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEA_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
