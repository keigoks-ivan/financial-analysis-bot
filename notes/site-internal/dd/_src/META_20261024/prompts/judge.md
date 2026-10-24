你是 stock-analyst **v20 判斷 agent**，標的 META（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"META","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":64601,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（YoY +26%；QoQ +6.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"},"note":"共識約 $63.4B（LSEG，Reuters 2026-10-20）；公司原指引 $61–64B"},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income（Meta 不報 Non-GAAP；此為剔除 $9.89B 訴訟和解費用後的調整數）","value":22880,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（利益率約 35.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":12988,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（利益率 20%；YoY -37%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi3_free_cash_flow","label":"Free cash flow","value":-2120,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（營運現金流 32,786 減 capex 33,942 減融資租賃本金；Q3 2025: +10,625）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi4_capital_expenditures","label":"Capital expenditures（含融資租賃本金）","value":34910,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi5_share_based_compensation","label":"Share-based compensation","value":7363,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（占營收 11.4%；占 GAAP 營業利益 56.7%；占剔除費用後營業利益 32.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi6_gaap_diluted_eps","label":"GAAP diluted EPS","value":3.83,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD（剔除和解費用後 7.40；Q3 2025: 1.05）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"},"note":"共識 EPS 分歧大（含費用口徑約 3.56–5.70、不含約 6.53，來源：web_search 彙整，未能單一驗證）"},{"id":"f_kpi7_guidance_q4_2026_revenue","label":"Guidance: Q4 2026 revenue","value":"73000～76000","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（含約 1% 匯率逆風）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"},"note":"Benzinga 彙整 Q4 營收共識約 $73.65B"},{"id":"f_kpi8_guidance_fy2026_total_ex","label":"Guidance: FY2026 total expenses","value":"175000～179000","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（已納入 9.9B 訴訟費用）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi9_guidance_fy2026_capex","label":"Guidance: FY2026 capex（含融資租賃本金）","value":"135000～145000","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（前次 130,000–145,000）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi10_guidance_fy2026_reality_","label":"Guidance: FY2026 Reality Labs 虧損與其他","value":"18000～19000","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD M（RL 虧損區間；Q4 稅率 15–17%；2027 RL 虧損約 $15B；剔除訴訟費用後 2026 營業利益仍預期高於 2025）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi11_family_daily_active_peop","label":"Family daily active people (DAP)","value":3.64,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"billion（YoY +3%，2026 年 9 月平均）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi12_ad_impressions_growth","label":"Ad impressions growth","value":10,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"% YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_kpi13_average_price_per_ad_gro","label":"Average price per ad growth","value":14,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","unit":"% YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[13]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-21）","citation":"Meta 公司新聞稿 https://s21.q4cdn.com/399680738/files/doc_news/Meta-Reports-Third-Quarter-2026-Results-2026.pdf（IR 站 investor.atmeta.com 同稿，2026-10-21）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-21","period":"2026-10-21","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-21"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_meta_gross_margin_pct","label":"META 毛利率","value":81.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_meta_operating_margin_pct","label":"META 營業利益率","value":38.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_meta_fcf_margin_pct","label":"META FCF 利潤率","value":17.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_googl_gross_margin_pct","label":"GOOGL 毛利率","value":60.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_googl_operating_margin_pct","label":"GOOGL 營業利益率","value":33.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_googl_fcf_margin_pct","label":"GOOGL FCF 利潤率","value":11.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amzn_gross_margin_pct","label":"AMZN 毛利率","value":50.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_operating_margin_pct","label":"AMZN 營業利益率","value":11.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_fcf_margin_pct","label":"AMZN FCF 利潤率","value":-0.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_snap_gross_margin_pct","label":"SNAP 毛利率","value":57.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNAP.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_snap_operating_margin_pct","label":"SNAP 營業利益率","value":-5.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNAP.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_snap_fcf_margin_pct","label":"SNAP FCF 利潤率","value":11.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNAP.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pins_gross_margin_pct","label":"PINS 毛利率","value":79.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PINS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pins_operating_margin_pct","label":"PINS 營業利益率","value":6.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PINS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pins_fcf_margin_pct","label":"PINS FCF 利潤率","value":28.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PINS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":642.62,"period":"2026-10-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-4.64,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":35.76,"period":"2026-10-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.03,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（30.3 → 30.29）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（34.8 → 34.8）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.47,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（40.23 → 40.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":30.29,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":34.8,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":40.42,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-2.85,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 31.18 → 30.29（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":21.92,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝54.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":54.9,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.78,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝57.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":57.8,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.91,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝58.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":58.9,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":21.22,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 30.29，分子＝快照價 642.62","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.327,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":32393.0,"period":"2026-10-24","unit":"USD m","basis":"yfinance 最新一季：總債務 114842.0、現金 82449.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":2547.51,"period":"2026-10-24","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1669471.4,"period":"2026-10-24","unit":"USD m","basis":"市值 1637078.4 ＋ 淨負債 32393.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":256558.0,"period":"2026-10-24","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（50 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":311385.98,"period":"2026-10-24","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（60 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.51,"period":"2026-10-24","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 642.62 / W52 629.96 / W104 642.27 / W250 440.98 / W250 13週斜率 1.36%"},{"id":"f_ma_w52","label":"52 週均線","value":629.96,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":642.27,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":440.98,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.36,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"META 10-K FY2025 風險因子自述：部分用戶（尤其年輕用戶）已轉用替代產品並減少使用 Meta 產品，且 Apple、Google 皆把競品整合進 iOS／Android。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"We believe that some users, particularly younger users, are aware of and actively engaging with other products and services similar to, or as a substitute for, our products and services, and we believe that some users have reduced their use of and engagement with our products and services in favor of these other products and services.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"META 10-K FY2025 自述除社群與廣告對手外，另在前沿 AI 模型與消費硬體／AR／VR 與其他公司競爭，且硬體經驗有限，可能讓他人更有效競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"We also compete with companies in the development and application of AI, particularly with respect to the development of frontier AI models, as well as the development and delivery of consumer hardware and augmented and virtual reality products and services.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"eMarketer 預測 2026 年 Meta 將以約 26.8% 全球數位廣告份額首度超越 Google（26.4%），預測值。","source":"AdNews／eMarketer","url":"https://www.adnews.com.au/news/meta-to-overtake-google-in-global-digital-advertising-revenue","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Meta 2026-10 起禁止 ByteDance（TikTok 母公司）在其 App 刊登廣告，與對手關係升溫。","source":"The Star","url":"https://www.thestar.com.my/tech/tech-news/2026/10/09/meta-bans-tiktok-from-advertising-on-its-apps-in-escalating-feud","excerpt":"Meta bans TikTok from advertising on its apps in escalating feud By RILEY GRIFFIN and ALEXANDRA S. LEVINE Friday, 09 Oct 2026 | 10:00 AM MYT share bookmark TikTok enacted a number of measures to make it harder to shift from its app to other social platforms. — Unsplash Meta Platforms Inc banned advertisements in the US from ByteDance Ltd, the former controlling owner","as_of":"2026-10-09","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"META FY2025 10-K 揭露：2025、2024、2023 年度皆無單一客戶占總營收或應收帳款達 10% 以上，無客戶集中度問題。","source":"SEC EDGAR｜Meta Platforms 10-K（FY2025）Item 8","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"No customer represented 10% or more of total revenue or accounts receivable for the years ended December 31, 2025, 2024, and 2023.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q3 2026 廣告曝光量年增 10%（Q2 為 14%），單價年增 14%（Q2 為 12%）；曝光成長放緩、價格加速（單一來源，未對官方 8-K）","source":"ppc.land / relevantaudience（Meta Q3/Q2 2026 results）","url":"https://www.relevantaudience.com/meta/meta-q2-2026-results-ad-prices-up-12-percent/","excerpt":"In Q3, the total number of ad impressions served across our services increased 10%","as_of":"2026-10-23","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"CFO Li 表示公司持續低估算力需求，並拒絕給 2027 年資本支出指引，稱規劃為動態","source":"Munich Startup feed（Meta CFO refuses 2027 capex guidance）","url":"https://insights.munich-startup.de/news/feed/meta-cfo-admits-company-keeps-underestimating-ai-compute-needs-refuses-2027-capex-guidance","excerpt":"continued to underestimate our compute needs","as_of":"2026-10-23","retrieved_at":"20261024","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q2 2026 家族日活人數 36.0 億，年增 3%","source":"Meta Reports Second Quarter 2026 Results","url":"https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"第三方預估全球數位廣告支出 2027 年約 9,103 億美元、2028 年約 9,656 億美元，成長率略降","source":"Oberlo Digital Ad Spend","url":"https://www.oberlo.com/statistics/digital-ad-spend","excerpt":"the online ad spend market will continue to expand over the next few years, albeit with a slight deceleration","as_of":"2026-01-01","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Advantage+ 於 Q2 2026 年化營收達 750 億美元","source":"Meta Q2 2026 results coverage","url":"https://ppc.land/meta-takes-9-89bn-teen-settlement-charge-as-ad-revenue-gains-26/","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 披露：FTC 自 2020 年起訴 Meta 反壟斷，訴求含剝離或重組 Instagram 與 WhatsApp；2024 年 11 月歐盟執委會就 Marketplace 搭售與資料使用開罰。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"Beginning in 2020, we became subject to a lawsuit by the FTC alleging that we violated antitrust laws, including by acquiring Instagram in 2012 and WhatsApp in 2014. The complaint seeks a permanent injunction against our company's alleged violations of the antitrust laws, and other equitable relief, including divestiture or reconstruction of Instagram and WhatsApp. In addition, in November 2024, the European Commission issued a fine as a result of its finding that we tied Facebook Marketplace to Facebook and use data in a manner that infringes European Union competition rules.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 披露：美國、歐洲及其他轄區競爭主管機關對 Meta 的社交、廣告、行動應用及併購行為有多項訴訟與調查，且數量與重要性近年增加。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"Over the last several years, the number and potential significance of the litigation and investigations involving the company have increased, and there can be no assurance that this trend will not continue.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FTC 在 Meta 贏得壟斷案後仍提出上訴（2026-01）。","source":"Euronews: FTC presses on with appeal after Meta's monopoly battle win","url":"https://euronews.com/business/2026/01/21/ftc-presses-on-with-appeal-after-metas-monopoly-battle-win","excerpt":"(FTC) said on Tuesday it will appeal a November court ruling in favour of Meta in its long-running antitrust battle with the social media giant. ADVERTISEMENT ADVERTISEMENT The appeal keeps alive a high-stakes legal fight over whether Meta unlawfully maintained monopoly power in social networking by acquiring competitors such as Instagram and WhatsApp.","as_of":"2026-01-21","retrieved_at":"20261024","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：Meta 有意義的營收來自服務中國廣告主的少數經銷商，美中貿易爭端（含關稅）可能使政府行動減少或消除中國廣告營收。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"we generate meaningful revenue from a small number of resellers serving advertisers based in China, and it is possible that the Chinese, United States, or other government could take action that reduces or eliminates our China-based advertising revenue, whether as a result of the trade dispute with the United States, including any tariffs implemented by the United States or China","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：消費硬體製造依賴少數第三方、營運集中亞洲，關稅、制裁、出口管制可能造成供應短缺與成本上升。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"tariffs, sanctions, export controls, and other measures that restrict international trade) that subject us to supply shortages, increased costs, or supply chain or logistics disruptions.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：資料中心與光纖基建擴張涉及多地，貿易爭端可能推高專案成本或延誤。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"geopolitical challenges or actions by governments, including trade disputes or other developments, may lead to increased project costs, operational inefficiencies","as_of":"2026-01-29","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01 起美國 Section 232 對部分先進運算晶片課 25% 關稅；與美國資料中心相關進口獲豁免，商務部須於 2026-07-01 前提交資料中心晶片市場更新以評估調整。（搜尋摘要，未見 Meta 專屬說明）","source":"Thomson Reuters OneSource / GHY 摘要","url":"https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/january-15th/trump-admin-tariffs-advanced-ai-chips-232.html","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露：消費性硬體製造依賴少數第三方，且常集中於亞洲單一區域；關稅、制裁、出口管制可能衝擊製造與銷售。","source":"Meta Platforms Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"The manufacturing of our consumer hardware products depends on a small number of third parties, often with significant operations in a single region such as Asia. Geopolitical challenges, trade disputes, and actions by governments such as tariffs, sanctions, and export controls may negatively affect manufacturing, distribution, and sales.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FT 報導 Goertek 代工 Meta AI 眼鏡，Meta 稱供應鏈多元、不單靠一家製造商。","source":"PYMNTS: Meta Seeks New Supply Chain Opportunities for AI Smart Glasses","url":"https://www.pymnts.com/meta/2025/meta-seeks-new-supply-chain-opportunities-ai-smart-glasses/","excerpt":"Chinese hardware manufacturer Goertek is reportedly tightening its grip on the supply chain around Meta’s artificial intelligence-powered smart glasses, even as Meta tries to expand its supply chain outside China.","as_of":"2025-09-16","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 廣告曝光數年增14%、平均每則廣告價格年增12%（Family of Apps）","source":"Meta Reports Second Quarter 2026 Results (investor.atmeta.com)","url":"https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/","excerpt":"Ad impressions delivered across our Family of Apps increased by 14% year-over-year. Average price per ad increased by 12% year-over-year.","as_of":"2026-07-29","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 2026 廣告曝光數年增19%、平均價格年增12%","source":"Meta Reports First Quarter 2026 Results (investor.atmeta.com)","url":"https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/","excerpt":"Ad impressions delivered across our Family of Apps increased by 19% year-over-year. Average price per ad increased by 12% year-over-year.","as_of":"2026-04-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Family of Apps 營收 64,158百萬美元 vs 去年同期 50,772；Reality Labs 443 vs 470（百萬美元，SEC 8-K 附表）","source":"Meta 8-K Exhibit 99.1 (quarter ended 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001326801/000162828026066700/meta-09302026xexhibit991.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"eMarketer 預測 2026 年 Meta 全球淨廣告營收約 243.46 億（千萬級單位：$243.46B），超越 Google 的 $239.54B；佔全球數位廣告支出 26.8% vs Google 26.4%；Amazon 9.0%，三者合計 62.3%","source":"eMarketer / Decision Marketing","url":"https://www.decisionmarketing.co.uk/news/meta-to-overtake-google-with-adspend-to-top-243bn","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"WARC 預測 Meta 廣告業務 2026 年成長22.3%至約$240B、2027年放緩至12.1%；全球廣告支出2026年+9.1%至約$1.30T、2027年+7.9%至約$1.40T","source":"Advanced Television / WARC (2025-12 press release)","url":"https://www.advanced-television.com/?p=284814","excerpt":null,"as_of":"2025-12-11","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 廣告曝光年增10%、平均廣告價格年增14%；廣告營收$63.06B vs $50.08B；DAP 3.64B(+3%)","source":"TheDesk.net Q3 2026 earnings report","url":"https://thedesk.net/2026/10/meta-platforms-facebook-instagram-q3-2026-earnings-report/","excerpt":"Family daily active people: 3.64 billion (+3%) Ad impressions: +10% Average price per ad: +14% Global employee headcount: 66,775 (-15%) Read more Q3 2026 media earnings coverage","as_of":"2026-10-21","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Meta 10-K 自述：部分用戶（尤其年輕用戶）已使用類似或可替代其產品的其他產品，並減少使用 Meta 產品。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"We believe that some users, particularly younger users, are aware of and actively engaging with other products and services similar to, or as a substitute for, our products and services, and we believe that some users have reduced their use of and engagement with our products and services in favor of these other products and services.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Meta 10-K 將其業務描述為快速變動、有顛覆性技術，並列出與 AI 前沿模型開發及 AR/VR 消費硬體業者的競爭。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"Our business is characterized by innovation, rapid change, and disruptive technologies.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 describes Reality Labs hardware sales via third-party retailers/resellers/distribution partners plus direct-to-consumer Meta.com and Meta stores.","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"For our RL products, our sales efforts utilize third-party sales channels such as retailers, resellers, and distribution partners, and our direct-to-consumer channel, Meta.com, and several Meta stores.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"IDC: XR headset/glasses shipments +35.3% YoY in Q2 2026; Meta doubling down on distribution.","source":"IDC blog: Smart glasses growth cools to 35% as Meta doubles down on distribution","url":"https://www.idc.com/resource-center/blog/smart-glasses-growth-cools-to-35-as-meta-doubles-down-on-distribution/","excerpt":"Smart Glasses Growth Cools to 35% as Meta Doubles Down on Distribution Share","as_of":"2026-09-16","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Click-to-WhatsApp ads grew ~60% YoY in Q3 2025; WhatsApp paid messaging a growing revenue line.","source":"Exchange4media: WhatsApp powers Meta's Q3 surge as click-to-chat ads spike 60%","url":"https://www.exchange4media.com/digital-news/whatsapp-powers-metas-q3-surge-as-click-to-chat-ads-spike-60-148883.html","excerpt":null,"as_of":"2025-10-30","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 2026（2026-07-29 公布）營收約 $60.8B 小幅優於預期約 $60.2B，GAAP EPS $6.18 低於預期約 $7.18–7.22；Q3 營收 guidance $61–64B，中點低於共識約 1%（Barchart 數字：中點 $62.5B vs 預期約 $63.1B）；FY2026 capex guidance 收窄至 $130–145B、費用 $165–169B。","source":"Barchart / Rivkin / Benzinga（搜尋摘要）","url":"https://www.barchart.com/story/news/3534115/meta-nasdaqmeta-exceeds-q2-cy2026-expectations-but-stock-drops","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價共識：MarketBeat（2026-09-09）47 位分析師平均目標價 $785.22，區間 $595–$1,000，38 買進／9 持有；Benzinga（2026 年 8 月初）35 位平均 $781；Q2 後 UBS 目標價由 $766 降至 $715、Baird 由 $830 降至 $750（7/30）。4 月 FactSet 平均目標價 $847.30，之後下修。","source":"MarketBeat Forecast；Benzinga price targets（搜尋摘要）","url":"https://www.marketbeat.com/stocks/NASDAQ/META/Forecast/","excerpt":null,"as_of":"2026-09-09","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q1 2026（4/29）公司上調 FY2026 capex guidance 至 $125–145B（原 $115–135B），Q2 營收 guidance $58–61B 涵蓋共識 $59.5B；公布後股價隔日跌近 10%。Benzinga 統計 2022-10 至 2026-07 共 17 次 guidance 更新，上調 11 次、下調 4 次。","source":"Investing.com (Reuters)；SiliconANGLE；Benzinga（搜尋摘要）","url":"https://siliconangle.com/2026/04/29/meta-shares-drop-hours-capex-guidance-overshadows-first-quarter-beats/","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"UBS 於 Q1 後（2026-04-30）將 2026 EPS 預估由 $30.35 上調至 $32.67（FactSet 共識 $31.43），2026 營收預估 $252.3B，目標價由 $908 降至 $865。","source":"Placera（UBS note 轉述）","url":"https://www.placera.se/telegram/meta-platforms-seen-well-positioned-for-q2-as-ad-engine-improvements-continue-ubs-says-20260430","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"BofA 下調 Meta 目標價至 $820（原 $885），維持買進","source":"Placera","url":"https://www.placera.se/telegram/bofa-securities-cuts-price-target-on-meta-platforms-to-820-from-885-maintains-buy-rating-20260420","excerpt":"BofA Securities Cuts Price Target on Meta Platforms to $820 From $885, Maintains Buy Rating MT Newswires 20 april, 15:54 Dela","as_of":"2026-04-20","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 SEC 8-K 共12份，含重大項目者4份；清單中未見 Item 2.01（併購完成）、4.02（財報不可信賴）。重大項目含2026-10-21 的 Item 1.01（資本結構重整）。","source":"SEC EDGAR 8-K 申報清單（程式統計）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001326801&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 12 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"董事會於2026-10-19 核准修訂公司章程，新設無投票權 Class C 普通股（資本結構重整），股東書面同意於10-20 通過，預計2027-01-19 生效。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026066700/meta-20261019.htm","excerpt":"approved and declared advisable, based on the unanimous recommendation of a special committee consisting of disinterested and independent directors established to review such transaction, and recommended to the Company’s shareholders, the amendment and restatement of the Company’s certificate of incorporation (as so amended and restated, the “Restated Charter”) to, among other things, adjust the Company’s capital structure by establishing a new class of non-voting Class C common stock","as_of":"2026-10-21","retrieved_at":"20261024","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露公司涉及多起集體訴訟與股東衍生訴訟，涵蓋廣告、反壟斷、隱私、青少年等主題，另有 AI 訓練版權訴訟。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"We are involved in numerous lawsuits, including stockholder derivative lawsuits and putative class action lawsuits, many of which claim statutory damages and/or seek significant changes to our business operations, and we anticipate that we will continue to be a target for numerous lawsuits in the future.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"In re Facebook Inc. Derivative Litigation 於2025-07-17 達成原則性和解，Delaware Chancery 排定2026-04-07 和解聽證。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828025056768/meta-20251205.htm","excerpt":"on July 17, 2025, the parties to the stockholder derivative action in the Delaware Court of Chancery, captioned In re Facebook Inc. Derivative Litigation, Consolidated C.A. 2018-0307-KSJM (Del. Ch.) (the \"Matter\"), agreed to a settlement in principle to resolve all claims in the Matter, which is subject to court approval.","as_of":"2025-12-12","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"聚合站記載 Meta 於2026-06-22 收購印度 CRED，金額約$900M；同站又稱 Meta 為少數股東，尚未由一手來源證實。","source":"Windsor Drake Market Intelligence — Transaction · Payments · 2026","url":"https://windsordrake.com/market-intelligence/transactions/cred-meta-2026","excerpt":"Meta / CRED 2026 Meta acquired CRED for $900M on June 22, 2026. Target CRED Acquirer Meta Deal value $900M Announced June 22, 2026 Sub-sector Payments","as_of":"2026-06-22","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"major_events#5","axis":"major_events","section":"coverage","direction":"-","claim":"投資人於聯邦法院聲請認證 Cambridge Analytica 相關證券集體訴訟（購買期間2017-02至2018-07）。","source":"MLex 報導","url":"https://www.mlex.com/mlex/articles/2517005","excerpt":"MLex Summary: Investors accusing Meta Platforms of making misleading statements about the impact of the Cambridge Analytica data scandal asked a US federal judge to certify a proposed class. If approved, the class would encompass anyone who purchased Facebook common stock between February 2017 and July 2018.","as_of":"2026-08-21","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FY2025 10-K 揭露公司涉及多起集體訴訟與股東衍生訴訟，涵蓋廣告、反壟斷、隱私、青少年等主題，另有 AI 訓練版權訴訟。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm","excerpt":"We are involved in numerous lawsuits, including stockholder derivative lawsuits and putative class action lawsuits, many of which claim statutory damages and/or seek significant changes to our business operations, and we anticipate that we will continue to be a target for numerous lawsuits in the future.","as_of":"2026-01-29","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"In re Facebook Inc. Derivative Litigation 於2025-07-17 達成原則性和解，Delaware Chancery 排定2026-04-07 和解聽證。","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1326801/000162828025056768/meta-20251205.htm","excerpt":"on July 17, 2025, the parties to the stockholder derivative action in the Delaware Court of Chancery, captioned In re Facebook Inc. Derivative Litigation, Consolidated C.A. 2018-0307-KSJM (Del. Ch.) (the \"Matter\"), agreed to a settlement in principle to resolve all claims in the Matter, which is subject to court approval.","as_of":"2025-12-12","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"META","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.75,"operating_margin_pct":38.08,"fcf_margin_pct":17.95,"rd_intensity_pct":31.38},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"GOOGL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.9,"operating_margin_pct":33.11,"fcf_margin_pct":11.95,"rd_intensity_pct":15.47},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AMZN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.25,"operating_margin_pct":11.52,"fcf_margin_pct":-0.49,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SNAP","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.33,"operating_margin_pct":-5.1,"fcf_margin_pct":11.11,"rd_intensity_pct":30.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SNAP","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"PINS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":79.47,"operating_margin_pct":6.27,"fcf_margin_pct":28.11,"rd_intensity_pct":34.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PINS","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"META"},"financial_history":{"ticker":"META","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":116609000000.0,"revenue_yoy_pct":null,"gross_margin_pct":78.35,"operating_margin_pct":24.82,"net_income":23200000000.0,"diluted_eps":8.59,"free_cash_flow":19289000000.0,"fcf_margin_pct":16.54,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":134902000000.0,"revenue_yoy_pct":15.69,"gross_margin_pct":80.76,"operating_margin_pct":34.66,"net_income":39098000000.0,"diluted_eps":14.87,"free_cash_flow":44068000000.0,"fcf_margin_pct":32.67,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":164501000000.0,"revenue_yoy_pct":21.94,"gross_margin_pct":81.67,"operating_margin_pct":42.18,"net_income":62360000000.0,"diluted_eps":23.86,"free_cash_flow":54072000000.0,"fcf_margin_pct":32.87,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":200966000000.0,"revenue_yoy_pct":22.17,"gross_margin_pct":82.0,"operating_margin_pct":41.44,"net_income":60458000000.0,"diluted_eps":23.49,"free_cash_flow":46109000000.0,"fcf_margin_pct":22.94,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/META/META_Q3_2026_Earnings_Call_20261021.md）

# Q3 2026 Earnings Call
**Meta Platforms, Inc.** | Earnings Calls | 2026-10-21

**Operator** (Operator):
Good afternoon. My name is Krista, and I will be your conference operator today. At this time, I would like to welcome everyone to Meta's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] And this call will be recorded. Thank you very much. Rob Bevegni, Meta's Director of Investor Relations, you may begin.

**Rob Bevegni** (Executives):
Thank you. Good afternoon, and welcome to Meta Platforms' Third Quarter 2026 Earnings Conference Call. Joining me today to discuss our results are Mark Zuckerberg, CEO; and Susan Li, CFO. Our remarks today will include forward-looking statements, which are based on assumptions as of today. Actual results may differ materially as a result of various factors, including those set forth in today's earnings press release and in our quarterly report on Form 10-Q filed with the SEC. We undertake no obligation to update any forward-looking statement. 
During this call, we will present both GAAP and certain non-GAAP financial measures. A reconciliation of GAAP to non-GAAP measures is included in today's earnings press release. The earnings press release and an accompanying investor presentation are available on our website at investor.atmeta.com. And now I'd like to turn the call over to Mark.

**Mark Zuckerberg** (Executives):
All right. Hey, everyone. Thanks for joining today. This has been a busy and exciting few months. Our Family of Apps is now used by 3.64 billion people each day, and we are seeing all-time highs in engagement on both Facebook and Instagram, driven by strong growth in video. Threads has now overtaken X in monthly actives and continues to grow quickly. WhatsApp is hitting all-time highs in messaging and is becoming an increasingly important platform for agents as well.
In the last few months, we have had several major milestones towards our goal of delivering personal superintelligence to everyone. We had one of our most successful launches ever with the Muse personal agent. We shipped Muse Wonder as our first frontier model, and we shipped several new glasses and gadgets with Muse integration, including coming soon to our new audio glasses.
We've been discussing our vision for personal superintelligence for more than a year now. We want to help every person have an extremely capable personal agent that understands your goals and can help you achieve them and improve your life in whatever ways you want, whether that's improving your relationships, helping you save time, save money, build a business, create new things or anything else that you can dream of. Muse is the product form of this vision. So now we have the foundational technology in place to deliver this. There is still a lot of work ahead, but our initial position is very strong. 
In just 1.5 months, more than 10 million people in the U.S. and Canada have set up Muse personal agents. Growth continues to be strong, and we have been #1 in the App Store almost every day. Engagement and retention are also off to a strong start. About 25% of people who have set up Muse use it on any given day. For our earliest adopters, the longer that they use Muse, the better the retention seems to get. So to put this in perspective, this is more than twice the level that Threads started at or where we believe that other AI apps started at as well.
The most common use case for Muse is shopping, with more than 1/4 of people who are using Muse engaging in this with an average purchase size of over $200. Plaid told us that they hadn't seen activity like they're seeing with their connector on any other service before. And in the first week, we had to work with Stripe to raise credit limits since the volumes were above what any of us expected.
Beyond shopping, the most common connectors are for personal productivity and connecting Muse to your other services like email and calendar. Now this shows the importance of the Muse Secure VM that we've built to provide state-of-the-art privacy and security, and we are looking forward to following up soon with a Muse Confidential VM, which will make it so that even Meta cannot see your content.
We've also seen that Muse Wonder improves quality, engagement and retention further, which suggests that as we continue to improve intelligence, Muse will perform better and better over time. Now that Muse has clear product market fit, we are entering a new phase and a more operational phase that is focused on scaling it. The goals for this next phase play to many of Meta's strengths. We need to do 3 things: scale the product, grow revenue and optimize compute costs.
We expect to grow Muse to serve billions of people. This is both our mission and our strategy. It's our mission in that we believe in putting the power of personal superintelligence in everyone's hands. We believe that, that is the path to ensuring a positive future for everyone with individual empowerment as the source of prosperity and balance of power as the foundation for safety. On a values level, we believe that delivering this capability widely is the best thing that we can be doing. This is also our strategy because we think that billions of Muses in a network at scale will be able to get more done for people and businesses by working together. So we'd like to create a large-scale Muse network as quickly as possible.
From a business perspective, the average revenue per American user for our existing Muse users is -- sorry, for our existing Family of Apps users is several hundreds of dollars annually, and we expect that Muse will reach an even higher level over time due to the amount of commerce that we already see taking place. This will take some time, but we're starting to work on this now. Our business model will have a few components. For most people, the product should be free, and we will build commerce tools so we get paid a fee based on the transactions that we help facilitate. We expect this will be paid for by businesses.
For people who want the most advanced models or to use extra tokens, they subscribe directly and pay. For business owners who want additional features to use Muse to grow their businesses or for companies that want people to use Muse for work, they will be able to subscribe directly and pay as well. And for those who want Muse to help improve the personalization and quality of their content and ads across Meta, they will be able to connect to those experiences as well. Just to clarify, the average revenue that I was talking about before is the Family of Apps revenue for our existing Muse users.
On the compute side, we are building out the capacity to serve more than 1 billion people over the next few years. In the near term, Muse is very compute-intensive to run, but we expect to improve its cost efficiency by more than 10x in the next year, which will enable it to be profitable once the revenue lines are at scale. If compute efficiency continues improving quickly for another few years, which we think is highly likely, then Muse will be highly profitable over multiple years. In the near term, the strength of our core business enables us to scale the Muse network before then, and we believe that we are the best-positioned company to pursue this strategy.
One other note on compute economics is that since training is a large fixed cost, now that we have leading models, we want to serve as much high-margin inference demand as possible. That is why we are building the Meta Enterprise Platform led by CJ Desai. Muse Wonder and even more advanced models that we're training can serve additional high-margin services beyond the Muse network, including our API, Muse Code and other enterprise services.
A fundamental feature of our business is that we have many good uses for this compute. It is difficult to forecast the exact growth rates for the Muse network, for our Enterprise Platform, and for how Muse Wonder and beyond will accelerate our core business. But through building up multiple ways to deploy these advanced models, we increase the chances that one or more of them significantly outperforms our expectations.
Beyond serving other businesses, we have not yet found the limit of how effectively we can apply compute to accelerating our own core business. We have implemented an eval with Muse Wonder to improve how effectively it can autonomously improve our recommendations and ad systems. And as our upcoming models get even more advanced, I expect that we're going to see an increasing rate of improvement in these systems.
All right. Let's talk about the models now. Muse Wonder is state-of-the-art across many dimensions that matter for personal superintelligence. This validates the importance of training models ourselves to deliver the best experience. In addition to Muse, we have also seen that engagement per person in Meta AI has more than doubled since April when we started rolling out our new models. While Muse Wonder has been our most important release, I have been very pleased with our pace of execution here. In the last few months, we've shipped Muse Spark 1.2 and 1.3, and Muse Code, 2 open weights models with Muse Glimmer and Muse Spark Open, and also Muse Voice. 
Going forward, with the field advancing quickly, we plan to focus on both pushing the frontier of intelligence and distilling those models into much smaller and more efficient product models that will be optimized for personal agents. My view is that we will be able to build superintelligence through scaling, so we are methodically working our way up the ladder there. We are already working on larger models after Muse Wonder, and they're going to be very impressive and capable. We are also working on new smaller models that are coming out soon that will deliver Muse Wonder-level intelligence more efficiently. 
Moving on. Our work on personal superintelligence is now also the focus of Reality Labs. Muse is coming to Meta Glasses starting next month, and that will be an important step towards this. People already love many features of the glasses already, music, calling, capturing moments, hearing assistance and more. But over time, we expect Muse and having your personal superintelligence with you throughout the day will be the most important part of the experience.
Muse is also central to the business model for the glasses. Again, our mission and strategy are to serve everyone here. We believe in putting the power of this technology in everyone's hands. So we have priced our devices, not to make a large profit on the hardware, but to build a large software and superintelligence business on top of them over time. Glasses sales continue to grow rapidly, and now with Muse, we expect that paid subscriptions will increase and that this business will begin improving meaningfully from here.
I also shared at Connect that we are changing our approach to virtual reality to only ship new devices when we have major breakthroughs like we had with the Meta VR Glasses this year, which, of course, are the first VR experience ever in a pair of glasses. I continue to believe that the path to delivering holographic experience of bringing together the physical and digital worlds in everyday glasses will come through VR first, but we will pace this aspect of our investment more to focus on delivering personal superintelligence first. So with these factors combined, we expect that the P&L of Reality Labs to improve from here with operating loss coming down to around $15 billion next year and trending towards profitability from there. 
Before we conclude, I want to spend a moment on the sheer velocity that we are seeing. An important part of our approach has always been to move fast so we can learn quickly and serve people better at scale. But recently, things have accelerated. In the last year, we shipped Edits, and it has already passed 50 million actives. New apps like Forum and Seller were built by small teams and are scaling quickly to serve power users. Muse went from an idea on a whiteboard to a successful product in just about 8 months. And we're about to ship Muse Charm, which will have gone from concept to a hardware device in people's pockets in less than a year.
I am proud of what we are building. People have all kinds of different opinions about the future, but at Meta, we believe that the future is for everyone, and that putting power in people's hands is how we get there. I think that this matters. There needs to be a company out there that represents these ideas. But this isn't just about ideas, it's also about execution. So I am grateful for everyone who is working so hard to deliver all of this to billions of people around the world. And as always, thank you to everyone who is on this journey with us. And now here's Susan.

**Susan Li** (Executives):
Thanks, Mark, and good afternoon, everyone. Let's begin with our segment results. All comparisons are on a year-over-year basis unless otherwise noted. Q3 total Family of Apps revenue was $64.2 billion, up 26%. Q3 Family of Apps ad revenue was $63.1 billion, up 26% on both a reported and constant currency basis. In Q3, the total number of ad impressions served across our services increased 10%. Impression growth was healthy across all regions, driven by growth in engagement and users as well as ad load optimizations. 
The global average price per ad increased 14% year-over-year, driven by ad performance gains and improvements in macro conditions relative to Q3 of last year. This was partially offset by strong impression growth, particularly from lower monetizing surfaces and regions. Family of Apps other revenue was $1.1 billion and grew 59%, driven primarily by WhatsApp paid messaging and subscriptions revenue. Within our Reality Labs segment, Q3 revenue was $443 million, down 6% due to lower Quest headset sales, which were partially offset by continued strong growth in AI glasses revenue.
Moving now to our consolidated results. Q3 total revenue was $64.6 billion, up 26% on both a reported and constant currency basis. Q3 total expenses were $51.6 billion, up 68% compared to last year and included a $9.9 billion charge related to the August 2026 multistate attorneys general agreement. Year-over-year growth was primarily driven by legal-related costs, infrastructure costs and third-party AI token costs. The growth in infrastructure costs was driven by higher third-party cloud spend, depreciation and data center operating costs. We ended Q3 with over 66,000 employees, down 12% from Q2 following the May 2026 head count reduction.
Third quarter GAAP operating income was $13 billion, representing a 37% decline year-over-year and a 20% operating margin. Excluding the Q3 legal charges related to the aforementioned legal settlement, our third quarter operating income would have increased 11% year-over-year. Our tax rate for the quarter was 24%, above our outlook range, primarily driven by the nondeductible portion of legal expenses. Net income was $9.9 billion or $3.83 per share.
Capital expenditures, including principal payments on finance leases, were $34.9 billion, driven by investments in servers, data centers and network infrastructure. Free cash flow was negative $2.1 billion. We ended the quarter with $82.4 billion in cash and marketable securities and $83.7 billion in debt. 
Turning now to the business performance. There are 2 primary factors that drive our revenue performance: our ability to deliver engaging experiences for our community and our effectiveness at monetizing that engagement over time. On the first, we continue to see significant gains from our content recommendation initiatives. On Instagram, global time spent per user reached an all-time high and grew double digits year-over-year in Q3, with strength across both Reels and Feed. On Facebook, Reels time spent reached all-time highs both globally and in the U.S., with both growing double digits year-over-year. Threads also continued to scale, with time spent per user growing over 20% year-over-year. Engagement gains across our services continue to be driven by improvements we're making to the relevance, personalization and timeliness of the content we recommend.
Investments into our recommendations engine across retrieval and ranking have continued to yield positive results on Instagram and Facebook. For instance, on Instagram Reels, our relevance launches in Q3 increased Reels time spent by over 4%, driven in part by our upgraded model architecture that ranks sequences of reels at a time instead of evaluating each reel independently as well as improvements we made to add richer watch time signals.
On Facebook Feed and Reels, we completed the global launch of a new generative retrieval architecture, which, inspired by LLMs, labels pieces of content with semantic representations and generates potential recommendations, helping our systems surface relevant new posts before they've accumulated significant engagement. This new architecture is now rolled out to roughly 1/4 of unconnected Feed views and half of Reels views and increased Reels watch time by 1%.
Our recommendations work is also helping us deliver fresher and more personalized content. Nearly 45% of recommended Instagram Reels are now less than 1 day old, up more than 11 percentage points from Q2. On Facebook Reels, we doubled the amount of history our ranking model can consider, driving a 1% increase in Reels watch time in the U.S. LLMs are also helping us understand content more deeply. We continue to process public Instagram posts each day through LLM-based content understanding systems. These signals have improved the engagement with Instagram search results by 1% through the end of this quarter.
This quarter, we also began moving our content understanding models onto our first-party Muse model family. In offline evaluations, these models are outperforming our prior production models and are reducing per-unit content processing costs by more than 80% across Instagram, Threads, Facebook and ads. Beyond improving quality, owning more of this stack gives us greater flexibility to develop models around the signals that matter the most for personalization.
Turning to the second driver of our revenue performance, increasing monetization efficiency. We see significant opportunity to continue improving performance for the businesses who use our services. Within our ad systems, we are continuing to drive performance gains as we deploy more predictive models that understand users more deeply and deliver ad experiences better aligned with their unique preferences, while also making our infrastructure more efficient. Last quarter, we introduced Meta Generative Recommender, which uses LLMs to reason across ad content and user preferences to predict the best ad for each person.
In Q3, we launched this approach to generative retrieval on Facebook Feed, driving a nearly 2% increase in conversions across targeted segments. In addition, we expanded our GEM model for ads ranking to additional services -- surfaces, driving a 1% -- 1.7% increase in conversions for off-site conversion campaigns and a 9.6% increase in app ad conversions. And we continue to scale our retrieval systems efficiently. In Q3, improvements to Andromeda, such as scaling model complexity and throughput, increased conversions by 1.4% on Facebook. We're also leveraging AI to make it easier for businesses to manage campaigns, develop creative and act on performance opportunities.
Meta AI business assistant is becoming a more proactive and capable partner for advertisers. We estimate that advertisers who adopted its recommendations drove almost 5% more conversions at the same cost per conversion and increased their advertising investment by 9% compared with similar nonadopters. We are rolling out additional capabilities, including creative insights, stronger business context and more agentic actions. These features will allow marketers to plan, create and optimize campaigns as well as schedule tasks and alerts through a conversational experience with approvals and previews that keep them in control.
I'll share one example of how Meta AI business assistant is empowering our advertisers. Simply Organic Maple, a family-run maple syrup producer in Vermont, used Meta AI business assistant to improve its campaign messaging. After the business assistant recommended testing longer, more descriptive advertising copy, the business saw a 57% increase in purchases and a 36% reduction in cost per purchase. Its strongest revised ad delivered a 3x return on ad spend, a 52% improvement from the original.
Adoption of our generative AI ad creative tools also continues to scale. In Q3, nearly 10 million advertisers used at least one of these tools. Advertiser adoption of our video generation features grew 25% quarter-over-quarter, driven in part by ready-made videos that reduce generation time to just a few seconds from a single image upload. We're also expanding the opportunity at the intersection of creators and advertising. Partnership ads, which allow advertisers to run ads with creators, brands and other businesses, continued to scale rapidly in Q3. Our partnership ads product grew over 97% year-over-year and surpassed $15 billion in annual revenue run rate.
In Q3, we also completed the global rollout of Creator Marketing Hub to all advertisers, bringing creator discovery, content organization and partnership ad activation into one place with more than 10 million creators now discoverable. We are integrating Meta AI business assistant into the hub so advertisers can conversationally search for creators, identify content to use in partnership ads and get guidance across their creator marketing workflows.
Outside of ads, we are also building out additional ways to monetize engagement across our ecosystem. In September, we announced the global expansion of Meta One, our unified subscription service for consumers, creators and businesses. Meta One is rolling out gradually with more than 50 features across Instagram, Facebook and WhatsApp, including Meta Business Agent and Meta AI, and has surpassed 15 million subscriptions and trials to date. The core experience across our apps and Meta AI will remain free, while subscriptions offer more specialized capabilities and expanded AI usage.
And beyond monetizing engagement across our existing services, we are building new experiences and revenue streams around consumer agents. Mark highlighted the impressive early momentum with Muse. Users have found many reasons to use Muse, with the top 3 categories being shopping, personal productivity and creativity. We're encouraged by the breadth of use cases, with shopping in particular being used by over 25% of Muse weekly actives.
While our near-term priority is to grow adoption and expand Muse's reach, we see multiple paths to monetization, beginning with subscriptions. We also see a significant opportunity to extend Muse to small businesses. Based on a recent user survey, we estimate that at least 500 million self-identified small businesses use Meta's Family of Apps to reach customers and generate revenue. Muse could help these businesses acquire customers and operate more efficiently while helping people complete transactions. Over time, consumer and business agents could connect and transact directly, creating opportunities around paid usage, commerce and business services.
Alongside growth, we are focused on building sustainable unit economics. Muse's compute intensity means that expanding its user base will require significant investment, and we expect total serving costs to rise. At the same time, we expect to improve compute cost efficiency by more than tenfold over the next year, driven by better utilization of off-peak capacity, more efficient models and inference optimization. As revenue scales, these efficiency gains give us confidence in our ability to build a highly profitable business over time. 
Moving now to our financial outlook. We expect fourth quarter 2026 total revenue to be in the range of $73 billion to $76 billion. Our guidance assumes foreign currency is an approximately 1% headwind to year-over-year total revenue growth based on current exchange rates.
Turning to the expense and CapEx outlooks. We are raising our expense outlook to incorporate the $9.9 billion charge related to legal proceedings recognized in Q3. We now expect full year 2026 total expenses to be in the range of $175 billion to $179 billion. Excluding the Q3 legal charge, we continue to expect 2026 operating income to be above 2025 operating income. At a segment level, we now expect Reality Labs losses to decline compared to 2025 to a range of $18 billion to $19 billion.
We anticipate 2026 capital expenditures, including principal payments on finance leases, to be in the range of $135 billion to $145 billion, narrowed from our prior outlook of $130 billion to $145 billion. Absent any changes to our tax landscape, we expect our fourth quarter 2026 tax rate to be between 15% and 17%. Additionally, we continue to monitor active legal and regulatory matters that could significantly impact our business and financial results. For example, we continue to see scrutiny on youth-related issues in several markets and have a number of youth-related trials scheduled in the coming months in the United States.
Looking beyond 2026, we are still developing our budget and capacity plans for next year, but we expect to continue investing aggressively to support both our core business and emerging AI initiatives. Our current capacity and what is scheduled to come online gives us the flexibility to allocate resources across model training, core business growth and the development and support of new products.
Our AI investments are already delivering substantial incremental advertising revenue through stronger engagement, better recommendations and more efficient monetization. Building on this progress, our MSL investments are creating the technology and infrastructure needed to unlock significant new revenue opportunities and strengthen capabilities across the business. While these investments will take longer to generate returns than those in our core business, the breadth of monetization opportunities and internal efficiencies gives us confidence in their long-term potential. 
Looking ahead, although we are not providing a full year 2027 revenue outlook, the benefits our AI investments are delivering to the core business, combined with emerging opportunities from model advances and product launches, position us to sustain strong overall revenue growth throughout 2027. Separately, we remain focused on improving Reality Labs profitability. As Mark mentioned, we expect losses to narrow next year to around $15 billion as we reallocate investment towards other priority areas, primarily AI.
Finally, today, we announced plans to create a new class of nonvoting capital stock, which will be distributed to all existing shareholders through a stock dividend. For each existing share held, stockholders will receive one share of the new nonvoting stock, effectively resulting in a 2-for-1 stock split. We expect trading to begin in late January 2027. In closing, our business momentum continued in Q3 with strong execution across our core ads and engagement initiatives, and we're also excited by our progress towards bringing personal superintelligence to everyone. With that, Krista, let's open up the call for questions.

**Operator** (Operator):
[Operator Instructions] And your first question comes from the line of Brian Nowak with Morgan Stanley.

**Brian Nowak** (Analysts):
I have 2, one on Muse, one on enterprise. Maybe, first, congrats on the success of Muse. But as you analyze the user behavior and the product, can you talk with us a little bit about any of the constraints to the slope of forward user growth that you're most focused on addressing, whether it's capabilities, model efficiency, capacity, et cetera, just so we understand what are the limiting factors to forward user growth that you want to address? And the second one is on enterprise. Mark, can you just sort of walk us through your vision for the Meta enterprise product offering and the key value drivers you hope to provide for the enterprises adopting the service?

**Mark Zuckerberg** (Executives):
Yes, I think I can talk about both of those, and then Susan can jump in with anything else. All right. So right now for Muse, we are -- and one of the things I pointed out is we have more than 10 million people in the U.S. and Canada who have set it up, but I think one of the biggest constraints so far is that because this is a compute-intensive service to run, we have not launched it globally yet. That's partially because of wanting to optimize it for each place, and there's some work around connectors for that. But it's partially that we want to make sure that we do this efficiently.
So I mean, there's pros and cons there. The pro, of course, is that, that just makes it even more impressive that you have 10 million people using it and signing up to use it in the first 6 weeks because those are all kind of Americans and Canadians in a small number of markets. So if we actually did roll it out more broadly, then you would expect that number to be significantly larger than what we're seeing today. But then on the flip side, we actually have to go do the work to bring the efficiency in line to make that make sense. 
And so that's a big part of it that we need to do. We -- the compute efficiency work is going to be important on this also because we want to make sure that we've built enough compute to be able to serve what we think is going to be 1 billion plus people if we can achieve certain compute efficiency targets, but we obviously have a lot of work to do there as well. And that'll be one of the limiting factors over the next year. We want to build out the business around it. I mean I talked about that, and I think doing that in tandem with bringing down the compute -- or increasing the compute efficiency is going to be important for getting this to work from a business perspective, which I'm optimistic about. But I think that that's one of the things that we need to do. 
And then there's just continuing to increase the value in the product, which I think we will largely do by continuing to develop new models. That's why I mentioned that we launched Muse first on Muse Spark, and that's what is currently the default across the free tier. And we rolled out Muse Wonder, and people can access that in the paid tier today. And we know that it performs a lot better, so we're working on getting a more efficient version of Muse Wonder that we'll be able to roll out more broadly. But you can imagine just as we iterate forward in 2, 3 models into the future, when you have significantly higher intelligence and capability to solve many more problems for people and the ability to deliver that at a much more affordable price point, I think that that's going to just unlock a lot more value to people. So we're very excited about that.
Transitioning to talking about the enterprise piece because I think that these 2 pieces, there is some connection here, in that the main enterprise offering in the near term is going to be the model API and Muse Code. We have business agents that we've been scaling for a while, and each of those 3 things is growing quite quickly, so we're excited about that. Over time, we would like to make it so that we have a whole kind of business network of Muse agents as well. There's the business agent, which we've talked about on previous earnings calls for businesses to help out with sales and customer support.
But what we see is a lot of people are actually using Muse today to help run especially small businesses. And we think that there's both an opportunity to help create an agent that people use to really enable them to automate and do a lot of the parts of spinning up a small business that are just kind of difficult and time-consuming but aren't the core thing that a person is trying to do. So we think that's a big deal.
And then making a version of Muse that people can bring into different corporate environments and work there, we think is going to be a big deal. And then beyond that, building what I refer to as the Muse network, which is making it so that Muse is not just a kind of single-player game where you have your Muse, but making it so that your Muses can work with your friends and your families. And if you want to buy something, it's not just navigating to that business' website, it's talking to their agent. I think that getting that all to work well together is going to unlock tremendous value at scale.
So I'm very excited about all of that. I think the enterprise use is going to be a big part of it, but it's also going to kind of have this very valuable boost in the utility for consumers, too. So I'm very excited about both of those.

**Susan Li** (Executives):
I would add on to Mark's comments on enterprise. AI is creating huge amounts of disruption in enterprise today. And we don't -- from what we can see, we really don't believe that traditional enterprise companies have this locked down. And in fact, some of the leading companies in this space today didn't exist a few years ago. Those companies made large investments in model development, and we've done the same, and we have increasingly competitive models to bring to bear for the benefit of all of our users, including small businesses and including enterprises. And already today, we have 500 million businesses using our product.
So we really believe that AI is going to reshape how businesses operate. We expect that businesses of all sizes are going to use AI agents across software development and productivity, sales, marketing, consumer -- customer service, et cetera. We have differentiated assets to serve this market, bringing together models, infrastructure, global distribution and long-standing relationships with businesses. And it's our hope that this will be able to be a new diversified recurring revenue stream for us that will be able to support multiple business models, including subscriptions and usage-based API and messaging and other revenue lines. So we expect that this will be an opportunity that will develop over multiple years, and we intend to scale our investment behind demonstrated customer demand and product market fit in this area.

**Operator** (Operator):
Your next question comes from the line of Eric Sheridan with Goldman Sachs.

**Eric Sheridan** (Analysts):
Maybe just the first one building on Brian's question, when you think about the friction points around agentic commerce, how do you guys as a company think about solving for friction that's rising where there are aggregators or suppliers that don't want agents to interact with their platforms or their services, and how you think about lowering that friction or creating the right balance between the existing services that consumers access today relative to how this might all be changed or altered by agentic behavior over the medium to long term?
And the second one would be with the announcement of the new class of shares tonight with earnings, any updated thoughts broadly about how you think about sources of capital and optimizing your capital structure to make sure you invest the proper amounts to capitalize on the opportunities that AI are presenting in the next couple of years?

**Mark Zuckerberg** (Executives):
I can answer the first one. So -- okay. So the question -- sorry, what was the first question there?

**Susan Li** (Executives):
Friction points around agentic commerce.

**Mark Zuckerberg** (Executives):
Yes. Got it. All right. Yes. So the -- right now, what we're seeing is that, overwhelmingly, businesses are very excited about enabling this because they recognize that it's going to be a new opportunity for them not only to increase the sales and the quality of the experience for existing customers, but also potentially to bring in new customers.
So now I mean, across the whole business ecosystem, different people will kind of adopt this at different paces and how our strategy evolves on that to develop the ecosystem will depend on how that goes. But overall, I would say we've been very positively surprised by how quickly, I think a huge amount of businesses have wanted to not only figure out how to make it so that Muse can use their services more effectively but have reached out to us to integrate around it. So I view that as a very good sign.
And obviously, not everyone wants to be an early adopter. That's fine. We'll work with folks on the terms that makes sense for them. But I do think that, over time, this is going to be quite valuable for everyone to make this work well, and I think we're on a good trajectory on that so far.

**Susan Li** (Executives):
Yes. I would add to that, and I will also answer your second question and just say, I think agents are going to be an important part of how reality evolves, and I think everyone is going to have to adapt to what that means, the new age of agentic commerce. We obviously have had a lot of businesses who are very excited to partner with us. There are also businesses that are understandably focused on protecting customer relationships. And we expect the market, I think, ultimately to evolve away from agents attempting to navigate every digital experience like a human. And I think over the long run, this will move towards more permissioned, structured interactions, and that will include authenticated APIs, approved agent partnerships or direct communications between a consumer's personal agent and a business' own agent.
And we're helping establish the standards needed to support that model. Earlier this month, we previewed the Personal Agent Protocol, an open standard across Muse and Meta Business Agents that we are developing with industry partners like Sierra, Walmart, Stripe, Shopify, et cetera. The protocol is intended to define how a consumer's personal agent can interact securely and reliably with the business' agent and preserve appropriate controls for both the business and customer. So again, I think adoption will likely be uneven and will take time, and in the near term we expect any experience -- many experiences will remain AI-assisted rather than fully autonomous. But as trusted integrations develop and agents demonstrate that they can generate incremental value and demand and operate safely, we expect that more and more businesses will be excited to participate.
Your second question was about the announcement of the new class of shares. So I should say, we created this new class of shares with the purpose of creating a publicly traded nonvoting stock usable for capital raising, employee compensation, acquisitions, other general corporate purposes while preserving the voting power of existing Class A and B shareholders. We believe the share class will maintain our founder-led structure. It will expand our funding tools and give us flexibility to invest behind the unprecedented momentum we're seeing across every part of our business driven by AI. We don't have any specific financing plans to announce at this time, but we thought it was prudent to establish the appropriate capital structure framework to ensure that we have access to a diverse pool of funding sources.

**Operator** (Operator):
Your next question comes from the line of Doug Anmuth with JPMorgan.

**Douglas Anmuth** (Analysts):
I have 2. First, just wanted to follow up on the -- your last comment, Susan, just around as Muse evolves and more businesses adopt agents, just wanted to get your sense of how things kind of change and shift as you go to more permission-based and agent-to-agent transactions. And like what does that really unlock over time?
And then secondly, just on kind of expenses and CapEx, thinking about '27, I know you're not really there yet, but if I go back to some previous comments, you've talked about maximizing compute in '26 and '27 and then having more flexibility in '28. A year ago, you talked about kind of notably larger dollar increase in '26 than '25, and then you've also used kind of growing operating income on an annual basis as well. So I'm just curious if there's any of those that you can kind of tie or to help us think about '27.

**Susan Li** (Executives):
Thanks, Doug. So on your first question about how the agentic ecosystem evolves, I wish I could sort of predict that more perfectly. And I think it will take some time. And again, I think it will be a little uneven. But I definitely think that, when I use Muse today, it's clear that there are a lot of parts of the experience that would be even better if Muse was able to interact more seamlessly with business agents on the other side. For example, when -- if Muse has to call a business on my behalf, I think it would be easier for the business if that call was handled by business agents that were representing it.
And I think also one of the things that is really distinctive about Muse, and one of the things that makes the product experience so great, is the degree of proactivity that it exhibits on my behalf, right? I can give it a task and Muse is going to go execute against that task for me, even as it encounters some obstacles or can't quite find the right thing and needs to chart a new path to helping me look for the thing I want.
And so I think the -- that sort of dimension of proactivity exhibited by either consumer agents or business agents, I think, are going to enable more transactions to happen or more activity to happen broadly than happens today where -- when things are -- when more actions are taken, primarily -- when like the latent demand expresses itself versus things where I can have Muse searching for things for me on an ongoing basis, giving me regular updates on things I'm looking for, sending me 10 new books a month. And agent should be doing similar things for businesses, and I think that creates sort of opportunities, again, for a new, more proactive sort of framework for what agent-to-agent interactions look like over time.
On your second question, which is about 2027, we are quite early in developing our budget and capacity plans for next year. So we are, I would say, at the point where we are both investing -- sorry, evaluating a lot of investment proposals that have attractive return profiles over different time horizons, and we want to figure out how we can fund as many of those as possible within the construct of our overall budget and financial goals. But it's very dynamic and it's still pretty early. And so we don't have anything more specific or quantitative to share until we get to the Q4 call, which is typically when we share guidance for the next year.

**Operator** (Operator):
Your next question comes from the line of Justin Post with Bank of America.

**Justin Post** (Analysts):
Great. One for Mark, one for Susan. Mark, you've got this powerful new model on your hands, and it seems like there's a lot you could do internally besides externally. But specifically to the ad business, you've rearchitected your systems around AI. How much room is there for improvement as you deploy that new model? How are you thinking about that? And then for Susan, you mentioned strong revenue growth next year. Just wondering if that's advertising or does that incorporate some incremental AI revenues hitting next year?

**Susan Li** (Executives):
I'm happy to take both of those. Great. On your first question, I think our ads business has been benefiting for now many years from our ongoing investments in both kind of what we would have called traditional AI machine learning models, and then, of course, from the sort of more recent generation of models. I would say that there are 3 themes there that I think are worth outlining. The first is just the kind of traditional road map of performance improvements that we have in the pipeline based -- that is what I would describe more as business-as-usual machine learning work. That continues to be a robust and healthy pipeline. And as we are looking into 2027, again, we're not providing an outlook, but I would say that our investments and product improvements across both engagement and ads initiatives give us confidence that we have meaningful runway to grow our core business throughout 2027. That also gets to your second question also. But I should say, basically, I think the ranking and recommendations pipeline is healthy.
The second theme I would say is that we are excited about some of the new research bets that we have as we move into sort of a more LLM-oriented AI infrastructure to help us more deeply reason about people's preferences, what they're interested in, both across organic content and recommendations, and we expect that we will be able to unlock benefits to our ranking and recommendations engine from that research, too.
And then the third thing is that we expect that generative AI tools, which have already been very valuable for advertisers, will continue to grow in terms of the features that we make available to advertisers, primarily through the Advantage+ suite but features that make it easier for advertisers to quickly and seamlessly generate, whether it is creative or take an image and generate video or generate sound, all, I think, in service of making the ads increasingly personalized for the person that they're being served to. So I would say we feel like there is meaningful runway across all 3 of those things.
Your second question was about revenue growth next year, and so as I mentioned, I think we're both feeling good about the budget investments that we expect we will make in both core ads and engagement initiatives next year. We're also building several new AI businesses, and we expect that those can begin contributing incremental revenue in 2027, but more importantly, can scale meaningfully over time. And those will include monetizing our AI products through subscriptions, transactions, advertising, developing enterprise offerings, as we talked about in one of the earlier questions. 
So I would say while many of these opportunities remain early and our near-term focus is really on building high-quality products and achieving product market fit and scaled product market fit, I think our track record of reaching billions of people and building businesses at scale makes us feel good that AI is going to become a meaningful source of revenue diversification over time.

**Operator** (Operator):
Your next question comes from the line of Mark Shmulik with Bernstein.

**Mark Shmulik** (Analysts):
Mark, coming out of Connect, it kind of felt like we were ushering in the next era of the company and the business reorienting around kind of Muse at the center of everything. Is that a fair assessment of kind of how things are going internally? And if so, can you just talk a little bit more about how some of the business mandates and outcomes may have changed?
And then, Susan, it was interesting to kind of see the launch cadence where enterprise announcements kind of preceded some of the small business ones. And I appreciate your comments on some of what's going on there around the SMB agent opportunity, but can you just share more details on kind of the work required to serve and scale the offerings to SMBs?

**Mark Zuckerberg** (Executives):
Yes. I mean I can talk briefly about the first one. I mean, look, it was more than a year ago that I think I wrote the letter about personal superintelligence as the North Star for the work that we're doing here. And it basically -- it fits with this line of work that we've done for more than 20 years at the company that is focused on empowering individuals, giving people a voice, giving people the tools to connect in the ways that they want. And when you extend that to the work around AI now, we think that the most important thing that we can be building for this next generation of technology is giving -- is basically putting the power of this technology in everyone's hands, which is the personal superintelligence vision.
So we've been working on this for a while, and this is when we did the reboot around MSL and building the lab. A lot of it was this idea that we need to build models specifically to be good as personal agents, that we'd be able to build the best experience by owning and building and designing ourselves the end-to-end technology. So that includes the models and then the agents. And this has been -- this has kind of been in the works for a while.
I mean, the vision around the glasses has also been this. I mean the -- we've wanted to build the next generation of hardware platforms so that we can deliver the best end-to-end experiences to people. And I think that that's starting to come together as well, and I think will even more over the coming years. I mean these are long-term bets. I feel like this is what we're here to do, is make long-term technology bets and design the best experiences end to end that we can for billions of people around the world. And I think as long as we continue to do that, then over time, the business takes care of itself, as long as we continue executing well, which I'm really proud of the team for how we're doing on that.

**Susan Li** (Executives):
Thanks, Mark. Your second question was around Muse for small business. So we launched that, which you can think of as an expansion for Muse in late September. Rather than a separate product, it's kind of a new -- a set of new skills and connectors inside the existing Muse app aimed at helping SMB owners run operations, find new customers. It connects to a business', for example, Instagram account analytics or Facebook pages or Meta ad accounts in a few clicks, along with dozens of third-party connectors that businesses already run on, like Shopify, QuickBooks, Canva, et cetera. It already understands what businesses sell, its brand voice, what customers are asking for. 
And Muse can take actions, including analyze ad and content performance, draft campaigns, customer responses, flag issues, and we are actively listening to our SMB users to understand what their top use cases are. We are seeing them use it for ads optimization, for direct message organizing, use it to expand their sales footprint, to keep their website current based on things like inventory and new products, to deal with employee load balancing. So we're pretty closely following how businesses use Muse to make sure that we are being thoughtful about new features that we release in Muse to make it maximally useful and productive for SMBs. 
I'd also say we have unique touch points to, again, I mentioned in my opening remarks, 500 million self-identified small businesses, and we think that many of the investments that we make in consumer products are going to carry over to help power those businesses also. We have multiple excellent channels to surface those opportunities to small businesses globally. So this is a place where we feel like we have an existing extremely strong platform, and we're very excited about it. And we also believe the transition to AI has broadly unlocked enterprise as a new opportunity for us as well.

**Operator** (Operator):
Your next question comes from the line of Ross Sandler with Barclays.

**Ross Sandler** (Analysts):
Great. Mark, you touched on this earlier, but could you elaborate a little bit on maybe some high-level metrics around the per-user cost structure of Muse today, and then how you kind of see that cost curve coming down as you go forward? And what are some of the things you're doing to bring that cost curve down?

**Susan Li** (Executives):
I'm happy to answer that. And Mark, you should add anything that you feel like I'm missing. We are -- we don't have sort of specific numbers to share around the cost structure of Muse today. But of course, it is, as Mark said, pretty compute expensive, and making sure that we are focused on compute efficiency is going to be one of the key vectors towards being able to both scale Muse and grow it into the business that we want.
I think there are a couple dimensions of achieving that efficiency. I think some of the more nearer-term pieces include things like leveraging off-peak or spare computing capacity to run some sets of jobs using smaller models. There's a lot of work to be done across different inference efficiency initiatives, like all in service effectively of higher GPU utilization and other product efficiency work we can do also.
And I think over the longer term, I think this is a place where we expect that we're going to be able to, over time, as LLMs scale, get more tasks done with fewer tokens and also rely on AI models themselves to help us improve the efficiency of the software that we use to run the model. So I think it's a place where we both feel like there is a lot more work on our efficiency road map that is going to help us bend the curve here. And we also expect that the sort of arc of how the sort of AI-driven technological advances are going to apply here will also help us achieve larger savings over time.

**Operator** (Operator):
Your next question comes from the line of Mark Mahaney with Evercore ISI.

**Mark Stephen Mahaney** (Analysts):
Two questions. There's a bit of a playbook, or there has been at Meta over the years when you surface new surfaces and you build up the user growth engagement, then you layer in monetization. Do you think it's sort of a similar playbook here? Or does it have to be a little bit faster with Muse just given that the costs associated with it are materially greater arguably than launching those surfaces in the past? And then just a clarification on that commerce data point that you provided about 25% of users and the $200 or greater ASP. Are you including in commerce travel purchases? Or is that just a retail data point?

**Mark Zuckerberg** (Executives):
My guess, I think that we are going to work on monetization somewhat sooner on this than our normal playbook for a couple of reasons. One is just the size of the numbers that we're talking about in terms of both the costs and the opportunity, I think make it kind of important to make progress on that in order to be able to scale it. The other is just that such a large part of what people are doing is commerce.
And to your question, that does include travel, too. I think we might consider travel a different case, but travel is actually one of the other top use cases for Muse, is basically people planning that out and planning different kinds of things that they would get than they might get through our Family of Apps. So I think that this is going to be an important thing for us to work on to deliver the consumer value that people want. And in doing so, I think we will be able to build a model where we get a percent of the value that we are helping to create for people. So I think that that's going to be -- it's going to be very important to kind of get the math on all of this to work out, so that way we can continue the compute build-out that we want to build in order to get this to reach everyone at scale.
And in addition to everything that Susan said in response to the last answer, I would also just add that like we just see this trend that year-over-year, I just expect that we will be able to deliver the same intelligence that we have now in Muse Wonder or, frankly, any of the current frontier models at a fraction of the cost in a smaller model a year from today. So to the extent that, that represents some kind of baseline level that people seem to -- that kind of is sufficient for product market fit for Muse, I think that we will just continue through kind of continued model development, make progress on that efficiency.
The thing that is -- and of course, less clear, is that I don't think in a year from now, most people are going to want to use the current model level of intelligence because that's also going to make progress. So I think we're going to need to work on all of these things, both the revenue pieces of it and scaling the different aspects of that as well as progressing on the model development and all the efficiency in order to be able to both fund and support the compute build-out and reach billions of people, which, again, we want to get to that as soon as possible.
Part of the reason why we're not just charging everyone upfront to use this is we want to establish this Muse network, and we think that it's going to be more valuable for people at scale when there are a lot of people and businesses using Muse, so that way they can collaborate and work together. I think that that's really a very important state to get to and one that we're quite excited about. And again, I don't think that there are many companies in the world that are well situated to be able to do that in the way that we are. I think we are very well situated to do that, and we plan to push on that quite aggressively.

**Operator** (Operator):
And that does conclude our question-and-answer session. Mr. Bevegni, I would like to turn the call back over to you.

**Rob Bevegni** (Executives):
Thank you for joining us today, and we look forward to speaking with you again soon.

**Operator** (Operator):
And ladies and gentlemen, this does conclude today's conference call. Thank you for your participation, and you may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### META_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜Susan Li (CFO)｜guidance：Q3 2026 總營收財測 $61–64 十億美元（原話："$61 billion to $64 billion."）
- 2026-07-29｜Susan Li (CFO)｜guidance：Q3 財測假設匯率約 1% 逆風（原話："Our guidance assumes foreign currency is an approximately 1%"）
- 2026-07-29｜Susan Li (CFO)｜guidance：2026 全年總費用指引 $165–169 十億美元（下限上調以納入 Q2 法律費用）（原話："in the range of $165 billion to $169 billion."）
- 2026-07-29｜Susan Li (CFO)｜guidance：仍預期 2026 營業利益高於 2025（原話："We continue to expect to deliver operating income this year"）
- 2026-07-29｜Susan Li (CFO)｜guidance：2026 資本支出指引 $130–145 十億，自原 $125–145 十億收窄（原話："to be in the range of $130 billion to $145 billion"）
- 2026-07-29｜Susan Li (CFO)｜guidance：其餘季度稅率預期 15%–17%，原為 13%–16%（原話："an increase from our prior outlook of 13% to 16%."）
- 2026-07-29｜Susan Li (CFO)｜risk：管理層點出青少年議題訴訟風險（原話："scrutiny on youth-related issues in several markets"）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 營業利益排除法律費用與資遣費後的口徑（原話："Excluding the Q2 legal charges and severance expenses"）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 總費用年增 55%，含 24 億美元法律費用（原話："up 55% compared to last year and included $2.4 billion"）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 含 12 億美元資遣費（5 月裁員）（原話："$1.2 billion in severance expenses"）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 年底員工數超過 7.5 萬人，較 Q1 減 3%（原話："We ended Q2 with over 75,000 employees, down 3% from Q1."）
- 2026-07-29｜Susan Li (CFO)｜margin：Q2 自由現金流僅 7.84 億美元（原話："Free cash flow was $784 million."）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：Q2 資本支出金額（原話："were $31.1 billion"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：期末現金與有價證券（原話："$90.3 billion in cash and marketable securities"）
- 2026-07-29｜Susan Li (CFO)｜customer：Q2 廣告營收與年增（原話："Q2 Family of Apps ad revenue was $59.4 billion, up 27%"）
- 2026-07-29｜Susan Li (CFO)｜customer：廣告曝光量年增 14%（原話："the total number of ad impressions served across our"）
- 2026-07-29｜Susan Li (CFO)｜customer：每則廣告均價年增 12%（原話："The global average price per ad increased 12% year-over-year"）
- 2026-07-29｜Susan Li (CFO)｜product：FoA 其他營收首度達 10 億美元，主要來自 WhatsApp 付費訊息與訂閱（原話："other revenue reached $1 billion and grew 73%"）
- 2026-07-29｜Susan Li (CFO)｜product：Reality Labs Q2 營收 4.31 億美元，AI 眼鏡成長（原話："Q2 revenue was $431 million, up 16% year-over-year"）
- 2026-07-29｜Susan Li (CFO)｜product：Advantage+ 年化營收規模（原話："continue to grow, reaching over $75 billion in"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜competition：CEO 稱其廣告業務美元成長速度為同業最快（原話："reporting faster year-over-year revenue growth than any"）
- 2026-07-29｜Susan Li (CFO)｜product：Reels 排名改善帶來 Instagram sessions 提升（原話："drove a 15 basis point increase in sessions on Instagram"）
- 2026-07-29｜Susan Li (CFO)｜product：Facebook 廣告模型改善數據（原話："8.3% increase in ad clicks and a 15.7% uplift"）
- 2026-07-29｜Susan Li (CFO)｜product：推出 Meta Generative Recommender 廣告系統（原話："a paradigm shift in how our ad system works"）
- 2026-07-29｜Susan Li (CFO)｜product：Instagram 時長雙位數成長（原話："global time spent this quarter grew double digits"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：推出 Meta One 訂閱服務（原話："We also just launched Meta One, a new subscription offering"）
- 2026-07-29｜Susan Li (CFO)｜product：已推出模型 API（原話："We also recently launched a high intelligence model API"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：Meta AI 每日互動人數成長（原話："a 60% increase in the number of people interacting"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜customer：商業代理已有逾百萬企業使用（原話："already more than 1 million businesses using"）
- 2026-07-29｜Susan Li (CFO)｜customer：Movida 案例：WhatsApp 每日訂位成長（原話："44% increase in daily bookings through WhatsApp"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：眼鏡早期銷售優於預期（原話："Early sales have been strong, exceeding our expectations"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜commitment：CEO 預告個人代理產品將很快推出（原話："we're going to ship this at some point soon"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜commitment：對個人代理的長期預測（原話："extremely unlikely if you look out 5 years from now"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜capital_allocation：管理層對算力的定位：可直接出售，現有算力獲高於成本的報價（原話："We're getting a lot of offers for compute at a"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜capital_allocation：問答中再提算力報價溢價（原話："quite a number of offers at a meaningful"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜margin：CEO 稱賣智能比賣算力毛利更高（原話："margin on selling intelligence rather than selling compute"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜capital_allocation：不會把算力全數出售換短期利潤（原話："foolish to basically just sell all of the compute"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜capital_allocation：與 BlackRock 合資興建 1GW 資料中心（原話："BlackRock to develop a new 1 gigawatt data center"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：資本結構納入更高比重債務（原話："to include a greater mix of debt as we"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：2026–2027 容量規劃以最大化為目標（原話："geared towards maximizing 2026 and 2027 capacity."）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：產業長期建置不足，現有容量極具價值（原話："making existing capacity, including our own,"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：自研晶片投資（原話："our internal custom silicon effort, which will provide"）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：2028 規劃重視彈性（原話："we're really focusing on flexibility."）
- 2026-07-29｜Susan Li (CFO)｜capital_allocation：核心業務仍有未滿足的算力需求（原話："ROI-positive places that we would put compute toward"）
- 2026-07-29｜Susan Li (CFO)｜competition：稱模型不在前沿也能服務用戶（原話："regardless of whether our models are on the frontier"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜competition：開源模型目前不如前沿模型，故不依賴（原話："source models are not as strong as the frontier models."）
- 2026-07-29｜Mark Zuckerberg (CEO)｜commitment：預期近期回頭釋出開源模型（原話："we will get back to releasing some open source models at"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜competition：自稱最擅長將產品規模化至數十億人（原話："we're probably the best company in the world at scaling"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜competition：AI 定位：把超級智能交到個人手中（原話："AI with the primary goal of putting superintelligence"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜customer：企業商機被描述為需新建的能力（原話："somewhat of a new muscle that we"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜customer：企業產品採按結果付費模式（原話："businesses only pay us when we achieve results for them"）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：對 MSL 實驗室進展的評價（原話："I'm quite happy with the trajectory that we're on."）
- 2026-07-29｜Mark Zuckerberg (CEO)｜product：持續擴大更大模型訓練（原話："we're in the process of scaling"）

### 問答異常語氣（迴避／改口／保留）
- META_Q2_2026_Earnings_Call_20260729.md｜問：Brian Nowak 問 2026–27 哪個新業務最先能展現可量化的 ROIC｜答法：Mark 未點名單一業務，改稱對所有領域都有意義的成長，細節『稍後分享』
- META_Q2_2026_Earnings_Call_20260729.md｜問：Brian Nowak 問 2027 年資本支出的哲學與上下行因素｜答法：Susan 表示不提供 2027 資本支出指引，僅說規劃高度動態

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
{"date":"20260730","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"廣告核心維持 ≥18% 營收成長，且 AI 能持續讓「曝光」與「每廣告價」同時上升（＝變現效率真的在提高，而非用廣告版位換量）"},{"id":"H2","text":"2026–2028 的巨額 AI capex 最終轉為可衡量的損益貢獻——經由（a）廣告變現效率續升，或（b）一條具名、帶金額的外部收入線（企業 agent／模型 API／直接賣算力／訂閱）。這是 make-or-break。"},{"id":"H3","text":"市場對資本強度的折價，隨 ROI 能見度回升而部分修復（不需要回到 25 倍，只需要不再往 12 倍走）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"廣告景氣下行——廣告是需求端週期敏感支出，中小企業預算對總經最敏感。Q2 的每廣告價 +12% 中，管理層明說有一部分來自「相對去年 Q2 的總經改善」與「匯率順風」，這兩項都會反向。Q3 指引已隱含匯率約 1% 的逆風。"},{"id":"R2","text":"AI capex 與折舊爬坡吞噬營運槓桿，ROI 遲遲不兌現（本檔最高機率風險）——Q2 折舊攤銷 $63.56 億（+46% YoY），H1 累計 $123.55 億（去年同期 $82.42 億）。2026 全年 D&amp;A 約 $275 億，2027 依當前資本投入節奏將跳到 $440 億上下。同期營收增速由 +28% 降到 +19–20%。費用的二階導數為正、營收的二階導數為負，這是利潤率壓縮的定義。"},{"id":"R3","text":"注意力介面遷移 ＋ 自家前沿模型落後——Meta Superintelligence Labs 的 Muse Spark 在 Artificial Analysis Intelligence Index v4.0 得 52 分、排名第 4，落後 Gemini 3.1 Pro（57）、GPT-5.4（57）、Claude Opus 4.6（53）。Zuckerberg 自己在法說上把「即使我們的模型不在前沿也沒關係，我們有分發」寫進論述——這是一個誠實但不令人安心的護欄。若消費者的預設 AI 互動介面長在別人的模型上，Meta 的分發優勢會被逐步中介化。"},{"id":"R4","text":"訴訟與監理已進入兌現階段（非「即將發生」）——這是本次相對前次報告最需要改寫的一條。截至報告日的已實現事實：① 2026-03 新墨西哥州陪審團認定 Meta 違反州法、危害兒童身心安全，判民事罰款 $3.75 億；② 同月另一新墨西哥州陪審團認定違反消費者保護法，再判 $3.72 億；③ 同月洛杉磯 K.G.M. v. Meta et al. 陪審團認定 Meta（與 YouTube）對用戶心理健康損害負有責任；④ 本季財報認列 $24 億法律相關費用，管理層並在展望中明文警告「數起美國兒少相關審判排定於今年，最終可能造成重大損失」。已兌現的民事罰款合計約 $7.47 億，與「$1.4 兆」的州檢察長理論求償上限相差三個數量級——但重點不是金額，是 Meta 至今在這一波審判中尚未勝訴過。加上 EU DMA 已於 2025-04 開罰 €2 億（consent-or-pay 違規），且 DMA 對重複違規的理論上限為全球營收 10%，這是一條持續性、非一次性的成本曲線。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"首階 1/3 現價可建；加碼掛 2026-10-29 的 2027 capex 指引 < $180B 且附具名外部算力／企業營收指引，或回檔至 $480（FY2026 正規化 PE 17.8x）","irr_base_pct":10.3,"ev5y_pct":55.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.9,"ev5y_pct":55.8,"irr_base_pct":10.3,"max_dd_pct":-60.0,"bull_5y_price":1500.0,"bear_5y_price":271.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"首階 1/3 現價可建；加碼掛 2026-10-29 的 2027 capex 指引 < $180B 且附具名外部算力／企業營收指引，或回檔至 $480（FY2026 正規化 PE 17.8x）","price_at_dd":542.49,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
