你是 stock-analyst **v20 判斷 agent**，標的 URI（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"URI","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/URI_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/URI_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"總營收（GAAP）","value":4893,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","citation":"公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001067701/000106770126000036/uri-9302026xex991.htm"},"note":"未查證"},{"id":"f_kpi1_ebitda_non_gaap_non_gaap","label":"調整後 EBITDA（公司揭露的 non-GAAP 獲利指標；新聞稿未揭露 non-GAAP 營業利益）","value":2331,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD m（利益率 47.6%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","citation":"公司新聞稿 8-K Ex.99.1 同上"},"note":"未查證"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":1409,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD m（利益率 28.8%，自算）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","citation":"公司新聞稿 8-K Ex.99.1 同上"},"note":"未查證"},{"id":"f_kpi5_2026","label":"全年 2026 指引（上調）","value":"營收 18.0–18.2B；調整後 EBITDA 8.3–8.4B；gross rental capex 5.2–5.5B；營運現金流 6.25–6.85B；FCF（不含重組付款）2.15–2.45B","period":"Q3 FY2026（公告於 2026-10-21）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026（公告於 2026-10-21）","citation":"公司新聞稿 8-K Ex.99.1 同上"},"note":"未查證"},{"id":"f_kpi6_fleet_productivity","label":"車隊生產力（fleet productivity）","value":6.5,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","unit":"% YoY","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","citation":"公司新聞稿 8-K Ex.99.1 同上"},"note":"未查證"},{"id":"f_kpi7","label":"二手設備銷售收入","value":348,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD m（YoY +4.5%；GAAP 毛利率 44.8%，調整後 46.3%；OEC 回收率 51.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","citation":"公司新聞稿 8-K Ex.99.1 同上"},"note":"未查證"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-21","period":"2026-10-21","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-21"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_uri_gross_margin_pct","label":"URI 毛利率","value":38.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.URI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uri_operating_margin_pct","label":"URI 營業利益率","value":25.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.URI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_uri_fcf_margin_pct","label":"URI FCF 利潤率","value":3.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.URI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hri_gross_margin_pct","label":"HRI 毛利率","value":31.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HRI.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hri_operating_margin_pct","label":"HRI 營業利益率","value":13.14,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HRI.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hri_fcf_margin_pct","label":"HRI FCF 利潤率","value":-2.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HRI.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wsc_gross_margin_pct","label":"WSC 毛利率","value":50.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WSC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wsc_operating_margin_pct","label":"WSC 營業利益率","value":20.41,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WSC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wsc_fcf_margin_pct","label":"WSC FCF 利潤率","value":12.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WSC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cat_gross_margin_pct","label":"CAT 毛利率","value":32.46,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cat_operating_margin_pct","label":"CAT 營業利益率","value":17.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_cat_fcf_margin_pct","label":"CAT FCF 利潤率","value":12.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":272,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","citation":"公司新聞稿 8-K Ex.99.1 同上"},"note":"未查證"},{"id":"f_kpi4_sbc_stock_compensation_e","label":"SBC（stock compensation expense, net）占 GAAP 營業利益","value":3.05,"period":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","unit":"%（SBC 43 ÷ 營業利益 1,409，自算；占營收 0.88%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）","citation":"公司新聞稿 8-K Ex.99.1 同上"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1098.88,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":13.2,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":60.2,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":3.54,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（50.07 → 51.84）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":4.66,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（58.2 → 60.91）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":5.81,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（65.42 → 69.22）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":51.84,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":60.91,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":69.22,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":21.2,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 51.84，分子＝快照價 1098.88","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.701,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 1098.88 / W52 938.92 / W104 853.64 / W250 619.24 / W250 13週斜率 1.97%"},{"id":"f_ma_w52","label":"52 週均線","value":938.92,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":853.64,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":619.24,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.97,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"URI 2025 年北美市占約 15%，與 2024 年底相比無重大變化（份額持平）。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770126000007/uri-20251231.htm","excerpt":"Our estimated North American market share of approximately 15 percent as of December 31, 2025, which is based on industry estimates (excluding party and event rentals) from the American Rental Association (“ARA”), did not change materially from our market share as of December 31, 2024.","as_of":"2026-01-28","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 描述產業高度分散、競爭者含小型獨立業者、區域業者、全國性公司及設備廠商／經銷商；URI 自述相對市占小可能不利於抑制租金價格壓力。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770126000007/uri-20251231.htm","excerpt":"The fragmented nature of the industry and our relatively small market share, however, may adversely impact our ability to mitigate rental rate pressure.","as_of":"2026-01-28","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子承認過去競爭壓力曾造成市占或價格下降，未來可能再發生，並可能遇到新競爭者。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770126000007/uri-20251231.htm","excerpt":"We may in the future encounter increased competition from our existing competitors or from new competitors.","as_of":"2026-01-28","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"某 2026 年 2 月分析稿估計 URI 北美份額約 15%，次大對手 Sunbelt 約 11–13%（來源間數字不一，無跨期比較）。","source":"Finterra／FinancialContent：United Rentals (URI): The Industrial Titan Navigating a New Economic Normal","url":"https://markets.financialcontent.com/stocks/article/finterra-2026-2-5-united-rentals-uri-the-industrial-titan-navigating-a-new-economic-normal","excerpt":"URI holds a 15% market share in North America. Its nearest rival, Sunbelt Rentals—owned by Ashtead Group (LSE: AHT)—holds approximately 11-13%.","as_of":"2026-02-05","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2025 10-K 顯示最大客戶僅占總營收 1%、前十大客戶合計 5%（前一年相同），客戶高度分散；搜尋未見最大客戶導入第二供應商或自製租賃車隊的來源。","source":"SEC EDGAR 10-K FY2025 客戶集中度表","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770126000007/uri-20251231.htm","excerpt":"Largest customer percent of total revenues | 1%","as_of":"2026-01-28","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"最大客戶占 2025、2024、2023 各年總營收 1% 以下；應收帳款最大單一客戶約占總應收 2%（2025 與 2024 年底），客戶基礎分散，信用集中度低。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770126000007/uri-20251231.htm","excerpt":"Our largest customer accounted for one percent or less of total revenues in each of 2025, 2024 and 2023. Our customer with the largest receivable balance represented approximately two percent of total receivables at December 31, 2025 and 2024.","as_of":"2026-01-28","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q2 2026 財報摘要稱管理層提到 S&P 可能調升至投資等級（公司自身信用，非客戶）","source":"fn2.ai URI FY2026 Q2 earnings","url":"https://fn2.ai/earnings/uri/2026-q2","excerpt":null,"as_of":"2026-07-25","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2 2026 財報電話會議：管理層上調 2026 指引，並表示大型專案需求延續至 2027；總營收指引 $17.5–17.8B，租賃資本支出 $4.85–5.25B","source":"MarketBeat United Rentals Q2 2026 Earnings Call Transcript","url":"https://www.marketbeat.com/earnings/reports/2026-7-21-united-rentals-inc-stock/","excerpt":"I was intrigued by the comment historically high time utilization. I was trying to see the industry add capacity again, and you always wonder about supply-demand balances when we get a recovery in the CapEx numbers. David Raso Analyst at Evercore ISI 00:15:28 That historically high time you comment, given the nature of large projects, more long-dated, is some of the CapEx increase being","as_of":"2026-07-22","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q3 2026 新聞稿：營收 $4.893B、調整後 EPS $15.55、車隊生產力年增 6.5%","source":"SEC 8-K Ex.99.1 (2026-09-30 quarter)","url":"https://www.sec.gov/Archives/edgar/data/0001067701/000106770126000036/uri-9302026xex991.htm","excerpt":"GAAP diluted earnings per share (“EPS”) of $14.77, and adjusted EPS3 of $15.55. •Adjusted EBITDA3 of $2.331 billion, at a margin2 of 47.6%. •Year-over-year, fleet productivity4 increased 6.5%.","as_of":"2026-10-21","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"URI 與同業被控透過 RB Global 子公司 Rouse Services 共享定價資料而共謀操縱價格的私人集體訴訟；URI 稱指控毫無根據並將積極抗辯（非政府調查）","source":"Equipment Finance News｜RB Global, United Rentals call antitrust claims meritless","url":"https://equipmentfinancenews.com/news/rentals/rb-global-united-rentals-call-antitrust-claims-meritless","excerpt":null,"as_of":"2025-04-03","retrieved_at":"20261024","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"FY2025 10-K 風險因子：新設備成本（含原物料關稅）上升可能影響租賃車隊成本與財務結果；關稅列為可能推高成本的因素之一","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770126000007/uri-20251231.htm","excerpt":"The cost of new equipment for use in our rental fleet has increased, and could continue to increase in the future, due to increased material costs for our suppliers (including tariffs on raw materials) or other factors beyond our control.","as_of":"2026-01-28","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-06 Section 232 調整：農業與部分 HVAC 設備關稅由 25% 降至 15%，符合條件資本設備 10% 稅率，6/8 生效（設備供應鏈背景）","source":"my-equipment.com 2026 tariff changes on construction equipment","url":"https://www.my-equipment.com/blog/2026/08/how-the-2026-tariff-changes-on-construction-equipment-affect-manufacturers-dealers-and-buyers/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261024","affects":["valuation","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"URI 管理層稱資本支出已全年談妥，關稅預期不增加成本；不確定性利於租賃","source":"Equipment Finance News: United Rentals may benefit","url":"https://equipmentfinancenews.com/news/rentals/united-rentals-may-benefit-as-clients-become-weary-of-ownership/","excerpt":null,"as_of":"2025-04-25","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 年報稱營運受通膨、關稅、利率與供應鏈限制等全球經濟條件影響；供應鏈中斷的衝擊至今有限，但不排除更嚴重的中斷。未披露供應商集中度或中國採購占比。","source":"United Rentals Form ARS FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1067701/000119312526124155/uri_ars_fye_2025.pdf","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"10-K 風險因素（FY2020–FY2023 版本相同）：集中採購使公司依賴一組關鍵供應商並承受其信用風險；供應商財務困難可能無法履約或要求重談條款。未點名單一製造商。","source":"United Rentals Form 10-K FY2023 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770124000007/uri-20231231.htm","excerpt":null,"as_of":"2024-02-01","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"URI 2026Q3 rental revenue +17.8% YoY to record $4.316B；驅動：平均原始設備成本 +7.9%、車隊生產力 +6.5%、附屬與轉租 +4.9%","source":"URI 8-K Ex.99.1 (Q3 2026)","url":"https://www.sec.gov/Archives/edgar/data/0001067701/000106770126000036/uri-9302026xex991.htm","excerpt":"Rental revenue increased 17.8% year-over-year, to a quarterly record of $4.316 billion","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 General Rentals 設備租賃營收 +8.8% YoY，歸因於平均 OEC 增加、需求強勁、附屬與轉租增加","source":"URI 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001067701/000106770126000034/uri-20260930.htm","excerpt":"General rentals equipment rentals increased $212, or 8.8 percent","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Specialty 設備租賃營收 +34.7% YoY","source":"URI 10-Q 2026-09-30","url":"https://www.sec.gov/Archives/edgar/data/0001067701/000106770126000034/uri-20260930.htm","excerpt":"Specialty equipment rentals increased $439, or 34.7 percent","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 財報會上管理層稱資料中心持續是成長來源，大型專案管線延續至明年，但未給 2027 指引；2026 營收指引上調至 $17.5–17.8B","source":"United Rentals Q2 2026 Earnings Call Transcript (MarketBeat) / Nasdaq","url":"https://www.marketbeat.com/earnings/reports/2026-7-21-united-rentals-inc-stock/","excerpt":null,"as_of":"2026-07-21","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"ARA（S&P Global 資料）2026年5月預測：美國 CIE 與一般工具租賃 2026 +3.6%（$83.5B）、2027 +3.8%、2028 +4.4%；Equipment Journal 版本數字不同（3.4/4.4/5.1），來源間不一致","source":"RER / Equipment Journal 報導 ARA 預測","url":"https://www.rermag.com/news-analysis/headline-news/article/55379161/american-rental-association-releases-updated-equipment-event-economic-forecasts-for-north-america","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261024","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"S&P Global 稱 CIE 板塊因營建市場停滯而處於停滯，一般工具板塊持續前進","source":"RER 報導 ARA 預測","url":"https://www.rermag.com/news-analysis/headline-news/article/55379161/american-rental-association-releases-updated-equipment-event-economic-forecasts-for-north-america","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"Sunbelt 為美國第二大租賃商，市佔約 11%，車隊逾 $20B；FY2026 租賃營收約 +3.4%，FY2027 指引租賃營收成長 5–8%","source":"Sunbelt Rentals Holdings profile (PitchBook/Walnut)","url":"https://walnutinvest.com/stocks/sunb","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"-","claim":"2025 年聯邦反托拉斯集體訴訟指 Sunbelt、URI、Herc 等藉 Rouse 租價基準資料協同定價，案件未決","source":"Sunbelt profile 摘要","url":"https://walnutinvest.com/stocks/sunb","excerpt":"A federal antitrust class action filed in 2025 names Sunbelt alongside United Rentals, Herc, H&E and Sunstate","as_of":"2026-09-01","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"URI 10-K 風險因子載明：客戶需求變化可能使部分現有設備過時，須以更高成本購置新設備（FY2023 10-K 文字；搜尋未找到具名替代技術取代租賃的來源）","source":"SEC EDGAR, United Rentals 10-K FY2023, Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770124000007/uri-20231231.htm","excerpt":"changes in customer demand could cause certain of our existing equipment to become obsolete and require us to purchase new equipment at increased costs.","as_of":"2024-02-01","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"URI 推出 Equipment Agent 並上架 ChatGPT，為首個租賃設備類應用（自身數位化動作）","source":"United Rentals 新聞稿","url":"https://investors.unitedrentals.com/press-releases/press-releases-details/2026/United-Rentals-Expands-Digital-Customer-Experience-with-Equipment-Agent-Launch-in-ChatGPT/default.aspx","excerpt":"United Rentals Expands Digital Customer Experience with Equipment Agent Launch in ChatGPT May 19, 2026 Download (opens in new window) Early adoption signals strong demand for faster equipment planning","as_of":"2026-01-01","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Q2 2026 專業租賃營收年增約 25%，管理層強調一站式（通用＋專業）模式","source":"MarketBeat United Rentals Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/united-rentals-q2-earnings-call-highlights-2026-07-23/","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 財報（2026-10-21）上調全年指引：營收 $18.0–18.2B（前 $17.5–17.8B）、調整後 EBITDA $8.3–8.4B（前 $7.975–8.125B）、淨租賃 capex $3.75–4.05B（前 $3.4–3.8B）、FCF $2.15–2.45B 不變","source":"SEC 8-K Ex.99.1 United Rentals Q3 2026 earnings release","url":"https://www.sec.gov/Archives/edgar/data/0001067701/000106770126000036/uri-9302026xex991.htm","excerpt":"$18.0 billion to $18.2 billion","as_of":"2026-10-21","retrieved_at":"20261024","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"目標價共識：Investing.com 均值約 $1,269（約 17% 上檔）；Benzinga 18 位分析師均值 $1,173、最高 $1,466（Truist）；Stockanalysis 22 位均值 $1,149.62","source":"Investing.com / Benzinga / Stockanalysis","url":"https://uk.investing.com/equities/united-rentals","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 目標價頁：共識 Buy、最高目標 $1466","source":"Benzinga URI price targets","url":"https://kr.benzinga.com/quote/URI/price-targets","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月（2025-10-24至2026-10-24）共11份8-K，含重大項目者3份；經查為債務融資（2025-12 發行15億美元5.375%優先票據、2026-06 應收帳款購買協議修訂）與新50億美元庫藏股計畫，清單中無2.01併購完成、4.02重編、3.01下市等項目。","source":"SEC EDGAR｜8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001067701&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"2026-01-28宣布新的50億美元庫藏股計畫，2026年計畫買回15億美元。","source":"SEC EDGAR｜8-K Item 8.01","url":"https://www.sec.gov/Archives/edgar/data/1067701/000106770126000009/uri-20260128.htm","excerpt":"On January 28, 2026, the Company announced a new $5.0 billion share repurchase program that does not have an established expiration date.","as_of":"2026-01-28","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"近12個月8-K清單中未見2.01（完成併購）項目；重大項目為債務融資與庫藏股。","source":"SEC EDGAR｜8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001067701&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"URI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.36,"operating_margin_pct":25.1,"fcf_margin_pct":3.75,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.URI","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HRI","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.95,"operating_margin_pct":13.14,"fcf_margin_pct":-2.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HRI","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"AHT.L","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AHT.L"},"note":"quarterly_income_stmt 無資料"},{"name":"WSC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.54,"operating_margin_pct":20.41,"fcf_margin_pct":12.98,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WSC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CAT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.46,"operating_margin_pct":17.52,"fcf_margin_pct":12.04,"rd_intensity_pct":3.04},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAT","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"URI"},"financial_history":{"ticker":"URI","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":11642000000.0,"revenue_yoy_pct":null,"gross_margin_pct":42.91,"operating_margin_pct":27.76,"net_income":2105000000.0,"diluted_eps":29.65,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":14332000000.0,"revenue_yoy_pct":23.11,"gross_margin_pct":40.56,"operating_margin_pct":26.9,"net_income":2424000000.0,"diluted_eps":35.28,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":15345000000.0,"revenue_yoy_pct":7.07,"gross_margin_pct":40.08,"operating_margin_pct":26.51,"net_income":2575000000.0,"diluted_eps":38.69,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":16099000000.0,"revenue_yoy_pct":4.91,"gross_margin_pct":38.16,"operating_margin_pct":24.68,"net_income":2494000000.0,"diluted_eps":38.61,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/URI/URI_Q3_2026_Earnings_Call_20261022.md）

# Q3 2026 Earnings Call
**United Rentals, Inc.** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Good morning, everyone, and welcome to the United Rentals Investor Conference Call. Please be advised that this call is being recorded.
Before we begin, please note that the company's press release comments made on today's call and responses to your questions contain forward-looking statements. The company's business and operations are subject to a variety of risks and uncertainties, many of which are beyond its control. And consequently, actual results may differ materially from those projected. A summary of these uncertainties is included in the safe harbor statement contained in the company's press release.
For a more complete description of these and other possible risks, please refer to the company's annual report on Form 10-K for the year ended December 31, 2025, as well as the subsequent filings with the SEC. You can access these filings on the company's website at www.unitedrentals.com. Please note that United Rentals has no obligation and makes no commitment to update or publicly release any revisions to forward-looking statements in order to reflect new information or subsequent events, circumstances or changes in expectations.
You should also note that the company's press release and today's call include references to non-GAAP terms, such as free cash flow, adjusted EPS, EBITDA and adjusted EBITDA. Please refer to the back of the company's recent investor presentation to see the reconciliation from each non-GAAP financial measure to the most comparable GAAP financial measure.
Speaking today for United Rentals is Matt Flannery, President and Chief Executive Officer; and Ted Grace, Chief Financial Officer. I will now turn the call over to Mr. Flannery. Please go ahead, sir.

**Matthew Flannery** (Executives):
Thank you, operator, and good morning, everyone. Thanks for joining our call. Yesterday afternoon, we were very pleased to report our third quarter results, which are a testament to our strategy, the team's dedication to the customer and the unmatched breadth and scale of our premier offering.
We came into 2026 expecting another year of growth. As evidenced by our results, the business continues to perform better than we expected. Large projects across a variety of end markets are driving our growth. And we expect this momentum will carry for the remainder of this year and into next year. We remain well positioned to outperform the industry with our broad footprint, our unmatched one-stop shop offering, accompanied by exceptional levels of service and leading technology and, of course, our unwavering commitment to safety.
These capabilities, combined with our customers' confidence and backlogs, support our revised guidance. We came into the year dedicated to being the partner of choice for our customers, accompanied by a laser focus on finding cost efficiencies. I'm very pleased with the team's efforts and how the year is playing out. Team United continues to raise the bar, providing an unmatched offering for our customers while also generating strong returns.
So let's get into the details of our third quarter results and our updated full year guidance and then Ted will get into more details around the numbers before we open up the call to Q&A.
Starting with the quarter's results. Total revenue grew by 16% year-over-year to $4.9 billion. Within this, rental revenue grew by 18% to $4.3 billion, both quarterly records. Fleet productivity of 6.5% contributed to OER growth of 12.9%. I'll note that time and mix all contributed to the quarter's productivity along with rate. Adjusted EBITDA was a record of $2.3 billion, resulting in a margin of 47.6%, an improvement of 160 basis points year-over-year. And finally, adjusted EPS came in at $15.55, up 33% year-over-year and another quarterly record.
Now let's discuss customer activity. The third quarter again saw growth across both our Gen Rent and Specialty business. Specialty was a standout with total revenue growth of 35% year-over-year, including 12 cold starts, which brings us to 40 cold starts year-to-date. Notably, each Specialty line of business reported strong double-digit growth in the quarter. By vertical, the trends in the first half of the year carried into the third quarter. Construction continues to grow across non-residential and infrastructure. And on the industrial side, power once again posted double-digit growth as did metals and minerals.
As I mentioned earlier, a variety of end markets drive our growth. This diversified exposure is an important and very intentional part of our strategy. With this in mind, we saw projects kick off in the third quarter across numerous end markets, including energy, manufacturing, infrastructure and data centers.
Now turning to the used market. We sold $677 million of OEC at a 51% recovery rate. The demand for used equipment remains strong, and we still expect to sell approximately $2.8 billion of fleet this year. Given the demand from our customers and our replacement of sold equipment, we spent $1.8 billion on gross rental CapEx in the quarter, and this takes us to $4.7 billion year-to-date. The combination of a strong demand environment and fleet productivity underpins this additional spend as we ensure we support our customers while driving profitable growth.
Subsequently, we generated year-to-date free cash flow of $1.4 billion. Even with higher CapEx needs, we're able to generate meaningful free cash flow due to a combination of our industry-leading profitability, capital efficiency and the flexibility of our business model. This strong free cash flow is redeployed in ways that allow us to augment shareholder value and is a critical part of our strategy.
Finally, our capital allocation in the quarter reflects the disciplined framework we employ. Our balance sheet is very healthy, allowing us to support both organic and inorganic growth and to also return nearly $500 million to shareholders during the quarter through a combination of share buybacks and our dividend. Our leverage of 1.8x remains well within our targeted range of 1.5 to 2.5x, leaving plenty of dry powder to support growth and to return excess capital to our shareholders.
We've long talked about the importance of financial strength to support our strategy and to drive long-term value creation. To this point, we were very pleased to see S&P acknowledge our efforts with their upgrade of our credit rating to investment grade earlier this month.
As we enter the last few months of 2026, our focus is unchanged. The demand environment for large projects remains robust, supporting our revised guidance, which reflects over 12% total revenue growth with EBITDA margins over 46%, all at the midpoint. We increased our CapEx guidance to over $5.3 billion at the midpoint as we see the opportunity to put even more equipment on rent while generating strong free cash flow and returns.
So in conclusion, the United Rentals team's diligent focus on our strategy day in and day out is delivering results we're all very proud of. Over the last nearly 30 years, we built and continue to expand the value proposition, which differentiates us in the industry. Our business model is truly unique and goes beyond purely equipment rental. By layering on technology, innovation and unmatched service across both our Specialty and Gen Rent businesses, we support our customers' productivity and drive a better partnership. And for our shareholders, this translates to profitable growth, strong free cash flow and compelling returns.
And with that, I'll hand it over to Ted to review our financial results, and then we'll take your questions. Over to you, Ted.

**William Grace** (Executives):
Thanks, Matt. Good morning, everyone. As Matt just shared, the team delivered strong results that exceeded even our raised expectations from last quarter. Quarterly records for total revenue, rental revenue, EBITDA and EPS. Beyond that, we raised our full year guidance for revenue and EBITDA to reflect our expectations that this performance will continue through year-end in support of a record 2026. But before we get into the details of the updated guidance, let's review the third quarter's results.
As you saw in our press release, rental revenue increased 17.8% to over $4.3 billion, supported once again by the team's strong execution across large projects and key verticals. Within this, OER increased by 12.9%, driven by a 7.9% increase in our average fleet size and fleet productivity of 6.5%, partially offset by assumed fleet inflation of 1.5%. And finally, within rental revenue, ancillary and re-rent grew over 37%, again outpacing OER growth by a healthy margin.
Pivoting to used, we sold $677 million of OEC in the quarter, generating $348 million of proceeds at an adjusted margin of 46.3% and a 51.4% recovery rate. As Matt mentioned, consistent with our initial guidance, we're on track to sell approximately $2.8 billion of OEC this year at a recovery rate in the low 50s in what remains a healthy used equipment market.
Next, let's turn to adjusted EBITDA, which increased $385 million to a record of over $2.3 billion. This was driven primarily by a $417 million increase in rental gross profit and an $8 million increase in used gross profits. SG&A increased by $54 million, translating to a 20 basis point improvement as a percentage of revenue, while gross profits from other lines of businesses added $14 million.
Looking at profitability. Our third quarter adjusted EBITDA margin increased 160 basis points to 47.6%, reflecting another quarter of strong cost discipline. While there were always -- while there will always be some quarter-to-quarter variability, we are very pleased with our team's ability to efficiently leverage our third quarter growth to offset the impacts of both lower-margin ancillary and re-rent revenues and other inflationary pressures.
Shifting to CapEx. We've responded to robust customer demand by investing over $4.7 billion in gross rental CapEx year-to-date, which is an increase of almost $1 billion year-over-year.
Moving to returns and free cash flow. Our return on invested capital increased 30 basis points year-over-year to 12.3%, which remains comfortably above our weighted average cost of capital, while our free cash flow year-to-date has exceeded $1.4 billion.
Turning to our balance sheet. Net leverage remains very comfortable at 1.8x at the end of September with total liquidity of over $2.6 billion. As Matt mentioned, we are very pleased to see S&P's recognition of our commitment to maintaining a strong balance sheet by upgrading our credit rating to investment grade earlier this month. We view this as a testament to our disciplined financial policies around leverage, liquidity and maturity management, as well as the strength and durability of our free cash flow.
Turning to capital allocation. Through the third quarter, we returned roughly $1.5 billion to shareholders, including $1.125 billion through repurchases and $371 million via dividends.
Now let's move to the guidance we shared last night, which reflects our confidence in delivering another record year. Total revenue is now expected in the range of $18 billion to $18.2 billion, an increase of $450 million at midpoint versus our prior guidance, while used sales are still expected at around $1.45 billion. At midpoint, this now implies full year total revenue growth, ex used, of better than 13% versus our initial 2026 guidance of closer to 6%.
In turn, we've also raised our adjusted EBITDA guidance by $300 million to a range of $8.3 billion to $8.4 billion, reflecting our continued expectation to bring the revenue growth to the bottom line and finish the year strong. Notably, at midpoint, excluding the benefit of the H&E termination fee last year and the gain on sale of our scaffolding business this year, this implies a roughly 70 basis point improvement in our full year EBITDA margin compared to the goal we initially shared in January of a flat full year margin.
On the fleet side, driven by strong customer demand, we've increased our gross CapEx guidance by $300 million to a range of $5.2 billion to $5.5 billion. This now implies net CapEx of $3.75 billion to $4.05 billion. And finally, we are reaffirming another year of strong free cash flow in the range of $2.15 billion to $2.45 billion, which reflects an increase in our cash flow from operations, offset by higher CapEx. I think it's important to call out that we've invested significantly in our fleet this year to drive strong organic growth, positioning the business for attractive returns over the coming years while also generating substantial free cash flow.
And finally, on the capital allocation front, we still intend to repurchase $1.5 billion of shares in 2026. Combined with our dividend, this will return roughly $2 billion to our shareholders this year, equating to approximately $32 per share or a return of capital yield of over 3% based on our current share price.
So with that, let me turn the call over to the operator for Q&A. Operator, please open the line.

**Operator** (Operator):
[Operator Instructions] We'll go first this morning to David Raso with Evercore ISI.

**David Raso** (Analysts):
The margins were impressive and the sustainability of that improvement is sort of the spirit of the question. The pricing opportunity you see coming up as some larger projects roll off to new ones, maybe some flexibility in pricing in current multiyear projects, just give us a sense of how you're thinking about the chance to maybe improve the pricing on those? Any change there?
And the same idea of, structurally, there are probably some ceiling to how high time utilization could go. And I mean, at least versus history, it feels like we're maybe getting a bit close to that ceiling. If that's the case, should we think of how we address that high ceiling as expect strong CapEx next year, but also maybe an increased focus on rental rate?

**Matthew Flannery** (Executives):
Thanks, David. I mean what you're touching on, right? You see we're doing all 3 components very strongly here in the quarter with the productivity of 6.5% that you saw. With all that being said, rates have been climbing and been a good guy for us for quite some time. And that's necessary because of the inflation that we're all experiencing in the industry. So we expect that to continue next year. Certainly, the demand environment and the high time utilization, to your point, assist that. So we feel really good about that opportunity.
And as far as the CapEx, we'll get to that when we get to January guidance. But it's a fair point that maybe running at this level of time utilization isn't the most prudent thing to do. We're doing it out of necessity right now, right? But we could temper that a little bit next year, which will require a little more CapEx, but not a lot. I think we'll get to that in January once we get through our planning process here throughout the fourth quarter and let you guys know in January.

**David Raso** (Analysts):
Any thoughts you maybe could provide on the rate opportunity, thinking about larger projects still as a base case driving the business next year. And obviously, any other color between rate growth for Gen Rent versus Specialty?

**Matthew Flannery** (Executives):
Yes, we're seeing positive fleet productivity throughout all business units and throughout all project types and all customer sets. So this isn't just unique to projects or local market or industrial. This is across-the-board, concerted effort for all of us to make sure we recapture the cost that we're absorbing.

**Operator** (Operator):
We go next now to Rob Wertheimer with Melius Research.

**Robert Wertheimer** (Analysts):
One of the concerns people had heading into the year, if we go back a few quarters, is just the fleet movement costs in a market that was bifurcated, soft on one side, strong in another. And it seems like you've alleviated that. I'm sure some of that is internal management. I wonder how much of that is the overall market has tightened up. And I wonder if you could just sort of comment on that dynamic and if it remains a risk or a focus.

**Matthew Flannery** (Executives):
Sure, Rob. It's really been a lot of internal management and process change more than anything. The reality is a tighter market could require more movement. So I think the team has done a great job. We obviously put more process changes and eyeballs into it. And it wasn't that the team was doing anything wrong last year, we just needed to see how we could do it better. We have a team that's very responsive to customer demand. And if we could bundle some of those responses together, and put a little more elbow grease into making sure cost was a big variable in these decisions, that's the result that you saw.

**Robert Wertheimer** (Analysts):
Perfect. And then just kind of more generally, and I guess, maybe David just touched on this, but as you roll through the mega-project era, you guys had a ton of value with fleet diversity, technology, service, uptime, all these different things you guys do well. Are conversations around the value you deliver to mega projects more constructive now than they were in the past? Do people kind of realize how much you can save through all those -- delivering all those factors?

**Matthew Flannery** (Executives):
Yes, I certainly think that surety of supply and the one-stop shop value proposition have definitely taken more prominence really in the last year plus. When you run a big site, not having a bunch of vendors running around is very helpful for the folks that have to control the security and the safety of that site. And I think probably all the large companies are playing favorable there, but we certainly think our unique value prop advantages us there.

**Operator** (Operator):
We'll go next now to Jerry Revich with Wells Fargo.

**Jerry Revich** (Analysts):
Yes, I just wanted to ask on the cost performance, what really stood out is really strong labor and R&M productivity across both General and Specialty rentals. And earlier this year, you folks have implemented a number of rationalization plans. Can you just update on where we stand on that? And is there more runway for further efficiency gains from here? Are we at the run rate from those efforts?

**William Grace** (Executives):
Sure. Thanks for the question, Jerry. Yes, to your point, this is something we've been talking about publicly since January, something we challenged the team to do early in the year, and they've delivered incredibly well. Certainly, we've gotten very good labor absorption and that you can see that in both sides of the businesses. And you mentioned R&M. But almost back to Rob's question, I think the team has also done an extraordinary job on the delivery side. And so we said that all 3 of those would be critical to producing kind of better margins year-on-year.
In terms of the restructuring, that's really played out in line with expectations. So the benefits have been consistent, and they really are not a big part of what's driven the year-on-year improvement. So they've been helpful for sure, and we were prepared to take those actions. But at the end of the day, it's really been the team's focus on leveraging growth efficiently.
So you think about growth, I mean, growth itself has been very strong, stronger than we expected. The composition of growth has been very strong. You can see that in the fleet productivity. And then to your point, the team has just done a really good job driving efficiency across those big 3 buckets. And that's something we've long talked about. It's a challenge we've got to meet every year. We feel like the team has done a great job prior to '26, to be honest, and we talked about that publicly.
And going forward, almost coming back to something David asked about, the sustainability, this is just how we run the business. And so there's always going to be an ebb and flow to all these dynamics. But certainly, our expectation is we'll continue to deliver. Our goal is to deliver margin expansion always, and we feel like we've got a good recipe to continue driving strong results.

**Jerry Revich** (Analysts):
And Matt, can I ask just to expand in your prepared remarks, you spoke about delivering to manufacturing as well as power? So what we're seeing in the semi fab plants is for plants to double CapEx '27 versus '26? Is that the magnitude of the start-up deliveries that you folks are alluding to when you mentioned in the prepared remarks the manufacturing? And can you expand on just the magnitude of growth in power because in addition to utility CapEx growth, obviously, behind-the-meter is set to more than double as well. Are you seeing that level of growth in those verticals?

**William Grace** (Executives):
So we don't get too specific in verticals, but certainly, we feel like we're very well positioned to be that partner of choice for the kinds of contractors that build the kind of facilities you're alluding to, the very high-spec demanding customers. So we feel very good there. I'm not sure we'd kind of quantify what that translates to too specifically, but we're doing very well there.
And on the power side, we saw double-digit growth. It's been a trend we've been talking about publicly for a while. And so certainly, that's actually not going to be behind-the-meter piece as much as it is working with investor-owned utilities across generation, transmission, distribution, all of which have been key elements to our power vertical strategy since really for over a decade since we introduced in '16, Matt?

**Matthew Flannery** (Executives):
Yes. Yes. And I think the broader point is our end markets are very diverse. We cover a broad range of end markets, both in construction and in industrial as well as infrastructure and all with the same fungible assets. And I think that's really the story there. For example, even in power, we're not doing a bunch of specialty power assets, right, or large scale to power some of these projects. We're really staying in our lane, and I think it's playing out really well for us. It gives us a lot of flexibility.

**Operator** (Operator):
We'll go next now to Angel Castillo with Morgan Stanley.

**Angel Castillo Malpica** (Analysts):
Could we just talk about price cost a little bit. As you start to do your 2027 planning, I know we're still a little bit early, but can you just talk about what kind of levels of inflation you're seeing across the major buckets of cost of goods sold? Again, you've done a great job so far here in 2026 covering that. So it would be helpful to understand how you're seeing that progression or the implications of cost inflation next year.
And as it relates to the questions earlier on rental rate, how much of that has maybe already been kind of secured through recent renewals or projects or just kind of increases versus -- and would just kind of roll through into next year versus how much do you still need to kind of go out there and get as you do renewals of contracts?

**William Grace** (Executives):
Yes. So touching on the first piece, Angel. Look, inflation is very real. It's certainly not benign. It's certainly not deflationary. I think it depends on the bucket. On the one hand, you look at that labor absorption we talked about. I mean, frankly, that's why we're absorbing above-trend merit increase. And we think that's important. We want to take care of our people. I think we pride ourselves on being the employer of choice, and that certainly means taking care of your people in a lot of ways. And so I can tell you we proudly think about the way that we reward our team for the great job they deliver. But honestly, the underlying increase is above trend, and yet you're still seeing the team offset that through productivity gains.
Within R&M, you can imagine that's another area where our suppliers are focused on their pricing on parts, and yet we've been able to manage that very effectively. And within delivery, what is incredible, I think people see what's happened with diesel. They can see what's happening with freight rates. And yet here, again, we've been able to offset that. So it's not at all to suggest that we're in some kind of deflationary beneficial cost environment.
Going forward, our -- we'll see how next year shapes up. There's a lot of dynamics to consider as we get into planning internally and then what that translates to from a forecasting perspective. But I come back to our goal is to be as efficient as possible and consistently deliver strong margin performance across the business.

**Angel Castillo Malpica** (Analysts):
And the second part of your business...

**Matthew Flannery** (Executives):
As far as the rate component to the second part of your question about fleet productivity, first of all, we manage rate and time rigorously. It's the mix of the 2 that matters, which is why we talk about fleet productivity. But to be clear, we manage rate throughout the year. There is no magic date or point where we're doing renewals. We work with our customers throughout the year, making sure there's a balance to get paid for our value and making sure they could do what they need to do on the job, both physically and economically. And we think we've found a really good balance, and we don't expect that to stop anytime soon.

**Angel Castillo Malpica** (Analysts):
That's very helpful. And then maybe could we touch on capital allocation. You now have investment grade with one credit agency and when I look at your balance sheet, you still have quite a bit of kind of firepower. So maybe a couple of things. Maybe touch on what the implications to your -- perhaps your borrowing cost or cost of capital is from the shift to IG.
And then as we think about your current leverage or net leverage versus your target of kind of 2.5 at the high end. Is there anything preventing, I guess, you from being able to deploy more of that, whether it's the buybacks or for M&A? I know you did, I think, a little over $100 million this quarter. So just talk about the puts and takes there for capital deployment and perhaps timing?

**William Grace** (Executives):
Sure. So -- and I think we talked a little bit about this last quarter, but when you think about our capital allocation philosophy, it always starts with the balance sheet and where we position. Certainly, over the years, you've seen us evolve that strategy, get to the point where we've got a very strong balance sheet that will allow us to do pretty much anything we think makes the most sense for the company and the shareholders.
As a result of that, we changed our internal financial policy such that we felt comfortable moving to investment grade. And the concern we previously had was the potential constraints that could put on inorganic growth. But as the company has grown and the scale has gotten bigger and bigger and what that's done for our financial capacity, we realized that, frankly, we had the ability to do anything we wanted with the existing constraints. And as a result, we've changed that internal financial policy and communicated that externally, and that's really what's precipitated at least one of the upgrades.
So it doesn't change much. It really doesn't change anything internally. So there's no "cost." The benefit is obviously there's tighter spreads that we'll get with -- as an IG issuer versus high yield. I wouldn't want to speak for the market, but certainly people can look at kind of BBB- credits to get a sense for kind of what their yields would look like relative to ours. And we think it will be a very appreciable benefit that will, over time, as we refinance debt or issue debt for whatever reason, accrue benefit to the shareholders. But it doesn't change that strategy of starting with a strong balance sheet, investing in organic growth, funding smart M&A and then returning the excess capital to our shareholders.
It's really going to be that kind of framework for the -- I think, certainly for 2027 would be a reasonable assumption that that's the framework we use to figure out that capital allocation strategy. Does that answer all the questions? Or was there one at the end that you also want us to address?

**Angel Castillo Malpica** (Analysts):
Just more, I guess, in terms of the potential for timing of either buybacks or M&A, should kind of be leaning one way or another, how to kind of think about that?

**Matthew Flannery** (Executives):
Well, if there was any impact on our ability to do M&A, frankly, we wouldn't be doing it. So we don't see any impact there. And as far as the buybacks, stay tuned. I think we've been pretty consistent there.

**William Grace** (Executives):
Yes. We've got to go through that planning process to see what that growth opportunity is, what the investment looks like organically, get a sense for what that part of the use of cash would be. And then obviously, we'll assess kind of the M&A opportunity. And then what's left over, consistent with history, I think you can expect us to return that excess capital to our shareholders. So I wouldn't anticipate any change there to Matt's point.

**Operator** (Operator):
We go next now to Seth Weber with BNP Paribas.

**Seth Weber** (Analysts):
Appreciate all the comments about the strength in the mega projects and stuff. I just wanted to get your sense a little bit on the local markets. Are they -- would you characterize them as still being kind of stable? And just how much of a lag do you think we should expect? How long will it take for those markets to accelerate once interest rates start to come down in your experience?

**Matthew Flannery** (Executives):
Sure, Seth. So we would continue to call it stable now to be a little more information there for you. It probably gave us a couple of points of growth here in this quarter, but the big driver here is still the mega projects, large projects and our large customers driving this growth. So we like the fact that there was a little bit of growth there. As far as is that a pivot point? We don't know.
And for the second part of your question, we'll stick in our lane, as I said earlier, we have no idea how to forecast what that lag would be. What we do have is the ability to get -- especially as we go through our budget process, to have boots-on-the-ground feedback, and that's what we'll learn. And we'll count more on that than any kind of thoughts about what a lag would be. But we have heard for a while now sentiment has been more positive. We have seen a little bit of growth in a lot of these local markets. So we are feeling good about the direction of it.

**Seth Weber** (Analysts):
Okay. And I guess, just on the Specialty business, I think you're talking 40 -- north of 40 cold starts this year. Is that -- do you think that would accelerate next year? And have you started to see any change in the competitive landscape in the Specialty categories?

**Matthew Flannery** (Executives):
Yes. So we're slightly ahead of target this year. This is kind of a continuum of markets that our teams in each business unit have on their docket and where they want to grow into. We haven't done that work yet. That's part of the budget process. So I don't want to try to predict what we're going to come out with, but we still have white space geographically in some of these markets and really the ability to grow some density in markets where we already exist in some product lines as we've been outgrowing the existing facilities. So I think there'll be more opportunity, and we'll update you guys in January.
As far as the competitive set, there's always competitors that want to get into what we're doing, right? Somebody always covets thy neighbor's revenue, so to speak. What I will say is the barrier to entry and the value prop that we've built is really strong. So I think we've got a pretty good competitive moat there as far as what we offer to the customer.

**Operator** (Operator):
We'll go next now to Kyle Menges with Citi.

**Kyle Menges** (Analysts):
Maybe following up on Seth's first question on the local market. I'd just love to hear a little bit more of what you think is driving some of the positive sentiment in those local markets in spite of still a choppy macro backdrop and elevated interest rate environment?

**Matthew Flannery** (Executives):
I don't really have any additional color in aggregate. We're giving you a number in aggregate, but the puts and takes in all these different markets, right, the 1,800 branches that we're in almost in the U.S. and Canada, it would be really hard to homogenize that for you as far as what's driving it, but we are seeing local markets that do have some growth, and we'll update you guys on what we think that's going to turn into in 2027, but I don't really have any additional color for you.

**Kyle Menges** (Analysts):
Got it. And then ancillary again, outgrew OER pretty significantly this quarter. How should we think about that gap between the ancillary and OER growth potentially narrowing over time and maybe into 2027? And how much of it is just a matter of mega projects maturing into maybe a year 2, year 3, year 4 versus a lot more of them in year 1 and getting ramped up and maybe there's more ancillary revenue as those projects ramp up?

**Matthew Flannery** (Executives):
Yes. We view ancillary as responsive to customers' needs and their request, not really something we'll predict. I'm certain that Specialty growth is one driver of it. I'm certain that projects do tend to need more of it. But as we continue to add more offerings and customers are aware of what we have to offer them, it will be interesting to see if that -- how that spreads.
I think more importantly is we're just being a better provider to our customers. So for us, we don't have a target for it to grow it or to not grow it, it's to make sure that we're in a position to respond when the customer asks us to do something for them that's related to our products and our services. So really no ability to predict there because it is a responsive non-CapEx driven type of volume.

**Operator** (Operator):
We go next now to Chad Dillard with Bernstein.

**Charles Albert Dillard** (Analysts):
My question for you is on the CapEx raise in the quarter and what drove it? Is it the demand that you're seeing right now? Or are you preparing for what you're seeing ahead? And if you could, just like what end markets are getting better to drive that? And then maybe just secondly, what was the breakdown between what drove it, Gen Rent or Specialty?

**Matthew Flannery** (Executives):
Sure, Chad. I'd say yes to both. So it is the work that we see right in front of us right now. We had talked about how we're driving historically high time utilization. So this isn't a pull forward of stuff we're going to need next year. But certainly, the fact that we think 2027 is going to be a growth year gives us the confidence to support these growth needs that we have late in the year here in Q4. So it's really a little bit of both. 
And as far as -- I forgot the second part of your question.

**Charles Albert Dillard** (Analysts):
Yes, just Gen Rent versus Specialty, like what...

**Matthew Flannery** (Executives):
Yes. Thank you. So you see the growth of Specialty. So really for quite a few years now, Specialty gets an overweighted amount of the growth CapEx to support the cold starts and the growth that they're having. Outside of that, and once you get beyond Specialty, within our Gen Rent portfolio, we're really utilizing our full portfolio on these major projects because you think about it's pretty evenly spent throughout those categories that we carry in our Gen Rent stores.

**Charles Albert Dillard** (Analysts):
Got you. And maybe just double-clicking on Specialty, saw some pretty sizable growth, plus 30% in the quarter. Can you break down how much is from cross-sell or scope increase versus just like a dedicated Specialty sales? If you can't do it quantitatively, just give some qualitative color.

**William Grace** (Executives):
Yes. It's hard to break down too specifically. But certainly, when you think about the value proposition of being a one-stop shop, I mean, that is a good example of cross-selling. And so certainly, as we've been providing more and more products and services on these large projects that lend themselves very well to it, it certainly benefits, I guess, what you would call cross-sell. To us, it's solving problems for customers and making their lives as easy as possible. And that all kind of comes back to the strategy we've been talking about of being that partner of choice. But it's hard to peel it apart, Chad.

**Operator** (Operator):
We go next now to Mig Dobre with Baird.

**Mircea Dobre** (Analysts):
If we can go back to the discussion around ancillary and maybe double-click specifically on the re-rent revenue. I mean, we'll see how Q4 shapes out, but it looks to me like this line item is going to be up quite significantly, maybe 40% to 50% on a year-over-year this year. And I'm curious what the right way to interpret this or think about this is, is this a function of you guys just re-renting equipment in categories that maybe you're not participating? Or is this more of a kind of like a CapEx signal in terms of where demand is materializing and part of the reason why you're raising CapEx, simply not having enough equipment and having to source it from third party?

**Matthew Flannery** (Executives):
Yes. I would say it's the latter, Mig. I mean, this goes hand-in-hand with the demand environment and the time utilization that we're driving and part of the reason why you see a CapEx raise here. So it is the latter. And sometimes, it's -- I would say most of it, I won't say all because there's always something that we're getting to support a customer's need that we don't necessarily have in that market. Sometimes it's the more efficient play, especially for a short-term need or for something that we don't have access to handily at that moment of need. But overall, it is indicative of the combination of demand and high time utilization that we're running.

**Mircea Dobre** (Analysts):
Okay. That's helpful. And as you're raising CapEx, and I'm sure you'll give us an update on '27, it sounds like you're probably going to spend a little bit more, is it fair to expect this line item, re-rent, to maybe like flip to more towards OER? And does that kind of have a bit of a margin benefit that we need to contemplate if that's the case?

**William Grace** (Executives):
It's a good question. I would say, ultimately, certainly, as we pivot some of the stuff through -- into CapEx and we internalize those cash flows, it's going to benefit your OER line. But one of the things, again, is solving problems for customers. And so I think you've long seen kind of re-rent as part of our business for a lot of different reasons, whether it's sourcing additional capacity or providing those things as a one-stop shop service provider that for one reason or another, we don't own or don't want to own. So I'm hesitant to get too specific, but I think your logic makes sense. As we do convert some of that re-rent into OER via CapEx, that's going to benefit our core results.

**Matthew Flannery** (Executives):
Overall, not that big a number in the overall scheme of things and not something that we plan for. So it's hard even for us to model what that would be. So I don't know how to guide you to how you would, frankly.

**Operator** (Operator):
We'll go next now to Jamie Cook with Truist Securities.

**Jamie Cook** (Analysts):
Congrats on a nice quarter. I guess, just two questions. My first question, just with regards to conversations that you're having with OEs as you think about CapEx for 2027, any concerns on capacity constraints in the market? Or are we having conversations earlier just because of concerns on OEM availability? And just sort of the pricing setup for 2027?
And then, I guess, my second question, just the competitive dynamics, which I'm sure there's always new ones each cycle. But obviously, you have a large OE who's trying to get more aggressive in compact and trying to focus more on mega. We have new players in the market trying to double their OE. I guess, just, Ted, given what you're seeing in the market, do you think the improvement that we've seen in rental rates, do you think that could continue into 2027?
And I guess, to what degree are you concerned that some of these peers are -- could be potentially putting too much fleet into the market and that becomes an issue potentially at some point next year? Or do you just see this as sort of normal new entrants trying to do things and ultimately not making big waves in the market?

**Matthew Flannery** (Executives):
So I believe what we heard at the tail end was that Jamie asking a question, if you'd like to repeat it?

**Jamie Cook** (Analysts):
Want me to repeat both questions? I guess, the first question was just on talking to OEMs about 2027 concerns basically on any constraints in terms of you being able to get equipment and pricing.
And then my second question, it was just the competitive dynamics this cycle with a major OE trying to get more into compact and mega. Obviously, other public players trying to double OEC. To what degree are you concerned potentially we could be flooding the market and this becomes -- equipment could be flooding the market and this becomes an issue. Or do you think the appropriate level of equipment that's going into the market sort of like meets demand like the -- so I guess that was the spirit of the question and whether competitive dynamics are any different or more concerning versus what you've seen in other cycles?

**Matthew Flannery** (Executives):
Yes, sure. So to the flooding supply, I mean, the industry has shown really good discipline on supply and demand and including the OEMs. So we feel good about that backdrop. More importantly, we feel really good about the demand going forward. So we're not overly concerned about that.
And as far as our ability to access, you see this year with the raised CapEx throughout the year, we've got real good relationships and flexibility with our partners, where we do feel we're able to react quickly and respond quickly to opportunities, but there's a lot of planning in that and a lot of forward-looking information that we're sharing with our partners to make sure we can do that effectively. So we do feel good about the supply and demand and our ability to participate appropriately in it.

**Operator** (Operator):
We'll go next now to Steven Fisher with UBS.

**Steven Fisher** (Analysts):
Great. My call dropped a little earlier, so I apologize if these have been addressed, but last year, in the fourth quarter, you had a couple of things that were specifically weighing on the margins in that quarter. And so the comps, I think, should be easier, and I guess, I'm just curious how you approached the expectations -- or setting the expectations for Q4 incremental margins or implied incremental margins in light of sort of easier comps on that from last year versus this year. I would think they should be better than what you saw in Q3, but it seems like there might be something else you're factoring in.

**William Grace** (Executives):
Yes. I mean, certainly, I won't rehash the dynamics we talked about a year ago, but I'd say the biggest thing we did call out was that repositioning a year ago, and the team has done a good job to some of my earlier points.
Steve, I'm getting the gist of your question is if you're trying to see what's implied at the midpoint of guidance on the fourth quarter. And we want to caution people against anchoring at the midpoint of our guidance. I mean, on the one hand, it's inevitable and anchors these conversations because it's an easy point to point to, but it's not without risk. So we've got a range. We feel very good about the momentum we're carrying throughout the year into the fourth quarter, the fundamental performance we would not expect to deviate.
And I'd just remind people the sensitivity of that calculation, right? I mean, if you think about a 1% variance in EBITDA or you hold everything else constant, that equates to about a 50 basis point swing in the implied margin year-on-year. And so without obviously decomposing all the factors that influence a quarter because it varies quarter-to-quarter, I'll just say we feel really good about the year-to-date execution, we feel really good about our expectations for the fourth quarter. Where we end up, time will tell. But if you're inferring that something's changed or anything along those lines, there's -- nothing has.

**Steven Fisher** (Analysts):
Okay. That's helpful. And then in terms of cold starts, I think, if not -- all of your cold starts have been in Specialty and certainly, it seems like the vast majority of them. I'm just curious, as we think about an increasing mix of large projects going forward, just curious, geographically, where those large projects are setting up, is there an opportunity for you to do more Gen Rent branches? Or are they in places where you've got adequate coverage already within your existing footprint?

**Matthew Flannery** (Executives):
Typically, we have adequate coverage where they are. But if there happens to be a large project in a really remote area, more times than not, we're able to get an on-site to service it that way. If we think it's a market that's going to continue to grow outside of the major project, then we certainly have no hesitation to put the cold start in there. But our coverage is pretty good, especially here in the U.S. and in Canada. So we feel we rarely need to add a store in Gen Rent just for a major project.

**Operator** (Operator):
We'll go next now to Sabahat Khan with RBC Capital Markets.

**Sabahat Khan** (Analysts):
I think last quarter, you shared some comments on sort of underlying margins ex some of the moving pieces. And I guess, with higher ancillary and re-rent mix, maybe if you could just share some thoughts on how underlying margins trended this quarter as well?

**William Grace** (Executives):
Yes. Thanks for the question. The dynamics we had to manage through in the third quarter were not dissimilar to what we managed through in the second quarter, whether it's that impact from the outgrowth of ancillary and re-rent, I would say, the headwind, which obviously you saw us offset, was similar. And even within fuel, right? We talked about the headwind we absorbed in fuel last quarter. It was pretty similar third quarter over second quarter.
So not a lot of change there, shouldn't surprise people. But obviously, what you saw was our ability to again leverage that growth, the composition of growth and just very good cost execution across the company.

**Sabahat Khan** (Analysts):
Great. And then as I think about '27, some of the costs or operational cost reductions you've been making, those likely help into next year. I guess, when you outlined some of the technology initiatives earlier this year, whether it's on the AI front and some of the other programs, do those become a material contributor to margins as we head into next year? Or are some of these technology programs that you're undertaking more longer-term contributors and maybe a bit less material? Should we start to think about them getting more material as you head into '27?

**Matthew Flannery** (Executives):
So as we get through the budget process, we'll probably get a little deeper into that. I think most of them are longer term and -- but there's certainly some productivity improvements in there. Some of them are less easily to input into a margin conversation, but just productivity of some of our human capital, I certainly think longer term, we should get productivity in the shops from some of the technology we're using and certainly free up some time for our managers to use more of their time to drive the business. So I think there's a range of opportunities probably more towards the long term, but we'll update appropriately as we learn.

**William Grace** (Executives):
And this isn't at all to take away from the opportunity. But just as a reminder, I mean, we've long embraced continual improvement. And so while a lot of the AI tools have a lot of potential and we're really excited, we view it as a continuation of what we've been driving internally to drive productivity for several decades.

**Operator** (Operator):
We'll go next now to Scott Schneeberger with Oppenheimer.

**Daniel Hultberg** (Analysts):
It's Daniel on for Scott. Could you please address the sustainability of the used sales margin expansion you've seen recently?

**William Grace** (Executives):
Sorry, which margin expansion?

**Daniel Hultberg** (Analysts):
Used sales?

**William Grace** (Executives):
Used Sales. Yes. Look, we've been very pleased. I'd say, overall, that market has performed as expected. We -- you rewind a year ago when we talked about we felt like 2025 was kind of the bottom innings of that normalization process. And we saw that progressively, if you think about how the first half of '25 played out versus second half. And obviously, we progressed through '26 pretty well. So it feels like the market is normalized. Certainly, it's a very deep market, plenty of demand. You can see that in our results.
In terms of the margins, I think we're back to kind of what we would say are normalized margins. And so I would not encourage people to think there's going to be a huge amount of variability there. The likelihood is we're kind of again back in this normalized market, but the good news is things have played out as we kind of expected them to.

**Daniel Hultberg** (Analysts):
Got it. And just to round off on EBITDA flow-through. I mean, you've done a great job with the efficiency this year. How do you think about EBITDA flow-through longer term? Any color there would be helpful.

**William Grace** (Executives):
Yes. So we've really tried to pivot this discussion away from flow-through because I think it almost simplifies things. And really, our goal is to drive margin expansion across the cycle and we feel like that's what we've done. Certainly, as we've talked about, in some periods of time, it's easier to do and easier to show and other times, it's more difficult or it gets clouded by dynamics, whether that's used, to kind of your earlier point, Daniel, or whether it's -- obviously, this outgrowth of ancillary and re-rent.
I would just say going forward, our focus is on driving profitable growth and then being as efficient as possible. And that obviously implies driving core margin expansion. And similar to what we talked about in '23 and '24 and '25, we're going to help people see what the underlying results look like as best as possible. But as we go forward, certainly, our goal again is going to be to drive strong margins and ultimately margin expansion is the goal.

**Operator** (Operator):
We'll go next now to Neil Tyler with Rothschild & Co.

**Neil Tyler** (Analysts):
Just one more for me, please. Coming back to the topic of inflation more broadly. Matt, I guess, you've talked about the various aspects in which that appears across your industry. Are there specific areas or verticals that you might want to call out where you're seeing customers come to you to solve their inflation problems since -- in ways that your model might be better able to absorb it? And if you could just talk a little bit about that as a theme?

**Matthew Flannery** (Executives):
Sure. We usually think about capital cost avoidance when we're thinking about rental versus owning. But to your point, those come at a cost. So I think the most important part is how can we help our customers drive efficiency. We believe fleet, right, technology and part of that and fleet is a great way for them to do that. So we make sure we provide that. And we do think rental is the better way. You could own fleet and get some productivity out of the usage, but we feel strongly that rental has proven to be the better way for them to do that. So I think it's a big part of our value proposition to continue to help customers drive efficiency to improve their margins and competitiveness in their markets.

**Neil Tyler** (Analysts):
And then the second question would be, obviously, you've talked confidently about your -- you feel good about demand and into '27 as well. Obviously, there are discussions ongoing as to sort of longevity of some of the cycles in end markets that you serve. Can you sort of talk a little bit more sort of longer term? It feels like the market is broadening out, the demand environment is broadening out, but how you would characterize your visibility compared to, say, 6, 12 months ago across the sort of indicators that you look at?

**Matthew Flannery** (Executives):
Yes. I would say we feel better than we did 6 to 12 months ago, certainly. You see that not only in the raised guidance, but in the activity that's going around in the industry. And the end markets we serve are very, very broad, even within non-res, and I know there's been a lot of talk underlying in that commentary, people are wondering how long data center is going to continue. Well, that sits in our non-res business. And even if you take data centers out, we've got strong double-digit growth within non-res. And then we think about infrastructure, power, LNG, even upstream oil and gas is doing well right now, but growing.
So those opportunities remain. And that's with a couple of end markets not being strong, like industrial manufacturing, we think, is a potential future opportunity for us. Residential, which then will drive more non-res work, right, is still down and downstream oil and gas. Petrochem overall on the downstream side, which is an area where we have a lot of run and maintain work, a lot of turnaround work that's just not getting done right now because those folks are busy as heck right now, as you could imagine. So we feel really good about the long-term view here and certainly more bullish than we did 6 to 12 months ago.

**William Grace** (Executives):
And the one thing I might add, Neil, is I think people know, we survey our customers regularly and they continue to feel very good about their own prospects. So this is something that Matt, Elizabeth and I have gotten a lot of questions on in the last, let's just say, 6-plus months given what's happened with energy pricing and inflation and what the market is discounting on rates and understandable concerns around whether it's the short end of the curve, the long end of the curve. Throughout all that volatility that markets have wrestled with, I would tell you, our customers have felt consistently positive, and that's certainly as of the most recent readings. So that also helps underpin our confidence in kind of what that outlook looks like.

**Operator** (Operator):
And ladies and gentlemen, that is all the time we have for questions this morning. Mr. Flannery, I'd like to turn things back to you, sir, for any closing comments.

**Matthew Flannery** (Executives):
Great. Thanks, operator. And once again, folks, we apologize for the tech disruption. But to everyone on the call, we appreciate your time. I'm glad you could join us and our Q3 investor deck has the latest updates. And as always, Elizabeth is available to answer your questions. So until we speak to you again in January, have a safe and happy holiday season, and have a great end of your year. Operator, you can now end the call.

**Operator** (Operator):
Thank you, Mr. Flannery. Thank you, Mr. Grace. Again, ladies and gentlemen, this does conclude United Rentals' Third Quarter Earnings Conference Call. We'd like to thank you all so much for joining us today and wish you all a great afternoon. Goodbye.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### URI_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜CFO｜guidance：CFO 公布全年營收財測上調 5 億美元至 175–178 億（原話："range of $17.5 billion to $17.8 billion"）
- 2026-07-23｜CFO｜guidance：CFO 說明調整後 EBITDA 財測上調 3 億並維持全年利潤率持平（原話："expectation to bring the revenue growth to the bottom"）
- 2026-07-23｜CFO｜guidance：總租賃 CapEx 財測上調 4.5 億，因需求更強（原話："we've increased our gross CapEx guidance by $450 million"）
- 2026-07-23｜CFO｜guidance：自由現金流財測維持 21.5–24.5 億，CapEx 增加由營運現金流增加抵銷（原話："we are reaffirming another year of strong free cash flow"）
- 2026-07-23｜CEO｜guidance：CEO 表示不給 2027 財測，但認為順風延續到明年（原話："We're not going to go as far as give '27 guidance"）
- 2026-07-23｜CEO｜guidance：CEO 說明 CapEx 季節節奏：新財測下 Q3 約引進 30–35%（原話："somewhere around 30% to 35% in Q3 -- balance in Q4,"）
- 2026-07-23｜CFO｜guidance：CFO 對下半年租賃營收成長不給落點，提醒看區間，主要變數為附屬與轉租，下次 10 月更新（原話："we would point people towards the range,"）
- 2026-07-23｜CEO｜guidance：CEO 說四月已有信心但通常不在四月上調，實際表現超出預期、專案管線更快更深（原話："The pipeline of projects moved faster and got deeper."）
- 2026-07-23｜CFO｜margin：CFO 拆解利潤率：報表口徑 +70bp，扣除出售鷹架業務利得後 -40bp（原話："Excluding both the gain on the sale of our scaffolding"）
- 2026-07-23｜CFO｜margin：CFO 再扣除附屬與轉租超額成長後，核心利潤率年增 40bp（原話："margins were up 40 basis points year-on-year, even"）
- 2026-07-23｜CFO｜margin：CFO 說附屬收入的燃料與運送成本轉嫁帶來營收但增量利潤有限（原話："brought limited incremental margin dollars."）
- 2026-07-23｜CFO｜margin：CFO 量化第二季自用燃料成本對利潤率的額外逆風（原話："20 or 30 basis points of additional headwind year-on-year"）
- 2026-07-23｜CFO｜margin：CFO 說明全年利潤率目標為持平（排除去年 H&E 影響）（原話："flat margins, excluding the impact of H&E last year."）
- 2026-07-23｜CFO｜margin：CFO 以去年對照量化運送成本：去年交貨成本增 20% 對租賃營收 6–7%，隱含約 1.15 億超額成本；今年 Q2 租賃營收 +12.7%、交貨 +11.7%（原話："rental revenue up 12.7%, delivery up 11.7%."）
- 2026-07-23｜CFO｜margin：CFO 說勞力、運送、維修三大核心成本今年皆領先預期曲線（原話："we're actually ahead of the curve on all 3."）
- 2026-07-23｜CFO｜margin：CFO 說第二季重組節省約 1,200 萬，已達年化速率；累計費用 5,100 萬，全年預期 5,500–6,500 萬（原話："benefit was on the order of about $12 million"）
- 2026-07-23｜CFO｜margin：CFO 稱附屬收入難以預測，Q3 燃料價格預期與 Q2 持平（原話："Our expectation is that fuel prices probably"）
- 2026-07-23｜CEO｜margin：CEO 說成本改善來自流程改變與執行，而非 CapEx 緩解重新調配成本（原話："is really more process change and execution"）
- 2026-07-23｜CEO｜customer：CEO 開場稱成長加速、客戶對大型專案保持樂觀（原話："Customers remain optimistic"）
- 2026-07-23｜CEO｜customer：CEO 說在地市場自一月以來已穩定，本地客戶約低個位數成長（原話："we are seeing stabilization with some very modest growth."）
- 2026-07-23｜CEO｜customer：CEO 確認半導體與電力（含資料中心）第二季雙雙加速（原話："Both of those have accelerated here in the second quarter."）
- 2026-07-23｜CEO｜customer：CEO 說電力垂直市場占營收逾一成（原話："in excess of 10% of our business"）
- 2026-07-23｜CEO｜customer：CEO 說石化與工業製造目前並未轉強，屬尚未啟動的上行空間；下游業者推遲歲修（原話："Industrial manufacturing is not really hot right now."）
- 2026-07-23｜CEO｜customer：CEO 說需求超預期主因是大型專案管線，涵蓋面廣（原話："projects across the board are just stronger and deeper"）
- 2026-07-23｜CEO｜product：專長業務租賃營收年增 25%，含 11 個新開據點（原話："exceptional rental revenue growth of 25% year-over-year"）
- 2026-07-23｜CFO｜product：CFO 說專長業務七大線皆雙位數成長，行動模組/儲存與 ROS 成長最快但規模最小（原話："I'll tell you, they're all in the double digits."）
- 2026-07-23｜CEO｜product：CEO 說電力產品十年來有機成長雙位數、據點已建置完成（原話："organically has been growing double digits for us"）
- 2026-07-23｜CFO｜product：CFO 說 AI 定價工具部分仍在試行，目前價格成功主因是產業紀律（原話："some things that we're working that are really in pilot"）
- 2026-07-23｜CFO｜competition：CFO 稱產業供需紀律是目前租金成功的最大因素（原話："that discipline that is critical."）
- 2026-07-23｜CEO｜competition：CEO 認為 URI 時間利用率高於產業，但產業整體也在提升（原話："the industry overall is driving higher time utilization"）
- 2026-07-23｜CEO｜competition：CEO 說產業整併會持續，連激進新開據點模式的業者也轉向併購（原話："The bigs will continue to get bigger."）
- 2026-07-23｜CEO｜risk：CEO 承認部分設備類別供給偏緊，額外 10 億美元設備買不到（原話："we wouldn't be able to get it."）
- 2026-07-23｜CEO｜risk：CEO 說若本地市場同時強勁，疊加大型專案需求將有供給挑戰（原話："it would be challenging today."）
- 2026-07-23｜CFO｜risk：CFO 指出運送重新調配成本仍在處理中，下半年須持續維持（原話："We've got to keep it up, right?"）
- 2026-07-23｜CFO｜capital_allocation：CFO 說上半年回饋股東 9.98 億，含回購 7.5 億與股利 2.48 億（原話："$750 million through repurchases and $248 million"）
- 2026-07-23｜CFO｜capital_allocation：CFO 重申今年回購 15 億，加股利約回饋 20 億（原話："intend to repurchase $1.5 billion of shares in 2026"）
- 2026-07-23｜CFO｜capital_allocation：S&P 將展望調為正向，12 個月內有機會升投資等級（原話："raising our credit outlook to positive from stable"）
- 2026-07-23｜CFO｜capital_allocation：CFO 說移向投資等級不影響資本配置與併購策略，內部政策原先使其留在高收益級（原話："internal financial policy that kept us in the high-yield"）
- 2026-07-23｜CEO｜capital_allocation：CEO 說併購管線穩健，成長 90% 以上為有機（原話："the pipeline continues to be robust."）
- 2026-07-23｜CFO｜capital_allocation：CFO 說併購以現金報酬率框架呈現，因收購會計可能短期稀釋 ROIC（原話："And that's why we frame the deals really as"）
- 2026-07-23｜CEO｜commitment：CEO 稱團隊靠艦隊生產力「贏得」額外 CapEx，且租金需抵銷通膨（原話："they earned this extra CapEx by"）
- 2026-07-23｜CEO｜commitment：CEO 表示預期租金與各項艦隊生產力組成皆為正向（原話："But rate is a good guy, and we expect it to"）
- 2026-07-23｜CEO｜commitment：CEO 表示明年仍會成長，但幅度與 CapEx 待規劃；預期多賣一些二手設備（原話："expect next year to certainly be another year of growth"）
- 2026-07-23｜CFO｜commitment：CFO 說公司不會迴避客戶要求的小型附屬服務，並會向市場說明對利潤率的影響（原話："So we're not going to shy away from them."）

### 問答異常語氣（迴避／改口／保留）
- URI_Q2_2026_Earnings_Call_20260723.md｜問：Rob Wertheimer / Ken Newman：租金（rate）是否已到位、後半年是否改善｜答法：管理層一貫不給租金數字，只說「rate is a good guy」並預期持續，未回答是否到位
- URI_Q2_2026_Earnings_Call_20260723.md｜問：David Raso：Q2 剔除利得後利潤率 -40bp 到下半年隱含 +10–20bp 的擺動因素｜答法：CFO 未列出擺動因素，改談上半年底層 +10bp 與「季度間正常變動」，並重述全年持平目標
- URI_Q2_2026_Earnings_Call_20260723.md｜問：Steve Fisher：CapEx 增加能否減輕重新調配成本、何時不必再提｜答法：CEO 先否認目前有特別強調，並否定 CapEx 為正向吸收原因；CFO 稱難以量化
- URI_Q2_2026_Earnings_Call_20260723.md｜問：Jamie Cook：CapEx 增加中 gen rent 與 specialty 的占比｜答法：CEO 拒絕拆分，僅稱可假設專長業務占不少
- URI_Q2_2026_Earnings_Call_20260723.md｜問：Tami Zakaria：下半年租賃營收成長是否放緩｜答法：CFO 不給具體預期，要求看區間，並稱要到 10 月才有更新

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
{"date":"20260723","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"結構性租賃滲透 + specialty + 資料中心 capex 使 URI 成長跑贏廣義建築循環的收縮","columns":{"2Y 驗證點":"FY27 rental rev 續正成長；general rentals 不轉負","5Y 驗證點":"租賃滲透率 >62%；specialty 佔比續升","10Y 驗證點":"租賃取代擁有成主流、URI #1 地位穩固","具體數字門檻 / Sourced Floor":"Sourced：ARA 滲透率 59.5%（連 5 年創高）；specialty 20.2% CAGR；Q2 rental rev +12.7%；資料中心 capex >$1T 2026（Dell'Oro）狀態：兌現中但集中度風險升（靠資料中心＋份額，非廣義循環）","漂移觸發":"general rentals 連兩季轉負 → 削弱；資料中心 capex 增速放緩 + 廣義續縮 → 反轉"}},{"id":"H2","text":"URI 維持 #1 規模與定價紀律，Herc 併 H&E 後不侵蝕其 specialty/mega-project 領先","columns":{"2Y 驗證點":"URI 規模仍 ~4x Herc；specialty margin 穩定","5Y 驗證點":"市佔續升；賽局理性（無破壞性降價）","10Y 驗證點":"整併持續、前三大集中度升","具體數字門檻 / Sourced Floor":"Sourced：URI FY26 guide $17.5–17.8B vs Herc $4.275–4.4B（~4x）；但 Herc specialty locations +25%、EBITDA margin ~47% 已與 URI 46.6% 齊平（Herc Q1'26）狀態：規模領先穩，但 specialty 同場競爭升溫","漂移觸發":"specialty 段 margin 連兩季"}},{"id":"H3","text":"結構性再評價可維持（EV/EBITDA ~10x 非循環頂假象，而是租賃滲透 + 資本回報支撐的新常態）","columns":{"2Y 驗證點":"循環未反轉時倍數守住 ~9–10x","5Y 驗證點":"與 ACN/優質工業複利中位收斂","10Y 驗證點":"市場永久接受 URI 為結構複利而非純循環","具體數字門檻 / Sourced Floor":"Sourced：Fwd PE 20x vs 5Y 均 13.5x；EV/EBITDA ~10x vs 10Y 中位 7x（+40%）；P/B 7.2x vs 均 4.6x狀態：溢價已建立但脆弱（若循環反轉，歷史顯示回 6–8x EV/EBITDA）","漂移觸發":"循環反轉 + EV/EBITDA 回落至"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"廣義非住宅建築收縮惡化成衰退 + 資料中心 capex 增速放緩，兩條腿同時斷（peak-cycle 盈餘正常化 + de-rate）","columns":{"對應假設":"H1／H3","時間尺度":"🔥 中期（4–6 季，但循環反轉可快）","監測指標":"ABI（連 40 月","警戒閾值":"fleet productivity 轉負 + general rentals 轉負 → 循環反轉確認、減碼"}},{"id":"R2","text":"Rouse benchmark-pricing 反托拉斯 MDL 敗訴/禁令 → 全產業租賃定價權結構性壓縮（非 URI 規模可分散）","columns":{"對應假設":"H2／H3","時間尺度":"🐢 長期（2+ 年司法程序）","監測指標":"MDL 3152（N.D. Illinois）動議裁決；benchmark-pricing 是否被禁","警戒閾值":"MTD 被駁回進入實質審理 → 風險升；禁令 → §3.F 命中、清倉重評"}},{"id":"R3","text":"估值溢價回吐：市場把 URI 從「20x 結構複利」重估回「13x 循環股」","columns":{"對應假設":"H3","時間尺度":"🔥 中期（估值隨循環轉）","監測指標":"EV/EBITDA vs 自身歷史；Fwd PE 分位","警戒閾值":"循環轉弱 + EV/EBITDA 回落"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔至 Fwd PE ≤ 15x（~$770）或 EV/EBITDA ≤ 8x；或 ABI 持穩 >50 + 廣義非住宅建築回正確認循環續行","irr_base_pct":6.7,"ev5y_pct":25.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.82,"ev5y_pct":25.0,"irr_base_pct":6.7,"max_dd_pct":-55.0,"bull_5y_price":1760.0,"bear_5y_price":704.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"回檔至 Fwd PE ≤ 15x（~$770）或 EV/EBITDA ≤ 8x；或 ABI 持穩 >50 + 廣義非住宅建築回正確認循環續行","price_at_dd":1035.06,"archetype":"品質複利成長","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/URI_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
