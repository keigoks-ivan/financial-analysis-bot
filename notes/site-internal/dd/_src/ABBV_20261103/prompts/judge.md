你是 stock-analyst **v20 判斷 agent**，標的 ABBV（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ABBV","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABBV_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABBV_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenues_gaap","label":"Net revenues (GAAP)","value":17404,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD m（YoY +10.3%，營運口徑 +10.5%；QoQ +2.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 investors.abbvie.com Q3 2026 press release"},"note":"未取得單季營收共識"},{"id":"f_kpi1_gaap_operating_margin","label":"GAAP operating margin","value":36.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"%（GAAP 營業利益 6,267 百萬美元；Q3 2025 為 1,904 百萬美元）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 investors.abbvie.com Q3 2026 press release"},"note":"未取得"},{"id":"f_kpi2_adjusted_non_gaap_operat","label":"Adjusted (non-GAAP) operating margin","value":48.7,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 investors.abbvie.com Q3 2026 press release"},"note":"未取得"},{"id":"f_kpi3_diluted_eps_gaap_adjuste","label":"Diluted EPS (GAAP / Adjusted)","value":3.82,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","unit":"USD（Adjusted；GAAP 2.37；含 IPR&D 與里程碑費用 216 百萬美元＝每股 −0.11）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-30）","citation":"公司 IR 新聞稿 investors.abbvie.com Q3 2026 press release"},"note":"未取得單季共識；FY1 共識 EPS 13.95（consensus_revision，10-31 快照）"},{"id":"f_kpi4_fy2026_adjusted_diluted_","label":"FY2026 adjusted diluted EPS guidance","value":"13.95–13.99","period":"Q3 FY2026（公告於 2026-10-30）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（公告於 2026-10-30）","citation":"公司 IR 新聞稿 investors.abbvie.com Q3 2026 press release；新聞稿未給 Q4 單季指引，且含截至 Q3 每股 0.69 美元 IPR&D 與里程碑費用負面影響"},"note":"FY1 共識 13.95（落在指引區間下緣）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-30","period":"2026-10-30","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-30"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_abbv_gross_margin_pct","label":"ABBV 毛利率","value":71.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_operating_margin_pct","label":"ABBV 營業利益率","value":33.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_fcf_margin_pct","label":"ABBV FCF 利潤率","value":28.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lly_gross_margin_pct","label":"LLY 毛利率","value":83.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lly_operating_margin_pct","label":"LLY 營業利益率","value":51.25,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lly_fcf_margin_pct","label":"LLY FCF 利潤率","value":13.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_gross_margin_pct","label":"MRK 毛利率","value":71.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_operating_margin_pct","label":"MRK 營業利益率","value":0.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_mrk_fcf_margin_pct","label":"MRK FCF 利潤率","value":18.72,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bmy_gross_margin_pct","label":"BMY 毛利率","value":69.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bmy_operating_margin_pct","label":"BMY 營業利益率","value":29.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_bmy_fcf_margin_pct","label":"BMY FCF 利潤率","value":18.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amgn_gross_margin_pct","label":"AMGN 毛利率","value":69.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMGN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amgn_operating_margin_pct","label":"AMGN 營業利益率","value":29.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMGN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amgn_fcf_margin_pct","label":"AMGN FCF 利潤率","value":26.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMGN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":289.86,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":41.09,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":64.19,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.95 → 13.95）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.2 → 16.2）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（18.1 → 18.1）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.95,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":16.2,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":18.1,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-1.2,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 14.12 → 13.95（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":49.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝38.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":38.6,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":7.76,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":8.73,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":20.78,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 13.95，分子＝快照價 289.83","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.387,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":64316.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 70885.0、現金 6569.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1767.12,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":576479.58,"period":"2026-11-03","unit":"USD m","basis":"市值 512163.58 ＋ 淨負債 64316.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":67815.45,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":73788.4,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":8.5,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 288.36 / W52 233.31 / W104 209.96 / W250 169.5 / W250 13週斜率 1.68%"},{"id":"f_ma_w52","label":"52 週均線","value":233.31,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":209.96,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":169.5,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.68,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出 Humira 面臨全球直接生物相似藥競爭，免疫產品與 IL-23、IL-17、JAK 抑制劑競爭，腫瘤產品與 BTK 抑制劑、ADC、細胞療法競爭。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"AbbVie's immunology products compete with IL-23 inhibitors, IL-17 inhibitors, JAK inhibitors, biosimilars and other competitive products intended to treat a number of disease states, and AbbVie's oncology products compete with targeted therapies including BTK inhibitors, ADCs, cell therapies and other competitive products intended to treat certain cancers.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：專利到期後生物相似藥／學名藥會在短時間內顯著侵蝕銷售，且大型藥廠與學名藥廠持續跨入生物相似藥。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"The expiration or loss of patent protection for a product typically is followed promptly by substitutes that may significantly reduce sales for that product in a short amount of time.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Skyrizi 取得美國乾癬總處方份額逾 45%，IBD 一線 in-play 病患擷取率 75%（Crohn's 80%）；Rinvoq RA in-play 份額中段十位數。","source":"Motley Fool AbbVie Q4 2025 earnings call transcript","url":"https://www.fool.com/earnings/call-transcripts/2026/02/04/abbvie-abbv-q4-2025-earnings-call-transcript/","excerpt":"SKYRIZI market share (US psoriasis) -- Secured over 45% total prescription share, while frontline in-play patient capture rate in US IBD has reached 75% overall and 80% in Crohn's disease.","as_of":"2026-02-04","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"AbbVie 10-K 風險因子：部分原料與零組件來自單一供應商；尋找替代供應商需耗時、花費且需監管核准，無法保證能達成協議。（此為 AbbVie 自身對供應商的依賴，非客戶導入第二供應商）","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"AbbVie uses raw materials and components in its pharmaceutical and biologic manufacturing processes that may be sourced from single suppliers.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"AbbVie 簽約收購 West Pharmaceutical 位於亞利桑那州 Tempe 的藥物遞送裝置工廠（含 SmartDose 3.5ml 製造與供應權），屬把供應商環節轉為自有生產；為 AbbVie 自身 in-house 化，非客戶端動作。","source":"pharmaceuticalonline.com, News January 14, 2026（搜尋摘要）","url":"https://www.pharmaceuticalonline.com/doc/abbvie-to-buy-device-manufacturing-facility-from-west-pharmaceutical-services-0001","excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"ABBV 10-K FY2025：美國三大批發商（McKesson、Cardinal、Cencora）占美國藥品銷售幾乎全部，單一批發商不超過美國毛營收 43%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"In 2025, three wholesale distributors (McKesson Corporation, Cardinal Health, Inc. and Cencora, Inc.) accounted for substantially all of AbbVie's pharmaceutical product sales in the United States. No individual wholesaler accounted for greater than 43% of AbbVie's 2025 gross revenues in the United States.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未見三大批發商 2026 年信評調降；McKesson 10-K 僅有一般性評級風險語句。","source":"WebSearch 摘要（McKesson 10-K FY2026）","url":"https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000069/mck-20260331.htm","excerpt":"Credit rating agencies regularly review our credit and rate our outstanding debt.","as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"AbbVie 將 Skyrizi+Rinvoq 2027 年合計營收目標由 >$27B 上調至 >$31B；2026 年指引已超過該目標","source":"TIKR: AbbVie Stock: Skyrizi and Rinvoq Already Cleared 2027 Guidance","url":"https://www.tikr.com/blog/abbvie-stock-skyrizi-and-rinvoq-already-cleared-2027-guidance-but-does-the-discount-still-make-sense","excerpt":"in Q4 alone, Skyrizi posted operational growth of 31.9% and Rinvoq grew 28.6%, with AbbVie guiding the combined franchise to over $31 billion in 2026, representing more than 20% growth on an already enormous base.","as_of":"2026-04-24","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 2026 營收近$17B、年增10.2%，全年營收指引上調$300M至約$67.6B；Skyrizi、Rinvoq、神經科學各成長逾20%","source":"Nasdaq: AbbVie Q2 earnings call highlights","url":"https://www.nasdaq.com/articles/abbvie-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Q1 2026 Humira營收$688M，年減38.6%，Humira侵蝕持續","source":"TIKR: AbbVie Stock: The Post-Humira Transition Is Working","url":"https://www.tikr.com/de/blog/abbvie-stock-the-post-humira-transition-is-working-and-the-road-to-311","excerpt":"Der weltweite Umsatz von Humira sank um 38,6 % auf 688 Mio. USD und blieb damit leicht hinter den Erwartungen zurück, aber der Rückgang war voll und ganz erwartet worden und bereits in der Prognose von AbbVie eingepreist.","as_of":"2026-05-10","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"AbbVie 於 2026 年 1 月與美國政府簽自願協議：加入 TrumpRx、降低 Medicaid 價格、承諾十年 1000 億美元美國投資，換取三年關稅與未來價格強制措施豁免（搜尋摘要轉述）","source":"AJMC / Pharmaceutical Commerce 2026-01 報導","url":"https://www.ajmc.com/view/abbvie-joins-trump-drug-pricing-effort-pledges-100b-in-us-r-d-investment","excerpt":null,"as_of":"2026-01-13","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026 年 1 月 CMS 選定 Botox 為 15 項納入 Medicare Part B/D 政府定價藥品之一，2028 年起適用；IRA 對 AbbVie 業務有重大且持續影響（搜尋摘要轉述 Q1 2026 10-Q）","source":"AbbVie 10-Q Q1 2026","url":"https://www.sec.gov/Archives/edgar/data/0001551152/000155115226000017/abbv-20260331.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026-06-30 10-Q 列示 Niaspan 反壟斷訴訟（EDPA MDL，指控 2005 專利和解違反反壟斷法），訴訟應計約 17 億美元（搜尋摘要轉述）；搜尋結果未見 EU 執委會對 AbbVie 的反壟斷行動","source":"AbbVie 10-Q Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0001551152/000155115226000026/abbv-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"AbbVie 10-K 風險因子列出貿易限制／關稅可能提高成本、中斷供應鏈，為已揭露風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"Trade restrictions, tariffs, and other changes in global trade policy could increase costs, disrupt supply chains, and adversely affect AbbVie’s business and results of operations.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026年1月AbbVie與美國政府達成自願協議，承諾10年內1000億美元美國研發與資本投資，換取三年關稅與未來價格強制令豁免。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"AbbVie pledged $100 billion in U.S.-based research and development and capital investments, including manufacturing, over the next decade. Under this voluntary agreement, the U.S. government has agreed to provide AbbVie a three-year exemption from tariffs and future price mandates.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Global Trade Alert 記載美國與AbbVie關於MFN藥價與關稅豁免協議。","source":"Global Trade Alert","url":"https://globaltradealert.org/state-act/97004-united-states-of-america-agreement-with-abbvie-on-most-favoured-nation-drug-pricing-and-tariff-exemption","excerpt":"United States of America: Agreement with AbbVie on Most-Favoured-Nation drug pricing and tariff exemption Announcement 12 Jan 2026","as_of":"2026-01-12","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：AbbVie 的藥品與生物製劑製程所用原料與零組件，部分來自全球各地的單一供應商，中斷會傷害業務。","source":"AbbVie Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"AbbVie uses raw materials and components in its pharmaceutical and biologic manufacturing processes, including those sourced from single suppliers around the world","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"早期 10-K（FY2014、FY2021）載明 AbbVie 有營業中斷保險，對單一供應商失效提供一定程度保護。","source":"AbbVie Form 10-K FY2021 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115222000007/abbv-20211231.htm","excerpt":"AbbVie does, however, carry business interruption insurance, which provides a degree of protection in the case of a failure by a single-source supplier.","as_of":"2022-02-18","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"AbbVie 宣布十年 1000 億美元美國製造投資，與 2026 年 1 月和美國政府協議、取得關稅豁免有關（德文二手報導）。","source":"boerse-express.com","url":"https://www.boerse-express.com/news/articles/abbvie-aktie-milliarden-investition-gestartet-869545","excerpt":null,"as_of":"2026-04-23","retrieved_at":"20261103","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026：Skyrizi $5.776B(+22.7%)、Rinvoq $2.706B(+23.9%)、Botox Therapeutic $1.080B(+9.8%)、Botox Cosmetic $669M(+4.9%)、aesthetics合計$1.176B(-1.4%)；全年aesthetics展望維持約$50億，免疫全年$349億","source":"AbbVie news release 2026-10-30 Q3 2026 results","url":"https://news.abbvie.com/2026-10-30-AbbVie-Reports-Third-Quarter-2026-Financial-Results","excerpt":"Global Skyrizi Net Revenues Were $5.776 Billion; Global Rinvoq Net Revenues Were $2.706 Billion; Global Humira Net Revenues Were $683 Million","as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"AbbVie預期Skyrizi與Rinvoq 2026及未來數年面臨低個位數價格逆風；Humira受生物相似藥衝擊下滑","source":"Nasdaq 文章 AbbVie Q2 earnings call highlights","url":"https://www.nasdaq.com/articles/abbvie-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AbbVie 10-K 列明免疫產品與 IL-23、IL-17、JAK 抑制劑及生物類似藥競爭，腫瘤產品與 BTK、ADC、細胞療法競爭；新產品與醫療實務改變可能導致產品過時。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"AbbVie's immunology products compete with IL-23 inhibitors, IL-17 inhibitors, JAK inhibitors, biosimilars and other competitive products intended to treat a number of disease states, and AbbVie's oncology products compete with targeted therapies including BTK inhibitors, ADCs, cell therapies and other competitive products intended to treat certain cancers.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：專利到期後學名藥/生物類似藥會在短時間內顯著壓低銷售。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"The expiration or loss of patent protection for a product typically is followed promptly by substitutes that may significantly reduce sales for that product in a short amount of time.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FDA 於 2026-03-18 核准 J&J 口服 IL-23 受體拮抗劑 icotrokinra（Icotyde）用於中重度斑塊型乾癬，被定位為 Skyrizi 的直接競爭者；搜尋摘要稱 AbbVie 管理層表示 Icotyde 上市後 Skyrizi 新患與轉換新處方仍成長，並上調 2026 年 Skyrizi 至 216 億、Rinvoq 至 102 億美元。","source":"WebSearch 摘要（引 S&P Global Market Intelligence、Fierce Pharma 等）","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/05/icotyde-forecast-to-reach-usd1-6b-by-2028-as-jnj-builds-psoriasis-franchise","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：AbbVie 美國藥品主要經獨立批發商（McKesson、Cardinal、Cencora 幾乎涵蓋全部美國藥品銷售），部分直售零售商、藥局、病人；通路結構為傳統批發模式。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"In the United States, AbbVie distributes pharmaceutical products principally through independent wholesale distributors, with some sales directly to retailers, pharmacies, patients or other customers.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026 年 1 月 AbbVie 與美國政府簽三年自願協議，內容含 Medicaid 低價、擴大部分產品的直接面向病人現金支付選項、十年 1000 億美元美國投資。","source":"AbbVie 財報電話會議逐字稿（financialfilings.com 轉載）","url":"https://financialfilings.com/filings/abbvie-inc/call-transcript/2026/48473482/","excerpt":"the company announced a voluntary agreement with the U.S. government that reinforces its commitment to patient access and affordability. Key elements include offering low prices in Medicaid, expanding direct-to-patient cash pay options for select products, and committing $100 billion in U.S. R&D and capital investments over the next decade.","as_of":"2026-01-13","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"AbbVie 2026Q3 財報（2026-10-30）將全年調整後 EPS 指引由 13.76–13.96 上調至 13.95–13.99（已吸收約 $0.69/股 IPR&D 與里程碑費用）；Q3 調整後 EPS $3.82，營收 $17.404B。搜尋摘要來源間數字不一致，需對 8-K 核實。","source":"AbbVie 8-K 新聞稿摘要（last10k.com）","url":"https://last10k.com/sec-filings/abbv/0001551152-26-000033.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"MarketBeat 報導（2026-07-07）稱 AbbVie 下修 FY2026 EPS 指引至 $13.91–$14.11，低於 Street $14.25；為單一來源，未對公司原文核實。","source":"MarketBeat: AbbVie issues FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/abbvie-nyseabbv-issues-fy-2026-earnings-guidance-2026-07-07/","excerpt":null,"as_of":"2026-07-07","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價：2026 年 7 月中至下旬彙總平均約 $274–$277，區間約 $200–$328（約 28 位分析師），評等以 Buy 為主（Investing.com：25 Buy/5 Hold/1 Sell）；晚於 2026-07 的目標價分布未查到。","source":"Investing.com AbbVie Inc (ABBV) 共識頁","url":"https://www.investing.com/equities/abbvie-inc","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Evercore ISI 下調目標價但稱 2026、2027 共識仍可望被超越；AbbVie 2 月初對 2026 的獲利展望高於華爾街預期。","source":"Yahoo Finance: Evercore ISI Cuts AbbVie PT","url":"https://finance.yahoo.com/news/evercore-isi-cuts-abbvie-inc-004928355.html","excerpt":null,"as_of":"2026-02-10","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Hudson Labs Q3 2026 財報前瞻：指引含 Apogee 收購稀釋約 $0.14/股","source":"Hudson Labs","url":"https://www.hudson-labs.com/research/abbvie-q3-2026-earnings-preview-abbv-results-and-outlook","excerpt":"EPS 13.87–14.07 3.84–3.88 Includes $0.14 dilution from Apogee deal Skyrizi Sales ($M) 21,700 Raised $100M in Q2 Neuroscience Sales 12,700 Raised $100M in Q2","as_of":"2026-10-06","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-18 AbbVie 簽約以每股 135.11 美元現金收購 Apogee Therapeutics，總值約 109 億美元，以債務融資；2026-09-03 8-K 報告完成交易；預期 2026 EPS 稀釋 0.14 美元、2027 稀釋 0.46 美元、2032 起增厚。","source":"RTTNews／iTiger 報導（Apogee 收購案）","url":"https://www.rttnews.com/3661650/abbvie-to-buy-apogee-therapeutics-for-135-11-share-in-cash.aspx?type=sta","excerpt":null,"as_of":"2026-06-18","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"2026-04-24 AbbVie 確認 trenibotulinumtoxinE BLA 收到 FDA 完整回覆信（CRL），事由為製造資訊，未提安全或療效疑慮。","source":"AbbVie 10-Q（2026-06-30）／搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001551152/000155115226000026/abbv-20260630.htm","excerpt":null,"as_of":"2026-04-24","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026 年 FDA 核准：Decnupaz（BPDCN，2026-05）、Skyrizi 兒童乾癬／乾癬性關節炎（2026-06）、Skyrizi 皮下誘導治療克隆氏症、Venclexta＋acalabrutinib 治療未經治療 CLL。","source":"AbbVie 10-Q（2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0001551152/000155115226000026/abbv-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2026-05-18 起 PRED MILD 眼藥水 Class III 召回（FDA 編號 D-0551-2026），2,736 瓶，因穩定性規格不合格。","source":"MarketScreener／FDA 召回資料","url":"https://www.marketscreener.com/news/abbvie-inc-faces-fda-enforcement-action-for-pred-mild-recall-ce7f5dd3d08ef521","excerpt":null,"as_of":"2026-05-18","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"-","claim":"10-K FY2025 列示未決訴訟：Niaspan 反托拉斯、鴉片類藥物訴訟（約 335 件）、Camargo v. AbbVie（Humira 定價集體訴訟，2026-01 法院准許撤銷、不影響再提）。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"In January 2026, the court granted AbbVie’s motion to dismiss, without prejudice.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-06-18 簽約以每股 135.11 美元現金收購 Apogee Therapeutics，約 109 億美元；2026-09-03 8-K 報告完成。","source":"RTTNews（Apogee 收購案）","url":"https://www.rttnews.com/3661650/abbvie-to-buy-apogee-therapeutics-for-135-11-share-in-cash.aspx?type=sta","excerpt":null,"as_of":"2026-06-18","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Camargo v. AbbVie（Humira 定價集體訴訟）2026-01 法院准許撤銷、不影響再提；另有 Niaspan 反托拉斯集體訴訟與鴉片類藥物訴訟持續。搜尋未見 2026 新增證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1551152/000155115226000008/abbv-20251231.htm","excerpt":"In January 2026, the court granted AbbVie’s motion to dismiss, without prejudice.","as_of":"2026-02-20","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"2026-04 trenibotulinumtoxinE 收到 FDA CRL（製造資訊）；2026-05 Decnupaz 核准；2026-06 Skyrizi 兒童適應症核准。","source":"AbbVie 10-Q（2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0001551152/000155115226000026/abbv-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"PRED MILD 眼藥水 2026-05-18 起 Class III 召回，2,736 瓶，穩定性規格不合格；搜尋未見 2026 警告信。","source":"MarketScreener／FDA 召回資料","url":"https://www.marketscreener.com/news/abbvie-inc-faces-fda-enforcement-action-for-pred-mild-recall-ce7f5dd3d08ef521","excerpt":null,"as_of":"2026-05-18","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 16 份 8-K 清單中無 Item 4.02（財報不可信賴／重編）項目，搜尋亦未見 SEC 調查。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001551152&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 16 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 4 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"}],"gaps":[],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ABBV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.48,"operating_margin_pct":33.94,"fcf_margin_pct":28.28,"rd_intensity_pct":15.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"LLY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":83.63,"operating_margin_pct":51.25,"fcf_margin_pct":13.52,"rd_intensity_pct":17.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"MRK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.31,"operating_margin_pct":0.87,"fcf_margin_pct":18.72,"rd_intensity_pct":53.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"BMY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.24,"operating_margin_pct":29.19,"fcf_margin_pct":18.56,"rd_intensity_pct":21.1},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"AMGN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.52,"operating_margin_pct":29.99,"fcf_margin_pct":26.71,"rd_intensity_pct":20.03},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMGN","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"ABBV"},"financial_history":{"ticker":"ABBV","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":58054000000.0,"revenue_yoy_pct":null,"gross_margin_pct":70.0,"operating_margin_pct":32.41,"net_income":11836000000.0,"diluted_eps":6.63,"free_cash_flow":24248000000.0,"fcf_margin_pct":41.77,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":54318000000.0,"revenue_yoy_pct":-6.44,"gross_margin_pct":62.42,"operating_margin_pct":24.92,"net_income":4863000000.0,"diluted_eps":2.72,"free_cash_flow":22062000000.0,"fcf_margin_pct":40.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":56334000000.0,"revenue_yoy_pct":3.71,"gross_margin_pct":69.99,"operating_margin_pct":21.11,"net_income":4278000000.0,"diluted_eps":2.39,"free_cash_flow":17832000000.0,"fcf_margin_pct":31.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":61160000000.0,"revenue_yoy_pct":8.57,"gross_margin_pct":70.24,"operating_margin_pct":32.85,"net_income":4226000000.0,"diluted_eps":2.36,"free_cash_flow":17816000000.0,"fcf_margin_pct":29.13,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ABBV/ABBV_Q3_2026_Earnings_Call_20261030.md）

# Q3 2026 Earnings Call
**AbbVie Inc.** | Earnings Calls | 2026-10-30

**Operator** (Operator):
Good morning, and thank you for standing by. Welcome to the AbbVie Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Today's call is also being recorded. If you have any objections, you may disconnect at this time.
I would now like to introduce Ms. Liz Shea, Senior Vice President, Investor Relations.

**Elizabeth Shea** (Executives):
Good morning, and thanks for joining us. Also on the call with me today are Rob Michael, Chairman and Chief Executive Officer; Jeff Stewart, Executive Vice President, Chief Commercial Officer; Roopal Thakkar, Executive Vice President, Research and Development, Chief Scientific Officer; and Scott Reents, Executive Vice President, Chief Financial Officer.
Before we get started, I'll note that some statements we make today may be considered forward-looking statements based on our current expectations. AbbVie cautions that these forward-looking statements are subject to risks and uncertainties that may cause actual results to differ materially from those indicated in our forward-looking statements. Additional information about these risks and uncertainties is included in our SEC filings. AbbVie undertakes no obligation to update these forward-looking statements, except as required by law.
On today's conference call, non-GAAP financial measures will be used to help investors understand AbbVie's business performance. These non-GAAP financial measures are reconciled with comparable GAAP financial measures in our earnings release and regulatory filings from today, which can be found on our website. Following our prepared remarks, we'll take your questions.
So with that, I'll turn the call over to Rob.

**Robert Michael** (Executives):
Thank you, Liz. Good morning, everyone, and thank you for joining us. AbbVie continues to perform above our expectations, with another quarter of outstanding results. We are delivering top-tier sales and earnings growth and making significant progress advancing our pipeline. Given the strength of our business and our promising outlook, we are once again raising our full year guidance and increasing our quarterly dividend.
Turning to our third quarter performance, we achieved adjusted earnings per share of $3.82, which is $0.07 above our guidance midpoint. Total net revenues were $17.4 billion, beating our expectations by $200 million and reflecting robust sales growth of more than 10%. This includes 9 key products that delivered double-digit growth. Based on the strong performance across our business, including Skyrizi, Rinvoq, Vraylar, Ubrelvy, Qulipta and Venclexta, we are raising our full year revenue guidance by $200 million and have now raised total revenue by $800 million since the start of the year. Further underscoring our confidence in our long-term outlook, today, we announced a 5.2% increase in our quarterly cash dividend, beginning with the dividend payable in February 2027. Since inception, we have grown our quarterly dividend by more than 350%.
Turning now to R&D. We are making excellent progress advancing our pipeline to help drive growth in the 2030s and beyond. In immunology, we completed the acquisition of Apogee Therapeutics, adding multiple differentiated assets in dermatology, respiratory and other related inflammatory diseases with significant sales potential. The lead asset, zumilokibart, will be starting Phase III development in atopic dermatitis later this year.
Also in immunology, we received U.S. approval for Skyrizi subcu induction in Crohn's. This new dosing option demonstrated exceptional efficacy and further strengthens Skyrizi's robust growth outlook. We also continue to make substantial progress with our strategy to combine Skyrizi with complementary mechanisms to further elevate the standard of care for patients with IBD. We have now started a large Phase IIb program in both Crohn's and UC with Skyrizi plus our alpha4beta7 382 as well as Skyrizi plus our TL1A 701.
Moving to neuroscience. We recently expanded our Parkinson's portfolio with the FDA approval of Juvmo. Juvmo provides physicians and patients with a meaningful new treatment option and represents a sizable commercial opportunity for AbbVie. Along with Vyalev/Duopa, we expect our Parkinson's therapies to collectively deliver peak sales of more than $5 billion.
We are also making excellent progress with our oncology pipeline. Etentamig in multiple myeloma has demonstrated very high efficacy as well as differentiated safety and convenience. We have now submitted our application for etentamig in the U.S. and anticipate approval in 2027. In addition, we reported positive Phase III data for Epkinly in frontline DLBCL and expect regulatory submission next year.
In summary, we are delivering strong execution across our business and see numerous opportunities to drive long-term growth.
With that, I'll turn the call over to Jeff for additional comments on our commercial highlights. Jeff?

**Jeffrey Stewart** (Executives):
Thank you, Rob. I'll start with the quarterly results for immunology, which delivered total revenues approaching $9.2 billion, reflecting operational sales growth of 16.6%. Skyrizi and Rinvoq continue to exceed our expectations, demonstrating robust growth across all indications.
Skyrizi total sales were nearly $5.8 billion, up 22.9% on an operational basis. In psoriasis, Skyrizi prescription trends remain very strong. Recent oral competition is not having a substantive impact on our in-play patient share with Skyrizi continuing to capture roughly 1 out of every 2 new or switching psoriasis patients. We believe that Skyrizi's best-in-class profile, which delivers 100% skin clearance for the majority of psoriasis patients, high durability of response, very convenient quarterly dosing, exceptional long-term safety and robust joint protection in psoriatic arthritis with strong data through 5 years of treatment sets a very high bar relative to other therapies on the market or in development for psoriasis.
In IBD, Skyrizi is growing very robustly as well and continues to capture half of the new patient starts in the class. And we are very excited to be launching the subcutaneous induction dosing for Crohn's disease, which further strengthens our competitive position. The data supporting this new delivery is striking, including impressive rates of endoscopic response and remission, particularly for CD patients in the frontline setting. This efficacy is clearly differentiated relative to our own Skyrizi IV formulation and will allow us to be very competitive versus all induction therapies available for Crohn's today.
Our subcu induction regimen is delivered with the same on-body injector as our IBD maintenance dose, which has received very favorable feedback from gastroenterologists and patients both, including overall ease of use, dosing speed and comfort. Now while access typically takes a couple of months to ramp, our commercial and medical teams have already hit the ground running, and we expect the subcu induction will accelerate our new patient share in Crohn's over the next several quarters.
Overall, we remain very competitively positioned in gastro and psoriatic disease. We are raising our Skyrizi full year sales guidance for the third time this year, and we see a substantial opportunity for both market and share growth well into the next decade.
Turning now to Rinvoq, which delivered global sales of $2.7 billion, reflecting operational growth of 24.3%. Rinvoq is also exceeding our expectations with particularly strong momentum in both RA and IBD, where we continue to see growing in-play patient share. We are also excited for the indication expansion opportunities in dermatology with commercialization of Rinvoq for vitiligo and alopecia areata underway already in Europe and approvals expected for both diseases in the U.S. over the next several months. Recall these 2 new indications combined are expected to contribute nearly $2 billion of peak sales.
Lastly, in immunology, Humira global sales were $683 million, down 30.6% on an operational basis, reflecting continued biosimilar competition.
Moving to neuroscience, where we continue to outperform expectations across our leading portfolio. Total revenues were nearly $3.4 billion, up 19.5% on an operational basis. In psychiatry, Vraylar global sales were nearly $1.1 billion, up 14.3%. Performance in both bipolar disorder and adjunctive MDD continues to be very strong, reflecting Vraylar's well-defined profile in terms of dosing flexibility, low sedation and the ability to treat a full spectrum of symptoms.
In migraine, we continue to deliver robust sales growth driven by share gains and underlying market growth as well. Botox Therapeutic global revenues were approximately $1.1 billion, up 9.8%. Ubrelvy global sales were $449 million, up 26.9% and Qulipta global revenues were $398 million, up more than 38%.
Menstrual migraine prevention represents another opportunity to further strengthen our leading CGRP profiles. Recent positive data for Qulipta and forthcoming results for Ubrelvy in this new potential indication could support approval and commercialization in late 2027.
We also have substantial momentum in Parkinson's disease. Vyalev total sales were $286 million, reflecting double-digit growth. We remain on track to exceed $1 billion in revenue this year. We are also launching Juvmo, another exciting new treatment for patients with Parkinson's. Juvmo selectively activates the D1/D5 dopamine receptors involved in motor control and can be prescribed now as both a monotherapy in Parkinson's as well as an add-on to standard of care.
And given Juvmo's distinct profile, including strong durable motor control and low rates of debilitating side effects such as impulse control disorder, somnolence and dyskinesia, it represents a sizable commercial opportunity. Sales for Juvmo are expected to ramp gradually over the next several quarters as we work to establish commercial and Medicare coverage, which is expected to be more broadly available starting in 2028.
Turning now to oncology, where total revenues were $1.7 billion, up 0.9% on an operational basis. Venclexta is performing very well especially in CLL as combination use with BTK inhibitors is a preferred fixed duration treatment globally. Total sales were $803 million, up 10.7%. Continued double-digit sales growth from Elahere and Epkinly also helped to offset the expected revenue decline for Imbruvica, which was down 26.1% due to IRA pricing and competitive share pressure.
I'm also very excited for our developing portfolio in hematology following positive data for both etentamig in multiple myeloma and Epkinly in frontline DLBCL. We anticipate their potential approvals will be an important catalyst for next year and immediately supported by our existing commercial resources, including a substantial heme sales force and medical affairs team.
Lastly, in aesthetics, global sales were nearly $1.2 billion, down 1.8% on an operational basis. Botox Cosmetic total revenues were $669 million, up 4.1% operationally, reflecting improving market growth globally. Juvéderm global sales were $222 million, down 11.8% operationally, reflecting continued headwinds in key dermal filler markets.
While economic uncertainty and lower consumer confidence have pressured the aesthetics category over the last several quarters, we are starting to see signs of stability. And we think that bringing forward innovation like our new fast-acting short-duration toxin Boey represents a meaningful opportunity for more new patients to initiate an aesthetic treatment. The commercial rollout of Boey is now underway in Europe and Canada and patient satisfaction has been very high, particularly with the rapid onset, which is consistent with the data from our clinical program. 
So overall, I'm very pleased with the execution and the continued strong performance across our commercial portfolio. 
And now I'll turn the call over to Roopal for comments on our R&D highlights. Roopal?

**Roopal Thakkar** (Executives):
Thank you, Jeff. I'll begin with gastroenterology programs in immunology. We further strengthened our leadership position in inflammatory bowel disease with the FDA approval of Skyrizi subcutaneous induction in Crohn's disease, which was based on the Phase III AFFIRM study. Detailed results from this trial were presented at the recent ACG and UEG meetings, demonstrating exceptional results across all clinical and endoscopic measures. We are extremely pleased with Skyrizi's strong performance, particularly in patients who had not previously experienced advanced therapy.
In this patient segment, unprecedented results were observed after just 16 weeks of therapy with 60% endoscopic response, 43% endoscopic remission and 74% for clinical remission. These results highlight the potential of subcutaneous induction to further enhance Skyrizi's position in earlier lines of Crohn's disease.
Additionally, the Skyrizi label was updated to provide health care providers greater discretion in determining whether tuberculosis evaluation is appropriate prior to treatment initiation, rather than requiring mandatory TB evaluation for all patients.
Also at the UEG conference, results were presented from the Phase II TARGET-CD study, evaluating Skyrizi plus our novel anti-alpha4beta7 antibody, ABBV-382 in Crohn's disease. The combination resulted in a near doubling of endoscopic remission at week 24 compared to either monotherapy. Additionally, gut gene expression data showed a clear improvement from active disease at baseline to early intestinal healing at week 12, followed by broader tissue restoration at week 24. Early changes reflected repair of the intestinal lining and restoration of the gut barrier, effects not observed with monotherapy. By week 24, these changes evolved into signatures associated with tissue repair, nerve recovery and normalization of metabolic function. We believe this progression from inflammation to healing and ultimately, tissue restoration may represent an important step towards modifying the underlying disease rather than simply controlling symptoms.
These results support our strategy of combining Skyrizi with complementary mechanisms to achieve meaningfully higher levels of efficacy in IBD. A large multi-arm Phase IIb trial is underway, evaluating Skyrizi plus 382 and Skyrizi plus 701, an extended half-life anti-TL1A antibody in both Crohn's disease and ulcerative colitis. In parallel, co-formulation work is ongoing in preparation for Phase III trials.
Moving to dermatology. Positive top line results were recently announced from a Phase III study evaluating lutikizumab in hidradenitis suppurativa. At week 16, lutikizumab demonstrated statistically significant and clinically meaningful improvements across multiple measures of disease activity. HiSCR 75, which is a rigorous bar for defining clinical response was achieved by 31% of lutikizumab patients. Lutikizumab also significantly improved skin pain, disease flares and quality of life measures with improvement in pain reported as early as week 1. HS remains one of the most underserved diseases in dermatology and these results support lutikizumab's potential to become an important new treatment option for patients with HS. Results from the 36-week blinded extension period will be available next year with regulatory submissions to follow in the second half of 2027.
Based on these results, we plan to begin an HS platform study later this year to evaluate lutikizumab and in combination with our long-acting amylin analog, 295. Other mechanisms such as anti-TL1A antibody are also being considered. The Phase III program for Rinvoq in HS is also nearing completion, where we remain on track for 16-week top line results near the end of the year.
Moving to atopic dermatitis. Zumilokibart, Phase II results were presented at the EADV Congress, demonstrating rapid and meaningful skin clearance and itch relief. Phase III studies are on track to begin later this year.
Turning to neuroscience, where in the third quarter, Juvmo was approved by the FDA for Parkinson's disease. Dopamine agonists have long been used to help manage symptoms and reduce reliance on oral levodopa escalation. However, currently available agents primarily target D2/D3 receptors and their use has been limited by adverse events. As a selective D1/D5 receptor agonist, Juvmo demonstrated strong motor control and a favorable tolerability profile with low rates of dyskinesia, sedation and impulse control disorder, which have historically impacted the use of dopamine agonists.
Additionally, long-term data continue to support a reduced reliance on oral levodopa when taking Juvmo. After more than 1.5 years on Juvmo, 93% of patients had not increased their levodopa dose and 94% of patients with early Parkinson's disease had not started oral levodopa. Physicians and patients now have a treatment option that targets dopamine pathways differently and may reduce the difficult trade-offs associated with D2/D3 agonists.
In psychiatry, the emraclidine dose escalation study has completed. The 150-milligram dose will be utilized in the monotherapy and adjunctive Phase II studies in schizophrenia with enrollment expected to begin by the end of this year. This new dose is 5x the highest dose evaluated in the previous 2 pivotal trials. The 150-milligram dose was well tolerated and no new safety signals were identified. We look forward to advancing this higher dose for schizophrenia, which may result in greater efficacy compared to prior studies. Doses have also been selected for the psychosis program, where Phase II studies in Alzheimer's and Parkinson's disease are expected to begin early next year.
Moving to our psychedelic asset, bretisilocin, a Phase III trial evaluating a single-course acute treatment in major depressive disorder is expected to begin later this year. We also remain on track for additional Phase II data in monotherapy MDD by year-end, which will help inform the Phase II study evaluating repeat dosing for chronic use. This MDD study as well as Phase II proof of concepts in post-traumatic stress, generalized anxiety and obsessive compulsive disorders are expected to begin in 2027.
In migraine, positive top line results were announced from the Phase III LUNA study, which evaluated Qulipta for the preventive treatment of menstrual migraine. No medicines are currently approved for menstrual migraine attacks, which are considered more difficult to treat, more disabling, tend to last longer and have a higher tendency to recur. This underscores the need for effective treatment strategies for this distinct disorder.
In the LUNA trial, Qulipta demonstrated meaningful and statistically significant reductions in migraine days associated with the menstrual period meeting the primary and all 8 ranked secondary endpoints versus placebo. A regulatory application will be submitted soon in Europe. Additionally, Phase III results for Ubrelvy in menstrual migraine prevention are expected near the end of the year, which will potentially support a submission in the U.S. in early 2027.
Moving to hematologic oncology. Positive top line results were announced from the Phase III CERVINO trial evaluating etentamig monotherapy versus standard of care in heavily pretreated triple-class exposed multiple myeloma patients. Etentamig delivered statistically significant and clinically meaningful improvements in progression-free survival and overall response rates with a manageable safety profile, supporting its potential to become an important new treatment option for multiple myeloma.
BCMA-directed bispecifics and CAR-T therapies have transformed multiple myeloma treatment. However, their adoption, particularly among community-based centers remains limited by adverse events such as CRS, neurotoxicity and serious infections as well as the need for specialized monitoring. With a differentiated safety profile, simplified onboarding and a more convenient once-monthly dosing schedule after a single step-up dose, etentamig has the potential to streamline treatment and expand access across settings, including community-based clinics. A regulatory application was recently submitted to the FDA with an approval decision anticipated next year.
Beyond the CERVINO program, 2 new Phase III trials were recently initiated for etentamig, one in combination with pomalidomide in second-line plus multiple myeloma and another as a monotherapy in patients with newly-diagnosed light chain amyloidosis. And at the upcoming ASH meeting, early results from a Phase II study evaluating etentamig plus daratumumab in frail, transplant ineligible frontline multiple myeloma will be presented with a third Phase III study potentially starting next year.
Continuing with other hem/onc programs. Positive top line results were announced from the Phase III EPCORE DLBCL-2 trial evaluating Epkinly in combination with R-CHOP in frontline DLBCL. The study demonstrated a statistically significant and clinically meaningful improvement in progression-free survival compared to R-CHOP alone. Epkinly plus R-CHOP showed an overwhelming treatment benefit at this interim analysis, reducing the risk of disease progression or death by 51% in a broad population covering patients with International Prognostic Index scores between 2 and 5.
Importantly, this is the first Phase III study with a bispecific antibody combination to demonstrate a progression-free survival benefit in front line [indiscernible] supporting the potential for Epkinly plus R-CHOP to become a new standard of care in this setting. Regulatory submissions are anticipated early next year.
Turning to solid tumors. At the World Conference on Lung Cancer, results from a Phase I study evaluating our PD-1/VEGF bispecific antibody, ABBV-1480 in frontline non-small cell lung cancer were presented. These early data were particularly encouraging, given the activity observed in PD-L1 negative patients, a group which has traditionally been more difficult to treat. A Phase III study was recently initiated to evaluate 1480 in combination with chemotherapy in frontline squamous and non-squamous small cell lung cancer. We also intend to move quickly to evaluate 1480 in combination with our ADCs across several tumor types. Two Phase II studies evaluating 1480 plus Temab-A were recently initiated, one in non-small cell lung cancer and another in colorectal cancer. And a Phase II combination study with ABBV-706, our SEZ6 ADC will begin next year in small cell lung cancer.
Moving to obesity. Detailed results were presented at EASD from a Phase I multiple ascending dose study evaluating ABBV-295 in adults with a mean BMI of less than 30. We continue to be encouraged by the emerging profile for this long-acting amylin analog. In the study, 295 demonstrated meaningful weight loss across multiple dosing regimens, a manageable tolerability profile and a PK profile that supports potentially differentiating dosing intervals of every other week or monthly. A Phase Ib study in obese patients is ongoing with interim data anticipated around the end of this year. Additionally, a Phase II trial in obese patients was recently initiated.
Turning to aesthetics. We continue to work closely with the FDA to resolve outstanding matters related to the complete response letter for Boey. Resubmission to the FDA is anticipated before the end of this year, with a regulatory decision expected in mid-2027. Additionally, we are exploring a combination of Botox with Boey, which has the potential to deliver differentiated efficacy by combining the rapid onset of Boey with the durable effects of Botox. A Phase II study recently began to evaluate this combination in glabellar lines.
In summary, we continue to make meaningful progress across all stages and therapeutic areas of our pipeline and look forward to several more important pipeline milestones during the remainder of this year and into 2027.
With that, I'll turn the call over to Scott.

**Scott Reents** (Executives):
Thank you, Roopal. Starting with our third quarter results. We reported adjusted earnings per share of $3.82, which is $0.07 above our guidance midpoint. These results include an $0.11 unfavorable impact from acquired IPR&D expense. Total net revenues were $17.4 billion, reflecting robust operational growth of 10.5%, excluding a 0.2% unfavorable impact from foreign exchange. Adjusted gross margin was 85.1% of sales. Adjusted R&D expense was 13.9% of sales, and adjusted SG&A expense was 21.2% of sales. The adjusted operating margin was 48.7% of sales, which includes a 1.2% unfavorable impact from acquired IPR&D expense. Adjusted net interest expense was $688 million. The adjusted tax rate was 13.6%.
Turning to our financial outlook. We are raising our full year adjusted earnings per share guidance range by $0.11 at the midpoint to between $13.95 and $13.99. This guidance does not include acquired IPR&D expense that may be incurred beyond the third quarter. We now expect total net revenues of approximately $67.8 billion, an increase of $200 million. At current rates, we continue to expect a roughly 0.5% favorable impact from foreign exchange on full year sales growth.
Our revenue forecast now includes the following approximate assumptions for several of our key products and therapeutic areas. For immunology, we are increasing our global sales outlook to $34.9 billion. This assumes Skyrizi revenue of $21.8 billion and Rinvoq revenue of $10.3 billion, reflecting increases for both brands based on continued strong momentum. In neuroscience, we now anticipate global revenues of $13 billion, an increase of $300 million reflecting Vraylar sales of $4.2 billion, Botox Therapeutic sales of $4.2 billion and total oral CGRP sales of $3.1 billion. For oncology, we are raising our global sales guidance to $6.6 billion. This now contemplates higher Venclexta sales of $3.1 billion as well as lower Imbruvica sales of $2.1 billion. In aesthetics, our global sales outlook remains unchanged at $5 billion and now assumes higher Botox Cosmetic sales of $2.8 billion, offset by lower expected revenues across products and other aesthetics.
Moving to the P&L for 2026. We continue to forecast full year adjusted gross margin above 84% of sales, adjusted R&D expense of approximately $9.8 billion and adjusted SG&A expense of approximately $14.5 billion. We also anticipate an adjusted operating margin of approximately 46.7% of sales, which includes a roughly 1.8% unfavorable impact from acquired IPR&D expense incurred through the third quarter.
Turning to the fourth quarter. We anticipate net revenues of approximately $18.4 billion, which includes a modestly unfavorable impact from foreign exchange. We also forecast adjusted earnings per share between $3.83 and $3.87. This guidance does not include acquired IPR&D expense that may be incurred in the quarter.
Finally, AbbVie's strong business performance continues to support our capital allocation priorities. Our cash balance at the end of September was $10.8 billion, and we generated approximately $14 billion of free cash flow in the first 9 months of the year, which includes nearly $2.7 billion of Skyrizi royalty payments. This robust free cash flow supports a strong and growing quarterly dividend, which we are increasing 5.2% to $1.82 per share beginning with the dividend payable in February of 2027, as well as capacity for additional business development where we continue to assess external innovation across all of our key growth areas. Following the recent close of the Apogee transaction, we remain on track to achieve a net leverage ratio of 2x over the next 2 to 3 years.
In closing, AbbVie has once again delivered outstanding top and bottom line results and our financial outlook remains very strong.
With that, I'll turn the call back over to Liz.

**Elizabeth Shea** (Executives):
Thanks, Scott. We will now open the call for questions. In the interest of hearing from as many analysts as possible over the remainder of the call, we ask that you please limit your questions to one or two. Operator, we'll take the first question, please.

**Operator** (Operator):
[Operator Instructions] We'll go first to Vamil Divan with Guggenheim Securities.

**Vamil Divan** (Analysts):
Great. Thanks for all information on the call. Maybe if I could just as I know you're not giving formal guidance for next year yet, but if I could just ask about -- as we think about updating our models today, any sort of key pushes and pulls as we think about next year in terms of dynamics to keep in mind? And also just at this point, anything you can share around payer discussions [indiscernible] Rinvoq and how we should think about [indiscernible].

**Robert Michael** (Executives):
Thanks, Vamil. This is Rob. I'll take the first question, and Jeff will take the second question. So as we typically do, we'll provide 2027 guidance on the Q4 call, but we are certainly exiting this year in a very strong position. Our sales and earnings growth in 2026 will be the second highest relative to our peers. And we expect to deliver top-tier growth again next year. When I look at Skyrizi and Rinvoq, they're delivering incredible growth of $6 billion combined this year despite already being on the market for 8 years and with more competition.
If you think about where that growth is coming from, that $6 billion, $3 billion of it is in IBD across Rinvoq and Skyrizi with obviously a competitive entry in that space. $2 billion of that growth is in Skyrizi psoriatic with the competitive entry in that space as well. So we're seeing despite increased competition just tremendous growth from Skyrizi and Rinvoq. And we have several catalysts that will help drive their growth next year and beyond, including subcu induction for Skyrizi in Crohn's with higher efficacy and more convenient dosing that will give us an even stronger competitive position. We'll see Skyrizi head-to-head data versus Entyvio, which will bolster our position in UC, and we will launch 2 new derm indications for Rinvoq, both vitiligo and alopecia areata. So we have very strong momentum in immunology to continue delivering robust growth next year and beyond.
Then in neuroscience, we're on track to deliver growth of 20% this year. which has made us the industry leader. I expect the strong demand to continue for Vraylar, Ubrelvy, Qulipta and Vyalev, in addition to Botox Therapeutic, Juvmo, as was mentioned on the call today, and it's our new Parkinson's therapy. That will also contribute to the growth, although the ramp will be more significant in '28 and beyond, given timing of Medicare coverage.
And then I would also keep in mind that the IRA price for Vraylar will begin in 2027, so you should be modeling that in as well, although I'd say many of the sell-side models have appeared to have modeled that in. But clearly, I mean, we have a lot of momentum across our business to drive strong top-tier growth again next year.

**Jeffrey Stewart** (Executives):
Yes, Vamil. It's Jeff. So we are beginning to close all of the arrangements with the large PBMs and payers. And I would say, overall, it's a very consistent story as prior years. Our portfolio of products will have very strong access and it's based on a lot of the demand and the profiles that we have. The physicians really like these products, they're leading products across almost all of our categories. And so we anticipate very good payer access.
In terms of the immunology approach that low single-digit sort of rebate concession is something that I would continue to think about in your modeling. Channels move around a bit, but that's typically been our pattern, and we continue to think that, that's a good level of guidance there in terms of as we move into '27 in terms of payer access.
And I couldn't fully hear your question, but in terms of Rinvoq, very consistent answer, and we anticipate with the pending approvals of vitiligo and alopecia areata, as we move into '27 that those new indications will also be reflected with favorable access as we move into the new year.

**Operator** (Operator):
We'll go next to Chris Schott with JPMorgan.

**Christopher Schott** (Analysts):
I just want to follow up on the full data from the Skyrizi subcu induction in Crohn's and that recent approval. Can you just help frame out the opportunity here? I guess, specifically, how are you thinking about market share dynamics going forward? And I guess, how quickly do you think that could play through as you think about just kind of the ramp of Skyrizi from here?
And then my second question was on the pipeline and the role of Skyrizi and the alpha4beta7 in IBD. Just following the Phase II data, are you thinking of this as a drug that's for later lines of therapy or something that could be earlier in the treatment paradigm? Just maybe kind of talk a bit more about how you're seeing that fit relative to Skyrizi and just other products being developed in the space.

**Jeffrey Stewart** (Executives):
Yes, Chris. It's Jeff. I'll take the commercial stuff and maybe Roopal can give a quick flavor over the new data that was announced at ACG and UEGW. Yes.

**Roopal Thakkar** (Executives):
So on the subcu data set, what you heard from us was very strong data. And when we compare it with our own Skyrizi IV induction, it's numerically higher and quite substantially higher in that treatment-naive setting, which is the current positioning of Skyrizi currently in Crohn's and UC. So it will further support that exact positioning. Because recall, with Rinvoq having a little bit of a label expansion that has allowed us for those patients that are deemed inappropriate for an anti-TNF, who can then use Rinvoq potentially right after Skyrizi. So that positioning, I should say, has been further substantially strengthened with this subcutaneous offering. So that's one point. And maybe I'll touch on the alpha4beta7 combo and then go back to Jeff.
So Chris, what we saw here was very strong efficacy in later lines, including patients who already used P19s, already used JAK inhibitors like Rinvoq. However, we also saw strong data in earlier lines. And we anticipate being able to see that in Crohn's and in particular, a lot of excitement from our thought leaders and how this combination can look in earlier lines of ulcerative colitis. Can we get much stronger disease control early in patients rather than waiting for a step-up in care, this can potentially modify the disease as I was describing based on gene expression. Could you have much better outcomes in the longer-term reductions in hospital visits and surgeries.
So as we move this forward, we'd be looking at early patients and in later lines of patients. And that's in Crohn's and UC. We would explore that with 382, which is the alpha4beta7 as well as with our TL1A antibody as well.

**Jeffrey Stewart** (Executives):
Yes. And Chris, in terms of your commercial question, so we are excited about the recent subcu approval, and our field teams already are out there promoting this AFFIRM data that's now reflected in the U.S. label. So I think what's important, as Roopal said, these endoscopic endpoints are really resonating for several years now with the gastroenterologist. And that's the single largest market value driver of what preference is.
And so when our experts and our IBD experts or gastros look at this AFFIRM data, it's quite striking. So it's sort of very, very high rates, higher than our IV. And when they look, of course, it's cross-study comparisons, when they look across not just IL-23 induction, but every single induction study that's been done to date, it really stands out. So as we've talked about over the last few quarters, the in-play share is roughly 50-50 in IBD versus the main competitor, we would anticipate certainly an acceleration in Crohn's where we have that approval.
Now in terms of timing as to when we'd see that, it will take us probably 60 days, maybe a little bit longer to get full access. That's just the normal cycle of the approval of something like this with our contracts. So certainly the first part of the year into the second quarter, we anticipate a pretty rapid share acceleration there.

**Roopal Thakkar** (Executives):
And Chris, let me add. We're also very pleased with the updated tuberculosis language that gives physicians more flexibility. So that was important based on years of data. So we're excited about that. And then recall, having the subcu option upfront and then having every 8-week dosing, that's another area we can continue to emphasize that makes Skyrizi so unique.

**Operator** (Operator):
We have Louise Chen from Scotiabank.

**Louise Chen** (Analysts):
I wanted to ask you for emraclidine, what gives you confidence that the under-dosing was really the issue in the prior studies? And what's your thinking -- your latest thinking on the market opportunity? And then the other thing I want to ask you is that you have a lot of potentially best-in-class assets in your pipeline. Maybe if you could highlight to us which one or which ones you're most excited about that you think are underappreciated by the Street. That would be very helpful.

**Roopal Thakkar** (Executives):
Louise, this is Roopal. I'll take that. With emraclidine, we did observe lower receptor occupancy and variability in PK, and again, that's 1/5 of the dose that we're going to take forward at 150 milligram. So the confidence is more around the PK and receptor occupancy and less heterogeneity at the higher dose. So that will drive, hopefully, more predictability there, and we continue to like the benefits of once-a-day dosing and the fact that we don't need another complementary drug to offset adverse events. And thus far, we've seen low GI adverse events. So we think that will be a nice benefit in monotherapy and adjunctive. We are going into Phase II, so we'll be able to test this out. So that's, I would say, drug specific.
And then also study specific. We were able to do deep dives into the EMPOWER studies and our own Vraylar studies. And from that, we can learn better approaches to reducing placebo responses. So there's a variety of factors that we're going to implement in all of our trials going forward. And hopefully, that will also support favorable outcomes in the future. And if we see that, we would pivot very rapidly to Phase III.
Some things that we're excited about staying in psychiatry. You heard us talk about bretisilocin. MDD is important, but also PTSD, anxiety and OCD are where we're going to look at Phase II. So that's potentially underappreciated. But I do have to, I would say, mention again etentamig. And that one is in our pipeline. We have multiple additional Phase IIIs that are prepared and ready to go. And this asset is quite near term, has a potential to launch around the middle of next year. And that is a very exciting asset as we've described. The CRS rates are very low and almost all Grade 1 and very few Grade 2 and just a single case of ICANS after a single step-up dose, and then you can immediately go to monthly dosing.
So this is very well differentiated across anything available currently in the TCE space. So we're very excited about that one. And we believe that the Street continues to underappreciate that asset and our opportunity in myeloma with etentamig, and then even potentially with our anti-CD38 BCMA T-cell engager tri-specific, which we are trying to move very quickly into Phase III. That's also a very unique opportunity.
And maybe, Jeff, why don't you comment...

**Jeffrey Stewart** (Executives):
Yes. No, I would agree. We've been surprised, maybe less so more recently, but etentamig is a fantastic profile and not only will it allow us to enter myeloma, I think, very, very rapidly here. We have multiple drugs behind it. And so this is a clear strategy that's underappreciated. I think more recently because Roopal had such a phenomenal discussion over some of these readouts, very excited about Epkinly and frontline NHL. This is really the big market value driver in terms of that particular product and the readout was spectacular.
I would have to say as well which is maybe not as big a surprise, but the ability to continue to raise the standard of care in IBD with 466, this combination platform. And we've got multiple shots on goal there with combination TL1A that is very, very close. So the ability to bring multiple assets to basically navigate really the exceptional performance of Skyrizi as we move into the 2030s is also a profound opportunity for the company.

**Robert Michael** (Executives):
And Louise, this is Rob. Just to add on here. We've mentioned etentamig. It's a multibillion-dollar opportunity that is significantly undercalled in many Street models. I would add Temab-A to that as well, similarly a multibillion-dollar opportunity, significantly undercalled in many Street models. And then if you look at the neuroscience business, we've said, we believe have three $5 billion-plus franchises covering psychiatry, migraine and Parkinson's. And we're still not seeing that reflected in longer-term consensus. I would also add zumilokibart as upside to the Street versus what we're expecting.
So as I look at the portfolio, we have -- as we look at longer-term growth in the 2030s, we have a number of upside opportunities that are not yet reflected in Street models.

**Operator** (Operator):
We'll go next to Trung Huynh with RBC.

**Trung Huynh** (Analysts):
My first question is just on 340B. It's been a persistent challenge for the industry. So it was interesting to see that earlier in this month that you're taking part in this 340B pilot launch for next year. So that's for Imbruvica, Linzess and Vraylar. Can you just walk us through the strategic rationale for participating there? Are there any potential gross-to-net improvements from the reduced duplicate discounts? Or do you think we could still expect a headwind from the broader 340B exposure? Just really wondering how material the benefits could be here. And then on aesthetics, could you just give us an update on TrenibotE following the CRL and your just time lines for resubmission? Just how should we think about that?

**Robert Michael** (Executives):
Trung, this is Rob. I'll take your first question on 340B. Yes, I mean, we are very focused on curbing the abuse in the program. And we are very supportive of the original intent of the program, which was to help safety-net hospitals serve the most vulnerable populations. But unfortunately, today, we have an outdated and overly broad definition of a 340B patient, which has led to significant program abuse. And that ultimately drives higher health care costs for employers, taxpayers and patients and it takes R&D investment away from the industry.
But that said, we are encouraged by the bipartisan support we are seeing across both the House and Senate on a few proposals that can bring greater transparency and accountability. And that's really what it's about. It's about driving more transparency and accountability, which is also what I believe this rebate pilot will accomplish. It's another opportunity to provide that transparency to ensure that this program ultimately serves its original intent to benefit patients and not steal investment away from R&D.
I think it's too early to call a financial impact. We'll have to see how this plays out. We certainly manage the duplicate discounts well. We have good visibility to that. So I'd say we've been managing through it. There has been, though profound growth in this program that I think the entire industry has been seeing, which is why we're advocating for policies that curb the abuse that we're seeing.

**Roopal Thakkar** (Executives):
And it's Roopal on the TrenibotE question. Recall that the CRL was not due to any particular issues around safety or efficacy it was on CMC assessments. And we're gathering that data for the agency, and we will resubmit at the end of this year, and we anticipate a 6-month review. So we think the middle of next year in the U.S. And while this is ongoing, we are also submitting in other countries across the globe, we already have European approval and as well as Canada.

**Operator** (Operator):
We will go next to Jason Gerberry with Bank of America.

**Jason Gerberry** (Analysts):
Mine was just on ABBV-466. And if you could talk about, are there any triggers to potentially move this into Phase III faster? I know you have the interim data for the Phase IIb with the higher dose integrin. I imagine that's something that you're curious to see the results from before going to Phase III, but wondering to the extent that you might be rate limited just by the co-formulation work and that's put the hard and fast kind of 2028 start on the Phase III program.

**Roopal Thakkar** (Executives):
Jason, it's Roopal. So we do have built-in interims in this next data set that's going forward. A few things that we're going to do to assess 382 exposure response. One thing to help speed things up is look at the data and run assays more often than you typically would and not waiting for the end. The other thing we will also see is for the Phase II study that we were just talking about here today, we've shown about 80% of the data. We'll get 100% of that data by the end of this year, early next year. And that will let us rerun some of these models and to see if we continue to observe that exposure response lack of plateau for 382, sometimes with greater sample size, you could see things move in either direction. And while that's occurring, we'll start generating more data on the combo.
So if something is looking good, then we can speed up the trial in a way by dropping the arm that's the current standard dose. Alternatively, if we are seeing that the efficacy is shouldering at a particular dose, then we don't have to continue the high dose and then we can pivot to the standard dose that we've already studied, gather some more data there, be ready for regulators and then potentially move into Phase III sooner.
It's hard to commit now. I would say there is some potential that we could start Phase IIIs at the end of 2027. We'll come back to see if that's possible. But I haven't ruled that out based on our ability to look at the data on an interim basis.

**Operator** (Operator):
We'll go next to Simon Baker with Rothschild & Co Redburn.

**Qize Ding** (Analysts):
This is Qize for Simon Baker. I have a quick question on Epkinly in first-line large B-cell lymphoma. So given your competitors developing a different combination regimen, any thoughts about the competitiveness of Epkinly-based regimen? Maybe just a quick follow-up on Epkinly as well. So how should we think about the launch trajectory of Epkinly in first-line large B-cell lymphoma?

**Roopal Thakkar** (Executives):
Maybe I'll start and then Jeff will comment. What we like about the approach with Epkinly with R-CHOP is that R-CHOP is very familiar, it's very well known across the globe and there's a simplicity of just adding Epkinly to a very well-known treatment regimen. So we think there's already a benefit there. And then you also don't have to add 2 novel agents to a regimen. This would just be a single novel to R-CHOP that people understand very well. So from an R&D standpoint, we're excited about that, and that's what we hear from clinicians that for them, it will be relatively simple approach.

**Jeffrey Stewart** (Executives):
Yes. And I think that, as I mentioned, I mean, that frontline potential is clearly the largest commercial opportunity. We had always known that, that was a larger commercial opportunity with our partner Genmab, but to see the strength of the data, it's quite striking. So we do believe, despite what we may see from the competitor readout that this is a very, very simple approach. It's going to play extremely well around the world because there is a variability over countries on how they view Polivy, the reimbursement of Polivy. And then again, you have a novel -- 2 novel novels, it starts to build up the cost. So the exquisite simplicity of what we've done in frontline with Epkinly has resonated very much with the thought leaders around the world. I think it will resonate very rapidly with the HTAs and other payers.
And so we anticipate, as we move towards approvals, and as Roopal mentioned, we'll be moving quickly with the regulatory filings here, I would expect quite a rapid adoption of that transformational indication.

**Scott Reents** (Executives):
And this is Scott. I would just make sure everyone recalls that with respect to that product and the partnership that we have with Genmab, there's partnership economics. So we are not booking sales, the full sales in the U.S. Puerto Rico and Japan, we're booking a profit share. So it's a little bit of a different impact on the revenue line.

**Operator** (Operator):
We'll go next to Terence Flynn with Morgan Stanley.

**Terence Flynn** (Analysts):
Great. Maybe a 2-part for me. I guess, Rob, now that you've integrated Apogee, could you just provide your latest perspective on M&A and business development appetite and how you're thinking about size of potential deals from here? And then relatedly, on obesity, a question we get a lot is, does AbbVie need a GLP-1 to be able to compete at scale in this market? Obviously, you have the amylin. You talked about an interesting combination approach today. But how do you think about need for a GLP-1?

**Robert Michael** (Executives):
Thanks, Terence. I'll take the first question, and Roopal will take the second one.
So I would point to the Apogee deal and really the PD-1/VEGF from RemeGen as great examples of the BD priorities that we've been communicating for a while now. And our focus really continues to be on differentiated assets in our core areas, immunology, neuroscience and oncology, but we're also looking to expand in obesity as well. And I'd say, across the portfolio, it could be an early-stage deal, late stage or even on market. And again, given that our existing products and pipeline give us a clear line of sight to strong durable growth into the 2030s. We have ample financial capacity to pursue the deals we're interested in.
Now I would expect these to be more bolt-on additions versus a large transformational deal like Allergan, and that's because our business already has good breadth. For us, it's really more about adding further depth to these areas to drive that long-term growth.

**Roopal Thakkar** (Executives):
Yes. And it's Roopal. Yes, we continue to have interest to build out obesity assets. We are open to anything that has a profile that's differentiated that could match potentially our 295, especially when it comes to a co-formulation. That could be incretin class or anything else. And we want to continue to drive efficacy, but very importantly, tolerability because patients still continue to start and stop and spin off.
And if we had other combo agents that continues to open the door in other indications that we already have leadership in psoriasis, psoriatic arthritis, I already mentioned HS with an amylin, but if we had another agent, you could imagine us going into HS. Just for context, the mean BMI of our study with lutikizumab was almost 34. So on average, it already fits a category where one could anticipate either amylin use in the future or incretin use today.

**Operator** (Operator):
We'll go next to Steve Scala with TD Cowen.

**Steve Scala** (Analysts):
I have 2 questions. Can you help us create an expectation for the Rinvoq efficacy readout in HS, specifically on HiSCR 50 placebo-adjusted benefit. Should we be thinking about something closer to 10% or 25%? So that's the first question. Second question is, what should be our expectation for Botox IRA pricing, both in percentage as well as issues revolving around the litigation. Presumably, AbbVie already knows the discount. So what can you tell us?

**Roopal Thakkar** (Executives):
Steve, it's Roopal. For HS and Rinvoq, we still anticipate the readout later this year. And as you mentioned, the primary endpoint is HiSCR 50. I would say it's difficult to know what the exact delta could be. We do see that drift in placebo. We observed it ourselves with lutikizumab that's probably driven by heterogeneity, larger patient populations, more sites, more countries. And it's difficult to know until we see the Phase III data.
But the way we think about it is that HiSCR is just one parameter. And really the key driver -- the #1 symptom that patients have and that clinicians also reiterate is pain. And what we saw with luti has us very encouraged because the pain started to -- patients had relief from pain as early as week 1 over the course of therapy. Quality of life is also important. Lack of flares is very important. And these are the things that we would look to in the Rinvoq study as well. It will come down to totality of data and what are these key drivers for patients and for clinicians.
And what I can say is we will be capturing this evidence in the Rinvoq study just as we did in the lutikizumab study. And what Rinvoq brings is an oral and recall that it's also coming in as a second line post other advanced therapies like other biologics. So the setup there and the positioning is consistent with PsA, Crohn's and UC, where we have a biologic today at Skyrizi that goes into more frontline, earlier patients and then Rinvoq comes in later. Same thing could develop here with lutikizumab going early and then Rinvoq coming in later.

**Robert Michael** (Executives):
And Steve, this is Rob. I'll take your question on Botox IRA. Look, we feel the IRA is very clear that products derived from human blood or plasma are not eligible for selection. One of Botox's 3 ingredients is human serum albumin, which is a protein extracted from human blood plasma. And Botox has 100,000x more human serum albumin than toxin, which is why we believe Botox is not eligible for selection under the IRA and a Federal District Court just yesterday ruled in our favor. Now that ruling is subject to appeal by the government. So we'll have to wait to see if there are any more proceedings. But in the meantime, we would not expect a price to be published while this plays out.

**Operator** (Operator):
Our next question comes from the line of David Risinger with Leerink Partners.

**David Risinger** (Analysts):
Yes. And congrats on the performance and all the updates. So I have a question for Roopal, please. Roopal, can you just talk about I&I pipeline candidate trial results to watch in 2027 after the Rinvoq HS results in coming months?

**Roopal Thakkar** (Executives):
Thanks. It's Roopal here. I would say after we see this data set, we're going to be keeping -- that's the Rinvoq HS. We're going to be keeping a close eye on the IBD combos. And as I stated before, we'd be looking for interim data to see if we can accelerate even further. The other important outcome next year is Rinvoq in lupus. So I would be looking for that. And then we can anticipate hopefully some data out of our B-cell depletion portfolio. That includes CD19-depleting antibody, the CD19 with an ADC and of course, our in-vivo CAR-T against CD19. So we're starting to see some patients starting to enroll post the first-in-human in healthies. So that could be other very important data sets that we would see next year.
Other readouts potentially are in rheumatoid arthritis combos with luti and psoriatic arthritis as well. And I would say that not necessarily readout, but we're going to be kicking off plenty of studies post the Apogee acquisition. And you'll see the Phase III study starts with zumi in atopic dermatitis, but we're also going to be doing either Phase IIb work quickly, I would say, and then moving into Phase III for pruritus, urticaria, prurigo nodularis, and then combination work with the TSLP in EoE, asthma, COPD, sinusitis, and then imagining as those move forward, 8 distinct Phase III programs that would be reading out in late '29 across the -- into the mid-2030s. So quite a bit to keep an eye on in immunology.

**Operator** (Operator):
We'll take our next question from Mohit Bansal with Wells Fargo.

**Mohit Bansal** (Analysts):
I just want to touch upon tavapadon a little bit. It does seem like in the trials you have done longer-term data suggests that the drug was able to spare patients from levodopa for a long time. So I would love to understand how you are thinking about positioning this drug? I mean you have a $5 billion guidance for the entire Parkinson's franchise that tavapadon is a smaller part of this. But what could be a surprise for us from the upside point of view? How should -- like what -- where are you positioning it? And what is the feedback you are getting so far from the physicians as you are launching this product?

**Roopal Thakkar** (Executives):
Yes. Mohit, it's Roopal. I'll make a few comments, and then Jeff can speak about the opportunity here. Yes, you caught on to something very interesting, and that's what our experts are quite excited about that if you're an early patient and you start taking tavapadon, very rarely will you need, and this is, I think, around 85 weeks or so that you would need to start levo/carbidopa, and many clinicians are interested in keeping that in pocket as long as possible due to the adverse events that can happen later.
And we saw that same thing play out in a little different format on patients that were currently on levo/carbidopa, you can effectively freeze that dose with tavapadon for the same period of time, approximately 1.5 years. So you have the setup in those patients that are trying to optimize oral therapy and giving tavapadon allows them to do that very quickly, which is really nice to see because that efficacy is observed early on.
And then as time goes by, because this is likely and Jeff will talk about this, we're likely it will first get utilized, and people will then recognize that there is a potential in earlier parts, and this is due to access elements that Jeff can now speak about.

**Jeffrey Stewart** (Executives):
Yes. Mohit, the market feedback has been quite strikingly positive so far. And it is exactly that. There's 2 elements of it. The first is this data that Roopal described, where when you add it on, you essentially freeze any dose escalations in almost all the patients for 85 weeks in counting. So the movement disorder experts and the neurologists, they know that as they continue to dose up and you have to escalate levodopa/carbidopa dosing, it just leads to the dyskinesia and it's not good. So the efficacy from the trials has been quite striking. And that's balanced really well with these low rates of really -- we call it somnolence, but the Parkinson's experts know it's like a sleep attack, like the patients can really get in trouble with the sleepiness, the sedation and the sleep attacks and very little to no observed impulse control disorders, and that's what really harmed the first generation of the agents that didn't focus on D1/D5 but D2/D3.
So we actually have been quite surprised at how strong the profile has been reacted to. Now it's only been a matter of a few weeks. What we also see that's been surprising is patients are aware of it, and they're pushing some of their neurologists and movement disorder experts. 
So in terms of upside, we know that we've missed sort of the Medicare window for '27. We'd love to be able to sort of see if we can get some early adds, that's sort of speculative at this point. But we are very, very encouraged at the initial market reaction that we're seeing. And right now, because there is no access, all we can see is sort of enrollments and people are going through medical exception processes, sort of the high-level demand in the funnel has been exceeding our initial expectations. So stay tuned. It looks like a very, very strong asset, and we'll just continue to watch it and press over time.

**Elizabeth Shea** (Executives):
Thanks, Mohit. We are cognizant that another peer call is starting shortly. So we just have time for one final question.

**Operator** (Operator):
Our last question comes from Gary Nachman with Canaccord Genuity.

**Gary Nachman** (Analysts):
So with the new indications for Rinvoq in vitiligo and alopecia areata, will it be positioned as first line for both of those conditions? And I know you said $2 billion plus for that in terms of the market opportunity. But review how big those markets are a little bit more specifically? And how much you'll be increasing your presence even more with the derms after those approvals?

**Jeffrey Stewart** (Executives):
Yes. Thanks, Gary. Great questions. And so as you know, as I mentioned in my remarks, we did raise the long-term targets for both of those based on the quality of the data. So alopecia data was substantially better than we anticipated, really transformationally this is that you have the ability on the so-called SALT score in some cases, to completely regrow hair or get 90% hair regrowth at rates that we haven't seen before. So that's been positive. Vitiligo data when we look at it, is going from strength to strength. So we continue to see through 76 weeks that we're progressively improving the repigmentation. And as you may recall, it will be the first-ever systemic treatment. There's some topical creams, but it's the one for higher body surface area.
So both of these markets are very, very small right now. I mean, if you look at the sales, they're in the small hundreds of millions of dollars. But if you look at their prevalence, they're quite high. And so that's the same way Crohn's was back in the day in ulcerative colitis, et cetera. So we see that we're going to have to build the market. We see that Rinvoq will have the most favorable data in the category for the foreseeable future. So that's also very positive.
And we are anticipating with the label that we will have more -- now for moderate to severe patients more of a frontline type approach versus stepping through because there's really nothing to step through. You sort of have a naive market. And it's quite similar to what we saw with our GCA label, which is the smallest of the next one. So we believe that these markets can become quite meaningful. We have increased our guidance based on the quality of the data, but we'll be the ones with the heavy lifting, and we plan to do that with expanding our dermatology sales forces around the world, and that's been underway.
So we are going to invest into these indications. And certainly, in the U.S., we would also anticipate pretty robust consumer activation because we find that the vitiligo and alopecia patients there's been nothing for them. So they're sort of sitting on the sideline. So that's the combination of the approaches there. We're certainly encouraged with the data and our ability to build those markets into the LRP.

**Elizabeth Shea** (Executives):
Thanks, Gary. That concludes today's conference call. If you'd like to listen to a replay of the call, please visit our website at investors.abbvie.com. Thanks again for joining us.

**Operator** (Operator):
This concludes today's call. Thank you for your participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ABBV_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜Scott Reents (CFO)｜guidance：全年調整後 EPS 指引更新為 13.87–14.07 美元（原話："We are updating our full year adjusted"）
- 2026-07-31｜Scott Reents (CFO)｜guidance：EPS 指引含本業改善 0.10 美元與 Apogee 稀釋 0.14 美元（原話："a $0.10 improvement in the outlook of our existing business"）
- 2026-07-31｜Scott Reents (CFO)｜guidance：全年營收指引上調 3 億美元至約 676 億美元（原話："total net revenues of approximately $67.6 billion"）
- 2026-07-31｜Scott Reents (CFO)｜guidance：EPS 指引不含 Q2 之後可能發生的收購 IPR&D 費用（原話："does not include an estimate for acquired IPR&D expense"）
- 2026-07-31｜Scott Reents (CFO)｜guidance：Skyrizi 全年營收預估 217 億美元，上調 1 億（原話："We now expect Skyrizi"）
- 2026-07-31｜Scott Reents (CFO)｜guidance：神經科學全年營收 127 億美元，含 Vraylar 與 Botox Therapeutic 預估（原話："Total neuroscience revenues of $12.7 billion"）
- 2026-07-31｜Scott Reents (CFO)｜guidance：Q3 營收與 EPS 指引（原話："We also forecast"）
- 2026-07-31｜Scott Reents (CFO)｜margin：Q2 調整後毛利率、R&D、SG&A 占比及營業利益率口徑（原話："Adjusted gross margin was 84.7% of sales"）
- 2026-07-31｜Scott Reents (CFO)｜margin：Q2 營業利益率 48.3%，含 1.7% 的收購 IPR&D 不利影響（原話："The adjusted operating margin was 48.3% of sales"）
- 2026-07-31｜Scott Reents (CFO)｜margin：全年毛利率、營業利益率及費用指引（原話："adjusted operating margin ratio approaching 47%"）
- 2026-07-31｜Scott Reents (CFO)｜margin：全年淨利息費用上調 2 億美元，反映 Apogee 融資成本（原話："reflects the partial year financing cost"）
- 2026-07-31｜Scott Reents (CFO)｜commitment：承諾在 Apogee 交割後 2–3 年內將淨槓桿降至 2 倍（原話："committed to achieving a net leverage ratio of 2x"）
- 2026-07-31｜Scott Reents (CFO)｜commitment：預期 Apogee 交易於第三季交割（原話："the Apogee transaction will close in the third quarter"）
- 2026-07-31｜Scott Reents (CFO)｜capital_allocation：已取得過渡性融資，預計未來數月發行長期債（原話："We have secured interim financing"）
- 2026-07-31｜Robert Michael (CEO)｜capital_allocation：CEO 稱有充足財務能力進行更多業務開發（BD）（原話："ample financial capacity for more business development"）
- 2026-07-31｜Robert Michael (CEO)｜product：Rinvoq 白斑與圓禿兩項適應症合計峰值銷售預期接近 20 億美元，高於先前預期（原話："these two indications alone to approach $2 billion"）
- 2026-07-31｜Robert Michael (CEO)｜product：Q2 營收與 EPS 表現及 Skyrizi、Rinvoq、神經科學成長（原話："Total net revenues were nearly $17 billion, beating our"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜product：Skyrizi Q2 銷售 55 億美元，營運基礎成長 24%（原話："Skyrizi total sales were"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜product：Humira 全球銷售 7.56 億美元，營運基礎下滑 36.1%（原話："Humira global sales"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜product：Imbruvica 下滑 29.4%，歸因 IRA 定價與競爭（原話："Imbruvica, which was down 29.4% as expected due to IRA"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜product：美容事業 Q2 營運基礎下滑 0.9%；Juvederm 下滑 6.6%，歸因主要皮下填充劑市場逆風（原話："reflecting continued headwinds in key dermal filler markets"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜product：Vyalev 預計今年達重磅銷售；巴金森氏症組合峰值維持逾 50 億美元（原話："We continue to expect collective"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜product：tavapadon 上市初期爬坡緩慢，歸因醫療保險處方集尚未納入，而非產品特性（原話："we do see that the ramp will be modest at first"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜product：Skyrizi 皮下誘導給藥若獲批，預期明顯加速，但實際放量要到 2027 年初（原話："we'll probably start seeing that really early in '27"）
- 2026-07-31｜Roopal Thakkar (CSO)｜product：Skyrizi 皮下誘導治療克隆氏症的 FDA 核准決定預期在今年秋季（原話："approval decision expected later this fall"）
- 2026-07-31｜Roopal Thakkar (CSO)｜product：Rinvoq 白斑美國核准預期今年稍後、圓禿明年初（原話："this year for vitiligo and early next year for alopecia"）
- 2026-07-31｜Roopal Thakkar (CSO)｜product：tavapadon FDA 核准決定預期在第三季（原話："an FDA approval decision is expected in the"）
- 2026-07-31｜Roopal Thakkar (CSO)｜product：Skyrizi 加 anti-α4β7 在克隆氏症的中期結果顯示內視鏡緩解加倍（原話："demonstrated a doubling of endoscopic remission at week 24"）
- 2026-07-31｜Roopal Thakkar (CSO)｜product：IBD 組合療法的 Phase III 啟動預期時程為 2028 年上半年（原話："hopefully, in the first half"）
- 2026-07-31｜Roopal Thakkar (CSO)｜product：etentamig 第三季進行 PFS 期中分析，若為正向則年內送件（原話："regulatory submission would occur"）
- 2026-07-31｜Roopal Thakkar (CSO)｜product：emraclidine 100 毫克耐受性良好，150 毫克評估中，第四季開始 Phase II（原話："we remain on track to begin Phase II studies"）
- 2026-07-31｜Roopal Thakkar (CSO)｜product：Temab-A 於難治轉移性大腸癌獲突破性療法認定，Phase III 已在收案（原話："breakthrough therapy designation was granted for Temab-A"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜competition：管理層稱不預期現有或新療法對乾癬展望有重大影響（原話："We do not expect a material impact to our robust outlook"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜competition：回應 Icotyde（口服 IL-23）上市影響：Skyrizi 動能無實質變化，其份額主要來自另兩種口服藥（原話："We've not seen a material change in our momentum"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜competition：Skyrizi 新處方（NBRx）自 Icotyde 3 月上市後無下降，反而成長（原話："absolutely seen no degradation in any of our NBRx trends"）
- 2026-07-31｜Robert Michael (CEO)｜competition：CEO 稱這是擴大市場的競爭性上市，Skyrizi NBRx 成長加速（原話："we always viewed this as a market expanding competitive"）
- 2026-07-31｜Roopal Thakkar (CSO)｜competition：CRO 稱對 Skyrizi 的頭對頭研究，數據差距隨時間縮小（原話："the data gap closes over time."）
- 2026-07-31｜Jeffrey Stewart (CCO)｜competition：白斑領域尚無系統性療法獲批，Rinvoq 將是第一個（原話："there's no systemic"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜competition：Humira 生物相似藥競爭下滑符合預期（原話："reflecting biosimilar competition and in line"）
- 2026-07-31｜Robert Michael (CEO)｜risk：Skyrizi 專利：組成物專利 2033 到期，法規資料保護至 2031，預計本年代末才見生物相似藥申請（原話："we do not expect to see biosimilar application filings"）
- 2026-07-31｜Roopal Thakkar (CSO)｜risk：HS（化膿性汗腺炎）Phase III 風險：承認該領域曾有其他失敗，並說明試驗設計管理（原話："We have observed other failures in the space in HS over"）
- 2026-07-31｜Roopal Thakkar (CSO)｜risk：emraclidine 先前 EMPOWER 試驗的受體占有率低於期望（原話："was lower than what we would have wanted."）
- 2026-07-31｜Jeffrey Stewart (CCO)｜customer：支付方合約談判與往年一致，免疫領域為量驅動、讓價為低個位數（原話："low single-digit concessions around rebates"）
- 2026-07-31｜Jeffrey Stewart (CCO)｜customer：Skyrizi 皮下誘導讓部分醫師不必跨 Part B 與藥局兩個給付通路（原話："allows a certain segment of physicians to not have to work"）
- 2026-07-31｜Roopal Thakkar (CSO)｜customer：Apogee 收購後 AD 資產：全部平行推進，盡可能加速 anti-IL-13（原話："we are running all of them in"）


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
{"date":"20260525","verdict":"B 衛星候選（護城河 A 級 9/10 + cliff cohort 最成功 + Skyrizi+Rinvoq 已超 Humira peak + 53 年股息紀錄；但估值 🟡 合理非便宜 Fwd PE 15.13x + Pure MA 🟡 mid-range → 等回測 W104 $190 或 BB 下軌 $190 分批進場）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Skyrizi + Rinvoq 合計持續 +15-25% YoY 至 FY28","columns":{"2Y":"FY28 合計 ≥ $42B","5Y":"FY30 合計 ~$50B peak","10Y":"FY33 LOC 前維持","數字":"S+R FY26 mid $31.8B → FY28 ≥ $42B","來源":"Q1 26 mgmt 上修 guide","漂移":"連 2 季合計"}},{"id":"H2","text":"Pipeline（neuroscience + oncology + obesity）合計 FY28 ≥ $5B","columns":{"2Y":"Aliada + Cerevel + 其他","5Y":"FY30 ≥ $10B","10Y":"FY33 next cliff 替代主軸","數字":"—","來源":"R&D + 投資人 day","漂移":"FY28"}},{"id":"H3","text":"估值倍數維持 14-17x 區間，dividend 持續增長 5-8%/年","columns":{"2Y":"2027 Fwd PE 14-17x","5Y":"持平","10Y":"—","數字":"—","來源":"§13.1","漂移":"連 4 季 Fwd PE"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":214.5,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABBV_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
