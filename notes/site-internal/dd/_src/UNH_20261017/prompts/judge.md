你是 stock-analyst **v20 判斷 agent**，標的 UNH（20261017）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"UNH","date":"2026-10-17","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UNH_20261017/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UNH_20261017/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":112694,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP（調整後）營業利益／利益率","value":6265,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"百萬美元；利益率 5.6%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":6563,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"百萬美元；利益率 5.8%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi6_fy2026","label":"管理層全年指引（FY2026）","value":"調整後 EPS ≥20.50；GAAP EPS ≥19.50","period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi7_mcr","label":"醫療成本率 MCR","value":88.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi8_unitedhealthcare","label":"UnitedHealthcare 服務人數","value":48.3,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"百萬人","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi9","label":"調整後每股盈餘","value":4.69,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi10_optum_rx","label":"Optum Rx 調整後處方量","value":393,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"百萬張","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-13","period":"2026-10-13","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-13"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_unh_gross_margin_pct","label":"UNH 毛利率","value":19.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UNH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_unh_operating_margin_pct","label":"UNH 營業利益率","value":4.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UNH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_unh_fcf_margin_pct","label":"UNH FCF 利潤率","value":5.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UNH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_lly_gross_margin_pct","label":"LLY 毛利率","value":83.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lly_operating_margin_pct","label":"LLY 營業利益率","value":49.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lly_fcf_margin_pct","label":"LLY FCF 利潤率","value":17.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvo_gross_margin_pct","label":"NVO 毛利率","value":80.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvo_operating_margin_pct","label":"NVO 營業利益率","value":43.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvo_fcf_margin_pct","label":"NVO FCF 利潤率","value":14.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_stvn_gross_margin_pct","label":"STVN 毛利率","value":29.17,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STVN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_stvn_operating_margin_pct","label":"STVN 營業利益率","value":17.37,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STVN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_stvn_fcf_margin_pct","label":"STVN FCF 利潤率","value":-2.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STVN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3","label":"營運現金流（單季）","value":5.1,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","unit":"十億美元（1.2x 淨利）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi4_ocf_capex","label":"自由現金流（前九個月，OCF-capex）","value":22666,"period":"2026 前九個月（截至 2026-09-30，公告於 2026-10-13）","unit":"百萬美元（OCF 25,087 − capex 2,421）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"2026 前九個月（截至 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}},{"id":"f_kpi5_sbc","label":"股權激勵費用 SBC（前九個月）","value":843,"period":"2026 前九個月（截至 2026-09-30，公告於 2026-10-13）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"2026 前九個月（截至 2026-09-30，公告於 2026-10-13）","citation":"SEC 8-K 財報新聞稿 https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm（UNH 官方新聞稿，2026-10-13）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":401.43,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":25.13,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":63.28,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（19.87 → 19.87）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.61 → 22.61）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（26.18 → 26.18）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":19.87,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":22.61,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":26.18,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":7.52,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 18.48 → 19.87（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":25.82,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝44.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":44.1,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.8,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝19.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":19.8,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.9,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝17.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":17.3,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.09,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 19.87，分子＝快照價 379.3","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.257,"period":"2026-10-17","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-17"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":45782.0,"period":"2026-10-17","unit":"USD m","basis":"yfinance 最新一季：總債務 74331.0、現金 28549.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":897.59,"period":"2026-10-17","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":406103.48,"period":"2026-10-17","unit":"USD m","basis":"市值 360321.48 ＋ 淨負債 45782.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":448670.65,"period":"2026-10-17","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":463782.06,"period":"2026-10-17","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.91,"period":"2026-10-17","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-17"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"搜尋摘要稱 UNH 2026 年 Medicare Advantage 份額由 29% 降至 26%，Humana 由 17% 升至 20%；2025→2026 UNH 流失約 64.7 萬 MA 會員（來源為 Becker's／KFF／Mark Farrah 彙整，摘要未標精確日期）","source":"Becker's Payer, 10 key Medicare Advantage numbers to know in 2026","url":"https://www.beckerspayer.com/?p=25640","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Fierce Healthcare 標題：UnitedHealthcare 預期今年流失 130 萬 Medicare Advantage 會員（公司預測，非已實現數字）","source":"Fierce Healthcare, UnitedHealthcare expects to lose 1.3M Medicare Advantage members this year","url":"https://www.fiercehealthcare.com/payers/unitedhealth-shares-fall-premarket-company-misses-revenue-releases-2026-outlook","excerpt":"UnitedHealthcare expects to lose 1.3M Medicare Advantage members this year","as_of":"2026-01-27","retrieved_at":"20261017","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"AMA 集中度分析（約 2024 年資料）：UNH 商業保險份額約 16%，Medicare Advantage 約 30%、Humana 19%、Aetna 12%、Elevance 5%；2026 年無完整五家份額序列","source":"Fierce Healthcare, AMA: A look at concentration in commercial insurance, MA markets","url":"https://www.fiercehealthcare.com/payers/ama-look-concentration-commercial-insurance-ma-markets","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Hudson Labs 2026 同業頁列 Cigna、Centene 等為對手，稱 UNH 產品廣度與 Optum 整合帶來規模與技術優勢；未點名新進入者。2026 年搜尋未找到新進入者或替代者搶單的報導（新進入者相關結果多為 2016–2022 舊文）","source":"Hudson Labs, UnitedHealthcare competitors UNH peers 2026","url":"https://www.hudson-labs.com/research/unitedhealthcare-competitors-unh-peers-2026","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"sec-api.io 對 FY2025 10-K 的分析稱單一交易對手 CMS 占約 44%（第三方數字，未在 10-K 原文核實）；FY2025 總營收 $447,567M、保費 $352,229M","source":"sec-api.io, Financial analysis of UnitedHealth Group FY2025","url":"https://sec-api.io/insights/financial-analysis-of-unitedhealth-group-fy2025","excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"UnitedHealthcare Medicare & Retirement 2025 全年營收 $171.3B，約占合併營收 38%（含非 CMS 收入）","source":"UnitedHealth Group Reports 2025 Results and Issues 2026 Outlook (BusinessWire)","url":"https://businesswire.com/news/home/20260126830491/en/UnitedHealth-Group-Reports-2025-Results-and-Issues-2026-Outlook","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261017","affects":["thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025 年 Moody's、S&P、Fitch 皆將 UNH 展望調為負面並維持評級；S&P 維持 A+，AM Best 下調母公司長期發行人評級至 a-（展望穩定）。搜尋未見 2026 年新評級行動","source":"Becker's Payer / fi-desk / BusinessWire (AM Best)","url":"https://www.beckerspayer.com/?p=16263","excerpt":null,"as_of":"2025-08-28","retrieved_at":"20261017","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"UNH 2026 定價假設醫療成本趨勢近 10%，並退出涵蓋逾 60 萬會員的方案以保護利潤率","source":"Becker's Payer: UnitedHealthcare's 'deliberate trade-off' for margin recovery","url":"https://www.beckershospitalreview.com/finance/unitedhealthcares-deliberate-trade-off-for-margin-recovery/","excerpt":"For 2026 pricing, UnitedHealth assumed trend approaching 10%—and made the difficult decision to exit plans serving over 600,000 members to protect margins.","as_of":"2026-04-21","retrieved_at":"20261017","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"2026 年第一季財報電話會議：UNH 預期 2027 年 Medicare Advantage 會員數減少約 130 萬，以會員數換利潤率；MA 成本趨勢仍高但符合定價假設","source":"Managed Healthcare Executive: 4 takeaways from UnitedHealth Group's first quarter earnings call (April 21, 2026)","url":"https://www.managedhealthcareexecutive.com/view/4-takeaways-from-unitedhealth-group-s-first-quarter-earnings-call","excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261017","affects":["thesis.R","valuation","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"CMS 2027 MA 給付預告僅 +0.09%，市場原預期 4–6%，引發管理式醫療股拋售；後續最終費率報導為平均 +2.48%","source":"Wedbush/MarketMinute: Rate Shock: 2027 Medicare Advantage Proposals Trigger $80 Billion Sell-Off in Managed Care；Nasdaq: UnitedHealth Jumps on CMS' MA Rate Boost","url":"https://investor.wedbush.com/wedbush/article/marketminute-2026-1-27-rate-shock-2027-medicare-advantage-proposals-trigger-80-billion-sell-off-in-managed-care","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261017","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Humana 表示進入 2027 投標週期時，MA 給付與醫療成本趨勢的缺口比前一年更寬，並預期 2027 年 MA 方案退出影響約 60 萬會員","source":"Becker's Payer: Humana to exit Medicare Advantage plans covering 600,000 members in 2027","url":"https://www.beckershospitalreview.com/finance/humana-to-exit-medicare-advantage-plans-covering-600000-members-in-2027/","excerpt":"the company said the gap between MA funding and its medical cost trend was wider heading into the 2027 bid cycle than a year earlier and would require benefit and geographic adjustments","as_of":"2026-08-01","retrieved_at":"20261017","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Evercore ISI 預期使用率 2026 年維持高檔，同業顯著改善自 2027 年起可見；UNH、Elevance、Centene、Molina 在 Q2 表示 Medicaid 利潤率 2027 將回升","source":"S&P Global Market Intelligence: US health insurers raise outlooks despite Q2 cost rises, shifting membership (2026-08-17)","url":"https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/8/us-health-insurers-raise-outlooks-despite-q2-cost-rises-shifting-membership-105000456","excerpt":null,"as_of":"2026-08-17","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"BofA 預期 2027 年風險池再有較小的負向轉移、風險池穩定最可能在 2028；CMS 編碼變更若依提案定案將延後回到目標利潤率至 2028 年或更晚；Medicaid 利潤率恢復可能延至 2029–2030","source":"BofA Global Research: Managing headwinds in managed care (Kevin Fischbeck)","url":"https://business.bofa.com/en-us/content/managed-care-earnings-kevin-fischbeck.html","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"WSJ 報導（2024 年 2 月）：美國司法部對 UnitedHealth 展開反壟斷調查，聚焦 UnitedHealthcare 保險與 Optum 醫師集團的關係；搜尋結果未見該調查的 2026 年結案或起訴結果。","source":"KFF Health News Morning Breakout / Star Tribune：DOJ antitrust investigation at UnitedHealth Group","url":"https://kffhealthnews.org/morning-breakout/unitedhealth-under-antitrust-investigation-by-doj-report/","excerpt":null,"as_of":"2024-02-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"DOJ 2025 年 8 月起訴阻止 UnitedHealth 收購 Amedisys（33 億美元），後與雙方達成和解，交易得以進行。","source":"CRA 競爭團隊案例頁／RACmonitor：DOJ files suit against UnitedHealth Group","url":"https://www.crai.com/engagements/cra-competition-team-advises-unitedhealth-group-clearing-path-for-amedisys-acquisition/","excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261017","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"DOJ 調查 Medicare Advantage 潛在詐欺（含民事與刑事調查），尚無正式起訴、無高管被指控；Zacks 2026 年中文章稱相關調查可能帶來標題風險與合規成本。","source":"Zacks：UnitedHealth's cost control story is gaining momentum; TipRanks; Daily Insurance Report","url":"https://www.zacks.com/stock/news/2963566/unitedhealths-cost-control-story-is-gaining-momentum-time-to-buy","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FTC 胰島素訴訟對象含三大 PBM（Optum Rx、CVS Caremark、Express Scripts），指控偏好高價胰島素以賺取回扣；UNH 同時轉向透明費用制 PBM 模式。","source":"Barchart／TipRanks 等聚合報導（UnitedHealth regulatory scrutiny 搜尋結果）","url":"https://www.barchart.com/story/news/36997776/unitedhealth-faces-renewed-scrutiny-into-its-nursing-home-practices-what-does-that-mean-for-unh-stock","excerpt":null,"as_of":"2025-09-01","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-04-02 公告對特定專利藥及其原料課 100% Section 232 關稅；有核准在美設廠計畫者 2026-09-29 起適用 20%，簽 MFN 定價協議者可適用 0%。搜尋結果未提及 UNH 本身，僅為藥品成本的間接通道（藥局福利管理業務），此連結為搜尋者推論，非來源所述。","source":"KPMG, United States: Section 232 tariff on pharmaceutical ingredients","url":"https://kpmg.com/us/en/taxnewsflash/news/2026/04/united-states-section-232-tariff-pharmaceutical-ingredients.html","excerpt":null,"as_of":"2026-04-02","retrieved_at":"20261017","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"KFF 報導：UnitedHealthcare of Oregon 在 2026 費率申報中納入 2.20% 關稅／回流不確定性價格影響，UnitedHealthcare of New York 等載體加計約 2.4%–3.6% 藥品關稅影響；零售處方藥約占私人健保支出 12%。","source":"KFF, Tariffs Are Driving 2026 Health Insurance Premiums Up","url":"https://www.kff.org/quick-take/tariffs-are-driving-2026-health-insurance-premiums-up/","excerpt":null,"as_of":"2025-08-01","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"搜尋未發現 UNH 被列入 BIS Entity List 或有任何出口管制行動；僅見 UnitedHealthcare 網站條款中的標準出口禁運條款。","source":"Conduct Atlas, UnitedHealthcare terms of use provision record","url":"https://conductatlas.com/platform/unitedhealthcare/unitedhealthcare-terms-of-use/prohibition-on-export-to-embargoed-countries/","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261017","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"二手風險彙整站稱 Change Healthcare 因服務集中而形成單點失效；該事件為 2024-02-21 的勒索軟體攻擊（網路安全面的集中風險，非地緣）。來源為二手聚合站，as_of 取事件日。","source":"Rankiteo, Optum company risk page","url":"https://scoringcyber.rankiteo.com/company/optum","excerpt":"With a single point of failure due to consolidated services, a large portion of health systems and patient care became vulnerable to cyber threats.","as_of":"2024-02-21","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026：合併營收約 $112.7B（去年同期 $113.2B）；UnitedHealthcare 營收 $86.3B 微降，醫療保險會員 48.3M（去年 50.1M），營收下滑主要來自 Medicare 業務收縮；營運利益率 3.3%（去年 2.1%）。","source":"UnitedHealth Group Q3 2026 8-K earnings release（SEC）／Fierce Healthcare／Quiver Quant 摘要","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm","excerpt":"Operating earnings totaled $6.6 billion, compared to $4.3 billion in the prior-year quarter.","as_of":"2026-10-15","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 2026：Optum Health 營收年減 10% 至 $22.9B（價值型照護服務病患減少），營業利益 $735M（去年 $41M）；Optum Insight 營收 +3% 至 $5.5B；Optum Rx 營收 $39.9B（去年 $39.7B，近乎持平）。","source":"UnitedHealth Group Q3 2026 8-K earnings release（SEC）","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/earningsrelease3q26unh.htm","excerpt":null,"as_of":"2026-10-15","retrieved_at":"20261017","affects":["thesis.H","thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Q2 2026：Optum Health 營收年減 5% 至 $23.5B，約少服務 70 萬名價值型照護病患，營業利益率 5.1%；Optum Insight 營收 $5.4B；Optum Rx 營收 $38.3B（去年 $38.5B）。","source":"UnitedHealth Group Q2 2026 8-K earnings release（SEC）","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000191/earningsrelease2q26_7152.htm","excerpt":"Optum Health's second quarter 2026 revenues of $23.5 billion decreased 5% year-over-year due to ~700,000 fewer value-based-care patients served.","as_of":"2026-07-15","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"Q2 2026：合併營收與去年大致持平，UnitedHealthcare 營收持平、Optum 營收下降 2%；醫療成本率 86.7%（去年 89.4%），含 $860M 有利前期準備金調整。","source":"UnitedHealth Group Form 10-Q（2026-06-30）","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000197/unh-20260630.htm","excerpt":"Consolidated revenues were consistent, with UnitedHealthcare revenues flat and Optum revenues lower by 2%.","as_of":"2026-07-31","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"CMS 定案 2027 年 Medicare Advantage 費率 +2.48%（約 $13B），高於 1 月預告的 0.09%；公司預期 2027 年 MA 會員減少約 1.3M，並退出涵蓋約 39 萬人的方案；管理層稱 2027 年醫療成本趨勢仍高於目前保費水準。","source":"TIKR／Nasdaq 報導（CMS 2027 MA 費率定案、UNH 會員預期）","url":"https://www.tikr.com/blog/unitedhealth-trades-at-365-as-it-shuts-plans-for-390000-medicare-advantage-members-heres-what-it-signals-for-2027","excerpt":"UnitedHealth Group is shutting Medicare Advantage plans that cover about 390,000 people for 2027, a company spokesperson told Bloomberg on October 1.","as_of":"2026-10-02","retrieved_at":"20261017","affects":["thesis.H","thesis.R","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Managed Healthcare Executive 報導：雇主正繞過保險公司、直接與醫療提供者簽約，成本上升與受託責任使興趣增加（直接簽約並非新現象）。","source":"Managed Healthcare Executive, MHE March 2026","url":"https://www.managedhealthcareexecutive.com/journals/mhe-publication/mhe-march-2026","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"BCG 文章（2026年6月）指出付款方風險不在傳統式顛覆，而是競爭邊界被抹除；垂直整合的提供者可能繞過付款方，消費科技公司與 LLM 超大規模業者可能使部分市場商品化。屬策略觀點／預測。","source":"BCG, AI for Healthcare Payers","url":"https://web-assets.bcg.com/pdf-src/prod-live/ai-for-healthcare-payers.pdf","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261017","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"UNH 管理層稱 2026 年將投入近 15 億美元於 AI 相關計畫，約三分之一投 Optum Insight 軟體平台，其餘用於內部流程；報導稱 AI 工作 2027 年加速、2028 年放大；數位事前授權首次通過率 96%。為管理層自述數字。","source":"Healthcare Finance News / Constellation Research / UNH Q1 2026 earnings call","url":"https://www.healthcarefinancenews.com/news/unitedhealth-group-track-invest-15-billion-ai","excerpt":null,"as_of":"2026-04-21","retrieved_at":"20261017","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"參議員要求三大 Medicare Advantage 保險人（含 UnitedHealthcare）提供其以 AI 與事前授權拒絕老年人術後照護的紀錄；Foley 律師稱近期判決為挑戰 AI 驅動承保決定開出契約基礎路徑。","source":"搜尋摘要（UNH 2026 威脅查詢）；Foley & Lardner news 2026-01","url":"https://www.foley.com/ja/news/2026/01/mehta-and-carboni-quoted-on-major-health-care-ai-cases","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"UnitedHealth 2026 指引預期 UnitedHealthcare 會員 46.9–47.5 百萬，Optum 營收下滑與 Optum Rx 會員流失及 Optum Health 策略性縮編相連。","source":"UnitedHealth Group Form 10-K FY2025 / Q4 2025 8-K","url":"https://www.sec.gov/Archives/edgar/data/731766/000073176626000025/q42025er992.htm","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261017","affects":["thesis.R","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Q2 2026 財報稿稱 Optum Rx 轉向現代藥局照護模式：取消 spread pricing，以明定的每會員費用取代量能獎勵。","source":"UnitedHealth Group 8-K Q2 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000191/uhgearnings_q22026vpower.htm","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261017","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"2025 年 7 月法說：UnitedHealthcare 將退出 2026 年約 60 萬 Medicare Advantage 會員的方案（以 PPO 為主、逾 100 個方案、109 郡），Optum 價值型 PPO 約 20 萬病人安排終止。","source":"Fierce Healthcare / Healthcare Finance News","url":"https://www.fiercehealthcare.com/payers/unitedhealth-cuts-2025-outlook-elevated-medical-costs-continue-sting","excerpt":null,"as_of":"2025-07-29","retrieved_at":"20261017","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-10-13 公司發布 Q3 財報並上調全年指引：調整後 EPS 至少 $20.50（納入第三季經驗）","source":"SEC 8-K UnitedHealth Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000255/uhgearnings_q32026vfinal.htm","excerpt":"The company now expects full year 2026 adjusted net earnings of at least $20.50 per share, incorporating experience through the third quarter 2026.","as_of":"2026-10-13","retrieved_at":"20261017","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-07-16 Q2 後公司將全年調整後 EPS 指引上調至 $19.50–$20.00；當時彙整共識約 $18.43，指引高於共識；2026 年未見下調指引報導","source":"MarketBeat/聚合站 Q2 2026 報導；SEC 8-K Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000191/earningsrelease2q26_7152.htm","excerpt":null,"as_of":"2026-07-16","retrieved_at":"20261017","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 醫療成本率 86.7%，低於去年同期 89.4%，亦低於華爾街預期 88.47%","source":"SEC 8-K Q2 2026 / 聚合站摘要","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000191/uhgearnings_q22026vpower.htm","excerpt":"The second-quarter medical care ratio was 86.7% in second quarter 2026 compared to 89.4% in second quarter 2025.","as_of":"2026-07-16","retrieved_at":"20261017","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價分布（聚合站，口徑不一）：Barchart 2026-07 均值 $482、最高 $529；Benzinga 約 24 位分析師共識 $443（20 買 4 持有，頁面更新 2026-08-31）；春季較低（Barchart 5 月均值 $389.16、最高 $444）。Q3 後（10/13 起）最新目標價分布未查到","source":"Barchart；Benzinga UNH price-targets","url":"https://kr.benzinga.com/quote/UNH/price-targets","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-04 底 Zacks 類報告：FY2026 共識 EPS $18.12（30 日修正 +3.4%），Zacks Rank #3 持有；來源為鏡像站，可信度較低；Q3 後賣方預估修正未查到","source":"Zacks 風格報告（鏡像站）UNH Near-Term Performance Outlook","url":"https://accred.deac.org/expert-time/UnitedHealth-Group-Incorporated-UNH-NearTerm-Performance-Outlook-Amid-Strong-30Day-Price-Rally-and-Robust-Earnings-Revision-Trends-11-1985","excerpt":"That said, the Zacks Rank #3 (Hold) designation signals that the recent positive momentum may be partially priced in at current levels.","as_of":"2026-04-29","retrieved_at":"20261017","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Optum Financial 完成收購福利管理平台 Alegeus Technologies（搜尋摘要稱 7/2 完成；Q1 2026 財報稿原預期下半年交割）","source":"Becker's Payer / UnitedHealth Q1 2026 8-K earnings release (搜尋摘要)","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000121/uhgearningsreleaseq12026.htm","excerpt":null,"as_of":"2026-07-02","retrieved_at":"20261017","affects":["moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"UNH 向 SEC 揭露正面臨 DOJ 刑事與民事調查（Medicare Advantage 業務），公司表示配合調查；2026 年最新進展本次未查到","source":"MarketBeat / ABC 新聞轉載","url":"https://www.marketbeat.com/articles/unitedhealth-says-it-is-under-a-federal-investigation-and-cooperating-2025-07-24","excerpt":null,"as_of":"2025-07-24","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"多起證券集體訴訟在案：明尼蘇達案（CalPERS 為 lead plaintiff，最新修正訴狀 2025-05）與 SDNY Faller v. UnitedHealth（1:25-cv-03799）；2026 新案或裁決本次未查到","source":"Rosen Law Firm / Robbins Geller 公告 (Business Wire)","url":"https://secure.businesswire.com/news/home/20250507603891/en/EQUITY-ALERT-Rosen-Law-Firm-Files-Securities-Fraud-Class-Action-Lawsuit-Against-UnitedHealth-Group-Incorporated-UNH","excerpt":null,"as_of":"2025-05-07","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Optum Financial 完成收購 Alegeus Technologies（搜尋摘要稱 7/2 完成）；同稿另載 Optum UK 出售完成、至少 20 億美元回購安排","source":"Becker's Payer / UnitedHealth Q1 2026 8-K (搜尋摘要)","url":"https://www.sec.gov/Archives/edgar/data/0000731766/000073176626000121/uhgearningsreleaseq12026.htm","excerpt":null,"as_of":"2026-07-02","retrieved_at":"20261017","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券集體訴訟在案：D. Minn.（CalPERS lead plaintiff，class period 2021-09 至 2025-04）與 SDNY Faller（1:25-cv-03799，Judge Hellerstein）","source":"Rosen Law Firm 公告 (Business Wire)","url":"https://secure.businesswire.com/news/home/20250507603891/en/EQUITY-ALERT-Rosen-Law-Firm-Files-Securities-Fraud-Class-Action-Lawsuit-Against-UnitedHealth-Group-Incorporated-UNH","excerpt":null,"as_of":"2025-05-07","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"UNH 在 SEC 文件中揭露 DOJ 刑事與民事調查（Medicare Advantage 業務）；公司配合調查","source":"MarketBeat / HealthExec","url":"https://www.marketbeat.com/articles/unitedhealth-says-it-is-under-a-federal-investigation-and-cooperating-2025-07-24","excerpt":null,"as_of":"2025-07-24","retrieved_at":"20261017","affects":["decision_inputs.bear","thesis.R","triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"UNH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":19.51,"operating_margin_pct":4.82,"fcf_margin_pct":5.25,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UNH","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"LLY","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":83.4,"operating_margin_pct":49.72,"fcf_margin_pct":17.02,"rd_intensity_pct":18.32},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"NVO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":80.65,"operating_margin_pct":43.13,"fcf_margin_pct":14.51,"rd_intensity_pct":17.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVO","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"STVN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":29.17,"operating_margin_pct":17.37,"fcf_margin_pct":-2.51,"rd_intensity_pct":2.08},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.STVN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"1A8.DE","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.1A8.DE"},"note":"quarterly_income_stmt 無資料"}],"subject":"UNH"},"financial_history":{"ticker":"UNH","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":324162000000.0,"revenue_yoy_pct":null,"gross_margin_pct":24.56,"operating_margin_pct":8.77,"net_income":20120000000.0,"diluted_eps":21.18,"free_cash_flow":23404000000.0,"fcf_margin_pct":7.22,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":371622000000.0,"revenue_yoy_pct":14.64,"gross_margin_pct":24.48,"operating_margin_pct":8.71,"net_income":22381000000.0,"diluted_eps":23.86,"free_cash_flow":25682000000.0,"fcf_margin_pct":6.91,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":400278000000.0,"revenue_yoy_pct":7.71,"gross_margin_pct":22.33,"operating_margin_pct":8.07,"net_income":14405000000.0,"diluted_eps":15.51,"free_cash_flow":20705000000.0,"fcf_margin_pct":5.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":447567000000.0,"revenue_yoy_pct":11.81,"gross_margin_pct":18.53,"operating_margin_pct":4.24,"net_income":12056000000.0,"diluted_eps":13.23,"free_cash_flow":16075000000.0,"fcf_margin_pct":3.59,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/UNH/UNH_Q3_2026_Earnings_Call_20261013.md）

# Q3 2026 Earnings Call
**UnitedHealth Group Incorporated** | Earnings Calls | 2026-10-13

**Operator** (Operator):
Good morning, and welcome to the UnitedHealth Group Third Quarter 2026 Earnings Conference Call. [Operator Instructions] As a reminder, this call is being recorded.
Here is some important introductory information. This call contains forward-looking statements under U.S. federal securities laws. These statements are subject to risks and uncertainties that could cause actual results to differ materially from historical experience or present expectations. A description of some of the risks and uncertainties can be found in the reports that we file with the Securities and Exchange Commission, including the cautionary statements included in our current and periodic filings.
This call will also reference non-GAAP amounts. A reconciliation of the non-GAAP to GAAP amounts is available on the Financial & Earnings Reports section of the company's Investor Relations page at www.unitedhealthgroup.com. Information presented on this call is contained in the earnings release we issued this morning and in our Form 8-K dated October 13, 2026, which may be accessed from the Investor Relations page of the company's website.
I will now turn the conference over to Chairman and Chief Executive Officer of UnitedHealth Group, Steve Hemsley.

**Stephen Hemsley** (Executives):
Good morning, and thank you for joining us today. Our third quarter performance reflects actions taken throughout 2026, driving meaningful progress and reinforcing our confidence to sustainably grow in 2027 and beyond, within our 13% to 16% long-term target growth range. Our revised full year 2026 guidance reflects continuing improvements in leadership and execution across Optum and UnitedHealthcare as we better align our businesses to serve the demands of the ever-changing U.S. healthcare environment. We are accelerating the modernization of our enterprise by advancing simplified and more responsive policies, processes and tools, focusing on more effective, integrated value-based care offerings and responsibly building modern agentic infrastructure as we seek to ensure people have access to higher quality care at lower costs. And at the same time, clinicians experience a simpler, faster and more supportive system.
Across the businesses, AI-enabled capabilities are beginning to help clinicians spend more time with patients, improve service speed and experience, streamline administration and reduce friction for both consumers and clinicians. A few examples. We have expanded AI-enabled chart summarization to more than 40% of our employed clinicians, reducing chart review time by 33%. AI-enabled information gathering and research have shortened appeal cycle times by 26%, improving both member and clinician experience, and we expect this to accelerate in 2027. And for this year's Medicare Advantage annual enrollment period, we are introducing AI-powered plan recommendations that use a member's care history and local plan options to help simplify their selection.
By the end of this year, we are on track to implement all previously announced prior authorization reforms, reducing decision time lines for patients, relieving administrative burden for clinicians and delivering better experiences for people. Collectively, these initiatives will reduce total prior authorizations by 30%, including a reduction of 2/3 in prior authorizations for people under the age 18. These efforts are only the beginning. More will follow. They are central to how we are changing our enterprise to be more in line with our mission, creating greater value and positive social impact.
In that vein, an important effort is the reimagined United Health Foundation. With $1 billion committed to date, the foundation's investments, along with the dedicated operational expertise of UnitedHealthcare and Optum, can help facilitate scaled solutions to some of the U.S. health system's greatest challenges, including rural health, maternal and infant health, behavioral health and workforce education. As just one example, in Tennessee, the foundation is helping expand and operate health hubs across the state, providing access to underserved communities in preventative care and chronic condition support. We will continue to highlight the foundation as part of our commentary on our earnings calls going forward.
The broader healthcare environment remains dynamic. Policy-driven regulatory developments, changing consumer expectations and the rapid evolution of clinical care and advances in technology continue to reshape the industry. These factors are pressuring basic affordability and access as never before. Success requires continuous adaptation, and the pace is accelerating. We recognize this and remain restless in our pursuit of change and improvement. We are challenging our assumptions, revising policies and practices and repositioning leadership and capabilities to better meet the needs of those we serve and to move faster as an enterprise to adapt to the changing healthcare landscape. That includes opportunities to better align with clinical partners, employers, government benefit sponsors to help improve the experience of all stakeholders in healthcare.
We've made progress in our 2026 performance. We have much to do to approach the full potential of our mission and the positive impact we can make as an enterprise. UnitedHealth Group has a long history of evolution to meet the needs of a changing U.S. health system. We're committed to accelerating these efforts as a stronger, more capable, more mission-centered enterprise.
And with that, let me turn the call over to Tim Noel.

**Timothy Noel** (Executives):
Thanks, Steve. UnitedHealthcare is seeing positive momentum across our Medicare and Medicaid businesses, while our commercial business continues to adjust to a challenging but steadily stabilizing environment. Costs remain stubbornly high across the entire healthcare landscape and particularly in areas such as specialty pharmacy and acute healthcare service intensity. We continue to address the challenge of increasingly expensive care with appropriate medical management, operational discipline and a commitment to identify and remove excess and unnecessary costs from our own enterprise as we advance simpler and more modern services. We are working to deliver stable benefits and value for our members and customers. We believe this positions us for continued organic growth and long-term value creation entering 2027.
Let me start with our Medicare business, where the annual enrollment period begins later this week. Medicare Advantage remains the choice of well more than half of eligible American seniors as it offers better and more modern benefits and importantly, better outcomes than fee-for-service Medicare. Beneficiaries choosing Medicare Advantage save, on average, more than $4,000 annually through lower premiums and cost sharing than those on original Medicare. With adequate funding, we believe Medicare Advantage will continue to be the choice of American seniors, particularly those who are disadvantaged and have chronic care challenges as they seek better value and modern care.
Heading into 2026, we made deliberate decisions regarding Medicare Advantage benefit design and market positioning to preserve the long-term sustainability and performance of our Medicare Advantage offerings. We continued this disciplined approach for 2027. We believe we are competitively positioned, focused on providing value for seniors in the markets we serve while being mindful of trend dynamics. In 2027, UnitedHealthcare will continue to prioritize high-value HMO, Chronic Special Needs and Dual Special Needs offerings. Our commitment to serving America's seniors is clear. More than 94% of Medicare-eligible individuals nationwide will have access to a UnitedHealthcare Medicare plan, and approximately 90% of Medicare-eligible consumers will have access to one of our Medicare Advantage plans with a $0 premium option.
We are maintaining important benefits such as dental, vision, hearing and additional health and wellness offerings that make a real difference in the lives of seniors. UnitedHealthcare Chronic Special Needs Plans will be available to nearly 50 million Medicare-eligible individuals in 2027, providing specialized support for people living with conditions such as diabetes, cardiovascular disease and chronic heart failure. These plans offer benefits and access to care tailored to the unique needs of individuals managing chronic conditions, helping them connect with care, medications and support they need.
Much of this work is in coordination with our partners at Optum Health, where evidence shows chronically complex seniors served by integrated value-based care experience better preventative care while improving health outcomes at lower costs. Medicare Advantage patients in value-based care arrangements are 40% likely than traditional Medicare patients to be hospitalized for acute and chronic conditions and 40% less likely to be readmitted to a hospital within 30 days of discharge.
Moving to Stars. Our initial Star ratings for payment year 2028 reflect our investment in quality, member experience and operating execution. As we move through 2027 and into 2028, we expect to approach 75% of total members in 4+ Star plans compared to the industry average of 70%. Our team remains intensely focused on building a best-in-class consumer and clinical experience. And along with better benefit design and stability going forward, we believe those efforts will continue translating into stronger quality performance over time. We will continue to work in support of the CMS Quality Program efforts to ensure the Medicare Advantage program continues to provide quality experience and stability to the 36 million seniors who depend on it.
Turning to medical costs. The actions we've taken to improve and modernize care management, strengthen clinical engagement and enhance operating discipline are having a meaningful effect. Care intensity remains elevated relative to historical norms even as we continue to see signs that trends are bending in a more stable direction than what we have recently experienced. We remain respectful of trends and are not assuming any deceleration to historical patterns or to ongoing clinician pricing pressure. Demand for care remains strong, particularly among senior and complex populations, and we fully support appropriate access to care for our members.
Turning to the commercial business. Performance continues to stabilize as we navigate a challenging market. As we previously noted, trends for commercial benefits are exceeding our initial expectations of 11%, driven by an acceleration of costs related to the No Surprises Act, greater cost intensity from clinicians and high-cost specialty drugs. Of particular concern is the ongoing abuse of the No Surprises Act dispute process by a relatively small number of clinician groups and third-party organizations.
Arbitration awards can approach nearly 6% of total medical spend in some regions, translating to billions of dollars in excess costs for consumers, employers and the health system. The law was intended to protect patients from unexpected bills, and we strongly support that objective. We will continue working with policymakers and regulators to ensure the law functions as intended and that healthcare dollars are directed towards appropriate patient care rather than significantly inflated market arbitration awards and volumes, along with unnecessary administrative expense.
Medicaid remained stable through the back half of the year, while our team continues to drive greater operational improvements through network curation and more effective behavioral health program initiatives. These actions help to partially offset the primary variable, which continues to be the timing and adequacy of state funding across several markets. As we move through the balance of 2026, we continue to work collaboratively with our state partners to ensure rates appropriately reflect the acuity and healthcare needs of the families being served, including the impacts of regulatory actions. While progress has been made in many states, the timing of updates remains uneven.
Based on our current outlook, we continue to view 2026 as a trough year for core Medicaid margins, which we now expect to be moderately better than negative 1%. Finally, we are focusing intensely on enhancing our support for and relationships with clinicians and health systems. In addition to the prior authorization changes Steve mentioned, which we see as only the beginning, we are meaningfully speeding up our claims processing and payments and reengineering -- reenergizing our relationship engagement efforts with more dedicated resources and executive ownership. Our goal is to provide a more seamless experience for clinicians and health systems who work with us and to resolve issues more quickly.
As we look towards 2027 and beyond, we are shifting our focus to sustainable organic growth underpinned by improving Medicare fundamentals, a stronger commercial outlook, continued opportunities to enhance Medicaid performance and an organization that is operating with greater discipline and accountability for all our stakeholders.
With that, I'll turn it over to Patrick.

**Patrick Conway** (Executives):
Thanks, Tim. Our results from the third quarter underscore the important work underway across all of Optum to lay the groundwork for long-term growth. Starting with Optum Health. Overall, Optum Health continued to deliver strong performance in the third quarter, driven by the continued return to value-based care principles, combined with strong execution across our clinical programs and operational improvements, enabling clinicians to focus more on their patients and improve patient experience.
A few of the examples for this morning: a 27% increase from last year in online self-scheduling, making it easier for patients to reach clinicians; an increase in home health visits by 10% over last year. And we are very encouraged by the early success of our program to co-locate behavioral specialists within our primary care practices. The number of patients referred has doubled since last year, with an engagement rate of more than 90%. As Tim mentioned, it is now more important than ever to provide seamless care and coverage for our chronic and complex patients through all phases of the care continuum, from primary care to specialist to home to the pharmacy.
Moving to Optum Rx. Our focus in this business continues to be on 2 efforts to ensure value alignment to the customers and patients we serve. First, we continue to increase transparency on the PBM side of Optum Rx. Through the 2027 selling season, we have seen our industry first affordability, experience and transparency initiatives resonating in the marketplace and customers, the employers, governments, unions we serve, continuing to recognize the vital role of PBMs in controlling prescription drug costs and ensuring people have access to the medications they need, particularly as the prices charged by drug manufacturers continue to increase. For the first time, over 50% of Optum Rx membership is external, non-UHC membership.
Second, we fundamentally believe that pharmacy services have to be closer to the patient. Accordingly, you will see continued efforts within our separate pharmacy services businesses to more closely align pharmacy care with medical care. Integrated value-based care means just that, integrated. When pharmacy care and medical care are aligned, outcomes improve for the patients we serve, access improves and the total cost of care is lowered.
Specifically, within the pharmacy service side of Optum Rx, Genoa continues to expand its dedicated behavioral health pharmacy footprint and serve patients with serious mental illness and substance use disorders. Specialty pharmacy continues to grow through both volume and mix while improving patient support for increasingly complex therapies. And infusion services are becoming more important as we help shift appropriate care into lower-cost and more convenient settings. We will continue to expand our portfolio of integrated pharmacy services and align them as close to medical care settings as possible, delivering better care, convenience and access.
Turning to Optum Insight. 2026 has been both a performance and an investment year, and 2027 will show meaningful progress, setting the foundation for accelerating growth in '28 and beyond. Our investment focus has been on further developing and bringing to market healthcare-specific AI solutions that enhance productivity, performance, outcomes while improving the patient and clinician experience.
Overall, we are looking to 2027 with confidence. Our major remediation work is largely complete and it's created a strong foundation for growth across Optum.
With that, I'll turn it over to Wayne.

**Wayne DeVeydt** (Executives):
Thanks, Patrick, and good morning. Third quarter results reflect continued progress across the enterprise and improving execution in our businesses where we have been focused on operating reforms to drive better consumer and clinician experience. For Q3 2026, we reported revenue of $113 billion and adjusted earnings per share of $4.69, up from $2.92 a year ago. Consolidated medical care ratio of 88.4% for the quarter compares to 89.9% last year. The quality of earnings is strong and durable as we head into 2027.
At UnitedHealthcare, performance continued to reflect pricing discipline, fundamental medical cost management and care delivery enhancements. We continue to be respectful of continued elevated utilization trends, which typically step up in the back half of the year, particularly in our risk-based businesses. Within Optum Health, we are seeing steady progress from modernization, a return to a disciplined value-based care approach and operating improvements as the actions taken through 2026 begin to yield results. In Optum Insight, performance is benefiting from technology and AI-enabled improvements, including payment integrity and broader operating efficiency, while we invest into the new areas to expand and modernize our offerings to drive growth. And in Optum Rx, we continue to see the benefits of disciplined execution and the breadth of our pharmacy services model now based on a simpler, more transparent approach to serving these evolving market needs.
Turning to the full year. Our updated 2026 adjusted EPS guidance of at least $20.50 reflects performance through the third quarter, balanced by expected investments in the final months of the year. From a capital deployment perspective, our priorities remain consistent. First, reinvest in the business through targeted organic growth and steady expansion in care delivery, technology modernization and broad-based AI adoption.
Second, maintain balance sheet strength. And third, return value to shareholders. Our balance sheet remains strong. Our debt-to-cap ratio was 41.7% at the close of the quarter, and we remain on track to approach 40% by year-end. We repurchased $5 billion of UNH stock through the third quarter. We have paid $6.2 billion in dividends year-to-date and expect to exceed $8 billion by year-end. Our strategic priorities remain focused on capabilities that align with and strengthen our ability to deliver value to consumers, benefit sponsors and customers and support long-term growth for shareholders.
We view our 2026 adjusted EPS guidance of at least $20.50 as a solid run rate on which to grow. We would offer that current analyst consensus for 2027 may understate the opportunity ahead, and we see the lower end of our long-term 13% to 16% growth rate as a more reasonable starting point.
As we think about 2027 more broadly, we continue to see a balanced set of tailwinds and headwinds. Tailwinds include continued enterprise-level performance progress, share repurchases, value-based care performance improvements and further gains from AI and modernization that improve both consumer and clinician experiences, drive productivity benefits, reduce costs and create sustainable performance improvement opportunities for our business and those we serve as well as product opportunities for Optum Insight. On the headwind side, we will accelerate our investments in the policy reforms and modernization of the businesses, particularly in UnitedHealthcare and Optum Insight, and remain respectful of medical trends and the broader external environment where health benefit funding remains pressured.
Overall, we're steadily and methodically improving performance broadly across the portfolio. We are positioned to finish 2026 strongly, and we remain focused on consistently delivering our 13% to 16% long-term growth target.
With that, I'll turn it back over to Steve.

**Stephen Hemsley** (Executives):
Thanks, Wayne. Let me close with a few thoughts before we move to questions. For a little more than a year, our priorities have been clear: return to our core mission and culture, better serve the needs of healthcare as one enterprise and one leadership team, restore financial and operating discipline, turn around and strengthen our performance business by business across all performance measures, begin the process of reimagining and modernizing all we do to harness the compelling potential of modern intelligent technologies, simplify our processes, elevate our service levels and advance our response and service speed to consumers and clinicians. And finally, reposition all our businesses to return to responsible levels of profitable organic growth.
As you've heard today, we are well underway in all those areas, but fully achieving those priorities requires us to get outside our 4 walls. Throughout our company, we are spending time listening carefully to customers, consumers, clinicians, policymakers and other stakeholders. We're doing so with humility and with a service mindset, conscious of the positive role we can play and the responsibility we have to improve the health system experience when we operate at our best. Those conversations are helping renew and reinforce the fundamental understanding that success in healthcare depends on relationships and trust, and we need to continue to build both with all stakeholders.
We will continue listening, we will continue learning, and we will continue advancing our business in ways that improve experiences, provide easier access and lower costs while delivering better outcomes. And for you, our shareholders, all these accountabilities align and create value. The progress we've made in 2026 gives us confidence. Our businesses are improving. Our modernization efforts are gaining traction. Our investments in AI and in integrated value-based care are creating tangible benefits today while positioning us for the future.
We remain focused on better managing our businesses, finishing '26 strong and building that foundation for growth in '27 and '28 and beyond. So we look forward to providing you a more comprehensive update on our outlook for next year before year-end.
And I'll thank you now. And the operator, let's open the line for questions.

**Operator** (Operator):
The floor is now open for questions. [Operator Instructions] Our first question comes from Justin Lake with Wolfe Research.

**Justin Lake** (Analysts):
I wanted to focus on the government side for a second, specifically your comments around Medicaid. Things were getting better. Curious what you're seeing in terms of your third quarter run rate and what's driving that? Are you actually back to kind of breakeven given your improvement there? And maybe you can also let us know where your MA margins are at this point for 2026.

**Stephen Hemsley** (Executives):
Mike, do you want to take that?

**Michael Cotton** (Executives):
Sure. Thanks, Justin. Thank you for the question. As Tim indicated, our membership and overall Q are within our expectations, and we now expect full 2026 performance moderately better than our forecasted range. The main drivers of that activity has really been our focus on complex care cost management, network and services curation, increasing our membership engagement, particularly in our coaching -- AI-powered coaching activities, modernization activities and the ongoing identification and removal of fraud, waste and abuse activities. And we do believe these activities are doable. We did see good improvement in Q3, and we believe that will continue on for the rest of the year.
We continue to see elevated trends in the areas of behavioral healthcare services, specialty pharmacy services and home and community based services and also in inpatient care costs as well. Those elevation rates are moderating slightly, and we're continuing to monitor that. We anticipate margin improvement as we look into next year, and we will continue to work with our state partners to mitigate what has been a stubborn gap between funding and medical cost trends through the year. And again, as we think about this for 2028, we're very aspirational to move to rate of margins by the end of that year. Thank you for the question.

**Bobby Hunter** (Executives):
And Justin, maybe just, this is Bobby, on the Medicare margin piece that you highlighted. So given where we've paced through 2026, we do now expect to be near the top end of the 2% to 4% range. I would attribute a lot of that to some of the great recovery actions that the team has executed on here throughout the year, I think the initiatives around medical trend, our cost management focus and then a broader focus on the durable product offerings that we've brought to the marketplace for '26. It also allows us to make investments now to set us up for future success, I think what we're doing in quality, what we're doing in AI, modernization, provider. And ultimately, I feel good about how it sets us up for continued success in '27. Thanks for the question.

**Operator** (Operator):
Our next question comes from Lance Wilkes with Bernstein.

**Lance Wilkes** (Analysts):
Great. Could you talk a little bit about how you're approaching growth in 2027, in particular, in Medicare Advantage as you're approaching the top end of the range, how you're looking at growth there? And then likewise, with the selling seasons in for national accounts and for PBM, how is that coming along?

**Stephen Hemsley** (Executives):
So we'll start with Bobby.

**Bobby Hunter** (Executives):
Yes. Thanks, Lance, for the question. So yes, AEP is kind of right around the corner here. And while we'll wait until later this year to provide kind of formal membership guidance, maybe a couple of early observations to share with you. So obviously, some of the things we did as we set out for planning in '27 was continue to look at ensuring we have a durable set of product offerings, and that meant some continued footprint refinements and product refinements really around the residual PPOs that we started kind of moderating a year or 2 ago. But then as I look at the opportunities, I think that's actually a lot of good growth potential out there.
So maybe one important stat for you, even with some of the footprint refinements, we did actually expand our overall footprint. Tim noted it in the prepared remarks. Now more than 94% of American eligibles for Medicare have access to one of our plan offerings. That's an expansion year-over-year. We also took a more dynamic approach to the product planning this year. And I think there are some real opportunities for smart, durable growth in the marketplace right now. We are particularly focused on the Dual Special Needs Plan offerings, the Chronic Special Needs Plan offerings and then some of the high-value HMO.
And I think we're better positioned to capture that growth in some of those key areas as we step into AEP in 2027 than we have been in recent years, and we aligned our go-to-market strategy accordingly. Maybe just last thing to highlight on that is I -- when I think about the overall capabilities of the enterprise, the capabilities that we bring to bear, our emphasis on value-based care, I do think we have an incredible opportunity to make an impact for the members that are on these D-SNP, C-SNP and HMO plans and really drive some incredible outcomes and quality for those folks over time.

**Stephen Hemsley** (Executives):
Great. Thanks, Bobby.

**Timothy Noel** (Executives):
Yes. Lance, this is Tim. I'm going to turn it over to Brandon Cuevas, who is our new CEO of our Commercial business, for some insights into the commercial selling season and our pricing posture there.

**Brandon Cuevas** (Executives):
No. Thanks, Lance. Appreciate the question. We're coming off of 2 really, really strong years in national account sales. And we're pleased to see that our persistency and our group retention looks very, very strong going into 2027. As we look at our pipeline and our selling season, obviously, we're well through that in our national accounts base. And we've had a really successful selling season this year. I think as we think about the overall growth looking into our commercial business, again, I think we remain respectful of trend.
We've had to be very mindful of the trend increases as well as being very markedly focused on affordability. As we look at 2026, we think that our growth is going to be reflective of some of the increased trend pressures that we've seen in the marketplace. But our pipeline is filling and products like Surest and where we are in our mid-market selling is actually continuing to come in remarkably strong. And so we're having a very solid selling season looking at 2027, but we're still in the midst of our mid-market selling. The national accounts look very strong going into next year. Thanks for the question.

**Stephen Hemsley** (Executives):
Thanks, Brandon. How about -- Jon, PBM?

**Jon Mahrt** (Executives):
Yes. Thank you, Steve. And Lance, thank you for the question. Building really on Brandon's comments, we've enjoyed a couple of strong selling seasons back-to-back years, and we see that trend continuing this year, really driven by the transformation and transparency modernization efforts within the PBM. Those efforts are really resonating in the market, driven, first and foremost, by the fact that every Optum Rx client gets the benefit of the fully transparent supply chain instrumentation that we are putting in place.
So that's driving retention, again, in the high 90s this year. And then success in the new client marketplace, as Patrick mentioned in his prepared remarks, while maintaining pricing discipline. We're growing membership now to north of 50% of our covered lives and expect that trend to continue in 2027. As we wind down the year, we're staying close to our clients who are in the heat of the enrollment season. Brandon and I still have efforts in flight together. We'll stay close to those clients as we work to update our membership outlook for 2027. Thanks for the question.

**Operator** (Operator):
Our next question comes from Stephen Baxter with Wells Fargo.

**Stephen Baxter** (Analysts):
Just to round out some of the 2027 color, I think you just spoke pretty clearly to the health plan and PBM assumptions. Can you add some color on how you're thinking about your top line dynamics for Health and Insight and repositioning those businesses for growth, I think, in 2028 or beyond?

**Stephen Hemsley** (Executives):
Sure. We'll start out with Krista, and then we'll go to Sandeep.

**Krista Nelson** (Executives):
Yes. Thanks so much for the question, Stephen. I would just -- I kind of want to just start with highlighting some of the performance that we're actually seeing inside the third quarter. Really strong performance in our clinical programs in medical management. Those programs are going to continue to be durable as we head into 2027. The work we're doing to reduce unnecessary inpatient stays, the work we're doing to improve access to primary care, preventive care, the work we're also doing to improve access to home health and helping serve our patients in community and home settings. As I think about 2027, again, we'll unpack more of this in the coming months. But I think, really confident in our ability to grow earnings inside 2027. And our focus is going to be on just really thoughtful growth.
And there's a couple of things I maybe would just point to as growth opportunities for this business in '27, but also just really long term. First is we serve 20 million patients today. About 4 million of those are in fully accountable relationships. So still room for fully accountable growth, but even more importantly, lots of opportunity for professional cap, shared savings and other ways in which we can serve our patients in our integrated model. Second, I would point to is just the high-performing service lines that we have today. So think examples of home health, hospice, surgery centers, D-SNP, C-SNP, HMOs. Again, lots of opportunity for growth in those services to go deeper in our existing markets and serve kind of more patients more comprehensively.
And then last, I would also just point to opportunities where we're launching new products in the market. Maybe just calling out one as an example. This year, in partnership with one of our payers, we've expanded our ability to manage risk across a post-acute continuum. So I think, from an inpatient hospital stay, all the way through SNF and home health. We've seen really strong demand for these products to serve post-acute care risk comprehensively. And we're also really pleased with the results. We're seeing an improved access to timely care, again, improved access to home health utilization. And I think you'll see those programs also expand inside 2027.
So taken together, this is still a multiyear journey to make sure we're pacing appropriately towards our 6% to 8% target margin range, but see ample opportunity for growth inside Optum Health.

**Stephen Hemsley** (Executives):
And you're really oriented to do the new things.

**Krista Nelson** (Executives):
Exactly.

**Stephen Hemsley** (Executives):
Sandeep?

**Sandeep Dadlani** (Executives):
Yes. Stephen, for Optum Insight, the goal is to simplify healthcare with AI for consumers, providers, payers and life sciences companies. As 2026 is on plan, I want you to think about Insight as a multiyear investment and execution journey. So there's a few moving parts here. We are continuing to rationalize existing products and contracts where they don't make sense. But we are infusing AI into our existing offerings that help make them more competitive and profitable and then launching new AI-first products and platforms.
To give you some examples of the momentum there, our Optum AI consulting firm with a Medicaid plan is helping them adjudicate their most complex claims in seconds instead of days using agentic AI. Another example is a product called Optum Integrity One, which automates claims coding in the revenue cycle space. We launched this at the end of 2025. We had 2 clients at the end of 2025. Today, we have 15 clients implemented and another 24 clients implementing. So you see the momentum of some of our new AI clients. We recently launched a partnership joining the Anthropic Partner Network. We had announced similar go-to-market partnerships with Microsoft and Google in recent quarters across products. We are seeing strong disciplined execution, new team members that are AI-first and new product teams, et cetera. And in the next 2 quarters, we'll be seeing a series of product launches. So overall, with those moving parts, we feel confident about our prospects for 2027. Thank you.

**Stephen Hemsley** (Executives):
AI is reinventing that business.

**Operator** (Operator):
We'll take our next question from A.J. Rice with UBS.

**Albert Rice** (Analysts):
I might go back to the commercial business. I think the risk portion, you guys have indicated that maybe that's operating at a below 5% margin. Part of that is the IDR issues that you've highlighted. It sounds like you're saying today that, that's stabilizing somewhat. And I know that historically, you've talked about that business having a high single-digit, 7% to 10% or something, margin. I wonder your thoughts about the pacing of margin recovery there and maybe flesh out a little bit more about the stabilization you're seeing right now.

**Stephen Hemsley** (Executives):
Tim, do you want to start with that?

**Timothy Noel** (Executives):
Yes. Thanks, A.J. Yes. So as we talked about in the opening remarks, we are seeing a stabilizing of the trends that we're seeing, the medical cost trends that we're seeing in the commercial business, albeit at levels that are high and significantly higher than historical norms that we've seen in the commercial business. As we priced for 2027, we took the view that we would see these trends continue and persist into 2027 and priced rationally just consistent with all of that. As we think about our long-term targeted margins and some of these utilization pressures that we're facing in the commercial business, it is going to stretch out our ability to achieve those long-term objectives and margins for the commercial business.
So more color in a couple of months. We'll have an opportunity to dive into some of the detail of that business, but that's how you should be thinking about it right now.

**Operator** (Operator):
Our next question comes from Ann Hynes with Mizuho Securities.

**Ann Hynes** (Analysts):
Maybe we could fine-tune some of your earlier comments on MA. Just in general, how do you view your competitiveness from a benefit offering versus your peers? And do you believe UNH is positioned to deliver overall membership growth for next year?

**Stephen Hemsley** (Executives):
Bobby?

**Bobby Hunter** (Executives):
Yes. Ann, thanks for the follow-up question. So again, we're not going to get to specific guidance. We'll get to that here in a few months. That said, we took a very deliberate approach for 2027 with a focus on investing in benefits, investing in products and providing stability in products where we know we can make a meaningful impact on growth, a meaningful impact on the consumers that we serve, meaningful impact in partnership with many of our value-based care providers who serve those populations and think about that, again, in the context of our Dual Special Needs Plans, our Chronic Special Needs Plans and our HMO plans.
A big part of why we've had the recovery actions we have in '26 is our focus in those areas, the broad capabilities that we bring to life in those areas, our ability to get after some of the medical cost areas, driving more cost management, things of that nature. So I think as I look to '27 and look at the competitive landscape, we have a nice opportunity to capture some of that growth to continue serving more members in those areas, and that's what we're focused on as we continue to modernize our business. Thanks for the question.

**Operator** (Operator):
We'll take our next question from Kevin Fischbeck with Bank of America.

**Kevin Fischbeck** (Analysts):
I appreciate the earlier comments that trend tends to be a little bit higher in the back half of the year, but the trend data points that we're tracking kind of really imply that trends start off really low to start the year, but it kind of has accelerated as the year has gone on. I mean, is this consistent with what you're seeing? And if so, why is it maybe accelerating a little bit more than normal? And I guess, how comfortable are you that you're pricing 2027 to the exit rate as far as trend goes?

**Stephen Hemsley** (Executives):
Tim?

**Timothy Noel** (Executives):
Kevin, this is Tim. So we are not seeing the dynamics that you're talking about. When you kind of go across each of our businesses, we've talked about commercial kind of continuing at the level, stabilizing somewhat in more recent durations, but still tracking north of 11% we talked about. We're seeing moderation in trend in the Medicaid business. And we are seeing some better-than-expected performance when you start thinking about the Medicare businesses broadly. But in terms of trend acceleration, no, we are not seeing that. And in fact, we're seeing some moderation in the government programs business and stabilization in the commercial business.
And as we think about our forward pricing, right now, we are able to incorporate the latest information using better analytical tools, more real-time information on the direction of travel of medical cost utilization and are incorporating all of that into our forward pricing assumptions, but not seeing the elevation that you're referencing as we pace through the year.

**Operator** (Operator):
Our next question comes from Scott Fidel with Goldman Sachs.

**Scott Fidel** (Analysts):
I was hoping just on the Medicaid side, would be interested in your thinking around, if we think about '27 to 2030 and you have that natural opportunity for cyclical margin recovery in Medicaid, clearly with margins still negative. But then sort of -- and then having to sort of interface with the implementation of the OB3 reforms that will sort of scale up from '27 to '30. And maybe sort of walk us through how you sort of see those 2 offsetting each other and maybe how you think about maybe a reasonable sort of view on sort of where margins maybe average over that time period.

**Stephen Hemsley** (Executives):
Mike?

**Michael Cotton** (Executives):
Scott, thanks for the question. As we look at what's happening over the next 4 years, there certainly will be a cycle process that goes through the Medicaid business. We've seen this over history, if you look at it, and we expect that to happen through Medicaid for this cycle as well, particularly as we think about OB3. We think there is an opportunity to get back to rate of margins in 2028. We're continuing to focus on our efforts around clinical care management, cost management, leveraging AI tools to do that as well. We do think that over time, there will be opportunities for us to look at markets, to look at ways we can tie into our strategy around duals and make sure that this can be effective. But overall, we think getting back to those margins and remaining at those margins will be an opportunity for us and will be our goal through 2030. Thank you for the question.

**Stephen Hemsley** (Executives):
And in the long term, Medicaid is a good, durable marketplace that to continue to grow.

**Operator** (Operator):
Our next question comes from Lisa Gill with JPMorgan.

**Lisa Gill** (Analysts):
I have a question on specialty pharmacy. You brought it up on the cost side, but Patrick also talked about it on the opportunity side. And just really want to understand 2 things here. One, you talked about infusion. I'm curious about capabilities today and what you see around infusion. Two, what do you see around potential opportunities in biosimilars?
And then lastly, the comment around integrated medical and pharmacy together. You talked about the fact that 50% are now external clients. I'm curious about how you bring the 2 entities together if they're not under a single umbrella of UnitedHealth Group.

**Stephen Hemsley** (Executives):
Sure. So why don't we start with Patrick, and then we'll go to Jon, and then we might come back to Patrick on the integrated piece, okay?

**Patrick Conway** (Executives):
So Lisa, thanks for the question. We'll call out a few areas. First, specialty pharmacy, as you know well, with the drug pipeline and the patient need, is a growing market. What we talked about in the opening comments is we're increasingly bringing that closer and closer with our care delivery enterprise and clinicians broadly across the marketplace. So Jon and the team have led terrific efforts, both in LDD drugs where we have high win rates with care models, working with Krista and the Optum Health team, also working with external clinicians and physicians and prescribers. So we see that market continuing to grow, and it's about service, experience and patient care.
Infusion, you also alluded to, that's a lower cost setting, as you know, and more convenient for patients. So what we hear from payers and our other customers is they want infusion to grow because it's lower cost and better experience for patients. And once again, we have a robust clinical care model and growth in that area.
I'll let Jon talk a little bit more about the sort of PBM and pharmacy linkage, and then we'll go from there.

**Jon Mahrt** (Executives):
Yes, very good. Thank you, Patrick. I'll start, Lisa, with the strength within -- Patrick started with this. With the strength within our specialty pharmacy led by Mike Einodshofer and the team, we're winning on experience there, Lisa. So if you look at overall volumes, while volumes might have been down 5% for the quarter, specialty volumes actually up 2.6% for the quarter. And that's driven by a couple of initiatives. We're winning on provider choice, which, again, is strong LDD win rates, our strongest in years there, Lisa. Coupled with the continued build-out of our centers of excellence -- our therapeutic centers of excellence. We have 15 of those serving the provider space. That allows us to get very close to those provider relationships across our covered footprint.
Within the specialty pharmacy, then we win on consumer experience. We recently won the Specialty Pharmacy of the Year from the National Association of Specialty Pharmacy, an incredibly competitive award. And so that puts us in the right place to serve consumers as we continue to expand that footprint. This offer is resonating with our PBM clients who look for a seamless extension of the specialty pharmacy care as part of their pharmacy benefit.

**Patrick Conway** (Executives):
Maybe just 2 quick other notes on biosimilar because you asked about that, we're seeing robust uptake across our clients, lowest net cost. Our Optum Specialty Distribution, which we had stood up, is functioning well. Last thing I'll call out across Krista and Jon's team, really great collaboration between the Optum Health clinicians and the pharmacies to make sure we're providing that integrated care experience for the patients we serve.

**Operator** (Operator):
We'll take our next question from Erin Wright with Morgan Stanley.

**Erin Wilson Wright** (Analysts):
So as you continue to make progress on the Optum Health turnaround, I guess, how should we think about Optum Health margins, where they land in 2027 relative to that 6% to 8%? And just longer term, how you think about potential margins exceeding even that range? Are there any structural constraints to further kind of margin expansion? And with the evolution of that business, the business mix, alongside what you're doing with automation and AI, I guess, could that support even higher margins over time?

**Stephen Hemsley** (Executives):
Yes. And before Krista gets to that, maybe just a general comment that there's only so much we can say about 2027, that we will have a conversation with you before the end of the year where we'll be able to give you, let's say, more color on 2027, which we view very positively, but we've already provided probably more forward-looking views than we probably have ever done on a call at this stage. So with that, I think very positive outlook. Krista and Mike, do you want to respond?

**Krista Nelson** (Executives):
Yes. Thanks, Steve, and thanks, Erin, for the question. Again, I think just kind of anchoring back to the work we've been doing to reposition this business for long-term success. Again, really pleased with the performance we're seeing inside 2026. Third quarter is another great example of that. That core performance improvement is durable and will contribute meaningfully to our kind of outlook in 2027. And again, I think 2027 is a year where we'll see a strong pace towards that 6% to 8% by 2028. That is really our focus. And then as I alluded to in the earlier question, I'm optimistic and see a lot of opportunities for growth in this business kind of across the domains I mentioned. But again, we look forward to unpacking more detail around those. And I see some of that starting in '27, but also opportunity in 2028 and beyond for this business across those 3 domains I mentioned.

**Stephen Hemsley** (Executives):
So very positive, but we can't really get to precision at this range.

**Operator** (Operator):
Our next question comes from Andrew Mok with Barclays.

**Andrew Mok** (Analysts):
Optum Health's EBIT guidance still appears to imply a meaningfully negative fourth quarter. Can you walk through what's driving that sharp seasonality and help quantify 4Q investments that might be impacting that segment?

**Krista Nelson** (Executives):
Yes, yes. Thanks for the question. So I mentioned the third quarter performance will be durable into the fourth quarter, but fourth quarter does reflect risk seasonality, which is normal course for this business, and some additional investments that we're making for long-term performance. So inside those additional investments, think things like technology, AI, but more specifically, even workflow improvements for our clinicians to ensure that we're providing the appropriate expanded access that we're focused on, but also make it easier to care for our patients to deliver strong quality outcomes and support that integrated experience that we're talking about.
So think of things like AI-enabled care summaries, to make it easier for clinicians to prepare for visits. Ambient, we've talked a lot about how can that translate from just listening and documentation to kind of next best action insights for our clinicians. Also doing quite a bit of work on scheduling that I mentioned. And there's a handful of other investments that we're making in our clinician workflows, again, really just to enable durable performance for the long term in this business. And those are the things that are really part of the fourth quarter. I would say, overall, again, third quarter will be kind of durable into fourth, but some kind of performance reflected with our risk seasonality. Thanks.

**Operator** (Operator):
We'll take our next question from Matthew Gillmor with KeyBanc.

**Matthew Gillmor** (Analysts):
I wanted to follow up on some of the policy items that Tim Noel referenced. I think you talked about your work with CMS on quality efforts. You have also talked about the issues on the IDR side. I was just hoping you could give us a sense for how you'd like to see those programs evolve over the next few years in a way that would be constructive to the system.

**Timothy Noel** (Executives):
Yes. Thanks, Matthew, for the question. Yes. So with respect to the IDR process, we're really referring to the dispute resolution process. The spirit of the legislation is one that we're certainly aligned on, but the result and outcomes that we're seeing where the awards are significantly more multiples, 10x, 11x what Medicare would pay in some of those instances is excessive, and it's contributing to the lack of affordability in healthcare that we're seeing right now. So our issue with the IDR process relates specifically to the dispute resolution and the inefficiencies of it, the costs associated with it and the outcomes that it's resulting in generating, but not with the spirit of the law because that is something that we're totally aligned to.
And I'll turn it over to Bobby to talk a little bit about some of the modernization of the Medicare program.

**Bobby Hunter** (Executives):
Yes. Thanks, Tim. So Matthew, and you alluded to it, but very appreciative of the active and ongoing dialogue that we have with CMS, that we have with policymakers. What I want you to hear from us is we are supportive of modernization. We are supportive of reform that advances the program and ensures sustainability of the program. We provided ideas in that regard, I think quality opportunities, payment opportunities, affordability opportunities, administrative efficiency, tech interoperability and all of those in response to CMS's various requests for proposals.
I think important to note, MA has a really strong foundation from which to build upon. And so it's key that as we kind of pace through these reforms and modernization opportunities that it's done thoughtfully and with broad stakeholder engagement, and that doesn't just mean plans like UnitedHealthcare, that means with providers, clinicians, members, broader stakeholders, et cetera, all those voices are critical to this conversation. And it all needs to be done with program stability at the forefront, and I'm optimistic about what that looks like. Thanks for the question.

**Operator** (Operator):
Our next question comes from Ryan Langston with TD Cowen.

**Ryan Langston** (Analysts):
Great. You recently talked about making some unique investments in the Stars program. Now that the details are out, I'm sorry if I missed this, but can you give us any insight into the size and maybe types of investments you're making in the Stars program? And any commentary you can provide on your broker strategy heading into open enrollment would be helpful as well.

**Bobby Hunter** (Executives):
Yes. Ryan, Bobby here. So I'll hit the Stars one and then I'll hit the broker one quickly as well. So overall, very pleased with how we executed on the controllables for this Star season. We take a long-term view of quality, no different than our approach to products and pricing. And so while we knew there could be some Star pressure related to the repositioning of benefits we did for '26 in response to the funding and policy headwinds impacting the overall industry, that's also why we made the investments we did, to drive improvements in key areas like clinical outcomes, pharmacy outcomes. And what you saw is we actually, therefore, year-over-year improved nearly every HEDIS and Rx measure for this Star season.
But we're not satisfied there. There's more work to be done. There's more opportunity. There's more opportunity to invest and further improve as we pace forward, and that is what we're focused on in that regard. So think of our continued investment in '26, Q4 and into '27 as continuing to accelerate, not slow down given the criticality of quality and Stars to the overall business.
And maybe lastly, just your question on broker. I would say, again, similar to my comments around the product positioning, more dynamic, really more strategically positioned for '27 than perhaps in recent years with key growth opportunities in the D-SNP, C-SNP and HMO space, we have aligned our broker strategies accordingly. We've aligned our marketing strategies accordingly, and we are going to market with that very clear objective to drive good stability within our base business and good growth opportunity in those areas where we think there's some nice opportunity for us. Thanks for the question.

**Stephen Hemsley** (Executives):
Thank you. So I think we will -- I appreciate the questions this morning and the level of engagement. I think we'll close this now, but we will be around as a team for the rest of the day if you have questions that didn't get responded to or if you have further questions. Again, we thank you for your time today. And I hope you get a sense of the momentum we're bringing into '27 as our emphasis on disciplined execution kind of -- and very much improved patient and care provider experiences continue to go forward. And I think we'll just build on this quarter-by-quarter. And we look forward to providing you with a more complete outlook. We'll meet before the end of the year to really engage with investors and really give more color to 2027. But thank you, and have a great day.

**Operator** (Operator):
This does conclude today's conference. We thank you for your participation, and have a great day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### UNH_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜Wayne DeVeydt｜guidance：CFO給出2026全年調整後EPS新區間，3Q略多於4Q（原話："range of $19.50 to $20 with slightly more earnings in 3Q"）
- 2026-07-16｜Wayne DeVeydt｜guidance：全年醫療費用率預期88.1%±25bp（原話："medical care ratio of 88.1%, plus or minus 25 basis points."）
- 2026-07-16｜Wayne DeVeydt｜guidance：UHC全年營業利益展望上調至至少120億美元（原話："UnitedHealthcare to at least $12 billion"）
- 2026-07-16｜Wayne DeVeydt｜margin：Q2報告MLR 86.7%，含有利前期醫療發展（原話："medical care ratio of 86.7% includes $860 million of net"）
- 2026-07-16｜Wayne DeVeydt｜margin：Q2營業成本率12.7%（原話："operating cost ratio was 12.7% for the quarter"）
- 2026-07-16｜Wayne DeVeydt｜margin：全年營業成本率預期落在先前區間高端，因投資人員、社區與AI（原話："operating cost ratio to come in at the higher end of our"）
- 2026-07-16｜Wayne DeVeydt｜guidance：盈餘季節性：UHC約75%落在上半年（原話："approximately 75% to the first half of the year."）
- 2026-07-16｜Wayne DeVeydt｜guidance：全年上下半年盈餘比約2/3、1/3（原話："we're seeing a 2/3, 1/3 first half to back half mix."）
- 2026-07-16｜Timothy Noel｜guidance：全年MA會員預期減少約110萬（原話："enrollment to decline by approximately 1.1 million"）
- 2026-07-16｜Timothy Noel｜risk：商業險醫療成本趨勢高於先前11%水準，未見趨緩（原話："medical cost trends modestly above 11% level"）
- 2026-07-16｜Timothy Noel｜risk：管理層稱未見商業險成本趨勢趨緩證據（原話："we are not yet seeing evidence of cost trend moderation"）
- 2026-07-16｜Timothy Noel｜margin：Medicare趨勢低於規劃假設，管理層表示不代表趨勢轉折點（原話："this does not represent an inflection point in trend."）
- 2026-07-16｜Timothy Noel｜commitment：管理層對2027年MA投標的表述：紀律且依現行趨勢環境（原話："our benefit planning remains disciplined"）
- 2026-07-16｜Timothy Noel｜margin：Medicaid全年利潤率仍承壓（原話："we expect Medicaid margins to remain pressured"）
- 2026-07-16｜Michael Cotton｜margin：Medicaid全年利潤率預期落在先前溝通區間（原話："negative 1% to negative 1.7%, and we expect to hit that"）
- 2026-07-16｜Michael Cotton｜margin：Medicaid 2026年化費率增幅約6%至7%，仍落後醫療趨勢（原話："rate impact will be in the zone of around 6% to 7%"）
- 2026-07-16｜Daniel Kueter｜risk：No Surprises Act獨立仲裁(IDR)為商業險2026增加約50bp趨勢，累計至少100bp（原話："now totaling at least 100 basis points of total cost."）
- 2026-07-16｜Daniel Kueter｜risk：IDR仲裁案件集中於少數實體（原話："Roughly 60% of all arbitration cases are brought by 1 of"）
- 2026-07-16｜Daniel Kueter｜margin：商業險利潤率回復時程延後，超出2027（原話："is extending the time frame for full margin recovery past"）
- 2026-07-16｜Daniel Kueter｜margin：管理層將2026描述為延遲而非挫折（原話："'26 as a delay to that margin recovery trajectory"）
- 2026-07-16｜Daniel Kueter｜commitment：管理層仍承諾商業險長期回到7%以上利潤率（原話："return to our historic margin performance of 7% or greater"）
- 2026-07-16｜Stephen Hemsley｜commitment：CEO表示相信13%至16%長期成長率（原話："definitely believe we can perform in that range."）
- 2026-07-16｜Wayne DeVeydt｜guidance：CFO稱19.5至20美元為合適起點，含前期發展（原話："the $19.50 to $20 is the right stepping off point"）
- 2026-07-16｜Wayne DeVeydt｜guidance：CFO稱無須扣除一次性項目，19.5至20美元為基準（原話："I think the $19.50 to $20 is the right baseline."）
- 2026-07-16｜Wayne DeVeydt｜risk：CFO稱基金會等投資不視為一次性（原話："We don't believe that's onetime, though."）
- 2026-07-16｜Bobby Hunter｜risk：Medicare趨勢出現下修的原因之一：未見未知風險全面浮現（原話："deviation from the still elevated underlying core trends"）
- 2026-07-16｜Timothy Noel｜margin：Medicare 2026趨勢新點估計延至下次財報（原話："until the next call when we've seen more of the year"）
- 2026-07-16｜Timothy Noel｜customer：健保交易所業績優於規劃，但2026承諾將利潤返還消費者（原話："made the pledge to return our"）
- 2026-07-16｜Timothy Noel｜commitment：承諾年底前取消30%事前授權量（原話："eliminating by the end of this year, 30% of prior"）
- 2026-07-16｜Timothy Noel｜commitment：承諾2027年底前80%事前授權即時處理（原話："eliminating by the end of this year, 30% of prior"）
- 2026-07-16｜Patrick Conway｜margin：OptumHealth預期利潤率隨計畫成熟持續改善（原話："80% of our prior authorizations in real time by the end of"）
- 2026-07-16｜Patrick Conway｜customer：Optum Rx客戶留存率在90%高段（原話："retention rates in the high 90s"）
- 2026-07-16｜Patrick Conway｜commitment：預期2026年底逾95%客戶採100%回扣全數轉嫁（原話："2026 with more than 95% of clients on 100% pass-through."）
- 2026-07-16｜Sandeep Dadlani｜product：Optum Insight約1/3投資用於將內部AI用例商品化（原話："about 1/3 of our investments this year are going into"）
- 2026-07-16｜Sandeep Dadlani｜guidance：Optum Insight Q2略優於預期，維持全年財測（原話："we remain on track for our full year guidance"）
- 2026-07-16｜Timothy Noel｜product：AI效益預期2027加速、2028更深（原話："accelerate into 2027 and even go deeper in terms of the"）
- 2026-07-16｜Wayne DeVeydt｜capital_allocation：全年庫藏股預期至少50億美元，高於原先25億（原話："total share repurchases of at least $5 billion in 2026"）
- 2026-07-16｜Wayne DeVeydt｜capital_allocation：負債資本比目標年底約40%（原話："reduce our debt-to-capital ratio to approximately 40% by"）
- 2026-07-16｜Bobby Hunter｜risk：Stars評等：管理層不評論最終結果（原話："speculate on final Star Year '26 results"）
- 2026-07-16｜Wayne DeVeydt｜margin：CFO稱PDR調整未影響OptumHealth持久利潤率（原話："No, it did not impact the durable margins that we're"）

### 問答異常語氣（迴避／改口／保留）
- UNH_Q2_2026_Earnings_Call_20260716.md｜問：A.J. Rice問是否已在可持續軌道上達到13%-16%成長，以及是否優於2028目標時程｜答法：CEO談持續改進與使命，重申從未不相信13%-16%，未直接回答2028時程或今年是否優於該目標
- UNH_Q2_2026_Earnings_Call_20260716.md｜問：Ann Hynes問Medicare核心使用率7.5%假設目前追蹤值與新財測假設的成本趨勢｜答法：管理層稱較低但不給新點估計，延至下次財報
- UNH_Q2_2026_Earnings_Call_20260716.md｜問：Stephen Baxter問2027年MA投標假設更接近上半年經驗或2025趨勢｜答法：Bobby Hunter稱現在談細節太早，只說規劃反映現行經驗並調整費率表等，不給數字
- UNH_Q2_2026_Earnings_Call_20260716.md｜問：Whit Mayo問Stars預期與產業訴訟看法｜答法：管理層稱不適合推測Star Year 2026/2027結果，只談與CMS合作與加碼品質投資

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
{"date":"20260525","verdict":"B 衛星候選 / 觀望偏進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"MCR 從 FY25 reset 後逐步 normalize，FY26-FY27 維持 88-89%","columns":{"2Y 驗證":"FY26 全年 MCR ≤ 88.8%（管理層 guide）","5Y 驗證":"FY28-FY30 重回 87-88%（pre-COVID normal）","10Y 驗證":"FY32-FY35 MCR 維持 ≤ 88%，無結構性逆轉","具體數字門檻":"MCR ≤ 88.8%（FY26 guide）；≤ 87.5%（FY28 H1 normalize）","信息來源":"UNH 2026 Outlook Press Release 2026-01-30","漂移觸發":"連 2 季 TTM 偏離 > 1pp（即季 MCR > 89.8%）→ 削弱"}},{"id":"H2","text":"Optum Health margin 從 2.4% guide 逐步回升至 3.5-4%（垂直整合 thesis 部分修復）","columns":{"2Y 驗證":"FY26 OH margin ≥ 2.4%（guide 下緣）","5Y 驗證":"FY28-FY30 OH margin 重回 3.5-4%（risk pool 重新承保後）","10Y 驗證":"OH margin 達到 4-5% sustainable 水位 + 醫師雇用網絡跨越 15 萬","具體數字門檻":"FY26 margin ≥ 2.4%（guide）；FY27 ≥ 3.0%；FY28 ≥ 3.5%","信息來源":"UNH FY26 outlook (2026-01-30) Optum segment guide","漂移觸發":"FY26 任一季 OH margin &lt; 2.0% → 削弱；連 2 季 &lt; 2.0% → 反轉"}},{"id":"H3","text":"DOJ Medicare Advantage 調查以 manageable settlement 收場（&lt; $5B），無 criminal indictment、無 Optum 分拆強制","columns":{"2Y 驗證":"2026-2027 任一進展訊號（DOJ filing、CMS 草案）落在「金錢解決」範圍","5Y 驗證":"5 年內 settlement 完成，UNH retains Optum vertical integration","10Y 驗證":"監管環境穩定，無 Medicare for All 政策推進","具體數字門檻":"Settlement 規模 ≤ $5B（單筆）；無 criminal indictment","信息來源":"DOJ public records；Senate Finance Committee 2026-01 report","漂移觸發":"單筆 settlement &gt; $5B 或 indictment → 直接反轉，不待累積"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"DOJ 升級為 criminal action 或要求 Optum 強制分拆","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"DOJ 季公告、SEC 8-K 重大訴訟 disclosure、CMS RFP 草案","警戒閾值":"任一觸發即重評：(a) criminal indictment；(b) Optum 部分強制分拆訊號；(c) 單筆 settlement &gt; $5B"}},{"id":"R2","text":"MCR 結構性無法回到 87-88%，stuck 在 90%+","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"季 MCR、GLP-1 utilization、心血管 + 高成本特藥 line item","警戒閾值":"連 2 季 MCR &gt; 89.8% → 削弱；連 4 季 &gt; 89.8% → 反轉，clip 至 X"}},{"id":"R3","text":"Optum Health margin 結構性無法回升，垂直整合溢價歸零","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"OH 季 margin、雇用醫師 productivity、provider attrition rate","警戒閾值":"4 個季度 rolling OH margin &lt; 2% 且趨勢未反轉 → 結構性反轉 thesis，clip 至 X"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":388.47,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UNH_20261017/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
