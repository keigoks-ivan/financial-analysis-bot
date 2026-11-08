你是 stock-analyst **v20 判斷 agent**，標的 TPR（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TPR","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1876.6,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":19.3,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":23.6,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"}},{"id":"f_kpi5","label":"管理層指引","value":null,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":null,"basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"},"needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-05","period":"2026-11-05","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-05"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tpr_gross_margin_pct","label":"TPR 毛利率","value":78.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpr_operating_margin_pct","label":"TPR 營業利益率","value":24.53,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpr_fcf_margin_pct","label":"TPR FCF 利潤率","value":22.95,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mc_gross_margin_pct","label":"MC 毛利率","value":34.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mc_operating_margin_pct","label":"MC 營業利益率","value":18.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mc_fcf_margin_pct","label":"MC FCF 利潤率","value":27.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cfr_fcf_margin_pct","label":"CFR FCF 利潤率","value":24.77,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CFR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3","label":"自由現金流","value":469.0,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"}},{"id":"f_kpi4_sbc","label":"SBC 占營業利益","value":7.0,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm（Schedule 8）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":132.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":0.15,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":70.47,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.96 → 7.96）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.89 → 8.89）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.08 → 10.08）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":7.96,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":8.89,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.08,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":13.88,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 6.99 → 7.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":17.07,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝7.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":7.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.19,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝75.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":75.8,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.61,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝77.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":77.9,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":16.68,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 7.96，分子＝快照價 132.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.252,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":3472.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 4254.0、現金 782.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":196.52,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":29569.39,"period":"2026-11-08","unit":"USD m","basis":"市值 26097.39 ＋ 淨負債 3472.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":8599.36,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":9043.81,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（19 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.44,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 132.8 / W52 133.07 / W104 108.15 / W250 65.77 / W250 13週斜率 2.13%"},{"id":"f_ma_w52","label":"52 週均線","value":133.07,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":108.15,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":65.77,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.13,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Coach 財年 Q3 FY2026 固定匯率營收 +29%；北美 +27%、大中華 +58%、歐洲 +27%，報導稱優於產業趨勢、持續取得份額；該季新客約 200 萬，Gen Z 加速。","source":"ouispeakfashion.com — Coach Momentum Accelerates Globally: Tapestry, Inc. Delivers Double-Digit Growth in Q3 FY2026","url":"https://ouispeakfashion.com/2026-05-07-tapestry-inc/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"財經內容稿稱 2025–2026 年 Tapestry 持續從歐洲對手（因大幅漲價疏遠嚮往型客群）手中取得份額；Ralph Lauren 同為雙位數成長，Capri 與 LVMH 時尚皮件表現較分歧。屬二手聚合稿，無一手份額數據。","source":"FinancialContent — The Reinvention of American Luxury: A Deep Dive into Tapestry, Inc. (TPR)","url":"https://markets.financialcontent.com/stocks/article/finterra-2026-4-3-the-reinvention-of-american-luxury-a-deep-dive-into-tapestry-inc-tpr","excerpt":null,"as_of":"2026-04-03","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Michael Kors（Capri）為 Coach 在輕奢手袋的主要對手；Polene、Jacquemus 等小眾品牌透過社群與稀缺性吸引年輕客群，轉售平台（The RealReal、Vestiaire）形成間接競爭。來源為彙整型文章，非一手數據。","source":"retailboss.co / Morningstar 搜尋結果彙整（Coach Is Now 89% Of Tapestry…）","url":"https://retailboss.co/coach-is-now-89-of-tapestry-inside-the-two-brand-portfolio-that-is-quietly-reshaping-accessible-luxury/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"MediaPost 報導 Coach 近 10 億美元行銷飛輪帶動 31% 成長（標題）。","source":"MediaPost — Near-$1B Marketing Flywheel Drives Coach's 31% Gain 05/27/2026","url":"https://www.mediapost.com/publications/article/415316/near-1b-marketing-flywheel-drives-coachs-31-gai.html?edition=142731","excerpt":null,"as_of":"2026-05-27","retrieved_at":"2026-10-05","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2026 10-K（截至 2026-06-27）：沒有任何單一客戶占各分部淨銷售額逾 10%；批發約占總淨銷售額 12%，客戶為百貨、專賣店與第三方數位夥伴。","source":"SEC Form 10-K FY2026, Tapestry, Inc.","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":null,"as_of":"2026-06-27","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 10-K（截至 2026-06-27）：沒有任何單一客戶占各部門淨銷售額超過 10%；批發約占總淨銷售額 12%。","source":"Tapestry Form 10-K FY2026（搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":null,"as_of":"2026-06-27","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Tapestry 對百貨與批發客戶評估信用並控管授信條件以降低呆帳；批發占 FY2024 淨營收約 18%（第三方彙整，非 10-K 原文）。","source":"growthsharematrix.com Tapestry SWOT Analysis／搜尋摘要","url":"https://growthsharematrix.com/products/tapestry-swot-analysis","excerpt":null,"as_of":"2024-12-31","retrieved_at":"2026-10-05","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Tapestry FY2026 Q4 call: CEO says FY26 results show the strategy's power and growth from a higher base within the long-term algorithm; CFO says FY27 guidance does not require holding the same growth level for the rest of the year.","source":"Yahoo Finance, Tapestry Inc (TPR) Q4 2026 Earnings: Key Takeaways","url":"https://finance.yahoo.com/markets/stocks/articles/tapestry-inc-tpr-q4-2026-231010449.html","excerpt":"fiscal 2026 results demonstrated the power of the strategy and that the company is growing from a higher base while maintaining its long-term algorithm.","as_of":"2026-08-14","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Coach handbag AUR rose mid-teens in Q4 and for FY26, with units up low double digits; Tabby expected to show no slowdown; platforms expanding in the $200-$500 price range.","source":"Yahoo Finance, Tapestry Inc (TPR) Q4 2026 Earnings: Key Takeaways","url":"https://finance.yahoo.com/markets/stocks/articles/tapestry-inc-tpr-q4-2026-231010449.html","excerpt":"Increased at a mid-teens rate in Q4; for the year, rose mid-teens with units up low double digits.","as_of":"2026-08-14","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY2027 guidance: revenue $8.4-8.5B, operating margin up about 50bp to nearly 24%, EPS $7.80-7.90.","source":"Yahoo Finance, Tapestry Inc (TPR) Q4 2026 Earnings: Key Takeaways","url":"https://finance.yahoo.com/markets/stocks/articles/tapestry-inc-tpr-q4-2026-231010449.html","excerpt":"$8.4 billion to $8.5 billion","as_of":"2026-08-14","retrieved_at":"2026-10-05","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Search summary of industry reports: global luxury market expected to grow 1-3% a year 2024-2027; 3-5% in 2026; US 4-6% 2025-2027. Specific report dates not confirmed; aggregated from multiple secondary sources.","source":"WebSearch results: 'luxury demand outlook 2027 2028 consensus' (McKinsey State of Luxury, Fashion Dive and others)","url":"https://www.mckinsey.com/industries/retail/our-insights/state-of-luxury","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-05","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FTC 於 2024-04-23 起訴阻止 Tapestry 收購 Capri（約 85 億美元），法院其後核准初步禁制令，交易被擋下；屬過往併購反壟斷案，非對 TPR 現有業務的調查。","source":"WUSTL Law Review: Is Dealmaking Going Out of Fashion? The Impact of the FTC-Tapestry, Inc. Litigation on M&A Activity in the Fashion Industry","url":"https://wustllawreview.org/2026/02/25/is-dealmaking-going-out-of-fashion-the-impact-of-the-ftc-tapestry-inc-litigation-on-ma-activity-in-the-fashion-industry/","excerpt":"following an investigation and 5-0 approval vote by FTC commissioners, the FTC sued on April 23, 2024.","as_of":"2026-02-25","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"法學評論稱 FTC 勝訴形成先例，可能限制「輕奢」層級未來的併購整合。","source":"WUSTL Law Review (2026-02-25)","url":"https://wustllawreview.org/2026/02/25/is-dealmaking-going-out-of-fashion-the-impact-of-the-ftc-tapestry-inc-litigation-on-ma-activity-in-the-fashion-industry/","excerpt":"The FTC's successful challenge of the Capri merger has set a precedent that will likely limit future consolidation within the \"accessible luxury\" tier.","as_of":"2026-02-25","retrieved_at":"2026-10-05","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Tapestry 預估美國關稅將使 FY2026 成本增加約 1.6 億美元，預期 2028 年前完全抵銷；FY2026 EPS 指引 5.30–5.45 美元，其中約 0.60 美元缺口來自關稅（含取消 de minimis 免稅）。","source":"Mexico Business News: Coach Owner Warns US Tariffs May Cost US$160 Million in FY2026（發布日以 2025-08-14 財報日近似，頁面日期未讀取）","url":"https://mexicobusiness.news/ecommerce/news/coach-owner-warns-us-tariffs-may-cost-us160-million-fy2026","excerpt":"Tapestry, the parent company of Coach and Kate Spade, warned that US tariffs could cost the company about US$160 million in fiscal 2026, with full offset expected by 2028.","as_of":"2025-08-14","retrieved_at":"2026-10-05","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"手袋多在越南、柬埔寨、菲律賓、印度生產，搜尋結果未顯示中國為主要關稅暴露來源；另已累計逾 2 億美元 IEEPA 與對等關稅成本。","source":"同上搜尋彙整（Mexico Business News／Inside Retail Asia，2025-08）","url":"https://mexicobusiness.news/ecommerce/news/coach-owner-warns-us-tariffs-may-cost-us160-million-fy2026","excerpt":"Most of Tapestry's handbags are manufactured in Vietnam, Cambodia, the Philippines, and India.","as_of":"2025-08-14","retrieved_at":"2026-10-05","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"搜尋摘要稱：越南、柬埔寨、菲律賓合計佔 Tapestry 約 70% 生產；Coach 與 Kate Spade 多數手袋在越南、柬埔寨、菲律賓、印度製造（東南亞集中）。","source":"Inside Retail Asia - Can Coach carry the weight as tariffs bear down on Tapestry?","url":"https://insideretail.asia/2025/08/18/can-coach-carry-the-weight-as-tariffs-bear-down-on-tapestry/","excerpt":null,"as_of":"2025-08-18","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"搜尋摘要稱：中國僅佔 Tapestry 約 10% 採購；三大生產國面臨 10% 關稅，關稅衝擊 FY2026 約 1.6 億美元。","source":"Inside Retail Asia / Mexico Business News (Coach Owner Tapestry Sees US$160 Million Profit Hit from Tariffs)","url":"https://mexicobusiness.news/ecommerce/news/coach-owner-tapestry-sees-us160-million-profit-hit-tariffs","excerpt":null,"as_of":"2025-08-18","retrieved_at":"2026-10-05","affects":["valuation","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"搜尋摘要稱：Tapestry 在 FY2026 10-K 列美中關係不確定性與貿易協定參與變動為風險因子；國際業務約佔淨銷售 40%。10-K 全文未讀，as_of 取會計年度結束日。","source":"SEC Form 10-K FY2026 (period ending 2026-06-27)","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":null,"as_of":"2026-06-27","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"搜尋摘要稱：Greater China 為 FY26 Q3 最強國際成長動能（固定匯率 +55%）；中國同時是銷售市場，與生產端分離。","source":"Yahoo Finance - Tapestry's International Growth Accelerates on China & Europe Gains","url":"https://finance.yahoo.com/markets/stocks/articles/tapestrys-international-growth-accelerates-china-124200007.html","excerpt":null,"as_of":"2026-05-01","retrieved_at":"2026-10-05","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"FY2026 全年營收 $8.00B（+14%）；Coach $6.91B（+24%）；Kate Spade $1.07B（-10%）。","source":"Ouispeakfashion: Tapestry Reports 14% Revenue Growth in Fiscal 2026 as Coach Sales Rise 24%（搜尋摘要）","url":"https://ouispeakfashion.com/tapestry-fiscal-2026-earnings/","excerpt":"Tapestry's fiscal 2026 revenue increased 14% to $8.00 billion, led by 24% growth at Coach, which generated $6.91 billion in full-year revenue. In contrast, Kate Spade New York reported annual revenue of $1.07 billion, down 10%.","as_of":"2026-08-13","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Kate Spade 前九個月淨銷售 -11.1% 至 $839.8M；Q4 -7% 至 $235.1M；管理層稱精簡動作對營收的拖累大於預期。","source":"SEC 10-Q (tpr-20260328) 與 WWD: Tapestry Q4 earnings（搜尋摘要）","url":"https://wwd.com/business-news/financial/tapestry-q4-earnings-coach-kate-spade-1239117671/","excerpt":"Kate Spade net sales decreased 11.1% or $104.7 million to $839.8 million in the first nine months of fiscal 2026. The decline continued through the full year, with Kate Spade slipping 7 percent to $235.1 million in the fourth quarter.","as_of":"2026-08-13","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Kate Spade 任命 Jonathan Saunders 為創意總監，作為轉型計畫一環。","source":"WWD / 搜尋摘要","url":"https://wwd.com/business-news/financial/tapestry-q4-earnings-coach-kate-spade-1239117671/","excerpt":"The brand named Scottish fashion designer Jonathan Saunders as its creative director last month, as part of a turnaround plan that includes improvements in product design and visual identity.","as_of":"2026-08-13","retrieved_at":"2026-10-05","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Coach 在 18–27 歲族群品牌偏好排名第一，FY2026 新增近九百萬客戶，Gen Z 為主要來源。","source":"Fortune: How Coach became Gen Z's favorite affordable luxury handbag brand（搜尋摘要）","url":"https://fortune.com/2026/05/19/coach-handbags-comeback-millennials-gen-z/","excerpt":"Coach now ranks #1 in brand preference among 18-27 year olds, completely overtaking similarly priced competitors like Michael Kors and Kate Spade. The brand attracted more than two million new customers during the quarter and nearly nine million during fiscal 2026, with Gen Z leading customer acquisition.","as_of":"2026-05-19","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Coach Q4 手袋平均單價（AUR）成長中十位數百分比，銷量大致持平；做法是減少促銷日而非加大折扣。","source":"Retail Insider: Coach Expands Store Investment as Gen Z Drives Global Growth（搜尋摘要）","url":"https://retail-insider.com/retail-insider/2026/08/coach-expands-store-investment-as-gen-z-drives-global-growth/","excerpt":"Handbag average unit retail increased at a mid-teens rate during the fourth quarter while unit volumes were roughly in line with the previous year, reflecting a decision to reduce promotional days rather than pursue additional discounting.","as_of":"2026-08-31","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Tapestry FY2026 10-K 風險因素稱：消費者愈來愈常用 AI 購物助理來探索商品、比價、下單，可能改變商務並影響公司吸引並留住數位平台客戶的能力（as_of 為 FY2026 財年結束日，實際申報日未確認）","source":"Tapestry Inc. Form 10-K FY2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":null,"as_of":"2026-06-27","retrieved_at":"2026-10-05","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"二手奢侈品市場估計 2026 年約 416 億美元（2025 年約 379 億），成長速度約為一手市場三倍；Gen Z 衣櫃 45% 的手袋為二手（來源為聚合文章，數字未回溯至原始報告）","source":"Luxury Resale Market: 2026 Gen Z $41B Boom Disrupts Status (editorialge.com)；Forbes Resale Market 2026 (2025-12-16)","url":"https://editorialge.com/luxury-resale-market-2026/","excerpt":null,"as_of":"2025-12-16","retrieved_at":"2026-10-05","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Tapestry 與 Adobe Firefly 合作以自有素材訓練客製生成式 AI 模型，用於手袋設計流程；FY2026 取得首件 AI 專利","source":"Adobe Business Blog: Coach reimagines handbag design process with Adobe Firefly；搜尋摘要","url":"https://business.adobe.com/blog/coach-reimagines-handbag-design-process-with-adobe-firefly-generative-ai","excerpt":null,"as_of":"2026-06-27","retrieved_at":"2026-10-05","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FY2026 DTC約佔總淨銷售87%；DTC營收Q4成長11%、全年成長16%，數位營收全年高個位數後段（high-teens）成長、門店營收中高個位數（mid-teens）成長。","source":"Tapestry Form 10-K FY2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":"DTC revenues were approximately 87% of total net sales in fiscal 2026","as_of":"2026-06-27","retrieved_at":"2026-10-05","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"批發占比FY2025約13%；摘要稱計畫持續關閉不賺錢門店並退出批發合作，以維持價格完整性（此段為搜尋摘要彙整，未逐項對到原文，as_of為FY2026 10-K期末日）。","source":"Tapestry Form ARS FY2025／搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/1116132/000114036125036305/ny20053837x3_ars.pdf","excerpt":"Wholesale represented approximately 13% of our total net sales for fiscal 2025","as_of":"2025-08-01","retrieved_at":"2026-10-05","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY27 Q1 (2026-11-05) 後公司上調全年調整後 EPS 指引至 $8.25–$8.35（原 $7.80–$7.90），高於共識 $7.96；營收指引 $8.5–8.6B 對共識 $8.538B 約在區間內。","source":"finviz: Tapestry shares rise over 8% as fiscal Q1 earnings exceed forecasts and 2027 outlook improves","url":"https://finviz.com/news/417150/tapestry-shares-rise-over-8-as-fiscal-q1-earnings-exceed-forecasts-and-2027-outlook-improves","excerpt":"Tapestry increased its full-year adjusted earnings per share forecast to $8.25–$8.35, compared with its previous guidance of $7.80–$7.90.","as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-08-13 FY27 初始指引 EPS $7.80–7.90、營收 $8.4–8.5B，與當時共識（EPS $7.82、營收 $8.464B）大致相符，但股價盤前跌 8.9%。","source":"RTTNews: Tapestry sees growth in FY27...shares down 8.8%","url":"https://www.rttnews.com/3680116/tapestry-sees-growth-in-fy27-swings-to-profit-in-q4-boosts-dividend-16-shares-down-8-8.aspx","excerpt":null,"as_of":"2026-08-13","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Chartmill 顯示 FY2027 EPS 共識 8.06（24 位分析師，2026-10-17），為 Q1 公布與上調指引前的數字。","source":"Chartmill TPR estimates","url":"https://www.chartmill.com/stock/quote/TPR/estimates","excerpt":"Latest recorded estimate: 8.06 USD · Oct 17, 2026 · 24 analysts","as_of":"2026-10-17","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布（各來源不一、多未標日期）：MarketBeat 2026-08-04 共識 $173.88 Moderate Buy，JPMorgan 目標 $211；Investing.com 平均 165.05、高 200、低 88（19 位）；MarketBeat 預測頁共識 $170.06（21 位：15 買、1 強買、5 持有）。","source":"MarketBeat 2026-08-04 alert; Investing.com consensus","url":"https://www.marketbeat.com/instant-alerts/tapestry-nysetpr-price-target-raised-to-21100-2026-08-04/","excerpt":"According to projections from 19 analysts, the average 12-month share price target for Tapestry is 165.05 USD, with a high estimate of 200 USD and a low estimate of 88 USD.","as_of":"2026-08-04","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q1 結果：調整後 EPS $1.82 對共識 $1.56；Q2 EPS 指引 $3.05 對共識 $3.02；Kate Spade 營收 -10% 並轉調整後營業虧損；有分析稱上調幅度符合市場預期。","source":"finviz: Tapestry Inc reports fiscal 2027 first quarter results and raises full year outlook","url":"https://finviz.com/news/416639/tapestry-inc-reports-fiscal-2027-first-quarter-results-and-raises-full-year-outlook","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"兩宗與已終止之 Capri 併購相關的證券集體訴訟（2024-12-23、2025-01-28 於德拉瓦聯邦地院提起）針對 Tapestry 及高管；公司 2025-07-14 聲請駁回，10-K（FY2026）仍列為未決事項。","source":"SEC EDGAR 10-K FY2026 財報附註（訴訟）","url":"https://www.sec.gov/Archives/edgar/data/1116132/000111613226000018/tpr-20260627.htm","excerpt":"two separate putative securities class actions were filed on December 23, 2024 and January 28, 2025, by plaintiff shareholders in the United States District Court for the District of Delaware against Capri and certain of its officers and against Tapestry and certain of its officers","as_of":"2026-08-13","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"SEC EDGAR 近12個月 6 份 8-K，含重大項目者 0 份（僅財報、董監事異動、股東會投票）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001116132&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月 8-K 清單無併購類重大項目（1.01／2.01 等）；Capri 併購已於 2024-11 終止。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001116132&type=8-K","excerpt":"2025-11-08 至 2026-11-08 共 6 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Capri 併購終止後的兩宗證券集體訴訟仍未決，公司 2025-07-14 聲請駁回。","source":"SEC EDGAR 10-K FY2026 財報附註（訴訟）","url":"https://www.sec.gov/Archives/edgar/data/1116132/000111613226000018/tpr-20260627.htm","excerpt":"On July 14, 2025, the Company moved to dismiss the complaint.","as_of":"2026-08-13","retrieved_at":"20261108","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 無 Item 4.02（財報不可信賴／重編）項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001116132&type=8-K","excerpt":"其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"TPR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":78.31,"operating_margin_pct":24.53,"fcf_margin_pct":22.95,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"RMS","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RMS"},"note":"quarterly_income_stmt 無資料"},{"name":"MC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.36,"operating_margin_pct":18.4,"fcf_margin_pct":27.54,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CFR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":24.77,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CFR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KER","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KER"},"note":"quarterly_income_stmt 無資料"}],"subject":"TPR"},"financial_history":{"ticker":"TPR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":6660900000.0,"revenue_yoy_pct":null,"gross_margin_pct":70.78,"operating_margin_pct":17.6,"net_income":936000000.0,"diluted_eps":3.88,"free_cash_flow":791000000.0,"fcf_margin_pct":11.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":6671200000.0,"revenue_yoy_pct":0.15,"gross_margin_pct":73.29,"operating_margin_pct":17.09,"net_income":816000000.0,"diluted_eps":3.5,"free_cash_flow":1146700000.0,"fcf_margin_pct":17.19,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":7010700000.0,"revenue_yoy_pct":5.09,"gross_margin_pct":75.44,"operating_margin_pct":18.11,"net_income":183200000.0,"diluted_eps":0.82,"free_cash_flow":1093900000.0,"fcf_margin_pct":15.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":8004200000.0,"revenue_yoy_pct":14.17,"gross_margin_pct":77.82,"operating_margin_pct":23.92,"net_income":1527700000.0,"diluted_eps":7.27,"free_cash_flow":1812500000.0,"fcf_margin_pct":22.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TPR/TPR_Q1_2027_Earnings_Call_20261105.md）

# Q1 2027 Earnings Call
**Tapestry, Inc.** | Earnings Calls | 2026-11-05

**Operator** (Operator):
Good day, and welcome to this Tapestry conference call.
Today's call is being recorded. [Operator Instructions]
At this time, for opening remarks and introductions, I would like to turn the call over to the Global Head of Investor Relations, Christina Colone.

**Christina Colone** (Executives):
Good morning. Thank you for joining us. With me today to discuss our first quarter results, our strategies and our outlook are Joanne Crevoiserat, Tapestry's Chief Executive Officer; and Scott Roe, Tapestry's Chief Financial Officer and Chief Operating Officer.
Before we begin, we must point out that this conference call will involve certain forward-looking statements within the meaning of the Private Securities Litigation Reform Act. This includes projections for our business in the current or future quarters or fiscal years. Forward-looking statements are not guarantees, and our actual results may differ materially from those expressed or implied in the forward-looking statements.
Please refer to our annual report on Form 10-K, the press release we issued this morning and our other filings with the Securities and Exchange Commission for a complete list of risks and other important factors that could impact our future results and performance.
Non-GAAP financial measures are included in our comments today and in our presentation slides. For a full reconciliation to corresponding GAAP financial information, please visit our website, www.tapestry.com/investors, and then view the earnings release and the presentation posted today.
Now let me outline the speakers and topics for this conference call. Joanne will begin with highlights for Tapestry and our brands. Scott will continue with our financial results, capital allocation priorities and our outlook going forward. Following that, we will hold a question-and-answer session where we will be joined by Todd Kahn, CEO and Brand President of Coach. After Q&A, Joanne will conclude with brief closing remarks.
I'd now like to turn it over to Joanne Crevoiserat, Tapestry's CEO.

**Joanne Crevoiserat** (Executives):
Good morning. Thank you, Christina, and welcome, everyone. Our first quarter marked a powerful start to the year with revenue, margin and earnings growth ahead of expectations and strength around the world. Our Amplify strategy continues to drive our outperformance as we consistently deliver our distinctive combination of creativity, craftsmanship and value.
During the quarter, we grew revenue by 12% on a pro forma basis to $1.9 billion, expanded operating margin by 230 basis points to over 23% and increased earnings per share by 32% to $1.82. We drove strong customer acquisition as we welcomed 2.6 million new customers to our brands, with Gen Z representing approximately 35%. Our core leather goods category continued to fuel our growth with both handbag AUR and unit growth. Luxury leather goods remains one of the most attractive categories within the consumer space because of its enduring demand, compelling economics and significant runway for growth.
In addition, we delivered broad-based growth across regions, gaining share and expanding the market. Growth in North America exceeded our expectations and drove our beats, while International added to our performance with strong double-digit revenue increases. Overall, building on this outperformance, we are raising our full year outlook, reflecting our confidence in the durability of our growth. Behind these results are advantages that compound over time, including our deep consumer understanding, data-driven approach and global scale. Together, they reinforce our conviction that our greatest opportunities are ahead of us.
Now, moving to our results by brand. Coach delivered another strong quarter with constant currency revenue growth of 16% and increasing gross margin and profitability, demonstrating the enduring desirability and relevance of our iconic 85-year-old brand. Several factors continue to underscore the durability of our growth. We drove new customer acquisition around the world, welcoming over 2.1 million new consumers in the quarter. This growth was led by Gen Z, a key focus of our strategy. At the same time, existing customers continue to drive strong sales growth, reflecting our ability to attract new consumers and deepen those relationships over time.
Our leather goods assortment continued to drive our growth, with handbag AUR increasing at a low double-digit rate and unit volumes growing low single digits. The strength of the brand is evident in how we're growing and in the choices we're making to support durable long-term growth. We delivered handbag AUR and strong unit growth within our $200 to $500 sweet spot, while intentionally deemphasizing more promotional price points, resulting in a planned unit decline below $200. Importantly, we continue to see significant runway to grow both AUR and units while staying true to the brand's core value proposition.
Touching on trends by geography at constant currency, we achieved strong global results with North America up 7%, greater China up 41%, Europe up 27% and Japan returning to growth with a 5% increase. This broad strength demonstrates our ability to grow in established markets while expanding our reach in markets where we remain underpenetrated.
Overall, our performance continues to reinforce the power of Coach's expressive luxury positioning and the exceptional execution of our teams. Our heritage and relevance allow us to connect with a broad audience around the world, bringing new consumers into the category and into our brand. With a large addressable market and significant opportunity ahead, we see a clear path for Coach to become a $10 billion brand.
Now, to cover our first quarter results in more detail, our key families continued to outperform with strength across the assortment. The New York, Tabby, Teri collections drove Gen Z acquisition and reinforced Coach's leadership in its core category with a robust innovation pipeline ahead. Structurally, we concentrate on product innovation behind core families that build over time, remaining disciplined in our pursuit of sustainable and profitable growth.
We also continue to see clear benefits from our One Coach strategy. By unifying the brand experience across channels, we are creating a stronger, more consistent expression of Coach, helping drive customer acquisition, higher AURs and growth around the world.
Next, turning to footwear, a significant growth opportunity for Coach. Revenue grew over 20% in the quarter, driven by the Margot family and the continued success of sneakers.
Turning to marketing. We continue to invest behind sustained cultural relevance and demand creation at scale. This quarter, we launched Live Your Story, the latest expression of our Courage to Be Real brand purpose. Our approach is globally connected and locally relevant, combining consistent brand storytelling with experiences and cultural partnerships tailored to consumers around the world. With this campaign, we are creating connection and empowering self-expression through music, which includes a new global cultural partnership with Spotify. Early results are encouraging with strong consumer engagement and positive brand lift.
Our marketing approach reflects the strength of our consumer insights and our ability to turn those insights into meaningful engagement and customer acquisition globally. And finally, we continue to invest in and innovate across our physical touch points with consumers, creating distinctive experiences that build brand desire and deepen engagement with Coach. We are rolling out our expressive luxury store concept globally. These stores are outperforming our investment targets across both new stores and remodels, driving higher traffic and longer dwell times, particularly among Gen Z consumers. This supports our plan to expand the concept to impact approximately 80% of our traffic by fiscal year '30. In addition, Coach Play is building brand desire with our target consumers, while providing insights that we are applying across the broader store experience.
Our food and beverage concepts are also outperforming, and we plan to continue expanding our coffee shop presence in North America. Our stores are both a place to connect with consumers and a powerful driver of growth. With strong field teams and a productive store fleet, we see significant opportunity to build on that strength through continued investment and innovation.
Looking ahead to holiday, we're leaning into proven drivers of the business, bringing the full expression of Coach to life through our assortment and store experiences. All stores will feature festive decor, including trees with custom Coach ornaments. Our gifting assortment includes fragrance box sets, new bag charms and straps, and seasonal colors and customer favorites such as Tabby, Brooklyn and Chelsea.
In closing, my confidence in Coach is grounded in the strength of the brand and how we're stewarding it for the future. We're building on 85 years of heritage with deep consumer understanding, disciplined execution, and continuous innovation, preserving what makes the brand distinctive while connecting with new generations of consumers around the world. This unique combination gives me confidence in Coach's continued leadership and significant long-term growth.
Turning to Kate Spade. Our strategy for Kate Spade is consistent and phased. Streamlining the business, solidifying the foundation and positioning the brand to scale for sustainable, profitable growth. During the quarter, revenue declined 10%, consistent with guidance, while gross margin expanded 190 basis points. We remain focused on strengthening the underlying business and continue to make strategic investments to support long-term growth.
Moving forward, a key priority is sharpening our creative execution in product and storytelling. Jonathan Saunders, our newly appointed Executive Creative Director, is working alongside our brand CEO, Eva Erdmann, to bring uplifting luxury to life for a new generation of consumers.
Now, touching on the first quarter results in more detail. First, we are investing in marketing to build brand relevance and connect with our target consumers. Our fall campaign, featuring Tyla, the brand's new global ambassador, and a constellation of influencers reinforced the brand's ethos to discover, share and spread joy. We achieved greater reach and strong organic engagement with Gen Z consumers whose brand consideration and purchase intent rose after engaging with the campaign. For holiday, we'll build on this engagement through creator content and social activations designed to increase awareness, build brand desire and drive customer acquisition.
Next, we continue to strengthen our handbag offering led by our blockbusters. Consistent with our strategy, handbags are driving customer acquisition with nearly 500,000 new customers entering the brand at higher AUR. This was led by our blockbuster families of Margot, 454 and Duo. For holiday, we'll animate these proven styles with seasonal colors and finishes and expand gifting opportunities at entry price points in small leather goods, charms and jewelry.
Finally, we continue to focus on creating compelling omnichannel experiences. Stores with our light-touch renovation program continued to achieve a lift in sales through improvements in conversion and average transaction value. We now have approximately 50 locations in this format with plans to add another 30 over the balance of the year.
To close, we remain confident in Kate Spade's long-term potential. With the creative team in place, we are bringing together the brand's distinctive identity and Tapestry's capabilities to build lasting consumer demand and position the brand for sustainable, profitable growth over time.
Before turning it over to Scott, I want to reiterate my confidence in the durability of Tapestry's growth and my excitement about where we're heading. We have a clear vision, a deep understanding of our consumers and exceptional teams that bring creativity, strategic thinking and disciplined execution to everything we do. Against the complex backdrop, our agile operating model and compelling combination of craftsmanship and value position us to compete and win, driving long-term growth and shareholder returns.
With that, I'll hand it over to Scott.

**Scott Roe** (Executives):
Thanks, Joanne, and good morning, everyone. Our first quarter results highlight the compounding benefits of our financial model. We are driving strong growth at scale, expanding an already strong margin profile and generating significant free cash flow. This gives us the capacity to invest in our brands and business to support durable growth while returning meaningful capital to shareholders.
So with that, let me walk through our first quarter results in more detail, starting with revenue trends on a pro forma constant currency basis. Sales increased 12% compared to the prior year with growth across regions. North America sales rose 4%, driven by a 7% increase at Coach, where we continued to deliver healthy growth and expanding gross margins. North America revenue and margins both exceeded our guidance. In Europe, revenue grew 22%, fueled by continued new customer acquisition and growth among local consumers. Given our strong momentum and relatively low market penetration, Europe remains a compelling long-term growth opportunity. We have runway to increase productivity across our existing business and reach more consumers by expanding our digital store and wholesale presence in both existing and new markets.
Now, turning to Greater China. Revenue rose 39%, with growth across channels. Coach's quality, craftsmanship and value together with its brand promise of authenticity and self-expression are attracting Gen Z consumers and driving market share gains. Our strong regional teams and more than 2 decades in China give us deep understanding of the local consumer. Building on this foundation, we're investing incrementally in brand building to capture the significant growth opportunity ahead. In Other Asia, revenue increased 23%, led by growth in South Korea and Australia. And in Japan, we inflected to growth with sales increasing 4%. Taken together, we remain confident in the long-term revenue drivers of our business with durable growth in North America, complemented by strong growth in international markets.
Now, touching on revenue by channel for the quarter. We drove a 9% increase in direct-to-consumer revenue, exceeding expectations, with store revenue growing low double digits and digital increasing mid-single digits. In addition, we delivered wholesale growth of approximately 30%. Breaking this down by region, with a focus on Coach, our wholesale growth was driven by international markets where we're growing brand awareness and reaching new customers. Conversely, in North America, Coach's growth was driven by our direct business with wholesale, a relatively small portion of sales growing due to strong point-of-sale trends at major department stores. So, overall, strong profitability in each of our channels allows us to meet consumers where they are, delivering brand-accretive experiences at compelling returns.
Moving down the P&L. We delivered a first quarter gross margin of 78.7%, up 220 basis points versus last year. This reflected 130 basis points of operational expansion, a 70 basis point net benefit from lower tariffs and duties and a 20 basis point benefit from FX. Gross margin exceeded guidance by 100 basis points, with 50 basis points of our upside coming from operational outperformance and 50 basis points due to tariff favorability.
Turning to SG&A. We leveraged 10 basis points versus last year, which was better than our guidance. Marketing represented over 12% of sales in the quarter, up 140 basis points as we continue to invest behind growth while maintaining strong operational discipline. Overall, operating margin expanded 230 basis points in the quarter driving a 24% increase in operating income ahead of our expectations.
First quarter EPS increased 32% to $1.82, exceeding guidance by approximately $0.27. This outperformance was driven by an $0.18 operational beat, reflecting higher revenue, stronger gross margin and lower expenses, $0.05 from lower tariffs and approximately $0.04 from a lower tax rate and share count combined.
Now, turning to shareholder returns. In the first quarter, we returned approximately $700 million to shareholders, including $600 million in share repurchases and over $90 million in dividends. We now expect to return approximately $2 billion to shareholders in fiscal 2027. This includes an increase of $350 million in share repurchases to $1.7 billion and an expected annual dividend of $1.85 per share. Our strong free cash flow generation enables us to increase shareholder returns while continuing to invest in our brands and business for the long term.
And now, before turning to the details of our balance sheet and cash flows, I'd like to reiterate our capital allocation priorities, which are unchanged. We have two foundational commitments. First, to invest in our brands and business to support long-term sustainable growth and to return capital to shareholders via our dividend with a goal over time to increase the dividend at least in line with earnings growth. Beyond these two foundational commitments, our robust cash flow generation provides us with balance sheet flexibility for value creation. This includes the opportunity for share repurchase activity under our previously announced share repurchase authorization. 
And finally, utilizing our rigorous 4-lens framework, we consistently evaluate opportunities for strategic portfolio management. Importantly, and as previously communicated, before moving forward with any acquisitions, we will ensure Coach remains strong and Kate Spade has returned to sustainable top line growth. These clear capital allocation priorities are underpinned by our firm commitment to a solid investment-grade rating and maintaining our long-term gross leverage target of below 2.5x. 
Now, turning to the details of our balance sheet and cash flows. We ended the quarter with $782 million in cash and short-term investments and total borrowings of $2.6 billion, representing net debt of $1.8 billion. Our gross debt to adjusted EBITDA leverage ratio was 1.1x, more than a full turn below our long-term target. Adjusted free cash flow totaled $56 million in the quarter and inventory at quarter end was 4% above prior year. Our inventories remain current and well positioned, and we continue to expect fiscal '27 inventory levels to increase year-over-year to support our growth. 
Now, moving to our guidance for fiscal '27, which is provided on a non-GAAP and comparable 52-week versus 52-week basis. We are raising our full year revenue, operating margin and EPS outlook, reflecting the strength of our business and our confidence in the future. For the fiscal year, we expect revenue of $8.5 billion to $8.6 billion representing 6% to 7% growth on a constant currency basis. FX is expected to be a 30 basis point tailwind for the year.
Touching on sales by region on a constant currency basis. In North America, we expect revenue to increase low single digits with Coach up mid-single digits in North America for the year. In both Europe and Greater China, we expect growth of mid-teens. In Japan, we're forecasting a return to growth of low single digits, and in Other Asia, we now anticipate low double-digit growth. By brand, this guidance continues to incorporate high single-digit growth at Coach, and a high single-digit decline at Kate Spade.
In addition, our outlook assumes operating margin expansion of approximately 100 basis points to more than 24%, driven by both an increase in gross margin and SG&A leverage. We expect gross margin to increase by approximately 80 basis points, driven by operational improvements and favorable geographic and brand mix. Embedded in our outlook is the assumption for a low to mid-20s percent tariff rate on U.S. imports for fiscal '27 resulting in a modest net P&L benefit year-over-year, including mitigating actions. On SG&A, we expect approximately 20 basis points of leverage, reflecting disciplined expense management while continuing to invest behind brand growth.
For some texture on operating profit by brand, we expect Coach's operating margin to be approximately 36% and at Kate Spade, we continue to expect a modest operating loss, reflecting ongoing investment in the brand. Corporate expenses are expected to leverage for the year. 
Moving to below the line expectations for the year. Net interest expense is forecasted to be approximately $60 million, a modest increase from our prior guidance, reflecting lower cash balances and higher commercial paper borrowings to fund incremental share repurchases. The tax rate is expected to be approximately 18% and our weighted average diluted share count for the year is expected to be approximately 200 million, which includes $1.7 billion in share repurchase activity planned for the year. 
Taken together, we expect EPS of $8.25 to $8.35, representing 17% to 18% growth versus prior year and a meaningful increase from our prior outlook of $7.80 to $7.90. To help bridge, $0.27 of the increase is due to our Q1 outperformance. Looking at the balance of the year, approximately $0.12 is due to below the line items, driven primarily by incremental share repurchases. The remaining increase primarily reflects higher revenue expectations driven by North America, still within our original guidance range for the region and underscoring our confidence in the achievability of the outlook.
As a reminder, our guidance is provided on a comparable 52-week basis. Fiscal 2027 includes a 53rd week, which is expected to contribute approximately 1 percentage point of annual revenue growth and have a neutral impact on operating margin. 
Moving on, we anticipate adjusted free cash flow to approach $1.7 billion. And finally, we expect CapEx and cloud computing costs to be in the area of $300 million or 3% to 4% of revenue. This reflects a year-over-year step-up in investment to support future growth, including incremental investment in Coach's store fleet through new openings and renovations. Approximately 70% of our spend will be related to growing and enhancing our fleet with the balance primarily supporting our ongoing technology and digital investments. 
Now, touching on expectations by quarter. Our Q2 guidance reflects our latest expectations, while our revenue outlook for the balance of the year is consistent in aggregate with our long-term financial algorithm. In Q2, specifically, we expect revenue growth of 5% to 6% on a constant currency basis versus the prior year. Using the midpoint of the guidance range, nominal revenue growth will be approximately 6%, including an expected FX tailwind of 70 basis points. Our top line guidance incorporates high single-digit growth at Coach, including mid-single-digit growth in North America and mid-teens growth internationally. On a 2-year basis, total Coach sales growth is in the mid-30% range. At Kate Spade, we've embedded a low double-digit decline. 
Turning to margins. We expect gross margin to increase by 170 basis points in Q2 and SG&A to increase by roughly 120 basis points, driven primarily by increased marketing investment. This results in operating margin expansion of 50 basis points versus prior year. Taken together, we expect Q2 EPS of approximately $3.05, representing low teens growth. 
Beyond Q2, we continue to anticipate uneven profitability by quarter given macro uncertainty evolving tariff dynamics, and shifts in the timing of investments year-over-year. With that said, for the second half of the year, we've embedded mid-single-digit revenue growth, and using the midpoint of our guidance range, low-teens EPS growth, with Q4 outpacing Q3 given prior year comparisons. Importantly, we remain confident in our ability to drive sustainable growth and build on our proven track record of delivering on our commitments.
So to close our prepared remarks, our strong start to the year reinforces the power and durability of our financial model. Our outperformance positioned us to raise our full year revenue, operating margin and EPS outlook and increase expected shareholder returns to $2 billion, all while continuing to invest in growth and competitive advantages. We are building on significant earnings power and cash flow generation with substantial runway to grow both well into the future. We move forward with confidence in the opportunities ahead and in our ability to deliver long-term shareholder value.
I'd now like to open it up and take your questions.

**Operator** (Operator):
[Operator Instructions] And we'll take our first question from Ike Boruchow with Wells Fargo.

**Irwin Boruchow** (Analysts):
Congrats on the great first quarter, strong beat and raise, like it. Just curious what gives you guys the confidence in the durability of a mid-single-digit growth in North America Coach, both in the second quarter and the fiscal year. I know you're anniversarying some pretty difficult compares. And then, just more broadly, thoughts on the U.S. consumer backdrop.

**Operator** (Operator):
Team, you may want to check your mute switches?

**Joanne Crevoiserat** (Executives):
Thanks, Ike. Can you hear me?

**Operator** (Operator):
Yes. Now we can.

**Joanne Crevoiserat** (Executives):
Okay. Sorry, having technical -- okay. Thank you for your comments. I'll kick us off and then turn it to Todd to comment on Coach specifically, but our first quarter shows the strength we're delivering around the world. Our strategies are working. We're bringing new customers into the market and our brands, and we're taking share globally. But you asked about North America specifically, and growth in the region drove our beat in the quarter. And you're seeing the results of deliberate actions we're taking to drive durable growth over the long term in our largest market. That's what gives us confidence, and that confidence is reflected in the increased outlook that we shared for the balance of the year as well.
Here's what we're seeing from consumers. Leather goods is driving our growth. And I think that shows the relevance of the category with consumers and the durability of this category. And we're driving strong customer acquisition, which is a testament to the execution behind our strategy, and we're seeing growth across generations, our target Gen Z consumer as well as non-Gen Z consumers are growing and we're seeing growth across income cohorts. So we're seeing broad-based consumer resilience. 
And the backdrop in the U.S., while we see a discerning consumer, they're choosing our category and our brand, and our value proposition has never been stronger. Industry forecast for holiday in the U.S. are calling for mid-single-digit growth. So there's a constructive backdrop overall as we head to holiday. At Coach, we're looking at mid-single-digit growth expectations for both the quarter and for the year in North America. We're ready to compete and win. Our teams are focused, we're aligned and we're executing with excellence.
But let me invite Todd to add his perspective on Coach.

**Todd Kahn** (Executives):
[indiscernible]. And let me be very clear. I am incredibly confident about the durability of the Coach brand to continue to grow both globally and in North America. First, it's worth remembering that in the last 23 quarters, we have grown 22 of them. That's a track record of consistency that I think makes us rather unique. In North America, this last quarter, we grew 7%, which is an acceleration from Q4 on a 2-year stack basis and of course, a beat to our guidance. What's important is almost all of the growth is coming from our direct business, which will continue in -- for the balance of the year.
As Joanne mentioned, our guidance embeds Coach North America at mid-single digits for Q2 and for the balance of the year. And as I look at the holiday quarter and the year ahead, we have multiple levers to help us achieve our goals. Our focus on the $200 to $500 price band for handbags will continue to provide us with both AUR and unit growth in that sweet spot. And we have a fantastic core offering.
I use the acronym TNT, Tabby, New York family and Teri. And what's important about that core is it's there to address this incredibly large TAM that we have both in North America and globally. But what it also does, because we have such a strong core, we're able to animate off of that core. And I'm going to give you one quick example. 11 months ago, we introduced a bag called Chelsea. Chelsea quickly became one of our best-selling New York family bags at $325. In September, we introduced Chelsea 20, a new bag for $250. And then I'm going to give you a little sneak preview, but in March, we're introducing Chelsea 40, a larger bag at $525. And that's a great example of how we focus on our core, we animate the core, and we provide such incredible value in the sweet spot. 
And of course, you're going to see us continue to have productivity gains from other categories like footwear and like men's, which will help boost our growth in the quarter and the years ahead. And all of this is fueled by our compelling marketing that maintains the relevancy of our brand for our Gen Z and young consumers.
So I remain hyper-focused on execution, and we're always balancing our short-term commitments, which we meet with being exceptional brand stewards for this 85-year-old incredible legacy brand.

**Operator** (Operator):
We'll move on now to Matthew Boss with JPMorgan.

**Matthew Boss** (Analysts):
Congrats on a nice quarter. Joanne, so on the durable compounding growth that you're seeing globally at the Coach brand and the multiyear stacked revenue growth in the first quarter that you talked about accelerating across all regions, I guess what are you seeing in the customer file if you looked at the U.S. versus China? 
And, then Scott, relative to the 130 basis points of operational gross margin expansion in the first quarter, how should we think about the evolution of the drivers that you're embedding over the course of the remainder of the year?

**Joanne Crevoiserat** (Executives):
Well, thanks, Matt. Taking the first part of your question in terms of regional differences and what's driving our compounding growth, there's more similarities than differences, and it really starts with the value proposition we're delivering. And Todd touched on the innovation that we're delivering in the market. And we're delivering style and quality at compelling price points. When I say our value proposition has never been stronger, that is a place that we play that gives us access to a broad range of consumers. And so that is, I think, at the core of our growth strategy.
And our growth strategy is to welcome more new consumers, it's driving customer acquisition around the world. Our brand values, our brand quality, the styling and innovation we're delivering are resonating with our target Gen Z consumer globally. We're building capabilities regionally to make sure that we execute with an understanding of the local customer and translating the core values of the brand appropriately and effectively for consumers in each market, and we've been very, very focused on making sure we have those capabilities globally.
And so the value proposition gives us that access to this really massive TAM. The customer acquisition opportunity is clear, and we continue to build growth -- drive growth through this customer acquisition, and that's the durability of our strategies and you're seeing it around the world. 
But I'll toss it maybe to Scott on gross margin levers.

**Scott Roe** (Executives):
Yes. I think first, Todd had a brief add on Coach, and then I'll come back to gross margin.

**Todd Kahn** (Executives):
Thanks, Scott. Just very quickly, building on everything Joanne said, remember, 2.1 million new customers, 40% of them were Gen Z in the last quarter, and we saw that across all markets. And I'm going to take a small victory lap here. Every major market grew, inclusive of Japan, where that was a great example of how our strategy came into fruition. We worked hard the last 1.5 years or so to reset that market and to focus on acquisition, focus on the younger consumer and create relevant marketing for that consumer, and it worked. And that's what gives us confidence that we can continue to replicate this strategy over and over again across the world. And when we win with Gen Z, Joanne said it, you've heard me say, we tend to win with every other cohort as well, but we have to stay focused on delivering that value to them. 
Sorry, Scott. Go give them the good...

**Scott Roe** (Executives):
Yes. You know I love gross margin, Todd. So I really appreciate the call out on the strong gross margin operational performance and what we see for the balance of the year. Just to ground everybody, remember, we did take up our full year gross margin and operating margin guidance. And I would say that was really led by strength in the Coach brand. We see that really across all the regions. Those drivers are still in place. You saw them in evidence in Q1, and what we see in Q1 and our early looks at Q2 give us a lot of confidence in the guide that we gave for the balance of the year. 
So what are those drivers? AUR, Todd and Joanne just talked about a reinvestment back in the brand, bringing innovation, bringing things that are resonating against that price-value relationship that we protect so dearly. That gives us the ability to price. We've talked about inflation plus a little bit, and we still have a lot of confidence in that on a go-forward basis.
Also, don't forget about AUC. Really, we've seen modest inflation pressures this year. We talked about that last quarter. We do see a little fuel-related surcharges. Honestly, they're not significant to the overall -- to our overall cost base, and what we see is reflected for the balance of the year and our current guide, but we also have the best supply chain in the business, in my opinion. And we are able to find efficiency across our network in terms of mitigating some of those costs. And finally, we're growing faster outside of the U.S. than we are inside, and we have better margins outside of the U.S. So that's a structural mix benefit that we see. So whether it's this year's guidance or beyond, we have a lot of confidence in our ability to continue to grow those gross margins.

**Matthew Boss** (Analysts):
Congrats. Best of luck.

**Operator** (Operator):
We'll move on now to Bob Drbul with BTIG.

**Robert Drbul** (Analysts):
I guess I was wondering if you could spend some more time on just the performance in China, what you're seeing with that level of growth in the consumer environment over there?
And, Todd, if you could just also give us more insight into like where the footwear business is and the sustainability at the Coach brand in footwear would be helpful.

**Joanne Crevoiserat** (Executives):
So, maybe I'll start and kick it off, Bob. On our progress in China, in the first quarter, our growth remains strong. And as we just said, new customer acquisition is driving that growth. And we are growing well above market. And it does speak to the values of the brand, but the value proposition in the market as well as our strong regional execution. We've had teams on the ground for decades, and we continue to invest in capabilities in the market. And there's a lot going on in the world in every market, and our work starts with understanding the consumer and the landscape and really understanding what resonates with our target consumers and what they value. And while we do that, we also invest in our future growth and marketing and experiences that they value as well as bringing great product into the market. 
And in China, overall, we continue to see a tremendous opportunity. We have low -- relatively low penetration in the market, and it is a large TAM, again, at our value proposition. And with this focus on the Gen Z consumer, we're winning today, and we have the capacity and capabilities to continue to drive growth for the long term. For the second quarter and for the year, we've modeled mid-teens growth even as we lap more difficult compares. So there's no change in our long-term expectations in China. We continue to believe it represents significant long-term opportunity. And we just came back from the region, super optimistic about what's happening on the ground. 
Maybe I'll invite Todd to share some comments about our recent store manager conference and the work we've done in China.

**Todd Kahn** (Executives):
Yes. Thanks, Joanne. We couldn't be more excited about China. As Joanne mentioned, Joanne, Scott, many of us were in China, we had a store manager conference in Macau. So it was a regional conference brought all of our APAC managers together. It was over 1,100 people because we had the opportunity to bring both Kate and Coach in the same venue. And the enthusiasm for our brands, the value and what we're doing at scale is so incredible, and we're seeing it on the ground. 
We said to you, Bob, at our Investor Day, 70% of our growth was going to come from international. Well, the good news is we're seeing growth domestically, but we're seeing that growth internationally as well. You're going to see us build more new stores. 2027 is a great year for us building stores at Coach. You're seeing us grow materially across all markets. But China, there's just so much untapped potential in China, both in areas that we're not or doubling down in areas that we are. And again, our brand positioning of expressive luxury gives us much more runway than perhaps traditional European luxury because we can go where young people are going and the value proposition is so clear.
So we feel extraordinarily excited by China. We could talk about how our co-creation in China and our Dongguan facility has inspired. Actually, Stuart, but now our Creative Director for Kate has seen the magic that can take place there. So that's where we leverage some of our capabilities. 
On footwear, footwear contributed about 6% of our growth. I mean, we're still walking. We haven't run yet. There is so much opportunity. And footwear is one of those examples where our One Coach strategy comes into being. We launched our Soho sneaker at one price across all channels, and that's resonating. What's interesting about Soho, it's a great acquisition vehicle for our young men. They may -- their first purchase at Coach is often a Soho and then eventually, we get them into leather goods. So we love that. 
Margot is an outstanding casual shoe in women's. And what we like about footwear, obviously, I love additional UPTs at any of our direct businesses, we love that. But in addition, it's a great beachhead for wholesale accounts in markets that maybe we were underpenetrated like Europe. So you see us drive a lot of wholesale business through that category in a very profitable way. So we love the frequency of purchase of footwear. We love the additional UPT, and we love that. It's expanding us across all genders.

**Operator** (Operator):
We'll move on now to Laurent Vasilescu with BNP Paribas.

**Laurent Vasilescu** (Analysts):
I think in the prepared remarks, it was called out that the expressive luxury concept stores will touch about 80% of your traffic by 2030, which I found very interesting as a data point or target. Maybe if you could, for the audience, can you share how much of these new concepts are touching the current fleet, and how do we think about that rolling up to 80% as we think about from a CapEx and a return on invested capital perspective?

**Todd Kahn** (Executives):
We are really pleased with what we're seeing with expressive luxury and the store design. I think we mentioned last year in the first 6 months of last fiscal, we tested a couple of stores, and we paused because we really wanted to see how the consumer responded to it. And that allowed us to go slow to smooth, smooth to fast. Now we're growing faster because we have the capabilities and understanding, and it's working. In every store so far, we're seeing a positive reaction. We're seeing positive reaction to dwell time. We're seeing positive reaction to how the consumer experiences our stores. We've taken many more elements of play and put them into expressive luxury. Our stores are engaging and not off-putting.
And what we're doing is, unlike times in the past, we're touching some of our biggest stores first, not necessarily whether they were a retail or whether they were traditionally an outlet store. Last week, we just launched and if you happen to be in L.A. area, Citadel, one of the most beautiful stores, if you close your eyes and walk in it, I challenge you to believe that you're in an outlet store because you're not, you're in a One Coach store. So it looks fantastic.
And I think I'll turn it over to Scott to let him talk to you about the CapEx elements since I hand them the check.

**Scott Roe** (Executives):
Yes. Yes. Well, I can assure you there's a close conversation between Todd, and me on CapEx. But -- so here's the great news. It's not that expensive, right? If you look at our total CapEx, $300 million, 3% to 4% of sales, very consistent with what we've talked about in our long-range plan. About 2/3 of that CapEx is related to -- specifically to doors or stores. We are opening stores predominantly outside of the U.S., a few in the U.S., but we're also doing the retrofit. So all of that is included in that roughly $200 million.
And as it relates to the returns, we -- first of all, we haven't touched a lot of these stores in some of them a decade or so, right? So this is ongoing built into our plans, and this is, call it, hygiene. That said, it's early days, but we do expect that we'll see some improvement, not just from making them look better, as Todd talked about, but also we learned a lot over the years how to lay out a store more effectively, what One Coach means and how we get the most out of that, some of the new categories and the applications there. So there's multifacets benefits to the retrofits that we're looking at.

**Operator** (Operator):
We'll move on now to Michael Binetti with Evercore.

**Michael Binetti** (Analysts):
Great quarter. Let me add my congrats up and down the line, really nice to see. I think, Joanne, on the holiday, you said industry forecast for North America to be a mid-single-digit growth. You expect mid-single-digit growth. Are you seeing the industry trending at that rate as we head into the holiday and maybe where you see any opportunities that you're most excited about for the brand to gain share outperform?
And then I just want -- I guess, on maybe a jump ball, I think North America promotions were lower in first quarter than they were in the first quarter a year ago. If I'm right on that, maybe still a very healthy full price growth, it looks like. And as you look at 2Q, does the plan also include lower promotions? Or just what's baked into your assumptions for the quarter?

**Joanne Crevoiserat** (Executives):
Thanks, Michael. We're just getting started on holiday. So I think our consumer research shows that only 25% of consumers will have started their shopping by Black Friday. So I fall into that category. So I'm pleased to hear that. But we're just getting started. We feel great. We have momentum in North America and in the U.S., as we talked about, the first quarter beat came from the North America market. And we took up our expectations for the year based on our confidence in the North America market. And I think the backdrop in the forecast is constructive overall. And in our research and in third-party research, we hear that more people are planning to spend more this holiday than a year ago.
And so there are a lot of data points that support constructive backdrop for holiday. We continue to steward our brand. What you saw us deliver in the first quarter includes discipline on promotion. So North America is our largest market. And our focus in terms of being great stewards of our brand is making sure that we're managing the brand for durable long-term growth. And we see that opportunity in North America as well as outsized opportunities in international.
So as we're stewarding the brand, and I'll toss it to Todd in a second to talk about how the team is really being exceptional stewards of the brand and managing our growth in a very healthy way to protect the durability of growth over time. That's what we see sort of long term. That's our strategic approach. And our day-to-day management reflects that long-term strategy.
And maybe, Todd, I'll send it to you to talk about that.

**Todd Kahn** (Executives):
Thanks, Joanne. Yes, we've got a lot of learnings on this. And it really starts with the value of our offering as is. And what we have found over time is it becomes less significant to the call to action of around price is not the driver. In fact, Black Friday, some of our "doorbuster" opportunities, while they performed, they were the least engaging element of our selection. This year, we've taken that learning and what we said is, instead of necessarily screaming price, we're screaming limitations, meaning if there's a colorway you want, you're going to have to come and get it the first few days because it won't be there. So that rarity, that exception is going to be what's compelling. 
And what we're seeing across the fleet, and this goes back to our One Coach strategy. What people want is our best product. They want Tabby, they want Teri. They want the New York family. They want Brooklyn, and they want it in the colorways they want that are relevant for the season or the animation that we provided in those families. And our price points are still accessible. So we're going to lean in on that. We're going to lean in on the festivities. We're going to lean in on how compelling our assortment is. And you know what? Get a bag charm while you're at it, you personalize the offering. That's what's exciting for us. So yes, net-net, you should see us be even less promotional, staying focused on the $200 to $500 sweet spot for handbags.

**Operator** (Operator):
We'll move next to Aneesha Sherman with Bernstein.

**Aneesha Sherman** (Analysts):
Congratulations on the quarter. I actually wanted to jump off on that last point, Todd, that you made around the $200 to $500 sweet spot and your strategy to intentionally shrink the sub-$200 business and grow that sweet spot. So do you envision a continued upward move on price mix for Coach beyond the $500 price point as well? And can you talk about how that factors into the mid-single-digit North America growth? Is that the primary driver of the mid-single-digit North America growth? 
And then stepping back, you've talked about the broadening value gap versus the European luxury brands. Is there any risk that this value gap could narrow as some of those brands are now trying to win back aspirational customers by mixing lower on AUR to try to compress the value gap versus Coach?

**Todd Kahn** (Executives):
Sure. So let's be clear, $200 to $500 is our sweet spot that will remain our sweet spot. Occasionally, we have bags over $500. I walk around with an Empire bag. It's a compelling bag. It is over $500. Our growth is coming from this $200 to $500 sweet spot in handbags. And I want to be clear, we have bags under $200. We have SLGs under $200. We have a lot of price points to enter the brand, whether it's through footwear, whether it's through jewelry, fragrance that people, particularly a young person can come in and their first purchase at a Coach brand doesn't necessarily have to be Tabby or Teri, but we would like them to aspire to that. So we will continue to innovate with newness across the entire spectrum. So you'll still see us innovate under $200.
But one of the things we have found is, generally speaking, under $200 bags are the most promotional. So we tend to want to take it up just a little bit. We are clear on: we are not going to do maybe what some other people do is just because the brand is hot to start going materially above our sweet spot because we want to stay focused on point of market entry. And today, that's Gen Z, eventually that will be Gen Alpha.
In terms of the European luxury and other people, the delta is material. So the fact that we -- look, we welcome competition. We thrive on competition. We are not scared of competition. I think the white space is so materially different. And remember, what we're focused on. We're focused on customer acquisition to drive growth. We know if we acquire a customer, if their first bag purchase, if their first footwear purchase is compelling, we have them for life. So this will stay in our DNA. And we have so much room on that TAM. Again, not just internationally, but here in North America, there are millions of customers who today can afford and have yet to experience the wonderfulness of owning a Coach bag, we want to get them into our family.

**Operator** (Operator):
We'll move next to Dana Telsey with Telsey Group.

**Dana Telsey** (Analysts):
As you think about the Kate Spade brand, Joanne, how are you framing the progress there? How you're thinking of icons and adding to the collections? Is it moving as you would have expected? 
And then on the store growth, any difference in performance outlets versus full price? And how you think about the availability of newness in the outlets because it certainly seems like when I go there, you can sell through higher price points in the outlets also. Anything you're seeing there and how it differs by region?

**Joanne Crevoiserat** (Executives):
Thanks, Dana. The Kate Spade business was in line at a revenue level, in line with our expectations at expanding margins this quarter, and we are making choices to improve the quality of the business to set a stronger foundation. Remember, our strategy has been to streamline the business and solidify that foundation to position it to scale. And our focus, to your point, is building stronger brand desire to accelerate our turn, which includes driving more distinctiveness in the product and storytelling. I'm really pleased to hear that you're in our outlet stores, and you believe, like I do, that there's quality and pricing power in that product that we're delivering. 
Jonathan Saunders, our new Executive Creative Director, has hit the ground running and is working on sharpening that creative execution behind Kate Spade. He has an incredible sense of the brand DNA, and we're modernizing that for today's consumers. So I'm excited about the future of Kate Spade. Both in terms of the product, but also the storytelling and the investments that we're making, and we'll continue to execute against our plan.

**Operator** (Operator):
We'll move next to Mark Altschwager with Baird.

**Mark Altschwager** (Analysts):
Just first, on Kate Spade, can you help us think through the cadence of the turnaround from here? What needs to happen in product and customer engagement before the improvements can translate to the top line? 
And then, Scott, SG&A, I believe the outlook for the second quarter and full year implies more leverage in the back half. Can you just talk us through the drivers there? How much of that is in marketing versus other expenses?

**Joanne Crevoiserat** (Executives):
Mark, on Kate, I sort of touched on the phases of our strategy, streamlining the business, closing unproductive stores, stepping away from promotional activity, and we see that having a headwind on the top line. We're managing the phases of the strategy in a very disciplined way, as I said in the first quarter, revenue met our expectations, and we're expanding gross margin. So that's a really important foundation.
As we move through the year, and I had an opportunity to be in Dongguan and see some of the early work that Jonathan and teams are doing as we sharpen that creative execution, we do expect progress as we move into the back half of the year and as we move forward. And I neglected to mention, on Aneesha's question earlier on stores, we are also investing. So we're investing in marketing and we're investing in remodels and effectively driving improvement in our store fleet, more engagement with consumers, a better experience, and we're seeing that translate.
What we need to see is higher customer acquisitions to drive long-term growth. And we're building our handbag assortment with that in mind. We're seeing early signs and green shoots with handbags driving 500,000 new customers in the quarter. They're coming in at higher AUR. We're expanding margins. So some of those early green shoots we're monitoring, and we expect to make progress as we move forward.

**Scott Roe** (Executives):
Yes, Mark, and I'll take your SG&A question. So let me just point you to the full year guide. So 100 basis points of operating margin expansion, that includes about 20 basis points of SG&A. That's pretty consistent with where we were in our initial guide for the year. And what's underneath the covers on that is more of the same, right? We've got marketing investments, about 12% of sales. That's an increase from the prior year and, like, 4x from where we were if we go back 5 years ago or so. And we believe that's a big part of the customer acquisition engine that we have. And we have every intent to maintain our investment in brand, and that's one of the things that gives us confidence in future growth. But underneath that is a lot of leverage across the rest of the P&L, I would say a testament to the operational discipline. 
The other thing, I can't talk about guidance without talking about cash, too. So it's top line growth led by Coach North America direct in Q1 and based on the balance of the year, mostly in Q2 based on what we see; it's gross margin expansion for all the reasons I talked about earlier. There's discipline in the P&L. We're reinvesting back into the business. And I'll just remind you, we upped our buyback by $350 million to a total return to shareholders of $2 billion. That includes dividends and repurchases. 
So I mentioned that to say our ability to keep investing and our confidence to return cash hopefully gives you some indication of not only the strength of the business, but our conviction that we have a long-term durable growth model here and a lot of confidence in the future.

**Mark Altschwager** (Analysts):
That's great. Congrats on the momentum.

**Operator** (Operator):
Thank you. That concludes our Q&A. I will now turn it over to Joanne Crevoiserat for some concluding remarks.

**Joanne Crevoiserat** (Executives):
Everyone, thanks for joining us. To recap, our first quarter results are a testament to the way we're stewarding our brands with discipline and the exceptional execution of our team whom I want to recognize and thank. I'm confident in what we've built. I'm excited about where we're headed, and I appreciate your continued interest in our story. Thank you.

**Operator** (Operator):
This concludes Tapestry's earnings conference call. We thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TPR_Q4_2026_Earnings_Call_20260813.md
- 2026-08-13｜CFO｜guidance：FY27 營收財測 84–85 億美元，中個位數成長（原話："$8.4 billion to $8.5 billion"）
- 2026-08-13｜CFO｜guidance：FY27 EPS 財測 7.80–7.90 美元（原話："we expect EPS of $7.80 to $7.90"）
- 2026-08-13｜CFO｜guidance：FY27 營業利益率預期擴張 50bp 至近 24%（原話："operating margin expansion of 50 basis points to nearly 24%"）
- 2026-08-13｜CFO｜guidance：FY27 北美營收預期低個位數成長（原話："In North America, we expect revenue to increase low single digits"）
- 2026-08-13｜CFO｜guidance：FY27 歐洲與大中華預期中十位數成長（原話："we expect growth of mid-teens"）
- 2026-08-13｜CFO｜guidance：FY27 Kate Spade 營收預期高個位數衰退（原話："a high single-digit decline at Kate Spade"）
- 2026-08-13｜CFO｜guidance：FY27 Kate Spade 預期小額營業虧損（原話："expect a modest operating loss"）
- 2026-08-13｜CFO｜guidance：Q1 EPS 財測約 1.55 美元（原話："Q1 EPS is forecasted to be approximately $1.55"）
- 2026-08-13｜CFO｜guidance：Q1 Coach 兩年疊加成長中 30% 出頭（原話："mid-30s growth on a 2-year stack basis"）
- 2026-08-13｜CFO｜guidance：全年上半年與下半年營收節奏：上半年高個位數（原話："grow high single digits in the first half of the year"）
- 2026-08-13｜CFO｜guidance：FY27 自由現金流預期接近 17 億美元（原話："we anticipate adjusted free cash flow to approach $1.7 billion"）
- 2026-08-13｜CFO｜guidance：FY27 資本支出（含雲端運算成本）約 3 億美元（原話："to be in the area of $300 million or 3% to 4% of revenue"）
- 2026-08-13｜CFO｜guidance：FY27 Coach 淨增 40–50 家門市（原話："between 40 and 50 doors is our expectation on a net basis at Coach"）
- 2026-08-13｜CFO｜margin：FY27 毛利率預期增加約 30bp（營益率拆解：毛利率加 SG&A 槓桿）（原話："gross margin to increase by approximately 30 basis points"）
- 2026-08-13｜CFO｜margin：財測假設美國進口關稅率落在 20% 中段（原話："a mid-20s percent tariff rate on U.S. imports"）
- 2026-08-13｜CFO｜margin：關稅對損益的影響上半年為小幅助益，下半年轉為逆風，獲利逐季不均（原話："tariffs providing a modest benefit in the first half of the year"）
- 2026-08-13｜CFO｜margin：Q4 毛利率拆解：含出售 Stuart Weitzman 的 60bp 有利影響（原話："a favorable 60 basis point impact"）
- 2026-08-13｜CFO｜margin：Q4 關稅與關務成本逆風約 60bp（原話："a tariff and duty headwind of approximately 60 basis"）
- 2026-08-13｜CFO｜margin：Q4 行銷費用占營收 14%，年增 130bp（原話："a 130 basis point increase in marketing, which represented 14% of sales"）
- 2026-08-13｜CFO｜margin：Q4 EPS 受稅率偏高拖累逾 0.05 美元（原話："a higher tax rate versus plan due to a number of discrete items"）
- 2026-08-13｜CFO｜margin：Q1 營益率持平，SG&A 增加全數來自行銷（原話："higher SG&A due entirely to continued increases in marketing"）
- 2026-08-13｜CFO｜margin：回答毛利率橋時說全年逐季將不平順（原話："it's going to be a little lumpy through the year"）
- 2026-08-13｜CFO｜margin：稱毛利率財測屬審慎（原話："we think the guidance we've given is prudent"）
- 2026-08-13｜CFO｜margin：Q4 行銷槓桿比原先指引多一些，管理層稱有時點因素（原話："we came in with a little more leverage in marketing"）
- 2026-08-13｜CFO｜margin：行銷（需求創造）約占營收 12%、約 10 億美元（原話："It's about $1 billion in advertising"）
- 2026-08-13｜CFO｜commitment：FY27 財測沿用投資人日的長期財務框架（原話："low double-digit EPS growth, consistent with our long-term commitments"）
- 2026-08-13｜CFO｜commitment：FY27 預計回饋股東 17 億美元，含 13.5 億美元回購（原話："we expect to repurchase approximately $1.35 billion of shares"）
- 2026-08-13｜CFO｜commitment：董事會核准股利提高 16%（原話："Our Board approved a 16% increase in the dividend"）
- 2026-08-13｜CEO｜commitment：中期目標：Coach 展店計畫改造 2030 財年前約 80% 客流量（原話："concept to impact approximately 80% of our traffic by fiscal year '30"）
- 2026-08-13｜CEO｜commitment：管理層重申 Coach 邁向 100 億美元品牌（原話："a clear path to Coach becoming a $10 billion brand"）
- 2026-08-13｜CFO｜capital_allocation：併購前提：Coach 維持強勁、Kate Spade 回到可持續成長（原話："we will ensure Coach remains strong"）
- 2026-08-13｜CFO｜capital_allocation：長期總槓桿目標低於 2.5 倍（原話："long-term gross leverage target of below 2.5x"）
- 2026-08-13｜CFO｜guidance：全年財測不需要 Coach 其餘季度維持 Q1 同等成長（管理層稱審慎）（原話："full year guide doesn't require us to keep that same level"）
- 2026-08-13｜CFO｜product：財測假設單價（AUR）與件數都成長（原話："our guidance assumes both unit and AUR growth"）
- 2026-08-13｜Coach CEO｜product：Q4 Coach 件數持平是刻意減少促銷天數（原話："We had fewer promotion days in the fourth quarter"）
- 2026-08-13｜Coach CEO｜product：Coach 鎖定 200–500 美元價位帶（原話："We are going to be very focused on that $200 to $500 space"）
- 2026-08-13｜Coach CEO｜product：Coach 全球成長下限由中個位數調升到高個位數（原話："floor up from mid-single digits to high single digits"）
- 2026-08-13｜CEO｜product：Kate Spade 營收進展比計畫緩慢（原話："Although top line progress was more gradual than we planned"）
- 2026-08-13｜CEO｜risk：Kate Spade 品牌知名度（未輔助）尚未改善（原話："awareness more broadly has not yet improved"）
- 2026-08-13｜CEO｜customer：FY26 新客 1,100 萬人，Z 世代為主（原話："welcomed 11 million new customers to our brands, led by Gen Z"）
- 2026-08-13｜CEO｜customer：新客留存率位居客戶檔案中最高之列（原話："retention rates among the highest retention rates in our customer file"）
- 2026-08-13｜Coach CEO｜customer：中國過去行銷投入不足，現在將行銷拉到與整體一致（原話："we underinvested in China over the years"）
- 2026-08-13｜CFO｜guidance：FY27 日本預期回到成長（原話："In Japan, we're forecasting a return to growth"）
- 2026-08-13｜Coach CEO｜competition：Coach CEO 稱產業沒有進入門檻（原話："there are no barriers of entry in our space"）
- 2026-08-13｜CFO｜competition：CFO 稱雖無進入門檻，但規模門檻正在提高（原話："there are barriers to scale, and those barriers are getting higher"）

### 問答異常語氣（迴避／改口／保留）
- TPR_Q4_2026_Earnings_Call_20260813.md｜問：Boruchow：Q4 北美 Coach 成長受促銷時點移轉影響多少？Q1 低十位數 Coach 全球財測對應多少北美成長？｜答法：Coach CEO 與 CFO 未直接給出時點移轉的影響幅度，也未給 Q1 北美數字；改以兩年疊加約 30% 與「comping the comp」回應
- TPR_Q4_2026_Earnings_Call_20260813.md｜問：Binetti：毛利率橋顯示 Q1 後幾乎沒有擴張，能否說明全年路徑｜答法：CFO 未給逐季毛利率數字，只說「lumpy」、全年約 +30bp、結構性驅動因素不變，並稱財測審慎
- TPR_Q4_2026_Earnings_Call_20260813.md｜問：Yih-Tennant：Coach 北美中個位數成長，是指 Q1 還是全年？｜答法：CFO 與 Coach CEO 先後澄清；CFO 講北美 Coach 中個位數（Q1 與全年），Coach CEO 再補述 Q1 Coach 整體低十位數、全年高個位數；先前 CFO 在回答 Binetti 時亦用相同說法，此處為分析師反覆追問確認
- TPR_Q4_2026_Earnings_Call_20260813.md｜問：Yih-Tennant：你們最擔心哪個競爭對手？｜答法：Coach CEO 未點名任何競爭對手，改談「沒有進入門檻」、護城河、85 年品牌與文化穩定

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
{"date":"20261005","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼條件：Q1 FY27 法說（約 2026-11）Coach 固定匯率成長 ≥ +10% 且手袋件數年增 ≥ 0，兩者同時成立","irr_base_pct":7.9,"ev5y_pct":35.6,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.3,"ev5y_pct":35.6,"irr_base_pct":7.9,"max_dd_pct":-55,"bull_5y_price":241.2,"bear_5y_price":74.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"加碼條件：Q1 FY27 法說（約 2026-11）Coach 固定匯率成長 ≥ +10% 且手袋件數年增 ≥ 0，兩者同時成立","price_at_dd":118.12,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
