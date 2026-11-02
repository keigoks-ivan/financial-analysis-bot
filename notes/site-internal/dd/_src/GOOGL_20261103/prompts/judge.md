你是 stock-analyst **v20 判斷 agent**，標的 GOOGL（20261103）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"GOOGL","date":"2026-11-03","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GOOGL_20261103/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GOOGL_20261103/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":127.577,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）"},"note":"未查得 Q3 單季共識營收；媒體稱 EPS 與營收低於預期，未採（非 IR 來源）"},{"id":"f_kpi1_gaap","label":"GAAP 營業利益","value":40.576,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）"},"note":"未查得"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":31.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）；Q3 2026 earnings call 逐字稿 2026-10-28"},"note":"未查得"},{"id":"f_kpi3_non_gaap","label":"Non-GAAP 營業利益／利益率","value":null,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）"},"note":"不適用","needs_sonnet":true},{"id":"f_kpi6_google_cloud","label":"Google Cloud 營收","value":30.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）；Q3 2026 earnings call 逐字稿 2026-10-28"},"note":"未查得"},{"id":"f_kpi7_google_cloud","label":"Google Cloud 營業利益／利益率","value":11.121,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn（利益率 36.2%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）；Q3 2026 earnings call 逐字稿 2026-10-28"},"note":"未查得"},{"id":"f_kpi8_google_cloud_backlog","label":"Google Cloud backlog","value":561,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Q3 2026 earnings call 逐字稿 2026-10-28（CFO 發言）"},"note":"未查得"},{"id":"f_kpi9_capex","label":"資本支出（capex）","value":51.355,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）"},"note":"媒體稱共識約 55.09bn（非 IR 來源，僅供參考）"},{"id":"f_kpi10","label":"管理層指引","value":"2026 全年 capex 195–205bn（維持不變）","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"text","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Q3 2026 earnings call 逐字稿 2026-10-28（CFO outlook）"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-28","period":"2026-10-28","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-28"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_googl_gross_margin_pct","label":"GOOGL 毛利率","value":60.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_operating_margin_pct","label":"GOOGL 營業利益率","value":33.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_googl_fcf_margin_pct","label":"GOOGL FCF 利潤率","value":4.19,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_gross_margin_pct","label":"MSFT 毛利率","value":67.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_operating_margin_pct","label":"MSFT 營業利益率","value":47.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_msft_fcf_margin_pct","label":"MSFT FCF 利潤率","value":17.31,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_amzn_gross_margin_pct","label":"AMZN 毛利率","value":50.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_operating_margin_pct","label":"AMZN 營業利益率","value":12.36,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_amzn_fcf_margin_pct","label":"AMZN FCF 利潤率","value":-0.82,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_aapl_gross_margin_pct","label":"AAPL 毛利率","value":48.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAPL.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_aapl_operating_margin_pct","label":"AAPL 營業利益率","value":33.17,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAPL.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_aapl_fcf_margin_pct","label":"AAPL FCF 利潤率","value":29.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAPL.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_meta_gross_margin_pct","label":"META 毛利率","value":81.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_meta_operating_margin_pct","label":"META 營業利益率","value":32.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}},{"id":"f_peer_meta_fcf_margin_pct","label":"META FCF 利潤率","value":11.86,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi4","label":"自由現金流（單季）","value":-9.065,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"USD bn","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）；Q3 2026 earnings call 逐字稿 2026-10-28"},"note":"未查得"},{"id":"f_kpi5_sbc_gaap","label":"SBC 占 GAAP 營業利益","value":21.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-28）","citation":"Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）（SBC 8,630m ÷ 營業利益 40,576m；占營收 6.8%）"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":282.98,"period":"2026-11-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-26.09,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":24.06,"period":"2026-11-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":39.19,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.89 → 16.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.33,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（15.19 → 15.14）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.87,"period":"2026-10-31","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（18.42 → 18.26）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":16.55,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":15.14,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":18.26,"period":"2026-10-31","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-19.58,"period":"2026-07-30 → 2026-10-31","unit":"%","basis":"FY1 共識 EPS 20.58 → 16.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-31","citation":"DD_universe_EPS_estimates_20261031.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":14.77,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":7.38,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝60.8","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":60.8,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.14,"period":"2026-11-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝55.5","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":55.5,"period":"2026-11-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":17.1,"period":"2026-10-31","unit":"x","basis":"分母＝FY1 EPS 16.55，分子＝快照價 282.97","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-31"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.304,"period":"2026-11-03","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-03"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-114767.0,"period":"2026-11-03","unit":"USD m","basis":"yfinance 最新一季：總債務 150331.0、現金 265098.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":12294.0,"period":"2026-11-03","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":3363705.88,"period":"2026-11-03","unit":"USD m","basis":"市值 3478472.88 ＋ 淨負債 -114767.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":499593.88,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（45 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":634498.64,"period":"2026-11-03","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（49 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.73,"period":"2026-11-03","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-03"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-03","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 283.02 / W52 332.67 / W104 262.39 / W250 184.44 / W250 13週斜率 1.49%"},{"id":"f_ma_w52","label":"52 週均線","value":332.67,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":262.39,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":184.44,"period":"2026-11-03","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.49,"period":"2026-11-03","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-03","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 競爭段列出 AI 模型開發商與 AI 產品服務供應商為競爭對手之一，並稱使用者對其他產品「一鍵之遙」","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"We face formidable competition in every aspect of our business, including but not limited to, from: •general purpose search engines and information services; •vertical search engines and e-commerce providers for queries on topics such as those related to travel, jobs, and health, which users may navigate directly to rather than go through Google;","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因素承認新進入者可能提供相似或更好的體驗，消費者可能改變取得資訊的方式，進而降低既有產品效用","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"As new and existing technologies continue to develop, competitors and new entrants may be able to offer experiences that are, or that are perceived to be, substantially similar to or better than ours, and the consumers may change how they obtain information online, potentially reducing the utility of our existing products and services.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 指出 AI 加速器（含 GPU 與自研 TPU）供給產能競爭激烈，競爭者若先搶下產能可能使 Alphabet 成本上升、供給受限","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"industry supply capacity for AI accelerators, including GPUs as well as our custom-built TPUs, is highly competitive and rapidly evolving. If we are unable to negotiate favorable contractual terms or our competitors claim the supply or capacity first, we may face increased costs and supply constraints","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Synergy：Q3 2026 全球雲端份額 Amazon 26%、Microsoft 19%、Google 16%","source":"DatacenterDynamics 報導 Synergy 資料","url":"https://www.datacenterdynamics.com/en/news/synergy-enterprise-cloud-infrastructure-spending-jumped-55-yoy-in-q3/","excerpt":null,"as_of":"2026-10-30","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"ChatGPT 網頁流量份額降至2023年以來低點，Gemini 快速上升","source":"Tom's Guide","url":"https://www.tomsguide.com/ai/chatgpts-traffic-share-hits-lowest-point-since-2023-as-gemini-surges-new-report-exposes-pressure-on-openai","excerpt":"ChatGPT’s traffic share hits lowest point since 2023 as Gemini surges — new report exposes pressure on OpenAI News By Amanda Caswell Published 26 January 2026","as_of":"2026-01-26","retrieved_at":"20261103","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"ChatGPT 仍領先聊天機器人市場但優勢下滑，Gemini 追趕","source":"The Decoder","url":"https://the-decoder.com/chatgpt-still-leads-the-chatbot-market-but-its-dominance-is-slipping-as-googles-gemini-gains-ground/","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#6","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"StatCounter 全球搜尋引擎份額 Google 約90%；ChatGPT 轉介極小","source":"StatCounter Google vs ChatGPT market share","url":"https://gs.statcounter.com/google-vs-chatgpt-market-share","excerpt":"Google Vs Chatgpts Percentage Market Share Google vs ChatGPT Market Share Worldwide - October 2026 Google 99.91% ChatGPT 0.09% Google vs ChatGPT Market Share Worldwide","as_of":"2026-06-30","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K FY2025 揭露：2023、2024、2025 年皆無單一客戶或關聯客戶群占營收超過 10%（總營收 2025 年 402,836 百萬美元）。","source":"SEC EDGAR 10-K FY2025 Item 8 Financial Statements","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"Total revenues $ 307,394 $ 350,018 $ 402,836 No individual customer or groups of affiliated customers represented more than 10% of our revenues in 2023, 2024, or 2025.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"10-K 揭露信用風險管理：應收帳款多為無擔保，公司持續評估客戶信用、限制授信額度，一般不要求客戶提供擔保品。","source":"SEC EDGAR 10-K FY2025 Item 8 Financial Statements（Credit Risks）","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"Accounts receivable are typically unsecured and are derived from revenues earned from customers located around the world. We manage the concentration of our credit risk exposure by performing ongoing evaluations to determine customer credit and we limit the amount of credit we extend. We generally do not require collateral from our customers.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 風險因子：國際營收約占 2025 年合併營收 52%，部分國家付款週期較長、信用風險與付款詐欺較高。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"International revenues accounted for approximately 52% of consolidated revenues in 2025.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Alphabet 管理層稱 AI 算力需求大於供給、預期供給限制持續；Pichai 稱每日都受容量限制，現在要 2027 算力極難","source":"Beri.net: Google Cloud 82% Growth Hides a Serious Supply Problem (summary of Alphabet Q2 2026 results)","url":"https://www.beri.net/article/google-cloud-82-percent-growth-enterprise-ai-supply-constraints-2026","excerpt":"We are capacity constrained on a daily basis.","as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Cloud 積壓訂單約 5,140 億美元（Q2），預計 24 個月內消化 50%，多數於 2027–2028 轉營收；2026 capex 指引上調至 1,950–2,050 億美元","source":"WebSearch summary of Alphabet Q2 2026 results (Beri.net / TechCrunch / Fierce Network)","url":"https://www.beri.net/article/google-cloud-82-percent-growth-enterprise-ai-supply-constraints-2026","excerpt":"Alphabet expects to work through 50% of the backlog over the next \"24 months\", so much of it converts to revenue in 2027 and 2028.","as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"EMARKETER 預測美國媒體廣告 2026 年增 15.6%、2027 年僅增 9.4%，部分來自世足賽與期中選舉等週期因素；IAB 亦提醒 2027 放緩","source":"EMARKETER: IAB raises ad spending forecast for 2026, but marketers should brace for 2027 slowdown","url":"https://www.emarketer.com/content/iab-raises-ad-spending-forecast-2026-marketers-should-brace-2027-slowdown","excerpt":"IAB raised its 2026 US ad growth forecast to 12.3%, mainly on cyclical factors and a strong first half.","as_of":"2026-06-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"IAB/PwC：十家公司取得 2025 年美國網路廣告每一美元的 84.1 美分，占比自 2022 年逐年上升","source":"IAB/PwC via WebSearch summary of EMARKETER/IAB coverage","url":"https://www.emarketer.com/content/iab-raises-ad-spending-forecast-2026-marketers-should-brace-2027-slowdown","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"搜尋案：2025-12 地方法院作出最終判決，限制搜尋分發並要求與特定競爭對手分享搜尋資料與提供syndication；Alphabet 2026-01 上訴，DOJ 與各州 2026-02 亦上訴。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"In August 2024, the US District Court for the District of Columbia ruled against Google, and in December 2025, entered a final judgment requiring remedies, which, among other things, imposes restrictions on how we distribute our services and requires us to share certain search data with and offer syndication services to certain competitors. In January 2026, we appealed the final judgment and moved to pause implementation of certain remedies. In February 2026, the DOJ and state Attorneys General also appealed.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"廣告技術案：2025-04 判決混合（出版商工具排擠對手、廣告主工具與併購不違法）；DOJ 的補救方案含結構性補救，2025-11 結案辯論後待最終判決（截至 10-K）。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"The DOJ's remedy proposal includes structural remedies that could harm our business. Closing arguments were held in November 2025, and we are awaiting a final judgment.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"Q3 FY2026 10-Q 法律事項：廣告技術補救裁決（報稱未判結構性分拆）、歐盟 Android 罰款定案、歐盟廣告技術罰款€3.0bn 上訴中。","source":"SEC EDGAR 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000084/goog-20260930.htm","excerpt":"In September 2026, the Court issued its remedies decision, denying the DOJ's request for structural divestitures of Google's advertising technology assets, instead ordering certain behavioral remedies concerning interoperability, data access, and auction conduct.","as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Alphabet 10-K FY2025 風險因素：供應短缺、漲價、交期拉長可能由關稅、制裁與出口管制、貿易爭端驅動；部分資料中心與裝置元件僅單一或有限來源；國際營收約占 52%，關稅與進出口管制可能增加成本、限制需求或元件取得。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"International revenues accounted for approximately 52% of consolidated revenues in 2025.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國對先進 AI 晶片依 Section 232 課 25% 關稅，2026-01-15 生效，範圍窄，排除供美國資料中心使用的進口；搜尋未見 Alphabet 專屬關稅或出口管制條目。","source":"Thomson Reuters ONESOURCE: Trump administration imposes tariffs on advanced AI chips under Section 232 authority","url":"https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/january-15th/trump-administration-imposes-tariffs-on-advanced-a","excerpt":"advanced AI chips under Section 232 authority Date of publication: January 15, 2026 On January 14, the White House announced significant new trade measures targeting advanced computing semiconductors, marking the latest use of Section 232 national security authorities to reshape U.S. trade policy in the technology sector. Immediate tariff action President Trump signed a proclamation imposing a 25%","as_of":"2026-01-15","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Alphabet FY2025 10-K 風險因素：地緣緊張、制裁、關稅與武裝衝突可能限制其取得零組件或成品的能力","source":"Alphabet Inc. Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":null,"as_of":"2026-02-05","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Alphabet 10-K 揭露其倚賴他公司製造多數成品與設計部分零組件，部分零組件僅來自單一或少數來源（FY2021 10-K）","source":"Alphabet Inc. Form 10-K FY2021 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204422000019/goog-20211231.htm","excerpt":null,"as_of":"2022-02-01","retrieved_at":"20261103","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"報導指 Google 所有 TPU 由 TSMC 製造（Ironwood 用 N3P，下一代 N2），Broadcom 負責設計、MediaTek 協調","source":"Jon Peddie Research: Ironwood, Broadcom, MediaTek and TSMC","url":"https://www.jonpeddie.com/news/ironwood-chetyorka-google-broadcom-mediatek-and-tsmc/","excerpt":"Ironwood chetyorka: Google, Broadcom, MediaTek, and TSMC It takes a village to build an AIP farm. December 1, 2025 Jon Peddie Google is expanding how it builds its AI chips.","as_of":"2025-12-01","retrieved_at":"20261103","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026（2026-10-28 發布）：Alphabet 營收約 $127.6B、年增 25%；Google Search 及其他 $63.35B、年增 12%；YouTube 廣告 $11.21B、年增 9.2%（增速放緩）；訂閱/平台/裝置 $14.29B。","source":"TheDesk.net, Alphabet Q3 2026 earnings report; securities.io","url":"https://thedesk.net/2026/10/alphabet-google-youtube-q3-2026-earnings-report/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Google Cloud 營收 $30.71B（前年同期 $15.16B，逾一倍）；Cloud 營業利益 $11.12B（前年 $3.59B）；Google Services 營收 $96.30B、年增 11%。","source":"TheDesk.net; Verdict","url":"https://thedesk.net/2026/10/alphabet-google-youtube-q3-2026-earnings-report/","excerpt":null,"as_of":"2026-10-28","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 Google Cloud backlog $514B（季增逾 $50B，前季約 $462B），逾半預期 24 個月內轉為營收；管理層稱供給受限預期持續；2026 資本支出指引上調至 $195–205B；部分 backlog 成長與單一大客戶（Anthropic）相關。","source":"Fierce Network / TechCrunch 2026-04-29 / 彙整報導","url":"https://www.fierce-network.com/cloud/google-cloud-cranks-capex-revenue-backlog-soar","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261103","affects":["thesis.H","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"美國搜尋市佔：WebFX 報告 Google 美國市佔 12 個月內由 87.28% 降至 84.17%，Bing 達 10.48% 創高；全球 StatCounter 約 90%；Google 付費搜尋點擊 2026 Q1 年增 14%，分析師指出 Q2 放緩。","source":"WebFX Google vs Bing; Search Engine Journal","url":"https://www.webfx.com/data/google-vs-bing/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"廣告市場預測：WARC 2026 全球廣告 +11.9% 至 $1.34T，搜尋 $295.7B（+14.2%），2027 搜尋 +8.8%；Dentsu 預測 2026 +5.0%、2027 +5.5%；WARC 估 Alphabet、Amazon、Meta 2026 占不含中國全球廣告 59.7%。預測機構間差異大。","source":"WARC Media Forecast Q3 2026 (ppc.land); Dentsu","url":"https://ppc.land/warc-forecasts-social-media-ad-spend-gains-21-3-to-394-6bn-in-2026/","excerpt":null,"as_of":"2026-10-12","retrieved_at":"20261103","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 競爭章節列出『AI model developers and providers of AI products and services』為競爭對手之一，並稱業務特徵為快速變化與新型顛覆性技術。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"Our business is characterized by rapid change as well as new and disruptive technologies. We face formidable competition in every aspect of our business, including but not limited to, from: •general purpose search engines and information services;","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素自述：新技術可能使競爭者提供相似或更好的體驗，消費者可能改變取得資訊的方式，降低現有產品效用與使用量。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"As new and existing technologies continue to develop, competitors and new entrants may be able to offer experiences that are, or that are perceived to be, substantially similar to or better than ours, and the consumers may change how they obtain information online, potentially reducing the utility of our existing products and services.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"MarketBeat 報導 Alphabet 仍居美國搜尋 88% 市占，同時有資料顯示網站點擊下降 8.9%，並提及年輕用戶轉向 AI 聊天機器人的疑慮。","source":"MarketBeat: AI takes over search, is Google's dominance at risk","url":"https://www.marketbeat.com/articles/ai-takes-over-search-is-googles-dominance-at-risk/","excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Motley Fool 引 Statcounter：Google 全球搜尋市占約 90%，Bing 低於 5%。","source":"Motley Fool 2026-02-21","url":"https://www.fool.com/investing/2026/02/21/investors-no-brainer-ai-stock-competitive-risk","excerpt":"According to statcounter, it has 90% share of the global search market. Bing has less than 5% share. This is why investors have no reason to worry.","as_of":"2026-02-21","retrieved_at":"20261103","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 指出 TAC 率持續受裝置組合、夥伴組合、經由付費入口的查詢比例、各通路廣告營收相對成長率等變動影響，並提及營收從 Google Network 轉向 Google Search & other。","source":"SEC EDGAR 10-K FY2025 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"shift from Google Network properties to Google Search & other properties. Our TAC rate will continue to be affected by changes in device mix; geographic mix; partner agreement terms; partner mix; the percentage of queries channeled through paid access points; product mix; the relative revenue growth rates of advertising revenues from different channels; and revenue share terms.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K FY2025 競爭段落：廣告競爭取決於吸引用戶（其他產品『僅一鍵之遙』）、廣告主與內容提供者，並須跨多種分銷通路投放，即使廣告媒介與用戶偏好趨勢改變。","source":"SEC EDGAR 10-K FY2025 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"advertisers, primarily based on our ability to generate sales leads, and ultimately customers, and to deliver their advertisements in an efficient and effective manner across a variety of distribution channels even as trends in advertising mediums and user preferences change","as_of":"2026-02-05","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q1 2026 Alphabet 付費訂閱數增加 2,500 萬至 3.5 億，subscriptions, platforms and devices 營收 +19% 至 124 億美元；CEO 稱用戶轉訂閱方案對廣告營收有負面影響。","source":"Pulse2 / earnings call 彙整","url":"https://pulse2.com/alphabet-reports-109-9-billion-in-q1-2026-revenue-as-google-cloud-growth-accelerates-to-63/","excerpt":"The company’s total number of paid subscriptions reached 350 million, with YouTube and Google One identified as the largest contributors.","as_of":"2026-07-23","retrieved_at":"20261103","affects":["thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"Apple Safari 搜尋量下滑證詞與 AI 瀏覽器（Atlas 等）被視為對 Google 預設通路的威脅；Google 公開否認 Safari 搜尋量下降。","source":"SAN: Apple, Google $20 billion search deal at risk amid rise of AI","url":"https://san.com/?p=387836","excerpt":null,"as_of":"2025-05-08","retrieved_at":"20261103","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 2026-08-03：54 位分析師 12 個月平均目標價 $413.54，區間 $220～$515（Q3 財報前資料）；Citizens JMP 為最高 $515","source":"MarketBeat: Alphabet receives consensus recommendation of Buy from brokerages","url":"https://www.marketbeat.com/instant-alerts/alphabet-inc-nasdaqgoogl-receives-consensus-recommendation-of-buy-from-brokerages-2026-08-03/","excerpt":null,"as_of":"2026-08-03","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"各來源共識目標價落差：TipRanks 2026-07-31 平均 $390.80（40 位）；S&P Global/StockAnalysis 2026-07-10 平均 $432.48；Walnut 2026-08 平均 $426.95、中位數 $425；UBS 降至 $379、Morgan Stanley 降至 $400（2026-07-23）","source":"WebSearch 彙整 TipRanks／StockAnalysis／Walnut","url":"https://walnutinvest.com/stocks/googl/forecast","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261103","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 後 Alphabet 將 FY2026 capex guidance 上調至 $195–205B（原 $180–190B），高於 Visible Alpha 事前共識 $187.8B；分析師隨後上修 FY26 營收 2% 至 $497.9B、FY26 capex 估計 +7.5%","source":"S&P Global Market Intelligence / w.media","url":"https://w.media/ai-infrastructure-demand-pushes-alphabets-2026-capex-guidance-to-us-205-billion/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q3 營收 $127.6B、Google Cloud $30.7B（+103%）、2027 capex 將超過 $300B（單一來源）","source":"AIWeekly","url":"https://aiweekly.co/alerts/alphabet-posts-1276b-q3-with-google-cloud-up-103-to-307b-as-2027-capex-set-to","excerpt":"Alphabet Posts $127.6B Q3 With Google Cloud Up 103% to $30.7B as 2027 Capex Set to Top $300B By Alexis Dufresne · Published October 28, 2026 at 21:33 UTC","as_of":"2026-10-28","retrieved_at":"20261103","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Wiz 收購於 2026-03-11 完成（申報稱調整後約 $29.5B），併入 Google Cloud；Intersect 收購於 2026-03-10 完成（調整後約 $5.9B）。","source":"SEC EDGAR 10-Q（Q1 FY2026）；搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000048/goog-20260331.htm","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"證券集體訴訟 Stewart v. Alphabet（N.D. Cal., No. 26-cv-11290）：指控就 Gemini 3.5 Pro 時程誤導投資人，class period 2026-05-19 至 2026-07-16；7/16 股價跌 4.4%。另有 2023 年起的舊案（3:23-CV-01186）仍在進行。為原告律所主張，尚非判決。","source":"PRNewswire 律所公告（2026-07-27）","url":"https://www.yourwyominglink.com/pending-class-action-lawsuit-involving-the-purchase-and-or-acquisition-of-alphabet-inc-class-a/article_3c874234-933f-5045-b56f-54fe55943797.html","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"反壟斷：廣告科技案 2025-04 判決部分不利，DOJ 提出結構性救濟，2025-11 結案辯論，待最終判決；Google Play 州檢察長和解 2025-11 初步核准。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"The DOJ's remedy proposal includes structural remedies that could have a material adverse effect on our business. Closing arguments were held in November 2025, and we are awaiting a final judgment.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06 資本動作：$40B ATM 股權發行計畫，及 6.25% 強制可轉換特別股 A/B 系列發行；2026-08-10 發行 $25B 優先債。","source":"SEC EDGAR 8-K（2026-06-04）","url":"https://www.sec.gov/Archives/edgar/data/1652044/000119312526257724/d83560d8k.htm","excerpt":"under which the Company may offer and sell, from time to time in its sole discretion, up to $40 billion of shares of Class A Common Stock and Class C Capital Stock (together, the “Shares”), through an “at-the-market” offering program (the “ATM Offering”).","as_of":"2026-06-04","retrieved_at":"20261103","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 共16份，含重大項目者7份；搜尋未見 SEC 調查或財報重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001652044&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 16 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 7 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Wiz 收購於 2026-03-11 完成（調整後約 $29.5B）；Intersect 於 2026-03-10 完成（調整後約 $5.9B）；GFiber 重組預計2026年底完成。","source":"SEC EDGAR 10-Q（Q1 FY2026）；搜尋摘要轉述","url":"https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000048/goog-20260331.htm","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261103","affects":["valuation","moat_trend"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Stewart v. Alphabet（N.D. Cal., No. 26-cv-11290）證券詐欺集體訴訟，class period 2026-05-19～2026-07-16；為原告主張，未判決。","source":"PRNewswire 律所公告","url":"https://www.yourwyominglink.com/pending-class-action-lawsuit-involving-the-purchase-and-or-acquisition-of-alphabet-inc-class-a/article_3c874234-933f-5045-b56f-54fe55943797.html","excerpt":null,"as_of":"2026-07-27","retrieved_at":"20261103","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"DOJ／州檢察長反壟斷案（廣告科技、搜尋、Android／Play）仍在進行，廣告科技案待最終判決。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm","excerpt":"Closing arguments were held in November 2025, and we are awaiting a final judgment.","as_of":"2026-02-05","retrieved_at":"20261103","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 共16份，其中含重大項目7份；查無 4.02（財報不可信）項目於清單中，搜尋亦未見 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001652044&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-03 至 2026-11-03 共 16 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 7 份。","as_of":"2026-11-03","retrieved_at":"20261103","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"GOOGL","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":60.86,"operating_margin_pct":33.32,"fcf_margin_pct":4.19,"rd_intensity_pct":15.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.GOOGL","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true},{"name":"MSFT","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.66,"operating_margin_pct":47.1,"fcf_margin_pct":17.31,"rd_intensity_pct":10.52},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MSFT","as_of":"TTM ending 2026-09-30（4季加總）"}},{"name":"AMZN","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.01,"operating_margin_pct":12.36,"fcf_margin_pct":-0.82,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMZN","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AAPL","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":48.65,"operating_margin_pct":33.17,"fcf_margin_pct":29.28,"rd_intensity_pct":9.19},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AAPL","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"META","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":81.03,"operating_margin_pct":32.86,"fcf_margin_pct":11.86,"rd_intensity_pct":31.68},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.META","as_of":"TTM ending 2026-09-30（4季加總）"}}],"subject":"GOOGL"},"financial_history":{"ticker":"GOOGL","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":282836000000.0,"revenue_yoy_pct":null,"gross_margin_pct":55.38,"operating_margin_pct":26.46,"net_income":59972000000.0,"diluted_eps":4.56,"free_cash_flow":60010000000.0,"fcf_margin_pct":21.22,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":307394000000.0,"revenue_yoy_pct":8.68,"gross_margin_pct":56.63,"operating_margin_pct":27.42,"net_income":73795000000.0,"diluted_eps":5.8,"free_cash_flow":69495000000.0,"fcf_margin_pct":22.61,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":350018000000.0,"revenue_yoy_pct":13.87,"gross_margin_pct":58.2,"operating_margin_pct":32.11,"net_income":100118000000.0,"diluted_eps":8.04,"free_cash_flow":72764000000.0,"fcf_margin_pct":20.79,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":402836000000.0,"revenue_yoy_pct":15.09,"gross_margin_pct":59.65,"operating_margin_pct":32.03,"net_income":132170000000.0,"diluted_eps":10.81,"free_cash_flow":73266000000.0,"fcf_margin_pct":18.19,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/GOOGL/GOOGL_Q3_2026_Earnings_Call_20261028.md）

# Q3 2026 Earnings Call
**Alphabet Inc.** | Earnings Calls | 2026-10-28

**Operator** (Operator):
Welcome, everyone. Thank you for standing by for the Alphabet Third Quarter 2026 Earnings Conference Call. [Operator Instructions] I would now like to hand the conference over to your speaker today, Jim Friedland, Head of Investor Relations. Please go ahead.

**James Friedland** (Executives):
Thank you. Good afternoon, everyone, and welcome to Alphabet's Third Quarter 2026 Earnings Conference Call. With us today are Sundar Pichai, Philipp Schindler, Thomas Kurian and Anat Ashkenazi.  
Now I'll quickly cover the safe harbor. Some of the statements that we make today regarding our business, operations and financial performance may be considered forward-looking. Such statements are based on current expectations and assumptions that are subject to a number of risks and uncertainties. Actual results could differ materially. Please refer to our Forms 10-K and 10-Q, including the risk factors. We undertake no obligation to update any forward-looking statement.
During this call, we will present both GAAP and non-GAAP financial measures. A reconciliation of non-GAAP to GAAP measures is included in today's earnings press release, which is distributed and available to the public through our Investor Relations website located at abc.xyz/investor. Our comments will be on year-over-year comparisons unless we state otherwise.
And now I'll turn the call over to Sundar.

**Sundar Pichai** (Executives):
Thanks, Jim, and hello, everyone. Q3 was a strong quarter for Alphabet. Our deep full stack approach is driving momentum across the business with many opportunities ahead. Let me give you a quick snapshot of the quarter.
Alphabet revenues grew 25% year-over-year. We are now at $0.5 trillion annual run rate. That's remarkable growth. Search has strong momentum. Our AI investments are driving increased usage and overall query growth, including commercial queries. In fact, our year-over-year query growth rate is the highest it's been in the last 5 years.
Google Cloud revenues grew 103%. Our AI infrastructure and solutions are the major drivers for Cloud growth and our customers see us as the leading provider here, so there's huge demand. We are working hard to bring more capacity online to meet this long-term demand. At the same time, we are seeing strong demand for our TPU systems across a wide range of customers, and we expect that to continue as we scale. I'm excited to welcome Thomas to the call, and he'll share more about Cloud's momentum.
On our AI models, customers are using our models more than ever. Our first-party model APIs are now processing nearly 32 billion tokens per minute, 40% more than last quarter and more than 4x what we processed a year ago. And with Gemini 4 Argon and now Carbon, which we announced today, we are excited to be leading at the frontier. The Gemini app is now at 1 billion users and is the fastest-growing product in Google's history. Lastly, we have surpassed 150 million YouTube Music and Premium subscribers globally, including trials.
Today, I'll talk more about our AI progress, our global consumer platforms led by Search and YouTube, then our long-term bets.
Starting with AI, highlighted by our Gemini 4 series of frontier models. We are seeing strong demand and usage for Argon, which we launched 2 weeks ago. In fact, on our developer platforms, usage in the first week ramped up 3.5x faster than Gemini 3, even with capacity constraints. Argon is proving to do really well in areas like finance, legal, cybersecurity and science.
Developers and cloud customers are already using it for things like untangling legacy code bases, accelerating scientific research, robotics, discovering product improvements and domain-specific tasks requiring in-depth reasoning. And at Google, just in the last few weeks, teams across Chrome, Ads and Search have used Argon to write and optimize code much faster, shipping 35% more code with 30% fewer errors. Argon is just the start of the Gemini 4 series.
Today, we announced Carbon. It's our strongest frontier model with state-of-the-art cybersecurity and long horizon capabilities. It ranks #1 on the recently updated Artificial Analysis Intelligence Index at 59. Carbon outperforms Argon across almost every domain like full stack web development, multimodal understanding, complex knowledge work and scientific reasoning.
We are rolling Carbon out first to a subset of trusted cyber defenders before we expand access, and it's being tested by the U.S. government. Beyond our Gemini 4 series, yesterday, we announced Genie 4, our most advanced world model yet that simulates safe, realistic, interactive worlds with native audio in real time. This is an important building block for training robots and agents. This rapid progress underscores our incredible model momentum.
We are at the point where AI is helping us increase our training and launch velocity. I would expect the next 12 months to see continued acceleration because of RSI. We have more models coming soon, including more efficient versions to help developers optimize for speed and cost and to deploy across our billions of users.
Let's turn to Search, which is bringing the benefits of AI to more people than any other product in the world. Just like our shift to mobile over a decade ago, we are focused on building the best Search user experience, followed by monetization. We are building one seamless experience across AI Overviews, AI Mode and traditional search. And people are using our AI features more searching in entirely new ways. Their queries are longer, personalized and multimodal. Queries in AI Mode are on average 3x longer than traditional searches, and 1 in 5 AI Mode searches globally use voice, images or documents.
We have now crossed over 50 billion visual searches per month. One area I'm excited about is helping people get things done, be it booking reservations, filling in forms, scheduling appointments or making purchases. As AI becomes more personal and starts taking action for people and businesses, trust and security matter more than ever. People already put their trust in Google to get things done in their daily lives, and our leadership here remains an important differentiator. We focus first on getting these agentic experiences right with the Gemini agent for enterprise because the bar for security, safety and governance is extremely high.
As the next step, we are bringing these features to Search and also, of course, to our 1 billion users on the Gemini app. People are already using the Gemini app to do more than ask questions. They're using it to do things, including complex multistep agentic queries. Our Gemini 4 series has been a really big step forward here and has already been handling these complex tasks really well. Agents will operate as a unifying layer across our products, so you will see us extend these agentic experiences beyond Search in the Gemini app to Chrome, Android and our Workspace products as well.
On to YouTube, which continues to lead in the living room as the #1 streaming platform in the U.S. in terms of watch time. It's also seeing good subscriber growth as I mentioned. At Made on YouTube last month, we announced more than 30 products and features for creators and viewers. One great example is custom feeds where you can simply pick a topic you love and get a tailored video home feed based on that topic. Philipp will say more on YouTube.
On to our long-term bets. Waymo is on a great trajectory. We have now driven more than 300 million fully autonomous miles. Waymo now operates in 15 major U.S. cities and just recently opened up service to the public in San Antonio, San Diego and Tampa with planned expansions into Canada, Germany, Singapore and Spain.
We're also seeing strong progress across our other long-term initiatives. Isomorphic is using Argon to support drug design research. We demonstrated magic state cultivation for the first time in quantum computing and launched our TPUs into space with Project Suncatcher.
So it's been a busy quarter, and there's much more to come. I want to thank our employees for their work this quarter, and over to you, Philipp.

**Philipp Schindler** (Executives):
Thanks, Sundar, and hello, everyone. I'll highlight our momentum across Search, YouTube and partnerships. We continue to accelerate the deployment of Gemini models across our entire ads infrastructure to boost performance in the 3 areas I've highlighted before: ad quality, advertiser tools and AI user experiences.
First, ads quality. The integration of Gemini models into our ads infrastructure is improving how we decode user intent and drive ads relevance. For example, in Q3, we made the biggest update to product listing ads in a decade, adding new AI capabilities to help users make more confident purchase decisions. Already, we've seen satisfaction increase by 19% and dissatisfaction dropped more than half. We're also seeing AI models enable better prediction of clicks and conversions, stronger overall performance and deeper personalization of ads. For instance, through several innovations and personalization modeling, we delivered 18% incremental advertiser value and an 8% increase in user sentiment on Discover ads in 2026. Overall, AI is accelerating our ads development and drives the majority of our product launches.
Second, advertiser tools. We're ensuring every advertiser, from global brands to small businesses, can seamlessly participate in our AI surfaces. AI Max and Performance Max continued to see strong adoption. To give marketers even more control, we're now introducing a way to test different budgets and ROI targets across multiple search campaigns in a single AI Max A/B test. To drive better performance, we integrated our AI creative tools directly into AI Max. In Q3 alone, Gemini models helped advertisers generate over 1.5 billion campaign assets, up over 7x year-over-year. For example, by using AI Max to capture long-form and multilingual queries, Telstra saw a 52% increase in conversions and a 36% reduction in cost per order, showing up in key moments however the customers search.
Third, AI user experiences. Sundar mentioned the distinct behavioral changes we're seeing as users ask entirely new categories of questions. We think of search holistically, a unified product spanning traditional results and AI-powered search. On AI Mode, many of these queries are upper-funnel queries, allowing us to capture new high-value commercial intent. In addition, the majority of AI Mode queries are incremental, creating more monetization opportunities over time.
Additionally, our user research shows that people are comfortable with ads on these surfaces and find them highly relevant. Click-through rates are already similar between sponsored and organic product list items within AI Mode.
Based on these collective results, we're now scaling high-quality ads within AI Overviews and AI Mode to more users and queries. This includes taking our monetization footprint global for the first time. Today, we're announcing the expansion of ads in AI Mode into international markets alongside multiturn ads and AI Mode in the U.S.
As always, our approach is deliberate, prioritizing the user experience and engagement first and then scaling the formats that drive proven ROI for advertisers. That discipline is what gives us a strong, durable foundation for the future.
As Sundar mentioned, we're in the early stages of agentic experiences across our surfaces and excited about the commercial opportunities ahead. The Universal Commerce Protocol, UCP, is being rapidly adopted by retailers. Today, UCP enables direct checkout for hundreds of thousands of brands across Google, including Chewy, Nike, Tapestry and many more. We're combining this with the Agent Payments Protocol as we build for the future of commerce. Our focus spans 2 fronts: unlocking agentic capabilities that act on behalf of the consumer, and designing practical tools that give shoppers confidence and control.
We launched Universal Cart this quarter to support that second track, mirroring how people actually shop today across Google. This allows retailers to maintain their relationships with customers while helping to capture sales and avoid abandoned carts.
Moving to YouTube. We view YouTube as a flywheel of creators, viewers and advertisers. First, creators. Every day, more than 20 million videos are being uploaded. We are making creation easier with new generative AI tools in YouTube Studio, plus a conversational editing assistant in Shorts and YouTube Create.
Looking at viewership. At Made on YouTube, we introduced short series where creators can structure their shorts into seasons and episodes. Sequential playback makes it seamless for viewers to discover new shorts and keep watching.
The third part is monetization starting with ads. Our focus remains on delivering value across the entire funnel. In Q3, living room accounted for over 1/3 of total YouTube Ads revenues. Small and medium advertisers continue to adopt Demand Gen, driving direct response. On YouTube, Wayfair's Demand Gen campaigns drove a 2.3x higher return on ad spend compared with traditional video reach campaigns.
Our YouTube Creator Partnerships program connects brands with over 3 million creators to drive highly effective campaigns. Brands like Lexus continue to partner with creators like Colin and Samir, driving 11% lift in brand consideration.
More than 1.3 million channels are enrolled in YouTube Shopping globally. Building on this momentum, we recently announced that Amazon is joining YouTube Shopping. U.S. creators can now tag Amazon products directly in their videos, shorts and live streams, driving direct conversions.
Importantly, our subscription ecosystem continues to complement our advertising business. Subscriptions continue to grow faster than ads led by YouTube Music Premium. YouTube Premium has more than 150 million subscribers. With Premium and Premium Lite, viewers have choice. As more people opt into premium experiences, it's a win for viewers, creators and our business. Subscriptions help fund the creator ecosystem and drive the platform forward.
Finally, strategic partnerships. Businesses are choosing Google because we bring together cloud, AI, ads and consumer platforms to accelerate their transformation. We expanded our partnership with American Express to support the ongoing modernization of their contact centers and collaborate on agentic commerce across Search and Wallet. And Unity signed an expanded multiyear cloud deal to use our full AI stack to power the next-generation game engine.
Our commercial priorities are clear: expanding advertiser ROI, systematically advancing our AI monetization efficiency and scaling our ecosystem partnerships to support the next era of discovery. In closing, I want to thank Googlers everywhere for their incredible execution and our customers and partners for their continued trust.
Thomas, over to you.

**Thomas Kurian** (Executives):
Our strong momentum is driven by our integrated AI portfolio of chips, models, data, security and agent platforms, all designed to work together. We have strong diversification across our product lines, industries and customers. Google Cloud now has 18 product lines with more than $1 billion each in annual revenue. And our growth this quarter was driven by strong growth in Google Cloud Platform with strength in both AI and core GCP. TPU system sales were also a meaningful contributor.
Over the past 12 months, more than 2,600 customers have used at least 100 billion tokens and nearly 75 at least 10 trillion tokens on Gemini Enterprise. Nearly 90% of the Fortune 100 use Gemini Enterprise, and customers who use Gemini Enterprise in Q3 2025 more than quadrupled their spend with us year-over-year. One of the important ways in which customers are using Gemini is for knowledge work. Across all our AI services, we have sold more than 100 million seats for knowledge work. Gemini Enterprise now includes the Gemini agent that is deeply integrated across our entire cloud portfolio. It can research and answer questions, write and run code and automate process flows with one agent, one API and a single prompt window.
It gives companies strong security and cost controls and the widest choice of frontier models. Customers include BNP Paribas, who is deploying Gemini Enterprise to more than 65,000 employees to streamline workflows while maintaining strict enterprise-grade security and data governance; Tata Steel who deployed more than 300 specialized AI agents in just 9 months to enhance manufacturing safety, optimize supply chains and cut service times for customers by 50%; Ulta Beauty, who built the Ulta AI shopping assistant, resulting in a 3x higher conversion rate than traditional browsing on their site.
Gemini is also driving acceleration for our database, analytics and cybersecurity products. Gemini can now help users find, analyze and visualize information from structured and unstructured data. Gemini uses our knowledge catalog to find the right sources and definitions of information, improving accuracy, lowering token cost and making responses more reliable. Gemini uses our Lakehouse to access information from multiple systems with 0 copy.
To respond to agentic analysis, BigQuery improved query speed over 40% year-over-year while reducing query processing cost by over 50% year-over-year. Customers include Deutsche Telekom, which uses BigQuery, Cloud Storage and Knowledge Catalog to build a unified data lakehouse across 40-plus legacy on-premise systems. Etsy, which migrated 3 petabytes of data to unified lakehouse, by using BigQuery and Iceberg, they now perform critical data joins up to 60% faster.
The growing risk of cybersecurity threats is also driving strong demand for our AI-powered security platform. Our Gemini Flash cyber models are frontier models that automate vulnerability discovery across 20 programming languages and patch 2.6x more reliably than other models. And there's even better performance to come as we roll out Argon and Carbon.
Our security platform integrates threat intelligence, cyber response prioritization, automated scanning, code remediation and monitoring. Gemini and Google Threat Intelligence autonomously analyzes millions of external events every day with 98% accuracy. And more than 95% of Wiz customers are adopting AI-powered features, and growth continues.
These security tools protect critical infrastructure, including financial institutions like Banorte and Jack Henry and telecommunication providers such as AT&T. All of this is powered by our leading AI infrastructure, spanning our TPU systems, Axion CPUs, the latest NVIDIA GPUs and our Agent Compute Engine, which is specifically designed for AI agents.
TPU systems are specialized systems built for AI, combining hardware, compute storage and networking with systems components and optimized software for training and inference. TPU 8t and 8i offer up to 2.7x better training performance and 80% better inference price performance, respectively, versus our previous generation of TPUs. To make it easy for developers to port workloads to TPUs, we recently worked closely with Meta to deliver TorchTPU, which allows users to train, serve and deploy PyTorch models on TPUs, using the tools they're already familiar with and rely on.
Nearly 100 customers use TPUs today, and we're seeing strong and growing demand from many others. In addition to our work with Anthropic, both directly and via Broadcom and public reference customers like Apple, who are scaling pretraining of their foundation models on the latest generation of TPUs, we're also working with new frontier model companies, including Mirendil and Physical Intelligence; capital markets firms, including Citadel Securities and Jump Trading; universities like Caltech; and public sector service providers, including Cassava and Cirrascale. Given continued strong and accelerating demand, we've recently entered into partnerships to deliver TPU systems with both Crux AI and Oracle, with more in the works.
Over to you, Anat.

**Anat Ashkenazi** (Executives):
Thank you, Thomas. My comments will focus on year-over-year comparisons for the third quarter, unless I state otherwise. I will start with the results at the Alphabet level and will then cover our segment results. I'll end with some commentary on our outlook for the fourth quarter and full year 2026.
We had a strong third quarter delivering our 13th consecutive quarter of double-digit revenue growth. Consolidated revenues were $127.6 billion, up 25% in both reported and constant currency. Total cost of revenue was $51.4 billion, up 24%. TAC was $16.4 billion, up 10%. Other cost of revenues was $35.1 billion, up 32%, driven by hardware costs primarily related to the sales of TPU systems, increase in depreciation, content acquisition costs and technical infrastructure operations costs.
Total operating expenses were up 20% to $35.6 billion. R&D expenses increased by 36%, driven by compensation, primarily for investment in AI talent as well as depreciation. Sales and marketing expenses were up 22% due to investments in Gemini and compensation. And G&A expenses decreased 17%, primarily due to lapping of higher legal expenses that occurred in Q3 last year, partially offset by current year legal charges.
Operating income increased 30% to $40.6 billion, and operating margin was 31.8%. Other income and expenses was negative $8.2 billion due primarily to unrealized loss from our investment in SpaceX from a decline in its stock price in the third quarter. Net income and earnings per share decreased due to the decline in OI&E. 
We generated strong operating cash flow of $42.3 billion in the third quarter and $179.6 billion for the trailing 12 months. Operating cash flow was negatively impacted by the buildup of inventory for TPU system sales as well as a $5.2 billion cash payment for a 2018 EC fine following the conclusion of the appeal process.
CapEx was $51.4 billion in the third quarter with the vast majority of the spend in technical infrastructure to support our investments in AI. Approximately 65% of our investments in technical infrastructure in Q3 was related to servers and networking equipment, which generally have useful lives of 6 years. The remaining 35% was for data centers, which have useful lives of 7 to 40 years.
We had negative free cash flow of $9.1 billion in the third quarter, driven by our investments in CapEx. Free cash flow in the third quarter was also affected by the aforementioned inventory build to support TPU system sales and payment of the EC fine. Free cash flow was $19.7 billion for the trailing 12 months. We ended the quarter with $265.1 billion in cash and marketable securities, which includes $90.4 billion of marketable equity securities. Long-term debt was $125.1 billion.
We have also entered into multiyear agreements to secure capacity for technical infrastructure and inventory as well as leases and energy. At the end of the third quarter, we had future purchase commitments of $924 billion and pre-commencement leases and other obligations of $152 billion. These dollar amounts reflect the maximum contractual obligations. However, a number of these agreements have variable pricing and volume flexibility, which could result in lower spend.
And as mentioned in our press release, our Board of Directors declared a quarterly cash dividend on our common stock of $0.22 per share, which is payable in December.
Turning to segment results. Google Services revenues increased 11% to $96.3 billion, reflecting strong growth in Search and subscriptions. Total advertising revenues were up 11% with growth across all major verticals. As we stated in our outlook last quarter, FX was a slight headwind on year-over-year growth rates and had a more significant impact on sequential basis.
Google Search and other advertising revenues increased by 12% to $63.3 billion, with retail driving the largest contribution followed by finance. YouTube advertising revenues increased 9% to $11.2 billion, with brand driving the largest contribution and notable strength in living room. Network advertising revenues of $7.5 billion were up 1%. Subscription, platforms and devices revenues increased 11% this quarter to $14.3 billion, driven by strong growth in YouTube subscriptions, particularly in YouTube Music and Premium and strong demand for AI plans in Google One. Google Services operating income increased 17% to $39.2 billion, and operating margin was 40.7%.
The Google Cloud segment delivered record growth in the third quarter. Cloud revenues were up 103% to $30.7 billion, driven by strong growth in GCP with strength in AI, including both AI infrastructure and AI solutions and core GCP.
TPU system sales were also a meaningful contributor. GCP accounted for the vast majority of the revenue generated in Q3. The cloud revenue growth rate, excluding the impact of TPU systems, was again incredibly strong. Cloud operating income was $11.1 billion, more than tripling year-over-year. Operating margin increased from 23.7% in the third quarter last year to 36.2%. The third-party bridging capacity, which we discussed on our prior call, came online only at the very end of Q3 and therefore, had limited negative impact to our margin in the quarter.
Google Cloud's backlog was $561 billion in the third quarter, with the majority of the backlog related to typical GCP contracts. We expect to recognize just over 55% of the total backlog as revenues over the next 24 months. In Other Bets, revenues were $372 million, and the operating loss was $2 billion as we continue to expand Waymo's business and invest in key Other Bets. In Alphabet-level activities, the operating loss was $7.7 billion, driven by shared AI R&D expenses.
I'll now turn to our outlook for the remainder of 2026. First, in terms of revenues, at current spot rates, we would expect a slightly larger FX headwind to our consolidated revenues in Q4 relative to the prior quarter. This impact will be seen primarily in Search and YouTube Ads. In Google Services, we will continue to lap the search performance acceleration that began in the third quarter last year, which will pressure revenue growth in Q4.
In Google Cloud, we expect TPU system sales to continue to scale in Q4, followed by a meaningful revenue ramp in 2027. With respect to Cloud margins, given the supply constrained environment, we started utilizing third-party compute capacity at the end of Q3 and will ramp usage in Q4. We expect margin headwinds in the near term as we utilize this capacity.
Moving to investments. Our full year 2026 CapEx guidance range of $195 billion to $205 billion remain unchanged. We continue to expect our CapEx to increase significantly in 2027, and we'll provide further details on our Q4 call. In terms of expenses, the significant increase in our investment in technical infrastructure will continue to weigh on the P&L in the form of higher depreciation expenses and related data centers operation costs such as energy.
Before we move to Q&A, let me say a few words on how we think about return on invested capital and free cash flow. We're in a unique position to be able to monetize our AI investments across many products that reach billions of users and enterprises. Our AI investments in Search are driving our highest query growth in half a decade. Google Cloud has generated tens of billions of dollars in AI revenues year-to-date, and Google One is our fastest-growing subscription products, driven by demand for AI plans.
Throughout this investment cycle, we expect to generate an attractive ROIC that remains meaningfully above our cost of capital and anticipate generating strong cash flow from operations. Our sizable investments in technical infrastructure and inventory build of TPU systems as we scale that business will put pressure on free cash flows.
Q3 was a strong quarter, highlighted by our innovation and disciplined execution across all areas of the business, including the launch of Gemini 4. I want to take this opportunity to thank our employees for their contributions to our performance.
We will now open the call for Q&A.

**Operator** (Operator):
[Operator Instructions] And our first question comes from Doug Anmuth with JPMorgan.

**Douglas Anmuth** (Analysts):
One for Sundar and one for Philipp. Sundar, on a recent podcast, you said that 2027 could be the golden age of productivity for Google because of the new class of models and how they'll integrate with your other products. I was hoping you could elaborate on that and just share more, how you think about the opportunity set there ahead.
And then, Philipp, just on query growth, the fastest in 5 years but obviously, some deceleration in Search growth. Can you just help us understand the disconnect there? Is it simply that you haven't been showing as many ads basically in AI Overviews and AI Mode, and that's now becoming a bigger percentage of the overall queries?

**Sundar Pichai** (Executives):
Thanks, Doug. We definitely started seeing a step change, I would say, with 3.8 Flash internally as our models got better at long-horizon tasks, agentic coding, et cetera. But I'm definitely seeing a huge point of inflection once we've started deploying Argon internally. It is one of the most meaningful internal productivity levers we have seen on software engineering, directly tracking high-quality code that's getting checked in, the rate at which it's getting checked in, reducing the number of rollbacks.
But more importantly, people are tackling massive problems as well as we are beginning to see innovation on the product and the consumer experience side from deploying those models. But all this happened only about 4 weeks ago. We are now deploying Carbon internally, and Carbon is a meaningful step-up from Argon, so as we roll it out and make it all widely available to Googlers with more compute, I expect to -- that's what I was referring to, and I'm even more excited since I said that in the podcast and what I would view as a golden year ahead in terms of us being able to be more productive, and so excited for the innovation ahead. Philipp?

**Philipp Schindler** (Executives):
Yes, Doug, on the second part of your question, look, in Q3, Search grew 12% year-over-year to $63 billion. And when you look at the change in growth rate from Q2 to Q3, there were a few drivers here. So first, there was FX. It was the single largest driver of Search deceleration relative to Q2. Second, there were vertical-specific dynamics. In retail, some of our APAC advertisers were impacted by the EU eliminating its de minimis exemption. In media and entertainment, spend normalized after an unseasonably strong Q2, driven by the FIFA World Cup, which had more matches and therefore, more advertising budgets allocated in June than actually in July.
It's also -- to the next part of your question, it's worth noting that the strong growth in AI Mode queries had an impact because of the lower monetization we were seeing in AI Mode. To be clear, we feel very good about our trajectory here. Our ad experiments have shown promising results, and we're now scaling ads within both AI Overviews and AI Mode to more users and more queries, including, as I mentioned, international markets and multiturn ads in the U.S.

**Operator** (Operator):
Our next question comes from the line of Brian Nowak with Morgan Stanley.

**Brian Nowak** (Analysts):
I have 2. Maybe let me start with agentic. You rolled out Spark to some of the users throughout the year. I know, Sundar, you've talked a lot about shipping more agentic products to the broader base of users. Can you just help us understand a little bit some of the key hurdles you have to overcome technologically to ship out agentic products to the full base of users? Is it model efficiency? Is it capacity? Is it the technology isn't ready? Like what do we have to do technologically to do that?
And then the second one just on to Doug's question on Search. Anat, can you help us better understand the search performance comparison factor that you talked about impacting Search? And how do we think about that as we kind of go into 4Q, 1Q just kind of looking at the compares?

**Sundar Pichai** (Executives):
Thanks, Brian. First of all, on agents, what an exciting and dynamic area. I think when I look at our new models and we see the capabilities of the kind of complex tasks they can take in an automated way and execute with very, very high quality, it's clear that the agentic capabilities we've all envisioned are going to be real. And so I couldn't be more excited to bring the next-generation agentic experiences to our users.
To your question, I would say a few things. I think the Gemini 4 model series has been important. We are working on distilled versions of our Carbon models so that we can deploy it across 1 billion user scale efficiently, both from a compute, from a latency standpoint and from a quality standpoint. So that's been an important area of investment, definitely making sure you need more than a capable model at scale. You need a robust harness. You need a highly secure run time, and this is where GCP comes in, being able to give each and every one of our users a secure run time at 24/7 availability in the cloud, the right ecosystem of skills and connectors. So all of that is the foundation.
We have been hard at work, and we decided to roll it out to enterprise first, which we announced with our Gemini agent for enterprise, essentially because they have the highest bar for security, governance and controls. And it's been well received, and we are in the process of expanding that.
Later this year, we will bring that same experience to consumers, obviously, starting with the 1 billion users in our Gemini app. We already see people in the app moving beyond chat to what are task and agent-like experiences. And so the trust users have in our products, the fact that all their context is right there, I think, sets us up well, but we are really focused as a company on delivering that unified experience across our products, and you should expect to see a lot of progress later this year.

**Anat Ashkenazi** (Executives):
Thanks. And on the second question with regards to my comments, I believe you're referring to the outlook with regards to Search. A couple of dynamics that I've mentioned. One is on sequential related to impact of FX headwinds, which we saw this quarter as well versus the previous quarter. So where we are today with current spot rates, we expect that this will be somewhat of a headwind to Q4 results.
And then when we look at the year-over-year comparison, this quarter, we started lapping the acceleration we saw in Search growth in 2025, the back end of 2025. We lapped about 3 points of growth versus Q3, and then we expect to see that continue in Q4, a couple of points of lapping that growth acceleration that we saw at the end of 2025.

**Operator** (Operator):
Our next question comes from the line of Eric Sheridan with Goldman Sachs.

**Eric Sheridan** (Analysts):
Based on some of the comments you've made recently, Sundar, on compute constraints, can you refresh for us your key priorities for the application of compute as it becomes available across the organization? 
And the second part, maybe either for you or Thomas, would be within Google Cloud specifically, how does your view continue to evolve with respect to the application of compute to cloud customer needs relative to external TPU?

**Sundar Pichai** (Executives):
Thanks, Eric. I'll start, and then Thomas will answer the second half. Definitely, compute allocation is an area where we are spending a lot of time on because of the forward planning that's needed. I would start with saying we feel fortunate to have an extraordinary set of opportunities ahead of us. We are operating a scale consumer business that reaches billions of people, a hyperscale cloud business with a lot of momentum and of course, a range of other highly important areas across Google and Alphabet.
We always take a long-range planning. And so each of our business areas submit long-range plans with a very disciplined ROIC framework. And so I would broadly think of all of this as a long-range planning process, not a short-term allocation exercise.
Obviously, our AI models underlie everything we do from Search and YouTube to Cloud to Waymo and so on. So it's the foundation and we view it as a highly leveraged approach, the full stack approach drives a lot of efficiency as well as gives us a lot of optionality across a wide variety of opportunities. So obviously, that is the foundation, and we plan for that for the long term, too.
And about that, as I said, we really look at our businesses and really take a disciplined long-range planning approach. To us, obviously, we are seeing very, very robust demand signals across a wide variety of areas. And so we view it as an extraordinary set of opportunities, and we are investing for that moment.
Thomas?

**Thomas Kurian** (Executives):
Eric, on the demand in Cloud, we are always managing our portfolio to ensure we have a breadth of customers, and we have different types of customers from digital natives, AI labs, traditional enterprises, financial and capital markets customers. So it's a broad set of customers. Many of them have either started with using TPU systems, for example, in our cloud. We have over 100 significant TPU customers who start in our cloud. They learn to use TPUs. And remember, a TPU system is a combination of hardware, system software, compilers, the whole thing assembled as a system, including optical networking and other things.
We've taken a very deliberate approach on how we're bringing TPUs to customers. The first one is to build the right silicon. So we have 8t for training, 8i for inference. They both offer substantial price performance and performance improvements relative to prior generations.
Second, we've optimized the software. The optimization in the software is not just to make the systems run better and to give you great performance but also to see -- make portability seamless. Recently, we introduced, for example, PyTorch, which opens up a much larger market for us by optimizing PyTorch on the TPU.
Third, we are broadening distribution. So in the past, you could use TPUs in our cloud. Now we make for customers who want TPU systems in their data centers, we're making TPU systems available in their data centers. We're also broadening availability to other providers. For example, we announced a partnership with Oracle and we've launched along with Blackstone an agreement for Crux AI, a joint venture to offer customers TPU systems. We are seeing extraordinary demand and strong growth from both AI labs, capital markets, financial service institutions and enterprises. And if you imagine these 100-plus customers growing to many more and also scaling their use into TPU systems, we see strong demand over the future.

**Operator** (Operator):
Our next question comes from Ross Sandler with Barclays.

**Ross Sandler** (Analysts):
I wanted to stick with the TPU resale business topic that you just mentioned. So Anat, last quarter, you kind of said that the revenue will be recognized on system sales, I believe. So if a gigawatt of TPU full system costs around $35 billion for the compute and all the kind of components around it, what percent of that are we actually recognizing as revenue? And what kind of flow-through does that have in terms of margin profile relative to where the Google Cloud segment currently sits?
And then I guess the second part of the question would be, as you help companies like Anthropic bring on more of their own kind of first-party infrastructure, what does that mean for the CapEx intensity of Alphabet as you start to kind of hand off some of the future CapEx to the AI labs and may not require as much CapEx intensity on your own, in your own data centers? Thoughts on that would be great.

**Anat Ashkenazi** (Executives):
Yes. Let me combine these 2 questions. First, obviously, we don't provide specific financials at the product level, but let me walk through how to think about the financials associated with the TPU system sales. And obviously, just as a reminder, and Thomas can elaborate on that as well, a TPU system is not just a chip, but it's a specialized system that combines multiple things, including hardware, compute, storage, networking. So we are selling much more than just a chip. Software, training, inference, there is a significant added value that's being provided to the customer that's purchasing a TPU system.
And the way this works, and this is linked to your second portion of the question, when we sign an agreement with the customer to sell TPU systems, once we sign that agreement, you'll first see that showing up in our backlog and then we start building inventory. So think about this from a CapEx versus cash perspective. We build the inventory ahead of getting the revenue stream in. So I think I've alluded to this on the previous call. You see inventory balances go up, where previously inventory balances primarily were some of our hardware products. Now those TPU systems that are not yet sold will be showing up. So you see cash going out, and we're building up the inventory base.
And then as we start delivering and billing customers for these TPU systems, then you see cash coming in. So it's not the traditional kind of CapEx as you're thinking about this, and I think that's the essence of your question, but rather a different cycle of cash flow generation.
Now given that we are in the process of building up and ramping up that business, you're seeing that cash needs in our cash flow statements and you see those inventory built. To date, we've had some system sales recorded as revenue, but expect more of it to come in through 2027.

**Operator** (Operator):
Our next question comes from the line of Justin Post with Bank of America.

**Justin Post** (Analysts):
I have some questions on the agentic transition. You did launch the universal shopping cart. Clearly, people are liking and using agentic use cases. As more in that -- more of that happens, how do you plan to manage the search transition to agentic use? Do you think that could be a headwind? And second, do you think agentic could actually drive more monetization for your traffic over the long term?
And then I'll go again at TPU margins. We're wondering, do you think this is a really good business for you? And maybe why? If you can't give us the margins, why you think this is a good way to use all this capacity?

**Philipp Schindler** (Executives):
Justin, we're in the early days of agentic, but maybe directly to the second part of your question, we view agentic experiences as clearly additive. Our focus is building trusted and secure superscale experiences that users love, anchored, frankly, on agentic commerce foundational blocks like you mentioned at Universal Commerce, the cart, the agents, payments, protocols and so on.
When users shop, and that's important, there's a part of the journey they don't like, the grunt work, which is, frankly, fantastic to automate with AI. But we also want to enhance, not just automate away the discovery experience that people frankly love in so many cases. Users like choice, and they want to consider things way beyond price, like brand loyalty, customer service and so on.
So we're really architecting these agentic workflows in a way that we can intentionally design the time and the space for users to explore those choices. So a simple example, an agent could respond, "Here is the insurance product we found, and here is another strong option, one of which is a higher premium, maybe a little deductible. And they are currently offering a very special discount."
So given that there's almost never only one perfect option for a decision, we're actually confident that we can actually provide really interesting, compelling advertising models for agentic use cases. And obviously, you can imagine going beyond us with subscriptions and other payment methods. But I'm really actually excited about the advertising opportunities in an agentic world.

**Sundar Pichai** (Executives):
Overall, I would add and say, look, I would view it as an expansion opportunity, right? Any time, just like a few years ago, being able to incorporate AI chat use cases in Search allow people to ask more and do more in Search, which is what is playing out in our usage. I think agents would again be an opportunity to expand the types of problems we solve for our users.
I think people always underestimate all the components you need to deliver these agentic -- these complex experiences for users. And Search on the surface looks simple, but there's extraordinary deep levels of investment and things we have built over time, like Knowledge Graph being an example and so our understanding of the world, et cetera. 
So I think I'm excited about agents, and I would view it as a new frontier, which brings in a new set of use cases to Search. And so we are excited to work through that.

**Thomas Kurian** (Executives):
On TPU systems and margins, we don't break out margins for individual products or infrastructure components. However, we see several benefits from designing and manufacturing TPU systems. So first of all, to remind you, the TPU system is not just a chip, but it's a complete system. Given the price performance benefits of TPU systems relative to competitors, growing demand for accelerated compute and the scarcity of accelerated compute, we're very focused on continuing to improve margins as we scale the business.
Two additional points. First of all, when Anat mentioned that we procure components to build inventory, we only do that after we have signed contracts. So all of the inventory that -- for TPU systems are associated with committed contracts. Additionally, by putting TPU systems in third-party facilities and in customer data centers, it allows us, one, to broaden our addressable market. Some -- for some industries, they have data in their premise that they cannot move to a cloud, and it allows us to bring accelerated compute to where the data sits. Additionally, it also offsets the need for us to have to prebuild facilities to host these TPU systems.

**Operator** (Operator):
Our next question comes from the line of Mark Shmulik with AllianceBernstein.

**Mark Shmulik** (Analysts):
I'm going to be on the same couple of topics. But Philipp, just on agentic, as we've kind of just taken a look at some of the early more agentic-style use cases on Gemini, AI Mode and kind of observing some of the 3P integrations with Google properties, anything that surprised you or changed your view? I know we've talked a lot about commerce, but perhaps on like consumer productivity as well.
And then either Thomas or Anat, just on kind of Cloud growth, is there anything you could share just around the rate of growth of Google Cloud excluding the TPU system sales? And just how much of that has been kind of constrained by capacity? And as some of that 3P capacity comes online in Q4, is it fair to kind of assume an acceleration of that Google Cloud business?

**Sundar Pichai** (Executives):
Look, maybe I'll take the first part on what we are observing on these early agentic-style use cases. We are definitely seeing it. Just recently in the Gemini app, we have added a task tab and where people are actually typing in agentic queries and so we can observe that.
Look, in all of this, users really want -- they want to be delighted. So they effectively are looking for -- they have a high bar. What encourages repeat use is your ability to more handle these longer tasks and actually deliver a satisfactory outcome at the end. Just like having seen this in other areas, including coding, et cetera, when you're doing it at 70%, it looks like it doesn't work until you cross a certain threshold, and it really takes off. And so we are closely learning from all of it, identifying gaps, laying all the foundations I talked about earlier. And I'm confident it's an area where you will see a lot of progress across our surfaces as we go through later this year and '27.
The one thing -- as we transition to TPUs, one other comment I would make on the TPU systems is, look, in the semiconductor industry, economies of scale matter. So I would look at our ability to do TPUs both for deploying in our data centers and TPU systems in others' data centers as an ability to scale up the product, which directly translates into better economics.

**Thomas Kurian** (Executives):
To address the question on the rate of growth of Cloud, Google Cloud segment delivered record growth in the third quarter with Cloud revenues up 103% to $30.7 billion. The strongest growth contributor was Google Cloud Platform with strength in both AI and core GCP. So GCP accounted for the vast majority of revenue generated in Q3, and Cloud revenue growth, excluding the impact of TPU system sales was again very, very strong. Demand was also strong across our product lines.
So we see 3 things going on. One, as people use Gemini, we see revenue growth from Gemini itself, but we also see that as people use Gemini, it drives growth in other parts of our portfolio. For instance, as they build agents, they use compute to perform a task, and so they buy compute. They use storage to store memories of the agent, database to serve up what's called context for the agent to reason on. And obviously, given all the cybersecurity threats, we are seeing strong growth in our cybersecurity portfolio.
So we are confident about our growth and the diversity in our growth. We're also seeing new customers buy into GCP and accelerating growth in new customer adoption. So we also see that as a growth vector for us. And we are always, at any point in time, we could obviously serve a lot more demand with capacity, but we are managing all of these parameters and growth carefully.

**Operator** (Operator):
And our last question comes from Michael Nathanson with MoffettNathanson.

**Michael Nathanson** (Analysts):
I have 2 for Sundar. In an earlier answer to Eric's question about TPU and Cloud, we heard a willingness to work with some of your competitors or companies that we may view as competitors in models and cloud. So I wonder how you think about the philosophy here about work with people that maybe are competing with you and why this strategy is an opportunity, not a risk longer term that makes sense.
And then secondly, on agentic consumer behavior. One of the debates is around safety and trust. Can you share with us what you've learned so far about safety and trust? Are those variables that matter to consumers? And how do you think -- if those variables matter, what are you doing to protect consumer trust and privacy as you build out agentic consumer tools?

**Sundar Pichai** (Executives):
Thanks, Michael. Great questions. On the first one, look, we've long viewed what we build as categories of things which we build as products and then there are categories of things which we build as platforms, right? And you need to have a clear view on which is which. And when you're building things as platforms, you really work hard to make the platform great and make sure it works for everyone.
We have a long history of operating many platforms, be it a browser, be it operating system, be it extraordinarily successful cloud platform. And in all of that, we've worked hard to provide it to all players and be a great customer. You've seen us work on our models with other companies, including Apple with whom we compete in many, many areas.
Similarly, we view our TPU systems as an important platform we are building. We want to be world-class in how we build it. That means you're putting it against market forces, testing it and competing for people who would have the most demanding workloads on top of it. And I think that's what makes sure those teams are continuing to be at the frontier.
So that's how we think about it. And over time, I think that always ends up in expanding opportunities, and we've been able to do well taking that approach over a very long period of time.
Second, on agentic behavior. I mean, to the earlier question, and I think I should have emphasized, people really -- when people are approaching these agentic experiences, we clearly see people are concerned about safety and trust. I mean it is a very, very high factor in how they want to use these things and over decades, the trust we have built by delivering these experiences in a safe way across many consumer products with scale in billions of users as well as putting in end to end as we are building our models and agents, deploying them both with extensive testing, the kind of real-time monitoring we do as we deploy these at scale, I think all of that will end up being a huge differentiator. And we already hear about it from our users, and I think they would vote with their feet as this frontier goes through.

**Operator** (Operator):
And that concludes our question-and-answer session for today. I'd like to turn the conference back over to Jim Friedland for any further remarks.

**James Friedland** (Executives):
Thanks, everyone, for joining us today. We look forward to speaking with you again on our fourth quarter 2026 call. Thank you, and have a good evening.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GOOGL_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜CFO｜guidance：CFO 將 2026 全年 CapEx 指引上調（區間起點）（原話："full year 2026 CapEx guidance range to $195 billion to"）
- 2026-07-22｜CFO｜guidance：CFO 說明上調前的舊區間（原話："previous estimate of $180 billion to $190 billion"）
- 2026-07-22｜CFO｜guidance：CFO 表示 2027 CapEx 將顯著增加，細節稍後提供（原話："expect our CapEx to increase significantly in 2027"）
- 2026-07-22｜CFO｜guidance：CFO 預期 Q3 有輕微匯率逆風（Q2 為 1 個百分點順風）（原話："we would expect a slight FX headwind to our consolidated"）
- 2026-07-22｜CFO｜guidance：CFO 指出 Q3 起開始對比去年 Search 加速的高基期（原話："we will begin lapping an acceleration in Search performance"）
- 2026-07-22｜CFO｜guidance：CFO 表示 TPU 系統銷售合約絕大多數營收在 2027 認列（原話："We anticipate the vast majority of the revenues from these"）
- 2026-07-22｜CFO｜guidance：CFO 預期自由現金流持續承壓（原話："we expect the free cash flow will remain under pressure"）
- 2026-07-22｜CFO｜guidance：CFO 說明折舊與資料中心營運成本將壓抑損益（原話："in the form of higher depreciation expense and"）
- 2026-07-22｜CFO｜margin：Cloud 營業利益率由 20.7% 升至 35.6%（原話："operating margin increased from 20.7% in the second quarter"）
- 2026-07-22｜CFO｜margin：Google Services 營業利益率 41.8%（原話："operating margin was 41.8%"）
- 2026-07-22｜CFO｜margin：集團營業利益 30% 成長至 $40.8B，營業利益率 34%（原話："Operating income increased 30% to $40.8 billion"）
- 2026-07-22｜CFO｜margin：其他營收成本成長的拆解含 TPU 系統銷售的存貨成本（原話："inventory costs, primarily from the sales of TPU systems to"）
- 2026-07-22｜CFO｜margin：CFO 表示 Q3 擴大第三方容量將使 Cloud 營業利益率承壓（原話："will put some pressure on operating margins for"）
- 2026-07-22｜CFO｜margin：CFO 提到 Wiz 整合在 2026 近期造成利潤率逆風（原話："the integration of Wiz does create some"）
- 2026-07-22｜CFO｜margin：CFO 不拆分 TPU 等個別產品的利潤率（原話："we don't break out margins for any specific products"）
- 2026-07-22｜CFO｜margin：G&A 成長含法律等相關費用（原話："charges for certain legal and other"）
- 2026-07-22｜CFO｜margin：OI&E 大增主要來自權益證券未實現利得（原話："unrealized gains in our equity securities portfolio"）
- 2026-07-22｜CFO｜product：Cloud 營收 +82% 至 $24.8B（原話："Cloud revenues were up 82% to $24.8 billion"）
- 2026-07-22｜CFO｜product：Search and Other 營收 +17% 至 $63.3B（原話："other advertising revenues increased by 17% to $63.3 billion"）
- 2026-07-22｜CFO｜product：Network 廣告營收年減 1%（原話："Network advertising revenues of $7.3 billion were down 1%."）
- 2026-07-22｜CEO｜product：CEO 說明模型 API 每分鐘處理 token 量（原話："approximately 22 billion tokens per minute"）
- 2026-07-22｜CEO｜product：CEO 說明 Gemini app 月活（原話："950 million monthly active users"）
- 2026-07-22｜CEO｜product：CEO 說明 AI Mode 月活突破 10 億（原話："we have surpassed 1 billion monthly active users"）
- 2026-07-22｜CEO｜product：CEO 說明 AI Mode 回應成本降至上線以來最低（原話："reduced the cost of AI Mode responses to its lowest level"）
- 2026-07-22｜CEO｜product：CEO 表示已啟動 Gemini 4 最大規模預訓練（原話："ambitious pretraining run yet for Gemini 4"）
- 2026-07-22｜CEO｜product：CEO 說明 3.6 Flash 在 DeepSWE 進步（原話："compared to 3.5 Flash jumped over 10 points in"）
- 2026-07-22｜CBO｜product：YouTube 訂閱業務成長快於廣告（原話："is growing faster than ads"）
- 2026-07-22｜CBO｜product：AI Max 採用者平均轉換或價值增幅（原話："AI Max or PMax see an average of 15% more"）
- 2026-07-22｜CEO｜customer：Cloud 現有客戶用量超出承諾 50% 以上（原話："their commitments by more than 50%"）
- 2026-07-22｜CEO｜customer：近 90% 財星百大使用 Gemini Enterprise（原話："nearly 90% of Fortune 100 are using Gemini Enterprise"）
- 2026-07-22｜CFO｜customer：CFO 說明 Cloud 積壓訂單中約一半 24 個月內認列（原話："to recognize just over 50% of the total backlog as revenue"）
- 2026-07-22｜CEO｜risk：CEO 表示持續供給受限（原話："we continue to be supply constrained"）
- 2026-07-22｜CEO｜competition：CEO 承認 coding／agentic coding 需改進（原話："Coding and agentic coding is an example of that"）
- 2026-07-22｜CEO｜competition：CEO 說明下一代前沿需要更大基礎模型（原話："we will need Gemini 4 as a larger base model to compete"）
- 2026-07-22｜CEO｜competition：CEO 回答護城河：模型只是解決方案的一環（原話："the model is just an ingredient in those solutions"）
- 2026-07-22｜CBO｜competition：CBO 說明對 AI Overviews 查詢的變現表現（原話："We continue to be encouraged with monetization performance"）
- 2026-07-22｜CEO｜commitment：CEO 承諾加快模型發布節奏至近月更（原話："releasing models almost at a monthly cadence"）
- 2026-07-22｜CFO｜commitment：CFO 表示只要有吸引人的回報就持續投資（原話："our goal is to invest as long as we see an attractive"）
- 2026-07-22｜CFO｜commitment：CFO 表示不再回到股權市場（ATM 為稅負 SBC 用途除外）（原話："we're not planning to go back to the equity markets"）
- 2026-07-22｜CFO｜capital_allocation：CFO 說明負債由約 $16B 擴增至約 $100B（原話："we went to about $100 billion across multiple currencies"）
- 2026-07-22｜CFO｜capital_allocation：CapEx 本季 $44.9B（原話："CapEx was $44.9 billion in the second quarter"）
- 2026-07-22｜CEO｜capital_allocation：CEO 說明橋接交易的投報評估（原話："is highly ROI positive"）
- 2026-07-22｜CEO｜capital_allocation：CEO 說明算力分配的基準（原話："what it takes to continue AGI development at the frontier"）
- 2026-07-22｜CEO｜capital_allocation：CEO 提到與 Blackstone 的 TPU 放置專案（原話："like the project we are doing with Blackstone"）
- 2026-07-22｜CEO｜capital_allocation：CEO 談 ROIC 看法（原話："we've gotten more bullish on the opportunities ahead"）
- 2026-07-22｜CEO｜capital_allocation：CEO 談 2027 投資的需求訊號（原話："the dynamics look healthier than where we were"）
- 2026-07-22｜CFO｜capital_allocation：Other Bets 營收與營業虧損（原話："operating loss was $1.8 billion as we continue"）
- 2026-07-22｜CEO｜capital_allocation：CEO 談 Waymo 目前聚焦（原話："We're really focused on scaling the business"）

### 問答異常語氣（迴避／改口／保留）
- GOOGL_Q2_2026_Earnings_Call_20260722.md｜問：Sheridan／Nathanson：TPU 系統銷售的利潤率（增量或較低）｜答法：CFO 表示不拆分個別產品利潤率，改談 TAM 擴張與 Cloud 整體 35.6%，未回答 TPU 是否較低利潤率
- GOOGL_Q2_2026_Earnings_Call_20260722.md｜問：Khajuria：TPU 長期是否發展成商用晶片事業｜答法：CEO 表示不想預測太遠，改談依需求與供給限制擴張
- GOOGL_Q2_2026_Earnings_Call_20260722.md｜問：Gawrelski：Waymo 在何種條件下可能移出 Alphabet 結構｜答法：CEO 未回答結構條件，改說聚焦執行與擴大規模
- GOOGL_Q2_2026_Earnings_Call_20260722.md｜問：Nowak：2027 CapEx 預算哲學與限制如何改變｜答法：CFO 未給 2027 數字，改談供給受限、全端效率與有吸引力回報就投資

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
{"date":"20260723","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"搜尋廣告挺過 AI 轉型（AI Mode/AI Overviews 貨幣化不劣於傳統搜尋，本次冷讀後下修信心語氣）","columns":{"2Y 驗證點":"搜尋廣告營收續成長 >10%、AI Mode 貨幣化不使每查詢營收結構下滑","5Y 驗證點":"搜尋仍是最大利潤池、「答案引擎」貨幣化 ≥ 連結搜尋","10Y 驗證點":"意圖層貨幣化在 AI 介面完成遷移","具體數字門檻":"搜尋 YoY ≥ 10%（Q2'26 +17%）且貨幣化不惡化","來源":"公司財報分部；AI Mode 1B MAU（法說）；零點擊 93%/CTR 1.76%→0.61%（web）","漂移觸發":"連 2 季 TTM 偏離 ≥ 5%（季節性/漂移分級）"}},{"id":"H2","text":"Google Cloud 維持 30%+ 成長 + margin 擴張，成第二利潤支柱","columns":{"2Y 驗證點":"Cloud 成長 >30%、OM >30%","5Y 驗證點":"Cloud 營收 >$200B、OM >35%（Q2 已達 35.6%）","10Y 驗證點":"Cloud 成主要利潤來源之一","具體數字門檻":"Cloud YoY ≥ 30%（Q2'26 +82%）、backlog 續增","來源":"公司法說（backlog $514B，QoQ +$50B）","漂移觸發":"連 2 季"}},{"id":"H3","text":"$195-205B capex 賺回資金成本（AI 基建 ROI）、FCF 於 ~2027 復原","columns":{"2Y 驗證點":"Cloud 產能轉營收、TPU 外售起量；FCF 於 ~2027Q1 越過谷底","5Y 驗證點":"FCF 復原至 >$60B、ROIC 不結構下滑","10Y 驗證點":"capex 強度回落、FCF margin 回 >12%","具體數字門檻":"FCF 復原軌跡 + ROIC > WACC","來源":"公司 capex guide（FY26 $195-205B）；FCF crossover ~2027Q1（web）","漂移觸發":"2027 全年 FCF 仍負 + Cloud OM 回落"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"搜尋每查詢貨幣化結構下滑（AI Mode 零點擊自我蠶食 + 外部 AI 助理分流資訊型查詢）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"搜尋營收 YoY vs 查詢量增；AI Mode 滲透率","警戒閾值":"搜尋 YoY"}},{"id":"R2","text":"AI capex 週期 digestion / overbuild（產業性需求放緩 → Cloud margin 擴張反轉 + 大型科技倍數壓縮，GOOGL 為最大 capex 部署者的相關性曝險）","columns":{"對應假設":"H2/H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Cloud 增速、Cloud OM、產業 capex/需求增速比","警戒閾值":"Cloud YoY"}},{"id":"R3","text":"反壟斷結構分拆（AdX/DFP 或 Chrome/Android）+ 折舊會計正常化壓 margin","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數）＋ AdX 為 binary tail","監測指標":"AdX 裁決 docket；折舊政策揭露","警戒閾值":"強制分拆生效；或折舊年限縮短 → EPS 下修 >10%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼觸發：AdX 裁決明朗（結構 vs 行為）或回檔 $300-320 或 2027 capex 指引與 Cloud ROI 對得上","irr_base_pct":8.5,"ev5y_pct":51.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.7,"ev5y_pct":51.0,"irr_base_pct":8.5,"max_dd_pct":-50.0,"bull_5y_price":718.0,"bear_5y_price":246.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"加碼觸發：AdX 裁決明朗（結構 vs 行為）或回檔 $300-320 或 2027 capex 指引與 Cloud ROI 對得上","price_at_dd":342.09,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GOOGL_20261103/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
