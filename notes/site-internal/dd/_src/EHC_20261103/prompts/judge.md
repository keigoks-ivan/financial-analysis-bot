你是 stock-analyst **v20 判斷 agent**，標的 EHC（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"EHC","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_net_operating_reven","label":"營收（GAAP net operating revenue）","value":1609.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm"}},{"id":"f_kpi1_adjusted_ebitda_non_gaap","label":"Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代替）","value":346.6,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益（營收減總營業費用，自算；新聞稿未直接列示）","value":288.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm"}},{"id":"f_kpi5_adjusted_eps","label":"Adjusted EPS","value":1.52,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm"}},{"id":"f_kpi6_2026","label":"2026 全年指引（上調）","value":"營收 6,450–6,500M；Adj EBITDA 1,395–1,415M；Adj EPS 6.23–6.37","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm"}},{"id":"f_kpi7_discharges","label":"出院人次（discharges）","value":69605,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"人次","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ehc_gross_margin_pct","label":"EHC 毛利率","value":95.88,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EHC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ehc_operating_margin_pct","label":"EHC 營業利益率","value":18.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EHC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ehc_fcf_margin_pct","label":"EHC FCF 利潤率","value":6.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EHC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hca_gross_margin_pct","label":"HCA 毛利率","value":42.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HCA.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hca_operating_margin_pct","label":"HCA 營業利益率","value":15.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HCA.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hca_fcf_margin_pct","label":"HCA FCF 利潤率","value":7.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HCA.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uhs_gross_margin_pct","label":"UHS 毛利率","value":90.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UHS.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uhs_operating_margin_pct","label":"UHS 營業利益率","value":11.28,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UHS.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uhs_fcf_margin_pct","label":"UHS FCF 利潤率","value":4.98,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UHS.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_thc_gross_margin_pct","label":"THC 毛利率","value":83.33,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.THC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_thc_operating_margin_pct","label":"THC 營業利益率","value":22.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.THC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_thc_fcf_margin_pct","label":"THC FCF 利潤率","value":14.09,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.THC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_adjusted_fcf","label":"自由現金流（Adjusted FCF）","value":263.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm"}},{"id":"f_kpi4_sbc","label":"SBC 占營業利益","value":5.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）","citation":"公司 Q3 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000236/ehcearningsrelease93026.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":136.69,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":28.64,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":70.12,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.62,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.11 → 6.27）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.95,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.68 → 6.81）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.78,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.29 → 7.42）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":6.27,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.81,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.42,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.5,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 6.0 → 6.27（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":21.87,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝92.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":92.1,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.12,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.55,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":21.8,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 6.27，分子＝快照價 136.69","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.571,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":2727.2,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 2803.4、現金 76.2（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":98.3,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":16163.83,"period":"2026-11-03","unit":"USD m","basis":"市值 13436.63 ＋ 淨負債 2727.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":6475.16,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":7017.86,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.5,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 137.08 / W52 110.36 / W104 109.65 / W250 83.37 / W250 13週斜率 1.6%"},{"id":"f_ma_w52","label":"52 週均線","value":110.36,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":109.65,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":83.37,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.6,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K：IRF 業除 EHC 外高度分散，主要對手為急性醫院內的復健單位（92% 患者來自急性醫院）；另有一家公開公司經營 38 家 IRF；CON 為進入障礙。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm","excerpt":"The inpatient rehabilitation industry, outside of our leading position, is highly fragmented. Our inpatient rehabilitation hospitals compete primarily with rehabilitation units, most of which are within acute-care hospitals, in the markets we serve.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：急性醫院系統可能擴張復健服務；2023 年南卡羅來納廢除 IRF 的 CON，CON 弱化可能提高競爭。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm","excerpt":"For example, in 2023, South Carolina enacted legislation to repeal CON regulations for several provider types, including IRFs.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"搜尋未找到 2026 年 IRF 新進入者或具體份額消長數據；聚合站未提供可靠 IRF 份額。","source":"WebSearch 結果彙整（csimarket/IBISWorld 等聚合站）","url":null,"excerpt":null,"as_of":"2026-11-03","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K：Medicare 與 Medicare Advantage 合計約占總營收 82%（傳統 Medicare 65.4%）；FY2023 為約 81%、FY2019 約 86%。","source":"Encompass Health FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm","excerpt":"Revenues from Medicare and Medicare Advantage represent approximately 82% of total revenues.","as_of":"2026-02-27","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 Q1 10-Q：循環信貸額度可用約 7.26 億美元，信貸協議債務 2031 年前不到期。","source":"Encompass Health Q1 2026 Form 10-Q (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000130/ehc-20260331.htm","excerpt":"approximately $726 million available to us under our revolving credit facility; the amounts outstanding under our credit agreement do not mature until 2031","as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"EHC 2025 年報稱持牌 IRF 數自 2010 年起僅小幅成長，complex medical 如中風的密集住院復健需求仍顯著未被滿足（公司自述）","source":"Encompass Health 2025 Annual Report and Proxy","url":"https://s203.q4cdn.com/714480614/files/doc_financials/2025/ar/Interactive-2025-Annual-Report-and-Proxy.pdf","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"EHC Q1 2026：總出院人次 +4.3% 至 67,763，同店出院 +1.6%；單位關閉拉低約 85bp；公司稱 75 歲以上人口年增約 4%（Q3 2025 call）、需求未被充分服務且隨高齡化成長","source":"Encompass Health Q1 2026 earnings call (MarketBeat / Yahoo Finance)","url":"https://www.marketbeat.com/earnings/reports/2026-4-30-encompass-health-co-stock-2/","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"EHC 已公布多家 2027 開業新院（Flowood MS 50 床、Cookeville TN 40 床、Apollo Beach FL 50 床、Conroe TX 24 床小型院）；2026 前三季開 4 院 189 床，Q3 稱 pipeline 15 院 654 床（Q2 為 13 院 606 床）","source":"Encompass Health press releases / Q3 2026 transcript summary (EarningsWhispers)","url":"https://www.earningswhispers.com/transcript/EHC/Q32026","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261103","affects":["thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"北卡羅來納州廢除 IRF certificate-of-need，據稱自 2029 年起可支撐每年 6–10 家新設施（潛在新進者供給）","source":"Q2 2026 earnings coverage (MarketBeat / Simply Wall St)","url":"https://www.marketbeat.com/instant-alerts/encompass-health-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CMS 2027 IRF final rule（7/30 發布）使 EHC 估計 10/1 起每 Medicare 出院淨營收 +2.3%；2026 指引營收 $6.41–6.49B、調整後 EPS $6.02–6.25","source":"Q2 2026 earnings coverage (MarketBeat)","url":"https://www.marketbeat.com/instant-alerts/encompass-health-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"有分析敘事指出價值導向照護與門診／居家復健轉移可能長期壓抑住院量","source":"Simply Wall St EHC narrative","url":"https://www.simplywall.st/narratives/8xc4v2rw-ehc-expanding-hospital-footprint-and-bed-upgrades-will-shape-measured-outlook","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Becker's：IRF 需求在多市場大幅超過供給（評論文章），SNF 人力短缺使出院去向受限、推向 IRF","source":"Becker's Hospital Review","url":"https://www.beckershospitalreview.com/care-coordination/whats-driving-system-investments-in-rehab-care/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因素：FTC 與 DOJ 近年積極挑戰併購，持續積極執法會增加收購的時間與費用並可能降低成交可能性（對併購／新設醫院的一般性風險，非針對 EHC 的調查）。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm","excerpt":"In recent years, the Federal Trade Commission and DOJ have been aggressive in challenging mergers and acquisitions they believe present antitrust concerns and in asserting novel legal arguments for what constitutes unlawful anticompetitive activity.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 法律程序：公司處於高度監管產業，受政府稽核與調查，並可能有未揭露的 qui tam（FCA）訴訟；未列出反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm","excerpt":"In the ordinary course of our business, we are subject to regulatory and other governmental audits and investigations and are party to various legal actions, proceedings, and claims, including wage and hour, employment and personal injury claims, some of which seek to be certified as class or collective actions.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"CMS FY2027 IRF 最終支付規則（2026-07-30）：EHC 估計每名 Medicare 出院淨營收約 +2.3%，自 2026-10-01 起。","source":"MarketBeat Encompass Health Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/encompass-health-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因素僅把貿易或關稅爭端列為可能干擾營運的不可預見事件之一，未點名具體關稅或出口管制暴露。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm","excerpt":"Other unforeseen events, including acts of violence, war, terrorism and other international, regional or local instability or conflicts (including labor issues), embargoes, trade or tariff disputes, short-term and long-term weather-related events, natural disasters such as earthquakes, wildfires, and floods, whether occurring in the United States or abroad, could restrict or disrupt our operations and negatively affect our results of operations and cash flows.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2025 Q1 法說會 CFO 表示近期關稅對建造成本與供應鏈風險不大。","source":"GuruFocus 摘要（itiger）","url":"https://www.itiger.com/news/2530146665","excerpt":null,"as_of":"2025-05-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"EHC 2026Q1 10-Q 顯示設施位於美國39州及波多黎各，截至2026-03-31共174家IRF，集中於佛州與德州；無海外營運","source":"Encompass Health Form 10-Q Q1 2026","url":"https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000130/ehc-20260331.htm","excerpt":"We operate hospitals in 39 states and Puerto Rico, with concentrations in Florida and Texas. As of March 31, 2026, we operated 174 inpatient rehabilitation hospitals.","as_of":"2026-05-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"EHC 2026 Q3 net operating revenue $1,609.5M, +8.9% YoY; discharges 69,605, +5.7% (same-store +3.0%); net patient revenue per discharge +4.0% to $22,543.","source":"Encompass Health Q3 2026 earnings release (Q4 CDN PDF)","url":"https://s203.q4cdn.com/714480614/files/doc_news/Encompass-Health-reports-results-for-third-quarter-2026-2026.pdf","excerpt":"Third-quarter discharges totaled 69,605, up 5.7%, and same-store discharge growth was 3.0%.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"CMS FY2027 IRF PPS final rule (effective 2026-10-01): 2.3% net update (3.2% market basket less 0.9pp productivity); est. +$755M aggregate vs FY2026; rural adjustment phase-out completes.","source":"CMS fact sheet FY 2027 IRF PPS final rule (CMS-1845-F)","url":"https://www.cms.gov/newsroom/fact-sheets/fy-2027-inpatient-rehabilitation-facilities-irf-prospective-payment-system-pps-final-rule-cms-1845-f","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Management says IRF demand remains strong; plans 250 beds via five new hospitals plus 100-150 beds at existing hospitals; NC certificate-of-need repeal effective Oct 1 could support 6-10 new facilities annually from 2029; Medicare-age population growing ~4% annually.","source":"MarketBeat, Encompass Health Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/encompass-health-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261103","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 results: Adjusted EBITDA +15.5% to $346.6M; full-year adjusted EPS guidance raised to $6.23-$6.37.","source":"Finviz/PRNewswire Q3 2026 release","url":"https://finviz.com/news/410657/encompass-health-reports-results-for-third-quarter-2026","excerpt":"$6.23 to $6.37 For considerations regarding the Company's 2026 guidance, see the supplemental information posted on the Company's website at http://investor.encompasshealth.com.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"文獻指出居家復健（HBR）是傳統住院復健的替代方案（2020 髖骨骨折比較研究，非 Medicare Advantage 情境）。","source":"Frontiers in Medicine 2020 (frontiersin.org) 居家 vs 住院復健","url":"https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2020.592693/pdf","excerpt":"home-based rehabilitation (HBR) is an alternative to classic inpatient rehabilitation (IR), which is an expensive framework with non-negligible risks.","as_of":"2020-01-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"醫院協會致 CMS 信函：2022 年 Medicare Advantage 的 IRF 使用率僅 0.4%，傳統 Medicare 為 1.16%。","source":"California Hospital Association letter to CMS re rehabilitation hospitals and MA network standards","url":"https://calhospital.org/wp-content/uploads/2024/10/Letter-to-CMS-RE_-rehabilitation-hospitals-and-MA-network-standards-Final.pdf","excerpt":"in 2022, the utilization rate for IRF care in Medicare Advantage was only 0.4% versus 1.16% in traditional Medicare","as_of":"2024-10-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"AJMC：高強度居家復健模式（Medicare ACO）在低至中度複雜度病患中功能結果較佳、成本較低；現行支付以地點而非強度計價，偏向住院復健。","source":"AJMC, High-Intensity Home-Based Rehabilitation in a Medicare ACO","url":"https://www.ajmc.com/view/high-intensity-home-based-rehabilitation-in-a-medicare-accountable-care-organization","excerpt":"High-Intensity Home-Based Rehabilitation in a Medicare Accountable Care Organization Author(s)Joshua K. Johnson, DPT, PhD, Michael B. Rothberg, MD, MPH, Jarrod E. Dalton, PhD +8 More High-intensity home-based rehabilitation (HIHR) may substitute for facility-based postacute rehabilitation. Patients in HIHR had better functional outcomes at lower costs than patients in","as_of":"2025-01-08","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"EHC 在 9 家醫院對部分遭 MA 初次拒付的轉介先收治再多級申訴（Q2 2026 call 摘要）","source":"MarketBeat Q2 2026 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/encompass-health-q2-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"EHC 加速增床、de novo 與新小型醫院 hub-and-spoke 模式","source":"Encompass Health Q2 2026 Form 10-Q","url":"https://www.sec.gov/Archives/edgar/data/0000785161/000078516126000186/ehc-20260630.htm","excerpt":"De novo projects(1) Norristown, Pennsylvania 3Q26 50 — Bangor, Maine 4Q26 50 — San Antonio, Texas 4Q26 50 — Avondale, Arizona 4Q26 60 — Wesley Chapel, Florida — 50 Apollo Beach, Florida — 50 St. George, Utah — 50 Fishers, Indiana — 50 Haslet, Texas — 50 Flowood, Mississippi — 50 Cookeville, Tennessee(2) — 40 Remote and satellite hospitals (included in bed additions)(1)","as_of":"2026-08-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat 彙整（截至 2026-08-28）：平均目標價約 $148.71，高 $160、低 $140，9 位分析師（1 hold、7 buy、1 strong buy）；Walnut Invest 2026-08 為平均 $148.17、中位 $150、12 位、區間 $140–$155。目標價分布集中、較新的 Q3 後更新未查到。","source":"MarketBeat EHC forecast / Walnut Invest (搜尋摘要)","url":"https://www.marketbeat.com/stocks/NYSE/EHC/forecast/","excerpt":null,"as_of":"2026-08-28","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 2026-08-05 Q2 上修全年指引：調整後 EPS $6.02–$6.25（前 $5.89–$6.11）、調整後 EBITDA $1,365–$1,395M（前 $1,350–$1,380M）；當時共識約 EPS $6.00、營收 $6.42–6.43B，指引區間下緣略高於共識。","source":"MarketBeat: Encompass Health issues FY 2026 earnings guidance; EarningsWhispers","url":"https://www.marketbeat.com/instant-alerts/encompass-health-nyseehc-issues-fy-2026-earnings-guidance-2026-08-05/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-10-28 Q3 新聞稿標題為「Increases full-year guidance」（再度上修），但新數字未能讀取；2026 年無下修紀錄，指引為 2/5 初始、4/30、8/5、10/28 逐次上調。","source":"Encompass Health Q3 2026 results release (PDF)","url":"https://s203.q4cdn.com/714480614/files/doc_news/Encompass-Health-reports-results-for-third-quarter-2026-2026.pdf","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 新聞稿上修全年指引","source":"Encompass Health Q3 2026 results","url":"https://www.encompasshealth.com/press-releases/encompass-health-reports-results-for-second-quarter-2026","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2025-07 起多家原告律所公告調查 EHC 可能違反證券法；Rosen 網頁載有證券集體訴訟起訴書，涵蓋 2022-02-26 至 2025-07-15 購入證券者，被告含 CEO Tarr 與 CFO。搜尋摘要稱 2025-07-15 股價跌 10.4% 收 107.28 美元。法院、案號、現況未查到。","source":"Rosen Law Firm｜Encompass Health complaint PDF；Business Wire 律所公告 2025-07-17","url":"https://rosenlegal.com/wp-content/uploads/2025/08/Encompass-Health-Upload1.pdf","excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共12份，含重大項目者4份；2026-03、05、06 的 Item 1.01 為新信貸協議與 5.875% 2034 年到期優先票據發行（再融資），非併購。","source":"SEC EDGAR 8-K 清單；8-K 2026-06-01","url":"https://www.sec.gov/Archives/edgar/data/785161/000078516126000161/ehc-20260529.htm","excerpt":"On May 29, 2026, Encompass Health Corporation (the “Company”) completed the issuance and sale of $500 million in aggregate principal amount of its 5.875% Senior Notes due 2034","as_of":"2026-06-01","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"搜尋未見 2025–2026 併購新聞；近12個月 8-K 的 Item 1.01 為信貸協議與票據發行，清單中未見 Item 2.01。","source":"SEC EDGAR 8-K 清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000785161&type=8-K","excerpt":"2026-03-10 8-K Items 1.01 Entry into a Material Definitive Agreement；1.02 Termination of a Material Definitive Agreement；2.03 Creation of a Direct Financial Obligation；9.01 Financial Statements and Exhibits","as_of":"2026-11-03","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Rosen 載有證券集體訴訟起訴書（Exchange Act 10(b)/20(a)），被告含 EHC、CEO Tarr 與 CFO，類別期間 2022-02-26 至 2025-07-15；多家律所於 2025-07 至 09 公告調查。法院、案號與現況未查到。","source":"Rosen Law Firm｜Encompass Health complaint PDF","url":"https://rosenlegal.com/wp-content/uploads/2025/08/Encompass-Health-Upload1.pdf","excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"FY2025 10-K 稱公司在日常業務中涉及各類訴訟，部分求准許為集體或集體訴訟，並可能有未公開的 qui tam 案。","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/785161/000078516126000081/ehc-20251231.htm","excerpt":"In the ordinary course of our business, we are subject to regulatory and other governmental audits and investigations and are party to various legal actions, proceedings, and claims, including wage and hour, employment and personal injury claims, some of which seek to be certified as class or collective actions.","as_of":"2026-02-26","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"EHC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":95.88,"operating_margin_pct":18.47,"fcf_margin_pct":6.97,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.EHC","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HCA","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":42.76,"operating_margin_pct":15.31,"fcf_margin_pct":7.59,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HCA","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"UHS","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":90.66,"operating_margin_pct":11.28,"fcf_margin_pct":4.98,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UHS","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"SEM","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SEM"},"note":"quarterly_income_stmt 無資料"},{"name":"THC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":83.33,"operating_margin_pct":22.52,"fcf_margin_pct":14.09,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.THC","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"EHC"},"financial_history":{"ticker":"EHC","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":4348600000.0,"revenue_yoy_pct":null,"gross_margin_pct":40.32,"operating_margin_pct":14.49,"net_income":271000000.0,"diluted_eps":2.7,"free_cash_flow":121700000.0,"fcf_margin_pct":2.8,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":4801200000.0,"revenue_yoy_pct":10.41,"gross_margin_pct":41.3,"operating_margin_pct":15.24,"net_income":352000000.0,"diluted_eps":3.47,"free_cash_flow":267700000.0,"fcf_margin_pct":5.58,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":5373200000.0,"revenue_yoy_pct":11.91,"gross_margin_pct":41.56,"operating_margin_pct":16.09,"net_income":455700000.0,"diluted_eps":4.46,"free_cash_flow":360300000.0,"fcf_margin_pct":6.71,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":5935200000.0,"revenue_yoy_pct":10.46,"gross_margin_pct":95.71,"operating_margin_pct":17.74,"net_income":566200000.0,"diluted_eps":5.54,"free_cash_flow":439200000.0,"fcf_margin_pct":7.4,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/EHC/EHC_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Encompass Health Corporation** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning, everyone, and welcome to Encompass Health's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Today's conference call is being recorded. If you have any objections, you may disconnect at this time. I will now turn the call over to Mark Miller, Encompass Health's Chief Investor Relations Officer.

**Mark Miller** (Executives):
Thank you, operator, and good morning, everyone. Thank you for joining Encompass Health's Third Quarter 2026 Earnings Call. Before we begin, if you do not already have a copy, the third quarter earnings release, supplemental information and related Form 8-K filed with the SEC are available on our website at encompasshealth.com. 
On Page 2 of the supplemental information, you will find the safe harbor statements, which are also set forth in greater detail on the last page of the earnings release. During the call, we will make forward-looking statements, such as guidance and growth projections, which are subject to risks and uncertainties, many of which are beyond our control. Certain risks and uncertainties, like those relating to regulatory developments as well as volume, bad debt and cost trends that could cause actual results to differ materially from our projections, estimates and expectations are discussed in the company's SEC filings, including the earnings release and related Form 8-K, the Form 10-K for the year ended December 31, 2025, and the Form 10-Q for the quarters ended March 31, 2026, June 30, 2026, and September 30, 2026, when filed. 
We encourage you to read them. You are cautioned not to place undue reliance on the estimates, projections, guidance and other forward-looking information presented, which are based on current estimates of future events and speak only as of today. We do not undertake a duty to update these forward-looking statements. Our supplemental information and discussion on this call will include certain non-GAAP financial measures. For such measures, reconciliation to the most directly comparable GAAP measure is available at the end of the supplemental information, at the end of the earnings release and as part of the Form 8-K filed yesterday with the SEC, all of which are available on our website. 
I would like to remind everyone that we will adhere to the 1 question and 1 follow-up question rule to allow everyone to submit a question. If you have additional questions, please feel free to put yourself back in the queue. With that, I'll turn the call over to President and Chief Executive Officer, Mark Tarr.

**Mark Tarr** (Executives):
Mark, thank you, and good morning, everyone. We're very pleased with our third quarter results. As revenue grew 8.9%, adjusted EBITDA increased 15.5% and adjusted EPS increased 23.6%. For the first 9 months of 2026, revenue rose 9.2%, adjusted EBITDA increased 11.9% and adjusted EPS was up 17%. 
Based primarily on our Q3 results, we are again raising our guidance for 2026. We achieved these results while once again delivering outstanding patient outcomes. Our Q3 discharge to community rate was 84.7%, discharge to acute rate was 8.4% and discharge to SNF rate was 6.2%. 
Our performance on each of these quality metrics continues to exceed industry averages. Our hospitals continue to be recognized for the outstanding clinical care we provide. Newsweek recently named Encompass Health as America's most awarded leader in inpatient rehabilitation for the seventh consecutive year. 
Also, NRC Health, a leading provider of patient experience data, recognized Encompass Health with the 2026 NRC Health Excellence and Patient Experience Award for the second consecutive year, placing us among the top 3 large health systems nationwide for patient experience. Our investments in professional growth and development programs for our clinicians continue to enhance our abilities to serve high-acuity medically complex patients. 
Encompass Health holds 408 Joint Commission disease-specific certifications, including 150 Joint Commission stroke certifications. This represents approximately 65% of total stroke certifications among all providers. In August 2026, the American Heart Association and American Stroke Association reaffirmed the importance of inpatient rehabilitation facilities in their updated 2026 stroke rehabilitation guideline, recommending IRF care over skilled nursing facilities for eligible stroke patients when both settings are available. 
The recommendation is supported by evidence showing greater functional improvement and higher rates of discharge back to the community following IRF care. We treat more stroke patients than any other inpatient rehabilitation provider. Through the first 3 quarters of 2026, we treated 37,620 patients recovering from a stroke, comprising approximately 18% of our patient mix. We will continue to put our resources to work to help stroke and other vulnerable patients regain their independence and return to the activities that matter most to them. 
Demand for inpatient rehabilitation services remains strong and is growing. We continue to invest in capacity additions to help address this underserved market. In Q3, we opened a new 50-bed hospital in Norristown, Pennsylvania and added 31 beds to existing hospitals. Through the third quarter, we opened 4 hospitals with a total of 189 beds and added 85 beds to existing hospitals. 
Earlier this month, we opened 2 additional 50-bed hospitals, one in Bangor, Maine and 1 in San Antonio, Texas and added 60 beds to existing hospitals. Over the balance of the year, we intend to open 2 more hospitals with a total of 100 beds and add up to 45 beds to existing hospitals. We maintain an active pipeline of new hospital development projects while also executing on bed expansion opportunities as warranted by occupancy trends and market dynamics. 
Our pipeline of announced new hospital projects with opening dates beyond 2026 currently consists of 15 hospitals with 654 beds. This includes our first 2 small format hospitals, Conroe, Texas and Richmond, Texas, both of which will be additive to our Houston market presence and serve as an exemplar of the hub-and-spoke strategy we have previously discussed. 
We anticipate additional projects will be announced over the balance of the year. We also continue to expect to add 150 to 200 beds to existing hospitals in 2027. On October 1, North Carolina's repeal of its Certificate of Need law became effective. As we have previously discussed, North Carolina has highly favorable population growth and demographic characteristics and our assessment indicates a large underserved market for IRF services. We currently operate 1 hospital in North Carolina and have thus far prioritized 15 markets for development. We currently have 6 real estate parcels under contract. Now I'll turn it over to Doug.

**Douglas Coltharp** (Executives):
Thank you, Mark, and good morning, everyone. The Q3 revenue increase of 8.9% was driven by 5.7% discharge growth and a 4% increase in net revenue per discharge. Net revenue per discharge again benefited from higher patient acuity. Bad debt expense in Q3 was 2.7%. The increase over last year is primarily due to a billing and collection disruption issue following a system conversion in Q2 of 2026. 
This was a one-off issue, and we expect bad debt expense as a percent of revenue in Q4 to normalize in the recent historical range of 2% to 2.5%. Q3 Medicaid supplemental payments decreased by $10 million from Q3 '25. Recall that Q3 '25 included $10.8 million of net provider tax revenue owing largely to retroactive Medicaid supplemental payments. 
In Q3 '26, we reversed $9.2 million of previously accrued supplemental payments within our other revenue category related to the anticipated approval by CMS of the Florida fiscal year 2026 Medicaid state-directed payment program. The Florida fiscal year '26 program is still pending approval from CMS. And as the fiscal year ended September 30, we deemed it appropriate to make this adjustment. 
We also reversed $3.4 million of accrued provider tax expense within our other operating expenses related to the 2026 Florida program. Q3 adjusted EBITDA increased 15.5% to $346.6 million even as we absorbed an $11.5 million year-over-year decrease in net provider tax contribution. Through the first 3 quarters of 2026, the adjusted EBITDA contribution from net provider taxes was $600,000, and that compares to $18.1 million for the comparable 2025 period. 
In our Q2 update, we had revised our expectation for the 2026 net provider taxes contribution to our adjusted EBITDA to approximately $10 million. This was based primarily on the Florida fiscal year 2025 Medicaid state directed payment program approved by CMS in May of 2026. Given the pending status of the fiscal year 2026 program and the related adjustments to our accruals, which I just reviewed, we now expect the 2026 net contribution to adjusted EBITDA to be approximately $3 million. 
Q3 SWB per FTE increased 3.8%, in part driven by increased participation in our career ladder programs, partially offset by declines in premium labor and medical plan costs. Premium labor costs comprised of contract labor and sign-on and shift bonuses declined $3.9 million from Q3 '25 to $23.1 million. This marks 16 consecutive quarters of year-over-year reductions in premium labor spend even as capacity and patient volumes have grown substantially. 
Contract labor FTEs as a percent of total FTEs was 0.9%, an improvement of 30 basis points from Q3 '25 and our lowest level since Q4 of 2020. Q3 net pre-opening and ramp-up costs were $4.9 million, flat from Q3 '25 and were $15.8 million on a year-to-date basis compared to $11 million through Q3 '25. 
Based on the incurrence to date and our projection for the balance of the year, we now expect net preopening and ramp-up costs of $20 million to $24 million for 2026. Adjusted free cash flow for the first 9 months of 2026 was $634.2 million, an 8.9% increase from the comparable period in 2025. 
During Q3, we repurchased approximately 495,000 shares of our common stock for a total of $57.9 million, bringing our year-to-date total share repurchase to approximately 1.91 million shares and $203.7 million. We also declared a cash dividend of $0.21 per share, which was paid earlier this month. 
During Q3, we issued an incremental $100 million of senior notes as an add-on to our 5.875% notes due in 2034, bringing the total amount of that note series to $600 million. Our leverage and liquidity remained very favorable. Net leverage at quarter end was 1.8x, and we ended the quarter with approximately $870 million available on our $1 billion revolving credit facility. 
As Mark mentioned, we have again raised our 2026 guidance as follows: we now expect net operating revenue of $6.45 billion to $6.5 billion, adjusted EBITDA of $1.395 billion to $1.415 billion and adjusted earnings per share of $6.23 to $6.37. The considerations underlying our guidance can be found on Page 11 of the supplemental slides. With that, we'll open the lines for Q&A.

**Operator** (Operator):
[Operator Instructions] And we'll take our first question from Pito Chickering with Deutsche Bank.

**Pito Chickering** (Analysts):
Nice quarter. So I know you aren't giving out 2027 guidance yet, but can you help us walk us through the known headwinds and tailwinds for next year as you do your modeling, specifically in areas like start-up losses from the hospitals opening up, managed care pricing because you just raised that this quarter, the VA penetration and then any things around labor and turnover that we should be thinking about?

**Douglas Coltharp** (Executives):
Pito, this is Doug. I'll start on that and then ask Mark and Pat to jump in as they see appropriate. I'd say, generally speaking, we think that things are setting up for another solid year in 2027. I won't hit these in the specific order that you mentioned, but I think some things to consider. I just went through quite a few adjustments, and we did the same in Q2 regarding net provider tax impact predominantly related to the Florida '25 proposal and then '26 as well. And so we're not going to have to repeat those same accrual adjustments in 2027, and that should present some upside there. 
With regard to pre-opening and ramp-up costs, we've got a comparable number of new hospitals opening next year. I would say that we would expect that number to be plus or minus $20 million. Some other things to consider is we'll anniversary the last of the 4 unit closures in late February of next year. 
On the labor perspective, we're going to start to anniversary the impact of the increased career ladder participation on SWB. By the same token, and I've said this a couple of times before, at some point, we're going to start to realize diminishing returns on the reductions that we've made in premium labor, but we continue to see some opportunity there. From an overall pricing perspective, as we move into Q4 of this year, we're lapping some of the increases that we've seen based on higher patient acuity on revenue per discharge. 
That's not to suggest that there isn't more room to go. But last year, in Q4, our net revenue per discharge was at 4.1%, and it stayed right around 4% for the last 4 quarters. I think those are the primary things that come to mind in terms of considerations.

**Mark Tarr** (Executives):
Yes, Pito, it's Mark. I would just say, as we noted in my comments and as we've made a general theme now for the last couple of quarters, I mean, adding capacity is a big focus for us. So bringing on the additional projects, not only in Q4 of this year, but then as it carries over into 2027 with additional beds coming on to existing hospitals. 
We're going to bring on the first small format hospital next year that we've talked about as well as additional de novos. So that will be a common theme that will go into 2027 that we've carried off from 2026.

**Patrick Tuer** (Executives):
Pito, this is Pat. Just a couple of points on VA and then hiring and turnover. VA continues to be a big positive for us. We've now hit our sixth consecutive quarter of at least 20% growth in that segment. We hit 21% growth in Q3. That's on top of 26.4% growth in Q3 of 2025. As well as that's going, there remains a lot of upside. 
There's a lot of variability between region to region and hospital to hospital in terms of capture of the VA population. So that's something our operators have done a great job with and continue to focus on. You didn't ask about this, but as I think about 2027, one of the things that I think deserves to be called out is the success that we've had in the MA admit-and-appeal strategy and how we're thinking about expanding that. 
So, so far, relatively small in size. We've had 294 claims go through. 87% of those have been overturned in our favor, 81% being overturned before they go to the ALJ. So a lot to like there. And if we think about discharge growth in that population, the MA growth in those 9 markets for MA was 36%. 
And then we've talked about how that has endeared us to the referral sources. They also saw total growth of about 9.5% with another benefit of 6.6% growth in Medicare. So we have just completed educating all of our hospitals on expanding that pilot for across every hospital, every payer for stroke specifically. 
We've increased the number of total pilot hospitals from 9 to 13 as well. So I think we'll start to see that incrementally tick up in Q4 and certainly in 2027. And then we'll evaluate how this goes. The next 2 diagnoses that we would likely scale up through the organization is brain injury and spine, which we're having a lot of success with as well. 
And then just on the hiring and turnover front, turnover did tick up slightly in Q3 to 20.7%, but that remains below our historical levels. In the 10 years from 2014 to 2023, we averaged about 24.2%. Even if you back out the COVID years, the 5 years before COVID, 2015 to 2019, we averaged about 23.2%. 
So well below historical levels there. And hiring has continued to remain robust. We have more full-time net RN hires through 3 quarters of this year than we've had in the last 5 calendar years on an individual basis. The high watermark there is 2023. So again, a lot of things to be optimistic about from a workforce perspective as well as the other 2 buckets that I mentioned.

**Operator** (Operator):
We'll take our next question from Ann Hynes with Mizuho .

**Ann Hynes** (Analysts):
So just on the capacity thought, I know that your capacity is running very high and I know -- I think you said like 35% of your hospitals may be running at 85% capacity. Can you update that stat for us? And when do you think those capacity constraints could be freed to really accelerate same-store discharge growth?

**Douglas Coltharp** (Executives):
Yes. So it is a factor. It's not the only factor. And generally speaking, when you're running at high system-wide occupancy rates, that's a really high-class problem. Specifically, we called out a cohort of hospitals that have been running at greater than 90% capacity with an average capacity -- an average occupancy of 95%. 
And so in Q1, we identified that there were 65 hospitals in that cohort. In Q2, the number dropped to 60. And in Q3, the number dropped further to 58. Across those 3 quarters, there have been 49 hospitals that have been present in that cohort for each of those 3 quarters. 19 of those will have bed additions between now and the end of fiscal year 2027. So that will help greatly in that regard. 
And as Mark mentioned earlier, we're excited about the addition of the small format hospitals that's really going to help us address those in some markets where there are physical limitations on our ability to expand.

**Patrick Tuer** (Executives):
Ann, this is Pat. Just in addition to what Doug has shared and what Mark has mentioned as well, we're really excited about our development pipeline. Both our development team, our operators and others at the home office have done a lot of work thinking about capacity expansions and how do we continue to take advantage of the demographic tailwind that is in front of us. And our pipeline from a de novo and small format hospital perspective is larger than it's ever been. 
And we're working hard to figure out how do we -- we guide to 6 to 10 hospitals a year with inclusive of North Carolina. We think we can get to the top of that range and potentially in the outer years, be above that range. So we're working towards that and really excited about the pipeline, both from a de novo and small format perspective.

**Douglas Coltharp** (Executives):
And the demand is there to support it. If you look just at the counties in which Encompass Health has a presence, from September of 2025 to 2026 in those counties, there were almost 0.5 million more Medicare beneficiaries. 
And roughly 50% of those, a little bit more than 50% were fee-for-service versus Medicare Advantage. So you've got an underserved population that continues to grow, and I know you've heard the mantra from us frequently, but the demographic tailwinds are still very much there.

**Operator** (Operator):
We'll take our next question from Andrew Mok with Barclays.

**Andrew Mok** (Analysts):
Just wanted to follow up on the managed care pricing. The guidance assumption increased 125 basis points at the midpoint to a new range of 3.5% to 4%. Would love to hear what's driving that increase. Is the admit and appeal strategy part of that? And can you also confirm that, that's unit pricing only and does not include shifts in acuity?

**Douglas Coltharp** (Executives):
It does include shift in acuity, and it's benefiting from that. The biggest driver there is something that Pat mentioned before, which is that is -- in that category, we include our VA DCM volume, and that's been growing consistently at north of 20%. And as a reminder, that pays at the fee-for-service rate. 
So the reason that we adjusted it up for the full year is because of the favorable performance we've had for the first 3 quarters of the year. Medicare Advantage is not included in that bucket. And again, that has skewed upward in acuity in part because of the more stringent pre-authorization that we've been facing and the fact that we've been able to replace some of the lower volume -- some of the lower acuity patients there with the higher acuity, specifically the stroke example that Pat gave earlier.

**Andrew Mok** (Analysts):
Got it. Okay. That's helpful. And then maybe just a follow-up on the small format hospitals. You mentioned that you have 2 in the pipeline, but I believe only one is expected to open in 2027. Can you confirm that one is still the expectation? And just given the smaller format and presumably faster speed to open, why isn't that a bigger number in 2027? Why can't you accelerate that?

**Douglas Coltharp** (Executives):
So I can confirm that our expectation is that one will open in late '27. The best explanation I can give you on why we're not moving faster right now is that small format hospitals are not only new to us, they're new to the communities in which we're introducing those, which have their own licensing and permitting aspects to them. 
And so in some of those instances, it doesn't fit -- the small format hospital doesn't fit neatly within the definition of either an acute care hospital or more of a subsidiary type of arrangement. And so we're having to spend a little bit more time on the front end through the permitting and licensing processes so that there's a greater understanding of what requirements really need to be contained within the remote location versus those that are provided by the host location. 
I think the good news is really on a state-by-state basis, once you have cracked the code the initial time, the template is set, and we'll be able to go much faster. And it's that aspect of it that gives us a lot of confidence that as we get rolling here, we're going to be able to accelerate that pipeline pretty significantly into 2028 and 2029. The design is there. We're confident in the design. We've got the capacity with our general contractors, and there's no capital constraint either.

**Patrick Tuer** (Executives):
I would add to that, that just from a market identification standpoint, our operators and development team have identified about 200 locations where this potentially could happen. As Doug mentioned, we really think that we're going to be in a position to ramp this up in 2028 and 2029. I think we would all be collectively disappointed if we're opening less than 6 of those a year by that point.

**Operator** (Operator):
We will take our next question from Matthew Gillmor with KeyBanc.

**Matthew Gillmor** (Analysts):
I wanted to ask about the RCD expansion. I think you indicated 75 more hospitals will be subject to RCD in 2027. And at least when we look at the CMS reports, it seemed like the affirmation rate with Palmetto had been improving. Just wanted to see if you had any comments in terms of what to expect as that gets rolled out to additional hospitals next year.

**Douglas Coltharp** (Executives):
Yes. So I'll start by saying that with regard to the expansion into Jurisdiction JJ, which does include 75 more of our hospitals, we are having ongoing discussions with both Palmetto and CMS to understand specifically how it's going to work. 
Our greatest concern is whether or not Palmetto is going to be able to handle this administratively. Palmetto's involvement in RCD thus far has been limited to the state of Alabama and 7 of our hospitals are included there. But the expansion into Jurisdiction JJ is going to increase the volume that they're going to have to process by more than 10x. 
It's a requirement that during cycle 1, which will -- is slated to begin on January 1 and extend through June 30, all providers will be on 100% prepayment claim review. There's no option out of that in cycle 1. So that's going to be a real burden on Palmetto, and we just want a greater understanding as to how they're going to be able to process that. 
That said, to the extent that we progress through cycle 1, and hospitals exceed the target affirmation rate of 80%, which we would have a high degree of confidence based on our experience to date, they will. And beginning July 1, one of the options we would have is to move from the 100% prepayment claim review to a 5% spot check. 
We have just moved into cycle 2 for the 24 hospitals that we have in Texas, where we performed very well and above the target affirmation rate, and we've made the decision to move to the 5% spot check there. And I think it's our anticipation that we'll avail ourselves of the same opportunity as it arises in other RCD markets.

**Matthew Gillmor** (Analysts):
Great. That's helpful. And then maybe just one follow-up. On the bad debt expense, you called out some impact from, I think, a system conversion. I was just hoping you could explain what happened there.

**Douglas Coltharp** (Executives):
Yes. So really about 2/3 of the increase was due to the system conversion. I'll probably give you more detail than you would want. But in Q2, we converted our patient billing system from a legacy system that was called Patcom to the Oracle module. And we did so because Patcom was essentially being sunsetted and the Oracle module has enhanced functionality as well as greater comparability with our Fusion ERP. 
When we initiated the cutover, the pending claims that were left in the legacy system required a more manual processing. And at the same time, we were shifting some of our resources in that area over to processing claims under the new system. As these claims were pending, they became subject to our aging-based reserve methodology. 
By the end of Q3, we were essentially caught up on our Medicare billing and collections, but the queue had not been cleared out for our managed care and our Medicare Advantage. And those payers typically run at a higher bad debt expense than Medicare fee-for-service, and they also generally require higher patient co-pays, and we can't bill for the co-pays until the payers process our claims. So it creates this backlog. 
Now we expect that queue to be fully cleared by the end of the year. And it is important to note that all claims since conversion are processing through the Oracle module without an issue. So this is really a onetime situation.

**Operator** (Operator):
We'll take our next question from Whit Mayo with Leerink.

**Morgan McCarthy** (Analysts):
It's Morgan McCarthy on for Whit. So your unit cost per discharge were effectively flat on a year-over-year basis. Is there anything to call out whether it's this year or in prior years related to provider taxes or any other cost items that might skew that metric?

**Douglas Coltharp** (Executives):
Yes. So the net impact from provider taxes was actually going to be a negative on that. But where we had some gains, again, SWB was very favorable. That was driven by lower group medical expense in the quarter and then also just by the lower overall turnover. EPOB was favorable for the quarter. Length of stay was favorable for the quarter. 
I will note that we had a benefit in supplies. You may recall that in Q3 of '25, we called out the fact that we had advanced some purchases of supplies in advance of the Fusion conversion in order to avoid any disruption. And obviously, we didn't have to replicate this year. But generally, when you've got a pricing increase in the 4% range, the flow-through and the efficiency there tends to be high.

**Operator** (Operator):
And we'll take our next question from Ryan Langston with TD Cowen.

**Ryan Langston** (Analysts):
You had some really nice acuity pickup recently that's carried through into the third quarter. I guess, is that acuity lift a durable opportunity into 2027? And might RCD expansion impact the acuity of the patient transfers from the acute care hospitals?

**Patrick Tuer** (Executives):
I'll start there, and -- acuity can shift or RC mix can shift on a quarter-over-quarter basis, but we do think that some of the trends that we're seeing are sustainable. We talked last quarter about the shift in acuity, and I'll call out a couple of diagnosis categories where we saw some really nice growth that are driving that again. 
We had 9.3% growth in our neuro RIC, 5.1% growth in stroke, 5.7% in brain injury, and then major trauma was up 10.3%. Some of those had a softer comp last year. But even if you look at it on a 2-year stack from a same-store basis, brain injury was up 9.8%, neuro up 8.5%, stroke and major trauma up 5.7%. And that mix is gaining because lower acuity conditions like lower extremity joint replacements are down. 
So in Q3, same-store lower extremity joint replacements were down 5.3%. On a total store basis, they were down 0.7%, and we were able to backfill that volume with those higher acuity conditions. Not only are we seeing an increase in -- from a RIC perspective, the percent of patients that come to us with comorbid conditions, it also continues to increase. And then we're getting the benefit on the pricing side as well from the outcomes that we're seeing. So even though we're seeing higher acuity conditions, we continue to do a better job of getting those patients home, and that has a favorable pickup on the pricing line.

**Douglas Coltharp** (Executives):
We don't anticipate that RCD expansion will have any impact on patient acuity. We believe we are admitting appropriate patients and providing the appropriate documentation for those patients.

**Ryan Langston** (Analysts):
Got it. And then sorry if I missed this in the supplemental payment commentary, but is there any update on the potential tax waiver program in Florida? And can you remind us if there's any impact, plus or minus, to guidance for 2026?

**Douglas Coltharp** (Executives):
Yes. So we went through the fact that we reversed the year-to-date accrual through the first 3 quarters. And that is because the fiscal year '26 ended on October 1 for Florida without a decision, positive or negative from CMS on the proposal set forth by Florida. 
The proposal set forth would include waivers for many of our hospitals in that state. If that were to come through in the fourth quarter, it has a potential favorable increase to EBITDA of about $8 million, which would be the sum of the roughly $5.5 million net impact that we reversed in our Q3 earnings plus the pickup we would get for Q4. As we look into 2027, again, if it's approved with the waivers in it as submitted, that would be a positive. And again, on a year-over-year basis, we took that $11.5 million hit related to the fiscal year '25 Florida plan in the second quarter, and we're not anticipating that we would replicate that.

**Operator** (Operator):
We'll move next to Joanna Gajuk with Bank of America.

**Joanna Gajuk** (Analysts):
So I guess, first on the small format hospitals, it was very exciting, I guess, type of developments there. But can you remind us -- I couldn't remember whether you talk about the returns on these projects versus, say, your typical 40, 50-bed hospital? 
Because I guess you're leveraging some of the local costs in there, right? So can you remind us how that progresses, I guess, when you have a small format versus just a regular hospital because of return?

**Douglas Coltharp** (Executives):
Yes, absolutely. So we've been targeting and realizing returns, IRRs on our de novo program in the mid-teens, and that's based on maintaining a cost per bed, which we feel some degree of confidence in moving forward of roughly $1.25 million per bed. Bed expansions to existing hospitals offer the greatest leverage opportunity and then also the highest returns. We are at 25% or higher with regard to the IRR on bed expansions at existing hospitals, and the average cost per bed there tends to be right around $850,000. 
The small format hospitals are going to fall right in between. We're estimating the cost per bed on those will be right at $1 million, and we're targeting an IRR of about 20%. You identified the ability to get some efficiencies by sharing certain components of the administrative staff with the host hospital. 
And as a result, whereas we run on a corporate-wide basis an EPOB of just under 3.4x, we think there's an opportunity for the small format hospitals to have an EPOB below 3x, and that's a highly sensitive metric with regard to the P&L and therefore, the flow-through to returns.

**Joanna Gajuk** (Analysts):
Okay. That is great. And I guess the other question that I had in terms of this acuity-driven pricing, it seems like it's very sustainable there, and thanks for breaking out the volume growth by the different categories. 
So anything to call out that would suggest that somehow things could slow down into next year? I know it's volatile quarter-to-quarter, but if we think say the next 12 months or so, anything that would say, hey, like things should slow down or change versus your trajectory?

**Douglas Coltharp** (Executives):
Other than to recall that at least some of the increase in acuity that's flowing through in the pricing growth is attributable to the trends that we've been seeing within Medicare Advantage. And the increase in pre-authorization denials that skewed us towards a higher acuity within our MA book of business first became really prevalent in Q4 of '25. 
So if you looked at Q4 of '25, we had a 4.1% net revenue per discharge. Our MA discount for that quarter, it tends to widen out from Q3 to Q4 because MA price increases on a calendar basis and fee-for-service increases on a fiscal year basis was 2%. And it's -- so as we anniversary those higher increases, even if acuity is maintained at the current levels, the year-over-year pricing change is going to be less pronounced.

**Operator** (Operator):
We'll take our next question from Brian Tanquilut with Jefferies.

**Brian Tanquilut** (Analysts):
So maybe, Doug, my first question, contract FTE this quarter showed some pretty good improvement. And I know in Q2, you said that the gains were getting smaller. So just curious what you're seeing there in terms of on the permanent side, hiring, retention and the career ladder grads that you're putting out there and how that's translating into contract labor.

**Douglas Coltharp** (Executives):
I'm going to toss that one over to Pat because it's something that he spends a lot of time focused on.

**Patrick Tuer** (Executives):
Yes. And Doug continues to challenge us on the operations side by talking about the diminished returns that we're going to see in reducing contract labor and premium pay. And there is a truth to that. But this was another really strong quarter, and I highlighted some of the hiring and turnover dynamics earlier in the call. But we still have -- if you look at contract labor, extra shift sign-on overtime and you normalize that by a per patient day basis, we still have a couple of dozen hospitals that are over $100 per patient day in spend. 
So there still is juice for us to squeeze there, and we've had a lot of success working on those higher spend hospitals to bring that number down. Again, just to reinforce what I said earlier, net RN hires and therapy hires has not been better in years. Even if turnover ticked up a bit, the hiring dynamics have certainly overcome that and turnover on a historical basis is still very strong. 
From a ladder perspective, we are up to 55% of eligible nurses are on the ladder. That represents about 31% of all of our full-time nurses being on the ladder. They have to be here for a certain period of time to move up into the ladder. So there's some upside there. 
Again, we had a big bolus in 2026 of the ladder, and we're going to anniversary some of that. So any of that upside within the ladder, we'll be able to take those dollars and not be as pronounced as they were in 2026. But our largest bucket of opportunity is noncertified non-laddered nurses, which represents about 60% of our full-time nurses. 
And again, we have some variation from region to region that we're working to improve upon. And I think if we can continue to do that, we're going to continue to see improvements not only in turnover reduction in the premium pay buckets, but also in the continued sustainability of the higher acuity patients that we've been able to bring in.

**Mark Tarr** (Executives):
Brian, you've heard us say before relative to contract labor, we've given our operators the green light. If they've got the volume and need to have contract labor to accommodate that volume, they need to go ahead, and we'll take the hit on a short term until we can work it back out of the system. But we are not being throttled on our volume because of the focus on eliminating contract labor.

**Brian Tanquilut** (Analysts):
Maybe my follow-up, just as I think about the hospitals that you've opened in the first half of the year, how are they tracking in terms of hitting breakeven in your typical ramp? I mean, just curious how this class of new openings are performing.

**Douglas Coltharp** (Executives):
So remember, we're heavily skewed towards the back end of the year with 4 hospitals, 4 of the 8 opening up in Q4. That said, we think that these are tracking in accordance with our recent historical performance. 
And just as a reminder there, generally, what we have been seeing is that our de novo hospitals are achieving a 4-wall positive EBITDA by about month 6, and they're climbing over a 70% occupancy by about month 10. And then they're achieving what we would suggest is full maturity and typically qualifying for a bed addition sometime between year 3 and year 4. So we have no reason to expect that the performance of the current class is going to be any different from that recent historical.

**Operator** (Operator):
We'll take our next question from A.J. Rice with UBS.

**Albert Rice** (Analysts):
Yes. First question on the discharge growth on the same-store basis, there's been a lot of focus on that. I wondered if you would just offer us any comments. I know -- I think you mentioned that you had the final 4 closures will anniversary in February of those. And then you've obviously had the pacing on the new facilities. 
Anything to call out in the way to think about same-store discharge growth over the next number of quarters here, where there's any challenges or where there's some easy comps? I know you got a long-term target of 4% to 6% growth on that.

**Douglas Coltharp** (Executives):
Yes. So actually, I think our total discharge growth from '23 to '27, the target that we put out there was 6% to 8%. We didn't break that down between new store and same store. This won't surprise you, A.J., but I'm going to start with my usual disclaimer that we think it is increasingly less relevant to think about the distinction between new store and same-store that what really matters most is total discharge growth and the capital that's required to generate it. 
Having now said my piece with regard to the disclaimer, I'm going to take you through 5 factors that we think are relevant to looking at same-store. The first that you mentioned was the impact from the 4 unit consolidations. That impact on a net basis, we estimate for Q3 was about 40 basis points. That's down from 70 basis points in Q2 and from 90 basis points in Q1, and that will be fully lapped in Q1 '27. 
And as a reminder, the reduction in the volumes related to those unit closures carried no impact to EBITDA. Second is something that I mentioned earlier, which is that cohort of high occupancy hospitals, 65% above 90% in Q1, 60% above 90% in Q2, 58% above 90% in Q3, 49 hospitals consistent through all 3 of those quarters, 19 of those will have bed additions coming on board prior to the end of the year in '27. 
The third factor I would mention was the change that we saw in MA pre-authorization denials beginning in Q3 -- or excuse me, in Q4 of last year. If you look at total MA discharges in Q3, it actually declined 1.1%. Adjusted for the unit closures, which were disproportionately high in Medicare Advantage for the patient mix, especially the sole SNF unit that we closed, we would have been up 1%, still not the height of our aspirations. 
As Pat mentioned earlier, in the 9 admit and appeal pilot markets for the quarter, total discharge growth was up 9.3%. So what we've demonstrated is that pilot is working. And as Pat outlined, we're looking forward to extending that across stroke in all of our hospitals and then bringing more hospitals into the fold from a pilot perspective. In terms of bed additions and new hospitals, as we mentioned previously, bed additions in 2026 were also heavily weighted towards the second half of the year. 
Q3 benefited from only 54 beds added to existing hospitals in the first half of '26. And also, we only had one de novo, and that was Loganville, Georgia that moved from new store to same-store in Q3. I'll note that we have 90 beds moving into same-store in Q4 and another 150 in Q1 of '27. 
And then something we haven't talked about a lot, but it's evident, I think, to some degree in our overall patient mix is there is some impact that is happening across the [indiscernible] team markets. And so in Q3, we saw knee and hip replacement actually declined 3.6%. These are small categories for us and cardiac declined about 0.7%. 
Now not all teams markets are reacting the same. And in those markets, we're having a lot of success substituting higher acuity and/or VA CCN patients for these lower acuity patients that may be subject for team [indiscernible]. It may not be a one-for-one change from a volume perspective, what we're seeing in those markets is that the move to the higher acuity patients and the move to the VA CCN patients is generating higher revenue and EBITDA.

**Albert Rice** (Analysts):
Okay. That's great. I would -- maybe as my follow-up, just to ask, I know you're now down to 1.8x net leverage. I think you previously said that it wouldn't necessarily make sense to go below 2x. Should we think of capital deployment from here, leaning into share repurchases, dividends? Anything else, any comment you want to make along those lines?

**Douglas Coltharp** (Executives):
Yes. I think the capital allocation framework is going to be relatively consistent. You'll probably see modest occasional or periodic increases in the dividend. So that's not going to consume a lot of that capacity. Pat mentioned earlier that as we think about an accelerating pipeline for both small format hospitals and for de novo openings, particularly with the attractiveness of North Carolina is just an example that we're likely to see our discretionary CapEx begin to increase, and that's still going to leave capacity while maintaining a very favorable leverage target for increased share repurchase activity. So we like the combination of those things.

**Operator** (Operator):
We'll take our next question from Jared Haase with William Blair.

**Jared Haase** (Analysts):
Maybe I'll ask one on the current mix of your beds between single occupancy and double. I know you kind of had this shift towards more single over the last couple of years. Just wanted to get an update on where that stands today? And then based on what you have in the pipeline, where you think that could trend over the next couple of years?

**Douglas Coltharp** (Executives):
Yes. So at the end of the third quarter, we were at 58%. That compares, if you go all the way back to 2020 at 41%. So 58% were private. All of -- essentially all of the capacity that we're bringing on in all 3 modalities, bed additions, de novos and small format hospitals is going to be 100% single occupancy. So that number will continue to push up. 
And we'll get some benefit of that here in the fourth quarter because of the number of bed additions and new hospitals that we have coming on board. So that number will be higher when we report it for Q4.

**Jared Haase** (Analysts):
Okay. Very helpful. And then I appreciate all the details on the Medicare Advantage admit-and-appeal strategy. I realize it's still relatively early with the pilots. But just given the success you've seen so far and then your thinking around how you can expand that to other conditions and other hospitals across the portfolio. 
I guess when we think about the impact to the model, are there any guardrails that you would sort of frame for us in terms of what the actual net impact could be on conversion rate or I guess, ultimately, volume growth within that cohort over the next several years?

**Douglas Coltharp** (Executives):
Well, generally speaking, we think it's positive, a, because we're anniversarying the more challenging pre-authorization from the MA plans that began in Q4 of last year, and this has proven to be an effective tool because even beyond what we were experiencing in these categories with regard to denial rates, pre that dip in Q4 of last year, we're seeing higher success rates. All that said, it's not going to happen in a vacuum. And so we believe it is a tailwind in terms of quantifying it. That's yet to be determined.

**Patrick Tuer** (Executives):
Jared, this is Pat. We're in the process now of -- we've added resources since we started the pilot. We're adding a good number of FTEs that are going to help us as we scale this throughout the organization. But we're putting the structure in place to be able to go a little bigger here.

**Operator** (Operator):
We will take our next question from Raj Kumar with Stephens.

**Raj Kumar** (Analysts):
Maybe just wanted to touch back on RCD. As I kind of look at the Alabama cycle-through reports, kind of the claims activity coming down by 25% relative to the pre-RCD baseline, but kind of looking at you guys' results, fee-for-service is still pretty strong. 
So would love to kind of reconcile kind of your experience in that kind of Alabama program across these 3 cycles. And more specifically, I guess, kind of where your initial affirmation rates are kind of maybe where your appeal rates are as well? And maybe helping us extrapolate to this more expanded RCD program. Any details there would be helpful.

**Douglas Coltharp** (Executives):
Well, it's hard to extrapolate any of our experience across the expanded program because Palmetto, in particular, has never been asked to handle this volume of claims. And so we don't know if it's going to be the same reviewers. We don't know if it's going to be under the direction of the same medical director. We don't know whether they're going to be using subcontractors. We don't know if the program is ultimately going to be phased in, et cetera. 
What we do have a high degree of confidence in is that there's -- that we are admitting the right kind of patients, and we are providing the appropriate documentation. And again, as this extension begins on -- assuming it begins across all of these 75 hospitals on January 1, we will be prepared administratively to do our part -- and the target affirmation rate in cycle 1 is going to be 80%, and we have a very high degree of confidence that all of our hospitals are going to get over that 80% target affirmation rate. 
And if they do beginning July 1, we can move to a 5% spot check. That is not something that we have experienced to date because to this point, either because we were in cycle 1 in the other states that just came out, which was a requirement like California and Texas or because we elected to stay for various reasons on 100% prepayment claim review in Alabama, we haven't had experience with the 5% spot check. But the math will tell you that the impact is going to be less and the administrative burden will be less. 
And so again, we think if there's volatility in the bad debt number that arises out of the rollout to the 75 incremental hospitals, it's going to be contained and it's likely going to be contained in the first half of the year. It's important to note, none of the coverage requirements, none of the patient criteria under RCD are any different than they have been under the audit programs that we've been subject to for an extended period of time and that have informed our historical bad debt in this recent range of 2% to 2.5%. 
So there's no reason to believe that things settle in, that we're going to settle in at a bad debt number that differs in any material way from that which we've experienced historically.

**Raj Kumar** (Analysts):
Got it. Maybe just following up on that. I guess when I think about maybe some of the more independent IRFs and maybe some behavioral changes around maybe not appealing or not admitting IRF-eligible patients that might be on the fringe of eligibility. 
I guess, have you maybe experienced any market share gain dynamics from that or any favorability as I kind of think about kind of your administrative working power versus maybe an independent mom-and-pop IRF?

**Douglas Coltharp** (Executives):
We don't think we're admitting patients who are on the fringe of eligibility. We think that the patients that we admit clearly meet IRF admission requirements.

**Patrick Tuer** (Executives):
Yes. This is Pat. I would just add, I sit on the Board of AMRPA, which is the Trade Association for Inpatient Rehab Providers. And I think not only Encompass, but the other providers within AMRPA have all done a really nice job with RCD. And it hasn't shifted our admission practices. 
I mean, we are taking the same patients that we did before and to my knowledge, the other providers are as well. So I think if anything, administrative burden aside, we're proud of the fact that this has demonstrated such a strong record of compliance within our company and the industry.

**Operator** (Operator):
At this time, there are no further questions in queue. I will now turn the meeting back to Mark Miller for any additional or closing remarks.

**Mark Miller** (Executives):
Thank you, operator. If anyone has additional questions, please call me at (205) 970-5860. Thank you again for joining today's call.

**Operator** (Operator):
Thank you. This brings us to the end of today's meeting. We appreciate your time and participation. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### EHC_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Douglas Coltharp｜guidance：CFO 公布 2026 全年調升後的 EBITDA 與 EPS 財測區間（原話："adjusted earnings per share of $6.02 to $6.25."）
- 2026-08-06｜Douglas Coltharp｜guidance：Q4 Medicare 定價假設反映 7/30 公布的 IRF final rule（原話："reflects the IRF final rule released on July 30."）
- 2026-08-06｜Douglas Coltharp｜guidance：全年每 FTE SWB 成長預期上修為 3.5% 至 4%（原話："year 2026 SWB per FTE growth is 3.5% to 4%"）
- 2026-08-06｜Douglas Coltharp｜guidance：淨 provider tax 對 2026 EBITDA 的貢獻預期由約 2,100 萬美元下修為約 1,000 萬（原話："we now expect the net benefit to adjusted EBITDA in 2026"）
- 2026-08-06｜Douglas Coltharp｜guidance：全年開辦前與爬坡成本預期維持 1,800 萬至 2,200 萬美元（原話："ramp-up costs of $18 million to $22 million"）
- 2026-08-06｜Douglas Coltharp｜guidance：回應下半年上修財測的來源：定價（敏銳度）上行不確定（原話："There's no certainty that, that continues"）
- 2026-08-06｜Douglas Coltharp｜guidance：EPS 財測僅反映年初至今已執行的庫藏股（原話："The EPS guidance change reflects only the share repurchases"）
- 2026-08-06｜Douglas Coltharp｜guidance：SWB 上調假設僅限今年下半年趨勢（原話："it is an assumption for this year only"）
- 2026-08-06｜Mark Tarr｜guidance：CMS 2027 IRF final rule 對 Medicare 每次出院淨收入的估計影響（原話："approximately 2.3% increase in net revenue per discharge"）
- 2026-08-06｜Douglas Coltharp｜margin：Q2 營收成長 9.6% 的拆解：出院量成長 5.6%（原話："The increase was comprised of 5.6% discharge growth"）
- 2026-08-06｜Douglas Coltharp｜margin：每次出院淨收入成長歸因於病患敏銳度提高（原話："growth was driven by higher patient acuity."）
- 2026-08-06｜Douglas Coltharp｜margin：Q2 調整後 EBITDA 數字，並說明吸收了 provider tax 年減（原話："Our Q2 adjusted EBITDA increased 9.2% to $348 million"）
- 2026-08-06｜Douglas Coltharp｜margin：壞帳費用 Q2 為 2.3%，管理層稱符合預期（原話："in Q2 was 2.3%, in line with our expectations"）
- 2026-08-06｜Douglas Coltharp｜margin：合約勞工 FTE 占比 1.1%，較去年同期改善 20 bp（原話："was 1.1%, an improvement of 20 basis points from Q2 '25."）
- 2026-08-06｜Douglas Coltharp｜margin：EPOB 改善來源：較高入住率與 career ladder 的附帶效益（原話："we did see some further benefits in EPOB"）
- 2026-08-06｜Douglas Coltharp｜margin：Q2 系統入住率及年增幅（原話："Q2 occupancy of 77.4% was up 290 basis points over Q2 '25."）
- 2026-08-06｜Douglas Coltharp｜margin：持有 CRRN 認證護理師的薪資溢價（原話："It's about 9% over their peers who do not have"）
- 2026-08-06｜Douglas Coltharp｜margin：CFO 稱溢價勞工降幅已進入邊際遞減（原話："Q2 marked our 11th consecutive quarter where we had a"）
- 2026-08-06｜Patrick Tuer｜margin：COO 表示溢價勞工還有空間但幅度較小（原話："There's some diminishing returns on this"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：Q2 庫藏股回購股數（原話："repurchased approximately 704,000 shares of our common stock"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：發行 5.875% 2034 到期票據並贖回 2028 到期舊票據（原話："we issued $500 million of 5.875% Senior Notes due 2034"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：季末淨槓桿比率（原話："Our net leverage at quarter end was 1.9x."）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：季度股利調升至每股 0.21 美元（原話："quarterly dividend next payable in October to $0.21"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：管理層稱資本配置框架不變，是「and」而非「or」（原話："we're an and story, not an or story"）
- 2026-08-06｜Douglas Coltharp｜capital_allocation：CapEx 約占營收 15%，管理層稱可能是高點（原話："probably represents close to a high watermark."）
- 2026-08-06｜Patrick Tuer｜capital_allocation：開始評估加床的入住率門檻由 80-85% 降到 70-75%（原話："lowered that threshold to 70% to 75%"）
- 2026-08-06｜Douglas Coltharp｜commitment：維持每年 6 至 10 家新院目標，期望北卡將其推向高端（原話："we're going to stay with the 6 to 10 range"）
- 2026-08-06｜Douglas Coltharp｜commitment：北卡將自 2029 年起把新院數推向 6-10 區間高端（原話："it would drive us probably beginning in 2029"）
- 2026-08-06｜Mark Tarr｜commitment：北卡下一家新院預計開業時間（原話："our next hospital opening in North Carolina to occur"）
- 2026-08-06｜Mark Tarr｜commitment：下半年計畫開 5 家新院、250 床（原話："we intend to open 5 more hospitals with a total of 250 beds"）
- 2026-08-06｜Mark Tarr｜commitment：2026 年後已宣布的新院管線規模（原話："currently consists of 13 hospitals with 606 beds"）
- 2026-08-06｜Douglas Coltharp｜commitment：小型院計畫明年至少開一家，2028 年起每年近五家（原話："the intent to get at least one open next year"）
- 2026-08-06｜Patrick Tuer｜commitment：admit-and-appeal 預計年底前評估是否全面推廣（原話："we'll be in a position to evaluate for a full"）
- 2026-08-06｜Patrick Tuer｜commitment：管理層表示不願承諾敏銳度會持續（原話："it'd be prudent for us to back us into a corner"）
- 2026-08-06｜Douglas Coltharp｜commitment：對 2027 年 SWB 每 FTE 增幅尚不給水準（原話："we're not ready to call a level on it"）
- 2026-08-06｜Douglas Coltharp｜competition：管理層稱高敏銳度病患形成競爭護城河（原話："there's a bit of a competitive moat around that"）
- 2026-08-06｜Douglas Coltharp｜competition：北卡進入策略強調先行者優勢（原話："we felt that first-mover advantage was"）
- 2026-08-06｜Mark Tarr｜competition：北卡將以自有與合資混合方式進入（原話："you could count on a mixture of some wholly owned and some"）
- 2026-08-06｜Douglas Coltharp｜competition：管理層說明同店與總出院量的區分重要性下降（原話："distinction between same-store and total discharge growth"）
- 2026-08-06｜Mark Tarr｜competition：北卡廢除 CON 的生效資訊（原話："North Carolina repealed its Certificate of Need law"）
- 2026-08-06｜Mark Tarr｜competition：北卡初步優先鎖定的市場數（原話："This has led to an initial prioritization of 15 markets"）
- 2026-08-06｜Patrick Tuer｜product：中風出院量成長（同店口徑另列）（原話："Those were up 7.9% and 8%, respectively, on a same-store"）
- 2026-08-06｜Douglas Coltharp｜product：髖膝關節置換類別成長（原話："was up only modestly, about 1% in the quarter."）
- 2026-08-06｜Patrick Tuer｜product：VA 業務 Q2 成長率（原話："we hit VA growth of around 33%"）
- 2026-08-06｜Douglas Coltharp｜product：新院平均損益轉正與入住率爬坡節奏（原話："4-wall positive EBITDA by the time they hit month 6"）
- 2026-08-06｜Douglas Coltharp｜product：AI／Palantir 效益多半仍在未來（原話："I think a lot of it is still in front of us"）
- 2026-08-06｜Mark Tarr｜product：Q2 開幕的新院（原話："we opened a new 50-bed hospital in Concordville"）
- 2026-08-06｜Douglas Coltharp｜risk：Medicare Advantage 事前授權拒付仍是挑戰（原話："denials through pre-authorization from Medicare Advantage"）
- 2026-08-06｜Douglas Coltharp｜risk：admit-and-appeal 試行勝訴率數字（原話："of that 144, we have prevailed on 128, which is"）
- 2026-08-06｜Douglas Coltharp｜risk：加州 RCD 的 MAC 準備不足（原話："the MAC was less well prepared than we would have hoped for"）
- 2026-08-06｜Patrick Tuer｜customer：護理離職率降至 12 年以上低點（原話："our nursing turnover sits around 19%"）
- 2026-08-06｜Patrick Tuer｜customer：career ladder 參與度（原話："we are up to 43% of eligible RNs"）
- 2026-08-06｜Douglas Coltharp｜customer：Q2 超過 90% 入住率的醫院數（原話："In Q2, we had 60 hospitals at greater than 90%"）
- 2026-08-06｜Patrick Tuer｜customer：COO 稱此為近年最佳招募季度（原話："this was our best hiring"）

### 問答異常語氣（迴避／改口／保留）
- EHC_Q2_2026_Earnings_Call_20260806.md｜問：Andrew Mok：同店出院量成長是否優於內部預期；若高敏銳度類別會持續，為何不願說敏銳度增益可持續｜答法：拒絕回答是否優於內部預期（只對照財測）；對敏銳度可持續性改談同店口徑不重要與波動，COO 稱不願被「逼到牆角」
- EHC_Q2_2026_Earnings_Call_20260806.md｜問：Pito Chickering：下半年同店出院量是否應模型化為 4% 以上｜答法：未給數字，改談同店與總出院量區分漸不重要、較易比較基期與新增產能
- EHC_Q2_2026_Earnings_Call_20260806.md｜問：A.J. Rice：SWB 上調是否僅今年，或長期以更高工資換較低離職｜答法：稱僅是今年假設，明年增幅預期放緩，但拒絕給出水準

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
{"date":"20260525","verdict":"B 衛星候選（護城河 8/10 B 級頂端 + 估值 🟢 便宜 Fwd PE 16x 5Y 分位 22%；但 Pure MA 🟡 觀察池修復中 + Rosen class action 未結案 🟡 兩項時機訊號疊加 → 等 W52 斜率轉正 + 訴訟 motion to dismiss 解除任一觸發後可升 A）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"2026-2028 新院 ramp 順利且新建總 capex IRR > 15%","columns":{"2Y 驗證點":"2026 開 8 新院 + 175 擴床如期完工；新院首年 occupancy ≥ 65%","5Y 驗證點":"2028 ROIC 維持 14-15%（capex peak 過後）；2030 IRF 床數較 2025 +25%（即 +1900 床）","10Y 驗證點":"2030 維持 30%+ IRF 市佔；新院第 4 年 occupancy ≥ 78%（與成熟院相當）","具體數字門檻":"2026 capex $675-725M / 新院 8 家全完工；首年新院 occupancy ≥ 65%；ROIC ≥ 14%","信息來源":"5/1 Q1 26 法說 + 2026 guidance；2025 10-K p.42","漂移觸發條件":"連 2 季 TTM occupancy"}},{"id":"H2","text":"IRF-PPS Medicare rate update 持續正向（2026 +2.6%，未來年化 +2% ~ +3%）","columns":{"2Y 驗證點":"2027 IRF-PPS proposed rule（4 月）顯示 rate update ≥ 1.5%","5Y 驗證點":"2028-2030 累積 rate update ≥ 8%（年化 ≥ 2.5%）","10Y 驗證點":"2030+ Medicare-for-All 或 MA bundled payment 未顛覆 fee-for-service IRF-PPS 架構","具體數字門檻":"年度 rate update ≥ 1.5% 為門檻；","信息來源":"CMS-1829-F（FY2026 final rule, Aug 2025）；前 5Y 平均 rate update +2.3%","漂移觸發條件":"連 2 年 rate update"}},{"id":"H3","text":"估值倍數從當前 16x 修復至 19-20x（capex 期過 + 監管疑雲消化）","columns":{"2Y 驗證點":"2027 末 Fwd PE 修復至 18x 以上","5Y 驗證點":"2028+ Fwd PE 19-20x（5Y 中位）","10Y 驗證點":"不適用（10Y 倍數本就 mean-revert）","具體數字門檻":"Fwd PE 修復至 18x 以上、PEG 修復至 1.5 以下","信息來源":"§13.1 歷史分位；StockAnalysis 5Y forward PE 區間","漂移觸發條件":"連 4 季 Fwd PE"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"新院 ramp 慢 + capex 浪費","columns":{"對應假設":"H1","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"新院首年 occupancy；ROIC 趨勢；growth capex 占營收比","警戒閾值":"新院首年 occupancy 15% 連 2 年 → 警戒；ROIC 跌破 13% → 反轉"}},{"id":"R2","text":"IRF-PPS rate update 結構性下降","columns":{"對應假設":"H2","時間尺度標記":"🐢 長期（2+ 年慢變數）","監測指標":"每年 4 月 proposed rule；MA 占 Medicare 比例變化；CMS 對 IRF 60% Rule 政策動態","警戒閾值":"連 2 年 rate update"}},{"id":"R3","text":"Class action 訴訟惡化 + 監管罰款","columns":{"對應假設":"H3、品質保證","時間尺度標記":"⚡ 短期（1-2 季可觸發）","監測指標":"Rosen / Levi 案 motion to dismiss 結果；SEC 公開調查公告；CMS 對個別醫院的監管動作","警戒閾值":"motion to dismiss 被駁回 → ⚡ 立即修正 trap 至 🔴；SEC 啟動正式調查 → ⛔ 重評至 X；多家醫院被 CMS 暫停 Medicare 認證 → ⛔"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":104.96,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EHC_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
