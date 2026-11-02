你是 stock-analyst **v20 判斷 agent**，標的 GLXY（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GLXY","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenues_gaap","label":"Revenues（GAAP）","value":8057.272,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi1_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（non-GAAP，公司未提供 non-GAAP 營業利益）","value":454.749,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi2_adjusted_gross_profit_no","label":"Adjusted gross profit（non-GAAP）","value":569.282,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi3_gaap","label":"GAAP 營業利益（推算＝營運收入含損益 − 總營業費用）","value":408.761,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi4_gaap","label":"淨利（GAAP）","value":322.772,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi6_data_centers_adjusted_gr","label":"Data Centers adjusted gross profit","value":79,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi7_data_centers_critical_it","label":"Data Centers 已交付 critical IT load","value":133,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"MW","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi8","label":"現金、穩定幣與美國公債","value":4.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi9_loan_book","label":"平均放款餘額（loan book）","value":1.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi10_aum_assets_under_stake","label":"AUM＋assets under stake 合計","value":10.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD B","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_kpi11","label":"管理層指引","value":"無數字指引","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"定性","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-27","period":"2026-10-27","unit":"date","basis":"距今 5 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-27"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_glxy_gross_margin_pct","label":"GLXY 毛利率","value":-0.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLXY.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_glxy_operating_margin_pct","label":"GLXY 營業利益率","value":-0.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLXY.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_glxy_fcf_margin_pct","label":"GLXY FCF 利潤率","value":-7.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLXY.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_coin_gross_margin_pct","label":"COIN 毛利率","value":71.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_operating_margin_pct","label":"COIN 營業利益率","value":5.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_coin_fcf_margin_pct","label":"COIN FCF 利潤率","value":68.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_gross_margin_pct","label":"HOOD 毛利率","value":81.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_operating_margin_pct","label":"HOOD 營業利益率","value":45.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_hood_fcf_margin_pct","label":"HOOD FCF 利潤率","value":58.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_iren_gross_margin_pct","label":"IREN 毛利率","value":62.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IREN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_iren_operating_margin_pct","label":"IREN 營業利益率","value":-53.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IREN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_iren_fcf_margin_pct","label":"IREN FCF 利潤率","value":-332.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IREN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_sbc_equity_based_comp_an","label":"SBC（Equity-based comp and related expense）","value":16.064,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-27）","citation":"公司新聞稿（8-K 附件，Galaxy Announces Third Quarter 2026 Financial Results）https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm"},"note":"未取得"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":15.14,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-48.13,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":36.75,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-0.07 → -0.07）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-10.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（-0.1 → -0.11）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.94 → 0.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-0.07,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":-0.11,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":0.94,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-86.27,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS -0.51 → -0.07（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.24,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.36,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":4816.27,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 9302.51、現金 4486.24（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":589.3,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":13732.34,"period":"2026-11-03","unit":"USD m","basis":"市值 8916.07 ＋ 淨負債 4816.27","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":51771.63,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":58914.13,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.27,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 14.81 / W52 24.09 / W104 None / W250 None / W250 13週斜率 None%"},{"id":"f_ma_w52","label":"52 週均線","value":24.09,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K列示的競爭者：傳統金融機構、金融科技、資管、加密原生平台，以及傳統資料中心業者轉做HPC、現有AI/HPC業者、雲端業者、前加密礦工轉型AI；資管業進入門檻低、可能費率壓縮","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"The asset management industry is highly competitive and has relatively low barriers to entry. As digital assets become more mainstream, additional competitors, potentially in large numbers, have and may begin providing asset management services with respect to digital assets.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K指出資料中心業務競爭對手包含傳統資料中心業者、雲端業者與轉型AI的前加密礦工，競爭焦點為電力、連網、冷卻與地點","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"This includes traditional data center operators expanding into HPC, cloud infrastructure providers scaling capacity, and former crypto mining operators pivoting to meet the needs of AI workloads.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"CoreWeave行使Helios第二期260MW關鍵IT容量選擇權（既有租戶擴約）","source":"DCD: CoreWeave leases another 260MW capacity from Galaxy in Texas","url":"https://www.datacenterdynamics.com/en/news/coreweave-leases-another-260mw-capacity-from-galaxy-in-texas","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Galaxy Q1 2026虧損$216M，管理層稱交易量QoQ持平而產業交易量大幅下滑","source":"Yahoo Finance: Galaxy posts $216 million Q1 loss","url":"https://finance.yahoo.com/markets/crypto/articles/galaxy-posts-216-million-q1-154200246.html","excerpt":"Galaxy said its digital asset trading volumes stayed flat quarter over quarter even as broader industry trading activity fell sharply.","as_of":"2026-04-28","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Galaxy 投資人簡報稱美國至 2030 年預估有 80+ GW 供給缺口；Helios 核准容量逾 1.6 GW，其中約 800 MW 已租、1,630 MW 已核准、830 MW 未簽約（均為公司自述，無獨立分析）","source":"Galaxy Digital 8-K Q1 2026 overview exhibit 99.2 / 10-Q (period 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000047/exhibit992-q12026overvie.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Helios Phase I 首個資料廳 2026 年 4 月交付、CoreWeave 租約 133 MW；260 MW Phase II 預計 2027 上半年開始交付；其餘容量仍在與潛在租戶洽談（租戶集中風險）","source":"Galaxy Digital 10-Q (2026-06-30) / theenergymag Q1 2026 results","url":"https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000091/glxy-20260630.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"加密資本市場端：Galaxy Research 預期 2026 年 DEX 占現貨交易逾 25%、穩定幣資金流量超越 ACH；Galaxy 稱 2026 太波動無法預測，維持 2027 年底 BTC $250K 目標（價格預測非量能預測）。未找到 2027 量能共識","source":"AOL Finance: Galaxy Digital: 2026 Too Volatile to Call, but $250K Bitcoin by 2027 Remains Plausible","url":"https://www.aol.com/finance/galaxy-digital-2026-too-volatile-165611705.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2025 10-K 法律程序：LUNA 事件與紐約州檢察長和解，未列反壟斷調查；應計法律準備 $151M（2025 年底），未折現和解額 $200M，2025–2028 分期支付。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"LUNA matters: On March 27, 2025, Galaxy reached an agreement with the New York State Attorney General to resolve civil claims related to certain investments, trading, and public statements made in connection with the LUNA digital asset from late 2020 to 2022.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素提及 AI 產業（含 AI/HPC 資料中心）受監管機構對市場集中與反競爭行為的關注，屬一般性風險揭露，非針對 Galaxy 的調查。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"AI and related industries are under increasing scrutiny from regulators due to their concerns about market concentration, anti-competitive practices, and the pace of partnerships and acquisitions involving generative AI startups.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未見針對 Galaxy 的反壟斷（DOJ/FTC/EU）調查或拆分風險。","source":"WebSearch 結果（SEC 10-K/10-Q 清單）","url":null,"excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：政府可能對產品課關稅，可能影響公司自供應商取得 AI/HPC 資料中心設備（Helios 建置供應鏈風險含關稅）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"Governments have limited or may limit the shipment of products in and out of their jurisdictions or impose tariffs on products, which could negatively impact our ability to receive AI/HPC data center equipment from our suppliers.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 業務章節：公司須遵守美國及他國經濟制裁（OFAC SDN 含加密地址），為制裁合規而非出口管制/實體清單曝險。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"We must comply with economic and trade sanctions administered by the United States and other foreign governments in jurisdictions in which we operate.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Helios 首期 133MW 關鍵 IT 負載由 CoreWeave 以 15 年租約承租，ERCOT 核准逾 1.6GW，單一承租人集中","source":"Galaxy Digital 10-Q (2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000091/glxy-20260630.htm","excerpt":"the first 133 megawatts (“MW”) of critical IT load, utilizing approximately 200 MW of gross power capacity, for CoreWeave, Inc. (“CoreWeave”) under a 15-year lease agreement (the “Lease Agreement”) entered into in April 2025. In total, the Electric Reliability Council of Texas (“ERCOT”) has approved over 1.6 gigawatts (“GW”) of gross power capacity at our Helios campus.","as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"GLXY 股價因 CoreWeave 債務疑慮兩週跌約 30%，StoneX 維持買進","source":"The Block: Galaxy's AI data center business is undervalued amid CoreWeave debt concerns, StoneX says","url":"https://theblock.co/news/markets/2026-10-19-galaxy-digital-glxy-stonex-buy-coreweave-helios-ai-data-center-421045","excerpt":null,"as_of":"2026-10-19","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026：Data Centers 調整後毛利 $79M（Q2 為 $20M），分部調整後 EBITDA $69M（Q2 $11M），反映 Helios I Phase I 對 CoreWeave 租約首個完整季；Digital Assets 調整後毛利 $71M，季增 9%。","source":"Galaxy Q3 2026 earnings release (SEC 8-K) / 搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000108/glxy-20260930xpressrelease.htm","excerpt":null,"as_of":"2026-10-27","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q2 2026 Global Markets 調整後毛利 $49M（Q1 $31M），交易量季減 7%；交易對手數 1,741（Q1 1,691）。2025 全年 Global Markets 調整後毛利 $423M，年增 88%。","source":"Galaxy Q2 2026 results / GuruFocus earnings call highlights","url":"https://www.gurufocus.com/news/9007532/galaxy-digital-inc-glxy-q2-2026-earnings-call-highlights-data-center-expansion-drives-growth-amid-crypto-volatility","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素自述：AI/HPC 資料中心需求、市場規模與競爭產品進入都難預測，且無法保證能跟上變動中的 AI 格局、及時發展出滿足客戶需求的服務或基礎設施。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"Therefore, it is difficult to predict the demand for AI/HPC data center capacity, the size and growth rate for this market, the entry of competitive products, or the success of any existing or future products that may compete with any AI/HPC data centers we may develop. In addition, we cannot assure you that we will be able to keep up with the changing AI landscape or in developing services or infrastructure that can meet our customers’ evolving needs in a timely manner, if at all.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素自述：AI/HPC 資料中心設備會需要維修或因過時而更換，替換品與零件取得可能受阻。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"As our AI/HPC data center equipment requires repair or becomes obsolete and requires replacement, our ability to obtain adequate replacements or repair parts from the third-party manufacturers may therefore be hampered.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"EY 引述調查：61% 投資人預期代幣化將對交易有重大影響（產業預測，非針對 Galaxy）。","source":"EY volatility drives discipline not retreat","url":"https://www.ey.com/content/dam/ey-unified-site/ey-com/en-us/campaigns/financial-services/documents/ey-volatility-drives-discipline-not-retreat.pdf","excerpt":"in addition, 61% of respondents expect tokenization to have a significant impact on market structure↗ are demanding compliance • Institutions and security from custodians ↗","as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FY2025 10-K：Galaxy 的 Digital Assets 分部自2025年Q2起承接數位資產財庫公司委託質押，區塊鏈獎勵分配年增37%至1.789億美元；Galaxy 保留淨比例約5%–10%（質押/平台化收入來源擴大）。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"Blockchain reward distributions were $178.9 million, an increase of $48.6 million, or 37%, for the year ended December 31, 2025, compared to $130.3 million for the year ended December 31, 2024.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：Galaxy 設有三家FINRA經紀商，其中FIN2提供零售經紀服務（introducing broker，由第三方清算券商清算），屬零售通路佈局。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"FIN2 is authorized to provide retail brokerage services as an introducing broker, with customer accounts cleared and carried by a third-party clearing broker.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026 財報電話會議：管理層稱新交易擴大「distribution surface area」，並推出GOFR、Galaxy Curator等新產品。","source":"GuruFocus Galaxy Digital Q2 2026 Earnings Call Highlights","url":"https://www.gurufocus.com/news/9007532/galaxy-digital-inc-glxy-q2-2026-earnings-call-highlights-data-center-expansion-drives-growth-amid-crypto-volatility","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q1 2026 10-Q：資產管理與基礎設施收入來自管理費、質押費與自託管技術授權費；Data Centers 尚無重大收入，預期成為長期可預測收入來源。","source":"SEC EDGAR 10-Q Q1 2026","url":"https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000054/glxy-20260331.htm","excerpt":"Solutions business generates management and performance fees on assets under management, fees on assets staked to our validator nodes and licensing fees from institutions who leverage our proprietary self-custody technology. Within our Data Centers operating business segment, we expect the majority of revenue to come from long-term lease agreements with cloud service provider clients that","as_of":"2026-05-01","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 共識目標價約 $39.21（14 位分析師），最新一筆為 Piper Sandler $33（2026-07-17）；Investing.com 平均 $41、高 $57、低 $26，14 買 2 持有 0 賣。聚合站樣本與日期不一，無單一權威共識。","source":"Benzinga GLXY analyst-ratings；Investing.com GLXY consensus estimates","url":"https://www.benzinga.com/quote/GLXY/analyst-ratings","excerpt":"Galaxy Digital Inc has a consensus price target of $39.21 based on the ratings of 14 analysts.","as_of":"2026-07-17","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"tickflow 資料（as of 2026-07-31）9 位分析師平均目標價 $33.67，最低 $24（Goldman Sachs），低於 Benzinga／Investing 的 $39–41，分布分歧。","source":"tickflow.io GLXY forecast","url":"https://tickflow.io/stock/GLXY/forecast","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"公司未提供正式數字 guidance，分析師預估為唯一基準。Q3 2026 調整後 EPS $0.83 vs 共識 $0.13，營收 $8.69B vs 預估 $12.12B（EPS 優於、營收低於）；同時宣布 $200M 買回。Chartmill 的預估修正欄位為 N/A，查無修正資料。","source":"247wallst Galaxy Digital Q3 2026；CrowdFund Insider 2026-10","url":"https://247wallst.com/cards/galaxy-digital-q3-2026-earnings-glxy-01m5ygtstptb75e50mbgbfmz11","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"安大略省擬議集體訴訟（LUNA 相關不實陳述指控）尚未認證，認證聽證排定 2026 年 6 月；結果未知","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"The plaintiff’s motion for leave and certification is scheduled to be heard in June 2026. Based on the stage of the case, the outcome remains uncertain, and the Company cannot estimate the potential impact, if any, on its business or financial statements at this time.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"與紐約州檢察長就 LUNA 達成和解，未折現 2 億美元，2025–2028 分期支付；2025 年底計提 1.51 億美元","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"On March 27, 2025, Galaxy reached an agreement with the New York State Attorney General to resolve civil claims related to certain investments, trading, and public statements made in connection with the LUNA digital asset from late 2020 to 2022.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Galaxy Helios Data Centers II 完成 35.07 億美元 9.875% 2031 年到期優先擔保票據發行","source":"SEC EDGAR 8-K Item 1.01 (2026-07-28)","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000079/glxy-20260728.htm","excerpt":"The aggregate principal amount of Notes sold in the Offering was $3,507,000,000.","as_of":"2026-07-28","retrieved_at":"20261103","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"2026-05-08 簽訂最高 5 億美元 ATM 增資協議","source":"SEC EDGAR 8-K Item 1.01 (2026-05-08)","url":"https://www.sec.gov/Archives/edgar/data/1859392/000162828026032991/glxy-20260508.htm","excerpt":"pursuant to which the Company may sell up to an aggregate of $500,000,000 of Common Shares.","as_of":"2026-05-08","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"GLXY 數位資產貸款的信用損失備抵：2025-12-31 為 $96K，2026-03-31 升至 $216K，2026-06-30 維持 $216K；搜尋未見 NPL/NCO 揭露","source":"Galaxy Digital Form 10-Q (period 2026-06-30), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000091/glxy-20260630.htm","excerpt":"Less: Allowance for credit losses (216) (96)","as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"GLXY 淨數位資產貸款 2026-03-31 為 $670.1M（2025 年底 $1,078.9M），2026-06-30 回升至 $786.7M","source":"Galaxy Digital Form 10-Q (period 2026-06-30), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000091/glxy-20260630.htm","excerpt":"Digital asset loans receivable, net $786,680","as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"+","claim":"GLXY 以抵押品公允價值作為估計信用損失的實務權宜法；多數貸款超額抵押","source":"Galaxy Digital 10-Q / 424B3 filings, SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001859392/000185939226000091/glxy-20260630.htm","excerpt":"most of the Company's loans are over collateralized","as_of":"2026-06-30","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#3","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"Morgan Stanley 的 Andrew Sheets 認為 2026 信用循環將先走熱再結束、尚未出現裂縫（總體信用循環階段：晚期但仍擴張）","source":"Morgan Stanley Thoughts on the Market, credit cycle 2026","url":"https://www.morganstanley.com/insights/podcasts/thoughts-on-the-market/credit-cycle-2026-andrew-sheets","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"0","claim":"世界交易所聯合會（WFE）要求 Basel 委員會修訂銀行加密資產曝險審慎標準；Basel 標準原訂 2026-01-01 實施，並已同意加速檢視（銀行端規則，間接影響加密業務）","source":"FOW: WFE urges Basel rethink on crypto capital rules","url":"https://www.fow.com/insights/wfe-urges-basel-rethink-on-crypto-capital-rules","excerpt":"WFE urges Basel rethink on crypto capital rules 18th March, 2026 Zak Jakubowski","as_of":"2026-03-18","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"搜尋結果未見 GLXY 被併購或重大併購交易；Q2 2026 財報稱季後購入德州三處 AI 資料中心站點，電力管線逾 5.7 GW（資產購置，非公司併購）","source":"WebSearch 摘要（引 Galaxy Q2 2026 業績，2026-08-05）","url":null,"excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"安大略省擬議集體訴訟（LUNA）未認證，認證聽證排定 2026 年 6 月；未見美國證券集體訴訟","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1859392/000185939226000016/glxy-20251231.htm","excerpt":"The plaintiff’s motion for leave and certification is scheduled to be heard in June 2026.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"+","claim":"SEC 執法部門兩項調查已於 2025 年 2 月收到終止函、無指控結案；未見近12個月新調查或重編","source":"WebSearch 摘要（引 Galaxy 申報文件風險因素）","url":null,"excerpt":"In February 2025, we received termination letters concluding these investigations without charges.","as_of":"2025-02-28","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GLXY","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":-0.45,"operating_margin_pct":-0.28,"fcf_margin_pct":-7.17,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GLXY","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COIN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.01,"operating_margin_pct":5.68,"fcf_margin_pct":68.4,"rd_intensity_pct":34.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COIN","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"HOOD","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.44,"operating_margin_pct":45.65,"fcf_margin_pct":58.44,"rd_intensity_pct":19.34},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HOOD","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"IREN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":62.32,"operating_margin_pct":-53.57,"fcf_margin_pct":-332.45,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IREN","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"GLXY"},"financial_history":{"ticker":"GLXY","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":0.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":-522676000.0,"diluted_eps":-4.99,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":51626779000.0,"revenue_yoy_pct":null,"gross_margin_pct":-0.21,"operating_margin_pct":0.74,"net_income":228514000.0,"diluted_eps":0.6,"free_cash_flow":-49692000.0,"fcf_margin_pct":-0.1,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":42596673000.0,"revenue_yoy_pct":-17.49,"gross_margin_pct":-0.26,"operating_margin_pct":1.69,"net_income":346722000.0,"diluted_eps":0.84,"free_cash_flow":-264104000.0,"fcf_margin_pct":-0.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":60406728000.0,"revenue_yoy_pct":41.81,"gross_margin_pct":-0.19,"operating_margin_pct":0.95,"net_income":-241349000.0,"diluted_eps":-0.61,"free_cash_flow":-1509170000.0,"fcf_margin_pct":-2.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GLXY/GLXY_Q3_2026_Earnings_Call_20261027.md）

# Q3 2026 Earnings Call
**Galaxy Digital Inc.** | Earnings Calls | 2026-10-27

**Operator** (Operator):
Good morning, everyone, and welcome to the Galaxy Digital Third Quarter 2026 Earnings Call. Today's call is being recorded. [Operator Instructions]
At this time, I'd like to turn the floor over to Taylor Reinhardt, Head of Investor Relations. Please go ahead.

**Taylor Reinhardt** (Executives):
Good morning, and welcome to Galaxy's Third Quarter 2026 Earnings Call. Before we begin, please note that our remarks, including answers to your questions, may contain forward-looking statements. Actual results may differ materially from those described in these statements as a result of various factors, including those identified in the disclaimers in our earnings release or other filings, which have been filed with the U.S. Securities and Exchange Commission and on SEDAR+. Forward-looking statements speak only as of today and will not be updated. Additionally, we may discuss references to non-GAAP metrics, the reconciliations of which can also be found in our earnings release. Finally, the information on this call does not constitute a recommendation, solicitation or offer by Galaxy or its affiliates to buy or sell any securities.
With that, I'll now turn the call over to Mike Novogratz, Founder and CEO of Galaxy, to discuss the results.

**Michael Novogratz** (Executives):
Good morning, everyone, and welcome, Taylor, to the Galaxy team. You guys will get to know her well and like her as much as we do. Listen, we had an awesome quarter. I'm really proud of what the team delivered. But what excites me more is what performance says about where Galaxy is headed. We spent years investing ahead of 2 enormous shifts, finance moving on chain and the build-out of AI infrastructure, and we're increasingly seeing those investments translate into results with the strategy playing out in 3 important ways this quarter.
First, we saw a strong rebound in crypto markets. Bitcoin was up more than 40% with a meaningful improvement in sentiment and client activity. Our Global Markets business capitalized on that momentum, growing trading volumes and expanding client engagement. We also saw a significant appreciation across our investment portfolio, reflecting the value of capital we've deployed across crypto and the broader technology ecosystem.
Second, the opportunity in digital assets is getting bigger, and I think we're just scratching the surface of what's ahead. Crypto remains an important and growing asset class, but the opportunity extends well beyond that, with digital assets increasingly becoming the foundation for the future of finance. And increasingly, those 2 worlds are coming together. You can see it in the growing adoption of stablecoins, the tokenization of traditional financial assets and the participation of major financial institutions.
I have a tremendous amount of conviction that the financial architecture developed by the crypto industry will underpin much of how the financial system operates in the future. Galaxy has spent years investing in these capabilities, and we're still in early stages, I believe that, that investment will translate into meaningful results over the next several years. Regulatory clarity will be an important part of that. While the CLARITY Act has not become law, unfortunately, the SEC and the CFTC are working towards clear frameworks. There's still a lot to sort out, but the direction is encouraging.
And investing ahead of these shifts has always been part of our strategy. We did it early in crypto, investing in companies and technologies that help build the ecosystem. And now we're taking that same approach to AI, increasingly investing in the next generation of companies through our investment strategies and our balance sheet.
Third is data centers, where we're building a very sizable business. Helios has come a long way in the past year. We're now generating approximately $80 million of leasing revenue per quarter from Phase I. As Phase II comes online next year, we expect to exit 2027 at an annualized leasing revenue run rate of between $800 million and $850 million based on our current delivery schedules. That is a substantial business from the capacity we've already leased, and the momentum is building. We have significant additional approved power available to lease and a deep development pipeline beyond that.
I want to address the timing of leasing announcement at Helios II. Earlier this year, I spoke about the possibility of reaching agreement during the summer. We were in advanced discussions around a potential transaction, but as the market dynamics shifted materially in late summer, we ultimately decided not to move forward on the terms being considered. The market for large-scale power via data centers has become increasingly constrained, while demand for capacity beginning in 2028 and beyond has strengthened. With more than 800 megawatts of secured power and supporting infrastructure, we believe Helios II is an even more valuable asset today than it was just a few months ago. And with delivery plan for 2028, we have the flexibility to evaluate our opportunities and get the right deal.
We built Galaxy by adapting to changing markets and being disciplined about where we commit capital. These are large long-term agreements, and we're not going to compromise on terms just to meet an announcement date. We continue to have productive and active discussions with prospective customers with a focus on maximizing long-term value for shareholders.
And as the Helios campus scales, we're fundamentally changing the earnings profile of Galaxy. We've established a Digital Asset franchise with significant earnings power, growing opportunities for recurring fee-based revenue and a data center business is adding long-term contracted cash flows. Together, these businesses give us multiple drivers of growth and more diversified earnings base that we believe will make Galaxy a stronger, more durable franchise over time.
We also have the balance sheet to back that ambition. It's a competitive advantage that allows us to commit capital as a principal, invest in growth across our businesses and take advantage of opportunities as they arise. We're focused on putting that capital to work where we see the most attractive long-term returns. That includes investing in our own shares when we believe they're trading at a meaningful discount. We've repurchased $200 million year-to-date and this morning announced an additional $200 million share repurchase authorization. As significant shareholders ourselves, we see buybacks as another potential way to allocate capital thoughtfully to create long-term value.
Chris will now take you through how we're translating these opportunities into results across our businesses and what we're focused on next. Chris, over to you.

**Christopher Ferraro** (Executives):
Thanks, Mike. Starting with digital assets. One of the strengths of our Global Markets business is the breadth of solutions we can offer clients. We're seeing growing demand for more sophisticated trading and financing solutions, particularly as traditional financial institutions look to participate in decentralized markets through products and structures they're familiar with. We spent years building capabilities for crypto-native clients, and that experience gives us an advantage as traditional finance increasingly moves on chain.
We understand these markets can move quickly and have the flexibility to develop solutions for both groups. Lending is a great example. We've expanded the Galaxy Onchain Financing Rate or GOFR, which gives clients access to on-chain financing alongside our growth financing facility, which allows us to support more lending activity through external capital. We're expanding our loan syndication, collar lending and structured financing capabilities, broadening the range of clients and financing needs we can serve.
We're seeing the same innovation across trading. Our derivatives business executes sophisticated options and hedging strategies for clients. And this quarter, we completed our first compute-linked derivatives transaction, extending our capabilities into an emerging market that we believe has the potential to grow into a sizable new stand-alone asset class. In Asset Management, we're expanding our investment strategies and product offerings to meet evolving institutional demand.
During the quarter, we launched the Galaxy Sharplink Onchain Yield Fund, an actively managed strategy, providing access to yield opportunities in decentralized finance through an institutionally managed SMA for a public company. Sticking with Onchain Asset Management theme, SWEEP, the first-ever decomposable 24/7 Onchain money market fund in partnership with State Street Global Advisors is now approaching $300 million of AUM, which we believe is an early signal of strong product market fit among first-mover institutions interacting with tokenized real-world assets.
With Galaxy Digital Ventures, we are progressing towards a first close of Fund II expected towards the end of Q4 with a fund target size of $250 million to $300 million. As an investor, you only win the right to raise a second larger fund once you've proven out a strong process and great returns. And the GV team has done that with Fund I currently marked at 2.25 gross MOIC.
In digital asset infrastructure, we're seeing growing momentum with some of the world's largest financial institutions and are expanding our capabilities and offerings across tokenization, custody and staking to meet their evolving needs. Staking is an area where we're seeing growing engagement with major institutions. Assets under stake grew 64% in the quarter to $4.6 billion.
While this was primarily driven by price appreciation of the underlying assets in the quarter, we've also seen a number of large ETF providers begin delegating their ETH and SOL stake to Galaxy's infrastructure, driving over $400 million of gross new inflows in Q3 and subsequent to quarter end, and we expect additional sizable partner launches before year-end.
More broadly, our relationship with BNY announced this summer has been an important validation of our capabilities as we continue to deepen our engagement with leading global financial institutions. These are complex engagements with long sales cycles, but the potential is significant. Our objective is to become a long-term strategic partner as institutions build out their digital asset businesses, creating opportunities to expand relationships beyond initial mandate and generate meaningful recurring revenue over time.
Turning to our data center business. We're continuing to deliver against our development plans while advancing a substantial pipeline of future opportunities. This was our first full quarter of leasing revenue from Helios, marking an important milestone as our development investments and long-term contracted revenues begin converting into realized contracted cash flows. Phase II, which will deliver an additional 260 megawatts of critical IT capacity is fully funded and under construction, putting us in a strong position as financing for new data center developments become increasingly constrained.
Both buildings and the supporting substation are progressing on schedule and within budget, building on our successful delivery of Phase I. Structural steel installation is well underway on the first building. Construction is advancing on the second and key electrical infrastructure is being installed. We expect construction activity to ramp significantly over the coming months with data hall deliveries scheduled to begin in the second quarter of 2027.
On permitting, we've secured the key environmental approvals required for ongoing construction at Helios. While certain additional approvals remain outstanding following Governor Abbott's September directive, we do not currently expect an impact to our construction progress or our anticipated energization time lines.
Turning to Helios II. To build on Mike's earlier comments, we saw several important shifts in market dynamics beginning in late summer that we believe have meaningfully strengthened our competitive position. Forward power availability has become increasingly constrained with new power approvals more difficult to secure and delays in competing developments limiting the amount of large-scale compute capacity that can realistically be delivered between 2028 and 2030.
At the same time, we're seeing a meaningful increase in demand from hyperscalers, frontier labs and neoclouds, now looking to secure capacity for 2028 and beyond to support existing backlogs and future growth. Underlying demand for compute remains as strong as we've ever seen it.
Financing markets have also become more selective, and we believe access to capital will increasingly favor developers with proven execution capabilities, high-quality counterparties and financing structures that appropriately allocate risk. Having successfully delivered Helios Phase I with Phase II fully funded and progressing on schedule, we are building a track record that we believe will differentiate Galaxy in this environment.
Meanwhile, the evolving regulatory and political landscape in Texas has created additional uncertainty around future data center development. Based on our current understanding of the applicable requirements, we do not believe Helios II is subject to the same uncertainties facing certain other projects, further strengthening its relative attractiveness. Taken together, these developments have changed how we evaluate the opportunity at Helios II. We're taking the time to engage with the right counterparties and evaluate structures that we believe can maximize long-term shareholder value for Galaxy. The focus of our active conversations is squarely on investment-grade hyperscalers or counterparties supported by investment-grade credit enhancements, considering not only headline economics and counterparty quality, but also critical lease terms, probability of execution and future growth potential outside of the Helios campus.
Beyond Helios II, we've made meaningful progress through ERCOT's Batch Zero process. As announced in September, 5 of our Texas data center projects received conditional Batch Zero classifications, representing approximately 4.2 gigawatts of capacity. That includes more than 1.6 gigawatts of previously approved baseload capacity at Helios I and II, which remains largely unaffected by the ongoing ERCOT process.
Our 3 expansion projects, Caspian, Selene and Helios III received Studied Load classifications, representing an additional 2.6 gigawatts of potential capacity. While we submitted Caspian for baseload classification, ERCOT ultimately reclassified it as Study Load and our subsequent dispute for reconsideration was denied. Although that wasn't the outcome we had sought, Caspian remains part of the Batch Zero study, and we expect greater clarity on power allocation and anticipated energization time lines for these projects in April 2027 based on the time lines communicated to us by ERCOT. These classifications cover a substantial portion of our broader development pipeline of more than 5.7 gigawatts, providing a foundation for potential growth well beyond the initial phases of Helios.
Beyond our data center business, we're also investing in the growth of AI across the firm with a focus on opportunities ranging from frontier model developers to emerging technologies at the intersection of AI and financial infrastructure. Through Galaxy Ventures and our broader investment activities, we're building on our experience gained from investing early in the digital asset ecosystem.
To date, we've deployed more than $80 million across 11 portfolio companies via 17 investments, including SpaceX, Etched, Karta, Ornn, TRM Labs and Architect. While these companies are all early in their growth journey, our current unrealized mark-to-market on that pool of investments is already 3.4x.
Importantly, our ambition extends beyond just generating returns for our balance sheet, we're using these investments to build a track record, establish relationships and create commercial opportunities across the Galaxy platform. Across our businesses, we're focused on translating the investments we've made into tangible results and long-term earnings growth. I'll now turn the call over to Tony to discuss our financial results.

**Anthony Paquette** (Executives):
Thanks, Chris and Mike. For the third quarter, Galaxy reported net income of $323 million, adjusted gross profit of $569 million and adjusted EBITDA of $455 million, marking a sharp improvement from second quarter performance. Our results reflected the continued earnings power of our digital assets franchise, the first full quarter of leasing revenue from Helios and significant appreciation across our investment portfolio. Firm-wide operating expenses, excluding grossed-up transaction costs, digital asset impairments and pass-through data center operator costs were $161 million compared with $147 million in the prior quarter. This increase was primarily driven by higher depreciation and amortization expense related to Helios Phase I entering full operation.
Our operating businesses generated combined adjusted gross profit of approximately $150 million, up more than 75% from $86 million in the prior quarter and adjusted EBITDA of $60 million compared with approximately $1 million in Q2. On a segment level, starting with digital assets, the business generated $71 million of adjusted gross profit, up from $66 million in the prior quarter, reflecting increased client activity and the breadth of our platform.
Within Global Markets, adjusted gross profit increased to $53 million from $49 million in Q2. Our digital asset trading volumes grew 12%, outperforming the broader spot market where volumes declined, demonstrating the strength of our trading franchise. In lending, our average loan book grew over 25% to approximately $1.8 billion, reflecting continued demand for our financing solutions.
Asset Management and Infrastructure Solutions generated $19 million of adjusted gross profit compared to $17 million in the second quarter. Assets under management increased by over 30% to $5.9 billion, driven by growth of more than 40% in ETFs and 30% in alternatives. As Chris mentioned, assets under stake also increased more than 60% to approximately $4.6 billion, reflecting both market appreciation and new capital inflows. Fee growth was more modest during the quarter as reported AUM reflects quarter-end balances, including capital raised late in the period, while fee revenue reflects activity throughout the course of the quarter.
Turning to data centers. We generated approximately $79 million of adjusted gross profit and $69 million of adjusted EBITDA, representing the first full quarter of contribution from Helios Phase I. Capital expenditures were approximately $757 million during the quarter compared with $448 million in Q2. We expect spending to increase as Phase II construction progresses with a significant portion of the remaining construction expenditures anticipated in the first half of 2027.
As a reminder, there are a few moving pieces related to interest income and expense in our data centers business that will affect our financials over the coming quarters. As financing proceeds are deployed into construction, our short-term investment balances and related interest income will decline. At the same time, a greater portion of our borrowing costs will be capitalized on the balance sheet rather than expensed through the income statement. At quarter end, Data Center segment had approximately $6.8 billion in total assets and approximately $5.3 billion in total liabilities, reflecting continued investment in Helios and the financing secured for Phase II. We do expect this segment's total asset base to grow as construction progresses and capital is deployed.
The Treasury & Corporate segment generated $419 million of adjusted gross profit during the quarter compared with a $42 million loss in Q2, driven primarily by significant appreciation across our digital asset holdings and private investments during the quarter, including notable contributions from Etched and Forward Industries, among others.
As Mike mentioned, these investments reflect our ability to identify compelling opportunities across the digital asset ecosystem and broader technology ecosystem and represent an important source of long-term value for Galaxy. We also held approximately $1.7 billion in net digital assets and investments at quarter end, up nearly 50% from Q2, including exposure to Bitcoin and other liquid digital assets.
Firm-wide, we ended the quarter with approximately $4.9 billion of cash, stablecoins and treasury bills compared with $2.5 billion at the end of June. This increase was driven largely by proceeds from the $3.5 billion financing completed during the quarter to fund construction of Helios Phase II. Looking ahead, we anticipate pursuing Phase II financing in the first half of 2027, with the structure of that financing being informed by market conditions, comparable transactions and our assessment of the most attractive terms available. We also had $445 million of exchangeable notes maturing in December 2026.
We have the necessary resources on balance sheet to meet that maturity today, but are always evaluating different financing options in the context of our overall liquidity position and broader capital priorities. We exited the quarter with approximately $3 billion of book equity with more than 80% allocated to our operating businesses, providing a strong capital foundation as we continue to scale. On share repurchases, we deployed approximately $79 million during the third quarter. And as Mike mentioned, we purchased the remaining portion of our previously authorized $200 million during the month of October.
These repurchases have more than offset dilution from equity-based compensation, contributing to a net reduction in shares outstanding year-to-date. The Board's approval of an additional $200 million authorization announced today allows us to continue opportunistically buying back stock when we believe it's trading at a meaningful discount to intrinsic value and it fits within our broader capital plan.
With that, operator, let's open the line for questions.

**Operator** (Operator):
[Operator Instructions] Our first question today comes from Patrick Moley from Piper Sandler.

**William Copps** (Analysts):
This is Will Copps on for Patrick. I want to go back to the comments on the Helios lease discussions over the summer. Can you help us understand what led you to step away and what terms you need to see in the deal you're willing to sign? Was it driven mainly by economics and revenue or potentially more by counterparty and credit support or something else?

**Christopher Ferraro** (Executives):
Thank you for joining for the question. So as we said in the remarks, we have been pursuing opportunities throughout the year at early stages given that Helios II energization time line really isn't until the middle of 2028 at the earliest expected right now. Those conversations got pretty serious going into the summer. And then a lot of stuff happened, right? The -- we saw actual projects around us getting delayed. We saw regulatory headwinds, not just in Texas but across the country tightening up and therefore, an expectation that available power on the forward was going to be tighter than I think we or the market really understood.
At the same time, we saw a number of financing structures start to come into the market, think like investment-grade wraps around noninvestment-grade potential counterparties that we thought were interesting and that we were evaluating. The issue there is the devils are in the details. And so an investment-grade wrap that doesn't actually achieve investment-grade protection for both our debt and our equity isn't really investment-grade wrap. And you don't really know those things until you get into the details and you get to the finer points.
And finally, to sort of back that up, the financing markets, obviously, around that time also started backing up. And the focus on structure, counterparty is really came into light for us and for the whole market. And so with all that as a backdrop, we decided to take a pause, take a breath, reignite conversations more broadly. And that sort of happened at exactly the same time that a number of the big hyperscalers started turning their attention to 2028 available power. And so that's what led us to decide to broaden out the process. And that's why now we're in active conversations with a number of high-grade potential tenants who are now very focused on figuring out what their power strategy is for 2028.

**Operator** (Operator):
Our next question comes from James Yaro from Goldman Sachs.

**James Yaro** (Analysts):
I was hoping you might be able to update us on your current capital deployment priorities in light of the new buyback program, the maturing notes at the end of the year as well as the continued need to deploy capital into the data center segment. And could you speak to your appetite, I guess, or maybe just expand on your appetite to potentially replace the notes maturing in December with additional debt?

**Anthony Paquette** (Executives):
Yes. Sure, James. I'll take that one. So first, when we think about capital planning, we start with what is the business need across our 2 businesses, which obviously have different capital need profiles. But that is the first focus for capital requirements. We obviously have a funding and financing plan for the data centers. The digital asset businesses broadly tend to be self-financing in many ways as financial services oriented. And so we think of our business needs as the first priority.
Secondly, I would say we think about a capital buffer and cushion on the balance sheet, maintaining a healthy, strong, robust balance sheet, I think, is a very important principle from our standpoint. As we talked about, we have significant cash, stable coins and liquidity on balance sheet in addition to liquid investments on the balance sheet that we have the ability to shift around as necessary. As you'll see, we've got about 80%, actually more than 80% of our capital now deployed into our operating businesses. We've talked about this over the last couple of quarters. You should expect that number to increase as we see the investment in those businesses grow out.
And then third, we extinguished the buyback, the $200 million initial. We thought it was appropriate to have an additional authorization, but we will be very, I would say, opportunistic in how we think about deploying additional capital from a buyback perspective. And the second part of your question, remind me just second part of your question.

**James Yaro** (Analysts):
If you could just maybe just expand a little bit on the comments around the exchangeable notes and I guess, appetite to replace that. I think you pointed out you have enough resources to not have to do so, but just maybe the moving parts there.

**Anthony Paquette** (Executives):
Yes, yes. Got it. Yes. So the exchange. So we have $445 million of exchangeable notes maturing in December. Look, the way we think about that is, first and foremost, we have the capital resources to pay that back in full without refinancing it. As you know, we did a convertible issuance Q4 of last year. Those resources were deployed across our operating businesses and to sort of prefund some of this. And so we're not going to precommit to anything in terms of what we may or may not do for broader debt or capital planning. But suffice to say, we have the resources to pay that back in the near term.

**Operator** (Operator):
Our next question comes from Peter Christiansen from Citi.

**Peter Christiansen** (Analysts):
I wanted to ask about the digital assets part of the business. You generated decent gross profit this quarter. You had EBITDA still negative. I'm just curious, what are some of the key investments that's suppressing profitability there? And how do you think for digital assets to become more sustainably EBITDA, what do we need to see occur?

**Anthony Paquette** (Executives):
So thanks for the question. This is Tony. I'll start and Chris can add as he sees fit. So I would say broadly the second quarter, as we talked about in our comments, the broader landscape was volumes and activity in the crypto space were down. Obviously, the price of crypto is still something underlying that drives a lot of the activity in our trading and derivatives businesses. We continue to outperform in that space. Our volumes were up on a quarter-over-quarter basis. We believe we're continuing to take share in those businesses. Our lending book grew about 25% quarter-over-quarter. And we're adding recurring revenue streams, which we think is the most important part of building a more durable business.
We do continue to invest. We are making investments in a few different areas that we've talked about, digital infrastructure areas where we see future growth and so as activity continues to pick up, I think we'll -- you should see us move closer towards consistent profitability in that segment. The other thing I would mention, it's a bit nuanced, but we did have a small accounting adjustment that we -- in terms of how we accounted for certain things in the business that if not for that change on a quarter-over-quarter basis, we would have been profitable in that segment just this quarter. It's sort of a onetime shift. But other than that, we're -- Chris, I don't know if you have any other comments.

**Christopher Ferraro** (Executives):
Yes, I'll just supplement that a little bit. I think there's a few things going on in digital assets and the broader financial infrastructure markets that drive our thinking and our planning around profitability and what we're investing in. The key is, like, one, volumes in the narrow niche crypto market obviously are suppressed and are a bit challenged at the moment. And our business generally is a pipe business where the more volume that flows through it, the more opportunity there is for us to generate revenue for the business historically at least. We do have a long-term view on crypto assets like Bitcoin, for example, and the decentralization theme, particularly in a more complicated digitally driven agentic AI world.
But that aside, the other thing that's happening is a transition to real-world assets of the legacy financial system moving on chain. And so what we're doing today is prosecuting the business that we can in the crypto markets while investing in technology and people and licensure, for example, so that we are going to be in a position to be on the forefront to be able to service the transition of volumes from traditional legacy real-world assets on chain into a digital form.
And so we actually -- while we never like to lose money ever, being able to sustain the amount of revenue we have in this niche market while being able having the luxury of being -- having the capital to be able to invest in growth so that we're positioned to capture that mega opportunity is really where we're at in the business today.

**Operator** (Operator):
Our next question comes from James Faucette from Morgan Stanley.

**James Faucette** (Analysts):
I wanted to ask quickly on Helios 1 and working with CoreWeave there. Just any insight you can share with us around what you know about their agreements with their partners for not only Phase I, but also if that's going to -- if that same partner is likely to also take on Phases II and III.

**Christopher Ferraro** (Executives):
Sure. James, thanks for the joining, for the question. So let me -- I'll just -- I'll set the stage for our relationship with CoreWeave, how it's set up and how we understand their contractor structure and how their business model works. And I think it's important and it's illustrative of how we think about the risk and also the insight we have or don't have into their ultimate operations. Our relationship with CoreWeave with the 3 leases that exist today for Helios I also at CoreWeave's parent company. We face CoreWeave Inc.
The way we think about that is that means that ultimately, we face CoreWeave's entire portfolio of customers. And we face effectively CoreWeave's residual equity and interest in those contracts after their site level GPU secured financings. That's pretty much the business model. That's our exposure. We like that exposure because what it means is that we are not subject to at our facility, a single counterparty look through exposure in the instance where there's an idiosyncratic problem with that one counterparty. CoreWeave's portfolio of pretty much all the entire hyperscaler universe and most of the Frontier labs is the credit that we look to across their whole portfolio.
Now CoreWeave's contracts, while we don't have insight into all of them or into the specificity necessarily, CoreWeave generally contracts with its customers under for, I believe now the average is closer to 5 years as they reported on a GPU hour basis generically, not on a facility level agreement. And so what that means is CoreWeave has the ability to balance their loads to their customers across their data center footprint. That's important because it means that the answer to the question of who's the underlying tenant at Helios, by definition, can and we expect will change over time, both because they commit generic GPU loads to their clients and because we know that the tenors of their contracts are shorter than the leases they have to sign by definition.
We have been communicated by Tim from CoreWeave that the loads running today that we see every day on the screen in Helios I are coming from a customer contract that's currently allocated to a large multitrillion dollar investment-grade hyperscaler.
We don't have insight yet into ultimately who's going to be in Phase II, let alone Phase III. That will happen as we get closer to energization and data hall turnover, and they decide at that point in time in 2027, where their load is needed and where they want to allocate load to a particular facility. And so that's really the setup. I know that investors want to hear a direct look through to investment-grade counterparty on the other side.
It's just not the business model and not the way the contracts are set about the CoreWeave side. And it's the platform and the risk that we underwrote when we originally did the transaction. That's not to say -- I'll add one thing. I was going to add that's not to say that there won't be opportunities if it's credit enhancing to look through to a direct customer and drop it down in SPV, for example, which we've seen happen once or twice in the market so far. But that sort of is downstream from CoreWeave financing their GPUs and getting better execution on their GPU financing through an SPV direct deal and would come with our ability to approve or disapprove of any change in the tenant from the CoreWeave parent company down to a particular SPV. And so we'll look at that on a case-by-case basis and evaluate it and assume it's credit enhancing. It's obviously something that we would engage with.

**James Faucette** (Analysts):
Got it. That's really helpful. And then back on the Helios II and, kind of, the engagement there. Obviously, I think we're all sensitive to the changes in some of the market dynamics, et cetera, that Mike alluded to and mentioned at the outset. Are there key market, incremental market changes or clarifications that we should expect to come through before you would be able to announce a new tenant for Helios II? Or I'm just trying to get a sense of what the time line and checklist is we should be paying attention to for that.

**Christopher Ferraro** (Executives):
Yes. So the dynamics there, I tried to lay it out as clearly as possible in the prepared remarks. There's a few things that I would look towards. There's nothing today holding us back from executing on what would be a deal with an end tenant. Like the speculation around late summer and the timing and the conversation we're in like we could have signed a deal had we wanted to. A lot of that was in our control to make a decision go forward. We proactively chose not to because of the change in market dynamics. And that still sort of exists today.
There is, obviously, Texas, there's a lot going on in Texas from a regulatory perspective. There are some key dates coming up. In December, we expect to have clarity on audit results that we've submitted across the assets, including Helios II. All of those things, in April of 2027, we expect to get allocations of Batch Zero Studied Load, power, et cetera. Like all of those things are on potential tenants minds. What I would say quite clearly is there are absolutely investment-grade tenants who despite questions around the ERCOT process, want to contract and lock up power.
And when they do the work on our portfolio, in particular, on Helios I and Helios II, we think they generally come to the same conclusion we have, which is Helios is a pretty unique asset in terms of when its studies were approved prior to the batch process and the likelihood that Helios II is going to be unimpacted generally by any of the uncertainty.
But nonetheless, like those dates are key. And for some of the tenant base looking at it, they're looking for us to pass through those unscathed as we expect to in order to sort of finally contract. Again, that's not the entire base. There are absolutely deals we expect we could do. But the entire universe, clarity on the regulatory front in Texas, in particular, is -- would help the process along.

**Operator** (Operator):
Our next question comes from Devin Ryan from Citizens Bank.

**Devin Ryan** (Analysts):
I want to come back to Chris' comments on, kind of, broadening the pipes to be able to trade more, kind of, a couple of parts here. What else are you watching on regulatory guidance that you guys think is critical from here? And then assuming that progresses, how are you thinking about where Galaxy is best positioned to participate in tokenization? Meaning how do you see Galaxy being able to compete with, obviously, well-funded incumbents that will likely be coming here as well?
And then are there specific real-world assets that are more attractive to Galaxy. And then even beyond just trading and trade finance, how do you see Galaxy's potential infrastructure partner here as we, kind of, progress to this world of tokenizing more real-world assets and trading them? I appreciate there's a lot in there, but just love some thoughts.

**Michael Novogratz** (Executives):
Yes. It's Mike. Listen, so our big bet is that the infrastructure that crypto created is going to end up being the infrastructure that a lot of the traditional world operates on. When that happens, we'll see, right? It is starting to happen. I would tell you that almost every traditional finance shop is building towards that, partly because they have to because it happens, they need to be there. One of our businesses, that is we're putting a lot of effort into and is growing, is actually being a partner to help build that infrastructure for traditional finance companies.
That's, in some ways, a fee or a SaaS business, but the real upside of that is once you get partnership, the ancillary services, the trading, the potentially offering other products, that's where the growth of those things come. And so we announced the deal with Bank of New York. We are very engaged with a few other large participants. And, like, I think that's a good strategy. It's not going to dominate our revenue in the next 12 months. But when I look out 24 and 36 months, it's where I think we'll be a key part of that play.
The second real angle is on chain credit. Chris talked about a few of the deals we've already done. Like we have credit as part of our DNA. Chris came from a credit shop. It's been a big driver of our business since we started. And we are one of the leaders of on-chain credit today. We think that business is going to continue to grow. And so building on chain Prime, building on chain credit, on chain Asset Management lives really on top of that. That I'd love to say in 2 years, we're really an on-chain -- our Digital Asset business is really an on-chain Digital Asset business. And that's what we're driving towards. And that's what -- when someone asked Tony about the investment dollars, they're all tech dollars and they're all tech dollars and regulatory dollars going into that build-out.

**Operator** (Operator):
Our next question comes from Edward Engel from Compass Point.

**Edward Engel** (Analysts):
Back in February, I think you, kind of, acknowledged maybe aspirations that you'd have a deal for Helios II within the next 12 months. Should we assume this time line maybe gets extended by a little bit just given that you walked away from the deal this summer? And then just quickly on Helios I financing. I think you last mentioned that the Phases I and II should have enough free cash flow to, kind of, self-fund Phase III. Has that also changed just given maybe the exchangeable notes that are due and maybe some of the recent buybacks on.

**Anthony Paquette** (Executives):
Yes. Ed, I'll take the first part of the question. On Helios II leasing time line, I think we've covered a lot of it so far. I think the expectations around timing of signing a deal, let's start from the fact that Helios II energization time line is expected to be in mid-2028. If you work back from mid-2028, that gives us 1.75 roughly years of room for both finding the right partner, negotiating the right deal, design, planning and then ultimate construction.
While that's not infinite time, that is a lot of cushion that we have, which we appropriately think we should take given how dynamic the market is to find the right partner, get the right economic transaction because these are deals we have to live with for effectively the rest of our professional lives given their tenure. So we take it very seriously. It's very important. I wouldn't peg a specific time. I would tell you, though, that it's very difficult to enter into direct conversations with some of the largest companies in the world without an intent to ultimately transact, and we are in direct conversations with some of those companies right now.
And so I'm pretty positive and pretty bullish on the opportunity set in front of us for that right now and know that our end date solving backwards is to deliver those potential clients data halls in 2028.

**Christopher Ferraro** (Executives):
Yes. On the second part of your question, so as you know, Phase I and Phase II are fully funded through the completion and end of construction. We will have the opportunity to refinance Phase I if we think the economics make sense from a refi standpoint, which may give us the opportunity to take some additional capital out. But importantly, we do not need to do that. As we've said before, Phase III is fully equity funded through the project. We intend to pursue debt financing sometime in the first half of 2027, and the equity financing being fully available already has not changed.

**Operator** (Operator):
Our next question comes from Brett Knoblauch from Cantor Fitzgerald.

**Brett Knoblauch** (Analysts):
Just like the permitting environment, I think you guys touched on it briefly in your prepared remarks regarding, kind of, Helios II. How critical is it to have all those permits in place before maybe we look to sign a lease there? And how are your customers thinking about maybe a permitting freeze and one, if the election goes the other way in Texas that potentially could be extended?

**Christopher Ferraro** (Executives):
Yes. So on the permitting front, we can take this in a couple of different tranches. One, for Helios, for Helios I and II and III under development, we have all the permits in hand needed to begin and continue construction. These are -- there are still a handful of permits that the TCEQ primarily would issue and/or approve that are not permits that would prevent us either from continuing construction or ultimately delivering and energizing data halls for the client. They're unrelated to cooling. They primarily relate around the potential to operate diesel gen backups. And so there's -- and some other like potable water and things on site. They're not limiters.
All the permits we need for those things are in hand already. And the -- for future developments that will require sort of those level of permits they're months to years out from when we would actually need them to begin construction. And so we're just very confident that while today, there's a permitting freeze, while ERCOT and all the stakeholders are attempting to comply with Governor Abbott's announcement, we're not of the belief that those time lines are going to intersect anywhere close to one another that we have concerns that permitting is going to be an issue for us at Helios.

**Operator** (Operator):
Our next question comes from Jon Petersen from Jefferies.

**Jonathan Petersen** (Analysts):
Sorry to keep going on the data center stuff. But you outlined that some of the hyperscalers might be willing to secure power now even before final approval -- or sorry, yes, secure a lease here in power even before final approvals from ERCOT. But curious what you're hearing in the project financing market and if the debt markets are, I guess, willing to be that forgiving or if we have to get past that April deadline for any potential leases you signed today to be financed?
And maybe also just, kind of, a follow-up. Just, I guess, as you talk to potential lenders, like, how much stricter are they being on different debt covenants and LTVs and LTCs and all those sort of metrics?

**Christopher Ferraro** (Executives):
Yes. So it's a very good question. The -- from a counterparty perspective, right, the -- we're not seeing -- as you pointed out, we're not seeing broadly really any pushback to, hey, let's just not engage until we see clarity in Texas. People know power exists in Texas. People know power is affordable and getting cheaper in Texas. People know that that's going to be a Tier 1 market, we believe, and they believe for a lot of time to come for these kinds of assets. And so the conversation we're having really -- they want to understand the dynamics at play with our assets, but they're certainly willing to move past that pretty quickly.
On the lender side, first and foremost, the existing facilities we have in place are not impacted at all by any potential perceived uncertainty around the Texas regulations. And so there's no permanent breaches. There's no risk to capital availability on those facilities. Those are fine. On a go-forward basis, like I do believe the risk on investing capital in advance of knowing for sure whether you have the right to energize is a risk that we, in theory, would be taking should we choose to do that and therefore, what lenders would be choosing to take along with us. And that -- and lenders generally are a lot more conservative than we would be as a developer in the equity. The good news for us is, as Tony pointed out, like, our potential financing needs outside of our own capital start to get highlighted as we turn the corner into Q1 into Q2 of 2027.
And so from a timing perspective, we, for better or for worse, have the luxury of being able to assess the regulatory environment, see how December goes with respect to the RFI audit results choose to deploy our own capital at risk based on that landscape. And we really don't have to go to the market to have conversations or will want to go to the market to have conversations until there's a lot more clarity in 2027. And so not all of our competitors are in that situation. We happen to have the luxury of being able to do that, and we're happy with that.

**Operator** (Operator):
Our next question comes from Joseph Vafi from Canaccord.

**Joseph Vafi** (Analysts):
Nice to see progress on all fronts here. I was wondering if we could, kind of, just drill down on the digital asset side of things. Is there anything particular to point to here on trading share gains in the quarter that you'd like to call out? And then just the appetite to continue to expand the lending book from here from a risk management point of view. Comments there would be appreciated, too.

**Christopher Ferraro** (Executives):
Yes. So on the trading side, I think factually, the numbers are that our volumes grew 12% quarter-over-quarter and industry volumes were roughly flat. So I think from a pure share gain perspective, we continue to make incremental gains of market share, albeit in a fairly slow and tepid environment for traditional crypto assets. But the team is performing extremely well given that condition, and Galaxy is getting stronger.
On the lending side of the business, we did expand our lending footprint over the quarter pretty dramatically. I think we were up 27% quarter-over-quarter average loan book size. We think there's huge opportunity in that space. We think that we could probably grow faster if we wanted to. That's not always the right thing to do as a lender is grow whenever you can. And so we don't. We pick our spots and we choose them wisely.
As I said in my remarks, the other thing we're really focused on, on the lending side is we're pretty cognizant that you can't really just grow a lending business, ad infinitum, with a finite balance sheet, particularly a finite balance sheet that has a lot of uses across the company. The good thing is we do have the capabilities internally, and we think there's a very large opportunity to expand our structured credit offerings to originate loans, package them, sell them off, think more traditional financial debt capital market businesses in a whole new design space on chain that really has not been tapped yet in any size.
And so I think you should expect us to both grow our balance sheet exposure to our loan book, but also be able to grow volumes outside of just our own balance sheet exposure. And the team is hard at work on creating structures, creating risk boxes so that we can do that responsibly for ourselves and potential clients and off-takers. And so more to come on that, but I think that's the future to see of our lending business.

**Operator** (Operator):
Our next question comes from Chris Brendler from Rosenblatt Securities.

**Christopher Brendler** (Analysts):
I wanted to follow up on the idea of the sort of modernization of financial infrastructure and this whole space moving on chain and Galaxy's sort of position within that opportunity. You had the BNY this last quarter. Any other sort of color you could provide on your progress with partnering with traditional financial institutions and helping with this process? And then zooming out a little bit, what does the revenue mix look like in digital assets as -- if you are successful in capitalizing this opportunity, how much will the business move away from sort of transactional and sort of lending and trading activity and more towards either asset management, custody or staking activities as you progress on that opportunity?

**Michael Novogratz** (Executives):
Well, certainly, the goal is to move away in a large fashion, right? And part of that is how fast this stuff moves on chain. It's one of these things that my intuition is it will go slow and then it will go fast, kind of, like where people go bankrupt, right? Like, it happens, it happens and all of a sudden, like, well, how does that happen? And so, we haven't seen it yet. We're seeing lots of positive signs, right? Stablecoin usage is a big part of it. But we haven't seen a wholesale shift to tokenization. People still trade, normal equity is not tokenized.
Partly, that's because most of the traditional players haven't built out their infrastructure. And so there is a scramble going on that we're part of for these institutions to build out their digital wallets, their custody, their staking abilities or to hire people to do their staking abilities for them. And I think once that infrastructure shows up, you very well might see that part of the business really start to grow. And so we're walking that tight rope between making sure our core business that we have operates as best it can and makes as much money it can while investing for this future that we're very confident will come. We just don't have the forward calendar with where the checkered flag is. I know it's not a perfect answer for you, but that's exactly the mindset that we have.
And again, we wouldn't be making this investment if we didn't have strong conviction that, that's where the world is going and seeing lots of green shoots.

**Anthony Paquette** (Executives):
I'll just add, if you think about the revenue mix, I think that was your second question. To Mike's point, this build-out in infrastructure and adoption will take time. But one way to think about it is our more traditional businesses around trading, derivatives, lending, et cetera, will grow -- the opportunity set will grow with the overall growth of the pie. So, the mix may shift for us, but we think that the opportunity set for the more recurring fee-based revenue as well as the more transactional-based can grow together, right, as the industry grows and adoption continues.

**Christopher Ferraro** (Executives):
And the last piece I'll add on that is just from an infrastructure business model perspective, which I think was part of the question. We see the traditional -- we see the financial players and institutions around the world in 2 categories or at least they pick and choose these 2 categories depending on the service needed, right? There's a -- we need to own it. own the underlying technology, own the underlying operating risk or we are okay white labeling and contracting out.
And so, what we are doing today is we are selectively partnering with some of the largest institutions who need to own certain components, think base layer custody, think maybe, like, a custody allocation engine, et cetera, to help build that, and we get paid to help build that. that increases not only their capabilities, but our portfolio of capabilities to then offer as a platform service to those companies and everyone else for the components that -- of those services that they are okay not owning and would rather contract out to create recurring revenue for us. And so, the model is getting paid both upfront to help build, but also over time, stacking a recurring revenue business for a platform service for both those customers and the long, long, long tail of middle market and lower market financial institutions who would never need to build and own their own capabilities.

**Operator** (Operator):
Our next question comes from Ben Sommers from BTIG.

**Benjamin Sommers** (Analysts):
So, kind of, build off the last one a little bit. I wanted to ask around the individual investor adoption of digital asset product offerings through Galaxy I. It seems like the TradFi institutional interest is significant, but, kind of, curious how Galaxy One could potentially contribute to the revenue mix over time.

**Christopher Ferraro** (Executives):
Yes. We haven't talked about Galaxy I in our prepared remarks or really question a lot recently. We're actually under the hood, really excited about not only what's going on there, but also the product road map. And so, our assets on platform, while still relatively small there, have grown quite substantially. We're well north of $125 million, I believe, the last number I saw there and growing fast.
And on the forward, this year was really a build baseline capabilities and ensure that our retail-facing offering had digital asset crypto-related capabilities that were on par with what's available in the market. We still got a little bit work to do on there, but that was the big lift so far this year. What we look forward to next year in 2027 actually is rolling out expanded brokerage capabilities across a number of different asset classes.
And our real focus there is not only just baseline capabilities to compete with existing platforms, but actually offer much more higher-end bespoke wealth management style access products and capabilities for high earners individuals with networks that they want to preserve and grow. And we have a really cool lineup of product road map on that front that we're really excited to start rolling out in Q1 2027. So, more to come on that, but we're -- we think the opportunity set is much broader than just offering crypto access and is going to be quite differentiated in 2027.

**Operator** (Operator):
Our next question comes from Michael Kim from Bloomberg.

**Michael Kim** (Analysts):
So, I noticed that the average annual revenue assumption for Phase II of Helios I. Just ticked down a bit from last quarter's forecast. So, just wondering if you could maybe flesh that out in terms of -- or maybe with respect to your earlier comments around supply remaining constrained and demand strengthening as well as your competitive positioning.

**Anthony Paquette** (Executives):
Yes, Michael, it's Tony. I'll address the first part of the question and then if Chris wants to hit the other. So, nothing has changed with regard to Phase II and the revenue. It's simply a clarification of the recognition under lease accounting for GAAP purposes that we just wanted to help analysts clarify for their model building. Nothing fundamentally has changed. Phase II is exactly the same.

**Operator** (Operator):
And our next question comes from Bill Papanastasiou from Chardan Capital Markets.

**Bill Papanastasiou** (Analysts):
We're hearing that long lead time item, equipment procurement is becoming increasingly harder to come by. Just quickly here, how is the team strategizing equipment procurement for its uncontracted sites and lining that up with energization time lines? Any pressure there on Helios II build-out time lines?

**Christopher Ferraro** (Executives):
Sure. So, on the procurement side, our internal mantra is be early and be deliberate, but don't get too far ahead of yourself on demand. So, it's always a delicate balance for us. Again, for us, the -- we have the lower case luxury of having a balance sheet and resources available to us to allow us to lean in where we see potential future supply chain bottlenecks. We're now becoming a large consistent buyer of a lot of the infrastructure. And so, the big suppliers, we are -- while not on the same level as the hyperscalers, we are a key customer to critical infrastructure suppliers now.
And so, we have the access and the ability to place deposits, lock up future capacity for ourselves. Like for example, for Helios II already, we've already committed approximately $230 million in deposits and purchase orders for future electrical infrastructure, mostly focused on long lead time equipment that early on, we saw the potential for some supply chain disruption. It's not -- I would not characterize supply chain for infrastructure today as something that's completely prohibiting and limiting from growth and expansion. It's available. There are also new suppliers globally that are emerging that we have traveled around the world to meet with and evaluate as to whether the equipment meets the highest standards so that we can install into our infrastructure, and we've made substantial progress on that front, too.

**Operator** (Operator):
And our final question today comes from Martin Toner from ATB Cormark Capital Markets.

**Martin Toner** (Analysts):
Mike is a very unique CEO because of his market sense. And so, I wanted to ask Mike, what he thinks of the credit market. Your customers need a lot of money or seems like, kind of, a handoff to me, and I would love to hear what Mike thinks about it and how he thinks it will be resolved and on what time line if he's willing to speculate.

**Michael Novogratz** (Executives):
Yes. Listen, it's a great question. I mean you don't have to be living under a rock, you didn't realize there was stress in the credit markets recently. And the equity markets have sold off some, but not as dramatic as the stress one might have seen in the credit markets. That's happened for a few reasons, right? This war in Iran has kept oil prices over $100. That pushed up the 10-year yield, which pushed up the credit yield and just the recognition of just how big this infrastructure build is going to be.
And so, I think partly pressure or higher rates as a base case is starting to be absorbed psychologically by the market, right? We are not going to go back any time in the short term to short-term interest rates at 1% or 2% and long-term rates below 4%, right? That -- there was a whole generation of traders and investors that started to live with that as their base case. And I think we're going back to an era where short-term rates are probably between 4% and 6%, 4% and 5% and the yield curve being more -- tending to be more steep.
And so, in some ways, this is a onetime adjustment in psychology that is coming off of what was really an era that was abnormal historically. I do think this election is going to come and go, and there's going to be a lot of readjustment for the first week or 2. And then like always, economic takeover from politics when it comes to markets. The war will -- if the war ends and oil comes down, right, if Trump attacks and we end the war or we pressure them to end the war, I mean, there are people negotiating like crazy right now to try to end the war. And you get oil going back from 100 to 60, it's going to take a tremendous amount of pressure off the fixed income markets and hence, the credit markets.
And so, Chris was saying we have the luxury of being able to wait to the turn of the first quarter, second quarter before we really need to tap credit markets. I'm thrilled with that because I know one thing, the tension never lasts forever, right? It always resolves itself. There are bullets that Scott Bessent has in his gun. We'll see if he uses them. Kevin Warsh is under -- will most likely raise rates, not the week before the election, but soon after. And at one point, you slow the economy because you have to, if that's what it takes. And so, we have indigestion the credit market. It is probably close to peak nervousness. There's not an easy path out, but I think time is going to heal this thing.
And mostly, that's going to be the reaction to the oil prices. The good news is Meta is coming out and doing a monster equity raise. Anthropic, which said they have $130 billion on their balance sheet. I think that was the number, is going to raise another $100 billion. And so, every time I see giant equity raises, I breath aid relief for the credit market, right?
You could argue is it good for the equity holders of those companies or not that they're being diluted. That's a separate discussion. But more equity, less credit is one way to think about it. And so, this last week to some degree was good for the credit markets because we saw this massive amount of equity. And I don't think the belief in what's coming in AI is going away. like if you just yesterday, 4 of the most -- to a layman absurd math problems got solved by these machines. And the breathtaking accomplishments of AI are going to start translating into medical advancements and even consumers, if you look at the consumer apps from instinct Tomo to Grok Bot, as consumers start using them, the demand for AI picks up, but also the acceptance of AI.
And so, it's going to be a politically charged issue. But like this is the transformative technology that is literally going to change the world. And in some ways, we need it to win. Like Galaxy is betting on it that it's going to win. But quite frankly, as an American, we need it to win. When I think of $41 trillion of debt, like the only way out is we have above-average growth with lower inflation, which is one of the promises of AI or at least one of the potentials of AI.
And so, one of the reasons we made this bet is because we're good patriots. But we actually believe that this really -- and listen, there's going to be a new regulatory framework that comes out sometime in the next 12 to 18 months. That meeting at the White House, which looked like it was performative, wasn't just performed. They've come out with a bunch of things that are going to slowly be or quickly be instituted to make people feel better about AI safety. But that conversation is not going away either.
We plan on being part of it, like being at the table, trying to help guide. Like I think the best AI policy is one that keeps people optimistic. And so, you might see some things that are perceived a small step backwards to go 2 steps forward. But this is -- like again, the country is making a long-term bet on AI. Galaxy is. And I think we're pretty optimistic it's going to turn out well.

**Operator** (Operator):
And with that, we'll conclude our question-and-answer session. I'd like to turn the floor back over to Mike for any closing comments.

**Michael Novogratz** (Executives):
Yes. Listen, I want to give a shout out to the Galaxy team. First of all, people have been working their tail off in all aspects of this thing. And also to our investors, nobody likes when their stock goes down or dislikes it as much as I do. We are working hard to build a company that someone whose stock markets are weighing machines. And we really hope that in 6 months, 12 months, 18 months and 36 months when we're weighed, the conclusion of the equity market is that we're worth a lot more than we are today. And so, that's our goal. I appreciate the questions and appreciate the support.

**Operator** (Operator):
And with that, we'll conclude today's conference call and presentation. We do thank you for joining. You may now disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GLXY_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Anthony Paquette｜guidance：CFO 指引 Q3 起 Phase I 首個完整季（原話："we expect Phase I to generate its first full"）
- 2026-08-05｜Anthony Paquette｜guidance：Phase I 完整季租賃收入約 8,000 萬美元、專案層級 adjusted EBITDA margin 高於 90%（90% 在下一行）（原話："quarter of leasing revenue of approximately $80 million and"）
- 2026-08-05｜Anthony Paquette｜guidance：資本支出預期隨 Helios 施工持續增加（原話："should expect CapEx to continue increasing alongside the"）
- 2026-08-05｜Christopher Ferraro｜guidance：Phase II 資料廳交付時程（原話："expect to commence Phase II data hall deliveries in the"）
- 2026-08-05｜Christopher Ferraro｜guidance：Helios I 第三階段預計 2028 年陸續上線（原話："The third and final phase of Helios I, which represents an"）
- 2026-08-05｜Christopher Ferraro｜guidance：Merlin 首期 74MW 預計 2028 年通電，附開發里程碑條件（原話："74-megawatt phase to begin energization in 2028, subject to"）
- 2026-08-05｜Christopher Ferraro｜guidance：Helios III 預期以 study load 納入 ERCOT Batch Zero（原話："Based on the completion of those milestones and the"）
- 2026-08-05｜Christopher Ferraro｜guidance：Helios IV 將走後續 ERCOT 批次、通電較晚（原話："Helios IV has not yet reached those same milestones. And as"）
- 2026-08-05｜Anthony Paquette｜margin：管理層定義資料中心 adjusted gross profit 排除代收代付營運成本（原話："center specifically, adjusted gross profit will exclude the"）
- 2026-08-05｜Anthony Paquette｜margin：說明合併損益表 leasing revenue 為直線法認列的總合約租金（原話："reflects the total contracted rent over the life of each"）
- 2026-08-05｜Anthony Paquette｜margin：Q2 GAAP 淨損與每股損失（原話："For the second quarter, we reported GAAP net loss of $85"）
- 2026-08-05｜Anthony Paquette｜margin：管理層將虧損歸因於 Treasury and Corporate 部門的調整後毛損（原話："digital asset prices during the quarter with our Treasury"）
- 2026-08-05｜Anthony Paquette｜margin：清潔電力投資稅收抵減因 Up-C 架構僅約一半進入損益表（原話："Given our Up-C corporate structure, only roughly half of"）
- 2026-08-05｜Anthony Paquette｜margin：管理層將數位資產 gross profit 成長歸因於市占提升（原話："asset prices and weaker industry activity reflects"）
- 2026-08-05｜Anthony Paquette｜capital_allocation：Phase II 以 85% LTC 發行 35 億美元 5 年期高收益擔保債（原話："offering of $3.5 billion of 5-year senior secured notes"）
- 2026-08-05｜Anthony Paquette｜capital_allocation：完成 CoreWeave 專案不需再有股權資金需求（原話："equity need expectation to complete the project for"）
- 2026-08-05｜Anthony Paquette｜capital_allocation：Phase III 未來還會有最後一筆債務融資（原話："What you likely will see happen into the future is a final"）
- 2026-08-05｜Christopher Ferraro｜capital_allocation：新站點採取先付少量資金、其餘繫於里程碑的結構（原話："These acquisitions have all been structured so that we"）
- 2026-08-05｜Anthony Paquette｜capital_allocation：季末現金與穩定幣餘額與季減幅（原話："Cash and stablecoins were $2.5 billion, down 6% from Q1,"）
- 2026-08-05｜Christopher Ferraro｜commitment：管理層表示在 Helios II 830MW 上不輕易部署資產（原話："Make no mistake, the team here is laser-focused on"）
- 2026-08-05｜Anthony Paquette｜commitment：對 GalaxyOne 表示持續投入產品建置（原話："we know building a consumer franchise takes time."）
- 2026-08-05｜Anthony Paquette｜commitment：預計下半年募集較大的 2026 年份 Galaxy Ventures 基金（原話："we expect to raise the next vintage of the Galaxy Ventures"）
- 2026-08-05｜Anthony Paquette｜commitment：behind-the-meter 發電：目前不是重點，未來可能跟進（原話："We are focused on front-of-the-meter assets."）
- 2026-08-05｜Michael Novogratz｜commitment：Novogratz 轉述 SEC 與 CFTC 主席的規則制定承諾（原話："There has been a commitment from both the SEC Chair and the"）
- 2026-08-05｜Christopher Ferraro｜risk：德州州長下令稽核，Batch Zero 分類通知延後（原話："in the industry no longer expect communication on Batch"）
- 2026-08-05｜Michael Novogratz｜risk：CLARITY 法案在休會前不太可能通過（原話："If clarity doesn't pass, it's not the end of"）
- 2026-08-05｜Anthony Paquette｜risk：管理層承認資源有限，需挑選合作夥伴（原話："We do have somewhat limited resources."）
- 2026-08-05｜Christopher Ferraro｜customer：Helios II 830MW 仍未簽約，管理層稱需耐心（原話："Furthermore, other market dynamics are at play that signal"）
- 2026-08-05｜Anthony Paquette｜customer：Helios II 通電時程為首要因素（原話："I think as I said in the remarks, the #1 factor for us in"）
- 2026-08-05｜Anthony Paquette｜customer：簽署與 BNY 的多年期協議（原話："That strategy reached an important milestone in Q2 when we"）
- 2026-08-05｜Anthony Paquette｜customer：摩根士丹利財富管理選 Galaxy 提供質押服務（原話："Morgan Stanley Wealth Management has now selected Galaxy"）
- 2026-08-05｜Anthony Paquette｜customer：管理層表示 GalaxyOne 對 markets 業務財務貢獻仍小（原話："still a very small contributor to the net financial profile"）
- 2026-08-05｜Anthony Paquette｜competition：更換 Phase II 總承包商為 HITT，管理層解釋原因（原話："We made a decision ultimately to go ahead, and it was"）
- 2026-08-05｜Anthony Paquette｜competition：機構客戶從外包轉向自建基礎設施（敘事）（原話："Increasingly, firms are moving beyond outsourcing core"）
- 2026-08-05｜Christopher Ferraro｜product：資料中心管道含 3 個新站點，總潛在電力逾 5.7GW（原話："5.7 gigawatts, providing Galaxy Power a visible development"）
- 2026-08-05｜Michael Novogratz｜product：Novogratz 說明數位資產與資料中心兩塊業務短期沒有直接整合（原話："In the short term, it's not a clear answer that there's a"）
- 2026-08-05｜Anthony Paquette｜product：貝萊德質押基金選 Galaxy 為驗證者（原話："Following BlackRock's selection of Galaxy as a validator"）

### 問答異常語氣（迴避／改口／保留）
- GLXY_Q2_2026_Earnings_Call_20260805.md｜問：Patrick Moley（Piper Sandler）：Helios II 未簽約 830MW 的租戶漏斗與卡關因素｜答法：未提供簽約進度或時間點，改談 2028 年底通電時程、關係建立與新出現的信用包裝結構
- GLXY_Q2_2026_Earnings_Call_20260805.md｜問：Mike Colonnese（H.C. Wainwright）：BNY 多快能成為實質貢獻者｜答法：未回答時間或金額，改談商業模式（建置期收費、後續分銷）與收入入帳位置
- GLXY_Q2_2026_Earnings_Call_20260805.md｜問：Chris Brendler（Rosenblatt）：GalaxyOne 近況｜答法：未給用戶數或財務數字，只提產品進度與「綠芽」，並稱仍是很小貢獻者

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

## ⑥ 條件附卡（archetype_hint='金融' 命中）：judge_addendum_archetype.md

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
{"date":"20260525","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Helios CoreWeave 15-year contract 按時 buildout，全 800MW 在 2028 H1 前 operational","columns":{"2Y 驗證點":"2026 年底 ≥ 300MW 交付（37.5% milestone）","5Y 驗證點":"2028 H1 800MW 全交付，年化 revenue $1B+ run rate","10Y 驗證點":"3.5GW full buildout 至 FY30+，年化 revenue $3B+","具體數字門檻":"2Y：2026 末 300MW；5Y：800MW 全交付 + 第二客戶簽約 300-500MW","信息來源":"Q1 2026 8-K + CoreWeave 合約披露 + project finance covenant","漂移觸發條件":"連 2 quarterly milestone 偏離 -25%+ → 削弱；連 4 quarter → 反轉"}},{"id":"H2","text":"Crypto trading + asset management 業務在新 cycle 中復甦，提供 Helios 過渡期支撐 cash flow","columns":{"2Y 驗證點":"FY27 trading + asset management combined revenue 回到 FY24 水平（$XB）","5Y 驗證點":"FY28-30 crypto cycle peak 期 trading revenue 超 FY21 peak（institutional 流入加速）","10Y 驗證點":"持續成長至 FY35","具體數字門檻":"2Y：trading rev 年化 ≥ $500M base；5Y：cycle peak rev ≥ $1B；asset management AUM ≥ $XB","信息來源":"10-Q 季度披露 + 法說會 commentary","漂移觸發條件":"連 4 季 trading + AM combined revenue YoY -20%+ → 削弱"}},{"id":"H3","text":"Helios full buildout 後 3.5GW 中扣除 CoreWeave 800MW 仍可成功找到第二 / 第三 AI 客戶，避免 single-customer concentration","columns":{"2Y 驗證點":"2028 末前簽約第二客戶 ≥ 300MW","5Y 驗證點":"FY30 前簽約 second + third customer，合計 ≥ 1.5GW","10Y 驗證點":"FY32+ Helios 多元客戶結構穩定","具體數字門檻":"2Y：第二客戶 LOI；5Y：合計 ≥ 1.5GW additional 客戶","信息來源":"Galaxy 法說會 + 業界 deal flow","漂移觸發條件":"2027 末若無第二客戶 LOI → 「Helios 僅 CoreWeave 單一客戶風險」確認，削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"CoreWeave 自身財務問題 / chapter 11 / 重組","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"CRWV 股價 + Q earnings + cash position","警戒閾值":"CRWV cash + access to capital 連 2 季減少 → 警戒；正式 restructure 公告 → 立即 thesis 重評"}},{"id":"R2","text":"Helios capex 重大 overrun 或時程延後 12+ 個月","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"Quarterly milestone reports vs original schedule + capex spending vs $1.4B 預算","警戒閾值":"連 2 季 capex 超預算 20%+ AND milestone 延後 → reduce conviction；正式 covenant breach → 立即減倉"}},{"id":"R3","text":"AI capex cycle 結構性退潮（hyperscaler over-investment correction）","columns":{"對應假設":"H1 + H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Hyperscaler capex guidance 趨勢 + GPU pricing 變化 + AI workload demand","警戒閾值":"連 4 季 hyperscaler capex guidance 累計下修 15%+ → AI infrastructure thesis 重評"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":28.65,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
