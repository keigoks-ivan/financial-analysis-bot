你是 stock-analyst **v20 判斷 agent**，標的 STM（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"STM","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_revenues_gaap","label":"Net revenues (GAAP)","value":3757,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"}},{"id":"f_kpi1_non_gaap_operating_incom","label":"Non-GAAP operating income / margin","value":429,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"US$M（利益率 11.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":367,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"US$M（利益率 9.8%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"}},{"id":"f_kpi3_free_cash_flow_non_gaap","label":"Free cash flow (non-GAAP)","value":351,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"US$M（營運現金流 1,020；淨資本支出 643）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"}},{"id":"f_kpi4_gross_margin_gaap","label":"Gross margin (GAAP)","value":37.3,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"}},{"id":"f_kpi5_inventory_days_dsi","label":"Inventory days (DSI)","value":126,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"days（存貨 US$3.25B）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"}},{"id":"f_kpi6_guidance_q4_2026_revenue","label":"Guidance Q4 2026 revenue (midpoint)","value":4150,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"US$M（±350bps，約 4,005–4,295 為區間推算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"},"note":"Q4 共識營收約 4.10B（來源：web_search 報導引 LSEG，未直接核對）"},{"id":"f_kpi7_guidance_q4_2026_gross_m","label":"Guidance Q4 2026 gross margin (midpoint)","value":39.0,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"%（±200bps，含約 40bps 閒置產能費用）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"}},{"id":"f_kpi8_guidance_fy2026_revenue","label":"Guidance FY2026 revenue","value":14500,"period":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","unit":"US$M（約，YoY +22.8%；毛利率 GAAP 約 36.4%／non-GAAP 約 36.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-26，公告於 2026-10-29）","citation":"公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_stm_gross_margin_pct","label":"STM 毛利率","value":33.84,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STM.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_stm_operating_margin_pct","label":"STM 營業利益率","value":6.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STM.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_stm_fcf_margin_pct","label":"STM FCF 利潤率","value":3.77,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STM.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nxpi_gross_margin_pct","label":"NXPI 毛利率","value":56.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nxpi_operating_margin_pct","label":"NXPI 營業利益率","value":28.55,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nxpi_fcf_margin_pct","label":"NXPI FCF 利潤率","value":24.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_txn_gross_margin_pct","label":"TXN 毛利率","value":60.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_txn_operating_margin_pct","label":"TXN 營業利益率","value":41.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_txn_fcf_margin_pct","label":"TXN FCF 利潤率","value":35.24,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_on_gross_margin_pct","label":"ON 毛利率","value":37.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_on_operating_margin_pct","label":"ON 營業利益率","value":18.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_on_fcf_margin_pct","label":"ON FCF 利潤率","value":24.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_adi_gross_margin_pct","label":"ADI 毛利率","value":65.8,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_adi_operating_margin_pct","label":"ADI 營業利益率","value":35.72,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_adi_fcf_margin_pct","label":"ADI FCF 利潤率","value":35.57,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":46.74,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-15.92,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.92,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.34 → 1.34）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":1.5,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.66 → 2.7）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.26,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（3.78 → 3.79）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":1.34,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":2.7,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":3.79,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-1.47,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 1.36 → 1.34（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":82.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝51.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":51.8,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.06,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.9,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":34.88,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 1.34，分子＝快照價 46.74","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.77,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-2106.0,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 3206.0、現金 5312.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":894.41,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":39698.95,"period":"2026-11-02","unit":"USD m","basis":"市值 41804.95 ＋ 淨負債 -2106.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":14497.18,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":17372.99,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":2.74,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 46.74 / W52 44.9 / W104 35.15 / W250 37.73 / W250 13週斜率 -0.01%"},{"id":"f_ma_w52","label":"52 週均線","value":44.9,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":35.15,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":37.73,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":-0.01,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"ST 20-F 自述：競爭激烈，產業整併可能侵蝕市占；小型利基業者與（特別在亞洲的）晶圓代工業者участations明顯擴張。","source":"SEC EDGAR 20-F FY2025 Item 4 Competition","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"Smaller niche companies are also increasing their participation in the semiconductor market, and semiconductor foundry companies have expanded significantly, particularly in Asia.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"ST 20-F 風險因子：整併可能導致市占流失，並需重組營運。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"the competitive environment of the industry has resulted, and is expected to continue to result, in vertical and horizontal consolidation among our suppliers, competitors and customers, which may lead to erosion of our market share","as_of":"2026-02-26","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1/Q2 2026 財報會議逐字稿摘要：ST 自述在車用（OBC、動力、主動懸吊）與工業等領域取得設計案（design wins）；摘要來自第三方轉錄站，未核原文。","source":"MarketBeat STMicroelectronics Q2 2026 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2026-7-24-stmicroelectronics-stock/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"中國本土 OEM（BYD、Nio、Geely、Xiaomi）擴大 SiC 布局，本土競爭升溫，ST 走在地化合資","source":"Astute Group","url":"https://www.astutegroup.com/?p=53946","excerpt":"Facing rising local competition, the firm has gone local to stay relevant—“become Chinese in China,” as Yole calls it. A $3.2 billion SiC joint venture with Sanan Optoelectronics, a manufacturing partnership with Hua Hong for automotive MCUs, and a stake in GaN leader Innoscience all","as_of":"2025-04-15","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"STM 20-F FY2025 揭露：最大客戶 Apple 占 2025 年營收 17.7%；近年部分客戶垂直整合，可能影響業務，失去關鍵客戶或重要 socket 會有不利影響。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"In recent years, some of our customers have vertically integrated their businesses. Such vertical integrations may impact our business.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"20-F 競爭章節列明競爭者包括自行開發 IC 產品與晶圓廠營運的客戶，部分競爭者同時是客戶或供應商。","source":"SEC EDGAR 20-F FY2025 Item 4","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"Competitors include manufacturers of standard semiconductor devices, ASICs and fully customized ICs, including both chip and board-level products, as well as customers who develop their own IC products and foundry operations. Some of our competitors are also our customers or suppliers.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Bloomberg 報導（經 Finanzaonline 轉述）：Apple 招募工程師自研無線/RF 晶片，Equita 分析師認為對 Apple 供應鏈含 STM 為負面，STM 股價當日跌近 3%。","source":"Finanzaonline: STMicroelectronics in caduta a Piazza Affari, Apple potrebbe sviluppare chip internamente","url":"https://www.finanzaonline.com/notizie/stmicroelectronics-in-caduta-a-piazza-affari-apple-potrebbe-sviluppare-chip-internamente","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025 年最大客戶 Apple 占 STM 營收 17.7%（2024 年 14.5%、2023 年 12.3%），逐年上升；公司稱不依賴單一客戶，但失去關鍵客戶或重要 socket 會有不利影響","source":"SEC EDGAR 20-F FY2025 Item 3 / Item 5","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"In 2025 our largest customer, Apple, accounted for 17.7% of our total revenues. While we do not believe to be dependent on any one customer or group of customers, the loss of key customers or important sockets at key customers could have an adverse effect on our results of operations and financial condition.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"截至 2025 與 2024 年底，無單一客戶占應收帳款淨額超過 10%，銷貨主要以現金結算，信用風險集中度有限","source":"SEC EDGAR 20-F FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"As of December 31, 2025 and 2024, no individual customer represented more than 10% of trade accounts receivable, net. Any remaining concentrations of credit risk with respect to trade receivables are limited due to the large number of customers and their dispersion across many geographic areas.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"券商估計 Apple 2026 年占 STM 營收約 15%（2025 年 17%）","source":"Websim - STMicroelectronics Apple riduce gli ordini per iPhone","url":"https://www.websim.it/azioni/blue-chip/stmicroelectronics-apple-riduce-gli-ordini-per-iphone/","excerpt":"Secondo indiscrezioni di stampa, Apple avrebbe ridotto gli ordini relativi alla gamma iPhone 18 Pro, in un contesto caratterizzato dall'aumento dei costi delle memorie e di altre componenti. Effetto Stimiamo che Apple rappresenterà circa il 15% dei ricavi di STM nel 2026 (dal 17% nel 2025) e che il business legato al cliente cresca di circa il 9%,","as_of":"2026-10-13","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Wolfe Research 分析師認為半導體(以記憶體為主)在 2028 年前幾乎不可能供過於求；結論主要針對記憶體，非類比/MCU。","source":"247WallSt: Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/?.tsrc=rss","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"搜尋摘要指出記憶體以外的半導體定價已大致正常化，2020–2023 的廣泛缺貨對多數晶片類別已結束(摘要彙整，非單一來源原文)。","source":"WebSearch 彙整：Semiconductor Capacity Crunch 2026 (TechInsights) 等","url":"https://techinsights.com/ja/node/61472","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"TrendForce 指新一波記憶體產能多自 2028 年後才釋出；新產能建置通常 3–5 年。","source":"TrendForce News (Oct 2026)","url":"https://www.trendforce.com/news/?p=64868","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"STM 2026 Q1 財報時 CEO Chery 稱需求回升、訂單強勁、庫存正常化；Q2 營收中值約 34.5 億美元。","source":"AWP via vermoegenszentrum.ch: STMicro sieht anziehende Nachfrage","url":"https://www.vermoegenszentrum.ch/boersen-und-maerkte/news/stmicro-sieht-anziehende-nachfrage-aktie-springt","excerpt":"the company recorded a demand recovery in the first quarter with strong order numbers and normalized inventories, CEO Jean-Marc Chery reported in Geneva on Thursday.","as_of":"2026-04-23","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"BofA 預期 2027 年運算、網通、記憶體供應商訂單近乎滿載、2028 仍偏緊；此為 AI 相關需求，非 STM 的類比/功率市場。","source":"Estrategias de Inversión: Bank of America previsión semiconductores","url":"https://www.estrategiasdeinversion.com/actualidad/noticias/bolsa-eeuu/bank-of-america-realiza-una-gran-prevision-para-n-950817","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"20-F FY2025 將反壟斷、競爭法列為尚未演變成訴訟的法律風險；重大訴訟見 Note 26，未見反壟斷調查或拆分的專述。","source":"SEC EDGAR 20-F FY2025 Item 5","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"We are also exposed to numerous legal risks which until now have not resulted in legal disputes and proceedings. These include risks related to product recalls, environment, shareholder rights, tariffs and export control regulations, anti-trust, anti-corruption, competition as well as other compliance regulations.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"產業監管：美國商務部依 232 條款對進口半導體啟動國安調查，可能帶來額外關稅與貿易限制。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"in April 2025, the Department of Commerce launched an investigation into the national security impacts of imported semiconductors and semiconductor manufacturing equipment. This investigation may result in additional tariffs and trade restrictions that may adversely impact the semiconductor industry and our business.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"網路搜尋未找到 2026 年針對 STM 的反壟斷調查；僅見 2008–2009 年歐盟智慧卡晶片卡特爾調查舊案。","source":"WebSearch 結果摘要（newelectronics.co.uk 等）","url":null,"excerpt":null,"as_of":"2026-02-26","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"STM 20-F 風險因子載明：美中關稅、出口限制與實體清單已限制或可能限制其與部分中國客戶／供應商交易；並點名美國威脅的 100% 晶片關稅與中國相關出口管制。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"In addition, we may be subject to the imposition of sector-specific tariffs, such as the 100% tariff on imported, foreign-produced semi-conductor chips threatened by the current U.S. administration, or China’s related export controls.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"20-F 載明 2025 年 4 月美國商務部啟動半導體及設備進口的 Section 232 國安調查，可能帶來額外關稅與貿易限制。","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"For example, in April 2025, the Department of Commerce launched an investigation into the national security impacts of imported semiconductors and semiconductor manufacturing equipment. This investigation may result in additional tariffs and trade restrictions that may adversely impact the semiconductor industry and our business.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"公司 2026 Q1 財測未計入全球關稅潛在進一步變動的影響。","source":"SEC EDGAR 20-F FY2025 Item 5","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"This business outlook does not include any impact from potential further changes to global trade tariffs compared to the current situation","as_of":"2026-02-26","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 總統公告對特定先進半導體課 25% Section 232 關稅，範圍狹窄，工業等用途有豁免；是否涵蓋 STM 產品未見來源。","source":"White & Case: narrowly targeted 25% Section 232 tariff","url":"https://www.whitecase.com/insight-alert/president-trump-orders-narrowly-targeted-25-section-232-tariff-certain-advanced","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"ST 2026 資本支出計畫涵蓋義大利 Catania 200mm SiC、與三安光電在中國重慶的 200mm SiC 合資廠、法國 Crolles 300mm、義大利 Agrate 300mm；2026 淨資本支出落在 20–22 億美元區間高端（來自搜尋摘要轉述，未核頁面原文）","source":"STMicroelectronics Form 6-K Semi-Annual Report 2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000069/stm_sarxmaster-semiannual2.htm","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ST 申報文件將地緣與軍事衝突列為其、客戶或供應商所在地區營運風險，並將關稅、貿易壁壘與制裁列為需求風險（屬一般性風險語言，非特定廠區評估）","source":"STMicroelectronics Form 6-K Q2 2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000058/stm-6k_q2x2026.htm","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ST 20-F 揭露其依賴少數供應商取得材料、設備與授權技術，部分材料僅來自單一地區少數供應商（摘要轉述自歷年 20-F，未核 FY2025 頁面原文）","source":"STMicroelectronics Form 20-F FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"STM Q3 2026 net revenue $3.76B (+17.9% YoY); segments YoY: AM&S $1,560M +8.8%, P&D $477M +11.3%, EMP $1,212M +24.1%, RFOC $504M +46.2%; P&D operating loss widened from $67M to $81M; Q4 guide midpoint $4.15B, GM 39.0%","source":"STMicroelectronics Form 6-K Q3 2026 earnings press release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 call: book-to-bill close to 2, demand and backlog exceed capacity; overall pricing expected broadly flat to slightly higher (easier for distribution/STM32, large customers contract-set); may lose some share at existing customers as new suppliers enter; data-center revenue >$1B in 2026 and well above $2B in 2027","source":"Nasdaq: STMicroelectronics Q2 Earnings Call Highlights AI Data Center Growth","url":"https://www.nasdaq.com/articles/stmicroelectronics-q2-earnings-call-highlights-ai-data-center-growth","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261102","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"WSTS Q2 2026 update: H1 2026 market $702B (+102% YoY); 2027 about $2.1T (~29% growth), memory-led; spring forecast 2026 about $1.51T","source":"WSTS Global Semiconductor Market records exceptional growth in Q2 2026","url":"https://www.wsts.org/76/Global-Semiconductor-Market-records-exceptional-growth-in-Q2-2026","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"STM 20-F 自述半導體產業技術變動快、產品週期短、價格侵蝕大，公司財務表現取決於能否掌握 AI、量子等新技術機會；未點名具體替代技術。","source":"SEC EDGAR 20-F FY2025 Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"The semiconductor industry is highly competitive and characterized by constant and rapid technological change, short product lifecycles, significant price erosion and evolving standards. Accordingly, our financial performance and future prospects depend to a significant extent on our ability to develop and maximize the opportunities offered by new technologies available to our industry, such as AI or quantum.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 經銷通路占營收 28%（2024 為 27%、2023 為 34%），通路結構近兩年大致穩定，未見結構性轉移；OEM 72%。","source":"SEC EDGAR 20-F FY2025 Item 5","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"By market channel, our 2025 net revenues in Distribution amounted to 28% of our total consolidated revenues, increasing from 27% in 2024. When comparing 2024 with 2023 figures, net revenues in Distribution had decreased by 7%, from 34% to 27%.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"公司銷售組織以大客戶與區域銷售為主，大眾市場與經銷夥伴合作；區域銷售行銷組織維持不變，無商業模式轉型（訂閱／D2C）揭露。","source":"SEC EDGAR 20-F FY2025 Item 4","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"The regional Sales & Marketing organization remained unchanged. We engage distributors and sales representatives to distribute and promote our products around the world.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026 上半年經銷占營收 29%（去年同期 28%）；Q2 財報稱經銷庫存低於標準目標。","source":"SEC EDGAR 6-K Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000058/stm-6k_q2x2026.htm","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 營收約 37.6 億美元，高於公司指引中點約 150bp；Q4 指引中點 41.5 億美元（季增約 10.5%、年增約 24.7%），毛利率約 39.0%；隱含 2026 全年營收約 145 億美元。","source":"STMicroelectronics Q3 2026 earnings press release (Form 6-K, SEC) / capital.com","url":"https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm","excerpt":null,"as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Bullstory 彙整：13 位分析師平均目標價 $71.52（高 $98／低 $32.80），as-of 2026-08-19；Tickflow：9 位分析師平均 $74.83（資料 2026-08-01）；Benzinga 情緒頁（約 10-08 更新）平均 $56（高 $83／低 $26）。各家聚合站數字不一致。","source":"Bullstory / Tickflow / Benzinga","url":"https://bullstory.io/en/stocks/stm/forecast/analyst-rating","excerpt":null,"as_of":"2026-08-19","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 財報（2026-07-23）後 Q3 營收指引中點約 37 億美元，被報導為低於分析師預期，股價下跌；Barclays 於 2026-07-24 將目標價降至 $60。","source":"goldesel.de / GuruFocus 引述 / Barclays 調整","url":"https://goldesel.de/aktien/news/stmicroelectronics-aktie-sturzt-nach-schwacher-q3-guidance-q2-gewinn-aber-markt-bleibt-skeptisch","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Citigroup 於 2026-09-02 將目標價自 €62 調升至 €65，維持 Buy；Equita 2026-09-17 因利率因素調降目標價並維持 Buy。","source":"Teleborsa / borsaitaliana.it；FMP","url":"https://www.borsaitaliana.it/borsa/notizie/teleborsa/finanza/stm-equita-abbassa-target-price-per-effetto-tassi-e-conferma-buy-prima-dei-conti-87_2026-09-17_TLB.html?lang=it","excerpt":null,"as_of":"2026-09-17","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"ST 於 2026-02-02 完成收購 NXP MEMS 感測器業務，總額最高 9.5 億美元（交割 9 億＋5,000 萬里程碑），2024 年營收約 3 億美元。","source":"ST 6-K／新聞稿（SEC EDGAR）NXP MEMS closing","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000005/st_nxpmemsclosingxprxfinal.htm","excerpt":null,"as_of":"2026-02-02","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"SDNY 證券集體訴訟（2024-08-23 起，涵蓋期間擴至 2023-03-14～2025-01-29，指控 10(b)/20(a)）；法院 2025-09-15 駁回公司撤銷訴訟聲請，公司稱將積極抗辯。","source":"SEC EDGAR 20-F FY2025 Note 26","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"The Company and its CEO and CFO moved to dismiss the lawsuit which motion was denied by the Court on September 15, 2025. The Company and its CEO and CFO believe that they have strong legal defenses against the allegations in the amended complaints and will vigorously defend themselves in court.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Purdue University 專利侵權案：2024-06-07 法院判決公司賠 3,200 萬美元，公司提出審後動議，風險評為 possible，估計損失 3,200 萬美元。","source":"SEC EDGAR 20-F FY2025 Note 26","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"On June 7, 2024, the Court accepted the jury's verdict and entered a judgment against the Company in the amount of $32 million.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"TSMC 2026 capex 計畫被報導由 52-56 億美元上調約 15% 至 60-64 億美元（原文單位為 billion）；Intel 2026 capex 升至 200 億美元、2027 將明顯更高；SK hynix 2026 capex 40 兆韓元、年增約 45%（皆為聚合站轉述 JPMorgan 彙整，非一手財報）","source":"iTiger: Semiconductor Earnings Season Signals Stronger Demand and Expanding Pricing Power","url":"https://www.itiger.com/news/1189767091","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"TrendForce 預期 2026 記憶體 capex 僅溫和成長（DRAM 約 613 億美元、約 +14%），多數供應商在多年景氣波動後對 capex 與擴產較審慎（記憶體產業，非 STM 直接同業）","source":"TrendForce / StorageNewsletter: Memory industry to maintain cautious capex in 2026","url":"https://www.storagenewsletter.com/2025/12/31/memory-industry-to-maintain-cautious-capex-in-2026/","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"STM 自身 2026 淨 capex 約 22 億美元，用於雲端光互連等成長驅動產能；同時依製造重整計畫縮減 6 吋/150mm SiC 與 200mm 矽產能，轉向 8 吋 SiC 與 300mm 矽；CEO 稱 Crolles 擴產決定預計在年底前做出（後者出自次級新聞站）","source":"STMicroelectronics Form 6-K FY2026 (Q2 2026) / 次級新聞站","url":"https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000058/stm-6k_q2x2026.htm","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261102","affects":["thesis.H","triggers"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"TSMC 2026 capex 約 560 億美元，CEO 稱晶片短缺將持續至 2027 年後","source":"Longport: Taiwan Semiconductor Invests $56 Billion in Expansion","url":"https://longportapp.cn/news/283506138","excerpt":null,"as_of":"2026-04-16","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"BNP Paribas 描述工業類半導體處於庫存從極低水位回補的循環；2026–2027 市場成長主要來自價格而非數量；車用復甦預期到 2027。","source":"BNP Paribas CIB, Semiconductor market 2026: it is not solely about AI","url":"https://cib.bnpparibas/semiconductor-market-2026-it-is-not-solely-about-ai/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Gartner 3Q26 庫存預測：庫存指數仍在中度短缺區，季減 2.1%，主因記憶體、AI 晶片、先進製程運算短缺（非類比/MCU）。","source":"Gartner Insights Abstract (3Q26 inventory forecast)","url":"https://www.gartner.com/en/documents/8515377","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce 2026年4月報告：PC DRAM 合約價仍漲但動能減弱，現貨市場趨穩；6月項目預期下半年合約價成長放緩（記憶體資料，非 ST 產品線）。","source":"TrendForce DRAM Contract Price Apr. 2026","url":"https://www.trendforce.com/research/download/RP260430QO","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"ST Q2 2026：CEO 稱通路庫存已低於標準目標；總庫存 $3.19B，DSI 126天（前季140、去年同期166）。","source":"ST Q2 2026 earnings release / investors.st.com","url":"https://investors.st.com/node/18966/pdf","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261102","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"STM 毛利率 2023 年 47.9% → 2024 年 39.3% → 2025 年 33.9%，2025 年降幅主因製造效率下降","source":"STMicroelectronics Form 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"STM 2025 Q1 毛利率 33.4%，CEO 稱該季為底部；Q2 2025 為 33.5%","source":"Malta CEOs: q1 2025 was the bottom says STMicroelectronics president and ceo","url":"https://maltaceos.mt/q1-2025-was-the-bottom-says-stmicroelectronics-president-and-ceo","excerpt":null,"as_of":"2025-04-24","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"半導體族群上一輪下行：SOXX ETF 2021-12-27 至 2022-10-14 約跌 46%；另一來源稱 2022 全年約跌 35%（兩者不一致）","source":"247wallst / Yahoo Finance: SOXL Lost 90 Percent in 2022 While Semiconductors Themselves Fell 35 Percent","url":"https://finance.yahoo.com/markets/options/articles/soxl-lost-90-percent-2022-220016228.html","excerpt":"From December 27, 2021 to October 14, 2022, the unleveraged iShares Semiconductor ETF fell about 46%.","as_of":"2026-05-26","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"歷史週期長度：1992–1996 約 4 年（銷售 -26%）、1998–2001 約 2 年（銷售 -46%）；Micron 前兩輪下行以 EBITDA 利潤率計為 7 與 9 季","source":"semiwiki / Seeking Alpha 'Micron: How Low Will It Go?'","url":"https://seekingalpha.com/article/4231388-micron-how-low-will-it-go","excerpt":null,"as_of":"2019-01-01","retrieved_at":"20261102","affects":["thesis.R","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"ST 於 2026-02-02 完成收購 NXP MEMS 感測器業務，總額最高 9.5 億美元。","source":"ST 6-K（SEC EDGAR）NXP MEMS closing","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000005/st_nxpmemsclosingxprxfinal.htm","excerpt":null,"as_of":"2026-02-02","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"SDNY 證券集體訴訟撤銷聲請於 2025-09-15 被駁回，案件續審。","source":"SEC EDGAR 20-F FY2025 Note 26","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"The Company and its CEO and CFO moved to dismiss the lawsuit which motion was denied by the Court on September 15, 2025.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Purdue 專利案判賠 3,200 萬美元，審後動議進行中。","source":"SEC EDGAR 20-F FY2025 Note 26","url":"https://www.sec.gov/Archives/edgar/data/932787/000093278726000009/stm-20251231.htm","excerpt":"On June 7, 2024, the Court accepted the jury's verdict and entered a judgment against the Company in the amount of $32 million.","as_of":"2026-02-26","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 15 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"STM","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":33.84,"operating_margin_pct":6.64,"fcf_margin_pct":3.77,"rd_intensity_pct":14.56},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STM","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"NXPI","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.43,"operating_margin_pct":28.55,"fcf_margin_pct":24.16,"rd_intensity_pct":17.92},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NXPI","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"TXN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.24,"operating_margin_pct":41.12,"fcf_margin_pct":35.24,"rd_intensity_pct":10.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"ON","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.72,"operating_margin_pct":18.05,"fcf_margin_pct":24.21,"rd_intensity_pct":9.05},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ON","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ADI","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":65.8,"operating_margin_pct":35.72,"fcf_margin_pct":35.57,"rd_intensity_pct":14.24},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ADI","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"STM"},"financial_history":{"ticker":"STM","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":16128000000.0,"revenue_yoy_pct":null,"gross_margin_pct":47.34,"operating_margin_pct":26.54,"net_income":3960000000.0,"diluted_eps":4.74,"free_cash_flow":1566000000.0,"fcf_margin_pct":9.71,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":17286000000.0,"revenue_yoy_pct":7.18,"gross_margin_pct":47.94,"operating_margin_pct":26.36,"net_income":4211000000.0,"diluted_eps":4.46,"free_cash_flow":1456000000.0,"fcf_margin_pct":8.42,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":13269000000.0,"revenue_yoy_pct":-23.24,"gross_margin_pct":39.34,"operating_margin_pct":11.26,"net_income":1557000000.0,"diluted_eps":1.66,"free_cash_flow":-216000000.0,"fcf_margin_pct":-1.63,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":11800000000.0,"revenue_yoy_pct":-11.07,"gross_margin_pct":33.89,"operating_margin_pct":2.74,"net_income":166000000.0,"diluted_eps":0.18,"free_cash_flow":-52000000.0,"fcf_margin_pct":-0.44,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STM/STM_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**STMicroelectronics N.V.** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Ladies and gentlemen, welcome to the STMicroelectronics Third Quarter 2026 Earnings Release Conference Call and Live Webcast. I am Sandra, the Chorus Call operator. [Operator Instructions] The conference is being recorded. The conference must not be recorded for publication or broadcast. At this time, it is my pleasure to hand over to Jerome Ramel, EVP, Corporate Development and Integrated External Communications. Please go ahead, sir.

**Jerome Ramel** (Executives):
Thanks, Sandra, and thank you, everyone, for joining our third quarter 2026 financial results call. Hosting the call today is Jean-Marc Chery, ST President and Chief Executive Officer; joining Jean-Marc on the call are Lorenzo Grandi, President and CFO; and Remi El-Ouazzane, President, Microcontroller, Digital ICs and RF Product Group. This live webcast and presentation materials can be accessed on ST Investor Relations website. A replay will be available shortly after the conclusion of this call. This call will include forward-looking statements that involve risk factors that could cause ST results to differ materially from management expectations and plans. We encourage you to review the safe harbor statement contained in the press release that was issued with the results this morning and also in ST's most recent regulatory filings for a full description of these risk factors. [Operator Instructions] Now I'd like to turn the call over to Jean-Marc Chery, ST President and CEO.

**Jean-Marc Chery** (Executives):
Thank you, Jerome. Good morning, everyone, and thank you for joining ST for our Q3 2026 earnings conference call. I will start with an overview of the third quarter, including business dynamics. And I will hand over to Lorenzo for the detailed financial overview. I will then comment on the outlook and conclude before answering your question. So starting with Q3. Our third quarter net revenues of $3.76 billion came in above the midpoint of our business outlook range, mainly due to higher revenue in Communication Equipment and Computer Peripheral, driven by AI datacenter and lower Earth orbit satellite revenues, communication and personal electronics. Gross margin was 37.3%, above the midpoint of our business outlook range. Non-U.S. GAAP diluted earnings per share was $0.37. 
During the third quarter, inventory in our balance sheet increased slightly to support the expected increase in Q4 revenues. In distribution, inventory decreased and continued to track below our standard target. We generated positive free cash flow of $351 million. Let's now discuss our business dynamics during Q3. During the quarter, the ongoing recovery and secular growth across the end markets we serve continued to gain momentum. Demand strengthened further in Q3 with bookings increasing sequentially and book-to-bill remaining well above 2 overall. Book-to-bill was well above 1 in all end markets and significantly above 2 in Communication Equipment and Computer Peripheral and Industrial. Visibility improved. Inventory distribution continued to track below our standard target and demand continued to outpace supply across multiple product categories. 
Automotive revenues were stable sequentially and increased 5% year-over-year. Our solid position in automotive continued to be driven by application-specific ICs and sensors for core application, electrical powertrain and ADAS. We maintained our automotive design win momentum with OEMs and Tier 1 suppliers across the portfolio of ST product families, including microcontrollers and Power & Discrete. These wins covered hybrid, electric and internal combustion engine vehicles in areas including onboard charging, powertrain and active suspension as well as a first award for 48-volt electromechanical braking. We made progress with our automotive MEMS business, supported by the successful integration of NXP's MEMS sensors, achieving several key customer awards in telematics, cockpit control and tire pressure monitoring. We had another important design win with our in-cabin monitoring solutions, and we introduced a new automotive image sensor for infrared in-cabin sensing, designed to extend driver and occupant monitoring across more vehicle models. 
Industrial revenues improved 12% sequentially and 40% year-over-year. This solid growth was mainly driven by our general purpose microcontrollers, analog and power conversion products. During Q3, the broad-based recovery in industrial continued and inventory in distribution declined further remaining below our standard target. We had design wins across industrial automation, robotics, power systems, building automation, power tools and home appliances. Our portfolio combines intelligent sensing, real-time control and efficient power management to support the transformation of factory automation, robotics and power energy infrastructures and the growing physical AI market. At the Embedded World North America event, we had a demonstration together with NVIDIA, illustrating our broad cooperation on robotics. We showed an integrated robotics development path from digital twin to deployed application based on our inertial sensors, microcontrollers and imaging solutions. 
We are continuing to strengthen these capabilities with new products. Our latest launch is a miniature 6-axis motion sensor with a machine learning core designed to improve accident alerts, robot teaching, board stabilization and structural monitoring. By bringing AI processing into the sensor, systems can reduce energy use and save resources. In embedded processing, we continue to expand our STM32 offering with a strong pipeline of new products and software innovations. You will hear more about this at our STM32 Summit on November 3, followed by a dedicated STM32 analyst call on November 18. For Personal Electronics, third quarter revenues came in better than expected, up 12% sequentially and down 4% year-over-year. During the quarter, we had design wins with secure solutions, MEMS and imaging sensors and microcontrollers across a variety of devices, including smartphones, gaming headsets, earbuds and smart rings. 
For Communication Equipment and Computer Peripherals, third quarter revenues were above expectation, increasing 14% sequentially and 64% year-over-year. This strong growth mainly reflected the contribution of our company-specific growth drivers in AI datacenter and low Earth orbit satellite communications. For AI datacenters, we continue to see strong demand driven mainly by our silicon photonic ICs, electronic ICs and microcontrollers as well as power solutions. This supports our revenue expectation for 2026 of about $1.3 billion and assuming the current dynamic continues and with the current engagements we have, our revenue ambition of well above $2 billion in 2027 and further growth beyond. Now over to Lorenzo, who will present our key financial figures.

**Lorenzo Grandi** (Executives):
Thank you, Jean-Marc. Good morning, everyone. Let's start with a detailed review of the third quarter, starting with revenues on a year-over-year basis by reportable segment. Analog products, MEMS and Sensor grew 8.8%, mainly due to MEMS and to a lesser extent, analog and imaging. Power & Discrete products increased 11.3%. Embedded Processing revenues were up 24.1%, mainly due to general purpose microcontrollers and RF & Optical Communication grew 46.2% -- by end market, Communication Equipment and Computer Peripheral grew 64%; Industrial, 40%; and Automotive 5%, while Personal Electronics decreased 4%. Year-over-year, sales to OEMs and distribution increased 10.2% and 38.8%, respectively. On a sequential basis, by reportable segment, Analog Product, MEMS and Sensor increased by 9.4%, Power & Discrete by 2.8%, Embedded Processing by 5.7% and RF Optical Communication by 13.4% -- by end market on a sequential basis, Communication Equipment and Computer and Peripheral grew 14%, Industrial, 12% Personal Electronic, 12%, while Automotive was flat. Turning now to profitability. Gross profit in the third quarter was $1.40 billion, increasing 32.2% on a year-over-year basis. Gross margin was 37.3%, increasing 410 basis points year-over-year, mainly due to a lower unused capacity charges and better product mix. On a sequential basis, gross margin increased by 250 basis points. Q3 gross margin included about 60 basis points of unused capacity charges and about 40 basis points of negative impact resulting from nonrecurring cost related to our manufacturing reshaping program. 
Looking beyond these near-term effects, improving our gross margin remains a key priority. We remain committed to achieving the 44% to the 46% gross margin of our intermediate financial model once our manufacturing reshaping plan is completed. Starting from the approximately 39% gross margin expected for Q4 '26, we see a clear path to margin expansion. First, Q4 '26 temporary headwinds, including approximately 40 basis points from unused capacity charges and approximately 30 basis points from nonrecurring costs associated with our manufacturing reshaping program are expected to largely disappear during the second half of 2027. 
Second, we continue to expect more than 400 basis points of structural gross margin improvement from the reshaping of our manufacturing footprint. This benefit is expected to materialize as a step function either toward the end of 2027 or in early 2028, subject to the shutdown of legacy fabs and customers' qualification timing. Finally, we expect better mix and price to contribute to margin expansion over time, while input cost increase is expected to be a headwind. The timing and the magnitude of these effects remain more difficult to assess. Moving now to total net operating expenses. In the third quarter, this amounted to $979 million, excluding restructuring. Non-U.S. GAAP OpEx stood at $972 million, better than the indication we gave in July, reflecting continuing cost discipline. For the fourth quarter of 2026, we expect non-U.S. GAAP net OpEx to stand at about $1.035 billion. 
The sequential increase is mainly due to the calendar days effect net of vacation. This would lead the full year 2026 non-U.S. GAAP net OpEx slightly above $3.8 billion, in line with our expectation. In the third quarter, we reported operating income of $367 million, which includes $55 million for impairment, restructuring charges and other related phaseout costs. These charges are related to the execution of our company-wide program to reshape our manufacturing footprint and to resize our global cost base. Q3 operating income also included $7 million in purchase price allocation effects from our acquisition of NXP's MEMS sensor business. Excluding these items, Q3 non-U.S. GAAP operating income stood at $429 million and non-U.S. GAAP operating margin was 11.4%, with Analog Products, MEMS and Sensor at 14.1% Power & Discrete negative 17.1% Embedded Processing at 23.1% and RF Optical Communications at 26.2%. Third quarter 2026 net income was $291 million compared to $237 million in the year-ago quarter. 
Diluted earnings per share were $0.31 compared to $0.26. Non-U.S. GAAP net income stood at $344 million and non-U.S. GAAP diluted earnings per share stood at $0.37. Net cash from operating activities totaled $1.02 billion in the third quarter compared to the $549 million in the year-ago quarter. Net CapEx was $643 million in the third quarter compared to $401 million in the year-ago quarter. Free cash flow was positive at $351 million in the third quarter compared to the positive $130 million in Q3 2025. Inventory at the end of the quarter was $3.25 billion compared to $3.19 billion in Q2 2026 and $3.17 billion in Q3 2025. Days sales of inventory at quarter end were 126 days, better than our expectation, unchanged from the previous quarter and compared to the 135 days in the year-ago quarter. Cash dividends paid to stockholders in the third quarter of 2026 totaled $83 million. 
In addition, ST executed a share buyback of $91 million. ST maintained its financial strength with a net financial position that remains solid at $2.11 billion as of September 26, 2026, reflecting total liquidity of $5.31 billion and total financial debt of $3.21 billion. Following the exercise of the call option for the early redemption of ST's convertible debt due in 2027, bondholders exercised their conversion rights on the total $750 million convertible bonds. ST settled the bonds on a net share basis, delivering $750 million in cash and about 4.2 million share from treasury stock. Finally, while we are not providing a quarterly indication for 2027, for modeling purposes, please note that 2027 will have 86 calendar days in Q1, 91 in Q2, 91 in Q3 and 97 in Q4. Now back to Jean-Marc, who will comment on our outlook.

**Jean-Marc Chery** (Executives):
Thank you, Lorenzo. Now let's move to our business outlook for Q4 2026. We are expecting Q4 revenues of $4.15 billion, plus/minus 350 basis points at the midpoint. Our Q4 '26 net revenues will increase 10.5% sequentially and 24.7% year-over-year. We expect our gross margin to be at about 39%, plus/minus 200 basis points, including about 40 basis points of unused capacity charges. This business outlook does not include any impact of potential further changes to global trade tariffs compared to the current situation. For 2026, the midpoint of this outlook translates into full year 2026 revenues of about $14.5 billion, representing a 22.8% year-over-year increase. 
Beyond the cyclical recovery across our end markets, the year-over-year growth is supported by ST's company-specific growth drivers, including AI datacenters and low Earth orbit satellite communications. Gross margin is expected to be about 36.4%. Non-U.S. GAAP gross margin is expected to be about 36.6%, representing an improvement of 270 basis points versus the fiscal year 2025. To conclude, we continue to see a very strong demand for our AI datacenters and low Earth orbit satellite communications products and technologies, alongside an ongoing cyclical recovery in automotive and Industrial. With demand across many of the markets we serve exceeding available supply, we are expanding capacity in line with ST's strategic road map and growth opportunities. 
At the same time, improving profitability remains a key priority as we progress toward our intermediate financial model. As mentioned earlier by Lorenzo, this is supported by our company-specific growth drivers, combined with the execution of our company-wide program to reshape our manufacturing footprint and resize our global cost base. Before handing over to Jerome, I would like to mention a few corporate developments. Earlier this month, the Supervisory Board asked me to be reappointed in my current role for an additional year. I was honored and pleased to accept the proposal. My reappointment as Chairman of the Managing Board and ST's President and CEO will be proposed for shareholder approval at ST's 2027 Annual General Meeting of Shareholders. Finally, earlier today, we announced updates to ST's organization aimed at better aligning our vision and business objectives with evolving market dynamics. This will strengthen the coordination between our strategy, technology and product road maps, accelerate innovation and time to market, ultimately supporting our long-term growth opportunities. 
Remi El-Ouazzane is confirmed as President, member of the Executive Committee and Head of Microcontrollers, Digital ICs, RF and Optical Communication products. He will also take on leadership on the Imaging Sensor Group and be appointed as the Chief Technology Officer. Marco Cassis is confirmed as President, Member of the Executive Committee and Head of Analog, Power & Discrete and MEMS Product. He will also take on leadership of R&D for Analog, Power & Discrete and MEMS technologies and be appointed as the Chief Strategy Officer. The new organization and the related adjustment to our reportable segments will take effect on January 1, 2027 with implementation of the changes to be completed by the end of March 2027. Thank you, and we are now ready to answer your questions.

**Operator** (Operator):
[Operator Instructions] Our first question comes from Joshua Buchalter from TD Cowen.

**Joshua Buchalter** (Analysts):
On the results. I guess to start, I want to ask about some of the comments you made on gross margins. So I believe you said after the manufacturing transition headwinds abate, there'd be a step function increase of 400 basis points to gross margin. Is that sort of going to hit all at once? Because I think you previously said we shouldn't expect gross margins to get to 40% until sort of second half '27 or first half '28. So I guess is the expectation that it very quickly goes from 40% to 44%?

**Lorenzo Grandi** (Executives):
Maybe I take this question. Clearly, in terms of gross margin, we -- what we said is that the impact of our reshaping plan in manufacturing, it will factor in, in our gross margin once we will close our fabs. You know that there are 4 fabs, the legacy fabs that we intend, let's say, to close. And this, let's say, clearly, the impact, the positive impact will be visible when we will, let's say, be able to close. And this will happen in the second part of next year, let's say, so means that it will happen towards the end of 2027 and let's say, at the beginning of 2028. Clearly, here, it depends on the acceptance of the customer for 3 of these fabs substantially, let's say, we believe we have all in our hands, let's say, still some discussion for one of those. 
In this respect, I would say that in any case, we will continue to see improvement of our gross margin moving forward along the various quarter also due to the fact that we have a positive impact of the mix and improvement in terms of manufacturing variance. As I was saying, progressively, let's say, reducing our unloading charges and reducing also the temporary impact of negative cost due to the activity to transfer product from the legacy fab to the new fab 300-millimeter or in case of silicon carbide to the 200 millimeter.

**Joshua Buchalter** (Analysts):
Okay. My follow-up, any help you can give us with either like context or any sort of tighter range on the datacenter contribution for next year of well greater than $2 billion? And any help you can give us on how much you expect to be MCUs versus electronic ICs and PICs and power?

**Lorenzo Grandi** (Executives):
On the revenues, I assume.

**Jerome Ramel** (Executives):
Josh, your question was on revenues?

**Joshua Buchalter** (Analysts):
Yes. Revenue contribution from datacenter.

**Jean-Marc Chery** (Executives):
Okay. So I will give the overall picture and Remi will comment on the detail. Well, as I said during my speech, this year, we will generate about $1.3 billion revenue for datacenter, 85% coming from MDRF, so mainly microcontroller, silicon photonics and electronic ICs and BiCMOS. Next year, I will not give in detail, okay? We will be well above doubling this number. And we will communicate in January, of course, a number for '27 and an indication for '28. So maybe, okay, Remi, you can comment some more detail.

**Remi El-Ouazzane** (Executives):
Sure. Microcontrollers in datacenters will see a steep growth year-on-year. It will grow 2x in revenue size. I won't give you the exact number. The contribution of silicon photonics next year will start to grow and become very relevant. I would say that actually, it will be tens of percent of the complete revenue consideration. We will not share the exact details. As to BiCMOS, I think the bulk of the effect we will see is from '28 onwards because we've won a lot of sockets over the past quarter. And I think that you'll see the effects mainly in '28, even though it will be nonnegligible in '27, but I guess from a contribution standpoint, it will be very, very visible in '28.

**Jean-Marc Chery** (Executives):
Thank you, Remi. So about $1.3 billion this year, well above doubling next year, and we continue towards '28, and we will communicate more detail in January.

**Operator** (Operator):
The next question comes from Francois Bouvignies from UBS.

**Francois-Xavier Bouvignies** (Analysts):
I had just a question on the gross margin as well. I mean a bit more short term here about the Q1. I was looking at the history, and it's a bit all over the place, the gross margin direction in Q1. And it seems to be that in an up cycle, it's up quarter-on-quarter. In the down cycle, it's down quarter-on-quarter. The average is down 70 bps, but it's very diverse. So I was wondering if you could help us on the direction of the gross margin given all the moving parts right now for the Q1, please?

**Lorenzo Grandi** (Executives):
For Q1, we see gross margin -- clearly, we don't give indication of the gross margin of the following quarter. But what I can say is that we see gross margin at least at the current consensus for Q1. Let's say, more than that, I would not say more at this stage.

**Francois-Xavier Bouvignies** (Analysts):
Okay. And maybe one on the satellites. Could you maybe update on -- you mentioned datacenter, but what about LEO into next year? How is it shaping? I mean you kept your guidance for a long time. It's a broad guidance of above $3 billion. But I was wondering if you could give more color on this year and next year as you get more visibility, please?

**Jean-Marc Chery** (Executives):
I pass the question directly to Remi.

**Remi El-Ouazzane** (Executives):
We see a lot of momentum across the board, not only in SpaceX, but other programs that are going to be ramping. I would expect actually next year to be as good, if not better than this year in terms of revenue contribution. As a matter of fact, I do believe that we are right now working hard to go and find more capacity to enable even more revenue. So that's the momentum we're into kind of very consistent with what you're hearing from one of our customer's earnings calls in terms of the momentum they're getting.

**Francois-Xavier Bouvignies** (Analysts):
Sorry, you mean that revenue contribution as a percentage of revenues or just growing on absolute -- just to clarify this point.

**Remi El-Ouazzane** (Executives):
My comment was the latter. Revenue would be a lot larger than this year.

**Operator** (Operator):
The next question comes from Sebastien Sztabowicz from Kepler Cheuvreux.

**Sébastien Sztabowicz** (Analysts):
On a global basis, what kind of visibility you have for the coming quarters and where the backlog is standing at the end of Q3? And attached to that, on the revenue side, how do you see the seasonality building up for '27? Should we expect a better than usual seasonality?

**Jerome Ramel** (Executives):
Sebastien, your line was breaking up. Can you rephrase the question what is the seasonality for Q1, you were asking?

**Sébastien Sztabowicz** (Analysts):
No, seasonality for '27. Do you expect better than usual or normal seasonality moving into '27?

**Jean-Marc Chery** (Executives):
Okay, the seasonality will be different. Why? Because as I explained a few minutes ago, we are on the dynamic where we are basically rebalancing the spread of ST across the various vertical. As an example, okay, at the midpoint of the guidance we provide, the automotive vertical's weight of total revenue ST will be about 35%. And then, okay, industrial will be, let's say, between 22%, 24% CCP, so means the digital infrastructure, datacenter, low Earth orbit satellite and some legacy will be slightly above 20% and personal electronics 22%. For 2027, we expect to see CCP continuing to grow. So you see the balance between the verticals will be significantly different. So of course, it will impact the seasonality. So this is some indication we will give clearly in January. And the first...

**Sébastien Sztabowicz** (Analysts):
The first question was on the backlog level today. And what kind of visibility do you have for the coming quarters based on your backlog right now?

**Jean-Marc Chery** (Executives):
You see, okay, with a book-to-bill that was well above 2, okay, and revenue of $3.5 billion. Now our backlog is well above $20 billion. So it's representing compared Q4 midpoint of the guidance, now about 5 quarters of revenue, which start to be appropriate visibility to drive our operation. We are still far the peak of 2023 and 2022.

**Operator** (Operator):
The next question comes from Menon Janardan from Jefferies.

**Janardan Menon** (Analysts):
I'll just start with a sort of clarification and then I have a question after that, but both on gross margin. You had said that you don't expect Q1 gross margin to be at least in line with current consensus. I'm just looking at it both Visible Alpha and Bloomberg, it's about 38%. So are you suggesting that gross margin could decline slightly quarter-on-quarter, given that you are guiding at 39% in Q4? And then the question also is on gross margin. So your target model -- medium-term target model is 44% to 46%. If you take more than 400 basis points from the fab conversion, that means you're sort of saying before that comes through, it's about 41%-ish. So should we assume that between Q4 this year at 39% and, let's say, Q3 2027, your gross margin will essentially go up by, give or take, around 200 basis points? And then as you go beyond that, you will get the full effect of 400, 450 basis points. And when you gave that target model, you did not have so much of visibility on the AI side where you've said that your margin is above the target model on areas like silicon photonics. So given that, that is so strong, is there a chance that your gross margin in this cycle with the help of that as well as pricing could actually end up above that target model?

**Jerome Ramel** (Executives):
So basically, Janardan, you want to know the gross margin in Q1 and for 2027, right? I will let Lorenzo answer but [indiscernible] guide for the gross margin going forward. But Lorenzo, do you want to...

**Lorenzo Grandi** (Executives):
No. At the end, clearly, in the past, and as we said also before, clearly, one of our focus is to increase our profitability and increase the gross margin. One of the key element on the gross margin definitely will be our reshaping plan. As we said, our reshaping plan, let's say, will factor in, in our gross margin towards the end of next year and in 2028, let's say, substantially. And this is one of the important element. The other important element is that the growth that we are in AI and the growth in the AI infrastructure and the growth that we have, let's say, now in the industrial that is very significant, as you have seen, is accretive for our gross margin. And this we do expect continuing, let's say, progressively also in 2027, so bringing a positive impact on the gross margin. 
As I said about the gross margin of the Q1 quarter, at this stage, for me, I don't want to guide, but what I said is that we will be at least at the level of the current consensus. And what's to say more than that, clearly, let's say, there are other elements that we need to consider. And one of the elements that you have to keep in mind is that we are also in an inflationary, let's say, environment for which there is a cost increase in our input cost. This will, let's say, have some impact. But on the other side, there are other positive that are, as I said, the impact of the improvement in manufacturing efficiency, the mix that will enter and also some continued price increase on our top line.

**Janardan Menon** (Analysts):
Understood. Just on the first answer, so you suggested and I understand it that because of the strong AI growth, you could end up above the target model. Is that the way I should understand your answer?

**Lorenzo Grandi** (Executives):
The question is if we can end up above our target model, let's say. The point is that for the time being, we target to be at our target model, let's say. And of course, as I said, there are many components. One could be the mix. Let's say, we'll see. But we will, let's say, update you moving forward, let's say, in January and during the next year.

**Operator** (Operator):
The next question comes from Gianmarco Bonacina from Banca Akros.

**Gianmarco Bonacina** (Analysts):
Just a follow-up on your book-to-bill, if you can provide a little bit more color for the different verticals. And also, you talked about seasonality for the year. If you can give also some indication given that you indicated you have good visibility also in terms of the Q1, also with the comment you made on the calendar days, we know that normally Q1 is down about 10% sequentially. So if you can indicate directionally this time, given seasonality and visibility, maybe the performance will be different.

**Jean-Marc Chery** (Executives):
So about the book-to-bill that is significantly above 2 for ST overall. It's above 1 for each of our end markets, product group in region. And specifically, it is well, well above 2 for Communication Equipment and Computer Peripheral and Industrial. When I say well, well above 2, I have to say well above 3. About the seasonality, again, what we can say similarly, Lorenzo commented that we feel comfortable to deliver the gross margin at least at the consensus for Q1. We feel comfortable to deliver at least the revenue consensus for Q1 on the calendar we have indicated.

**Jerome Ramel** (Executives):
So despite having only 86 days in Q1.

**Operator** (Operator):
The next question comes from Didier Scemama from Bank of America.

**Didier Scemama** (Analysts):
Two questions. One, can you give us a sense of the early indications of your pricing negotiations with your Tier 1 customers, if that -- you want to share anything about that? And I've got a follow-up.

**Lorenzo Grandi** (Executives):
Let's say that -- what we can say is that in terms of pricing, we confirm that in this context that this higher input cost and the increasing lead time, we are increasing pricing on some selected product. This, of course, is an ongoing process. When we look, let's say, about pricing, assuming that this gap between supply and demand remains having -- and this is what we see today when we look at the evolution of our backlog and when we look at the billing, let's say, the fact that next year, we may have in terms of pricing stability or slightly increase, but this is not out of reach. We think that is something that we may see. Anyway, at this stage, it's a little bit early to comment more in general because as you can understand, the discussion for next year, let's say, have not yet been completed. So we are in discussions with our customers.

**Didier Scemama** (Analysts):
Yes. No, very clear. Sorry, I just want to understand better what you're trying to say for Q1 because you just said a number of things which are, in my understanding, contradictory to what you said before. So I just wanted to make clear. The number of calendar days in Q1 implies a decline of about 10.6% sequentially, and then you've got normal seasonality of down 10%. So let's say, call it minus 21. Consensus is like minus 5%, minus 6%. And you just said you think you'll be in line with consensus on revenues adjusted for the calendar number of days. So sorry, I'm not sure what to understand from all of that. If you could help me, that would be great. And related to this, the seasonality in Q1 normally is strongly influenced by your Personal Electronics business and by the price cuts that you give to your Tier 1s. So you've answered the second part. On the Personal Electronics side, it looks like your Q3 was a lot better than expected. Is there a risk of a pull-in? Or is it genuine end demand and therefore, no risk that Q1 is worse than seasonal, let's say?

**Jean-Marc Chery** (Executives):
No. I will try to be much more clear, okay. With the visibility we have with a quarter of 86 days, we are comfortable to deliver the consensus of Q1.

**Didier Scemama** (Analysts):
Very clear. And on the Personal Electronics, I mean, Q3 strength, was that a pull-in? Or do you think there was just end demand being better than expected? I mean you guided very cautiously for Q3 in fairness.

**Jean-Marc Chery** (Executives):
No, no, no. There is no specific pull-in. It is -- we just deliver, okay, the demand of the customer. And no, we don't see a specific pull-in.

**Operator** (Operator):
The next question comes from Jakob Bluestone from BNP Paribas.

**Jakob Bluestone** (Analysts):
I just had a question on your silicon photonics ramp. Just wondering if you can give a little bit of an update on how that is progressing in terms of yields? And maybe if you can also update us a little bit on your expansion of your production capacity there.

**Jean-Marc Chery** (Executives):
Thank you. I pass the question to Remi.

**Remi El-Ouazzane** (Executives):
Jakob, we -- it's going as per plan. The electro-optical yield our customers are getting at this stage are setting a new bar for the industry. Keep in mind that we are probably the only at-scale 12-inch SiPho player shipping right now. And I think it speaks volume for the value of 12-inch in critical dimension and yield entitlement. So I can say with high confidence that our customers are very, very, very happy with the yield that our technology platform is providing. Clearly, this year, the contribution is not marginal, but it's not at all to the tune of what it will be next year. There will be -- we expect a steep growth, which itself is backed up by the fact that we've communicated that we would increase capacity by 4x year-on-year. Actually, it will be a little bit more than 4x when you look specifically at the number. So I think silicon photonics in ST is going to be a long growth story for which we happen to have actually long-term visibility.

**Jerome Ramel** (Executives):
Do you have a follow-up, Jakob?

**Jakob Bluestone** (Analysts):
A quick one, maybe I don't know if you can comment at this point, but just in terms of the -- you obviously had lower OpEx this quarter, obviously flagging a little bit of a step-up for Q4. Just sort of if you can maybe just give us an update on the outlook for your OpEx beyond here? Do you think it could be sort of flattish next year? Or given some of the cost inflationary pressures you flagged, could it be up next year?

**Lorenzo Grandi** (Executives):
On the OpEx of next year, directionally, I would say that they will go up. At this stage, it's a little bit too early to comment. But keep in mind that during 2027, we will keep on continuing our cost savings programs, which should bring, let's say, something in the range of $100 million, $120 million benefit -- we should have also, especially in the second part of the year, some decline in our start-up cost. This means that are impacting our other income and expenses in a negative way. Conversely, on the other side, we are accelerating some of our investment in new business opportunities, as you can imagine. And then on the other side, there will be also, let's say, some impact related to the normal wage salary inflation and these kind of things. So there will be some increase next year, well below, let's say, with anyway an improvement in our expense-to-sales ratio.

**Operator** (Operator):
The next question comes from Stephane Houri from ODDO BHF.

**Stephane Houri** (Analysts):
First question is a clarification on what has been said about the satellite opportunity for next year? Because basically, you're saying you're not sure you will grow, but you're working hard to do so. Can you maybe elaborate and separate a little bit what is the end demand at the moment? And how many customers you have besides your main customer? And what is also linked to the capacity ramp issues?

**Remi El-Ouazzane** (Executives):
I'll repeat what I said, Stephane. I said that actually, I expect next year revenue to be same or better than this year revenue. That's the first thing I said. This year revenue was a record year for that business due to the fast growth of our major customers. Next year, that growth continues unabated and comes with additional customers piling on top. And we are actually working hard to release pocket of capacity to be able to capture the entire demand they have because I can say with confidence that at this stage, when we look at front-end module technology, and by BiCMOS technology, there is nothing coming close to it. 
And keep in mind that actually the technology matter in that case because the noise figures that you can actually get out of the technology will translate into the efficiency of the spectrum, which itself translate into the efficiency of the deployment. So we truly have a first row seat position in those accounts. And right now, I will state that next year, we are most likely going to be capacity gated not demand-gated. And we are working to go and as usual, to find ways to go and release more and more capacity over time. That's the summary of what I said.

**Stephane Houri** (Analysts):
Okay. And the second question, the follow-up is about automotive. We didn't speak a lot about automotive today. And there is a sense that the book-to-bill seems to be above 1, so improving. At the same time, the situation among the automotive customers doesn't seem to improve. So what is your view on what's going to happen in 2027? And if you can maybe elaborate a bit about the electromobility opportunity and the software-defined vehicle opportunity at the same time?

**Jean-Marc Chery** (Executives):
Automotive, first of all, the visibility we have from our European Tier 1 is really stable since more than 6 months now, which is really positive compared to the previous year. In '26, we expect to grow for the full year '26 automotive, that is slightly above 10% for us that is basically consistent with the market. It is pretty well spread with our main product group except, of course, radio frequency and optical cable. We are not yet putting optical cable in cars. But between AM&S and Power Discrete and let's say, the digital processing solution, the growth will be pretty similar. But then yes, we are seeing an acceleration of our Power Discrete in Q4 [indiscernible] will be well above 20% -- 25%. 
So this is driven by the European market of electromobility. So we expect next year the automotive to contribute to the growth of the company. Most likely [indiscernible] I repeat, next year the growth driver of the company will remain the AI datacenter will remain the infrastructure industrial will remain the B2B industrial business for factory automation robotics, this kind of stuff. Our consumer overall, we believe will remain soft or weak. But good confidence level to continue to grow in automotive, driven by European electromobility and also, the many socket wins we have in internal combustion engine cars and hybrid.

**Stephane Houri** (Analysts):
Okay. And just one follow-up, a view on silicon carbide for 2027.

**Jean-Marc Chery** (Executives):
Silicon carbide, first of all, this year, okay, we will grow about 20% which is a positive news. So clearly, the main growth driver is European, let's say, electrical car, and this will continue next year. Importantly, for us on silicon carbide, and also part of our, let's say, turnaround of the profitability of this group is the diversification we have engaged first of all, for the power supply of datacenter, but also for power application requesting high power conversion in the industrial market. So next year will be another year of growth, of significant growth for our silicon carbide. And okay, we expect to have the benefits of the wafer size conversion to 8-inch, both from Catania and Chongqing.

**Jerome Ramel** (Executives):
We have time for one more question.

**Operator** (Operator):
The last question comes from Sandeep Deshpande from JPMorgan.

**Sandeep Deshpande** (Analysts):
Just quickly coming back to the gross margin question. You've got this 400 bps of gross margin improvement once the reshaping program is over. How much of that is coming from -- today, you're running both the 200- and 300-millimeter fabs. And so what percentage of your gross margin uplift is from that versus how much of it, could you remind us is coming from -- because you're going to have lower cost on the wafer, et cetera, per chip associated with the shift to 300 millimeters? And my second question is that despite your revenue growth, which was quite considerable in both the Analog, MEMS and Sensors business and in your Power & Discrete business, your margin actually declined year-on-year in both those business units. Why was that?

**Lorenzo Grandi** (Executives):
Okay. In terms of, let's say, clearly improvement of above 400 basis points is a combination of different elements. Clearly, the size of the wafer, the fact that we move from fabs that are poorly automatized so with a significant cost of labor on, let's say, fabs that are much more automatized. Now to split, let's say, the various contributor is a little bit complex to be done. When we look, let's say, the profitability of AMS, let's say, overall going down on a year-over-year basis clearly here is the group where is mainly major impact where there is the major impact of the legacy fab that we are now, let's say, on which we are now transferring the products. 
Clearly, here, there is an impact related to the fact that in this moment, there are some extra cost, as I was explaining overall for the company, but there is also, let's say, an impact on the efficiency of this fab on which we are transferring the cost. So here, when we look at this segment, clearly here is now suffering about this transition phase. It's also true that will be one of the groups that will, let's say, enjoy more when we will finally move to the new fab, to the most advanced fab here, especially for the 300-millimeter. And at the same time, the Power & Discrete, where Power & Discrete will enjoy the move from the 150 to the 200 millimeter.

**Sandeep Deshpande** (Analysts):
Just a quick question on this. When you talk about the guidance of 39% gross margin in the fourth quarter, you've highlighted how much of that is -- how much underloading is involved. But how much of this 39% gross margin has impact from this negative impact from this double counting of costs, et cetera?

**Lorenzo Grandi** (Executives):
So for what concern, let's say, the underloading, yes, it's 40 basis points. The extra cost, let's say, related to the new mask, transfer of the process, trials and so on, we estimate in the range of 30 basis points. It's more difficult to say, let's say, the overall inefficiency created by this activity in the fab. It's something that we don't quote because it's a little bit more difficult to really say what is this impact. But this is an impact that, of course, will disappear when we will move, let's say, to the new fab. Anyway, it's 40 basis points, let's say, the unused and 30 basis points, the extra cost. This is what we report usually each quarter.

**Jerome Ramel** (Executives):
Thank you, Sandeep, and thank you, everyone. I think that concludes our call. So thank you, everyone, for joining us, and feel free to reach out if you have further questions, the IR team.

**Operator** (Operator):
Ladies and gentlemen, the conference is now over. Thank you for choosing Chorus Call, and thank you for participating in the conference. You may now disconnect your lines. Goodbye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### STM_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Jean-Marc Chery｜guidance：CEO 給 Q3 毛利率指引約 37%（原話："We expect our gross margin to be about 37%"）
- 2026-07-23｜Jean-Marc Chery｜guidance：CEO 預期 Q4 營收高於 40 億美元（原話："We expect Q4 revenues to be above $4 billion"）
- 2026-07-23｜Jean-Marc Chery｜guidance：資料中心 2026 營收預期上調至逾 10 億美元（原話："We now expect revenues above $1 billion in 2026"）
- 2026-07-23｜Jean-Marc Chery｜guidance：資料中心 2027 營收預期遠高於 20 億美元（原話："well above $2 billion in 2027"）
- 2026-07-23｜Lorenzo Grandi｜guidance：Q3 non-GAAP 營業費用預期約 9.8 億美元（原話："net OpEx to stand at about $980 million"）
- 2026-07-23｜Lorenzo Grandi｜guidance：2026 淨資本支出預期落在 20–22 億區間高端（原話："2026 net CapEx to be at the high end"）
- 2026-07-23｜Jean-Marc Chery｜guidance：Q3 展望不含進一步關稅變動（原話："does not include any impact for potential further"）
- 2026-07-23｜Jean-Marc Chery｜guidance：個人電子 Q3 成長低於正常季節性（原話："below normal seasonality in Q3"）
- 2026-07-23｜Jean-Marc Chery｜guidance：通訊設備與電腦周邊 Q4 年增約 90%（原話："we will be about 90% growth"）
- 2026-07-23｜Marco Cassis｜guidance：SiC 2026 營收預期雙位數成長（原話："we should grow the silicon carbide revenues double digit"）
- 2026-07-23｜Remi El-Ouazzane｜guidance：太空/LEO 2026–2028 累計營收預期逾 30 億美元（原話："we stick to well above $3 billion over '26, '27, '28"）
- 2026-07-23｜Lorenzo Grandi｜margin：Q2 毛利率含製造重整一次性成本負面影響約 60bp（原話："about 60 basis points of negative impact"）
- 2026-07-23｜Lorenzo Grandi｜margin：Q4 毛利率較 Q3 的 37% 環比改善，但有暫時性逆風（原話："I confirm that in Q4, there will be an"）
- 2026-07-23｜Lorenzo Grandi｜margin：Q4 匯率效果中性，不再如 Q3 有助益（原話："It will be neutral"）
- 2026-07-23｜Lorenzo Grandi｜margin：資料中心產品組合對毛利率正貢獻（原話："product mix is contributing in a positive way"）
- 2026-07-23｜Lorenzo Grandi｜margin：毛利率 40% 以上模型需等製造重整完成，預計 2027 年底（原話："we confirm our model to be, let's say, above 40%"）
- 2026-07-23｜Lorenzo Grandi｜margin：Power & Discrete 部門 Q2 non-GAAP 營業利益率為負 21.4%（原話："Power & Discrete at minus 21.4%"）
- 2026-07-23｜Lorenzo Grandi｜margin：漲價與投入成本上漲目前大致互抵（原話："the 2 impacts are more or less offsetting each other"）
- 2026-07-23｜Jean-Marc Chery｜commitment：確認 2028 年營收 180 億美元目標（原話："confidence level to reach $18 billion in 2028"）
- 2026-07-23｜Jean-Marc Chery｜commitment：200 億美元目標暫不討論，先達成 180 億（原話："let's reach together the $18 billion"）
- 2026-07-23｜Lorenzo Grandi｜commitment：製造重整計畫預計 2027 年底完成（原話："it will be at the end of 2027, not before"）
- 2026-07-23｜Jean-Marc Chery｜commitment：2026 資料中心訂單 100% 已覆蓋（原話："Backlog for this year, 100% coverage."）
- 2026-07-23｜Jean-Marc Chery｜risk：部分產品供給吃緊、交期拉長（原話："some tension on the supply"）
- 2026-07-23｜Jean-Marc Chery｜risk：傳統類比產線 Q2 爬坡延遲影響 Q3 供貨（原話："pure legacy analog technologies"）
- 2026-07-23｜Remi El-Ouazzane｜risk：其他星座業者近期遇到問題（原話："Other constellation have faced a bit of a snag"）
- 2026-07-23｜Lorenzo Grandi｜risk：閒置產能費用 Q4 不會明顯下降（原話："will not change significantly in Q4"）
- 2026-07-23｜Jean-Marc Chery｜customer：Q2 book-to-bill 接近 2（原話："book-to-bill close to 2 overall"）
- 2026-07-23｜Jean-Marc Chery｜customer：Q2 訂單超過半數為明年（原話："well above 50% were for next year"）
- 2026-07-23｜Jean-Marc Chery｜customer：在手訂單約相當 4.5–5 個季度營收（原話："4.5 to 5 quarters of Q2 average revenue"）
- 2026-07-23｜Remi El-Ouazzane｜customer：資料中心營收分布與超大規模業者市占相近（原話："quite confident about the composition of our revenue"）
- 2026-07-23｜Jean-Marc Chery｜customer：Q1 2027 訂單負載良好（原話："Q1 is today on the dynamic to be well loaded"）
- 2026-07-23｜Remi El-Ouazzane｜product：矽光子不受產能擴充限制（原話："we are not right now gated by capacity expansion"）
- 2026-07-23｜Jean-Marc Chery｜product：Crolles 產能將達每週 15,000 片（原話："Crolles will reach 15,000 wafer per week"）
- 2026-07-23｜Lorenzo Grandi｜competition：對選定產品漲價（原話："we're increasing the prices on selected"）
- 2026-07-23｜Lorenzo Grandi｜capital_allocation：發行 15 億美元可轉債（原話："ST issued a new $1.5 billion dual tranche"）
- 2026-07-23｜Jean-Marc Chery｜product：中國製造夥伴 14nm 製程已認證，中國供中國策略（原話："China for China strategy that will start to pay back"）
- 2026-07-23｜Jean-Marc Chery｜customer：通訊設備與電腦周邊 Q3 年增近 60%（原話："this segment will grow very similarly"）

### STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md
- 2026-03-09｜Remi El-Ouazzane｜guidance：管理層上調資料中心營收預期：2026 年明顯高於 5 億美元、2027 年遠高於 10 億美元（含光互連與 AI 伺服器電源/類比）（原話："nicely above $500 million of revenue in 2026"）
- 2026-03-09｜Remi El-Ouazzane｜guidance：管理層預期 800V 架構於 2027 年開始放量，效益延伸至 2027 年之後（原話："volt architecture to start to ramp in '27"）
- 2026-03-09｜Remi El-Ouazzane｜guidance：管理層表示 NPO 將自 2027 下半年起在 AI 叢集出現（原話："you will start to see NPO from second half '27"）
- 2026-03-09｜Remi El-Ouazzane｜guidance：管理層個人看法：scale-up 機架於 2030 年達 100% 光學化（原話："100% coverage in 2030 is my opinion."）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層以每 GW 資料中心基礎設施約 2.3 億美元的 SAM 作為市場口徑（而非總市場金額）（原話："We see around $230 million."）
- 2026-03-09｜Remi El-Ouazzane｜margin：該 SAM 由約 400 款產品支撐（原話："backed up by about 400 products"）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層說明 2.3 億美元 SAM 僅以可插拔光學為基礎，NPO 成長尚未計入（原話："it's only based on pluggable optics."）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層說明 NPO 成長不在 2.3 億美元內，將疊加其上（原話："We have not included the growth of NPO."）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層明言不拆分 5 億/10 億美元的光子與電源組成（原話："but we have decided actually not to break it down"）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層解釋刻意不給總 SAM 金額，因 GW 部署量持續變動（原話："it's on purpose we've not done it."）
- 2026-03-09｜Remi El-Ouazzane｜commitment：矽光子產能擴張超過四倍（2027 年對比現況）（原話："more than quadruple our output by '27"）
- 2026-03-09｜Remi El-Ouazzane｜commitment：產能擴張由客戶長期產能預留承諾支撐（原話："fully backed by long-term capacity reservation commitments"）
- 2026-03-09｜Remi El-Ouazzane｜commitment：與 AWS 的多年期、數十億美元商業合作（原話："multibillion dollar commercial engagement"）
- 2026-03-09｜Remi El-Ouazzane｜commitment：管理層稱到今年產品供應可涵蓋整個 2.3 億美元 SAM（原話："By this year, we can cover the entire $230 million"）
- 2026-03-09｜Remi El-Ouazzane｜capital_allocation：資本支出維持 20～22 億美元區間但重新配置以加速矽光子（原話："billion to $2.2 billion envelope, but remixing it"）
- 2026-03-09｜Remi El-Ouazzane｜capital_allocation：管理層不提供絕對 CapEx 金額（原話："CapEx number dollar to share with you."）
- 2026-03-09｜Remi El-Ouazzane｜capital_allocation：目前新增矽光子產能 100% 在前段製程（原話："Today, these announcement is 100% front-end."）
- 2026-03-09｜Remi El-Ouazzane｜product：PIC100 於 300mm 進入量產，供應主要超大規模客戶（原話："PIC100 in 300 millimeter for leading hyperscalers."）
- 2026-03-09｜Remi El-Ouazzane｜product：800V DC 架構尚未進入量產（原話："it's not involved in volume production yet."）
- 2026-03-09｜Remi El-Ouazzane｜product：局部轉換 50V 轉 12V 已與主要客戶量產（原話："in production with key customers on the 50-volt to 12-volt"）
- 2026-03-09｜Remi El-Ouazzane｜product：管理層認為 NPO 將是未來五年主流（原話："NPO will be the winner for the 5 years to come."）
- 2026-03-09｜Remi El-Ouazzane｜product：Crolles 以閘道分批加產能，客戶無需重新認證（原話："copy exact of the previous gateway."）
- 2026-03-09｜Remi El-Ouazzane｜competition：管理層承認 ST 在 54V 架構的電源市場過去僅是邊緣角色（原話："we have been actually marginal as the players."）
- 2026-03-09｜Remi El-Ouazzane｜competition：管理層稱 EIC 已是市場領導者；PIC 目標為市場領導（以 30% 起算）（原話："We are the market leader today."）
- 2026-03-09｜Remi El-Ouazzane｜competition：PIC 方面管理層表示想成為市場領導者（原話："we want to become the market leader."）
- 2026-03-09｜Remi El-Ouazzane｜competition：客戶通常採最佳組合方式採購 MCU/EIC/PIC，非必須同一供應商（原話："is more a best-of-breed approach."）
- 2026-03-09｜Remi El-Ouazzane｜risk：管理層預期未來 2～3 年相關技術供應吃緊（原話："there will be a lot of supply challenges in the industry."）
- 2026-03-09｜Remi El-Ouazzane｜risk：管理層稱銅與光學之爭是時間問題而非是否發生（原話："So I think it's a question of when, not a question of if."）
- 2026-03-09｜Remi El-Ouazzane｜risk：管理層說明 1.6T 轉換加速，光子將成為明日瓶頸（原話："the transition to 1.6T is completely accelerating"）
- 2026-03-09｜Remi El-Ouazzane｜customer：長期產能預留客戶分散，涵蓋晶片、模組與超大規模業者（原話："It's actually more diversified thing, Amelia."）

### STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260504.md
- 2026-05-04｜Remi El-Ouazzane｜guidance：管理層回應提問時重申 2026–2028 太空業務（LEO 加傳統太空）累計營收目標遠高於 30 億美元（原話："cumulative revenues of well above $3 billion for space as a"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：管理層表示 2026 年太空營收可能已接近 10 億美元（原話："we may already be close to $1 billion"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：ST 對 LEO 寬頻電子 SAM 的估計：2028 年約 20 億美元（原話："growing to roughly $2 billion in 2028"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：管理層說明上述數字不含太空資料中心的潛在上行（原話："do not include any potential upside coming from data"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：2026 年之後成長取決於星座部署節奏，火箭運載被列為首要關鍵路徑（原話："rocket launcher is at the top of the list"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：ST 估計新增訂戶 2030 年前可超過 2 億，目前約 1,000 萬（原話："could exceed 200 million by 2030 from about 10 million"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：LEO 業務 2025 年營收約 6 億美元（2021 年約 1.75 億）（原話："reaching approximately $600 million in '25"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：ST 的 LEO RF 市占估計約 90%（2025）（原話："estimate our RF market share for LEO at about 90% in '25"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：每顆 Starlink 衛星的 ST 料件價值自 V1.5 到 V3 增為 8 倍，達數萬美元（原話："material was multiplied by 8x between the V1.5"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：每個用戶終端的 ST 內容約數十美元（原話："reached down to only several tens of USD per user terminal"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：用戶終端為最大營收貢獻者，管理層拒絕給細項（原話："we are not going to give any breakdown"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：軍用應用不含在約 10 億美元內，且金額微不足道（原話："its completely marginal"）
- 2026-05-04｜Remi El-Ouazzane｜commitment：管理層承諾將 ST 維持為新太空領域的領先半導體供應商（原話："we are and we intend to"）
- 2026-05-04｜Remi El-Ouazzane｜commitment：與 SpaceX 合作持續，聚焦量產中設計與下一代衛星與終端共同架構（原話："the collaboration continues with a focus on ramping up"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層稱預測已納入主要客戶的市占流失（原話："some market share loss for our main customer"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層不認為超過 90% 的市占可以維持（原話："is exceeding 90% is something that we can keep as is"）
- 2026-05-04｜Remi El-Ouazzane｜competition：預期到 2030 年市占仍偏高，但低於 90%（原話："pretty oversized market share, clearly, lower"）
- 2026-05-04｜Remi El-Ouazzane｜competition：市場以 35% CAGR 成長，新供應商會來搶份額，已計入預測（原話："try to gain share, which we have factored in our numbers"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層承認 BiCMOS 前端模組市場會有競爭，但自認技術差異化強（原話："will have competition. But we feel quite strong as well"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層描述潛在競爭者輪廓：IDM、做 BiCMOS、具大規模封裝並掌握 PLP（原話："has huge assembly capabilities and is able to master PLP"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層解釋為何競爭者需為 IDM：後段封裝與前段同等重要（原話："the back-end, end up being as important as front-end"）
- 2026-05-04｜Remi El-Ouazzane｜product：每顆衛星的矽含量預期持續增加（原話："I do believe that silicon content will continue to increase"）
- 2026-05-04｜Remi El-Ouazzane｜product：Ku 頻段用戶終端的含量預期接近高原（原話："we're going to soon reach a plateau"）
- 2026-05-04｜Remi El-Ouazzane｜product：用戶終端經濟面為軟著陸，Ka 頻段被視為助力（原話："we are going to a soft landing in terms of the economics"）
- 2026-05-04｜Remi El-Ouazzane｜product：用戶終端產品世代週期約一年多一個月（原話："are for user terminal a year and roughly a month"）
- 2026-05-04｜Remi El-Ouazzane｜customer：ST 已在另一家主要業者通過驗證（原話："we have already been qualified at another"）
- 2026-05-04｜Remi El-Ouazzane｜customer：未來五年客戶數預期不超過 10 家（原話："I don't see more than 10 players"）
- 2026-05-04｜Remi El-Ouazzane｜customer：中國方面：因出口管制無法參與衛星端，只聚焦用戶終端（原話："we cannot be in any satellite technology happening in China"）
- 2026-05-04｜Remi El-Ouazzane｜customer：中國用戶終端目前未揭露具體進展（原話："we have not yet disclosed anything specifically happening"）

### 問答異常語氣（迴避／改口／保留）
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Menon 追問 Q4 毛利率方向與 2027 走勢｜答法：只確認 Q4 環比改善並列舉逆風，未給幅度，也未回答 2027
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Menon 追問營收跳升是否代表毛利率跳升也更大｜答法：重申會改善但強調閒置費用與匯率逆風，未給量化
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Ghilotti 詢問 40 億營收是否仍對應 40% 毛利率｜答法：改口補上第二條件（製造重整完成、2027 年底），Q4 達 40 億不足以到 40%
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Didier 詢問 45%/180 億與 50%/200 億模型是否仍成立｜答法：確認 180 億，200 億明確擱置，毛利率目標附加條件（重整準時、匯率）
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Buchalter 詢問 2027 資料中心是否因產能受限而高於 20 億｜答法：未直接回答是否高於 20 億，轉談成長驅動與矽光子產能無瓶頸
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Bluestone 詢問漲價順風與何時影響營收｜答法：只說投入成本與漲價大致互抵，未給時間與金額
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Joshua Buchalter (TD Cowen)：請拆分 5 億/10 億美元中矽光子與電源及各電壓級的組成｜答法：回答「Not really」，僅描述各產品量產狀態，明言不拆分
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Sandeep Deshpande (JPMorgan)：2.3 億美元 SAM 中 ST 目前已佔多少份額｜答法：先答「We have not documented that」，被追問後改談產品供應涵蓋度而非份額
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Adithya Metuku (HSBC)：EIC 市佔率具體多少｜答法：不給數字，回「I still have the same definition, I just gave you」
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Gianmarco Bonacina (Banca Akros)：2027 與 2030 的總 SAM 金額（十億美元）｜答法：明言刻意不給，請分析師自行依 GW 部署建模
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Stephane Houri (ODDO BHF)：成長所需 CapEx 增量及各市場規模與份額（對照 Infineon）｜答法：不給絕對 CapEx 金額與分市場規模/份額，僅重申 20～22 億美元區間重新配置
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Adithya Metuku (HSBC)：納入 scale-up 後 SAM 是否為 4.6 億美元｜答法：表示無法回答，因未給 2.3 億美元的拆分，僅說 NPO 將疊加其上
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260504.md｜問：Buchalter 追問市占下滑中有多少來自 SpaceX 自身占比下降、多少來自雙供應商｜答法：明說不直接回答，改談總 SAM 以 SpaceX 為大宗、ST 數字取決於在 SpaceX 的市占
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260504.md｜問：Scemama 要求 2025 與 2028 用戶終端／閘道／衛星的營收拆分｜答法：拒絕給精確數字，只給排序（終端最大、衛星次之、閘道最小）
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260504.md｜問：Houri 與 Bonacina 追問 2026–2028 營收軌跡及 2028／2030 市占水準｜答法：只重述「遠高於 30 億」與市占「低於 90% 但仍偏高」，未給逐年數字或市占百分比

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
{"date":"20260724","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"車用/工業補庫存升循環為結構性、非脈衝，STM 營收與利用率持續爬升","columns":{"2Y 驗證點":"2026-27 book-to-bill 守 >1、GM 序列改善","5Y 驗證點":"2028 營收向 $18B 模型靠攏","具體數字門檻":"Q3 GM ~37%→2027 持續升；2026 全年營收 ~$14.3B（共識）","來源":"Q2 法說 guidance、Bernstein 升循環判定","漂移觸發":"連 2 季 TTM 營收偏離 ≥5% 或 book-to-bill"}},{"id":"H2","text":"毛利率恢復到「40% @ $4B／45% @ $18B」模型（依賴製造重整 2027 末完成）","columns":{"2Y 驗證點":"Q4 2026 GM 淨向 40% 軌道","5Y 驗證點":"2028 GM ~45%","具體數字門檻":"Q3 37%±200bps → Q4 序列改善 → 2027 末重整完成","來源":"Q2 法說 Grandi/Chery 明確「須完成重整、2027 末、不早於」","漂移觸發":"連 4 季 TTM GM 偏離模型 ≥5% → 削弱（此為多頭核心賭注）"}},{"id":"H3","text":"估值修復＝谷底 EPS 恢復（FY26 $1.32→FY27 $2.68→FY28 $3.85）兌現、倍數不再進一步壓縮","columns":{"2Y 驗證點":"共識 EPS 不再下修、股價守住循環中段倍數","5Y 驗證點":"2028 EPS ~$3.85 × ~18x = ~$69","具體數字門檻":"FY27 Fwd PE 20x（$2.68）、FY28 13.9x（$3.85）","來源":"Excel snapshot 2026-07-16 normalized consensus（USD）","漂移觸發":"共識 FY27/28 EPS 連 2 季下修 ≥10% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"毛利率恢復停滯：製造重整延後 / 新產能折舊超前量能 / 傳統類比 legacy 產能爬坡卡關（法說已承認 Q2 legacy 類比 ramp 延遲）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 GM vs 40% 模型軌道；unused capacity charges 走勢","警戒閾值":"連 4 季 GM 停在 37% 以下且無序列改善"}},{"id":"R2","text":"需求空窗：補庫存脈衝退潮後現需求不接棒（S&P 車銷 −2%、PE 記憶體漲價擠壓低階手機）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"book-to-bill、分銷 POS、DSI 是否止跌回升","警戒閾值":"book-to-bill"}},{"id":"R3","text":"車用 MCU 份額結構性讓 Infineon AURIX：SDV 高內容段被生態綁定通吃","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"SDV MCU design-win、AURIX vs STM32 車規內容比","警戒閾值":"連續財季車用 MCU 內容/份額流失，≥50% 機率結構化"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"事件錨：Q4 GM 淨向 40% 模型軌道確認＋製造重整如期＋分銷去化未反轉；或估值回踩至 EV/EBITDA 正常化（約 $42-45）","irr_base_pct":7.0,"ev5y_pct":36.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.6,"ev5y_pct":36.0,"irr_base_pct":7.0,"max_dd_pct":-55.0,"bull_5y_price":110.0,"bear_5y_price":31.0,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":"事件錨：Q4 GM 淨向 40% 模型軌道確認＋製造重整如期＋分銷去化未反轉；或估值回踩至 EV/EBITDA 正常化（約 $42-45）","price_at_dd":53.49,"archetype":"循環/商品","cycle_position":"早循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
