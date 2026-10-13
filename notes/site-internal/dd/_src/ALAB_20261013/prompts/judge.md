你是 stock-analyst **v20 判斷 agent**，標的 ALAB（20261013）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"ALAB","date":"2026-10-13","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261013/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261013/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":392.4,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益率","value":39.1,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":22.7,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi5_non_gaap","label":"Non-GAAP 毛利率","value":73.7,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi6_non_gaap_eps","label":"Non-GAAP EPS","value":0.8,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"},"note":"consensus 0.69（來源：web_search，MarketBeat／Benzinga 2026-08-04）"},{"id":"f_kpi7_q3_fy2026","label":"下一季指引（Q3 FY2026）","value":"營收 540–560M；GAAP/Non-GAAP 毛利率約 72%；Non-GAAP opex 156–160M；Non-GAAP EPS 1.16–1.21；GAAP EPS 0.87–0.92；稀釋股數約 185M","period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"文字","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-04","period":"2026-08-04","unit":"date","basis":"距今 50 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_alab_gross_margin_pct","label":"ALAB 毛利率","value":75.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_alab_operating_margin_pct","label":"ALAB 營業利益率","value":22.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_alab_fcf_margin_pct","label":"ALAB FCF 利潤率","value":23.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crdo_gross_margin_pct","label":"CRDO 毛利率","value":67.07,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crdo_operating_margin_pct","label":"CRDO 營業利益率","value":31.74,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_crdo_fcf_margin_pct","label":"CRDO FCF 利潤率","value":27.57,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_gross_margin_pct","label":"MRVL 毛利率","value":52.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_operating_margin_pct","label":"MRVL 營業利益率","value":16.81,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_mrvl_fcf_margin_pct","label":"MRVL FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF，上半年累計；新聞稿無單季）","value":134.2,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}},{"id":"f_kpi4_sbc","label":"SBC 占營收","value":16.3,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":308.85,"period":"2026-10-13（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-13（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":81.32,"period":"2026-10-13（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-13（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":42.79,"period":"2026-10-13（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-13（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.03 → 4.03）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（6.39 → 6.39）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.08 → 8.08）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":4.03,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":6.39,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":8.08,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":33.89,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 3.01 → 4.03（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":152.14,"period":"2026-10-13（RTH 收盤，UTC）","unit":"x","basis":"1 個年度端點內的分位＝50.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-13（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":50.0,"period":"2026-10-13（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-13（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":44.58,"period":"2026-10-13（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝8.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-13（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":8.8,"period":"2026-10-13（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-13（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":43.57,"period":"2026-10-13（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝7.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-13（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":7.8,"period":"2026-10-13（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-13（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":84.92,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 4.03，分子＝快照價 342.21","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-1208.55,"period":"2026-10-13","unit":"USD m","basis":"yfinance 最新一季：總債務 44.41、現金 1252.96（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":173.49,"period":"2026-10-13","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":52371.46,"period":"2026-10-13","unit":"USD m","basis":"市值 53580.01 ＋ 淨負債 -1208.55","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":1908.53,"period":"2026-10-13","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":2972.7,"period":"2026-10-13","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":27.44,"period":"2026-10-13","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-13"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#none","axis":"competitive_share_entrants","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"FY2025 年報揭露客戶高度集中：前三大終端客戶約占營收 86%，風險揭露稱單一終端客戶超過 2025 年營收 70%（經搜尋摘要轉述，未直接讀原文頁面）。","source":"Astera Labs, Inc. Form ARS FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000114036126016366/ny20065212x3_ars.pdf","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"2026 年 Q1 業績揭露：Astera 贏得第二個客製 CXL 設計（KV cache offload），營收預計 2027 年；NVLink Fusion 相關客製矽與 NVIDIA 及一家 hyperscaler 深度開發中，營收 2027 年起；管理層稱客製產品會選擇性承接（經二手摘要轉述）。","source":"Astera Labs Q1 2026 earnings coverage (Converge Digest / Yahoo Finance summary)","url":"https://convergedigest.com/astera-labs-q1-revenue-jumps-93-ai-fabric-growth/","excerpt":null,"as_of":"2026-05-05","retrieved_at":"20261013","affects":["thesis.H","triggers"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K（搜尋摘要轉述）：五家客戶各占營收 10% 以上——A 20%、B 20%、C 17%、D 16%、E 11%，合計約 84%；最大單一客戶 20%。數字來自搜尋摘要對 10-K 表格的轉述，未逐字讀頁面。","source":"Astera Labs, Inc. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"The Company had the following customers that individually comprised 10% or more of its revenue","as_of":"2026-02-28","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2024 10-K：客戶 A 占營收 36%、B 24%、C 11%；客戶 F 占 2024 年底應收帳款 31%。","source":"Astera Labs, Inc. Form 10-K FY2024 (Financial_Report, SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629725000003/Financial_Report.xlsx","excerpt":"Customer A | Revenue 0.36; Customer B | Revenue 0.24; Customer C | Revenue 0.11; Customer F | Accounts Receivable 0.31","as_of":"2025-02-28","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 年 6 月 30 日 10-Q：現金、約當現金與有價證券 $1.3B，公司稱現金足以支應至少未來 12 個月營運；2026 上半年營運現金流 $162.3M。第三方資料站列總債務 $41.9M。（搜尋摘要轉述）","source":"Astera Labs, Inc. Form 10-Q (quarter ended 2026-06-30), SEC EDGAR","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000035/alab-20260630.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261013","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Amazon 持有認股權證，與採購 Astera 產品掛鉤，額度最高 $65 億採購額，隨採購至 2033 年 2 月歸屬（搜尋摘要轉述，第二手）；對毛利率有非現金影響。","source":"WebSearch 摘要（引 Astera 10-Q 與聚合站）","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000035/alab-20260630.htm","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#4","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"未查到主要客戶（超大型雲端業者）信用評等或財務惡化、破產、Astera 下修財測的報導；Q2 2026 財測 $355–365M 為指引而非下修。僅見 TD Cowen 目標價 $425→$375 維持 hold，屬評價面。","source":"TIKR 等聚合站（搜尋摘要）","url":"https://www.tikr.com/blog/astera-labs-beat-q1-2026-estimates-on-all-four-lines-heres-why-the-stock-sold-off-and-where-it-could-go","excerpt":"TD Cowen cut its target from $425 to $375 and kept a hold rating","as_of":"2026-05-05","retrieved_at":"20261013","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Gartner 2026年7月存貨預測：2Q26 全球半導體存貨指標(GIISST)降8.5%進入中度短缺，受AI半導體需求驅動，預期此趨勢延續至2027年。","source":"Gartner Insights Abstract","url":"https://www.gartner.com/en/documents/8208429","excerpt":"In 2Q26, the GIISST fell 8.5% into moderate shortage, driven by strong AI semiconductor demand. This trend is expected to persist through 2027","as_of":"2026-07-01","retrieved_at":"20261013","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"TrendForce：2026年NAND供給短缺4-5%，2027下半年供給位元成長將超過需求成長（二手轉載）。","source":"TrendForce via itiger: NAND Flash Supply Shortage Expected to Ease in Second Half of 2027","url":"https://www.itiger.com/news/1168527958","excerpt":"supply will fall short of demand by 4-5% in 2026, but by the second half of 2027, the growth in supply bits will outpace demand growth.","as_of":"2026-07-01","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Wolfe Research分析師Chris Caso認為半導體供過於求最早在2028年之前幾無可能（受新晶圓廠物理限制）。","source":"247WallSt: Top Chip Analyst: Semiconductor Oversupply Is Nearly Impossible Before 2028","url":"https://247wallst.com/investing/2026/07/30/top-chip-analyst-semiconductor-oversupply-is-nearly-impossible-before-2028-why-hes-bullish-on-memory/","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Micron執行長在9月30日財報會議表示記憶體供需於FY2027、FY2028可能進一步趨緊；下一波供給(Micron愛達荷/日本、SK hynix清州)多要到2028下半年後才放量。","source":"Micron earnings call 2026-09-30 (via search summary)","url":null,"excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261013","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ASML(2026年7月)：產能實質上賣到2027，訂單簿延伸至2028，指引今年約成長35%。","source":"Quilter: ASML beat and raise reinforces strength of semiconductor demand","url":"https://media.quilter.com/search/2026/asml-beat-and-raise-reinforces-strength-of-semiconductor-demand/","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"SEMI：300mm晶圓月產能至2028年底達1110萬片，年複合成長7%；先進製程(7nm以下)CAGR 14%。","source":"The Machine Maker: SEMI Projects 69% Growth in Advanced Semiconductor Capacity by 2028 Driven by AI Demand","url":"https://themachinemaker.com/news/semi-projects-69-growth-in-advanced-semiconductor-capacity-by-2028-driven-by-ai-demand/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"ALAB Q1 2026營收3.084億美元、年增93%；PCIe Gen 6約占近季營收三分之一且ASP高於前代；第三方稱Q2 2026營收年增104%至3.924億美元；風險含自研客戶晶片、多季客戶ramp執行風險。","source":"TIKR: Astera Labs Stock Is Up 227% in One Year","url":"https://www.tikr.com/blog/astera-labs-stock-is-up-227-in-one-year-heres-whats-driving-the-rally","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261013","affects":["moat_trend","thesis.H","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Astera Labs FY2025 10-K 與年報列出出口管制風險：若被認定違反貿易制裁或出口規則，可能面臨喪失出口權及罰款；亦提及美國商務部對先進運算晶片的限制持續修訂。屬一般性風險揭露，非特定進行中調查。（內容取自搜尋摘要轉述，未讀原文頁面）","source":"Astera Labs, Inc. Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Astera FY2025 10-K 風險揭露：Chinese customers facing tariffs may build their own products or buy from competitors, and may cancel or delay orders; prolonged or expanded export restrictions would hurt revenue and results.","source":"Astera Labs, Inc. Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Astera S-1 揭露：美國對部分中國客戶的銷售限制，使部分銷售可能需出口許可，且不保證獲准；並提及中國不可靠實體清單風險。","source":"Astera Labs, Inc. Form S-1 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000119312524040419/d285484ds1.htm","excerpt":"Due to the U.S. government restricting sales to certain customers in China, sales to some of our customers may require licenses in order for us to export our products; however, there can be no assurances that requests for licenses will be approved by the U.S. government.","as_of":"2024-02-01","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Q1 2025 法說：管理層稱中國出口限制對 retimer 出貨（連結 merchant GPU 系統）屬小幅逆風，終端客戶中國曝險低於營收 10%，尚未見關稅重大影響。","source":"Fintool Astera Labs Q1 2025 earnings summary","url":"https://fintool.com/app/research/companies/ALAB/earnings/Q1 2025","excerpt":null,"as_of":"2025-05-06","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 稱半導體關稅可能降低產品需求，美國對關鍵礦物的關稅可能推高投入成本。","source":"Astera Labs, Inc. Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":null,"as_of":"2026-02-28","retrieved_at":"20261013","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-01-14 公告對一小類先進半導體及含其衍生產品課 25% Section 232 關稅，2026-01-15 生效；適用範圍窄，搜尋結果未顯示 Astera 產品是否在涵蓋範圍內。","source":"White & Case; EY Tax News, 25% Section 232 tariff on certain advanced semiconductors","url":"https://taxnews.ey.com/news/2026-0209-us-section-232-proclamation-imposes-25-percent-tariff-on-certain-semiconductors","excerpt":"Effective 12:01 a.m. EST on 15 January 2026, a 25% ad valorem tariff applies to certain advanced computing chips and specified derivative products.","as_of":"2026-01-15","retrieved_at":"20261013","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"ALAB 10-K 揭露其主要製造商台積電的晶圓廠與主要經銷商皆位於台灣","source":"Astera Labs Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"the foundry used by our primary manufacturer, TSMC, as well as our primary distributor, is located in Taiwan","as_of":"2025-12-31","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險揭露：若台積電無法供應足量晶圓，ALAB 出貨與營收會受損","source":"Astera Labs Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629726000010/alab-20251231.htm","excerpt":"if TSMC is unable to supply us with sufficient quantities of wafers to meet all of our requirements","as_of":"2025-12-31","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K 稱製造夥伴、經銷商與多數營收集中於台灣、中國、南韓；FY2025 年報再加入新加坡，且多數營收來自東亞","source":"Astera Labs Form 10-K FY2024 / Form ARS FY2025 (SEC)，經搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/1736297/000173629725000003/alab-20241231.htm","excerpt":null,"as_of":"2024-12-31","retrieved_at":"20261013","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"IPO 招股書指出台灣地震風險因晶圓廠鄰近斷層帶而顯著，且可能無法以合理條件取得替代產能","source":"Astera Labs Form 424B4 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1736297/000119312524073873/d285484d424b4.htm","excerpt":"the risk of an earthquake in Taiwan and elsewhere in the Pacific Rim region on our business is significant due to the proximity of major earthquake fault lines to the foundry's facilities","as_of":"2024-03-20","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"第三方彙整站 policyrisk.com 評 ALAB 製造曝險為高，稱約 73% 不動產及設備位於台灣，且 2025 年單一終端客戶占營收逾 70%、前三大約 86%（第三方轉述，非原始 filing 逐字）","source":"policyrisk.com ALAB company profile","url":"https://policyrisk.com/world/company/ALAB","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"ALAB 2026 Q2 營收 $392.4M，QoQ +27%、YoY +104%；non-GAAP 營業利益率 39.1%。","source":"Astera Labs Reports Second Quarter 2026 Financial Results (asteralabs.com)","url":"https://www.asteralabs.com/news/astera-labs-reports-second-quarter-2026-financial-results/","excerpt":"Record quarterly revenue of $392.4 million, up 27% QoQ and up 104% year-over-year. Non-GAAP operating margin was 39.1%","as_of":"2026-08-04","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"PCIe 6 產品占 Q2 營收過半，Aries 訊號調節產品線創單季紀錄；管理層預期 Scorpio 交換器於 Q3 成為最大產品線，比先前預期提早一季。","source":"Futurum, Astera Labs Q2 FY 2026 Earnings Pull Scorpio Switch Leadership Forward","url":"https://futurumgroup.com/insights/astera-labs-q2-fy-2026-earnings-pull-scorpio-switch-leadership-forward/","excerpt":"Scorpio fabric switches become our largest product family, one quarter ahead of our prior expectations.","as_of":"2026-08-04","retrieved_at":"20261013","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 Q1 營收 $308.4M，YoY +93.4%；資料商顯示公司僅 1 個報告部門（Intelligent Connectivity Platform），無正式分部營收，以產品線為準。","source":"OpenCapital ALAB Q1 2026","url":"https://www.opencapital.sh/stocks/alab/earnings/q1-2026","excerpt":"Q1 2026 revenue of $308.4M (+93.4% YoY)","as_of":"2026-05-01","retrieved_at":"20261013","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"競爭風險：BofA 初始報告指出 Nvidia NVLink 與 Broadcom scale-up Ethernet 交換器的競爭可能拖累成長；Scorpio-X 對應 AWS 部署的 2026-29 年機會約 $2.5B。","source":"Nasdaq/Zacks, ALAB articles citing BofA initiation","url":"https://www.nasdaq.com/articles/alab-rides-strong-demand-pcie-solution-sign-more-upside","excerpt":"competition from Nvidia's NVLink and Broadcom's Scale-Up Ethernet based switches could weigh on growth","as_of":"2026-05-01","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"WSTS 2026 春季預測：2027 年全球半導體市場再成長 27% 至約 USD 1.9 兆；2026 年約 USD 1.51 兆。（as_of 為約略月份，2026-06）","source":"WSTS FC Release 2026 May / bits-chips 報導","url":"https://www.wsts.org/esraCMS/extension/media/f/WST/7618/WSTS_FC-Release-2026-May.pdf","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261013","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Astera 管理層稱光學為銅線的增量補充而非取代；整合 CPO 模組的 Scorpio X 規劃 2028 年以後，光學大規模採用預期在 2028 年以後。","source":"MarketBeat, Astera Labs targets $10B AI connectivity opportunity as Scorpio X series ramps","url":"https://www.marketbeat.com/instant-alerts/astera-labs-targets-10b-ai-connectivity-opportunity-as-scorpio-x-series-ramps-2026-05-27/","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261013","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"分析師指出 Nvidia NVLink 與 Broadcom Scale-Up Ethernet(SUE) 交換器的競爭可能拖累成長並限制估值倍數擴張；Broadcom 亦已推出 PCIe Gen 6 retimer/交換器，Marvell、Credo 為競爭者。","source":"Yahoo Finance, Astera Labs Battles Nvidia And Broadcom As AI Chip Market Heats Up; ServeTheHome, Broadcom Fires a Shot at Astera Labs with New PCIe and CXL Retimers","url":"https://finance.yahoo.com/news/astera-labs-battles-nvidia-broadcom-182512569.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261013","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"公司 2026 年 10-Q 風險因素列示競爭、產業整併、依賴第三方技術及產品價格隨時間下降；搜尋未發現 2026 年有具體替代品奪取份額的報告。","source":"Astera Labs Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000035/alab-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261013","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 約 2026-07-31 快照：23 位分析師（18 Buy、5 Hold），平均目標價約 $246；當時股價 $311.23，平均目標價低於當時股價約 19%。目標價均值相對近期個別調升顯得偏舊。","source":"Benzinga ALAB price-targets page","url":"https://kr.benzinga.com/quote/ALAB/price-targets","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261013","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"個別目標價：Barclays 於 2026-07-20 調升至 $325；Susquehanna 於 2026-07-31 調升至 $275 並維持 Neutral。","source":"Benzinga ALAB price-targets page","url":"https://kr.benzinga.com/quote/ALAB/price-targets","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261013","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"公司 2026-08-04 公布 Q2：營收創高 $392.4M，年增 104%；Q3 營收指引 $540M–$560M，前一季指引為 $355M–$365M。Benzinga 統計 2024-05-07 至 2026-08-04 共 10 次指引更新、9 次上調。","source":"Benzinga ALAB earnings-forecasts; Trefis 2026-08-06","url":"https://www.trefis.com/articles/610418/astera-labs-beat-and-guided-higher-then-fell-because-the-rally-came-first/2026-08-06","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261013","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"財報後股價下跌約 12%（Trefis 歸因於財報前已先漲）；Q3 躍升取決於 Scorpio X-Series 320-lane fabric switch 的單一部署時程。另有 Q3 EPS 指引 Benzinga 列 $1.16–$1.21（非GAAP），Simply Wall St 列 GAAP $0.87–$0.92，兩者口徑不一致、未能釐清。","source":"Trefis 2026-08-06; Benzinga earnings-forecasts","url":"https://www.trefis.com/articles/610418/astera-labs-beat-and-guided-higher-then-fell-because-the-rally-came-first/2026-08-06","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261013","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 指引毛利率約 73%（Q1 為 76.4%），約 200bp 下滑來自與關鍵客戶的非現金 warrant 協議（TIKR）。","source":"TIKR blog","url":"https://www.tikr.com/blog/astera-labs-stock-is-trading-at-all-time-highs-here-is-what-could-drive-it-even-higher?","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261013","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-02-09 以 $74.0M 收購一家私人資料中心加速方案公司的資產（商譽為主）；媒體傳目標為 Pliops，未獲官方證實","source":"Astera Labs Form 10-Q (quarter ended 2026-06-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000035/alab-20260630.htm","excerpt":"On February 9, 2026, the Company acquired certain assets of a privately held company that develops data center acceleration solutions, and the total purchase consideration was $74.0 million.","as_of":"2026-02-09","retrieved_at":"20261013","affects":["moat_trend","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-02-09 以 $74.0M 收購一家私人資料中心加速方案公司的資產（商譽為主）；媒體傳目標為 Pliops，未獲官方證實。另披露 2026-05-29 另一筆資產收購，對合併財報不重大；2025-12 另有 aiXscale Photonics 收購報導","source":"Astera Labs Form 10-Q (quarter ended 2026-06-30), SEC","url":"https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000035/alab-20260630.htm","excerpt":"On February 9, 2026, the Company acquired certain assets of a privately held company that develops data center acceleration solutions, and the total purchase consideration was $74.0 million.","as_of":"2026-02-09","retrieved_at":"20261013","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"ALAB","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":75.13,"operating_margin_pct":22.75,"fcf_margin_pct":23.02,"rd_intensity_pct":36.13},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ALAB","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"CRDO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.07,"operating_margin_pct":31.74,"fcf_margin_pct":27.57,"rd_intensity_pct":21.46},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CRDO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"MRVL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.21,"operating_margin_pct":16.81,"fcf_margin_pct":18.23,"rd_intensity_pct":25.84},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRVL","as_of":"TTM ending 2026-07-31（4季加總）"}}],"subject":"ALAB"},"financial_history":{"ticker":"ALAB","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":79872000.0,"revenue_yoy_pct":null,"gross_margin_pct":73.47,"operating_margin_pct":-75.36,"net_income":-58345000.0,"diluted_eps":-0.447253,"free_cash_flow":-39771000.0,"fcf_margin_pct":-49.79,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":115794000.0,"revenue_yoy_pct":44.97,"gross_margin_pct":68.94,"operating_margin_pct":-25.47,"net_income":-26257000.0,"diluted_eps":-0.172174,"free_cash_flow":-15477000.0,"fcf_margin_pct":-13.37,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":396290000.0,"revenue_yoy_pct":242.24,"gross_margin_pct":76.38,"operating_margin_pct":-29.29,"net_income":-83421000.0,"diluted_eps":-0.64,"free_cash_flow":102431000.0,"fcf_margin_pct":25.85,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":852525000.0,"revenue_yoy_pct":115.13,"gross_margin_pct":75.69,"operating_margin_pct":20.34,"net_income":219134000.0,"diluted_eps":1.22,"free_cash_flow":281762000.0,"fcf_margin_pct":33.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/ALAB/ALAB_Q2_2026_Earnings_Call_20260804.md）

# Q2 2026 Earnings Call
2026-08-04

Q2 2026 Earnings Call
Astera Labs, Inc. | Earnings Calls | 2026-08-04
Operator (Operator)
Good afternoon. My name is Holly, and I will be your conference operator today. At this time, I would
like to welcome everyone to the Astera Labs Q2 2026 Earnings Conference Call. [Operator Instructions]
Thank you. I will now turn the call over to Leslie Green, Investor Relations for Astera Labs. Leslie, you
may begin.
Leslie Green (Executives)
Thank you, Holly, and good afternoon, everyone, and welcome to the Astera Labs Second Quarter 2026
Earnings Conference Call. Joining us on the call today is Jitendra Mohan, Chief Executive Officer and
Co-Founder; Sanjay Gajendra, President and Chief Operating Officer and Co-Founder; and Desmond
Lynch, Chief Financial Officer.
Before we get started, I would like to remind everyone that certain comments made in this call today
may include forward-looking statements regarding, among other things, expected future financial
results, strategies and plans future operations and the markets in which we operate. These forward-
looking statements reflect management's current beliefs, expectations and assumptions about future
events, which are inherently subject to risks and uncertainties that are discussed in detail in today's
earnings release and the periodic reports and filings we file from time to time with the SEC, including
the risks set forth in our most recent annual report on Form 10-K. It is not possible for the company's
management to predict all risks and uncertainties that could have an impact on these forward-looking
statements or the extent to which any factor or combination of factors may cause actual results to differ
materially from those contained in any forward-looking statements. In light of these risks and
uncertainties and assumptions, the results, events or circumstances reflected in the forward-looking
statements discussed during this call may not occur, and actual results could differ materially from
those anticipated or implied. All of our statements are based on information available to management
as of today, and the company undertakes no obligation to update such statements after the call, except
as required by law.
Also during this call, we will refer to certain non-GAAP financial measures, which we consider to be
important measures of the company's performance. For example, the overview of our Q2 financial
results and Q3 financial guidance refer to various non-GAAP financial measures. These non-GAAP
financial measures are provided in addition to and not as a substitute for financial results prepared in
accordance with U.S. GAAP. A discussion of why we use non-GAAP financial measures and
reconciliations between our GAAP and non-GAAP financial measures and outlook are available in the
earnings release we issued today, which can be accessed through the Investor Relations portion of our
website.
With that, I would like to turn the call over to Jitendra Mohan, CEO of Astera Labs. Jitendra?
Jitendra Mohan (Executives)

Thank you, Leslie. Good afternoon, everyone, and thanks for joining our second quarter conference call
for fiscal year 2026. Today, I'll provide an update on AI infrastructure market trends, our Q2 results
and recent announcements. I'll then turn the call over to Sanjay to discuss Astera Lab's long-term
growth profile. Des will then cover our Q2 financial results and Q3 guidance.
Since our last earnings call, investment in AI infrastructure has continued to accelerate. Multiple
industry forecasts now point to hyperscaler AI and cloud infrastructure spending in 2027 reaching into
the $1 trillion range with sovereign AI initiatives, inference workloads and enterprise adoption
expanding globally. These secular trends are increasing the need for intelligent connectivity and
expanding our long-term growth opportunity.
Astera Labs delivered outstanding results in Q2 with record revenue of $392.4 million, up 27%
sequentially and up 104% year-over-year. This strong performance was driven by broad-based strength
across our entire product portfolio, reflecting the diversification of our business as we continue to win
new designs across multiple customers and product categories.
PCIe 6 momentum further accelerated in Q2, representing more than 50% of our total revenue driven
by both Scorpio AI Fabric Switches and Aries Retimers. This milestone demonstrates the maturity and
scale of our Gen 6 portfolio and clear market leadership.
On the AI fabric front, Scorpio delivered significant growth in Q2. High-radix Scorpio X-Series has
entered volume production and will continue to scale materially in the second half of this year. We
expect Scorpio to become our largest product family in Q3, which is 1 quarter ahead of our prior
expectations, marking an important strategic milestone.
We are now shipping multiple configurations of Scorpio X-Series into scale-up applications to our
initial customers, and we remain on track to ship Scorpio X-Series to additional customers by year-end.
Scorpio P-Series also continued to expand across multiple customers with new shipments to
hyperscalers and AI infrastructure providers.
These programs are currently in preproduction and are expected to ramp more meaningfully in 2027.
We're also closely engaged with our customers to support their future system architectures with
purpose-built AI fabrics, including next-generation PCI Express and UALink protocols. Upcoming AI
systems will employ more complex switching topologies to enable larger XPU cluster sizes and higher
bandwidth. These designs are expected to drive a material increase in our silicon dollar content per
XPU.
To summarize, our Scorpio Fabric Switch family is well positioned for a multiyear growth cycle driven
by the following factors: first, higher dollar content per XPU due to greater attach rate and increased
capabilities; second, expanding customer base with exceptional traction and design-in pipeline; third, a
greenfield TAM growing rapidly with broadening use cases across training and inferencing.
Turning to our signal conditioning business. Aries delivered record quarterly revenue in Q2, driven by
strong adoption of retimers and gearboxes across scale-up and scale-out topologies in AI and general-
purpose compute platforms. Aries' growth is being fueled by increased AI system deployments,
expanding AI accelerator cluster sizes, greater unit attach rates and higher ASPs associated with the
transition to PCIe 6.
Taurus also provided strong revenue growth in Q2 with increased units shipped across a variety of AI
and general-purpose platforms. During the quarter, we also shipped preproduction volume of our 100

gig per lane Taurus Smart Cable Modules for 800-gig AECs for scale-out applications. We expect
Taurus to continue its growth trajectory in the second half of the year as 800-gig deployments expand,
driving improved attach rates and higher ASPs compared to 400-gig solutions.
We also expanded our Taurus portfolio with a new family of 3.2T Smart Retimers and Smart Redrivers,
supporting 200 gig per lane for next-generation Ethernet and UALink connectivity. These are the
industry's first solutions to enable Smart Swap, giving platform designers the flexibility to choose
between low-power Smart Redrivers and long-reach Smart Retimers without requiring a board
redesign. This architectural flexibility is critical as AI systems evolve rapidly and designers need to
address increasing signal integrity challenges at higher data rates while optimizing system power
consumption. We expect our new high-speed 200-gig per lane retimers and redrivers to double our
Taurus portfolio market opportunity to over $4 billion by 2030.
In CXL, we are seeing renewed momentum as industry is recognizing its potential to unlock
performance and utilization benefits in agentic AI applications. For a growing set of memory-intensive
inference in agentic AI workloads, memory capacity and utilization are increasingly becoming system
constraints and CXL attached memory can offer attractive cost performance relative to local HBM.
As our hyperscaler customers look to address current memory supply and pricing dynamics, we are also
seeing additional opportunities for CXL in mainstream general-purpose server platforms. During Q2,
we closed a new design win with our standard Leo memory controller at a U.S. hyperscaler. Looking
into 2027, we expect to ship both standard and custom Leo CXL memory controllers in volume across
general-purpose compute and AI inferencing applications to 2 U.S. hyperscalers. Activity and
engagement within the CXL ecosystem continues to be robust, and we expect to convert additional
designs in the coming quarters.
In closing, I'm proud of the results we have delivered, and what excites me most is the trajectory ahead
for Astera Labs. Scorpio X-Series is in volume production, and we expect our Scorpio family to become
our largest product category by revenue in Q3, a significant milestone in our evolution as a company. At
the same time, new and existing designs across Aries, Taurus and Leo are contributing to our broad-
based growth.
Intelligent connectivity is now fundamental to the AI infrastructure, and we are winning with the
customers and platforms that define the market. With proven execution, deep customer partnerships
and growing design win visibility, we are confident in our ability to continue outgrowing the market.
With that, let me turn the call over to our President and COO, Sanjay Gajendra, to provide more details
on our product momentum and strategic initiatives.
Sanjay Gajendra (Executives)
Thanks, Jitendra, and good afternoon. I'll walk through our product execution and the expanding
market dynamics that are positioning Astera Labs to capture a significantly larger share of AI
infrastructure spend over the coming years.
Our laser focus on execution and innovation has delivered a purpose-built intelligent connectivity
platform to our hyperscaler customers and is solving sophisticated technology challenges against
aggressive time lines. This results-oriented mindset has helped us strengthen the trust that our
customers and partners place in us. As a result, we continue to unlock many new opportunities in next-

generation designs across multiple customers to rapidly expand our top line growth. Let me deep dive
into some of the key product categories, starting with AI fabrics.
Our broad portfolio of Scorpio switching solutions is perfectly suited to address the increasing
complexity and bandwidth requirements in AI architectures. With leading hyperscalers planning large-
scale training and inference deployments with ever-growing accelerator cluster sizes, our Scorpio X-
Series high-radix Fabric Switch family provides intelligent AI fabric with industry-leading features to
maximize token economics.
These capabilities are driving exceptional demand for our Scorpio X Smart Fabric Switches to address
the $20 billion merchant scale-up switching TAM. Scorpio X-Series differentiation comes from its
intelligence layer, hardware-accelerated Hypercast and In-Network Compute capabilities delivered up
to 2x improvement in collective performance for large-scale training and inference workloads.
These capabilities are implemented through our COSMOS software platform, which now extends
beyond basic fleet management functionality to enable dynamic traffic shaping and advanced real-time
performance management. And we are not stopping here, drawing on our multigenerational
partnerships with customers and the lessons learned from deployments at scale, we are building an
ambitious road map for our scale-up smart fabric switches.
Our Scorpio road map is closely aligned with our customers' next-generation XPU architectures,
enabling more complex topologies, larger cluster sizes and higher bandwidth. Looking ahead, we expect
the content opportunity for Scorpio X-Series solutions alone to grow well beyond $1,000 per XPU in
future generations of AI platforms.
Scorpio P-Series momentum also remains very strong, with both early stage and production
deployments expanding across multiple AI platforms. We are shipping Scorpio P-Series to several
customers to enable high-speed connectivity across AI networking applications. Over the long term, we
aim to proliferate Scorpio P-Series across a broader set of applications spanning modular AI servers,
disaggregated KV Cache appliances, storage platforms and enterprise-level servers.
On signal conditioning, Aries delivered record quarterly performance in Q2 and is well positioned for
sustained growth over the long term. PCIe 6 retimers and gearboxes have become critical infrastructure
for AI servers where signal integrity directly determines whether systems achieve rated performance.
Aries established itself as a gold standard across major XPU and CPU platforms for PCIe 5, and this
position has continued for PCIe 6. We continue to invest in our customers' technology road maps, and
we expect to have PCIe 7 solutions ready to meet their time lines.
Taurus is also expected to deliver strong long-term growth propelled by 800-gig deployments for AI
scale-out networks in the near term and 1.6T and 3.2T-based systems over the long term. We are
pleased to report that Taurus has entered preproduction ramp for 400 gig per lane in Q2, which will
support platforms utilizing 800-gig links. Our Taurus portfolio expansion supporting 200 gig per lane
for 1.6T and beyond positions our road map through the next Ethernet generation and the forthcoming
ramp of UALink driving continued content gains and above industry growth for the Taurus product
family.
Moving to UALink. The consortium's 2.0 specification validates our architectural approach. UALink 2.0
codifies In-Network Compute, advanced RAS features and 200-gig SerDes as next-generation scale-up
fabric requirements. These directly align with our investment areas. We remain engaged with lead
customers and ecosystem partners to enable UALink deployments supported by our upcoming fabric

and signal conditioning solutions. We are on track to deliver UALink-enabled Scorpio X-Series scale-up
switches in 2027.
Optical connectivity represents a substantial expansion vector with the potential to unlock tens of
billions of dollars of additional market opportunity beyond our current copper connectivity TAM. Over
the past 2 years, we have assembled capabilities spanning analog and mixed-signal design, DSP,
electronic and photonic IC integration, and optical packaging through organic investment and the
aiXscale acquisition. This enabled us to deliver complete optical engines in addition to optical
components.
Our optical strategy unfolds in 3 phases. First, high-density fiber attach solutions leveraging our
aiXscale core technology enables up to 50-meter fiber connectivity with ultra-low latency. Our initial
opportunity with a Tier 1 AI platform provider is expected to enter volume production in 2027. Second,
near packaged optics, or NPO, chipsets enabling multi-rack scale-up clusters via optical links are also
targeted for 2027 production. Third, fully integrated Scorpio X-Series Fabric Switches with CPO optical
engine module represents our longer-term road map for 2028 and beyond, supporting larger fabric
domains with terabits per second optical I/O per switch.
Beyond standard products, we continue to make solid progress with our custom solutions. The
increasingly diverse XPU landscape and workloads are driving demand for custom connectivity
solutions. We are executing across multiple vectors with custom solutions for hybrid rack architecture,
including NVLink Fusion-based designs and separately, custom Leo memory controllers in specialized
interface applications. We expect initial shipments for these custom design wins to commence in 2027.
We're also engaged with multiple customers on additional high-value custom connectivity
opportunities to deliver end-to-end purposeful silicon solutions. Together, these design wins and active
opportunities validate our capability to deliver differentiated custom silicon and represents a
multibillion-dollar incremental opportunity over time.
Overall, our platform philosophy, which we call AI Your Way reflects our strategy. Rather than
prescribing a single architecture approach, we provide the broadest portfolio of connectivity solutions
that let customers deploy AI infrastructure optimized for their specific workloads, whether that's
standards-based or custom or copper or optical interconnects and scale-up or scale-out connectivity
across a plethora of standards. This architectural flexibility is becoming a competitive advantage as the
market diversifies.
To summarize, Astera Labs has hit another important inflection point with Scorpio high-radix AI
fabrics reaching volume production. This marks our evolution to a complete AI fabric infrastructure
provider extending beyond signal conditioning and memory connectivity solutions. Our expansion into
optical interconnects and custom solutions further broadens our addressable market in 2027 and
beyond.
With that, let me turn over the call to Des to walk through our Q2 financial results and Q3 guidance in
more detail.
Desmond Lynch (Executives)
Thank you, Sanjay, and good afternoon, everyone. Today, I will review our Q2 financial results and then
discuss our Q3 guidance, both presented on a non-GAAP basis. We delivered outstanding second
quarter results with record revenue of $392.4 million, up 27% sequentially and up 104% year-over-

year. Growth was broad-based across our AI fabric and signal conditioning portfolios led by PCIe 6
products and the initial production ramp of Scorpio X-Series.
Our Scorpio product family delivered a strong Q2. Scorpio P-Series momentum continued during the
quarter, driven by the scaling of existing customer deployments and the early ramp of new programs
into production. Scorpio X-Series also grew strongly as we began shipping initial production volumes
across a variety of radix configurations. Aries revenue reached a new quarterly record, driven by strong
PCIe 6 retimer adoption across both scale-up and scale-out applications. Overall, revenues from PCIe 6
across our AI fabric and signal conditioning portfolios represented more than 50% of total company
revenue in Q2, up from 1/3 in Q1.
Taurus revenue also grew strongly in Q2, driven by increased unit shipments across both AI and
general-purpose compute platforms.
Non-GAAP gross margin for the second quarter was 73.7%, above our guidance of 73%. Non-GAAP
operating expenses for the second quarter were $135.8 million, up 10% sequentially, reflecting
continued investment in our road map. Non-GAAP operating margin for the second quarter was 39.1%,
up 290 basis points from Q1, driven primarily by strong revenue growth and the resulting operating
leverage.
For the second quarter, interest and other income was $12.1 million. Our non-GAAP tax rate was 12%
and non-GAAP net income was $145.8 million, resulting in non-GAAP diluted earnings per share of
$0.80, an increase of more than 30% from Q1. We ended the quarter with cash, cash equivalents and
marketable securities totaling $1.25 billion, up $68.5 million from Q1, driven by cash from operations
of $87.7 million.
Now turning to our outlook for the third quarter. We expect revenue to be in the range of $540 million
to $560 million. At the midpoint, this represents 40% sequential growth driven by the transition of
Scorpio X-Series to volume production, continued strength in Aries PCIe 6 Retimers and preproduction
shipments of Taurus solutions supporting 100 gigabits per lane for 800-gigabyte Ethernet.
As Jitendra mentioned, we expect Scorpio to become our largest product line by revenue in the third
quarter, marking an important milestone in our journey from smart signal conditioning products to
mission-critical AI fabric solutions. This milestone reflects the progress we have made over the past
several quarters as Scorpio X-Series transitions to volume production.
We expect third quarter non-GAAP gross margin to be approximately 72%. We expect third quarter
non-GAAP operating expenses to be between $156 million and $160 million. Our non-GAAP operating
margin is expected to be approximately 43%, up 400 basis points sequentially, which reflects
significant operating leverage as our revenue expands.
Interest and other income is expected to be approximately $12 million, and we expect our non-GAAP
tax rate to be approximately 12%. We expect our Q3 diluted share count to be approximately 185
million shares outstanding. Overall, we expect non-GAAP fully diluted earnings per share to be between
$1.16 and $1.21.
In closing, Q2 was an excellent quarter with strong execution, driving record revenue and expanding
operating leverage. Our strong Q3 guidance reflects continued momentum and confidence in sustained
growth across both our AI fabric and signal conditioning portfolios. We will continue to invest

strategically to capture the substantial opportunity ahead while maintaining strong profitability and
driving long-term value to our stockholders.
This concludes our prepared remarks. I will now turn the call back to our operator to begin Q&A.
Operator?
Operator (Operator)
[Operator Instructions] Your first question comes from the line of Harlan Sur with JPMorgan.
Harlan Sur (Analysts)
Great execution by the team. It's great to see the volume production ramp of your Scorpio X scale-up
fabric switching solutions here in the third quarter. I think in the press release, you said that Scorpio X
ramp would be led by your newer 320-lane products. I think that's with one hyperscaler customer,
right? You have another hyperscale cloud customer that is targeted to ramp your lower-radix Scorpio X
product family as well. Is that more of a Q4 high-volume ramp? And then with the strong ramp in Q3, is
Scorpio X revenues going to exceed Scorpio P revenues this quarter? Or is that still looking to be more
like a Q4 time frame?
Sanjay Gajendra (Executives)
Yes. So thanks, Harlan. So a couple of points. First, the Scorpio X-Series has been gaining tremendous
amount of interest in the market. So we have started shipping the parts for preproduction for multiple
customers starting this quarter. We do expect Q3 for -- at least for a lead opportunity and lead
customer to ramp to high-volume production in Q3 and essentially taking over the -- or surpassing the
revenue from Scorpio P-Series, so which should give you an idea of the value that we bring in scale-up
use cases. We do expect to ship to revenue for additional customers on Scorpio X by end of the year.
So in general, what I would say is that there's been an exceptional traction that we're seeing, both for
Scorpio X and P. X tends to be more tied to scale-up and various different configurations. P goes to a
multitude of opportunities. But overall, it's been great to see how the customer base is seeing the value
that we deliver with our Scorpio family. And like we noted in the call, Q3 onwards, we expect Scorpio as
a family to be the largest product line within the company.
Operator (Operator)
Your next question comes from the line of Blayne Curtis with Jefferies.
Blayne Curtis (Analysts)
Great results. I actually -- I know there's going to be a lot on Scorpio, but I want to ask on the Aries
product. You said record revenue. I think when you gave initial outlook, it was directionally growth. I
think people had pretty low expectations. Just kind of curious if you could talk about the drivers within
Aries. And then as you look to kind of the next generations of AI servers, are you seeing -- what kind of
design traction are you seeing and retimer attach in those systems?
Sanjay Gajendra (Executives)
Yes. So 2 parts to that. One is, again, Scorpio 5, which is our Gen 5 portfolio that's been around, I want
to say, definitely continues to expand especially as we're seeing inference-based applications start
showing up. So that's driving a new wave of growth, is how I would put it.

Aries 6, which is for Gen 6 supporting the higher data rate, the 64 gigabit per second, obviously, that is
-- comes in with higher attach rate and going into several new platforms. And also, there are other use
cases around the cabled application and so on.
So overall, like we've always said, the retimers is a socket that somewhat keeps on giving in the sense
that you need it for a variety of use cases. If anything, the surprise is how long Gen 5 has continued, and
given that there is a new set of use cases opening up for inference, all of those are contributing to help
us achieve a new record on the Aries portfolio.
And by the way, we expect this trend to continue as new Gen 6 platforms and GPUs are being
developed. So this is not a trend that will stop. And then, of course, then we move on to Gen 7, and you
can expect some of the cycle to continue for a long time.
Operator (Operator)
Your next question comes from the line of Joe Moore with Morgan Stanley.
Joseph Moore (Analysts)
You mentioned UALink in your road map there. Can you talk a little bit about that road map? And do
you see, I guess, a transition from PCIe to UALink? And how broad do you expect the customer
adoption to be there?
Jitendra Mohan (Executives)
Joe, thank you for the question. Yes, we continue to see a lot of interest in UALink for scale-up
networking. As we mentioned during the prepared remarks, the ecosystem is evolving. We have new IP
vendors coming online, new tools coming online. Some of the other vendors have also introduced their
own products or announced their own products. That kind of all points to a nice, vibrant ecosystem.
From a customer standpoint, we continue to stay engaged with our customers. There is continuing
interest in UALink. A lot of it is actually driven by not only the additional throughput that UALink
brings but also because of the low latency that UALink will deliver compared to some of these other
protocols.
So we find a lot of traction for that in inferencing applications, and the throughput and the latency and
the open ecosystem is definitely continuing to drive the traction from our customers. We are completely
plugged in, in terms of the development cycle for UALink. We plan to intercept the XPUs that are on
track to be released in 2027 with our own UALink solutions. And as we have discussed, we want to
come in here with a full portfolio of devices, which would be anchored around our switch platform and
then also providing signal conditioning solutions, both for copper and optical. In fact, we recently
introduced our Taurus family, which supports UALink 200 gig per lane line rates.
So it's all looking very good. We continue to stay completely engaged. And as things move from the PCI
Express generation to UALink, we do expect the dollar content per XPU to increase, and that's going to
be a favorable trend for us.
Operator (Operator)
Your next question comes from the line of Tore Svanberg with Stifel.
Tore Svanberg (Analysts)

Congratulations on the strong results. You talked about new software for the Scorpio X deployment. I
think you even talked about really improving efficiency, tokenomics and so on and so forth. Can you
maybe elaborate a little bit on that? And I'm especially curious, is that new software is also lending you
more new customers? Because I assume that's something that's going to be very, very beneficial as they
launch their switch fabrics.
Jitendra Mohan (Executives)
Yes. Sanjay mentioned, Tore, there is exceptional traction from our new customers for the new software
devices that we introduced. Part of it comes just because of the fact that we have higher radix and
higher lane count; and therefore, we can connect more XPUs to the switch.
But a lot of it is also stemming from the advanced capabilities that we built in. And I think this is what
you refer to when you talk about software, which is the In-Network Compute as well as Hypercast. Both
of these are very important technologies that really set us apart and enable very low-latency inferencing
as well as very high efficiency for In-Network Compute, almost 2x improvement in the collective
operations that are required for training.
And all of these are hardware-based features, but they are enabled through software and this software
resides in our COSMOS platform. And so while previously, COSMOS was mainly responsible for
optimization, telemetry, diagnostics, now we are becoming part of the orchestration layer. And the
XPUs are talking directly to this -- our COSMOS platform to run the workload, and this drives a lot
more stickiness into our solution. Many customers that has adopted our platform in this generation will
continue to use this for the next generation. It's the easiest thing for them to do. And we continue to
support these type of advanced capabilities in our current devices, and we'll carry them forward for the
next devices -- next-generation devices as well.
Operator (Operator)
Your next question comes from the line of Natalia Winkler with UBS.
Natalia Winkler (Analysts)
I wanted to follow up on the CXL opportunity. So you guys mentioned the CXL controller and kind of 2
new hyperscalers that you will be ramping in 2027. But curious how that CXL opportunity plays out for
the switching content as well. And how do you see that market kind of progressing from here?
Sanjay Gajendra (Executives)
Yes, I think it was about time isn't it. I think it's finally great to see some traction back on CXL. As you
know, we have been investing in the technology for quite a while now, and it's great in some ways
because we understand exactly what is needed, both from a hardware and software standpoint.
So now we see actually 3 main use cases. One is largely driven around sort of the memory market
dynamics, people wanting to find alternates to the availability or the high cost of memory today. And
they're trying to do that through CXL and try to leverage the fact that you can stick different kinds of
memory behind a CXL bus. The second one, which is very exciting for us is the GPU attach or
accelerator attach where, combined with our KV Cache acceleration type of function, we're able to do
unique things that fundamentally are improving the latency and performance for inference
applications. The third one is something that we've been talking for a while, which is general compute

or HPC application, where for use cases like SAP, where you need a high memory or memory intensity
workloads, the CXL provides a way of adding more memory to the CPU.
So those are the 3 main applications or dynamics that we see. And for us, what we are tracking is, of
course, multiple design wins and opportunities at this point with most of them in qualification or early
stage this year and getting into high-volume production in 2027.
So we do see this trend to continue, by the way, and we are investing heavily in coming out with
technologies and capabilities to solve the memory wall problem and the memory availability problem in
some ways given where the market is on that front. So overall, we are positive and we are continuing to
invest.
Operator (Operator)
Your next question comes from the line of Sean O'Loughlin with TD Cowen.
Sean O'Loughlin (Analysts)
Congrats on another great set of results. And thanks for letting me hop on. I wanted to ask maybe a
bigger picture question on the product portfolio, especially as we start to think about optics really
starting to be something that sees at-scale deployment within most investors' time horizons. I guess the
question is, as I think about UALink NPO or CPO switch, you have an optics-based Ethernet PHY, is
there a fundamental reason why like Taurus, over time, couldn't also transition that physical media
dependent layer to one that's based on fiber rather than copper? And does that end in effect extend the
assumed lifetime revenue of what maybe most of us are thinking of as an inherently copper-based
solution today? Apologies if I'm leading the witness here a bit, but just wanted to get your thoughts on
that.
Jitendra Mohan (Executives)
No, no, that's a great question. So let me comment on that. So first of all, we do fully expect copper and
optical to coexist. As you know, most of the scale-up connectivity today is done in copper, and our
customers are asking us to continue to push that forward, and we will continue to do that. And as these
data rates go up and the signal integrity challenges increase, there is definitely room for additional
products and additional product categories, just like we announced our Taurus 200-gig both retimers
and redrivers in support of these applications.
Now we do expect that for this generation and the next generation the scale-up within a rack will
continue to be copper. But then as these cluster sizes grow and the data rates increase, optical will
definitely play an increasingly important role as you start connecting these racks to each other and
cluster size expands from maybe 1 or 2 racks to 4, 5 or even a larger number of racks.
And we are very well positioned to play our part in this developing market segment. We are very closely
engaged with our customers. We understand when they want to deploy these increased cluster sizes.
And we expect that the first deployment will happen with NPO solution. As we go from copper in
addition to copper to NPO solution, our dollar content per XPU or per link actually goes up. So we
definitely welcome this change.
Overall, if you look at the optical market, it's several tens of billions of dollars in TAM that gets
unlocked. Once NPO gets deployed and data rates continues to increase, we will start to see CPO getting

deployed. So we look at it as 2027 being the year where NPO gets deployed and then 2028 and beyond
is when CPO gets deployed.
From a product development standpoint, we are very comfortable. We started investing in this a couple
of years back. We have a team of engineers working on the EIC solution, which is the electrical
component. We have a team of engineers that is working on the silicon photonics. And of course, late
last year, we acquired aiXscale Photonics, which gives us the ability to develop a connector. And put all
of these things together. We have now the ability or we will have the ability to have full optical engines,
which will eventually lead to not only optical links and Taurus-like components as you pointed out, but
actually a fully optically enabled Scorpio switch.
So we are really looking forward to that, supplying both that optically enabled Scorpio switch as well as
the individual components that make up the full optical link. And that's a tremendous opportunity for
us in addition to what we have at copper.
Operator (Operator)
Your next question comes from the line of Papa Sylla with Citigroup.
Papa Sylla (Analysts)
Congrats on the impressive results. So I wanted to double click on the content per accelerator. I think
when you initially kind of IPOed, it was more around $50 to $100 for accelerator and over the past
quarters or so, you went to $1,000 plus. And Sanjay, you mentioned today Scorpio X alone could be
well over $1,000 per accelerator.
So I'm wondering if that $1,000 plus for Scorpio X, is it a pre-UALink metric or perhaps if you can
provide color on the path to that $1,000 plus per accelerator for Scorpio X. Finally, maybe tying
everything together, if you can speak more generally on your content per accelerator currently and
where do you see that going over the next 2, 3 years.
Sanjay Gajendra (Executives)
Yes, good question. I think this is a fundamental question that you asked, and it's a very important
focus for us, which is how do we keep ensuring that our long-term business continues to grow and we
are able to sustain the kind of growth that we're able to deliver.
And it really, like you highlighted, comes down to how can we keep increasing the dollar content that
we can get per XPU attach. Like you correctly noted, we started with small numbers when -- IPO time.
Now we see our business contributing multiple thousands of dollars per XPU with the aiXscale or scale-
up switch itself offering over $1,000 per XPU.
And this is already starting to happen, of course, with the high-radix switch that we are shipping right
now. But at the same time, this is just the beginning of it because when you start adding several other
features that are important in terms of optical, for example, or adding more signal conditioning because
of the higher speed and the higher attach rate, we do believe that this number will continue to scale up.
And that is what we are focusing our investment right now, which is how do we ensure, a, we keep
increasing the dollar content we get per XPU targeting multiple thousands of dollars; and b, how do we
continue to keep diversifying our business, adding more hyperscalers around the anchor socket that we
have, which is a scale-up switch, and continue to grow significantly above where the market is.

Operator (Operator)
Your next question comes from the line of Tom O'Malley with Barclays.
Robert Smith (Analysts)
This is Trip Smith on for Tom O'Malley. Appreciate the question and very nice results. I was just
curious about how we should think about the Scorpio gross margins now that it's becoming a bigger
part of the business. And what are the puts and takes there for gross margins looking out? And I believe
you still have the Amazon warrant impact. So I just wanted to double check on that and how we should
be modeling that over the next few quarters.
Desmond Lynch (Executives)
Thanks for the question. It's Des here. As we mentioned in the prepared remarks, we do expect our Q3
gross margins to be approximately 72%. And really as our portfolio continues to sort of diversify, we
continue to see a wider range of gross margins with the main impacts being silicon versus module
revenue mix and the different use cases associated with our switching portfolio.
On Scorpio across both P- and X-Series, we do have a wide range of margins, really driven by use case
and lane count utilization. But I would say, on average, Scorpio across all use cases has an average
margin profile broadly in range with our sort of corporate gross margins. In any given quarter, this mix
can sort of change.
But what I would say on the switching side is that we are going after large opportunities. And as the top
line continues to scale, we'll see the gross margin dollars flow through and contribute to the bottom
line. We clearly saw that in our Q2 results and also our Q3 guidance from here. But really, given the
broadening of the portfolio, I would expect our gross margins continue to trend towards a long-term
target of 78% from here.
Operator (Operator)
Your next question comes from the line of Ananda Baruah with Loop Capital Markets.
Ananda Baruah (Analysts)
What's a useful way to think about the contribution that the China hyperscale can make across the
portfolio as you continue to introduce the new products and move up from generation to generation?
Jitendra Mohan (Executives)
Ananda, that's a good observation. In China, as you can imagine, the open protocols are quite popular,
which includes PCI Express, Ethernet and increasingly, UALink. So we definitely see that as a good
market, not nearly as big as what we have here. But certainly, there is a lot of interest, and we are
engaging with the customers there with our PCI solutions as well as our Taurus-based Ethernet
solutions. So in aggregate, that can be a very promising opportunity, especially as PCI Express is the
nervous system of servers and probably the best way to connect many add-in card format GPUs
together to deliver good inferencing capabilities.
Ananda Baruah (Analysts)
I appreciate -- and is it a way that can be noticeable on the P&L over time?

Jitendra Mohan (Executives)
I think it will be, in an absolute scale, yes, our revenues from China will continue to increase. However,
we do expect the rest of the world to increase even faster. So as a percentage of total revenue, they will
continue to be in the single digit.
Operator (Operator)
Your next question comes from Suji Desilva with ROTH Capital Partners.
Sujeeva De Silva (Analysts)
Congrats on the results here. I'm curious, you talked about the software supporting telemetry and now
orchestration gaining more kind of functionality there. Is there kind of a soft line where you might cross
over to helping the XPU itself with some of the functionality as a co-processor? Or would you draw sort
of a straight line there as connectivity versus that eventual trend in memory compute and things like
that?
Jitendra Mohan (Executives)
Yes, very good point. No, actually, that is what I was trying to say when I answered the question earlier
that with the advancement of the In-Network Compute and Hypercast features in our latest Scorpio
320-lane device, we are indeed crossing over that line where the XPU is directly talking to the switch to
orchestrate the workloads to reduce the latency and increase the throughput for both inferencing as
well as training workloads.
So that's a very important development for our COSMOS platform, where not only are we doing the
traditional optimization, customization, diagnostics and telemetry, but we are really helping to improve
the workload and directly improve the utilization of the GPUs that are connected to our switch. So it's a
very important development. And as I mentioned, it makes our solution -- software solution more
powerful and a lot more sticky as customers design in our current generation of switches and then look
to upgrade them in the future.
Operator (Operator)
Your next question comes from the line of Simon Leopold with Raymond James.
Jeffrey Koche (Analysts)
Jeff Koche in for Simon. Maybe you could just talk qualitatively about your end market concentration.
How is the trend in the quarter? How do you expect it to trend over the next, I guess, through 2027,
especially with the new launches?
Desmond Lynch (Executives)
Yes, it's a really good question. What I was really pleased to see in our sort of first half is that really it
has been the broad-based strength across our sort of portfolio. And really looking at our sort of drivers,
I would say Aries delivered a record quarterly revenue in Q2 and remained our largest product line,
really supported by the ongoing transition to PCIe 6 across both scale-out and scale-up connectivity.
And I do expect Aries to continue to grow in Q3 and beyond.

As we mentioned in the prepared remarks, Scorpio continues to show strong momentum in Q2, really
driven by X- and P-Series. And as we mentioned, we do expect to see Scorpio becoming our largest
product line in terms of revenue as a result of the production ramp of the high-radix solutions in Q3.
Taurus also continues to show nice growth, really supported by AI and general purpose sort of
platforms. And I do expect to see further growth in the third quarter driven by the strong base of the
400 gig demand as well as the early contribution to the 800 gig as well.
And I think, as Sanjay has sort of mentioned, we continue to see sort of strong progress on the Leo CXL
products, and we continue to see some revenue here in the back half of the year, which will ramp more
materially into sort of '27. As we look into '27, we'll continue to see further opportunities on the optical
and custom sort of side, but we're really pleased with the overall performance of the portfolio and the
continued diversification.
Operator (Operator)
Our next question comes from Karl Ackerman with BNP Paribas.
Karl Ackerman (Analysts)
Jitendra, Scorpio X is ramping significantly in the second half of this year, largely driven by the product
transition at your main customer. But can you discuss the breadth of customer wins including a
growing mix of neoclouds and whether your Scorpio X opportunity extends across both liquid-cooled
and air-cooled servers?
Sanjay Gajendra (Executives)
Yes, I'll take this question. This is Sanjay here. So like we've said, the demand for Scorpio X and Scorpio
P has truly been exceptional. We have over 10 customers engaged on the Scorpio X itself. Many of these
opportunities are either getting into preproduction or getting deeper into the qualification cycle. So to
that standpoint, we are already shipping Scorpio X to multiple customers right now as they get ready
for their own internal qualification cycle, and we do expect that we'll have additional customers
ramping to production towards the end of this year, early next year based on the progress that they can
make.
So this trend is something that, of course, given the features and capabilities that we have, especially
with the 320 lane, we're able to unlock several things when it comes to inference type of applications.
So there are several unique things that we're able to achieve. And all of these are contributing to
diversifying our customer base on Scorpio X. And like I noted on Scorpio P, it's truly broad-based
because the P-Series is going to go into standard PCIe switching application. So from storage to
networking and some of the scale-out use cases, we have several design wins and design-ins that are
ramping to production. So in general, I want to say Scorpio family has taken off in a very positive way
for us, and we intend to add more customers and more revenue growth in the second half through
2027.
Jitendra Mohan (Executives)
If I may just add to that, the -- it is -- the chip itself supports both liquid cooling and air cooling. In fact,
we do have customers that are designing it for both of them. And your point about the neocloud is also
very valid because people, when they start to deploy these solutions for especially inferencing

applications, sometimes they can do that without using a full rack level solution. And so we do see this
increasing use case of enterprise customers and neoclouds looking at solutions that are based on
Scorpio as a scale-up and using add-in card form factor GPUs to deliver good inferencing TCO.
Sanjay Gajendra (Executives)
And also maybe to add one more point that is somewhat lost is even with the lead hyperscaler we have,
there are multiple platforms where we are designed in. It's not like there is just one, right? So I think
that's a nuance that needs to be considered as you look at our business.
Operator (Operator)
There are no further questions at this time. I will now turn the call back over to Leslie Green for closing
remarks.
Leslie Green (Executives)
Thank you, everyone, for your participation and questions. And please refer to our Investor Relations
website for information regarding upcoming financial conferences and events. Thanks so much.
Operator (Operator)
This concludes today's conference call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ALAB_Q1_2026_Earnings_Call_20260505.md
- 2026-05-05｜CFO｜guidance：Q2 營收指引 3.55–3.65 億美元，季增 15–18%（原話："$365 million, up 15% to 18% sequentially"）
- 2026-05-05｜CFO｜margin：Q2 non-GAAP 毛利率指引約 73%，含客戶認股權證協議的約 200bp 非現金影響（原話："estimated 200 basis point noncash impact"）
- 2026-05-05｜CFO｜margin：Q1 non-GAAP 毛利率 76.4%，季增 70bp（原話："gross margin for the first quarter was 76.4%"）
- 2026-05-05｜CFO｜margin：Q1 毛利率改善歸因於訊號調節產品硬體銷售占比下降（原話："driven by a lower mix of hardware sales across our"）
- 2026-05-05｜CFO｜guidance：Q2 non-GAAP 營運費用指引 1.28–1.31 億美元（原話："non-GAAP operating expenses to be between $128 million"）
- 2026-05-05｜CFO｜guidance：Q2 non-GAAP 稀釋 EPS 指引 0.68–0.70 美元（原話："fully diluted earnings per share to be between $0.68"）
- 2026-05-05｜CFO｜guidance：預期 Scorpio 年底成為最大產品線（原話："will become our largest product line by the end of the year"）
- 2026-05-05｜CFO｜guidance：預期年內 Scorpio X 營收超過 P 系列（原話："expect to see X-Series revenue exceeding P-Series"）
- 2026-05-05｜CEO｜product：Q1 營收 3.08 億美元，季增 14%、年增 93%（原話："up 14% from the prior quarter and up 93% versus Q1 of last"）
- 2026-05-05｜CEO｜product：PCIe 6 業務占總營收超過三分之一（原話："expanding to more than 1/3 of our total revenue"）
- 2026-05-05｜CEO｜product：矽含量機會超過每 XPU 1,000 美元（原話："silicon dollar content opportunity beyond $1,000 per XPU"）
- 2026-05-05｜CEO｜product：320 通道 Scorpio X 已開始出初期量（原話："now shipping initial volumes of our new 320 lane Scorpio X"）
- 2026-05-05｜CEO｜commitment：320 通道 Scorpio X 量產於 2026 下半年放量（原話："production volumes ramping in the second half of 2026"）
- 2026-05-05｜CEO｜customer：Scorpio P 預期年底前開始出貨給至少兩家新增大型超大規模客戶（原話："initial shipments to at least 2 additional major"）
- 2026-05-05｜CEO｜product：光纖耦合器預計 2027 年起量產出貨（原話："we expect to ship in volume starting in 2027"）
- 2026-05-05｜CEO｜product：新獲 KV Cache 卸載客製設計案，2027 出貨（原話："offload application with shipments expected in 2027"）
- 2026-05-05｜CEO｜customer：Microsoft Azure M 系列 CXL 專案目前私測，預期年底全面可用（原話："in private beta now expected to go into general availability"）
- 2026-05-05｜President/COO｜commitment：NVLink Fusion 客製專案預期 2027 開始有實質營收（原話："this will start providing some meaningful revenue in 2027"）
- 2026-05-05｜President/COO｜competition：被問 NVLink Fusion 競爭態勢，答以不被競爭對手新聞稿分心（原話："not get distracted by any competitive press releases"）
- 2026-05-05｜President/COO｜capital_allocation：客製業務採 NRE 等開發付費模式（原話："NREs and other ways of paying for the development"）
- 2026-05-05｜President/COO｜commitment：客製業務將系統性篩選，不接所有機會（原話："We will not take any opportunity that comes our way"）
- 2026-05-05｜President/COO｜risk：管理層點出客製業務可能對單一客戶高度專屬、帶來風險與毛利問題（原話："unique to one customer and with a lot of risk and margin"）
- 2026-05-05｜CEO｜product：Amazon 與 AMD 已表示其 ASIC／GPU 2027 推出，公司準備對接 UALink 交換器（原話："their respective ASIC and GPU will launch sometime in 2027"）
- 2026-05-05｜CEO｜product：UALink 世代產品可收取的價值預期顯著高於 PCIe 交換器（原話："charge for these devices will be substantially higher"）
- 2026-05-05｜President/COO｜commitment：光學時程：CPO 主流部署預計 2028（原話："mainstream deployments for CPO happening in the 2028"）
- 2026-05-05｜CEO｜competition：公司稱與客戶緊密合作建立持久競爭護城河（原話："customer collaborations, creating a durable competitive"）
- 2026-05-05｜CEO｜risk：XPO：目前並非所有客戶要對接（原話："But not all of our customers, at the moment, are"）
- 2026-05-05｜CFO｜risk：供應：業界仍有零星供應挑戰（原話："we continue to see pockets of supply challenges"）
- 2026-05-05｜CFO｜commitment：持續與供應鏈夥伴合作確保 2027 供應（原話："continue to work with our supply chain partners for supply"）
- 2026-05-05｜CFO｜capital_allocation：將持續策略性投資以追求高於產業的成長（原話："We will continue to invest strategically to drive above-"）
- 2026-05-05｜CFO｜capital_allocation：Q1 現金持平，營運現金流 7,460 萬被併購支出抵銷（原話："cash from operations of $74.6 million was offset by cash"）
- 2026-05-05｜CFO｜guidance：2027 年 Scorpio 仍為最大且成長最快業務，Aries 預期仍強勁成長（原話："Scorpio will continue to be our sort of largest"）

### ALAB_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜CEO Jitendra Mohan｜guidance：CEO 重述上季營收 3.92 億美元，Q3 指引中點 5.5 億美元（原話："We guided for $550 million at the midpoint for Q3."）
- 2026-09-09｜CEO Jitendra Mohan｜product：每 XPU 含量從 IPO 時不到 100 美元到現在近 1,000 美元（原話："Now we are already at close to $1,000 of content."）
- 2026-09-09｜CEO Jitendra Mohan｜product：Scorpio X 單獨一個產品線預計每 XPU 含量達 1,000 美元以上（原話："$1,000 or more content on a per XPU basis"）
- 2026-09-09｜CEO Jitendra Mohan｜product：Scorpio X 於 Q2 推出、Q3 進入量產，並出貨給額外客戶（原話："already entering volume production here in Q3"）
- 2026-09-09｜CEO Jitendra Mohan｜guidance：Q3 Scorpio 將成最大產品族，且 Scorpio X 超越 Scorpio P（原話："Scorpio will become our largest product family by revenue"）
- 2026-09-09｜CEO Jitendra Mohan｜commitment：管理層預期多數 Scorpio X 設計導入於 2027 轉為完整 design win 放量（原話："full design wins to ramp in 2027"）
- 2026-09-09｜CEO Jitendra Mohan｜product：Scorpio P 去年前三季占總營收 15%（原話："it was 15% of our total revenue"）
- 2026-09-09｜CEO Jitendra Mohan｜risk：CEO 說明 Scorpio 放量快速部分靠運氣，且公司傾向保守估計認證時間（原話："we do try to be conservative"）
- 2026-09-09｜CEO Jitendra Mohan｜competition：CEO 承認競爭者將進入 Scorpio 市場，並稱非零和（原話："the competition will come. And we welcome that."）
- 2026-09-09｜CEO Jitendra Mohan｜competition：Scorpio P 在 PCIe Gen 6 出貨量最高；此前 PCIe Gen 5 交換器主導者為 Broadcom（原話："shipping this in the highest volume for PCI Express Gen 6"）
- 2026-09-09｜CFO Desmond Lynch｜margin：CFO 稱毛利率目前約中 70% 區間，長期預期往 70% 靠攏（原話："we do see the margins trending down towards 70%"）
- 2026-09-09｜CFO Desmond Lynch｜margin：CFO 說明毛利率受矽 vs 模組組合及 Scorpio X 貢獻影響（原話："Firstly would be the mix of silicon versus module content."）
- 2026-09-09｜CFO Desmond Lynch｜margin：CFO 稱 Scorpio 毛利率與公司平均相當，視用途與 lane 配置而異（原話："our Scorpio margins are in line with our corporate averages"）
- 2026-09-09｜CEO Jitendra Mohan｜product：AMD MI450 初期以乙太網路承載 UALink，因 UALink 交換器尚未問世（原話："UALink switches are not yet available."）
- 2026-09-09｜CEO Jitendra Mohan｜product：CEO 說明支援 scale-up 協定時含量大增，否則僅限 scale-out（原話："then our content really does explode a lot"）
- 2026-09-09｜CEO Jitendra Mohan｜commitment：CEO 表示長期目標是涵蓋完整 scale-up TAM，並已參與 NVLink Fusion（原話："our goal over time is to address the full scale-up TAM"）
- 2026-09-09｜CEO Jitendra Mohan｜product：光學營收預計 2027 起，先從元件級（aiXscale 連接器）銷售（原話："revenue perspective, that will happen in 2027"）
- 2026-09-09｜CEO Jitendra Mohan｜guidance：NPO 初期營收預計 2027 下半年，2028 全年貢獻（原話："initial revenues in the back half of 2027"）
- 2026-09-09｜CEO Jitendra Mohan｜product：CEO 稱 radix 提高時每 lane ASP 反而上升（原話："it actually goes up with radix"）
- 2026-09-09｜CFO Desmond Lynch｜customer：CFO 稱已出貨給所有美國超大規模業者，並預期客戶集中度持續（原話："customer concentration is to be expected from here."）
- 2026-09-09｜CFO Desmond Lynch｜customer：Scorpio X 客戶接洽數由原先 10 家增至高十幾家（原話："That number now today is up into the high teens"）
- 2026-09-09｜CFO Desmond Lynch｜commitment：CFO 預期年底前與 2027 將有數個 Scorpio X 機會轉為 design win（原話："convert several of these opportunities into design wins"）
- 2026-09-09｜CFO Desmond Lynch｜customer：客戶分散化將延續到 2027 之後，同時主要客戶也持續成長（原話："our lead customer will also continue to grow as well."）
- 2026-09-09｜CEO Jitendra Mohan｜product：LEO CXL 取得 KV Cache offload 客製機會，認證中、2027 起放量（原話："That is in qualification now and will start to ramp in 2027."）
- 2026-09-09｜CEO Jitendra Mohan｜competition：NVLink Fusion 與 AWS 原生 UAL 交換器方案相比，每機架營收機會大致相當（原話："it's a wash."）
- 2026-09-09｜CFO Desmond Lynch｜capital_allocation：CFO 稱資本配置聚焦有機與無機投資，並未提及回饋股東（原話："continue to invest both organically and inorganically"）
- 2026-09-09｜CFO Desmond Lynch｜capital_allocation：aiXscale 為小型併購例子，並持續尋找小型併購與 acqui-hire（原話："aiXscale was a great example of that"）

### 問答異常語氣（迴避／改口／保留）
- ALAB_Q1_2026_Earnings_Call_20260505.md｜問：Quinn Bolton 問 KV Cache 客製設計的單位美元含量／規模｜答法：未給數字，稱平台架構仍在定案、'a little bit early'，改談 ASP 不受壓縮
- ALAB_Q1_2026_Earnings_Call_20260505.md｜問：Sebastien Naji 問 320 通道 Scorpio 的 ASP 與通道數是否正相關｜答法：未給 ASP 數字，改談功能組合與每加速器超過 1,000 美元含量
- ALAB_Q1_2026_Earnings_Call_20260505.md｜問：Natalia Winkler 問 NVLink Fusion 的競爭態勢｜答法：未正面回應競爭，改稱專注於真實客戶與應用、不被新聞稿分心

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
{"date":"20260522","verdict":"觀望","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"ALAB 在 PCIe Gen 6 retimer 維持 60%+ 市佔，Scorpio 拓展至 PCIe Switch 領先地位，Aries / Scorpio / Taurus / Leo 4 大產品線並進","columns":{"2Y 驗證點":"Q4 26 Scorpio + Leo + Taurus 合計營收占比 ≥ 30%；H2 26 兩家新 hyperscaler 接收 Scorpio P；Marvell Alaska P 量產規模 &lt; ALAB 30%","5Y 驗證點":"FY28 4 大產品線各占 20-30%（Aries 仍最大但 ≤ 40%）；PCIe Gen 7 retimer sample 給 hyperscaler；UALink 1.0/2.0 採用","10Y 驗證點":"FY30 公司 Revenue $3B+；retimer 全球市佔 ≥ 60%（不論 Marvell 後續追趕）；多產品線結構穩定","具體數字門檻":"4 產品線合計 ≥ $1.2B FY26 (Q1 + Q2 + Q3 + Q4 implied) → $2B FY27 → $2.8B FY28；Aries 占比 ≤ 65%","信息來源":"5/5 Q1 26 earnings call + Excel snapshot 2026-05-20 + Marvell OFC 2026 March 公告","漂移觸發條件":"連 2 季 TTM Aries 占比 &gt; 75% 或 Scorpio + Taurus 占比 &lt; 25% → 削弱（對齊 QC-34/35）"}},{"id":"H2","text":"Marvell / Broadcom PCIe Gen 6 retimer 競爭實質化但 ALAB 維持 6-12 月領先 + 客戶綁定","columns":{"2Y 驗證點":"2026 H2 - 2027 H1 Marvell Alaska P 月 wafer shipment 達 ALAB 30% 之內；無 hyperscaler 公告 dual-source 完全切換","5Y 驗證點":"2028-2029 PCIe Gen 7 spec 公布後 ALAB 仍領先 sample；hyperscaler 至少 3 家維持 ALAB 為 primary supplier","10Y 驗證點":"2030+ ALAB 在 retimer 市佔不低於 50%；如 Marvell 追上至 30%+ → 雙寡占（仍可接受）","具體數字門檻":"Marvell Alaska P 月 wafer shipment 2026 H2 &lt; 30K wafer (vs ALAB 估 100K+)；hyperscaler 維持 ALAB 主供","信息來源":"Marvell investor 2026-03 OFC 發表 + ALAB Q1 26 call commentary + 業界 design win 追蹤","漂移觸發條件":"連 2 季 Marvell wafer shipment 達 ALAB 30%+ → R2 觸發；任一 hyperscaler 公告 dual-source 切換 → 強烈削弱"}},{"id":"H3","text":"Hyperscaler capex 持續高位（2026 $602B → 2027 $1T+），AI Infra TAM 不萎縮","columns":{"2Y 驗證點":"2026 Q4 / 2027 Q1 Mag 7 capex guide 中位 ≥ $700B；AI workload 多元化（training + inference + agent + sovereign）","5Y 驗證點":"2028-2030 AI infra TAM 維持 5%+ YoY growth；sovereign AI / enterprise AI 訂單跟上補位 hyperscaler 邊際放緩","10Y 驗證點":"2030+ AI capex 達 plateau 但維持 $1T+ 年度（即使 hyperscaler 個別停擴，加總穩定）","具體數字門檻":"NVIDIA / Microsoft / Google / Amazon / Meta FY27 capex guide 加總 ≥ $700B；無單一 hyperscaler 砍 capex &gt; 10% YoY","信息來源":"5 家 Mag 7 Q1 26 公司財報 + Goldman Sachs / MS / JPM 2026 capex outlook","漂移觸發條件":"連 2 季 hyperscaler capex 共識下修 &gt; 10% → R3 觸發；NVIDIA/Microsoft 單一公司 FY27 capex 下修 &gt; 15% → 強烈削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"估值修復（mean reversion）：4 週 +40.5% 漂移 + Fwd PE 99x + PEG 2.89 觸發歷史回測 3-6 月 -30% 機率 60%+","columns":{"對應假設":"H1（thesis 不變但估值面）","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"股價回測 BB 中軌 $163 或 W52 $158 進度；Bollinger 位置；4 週滾動報酬","警戒閾值":"連 2 月 Fwd PE 維持 > 90x + 無 EPS 大幅上修 → 估值風險加大"}},{"id":"R2","text":"Marvell 競爭實質化：Alaska P PCIe Gen 6 retimer 已 server vendor 量產 + Structera S 260-lane Q3 26 sample，雙寡占格局形成","columns":{"對應假設":"H2（競爭 / 護城河）","時間尺度":"🔥 中期（4-6 季）","監測指標":"Marvell Alaska P 月 wafer shipment；hyperscaler dual-source 公告；ALAB GM 是否守住 73%+","警戒閾值":"Marvell wafer shipment 達 ALAB 30%+ 或任一 hyperscaler 公告 dual-source 完全切換 → R2 觸發"}},{"id":"R3","text":"Hyperscaler ASIC 化 / 內製 retimer：NVIDIA / Google / AWS 任一自研 PCIe retimer 至量產（CRDO 2025 教訓 - AWS Trainium 3 替換 SerDes）","columns":{"對應假設":"H1 / H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"各 hyperscaler internal silicon roadmap；Annapurna / Google silicon team 動向；ALAB Top 1 客戶占比變化","警戒閾值":"任一 hyperscaler 公告自研 PCIe retimer 量產 → R3 觸發（需 ≥ 50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":297.84,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261013/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
