你是 stock-analyst **v20 判斷 agent**，標的 ALAB（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ALAB","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":392.4,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益率","value":39.1,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":22.7,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi5_non_gaap","label":"Non-GAAP 毛利率","value":73.7,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi6_non_gaap_eps","label":"Non-GAAP EPS","value":0.8,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"},"note":"consensus 0.69（來源：web_search，MarketBeat／Benzinga 2026-08-04）"},{"id":"f_kpi7_q3_fy2026","label":"下一季指引（Q3 FY2026）","value":"營收 540–560M；GAAP/Non-GAAP 毛利率約 72%；Non-GAAP opex 156–160M；Non-GAAP EPS 1.16–1.21；GAAP EPS 0.87–0.92；稀釋股數約 185M","period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"文字","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-03","period":"2026-11-03","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-03"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_alab_gross_margin_pct","label":"ALAB 毛利率","value":73.89,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_alab_operating_margin_pct","label":"ALAB 營業利益率","value":25.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_alab_fcf_margin_pct","label":"ALAB FCF 利潤率","value":22.15,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crdo_gross_margin_pct","label":"CRDO 毛利率","value":67.07,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crdo_operating_margin_pct","label":"CRDO 營業利益率","value":31.74,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crdo_fcf_margin_pct","label":"CRDO FCF 利潤率","value":27.57,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_gross_margin_pct","label":"MRVL 毛利率","value":52.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_operating_margin_pct","label":"MRVL 營業利益率","value":16.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_fcf_margin_pct","label":"MRVL FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF，上半年累計；新聞稿無單季）","value":134.2,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi4_sbc","label":"SBC 占營收","value":16.3,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":190.71,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-4.54,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":29.11,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":7.33,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.09 → 4.39）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":5.63,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.57 → 6.94）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":4.87,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.21 → 8.61）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":4.39,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.94,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":8.61,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":8.93,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 4.03 → 4.39（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":75.38,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":21.42,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":20.56,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":43.44,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 4.39，分子＝快照價 190.71","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1333.25,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 44.99、現金 1378.24（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":174.78,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":31999.44,"period":"2026-11-08","unit":"USD m","basis":"市值 33332.69 ＋ 淨負債 -1333.25","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":2027.27,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":3353.93,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":15.78,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 190.71 / W52 236.29 / W104 178.69 / W250 None / W250 13週斜率 None%"},{"id":"f_ma_w52","label":"52 週均線","value":236.29,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":178.69,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 列出主要對手為 Broadcom、Credo、Marvell、Microchip、Montage、Parade、Rambus；對手多只在部分產品線重疊。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"Our competitors typically compete with us with respect to some, but not all, of our solutions. Our principal competitors include Broadcom, Inc., Credo Technology Group Holding Ltd., Marvell Technology, Inc., Microchip Technology Inc., Montage Technology, Parade Technologies, Ltd., and Rambus, Inc.","as_of":"2026-02-20","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：對手可能較易取得設計導入（design wins），CXL 與 UALink 仍在早期採用，若大廠不支持同一標準或出現競爭標準，公司可能失去份額。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"As a result, some of our competitors may be better situated to meet changing customer needs and secure design wins. Increasing competition in the markets in which we operate may negatively impact our revenue and gross margins.","as_of":"2026-02-20","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Astera 公布 Scorpio X-Series 320 lane 交換器，2026 下半年量產，目標為商用 scale-up 市場。","source":"Astera Labs Q1 2026 財報新聞稿 (barchart)","url":"https://www.barchart.com/story/news/1721880/astera-labs-reports-first-quarter-2026-financial-results","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Zacks 稱 Credo 在光學 DSP 持續拿下份額，Astera 同時面對 Broadcom 與 Credo 的競爭。","source":"Zacks: ALAB benefits from PCIe demand, can it stay ahead of its competitors","url":"https://www.zacks.com/stock/news/2973762/alab-benefits-from-pcie-demand-can-it-stay-ahead-of-its-competitors","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 年報揭露客戶高度集中：前三大終端客戶約占營收 86%，風險揭露稱單一終端客戶超過 2025 年營收 70%（經搜尋摘要轉述，未直接讀原文頁面）。","source":"Astera Labs, Inc. Form ARS FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000114036126016366/ny20065212x3_ars.pdf","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"2026 年 Q1 業績揭露：Astera 贏得第二個客製 CXL 設計（KV cache offload），營收預計 2027 年；NVLink Fusion 相關客製矽與 NVIDIA 及一家 hyperscaler 深度開發中，營收 2027 年起；管理層稱客製產品會選擇性承接（經二手摘要轉述）。","source":"Astera Labs Q1 2026 earnings coverage (Converge Digest / Yahoo Finance summary)","url":"https://convergedigest.com/astera-labs-q1-revenue-jumps-93-ai-fabric-growth/","excerpt":null,"as_of":"2026-05-05","retrieved_at":"2026-10-13","affects":["thesis.H","triggers"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K（搜尋摘要轉述）：五家客戶各占營收 10% 以上——A 20%、B 20%、C 17%、D 16%、E 11%，合計約 84%；最大單一客戶 20%。數字來自搜尋摘要對 10-K 表格的轉述，未逐字讀頁面。","source":"Astera Labs, Inc. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"The Company had the following customers that individually comprised 10% or more of its revenue","as_of":"2026-02-28","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2024 10-K：客戶 A 占營收 36%、B 24%、C 11%；客戶 F 占 2024 年底應收帳款 31%。","source":"Astera Labs, Inc. Form 10-K FY2024 (Financial_Report, SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629725000003/Financial_Report.xlsx","excerpt":"Customer A | Revenue 0.36; Customer B | Revenue 0.24; Customer C | Revenue 0.11; Customer F | Accounts Receivable 0.31","as_of":"2025-02-28","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 年 6 月 30 日 10-Q：現金、約當現金與有價證券 $1.3B，公司稱現金足以支應至少未來 12 個月營運；2026 上半年營運現金流 $162.3M。第三方資料站列總債務 $41.9M。（搜尋摘要轉述）","source":"Astera Labs, Inc. Form 10-Q (quarter ended 2026-06-30), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000035/alab-20260630.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Amazon 持有認股權證，與採購 Astera 產品掛鉤，額度最高 $65 億採購額，隨採購至 2033 年 2 月歸屬（搜尋摘要轉述，第二手）；對毛利率有非現金影響。","source":"WebSearch 摘要（引 Astera 10-Q 與聚合站）","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000035/alab-20260630.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"未查到主要客戶（超大型雲端業者）信用評等或財務惡化、破產、Astera 下修財測的報導；Q2 2026 財測 $355–365M 為指引而非下修。僅見 TD Cowen 目標價 $425→$375 維持 hold，屬評價面。","source":"TIKR 等聚合站（搜尋摘要）","url":"https://www.tikr.com/blog/astera-labs-beat-q1-2026-estimates-on-all-four-lines-heres-why-the-stock-sold-off-and-where-it-could-go","excerpt":"TD Cowen cut its target from $425 to $375 and kept a hold rating","as_of":"2026-05-05","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner 2026年7月存貨預測：2Q26 全球半導體存貨指標(GIISST)降8.5%進入中度短缺，受AI半導體需求驅動，預期此趨勢延續至2027年。","source":"Gartner Insights Abstract","url":"https://www.gartner.com/en/documents/8208429","excerpt":"In 2Q26, the GIISST fell 8.5% into moderate shortage, driven by strong AI semiconductor demand. This trend is expected to persist through 2027","as_of":"2026-07-01","retrieved_at":"2026-10-13","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"TrendForce：2026年NAND供給短缺4-5%，2027下半年供給位元成長將超過需求成長（二手轉載）。","source":"TrendForce via itiger: NAND Flash Supply Shortage Expected to Ease in Second Half of 2027","url":"https://www.itiger.com/news/1168527958","excerpt":"supply will fall short of demand by 4-5% in 2026, but by the second half of 2027, the growth in supply bits will outpace demand growth.","as_of":"2026-07-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Wolfe Research分析師Chris Caso認為半導體供過於求最早在2028年之前幾無可能（受新晶圓廠物理限制）。","source":"247WallSt: Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Micron執行長在9月30日財報會議表示記憶體供需於FY2027、FY2028可能進一步趨緊；下一波供給(Micron愛達荷/日本、SK hynix清州)多要到2028下半年後才放量。","source":"Micron earnings call 2026-09-30 (via search summary)","url":null,"excerpt":null,"as_of":"2026-09-30","retrieved_at":"2026-10-13","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ASML(2026年7月)：產能實質上賣到2027，訂單簿延伸至2028，指引今年約成長35%。","source":"Quilter: ASML beat and raise reinforces strength of semiconductor demand","url":"https://media.quilter.com/search/2026/asml-beat-and-raise-reinforces-strength-of-semiconductor-demand/","excerpt":null,"as_of":"2026-07-15","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"SEMI：300mm晶圓月產能至2028年底達1110萬片，年複合成長7%；先進製程(7nm以下)CAGR 14%。","source":"The Machine Maker: SEMI Projects 69% Growth in Advanced Semiconductor Capacity by 2028 Driven by AI Demand","url":"https://themachinemaker.com/news/semi-projects-69-growth-in-advanced-semiconductor-capacity-by-2028-driven-by-ai-demand/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ALAB Q1 2026營收3.084億美元、年增93%；PCIe Gen 6約占近季營收三分之一且ASP高於前代；第三方稱Q2 2026營收年增104%至3.924億美元；風險含自研客戶晶片、多季客戶ramp執行風險。","source":"TIKR: Astera Labs Stock Is Up 227% in One Year","url":"https://www.tikr.com/blog/astera-labs-stock-is-up-227-in-one-year-heres-whats-driving-the-rally","excerpt":null,"as_of":"2026-05-01","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Astera Labs FY2025 10-K 與年報列出出口管制風險：若被認定違反貿易制裁或出口規則，可能面臨喪失出口權及罰款；亦提及美國商務部對先進運算晶片的限制持續修訂。屬一般性風險揭露，非特定進行中調查。（內容取自搜尋摘要轉述，未讀原文頁面）","source":"Astera Labs, Inc. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Astera FY2025 10-K 風險揭露：Chinese customers facing tariffs may build their own products or buy from competitors, and may cancel or delay orders; prolonged or expanded export restrictions would hurt revenue and results.","source":"Astera Labs, Inc. Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Astera S-1 揭露：美國對部分中國客戶的銷售限制，使部分銷售可能需出口許可，且不保證獲准；並提及中國不可靠實體清單風險。","source":"Astera Labs, Inc. Form S-1 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000119312524040419/d285484ds1.htm","excerpt":"Due to the U.S. government restricting sales to certain customers in China, sales to some of our customers may require licenses in order for us to export our products; however, there can be no assurances that requests for licenses will be approved by the U.S. government.","as_of":"2024-02-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Q1 2025 法說：管理層稱中國出口限制對 retimer 出貨（連結 merchant GPU 系統）屬小幅逆風，終端客戶中國曝險低於營收 10%，尚未見關稅重大影響。","source":"Fintool Astera Labs Q1 2025 earnings summary","url":"https://fintool.com/app/research/companies/ALAB/earnings/Q1 2025","excerpt":null,"as_of":"2025-05-06","retrieved_at":"2026-10-13","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 稱半導體關稅可能降低產品需求，美國對關鍵礦物的關稅可能推高投入成本。","source":"Astera Labs, Inc. Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 公告對一小類先進半導體及含其衍生產品課 25% Section 232 關稅，2026-01-15 生效；適用範圍窄，搜尋結果未顯示 Astera 產品是否在涵蓋範圍內。","source":"White & Case; EY Tax News, 25% Section 232 tariff on certain advanced semiconductors","url":"https://taxnews.ey.com/news/2026-0209-us-section-232-proclamation-imposes-25-percent-tariff-on-certain-semiconductors","excerpt":"Effective 12:01 a.m. EST on 15 January 2026, a 25% ad valorem tariff applies to certain advanced computing chips and specified derivative products.","as_of":"2026-01-15","retrieved_at":"2026-10-13","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ALAB 10-K 揭露其主要製造商台積電的晶圓廠與主要經銷商皆位於台灣","source":"Astera Labs Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"the foundry used by our primary manufacturer, TSMC, as well as our primary distributor, is located in Taiwan","as_of":"2025-12-31","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險揭露：若台積電無法供應足量晶圓，ALAB 出貨與營收會受損","source":"Astera Labs Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"if TSMC is unable to supply us with sufficient quantities of wafers to meet all of our requirements","as_of":"2025-12-31","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K 稱製造夥伴、經銷商與多數營收集中於台灣、中國、南韓；FY2025 年報再加入新加坡，且多數營收來自東亞","source":"Astera Labs Form 10-K FY2024 / Form ARS FY2025 (SEC)，經搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629725000003/alab-20241231.htm","excerpt":null,"as_of":"2024-12-31","retrieved_at":"2026-10-13","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"IPO 招股書指出台灣地震風險因晶圓廠鄰近斷層帶而顯著，且可能無法以合理條件取得替代產能","source":"Astera Labs Form 424B4 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000119312524073873/d285484d424b4.htm","excerpt":"the risk of an earthquake in Taiwan and elsewhere in the Pacific Rim region on our business is significant due to the proximity of major earthquake fault lines to the foundry's facilities","as_of":"2024-03-20","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"第三方彙整站 policyrisk.com 評 ALAB 製造曝險為高，稱約 73% 不動產及設備位於台灣，且 2025 年單一終端客戶占營收逾 70%、前三大約 86%（第三方轉述，非原始 filing 逐字）","source":"policyrisk.com ALAB company profile","url":"https://policyrisk.com/world/company/ALAB","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"ALAB 2026 Q2 營收 $392.4M，QoQ +27%、YoY +104%；non-GAAP 營業利益率 39.1%。","source":"Astera Labs Reports Second Quarter 2026 Financial Results (asteralabs.com)","url":"https://www.asteralabs.com/news/astera-labs-reports-second-quarter-2026-financial-results/","excerpt":"Record quarterly revenue of $392.4 million, up 27% QoQ and up 104% year-over-year. Non-GAAP operating margin was 39.1%","as_of":"2026-08-04","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"PCIe 6 產品占 Q2 營收過半，Aries 訊號調節產品線創單季紀錄；管理層預期 Scorpio 交換器於 Q3 成為最大產品線，比先前預期提早一季。","source":"Futurum, Astera Labs Q2 FY 2026 Earnings Pull Scorpio Switch Leadership Forward","url":"https://futurumgroup.com/insights/astera-labs-q2-fy-2026-earnings-pull-scorpio-switch-leadership-forward/","excerpt":"Scorpio fabric switches become our largest product family, one quarter ahead of our prior expectations.","as_of":"2026-08-04","retrieved_at":"2026-10-13","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q1 營收 $308.4M，YoY +93.4%；資料商顯示公司僅 1 個報告部門（Intelligent Connectivity Platform），無正式分部營收，以產品線為準。","source":"OpenCapital ALAB Q1 2026","url":"https://www.opencapital.sh/stocks/alab/earnings/q1-2026","excerpt":"Q1 2026 revenue of $308.4M (+93.4% YoY)","as_of":"2026-05-01","retrieved_at":"2026-10-13","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"競爭風險：BofA 初始報告指出 Nvidia NVLink 與 Broadcom scale-up Ethernet 交換器的競爭可能拖累成長；Scorpio-X 對應 AWS 部署的 2026-29 年機會約 $2.5B。","source":"Nasdaq/Zacks, ALAB articles citing BofA initiation","url":"https://www.nasdaq.com/articles/alab-rides-strong-demand-pcie-solution-sign-more-upside","excerpt":"competition from Nvidia's NVLink and Broadcom's Scale-Up Ethernet based switches could weigh on growth","as_of":"2026-05-01","retrieved_at":"2026-10-13","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"WSTS 2026 春季預測：2027 年全球半導體市場再成長 27% 至約 USD 1.9 兆；2026 年約 USD 1.51 兆。（as_of 為約略月份，2026-06）","source":"WSTS FC Release 2026 May / bits-chips 報導","url":"https://www.wsts.org/esraCMS/extension/media/f/WST/7618/WSTS_FC-Release-2026-May.pdf","excerpt":null,"as_of":"2026-06-01","retrieved_at":"2026-10-13","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Astera 管理層稱光學為銅線的增量補充而非取代；整合 CPO 模組的 Scorpio X 規劃 2028 年以後，光學大規模採用預期在 2028 年以後。","source":"MarketBeat, Astera Labs targets $10B AI connectivity opportunity as Scorpio X series ramps","url":"https://www.marketbeat.com/instant-alerts/astera-labs-targets-10b-ai-connectivity-opportunity-as-scorpio-x-series-ramps-2026-05-27/","excerpt":null,"as_of":"2026-05-27","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"分析師指出 Nvidia NVLink 與 Broadcom Scale-Up Ethernet(SUE) 交換器的競爭可能拖累成長並限制估值倍數擴張；Broadcom 亦已推出 PCIe Gen 6 retimer/交換器，Marvell、Credo 為競爭者。","source":"Yahoo Finance, Astera Labs Battles Nvidia And Broadcom As AI Chip Market Heats Up; ServeTheHome, Broadcom Fires a Shot at Astera Labs with New PCIe and CXL Retimers","url":"https://finance.yahoo.com/news/astera-labs-battles-nvidia-broadcom-182512569.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-13","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"公司 2026 年 10-Q 風險因素列示競爭、產業整併、依賴第三方技術及產品價格隨時間下降；搜尋未發現 2026 年有具體替代品奪取份額的報告。","source":"Astera Labs Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000035/alab-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"2026-10-13","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 說明公司直接銷售並透過經銷商銷售；經銷商主要負責履約與物流，而非銷售、行銷或技術支援，無通路結構性轉變的記載。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"We sell our products directly to our customers and through distributors. Our distributors are primarily focused on fulfillment and logistical purposes, rather than selling, marketing, or providing technical support for our products.","as_of":"2026-02-20","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"經銷商依半導體業常見的 DPA 計畫取得折讓，並有標準價降價時的價格保護credit。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"Sales to most distributors are made under programs common in the semiconductor industry whereby distributors receive DPAs to meet individual competitive opportunities.","as_of":"2026-02-20","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 約 2026-07-31 快照：23 位分析師（18 Buy、5 Hold），平均目標價約 $246；當時股價 $311.23，平均目標價低於當時股價約 19%。目標價均值相對近期個別調升顯得偏舊。","source":"Benzinga ALAB price-targets page","url":"https://kr.benzinga.com/quote/ALAB/price-targets","excerpt":null,"as_of":"2026-07-31","retrieved_at":"2026-10-13","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"個別目標價：Barclays 於 2026-07-20 調升至 $325；Susquehanna 於 2026-07-31 調升至 $275 並維持 Neutral。","source":"Benzinga ALAB price-targets page","url":"https://kr.benzinga.com/quote/ALAB/price-targets","excerpt":null,"as_of":"2026-07-31","retrieved_at":"2026-10-13","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 2026-08-04 公布 Q2：營收創高 $392.4M，年增 104%；Q3 營收指引 $540M–$560M，前一季指引為 $355M–$365M。Benzinga 統計 2024-05-07 至 2026-08-04 共 10 次指引更新、9 次上調。","source":"Benzinga ALAB earnings-forecasts; Trefis 2026-08-06","url":"https://www.trefis.com/articles/610418/astera-labs-beat-and-guided-higher-then-fell-because-the-rally-came-first/2026-08-06","excerpt":null,"as_of":"2026-08-04","retrieved_at":"2026-10-13","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"財報後股價下跌約 12%（Trefis 歸因於財報前已先漲）；Q3 躍升取決於 Scorpio X-Series 320-lane fabric switch 的單一部署時程。另有 Q3 EPS 指引 Benzinga 列 $1.16–$1.21（非GAAP），Simply Wall St 列 GAAP $0.87–$0.92，兩者口徑不一致、未能釐清。","source":"Trefis 2026-08-06; Benzinga earnings-forecasts","url":"https://www.trefis.com/articles/610418/astera-labs-beat-and-guided-higher-then-fell-because-the-rally-came-first/2026-08-06","excerpt":null,"as_of":"2026-08-06","retrieved_at":"2026-10-13","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 指引毛利率約 73%（Q1 為 76.4%），約 200bp 下滑來自與關鍵客戶的非現金 warrant 協議（TIKR）。","source":"TIKR blog","url":"https://www.tikr.com/blog/astera-labs-stock-is-trading-at-all-time-highs-here-is-what-could-drive-it-even-higher?","excerpt":null,"as_of":"2026-07-28","retrieved_at":"2026-10-13","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共9份，僅1份含重大項目（2026-02-10 Item 1.01：與 Amazon 簽 Transaction Agreement 及 warrant，最多 3,262,299 股、履約價 $142.82，對應最多 $65 億採購）；無 1.02／1.03／2.01／2.05／4.02 等併購、重編類項目。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001736297&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-02-05 Astera 與 Amazon 簽 Transaction Agreement 與 Warrant Agreement，warrant 最多 3,262,299 股、履約價 $142.82，依 Amazon 採購達 $65 億分批 vest。","source":"SEC EDGAR 8-K Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/1736297/000110465926012606/tm265461d1_8k.htm","excerpt":"On February 5, 2026, Astera Labs, Inc. (the “Company”) and Amazon.com, Inc. (“Parent”) entered into a Transaction Agreement (the “Transaction Agreement”) and the Company entered into a Warrant Agreement with Amazon.com NV Investment Holdings LLC (“Warrantholder”), to acquire up to an aggregate of 3,262,299 shares of common stock","as_of":"2026-02-10","retrieved_at":"20261108","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Astera 收購 aiXscale Photonics GmbH（光纖—晶片耦合技術），2025-10 宣布，2026-01-12 完成，條款未揭露。","source":"Nasdaq／Zacks 文章 ALAB Expands Portfolio on Acquisitions（搜尋摘要）","url":"https://www.nasdaq.com/articles/alab-expands-portfolio-acquisitions-whats-ahead-stock","excerpt":null,"as_of":"2026-01-12","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Astera 收購 aiXscale Photonics GmbH，2026-01-12 完成，條款未揭露。","source":"Nasdaq／Zacks 文章 ALAB Expands Portfolio on Acquisitions（搜尋摘要）","url":"https://www.nasdaq.com/articles/alab-expands-portfolio-acquisitions-whats-ahead-stock","excerpt":null,"as_of":"2026-01-12","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02（非可靠財報）申報，搜尋亦未見 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001736297&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 9 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 1 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ALAB","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":73.89,"operating_margin_pct":25.52,"fcf_margin_pct":22.15,"rd_intensity_pct":33.82},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"CRDO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.07,"operating_margin_pct":31.74,"fcf_margin_pct":27.57,"rd_intensity_pct":21.46},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"MRVL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.21,"operating_margin_pct":16.81,"fcf_margin_pct":18.23,"rd_intensity_pct":25.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"ALAB"},"financial_history":{"ticker":"ALAB","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":79872000.0,"revenue_yoy_pct":null,"gross_margin_pct":73.47,"operating_margin_pct":-75.36,"net_income":-58345000.0,"diluted_eps":-0.447253,"free_cash_flow":-39771000.0,"fcf_margin_pct":-49.79,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":115794000.0,"revenue_yoy_pct":44.97,"gross_margin_pct":68.94,"operating_margin_pct":-25.47,"net_income":-26257000.0,"diluted_eps":-0.172174,"free_cash_flow":-15477000.0,"fcf_margin_pct":-13.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":396290000.0,"revenue_yoy_pct":242.24,"gross_margin_pct":76.38,"operating_margin_pct":-29.29,"net_income":-83421000.0,"diluted_eps":-0.64,"free_cash_flow":102431000.0,"fcf_margin_pct":25.85,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":852525000.0,"revenue_yoy_pct":115.13,"gross_margin_pct":75.69,"operating_margin_pct":20.34,"net_income":219134000.0,"diluted_eps":1.22,"free_cash_flow":281762000.0,"fcf_margin_pct":33.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ALAB/ALAB_Q3_2026_Earnings_Call_20261103.md）

# Q3 2026 Earnings Call
**Astera Labs, Inc.** | Earnings Calls | 2026-11-03

**Operator** (Operator):
Good afternoon. My name is Connor Meek, and I will be your conference operator today. At this time, I would like to welcome everyone to the Astera Labs Q3 2026 Earnings Conference Call. [Operator Instructions]. I will now turn the call over to Leslie Green, Investor Relations for Astera Labs. Leslie, you may begin.

**Leslie Green** (Executives):
Thank you, Connor, and good afternoon, everyone, and welcome to the Astera Labs Third Quarter 2026 Earnings Call. Joining us on the call today are Jitendra Mohan, Chief Executive Officer and Co-Founder; Sanjay Gajendra, President and Chief Operating Officer and Co-Founder; and Desmond Lynch, Chief Financial Officer.
Before we get started, I would like to remind everyone that certain comments made in this call today may include forward-looking statements regarding, among other things, expected future financial results, strategies and plans, future operations and the markets in which we operate. These forward-looking statements reflect management's current beliefs, expectations and assumptions about future events, which are inherently subject to risks and uncertainties that are discussed in detail in today's earnings release and the periodic reports and filings we file from time to time with the SEC, including the risks set forth in our most recent annual report on Form 10-K. It is not possible for the company's management to predict all risks and uncertainties that could have an impact on these forward-looking statements or the extent to which any factor or combination of factors may cause actual results to differ materially from those contained in our forward-looking statements.
In light of these risks, uncertainties and assumptions, the results, events or circumstances reflected in the forward-looking statements discussed during this call may or may not occur, and actual results could differ materially from those anticipated or implied. All of our statements are made based on information available to management as of today, and the company undertakes no obligation to update such statements after the date of this call, except as required by law. Also during this call, we will refer to certain non-GAAP financial measures, which we consider to be important measures of the company's performance. For example, the overview of our Q3 financial results and Q4 financial guidance refer to various non-GAAP financial measures.
These non-GAAP financial measures are provided in addition to and not as a substitute for financial results prepared in accordance with U.S. GAAP. A discussion of why we use non-GAAP financial measures and reconciliations between our GAAP and non-GAAP financial measures and outlook are available in the earnings release we issued today, which can be accessed through the Investor Relations portion of our website. 
With that, I would like to turn the call over to Jitendra Mohan, CEO of Astera Labs. Jitendra?

**Jitendra Mohan** (Executives):
Thank you, Leslie. Good afternoon, everyone, and thanks for joining our third quarter 2026 conference call. Today, I'll cover our Q3 results, market trends and traction across our AI fabric and signal conditioning portfolios. I'll then turn the call over to Sanjay to discuss our long-term growth profile, and Des will cover our Q3 financial results and Q4 guidance. 
Astera Labs delivered outstanding results in Q3 with record revenue of $584.9 million, up 49% sequentially and up 154% year-over-year. Operational execution was strong during the quarter as we've broadened our customer base with new design wins and expanded our intelligent connectivity platform with the launch of multiple new products.
Q3 revenue growth was broad-based, led by the high-volume ramp of Scorpio X-Series for scale-up networks. Scorpio was our largest product family in Q3, with Scorpio X-Series revenue crossing over our P-Series. Together, Scorpio represented over $1 billion in annualized revenues. This is an important milestone in our journey to be a critical rack-scale AI infrastructure solutions provider. 
Since our last earnings call, we have meaningfully expanded our portfolio with a record number of product launches. This includes the launch of Aries 7, the industry's first PCIe Gen 7 copper and optical connectivity solutions, Leo 2 and Leo X-Series smart memory controllers for AI and general purpose use cases, and Orion, our new compute agnostic rack scale architecture targeting enterprise AI and inference applications. Together, these innovations broaden the markets and applications we serve, creating greater value for our hyperscaler and enterprise customers while supporting a diversified long-term revenue growth profile. Our design-in picked up significantly in Q3 at both new and existing customers.
Scorpio is increasingly establishing itself as a diversified AI fabric platform with momentum extending across both X-Series and P-Series portfolios. In Q3, X-Series shipped to two customers across multiple platforms, and we expect to deliver preproduction volumes to additional new customers during the current quarter. The P-Series similarly broadened its footprint across multiple platforms, including 2 U.S. hyperscalers in Q3. 
Beyond AI fabric, we see additional vectors for diversification. Taurus 800-gig solutions are qualified and shipping in volume to our lead customer and are currently sampling across several additional customers. Leo momentum continues with qualifications completed across several customers, including two hyperscalers and we expect to ramp volume shipments in mid-2027. Our custom solutions business is also seeing a substantial increase in design activity as the number of opportunities have broadened over the course of the year with over 10 active engagements. 
Finally, our platform business, anchored by our Orion reference architecture, is generating strong early customer interest with initial shipments expected to begin in 2027. AI infrastructure demand continues to strengthen with our hyperscaler customers reporting strong revenue growth from AI services. Yet the physical inputs, wafer capacity, grid power and memory supply remain tightly constrained.
That combination puts a premium on utilization. At the same time, the workload mix is shifting to inference where continuous reasoning loops multiply the traffic crossing the fabric. Operators now optimize for two things: latency to deliver faster time to first token and accelerator utilization to drive dollars per token. Our Scorpio AI fabric is purpose built for exactly these metrics. As token economics become increasingly important to our customers, let me highlight the differentiated capabilities driving  Astera's success in AI fabric.
First, radix. Our. radix portfolio of Scorpio X devices including the industry's largest 320-lane configuration enables large cluster sizes for PCIe-like scale-up AI fabrics. Scorpio X high lane count helps to maximize scale-up domain sizes while enabling an all-to-all flat topology to allow AI accelerators to communicate at full bandwidth with low latency. This is particularly important for AI inferencing as fewer hops reduce collective communication latency, allowing resources to be spent on compute rather than moving data between switches. Increased utilization results in higher tokens per second and ultimately, greater monetization from the same accelerator investment.
Second, intelligence. Conventional switches just move packets. Scorpio X-Series is AI workload aware and participates in collective communication and computation. Hardware accelerated Hypercast and in-network compute offload AI operations such as all-reduce and broadcast from the accelerators directly into our fabric, delivering up to a 2x improvement in collective performance. Similarly, fabric attached Leo memory controllers for KV cache offload delivered significant improvement in time to first token and tokens per second. By utilizing advanced AI aware capabilities enabled by Scorpio and Leo products, customers can improve token economics and increase token output with the same number of accelerators.
Third, software. COSMOS is a software layer that transforms our AI fabric and smart connectivity solutions into infrastructure that our customers can deploy, manage and operate efficiently at scale. COSMOS software spans our entire portfolio, is broadly adopted across the AI ecosystem and extends from device level diagnostics to fabric and rack management. COSMOS speeds rack deployment by resolving connectivity issues in software instead of costly hardware spins, then keeps rack online with fabric-wide telemetry and predictive fault detection. It also configures and manages Hypercast and in-network compute. So our software directly participates in the AI workload running on XPUs in addition to managing the connectivity infrastructure.
Faster time to revenue and higher utilization of AI infrastructure are the reasons why COSMOS is driving new design wins across our product portfolio. These differentiated capabilities are optimizing performance and increasing XPU utilization, which is rapidly expanding our opportunity funnel and accelerating design win conversion. As a result, we expect to deliver strong diversified growth with our AI fabric portfolio through increasing value to our customers and continued expansion of our dollar content per AI accelerator. Today, our content per XPU across fabric switches and copper signal conditioning can exceed $1,000 per XPU.
We expect our next-generation AI fabric products alone to contribute well beyond $1,000 per XPU. Over time, we aim to address the entire scale-up switching TAM, expanding from PCI Express and NVLink Fusion-based platforms today to systems based on UALink and other protocols. With the addition of memory controller and optical connectivity products, increasing AI fabric attach rates driven by next-generation scale-up protocols, including UALink, larger cluster sizes and higher ASPs associated with each data rate transition, we see a path to doubling our total silicon dollar content per XPU with each new generation of AI platforms.
In summary, Q3 marked another important step in Astera Labs evolution. Record results were led by the high-volume ramp of Scorpio X-Series and continued growth across our signal conditioning portfolio. We also saw a strong design win momentum across new and existing customers and launched a record number of products during the quarter. Looking ahead, we see significant opportunities across optical connectivity, custom silicon, memory solutions and rack scale infrastructure that build on our core franchises, expand our addressable market and position us for long-term growth.  
With that, let me turn the call over to our President and COO, Sanjay Gajendra.

**Sanjay Gajendra** (Executives):
Thanks, Jitendra, and good afternoon, everyone. This quarter was an important inflection point for Astera Labs. We have evolved from a component level supplier into a rack scale infrastructure platform provider. We are now bringing together silicon, hardware and software to solve connectivity challenges across the AI rack and pods over both copper and optical interconnects to improve XPU utilization and higher ROI. As we broaden our intelligent connectivity portfolio, we are increasing our silicon dollar content to thousands of dollars per accelerator across AI and cloud infrastructure while expanding our addressable market opportunity.
Our foundation today comprises of two core revenue-generating franchises, AI fabrics and signal conditioning and is rapidly expanding across four additive market vectors, including optical connectivity, custom silicon, memory solutions and our rack scale infrastructure platforms. As AI systems scale, the challenge is no longer simply connecting more accelerators inside a server. As Jitendra mentioned, customers are building larger scale-up domains that need more bandwidth, lower latency and smarter ways to move data to improve token economics. Our real-world experience deploying scale-up networks in production volume is helping us define workload-specific, high-value feature sets. Based on these factors and increased attach ratios, we believe we can more than double the dollar content per XPU in each subsequent generation.
Signal conditioning remains the critical problem to solve as data rates double and AI clusters scale. As a result, we expect ASPs and attach rates for our new PCIe Gen 7 portfolio across optical and copper to expand versus the prior generation. In addition, our Aries Gearbox and Redriver solutions are expected to address new sockets within AI platforms. Taurus for 800-gig applications began shipping in volume during Q3, and we anticipate solid growth within scale-out Ethernet AECs heading into 2027, driven by higher ASPs and new program ramps. We're also sampling 3.2T retimers to multiple customers.
Looking ahead, we are adding 4 growth drivers that materially expand our addressable market. Starting with optical. We continue to make great progress on our fiber connectivity business. At OCP last month, introduced our first optical products, including Smart Optical Drivers and TIAs optimized for scale-up PCIe Gen 7 topologies, addressing near-packaged and linear pluggable optics applications. We also demonstrated integration of our optical technology with our Scorpio X-Series fabric switches. Our smart TIAs and laser drivers will begin sampling this quarter to select hyperscaler and OEM partners for NPO applications, and we are actively working with multiple customers to extend PCIe fabrics beyond the rack to the pod level.
With near-packaged optics for scale-up application, we see our TIAs and drivers unlocking additional content opportunity per XPU and we expect these optical products to begin initial revenue contribution in late 2027. Longer term, we are fully -- we are developing fully integrated optical engines with the goal of building an optically enabled Scorpio X-Series fabric switch. In 2030, we estimate the scale-up optics interconnect opportunity to be a $40 billion market, which we will service through our high-density fiber attach solutions and optical engines for NPO and CPO applications.
Moving to custom solutions. The AI accelerator landscape continues to broaden and diversify, driving demand for purpose-built intelligent connectivity. Interest and activity for our custom offerings have accelerated in 2026, and we are engaged with 10-plus opportunities now. We are developing custom fabric solutions, custom memory controllers for specialized inference applications and IO chiplets for next-generation accelerator platforms. We expect initial shipments of these solutions to commence in late 2027 and ramp to volume in 2028. We are being selective and focusing on high-value custom programs looking to leverage our deep portfolio of connectivity IP, robust supply chain partnerships and system-level expertise.
Next is our memory solutions business where we recently expanded our Leo smart memory controller family to address new applications and use cases. Leo X-Series is our new fabric attached memory controller that pairs with our Scorpio X-Series AI fabric to create a dedicated memory tier for KV caches and agent context. We also introduced Leo 2 E-Series and P-Series which double memory bandwidth and capacity versus the prior generation and support both DDR4 and DDR5 DIMMS. As memory constraints intensify, Leo lets customers expand memory capacity, pool standard memory across a rack and reliably reuse previously deployed DDR4 alongside new DDR5 DIMMS. Engagement and design activity remains strong across a broadening set of hyperscaler and inference cloud customers.
I'm happy to report that Leo 2 products are now shipping in preproduction volume with high volume ramp projected in mid-2027.
Turning to platform solutions, we recently announced Orion, our compute agnostic rack-scale reference architecture built to enable turnkey AI infrastructure solutions for inference, cloud and enterprise customers. Orion spans 6 production-ready reference designs, scales from 8 to 160 accelerators per cluster and integrates with COSMOS, our software management platform that is now enhanced to include rack and fabric manager functionality. These reference designs leverage our portfolio of intelligent connectivity solutions, including AI fabric, smart signal conditioners, advanced memory solutions and COSMOS to provide a tightly integrated, highly-performing platform. We are already seeing substantial interest from GPU and XPU suppliers and Orion is on track to enter the market through our ODM and OEM partners in 2027. Fully loaded Orion rack scale designs contain greater than $100,000 in Astera Labs content, creating another large additive market opportunity.
In conclusion, we remain focused on execution and delivering substantial value to our AI and cloud infrastructure customers across silicon, hardware and software. Design activity accelerated with wins across a broad set of programs and applications at multiple customers. Finally, a record number of product launches is broadening our portfolio, creating deeper synergies across our solutions and expanding both our market opportunity and silicon dollar content per AI platform.
With that, let me turn the call over to Des.

**Desmond Lynch** (Executives):
Thank you, Sanjay, and good afternoon, everyone. Today, I will review our Q3 financial results and then discuss our Q4 guidance, both presented on a non-GAAP basis. We delivered outstanding third quarter results with record revenue of $584.9 million, up 49% sequentially and 154% year-over-year. Growth was broad-based across our AI fabric and signal conditioning portfolios led by the volume ramp of Scorpio X-Series. Revenue also diversified across a broader base of customers and platforms during the quarter. Scorpio became our largest product family by revenue in Q3, also with X-Series revenue surpassing P-Series. X-Series revenue increased significantly as shipments expanded across multiple platforms and radix configurations while P-Series also grew sequentially as existing deployments expanded and new programs entered production.
Within signal conditioning, Aries growth was led by strong PCIe Gen 6 adoption across scale-up and scale-out applications, while Taurus also gained momentum as our 400-gig and 800-gig solutions ramped across scale-out applications.
Non-GAAP gross margin for the third quarter was 72.4%, above our guidance of 72%. Non-GAAP operating expenses for the third quarter were $162 million, up 19% sequentially, reflecting continued R&D investment to expand our addressable market across our core franchises and emerging growth sectors. Non-GAAP operating margin for the third quarter was 44.7%, up from 39.1% in the prior quarter, an increase of 560 basis points, reflecting significant operating leverage as revenues scaled.
Interest and other income was $13 million, and our non-GAAP tax rate was 11.4%. Non-GAAP net income was $243.4 million, resulting in non-GAAP diluted earnings per share of $1.32 up $0.52 or 65% sequentially from Q2. We ended the quarter with $1.38 billion in cash, cash equivalents and marketable securities, an increase of $125.3 million from Q2. The increase was primarily driven by record cash from operations of $179.2 million. 
Now turning to our outlook for the fourth quarter. We expect revenue to be in the range of $730 million to $750 million. At the midpoint, this represents 27% sequential growth. Growth is expected to be driven by the continued expansion of Scorpio X-Series and P-Series across both customers and platforms. Signal conditioning growth is expected to be led by PCIe Gen 6 Retimer adoption in Aries and the ramp of Taurus 800-gig solutions.
We expect fourth quarter non-GAAP gross margin to be approximately 72%. We expect fourth quarter non-GAAP operating expenses to be between $194 million and $200 million, reflecting continued investment in our core AI fabric and signal conditioning portfolios as well as additional investments in the growth opportunities outlined by Sanjay. We expect non-GAAP operating margin to be approximately 45%. Interest and other income is expected to be approximately $13 million and we expect our non-GAAP tax rate to be approximately 12%. We expect our Q4 share count to be 187 million diluted shares outstanding. Overall, we expect non-GAAP fully diluted earnings per share to be between $1.62 and $1.66.
In closing, Q3 was an exceptional quarter, marked by record revenue, significant operating leverage and the strategic milestone of Scorpio becoming our largest product family by revenue. Looking ahead, our growth drivers continue to broaden. Scorpio X-Series and P-Series are scaling across new and existing customers and platforms. In signal conditioning, Aries and Taurus are benefiting from growing adoption of next-generation connectivity standards. Beyond our core franchise, opportunities are emerging across optical, custom, custom memory and platform solutions, reflecting the strategic R&D investments we have made to expand our portfolio into addressable markets. We will continue to invest across our portfolio, execute with discipline, maintain strong profitability and deliver long-term value for our stockholders.
This concludes our prepared remarks. I will now turn the call back to our operator to begin Q&A. Operator?

**Operator** (Operator):
[Operator Instructions]. Your first question is from the line of Harlan Sur of JPMorgan.

**Harlan Sur** (Analysts):
As always, great execution by the team. On the new Orion rack-scale reference architecture, as large corporations like ours start to evaluate open source, open weight models on-premise for lower token inferencing cost, control on things like model fine-tuning. I guess more importantly, like internal data security. These customers are looking for compute platforms that can fit into their private data center architectures, like air cooled, compact cluster sizes, flexibility on XPU, CPU supported. Orion seems to be that sort of perfect solution. So what's been the interest level? Have you engaged with large enterprises? And what's the Astera dollar content capture across the different configurations you offer?

**Sanjay Gajendra** (Executives):
Great question, Harlan. Thank you so much. No, we are very excited with Orion. Like you correctly pointed out, enterprise AI is something that is a significant market. It's a very fragmented market with different workloads and all of them need compute in a form factor that is readily available, but more importantly, it is workload specific. So what we have developed with Orion is that it's a GPU-agnostic rack, meaning you can bring any GPU that you want that suits your workload or based on availability and things like that. The rest of the infrastructure is all defined, meaning the connectivity is all defined as part of the reference design, the power, the cooling and other components that are essential. 
What Astera is providing are three main things. We are providing the entire reference architecture, whether it's at a box level or rack level. We're providing baseboards that utilize our silicon. That combines the fabric solutions, the memory solutions, the signal conditioning and other components that are required in a well-optimized, fully-tuned and fully-validated way. And then we're providing the software, which we are excited about because COSMOS has now gone from being a device level software to being a rack level and fabric level. So it manages all the fabric, it manages the rack level, diagnostic and other aspects that are involved in orchestrating the GPU performance. 
So overall, this Orion is squarely addressing use cases like you outlined and the Orion family will have multiple generations of it which will obviously have higher and higher content. But the initial platform that we call Orion 1.0, that's based on PCIe scale-up, we estimate about $100,000 of Astera content that will be monetized through components, through boards and software.

**Operator** (Operator):
The next question is from the line of Joe Moore of Morgan Stanley.

**Joseph Moore** (Analysts):
And congratulations. Can you talk about Scorpio X? You hit the $1 billion threshold. It's been such a steep ramp. Do you anticipate that there could be kind of a plateau as the products that Scorpio X is in sort of matures before you get to UALink? Or just help us out a little bit with what that progression may look like. And it seems like you're anticipating a sort of long tail for PCI Express, but also this transition to other protocols. Can you just talk about that dynamic?

**Desmond Lynch** (Executives):
Joe, it's Des here. Thanks for the question. We've been really pleased with our sort of execution throughout 2026, which really has shown broad-based strength across the portfolio. If you look at our growth in the second half of the year, this has really been led by scale-up deployments and the production volume ramp of Scorpio X-Series, which started in Q3 and will continue into Q4. This led to us being able to deliver almost 50% revenue growth in Q3. And using the midpoint of our guidance for Q4, we do expect to see a further 27% sequential growth. If I look further ahead, what I would say is that the initial Scorpio X platforms have completed much of their initial deployment ramps, and they'll be contributing at scale going forward. 
We expect Scorpio X to continue to grow driven by new platforms and also additional customers layering into the model throughout 2027. And then if I look further ahead, given their experience with high scale deployment, advanced feature sets and our strong relationships with our customers, we are very well positioned for the next-generation platform growth. And certainly, beyond Scorpio, we're excited about the growth opportunities as we outlined in the call, earlier, we continue to see growth in the new product periods of Aries 7, Leo and optical products, which will all start layering into the model in 2027 and offer future growth opportunities. So overall, we're very pleased with our performance and overall momentum that we have across our portfolio.

**Operator** (Operator):
Your next question is from the line of Blayne Curtis with Jefferies.

**Blayne Curtis** (Analysts):
Nice results here. I wanted to ask on NPO. You mentioned some design progress there. You had some new parts at OCP on the analog side. Can you just maybe walk us through kind of how we should think about all these different components layering in? And is there designs that you're working on for the full NPO solution now? Or is that a bit later?

**Sanjay Gajendra** (Executives):
Absolutely now, Blayne. So we -- as we noted in the prepared remarks, we are planning to start sampling our NPO products to lead customers this quarter. We do expect roughly about 6 months of qualification and system-level integration and all that. So we do expect that revenue will start contributing towards the second half of 2027 from NPO deployments. And these are, again, components that we're servicing for going inside the NPO module, the TIAs and laser drivers and so on. So we do expect hundreds of dollars to come in per accelerator with the NPO type of products and solutions that we're building. Going forward, NPO, we do expect to continue to drive the growth beyond 2027 with CPO volumes coming in probably mostly in the '28-'29 time frame.

**Operator** (Operator):
The next question is from the line of Papa Sylla of Citi. My apologies, the next question is from the line of Tore Svanberg of Stifel.

**Tore Svanberg** (Analysts):
Congrats on another record quarter. So you've got these four new big growth engines, and I agree, these are huge TAMs. You also stepped up the -- or you're going to step up the OpEx quite a bit here in the December quarter. I'm just curious, should we think of a lot of the OpEx for these 4 new business opportunities? Is that still on the come? Or have you already made a lot of heavy lifting to target those 4 opportunities?

**Desmond Lynch** (Executives):
Tore, it's Des here. We continue to invest in the business at the right level to support the high growth opportunities ahead of us. You are correct. We did see the OpEx step up to about $162 million in Q3. We expect it to continue to grow into sort of Q4. But what I would point out is that our OpEx is growing slower than our sort of revenue growth. So you're seeing a significant leverage within the model. I would say that our OpEx growth is really driven by sort of three factors in the second half of the year. We continue to grow our head count to support our customer programs. Our head count has doubled year-over-year from here. 
Secondly, I would say that we've seen additional variable R&D expenses in the form of wafers, [masks] and IP expenses. And then lastly, as we continue to outperform our P&L model, we are seeing some higher variable comp from there. But again, what I would really reiterate is that we are seeing the significant leverage within the model. I think going forward, the right way to think about OpEx in the longer term is around 30% of revenue. We're certainly underperforming that today given the high revenue growth that we're seeing.

**Operator** (Operator):
The next question is from the line of Ananda Baruah of Loop Capital.

**Ananda Baruah** (Analysts):
Congrats on the progress. I guess, question clarification. You guys mentioned a couple of times of doubling the content for XPU with each new generation of platform. And I guess the question clarification is, is it each new generation of XPU? Or is it each new generation of Astera Labs like Gen 7, Gen 8? Or is this something else? I would just love to get context around how to think about that?

**Jitendra Mohan** (Executives):
Ananda, great question. This is Jitendra. So if you look at the content that we have in some of the highly loaded systems today, it already exceeds $1,000 of content on a per XPU basis across our fabric switches and signal conditioning products. As we go to the next generation of our products, we aim to add $1,000 plus content just from switching opportunity on a per XPU basis. So that kind of gets you to the first doubling as we speak. Then beyond that, as we go to the next generation of AI platforms or the next generation of XPU, we bring in additional content to bear on these platforms, which includes, for example, optical networking components that Sanjay just talked about. Leo memory controllers for KV cache offload and so on as well as growing cluster sizes that drive higher ASP on a per product basis as well as higher data rates that also drive higher ASP on a per product basis. So if we model all of this out, we expect to get double the content on a per XPU basis on each successive generation of XPU.

**Ananda Baruah** (Analysts):
Oh boy, that sounds like a lot of content, Jitendra. I appreciate it, guys.

**Jitendra Mohan** (Executives):
Yes, our customers continue to build larger and larger cluster sizes. And as these cluster sizes go bigger, we get a higher attach rate. Thank you.

**Operator** (Operator):
The next question is from the line of Papa Sylla of Citi.

**Papa Sylla** (Analysts):
Congrats on the very strong results. So maybe Jitendra or Sanjay, I just wanted to double click a little bit on the prior 10-plus Scorpio X engagement you previously talked about. Any color on how many of those you expect to be meaningful ramps in the first half of '27? And maybe tied to that, how are you still thinking about UALink time line? Do you still kind of see more of a kind of second half '27 story? And if that's the case, is it reasonable to assume that some of your current Scorpio X engagement will kind of turn into UALink engagement or opportunities?

**Sanjay Gajendra** (Executives):
Yes. Thanks for the question. So what we had guided was that there are more than 10 customers we are engaged on Scorpio X. So that -- those engagements continue to make progress in a very positive way. What we noted was that we, of course, have our lead hyperscaler platform that's now in production. That's reflected in the Q3 numbers. And also on the guide that we provided for Q4. What we also noted is in Q3, we started shipping the X-Series Scorpio to an additional hyperscaler. So that's now in preproduction. So that should help us generate revenue in 2027. 
We do have backlog from multiple additional customers in Q4 for Scorpio X. So these are parts that will get shipped out this quarter, and then it will go through its development and qualification phases in the first half of '27 and contributing revenue in the second half. Now what is also happening is that because of all the results and performance that we are able to deliver to our customers with Scorpio X with many of the unique features that we highlighted in our prepared remarks, the customers that have designed in are now adding new platforms or essentially using Scorpio X on new platforms. 
So not only are we growing the number of customers that are adopting Scorpio X, we're also seeing customers rapidly expanding the use of Scorpio X in multiple platforms that they're developing. So overall, I want to say the -- this Scorpio X has taken off very well, reflected both in the pipeline opportunities as well as the revenue that we highlighted with Scorpio family exceeding $1 billion of annualized run rate in Q3.

**Jitendra Mohan** (Executives):
Maybe let me take the UALink question. So we continue to see the UALink ecosystem strengthen. There is more IP available. There are more vendors that are coming in with products for UALink. So overall, there's not a lot of change in the UALink from a customer standpoint. The customers who had focused on memory semantic-based protocols such as PCI Express continue to stay in that swim lane and will, as you said, over time, convert to UALink. Our development of UALink products also continues. We introduced our Taurus family earlier this year, and we continue to work on the anchor sockets on switching and so on, in order to intercept them with the release of the UALink XPUs from our customers. 
So not much has changed. Those who are in the UALink swim lane will continue there. Those who are in the Ethernet swim lane will continue in that swim lane. Overall, our strategy is to address the entire scale of switching TAM. We have started with PCI Express, gone on to the NVLink Fusion and actively working on UALink. And as we start to see more customer interest, we will address other protocols for scale up as well.

**Operator** (Operator):
The next question is from the line of Sebastien Naji of William Blair.

**Sebastien Cyrus Naji** (Analysts):
I want to stay on the theme of Scorpio in particular, but maybe ask a little bit about the P-Series, or Scorpio X-Series revenue crossed P-series in the quarter. Can you maybe just comment on how we should think about the growth in P-Series in Q4 and in 2027. It seems like X-Series has maybe more significant content, but is more concentrated while P-Series is perhaps lower content, but has a broader set of customers. So just how should we think about the mix between those two products going forward?

**Desmond Lynch** (Executives):
Sebastien, it's Des here. We've been really pleased with our performance in Scorpio P-Series. In the third quarter, it grew double-digit sort of growth and I expect that to continue in Q4 at a similar sort of rate going forward. As we continue to look further ahead into sort of next year, what we continue to see is the hyperscalers continuing to grow. We talked about having two hyperscalers growing in revenue in the second half of this year. So that will continue to grow into next year. We continue to see a variety of engagements across different customers that continue to ramp. So we've seen this being -- continue to be a meaningful part of the overall sort of Scorpio ramp. 
Obviously, Scorpio X-Series, given the higher ASPs, that's going to be the sort of dominant sort of growth driver going into next year. But P-Series continues to perform really well.

**Operator** (Operator):
The next question is from the line of Quinn Bolton of Needham.

**Quinn Bolton** (Analysts):
My congratulations on the outlook. I just wanted to ask a longer-term question. You gave us sort of four new product categories on the call, optical, custom, the memory controller expansion, and then the Orion rack-level platforms. And I won't hold you to it, but of those four, would you say one is more likely than the others to hit 10% of revenue at some point over the next couple of years? Or how should we think about the relative growth rates of those four new opportunities?

**Sanjay Gajendra** (Executives):
Yes. So what I would start off by saying is that all the four are significant TAMs, as you can imagine, with optical or the memory inferencing use cases. Custom is a huge opportunity out there, both for XPU attach and some of the other XPU-like opportunities. So for us -- and of course, the rack is going into several enterprise and inference applications, the value proposition and form factor there is very different. So I would say, if you start off, these are all big markets for us. So now it comes down to how are we able to develop the right product, make sure that we execute and deliver.
And it's a matter of timing is what I would say. In other words, the most near-term opportunity that we're expecting in second half is all the optical ramp that we're expecting specifically on the NPO side. So that is something that will have the most immediate effect from a revenue contribution standpoint. Custom silicon, that one is a muscle that we have been building and making a lot of progress. Like we noted, we have 10 engagements right now for doing custom fabrics, custom memory controllers and so on. So this one, I would say, is going to be a significant opportunity for us, but I would say probably more in the 2028 time frame. And the last one, the Orion is, to be candid, it's been like fantastic reception since we announced it at OCP. A lot of folks are coming to us, especially enterprise folks and folks that are building XPUs and other accelerators. 
So that one, we will start launching the product, of course, through ODM and OEM partners that are building the system for us. So that will start contributing revenue in '27. We're yet to sort of get a full handle on exactly what that number would look like for the Orion platform. So we expect to provide more concrete data on that in our next quarterly call. But in general, the key message here is that all of these are substantial market opportunities. They all require innovation and execution that we have proven ourselves to be able to deliver as a company.
So we are looking forward to playing in all this market and contributing additional growth engines to go along with the signal-conditioning franchise we have and the fabric franchise that we have. So overall, if we can have 6 engines that are all pumping out great growth, I think we will have achieved the goal of being a great iconic company.

**Operator** (Operator):
The next question is from the line of Karl Ackerman of BNP Paribas.

**Samuel Feldman** (Analysts):
This is Sam Feldman on for Karl Ackerman. So you're seeing strong growth with Aries. Can you delineate this growth between content uplift from the transition to PCIe Gen 6 versus unit growth? And more generally, how do you think about your retimer content per XPU as optics moves closer to compute?

**Jitendra Mohan** (Executives):
Yes, it's a great question. We had a record quarter for Aries and Aries family continues to grow. We started the company actually with Aries PCI Express Gen 4. And now we are going to Gen 5, Gen 6. And at OCP, we launched our Gen 7 portfolio. And as you correctly pointed out, there are two factors that are causing the ASP to go up. One is just the increase in data rates. So every time we double the data rate, we can expect to get a 20%, 25%, 30% increase in ASP from generation to generation. The other factor is that we also ship these devices in multiple form factors, so you have the chip-down opportunity where the chip is directly soldered on the board, but we also have the smart cable modules where the chip is soldered in the form of a PC board that gets then built into an active electrical cable and there we get higher ASPs. And just as importantly, we have these active electrical cables attaching into the scale-up part of the network. And therefore, we get a higher attach rate and overall growth in revenue. At the high level, I would say that we've been very happy with the growth of the Aries family. It continues to grow. It's grown from '24 to '25 to '26, and we expect it to grow in '27 as well. 
So the last point that you made is some of these links that were previously served with copper will get served with optics as we go into the next generation. And there is an opportunity for us to have even higher content because the dollars that we can get on a per link basis on optical links is much more than what we get on copper. In addition to that, there were several links that previously did not require any kind of retimers at all, which will now require both copper as well as optical content. And that's a great opportunity for us to continue growing the Aries portfolio.

**Operator** (Operator):
The next question is from the line of Simon Leopold of Raymond James.

**Jeffrey Koche** (Analysts):
Jeff Koche in for Simon. Just wanted to ask you a quick question on the Marvell-Lumentum merger. Obviously, you're trying to bring silicon and photonics closer together, potentially enabling tighter co-design and improved power. I just want to get your take on this strategy. Do you think that this can provide a competitive advantage in -- and does it change how you are viewing your -- how you're going to vertically integrate?

**Jitendra Mohan** (Executives):
Marvell and Lumentum are both great companies. We have good respect for both of them. So I'm sure they have thought through the strategy before getting into this combination discussion. So I'll let them comment kind of what they think about it. But I'm happy to talk about our own strategy for optical. So our strategy for optical is more grounded in scale-up, right? Unlike the other companies, we are not yet focused on scale-out or scale across. 
Our focus on scale up, which is not a big TAM today. But as we talked about during the prepared remarks, we expect that to be a $40 billion TAM going forward. And all of the components that we need to address that TAM, we are building ourselves starting with the electrical ICs, laser drivers and TIAs for the NPO generation and more complex EICs for the CPO generation. At OCP, we also showed our silicon photonics that goes into some of these NPO modules as well as the connectors that allow us to build full optical engines for NPO as well as CPO. These optical engines will then get deployed with our hyperscalers and hyperscalers will continue to source laser components just like they do today with their existing vendors.

**Operator** (Operator):
The next question is from the line of Tom O'Malley of Barclays.

**Robert Smith** (Analysts):
This is Trip Smith on for Tom O'Malley. I was just curious if you could talk about the cadence of revenue growth into calendar year '27. I think there are some expectations that your lead customers' current generation builds are kind of peaking out in the 1Q time frame. And then the next gen is not really expected to ramp until kind of closer to calendar year '28. So any color there would be super helpful.

**Desmond Lynch** (Executives):
Des here. Thanks for the question. Obviously, we will not comment upon our end customers' volume sort of. I think I addressed some of this sort of earlier in the Q&A when I talked about our sort of -- the large scale that we've been able to generate on the Scorpio X platforms. The initial deployment is taking place, and they'll continue contributing in scale sort of going forward and we'll continue to see new platforms plus additional customers layering into the model on a go-forward basis. I think it's important just that we also remember the scale that we've been able to generate in terms of our Scorpio X family. I think Jitendra talked about a $1 billion sort of run rate being achieved in sort of Q3. And we're optimistic about our growth prospects going forward as we go into next-generation platforms as well.

**Operator** (Operator):
The next question is from the line of Bastien Falcon of Susquehanna.

**Bastien Faucon-Morin** (Analysts):
I'm filling in for Mehdi Hosseini. I guess I wanted to come back to your comments about the content that you're capturing by Orion rack-scale designs. You mentioned that you captured about $100,000 of content per rack. In your press release, you highlighted that those parts have from 8 accelerators to 160. So I wanted to know a little bit more about how to think about that $100,000? How many GPUs or accelerators are you taking into consideration for that estimate? And then my follow-up would be, how should we think about the gross margin profile of the rack scale solutions relative to your long-term gross margin targets of 70%?

**Sanjay Gajendra** (Executives):
Yes. So let me try to break it down for you. So the Orion rack is designed to support up to 10 compute trays. Each compute tray can have up to 8 GPUs or accelerators that are plugged in. So our content, which includes the fabric, the switches and so on, they reside at the compute tray level to interconnect the GPUs. So we do have content there. Now some customers rather than operating the 10 compute trays individually, they want to create a larger cluster, meaning operate the 80 GPUs as 1 unit. For that, they need a scale-up switch and a tray as well. So in those situations, there is additional hardware that is required.
And of course, when you think of 160 GPUs, we're talking about two racks that are talking to each other in a -- with connectivity going from the East to West type of topologies. So in general, if you think about that kind of system, then the components that we are able to integrate in that includes, of course, all of our fabric and switch products both at the compute tray level and at the rack level. It includes all of our signal conditioning products, retimers and such that would be required, including AECs, right? And then we are also, for the first time, monetizing our COSMOS software.
So COSMOS software, like I noted, has upgraded from being a component level solution to a rack-level solution, a fabric manager and so on. So that provides additional monetization points that adds to the $100,000 that I noted. And then the last point I would make is that, again, we are providing this as production-ready reference design. So obviously, there's a certain amount of royalty that we get from our OEM and ODM partners that are taking that and providing it to their end customers, the enterprise AI and inference cloud guys. 
So all in all, there are 3 monetization points. It's the base boards that we sell. It's the software that we sell and royalty that we get for the reference design. So that's the way to think about how the monetization happens. When we said $100,000, we're just talking about 1 rack, meaning 80 GPUs, even though the reference design itself can support up to 160. The $100,000 refers to a single rack. So that's the other point I want to emphasize. And overall, like I noted, this is just the beginning of the Orion story, meaning we'll have additional versions that brings in UALink and liquid cooling and all that stuff. So in general, we do expect that we'll be able to add more value by doing a vertical integration of the components and software. 
And in terms of the margin itself, we do expect this to be accretive just given the business model that I noted, where we are not only providing silicon, but we are providing software and there is additional revenue coming in through the royalty approach that we're taking. So overall, it's meant to bring in top line. It's meant to be accretive to the margin that we have. But I will also like to call out and say this is early days for this platform. The interest has been great. We will, of course, keep updating you guys on how the business is growing. And I think in Q1, we'll be able to provide lot more details on the impact for our overall P&L.

**Operator** (Operator):
There are no further questions at this time. I will now turn the call back over to Leslie Green for closing remarks.

**Leslie Green** (Executives):
Thank you, everyone, for your participation and questions. And please refer to our Investor Relations website for information regarding upcoming financial conferences and events. Thank you so much.

**Operator** (Operator):
This concludes today's conference call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ALAB_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Desmond Lynch｜guidance：Q3營收財測區間下緣$540M（上緣$560M，中點季增40%）（原話："We expect revenue to be in the range of $540 million"）
- 2026-08-04｜Desmond Lynch｜guidance：Q3 non-GAAP毛利率財測約72%（原話："third quarter non-GAAP gross margin to be approximately 72%."）
- 2026-08-04｜Desmond Lynch｜guidance：Q3 non-GAAP營業利益率財測約43%，季增400bp（原話："approximately 43%, up 400 basis points sequentially"）
- 2026-08-04｜Desmond Lynch｜guidance：Q3 non-GAAP營業費用財測$156–160M（原話："between $156 million and $160 million."）
- 2026-08-04｜Desmond Lynch｜guidance：Q3 non-GAAP稀釋EPS財測$1.16–$1.21，稀釋股數約1.85億（原話："non-GAAP fully diluted earnings per share to be between"）
- 2026-08-04｜Jitendra Mohan｜guidance：Scorpio Q3成為最大產品線，比先前預期早一季（原話："Scorpio to become our largest product family in Q3, which is"）
- 2026-08-04｜Sanjay Gajendra｜guidance：Scorpio X領先客戶Q3量產爬坡並超越Scorpio P營收（原話："at least for a lead opportunity and lead"）
- 2026-08-04｜Desmond Lynch｜margin：Q2 non-GAAP毛利率73.7%，高於財測73%（原話："gross margin for the second quarter was 73.7%, above our"）
- 2026-08-04｜Desmond Lynch｜margin：Q2 non-GAAP營業利益率39.1%（原話："Non-GAAP operating margin for the second quarter was 39.1%,"）
- 2026-08-04｜Desmond Lynch｜margin：Scorpio平均毛利率大致與公司整體相當（原話："margin profile broadly in range with our sort of corporate"）
- 2026-08-04｜Desmond Lynch｜margin：毛利率長期目標78%（原話："trend towards a long-term target of 78% from here"）
- 2026-08-04｜Desmond Lynch｜margin：毛利率區間擴大，主因矽片對模組營收組合（原話："a wider range of gross margins with the main impacts being"）
- 2026-08-04｜Desmond Lynch｜capital_allocation：Q2 non-GAAP營業費用$135.8M，季增10%（原話："were $135.8 million, up 10% sequentially,"）
- 2026-08-04｜Desmond Lynch｜capital_allocation：現金及有價證券$1.25B，較Q1增$68.5M（原話："totaling $1.25 billion, up $68.5 million from Q1"）
- 2026-08-04｜Sanjay Gajendra｜capital_allocation：CXL方向持續重押投資（原話："we are investing heavily in coming out with"）
- 2026-08-04｜Jitendra Mohan｜product：PCIe 6占Q2營收逾50%（Q1約1/3）（原話："representing more than 50% of our total revenue driven"）
- 2026-08-04｜Sanjay Gajendra｜product：Scorpio X單獨內容價值預期遠超每XPU $1,000（原話："alone to grow well beyond $1,000 per XPU"）
- 2026-08-04｜Jitendra Mohan｜product：新200G Taurus產品使Taurus TAM於2030年超過$40億（原話："portfolio market opportunity to over $4 billion by 2030."）
- 2026-08-04｜Sanjay Gajendra｜product：Gen 5 Aries持續時間超出預期（原話："the surprise is how long Gen 5 has continued, and"）
- 2026-08-04｜Jitendra Mohan｜product：COSMOS由遙測診斷擴展為編排層（原話："now we are becoming part of the orchestration layer."）
- 2026-08-04｜Jitendra Mohan｜product：CXL新增一個美國超大規模客戶標準Leo設計案（原話："we closed a new design win with our standard Leo memory"）
- 2026-08-04｜Sanjay Gajendra｜commitment：UALink版Scorpio X交付時程2027（原話："on track to deliver UALink-enabled Scorpio X-Series"）
- 2026-08-04｜Sanjay Gajendra｜commitment：NPO晶片組目標2027量產（原話："targeted for 2027 production."）
- 2026-08-04｜Sanjay Gajendra｜commitment：客製方案首批出貨2027（原話："custom design wins to commence in 2027."）
- 2026-08-04｜Jitendra Mohan｜commitment：2027對兩家美國超大規模客戶量產出貨Leo CXL（原話："we expect to ship both standard and custom Leo CXL memory"）
- 2026-08-04｜Sanjay Gajendra｜customer：Scorpio X有逾10家客戶接洽（原話："We have over 10 customers engaged on the Scorpio X itself."）
- 2026-08-04｜Jitendra Mohan｜customer：中國營收絕對值增加但占比維持個位數（原話："they will continue to be in the single digit."）
- 2026-08-04｜Sanjay Gajendra｜customer：主要超大規模客戶有多個平台設計導入（原話："even with the lead hyperscaler we have,"）
- 2026-08-04｜Jitendra Mohan｜competition：提及其他廠商已推出或宣布UALink相關產品（原話："Some of the other vendors have also introduced their"）
- 2026-08-04｜Jitendra Mohan｜risk：機櫃內scale-up本世代與下一代仍以銅為主，光學用於機櫃間（原話："within a rack will continue to be copper."）

### 問答異常語氣（迴避／改口／保留）
- ALAB_Q2_2026_Earnings_Call_20260804.md｜問：Barclays（Trip Smith）問Scorpio毛利率變化與Amazon warrant影響如何建模｜答法：CFO回答Q3毛利率約72%、Scorpio平均毛利率與公司整體相當、長期78%，未回應Amazon warrant影響
- ALAB_Q2_2026_Earnings_Call_20260804.md｜問：Citi（Papa Sylla）問Scorpio X逾$1,000是否為UALink前指標，及目前每加速器內容價值與未來2–3年走向｜答法：回答『multiple thousands of dollars』與『targeting multiple thousands』，未給目前具體數字或是否為UALink前指標

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
{"date":"20261013","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價≤200美元且FY2027E共識EPS≥6.39；或最大客戶外≥2家Scorpio X量產且股價≤260美元；任一成立重跑判斷再定首倉","irr_base_pct":1.5,"ev5y_pct":14.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"-","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.6,"ev5y_pct":14.0,"irr_base_pct":1.5,"max_dd_pct":-70,"bull_5y_price":665.0,"bear_5y_price":120.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價≤200美元且FY2027E共識EPS≥6.39；或最大客戶外≥2家Scorpio X量產且股價≤260美元；任一成立重跑判斷再定首倉","price_at_dd":308.85,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
