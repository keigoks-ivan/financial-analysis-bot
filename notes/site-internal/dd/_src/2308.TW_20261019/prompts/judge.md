你是 stock-analyst **v20 判斷 agent**，標的 2308.TW（20261019）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"2308.TW","date":"2026-10-19","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261019/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261019/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_ifrs","label":"營收（IFRS 合併）","value":183.256,"period":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","unit":"NT$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","citation":"公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf"},"note":"市場共識 182.833（Bloomberg，經 KGI 報告），+0.2%"},{"id":"f_kpi1","label":"毛利率","value":35.6,"period":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","citation":"公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf"},"note":"共識 36.4%（經 KGI），低 0.8ppt"},{"id":"f_kpi2_ifrs_non_gaap","label":"營業利益（IFRS，台達電無 non-GAAP 口徑）","value":30.57,"period":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","unit":"NT$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","citation":"公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf"},"note":"共識 33.77（經 KGI），低 9.5%"},{"id":"f_kpi3_ifrs","label":"營業利益率（IFRS）","value":16.7,"period":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","citation":"公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf"},"note":"共識 18.5%（經 KGI），低 1.8ppt"},{"id":"f_kpi4_eps","label":"稅後淨利（歸屬母公司）／EPS","value":9.68,"period":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","unit":"NT$/股（淨利 25.14 十億）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","citation":"公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf；業外收益 4.43 十億（占營收 2.4%）墊高 EPS"},"note":"共識 EPS 9.47（經 KGI），+2.2%"},{"id":"f_kpi6_2026","label":"2026 年資本支出（管理層上調）","value":"65–70","period":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30），法說會表述","unit":"NT$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30），法說會表述","citation":"KGI 2026-07-30 報告 https://www.kgi.com.hk/zh-hk/-/media/files/kgishk/research-reports/tw-reports/delta-electronics_20260730_en.pdf（轉述管理層：上調逾 100 億，原則上 2027–28 仍可能成長）"}},{"id":"f_kpi7_infrastructure","label":"部門營收：Infrastructure（資料中心等）","value":62.938,"period":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","unit":"NT$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","citation":"公司 IR 2Q26 法說會簡報 https://filecenter.deltaww.com/ir/download/calendar/2Q26_Analyst%20Meeting.pdf"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-07-29","period":"2026-07-29","unit":"date","basis":"距今 58 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-07-29"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_2308_tw_gross_margin_pct","label":"2308.TW 毛利率","value":35.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_operating_margin_pct","label":"2308.TW 營業利益率","value":16.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_fcf_margin_pct","label":"2308.TW FCF 利潤率","value":11.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vrt_gross_margin_pct","label":"VRT 毛利率","value":38.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_operating_margin_pct","label":"VRT 營業利益率","value":19.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_fcf_margin_pct","label":"VRT FCF 利潤率","value":25.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":13.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2301_tw_gross_margin_pct","label":"2301.TW 毛利率","value":23.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2301.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2301_tw_operating_margin_pct","label":"2301.TW 營業利益率","value":11.41,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2301.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2301_tw_fcf_margin_pct","label":"2301.TW FCF 利潤率","value":-6.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2301.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5","label":"自由現金流（營運現金流－資本支出）","value":26.9,"period":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","unit":"NT$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"2Q26（季末 2026-06-30，自結財報公告 2026-07-29，法說會 2026-07-30）","citation":"yfinance quarterly_cashflow（營運現金流 43.17、資本支出 16.27，單位十億 NT$）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1640.0,"period":"2026-10-19（RTH 收盤，UTC）","unit":"TWD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-13.23,"period":"2026-10-19（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^TWII","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":37.27,"period":"2026-10-19（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.5,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（40.25 → 40.45）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.97,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（63.71 → 64.33）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.82,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（96.35 → 97.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":40.45,"period":"2026-10-08","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":64.33,"period":"2026-10-08","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":97.14,"period":"2026-10-08","unit":"TWD/share","basis":"Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-1.12,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 40.91 → 40.45（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":52.28,"period":"2026-10-19（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-19（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-19（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.51,"period":"2026-10-19（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-19（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-19（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.34,"period":"2026-10-19（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-19（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-19（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":48.58,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 40.45，分子＝快照價 1965.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.707,"period":"2026-10-19","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-19"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-111877.84,"period":"2026-10-19","unit":"TWD m","basis":"yfinance 最新一季：總債務 74292.72、現金 186170.56（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":2597.54,"period":"2026-10-19","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":4148093.49,"period":"2026-10-19","unit":"TWD m","basis":"市值 4259971.33 ＋ 淨負債 -111877.84","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":776572.09,"period":"2026-10-19","unit":"TWD m","basis":"yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":1098817.94,"period":"2026-10-19","unit":"TWD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":5.34,"period":"2026-10-19","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-19"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-10-19","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-19","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 1635.0 / W52 1557.9 / W104 1021.4 / W250 593.89 / W250 13週斜率 4.51%"},{"id":"f_ma_w52","label":"52 週均線","value":1557.9,"period":"2026-10-19","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-19","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":1021.4,"period":"2026-10-19","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-19","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":593.89,"period":"2026-10-19","unit":"TWD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-19","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":4.51,"period":"2026-10-19","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-19","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"凱基證券 2026-04 研報預期台達電液冷市占率因競爭加劇而下降，但仍是散熱方案關鍵供應商；並指台達電有望成為 NVIDIA VR200 首家通過認證的 12kW PSU 供應商","source":"KGI Securities, Delta Electronics (2308 TT) 研究報告 20260420","url":"https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/delta-electronics_2308-tt_20042026.pdf","excerpt":"They assume a lower market share on intensified competition.","as_of":"2026-04-20","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"中國時報報導投顧報告：水冷標案出現競爭對手，台達電最大水冷專案可能流失小部分市占，但下半年新產品仍有較高機率維持獨家供應","source":"中國時報 wantrich","url":"https://wantrich.chinatimes.com/news/20260405900002-420101","excerpt":null,"as_of":"2026-04-05","retrieved_at":"2026-10-19","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"經濟日報報導：台達電與光寶科在 AI 伺服器電源領跑，法人估台達電大型 AI 運算中心客戶電源供貨比由去年約5成升至今年約7成；客戶可能找第二、第三供應商，董事長表示未來市占率不會維持這麼高","source":"經濟日報 money.udn.com《台達電、光寶 AI 電源供貨比7成！2026年競爭因2原因加劇》","url":"https://money.udn.com/money/story/5612/9109934","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"優分析指台灣廠商占全球電源供應器市場近七成，台達電居龍頭，主要對手為光寶科(2301)、群電(6412)、康舒(6282)；台達電營收規模、毛利率、營益率最佳","source":"優分析 uanalyze.com.tw","url":"https://uanalyze.com.tw/articles/9129310785","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-19","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"執行長鄭平表示台達在液冷與電源供應器早期市占率很高，部分細分元件高到客戶感到不安，客戶已開始找第二、甚至第三供應商（未點名客戶）","source":"經濟日報（money.udn.com）","url":"https://money.udn.com/money/story/5612/9109934","excerpt":"鄭平表示，台達在液冷跟電源供應器的早期階段，市占率都相當高，某些細分的元件上，甚至高到「客戶感到不安」，故客戶已經開始找第二供應商，甚至第三供應商，是自然而然的事。","as_of":"2025-10-31","retrieved_at":"2026-10-19","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"搜尋未找到台達電年報「主要銷貨客戶」表或任何單一客戶占營收比重數字；公開報導稱公司向來不揭露客戶資訊、不評論單一客戶（搜尋摘要轉述，非原文）","source":"自由時報 焦點股》台達電：客戶墨國產線慘了 股價重挫9%","url":"https://ec.ltn.com.tw/article/breakingnews/4939499","excerpt":null,"as_of":"2025-02-01","retrieved_at":"20261019","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Reuters 報導稱台達電客戶包括 Nvidia 與 Google、Meta 等雲端業者；無 Nvidia 占台達電營收比重的揭露；2025Q2 AI 電源占營收 22%、液冷 5%（產品別，非客戶別）","source":"Reuters via whbl.com / Taipei Times 2025-08-01","url":"https://whbl.com/2026/04/30/taiwans-delta-electronics-warns-costs-rising-as-ai-data-centre-demand-surges/","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261019","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2025-02 因美墨關稅，市場擔憂台達電 AI 伺服器電源客戶（廣達、鴻海、緯創等輝達夥伴）出貨受阻，股價盤中跌約 9%；未發現客戶信用惡化的具體證據","source":"自由時報 焦點股》台達電：客戶墨國產線慘了 股價重挫9%","url":"https://ec.ltn.com.tw/article/breakingnews/4939499","excerpt":null,"as_of":"2025-02-01","retrieved_at":"20261019","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"2026 年 7 月報導提到市場流傳「掉單」與競爭格局生變傳聞，公司尚未證實；來源僅見搜尋摘要","source":"工商時報 wantrich.chinatimes.com","url":"https://wantrich.chinatimes.com/news/20260704900004-420101","excerpt":null,"as_of":"2026-07-04","retrieved_at":"20261019","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"董事長鄭平 2026-07 表示看不到 AI 停下來，將在泰國、大陸、美國持續建新廠；2026 全年資本支出預估約 700 億元（上半年約 275 億元），高於 2025 年約 466 億元","source":"工商時報 ctee 2026-07-31 報導","url":"https://www.ctee.com.tw/news/20260731700677-430201","excerpt":"目前沒有看到AI會停下來，相信大家會愈用愈多，我們看好的能源基礎建設/微電網/綠電/固態電池等也需要產能，我們會持續在泰國、大陸及美國建置新廠。","as_of":"2026-07-31","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026-02 泰達電董事會通過擴產資本支出約 165 億元，興建印度 F3、F7、F8 廠；報導稱 AI 電源與液冷需求強勁使全球產能吃緊","source":"工商時報 ctee 2026-02-22 / uanalyze 報導","url":"https://uanalyze.com.tw/articles/5097147850","excerpt":"因 AI 電源、液冷散熱需求強勁，導致台達電全球產能吃緊，公司也積極推進擴產計畫。","as_of":"2026-02-22","retrieved_at":"2026-10-19","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026-02 法說：HVDC 預計 2026 下半年小量出貨、2027 年進入大量貢獻期；2026 資本支出高於 2025 年","source":"台達電 2025Q4 法說會（2026-02-26）及重點摘要","url":null,"excerpt":null,"as_of":"2026-02-26","retrieved_at":"2026-10-19","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026 年 6 月合併營收 656.03 億元，月增 11.3%、年增 55.4%，創單月歷史新高；AI 資料中心電源與散熱出貨暢旺，樓宇自動化與 IA 需求增溫","source":"工商時報 ctee 2026-07-28 法說前報導","url":"https://www.ctee.com.tw/news/20260728701086-430201","excerpt":"AI資料中心電源與散熱出貨暢旺，且樓宇自動化與IA需求增溫，115年6月合併營收為656.03億元，月增11.3%，年增55.4%，創下單月歷史新高。","as_of":"2026-07-28","retrieved_at":"2026-10-19","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"2Q26 伺服器電源受缺料影響，功率半導體部分料號交期逾六個月，毛利率低於預期（凱基）；外資另指 IGBT/MOSFET 交期拉長、資料中心專案延期","source":"KGI 研究報告 delta-electronics_20260730","url":"https://www.kgi.com.hk/zh-hk/-/media/files/kgishk/research-reports/tw-reports/delta-electronics_20260730_en.pdf","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"2026-08 全球電子協會調查：零組件與材料市場可得性在 2Q26 較 1Q26 惡化者為改善者的四倍以上（44% 對 10%）；整體缺料呈選擇性緊張（被動元件、部分記憶體），伺服器需求 2027 預期仍強、消費端疲弱","source":"Global Electronics Association / VSE 2026 供應鏈展望","url":"https://www.electronics.org/blog/supply-chain-tightening-again-data-makes-it-hard-look-away","excerpt":null,"as_of":"2026-08-01","retrieved_at":"2026-10-19","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"美國ITC於2026年10月依337條款對特定垂直供電系統啟動調查，申訴方Vicor主張專利侵權；台達電及兩家美國子公司（Delta Electronics (Americas) Ltd.、DET Logistics (USA) Corporation）列為被調查對象。性質為專利／進口爭議，非反壟斷。台達電表示將積極因應、相關產品目前未受影響；經濟部貿易署稱審理通常12至16個月。","source":"中央社 美國啟動337調查鴻海台達電等台廠入列 經濟部：必要時提供協助","url":"https://cna.com.tw/news/afe/202610110072.aspx","excerpt":null,"as_of":"2026-10-11","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","triggers","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"券商報告稱USITC於2026-10-09依Vicor申訴對台達電等20家公司啟動調查，預估16–18個月，和解或改設計較可能；引述Vicor與台達電先前爭議於2025年5月和解（二手來源，未對照USITC案卷）。","source":"Kaohoon International: Kiatnakin Maintains 'Buy' on Delta Thailand, Expecting Limited Impact From US Probe Into Taiwan Parent","url":"https://www.kaohooninternational.com/?p=592631","excerpt":null,"as_of":"2026-10-09","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2025Q1法說會（2025-04-30）：董事長鄭平表示客戶趁90天寬限期加快拉貨，並認為即使泰國產地再加徵三、四成關稅，整體成本仍低於美國製造；公司與客戶密切討論應對對等關稅（依搜尋摘要轉述，未讀原頁）。","source":"股感 stockfeel 法說會 台達電 2025Q1／Yahoo 奇摩股市《電零組》台達電3月寫最強單月營收 偕客戶應對關稅戰","url":"https://www.stockfeel.com.tw/%E6%B3%95%E8%AA%AA%E6%9C%83-%E5%8F%B0%E9%81%94%E9%9B%BB-2025q1-0430","excerpt":null,"as_of":"2025-04-30","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"法人分析文章估計：電動車、工業／醫療用電源與風扇短期可能由客戶負擔關稅，液冷系統部分零組件需台達電自行負擔，液冷毛利率可能下降約5%；此為法人估計非公司公告，發布日未確認（2025年）。","source":"搜尋結果分析文章（台達電 美國 關稅 轉嫁），來源頁面未逐字讀取","url":null,"excerpt":null,"as_of":"2025-04-30","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"另有文章指出美國占台達電營收比重達30%以上，生產基地無法完全避開美方貿易壓力（搜尋摘要轉述，文章日期未確認）。","source":"搜尋結果（台達電 美國 關稅 轉嫁 客戶 分攤）","url":null,"excerpt":null,"as_of":"2025-04-30","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"台達對外出口管制政策（EMEA版，2026/01）聲明其業務受歐盟制裁規則與美國EAR約束，交易可能依目的地、終端用戶、用途或產品分類受限（依搜尋摘要轉述）。","source":"Delta Electronics filecenter 出口管制政策 PDF","url":"https://filecenter.deltaww.com/about/images/about-202604012230573284.pdf","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-19","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026年2月報導：鄭平指出台灣既有產能趨於飽和、美國在地產能受建置成本與時程限制，全球擴產重心轉向泰國基地","source":"工商時報 ctee.com.tw 2026-02-22 報導（搜尋摘要轉述）","url":"https://www.ctee.com.tw/news/20260222700008-430105","excerpt":null,"as_of":"2026-02-22","retrieved_at":"2026-10-19","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"台達電生產基地分布大陸、台灣、泰國、印度、斯洛伐克；較早報導（約2018年）稱大陸產能約佔七成，後續持續提高中國以外配置；搜尋未找到最新各地區產能百分比","source":"搜尋結果摘要（天下雜誌 cw.com.tw／科技新報等，年份不一）","url":"https://www.cw.com.tw/article/5131157","excerpt":null,"as_of":"2018-09-09","retrieved_at":"2026-10-19","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"2026年7月法說：泰國新廠完成後產能將較原廠區大幅提升；台灣、中國、美國也持續擴產；2026年資本支出約700億元，較去年466億元增約50%","source":"鉅亨／uanalyze 台達電法說報導及自由時報 ec.ltn.com.tw（搜尋摘要轉述）","url":"https://ec.ltn.com.tw/article/paper/1764827","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.H","valuation"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2018年收購泰國DET，考量之一為降低地緣政治不確定及美中貿易戰風險；2022年上海封控期間蘇州、昆山廠區進料出貨一度受影響，列入白名單後改善","source":"搜尋結果摘要（tw.tpcashow.com、鉅亨／經濟日報等）","url":"https://tw.tpcashow.com/en/newsDetail.asp?serno=5506","excerpt":null,"as_of":"2018-12-31","retrieved_at":"2026-10-19","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"近期報導稱主要零組件供應在可控範圍，公司透過多元供應來源降低波動；搜尋未找到對特定單一供應商依賴的揭露","source":"搜尋結果摘要（ctee.com.tw）","url":"https://ctee.com.tw/news/tech/912471.html","excerpt":null,"as_of":"2026-01-01","retrieved_at":"2026-10-19","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年8月合併營收645.86億元，月減3.7%、年增35.0%，累計前8月4,742.68億元、年增41.1%","source":"TechNews 台達電(2308)8月營收","url":"https://finance.technews.tw/2026/09/09/delta-2308-202608-financial-report/","excerpt":"台達電(2308)今(9)日公布 8 月營收，達 645.86 億元，較 7 月成長 -3.7%,較去年同期成長 35.0%,累計前 8 月營收為 4,742.68 億元，年增 41.1%。","as_of":"2026-09-09","retrieved_at":"2026-10-19","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"0","claim":"2026年9月營收約654億元、年增14.6%，Q3合併營收約1,970.59億元，季增7.5%、年增31.1%，再創單季新高；9月年增較上半年大幅降速","source":"statementdog／TechNews 2026-10-12 報導 台達電 Q3 營收","url":"https://statementdog.com/news/17869","excerpt":"台達電 Q3 營收近 1971 億元再創新高 強調 337 調查暫不影響產品","as_of":"2026-10-12","retrieved_at":"2026-10-19","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3成長降速主因電源IC、PMIC、MOSFET等關鍵零組件供給吃緊，部分AI伺服器訂單出貨遞延，可能於Q4回補","source":"優分析 台達電(2308) Q3成長為何降速?何時回升?","url":"https://uanalyze.com.tw/articles/1907556908","excerpt":"台達電(2308) Q3成長為何降速?何時回升?","as_of":"2026-10-12","retrieved_at":"2026-10-19","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年6月營收656.03億元創單月新高、年增55.4%，上半年合併營收3,426.09億元年增41%；6月營收比重電源及零組件約50%、基礎設施約37%、自動化約8%、交通約5%","source":"TechNews 2026-07-09 delta june ai power hvdc／經濟日報","url":"https://finance.technews.tw/2026/07/09/delta-june-ai-power-hvdc/","excerpt":null,"as_of":"2026-07-09","retrieved_at":"2026-10-19","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"凱基指出2Q26伺服器電源受缺料影響，營收季增16%、占比30%，預期伺服器電源為主要成長動能","source":"KGI Delta Electronics 2026-07-30 報告","url":"https://www.kgi.com.hk/zh-hk/-/media/files/kgishk/research-reports/tw-reports/delta-electronics_20260730_en.pdf","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"0","claim":"7月底法說會董事長鄭平稱下半年仍有新機種導入、建置端缺料與延遲等變數，預期下半年營運優於上半年","source":"經濟日報／聚合報導 2026-07 法說會","url":"https://www.ctee.com.tw/news/20260728701086-430201","excerpt":"台達電董事長鄭平先前於 7 月底法說會表示，下半年市場仍存在新機種導入、建置端缺料與延遲等變數，不過公司與客戶合作正常，產能布局及物料掌握情況尚稱穩定，預期下半年營運將優於上半年。","as_of":"2026-10-12","retrieved_at":"2026-10-19","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"2026年資本支出預算由650億元上調至約700億元；大摩／法人對AI相關營收占比估計口徑不一（約25%至逾40%），未取得一手定義","source":"TechNews／優分析／經濟日報 2026","url":"https://uanalyze.com.tw/articles/7262249211","excerpt":null,"as_of":"2026-07-09","retrieved_at":"2026-10-19","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"董事長在2026Q1法說會表示±400V高壓直流產品今年出貨，800V架構配合新一代AI平台，預計2026下半年小量出貨、2027年進入主要貢獻期（公司自身的電壓架構世代轉換，非外部替代者）","source":"永豐金證券 股市話題：台達電法說會重點 Q1 EPS 7.91元","url":"https://www.sinotrade.com.tw/richclub/hotstock/%E5%8F%B0%E9%81%94%E9%9B%BB%E6%B3%95%E8%AA%AA%E6%9C%83-Q1-EPS-7-91%E5%85%83%E6%94%B9%E5%AF%AB%E5%96%AE%E5%AD%A3%E7%B4%80%E9%8C%84-%C2%B1400V%E4%BB%8A%E5%B9%B4%E5%87%BA%E8%B2%A8-800V%E8%93%84%E5%8B%A22027%E5%B9%B4%E6%94%BE%E9%87%8F-%E8%82%A1%E5%B8%82%E8%A9%B1%E9%A1%8C-69f3237ae912b0007968ba63","excerpt":null,"as_of":"2026-05-06","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"總裁張訓海稱固態變壓器（SST）可望取代傳統矽鋼片變壓器，市場最慢2027年爆發；SST屬公司自身研發項目之一","source":"科技新報 technews.tw SST 標籤頁","url":"https://technews.tw/tag/sst/","excerpt":null,"as_of":"2026-05-06","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"凱基研究：公司將2026年資本支出上調逾100億元至650–700億元，研發重點含SST與燃料電池（SOFC）","source":"KGI Research 台達電報告 2026-07-30","url":"https://www.kgi.com.hk/zh-hk/-/media/files/kgishk/research-reports/tw-reports/delta-electronics_20260730_en.pdf","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.R","valuation"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"KGI 2026年4月報告：伺服器電源1Q26營收年增逾90%、占營收31%；液冷營收季減22%至150億元；Delta在GTC展示660kW 800V DC機櫃，目標2H26開始出貨","source":"KGI Securities, Delta Electronics 2308 TT 研究報告","url":"https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/delta-electronics_2308-tt_20042026.pdf","excerpt":"Server power sales surged by over 90% YoY to 31% of revenue, while liquid cooling system revenue was down 22% QoQ to NT$15.0bn.","as_of":"2026-04-20","retrieved_at":"2026-10-19","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026年第二季毛利率降至35.64%，原因為零組件成本及產品組合；法說焦點為AI伺服器電源、液冷與HVDC進度（僅見法說前後報導摘要，未讀到會後完整原文）","source":"工商時報 ctee.com.tw 2026-07-30 台達電法說相關報導","url":"https://www.ctee.com.tw/news/20260730700219-430502","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"中央社：鄭平在法說會表示受惠AI資料中心建置，2026年全年資本支出約700億元，高於去年466億元","source":"中央社相關報導（經搜尋摘要轉述）","url":"https://news.cnyes.com/news/id/2065984","excerpt":null,"as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"電動車業務處於修正期，公司將視需求在AI與EV業務間調整產能與投資（來源日期不明，可能早於2026）","source":"Taiwan News 報導","url":"https://www.taiwannews.com.tw/en/news/6371685","excerpt":"The company will continue to shift capacity and investment between AI and EV-related businesses as demand changes","as_of":"2026-01-01","retrieved_at":"2026-10-19","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026年9月中旬，民營金控旗下投顧將目標價由2300元下修至2200元，維持買進；主因8月營收低於預期與電源IC等供應瓶頸，2027年EPS預估下修至62.50元、改用35倍本益比。","source":"中國時報 旺得富 2026-09-17 報導（搜尋摘要）","url":"https://wantrich.chinatimes.com/news/20260917900478-420101","excerpt":"民營金控旗下投顧近日報告將台達電目標價由2300元下修至2200元，維持「買進」評等。","as_of":"2026-09-17","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026年7月底第2季財報後，國泰、富邦、凱基投顧同步下修目標價（國泰2680→1930、富邦2500→2300、凱基2910→2505），評等仍為買進或增加持股；目標價分布約1930至2505元。","source":"搜尋摘要整理（中文財經媒體，7月底）","url":"https://wantrich.chinatimes.com/news/20260731900154-420101","excerpt":"國泰、富邦與凱基投顧同步下修目標價，但仍一致維持「買進」或「增加持股」評等","as_of":"2026-07-31","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年5月第1季財報後，日系外資給予目標價2440元；Q1 EPS 7.91元創單季新高。","source":"工商時報 2026-05-04","url":"https://www.ctee.com.tw/news/20260504700790-430201","excerpt":"日系外資最新報告給予台達電目標價2440元","as_of":"2026-05-04","retrieved_at":"2026-10-19","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026年第二季自結營收1,832.56億元、EPS 9.68元創單季新高，毛利率降至35.64%，受零組件成本與產品組合影響。","source":"工商時報 2026-07 報導（搜尋摘要）","url":"https://www.ctee.com.tw/news/20260730700219-430502","excerpt":"毛利率降至35.64%，仍優於去年全年平均水準","as_of":"2026-07-30","retrieved_at":"2026-10-19","affects":["thesis.R","valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"法說會前有外資調降目標價，理由為零組件成本上升持續壓抑毛利率，並提到800V高壓直流供電架構導入速度較預期慢。","source":"UDN 搜尋摘要","url":"https://udn.com/news/story/7252/9653321","excerpt":"零組件成本上升，將持續壓抑毛利率的表現","as_of":"2026-07-28","retrieved_at":"2026-10-19","affects":["thesis.R","valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026年8月營收645.86億元，月減3.7%、年增35.0%，累計前8月4,742.68億元、年增41.1%；7月營收670.73億元創單月新高、年增47.8%。","source":"科技新報 2026-09-09","url":"https://finance.technews.tw/2026/09/09/delta-2308-202608-financial-report/","excerpt":"台達電(2308)今(9)日公布 8 月營收，達 645.86 億元，較 7 月成長 -3.7%,較去年同期成長 35.0%,累計前 8 月營收為 4,742.68 億元，年增 41.1%。","as_of":"2026-09-09","retrieved_at":"2026-10-19","affects":["thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"美國 USITC 於 2026-10 對 AI 伺服器供電系統啟動 337 專利侵權調查，台達電及兩家美國子公司列為調查對象；台達表示生產出貨未受影響，審理通常 12–16 個月，尚無侵權認定或排除令","source":"中央社 美國啟動337調查鴻海台達電廣達入列 業者：依程序積極應對","url":"https://cna.com.tw/news/afe/202610110175.aspx","excerpt":"美國啟動337調查鴻海台達電廣達入列 業者：依程序積極應對","as_of":"2026-10-11","retrieved_at":"2026-10-19","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"台達電對持股 56.88% 的晶睿（Vivotek）進行股份轉換，每股現金 100 元，溢價約 17.5%，原定 2026-01-12 臨時股東會、3 月 27 日暫定基準日","source":"中時 wantrich 報導（晶睿股份轉換案）","url":null,"excerpt":"此次股份轉換案的現金對價每股 100 元，相較晶睿今日收盤價 85.1 元，溢價約 17.5%","as_of":"2025-12-11","retrieved_at":"2026-10-19","affects":["thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"台達電對持股 56.88% 的晶睿進行股份轉換，每股現金 100 元，溢價約 17.5%","source":"中時 wantrich 報導（晶睿股份轉換案）","url":null,"excerpt":"此次股份轉換案的現金對價每股 100 元，相較晶睿今日收盤價 85.1 元，溢價約 17.5%","as_of":"2025-12-11","retrieved_at":"20261019","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"USITC 於 2026-10 啟動 337 調查，台達電及兩家美國子公司列為調查對象（Vicor 專利案延伸），尚無認定","source":"中央社 美國啟動337調查鴻海台達電廣達入列 業者：依程序積極應對","url":"https://cna.com.tw/news/afe/202610110175.aspx","excerpt":"美國啟動337調查鴻海台達電廣達入列 業者：依程序積極應對","as_of":"2026-10-11","retrieved_at":"20261019","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"2308.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.69,"operating_margin_pct":16.78,"fcf_margin_pct":11.7,"rd_intensity_pct":8.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"VRT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.04,"operating_margin_pct":19.4,"fcf_margin_pct":25.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ETN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.9,"operating_margin_pct":17.71,"fcf_margin_pct":13.1,"rd_intensity_pct":2.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"2301.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":23.4,"operating_margin_pct":11.41,"fcf_margin_pct":-6.21,"rd_intensity_pct":5.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2301.TW","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"2308.TW"},"financial_history":{"ticker":"2308.TW","currency":"TWD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":384443308000.0,"revenue_yoy_pct":null,"gross_margin_pct":28.81,"operating_margin_pct":10.81,"net_income":32665728000.0,"diluted_eps":12.52,"free_cash_flow":24089530000.0,"fcf_margin_pct":6.27,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":401226501000.0,"revenue_yoy_pct":4.37,"gross_margin_pct":29.21,"operating_margin_pct":10.24,"net_income":33392665000.0,"diluted_eps":12.8,"free_cash_flow":42786756000.0,"fcf_margin_pct":10.66,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":421147557000.0,"revenue_yoy_pct":4.97,"gross_margin_pct":32.43,"operating_margin_pct":11.35,"net_income":35228577000.0,"diluted_eps":13.51,"free_cash_flow":37820576000.0,"fcf_margin_pct":8.98,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":554885168000.0,"revenue_yoy_pct":31.76,"gross_margin_pct":34.27,"operating_margin_pct":15.2,"net_income":60108399000.0,"diluted_eps":23.08,"free_cash_flow":51321494000.0,"fcf_margin_pct":9.25,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/2308.TW/2308.TW_Q4_2025_Earnings_Call_20260226.md）

# Q4 2025 Earnings Call
2026-02-26

Q4 2025 Earnings Call
Delta Electronics, Inc. | Earnings Calls | 2026-02-26
Unknown Executive (Executives)
Hello, everyone. Welcome to the first earnings conference of this year. And before we officially start our
-- I mean, today's conference, I would like to say Happy New Year to everyone. So now we will have our
IR, Rodney, to report the financial numbers for the -- for Q4 and 2025.
So as usual, we have announced our financial numbers yesterday, and we also uploaded our financial
reports -- financial report yesterday. So if you need more details, you can actually find the financial
report on our website.
Rodney Liu (Executives)
So our Q4 revenue reached TWD 161.6 billion, marking a record high for a single quarter. This
represents a 42% year-over-year growth and an 8% sequential increase, mainly driven by strong data
center demand.
So this sequential increase was actually above normal seasonality. But just because in terms of the
contributions from the data center, business has been increasing, I mean, for the last couple of
quarters. So the normal seasonality has become a little bit different, I mean, from -- it was -- from it
was before.
So in terms of the GP margin, gross profit in Q4 was TWD 55.9 billion, up 59% year-over-year and 7%
quarter-over-quarter, marking a new all-time high. GP margin in Q4 was 34.6% versus 30.8% a year
ago and 34.9% in Q3. Year-over-year, R&D and SG&A expenses increased 17% and 24%, respectively,
leading OpEx up 21%, with profit surging 147%.
Sequentially, OpEx rose 7%, reflecting 2% and 11% increases in R&D and SG&A expenses, respectively,
with profit growing 6%. As a percentage of sales, R&D expenses declined to 8.1% this quarter compared
with 9.8% a year ago and 8.5% last quarter. SG&A expenses were 10.2% versus 11.6% a year ago and
9.9% in the previous quarter.
So benefiting from improved economies of scale, OpEx ratio in Q4 dropped to 18.3% from 21.4% a year
ago and 18.4% last quarter. Operating profit was up 147% year-over-year and 6% sequentially, bringing
our Q4 operating margin to 16.3% compared with 9.4% a year ago and 16.5% in Q3.
So in terms of the segmentation performance, Infrastructure delivered the strongest growth with
revenues up 94% year-over-year and 12% quarter-over-quarter. Power Electronics also posted solid
growth, while Automation recorded modest but improving momentum. In contrast, Mobility remained
under pressure with sales down 31% year-on-year and 15% quarter-over-quarter.
From a profitability standpoint, Infrastructure delivered the strongest performance with profit up 287%
year-over-year and 25% quarter-over-quarter. Power Electronics also posted solid growth, rising 93%
year-over-year and 1% quarter-over-quarter.
In contrast, Mobility and Automation saw year-over-year profit declines of 27% and 83%, respectively.
Quarter-over-quarter, Mobility recorded a profit drop, while Automation swung to a profit. So non-
operating income was negative TWD 800 million in Q4 compared with negative TWD 900 million a

year ago and positive TWD 2.2 billion in Q3. The negative income in Q4 was mainly due to the write-
offs after a careful review of the assets at year-end. So in Q4, we had TWD 25.6 billion profit before tax.
And then our Q4 EBITDA was TWD 32.7 billion, up 92% year-over-year and down 7% quarter-over-
quarter.
Q4 tax expense was about TWD 6 billion. The effective tax rate was 23.4% and net profit after tax was
about TWD 17.3 billion. So the Q4 EPS was TWD 6.67. So now let's have a look at the full year
cumulative results. So the revenue was TWD 554.9 billion in 2025, up 32% year-over-year. Gross
margin was up 90 -- sorry, 39% year-over-year with a GP margin of 34.3% versus 32.4% a year ago.
So on a year-over-year basis, R&D expenses, I mean, increased 17%. SG&A rose 21% and OpEx grew
19%. Operating profit increased 76% year-over-year. By segment, Infrastructure delivered the strongest
performance with sales up 82% year-over-year and profit surging 413%. Power Electronics also posted
solid growth with sales up 25% and profit up 37% year-over-year.
Automation saw modest revenue growth, while profit declined 39%. Mobility remained under pressure,
while -- with sales down 16% year-over-year and profit turned to a loss.
So in 2025, we had about TWD 3.9 billion, I mean, nonoperating profit. In total, we had TWD 87.9
billion pretax income and EBITDA was TWD 117.9 billion. So tax expense was about TWD 19.9 billion,
representing an effective tax rate of 22.7%. As a result, net profit after tax was TWD 60.1 billion and
translating this number into EPS, EPS was TWD 23.14. And yesterday, I mean, we -- during the Board
meeting, we actually proposed a cash dividend for this year, which was TWD 11.6 per share. So now we
are open to the Q&A session.
Unknown Analyst (Analysts)
So I have 2 questions. So for the first question, I would like to know, would you have any guidance on
the OpEx increase of this year? And then also, do you have any guidance for the CapEx for this year as
well?
Po-Wen Yu (Executives)
So for the OpEx increase, this year, I think the OpEx will continue to increase. So first of all, because we
continue to have a lot of innovations and R&D need to be invested because we have, I mean, many new
-- sorry, we have many new products. So we continue to need to invest a lot into the R&D and
innovations of our products.
And secondly, because we -- okay. So for -- sorry, for the expenses, because we continue to -- we
actually are expanding our service team in other regions because we are -- our solution business -- our
solutions businesses have been increasing, I mean, within the company. So we need to have more sales
force and more FAEs and so on and so forth to serve our clients in different regions.
So that is also part of the reasons we actually expect an increase, I mean, of the OpEx this year. And
speaking of the -- okay. Speaking of the CapEx, I think the CapEx this year is probably going to be
slightly higher than the CapEx of 2025.
Unknown Analyst (Analysts)
Okay. So the next question is related to the GP margin in Q4. So could you please give us more, I mean,
colors on your GP margin in Q4?

Po-Wen Yu (Executives)
So because the GP margin in Q4 was actually softer compared to the third quarter. So my answer to
that question is, I think because our GP margin is very much subject to the overall mix -- product mix of
the companies. So there are actually -- because we have, I mean, very diversified and many different
product lines. So the GP margin is always going to be a little bit lumpy.
But I think our GP margin currently, as I always said, I think it's actually quite healthy. I mean, it's at a
quite healthy level, but we just can't really guarantee that we will always continue to, I mean, to achieve,
I mean, the new record high of GP margin.
So I think that is actually our expectation -- a healthy expectation for the GP margin.
Unknown Analyst (Analysts)
So yesterday, according to the financial report, I actually noticed that you actually mentioned -- I mean
you actually mentioned asset, the write-offs of some of your assets on your financial reports. So can I
say -- is this kind of write-offs is actually one-off or we will continue to see this kind of write-offs going
forward.
Po-Wen Yu (Executives)
So I think that is actually kind of a regular practice at the year-end of every year, I can't really say that
we will -- I mean, actually expect to see such I mean, write-offs every year. But we always take this
cautious and conservative approach to review our assets at year-end. So that is basically like that.
Unknown Analyst (Analysts)
So next question, what percentage of total revenue does liquid cooling represent currently? And what
level could it reach in 2026?
Unknown Executive (Executives)
So in 2025, I think liquid cooling-related revenue accounts for approximately 9% of our total revenue
with the majority coming from system-level solutions. But we are not in a position to provide guidance
for 2026, particularly in terms of mix, given the diversified nature of our business and multiple
variables involved.
That said, with the continued expansion of AI data centers, I think our AI-related businesses, including
the liquid cooling business and our power-related businesses or the liquid cooling market is actually
experiencing a strong growth momentum. And so we see significant opportunities ahead.
So I think in terms of the AI investment, actually, the main demand driver for the AI deployment is
actually still mainly coming from the major hyperscalers, especially in the U.S. So if you look at the
numbers and the investment, I mean, the CapEx numbers they have announced, so for this year,
supposedly, their investment -- the absolute number of their investments are actually not less than the
previous year.
So of course, the CapEx investment is one thing, but there are always some other bottlenecks or
uncertainties. For example, the lack of labors and the lack of the materials. So we can't be totally sure
about the pace of the deployment of their investments. But still, given that -- given the commitment
from those major CSPs, the commitment into the AI investment from those major CSPs, so we remain

actually cautious optimistic about the demand for this year. So although there might be some
uncertainties and/or maybe just some ups and downs in this long-term AI cycle, but for the long run,
we do believe that it is just a very early stage of this -- the new era of AI. So we remain pretty optimistic
for the long-term opportunity.
Unknown Analyst (Analysts)
So the next question is related to the potential bottleneck in terms of the power outage in the U.S. So I
know that -- actually, Delta has always been very ambitious in terms of your opportunities in the energy
infrastructure business. So can you tell us more about your plans or your opportunities in this space?
Unknown Executive (Executives)
So I think that is actually a universal issue in many different countries and for many different types of
our customers. We do have this ambition to address this issue, but -- and actually, the architecture
change in the -- the power architecture change in the data center is also somewhat related to this power
efficiency issue. So we will continue to work on this and let's see then what we can achieve.
Unknown Analyst (Analysts)
So in terms of the outlook for this year, can you please give us some updates or just more colors for this
-- for main segments?
Unknown Executive (Executives)
So I think as we -- as our Chairman just mentioned, this year, I think the main growth driver will
continue to be the AI data centers. So we actually expect to see a pretty healthy or solid growth
momentum for our Power Electronics and our Infrastructure business.
And even though -- and I'm speaking of the Mobility business, even though I think the market has been
actually experiencing a pretty struggling and pretty challenging period. But still, in the long run, we still
believe this -- the EV, it's actually one of the key to address the carbon emission issues. So we will
continue to stay in this market. But just in terms of the clientele, I think we -- actually, as everybody
knows that in terms of the customers, we actually had or have -- still have like much more customers.
There are the European OEMs or the American OEMs, but as everybody knows that the Chinese OEMs,
they actually have been really, really dominant in the global market. So we will continue to try to
approach the Chinese OEMs. And hopefully, our exposure to the Chinese OEM customers can continue
to increase going forward.
And then speaking of the Automation business, as we just reported last year, we actually had a very
modest growth for Automation segment. But still, we can really say that -- I can really say that we have
already seen very clear signs of recovery in the China market. So the only thing I can say is the market is
probably, has already been bottoming out a little bit, but still not a very strong signs of recovery yet. So
hopefully, of course, we do hope to see the growth for this year can accelerate. But that is something
actually out of our control.
Unknown Analyst (Analysts)
So the first question is actually related to the capacity. So in terms of the capacity issue, I think we still
have actually pretty tight capacity in order to fulfill the customers' demand. So last year, actually at the

year-end of last year, we had 3 new factories in Thailand -- three of our new factories in Thailand have
been going online at the year-end of last year. And then we continue to have some new capacity plans
for other regions.
Unknown Executive (Executives)
So not just -- I mean, not just Thailand. Actually, this year, we even visited Mexico. But still, we are still
in the process of evaluating whether the environment, the overall environment in Mexico is suitable for
us to further expand our capacity in the America regions.
Unknown Analyst (Analysts)
So the next question is related to what is the time line and shipment scale for power racks? Could this
become the next growth driver?
Unknown Executive (Executives)
So actually assuming no major disruptions, we expect to see initial shipments of power racks this year.
However, the actual contribution will depend on customer demand and broader supply chain
coordination. So visibility remains limited. Conceptually, power racks integrate additional components
such as relays, breakers, cabling, PDU, ADS, BBU, PCS and even liquid cooling systems which
meaningfully expand the addressable revenue opportunity for us.
Unknown Analyst (Analysts)
So I want to circle back a little bit to the -- to your opportunities in the energy infrastructure market. So
I know that you have this hydrogen energy business, which aims to address this power insufficiency
issue. So do you have any other like plans? Or do you have any other new product lines, which might
actually help with this power insufficiency issue in the background of increasing power usage due to the
AI deployment.
Unknown Executive (Executives)
So I think we just actually briefly mentioned that the new architecture in the data center, which is
actually refers to this 800-volt DC is actually part of the solutions to solve this energy issue. Because in
terms of this new power architecture, actually, the AI data centers all have been -- they are all using a
lot of energy and electricity.
So something that we can actually do to help with the situation or issue is we help our customers to try
to save as much as energy as possible by saving or reducing the energy loss during this energy
conversion process. So that is actually one way that we help with this energy or electricity insufficiency
issue.
And the other one is actually the one you just mentioned, which is related to our hydrogen energy
business. So as we previously explained in our earnings conference, this hydrogen energy actually
compared to the traditional power -- discrete power generation solutions, actually, in terms of the
power conversion efficiency is maybe higher, much higher than the traditional solution. So it can up to
maybe 65% conversion efficiency for this hydrogen energy.
But in terms of the contribution or the shipment, I think we are actually expecting to have some very
initial shipment at the end of this year. But if we want to see like more -- slightly maybe more

meaningful contribution from this hydrogen energy business, we may need to wait until maybe next
year or even maybe for the longer run.
Unknown Analyst (Analysts)
So you just mentioned that you already have some clients, they are testing your products. They're
testing your fuel cell products currently. So what kind of customers they are. Are they like the CSPs or
other types of customers?
Unknown Executive (Executives)
For the hydrogen energy, the fuel cells, actually the clients currently, they are the utility companies
instead of the CSPs. So I think there is still for the CSP clients, penetrating into the CSP clients. I think
still, it's still going to take some time to penetrate into the CSP clients.
Unknown Analyst (Analysts)
So the next question is, can you please give us some maybe breakdown or split in terms of your power
products for maybe GPU servers or maybe like ASIC servers.
Unknown Executive (Executives)
Actually, we don't really have the -- we don't really provide the details for this kind of split. And
actually, we provide a lot of different products, including our AC products, AC powers and DC
converters for different type of data center clients. So it's actually not that simple to really separate
different type of our products for different type of the platforms or for different customers.
Speaking of our DC/DC converter business, we actually do not comment on specific customer
programs. However, given the expected meaningful increase in the market demand, we actually remain
cautiously optimistic about our overall DC/DC business this year. Generally speaking, the whole
industry or the whole architecture is still in the stage of -- is still evolving. So just like many Silicon
Valley guys are talking about, maybe we can actually put our -- we can actually set up or set up the data
centers in the space.
So I think there might be some advantages of, if you try to put the data centers or set up the data
centers in the space. But there is still some other problems that you have to solve. For example, in
terms of the cooling, how do you plan to cool down the equipment, if you put those equipment or data
center equipment in the space? So there are many different conceptional ideas are being raised in this
stage, especially, during the innovation of technology.
So the only thing I can say is we actually must continue to innovate in line with market trends and
customer needs in order to sustain our competitiveness.
Unknown Analyst (Analysts)
So my next question is actually, can you please give us maybe some rough breakdown or split between
your AI servers and your traditional servers?
Unknown Executive (Executives)
No, we think that actually it's not easy to separate AI server revenues -- AI server power revenues and
traditional server power revenues.

Unknown Analyst (Analysts)
So can you give us maybe some guidance for the Q1 seasonality because traditionally, we all know about
the first quarter, historically should be the lowest season for the whole year. But just because, I mean,
the product mix, the business mix has been changed over the years -- over the quarters, so can you
please maybe just give us some ideas or some clues about the first quarter seasonality?
And the second question is related to the high-voltage DC. As I recall that you actually not just have --
you don't just have the 800-volt DC, you also have the plus/minus, 400-volt DC. So can you please tell
us the adoption rate by the CSP clients for these 2 different types of high-voltage DC power racks?
Unknown Executive (Executives)
So I think as we -- as Chairman said, different customers actually have different preference for these 2
types of HVDC power racks. So -- but we do provide both solutions. So it's not a problem for us.
And then speaking of the seasonality because as everybody knows that in the first quarter because there
are actually fewer working days in the first quarter because of the Chinese New Year holidays. So
theoretically, the second quarter is very likely going to be better than the first quarter given that reason.
And then speaking of the 800-volt DC and plus/minus 400-volt DC, because in terms of the
deployment, in terms of the pace of deployment because they are all based on the needs of our
customers, so it's actually hard for us to forecast the pace of their pulling our merchandise. But still, I
think, generally speaking, in terms of the sales contributions from this high-voltage DC, I think next
year should actually be the main year in terms of we start to see some more meaningful contribution
from the power rack business instead of this year.
Unknown Analyst (Analysts)
So my next question is still related to the capacity issue we just discussed at the beginning of the
conference. So because you mentioned that you actually are considering to maybe expand your capacity
in Thailand or maybe the U.S. or maybe even Mexico. So if you have any new capacity or new factories
in those regions. Are they only related to your power products? Or maybe you have plans for both
power and liquid or the cooling products as well for those new factories in different regions.
Unknown Executive (Executives)
So I think we always plan our capacity. We always plan our capacity based on our long-term plans
instead of any short-term needs because it always takes like a few years at the very least, maybe 2 to 3
years to complete the whole construction of new factory. So we can only have some rough estimate.
Let's say that we may need -- like we may need more new capacity and then we want those capacity to
serve maybe the clients in different regions. So I think -- but there are always some dynamics and
always some flexibility in terms of the capacity planning, especially for different type of products.
So we can actually decide which factory for which product later. So we need to just think of -- think
about which region we might want to increase our capacity at this stage. So now we -- I think we can
still have like 1 last question before we call it a day.
Unknown Analyst (Analysts)
So the final question, I think, is actually related to whether Delta has any plan on the AI robots?

Unknown Executive (Executives)
So I think currently, at this stage, I think we have actually still more industrial robots, which we really
have the mass production for these kind of products. But speaking of the AI robot or service robot, we
actually just having set up -- established a robot research center. I think it was last year. So this is
actually for the long-term innovation and the long-term plan for this area.
So I think in order to achieve, in order to -- for those so-called service robots to be more reliable and to
be more realistic for the actual use, I think it's going to take maybe a few years before that. So I think
there are actually some areas or some areas or some problems have to be tackled before we see that
really happen. So including the sensor or the sensing technology, including the communication
capability and also including the communication between the edge and cloud, and then also, you need
to consider the safety issues if you want to really deploy the service robot in the live environment.
So it's not like the factories environment. It's actually much more simple. It's much more simple. So I
do believe it's actually going to take some time to achieve that.
So I think, as I said, I think, what we have been seeing now, they are still mainly more for
demonstration purpose instead of they can be actually used in the real environment. So that is my
perspective.
So okay, thank you for joining our earnings conference today. So I will see you on the next quarter. So
thank you.
[Statements in English on this transcript were spoken by an interpreter present on the live call.]


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2308.TW_Q3_2025_Earnings_Call_20251030.md
- 2025-10-30｜Rodney Liu｜margin：財務長報告 Q3 毛利率 34.9%，較 Q2 略降（原話："GP margin for Q3 was 34.9%, slightly"）
- 2025-10-30｜Rodney Liu｜margin：Q3 營收創單季新高（原話："billion, marking a record high quarterly result."）
- 2025-10-30｜Executive｜margin：管理層把 Q2 到 Q3 毛利率下滑歸因於存貨回沖與跌價損失的差異（原話："was still related to the inventory reversal and inventory"）
- 2025-10-30｜Executive｜margin：管理層說明資料中心系統型業務毛利不一定高於零組件業務，是毛利率下滑的主因（原話："is not necessarily higher or is not going to"）
- 2025-10-30｜Executive｜margin：營收加速成長時，費用率有機會因營運槓桿續降（原話："we will continue to enjoy some operating leverage."）
- 2025-10-30｜Executive｜guidance：對第四季與明年第一季展望表示相當樂觀（原話："I think we are quite optimistic."）
- 2025-10-30｜Executive｜guidance：同一段話中附帶提醒環境變化快、需保持謹慎（原話："So we still need to be cautious and be prepared."）
- 2025-10-30｜Rodney Liu｜guidance：管理層認為明年動能應該不差，理由是資料中心業者仍高度投入 AI 資本支出（原話："for the whole next years I think the momentum should be"）
- 2025-10-30｜Executive｜guidance：被問明年 AI 相關營收貢獻時，管理層表示難以預測比重（原話："So it's really difficult to forecast the percentage."）
- 2025-10-30｜Executive｜margin：管理層揭露 Q3 伺服器電源占營收 23%（原話："sorry, 23% of our total"）
- 2025-10-30｜Executive｜margin：管理層揭露 Q3 散熱方案占營收約 11%（原話："the cooling solutions was around 11% of our total revenues."）
- 2025-10-30｜Executive｜capital_allocation：前三季資本支出約 297 億台幣（原話："quarters, it was around TWD 29.7 billion."）
- 2025-10-30｜Executive｜capital_allocation：全年資本支出預估約 400 億台幣（原話："for the whole year, I think it's going to be somewhere"）
- 2025-10-30｜Executive｜capital_allocation：明年資本支出金額與今年相近，內容偏向工廠自動化與設備（原話："for the next year, I think, in terms of the dollar amount"）
- 2025-10-30｜Executive｜capital_allocation：解釋收購日本公司動機：整合半導體電源關鍵技術，取得 RF 電源能力（原話："this Japanese company brings leading RF power expertise"）
- 2025-10-30｜Rodney Liu｜capital_allocation：管理層把併購視為加速成長的主要工具之一（原話："we do view this M&A as one of our main tools"）
- 2025-10-30｜Executive｜product：產能很緊，持續擴產（原話："the capacity is actually pretty tight."）
- 2025-10-30｜Executive｜commitment：泰國三座新廠預計年底前完成建造（原話："we may have 3 new factories in Thailand are likely to be"）
- 2025-10-30｜Executive｜product：800 HVDC 要一段時間才會對營收有意義貢獻（原話："it's still going to take some time before it become more"）
- 2025-10-30｜Po-Wen Yu｜risk：美國產能約兩年後才會有較有意義的規模，且占整體比重不會太大（原話："the U.S. capacity is going to account for a really big"）
- 2025-10-30｜Executive｜risk：被問美國製造成本時，管理層補充勞力是美國製造的關鍵瓶頸（原話："labors are actually one of the key bottlenecks"）
- 2025-10-30｜Executive｜risk：超過 95% 業務為 FOB，關稅由客戶負擔，有時公司先墊再向客戶請款（原話："more than 95% of our businesses on this FOB basis, which"）
- 2025-10-30｜Executive｜customer：大客戶新一代產品今年仍未使用 DC/DC 模組（原話："they are still not using the DC/DC"）
- 2025-10-30｜Executive｜competition：管理層承認客戶會想找第二供應商以增加供應商間競爭（原話："increase the competition among the suppliers."）
- 2025-10-30｜Executive｜competition：管理層認為客戶尋找第二來源必然會發生（原話："something that is definitely going to happen."）
- 2025-10-30｜Executive｜guidance：氫能未來一兩年內不預期對財務有實質貢獻（原話："we do not expand hydrogen to make a meaningful contribution"）
- 2025-10-30｜Executive｜risk：交通與自動化兩個事業今年都很吃力（原話："these 2 businesses have been very challenged"）
- 2025-10-30｜Executive｜risk：中國以外主要車廠電動車銷售明顯下滑（原話："nearly all major OEMs are seeing clear declines in EV sales"）

### 問答異常語氣（迴避／改口／保留）
- 2308.TW_Q3_2025_Earnings_Call_20251030.md｜問：分析師問明年 AI 相關業務的預估營收貢獻｜答法：未給數字，表示變數多、難以預測比重
- 2308.TW_Q3_2025_Earnings_Call_20251030.md｜問：分析師追問 AI 占比提高為何 Q3 毛利率仍低於 Q2，以及費用率走向｜答法：重複前一題的產品組合說法，未提供毛利率或費用率數字，費用率僅以有條件語氣回應
- 2308.TW_Q3_2025_Earnings_Call_20251030.md｜問：分析師問先前說美國製造成本遠高於泰國，現在對美國製造是否改變想法｜答法：未直接回答是否改變想法，改談勞力瓶頸與美國產能擴張時程

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
{"date":"20260514","verdict":"B 觀望偏進場（thesis 完整 + Q1 26 GM 37% 超預期、估值透過 EPS 修正自然壓縮至 FY+2 PE 33.4x，但短中期 R:R 仍雙負，等 BB 中軌 1,500 或 Q2 法說連 2 季驗證）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 資料中心 Capex 結構性持續，±400V 2026 量產、800V 2027 主貢獻，Infrastructure 維持 +40%+ 連 6 季","columns":{"具體數字門檻（sourced floor）":"Infrastructure YoY ≥ +30% 連 6 季（Q4 25 基準 +53%）；800V 出貨量 2027 成為 &gt;50% Infrastructure Rev 來源（管理層法說 2026-04-30）","信息來源":"管理層 2026-04-30 法說確認「800V 2027 年進入主要貢獻期」；GOOGL FY26 Capex 上修至 $185-190B（2026-04 Reuters）","漂移觸發條件（對齊 QC-34）":"連 2 季偏離（Infrastructure YoY &lt;+30%）→ H1 警戒；連 4 季偏離 → H1 反轉（QC-35：2Y 假設連 2 季即可警戒）","2Y 驗證點":"Q2-Q3 2027：Infrastructure YoY +40%+ × 6 季；800V 出貨 ramp 確認","5Y/10Y 驗證點":"5Y（2031）：Infrastructure 占總 Rev 35%+；10Y（2036）：AI DC 電源系統整合市佔 25%+"}},{"id":"H2","text":"合併 GM 升級至 36-37%（Q1 26 已達 37%），液冷 + 800V 高附加價值產品組合持續","columns":{"具體數字門檻（sourced floor）":"合併 GM ≥ 35%（每季，Q1 26 actual 37%）；Infrastructure OI margin ≥ 16.3%（Q4 25 基準）","信息來源":"Q1 2026 法說 GM 37% 實際數字（sinotrade.com 2026-05 引用）；管理層指引「全年 GM ≥ 35%」","漂移觸發條件（對齊 QC-34）":"連 2 季 GM &lt;35% → H2 警戒（QC-35：2Y 連 2 季警戒）；連 4 季 &lt;34% → H2 反轉","2Y 驗證點":"FY26 GM 全年 ≥ 36%（Q1 26 已 37%，需 Q2-Q4 維持）","5Y/10Y 驗證點":"5Y（2031）：GM 穩定 36-38%；10Y（2036）：Delta 從「電源 OEM」升級為「DC 電力系統 IP 商」，GM 趨近 IDC 廠水位 38-42%"}},{"id":"H3","text":"市場給予合理 Forward P/E 32-38x；當前 FY+2 33.40x 已落入合理區間，需 EPS 持續上修才能維持","columns":{"具體數字門檻（sourced floor）":"FY+2 PE ≤ 38x（32-38x 合理帶）；FY26 EPS 共識 ≥ 41.67（當前）；FY27 共識 ≥ 64.52（當前）","信息來源":"yfinance 共識 EPS（17-19 位分析師）；5Y PE 歷史分位 56%（§13.1）","漂移觸發條件（對齊 QC-34）":"FY+2 PE 突破 42x 連 4 週 → 估值體系透支警告；EPS 共識下修連 2 個月 → H3 警戒","2Y 驗證點":"FY26 共識 EPS 再上修至 ≥50（再 +20%）；FY27 上修至 ≥75","5Y/10Y 驗證點":"5Y：估值體系穩定在「系統廠」35-40x；10Y：EPS 複利成長為長期驅動主軸"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI Capex 2027 拐點，Top 4 Hyperscaler 削減資本支出","columns":{"對應":"H1","時間尺度":"🔥 中期（4-6 季可觸發）","監測指標":"Top 4 Hyperscaler Capex 指引（季法說）、Infrastructure YoY","警戒閾值":"連續 2 季 Infrastructure &lt;+30% YoY，或任 1 Hyperscaler 2027 Capex YoY &lt;+10%"}},{"id":"R2","text":"Vertiv 在 800V HVDC 標準戰中拿下 NVIDIA Rubin Ultra 主供地位（Vertiv backlog $9.5B Q1 26，800V H2 2026 release 確認）","columns":{"對應":"H1, H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"2026 Q3 OCP Summit、Vertiv / Schneider 新訂單公告、Yole/TrendForce 季報 Delta 市佔","警戒閾值":"Vertiv 取得 NVIDIA Rubin 主供 reference design 公告 → H1 立即削弱 50%；Delta 市佔 &lt;50% → §5.F 觸發"}},{"id":"R3","text":"地緣政治升級，中國產能（估 ~25% 營收）遷移成本超預期","columns":{"對應":"整體","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"美中關稅政策、Delta 中國產能占比、東南亞 / 墨西哥稼動率","警戒閾值":"遷移期間 GM 回落 &gt;200bp 連 4 季，或東南亞 / 墨西哥稼動率 &lt;70% 連 6 季"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":2155.0,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261019/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
