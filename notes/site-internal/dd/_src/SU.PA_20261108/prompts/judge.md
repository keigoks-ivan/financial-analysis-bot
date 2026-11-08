你是 stock-analyst **v20 判斷 agent**，標的 SU.PA（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SU.PA","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SU.PA_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SU.PA_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_q3","label":"Revenue（Q3，營收）","value":11460,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-16）","unit":"€ million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-16）","citation":"公司 Q3 2026 營收新聞稿（Rueil-Malmaison, 2026-10-16），https://www.webdisclosure.com/press-release/third-quarter-revenues-2026-odiihfxJLgs"},"note":"有機成長 +16.9% 對分析師預期 13.8%（來源：Quartr Q3 2026 summary 經 web_search，未核對原始共識）"},{"id":"f_kpi1_revenue_h1","label":"Revenue（H1，營收）","value":21.2,"period":"H1 2026（半年報，2026-07-30 公告）","unit":"€ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"H1 2026（半年報，2026-07-30 公告）","citation":"公司 H1 2026 新聞稿（2026-07-30），經 web_search 摘要（emr-online／optionfinance），非直接讀原稿"},"note":"查無"},{"id":"f_kpi2_adjusted_ebita_non_gaap","label":"Adjusted EBITA（Non-GAAP 營業利益）與利益率","value":19.3,"period":"H1 2026（半年報，2026-07-30 公告）；Q3 無單季數字","unit":"% margin（Adj. EBITA €4.1bn，有機 +22%，利益率有機 +120bps）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"H1 2026（半年報，2026-07-30 公告）；Q3 無單季數字","citation":"公司 H1 2026 新聞稿（2026-07-30），經 web_search 摘要，非直接讀原稿"},"note":"查無"},{"id":"f_kpi4_net_income","label":"Net income（淨利）","value":2.5,"period":"H1 2026（半年報，2026-07-30 公告）","unit":"€ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"H1 2026（半年報，2026-07-30 公告）","citation":"公司 H1 2026 新聞稿，經 web_search 摘要"},"note":"查無"},{"id":"f_kpi5_2026_q3","label":"2026 全年指引（Q3 後上修）","value":"營收有機 +12%～+14%；Adj. EBITA 有機 +18%～+21%；利益率有機 +100～+120bps，隱含約 19.7%～19.9%","period":"Q3 2026（公告於 2026-10-16）","unit":"organic","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（公告於 2026-10-16）","citation":"公司 Q3 2026 營收新聞稿，https://www.webdisclosure.com/press-release/third-quarter-revenues-2026-odiihfxJLgs"},"note":"查無"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-16","period":"2026-10-16","unit":"date","basis":"距今 15 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-16"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":11.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abbn_sw_gross_margin_pct","label":"ABBN.SW 毛利率","value":40.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abbn_sw_operating_margin_pct","label":"ABBN.SW 營業利益率","value":17.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_abbn_sw_fcf_margin_pct","label":"ABBN.SW FCF 利潤率","value":13.29,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lr_pa_gross_margin_pct","label":"LR.PA 毛利率","value":49.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LR.PA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lr_pa_operating_margin_pct","label":"LR.PA 營業利益率","value":19.11,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LR.PA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_lr_pa_fcf_margin_pct","label":"LR.PA FCF 利潤率","value":13.51,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LR.PA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_sie_de_gross_margin_pct","label":"SIE.DE 毛利率","value":39.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIE.DE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sie_de_operating_margin_pct","label":"SIE.DE 營業利益率","value":12.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIE.DE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sie_de_fcf_margin_pct","label":"SIE.DE FCF 利潤率","value":14.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIE.DE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_free_cash_flow","label":"Free cash flow（自由現金流）","value":1.6,"period":"H1 2026（半年報，2026-07-30 公告）","unit":"€ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"H1 2026（半年報，2026-07-30 公告）","citation":"公司 H1 2026 新聞稿，經 web_search 摘要（connaissancedesenergies／AFP）：較去年同期增逾三倍，部分因去年有法國法律罰款"},"note":"查無"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":228.65,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-14.81,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":32.85,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":10.37,"period":"2026-11-08","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-08","citation":"yfinance earnings_estimate"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":12.59,"period":"2026-11-08","unit":"USD/share","basis":"yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-08","citation":"yfinance earnings_estimate"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":27.48,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝57.6","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":57.6,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.2,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝81.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":81.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.58,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝97.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":97.1,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.837,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":16291.0,"period":"2026-11-08","unit":"EUR m","basis":"yfinance 最新一季：總債務 20809.0、現金 4518.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":587.71,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":150671.89,"period":"2026-11-08","unit":"EUR m","basis":"市值 134380.89 ＋ 淨負債 16291.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":45342.69,"period":"2026-11-08","unit":"EUR m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":50495.77,"period":"2026-11-08","unit":"EUR m","basis":"yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.32,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 228.65 / W52 259.25 / W104 242.47 / W250 193.61 / W250 13週斜率 0.72%"},{"id":"f_ma_w52","label":"52 週均線","value":259.25,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":242.47,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":193.61,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.72,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Dell'Oro 1Q 2025：Schneider 與 Vertiv 在全球資料中心實體基礎設施份額幾乎並列，差距僅約 0.1 個百分點（搜尋摘要轉述，未核原文）","source":"Dell'Oro Group, Data center physical infrastructure grew 17 percent y/y in 1Q 2025 driven by AI buildout","url":"https://www.delloro.com/news/data-center-physical-infrastructure-grew-17-percent-y-y-in-1q-2025-driven-by-ai-buildout/","excerpt":null,"as_of":"2025-06-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Bernstein 研究：投資人曾質疑 Schneider 在資料中心電力設備流失份額；Bernstein 認為其銷售與訂單與市場同步成長，3 年銷售 CAGR 與 Vertiv 相當（搜尋摘要轉述，未核原文）","source":"發現報告 fxbaogao，伯恩斯坦：施耐德：數據中心增長對標分析","url":"https://www.fxbaogao.com/detail/5463043","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Schneider 2026 Q3 營收年增 18%、資料中心設備銷售翻倍以上，並上調 2026 年目標（dpa 報導摘要，未核原文）","source":"channelpartner.de，Rechenzentren-Boom lässt Schneider Electric Jahresausblick anheben","url":"https://www.channelpartner.de/article/4236308/rechenzentren-boom-lasst-schneider-electric-jahresausblick-anheben.html","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Digital Realty 與 Schneider 簽 US$373m 供應協議（UPS、低壓開關櫃、預製 skid），Digital Realty 維持多供應商結構","source":"Data Centre Magazine: Schneider and Digital Realty: US$373m for Data Centre Demand","url":"https://datacentremagazine.com/news/schneider-and-digital-realty-us-373m-for-data-centre-demand","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"電氣設備經銷商約占 Schneider 總銷售 50%、型錄產品銷售 70%","source":"Schneider Electric distributors partner page","url":"https://se.com/eg/en/partners/distributors","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Moody's 於 2025-06-20 將 Schneider 評等由 A3 升至 A2，展望穩定（發行人自身信用，非客戶信用；搜尋未見 2026 評等異動）","source":"investing.com: Moody's upgrades Schneider Electric to A2, outlook stable","url":"https://ng.investing.com/news/stock-market-news/moodys-upgrades-schneider-electric-to-a2-outlook-stable-93CH-1975019","excerpt":null,"as_of":"2025-06-20","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026 group revenue about €11.46bn, organic growth 16.9% vs 13.8% consensus; FY2026 outlook raised; CEO cites triple-digit data center demand growth and increasing visibility into 2027 and 2028; record backlog reported.","source":"Idéal Investisseur / vermoegenszentrum.ch / placera.se Q3 2026 coverage","url":"https://www.ideal-investisseur.fr/en/stock-news/schneider-electric-revenue-up-16-9-organically-in-third-quarter-adjusted-ebita-target-raised/27273.html","excerpt":null,"as_of":"2026-10-16","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Capacity additions underway in India: Kolkata capex raised to ₹184 crore targeting 250,000 MV units/yr; Vadodara switchgear plant at ~90% utilization to add 6,000 panels to 8,000 capacity.","source":"sahi.com; machinist.in","url":"https://www.sahi.com/news/schneider-electric-hikes-kolkata-capex-to-184-crores-to-boost-output-to-250-000-units-4010-PE1_COR","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Group Q3 2026 results: revenue up 17% organically, guidance raised, record backlog","source":"vermoegenszentrum.ch","url":"https://www.vermoegenszentrum.ch/en/stock-exchange-and-markets/news/schneider-ups-guidance-quarterly-revenue-jumps-17","excerpt":"demonstrated \"the strength of our value proposition across end-markets and geographies.\" CEO Blum calls Data Centers \"a key growth driver as we continue to execute on our backlog while seeing triple-digit demand growth in the quarter, providing increasing visibility into 2027 and 2028.\" Says demand remains healthy across all four end-markets, leading to a record backlog at quarter-end.","as_of":"2026-10-16","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"法國競爭管理局2024-10-29裁定 Schneider 與經銷商 Rexel、Sonepar 間2012-12至2018-09的轉售價格安排違規，Schneider 被罰2.07億歐元（四家合計4.7億歐元）；Schneider 表示不同意並保留上訴權；搜尋未見2026年上訴結果","source":"Bloomberg Law: Schneider Among Firms Fined €470 Million in French Cartel Case","url":"https://news.bloomberglaw.com/antitrust/schneider-among-firms-fined-470-million-in-french-cartel-case","excerpt":null,"as_of":"2024-10-30","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Schneider 以約12億歐元現金公開收購 Shelly Group，需完成要約並取得常規監管核准，預計2027年Q1前完成；為併購審查，非反壟斷調查","source":"Debevoise: Debevoise Advises Schneider Electric in Its €1.2 Billion Voluntary Public Takeover Offer for Shelly Group","url":"https://www.debevoise.com/news/2026/10/debevoise-advises-schneider-electric-in-its","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Schneider FY2025 results (Feb 2026): CFO Maxson guided 2026 import-tariff impact (incl. US) relative to the EUR160m incremental 2025 impact; reports conflict on the multiple","source":"Reuters via itiger: Schneider Electric Exceeds Profit Expectations as Data Center Demand Counters Weak Dollar Impact","url":"https://www.itiger.com/news/1168500841","excerpt":"Maxson noted that the impact of import tariffs, including those in the United States, would be \"roughly half\" the €160 million incremental impact disclosed for 2025.","as_of":"2026-02-26","retrieved_at":"20261108","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"中國為施耐德第二大市場，2026年4月高管訪談稱已在中國39年、工程師逾2,900人。","source":"The Star (Xinhua interview) Interview: China emerges as engine of global industrial innovation, says Schneider senior executive","url":"https://www.thestar.com.my/news/world/2026/04/24/interview-china-emerges-as-engine-of-global-industrial-innovation-says-schneider-senior-executive","excerpt":null,"as_of":"2026-04-24","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"施耐德披露供應鏈依賴與營運持續為風險，電子零組件（晶片）為主要限制；以多區域採購與替代料件驗證因應，疫情以來投入逾1億美元強化區域供應鏈韌性（該文件為2022年前後）。","source":"Schneider Electric Universal Registration Document / press (se.relayto.com)","url":"https://se.relayto.com/e/universal-registration-document-ubzjtntbgejjt/hgblZajY264","excerpt":"Ensuring supply categories are supported by multi-region sourcing.","as_of":"2022-03-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 營收年增 17.9% 至 €11.46bn（有機 +16.9%），資料中心需求翻倍以上；全年有機成長指引上調至 12–14%（原 10–13%）","source":"Sharecast, Schneider Electric Q3 results","url":"https://www.sharecast.com/scroll_4/news/international-companies/schneider-electric-schneider-electric-q3-results-data-centre-demand-ai-infrastructure-schneider-electric-revenue-energy-management-schneider-electric-profit-forecast-industrial-automation--23870164.html","excerpt":null,"as_of":"2026-10-23","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Energy Management 段 Q3 2026 有機成長 18.8%（€9.62bn），主要由資料中心帶動；北美約占 40% 營收、成長 19.9%，中國及東亞成長 26.1%","source":"getquin / Yellow.com 轉述 Q3 2026 結果","url":"https://yellow.com/news/ai-data-centers-schneider-record-quarter","excerpt":null,"as_of":"2026-10-23","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Q2 2026 摘要：四大終端市場需求健康、期末訂單創高；管理層聚焦毛利、定價與工業生產力。分析師質疑資料中心三位數成長是否見頂","source":"Quartr, Schneider Electric Q2 2026 earnings summary","url":"https://quartr.com/events/schneider-electric-s-e-su-q2-2026_3gmCZZyS","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Uptime Institute 分析指固態變壓器（SST）可把中壓交流直接轉為 400/480V AC 或 800V DC，部分設計可能不再需要 sidecar（Schneider 現行 800VDC 方案採 sidecar）；SST 仍在開發與產業化階段","source":"Uptime Institute intelligence report","url":"https://intelligence.uptimeinstitute.com/pdf-download/node/154174","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Navitas 與 EPFL 於 APEC 2026 展示 250kW SST，用於 800V DC 資料中心架構","source":"Electronic Design","url":"https://www.electronicdesign.com:443/technologies/power/product/55371996/electronic-design-novel-solid-state-transformer-supports-800-v-dc-power-in-ai-data-centers","excerpt":"Novel Solid-State Transformer Supports 800-V DC Power in AI Data Centers","as_of":"2026-04-20","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Schneider 2026-10 在 PTC 收購計畫中提到以配銷通路擴展工業軟體銷售","source":"Distribution Strategy: Schneider Electric Cites Distribution Channels in $22.6 Billion PTC Acquisition Plan","url":"https://distributionstrategy.com/2026/10/schneider-electric-cites-distribution-channels-in-22-6-billion-ptc-acquisition-plan/","excerpt":"Distribution Events Chicago Thought Leadership and Software for Wholesale Change Agents Search Subscribe Distribution Industry News Schneider Electric Cites Distribution Channels in $22.6 Billion PTC Acquisition Plan","as_of":"2026-10-09","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Schneider 授權 Tradeling（MENA B2B 數位平台）為 Lauritz Knudsen 電氣與部分工業自動化產品配銷商，線上線下混合模式","source":"Channel Post MEA: Schneider Electric to Distribute its Electrical and Industrial Automation Products on the Tradeling Platform","url":"https://channelpostmea.com/?p=120190","excerpt":"Tradeling is now authorized to distribute a comprehensive portfolio of Lauritz Knudsen (LK)-branded electrical products alongside select Industrial Automation (IA) offerings from Schneider Electric, via its unified digital platform and retail presence. The partnership introduces an innovative hybrid route-to-market that combines the reach and convenience of online procurement with the","as_of":"2026-03-13","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Schneider 於 Q3 2026 財報上調 FY26 指引：營收有機成長 12-14%（原 10-13%），調整後 EBITA 有機成長 18-21%（原 14-19%）；Q3 營收 11.46bn 有機 +16.9%","source":"Vermoegenszentrum: Schneider ups guidance as quarterly revenue jumps 17%","url":"https://www.vermoegenszentrum.ch/en/stock-exchange-and-markets/news/schneider-ups-guidance-quarterly-revenue-jumps-17","excerpt":"It now expects adjusted earnings before interest and taxes growth between 18% and 21%, up from 14% to 19% before, alongside organic revenue growth of 12% to 14%, up from between 10% and 13%.","as_of":"2026-10-30","retrieved_at":"20261108","affects":["valuation","triggers","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價共識：stockanalysis 引 S&P Global 23 位分析師均價 €300.78，區間 €250-340","source":"StockAnalysis SU forecast","url":"https://stockanalysis.com/quote/epa/SU/forecast/","excerpt":null,"as_of":"2026-06-19","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Schneider 於 2026-10-05 宣布以約 226 億美元現金收購 PTC（隱含 EV 237 億美元），以約 €6B 增資加 €16-17B 新債融資，預期年成本綜效 €250M","source":"La Télé / vermoegenszentrum.ch 搜尋摘要","url":"https://latele.ch/articles/schneider-electric-acquiert-ptc-pour-22-6-milliards-de-dollars","excerpt":null,"as_of":"2026-10-05","retrieved_at":"20261108","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-30 Schneider 同意以 31 億美元現金收購 Cognite，併入 AVEVA；需監管核准","source":"GDELT Cloud 搜尋摘要","url":"https://gdeltcloud.com/events/schneider-electric-to-buy-cognite-for-31-billion--cameoplus_ae1428f6","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Chile SERNAC 公告 Schneider SYBTU 電池模組安全警示（2024-12 至 2026-09 銷售），內部電池模組可能故障","source":"SERNAC","url":"https://www.sernac.cl/portal/619/w3-article-89192.html","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-10-05 宣布以約 226 億美元現金收購 PTC，增資約 €6B＋新債 €16-17B","source":"La Télé","url":"https://latele.ch/articles/schneider-electric-acquiert-ptc-pour-22-6-milliards-de-dollars","excerpt":null,"as_of":"2026-10-05","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2026-06-30 同意以 31 億美元現金收購 Cognite","source":"GDELT Cloud","url":"https://gdeltcloud.com/events/schneider-electric-to-buy-cognite-for-31-billion--cameoplus_ae1428f6","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"Chile SERNAC 公告 SYBTU 電池模組安全警示（2024-12 至 2026-09 銷售）","source":"SERNAC","url":"https://www.sernac.cl/portal/619/w3-article-89192.html","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 33 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SU.PA","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SU.PA"},"is_subject":true,"note":"quarterly_income_stmt 無資料"},{"name":"ETN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.05,"operating_margin_pct":17.32,"fcf_margin_pct":11.87,"rd_intensity_pct":2.75},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ABBN.SW","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":40.12,"operating_margin_pct":17.6,"fcf_margin_pct":13.29,"rd_intensity_pct":3.86},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"LR.PA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.66,"operating_margin_pct":19.11,"fcf_margin_pct":13.51,"rd_intensity_pct":4.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LR.PA","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"SIE.DE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.36,"operating_margin_pct":12.98,"fcf_margin_pct":14.61,"rd_intensity_pct":8.31},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIE.DE","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"SU.PA"},"financial_history":{"ticker":"SU.PA","currency":"EUR","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":34176000000.0,"revenue_yoy_pct":null,"gross_margin_pct":40.6,"operating_margin_pct":16.27,"net_income":3477000000.0,"diluted_eps":6.15,"free_cash_flow":3261000000.0,"fcf_margin_pct":9.54,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":35902000000.0,"revenue_yoy_pct":5.05,"gross_margin_pct":41.81,"operating_margin_pct":16.61,"net_income":4003000000.0,"diluted_eps":7.07,"free_cash_flow":4542000000.0,"fcf_margin_pct":12.65,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":38153000000.0,"revenue_yoy_pct":6.27,"gross_margin_pct":42.64,"operating_margin_pct":17.22,"net_income":4269000000.0,"diluted_eps":7.61001,"free_cash_flow":4161000000.0,"fcf_margin_pct":10.91,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":40152000000.0,"revenue_yoy_pct":5.24,"gross_margin_pct":42.08,"operating_margin_pct":17.46,"net_income":4163000000.0,"diluted_eps":7.33,"free_cash_flow":4588000000.0,"fcf_margin_pct":11.43,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SU.PA/SU.PA_2025_Earnings_Call_20260226.md）

# 2025 Earnings Call
**Schneider Electric S.E.** | Earnings Calls | 2026-02-26

**Operator** (Operator):
Welcome to the Schneider Electric's Full Year 2025 Results with Olivier Blum, Chief Executive Officer; Hilary Maxson, Chief Financial Officer; and Nathan Fast, Head of Investor Relations. [Operator Instructions]. 
I'd like to inform all parties that today's conference is being recorded. If you have any objections, you may disconnect at this time. 
I will now hand it over to you, Mr. Nathan Fast.

**Nathan Fast** (Executives):
Good. Good morning, everyone, and welcome to our full year 2025 results presentation and webcast. I'm joined in Paris today by our CEO, Olivier; and our CFO, Hilary. For the agenda, you already have the slides available. We'll go through them now and then make sure to have enough time for Q&A. As always, I want to remind everyone about the disclaimer on Page 2. 
And with that, Olivier, I hand it over to you.

**Olivier Pascal Blum** (Executives):
Thank you very much, Nathan. Extremely happy to be with all of you today. Look, more than 15 months in the job, the first time I'm doing really this earnings call with you for the full year '25. And I'm extremely excited to be with you to report on what happened in '25 and even more important, what we see for the future. 
As you know, with the management team, we did spend a lot of time in '25 to define the next cycle. We were with many of you during our Capital Market Day. And we launched the new mission of Schneider Electric, which is to be your energy technology partner, to be the company which will be at the convergence of electrification, automation, digitalization in every single industry, to drive efficiency and sustainability for all. That's what we call at Schneider Electric, advancing energy tech to the next level. And of course, I'm going to come back on that. 
The point I want to make here, it has really received a very, very good feedback. We got a very good feedback from the market, from our business analysts, from our customers, from our employees, from all our partners. So that's really exciting for us to enter '26 with this new positioning, which is giving a lot of inspiration for all our stakeholders. 
So now let's turn to the most important part, of course, of this call, which are our results. I'm pleased to report a very strong Q4 revenues growth at 10.7%, EUR 11 billion. And even more important for me, it's really the acceleration of the 2 businesses, the acceleration of Energy Management, but the acceleration again in Industrial Automation in Q4 with a growth of 8%. 
If you go look at the full year results, that's an important milestone for Schneider Electric. For the first time, we have exceeded EUR 40 billion in terms of revenue, with a 9% organic growth. So that's, as you can imagine, an important milestone for a company. And even more important is the acceleration that we have seen in our 2 business. I was just talking about Industrial Automation. We told you with Hilary a year ago that we will turn positive for Industrial Automation in '25. We did it, and we delivered 7% growth in H2, which as a result, has helped us to achieve 3% growth for Industrial Automation. As you know, Energy Management has been really the driving force from a growth standpoint for the past years, and it continue again to be the case in '25 with a growth slightly above 10%. 
So all in all, again, a great year from a top line standpoint, both businesses driving good contribution to the growth of the company and an important milestone, EUR 40 billion. 
When you go a bit deeper in all our achievements, we are pleased to report that we have achieved a margin expansion of 50 bps, which is in line with the target we set up for us at the beginning of the year, which translates in an adjusted EBITA growth of 12.3%, which is again within our guidance of 10% to 15%. Extremely important milestone also for Schneider Electric, free cash flow of EUR 4.6 billion with a conversion rate slightly above 110%, which show again the strong financial health of the company overall. We are pleased to report that we are going to distribute a dividend of EUR 4.2 per share, again, in line with our progressive dividend policy, which has been the case for the past 16 years. And our TSR has grown by 89% for the past 3 years. 
So all those financials show really the solidity of Schneider Electric strategy, but even more the solidity of our execution. And as you know, it's equally important for me and the team that we always look at our digital metrics, which are translated inside the digital flywheel. It has been an important transformation for Schneider Electric in the past cycle. It will continue in the future. And the digital flywheel is giving us really the illustration of the execution of our portfolio strategy transformation. 
So we reached EUR 25 billion of our turnover with digital flywheel, which represents 62% of our overall revenue. And pleased to report that it has achieved a growth of 15% last year. We continue to grow very fast on all the aspects of the digital flywheel, but very excited to see that we are now close to 20% of our total portfolio in services and software. And last but not the least, it has been an important focus for us in the past year, not only the acquisition of AVEVA, but the transformation of AVEVA, the acquisition of OSI. And last year, we have achieved an outstanding performance with 12% growth in ARR for AVEVA. 
It's also important to mention that '25 was the last year of our sustainability program, the one we launched 5 years ago. You know that we have this culture at Schneider since 20 years to launch every 3 to 5 years, a new program where we set up an ambition on where we want to take the company. And we are pleased to report that we have achieved overall our goal. I'm not going to go through all the metrics, but that's very, very important, and I'll talk later about -- when we speak about '26. 
The only thing I'd like to mention is when you look at all these metrics, if I just highlight some of them, extremely pleased to see that with the portfolio of Schneider, we have helped to save and avoid 862 million tonnes of CO2, which is tremendous since we created that initiative in 2018. You will see later that we'll keep going in the next chapter, but that show how the impact of the business of Schneider Electric can support all our customers everywhere in the world. And we have embarked not only our customer, but our partner, our supplier. Our supplier have also achieved their goals. So we divided by 2 the CO2 emission of our suppliers that were part of that program. 
And we continue to have a very strong focus on access to clean energy to many people who don't have access energy in the world. And we have achieved this milestone, which was super important for us, 50 million plus. Actually, we have exceeded reaching 61 million. And of course, all those achievements have been recognized multiple times in the past year. It's always great to be a leader in that domain. 
So if we wrap up '25 in short, as I said, a record year in terms of revenue, crossing EUR 40 billion, all-time high level in terms of backlog. We'll come back to that with Hilary. Extremely strong performance in adjusted net income and free cash flow and acceleration of the demand and profitability in H2, which is what we told you with Hilary when we were together in July. 
What is very important for me, and we told you that during our Capital Market Day, we are accelerating the transformation of the company. We have a plan. We are accelerating the transformation of the portfolio, making Schneider Electric the company which will advance energy tech to the next level. We are going to the next level to -- of our digital portfolio, leveraging AI and bringing energy and industrial intelligence. 
We have reinforced our multi-hub strategy in a world which is very fragmented. We do believe that our regional model brings a lot of advantage. We have reinforced in particular, in India for the international market with the acquisition of L&T last year, the completion, I should say, of the acquisition. 
And last but not the least, we spent a lot of time with the team last year to simplify the operating model to make sure we can generate more efficiency and create even faster execution. 
So now if I turn to '26. I'm not going to talk about the long term today. It was done during the CMD. But if I recap what we told you in London in December: We have 3 megatrends in front of us that have been the main driver of Schneider Electric growth in the past year: The evolution of the new energy landscape, electrification of usage everywhere in the world; digitalization going to next level with AI; and of course, a world which is more and more multipolar, and we don't believe it's going to stop. So for us, what is very important is to make sure we can leverage and accelerate really everything we do at Schneider Electric to make the most of those 3 trends. And of course, what we see, and I'm sure you see it as well, all those 3 trends are accelerating at the same time at a speed which is unprecedented, which impact, of course, all our end markets. 
But speaking about the end market, it's fairly positive for Schneider Electric. And we like always to go back to those end market growth and to tell you how we see the market. We continue to see a double-digit opportunity plus in data center and network, solid growth on buildings and industry, and we'll say a little bit more with Hilary also on that one. And we continue to see infrastructure growing fairly fast between 5% and 7%. What you see as a result of the past cycle, we continue to be a very, very balanced company in terms of exposure. We'll talk about geography, but balanced in terms of end market, having our 3 largest market contributing all to 1/3 of the revenue of Schneider Electric and infrastructure step-by-step going also to the next level with close to 15% of our revenue. 
So what's next for '26? We are basically going to execute our plan, our strategic plan, the one we present to you, which is really to advance energy tech to the next level of intelligence. We are going always to follow those 3 important transformation, which we have launched internally. We call that inside Schneider, our company program. This is a vehicle we are using to align all the entities of Schneider Electric everywhere in the world. For me, what is very important is not only to define the North Star, advancing energy tech, defining those strategic priorities but equally and even more important is how we align our teams everywhere in the world to make sure we execute faster the strategy of Schneider Electric. 
So talking about Energy & Industrial Intelligence, we want to reinforce our energy, our technology leadership. We've presented in detail our strategy in December, but I want to recap what we told you. We have built a huge portfolio in the past, which is extremely differentiated, starting by our legacy product business, but going to the next level of Edge Control, starting to do more and more in digital and software and digital services everywhere in our portfolio. 
What makes Schneider Electric very, very different at the end of the day? We are combining a unique expertise in different domains. Those domains are the building domain, the power and IT domain and the industrial automation domain. What we want -- we don't want those domains to innovate in parallel universe. We want to create a unified customer experience for our customer. Let's make it simple. Every time we sell solution to our customer, we want to keep it simple for our customers to commission the asset, to be able to leverage all the software, to create a unique user experience. It means that, for instance, you need to have a digital platform, which are the same, and we need to create hub, which are the same. 
So for us, it's not only about creating the largest portfolio in our industry in those domains, is to make sure we make it simple, easy for our customers to use all those offers of Schneider Electric. And what we want to do even more in the next cycle is to do it through their full life cycle. Schneider was known 10, 15 years ago as a company which was more at the CapEx stage when we built. We've moved big time in the past 5 years to make sure we are also at the design level. We can help our customers to design, to simulate, to create digital twin for their asset. And of course, when we have installed our solution, what we want to do even more through digital is how we can help them to operate efficiently, how we can help them to maintain efficiently, to extract data that will help them to manage the obsolescence of their asset, for instance. So all in all, this is what you see on this slide, which is the strategy of Schneider, I think. 
And what are we doing differently in the next -- in this cycle? Now we've reached a level where most of our assets are connected. Again, keep in mind the digital flywheel, going step by step to 70% of the digital flywheel. So it's about extracting all those data at all layer of our digital stack, extracting external data, federating, structuring those data in the data cube to make sure, thanks to AI, we can amplify what we give to our customer and deliver more intelligence. So it's about building the foundational model in AI, in energy and industry that will create more value for our customers in the future. 
And it's not something that we are dreaming to do in 5, 10 years from now. It's something we do already. If you take just one example of the data center, which is a place where we have invested, as you know, a lot in the past years. We are, of course, in the middle, as you can see, present at the build stage historically. We have reinforced our portfolio, for instance, with the acquisition of Motivair in liquid cooling. But what is equally important is being able to work with NVIDIA, with our customer, the large hyperscaler on how you can design and simulate, how you can work in the universe of NVIDIA, on how we'll behave digital and electrical infrastructure in the future based on the next generation of GPU that NVIDIA will launch in the future. And then we can move to a stage where we are working with our customers to design their own AI factory. We can build, we can execute with them. And we can also extract data at the end of the cycle to make sure we give more to those customers. 
So that's really a typical illustration of what we mean going to the next level of energy intelligence, unique customer experience, leveraging all the portfolio of Schneider and being able to do it through the portfolio of -- through the full life cycle of our customer. 
Now we have multiple proof points and other example we are doing. We are launching, for instance, EcoStruxure Foresight Operation, which is basically the convergence of power and building management in one software amplify with AI that can give a lot of opportunity for our customers to improve the efficiency of our building. And I'm not going to cover all the examples, but we have also what we presented to you in November -- in December, what we are doing in Industrial Automation with EAE, EcoStruxure Automation Expert, which is taking automation to the next level. 
So all in all, just as a recap, we are investing a lot in R&D. We are growing progressively to the next level of our journey in R&D with 7% approximately of our turnover. And having always in mind those end targets, which is keeping on increasing the part of our portfolio, which will be more digital, more than 70% by 2030, accelerating everything we do in software and services, so going step by step to 25% of our total revenue. And all of that helping us to multiply by 2 our recurring revenue as part of the turnover of Schneider. 
The second chapter, which is very, very important for me, and I'm passionate by technology. I strongly believe in innovation. I strongly believe that what will make Schneider Electric very different. But I'm equally passionate on how we are going to differentiate in front of our customer. You know it, but we have decided to go to the next level of the regionalization of Schneider Electric. So it's basically how we structure the company in terms of innovation, in terms of supply, but also in terms of sales and making sure that we are creating 4 regional loop: in North America; Europe; China, East Asia; and Southeast Asia and International to create agility and speed. 
So what does this mean in simple terms? You identify needs in one of those regions. You can speak to R&D people who are very, very close to you. You can speak to the supply chain people, and you can execute projects very, very, very fast. And you don't need always to go back to the top of the company. Now it doesn't mean that we want to cut Schneider Electric in 4 pieces. All of that is supported by a global governance where we define very clearly where we want to go in terms of R&D. For instance, what are the platform we want to develop, what are the choice we want to make in terms of electronic. Also the way we want to design our supply chain. But when this global framework has been defined, we want to empower our 4 regions to go much faster. 
And what we are doing also in terms of operating model evolution is how we go to the next level of engagement with our global customer, which, as you know, will represent a growing part of our sales. When we go, for instance, to cloud and service providers to utilities in all the segments, we are going to next level also of engagement with our global customer. 
So on this slide, you have a couple of, again, of proof points of what we are doing to make it happen. I'm just going to give you a few examples. We want to have 90% of our sales to be manufactured in each region. Manufactured means both what we buy from outside, but also the cost -- the labor cost that we have for manufacturing. So for us, it's important that we keep investing in all the regions. I said it, we've completed the acquisition of Lauritz Knudsen in India, which creates a very, very strong India hub to support the international market. 
We continue to invest in the U.S., in North America, for North America, especially to support the growth of our data center business, both in low voltage UPS, but also in liquid cooling with the acquisition of Motivair. Talking about Motivair, we have decided to open a new factory in India. Actually, we announced last week to accelerate the expansion of Motivair outside of North America. And we continue to leverage, for instance, China as one very important hub for us in terms of power electronics but also localizing offer like GVXL to make sure we are more competitive in the Chinese market. And we continue also to invest in Europe, new factory we are launching in Macon and taking our joint venture, Schneider eStar to the next level for electrical vehicle. 
So the last pillar of that transformation is operational excellence. Also extremely important for me. We've been very, very vocal with Hilary and the management team in December that we want to innovate in technology. We want to accelerate the growth of the company, but all of that has to translate in a very strong operating margin, strong return for our shareholders. And that's why we decided we need to accelerate all our plan when it comes to cost competitiveness and scalability. 
Cost competitiveness on one side because I want to make sure we always stay competitive in everything we do, the design of our product, the cost of our product, the cost of our solution for our customer, how we do a better job to collaborate with our supplier to deliver innovation, cost and time to market, which is very important for me. And having a very strong machine where we deliver strong industrial productivity every year. 
At the same time, I want Schneider Electric to be extremely scalable. We just said it, EUR 40 billion, huge milestone for a person like me who joined the company no more than 32 million -- 32 years, which was, I think, EUR 5 billion at that point of time. I mean it's just an impressive milestone. But if we want to go to the next level of our ambition, 7%, 10% growth every year, that's super important that we always work on the fundamental of the company, our IT system, our supply chain and so on and so forth. And I do believe we have a huge opportunity to leverage AI to keep really a strong level of scalability but also efficiency at the same time. And I said it, I will go very, very fast. We are also working a lot with the management team on how we keep simplifying Schneider Electric year after year to make it easier for our people to execute. 
Here again, a certain number of proof points on how we want to collaborate more with partner, supplier, company like Infineon, for instance. I mentioned going to next level of flexibility in capacity also, working strongly with companies like Samsung and Foxconn, for instance, where we believe it will give us an opportunity to accelerate really our capacity everywhere in the world, accelerate our competitiveness and an absolute obsession on at cost by design in order to contribute really to a very strong improvement of our gross margin. 
So a couple of examples that you have on that slide, but I remind you on the right-hand side of the slide, those operational metrics we've defined with Hilary during the Capital Market Day, which are absolutely essential for us. While we want to grow very fast, we want to stay very, very healthy at the gross margin level, always focus on the efficiency of the company. And last but not the least, always working also on our portfolio to make our portfolio more efficient. 
So these are really the main chapter that we presented to you on which we will give you an update every year, every half year on how we are progressing. But of course, I would not be complete if I would not speak about what makes Schneider Electric extremely different in the market, a very, very, very people and sustainability-centric company. I said it, we've completed successfully the past cycle when it comes to our sustainability achievement. We've presented that to you already. So I'm not going to go one by one, but we have launched our new program when it comes to what are the next transformation we want to deliver, with a very, very strong belief that as a company, we can have a lot of impact, but we believe that advancing energy tech will bring progress to all everywhere in the world. 
So there are a couple of metrics that we have kept from the past program. Again, saved and avoided emission, going to the next level. I told you 800 million tonne, plus we want to achieve 1.5 gigaton by the end of 2030. But new metrics we are building right now on how we can build, train more electrician in the world to support that big trend on electrification. And of course, always covering all the aspects of ESG and trying to impact our entire ecosystem, including supplier partner everywhere in the world. 
When it comes to people, we continue to invest a lot. Super important for me that, one, we keep our employees engaged in the transformation of Schneider. We are moving very, very fast. So we want to keep our employee along with us to keep the management, and we want really to make sure they are motivated and engaged to work with Schneider Electric. And at the same time, what is super important for me, we are moving really to this tech world, which require new competencies. So training our people in digital, in AI, in those new energy landscape technology is extremely important. 
And last but not the least, the second metric for us in terms of engagement is always offering the possibility of our employees to become shareholder of Schneider Electric and extremely pleased to tell you that 63% of our employees have invested in our worldwide plan last year with some country going above 80% of employee. So you imagine that's a strong demonstration of the commitment of our employees. And we've built this multiyear model, going to the next level of regionalization. We have a unique model of management where we want to have a very decentralized leadership, not only for the regional team, but also for the global people who are managing Schneider Electric. Why? Because I believe that in a world which is going to be more and more fragmented, that will make Schneider Electric much more agile and much faster to make the right decision. 
So to wrap up on the priority for me as the CEO of the company in '26, definitely, first and foremost, delivering a very strong performance. We'll come back to that with Hilary in a couple of minutes. But again, accelerating everything we do on the technology leadership side, being the absolute leader in the new energy landscape. We are the worldwide leader in electrification. We know the energy landscape is changing. It's bringing even more electrification, more change in our industry. We want to keep and reinforce that leadership. 
Going to the next level, leveraging AI and creating energy and industrial intelligence for our customers. And of course, with the data center market, which is growing fast, keeping an absolute leadership and making the most of this growth opportunity. Going to the next level of regionalization to satisfy even more our customers, local, regional and global. We see strong demand everywhere in the market. Most of the geography, all key geography will contribute positively in '26. So let's make the most of the growth everywhere in the world. And of course, executing seamlessly, the record high backlog that we delivered last year. 
Last but not the least, I said it, huge focus on operational excellence, gross margin improvement means strong focus on cost, productivity, pricing, margin obsession. This is very high in my agenda, very high in the agenda of the management team. And of course, we want to continue to build the next level of scalability for Schneider Electric and in particular, leveraging AI. 
So this is about the -- really what we plan to do in '26. But before going more in detail on how it translates in terms of financial ambition, I would like to hand over to Hilary, our Chief Financial Officer, to tell you more about our '25 financial performance. Over to you.

**Hilary Maxson** (Executives):
Thanks very much, Olivier, and good morning, everyone. Happy to be here with you all today. I'll start with our key financial highlights for the full year, some of which Olivier has already mentioned. 
Starting with revenues, and Olivier mentioned a few times, we're excited to show revenues of more than EUR 40 billion for the first time, finishing the year at EUR 40.2 billion in revenues, up 9% organic. In gross margin, as expected, we finished the year slightly negative. Despite this, we did continue to see a step-up in our adjusted EBITDA margin, which improved by 50 basis points organic, supported by strong cost control and the simplification actions we started in 2025. 
Our free cash flow was above EUR 4 billion for the third year in a row, a bit higher than our expectations, driven by strong operating cash flow and working capital improvements. In terms of net income, we were slightly negative at minus 2% with our adjusted net income up 4% recorded. And lastly, we did see a step-up in our ROCE to greater than 15% for the first time, reflective of our strong operating results. 
To get into a bit more detail, both businesses contributed to our overall growth in revenues of plus 9% organic with Energy Management up double digit for the fifth year in a row at plus 10% and Industrial Automation back to full year growth at plus 3%. And while it's not on this slide, I'll mention that all 4 of our geographies finished with positive full year organic growth in revenues in both businesses, a reflection of our strong portfolio positioning across our hubs. 
The positive contribution from scope is from Motivair and Planon, and we did finish the year with a negative impact from FX as anticipated, primarily due to the depreciation of the U.S. dollar and U.S. dollar impacted currencies. Based on current rates in 2026, we'd expect this negative FX impact to continue with minus EUR 850 million to minus EUR 950 million impact on full year revenues and minus 10 basis points impact on adjusted EBITDA margin. Of course, FX rates are not easy to predict. So to support your modeling efforts, we've updated our FX sensitivities to key currencies in the appendix of this presentation tied with the 2026 guidance we're giving today. 
Olivier already mentioned the 15% growth in our digital flywheel, which we use to track the progress of our transformation towards more digital and more recurring revenues. The only additional point I'll mention here is that you can see we're now at 79% recurring revenues in our agnostic software business. This recurring revenue profile supports greater visibility and margin and cash flow resilience over time, and it remains a central pillar of our value creation strategy. 
Turning now to our backlog at the end of 2025. We exit full year 2025 with a record backlog of more than EUR 25 billion and a growth of 18%. And just to note, that 18% is not in constant currency, so it reflects a similar drag from FX as we saw in our 2025 revenues. A couple of points I'll make here. First, this strong backlog will obviously support our sales in 2026 and into 2027. And more importantly, it gives us very good visibility, particularly in our data center business for the next 18 to 24 months. Second point, we did see a clear acceleration in orders in the fourth quarter, driven by data center, but not only, we also saw a good pickup in demand in infrastructure and in industry, including process and hybrid in the Q4. 
Moving now to Q4 revenues, which was a record high quarter for us. All 4 geographies contributed to our strong finish to the year, driving sales to EUR 11 billion, or plus 11% organic, and both businesses also contributed strongly. The positive scope is for Motivair. The first year there was very strong, better than business plan, and we saw a negative impact in FX in Q4, tied to the depreciation of the U.S. dollar and dollar impacted currencies. 
In terms of business models, we were up plus 4% in products with around half of that due to price as we ramped up our pricing to offset tariffs and inflation, particularly in North America. Our systems business grew very strongly, plus 19%, with growth led by data center with strong growth in Industrial Automation as well. Software and services was back to double-digit growth, plus 10% organic growth for the quarter, driven by double-digit growth in revenues in AVEVA and digital services. 
Turning to the 2 businesses. Energy Management was up 11% for the quarter, with North America at plus 19%, driven by growth in data center as well as industry and infrastructure. We did still see negative growth in residential in the U.S. and in Canada with some early signs, maybe wishful thinking of stabilization of demand in terms of orders in the U.S. In Western Europe, up 5% organic, the growth was led by data center with solid contribution from residential buildings. Asia Pacific was up 5%, with China up low single digit, driven by continued demand in data center with the building and construction markets still subdued. India was up double digit with strong growth in both products and systems, and Rest of the World was up 9% organic, with continued double-digit growth in Middle East and Africa. 
Industrial Automation was up 8% for the quarter, with North America turning to growth, up 5% organic, driven by discrete automation in the U.S., supported by the market as well as some investments we've made in the commercial organization there and with double-digit growth in both discrete and Process & Hybrid in Canada. Western Europe was up 8%, with growth led by AVEVA with solid growth in discrete and Process & Hybrid. Asia Pacific was up 7%, supported by sales at AVEVA with solid growth in discrete and Process & Hybrid. China was up low single digit and India was up double digit, both driven by continued growth in discrete. Rest of World was up 14% with strong growth across most of the region. 
Turning now to our P&L. We finished the year with adjusted EBITA of EUR 7.5 billion, up 12% organic, and we continued with another year of progression in our adjusted EBITA margin, up 50 basis points organic. This was driven by our strong organic revenue growth as well as strong leverage on our operating costs as we focused on cost control and started the implementation of our simplification program. These actions translated into our SFC to sales ratio, which stepped down almost 1 point to 23.3%. At the same time, we continue to support investments for the future in technology leadership and in customer differentiation. And you can see our R&D as a percentage of sales remained flat at close to 6% for the year. Our gross margin was negatively impacted by inflation, tariffs and by mix, partly offset by a strong acceleration in productivity in H2, and I'll speak more to that in a moment. 
Energy Management finished the year with adjusted EBITDA margin of 21.8%, flat to 2024, impacted by the same negative trends in gross margin as the group, offset by operating leverage. Industrial Automation finished with adjusted EBITDA margin of 14.2%, an improvement of 10 basis points organic, driven by improvements in gross margin, mostly offset by a deleverage in operating costs in the first half of 2025. 
Gross margin at the group level came in at 42.1%, down 40 basis points organic. And you can see the details quite clearly in the bridge. We did see a pickup in product pricing in H2, but not yet enough to offset headwinds from tariffs and raw materials, as expected. Mix continued negative for the full year, also as expected, due to the higher growth in our systems business. And we did see a strong pickup in productivity in the H2, supporting a stronger gross margin evolution in the second half of the year. 
Now Olivier will speak to more details in the trends we expect for 2026 in a few minutes, but we do expect a continued pickup in pricing throughout 2026, which, alongside the other drivers of our gross margin that we presented at our Capital Markets Day, should support a positive evolution of our gross margin in full year 2026. However, the timing of that ramp-up in price as well as the timing in RMI and tariffs will likely mean we continue with flat to negative gross margin progression in the first half of 2026 and tariffs being a bit difficult to predict at the moment. 
I mentioned the strong operating leverage we drove in our operating costs, or what we call our support function costs, in 2025 through both cost control as well as the kickoff of our simplification program. You can see we drove EUR 349 million in cost savings in 2025, more than offsetting inflation and allowing for investments in R&D, in commercial initiatives and in our digital backbone, including AI. 
Turning now to net income. Including scope and FX, our adjusted EBITDA is up 6%. As I mentioned in December at our Capital Markets Day, our restructuring costs did tick up to close to EUR 300 million tied to the simplification program that we kicked off this year and in support of the additional minus 1.5 to minus 2 points, we expect to drive in our SFC to sales ratio between '26 and 2030, and that excludes R&D. The only other item I would note is we did have an additional around EUR 100 million impairment in H2 tied to some equity method investments in the U.S. Alongside as anticipated increases in financing costs and PPA accounting, we did see a negative evolution of our net income of minus 2% with our adjusted net income, which excludes restructuring and impairments of EUR 4.8 billion, up 4% reported, or plus 14% organic, better reflecting our strong operating results. 
Free cash flow came in at a strong EUR 4.6 billion, a bit better than we expected, with strong operating cash flows, up 7%, and strong working capital improvements in inventory and days sales outstanding, driving a free cash flow conversion ratio of 106% or 111%, including those noncash impairments. As I mentioned in our Capital Markets Day, we'd anticipate our cash conversion ratio to be around 100% over the next years despite the capital investments we're making to support our growth, bolstered by structural working capital plans. 
And I'll finish with a slide on our balance sheet and ROCE. We did close the India transaction at the end of 2025, so you can see a small uptick in our net debt to adjusted EBITDA ratio. But overall, our balance sheet remains strong, well supportive of the A-level credit ratings we committed to at our Capital Markets Day. And I'm pleased to see our ROCE surpassed 15% at the end of 2025, reflecting our strong operating results. 
With that, I'll hand back to Olivier to cover our 2026 expectations.

**Olivier Pascal Blum** (Executives):
Thank you very much, Hilary. Indeed, let's close the first part of our call with what we see as a key trend in '26. It's going to be a summary because we've covered already a lot. But in short, what we see is a continued strong market demand, which will help us to drive growth and with positive contribution for all our end markets. Obviously, data center end market will lead the growth based on the growth demand -- the strong demand we've seen in '25 and we see that to continue in the future. 
What is very, very important for me is while we like and we love really taking the most of that opportunity, we will continue to position Schneider Electric strongly in industry and infrastructure, and we see great opportunity to accelerate the growth, and buildings to improve its contribution progressively also aligned with the macroeconomic trends. System will continue to lead our growth, but we see also some improvement on our product business, which will have a positive contribution this year and in particular, but not only in discrete automation, which has also been a very important point of focus last year. 
We'll keep growing in software and services. This is a translation of our energy intelligence story, with a very, very strong focus at the end of the day to drive more recurring revenues in all part of our business. The good news, all 4 regions will contribute to the growth, from North America, Europe, China, Southeast Asia and International, of course, led still by U.S. first and India probably second. But the good news is all markets will contribute positively. 
It's very, very important. We said it several times. What makes Schneider Electric very, very different, it's a balanced exposure by end market, by business model, also by geography, and we want really in '26 to continue to have this balanced exposure and to make sure we always make the most of those market opportunity and always building strong muscle for the future in case some part of the market might be less exciting in the future. So as a result of that, we are also putting a lot of action on price. Hilary said it. We want to be net price positive in value to be able to offset raw material impact and tariffs, ramp it up throughout the year. And as Hilary said, bringing and turning our gross margin positive during the year 2026. 
So the group expects the other driver of adjusted EBITDA margin expansion to be aligned with what we shared with you during the Capital Market Day. As a result of that, we have set up the following target for '26. So an adjusted EBITA growth between 10% and 15% which is supported on one side by a revenue growth of 7% to 10% organic. I insist organic is really an important point for us. We see massive opportunity in the market. And at the same time, we'll keep on increasing our adjusted EBITDA margin between 50 and 80 bps organically in '26. So all of that will translate our adjusted EBITDA in margin -- I mean, margin in a bracket of around 19.1% to 19.4% for the full year '26. 
So exciting year in front of us. We are ready. We have a plan. And definitely, we plan to accelerate the overall execution of that strategy in '26. 
So before we hand over to you for Q&A, today is an important also day. We made the announcement this morning that it will be your last earnings call, Hilary. Hilary has been with us for 9 years. She has been the CFO for the past 6 years. She's going to take the next assignment in the United States that will be announced later. And she will be replaced by Nathan Fast, which is actually on my left. So Nathan has been in the company for almost 20 years, have been doing a lot of different job in different part of Schneider Electric, the last one being Investor Relationship. So very pleased to have you Nathan, in this new role, and I'm sure you will build on the strong legacy that has been built by Hilary in the finance, and you will help us to execute that plan very, very fast and to drive strong shareholder return. 
Hilary, I want to thank you for the partnership. It has been a great journey in the past 10 years, but in particular, in the past 15 months, the 2 of us. You have been a fantastic support for me to become the CEO of Schneider Electric. So I want to thank you on behalf of the team here at Schneider Electric and wishing you all the best in your next chapter.

**Hilary Maxson** (Executives):
Yes. Thanks, Olivier. Schneider has obviously been a huge piece of my life and my career, and I'm extremely grateful to the Board, to yourself, the CEOs and colleagues with whom I've worked over these past 9 years and for the trust and support they've given me. And in particular, you mentioned I'm excited on the work we've done together over the past 15 months, to put the company on the trajectory we described in our Capital Markets Day and reiterated today. I'm certain I'm leaving at a time when the company is on a great trajectory, and I'm really pleased we've been able to prepare a great successor with Nathan over the past few years. I'm confident that he'll hit the ground running. And then just for those curious, my next role will be announced closer to the date of my departure. 
So Olivier, back to you.

**Olivier Pascal Blum** (Executives):
All the best, Hilary, and we will work together, you, Nathan and I in the coming weeks to do a very smooth transition and starting next week, by the way, with all our investor roadshows. So we'll continue to have fun together for a couple of weeks. 
Nathan, back to you for the next part.

**Nathan Fast** (Executives):
Okay. Olivier, maybe I can say a couple of words as well. First, I'd really like to thank Hilary, right, first, for her leadership across the finance function, but also the opportunity to have learned many, many things, Hilary, over the last 9 years working extremely closely together. And then I guess, Olivier, also maybe a bit to you. Thank you for the trust. I, of course, take the position with humility and determination to succeed together with you and your leadership team. So thank you for that.

**Nathan Fast** (Executives):
I'll make the transition then to the Q&A, of course. and thank you both for the presentation. We have around 20, 25 minutes. I'm sure there's a lot of questions, and I want to make sure we get to every analyst with the question. So if you can please just stick to one question, that would be great. 
And with that, operator, let's go to you for the first question, please.

**Operator** (Operator):
[Operator Instructions] The first question is from Phil Buller of JPMorgan.

**Philip Buller** (Analysts):
Just to follow up on that CFO transition topic, if I can, to start. And obviously, thanks, Hilary, very best wishes for the next chapter, and congrats, Nathan, of course. The question is on timing. I've had a few investors asking about that today. It obviously sounds very smooth, but it's obviously also been announced shortly after a major CMD. So if you could just share some additional color as to the genesis of this, Olivier, perhaps, is this something that you were envisaging during the CMD buildup as you build those 2030 objectives together as a team? How involved was Nathan, in particular, in that process? And has anything changed? One of the data points offered at the CMD was in relation to the AVEVA margin expansion. And obviously, there's a question at the moment about software more broadly. So just a little bit more color about the genesis and the time line and if anything has changed in terms of the assumptions even in that relatively short period since the CMD, please?

**Olivier Pascal Blum** (Executives):
Sure, sure, sure. Well, look, as we said, and I'm sure you can feel it today, this is a very smooth transition that we are managing with Hilary. Just want to tell you that Schneider Electric is not one man or two people show. What we've presented to all of you at the CMD, it's the work of the entire executive committee. They have been associated to the building of this next cycle. I told you many, many times in '25 that it was time for Schneider Electric to build this next cycle, inventing what advancing energy tech and with actually more executive last year that we have usually to work all together as a team. And Nathan has been associated in the later part of last year, of course, as a new IR of the company in the building of that plan. So I understand that a change of leadership always raised question. 
But again, we respect, first of all, the choice of Hilary to take a new role and to have a next chapter in your career life. But what is very, very important at the same time, we are very, very solid team behind this plan. I've been now the CEO for 15 years -- 15 months. Before that, I was in Schneider again for more than 32 years. So I think what is super important and Hilary has helped me a lot to build this very strong plan for the next cycle. Whatever we presented to you in the CMD in terms of assumption, driver and how we want to accelerate the performance of Schneider Electric remain absolutely valid. And as I, Nathan has been associated through this plan from day 1, so I feel confident that we will manage this transition smoothly, and we are fully ready this year to execute our plan extremely fast.

**Operator** (Operator):
The next question is from Alasdair Leslie of Bernstein.

**Alasdair Leslie** (Analysts):
So a question on pricing. I mean, obviously, if we look at that EBITA bridge, it does look like the gross pricing was still relatively muted in H2, but obviously, you're flagging an acceleration in Q4. I was just wondering if you could talk a little bit more about those kind of pricing exit trends. Any price increases you've already put through year-to-date? And then I was actually wondering if you could comment specifically on the pricing environment in China. Have you seen any stabilization or improvement in the deflationary environment there? It's a market, I think you said recently at the CMD that you were working on pricing as well. So what's the problem is for 2026 and our margins generally in China still holding up at high levels?

**Olivier Pascal Blum** (Executives):
Yes. Absolutely. Thank you very much for the question. I'll start and hand over to you, Hilary, to complete. Look, we told you last year in H2 with Hilary that definitely, we were ramping up step-by-step more pricing everywhere in the world and in particular, in North America, we know with impact of the tariffs. Last year, as you know, was a complicated year where we had up and down on tariff. It kept changing. So it was not always easy really to plan what would happen. Last year, in Q4, we put a very solid plan to accelerate pricing. 
What happened since Q4, we have seen also a huge increase of raw material. So there was, on one hand, the need to implement what we decided last year, but also to accelerate everything we plan in pricing to compensate the impact of raw material. We have a lot of silver and copper in all our products. So I think the good news this time we were ready with the initial plan of Q4, and it was just about how we accelerate to add on top of that the compensation of raw material. I'll let you complete maybe on the second part of the question on China [indiscernible].

**Hilary Maxson** (Executives):
Yes, sure. Indeed. So we did see an acceleration in 2025 in the Q4 in pricing generally, of course, in particular, in North America, that's where we have the tariff impacts in front of us. China for 2025 definitely remain deflationary. So those low single-digit numbers that we're talking about in China would be higher without that deflationary. They're higher in volume. We would expect China -- it's not always easy to call. The government is trying to combat deflation. But in general, we'd expect China to remain deflationary in 2025. That said, with the uptick of raw material prices, which impacts far more beyond just our industry and our own competitors, we did start to see pricing and price increases, including with all kinds of local competitors across industries in this Q1 in China. 
So we expect there to be a bit of a turn there as well. And I'll just mention that we did update in the appendix of this presentation, a slide we gave a few years ago with the breakdown of copper and silver for us in terms of raw materials in 2025. So you can see all of the information. And like Olivier mentioned, '26, we expect that we'll continue that ramp-up that we already talked about in the second half of last year.

**Operator** (Operator):
The next question is from Andre Kukhnin of UBS..

**Andre Kukhnin** (Analysts):
I'll focus on data centers, please. Historically, you gave us very helpful disclosure on how much of your backlog is from data centers and distributed IT and how much of that sort of pure data centers and hyperscalers within that. Could you please give us those details for 2025? And the bigger question really, I wanted to get your view on how you're positioned for the 800-volt direct current architecture transition and in particular, what are your state of offering at the moment in solid-state transformer and solid-state braking?

**Olivier Pascal Blum** (Executives):
Absolutely. Well, look, it's a very important question. Maybe I can start by the second part of the question, Hilary, and hand over back to you for the first part on that backlog. Indeed, when you look at the evolution of data center, the type of AI factory you will have to build in the future to support the next generation of GPU of NVIDIA like Rubin Ultra or Feynman, that will require at one point of time, a different type of infrastructure. So that's why there is so much buzz on 800-volt DC. We see that it will be an important trend. It's very difficult to say by 2030, when you look at all the data, we say 200 gigawatts to be built in the world. 
We estimate all reports in the market estimate 15%, 25% of the demand could be impacted by 2030. What is super important, you are talking about an evolution of the electrical infrastructure, which is, again, where Schneider Electric has a very strong leadership. So we are developing one, what we call, as you know, the sidecar concept, which can be available immediately, which is a minor evolution of the infrastructure. But we are developing those full definitely architecture that could be ready by '28 when the market will start to grow. And we are leveraging here a lot of competency we have in-house, in particular, in China, but also we're working with partners. 
So again, that's a domain that we know very well because it's touching the core of the electrical infrastructure that creates actually also opportunity for Schneider Electric to stay extremely differentiated in the market in the future. And as I said, we have to get ready for a transition that will be slow, that will take time, but it's super important that as a worldwide leader in electrical distribution, Schneider Electric is the first one really to offer the most innovative solutions. 
So again, you're absolutely right. That's an important trend. We are extremely well positioned. We have accelerated our investment in '25 to develop concept. A bit too early to say because the demand is just about to start, but we are fully ready to face this new trend, which again will impact our market step by step between probably '28 and 2030. Hilary?

**Hilary Maxson** (Executives):
Thanks, Olivier. In terms of the backlog, you're right, we didn't give a backlog breakdown by end market. And I don't think we would intend to do that. But what we are doing, and you can see we've updated the exposure in terms of our 2025 orders across our end markets. So now we're doing that annually. I think you can infer generally the orders growth that we've seen there, and you can infer from that probably some component of data center and networks. Of course, out of the energy management piece of the backlog, which we showed, a good portion of that is data center and network, but not only. So we also had good growth in the rest of the end markets.

**Operator** (Operator):
The next question is from Jonathan Mounsey of BNP Paribas.

**Jonathan Mounsey** (Analysts):
And may I just also say, sorry to see you go, Hilary, but welcome, Nathan. In terms of my question, will you just so -- the intake so far in Q1? I mean, obviously, there was a big step-up in DC intake in Q4, I think probably for all the players, and you've confirmed that again today. Just wondering whether that's really continued into 2026. And also, with the order intake where it is and with your comment around it really gives you visibility through for the next 18 months, are we saying now that kind of revenue growth in data centers is capped this year and what we're booking now is really for 2027?

**Olivier Pascal Blum** (Executives):
Do you want to start, Hilary?

**Hilary Maxson** (Executives):
Sure. So in terms of intake in Q1, well, we've said quite a few times before, and we're not quite done with the Q1 yet that we don't consistently look at orders as the right way to look at data center and network. But what I would definitely say is that demand for data center accelerated in the Q4, and we don't see a different change in trend in the Q1, if that's what you mean. That's the first part of your question. Visibility, indeed, we have good visibility. We've talked about it for some time, and you can see it even in orders in the backlog now, 18 to 24 months in terms of data center. In general, those projects now are being planned probably mostly in those later two years. That's what the hyperscalers and the others are doing. So yes, we would have a decent visibility on 2026 revenues associated with data center at this time, exactly.

**Operator** (Operator):
The next question is from Gael de-Bray of Deutsche Bank.

**Gael de-Bray** (Analysts):
So just a follow-up on this. I mean, you obviously finished the year with a very strong backlog now exceeding EUR 25 billion. So can you help us understand how we should think about the timing of conversion, specifically for 2026 and '27? And what are the potential bottlenecks you may have to solve to convert that backlog into revenues?

**Olivier Pascal Blum** (Executives):
Yes. Thank you for the question. First of all, I'd like to remind and probably rebound on what Hilary said. In the way we operate in that market and in particular, with the large hyperscaler, we work with them on the design, we freeze the design, we look at the planning they need in terms of capacity, and it help us to adjust our capacity. So the combination of this work we are doing on design agreements we are making with them is helping us really to have a good visibility, as Hilary said, 18, 24 months on what's going to happen. To answer more specifically your question, in the acceleration of Q4, a large part of what we booked in Q4 will be executed more in '27, but that will impact a little bit '26. 
And the second part is definitely, we see an acceleration in demand of those AI factory everywhere in the world. We see that in North America, but I was just in India last week, for instance, for the AI Summit. We see also that India is accelerating. So that gives us the confidence that we can predict pretty well what's going to happen because we are really very well connected first with hyperscaler. We are operating in those key geography. And for a company like Schneider Electric, if we have a kind of 2 years visibility on the demand, we can react on capacity. We can do it by ourselves by building extra capacity. But we are also working more and more with different partners. I was mentioning Foxconn, the regional partner everywhere in the world to adjust capacity plus/minus if needed. 
So the only change for a company like us, probably a couple of years ago, we are looking at our overall capacity every 2 to 3 years, and then we move to 1 year. Now it's a very dynamic process where every quarter, we revisit the demand for the next 3 years, and we adjust eventually the capacity we need. Keeping in mind that we want to stay very balanced. So it's not only about building capacity for North America, but also making sure we are building capacity in the other part of the world. That's why I was saying you, for instance, before that we decided last year to invest in a new factory for liquid cooling in India because we see the demand for AI factory in India also coming, and that's why we have accelerated the execution of the plan. So that's how we are managing. There will be up and down. Of course, we'll continue to adjust. But I think we are fairly confident with the visibility that we have in the pipeline, the way we are working with all those key stakeholders and adjusting permanently our capacity.

**Hilary Maxson** (Executives):
And we do give a breakdown of the backlog between less than 1 year and more than 1 year. We would intend to meet the customer commitments we have. So all that backlog you see in less than 1 year, we'd obviously expect to accomplish in 2026.

**Operator** (Operator):
The next question is from James Moore of Redburn Atlantic.

**James Moore** (Analysts):
Hilary, thank you for all your help and best of luck. And Nathan chapeau. Could I ask about software and AI and the disruption risk in sort of 3 dimensions. I think we're talking increasingly about software being made up of a kind of UI SaaS application layer that is going to be fully disrupted by agents, but under that a system of record and a database with more of a moat. And I would argue that your AEC business does have some of that top UI layer that could be disintermediated. Have you done any work on what proportion of revenue do you think that is at risk and what proportion you think is safe from AI directly substituting you? 
And secondly, as customers increasingly use AI to increase their workflow productivity and presumably, if you continue to price on a seat-based monetization model, you're going to see a decline in revenue. How quickly? And are you planning to pivot to tokens or to another form of usage? And how quickly do you think you can do that? And I guess the third dimension is you're going to be trying to increase the degree of AI in your own software products to add compute and value. Are you worried that, that aspect of AI uplift can also be disintermediated by others taking that aspect of the productivity improvement work? This is sort of quite a lot bundled into that. But Olivier, I'd be very interested in your thoughts.

**Olivier Pascal Blum** (Executives):
Thank you. No, it's an excellent question and indeed, a very complete question. Let me start. Of course, we are doing analysis permanently. And I tell you why, because when we really started to see even end of '24, the acceleration of AI, we discovered that it was a massive opportunity for Schneider. We've been quite vocal with you for the past 2 years on what we do in digital services. Digital services is basically a business where we extract data coming from all the assets that we make more connectable. We've been -- we built this offer that we call EcoCare. AI has helped us to go much faster actually in creating more value for our customer. 
So obviously, when we realize that it will help us to go much faster, and to deliver more value and you don't need to go through a very complex software in the middle. Immediately, what we've done with Caspar, the CEO of AVEVA, was ready to look at our own portfolio and to check if it could be disrupted. Now I don't want to be too oversimplified, but what AI brings is when you have simple repetitive task, a lot of information that you need to capture. And when you look at the portfolio of AVEVA, I don't want to say that we have 0 risk. But the large part of what we are doing is about leveraging extremely complex data that come from industrial infrastructure, working on very complex and critical installation, where cybersecurity, by the way, on top of that is extremely important. 
So I see that there is still a space for huge growth for all those complex software because we are solving complex problems for our customers. And here, as you said in one of your question, AI is also an opportunity to amplify what we have been doing with AVEVA with the AI agent to go to the next level. So at that point of time, I don't want to say we are not worried, but we believe a large part of what we are doing in our software portfolio is not impacted negatively, but more positively. I'll just give you a last example maybe before I hand over to Hilary on the pricing side. 
You take what we have been doing with ETAP. ETAP is about building a software to design electrical infrastructure for the future, where you have to simulate a lot of assets, which are extremely complex assets. That's what we are doing in the Omniverse, for instance, with NVIDIA. We don't see AI at all being able to disrupt that kind of software. Now again, building AI agent on top of our software to make it even easier for our customer to use it, of course, why not? So all in all, we are -- we believe we are in a good place. We will be attentive. And at the same time, wherever we don't have a strong software business, we believe it will help us to accelerate some part of our portfolio for simple implication that we can deliver to our customer.

**Hilary Maxson** (Executives):
And in terms of your question about the seat-based model or pricing in the software business, as part of the AVEVA transition to subscription, and we did a lot there. It's not just changing contracts and things like that. But you may recall that we've talked about the flex pricing model that we've been invoking at AVEVA more and more tied with Connect, but not only with most of the services of AVEVA and into OSI. That's the pricing model that we've been moving to over the past few years. And that's effectively token-based. So we didn't do that because of foresight on AI -- agentic AI, but that is the model that we've moved -- started to move to and that I feel comfortable will be sort of the model of the future for this type of software.

**Nathan Fast** (Executives):
Thanks, James. We probably have about 5 minutes left. So if you can make the questions pretty concise, then we can maybe fit in a couple more. Operator, next question?

**Operator** (Operator):
So the next question is from Ben Uglow of OxCap.

**Benedict Uglow** (Analysts):
I will keep it brief. It's really just on Industrial Automation and the margins. I have to be honest, I am surprised to see your margins still below 15%. And I guess it's two things. One is why aren't we seeing a little bit more operating leverage? And certainly, that's what we have seen in some of your peers. And secondly, just in absolute terms, why are we so low? Is this to do with China and country mix? How much is to do with process? How much is to do with SaaS transition? If you can just give us a sense of what part of the business is keeping the margins so low, that would be helpful?

**Hilary Maxson** (Executives):
Sure. So with Industrial Automation, indeed, we did finish below 15%. I mentioned that on the positive side, we do start to see that -- those improvements in gross margin in the business, which is exactly what we expected as we moved into the second half. So the big -- the detractor, I would say, in 2025 is that we did continue to have negative operating leverage in the first half. So what's driving -- and I'll talk to that in a second, but what's driving those lower margins, we've mentioned it a couple of times. A big component of it for us has been mix, the mix between Process and Hybrid and Discrete. We saw Discrete start to come back in the second half. That's been a big component of the mix return for us, and we'd expect that to move forward in future. Second, AVEVA and that transition to subscription, we shared in the Capital Markets Day that we're going to be moving our adjusted EBITDA margins up there now more swiftly over the next couple of years. So that's been a bit of a detractor, although it was an improver, obviously, in gross margin in the second half in terms of mix contribution. 
And then we have had a real drag in terms of operating leverage at the business. We have Gwenaelle, our new leader there in Industrial Automation that spoke about the changes that she's making in not just 2026, but going forward. But we would expect all of that to be operating in the right direction on all cylinders in 2026. So we'll have some more improvement in mix, normal productivity. And AVEVA, we're almost done with that transition to subscription. So we'll start to see more and more contribution at the level of adjusted EBITDA as well. So yes, not where -- exactly where we would have liked to be in 2025, but I think all the levers are there for '26 and beyond. And we gave a little bit of an idea of that margin journey in the Capital Markets Day to 18% and perhaps even a bit better by 2028.

**Nathan Fast** (Executives):
Thanks, Ben. Maybe one last question, and we can try to go quick on this one. Operator, next question?

**Operator** (Operator):
The next question is from Martin Wilkie of Citi.

**Martin Wilkie** (Analysts):
First, Hilary, thanks for all the debates and interactions over the years and good luck for the future. My question was just on the seasonality and the implications for the profit uplift in the second half. And I know you've not guided explicitly, but if gross margins are lower in the first half, presumably the organic EBITA margin expansion is sort of clearly less than 50 basis points. As we think about the implication for the second half and at the upper end of the range, it would have to be more than 100 basis points up in H2. Is that all driven by price cost? Or is the leverage from industrial automation coming back and the volume effect from that? Or is the AVEVA timing? What would drive that quite large uplift in profitability in the second half?

**Hilary Maxson** (Executives):
So in terms of seasonality, we have two pieces of seasonality in my mind. One, something that is completely out of our control, which is raw materials and then the pricing that we do beyond that. The pricing is obviously in our control. That can pull our seasonality one way or another. So we've seen in 2022, 2023, that seasonality going in different directions being pulled by that. And here, when I talked about that negative gross margin potential in the first half, that's a lot driven by that uptick in pricing. And for example, with tariffs, we don't have any baseline of tariffs in the first half, whereas we do in the second half. So there's timing there. 
The other component of seasonality that we generally always see in our business is just associated with volumes. We have stronger volumes in the second half than the first half. That's been a seasonality for a long time across the business. So we have stronger leverage and we have stronger productivity usually in the first half. So in 2026, in particular, we would have better baseline on RMI and tariffs, the pricing plus productivity and volumes and operating leverage, which is those differences you'll see between the H1 and the H2.

**Olivier Pascal Blum** (Executives):
And I'd just like to complete indeed, there are a couple of drivers which are very specific to what's going to happen in '26. But as we said multiple times, in the plan we built last year, we have the ambition to work on all the cylinders of the gross margin. So of course, this year, we have a very strong focus on pricing, and we'll keep on going and especially with raw material. It's pricing of product. It's also how we price our services business, how we bring the right level of selectivity in our system business. It's also working on the portfolio. We have historically some activity which are more dilutive than the others. You've seen in the CMD that we want to take out EUR 1.5 billion. So since last year, we built this very strong plan that we call gross margin obsession, making sure we work on all the drivers. But indeed, as Hilary said, there are some specific drivers for this year, but it's a short term and long term because we want really to make sure that we have an extremely solid gross margin, which is for me, the best reflection of the health of the business of Schneider Electric.

**Nathan Fast** (Executives):
Okay. Thanks, Martin, for the question. Olivier, you have one word, and then we...

**Olivier Pascal Blum** (Executives):
We are done with the question. I guess...

**Nathan Fast** (Executives):
Yes, we're done with the Q&A.

**Olivier Pascal Blum** (Executives):
So again, I want to thank you for spending time with us today. We are closing the chapter of '25. You can feel that we've been excited, EUR 40 billion, EUR 4.6 billion of cash flow generation. It has been the great year, but it's closed. We have a plan. Now our focus is really to make the most on '26 and make sure we can continue to drive a strong shareholder return. So we will be excited, of course, in the coming days, coming weeks to follow up with some of you and especially next week to go more in detail on that presentation. Again, thank you for the time spent with us. Thank you again, Hilary. All the best to you, Nathan, and focus on '26 now.

**Nathan Fast** (Executives):
All right. Thanks, Olivier. I think we'll stop there. Look forward to meeting you, Olivier, mentioned earlier on some virtual road shows in the coming weeks. And additionally, of course, the IR team is available for you to engage. Thank you very much, and have a good rest of the day.

**Olivier Pascal Blum** (Executives):
Thank you.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SU.PA_2024_Earnings_Call_20250220.md
- 2025-02-20｜Olivier Blum (CEO)｜guidance：2025 調整後 EBITA 有機成長目標 10%–15%（原話："we have set up a target with an improvement of our adjusted EBITA from 10% to 15% organically."）
- 2025-02-20｜Olivier Blum (CEO)｜guidance：2025 有機營收成長目標 7%–10%（原話："strong growth organically between 7% and 10% for the year 2025"）
- 2025-02-20｜Olivier Blum (CEO)｜guidance：2025 調整後 EBITA 利潤率目標約 19.2%–19.5%（原話："an adjusted EBITA margin around 19.2% to 19.5%"）
- 2025-02-20｜Olivier Blum (CEO)｜guidance：跨循環成長率維持 7%–10%（原話："we confirm really this 7% to 10% growth across the cycle"）
- 2025-02-20｜Hilary Maxson (CFO)｜guidance：2025 匯率預期轉為正貢獻，營收約 +6–7 億歐元（原話："plus EUR 600 million to EUR 700 million to our top line"）
- 2025-02-20｜Hilary Maxson (CFO)｜guidance：2025 有效稅率預期 23%–25%（原話："our ETR will be in the range of 23% to 25% for 2025"）
- 2025-02-20｜Hilary Maxson (CFO)｜guidance：2025 現金轉換率預期再度接近 100%，含資本支出增加（原話："the cash conversion ratio to again be approaching 100%"）
- 2025-02-20｜Olivier Blum (CEO)｜guidance：Discrete 自動化需求回升，預期下半年加速（原話："accelerating a bit more in the second part of the year 2025"）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：2025 毛利率仍有進步但幅度較小（原話："some gross margin progression, but at a more muted level"）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：Systems 定價在 2025 預期趨於正常化（原話："We would expect some normalization of that in 2025."）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：2025 毛利率放緩原因：Systems 定價正常化，加上正常範圍的產業生產力（原話："more normal pricing in Systems"）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：2024 工業自動化調整後 EBITA 利潤率下滑 150bp，管理層稱符合預期（原話："was down, as expected, 150 basis points"）
- 2025-02-20｜Olivier Blum (CEO)｜margin：管理層稱 AI 訓練／推論資料中心對利潤率無特別影響（原話："From a margin standpoint, it does not have any particular impact."）
- 2025-02-20｜Hilary Maxson (CFO)｜margin：數字口徑：資料中心占訂單 24% 的拆解（原話："Around 20% of that is pure Data Center, around 4% is Distributed IT now."）
- 2025-02-20｜Hilary Maxson (CFO)｜customer：純資料中心中，超大規模雲端客戶占比不到一半（原話："Of that 20%, a bit less than half of that will be with hyperscalers."）
- 2025-02-20｜Olivier Blum (CEO)｜customer：資料中心占 2024 終端訂單 24%（原話："that represents 24% of our end orders in 2024"）
- 2025-02-20｜Hilary Maxson (CFO)｜customer：資料中心成長描述為健康而非指數式（原話："As we've said before, not exponential, but healthy growth"）
- 2025-02-20｜Olivier Blum (CEO)｜customer：針對 DeepSeek 提問，稱客戶端訂單趨勢沒有變化（原話："there is no change in the trend"）
- 2025-02-20｜Olivier Blum (CEO)｜customer：北美占比：在地製造在地銷售比例（原話："we have already 83% of what we sell in North America"）
- 2025-02-20｜Olivier Blum (CEO)｜competition：DeepSeek 被詮釋為 AI 消耗量增加的佐證（原話："the consumption for AI will get bigger and bigger"）
- 2025-02-20｜Hilary Maxson (CFO)｜product：數位與數位賦能營收占比及軟體循環收入占比（原話："we're now at 77% recurring revenues in agnostic software"）
- 2025-02-20｜Hilary Maxson (CFO)｜product：Systems 業務 Q4 銷售成長 27%（原話："translating into sales of plus 27%"）
- 2025-02-20｜Hilary Maxson (CFO)｜risk：北美住宅市場疲弱，管理層歸因於高利率（原話："We did see some weakness in residential, particularly in the U.S."）
- 2025-02-20｜Hilary Maxson (CFO)｜risk：法國競爭主管機關罰款已提列 1.04 億歐元準備（原話："a provision of EUR 104 million tied to the fine"）
- 2025-02-20｜Hilary Maxson (CFO)｜risk：關稅：若現行貿易協定特殊區維持，墨西哥對美進口曝險規模（原話："only in a few hundred millions"）
- 2025-02-20｜Olivier Blum (CEO)｜risk：中國 2025 預期無重大轉變（原話："we don't expect any major shift in 2025"）
- 2025-02-20｜Hilary Maxson (CFO)｜capital_allocation：不排除特別配息（原話："not averse to some sort of special distribution"）
- 2025-02-20｜Hilary Maxson (CFO)｜capital_allocation：庫藏股僅用於抵銷員工持股計畫（原話："share buybacks to neutralize our employee share plans"）
- 2025-02-20｜Olivier Blum (CEO)｜capital_allocation：2027 計畫不含併購（原話："the plan that we have presented by '27 is without M&A"）
- 2025-02-20｜Hilary Maxson (CFO)｜capital_allocation：第 15 年累進股息提案（原話："dividend for the 15th year of EUR 3.90 per share"）
- 2025-02-20｜Olivier Blum (CEO)｜commitment：下一循環增量產能投資 20 億歐元（原話："EUR 2 billion of incremental capacity in the next cycle"）
- 2025-02-20｜Olivier Blum (CEO)｜commitment：稱商業應變措施可使 2025 獲利指引仍能達成（原話："we will be able still to deliver our profitability guidance in 2025"）
- 2025-02-20｜Olivier Blum (CEO)｜commitment：數位飛輪目標：2027 年占集團營收 60%–65%（原話："60% to 65% of our group revenue by 2027"）
- 2025-02-20｜Olivier Blum (CEO)｜commitment：Motivair 收購將於數日內完成（原話："we are closing, in the coming days, the acquisition of Motivair"）

### SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20230504.md
- 2023-05-04｜Hilary Maxson｜guidance：CFO 宣布調升 2023 年調整後 EBITDA 同口徑成長目標區間（原話："adjusted EBITDA to between plus 16% and plus 21%"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 稱 2023 年需求持續強勁（原話："persistence of strong demand, supported by underlying trends"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 預期供應鏈情況改善（原話："expect an improvement in the supply chain situation"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 提到消費相關區塊出現放緩（原話："a slowdown observed in consumer-related segments"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 揭露年底在手訂單金額（原話："record backlog of EUR 16.50 billion"）
- 2023-05-04｜Hilary Maxson｜guidance：CFO 報告能源管理事業第一季營收與同口徑成長（原話："ended the quarter at EUR 6.5 billion, up by more than 18%"）
- 2023-05-04｜Hilary Maxson｜margin：CFO 揭露 2022 調整後 EBITDA 利潤率水準（原話："ended the year at a record level of 17.6%"）
- 2023-05-04｜Hilary Maxson｜margin：CFO 說明 2022 調整後 EBITDA 利潤率同口徑改善幅度（原話："improve our adjusted EBITDA margin by 40 basis points"）
- 2023-05-04｜Hilary Maxson｜margin：CFO 說明毛利率韌性的來源（原話："thanks to actions on prices to counter inflation"）
- 2023-05-04｜Jean-Pascal Tricoire｜margin：執行長說明營運現金流與自由現金流差距的原因（原話："we built up stock to be able to supply our customers"）
- 2023-05-04｜Hilary Maxson｜product：CFO 揭露數位飛輪占集團營收比重（原話："digital flywheel represent 53% of group revenues"）
- 2023-05-04｜Hilary Maxson｜product：CFO 揭露軟體與服務中經常性收入占比及目標（原話："36% of the revenues associated is classified as recurring"）
- 2023-05-04｜Hilary Maxson｜product：CFO 揭露 AVEVA 年化經常性收入成長（原話："ended the year with 23% growth annualized recurring revenue"）
- 2023-05-04｜Jean-Pascal Tricoire｜product：董事長說明集團軟體營收規模（原話："software company with revenues of EUR 2.6 billion"）
- 2023-05-04｜Jean-Pascal Tricoire｜competition：董事長說明集團在工業軟體的排名（原話："top 3 of industrial software businesses"）
- 2023-05-04｜Jean-Pascal Tricoire｜product：董事長談 AI 對產品的影響（原話："A huge impact."）
- 2023-05-04｜Jean-Pascal Tricoire｜product：董事長說明 AI 工程師招募（原話："several hundreds of recruitment of AI engineers"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 說明槓桿比率偏高及預期（原話："we expect it to normalize over time"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 宣布股利提案（原話："EUR 3.15 per share, up 9% on last year"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 回答庫藏股暫停（原話："we've been on a pause for quite some time"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 指出現行庫藏股計畫規模（原話："EUR 1.5 billion to EUR 2 billion worth of plan"）
- 2023-05-04｜Hilary Maxson｜capital_allocation：CFO 說明近年未宣布新的庫藏股計畫（原話："we haven't announced any new share buyback plans"）
- 2023-05-04｜Jean-Pascal Tricoire｜capital_allocation：董事長列出現金配置第一優先（原話："The #1 priority is to preserve a high-quality rating."）
- 2023-05-04｜Peter Herweck｜commitment：新任執行長承諾 2023 年交付（原話："focused on sticking to our commitments and driving growth"）
- 2023-05-04｜Jean-Pascal Tricoire｜commitment：董事長重申影響力營收承諾（原話："we have committed to generate 80% impact revenue by 2027"）
- 2023-05-04｜Jean-Pascal Tricoire｜commitment：董事長說明 SBTi 認證的 2030 減碳承諾（原話："by 2030 to reduce our carbon footprint by 25%"）
- 2023-05-04｜Jean-Pascal Tricoire｜commitment：董事長說明 2050 減碳承諾（原話："by 2050, we are determined to reduce our emissions by 90%"）
- 2023-05-04｜Jean-Pascal Tricoire｜risk：董事長談美中兩大市場夾在地緣緊張中（原話："we're in the crossfire"）
- 2023-05-04｜Jean-Pascal Tricoire｜risk：董事長談電子零組件供應壓力（原話："a great deal of pressure on the number of components"）
- 2023-05-04｜Jean-Pascal Tricoire｜risk：董事長談俄羅斯營運撤出（原話："We managed to extract from Russia."）
- 2023-05-04｜Jean-Pascal Tricoire｜customer：董事長說明財星 500 大客戶覆蓋（原話："partners of around 40% of Fortune 500 businesses"）
- 2023-05-04｜Jean-Pascal Tricoire｜customer：董事長說明沃爾瑪要求協助其供應商減碳（原話："Walmart has asked us to work with its suppliers"）
- 2023-05-04｜Jean-Pascal Tricoire｜risk：董事長回應 EACOP 專案爭議決定續做（原話："We, therefore, decided to continue with this project."）
- 2023-05-04｜Jean-Pascal Tricoire｜product：董事長談核能業務定位（原話："we did not work so much in nuclear"）
- 2023-05-04｜Jean-Pascal Tricoire｜customer：董事長說明節能效益（住宅）（原話："You can save up to 25% of energy."）
- 2023-05-04｜Jean-Pascal Tricoire｜capital_allocation：董事長說明併購與庫藏股之間的取捨（原話："the creation of the future through acquisitions"）

### SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md
- 2023-11-09｜Hilary Maxson｜guidance：2024–2027 有機成長 CAGR 目標 7%–10%（原話："organic growth CAGR of plus 7% to 10%"）
- 2023-11-09｜Hilary Maxson｜guidance：Hilary 說明 7–10% 不是逐年指引，而是整個週期（原話："that's not a guideline for any of the given years"）
- 2023-11-09｜Peter Herweck｜guidance：可觸及市場未來 4 年 CAGR 6%–7%（原話："a 6% to 7% CAGR over the next 4 years"）
- 2023-11-09｜Hilary Maxson｜guidance：調整後 EBITA 率有機 CAGR 約 50 bp（原話："adjusted EBITA margin at a CAGR of around 50 basis points"）
- 2023-11-09｜Hilary Maxson｜margin：分析師問 50bp CAGR 是否=20% 利潤率，Hilary 說明 CAGR 口徑（原話："then it would be 50-50, 50-50"）
- 2023-11-09｜Peter Herweck｜guidance：長期營收與獲利願景：500 億歐元營收（原話："EUR 50 billion revenue, we think,"）
- 2023-11-09｜Peter Herweck｜guidance：長期調整後 EBITA 目標 100 億歐元（2x5）（原話："We need profitability, EUR 10 billion, 2x5 adjusted EBITA."）
- 2023-11-09｜Peter Herweck｜guidance：自由現金流轉換率目標約淨利 100%（原話："100% of net income over the and across the cycle"）
- 2023-11-09｜Hilary Maxson｜guidance：現金流 2024 年 40 億歐元目標維持（原話："the EUR 4 billion ambition by 2024"）
- 2023-11-09｜Hilary Maxson｜guidance：產品商業模式 2024–2027 年成長中高個位數（原話："growth of mid- to high single digit from 2024 to 2027"）
- 2023-11-09｜Hilary Maxson｜guidance：系統業務 2027 前預期雙位數成長（原話："we'll see double-digit growth in this business model"）
- 2023-11-09｜Hilary Maxson｜guidance：系統業務積壓訂單延伸到 2025（原話："backlog in the systems business model now extends into 2025"）
- 2023-11-09｜Hilary Maxson｜guidance：軟體與服務預期雙位數成長（原話："expect double-digit growth in both of those business models"）
- 2023-11-09｜Hilary Maxson｜guidance：數位飛輪占營收 2027 年達 60%–65%（原話："stepping up to 60% to 65% of our total revenues by 2027"）
- 2023-11-09｜Hilary Maxson｜guidance：agnostic 軟體經常性收入 2027 年約 80%（原話："agnostic software to around 80% by 2027"）
- 2023-11-09｜Hilary Maxson｜guidance：法國與歐洲成長預期低於集團其餘部分（原話："grow at a relatively lower pace than the rest"）
- 2023-11-09｜Hilary Maxson｜margin：淨價格（net price）口徑：產品價格加總減原料指數（原話："the sum of all the price that we put on our products"）
- 2023-11-09｜Hilary Maxson｜margin：過去多年淨價格貢獻毛利率約 30bp（原話："around 30 basis points average improvements"）
- 2023-11-09｜Hilary Maxson｜margin：工業生產力 2024–2027 預期為強勁貢獻（原話："a strong contributor for us between '24 and '27"）
- 2023-11-09｜Hilary Maxson｜margin：系統成長快於產品，預期對毛利結構負面但幅度較小（原話："growth in systems to negatively impact our mix"）
- 2023-11-09｜Hilary Maxson｜margin：系統與集團毛利率差距自 2016 年已縮小逾 1/3（原話："this difference has decreased by more than 1/3 since 2016"）
- 2023-11-09｜Hilary Maxson｜margin：系統業務 OpEx 密度較低，EBITA 層級緩衝更強（原話："the systems business is less OpEx-intensive"）
- 2023-11-09｜Hilary Maxson｜margin：SFC／銷售比預期下降（原話："a reduction in our SFC to sales ratio between '24 to '27"）
- 2023-11-09｜Hilary Maxson｜margin：研發占銷售由約 5.7% 提高到 2027 年約 7%（原話："we expect that to step up to around 7% by 2027"）
- 2023-11-09｜Hilary Maxson｜margin：自身永續投資約 4 億歐元至 2030（原話："around EUR 400 million in our own sustainability journey"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：增量資本支出約 20 億歐元（2024–2027）（原話："CapEx around EUR 2 billion to support growth"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：有形資本支出維持占銷售 2%–2.5%（原話："remain in a range of around 2% to 2.5%"）
- 2023-11-09｜Hilary Maxson｜guidance：ROCE 目標 15% 以上（原話："our ROCE towards 15% plus in the next few years"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：庫藏股改為只對沖員工股權計畫（原話："buy back shares to neutralize employee share plans"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：近期無轉型性併購或處分（原話："don't see any transformative transactions in the near term"）
- 2023-11-09｜Peter Herweck｜capital_allocation：CEO：議程上無轉型性併購（原話："no transformational M&A on my current agenda"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：連續 13 年累進股利，列為優先順位（原話："maintained a progressive dividend for the past 13 years"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：槓桿預期從 OSI／AVEVA 少數股權後的高點下降，不給具體數字（原話："decrease versus the level of leverage that we have today"）
- 2023-11-09｜Hilary Maxson｜capital_allocation：若有多餘現金，不排除以特別股息或買回形式返還（原話："not averse to giving that back in some form"）
- 2023-11-09｜Hilary Maxson｜commitment：「Company of 25」為跨週期目標（成長＋EBITA 率）（原話："a sum of our organic growth and adjusted EBITA margin"）
- 2023-11-09｜Peter Herweck｜commitment：CEO 承諾延續性與嚴格執行（原話："what I will promise you a stringent execution"）
- 2023-11-09｜Hilary Maxson｜commitment：2021 資本市場日承諾達標進度：在軌（原話："we're well on track to meet these commitments"）
- 2023-11-09｜Peter Herweck｜guidance：CEO 表示今天不談 2024 財測，之後公布（原話："not the day to talk about the '24 guidance"）
- 2023-11-09｜Peter Herweck｜guidance：CEO：部分市場未來數季偏慢甚至轉負，其他雙位數（原話："certain areas will be a little bit slower"）
- 2023-11-09｜Hilary Maxson｜guidance：7–10% 成長不假設價格是主要驅動（原話："haven't assumed that price would be an enormous driver"）
- 2023-11-09｜Peter Herweck｜risk：OEM 市場疲弱，始於中國，後延及歐洲部分市場（原話："OEM market shows some weaknesses predominantly started"）
- 2023-11-09｜Peter Herweck｜risk：CEO 預期此輪 OEM 週期歷時數季（原話："cycles have traditionally had a certain period"）
- 2023-11-09｜Peter Herweck｜risk：CEO 承認市場有波動（原話："there are some volatilities in the market"）
- 2023-11-09｜Peter Herweck｜risk：AI 熱潮能持續多久無法預測（原話："I don't have the glass ball"）
- 2023-11-09｜Aamir Paul｜risk：美國 IRA 資金流經聯邦到州再到市，大案進度較慢（原話："Now those tend to move a little bit slower."）
- 2023-11-09｜Peter Herweck｜customer：資料中心占集團 19%，稱不爭議第一（原話："19% of the group, undisputed #1 position"）
- 2023-11-09｜Peter Herweck｜customer：資料中心過去數年成長高於市場（原話："it will continue to be a double-digit growth market"）
- 2023-11-09｜Christopher Crosby｜customer：Compass 簽 30 億美元多年期電力中心單元供貨協議（原話："$3 billion multiyear agreement for supply"）
- 2023-11-09｜Christopher Crosby｜customer：Compass 預期含預測維護服務合約毛利高（原話："which we expect to be very high margin for them"）
- 2023-11-09｜Aamir Paul｜customer：Compass 合約為 5 年期，資料中心可見度為史上最高（原話："highest visibility we've ever had on data centers"）
- 2023-11-09｜Peter Herweck｜customer：Compass 為既有客戶，合約是成長（原話："It's not a new customer. We've had them before."）
- 2023-11-09｜Aamir Paul｜customer：美國管線大案增加，案件規模變大（原話："the deal sizes are getting larger"）
- 2023-11-09｜Kathleen Mazzarella｜customer：Graybar 稱 Schneider 為其最大供應商（原話："Graybar's largest supplier"）
- 2023-11-09｜Peter Herweck｜customer：通路夥伴約貢獻 60% 營收（原話："It creates and it turns roughly 60% of our revenue."）
- 2023-11-09｜Nicole Dezen｜customer：Microsoft 與 Schneider 簽訂供應鏈確定性協議（原話："agreement ensuring supply chain certainty"）
- 2023-11-09｜Amit Bhalla｜customer：電網業務占比高個位數（原話："high single-digit exposure for Schneider"）
- 2023-11-09｜Caspar Herzberg｜competition：AVEVA 高層對比整合型廠商：agnostic 擴張更快（原話："we scale better. We scale faster"）
- 2023-11-09｜Peter Herweck｜competition：分析師質疑 PLC 規模偏小，CEO 稱差距不大（原話："Yes, but not substantially."）
- 2023-11-09｜Peter Herweck｜competition：CEO 稱大型同業不太會加入開放自動化（原話："the very large ones, I wouldn't expect them to sign up"）
- 2023-11-09｜Olivier Pascal Blum｜competition：低壓業務規模為第二名 2 倍（原話："2x bigger than the second player in the market"）
- 2023-11-09｜Peter Herweck｜product：軟體定義自動化可能減少 PLC 硬體銷售、增加軟體（原話："we're going to be selling more software"）
- 2023-11-09｜Unknown Executive (Caspar Herzberg)｜product：Connect 平台已有 3 家外部公司承諾上線（原話："have committed to move on to this platform"）
- 2023-11-09｜Peter Herweck｜product：ETAP 為核能領域唯一獲認證軟體（原話："Every nuclear player we are talking to"）
- 2023-11-09｜Olivier Pascal Blum｜product：EcoCare 數位服務定位為下一個大型業務（原話："we love recurring revenues at Schneider"）
- 2023-11-09｜Caspar Herzberg｜product：AVEVA 稱按進度達管理層目標（原話："on track to meet the targets"）
- 2023-11-09｜Caspar Herzberg｜product：訂閱／SaaS 轉型對營收表現有影響，屬計畫內（原話："has an impact on the revenue performance"）
- 2023-11-09｜Caspar Herzberg｜product：AVEVA ARR 成長高於 15%（原話："annualized recurring revenue growth of above 15%"）
- 2023-11-09｜Caspar Herzberg｜product：agnostic 軟體營收約 19 億歐元（原話："just under EUR 2 billion, EUR 1.9 billion"）
- 2023-11-09｜Hilary Maxson｜guidance：AVEVA 訂閱轉型的大額衝擊預期 2026–2027 結束（原話："through the big impacts in terms of revenue"）
- 2023-11-09｜Barbara Frei｜product：馬達管理業務 15 年內成長 3 倍（原話："this business has tripled over the last 15 years"）

### SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20250507.md
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO重申2025年調整後EBITDA有機成長區間（原話："organic growth of adjusted EBITDA between 10% and 15%"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO拆解EBITDA成長的營收成長區間（原話："organic revenue growth between 7% and 10%"）
- 2025-05-07｜CFO Hilary Maxson｜margin：CFO拆解2025年調整後EBITDA margin有機增幅區間（原話："adjusted EBITDA margin between 50 and 80 basis points"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO說離散自動化需求復甦、銷售成長偏重下半年（原話："sales growth weighted towards the second half of the year"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO說軟體與服務預期不變，AVEVA年化經常性收入雙位數成長（原話："annualized recurring revenues at AVEVA"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO談離散自動化市場預期復甦（原話："a recovery in demand in the Discrete automation market"）
- 2025-05-07｜CFO Hilary Maxson｜margin：CFO報告2024年調整後EBITDA margin創高（原話："record adjusted EBITDA margin of 18.6%"）
- 2025-05-07｜CFO Hilary Maxson｜margin：CFO報告ROCE 2024年水準與目標（原話："Now at 14.8%, well on track towards our goal of 15%-plus."）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO報告能源管理2024年營收規模（原話："Energy management achieved EUR 31 billion revenues"）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO報告工業自動化2024年有機衰退（原話："an organic decline of 4%"）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO報告系統業務占比與成長（原話："which represent 31% of sales in 2024 and grew 19% organic"）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO說產品業務尚未回到成長（原話："not yet returning to growth overall"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO報告2025Q1能源管理成長（原話："up 10% organic in the first quarter"）
- 2025-05-07｜CFO Hilary Maxson｜product：CFO報告2025Q1工業自動化持平（原話："Industrial Automation was around flat during the quarter"）
- 2025-05-07｜CFO Hilary Maxson｜risk：CFO談關稅，稱已在採取因應措施（原話："already taking measures to counter the impacts of tariffs"）
- 2025-05-07｜CEO Olivier Blum｜risk：CEO談關稅對營業利益率的因應是調價（原話："we would work on the pricing in the regions concerned"）
- 2025-05-07｜CEO Olivier Blum｜risk：CEO說明在地化供應鏈目標（原話："90% of our supply chain needs to come from the region"）
- 2025-05-07｜CFO Hilary Maxson｜risk：CFO說明股價下跌原因之一為美元貶值（原話："a big degradation of the U.S. dollar"）
- 2025-05-07｜CFO Hilary Maxson｜risk：CFO說資料中心成長預期分歧影響股價（原話："low double digit and super high double digits"）
- 2025-05-07｜CFO Hilary Maxson｜guidance：CFO在Q&A表示對2025財測有信心（原話："We feel very confident in the 2025 guidance, 7% to 10%."）
- 2025-05-07｜CEO Olivier Blum｜commitment：數位化營收占比現況（原話："We reached 57% of digital offering, 57% of our revenue."）
- 2025-05-07｜CEO Olivier Blum｜commitment：CEO談數位化中期目標（同篇另有60%–65%的說法）（原話："medium-term target, which is around 70% of digitalization"）
- 2025-05-07｜CEO Olivier Blum｜commitment：CEO談2027年數位化營收占比目標（原話："60% to 65% of group revenues by 2027"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜commitment：董事長重申投資人日的自由現金流轉換目標（原話："conversion of free cash flow of 100% on average year-on-year"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜capital_allocation：董事長報告股利與連續增加年數（原話："a dividend of EUR 3.90 per share, an increase of 11%"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜capital_allocation：董事長指出連續第15年增加股利（原話："15th year in a row of an increase of dividend"）
- 2025-05-07｜CFO Hilary Maxson｜capital_allocation：CFO列出資本配置第一優先為信用評等（原話："strong credit grade ratings as the first priority"）
- 2025-05-07｜CFO Hilary Maxson｜capital_allocation：CFO談併購態度（原話："cautiously opportunistic and agile regarding acquisitions"）
- 2025-05-07｜CEO Olivier Blum｜capital_allocation：CEO談遇到合適標的可加速執行併購（原話："if we find the right company at the right price"）
- 2025-05-07｜CEO Olivier Blum｜capital_allocation：CEO說明買Motivair的原因（原話："that's why we bought Motivair"）
- 2025-05-07｜CEO Olivier Blum｜commitment：CEO確認7%–10%成長為有機成長（原話："that growth would be organic"）
- 2025-05-07｜CEO Olivier Blum｜competition：CEO說明客戶向NVIDIA推薦施耐德的理由（原話："most advanced portfolio of technologies"）
- 2025-05-07｜CEO Olivier Blum｜customer：CEO以Capgemini為案例，節能成果（原話："They saved 30% in energy consumption"）
- 2025-05-07｜CEO Olivier Blum｜customer：CEO說明Capgemini服務合約帶來經常性收入（原話："Capgemini will be paying us every year"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜product：董事長說明StarCharge合資在歐洲的獨家權（原話："exclusivity in developing these technologies in Europe"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜risk：董事長說明資料中心占全球用電比重（原話："only 0.4% of the world's electricity consumption"）
- 2025-05-07｜CEO Olivier Blum｜risk：CEO回應美國ESG壓力：大型美企仍重視淨零（原話："continue to have a powerful focus on their net 0 targets"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜risk：董事長說明美國CSR招標規則僅政府合約有變（原話："The only change has been for government contracts"）
- 2025-05-07｜Chairman Jean-Pascal Tricoire｜risk：董事長說明美國業務約80%不受影響（原話："About 80% of what we do in the States, nothing has changed"）
- 2025-05-07｜CEO Olivier Blum｜risk：CEO談印度–巴基斯坦衝突的可能影響（原話："our ambitions remain untouched"）
- 2025-05-07｜Vice-Chairman Manfred Kindle｜risk：董事會主席說明前CEO的非競業與資遣補償（原話："a non-compete indemnity and also to a severance indemnity"）
- 2025-05-07｜Vice-Chairman Manfred Kindle｜commitment：董事會提議調高CEO總薪酬（原話："an increase in total compensation for the CEO"）
- 2025-05-07｜CEO Olivier Blum｜product：CEO稱工業自動化已見低點（原話："I think we've reached the low point"）
- 2025-05-07｜CEO Olivier Blum｜competition：CEO稱未流失市占（原話："We did not lose any market share"）
- 2025-05-07｜CEO Olivier Blum｜guidance：CEO報告2024營收成長與規模（原話："we attained 8.4% revenue growth, EUR 38 billion"）

### SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md
- 2025-12-11｜CEO Olivier Blum｜guidance：CEO 說下一個週期可達 7%～10% 的持續成長。（原話："a sustained growth of 7% to 10%"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：CFO 將 7%～10% CAGR 的差異化成長目標延伸到 2030 年。（原話："differentiated growth target of 7% to 10% CAGR"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：CFO 估計可觸及市場到 2030 年年增 6%～7%。（原話："will grow between 6% and 7% between now and 2030"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：純資料中心這塊 2025～2030 年預期年複合成長 12%～14%。（原話："to grow 12% to 14% CAGR between 2025 and 2030"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：資料中心與網路整體預期成長超過 10%。（原話："still greater than 10% growth expected there"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：其他終端市場成長預期：建築與工業 4%～5%，基礎設施 5%～7%。（原話："industry at 4% to 5% and infrastructure at 5% to 7%"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：揭露每百萬瓦資料中心對公司的商機區間，並說明最複雜的 AI 資料中心不預期落在區間高端。（原話："$1.2 million to $3.3 million per megawatt"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：同一段中，CFO 表示 AI 資料中心每百萬瓦金額不預期走到區間頂端。（原話："we wouldn't expect to trend to the top of that range"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：預期中國在這個週期朝中個位數成長。（原話："China to be trending towards mid-single-digit growth"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：依商業模式拆解：產品中高個位數成長（系統與軟體服務另述）。（原話："products to grow mid-single digit to high single digit"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：CFO 說明終端市場拆分是用年底訂單簿預測，並說明為何公布訂單而非營收。（原話："best indicator of what the upcoming sales are looking like"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：電網在基礎設施終端市場中占大宗，對集團的曝險約為高個位數百分比。（原話："probably high single digit in terms of exposure with the group"）
- 2025-12-11｜CFO Hilary Maxson｜guidance：建築市場因住宅拖累而延後，現在預期 4%～5% 的終端市場成長。（原話："we now expect that 4% to 5% end market growth"）
- 2025-12-11｜CEO Olivier Blum｜guidance：CEO 描述工業自動化市場 2025 年是逐步復甦的一年。（原話："was a year of step-by-step recovery in the IA market"）
- 2025-12-11｜Aamir Paul (North America)｜guidance：北美銷售團隊稱電力鏈公司目前對資料中心的確定可見度為 12～18 個月。（原話："So we have visibility for 12 to 18 months"）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 承諾調整後 EBITA 利潤率在 2026～2030 年有機擴張 250 個基點。（原話："another plus 250 basis points organic expansion"）
- 2025-12-11｜CFO Hilary Maxson｜margin：被問到 250 個基點是否前低後高，CFO 回答不要多解讀、也不是後段集中。（原話："Nothing back-end loaded."）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 說明 250 個基點的時間分布大致可假設為線性。（原話："you could assume somewhat linear over that time frame"）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 解釋改用「加 250 基點」而非「每年 50 基點 CAGR」的表述原因。（原話："plus 250 a bit little better than the 50 CAGR"）
- 2025-12-11｜Gwenaelle Avice-Huet (Industrial Automation)｜margin：工業自動化事業負責人給出利潤率目標：2028 年回到 18%。（原話："the margin ambition is to get back to 18% by 2028"）
- 2025-12-11｜Caspar Herzberg (AVEVA)｜margin：AVEVA 主管說隨訂閱轉型拖累淡出，利潤率將朝 30% EBITDA 邁進。（原話："moving towards 30% EBITDA over the coming years"）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 給出 AVEVA 調整後 EBITA 利潤率 2028 年約 30% 的口徑。（原話："strong adjusted EBITA margins of around 30% by 2028"）
- 2025-12-11｜CFO Hilary Maxson｜margin：管理層點出毛利率路徑不如 EBITA 利潤率平順，內部要加強毛利率管理。（原話："driving an obsession with gross margin"）
- 2025-12-11｜CFO Hilary Maxson｜margin：工業生產力節省目標：2026 年起這個週期 20～25 億歐元。（原話："industrial productivity of EUR 2 billion to EUR 2.5 billion"）
- 2025-12-11｜CFO Hilary Maxson｜margin：CFO 承認今年的定價相對通膨偏慢。（原話："We've been a bit slow this year in terms of pricing"）
- 2025-12-11｜CFO Hilary Maxson｜margin：未來五年的定價目標：淨定價持平到正向，以完全抵銷關稅與通膨影響。（原話："an ambition of flat to positive net pricing"）
- 2025-12-11｜CFO Hilary Maxson｜risk：CFO 表示未來五年很可能面臨通膨，且關稅更難預測。（原話："some more unpredictability in terms of tariffs"）
- 2025-12-11｜CFO Hilary Maxson｜margin：毛利率層面預期持續受到負面組合影響，主要在調整後 EBITA 層面抵銷。（原話："we expect to continue to have negative gross margin impacts"）
- 2025-12-11｜CFO Hilary Maxson｜margin：系統業務稀釋毛利率，但在調整後 EBITA 利潤率層面已接近中性。（原話："systems are already around neutral to our adjusted EBITA margin"）
- 2025-12-11｜CFO Hilary Maxson｜margin：軟體在調整後 EBITA 層面預期在這個週期轉為加分。（原話："software to become accretive at the adjusted EBITA level"）
- 2025-12-11｜Caspar Herzberg (AVEVA)｜margin：AVEVA 經常性收入占比與毛利率口徑。（原話："has reached 85% of this business"）
- 2025-12-11｜Caspar Herzberg (AVEVA)｜margin：AVEVA 預期營收與 ARR 成長將趨於收斂。（原話："revenue and ARR growth will start to converge"）
- 2025-12-11｜Caspar Herzberg (AVEVA)｜product：AVEVA 揭露客戶流失與留存指標。（原話："low churn of less than 2% and 110% retention rate"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：研發費用占營收比重逐步提高到約 7%。（原話："move our R&D as a percentage of sales to around 7%"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：資本支出約占營收 2.5%，前幾年達到高峰。（原話："invest around 2.5% of our group revenues in CapEx"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：CFO 說明資本支出領先需求 18～24 個月投入。（原話："we're investing now 18 to 24 months in advance of the demand cycle"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：銷售與行政等費用占營收比（不含研發）目標下降 1.5～2 個百分點。（原話："SFC to sales ratio down by 1.5 to 2 points"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：2025 年重組費用約 3 億歐元，並預期到 2027 年有額外重組費用。（原話："restructuring of around EUR 300 million in 2025"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：自由現金流轉換率目標約 100%（占淨利）。（原話："around 100% free cash conversion ratio"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：ROCE 目標上調為 15%～20%。（原話："upgraded our ambition for ROCE growth to between 15% and 20%"）
- 2025-12-11｜CEO Olivier Blum｜commitment：2030 年數位飛輪占營收超過 70%。（原話："More than 70% of our revenue should come from the flywheel"）
- 2025-12-11｜CEO Olivier Blum｜commitment：軟體與服務占集團營收目標 25%。（原話："25% of our group revenue being made of software and services"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：經常性收入占比到 2030 年加倍。（原話："contractual recurring revenues by 2030"）
- 2025-12-11｜CEO Olivier Blum｜commitment：供應鏈在地化目標：每個區域 90% 銷售商品為當地製造或採購。（原話："in every region, 90% of what we sell is made sourced locally"）
- 2025-12-11｜CFO Hilary Maxson｜commitment：自 2026 年第一季起改用新區域口徑報告。（原話："intend to start reporting on in Q1 of 2026"）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：未來五年股票回購計畫 25～35 億歐元，並稱會比近年更有系統。（原話："EUR 2.5 billion to EUR 3.5 billion in share buyback"）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：信用評等目標明確化為維持 A 級類別。（原話："retain category A credit ratings over this next 5 years"）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：股利政策維持累進，已連續 15 年。（原話："paid a progressive dividend now for 15 years in a row"）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：首次設定處分目標：到 2030 年處分 10～15 億歐元營收的資產。（原話："EUR 1 billion to EUR 1.5 billion revenue disposal"）
- 2025-12-11｜CEO Olivier Blum｜capital_allocation：CEO 說明處分屬例行修剪，不預期有大案。（原話："Don't expect any big things"）
- 2025-12-11｜CEO Olivier Blum｜capital_allocation：CEO 說所有中期目標均為有機成長，不含併購。（原話："all the ambition that we are giving to you today are organic"）
- 2025-12-11｜CEO Olivier Blum｜capital_allocation：CEO 表示目前不計畫大型收購。（原話："We don't plan any major acquisition at that point of time."）
- 2025-12-11｜CFO Hilary Maxson｜capital_allocation：CFO 回應若做大型併購 ROCE 目標是否成立：稱 15%～20% 在五年內仍有把握。（原話："we feel comfortable with over the 5-year time frame"）
- 2025-12-11｜CEO Olivier Blum｜capital_allocation：印度 Lauritz Knudsen 收購已獲印度競爭委員會核准，預計年底前完成。（原話："close the acquisition before the end of this year"）
- 2025-12-11｜Aamir Paul (North America)｜customer：與 Switch 的資料中心整合模組方案，單筆金額 19 億美元。（原話："that particular deal was $1.9 billion"）
- 2025-12-11｜David Howson (Vantage Data Centers)｜customer：Vantage 表示已與公司簽訂長期供應產能協議。（原話："long-term supply capacity agreements with Schneider"）
- 2025-12-11｜Aamir Paul (North America)｜customer：與 Vantage 的業務規模約為過去的十倍。（原話："almost 10x larger than it used to be"）
- 2025-12-11｜CEO Olivier Blum｜customer：CEO 描述與大型客戶的新型承諾式合約：客戶承諾採購量，公司承諾產能。（原話："commit on a certain number of capacity we'll give to them"）
- 2025-12-11｜Noelle Walsh (Microsoft)｜customer：微軟代表稱公司為關鍵且具策略性的供應商。（原話："We view Schneider as a critical and strategic supplier."）
- 2025-12-11｜Unknown Executive｜risk：高管提到大型客戶的建置節奏會調整，去年微軟曾放慢。（原話："as you saw with Microsoft last year, they'll slow things down"）
- 2025-12-11｜Aamir Paul (North America)｜customer：Compass 案例：資料中心連網監控帶來現場事件與資本支出下降。（原話："a 40% reduction in on-site events"）
- 2025-12-11｜Guillaume Texier (Rexel)｜customer：通路夥伴 Rexel 預期定價環境支持價格上漲（為分銷商觀點）。（原話："price appreciation over the next few years"）
- 2025-12-11｜CEO Olivier Blum｜risk：CEO 承認 2025 年是定價的過渡年。（原話："25 years has been a bit of a year of transition"）
- 2025-12-11｜CEO Olivier Blum｜risk：CEO 說中國市場通縮，限制了正向定價的能力。（原話："the capacity to deliver positive pricing is very limited"）
- 2025-12-11｜CEO Olivier Blum｜risk：CEO 說明關稅反覆期間，公司花了數週到數月才決定定價。（原話："a couple of weeks, months to really take stock"）
- 2025-12-11｜Laurent Bataille (Europe)｜risk：歐洲區主管承認歐洲在 AI 與資料中心相關成長上落後。（原話："Europe has probably missed in terms of growth potential"）
- 2025-12-11｜Aamir Paul (North America)｜risk：北美住宅在疫後強勁後目前承壓。（原話："that is more challenged right now"）
- 2025-12-11｜Aamir Paul (North America)｜risk：墨西哥因 USMCA 談判目前偏軟。（原話："Mexico is softer a little bit for us right now"）
- 2025-12-11｜Aamir Paul (North America)｜risk：美國電工人力缺口被點名為資料中心擴張的限制之一。（原話："There are roughly about 600,000 electricians in the U.S."）
- 2025-12-11｜Frederic Godemel｜competition：被問到固態變壓器（SST），資料中心技術長說 2027 年前不預期大規模新技術。（原話："Up to 2027, we don't see at large new technology like SST"）
- 2025-12-11｜Gwenaelle Avice-Huet (Industrial Automation)｜competition：工業自動化負責人承認 PLC 不是領先位置，策略上刻意轉向虛擬 PLC 與軟體定義自動化。（原話："the areas where we are not the leaders, PLC."）
- 2025-12-11｜Gwenaelle Avice-Huet (Industrial Automation)｜competition：工業自動化策略強調選擇性，與競爭者合作推動開放標準。（原話："even with competition to impose standards"）
- 2025-12-11｜CFO Hilary Maxson｜competition：CFO 稱公司是資料中心與網路的市場領導者並打算維持。（原話："we are clearly the market leader, and we intend to remain so"）
- 2025-12-11｜Frederic Godemel｜product：預告明年推出的馬達控制中心新方案，可節省最多 80% 空間。（原話："up to 80% of space saving"）
- 2025-12-11｜Frederic Godemel｜product：軟體定義中壓架構可大幅縮短訂購與設計時間。（原話："accelerate 3x the time to order and design"）
- 2025-12-11｜David Howson (Vantage Data Centers)｜product：Vantage 表示 800 伏特直流技術預計 2028～2030 年才會部署。（原話："until 2028, 2029, 2030"）
- 2025-12-11｜Frederic Godemel｜product：服務業務：公司估計目前服務的裝置基數比例，並預期服務持續雙位數成長。（原話："we serve around 16% of our asset"）
- 2025-12-11｜Frederic Godemel｜product：服務業務下個週期預期維持雙位數成長。（原話："to keep growing double digit this business"）
- 2025-12-11｜Rich Whitmore (Motivair)｜product：Motivair 於今年 3 月被收購，目前正推動全球產能工業化。（原話："we were acquired in March this year"）
- 2025-12-11｜Gwenaelle Avice-Huet (Industrial Automation)｜product：EcoStruxure Automation Expert 已部署站點數。（原話："Today, we have 550 sites deployed with EAE"）
- 2025-12-11｜CEO Olivier Blum｜commitment：組織效率：CEO 說明不會有大規模重組，但會逐步減少領導層人數。（原話："we are not going through massive restructuring"）
- 2025-12-11｜CEO Olivier Blum｜commitment：CEO 說將逐步精簡領導層。（原話："we are going to reduce step-by-step the number of leaders that we have"）
- 2025-12-11｜CEO Olivier Blum｜commitment：被問到薪酬與 KPI 是否調整，CEO 說薪酬制度不變。（原話："nothing that we are changing on compensation"）

### SU.PA_2026_20260730.md
- 2026-07-30｜Olivier Blum (CEO)｜guidance：全年營收有機成長財測上調（原話："from 7% to 10% to 10% to 13% organic"）
- 2026-07-30｜Olivier Blum (CEO)｜guidance：全年調整後 EBITA 利潤率改善幅度財測上調（原話："from 50 to 80 bps to 70 to 100 bps by the end of the year"）
- 2026-07-30｜Olivier Blum (CEO)｜guidance：調整後 EBITA 有機改善的區間說法（原話："between 14% and 19% of organic improvement of adjusted EBITA"）
- 2026-07-30｜Nathan Fast (CFO)｜guidance：CFO 預期全年匯率對營收的影響（原話："minus EUR 450 million to minus EUR 500 million on revenues"）
- 2026-07-30｜Nathan Fast (CFO)｜guidance：CFO 預期全年現金轉換率（原話："cash conversion ratio to be around 100% for full year"）
- 2026-07-30｜Nathan Fast (CFO)｜guidance：重組費用預期今年見頂（原話："restructuring charges of around EUR 450 million this year"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：上半年毛利率數字（原話："gross margin of 42.5%, up 10 bps"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：Q2 價格對產品業務成長的貢獻口徑（原話："represent approximately 4 points of product growth in Q2"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：毛利率橋中含關稅退款一次性項目（原話："around EUR 100 million coming from tariff refunds in Q2"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：CFO 提醒生產力下半年基期較高（原話："more than 70% of our full year 2025 productivity in H2"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：系統業務成長使毛利率結構轉差（原話："Mix was negative in gross margin as expected"）
- 2026-07-30｜Nathan Fast (CFO)｜margin：支援職能費用占銷售比改善幅度（原話："SFC to sales ratio improving by 1.1 points"）
- 2026-07-30｜Olivier Blum (CEO)｜margin：管理層說明下半年若價格貢獻重現可抵銷原料與關稅衝擊（原話："if we are able to repeat that in H2"）
- 2026-07-30｜Nathan Fast (CFO)｜commitment：工業自動化利潤率回復目標重申（原話："on track to our 18% by 2028"）
- 2026-07-30｜Nathan Fast (CFO)｜commitment：對長期生產力節奏的回答：不會線性延續（原話："the same linear over a 5-year period? Probably not"）
- 2026-07-30｜Olivier Blum (CEO)｜commitment：今年不增加人力、嚴控 SG&A（原話："not increasing our headcount this year"）
- 2026-07-30｜Olivier Blum (CEO)｜capital_allocation：股利政策連續年數（原話："progressive since 16 years"）
- 2026-07-30｜Olivier Blum (CEO)｜capital_allocation：上半年已執行的庫藏股金額（原話："already EUR 250 million that have been repurchase"）
- 2026-07-30｜Olivier Blum (CEO)｜capital_allocation：回答 M&A 問題：成長主要來自內生（原話："most of it will come organically"）
- 2026-07-30｜Olivier Blum (CEO)｜capital_allocation：CEO 描述 Cognite 收購的定位（原話："it's the brain of the next cycle of Schneider"）
- 2026-07-30｜Olivier Blum (CEO)｜product：資料中心新架構（固態變壓器電力中心）研發進度（原話："power center with new SST solution that we have developed"）
- 2026-07-30｜Nathan Fast (CFO)｜product：系統業務 Q2 成長數字與驅動（原話："sales of 28% growth driven by data center"）
- 2026-07-30｜Olivier Blum (CEO)｜product：與 Foxconn 合作擴充北美預製化產能，並提及產業放緩情境（原話："mitigate potential not, I would say, decline, but slowdown"）
- 2026-07-30｜Olivier Blum (CEO)｜competition：CEO 回應競爭與資料中心整合方案執行風險：已增加安全庫存（原話："we increased our safety stock in all those components"）
- 2026-07-30｜Olivier Blum (CEO)｜risk：資料中心市場可能受零組件與記憶體限制（原話："constrained sometimes by component, by memory"）
- 2026-07-30｜Nathan Fast (CFO)｜risk：中東情勢被列為下半年挑戰（原話："we see this as a challenge in H2 2026"）
- 2026-07-30｜Olivier Blum (CEO)｜risk：CEO 對資料中心執行的保留語氣（原話："the world is so unpredictable that you can have always issue"）
- 2026-07-30｜Olivier Blum (CEO)｜customer：資料中心客戶基礎與預測方式（原話："work with 200 customers in the world"）
- 2026-07-30｜Olivier Blum (CEO)｜customer：客戶選擇標準：重視長期合作與經濟條件（原話："customers that wants to build a long-term partnership"）
- 2026-07-30｜Olivier Blum (CEO)｜customer：中國需求結構：建築與住宅仍慢，並已降低曝險（原話："we reduced drastically our exposure"）
- 2026-07-30｜Olivier Blum (CEO)｜customer：CEO 描述需求來源的敘事：由資料中心擴及所有終端市場（原話："we see all segments contributing"）

### SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md
- 2026-10-05｜Nathan Fast (CFO)｜guidance：CFO 給出成本綜效 2.5 億歐元、3 年內實現（原話："EUR 250 million of cost synergies to be generated"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：一次性整合成本約 2.5 億歐元（原話："EUR 250 million of onetime implementation costs"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：營收綜效 8 億歐元，由三個槓桿構成（原話："EUR 800 million of revenue synergies clearly defined"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：營收綜效時程：交割後不久開始、中期線性實現（原話："delivered linear over the midterm"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：交易價值：PTC 100% 現金收購、企業價值約 210 億歐元（原話："implying approximately EUR 21 billion of enterprise value"）
- 2026-10-05｜Nathan Fast (CFO)｜margin：估值倍數口徑：含完整綜效約 13 倍調整後 EBITDA（原話："valued at approximately 13x adjusted EBITDA"）
- 2026-10-05｜Nathan Fast (CFO)｜margin：2027 調整後 EBITA 倍數隨綜效下降的分段口徑（原話："21x before synergies to 17x with cost synergies"）
- 2026-10-05｜Nathan Fast (CFO)｜margin：PTC 綜效前毛利率與調整後 EBITA 利潤率（原話："85% gross margin and 40% adjusted EBITA margin"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：PTC 中期有機 ARR 與營收 CAGR 約 10%（原話："10% organic ARR and revenue CAGR in the medium term"）
- 2026-10-05｜Nathan Fast (CFO)｜margin：PTC 現金轉換率高於 100%（原話："PTC cash conversion is above 100%"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：調整後 EPS（PPA 前）第一年增厚：未計完整綜效為低個位數（原話："immediately accretive to adjusted EPS before PPA in year 1"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：交易 ROCE 第 5 年超過 WACC（原話："the transaction ROCE is expected to exceed the WACC"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：集團 ROCE 於交割後 1 年內回到 15%–20%（原話："ROCE to be back in the 15% to 20% at a Schneider level"）
- 2026-10-05｜Nathan Fast (CFO)｜guidance：預計交割時點（CFO 口徑）（原話："We are expecting closing by Q3 2027."）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：股權融資規模 50–60 億歐元（原話："EUR 5 billion to EUR 6 billion of equity"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：新增優先債規模 160–170 億歐元（原話："EUR 16 billion to EUR 17 billion of senior debt"）
- 2026-10-05｜Nathan Fast (CFO)｜commitment：承諾維持 A 級信用評等（原話："a commitment to our category A credit rating"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：2030 庫藏股總額維持，但 2027、2028 暫停（原話："with some pause over 2027 and 2028"）
- 2026-10-05｜Nathan Fast (CFO)｜commitment：CFO 重申利潤率改善承諾（原話："We remain committed on the margin improvement"）
- 2026-10-05｜Nathan Fast (CFO)｜commitment：CFO 稱相對 CMD 承諾無改變，並自述併購紀律（原話："nothing changes versus those commitments from CMD"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：CFO 列舉併購篩選條件（原話："nothing changes versus those commitments"）
- 2026-10-05｜Olivier Blum (CEO)｜product：CEO 稱收購使可觸及的工業軟體市場放大 3 倍（原話："we multiply by 3, the accessible market"）
- 2026-10-05｜Olivier Blum (CEO)｜margin：合併後軟體與服務占集團營收口徑（以 2025 為基準）（原話："representing 24% of our group revenues"）
- 2026-10-05｜Olivier Blum (CEO)｜margin：合併軟體組合經常性收入占比（原話："89% of that portfolio being recurring"）
- 2026-10-05｜Olivier Blum (CEO)｜product：CEO 稱 Cognite 將成為集團能源管理的 AI 基礎（原話："Cognite will be definitely the AI foundation"）
- 2026-10-05｜Olivier Blum (CEO)｜competition：CEO 以開放、互通為差異化主軸（原話："we are open by design"）
- 2026-10-05｜Olivier Blum (CEO)｜competition：CEO 回應整合式硬軟體廠商 vs 純軟體廠商之爭，指客戶看待 Schneider 的方式已改變（原話："they don't perceive Schneider Electric today like it was"）
- 2026-10-05｜Olivier Blum (CEO)｜customer：CEO 描述客戶採購趨向整合、AI 化方案（原話："buying integrated, connected and AI-enabled solutions"）
- 2026-10-05｜Nathan Fast (CFO)｜product：CFO 談軟體定價：席位制與 flex credit 並存、保留兩種模式（原話："the seat and flex credit models are probably complementary"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：CFO 回應收購時點／估值：看長期內在價值而非當下股價（原話："their trading value at an arbitrary point in time"）
- 2026-10-05｜Olivier Blum (CEO)｜risk：整合風險：CEO 稱人才留任是首要事項（原話："retention of people is an absolute priority"）
- 2026-10-05｜Olivier Blum (CEO)｜risk：CFIUS 等監管審批：CEO 稱不預期重大問題（原話："we don't expect any major issue"）
- 2026-10-05｜Nathan Fast (CFO)｜risk：被問及競標／第三方介入，CFO 表示不就假設性情境表態（原話："not going to speculate on what type of interlopers"）
- 2026-10-05｜Nathan Fast (CFO)｜capital_allocation：股權與債務置換時點尚未決定（原話："we haven't decided exact timing of those yet"）
- 2026-10-05｜Olivier Blum (CEO)｜competition：敘事變化：CEO 稱工業自動化不是獨立事業，須與其他產品組合一起看（原話："Industrial Automation is not a stand-alone business"）
- 2026-10-05｜Olivier Blum (CEO)｜margin：CEO 提到工業自動化單獨報告時仍須展現獲利反轉（原話："has also to demonstrate a turnaround in profitability"）
- 2026-10-05｜Olivier Blum (CEO)｜commitment：CEO 說明交割前兩家公司獨立營運、交割後單一軟體載體單一領導（原話："continue to operate in post-closing with one software"）

### SU.PA_Schneider_Electric_S_E_Q3_2026_Sales_Trading_Statement_Call_Oct_16_2026_20261016.md
- 2026-10-16｜Olivier Blum｜guidance：CEO 宣布 2026 全年目標第二次上調（營收與調整後 EBITA margin）（原話："we are upgrading for the second time in 2026"）
- 2026-10-16｜Olivier Blum｜guidance：全年有機營收成長目標 12%–14%（原話："between 12% and 14% organically"）
- 2026-10-16｜Olivier Blum｜margin：全年調整後 EBITA margin 隱含約 19.7%–19.9%（有機 +100 至 +120bps）（原話："adjusted EBITA margin of around 19.7% to 19.9%"）
- 2026-10-16｜Nathan Fast｜margin：匯率對全年 margin 影響預期可忽略（原話："negligible impact in adjusted EBITA margin for the full year"）
- 2026-10-16｜Nathan Fast｜margin：管理層預期 2026 年以價格行動以價值計抵銷原物料與關稅逆風（原話："expect to offset in value for 2026 the headwinds"）
- 2026-10-16｜Nathan Fast｜margin：Q3 產品價格貢獻金額與整個上半年相當（原話："product pricing in Q3 around the same level in value"）
- 2026-10-16｜Nathan Fast｜guidance：全年區間上調同時收窄，說明為信心與能見度提高（原話："we have also narrowed the range"）
- 2026-10-16｜Nathan Fast｜guidance：CFO 回應 Q4 隱含放緩：基期為 2025 年最強季度之一（原話："the baseline was the strongest quarter in 2025"）
- 2026-10-16｜Nathan Fast｜product：資料中心需求再一季三位數成長（原話："another quarter of triple digit demand growth in Q3"）
- 2026-10-16｜Nathan Fast｜product：預製化（prefab）占比不揭露，僅稱成長極強（原話："we don't give the exact split of the prefab business"）
- 2026-10-16｜Nathan Fast｜product：AVEVA ARR 與 Q3 有機成長均約 10%（原話："AVEVA's ARR and Q3 organic sales growth both at around 10%"）
- 2026-10-16｜Nathan Fast｜customer：Q4 預期趨勢中，成長國家新增中國（原為美國、印度）（原話："we add China alongside U.S. and India"）
- 2026-10-16｜Olivier Blum｜customer：CEO 稱與客戶討論後，中國成長水準至少可延續至 2027（原話："this level of growth could continue at least across '27"）
- 2026-10-16｜Olivier Blum｜customer：年初對中國需求是否短期現象較為保守（敘事與當時不同）（原話："we were a bit more cautious in our answer"）
- 2026-10-16｜Olivier Blum｜customer：CEO 說明客戶選擇上高度挑剔（技術共同設計、財務能力）（原話："we are extremely careful to select those company"）
- 2026-10-16｜Nathan Fast｜customer：去年底資料中心與網路占營收 30%，今年預期集中度上升（原話："was 30% on data center and networks"）
- 2026-10-16｜Olivier Blum｜competition：中國通路優勢：最大夥伴網絡（原話："we are the largest network of partner in the country"）
- 2026-10-16｜Nathan Fast｜competition：800V 等技術轉向目前客戶端尚未提出疑問（原話："we have not had a question on 800 volt"）
- 2026-10-16｜Nathan Fast｜capital_allocation：持續於區域據點擴充產能（含液冷，與 Foxconn 合作）（原話："capacity investments across our regional hubs"）
- 2026-10-16｜Nathan Fast｜risk：住宅端貢獻不及其他板塊（原話："residential has not matched the level of the other segments"）
- 2026-10-16｜Nathan Fast｜risk：工業自動化 Process 與 Hybrid 成長仍疲弱（原話："Sales growth in Process and Hybrid remains subdued overall"）
- 2026-10-16｜Nathan Fast｜risk：CFO 指出下一波投入成本（半導體、記憶體、銅）上漲（原話："Now we see the next wave coming"）
- 2026-10-16｜Nathan Fast｜risk：建築市場：高利率目前未見對需求的影響（原話："We have not seen any impact from higher interest rates."）
- 2026-10-16｜Nathan Fast｜commitment：若 2027 有通膨壓力，將再執行定價（原話："we'll be flexing those muscles from an execution perspective"）

### 問答異常語氣（迴避／改口／保留）
- SU.PA_2024_Earnings_Call_20250220.md｜問：James Moore (Redburn)：資料中心各細分（含超大規模雲端）訂單成長幅度與未來 3–5 年展望｜答法：CEO 表示不提供具體數字（'We don't communicate any specific number moving forward'），CFO 給占比拆解但稱難以回推訂單成長率，未確認分析師推算的 70–75% 成長
- SU.PA_2024_Earnings_Call_20250220.md｜問：Andre Kukhnin (UBS)：中壓業務占比、急單定價是否已享受、SF6-free 帶來的增量｜答法：CEO 稱不公布占比，轉談 AirSeT 產品更新；未回答急單定價問題與 2025 SF6-free 貢獻；CFO 稱 'you said it all'
- SU.PA_2024_Earnings_Call_20250220.md｜問：Alexander Virgo (BofA)：Systems 定價約 15% 以上、2025 毛利率緩和幅度是否如此｜答法：CEO 先談產品組合與在地定價能力，CFO 稱無特別事項，只說 Systems 定價預期正常化，未給幅度數字
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：UBS：未來 12 個月成長與利潤率如何取捨？｜答法：CEO 未直接回答取捨，表示今天不談 2024 財測，改談各市場分化、部分領域可能轉負
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Berenberg：激勵薪酬是否會對齊新成長與利潤率目標？｜答法：CEO 稱尚未想過，長期激勵已定，只說各年 KPI 權重會視情況調整
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：BNP Paribas Exane：多餘資本將返還多少、理想槓桿？｜答法：CEO 先轉給 CFO；CFO 明說不給具體槓桿數字，只說預期自高點下降，返還形式為特別股息或買回
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Morgan Stanley：PLC 規模偏小是投資組合弱點，如何強化？｜答法：CEO 未提補強計畫，改談製程／混合市場強勢，並說 PLC 只占業務約幾個百分點、刻意避開汽車
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Citi：成長是否需要更多政府方案？｜答法：CEO 不直接回答是否需要，改談現有法規、能源成本與高端市場聚焦
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Citi（Daniela Costa）：AVEVA 轉型順風使利潤率路徑是否前高後低？｜答法：CFO 未確認前高後低，表示時間點無法精確預知，說軟體貢獻偏後段、系統業務同時回升
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：SocGen：SFC 比率是否可再降 100–150bp？｜答法：CFO 回答系統毛利差距，但未回應 SFC 具體降幅
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20231109.md｜問：Bernstein：2027 年軟體與服務占比會到多少？｜答法：CFO 表示這次未提供數位飛輪各部分細項，只給成長方向，不給 2027 占比數字
- SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20250507.md｜問：股東問Peter Herweck離職補償，以及下任CEO若自願離職是否也有同樣補償政策｜答法：董事長答該合約已經股東大會表決、依合約執行，未直接回答下任CEO自願離職是否適用
- SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20250507.md｜問：股東問Notre-Dame專案花費多少百萬歐元｜答法：CEO答數字大概未公開，改談捐贈內容包含設備與工時，未給金額
- SU.PA_Shareholder_Analyst_Call_Schneider_Electric_S_E_20250507.md｜問：股東問風力發電機與住家的最小距離政策｜答法：董事長答公司不製造風機、無法回答，改談荷蘭風車
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：UBS 分析師：工業終端市場目標被調低、大盤成長目標卻維持，是什麼讓你們對更長期可見度有信心？｜答法：CEO 以電氣化／自動化／數位化趨同、全生命週期與地理擴張作答，未回答工業目標為何調低；CFO 補稱是用內部經濟模型估算，並說資料中心才有跟客戶談較長週期，工業『may happen in this cycle or a bit beyond』難預測。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：分析師：Schneider 很少見不當價格領先者，這是單一區域、事業部還是系統性問題？｜答法：CEO 未指認區域或事業部，改談中國通縮、關稅反覆造成決策延遲、服務過去以成長優先；未給定價落差的數字，並承諾回到定價紀律。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：Gael：若 AVEVA 回到 30% 利潤率，其餘工業自動化 18% 目標是否保守（隱含不到 15%）？｜答法：CFO 未回應推算，也未給任何額外數字，只重申 2028 年 18% 並說『Let us get started』『不是旅程終點』。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：分析師：同業都在布局固態變壓器（SST），你們是自建、合作還是收購？｜答法：CEO 轉交資料中心技術長；技術長未回答自建／合作／收購，只說 800V 直流下功能區塊仍在、2027 年前不預期大規模新技術，並把細節推給下午的展示攤位。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：分析師：重組費用上升、過去人員增幅高於同業，是否人招太多？｜答法：CEO 以『疫後週期檢討效率』作答，未回答是否多聘人，也未給人數或節省金額，只說不會有重大新聞級的重組、領導層逐步精簡。
- SU.PA_Analyst_Investor_Day_Schneider_Electric_S_E_20251211.md｜問：Citi 分析師：若做大型併購，ROCE 目標是否仍成立？｜答法：CEO 重申有機優先、目前不計畫大型收購；CFO 自己承認『pretty much all acquisitions cause a small … negative impact on ROCE』，但仍稱 15%～20% 有把握，未說明大型併購時的影響幅度。
- SU.PA_2026_20260730.md｜問：Phil Buller (JPMorgan)：毛利率與 EBITA 利潤率優於預期，但財測隱含下半年利潤率進展較低，如何調和？｜答法：CEO 說上半年「a bit in advance versus what was the initial plan」；CFO 接著說上半年「primarily in line with what we had guided」，兩人說法略有差異，且未直接回應下半年隱含利潤率進展為何較低，只提到關稅退款與多種情境
- SU.PA_2026_20260730.md｜問：James Moore (Redburn)：今年高訂單水準明年能否再成長，還是會正常化？｜答法：CEO 未給訂單或成長數字，改談公司自身使用 AI、token 成本與 Schneider 預測方式，結論為「so far, we believe it's manageable」
- SU.PA_2026_20260730.md｜問：Daniela Costa (Goldman)：Cognite 的成長與利潤率輪廓，以及是否加速 M&A｜答法：CEO 自述「I'm afraid I'm going to be a bit boring and repeating」，未給 Cognite 的成長或利潤率數字，只講策略定位
- SU.PA_2026_20260730.md｜問：Jonathan Mounsey (BNP)：IA 營收成長強但利潤率僅 +30bps，何時改善？｜答法：CEO 與 CFO 重申計畫在軌，說明需要「a couple of months, maybe 2 years」，CFO 稱「we don't give you the details」，未提供拆解數字
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Mackie：對 PTC 客戶基礎的反向綜效（dis-synergies）與競爭反應如何評估？｜答法：CEO 談開放互通與客戶採購趨勢，未直接量化或回答 dis-synergies；交割風險部分 CFO 稱不就第三方介入作假設性推測。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Buller：自上次 CMD 後策略改變了什麼？AI 顛覆風險是否升高？何時再開 CMD？｜答法：CEO 改談以終端市場而非事業群看組合，未直接回答 AI 顛覆風險是否升高，也未回答新 CMD 時點；CFO 補充承諾不變。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Moore：8 億歐元營收綜效按四個領域的拆分、各年度節奏、PTC 自身 vs Schneider 自動化各占多少？｜答法：CFO 明說不給拆分（I'm not going to dimension exactly），只稱雙向、交割後不久開始、中期線性。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Moore：ROCE 計算所用 WACC 是多少？｜答法：CFO 回答 ROCE 15–20% 與 5 年內超過 WACC，但未給出 WACC 數字。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Yates：股權募集時點？是否等監管核准後才募？｜答法：CFO 稱時點尚未決定，僅說會相當快降低融資風險。
- SU.PA_Schneider_Electric_S_E_PTC_Inc_M_A_Call_20261005.md｜問：Kukhnin：兩宗大型併購（Cognite、PTC）同時進行，內部如何管理？｜答法：CEO 稱交割時點「probably Q2 next year」，與 CFO 簡報中「closing by Q3 2027」口徑不同，未在 Q&A 中說明差異。
- SU.PA_Schneider_Electric_S_E_Q3_2026_Sales_Trading_Statement_Call_Oct_16_2026_20261016.md｜問：Ben Heelan (BofA)：2027 是否還會有漲價以抵銷成本？｜答法：明說不給 2027 指引，改談年內三輪漲價與定價紀律，未回答 2027 漲價幅度
- SU.PA_Schneider_Electric_S_E_Q3_2026_Sales_Trading_Statement_Call_Oct_16_2026_20261016.md｜問：Max Yates (Morgan Stanley)：資料中心訂單在超大型雲端、neocloud、其他的拆分｜答法：兩度表明不揭露分類拆分，僅稱曝險「應與大盤相當」並稱選擇性高
- SU.PA_Schneider_Electric_S_E_Q3_2026_Sales_Trading_Statement_Call_Oct_16_2026_20261016.md｜問：Delphine Brault (Oddo)：新指引隱含 Q4 放緩，原因為何？｜答法：提及多重情境與高基期，未給 Q4 具體數字或確認是否保守

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
{"status":"no_prior_dd"}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SU.PA_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
