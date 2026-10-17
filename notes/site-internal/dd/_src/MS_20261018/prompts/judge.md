你是 stock-analyst **v20 判斷 agent**，標的 MS（20261018）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MS","date":"2026-10-18","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MS_20261018/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MS_20261018/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"淨營收（GAAP）","value":20338,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi1_gaap","label":"稅前利益（GAAP）","value":6478,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi2_non_gaap","label":"稅前利益率（營業利益率對應，銀行無 non-GAAP 營業利益）","value":31.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi3","label":"費用效率比","value":67,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi5_rotce","label":"ROTCE","value":22.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi6","label":"薪酬與福利費用","value":7997,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi7","label":"財富管理淨營收","value":9065,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi8","label":"財富管理淨新增資產","value":232.4,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"十億美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi9","label":"機構證券淨營收","value":10029,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi10","label":"投資管理淨營收","value":1459,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi11_cet1","label":"標準法 CET1 比率","value":14.9,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_kpi12","label":"股票買回","value":1540,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-14","period":"2026-10-14","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-14"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_ms_fcf_margin_pct","label":"MS FCF 利潤率","value":-25.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_jpm_fcf_margin_pct","label":"JPM FCF 利潤率","value":-83.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JPM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_gs_fcf_margin_pct","label":"GS FCF 利潤率","value":-62.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_bac_fcf_margin_pct","label":"BAC FCF 利潤率","value":73.37,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wfc_fcf_margin_pct","label":"WFC FCF 利潤率","value":22.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WFC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_eps","label":"稀釋後 EPS","value":3.03,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-14）","citation":"公司財報新聞稿（Form 8-K 附件）https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":180.57,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-3.33,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":25.42,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-1.47,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.94 → 12.75）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.29,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.61 → 13.57）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":1.82,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（14.3 → 14.56）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":12.75,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":13.57,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":14.56,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.59,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 12.19 → 12.75（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":14.32,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝34.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":34.1,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.55,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝53.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":53.9,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":1.91,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":14.9,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 12.75，分子＝快照價 190.02","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.298,"period":"2026-10-18","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-18"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-131580.03,"period":"2026-10-18","unit":"USD m","basis":"yfinance 最新一季：總債務 607495.98、現金 739076.01（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1570.57,"period":"2026-10-18","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":152017.15,"period":"2026-10-18","unit":"USD m","basis":"市值 283597.18 ＋ 淨負債 -131580.03","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":82176.77,"period":"2026-10-18","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":86675.37,"period":"2026-10-18","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":1.85,"period":"2026-10-18","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"MS 2026 Q2 營收創高 213.5 億美元，投銀收入年增 58% 至 24.4 億美元（搜尋摘要轉述，二手來源）","source":"XTB market analysis: Morgan Stanley delivers a blockbuster quarter","url":"https://www.xtb.com/en/market-analysis/morgan-stanley-delivers-a-blockbuster-quarter-record-earnings-spark-wall-street-rally","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"LSEG 報導：投銀費用榜 JPMorgan 居首（101 億美元）、Goldman 第二（82 億美元），其後為 Morgan Stanley、BofA、Citi；前十大合計 wallet share 41.8%，較去年增 3.4pp；時點未明","source":"Investment Executive: Strong markets boost bankers' fortunes","url":"https://www.investmentexecutive.com/news/markets/strong-markets-boost-bankers-fortunes/","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261018","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Goldman 2026 上半年投銀費用年增 52% 至 62.4 億美元（股票承銷 +90%），為同業對手動能數據；未找到 MS 同期份額數字","source":"Zacks via yourwyominglink: Goldman's IB fees jump 52% in 1H26","url":"https://www.yourwyominglink.com/goldmans-ib-fees-jump-52-in-1h26-will-the-uptrend-continue/article_0a820192-75ad-5988-b2e1-192e1ae5fca0.html","excerpt":"Goldman's IB fees jumped 52% to $6.24 billion in 1H26 on broad-based strength.","as_of":"2026-07-20","retrieved_at":"20261018","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Zacks 預估 MS 投銀收入 2025 年 +12.8%、2026 年 +4.1%、2027 年 +5.4%","source":"Zacks research report MS (2026-01-08)","url":"https://advisortools.zacks.com/proxy/ResearchReport/MS/report?d=20260108","excerpt":"We expect IB revenues in the IS segment to grow 12.8% in 2025, 4.1% in 2026 and 5.4% in 2027.","as_of":"2026-01-08","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 風險段把集中風險定義為單一發行人／國家／產業的部位集中，搜尋未見單一客戶營收占比揭露","source":"Morgan Stanley Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/895421/000089542126000086/ms-20251231.htm","excerpt":"The Firm is subject to concentration risk by holding large positions in certain types of securities, loans or commitments to purchase securities of a single issuer, including sovereign governments and other entities.","as_of":"2026-02-26","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"母公司長期評等 A1(Moody's)／A-(S&P)／A+(Fitch)，展望皆穩定；未見 2026 年母公司評等調降","source":"Morgan Stanley 2Q26 Fixed Income Investor Presentation (2026-08-06)","url":"https://www.morganstanley.com/content/dam/msdotcom/en/about-us-ir/pdf/Morgan_Stanley_2Q26_Fixed_Income_Investor_Presentation.pdf","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261018","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"投行景氣被管理層與報導描述為循環回升；CEO Pick 對是否進入「黃金期」保持保留，但預期 IB 活動未來幾年續升。","source":"Reuters 轉載：Wall Street bankers shift focus to busy 2026 after cashing in on big deals (Kitco)","url":"https://www.kitco.com/news/off-the-wire/2026-01-15/wall-street-bankers-shift-focus-busy-2026-after-cashing-big-deals","excerpt":"whether we are entering a golden age of investment banking remains to be seen","as_of":"2026-01-15","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"CFO Yeshaya 稱 M&A 與 IPO 管線加速。","source":"Reuters 轉載：Wall Street bankers shift focus to busy 2026 (Kitco)","url":"https://www.kitco.com/news/off-the-wire/2026-01-15/wall-street-bankers-shift-focus-busy-2026-after-cashing-big-deals","excerpt":"We are seeing an accelerating pipeline in M&A and IPOs","as_of":"2026-01-15","retrieved_at":"20261018","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"3Q26 財富管理淨收入 $9,065M（上年 $8,234M），費用型資產 $3,155B，費用型流入 $80.5B（上年 $41.9B）；有分析指出約過半淨新增資產來自 IPO 相關流入，剔除後趨勢未明。","source":"Morgan Stanley 3Q26 earnings release (SEC 8-K) 與 Family Wealth Report 摘要","url":"https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261018","affects":["thesis.H","thesis.R","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"MS 10-Q（2026-06-30）列示私人反壟斷訴訟：VRDO 集體訴訟（最高法院 2026-04-20 駁回調卷，2026-07-13 被告提出簡易判決動議）與利率交換訴訟（2026-03-12 被告提出簡易判決動議）仍在進行；搜尋未見 2026 年新的 DOJ／FTC 反壟斷調查","source":"Morgan Stanley Form 10-Q for period ended 2026-06-30 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000212/ms-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"美國大型銀行 Basel III 修訂提案（Federal Register 2026-03-27）與 GSIB 附加資本提案進行中；MS CFO 2026-04 表示資本要求將持平或小幅下降，細節取決於最終規則；搜尋結果未顯示最終規則是否已發布","source":"Federal Register / Morgan Stanley Q1 2026 earnings call summary (via search results)","url":"https://www.federalreserve.gov/apps/proposals/comments/FR-2026-0007-01-C72","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261018","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"第三方彙整的 MS 風險揭露（標示 2026）：機構證券部門業績受全球貿易政策、關稅、保護主義、貿易制裁或投資限制變動影響；屬常設風險因子，無量化關稅衝擊。","source":"policyrisk.com MS company page（SEC 揭露彙整）","url":"https://policyrisk.com/world/company/MS","excerpt":"Morgan Stanley's Institutional Securities results are subject to changes in global trade policies, supply-chain complications, tariffs, protectionist trade policies, trade sanctions or investment restrictions.","as_of":"2026-01-01","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025 年 4 月關稅宣布後 MS 股價單日跌 9.5%；評論稱客戶可能延後大型併購。","source":"Motley Fool: why morgan stanley stock sank today","url":"https://www.fool.com/investing/2025/04/03/why-morgan-stanley-stock-sank-today","excerpt":null,"as_of":"2025-04-03","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"MS FY2025 10-K 將第三方弱點列為營運風險的外部來源，並表示公司或其第三方發生中斷可能損及業務或聲譽；未見點名特定供應商集中或單點失效。","source":"SEC EDGAR, Morgan Stanley Form 10-K FY2025 (ms-20251231.htm)","url":"https://www.sec.gov/Archives/edgar/data/895421/000089542126000086/ms-20251231.htm","excerpt":"Operational risk refers to the risk of loss, or of damage to our reputation, resulting from inadequate or failed processes or systems","as_of":"2025-12-31","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"3Q26 淨營收 203 億美元（去年同期 182 億）；機構證券約 100 億（去年 85 億），其中股票交易 +41%、投行 +2%、固定收益 -7%。","source":"Morgan Stanley 3Q26 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261018","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"3Q26 財富管理營收創高 91 億（去年 82 億），稅前利潤率 30.4%，淨新增資產 2,324 億（去年 810 億），收費型資產流入 805 億（去年 419 億）；收費型客戶資產 3.155 兆。","source":"Morgan Stanley 3Q26 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"3Q26 投資管理營收降至 15 億（去年 17 億），資產管理費隨平均 AUM 上升，長期淨流入 158 億。","source":"Morgan Stanley 3Q26 earnings release (SEC 8-K)","url":"https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261018","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"2Q26 財富管理淨新增資產 1,481 億，收費型流入 391 億；略過半流入與客戶在 Workplace 通路的 IPO 相關，屬事件性來源。","source":"Pulse 2.0: Morgan Stanley Adds Record $148 Billion In Wealth Management Net New Assets","url":"https://pulse2.com/morgan-stanley-adds-record-148-billion-in-wealth-management-net-new-assets-with-more-than-half-tied-to-ipos/","excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"1Q26 六大美銀投行費用平均 +27%，業界投行營收 +14% 至 282 億（Dealogic）；2025 全球投行營收突破 1,000 億；MS CFO 稱併購與 IPO 管線加速；中東衝突與經濟不確定性為風險。未找到 2027 預測。","source":"Reuters WRAPUP via marketscreener: Wall Street bankers shift focus to busy 2026","url":"https://in.marketscreener.com/news/wall-street-bankers-shift-focus-to-busy-2026-after-cashing-in-on-big-deals-ce7e58d9d18ef326","excerpt":null,"as_of":"2026-04-15","retrieved_at":"20261018","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#none","axis":"substitute_technology","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 2026 財報電話會議上 CFO 稱，逾 1 兆美元客戶資產已從職場與 E*TRADE 通路轉入顧問主導的財富管理業務，約占 5.8 兆美元顧問資產的 20%（二手文章轉述，未對照逐字稿）","source":"247WallSt: Morgan Stanley Says a $1 Trillion Shift Is Coming to Wealth Management","url":"https://247wallst.com/investing/2026/07/08/morgan-stanley-says-a-1-trillion-shift-is-coming-to-wealth-management/","excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"E*Trade 計畫經 Zerohash 提供加密幣交易（BTC/ETH/SOL），2026 年 5 月報導稱處於試點、年內推向約 860 萬用戶，定價低於 Coinbase／Robinhood／Schwab（二手轉載 Bloomberg，未證實）","source":"Cointelegraph / Bloomberg 轉載：Morgan Stanley E*Trade crypto trading 2026","url":"https://cointelegraph.com/news/morgan-stanley-etrade-crypto-trading-2026","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261018","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-10-14 快照：26 位分析師平均目標價 $222.14，區間 $184–$262；11 買進、14 持有、1 賣出。其他來源數字不一（Investing.com $233.43/21 位、Benzinga 9/30 $208/17 位），日期與口徑不同。","source":"搜尋彙整（Barchart／Investing.com／Benzinga 等）","url":"https://www.barchart.com/story/news/35885486/what-are-wall-street-analysts-target-price-for-morgan-stanley-stock","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MS 3Q26（2026-10-14 公布）淨收入 $203 億、EPS $3.03、ROTCE 22.6%；LSEG 預期 EPS $2.91、營收 $199.5 億，優於預期。股票交易收入約 +41%，投行收入 +2% 但低於預期約 $1.1 億。","source":"Morgan Stanley 3Q26 earnings release (SEC 8-K)；新聞彙整","url":"https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000288/a3q26msearningsrelease.htm","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261018","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"財報前預覽稱管理層維持紀律性目標（如財富管理 30% 利潤率），若持續超標願意重新檢視；未找到本次發布確認任何目標更動或新 guidance 調整。","source":"Hudson Labs／FMP Q3 2026 earnings preview","url":"https://www.hudson-labs.com/research/morgan-stanley-q3-2026-earnings-preview-ms-results-preview","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261018","affects":["triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"現金掃款（cash sweep）客戶集體訴訟已合併為 SDNY 單一案件 Estate of Sherlip v. Morgan Stanley；2025-08-15 提出修正訴狀，2025-09-12 MSSB 聲請駁回。性質為契約／受託／法定請求，非證券詐欺。","source":"Morgan Stanley Form 10-Q (2025-09-30)","url":"https://www.sec.gov/Archives/edgar/data/895421/000089542125000539/ms-20250930.htm","excerpt":null,"as_of":"2025-09-12","retrieved_at":"20261018","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"第三方摘要稱 2026-08-04 10-Q 顯示歐洲銀行實體 Morgan Stanley Europe SE 併入 Morgan Stanley Bank, N.A.（集團內部重組），並重新授權 200 億美元回購。屬聚合站二手摘要，非一手文件。","source":"autobound.ai: What Morgan Stanley's latest 10-Q says","url":"https://www.autobound.ai/companies/morgan-stanley/10-q","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"financial_capital_credit_cycle#0","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"MS 3Q26 全公司信用損失撥備 1.48 億美元，去年同期為零；9 個月累計 3.44 億 vs 去年同期 3.31 億；2Q26 為 9,800 萬。","source":"Morgan Stanley 3Q26 Quarterly Financial Supplement / 3Q26 shareholder letter (morganstanley.com IR)","url":"https://www.morganstanley.com/content/dam/msdotcom/en/about-us-ir/finsup3q2026/finsup3q2026.pdf","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#1","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"3Q26 撥備高於市場預期（共識約 8,400 萬）；季內有 1.05 億美元沖銷，對應特定企業與商用不動產放款，且先前季度已大部分提列。","source":"Private Banker International 摘要；roic.ai「Morgan Stanley Q3 earnings beat estimates but trading and credit signals diverge」","url":"https://www.roic.ai/news/morgan-stanley-q3-earnings-beat-estimates-but-trading-and-credit-signals-diverge-10-14-2026","excerpt":null,"as_of":"2026-10-14","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_capital_credit_cycle#2","axis":"financial_capital_credit_cycle","section":"coverage","direction":"0","claim":"1Q26 撥備 9,800 萬（4Q25 為 1,800 萬），主因為部分商用不動產放款的個別評估與總經不確定性升高；2Q26 機構證券撥備來自企業放款與擔保融資成長及部分企業／CRE 放款個別評估。1H26 淨沖銷率約 0.03%。","source":"Morgan Stanley 1Q26 Financial Supplement／2Q26 shareholder letter／2Q26 Fixed Income Investor Presentation","url":"https://www.morganstanley.com/content/dam/msdotcom/en/about-us-ir/shareholder/2q2026.pdf","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"financial_capital_credit_cycle#3","axis":"financial_capital_credit_cycle","section":"coverage","direction":"-","claim":"產業面：Fitch 報告私募信貸違約率創 6% 紀錄（至 2Q26）；Morningstar DBRS 12 個月借款人違約率 4%（前年 2.8%）、1Q26 降級／升級比 3.3 倍、2026 展望為負面；美國銀行對私募信貸提供者放款近 3,000 億美元（Moody's，至 2025 年 6 月）。","source":"alternativecreditinvestor.com／Morningstar DBRS／Reuters 引述 Moody's 彙整","url":"https://alternativecreditinvestor.com/2026/02/17/defaults-rise-as-credit-quality-weakens-in-q1-2026/","excerpt":null,"as_of":"2026-02-17","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"financial_regulatory_capital_rules#0","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"+","claim":"Fed 於 2026-02-04 表示 MS 維持 4.3% SCB 至 2027-10-01；CCAR 2026 結果（2026-06-24）不影響其 SCB；標準法 CET1 要求 11.8%，2026-03-31 實際 CET1 15.1%，緩衝約 330bp。","source":"Morgan Stanley Form 10-Q (Q1 2026) / SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0000895421/000089542126000121/ms-20260331.htm","excerpt":"The Federal Reserve said on February 4, 2026 that Morgan Stanley remains subject to its current 4.3% SCB until October 1, 2027","as_of":"2026-03-31","retrieved_at":"20261018","affects":["decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"financial_regulatory_capital_rules#1","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"+","claim":"2026-03-19 三項資本提案取代 2023 年 Basel III Endgame；機關估計最大 GSIB 的 CET1 要求下降約 4.8%，Fed 估 GSIB 附加費平均降約 40bp；尚無最終規則。","source":"Fed/OCC/FDIC 2026-03-19 proposals，經 Basel III Endgame 2026 摘要整理（learnsignal／Senate letter）","url":"https://www.learnsignal.com/blog/basel-iii-endgame-explained-2026-us-capital-rules/","excerpt":"The agencies project Common Equity Tier 1 requirements falling about 4.8 percent for the largest global systemically important banks. The Fed estimates a GSIB surcharge cut averaging 40 basis points.","as_of":"2026-03-19","retrieved_at":"20261018","affects":["valuation","thesis.H","triggers"],"status":"ok"},{"id":"financial_regulatory_capital_rules#2","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"-","claim":"2026-06-18 參議院民主黨議員要求 Bowman、Gould、Hill 撤回三項資本提案，主張重新提出更嚴規則；屬提案翻轉風險。","source":"Senate Banking Committee, letter to financial regulators re Basel III proposal","url":"https://www.banking.senate.gov/imo/media/doc/20260618_letter_to_financial_regulators_re_basel_iii_proposalpdf.pdf","excerpt":"On June 18, 2026, Senate Democrats asked Bowman, Comptroller Gould, and FDIC Chairman Hill to withdraw all three proposals.","as_of":"2026-06-18","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"financial_regulatory_capital_rules#3","axis":"financial_regulatory_capital_rules","section":"coverage","direction":"+","claim":"MS 在 2026-06-18 意見信支持提案核心設計，促請 2026 年內定案，修訂資本標準一般於 2028-01-01 生效；與 Fed 幕僚會談聚焦短期批發資金指標與實施時程。GSIB 提案把附加費級距由 0.5pp 改為 0.1pp。","source":"Fed 公開會議紀錄 morgan-stanley-meeting-20260707 及 MS 意見信（經搜尋摘要）","url":"https://www.federalreserve.gov/regreform/rr-commpublic/morgan-stanley-meeting-20260707.pdf","excerpt":"it supported the core design of these proposals and urged the agencies to finalize standards in 2026, with revised capital standards generally taking effect on January 1, 2028.","as_of":"2026-07-07","retrieved_at":"20261018","affects":["valuation","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"第三方摘要稱 2026-08-04 10-Q 顯示歐洲銀行實體 Morgan Stanley Europe SE 併入 Morgan Stanley Bank, N.A.（集團內部重組，非外部併購）。二手來源。","source":"autobound.ai: What Morgan Stanley's latest 10-Q says","url":"https://www.autobound.ai/companies/morgan-stanley/10-q","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"現金掃款客戶集體訴訟合併為 SDNY Estate of Sherlip v. Morgan Stanley；2025-08-15 修正訴狀，2025-09-12 聲請駁回；NJ 案合併為 In re E*TRADE Cash Sweep Litigation。非證券詐欺。","source":"Morgan Stanley Form 10-Q (2025-09-30)","url":"https://www.sec.gov/Archives/edgar/data/895421/000089542125000539/ms-20250930.htm","excerpt":null,"as_of":"2025-09-12","retrieved_at":"20261018","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：gross_margin_pct、operating_margin_pct、rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"MS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-25.44,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MS","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"JPM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-83.39,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JPM","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"GS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":-62.71,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GS","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"BAC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":73.37,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BAC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"WFC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":22.09,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WFC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MS"},"financial_history":{"ticker":"MS","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":50210000000.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":11029000000.0,"diluted_eps":6.15,"free_cash_flow":-9475000000.0,"fcf_margin_pct":-18.87,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":50667000000.0,"revenue_yoy_pct":0.91,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":9087000000.0,"diluted_eps":5.18,"free_cash_flow":-36948000000.0,"fcf_margin_pct":-72.92,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":57621000000.0,"revenue_yoy_pct":13.72,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":13390000000.0,"diluted_eps":7.95,"free_cash_flow":-2100000000.0,"fcf_margin_pct":-3.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":65966000000.0,"revenue_yoy_pct":14.48,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":16861000000.0,"diluted_eps":10.21,"free_cash_flow":-20787000000.0,"fcf_margin_pct":-31.51,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MS/MS_Q3_2026_Earnings_Call_20261014.md）

# Q3 2026 Earnings Call
**Morgan Stanley** | Earnings Calls | 2026-10-14

**Operator** (Operator):
Good morning. Welcome to Morgan Stanley's Third Quarter 2026 Earnings Call. On behalf of Morgan Stanley, I will begin the call with the following information and disclaimers. This call is being recorded. During today's presentation, we will refer to our earnings release and financial supplement, copies of which are available at morganstanley.com. 
Today's presentation may include forward-looking statements that are subject to risks and uncertainties that may cause actual results to differ materially. Morgan Stanley does not undertake to update the forward-looking statements in this discussion. Please refer to our notices regarding forward-looking statements and non-GAAP measures that appear in the earnings release. This presentation may not be duplicated or reproduced without our consent. I will now turn the call over to Chairman and Chief Executive Officer Ted Pick.

**Ted Pick** (Executives):
Thank you, operator. Good morning, and thank you for joining us. In the third quarter, Morgan Stanley delivered strong performance on the top and bottom lines with firm-wide revenue of $20.3 billion and earnings per share of $3.03. With a return on tangible equity of 22.6%, this quarter marks our fifth consecutive quarter above 20%, speaking to the consistent strength of our global franchise. 
Total client assets across Wealth and Investment Management grew by nearly $400 billion during the quarter to a record $10.5 trillion. Against a complicated backdrop, the quarter's overall performance speaks to the momentum of the integrated firm. Wealth Management continues to scale as clients entrust us with additional assets and deepen their relationships with Morgan Stanley. 
Wealth had a record quarter with revenues of over $9 billion, with milestone levels of net new assets of $232 billion and fee-based flows of $80 billion. This sustained performance reflects the strength of our financial advisers, the breadth of our unique capabilities and product offerings and the trusted partnerships that distinguish our integrated firm. Institutional Securities delivered $10 billion of revenue, up 18% year-over-year. Equities led the way with another outstanding quarter at $5.8 billion. 
Clients largely remained active as we deepened engagement across our global franchise. On the forward, banking pipelines remain high and strategic dialogues inside corporate boardrooms are active and generally receptive to action. Clients are seeking advice to capitalize on the current dynamic growth environment while accepting some additional structural volatility. Pent-up demand and catalysts to drive scale and productivity and a more constructive regulatory backdrop support an ongoing favorable outlook for Investment Banking activity. In short, we remain positive about the ongoing ability to monetize the corporate finance life cycle across the investment bank. 
Stepping back, the third quarter unfolded in 2 distinct phases. July and August were unusually brisk as risk appetite was dominated by hyperscaler investment in the build-out of the AI ecosystem. In contrast, as Labor Day approached, we observed the headwinds of renewed tensions in the Middle East and higher interest rates globally as central banks moved to keep inflation at bay. Market volumes were slower across asset classes as investors and institutional actors gauged risk-reward into the fourth quarter and year-end. 
As we move through October, the 2 known unknowns that we wrote about in our March shareholder letter, namely the acceleration of AI at the enterprise level and the risks associated with geopolitical conflict, have reached a critical juncture. In the glass-is-mostly-full camp, the enormous capital, which continues to be raised and deployed across the AI ecosystem toward efficiency, resiliency and productivity, is driving U.S. nominal GDP growth of 5% to 6%. Large-cap corporate earnings continue to move higher. The economy is at full employment. The Fed is focused on managing long-term inflation expectations, and the salutary effects of common sense regulation are kicking in. 
In the glass-is-half-empty camp, persisting conflicts in the Middle East and Ukraine, meaningfully higher benchmark interest rates and energy prices around the developed world, elevated asset prices in a fourth year of a bull market for equities, and uncertain electoral and policy responses in both the U.S. and globally are reasons to be more cautious. As we move into the fourth quarter, it is clear to us now that these 2 known unknowns and how they interact and which of the third quarter's narratives, half full or half empty, holds the upper hand, will drive investor and corporate behavior into year-end and into the first half of 2027. 
Against either backdrop, financial strength remains a key pillar of Morgan Stanley. We continue to actively support clients while remaining well capitalized. Our very healthy level of excess capital, with 300 basis points of excess CET1, contributes to our financial strength and affords us with substantial flexibility ahead. We look forward to continued dialogue and upcoming transparency as our regulators finalize the bank capital regulatory framework. 
As we enter the final quarter of the year, Morgan Stanley remains aligned and cohesive, focused on delivering higher highs and higher lows through the cycle. Particularly when the environment is as complex as it is today, it is essential that we continue to execute on our clear and consistent strategy to act as trusted adviser to our clients, raising, managing and allocating capital across the integrated firm. With that, I'll turn it over to Sharon to take you through the quarter in greater detail.

**Sharon Yeshaya** (Executives):
Thank you, and good morning. In the third quarter, the firm delivered strong results. Revenues of $20.3 billion, EPS of $3.03 and an ROTCE of 22.6%. Growth momentum from the second quarter carried into the early part of the third quarter, with markets focused on AI investment and continued economic expansion. However, rising energy prices and interest rates weighed on market activity following a shortened post-Labor Day September. Despite market uncertainty, corporate activity remains strong, reflecting continued strategic dialogue. Ongoing client engagement reinforces the opportunity for our integrated firm to deepen relationships and support future activity.
Year-to-date, the firm's efficiency ratio was 66%. Strong revenues drove operating leverage, more than offsetting elevated execution-related costs compared to the prior year. We continue to invest across our technology stack, embracing AI tools to support our infrastructure, business growth and people. Together, these investments position us to strengthen our competitive moats across the integrated firm. 
Now to the businesses. Institutional Securities revenues were $10 billion, up 18% versus the prior year. The year-over-year increase was driven by our leading equities franchise and a pickup in advisory. Exit momentum from the second quarter carried into July before client activity and markets moderated through September, but boardroom dialogue remained strong through the quarter, supporting the build of strategic pipelines and future capital markets financings. 
Investment Banking revenues were $2.2 billion, up 2% from the prior year, reflecting strength in the Americas as well as in Asia, consistent with our expectations of a sequential broadening out of global activity. Advisory revenues of $887 million drove results. The increase relative to the prior year period reflects higher completed activity across most sectors. Equity underwriting revenues were $525 million, down compared to broad-based strength in the prior year with a few large deals driving the market. 
Fixed income underwriting revenues continued to be strong at $747 million, supported by a new issue market that remained active. Pipelines remain robust and diversified across products, sectors and regions. Strategic activity remains healthy, supported by ongoing corporate investment, portfolio repositioning and capital allocation priorities. AI continues to contribute to the advisory and capital markets momentum, but activity is broad-based across sectors and products.
Turning to equity. Revenues were $5.8 billion, increasing 41% versus the prior year, reflecting growth across products and across Asia. As client needs become more complex and global, our integrated franchise is well positioned. Our investments in technology and talent have strengthened our capabilities, allowing us to serve at greater scale and manage risk more effectively in fast-moving markets. Prime brokerage drove results led by growth in financing revenues on higher average client balances. Derivative results increased versus the prior year, driven by higher client activity early in the quarter and strong risk management. 
Cash results were higher year-over-year, driven by increased client volumes across regions. Fixed income revenues were $2 billion, reflecting lower structured activity in credit and commodities. Macro results increased modestly compared to the prior year, aided by foreign exchange. Micro results declined year-over-year, driven by lower performance in securitized products. Commodity results were solid, though declined against a strong comparative period that benefited from structured transactions.
Turning to ISG lending and provisions. In the quarter, ISG provisions were $141 million, driven primarily by portfolio growth. Net charge-offs were $105 million, primarily related to certain corporate and commercial real estate loans, which were largely provisioned for in prior periods.
Turning to Wealth Management. The business delivered records across key growth indicators, including net new assets of $232 billion and fee-based flows of $80 billion. In the first 9 months of the year, we have delivered roughly $0.5 trillion of net new assets and about $175 billion in fee-based flows. These results demonstrate the reach of our multichannel model and our ability to connect clients with trusted advice. Revenues of $9.1 billion and pretax profit of $2.8 billion were also records. The pretax margin of 30.4% shows consistent strength as we invest in technology, marketing and our banking capabilities to support future growth. 
Asset management revenues grew 16% year-over-year to $5.5 billion, benefiting from higher markets and the cumulative impact of robust fee-based flows. Fee-based flows of $80 billion set a new organic record, with nearly half coming from a corporate retirement mandate. We continue to expand our retirement capabilities and deepen engagement with plan participants, creating more opportunities to build advice-based relationships over time. Transactional revenues were $1.2 billion, up 6% year-over-year, excluding the prior year's DCP benefit. 
While trading activity moderated from the second quarter, retail engagement across our differentiated product offering remains healthy, with alternatives delivering another quarter of record sales. Bank lending balances grew $5 billion sequentially, driven by securities-based lending and mortgages. Total deposits grew by nearly $30 billion sequentially to $465 billion, reflecting investments to strengthen our bank offering. Net interest income was $2.2 billion, down modestly as deposits grew and the mix shifted. Looking ahead, we expect a modest increase in the fourth quarter, subject to rates and client behavior. 
Lastly, net new assets of $232 billion reflect the strength of our core business and the differentiated growth opportunities created by Workplace and the integrated firm. IPO-related flows once again contributed to just over half of the overall NNA. With an active IPO calendar, the pace of our funnel accelerates and client interest in advice increases. While flows will fluctuate as lockups expire, funds make distributions and individuals use assets for consumption, our pipeline and our connectivity across channels allows us to build relationships early and deepen them over time.
Since acquiring E*TRADE and expanding our Workplace offering 6 years ago, we have added over $2 trillion of net new assets. Our multiyear track record demonstrates our differentiated client acquisition funnel and its durability. Today, we have $8.4 trillion in client assets and serve nearly 21 million relationships. Our platform and broad product offering enables us to serve our clients across a wide range of needs, while our scale supports continued investment in future technology, including AI and digital tools. Together, these strengths provide us with a powerful competitive advantage that positions us to lead as the future of Wealth Management takes shape.
Turning to Investment Management. Consistent strength from Parametric and fixed income contributed to long-term flows -- inflows of $15.8 billion. Parametric continues to benefit from distribution through our scaled Wealth Management platform, while fixed income was supported by strong performance. Revenues of $1.5 billion reflect steady growth in asset management and related fees. Carry reversal, primarily related to 2 investments in a private fund, muted overall results. Looking ahead, we continue to invest in opportunities related to global distribution and connectivity with our financial advisers.
Turning to the balance sheet. Total spot assets ended the quarter at $1.7 trillion. Standardized RWAs increased sequentially to $596 billion as we actively supported clients in our markets business and continued to grow corporate lending. We repurchased $1.5 billion of common stock in the quarter, and our standardized CET1 ratio ended at 14.9%. Our quarterly tax rate was 23.3%. For the fourth quarter, we expect our tax rate to be slightly above the third quarter's tax rate, and our full year guidance remains unchanged. 
Amid a changing rate environment and geopolitical uncertainty, we remain a trusted adviser to clients. This environment underscores the value of the integrated firm, as we leverage capabilities across businesses to address evolving client needs. With $10.5 trillion in total client assets across Wealth and Investment Management, we have the foundation to build on as we close out the year. With that, we will now open the line up to questions.

**Operator** (Operator):
[Operator Instructions] We'll take our first question from Steven Chubak with Wolfe Research.

**Steven Chubak** (Analysts):
This is a meaty one, so I'm just going to limit it to one question, but a 2-parter. Just on the topic of digital infra, CapEx spending, and the implications for future revenue growth. So you guys have been the leader just in digital infra-related financing activity. We see that in the league table numbers for both ECM and DCM. As we look ahead, do you think there's room for digital infra-related IB fees to continue to grow off the current base, even as a larger portion of equity and debt financing is expected to migrate from the public to the private markets? And then for the second part, I was hoping you could just speak to some of the ancillary revenue streams tied to a lot of this digital infra build-out that exists outside of the core IB franchise. So certainly, SpaceX and the NNA tailwind, it should be a durable source of strength in wealth, but whether there is other sources of revenue related to this opportunity that might be overlooked by the investor community.

**Ted Pick** (Executives):
Yes. Meaty questions. And on AI, of course, we're still relatively early in the CapEx cycle. Whether it ends up being $10 trillion or more or less, we will see as it plays out, but the hyperscaler CapEx is running as we speak at around $1 trillion a year. And our role as an adviser in all pieces of this will remain to be a critical differentiator. We're advising clients on the full ecosystem of their strategic and capital markets alternatives. We're helping them innovate. We're helping them finance through the life cycle, and we're working really across the full ecosystem, whether it's our teams working to help build public solutions or private solutions to act as an innovator across the world.
And whether we're working with the chips folks, the data centers or the power providers, the activity from here may not accelerate, but I think we all see that the power of AI, as an efficiency and productivity and resiliency tool, is incontrovertible, a generational jump in technology. The relationships and innovation that Morgan Stanley brings to our clients will absolutely be critical as friends become friends in certain contexts. Maybe not permanent friends, but permanent interests in the context of who does deals with whom and how they are structured, in what market, where on the capital structure. That requires real structuring knowledge, real expertise and real trust. 
And the Morgan Stanley team has shown itself to be quite excellent here as a differentiator and importantly, what clears the market. Sometimes the technology will be ahead of what the market will accept, and sometimes vice versa, and we have to be cognizant of what the market will accept at a given time. So some judgment there is, of course, experiential judgment is critical.
Steve, on your net new asset question, we see a lot of growth associated with IPO events, but beyond the IPO channel, when we look at Workplace and our presence with so many private companies, we believe that this cycle has many years to come. Net new assets will ebb and flow in a given quarter, but as Sharon said, but let's take a step back and remember that we bought E*TRADE 6 years ago. This completed the funnel. The funnel is this extraordinary self-directed piece, the Workplace and then, of course, the financial adviser. And we generated $1 trillion of net new assets in the 3 years subsequent to the acquisition of E*TRADE. 
And then the last 3 years, we drew in another $1 trillion. So $1 trillion over 3 years, 2-, 3-year sets running, shows not only our ability to make the proposition, the case, that scale begets scale, but the reinvestment from within the funnel is clearly here. And of course, as lockups and funds make distributions, there are further opportunities to retain assets. So we are very excited about the attachment points ultimately that bring clients to E*TRADE, that we are close with them in the corporate stock plan context, i.e., Workplace, but then ultimately, where it's appropriate, fee-based flows that make their way to the advisers, which is why that $80 billion number that Sharon speaks to, the fee-based flows, is such an important statistic.

**Operator** (Operator):
We'll take our next question from Brennan Hawken with BMO Capital Markets.

**Brennan Hawken** (Analysts):
I was hoping to follow up on that last point. The net new at $232 billion, really quite impressive. You flagged the benefits from the IPOs despite a slower quarter for issuance. So could you speak to how much of that was a tail from prior deals versus the current quarter? And what's the best way that we should be thinking about that tail as we think about quarters still to come?

**Sharon Yeshaya** (Executives):
Sure. Thanks, Brennan. I'll take it. In terms of -- you highlight a really good point, that we talk about IPOs, and we talk about them as not just one quarter, but you use a word that I use as well, which is there's a tail to this process. So in the second quarter, you'll note, specifically even in the press release, I think I spoke about it in my prepared remarks, we talked about the flows that came from the IPOs being largely employee-related.
In this quarter, what you saw is a continuation of these flows that come from IPOs, which is not necessarily just a one-quarter event. So as you know, we have a full cap table. We understand early investors. And you can think, for example, of an endowment that might receive a stock associated with an IPO. He or she might take that and put it through from a transfer agent into a Morgan Stanley advice-based relationship. So now you have flows that are under the advice-based channel and are through, say, a different portion of the cap table.
You might, as Ted said, also have flows that are now distributed from funds that go into individual-based accounts, right? So the fund takes it, and the lockups expire, and they're distributed to the underlying investor, or on an individual level. So there's a lot of places where that funnel begins to move into an advice-based relationship. Of course, as we move forward, Ted said it, you can ebb and flow, and you can see people actually, as lockups expire, selling stock and using it for different acquisitions of different real assets.
But the point is that this is the top part of the funnel. It's really a way to continue to aggregate new assets, new employee relationships, and we're seeing that. We're seeing with some of these IPOs, the first or the third quarter, so now that some of these IPOs have come to market, real relationships, adviser-led relationships being built. And that's just one piece, right? That's one piece of the top of the funnel.
You also have, as you probably saw, these corporate retirement flows that are coming through as fee-based assets where we're also talking to the individuals. So it's all a very big picture that we've been investing in for many, many years that has to do with both the Workplace and the individual and the corporate life cycle of wealth.

**Brennan Hawken** (Analysts):
Sharon, good to see the funnel operating so well. I'd love to also ask another question on wealth. The deposit growth was really robust here. And although it was driven realistically by the sort of higher-cost variety, could you speak to maybe how this growth is related to the bank and what you're doing there with funding of ISG operations and how we should think about those benefits playing through, whether there's a lag and how long that might take?

**Sharon Yeshaya** (Executives):
Yes, absolutely. So thank you for -- you hit the nail on the head in terms of what you see from NII, which is a very modest decline in the NII from a quarter-over-quarter basis, but a very large increase in the deposits of nearly $30 billion on a sequential basis. This is a very intentional decision, a strategic choice that we've made to grow the bank. We saw an opportunity to do so. I'd say that it's twofold, both from an integrated firm perspective, but also from a Wealth Management perspective.
So from the integrated firm, we've talked a lot about the bank and using the bank more strategically as a source of funding, and we saw that as we've begun to move assets into the bank, eligible assets that move into the bank over the course of the year. And yes, I think I spoke about it in the first quarter call that, that will be something that we'll see from a funding benefit as we enter into next year. So it's not immediate. It will come over time, and you'll see that play in through our numbers over the course of next year.
But in addition to the funding benefit, I also should mention that we do see really strong attachment points that are coming from the bank. So those clients that are bank first clients, over time, we've seen that 1/3 of them end up being a digital client or in a relationship, an adviser-based client as well. So that also helps. In addition, they end up also having more -- multiples more of NNA that comes to the institution. So we see a real opportunity to grow the bank, both from the Wealth Management perspective and the top of the funnel, but also from the funding side that will play out over time.

**Operator** (Operator):
We'll move to our next question from Glenn Schorr with Evercore ISI.

**Glenn Schorr** (Analysts):
So we've all asked the banks on agentic cash and all that movement. But from time to time, people have the same questions on how changes in technology are going to impact the wealth business going forward. So I know you guys invested in OpenAI before I knew that was a company. But outside of just the normal efficiency and advisory productivity that you're getting, I'm curious on, as the leaders in wealth, how you see -- what investments you're making and how you see the wealth advice as a service evolving in this technological backdrop.

**Ted Pick** (Executives):
Glenn, it's a critical question for Morgan Stanley as a strategic matter. We are now in a singular position in the industry where we see the integrated scaling of the funnel that you described. We have the self-directed channel that continues to innovate for clients. We have, as Sharon was describing, a differentiated Workplace offering that continues to expand and source new relationships. And we have ultimately the deep trust-based relationships between the financial advisers and their clients. And against that platform, we have built a number of advantages that not only allow us to preserve our moat, but actually make technology a differentiator in our favor.
I'd highlight 4. The first is, we all bear in mind that we've got a unique set of products and capabilities as the largest distributor in the world. We're the most important wealth partner to the entire asset management industry. There are significant parts of our alts platform, both product and pricing, that are not available to clients anywhere else. You are a Morgan Stanley client, you have access to our research, you have access to the calendar, you have access to private markets via EquityZen, you have co-investment opportunities, and then importantly for ultra-high net worth, family office infrastructure solutions. So the scale that we have offers differentiation that will remain and even be aided by agents.
Second, unique data. With $8.4 trillion of assets in Wealth Management and now getting to 21 million households, we have tremendous insights into what works and what doesn't when you talk to your financial adviser. You want to gauge on a particular day or particular month or particular year, what your risk-reward sentiment ought to be, how you should be thinking about life, and some of that can be governed by what others are doing through the use of data. It gives us insights, given our size and scale, that allow our FAs to tailor advice and equip our own tools to deliver that advice to help clients achieve their goals.
Third, and this is critical, is the ability to protect client assets. We're one of a very few number of firms that could continue to invest whatever it takes to protect our clients. Others, you can't engage head-to-head with AI out of your garage. So there will be a resiliency theme that will be super important to clients with real net worth as we go forward. And then fourth point, and this is really where it begins, where it ends, is it's a people business. At some level, if the technology is world-class, folks want to make decisions with their financial advisers based on the complexity and singularity of their own financial needs at a particular point in life, with respect to their parents, their kids, how they want to go about philanthropy, how they want to go about taxes, the whole thing. That is something that technology can help do a lot of the early work.
But ultimately, once you know that you have the ability to allocate across the entire asset spectrum, given that we are the largest distributor in the world of any kind of asset management product, given that we have insights from the unique data, and given that we are a protective shield for those assets, ultimately it comes down to, do I trust my financial adviser? And if I do, I'm at a place where the adviser retention rate is above 99% and the clients obviously are quite happy, which is why over time it's so important that we continue to scale not quarter-to-quarter, but over multiple years, and that we see the reinvestment in the funnel. That the funnel becomes not only a way to preserve our moat, but actually to be a technology winner, which is dating back to some of what you talked about, but continues today. So I'd say of all the many things to be excited about, I'd say now what the management team is most excited about is our ability now to further our scaling and, over time, our operating leverage in the Wealth Management business.

**Operator** (Operator):
We'll take our next question from Christian Bolu with Autonomous Research.

**Chinedu Bolu** (Analysts):
Maybe first another question on the impressive IPO flows into Wealth Management. Sorry if I missed, Sharon, on your earlier answer, but are you still expecting incremental flows in 4Q and '27 of what you've had so far? And then more broadly, how should we think about the economics of these flows? Are you seeing any signs that you can ultimately retain and turn them into annuitized fee-based assets?

**Sharon Yeshaya** (Executives):
Absolutely. Why don't I take it, and I'll take the last one first, which is that we are absolutely seeing that we can retain the assets. And we're seeing a pickup in the ability, and this is what I was trying to allude to in the last answer, is those IPOs that came to fruition in the second quarter, that we are building relationships, adviser-led relationships. And there's a lot of opportunities to do so, and there's a lot of interest to move forward. And we continue -- we will continue to build on those relationships, not just with where we've started now, but I think there's more opportunities to go with those individuals.
As it relates to retention rates, we're seeing steady retention rates. So what does that mean? It actually means that the dollars of assets is greater. So if you can keep the retention rates where they are, even as you get more flow, more assets at the top of the funnel, yes, that means that eventually that will help from a fee-based advisory flow as well or an adviser-led product, or an adviser-led relationship. Now as it relates to the second quarter, there's nothing material to call out in terms of expectations for those flows as you move forward. But as we said, assets will ebb and flow. You can think of an individual who might sell assets in order to buy something, but you can also think of individuals that now have those advice-based relationships and begin to aggregate assets held away. 
And that's been a lot of the strategy, even over the course -- if you go back 10 years, we used to talk about that, Christian, which is we see a great opportunity with assets held away. These individuals have just stepped into wealth. They begin to consolidate assets and understand the value of a fulsome advice-based relationship.

**Chinedu Bolu** (Analysts):
Great. Great. On expenses, I guess, non-comp expenses were flat Q-o-Q firm-wide despite sort of lower revenues. I think you spoke about some AI investments in your prepared remarks. Give me a sense of like more detail here. What are you spending on? Is it sort of tokens? Or are there more structural AI investments? And should we think about this as a sort of multiyear investment program?

**Sharon Yeshaya** (Executives):
Yes. I think that you will see that from any company in America is using their technology dollars to think about how to use AI, how to be more productive and how to support greater growth in revenues with their current expense base, with some of that translating into technology itself. So sort of a redistribution of dollars as you move forward. And how do you actually see that productivity? Again, anybody who works in sort of a senior management role can tell you how much AI is fundamentally changing what our own [ teams ] do. I can speak as sort of just as Head of Finance.
What we're seeing is remarkable. The reconciliation that you can see across different books, things that usually take so many manual human hours and can have, obviously there are controls in place, but the ability to see it with fewer errors and fewer mistakes and fewer checks is real. And in addition to that, there are just manual processes and manual, what we call EUCs, which are spreadsheets and others. They can automatically be written, understood, coded, and then moved into our real productivity life cycle sort of front to back of products. 
So it's an incredible tool. We're seeing it in the actual businesses themselves, even within our equities business, where you have different AI tools that salespeople can use. And I think that, that productivity is real, and that's where a lot of the spend is being seen.

**Operator** (Operator):
We'll take our next question from Mike Mayo with Wells Fargo.

**Michael Mayo** (Analysts):
You talked about half full, half empty. In the half empty column, you've had concerns about the AI CapEx super cycle as it relates to overbuilding, power, financing, politics, and you can probably complete that list a lot more. Where is your conviction on the AI CapEx super cycle in light of all these headlines? And you had some pulled IPOs, and last quarter you talked about CapEx. I think you had numbers like $800 billion to $1.3 trillion to $1.5 trillion. I'm just kind of marking the market the way you're thinking about it.

**Ted Pick** (Executives):
Yes. And Mike, I actually think this question is just going to have to be asked over and over again because the quantums are so big, and the growth of the U.S. economy is at some level, and even the global economy being powered by this AI CapEx cycle. I don't know that it necessarily accelerates from the $1 trillion that we're at. It could be $1 trillion, it could be $1.2 trillion, but we are at a level where it is meaningful, 50, 70 basis points of real GDP in the U.S. That is no small matter. And then how many years it takes? I mean, as we've talked about, sometimes the technologies can be ahead of the financing, the financing ahead of the technology.
But the efficiency and productivity, and then obviously the need to protect, all of these are incontrovertibly important for every large-cap institution over time. Every institution, of course, it's not just at the enterprise level, it's at the individual level. The key is our ability to continue to act as an adviser. That is what we are most focused on, that we are able to effectively act as the clearing mechanism in this very complicated ecosystem between all of the players, such that we are viewed as a fair hand in acting as the adviser, the structurer, the financing partner. If a deal doesn't clear the public markets, what do they do next? Do they raise private capital? How do they do that? How do they satisfy the needs of their LPs and other constituencies -- so it will be complicated, i.e., there will be moments of uncertainty.
And I have no doubt there will be times when it'll feel like it's going too fast, and there is a sense of overbuilding in some respects. And then there are going to be other times when it's not fast enough, and that there's a different bottleneck in the ecosystem, perhaps it's power. But the reality is the capital is going to have to be provided for this once in a multigeneration change. As we talked about, S&P 500 value is somewhere between $65 trillion and $70 trillion. Global GDP is, let's say, $120 trillion. These are sort of the denominators one can talk about. So $1 trillion is a heck of a lot in a given year, but $1 trillion against some of the best-performing companies of modern times that are still running cash flow positive to something that becomes -- you got to be in it to win it.
That is conceivable, really, over the course of 5, 10 years, that it could be at a run rate that is plus or minus $1 trillion. And our role is when things feel like they're going too fast and the market's not ready for the next financing or structure or innovation, we have to effectively consider what is appropriate. And then when it's not fast enough because the capital is needed, we throttle accordingly. So I am -- I continue to be humble and as querying as anyone with respect to whether the right number for, let's say, 2028 on hyperscaler CapEx is $1.2 trillion or $1.4 trillion or $1 trillion. But the number is going to be, we see, $1 trillion and at some kind of plateau level continue to be a very important part of what we all do in the capital markets as originators, in delivering content, and again, in bringing real sustained, not just efficiency, but productivity improvement to large-cap companies.

**Michael Mayo** (Analysts):
So where the rubber meets the road, you have to allocate resources for the AI opportunity. So in light of what you just said, the risks and opportunities, are you allocating more or less to the AI opportunity? And how are your backlogs?

**Ted Pick** (Executives):
We were, as you know, overweighted to AI from the early days in wealth with some of the work we did with OpenAI. We've been overweighted working with other complexes. You know who they are in terms of banking coverage, in terms of usage in our plans, in terms of wealth relationships, in terms of thinking about what it's like to go public. I would say that we were overweight, and in light of it being something that matters not just to our clients, but to us, I would say we are now double overweight.
There is just no question that this is existentially important that we are viewed as a trusted adviser in the middle of the ecosystem, given that we have a very clear strategy where we are acting as the wealth manager, the asset allocator, the banker. And for us to be part of the content and the thinking and the evolution of this is absolutely the top priority for the firm as the adviser. And then also that we're eating our cooking, and that we are providing resiliency and all that comes with the need to keep up with all of the innovation. And I appreciate the question, Mike.

**Operator** (Operator):
Our next question comes from Dan Fannon with Jefferies.

**Daniel Fannon** (Analysts):
You guys have talked about fee-based flows being key to the margin expansion within the wealth channel. And as you have more success with migrating Workplace clients to advice, should we see this convergence of the total flows and the fee-based flows continue? Or is that something that will always, kind of, have some spread to it?

**Sharon Yeshaya** (Executives):
That's a great question, Dan. It's going to depend really on what flows end up seeking what type of advice and those that want to be part of the fee-based ecosystem. What we've seen is it can -- let's take this quarter as an example, right? So the fee-based flows, we talked about a portion of those fee-based flows coming from a corporate retirement mandate. As you bring a full corporate retirement mandate on board, those will also be considered net new assets, right, because it's coming in immediately as a fee-based flow.
But you can have other situations, and we saw big backlogs where we had dollars accumulate just in brokerage, both on the advisory side and on the self-directed side, that then move into fee-based flows. And those are just individual accounts. And then you might have also relationships between stock plan, where people aggregate assets and move them directly into fee-based. So I think it just will depend on what flows you're discussing.
But importantly, we do see that, that value of advice, either they come in directly as a fee-based account or they come in and they migrate over time from self-directed or otherwise, is critically important. I think a statistic that I gave you guys earlier in the year was that a little bit over 20% of all of the adviser-led flows are fee-based flows. I mean that still holds, if not growing. And so that just shows you how powerful the fee-based model and the advice-led model is.

**Daniel Fannon** (Analysts):
That's helpful. And then just a follow-up on NII, and we heard your outlook for 4Q. But as you look at the rate backdrop today, trends in loan growth still seem to be positive. Is it reasonable to think about loan NII growth as we think about 2027 based upon kind of where things sit today?

**Sharon Yeshaya** (Executives):
Yes. We do expect to see NII over next year expand. And to your point, that's largely on the back of loan growth.

**Operator** (Operator):
Our next question comes from Ebrahim Poonawala with Bank of America.

**Ebrahim Poonawala** (Analysts):
I guess just one question first on -- when we think about the Wealth Management business, like the conversion from Workplace seems to be going extremely well, all the investments you talked about. In a world where, like, there's a lot of focus on just downside risks to the revenue environment, how should we think about that pretax margin? Like, it's 30%. I get you're making investments for the foreseeable future, so you're not, like, short-term targeting a higher pretax margin. I'm trying to get to, like, is all this conversion going to translate into a better pretax margin environment? And if things were to slow down, does it add to defensibility of earnings within that business and to the firm-wide ROE? If you could help us sort of think through that.

**Sharon Yeshaya** (Executives):
Yes. The answer is yes. The pretax margin will expand over time with scale. And to your point, our intention is not to manage it on a quarter-by-quarter basis. It's to make investments over the long term. You've seen us make those investments across our channels, Workplace, self-directed and advisory. That increases the breadth of the funnel, moves it to fee-based, and we see an expansion of margins since the beginning -- this inception of this larger business model well over a decade ago.

**Ted Pick** (Executives):
I mean, Ebrahim, just to add to that, we have -- we've really tried to be very disciplined about the slide deck and these targets, these objectives, and to really meet them and beat them. And as you know, 5 quarters of above 20% ROTCE, and some would say, okay, then are you going to raise that? And then you're at 30%, are you going to raise that? And we're really trying to, again, speak to, as you know, the core of our very long-term real money shareholder base. They want multiple year returns, higher highs, higher lows in all seasons.
Now obviously, if we're risk-off and things are really tough and the glass is more than half empty, it's 3/4 empty, we're going to be slower because there's going to be less to do. But this idea of having something that really is close to all-weather, but then can actually power higher over time just on scaling, and the ability to actually activate the funnel, that is what the team is most focused on. So if there was one statistic of all of the sea of statistics, and I know that the market backdrop in the last couple of days has been more mixed, but if there's one takeaway, it's $1 trillion of net new assets over the last 3 years, which was preceded by $1 trillion of net new assets in the preceding 3 years.
And the key then is, will those assets make their way ultimately to fee-based flows into the financial adviser? And in many cases, yes. And the ability for us to, with the financial adviser, monetize that singular experience and actually to have technology act as our friend here over the long expanse of time. The long expanse of time. That should create incremental operating leverage. So the answer is, ultimately, yes.

**Ebrahim Poonawala** (Analysts):
That's good color. And maybe separately, I mean, it still feels like a sandbox, but the SEC put out some rules around tokenized equities. Just talk to us, what does that mean for your business? How are you investing and the ability of the firm to, one, defend share, gain share if we move, if it gains steam as far as just broad-based tokenization of equities is concerned?

**Sharon Yeshaya** (Executives):
Sure. I think that Ted, in one of his comments, said, we're excited about the future of wealth and investing in this, what does it mean to think about the future of Wealth Management? The tokenized world is just a portion of that, and the tokenized world means it's faster and easier to move assets around, and you will need advice to think about those assets and how do you move those assets quickly? What are the right assets to move? And how do you think about token usage? So from our perspective, it's just an opportunity, another opportunity that we've been investing in. We've been investing in the digital space more broadly across both wealth and ISG, and I think we'll continue to be a leader, specifically as investors and clients demand advice.

**Operator** (Operator):
Our next question comes from Devin Ryan with Citizens Bank.

**Devin Ryan** (Analysts):
I want to start on institutional equities. Obviously, as we continue to see these really impressive results come through, revenues are almost double where they were in 2024. I think a lot of us and clients are trying to understand or better contextualize the cyclical versus secular elements. And obviously, we see the largest firms consolidating share. The prime businesses are doing great. And it seems like geographies like Asia are structurally larger. But can you help us unpack, like, from your lens, how much of this feels cyclical versus just you're seeing a bigger pie, and there's new areas that are contributing that weren't historically, and you're gaining market share in those areas?

**Ted Pick** (Executives):
Well, we're still in a stock-based world. Equities are still, all things being equal, the attractive asset class. The question would be if interest rates were to back up further and it would start pinching corporate earnings, would you see earnings multiple contraction, and then it becomes less attractive to be allocated to equities. I mean just sort of vanilla. But we're still in an equities world, and we're seeing growth, and we're seeing the returns on capital being generated by very healthy large-cap corporates. So when you put that together with the need for private equity and other private capital underwriters to effectively harvest their portfolio through the public markets, that is all kind of in our favor.
If we go way back in time, this is, I guess, 15 years ago, when we created the 9 boxes, cash, derivatives and prime brokerage in the 3 regions, we were recovering post-GFC, and we got the prime brokerage piece right early because we had world-class technology in MSET that linked us to a world-class high-touch cash product. That continues today. You see it in our mandates to stabilize IPOs. You see it in our ability to work large transactions for asset managers. You see it in our ability to deliver research content.
What's changed here in recent years under the leadership of Alan and Gokul is really the build-out of a world-class derivatives business. This was something that I just didn't get done, and they have figured it out. It's really the missing link in a world that has gone way beyond cash product to hedge, to express a customized view. It's a global business, and they've done a wonderful job knitting cash to prime brokerage through the derivatives product. 
So in that sense, I'd say the equities business is more robust than it was 7 or 8 years ago. But it would be silly to say that it's not subject to cycles and investor sentiment. We saw in September when volumes were drying up in Asia, and that became sort of the re-underwriting moment in the U.S. Of course, the volumes are lower, which means the output is going to be lower for everybody in the ecosystem. But we clearly have found a position now that's an enviable one, where we act as a trusted adviser now in the secondary context to asset managers across the 9 boxes. 
And here, a little like wealth, actually much like wealth, scale is existentially important. You have to be faster, better, cheaper, in addition to having the ability to get the trust of the client, and you got to be global, which is why it matters that we are -- we're big in London and we're big in Paris, but so too, in Hong Kong, Tokyo, in Seoul, in India and, of course, in the U.S. So it's a business that I think inures the benefit of the largest players, and we will continue to focus on scaling that. We're also very focused on use of capital. 
One of the underlying themes of today for us, in addition to the $1 trillion every 3 years, and I know there's a potential for distraction with all that's going on in the world, and the whole group reporting, is the fact that we have a 300 basis point CET1 buffer. That is not a small matter. That is something we have worked to achieve assiduously at the top of house in partnership with the business unit. And of course, there are other ways to measure usage, SLR, and the like, but we like the capital buffer because it, in different periods, will allow us to actually put more capital to clients through the equities and fixed income businesses when the opportunity arises.

**Operator** (Operator):
[Operator Instructions] Our next question comes from Chris McGratty with KBW.

**Christopher McGratty** (Analysts):
Just going back to the prior question. So it's more of a geography capital allocation. Like, where are you most excited about in the next couple of years to lean into capital allocation, domestically, internationally, by product? So maybe just a few comments there would be great.

**Ted Pick** (Executives):
I'll take a crack at it. I'm interested. Sharon will improve my answer. I think the answer geographically is a global allocation. I think part of this is, you can't decide you wanted to be big in Hong Kong over the last 3 years. You already were in Hong Kong for the last 20, 25 years with a world-class team or you weren't. And we have been there. Tokyo, of course, is super hot. We've been there with our partners at MUFG. We have the largest capital markets franchise in Japan, both clearing FX and also working in the equity space amongst the global firms. And you sort of go down the tick list. A number of us have been in Europe the last couple of weeks, need to be big across the U.K. and the continent.
And of course, the U.S. continues to be fertile, especially in a world of dispersion where you want to own new issues and have performance that is just beyond beta. So I think the answer is a geographic matter. We've had edge in Asia for sure, but I think the answer is global. And again, I would give a similar answer with respect to the products. I think it's the integrated solution across cash, derivatives and prime brokerage. I don't think you can just be the prime broker of choice. You have to have proper risk management and margin around the right clients. And you need to be able to monetize them not just through the financing product, but through your ability to execute low and high-touch cash and the derivatives product as well.
And I would add that what's most critically important in this period is the integration across the markets businesses. Some clients, and this goes back to some of the AI questions, it isn't just a banking phenomenon. It becomes a fixed income secured lending -- securitized lending phenomenon where we have a world-class group. So the micro and macro and commodities folks working closely with equities in an integrated markets offering where folks have sat in each seat and they want to generate the best risk-adjusted return for the client. That's something that is not just kind of a technocratic exercise, but also a behavioral one and something that is tried and true here because people get along real well, and that actually matters and the clients see it.

**Operator** (Operator):
Our next question comes from Erika Najarian with UBS.

**L. Erika Penala** (Analysts):
Just to take a step back, Ted, you're asked a lot about the pipeline as it relates to the AI super cycle, and I appreciate your prepared remarks. Just to zoom in on this a little bit. Clearly, the equity market or at least bank investors are starting to worry about the impact of sustainably higher rates, obviously both in the direction of the Fed and the 10-year. And as you talk to your clients broadly across sectors and across the type of capital need, how are higher rates and the sort of sustained level in the 10-year impacting, if at all, sort of their decisions in terms of capital raising?

**Ted Pick** (Executives):
An excellent question. It's not just higher nominal rates, as you're saying, it's also higher real rates. And the reality that the cost of capital is nothing like it was during a financial repression or the years following with COVID and stimulus. So you have to have real capital structure. And if it doesn't work, it's something that resembles, in some cases, an investment-grade capital structure, in other cases, a sub-investment-grade capital structure at sub-investment costs of capital on a traditional basis. If that's not working, the immediacy of the market is going to find that out. 
And we, as a structurer, as an underwriter, of course, we want to try to pick winners, and we want to be giving advice at the right place, but where we are committing capital as a lender or helping in any respect, again, putting our own balance sheet to work, this is part of the implication of double overweight. Double overweight doesn't mean just that we're going to send bankers out to try to get business, but that we are being incredibly rigorous and sharp about where we want to allocate risk capital. Where a bridge or where a relationship loan that, in theory, was a piece of debt turns into a piece of equity, which eventually gets provisioned. 
I imagine there are going to be cases where we are going to make mistakes. That is just an inevitable reality of something that is a generational change. But our job is to minimize the foolishness and to make sure that we are active and where it makes sense for us to help bridge capital. But ultimately, our value add, again, is the M&A advice, the strategic advice versus just putting a bunch of balance sheet out. But you are right, when there's elevated -- an elevated interest rate world, if interest rates are higher as a function of higher productivity and higher GDP, all is good. That is back to a world that we saw pre-GFC, where we see real GDP at 2% or 3%. 
And if this is helping stimulate that, I think that would be viewed as a very healthy and necessary phenomenon. If higher interest rates are the result of a lack of control over inflationary expectations or supply-side shocks as a result of some of the geopolitical tail risk, well, then obviously people are going to be less excited about putting up illiquid risk capital. And that's just the reality of private and public markets checking each other, and that's why we have super sharp people in our capital markets business, GCM, constantly working with the entire ecosystem to see what works, not just in the long term, but whether a market window opens or closes.

**Operator** (Operator):
We'll take our next question from Scott Siefers with TD Cowen.

**Robert Scott Siefers** (Analysts):
A little bit of a follow-up on the capital markets state of play. I do have to say the glass half full, half empty analogy is probably the clearest and most balanced short-form commentary I've heard sort of regarding where we are and can go. I was just hoping you could speak specifically to...

**Ted Pick** (Executives):
Thank you for that. Could you repeat that? I want to be sure that we -- there are probably some listeners left. Just if you don't mind, give me a read back of that.

**Robert Scott Siefers** (Analysts):
Whether you wrote it or others, it was...

**Ted Pick** (Executives):
No, I wrote it. I wrote it. No Chat, it's me.

**Robert Scott Siefers** (Analysts):
Well done.

**Ted Pick** (Executives):
Middlebury College.

**Robert Scott Siefers** (Analysts):
Excellent. Excellent. I was hoping you could speak to the backlog in sponsor mandates specifically. That's an area that hasn't necessarily ebbed and flowed as much. Feels like it's been more of a waiting game for the last couple of years. How does that logjam break? What's sort of hold up as you see it? I mean is the answer the same as what you just said in response to the last question? Or is it anything different as you see it?

**Ted Pick** (Executives):
Yes, I'll give you 2 answers on that. The first one is that at some point, the piper must be paid, i.e., the investment portfolio needs to be harvested. On the other hand, there's been, of course, a ton of engineering, continuation funds, the ability to put some assets in new funds. And in fairness, there are some very smart private equity investors and others in the private universe who have decided they actually want to keep some of these investments on their balance sheet, that these investments work in a higher interest rate world, back to Erika's question, and that actually, over time, if they can generate low to mid-double-digit IRRs with whatever they think is the appropriate leverage. Maybe they want to keep it for themselves or maybe they want to bring the harvesting out later. That's my positive response. 
My less positive, less salutary response would be it is a little frustrating. There are some sponsors in the universe that are stuck on marks and MOICs that are just not going to come to pass, given the market is very sharp to what is in folks' portfolio and very sharp to the reality of what the new weighted average cost of capital regime is around the world, and what incremental country risk or supply risk or AI risk means for that asset. 
So the question is going to be, at what point are they going to come and how are they going to come? And I think, in some cases, the leading private equity firms and others have been incredibly smart and agile about bringing some stuff that maybe doesn't have a higher mark, but is ready for prime time and maybe they bring that along with stuff that is a big winner, so they've had sort of portfolio composition mix. And then in other cases, they're holding on and hoping for better. And I think it is probably a longer odds bet that we are going to have a low interest rate, low inflation, nonrecessionary environment. I think that I would not bet on that.
In which case, you really have to think about what old-school corporate finance looks like for these companies. And I think the smartest and most important private equity partners that we have will be continuing to find ways to bring these companies to market against a favorable regulatory backdrop, whether they IPO them or go the M&A route. 
So in short, I think it is with some conditionality here, I continue to think it is a positive tailwind where perhaps I was mistaken was a couple of years ago, thinking it might lead the corporate finance life cycle. It's very clear to all of us that it's the strategic, real corporate universe that's leading the life cycle and the sponsors have to hustle to keep up with, effectively, the strategic bid and the strategic demand for capital.

**Operator** (Operator):
We'll take our next question from Ben Gerlinger with Citi.

**Benjamin Gerlinger** (Analysts):
Well, it's admittedly not the easiest or best way to look at your franchise versus others, but if you just look at league tables of equities or FICC or Investment Banking, you guys have stood out well in the areas that have been strong. And obviously, not trying to say the pie's gotten bigger, so you've clearly made strategic investments. But when we look at you guys versus peers within FICC itself, it seems like you have excess capital and you have a unique funding opportunity in front of you. But is FICC an area where there's a substantial amount of investment opportunity to take market share? Or is it an area more so focused on equities because equity is on a global scale, has so much more expansionary opportunity in front of it?

**Ted Pick** (Executives):
Appreciate the question. The -- as you may recall, there was a time when fixed income was an Achilles' heel of the Morgan Stanley Investment Bank dating back 15 years. And what is extraordinary about the leadership that Jay and Jakob have brought to bear is the utter stability of this business against some headwinds and crosswinds. These folks are generating efficient returns on capital and $2 billion a quarter. There was a time when we wanted to get to $1 billion a quarter.
Importantly, the business is integrated with Investment Banking and capital markets on the private side and equities in a way that this institution has never seen, which is an extraordinary thing. So there is a lot of time that is spent helping to prosecute equities product or banking product that may not book into fixed income as an external segment matter, but absolutely books existentially in the underwriting line, the advisory line, the equities line. So I think it is a world-class business.
We are not a traditional natural in the sense we're not a commercial bank, dating back to all that. But given the work that we've done to bring assets on the bank, and given now the cost of funding is more pari passu with the group, and given the talent we have, and given the importance of the AI ecosystem, and importantly, that we've built the product out globally, I think our commodities business with the 2 Nialls, our macro business and our micro business, Salva in Europe and others, these are folks that get the entire proposition of the integrated firm, and it's a business that we will continue to invest in over time.

**Operator** (Operator):
Ladies and gentlemen, this concludes today's conference call. Thank you for participating. You may now disconnect and have a great day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MS_Q2_2026_Earnings_Call_20260715.md
- 2026-07-15｜Sharon Yeshaya (CFO)｜guidance：CFO 對第三季財富管理 NII 的指引：小幅季增。（原話："we expect a modest sequential increase in NII."）
- 2026-07-15｜Sharon Yeshaya (CFO)｜guidance：CFO 重申全年稅率區間 22%–23%。（原話："expect our annual tax rate to be between 22% and"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜guidance：CFO 稱投行展望正面、pipeline 健康。（原話："The Investment Banking outlook is constructive and"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：財富管理稅前利潤率 30.5%。（原話："The pretax margin was 30.5%, a reflection of the scale"）
- 2026-07-15｜Ted Pick (CEO)｜margin：CEO 說 30% 是已達成多次的基準，但不是求解目標。（原話："30% is a benchmark now we've hit a number of times"）
- 2026-07-15｜Ted Pick (CEO)｜margin：CEO 稱若門檻不足、有需要才會調高，留待年底處理。（原話："the margin hurdle is not enough, and we want to take it up"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：CFO 報上半年效率比 65%。（原話："efficiency ratio was 65%."）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：NII 優於預期，原因為掃入餘額與放款成長。（原話："NII outperformed on higher-than-expected sweep balances"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：其他收入虧損主因為待售企業貸款的評價損失（含避險）。（原話："mark-to-market losses on corporate loans held for sale"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜margin：外匯波動度處於歷史低點附近，外匯收入下滑。（原話："where volatility traded near historic lows."）
- 2026-07-15｜Ted Pick (CEO)｜commitment：CEO 說年中不調整策略目標。（原話："not moving the targets during the course of the year,"）
- 2026-07-15｜Ted Pick (CEO)｜commitment：CEO 重申「更高的高點與更高的低點」。（原話："delivering higher highs and importantly, higher lows"）
- 2026-07-15｜Ted Pick (CEO)｜commitment：CEO 稱下一塊錢資產優先投入整合式公司。（原話："the next dollar of assets should go straight into feeding"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜capital_allocation：CET1 比率季末 14.8%。（原話："our standardized CET1 ratio ended the quarter at 14.8%."）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：宣布季股息調升 15% 至 1.15 美元。（原話："a 15% increase in our quarterly dividend to $1.15 per share."）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：CEO 稱超額 CET1 約 300–350 bps。（原話："300 to 350 basis points of excess CET1 capital depending"）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：CEO 稱對資本運用「相當嚴格」，不每季擠壓到極限。（原話："But we are quite ruthless about how we are playing this"）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：CEO 稱目前偏向有機成長而非併購。（原話："the bias continues to be to go organic."）
- 2026-07-15｜Ted Pick (CEO)｜capital_allocation：併購門檻：策略合理性與文化契合。（原話："cultural fit continue to be threshold criteria"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜customer：CFO 稱職場通路涵蓋前 100 大獨角獸約 70%。（原話："we have about 70% of the top 100"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜customer：IPO 的股票計畫資金流占本季淨新增資產略過半。（原話："Stock plan IPO flows represented just over half of"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜customer：客戶關係達 2,000 萬。（原話："We're currently at 20 million relationships."）
- 2026-07-15｜Sharon Yeshaya (CFO)｜competition：回應小型 RIA 低價競爭：CFO 稱小機構無此廣度。（原話："institutions, they will not have that type of breadth."）
- 2026-07-15｜Ted Pick (CEO)｜competition：CEO 稱融資提供者有一些定價槓桿，但生態系內資本充裕者多。（原話："I would say there is some pricing leverage"）
- 2026-07-15｜Ted Pick (CEO)｜competition：CEO 強調亞洲業務，與 MUFG 合作。（原話："But we're also an Asia house, very much an Asia house."）
- 2026-07-15｜Sharon Yeshaya (CFO)｜product：Parametric 管理資產規模。（原話："$760 billion in AUM today."）
- 2026-07-15｜Ted Pick (CEO)｜risk：CEO 估 AI 資本支出進度約 10%–15%。（原話："around 10% to 15% of the way through the investment cycle."）
- 2026-07-15｜Ted Pick (CEO)｜risk：CEO 承認可能出現科技與電力瓶頸。（原話："there will be technology and power bottlenecks"）
- 2026-07-15｜Sharon Yeshaya (CFO)｜risk：CEO 稱 sponsor 週期尚未完整出現。（原話："we have not yet seen that complete"）
- 2026-07-15｜Ted Pick (CEO)｜risk：CEO 描述經濟背景。（原話："the economy is in great shape."）

### 問答異常語氣（迴避／改口／保留）
- MS_Q2_2026_Earnings_Call_20260715.md｜問：Poonawala：財富管理稅前利潤率是否會走向 30% 中段？｜答法：CEO 未給方向或數字，回到不在年中調整目標、30% 非求解目標，留待年底。
- MS_Q2_2026_Earnings_Call_20260715.md｜問：Mayo：以 10 兆美元 AI 資本支出為例，MS 在募資中占幾成？｜答法：CEO 明說 I wouldn't attach a percentage to it，只稱 meaningful。
- MS_Q2_2026_Earnings_Call_20260715.md｜問：Schorr：為何維持高資本而不更積極運用？｜答法：CEO 未給回購節奏或數字，改談客戶需求、緩衝價值與有機優先。

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
{"date":"20260716","verdict":"觀望","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"WM 年金流第二曲線兌現（客戶資產 $10T→$12T+、pre-tax margin 守 ~30%）","columns":{"2Y 驗證":"FY26–27 WM rev YoY ≥ 8%，NNA ≥ $50B/季","5Y 驗證":"FY30 WM+IM 客戶資產 ≥ $12T","10Y 驗證":"FY35 財管費收占 group rev > 55%","數字門檻":"NNA 維持 $200B+/年；WM margin ≥ 28%","來源":"Q2 26 法說 + 2Q26 ARS","漂移觸發（QC-35）":"連 4 季 NNA"}},{"id":"H2","text":"機構證券週期上行支撐 group ROTCE 高位（但本假設本質是週期性，非結構）","columns":{"2Y 驗證":"FY26 IS rev 維持 $40B+","5Y 驗證":"FY30 IS through-cycle ROE ≥ 14%","10Y 驗證":"2030+ IB fee pool 正成長","數字門檻":"IS 季 rev 不連 2 季 YoY","來源":"Q2 26 法說（IS $11.0B 紀錄）","漂移觸發（QC-35）":"連 2 季 IS rev TTM 偏離 ≥ 5% → 削弱（2Y 假設）"}},{"id":"H3","text":"估值：market 持續 capitalize peak-cycle ROTCE，P/TBV 守 3.5–4.4x（本假設是本裁決最脆弱環節）","columns":{"2Y 驗證":"P/TBV 2026 不破 3.2x","5Y 驗證":"5Y 末 P/TBV ~3.0–3.5x（視 through-cycle ROTCE）","10Y 驗證":"through-cycle ROTCE ≥ 18%","數字門檻":"正常化 ROTCE ≥ 18%","來源":"GuruFocus P/TBV + ROE-P/B regression","漂移觸發（QC-35）":"連 4 季 TTM ROTCE 偏離 ≥ 5% → 削弱（5Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"WM NNA 從 $148B 高位失速 → 財管年金曲線 thesis 受重創","columns":{"對應":"H1","時間尺度":"⚡ 短期（1–2 季）","監測":"季度 NNA 金額","警戒閾值":"連 2 季"}},{"id":"R2","text":"capital-markets 週期 2026H2–2027 反轉 → IS rev 失墜、blended ROTCE 從 27% 回落 → §12 核心矛盾兌現","columns":{"對應":"H2 / H3","時間尺度":"週期（2–5 季）","監測":"IS 季 rev YoY + P/TBV","警戒閾值":"IS 連 2 季 YoY"}},{"id":"R3","text":"AML 監管程序升級（FinCEN/OCC/SEC/FINRA 客戶審查 2021–2024 窗）→ consent order + 罰金 + 財管展業限制","columns":{"對應":"治理","時間尺度":"事件（不定）","監測":"docket 進展 / 8-K 揭露","警戒閾值":"升級為 consent order 或罰金 > $500M"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"P/TBV 回落至 ≤3.3x（≈$180，等 warranted 錨）或 through-cycle ROTCE 連 3 季 >20%（弱市確認結構性步階）或 SEC/FinCEN/OCC AML 程序結案","irr_base_pct":5.5,"ev5y_pct":21.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"核心","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.5,"ev5y_pct":21.0,"irr_base_pct":5.5,"max_dd_pct":-55.0,"bull_5y_price":389.0,"bear_5y_price":142.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"P/TBV 回落至 ≤3.3x（≈$180，等 warranted 錨）或 through-cycle ROTCE 連 3 季 >20%（弱市確認結構性步階）或 SEC/FinCEN/OCC AML 程序結案","price_at_dd":228.55,"archetype":"金融","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MS_20261018/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
