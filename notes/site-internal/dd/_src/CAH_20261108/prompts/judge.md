你是 stock-analyst **v20 判斷 agent**，標的 CAH（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"CAH","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":67513,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook"},"note":"未取得（新聞稿未列共識，未另查證）"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益","value":1001,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook"},"note":"未取得（新聞稿未列共識，未另查證）"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益","value":753,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook"},"note":"未取得（新聞稿未列共識，未另查證）"},{"id":"f_kpi6_fy2027_non_gaap_eps","label":"FY2027 non-GAAP EPS 指引","value":"12.8～13.0","period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook"},"note":"共識 FY1 EPS 12.56（財報前快照 2026-11-07 xlsx，指引下緣已高於共識；來源 dd_numbers_extra.py consensus_revision）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_cah_gross_margin_pct","label":"CAH 毛利率","value":3.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cah_operating_margin_pct","label":"CAH 營業利益率","value":1.26,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cah_fcf_margin_pct","label":"CAH FCF 利潤率","value":1.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mck_gross_margin_pct","label":"MCK 毛利率","value":3.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mck_operating_margin_pct","label":"MCK 營業利益率","value":1.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mck_fcf_margin_pct","label":"MCK FCF 利潤率","value":1.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cor_gross_margin_pct","label":"COR 毛利率","value":4.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cor_operating_margin_pct","label":"COR 營業利益率","value":1.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cor_fcf_margin_pct","label":"COR FCF 利潤率","value":0.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_gross_margin_pct","label":"HSIC 毛利率","value":31.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_operating_margin_pct","label":"HSIC 營業利益率","value":5.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_fcf_margin_pct","label":"HSIC FCF 利潤率","value":3.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_non_gaap_eps","label":"Non-GAAP 稀釋 EPS","value":3.26,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook"},"note":"未取得（新聞稿未列共識，未另查證）"},{"id":"f_kpi4_1_398_157","label":"自由現金流（營業現金流 1,398 − 資本支出 157，自算）","value":1241,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook"},"note":"未取得（新聞稿未列共識，未另查證）"},{"id":"f_kpi5_sbc_non_gaap","label":"SBC 占 non-GAAP 營業利益","value":10.9,"period":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q1 FY2027（季末 2026-09-30，公告於 2026-11-05）","citation":"公司 IR 新聞稿 https://newsroom.cardinalhealth.com/2026-11-05-Cardinal-Health-Reports-First-Quarter-Fiscal-Year-2027-Results-and-Raises-Outlook"},"note":"未取得（新聞稿未列共識，未另查證）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":271.72,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":48.62,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":73.89,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.56 → 12.56）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（14.06 → 14.06）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.61 → 15.61）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":12.56,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":14.06,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":15.61,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.48,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 12.5 → 12.56（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":35.15,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝15.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":15.4,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.24,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.26,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":21.63,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 12.56，分子＝快照價 271.72","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.756,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":3551.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 8815.0、現金 5264.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":231.14,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":66355.45,"period":"2026-11-08","unit":"USD m","basis":"市值 62804.45 ＋ 淨負債 3551.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":266074.5,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":282369.46,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.25,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 271.72 / W52 219.16 / W104 180.24 / W250 122.33 / W250 13週斜率 2.81%"},{"id":"f_ma_w52","label":"52 週均線","value":219.16,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":180.24,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":122.33,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.81,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"FY2026 10-K 列出主要對手：Pharma 為 McKesson、Cencora 等；GMPD 為 Medline、Owens & Minor 等；並稱新進入者、新商業模式與產業整併可能加劇競爭壓力、壓縮利潤，客戶整併可能導致從兩家既有供應商中只選一家而流失客戶。未揭露具體份額數字或具名新進入者。","source":"SEC EDGAR 10-K FY2026 Competition","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"Competitive pressures in each of our businesses may also be increased by new business models, new entrants, new regulations, or changes in enforcement priorities, changes in consumer demand, or general competitive dynamics. Our businesses face continued pricing pressure from these and other factors, which adversely affects our margins.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"最大客戶 CVS Health 占 FY2026 營收 28%，前五大客戶合計 43%（集中度高）。","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"Our largest customer, CVS Health, accounted for 28 percent of our fiscal 2026 revenue. In the aggregate, our five largest customers, including CVS Health, accounted for 43 percent of our fiscal 2026 revenue.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"+","claim":"2026-10-01 Cardinal 與 CVS 簽具約束力意向書，將配銷協議延長至 2032-06-30，服務範圍不變；尚未定案。搜尋未見 CVS 導入第二供應商或自製配銷的報導。","source":"Distribution Strategy: Cardinal Health Extends CVS Pharmaceutical Distribution Deal Through 2032","url":"https://distributionstrategy.com/2026/10/cardinal-health-extends-cvs-pharmaceutical-distribution-deal-through-2032/","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261108","affects":["moat_trend","thesis.R","triggers"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"CVS Health 為最大客戶，占 FY2026 營收 28%、期末應收帳款毛額 22%；前五大客戶合計占營收 43%；10-K 自述銷售與信用集中度顯著，若主要客戶減少採購、違約或不續約，營運與財務可能受不利影響。","source":"SEC EDGAR｜Cardinal Health 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"Our largest customer, CVS Health, accounted for 28 percent of our fiscal 2026 revenue. In the aggregate, our five largest customers, including CVS Health, accounted for 43 percent of our fiscal 2026 revenue.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"CVS 10-Q（截至 2026-09-30）：長期債信評等 Fitch BBB 展望負面、Moody's Baa3 展望 2026-08 由穩定升為正面、S&P BBB 展望 2026-05 由負面轉穩定，仍屬投資等級。","source":"SEC EDGAR｜CVS Health 10-Q 2026Q3","url":"https://www.sec.gov/Archives/edgar/data/0000064803/000006480326000108/cvs-20260930.htm","excerpt":"As of September 30, 2026, the Company’s long-term debt was rated “BBB” by Fitch Ratings, Inc. (“Fitch”), “Baa3” by Moody’s Ratings (“Moody’s”) and “BBB” by Standard & Poor’s Financial Services LLC (“S&P”), and its commercial paper program was rated “F2” by Fitch, “P-3” by Moody’s and “A-2”","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"FY27 指引：GMPD 營收成長 2%–4%、部門利潤 2.0–2.2 億美元；FY26 GMPD 營收 127 億美元、+1%，部門利潤含一次性 1 億美元關稅退款","source":"Cardinal Health Q4 FY26 Earnings Press Release","url":"https://s201.q4cdn.com/566741227/files/doc_financials/2026/q4/Q4-FY26-Earnings-Press-Release.pdf","excerpt":"Global Medical Products and Distribution segment: Revenue Segment profit 2% to 4% growth $200 million to $220 million Other (NPHS, at-Home Solutions, OptiFreight Logistics):","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"GLP-1 對 Pharma 營收成長貢獻 6 個百分點，但被 IRA WAC 調價 6 個百分點抵銷；10-Q 稱 GLP-1 未實質貢獻部門利潤、未來需求不可預測","source":"Cardinal Health 10-Q 季度截至 2026-03-31","url":"https://www.sec.gov/Archives/edgar/data/0000721371/000072137126000018/cah-20260331.htm","excerpt":"months ended March 31, 2026, we saw an increased demand for GLP-1 pharmaceuticals which positively impacted our Pharma segment and consolidated revenue for the three and nine months ended March 31, 2026; however, increased GLP-1 sales did not meaningfully contribute to segment profit. Future demand for these medications is unpredictable and our ability to meet demand may be impacted by supply","as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"DOJ 於 2023-11 發出 CID，調查 2022 年收購 GPO 與風濕科 MSO 少數股權交易是否違反反回扣法與 False Claims Act；公司配合調查，屬非反壟斷事項。","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"In November 2023, we received a Civil Investigative Demand (\"CID\") from the Department of Justice focused on potential violations of the Anti-Kickback Statute and False Claims Act in connection with a 2022 transaction in which we purchased a minority ownership interest in a rheumatology managed services organization and a group purchasing organization. We are cooperating with this investigation.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"公司在反壟斷集體訴訟中是原告／集體成員，FY2026 認列淨回收 2,400 萬美元（FY2025 為 1.71 億），非被告。","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"We recognized income for net recoveries in class action antitrust lawsuits in which we were a class member or plaintiff of $24 million, $171 million, and $117 million during fiscal 2026, 2025, and 2024, respectively.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"搜尋未見 2026 年針對 CAH 的新 DOJ／FTC 反壟斷調查或拆分報導；結果主要為 SEC 文件與舊案（2015–2018 FTC 放射藥房案）。","source":"WebSearch 彙整（SEC 文件、Mintz 2018 FTC 案）","url":null,"excerpt":null,"as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"自2025年2月起CAH已支付約2億美元IEEPA關稅，主要在GMPD部門；最高法院2026年2月裁定IEEPA關稅違法。","source":"SEC EDGAR 10-K FY2026 MD&A Tariffs","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"Since February 2025, we have paid approximately $200 million in IEEPA tariffs, related to products that we source, manufacture or distribute, primarily in our GMPD segment.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"FY26 Q4認列約2億美元IEEPA關稅退款應收款，並預期把相應部分退還客戶；淨營業利益影響約1億美元（Q4），全年不重大。","source":"SEC EDGAR 10-K FY2026 MD&A Tariffs","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"During the fourth quarter of fiscal 2026, we recorded a receivable of approximately $200 million in relation to the expected refund of IEEPA tariffs from the U.S. Government.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"GMPD持續承受Section 122/232/301及Smoot-Hawley 308關稅帶來的成本增加，調價未能完全抵銷。","source":"SEC EDGAR 10-K FY2026 MD&A Tariff Environment","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"our GMPD segment has experienced, and expects to continue to experience increased costs as a result of tariffs imposed or expected to be imposed under different legal authority, including Sections 122, 232 and 301 of the Trade Act of 1974 and Section 308 of the Smoot-Hawley Tariff Act.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026年4月總統公告對品牌藥及相關原料進口課關稅，Pharma部門可能受影響。","source":"SEC EDGAR 10-K FY2026 MD&A Tariff Environment","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"An April 2026 proclamation issued by the President of the United States imposed tariffs on imports of branded pharmaceutical products and associated ingredients imported into the United States.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"總統聲明學名藥2028年起課100%、2029年起課200%關稅，實施仍高度不確定，可能影響Pharma部門成本或供給。","source":"SEC EDGAR 10-K FY2026 MD&A Tariff Environment","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"the President recently issued a statement indicating that generic pharmaceutical products will be subject to 100% tariffs beginning in 2028 and 200% tariffs beginning in 2029.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K 揭露 2024 年 4 月 FDA 對 CAH 發警告信：向中國第三方製造商採購的塑膠針筒缺乏適當 510(k) 許可","source":"Cardinal Health Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000721371/000072137126000038/cah-20260630.htm","excerpt":"in April 2024, the FDA issued a warning letter to Cardinal Health asserting that plastic syringes sourced from a third party manufacturer in China did not have appropriate 510(k) clearance","as_of":"2026-08-15","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 警示：供應商不合規或生產地點轉移過去曾、未來可能導致營運實質修改","source":"Cardinal Health Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000721371/000072137126000038/cah-20260630.htm","excerpt":"Noncompliance or concerns over noncompliance, including by suppliers, as a result of use of third party manufactures, or planned shifts in production sites, has in the past, and may in the future result in substantial modifications to our business practices and operations.","as_of":"2026-08-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"CEO 稱約 10% 產品來自中國，並在分散供應商、擴大美國製造（如針筒）","source":"HME News: Cardinal Health juggles business supply demands in costlier environment","url":"https://www.hmenews.com/article/cardinal-health-juggles-business-supply-demands-in-costlier-environment","excerpt":null,"as_of":"2025-07-15","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 Pharmaceutical and Specialty Solutions 營收 +15% 至 $234.8B，來自既有與新客戶的品牌藥與特殊藥銷售成長；segment profit +23% 至 $2.8B","source":"Cardinal Health FY2026 Form 10-K","url":"https://www.sec.gov/Archives/edgar/data/0000721371/000072137126000038/cah-20260630.htm","excerpt":"Pharma segment revenue for fiscal 2026 increased 15 percent to $234.8 billion from the prior year, primarily due to branded and specialty pharmaceutical sales growth from existing and new customers","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"FY2026 GMPD 營收約持平（$12.7B，+1%）：自有品牌成長被配送量下滑與 IEEPA 關稅退款返還客戶抵銷；segment profit +91% 至 $258M","source":"Cardinal Health FY2026 Form 10-K（經搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000721371/000072137126000038/cah-20260630.htm","excerpt":null,"as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"FY2027 指引：Pharma 營收 +3~5%、segment profit +8~11%；GMPD 營收 +2~4%、segment profit $200~220M；non-GAAP EPS $12.40~12.60","source":"Cardinal Health Q4 FY26 Earnings Press Release","url":"https://s201.q4cdn.com/566741227/files/doc_financials/2026/q4/Q4-FY26-Earnings-Press-Release.pdf","excerpt":null,"as_of":"2026-08-11","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"FY2026 Q4 GLP-1 成長與 IRA WAC 調整各約 500bps 的反向營收影響；specialty 成長 FY2026 超過 25%","source":"MarketBeat Cardinal Health Q4 earnings call highlights（經搜尋摘要）","url":"https://www.marketbeat.com/instant-alerts/cardinal-health-q4-earnings-call-highlights-2026-08-11/","excerpt":null,"as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"管理層預期 FY2027 學名藥量回歸常態；品牌轉學名藥（LOE）對營收是下拉、對利潤為正；公司處於 McKesson、Cencora 三強高度集中且競爭激烈的配送業","source":"MarketBeat Q3 FY26 call highlights／10-K（經搜尋摘要）","url":"https://www.marketbeat.com/instant-alerts/cardinal-health-q3-earnings-call-highlights-2026-05-01/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"FY2026 10-K 揭露競爭壓力可能因新商業模式、新進入者等而加劇，並持續面臨定價壓力影響毛利；未點名具體替代技術。","source":"SEC EDGAR 10-K FY2026 全文","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"Competitive pressures in each of our businesses may also be increased by new business models, new entrants, new regulations, or changes in enforcement priorities, changes in consumer demand, or general competitive dynamics. Our businesses face continued pricing pressure from these and other factors, which adversely affects our margins.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"董事會風險監督委員會被授權監控 AI 等新興技術如何納入營運、服務與策略並討論相關風險。","source":"SEC EDGAR 10-K FY2026 全文","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"monitoring emerging technologies such as artificial intelligence, including how such technologies are, or may be, incorporated into our operations, services and strategies and discussing risks related to these emerging technologies.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"10-K 指出競爭壓力可能因新商業模式、新進入者、法規變動而加劇，產業整併與製造商直接配送給客戶亦構成競爭。","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"Competitive pressures in each of our businesses may also be increased by new business models, new entrants, new regulations, or changes in enforcement priorities, changes in consumer demand, or general competitive dynamics.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"CAH 2026-07 收購 AdaptHealth 糖尿病業務與 Strive Medical（約 3.6 億美元），擴張 at-Home 直接對患者郵購模式","source":"HLTH 2026-07 報導","url":"https://hlth.com/insights/news/cardinal-health-expands-home-care-business-with-two-strategic-acquisitions","excerpt":"Cardinal Health has agreed to acquire AdaptHealth’s Diabetes Health business and home medical supply provider Strive Medical in two transactions valued at approximately $360 million.","as_of":"2026-07-22","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-11-05 公布 FY27 Q1：non-GAAP EPS $3.26（+28%），並把 FY27 non-GAAP EPS guidance 由 $12.40–12.60 上調至 $12.80–13.00；PSS 利潤成長 guidance 上調至 10–12%。","source":"Cardinal Health 8-K / 新聞稿 (finviz/PR Newswire)","url":"https://finviz.com/news/416625/cardinal-health-reports-first-quarter-fiscal-year-2027-results-and-raises-outlook","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 FY27 EPS $3.26 對比 Q1 前共識約 $2.92–2.94，beat 約 11%。","source":"247wallst: Cardinal Health Q1 2027 EPS beats by 11%","url":"https://247wallst.com/cards/cardinal-health-q1-2027-earnings-cah-01m6nrkc2mw730rat7vnk151yj","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"8 月財報前，FY27（至 2027-06）EPS 共識約 $12.04–12.05，低於當時 guidance 下限 $12.40；之後有來源稱共識已升至 $12.57（日期未確認）。尚未找到 11-05 後的新共識。","source":"stockanalysis.com / Barchart 預覽（經搜尋彙整）","url":"https://stockanalysis.com/stocks/CAH/","excerpt":null,"as_of":"2026-08-11","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價：Tickflow（2026-08-01）14 位分析師共識 Buy，平均目標價 $253.38，最高 $275（Leerink）；MarketBeat（2026-05）平均 $241.80，JPMorgan 5 月降至 $215（Neutral）。Q4 後 Mizuho 升至 $250、Evercore ISI $270。11-05 後的新目標價未找到。","source":"Tickflow CAH forecast; MarketBeat","url":"https://www.tickflow.io/stock/CAH/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 FY27 guidance 上調至 $12.80–13.00","source":"SEC 8-K Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/0000721371/000072137126000042/a27q1_x093026xex991xnewsre.htm","excerpt":"Cardinal Health is raising its fiscal year 2027 guidance for non-GAAP diluted EPS to $12.80 to $13.00, from the previous range of $12.40 to $12.60. The updated guidance reflects +17% to +19% growth3 compared to its FY26 ex-tariff refund baseline and +14% to +15% growth from reported FY26 results.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"IVC 濾器產品責任訴訟持續：2023-04 和解約 4,375 件 $2.75 億，其餘案件續辯；2026-06-30 應計 $2,900 萬","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"At June 30, 2026, we have a total of $29 million accrued for losses and legal defense costs, included in the qualified settlement fund, related to the IVC filter product liability lawsuits in our consolidated balance sheets.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 10 份 8-K 中僅 1 份含重大項目（2026-08-11 Item 1.01/1.02 信貸協議，$40 億循環信貸至 2031 取代舊信貸與應收帳款出售機制）；無 4.02 重編","source":"SEC EDGAR 8-K 清單／8-K 2026-08-11","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000036/cah-20260807.htm","excerpt":"The Credit Agreement, among other things, allows the Company access to $4.0 billion of revolving credit through August 7, 2031 (the “Termination Date”).","as_of":"2026-08-11","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Specialty Alliance 於 2025-08 宣布以約 $19 億現金收購 Solaris Health（約 75% 股權），預計 2025 年底前完成；搜尋結果未確認是否已完成","source":"RTTNews／Benzinga 搜尋結果","url":"https://www.rttnews.com/3564989/cardinal-health-s-specialty-alliance-to-buy-solaris-health-cah-down-over-8-in-pre-market.aspx","excerpt":null,"as_of":"2025-08-12","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"Webcol 大型酒精棉片因微生物污染自願召回（FDA 公告 2026-03-20）","source":"pulse.bot 轉載 Cardinal Health 公告","url":"https://www.pulse.bot/healthcare/news/cardinal-health-issues-voluntary-nationwide-recall-of-webcol-large-alcohol-prep-pad-b18fc035-ac9f-4a09-a1eb-58b6c1f6cf2e","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"據單一來源，2026-07 Cardinal 收購 Strive Medical 與 Adapt Health 糖尿病業務，合計約 $3.6 億","source":"medindexer","url":"https://medindexer.com/news/cardinal-health-makes-acquisition-duo-worth-360m-for-home-care-business-advance","excerpt":"Cardinal Health makes acquisition duo worth $360m for home care business advance Cardinal Health acquired Strive Medical and Adapt Health's diabetes unit in two deals totaling $360 million to expand its home care business.","as_of":"2026-07-21","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Solaris Health 約 $19 億收購（2025-08 宣布）","source":"RTTNews","url":"https://www.rttnews.com/3564989/cardinal-health-s-specialty-alliance-to-buy-solaris-health-cah-down-over-8-in-pre-market.aspx","excerpt":null,"as_of":"2025-08-12","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"IVC 產品責任訴訟持續；搜尋未見2026新證券集體訴訟（Cordis 案 $1.09 億已於2023-09 final approval）","source":"SEC EDGAR 10-K FY2026","url":"https://www.sec.gov/Archives/edgar/data/721371/000072137126000038/cah-20260630.htm","excerpt":"At June 30, 2026, we have a total of $29 million accrued for losses and legal defense costs, included in the qualified settlement fund, related to the IVC filter product liability lawsuits in our consolidated balance sheets.","as_of":"2026-08-11","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"Webcol 酒精棉片微生物污染召回（2026-03-20）","source":"pulse.bot","url":"https://www.pulse.bot/healthcare/news/cardinal-health-issues-voluntary-nationwide-recall-of-webcol-large-alcohol-prep-pad-b18fc035-ac9f-4a09-a1eb-58b6c1f6cf2e","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02（重編）；搜尋僅見2003–2008舊案","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000721371&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"CAH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":3.9,"operating_margin_pct":1.26,"fcf_margin_pct":1.9,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"MCK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":3.67,"operating_margin_pct":1.67,"fcf_margin_pct":1.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":4.12,"operating_margin_pct":1.44,"fcf_margin_pct":0.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HSIC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.59,"operating_margin_pct":5.79,"fcf_margin_pct":3.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"CAH"},"financial_history":{"ticker":"CAH","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":204979000000.0,"revenue_yoy_pct":null,"gross_margin_pct":3.35,"operating_margin_pct":0.87,"net_income":330000000.0,"diluted_eps":1.0,"free_cash_flow":2363000000.0,"fcf_margin_pct":1.15,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":226827000000.0,"revenue_yoy_pct":10.66,"gross_margin_pct":3.27,"operating_margin_pct":0.94,"net_income":852000000.0,"diluted_eps":3.45,"free_cash_flow":3251000000.0,"fcf_margin_pct":1.43,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":222578000000.0,"revenue_yoy_pct":-1.87,"gross_margin_pct":3.67,"operating_margin_pct":1.04,"net_income":1561000000.0,"diluted_eps":6.45,"free_cash_flow":1850000000.0,"fcf_margin_pct":0.83,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":254248000000.0,"revenue_yoy_pct":14.23,"gross_margin_pct":3.84,"operating_margin_pct":1.25,"net_income":1714000000.0,"diluted_eps":7.23,"free_cash_flow":4525000000.0,"fcf_margin_pct":1.78,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CAH/CAH_Q1_2027_Earnings_Call_20261105.md）

# Q1 2027 Earnings Call
**Cardinal Health, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to Cardinal Health, Inc. First Quarter Fiscal Year 2027 Earnings Release. [Operator Instructions] 
I will now hand the conference over to David Frost, Vice President, Investor Relations. David, please go ahead.

**David Frost** (Executives):
Good morning. Welcome to Cardinal Health's First Quarter Fiscal 2027 Earnings Conference Call, and thank you for joining us. With me today are Cardinal Health's CEO, Jason Hollar; and our CFO, Aaron Alt. You can find this morning's earnings press release and investor presentation on the Investor Relations section of our website at ir.cardinalhealth.com.
Since we will be making forward-looking statements today, let me remind you that the matters addressed in these statements are subject to risks and uncertainties that could cause our actual results to differ materially from those projected or implied. Please refer to our SEC filings and the forward-looking statement slide at the beginning of our presentation for a description of these risks and uncertainties. 
Please note that during our discussion today, the comments will be on a non-GAAP basis unless specifically called out as GAAP. GAAP to non-GAAP reconciliations for all relevant periods can be found in the supporting schedules attached to our press release. For the Q&A portion of today's call, we kindly ask that you limit questions to one per participant so that we can try and give everyone an opportunity. 
With that, I will now turn the call over to Jason.

**Jason Hollar** (Executives):
Good morning, and thank you for joining us. I am pleased to report a strong start to fiscal '27 with broad-based growth once again across the enterprise. This quarter's results reflect disciplined execution and continued progress against our strategic priorities. We are strengthening our core while investing in the capabilities that will drive growth and long-term value creation. 
As election results have come into focus, our priorities remain consistent. We have a long-standing record of constructive engagement with policymakers on both sides of the aisle. Our focus on better access, lower cost and continued innovation aligns with objectives shared across the political spectrum. Any policy changes will take time, and we would expect to be manageable as we continue to be active in our engagement with government. Our essential role across the health care ecosystem positions us to contribute meaningfully to those conversations. And in the meantime, our teams remain focused on delivering for customers and patients every day. 
Performance demonstrates the value of Cardinal Health's scale, reach and capabilities across the health care ecosystem. Recently, we announced the renewal of our largest customer, CVS Health, through June 2032. This reflects our long-standing relationship, which predates CVS Health's acquisition of Aetna. The renewal reinforces the strategic value and stability that the partnership with Cardinal Health brings to CVS' retail pharmacy network, something that will continue beyond the spin-off in 2028.
Just as importantly, when combined with our other recent significant renewals, it provides a steady foundation for continued investment in the business and supports the sustained execution of our growth strategies. In Global Medical Products and Distribution, performance was stable, notwithstanding global volatility as the team continued to execute the improvement plan, including actions to optimize the network, improve efficiency and grow Cardinal Health brand. We remain encouraged by our progress while recognizing there's more opportunity ahead to continue to optimize this segment. 
Our Other growth businesses also delivered positive results, supported by healthy demand from underlying secular trends, the investments we've made to build differentiated positions and a firm focus on integrating the acquisitions in at-Home. Taken together, the quarter's performance and our visibility into the balance of the year give us confidence to raise our fiscal '27 outlook, which Aaron will walk through in more detail.
With that, I'll turn the call over to Aaron.

**Aaron Alt** (Executives):
Good morning. The Cardinal Health team delivered a strong first quarter, above and below the line on the income statement and with respect to cash flow. Our performance was characterized by strong demand across the enterprise, led by our Pharmaceutical and Specialty Solutions segment and our Other operating businesses. Demand was matched by good operational execution by all of our teams. Given our Q1 delivery, we are pleased to raise our fiscal 2027 EPS guidance to $12.80 to $13 from the previous range of $12.40 to $12.60. 
Moving on to our consolidated first quarter results. Total company revenue grew 5% to $67.5 billion. Consolidated gross profit increased 12% to $2.6 billion. We saw continued strength in our core distribution operations, expanded contributions from our investments in Specialty and gross profit increases from our 3 growth businesses in Other. Consolidated SG&A grew more slowly, increasing 9% to $1.6 billion. In addition to servicing growing sales, we continue to invest in capabilities for our businesses while also remaining focused on simplification and cost optimization. 
As gross profit grew faster than SG&A, our operating income grew 17% to $1 billion, achieving that milestone in the quarter for the first time and highlighting the operating leverage we are pursuing. Moving below the operating line, interest and other was $67 million, and our effective tax rate for the first quarter was 18.5%. We are pleased with our progress and continue to focus on building durable improvements to items below the line. After completing a $500 million accelerated share repurchase program during the quarter, our diluted weighted average shares outstanding for the quarter were approximately 233 million shares. All in, our efforts resulted in first quarter diluted earnings per share growth of 28% or $3.26. 
Let's turn to the specific segment results, beginning with Pharma. Segment revenue increased 6% to $62.6 billion, driven by growing brand and specialty sales from existing customers. Specialty grew at an 18% clip during the quarter. While the business put up 6% revenue growth in the quarter, we again observed offsetting top line revenue growth dynamics. GLP-1 medications, which continued to grow on pace, drove approximately 500 basis points of revenue growth in the quarter. That was offset in large part by the impact of IRA WAC reductions, which drove a 400 basis point revenue headwind year-over-year. 
Segment profit in Pharma increased 17% to $783 million. This robust performance reflects healthy contributions from Brand, Specialty and our generics program, where we continue to observe consistent market dynamics. The core distribution business remains highly resilient and our strategic sourcing initiatives, notably our Red Oak Sourcing partnership, continue to drive significant value. Pharma segment profit also reflected the contribution of our Solaris acquisition, which we will lap in the second quarter. MSOs are a part of our broader specialty strategy, and we remain focused on integration and building the capabilities needed for long-term growth. 
Now moving to our Global Medical Products and Distribution segment. Segment revenue was roughly flat to prior year at $3.2 billion. This top line result was driven by growth in Cardinal Health Brand, offset by lower distribution revenue during the period. Segment profit for GMPD was higher than expected at $33 million for the quarter. We saw a steady improvement in underlying operational performance as our team continued to execute against our GMPD improvement plan. We continue to see healthy demand for our Cardinal Health Brand products with U.S. growth in the low to middle single digits for the quarter. Foreign exchange and distribution were headwinds, while on the cost side, modest commodity pressure, primarily in transportation costs, was offset by tariff tailwinds.
Now let's turn to Other, which encompasses our 3 growth businesses. As we have remarked in the past, these businesses operate in markets aligned with powerful secular trends, including the aging population, the shift to home-based care and complex medical innovation and our results continue to reflect these favorable trends. Revenue for Other grew 7% to $1.8 billion and profit increased 16% to $193 million. With profit growing well above our long-term targets and at more than twice the rate of revenue, our results in Q1 demonstrate our smart growth strategy in action. All 3 businesses in Other delivered revenue and profit growth as we continue to invest in each business' distinct priorities.
Turning to cash on the balance sheet. We ended the first quarter with $5.3 billion of cash after generating $1.6 billion of adjusted free cash flow. We took several actions aligned to our capital allocation framework, including investing $157 million of capital into our business, executing the $500 million share repurchase program I referenced earlier and returning approximately $125 million to shareholders through dividends. We finished the quarter near the midpoint of our targeted leverage range and preserved our strong investment-grade ratings. 
So let's talk about our fiscal 2027 guidance. We are raising our non-GAAP diluted EPS guidance to a new range of $12.80 to $13, up from our prior range of $12.40 to $12.60. This updated guidance represents 17% to 19% growth off our ex-tariff refund adjusted fiscal '26 EPS of $10.95 and 14% to 15% growth off our reported fiscal '26 EPS of $11.26. This raise reflects the broad-based operating momentum we see across the business and our confidence in continuing to deliver robust profit growth across our operating segments. For the Pharma segment, while we continue to expect revenue growth of 3% to 5%, consistent with our original guidance, we have increased our segment profit growth guidance to a range of 10% to 12% from the prior guidance of 8% to 11%. 
For those wondering about our recent renewals, our original profit guidance for fiscal '27 largely anticipated the financial impact of the CVS renewal. Recall that we provided guidance on the basis of a consistent book of business. Our updated guidance also assumes continued strong demand and performance across our core distribution, generic sourcing and Specialty business. For modeling purposes, following strong growth in the first quarter, we expect earnings growth to moderate in the second and third quarters before strengthening in the fourth quarter to a level modestly below Q1. This is largely a result of the timing of the year-over-year impact of customer renewals and lapping the Solaris acquisition. 
For the Global Medical Products and Distribution segment, we continue to expect revenue growth of 2% to 4%. While we are not changing our financial guidance for GMPD for the year, we do note that sustained high petroleum costs driven by the ongoing Iran conflict are pushing GMPD segment profit toward the low end of our guidance range of $200 million to $220 million. We remain highly focused on driving long-term profitability through our operational improvement plan in GMPD and expect the segment's results to be weighted towards the back half of the fiscal year, consistent with historical trends. For modeling purposes, we expect the second quarter to be generally consistent with the Q1 result with sequential quarterly growth for the remainder of the year thereafter. 
For Other, we anticipate revenue growth of 12% to 14%, up from our previous range of 11% to 13%, driven by strong demand across all 3 operating businesses. We are raising our profit guidance to 17% to 20% growth, up from our prior range of 15% to 18% growth. This reflects the favorable performance and underlying demand we are capturing. We still expect revenue and profit growth to accelerate in the second half of the fiscal year, consistent with our previous guidance. 
Moving below the operating line, we continue to expect interest and other to be between $240 million and $290 million. We expect our effective tax rate to be in the range of 18.5% to 19.5%, down from our previous guidance of 19% to 20% and reflective of the efforts our teams have made in identifying and executing durable improvements. Regarding capital deployment, our anticipated capital expenditure of approximately $700 million remains unchanged. We are actively investing in supply chain modernization, automation, technology and AI infrastructure to drive future productivity. We expect diluted weighted average shares outstanding to be in the range of 231 million to 232 million shares, reflecting the timing of our recently completed $500 million share repurchase program. 
Finally, we continue to expect adjusted free cash flow to be between $3.5 billion and $4 billion. This robust free cash flow generation provides us with the necessary flexibility to fund organic growth, return capital to our shareholders and pursue accretive targeted M&A. To conclude, we have delivered an excellent start to fiscal 2027. We are doing what we said we would do, and we are operating with clear strategic and financial priorities, strengthening our core Distribution business, expanding our footprint in Specialty and accelerating our Other growth businesses. By ruthlessly prioritizing operational excellence and maintaining disciplined capital allocation, we continue to be well positioned for growth and long-term value creation in fiscal 2027 and beyond. 
With that, I will turn it back over to Jason.

**Jason Hollar** (Executives):
Thanks, Aaron. Beyond the strong quarter, our results continue to reinforce the durability of our business and the important role we play across health care. The consistency of our execution and the strength of our customer relationships position us well as we look ahead. Over the last 12 months, we have renewed contracts representing nearly 2/3 of our enterprise revenue, the majority of which is long-term in length, demonstrating that the value we deliver to customers resonates in the marketplace and provides a stable foundation for continued investment in our business. 
The commercial success spans the enterprise, including renewing our 2 largest customers in Pharma and our 2 largest customers in GMPD. During this time frame, we've also secured meaningful new business across the other growth businesses. These milestones reflect the consistent service and execution our customers expect from us. And with that backdrop, I want to highlight the progress we're making against several of our strategic priorities. Beginning with our largest, most significant segment, Pharma, once again served as the key contributor to our growth, demonstrating the underlying strength of the business and the effectiveness of the strategic investments we have made. 
The core distribution business remains durable, and we continue to scale the capabilities that extend our value with providers and biopharma partners. The long-term renewal with CVS Health adds to the proof points of our commercial success following the announced Kroger renewal and our significant new business wins in fiscal '25, including several prominent health systems. The combination has strengthened our core and increased the visibility into the future of the business. This strong position allows us to invest strategically, maintain or improve the high service levels our customers rely on and advance key growth priorities. 
We also continue to align closely with our manufacturer partners on the evolving pharmaceutical landscape, a collaborative focus highlighted at our recent Business Partners Conference, which convened nearly 500 supplier partners. The breadth of participation reinforces the strategic value of these relationships and our position as the trusted partner across the supply chain. Our specialty strategy is focused on building connected platforms that help community-based physicians operate more effectively while creating opportunities across data, research and ancillary services. 
The integration of Solaris and our MSO strategy continued to progress during the quarter as we identify synergies between our platforms to strengthen the group with the best of each of the parts. We are heads down approaching this work with discipline and an emphasis on realizing the benefits of greater scale while maintaining a high-quality experience for physicians and patients. We are also seeing the value of the network beyond practice support. The launch of the INSIGHT-IBD study with Eli Lilly is one example of how our MSO provider relationships, combined with Specialty Networks' real-world data and research capabilities, can generate actionable insights for industry partners and support innovation and patient care. 
In BioPharma Solutions, to keep pace with the growing demand, we are expanding 3PL and cold chain capacity through our new St. Louis facility, which we anticipate will start operating by the end of calendar year '27, increasing the breadth and scale of the services we provide. We also continue to see success in the cell and gene market where our 3PL business secured another new exclusive commercialization agreement this quarter to build upon the 2 new agreements we announced last quarter. 
Further, our Sonexus Patient Hub also continued to grow organically, and we remain on track to meet our prior target of doubling the number of therapies supported by fiscal '28, supporting our objective to deepen relationships with biopharma customers across the product life cycle. In our Global Medical Products and Distribution segment, we continue to execute against our improvement plan, growing Cardinal Health Brand and simplifying our operations. As part of this strategy, we recently deployed more than 100 Locus autonomous robots at our Dixon, California, distribution center, building on the progress we have made over the past couple of years, implementing this AI-enabled technology, which is now in a dozen of our distribution centers. 
This is a tangible example of how we are using technology to simultaneously improve both efficiency and resiliency. In Cardinal Health Brand, our Specialty portfolio, which includes our more clinically differentiated products, grew above market and contributed to overall Cardinal Health Brand growth in the quarter. Across our Other growth businesses, strong industry secular growth trends, combined with disciplined investment and execution, are translating into excellent financial outcomes. In at-Home Solutions, we delivered positive results and remain well positioned for continued growth as demand for home-based care expands. 
We have successfully migrated all employees and volume from our recent acquisition of Strive Medical into our nationwide network, further strengthening the platform and reinforcing our strategy to build a scaled national leader in at-home care. In addition, we began construction on our new Sacramento distribution center to support long-term capacity, efficiency and customer service. These initiatives, together with the continued deployment of AI-enabled automation within distribution centers across the network, are critical elements for our focus on core operations. 
Nuclear and Precision Health Solutions delivered solid results with continued growth in the core business and strong momentum in PET and Theranostics. We remain well positioned to serve the growing pipeline of complex radiopharmaceutical therapies coming to market, including areas like neuroendocrine tumor therapies that we will dispense and distribute. We also continue to invest across our network to drive growth and efficiency, including the rollout of our AI-driven route optimization tool, which is now live in 20 sites and expected to reach all of our 130 radiopharmacies by the end of fiscal '27. 
These investments ensure we continue to be an indispensable part of this cutting-edge area of medicine, building on our unmatched geographic reach and service capabilities. Within OptiFreight Logistics, we remain focused on expanding the ways we support our customers, reinforcing and growing our leading value proposition. With the launch of our new pharmacy solution in fiscal '26, we are now able to provide better tracking visibility and shipping efficiencies to the over 2 dozen pharmacies currently utilizing the technology. 
The continued improvement and broadening of this suite of services expands our role in managing our customers' shipping and receiving operations, delivering cost savings for them while also strengthening their resiliency. In addition to meeting a customer need, it also helps prevent disruptions that can ultimately affect patient care. As we look to the balance of the year, we are confident in our outlook, supported by the long-term customer agreements we have secured, the progress we're making across the enterprise and our disciplined execution. With a broad and diverse portfolio and our role as the backbone of health care, we are well positioned to navigate the industry's dynamic environment while advancing our priorities around access, affordability and innovation. Our strategy remains clear: strengthen the core, scale Specialty in our growth businesses, improve GMPD and deploy capital with discipline.
With that, we will take your questions.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Erin Wright with Morgan Stanley.

**Erin Wilson Wright** (Analysts):
Could you unpack the momentum a little bit more on the Pharma Distribution segment? Just more specifically also on the quarterly cadence, you gave the detail on renewals and Solaris, which is helpful. But just on an underlying basis, excluding some of those factors, are there any changes that you're seeing in underlying demand trends, generics or otherwise, that are evolving maybe better than expected on an underlying basis?

**Aaron Alt** (Executives):
Thanks for the question. We were really pleased to report the strong Q1 results for the Pharma business, really demonstrating the continued momentum that, that business has. As we called out in the prepared remarks, it was really driven by the strong unit demand across key product categories, certainly specialty, certainly generics and indeed, from our largest customers. The specialty part of our business continues to be quite strong. We saw high teens growth in the quarter, as we called out, certainly a bit above our double-digit expectations that we called from our original guide. 
And importantly, that strength was coming from some key priority areas, particularly urology and oncology, areas of emphasis for us across the broader portfolio. Also pleased with the positive performance in generics. We saw the strong volume growth, which is a touch above our long-term targeted levels, consistent market dynamics and very -- driven really by the resilient Red Oak performance. I would be remiss if I didn't also call out the strong operational execution by our management team really in service of our customers. And so we are quite pleased with how the quarter resulted. 
From an M&A perspective, the Solaris integration remains on track, right? The results so far are at least as good as our business case in the quarter. And we -- while we did do a couple of ancillary acquisitions, there was not a new contribution, so to speak, from an M&A perspective, and we continue to be disciplined and focusing on the integration in the assets that we've acquired so far. So overall, very pleased from a first quarter perspective, which is really the basis for us then providing the updated guidance for Pharma. We saw strong demand in the first quarter. And indeed, our guidance going forward assumes that strong demand persists into the rest of the year, right? 
We continue to expect some goodness with respect to generics and goodness with respect to the specialty growth that we called out before. Now we did call out a couple of factors impacting some timing from a quarterly perspective. We need to keep in mind that the Solaris acquisition, we will lap that in the middle of the second quarter. And as Jason highlighted in the remarks, we did renew the CVS contract, and we do have the impact of the customer contract renewals baked into our guidance as well.

**Operator** (Operator):
Your next question comes from the line of Elizabeth Anderson with Evercore ISI.

**Elizabeth Anderson** (Analysts):
Maybe not too dissimilar to Erin's question, but maybe focusing on Other. If we think about the relative like strength, you obviously talked about Strive closing and [ AdaptHealth ], like how do we think about that from like a go-forward rate? Are you seeing sort of increased customer acceptance and penetration? Are you [ seeing ] unit volumes? Like what's driving the strength exactly? Is it kind of early deal synergies? Like just a little bit more detail on that would be super helpful. And any timing-related issues as well in the year.

**Aaron Alt** (Executives):
Thank you. I appreciate the question. We are delighted with the performance of the 3 businesses that constitute Other for us, at-Home, Nuclear and Precision Health and OptiFreight, and a little bit of color around each of those. In the at-Home space, we are being very intentional to set that business up for long-term success, reflective of the secular trends, the competitive strength that we are building through our acquisitions as well. We call it smart growth. 
And so really pleased with how the team is executing, taking advantage of the organic investments we've been making in our supply chain capabilities as well as then how the acquisitions we've completed like ADSG are now rolling into our overall progress. Those plans are on track, and we're realizing the planned synergies there. We've completed the acquisition of Strive, emphasizing the urology part of our category. That's an important element relative to our enterprise strategy as well. And we're looking forward to completing the Adapt transaction at some point after the turn of the calendar year. But overall, we are on track from an operational build perspective and from an integration perspective within at-Home. 
The Nuclear business, strong revenue growth in both PET and Theranostics, areas where we are very focused. That is a key part of our strategy going forward. Again, very focused in urology, another key part of our enterprise strategy. And we continue to expand our capacity and our resiliency there really focused on applying the technology to make that business better, as Jason highlighted in his remarks. And then OptiFreight, just another good business there. We are benefiting from the continued expansion of the capabilities there with existing and new customers as well. 
So from a go-forward perspective from them, again, we are predicting or we are calling from a guidance perspective is the secular tailwinds are going to be unchanged. They're going to help us carry through the year. We are anticipating strong demand driven by those leading positions and the investments that I referenced. Growth will accelerate over the course of the year. That's partly driven by higher confidence in our pipeline than our original guidance as well. And I've already referenced the fact that we have a positive view of the impact of the integrations as we carry forward. So all in all, a very positive story for us.

**Operator** (Operator):
Your next question comes from the line of Michael Cherny with Leerink Partners.

**Michael Cherny** (Analysts):
I'm going to ask another specialty question, but just diving a little deeper in terms of the totality of the pieces coming together. I appreciate you called out the Strive transaction and the importance of urology. Maybe using urology as an example, how do the pieces you have between distribution, MSO, other capabilities drive your level of outperformance? I know we're all trying to get to the bottom of what's been behind some of this recent strength. Is there anything, whether it's urology or other examples, you can call out on maybe getting to a 1 plus 1 plus 1 greater than 3 dynamic?

**Jason Hollar** (Executives):
Yes, sure. I love the question and what you just described is the setup for very much the flywheel, the virtuous cycle, the ecosystem of our specialty strategy, recognizing that these very specialized therapeutic areas have wide-ranging needs. And Strive is a great example of that. You know that we are the leader in urology across many different parts of our enterprise. The obvious ones are certainly within the Pharma business, whether it's distribution or GPO or certainly more recently with our acquisition of Solaris and fitting into the Specialty Alliance. 
To your point, within Strive is a great example of their leadership within urology supplies for delivery to patients in their home, of which we already had a very strong presence with urology in at-Home Solutions, and this just further expands upon that. So not only can it bring a greater breadth of products and services to urologists and patients who have urological needs, it also allows us to create this general ecosystem of expertise across the business. 
The other area that you know that we lead in urology is nuclear. And so there's some direct opportunities like with nuclear now being a very large provider of radiopharmaceutical products to Solaris. But it's also way beyond that. It's also the expertise that when our MSO has an opportunity or a challenge, they've got a direct line to leaders in that space that can help them quickly move to different growth and capabilities. Of course, we do that with all of our customers, but these relationships are even tighter, even quicker. But it's even in less glamorous ways of perhaps some of the medical supplies and GMPD that also have very broad capabilities. 
This list just keeps going on and on and on. And Specialty Networks is another great example of where we started, that business originated in urology. Part of the reason we acquired them first in the specialty journey was because of the breadth and the capabilities that they had to enter into new therapeutic areas, but also being the leader in both GPO and other data services for urology. And they -- now they're expanding further into oncology, where we see similar connective tissue, a little bit less mature in terms of all the different touch points. Urology is definitely that example that connects more broadly. 
Each one of these examples I just provided you, I would say it's a series of singles and doubles and not home runs. And so when you hear us talk about it, it's a driver here and there in the enterprise and in the ecosystem, but it's rarely the driver, the primary driver. It's a component amongst many others. And that's what this team is focused on is the rising tide of demand and utilization growing and making sure that we're providing solutions to customers and ultimately to patients so that we help close the loop on that service, and we can use the full value of all the components of our business to drive the business, but also to solve patient needs.

**Operator** (Operator):
Your next question comes from the line of George Hill with Deutsche Bank.

**George Hill** (Analysts):
And Jason, one where I might ask you to kind of dive in on some recent news is the OPPS rule was finalized last night with the reimbursement changes to 340B. I know that you guys have called out provider strength recently as it relates to revenue growth in the North American Pharma business. Would just be interested in how you think this reimbursement change impacts the provider space and like whether or not it benefits your MSOs, particularly as a result of a mix shift as volume moves in that direction.

**Jason Hollar** (Executives):
Yes. It's a great question, George, because I think you teed it up the right way where ultimately, these are needs by patients. It's a matter of where does the volume go. And the providers at the end of the day for OPPS, the health systems, the hospitals, that's something they're going to have to work through. And of course, we're doing wherever we can to help support them. If there are instances where they find that less affordable to serve those patients, then we do believe those patients will go elsewhere. 
And given our fair share of market across other aspects of the industry, we anticipate picking up that volume consistent with that. That's an assumption and an expectation. We think it's a logical one. We don't know how much may move around within the industry, but it's something that we would anticipate participating in appropriately. But I think it's a little premature to predict how much and the quantification of that. We'll certainly be watching this very closely though.

**Operator** (Operator):
Your next question comes from the line of Allen Lutz with Bank of America.

**Allen Lutz** (Analysts):
I want to follow up on Mike's question around urology. It's really nice to see the strong contributions from urology to specialty growth. I know that Solaris and typical urology practices, only about 40% of revenue comes from medications, but that's been a clear part of your strategy. Would love to dig in more about how the pipeline to add more urologists is progressing. What do they care about? And how is pitching to that type of physician different than maybe an oncologist or another type of physician?

**Jason Hollar** (Executives):
Yes. Let me start with where they are similar. At the end of the day, specialty community physicians do what they do for a pretty particular reasons. They want to take care of patients and want to do so in their community and have that type of relationship. And that means that they're having the challenge of having that connection with their patients while also running a business. And I think more and more the community physicians see that they need some type of partnership through that process. 
So we continue to see that across all of these, especially more complex therapeutic areas where you have wide-ranging needs beyond just distribution contracting support, but really getting deep into data and analytics. And of course, all the back office and physician-specific requirements and ancillary services, this is all very difficult to run a business while also taking care of patients. And so that urology, I think, is very similar to the other areas that we prioritize, whether that is oncology or autoimmune. They have complex enough business requirements and complex enough conditions that they're treating with their patients that they do need support of some sort. 
We don't go into urology with a one-size-fits-all type of approach. We look at what is specific on those services. We see urology fits nicely in between oncology and autoimmune. Many of the ancillary services fit one or the other. And there's not much in urology that's not also either in autoimmune or in oncology. So we see that the breadth of capabilities that we bring and the expertise that we bring across those different therapeutic areas allows those urologists to have it all ways, to have it able to take care of the patient, but also to run a successful business. 
So it's all a long lead-up to say the message absolutely resonates with urologists, and we have a very active, robust pipeline. And we, in our comments, highlighted that we're very focused on making sure we get this integration right so that we have a strong foundation to then further build well into the future. It is a space that continues to be quite fragmented. It is much more fragmented than oncology, a little bit more consolidated in autoimmune, but more closely related to autoimmune than it is to oncology. So there's a lot of potential opportunities for consolidation. We will have opportunities to consolidate further. Our constraint is very much on our confidence that we will integrate it very successfully so the physicians have a fantastic experience in the process.

**Operator** (Operator):
Your next question comes from the line of Lisa Gill with JPMorgan.

**Lisa Gill** (Analysts):
I appreciate your comments around 340B and the potential and change in site of care. Obviously, with the [indiscernible] very dynamic environment right now. How should we think about any potential changes or things that you're watching from a DC perspective as we think about reimbursement going forward? You've highlighted WAC changes and your ability to be able to manage through that. But anything that's on your radar that you're looking at from that perspective as we think about going into calendar '27?

**Jason Hollar** (Executives):
Yes. Well, we're always looking at everything, I guess, is probably the short answer. When I think about regulatory, I start with nearly the same starting point no matter what particular topic we're talking about. Number one, we do not believe it's the intention, and this is getting off 340B a little bit. I'll get back to it in a second, but just regulatory more general, you commented about DC, where there's the most implication typically is at the provider level. And of course, where we are the provider is normally within the MSOs, in those community physicians. So in those instances, we do not believe the intention of the administration is to harm that community provider. Our goals and objectives are very aligned with the administration, very aligned with those physicians. We're looking for greater access to low-cost innovative health care. And we don't think it's their intention to harm what is now the lowest-cost form of care already in those communities and of course, the access to those communities. 
So first and foremost, we don't believe that, that is the objective and the intent. And then secondly, even if there are implications to those providers, those physicians, it is usually a second order effect for us. Again, while we have the direct impact for some therapeutic areas, where we participate typically has a very diverse payer set, very substantial portion of our business with commercial payers, and we have very diversified drug spend and other types of revenue within those MSOs and those providers. So we have a relatively low potential impact even if there is legislation that ends up impacting those providers, which, again, we don't think is likely to be the case. 
So there's a lot of potential variables that happen with that. And of course, we are in DC a lot. We are very closely engaged with both sides of the aisle. Of course, we had long-standing relationships and continue to have long-standing relationships. There are some new members of Congress that we're going to now need to spend a little bit more time with. But the vast majority of the people we see are still the same people, and we'll continue to make sure that we're advocating not just for our business, but ultimately for customers and the patients. 
As it relates to the 340B, I think conceptually, a lot of those things carry over with that. The only thing I'd add specifically about any specific product category that would be outside of the provider space now thinking about us as a distributor, you've seen our consistent ability to migrate through that. Sometimes there may be a little bit of a timing differential in terms of when certain corridors are touched and when those impacts can then be passed on to customers. But at the end of the day, we provide huge value for the services that we provide, and we would anticipate that the continued compensation would be appropriate for that.

**Operator** (Operator):
Your next question comes from the line of Eric Percher with Nephron Research.

**Eric Percher** (Analysts):
A question on generic program performance. I believe we heard volume running a bit ahead of your expectations, and that continues on. But there was also a comment on Red Oak. And so I wanted to ask if the Red Oak benefits tend to continue to accumulate over time, is there any change relative to extending the distribution agreement? Or does Red Oak continue to extend through 2029?

**Jason Hollar** (Executives):
Yes. Well, I will never speak for our customer, but I'm pretty confident they speak very highly of -- or I should say, our joint venture partner, in this case, would speak very highly of the value that we receive from Red Oak, not just in terms of value in dollars and cents, but in terms of the service level, which we continue to believe we're best-in-class with. So yes, Red Oak is a separate contract that we'll certainly be looking to address relatively soon. It's a relationship that goes back a long way, and we see that there is continued value. 
So your question on ongoing value, it's an evergreen opportunity. While -- and again, it goes to value in terms of dollars as well as service level. There's opportunities for Red Oak to perform every single day. There's always going to be opportunities in the marketplace to improve service. There will be manufacturers coming in and out of market, and it's their objective to bring us the best value, the best cost, the best service. And as those new items, which is an opportunity for the industry and for ourselves in particular, the loss of exclusivity, new items this year is pretty good. It's fairly consistent to what we saw last year. We see an increasing pipeline building over the next couple of years. So we see additional opportunity for Red Oak to provide value to both of their parents there. And it's our expectation that, that relationship certainly would transcend any spin-off on the CVS side. But then certainly, we would anticipate it proceeding beyond the '29 time frame as well. But we have a little bit of work to do to complete that step.

**Aaron Alt** (Executives):
Just to jump on top of that briefly, Eric, from a guidance perspective, Jason referenced that the LOE benefits year-over-year for '27, which we're in, are roughly consistent with what they were last year. We will see a nice benefit, particularly in '29 going forward as we look at the number of LOEs that are coming. And so I just want to be clear on that from a long-term perspective.

**Operator** (Operator):
Your final question comes from the line of Kevin Caliendo with UBS.

**Kevin Caliendo** (Analysts):
I want to talk a little bit about like future M&A plans. You highlighted specialty and the like. But when we're thinking about this, is it market share? Is it more services? Would you be interested in sort of following suit with McKesson and maybe adding some clinical trial opportunities for your urology GPO network? Or -- and maybe there's stuff to do in the home? I guess what I'm asking is where do you feel like there's opportunity to grow? What would be a leverageable asset for you in either of these venues?

**Jason Hollar** (Executives):
Sure. Love the question and happy to go deeper. First of all, what's really important to us with any M&A is you start with, you lead with the strategy. And I think it's highly likely that anything that we do in the future, you'll see connective tissue to the broader strategy that we've laid out in good detail and somewhat at least consistent with the work that we've done before. And that's because not only is that the best way to create value by executing well and being tight with that strategy, there's so much opportunity within the current realm of total addressable market that we have today that I think it's highly likely that we're going to want to continue to stay focused. So for -- to be very clear, we're not looking for a fourth leg of this stool, but there's still a lot of additional opportunities within the other 3 legs that we have today. 
And another thing I'll just say, a little bit of an editorial on this. Our answer could be very different than our competition's answer, and we all could be right. What I mean by that is we have different strengths. We have different -- of course, we all have a similar core, but we have different areas that we are leaders in. When you look at within our Specialty business, what we have with the Specialty Alliance, our focus on the multi-specialty and all the investments we've made there with BioPharma Solutions, they have similar types of services there, but they don't necessarily overlap in exactly the same way. And so we have some strength there. And of course, we have our other growth businesses of Nuclear, at-Home and OptiFreight that are leaders in their space and also quite unique relative to the competition. 
So we could end up having a different answer. They could go deeper in a particular area, and it may or may not be where we want to focus on. So where are we going to focus? It's going to be a lot of the same themes that you've heard from us. Specialty, absolutely. Within specialty, we do see continued opportunity within the MSOs. As I just indicated, where we have prioritized within our MSOs, it remains a more fragmented space, and we are starting to consolidate that, but there's still a lot of opportunity there. Outside of the MSOs within BioPharma Solutions, we highlighted our leadership in areas like our 3PL, like our Sonexus Patient Hub. These are areas that we are the leader, and we have some opportunity because it's still, in many cases, fragmented and with good opportunity. But there's a broad need by customers that's not always being satisfied in the marketplace to their desires, and we see more opportunity there. 
And then within the Other growth businesses where we've been most active has been in at-Home Solutions, also very fragmented space. So the word fragmented came up in most everything I talked about, and that just tells you that there's a lot of opportunity, a lot of potential partners there, and it can be a partnership. It doesn't have to be an acquisition. But there's enough on that list that I suspect you're going to -- that's where we spend the most time. That's where we spend all of our dollars is in areas that hit those particular parameters to date, and it's where we are most focused in our investigations and our exploratory discussions in the marketplace today. 
So our objective is consistent with the strategy. Therefore, it should not be a surprise whatever we choose to do. We have the financial flexibility to do so, but we also have a lot of confidence in the core. So we'll be ready to execute financially and with the support organization when the opportunity presents itself.

**Aaron Alt** (Executives):
I want to emphasize on that. Jason's use of the word flexibility is really driven by the strong cash flow generation that the business has been able to deliver for the last several quarters. You will have seen that we had another quarter of great adjusted free cash flow, $5.3 billion of cash in the bank at the end of our first quarter. But in all of that, we will remain loyal to our disciplined capital allocation philosophy, right? We are investing all the dollars that we need to and should from an organic CapEx perspective. 
We feel great about the breadth of our investments more than we ever have before across the businesses, really all 5 of our operating businesses. We've got a great, strong balance sheet. We're within our targeted leverage ratio. So we don't need to take actions there to protect it. You saw we repurchased half of our annual commitment of share repurchase of $1 billion. We repurchased $500 million in the first quarter, really putting us in a place where we can consider what next from that strong cash flow, whether it's the incremental M&A that Jason was just referencing or further return of capital to shareholders. So we're in a strong place as we carry forward into the rest of the year and are really pleased with the momentum overall.

**Operator** (Operator):
We have reached the end of the Q&A session. I will now hand the call back to Jason Hollar for closing remarks.

**Jason Hollar** (Executives):
Yes. Just thanks for joining us. And as always, reach out to David and team for any follow-ups that you may have. Have a great day.

**Operator** (Operator):
This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CAH_Q4_2026_Earnings_Call_20260811.md
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 EPS 指引區間（原話："expect fiscal '27 EPS to be between $12.40 and $12.60"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 EPS 成長指引 13–15%（對基準）；長期 12–14% 重申（原話："EPS growth rate guidance of 12% to 14% per year"）
- 2026-08-11｜CFO Aaron Alt｜margin：FY27 基準 EPS 排除 Q4 一次性 $0.31 關稅退款（原話："So the baseline adjusted non-GAAP EPS number is $10.95."）
- 2026-08-11｜CFO Aaron Alt｜guidance：Pharma 營收 FY27 成長 3–5%（原話："Pharma segment revenue to show 3% to 5% growth"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Pharma 部門利潤 FY27 成長 8–11%（原話："we expect the Pharma segment to deliver 8% to 11% growth"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Pharma 利潤成長節奏：Q1 接近區間高端（含 Solaris）（原話："we expect Q1 profit growth to be near the high end of our"）
- 2026-08-11｜CFO Aaron Alt｜guidance：已宣布併購貢獻 Pharma 利潤成長 2–3 個百分點（原話："M&A is expected to contribute 2 to 3 percentage points"）
- 2026-08-11｜CFO Aaron Alt｜guidance：GMPD FY27 部門利潤指引 $200–220M（原話："expected segment profit of $200 million to"）
- 2026-08-11｜CFO Aaron Alt｜guidance：GMPD Q1 FY27 利潤約為 FY26 Q1 的一半，後段加權（原話："roughly half of the Q1 fiscal 2026 result"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Other 群組營收成長指引 11–13%，並於年內加速（原話："we anticipate 11% to 13% growth in revenue"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Other 群組利潤成長指引 15–18%（原話："We expect segment profit to deliver 15% to 18% growth in the"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 利息及其他費用指引（原話："interest and other expense to be $240 million to $290"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 有效稅率指引 19–20%（原話："tax rate to be 19% to 20% for the year"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 調整後自由現金流指引 $3.5–4B（原話："between $3.5 billion and $4 billion in adjusted free"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：FY27 資本支出預期 $700M（原話："we expect capital expenditures of $700 million"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：FY27 至少 $10 億回購（原話："least $1 billion in share repurchases"）
- 2026-08-11｜CEO Jason Hollar｜capital_allocation：董事會增加 $50 億回購授權（原話："has authorized a $5 billion increase to our share repurchase"）
- 2026-08-11｜CEO Jason Hollar｜capital_allocation：新授權被形容為補充彈藥（原話："our new authorization effectively recharges the battery"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：FY27 不假設重大併購，保留小型併購彈性（原話："not assuming material M&A, but have reserved modest"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：可能考慮策略性併購或額外資本回饋（原話："consider strategic M&A or incremental return of capital"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：FY26 回購總額與均價（原話："totaled $1.35 billion of share repurchase during the year"）
- 2026-08-11｜CFO Aaron Alt｜capital_allocation：新 $40 億循環信貸取代三個舊額度（原話："a new $4 billion revolver program, replacing 3"）
- 2026-08-11｜CFO Aaron Alt｜margin：Q4 GMPD 認列一次性 IEEPA 退款淨營業利益 $1 億（原話："a onetime $100 million net operating earnings benefit"）
- 2026-08-11｜CFO Aaron Alt｜margin：Q4 EPS 中 $0.31 來自 IEEPA 退款（原話："$0.31 of the EPS is due to recording the IEEPA tariff refund"）
- 2026-08-11｜CFO Aaron Alt｜margin：管理層稱退款屬非經常性（原話："We view the refund as nonrecurring"）
- 2026-08-11｜CFO Aaron Alt｜risk：取代 IEEPA 的關稅仍持續產生成本（原話："incur costs from the tariffs that replaced IEEPA"）
- 2026-08-11｜CFO Aaron Alt｜margin：GMPD Q4 部門利潤扣除退款後為 $5,000 萬（原話："GMPD segment profit was $50 million, normalized for the"）
- 2026-08-11｜CFO Aaron Alt｜product：Cardinal Health 自有品牌排除關稅影響後連續第六季至少中單位數成長（原話："the sixth consecutive quarter of at least mid-single-digit"）
- 2026-08-11｜CFO Aaron Alt｜margin：Pharma 營收中 GLP-1 順風與 IRA WACC 逆風各約 500 bp，大致抵銷（原話："IRA WACC changes, each worth approximately 500 basis points"）
- 2026-08-11｜CFO Aaron Alt｜guidance：FY27 IRA 價格變動對營收影響與 FY26 下半年相近，且無利潤不利影響（原話："to have no adverse profit impact"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Pharma 營收假設：強勁但非超額需求（原話："strong demand, but not the outsized demand we experienced"）
- 2026-08-11｜CFO Aaron Alt｜customer：Pharma 客戶續約含 Kroger 長期延長（原話："long-term extension with Kroger"）
- 2026-08-11｜CFO Aaron Alt｜guidance：Specialty 營收含有機與已宣布併購，雙位數成長（原話："all organic and already announced inorganic efforts"）
- 2026-08-11｜CEO Jason Hollar｜customer：GMPD 最大客戶長期續約（原話："long-term renewal of our largest customer"）
- 2026-08-11｜CEO Jason Hollar｜customer：3PL 取得兩項基因療法商業化協議；細胞與基因治療市占（原話："exclusively service nearly half the cell and gene market"）
- 2026-08-11｜CEO Jason Hollar｜product：Theranostics 與 PET 成長率（原話："PET growing over 20% and Theranostics growing nearly 30%"）
- 2026-08-11｜CEO Jason Hollar｜product：ADS 整合綜效高於預期（原話："where we are seeing greater than anticipated synergies"）
- 2026-08-11｜CEO Jason Hollar｜commitment：Biopharma Solutions 2028 年 $10 億目標，稱進度符合（原話："getting that business to $1 billion by '28"）
- 2026-08-11｜CEO Jason Hollar｜product：Biopharma Solutions 成長 20% 以上（原話："20-plus percent growth expected and realized"）
- 2026-08-11｜CEO Jason Hollar｜risk：IRA/340B 等監管：管理層認為不應改變其報酬（原話："don't believe our compensation should change"）
- 2026-08-11｜CEO Jason Hollar｜risk：340B 對醫院客戶影響可能大於對公司影響（原話："customer impact is likely to be greater than our impact"）
- 2026-08-11｜CEO Jason Hollar｜capital_allocation：FY27 投資優先順序框架與去年相同（原話："commentary certainly is exactly the same"）
- 2026-08-11｜CEO Jason Hollar｜capital_allocation：擴產以瓶頸（冷凍冷藏）與自動化為導向，非先建後等客（原話："not like we're a build-it-and-they-will-come strategy"）
- 2026-08-11｜CEO Jason Hollar｜competition：分銷模式可能演變，管理層稱將調整（原話："So the model will change. It will evolve."）
- 2026-08-11｜CEO Jason Hollar｜margin：企業整體彙總利潤率約 1%（原話："our margin at 1% overall aggregate margins"）
- 2026-08-11｜CEO Jason Hollar｜margin：Other 群組三個事業毛利結構差異；OptiFreight 利潤率較高（原話："services business has an overall higher rate"）
- 2026-08-11｜CFO Aaron Alt｜margin：學名藥轉換帶來較高獲利，並預期 FY27 續有貢獻（原話："we prefer the profitability that comes with a generic"）
- 2026-08-11｜CFO Aaron Alt｜risk：GLP 量成長但放緩（原話："growing but moderating GLP volumes"）
- 2026-08-11｜CEO Jason Hollar｜risk：油價/商品成本壓力：若全年居高，GMPD 落在指引低端（原話："closer to that bottom end of our guidance range for GMPD"）
- 2026-08-11｜CFO Aaron Alt｜risk：若伊朗衝突拖長，GMPD 利潤傾向指引低端（原話："Should the conflicts in Iran prove protracted"）
- 2026-08-11｜CEO Jason Hollar｜commitment：GMPD 改善計畫維持（原話："the GMPD improvement plan remains in place"）
- 2026-08-11｜CEO Jason Hollar｜guidance：FY27 學名藥量成長仍未達長期規劃 2–3% 的上緣（原話："still not in the 2% to 3% range for '27"）
- 2026-08-11｜CFO Aaron Alt｜guidance：稅率 19% 預期延續至 FY27；更長期稅率延後說明（原話："19% anticipated rate for '26 to be durable into '27"）
- 2026-08-11｜CEO Jason Hollar｜commitment：管理層稱過去四年達成所說的事（原話："we have done what we said we would and more"）

### 問答異常語氣（迴避／改口／保留）
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Kevin Caliendo（UBS）：量化「超額需求」與「強勁需求」差異｜答法：Aaron Alt 表示不提供數學公式（'we're not going to provide you with a mathematical'）；Jason Hollar 改以 Specialty 與學名藥量舉例，未給界線數字
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Allen Lutz（BofA）：品牌轉學名藥對營收與 EBIT 加速各貢獻多少｜答法：Aaron 稱學名藥為正貢獻但未給數字；Jason 稱 'not so much that we're going to break out that number'，僅說遠低於 500 bp
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Lisa Gill（JPM）：IRA 之外的監管風險與 340B 對醫院客戶量的影響｜答法：Jason 以通則回答（與各方密切接觸、支持可及性與可負擔性），未給 340B 量的影響數字
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Stephen Baxter（Wells）：新聞稿未點名 Nuclear 為利潤成長驅動的原因｜答法：Aaron 稱 'I wouldn't read too much into the order of prioritization'，未直接說明未點名原因
- CAH_Q4_2026_Earnings_Call_20260811.md｜問：Kevin Caliendo（UBS）：19–20% 稅率是否為長期基準｜答法：Aaron 確認 FY27 稅率，長期稅率 'defer comments' 留待之後

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
{"date":"20260525","verdict":"B 衛星候選","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Specialty 業務超越基底分銷，貢獻 OI 25%+","columns":{"2Y 驗證點":"Specialty 營收 YoY ≥ 18%","5Y 驗證點":"Specialty OI ≥ 25% 全公司 OI","10Y 驗證點":"Specialty + MSO 平台 OI ≥ 40% 全公司 OI","具體門檻":"FY26: Specialty 營收 +20% YoY (Q3 已達)；FY28 Specialty OI 占比 ≥ 22%","來源":"FY26 法說會、mgmt Investor Day 2025 9/2025","漂移觸發":"連 2 季 TTM 偏離 ≥ 5% → 削弱（2Y 假設）"}},{"id":"H2","text":"Pharma 段 OI margin 穩定在 1.4%+","columns":{"2Y 驗證點":"連續 4 季 OI margin ≥ 1.35%","5Y 驗證點":"5Y 滾動均 OI margin ≥ 1.40%","10Y 驗證點":"10Y 平均 OI margin ≥ 1.35%（即使遇 cycle 低谷）","具體門檻":"FY25: Pharma OI margin = 1.42%；FY26 guide 維持 +OPI growth 9-11%","來源":"FY25 10-K、Q3 FY26 8-K","漂移觸發":"連 4 季 TTM 偏離 ≥ 5% → 削弱（5Y 假設）"}},{"id":"H3","text":"大客戶結構保持穩定（CVS、Walmart 維持合約）","columns":{"2Y 驗證點":"無大客戶流失公告","5Y 驗證點":"Top 10 客戶占比 ≥ 60%（穩定）","10Y 驗證點":"無新 vertical PBM 整合導致分銷結構重組","具體門檻":"FY25 10-K 揭露 5 大客戶占比 50%+；無公開 contract 更動","來源":"FY25 10-K","漂移觸發":"單一客戶流失公告 → 立即重評（不需連兩季）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"大客戶流失（CVS / Walmart 等轉投 MCK）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期","監測指標":"季度 8-K 客戶留存公告 + Pharma 營收 YoY","警戒閾值":"季度 Pharma 營收 YoY 跌破 5%（暗示大客戶流失，已知 baseline ~9%）"}},{"id":"R2","text":"關稅 + manufacturer 議價權壓縮 Pharma OI margin","columns":{"對應假設":"H2","時間尺度":"🔥 中期","監測指標":"Pharma segment OI margin（季度）","警戒閾值":"連兩季 ≤ 1.35%（FY25 = 1.42%，跌 5bp 即削弱 H2）"}},{"id":"R3","text":"GLP-1 處方量見頂 / 被新藥取代 + biosimilar 滲透加速","columns":{"對應假設":"H1","時間尺度":"🐢 長期","監測指標":"GLP-1 weekly scripts、biosimilar share、specialty mix","警戒閾值":"2027-2028 期間 Specialty 整體 YoY 連 4 季"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":200.68,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAH_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
