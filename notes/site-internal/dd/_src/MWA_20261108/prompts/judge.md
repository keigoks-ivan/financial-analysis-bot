你是 stock-analyst **v20 判斷 agent**，標的 MWA（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MWA","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales（GAAP）","value":376.5,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）"},"note":"未查得（本次未取得可靠共識值，不填造）"},{"id":"f_kpi1_adjusted_operating_margi","label":"Adjusted operating margin（Non-GAAP）","value":21.9,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）"},"note":"未查得（本次未取得可靠共識值，不填造）"},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":19.4,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）"},"note":"未查得（本次未取得可靠共識值，不填造）"},{"id":"f_kpi3_free_cash_flow_q4","label":"Free cash flow（Q4 單季）","value":96.7,"period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）"},"note":"未查得（本次未取得可靠共識值，不填造）"},{"id":"f_kpi5_fy2027_guidance_metering","label":"FY2027 guidance（不含 metering，FY2026 metering 銷售約 $40M）","value":"Net sales 1,440–1,470；Adj. EBITDA 378–388（中位 margin 26.3%，+110bps）","period":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04），新聞稿給 FY2027 指引","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-09-30，公告於 2026-11-04），新聞稿給 FY2027 指引","citation":"公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）；其他：capex 60–70、FCF >80% adj. net income、SG&A 228–233、利息淨支出 3–5、稅率 24–26%、D&A 48–52"},"note":"yfinance FY 營收共識 1,502.85（4 位分析師，期別標籤不確定、含 metering，不可直接比較）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mwa_gross_margin_pct","label":"MWA 毛利率","value":38.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MWA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mwa_operating_margin_pct","label":"MWA 營業利益率","value":21.54,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MWA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mwa_fcf_margin_pct","label":"MWA FCF 利潤率","value":10.07,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MWA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wts_gross_margin_pct","label":"WTS 毛利率","value":48.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WTS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wts_operating_margin_pct","label":"WTS 營業利益率","value":19.73,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WTS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wts_fcf_margin_pct","label":"WTS FCF 利潤率","value":11.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WTS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_xyl_gross_margin_pct","label":"XYL 毛利率","value":39.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XYL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_xyl_operating_margin_pct","label":"XYL 營業利益率","value":16.06,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XYL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_xyl_fcf_margin_pct","label":"XYL FCF 利潤率","value":10.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XYL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_zws_gross_margin_pct","label":"ZWS 毛利率","value":50.41,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ZWS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_zws_operating_margin_pct","label":"ZWS 營業利益率","value":22.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ZWS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_zws_fcf_margin_pct","label":"ZWS FCF 利潤率","value":21.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ZWS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bmi_gross_margin_pct","label":"BMI 毛利率","value":41.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bmi_operating_margin_pct","label":"BMI 營業利益率","value":18.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bmi_fcf_margin_pct","label":"BMI FCF 利潤率","value":16.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_sbc_gaap_fy2026","label":"SBC 占 GAAP 營業利益（FY2026 全年）","value":4.7,"period":"FY2026 全年（截至 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"FY2026 全年（截至 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）；SBC 全年 13.7M ÷ GAAP op income 290.8M（計算值）；單季 SBC 新聞稿未揭露"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":24.05,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-8.31,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":63.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.57 → 1.57）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.59 → 1.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.57,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.59,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 1.57 → 1.57（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":17.06,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.54,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝81.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":81.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.46,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝71.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":71.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":15.32,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 1.57，分子＝快照價 24.05","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.164,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-112.2,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 453.8、現金 566.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":155.5,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":3627.6,"period":"2026-11-08","unit":"USD m","basis":"市值 3739.8 ＋ 淨負債 -112.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":1502.85,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（4 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":1524.24,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（2 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.41,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 24.05 / W52 25.46 / W104 25.03 / W250 18.53 / W250 13週斜率 0.87%"},{"id":"f_ma_w52","label":"52 週均線","value":25.46,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":25.03,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":18.53,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.87,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"FY2025 10-K：閥門與消防栓市場成熟，終端用戶不易轉換品牌；鐵閘閥與消防栓主要對手為 McWane 與 American Cast Iron Pipe，僅少數競爭者。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"The competitive environment for most of Water Flow Solutions’ valve products is mature and many end users are slow to transition to brands other than their historically preferred brands.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：除北美對手外，亦面臨北美以外廠商競爭，強度受匯率、運費與貿易救濟影響。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"In addition to competition from United States and Canadian companies, we face the threat of competition from outside of North America.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"MWA 賣給全國/區域水務經銷商，關係非獨家、無長期合約；兩大經銷商合計占毛銷售約 37%（FY2025）、38%（FY2024）、35%（FY2023）。經查未見最大客戶導入第二供應商或自製的報導。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"Although we have long-standing relationships with most of our key distributors, we typically do not have long-term contracts with them, including our two largest distributors, which together accounted for approximately 37%, 38% and 35% of our gross sales in 2025, 2024 and 2023 fiscal years, respectively.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"兩大經銷商合計占毛銷售約 37%（FY2025）、38%（FY2024）、35%（FY2023），且無長期合約。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"we typically do not have long-term contracts with them, including our two largest distributors, which together accounted for approximately 37%, 38% and 35% of our gross sales in 2025, 2024 and 2023 fiscal years, respectively.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"最大客戶占毛銷售 20%（FY2025、FY2024）、18%（FY2023），應收 $56.5M；第二大客戶 17%，應收 $42.4M。","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"One customer comprised 20% of gross sales for each of the fiscal years ended September 30, 2025 and 2024, and 18% of gross sales for fiscal year ended September 30, 2023. The Company had outstanding Accounts receivable from this customer of $56.5 million and $59.1 million as of September 30, 2025 and 2024, respectively.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"MWA 2026-06-30 10-Q 列示 Moody's Ba1（穩定）、S&P BB+（正向），評等無降級。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000036/mwa-20260630.htm","excerpt":"Corporate credit rating Ba1 Ba1 BB+ BB ABL Agreement Not rated Not rated Not rated Not rated 4.0% Senior Notes Ba1 Ba1 BB+ BB Outlook Stable Stable Stable Positive","as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"MWA FY2027 consolidated net sales guidance $1,440-1,470M (excluding metering) and adjusted EBITDA $378-388M","source":"MWA 8-K FY2026 Q4 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000043/exhibit991releasefy26q4.htm","excerpt":"is introducing fiscal 2027 consolidated net sales guidance of $1,440 million to $1,470 million. This guidance excludes all metering-related financial results. In fiscal 2026, the metering-related net sales were approximately $40 million. The Company anticipates its fiscal 2027 adjusted EBITDA to be between $378 million and $388 million.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"MWA expects resilient municipal repair and replacement demand driven by aging water infrastructure, moderated by municipal budget pressure; 60-65% of FY2025 sales tied to municipal repair/replacement","source":"MWA 10-Q for quarter ended 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000036/mwa-20260630.htm","excerpt":"We estimate approximately 60% to 65% of our fiscal 2025 net sales were associated with the repair and replacement of municipal water infrastructure, approximately 25% to 30% were related to residential construction activity and approximately 10% were related to natural gas utilities","as_of":"2026-08-01","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 未列出重大訴訟；除已述訴訟外，公司認為無未決訴訟會對業務或前景造成重大不利影響，未見反壟斷調查揭露。","source":"SEC EDGAR 10-K FY2025 Item 3. Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"Other than the litigation described elsewhere in this Annual Report, we do not believe that any of our outstanding litigation would have a material adverse effect on our business or prospects.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"2026-02 投資人簡報提到鉛／銅規則改善版（LCRI）：供水系統預期自 2027-11-01 起過渡至最終 LCRI（鉛管線更換需求相關的產業監管）。","source":"Mueller Water Products 8-K 投資人簡報 2026-02","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059326000016/mwairpresentationfebruar.htm","excerpt":"submitted in 2024/2025 • Water systems expected to transition to the final Lead and Copper Rule Improvements (LCRI) starting Nov. 1, 2027, including updating inventories and preparing service line replacement plans to replace LSLs over a 10-year period Lead Service Line (LSL) Replacement Background (1) (1) U.S.","as_of":"2026-02-01","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：美國對 MWA 所有供應國及鋼、鋁、銅等原料課關稅；若再擴大或遭報復，可能須漲價並流失客戶。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"Furthermore, the Trump administration has implemented tariffs on foreign imports into the United States from all of our supplier countries, as well as on specific commodities used in our operations, such as steel, aluminum, and copper.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"MD&A：以色列製產品進口關稅壓抑毛利；Repair 與 Specialty Valve 產品線承擔多數成本；漲價動作預期大致抵銷關稅金額但稀釋毛利率。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"In response to tariffs that went into effect in the second half of fiscal 2025, we implemented additional pricing actions, which are expected to mostly offset tariff costs in dollar terms but will result in tariff-related impacts being dilutive to margins.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 預期直接關稅成本約占銷貨成本 3%，續推高通膨壓力。","source":"SEC EDGAR 10-K FY2025 Item 7 Outlook","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"In addition, higher direct tariff costs of approximately 3% of costs of goods sold are expected to continue to contribute to inflationary pressures in 2026.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"國內鑄造產能投資定位：地緣與關稅不確定下，預期國產產品需求上升。","source":"SEC EDGAR 10-K FY2025 Item 7","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"strategically position ourselves as the demand for domestic product is expected to increase given the uncertainty in the current geopolitical and tariff environment.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"經查搜尋結果，未見 MWA 被列入 BIS Entity List 或受出口管制行動之來源。","source":"WebSearch: Mueller Water Products export control OR entity list","url":null,"excerpt":null,"as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#5","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 Q3 10-Q（2026-06-30）稱 Section 232 關稅升至 50% 對進口零組件與原料（含 Krausz 修理產品）造成實質上行成本壓力，預期於 FY2026 餘期持續負面影響。","source":"SEC EDGAR 10-Q 季度 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000036/mwa-20260630.htm","excerpt":"increases on imported steel and aluminum from 25% to 50% under Section 232 of the Trade Expansion Act (“Section 232”). The increase in Section 232 tariffs to 50% has resulted in material, upward pressure on certain purchased components and raw material costs, including the Repair products we import to the U.S. that are produced by our Krausz business, which have borne most of the higher costs.","as_of":"2026-07-30","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Section 232 steel and aluminum tariffs rose to 50%, putting upward pressure on purchased components and raw material costs, mostly in Repair and Specialty Valve lines","source":"Mueller Water Products Form 10-Q (quarter ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000036/mwa-20260630.htm","excerpt":"While tariffs are adversely impacting several product lines, Repair and Specialty Valve product lines are bearing most of the higher costs. In 2025, the U.S. government announced significant changes to its trade policy, including tariff increases on imported steel and aluminum from 25% to 50% under Section 232 of the Trade Expansion Act (“Section 232”).","as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"In January 2025 the company ceased melting and casting at its legacy brass foundry and moved production to a new foundry","source":"Mueller Water Products Form 10-Q (quarter ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000036/mwa-20260630.htm","excerpt":"In January 2025, we ceased melting and casting operations at our legacy brass foundry and transitioned production to our new state-of-the-art foundry.","as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Ariel, Israel facility had production delays in 2023 after the war; the company added suppliers to mitigate","source":"Mueller Water Products Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"Our facility in Jingmen, China, manufactures and assembles specialty valve products, and our facility in Ariel, Israel, designs, manufactures, and assembles repair products and solutions.","as_of":"2025-11-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Water Flow Solutions FY26 Q4 銷售年減3.0%至$210.9M，因量減、價格部分抵銷；全年$817.5M vs $824.9M","source":"Mueller Water Products FY2026 Q4 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000043/exhibit991releasefy26q4.htm","excerpt":"Net sales for the 2026 fourth quarter decreased $6.6 million, or 3.0%, to $210.9 million","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Water Management Solutions FY26 Q4 銷售年增1.4%至$165.6M，價格帶動、量減；全年$657.5M vs $604.8M","source":"Mueller Water Products FY2026 Q4 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000043/exhibit991releasefy26q4.htm","excerpt":"Net sales for the 2026 fourth quarter increased $2.3 million, or 1.4%, to $165.6 million","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"FY27 合併營收指引$1,440–1,470M（不含約$40M的metering），調整後EBITDA $378–388M；管理層稱市政維修汰換需求具韌性、新住宅放緩","source":"Mueller Water Products FY2026 Q4 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000043/exhibit991releasefy26q4.htm","excerpt":"The Company is introducing fiscal 2027 consolidated net sales guidance of $1,440 million to $1,470 million.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"市政維修汰換需求具韌性","source":"Mueller Water Products FY2026 Q4 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000043/exhibit991releasefy26q4.htm","excerpt":"Municipal repair and replacement demand remains resilient.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"+","claim":"MWA 10-K 描述其 Echologics 非侵入式聲學漏水偵測與管況評估為關鍵競爭優勢，並以 Singer Valve 與 i2O 提供智慧水務方案（公司自身技術升級路線，非外部替代品證據）","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"We believe Water Management Solutions’ ability to offer non-invasive leak detection and pipe condition assessment services is a key competitive advantage. With our Singer Valve and i2O products, we provide a range of intelligent water solutions including pressure control valves, advanced pressure management, network analytics, event management and data logging.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子提及競爭對手若更有效運用 AI 改進營運或創造新產品，MWA 有競爭劣勢風險","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"Further, we face risks of competitive disadvantage if our competitors more effectively leverage AI to drive operational efficiencies, create new or enhanced products, services and solutions or otherwise disrupt the marketplace.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子：運輸成本高，高運輸成本可能使產品相對競爭者的類似或替代產品較不具競爭力","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"High transportation costs could make our products less competitive compared to similar or alternative products offered by competitors.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：公司主要仍賣給美加全國與區域性水務經銷商，經銷關係非排他、無長期合約，前兩大經銷商占毛銷售約37%（2025）、38%（2024）、35%（2023）；一手文件未見通路轉為直銷或D2C。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"We primarily sell to national and regional waterworks distributors in the United States and Canada. Our distributor relationships are generally non-exclusive, but we attempt to align ourselves with key distributors in the principal markets we serve.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026-11-04 公司宣布退出計量（metering）業務，客戶移轉給 ZENNER USA；預期年化調整後EBITDA利潤率增加100–140bp，主要自FY2027 Q2起，FY2027一次性費用約2,600萬美元。屬產品線／商業模式縮減，非通路改變。","source":"Mueller Water Products 8-K 新聞稿（Exhibit 99.2）／Finviz 新聞","url":"https://finviz.com/news/415881/mueller-water-products-announces-agreement-to-transition-metering-business-to-zenner-usa","excerpt":"Under the agreement, Mueller is exiting the metering business and will transition customers to ZENNER USA for replacement software and hardware to continue to fulfill our customer commitments.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FQ3 2026（2026-08-05 公布）調整後 EPS 0.50 美元，高於共識約 0.39；公司維持全年營收指引中點約 14.8 億美元（較分析師預估低約 0.6%），並上調調整後 EBITDA 指引，中點約 3.695 億美元，高於分析師預估 3.63 億。","source":"WebSearch 摘要（聚合自 Benzinga／新聞稿轉載）","url":"https://www.benzinga.com/quote/MWA/earnings-forecasts","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Tickflow 截至 2026-08-01 的共識為 Hold，3 位分析師平均目標價 30.80 美元；MarketBeat 2026-07-20 摘要為 1 賣、2 持有、2 買，共識 Hold。","source":"Tickflow forecast；MarketBeat 2026-07-20","url":"https://www.marketbeat.com/instant-alerts/mueller-water-products-nysemwa-receives-consensus-recommendation-of-hold-from-analysts-2026-07-20/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"各聚合站目標價分布不一：MarketBeat（2026-05）平均 31.25；另一 MarketBeat 頁平均 28.33（區間 27–29，4 位）；pricetargets.com 平均 31.33（高 33、低 29，3 位）；StreetInsider 個別目標價 25（Barclays）至 34（Baird）。多為 2026 年中以前資料，非 11 月最新。","source":"MarketBeat／pricetargets.com／StreetInsider 搜尋摘要","url":"https://www.pricetargets.com/NYSE/MWA","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026 年 2 月（FQ1）公司上調 FY2026 營收指引至 14.7–14.9 億（中點 +0.2 億）、調整後 EBITDA 至 3.55–3.60 億（中點 +0.1 億）；後續再上調 EBITDA 至 3.60–3.65 億，SG&A 下修至 2.41–2.45 億、有效稅率降至 21–23%。","source":"Seeking Alpha／SEC 8-K 新聞稿（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001350593/000135059326000034/exhibit991pressreleasefy26.htm","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-11-04 8-K：與 ZENNER USA 簽約，將計量（metering）業務移轉給 ZENNER，預計一次性稅前費用約 $26M，多數在 FY2027 Q1 認列；為業務退出而非收購。","source":"SEC EDGAR 8-K Item 2.05 (2026-11-04)","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059326000043/mwa-20261104.htm","excerpt":"the Company expects to record total one-time pre-tax charges of approximately $26 million, substantially all of which are expected to be recognized in fiscal 2027, with the majority expected to be recognized in the first quarter of fiscal 2027.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"10-K FY2025：Cobb County 訴訟（Hydro Gate 產品瑕疵指控），提供 $15M 和解，預期由第三方全額補償；公司認為不致重大不利。","source":"SEC EDGAR 10-K FY2025 附註","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"Hydro Gate anticipates that the Settlement Offer will be fully reimbursed by third parties upon settlement. As the settlement is probable and reasonably estimable, we have recorded a $15 million liability with a corresponding receivable","as_of":"2025-11-19","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"10-K FY2025：資安事件集體訴訟已於 2025-07-07 達成和解，總額上限 $285,000，待法院核准。","source":"SEC EDGAR 10-K FY2025 附註","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"the Company entered into a settlement agreement with the Plaintiff on July 7, 2025, to provide credit monitoring, ordinary and extraordinary losses, lost time and alternative cash payment benefits subject to an overall aggregate cap of $285,000.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"-","claim":"2026-11-04 與 ZENNER USA 簽約移轉計量業務（業務退出，非收購），預計一次性稅前費用約 $26M。","source":"SEC EDGAR 8-K Item 2.05 (2026-11-04)","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059326000043/mwa-20261104.htm","excerpt":"the Company's metering software customers are expected to transition to ZENNER, and the Company will retain its existing hardware contracts and warranty obligations","as_of":"2026-11-04","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"資安事件集體訴訟 2025-07-07 和解，上限 $285,000，待法院核准；Cobb County 訴訟 $15M 和解預期由第三方補償。","source":"SEC EDGAR 10-K FY2025 附註","url":"https://www.sec.gov/Archives/edgar/data/1350593/000135059325000066/mwa-20250930.htm","excerpt":"subject to an overall aggregate cap of $285,000. The settlement agreement is subject to and is awaiting Court approval.","as_of":"2025-11-19","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MWA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.24,"operating_margin_pct":21.54,"fcf_margin_pct":10.07,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MWA","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WTS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.87,"operating_margin_pct":19.73,"fcf_margin_pct":11.55,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WTS","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"XYL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.79,"operating_margin_pct":16.06,"fcf_margin_pct":10.17,"rd_intensity_pct":2.55},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.XYL","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ZWS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.41,"operating_margin_pct":22.52,"fcf_margin_pct":21.19,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ZWS","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"BMI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":41.64,"operating_margin_pct":18.76,"fcf_margin_pct":16.16,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMI","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MWA"},"financial_history":{"ticker":"MWA","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-09-30","revenue":1247400000.0,"revenue_yoy_pct":null,"gross_margin_pct":29.2,"operating_margin_pct":10.07,"net_income":76600000.0,"diluted_eps":0.48,"free_cash_flow":-2400000.0,"fcf_margin_pct":-0.19,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-09-30","revenue":1275700000.0,"revenue_yoy_pct":2.27,"gross_margin_pct":29.75,"operating_margin_pct":10.79,"net_income":85500000.0,"diluted_eps":0.55,"free_cash_flow":61400000.0,"fcf_margin_pct":4.81,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-09-30","revenue":1314700000.0,"revenue_yoy_pct":3.06,"gross_margin_pct":34.91,"operating_margin_pct":16.26,"net_income":115900000.0,"diluted_eps":0.74,"free_cash_flow":191400000.0,"fcf_margin_pct":14.56,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-09-30","revenue":1429700000.0,"revenue_yoy_pct":8.75,"gross_margin_pct":36.14,"operating_margin_pct":18.84,"net_income":191700000.0,"diluted_eps":1.22,"free_cash_flow":172000000.0,"fcf_margin_pct":12.03,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-09-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MWA/MWA_Q4_2026_Earnings_Call_20261105.md）

# Q4 2026 Earnings Call
**Mueller Water Products, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good morning, and thank you for standing by. [Operator Instructions] Today's conference is being recorded. If you have any objections, you may disconnect at this time. It is now my pleasure to turn the call over to Whit Kincaid.

**Whit Kincaid** (Executives):
Good morning, everyone. Thank you for joining Mueller Water Products' Fourth Quarter and Fiscal 2026 Conference Call. Yesterday afternoon, we issued our press release reporting results for the quarter and year ended September 30, 2026. The release is available on our website, muellerwaterproducts.com.
Joining me this morning are Paul McAndrew, our President and Chief Executive Officer; and Mike Morgan, our Executive Vice President of Finance and future Chief Financial Officer. After our prepared remarks, we will take questions about the information covered on the call. [Operator Instructions] Today's call is being recorded and webcast live on the Internet. The accompanying slides are available on our website and include our forward-looking statements and non-GAAP disclosures.
Please turn to Slide 2, which identifies the non-GAAP financial measures referenced in our press release, slides and remarks. It explains why we believe these measures are useful to investors. Reconciliations of non-GAAP measures to GAAP measures are included in the supplemental information in our press release and on our website.
Slide 3 addresses forward-looking statements made on this call. This slide includes cautionary information identifying important factors that could cause actual results to differ materially from those included in forward-looking statements. Please review Slides 2 and 3 in their entirety. Unless otherwise noted, all references to years and quarters on this call refer to our fiscal year, which ends September 30.
A replay of this morning's call will be available for 30 days at 1 (800) 819-5743. The archived webcast and corresponding slides will be available for at least 90 days on the Investor Relations section of our website.
I'll now turn the call over to Paul.

**Paul McAndrew** (Executives):
Thanks, Whit. Good morning, everyone. Thank you for joining our Fourth Quarter and Fiscal 2026 Earnings Call. 2026 was an excellent year for Mueller. We delivered record results and made meaningful progress in strengthening the business. Full-year net sales increased 3.2% to approximately $1.5 billion, supported by enhanced commercial execution and resilient end-market demand. Higher pricing was partially offset by lower volumes.
Adjusted EBITDA grew 14.1% year-over-year to a record $372 million. Adjusted EBITDA margin expanded 240 basis points to 25.2%, bringing our cumulative expansion over the past 3 years to 940 basis points. Adjusted net income per share reached a record $1.57, an increase of approximately 20% year-over-year.
Free cash flow was strong in the fourth quarter and for the full year, totaling $207 million for the year. This cash generation enabled us to return $74 million to shareholders through dividends and share repurchases. We recently announced a $300 million increase in our share repurchase authorization and a 14.3% increase in our quarterly dividend to $0.08 per share. These actions reflect our confidence in Mueller's strategy and our ability to continue investing in the business.
Three things drove our progress: first, operational improvements through greater productivity and disciplined cost management, including SG&A productivity; second, commercial execution through improved service levels, strategic pricing and strong growth in specialty valves; third, a stronger organization built around leadership accountability. Together, these efforts have made Mueller a more profitable business and positioned us well for fiscal 2027.
These results reflect the hard work and dedication of our employees across Mueller. I want to thank our teams for their commitment to our customers and to making the company stronger. I am proud of what we have accomplished together.
I also want to highlight an important announcement about our metering business. We have entered into an agreement to transition the business, which operates through our Mueller Systems subsidiary to ZENNER USA, who is part of the Minol-ZENNER Group. Following a comprehensive portfolio review, we believe that exiting this business will improve earnings quality, simplify operations, strengthen returns on invested capital and allow us to direct resources towards areas with stronger growth potential. 
This transition is another decisive step in strengthening Mueller. Metering requires scale and technology investments that a more specialized company is better positioned to provide. ZENNER is an established global metering company with extensive industry experience and compatible technology. We believe these capabilities will support a smooth transition for our customers. This decision reinforces our focus on building a stronger, more profitable Mueller through disciplined execution of our strategy, supported by the Mueller Operating System.
As we expand margins, accelerate growth and create long-term shareholder value, we will begin the transition immediately and work closely with our customers and suppliers to maintain service continuity and ongoing support. We expect most of the transition to occur in 2027, although some activity and associated costs could extend beyond this year. The timing of customers' migration to the ZENNER platform will be the main source of variability in the phased transition.
In connection with the agreement, we expect to incur approximately $26 million of onetime expenses in fiscal 2027. These primarily relate to the outstanding warranty liability, operating and customer service costs, transaction-related costs, and severance. The transition impacts will be adjusted as appropriate in our key financial metrics. The onetime and ongoing transition activities will be included in net sales, cost of sales, and strategic reorganization and other charges. The majority of the expenses will be incurred during the first quarter, with most of the remaining expenses incurred prior to the end of the year. Finally, the financial impacts and benefits will occur in the Water Management Solutions segment.
For 2026, we generated approximately $40 million in metering-related sales with a negative adjusted EBITDA margin. We expect the transaction to support adjusted EBITDA margin expansion with a 100 to 140 basis points annualized benefit, primarily beginning in the second quarter of fiscal 2027. At the midpoint of the range, this would be approximately $8 million favorable to EBITDA on an annualized basis. Taking the onetime expenses and annualized benefit into account, we believe the cash return on investment of completing this transition is very attractive relative to other opportunities.
I would like to welcome Mike Morgan, who joined Mueller on October 28 and will become our Chief Financial Officer on or about November 19 following the filing of our annual report. He most recently served as Chief Financial Officer of Indicor and previously held senior finance roles at Labcorp and Timken. Mike is a proven industrial finance leader with an extensive track record working with management teams and boards to improve performance and drive profitable growth. He'll recap our fourth quarter and full year performance, and I'll provide more details on our annual guidance for 2027.

**Michael Morgan** (Executives):
Thanks, Paul. Good morning, everyone. It's an exciting time to join Mueller. Over the coming months, I look forward to meeting many of you and working with Paul and the leadership team to strengthen execution, support disciplined investment and advance Mueller's strategy for profitable growth.
Fourth quarter net sales decreased 1.1% versus the prior year to $376.5 million, with Water Management Solutions up 1.4% and Water Flow Solutions down 3.0%. The year-over-year decrease in consolidated net sales was primarily driven by lower volumes, partially offset by higher pricing across most product lines. In the quarter, gross profit of $139.3 million decreased 0.5% year-over-year, and gross margin expanded 20 basis points to 37.0%.
We incurred $600,000 of Decatur legacy brass foundry costs in the Water Flow Solutions segment. Excluding these costs, our gross margin was 37.2%. This was down 100 basis points compared with the prior year, excluding the $5.6 million warranty charge at Water Management Solutions in the prior year. The decrease was primarily driven by lower volumes, product mix and inflationary pressures, including the impact of higher Section 232 tariffs, partially offset by higher pricing and manufacturing performance.
For the full year, we achieved a record gross margin of 37.9%, an increase of 180 basis points compared with the prior year. Excluding the impact of tariff refunds, portfolio optimization costs and Decatur foundry closure cost, adjusted gross margin was 37.8%. Gross margin expanded 100 basis points compared with the prior year, excluding onetime items in both periods. This increase was primarily driven by manufacturing performance and price/cost.
Total SG&A expenses for the quarter of $57.3 million decreased $9.4 million year-over-year, primarily due to lower incentive-based compensation, favorable personnel-related costs resulting from productivity actions, and reduced foreign currency headwinds, partially offset by inflationary pressures. We incurred $8.9 million of strategic reorganization and other charges, which have been excluded from adjusted results. These costs primarily relate to closure of our legacy brass foundry in Decatur, Illinois and severance. Strategic reorganization and other charges and the brass foundry closure costs and gross profit have been excluded from adjusted results for the fourth quarter.
For the quarter, adjusted EBITDA of $95.5 million increased 4.0% year-over-year. Adjusted EBITDA margin expanded 130 basis points versus the prior year to 25.4%, setting a new fourth quarter record. Our strong margin performance was driven by higher pricing, lower SG&A expenses and manufacturing performance, partially offset by inflationary pressures, lower volumes, product mix and tariffs. For the full year, adjusted EBITDA increased 14.1% year-over-year to a record $372.2 million, representing 25.2% of net sales. For the quarter, adjusted net income per share was $0.38, which was flat compared with prior year.
Our fourth quarter effective income tax rate was 28.0% compared with 23.4% in the prior year quarter. The fourth quarter income tax rate was within our expectations as our annual guidance for the full year effective tax rate was 21% to 23%. For the full year, the effective income tax rate was 22.7% as compared with 24.6% in the prior year. The lower effective tax rate for the full year was primarily due to a onetime tax benefit resulting from the recognition of a loss on a foreign subsidiary investment. This benefit was in the third quarter and equates to a onetime cash tax benefit of $0.06 per share.
Full year adjusted net income per share increased 19.8% year-over-year to a record $1.57 per share. As a reminder, full year earnings per share included a combined $0.09 benefit from tariff refunds and the onetime tax item associated with the i2O business exit.
Turning now to segment performance, starting with Water Flow Solutions. Fourth quarter net sales decreased 3.0% year-over-year to $210.9 million, primarily due to lower iron gate valve and service brass volumes. These declines were partially offset by higher pricing across most product lines and increased specialty valve volumes. Adjusted EBITDA increased 7.0% year-over-year to $67.1 million, and adjusted EBITDA margin improved 300 basis points versus prior year to 31.8%. This improvement was driven by manufacturing performance, higher pricing and lower SG&A expenses, which more than offset lower volumes, product mix, inflationary pressures and tariffs. For the full year, adjusted EBITDA margin expanded 430 basis points year-over-year to 33.0%, a record for the segment.
Moving on to Water Management Solutions. Fourth quarter net sales increased 1.4% year-over-year to $165.6 million, driven by higher pricing across most product lines and volume growth in repair and natural gas distribution products. These were partially offset by lower volumes of applications and hydrants.
Adjusted EBITDA decreased 8.4% year-over-year to $41.2 million, and adjusted EBITDA margin of 24.9% decreased 270 basis points. The decrease was due to lower volumes, tariffs and inflationary pressures, partially offset by higher pricing and lower SG&A expenses, including reduced foreign currency headwinds. For the full year, adjusted EBITDA margin was 24.6%, slightly below the prior year.
Moving on to cash flow. For the year, free cash flow increased $35.3 million to $207.3 million and was 84% of adjusted net income. Free cash flow exceeded our expectations, primarily due to favorable working capital and lower capital expenditures. Net cash provided by operating activities for the year increased by $43.6 million year-over-year to $262.9 million, primarily driven by higher net income and lower cash taxes, offset by changes in working capital. 
We increased our capital expenditures by 17.5% year-over-year to $55.6 million or 3.8% of net sales, primarily driven by investments in our iron foundries. We ended the year with $566 million in cash and cash equivalents and $454 million in total debt. Our balance sheet remains exceptionally strong, providing significant flexibility for organic investment and strategic growth opportunities. We have no debt maturities until June 2029. Our senior notes total $450 million at a favorable fixed interest rate of 4%, and we had no borrowings under our ABL facility.
Total year-end liquidity was $731 million, including $165 million available under the ABL facility. This positions us to reinvest in the business, return cash to shareholders, and pursue acquisitions in existing and adjacent markets that create value.
I'll now turn it back to Paul to discuss the outlook for 2027.

**Paul McAndrew** (Executives):
Thanks, Mike. I'll now review our fiscal 2027 outlook, which excludes all metering-related financial results. We expect consolidated net sales between $1.44 billion and $1.47 billion. In fiscal 2026, the metering-related sales were approximately $40 million. Excluding the portfolio optimization headwind, our net sales would range between flat and approximately 2.5% higher year-over-year. For price realization, we are assuming a low single-digit to mid-single-digit benefit for the year. This includes carryover pricing and new price increases sometime in Q2, which we have not yet announced. The year-over-year volume headwinds are mainly driven by the prior year hydrant backlog benefit at Water Management Solutions.
Excluding this impact, we anticipate consolidated volumes will be flat at the midpoint. This includes double-digit specialty valve growth and benefits from commercial initiatives. These benefits will be offset by slower new residential construction activity and cautious purchasing behavior from municipalities in terms of repair and replacement.
We expect our adjusted EBITDA to range from $378 million to $388 million. At the midpoint of our guidance range, adjusted EBITDA achieves a 26.3% margin for the year, reflecting a 110 basis point year-over-year improvement. This would be a 150 basis point year-over-year expansion, excluding the prior year tariff refund benefit. The expansion is driven by the metering and i2O portfolio optimization actions, higher pricing, manufacturing performance, and SG&A productivity, partially offset by inflationary pressures, lower volumes and product mix.
Similar to the prior year, we expect our second half net sales and adjusted EBITDA margin to be higher than the first half of the year, with the first quarter lower than the second quarter. This is driven primarily by the seasonality of our business, where construction activity ramps up in the spring and the timing of the benefits from the portfolio optimization and operational improvements.
For the Water Flow Solutions segment, we expect net sales growth in the low single-digit to mid-single-digit range, supported by higher pricing and volume growth from specialty valves, partially offset by lower volumes of iron gate valves and service brass products. We anticipate adjusted EBITDA margin will be up slightly versus the prior year, excluding tariff refunds. Benefits from higher pricing and specialty valve volume growth will be partially offset by lower volumes of iron gate valves and service brass and inflationary pressures.
For the Water Management Solutions segment, we anticipate net sales to decrease in the high single-digit range, reflecting lower sales associated with the metering portfolio optimization and the prior year hydrant backlog benefit. We expect strong adjusted EBITDA margin expansion, even with the lower sales, primarily driven by higher pricing, lower SG&A related to the portfolio optimization benefits and manufacturing performance, partially offset by lower volume of hydrants, inflationary pressures and higher tariffs.
We expect total SG&A expenses of $228 million to $233 million, reflecting portfolio optimization benefits, including the metering business transition. We expect an effective tax rate of 24% to 26%, reflecting a more normalized rate after prior year onetime tax benefit. We expect free cash flow to exceed 80% of adjusted net income, including higher capital expenditures of $60 million to $70 million. We will continue investing in growth, operational efficiencies and domestic capacity with a focus on our iron foundries.
Before opening up for Q&A, I want to provide a few closing comments. We delivered strong results in an uncertain operating environment by focusing on customer service, disciplined execution and investments in capabilities that support long-term value creation.
Our fiscal 2027 priorities are straightforward: protect the strength of our core business, improve operational returns and invest in the best opportunities to create value. Our balance sheet gives us capacity to invest as we pursue above-market sales growth and continued margin expansion.
While we remain mindful of market uncertainty, we enter the year with a clear agenda and confidence in our ability to take another step forward in margin performance. The Mueller Operating System supports these priorities with tools, processes and management disciplines that strengthen execution, accountability and continuous improvement across the company. 
This quarter provides further evidence that the system is taking hold. I want to thank our employees worldwide for their extraordinary commitment to our customers and communities. They are the reason for our success and why Mueller has been a trusted partner for more than a century.
That concludes our comments. Operator, please open the call up for questions.

**Operator** (Operator):
[Operator Instructions]
Brian Lee with Goldman Sachs.

**Keshav Choudhary** (Analysts):
This is Keshav Choudhary on for Brian Lee. So firstly, your 2027 sales guidance implies growth excluding the metering business. Can you maybe walk us through what you're assuming for residential construction versus municipal repair and replacement, and specialty valves within that outlook?

**Paul McAndrew** (Executives):
Our sales guidance, excluding the metering portfolio optimization, is 1.5%. We are expecting residential construction to continue to decline at low single digits on top of double-digit decline in FY '26. We anticipate municipality spending to be cautious as they have the inflationary pressures around their budgets. Where we are expecting to see double-digit growth and where we've seen growth at that level over the last few years is around our specialty valve business as we continue to move this company to a broader flow control platform.

**Keshav Choudhary** (Analysts):
That was helpful. And then just maybe on the price/cost side of things, you previously expected to remain price/cost positive despite lower price realization. How are you thinking about pricing relative to inflation and maybe Section 232 tariff costs as you enter '27?

**Michael Morgan** (Executives):
Yes, the company -- this is Mike Morgan, by the way. The company has strong brands, and we continue to expect to be able to deliver price increases year-over-year. So from a price/cost perspective, we would expect to be dollar positive, and in terms of margin, it's in the neutral range in terms of price/cost.

**Paul McAndrew** (Executives):
As a reminder on our tariffs, the Section 232 impacted our steel products from Israel when the IEEPA tariffs came to an end. But right now we have all that priced in our assumptions.

**Operator** (Operator):
[Operator Instructions] Our next caller is Jeffrey with RBC Capital Markets.

**Jeffrey Reive** (Analysts):
Just want to say congrats to Mike, and it's nice to have you on the call.

**Michael Morgan** (Executives):
Thank you very much. Appreciate it.

**Jeffrey Reive** (Analysts):
Yes. And just I want to follow up on that pricing question. So the slides indicate, I think, it's low single-digit to mid-single-digit realization for next year, but this is including, I guess, a new price increase that has not been announced. This is a change from the historical practice that used to just not embed the price increase until you announced it. Just can you help us understand what gives you confidence to include that now, the ability to capture it?

**Paul McAndrew** (Executives):
Yes, thanks, Jeff. I think twofold. Look, our price confidence is high based on the brands of our business and our commercial execution and operational execution with our customers. So this is why we've given a range. I think previously, it was a little confusing to everyone, so we wanted to make it clear this is what is baked into our guidance right now. And in terms of that price increase, it would be in -- later in our Q2 as per we do on an annualized basis.

**Jeffrey Reive** (Analysts):
Got it. Okay. I appreciate that. I think it makes sense. And maybe just moving to the metering exit. Can you just help us understand the economics of the agreement? Is it that Mueller's not receiving any consideration and you just have to basically take a $26 million charge and you hand over the customers? And is there any, I guess, incremental liability that can persist?

**Paul McAndrew** (Executives):
First of all, Jeff, I want to kind of remind everyone on the metering business. The sales have been declining at a 10% CAGR over the last 4, 5 years with negative EBITDA margin. And it's really about how the team and myself have looked at the portfolio, and removing what is a subscale and competitively disadvantaged business from our portfolio allows us to really focus on where we believe we are transitioning this company to from a growth opportunities perspective.
But to answer your question directly, the annualized benefit when you back in at the midpoint is $8 million of EBITDA improvement. And the onetime charges are predominantly around a warranty, both software and hardware services to fulfill customer commitments on an ongoing basis, along with the transactional costs. Just a reminder, we do have a manufacturing facility related to this business. 
So what we will be doing ongoing is transitioning customers to ZENNER. We will continue to support them from a customer warranty perspective ongoing. And the goal here is to work closely with a much larger water metering company who wants to make progress in North America and is backed by a global metering manufacturer and transition our customers across smoothly to a much better position for them.

**Jeffrey Reive** (Analysts):
All makes sense. And if I can just sneak in one more, when you look across your portfolio today, are there other low-margin products or technologies that you're evaluating for divestiture?

**Paul McAndrew** (Executives):
Look, part of the Mueller Operating System in that simplification is looking constantly at the portfolio, and I take that down to a SKU level, not just a product portfolio. We believe we are positioned well now. We still believe the leak detection business is a key part of our technology going forward. How that integrates into our industrial products is critical. We know municipalities have a need to address non-revenue water, and we believe that technology is a key part of how that fits in.

**Operator** (Operator):
Our next caller is Bryan Blair with Oppenheimer.

**Bryan Blair** (Analysts):
Mike, welcome to the call.

**Michael Morgan** (Executives):
Thank you.

**Bryan Blair** (Analysts):
Hoping we could level set on hydrant backlog normalization. Sorry if I missed this detail. But what was the impact in Q4? I assume that would start to phase in. And then we have enough information to back into the segment and consolidated impact for fiscal '27 overall. But how should we think about the cadence throughout the year?

**Paul McAndrew** (Executives):
Yes, Bryan, as we kind of think about the hydrant backlog, it was minimal in Q4 as an impact as we kind of caught up on that backlog and have seen that normalization with the channel. The overall impact for the year is around 2% from a sales perspective as a headwind that we'll move in to FY '27 for a comp comparison.

**Bryan Blair** (Analysts):
Okay. Understood. And a bigger picture, I guess, medium-term follow-up. It looks like EBITDA margin will exceed 26% this year, so over 1,000 basis points expansion since fiscal '23. How should we think about runway from here? Are you willing to offer a medium-term margin target? And I guess at risk of leading the witness here, would that start with a 3?

**Paul McAndrew** (Executives):
Yes, great question. And part of Mike coming onboard now is to help us kind of put that narrative together from a longer-term perspective. We're really pleased with the organization, Bryan, 940 basis points in 3 years, and at the midpoint of our guidance would be 1,150 in 4 years. So we've really transformed the company. The next step now, as I said, is how do we really take the specialty valve business, which plays in the plant work, both potable and wastewater, larger pipe distribution, water and flood control, along with importantly the growing industrial segment where we are seeing a lot of traction in our investments. I know a relatively small number to start from but definitely seeing a lot of high-growth opportunities in our industrial applications. And we believe we're a company that has deep expertise and engineering skills in flow control and how we leverage that and change the company from that perspective.

**Michael Morgan** (Executives):
The only thing I'd add to that is that the Mueller Operating System is just taking hold, so there's room to run.

**Operator** (Operator):
We are showing no further questions. I'll turn the call back over to you for closing comments.

**Paul McAndrew** (Executives):
Thank you, operator. Thanks to everyone who joined our call today. We're excited about the progress we made in 2026, leading continued margin improvement and strong cash generation. We enter fiscal 2027 focused on strengthening our core business using the Mueller Operating System and portfolio optimization to simplify operations, enhance execution, and improve returns. We remain mindful of market uncertainty, and we will stay focused on what we can control. Once again, I want to thank our dedicated team members for their commitment to our customers and communities. We look forward to speaking with you again with our with our first quarter results when they're announced in early February. 
And with that, operator, please conclude the call.

**Operator** (Operator):
Thank you, sir. This concludes today's conference. You may disconnect at this time, and have a great rest of your day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MWA_Q3_2026_Earnings_Call_20260806.md
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：CFO 將 FY2026 淨銷售成長財測收窄至 2.8%–3.5%（原話："we are narrowing our consolidated net sales growth guidance to a range of 2.8%"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：CFO 上調全年 adjusted EBITDA 財測至 $367–372 百萬（原話："we are raising our annual adjusted EBITDA guidance to a new range of"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：財測中點對應 adjusted EBITDA margin 25.1%（原話："adjusted EBITDA margin of 25.1%, which would represent another annual record for the company"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：SG&A 財測下修至 $241–245 百萬；稅率財測降至 21%–23%（原話："we are lowering our effective tax rate guidance to between 21% and 23%"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：重申 capex $60–65 百萬與自由現金流轉換率超過 70% 的展望（原話："continue to expect our free cash flow conversion"）
- 2026-08-06｜Paul McAndrew (CEO)｜guidance：CEO 指出已連續第三季上調全年 adjusted EBITDA 財測（原話："I'm pleased for the third"）
- 2026-08-06｜Paul McAndrew (CEO)｜guidance：CEO 說明收窄銷售財測的原因：訂單出貨預期、住宅建設放緩、去年 Q4 關稅調價的基期（原話："We're also lapping tariff price"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：WFS 第四季 adjusted EBITDA 預期高於去年同期，但較 Q3 季減（原話："For the WFS segment, we are expecting adjusted EBITDA to be above prior year due to gross margin"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：WMS 第四季利潤率預期低於去年同期與前一季，因消防栓積壓訂單正常化（原話："For WMS, we're expecting to see lower margins versus the prior year and sequentially."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：第四季價格實現略低，因基期含去年 Q4 起的關稅調價；仍預期價格成本為正（原話："We have been price/cost positive and continue to expect that, that"）
- 2026-08-06｜Paul McAndrew (CEO)｜guidance：FY2027 財測要到下次財報才給（原話："We don't give our guidance for 2027 until the next earnings call."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：Q3 毛利率 39.4%，年增 110bp，含關稅退款與 i2O 退出成本（原話："gross margin expanding 110 basis points to 39.4%."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：排除前期關稅退款與投資組合優化成本後，調整後毛利率僅比去年 38.3% 高約 30bp（原話："adjusted gross margin was approximately 30 basis points higher than the prior year's gross margin of 38.3%,"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：Q3 adjusted EBITDA $107.4M，margin 27.1%，年增 440bp，驅動為調價、關稅退款與 SG&A（原話："Adjusted EBITDA margin expanded 440 basis points year-over-year to a record 27.1%."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：關稅退款對 Q3 合併貢獻 150bp，WFS 約 140bp、WMS 約 170bp（原話："we had 150 basis point benefit overall for the tariff"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：Q3 稅率 15.7%，含 i2O 退出的一次性稅務利益，約貢獻每股 $0.06（原話："approximately $0.06 per diluted share during the quarter."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：WMS 淨銷售年增 10.3%、adjusted EBITDA margin 年增 650bp 至 28.1%（原話："expanded 650 basis points to a record 28.1% compared with 21.6% in the prior year period."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：WFS 淨銷售年減 0.6%，margin 34.1% 對去年 31%（原話："Net sales were $215.3 million, declining"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：Q3 營收成長主因為調價，量略減（原話："driven primarily by higher pricing across most product lines,"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜risk：IEEPA 關稅退款被更高的 Section 232 關稅取代（影響 Krausz），且不預期再有退款（原話："And we do not expect to have any further tariff refunds."）
- 2026-08-06｜Paul McAndrew (CEO)｜risk：CEO 結語提到需求、關稅與通膨的外部環境不確定性升高，必要時採取行動（原話："We will stay focused"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜risk：CFO 預期第四季新住宅建設更弱，市政維修汰換仍具韌性（原話："While we anticipate softer new residential construction activity during the fourth"）
- 2026-08-06｜Paul McAndrew (CEO)｜risk：聯邦資金退場影響：聯邦占市政投資不到 5%，未來 1–3 年預期無重大變化（原話："we don't see any meaningful change then from the federal funding impact."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜risk：營運資金因庫存投資、通膨與關稅仍偏高（原話："While working capital remains elevated due to inventory investments, inflation and tariffs,"）
- 2026-08-06｜Paul McAndrew (CEO)｜product：specialty valves 占積壓訂單多數，為近年成長最快類別（原話："So specialty valve makes up the majority of our backlog then."）
- 2026-08-06｜Paul McAndrew (CEO)｜product：已推出消防栓更新系統，客戶試用回饋正面，內含漏水檢測功能（原話："We continue to get very positive customer feedback from"）
- 2026-08-06｜Paul McAndrew (CEO)｜product：完成 i2O 北美以外壓力監測業務出售給 GWF AG（原話："we completed the exit of the i2O pressure monitoring business outside of North"）
- 2026-08-06｜Paul McAndrew (CEO)｜customer：資料中心相關工業用水 specialty valves 為成長最快之一，但規模相對小（原話："It's relatively small in the overall size of the business for us, Jeff."）
- 2026-08-06｜Paul McAndrew (CEO)｜customer：資料中心通路為經銷加投資團隊取得核准製造商名單（AML），開始看到進展（原話："We sell through distribution."）
- 2026-08-06｜Paul McAndrew (CEO)｜competition：管理層稱品牌強、定價權佳，有能力抵銷通膨或關稅成本（原話："we have very strong brands and very good pricing power."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜capital_allocation：期末現金 $495M、總債務 $453M，2029 年 6 月前無到期債務（原話："We ended the quarter with $495 million of cash and cash equivalents and $453 million of total debt."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜capital_allocation：前九個月自由現金流 $110.6M，占調整後淨利 59%；capex 前九個月 $43.6M（去年 $32.8M），投入鑄造廠（原話："free cash flow increased $7.6 million to"）
- 2026-08-06｜Paul McAndrew (CEO)｜capital_allocation：本季透過股息與回購回饋股東約 $21M（原話："returning approximately $21 million to shareholders through our quarterly dividend"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜capital_allocation：管理層稱流動性可支應有機投資並尋求有吸引力的收購機會（原話："positioning us well to execute our strategic priorities and pursue attractive"）
- 2026-08-06｜Paul McAndrew (CEO)｜commitment：管理層列出優先事項：高於市場的銷售成長、持續擴大利潤率、紀律性資本配置（原話："drive above-market sales growth, continued expanding margins and maintain disciplined capital"）
- 2026-08-06｜Paul McAndrew (CEO)｜commitment：管理層稱將在有機投資、目標性收購與股東回饋間紀律性配置資本（原話："Finally, we will remain disciplined in allocating capital across organic investments,"）
- 2026-08-06｜Paul McAndrew (CEO)｜commitment：CEO 稱將以 Mueller Operating System 降低複雜度、擴大利潤率並產生現金（原話："reduce complexity, improve business processes, expand margins and generate cash to fund growth"）
- 2026-08-06｜Paul McAndrew (CEO)｜commitment：CEO 稱住宅建設不會永遠低迷，市政與商業策略可抵銷住宅疲弱，住宅回升將是順風（原話："residential construction cannot stay depressed"）

### 問答異常語氣（迴避／改口／保留）
- MWA_Q3_2026_Earnings_Call_20260806.md｜問：FY27 若住宅持續疲弱，市政與 specialty valves 能否支撐成長？（Goldman 代表）｜答法：未回答 FY27 數字，稱 2027 財測下次財報才給；以『相信可抵銷』與住宅終將反彈的定性說法回應
- MWA_Q3_2026_Earnings_Call_20260806.md｜問：資料中心業務目前規模多大？（RBC）｜答法：未給數字，僅答『relatively small』
- MWA_Q3_2026_Earnings_Call_20260806.md｜問：消防栓更新系統的商業化進度與預期營收貢獻？（RBC）｜答法：只談客戶回饋與產品特性，未回答營收貢獻

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
{"date":"20260524","verdict":"A","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"美國水基建結構性需求 + IIJA 政策順風延續：fire hydrant + iron gate valve duopoly 維持 + IIJA 9/30/26 reauthorization 成功或部分延續","columns":{"2Y 驗證點":"FY27 全年 sales ≥ $1.55B (+5%)；IIJA reauthorization 至少 50% 規模延續","5Y 驗證點":"FY30 sales ~$1.85-2.0B（含 IIJA 完整週期 + 鉛水管 $15B 完成）","10Y 驗證點":"FY35 sales ~$2.4-2.7B（含後續政策週期 + 老化基建剛性需求）","具體數字門檻":"FY27 sales ≥ $1.55B；IIJA 9/30/26 reauthorization ≥ 50% 原規模","信息來源":"5/5/26 Q2 法說、IIJA funding tracker","漂移觸發條件":"連 2 季 sales YoY &lt; 2% → 削弱；連 3 季 &lt; 0% → 反轉"}},{"id":"H2","text":"Adj EBITDA margin 結構性擴張至 26-28%：brass foundry 整合完成 + EchoShore mix shift + pricing power 維持","columns":{"2Y 驗證點":"FY27 全年 adj EBITDA margin ≥ 25%；FY27 adj EBITDA ≥ $390M","5Y 驗證點":"FY30 adj EBITDA margin ≥ 26%；EBITDA ≥ $480M","10Y 驗證點":"FY35 adj EBITDA margin ≥ 27%；EBITDA ≥ $650M","具體數字門檻":"FY27 adj EBITDA margin ≥ 25%；EchoShore subscription 年化 &gt; $100M","信息來源":"FY26 Q2 法說（margin 25.3% +210bps）","漂移觸發條件":"連 2 季 adj EBITDA margin &lt; 23% → 削弱；連 3 季 &lt; 21% → 反轉"}},{"id":"H3","text":"Fwd PE 從 17x 維持或微升至 20-22x：基本面持續驗證 + IIJA 政策確定性提升 + smart water 占比擴大支撐 multiple expansion","columns":{"2Y 驗證點":"FY27 末 trailing PE ~20-22x（股價適度上漲 + EPS 兌現）","5Y 驗證點":"FY30 trailing PE 20x（成長放緩至 8-10% CAGR 對應）","10Y 驗證點":"FY35 PE 18-20x（mature 公用事業相關等級）","具體數字門檻":"FY27 末 trailing PE ≥ 20x 且 EBITDA margin ≥ 25%","信息來源":"歷史對標 WTS 2018-2023 倍數軌跡","漂移觸發條件":"5Y 假設，連 4 季 TTM 偏離 ≥ 5% 才削弱（QC-35）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Brass / 銅 / 鋼 tariff outpace pricing power — Trump 2.0 升級 232 條款 + raw material 成本 +20%，MWA 無法完全 pass through，GM 從 36% 跌至 33%","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"季度 GM YoY 連 2 季 -1pp+；管理層 guide 提到 tariff pass-through 困難","警戒閾值":"連 2 季 GM &lt; 34% 或 adj EBITDA margin &lt; 23%"}},{"id":"R2","text":"IIJA 9/30/26 reauthorization 失敗或大幅縮水 — Trump 2.0 政府優先 defense / oil & gas，FY27-28 sales 從 +5% 降至 -2%","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"9/30/2026 reauthorization 公告；FY27 sales YoY 連 2 季 &lt; 1%","警戒閾值":"reauthorization &lt; 50% 原規模 或 sales 連 2 季 &lt; 0%"}},{"id":"R3","text":"競爭格局蠶食 — McWane / American Cast Iron 在 fire hydrant 取得單一大都市 design win，MWA 市佔從 45% 跌至 40%","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"單一大都市 spec 變化公告；MWA 季報市佔提到「losses」","警戒閾值":"主要市佔指標 -3pp 或 management 法說承認「losing market share」"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"🟢","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":25.31,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
