你是 stock-analyst **v20 判斷 agent**，標的 DECK（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"DECK","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1481,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司新聞稿（Business Wire 轉載，見 quarter 欄 URL）"},"note":"共識約 $1,510M，未達（來源：Zacks/Yahoo Finance 轉述）"},{"id":"f_kpi1_non_gaap_ieepa","label":"Non-GAAP（剔除 IEEPA 關稅退款）營業利益率","value":23.2,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"法說逐字稿（管理層口述 excluding refund benefit）；公司不另報 non-GAAP 營業利益"},"note":"營業利益率共識未取得"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":389.5,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"百萬美元（利益率 26.3%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司新聞稿（Business Wire 轉載）；利益率 26.3% 見法說稿"},"note":"未取得"},{"id":"f_kpi3_gaap","label":"毛利率（GAAP）","value":60.5,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司新聞稿（Business Wire 轉載）"},"note":"未取得"},{"id":"f_kpi5_q3_fy2027","label":"管理層指引：Q3 FY2027","value":"EPS $3.52–3.60；營收年增低個位數","period":"Q2 FY2027 公告（2026-10-22）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2027 公告（2026-10-22）","citation":"法說逐字稿（Motley Fool）"},"note":"未取得"},{"id":"f_kpi6_fy2027","label":"管理層指引：全年 FY2027","value":"營收 $5.700–5.725B；EPS $7.80–7.95；毛利率約 58.5%；營業利益率約 23%；SG&A 約 35.5%；稅率約 23%；假設回購 $1.0B","period":"Q2 FY2027 公告（2026-10-22）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2027 公告（2026-10-22）","citation":"公司新聞稿（Business Wire 轉載）"},"note":"營收指引下修（HOKA 高個位數、UGG 低個位數成長，均較前次調降）；FY1 EPS 共識 7.73（見 consensus_revision，財報前快照）"},{"id":"f_kpi7","label":"品牌／通路","value":"HOKA $677.2M；UGG $786.4M","period":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司新聞稿（Business Wire 轉載）"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_deck_gross_margin_pct","label":"DECK 毛利率","value":57.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DECK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_deck_operating_margin_pct","label":"DECK 營業利益率","value":22.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DECK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_deck_fcf_margin_pct","label":"DECK FCF 利潤率","value":20.22,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DECK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_onon_gross_margin_pct","label":"ONON 毛利率","value":64.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONON.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_onon_operating_margin_pct","label":"ONON 營業利益率","value":13.79,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONON.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_onon_fcf_margin_pct","label":"ONON FCF 利潤率","value":13.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONON.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nke_gross_margin_pct","label":"NKE 毛利率","value":43.16,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NKE.gross_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nke_operating_margin_pct","label":"NKE 營業利益率","value":8.28,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NKE.operating_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nke_fcf_margin_pct","label":"NKE FCF 利潤率","value":6.25,"period":"TTM ending 2026-08-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NKE.fcf_margin_pct","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_birk_gross_margin_pct","label":"BIRK 毛利率","value":56.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BIRK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_birk_operating_margin_pct","label":"BIRK 營業利益率","value":24.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BIRK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_birk_fcf_margin_pct","label":"BIRK FCF 利潤率","value":12.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BIRK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crox_gross_margin_pct","label":"CROX 毛利率","value":57.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CROX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crox_operating_margin_pct","label":"CROX 營業利益率","value":20.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CROX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_crox_fcf_margin_pct","label":"CROX FCF 利潤率","value":17.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CROX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4_eps","label":"稀釋 EPS","value":2.31,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"美元（剔除退款 $2.03，年增 11.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司新聞稿（Business Wire 轉載）"},"note":"Zacks 稱共識 $1.82 → 調整後 EPS 超預期；但 $1.82 同為去年同期 GAAP EPS，疑似轉述混淆，使用前須另行核對"},{"id":"f_kpi8","label":"期末現金／存貨／回購","value":"現金 $1.210B；存貨 $860.8M；Q2 回購 $299.3M","period":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","unit":"","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-10-22）","citation":"公司新聞稿（Business Wire 轉載）"},"note":"未取得"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":81.09,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-25.28,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.37,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.93,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.51 → 7.73）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-1.44,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.33 → 8.21）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-1.27,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.46 → 9.34）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":7.73,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":8.21,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":9.34,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":2.66,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 7.53 → 7.73（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":10.49,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 7.73，分子＝快照價 81.09","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 81.09 / W52 98.68 / W104 117.13 / W250 102.88 / W250 13週斜率 0.36%"},{"id":"f_ma_w52","label":"52 週均線","value":98.68,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":117.13,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":102.88,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.36,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"公司 10-K 風險因子自述：面臨既有與新進入者競爭，HOKA 與 UGG 的能見度吸引了專攻這些品類的競爭者，離岸製造降低進入門檻，市占可能下滑。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"We believe that the growth and visibility of our HOKA brand and UGG brand have attracted competitors specifically targeting the categories in which we operate. Barriers to entry have been reduced by access to offshore manufacturing and evolving technologies, allowing competitors to develop and scale products more quickly and at lower cost.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"公司 10-K 自述已經歷並預期持續面臨定價與促銷壓力，競爭者加大折扣可能迫使其降價或加促銷。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"Consistent with these dynamics, we have experienced, and expect to continue to experience, pricing and promotional pressure across our brands and channels, particularly during periods of elevated industry inventory levels or inflationary pressure.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"管理層引 Circana：HOKA 於美國路跑 $140 以上價位段份額於 2025 年 10–12 月三個月顯著上升並居首。","source":"Yahoo Finance Deckers Q3 FY2026 earnings call","url":"https://finance.yahoo.com/news/deckers-outdoor-q3-earnings-call-023918271.html","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Bernstein 給予 Deckers Underperform、目標價 $100，認為休閒鞋品類趨於萎縮。","source":"Tiger Brokers 轉載 Bernstein","url":"https://www.itiger.com/news/1192453254","excerpt":"Bernstein: Iconic Brands Losing Steam, Assigns \"Underperform\" Rating to Deckers with $100 Target Stock News 2025/09/19","as_of":"2026-01-01","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026（截至2026-03-31）無單一客戶占淨銷售10%以上；但有一家客戶占應收帳款淨額18.5%（前一年13.6%），該應收通常無擔保，帶來收款風險。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"However, no single customer accounted for 10.0% or more of our total net sales during fiscal year 2026. The failure to increase sales to these customers could negatively affect our growth prospects, and any reduction or loss of their business could materially and adversely affect our net sales and results of operations, particularly if we are unable to offset such declines through our DTC channel. As of March 31, 2026, one customer represents 18.5% of trade accounts receivable, net, which is generally unsecured and exposes us to collection risk that could affect our results of operations and liquidity.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"財報附註：2024–2026三個會計年度均無單一客戶占淨銷售10%以上；單一客戶應收占比由13.6%升至18.5%。","source":"SEC EDGAR 10-K FY2026 財報附註","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"Customer Concentration. For the years ended March 31, 2026, 2025, and 2024, no single global customer comprised 10.0% or more of the Company’s total net sales. As of March 31, 2026, the Company has one customer that represents 18.5% of trade accounts receivable, net, compared to one customer that represents 13.6% of trade accounts receivable, net, as of March 31, 2025.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY27 營收指引維持 $5.86–5.91B、EPS 指引上調至 $7.35–7.50；管理層預期 HOKA 低雙位數成長、UGG 中個位數成長；Q1 HOKA +7.7%（$703.5M）、UGG +4.9%（$278.0M）","source":"Deckers Brands Q1 FY2027 Financial Results (Business Wire)","url":"https://secure.businesswire.com/news/home/20260723881452/en/Deckers-Brands-Reports-First-Quarter-Fiscal-Year-2027-Financial-Results","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"管理層長期目標：至 FY2030 年營收高個位數年成長，HOKA 與國際市場成長快於整體；未見供需失衡（缺貨／過剩）的結構性或週期性論述","source":"Deckers Q1 FY27 earnings call highlights (Nasdaq/MarketBeat)","url":"https://www.nasdaq.com/articles/deckers-outdoor-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Zacks 共識隱含 FY27 EPS 成長 6.1%、FY28 成長 10.6%（Q1 前資料，可能過時）；未找到 FY28 營收共識數字","source":"Chartmill: Can UGG & HOKA's Global Growth Drive Deckers' Next Phase?","url":"https://www.chartmill.com/news/external/63266/can-ugg-hoka-s-global-growth-drive-deckers-next-phase","excerpt":"The Zacks Consensus Estimate for Deckers' fiscal 2027 earnings implies year-over-year growth of 6.1%, whereas the same for fiscal 2028 indicates an uptick of 10.6%.","as_of":"2026-07-01","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"關稅假設由 10% 上調至 12.5%，管理層預期 Q2 毛利率受關稅與運費壓力；風險列有消費支出轉變、貿易政策、供應鏈中斷","source":"Deckers Q1 FY27 earnings call highlights (MarketBeat)","url":"https://www.marketbeat.com/instant-alerts/deckers-outdoor-q1-earnings-call-highlights-2026-07-23/","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K 法律程序章節僅述例行智財與一般商業訴訟，未列政府反壟斷調查；風險因素提及 FTC 與州檢察長對隱私的審查加強。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"From time to time, we are involved in various legal proceedings, disputes, and other claims arising in the ordinary course of business, including employment, intellectual property, product liability, and breach of contract claims.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Quince 於 2026-02 對 Deckers 提起反壟斷訴訟，指稱以 trade dress 訴訟企圖壟斷羊皮／羊毛內裡休閒鞋市場；2026-08 下旬聯邦法院駁回起訴書但准許修正。","source":"The Fashion Law: Quince's Antitrust Case Against UGG Owner Deckers Hits an Early Hurdle","url":"https://www.thefashionlaw.com/quince-antitrust-case-against-ugg-owner-deckers-hits-an-early-hurdle/","excerpt":"Image : Quince key points Quince’s antitrust case against UGG owner Deckers has hit an early hurdle, with a court dismissing the complaint with leave to amend. Quince alleges that Deckers has used unprotectable trade dress rights to restrict competition in the footwear market. The court found that Quince had not adequately pleaded that Deckers’ litigation falls within the relevant sham-litigatio","as_of":"2026-08-31","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2026 成品生產主要在越南與印尼，中國或任何其他單一國家不到 5%；關稅可能在有限通知下調整，公司揭露地理集中與關稅風險。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"During fiscal year 2026, production of our finished goods was predominantly from Vietnam and Indonesia, while less than 5% was from China or any other individual country.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"FY2026 毛利率 57.7%（前期 57.9%），主因國內商品增額關稅；IEEPA 關稅已被最高法院判無效，CBP 公告分階段退款流程，截至 2026-03-31 未認列任何退稅。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"As of March 31, 2026, we have not recognized any amounts related to potential tariff refunds or other recoveries.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["valuation","thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"毛利率下滑主因關稅，HOKA、UGG、Teva 皆受影響。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"Gross margin decreased to 57.7% from 57.9%, compared to the prior period, primarily due to incremental tariffs on domestic goods and a slightly unfavorable channel mix","as_of":"2026-05-22","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"10-Q（截至 2026-06-30）提及先前繳納 IEEPA 關稅總額及 2026 年 6 月公告的退款申請流程。","source":"SEC EDGAR 10-Q 2026-06-30","url":"https://www.sec.gov/Archives/edgar/data/0000910521/000091052126000022/deck-20260630.htm","excerpt":"filing for refunds of previously paid IEEPA tariffs pursuant to the CAPE Phase 2 administrative refund process announced in June 2026. The Company previously paid an aggregate gross amount of approximately $120,000 in IEEPA tariffs.","as_of":"2026-08-01","retrieved_at":"20261024","affects":["valuation","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K：成品由外部製造商生產，主要在東南亞，以越南與印尼為主，中國或其他單一國家低於 5%；公司揭露集中度帶來貿易關係、關稅、政治不穩等風險","source":"Deckers FY2026 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000910521/000162828026037664/deck-20260331.htm","excerpt":"Vietnam and Indonesia, while less than 5% was from China or any other individual country. We continue to diversify our independent manufacturers and the regions in which they operate.","as_of":"2026-05-30","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2026 10-K：UGG 羊皮主要自澳洲採購，並倚賴中國兩家製革廠供應多數羊皮，替代材料可能無法及時取得","source":"Deckers FY2026 Form 10-K (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000910521/000162828026037664/deck-20260331.htm","excerpt":"Sheepskin used to manufacture a significant portion of our UGG brand products is sourced primarily from Australia and processed by two tanneries in China.","as_of":"2026-05-30","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"FY27 Q1（2026年4–6月）HOKA 淨銷售 +7.7% 至 $703.5M，UGG +4.9% 至 $278.0M，其他品牌（Koolaburra 收尾）−18.1% 至 $37.9M；DTC +13%、批發 +2.2%。","source":"Deckers Brands Reports First Quarter Fiscal Year 2027 Financial Results (BusinessWire)","url":"https://secure.businesswire.com/news/home/20260723881452/en/Deckers-Brands-Reports-First-Quarter-Fiscal-Year-2027-Financial-Results","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27 全年指引維持：合併營收 $5.86–5.91B，HOKA 低雙位數成長、UGG 中個位數成長；FY28–30 目標年營收高個位數成長。","source":"Deckers Q1 FY27 results / FashionUnited FY26 report","url":"https://secure.businesswire.com/news/home/20260723881452/en/Deckers-Brands-Reports-First-Quarter-Fiscal-Year-2027-Financial-Results","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"管理層將預設關稅率由10%上調至12.5%，毛利率指引上調至略高於56.5%；CEO 稱美國與國際終端需求仍強，但消費環境承壓。","source":"Deckers Q1 FY27 earnings call coverage (Nasdaq)","url":"https://www.nasdaq.com/articles/deckers-outdoor-q1-earnings-call-highlights","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"FY26 Q3 HOKA +18% 至 $629M、UGG +5% 至 $1.3B；公司 2025年7月起選擇性漲價，稱未見銷售明顯下滑；FY26 未緩解關稅衝擊約 $110M、淨衝擊約 $25M。","source":"Deckers Outdoor Q3 earnings call (Yahoo Finance)","url":"https://finance.yahoo.com/news/deckers-outdoor-q3-earnings-call-023918271.html","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素：部分競爭者在財務、技術、製造、行銷與通路資源上遠大於 Deckers，能更快加速產品開發、運用數據分析或 AI、適應技術變化；Deckers 亦稱無法保證能成功適應技術變化。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"Some of our competitors also have substantially greater financial, technological, manufacturing, marketing, and distribution resources than we do, as well as broader brand awareness, which may enable them to compete more effectively on price, accelerate product development, leverage advanced data analytics or AI, adapt to technological changes, and withstand periods of excess inventory or reduced consumer demand.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"搜尋未找到 UGG 羊皮的替代材料或「平替」威脅的來源；10-K 僅提到替代材料不含同樣商標。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"Although alternative materials may be available for certain branded components, which may be limited, such alternatives would not include the same trademarks.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Bernstein 給 Deckers Underperform、目標價 $100：稱 Hoka 緩衝技術已被競品複製、On 持續取得市占、Nike 跑鞋回歸構成威脅，UGG 休閒品類緩慢萎縮。","source":"Tiger Brokers 轉載 Bernstein 報告","url":"https://www.itiger.com/news/1192453254","excerpt":"Looking at the challenges facing each brand, Hoka's superior cushioning technology has been replicated by competitors, while retailers are showing fatigue with the trend. Nike's strong comeback in the running shoe segment poses a threat with its more diverse product lineup, while On continues to gain market share.","as_of":"2026-01-01","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 批發淨銷售 +12.3% 至 $3.208B，DTC +6.3% 至 $2.264B；批發成長快於 DTC，HOKA 批發 +18.2%、DTC +12.0%，UGG 批發 +12.7%、DTC +3.6%。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"Total Wholesale $3,208,107 $2,855,865 $352,242 12.3% Total Direct-to-Consumer 2,264,189 2,129,747 $134,442 6.3","as_of":"2026-05-22","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"公司長期策略仍是提高 DTC 占比，但為擴大品牌認知與市占也擴張批發，批發占比在特定期間可能上升並壓低毛利率。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"Our long-term strategy is to grow our DTC channel to represent a larger portion of our total net sales by differentiating the consumer experience relative to the wholesale channel and driving consumer acquisition and retention.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Teva 將批發通路重新聚焦戶外與高端零售商，價值導向批發客群銷售下滑，Other brands 淨銷售 -33.9%。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"We continue to take actions to reposition the Teva brand, including refocusing certain wholesale channel distribution toward outdoor and premium retail partners and emphasizing brand messaging around its outdoor-adventure heritage.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"截至 2026-03-31 共 203 家自營店（UGG 141、HOKA 62），電商網站涵蓋 54 國；UGG 批發通路分銷與產品分層持續檢討。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"As of March 31, 2026, we have a total of 203 global Company-owned retail stores (including 141 UGG brand retail stores and 62 HOKA brand retail stores), which include 105 concept stores and 98 outlet stores.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FY2027 EPS 指引 $7.35–7.50（營收 $5.86–5.91B），對照共識約 $7.48，指引中點略低於共識、上緣與共識相當；先前區間為 $7.30–7.45。","source":"Benzinga earnings forecasts（經搜尋摘要轉述）","url":"https://www.benzinga.com/quote/DECK/earnings-forecasts","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價：Benzinga 28 位分析師平均目標價約 $119，最高 $175，最低 $70（BMO 2026 年 9 月以 Underperform 啟動coverage）；MarketBeat 7 月共識為 Hold，平均 $119.05，9 買／13 持有／2 賣。","source":"Benzinga price targets；MarketBeat","url":"https://kr.benzinga.com/quote/DECK/price-targets","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"2026 年 7 月財報後目標價下修：Telsey 由 $113 降至 $105，Needham 由 $138 降至 $125，Truist 降至 $105。","source":"MarketBeat instant alerts","url":"https://www.marketbeat.com/instant-alerts/deckers-outdoor-nysedeck-price-target-lowered-to-10500-at-telsey-advisory-group-2026-07-24/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261024","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY2026 第三季（2026-01）財報時上調全年指引：EPS 由 $6.30–6.39 升至 $6.80–6.85，高於當時共識 $6.41；稍早第二季曾下修。","source":"Barchart / Business Wire Q3 FY2026 results","url":"https://www.businesswire.com/news/home/20260129217686/en/Deckers-Brands-Reports-Third-Quarter-Fiscal-Year-2026-Financial-Results","excerpt":"Diluted EPS Guidance Raised to Range of $6.80-$6.85","as_of":"2026-01-29","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Seeking Alpha 2026-03-20 顯示下一季估計過去 90 天修正偏空：2 上修、16 下修。","source":"Seeking Alpha DECK earnings","url":"https://seekingalpha.com/symbol/DECK/earnings","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"FY2026 10-K Item 3：訴訟僅為一般營運範圍（智財、僱傭、產品責任、合約），公司認為不會有重大不利影響；無集體訴訟或重大個案揭露。","source":"SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"we currently believe that the final outcome of these ordinary course matters will not, individually or in the aggregate, have a material adverse effect on our business, results of operations, financial condition, or cash flows.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月6份8-K中僅1份含重大項目：2026-08-27信貸協議第一次修訂（Item 1.01），屬融資安排，非併購。","source":"SEC EDGAR 8-K 2026-08-31 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/910521/000091052126000024/deck-20260827.htm","excerpt":"entered into a First Amendment to the Credit Agreement (the “Amendment”) with Citibank, N.A. (“Citibank”), as administrative agent, and the lenders party thereto","as_of":"2026-08-31","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K唯一重大項目為信貸協議修訂（Item 1.01），非併購；搜尋亦未見2026年併購公告。","source":"SEC EDGAR 8-K 2026-08-31 Item 1.01","url":"https://www.sec.gov/Archives/edgar/data/910521/000091052126000024/deck-20260827.htm","excerpt":"entered into a First Amendment to the Credit Agreement (the “Amendment”) with Citibank, N.A. (“Citibank”), as administrative agent","as_of":"2026-08-31","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"0","claim":"10-K Item 3 僅列一般營運訴訟與智財執法，認為無重大不利影響；搜尋只見2012年舊集體訴訟（已駁回）。","source":"SEC EDGAR 10-K FY2026 Item 3","url":"https://www.sec.gov/Archives/edgar/data/910521/000162828026037664/deck-20260331.htm","excerpt":"we currently believe that the final outcome of these ordinary course matters will not, individually or in the aggregate, have a material adverse effect on our business, results of operations, financial condition, or cash flows.","as_of":"2026-05-22","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"DECK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.8,"operating_margin_pct":22.67,"fcf_margin_pct":20.22,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.DECK","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ONON","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.82,"operating_margin_pct":13.79,"fcf_margin_pct":13.32,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ONON","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"NKE","period":"TTM ending 2026-08-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":43.16,"operating_margin_pct":8.28,"fcf_margin_pct":6.25,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NKE","as_of":"TTM ending 2026-08-31（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"BIRK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":56.86,"operating_margin_pct":24.94,"fcf_margin_pct":12.86,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BIRK","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CROX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":57.47,"operating_margin_pct":20.73,"fcf_margin_pct":17.38,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CROX","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"DECK"},"financial_history":{"ticker":"DECK","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-03-31","revenue":3627286000.0,"revenue_yoy_pct":null,"gross_margin_pct":50.32,"operating_margin_pct":18.0,"net_income":516822000.0,"diluted_eps":3.228333,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-03-31","revenue":4287763000.0,"revenue_yoy_pct":18.21,"gross_margin_pct":55.63,"operating_margin_pct":21.63,"net_income":759563000.0,"diluted_eps":4.86,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-03-31","revenue":4985612000.0,"revenue_yoy_pct":16.28,"gross_margin_pct":57.88,"operating_margin_pct":23.65,"net_income":966091000.0,"diluted_eps":6.33,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-03-31","revenue":5472296000.0,"revenue_yoy_pct":9.76,"gross_margin_pct":57.7,"operating_margin_pct":23.08,"net_income":1024071000.0,"diluted_eps":7.02,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/DECK/DECK_Q2_2027_Earnings_Call_20261022.md）

# Q2 2027 Earnings Call
**Deckers Outdoor Corporation** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Good afternoon, and thank you for standing by. Welcome to the Deckers Brands Second Quarter Fiscal 2027 Earnings Conference Call. [Operator Instructions] I would like to remind everyone that this conference call is being recorded. 
I'll now turn the call over to Erinn Kohler, Vice President, Investor Relations and Corporate Planning.

**Erinn Kohler** (Executives):
Hello, and thank you, everyone, for joining us today. On the call are Stefano Caroti, President and Chief Executive Officer; and Steve Fasching, Chief Financial Officer. 
Before we begin, I would like to remind everyone of the company's safe harbor policy. Please note that certain statements made on this call are forward-looking statements within the meaning of the federal securities laws, which are subject to considerable risks and uncertainties. These forward-looking statements are intended to qualify for the safe harbor from liability established by the Private Securities Litigation Reform Act of 1995. 
All statements made on this call today, other than statements of historical fact, are forward-looking statements and include statements regarding our ability to drive profitable growth, brand health and long-term value, the macroeconomic and consumer environment and related impacts on our business and operating results, including the expected persistence of current consumer and promotional trends, our current and long-term strategic objectives, the expected performance of our brands and demand for our products. 
The anticipated impacts of our brand, product, marketing, marketplace, distribution and investment strategies, including the expansion of our wholesale presence and our brands' lifestyle, apparel and year-round product offerings; our product development plans and the timing and anticipated performance of product launches, changes in consumer behavior, our ability to acquire new consumers and gain market share; our ability to achieve our financial outlook, including anticipated revenues, gross margin, SG&A expenses, operating margin, effective tax rate, promotional activity, anticipated rate of full price selling and earnings per share; our cost management and resource allocation actions, the anticipated effects of corrective actions related to our European third-party logistics provider, the timing of wholesale and distributor shipments, our ability to maintain a premium full-price global marketplace, statements regarding tariff refunds and our ability to generate free cash flow and execute our capital allocation strategy, including potential share repurchases. 
Forward-looking statements made on this call represent management's current expectations and are based on information available at the time such statements are made. Forward-looking statements involve numerous known and unknown risks, uncertainties and other factors such as changes in consumer demand, foreign currency exchange rate fluctuations and changes to trade policies, including the amount and timing of any future tariff refunds that may cause our actual results to differ materially from any results predicted, assumed or implied by the forward-looking statements. The company has explained some of these risks and uncertainties in its SEC filings, including in the Risk Factors section of its annual report on Form 10-K and quarterly reports on Form 10-Q. Except as required by law or the listing rules of the New York Stock Exchange, the company expressly disclaims any intent or obligation to update any forward-looking statements. 
On this call, management may refer to financial measures that were not prepared in accordance with generally accepted accounting principles in the United States, including constant currency, free cash flow and certain results and outlook measures presented, excluding the net benefit of IEEPA tariff refunds and related interest such as diluted earnings per share, gross margin and operating margin. For example, the company reports comparable direct-to-consumer sales on a constant currency basis for operations that were open throughout the current and prior reporting periods. The company believes these non-GAAP financial measures are useful supplemental indicators of its operating performance because they exclude items that are unrelated to and may not be indicative of its core operating results. 
The company defines free cash flow as net cash provided by operating activities for a particular period, less capital expenditures made during that same period and believes free cash flow is a useful supplemental measure of liquidity as it reflects the cash generated from operations after investments required to support the strategic growth of the business. Please review our earnings release published today for additional information regarding our non-GAAP financial measures. 
With that, I'll now turn it over to Stefano.

**Stefano Caroti** (Executives):
Thank you, Erinn. Good afternoon, everyone, and thank you for joining today's call. In the second quarter, Deckers delivered another solid result. We expanded our global presence, performed well in multi-brand environments and delivered a high mix of full price sales. For the quarter, total company revenue grew 3.5% versus last year with HOKA and UGG increasing 7% and 4%, respectively. 
Diluted earnings per share was $2.31, including a $0.28 benefit from the impact of IEEPA net tariff refunds received in the quarter. Excluding this benefit, diluted EPS would have been $2.03, well above the high end of our guidance range and up 11.5% versus last year.
Despite some top line pressure, we maintained healthy gross margins, delivered global growth and continued to invest in the long-term strength of our brands. Our commitment to full price selling and disciplined expense management demonstrates the resilience of our operating model and the value of our strategic approach to growth. 
As consumers face increasing economic pressure, our updated fiscal year outlook reflects a more measured approach to growth over the next 2 quarters. Consistent with our strategic framework, we're making deliberate choices about how we compete, win and grow our brands. We will continue to prioritize margin preservation and long-term value over chasing potential incremental near-term revenue that could dilute our brands. We will use our flexible expense levers to stay agile and protect the integrity of our premium global brands.
Against the backdrop, I will now share what we are seeing across the business and the operating environment, along with the actions we're taking to build on what's working and address the areas where we see opportunity for improvement. International continues to be an area of strength for our brands. 
Within international, APAC delivered our highest percentage growth and was a meaningful contributor to incremental year-over-year dollar growth in the second quarter. International markets serve as a proving ground for our brands in emerging categories. With UGG and HOKA still in the earlier stages of development in many of these markets, these consumers often view our brands through a broader lifestyle lens, helping to influence trends that later gained traction in other regions.
In EMEA, demand signals remained strong. However, service disruptions at our third-party logistics provider during a peak shipping period affected the timing of certain shipments. While this impacted revenue in the quarter, we've taken corrective action with our partner to restore normal operations, improve visibility and reduce the risk of future disruptions. 
In the U.S., we saw promotional activity increase throughout the quarter, particularly in athletic footwear, which weighed on our U.S. e-commerce performance as we maintain full price discipline. We also observed 2 shifts in consumer behavior, consumers increasingly seeking discounts, concentrating traffic around promotional events and consumers becoming more purposeful in their spending and prioritizing products with immediate relevance and utility.
Given the trends across our brands and the growing pressure on consumers, we've identified areas where improving execution can have a meaningful impact. Our objective is to deliver healthy market share gains even in a more challenging environment. These actions are grounded in our 4 guiding principles of consumer-first, brand-led, innovation-forward and globally-driven. Along with our playbook, these key pillars are designed to support sustainable brand growth and create long-term value for shareholders.
As we look ahead, we're focused on, first, delivering product excellence. We have a robust innovation pipeline designed to deliver tangible consumer benefits, reinforce the positioning and credibility of our brands and create meaningful new revenue streams. We will maximize its impact through sharper franchise segmentation, clear differentiation, elevated design and purposeful innovation that is commercially relevant and directly connected to consumer demand.
Second, elevating marketing capabilities. We are strengthening our global marketing capabilities so our products connect with consumers more meaningfully. Through sharper brand storytelling, more impactful consumer messaging and more compelling experiences, we will build deeper engagement across our growing global audience. This integrated approach will also enable us to deploy resources more effectively and generate greater consistency, leverage and returns from our marketing investments.
Third, strengthening marketplace execution. Consumer behavior is changing rapidly and we're evolving how we show up. We're focusing our resources in the channels, platforms and points of sale where consumers are most engaged and purchase intent is highest. By amplifying our digital presence, deepening engagement, enhancing loyalty programs and elevating execution at point of sale, we can meet consumers more effectively and convert interest into demand.
And finally, continuing to apply disciplined cost control and resource allocation. We're making clear choices, moving faster and prioritizing initiatives that we believe will deliver the greatest results. This approach will help us manage cost pressures, spend efficiently and concentrate resources on the actions that will most effectively support the long-term health of our brands. 
Steve will provide more detail on our second quarter financial performance and updated fiscal '27 outlook later in the call. Before that, however, I will review HOKA and UGG second quarter performance and discuss how we expect current trends to develop through the balance of the year.
Starting with HOKA. Global revenue in the second quarter increased 7% versus last year to $677 million. HOKA growth versus last year was driven by both wholesale and DTC. HOKA wholesale increased 9% to $444 million, while DTC grew by 4% to $234 million. HOKA continued to perform well across our global wholesale accounts with strong sell-through in domestic and international regions. Consumers are increasingly turning to wholesale partners, both in stores and online to explore and compare brands in multi-brand destinations and HOKA continues to deliver a high degree of full price selling. This performance reinforces the brand's premium positioning and the strength of key franchises.
While HOKA maintained strong performance in a competitive wholesale landscape, DTC results were uneven across markets. While the international DTC growth remained robust, U.S. performance was pressured amid a highly promotional U.S. environment, particularly in the athletic footwear category. Across the business, our core franchises performed well, led by Bondi. The introduction of Clifton Pro, a well-received extension of the Clifton franchise, also contributed to that success. However, feedback from consumers and wholesale partners indicated that some of the franchise updates in calendar year '26 did not resonate as well. This feedback highlights where we have an opportunity to improve for future seasons, starting with spring 2027. We remain focused on continuing to deliver high-quality growth with our wholesale partners while also improving DTC execution.
Across the global marketplace, we'll continue to focus on distinctive performance product franchises that reinforce our innovation credibility, convert awareness into a broader base of lifetime consumers and expand the HOKA brand's authentic relevance in lifestyle. As we advance these initiatives, we're confident it will improve our ability to capture market share moving forward. Specific to our product pipeline, our work to sharpen franchise segmentation is already in flight. 
Let me provide further insight into the work we're doing. On the performance side, we have a clear approach across the Glide and Fly collections that I shared on last quarter's earnings call. We will extend our leadership in max cushioning through Glide and expand our speed platform with Fly.
Within the Glide collection, Bondi 10 launches in January, introducing an upgraded dual-density supercritically foam midsole with streamlined design built for performance runners looking for premium cushioning and comfort. I'm confident Bondi 10 will be a standout performer. In our Fly collection, we'll launch Mach Pro in April, which brings a bold new aesthetic and aTPU midsole to our fastest performance [road] franchise designed for daily training. 
Testing of Mach Pro has been exceptional and bookings are very strong. Then in early fall, we'll build on that momentum with another major update to the Mach franchise. We recently previewed Mach 8 with several major accounts and the reaction was excellent.
In addition, we'll be expanding our price architecture in both directions, up and down, broadening access while elevating the pinnacle of the brand. In the first half of calendar '27, we'll introduce 2 powerful expressions of this strategy. Fly Pace in January at $115 will welcome a new consumer into HOKA and Bondi Ultra X in June at $325 will deliver our softest, most cushioned ride for consumers seeking the very best. Bondi Ultra X represents a major leap forward in HOKA innovation, featuring a triple density aTPU midsole that takes maximum cushioning to a whole new level.
Turning to lifestyle. We have a 3-pronged approach. First, we're building on the success of archived models such as Mafate Speed 2 with modernized applications, taking insights from early success we're seeing in certain markets to influence opportunities across the globe. Second, we'll expand Bondi and Clifton through fresh colors and new materials that unlock more wearing occasions to drive greater franchise segmentation and differentiation across the marketplace. And third, we'll seed new models like Cielo 70, a lower profile silhouette inspired by running shoes from the 1970s and designed to bring new lifestyle consumers into the brand.
As we build the lifestyle opportunity for HOKA, we're applying the same authentic approach that established the brand's performance credibility. We're staying grounded in our performance heritage while building lifestyle relevance through differentiated product and consistent storytelling, refined season over season based on consumer and partner insights. Positive feedback from key accounts reinforces our belief that we're building momentum with our target consumer and have ample opportunity to take share in this category. We have a powerful product pipeline across performance and lifestyle, grounded in meaningful innovation, clear segmentation and disciplined distribution. That combination will help us reach more consumers, strengthen the brand at every level and drive the next phase of HOKA growth. 
Delivering differentiated products is only part of the equation. We must also connect innovation with consumers in more compelling and impactful ways. Working with external experts, we reviewed the deployment of our marketing investments and are making changes to improve its effectiveness and efficiency. We're clarifying HOKA brand messaging, sharpening product storytelling and broadening our content to resonate with a larger audience. 
Specific to our third quarter, we're focused on executing a strong holiday season for HOKA, maintaining the strength of full price demand while preparing the marketplace for key launches in our fiscal fourth quarter. We remain focused on protecting what makes the HOKA brand distinctive while raising the level of execution needed to capture the significant global opportunity ahead.
Moving on to UGG. Global revenue in the second quarter increased by 4% versus last year, to $786 million. Growth was driven by wholesale, which increased 7% to $641 million. This was partially offset by an 8% decline in DTC, which delivered $146 million in the quarter. With the second quarter being a largely sell-in quarter for the brand, wholesale performance was healthy across the U.S. and international regions, which sets the stage for the upcoming holiday season. 
In addition, we continue to see very positive indicators of brand health and interest, giving us confidence that UGG is well positioned for peak season. At the same time, pressures on consumers are prompting some to delay purchase until closer to need. We believe that this shift toward a more deliberate buy now, wear now purchasing behavior makes it even more important to give consumers compelling reasons to choose UGG across a broader range of styles and occasions.
Across the globe, consumers are responding to elevated product that is distinctly UGG, gravitating towards fresh expressions of our iconic franchises as well as new styles that bring recognizable UGG brand codes into new and unexpected categories. In Q2, we drove success with Lowmel continuing to build the UGG brand's relevance in sneakers, Goldenstar Evelina extending our presence in clogs and Zora and Quill demonstrating the brand's ability to quickly adapt to fashion trends. We're also seeing growing demand for UGG head-to-toe with fleece-led apparel driving engagement and reinforcing the brand's potential to cement itself as a premium global lifestyle brand. The goal now is to bring these innovation stories to a broader audience.
Our most loyal consumers look to UGG for what is next and we're focused on extending that excitement across a broader consumer base and all genders. Classics and Tasman are already well-established franchises, while we're building Lowmel, Golden, Zora and Quill into more meaningful contributors. This deliberate season-by-season approach is designed to create hero franchises with lasting relevance. As awareness grows, these franchises can expand how consumers engage with UGG across categories and wearing occasions. 
During the quarter, our teams created urgency through scarcity, timely restock messaging and culturally relevant product stories. Sunburst, Classic Tall and Classic Mini Dipper Legwarmer demonstrated the effectiveness of the strategy with early season demand exceeding our expectations. These successes show that consumers continue to respond to compelling styles and fresh expressions of the brand even in a more selective spending environment. 
As we move deeper into UGG season, our focus is on applying those learnings more broadly and raising our level of execution across the business. That means being more purposeful in how we tell our product stories, creating greater energy and urgency around key franchises and newness, and driving elevated consumer engagement through sharper alignment across product, marketing and marketplace execution. 
Building on the encouraging response to key styles, our teams are hyper-focused around a key action plan to deliver the UGG brand's largest quarter in its nearly 50-year history. We will support peak shopping periods with coordinated marketing and enhanced digital experience and compelling product storytelling anchored in our Gift the Feeling holiday campaign. Throughout the third quarter, we remain disciplined in how we drive digital conversion and execute peak shopping periods while managing promotions selectively to protect the long-term health of the brand. I'm excited to see the brand activations come to life this holiday season. 
With that, I'll now hand over the call to Steve, who will provide more detail on our second quarter financial results and updated fiscal year '27 outlook.

**Steve Fasching** (Executives):
Thanks, Stefano, and good afternoon, everyone. As Stefano outlined, second quarter performance reflected a combination of continued international momentum and solid performance in multi-brand environments, combined with softer U.S. DTC trends and fulfillment challenges associated with our EMEA third-party logistics transition. As the quarter progressed, the U.S. marketplace became increasingly promotional. However, we remain disciplined in how we manage the marketplace, protecting full price selling and prioritizing the long-term health of our brands. That discipline is reflected in our financial results.
While revenue came in slightly below our expectations, our continued focus on full price selling and expense management contributed to exceptional gross margin and earnings per share performance. Importantly, these results demonstrate the flexibility and the resilience of the Deckers operating model even in a more pressured environment. As we execute against the actions Stefano outlined, our financial strength gives us the capacity to continue investing behind our brands while remaining disciplined in how we allocate resources. We believe that balance, protecting profitability today while investing behind our most compelling long-term opportunities remains fundamental to how we aim to create sustainable value over time.
Now let's get into the details of second quarter results. Second quarter fiscal 2027 revenue came in at $1.48 billion, representing an increase of 3.5% versus the prior year. Performance in the quarter was driven by HOKA and UGG, which increased 7% and 4% versus last year, respectively. And our Other Brands segment was down 54% versus last year, primarily due to lapping the final quarter of impacts related to the wind down of stand-alone operations for the Koolaburra brand. 
As Stefano mentioned, we saw some top line pressure against our original expectation for the quarter as a result of shipping delays related to our European 3PL transition as well as some e-commerce softness. The amount of the 3PL shipment delays impacting the quarter was approximately $22 million. The softness in our domestic DTC business was largely offset by better-than-expected wholesale sell-in across the globe.
Gross margins for the second quarter was 60.5%, up 430 basis points from last year's 56.2%. Second quarter gross margin included an approximate 310 basis point benefit from IEEPA tariff refunds net of cost sharing arrangements with our independent manufacturers. The underlying 120 basis point improvement was driven by favorable full price selling and favorable product mix. SG&A dollar spend for the second quarter was $506 million, up 6% versus last year's $477 million. The total SG&A expense was below our prior expectations for the quarter, reflecting cost management actions to better align spend with lower revenue growth, while marketing and technology remained the primary drivers of year-over-year investment.
This led to an operating margin of 26.3%. Excluding the net IEEPA refund benefit, our operating margin was 23.2%, 40 basis points above last year's 22.8%. Our tax rate was 22.4%, which compares to 21.7% in the prior year quarter. During the second quarter, we repurchased approximately $299 million worth of shares at an average price of $93.65. Over the first 6 months of fiscal year 2027, we have repurchased $637 million, representing approximately 5% of our outstanding common stock, pacing well ahead of what we signaled at the beginning of the year. This continues to demonstrate our commitment to returning capital to shareholders through disciplined share repurchases while utilizing our strong free cash flow. As of September 30, 2026, the company had approximately $4.4 billion remaining under its stock repurchase authorization.
These results culminated in diluted earnings per share of $2.31 for the quarter, which is $0.49 above last year's $1.82 diluted earnings per share, representing EPS growth of 27%. Excluding the net impact of the IEEPA tariff refunds and related interest, diluted earnings per share was $2.03, representing growth of 11.5% versus last year. Turning to our balance sheet. At September 30, 2026, we ended September with $1.2 billion of cash and equivalents. We continue to tightly manage inventory, which was up 3% versus the same point in time last year to $861 million. And during the period, we had no outstanding borrowings.
Now moving into our updated outlook for fiscal year 2027. As Stefano outlined, our updated outlook reflects a measured approach to revenue growth in the current landscape, maintaining our focus on protecting brand health and profitability. Importantly, we are maintaining our operating margin outlook and in large part, maintaining our prior EPS expectations before the benefit of net IEEPA tariff refunds. Then with the net impact of refunds received to date, we are increasing our full year EPS outlook. With that in mind, let me walk you through our expectations for fiscal year 2027. Total company revenue is now expected to be in the range of $5.7 billion to $5.725 billion, with HOKA now increasing by a high single-digit percentage versus last year and UGG now increasing by a low single-digit percentage.
We are increasing our gross margin expectation to now be approximately 58.5%, reflecting slightly better performance as well as the approximate $88 million IEEPA tariff refund benefit in cost of sales, which is net of cost sharing arrangements with our independent manufacturers for amounts received to date in both the second and third quarter, representing approximately 90% of the amounts we have submitted. We have not factored any remaining unreceived amounts in our forward-looking guidance. SG&A is now expected to be approximately 35.5% of revenue as we manage costs with discipline and reduced dollar spend in response to lower revenue growth expectations, resulting in a slightly higher percentage of revenue, with these all culminating in a raised operating margin expectation of approximately 23%, inclusive of the net IEEPA tariff refunds received to date.
Our effective tax rate is still projected to be approximately 23% and we now expect diluted earnings per share in the range of $7.80 to $7.95. This earnings per share guidance now includes IEEPA net tariff refunds and associated interest received to date and assumes share repurchases with a value of $1 billion in fiscal year 2027. Excluding the benefit of IEEPA net tariff refunds received that are now reflected in our outlook, gross margin would be increasing to 57% and our full year operating margin would still be slightly better than 21.5%, highlighting our discipline and expected preservation of high-quality selling.
To provide a little insight on the third quarter, as we are comparing to a very strong quarter last year, we are expecting third quarter total company revenue growth to be in the low single digits with UGG expected to grow low single digits and HOKA anticipated to deliver low to mid-single digits in the third quarter. Our expectations have factored continued strength internationally, along with anticipated ongoing pressures in the U.S. market, primarily impacting DTC. Third quarter diluted EPS is expected to be in the range of $3.52 to $3.60, which includes an IEEPA net tariff refund benefit of approximately $0.24. With this third quarter context in mind and our updated full year outlook, we recognize this implies acceleration of revenue growth in the fourth quarter for HOKA. This expectation reflects our confidence in continued international demand signals and includes the benefit of planned global product launches Stefano discussed earlier. As always, these forward-looking statements are subject to the risks Erinn outlined at the beginning  of the call.
In closing, our second quarter results represent the flexibility and the resilience of the Deckers operating model. Our high levels of profitability and strong balance sheet provide the opportunity to make targeted investments that we believe can support future market share gains and drive sustainable long-term growth. 
Thanks, everyone. I'll now turn the call back to Stefano for his final remarks.

**Stefano Caroti** (Executives):
Thank you, Steve. As we look ahead, we remain confident in the power of HOKA and UGG and the significant long-term opportunities in front of both brands. We recognize that the consumer landscape continues to evolve and we are operating with the agility and discipline required to respond. We will remain laser-focused on protecting our premium brand positioning, driving growth with a high degree of full-price business, managing inventory with discipline, building clear channel and franchise segmentation while preserving industry-leading levels of profitability. 
Fundamentally, our long-term goals remain intact and we believe in the significant runway ahead for both HOKA and UGG. Our brands are strong. Our balance sheet provides flexibility and our operating model allows us to move decisively without sacrificing the long-term health of our brands. We believe that this combination positions Deckers well to navigate the near term and capture the substantial opportunities ahead. 
Before turning to Q&A, I'd like to mention a Board update we announced today. We are pleased to welcome Rati Sahi Levesque to the Deckers Board effective December 1. Rati brings more than 15 years of leadership experience in the retail industry with deep expertise in digital innovation, brand positioning, elevating brands online and consumer engagement. I'm super excited to have Rati join the Board and bring her expertise, especially her deep knowledge within the digital commerce channel. We look forward to working with Rati to advance our disciplined growth strategy.
I also want to thank Lauri Shanahan, who will retire from the Board when Rati joins. Lauri has been a tremendous asset to me and to Deckers through a period of exceptional growth. Her knowledge, passion and insights have been incredibly valuable and we're grateful for Lauri's immense contribution, dedication and service to Deckers. We wish her all the best. 
Thank you for joining us today. We'll now open the call for questions.

**Operator** (Operator):
[Operator Instructions] Our first question is coming from Jay Sole with UBS.

**Jay Sole** (Analysts):
I'm going to start with one question, then I do have a follow-up. Stefano, clearly, you're protecting the health of the brand and playing the long game, lowering the guidance for both brands right now to high single digit and low single digit. How do we think about the long-term guidance that we talked about in May with HOKA being a -- potentially growing low double digits through fiscal '30 and UGG being mid-single digits. Can you get back to that algo going forward next year? If so, how? Just if you can tell us how you feel about that, that would be great to start.

**Stefano Caroti** (Executives):
Yes, of course. I think we're only 6 months into the guidance we shared. The near-term challenges do not change my belief in our brands and their potential for growth. As you know, growth is never a straight line. And in this environment, we don't want to trade brand equity for short-term revenue. We need to manage the next couple of quarters with discipline. At the same time, we need to keep investing in the opportunities that will drive long-term growth. And the discipline starts really with the quality of our growth. Not all growth is healthy, not all growth is profitable, not all growth is brand enhancing. And I assure you, we'll compete aggressively but we're not participating in the race to the bottom. 
Experience has taught really all of us that the right approach in this environment is to continue to build your brand, to keep inventories tight and to really focus on full price selling. So our brands continue to be healthy, engagement is strong. Our strategy, we believe, is sound and our premium model continues to support attractive margins. So our vision remains largely intact at this point in time.

**Steve Fasching** (Executives):
Yes, Jay, it's Steve. Just to kind of add on that. I think the most important thing is these brands are healthy and we're controlling them in the marketplace. And so the takedown that you're seeing reflected in this year is more an indication of what we're seeing in the current environment. It is not indicative of what we see for these brands kind of going forward. So the brands are in healthy shape. This is our ability to control the market and to control pricing and margins and profitability. 
And we just think given some of the pressures that we're seeing in the market, some of the level of promotion that's going on in the market, especially with our competitors, this is the right step for us and for our brand health. And in the long term, these brands will continue to do well. And I would just be careful about kind of extrapolating what we're doing in a quarter or 2 into any indication of what this represents for the brand over the long term. We believe and have high confidence in what these brands can do over the long term.

**Jay Sole** (Analysts):
Got it. I mean that makes total sense. If I can follow up on that. Steve, obviously, I think gross margin this quarter better than the Street had modeled, even though wholesale grew a lot faster than DTC. Can you just talk about what drove the gross margin upside? And then maybe, Stefano, obviously, there's a lot of promotions out there from your competitors in the athletic footwear space across the wholesale channel. When do you think the marketplace gets clean? When do you think that sort of like just maybe irrational pricing that's out there sort of gets back to a more rational level where maybe full price selling doesn't get hit so much?

**Stefano Caroti** (Executives):
Yes. You go first.

**Steve Fasching** (Executives):
Yes, I'll start first. So Jay, kind of in terms of that 120 basis point improvement that we talked about outside...

**Jay Sole** (Analysts):
Ex IEEPA refunds, ex IEEPA tariff refunds.

**Steve Fasching** (Executives):
So that really was kind of split evenly between full price selling and product mix. And so I think it was -- as we look at it, what drove that, it was higher-margin products selling through better as well as us maintaining our full price selling environment. So where we saw others being more promotional or heavily promotional, we stayed out of that. We were not getting as aggressive in our promotion levels. We do know that weighed on our DTC performance in the U.S. as a result. But again, to Stefano's point, we don't want to chase revenue that is not productive to the brand or profitability. And so in pulling back on that, we actually performed better from a margin perspective.

**Stefano Caroti** (Executives):
If you're concerned about the marketplace and how soon it will be clean, Jay, I don't have a crystal ball but what I see is that the second -- summer '27 and the fall will look better. What I can assure you is that in the transition of our models, there was a bit still of an overhang of Clifton 10 when we introduced Clifton 11, but we'll be very, very clean of Bondi 9 when we introduce Bondi 10 in January. So I'm confident that we will be quite clean in the marketplace and that will allow us to continue to drive full price business.

**Steve Fasching** (Executives):
Yes. And I think just one more thing to add on that, Jay, is, look, we're also watching to see what competitors are doing. We don't want to enter that race to the bottom. There's a lot of promotional product out there. There's a lot of product in the inventory that's weighing, especially in the athletic footwear space. Our belief is, if we steer clear of that, it maintains better brand health over the long term. You're seeing in the current quarter how it's driving better margins. So this will serve us better in the long run. And that's really a big driver of, again, the reduction.

**Operator** (Operator):
Our next question is coming from  Adrienne Yih with Barclays.

**Adrienne Yih-Tennant** (Analysts):
Stefano, I guess my question will still be on the promotional environment. Is it -- we know that there is kind of an excess of inventory in kind of that lifestyle category but it now also sounds like it's kind of also in the performance category. Is it broadly that athletic footwear in general is promotional and, therefore, you end up competing against lifestyle products that are also promotional in the marketplace? 
And then secondarily, UGG is -- it's really in my mind and the callout has been -- it really is UGG's brand moment, a little bit more on the brown shoe, a little bit of a nonathletic look to it. So I guess the question there is, are you holding back some sell-in because it is promotional out there? Do you see the order book sort of building into spring/summer? As I've said before, I think that you have some of the most newness that you've had in a couple of years and it really looks fantastic. So just a little bit more color commentary on the sales mix there.

**Stefano Caroti** (Executives):
Yes. Adrienne, let me start with UGG. Buy now, wear now is real and consumers are purchasing closer to need. To your point, what is very encouraging is that our 360 strategy is paying off, and it's really working across categories and also seasons and wearing occasions. Our growth is increasingly driven by sneakers, shoes, flats, clogs, apparel and consumers are indeed responding to newness. Keep in mind that we've also been allocating our key styles to ensure scarcity of full price selling. So some of the new products that the team has delivered, Quill, Zora, Evelina Clog, have been really standout. And the way that we've also dimensionalized the Lowmel franchise has been really resonating. So we are looking forward to have -- things are slower than we would like at this present time, but we're confident the consumer will show up because the brand is super healthy and consumer engagement is strong.

**Steve Fasching** (Executives):
Yes. On the first question, Adrienne, maybe I'll take a first shot and Stefano can jump in. In terms of kind of the difference between performance and lifestyle, clearly, I think one dynamic that we're seeing in the current environment is some people are wearing performance as lifestyle. So any time you have heavy promotion in performance, it is carrying over to an individual who may be wearing performance for lifestyle. So that is creating kind of this promotional cloud, I think, over the environment. That's what we're trying to stay out of. 
Clearly, there are going to be elements that will always be promotional, your closeout product and so forth. What we don't want to get into is a heavy promotional environment where you're seeing a lot of promotion across multiple franchises. And that includes both brands. And so this is just our step to say some of our competitors want to be very promotional. We don't need to enter that competitive promotional environment. Our brands are healthy. We can maintain better health just by staying clean with a bigger focus on that fuller price sell.

**Operator** (Operator):
Our next question is coming from Laurent Vasilescu with BNP Paribas.

**Laurent Vasilescu** (Analysts):
I wanted to ask, Steve, Stefano, I think at the beginning of the year, you guys called out that HOKA DTC would outpace HOKA wholesale. I'm just curious -- and I think on UGG, it was supposed to be an equal balanced growth between both channels. So with the revised guidance, any chance you can give us some updated thoughts on how we should think about those channels across both brands for the year? And then I've got a follow-up question on the gross margin.

**Steve Fasching** (Executives):
Yes. Sure. Just related on HOKA, I think from an international perspective, we still believe that to be true, what you stated. Where we're seeing the pressure more is in the U.S. market. So that dynamic has changed a little bit with the pressure that we're seeing in the U.S. and where we're trying to remain as clean as possible within our e-commerce platform, especially. That's where we're seeing some of the pressure where consumers may be finding product through wholesalers, through wholesale online at heavier promotions. We don't want to enter into that promotional environment within our e-commerce. 
Again, we'll have some level of promotion but we don't want to get overly promotional. That's putting a little bit of pressure on that DTC growth. So that dynamic within the U.S. has shifted a little bit where we'll now expect to see wholesale growth in the U.S. outpace DTC growth.

**Laurent Vasilescu** (Analysts):
Okay. Very helpful. And then I wanted to ask a housekeeping question. The $22 million shift, is that -- in Europe, is that a shift, Steve? Or is that kind of just lost sales? And then on the gross margin question specifically, ex IEEPA tariffs, they were up. I think you were calling them to be down for 2Q. For 3Q, it's a little bit hard for us to model so far but -- because there was an IEEPA benefit in 3Q on EPS. But should -- ex IEEPA, should we think about your 3Q gross margin up or down?

**Steve Fasching** (Executives):
Yes, sure. So first, starting on the European shift, that $22 million, it's not a full shift into Q3. Some of it will get potentially pushed out longer and some of it may get canceled, right? So again, we'll have to see how the environment plays out. Right now, the way we've modeled it is not all of it carries through into the back half of the year. A portion of it will move in and some of it is risk of cancellation. In terms of the gross margin, I think your question was how does it compare to the prior -- to the kind of the prior guide. We didn't give a prior guide kind of on the quarter. 
Really, the assumption, if you kind of look at a bit of Q3 is, there is the IEEPA benefit, which we haven't necessarily called out, but you can calculate it. That's going to drive an overall net improvement in the gross margin. There will be some slight offset to that, that we're anticipating, which is higher freight rates as well as a slight increase in the promotion environment. So again, we won't get highly promotional, but we are anticipating the promotional level to increase slightly. So net overall positive, driven by the IEEPA tariff refunds that we've received to date, partially offset by some pressure on rising freight rates and then a slightly increased promotion assumption.

**Operator** (Operator):
Our next question is coming from Sam Poser with Williams Trading.

**Samuel Poser** (Analysts):
I'm just going to follow up on Laurent's question. I believe he asked if compared to last year, how to think about the gross margin -- last 3Q, how to think about the gross margin in 3Q '27 without the IEEPA refund. So that's what he wants. I think that was the question. So I want you to give an answer to it.

**Steve Fasching** (Executives):
Yes. No, I think that's the way we're thinking about it is in terms of kind of compared to last year as well, we will get a net improvement driven by the IEEPA refund and then a partial offset from higher freight rates this year versus last year and a slight increase in promotional activity this year versus last year.

**Samuel Poser** (Analysts):
Okay. All right. The thing is that we're going to have to take out these benefits in Q2 and Q3 of next year. So if you gave us -- like we know that you were at 57.1%, I believe, in Q2 without IEEPA. Why -- can't you just give us where you're guiding without it because we're going to take it out next year anyway, and it's going to be -- all the numbers are going to be wrong unless you give it to us.

**Steve Fasching** (Executives):
Sure, sure. So if I give it to you in terms of last year, last year Q3, we were at 59.8% on the gross margin. And what we're implying is just north of 60% in the current quarter. The way you can break that out is, a little more than 200 basis point IEEPA tariff refund impact, offset by 150 basis points related to mostly freight with a little bit of promo. So up, call it, 210 basis points, off by 150 basis points, that net is the increase you're seeing year-over-year.

**Samuel Poser** (Analysts):
And then with the Bondi transition to the -- from the 9 to the 10, when are you going to break price on the 9 to ensure that you're clean when the 10 comes out in January?

**Stefano Caroti** (Executives):
First of all, it's already pretty clean because the Bondi 9 continues to perform very, very well across the marketplace at full price. I believe the markdown cadence starts around Cyber. But let me get back to you on that, Sam.

**Steve Fasching** (Executives):
Yes. Part of that, Sam, will depend on inventory levels and kind of where we want to go. But to Stefano's point, the sell-through of Bondi 9 right now continues to be very strong at full price.

**Operator** (Operator):
Our next question is coming from Jonathan Komp with Baird.

**Jonathan Komp** (Analysts):
I want to follow up just on HOKA and the U.S. wholesale marketplace. When you look at indicators of sell-through in wholesale, are you seeing any similar dynamics where you maybe are losing out on some sales to brands that are being more promotional? And as you think about total growth for the wholesale category for HOKA, how far of a runway or visibility do you have on the distribution front, some of the new doors that could sustain total growth even though it's a more difficult sell-through marketplace?

**Stefano Caroti** (Executives):
Yes. Let me start with the second part, Jon. As you know, we're still in much less distribution than many of our peers in sporting goods, athletic specialty especially, in run specialty, we're pretty covered. So ample opportunities for us in terms of expansion. And now that we have a line, a collection, an offer that allows us to segment the market more purposefully, we'll be able to differentiate accounts more meaningfully. So starting with spring, you should see a continued thoughtful expansion of our wholesale distribution in the U.S., which will continue in the fall and not just in the U.S., in Europe as well because the line now allows us to do so. Regarding the first part of your question, we continue to gain share above $120 and we continue to be the leading performance running brand in the U.S. at a premium price point. So where we potentially lose share to others are the more compressed price points below $120, where the competition is greater.

**Jonathan Komp** (Analysts):
Okay. And can you comment at all, when you look at a few of the new model changeovers that didn't go as planned, are you making significant changes as you look ahead? Or is it more tied to the product features on the Bondi 10 and others? Just any more color there.

**Stefano Caroti** (Executives):
No, no, no. It's a good question. So as I referred in the remarks, some products didn't go as planned. I referred to Transport, Kawana and Solimar. Others have performed super well. Speedgoat 7, Arahi 9, Stinson 8 continue to do well, are doing very well across the marketplace. I am very encouraged by what Robin and team have crafted and created for spring/summer '27 and fall '27. The lineup of new products and I'm talking about not just Bondi and Clifton, which are -- have been received very, very well but the supporting cast. Mach Pro, well received, booked super well. Mach 8 early in the fall, best Mach to date, also been very, very well received by the market. 
So the supporting lineup of products and some of the upgrades that are coming across performance and lifestyle will be very strong. Cielo 70 will help us attract a new consumer. And these extensions of Bondi and Clifton with material applications and colors to appeal to a lifestyle consumer, also very well received. So I am very confident that the lineup we have, the collection we have for spring and fall will allow us to get the U.S. market back to growth.

**Steve Fasching** (Executives):
Yes. I think on that, Jon, too, some of the updates that you'll see in '27 are more significant than the updates you saw in '26. And that's kind of really what Stefano was highlighting is that the updates you saw on some of these were not as significant as what you will see next calendar year.

**Operator** (Operator):
Our next question is coming from Peter McGoldrick with Stifel.

**Peter McGoldrick** (Analysts):
I wanted to ask on the UGG brand as we enter holiday. With UGG wholesale performing better than DTC, can you help us think about the assumptions around retail sell-through and replenishment embedded in the low single-digit growth outlook for the December quarter? And then how do those assumptions compare to the current trends you're experiencing in the marketplace right now?

**Steve Fasching** (Executives):
Yes, I'll start. Maybe just a little bit about kind of how we're thinking about the setup. So coming out of Q2, we definitely saw some of the impact on the consumer. I think as we mentioned a little bit in the prepared remarks, we are seeing consumers kind of buying closer to wearing occasions. We're also seeing sales events driving kind of higher level of sales as opposed to kind of routine level of sales. So that is how we're looking at it. As we mentioned and Stefano talked about the excitement around some of the new product, we think that's going to garner consumer attention, especially as we're getting closer to season. As you know, we just opened up our UGG season. And so we've seen some strong early reaction to the opening of UGG season that is encouraging. 
But again, it's still very early days in that. A lot of UGG sales will come in November kind of through December. So still very early on in that. In terms of the assumptions then, we aren't necessarily making the same assumptions around reorders that we had last year because recall that last year was a very strong season, the setup, the weather contributed very well. That drove a very, very strong additional order business for us in December and January. So we're not anticipating that same level of reorder. And -- but we'll see what happens. We think our brands are well positioned in the market. If the consumers show up, we believe we've got the product out there that will resonate, and we'll see what happens.

**Stefano Caroti** (Executives):
Yes. To Steve's point, the way consumers are responding to newness is fantastic. And some of the heritage styles that we're bringing back like Sunburst Tall, Disquette Heritage, Classic Mini Dipper Legwarmer are all performing well. So that gives us confidence that the consumer will show up.

**Peter McGoldrick** (Analysts):
Okay. And then on the HOKA opportunity and zooming out a bit, I wanted to ask how the current environment is influencing your multiyear opportunity to penetrate more meaningfully in athletic specialty sporting goods and run specialty environment.

**Stefano Caroti** (Executives):
Our strategy doesn't change. As we shared previously, we're going to slowly expand where it makes sense. And now that the offer gives us more differentiation opportunities, that's what we'll be doing. So our strategy and outlook doesn't change for HOKA.

**Operator** (Operator):
Thank you. This concludes today's Deckers Brand Second Quarter Fiscal 2027 Earnings Conference Call. Please disconnect your line at this time and have a wonderful day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DECK_Q1_2027_Earnings_Call_20260723.md
- 2026-07-23｜Steve Fasching (CFO)｜guidance：FY27 營收財測區間維持不變。（原話："range of $5.86 billion to $5.91 billion"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：FY27 毛利率預期上調至略高於 56.5%。（原話："now be slightly better than 56.5%"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：FY27 稀釋 EPS 財測上調 $0.05 至 $7.35–7.50。（原話："range of $7.35 to $7.50, which represents a $0.05 increase"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：第二季合併營收預期年增約 5%。（原話："consolidated revenue up approximately 5% in Q2"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：第二季 EPS 財測區間。（原話："earnings per share in the range of $1.73 to $1.78"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：第二季毛利率預期下滑，原因為關稅與運費上升。（原話："gross margin is expected to be down due to tariffs and"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：下半年成長率預期加速。（原話："expect growth rates to accelerate in the second half"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：下半年加速主要來自 HOKA 與國際批發及經銷商業務。（原話："driven primarily by the HOKA brand and our international"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：第二季其他品牌預期年減約 50%，歸因於精簡品牌組合。（原話："other brands are expected to be down approximately 50%"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：財測的前瞻關稅稅率假設由 10% 調高至 12.5%。（原話："go-forward tariff rate assumption to 12.5% from the"）
- 2026-07-23｜Steve Fasching (CFO)｜guidance：財測未納入任何關稅退款假設。（原話："not included any assumptions regarding refunds"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：第一季毛利率 56.4%，年增 60 bps。（原話："Gross margin for the quarter was 56.4%, which is up 60"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：毛利率橋接：全價銷售加通路與品牌組合貢獻約 110 bps、匯率約 40 bps。（原話："about 110 basis points. And then FX, we benefited a little"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：毛利率橋接：第一季關稅造成約 150 bps 年增負面影響。（原話："impact of about 150 basis points."）
- 2026-07-23｜Steve Fasching (CFO)｜margin：第一季折扣出清（closeout）管理較佳，約貢獻 60 bps。（原話："60 basis points."）
- 2026-07-23｜Steve Fasching (CFO)｜margin：管理層稱出清帶來的順風屬第一季獨有，其餘季度促銷節奏假設無重大變化。（原話："assumed any significant change in the promotional cadence"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：管理層預期其餘季度毛利率相較去年同期會有壓力。（原話："we will see some pressure on the gross margin"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：第一季是全年四季中關稅年增逆風最大的一季。（原話："headwind in terms of the 4 quarters that we will experience"）
- 2026-07-23｜Stefano Caroti (CEO)｜margin：UGG 產品組合轉向帶動該品牌毛利率提升。（原話："favorable product mix shifts that supported higher gross"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：第一季 SG&A 為 $420M，年增 13%。（原話："quarter was $420 million, which is up 13% from last year's"）
- 2026-07-23｜Steve Fasching (CFO)｜margin：關稅稅率上調對毛利率的影響集中在第三季尾與第四季，未拆出金額。（原話："some impact to it in Q3 and more impact on a full Q4 basis"）
- 2026-07-23｜Steve Fasching (CFO)｜commitment：FY28 起開始釋放營業費用槓桿。（原話："begin delivering operating expense leverage in fiscal year"）
- 2026-07-23｜Stefano Caroti (CEO)｜commitment：維持拉式需求模式為核心承諾。（原話："preserving a pull model of demand and investing with purpose"）
- 2026-07-23｜Stefano Caroti (CEO)｜commitment：承諾維持高端全價的全球通路。（原話："maintaining a premium full-price global marketplace."）
- 2026-07-23｜Stefano Caroti (CEO)｜commitment：UGG 男裝目標佔營收 20% 以上（逐字稿記為 15% 的更正）。（原話："the goal is to get it to 20% or higher"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：第一季回購約 $338M，均價 $103.79。（原話："we repurchased approximately $338 million worth of shares"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：回購授權剩餘約 $4.7B。（原話："approximately $4.7 billion remaining"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：EPS 財測假設回購金額約為 FY27 自由現金流的 80%。（原話："equal to approximately 80% of our projected fiscal year"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：若收到關稅退款，將部分返還分攤成本的夥伴。（原話："return some of those funds to our partners"）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：關稅退款預期非一次性入帳。（原話："We don't see it necessarily as a lump sum."）
- 2026-07-23｜Steve Fasching (CFO)｜capital_allocation：季末存貨 $808M，年減 5%。（原話："Inventory was $808 million, down 5% versus the same point"）
- 2026-07-23｜Stefano Caroti (CEO)｜product：HOKA 全球營收 +8% 至 $704M。（原話："first quarter increased 8% versus last year to $704 million."）
- 2026-07-23｜Stefano Caroti (CEO)｜product：HOKA 全球批發營收僅 +3%，管理層稱符合國際出貨時點差異預期。（原話："global revenue increased 3% versus last year, aligned with"）
- 2026-07-23｜Stefano Caroti (CEO)｜product：Clifton PRO 上市約兩週已有帳戶補單。（原話："some accounts already placing reorders."）
- 2026-07-23｜Stefano Caroti (CEO)｜product：Clifton PRO 採選擇性策略性批發分級，Clifton 11 走較廣批發配銷。（原話："PRO launched with selective strategic wholesale segmentation"）
- 2026-07-23｜Stefano Caroti (CEO)｜product：EMEA 批發出貨實績與補單創季度紀錄。（原話："robust wholesale sell-through and another quarterly record"）
- 2026-07-23｜Stefano Caroti (CEO)｜product：下半年 HOKA 依通路分級推出不同款式，含運動用品通路新款 Fly Pace。（原話："a new shoe for sporting goods called the Fly Pace."）
- 2026-07-23｜Stefano Caroti (CEO)｜product：HOKA 預期生活風格品類在下半年帶來更大貢獻。（原話："you'd like to see a bit more of an impact in the second"）
- 2026-07-23｜Stefano Caroti (CEO)｜customer：管理層表示 UGG 訂單簿沒有取消。（原話："No, no cancellations to the order book, Laurent."）
- 2026-07-23｜Stefano Caroti (CEO)｜customer：HOKA 下半年將新增運動用品等通路的優質夥伴，不給家數。（原話："to provide specific numbers, but you'll see an expanded"）
- 2026-07-23｜Stefano Caroti (CEO)｜customer：管理層稱今年消費者買氣更偏事件驅動。（原話："I think we're seeing a bit more event-driven buying this"）
- 2026-07-23｜Stefano Caroti (CEO)｜competition：稱 HOKA 在效能跑鞋與越野跑鞋維持或取得市占。（原話："we continue to maintain or gain share in performance run"）
- 2026-07-23｜Stefano Caroti (CEO)｜competition：引用 Circana 資料稱 $120 以上價帶取得市占。（原話："we've gained share above $120, which is fantastic."）
- 2026-07-23｜Stefano Caroti (CEO)｜risk：承認歐洲消費者壓力高於美國，起因為能源價格上升。（原話："consumer in Europe is probably a bit more pressured"）
- 2026-07-23｜Stefano Caroti (CEO)｜risk：開場稱消費環境仍承壓。（原話："continue to see people showing up for the brands they love"）
- 2026-07-23｜Stefano Caroti (CEO)｜risk：被問暖冬風險，稱即使暖冬仍預期持續表現。（原話："even if we had a warmer winter, we believe we will continue"）
- 2026-07-23｜Steve Fasching (CFO)｜risk：國際批發與經銷商出貨時點移至今年下半年，管理層稱是物流變動而非需求變動。（原話："It's not any change in assumption in demand, right?"）
- 2026-07-23｜Steve Fasching (CFO)｜risk：第二季受去年 Koolaburra 品牌收尾的基期影響。（原話："impact from lapping last year's wind-down of the Koolaburra"）

### 問答異常語氣（迴避／改口／保留）
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Peter McGoldrick 請 CFO 估算關稅假設由 10% 升至 12.5% 的影響（bps 或 EPS）｜答法：CFO 說「We haven't called it out」，未給金額，只說影響在第三季尾與第四季，建議分析師自行在模型中計算
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Sam Poser 問 HOKA 官網促銷與出清對第一季營收與毛利率的貢獻幅度｜答法：CFO 說「I'm not going to give you kind of specifics」，只說包含在毛利率超預期內、Clifton 為其中一部分
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Sam Poser 問 UGG 美國通路是否在收縮小客戶、調整配銷｜答法：CEO 先承認「you've seen some changes」，隨後稱策略不變、「no major changes」，未回應去年取消訂單的零售商是否被調整
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Rick Patel 問 HOKA 新增批發夥伴的據點數與對下半年加速的貢獻｜答法：CEO 表示不提供具體數字，只說下半年會有新夥伴與擴大配銷
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Laurent Vasilescu 追問第二季 HOKA 全球 DTC 成長如何看｜答法：CFO 兩次回答都停在「not a significant change」與「significant growth」，未給 DTC 成長數字
- DECK_Q1_2027_Earnings_Call_20260723.md｜問：Blake Anderson 問下半年 HOKA 的 DTC 與批發相對規模｜答法：CFO 只說加速來自物流時點，未回答批發是否會高於 DTC，也未給兩通路的幅度

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
{"date":"20260706","verdict":"進場","role":"衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"HOKA 維持低雙位 cc growth（從 $2.59B 走向 $3.5-4B），Q1 高單位為 wholesale timing 一次性","columns":{"2Y 驗證":"FY27 HOKA +低雙位（管理層 guide）；Q1 高單位後 Q2-Q4 回站 ≥ +10%","5Y 驗證":"HOKA 達 $3.8-4B（FY29-30）","10Y 驗證":"HOKA 全球 premium running share ~10-12%（vs 當前 ~23% run-specialty 並列 Brooks）","數字門檻":"HOKA quarterly cc growth ≥ 10%；全價銷售 ≥ 80%","來源":"Q4 FY26 法說 2026-05-21 / FY27 guide","漂移觸發":"連 2 季 ＜ 10% 削弱；連 3 季 ＜ 8% 反轉"}},{"id":"H2","text":"UGG 維持 mid-single mature 穩定（不從 +8% 滑入負成長）","columns":{"2Y 驗證":"FY27 UGG +mid-single；冬季 Q3 sell-through 穩","5Y 驗證":"UGG 維持 $2.8-3B 穩定","10Y 驗證":"UGG cozy boot 全球 share 維持 ~25-30%","數字門檻":"UGG cc growth ≥ +3%；Q3（冬季）＞全年 50%","來源":"FY26 +8% / FY27 guide mid-single","漂移觸發":"連 2 季 ＜ 0% 削弱；單季 ＜ −10% 反轉"}},{"id":"H3","text":"Tariff 可吸收，GM 維持 ≥ 55%（越南 75% 採購、20% 關稅、$185M 毛衝擊、~$75M 靠提價 offset）","columns":{"2Y 驗證":"FY27 GM ≥ 56%（guide 56.5%）","5Y 驗證":"5Y avg GM ≥ 55%","10Y 驗證":"結構性 GM ≥ 53%（即使 tariff 持續）＋ 越南採購降至 ＜ 70%","數字門檻":"季度 GM ≥ 55%","來源":"FY27 公司 guide 56.5% / 5/21 法說","漂移觸發":"連 2 季 ＜ 55% 削弱；連 2 季 ＜ 53% 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"HOKA 減速從一次性變結構性 — Q1 FY27 已掉到高單位，若非 wholesale timing 而是 On/Nike 搶走 race-day credibility → 掉低單位","columns":{"對應":"H1","時間尺度":"🔥 中期（2-4 季）","監測指標":"HOKA cc growth；run-specialty sell-through；international growth","警戒閾值":"連 2 季 cc ＜ 10% 削弱；連 3 季 ＜ 8% 反轉（trap 升 🔴）"}},{"id":"R2","text":"UGG 高 base 冬季反轉 — Q3+Q4 佔 UGG 75%+，若時尚輪替轉向 retro non-cozy → 佔 50% Rev 的品牌 YoY 轉 −5% ~ −15%","columns":{"對應":"H2","時間尺度":"🔥 中期（4-6 季，季節性）","監測指標":"UGG quarterly cc；冬季旺季趨勢；Gen Z sentiment","警戒閾值":"連 2 季 cc ＜ 0% 削弱；單季 ＜ −10% 反轉"}},{"id":"R3","text":"Tariff 升級至 25-30% — 越南 75% 集中，Trump 政府進一步上調風險，GM 結構性壓 100-150bp","columns":{"對應":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"US Trade Rep 通報；提價接受度；越南採購佔比","警戒閾值":"連 2 季 GM ＜ 55% / 越南採購未降 ＜ 70% 24 個月"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"HOKA cc growth 連 2 季回站 ≥ 低雙位數（證 Q1 高單位是 wholesale timing 一次性）或 回檔至 BB 下軌 $92 附近 thesis 完整","irr_base_pct":9.6,"ev5y_pct":51.5,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星持倉","signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":6.0,"ev5y_pct":51.5,"irr_base_pct":9.6,"max_dd_pct":-40.0,"bull_5y_price":218.5,"bear_5y_price":86.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"HOKA cc growth 連 2 季回站 ≥ 低雙位數（證 Q1 高單位是 wholesale timing 一次性）或 回檔至 BB 下軌 $92 附近 thesis 完整","price_at_dd":104.69,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
