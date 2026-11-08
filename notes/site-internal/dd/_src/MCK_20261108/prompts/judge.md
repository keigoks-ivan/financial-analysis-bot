你是 stock-analyst **v20 判斷 agent**，標的 MCK（20261108）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MCK","date":"2026-11-08","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":110957,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm"},"note":"新聞媒體稱營收低於共識（finanzen.net，未取得數字，待核）"},{"id":"f_kpi1_non_gaap_adjusted_operat","label":"Non-GAAP (adjusted) operating profit","value":1852,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm"},"note":"未取得"},{"id":"f_kpi2_non_gaap_operating_margi","label":"Non-GAAP operating margin（推算＝1,852÷110,957）","value":1.67,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（利益率為自行以公布數字推算）"},"note":"未取得"},{"id":"f_kpi3_gaap_operating_income","label":"GAAP operating income","value":1604,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm"},"note":"未取得"},{"id":"f_kpi4_gaap_operating_margin_1_","label":"GAAP operating margin（推算＝1,604÷110,957）","value":1.45,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm（推算）"},"note":"未取得"},{"id":"f_kpi5_free_cash_flow","label":"Free cash flow（單季）","value":2947,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm"},"note":"未取得"},{"id":"f_kpi6_adjusted_eps","label":"Adjusted EPS","value":11.68,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm"},"note":"媒體稱優於共識（finanzen.net，未取得數字，待核）"},{"id":"f_kpi7_guidance_fy2027_adjusted","label":"Guidance: FY2027 adjusted EPS（上修）","value":"45.60–46.40","period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm"},"note":"consensus_revision fy1 = 44.66（財報前快照，已落在新區間之下）"},{"id":"f_kpi8_operating_segment_revenu","label":"Operating segment revenue: Oncology & Multispecialty","value":14980,"period":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q2 FY2027（季末 2026-09-30，公告於 2026-11-04）","citation":"公司新聞稿（8-K Ex.99.1，即 investor.mckesson.com 發布之 Q2 FY27 press release）https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000279/mck_exhibit991x9302026.htm"},"note":"未取得"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-11-04","period":"2026-11-04","unit":"date","basis":"距今 3 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-11-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mck_gross_margin_pct","label":"MCK 毛利率","value":3.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mck_operating_margin_pct","label":"MCK 營業利益率","value":1.67,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mck_fcf_margin_pct","label":"MCK FCF 利潤率","value":1.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cah_gross_margin_pct","label":"CAH 毛利率","value":3.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cah_operating_margin_pct","label":"CAH 營業利益率","value":1.26,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cah_fcf_margin_pct","label":"CAH FCF 利潤率","value":1.9,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cor_gross_margin_pct","label":"COR 毛利率","value":4.12,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cor_operating_margin_pct","label":"COR 營業利益率","value":1.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cor_fcf_margin_pct","label":"COR FCF 利潤率","value":0.47,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_gross_margin_pct","label":"HSIC 毛利率","value":31.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.gross_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_operating_margin_pct","label":"HSIC 營業利益率","value":5.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.operating_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_hsic_fcf_margin_pct","label":"HSIC FCF 利潤率","value":3.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC.fcf_margin_pct","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":1060.84,"period":"2026-11-06（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":44.43,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":70.22,"period":"2026-11-06（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=False","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（44.66 → 44.66）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（50.63 → 50.63）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-11-07","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（57.72 → 57.72）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":44.66,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":50.63,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":57.72,"period":"2026-11-07","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.09,"period":"2026-08-13 → 2026-11-07","unit":"%","basis":"FY1 共識 EPS 44.62 → 44.66（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-11-07","citation":"DD_universe_EPS_estimates_20261107.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":27.36,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.29,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":0.3,"period":"2026-11-06（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-11-06（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-11-06（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-11-06（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":23.75,"period":"2026-11-07","unit":"x","basis":"分母＝FY1 EPS 44.66，分子＝快照價 1060.84","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-11-07"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.321,"period":"2026-11-08","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-11-08"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":4674.0,"period":"2026-11-08","unit":"USD m","basis":"yfinance 最新一季：總債務 11202.0、現金 6528.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":115.46,"period":"2026-11-08","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":127155.04,"period":"2026-11-08","unit":"USD m","basis":"市值 122481.04 ＋ 淨負債 4674.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":434899.73,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（14 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":464859.08,"period":"2026-11-08","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":0.29,"period":"2026-11-08","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-11-08"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-11-08","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 1060.84 / W52 860.18 / W104 767.33 / W250 562.73 / W250 13週斜率 2.24%"},{"id":"f_ma_w52","label":"52 週均線","value":860.18,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":767.33,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":562.73,"period":"2026-11-08","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.24,"period":"2026-11-08","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-11-08","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"10-K 指出主要對手為 Cencora 與 Cardinal Health；Oncology & Multispecialty 另與專科經銷商、GPO、專科藥局、腫瘤網絡競爭，Cencora、Cardinal 亦提供經銷＋GPO＋提供者服務組合。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"Our primary competitors in distribution, wholesaling, and logistics are Cencora, Inc. and Cardinal Health, Inc.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 風險因子：越來越多新競爭進入者在資料分析、機器學習、AI 等技術上比公司更有經驗。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"Additionally, some of our historical competitors and a growing number of new competitive entrants have more experience than we do in enabling technologies such as data analytics, machine learning, or AI.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"MCK FY2026 10-K：最大客戶 CVS 占營收約 24%、應收約 21%；前十大客戶占約 73%；與 CVS 的配銷合作已延至 2027 年 6 月。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"Sales to our largest customer, CVS Health Corporation (“CVS”), accounted for approximately 24% of our total consolidated revenues in fiscal 2026. In fiscal 2023, we extended our pharmaceutical distribution partnership with CVS to June 2027.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"10-K 風險因素：客戶可能減少採購或不續約，單一或多個大客戶減量、不續約可能對業務造成重大不利影響。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"Some of our customers from time to time reduce the amounts they purchase from us, do not renew their purchase contracts with us, renew their purchase contracts at less favorable terms, delay or default on their payments to us, or avoid payments to us through bankruptcy proceedings.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"+","claim":"McKesson 於 2026-10-01 宣布與 CVS 就藥品配銷協議延長至 2032 年 6 月達成原則性協議（尚非最終合約）；Cardinal Health 亦與 CVS 延長至 2032 年 6 月。","source":"Distribution Strategy: McKesson Extends CVS Pharmaceutical Distribution Agreement Through 2032","url":"https://distributionstrategy.com/2026/10/mckesson-extends-cvs-pharmaceutical-distribution-agreement-through-2032/","excerpt":null,"as_of":"2026-10-02","retrieved_at":"20261108","affects":["thesis.R","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2026 前十大客戶占營收約73%、占應收約43%；最大客戶CVS占營收約24%、占應收約21%；次兩大客戶各占11%與10%。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"Sales to our largest customer, CVS Health Corporation (“CVS”), accounted for approximately 24% of our total consolidated revenues in fiscal 2026. In fiscal 2023, we extended our pharmaceutical distribution partnership with CVS to June 2027. Sales to our next two largest customers accounted for 11% and 10% of total consolidated revenues in fiscal 2026.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"10-K 自述銷售與信用集中度顯著，單一大客戶重大違約、減量或流失可能對財務、營運與流動性造成重大不利影響；與CVS合約延至2027年6月。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"As a result, our sales and credit concentration is significant. We also have agreements with GPOs, each of which functions as a purchasing agent on behalf of member hospitals, pharmacies and other healthcare providers, as well as with government entities and agencies.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"最大客戶CVS 2026-06-30 長期債評等為投資等級（Fitch BBB、Moody's Baa3、S&P BBB）；2026年5月S&P展望由負面改為穩定；本次搜尋結果未見2026年降評。","source":"CVS Health Form 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0000064803/000006480326000098/cvs-20260630.htm","excerpt":"As of June 30, 2026, the Company's long-term debt was rated \"BBB\" by Fitch Ratings, Inc. (\"Fitch\"), \"Baa3\" by Moody's Ratings (\"Moody's\") and \"BBB\" by Standard & Poor's Financial Services LLC (\"S&P\").","as_of":"2026-06-30","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY27 adjusted EPS guidance raised to $44.20-$45.00 from $43.80-$44.60; GLP-1 distribution revenue ~$15B in Q1, up ~24% y/y; GLP-1 volumes expected to keep growing through FY27 with quarterly swings","source":"MarketBeat, McKesson Q1 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/mckesson-q1-earnings-call-highlights-2026-08-08/","excerpt":null,"as_of":"2026-08-08","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY27 segment revenue guide: North American Pharmaceutical +4-8%, Oncology & Multispecialty +14.5-18.5%, Prescription Technology Solutions +2.5-6.5%, Med-Surg +1-6%","source":"Quartr / Zacks summaries of McKesson Q1 FY2027","url":"https://www.zacks.com/stock/news/2979315/mckesson-raises-fy27-guidance-as-oncology-and-glp-1-growth-accelerate","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"IRA drug price cuts pricing pressure expected to persist through FY27","source":"Chartmill/Zacks, Retain McKesson Stock","url":"https://www.chartmill.com/news/external/65091/here-s-why-you-should-retain-mckesson-stock-in-your-portfolio-for-now","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"10-K FY2026 稱 FTC 與 HHS 2024 年就批發商／GPO 對學名藥短缺影響徵求公開意見，之後無進一步行動；並稱醫療業反壟斷執法仍是 FTC/DOJ 重點，策略交易可能需競爭主管機關審查。","source":"SEC EDGAR 10-K FY2026 Item 1","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"the Federal Trade Commission (“FTC”) and HHS issued a request for public comment in 2024 on how the practices of pharmaceutical wholesalers and group purchasing organizations impact generic drug shortages. Various industry stakeholders responded to this request, but no further action has been taken by the FTC or HHS.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2026 10-K Item 3 僅指向附註 17，未在該節單獨列出針對 MCK 的新反壟斷調查；MCK 反而是反壟斷和解金的受益方（FY2026 $23M、FY2025 $444M）。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"Gross profit for the years ended March 31, 2026 and 2025 included gains of $23 million and $444 million, respectively, representing our share of antitrust legal settlements.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"McKesson FY2026 10-K 風險因子列明政府行動（含貿易制裁、關稅與其他貿易限制）可造成供應中斷，且替代貨源不一定完全成功，可能面臨延遲或較高採購成本；並稱貿易環境仍高度動態且不確定。","source":"SEC EDGAR 10-K FY2026 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"Supply disruptions also arise from other factors beyond our control, such as product rationalization; government actions or policies (including trade sanctions, tariffs and other trade restrictions, as well as the requisition, diversion, or allocation of inventory)","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"10-K 指出海外業務約占合併營收 4%（FY2026 與 FY2025 各約 4%），並參照風險因子中的貿易與關稅風險。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"Our foreign operations represented approximately 4% of our consolidated revenues in each of fiscal 2026 and fiscal 2025, respectively.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"報導稱學名藥分階段關稅政策可能對三大美國藥品經銷商產生重大影響（McKesson 為其一屬搜尋結果推論，來源是否明指待核）。","source":"FreightWaves","url":"https://freightwaves.com/news/trumps-tariff-on-drugs-targets-one-of-the-worlds-most-globalized-supply-chains","excerpt":"McKesson Largest pharmaceutical distributor and wholesaler Cardinal Health National pharmaceutical distributor serving pharmacies and hospitals Cencora (formerly AmerisourceBergen) Global pharmaceutical wholesaler and distribution company Three companies dominate U.S. drug distribution Every imported generic drug ultimately moves through a remarkably","as_of":"2026-07-22","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"Section 232 專利藥及 API 關稅：預設 100%，歐盟／日本／韓國／瑞士 15%，學名藥原則上排除，2026-07-31 起部分公司適用。","source":"Mallory Group","url":"https://www.mallorygroup.com/blog-posts/100-duties-two-deadlines-section-232-pharmaceutical-tariffs-take-effect-july-31-2026","excerpt":"Tariffs Take Effect July 31, 2026 Executive Summary Starting July 31, 2026, imports of patented drugs and their active ingredients from the 17 companies named in Annex III face Section 232 tariffs of up to 100%. Every other importer’s date is September 29, 2026. Onshoring plans, MFN pricing deals, and trade agreements can cut the rate, sometimes to zero. Generics, biosimilars, and","as_of":"2026-07-31","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"MCK FY2024 10-K 風險因素列舉供應中斷成因，含供應商財務困難、天災、內亂或戰爭、流行病；曾因供應商無法交貨受影響（搜尋摘要轉述，未讀原頁）","source":"McKesson Form 10-K FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765324000035/mck-20240331.htm","excerpt":null,"as_of":"2024-05-01","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"產業層級：美國學名藥 API 設施逾 92% 在海外（主要印度、中國、義大利）；MCK 為連接印中製造商與美國通路的三大經銷商之一；學名藥關稅報導計畫 2028 起（尚非定案）。未見 MCK 自身對關稅或地緣曝險的揭露（搜尋摘要轉述）","source":"FreightWaves / PharmExec (2026-07-22)","url":"https://freightwaves.com/news/trumps-tariff-on-drugs-targets-one-of-the-worlds-most-globalized-supply-chains","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"MCK FY2026 10-K 風險因素之供應中斷與供應商集中描述","source":"McKesson Form 10-K FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000069/mck-20260331.htm","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27 Q2（截至2026-09-30）營收約$110.96B、年增8%；Oncology & Multispecialty 營收年增24%至$14.98B；Medical-Surgical 營收年增5%至$3.1B但調整後營業利益降10%（產品組合不利）；Prescription Technology Solutions 年增10%（二手彙整，未核原文）","source":"Panabee: McKesson Revenue Grows 8% to $111 Billion as Specialty Segments Expand","url":"https://www.panabee.com/news/mckesson-earnings-q2-2027","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FY27 Q2 官方10-Q：Oncology & Multispecialty 營收增$2.9B或24%","source":"McKesson Form 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000281/mck-20260930.htm","excerpt":"Oncology & Multispecialty Three Months Ended September 30, 2026 vs. 2025 Oncology & Multispecialty revenues for the three months ended September 30, 2026 increased $2.9 billion or 24% compared to the same prior year period primarily driven by higher specialty pharmaceutical sales in","as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"WAC下降部分抵銷處方量成長；公司預期FY27定價逆風延續","source":"McKesson Form 10-Q (period 2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0000927653/000092765326000281/mck-20260930.htm","excerpt":null,"as_of":"2026-11-05","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因素揭露：競爭對手包含製造商直銷、第三方物流與大型付款方，客戶或製造商可能自建供應管理能力取代 MCK 服務；也可能面對更快採用新興技術的公司。","source":"SEC EDGAR 10-K FY2026 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"In addition, our businesses face competition from various other service providers and from pharmaceutical and other healthcare manufacturers as well as other potential customers, which may from time to time decide to develop, for their own internal needs, supply management capabilities that might otherwise be provided by our businesses. We also may face competition from companies that move faster to adopt emerging technologies.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"第三方分析稱製造商直銷模式是中期較可信的威脅，AI 降低藥廠自建專科藥 hub 服務的營運負擔；Prescription Technology Solutions 為最可能被 AI 顛覆的部門（低可信度來源）。","source":"pitchgrade: mckesson ai margin pressure","url":"https://pitchgrade.com/research/mckesson-ai-margin-pressure","excerpt":"This analysis assigns McKesson an AI Margin Pressure Score of 3/10, placing it firmly in the protected category. The primary risk is slow and structural, not sudden. Business Through an AI Lens McKesson's business can be decomposed into three segments: US Pharmaceutical (the bulk drug distribution engine), Prescription Technology Solutions (RxTS, software and services for pharmacy","as_of":"2026-02-13","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2026 10-K：McKesson 宣布將 Medical-Surgical Solutions 分拆為獨立公司，並於 2026-04-20 與 Apollo 基金簽約，以約 $12.5 億可轉換特別股取得該部門約 13% 少數股權，待監管核准。","source":"SEC EDGAR 10-K FY2026 Item 7 MD&A","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"During fiscal 2026, we announced our intention to separate this segment into an independent company. As a part of the separation strategy, on April 20, 2026, we announced a definitive agreement under which funds managed by affiliates of Apollo Global Management, Inc. (“Apollo Funds”) will acquire approximately 13% minority ownership interest in our Medical‑Surgical Solutions segment through an investment of approximately $1.25 billion in the segment’s convertible preferred equity.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"10-K 列示 Oncology & Multispecialty 部門服務包含 direct to patient pharmacy 能力與 InspiroGene 細胞與基因治療服務；競爭段亦列出製造商直接配送（manufacturers engaged in direct distribution）為競爭者之一。","source":"SEC EDGAR 10-K FY2026 Item 1 Business","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"we face strong competition from international, national, regional, and local full-line, short-line, and specialty distributors; service merchandisers; self-warehousing chain drugstores; manufacturers engaged in direct distribution; third-party logistics companies; and large payer organizations.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"產業文章稱 2026 年中品牌平台處方占比上升，顯示直接面向病患通路遷移（廠商視角），未量化對批發商影響。","source":"Pharmaceutical Commerce, Mid-year check-in: how direct-to-patient momentum is accelerating","url":"https://www.pharmaceuticalcommerce.com/view/mid-year-check-in-how-direct-to-patient-momentum-is-accelerating","excerpt":"Check-In: How Direct-to-Patient Momentum Is Accelerating Author(s)Chip Parkinson, Stephen Appezzato Key Takeaways A compressed 150-day period saw policy and market shifts that outpaced typical formulary-driven timelines and catalyzed manufacturer adoption of direct-to-patient infrastructure. Rising prescription share routed through brand platforms indicates measurable channel migration, with","as_of":"2026-07-29","retrieved_at":"20261108","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"McKesson 公布 FY2027 Q2（2026-11-04）：調整後 EPS 11.68 美元，高於市場預期 10.75；FY2027 調整後 EPS 指引由 44.20–45.00 上調至 45.60–46.40（年增 17–19%），營收成長展望上調至 6–10%。","source":"finviz: McKesson Reports Fiscal 2027 Second Quarter Results and Raises Full Year Adjusted EPS Guidance","url":"https://finviz.com/news/416008/mckesson-reports-fiscal-2027-second-quarter-results-and-raises-full-year-adjusted-eps-guidance","excerpt":null,"as_of":"2026-11-04","retrieved_at":"20261108","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價共識分布依來源與日期而異：MarketBeat（2026-06-22）共識 960.53、高 1,085、低 812；FN2 頁面（2026-07）共識約 999、中位 1,010，含 UBS 1,200（2026-10-16）、Mizuho 1,020（2026-10-20）。","source":"MarketBeat／FN2 aggregators（經搜尋摘要）","url":"https://fn2.ai/earnings/mck/analysts","excerpt":null,"as_of":"2026-10-20","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"MarketBeat 共識目標價 960.53、高 1,085、低 812","source":"MarketBeat","url":"https://www.marketbeat.com/stocks/NYSE/MCK/sustainability/","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261108","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"搜尋結果顯示 McKesson 於 2026-08-25 宣布以約 22.5 億美元收購 Precision Medicine Group（臨床研究與生技商業化服務）；後續 8-K 稱已完成。摘要未提供可逐字複製原文。","source":"WebSearch 結果：wmbdradio 轉載（Reuters 稿）「McKesson to buy Precision Medicine Group in about $2.25 billion deal」","url":"https://wmbdradio.com/2026/08/25/mckesson-to-buy-precision-medicine-group-in-about-2-25-billion-deal/","excerpt":null,"as_of":"2026-08-25","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"近12個月 8-K 清單含重大項目者 3 份，皆為 Item 1.01／1.02／2.03（信貸協議，2026-04-06、04-28、06-12），無 Item 4.02（重編）。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000927653&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"FY2026 10-K 揭露 McKesson 仍為數百件鴉片類私人原告案件被告，並有 Omni Healthcare qui tam（False Claims Act）案。","source":"SEC EDGAR 10-K FY2026 Item 8 Note 17","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"The Company has also been a defendant in hundreds of opioid-related cases brought in the U.S. by private plaintiffs, such as hospitals, health and welfare funds, third-party payors, and individuals.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"FDA 執法紀錄顯示 McKesson 為 UDENYCA 預充填針劑 Class I 藥品召回（D-0353-2026）的召回廠，2026-01-16 啟動，116 箱，原因為儲存不當。摘要未提供可逐字複製原文。","source":"FDA recall D-0353-2026（ai-analytics.org 彙整）","url":"https://api.ai-analytics.org/recall/D-0353-2026","excerpt":null,"as_of":"2026-01-16","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-08-25 宣布以約 22.5 億美元收購 Precision Medicine Group，8-K 稱已完成。","source":"WebSearch：wmbdradio 轉載 Reuters","url":"https://wmbdradio.com/2026/08/25/mckesson-to-buy-precision-medicine-group-in-about-2-25-billion-deal/","excerpt":null,"as_of":"2026-08-25","retrieved_at":"20261108","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"10-K 揭露仍有數百件鴉片類私人原告訴訟；與其他兩家經銷商已與急性照護醫院及部分第三方付款人達成集體和解。搜尋未見近12個月新的證券集體訴訟（2018 年案已於 2022 年達成保險全額涵蓋之和解原則）。","source":"SEC EDGAR 10-K FY2026 Item 8","url":"https://www.sec.gov/Archives/edgar/data/927653/000092765326000069/mck-20260331.htm","excerpt":"The Company and two other national distributors reached class-action settlements with representatives of nationwide groups of acute care hospitals and certain third-party payors.","as_of":"2026-05-08","retrieved_at":"20261108","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"McKesson 為 UDENYCA Class I 召回（D-0353-2026）召回廠，2026-01-16 啟動，116 箱，儲存不當。查無 2026 年新警告信（前次為 2019 DSCSA、2024 年針筒相關）。","source":"FDA recall D-0353-2026（ai-analytics.org 彙整）","url":"https://api.ai-analytics.org/recall/D-0353-2026","excerpt":null,"as_of":"2026-01-16","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近12個月 8-K 清單無 Item 4.02（非可信賴之財報／重編）；搜尋只見 1999–2004 HBOC 舊案，SEC 對公司調查已於 2002 終止。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000927653&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-11-08 至 2026-11-08 共 13 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-11-08","retrieved_at":"20261108","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"MCK","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":3.67,"operating_margin_pct":1.67,"fcf_margin_pct":1.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MCK","as_of":"TTM ending 2026-09-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CAH","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":3.9,"operating_margin_pct":1.26,"fcf_margin_pct":1.9,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CAH","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"COR","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":4.12,"operating_margin_pct":1.44,"fcf_margin_pct":0.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.COR","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"HSIC","period":"TTM ending 2026-09-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":31.59,"operating_margin_pct":5.79,"fcf_margin_pct":3.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HSIC","as_of":"TTM ending 2026-09-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"MCK"},"financial_history":{"ticker":"MCK","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-03-31","revenue":276711000000.0,"revenue_yoy_pct":null,"gross_margin_pct":4.47,"operating_margin_pct":1.66,"net_income":3560000000.0,"diluted_eps":25.03,"free_cash_flow":4601000000.0,"fcf_margin_pct":1.66,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-03-31","revenue":308951000000.0,"revenue_yoy_pct":11.65,"gross_margin_pct":4.15,"operating_margin_pct":1.35,"net_income":3002000000.0,"diluted_eps":22.39,"free_cash_flow":3627000000.0,"fcf_margin_pct":1.17,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-03-31","revenue":359051000000.0,"revenue_yoy_pct":16.22,"gross_margin_pct":3.71,"operating_margin_pct":1.34,"net_income":3295000000.0,"diluted_eps":25.72,"free_cash_flow":5226000000.0,"fcf_margin_pct":1.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-03-31","revenue":403430000000.0,"revenue_yoy_pct":12.36,"gross_margin_pct":3.61,"operating_margin_pct":1.6,"net_income":4762000000.0,"diluted_eps":38.38,"free_cash_flow":5410000000.0,"fcf_margin_pct":1.34,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-03-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MCK/MCK_Q2_2027_Earnings_Call_20261104.md）

# Q2 2027 Earnings Call
**McKesson Corporation** | Earnings Calls | 2026-11-04

**Operator** (Operator):
Welcome to McKesson's Second Quarter Fiscal 2027 Earnings Conference Call. Please be advised that today's conference is being recorded. At this time, I would like to turn the call over to Paula Adkison, SVP of Corporate Finance and Investor Relations. Please go ahead.

**Paula Adkison** (Executives):
Thank you, operator. Good afternoon, and welcome, everyone, to McKesson's Second Quarter Fiscal 2027 Earnings Call. Today, I'm joined by Brian Tyler, our Chair and Chief Executive Officer; and Kenny Cheung, our Chief Financial Officer. Brian will lead off, followed by Kenny, and then we will move to a question-and-answer session.
Today's discussion will include forward-looking statements such as forecasts about McKesson's operations and future results. Please refer to the cautionary statements in today's earnings release and presentation slides available on our website at investor.mckesson.com and to the Risk Factors section of our most recent annual and periodic SEC filings for additional information concerning risk factors that could cause our actual results to materially differ from those in our forward-looking statements.
Information about non-GAAP financial measures that we will discuss during this webcast, including a reconciliation of those measures to GAAP results, can be found in today's earnings release and presentation slides. The presentation slides also include a summary of our results for the quarter and guidance assumptions.
With that, let me turn it over to Brian.

**Brian Tyler** (Executives):
Good afternoon, everyone. Thank you for joining our call. Today, we reported another strong quarter, reflecting continued momentum across our business and disciplined execution against our strategic priorities. Second quarter revenues increased 8% with growth across all segments, while adjusted earnings per diluted share increased 18% year-over-year. These results demonstrate the strength and resilience of McKesson's operating model, the momentum across our diversified health care platform and our continued focus on delivering sustainable long-term value for our customers and partners, and importantly, for our shareholders.
As a result of our strong performance and our confidence in the outlook for our business, we are raising our fiscal 2027 adjusted earnings per diluted share guidance to $45.60 to $46.40 from the previous range of $44.20 to $45. Our results continue to demonstrate the benefits of our strategic focus, differentiated capabilities and disciplined capital deployment. Across the enterprise, we remain focused on advancing our mission of improving health outcomes for all while executing against the strategic priorities that we believe will drive long-term sustainable growth.
Now let's discuss how we're translating these priorities into actions across the enterprise. I'll start with our people and culture, which remain foundational to everything we do. We continue to invest in experiences and programs that strengthen our culture and support engagement, development and well-being.
Recently, we launched Family Forward, a new employee resource group that fosters connection and supports employees with caregiving responsibilities at every stage of life. We now have 12 employee-led resource groups across the company, and I am proud of how these groups enrich our culture and advance inclusion for all members of Team McKesson. 
Our annual impact report published in July highlights additional examples of the progress we're making to advance health outcomes by supporting our communities, developing our people and enabling our partners to improve care for patients. Building on a strong commitment to our mission and purpose, we continue to accelerate our enterprise strategy with a focus on strengthening our North American distribution business and advancing our growth platforms in oncology, multi-specialty and biopharma services. During the quarter, we were pleased to announce a strategic transaction that directly supports these priorities, our acquisition of Precision Medicine Group, which we closed this week. We're pleased to welcome PMG to McKesson as we advance our shared commitment to accelerating innovation and improving patient access to care.  
Expanding access to clinical trials is an important element of our oncology strategy, connecting innovation in drug development with community-based practices where patients receive care. In 2022, we established our joint venture with Sarah Cannon Research Institute, bringing together the US Oncology Network's provider reach and practice management expertise with SCRI's research infrastructure and clinical trial expertise to support these practices. Precision Medicine Group builds on this foundation, adding complementary clinical research expertise in oncology, rare and orphan diseases, and cell and gene therapies. Its global footprint and experience conducting late-stage clinical trials broaden our ability to support clinical development and expand patient access to innovative therapies.
The acquisition also advances our biopharma services strategy. Precision Medicine Group's market access and commercialization services complement our existing access and affordability solutions, broadening the support we can provide to biopharma partners as they bring their therapies to market.
In addition, last month, we signed a definitive agreement to make a strategic investment in Option Care Health, the nation's largest independent provider of home and alternate site infusion services. As specialty therapies grow in importance and complexity, this transaction reflects our conviction that care will increasingly be delivered in lower-cost community settings at or closer to home. McKesson knows this shift well. For over 25 years, we have supported the US Oncology Network and over 3,400 providers in delivering connected high-quality care in the community.
Option Care Health's clinical model and national infusion footprint across home and ambulatory sites are well aligned with these priorities. As a strategic investor, we look forward to bringing our specialty expertise to help broaden access to complex therapies and to support its continued growth. And we're pleased to partner with CD&R, which brings a strong track record of supporting companies and creating long-term value. CD&R will own a majority interest in Option Care Health at closing. The transaction is subject to customary closing conditions, including approval by Option Care Health stockholders and the receipt of required regulatory approvals.
In our Oncology & Multispecialty platform, we are encouraged by strong market trends, supported by drug innovation and stable utilization. As new therapies come to market, our deep expertise in specialty distribution and specialty pharmacy, together with our strong connections across community-based care, position us well to enable access to these medications.
Within the oncology platform, we continue to reinforce our value to community-based providers by bringing together complementary capabilities, which include community-based practice management experience, clinical research expertise and data-enabled capabilities. As we welcome Precision Medicine Group, we're excited to build on this foundation and accelerate our strategy.
Within our retina and ophthalmology platform, we welcome Spectrum Vision Partners and its over 150 providers to the PRISM Vision Group, further expanding its footprint. This is another meaningful addition to our platform. We're encouraged by its continued strong performance, which demonstrates its compelling value proposition to providers and their patients. Across oncology and other specialty areas, our distribution capabilities, data-enabled insights, clinical expertise and experience supporting providers allow us to create value for customers and improve patient access to care.
Within our biopharma services platform, we continue to see strong demand for solutions that improve medication access and affordability. As therapeutic innovation accelerates and the treatment landscape becomes more complex, our differentiated solutions are helping translate that innovation into meaningful access for patients. Our platform connects providers, pharmacies, payers and manufacturers through technology that's embedded in prescribing and dispensing workflows.
We continue to expand our payer network, which now includes payers that represent 96% of U.S. prescription volume. This connectivity enables us to simplify administrative processes and address financial barriers at scale, helping patients start and stay on therapy while supporting biopharma partners across their product life cycles.
The momentum across our biopharma services platforms continues to be broad-based. During the quarter, we added 67 new programs across 58 unique brands, representing a diversified portfolio of therapeutic areas in both access and affordability. We expanded connectivity with providers, with more of them exploring our automated solutions, including our recently introduced medical prior authorization capabilities. We also saw growth in services that provide dedicated reimbursement specialists to help providers navigate insurance coverage and reimbursement challenges, reinforcing the value of hands-on expertise alongside our automated solutions.
Looking ahead, we remain focused on leveraging technology and automation to enhance the functionality of our solutions and streamline workflows. By simplifying routine processes and complementing them with specialized expertise where greater support is needed, we can address a broad range of access and affordability barriers and strengthen the value we deliver to biopharma partners, providers and patients.  
Let's turn to North American distribution. Our pharmaceutical distribution business continues to perform well, supported by stable market fundamentals, operational excellence and our differentiated customer value proposition. Recently, we announced an extension of our pharmaceutical distribution relationship with CVS Health. This agreement reflects the strength of our long-standing partnership of more than 25 years, the value of our distribution capabilities and our ability to support customers at scale with reliability, efficiency and service excellence. We value our relationship with customers across the health care ecosystem and remain focused on supporting their growth through consistent execution and the highest levels of service.
Across this segment, we continue to see strong momentum, reflecting our unwavering commitment to customers, the consistent delivery of high-quality service and a disciplined focus on operational excellence. This performance enables us to reinvest in the business, including our distribution network, supply chain capabilities and technology infrastructure, which further strengthen the reliability, efficiency and scale of our platform and position us to deliver sustainable long-term growth.
The strength of our business and our diversified capabilities position us well to drive continued growth amid evolving industry trends and a dynamic policy environment. We are committed to working closely with policymakers to advance thoughtful reforms that support patients and providers, expand access to care and improve health outcomes.
In closing, our strong second quarter results build on a strong record of execution and growth. We're pleased with the momentum of the underlying business, reinforcing our commitment to our strategic priorities. The Precision Medicine Group acquisition and our proposed investment in Option Care Health represent significant progress in expanding our capabilities and investing in areas of compelling long-term opportunity. Looking ahead, we're confident in our ability to deliver sustainable growth and long-term shareholder value.
With that, let me turn it over to Kenny.

**Kenny Cheung** (Executives):
Thank you, Brian, and good afternoon, everyone. We delivered a strong second quarter, supported by broad-based growth across the enterprise. This quarter's performance builds on the momentum from last quarter, resulting in a strong first half of fiscal 2027 and reinforcing our confidence in the opportunities ahead.
Before I turn to our adjusted results, I want to highlight the 2 important transactions we announced recently. As Brian mentioned in his opening remarks, we are pleased to have completed the acquisition of Precision Medicine Group for approximately $2.25 billion. The business will report within our Oncology & Multispecialty segment, further expanding the breadth of solutions we provide across our oncology, multispecialty and biopharma services. We expect the transaction to be accretive and reinforce our long-term growth profile.
We estimate the acquisition will contribute approximately $0.10 to $0.20 of adjusted earnings per diluted share in fiscal '27, with contributions more heavily weighted towards the fourth quarter. By the end of year 3, we estimate accretion of approximately $1.60 to $1.80. We funded the transaction with cash, reflecting the strength and flexibility of our balance sheet.
Additionally, we announced that we have entered into a definitive agreement to invest approximately $1.4 billion for a 49% minority interest in Option Care Health. The transaction aligns with our strategy to expand access to innovative therapies and our commitment to advance care in lower-cost community settings. The transaction is expected to close during the first half of calendar year '27, subject to customary closing conditions, including approval by Option Care Health's shareholders and the receipt of required regulatory approvals. Our current outlook does not contemplate contributions from Option Care Health.
Together, these investments reinforce our disciplined approach for capital deployment. First, we prioritize growth opportunities that align with our strategy, complement our portfolio and meet our financial criteria for attractive returns and long-term value creation. Second, we remain committed to returning capital to shareholders through a combination of share repurchases and a growing dividend. Lastly, we maintain a strong balance sheet supported by robust free cash flow generation and liquidity. This enables us to continue investing in and growing the business. 
Unless otherwise noted, my comments today will refer to our adjusted results. Let me turn to our second quarter consolidated performance. Revenues increased 8% to $111 billion, with growth across all 4 operating segments. Growth was driven by higher prescription volumes in North American Pharmaceutical and continued strength in Oncology & Multispecialty. This was partially offset by lower contributions from branded pharmaceuticals and continued branded-to-generic conversions.
Gross profit increased 10% to $3.9 billion, driven by growth in North American Pharmaceutical, Oncology & Multispecialty and Prescription Technology Solutions. The increase reflects higher prescription volumes and continued strength in specialty as we leverage our scale and distribution capabilities. Operating expenses increased 8% to $2.1 billion, reflecting higher expenses to support growth across the business. We remain focused on driving productivity and strengthening our network while maintaining expense discipline and investing to enhance how we serve our customers and drive future growth.
We demonstrated strong operating leverage during the quarter, with operating expenses as a percentage of gross profit improving by approximately 141 basis points year-over-year. Operating profit increased 13% to $1.9 billion, driven by North American Pharmaceutical, Prescription Technology Solutions and Oncology & Multispecialty. Interest expense was $103 million, reflecting financing activities completed in support of the planned Medical-Surgical Solutions separation.  
The effective tax rate in the second quarter was 17.8%, which included net discrete tax benefits of $105 million. As a reminder, our effective tax rate can vary quarter-to-quarter, driven by timing and the amount of discrete tax items. Diluted weighted average shares were 116.7 million, a decrease of 6%, reflecting continued share repurchase activity. Adjusted earnings per diluted share increased 18% to $11.68, driven by strong operating performance across North American Pharmaceutical, Oncology & Multispecialty and Prescription Technology Solutions segment and the benefit of a lower share count. Excluding the prior year contribution from the $25 million Norway divestiture and the net gains of $51 million from the sale of an equity investment and market positions within the US Oncology Network, adjusted earnings per diluted share increased 24%.
Let me now turn to our segment results. Starting with North American Pharmaceutical segment. Revenues were $91.4 billion, an increase of 6%, driven by higher prescription volumes, including growth in specialty products and GLP-1 medications. This was partially offset by lower contributions from branded pharmaceuticals and continued branded-to-generic conversions. Lower branded pharmaceutical pricing as a result of wholesale acquisition cost decreases in January 2026 reduced year-over-year revenue growth by approximately 4%.
Consistent with prior periods, these pricing changes did not have a meaningful impact on the segment operating profit. Revenues from GLP-1 medication distribution were $16 billion in the quarter, an increase of approximately $3 billion or 26% versus the prior year. Sequentially, GLP-1 revenues increased 8%. Demand and volumes across the category remain strong, with quarter-to-quarter variability based on payer dynamics and patient utilization.
Operating profit increased 22% to $1 billion. Growth was driven by specialty distribution, including health system and strategic accounts. Our distribution platforms support a broad evolving portfolio of products, including increasingly complex therapies. Our reach and expertise allows us to effectively support these products as demand continues to grow.
Turning to Oncology & Multispecialty. Revenues were $15 billion, an increase of 24%, driven by growth from specialty product distribution and higher volumes across our provider platforms. We saw strong utilization within provider solutions, including distribution of Oncology & Multispecialty products. Operating profit increased 8% to $427 million. As a reminder, the prior year period included net gains of $51 million within the US Oncology Network. Excluding the net gains, operating profit increased by 23%.  
Growth was driven by provider solutions businesses, including GPO services and higher specialty distribution volumes. We expanded our provider platforms through growth within existing practices and new provider additions. Utilization trends remain solid, with the same-store patient visits reaching their highest level in recent quarters across our networks.
In Prescription Technology Solutions, revenues were $1.5 billion, an increase of 10%, driven by higher prescription volume in third-party logistics and access solutions. This was partially offset by lower contributions from hub dispensing services. Operating profit increased 18% to $307 million, driven by higher demand across our access solutions, including prior authorization services.  
We continue to see volume growth across services for both GLP-1 and non-GLP-1 medications, including contributions from the CMS Medicare GLP-1 Bridge program, which started on July 1. We also saw solid performance across other therapeutic categories as we added new brands and expanded existing programs across the platform.
Our solutions support biopharma partners across the life cycle of a product. As therapies move from launch to broader adoption and maturity, our platform is well positioned to support the evolving need for access, affordability and adherence solutions.
Turning to Medical-Surgical Solutions. Revenues were $3.1 billion, an increase of 5%, driven by growth across extended and ambulatory care channels. This represents continued sequential improvement in revenue growth trends, supported by higher volumes across multiple product categories, including specialty pharmaceuticals. Operating profit decreased 10% to $225 million, driven by lower contributions from the ambulatory care channel due to product mix, partially offset by growth in the extended care channel. We are pleased with the growth in the extended care channel, supported by higher demand across several product categories.
Wrapping up our review with Corporate. Corporate expenses were $147 million, a decrease of 3%, reflecting disciplined expense management, partially offset by continued investment in technology capabilities to support the business.
Let me turn to cash and capital allocation. We ended the quarter with $6.5 billion in cash and cash equivalents and total liquidity of approximately $11.5 billion, which is above the minimum threshold. Our balance sheet remains robust and provides ample capacity to support our strategic priorities. 
During the second quarter, we delivered free cash flow of $2.9 billion, including $123 million in capital expenditures. Our strong cash generation provides capacity to reinvest in the business, including technology, infrastructure and operational capabilities. We also maintain flexibility to continue to execute our capital allocation priorities, including share repurchases. During the quarter, we returned $990 million to shareholders through a combination of share repurchases and dividend payments. We remain disciplined in deploying capital towards opportunities that offer attractive returns and long-term shareholder value.
Turning now to our fiscal '27 outlook. We delivered strong results through the first half of the year, including second quarter performance that exceeded our expectations. Based on these results, our outlook for the remainder of the year, we are raising our fiscal '27 adjusted earnings per diluted share outlook to $45.60 to $46.40.
We entered the second half with confidence in the fundamentals of our business and our ability to execute against our priorities. Our updated outlook implies adjusted EPS growth of 17% to 19%. Excluding the impact of the Norway divestiture and the net gains within the US Oncology Network in fiscal '26, our outlook implies adjusted EPS growth of 19% to 21%, which is well above our long-term growth target of 13% to 16%. For fiscal '27, we anticipate revenue growth of 6% to 10% and operating profit growth of 12% to 16%.
Let me provide additional context on our segment outlook. In North American Pharmaceutical, we anticipate revenue growth of 5% to 9% and operating profit growth of 14% to 18%. The outlook reflects broad-based strength across the business, including strong performance in the second quarter. We anticipate the momentum will be supported by stable market trends, including growth in prescription volume, increasing demand for specialty and branded medications, including GLP-1s, and benefits of improved productivity, driving operational leverage, underpinned by disciplined execution across sourcing and distribution. The outlook also contemplates continued impact on segment revenue from lower branded pharmaceutical pricing following wholesale acquisition cost decreases.
Looking ahead to the second half of the fiscal year, we anticipate accelerated investments focused on enhancing our capabilities and supporting business growth. Additionally, the outlook reflects our continued strong relationship with customers, including customer wins and renewals of existing relationships.
Turning to Oncology & Multispecialty. We anticipate revenue growth of 20% to 24% and operating profit growth of 18% to 22%. Excluding the net gains of $51 million in fiscal '26, our outlook implies operating profit growth of 22% to 26%. The outlook is supported by provider solutions, including specialty distribution and GPO services, and our broader portfolio of Oncology & Multispecialty offerings.
We continue to see expansion across our provider platforms through both new additions and growth within existing practices. Within our retina and ophthalmology platform, the PRISM Vision Group recently welcomed Spectrum Vision Partners, further strengthening its presence in the Mid-Atlantic region. We anticipate some variability from quarter-to-quarter, including investments weighted towards the earlier part of the second half.
In Prescription Technology Solutions, we anticipate revenue growth of 2.5% to 6.5% and operating profit growth of 11% to 15%. We expect continued growth in access and affordability solutions, supported by demand across GLP-1 medications and other therapeutic categories. As products move through their life cycle, the type and level of support required could change. This creates opportunities for onboarding of new programs and expanding the services provided through existing relationships. These dynamics can also create quarterly variability based on utilization, product launch timing, shifts in payer landscape and changes in program requirements.
For example, we are in the early phases of supporting the CMS Medicare GLP-1 Bridge program. Following initial strong demand, prior authorization volumes have begun to normalize, and we will continue to monitor trends as the program progresses. Looking to the second half, the fourth quarter historically benefits from contribution from annual reverification programs, and we anticipate a similar cadence this year. 
Moving now to MedSurg. We anticipate revenue growth of 1% to 6% and operating profit to range from a 4% decline to flat. Our outlook reflects the breadth of the business across alternate sites of care, including inventory and extended care, consumer health and at-home care. To support future growth, we implemented initiatives across the business focused on driving growth opportunities, building the commercial pipeline and driving operating efficiency. We expect the initiatives implemented during the first half to support growth and performance through the remainder of the year.
Our second half results can also be impacted by the annual illness season. As a reminder, each illness season is unique. The timing, severity and duration can vary from year to year. In Corporate, we anticipate expenses at the high end of the $580 million to $640 million range. As a reminder, we completed our exit from Norway in January. In fiscal '26, the Norway business contributed $74 million of operating profit, including $28 million in the fiscal third quarter.
Turning now to items below the line. We expect interest expense to be in the high end of $380 million to $420 million, reflecting higher borrowing rates associated with financing activities. We expect income attributable to noncontrolling interest of $290 million to $320 million, which includes the minority ownership interest by Apollo in our MedSurg business.
We anticipate a full year effective tax rate of 18% to 19%. We expect quarterly tax rate phasing to be broadly similar to fiscal '26, with a higher tax rate in the third quarter than the fourth quarter due to the timing of discrete tax items.
Wrapping up our outlook with cash flow and capital deployment. We anticipate free cash flow of approximately $4.5 billion to $4.9 billion. As a reminder, cash flow can vary from quarter-to-quarter based on timing, including day of the week a quarter ends.
We remain disciplined on capital allocation. We expect to repurchase approximately $5 billion of shares during fiscal '27. Through the first half, we purchased approximately $3.4 billion of shares at an average price of approximately $818 per share, completing a significant portion of our planned full year share repurchases. We estimate diluted weighted average shares outstanding to be in the range of 115.5 million to 117.5 million.
In closing, I am pleased with our performance through the first half of the year and the progress we are making across the business. We entered the second half with strong momentum, clear priorities and confidence in our outlook. We remain focused on execution and delivering long-term value for our shareholders.
With that, let's move to Q&A.

**Operator** (Operator):
[Operator Instructions] And our first question will come from Glen Santangelo with Barclays.

**Glen Santangelo** (Analysts):
Just 2 quick ones for me. Brian and Kenny, I'm trying to understand these 2 acquisitions you did, Precision Medicine Group and Option Care Health. I'm just trying to -- I want to make sure I'm clear on how these businesses will weave through the reporting segments of the company and the potential impact that, that may have on your margins.
And as I think to model calendar '27, not that you want to give any forward guidance, I'm just trying to think through these ancillary services that you're acquiring. And then secondly, as we have a whole slate of biosimilars set to be launched here in the next 12 months, I'm just trying to think about the puts and takes on your margins across your 2 segments, Onco & Multispecialty and Prescription Technologies.

**Brian Tyler** (Executives):
Why don't I start by maybe reviewing the strategic rationale for these and then, Kenny, you can comment on the question about where it reports and the margin profiles. So Precision Medicine Group, which we closed earlier this week, very excited about. It's really composed of 2 different business segments: Precision for Medicine, which provides global clinical research, translational science and laboratory capabilities with deep oncology experience and trials active in more than 30 countries. We really see that as being highly complementary to our oncology strategy, complementing USON, the joint venture we have with SCRI. And some of the site management and CRO-light-ish skills that SCRI had is now really accelerated with the acquisition of Precision for Medicine. And so as we think about the oncology strategy holistically, we think this is a really, really complementary piece to the assets that we currently have.
And then the other side of Precision is Precision AQ, which is a leading market access, health economics and commercialization services platform, which we think is highly complementary to our access and affordability capabilities and just gives us a broader portfolio or suites of solutions to support our biopharma partners as they commercialize over the life cycle of their products.
So as kind of the strategic rationale, it's really anchored in our 2 core growth strategies of oncology and serving biopharma. Both of these businesses will report through the O&M segment. And would you like to comment?

**Kenny Cheung** (Executives):
Yes. So for PMG, just a couple of things on this one. So as Brian mentioned, very pleased to acquire PMG. We anticipate the transaction to be accretive in the current fiscal year and beyond. A purchase price of roughly $2.25 billion, from a financing source standpoint, this is all funded with cash given the strength of our balance sheet. Reporting standpoint, PMG will be reported within the O&M segment. From a financial profile standpoint, we estimate the acquisition will contribute approximately $0.10 to $0.20 of adjusted EPS in fiscal '27. And by the end of year 3, we estimate accretion of approximately $1.60 to $1.80.
And like other prior M&A, the way to think about this is that we will anticipate a ramp-up in synergies as we continue to integrate the business within our platform. Obviously, there will be cost synergies assumed. But what Brian and I and the whole team are really excited about is the ability for us to enhance our clinical trial capabilities, serve even greater baskets of biopharma companies across more stages of clinical trial, being able to be part of a global platform and just overall strengthen the value proposition for a biopharma company.

**Brian Tyler** (Executives):
And then to the margin profile question, if you remember at our Investor Day a couple of years ago, we laid out kind of on the left side of the slide, you have distribution and GPO with lower margin. As you progress into data services and SCRI, those tend to be higher margin, more complementary -- more higher-margin businesses, and we would put PMG more on the right side of the chart.
The second one you asked about was Option Care. I'll go quickly just in being conscious of time. Let's just remind everybody, this is a minority investment. We really are excited about this investment for a couple of reasons. As we think about the innovation pipeline, how specialty is evolving, we want to be an important player represented in all growth segments. And so given our expertise and scale in specialty, this made sense from that avenue.
We also have a very deep conviction about community-based care and providing care close to the home and in this case, even potentially in the home. And so as we thought our experience managing assets that are community practice-based and our experience in specialty and then the CD&R capabilities that come with it, we think this is just a good setup for us to complement the assets that we have. But this will be recorded under the equity method, so not really in any of the segment margin profiles.

**Kenny Cheung** (Executives):
Yes, just to double click on the equity method. So from a geography standpoint, this will show up as other income within AOP. And from a BU standpoint, as Brian mentioned, not within the BU, but it will be reported within the Corporate segment.

**Operator** (Operator):
And next will be Brian Tanquilut with Jefferies.

**Brian Tanquilut** (Analysts):
Congrats on the quarter. Maybe just a follow-up on the Option Care comments. I know you have a call option on it to acquire the remainder of the business at some point. Maybe, Brian, as we think about the strategy there, I hear your comments on specialty. But is there an overlay there for the oncology business that you're contemplating? Or maybe a different way of asking it strategically, other than just bringing in incremental revenue and access points, I mean, how are you thinking about overlaying that potentially eventually?

**Brian Tyler** (Executives):
Well, we have capabilities at McKesson, not just in oncology but in really all specialties, in rare and orphan therapies, and cell and gene therapies. And as we think about the future of how those markets evolve, we think having -- ultimately having access to our capabilities to provide those in ambulatory infusion, more community-based settings and in the home is going to be a growing and increasingly important channel. And so we just view this as very complementary to the channels and assets and reach that we have today.

**Operator** (Operator):
And next will be Elizabeth Anderson with Evercore.

**Elizabeth Anderson** (Analysts):
Given the outperformance in North American Pharma, obviously, growing well in excess of the long-term guide there. How do we think about the sustainability of that over the long term? It's obviously been several -- a while of this. So we think about sort of where the longer-term drivers of upside to that number might be. Or is this something that you think, okay, that's great, but there are potentially some other things to think about for fiscal '28 and beyond?

**Kenny Cheung** (Executives):
Yes, I can start. So maybe first, let me get into the drivers of Q2, help you understand what drove the 22% AOP growth. And I'll talk more about how we're thinking about the rest of the year leaking into '28 as well. So as you think about Q2, we're pleased with the strong performance of NAPD. Revenue grew 6%, really driven by a few things. One is just broad-based growth, which included higher prescription volume, growth in specialty products and GLP-1s. And just to triple click on GLP-1, was roughly $16 billion of revenue for us, increased $3 billion or 26% year-on-year and 8% sequentially versus last quarter. We did have some WAC declines experienced in the quarter. However, as we mentioned before, it impacts more on the revenue line and less on the operating profit line.
Speaking of operating profit, it increased 22%, driven by growth in the distribution of specialty products, the health systems and strategic accounts. So overall, it was broad-based growth. So that's the beauty of our business. When you parlay a strong, healthy, broad-based growth with continued operational excellence and productivity within our supply chain ecosystem, we saw really nice operating leverage close to 150 bps, which was led by our North America Pharmaceutical business.
So overall, we're really pleased with the growth, the momentum and the durable profile of this business. As I think through the second half of the fiscal year, the outlook reflects continued broad-based strength across the business. We anticipate momentum to be supported by stable market trends, including prescription volume, increasing demand for specialty and branded medication, including GLP-1s and overall continued health of our supply chain.
It also incorporates a couple of other things, investments in the second half of the year. We are continuing to focus on automation, technology and business growth. And also, our outlook reflects continued strong relationship with our customers. So our outlook includes wins, renewals with existing relationships. As we mentioned earlier, we did renew our CVS contract, and that term starts in October 1. It runs through June of 2032, and that is also baked into our outlook guidance as well. So overall, we're pleased with the performance of our business.

**Operator** (Operator):
And next will be Lisa Gill with JPMorgan.

**Lisa Gill** (Analysts):
I just want to follow up on a few things here. When I think about the North American Pharmaceutical performance and you highlighted the specialty tech health system. One, how are you thinking about potential changes around 340B? I know we had an election that happened yesterday, and perhaps some things are off the table. But how could that potentially impact the amount of volume that you see there?
And kind of dovetailing to that, Brian, you talked about a dynamic policy environment. Can you maybe just update us on any of your thoughts now that we have an idea of what Congress is going to look like going into '27? Any changes that you're anticipating that could impact either side of your business?

**Brian Tyler** (Executives):
Yes. All right. Let me start with your first question on 340B. We obviously provide distribution services to contract pharmacies. We support covered entities. We support the biopharma manufacturers themselves. We also, as you know, Lisa, have a range of 340B-related services, including consulting and software to help manage the supply chain optimization.
As we think about the potential for January 2027 implementation of a rebate model, and you've also got OPPS, I think the difficult thing to -- for us to kind of contemplate in this moment is how are these going to be effectuated or implemented? How are customers going to think about new choices? In the case of the rebate model, it's probably a cash, more of a cash issue. So we'll have to work with our customers as we always do. We'll work with them to administratively support what we need to administratively support. We'll work with them to make sure that they continue to have the success they need to have to be viable.
But we really don't know what their response will be in terms of behaviorally trying to grow 340B, trying to migrate away. Do some 340B scripts go to the community? Or do they stay where they currently are? The thing for us is we are represented in all channels. And what we know is the script will still be there, and we'll be ready to receive it and support it in whatever channel we can.
We're actively tracking this. We're very engaged. Depending on where the policy ultimately lands, we will use the capabilities of our company to help navigate both on behalf of the customers and on behalf of ourselves.
To your bigger question of now that I've had 12 hours to absorb the election results, I don't think my view of any of the policy discussion is different than it would have been last quarter. It is a dynamic environment. We know that cost and quality and access and transparencies are going to still be issues of high interest in Capitol Hill from our regulators and our legislators. And we will be part of those conversations, now building new relationships, educating new members, advocating on behalf of what we think is important to helping health care address the challenges that we have, advocating for community-based providers because they're affordable and more accessible.
And we'll continue to build those relationships. And just like we have always done, we've always worked with both sides of the house. We've always worked to try to figure out how we do the right thing for the health care system, and that's what we'll continue to do.

**Kenny Cheung** (Executives):
Yes. Just a couple of things on 340B from my end. Regardless of how 340B plays out, the value of our distribution services remains intact. We'll continue to focus on providing our customers with the highest quality of service and support them with our products and diverse portfolio.
And this is an important piece. We will get fairly compensated for the fair value of service we provide. At this time, we do not anticipate any material financial impact to our business, and as Brian said, we'll watch this very, very carefully.

**Operator** (Operator):
And next will be Kevin Caliendo with UBS.

**Kevin Caliendo** (Analysts):
I'm going to take Elizabeth's question and ask it a little bit differently, which is, your LRP versus what you've done over the last year, 2 years or so, seems comically low. So maybe instead of asking what drove you to getting to, in this quarter, north of 20% EBIT growth, maybe, what needs to happen for you to actually grow North American Pharma inside the LRP? Like what's embedded there for that versus the market growth or whatever? Because it just seems that your ability to beat that is tremendously easy.

**Kenny Cheung** (Executives):
Yes. So I can start. So when we refer to the LRP, obviously, we're referring to the long-term targets. So I've reviewed our long-term business plan. I feel confident about the business fundamentals and our ability to execute against these long-term targets. For EPS, it was roughly 13% to 16%, just to remind everybody.
Looking at the long term, we anticipate the growth will be driven by the strength of our leading platforms in oncology, multi-specialty and biopharma solutions and supported by operating leverage and efficient capital deployment. We are well positioned to capture long-term growth through disciplined execution of strategic priorities and sustainable operational momentum. I just want to remind you that our long-term targets are long term in nature and not an indicator of short-term variations that incur -- that can occur within the business year-to-year.

**Brian Tyler** (Executives):
Yes. I just want to reflect on -- I think the performance we're enjoying now is an accumulation of years of focus on our strategic priorities, years of investment in technologies, whether that's physical distribution or robotic process automation or now large language models in AI that are translating from gross profit leverage ratios that Kenny reviewed. And I think it's just reflective of the great alignment and understanding of the team of how we need to show up every day for our customers, how we win new customers, win customers that are winning, support those customers in a way that enables them to be successful, which reinforces our own success.

**Operator** (Operator):
And next will be Allen Lutz with Bank of America.

**Allen Lutz** (Analysts):
I really appreciate the color so far. One for Brian on the capital deployment strategy. As we think about Precision and we think about Option Care, these are new businesses for you relative to what the capital allocation strategy has been around M&A, adding MSO assets and even added Spectrum to PRISM a few days ago. Can you talk about the relative complexity of integration of PMG and Option Care relative to what we've seen over the past couple of years, growing that U.S. oncology business, growing the retina business? Is there a delta there? Would love any perspective.

**Brian Tyler** (Executives):
Yes. It's a really great question. First, I would say, parts of the Precision Medicine Group business are new to us, like the CRO component. They are highly adjacent to businesses that we're already in, and they are highly relevant because of their focus on oncology to our oncology strategy.
The biopharma services side of that business are natural adjacencies to the businesses that we're already in. And so there's not, per se there, a bunch of integration as much as it is. We now have more solutions that we can put in our bag to offer biopharma manufacturers.
We think we have a great opportunity, I'm not going to say to integrate, but to complement the SCRI capabilities and the PMG capabilities to improve, reimagine, make more efficient and usable and easy the process of getting community-based providers into clinical trials and allowing their patients then to benefit from those therapies.
So we'll be very thoughtful about how we "integrate the business." But these are highly complementary businesses with very little overlap but complementarity to the assets that we have. So we're very excited. We think -- I would just remind you on the Option Care side, we are the minority nonoperating partner. So there will be years where this is really under the stewardship of CD&R. We'll bring our knowledge, expertise in specialty and just understanding of supply chain, obviously help that business, but we'll be relying on them to run it day to day.

**Kenny Cheung** (Executives):
Yes. On Option Care, CD&R is a strong operating partner. We think Option Care is a platform, and it helps having a partner solely focused on strategic investments and growth. And that will be beneficial for us. We will clearly have a voice at the table as well. There'll be proper and appropriate governance. But it really gives an opportunity to grow the business with a strong operating partner that has a lot of experience, while we, as McKesson, can also focus on our own strategic pillars as well as oncology, multispecialty and biopharma services as well. So it's really a win-win proposition.

**Operator** (Operator):
And that question will come from Michael Cherny with Leerink Partners.

**Dylan Finley** (Analysts):
This is Dylan Finley on for Mike. Would love to hear you expand a bit on the Option Care deal rationale. Should we think of this as an operating partnership with CD&R, where you could come in and do something on procurement and contracting and drive value? Or is this primarily an equity method investment? And are there currently any supplier arrangements between McKesson and Option Care? And would that be an opportunity for you in future years?

**Brian Tyler** (Executives):
So first, the Option Care transaction has not closed, so we are still awaiting approval from their shareholders as well as the regulatory agencies. So there are no interfaces ongoing today. We do envision this as a CD&R-run business with the benefits of all the resources and knowledge that McKesson has and can bring to bear around specialty pharmaceuticals, providing care in community-based settings, et cetera.
And so we really like the future trajectory of community and home-based care. We like the future trajectory of specialty. I think as Kenny said, this allows us to germinate a business outside of the day-to-day operating requirements that have been delivering the results that you've seen us delivering. And so I very much think of this as incubating future growth platforms highly adjacent to our core strategy and supporting our long-term growth algorithm well into the future.
Perfect. Great questions. Appreciate everybody taking time to join us. There's a lot going on in the world today that we're all aware of. Look, I'm very pleased with the results that McKesson delivered in our fiscal second quarter. They were very strong. Our strategy is working. Our execution is strong. I'm confident in our ability to continue to deliver long-term sustainable growth for our shareholders.
This does not happen without Team McKesson. So I want to thank them for their continued dedication to advancing our mission. They're unwavering in their commitment to our customers and to our customers' patients and to each other. And they are the foundation for all of the success we will continue to have. So thanks, everybody. I hope you have a great night.

**Operator** (Operator):
Thank you for joining today's conference call. You may now disconnect, and have a great day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MCK_Q1_2027_Earnings_Call_20260805.md
- 2026-08-05｜Brian Tyler｜guidance：FY27 調整後 EPS 財測上調至 $44.20–45.00（原話："guidance to $44.20 to $45.00 from the prior range of"）
- 2026-08-05｜Kenny Cheung｜guidance：財測隱含調整後 EPS 成長（排除挪威出售與 USON 股權出售利得）（原話："It implies adjusted EPS growth of 13%"）
- 2026-08-05｜Kenny Cheung｜guidance：FY27 營收與營業利益成長財測（原話："5% to 9% and operating profit growth of 9% to 13%."）
- 2026-08-05｜Kenny Cheung｜guidance：北美藥品批發營業利益成長落在原區間高端（原話："growth at the high end of the previous range"）
- 2026-08-05｜Kenny Cheung｜guidance：腫瘤與多專科營收財測維持不變（原話："We continue to anticipate revenue growth of 14.5% to 18.5%"）
- 2026-08-05｜Kenny Cheung｜guidance：RxTS 營收成長財測（原話："revenue to increase by 2.5% to 6.5%"）
- 2026-08-05｜Kenny Cheung｜guidance：MedSurg 營收成長財測（原話："We anticipate revenue growth of 1% to 6%"）
- 2026-08-05｜Kenny Cheung｜guidance：利息費用財測（原話："interest expense to be in the range of $380 million to"）
- 2026-08-05｜Kenny Cheung｜guidance：全年稅率財測較前次略升（原話："a slight increase from the prior guidance range"）
- 2026-08-05｜Kenny Cheung｜guidance：FY27 自由現金流財測（原話："cash flow of approximately $4.5 billion to $4.9 billion"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：FY27 回購約 $50 億，Q1 已完成 $25 億（原話："of which $2.5 billion was completed in the first quarter."）
- 2026-08-05｜Kenny Cheung｜capital_allocation：加權平均稀釋股數財測（原話："range of 115.5 million to 117.5 million."）
- 2026-08-05｜Kenny Cheung｜capital_allocation：董事會批准股息調升 15%（原話："approved a 15% increase to our quarterly dividend"）
- 2026-08-05｜Kenny Cheung｜commitment：管理層承諾股息成長與長期獲利成長目標相稱（原話："committed to dividend growth that is commensurate with"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：資本配置優先順序宣稱不變（原話："We remain focused on investing in our strategic priorities"）
- 2026-08-05｜Kenny Cheung｜commitment：新任 CFO 說明其角色標準：say-do ratio（原話："maintain what I call a strong say-do ratio"）
- 2026-08-05｜Kenny Cheung｜margin：NAP 品牌藥 WAC 下降影響營收但對營業利益無顯著影響（原話："they did not have a meaningful impact on operating profit"）
- 2026-08-05｜Kenny Cheung｜margin：品牌藥 95% 以上為服務費模式（口徑說明）（原話："more than 95% of our branded drugs are fee-for-service"）
- 2026-08-05｜Kenny Cheung｜margin：營業費用占毛利比率年減約 150bp（原話："gross profit improved by approximately 150 basis points"）
- 2026-08-05｜Kenny Cheung｜margin：NAP 營業利益成長快於營收（利潤率結構）（原話："AOP did grow faster than revenue"）
- 2026-08-05｜Kenny Cheung｜margin：管理層列出 NAP 利潤率變動的驅動因素（原話："operating margin changes in the segment can be driven by"）
- 2026-08-05｜Kenny Cheung｜product：GLP-1 配送營收 $150 億（原話："GLP-1 medications distribution were $15 billion in the"）
- 2026-08-05｜Kenny Cheung｜guidance：GLP-1 全年持續成長但單季有波動（原話："with quarter-to-quarter variability."）
- 2026-08-05｜Brian Tyler｜product：7 月起支援 CMS Medicare GLP-1 Bridge 計畫（原話："began supporting the CMS Medicare GLP-1 Bridge program"）
- 2026-08-05｜Brian Tyler｜customer：GLP-1 承保面的討論未明顯移動（原話："it really hasn't moved super significantly"）
- 2026-08-05｜Kenny Cheung｜guidance：管理層稱財測為平衡觀點、非最佳情境（原話："a balanced view of the year, not a best case scenario"）
- 2026-08-05｜Kenny Cheung｜guidance：財測較前次中點高 $0.40（原話："the reason why we guided $0.40 above the last"）
- 2026-08-05｜Kenny Cheung｜guidance：6 月為當季最強月份（原話："June was the strongest month of the quarter."）
- 2026-08-05｜Brian Tyler｜risk：學名藥有利因素提前到本年初，以後續季度為代價（原話："That obviously will come at the expense of later quarters"）
- 2026-08-05｜Brian Tyler｜risk：學名藥有利因素提前出現（原話："favorability in the generics portion of the business"）
- 2026-08-05｜Kenny Cheung｜guidance：下半年加速投資（成長與 AI）已納入 NAP 財測（原話："focused on growth and also AI"）
- 2026-08-05｜Kenny Cheung｜commitment：管理層稱投資報酬時點最可能在 2028 年初（原話："return timing will most likely be the beginning of 2028"）
- 2026-08-05｜Kenny Cheung｜margin：O&M 排除 Core Ventures 後營業利益成長口徑（逐字稿記為 50%，與他處 15% 不同）（原話："roughly 50%, which is in line with the long-term targets"）
- 2026-08-05｜Brian Tyler｜customer：Florida Cancer 整合表現（原話："we are on the high end of the guidance range"）
- 2026-08-05｜Brian Tyler｜capital_allocation：不預期有 FCS 規模的併購，但有小型併購（原話："opportunities for kind of the scale of adding additional FCS"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：Kenny 稱會有一些 tuck-in 併購（原話："there will be some M&A along the way,"）
- 2026-08-05｜Brian Tyler｜product：AI 工具被視為擴大醫師看診量的成長動能（原話："expand our capacity to see patients"）
- 2026-08-05｜Brian Tyler｜risk：340B 改革：提案仍在評論期，現在談財務影響言之過早（原話："premature to speculate on the financial impact"）
- 2026-08-05｜Brian Tyler｜risk：IRA Part D 不確定性：MFP 水準未知（原話："We don't know what the MFP will be."）
- 2026-08-05｜Brian Tyler｜risk：IRA Part D 生效時點（原話："until January of 2028"）
- 2026-08-05｜Brian Tyler｜risk：GLOBE 示範計畫對診所無影響的說明（原話："with no impact on the provider practice itself"）
- 2026-08-05｜Brian Tyler｜capital_allocation：MedSurg 將更名 Wellverse（原話："formally operating as Wellverse starting in January 2027"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：Apollo 持有 MedSurg 約 13% 少數股權（原話："Apollo Funds, which now holds approximately 13% minority"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：ASR 初始平均價格（原話："initial average price of approximately $755 per share"）
- 2026-08-05｜Kenny Cheung｜margin：MedSurg 營業利益年減 20%（原話："decreased 20% to $195 million, driven by product mix"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：Q1 自由現金流為負（原話："We had negative free cash flow of $372 million"）
- 2026-08-05｜Kenny Cheung｜capital_allocation：近 12 個月自由現金流（原話："free cash flow remained strong at approximately $6.1 billion"）
- 2026-08-05｜Kenny Cheung｜guidance：FCF 財測維持不變、未上調（原話："sticking with the current guide"）
- 2026-08-05｜Kenny Cheung｜guidance：管理層稱營運資金改善有機會優於財測（原話："opportunities along the way to beat that off"）
- 2026-08-05｜Kenny Cheung｜guidance：季度節奏：Q4 為最大季（原話："Q4 will be the biggest quarter for us"）
- 2026-08-05｜Kenny Cheung｜guidance：Q2 對比去年 $51M 出售股權利得（原話："lapping prior year gains of $51 million"）

### 問答異常語氣（迴避／改口／保留）
- MCK_Q1_2027_Earnings_Call_20260805.md｜問：Kevin Caliendo 追問自由現金流兩年來成長落後獲利、何時加速｜答法：未給具體加速時點或數字，回答維持原財測並稱「More to come on this one」，改談 Q1 較去年改善與營運資金結構性改善
- MCK_Q1_2027_Earnings_Call_20260805.md｜問：Michael Cherny 追問 NAP 下半年比較基期與路徑｜答法：Brian 提到學名藥有利因素提前、將以後續季度為代價；Kenny 轉談新產品時點與下半年加速投資，未給下半年季度數字
- MCK_Q1_2027_Earnings_Call_20260805.md｜問：Lisa Gill 追問 340B 變動對北美業務影響｜答法：管理層稱提案仍在評論期、推測財務影響言之過早，未給數字
- MCK_Q1_2027_Earnings_Call_20260805.md｜問：Kenny 回答 Elizabeth Anderson 時稱 O&M 排除 Core Ventures 後營業利益成長約 50%｜答法：該數字與準備稿的約 15% 不一致，後續 Kenny 亦稱「The 15% growth I mentioned earlier」；原稿未更正

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
{"date":"20260525","verdict":"A 核心候選 / 觀望偏進場（pullback 中）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"U.S. Pharmaceutical 段保持 11-13% Rev CAGR + Pharma OI margin ≥ 1.4%","columns":{"2Y 驗證":"FY27 全年 Rev +12% + Pharma OI margin ≥ 1.4%","5Y 驗證":"FY30 Rev $590B + Pharma OI margin 1.5-1.6%","10Y 驗證":"FY32+ 維持市佔 41-43%","具體數字門檻":"季 Rev YoY ≥ 10%；季 Pharma OI margin ≥ 1.4%","信息來源":"MCK FY26 10-K + mgmt FY27 guide","漂移觸發":"連 2 季 Pharma Rev YoY &lt; 8% → 削弱"}},{"id":"H2","text":"Oncology & Multispecialty + Specialty Solutions 段保持 +20-25% Rev YoY + OP margin ≥ 3%","columns":{"2Y 驗證":"FY27 全年 Oncology Rev +25% + OP margin ≥ 3.5%","5Y 驗證":"FY30 Oncology Rev $60B + OP margin 4-5%","10Y 驗證":"FY32+ MSO 平台 physicians ≥ 5,000","具體數字門檻":"季 Oncology YoY ≥ 20%；OP margin ≥ 3%","信息來源":"MCK 2025 investor day + FY26 Q4 update","漂移觸發":"連 2 季 Oncology YoY &lt; 15% → 削弱；OP margin &lt; 2.5% → 反轉"}},{"id":"H3","text":"MedSurg 分拆 2027 完成 + spinco 創造 unlock value（MCK 估值 multiple 維持或擴張）","columns":{"2Y 驗證":"2027 MedSurg spin-off / split-off 完成 + Apollo $1.25B 退場 / 轉換","5Y 驗證":"分拆後 MCK + spinco 合計市值 &gt; 當前 $95B + 25%","10Y 驗證":"分拆後 MCK 獨立 Pharma + Specialty 報表清晰，multiple expansion 至 20x","具體數字門檻":"2027-06 前完成 spin；spinco IPO 或合約完成","信息來源":"MCK Q1 FY26 announcement + Apollo deal 2026-04-20","漂移觸發":"分拆延後 6+ 個月 → 警戒；分拆放棄 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"MedSurg 分拆執行失敗或大幅延後","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"SEC 8-K + 公司 announcement + Apollo 出場條件","警戒閾值":"分拆延後 6 個月以上 OR Apollo 公開退出 OR financial restatement → 立即重評"}},{"id":"R2","text":"OptumRx 大單反向流失或 in-house in-house","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"季財報 segment 細節 + Optum / UNH 公開合約 disclosure","警戒閾值":"OptumRx 合約變動公告 → 立即重評；MCK 大客戶 disclosure 變化 → 警戒"}},{"id":"R3","text":"Direct-to-pharmacy / Lilly Direct 類模式擴大壓 distributor margin","columns":{"對應假設":"H1, H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Lilly / Pfizer / Novo Direct 業務 disclosure；GLP-1 distribution 模式變化","警戒閾值":"連 4 季 Specialty Rx margin 下滑超 50bp → 結構性壓力；direct 模式占 GLP-1 30%+ → thesis 部分推翻"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"🟢","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":766.08,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
