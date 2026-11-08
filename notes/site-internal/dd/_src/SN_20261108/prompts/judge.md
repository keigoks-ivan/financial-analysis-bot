你是 stock-analyst **v20 判斷 agent**，標的 SN（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SN","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SN_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SN_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_net_sales_gaap","label":"Net sales (GAAP)","value":1976.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results"},"note":"未驗證（僅第三方稱 adj EPS $2.34 vs consensus $1.87，新聞稿無此數）"},{"id":"f_kpi1_adjusted_non_gaap_operat","label":"Adjusted (Non-GAAP) operating income / margin","value":21.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"% margin（$425.5m，YoY +47.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results"}},{"id":"f_kpi2_gaap_operating_income_ma","label":"GAAP operating income / margin","value":22.4,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"% margin（$442.9m，YoY +68.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results；含 $109.6m IEEPA 關稅退款（不計入 adjusted）"}},{"id":"f_kpi3_gross_margin_gaap_adjust","label":"Gross margin GAAP / Adjusted","value":59.2,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"% GAAP（Adjusted 55.9%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results"}},{"id":"f_kpi5_share_based_compensation","label":"Share-based compensation","value":42.0,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m（占 GAAP 營業利益 9.5%、占營收 2.1%，由兩數換算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results"}},{"id":"f_kpi6_adjusted_diluted_eps","label":"Adjusted diluted EPS","value":2.34,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results（GAAP diluted EPS $2.39）"}},{"id":"f_kpi7_guidance_fy2026","label":"Guidance FY2026（上修）","value":"net sales +18.0%~19.0%（前次 16~17%）；adj EPS $6.65~6.75（前次 $6.45~6.55）；adj EBITDA $1,380~1,391m（前次 $1,357~1,369m）","period":"Q3 FY2026（公告於 2026-11-04）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results；稅率約 22~23%、稀釋股數約 142.0m、capex $190~210m；新聞稿無單獨 Q4 指引"},"note":"FY1 共識 EPS $6.59（dd_numbers_extra.py consensus_revision，財報前快照）；指引中位 $6.70 高於該值"},{"id":"f_kpi8_net_sales_by_category_cl","label":"Net sales by category（Cleaning / Cooking&Beverage / Food Prep / Beauty&Home Env）","value":"617.2 (+4.1%) / 597.7 (+36.6%) / 485.5 (+18.3%) / 276.1 (+45.8%)","period":"Q3 FY2026（公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 FY2026（公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results；Domestic $1,313.7m +19.4%、International $662.7m +25.2%"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_sn_gross_margin_pct","label":"SN 毛利率","value":51.45,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_sn_operating_margin_pct","label":"SN 營業利益率","value":15.58,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_sn_fcf_margin_pct","label":"SN FCF 利潤率","value":6.8,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_whr_gross_margin_pct","label":"WHR 毛利率","value":13.08,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WHR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_whr_operating_margin_pct","label":"WHR 營業利益率","value":2.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WHR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_whr_fcf_margin_pct","label":"WHR FCF 利潤率","value":-1.71,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WHR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hele_gross_margin_pct","label":"HELE 毛利率","value":47.37,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HELE.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hele_operating_margin_pct","label":"HELE 營業利益率","value":9.4,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HELE.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hele_fcf_margin_pct","label":"HELE FCF 利潤率","value":8.06,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HELE.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nwl_gross_margin_pct","label":"NWL 毛利率","value":35.58,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NWL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nwl_operating_margin_pct","label":"NWL 營業利益率","value":8.38,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NWL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nwl_fcf_margin_pct","label":"NWL FCF 利潤率","value":0.72,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NWL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_free_cash_flow_fcf","label":"Free cash flow（僅有前九個月，新聞稿未列單季與 FCF 定義）","value":-17.2,"period":"YTD 9M FY2026（至 2026-09-30，公告於 2026-11-04）","unit":"USD m（九個月：營業現金流 $107.4m − 資本支出 $124.6m，本欄為自行換算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"YTD 9M FY2026（至 2026-09-30，公告於 2026-11-04）","citation":"公司 IR 新聞稿 Q3 2026 Results 現金流量表"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":222.95,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":99.65,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":74.63,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.59 → 6.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.67 → 7.67）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.76 → 8.76）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":6.59,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":7.67,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":8.76,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 6.59 → 6.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":37.41,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝86.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":86.5,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":4.33,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":4.39,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":33.83,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 6.59，分子＝快照價 222.95","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.0,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"},"note":"近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）"},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":424.84,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 912.66、現金 487.82（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":140.91,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":31841.06,"period":"2026-11-08","unit":"USD m","basis":"市值 31416.22 ＋ 淨負債 424.84","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":7641.24,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":8720.29,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":4.17,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 222.95 / W52 137.88 / W104 118.7 / W250 None / W250 13週斜率 None%"},{"id":"f_ma_w52","label":"52 週均線","value":137.88,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":118.7,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"10-K稱公司已在各地區取得市佔，從價位高於與低於自家的對手手中拿走份額；Shark為美國floorcare第一品牌，Ninja為美國最暢銷小型廚房家電（Circana，截至2026-01-03）。為公司自述。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"We have successfully gained market share across geographies, taking share from competitors priced both above and below our offerings.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K列出主要對手：Shark對Dyson、Hoover、Bissell；Ninja對Vitamix、De'Longhi、Breville、Hamilton Beach、Cuisinart；Dyson亦在Beauty類別；無單一對手橫跨所有類別。","source":"SEC EDGAR 10-K FY2025 Item 1 Competition","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"Shark competes with brands including Dyson, Hoover and Bissell.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K風險因子：部分對手可能降價並接受較低利潤，公司可能流失市佔。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"Some competitors may be willing to reduce prices and accept lower profit margins to compete with us. As a result of this competition, we could lose market share and sales or be forced to reduce our prices to meet competition.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q1 2026 新聞稿：淨銷售+15.6%、各品類市場疲弱下仍取得份額（公司自述）","source":"SharkNinja Q1 2026 results newsroom","url":"https://newsroom.sharkninja.com/sharkninja-reports-first-quarter-2026-results/","excerpt":"Barrocas, Chief Executive Officer, commented, “SharkNinja’s momentum has continued into 2026, with Q1 results delivering 15.6% net sales growth that reflects both strength and steadiness in execution. Our three-pillar growth strategy continues to drive substantial market share gains across our expanding portfolio, as we innovate in new categories, capture share in existing segments, and","as_of":"2026-05-06","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"SharkNinja 10-K FY2025: customers are retailers; largest customer 23.8% of net sales; Amazon, Costco, Walmart each >10% (combined 45.7%); no retail exclusivity. 搜尋未發現客戶導入第二供應商或自製的來源。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"We have low retailer concentration, with our largest customer representing 23.8% of net sales for the year ended December 31, 2025.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 最大客戶占淨銷售 23.8%；Amazon、Costco、Walmart 各逾 10%，合計 45.7%","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"We have low retailer concentration, with our largest customer representing 23.8% of net sales for the year ended December 31, 2025.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"客戶 A 占營收 23.8%（2024 23.1%、2023 19.9%）、B 11.4%、C 10.5%；客戶 A 占應收帳款 22.0%（2024 為 29.1%）","source":"SEC EDGAR 10-K FY2025 財報附註","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"Customer A 23.8 % 23.1 % 19.9 % Customer B 11.4 10.0 10.0 Customer C 10.5 12.8 14.8","as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未見 Walmart 信用降級；其 FY2026 10-K 列 S&P AA、Moody's Aa2、Fitch AA（Amazon、Costco 未查得一手評等）","source":"Walmart 10-K FY2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm","excerpt":null,"as_of":"2026-01-31","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Allianz Trade 預期無房屋換手回升則 2026–2027 家電銷量無復甦；中國補貼提前拉貨留下餘波；高端區塊比量販區塊撐得住；美國僅約四分之一家電為本土生產；記憶體晶片短缺推高 BOM。","source":"Allianz Trade, household equipment sector report","url":"https://www.allianz-trade.com/en_global/economic-research/sector-reports/household-equipment.html","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"美國家電產業擴產中：Whirlpool 宣布投資 3 億美元擴 Ohio 洗烘衣機產能；GE Appliances 在 Louisville 擴洗衣廠 4.9 億美元（CRU 分析）。","source":"Bloomberg 2025-10-15 Whirlpool to invest $300 million; CRU via Steel Market Update","url":"https://www.bloomberg.com/news/articles/2025-10-15/whirlpool-to-invest-300-million-to-make-more-appliances-in-us","excerpt":null,"as_of":"2025-10-15","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SharkNinja Q2 2026 上調全年銷售成長至 16–17%（原 11.5–12.5%），烹飪與飲品銷售 +36.5%、國際 +36.6%；管理層稱既有品類近三年約中高個位數成長；部分上調含關稅退款效益；2025 年底庫存 +11% 至 10 億美元。","source":"SharkNinja Q2 2026 results / pulse2 / Zacks","url":"https://pulse2.com/sharkninja-cooking-and-beverage-sales-jump-36-5-as-company-raises-2026-sales-growth-outlook-to-16-17/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"德國 GfU 預期主要家電在歐洲以換機需求為主，2025 年底至 2027 年底營收約 +2.6%；供應商報告核心家電市場 2027–2028 低至中個位數成長，智慧家電成長較快（供應商估計，彼此數字差異大）。","source":"GfU major domestic appliances forecast; Lucintel/Valuates via search summary","url":"https://gfu.de/en/?p=4434","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K 風險因素稱公司過去及未來可能面臨涉及競爭與反壟斷等事項的訴訟或政府調查，屬一般性風險揭露，未指明具體反壟斷調查；2026 年搜尋未見 FTC/DOJ/EU 對 SharkNinja 的反壟斷調查或拆分報導。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"From time to time, we have been, and may continue to be, subject to claims, lawsuits, including class actions, government investigations and other proceedings involving products liability, competition and antitrust, intellectual property, privacy, consumer protection, securities, tax, labor and employment, commercial disputes and other matters that could adversely affect our business, financial condition and results of operations.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 稱美國貿易政策變動（進口關稅）已對公司造成並預期持續造成重大不利影響；大部分產品在中國、越南等美國以外地區製造；2026-02-20 最高法院裁定推翻部分 IEEPA 關稅，政府宣布以其他法律徵收新關稅","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"Significant changes to U.S. trade policies that restrict imports or increase import tariffs and the responses of other countries have had, and we will expect will continue to have, a material adverse effect on our business.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K：大部分產品在中國、越南等美國以外地區製造，美國政策使取得海外製品更困難或更昂貴，已影響並可能持續影響銷售與獲利","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"A significant proportion of our products are manufactured in China, Vietnam and other regions outside of the United States. Accordingly, such U.S. policy changes have made it, and may continue to make it, difficult or more expensive for us to obtain certain products manufactured outside the United States, which have affected and could continue to affect our net sales and profitability.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K：公司認為產品不受近期出口管制措施直接影響，但不排除對貨源取得有間接負面影響；亦提及供應商可能被列入 BIS Entity List 的風險","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"We do not believe our products are directly impacted by these recent measures, but we cannot rule out the possibility that these measures could have an indirect negative impact on our business and our ability to source certain products from key jurisdictions.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Q3 2026 指引假設中國、越南、泰國關稅 12.5%，印尼、馬來西亞、柬埔寨 10%；IEEPA 退稅申請約 $247.1M 獲 CBP 接受，預計列為銷貨成本減項","source":"SharkNinja 8-K Exhibit 99.1 Q3 2026 press release","url":"https://www.sec.gov/Archives/edgar/data/0001957132/000195713226000055/exhibit991pressreleaseofsh.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"CEO 稱公司對多數 SKU 採中國內外雙供應來源，所有主力 SKU 皆有多於一家工廠，可在工廠與區域間轉單；美國銷量約 90% 在 2025 年 Q2 底前移出中國，其後移往柬埔寨、印尼、馬來西亞、泰國、越南（公司自述，未獨立驗證）","source":"Supply Chain Dive, SharkNinja leverages production flexibility to mitigate tariffs","url":"https://www.supplychaindive.com/news/sharkninja-leverages-production-flexibility-to-mitigate-tariffs/821264/","excerpt":"we sources all of its top SKUs from more than one factory","as_of":"2026-05-07","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"CFO 稱關稅為 2026 Q1 的 sizable headwind；展望假設中國、越南等數個東南亞國家基準關稅 10%","source":"Supply Chain Dive, SharkNinja leverages production flexibility to mitigate tariffs","url":"https://www.supplychaindive.com/news/sharkninja-leverages-production-flexibility-to-mitigate-tariffs/821264/","excerpt":"sizable headwind","as_of":"2026-05-07","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2025 10-K 揭露重要比例產品在中國、越南及其他非美地區製造，美國政策變動影響淨銷售與獲利，他國報復性關稅可能影響出口","source":"SharkNinja FY2025 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"Retaliatory tariff and trade measures imposed by other countries could affect our ability to export products","as_of":"2026-02-27","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 淨銷售 $1,976.4M、年增 21.2%；10-Q 分類：Cooking & Beverage +36.6%（$597.7M）、Beauty & Home Environment +45.8%（$276.1M）、Food Preparation +18.3%（$485.5M）、Cleaning +4.1%（$617.2M）","source":"SharkNinja 10-Q 2026-09-30 / Q3 2026 press release（經搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001957132/000195713226000056/sharkninja-20260930.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 後全年 2026 淨銷售成長指引上調至 18%-19%（前為 16%-17%）；北美 +19.4%、國際 +25.2%","source":"247wallst: SharkNinja Q3 2026 Earnings Beat（經搜尋摘要）","url":"https://247wallst.com/cards/sharkninja-q3-2026-earnings-sn-01m6k7dyhj9x4g5k5faf8fzmqz","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Q3 認列 IEEPA 關稅退款 $109.6M 一次性利益；關稅為美國市場毛利率壓力來源。未找到具體市佔百分比。","source":"SharkNinja Q3 2026 results 搜尋摘要","url":"https://finviz.com/news/415273/sharkninja-reports-third-quarter-2026-results","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["valuation","thesis.R"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 分部營收成長","source":"SharkNinja Q3 2026 press release","url":"https://s202.q4cdn.com/977000893/files/doc_news/SharkNinja-Reports-Third-Quarter-2026-Results-2026.pdf","excerpt":"Net sales increased 21.2% to $1,976.4 million, compared to $1,630.2 million during the same period last year, on both a reported and constant currency basis. Cleaning Appliances net sales increased by $24.2 million, or 4.1%, to $617.2 million, compared to $592.9","as_of":"2026-11-05","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"SharkNinja 10-K 風險因子自陳技術變化加速（AI、機器人、感測器等），未能適應可能不利營運","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"The pace of technological change is increasing at an exponential rate. To remain competitive, we must invest in developing tools and processes to improve the speed at which we are able to develop competitive products","as_of":"2026-03-02","retrieved_at":"20261108","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"瑞士零售商資料顯示中國品牌 Dreame、Roborock 已幾乎接管機器人吸塵器品類，Dyson 傳統吸塵器份額下滑","source":"Digitec/Galaxus, Chinese vacuum cleaner brands are blowing away their global competition","url":"https://www.digitec.ch/en/page/chinese-vacuum-cleaner-brands-are-blowing-away-their-global-competition-41328","excerpt":"While Dyson still rules the roost, Chinese brands such as Dreame and Roborock have almost completely taken over the robot segment, leaving Western pioneers such as iRobot trailing behind.","as_of":"2026-01-01","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 說明 DTC 通路毛利通常高於賣給零售商與經銷商，通路組合會影響毛利率；通路以零售加 DTC 的全通路為主。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"Gross margin is generally impacted by changes in channel mix since our DTC sales usually generate a higher gross margin than sales to retailers and distributors.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 顯示 Amazon、Costco、Walmart 各超過 10%，合計占淨銷售 45.7%，最大客戶 23.8%。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000015/sharkninja-20251231.htm","excerpt":"Our largest retailers include Amazon, Costco and Walmart, each of which accounted for more than 10% of our net sales, and together made up 45.7% of our net sales for the year ended December 31, 2025.","as_of":"2026-03-02","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2026 Q2 財報電話會議摘要：Italy、Spain 由經銷商轉直營，並完成主要國際市場 DTC 平台推出；管理層預期 DTC 與聯盟通路成長快於整體至 2027；擴張 TikTok Shop。","source":"Nasdaq／MarketBeat，SharkNinja Q2 Earnings Call Highlights","url":"https://www.nasdaq.com/articles/sharkninja-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-08-09","retrieved_at":"20261108","affects":["moat_trend","valuation","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026 call：Italy、Spain 轉直營；DTC 與聯盟通路預期成長快於整體至 2027。","source":"MarketBeat Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/sharkninja-q2-earnings-call-highlights-2026-08-09/","excerpt":null,"as_of":"2026-08-09","retrieved_at":"20261108","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08-05 Q2 後公司把 FY2026 指引上調至 EPS $6.45–6.55、營收 $7.4–7.5B，高於當時 Street 的 EPS $6.07、營收 $7.2B；上調前指引為 EPS $6.00–6.10。","source":"MarketBeat: SharkNinja issues FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/sharkninja-nysesn-issues-fy-2026-earnings-guidance-2026-08-05/","excerpt":"SharkNinja issued FY 2026 guidance for EPS of $6.45–$6.55 and revenue of $7.4–$7.5 billion, both above Wall Street estimates of $6.07 EPS and $7.2 billion in revenue.","as_of":"2026-08-05","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-11-04 Q3 後再度上調 FY2026 指引：淨銷售成長 18–19%（前 16–17%）；Q3 淨銷售 +21.2% 至 $1,976.4M；含 $109.6M 關稅退款認列（調整後排除）。","source":"Quartr: SharkNinja (SN) Q3 2026 earnings summary / company press release","url":"https://quartr.com/events/sharkninja-inc-sn-q3-2026_FGH0J5qh","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價 2026 年持續上移：MarketBeat 共識 4 月約 $145.90、8 月約 $181.73；Investing.com 10 月底 13 位分析師平均 $215.81（高 240、低約 195.67，Piper $234、TD Cowen $230、JPM $223）。各站分析師數與方法不同，且該聚合站為搜尋摘要未核頁面。","source":"Investing.com SharkNinja consensus estimates","url":"https://uk.investing.com/equities/sharkninja-consensus-estimates","excerpt":null,"as_of":"2026-10-31","retrieved_at":"20261108","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 公司上調 FY2026 調整後 EPS 指引至 $6.65–6.75。","source":"24/7 Wall St.","url":"https://247wallst.com/cards/sharkninja-q3-2026-earnings-sn-01m6k7dyhj9x4g5k5faf8fzmqz","excerpt":"Adjusted EPS guidance was lifted to $6.65 to $6.75, and adjusted EBITDA is now expected to land between $1,380 million and $1,391 million.","as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Intrinsic Alpha 共識目標 154、區間 128–200（可能早於上調）。","source":"Intrinsic Alpha SN estimates","url":"https://intrinsicalpha.com/equity/nyse/sn/estimates","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月8-K共8份，僅2份含重大項目（7/13 Item 8.01 董事長豁免後出售持股；2/11 Item 8.01 授權7.5億美元回購）；無併購類(1.01/2.01)項目","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001957132&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 8 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"董事會2026-07-10批准董事長CJ Xuning Wang一次性限制期豁免，其出售部分持股予既有機構投資者","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1957132/000110465926082783/tm2620293d1_8k.htm","excerpt":"the board of directors (the “Board”) of SharkNinja, Inc. (the “Company”) approved a one-time limited waiver to the Company’s Chairman, CJ Xuning Wang, under the Company’s Insider Trading Policy and Code of Business Conduct and Ethics","as_of":"2026-07-13","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026-02-11董事會授權最多7.5億美元股票回購，預計不舉債","source":"SEC EDGAR 8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1957132/000195713226000009/sharkninja-20260211.htm","excerpt":"the Company announced that its Board of Directors authorized a share repurchase program of up to $750.0 million of the Company’s outstanding ordinary shares.","as_of":"2026-02-11","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"Foodi OP300壓力鍋召回（CPSC #25-247，180萬台、106起燙傷）；後續消費者集體訴訟，N.D. Cal. Biscovich案獲早期駁回（2026-03）","source":"Shook Hardy & Bacon news 2026 / CBS News","url":"https://www.shb.com/news/2026/03/sharkninja-class-action-win","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 10-K（2026-03-02）：二手報導稱公司揭露財報內控重大缺陷、審計師對ICFR出具否定意見；未見重編報導（二手來源，未核10-K原文）","source":"rallies.ai: SharkNinja slides as internal-control weaknesses resurface","url":"https://rallies.ai/news/sharkninja-slides-as-internal-control-weaknesses-resurface-and-secondary-sale-overhang-lingers","excerpt":null,"as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"壓力鍋召回後消費者集體訴訟，N.D. Cal.案獲SharkNinja聲請駁回；另有NeverStick炊具、果汁機消費者案；搜尋未見證券集體訴訟","source":"Shook Hardy & Bacon: SharkNinja class action win","url":"https://www.shb.com/news/2026/03/sharkninja-class-action-win","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"CPSC召回Foodi OP300壓力鍋180萬台（#25-247，2025-05-01，約在12個月窗口之前）；搜尋未見2026新召回","source":"CBS News / CPSC recall #25-247","url":"https://www.cbsnews.com/news/sharkninja-recall-1-8-million-pressure-cooker-burns-walmart-amazon","excerpt":null,"as_of":"2025-05-01","retrieved_at":"20261108","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"-","claim":"未見SEC調查或重編報導；近12個月8-K無Item 4.02。但二手報導稱FY2025內控有重大缺陷、ICFR否定意見","source":"rallies.ai / SEC EDGAR 8-K 清單","url":"https://rallies.ai/news/sharkninja-slides-as-internal-control-weaknesses-resurface-and-secondary-sale-overhang-lingers","excerpt":null,"as_of":"2026-03-02","retrieved_at":"20261108","affects":["decision_inputs.bear","thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":51.45,"operating_margin_pct":15.58,"fcf_margin_pct":6.8,"rd_intensity_pct":5.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SN","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"WHR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":13.08,"operating_margin_pct":2.05,"fcf_margin_pct":-1.71,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WHR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HELE","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.37,"operating_margin_pct":9.4,"fcf_margin_pct":8.06,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HELE","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"NWL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.58,"operating_margin_pct":8.38,"fcf_margin_pct":0.72,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NWL","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"SN"},"financial_history":{"ticker":"SN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":3717366000.0,"revenue_yoy_pct":null,"gross_margin_pct":37.94,"operating_margin_pct":8.65,"net_income":232354000.0,"diluted_eps":1.671818,"free_cash_flow":110530000.0,"fcf_margin_pct":2.97,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":4253710000.0,"revenue_yoy_pct":14.43,"gross_margin_pct":44.85,"operating_margin_pct":8.78,"net_income":167078000.0,"diluted_eps":1.2,"free_cash_flow":148800000.0,"fcf_margin_pct":3.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":5528639000.0,"revenue_yoy_pct":29.97,"gross_margin_pct":48.15,"operating_margin_pct":11.65,"net_income":438705000.0,"diluted_eps":3.11,"free_cash_flow":295439000.0,"fcf_margin_pct":5.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":6399188000.0,"revenue_yoy_pct":15.75,"gross_margin_pct":49.01,"operating_margin_pct":14.38,"net_income":701374000.0,"diluted_eps":4.94,"free_cash_flow":474353000.0,"fcf_margin_pct":7.41,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SN/SN_Q3_2026_Earnings_Call_20261104.md）

# Q3 2026 Earnings Call
**SharkNinja, Inc.** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to the SharkNinja Third Quarter 2026 Earnings Call. [Operator Instructions] 
I will now hand the conference over to James Lamb, Senior Vice President of Investor Relations and Treasury. 
James, please go ahead.

**James Lamb** (Executives):
Good morning, and welcome to SharkNinja's Third Quarter 2026 Earnings Conference Call. Earlier today, we issued our Q3 earnings release, which is available on the company's website at ir.sharkninja.com. A replay of today's webcast will also be available on the site shortly after the call. 
Before we begin, let me remind you that today's discussion will include forward-looking statements based on our current perspective of the business environment. These statements involve risks and uncertainties, and actual results may differ materially. For more details, please refer to our earnings release and the company's most recent SEC filings, which outline factors that could impact these statements. 
The company assumes no obligation to update or revise forward-looking statements in the future. Additionally, during the call, we will reference non-GAAP financial measures, which we believe provide valuable insight into the underlying growth trends of our business. You can find a full reconciliation of these measures to their most directly comparable GAAP measures in the earnings release.
Joining me today are our Chief Executive Officer, Mark Barrocas, and Chief Financial Officer, Adam Quigley. Mark will start by providing a business update, followed by Adam, who will review our Q3 financial results and share our outlook for 2026. Mark will then offer some closing remarks before we open the call to questions. During the Q&A session, please limit yourself to one question and one follow-up.
I would now like to turn the call over to Mark.

**Mark Adam Barrocas** (Executives):
Thank you, James. Good morning, everyone, and thank you for joining us today. Hard-working and never satisfied, at SharkNinja, we believe these are essential traits to keep us focused squarely on solving consumer problems. When we do that, we earn consumers' trust and drive success in our business. Q3 was another great example of this, and we couldn't be more energized to drive momentum into Q4 and 2027. 
In the third quarter, net sales grew 21.2% year-over-year. This marks SharkNinja's second quarter in a row over 20% and 14th consecutive quarter of double-digit growth. Our top line strength this quarter was well balanced.
Domestic net sales grew over 19% year-over-year and international grew more than 25%. We saw tremendous performance across channels, categories and geographies. Importantly, our base business contributed the largest impact of net sales performance, reinforcing the growth foundation I focused on last quarter.
We spoke about a strong focus on the core a year ago, and our results clearly show that we're succeeding here. In our view, this kind of growth at a consumer company of our size is highly differentiated and something we're really proud of. We keep doing it quarter after quarter against a bar that keeps rising. We often describe this durability coming down to 3 SharkNinja differentiators: diversification, strengthen the core, and execution powered by our unique culture. There's a fourth factor, reinvention.
Our mission remains steadfast, positively impacting people's lives every day in every home around the world. But how we accomplish this is constantly evolving. To win consistently over time, we believe SharkNinja must continuously reinvent the ways we operate. Where other companies may resist change, we embrace new challenges head on, whether it's the emergence of opportunities like social and agentic commerce or generational technology advancements like artificial intelligence. SharkNinja is purpose-built to adapt and thrive.
Reinvention means we can boldly enter a new era. When I look back at how we've transformed the business over the last 18 months, one thing is clear, SharkNinja is a consumer technology company operating at hyperscale. That's not a new idea for us. It's the natural extension of how we have described SharkNinja as a consumer problem-solving company.
To us, hyperscale means scale that compounds where every product, market and piece of content is designed to make the next one better, more innovative and more successful. This concept shows up in what we make, how we market, how we sell, how fast we learn, and how far we reach.
Starting with product. Today, we compete in 41 subcategories from vacuums to espresso makers, air purifiers, beauty tools, air fryers, outdoor products and everything in between. That is hyperscale in action, which we believe is the first enabler of our long-term diversified growth opportunity. We're complementing that scale by introducing more technologically advanced products across the portfolio. 
Take the Ninja AutoBarista as an example. The complex software that automates countless drink options is significantly more sophisticated than our capabilities even a year ago. You will see more examples like this in our 2027 new product lineup, clear evidence that we're a consumer technology leader. 
Next, how we market, which brings me to a concept internally we call spillover. In short, spillover is the global demand generation benefit we see from how far our content reaches. Content from Canada gets watched in the United States. Content from Spain can influence Chile. Content from France, finds an audience in Quebec. Picture of spiderweb with threads running back and forth and in every direction, where the content originates is often not the only place is where it's consumed. We have always known spillover existed. 
What we didn't have was a data science-driven way to measure it and immediately act on it, not in weeks, but in hours. Over the last 12 to 18 months, we've built proprietary technology platforms that do exactly that. Today, we can identify a piece of content from the U.K. taking off in Norway, alert our marketing teams immediately and amplify it same day across our media ecosystems. Our social media scale makes us uniquely positioned to succeed at this.
Now spillover only matters if you can serve the consumer. As our products become more available and our brands become better known in more countries, we can build the sales strategy around what the content is telling us. Spain is a great example. When we converted to a direct model, we knew where to lean in with retailers. We had seen how Spanish language content from places like Mexico was landing with Spanish consumers and which products they were asking for by name. Investments in technology paired with globalizing our demand generation strategy, that is hyperscale marketing, befitting a true consumer technology company. 
How we sell is the next lens. We operate in more than 30 countries with more than 180 partners worldwide. Our goal is simple: be everywhere the consumer shops. This starts with our long-standing retail partnerships where increased placements, media activations and big support create a tremendous amount of excitement as we move toward the holiday season.
Simply put, consumers want SharkNinja products. So retailers want to feature our products. We're privileged to have earned this status with retailers, both domestically and internationally. And as we expand worldwide, this means establishing new channels of growth with regional pure-player partners like Mercado Libre in Latin America and Allegro in Poland to name a few. 
As shopping behaviors evolve in the coming years, we feel our scale advantage can compound further. I believe social commerce is the biggest change in consumer retail since Amazon. We're a leader on TikTok Shop, and our global presence gives SharkNinja access to an enormous number of affiliates and the technology to identify and succeed with them. This opportunity extends beyond TikTok Shop with affiliate networks emerging on Meta, YouTube, Snap and other platforms. 
Results so far have been incredibly encouraging and we're excited to continue to build this capability worldwide. Social commerce represents selling scale we could not have unlocked even 18 to 24 months ago, all managed using proprietary technology and KPI dashboards that we have developed. These social commerce efforts don't just benefit their respective platforms, they help fuel the demand flywheel for SharkNinja products across the entire e-commerce system. We're leveraging our digital presence with learnings from our own direct-to-consumer overhaul to drive much stronger outcomes on traditional retailers' digital storefronts.
In fact, year-to-date POS across our major U.S. retailer sites is up more than 30% year-over-year. We believe SharkNinja's capabilities as a global consumer technology company deepen our omnichannel competitive advantage. 
Next, how fast we learn? We have always moved fast at SharkNinja, but AI is supercharging our capabilities across the organization. Our internal AI proliferation initiative, Jailbreak SharkNinja has been a runaway success this year. The impacts we're seeing from the people closest to the business have been eye-popping. So much so that we are doing another Hack Week starting next Monday. The timing is intentional. We're refilling the pipeline with lots of additional initiatives focused on supercharging 2027. 
Our most significant AI investments are targeted at 2 of our largest costs, media spending and promotional dollars. At our hyperscale, the total opportunity here is massive. We spend more than $1.5 billion annually in these 2 areas combined. We're doing the work now in 2026 to pay off in '27 and '28 and beyond.
Even in the early stages, we're discovering meaningful insights, all of which we anticipate will help optimize share gains, gross profits and contribution margin. The dawn of agentic commerce is another major opportunity for SharkNinja. While it remains early days, we continue to work closely with leading AI and commerce platforms to develop and test new consumer experiences.
Holiday 2026 will be an important measure of how consumers utilize these platforms for product discovery and brand engagement. Because our goal is to be everywhere the consumer shops, we intend to remain at the forefront as this exciting channel opportunity evolves in 2027. The same drive is powering new initiatives on sharkninja.com. AI-powered search is live with early results showing a nice high single-digit increase in revenue per search visitor, Consumers can also now add products directly to their carts within our shopping agent. Agentic Commerce is another area where we believe our scale is a meaningful differentiator versus our peers. 
Finally, how far we reach? Becoming a consumer technology company has significantly broadened our demographic profile. This summer, our consumer insights and analytics teams conducted a deep dive into a question I hear most from investors. How durable is this growth? And who is it coming from? We looked at SharkNinja inside the American household. Based on our internal data and external sources such as Circana Consumer Panel, we measured household penetration across age, income, household size and more. And here's a big takeaway, we're seeing widespread gains across the demographic spectrum. Success isn't concentrated in one age group, one income level or one household size. It's broad-based. 2 powerful trends in the data really stand out. 
First, our fastest-growing cohort is our youngest one. We've discussed previously how 10 years ago, our core consumer was typically 35 to 55 years old. Today, our demographic data shows that among 18- to 24-year-olds, household penetration is up more than 50% over 2 years to the high single-digit range. This is significantly faster than the next fastest cohort with the Shark and Ninja brands, both driving gains with these younger consumers.
Naturally, discretionary buying power in this cohort is still relatively low compared to other demographic groups. This means that success in capturing younger consumers isn't just about revenue today, it's about laying roots for future growth and customer lifetime value. When you earn a consumer at an early age, you get the opportunity to grow with them, the college dorm room, the first apartment, getting married, the first home, and more. Each of these moments is a reason to engage with SharkNinja. We're developing that relationship earlier than ever with a long runway to deepen it. 
Second, when looking at cohorts by household size, penetration grew fastest in families with 4 or more members. This matters because a bigger household has more consumer problems to solve. Encouragingly, we also see evidence of multiple members in a family unit purchasing from SharkNinja. More density in the household means more occasions, more needs and likely a larger wallet to access. That's a cross-selling opportunity, both for existing categories and new ones.
What this means is SharkNinja has a growing presence in the American home. Two things are happening at once: Younger customers are finding us early, which means decades of potential growth and larger households are buying more of our products because they value our ability to solve multiple problems across their lives. It all adds up to a growing buyer base that continues to engage across the breadth of the Shark and Ninja brands. That's a powerful compounding growth driver and another example of increasing scale. 
The journey to become a consumer technology leader didn't happen overnight, but it feels like we're accelerating. Consider where the business was only a year ago. We were replatforming our direct-to-consumer website from 3 URLs into one upgraded sharkninja.com. TikTok Shop had just launched only in the United States and the United Kingdom. We were in the midst of converting key markets from distributor-led to direct models. And in some countries, too few categories and channels were limiting our growth.
We have worked diligently to address every one of these areas, and we're now seeing the fruits of that labor in our results. And we're just getting started. Scale drives success and success builds more scale. It's a positive flywheel that has enabled our transformation. SharkNinja is a consumer technology company with limitless potential in my mind. In fact, I've never been more excited to be in business than I am today. 
Now let me walk you through our 3-pillar growth strategy beginning with our first pillar, expansion into new and adjacent categories. In August, we launched the Ninja HydraSense, a revolutionary new water filtration product. This is a perfect example of consumer technology in action. At first glance, water filtration appears to be a crowded category, but we believe we found a real white space. 
Our consumer insights research identified a highly bifurcated market between entry level and very costly products. Importantly, we also discovered that consumers don't often fully understand filter performance, especially with low-end solutions. The Ninja HydraSense is designed to be an innovative disruptor. Our new precision pressure technology removes up to 10x more contaminants than the leading filter. This level of performance is akin to a reverse osmosis system, which can often cost $2,000 or more. 
For $199, we feel the Ninja HydraSense has democratized great water. We view this as a clear opportunity in a large market we have sized to over $6 billion. Consumer response has been extraordinary with social media post testing the HydraSense on everything from soda to pickle brine. This is also a real repeat purchase opportunity with replacement filters. Early subscribe and save attach rates on our D2C site more than tripled our internal expectations, a strong early sign as we look to apply this concept to other parts of our business. 
The launch of Ninja HydraSense was years in the making. We took the time to really understand the consumer problem, the market opportunity and the competition. While we're thrilled with the debut, we're even more excited to develop a technology platform here to drive years of future innovation. SharkNinja doesn't just introduce products. We launched consumer technology franchises, and we always strive to bring a differentiated perspective on where the white space is. The opportunity of water filtration is a great example, but we took a similar approach to espresso to microwaves to fans and countless other categories. We believe SharkNinja is at its best when people ask, why didn't anyone else think of this? 
Looking into 2027, we're committed to entering 2 additional new subcategories to build on our 41 today. The ability to repeatedly and successfully introduce new and adjacent categories is one of the biggest differentiators for SharkNinja. Our scale across existing categories, consumer insights, social media and more gives us a unique ability to keep expanding our scope.
Our second pillar is growing share in existing categories. This pillar is the cornerstone of everything else we do at SharkNinja. We never stop innovating. Even in categories where our market share lead is dominant. Each of the major initiatives we introduced in our core franchises in 2026, the Shark PowerDetect Transformer in the upright vacuums, the new Shark AquaReach vacuum mop and the Ninja CrushBOSS kitchen system shows how we continue to reinvent our core as the bedrock of our growth. 
It comes from an obsessive focus on the consumer and from the technology scale and expertise that allows SharkNinja to be a disruptor, time and time again. Consistently delivering on product development is key and we're increasingly confident that the SharkNinja machine is built to do this broadly.
The Ninja MultiPot is one of the best-selling launches we ever had. The Ninja PREPi went from 0 to 10 million impressions on social media at a speed that impressed even us. These 2 respective categories, multi-cookers and food processors are as core as it gets. When consumers respond to existing category launches in such a huge way, it reinforces our strategy to focus so much attention here. And as subcategories evolve from new into existing franchises, SharkNinja's scale advantages continue to compound. 
Our third pillar is international expansion. I want to start with EMEA, where balanced growth drove our robust Q3 '26 results. The U.K. continued the excellent performance we have seen throughout 2026 led by contributions from several categories. Several of our recently converted distributor to direct markets also delivered noteworthy growth in the quarter. Spain and Italy were standouts and we can't wait for our first holiday season as a direct operator in these countries.
This same excitement extends to Germany and France. Meaningful expansion in category diversification and retailer product placements set us up for a strong finish to the year. The Latin America region further extended its run of excellent results. Mexico has set the standard for what a distributor-to-direct conversion should look like, partnering effectively with retailers, driving consumer demand with local language social media and executing operationally to fulfill that demand.
Beyond Mexico, our Latin America distributor markets had their best net sales quarter ever. We believe this underscores how much Latin American consumers want SharkNinja products, while showing the power of our omnichannel approach. We enter holiday 2026 with huge excitement across the region to reach more countries and more consumers than ever before. All of this is augmented by the newer ways we're reaching the consumer.
Our recent D2C upgrades and TikTok Shop launches have exceeded our expectations to date. We remain on track to be live with TikTok Shop in 14 countries ahead of the holiday shopping season. This increasingly robust omnichannel approach gives us confidence that international net sales growth can reaccelerate year-over-year in Q4 relative to Q3. 
That brings me back to where I started. What sets SharkNinja apart is our ability to leverage our hyperscale to serve the consumer, solving their pain points, rapidly innovating across products and markets and reaching them wherever they are. We see clear evidence that our focus on investment is a key enabler of this strong position.
In this quarter, we proactively reinvested a portion of our tariff refund across multiple high-return opportunities. There are a lot more places where we want to plant seeds and we intend to remain opportunistic in Q4. This is a moment for SharkNinja to be on offense to widen our moat by investing for the benefit of future years. 
Zooming out, there's a consistent theme here. Hard work and investments that we made in 2024 and 2025 are paying off now. We're doubling down and making big investments in 2026 to plant more seeds across product, technology, demand generation and more. We expect these will pay off in 2027 and 2028 as we continue pursuing our mission of positively impacting people's lives every day in every home around the world. 
Our guidance raise reflects the continued strength we are seeing in the business while we balance investment with a focus on profitability and margin expansion, we could not be more enthusiastic as we look ahead to the new year with all our hyperscale advantages poised to deliver exceptional performance. 
With that, I'll turn it over to Adam, who will walk you through our financial results and share our updated outlook for 2026.

**Adam Quigley** (Executives):
Thank you, Mark, and good morning, everyone. Q3 was a tremendous quarter for SharkNinja. Simply put, the business is firing on all cylinders, and I'm excited to walk through the details. 
Net sales in the third quarter increased 21.2% year-over-year to $1.98 billion. By geography, domestic net sales, which includes U.S. and Canada, increased 19.4% to $1.31 billion and international net sales were $663 million, up 25.2%. 
Starting with the strength of the U.S. business, net sales grew 20.8% to $1.22 billion. This is our highest growth rate in the U.S. since Q4 2024. As we highlighted last quarter, this strength is primarily coming from our focused efforts within the base business. We see core momentum in multiple subcategories and across our omnichannel ecosystem. Our large diversified collection of existing categories is growing through execution and innovation as a consumer technology company. This quarter is a clear proof point of compounding growth at scale within our U.S. business.
Moving to the international business. We saw broad-based strength across all regions in the third quarter. As Mark highlighted earlier, our EMEA results were robust with significant strength in places like Spain and Italy, where we recently converted from a distributor led to a direct model. 
Mexico and the rest of Latin America region continued to see strong sales trends as well. Our U.K. business grew 13.3% year-over-year to $268 million and is up nearly 17% year-to-date. As a reminder, we are comping over 26% U.K. growth in the third quarter last year following the launch of TikTok Shop while also lapping the point at which air fryer headwinds began to ease. We remain as convicted as ever in our ability to be a long-term grower in the largest and most mature markets, as demonstrated by the U.S. and U.K. performance this quarter. 
Turning to performance by category. Net sales in the cleaning category increased 4.1% year-over-year to $617 million, driven by our corded and cordless vacuum subcategories. Here again, we saw the power of relentless innovation to drive sales in our core businesses.
Net sales in the Cooking and Beverage category increased 36.6% year-over-year to $598 million. Multiple franchises contributed to the strength in the quarter, including the Ninja Luxe Café, Ninja Crispi and more. 
Net sales in the Food Preparation category increased 18.3% year-over-year to $486 million, driven by robust growth in our blending subcategory as we continue to innovate with launches like the Ninja CrushBOSS. Frozen Treats also performed nicely in the quarter. This is a good example of how growth compounds as we increasingly diversify the number of core categories at SharkNinja. 
Finally, our Beauty and Home Environment category increased 45.8% year-over-year to $276 million with continued strength across product lines. This quarter, we saw particular momentum in our Shark Beauty portfolio, both hair care and skin care.
Now let's move to gross profit. Adjusted gross margin increased 560 basis points to 55.9% of net sales our GAAP gross margin increased by roughly 910 basis points to 59.2% of net sales. As previewed last quarter, the primary driver of the Q3 gross margin expansion is the recognition of refund claims accepted by the U.S. Customs and Border Protection for duties previously paid under IEEPA that are attributable to duties, expense, and cost of sales. 
For the portion of the tariff refund claims attributable to duties expense in fiscal 2025, we exclude the benefit from our adjusted results. These duties were recognized in a prior period and are not indicative of our ongoing operating performance. The portion of the refund claims attributable to duties expense in fiscal 2026 is not excluded and remains in our adjusted results.
The IEEPA tariff refund claim related to 2025 of approximately $110 million represents the gross number recognized in Q3. This differed slightly from our original expectation of roughly $124 million or about half of the total refund claim of approximately $247 million. 
The difference is due mostly to slight changes in the realized split between duties attributable to FY 2025 and 2026. The $110 million of gross FY 2025 duties is partially offset by intentional reinvestment into our cost of goods sold line. In Q3, we recorded approximately $45 million due to our factory partners as recognition of their extraordinary partnership during the tariff-related headwinds in 2025. 
Moving down the P&L. Our adjusted operating expenses this quarter totaled $680 million or 34.4% of net sales. This compares to 32.6% of net sales in the year ago quarter. Before I break down each operating expense line item, I want to take a moment to remind everyone of the plans we laid out last quarter. Our updated outlook in August reflected stronger underlying operating performance as well as the expected net benefit from the tariff refund associated with FY 2026 duties. 
We foreshadowed opportunistic reinvestment of a portion of that benefit in targeted areas that support long-term growth. These include retail activation, media, technology and AI capabilities along with the acceleration of some R&D efforts. Some of these investments impacted the following operating expense lines. 
The numbers I will walk through here are non-GAAP results. For the full reconciliation to our GAAP measures, please reference our earnings release. Non-GAAP research and development expenses increased 24.4% year-over-year to $111 million compared to $89 million in the prior year period, deleveraging roughly 10 basis points year-over-year. 
Disruptive innovation has always been a competitive advantage for SharkNinja, and we will continue to invest in our R&D engine, including opportunistically accelerating the time line of investments when we believe it makes sense to do so. Non-GAAP sales and marketing expenses increased 25.3% year-over-year to $445 million compared to $355 million in the prior year period deleveraging approximately 70 basis points year-over-year. 
Leaning into our media and selling efforts, especially as we ramp up new categories and geographies, helped SharkNinja build a stronger global brand. Non-GAAP general and administrative expenses increased 43.3% year-over-year to $125 million compared to $87 million in the prior year period, deleveraging just about 100 basis points year-over-year. 
Investments in SharkNinja personnel and technology, including the acceleration of strategic, AI investments drove the increase here. Ultimately, we delivered over 21% sales growth and approximately 46% adjusted EBITDA growth in the third quarter for an adjusted EBITDA margin of 23.3% of net sales. This is consistent with SharkNinja's profitability goal of delivering full year adjusted EBITDA growth ahead of net sales growth.
We continue to do this while spending proactively on high ROI investment opportunities balanced by remaining prudent and disciplined when considering operating expenses as a percent of net sales. 
To wrap up the income statement, our GAAP effective tax rate in Q3 was 23.3% while our non-GAAP effective tax rate was 21.7%. Adjusted net income in the period was $331 million or $2.34 per diluted share compared to $213 million or $1.50 per diluted share in the year ago period. Our adjusted net income in Q3 grew roughly 55% year-over-year, marking growth of 25% or better in 13 of the last 15 quarters.
Turning to the balance sheet and cash flow. At the end of the third quarter, cash and cash equivalents totaled almost $488 million, up approximately 85% year-over-year. Total debt outstanding at quarter end was $709 million, and we continue to have nearly $495 million of capacity available to us on our $500 million revolving credit facility. 
Total inventories were $1.43 billion exiting the quarter, up 23.3% year-over-year. We have now lapped the large levels of tariff prebuilt inventory from late 2024 and early 2025 with inventory growth tracking closer to net sales growth. In the quarter, we repurchased roughly $50 million worth of stock as part of our authorization. This brings our year-to-date activity to $170 million so far in 2026. We are pleased with our stock buyback activity, and we'll continue to utilize the program opportunistically. 
Let's move to our outlook. Consistent with prior quarters, our updated 2026 outlook assumes current tariff levels persist for the remainder of the year, including minimum rates of 10% for Indonesia, Malaysia and Cambodia and 12.5% for China, Vietnam and Thailand. 
As I mentioned earlier, we utilized a portion of the tariff refund benefit recognized in Q3 to reinvest across multiple areas of the P&L. Last quarter, we had sized this opportunity at approximately $95 million as the difference between the approximately $125 million expected tariff refund amount attributable to duties expense in fiscal 2026 and the anticipated flow-through to adjusted EBITDA of approximately $30 million. 
In the quarter, we actually recognized approximately $134 million of tariff refund benefit associated with fiscal 2026 duties. This slightly higher amount allows us additional flexibility to reinvest in the same priorities I outlined earlier. 
As we begin to execute on the reinvestments in Q3, some timing and other considerations spread a portion of the spending across 2 quarters. We see multiple opportunities in Q4 to complete these reinvestment initiatives in targeted areas designed to drive exciting momentum in 2027 and beyond. Our updated outlook reflects this timing dynamic in tandem with our very strong core business performance. 
For the full year 2026, we now expect net sales to increase between 18% and 19% compared to our prior guidance of a 16% to 17% increase. Adjusted net income per diluted share to be in the range of $6.65 and to $6.75 compared to $6.45 to $6.55 previously. Adjusted EBITDA to be in the range of $1.38 billion to $1.391 billion representing growth of 21.5% to 22.5% year-over-year compared to the prior expectation of $1.36 billion to $1.37 billion, representing growth of 19.5% and to 20.5% year-over-year. 
We continue to expect net interest expense to be down relative to 2025. Our GAAP effective tax rate to be approximately 22% to 23% and capital expenditures to be between $190 million to $210 million for the year, where we are now tracking closer to the midpoint instead of the high end. 
Our Q3 actuals and the high end of our updated 2026 outlook imply that in the fourth quarter of 2026, we expect our net sales growth to be up approximately 17% year-over-year. With some timing shifts of previously planned reinvestments from Q3 into Q4, we anticipate adjusted gross margins in the fourth quarter to be down approximately 100 basis points year-over-year. 
Finally, the high end of our updated 2026 outlook implies that in the fourth quarter of 2026, we expect adjusted EBITDA growth in Q4 to be up approximately 9% year-over-year. It's important to reiterate that this is simply the timing of certain tariff refund reinvestments, all of which we expect to be contained in Q4. 
Furthermore, these investments are intentionally designed to benefit 2027 and beyond, not 2026. Take our additional media spending as an example. When SharkNinja converts a distributor-led market to direct operations, we have a major marketing opportunity. We have the capability to ramp up advertising and media in a way the distributor partners simply cannot afford. 
Historically, the spending surge leads to meaningfully increased consumer awareness of SharkNinja products. In turn, we tend to see a demand generation uptick that typically leads to sizable inflection in sales. With several countries having recently transitioned to direct operations in EMEA, we are utilizing a portion of the tariff refund windfall to target incremental media dollars in these areas. 
For simplicity and clarity, consider the second half of 2026 compared to the second half of 2025. When looking at the top line and bottom line in totality based on the high end of our updated outlook, we anticipate net sales in the second half of 2026 to grow roughly 19% and adjusted EBITDA to grow roughly 25% compared with the second half of 2025. Once again, this is consistent with our annual goal of growing adjusted EBITDA dollars faster than net sales. 
Our growth and profitability algorithm remains intact. Importantly, we intend to perpetuate this into next year and beyond. Our main objective remains the same: to grow adjusted EBITDA dollars faster than net sales dollars in 2027. 
To close, our Q3 performance reflects powerful momentum across the business. All elements of our net sales engine are firing across products, geographies and channels as components of our 3-pillar growth strategy. 
Most importantly, we continue to pair exceptional profitability improvement alongside top line growth. I could not agree more with the point Mark made earlier, we believe there has never been a more exciting time for SharkNinja to be in business. 
Thank you. With that, I will now turn it back to Mark.

**Mark Adam Barrocas** (Executives):
Thanks, Adam. This has truly been a transformational year for SharkNinja. We've made significant strides across the board, in what we make, how we market, how we sell, how fast we learn and how far we reach. We've done all of this globally with a larger and more complex business than ever before. Investors constantly wonder how SharkNinja can keep growing at this size, and we continue to deliver.
In fact, our 21% net sales growth this quarter is right in line with our longer-term track record, a 21% compound annual revenue growth rate over the last 18 years. It all adds up to one thing. SharkNinja is a consumer technology company operating at hyperscale. In my experience, consistent success requires constant reinvention and the willingness to adapt. We can't wait to show the world what we're capable of as we close out a strong 2026 and look ahead to 2027. 
While SharkNinja will never stop evolving, at the end of the day, it always comes back to the consumer. Everything we do is grounded in remaining true to this mantra. It keeps us diligent, ambitious and laser-focused on solving the next consumer problem. 
I want to express my gratitude to the more than 4,100 team members around the globe who make this possible. Because of you, we believe SharkNinja is powerful and differentiated with an incredibly bright future ahead. Thank you. 
This concludes our prepared remarks, and I'll now turn it over to the operator to kick off Q&A. Operator?

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Randy Konik with Jefferies.

**Randal Konik** (Analysts):
Yes. Mark, I was just looking at our initiation report from 3 years ago, time flies. But in that report, it kind of references your thoughts at the time on the total addressable market and the serviceable addressable market, both on a global basis and a U.S. basis. 
And the numbers at the time, if I look at it, on a global TAM basis, you were looking at $112 billion total addressable market and a serviceable addressable market of about $39 billion. And then on the U.S. side of things, at the time, again, 3 years ago, you were looking at a $38 billion total addressable market in the United States and a $16 billion serviceable addressable market in the United States against 3 years ago. 
So if you think about where we've come from over those past 3 years around country expansion, category expansion, et cetera, how do you want us to think about changes in those numbers in terms of kind of framing up TAM and SAM today and going forward?

**Mark Adam Barrocas** (Executives):
Yes, Randy, thanks for the question. Look, the latest thinking that we have is that our total addressable market is roughly about $130 billion, and that number continues to keep growing as we expand into new categories. I mean just with the addition of water purification and microwaves added almost $10 billion of TAM to the overall addressable market. 
So if you think about our current guidance at a little under $8 billion this year, we're very, very small percentage right now of that available TAM. Now to me, and I think the biggest change from kind of 3 years ago when you and I had this conversation was, are we going to be able to really take advantage of that TAM in markets like Latin America in markets like non-English-speaking Europe. 
And I think that we've really proved that over the last couple of years that consumers are responding to us as much in Chile and in Poland, as they are in the U.K. or the United States. I mean we're obviously just still in the very early stages in those markets, but demand is strong. Consumer engagement is strong. Obviously, our distribution model is going to need to mature and improve, and we're going to need to be able to scale up more categories in those markets. 
So we're in the very, very early stages. But for us, the main question is always, do consumers love the products? I mean that's where everything starts. I mean if we developed a water purifier and we said, great, consumers in America love the product, but we're not really sure that consumers in Norway are going to respond to it or consumers in Mexico are going to respond to it. I think that, that is a huge change from 3 years ago that consumers are in these markets responding to it. Our demand generation model is resonating and working in these markets. 
I remember people saying to me, Mark, Continental Europe is so different than anywhere else in the world. It's not so different than anywhere else in the world. I mean there's a robust direct-to-consumer business. There's a strong pure player market. TikTok Shop and social commerce is penetrating into these markets. We're in all the major brick-and-mortar retailers and we're scaling up and consumers are engaging with the content in these markets as well as they're engaging with the content in the United States or the U.K. 
So I think the market is big. I think you'll expect us to get into more new categories next year that will only continue to enlarge the size of the available market.

**Randal Konik** (Analysts):
Super helpful. My last question would be, I want to talk about unpacking your comments around the core growing. I think it gets lost sometimes when we're all focused on the innovation part of your business in the new category. 
But maybe talk about how you're thinking about proportion over the next few years or maybe 3 to 5 years of how much of the business is going to come from the core? How much from innovation? And based on that plus what you've talked about is framing out the customer cohorts and the customer base changing and expanding and widening that breadth, do you think that, that would give you an opportunity to continue to grow double digits in the United States market over the medium to long term?

**Mark Adam Barrocas** (Executives):
Randy, we came out of the first quarter and we grew high single digits in North America. And I got asked constantly why we're concerned about North America growth, I mean, look at what North America has done in the last 2 quarters, I mean, our North America business is on fire in these markets right now, and it is really being driven by the core by the base business. 
I mean -- and it's not just enhancements. I mean, we talked about product assortment changes a year ago. Assortments at retailers have gotten stale in certain categories. We talked about things that we did with the BlendBOSS a year ago. Look what we did this year and what we did to upright vacuum cleaners and look at what we've done with the CrushBOSS that we launched in the last quarter to reinvent the blending category. I mean, we've got food prep back to really significant growth year-on-year in the largest category within food prep is blenders and kitchen systems.
So I think between product assortment, between new products in these base categories, between things like Colors and you're going to see a lot more prints and collectibles coming out in these categories. We're doing a lot in terms of AI work, around promotion and media analytics and segmentation. I'm really excited about the base business. 
And I'll tell you, one of the proof points of that is, we've got a lot of engineers that want to work on the base business. I mean they want to work on reinventing corded sticks and where corded sticks can be moving forward. It's not that everyone is kind of going to the new shiny object. I mean we've got a lot of our engineering team that wants to go and really revolutionize the base business. And I think that is something that is so different in the business than it was 15, 18 months ago.

**Operator** (Operator):
Your next question comes from the line of Brooke Roach with Goldman Sachs.

**Brooke Roach** (Analysts):
Mark, in your prepared remarks, you indicated international will accelerate in 4Q versus 3Q. When I put that in the context of your 17% 4Q revenue guide, it implied a slower rate of growth in the U.S. exiting the year. Can you contextualize what you're seeing there?

**Adam Quigley** (Executives):
Yes. Thanks, Brooke. I appreciate it. I think what you saw from us in Q3 was an outstanding performance within the domestic market, right? U.S., one of the most impressive growth rates that you've seen all year. And so I think -- what happened in the quarter was really sales execution, operational execution, and we feel great about the holiday sell-in that's happening in Q3. 
As you look into Q4, we're comping some massive social commerce numbers from last year as well. And so TikTok Shop and other avenues were live for the first time last Q4 as well. And so exiting the year, domestic is very firmly a double-digit grower. And I think we've proven that now quarter after quarter this year. 
And going into next year, the trajectory is as strong as ever, both across new categories, across what social commerce has done. And to Mark's point on reinventing the core, the domestic business has a massive core component to it. 
So I think that's been one of the real proof points for us as we've grown the domestic businesses. What we're doing in the core is directly showing up in that domestic growth. So that will continue into '27.

**Mark Adam Barrocas** (Executives):
And Brooke, I mean, listen, we'll stand out in the quarter, and I think we'll see that in Q4 is the Walmart business. It's really rebounded tremendously for us. All of our major brick-and-mortar retailers are doing really, really well. We're growing our dot-com business. I mean things like walmart.com bestbuy.com and target.com are doing great. Our club business is strong. So there's really nice broad-based growth within North America. It's not coming from any one particular channel or retailer. 
And the last thing I would say is that we've really lapped all of the Canada changes. I think you're going to see really nice growth come from Canada in Q4. And I think we're set up for a strong Canada business in 2027 with a really new model in that category that's going to take on much more of a look like the U.S. business.

**Brooke Roach** (Analysts):
Great. And then just a follow-up for Adam. Can you contextualize the underlying gross margin drivers, excluding the refund and onetime reinvestment? How should we be thinking about the biggest buckets of opportunity and headwinds across tariffs, raw materials, freight mix and pricing as we enter 2027?

**Adam Quigley** (Executives):
Sure. I think when you think about the Q3 gross margin, certainly, the tariff refund is a big component of it. If you exclude the refund, gross margin would have been down around 100 basis points. That 100 basis points was really a choice that once we had visibility into the refund, we delayed any price increases. We've been taking on commodity increase, we've been taking on fuel, we've been taking on FX. There's been a number of headwinds, as you mentioned. 
And the refund once we had line of sight, it allowed us to then delay some of those price increases. Now exiting this year and then going into 2027, the dynamic that we're looking at is some of those headwinds remain headwinds.
And this is where we've kicked off work well earlier in the year across operating expenses as well as gross margin to start to get ahead of that. I think the headwinds, there's no new headwinds over the last couple of months. It's really the same ones that we've been talking about all year. And this is again where the SharkNinja playbook is on full display in terms of looking at every single lever that we have. And I think looking at '27, above all else, our overall growth algorithm remains unchanged, right? 
It's to grow adjusted EBITDA at a faster rate than net sales, and we feel very confident in our ability to continue to do that as we go into 2027. Operating expense leverage, that's going to be a massive component. You've seen us leverage before, you've seen us leverage significantly. And then you've seen us be opportunistic when we're able to. And so this is a very dynamic business that's enabled by the diversification in which we operate. And going into '27, that will be no different.

**Operator** (Operator):
Your next question comes from the line of Bob Drbul with BTIG.

**Robert Drbul** (Analysts):
I guess I'd like to ask 2 questions really around similar top line. As you look at the TikTok Shops, what you're seeing in the U.S., but also, I think you said up to 14 countries this holiday. How accretive do you think that can be to the business? And I guess the other sort of follow-on to that is, this is the, I think, the first year with the single website and the opportunity that you see there as well for this holiday season would be helpful.

**Mark Adam Barrocas** (Executives):
Yes, Bob. So look, I want investors to kind of think of this as more than TikTok Shop, but really think about it in terms of social commerce and kind of what is social commerce look like because we're growing on Meta, we're growing on YouTube. There are other platforms that we're scaling. So on the social commerce side, I think there's a few interesting dynamics. I think that one is the sales that we generate on the platform and the second is the sales that are generated off platform from the content that is viewed on the platform. So there's a lot of halo and spillover. 
The analytics that we've done is that we believe for every dollar of on platform sales that we're generating, we're generating $2 of off-platform sales that places like Amazon and walmart.com and target.com and our D2C site are beneficiaries of this content that is being put out there on social commerce where the consumer might decide later on that they're going to buy the product, but they're not going to buy it on the platform. 
The second is on the D2C business. We saw really nice D2C growth in Q3 globally. I think we're set up for a great holiday season from a D2C perspective. We're really credible destination now for the consumer to shop for our products. That is not something that I could have said globally for Christmas 2025. Our site experience wasn't great.
We had multiple sites. So I think, Bob, and we're just getting started in this. I mean we're just -- we just put an Agentforce. We're still working with Salesforce on implementing marketing cloud. So I think the CRM piece of it, the loyalty piece of it are all things that into 2027, I think there's still a lot of opportunity for us to scale the D2C business. And I do believe through '27, that will come in at a faster growth rate than the rest of the business.

**Operator** (Operator):
Our next question comes from the line of Phillip Blee with William Blair.

**Phillip Blee** (Analysts):
So Mark, now that you've had some time then to replatform your DTC channel, you're launching social commerce more just in international markets. How do you think about the category expansion opportunity there? You're not necessarily beholden to some of these slower open-to-buys at retailers now. 
Could you theoretically expand at a quicker pace? Is this something we should think about accelerating more meaningful? And then how should we think about the incremental contribution there?

**Mark Adam Barrocas** (Executives):
Well, listen, I mean we've talked about this in the past, Phillip, that we can develop these great products. We can create demand. But ultimately, if we can't get the product to the end consumer, that's where it falls down. 
And I think that we've always said that in places like Europe or Latin America, that we were somewhat constrained by the pace by which retailers were willing to bring on more product from us. Things like DTC growth, things like social commerce, things like platforms like Allegro in places like Poland, Mercado Libre in Latin America, break down a lot of those barriers. 
Now listen, there's no doubt that we want to continue to keep scaling in the brick-and-mortar retailers. But I'll give you an example. I mean this holiday season we're really excited about Spain and Italy. We have expanded placement in retailers, but I would say 50% of our product in Spain and Italy, this holiday season is only going to be available on D2C and social commerce and Amazon. So the consumer is going to have a much broader assortment from us on those platforms than they will in some of the brick-and-mortar retailers. 
Now I think the brick-and-mortar retailers will catch up. But I think it will take time, but I'm excited because we're somewhat more in control of our own destiny as it relates to our ability to be able to innovate, create demand and still get the product to the consumer without the blocker of the fact that it's not distributed in a particular market.

**Operator** (Operator):
We have reached the end of the Q&A session. This concludes today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SN_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：FY2026 淨銷售成長財測上調（原話："we now expect net sales to increase between 16% and 17%"）
- 2026-08-05｜CFO｜guidance：FY2026 調整後 EPS 財測區間與前次比較（原話："$6.45 to $6.55 compared to $6 to $6.10 previously."）
- 2026-08-05｜CFO｜guidance：FY2026 調整後 EBITDA 財測區間（原話："in the range of $1.36 billion to $1.37 billion"）
- 2026-08-05｜CFO｜guidance：EPS 上調 $0.45 中關稅退款貢獻口徑（原話："is associated with the expected net tariff refund benefit."）
- 2026-08-05｜CFO｜guidance：關稅退款認列金額與時點（原話："recognize a benefit of approximately $247.1 million as a"）
- 2026-08-05｜CFO｜margin：2026 年度關稅退款納入調整後指標的口徑（原話："will be reflected in these same adjusted metrics as part"）
- 2026-08-05｜CFO｜guidance：財測假設關稅維持現況（原話："assumes current tariff levels persist for the remainder"）
- 2026-08-05｜CFO｜guidance：仍預期全年調整後 EBITDA 成長高於淨銷售成長（原話："anticipate adjusted EBITDA growing ahead of net sales"）
- 2026-08-05｜CFO｜margin：毛利率壓力主因（原話："primary headwind due mostly to the annualization"）
- 2026-08-05｜CFO｜margin：調整後營業費用率連續第五季槓桿（原話："driven leverage on adjusted operating expense as a"）
- 2026-08-05｜CFO｜margin：獲利目標定義（原話："full year adjusted EBITDA growth that outpaces"）
- 2026-08-05｜CFO｜margin：Q2 調整後 EBITDA 利潤率下滑幅度（原話："adjusted EBITDA margin, down approximately 50 basis points"）
- 2026-08-05｜CFO｜margin：DTC／社群電商結構性毛利較高（原話："commerce does come at a higher structural gross margin."）
- 2026-08-05｜CFO｜capital_allocation：管理層選擇將部分退款再投資（原話："We are opportunistically choosing to reinvest a portion of"）
- 2026-08-05｜CFO｜capital_allocation：Q2 買回金額（原話："repurchased roughly $100 million worth of stock"）
- 2026-08-05｜CFO｜capital_allocation：買回採機動執行（原話："continue to utilize the program opportunistically."）
- 2026-08-05｜CFO｜capital_allocation：資本支出預期偏高端（原話："tracking toward the high end"）
- 2026-08-05｜CEO｜commitment：美國＋加拿大下半年雙位數成長（原話："double-digit second half number for the domestic business."）
- 2026-08-05｜CEO｜commitment：DTC 與聯盟行銷成長快於其他業務至 2027 年底（原話："to grow at a faster rate than the rest of the business"）
- 2026-08-05｜CEO｜commitment：2027 年大致持平人力下維持成長（原話："on roughly flat headcount as we get into '27."）
- 2026-08-05｜CEO｜commitment：每年至少推出 2 個新子類別（原話："we would launch in a minimum of 2 subcategories a year."）
- 2026-08-05｜CEO｜commitment：TikTok Shop 國家數目標（原話："goal of more than double that number by this holiday season."）
- 2026-08-05｜CEO｜commitment：經銷商轉直營告一段落（原話："now done for the foreseeable future with these distributor"）
- 2026-08-05｜CEO｜commitment：將推動零售商庫存於 Q4 增加（原話："push for inventory levels to grow as we head into"）
- 2026-08-05｜CEO｜risk：分析師懷疑雙位數成長可持續性（管理層轉述）（原話："hard to believe that double-digit growth in a business"）
- 2026-08-05｜CEO｜risk：加拿大 Q2 衰退（原話："The Canada business was down 17% as we flow"）
- 2026-08-05｜CEO｜risk：歐洲 DTC 轉換對 Q2 的影響（原話："they may even have a little bit of hurt"）
- 2026-08-05｜CFO｜risk：Q2 POS 高於出貨主因為 Prime Day 時點（原話："largely driven by the timing of Prime Day."）
- 2026-08-05｜CEO｜customer：TikTok Shop 國家數（原話："TikTok Shop in 7 countries compared to 0 in the year ago"）
- 2026-08-05｜CFO｜customer：零售商庫存（原話："Overall, the retailer inventory is extremely healthy."）
- 2026-08-05｜CEO｜customer：歐洲零售商是否調整年度陳列（原話："Some are simply not."）
- 2026-08-05｜CEO｜product：既有品類成長範圍（原話："typically grow mid- to high single digits."）
- 2026-08-05｜CEO｜product：新品多數落在既有品類（原話："products we launch each year go into existing categories."）
- 2026-08-05｜CFO｜product：清潔類 Q2 成長（原話："Cleaning category increased 4.1% year-over-year"）
- 2026-08-05｜CFO｜product：美容與居家環境類 Q2 成長（原話："Beauty and Home Environment category increased 65.3%"）
- 2026-08-05｜CEO｜product：電扇缺貨（原話："we sold out and couldn't capture all"）
- 2026-08-05｜CEO｜product：第 41 個子類別 Q3 末進入（原話："we'll be entering into our 41st subcategory"）
- 2026-08-05｜CEO｜product：AI 提升社群內容擷取率（原話："AI has lifted our capture rate to 60% plus accuracy"）
- 2026-08-05｜CEO｜product：AI 專案數量（原話："bet projects and 20 quick win projects."）
- 2026-08-05｜CEO｜product：AI 專案兩週檢視機制（原話："tangible progress on an initiative every 2 weeks"）
- 2026-08-05｜CEO｜product：Palantir 二期專案（原話："moved ahead with a Phase 2 initiative with Palantir"）
- 2026-08-05｜CEO｜product：AWS 媒體優化系統上線時程（原話："going live at the end of September on a system"）
- 2026-08-05｜CEO｜product：AWS 系統效益多在 2027 年（原話："really for the most part, that won't scale until '27."）
- 2026-08-05｜CEO｜competition：歐洲品類滲透率估計（原話："less than 10% penetrated on an overall category basis"）
- 2026-08-05｜CEO｜competition：年底可觸及 TAM 估計（原話："$125 billion to $130 billion available TAM"）
- 2026-08-05｜CEO｜competition：管理層對市場與自身創造需求的說法（原話："getting consumers excited about our products"）

### 問答異常語氣（迴避／改口／保留）
- SN_Q2_2026_Earnings_Call_20260805.md｜問：Randy Konik 問 DTC 與批發毛利差距，及行銷費用是否有槓桿空間｜答法：CFO 只說 DTC／社群電商結構性毛利較高，未給差距數字，也未回應行銷槓桿問題
- SN_Q2_2026_Earnings_Call_20260805.md｜問：Brooke Roach 問美國 DTC 業務目前規模｜答法：CEO 答不拆分 D2C 占比，改談成長快於其他業務與 Salesforce 上線
- SN_Q2_2026_Earnings_Call_20260805.md｜問：Steven Forbes 問相較去年錯過陳列日期，今年美國零售商陳列有何實質變化｜答法：CEO 先談歐洲與新通路，美國部分講 Walmart／Target 等促銷，未直接回答去年錯過陳列日的比較

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
{"date":"20260619","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"創新引擎可持續命中爆品（hit 接棒）","columns":{"2Y 驗證點":"每年 ~25 款新品中 ≥2-3 款成為千萬美元級爆品","5Y 驗證點":"新品類（戶外/家居環境/Beauty）合計營收佔比升至 ≥ 25%","10Y 驗證點":"研發命中率不衰減，品類數持續擴張","具體數字門檻":"整體營收 CAGR ≥ 10%；Beauty &amp; Home Env 維持 &gt; 20% 成長","信息來源":"公司法說（Q 報品類拆分）","漂移觸發":"連 2 季整體營收 &lt; +8% → 削弱（2Y 假設）"}},{"id":"H2","text":"供應鏈出中國 + 關稅可控（margin 不被吃）","columns":{"2Y 驗證點":"東南亞產能滿載、adj GM 維持 ~48%","5Y 驗證點":"SE Asia 多地分散降低單一國地緣風險","10Y 驗證點":"長期 GM 結構穩定 &gt; 47%","具體數字門檻":"adj GM（扣關稅一次性）≥ 47%；FY26 adj EPS ≥ $6.00（guide 下緣）","信息來源":"Q1'26 法說 + 8-K（5/6）","漂移觸發":"連 4 季 adj GM &lt; 47% → 削弱（5Y margin 假設）"}},{"id":"H3","text":"估值維持 high-teens~low-20s fwd PE（不 de-rate 至成熟期倍數）","columns":{"2Y 驗證點":"fwd PE FY27 維持 18-24x","5Y 驗證點":"成長放緩前不被重設至 De'Longhi 13.5x 級","10Y 驗證點":"市場持續給予「成長性溢價」","具體數字門檻":"fwd PE FY27 ≥ 16x（否則向消費電器成熟期收斂）","信息來源":"市場估值（Koyfin/yfinance）","漂移觸發":"fwd PE &lt; 16x 持續 → 反轉（市場 de-rate）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"消費降溫 + 爆品退潮 → 營收增速失速","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季營收 YoY、Beauty/Food Prep 增速","警戒閾值":"整體連 2 季 &lt; +8%"}},{"id":"R2","text":"關稅上修 / 促銷加劇 → adj GM 壓縮","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"adj GM（扣一次性）、東南亞稅率","警戒閾值":"連 4 季 adj GM &lt; 47%；SE Asia 稅率 ≥ 20%"}},{"id":"R3","text":"私牌/競品侵蝕 + 創新引擎衰減 → pricing power 結構下滑","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"新品命中率、ASP 趨勢、市佔","警戒閾值":"連續 ≥ 2 年新爆品數下滑 + ASP 下行（需 ≥ 50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":140.84,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SN_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
