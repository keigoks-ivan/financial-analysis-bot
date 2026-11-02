你是 stock-analyst **v20 判斷 agent**，標的 TT（20261102）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TT","date":"2026-11-02","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TT_20261102/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TT_20261102/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP，持續營運）","value":6759.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m（YoY +18%，有機 +16%；去年同期 5742.5）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"查無（新聞稿未載共識，未自行填造）"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP（調整後）營業利益","value":1363.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m；利益率 20.2%（去年同期 20.6%，-40bps）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"查無（新聞稿未載共識，未自行填造）"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益","value":1343.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m；利益率 19.9%（去年同期 20.3%，-40bps；YoY +15%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"查無（新聞稿未載共識，未自行填造）"},{"id":"f_kpi4_eps","label":"調整後持續營運 EPS","value":4.86,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD（YoY +25%；GAAP 4.79，去年同期 3.88／3.82）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"查無單季共識；FY 對照見 consensus_revision（FY1 15.28，財報前快照）"},{"id":"f_kpi5_bookings","label":"訂單 Bookings","value":7248,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m（YoY +21%，有機 +20%；去年同期 5979）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"查無（新聞稿未載共識，未自行填造）"},{"id":"f_kpi6_book_to_bill","label":"Book-to-bill","value":107,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"查無（新聞稿未載共識，未自行填造）"},{"id":"f_kpi7_backlog","label":"Backlog 在手訂單","value":12.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD bn（YoY +73%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"查無（新聞稿未載共識，未自行填造）"},{"id":"f_kpi8_2026","label":"管理層全年 2026 指引","value":"reported_rev_growth 約 13.5%（上調）；organic_rev_growth 約 11%（上調）；adj_EPS 15.20–15.30（維持）；GAAP_EPS 15.00–15.10","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"FY2026","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"FY1 共識 EPS 15.28（consensus_revision，落在指引區間內）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-29","period":"2026-10-29","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tt_gross_margin_pct","label":"TT 毛利率","value":34.99,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_operating_margin_pct","label":"TT 營業利益率","value":17.92,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tt_fcf_margin_pct","label":"TT FCF 利潤率","value":16.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_carr_gross_margin_pct","label":"CARR 毛利率","value":24.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_carr_operating_margin_pct","label":"CARR 營業利益率","value":8.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_carr_fcf_margin_pct","label":"CARR FCF 利潤率","value":10.43,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_jci_gross_margin_pct","label":"JCI 毛利率","value":36.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_operating_margin_pct","label":"JCI 營業利益率","value":14.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jci_fcf_margin_pct","label":"JCI FCF 利潤率","value":6.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lii_gross_margin_pct","label":"LII 毛利率","value":33.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lii_operating_margin_pct","label":"LII 營業利益率","value":19.94,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lii_fcf_margin_pct","label":"LII FCF 利潤率","value":15.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf_9_q3","label":"自由現金流（FCF，年初至今 9 個月；Q3 單季新聞稿未載）","value":2827.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","unit":"USD m（YTD，去年同期 1786.0，約 +60%；營業現金流 YTD 3060.1，淨資本支出 264.2）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-29）","citation":"公司 Q3 2026 新聞稿（8-K Exhibit 99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm；investors.tranetechnologies.com 未查得同稿副本"},"note":"查無（新聞稿未載共識，未自行填造）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":410.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-15.33,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":31.37,"period":"2026-10-30（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.07,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.29 → 15.28）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.7 → 17.7）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.05,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（20.32 → 20.33）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":15.28,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":17.7,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":20.33,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.48,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 14.91 → 15.28（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":28.49,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝53.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":53.0,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.86,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝74.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":74.2,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.99,"period":"2026-10-30（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝71.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-30（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":71.4,"period":"2026-10-30（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-30（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":26.83,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 15.28，分子＝快照價 410.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.768,"period":"2026-11-02","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-02"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":2990.2,"period":"2026-11-02","unit":"USD m","basis":"yfinance 最新一季：總債務 4217.6、現金 1227.4（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":218.9,"period":"2026-11-02","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":92737.29,"period":"2026-11-02","unit":"USD m","basis":"市值 89747.09 ＋ 淨負債 2990.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":24139.46,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":26525.58,"period":"2026-11-02","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.84,"period":"2026-11-02","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-02"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-11-02","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 410.0 / W52 441.74 / W104 418.19 / W250 298.0 / W250 13週斜率 1.45%"},{"id":"f_ma_w52","label":"52 週均線","value":441.74,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":418.19,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":298.0,"period":"2026-11-02","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.45,"period":"2026-11-02","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-02","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子載明產業已有整併與新進入者（含非傳統競爭者），可能加劇競爭與價格壓力，並有來自非傳統製造商的顛覆性技術風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"There has been consolidation and new entrants (including non-traditional competitors) within our industries and there may be future consolidation and new entrants, either of which could result in increased competition and pricing pressures and significantly alter the dynamics of the competitive landscape in which we operate.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 稱公司監控主要競爭對手與客戶以評估相對表現；未揭露量化份額數字。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"We monitor key competitors and customers in order to gauge relative performance and the outlook for the future.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"次要來源稱 Vertiv 純資料中心冷卻聚焦造成價格壓力，浸沒式冷卻可能使設備商品化；Trane 以收購 Stellar Energy Americas、LiquidStack 回應。","source":"Finimize / Memoori 等次要來源","url":"https://memoori.com/trane-buys-liquidstack-2nd-data-center-deal-3-months/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"10-K 揭露無單一客戶占合併營收逾 10%，業務不依賴單一客戶或少數客戶（FY2023 10-K；搜尋摘要稱 FY2025 10-K 同）。搜尋未找到任何客戶導入第二供應商或自製的報導。","source":"Trane Technologies plc Form 10-K FY2023","url":"https://www.sec.gov/Archives/edgar/data/1466258/000146625824000047/tt-20231231.htm","excerpt":"We have no customer that accounted for more than 10% of our consolidated net revenues in 2023, 2022 or 2021.","as_of":"2024-02-01","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K FY2025 揭露無單一外部客戶占合併營收超過10%（2023–2025），亦無重大依賴單一或少數客戶。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"We have no single external customer that accounted for more than 10% of our consolidated net revenues in 2025, 2024 or 2023. No material part of our business is dependent upon a single customer or a small group of customers; therefore, the loss of any one customer would not have a material adverse effect on our results of operations or cash flows.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TT Q2 2026 enterprise organic bookings +37%，backlog 創高 $12.1B，其中約 $6B 排在 2027 年及以後；管理層稱商用 HVAC 成長廣泛，資料中心非唯一驅動","source":"MarketBeat: Trane Technologies Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/trane-technologies-q2-earnings-call-highlights-2026-07-31/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261102","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TIKR 分析稱 TT backlog 創高、資料中心冷卻為結構性順風（分析師意見，非公司指引）","source":"TIKR: Trane Technologies has a 12 billion backlog","url":"https://www.tikr.com/blog/trane-technologies-has-a-12-billion-backlog-the-ai-cooling-boom-is-just-getting-started","excerpt":"Five consecutive years of EPS growth, free cash flow that consistently matches reported earnings, a ROIC of 28%, and a record backlog that provides unusual visibility into the next several quarters. The data center cooling story adds a genuine structural tailwind on top of an already-strong base business, and management has raised guidance consistently enough that the market has learned","as_of":"2026-08-13","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K Item 3 稱未決法律事項預期不致對營運、財務、流動性或現金流造成重大不利影響；最重大訴訟為 Aldrich 與 Murray 石棉破產案，未列政府反壟斷調查。","source":"SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"The most significant litigation facing the Company is the asbestos-related bankruptcy cases of Aldrich and Murray.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因素列示公司受反托拉斯等多項法規規範，違規可能面臨罰款、禁制令等；為通用風險揭露，非具體調查。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"We are subject to regulation under a wide variety of U.S. federal and state and non-U.S. laws, regulations and policies, including laws related to anti-corruption, anti-human trafficking, anti-bribery including the U.S. Foreign Corrupt Practices Act and the U.K. Bribery Act, export and import compliance, anti-trust, cybersecurity, data privacy, and money laundering","as_of":"2026-02-05","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"HVAC Equipment Antitrust Litigation：2026-03-20 於 E.D. Michigan 提起，被告含 Trane Technologies plc，主張 Sherman Act 第 1 條價格壟斷；2026-05-15 合併案件。","source":"Justia Dockets HVAC Equipment Antitrust Litigation","url":"https://dockets.justia.com/docket/michigan/miedce/2:2026cv10949/392954","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K FY2025 風險因素：美國已對多國商品加徵關稅並引發報復性關稅，另可能有進出口管制，公司稱無法預測關稅範圍，且限制可能無預警實施","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"The U.S. continues to implement certain trade actions, including imposing tariffs on certain goods imported from several countries, which has resulted in retaliatory tariffs by other countries. Additional tariffs have been proposed by the current U.S. administration and there are active negotiations for extending trade treaties. It is not possible to predict the extent or focus of any such tariffs at this time.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K FY2025 MD&A：公司持續監控2025年美國關稅與他國報復關稅，可能面臨供應鏈挑戰與商品成本波動；稱 in-region for region 策略可因應；約75%營收來自美國","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"These global trade policy changes continue to be dynamic and, as a result, we may experience supply chain challenges, commodity cost volatility, and consumer and economic uncertainty. We believe our business operating system, our in-region for region strategy, and strength in execution will enable us to navigate potential risks stemming from these recent events.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026-06-01 公告將部分 HVAC 與農業設備 Section 232 關稅由25%降至15%，至2027-12-31","source":"JD Supra: President Trump Reduces Section 232 Tariffs on Certain Agricultural, Mobile Industrial, and HVAC Equipment","url":"https://www.jdsupra.com:443/legalnews/president-trump-reduces-section-232-7053404/","excerpt":"Agricultural and HVAC Equipment Per the proclamation, tariffs on agricultural and HVAC equipment listed in Harmonized Tariff Schedule of the United States (“HTSUS”) subheadings now added to Annex III will be reduced from 25% to 15% through December 31, 2027.","as_of":"2026-06-02","retrieved_at":"20261102","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Q4 2025 財報電話會議：2025年關稅成本略高於1.4億美元，預期2026年有更多通膨影響","source":"Yahoo Finance: Trane Technologies Q4 earnings call","url":"https://finance.yahoo.com/news/trane-technologies-q4-earnings-call-070805492.html","excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"北美 21 座工廠中 20 座在美國；管理層稱在美國銷售的產品超過 95% 於美國製造或組裝。","source":"Trane Technologies Bank of America Conference Transcript 2026","url":"https://s2.q4cdn.com/950394465/files/doc_events/2026/May/13/Bank-of-America-Conference-Transcript-2026.pdf","excerpt":"21 factories that serve our North America business, and 20 of those factories are in the US. So over 95% of what we sell in the US is either manufactured and/or assembled in the United States.","as_of":"2026-05-13","retrieved_at":"20261102","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2025 年關稅成本略高於 1.4 億美元，2026 年因多一季關稅預期再增約 5,000 萬美元通膨影響；管理層先以緩解措施、必要時才訂價因應。","source":"Trane Technologies Bank of America Conference Transcript 2026","url":"https://s2.q4cdn.com/950394465/files/doc_events/2026/May/13/Bank-of-America-Conference-Transcript-2026.pdf","excerpt":"mitigation first, and then ultimately if we need to, to deploy pricing","as_of":"2026-05-13","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"2025 年約 25% 營收來自美國以外；管理層點出中東區域逆風（Q2 約 5,000 萬美元營收）與中國市場艱困。","source":"Trane Technologies Q1 2026 Earnings Call Transcript (MarketBeat)","url":"https://www.marketbeat.com/earnings/reports/2026-5-1-trane-technologies-plc-stock/","excerpt":"regional headwinds from the Middle East (~$50M revenue / ~$0.05 EPS impact in Q2) and a challenging China market","as_of":"2026-05-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露部分品項向單一或有限來源供應商採購（成本效益、法規要求、設計獨特性或產品品質），並稱許多客戶、製造營運與供應商位於美國以外。","source":"Trane Technologies plc Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261102","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026Q3：合併訂單 $7,248M（+21%）、營收 $6,760M（+18%）、積壓訂單 $12.5B（+73%）；全年營收指引上調（報告營收約 +13.5%、有機約 +11%），EPS 指引 $15.00–15.10 維持","source":"Trane Technologies Q3 2026 earnings release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 Americas 營收 $5,647.9M（+21%）、訂單 $5,681.4M（+18%）、book-to-bill 101%；商用 HVAC 積壓約 +80%","source":"Trane Technologies Q3 2026 earnings release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 EMEA 營收 $755.8M 僅 +1%、訂單 $1,109.4M（+40%）、book-to-bill 147%，GAAP 營業利益率下滑 240bp 至 17.2%","source":"Trane Technologies Q3 2026 earnings release (SEC 8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 亞太營收 $356.0M（+8%）、訂單 $457.1M（+22%）；管理層稱占亞太約三分之一的中國仍具挑戰","source":"Trane Technologies Q3 2026 earnings release / call summary","url":"https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261102","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 財報會：Americas 商用 HVAC 訂單創高、+50%，需求涵蓋資料中心與其他垂直領域；資料中心專案時程可能因場址與電力併網而位移","source":"Nasdaq: Trane Technologies Q2 earnings call highlights","url":"https://www.nasdaq.com/articles/trane-technologies-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"2026-09 報導：Carrier 與 Trane 表示住宅 HVAC 需求轉強並未消除價格壓力，關稅與投入成本持續推動漲價","source":"ACHR News: Price increases remain part of the residential HVAC outlook","url":"https://www.achrnews.com/articles/166689-price-increases-remain-part-of-the-residential-hvac-outlook","excerpt":null,"as_of":"2026-09-15","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子承認有來自非傳統製造商/服務商的顛覆性技術風險，且技術變遷加速會縮短產品生命週期；未點名具體替代品。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"While we understand our markets and competitive landscape, there is always the risk of disruptive technologies coming from companies that are not traditionally manufacturers or service providers of our products.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"ACHR News：Nvidia CEO 稱最新 AI 系統可用熱水冷卻、無需冷水機，多家 HVAC 廠商股價下跌；Rubin 系統預計 2026 下半年上市。","source":"ACHR News - Cooling without water chillers","url":"https://www.achrnews.com/articles/165793-cooling-without-water-chillers","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261102","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"ABI Research：DC 液冷目前占 DC HVAC 市場 15%（9.7 億美元），預計 2030 年達 35 億美元；營運商採液冷＋氣冷 HVAC 的兩段式冷卻。","source":"ABI Research press release","url":"https://abiresearch.com/press/ai-compute-and-regulatory-pressures-catalyze-fourfold-adoption-of-liquid-cooling-technology-in-data-centers-by-2030","excerpt":"Liquid cooling, currently 15% of the DC HVAC market at US$970 million, is forecast to reach US$3.5 billion by 2030 at a 20% CAGR.","as_of":"2026-01-01","retrieved_at":"20261102","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 描述美國銷售經由分公司、經銷商與代理商；未見通路結構性轉移的揭露","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"U.S. sales are made through branch sales offices, distributors and dealers across the country.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Trane 與 Valent（Greenheck 旗下）簽獨家供應協議，自 2026-05-18 起成為 Valent 品牌產品在美加的獨家通路（DOAS、RTU、能源回收）","source":"HVACInsider／Supply House Times：Trane and Valent announce exclusive supply agreement","url":"https://hvacinsider.com/trane-by-trane-technologies-and-valent-announce-exclusive-supply-agreement-in-the-u-s-and-canada/","excerpt":null,"as_of":"2026-05-18","retrieved_at":"20261102","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"年報稱成長策略包含透過服務與租賃擴大經常性收入；服務約占企業營收1/3、低十位數複合成長。無正式訂閱分部揭露，『訂閱』說法來自外部分析師","source":"Trane Technologies FY2025 Annual Report (ARS)","url":"https://www.sec.gov/Archives/edgar/data/0001466258/000162828026026681/tt2026_proxyandannualreporta.pdf","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261102","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 release：公司全年 2026 指引為報告營收成長約 13.5%、有機約 11%、調整後持續營運 EPS $15.20–$15.30（EPS 區間與 Q2 後相同，僅營收上調）","source":"Trane Technologies Q3 2026 earnings release, 8-K Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/0001466258/000146625826000001/exhibit991-q32026earningsr.htm","excerpt":"The Company expects adjusted continuing EPS for full- year 2026 of $15.20 to $15.30.","as_of":"2026-10-29","retrieved_at":"20261102","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 後（2026-07-30）公司 EPS 指引 $15.20–$15.30，高於當時共識約 $14.90；營收指引約 $23.8B vs 共識約 $23.4B；平均目標價約 $520（MarketBeat），Barchart 23 位分析師共識目標價 $527.77","source":"MarketBeat / Barchart / Sentisense 彙整（搜尋摘要）","url":"https://app.sentisense.ai/stories/trane-technologies-beats-earnings-estimates-and-updates-fy-2026-earnings-guidanc-07302026","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261102","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價分布（as-of 約 2026-08）：valueinvesting.io 均值 530.15、區間 444.40–614.25；StreetInsider 12 個月均值 $521.61、高 $585（Barclays）低 $460（HSBC），整體 neutral；各站數字不一致","source":"valueinvesting.io / StreetInsider（搜尋摘要）","url":"https://www.streetinsider.com/rating_history.php?q=TT","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261102","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2025-12-02 公司公告與 Stellar Energy International 簽訂definitive agreement，收購 Stellar Energy Digital 業務（8-K Item 8.01）","source":"SEC EDGAR 8-K 2025-12-02 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828025054789/tt-20251202.htm","excerpt":"On December 2, 2025, Trane Technologies plc issued a press release announcing a definitive agreement with Stellar Energy International, Ltd. to acquire the Stellar Energy Digital business.","as_of":"2025-12-02","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 8-K 共 9 份，含重大項目者 2 份（2025-12-02 Item 8.01 併購公告；2026-04-24 Item 1.01 新 15 億美元循環信貸協議）","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001466258&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"10-K FY2025：最重大訴訟為 Aldrich 與 Murray 石棉破產案，管理層認為待決法律事項預期不會有重大不利影響","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"The most significant litigation facing the Company is the asbestos-related bankruptcy cases of Aldrich and Murray.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"搜尋摘要稱 2026 年 2 月完成 Stellar Energy Americas 收購（對價約 5.534 億美元，不含 1.854 億美元取得現金）、併購 LiquidStack 剩餘股權、Thermo King 買 CSTK 經銷商、取得 Kieback&Peter 49% 股權；2026-10-21 宣布收購 Cancoil（未揭露金額，預計 2026 年底前交割）。來源為 10-Q 與產業媒體，未讀頁面逐字原文","source":"Trane 10-Q FY2026 Q3 / refindustry.com / memoori.com（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001466258/000162828026068122/tt-20260930.htm","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"Trane 宣布收購 Cancoil Thermal Corporation","source":"Refindustry","url":"https://refindustry.com/news/trane-technologies-to-acquire-canadian-heat-transfer-manufacturer-cancoil/","excerpt":"Trane Technologies to Acquire Canadian Heat-Transfer Manufacturer Cancoil The deal adds Ontario and Texas manufacturing operations and more than 450 employees, with closing expected by year-end 2026. October 23, 2026 Trane Technologies announced on October 21, 2026, that it has entered into a definitive agreement to acquire Cancoil Thermal Corporation, a Canadian manufacturer of","as_of":"2026-10-23","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2025-12-02 簽訂收購 Stellar Energy Digital 業務的 definitive agreement","source":"SEC EDGAR 8-K 2025-12-02 Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828025054789/tt-20251202.htm","excerpt":"On December 2, 2025, Trane Technologies plc issued a press release announcing a definitive agreement with Stellar Energy International, Ltd. to acquire the Stellar Energy Digital business.","as_of":"2025-12-02","retrieved_at":"20261102","affects":["thesis.H","valuation"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"搜尋摘要稱 2026 年另有 LiquidStack、CSTK、Kieback&Peter 49% 股權、Cancoil（2026-10-21 宣布）等交易；未讀頁面逐字原文","source":"Trane 10-Q FY2026 Q3 / refindustry.com（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001466258/000162828026068122/tt-20260930.htm","excerpt":null,"as_of":"2026-10-21","retrieved_at":"20261102","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"搜尋未見證券集體訴訟；10-K 稱最重大訴訟為 Aldrich／Murray 石棉破產案，其餘待決事項預期無重大影響","source":"SEC EDGAR 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1466258/000162828026005731/tt-20251231.htm","excerpt":"The most significant litigation facing the Company is the asbestos-related bankruptcy cases of Aldrich and Murray.","as_of":"2026-02-05","retrieved_at":"20261102","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單中無 Item 4.02（財報不可信賴）；搜尋亦未見 SEC 調查","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001466258&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-02 至 2026-11-02 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-02","retrieved_at":"20261102","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.99,"operating_margin_pct":17.92,"fcf_margin_pct":16.43,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TT","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CARR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":24.64,"operating_margin_pct":8.05,"fcf_margin_pct":10.43,"rd_intensity_pct":2.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CARR","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"JCI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.65,"operating_margin_pct":14.45,"fcf_margin_pct":6.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JCI","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LII","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":33.1,"operating_margin_pct":19.94,"fcf_margin_pct":15.34,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LII","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"TT"},"financial_history":{"ticker":"TT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":15991700000.0,"revenue_yoy_pct":null,"gross_margin_pct":31.05,"operating_margin_pct":15.13,"net_income":1756500000.0,"diluted_eps":7.48,"free_cash_flow":1212200000.0,"fcf_margin_pct":7.58,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":17677600000.0,"revenue_yoy_pct":10.54,"gross_margin_pct":33.13,"operating_margin_pct":16.37,"net_income":2023900000.0,"diluted_eps":8.77,"free_cash_flow":2088900000.0,"fcf_margin_pct":11.82,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":19838200000.0,"revenue_yoy_pct":12.22,"gross_margin_pct":35.69,"operating_margin_pct":17.64,"net_income":2567900000.0,"diluted_eps":11.24,"free_cash_flow":2775000000.0,"fcf_margin_pct":13.99,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":21321900000.0,"revenue_yoy_pct":7.48,"gross_margin_pct":36.16,"operating_margin_pct":18.61,"net_income":2918600000.0,"diluted_eps":12.98,"free_cash_flow":2811500000.0,"fcf_margin_pct":13.19,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TT/TT_Q3_2026_Earnings_Call_20261029.md）

# Q3 2026 Earnings Call
**Trane Technologies plc** | Earnings Calls | 2026-10-29

**Operator** (Operator):
Good morning. Welcome to the Trane Technologies Q3 2026 Earnings Conference Call. My name is Warren, and I will be your operator for the call. The call will begin with in a few moments with the speakers' remarks and the Q&A session. [Operator Instructions] I will now turn the call over to Pat Uotila, Director of Investor Relations. Please go ahead.

**Patrick Uotila** (Executives):
Thanks, operator. Good morning, and thank you for joining us for Trane Technologies' Third Quarter 2026 Earnings Conference Call. Our webcast and slide presentation are available at tranetechnologies.com, where a replay will also be archived. Today's discussion includes forward-looking statements. Key risk factors are detailed in our SEC filings. We also use non-GAAP measures. Explanations and reconciliations are in our press release and presentation appendix. Joining me on today's call are Dave Regnery, Chair and CEO; Chris Kuehn, Executive Vice President and CFO; and joining us for Q&A is Donnie Simmons, Executive Vice President and Chief Operating Officer. With that, I'll turn the call over to Dave. Dave?

**David Regnery** (Executives):
Thanks, Pat, and good morning, everyone. Please turn to Slide #3. Our focused strategy is aligned to powerful megatrends and continues to propel strong performance. Today, global energy systems are stretched and buildings still waste about 30% of the energy they pay for. If we want a sustainable and resilient energy future, efficiency isn't optional. It's imperative. Customers choose Trane Technologies because we solve this problem at scale. Our smart systems, advanced controls and deep service expertise allow buildings and industry to optimize their energy footprint in real time. This enables our customers to boost performance, reduce cost and reduce emissions and help create more resilient energy systems. 
When you combine this strong customer demand with our leading innovation and talented team, we are well positioned to deliver differentiated long-term value for our shareholders. Please turn to Slide #4. Q3 was another strong quarter. Enterprise organic bookings grew 20%, fueled by robust growth across all segments. Our commercial HVAC businesses delivered outstanding performance with global applied bookings up over 40%, driving our backlog to $12.5 billion. 
Organic revenue grew 16%, led by the Americas and with growth across all segments. Our service business, which represents about 1/3 of enterprise revenue, continues to be a resilient growth driver with low teens compound annual growth rate since 2020. All in, we delivered adjusted EPS growth of 25%. This includes a tax benefit of about $0.10 due to timing. Excluding this tax benefit, our underlying adjusted EPS growth is up 23%. We also delivered exceptional free cash flow, reaching $2.8 billion year-to-date and now expect to deliver free cash flow greater than 100% of net earnings for the full year. Given our robust backlog, strong pipeline and proven execution, we are raising our full year revenue guidance and reaffirming our EPS guidance. 
Please turn to Slide #5. Our third quarter results were driven by standout performance in the Americas segment. Commercial HVAC delivered exceptional bookings, up low double digits and strong organic revenues up low 20s. As expected, Applied Solutions revenues ramped significantly with growth exceeding 60%. Services in the Americas continues to be a key growth engine, up 10%. The residential business exceeded our expectations with both bookings and organic revenues up approximately 20%. 
Our transport business also gained momentum with bookings up in the high 30s and revenues up high single digits. In EMEA, our performance was solid and in line with our expectations. Excluding the Middle East, segment bookings were up over 50% and revenues grew high single digits. Our team in Asia Pacific delivered strong results outside of China, with bookings in the rest of Asia up 70% and revenues up in the high teens. China now represents 1/3 of our Asia Pacific segment. Now I'd like to turn the call over to Chris. Chris?

**Christopher Kuehn** (Executives):
Thanks, Dave. Please turn to Slide #6. As Dave highlighted, enterprise organic revenue grew a strong 16%, supported by robust equipment and services growth. Adjusted EPS increased 25%, underscoring the power of our business operating system. We are capitalizing on unprecedented demand, which has created near-term supply chain and inflationary pressures that we are actively mitigating. A prime example is our recent acquisition of Cancoil, one of our key suppliers, which strengthens our supply chain and bolsters our heat transfer expertise. 
Leverage in Q3 improved versus Q2, and we are confident we will see further leverage improvement in the fourth quarter, driven by both higher price and productivity. Please turn to Slide #7. Our third quarter performance reflects solid execution in a dynamic environment and strategic reinvestment for future growth. Operating income margins in the Americas expanded by 50 basis points on strong volume growth that helped offset inflationary and supply chain headwinds. In EMEA, we delivered solid performance in Europe with segment margins impacted by the continued conflict in the Middle East. Excluding the Middle East, our commercial HVAC business leveraged above 25%. Asia Pacific margins were impacted by challenging markets in China, balanced by notable strength in the rest of Asia. With that, I'll turn the call back over to Dave. Dave?

**David Regnery** (Executives):
Thanks, Chris. Please turn to Slide #8. Commercial HVAC Americas continues to set the pace with another quarter of exceptional bookings and backlog. Data centers continue to be a powerful driver, and our core markets also remain strong. Year-to-date, we delivered growth in 11 of our 14 verticals. As a result, we are raising our full year commercial HVAC organic revenue outlook. In residential, we are also raising our full year outlook, reflecting our strong year-to-date performance. 
Transport markets continue to show improvement, and we expect strong revenue growth in the fourth quarter, leading into a 2027 recovery. In EMEA, we continue to expect flattish organic revenue growth for the full year, with commercial HVAC offsetting headwinds in the Middle East and transport. In Asia, we expect strong demand in the rest of Asia to offset challenges in China. With that, I will turn the call back to Chris. Chris?

**Christopher Kuehn** (Executives):
Thanks, Dave. Please turn to Slide 9. For the full year, we are increasing our organic revenue growth outlook to approximately 11% and reaffirming our adjusted EPS guidance range of $15.20 to $15.30. For the fourth quarter, we expect organic revenue growth in the mid-teens with adjusted EPS of approximately $3.40 to $3.50. This includes a $0.10 headwind from a higher fourth quarter tax rate, which neutralizes the third quarter benefit and keeps our full year effective tax rate forecast unchanged at 19%. 
Looking at the balance of the year, we are updating our full year price realization expectation from 1.5 points to approximately 1 point, primarily reflecting timing and mix across our shorter-cycle businesses. We expect price to accelerate in the fourth quarter to approximately 1.5 points at the enterprise and close to 2 points in the Americas segment. 
We now expect organic leverage to land in the low 20s, an adjustment from our prior expectation of 25% plus, primarily due to the updated price expectation and near-term supply chain and inflationary headwinds, all of which we are actively managing. Please turn to Slide #10. We remain committed to our balanced capital allocation strategy, which is focused on deploying excess cash to maximize shareholder returns. 
First, we strengthen our core business through relentless and strategic reinvestment. Second, we maintain a strong balance sheet to ensure optionality as markets evolve. Third, we are on track to deploy 100% of excess cash over time. Our disciplined approach includes pursuing strategic M&A to enhance long-term returns and executing share repurchases when our stock trades below its calculated intrinsic value. 
Please turn to Slide #11. We now expect to deploy more than $3.4 billion in 2026, exceeding the high end of our prior range. A key pillar of this strategy is our commitment to shareholder returns. Earlier this year, we increased our dividend by 12%. We also repurchased approximately $1.4 billion of shares year-to-date with significant share repurchase authorization remaining. Our M&A pipeline is active. During the third quarter, we committed to 3 strategic acquisitions, including Cancoil, which we expect to close in late 2026 or early 2027. We now expect CapEx of approximately 2% of revenue in 2026, which will further bolster our strong free cash flow and balance sheet position. And with that, I'll turn the call back over to Dave. Dave?

**David Regnery** (Executives):
Thanks, Chris. Please turn to Slide #13. In Americas Transport, we are seeing positive signs after a multiyear downturn. Preliminary discussions with customers have been encouraging, and we believe the markets will continue to improve into 2027 and enter a multiyear up cycle. Please turn to Slide #14. While we'll provide formal 2027 guidance on our fourth quarter call, I'll share an early view based on current insights. 
Globally, commercial HVAC remains very strong, led by our innovation and direct sales force. With backlog up more than 70% from the prior year, we are well positioned for strong growth in 2027. For Residential, we will be exiting 2026 with normalized channel inventories and stronger momentum than the year before. We will be monitoring the interest rate environment and other economic indicators as we move into 2027. In Thermo King Americas, as discussed, we expect market conditions to strengthen through 2027. Services, representing 1/3 of our business, remains a resilient growth engine, powered by our expanding Applied installed base and digital energy management solutions. 
Underpinning all of this, our business operating system continues to drive productivity while navigating inflation and supply chain dynamics. In short, we are well positioned for strong performance in 2027 and beyond. Please turn to Slide #15. In closing, our strategy is aligned to powerful mega trends that are intensifying the need for our sustainable solutions and services. Customers choose Trane Technologies for our leading innovation, strong execution and the expertise of our team around the world. With our clear strategy, elevated backlog and booking strength across all segments, we are confident in raising our full year revenue guide and well positioned to deliver differentiated shareholder value. And now we'd be happy to take your questions. Operator?

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Andy Kaplowitz with Citi.

**Andrew Kaplowitz** (Analysts):
So Dave or Chris, maybe just a little more color on what you're seeing in terms of the competitive environment in Americas Commercial HVAC. Obviously, orders in the Americas were still good in mid-teens, but it did decelerate from Q2, and I'm sure you can tell me data center orders are lumpy, but maybe you can elaborate on what you're seeing in terms of the visibility towards continued strong order growth in Americas Commercial HVAC.

**David Regnery** (Executives):
Yes. Andy, it's a fair question. And yes, look, they are lumpy. I think you know that. But look, I think that the pipeline of activity that we're seeing is still very, very robust. And that's very encouraging to me. So I know I've read some of the pre-reports and I know that there's some conversation about orders are slowing. Let me tell you something. We're not concerned about orders slowing. In fact, the pipeline continues to grow. And we're seeing that not only in the Americas, but we're really seeing that around the globe. 
When you and I were together a few weeks ago, we talked about Europe, and I told you that we're seeing a strong pipeline there. I'm happy to say that some of that pipeline converted to orders. We actually even had more upside than I thought there with orders where if you exclude the Middle East, they were up over 50%. And we had very strong orders in the rest of Asia. So orders are -- those -- to me, the order rate was a positive and the pipeline remains very, very robust. And just to reiterate, yes, the data center orders will be more lumpy, and they're larger than what we would see in our core verticals.

**Andrew Kaplowitz** (Analysts):
And then Chris, I know you lowered your incremental margin guide for the year a bit, but your Americas incremental margin was just south of your 25% long-term target. So maybe you could give us more color in terms of the price cost dynamic that you're seeing. Have you been more aggressive with pricing in your residential business? And how are you thinking about your ability to get back to that 25% normalized incremental in '27?

**Christopher Kuehn** (Executives):
Andy, no change to our long-term framework here of 25% or greater. There are some impacts this year in terms of navigating through a little bit lower price than we expected. And let me spend a moment on that. Look, comps matter in the third quarter, we delivered over 3 points of price last year at the enterprise. And actually, the Americas delivered over 4 points of price. 
In our residential business, we're still experiencing some of the impacts of the transition to the 454B product. Just a reminder, we account for that price actually in volume. That normalizes next year, but that's part of the story here for 2026. And pricing did come in a little bit lighter in the third quarter than we expected, and it's really due to timing and mix in our short-cycle businesses. I'll give you an example or 2. Residential had a very strong quarter, up 20% in terms of revenues in the third quarter. And when you think about incentives in the IWD channel, as you have higher volumes, there's more incentives there. 
So we wound up not expecting as much growth in the third quarter in residential that we delivered, but the incrementals on the incentives wound up just being a little bit of a headwind on price. On the mix side, our Transport Americas business delivered 10% revenue growth in the quarter. And we saw the mix to the larger fleet customers, which with the larger volumes that they buy from, they get a little bit better pricing for that. 
The good news is that's typically the start of the uptick of the cycle where the larger fleets start buying earlier. So again, on the way we account for it on price, a little bit lower than we expected. But I'll tell you, going into the fourth quarter, we're expecting price to be stronger than the third quarter. Think of that around 1.5 points at the enterprise, closer to 2 points at the Americas segment, and we're putting all of our plans in for next year as well.

**David Regnery** (Executives):
And our incremental leverage in the fourth quarter, we're projecting to be north of our target range.

**Operator** (Operator):
Your next question comes from the line of Scott Davis with Melius Research.

**Scott Davis** (Analysts):
Can you hear me okay?

**David Regnery** (Executives):
Yes, how are you?

**Scott Davis** (Analysts):
I'm glad you can hear me. The last call, seemingly was on mute, I guess. But anyways, I'm kind of confused. Are supply chains getting worse or better? They almost feel like they're getting worse. Is that just -- maybe just how we're seeing it, but what are the remaining bottlenecks? And kind of how are you guys seeing it?

**David Regnery** (Executives):
Yes. I'll start with, yes, we did see supply chain headwinds build as we move through the quarter. However, I will tell you that our team has done a great job of managing through this. Some of this was caused by what I would call like ordinary supply and demand constraints as we ramp up demand on our suppliers, specifically around like fans, coils, heat exchangers, we're putting a lot of demand on our supply partners. And obviously, they're trying to expand their capacity. We're working with them, helping them become great lean operators, but it is putting stress on them. I think that's going to continue through the -- I know that will continue in the fourth quarter. We'll see that get better as we work through the first half of 2027. 
Also in the quarter, though, we had to navigate some sudden regulatory changes in early August, and I'm not sure if you're aware of this, but more than 40 companies were added to what they call the UFLPA list. So this is a list that blocks goods tied to where there's perceived forced labor from entering the U.S. And unfortunately, in our case, one of our lower-tier suppliers, so think of this as like a Tier 4 to us, maybe even a Tier 5, they make capacitors and they sell to some of our motor suppliers as well as some of our drive suppliers. And what that did was it caused them to have to pivot and find another source. Well, they did that in the quarter. Unfortunately, caused us to have a couple of weeks where we didn't have supply. And these, both drives and motors are components that we are kind of just in time for in our manufacturing locations. 
So we had like 3 or 4 of our plants where we were running product down the line and we didn't have all the components. Then we had -- when the components came in, we had to put those products back on the line and that caused a relatively large disruption as well as a large cost for rework. The good news there is that's behind us. At least 80% of it was behind us at the end of the third quarter. As we speak today, it's 100% behind us. That rework has all been done now. 
Unfortunately, it was an unforeseen item that hit us, and our team reacted quickly. Part of our operating system is, believe it or not, to run a line without all the components and how do you do that? So we acted quickly and implemented that. It just was a cost for us in the quarter, and it's behind us now. But look, those things can happen from time to time. It's really how agile you are to be able to adapt to those. And I would tell you with our operating systems, we're pretty agile, and I'm proud of what our team was able to accomplish with some pretty stiff headwinds in front of us.

**Scott Davis** (Analysts):
So, just a natural follow-on. I mean, you announced this Cancoil deal. Is this -- are we going to see other types of transactions like this where you guys really just need to be able to control more around your supply chain and just take that risk off the table, assuming there could be a pretty long up cycle in front of us. Is this the type of mitigation that we should expect more deals like this?

**David Regnery** (Executives):
Yes. Look, Cancoil is a great company, okay? They've been a supply partner of ours for years. Think of them as manufacturers of coils and heat transfer products. They have a lot of expertise there. It's going to be a nice bolt-on for our company. So we're going to continue to -- if opportunities like this continue to present themselves, we'll be looking at them. And obviously, as a major HVACR player, we're going to get to see lots of opportunities. But this one, in particular, it certainly helps us with our supply chain resiliency. And that's obviously one of the reasons why we jumped at it. And also the expertise that they're bringing to us is also going to help us in other areas. I don't know, Donnie, if you want to add anything?

**Donald Simmons** (Executives):
Yes, I would just add they're a really great partner of ours. We represented roughly 40% of the volume. So we're already a major player for them. So us bringing that in-house is a big benefit. Think of these as very large coils that go into large air handlers and large air-cooled chillers. So this really does help solve one of our core component issues from a supply chain perspective.

**Operator** (Operator):
Your next question comes from the line of Julian Mitchell with JPMorgan.

**Julian Mitchell** (Analysts):
Maybe just a first question, please, around organic operating leverage. So I think as you said, that steps up above the sort of placeholder in the fourth quarter. So maybe it's close to sort of 30% after low 20s in Q3. Just trying to understand the drivers of that and how sustainable that rate is as we look into early next year. I realize the comp was very easy from the Resi headwinds in Q4 last year. Is that what's helping it or a onetime catch-up on the component shortage reversing? Just trying to understand sort of how you're thinking about that organic operating leverage driver in Q4 and then beyond.

**Christopher Kuehn** (Executives):
Yes, Julian, it's Chris. So the way you described it, exactly right. The comps are easier in the fourth quarter. When we think about the third quarter leverage last year was actually over 50%. So a tough comp in the third quarter. But it sequentially gets better in the fourth quarter, a little bit easier comps on price. We've announced a number of price increases this year, and that continues to stick. Dave described some of the challenges around supply chain in the third quarter that are behind us now. So that is not carrying over into the fourth quarter. And I think at this point, we're looking forward to ending the year on a strong momentum in terms of leverage, and we're putting the plans in for next year to return to the 25% plus algorithm. That's our long-term algorithm for a very long period of time.

**David Regnery** (Executives):
The only point I would add, Julian, is remember, in our -- in EMEA, okay, if you look -- if you take our commercial HVAC business and you look at that at the segment level and then remove the Middle East, it leveraged at over 25%. So it's really kind of isolated as to where we're seeing the issues, the supply chain here for sure. Inflation has been a little bit higher than we thought. Middle East is going to -- next year, obviously, that's going to be -- hopefully, that gets resolved, but obviously, it's going to be easier comps there. But we're confident in our long-term framework, and that's the important part I want all investors to take away. Our long-term framework continues to be the 25% plus, and we're going to continue to invest heavily in our business so we could maintain the future growth that we believe is all possible for Trane Technologies.

**Julian Mitchell** (Analysts):
That's helpful. And maybe just one follow-up, Dave, in a way to where you left off on reinvestment. Just wondered, as you look across the business, particularly some of the larger pieces like Applied, Commercial HVAC, on the smaller side, Residential, do you see anything changing in terms of competitive dynamics? I think residential, a lot of companies are struggling to get price. And then on the applied side, we receive a lot of questions about a lot of supply coming on from different manufacturers and could that affect pricing? Any thoughts on that, please?

**David Regnery** (Executives):
Yes. I mean on the pricing side, look, you -- I've been saying this for a long time. As you become an innovative company, right, it helps with pricing. So we're going to continue to invest in our innovation. We're going to continue to invest in what the future is going to be for thermal management systems and whether that's in the data center or that's in our core market, that's fundamental to who we are. So we're never going to back off of those high investment levels because we know we could always sell innovation to our customers. We could always sell total cost of ownership. We could always sell efficiency. So that's our strategy. It's been working quite well for the last 5 or 6 years, and it's going to work well into the future as well.

**Christopher Kuehn** (Executives):
And Julian, to be clear, Residential delivered positive price in the third quarter, sequential improvement from the second quarter. It remained a little bit lower than we thought based on the fact that we had much stronger volume growth in that IWD channel and the incentives I previously mentioned. 
But the business has announced 2 price increases this year, early April effective date, early July effective date to continue to take all the cost inputs and leveraging our business operating system to drive not only negotiations with suppliers, ultimately productivity. And then to the extent there's still inflation, we'll look at pricing, but just leveraging the business operating system here for that business as well. But again, sequential improvement in price, and we'd expect that to continue to be better in the fourth quarter than in the third quarter.

**Operator** (Operator):
Your next question comes from the line of Amit Mehrotra with UBS.

**Amit Mehrotra** (Analysts):
Maybe this one is for Chris. Just a quick one on Stellar. I know you have $500 million going to $1 billion run rate in '28, currently sort of neutral to EPS. What is the normalized margin opportunity? That's obviously a big ramp in revenue. What's sort of the normalized margin? And when can that sort of become more meaningfully accretive?

**Christopher Kuehn** (Executives):
Yes. No change to the outlook for Stellar for 2026 and around $500 million of revenue and really neutral on the earnings line. We described a few months ago in our last call around the investments we saw in the business to scale with volume. One of our large investments is not only the factory in Florida, but also the new factory that's in the process right now of commissioning in Texas. So continue to execute on those investments here in the quarter. And we've described it, Amit, as in a couple of years now -- in a couple of years' time, mid-teens EBITDA opportunity. 
So we'll see as we put our plans together for 2027, but backlog remains very strong. The fundamental theme of modular designs and the need for modular chiller plants on job sites remains very, very strong. And we're putting the investments in place to be ready for a couple of years right now to make it a $1 billion revenue business with mid-teens EBITDA.

**David Regnery** (Executives):
And the pipeline remains very strong, the activity we're seeing there within the Stellar business. And just so everyone is clear, Stellar today is predominantly almost 100% data centers. We believe that will continue to be an opportunity, but we believe this will move to our core verticals as well. We just want to make sure we're ready. That's why we're spending a lot of money deploying our operating system so we could flex more as our customers' needs.

**Amit Mehrotra** (Analysts):
And just as a quick follow-up, Dave, I know you talked about the lumpiness of orders, but the decline, at least sequentially in orders in the Americas was double digits. Book-to-bill is still above 1, but it was down a lot, and you talked about interest rates. And is it really just lumpiness? Is that what explains it? Or are there sort of some non-data verticals that are a little bit also longer cycle that are starting to feel a little bit of this pause on from an interest rate perspective?

**David Regnery** (Executives):
No, I would say it's lumpiness. I mean, look, if you look at mega projects, and I know I'm the one who probably doesn't like looking at mega projects, but that list continues to grow. I mean we were in the second quarter, we were talking about tracking 1,400 projects. We're tracking 1,700 projects now. Now some of those have greater opportunities than others. A lot of those are -- over 90% of those are data centers, but there's also some nice high tech in there as well. So look, it's going to be lumpy, okay? These orders are quite large. And I am not concerned about order rates. In fact, our backlog now at $12.5 billion, look, we're executing well on the front end of our business. Pipeline is strong. We'll continue to have a bit of lumpiness, but we also continue to see strong order growth.

**Operator** (Operator):
Your next question comes from the line of Steve Tusa with Wells Fargo.

**David Regnery** (Executives):
Steve, another voice. Glad to hear you again. I saw you on TV the other day. You look great.

**Charles Stephen Tusa** (Analysts):
Yes. Not feeling good this morning, but it is what it is. And thanks happy to be back for sure. Just on the backlog, you guys give kind of a figure of what's booked for forward years. I think it was $6 billion last quarter. What's that number roughly around now?

**Christopher Kuehn** (Executives):
Yes. It's over $8 billion of the $12.5 billion of backlog at the end of September would be for 2027 and beyond, Steve. So that continues to grow.

**Charles Stephen Tusa** (Analysts):
Okay. And then if you guys actually reported kind of price mix, if you will, in resi, I think there's a bit of confusion out there, just the way you guys report. What would price/mix have been in the quarter? And then what are you guys actually expecting for price cost this year, however, is the right way to look at that? I mean, are you guys like underwater neutral-ish, a little bit positive? I assume you're below kind of the 20 to 30 bps algo that you usually target.

**Christopher Kuehn** (Executives):
Yes, I'll start with your second question. We've described price versus inflation this year as being a headwind. It was in the third quarter. We're anticipating that for the fourth quarter and the full year, and that is baked into our guide. We continue to remain nimble here as we think about offsets to inflation. And one of the levers there as we leverage our business operating system will be price. So we're actively managing that. But do expect it to be a continued headwind through the balance of this year.
On residential, when we launched the 454B product last year, think of that as the pricing on that was in the high single-digit range. And we've accounted for all of that in volume. And that carryover into 2026 is also reported in volume for us this year. If I look at on a year-over-year basis, we have positive price on those products. So again, we're accounting for 454B initially in volume. On a year-over-year price, it's positive, and that will all normalize as we go into next year.

**Charles Stephen Tusa** (Analysts):
Sorry, one more quick one. There's a lot of hysteria out there about these hybrid ductless products. You guys, I think, have a pretty nice hedge through your Mitsubishi Trane JV. Am I correct about that?

**Donald Simmons** (Executives):
Yes. Steve, this is Donnie. Yes, we do have a partnership there with Mitsubishi that helps us with the hybrid systems. I think a lot of the discussion you're hearing is also around a side discharge outdoor unit. We also have that in our own portfolio as well. That -- the trend in the marketplace is that part of the portfolio is growing, and we would expect that to continue to grow.

**David Regnery** (Executives):
But with 20% growth. A lot is growing in resi.

**Operator** (Operator):
Your next question comes from the line of Tobe Okwara with Morgan Stanley.

**Tobenna Okwara** (Analysts):
I wanted to follow up on some of the service commentary. I mean it looked like the comp was getting easier quarter-over-quarter, but the organic still stepped down. Is there anything to call out there? Is it just some timing differences? Or how should we think about it?

**David Regnery** (Executives):
Look, our service business is strong. I mean, if you took the Middle East out of our number, our service business on a global basis was over 10% again. And if you go back, I think we're back to 2020, I was quoting numbers where our compound annual growth rate is in that low teens rate. So this is a very strong, very dependable engine that we have in our company, and it represents approximately 1/3 of our revenues. 
And I would tell you that it doesn't happen by accident. We invest heavily in our service business, whether that be on the training side or that be the tools that we provide our service techs, so they're the best possible in front of our customers. Remember, all of our service technicians are company employees, company trained, and they do a great job every day of representing Trane Technologies with our customers.

**Tobenna Okwara** (Analysts):
And kind of to follow-up on that piece and also kind of tying into the broader labor side of it. How much does market labor constraints kind of factor into some of the supply chains and inefficiencies you've called out? And any sense on how like hiring and training practices are trending in second half and potentially for '27?

**David Regnery** (Executives):
Yes. I mean -- just so I'm clear, is your question on the service side or is it on the supply side or both?

**Tobenna Okwara** (Analysts):
The labor side, both for service and for your own manufacturing.

**David Regnery** (Executives):
So on the service side, I'll start with that. And we saw this coming probably, I don't know, I'll say, 3 years ago. And we've developed apprenticeship programs where we're basically developing some of the best technicians in the world in our company. And this is a very -- it's registered with the Department of Labor here in the United States. It's a very robust program. Think of it as a 4-year program. Some of it is classroom, some of it's on the job, mentorships. I mean we're really proud of what we've been able to accomplish with that program. 
And we're getting a lot of -- I was at an event recently out -- in Detroit, and we were actually presented an opportunity to describe this so other companies can learn from what we've been able to do to really promote work in the essential workforce as it's being referred to as. So look, we're very proud there, and that pipeline continues to grow. I think we have now over 350 in the program, and that number is going to continue to grow. So that's a good sign. 
On the supplier side, that's one I can't really comment too much about. I'm not -- I don't have that level of detail. I would just tell you that skilled labor, the essential worker is certainly something that we all need to make sure that we're helping to develop the next set of workers that are going to continue to make the United States and really all of the manufacturers around the world, great manufacturers. And we're participating certainly within our own operations, whether that be in our service organization or in our plants to make sure that we develop, we create career ladders. And people understand that if you come to Trane Technologies, it's not just a job for a year, it's a job for a career. And we want all of our employees to think that way.

**Operator** (Operator):
Your next question comes from the line of Joe Ritchie with Goldman Sachs.

**Joseph Ritchie** (Analysts):
So look, I want to focus on some of the announcements you've made recently. You had the successful lab demonstration for 800-volt DC architecture and then the 250-megawatt reference designs with Stellar. I'm just wondering, as you talk to hyperscalers, how quickly are these like next-generation systems and modular plants moving from reference design to the actual pipeline? And then also, how does that change your content per facility?

**David Regnery** (Executives):
Yes. If I told you the answer to the first one, we wouldn't be here, but no, I kid you. Look, we're doing a lot of work with hyperscalers and other influencers and the 800-volt direct current system that we were able to demonstrate, okay, that's going to happen, okay? We could all get varying levels as to the when, okay? I would just tell you that we'll be ready. And when we get the right standards developed around that, we're more than capable of delivering that. And that's a good thing, right? In the data center vertical, Joe, and I've said this for a long time, innovation has continued to evolve very, very quickly. And I want everyone to know that we're sitting at the table helping to develop the future data centers. And they referred to as reference design or next generation, but we're there, we're developing it, and it's fun and it's exciting. On the CDU, Donnie, I don't know if you want to comment on that?

**Donald Simmons** (Executives):
In terms of...

**David Regnery** (Executives):
Was it the 250 megawatt from LiquidStack...

**Donald Simmons** (Executives):
Yes. So that modular design that we have there is -- I mean, your question is how fast will that be adopted? I mean we've got orders in the pipeline now that we're projecting to be -- to come in for that portfolio. So it's very positive.

**Joseph Ritchie** (Analysts):
Great. That's helpful. And then just a quick one on the EMEA margins. I know that the Middle East is like roughly 15% of that overall business. How much of the margin impact that you're seeing this year is coming just from the Middle East situation?

**Christopher Kuehn** (Executives):
Joe, it's Chris. Yes, for the third quarter, if you think of it as probably 80-plus percent of the impact of the margins in EMEA are due to the conflict in the Middle East. It's important to look at the dollars as well as the percentages. So when you look at the dollars on a year-over-year basis, it's around $18 million of an operating income impact lower this year than last year. And of that, I'd say over 80% of it is really due to the deleverage in the Middle East in terms of the conflict. 
The other piece of it would be we've done some acquisitions in the region, and we're making some modest investments there to take what I'd call lower-margin businesses and ultimately make the investments to have them grow. But the Middle East is certainly having a big impact on the segment itself. The good thing is if you take the Middle East out and you look at commercial HVAC across the segment, leverage is over 25% in the quarter. So it's executing well, and we'll get through, to Dave's earlier point, we'll see what this means for 2027, but it's unfortunately a big impact to the segment.

**David Regnery** (Executives):
I'm very happy -- Joe, I'm very happy with the order rates that we're seeing in EMEA. That's going to give us a lot of momentum as we move into 2027. So Middle East will -- obviously, the comps are going to get easier there. Chris explained to you how that does have a pretty big impact on our margins there, but we'll get behind that. Hopefully, the world gets behind and we don't have a war going on. But the order rates that we saw in the third quarter were very, very encouraging to us.

**Operator** (Operator):
Your next question comes from the line of Andrew Obin with Bank of America.

**Andrew Obin** (Analysts):
Just want to confirm, when you said that pricing in third quarter was below expectations, was that both Residential and Commercial or just Residential, sorry?

**Christopher Kuehn** (Executives):
Think of it really in the short-cycle businesses, Andrew. Think of, say, Residential and Transport were really the big drivers there. And unitary as well. So I think about, again, the strong performance in both of those businesses on a revenue side and in the short-cycle businesses in Residential, the higher incentives and in Transport, the mix up to the larger fleet customers, really a Q3 impact. We don't see that repeating into the fourth quarter, but it is having an impact on the full year, and that's why we're expecting pricing for the full year to be around 1 point. but pricing in the fourth quarter will accelerate versus the third quarter. Think of that as around 1.5 points at the enterprise and approaching 2 points at the Americas segment in Q4.

**David Regnery** (Executives):
Which will again...

**Andrew Obin** (Analysts):
Applied was fine, right?

**Christopher Kuehn** (Executives):
Yes, positive price in commercial HVAC.

**David Regnery** (Executives):
And pricing in Q4, Andrew, is going to provide some momentum going into 2027.

**Andrew Obin** (Analysts):
And then just a follow-up on EMEA, the strong orders. Is it technology -- because clearly, you're very active with new technology introduction in Europe. But are you seeing any discernible change in attitude towards just HVAC, getting a bit of a mixed message. Some OEs are more constructive that we are seeing some change after last year's heat wave and some basically say, hey, not much is happening. Where do you sort of stand on that?

**David Regnery** (Executives):
Obviously, I think for sure, that will have an impact. You're probably going to see it more on the Resi side, maybe than on the Applied side. But I'm sure there will be an impact there. Look, Europe, the pipeline of activity is in both core and in data centers. So it's really both. So we're very proud of what that team has been able to develop and deliver around the innovation. I think we've talked about this in the past with thermal management systems there really just kind of changing the game. And in Europe, there's the carbon footprint and how we can really help our customers reduce their carbon footprint is still super, super important, and we have great solutions that we're winning with our customers in really all of our verticals there.

**Donald Simmons** (Executives):
Yes, I would add to that, which is a lot of times we talk about electrification of heat. So you're asking about air conditioning. But when we look at -- the electrification of heating in Europe is also growing where then we're able to provide both cooling and heating from the same plant as opposed to having a boiler operation and a chiller operation providing an Applied solution to a customer.

**Operator** (Operator):
Your next question comes from the line of Noah Kaye with Oppenheimer.

**Noah Kaye** (Analysts):
Good. So Dave, you said in the past, we're kind of 4 years into the 18-month recovery on Transport. And it looks like you're finally seeing some inflection there. So mix issues in 3Q aside, is it still fair to think about the incrementals on that recovery being above the 25% organic kind of average for the company? And I would assume that partly supports better 4Q organic incrementals, but maybe just frame for us what recovery means.

**David Regnery** (Executives):
Yes. Look, first of all, very bullish on our Thermo King business in the Americas. They had order growth over 30%, which is great to see. As Chris said earlier, a lot of that was the large fleets, we tend to see the large fleets jump in faster, okay? So that's good -- that's a great sign. And I would tell you that we also have fundamentals that would say the recovery that ACT is forecasting, maybe it's not at the 28% growth that they have for 2027, it will be a robust number, which is going to be great for that business. Chris, I don't know if you want to talk about the incrementals.

**Christopher Kuehn** (Executives):
Look, as we think about volumes coming up, it will give us a nice opportunity to get strong incrementals on volume. We're obviously putting all of our plans in place as we think about pricing for next year. The business actually opened up the order book here in October for the first half of 2027. We're remaining very nimble around the cost inputs to think about what pricing needs to be, and they're executing their business operating system. So look, it should be very much a contributor into next year as we think about 25% or better incrementals as we start and look into every year.

**Noah Kaye** (Analysts):
And then it looked like the M&A impact to reported leverage was -- actually looks a little better now versus the prior guide. So maybe just unpack that a little bit for us. Is it more operating profit? And what is better versus your prior expectations given your earlier comments on Stellar?

**Christopher Kuehn** (Executives):
Yes. I mean Stellar hasn't changed in terms of the revenue and/or the expectations on bottom line performance. We've purchased a couple of other businesses here in the channel, namely in transport and a few others we mentioned earlier. But a little bit of lot of small numbers here on the delta. It will still be meaningful of a 500 basis point delta between reported incrementals and organic incrementals. But we're still seeding these acquisitions with investments, making sure that we've got strong growth going into next year.

**David Regnery** (Executives):
And, Noah, obviously, as the longer we own some of these businesses and we deploy our operating system, we certainly see them improving as we deploy them.

**Noah Kaye** (Analysts):
So there's maybe some of that improvement already.

**Operator** (Operator):
Your next question comes from the line of Nigel Coe with Wolfe Research.

**Nigel Coe** (Analysts):
Can you hear me okay?

**David Regnery** (Executives):
Yes.

**Nigel Coe** (Analysts):
So maybe to start off with maybe just a bit more color on '27 as you see it. I know you haven't given guidance, but I'm just curious of that backlog, how much of that backlog is convertible or shippable in '27? And then if we do get to the 35,000 unit market for TK Americas next year, 30% growth, how much of that -- how does that translate to an actual segment number for Trane?

**David Regnery** (Executives):
Yes. As far as the backlog goes, Chris already talked about this, we got $8 billion beyond 2027. Some of that is in 2028, though. So just be aware of that. And remember, our backlog is equipment only. So there's no services in that number. On the Thermo King side, look, I don't believe that ACT has a number out there in 2027. I think they -- I think it came down a little bit. I think they're at 28% growth. I don't think that's realistic for a lot of other reasons like basically, can trailer OEMs actually ramp up at that level? I don't think they can. But I think it's going to be a robust year for Thermo King in 2027, which -- and beyond, by the way. 
These up cycles don't -- they're not -- they tend to go for a longer period of time. And yes, you're right, we've been in a trough for a while, and I'm just glad to -- I'm glad to see that trough hopefully ending. And I look forward to reporting our fourth quarter results here in January and hopefully be able to tell you that story is continuing.

**Christopher Kuehn** (Executives):
Yes. And Nigel, just on the...

**David Regnery** (Executives):
Sorry, go over.

**Christopher Kuehn** (Executives):
Backlog, that's for 2027 and beyond. And as Dave described, there's probably some backlog we're already building here for 2028 that could be over $1 billion at this point.

**Nigel Coe** (Analysts):
And then I'm sorry to be annoying. I just want to go back to the price question. Obviously, we'll get the price kind of disclosure in about a few hours in the 10-Q. We're back into like 50 basis points or so for the enterprise. Based on your comments around Resi and Commercial, if you want to confirm or deny that, that's helpful. But APAC last quarter was slightly negative. And just given the margin performance in APAC, I'm wondering if that's maybe gotten a bit worse and I'm thinking of China perhaps, but any comments on that would be helpful.

**Christopher Kuehn** (Executives):
Yes. I'll share with you the numbers you'll see. I mean, for the third quarter, you're right, Enterprise was around 50 basis points. Americas was up about 60 basis points in price, so positive price in the Americas. To my earlier comment about Transport and the mix to the larger fleets, Transport was actually negative in the quarter based on that mix. So it just gives you a little bit maybe more insight on the Americas sub-businesses. But EMEA had positive price of 50 basis points, and Asia did have negative price of around 1 point, really all attributable to China here as we're just, again, focused on the customers we want to do business with.

**Operator** (Operator):
Your next question comes from the line of Joe O'Dea with Vertical Research.

**Joseph O'Dea** (Analysts):
Can you elaborate on the inflation side of things, where it stands now for 2026 relative to how you were thinking about it earlier in the year? And then any detail on the different buckets. So if we think about commodities and components or logistics and supply chain inefficiencies and tariffs, just to unpack some of the inflation drivers.

**Christopher Kuehn** (Executives):
Yes. Versus 3 months ago, 6 months ago, 9 months ago, I put all those categories into higher inflation, Joe. Obviously, the commodity markets and the metals markets, we can see where that is net inflationary, fuel cost inflationary, Tier 2, be it electronics and components inflationary. So it's been a pretty dynamic year as we think through the inflation. We described this year as a bit of a headwind as we think about price versus inflation. And we're putting our plans in place for next year to return to our long-term algorithm of positive price over inflation, 20 to 30 basis points. 
So we're going to measure twice and cut once here, so to speak, but we'll provide more color on that in our Q4 call, but it has remained an inflationary environment, and we're going to drive for the negotiations with suppliers. We're going to drive the productivity in the plants. And whatever is left over, we're going to look at pricing as we leverage our business operating system.

**Joseph O'Dea** (Analysts):
That's helpful. And then shifting to Americas Resi HVAC. Can you just talk a little bit about direction of travel there? Good growth in the third quarter, the year pacing better than initially thought. It does look like that growth is expected to slow in the fourth quarter. Was there any pull forward ahead of anticipated price increases? Anything that you're managing before price increases? And then just bigger picture, the confluence of replacement demand versus mortgage rates and consumer sentiment, how you're thinking about demand in Resi HVAC moving forward?

**David Regnery** (Executives):
I mean, I think as far as the third quarter goes, obviously, stronger than we anticipated. We already talked about that. I'll remind you, it was a relatively easy comp there, too, but it was certainly stronger than we thought. Look, the fourth quarter, there's no pull-through. There's no pull forward there. So I think that the fourth quarter will be fine in the fourth quarter. 
I think when you start getting into 2027, not ready to guide 2027 yet, but obviously, we have to have our eyes wide open, as I said in our prepared remarks around the fact that we'll pay attention to what's going on with interest rates. Obviously, that could be an impact. But we think that the Resi business, we've been more bullish on Resi than maybe others have been certainly in 2026. And I think that's proving to be accurate. We see what happens in 2027. On the repair versus replace, look, we haven't -- we had a very strong quarter in completes. We had a very strong quarter, we call our supply business or parts. So we're not really seeing any clear direction there. whereas last year, obviously, we saw a lot of repair versus replace just because the refrigerant to block that occurred, we weren't able to get complete units installed.

**Christopher Kuehn** (Executives):
Joe, let me add. Year-to-date sell-in and sell-through are roughly equivalent to each other. Inventory in the channel at the end of September was in very good position. That's very similar to where we saw it throughout each of the quarters this year. And for the fourth quarter, in terms of our guide, we're expecting residential to be up in that high single-digit range, again, with easier comps on a year-over-year basis. But otherwise, the fundamentals in the business remain intact here as we're managing inventory and sell-in, sell-through.

**David Regnery** (Executives):
And I'll also tell you that our team is executing at a very high level in that business, too.

**Operator** (Operator):
Your next question comes from the line of Varun Govindaraj with Bernstein.

**Varun Govindaraj** (Analysts):
So just picking up on the point of reference design, someone brought up earlier. Trane puts out a lot of these. What role does that play in the commercial process? Is it more of a tool showcasing expertise? Or have you found it almost necessary to engage with some kind of customers?

**David Regnery** (Executives):
I would tell you that we get called to sit around a lot of tables to help whether it be hyperscalers or other influencers to think through how we can make the thermal management system more efficient. And we have a team that led by our Chief Technology Officer and his team of experts that are really, really good at it. And that's why we get called to a lot of different tables to help design what the future is going to look like. 
There's -- in the data center world, and you're going to hear a lot more about this, there's trade-offs that need to be considered, right? It used to be all about PUE, and that's still obviously very, very important. But there's other trade-offs that need to be considered that we're really good thinking through because we like to think of everything at a system level. I mean that's kind of like our DNA and kind of like what we do in all of our core verticals. We've just taken that thought process to the data center vertical. And I think if you talk to some of the hyperscalers or some of the chip manufacturers, they'd say it's a refreshing view and how we look at what's possible for the future. So I expect more reference designs, not less in the future, and it's really just, again, speaks to the innovation that Trane Technologies can bring to the table.

**Varun Govindaraj** (Analysts):
Absolutely. I appreciate the color. And then just as a quick follow-up. Outside of chillers, CDUs and then modular via Stellar, are there any other white spaces in the data center space that you're looking at and thinking of expanding into?

**David Regnery** (Executives):
Yes. I mean, obviously, I won't go into the M&A pipeline, but as a major HVACR player on a global basis, we're going to see lots of opportunities. I would just tell you that we're going to be disciplined, and we like our portfolio that we have today. We certainly like our service capability that we have today. And -- but we'll also be opportunistic as opportunities present themselves to us.

**Operator** (Operator):
We have reached the end of the question-and-answer session. This concludes today's call. As always, Pat and Kirsten with Investor Relations are available for any questions. Thank you for joining. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TT_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO Chris Kuehn｜guidance：全年調升：調整後 EPS 區間 $15.20–$15.30（有機營收約 9% 於同段）（原話："our adjusted EPS guidance to a range of $15.20 to $15.30."）
- 2026-07-30｜CFO Chris Kuehn｜guidance：Q3 指引：有機營收約 +10%、調整後 EPS 約 $4.70（原話："with adjusted EPS of approximately $4.70."）
- 2026-07-30｜CFO Chris Kuehn｜guidance：Q3 利潤率預期擴張約 50 bp 等級（原話："We would expect margin expansion in the third quarter."）
- 2026-07-30｜CFO Chris Kuehn｜guidance：Q4 目標利潤率擴張超過 1 個百分點（原話："we'd be targeting over 1 point"）
- 2026-07-30｜CFO Chris Kuehn｜margin：報告槓桿與有機槓桿之間約 700 bp 差距，來自併購與第一年投資（原話："about a 700 basis point delta between reported leverage"）
- 2026-07-30｜CFO Chris Kuehn｜margin：價格對比通膨在 Q2 為逆風，下半年仍略為逆風（原話："a bit of a headwind in the second half of the year as well."）
- 2026-07-30｜CEO Dave Regnery｜margin：CEO 稱不介意單季或單半年的槓桿（原話："concerned about leverage in any quarter or really in any"）
- 2026-07-30｜CEO Dave Regnery｜commitment：長期槓桿目標 25% 以上，Q2 低於該水準（原話："our target is 25% plus. We may have a quarter like the"）
- 2026-07-30｜CFO Chris Kuehn｜margin：EMEA 因中東衝突採取成本行動，預期下半年減損落在毛利率之內（原話："we do expect deleverage to be within gross margins"）
- 2026-07-30｜CFO Chris Kuehn｜risk：EMEA 中東營收 Q2 下滑約 30%，下半年指引同樣假設下滑約 30%（原話："we're anticipating to be down about 30%."）
- 2026-07-30｜CFO Chris Kuehn｜risk：6 月底採取成本行動（調整人員與基礎設施）（原話："we did take some cost actions at the end of June."）
- 2026-07-30｜CEO Dave Regnery｜customer：Q2 企業有機訂單 +37%，積壓訂單創高 $12.1 billion、年增 70%（原話："record backlog of $12.1 billion, up 70% year-over-year."）
- 2026-07-30｜CEO Dave Regnery｜customer：約 $6 billion 積壓訂單排在 2027 年及之後（原話："approximately $6 billion slated for 2027 and beyond."）
- 2026-07-30｜CEO Dave Regnery｜customer：Applied 訂單 +130%（原話："Applied bookings were up 130%"）
- 2026-07-30｜CEO Dave Regnery｜customer：14 個垂直領域中，年初至今 11 個訂單成長（原話："growth in 11 of 14 verticals from an order standpoint."）
- 2026-07-30｜COO Donny Simmons｜customer：Q2 有 4 筆超過 1 億美元訂單，其一來自 Stellar（原話："we had 4 orders that were over $100 million"）
- 2026-07-30｜CEO Dave Regnery｜customer：超大規模客戶多有主採購協議或長期產能承諾（原話："master purchase agreement or a long-term capacity commitment"）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：預期長期部署 100% 的超額現金（原話："we expect to deploy 100% of excess cash over time."）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：2026 資本部署目標 $2.8–$3.3 billion（原話："deployment of $2.8 billion to $3.3 billion"）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：年初至今買回約 $840 million 股票（原話："repurchased approximately $840 million of shares"）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：現行買回授權剩餘 $3.8 billion（原話："$3.8 billion remaining on our current share repurchase"）
- 2026-07-30｜CFO Chris Kuehn｜capital_allocation：2026 CapEx 預期為營收的 2%–3%（原話："expected CapEx of 2% to 3% of revenue in 2026."）
- 2026-07-30｜CFO Chris Kuehn｜commitment：管理層表示不拒單、產能不落後（原話："we're not turning away any orders"）
- 2026-07-30｜CEO Dave Regnery｜commitment：Applied 產能過去三年擴充 4 倍，仍在擴充（原話："applied capacity 4x over the last 3 years."）
- 2026-07-30｜CEO Dave Regnery｜risk：供應鏈限制比平常多一些但可管理（原話："we are asking more from our supply partners."）
- 2026-07-30｜CFO Chris Kuehn｜risk：指引已假設部分專案延遲（leakage/breakage）（原話："assume some level of leakage, breakage in the guide, right?"）
- 2026-07-30｜CFO Chris Kuehn｜risk：資料中心專案可能位移（原話："So could there be some things that shift?"）
- 2026-07-30｜CEO Dave Regnery｜product：資料中心冷卻創新快，稱冰水機組變得更聰明（原話："think of chillers as getting smarter."）
- 2026-07-30｜COO Donny Simmons｜competition：市場整體朝風冷傾向（原話："the overall market has trended more towards air"）
- 2026-07-30｜CEO Dave Regnery｜product：LiquidStack 併購優於預期（原話："The LiquidStack acquisition is exceeding our expectations"）
- 2026-07-30｜CEO Dave Regnery｜product：不做冷板（cold plates）（原話："we don't have cold plates."）
- 2026-07-30｜CEO Dave Regnery｜product：電池儲能租賃等仍屬早期（原話："So we're still early days."）
- 2026-07-30｜CEO Dave Regnery｜guidance：Stellar 納入指引的 EPS 為持平，前一季說法為略有加分（原話："being flat for the year from an EPS standpoint."）
- 2026-07-30｜COO Donny Simmons｜guidance：Stellar 2026 營收仍預期 $500 million（原話："we expect the Stellar business to be $500 million in"）
- 2026-07-30｜CEO Dave Regnery｜customer：住宅今年預期中個位數成長，年初預期可能下滑、Q1 末修正為持平（原話："a mid-single-digit growth number for us in 2026"）
- 2026-07-30｜CEO Dave Regnery｜customer：住宅聚焦替換市場而非新建（原話："heavily focused on the replacement, not on new construction"）
- 2026-07-30｜CFO Chris Kuehn｜customer：年初至今住宅 sell-in 約等於 sell-through（原話："sell-in is really approximately equal to sell-through."）
- 2026-07-30｜CEO Dave Regnery｜customer：Americas 運輸市場預期 2026 下半年改善，內部假設復甦斜率較 ACT 平緩（原話："assumes a more gradual slope of recovery."）
- 2026-07-30｜CEO Dave Regnery｜customer：Thermo King 預期下半年轉為成長引擎（原話："Thermo King is going to be transitioning into more of a"）
- 2026-07-30｜CEO Dave Regnery｜customer：亞洲除中國外成長，加碼通路投資（原話："we're also doubling down on some of our investments"）
- 2026-07-30｜CFO Chris Kuehn｜customer：中東占企業營收不到 3%（原話："the Middle East is less than 3% of our total enterprise"）
- 2026-07-30｜CFO Chris Kuehn｜commitment：2027 出口率：管理層說再多幾季才會校準 2027（原話："let's get a few more quarters in before we dial in 2027"）

### 問答異常語氣（迴避／改口／保留）
- TT_Q2_2026_Earnings_Call_20260730.md｜問：Mehrotra：下半年成長出口率是否為 2027 起點、供應鏈能否跟上｜答法：CFO 未給 2027 數字，表示再多幾季才校準 2027
- TT_Q2_2026_Earnings_Call_20260730.md｜問：Mehrotra：是否已到訂單高峰｜答法：CEO 改談過去訂單規模與管線強勁，未直接回答是否高峰
- TT_Q2_2026_Earnings_Call_20260730.md｜問：Ritchie：CDU 業務占積壓比重與趨勢｜答法：CEO 表示不會講到那個細節，僅稱業績與管線良好
- TT_Q2_2026_Earnings_Call_20260730.md｜問：Hammond：Stellar 營收節奏｜答法：管理層重申營收 $500M 未變，EPS 假設由前一季的略有加分改為持平

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
{"date":"20260731","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"核心商用 HVAC 的訂單洪流是廣泛的、不是單一垂直市場的——因此其可持續性高於「資料中心敘事」所隱含者"},{"id":"H2","text":"定價權與資本效率同時維持：產品組合升級（applied／高效／控制／液冷）持續推升毛利率與 ROIC，且投資前置只是階段性壓抑增量槓桿"},{"id":"H3","text":"紀錄 backlog 提供的是「一年半」能見度，不是「多年」——但足以讓 FY26-27 營收預測的變異數低於同業"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Hyperscaler 資本支出於 2027 進入消化期，同時商用建築與貨運週期下行。"},{"id":"R2","text":"HVAC 價格操縱民事集體訴訟（Carrier／Trane／Rheem 等，2026 年 3-5 月 5 案合併於密西根聯邦法院；控以疫情／法規變動為掩護協調漲價；TT 否認，未經法院認定，無 DOJ 刑事立案證據）。"},{"id":"R3","text":"資料中心 bolt-on 整合失敗與出價紀律惡化。"},{"id":"R4","text":"資料中心熱管理的美元往晶片端位移：TT 明言不做冷板、依賴夥伴；浸沒式「還有一段距離、有些挑戰」。"},{"id":"R5","text":"宏觀成本／法規外生變數（關稅、A2L 冷媒轉換、Pillar Two 全球最低稅負）。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已持有續抱＋首階加碼 1/3；再加碼＝$415 以下，或 FY26 有機增量槓桿回到 25%＋","irr_base_pct":9.0,"ev5y_pct":49.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.2,"ev5y_pct":49.0,"irr_base_pct":9.0,"max_dd_pct":-48.0,"bull_5y_price":910.0,"bear_5y_price":285.0,"p_bull_pct":27.0,"p_bear_pct":25.0,"rearm_trigger":"已持有續抱＋首階加碼 1/3；再加碼＝$415 以下，或 FY26 有機增量槓桿回到 25%＋","price_at_dd":440.28,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TT_20261102/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
