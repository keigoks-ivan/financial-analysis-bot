你是 stock-analyst **v20 判斷 agent**，標的 CRWV（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CRWV","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":2575,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","citation":"公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx"},"note":"未取得 consensus（查無）"},{"id":"f_kpi1_non_gaap_adjusted_operat","label":"Non-GAAP (adjusted) operating income","value":128,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","unit":"USD M（利益率 5.0%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","citation":"公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx"},"note":"未取得 consensus（查無）"},{"id":"f_kpi2_gaap_operating_income_lo","label":"GAAP operating income (loss)","value":-49,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","unit":"USD M（利益率 -1.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","citation":"公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx"},"note":"未取得 consensus（查無）"},{"id":"f_kpi5_guidance_q3_2026","label":"Guidance Q3 2026","value":"營收 3,450–3,600；adjusted operating income 200–260；利息費用 860–940；capex 11,500–13,500","period":"Q3 2026 指引（2026-08-11 法說會）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026 指引（2026-08-11 法說會）","citation":"新聞稿未載指引；取自 MarketBeat 法說會摘要 https://www.marketbeat.com/instant-alerts/coreweave-q2-earnings-call-highlights-2026-08-11/（二手，需對照逐字稿）"},"note":"未取得"},{"id":"f_kpi6_guidance_fy2026","label":"Guidance FY2026（上調）","value":"營收 12,400–13,200；adjusted operating income 960–1,150；capex 35,000–39,000；年底年化營收 18,500–19,500；年底 active power >1.85 GW（前 >1.7 GW）","period":"FY2026 指引（2026-08-11 法說會）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"FY2026 指引（2026-08-11 法說會）","citation":"同上 MarketBeat（二手）"},"note":"未取得"},{"id":"f_kpi7_revenue_backlog","label":"Revenue backlog","value":104,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","unit":"USD B（不含早 Q3 新增逾 25B 承諾）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","citation":"公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx"},"note":"n/a"},{"id":"f_kpi8_active_power_contracted_","label":"Active power／Contracted power","value":"1.5 GW／約 3.7 GW","period":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","citation":"公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-11","period":"2026-08-11","unit":"date","basis":"距今 44 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-11"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_crwv_gross_margin_pct","label":"CRWV 毛利率","value":67.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crwv_operating_margin_pct","label":"CRWV 營業利益率","value":-3.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crwv_fcf_margin_pct","label":"CRWV FCF 利潤率","value":-179.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nbis_gross_margin_pct","label":"NBIS 毛利率","value":74.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NBIS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nbis_operating_margin_pct","label":"NBIS 營業利益率","value":-50.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NBIS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nbis_fcf_margin_pct","label":"NBIS FCF 利潤率","value":-434.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NBIS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_orcl_gross_margin_pct","label":"ORCL 毛利率","value":63.96,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ORCL.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_orcl_operating_margin_pct","label":"ORCL 營業利益率","value":34.23,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ORCL.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_orcl_fcf_margin_pct","label":"ORCL FCF 利潤率","value":-40.01,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ORCL.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"}},{"id":"f_peer_iren_gross_margin_pct","label":"IREN 毛利率","value":62.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IREN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_iren_operating_margin_pct","label":"IREN 營業利益率","value":-53.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IREN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_iren_fcf_margin_pct","label":"IREN FCF 利潤率","value":-332.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IREN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow_679_capex","label":"Free cash flow（營運現金流 679 減 capex 6,422，自算）","value":-5743,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","citation":"公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx（OCF 679、purchase of PP&E 6,422；公司未報 FCF，此為自算）"},"note":"n/a"},{"id":"f_kpi4_sbc","label":"SBC 占營收","value":6.4,"period":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","unit":"%（SBC 165 USD M ÷ 營收 2,575；GAAP 營業利益為負故以營收為分母）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 2026（季末 2026-06-30，公告於 2026-08-11）","citation":"公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx"},"note":"n/a"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":82.08,"period":"2026-10-09（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-19.53,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.71,"period":"2026-10-09（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.25,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-3.95 → -3.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.55,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-1.82 → -1.81）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":7.76,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.16 → 1.25）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-3.94,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":-1.81,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":1.25,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.65,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS -3.66 → -3.94（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.96,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":12.03,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":46074.0,"period":"2026-10-12","unit":"USD m","basis":"yfinance 最新一季：總債務 51613.0、現金 5539.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-12"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":551.54,"period":"2026-10-12","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-12"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":91344.12,"period":"2026-10-12","unit":"USD m","basis":"市值 45270.12 ＋ 淨負債 46074.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-12"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":12869.75,"period":"2026-10-12","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（40 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-12"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":26295.93,"period":"2026-10-12","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（40 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-12"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":7.1,"period":"2026-10-12","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-12"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"CoreWeave 仍為營收規模最大的 neocloud：2026 Q2 營收約 $2.58B，對比 Nebius $582M、IREN $137M；backlog 約 $104B。","source":"Constellation Research: CoreWeave Q2 stronger than expected, touts backlog（搜尋彙整亦引 Stocktwits、Daloopa）","url":"https://www.constellationr.com/insights/news/coreweave-q2-stronger-expected-touts-backlog","excerpt":null,"as_of":"2026-08-12","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"同業 Nebius、Lambda、Crusoe、Groq 在價格、合約與電力取得上競爭；有來源列 Nebius 的 H100 on-demand 價格最低而 CoreWeave 維持價格溢價；IREN 近期取得 $9.7B Microsoft 合約；CoreWeave 在 SemiAnalysis ClusterMAX 2.0 評為 Platinum。","source":"Diario Bitcoin: CoreWeave, Nebius, Lambda, Crusoe y Groq: la batalla por el cómputo de IA en 2026","url":"https://www.diariobitcoin.com/negocios/coreweave-nebius-lambda-crusoe-y-groq-la-batalla-por-el-computo-de-ia-en-2026/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"客戶集中：兩家客戶約占 2026 上半年營收 40% 與 23%；Meta 在先前 $14B 合約外再增 $21B 承諾；另有與 Anthropic 的協議。","source":"Constellation Research / Invezz (2026-04-15)","url":"https://invezz.com/au/news/2026/04/15/heres-why-the-coreweave-stock-price-rally-is-set-to-accelerate/","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261012","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Bloomberg 2026-03-25 報導 IPO 一年來 CRWV 股價落後對手 Nebius；247WallSt 2026-09-22 文章標題指兩者中其一更暴露於即將到來的 neocloud 威脅（內文未讀取）。","source":"Bloomberg: In Wild Year Since IPO, CoreWeave Stock Is Lagging Rival Nebius; 24/7 Wall St","url":"https://247wallst.com/investing/2026/09/22/coreweave-vs-nebius-one-is-much-more-exposed-to-the-looming-neocloud-threat/","excerpt":"CoreWeave Vs. Nebius: One is Much More Exposed to The Looming Neocloud Threat","as_of":"2026-09-22","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"CoreWeave 2026 Q2 10-Q 表示預期少數大客戶集中度將持續（合約長期性），且大客戶需求或履約意願的不利變化會衝擊業績；未見其揭露最大客戶導入第二供應商或自製。","source":"CoreWeave Form 10-Q (period ended 2026-06-30), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000366/crwv-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"CoreWeave 2026 Q1 10-Q 稱 Meta 於 2026-03 簽訂約 $21B 訂單、預期成為重要客戶；客戶基礎由 Microsoft 擴向 OpenAI、Meta（搜尋摘要轉述，數字未對照原文）。","source":"CoreWeave Form 10-Q (period ended 2026-03-31), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000222/crwv-20260331.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"OpenAI 與 Broadcom 宣布 10GW 自研加速器合作，2026 下半年起部署、2029 年底完成；晶片初期用於 OpenAI 自家資料中心。報導無 CoreWeave 專屬資訊，亦未確認 2026 出貨進度。","source":"Capital Brief / Yahoo Finance / Outlook Business 報導 OpenAI-Broadcom 10GW deal","url":"https://www.capitalbrief.com/briefing/openai-and-broadcom-ink-10gw-chip-deal-070c8d1b-1d47-406a-87ae-98fae1ee81e4/","excerpt":null,"as_of":"2025-10-13","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Q1 2026 10-Q：前兩大客戶合計約占營收 65%（約三分之二），無其他客戶達 10%；去年同期最大客戶單獨約 72%","source":"SEC EDGAR CoreWeave 10-Q 期間 2026-03-31（經搜尋摘要轉述，未開頁面核對）","url":"https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000222/crwv-20260331.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"第三方 sec-api 分析稱最大客戶占比 Q1 2026 為 45%、Q2 2026 為 36%，第二大 26%、第三大 10%；未具名客戶，未與 10-Q 原文核對","source":"sec-api.io insights: CoreWeave CRWV 2026 revenue analysis top customer concentration exposure","url":"https://sec-api.io/insights/coreweave-crwv-2026-revenue-analysis-top-customer-concentration-exposure","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Q2 2026 10-Q 風險語言：預期因長約，營收仍將集中於少數大客戶；這些客戶需求或履約能力的負面變化會損害業績","source":"SEC EDGAR CoreWeave 10-Q 期間 2026-06-30（經搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000366/crwv-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Meta 2026 年 3 月訂單承諾最高約 $210 億；OpenAI 主服務協議承諾最高約 $65 億（至 2031/5）；公司預期兩者成為重要客戶","source":"SEC EDGAR CoreWeave 10-Q 期間 2026-03-31（經搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000222/crwv-20260331.htm","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"OpenAI（主要非超大規模客戶）無公開信用評等；第三方報導稱截至 2026-03-31 無負債但採購承諾約 $6,650 億（未審計、非公開文件），2026 年初單季燒現金約 $37 億；IFR 估計供應商帳單到期將出現約 $200 億缺口","source":"Vested Finance community / IFR 'OpenAI faces financial crunch point as huge supplier bills start to come due'（二手報導）","url":"https://www.ifre.com/people-and-markets/2373243/openai-faces-financial-crunch-point-as-huge-supplier-bills-start-to-come-due","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Goldman Sachs expects AI infrastructure supply and demand may not rebalance until 2028; its 2027 hyperscaler capex base case is about $1.1T (bull $1.4T).","source":"fourweekmba / kucoin blog summaries of Goldman Sachs (secondary)","url":"https://www.kucoin.com/blog/th-ai-infrastructure-shortage-may-last-until-2028-as-hyperscaler-capex-keeps-rising","excerpt":null,"as_of":"2026-09-25","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Sell-side 2027 hyperscaler capex: Morgan Stanley $1.2T in 2027 (+30%) with $1.4T upside in 2028; UBS models capex growth slowing from 76% (2026) to 25% (2027) and 6% (2028).","source":"roic.ai Morgan Stanley / Goldman news pages; UBS via search summary (secondary)","url":"https://www.roic.ai/news/morgan-stanley-sees-cloud-spending-surging-to-12t-08-03-2026","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner (Nov 2024 forecast) predicts power shortages will restrict 40% of AI data centers by 2027; new grid capacity approvals reportedly take 24-36 months. Power is cited as binding constraint on new capacity.","source":"Data Center Knowledge: Power Shortages Will Restrict 40% of AI Data Centers By 2027 – Gartner","url":"https://www.datacenterknowledge.com/energy-power-supply/power-shortages-will-restrict-40-of-ai-data-centers-by-2027-gartner","excerpt":null,"as_of":"2024-11-19","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Spheron (GPU-cloud vendor) says GPU availability has improved over the past 18 months with neo-clouds and resellers offering H100/H200/Blackwell capacity; scarce input shifting from GPUs to grid connections. Vendor-biased source; no independent 2027 price forecast found.","source":"Spheron blog: AI data center power constraints 2026","url":"https://www.spheron.network/blog/ai-data-center-power-constraints-2026/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CoreWeave backlog $99.4B at 2026-03-31 (vs $25.9B a year earlier); ~36% converts to revenue within 24 months, ~75% within four years; weighted average contract length about five years. Q1 2026 adjusted operating income $21M vs $163M a year earlier; adjusted net loss $589M; third-party data center delays accepted by customers with full contract value kept.","source":"Futurum: CoreWeave Q1 FY 2026 Capacity Constraints Amid Accelerating AI Demand; Nasdaq/Zacks summaries","url":"https://futurumgroup.com/insights/coreweave-q1-fy-2026-capacity-constraints-amid-accelerating-ai-demand/","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261012","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-Q（期間 2026-06-30）風險因素稱 AI 與雲端服務產業因市場集中、反競爭行為等受監管機關日益審視；搜尋三輪未發現針對 CoreWeave 的 DOJ／FTC／EU 反壟斷調查。","source":"CoreWeave Form 10-Q FY2026 (period ended 2026-06-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000366/crwv-20260630.htm","excerpt":"AI and related industries, including cloud services, are under increasing scrutiny from regulators due to their concerns about market concentration, anti-competitive practices, environmental harm, misuse of AI","as_of":"2026-06-30","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-Q 提及聯邦與州層級 AI 法規、跨轄區規則衝突，可能放慢客戶對平台的需求。","source":"CoreWeave Form 10-Q FY2026 (period ended 2026-06-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001769628/000176962826000366/crwv-20260630.htm","excerpt":"The difficulty of achieving compliance is exacerbated by conflicting regulations in different jurisdictions without a unified set of regulations.","as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Blockspace 報導：CEO Intrator 稱地方資料中心禁建令會改變建設地點而非減少需求；紐約州行政命令暫停大型新資料中心（≥50MW）部分環評核准最長一年。報導日期未能核實。","source":"Blockspace Media, 'CoreWeave shifts data center sites amid moratoriums'","url":"https://blockspace.media/insight/coreweave-shifts-data-center-sites-amid-moratoriums/","excerpt":null,"as_of":"2026-08-12","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國 Section 232 對特定先進運算晶片課 25% 關稅，2026-01-15 生效；供美國資料中心使用的進口半導體列為豁免（來源未直接提及 CoreWeave）。","source":"Thomson Reuters OneSource, Trump administration imposes tariffs on advanced AI chips under Section 232 authority","url":"https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/january-15th/trump-admin-tariffs-advanced-ai-chips-232.html","excerpt":"The new Section 232 tariff will not apply to imported semiconductors for use in U.S. data centers, repairs or replacements performed in the U.S., research and development in the U.S., and use by startups, among other listed uses.","as_of":"2026-01-15","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"商務部長須於 2026-07-01 前提交美國資料中心用半導體市場更新，作為調整關稅制度依據；本軸未查到該更新內容。總統保留日後擴大課稅權限。","source":"White & Case, President Trump orders narrowly targeted 25% Section 232 tariff on certain advanced semiconductor articles","url":"https://www.whitecase.com/insight-alert/president-trump-orders-narrowly-targeted-25-section-232-tariff-certain-advanced","excerpt":"This represents a narrowly targeted initial phase focused on high-performance AI-enabling semiconductors.","as_of":"2026-01-15","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"眾議院 2026-01-12 以 369-22 通過 Remote Access Security Act，針對外國對手經雲端遠端取用受管制技術；該頁稱 BIS 目前不視提供雲端運算為出口。是否成為法律本軸未查到。","source":"cmtradelaw.com BIS tag page","url":"https://www.cmtradelaw.com/tag/bis/","excerpt":null,"as_of":"2026-01-12","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"未查到 CoreWeave 被列入 Entity List 或受出口管制/中國關稅之公司層級報導。","source":"WebSearch results (no CoreWeave-specific hit)","url":null,"excerpt":null,"as_of":"2026-10-12","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 一般性風險因素把中國與台灣緊張、關稅、貿易管制列為可能壓抑需求與定價的總體地緣因素；摘要未顯示公司在兩地有直接營運或供應商。","source":"CoreWeave Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2025 年底第三方資料中心供應商未如期交付，致 CoreWeave 下修全年營收預測；管理層稱延遲多數於 2026 年 Q1 解決。","source":"Bisnow: Data Center Delays Trigger Sell-Off Of AI Cloud Firm CoreWeave","url":"https://www.bisnow.com/news/national/data-center-capital-markets/data-center-delays-trigger-selloff-of-ai-cloud-firm-coreweave-131860","excerpt":null,"as_of":"2025-11-10","retrieved_at":"20261012","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 年 3 月會議摘要：供應鏈執行『極其困難』，並區分電網可得性與實際送達機櫃的可用電力。","source":"MarketBeat: CoreWeave conference, 2026 compute capacity broadly sold out","url":"https://www.marketbeat.com/instant-alerts/coreweave-conference-insatiable-ai-demand-leaves-2026-compute-capacity-broadly-sold-out-2026-03-08/","excerpt":null,"as_of":"2026-03-08","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2026 年 1 月報導：川普對數個歐洲國家的關稅威脅衝擊 CoreWeave 股價，因其在挪威、瑞典、英國等地興建資料中心。","source":"Finviz: What's happening with CoreWeave stock this week","url":"https://finviz.com/news/282857/whats-happening-with-coreweave-stock-this-week","excerpt":null,"as_of":"2026-01-20","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"CoreWeave Q2 2026（2026-08-11 公布）營收約 $2.6B，年增 112%、季增約 24%；backlog $104.2B（RPO $103.7B），另有 >$25B 新承諾於 Q3 初新增、未計入。","source":"CoreWeave investor release 'CoreWeave Reports Strong Second Quarter 2026 Results'; Quartr; Pulse 2.0（二手摘要）","url":"https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/","excerpt":null,"as_of":"2026-08-11","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"2026 全年營收指引上調至 $12.4–13.2B；Q3 指引 $3.45–3.6B；2026 capex 上調至 $35–39B（原 $31–35B）；Q2 GAAP 淨損 $626M、利息費用 $640M；約 41% RPO 於未來 24 個月認列。","source":"CoreWeave Q2 2026 results 二手摘要（Pulse 2.0／Beancount.io／Quartr）","url":"https://pulse2.com/coreweave-revenue-backlog-reaches-104-billion-before-another-25-billion-of-new-commitments/","excerpt":null,"as_of":"2026-08-11","retrieved_at":"20261012","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"KGI 報告：前五大雲端業者 2026 capex 指引上修至約 $753bn（年增 83%），2027 約 $922bn，市場預期五大超大規模業者 2027 capex 超過 $1.0tn。","source":"KGI Securities, IT hardware report (July 2026)","url":"https://www.kgi.com.hk/zh-cn/-/media/files/kgishk/research-reports/tw-reports/it-hardware_01072026e.pdf","excerpt":"2026 capex growth guidance from the top five CSPs was revised up to US$753bn, up 83% YoY, and the market expects five major hyperscalers' 2027F capex to grow to over US$1.0tn.","as_of":"2026-07-01","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"ABI Research 預估 neocloud GPUaaS 營收 2030 年約 $250bn，推論占比 2030 達 80%；北美占比自 2026 的 88% 降至 2030 的 72%。","source":"ABI Research, 'neocloud market trends'","url":"https://abiresearch.com/blog/neocloud-market-trends","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"-","claim":"Contrary Research（2026-06）認為受融資與需求規模要求，許多較小 neocloud 難以存活。","source":"Contrary Research, 'why 20% of neoclouds won't survive the AI boom'","url":"https://research.contrary.com/report/why-20-of-neoclouds-wont-survive-the-ai-boom","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"CoreWeave 公開 on-demand 牌價：H100 $6.16／GPU-hr、B200 約 $8.60、GB200 NVL72 $10.50；Nebius H100 約 $3.85，CoreWeave 高約 60%。所謂 7 月調價 25% 未證實（頁面價格 7–8 月不變）；CFO「largely sold out」說法僅單一二手來源、未對證財報。牌價為競品／供應商部落格資料，合約價可能不同。","source":"Spheron blog（CoreWeave GPU pricing 2026 系列）；CloudZero","url":"https://www.spheron.network/blog/coreweave-gpu-pricing-2026/","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"TAM 估計分歧大：MarketsandMarkets AI infrastructure 2030 達 $394.46B（CAGR 19.4%）；GPU-as-a-Service 2030 約 $26.62B（CAGR 26.5%）；Lucintel AI infrastructure 2030 約 $123.9B；DeployBase GPU cloud 2030 $80–120B（CAGR 35–45%，來源不明）。定義不同不可直接比較。","source":"MarketsandMarkets／Barchart；Lucintel；DeployBase","url":"https://www.barchart.com/story/news/33626774/gpu-as-a-service-market-worth-26-62-billion-by-2030-at-a-cagr-of-26-5","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Hyperscaler custom AI ASICs（Google TPU、AWS Trainium3、Meta MTIA 等）擴張中；Broadcom 稱 2027 年 AI 晶片營收有超過 1000 億美元的能見度、已揭露 730 億美元 AI 積壓訂單；TPU v6e 在 Google Cloud 按需 $2.70／chip-hour（價格效能為 Google 自家基準）","source":"Tom's Hardware, The custom AI ASIC state of play (May 2026)","url":"https://tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia","excerpt":"Trainium3, which went generally available at re:Invent in December, is AWS's first 3nm chip.","as_of":"2026-05-31","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"第三方部落格（Introl, 2026-02）預測客製 ASIC CAGR 約 44.6%、主攻推論，並稱 Nvidia 推論市占 2028 年可能由 90%+ 降至 20–30%；屬二手預測，來源權威性較低","source":"Introl, The Custom Silicon Inflection Point (Feb 2026)","url":"https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu","excerpt":"NVIDIA responds with Vera Rubin (50 PFLOPS FP4, 288GB HBM4), but analysts project its inference market share could fall from 90%+ to 20-30% by 2028.","as_of":"2026-02-28","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"CoreWeave 以六年（2023 年前為五年）折舊 GPU；批評者（含 Burry）認為 Nvidia 年度換代使舊硬體 2–3 年即經濟性過時；公司反駁稱 H100 到期後以原價 95% 再簽約。日期為文章發布日未確認，來源多為評論／電子報","source":"Yahoo Finance / Electroneconomics Substack 等評論（搜尋摘要彙整）","url":"https://electroneconomics.substack.com/p/the-depreciation-clock-coreweaves","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear","valuation","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"CoreWeave 透過併購建軟體層：Weights & Biases（約 $1.029B，2025-05 完成），2025 年底再加 OpenPipe、Monolith AI、Marimo；搜尋結果未見正式轉向軟體導向營收的商業模式宣告。","source":"Sacra, CoreWeave profile","url":"https://sacra.com/c/coreweave/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 2026 法說：管理層稱核心客戶（超大型雲端與基礎模型實驗室）加深承諾，同時有新一波企業客戶進入；Q1 新增承諾逾 $400 億、積壓訂單近 $1,000 億。","source":"CoreWeave Q1 2026 earnings call (2026-05-07)","url":"https://s205.q4cdn.com/133937190/files/doc_financials/2026/q1/CoreWeave-Inc-CRWV-US-Q1-2026-Earnings-Call-7-May-2026-5_00-PM-ET.pdf","excerpt":"our core customers, historically hyperscalers and foundation labs, are deepening their commitment to us, while an entirely new wave of enterprises are arriving","as_of":"2026-05-07","retrieved_at":"20261012","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 價目頁（收盤日 2026-09-04）：31 位分析師、共識 Buy、平均目標價 $140；21 Buy、2 Strong Buy、7 Hold、1 Sell；Truist 8/24 升目標價至 $165、Goldman 8/21 升至 $139。為 9 月初快照，無 10 月數據。","source":"Benzinga CRWV price targets","url":"https://www.benzinga.com/quote/CRWV/price-targets","excerpt":"Benzinga's price-target page, showing a close on Sep 4, lists 31 analysts with a consensus rating of Buy, and an average price target of $140.","as_of":"2026-09-04","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026 財報（約 8/11）上調 FY2026 營收指引至 $12.4B–$13.2B、調整後營業利益 $960M–$1.15B，年底年化營收 run rate $18.5–19.5B；來源為二手摘要，非公司原文。","source":"Quartr / MarketBeat / channelchek 等 Q2 2026 財報摘要（經搜尋彙整）","url":"https://www.marketbeat.com/instant-alerts/coreweave-q2-earnings-call-highlights-2026-08-11/","excerpt":"Full-year 2026 revenue guidance was raised to $12.4B to $13.2B. Full-year 2026 adjusted operating income guidance was raised to $960M to $1.15B.","as_of":"2026-08-11","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026 capex 指引由 $31–35B 上調至 $35–39B；Q3 營收指引 $3.45–3.6B（二手來源）。公司表示後續投資可能需額外債務與/或股權融資。","source":"CoreWeave Q2 2026 earnings summaries (channelchek / indmoney / quartr)","url":"https://dashboard.channelchek.com/?p=104902","excerpt":"The company raised its full-year 2026 capital expenditure guidance to $35 billion to $39 billion, up from a prior range of $31 billion to $35 billion.","as_of":"2026-08-11","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 營收 $2.58B（年增 112%）略高於共識 $2.56B；淨損 $626M，利息費用 $640M。","source":"CoreWeave Q2 2026 earnings summaries","url":"https://www.indmoney.com/blog/us-stocks/crwv-stock-jumps-coreweave-q2-earnings-analysis","excerpt":"One source reports revenue of $2.58 billion, up 112% year over year, edging past the $2.56 billion analyst consensus.","as_of":"2026-08-11","retrieved_at":"20261012","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q1 後（2026-05-08）FY2026 營收指引維持 $12–13B、capex 區間下緣上調至 $31B（零組件漲價）；Q2 營收指引中點低於當時共識 $2.69B。7 月 Jefferies Buy、Barclays Equal Weight、Mizuho Neutral、Macquarie Outperform 皆重申無評等變動；7 月後未見券商評等變動。","source":"搜尋彙整：Placera/Dow Jones 2026-05-08、聚合頁","url":"https://www.placera.se/telegram/coreweave-update-coreweave-q1-loss-narrows-revenue-rises-2026-capex-outlook-revised-shares-down-pre-bell-20260508","excerpt":"The company now projects capex between $31 billion and $35 billion, compared with its prior outlook range of $30 billion to $35 billion.","as_of":"2026-05-08","retrieved_at":"20261012","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2025-07-07 CoreWeave 宣布以全股票方式收購 Core Scientific（約 $9B，換股比 0.1235 CRWV/CORZ）；2025-10-30 因 Core Scientific 股東未批准而終止合併，維持商業合作。","source":"TipRanks: CoreWeave terminates merger with Core Scientific","url":"https://www.tipranks.com/news/company-announcements/coreweave-terminates-merger-with-core-scientific","excerpt":null,"as_of":"2025-10-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"聯邦證券集體訴訟 Masaitis v. CoreWeave（D.N.J., No. 2:26-cv-00355），class period 2025-03-28 至 2025-12-15，指控高估滿足客戶需求能力、低估對單一第三方資料中心供應商（Denton, TX）依賴之風險；主理原告截止日 2026-03-13。為原告律所新聞稿所述指控，非裁決。","source":"Berger Montague: CoreWeave securities fraud","url":"https://bergermontague.com/cases/coreweave-securities-fraud/","excerpt":null,"as_of":"2026-01-13","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"2025-11-10 Q3 結果下修 2025 年營收指引，原因為第三方資料中心開發商進度落後。","source":"Glancy Prongay Murray (BusinessWire): Securities Fraud Investigation Into CoreWeave","url":"https://www.businesswire.com/news/home/20260114050795/en/Securities-Fraud-Investigation-Into-CoreWeave-Inc.-CRWV-Announced-%E2%80%93-Shareholders-Who-Lost-Money-Urged-To-Contact-Glancy-Prongay-Murray-LLP-a-Leading-Securities-Fraud-Law-Firm","excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261012","affects":["thesis.R","valuation"],"status":"ok"},{"id":"unprofitable_nrr_rule40_band#none","axis":"unprofitable_nrr_rule40_band","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"unprofitable_dilution_trajectory#0","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"年度稀釋加權股數：2023 約403.7M、2024 404.4M、2025 436.0M（+7.8% YoY）；AlphaQuery 獨立列示 FY2025 為436.00M","source":"AlphaQuery / tickerleague 彙整（weighted average shares outstanding diluted）","url":"https://www.alphaquery.com/stock/CRWV/fundamentals/annual/weighted-average-shares-outstanding-diluted","excerpt":"CoreWeave diluted shares outstanding in 2024 was 404.41M, edged up 0.2% from 2023. and 2025's annual diluted shares outstanding for CoreWeave (CRWV) came in at 436.00M – grew 7.8% year-over-year.","as_of":"2025-12-31","retrieved_at":"20261012","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#1","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"聚合站Digrin列示SBC約每季$144M–$165M（2025Q3至2026Q2）；2025全年SBC約$630M，2024為$31.49M（聚合站數字，未對照10-K）","source":"Digrin CRWV Financials；tickerleague SBC expense（第三方彙整）","url":"https://www.digrin.com/stocks/detail/CRWV/financials","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261012","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#2","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"0","claim":"2026年基本股數快照分歧（Equibles：419.0M、428.2M、447.6M，日期未標；Substack 2026-01稱約497M；tickerleague稱最新稀釋527M但與+7.8%標示不一致），無法定出2026年增率；需以Q2 2026 10-Q核實","source":"Equibles CRWV；Substack「CoreWeave's Projected Shareholder Dilution in 2026」；tickerleague","url":"https://mschief1994.substack.com/p/coreweaves-projected-shareholder","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#3","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"TIKR稱CoreWeave併購Core Scientific（$9B全股票）完成時將顯著稀釋既有股東；是否已完成未查證","source":"TIKR blog：CoreWeave (NASDAQ: CRWV) stock tanks over 10% as investors are worried about narrowing margins","url":"https://www.tikr.com/blog/coreweave-nasdaq-crwv-stock-tanks-over-10-as-investors-are-worried-about-narrowing-margins","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#4","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"0","claim":"2026Q2營收約$2.575B（+112% YoY），營業損益$(49)M；搜尋未取得2026 SBC佔營收比的官方數字，SBC/營收比需由判斷層以上述SBC與營收自算","source":"MarketBeat：CoreWeave Q2 earnings call highlights 2026-08-11","url":"https://www.marketbeat.com/instant-alerts/coreweave-q2-earnings-call-highlights-2026-08-11/","excerpt":null,"as_of":"2026-08-11","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"unprofitable_path_to_profitability#0","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"+","claim":"Q2 2026 財報後管理層上調 2026 全年指引：營收 $12.4–13.2B、調整後營業利益 $960M–$1.15B；全年未給淨損或 FCF 轉正指引。","source":"MarketBeat, CoreWeave Q2 earnings call highlights (2026-08-11)","url":"https://www.marketbeat.com/instant-alerts/coreweave-q2-earnings-call-highlights-2026-08-11/","excerpt":"For the full year, CoreWeave raised revenue guidance to $12.4 billion to $13.2 billion and adjusted operating-income guidance to $960 million to $1.15 billion.","as_of":"2026-08-11","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"unprofitable_path_to_profitability#1","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"-","claim":"2026 資本支出指引上調至 $35–39B（原 $31–35B）；Q2 capex $9.4B，Q3 指引 $11.5–13.5B。","source":"MarketBeat, CoreWeave Q2 earnings call highlights (2026-08-11)","url":"https://www.marketbeat.com/instant-alerts/coreweave-q2-earnings-call-highlights-2026-08-11/","excerpt":"The company raised its full-year 2026 capital expenditure guidance to $35 billion to $39 billion, up from a prior range of $31 billion to $35 billion.","as_of":"2026-08-11","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"unprofitable_path_to_profitability#2","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"-","claim":"Q2 2026 調整後營業利益 $128M（5% 利潤率），淨損 $626M，利息費用 $640M；Q3 利息費用指引 $860–940M。管理層預期調整後營業利益率逐季擴張，Q4 達低十位數百分比（low-teens）。","source":"MarketBeat, CoreWeave Q2 earnings call highlights (2026-08-11)","url":"https://www.marketbeat.com/instant-alerts/coreweave-q2-earnings-call-highlights-2026-08-11/","excerpt":"Adjusted operating income was $128 million, a 5% margin. Net loss was $626 million, driven by $640 million interest expense due to increased debt.","as_of":"2026-08-11","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"unprofitable_path_to_profitability#3","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"-","claim":"2025 年 FCF 約 -$7.25B（營運現金流 $3.1B、capex $10.3B）；『FCF 轉正』為第三方分析預期，非公司目標。","source":"DefiLlama dashboard, CRWV revenue streams and P/E","url":"https://defillama.com/pro/crwv-revenue-streams-and-p-e-ennlo2","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_path_to_profitability#4","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"-","claim":"2025 年底總債務約 $29.82B；管理層稱燒錢屬刻意前置、已鎖定約 300bp 較低借款成本，但有分析稱年度數字尚未印證。","source":"TIKR, CoreWeave's $640M interest bill is growing faster than its $128M profit","url":"https://www.tikr.com/blog/coreweaves-640m-interest-bill-is-growing-faster-than-its-128m-profit-but-management-says-the-burn-is-by-design-heres-what-investors-need-to-know","excerpt":"Management says CoreWeave front loads the burn by design and has already locked in nearly 300 basis points of lower borrowing costs","as_of":"2026-08-15","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"-","claim":"2025-07-07 宣布全股票收購 Core Scientific（約 $9B）；2025-10-30 因 CORZ 股東否決而終止。搜尋未見 2026 年新的併購協議。","source":"TipRanks: CoreWeave terminates merger with Core Scientific","url":"https://www.tipranks.com/news/company-announcements/coreweave-terminates-merger-with-core-scientific","excerpt":null,"as_of":"2025-10-30","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Masaitis v. CoreWeave（D.N.J. 2:26-cv-00355）證券詐欺集體訴訟，class period 2025-03-28~2025-12-15，Section 10(b)/20(a)；另有第二件類似訴狀；主理原告截止 2026-03-13。屬指控非裁決。","source":"Berger Montague: CoreWeave securities fraud","url":"https://bergermontague.com/cases/coreweave-securities-fraud/","excerpt":null,"as_of":"2026-01-13","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"CRWV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.42,"operating_margin_pct":-3.04,"fcf_margin_pct":-179.92,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRWV","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"NBIS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.26,"operating_margin_pct":-50.48,"fcf_margin_pct":-434.2,"rd_intensity_pct":26.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NBIS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ORCL","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":63.96,"operating_margin_pct":34.23,"fcf_margin_pct":-40.01,"rd_intensity_pct":14.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ORCL","as_of":"TTM ending 2026-08-31（4季加總）"}},{"name":"IREN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":62.32,"operating_margin_pct":-53.57,"fcf_margin_pct":-332.45,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IREN","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"CRWV"},"financial_history":{"ticker":"CRWV","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":15830000.0,"revenue_yoy_pct":null,"gross_margin_pct":23.42,"operating_margin_pct":-144.54,"net_income":-31055000.0,"diluted_eps":-0.076921,"free_cash_flow":-71494000.0,"fcf_margin_pct":-451.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":229000000.0,"revenue_yoy_pct":1346.62,"gross_margin_pct":69.87,"operating_margin_pct":-6.11,"net_income":-594000000.0,"diluted_eps":-1.471291,"free_cash_flow":-1110000000.0,"fcf_margin_pct":-484.72,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":1915000000.0,"revenue_yoy_pct":736.24,"gross_margin_pct":74.26,"operating_margin_pct":16.92,"net_income":-863000000.0,"diluted_eps":-2.018966,"free_cash_flow":-5953000000.0,"fcf_margin_pct":-310.86,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5131000000.0,"revenue_yoy_pct":167.94,"gross_margin_pct":71.68,"operating_margin_pct":-0.9,"net_income":-1167000000.0,"diluted_eps":-2.81,"free_cash_flow":-7251000000.0,"fcf_margin_pct":-141.32,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CRWV/CRWV_Q2_2026_Earnings_Call_20260811.md）

# Q2 2026 Earnings Call
2026-08-11

Q2 2026 Earnings Call
CoreWeave, Inc. | Earnings Calls | 2026-08-11
Operator (Operator)
Hello, everyone. Thank you for joining us, and welcome to CoreWeave's Second Quarter 2026 Earnings
Call. [Operator Instructions] I will now hand the conference over to CoreWeave. Please go ahead.
Unknown Executive (Executives)
Thank you. Good afternoon, and welcome to CoreWeave's Second Quarter 2026 Earnings Conference
Call. Joining the call today to discuss our results are Mike Intrator, CEO; and Nitin Agrawal, CFO.
Before we get started, I would like to take this opportunity to remind you that our remarks today will
include forward-looking statements. Actual results may differ materially from those contemplated by
these forward-looking statements because of factors that are set forth in today's earnings press release
and in our quarterly report on Form 10-Q to be filed with the SEC. Any forward-looking statements that
we make on this call are based on assumptions as of today, and we undertake no obligation to update
these statements as a result of new information or future events.
During this call, we will present both GAAP and certain non-GAAP financial measures. A reconciliation
of GAAP to non-GAAP measures is included in today's earnings press release. The earnings press
release and an accompanying investor presentation are available on our website at
investors.coreweave.com. A replay of this call will also be available on our Investor Relations website.
And now I'd like to turn the call over to Mike.
Michael Intrator (Executives)
Good afternoon, everyone, and thank you for joining us. Q2 was an exceptional quarter for CoreWeave.
We outperformed our plan across the board with the operating leverage we have been building
beginning to show up clearly in our results. Extraordinary execution across the organization, drove
record financial performance, rapid capacity growth, broadening customer demand and continued
platform innovation.
We generated record revenue of $2.6 billion, up 112% year-over-year. Increased revenue backlog to
$104 billion (sic) [ $104.2 billion ] while driving rapidly expanding enterprise adoption. This figure
does not include the over $25 billion of net new customer commitments added in the early weeks of Q3.
We continue to execute on our power strategy, reaching 1.5 gigawatts of active power, adding nearly
500 megawatts, more than any quarter in our history and more than tripling year-over-year. We
remain firmly on track to reach at least 8 gigawatts by 2030. We grew adjusted operating income to
$128 million, with margins expanding meaningfully as our scale increasingly translates into operating
leverage, and we continue to broaden our technology stack, delivering 7 new AI platform capabilities,
and achieving multiple industry-first milestones that enable customers to build, deploy and operate AI
faster and at greater scale.
Our incredible progress is a testament to the entire organization, and the business is only getting
stronger. In Q2, the customer contracts we signed came with contribution margins we expect to be 5 to
10 percentage points above those added in recent quarters. This is more than a collection of milestones.

It is evidence that the AI market is developing in line with the convictions on which we built
CoreWeave.
We believe that the AI era is here and will ultimately touch every part of the global economy, that every
organization is being transformed, creating an opportunity to reinvent established markets and create
entirely new ones that the future will be led by the pioneers who seize that opportunity, both AI-native
companies at the frontier and change makers inside established enterprises. That learning and iterating
at light speed are now table stakes for AI leadership. And we believe those pioneers need a new kind of
platform to unleash AI's potential at scale. These beliefs are the operating assumptions that drive our
strategy. They guide our product road map, our capital allocation, our partnerships and ultimately, how
we serve our customers.
Today, I want to discuss how our vision is translating into 4 areas: one, broadening demand and
customer adoption; two, the continuous AI development tools we provide on our platform; three, the
performance and economics enabled by our AI native architecture; and four, the power and supply
chain foundation that will support years of growth. AI is transforming every organization. The debate
around future demand for AI cloud infrastructure will likely continue. But what we know with certainty
is informed by our customers' actions. Demand continues to intensify as the market broadens across
sectors, geographies, workloads and generations of GPU architecture.
AI is no longer confined to frontier model labs. It is becoming embedded in software, industrial
systems, financial markets, enterprise workflows and national security missions. We see that breadth in
our backlog, in the new commitments we have signed and in the utilization and pricing environment
across our platform. Pricing and margins for our Blackwell and Vera Rubin SKUs are setting new highs,
while pricing for prior generation SKUs is at or above where it was years ago. Our near-term capacity
remains effectively sold out. That is translating into signed commitments on increasingly favorable
terms from a broadening set of customers and is positioning CoreWeave to gain market share for years
to come.
Every organization is being challenged to rethink what is possible. AI is not simply accelerating existing
processes. It is enabling enterprises to redesign core functions, create new offerings and enter markets
that did not exist before. Caterpillar is a powerful example. Together, we will deploy NVIDIA's Vera
Rubin platform to support Caterpillar's physical AI training and inference at industrial scale. Using
CoreWeave's AI cloud infrastructure as its data factory, Caterpillar will train specialized models that
enhance the intelligence and productivity of autonomous construction equipment.
Life sciences is emerging as another important growth vertical for CoreWeave, as organizations tackling
some of the world's most complex scientific challenges increasingly turn to our platform. We recently
welcomed Isomorphic Labs as a new customer and are excited to support them in their mission to solve
all disease. Financial services remains a major growth area for us as well. We recently added Flow
Traders and IMC to our growing roster of systematic trading firms. These customers are using
CoreWeave to develop and deploy the next generation of AI models for quantitative trading. They select
our platform because of our ability to orchestrate high-performance workloads with the speed,
reliability and efficiency those applications require. And in the public sector, our collaboration with
Leidos marks an important step in the growth of CoreWeave Federal.
Together, we are working to accelerate the delivery of secure AI capabilities for defense, national
security, and intelligence missions. The future of AI is being built by a new class of innovators. Some

are AI native companies operating at the frontier. Others are change makers inside established
enterprises who are willing to challenge the status quo. CoreWeave serves both. Companies such as
Decart are using our platform to develop Oasis 3, the first API accessible world model for physical AI.
IBM is using CoreWeave to experiment securely with reinforcement learning, agent tool use and model
evaluation. And through Monolith, our specialist field engineers, work directly alongside customers
such as Nissan and ZF to accelerate the development of enterprise-ready AI applications.
Demand now extends beyond our infrastructure as well. Through CoreWeave Omni, we are seeing
significant interest from sovereign, enterprise and cloud customers alike. In the past few weeks, we
signed our first deal, which will begin to scale in 2027. These examples differ by industry and use case,
but the pattern is consistent, AI is moving from experimentation into core operations and the
organizations that act decisively are creating an advantage. Deployment is no longer the finish line. As
AI moves into production, the way applications are built is changing, and the leaders will be those who
learn and iterate the fastest.
For the last several years, many organizations treated a model like a deliverable, train it, deploy it and
move on. Enterprises no longer operate that way. Training, inference, evaluation and improvement
now form a single continuous loop. Models and agents in production generate real-world data. That
data informs evaluation, driving new experiments, which improve the model or application before
being redeployed into production.
The loop repeats and capability compounds over time. That shift fundamentally changes both the
demand curve and the economics of AI. Compute is no longer a onetime requirement concentrated at
the beginning of a model's life. It becomes an ongoing requirement that grows with every application in
production and every cycle of improvement. Our AI native platform was built for this. It spans cutting-
edge cloud infrastructure, a rapidly growing managed inference business, leading developer tooling and
agent solutions and a best-in-class orchestration and observability layer powered by mission control.
Together, these capabilities give customers one integrated environment. Customers deploy applications
through CoreWeave inference, using our models or the ones they have customized with our serverless
capabilities. Monitor performance with Weights & Biases, evaluate applications in production,
experiment with new models, refine their performance through serverless reinforcement learning or
sandboxes, and validate every change against quality, performance and cost before returning it to
production.
CoreWeave ARIA, our AI Research and Iteration Agent accelerates that process further by analyzing
thousands of evaluation runs, surfacing insights in minutes and recommending the next experiment.
That allows customers to compress the time between an idea and experiment and a production
improvement at light speed. In Q2, we introduced 7 new AI platform capabilities and achieved multiple
industry firsts. These innovations were built alongside our customers and partners to solve real
production challenges. That is why we are seeing such strong adoption. And just this week, we
surpassed 1 billion model training runs tracked on our platform. Behind that number are millions of
experiments, thousands of research breakthroughs, and a growing community of engineers, researchers
and organizations building the next generation of AI.
Our AI development services, which carry higher margins, are also being adopted by a broader set of
customers than our core cloud. That is proving to be a natural customer expansion path because the
developers building AI applications today are the AI cloud infrastructure customers of tomorrow. By

serving them early, we are establishing relationships that naturally expand as AI workloads scale. We
have seen an explosion of growth in our managed inference platform in the few months since its
launch, with growth constrained only by our near-term capacity. Across serverless offerings and
dedicated deployments, CoreWeave is monetizing tokens while giving customers flexibility in how they
consume our platform. Companies such as Grammarly and You.com are moving from experimentation
to real production traffic, running AI coding agents, serving their own fine-tuned models and deploying
open weight models at scale.
Customers shouldn't have to trade speed for cost. And on CoreWeave, they don't. They choose our
platform for the combination of total cost of ownership, quality, breadth of service and performance.
That is reflected in our consistent leadership across cost per token and speed to first token on
leaderboards like artificial analysis for open source models, including Kimi 2.6, K2.7 Code, GLM-5.2
and MiniMax M3. And that leadership is converting directly into revenue.
In the past few months since its launch, booked ARR for our managed inference platform has grown
from $1 million to more than $100 million. We expect to exit 2026 with at least $250 million of
managed inference ARR. Pioneers need a different kind of platform. The continuous AI life cycle cannot
be supported by simply adding GPUs to a general-purpose cloud. It requires a new approach from
power, cooling and rack design through networking, orchestration, observability, developer tools and
managed services. That is why CoreWeave is purpose-built for AI.
Our platform is singular in its depth, breadth and technical capability. In Q2, we became the first cloud
provider to bring up and validate NVIDIA's Vera Rubin NVL72, leveraging our innovations in software-
defined liquid cooling and rack management to extend our track record of being first to market. We
also set new MLPerf records for training and inference with open source models, running on the
NVIDIA Grace Blackwell platform, and in our tests, achieved the lowest cost per token for inference.
However, performance alone is not enough. Customers need enterprise-grade security and
observability, reliability, and compelling economics. According to Signal65, CoreWeave delivers total
cost of ownership estimated to be up to 47% lower than the average hyperscaler.
Customers also require our platform, which integrates these capabilities with a broader portfolio of
storage, CPU and networking services across a distributed footprint of data centers globally. In July,
Gartner named CoreWeave a visionary in its 2026 Magic Quadrant for Cloud AI infrastructure. We
believe that recognition provides additional independent validation of our approach to building the AI
cloud. These achievements are not isolated technical milestones. They translate directly into faster
deployment, higher utilization, better application performance and lower cost for customers. Pairing
product depth with best-in-class performance, quality and market-leading TCO is a winning formula
for our customers and for CoreWeave.
CoreWeave is the foundation for AI at scale. This market requires a foundation at a magnitude unlike
anything that came before. That means securing power, sites, cooling, hardware, storage, networking
and supply chain inputs well ahead of need and operating them as 1 integrated system. As I shared at
the top of the call, we ended Q2 with 1.5 gigawatts of active power, adding close to 500 megawatts in
the quarter alone. To put that in perspective, we added more power in Q2 than any single neo-cloud
operates in total today, according to third-party estimates.
Critically, our scale is working in our favor, and the math gets better from here. Each new deployment
is landing against a much larger installed base than it was even 1 quarter ago. As that base grows, each

new build becomes a smaller part of the whole, while contracted revenue from existing deployments
remains in place. This is how we are transforming scale into operating leverage. It is why margins
expanded in Q2 and why we expect them to continue expanding sequentially during Q3 and Q4. We are
also securing the ingredients required to sustain growth over a multiyear horizon. Contracted power
grew to 3.7 gigawatts in Q2, and since quarter end, we have added roughly 500 megawatts, bringing
contracted power to 4.2 gigawatts as of today. These figures exclude more than 1.5 gigawatts of further
potential power from powered land we have accumulated. Options we have to expand at existing sites,
and LOIs we have executed.
Our first several self-builds are already well underway, including our first site expected to come online
later this year. Powered land forms the foundation for deeper vertical integration, giving us greater
operational control and supporting enhanced long-term margins. We are also expanding globally and
have contracted more than 1 gigawatt of power outside the United States, including recently entering
the APAC region with 360 megawatts in Indonesia, that will begin coming online in approximately 18
months. We expect international markets to become a major driver of growth as we meet customers
where they and their end users operate. All in, we have excellent visibility to our target of at least 8
gigawatts by 2030. We expect demand to meaningfully exceed supply for years. In that environment,
access to power is only part of the equation.
Just as important is each necessary component required to deliver the AI cloud at scale. Building on
our close partnerships with NVIDIA and our OEM and ODM partners, our recent long-term agreement
with Solidigm is one illustration of how we are derisking access to the critical inputs needed to serve
our customers. Our investments in technology, capacity, vertical integration, supply chain and global
expansion, all flow from the same vision. AI is increasingly pervasive. The pioneers who move fastest
will lead, and they will require a platform capable of supporting continuous learning and deployment at
unprecedented scale.
Before I turn to Nitin, I want to reiterate that CoreWeave enters the second half of the year with more
momentum than at any point in our history. AI is reshaping every industry. The pioneers that are
building need more than compute, and that is why they come to CoreWeave for an AI cloud designed
for the full AI life cycle, serving any workload from frontier training to rapidly scaling inference.
Demand continues to exceed supply across sectors, geographies and generations of infrastructure. We
are delivering at extraordinary scale to a diverse set of customers with improving operating leverage
and visibility into the power and critical components required to sustain growth for years. The
opportunity ahead is generational. CoreWeave is the essential cloud for AI. Our conviction in our
strategy has never been stronger, and our execution continues to reinforce it. With that, I'll turn it over
to Nitin.
Nitin Agrawal (Executives)
Thanks, Mike, and good afternoon, everyone. Q2 was an exceptional quarter for CoreWeave marked by
intense customer demand, significant ramp of our active capacity and continued execution against our
product and financing road maps. Perhaps most importantly, Q2 marked the quarter in which we saw
margins inflect expanding sequentially as we had discussed over the past several quarters. Before
diving into results, I wanted to spend a few moments touching upon how demand dynamics are
evolving in the current environment as well as its implications on cash flows and the value of our
rapidly growing infrastructure footprint.

Demand for CoreWeave Cloud remains exceptionally strong across the entirety of our customer base,
with demand from multiple customers for each GPU we bring online. We are being disciplined in how
we allocate our scarce cloud capacity. We are prioritizing opportunities that are strategically important,
adding new customers while deepening long-term existing relationships and delivering attractive
returns that, as Mike noted, are expanding further.
The scale of our AI products and services beyond GPUs also continues to ramp significantly as
customers consolidate spend with us. These margin-accretive businesses including storage, CPU,
networking and software already exceed $400 million of ARR as of Q2. We expect they will continue to
expand rapidly. Simply put, customer spending on CoreWeave has gone up as customers recognize the
increased value we deliver. And this operating margin improvement came before our July pricing
changes which included an approximately 25% increase across SKUs in response to the current demand
environment and the increasing ROI our customers are observing from their investments in the
CoreWeave platform as they shift to inference.
We are also passing through component price increases. In terms of how this translates to cash flows,
as we previously discussed, a typical 5-year contract carries strong and still-expanding unit economics
across its term. But those economics do not arrive evenly. The cost, primarily in the form of CapEx is
front-loaded requiring a combination of debt, customer prepayments, and other corporate level capital
to finance its build out. Once the cluster is delivered, contracted revenue ramps becoming predictable
and highly cash flow generative. This is all considered in our underwriting of expected margins before a
contract is signed.
The deployment delivers attractive returns, fully repaying asset-level debt used to fund the CapEx while
generating significant additional free cash flow. So when an initial contract ends, the cluster no longer
has any leverage, and we are free to recontract that cloud infrastructure or offer it to the market. We
will have generated an attractive return even before the prospect of further monetizing the cloud
infrastructure. Every resale or renewal is incremental on top of the returns already earned within the
initial term. What we are seeing today is that the upside of recontracting is real as we remain largely
sold out of prior generations of NVIDIA GPUs in addition to the current SKUs. So as our earlier
generation fleets roll off their original contract, they offer the potential to deliver strong returns in the
subsequent years. We are seeing this across our Ampere and Hopper fleet.
As an example, we recently signed an A100 contract that extends into 2029 at an attractive price. As a
reminder, this SKU was introduced in 2020. Clusters of prior generations of architecture offer installed,
energized production-grade compute already running at scale. They come with a proven ROI for
customers. In a market where new capacity is supply constrained and costs are rising, AI cloud
infrastructure and production is a scarce, valuable asset. While we have built a business whose
economics do not rely on recontracting after initial customer term. Increasingly, we are seeing longer
utilization at higher prices, offering the potential for significant further upside.
With these tailwinds at our back, we are more confident than ever in the long-term ROI of our product
and capacity investments, enabled by our industry-leading AI cloud services. Now turning to Q2
results. Revenue was $2.6 billion in Q2, up 112% year-over-year and 24% sequentially, driven by
continued strong execution and customer demand for CoreWeave's AI cloud platform. Revenue backlog
ended the quarter at $104.2 billion, up 246% year-over-year. As Mike noted, this does not include the
over $25 billion of net new customer commitments we added early in Q3.

Of the existing backlog, more than 50% is attached to a contract where customer delivery has
commenced. We expect this figure to reach more than 2/3 of our Q2 backlog by the end of this year.
Operating expenses in the second quarter were $2.6 billion, including a stock-based compensation
expense of $165 million. The increase in our operating expenses was a direct result of scaling our active
power while converting backlog into revenue.
This drove the corresponding increases in our cost of revenue and technology and infrastructure spend.
In addition, the increase in sales and marketing was driven by increased investment in our go-to-
market organization as we further diversify our customer base and expand into new products and
markets. G&A increased driven by personnel cost to support our growth while continuing to moderate
versus revenue growth. Adjusted EBITDA for Q2 was $1.5 billion compared to $753 million in Q2 of
2025, doubling year-over-year. Our adjusted EBITDA margin was 59%. Adjusted operating income for
Q2 was $128 million compared to $200 million in Q2 of 2025 and up from $21 million last quarter,
well above the high end of our guidance as operating leverage comes into a business with scale.
Adjusted operating margin was 5%. Margins expanded as we scaled despite continuing to incur
significant ramp costs.
Net loss for Q2 was $626 million compared to a net loss of $290 million in Q2 of 2025. Interest
expense for Q2 was $640 million compared to $267 million in Q2 of 2025, driven by increased debt to
support the continued scaling of our infrastructure and delivery of our contracted customer
commitments. We recorded an income tax provision despite a net loss due to valuation allowance on
net deferred tax assets. As noted last quarter, absent significant discrete items or a change in
circumstances, our tax rate should remain broadly consistent over 2026. Adjusted net loss for Q2 was
$567 million compared to a net loss of $130 million in Q2 of 2025.
Turning to capital expenditures. CapEx in Q2 totaled $9.4 billion, slightly above the high end of our
guided range. Higher CapEx in the quarter reflects customer deliveries accelerating. Construction in
progress, CIP, increased to $11.9 billion from $9.6 billion quarter-over-quarter signaling the significant
amount of PP&E we expect to deploy early in Q3 based on the large amount of power we received very
late in Q2. In fact, in June, we brought on more than 300 megawatts of active power, which makes June
itself larger than any full quarter in our history. As Mike noted, the global supply chain remains
complex. We continue to navigate these challenges with operational discipline and leveraging our
partner relationships including new ones like Solidigm to strategically source required inputs.
Turning to our balance sheet and strong liquidity position. As of June 30, we had more than $6.9
billion in cash, cash equivalents, restricted cash and marketable securities. In Q2, we made significant
progress in strengthening our balance sheet and expanding the depth and breadth of our access to
capital, raising approximately $18 billion across a combination of debt, convertibles and equity. These
transactions included several firsts, like our inaugural Eurobond as well as our first ever delayed draw
term loan backed by HPC infrastructure issued in the public markets. Our most recent financing, our
second publicly syndicated term loan marked another significant milestone as the first to include
shorter duration customer contracts. The transaction, which priced during one of the most dislocated
weeks for credit this year was met with meaningful interest.
Despite the environment at the time, we chose to complete the transaction at its full size. Our spreads
have retraced since. Perhaps most importantly, the transaction demonstrated the credit market's
growing conviction in long-term value of NVIDIA infrastructure running on CoreWeave cloud. This

financing is significant as it unlocks our ability to serve critical part of the enterprise market at scale
while also allowing us to accelerate the ramp of our managed inference platform and grow our exposure
to shorter dated contracts that typically come at a higher ASP and margins. These transactions
attracted broad and deep investor participation highlighting the significant interest we continue to see
in supporting CoreWeave's journey. The combination of these transactions brings us to over $32 billion
of debt and equity capital secured to date.
Over the past year, we have reduced our weighted average cost of debt by almost 300 basis points,
representing approximately $1.1 billion of annualized interest savings based on our end of Q2 debt
load. Turning to guidance. As a result of continued strong execution, we now expect to end the year
with more than 1.85 gigawatts of active power, up from our previous guidance of more than 1.7
gigawatts. In terms of how this flows through the second half, we expect Q3 revenue to be in the range
of $3.45 billion to $3.6 billion. We expect Q3 adjusted operating income of $200 million to $260
million as margins continue to sequentially expand reaching low teens in Q4. Q3 interest expense is
expected to be in the range of $860 million to $940 million reflecting the growth in our debt balance to
finance our accelerating deployments.
We expect CapEx to be $11.5 billion to $13.5 billion based on the significant amount of new capacity, we
will be delivering to customers. Moving on to full year. Our disciplined execution and the momentum
we are seeing across our customer base gives us confidence in raising our full year 2026 revenue
guidance to $12.4 billion to $13.2 billion and adjusted operating income to $960 million to $1.15
billion. As a result of our increased expectations around capacity to be delivered to customers this year
as well as some of our significant recent wins, we now expect 2026 CapEx in the range of $35 billion to
$39 billion.
Finally, we're also raising our expected end of year annualized run rate revenue to $18.5 billion to $19.5
billion. The long-term nature and attractive margins underpinning our contracted revenue backlog
continue to provide us with clear visibility, and we are confident in the targets we have put forward. In
closing, Q2 demonstrated the strength of the demand environment for CoreWeave's full technology
stack and the discipline of our operating model. We strategically expanded our customer base to
support the next wave of enterprise AI adoption at increasingly attractive margins. Customers are
expanding their spend with CoreWeave to leverage the full depth of our AI native platform. We remain
on track for our sequential margin expansion through the balance of the year and we have made
significant additional progress on our capital structure, reducing our weighted average cost of capital
while securing the financing required to support our long-term growth plan.
We look forward to seeing many of you at our annual developer conference, Fully Connected, in
September, where you will hear from our leadership and customers alike in how our platform is
accelerating AI in production. Thank you. With that, we will open up for questions.
Operator (Operator)
[Operator Instructions] Your first question comes from the line of Samik Chatterjee with JPMorgan.
Samik Chatterjee (Analysts)
Congrats on a strong overall print here. Maybe just a couple of topics. One, you did mention the
renewal opportunity with shorter-term contracts as some of the older contracts come off expiration to
leverage sort of the pricing that we are seeing in the market. Can you just help us think through as you

engage in some of that discussion with customers, what you're finding in terms of typical customer
intent in terms of contract period? And how much of your installed base of equipment is maybe up for
renewal over the next few years, if you can get us -- give us a sense of how to think about the magnitude
of that opportunity? And I have a follow-up.
Michael Intrator (Executives)
Thank you for the question and excited to spend a little bit of time with you talking about what was a
truly outstanding quarter for the company across our infrastructure, across our software, across our
solutions, across our sales and contracts with new clients and existing clients.
Yes, one of the most exciting components of what we are beginning to understand, what we believe the
market is providing real insight into right now is that the older generations of infrastructure continue to
have significant value for use cases within many of the consumers of AI. And we've talked about this
literally for years now that the most bleeding edge solutions that are coming out of NVIDIA that we
build into our cloud and deliver to our most demanding customers. That's really important for some of
the most cutting-edge use cases.
But within that environment within that ecosystem, there are an enormous number of other use cases
that can make use of older, more later-dated SKUs. And the fact that we have been able to go ahead and
sell a GPU whose architecture was from 2020 in a contract that was fully priced out to 2029, really
provides some insight into what the future is going to look like as this infrastructure comes off contract.
Nitin Agrawal (Executives)
Yes. In terms of the capacity that's coming up for renewal, Samik, is a very limited part of our fleet. And
the ASPs on the older generation remain higher or at levels that we've seen about a year ago. The
second part of the piece that is very interesting in our business is as these fleets come off maturity, it
allows us to have a great product in terms of managed inference to serve for our customers, which, as
Mike noted, is a very fast-evolving nature of our business -- part of our business, which we expect to
continue to grow rapidly and expect to have about $250 million of ARR by the end of the year.
Samik Chatterjee (Analysts)
Got it. And so my follow-up there. But in terms of the follow-up, can you talk about the supply chain a
bit. You're obviously navigating it pretty well to bring capacity online. But in terms of the agreement
that you have now with Solidigm, for example, how are you looking at sort of the need to maybe do
something more broad-based across supply chain in terms of longer-term agreements to assure
yourselves of more supply as well so that you can continue to sort of execute on the power -- on the
capacity that you want to bring online?
Michael Intrator (Executives)
Yes, it's a great question. So look, End of the day, my job is to ensure that this company has the capacity
to deliver the product that our clients require. And in order to do that, we need to aggressively manage
a complicated supply chain. And that supply chain includes everything from land power and shell
through GPUs and networking through memory, all of which is being challenged by the growth and
expansion of artificial intelligence. In order to do that, we have built over the last several years, really
long-standing deep relationships with our ODMs, our OEMs, NVIDIA the companies that supply us

with memory, all of them. And what we've done is we've thought about what is necessary to ensure that
we have access to the infrastructure and the components and the capital that we need in order to
deliver our products at an acceptable price and quality to our clients.
And it's one of the things that's just embedded in the DNA of CoreWeave. That's what we do. It's part of
what we do every single day is nurture these relationships and ensure that we have access to everything
that we need in order to deliver the product, which is NVIDIA infrastructure delivered through our
cloud.
Nitin Agrawal (Executives)
One thing, Samik, to note here is the increase in the value of output of the CoreWeave cloud has
outpaced the value of the input increases that we are currently experiencing in the supply chain. And as
a result of it, what you're seeing is margins expand, as Mike noted, in his comments around the typical
contribution margins that we saw last quarter were 5 to 10 percentage points higher than what we've
observed in the recent quarters.
Operator (Operator)
Your next question comes from the line of Brad Zelnick with Deutsche Bank.
Brad Zelnick (Analysts)
Great. Congrats on the strong execution. My first question, I wanted to ask about your managed
inference offering, which is off to a really strong start. What are your initial learnings? And what are the
factors that inform your thinking on allocating capacity to it going forward versus your traditional take-
or-pay deals? And I have a follow-up to that as well.
Michael Intrator (Executives)
Yes. Thank you for the complement. It really was a great quarter for us. We're very excited about it.
Look, when we think about our offering, we really think about it holistically and we have made
enormous strides through the last several years to focus on building scale through these long-term take-
or-pay contracts. As we've hit hyperscale, we understand that we are going to need to broaden our
offering to provide the products that our clients need, to deliver products that have higher margins, to
provide the software solutions, to provide access to CPUs, all of the things that are necessary for our
clients to be successful. And when we think about the lessons that we've learned, as we've gone through
this unbelievable and unique scaling of our managed inference product, which went from $1 million to
$100 million inside of a single quarter, we really think about the fact that, that is an incredible
opportunity for us to offer the most bleeding edge compute that we have, but also a wonderful way for
us to access and use contract -- GPUs that are coming off contract in a way to extract maximum value
for the company over time.
So look, the market is very deep. We think that we have an embedded advantage because of our control
over the silicon, and we think that we're going to be very successful in that market over time.
Nitin Agrawal (Executives)
And Brad, 1 thing to note here is we announced yesterday around our DDTL 5.5 closing and that shows
that the capital markets are extremely interested in supportive of CoreWeave's product in terms of

underwriting shorter duration contracts, which is definitely a tailwind as we look at these markets to
support our customer needs.
Brad Zelnick (Analysts)
That actually leads to my next question. So on the 5% to 10% better margin that you're seeing on recent
deals that you're signing, can you help unpack the drivers how much is a function of shorter duration
deals, versus strong competitive differentiation or other factors? And what are you seeing more broadly
just out there in the market as it relates to pricing?
Michael Intrator (Executives)
So it's a combination of a lot of things, and it's difficult to deconstruct it. The infrastructure that we
deliver through the CoreWeave cloud is more valuable to our customers than any other solution that
they can encounter. The quality of the platform, the reliability of the infrastructure, the security, the
TCO, all of those things contribute to customers coming back to us again and again and expanding their
footprint within our cloud and infrastructure. And so there is a piece of it, which is they understand
how much more valuable a given piece of infrastructure is delivered through us. The second piece of it
is, many of our clients are monetizing their products. And so they are more aggressive about coming in
and willing to pay us higher margins because they need access to the compute that will allow them to be
successful.
This is a phenomenon that's occurring across the infrastructure space but it's particularly occurring
within our ecosystem. And it's very exciting to see as the premium product that we deliver is priced in a
premium fashion by the consumers of this compute.
Operator (Operator)
Your next question comes from the line of Amit Daryani (sic) [ Amit Daryanani ] with Evercore ISI.
Jyhhaw Liu (Analysts)
This is Irvin Liu on for Amit. I had 1 and a follow-up. So my first question is, it sounds like there's
upward pressure to pricing across multiple vectors, including the higher value you provide to your
customers, the pass-through of higher component costs and the recontracting opportunity coming up.
So with that in mind, should we still think of kind of the $18 billion to $19 billion in ARR as kind of the
exit target for 2027?
Nitin Agrawal (Executives)
Yes. So we increased the exit ARR number that we provided in guidance to you folks right now at $18.5
billion to $19.5 billion for 2026, so that is baked in our guidance that we provided to you.
Jyhhaw Liu (Analysts)
Okay. Got it. Got it. And then for my follow-up, I think the regulatory backdrop for data centers appears
to be increasingly difficult. There have been reports of local opposition to data centers. With this in
mind, can you talk about your confidence level in deploying more than 3 gigawatts of active power by
the end of next year and kind of your road map to 8 gigawatts by the end of the decade?
Michael Intrator (Executives)

Sure. And your question is very timely and very important for the entire AI space in the entire data
center space. I guess I'll start with -- we believe that the certain communities have moved forward with
moratoriums. And we feel like moratoriums are -- they're not going to impact the demand for this
infrastructure, they are going to impact where this infrastructure gets built. And so our approach to
how you engage with the stakeholders is that you have to be extremely collaborative with the
communities that ultimately host the infrastructure. And that's based on transparency. You have to
work with the local governments. You've got to work with the utilities, you've got to work with the
policymakers in order to allow yourself to ensure that what you're building fits into the communities
that you're entering.
Ultimately, at the end of the day, it is in our interest, and it is in their interest for us to be good
neighbors of their community. A lot of that comes down to making sure that you're paying for grid
upgrades so that it doesn't fall or impact the rate base. You create an enormous number of construction
jobs. You are -- there are long-term jobs that are left that survive within the data centers, the data
centers that are being built contributed to the tax base. All of these things are incredibly important to
how you enter into a community and how you engage that community as you're building this
infrastructure that is so necessary in order to be able to provide America's AI leadership. And so when
we talk through the numbers with you guys, we -- basing our progress on where we are today and what
we have guided here, none of those numbers will be impacted by the regulatory pushback as of today.
We are comfortable with it. We continue to expand. We continue to engage our data centers are best-in-
class, and we expect to be held to that as we continue to build our infrastructure across the globe.
Nitin Agrawal (Executives)
And Irvin, just to give you some numbers in perspective here, if you look at our gigawatts contracted
today, they're already at 4.2 gigawatts contracted. In addition, we have about 1.5 of powered land
options to execute LOIs that we have executed. That puts you close to about 6 gigawatts already in
terms of how we think about power and it's middle of 2026. So we remain well on track to execute
against our stated goal of greater than 8 gigawatts of active power by end of 2030.
Operator (Operator)
Your next question comes from the line of Raimo Lenschow with Barclays.
Raimo Lenschow (Analysts)
Congrats from me as well. I just -- I wanted to talk a little bit about the growing importance of inference
for you guys. How does your fleet need to evolve? Because inference needs to do a lot more CPU, a lot
more storage, can you do that in the existing data centers? Do they need to evolve? Can you speak to
that as well to make sure we have the capacity there going forward?
Michael Intrator (Executives)
Yes. It's a great question. It's a question we've been talking about now for several quarters. We believe
that when you're building infrastructure, you don't build infrastructure for training, and you don't build
infrastructure for inference. You build AI infrastructure. And when you build AI infrastructure, you
need to ensure that you have all of the components to be able to serve the full AI loop, everything from
training through inference as it cycles back and forth as it moves through the iterations that are

required in order to serve your clients and those companies that are consuming this. And so really, the
infrastructure that we built will move seamlessly into the ability to serve inference over time.
Raimo Lenschow (Analysts)
Okay. Perfect. And then 1 follow-up is like, obviously, with the news from Meta yesterday, a lot of
questions that we face today was around doing AI in the edge, et cetera, and then all these concerns
came up again. Like can you talk about like how you see the market evolving between edge, smaller
clouds, neocloud and hyperscalers.
Michael Intrator (Executives)
Yes. One of the things about CoreWeave that should never be underestimated is we sit at the epicenter
of an incredible amount of information flow from across the entire industry, right? The hyperscalers
use us, the labs use us. You've seen enterprise begin to scale within our platform. The information flow
that's coming back and feeding us the clues to how the world is going to look in the future has been
incredibly powerful for us in terms of how we position ourselves and our compute to serve our clients.
Look, at the end of the day, we believe that there are workloads that are going to be served from the
edge and there are workloads that do not require the same level of latency protection. And we have built
our cloud to be able to serve both of those constituents effectively. And we will continue to build in that
fashion. We will be informed by our clients continuously whether they need a little bit more of edge,
they need a little bit more of scale that is not as latency sensitive. All of those things are being fed to us
on a continual basis.
And so yes, we do see workloads on the edge. And yes, we do see workloads that don't require to be on
the edge, and we are very, very comfortable that the scale of our infrastructure and the ability to move it
back and forth is going to provide a competitive advantage for CoreWeave over time.
Nitin Agrawal (Executives)
Raimo, to your point in terms of increased competition. Even with this increased competition, we are
seeing demand, pricing and margin all expanding which is a signal for the growth in the CoreWeave
kind of product as well as our growth overall in an already massive TAM that exists.
Operator (Operator)
Your next question comes from the line of Michael Turrin with Wells Fargo Securities.
Michael Turrin (Analysts)
I realize there's likely some rounding here, but you added an impressive 500 megawatts of active power
in the quarter. The revenue, if we're looking at the sequential adds is fairly consistent with last quarter.
We can hear all the commentary around the uplift that's coming. So maybe help us think through the
linearity of capacity added. And when that 300 megawatts added in June started to hit more of a steady
state in terms of model contribution and also would be useful as a second part to hear any early market
signals you're gathering on Vera Rubin monetization and what the uplift there could look like versus
prior generations?
Nitin Agrawal (Executives)

Yes. So as you mentioned, right, you saw Q3, we added about -- sorry, Q2, we added about 500
megawatts of power. 300 of that alone was in the month of June, which is higher than any amount of
power that we've added in any history of prior quarter for CoreWeave. So definitely, that power was
back-end loaded in terms of Q2, which you would start seeing kind of come through in Q3 and Q4 in
our business. And then in terms of...
Michael Intrator (Executives)
Yes. So let me -- maybe I'll take a moment to speak to Vera Rubin. Vera Rubin is a generation that is
seeing the margin expansion right from the start. And so it's really exciting for us. The demand for the
Vera Rubin platform is enormous and the pricing power that CoreWeave has been able to garner with
its CoreWeave cloud, delivering that infrastructure really bodes well. And when we were talking about
that 5% to 10% margin step function that we're seeing, a lot of that is coming in, in the Vera Rubin SKU.
We're excited about where that's going to lead. We think that it's going to be a very, very successful SKU
for CoreWeave and CoreWeave's clients.
Operator (Operator)
Your next question comes from the line of Brett Knoblauch with Cantor Fitzgerald.
Brett Knoblauch (Analysts)
Congrats on the very strong quarter. Mike, I guess, just kind of based on the prepared remarks, it looks
like the price environment has never really been better for older generation and obviously, newer
generation GPUs here. As you look at the GPU fleet that's maybe rolling off contract, can you talk about
the cadence of how you guys look to either recontract that or kind of put it on spot or in your inference
products? And how far in advance of the roll off of those contracts, would you look to kind of make that
decision?
Michael Intrator (Executives)
Yes. So look, it's a good question. It's one we're working through. Keep in mind that the environment
for inference is incredibly dynamic, and it is scaling so fast, as we kind of struggle to keep up with the
build-out of new infrastructure, the flexibility that we are giving because we have infrastructure coming
off-line allows us to continue to scale the inference product as we're continuing to explore exactly how
big, how extensive is the managed inference opportunity for us. Some of the infrastructure that comes
off-line, we go ahead and we place back into a term contract. If we think the economics warrant putting
it in.
And the economics include both the term that we're able to garner as we think about the long-term
stability of the company and the long-term obligations that we need to support as we continue to build
and scale the company. But we also do recognize that in the short term, there is an opportunity to sell
on shorter-term contracts and extract additional margin on this infrastructure as the world tries to
catch up with what is a systemic disequilibrium that has really existed for several years now and will
continue to exist for the foreseeable future.
Brett Knoblauch (Analysts)
I think that kind of leads to my next question. I guess, off the back of DDTL 5.5 where you were able to
kind of get funding for shorter duration contracts combined with kind of this data center NIMBYism

political atmosphere that's kind of taking off. It feels like you guys should be quite well positioned given
you are the most scaled to realize the most price benefits. How does the success of the DDTL 5.5 change
the way you view on kind of target durations on a go-forward basis? Does -- is that an avenue you want
to use more to maybe extract more margin in shorter duration contracts, given you know the useful life
is there?
Michael Intrator (Executives)
Yes. I mean, you're exactly right. The execution of the DDTL 5 puts CoreWeave in a position where we
get to populate the curve in terms of what we think is the most profitable configurations for term
leasing. And so we want to sell our compute on long-term contracts. We also want to sell it on shorter-
term contracts to extract additional margin. And we have been really, really aggressive about doing
that. We were the first ones to bring the 5.5 to market in order to be able to really plug into those.
There's one more really important part of the short-term contracts that I think it's important for
everyone to understand. When you're thinking about enterprise, enterprise tends to want to enter into
contracts that are not 5 years in length. They tend to think in shorter cycles than that. And so by
enabling the financing market to support the contracts in 5.5, we're able to go ahead and diversify our
terms so that we're able to support additional contracts. It opens up whole new markets for us.
These clients want to buy compute for 2 years or 3 years, and that's not a market that was easily
accessible to us until we were able to bring DDTL 5.5 to market. And now that market will accelerate
meaningfully as we're able to offer compute to our customers on a time frame that they are able to
consume it, buy it and entering the contracts to purchase it from us.
Operator (Operator)
This concludes our question-and-answer session. I will now turn the call back to Mike Intrator for
closing remarks.
Michael Intrator (Executives)
Before we sign off, I want to thank our team customers and partners for their trust, hard work and
commitment to CoreWeave. None of these achievements would have been possible without you. I'm
incredibly proud of what we have accomplished together and for what comes next as we build the
essential cloud for AI. Thank you all for joining today. We appreciate your support, and we look
forward to updating you on our progress in the quarters to come.
Operator (Operator)
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CRWV_Q1_2026_Earnings_Call_20260507.md
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：重申全年營收 $12–13B（原話："reaffirming our full year guidance of $12"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：重申全年調整後營業利益 $0.9–1.1B（原話："$900 million to $1.1 billion of adjusted operating income"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：Q2 營收指引 $2.45–2.6B（原話："revenue in the range of $2.45 billion to $2.6 billion"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：Q2 調整後營業利益 $30–90M，利潤率自 Q1 低點回升（原話："of $30 million to $90 million as margins start to expand"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：Q2 利息費用指引 $650–730M（原話："in the range of $650 million to $730 million"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：全年 CapEx 指引 $31–35B（原話："we now expect CapEx of $31 billion to $35 billion"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：CapEx 下緣上調歸因於零組件價格上漲（原話："increases in component pricing"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：2026 年底年化營收 run-rate 預期 $18–19B，下緣上調 $1B（原話："$18 billion to $19 billion of annualized run rate revenue"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：2027 年底 run-rate 逾 $30B，其中逾 75% 已簽約（不含未行使續約）（原話："more than 75% of which is already contracted,"）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：管理層稱利潤率壓力屬時間性而非經濟性（原話："This margin dynamic is timing based, not economic."）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：新部署成熟後貢獻利潤率約落在 20% 中段（原話："contribution margins normalizing in the mid-20s"）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：Q4 調整後營業利益率回到低雙位數（原話："returning to low double digits by Q4."）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：Q1 調整後營業利益率 1%，管理層稱為低點（原話："Our Q1 adjusted operating margin was 1%"）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：Q1 調整後 EBITDA 利益率 56%（原話："Our adjusted EBITDA margin was 56%."）
- 2026-05-07｜Michael Intrator (CEO)｜margin：毛利率受相對於既有裝機量的新增規模影響，管理層稱已近逃逸速度（原話："when I say that they're achieving escape velocity"）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：收入於交付客戶後按合約期直線認列（原話："we start recognizing revenue on a straight-line basis"）
- 2026-05-07｜Michael Intrator (CEO)｜margin：零組件與電力成本於簽約時以轉嫁方式處理（原話："it is effectively passed through"）
- 2026-05-07｜Michael Intrator (CEO)｜margin：管理層稱大致不受部分零組件通膨影響（原話："we are insulated from the price inflation on some of the"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：積壓訂單 $99.4B（原話："Revenue backlog for the quarter ended at $99.4 billion"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：積壓訂單認列時程：24 個月內 36%（原話："expected to be recognized in the next 24 months"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：非投資等級 AI 原生與基礎模型實驗室占積壓訂單比重（原話："foundation labs now represents less than 30% of our"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：新增容量加權平均合約年限約 5 年（原話："new capacity remaining at approximately 5 years"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：Q1 新增 Anthropic 為客戶（原話："we added Anthropic as a"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：Meta 簽訂多筆新單，含 $21B 協議（原話："the $21 billion agreement announced in early April"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：金融服務垂直領域積壓訂單近 $100 億（原話："approaching $10 billion in our revenue backlog"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：10 家客戶承諾至少 $1B 支出（原話："10 customers committed to spending at"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：A100/H100/H200/L40s 平均價格季增（原話："all increased quarter-over-quarter"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：2026 年容量大致售罄（原話："we remain largely sold out of our 2026 capacity"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：管理層估算推論占算力已大幅逾 50%（原話："materially in excess of 50% of our compute is"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：H100 售罄（原話："We are sold out in our H100s."）
- 2026-05-07｜Michael Intrator (CEO)｜customer：管理層以「配置」描述客戶分配（原話："I think the word allocate is probably accurate."）
- 2026-05-07｜Michael Intrator (CEO)｜product：推出 Flex Reservation 與 Spot 定價（原話："Both offerings were immediately oversubscribed."）
- 2026-05-07｜Michael Intrator (CEO)｜product：開始提供 CoreWeave Omni（客戶自有資料中心部署）（原話："we are beginning to offer CoreWeave Omni"）
- 2026-05-07｜Michael Intrator (CEO)｜product：軟體、CPU、網路業務年底各預期逾 $100M ARR（原話："$100 million of ARR by the end of the year."）
- 2026-05-07｜Michael Intrator (CEO)｜product：NVIDIA 將 CoreWeave 軟體方案列為參考架構（原話："software solution as a reference architecture for them"）
- 2026-05-07｜Michael Intrator (CEO)｜commitment：2026 年底活躍電力目標逾 1.7GW（原話："our target of more than 1.7 gigawatts by the end of 2026"）
- 2026-05-07｜Michael Intrator (CEO)｜commitment：2030 年活躍電力目標逾 8GW（原話："reaching more than 8 gigawatts of active power by 2030"）
- 2026-05-07｜Michael Intrator (CEO)｜commitment：首個自建站點預計今年稍晚上線（原話："We expect our first self-build site to come"）
- 2026-05-07｜Nitin Agrawal (CFO)｜commitment：承諾下半年調整後營業利益成長快於營收（原話："accelerate faster than revenue growth"）
- 2026-05-07｜Michael Intrator (CEO)｜commitment：2026 大部分零組件已鎖定（原話："The overwhelming majority of it is locked in already"）
- 2026-05-07｜Michael Intrator (CEO)｜capital_allocation：DDTL 4.0 為首個 HPC 基礎設施投資等級貸款（原話："first ever investment-grade Delayed Draw Term Loan"）
- 2026-05-07｜Michael Intrator (CEO)｜capital_allocation：DDTL 4.0 隱含成本低於 6%（原話："implying a cost of less than 6%"）
- 2026-05-07｜Michael Intrator (CEO)｜capital_allocation：加權平均債務成本 2023–2025 年降約 600 bp（原話："weighted average cost of debt by approximately 600 basis"）
- 2026-05-07｜Nitin Agrawal (CFO)｜capital_allocation：2029 年前無債務到期（自償合約債與 OEM 融資除外）（原話："no debt maturities until 2029"）
- 2026-05-07｜Nitin Agrawal (CFO)｜capital_allocation：Q1 因 NVIDIA 關係擴大募集 $20 億股權（原話："we raised $2 billion of equity"）
- 2026-05-07｜Nitin Agrawal (CFO)｜capital_allocation：Jane Street 策略投資 $10 億（原話："$1 billion strategic investment we received from Jane Street"）
- 2026-05-07｜Nitin Agrawal (CFO)｜capital_allocation：定價第五筆 DDTL，涵蓋 OpenAI 與 Cohere 合約（原話："we priced our fifth DDTL Facility"）
- 2026-05-07｜Michael Intrator (CEO)｜capital_allocation：新增電力全數以長期租賃取得，並加速自建（原話："We added more than 400 megawatts of contracted power in Q1"）
- 2026-05-07｜Michael Intrator (CEO)｜competition：管理層描述在高度競爭市場中的多面向擴張策略（原話："positions CoreWeave to grow in a highly competitive"）
- 2026-05-07｜Michael Intrator (CEO)｜competition：新增 5GW 與 NVIDIA 關係：管理層稱可獨立取得電力（原話："independent of any support from NVIDIA or anyone else"）
- 2026-05-07｜Michael Intrator (CEO)｜risk：管理層承認近 6–9 個月零組件嚴重短缺（原話："an acute shortage of certain components"）
- 2026-05-07｜Michael Intrator (CEO)｜risk：管理層稱限制因素不只電力，還有勞力、記憶體、儲存（原話："limiting factor isn't just power, it's labor, it's memory"）
- 2026-05-07｜Michael Intrator (CEO)｜risk：單一資料中心供應商不超過活躍基礎設施 17%（原話："no single data center provider that delivers more than 17%"）

### CRWV_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md
- 2026-09-08｜CEO｜competition：說明自家雲端從創立起專為 AI 打造，而非改裝舊環境（原話："it's like the minivan versus the F1, right?"）
- 2026-09-08｜CEO｜guidance：管理層重申對算力供需的看法：需求持續壓過供給（原話："wildly overwhelmed by the delivery and demand"）
- 2026-09-08｜CEO｜customer：大型客戶對資源的需求量持續擴大（原話："consumers are demanding ever larger amounts of resources"）
- 2026-09-08｜CEO｜customer：舉 Caterpillar 為企業客戶新進場的例子（原話："a company like Caterpillar comes and starts to use us"）
- 2026-09-08｜CEO｜risk：指出社區對資料中心的反對在增加（原話："increased resistance to data centers going into communities"）
- 2026-09-08｜CEO｜risk：預期選舉前資料中心議題聲量最大（原話："it's going to be a maximum volume"）
- 2026-09-08｜CEO｜capital_allocation：美國以外已簽約電力超過 1 GW，作為分散資料中心組合（原話："over 1 gigawatt of power contracted outside of the U.S."）
- 2026-09-08｜CEO｜margin：說明向下整合資料中心的兩個理由之一是回收毛利，並稱其為較次要者（原話："you can recapture some margin, right?"）
- 2026-09-08｜CEO｜commitment：表示自建資料中心已開始啟動前 2-3 座（原話："starting to see the first 2 or 3 of our self-builds spin up"）
- 2026-09-08｜CEO｜competition：談產業結構：資本密集產業會有擴張與整併期（原話："they will tend towards periods of consolidation"）
- 2026-09-08｜CEO｜risk：回應供需正常化後超大規模客戶是否收回外包（原話："We do not believe that they are going to pull back, right?"）
- 2026-09-08｜CEO｜customer：談合約屆期後客戶去留（原話："some of those contracts may come back to us"）
- 2026-09-08｜CEO｜margin：談規模帶來的經濟效益與毛利（原話："ways of driving economics and driving margin"）
- 2026-09-08｜CEO｜product：產品附加率：75% 客戶使用三項服務（原話："75% of our clients are using 3 different services"）
- 2026-09-08｜CEO｜product：NVIDIA 將其軟體堆疊指定為參考架構（原話："NVIDIA designated our software stack as a reference"）
- 2026-09-08｜CEO｜product：Omni 軟體層可在他人資產負債表上取得槓桿（原話："allows us to get some leverage on other balance sheets"）
- 2026-09-08｜CEO｜capital_allocation：最大融資引擎在 SPV 層級（原話："largest engine of our borrowing is occurring at an SPV"）
- 2026-09-08｜CEO｜capital_allocation：最近一次債務結構由貸方承擔續約風險（原話："now the lenders are taking renewal risk"）
- 2026-09-08｜CEO｜capital_allocation：曾以 A- 信用等級取得借款（原話："we were able to borrow at A- credit"）
- 2026-09-08｜CEO｜commitment：表示產品範圍聚焦 AI 工作流，不跨出此範圍（原話："And then we don't wander too far from it, right?"）
- 2026-09-08｜CEO｜customer：對開源與閉源模型採中立態度（原話："more demand for compute is better for our business"）

### 問答異常語氣（迴避／改口／保留）
- CRWV_Q1_2026_Earnings_Call_20260507.md｜問：Mark Murphy：Q1 營收超預期，為何不把上調帶入全年營收指引｜答法：未直接解釋，改談 2026 年容量售罄、年底 ARR 下緣上調與 2027 ARR 已簽約比例
- CRWV_Q1_2026_Earnings_Call_20260507.md｜問：Brent Thill：上半年與下半年營業利益差距大，下半年獲利憑什麼成立｜答法：重申軌跡與指引符合先前說法、Q1 為低點，未提供上下半年逐項拆解數字
- CRWV_Q1_2026_Earnings_Call_20260507.md｜問：Nehal Chokshi：每季可新增多少電力｜答法：明言無法給出每季兆瓦數，改述管線龐大與過去 12 個月合計 2GW
- CRWV_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md｜問：供需正常化後，超大規模客戶收回外包的看空論點，長期如何看待｜答法：CEO 先自稱前一題答案是最政治正確的答案，未提供正常化後的數字，改談客戶續約、事業規模與自有產品需求；稱部分合約可能回來、部分不會

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
{"date":"20260523","verdict":"B 衛星候選：Q1'26 Rev $2.08B +112%/adj EBITDA margin 56%/Backlog $99.4B (+49% QoQ) 但 Q2 指引偏低觸發 -10%；Microsoft 67% 客戶集中度極端 + Debt $25-29B D/E 4.5x；EV/Rev FY27 4.3x 同 tier 略折價；MA 🟠 中段消化（從 peak $187 -42%）；等 $90-95 分批進。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"CRWV 兌現 FY26 Revenue $12-13B + FY27 $19-20B 共識路徑，並在 FY28 首次達 GAAP 盈利","columns":{"2Y 驗證點":"FY26 Revenue $12.5B mid 兌現","5Y 驗證點":"FY28 GAAP EPS +$2.14 共識兌現","10Y 驗證點":"FY30 Revenue ≥ $45B + GAAP margin > 5%","數字門檻":"FY26 Revenue ≥ $12B 否則 thesis 削弱","來源":"CRWV Q1'26 法說 5/7 + guidance","漂移觸發":"連 2 季 Revenue YoY"}},{"id":"H2","text":"Microsoft 集中度從 67% 逐步降至","columns":{"2Y 驗證點":"FY26 EOY Microsoft 占比","5Y 驗證點":"FY28 Microsoft 占比","10Y 驗證點":"FY30 Microsoft 占比","數字門檻":"2027 全年 Microsoft ≥ 65% → 反轉","來源":"backlog 結構 + 10 個 $1B+ 客戶 ramp","漂移觸發":"連 2 季 Microsoft 比例上升 → 削弱"}},{"id":"H3","text":"Debt $25-29B 對應的 Debt/EBITDA 從 ~3-4x 改善至","columns":{"2Y 驗證點":"FY27 H1 Debt/EBITDA","5Y 驗證點":"FY28 Debt/EBITDA","10Y 驗證點":"FY30 Debt/EBITDA","數字門檻":"FY28 仍 > 3.5x → 反轉","來源":"Bank covenant + Q1'26 balance sheet","漂移觸發":"新 debt 大規模 issue → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Microsoft Maia v2/v3 量產 + Azure AI workload 50%+ 遷移至 in-house","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Microsoft 季法說 Maia deployment 進度","警戒閾值":"Microsoft Q3-Q4 2026 公開 Maia v2 mass deployment → 警戒；公開 50%+ 遷移計劃 → 反轉"}},{"id":"R2","text":"Debt $25-29B 在利率上行或 customer payment delay 引發流動性 / covenant 危機","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"季度 Debt / EBITDA 比率 + Q1'26 OCF $2.98B 持續性","警戒閾值":"FY27 H1 Debt/EBITDA > 4x → 反轉"}},{"id":"R3","text":"OpenAI 自建 ASIC（與 Broadcom 合作）2027-28 量產，$22.4B 合約縮減","columns":{"對應假設":"H1, H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"OpenAI compute supply 公開動態 + Broadcom ASIC 進度","警戒閾值":"OpenAI 公告任何 CRWV 合約縮減 → 即刻削弱"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":107.58,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
