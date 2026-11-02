你是 stock-analyst **v20 判斷 agent**，標的 GLW（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GLW","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLW_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLW_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_net_sales","label":"GAAP net sales","value":4855,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99，2026-10-27，IR 檔 s203.q4cdn.com/212458750） https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm"}},{"id":"f_kpi1_core_sales","label":"Core sales","value":5081,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99，2026-10-27，IR 檔 s203.q4cdn.com/212458750） https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm"}},{"id":"f_kpi2_core_non_gaap_operating_","label":"Core（non-GAAP）operating income / margin","value":22.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99，2026-10-27，IR 檔 s203.q4cdn.com/212458750） https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm"}},{"id":"f_kpi3_gaap_operating_income_ma","label":"GAAP operating income / margin","value":18.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99，2026-10-27，IR 檔 s203.q4cdn.com/212458750） https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm"}},{"id":"f_kpi4_adjusted_free_cash_flow","label":"Adjusted free cash flow","value":661,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99，2026-10-27，IR 檔 s203.q4cdn.com/212458750） https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm"}},{"id":"f_kpi6_q4_2026_guidance_core_sa","label":"Q4 2026 guidance：core sales","value":"5200～5300","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99，2026-10-27，IR 檔 s203.q4cdn.com/212458750） https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm"}},{"id":"f_kpi7_q4_2026_guidance_core_ep","label":"Q4 2026 guidance：core EPS","value":"0.96～1.0","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99，2026-10-27，IR 檔 s203.q4cdn.com/212458750） https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_glw_gross_margin_pct","label":"GLW 毛利率","value":36.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_glw_operating_margin_pct","label":"GLW 營業利益率","value":15.62,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_glw_fcf_margin_pct","label":"GLW FCF 利潤率","value":15.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_cohr_gross_margin_pct","label":"COHR 毛利率","value":37.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohr_operating_margin_pct","label":"COHR 營業利益率","value":12.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cohr_fcf_margin_pct","label":"COHR FCF 利潤率","value":-14.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lite_gross_margin_pct","label":"LITE 毛利率","value":41.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lite_operating_margin_pct","label":"LITE 營業利益率","value":17.79,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lite_fcf_margin_pct","label":"LITE FCF 利潤率","value":9.96,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_aph_gross_margin_pct","label":"APH 毛利率","value":37.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aph_operating_margin_pct","label":"APH 營業利益率","value":26.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aph_fcf_margin_pct","label":"APH FCF 利潤率","value":17.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":5.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司 Q3 2026 新聞稿（8-K Ex.99，2026-10-27，IR 檔 s203.q4cdn.com/212458750） https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":126.9,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-20.4,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":39.71,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.38 → 3.38）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.52 → 4.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.12 → 6.12）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":3.38,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":4.52,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":6.12,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":3.36,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 3.27 → 3.38（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":51.38,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝51.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":51.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.17,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.54,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":37.54,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 3.38，分子＝快照價 126.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.883,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":6634.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 9171.0、現金 2537.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":861.4,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":115945.8,"period":"2026-11-03","unit":"USD m","basis":"市值 109311.8 ＋ 淨負債 6634.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":19426.03,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":23533.86,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.97,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 125.18 / W52 141.52 / W104 98.66 / W250 59.96 / W250 13週斜率 2.55%"},{"id":"f_ma_w52","label":"52 週均線","value":141.52,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":98.66,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":59.96,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.55,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出光通訊主要競爭者為 Amphenol、Fujikura、Sumitomo、Prysmian；公司稱維持領導地位，但承認競爭格局含整併與價格壓力，且不保證能維持或提升市占。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"We maintain a leadership position in the segment’s principal product groups, which include carrier and enterprise networks. The competitive landscape includes industry consolidation, pricing pressure and competition for the innovation of new products. These competitive conditions are likely to persist.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：光通訊與顯示器貢獻大量利潤，價格、數量或市占的顯著下滑會對財務造成重大負面影響。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"Corning’s Optical Communications and Display segments generate a significant amount of the Company’s profits and cash flow; any significant decrease in pricing, volume or market share could have a material and negative impact on our financial results","as_of":"2026-02-12","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Corning 2026 年簽下 Meta（最高 $6B）、Nvidia（最高 $3.2B）、Amazon 光纖長約，顯示超大規模客戶綁定。","source":"Nasdaq - GLW Rides on Solid Traction in Optical Communication","url":"https://www.nasdaq.com/articles/glw-rides-solid-traction-optical-communication-will-it-sustain","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：少數終端客戶占各事業部淨銷售高比例，客戶流失或客戶擁有議價優勢為風險；未提及具體第二供應商或自製事件。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"A relatively small number of end customers account for a high percentage of our net sales in each of our business segments.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Zacks 報導：2025 年三家終端客戶占 Display Technology 淨銷售 59%、三家客戶占 Automotive 61%、兩家客戶占 Specialty Materials 43%（搜尋摘要轉述，未讀原頁）。","source":"Zacks/Nasdaq: Corning Stock Rises 60.6% in 3 Months: How to Play the Stock","url":"https://www.nasdaq.com/articles/corning-stock-rises-606-3-months-how-play-stock","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未發現 Moody's/S&P/Fitch 對 Corning 的信用評等調降；僅見分析師評等調降（JPMorgan 2026-04-16 降至 Neutral，屬估值理由）。","source":"Akros catalyst event: JPMorgan GLW","url":"https://akrostec.com/indices/AUT100/events/2026-04-16t00-00-00z-corning-inc-glw-other-08efbadd","excerpt":null,"as_of":"2026-04-16","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce：光纖供給缺口延續至至少2028；2026年產能利用率92%，庫存由2024年4個月降至1個月；新預製棒產能需18–24個月","source":"TrendForce press center, Optical Fiber Spot Prices Surge Severalfold in 2026","url":"https://www.trendforce.com/presscenter/news/20261019-13275.html","excerpt":"global optical fiber capacity utilization has climbed to 92% in 2026, while inventory levels have fallen from four months in 2024 to just one month","as_of":"2026-10-19","retrieved_at":"20261103","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TrendForce：資料中心占光纖需求比重由2026年約18–20%升至2027年30–35%","source":"TrendForce press center","url":"https://www.trendforce.com/presscenter/news/20261019-13275.html","excerpt":"Global optical fiber demand is estimated to reach 577 million fiber-kilometers in 2026, driven primarily by data center construction, which accounts for roughly 18–20% of the total. That share is projected to rise to 30–35% in 2027.","as_of":"2026-10-19","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Verizon與Corning 2026年9月簽多年供貨協議，涵蓋1.29億光纖公里、2027–2032交付","source":"TrendForce press center (via search summary)","url":"https://www.trendforce.com/presscenter/news/20261019-13275.html","excerpt":"In September 2026, Verizon and Corning signed a multi-year supply agreement covering 129 million fiber-kilometers","as_of":"2026-10-19","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Corning稱已與客戶敲定類似Meta約60億美元的長期產能保留協議，財務影響2027起、2028逐步放大（隨新產能上線）","source":"Converge Digest, Corning Jan 2026 earnings coverage","url":"https://convergedigest.com/?p=108381","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"管理層稱全球光纖整體夠用，但最新高密度光纖/纜/連接產品緊缺","source":"Fintool Corning Springboard upgrade Meta deal","url":"https://fintool.com/news/corning-springboard-upgrade-meta-deal","excerpt":null,"as_of":"2026-01-28","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：管理層認為訴訟對財務的重大不利影響可能性極低；法律程序僅列環境訴訟（20 個超級基金場址，應計約 $89M），未列反壟斷案。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"In the opinion of management, the likelihood that the ultimate disposition of these matters will have a material adverse effect on the Company’s consolidated financial position, liquidity, or results of operations, is remote.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因子指出公司可能受 FTC 等監管，並可能被調查；社會對經濟權力集中的關注可能帶來更多反競爭立法與執法。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"Growing public concern over concentration of economic power in corporations is likely to result in increased anti‐competition legislation, regulation, administrative rule making and enforcement activity.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"歐盟執委會 2024 年對 Corning 手機蓋板玻璃獨家供應協議展開調查，2025 年 7 月接受其放棄獨家條款的承諾而結案、無罰款；承諾期 9 年並有受託人監督；Apple 協議不在範圍內。2026 年 2 月 MLex 報導執委會發布相關和解決定摘要版。搜尋未見 2026 年 DOJ/FTC 對 Corning 的調查。","source":"搜尋摘要彙整（Law360/MLex、Bloomberg Law、9to5mac 等標題）","url":"https://news.bloomberglaw.com/antitrust/corning-dodges-eu-antitrust-clash-with-gorilla-glass-deal","excerpt":null,"as_of":"2025-07-18","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"EU 執委會接受 Corning 承諾、免罰款結案","source":"9to5mac","url":"https://9to5mac.com/2025/07/19/apple-exempt-from-cornings-eu-antitrust-probe-deal/","excerpt":"Glass Ceramics were included in the commitments because this cover material is likely to be used more extensively in the future by OEMs. But the commitments would not apply to Corning’s agreements with Apple given that the Commission found that the cover glass products developed by Corning for Apple are not part of the relevant market. To waive all exclusive dealing clauses in all its current","as_of":"2025-07-19","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 揭露：部分關鍵原料為單一或少數供應商，且部分原料受原產國出口限制，可能造成出貨延遲或毛利下降。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"Additionally, some required raw materials are subject to export restrictions imposed by their country of origin.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因子：全球營運受 CBP、BIS、OFAC 等進出口法規約束，更高關稅或新貿易障礙、反傾銷等可能對業務與財務造成負面影響。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"The implementation of more restrictive trade policies, such as higher tariffs or new barriers to entry, together with anti-dumping claims, duties, slowed regulatory approvals and other restrictions, in countries in which we import raw materials and components or sell large quantities of products and services could negatively impact our business, results of operations and financial condition.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Corning Q3 2026 新聞稿：美國 Section 232 行動改善美製太陽能產品的價格環境與需求。","source":"Corning 8-K Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm","excerpt":"•Solar grew sales 37% year over year, as production continued to ramp, albeit at a slower pace than anticipated. As productivity continues to improve, so will output and profitability. Additionally, in Q3, U.S. trade action under Section 232 of the Trade Expansion Act of 1962 improves the overall pricing environment","as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"CEO Weeks 稱約 90% 營收來自美國內、僅約 1% 美國銷售來自中國工廠，關稅暴露有限。","source":"24/7 Wall St，Corning's Tariff Immunity Comes Down to One Strategic Choice","url":"https://247wallst.com/investing/2026/08/17/cornings-tariff-immunity-comes-down-to-one-strategic-choice-ceo-says/","excerpt":"So tariffs, because of our fundamental philosophy and our values tend not to have a significant impact on us.” Those two figures, attributed to Weeks on the broadcast rather than to a formal company disclosure, are the spine of the case. If 90% of what Corning sells into the United States is made in there, and only 1% of U.S. sales originate from Chinese factories, the surface","as_of":"2026-08-17","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國商務部對美國單模光纖課反規避關稅，Corning 適用 37.9%，至 2028-04-21。","source":"Bloomberg Law，China Hits US Optical Fiber Imports With Anti-Dumping Duties","url":"https://news.bloomberglaw.com/international-trade/china-hits-us-optical-fiber-imports-with-anti-dumping-tariffs","excerpt":"The duties, ranging from 33.3% to 78.2%, took effect Thursday Beijing time on “certain cut-off shifted single-mode optical fiber” from the US, according to a statement from the Chinese Ministry of Commerce. Among the companies subject to the new duties, Corning Inc. now faces a 37.9% levy, OFS Fitel LLC is at 33.3% and Draka Communications Americas Inc.","as_of":"2025-09-04","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"第三方彙整（policyrisk.com，非官方文件）稱 Corning 顯示玻璃製造集中於中國、南韓、台灣；光纖業務分布於中國、印度、波蘭、墨西哥、德國；部分關鍵原料與專有設備為單一來源或少數供應商。","source":"policyrisk.com GLW company page（摘要 Corning SEC 文件）","url":"https://policyrisk.com/world/company/GLW","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2026 年 8 月 CEO Weeks 稱關稅影響微乎其微，歸因於工廠靠近客戶的佈局；在美國銷售的產品僅 1% 在中國製造。","source":"247wallst: Corning's Tariff Immunity Comes Down to One Strategic Choice, CEO Says","url":"https://247wallst.com/investing/2026/08/17/cornings-tariff-immunity-comes-down-to-one-strategic-choice-ceo-says/","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Q1 2025 財報電話會：中國銷售 80% 在中國製造或在保稅區加工，15% 在區域內（韓國、台灣）製造。","source":"Insider Monkey Corning Q1 2025 earnings call transcript","url":"https://www.insidermonkey.com/blog/corning-incorporated-nyseglw-q1-2025-earnings-call-transcript-1520936/","excerpt":null,"as_of":"2025-04-29","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Optical Communications net sales $2,379M, +44% YoY, +15% QoQ; segment net income $532M","source":"Corning 8-K Ex.99 Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026 Glass Innovations (merged Display + Specialty Materials) net sales $1,506M, +3% QoQ, -3% YoY","source":"Corning 8-K Ex.99 Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000024741/000002474126000273/glw-20261027xex99xq32026.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q4 2026 guidance: core sales about +19% YoY to $5.2-5.3B; core EPS $0.96-1.00","source":"Corning Q3 2026 release via Business Wire/finviz","url":"https://finviz.com/news/408572/corning-delivers-outstanding-third-quarter-results1","excerpt":"quarter, we expect to grow core sales approximately 19% year over year to a range of $5.2 billion to $5.3 billion and grow core EPS approximately 36% year over year to a range of $0.96 to $1.00.","as_of":"2026-10-27","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Corning expects handheld-market unit volumes down mid-teens % in 2026 due to memory prices; Q1 2026 Optical +36% YoY driven by GenAI, hyperscaler LTAs, pricing and mix; 19% sales CAGR targeted Q4 2026-Q4 2030","source":"Nasdaq: Corning Q2 earnings call highlights / search summaries","url":"https://www.nasdaq.com/articles/corning-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261103","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Counterpoint Research report titled 'Corning Raising Display Glass Prices in Q4 2026' (only title seen)","source":"Counterpoint Research","url":"https://counterpointresearch.com/en/reports/corning-raising-display-glass-prices","excerpt":null,"as_of":"2026-10-07","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Corning's FY2025 10-K risk factors state that if its products or technologies become obsolete or disrupted by emerging technologies, revenue and operating margins could be negatively impacted in both near and long term.","source":"SEC EDGAR 10-K FY2025, Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"if our products or technologies become obsolete or disrupted by emerging technologies, it could negatively impact our revenue and operating margins for both near- and long-term.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Hollow-core fiber is an emerging alternative to solid-glass fiber; early deployments are short-haul, high-value routes; competitors beyond Corning exist.","source":"STL, Hollow Core Fiber: The Next Frontier in Ultra-Low-Latency Optical Networks","url":"https://stl.tech/2026/03/","excerpt":"Hollow Core Fiber: The Next Frontier in Ultra-Low-Latency Optical Networks For years, fiber-optic innovation focused on sending more data through glass.","as_of":"2026-03-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Corning research VP says move from copper to fiber in AI back-end networks is inevitable; CPO is central to this shift (Corning positioned as beneficiary).","source":"Fierce Network, Corning wants to cut copper out of the data center","url":"https://www.fierce-network.com/broadband/corning-sees-opportunities-convert-copper-data-center","excerpt":"copper Plenty of copper wiring lurks in the data center, and Corning sees a ripe opportunity to replace it with optical fibers. (Art by Midjourney for Fierce Network) Corning wants to replace the copper cables in data center servers to optical fiber Data centers use a ton of copper for various purposes, which is poised to push their power constraints to the limit Corning said co-packaged optics","as_of":"2025-03-18","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Cignal AI expects CPO deployments to start in 2026 with large-scale deployment in three to five years.","source":"Lightwave, Co-packaged optics deployments will start in 2026, says Cignal AI","url":"https://lightwaveonline.com/home/article/55276162/co-packaged-optics-deployments-will-start-in-2026-says-cignal-ai","excerpt":"Co-packaged optics deployments will start in 2026, says Cignal AI The research firm notes hyperscalers will conduct early deployments. Sean Buckley March 20, 2025","as_of":"2025-03-20","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"10-K 載明 Life Sciences 面臨大型經銷商向後整合或推出自有品牌產品的競爭（通路端競爭壓力的書面揭露）；搜尋未見 2026 年訂閱化、D2C 或平台化的通路結構轉變報導。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"Corning also faces competition from large distributors that have pursued backward integration or introduced private label products.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Walnut Invest 2026年8月資料：15位分析師平均目標價$193.40，區間$129–$226","source":"Walnut Invest GLW forecast","url":"https://walnutinvest.com/stocks/glw/forecast","excerpt":"15 analysts covering Corning (GLW) carry an average price target of $193.40 as of August 2026; Target range $129.00 to $226.00","as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Tickflow（資料截至2026-08-01）：30位分析師共識目標價$175.33，評級Buy","source":"Tickflow GLW forecast","url":"https://www.tickflow.io/stock/GLW/forecast","excerpt":"The consensus among 30 analysts covering Corning Inc (GLW) is Buy with an average price target of $175.33.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Investing.com：12個月平均目標價197.67美元，高230、低149","source":"Investing.com Corning","url":"https://uk.investing.com/equities/corning-inc","excerpt":"The average 12-month price target for Corning is 197.67 USD, with a high estimate of 230 USD and a low estimate of 149 USD.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Corning 2026-07-28 給 Q3 指引：核心營收$4.9–5.0B、核心EPS $0.85–0.89；EPS區間高於共識$0.85","source":"MarketBeat / 搜尋彙整","url":"https://www.marketbeat.com/instant-alerts/corning-nyseglw-issues-q3-2026-earnings-guidance-2026-07-28/","excerpt":"Corning's Q3 2026 guidance for core sales of US$4.9–5.0 billion and core EPS of US$0.85–0.89","as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 營收$4.74B、核心EPS $0.78，高於共識（EPS $0.76、營收$4.63B）","source":"搜尋彙整（Q2 2026結果）","url":"https://www.barchart.com/story/news/3518670/glw-q2-deep-dive-optical-growth-photonics-ambitions-and-guidance-miss-drive-market-reaction","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Seeking Alpha 修正頁：EPS下修4次、營收上修7次/下修2次（期間未標）","source":"Seeking Alpha GLW revisions","url":"https://seekingalpha.com/symbol/GLW/earnings/revisions","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-09-11 Corning與Goldman Sachs簽訂Equity Distribution Agreement，ATM增資計畫總額最多20億美元，所得用於一般企業用途（非併購、訴訟或監管事件，屬資本市場事件）","source":"SEC EDGAR 8-K Item 8.01 (2026-09-11)","url":"https://www.sec.gov/Archives/edgar/data/24741/000119312526389321/d154232d8k.htm","excerpt":"On September 11, 2026, Corning Incorporated (the “Company”) entered into an Equity Distribution Agreement (the “Equity Distribution Agreement”) with Goldman Sachs & Co. LLC (“Goldman Sachs”) to sell shares of the Company’s common stock, par value $0.50 per share (the “Common Stock”), having an aggregate offering price of up to $2,000,000,000","as_of":"2026-09-11","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3：管理層認為未決訴訟對財務重大不利影響的可能性極低；環境訴訟方面被指定為20處危險廢棄物場址的潛在責任方，應計約8,900萬美元","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"In the opinion of management, the likelihood that the ultimate disposition of these matters will have a material adverse effect on the Company’s consolidated financial position, liquidity, or results of operations, is remote.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"FY2025 10-K Legal Proceedings：未提及近期集體訴訟；管理層認為重大不利影響可能性極低；環境訴訟應計約8,900萬美元","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/24741/000002474126000124/glw-20251231.htm","excerpt":"In the opinion of management, the likelihood that the ultimate disposition of these matters will have a material adverse effect on the Company’s consolidated financial position, liquidity, or results of operations, is remote.","as_of":"2026-02-12","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月11份8-K中僅1份含重大項目（為8.01 ATM），清單無Item 4.02（財報不可信賴）項目；搜尋亦未見SEC調查，唯一重編為2006年舊事","source":"SEC EDGAR 8-K 申報清單（2025-11-03至2026-11-03）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000024741&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GLW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.16,"operating_margin_pct":15.62,"fcf_margin_pct":15.12,"rd_intensity_pct":6.69},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLW","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"COHR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.5,"operating_margin_pct":12.67,"fcf_margin_pct":-14.48,"rd_intensity_pct":10.16},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COHR","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"LITE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":41.67,"operating_margin_pct":17.79,"fcf_margin_pct":9.96,"rd_intensity_pct":11.83},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LITE","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"5201.T","period":"TTM ending 2026-03-31（2季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.5201.T","as_of":"TTM ending 2026-03-31（2季加總）"},"note":"Total Revenue 缺失，無法算利潤率；僅 2 季可得，非完整 TTM"},{"name":"APH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.63,"operating_margin_pct":26.77,"fcf_margin_pct":17.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APH","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"GLW"},"financial_history":{"ticker":"GLW","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":14189000000.0,"revenue_yoy_pct":null,"gross_margin_pct":31.76,"operating_margin_pct":10.13,"net_income":1316000000.0,"diluted_eps":1.54,"free_cash_flow":1011000000.0,"fcf_margin_pct":7.13,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":12588000000.0,"revenue_yoy_pct":-11.28,"gross_margin_pct":31.23,"operating_margin_pct":7.07,"net_income":581000000.0,"diluted_eps":0.68,"free_cash_flow":615000000.0,"fcf_margin_pct":4.89,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":13118000000.0,"revenue_yoy_pct":4.21,"gross_margin_pct":32.6,"operating_margin_pct":8.65,"net_income":506000000.0,"diluted_eps":0.58,"free_cash_flow":974000000.0,"fcf_margin_pct":7.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":15629000000.0,"revenue_yoy_pct":19.14,"gross_margin_pct":35.97,"operating_margin_pct":14.58,"net_income":1596000000.0,"diluted_eps":1.83,"free_cash_flow":1413000000.0,"fcf_margin_pct":9.04,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GLW/GLW_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**Corning Incorporated** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Ladies and gentlemen, thank you for standing by. Welcome to the Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please be advised that today's conference is being recorded. I would like now to turn the conference over to Chris Keenan, Director of Investor Relations. Please go ahead.

**Christopher Keenan** (Executives):
Thank you, and good morning. Welcome to Corning's Third Quarter 2026 Earnings Call. With me today are Wendell Weeks, Chairman, Chief Executive Officer and President; and Ed Schlesinger, Executive Vice President and Chief Financial Officer. I'd like to remind you that today's remarks contain forward-looking statements that fall within the meaning of the Private Securities Litigation Reform Act of 1995. These statements involve risks, uncertainties and other factors that could cause actual results to differ materially. These factors are detailed in the company's financial reports. You should also note that we will be discussing our consolidated results using core performance measures unless we specifically indicate our comments relate to GAAP data. 
Our core performance measures are non-GAAP measures used by management to analyze the business. For the third quarter, the difference between GAAP and core EPS principally reflects adjustments for hedged exposures, along with discrete tax items. A reconciliation of core results to the comparable GAAP value can be found in the Investor Relations section of our website at corning.com. You may also access core results on our website with downloadable financials in the Interactive Analyst Center. Supporting slides are being shown live on our webcast, and we encourage you to follow along. They are also available on our website for downloading. And with that, I'll turn the call over to Wendell.

**Wendell Weeks** (Executives):
Thank you, Chris, and good morning, everyone. Today, we announced outstanding third quarter results. Year-over-year, we grew sales 19% to $5.1 billion and grew EPS significantly faster at 36% to $0.91, both exceeding guidance. We expanded gross margin 150 basis points to 40.5%. We increased operating margin 310 basis points to 22.7%, and we improved ROIC 330 basis points to 16.7%, all while delivering $661 million of free cash flow after investing over $0.5 billion in capacity to support future growth. Overall, a great quarter. And we expect our strong performance to continue. For the fourth quarter, we expect to grow sales about 19% year-over-year to a range of $5.2 billion to $5.3 billion and to grow EPS by about 36% year-over-year to a range of $0.96 to $1. 
So let's put our very strong results and outlook in the context of our Springboard journey. In May of this year, we upgraded and extended our Springboard plan to grow our annualized sales run rate to $20 billion by the end of 2026, $30 billion by the end of 2028 and $40 billion by the end of 2030. We shared that we are entering a new phase of accelerating growth. We plan for our compound annual growth rate to increase to 19% beginning in 2027 through 2030 after already growing at a robust 15% CAGR for the first 3 years of Springboard. That is a 400 basis point acceleration. In the third quarter, we already began to grow 19% year-over-year to $5.1 billion. That is an annualized run rate of $20.3 billion. And looking ahead to quarter 4, if you take the midpoint of our guidance, we'll grow 19% again to $5.25 billion. That is an annualized run rate of $21 billion. 
So just one quarter after upgrading our plan, we are exceeding our Springboard target of a $20 billion run rate by the end of 2026. And we are already demonstrating the accelerated growth rate anticipated for the next phase of our plan. Interestingly, today's earnings call actually marks the 3-year anniversary of when we introduced Springboard to all of you. So let's briefly look back on our journey and review what we've accomplished together. In the first 3 years of Springboard, from our starting point through quarter 4 2026, we will grow sales 60% and grow EPS much faster at over 150%. And along the way, we are significantly enhancing our financial profile, nearly doubling ROIC and more than tripling full year free cash flow. Altogether, we've established a strong launch point for the next phase of Springboard. 
Looking ahead, we plan to double sales from $20 billion to $40 billion, grow EPS significantly faster than sales, expand ROIC, all while delivering robust free cash flow even as we continue to invest to capture growth. So if you like the first phase of Springboard, you're going to love the next one. Importantly, we already have many of the critical customer relationships and long-term agreements in place that underpin our growth outlook. Now each relationship is unique, but they do have 2 common characteristics. The first is a focus on technology and co-innovation. We share our technology and development plans with each other. This allows us to help our customers achieve their vision. Secondly, we seek to appropriately share risks and rewards as we deliver that vision. 
Our customers are counting on us to provide the right products at the right time. So we take on the nontrivial responsibility of meeting challenging performance standards and production ramps. They take on the responsibility for how much of our products that they need because, of course, they are best positioned to make that determination. We use multiple mechanisms to achieve the appropriate balance of mutual obligations depending on the unique circumstances of our customers and their requirements of us. One example of a tool that we have used successfully in our glass and solar businesses and have now applied in Optical Communications is to have our customers provide upfront cash to fund our capacity. We then simply return the cash to our customers as they purchase the committed volume. This helps to both derisk our capacity investments and give our customers supply chain assurance. 
You can see this dynamic already at work in our financials. In the first phase of Springboard, we more than tripled our full year free cash flow while investing strongly in new capacity. Looking ahead to the new Springboard phase of accelerating growth, we are seeking to continue to increase free cash flow and improve our financial profile even as we invest to double the size of the company. Ed will share more color on this in a few minutes. We feel blessed to have these types of foundational relationships with our customers. They extend from our long-standing model of invent, make and serve. This fundamental approach has governed us for 175 years and will continue to guide us well into the future. We invest in innovation to invent products that enable transformative technologies. 
We create and build manufacturing platforms to deliver higher quality and lower cost than anyone else in the world, all to serve our customers over decades-long relationships. When we get this right, our customers become enduring partners, giving us the opportunity to solve their challenges and help create their own extraordinary products that delight their customers in turn. So after 175 years, we are once again in a moment where we have the opportunity to apply our long-standing principled approach to value creation for our customers, for our people, for our communities and importantly, for our shareholders. We are delighted to have you with us on that journey. Ed?

**Edward Schlesinger** (Executives):
Thank you, Wendell. Good morning, everyone. We delivered an outstanding third quarter, and our results demonstrate the acceleration of growth outlined in our 20-30-40 Springboard Plan. Year-over-year in Q3, sales grew 19% to $5.1 billion and EPS increased 36% to $0.91, both above our guided ranges. We expanded gross margin 150 basis points to 40.5%. Operating margin grew 310 basis points to 22.7%. ROIC grew 330 basis points to 16.7%, and we delivered strong free cash flow of $661 million even as we continue to invest to capture robust demand. Now moving to our segments. Our results were led by Optical Communications. Sales were $2.4 billion, up 44% year-over-year. Net income was $532 million, up 80% year-over-year, with the segment again delivering record profitability. 
Enterprise grew sales 84% year-over-year with Gen AI product sales growing more than 100% year-over-year, significantly outpacing GPU unit growth. This was driven by the rapid and broader adoption of our innovations and enabled by our steady capacity additions. At the launch of Springboard, our enterprise sales run rate was $1.4 billion. Since that time, we've quadrupled enterprise sales to a $6 billion run rate. And keep in mind, our growth is driven by scale-out. As Optical penetrates the scale-up portion of the network, our revenue opportunity will increase dramatically. In Carrier, sales grew 4% year-over-year, driven by growth in data center interconnect. During the quarter, we announced long-term customer agreements with Zayo, Verizon and AT&T to deliver fiber and connectivity solutions in support of their network expansions across broadband and data center interconnect. 
Collectively, these agreements serve as an excellent proof point for our long-term opportunity in Carrier and give us confidence that our opportunity in DCI is bigger than the $1 billion target we've previously communicated. Moving to Glass Innovations. The successful execution of our More Corning strategy helped us outperform our end markets, which were significantly impacted by memory prices. Looking at the market in the third quarter, TV units were down 4%, while notebooks and handhelds were down about 20%. Our third quarter sales were $1.5 billion, down $54 million or 3% year-over-year. Net income was $328 million, down 10% year-over-year. Looking ahead, we expect to continue executing our More Corning strategy. For example, we continue advancing our nearly 20-year partnership with Apple. By the end of 2026, all of the cover glass for iPhone, including iPhone Duo and Apple Watch sold worldwide will be produced at our Harrodsburg, Kentucky facility. 
Additionally, we recently announced a price adjustment for our display glass substrates that will begin to take effect in the fourth quarter to address a weaker yen environment and rising costs such as critical materials and energy. In automotive, our sales were up 4% year-over-year. Recovery in North American Class 8 truck market more than offset the impact from the light-duty vehicle market, which was down 3%. Net income of $67 million was down 1% year-over-year. Looking ahead, we remain focused on our More Corning content strategy. In Solar, Q3 sales were $436 million, up $117 million or 37% year-over-year. The segment reported a net loss of $7 million. 
We continue to ramp production at our wafer and module facilities, albeit at a slower pace than anticipated. As our productivity improves, so will our output and profitability. Demand remains strong and the market preference for U.S.-made solar products continues to strengthen. Recent U.S. trade action under Section 232 of the Trade Expansion Act of 1962 improves the overall pricing environment and demand for Corning's solar products. Overall, we are making solid progress building a more than $3 billion revenue stream in Solar with profitability above the corporate average. 
Sales in Life Sciences and Emerging Growth businesses were up 1% year-over-year as our Life Sciences business outperformed the end market. Net income was down $13 million year-over-year due to investments in emerging growth programs. Shifting to our outlook. In the fourth quarter, we expect sales to grow approximately 19% year-over-year to a range of $5.2 billion to $5.3 billion and EPS to grow approximately 36% year-over-year to a range of $0.96 to $1. As we move to our next phase of Springboard, we have a really compelling opportunity in front of us. We plan to double the size of the company from $20 billion to $40 billion by the end of 2030. We grow organically by inventing products that enable transformative technologies, and we create and build manufacturing platforms to deliver higher quality and lower costs than anyone else in the world. 
Historically, this meant we invest capital upfront before the revenue and free cash flow shows up. And then we have high returns and generate strong free cash flow down the road. We have been steadily improving that model by appropriately sharing the risk and responsibility of investments with our customers. Many such long-term customer agreements underpin our growth. We use multiple mechanisms in our agreements to achieve the appropriate balance of mutual obligations depending upon unique circumstances of our customers and their requirements of us. One tool we use is for our customers to provide the cash upfront, and then we return that cash as they purchase the committed volume. 
We have successfully used this tool in our Glass and Solar businesses and are now applying it in Optical Communications. This both provides our customers with supply chain certainty while securing our revenue, returns and free cash flow. You can see this dynamic already at work in our financials. There is a line in our operating cash flow labeled customer deposits. For the first 9 months of the year, that amount was $639 million. This line includes upfront cash we receive from our customers during the period, net of the cash returned to customers from previous deposits as they purchase their committed volumes. At a macro level, this mechanism smooths the cash impact of our capacity additions, helping fund the upfront investment and then returning customer deposits from the operating cash flow generated by our profitable delivery of the committed volume. 
You can already see this in effect in our cash flows. We generated $2.3 billion of free cash flow over the first 9 months of this year, while we steadily invested $1.3 billion in CapEx to add capacity supporting the growth outlined in Springboard. As we've previously shared, in 2026, we're planning to invest approximately $2 billion in CapEx, primarily to support the growth in Optical Communications. We plan to keep this flywheel going as we enter our new accelerating growth phase of Springboard. We seek to continue to increase free cash flow and further improve our financial profile even as we invest to double the size of the company. Given our increasing free cash flow, this takes us to capital allocation. Our philosophy is to prioritize investing in organic growth opportunities that drive significant returns. Our shareholders have validated that this creates the most value for them, and this remains a priority. 
We will continue to maintain a strong and efficient balance sheet, and we're in great shape. We have one of the longest debt tenors in the S&P 500. Our current average debt maturity is more than 20 years, and we have no significant debt maturity coming due in any given year. We also expect to continue our strong track record of returning excess cash to shareholders. We already have a strong dividend, and therefore, as we go forward, our primary vehicle for returning cash to shareholders will be share buybacks. Now before we move to Q&A, let me reiterate my key takeaways. We've had great success to date with Springboard. We delivered significant growth and dramatically enhanced our financial profile. 
We also built a strong foundation with our capabilities, manufacturing platforms and our deep customer relationships. From this foundation, our growth will accelerate. Our third quarter results and fourth quarter outlook already demonstrate the momentum we expect in the next phase of Springboard. We expect to double our sales from $20 billion to $40 billion by the end of 2030 to grow EPS much faster than sales and to improve our financial profile even further. We expect our free cash flow to grow through the planning cycle even as we invest. In total, we're focused on creating significant value for our shareholders, and we look forward to updating you on our journey. And with that, I will turn things back over to Chris for Q&A.

**Christopher Keenan** (Executives):
Thank you, Ed. Operator, we are ready for the first question.

**Operator** (Operator):
[Operator Instructions] The first question comes from Josh Spector with UBS.

**Joshua Spector** (Analysts):
I wanted to ask on just the optical margin cadence. I don't know, Ed or Wendell, when you guys feel comfortable to kind of talk about margins on a forward view at all. Clearly, your investments are picking up. Your incremental pretax margins are still in kind of the 40% or higher range. Is this something you have confidence yet to be able to talk about and give a target at some point in the near future?

**Edward Schlesinger** (Executives):
So thanks for the question, Josh. So I would agree, I think we have done a really nice job as we've been growing optical to improve our net income margin. I'll use that as sort of the vector to think about. We were in the mid-teens. We're now in the low 20s. I certainly think there is an opportunity for us to continue to improve from there. And obviously, that has driven the company's operating margin significantly. We've grown that into the low 20s as well. And again, I think we feel good about our environment. The thing I would say is we're going to be adding capacity in optical to grow. As we've shared, we're also still building a Solar business, and that is actually still negatively impacting or dragging our margins a little bit. So I don't know that we're quite yet ready to put out a new target, but I think you should think of us as continuing to be where we're at and making progress from there as we grow.

**Joshua Spector** (Analysts):
That's helpful. If I could just follow up just in terms of corporate costs, that seems to be a thing people are nitpicking on this morning a bit. You're about $50 million-ish lower year-on-year. That was kind of a big part of kind of why 3Q was in line. Is there something going on there between the allocations between corporate and the segments? And what's the assumption in the fourth quarter, please?

**Edward Schlesinger** (Executives):
Yes, there's nothing going on. I mean we mentioned on our second quarter call, and it continues here in our third quarter that our variable compensation expense. So we pay for performance, and we have a number of tools that we use to do that. And the compensation expense is a little above what I would consider to be normalized levels. We saw that in the second quarter. We've seen that here in the third quarter. It probably levels off. I don't necessarily think it accelerates in the fourth quarter. And then it resets as we go into the subsequent year. So I view operating expenses, which in general is what sits in that corporate expenses bucket as being a leverage point for us as we grow. I think we will continue to be able to leverage our operating expenses. They will grow slower than our sales.

**Operator** (Operator):
And our next question will come from Asiya Merchant with Citi.

**Asiya Merchant** (Analysts):
Just a couple of quick questions here. Wendell, you talked about at CNBC earlier this morning about Gen AI-related demand. There's just been a lot of concerns in the market about the durability of this demand, whether it's financing or any other kind of various constraints that are out there. Just you're standing firm with your Springboard. There was a large growth factor associated with optical. Just if you can talk about how you're thinking about these various constraints and how you factored that into your Springboard.

**Wendell Weeks** (Executives):
Thanks for the question, Asiya. What she is referring to for those of you who didn't have a chance to see CNBC this morning is one of the things that I talked about is sort of an important document has been filed this last week, which is Anthropic's S-1. And you see a number of interesting things in that. My 3 main takeaways are the tremendous growth is there. Second is the implied profitability of their inference tokens, which is that primary driver for what it is their customers use as inference, and that looks very profitable. And their comment that their #1 constraint is now and will continue to be compute, and we provide the networking for that compute. 
What we see in our demand, Asiya, is a continued press from our customers to do more and more. And as a result, what you see us doing when we're doing these multiyear agreements is asking those customers. Our customers are primarily the major hyperscalers, given our long-standing relationships, help us fund and secure that capacity so that we can be assured of that demand and we reduce any amount of risk to our shareholders. So I don't think I have gotten one call yet that has been for anything else other than more of our new products, faster and broader. Does that answer your question? Or did you have something deeper behind that, Asiya?

**Asiya Merchant** (Analysts):
No, no, that's great. And just on the scale-up, Ed, I know you talked about the scale-up opportunity being significantly greater. You guys talked about it at your Investor Day as well. Just any updates? There's been just a lot of chatter around all the various events that have happened around optical and scale-up. Just any more color on how you're thinking about photonics as a map through 2030? And any other color for next year as well on the photonics map?

**Wendell Weeks** (Executives):
That's a great question, Asiya. So for those of you who don't follow this closely, Asiya is asking about scale-up [indiscernible] our demand is primarily driven by what's called scale-out, connecting those GPUs out down the rows to every other GPU that sits in the cluster. That's about 16 fibers per GPU in today's architectures. 100% of the current scale-up architectures are in copper. If that was 100% optical scale-up, you increase to 160 fibers per GPU. So that's a tenfold increase. 
And so the question then becomes how fast is that going to happen? What percent of the GPUs will be connected by optical scale-up? And given its strong leverage on our financials because obviously, a 10x increase in demand per GPU would have a significant impact on our financials given our position. This is what drives the quite appropriate fascination with timing. So what we said in the May IR event was we expected optical scale-up to begin to accelerate in 2028. We continue to believe that strongly. We're on the inside of that ecosystem. I know people hear different things about different particular components and will this be delayed or will that be delayed? This is just classic technology development. We continue to be quite convicted that this accelerates in 2028.

**Operator** (Operator):
The next question comes from Meta Marshall with Morgan Stanley.

**Meta Marshall** (Analysts):
Great. Maybe, Wendell, maybe expanding on that. If you could just speak to kind of the battle that you guys are having in terms of being able to fulfill carrier versus enterprise and maybe just how -- if there is a battle there to figure out how to make those allocations. And then maybe second for Ed, just I believe in previous quarters, you would kind of contextualize what the solar overhang was, just if you were willing to lay that out.

**Wendell Weeks** (Executives):
So we've been -- we started so early that we -- it's why you've been able to see our revenues they seem to increase so smoothly because we started on the capacity early. You are correct that especially our newest high-density products are surprising us with the speed and breadth of their adoption and that our traditional carrier customers now really want this product in their DCI architectures because they can fit 2 to 4 more times fiber in the same conduit. And at the same time, Gen AI is why we developed the dense products as we try to increase the amount of fibers per GPU, that also has a strong demand for those products. And so what's really causing the tension is people want that newest product, and we're still ramping that up to be the product across all of our platforms. 
The way we sort of sort that out is centered around the long-standing nature of the relationships, those ones that are going on for decades. We tend to prioritize those customers. And then as well, when we have to add capacity, we have a natural sort towards quality because we ask them to contribute to those capacity adds. This will tend to shift our allocation, shift the percent of our revenue that goes to those folks who have the resources to help us fund that capacity. Does that make sense to you, Meta?

**Meta Marshall** (Analysts):
Yes, that does.

**Edward Schlesinger** (Executives):
Well, I'll take the second question, Meta. The first thing I want to point out is, I think the most important thing on solar, the most important takeaway, I think, for folks, is the Section 232 ruling, which took place in the third quarter. That actually has a very nice impact on the pricing environment and also indexes to demand for U.S. made solar products. So that's us. I think that is a really important thing. It actually continues to strengthen our view in the ability to build a more than $3 billion business with nice profitability. So I think that's important. 
As we said on the call, we continue to make slow, steady progress on our ability to make and sell the products that we make. So we make polysilicon wafers and modules in the U.S. And we had sort of, I'll call it, bottomed out in the second quarter, and we're around the same level here in the third quarter. So the drag, if you will, or the EPS or margin impact in the third quarter is similar to what we saw in the second quarter, and we would expect it to slowly improve from this level as we go through 2027. And then depending on our ability to inflect up on our productivity, that will really drive the profitability aspect of the business.

**Operator** (Operator):
And the next question is going to come from Joseph Cardoso with JPMorgan.

**Marc Vitenzon** (Analysts):
This is Marc Vitenzon for Joseph Cardoso. I guess the first question kind of piggybacks on the supply question with regards to accelerating top line growth from 17% in 2Q to 19% in 3Q and then high teens exiting the year and going into next year. How much of that is driven by demand versus new capacity coming online? How should we just think about the broader demand/supply dynamics there? And then I have a follow-up.

**Wendell Weeks** (Executives):
Things are tight. And so as you see our revenue increasing, certainly is bringing on our new capacity is part and parcel of that. And we have the capacity plans in place that are already well underway to support that accelerating growth that you see in the next phase of Springboard as we move from the 15% CAGR during the first 3 years to 19% from '27 throughout the end of our Springboard planning period. And so it will be both. The other thing that also helps us on the revenue is basically realized price. Overall price is going up, but more importantly, as we develop these new products, they create a lot of value for our customers, and we tend to split that value creation with our customers that allows us to get more revenue per element of capacity. Did that answer your question, Marc?

**Marc Vitenzon** (Analysts):
Yes. That's super helpful. And then the follow-up would be on carrier, where historically, you framed growth around mid-single digits. This quarter, you signed Verizon and AT&T on top of Lumen and Zayo, how are you thinking about carrier growth into 2027? Would the acceleration primarily be driven by DCI in the long haul? Or is fiber-to-the-home also a substantial contributor?

**Edward Schlesinger** (Executives):
Yes. Thanks, Marc. For sure, data center interconnect is the bigger opportunity in the carrier space. I would expect that to drive nice growth as we go into next year and then beyond that. As we shared, we had originally said we thought that DCI could be a $1 billion business by the end of the decade. We will clearly exceed both the timing and the magnitude of that target. We haven't yet set a new target because I think there's a lot of activity in that space. So we'll take some time and sort of lay that out and come back and talk about it later. I would also say that fiber-to-the-home will continue to be a growth driver. I think you will see deployments certainly by the large carriers in that space. We're very well positioned for that as well.

**Operator** (Operator):
And the next question will come from Wamsi Mohan with Bank of America.

**Wamsi Mohan** (Analysts):
I had 2 as well. Maybe first on the customer deposits. Can you help us think through how much of the $2 billion of 2026 CapEx was funded by customers? And how does that share change into 2027 and beyond? And if you sort of look at the free cash flow dynamic, if I understand it right, you're going to repay deposits as customers take volume. So how much does it sort of create a headwind for free cash flows as you look into '27 and '28? And I have a follow-up.

**Edward Schlesinger** (Executives):
Thanks, Wamsi. And also congrats on the Marathon. I saw some photos of you at the Wineglass Marathon. So on the customer funding, what I would say is not all of our capital is for optical or towards our growth. Some of it is maintenance of business. So if I sort of exclude that part, the maintenance of business part, the majority of our capital is funded by the long-term agreements that we've signed. And that will kind of -- over the long term, that will kind of even out. It may not match exactly in any given quarter. We generally would get cash before we're spending the capital. The cash flow question, which I tried to explain today a little bit, but maybe I'll elaborate a little bit more, I think is really the important one. 
So for us, what we are seeking to do is as we grow and invest to continue to increase our free cash flow through the planning cycle. You saw that or you've been seeing that in 2026. Clearly, year-to-date, we're in a great position. And even as we return that cash, we expect to be able to continue to grow our free cash flow nicely because we will be generating a nice return, a nice level of profit and cash on the volume we're selling. And then therefore, we're returning a portion of that via that incremental operating cash flow. So it sort of smooths out our cash flow, reduces the volatility over time and it allows us to grow free cash flow as we continue to grow sales. So that's how you should think about it.

**Wamsi Mohan** (Analysts):
I appreciate the comment. On the display price increases, how large is the increase? And how much shows up in Q4? Does it fully offset sort of the weaker yen because you did have a little step down in display profitability in the quarter? Are we back to normal by Q4? Or does it take a little longer for it to flow through?

**Edward Schlesinger** (Executives):
Yes. So first of all, on the timing, we're implementing those increases now. They should begin to take place in the fourth quarter, but I don't think you should expect that to be a significant impact in the quarter. They're really geared around 2027 and beyond. As you know, the yen has been weak, and there are other input costs where we're seeing some level of inflation. We shared back in May that we had sort of derisked our long-term plan and taken the yen to 150, we continue to hedge, and we hope to do better than that in our hedging, but that's sort of why we're making these price increases. We're not disclosing the specific amount of the increase, but you can think of it as similar to what we've done the last few times we've done it.

**Operator** (Operator):
And our next question comes from George Notter with Wolfe Research.

**George Notter** (Analysts):
Wendell, I wanted to ask about your perspective on the Chinese fiber in your business. I assume you're going to talk to tariffs and shipping costs, keeping Chinese fiber out of the markets that you play in. Certainly, there's geopolitical concerns. Certainly, there's your LTAs and co-innovation with customers. But at the same time, I mean, the market is just so asymmetric in terms of supply and demand. And I guess what I'm asking is, are you seeing fiber from China? And what's your perspective on that potential impact on your business?

**Wendell Weeks** (Executives):
That's actually a great question, George. In terms of the percent of the market that we see exposure to Chinese fiber, that has been dropping actually. Now it has to do with a lot of different things, not the least of which is more and more of the fiber is being consumed in pretty complicated connectivity product sets where the degree of integration is high. And once it becomes integrated, its shipping costs become a lot higher, right? And the tariff costs become a lot higher. So it's not quite as easy as shipping reels of fiber around because you have so much of the value sitting in connectivity. 
Now that being said, we always -- we compete in China against the Chinese players. And what we always count on for the long term is we're the highest quality, lowest cost, biggest producer in the world, and we continue to expand those advantages. So for now, we're not seeing it as a significant competitive pressure, but we're always preparing for the moment when that could happen.

**Operator** (Operator):
And our next question is going to come from Matt Niknam with Truist.

**Matthew Niknam** (Analysts):
Congrats on the quarter. I'll continue the theme and just ask 2 quick ones, if I could. First, on the fourth quarter outlook, maybe, Ed, if you can help us unpack the outlook for the $5.2 billion to $5.3 billion for sales just across the different segments. And then maybe a follow-on for Ed as well. You filed for a $2 billion ATM equity program a few months ago, you've got $2.5 billion of cash on the balance sheet. The business is obviously generating additional incremental cash flow. So if you can speak to the rationale for setting up the ATM and what would make you effectively use it relative to debt or other sort of customer prepayments.

**Edward Schlesinger** (Executives):
Yes. And Matt, I just want to make sure I caught your first question specifically. Are you asking about the content of the sales growth, like where it's coming from in the fourth quarter?

**Matthew Niknam** (Analysts):
That's right across the different segments. Any relative changes relative to 3Q.

**Edward Schlesinger** (Executives):
Got you. Yes. I think for sure, we expect to have a really robust quarter in Optical Communications. That will drive the lion's share of our growth year-over-year. As we shared, the AI data center component of our enterprise business grew 100%. I think we really are seeing very strong demand, and that's going to do -- drive a lot of the growth. I think solar will continue to also drive growth as we bring capacity on, and then that should start to impact our earnings as we improve our productivity. 
Again, I think of that as slow and steady, but it will certainly be a growth driver. So probably pretty similar dynamics to what you saw in the third quarter. And on the ATM, I think of it as housekeeping for us. We have a shelf registration for debt. This is very much like a shelf registration for equity. So we have no intention of doing anything at this time, but it just -- it allows us to use this as a tool if we ever need to do that in the future. As you know, what's important to us is having a very strong balance sheet. We invest over long cycles in innovation, and we are growing a lot now, and obviously, we're adding capacity. But there are a lot of technology opportunities for us, and we want to make sure that no matter what happens in the external environment, we can continue to invest through any kind of cycle. So we always do things that help improve our balance sheet, and this is just a housekeeping thing for us to have on the shelf.

**Operator** (Operator):
And the next question is going to come from Martin Yang with Oppenheimer.

**Martin Yang** (Analysts):
A question on solar's profitability in the medium term, perhaps -- your operating -- corporate operating margin keeps improving and you have the goal of solar getting to corporate average towards the end of '27. I just want to make sure that goal is still intact. And you're referring to this continued improving trajectory of a corporate average. So solar is meeting that moving target? Or is it solar's margin profile getting to the previous corporate average comparing to the most recent one?

**Edward Schlesinger** (Executives):
Yes. I think in general, currently, solar is below our corporate operating margin, so it's creating a drag. As we improve productivity, that profitability will improve. And I think it will be slow and steady. And we feel great about the business overall and the Section 232 ruling is also very favorable to the pricing environment, which is a nice impact in general to margins. I don't know -- I think you should just think about it as continuing to help our overall corporate average as it improves. If we continue to move that number up, it's certainly possible that solar gets there. But I think of -- if we get above 20% in solar, it will significantly improve our overall corporate average.

**Wendell Weeks** (Executives):
It's a positive sort of question in that will our corporate average improve faster than we can -- the ultimate level of profitability we can deliver. And so that would be a really good problem to have, both of them racing for increased profitability.

**Operator** (Operator):
[Operator Instructions] Our next question will come from John Roberts with Mizuho.

**John Ezekiel Roberts** (Analysts):
We usually think of Starlink as a competitive threat. But with their new move towards terrestrial, do they become a frenemy? And maybe with their data centers, they become more than a frenemy. Could you maybe give us some thoughts on that?

**Wendell Weeks** (Executives):
So we're fans of LEO, of low earth orbit. A, because we have some content on those. But B, you are right on the right area, which is now we'll be able to connect people, especially in more sparsely created areas -- more sparsely populated areas, as well as any sort of spots in the network that you can easily reach with a shared architecture. That's going to increase the bandwidth as they go more and more into data centers, that becomes a big driver for our product as well. And as you quite rightly point out, the data has to land in a network, and that data, as it lands, is certainly fiber optics. So in general, we are very positive on LEO, and we think you're looking at it right. The thing about the frenemy part, I think they are an important part of the mosaic, and we like customers.

**John Ezekiel Roberts** (Analysts):
And then, Ed, the yen hedge went from 98% down to 94%. Is there a plan to lower that over time by about 4% per quarter?

**Edward Schlesinger** (Executives):
No. No plans, John. We do our best to hedge the majority of our exposure in any given quarter. That moves around a little bit depending on what happens in the quarter. But the goal is to be as hedged up, if you will, as we can be practically.

**Operator** (Operator):
I am showing no further questions at this time. I will now turn the call back over to Chris for closing remarks.

**Christopher Keenan** (Executives):
Thank you for joining us. And before we close, I want to let everyone know that we will be attending the UBS Global Technology and AI Conference on December 1. Additionally, we'll be scheduling management visits to investor offices in select cities. Finally, a web replay of today's call will be available on our site starting later this morning. Once again, thank you all for joining us. Operator, that concludes our call. Please disconnect all lines.

**Operator** (Operator):
Thank you for participating, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GLW_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：CFO 給 Q3 財測：營收約年增 16%、區間 49–50 億美元，core EPS 0.85–0.89 美元。（原話："range of $4.9 billion to $5 billion and core EPS to grow"）
- 2026-07-28｜CFO｜guidance：CFO 說 Q3 財測並非暗示成長減速，而是與 Q2 相近的年增率。（原話："intended to imply similar year-over-year growth as we had"）
- 2026-07-28｜CFO｜guidance：CFO 說 Q3 財測隱含年化營收可能比預定提早一季達到 200 億美元。（原話："actually get to that $20 billion that we put out for the"）
- 2026-07-28｜CEO｜guidance：CEO 說不想在 5 月剛上調後再度上調 Springboard，Q4 財測時再更新，Q4 無隱含訊息。（原話："we didn't want to reupgrade our Springboard plan again"）
- 2026-07-28｜CEO｜guidance：CEO 重申升級版 Springboard 20-30-40 年化營收目標：2026 年底 200 億、2028 年底 300 億、2030 年底 400 億美元。（原話："grow our annualized sales run rate to $20 billion by the"）
- 2026-07-28｜CEO｜guidance：CEO 說 2026 年第四季至 2030 年第四季營收年複合成長率 19%，且獲利成長快於營收。（原話："expect to deliver a sales CAGR of 19% from"）
- 2026-07-28｜CFO｜guidance：CFO 說明對投資人的「高信心計畫」是內部計畫風險調整後的版本：2028 年 270 億、2030 年 350 億美元年化營收。（原話："Our high confidence plan is to grow sales to an annualized"）
- 2026-07-28｜CFO｜guidance：CFO 預計全年資本支出約 20 億美元，Q3、Q4 支出速率提高，並維持全年自由現金流顯著年增。（原話："invest approximately $2 billion for the year to support the"）
- 2026-07-28｜CFO｜guidance：CFO 預期今年手機市場因記憶體價格出貨量衰退中段十位數百分比。（原話："expect memory prices to impact the handheld market with"）
- 2026-07-28｜CFO｜margin：光通訊部門 Q2 淨利率（NPAT/營收）創高，為 21%。（原話："profitability in the second quarter with NPAT as a percent"）
- 2026-07-28｜CEO｜margin：CEO 說光通訊獲利提升主因不是裸光纖漲價，而是創新產品創造價值後留下一部分。（原話："increasing the price of bare fiber. The price is higher,"）
- 2026-07-28｜CEO｜margin：CEO 說明定價邏輯：以創新為客戶創造價值，公司保留其中一部分。（原話："we get to keep a portion of that"）
- 2026-07-28｜CFO｜margin：CFO 回答 JPM 分析師，確認其對 Q3 財測隱含毛利率與營業利益率上升的推算方向正確。（原話："Yes, Joe, I think your assessment is correct."）
- 2026-07-28｜CFO｜margin：太陽能 Q2 因晶圓廠延長維修停工多出約 3,000 萬美元費用，部門淨損 700 萬美元。（原話："an additional $30 million of expense versus"）
- 2026-07-28｜CFO｜commitment：CFO 承諾營業利益率維持在 20% 或以上，並在今年稍後更新營業利益率想法。（原話："run at or above 20% operating margin even as we continue to"）
- 2026-07-28｜CFO｜commitment：CFO 表示尚未設定新的利潤率目標，要累積更多太陽能與光子業務經驗後才調整。（原話："We haven't set a new target. We'll come back later this"）
- 2026-07-28｜CFO｜commitment：CFO 預期 ROIC 在規劃期內從約 15% 提升至高十位數。（原話："we expect to continue improving ROIC into the high teens"）
- 2026-07-28｜CFO｜commitment：CFO 說太陽能業務將做到 30 億美元營收，獲利高於公司平均。（原話："build our solar business into a $3 billion revenue"）
- 2026-07-28｜CEO｜commitment：CEO 說明確表示未對光子業務給出明年具體數字，只給 2030 年 100 億長期目標，每季更新。（原話："And I don't think we guided anything for next year on"）
- 2026-07-28｜CEO｜commitment：CEO 承諾持續提高長期協議（LTA）比重，所有重大擴產都由此類協議支撐。（原話："all of our significant capacity moves are backed by those"）
- 2026-07-28｜CEO｜commitment：CEO 回應表示會提高多晶矽在半導體級（最高等級）的占比。（原話："you should expect us to continue to increase our"）
- 2026-07-28｜CFO｜capital_allocation：CFO 說明資本模式：有機投資需先投入大量資本，現以與客戶的長期協議分攤擴產風險與成本。（原話："long-term agreements to more appropriately share the risk"）
- 2026-07-28｜CFO｜capital_allocation：CFO 預期自由現金流在持續投資的同時仍將顯著成長。（原話："we expect free cash flow to"）
- 2026-07-28｜CEO｜product：CEO 說 Q2 企業網路營收年增 65% 至 12.7 億美元，Gen AI 產品營收近乎翻倍，且尚未看到 scale up 或光子貢獻。（原話："So the results will be attractive and we expect free cash"）
- 2026-07-28｜CEO｜product：CEO 估計到 2028 年企業網路每 GPU 光學含量增加 1.3 至 1.5 倍，2030 年可能高得多。（原話："increase by 1.3x to 1.5x by 2028."）
- 2026-07-28｜CEO｜product：CEO 說 20-30-40 計畫假設頻寬成長對每 GPU 光纖數的影響為中性。（原話："per GPU to be neutral."）
- 2026-07-28｜CEO｜product：CEO 說全光 scale-up 的情境下每 GPU 光纖總量 160 條，為目前 scale-out 的 10 倍；實際會介於全銅與全光之間。（原話："fiber content of 160 fibers per GPU, which is 10x the"）
- 2026-07-28｜CEO｜product：CEO 說光子 MAP 有機會在 2030 年成為 100 億美元的市場進入平台。（原話："we have the opportunity for a $10 billion market access"）
- 2026-07-28｜CEO｜product：CEO 說光子業務是公司過去在設備內部沒有的新內容（CPO/NPO 被動光子元件）。（原話："Historically, we have had no inside-the-box content."）
- 2026-07-28｜CEO｜product：CEO 說光學連接埠占比屬機密，且 scale-up 的成功程度沒有人確知。（原話："Regretfully, I can't share the first because it's"）
- 2026-07-28｜CFO｜product：CEO 說 Gorilla Glass 預期優於終端市場；CFO 說明 TV 品牌轉向大尺寸有利 Gen 10.5。（原話："we expect Gorilla Glass sales to outperform the end market"）
- 2026-07-28｜CFO｜risk：CFO 指出風險調整中最大的一項是 scale-up 網路採用時機，影響企業網路與光子兩條線。（原話："One of the most significant areas we are adjusting for is"）
- 2026-07-28｜CEO｜risk：CEO 說光學 scale-up 的採用曲線可能呈指數型、時點難以預測。（原話："technology that will likely have an exponential adoption"）
- 2026-07-28｜CEO｜risk：CEO 承認產業對 scale-up 時點有許多揣測，但稱公司基本看法自 5 月起未變。（原話："we see no changes to our fundamental belief that we just"）
- 2026-07-28｜CFO｜risk：CFO 說手機市場下半年將顯著弱於上半年，汽車市場維持疲弱。（原話："will be significantly weaker than the first half of the"）
- 2026-07-28｜CEO｜risk：內部計畫假設 2027–2030 日圓匯率 150，並假設電視、IT、手機終端市場持平、內燃機需求下降。（原話："forward rate of JPY 150 per USD to account for a weaker yen."）
- 2026-07-28｜CEO｜customer：CEO 列舉客戶協議：Apple 100% iPhone/Watch 蓋板玻璃、Meta 最高 60 億美元多年協議。（原話："Meta announced a multiyear up to $6 billion agreement to"）
- 2026-07-28｜CEO｜customer：CEO 提到 5 月 NVIDIA 多年商業與技術夥伴關係，6 月 Amazon 數十億美元協議。（原話："agreement with Corning under which we'll supply the optical"）
- 2026-07-28｜CEO｜customer：CEO 說「若能多生產就能多賣」，尤其是最創新的高密度產品。（原話："if we could make more, we could sell more."）
- 2026-07-28｜CEO｜customer：CEO 解釋 Carrier Q2 僅年增 1% 是客戶專案時點，上半年 Carrier 年增約 17%。（原話："So it's just customer timing what you're seeing in the"）
- 2026-07-28｜CEO｜competition：CEO 說產業內部對 scale-up 的變化遠少於外界揣測，各方知道如何取捨仍可交付 scale up。（原話："there's just way less change than from what sort of gets"）
- 2026-07-28｜CFO｜competition：CFO 稱康寧是唯一的美國本土多晶矽與晶圓製造商。（原話："we are the only U.S.-based polysilicon and wafer"）

### 問答異常語氣（迴避／改口／保留）
- GLW_Q2_2026_Earnings_Call_20260728.md｜問：Josh Spector (UBS)：光子是否仍有 2027 年 10 億美元以上的能見度，與兩個月前相比有無改變？｜答法：CEO 先說基本看法無變、以機率調整時點，未直接確認 2027 年 10 億美元；後補充公司未對光子明年給過任何具體數字。
- GLW_Q2_2026_Earnings_Call_20260728.md｜問：Asiya Merchant (Citi)：Q3 財測後 Q4 為何成長有限？｜答法：CFO 與 CEO 改談長期 20-30-40 與提早一季達標，稱「無隱含訊息」，未給 Q4 數字，表示等 Q4 財測時再更新。
- GLW_Q2_2026_Earnings_Call_20260728.md｜問：George Notter (Wolfe)：非 LTA 客戶定價漲幅多少、LTA 占比現況？｜答法：CEO 未給 LTA 占比數字（僅稱「大部分」）也未給調價幅度，改談價值分享與獲利率成長。
- GLW_Q2_2026_Earnings_Call_20260728.md｜問：Wamsi Mohan (BofA)：Enterprise 營收季增約 3 億美元，為何淨利率沒有明顯營運槓桿？｜答法：CFO 未直接回答抵銷因素，改述光通訊利潤率將持續提高。
- GLW_Q2_2026_Earnings_Call_20260728.md｜問：Joseph Cardoso (JPM)：能否說明營業利益率目標，及 Q3 利潤率改善的可持續性？｜答法：CFO 確認方向，但拒絕設新目標、只稱 20% 以上，且「要再多些經驗」才調整，今年稍後再談。

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
{"date":"20260729","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 光連接的結構性需求延續，且 Corning 的價值捕獲能力上升（不只賣得多，還賣得更賺）"},{"id":"H2","text":"Springboard「高信心版本」兌現（2028 年底 $27B、2030 年底 $35B run-rate），營業利益率維持 20%+"},{"id":"H3","text":"結構性重估可持續：市場願意給營業利益率 21%、核心 ROIC 15% 的 Corning 高於歷史中位 17.5x 的倍數（進場條件而非業務假設）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI 資本支出於 2028-2029 進入消化期，且光纖產能同步過剩。多份獨立產業評論已把當前光通訊資本支出與 2001 年 dark fiber 泡沫類比，並指出若磷化銦、共封裝光學、光路交換多方同時擴產，2028-2029 可能出現產能過剩與價格壓力。本報告的 5 年窗口正好覆蓋 2028-2031。"},{"id":"R2","text":"資本強度上升吃掉自由現金流。資本支出自 $12.8 億提高至約 $20 億（+56%），而自由現金流利潤率僅 9.0%。管理層承諾「即使投資也要讓自由現金流顯著成長」，但尚未經完整年度驗證。"},{"id":"R3","text":"空芯光纖與競爭者整併的雙重結構侵蝕。(a) Microsoft 空芯損耗 0.091 dB/km 已優於矽玻璃 0.14 dB/km 的物理地板，Azure 已部署 15,000 公里，且 Microsoft 是四大雲端中唯一缺席長約名單者；(b) Amphenol 於 2026-01-09 完成 $105 億收購 CommScope 連接業務；(c) 全球光纖市場高度分散（Corning 份額約 10.4%、前五大合計約 43-53%）。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"CY27本益比≤27x（約$116）建1/3；≤24x（約$103）補足；或Photonics首度給出可驗證近期里程碑→跑道回🟢重跑升級路徑","irr_base_pct":9.4,"ev5y_pct":49.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.9,"ev5y_pct":49.9,"irr_base_pct":9.4,"max_dd_pct":-55.0,"bull_5y_price":325.0,"bear_5y_price":69.0,"p_bull_pct":22.0,"p_bear_pct":31.0,"rearm_trigger":"CY27本益比≤27x（約$116）建1/3；≤24x（約$103）補足；或Photonics首度給出可驗證近期里程碑→跑道回🟢重跑升級路徑","price_at_dd":126.01,"archetype":"品質複利成長","cycle_position":"早循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLW_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
