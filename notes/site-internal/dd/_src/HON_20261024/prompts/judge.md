你是 stock-analyst **v20 判斷 agent**，標的 HON（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"HON","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":4994,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}},{"id":"f_kpi1_gaap","label":"GAAP 營業利益","value":740,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益率","value":14.8,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}},{"id":"f_kpi3_segment_margin","label":"Segment margin（公司口徑調整後營業利益率）","value":21.3,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}},{"id":"f_kpi4_adjusted_eps","label":"Adjusted EPS","value":2.27,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}},{"id":"f_kpi7_2026","label":"全年 2026 指引","value":"見 guidance 欄","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}},{"id":"f_kpi8_backlog","label":"Backlog","value":19000,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"USD m（近 19B）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_hon_gross_margin_pct","label":"HON 毛利率","value":36.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hon_operating_margin_pct","label":"HON 營業利益率","value":16.58,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_hon_fcf_margin_pct","label":"HON FCF 利潤率","value":11.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rok_gross_margin_pct","label":"ROK 毛利率","value":54.53,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rok_operating_margin_pct","label":"ROK 營業利益率","value":19.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rok_fcf_margin_pct","label":"ROK FCF 利潤率","value":16.76,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sie_de_gross_margin_pct","label":"SIE.DE 毛利率","value":39.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIE.DE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sie_de_operating_margin_pct","label":"SIE.DE 營業利益率","value":12.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIE.DE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_sie_de_fcf_margin_pct","label":"SIE.DE FCF 利潤率","value":14.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIE.DE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbn_sw_gross_margin_pct","label":"ABBN.SW 毛利率","value":40.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbn_sw_operating_margin_pct","label":"ABBN.SW 營業利益率","value":16.93,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbn_sw_fcf_margin_pct","label":"ABBN.SW FCF 利潤率","value":11.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5_fcf","label":"自由現金流（FCF）","value":688,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}},{"id":"f_kpi6_sbc","label":"SBC 占營業利益","value":14.1,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 新聞稿（Form 8-K Exhibit 99，新聞稿稿名載明 IR 網站 investor.honeywell.com）https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":221.15,"period":"2026-10-23（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-0.24,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":66.35,"period":"2026-10-23（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":1.56,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.31 → 8.44）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.51,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.79 → 9.84）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.64,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.96 → 11.03）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":8.44,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.84,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":11.03,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.81,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 8.29 → 8.44（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":10.96,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":1.86,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝39.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":39.0,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":2.13,"period":"2026-10-23（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-23（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-23（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-23（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":26.2,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 8.44，分子＝快照價 221.15","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.01,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":10407.0,"period":"2026-10-24","unit":"USD m","basis":"yfinance 最新一季：總債務 16593.0、現金 6186.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":316.94,"period":"2026-10-24","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":80498.28,"period":"2026-10-24","unit":"USD m","basis":"市值 70091.28 ＋ 淨負債 10407.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":20158.86,"period":"2026-10-24","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（22 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":20524.26,"period":"2026-10-24","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.99,"period":"2026-10-24","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-24"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 221.15 / W52 224.57 / W104 216.81 / W250 196.48 / W250 13週斜率 0.22%"},{"id":"f_ma_w52","label":"52 週均線","value":224.57,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":216.81,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":196.48,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.22,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"HON 10-K 列出各事業主要對手（航太：Garmin、L3Harris、Rolls Royce、RTX、Safran、Thales；樓宇：Johnson Controls、Schneider、Siemens；工業自動化：Emerson、Rockwell 等），並把新進入者與產品商品化列為可能造成市占下降、價格與毛利下滑的風險。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"changes in the competitive landscape, including new market entrants and new technologies that may lead to product commoditization, and adverse industry economic conditions, all of which could result in lower market share, reduced selling prices, and lower margins.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"10-K 稱公司須在對手數量不斷增加（含許多新進與非傳統對手）的情況下守住市占。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"defend our market share against an ever-expanding number of competitors, including many new and non-traditional competitors","as_of":"2026-02-17","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"CSIMarket 顯示 Honeywell Aerospace 在其追蹤同業營收合計中的份額由 4.62% 降至 4.31%（商業資料庫，分母口徑未驗證）。","source":"CSIMarket HON Competitors","url":"https://csimarket.com/stocks/HON-Competitors","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 10-K 稱公司銷售不實質依賴單一客戶或少數客戶群，信用條款設計以降低單一客戶信用集中。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"The Company's sales are not materially dependent on a single customer or a small group of customers.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Q1 2026 10-Q 揭露 Fitch 於 2026-03-06 將信用評等展望由 watch negative 調為 stable；本次搜尋未見 2026 年主要評等機構降級。","source":"SEC EDGAR 10-Q Q1 2026（經搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000057/hon-20260331.htm","excerpt":"On March 6, 2026, Fitch revised their credit rating outlook from watch negative to stable.","as_of":"2026-03-06","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Honeywell Aerospace Q2 2026: orders +8% with book-to-bill 1.1 but output only +4%; supply chain constraints persist, 2026 organic growth guidance cut to 4-5%.","source":"GuruFocus/MarketBeat, Honeywell Aerospace Q2 2026 earnings call highlights","url":"https://www.gurufocus.com/news/9009441/honeywell-aerospace-inc-hona-q2-2026-earnings-call-highlights-supply-chain-constraints-prompt-guidance-reset-despite-robust-demand","excerpt":"Orders increased 8% over the past year, with a book-to-bill of 1.1. Supply chain constraints persist, with output growth only 4% in Q2, below expectations, leading to a guidance cut.","as_of":"2026-08-05","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Management expects aftermarket catch-up from 2027 as supply constraints ease, supporting 6-8% CAGR through 2030; OE prioritization temporarily depresses spares.","source":"MarketBeat, Honeywell Aerospace Q2 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/honeywell-aerospace-q2-earnings-call-highlights-2026-08-05/","excerpt":"Catch-up in aftermarket expected from 2027 as supply constraints ease, supporting a return to 6–8% CAGR through 2030.","as_of":"2026-08-05","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Critical suppliers reduced from hundreds to 70 with only 10 highly constrained across four commodities after >$1B investments since 2023; supply-chain actions expected to matter more in 2027.","source":"GuruFocus, Honeywell Aerospace Q2 2026 earnings call highlights","url":"https://www.gurufocus.com/news/9009441/honeywell-aerospace-inc-hona-q2-2026-earnings-call-highlights-supply-chain-constraints-prompt-guidance-reset-despite-robust-demand","excerpt":"Investments exceeding $1 billion since 2023 have reduced critical suppliers from hundreds to 70, with only 10 now highly constrained across four key commodities.","as_of":"2026-08-05","retrieved_at":"20261024","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Aerospace backlog up 9% YoY to ~$18.2B at end Q2 2026; trailing 12-month orders +8%, led by Defense and Space.","source":"Pulse 2 / Honeywell Aerospace Q2 2026","url":"https://pulse2.com/honeywell-aerospace-15-billion-of-new-wins-includes-record-810-aircraft-indigo-deal-as-backlog-reaches-18-2-billion/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"FY2025 10-K：2022 年 Petrobras／Unaoil 的 DOJ、SEC 與巴西當局調查已和解；2025 年 7 月 DOJ 聲請提前終止 DPA，法院准許，相關指控已不得再訴而撤銷。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"In July 2025, the DOJ filed, and the court granted, a motion for early termination of the DPA, and the deferred charges related to the UOP Matters have been dismissed with prejudice.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FY2025 10-K 風險因素列出反壟斷等訴訟與調查屬一般性風險，未指明現行具體反壟斷調查。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"We are currently, and may in the future become, subject to lawsuits, fines, investigations, and disputes (some of which involve substantial amounts claimed) arising out of the conduct of our business","as_of":"2026-02-17","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 披露國際營運（含美國出口）占銷售逾半，關稅與其他貿易限制若升高，可能衝擊競爭地位與財務表現；美國對中國等國關稅已引發報復性關稅，公司稱可能有重大不利影響，且無法保證完全抵銷","source":"SEC EDGAR Honeywell 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"Our international operations, including U.S. exports, represent more than half of the Company’s sales.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 稱美方持續對中國及其他國家商品加徵關稅並引發報復，公司已部署緩解策略，但不保證能完全抵銷","source":"SEC EDGAR Honeywell 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"While we have deployed strategies to mitigate the impact of these dynamic trade policies, there is no assurance that we will be able to mitigate the full impact of all such tariffs, retaliatory tariffs or other trade policies that have or may develop in this rapidly changing environment.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 載明航太事業多項主要零組件與原料為單一或唯一來源採購，關稅與貿易障礙可能影響關鍵供應商","source":"SEC EDGAR Honeywell 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"Many major components, product equipment items, and raw materials, particularly in Aerospace Technologies, are procured or subcontracted on a single or sole-source basis.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 載明俄烏衝突下美國與他國對俄、白俄實施制裁與出口管制，公司對俄方合約剩餘義務無法估計超出已提列準備的合理可能損失","source":"SEC EDGAR Honeywell 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"Given the uncertainty inherent in our remaining obligations related to our contracts with Russian counterparties, we do not believe it is possible to develop estimates of reasonably possible loss in excess of current accruals for these matters.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026 年 Q1 10-Q 列出 2025 與 2026 年關稅、新貿易調查與談判造成市場波動，並提及關稅傳導增加供應鏈與成本壓力；摘錄未給中國專屬金額","source":"SEC EDGAR Honeywell 10-Q (2026-03-31)","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000057/hon-20260331.htm","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Honeywell 10-Q 揭露：營運處於中東衝突環境，影響能源市場、貿易流與航運；管理層稱正轉向在地/區域供應來源並對受限物料雙重採購，並警告地緣衝突、貿易政策變動與通膨可能對業績造成重大不利影響。","source":"Honeywell Form 10-Q FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000143/hon-20260930.htm","excerpt":null,"as_of":"2026-10-23","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Honeywell 10-Q 稱，對其製造或採購所在國家的關稅或貿易限制可能損害競爭地位與財務結果；Q1 2026 10-Q 並提及中東衝突、美國關稅授權法院裁決後的政策不確定性。","source":"Honeywell Form 10-Q Q1 FY2026 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000057/hon-20260331.htm","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"FY2024 10-K 風險因子：供應商財務困難或交貨問題可能使公司無法滿足供應需求，導致銷售與利潤下降、合約罰則或終止；未找到指名單一供應商/零件為關鍵單點。","source":"Honeywell Form 10-K FY2024 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384025000010/hon-20241231.htm","excerpt":null,"as_of":"2025-02-13","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Aerospace 負責人 Jim Currier（2025年3月）稱機械類供應基礎「still very fragmented」「still very non-robust」，為持續性問題。","source":"IndustryWeek: Honeywell aerospace CEO says supply chain problems persist","url":"https://industryweek.com/leadership/companies-executives/article/55273946/honeywell-aerospace-ceo-says-supply-chain-problems-persist","excerpt":null,"as_of":"2025-03-01","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Building Automation sales $2,020M, +8% organic YoY","source":"Honeywell Q3 2026 earnings release (8-K Ex.99)","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm","excerpt":"Building Automation sales grew 8% organically1 year over year.","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Industrial Automation sales +4% organic YoY (reported -23% due to divestitures)","source":"Honeywell Q3 2026 earnings release (8-K Ex.99)","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm","excerpt":"Industrial Automation sales grew 4% organically1 year over year.","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Process Automation and Technology sales $1,859M, +8% organic YoY","source":"Honeywell Q3 2026 earnings release (8-K Ex.99)","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm","excerpt":"Process Automation and Technology sales increased 8% organically1 year over year.","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Backlog up 7% YoY to nearly $19B; company raised FY organic revenue, adj EPS and FCF outlook; FY sales $20.0-20.1B","source":"Honeywell Q3 2026 earnings release (8-K Ex.99)","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm","excerpt":"Backlog increased 7% year over year to nearly $19 billion","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"10-K 風險因子列出成長取決於監控顛覆性技術與商業模式、防止產品商品化，並提及競爭者可能開發售後服務與零件；未點名具體替代技術。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"(iii) defend our market share against an ever-expanding number of competitors, including many new and non-traditional competitors; (iv) enhance our products by adding innovative features that differentiate our products from those of our competitors and prevent commoditization of our products;","as_of":"2026-02-17","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"10-K 指出需監控顛覆性技術，且競爭者可能開發售後服務與零件吸走客戶、衝擊新產品投資報酬。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"(vii) monitor disruptive technologies and business models; (viii) achieve sufficient return on investment for new products introduced based on capital expenditures and research and development spending;","as_of":"2026-02-17","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Memoori 比較樓宇業者 AI 策略：四大業者押注水平平台層，Honeywell 靠 Niagara 裝機基礎；Trane 收購 BrainBox AI 走單一領域深度。","source":"Memoori: AI Strategies of the Smart Building Incumbents: 2026 Compared","url":"https://memoori.com/ai-strategies-smart-building-incumbents/","excerpt":"all betting that value accrues to the horizontal platform — the layer that aggregates data across HVAC, fire, security, energy, and third-party systems, and increasingly fronts it with generative AI agents. OpenBlue, Forge, Building X, and EcoStruxure are competing visions of the same thesis. The differentiation is in the substrate: Honeywell brings Niagara’s 1M+ installed middleware instances,","as_of":"2026-06-12","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"FY2025 10-K：各報告分部不倚賴任何單一專利、商標、授權或經銷權；經查一手文件未見單一通路／經銷權依賴。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"Our reportable business segments are not dependent upon any single patent or related group of patents, trademarks, licenses, or distribution rights.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Honeywell 2026 委託書稱修剪商業模式適配度低的資產，聚焦經常性、連網與售後服務；並提及 5K+ 頂級通路夥伴。","source":"SEC EDGAR DEF 14A 2026","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000029/hon-20260409.htm","excerpt":"Global Installed Base in Buildings ~20K Process Plants with HON Technology >5K+ Top Tier Channel Partners PORTFOLIO OPTIMIZATION AND STRATEGIC CAPITAL DEPLOYMENT","as_of":"2026-04-09","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Tickflow 報告 27 位分析師共識 Buy、平均目標價 $249.64（2026-07-31）；VCP Scanner 7 月初為 $251.08（28 位，區間 $220–$276）；StreetInsider 12 個月平均 $253.74，Jefferies Hold 目標 $255（2026-08-17）。","source":"Tickflow / VCP Scanner / StreetInsider 搜尋摘要","url":"https://tickflow.io/stock/HON/forecast","excerpt":"The consensus among 27 analysts covering Honeywell International Inc. (HON) is Buy with an average price target of $249.64.","as_of":"2026-07-31","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 2026 財報 8-K：調整後 EPS 指引由 $8.05–$8.35 升至 $8.40–$8.45，營收指引 $20.0B–$20.1B（原 $19.8B–$20.0B），有機成長 4–5%（原 3–4%）；指引含 Johnson Matthey Catalyst Technologies 併購（2026-07-17 完成），且 1 比 2 反向分割 2026-06-29 生效，與分拆前基準不可直接比較。","source":"SEC 8-K Exhibit 99 Q3 2026 earnings release（經搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0000773840/000077384026000141/exhibit99-q32026earningsre.htm","excerpt":null,"as_of":"2026-10-23","retrieved_at":"20261024","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"MarketBeat 稱 FY2026 EPS 指引 $8.05–$8.35 低於 $10.78 的分析師預估、營收指引 $19.8–20.0B 低於 $24.1B 共識，平均評級 Hold、共識目標價 $257.79；共識似為分拆前舊基準，尚未更新。","source":"MarketBeat: Honeywell releases FY 2026 earnings guidance","url":"https://www.marketbeat.com/instant-alerts/honeywell-international-nasdaqhon-releases-fy-2026-earnings-guidance-2026-08-01/","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q1 2026 後 Barclays 將 12 個月目標價由 $255 降至 $243（4/24），維持 Overweight，理由為航太部門表現；來源為轉載站，品質偏弱。","source":"轉載頁 Honeywell HON Sell-Side Analysts Trim Price Targets Post Q1 2026 Results","url":"https://www.ocpartnership.org/first-dry/Honeywell-International-Inc-HON-SellSide-Analysts-Trim-Price-Targets-Post-Q1-2026-Results-Flag-Aerospace-Segment-Headwinds-11-4788","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Honeywell 於 2026-06-29 完成 Aerospace 分拆（Spin-Off），Aerospace Technologies 自 2026 年第三季起列為停業單位。","source":"SEC EDGAR 8-K Item 2.01（2026-06-29）","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000084/hon-20260625.htm","excerpt":"In connection with the completion of the Spin-Off, the Company’s Aerospace Technologies business will be reported as discontinued operations beginning in the third quarter of 2026, and retrospectively for all comparative periods reported.","as_of":"2026-06-29","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"2026-01-16 與 Flexjet、Duncan、StandardAero 達成全面和解，相關案件已於 2026-01-21 前撤銷。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"On January 16, 2026, the Company completed a comprehensive settlement relating to its lawsuit with Flexjet. As part of this comprehensive settlement, the Company entered into settlement agreements with Duncan, StandardAero, and Flexjet. As of January 21, 2026, each of these cases have been dismissed.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"Aerospace 分拆前發行 160 億美元優先無擔保票據。","source":"SEC EDGAR 8-K（2026-03-16）","url":"https://www.sec.gov/Archives/edgar/data/773840/000119312526108366/d107386d8k.htm","excerpt":"Aerospace issued $16,000,000,000 aggregate principal amount of senior notes in a private offering","as_of":"2026-03-16","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Honeywell 於 2026-06-29 完成 Aerospace 分拆。","source":"SEC EDGAR 8-K Item 2.01（2026-06-29）","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000084/hon-20260625.htm","excerpt":"In connection with the completion of the Spin-Off, the Company’s Aerospace Technologies business will be reported as discontinued operations beginning in the third quarter of 2026, and retrospectively for all comparative periods reported.","as_of":"2026-06-29","retrieved_at":"20261024","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"+","claim":"與 Flexjet 的訴訟於 2026-01-16 全面和解並撤銷。","source":"SEC EDGAR 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/773840/000077384026000013/hon-20251231.htm","excerpt":"On January 16, 2026, the Company completed a comprehensive settlement relating to its lawsuit with Flexjet. As part of this comprehensive settlement, the Company entered into settlement agreements with Duncan, StandardAero, and Flexjet.","as_of":"2026-02-17","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#0","axis":"product_recall_warning","section":"events","direction":"-","claim":"英國產品安全通報（2026-06-25）：Honeywell Lighting Controls UltraLite CDW4U1UL／CDW6U1UL 特定批次因黏著不良有觸電風險，召回換新。","source":"GOV.UK Product safety alert（2606-0168）","url":"https://www.gov.uk/product-safety-alerts-reports-recalls/product-recall-honeywell-lighting-controls-connect-ultralite-cdw4u1ul-and-cdw6u1ul-2606-0168","excerpt":null,"as_of":"2026-06-25","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"HON","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":36.57,"operating_margin_pct":16.58,"fcf_margin_pct":11.1,"rd_intensity_pct":5.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.HON","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"ROK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":54.53,"operating_margin_pct":19.75,"fcf_margin_pct":16.76,"rd_intensity_pct":5.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ROK","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"SIE.DE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.36,"operating_margin_pct":12.98,"fcf_margin_pct":14.61,"rd_intensity_pct":8.31},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SIE.DE","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ABBN.SW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":40.09,"operating_margin_pct":16.93,"fcf_margin_pct":11.7,"rd_intensity_pct":3.92},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBN.SW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"SU.PA","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SU.PA"},"note":"quarterly_income_stmt 無資料"}],"subject":"HON"},"financial_history":{"ticker":"HON","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":35466000000.0,"revenue_yoy_pct":null,"gross_margin_pct":36.99,"operating_margin_pct":18.12,"net_income":4966000000.0,"diluted_eps":14.54,"free_cash_flow":4508000000.0,"fcf_margin_pct":12.71,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":33009000000.0,"revenue_yoy_pct":-6.93,"gross_margin_pct":37.48,"operating_margin_pct":18.51,"net_income":5658000000.0,"diluted_eps":16.94,"free_cash_flow":4599000000.0,"fcf_margin_pct":13.93,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":34717000000.0,"revenue_yoy_pct":5.17,"gross_margin_pct":38.47,"operating_margin_pct":19.21,"net_income":5705000000.0,"diluted_eps":17.42,"free_cash_flow":5226000000.0,"fcf_margin_pct":15.05,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":37442000000.0,"revenue_yoy_pct":7.85,"gross_margin_pct":36.93,"operating_margin_pct":17.54,"net_income":4729000000.0,"diluted_eps":14.72,"free_cash_flow":5422000000.0,"fcf_margin_pct":14.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HON/HON_Q3_2026_Earnings_Call_20261022.md）

# Q3 2026 Earnings Call
**Honeywell International Inc.** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Thank you for standing by, and welcome to the Honeywell Technologies Third Quarter 2026 Earnings Conference Call. [Operator Instructions] Please be advised that today's call is being recorded. I would now like to hand the call over to Mark Macaluso, Senior Vice President of Investor Relations. Please go ahead, sir.

**Mark Macaluso** (Executives):
Thank you. Good morning, and welcome to Honeywell Technologies Third Quarter 2026 Earnings Conference Call. Joining me today are Honeywell Technologies' Chairman and Chief Executive Officer, Vimal Kapur; and Senior Vice President and Chief Financial Officer, Mike Stepniak. 
This webcast and the presentation materials, including non-GAAP reconciliations, are available on our Investor Relations website. From time to time, we post new information on the Investor Relations website that may be of interest or material to our investors. Our discussion today includes forward-looking statements that are based on our best view of the world and of our businesses as we see them today and are subject to certain risks and uncertainties, including those described in our recent SEC filings. This morning, we will review our financial results for the third quarter of 2026 and discuss our updated 2026 guidance. And as always, we'll leave time for your questions at the end.
With that, it's my pleasure to turn the floor over to Vimal, who will begin on Slide 3.

**Vimal Kapur** (Executives):
Thank you, Mark, and good morning, everyone. Our first quarter as a stand-alone pure-play automation company was a clear demonstration of the value creation strategy we laid out during Investor Day in June with broad-based organic growth, strong margin expansion and higher free cash flow conversion. And I'm very pleased with the results our teams delivered.
This quarter showed the breadth and quality of new Honeywell Technologies portfolio with strong results across all segments. We delivered 7% organic sales growth above the high end of the targets we unveiled at Investor Day in June. Demand across the portfolio was broad-based, which drove short-cycle orders growth of 8%, excluding our divestitures led by Industrial and Building Automation. Additionally, the growth inflection we expected in Process Automation and Technology is occurring with the business growing 8% organically in third quarter. As I will talk more about shortly, we believe PA&T is beginning a multiyear growth inflection fueled by a robust project backlog and continued capital investment in energy sector, especially in Africa, Middle East and U.S.
On profitability, we expanded margins by 370 basis points to over 21% through strategic pricing, productivity actions and the continued reduction in the stranded cost. Importantly, with accelerated progress this quarter, we now expect to eliminate all remaining stranded costs by end of 2026, just 6 months after the Aerospace spin-off, demonstrating our strong execution capabilities. Together, this combination of profitable growth and the fixed cost productivity drove adjusted EPS of $2.27, up 34% year-over-year.
To round out the story, the cash conversion accelerated to 95% for the quarter, and we expect to be above 100% conversion in the fourth quarter. As a result of our strong execution this quarter and momentum heading into fourth quarter, we are raising our full year 2026 guide across all metrics. The growth inflection in PA&T and the turnaround in Industrial Automation are well underway, compounded by 8 straight quarters of outperformance in Building Automation. Mike will talk more about our stronger outlook for Q4 and the full year in a few minutes.
Our transformation into a pure-play automation company is complete. As our third quarter results have demonstrated, we have strong position in growing end markets, differentiated offerings and clear competitive advantage in higher-growth verticals like LNG and data centers. We are instrumenting the business to outperform both in 2027 and over the long term with strong short-cycle demand, a backlog of nearly $19 billion and momentum across the portfolio. This gives me and the leadership team great confidence in delivering of our 2029 targets.
Let's now turn to Slide 4 to talk more about the order trends in the business. The key takeaway is that demand remains strong across most of our portfolio. We saw growth across our short-cycle businesses led by sensing and measurement in Industrial Automation and double-digit growth in Building Automation product businesses. Orders in data center vertical were up over 100%. In PA&T, we saw strong refining catalyst demand, consistent with our expectation for a second half recovery. And on a regional basis, we saw strength in India, the Middle East and Africa. 
In Process Automation and Technology, we are navigating tough prior year comparison due to the 2 strategic low carbon energy and LNG awards in third and fourth quarter of 2025, which were each $700 million. From time to time, large award like this do not always correlate with underlying market demand we are seeing, which is why we have elected to present a normalized view of the demand. Excluding the impact of Q3 award last year, total company orders are up 3% organically. Furthermore, book-to-bill in this quarter was 1.0, which drove ending backlog to nearly $19 billion, up 7%, excluding our divestitures. 
In PA&T, specifically, the backlog was up double digits, driven by these large project awards. We continue to believe that the ongoing transition to LNG and renewable as priority fuel, increasing pipeline activity from refurbishment and rebuilds in Middle East and the refining build-out in Africa will drive a meaningful energy up cycle over the next several years. Looking ahead to the fourth quarter, we expect orders to grow in the high single-digit range, excluding the large LNG awards shown in the chart on Slide 4. This will be driven by demand in Middle East, India and Asia Pacific in Process Technology and Building Automation, continued short-cycle demand in Building Automation products and sensing and utilities in Industrial Automation and momentum in our high-growth verticals.
Let us now turn to Slide 5 to discuss the favorable dynamics we are seeing in the global energy value chain, reinforcing our growth outlook for Process Automation and Technology business. On a global basis, we continue to see activity increasing on large energy projects, including over $1 billion in Process Technology orders since quarter 1 of 2026. PA&T backlog is over 10% higher than a year ago, supported by win across LNG, refining and petrochemicals and low-carbon energy projects. The breadth of these orders is important, too. We are seeing investments across North America, the Middle East, Africa and Asia rather than a single region. LNG remains strong in U.S. and internationally, while refining and petrochemical orders include major projects in Africa and continued activity across Middle East and Asia.
Low carbon energy remains a small part of the business overall, but it's growing at a strong double-digit rate with wins in areas such as sustainable aviation fuel and carbon capture. And we continue to believe that longer term, this will be a growth driver. These orders expand our installed base and create opportunities beyond the initial project win. As these facilities come online and operate at high utilization rate, they will drive future demand for catalyst, automation, digital modernization and life cycle services. Overall, the strength and global diversity of the orders give us confidence in the outlook for continued growth of PA&T segment as we enter 2027.
In conclusion, we are seeing robust backlog growth and commercial momentum across our business, and we expect 2027 organic growth to be at or above our long-term growth algorithm. Let me now turn it to Mike to discuss the third quarter results and our 2026 outlook in more detail.

**Mike Stepniak** (Executives):
Thank you, Vimal, and good morning. In the third quarter, Honeywell Technologies delivered strong results that surpassed our expectations across most metrics. Sales grew 7% organically with strength across all segments. Process Automation Technology sales grew 8% organically, led by double-digit growth in projects and a return to growth in aftermarket, led by refining catalyst demand. Project sales grew 14% year-over-year, led by strong LNG and petrochemical backlog conversion. The momentum in Building Automation continued with 8% organic growth, our eighth straight quarter of high single-digit growth, evidence that we continue to gain share in the market. This was principally driven by 11% organic growth in products, led by both the Fire and Security businesses, while Solutions also grew 4% organically, driven by strength in services. On a regional basis, we saw double-digit growth in both India and Asia Pacific with continued strength in the Americas.
Finally, in Industrial Automation, organic sales were up 4% in the third quarter, led by double-digit growth in solutions, principally in industrial measurement and utilities. Product sales were roughly flat with sensing and industrial measurement demand offset by industry-wide deferrals in meter deployments across the utility segment. On profitability, segment profit grew 23% and segment margin expanded 370 basis points to 21.3%, driven by productivity, accelerated stranded cost elimination as well as strategic pricing actions and volume leverage. This more than offset rising inflation, headwinds from the mix of projects versus aftermarket and the acquisition impact in Process Automation and Technology.
By segment, in Industrial Automation, price and productivity actions in the core business drove 350 basis points of margin expansion with the business firmly on path to deliver 22% segment margin in the fourth quarter. In Building Automation, segment margin expanded another 30 basis points to 27%, driven by volume leverage and pricing actions that more than offset rising inflation. And in Process Automation and Technology, margin contracted as expected, driven by mix headwinds stemming from higher project growth and dilution related to the acquisition of Johnson Matthey's Catalyst Technologies business. 
Adjusted earnings per share was up 34%, driven primarily by 23% segment profit growth and lower interest expense, which more than offset a higher adjusted tax rate in the quarter. Finally, free cash flow was up 15% to roughly $690 million, while our conversion increased to 95% in the quarter. We expect free cash flow conversion to be above 100% in the fourth quarter as we drive working capital improvements, including strong receivable collections.
Let's now move to Slide 7 to discuss the third quarter segment margin and adjusted EPS bridges. Starting with margin, we're delivering stronger incremental margin in our short-cycle businesses, driving roughly 70 basis points of volume leverage. We're also continuing to effectively mitigate high inflation with strategic pricing actions, productivity and a reduction in stranded costs. We expect inflation to remain at these levels at least into the first half of 2027. Our strong market positions, installed base-driven business model and the mission-critical nature of our offerings give us confidence in our ability to successfully navigate this inflationary environment.
On adjusted EPS, earnings growth in the third quarter was principally driven by a strong operational performance in all 3 segments, which allowed us to overcome the operating loss from our divestitures. Below segment profit, interest and other expenses declined year-over-year, while our tax rate was slightly higher. We're making good progress against commitments we outlined at the Investor Day in June. Our focus on offsetting inflation, delivering productivity and aggressively eliminating stranded costs for transformation is having a meaningful impact. This provides a strong foundation for 2027.
Let's turn to Slide 8 to provide an update on our leverage commitments. As I discussed at the Investor Day, we're committed to reducing our gross leverage to less than 3x this year by lowering our gross debt balance from $18 billion in the second quarter to under $13 billion at the end of 2026. This will be enabled by the acceleration in free cash flow that we expect to continue in the fourth quarter. We expect our year-end cash balance to be approximately $3 billion, resulting in a net debt of around $10 billion. Importantly, the cash generation and continued reduction in our leverage will increase our capital allocation flexibility, including capacity to pursue disciplined M&A. 
Let's now turn to Slide 9. As you can see here, we have made considerable progress reducing fixed costs related to the portfolio transformation, and we expect this to continue in 2027. We're implementing a cross-functional shared services model across the company with a simplified and more flexible corporate structure. More importantly, during this time, we continue to invest in our businesses to drive future growth. The progress on stranded cost reduction underscores the pace of execution across the organization and the progress we are making in building a simpler, more focused company. This will position the company for long-term profitable growth. Executing stranded cost takeout within 6 months of the Aerospace spins demonstrates the strong operational execution capabilities of Honeywell Technologies. 
Let's turn to Slide 10 to discuss our revised full year outlook. Today, we're raising our full year organic growth, adjusted earnings per share and free cash flow guidance as well as tightening our margin guidance around the previous high end. We now expect full year organic growth of 4% to 5%, up from 3% to 4% previously, driven by our execution in the third quarter and stronger outlook in the fourth quarter. By business, in the fourth quarter, we expect to see continued strength in buildings across both products and solutions, high single-digit growth in Process Automation and Technology led by project backlog conversion and higher catalyst volumes and continued sensing and industrial measurement demand in Industrial Automation. As a result, we expect to deliver 5% to 6% organic growth. 
With the performance to date, we expect to be at the high end of our full year margin range at 20.5% and at approximately 22% for the fourth quarter. This will continue to be driven by pricing, productivity and volume leverage, overcoming higher inflation and anticipated mix headwinds in Process Automation and Technology, driven by higher project activity and dilution from the Catalyst Technologies acquisition. Industrial Automation should be at 22% margin in the fourth quarter, while Building Automation is expected to expand margins 70 to 90 basis points and Process Automation Technology will end the fourth quarter around 21.5%.
We now expect full year adjusted EPS in the range of $8.40 to $8.45, which represents a $0.23 improvement at the midpoint. Notably, the low end of our guidance range is now above our previous high end. This results in full year earnings growth of approximately 30%. Lastly, our free cash flow guidance is up $100 million to $2.1 billion given the higher income conversion. You can find additional information on our 2026 outlook in the appendix of our presentation, which includes estimates for corporate and below-the-line items. Thank you for your time today.
Let me now turn the call back to Vimal to wrap up before the Q&A.

**Vimal Kapur** (Executives):
Thank you, Mike. We are proud of our results in the first quarter as a stand-alone company. We surpassed our expectations across most metrics, and we see encouraging demand signal in many key end markets. We believe PA&T is at the beginning of a multiyear growth inflection, coinciding with an up cycle in global energy markets. We are also encouraged by the turnaround the team is driving in Industrial Automation, and Building Automation continues to execute on all fronts. We're also launching new offering on our Forge platform, both in Building Automation and Process Automation and Technology, creating a robust foundation for future growth. With our performance this quarter and backlog of nearly $19 billion, we are confidently raising our 2026 outlook across all metrics, setting up for a strong start to 2027.
Thank you for joining us today. And Mark, let's now take some questions.

**Mark Macaluso** (Executives):
Vimal, Mike and I are now available to answer your questions. [Operator Instructions] Operator, please open the line for Q&A.

**Operator** (Operator):
[Operator Instructions] Our first question comes from the line of Nigel Coe with Wolfe Research.

**Nigel Coe** (Analysts):
So I'm curious the confidence in 4Q order growth. We're still only 1 month into the quarter. I'm assuming December is a pretty important month for bookings. So I'm just wondering what gives you the confidence that the pipeline converts into orders? And maybe just touch on how you -- what you've seen in October.

**Vimal Kapur** (Executives):
Yes. So, so far, Nigel, the first 3 weeks of October has been trending on and above expectations. So that certainly is a good data point. And we look at our statistical performance against pipeline, our win rates when we forecasted. We also provision for some adequate contingency for things which cannot happen as projected. So overall, our confidence to what we are stating on high single-digit orders growth in quarter 4, less of the low carbon energy -- LNG order, I'm sorry, which we booked last year, which was several hundred million dollars, we remain highly confident on that.

**Nigel Coe** (Analysts):
Okay. Okay. And then, Mike, a quick one on stranded costs. Good news that you'll be done by the end of this year. I think that's about 6 months earlier than expected. Does that change your perspective on your corporate expense for next year? I think that the guide was less than $600 million. How does that look right now?

**Mike Stepniak** (Executives):
Right. So it's a little bit early yet, but -- and we'll talk about it in February. But for next year, just like we talked about, I think, before, we plan for our corporate cost to be about $400 million. And then we're instrumenting the teams, obviously, to productivity and margin expansion north of 60 bps, like we talked about. So I feel we have a really good setup. Like you said, we're ahead, and that has implications as far as us having a really good momentum going into next year, and we'll work with that.

**Operator** (Operator):
Our next question comes from the line of Julian Mitchell with JPMorgan.

**Julian Mitchell** (Analysts):
Just wanted to start off with a question on the IA segment. It's had a sort of rocky or uneven time for a few years for various reasons. It looks to be very well set today with a large sequential margin increase guided for the fourth quarter. I suppose maybe when we try and look a little bit further out, how confident are you in continued margin expansion at IA in the coming quarters? And given the macro backdrop is a bit choppy, anything concerning you've seen in the order rates of IA, the shorter-cycle pieces?

**Vimal Kapur** (Executives):
So overall, Julian, for IA, we remain very confident on continued performance in both top line recovery and margin rate expansion. The reason for that is the basics are improving as we talked about it in Investor Day very rapidly. Our on-time delivery now is -- it used to be just shy of 40% is now 60%. Our past dues are down 18%. Our new product launches are being highly accepted by our channel partners and our OE customers. So those foundations has turned the business from a negative territory to now more low single digit. And we do expect that it will continue to progress and find its pathway to mid-single-digit growth as we lap from '26 to '27. So we remain very convicted.
Same is true on the margin rate. We expect the year to end at 22%. Primarily, it's a higher-quality business now. And from this baseline, as we continue to execute our pricing action, productivity actions, we remain very confident on the margin expansion and also achieve 25% goal by 2029. So overall, sensing and measurement, building a unique segment in Industrial Automation, that's our pathway. And we remain highly convicted this is a high-quality business as part of our portfolio.

**Julian Mitchell** (Analysts):
That's helpful. And then just a quick follow-up on PA&T. Margin pressure kind of year-on-year in the third quarter, that's continuing into the fourth. Should we assume that margins stay under that type of pressure until the Johnson Matthey acquisition anniversaries? Or is there anything in the base business moving around that could help the margins sooner?

**Mike Stepniak** (Executives):
Yes. So versus where the team finished at the 22.2%, I would say, next quarter, 21.5%. And then in the first half, I would say, probably something similar. But next year, PA&T is going to expand margins. And what's happening there is, one, we have catalyst mix is starting to mix up. That volume is going to grow. That's going to help. The project volume mix is going to abate. And as you know, we obviously are integrating CT. So in the second half, we will be substantively past CT integration. We see a really good margin expansion into the second half of 2027.
And I'd just remind you, like we talked about, this is a multiyear cycle. In 2028, there is a significant margin pickup again as we're counting on catalyst volume. So we have very good visibility to this cycle. We have proven it cycle over cycle over multiple decades, and we're extremely confident on the progression of the business in that fashion.

**Operator** (Operator):
Our next question comes from the line of Steve Tusa with Wells Fargo.

**Charles Stephen Tusa** (Analysts):
Very helpful chart on the segment bridge. Can you just -- I think, kind of teasing out core incrementals, putting everything else aside on volume, roughly 40%. Is that right? And then can you just discuss that inflation number, the 350 basis points? Like what was that in the first and second quarter? And then what do you expect for that in the fourth?

**Mike Stepniak** (Executives):
Sure. So you're exactly right. I think on core, we're about 40% incrementals. Price to cost in the third quarter was about 30 bps net positive. So that 350 bps that you -- on inflation is a little bit higher versus the first half, but also our price is higher. We are averaging about 3.5% price in the first half. We'll average about 4.5% in the second half, 4% for the year. That's going to be on a year basis, maybe 10, 20 bps of, I would say, margin expansion from price cost. And we see, obviously, inflation elevated. We expect that to continue into year-end and then starting to abate in the first half. Everything we get from our teams as far as planning for next year, we see inflation coming down a bit. So the price will move with that, but it's still around that 3% to 4%.

**Charles Stephen Tusa** (Analysts):
Okay. And then just for the fourth quarter, my follow-up is the margin went to the low end of the range, I guess, for the fourth quarter. Any -- is that really just the price cost timing stepping up a little bit sequentially? Just curious as to that or just conservatism?

**Mike Stepniak** (Executives):
No, not at all. Pricing cost is well. We actually -- we managed price in the third quarter to account for year-end. It's really just mix. So revenue is coming up. And like Vimal talked about, the products are performing extremely well. We don't see anything changing on products. On the other hand, projects is doing better and CT outlook is better, and they're dilutive to our overall mix, and that's what's driving our margin to that 400 basis. Still, I would say at the high end of our guide for the year, 20.5%, about 300 bps margin expansion for the year, really good setup for next year.

**Operator** (Operator):
Our next question comes from the line of Scott Davis with Melius Research.

**Scott Davis** (Analysts):
I appreciate the shorter comments today, too, to leave more time for Q&A. Guys, you've been seemingly gaining a meaningful amount of share in Fire, Security. It seems for a while now. That was always a pretty low growth business, like literally like a 1% to 2% type growth business. You seem to have made it something a little bit bigger. What -- can you just update us on what you're doing there? And what's kind of changed at the margin? What's driving that growth or at least the sustainability of that growth?

**Vimal Kapur** (Executives):
I think the fundamental is our higher cycle of new product introduction, coupled with the mix change of the end markets. So we continue to amplify our new product introduction and maintain a very high vitality by which we then gain share from our competition. Forge is playing a very important role. Fire business was the first out of the door to build a connected solution by which you can configure our fire panels remotely. We introduced that almost 3 years back. So what it does is, Scott, that while the software content is low, it pulls the core product. And that value proposition is very compelling for our channel partners because they save significant commissioning time, inspection time and improve their P&L.
Also, we are benefiting from data center growth. We have some unique products in fire for data center growth for early detection of fire in a very unique environment because you have a lot of electrical cables, a lot of servers. So there's a unique way we detect fire there. We have differentiated product line. We also introduced some unique new products for detecting fire in batteries as more and more lithium-ion batteries are being used. 
On the Security side, we're benefiting from very premium position of LenelS2. They continue to perform at double-digit growth rates across the world. And Honeywell added a lot of value in that business by globalizing it. We talked about that hypothesis when we acquired the business. And we clearly see growth of that business outside the U.S. with a lot of synergies we are bringing in. So all in all, I would say we maintain the momentum in this business, and we see no reason that we won't perform at this level in the foreseeable future.

**Scott Davis** (Analysts):
So just to follow up on that on Forge, just that answer was complete. But how do you go to market with Forge then? Is this kind of the -- is it getting wrapped in as a standard offering with every install? Or has it come in as kind of a sidecar, if you will, and priced separately? I mean how do you guys go to market with it and get value for it? Or is it just more of a tool used to, again, to be able to gain share because you've got another kind of...

**Vimal Kapur** (Executives):
So there are -- no, very good question, Scott. There are 3 sales motions for Forge today. So it's our recurring revenue is now coming close to $1 billion in 2026, just shy of that. The first sales motion is Forge is sold along with our service contracts. So we make our customers connect to Forge, change the pricing of our service contract because we are able to provide higher value outcome. So that's sales motion 1. Sales motion 2 is there are unique applications built in to make our existing offering better, like I gave an example of fire panel. So they are now, even though we sell it as a stand-alone offering, but it goes hand-in-hand with our core products.
And then the third is a stand-alone offering of Forge, which we launched, I would say, 18 to 24 months back, first in buildings, where we can connect stand-alone buildings of even competitors apart from Honeywell installed base to get better insight into customers' energy consumption, predictive maintenance, emissions. And we launched a similar offering for process earlier this year. In that scenario, it's sold as a stand-alone SaaS software. So all 3 sales motion are in place. And as we talked about at Investor Day, we expect our ARR to grow. Our aspiration is 15%. We want to have high aspiration. This year, probably we'll be slightly shy of that, more like 12%, 13%, but we'll continue to work our way through to get to closer to 15% every year.

**Operator** (Operator):
Our next question comes from the line of Amit Mehrotra with UBS.

**Amit Mehrotra** (Analysts):
Maybe just starting with Process and just understanding sort of the mid- to long-term growth opportunity as these maybe comps normalize. Obviously, great to see the high single-digit growth as you expected. I know there's been sort of a management change recently from Building to Process. I think Forge Cognition is maybe part of the growth story. So just talk about sort of beyond the first half of '27 and into the second half and beyond, what we think the sort of run rate steady-state growth opportunity is for Process?

**Vimal Kapur** (Executives):
So we see, Amit, the growth in Process Automation and Technology, both on the project side and on the aftermarket and services and catalyst side. The project side, if you see the chart we added into our prepared remarks, we see continued investments in LNG. So our backlog is very strong for LNG. We also see investments in Africa and Middle East and Asia on traditional refining, which is helping us a lot in our backlog. And finally, we also see activity in low carbon energy projects. Just as a reminder, we have licensed 100 projects so far in sustainable aviation fuel and only about 20% of those have been built so far. So there's a lot of runway people coming back to us with FIDs, which then turn into a significant revenue stream. So project activity remains very robust and very diversified.
Then on the aftermarket side, we expect second half of 2026 catalyst growth to be double digit. It's double digit in Q3. It's going to be actually mid-teens growth in Q4. And given the higher margins our customers are making on the finished products, we expect catalyst demand to remain strong in 2027, more normalized year. And on the automation side, we see strength in our services portfolio, cybersecurity, our Forge offering, we call it Plant Cognition. So that offering is also getting strong customer reception. 
So across the board, as Mike laid out, we see this as a multiyear cycle in which the project strength will provide us the top line growth and we'll maintain our margin with a high mix of catalyst and services and software as we progress.

**Amit Mehrotra** (Analysts):
Got it. Okay. That's helpful. And maybe just as a follow-up, I know 2027 guidance is forthcoming, but I think, Vimal, you've talked about sort of at or above the long-term algorithm. I think, Mike, maybe a couple of months ago, you sort of floated this idea of 15% EPS growth. If I just sort of compare the 2, I would say, bottom line EPS growth, maybe I would have expected something a little bit higher just given the margin opportunity. Maybe just unpack that a little bit for us. Maybe the IA margins headwind in the first half of next year, maybe that's what's driving it. But just to the extent that you can, just sort of fill in the color between what you've already commented on '27 between the algorithm versus the 15% EPS growth.

**Vimal Kapur** (Executives):
I would say, Amit, the setup for 2027 is very strong. First for starters, our midpoint of the guide for '26 is up by $0.23. So we are starting at a higher baseline. On the top line, we remain very confident on performing at upper end of our 4% to 6% guide. Our backlog is very strong. Our short-cycle momentum sustained itself, and we continue to maintain our share or gain share through new products. So that's going to continue.
On the margin rate, we have done a good job to manage inflation through price cost. It's slightly positive. We expect to maintain that. And we have maintained our fixed cost by elimination of stranded costs ahead of time. So when you see the setup here across the board, top line margin expansion and fixed cost, we expect a strong print in 2027. I can't tell you specifics because I'll be giving you guide, which I think we'll have to wait for February when we plan to come back to you. But final comment I'll make is, directionally, we are on the road to deliver $12 or better our long-term 2029 guide we set up in Investor Day.

**Operator** (Operator):
Our next question comes from the line of Nicole DeBlase with Deutsche Bank.

**Nicole DeBlase** (Analysts):
If we could just start with the 4Q outlook. I think you're embedding a little bit of a deceleration in organic growth, but backlog is obviously so strong, short-cycle order growth is still strong. Can you maybe talk through the expectations by segment, like what's driving the modest deceleration that you've embedded for 4Q?

**Mike Stepniak** (Executives):
I would say probably this is just more conservatism than anything else. We -- like we said, I think on the short-cycle orders, they're extremely strong on product side, of BA and IA booked in third quarter, high single-digit, double-digit growth. So we feel good about that. And then projects are incrementally better. So I think it's just more mix. And like we said, we'll do 4% to 5% in the -- for the year and 5% to 6% in the fourth quarter. And as we stand today, we're probably on the higher end of the 5% versus -- so it's incrementally, we feel -- I would say we feel better about the fourth quarter.

**Vimal Kapur** (Executives):
I think it's fair to say, Nicole, we don't see any change quarter-on-quarter. I think the revenue mix can be different within a quarter for projects. But other than that, fundamentals of the business remains very strong quarter-over-quarter.

**Nicole DeBlase** (Analysts):
Okay. Understood. And then maybe just in IA, you guys referenced some deferrals in utility meter deployments. Can you just give some more color around what's going on there? And if that's expected to continue into 4Q or into '27, the time line for that kind of rectifying?

**Vimal Kapur** (Executives):
Yes. I think that's more of an upside opportunity for us in 2027. We've introduced some very new technology, both for gas meters and water meters. Gas meters, unlike electricity meters have not been upgraded at a large scale by utilities over the last decade. So our technology being new is being tested by multiple utilities and each utility done their testing by themselves rather than this being a common testing protocol, which just adds time.
So we are in the process of working with our testing of our new gas meter with several utilities. And once they complete that cycle, which could be 6 to 9 months, we expect them to turn into a major rollouts '27 onwards for several years. So actually, the low growth in our metering business is actually already factored in, in '26 and potentially in '27. But looking ahead, it's going to turn into a tailwind when the adoption rates will pick up in the period ahead.

**Operator** (Operator):
Our next question comes from the line of Andrew Obin with Bank of America.

**Andrew Obin** (Analysts):
Can you hear me? Excellent. Just a question a little bit on Process Automation and Technology on the aftermarket services. I think you highlighted some good tailwinds on Catalyst. But if I look at sort of year-over-year comps, I mean, the comps have gotten quite a bit easier versus last quarter. So I would have expected more of a pickup sequentially in organic growth. What are the headwinds that the business is facing because clearly, the catalyst business is accelerating. But what are the headwinds?

**Vimal Kapur** (Executives):
I mean I won't call it headwinds. When you grow at 8% and then you grow subsequent quarter, probably at 7%, I may not call it headwinds. I would simply call it the cycle of the projects. I can't control the milestone when they have to be achieved. So they come at a certain timing. So I would say, broadly speaking, the PA&T revenue profile on an organic growth basis is very similar between Q3 and Q4. Q3 was slightly higher versus Q4, but not substantially different. You are talking a narrow range here. Catalyst demand is very strong in quarter 4, sequentially better than quarter 3. We were double digit, and we're going to go towards mid-teens growth in catalyst. For example, in quarter 3, our refining catalyst growth was up 80%. So we expect to maintain high rates there. Services growth also remains strong in automation, more like low to mid-single digits. So fundamentals are very robust in this business. I think the change you see is just the sequencing of the projects within a quarter.

**Andrew Obin** (Analysts):
Okay. And just maybe another question on Industrial Automation. On the products, what would it take for the products to start growing faster? Because I think you guys sort of talked about initiatives to get deliveries on time, delivery improved, so that would sort of lead to a lot of good things happening. What would it take for that growth in that business to inflect materially positive or we're waiting for the new product introduction, as you alluded in the prior answer?

**Vimal Kapur** (Executives):
I think directionally speaking, Andrew, if you observe, we have been turning this business to slow growth. Now we are at low single-digit territory right now. I would also like this to go to mid-single-digit territory. And we expect that to occur in 2027 moving forward. I think the drivers of fundamentals are the same. I talked about improving customer service, better delivery, improved past due rates, that's certainly already happening. New product launches and its penetration is -- takes time. I think that's the only variable. As some of them gets more penetration, we expect to continue to perform better in this segment. So there's no doubt in my mind. I think it's just the timing as we go from low single digit to mid-single digit in this portfolio -- in this business in '27.

**Mike Stepniak** (Executives):
And Andrew, I would just add that the third quarter orders for Industrial Automation core were up 15%. So this is a business that's going to the next year probably with the best backlog it has seen in over 5 years. We're quite confident about finishing.

**Vimal Kapur** (Executives):
And we expect fourth quarter orders to be up high single digit. So there is a lot of momentum here. It's just the cycling of the business going from one phase to another phase.

**Operator** (Operator):
Our next question comes from the line of Andrew Kaplowitz with Citigroup.

**Andrew Kaplowitz** (Analysts):
Vimal, I think we know your data center business overall is still a relatively small part of Honeywell. But last quarter, I think you mentioned your offerings in power generation were beginning to help your Process business in data centers in addition to Building Automation. So how do we think about that data center, call it, ecosystem and how it might help you in '27 and beyond?

**Vimal Kapur** (Executives):
Well, certainly, we always talked about data center as mid-single-digit business for BA, Building Automation. We are now turning to a point with the change in demand of the customer. We continue to see this can become actually, at some point, mid-single digits of Honeywell. So we -- because now we see the demand in Process Automation, we saw year-to-date orders growth of more than 100%. Based upon the pipeline visibility we have, we expect very high growth in 2027 also. It will be mixing up not only the Building Automation, but even some Process Automation order for power island for controls, for energy storage, that solution is being mixed up.
One interesting thing which is occurring in addition to this for the last, I would say, 6 months is liquid cooling. As liquid cooling will take more penetration, we expect our spend -- share of spend to further go up. We are working with customers for sensing for liquid cooling from our sensors business. And our Sundyne pumps are a premium solution to circulate those liquid cooling. Those will -- as we can imagine, those are going to scale in future, probably it's more post '27. 
But what I can see is something we started with a very modest content in Building Automation. Now we added Process Automation and now we are adding even our content from Process Technology and Industrial Automation. It's truly becoming a pan-Honeywell strategy, and we continue to improve our content. Last comment I'll make is, as we grow -- as data center growth is happening outside the U.S., in Europe and in Asia, particularly in Korea and India, we expect to continue to do well because of our global presence and global execution capabilities.

**Andrew Kaplowitz** (Analysts):
That's helpful. And then, Vimal, I think you or Mike mentioned that you'll get net leverage down under 2.25 by the end of the year. And so -- and I think you also mentioned at that point, you could pursue, I think you said, disciplined M&A. So how do you characterize the environment right now? Obviously, it's the new company or the new Honeywell Technologies. So any sort of repriorities that you have as you move forward here toward the end of the year?

**Vimal Kapur** (Executives):
I mean our highest priority is first to get our leverage ratio 3 or below and continue to work it way down as we get into '27, generate more cash, we want our leverage to further improve. Think from an M&A perspective, it's an optionality. As you know, our 2029 $12 commitment is all organic. So we have no compulsion. We have no need to wake up and think about an M&A to do our -- meet our organic earnings commitment.
Having said that, we are looking at options 3 ways: highest priority being Industrial Automation, how we look at adding more content in measurement and sensing. That's the highest priority. Second area we are looking at it is higher growth verticals, how can we add more content to further upgrade our portfolio. And finally, we never overlook some of the frontier technologies. There are always tuck-ins, which can change the profile of our businesses, and we look at these midsized small businesses in addition to that. But -- all said, I think near term, you will see us staying very disciplined on our debt paydown and we'll work our pipeline for M&A for '27 onwards.

**Operator** (Operator):
Our next question comes from the line of Joe O'Dea with Vertical Research Partners.

**Joseph O'Dea** (Analysts):
Can you talk a little bit about the self-help opportunities moving forward, what you're most excited about heading into next year? I'm not sure if you perhaps touched on this with Johnson Matthey and Catalyst Technologies, but just on the heels of the speed with which you did the stranded cost takeout kind of thinking about other parts of the organization where you see kind of the biggest self-help opportunities.

**Mike Stepniak** (Executives):
I would say just quickly maybe 2 or 3 which stand out the most, and that's obviously a focus for us as a company. One is, we're moving more into lighter headquarters and more of adoption of shared services across the company, which obviously will help us continue to focus on productivity, which is value engineering, component engineering. That's more from a supply chain standpoint and how we think about NPI. That's a significant opportunity for us.
And finally, we're obviously working through adoption of AI. All of our teams are either already trained or being trained on AI. Everybody has access to the models using across the company, and that's really opportunity for us in terms of manage OEF. And it's not as far as reduction in OEF, but manage the OEF growth or staying flat on OEF while we obviously grow mid- to high single digit operation.

**Vimal Kapur** (Executives):
Two points I'll add to what Mike said on the self-help side. First is on the Catalyst Technologies business, as we integrate the business, we are seeing higher cost synergies than we had forecasted. So that should certainly help us in our 2027 planning. We are also working on sales synergies, building pipeline, but that you can imagine that takes time to convert into a real revenue. So we do expect CT business to overdrive from a cost synergy standpoint.
Final point I would say is cross-sell between different parts of Honeywell. I gave an example of data center just in my remarks a couple of minutes before on how something which was centered around just one segment, we are doing it cross segment. We are doing that in other verticals, too. For example, in life sciences, how we cross-sell between Building and Process Automation. In semiconductor, where we have a very strong position in gas detection, how we also accelerate our participation in fire detection, which comes from Building Automation. So that's also a self-help. It's leveraging our sales channels to the fullest potential. And certainly, we are maximizing our efforts on that.

**Joseph O'Dea** (Analysts):
And then on Building Automation and demand visibility, clearly, strength is in the data center side of things, but maybe talking about end markets ex data center. Obviously, the growth rates over the past couple of years are tougher comps. But what the product innovation pipeline looks like, what that means in terms of the growth visibility you have heading into next year in the non-data center parts of Building Automation?

**Vimal Kapur** (Executives):
I think the Building Automation business, the content of higher growth verticals and in high-growth verticals, we count 3 data centers, health care and hospitality is 20%. 80% of the business come from core or base business, and that's growing at mid-single digit. And that's on the strength of great customer service and new products.
To your question on new products, we have several big launches coming up ahead. Really right now, we have a new version of our security system launched, which is cloud-based. That's going to play in the mid-segment. A lot of our new offerings are actually going into the mid-segment as a broader theme. A new version of our fire system going into a mid-segment. We're also looking at similar offering in building management system. We are refreshing our EBI platform with a newer version. So across the board, we have learned that as we continue to accelerate our vitality and innovate, we will perform at this level of mid-single-digit plus. And the pipeline is very full, and I'm extremely confident on performance of results by this business.

**Operator** (Operator):
Our next question comes from the line of Joe Ritchie with Goldman Sachs.

**Joseph Ritchie** (Analysts):
So I think I'm going to focus both of my questions on PA&T. So I guess on the project side of the business with Brent now sitting above $110, typically, that stimulates investments from your customers. I don't know if you can maybe just give us a little bit of background on like what your customer conversations are like today, whether the pipeline has like materially increased over the past year. I thought that Slide #5 was very helpful. But just any color you can give us on that would be great.

**Vimal Kapur** (Executives):
So we -- as we said in the chart, Joe, we see investments certainly in diversity of fuels and energy security. What I mean by that is Africa was not seen as a destination of investments by refining petrochemicals. So Dangote Refinery, if you recall during Investor Day, he was up there and talking about partnership with Honeywell. They're not only expanding their existing refinery by 100%, which is the largest refinery in the world. They are doubling it. They're also putting additional refinery in Kenya. These are all firm projects. If you look at their cash flow, it's billions of dollars in a quarter. So these are high certainty projects. There are additional investments happening in Africa on petrochemical side, too. So we can clearly see that as a trend.
One thing which we highlighted is also low carbon energy projects are finally taking shape from a low base. We had 2 big wins on carbon capture-related projects in quarter 3, and we have some robust pipeline for quarter 4 ahead for us. So there are some investments happening. And the driver for that is European Union continues to hold its mandate for SAF adoption. And to fulfill that demand, there's more capacity which is required.
And finally, we do see capacity addition for petrochemicals. Our licensing activity and automation business in petrochemicals continues to remain strong. So when you add it all together, it's less linked to the oil price. It's more linked to the drivers, which are more broader, energy security, resiliency, low carbon fuels or the broader demand of petrochemicals. And that's why we believe it's a multiyear cycle. It's less linked to the price. It's more linked to other drivers. That's why it gives us more conviction.

**Joseph Ritchie** (Analysts):
Yes. Super helpful, Vimal. And I guess maybe just to ask Andrew's question slightly differently from before. On the refining side of the business, are you seeing any deferrals just given where crack spreads are, refiners may be running out harder a little bit given profitability looks really, really good right now. So are you seeing like any of that like business maybe pushing out into next year? Or has that remained very healthy for you?

**Vimal Kapur** (Executives):
I would say what we all read, deferrals or higher uptime by U.S. refiner is actually correct, which essentially means that some of the activity, which requires a shutdown cannot be performed. We look at our services business, aftermarket business in 2 buckets. A lot of it can be done online. So a lot of our automation offerings do not require a plant shutdown. If you want to harden your control system for cybersecurity or you want to migrate to the current version, it can be done online. So those businesses get protected even though customers are running at a higher rate. 
But there are things which you need to replace like a Sundyne pump has to be replaced, you need a shutdown or if you want to refurbish a catalyst. So to me, there's some demand moving right, but it's not a lost demand. It's moving -- it's kind of pent-up demand, which will eventually show up. But when you look at the global view, the overall services and catalyst demand is very stable. As I mentioned before, we see the catalyst demand to be in teens -- high teens in quarter 4. Next year, we see overall catalyst to be very stable, mid-single-digit growth. Services growth remains very stable. Yes, absolutely, this is a trend of high utilization and no shutdowns. But it doesn't change the overall dynamics of the business for us in the near term.

**Operator** (Operator):
Our next question comes from the line of Varun Govindaraj with Bernstein.

**Varun Govindaraj** (Analysts):
So a question on PA&T. When you're looking at projects and their delivery times, have they been in line with historical norms? I think there's been a concern that we're short labor in North America and that might lead to some of this just getting stretched. Are you seeing any of that in your numbers? Or is that not really a concern right now?

**Vimal Kapur** (Executives):
Not a concern because a large part of our backlog is actually not in North America. LNG backlog is in North America. Everything else is in rest of the world. And in case of LNG, we build our own equipment in our own factory, and we have enough capacity to fulfill all our backlog. So we don't have any concern on that. On a broader basis, yes, the construction labor or labor shortages is a trend, but that's not driving any impact on our revenue execution on a visible basis.

**Varun Govindaraj** (Analysts):
Appreciate it. And then just as a side note. So on Industrial Automation, big sequential jump from 18.4% to 22%. How much of that is coming from the spins of WWS and PSS and how much of that is more productivity? It feels at this point, everyone is very confident about the number, but just any color on that split?

**Mike Stepniak** (Executives):
Yes. I would say that organically, if you will, the business is probably expanding 150-plus bps just by operation getting better, rest of it is related to the [indiscernible] separation.

**Operator** (Operator):
Our final question this morning comes from the line of Dan DiCicco with BMO Capital Markets.

**Daniel DiCicco** (Analysts):
On the inflation topic, 4.5% price in half 2, just what businesses are you having to push the hardest on price? And then is there anywhere in the portfolio where this might be proving to be a little bit more challenging?

**Vimal Kapur** (Executives):
I mean the pricing is -- I wouldn't say there's a large deviation within the segment. Pricing is a factor of inflation in the segment. And inflation drivers vary from semiconductor to electronics to metals like copper and brass. So I would say that our overall pricing is a narrow range. It doesn't vary from business one -- from 1% and some business is 10%. It's not in that wide range. You can have a range from 3.5% to 4.5%. So it's a very narrow range for us. And the pricing attainment doesn't require only the action of pricing, but it requires good customer service, good customer communication, a good pipeline of new product. And I think that comprehensive 360-degree view is what we have really adopted to attain the price and keep the price cost positive.

**Operator** (Operator):
Ladies and gentlemen, that concludes our question-and-answer session. I'll turn the floor back to Mr. Kapur for final comments.

**Vimal Kapur** (Executives):
Thank you. I would like to thank our shareowners, our customers and all Honeywell Technologies Futureshaper around the world for the strong third quarter results you delivered. Today marks another important milestone in our journey as a new Honeywell Technologies. Our first quarter as a stand-alone pure-play automation company demonstrated progress on all 3 elements for our investment case, broad-based organic growth, strong margin expansion and a higher free cash flow conversion. PA&T is converting its backlog into organic growth. IA is driving meaningful turnaround and BA continues to deliver. With nearly $19 billion in our backlog and a strong 2026 outlook, we entered the fourth quarter with strong momentum and increased confidence in our ability to deliver the commitments we outlined at Investor Day.
Thank you all for joining us today, and we hope you have a great rest of your day.

**Operator** (Operator):
Thank you. This concludes today's conference call. You may disconnect your lines at this time. Thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HON_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：全年有機營收成長財測上修（原話："up from previous guidance of 2% to 3%"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：全年調整後 EPS 中點 8.20 美元（原話："We now expect full year adjusted earnings per share of $8.20"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：全年 segment margin 擴張幅度（原話："segment margin expansion of 250 to 290 basis points"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：年底 segment margin 水準（原話："exit the year above 22% segment margin"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：全年自由現金流（原話："expect free cash flow of roughly $2 billion in 2026"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：PA&T 自第三季起成長急遽轉折（原話："we expect a sharp inflection in growth"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：2027 展望較上月投資人日更強（原話："looking stronger versus when we talked even last month"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：中東營收與訂單全年預期（原話："orders should be about 40%"）
- 2026-07-23｜Vimal Kapur (CEO)｜guidance：第二季訂單成長與涵蓋範圍（原話："Orders grew 16% organically with broad-based demand"）
- 2026-07-23｜Vimal Kapur (CEO)｜guidance：中東假設情境（原話："we are assuming the situation remains as it is today"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：管理層認為仍有超越上修財測空間（原話："I also think there is more room"）
- 2026-07-23｜Mike Stepniak (CFO)｜guidance：IA 第四季 segment margin 目標（原話："Pete will deliver a 22% margin rate in the fourth quarter"）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：PA&T 第二季 margin 下滑口徑（原話："margin contracted 180 basis points to 22.1%"）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：第二季稅率造成 EPS 逆風（原話："tax rate drove a $0.16 headwind"）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：呆滯成本（stranded cost）較投資人日預期少約 2000 萬（原話："This is about $20 million better right now."）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：價格第二季漲幅（原話："Price was about 3.5%, 3.7% for the second quarter."）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：通膨黏性、價格僅涵蓋通膨（原話："but inflation is stubborn"）
- 2026-07-23｜Mike Stepniak (CFO)｜margin：整併重組費用全年估計（原話："around that $100 million, $110 million"）
- 2026-07-23｜Vimal Kapur (CEO)｜margin：60bp/年營運面利潤率擴張的組成（原話："we expect to drive 60 basis points a year of operational"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：三年承諾信心（原話："highly confident in our ability to deliver on our 3-year"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：三年 EPS 目標（原話："Collectively, this will drive approximately $12 of adjusted"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：現金轉換率目標（原話："we expect to improve our conversion to over 90%"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：2026 年先償債（原話："we are very focused to retire our debt"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：12 美元 EPS 不含併購（原話："There's not even single M&A assumed"）
- 2026-07-23｜Vimal Kapur (CEO)｜commitment：軟體 ARR 2026 成長目標（原話："about 15% for 2026"）
- 2026-07-23｜Vimal Kapur (CEO)｜capital_allocation：JM Catalyst 收購倍數與綜效假設（原話："13x EBITDA with cost synergies, no sales synergies"）
- 2026-07-23｜Vimal Kapur (CEO)｜capital_allocation：Quantinuum 持股後續說明時程（原話："more color on our plans of our 47% ownership stake"）
- 2026-07-23｜Vimal Kapur (CEO)｜capital_allocation：M&A 第一優先為 IA 感測與量測（原話："strengthening our industrial automation, sensing"）
- 2026-07-23｜Vimal Kapur (CEO)｜customer：資料中心於 Building Automation 的占比（原話："that's 5% of the Building Automation business"）
- 2026-07-23｜Vimal Kapur (CEO)｜customer：資料中心現場發電商機尚未進訂單（原話："None of that is into our orders even yet"）
- 2026-07-23｜Mike Stepniak (CFO)｜customer：LNG 設備產能已被預訂（原話："we're sold out LNG for the next 3 years"）
- 2026-07-23｜Vimal Kapur (CEO)｜customer：中東以外專案增加（原話："We absolutely are seeing projects coming in."）
- 2026-07-23｜Vimal Kapur (CEO)｜product：IA 交貨準時率改善（原話："we were in mid-40s"）
- 2026-07-23｜Vimal Kapur (CEO)｜product：Forge 軟體 ARR 規模（原話："We are going to inch from about $900 million"）
- 2026-07-23｜Vimal Kapur (CEO)｜competition：對 BA 高個位數成長持續性的謹慎理由（原話："we are always cautious given competition can respond to"）
- 2026-07-23｜Vimal Kapur (CEO)｜risk：中東收款問題（原話："we observed some collection issues in pockets"）
- 2026-07-23｜Vimal Kapur (CEO)｜risk：BA 財測內含審慎成分（原話："there is a level of prudence"）

### HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md
- 2026-06-11｜Vimal Kapur｜guidance：三年有機成長承諾 4%–6%，並內建緩衝（原話："4% to 6% organic growth. We do have a contingency"）
- 2026-06-11｜Vimal Kapur｜guidance：IA 與 PA&T 中個位數、建築中到高個位數成長（原話："high single-digit growth is absolutely going to happen"）
- 2026-06-11｜Vimal Kapur｜guidance：市場約 3.5% 成長，公司目標高於市場 4%–6%（原話："Now we want to grow 4% to 6%"）
- 2026-06-11｜Mike Stepniak｜guidance：承諾 2029 年前 EPS 年增 10% 以上（原話："committing to delivering 10% plus EPS growth through 2029"）
- 2026-06-11｜Mike Stepniak｜guidance：2029 年 EPS 約 $6，稱為基本門檻（原話："the $6 EPS in 2029 of 10% drop, this is table stakes"）
- 2026-06-11｜Mike Stepniak｜guidance：2026 年 EPS $4.05 仍有超越空間（原話："the $4.05 for this year, there's still a lot of opportunity"）
- 2026-06-11｜Mike Stepniak｜guidance：明年 EPS 成長目標 12% 以上（原話："super disappointed in next year if we don't grow EPS by 12%"）
- 2026-06-11｜Mike Stepniak｜guidance：成長框架：量每年 4%（原話："we should grow 4% a year"）
- 2026-06-11｜Mike Stepniak｜guidance：定價三年內 3% 以上（原話："confident we'll deliver 3% plus pricing"）
- 2026-06-11｜Mike Stepniak｜guidance：併購貢獻約 1% 增量成長（原話："M&A will drive 1% incremental growth"）
- 2026-06-11｜Mike Stepniak｜guidance：保留大額緩衝因地緣風險頻繁（原話："we have a 100-year flood about every 6 months"）
- 2026-06-11｜Mike Stepniak｜guidance：確認隱含量成長約 2%、定價約 3%，並稱為超越空間（原話："that's really where the opportunity is for us to overdrive"）
- 2026-06-11｜Vimal Kapur｜guidance：定價 2026–27 年預期在 3%–4% 區間，並設 2% 緩衝（原話："why we show the hedge of 2%, right?"）
- 2026-06-11｜Mark Macaluso｜guidance：IR 描述 PA&T 下半年成長轉折至高個位數（原話："inflection in the back half to sort of high single-digit"）
- 2026-06-11｜Kenneth West｜guidance：PA&T 近幾季訂單出貨比高於 1.2（原話："higher than 1.2 book to bills over the past few quarters"）
- 2026-06-11｜Mike Stepniak｜guidance：催化劑短期需求下半年較上半年增逾 20%（原話："catalyst short-term demand is going to be up more than 20%"）
- 2026-06-11｜Mike Stepniak｜guidance：LNG 業務未來三年已售罄（原話："Our LNG business is sold out for the next 3 years"）
- 2026-06-11｜Billal Hammoud｜guidance：建築自動化 2025 年成長 8%、營收 74 億美元（原話："grow our top line by 8% to $7.4 billion"）
- 2026-06-11｜Billal Hammoud｜guidance：建築自動化展望為高個位數成長（原話："this business to grow at high single digits"）
- 2026-06-11｜Peter Lau｜guidance：IA 稱下半年與 2027 年看法樂觀、成長非後段集中（原話："I feel very bullish about the second half of 2026 and 2027"）
- 2026-06-11｜Peter Lau｜guidance：IA 三年營收中個位數成長（原話："this business is going to grow mid-single digits"）
- 2026-06-11｜Vimal Kapur｜guidance：服務與軟體 ARR 以約 15% 成長，基期約 10 億美元（原話："the ARR growth of 15% from a base of about $1 billion"）
- 2026-06-11｜Billal Hammoud｜margin：建築自動化 2025 年利潤率與三年目標 29%（原話："We see that going to 29% over the next 3 years"）
- 2026-06-11｜Billal Hammoud｜margin：建築自動化稱不需新建廠房即可支應成長（原話："without having to build a single factory"）
- 2026-06-11｜Billal Hammoud｜margin：定價與生產力持續高於通膨與投資（原話："productivity always exceeding inflation and investment"）
- 2026-06-11｜Peter Lau｜margin：IA 三年 segment margin 擴張 500 bps（原話："500 basis points of segment margin expansion"）
- 2026-06-11｜Peter Lau｜margin：對 500 bps 擴張的把握程度（原話："the margin expansion of 500 basis points, I go as far as a"）
- 2026-06-11｜Peter Lau｜margin：IA 利潤擴張僅靠低個位數成長即可（原話："feel like we could do that at low single-digit growth"）
- 2026-06-11｜Mike Stepniak｜margin：IA 重整使公司未來 12 個月貢獻 100 bps 利潤率（原話："going to deliver 100 bps of margin expansion for Honeywell"）
- 2026-06-11｜Mike Stepniak｜margin：2026 年 segment margin 約 20%（原話："we'll deliver about 20% segment margin this year"）
- 2026-06-11｜Mike Stepniak｜margin：結構性行動未來 12 個月擴張約 200 bps（原話："expand about 200 bps over the next 12 months"）
- 2026-06-11｜Mike Stepniak｜margin：有機每年再擴張 60 bps（原話："we'll expand another 60 bps a year"）
- 2026-06-11｜Mike Stepniak｜margin：24% 目標被稱為可超越（原話："24% is not only achievable, it's actually beatable"）
- 2026-06-11｜Mike Stepniak｜margin：滯留成本剩 2.9 億美元（原話："our stranded cost is only $290 million"）
- 2026-06-11｜Mike Stepniak｜margin：約 2 億美元滯留成本已啟動措施，待反映於 run rate（原話："actioned about $200 million of that through repositioning"）
- 2026-06-11｜Mike Stepniak｜margin：法人實體由約 700 個減至 300 個（原話："Over the next 2 years, we'll eliminate 400 legal entities"）
- 2026-06-11｜Mike Stepniak｜margin：ERP 由約 10 套整併為 2 套（原話："Today, we still have about 10 ERPs"）
- 2026-06-11｜Mike Stepniak｜margin：共享服務滲透率由約 40% 升至逾 70%（原話："our shared services penetration is about 40%"）
- 2026-06-11｜Mike Stepniak｜margin：固定成本占比 2025 至 2027 下降 500–600 bps（原話："is going down by about 500 to 600 bps from '25 to '27"）
- 2026-06-11｜Vimal Kapur｜margin：固定成本已降近 600 bps，目標維持 31%（原話："Now our job is to keep it at 31%"）
- 2026-06-11｜Mike Stepniak｜margin：利潤擴張不依賴強勁營收成長（原話："expansion is not dependent on the strong top line growth"）
- 2026-06-11｜Mike Stepniak｜margin：稱利潤擴張大致已去風險（原話："the margin expansion is largely derisked"）
- 2026-06-11｜Mike Stepniak｜margin：軟體增量利潤高，Forge 投入已減少（原話："We invested $1 billion in Forge"）
- 2026-06-11｜Vimal Kapur｜margin：PA&T 納入 Johnson Matthey 使基期利潤率偏低（原話："the Johnson Matthey acquisition. It pulls our margins down"）
- 2026-06-11｜Mike Stepniak｜margin：口徑：服務與軟體約 70 億美元占 40%，軟體 ARR 約 9 億美元（原話："software ARR is about $900 million"）
- 2026-06-11｜Vimal Kapur｜margin：口徑：軟體 ARR 以開立發票金額定義（原話："just report ARR, which is what we invoice"）
- 2026-06-11｜Jim Masso｜margin：口徑：PA 單一事業服務與軟體約 10 億美元 ARR（與 Vimal 全公司 10 億美元說法並陳）（原話："got around $1 billion of ARR"）
- 2026-06-11｜Vimal Kapur｜margin：口徑：vitality 定義為近三年新產品占比（原話："defined as products you created over the last 3 years"）
- 2026-06-11｜Peter Lau｜margin：口徑：IA 同時以淨新品 NPI 衡量，vitality 較大（原話："we measure it not just in vitality, but in net new"）
- 2026-06-11｜Vimal Kapur｜product：vitality 升至 40% 中段（原話："our vitality has been progressively growing to mid-40s"）
- 2026-06-11｜Vimal Kapur｜product：R&D 已提高約 50 bps，不再需要更多調整（原話："We are at the point we like it to be"）
- 2026-06-11｜Billal Hammoud｜product：2025 年 8% 成長中 4.5 個百分點來自新品（原話："4.5% came from new product introduction"）
- 2026-06-11｜Vimal Kapur｜product：連網資產 520 萬，預計 2028 年達 900 萬（原話："it will be 9 million conservatively by 2028"）
- 2026-06-11｜Kenneth West｜product：PA 系統連網比例僅 14%（原話："Only 14% of our systems are connecting"）
- 2026-06-11｜Vimal Kapur｜product：服務與軟體占營收由 40% 提高到 45%（原話："we want our services and software revenue to grow to 45%"）
- 2026-06-11｜Mike Stepniak｜product：軟體成長速度約為其餘業務 3 倍（原話："software is going to grow at about 3x the rest of the"）
- 2026-06-11｜Peter Lau｜product：IA 三年 R&D 再增 15%–20%（原話："we're going to do another 15% to 20%"）
- 2026-06-11｜Suresh Venkatarayalu｜product：CLSS 軟體組合 1.3 億美元，ARR 4,000 萬美元（原話："$130 million software portfolio with $40 million ARR"）
- 2026-06-11｜Billal Hammoud｜competition：建築產品組合以消防與安防為主，與 HVAC 設備商重疊較少（原話："Fire and Security being over 2/3 of what we sell"）
- 2026-06-11｜Peter Lau｜competition：IA 同業比較對象為 AMETEK、Teledyne、IDEXX 類（原話："AMETEK, Teledyne and IDEXX"）
- 2026-06-11｜Peter Lau｜competition：IA 無單一公司在所有領域競爭（原話："company that we compete with in every place that we play"）
- 2026-06-11｜Peter Lau｜competition：IA 過去四年份額流失（原話："As a result, we lost share."）
- 2026-06-11｜Vimal Kapur｜competition：工業與流程自動化自認前三、目標第一（原話："honest admission, we are top 3"）
- 2026-06-11｜Kenneth West｜competition：稱不陷入價格戰、較早切入專案（原話："We're not getting into a price war"）
- 2026-06-11｜Jim Masso｜competition：AI 與新軟體正在顛覆許多企業，公司稱其強化自身（原話："a lot of businesses are being disrupted by a lot"）
- 2026-06-11｜Vimal Kapur｜competition：離散自動化控制層目前未參與，保持彈性（原話："today, our position is open at this point"）
- 2026-06-11｜Billal Hammoud｜customer：建築自動化資料中心占比由 4% 升至 5% 以上（原話："And as we sit here it's operating well above 5%"）
- 2026-06-11｜Jim Masso｜customer：生命科學營收約 6 億美元（原話："around $600 million of revenue"）
- 2026-06-11｜Kenneth West｜customer：Dangote 將自動化合約由他人轉給公司（原話："he took contracts away from others for the automation side"）
- 2026-06-11｜Suresh Venkatarayalu｜customer：NVIDIA 園區試點客戶再給六週評估（原話："they've given us 6 more weeks"）
- 2026-06-11｜Billal Hammoud｜customer：通路占建築銷售逾 60%（原話："Our channels represent over 60% of our sales"）
- 2026-06-11｜Vimal Kapur｜customer：Forge 開放給通路夥伴，收取授權費（原話："When they sell it, they have to pay me a license fee"）
- 2026-06-11｜Vimal Kapur｜customer：跨事業交叉銷售未計入現有數字（原話："cross-sell built in because we haven't proven anything"）
- 2026-06-11｜Vimal Kapur｜customer：交叉銷售可能再貢獻 200 bps 成長（原話："200 basis point of growth in there is possible? Absolutely"）
- 2026-06-11｜Peter Lau｜customer：為提升客戶交付願多備庫存 2,000 萬美元（原話："putting in $20 million of extra inventory"）
- 2026-06-11｜Kenneth West｜risk：中東設施受衝擊，公司預期參與重建（原話："facilities across the Middle East that are our technology"）
- 2026-06-11｜Mike Stepniak｜risk：上半年自由現金流受中東衝突影響（原話："also the conflict in Middle East"）
- 2026-06-11｜Peter Lau｜risk：承認對 IA 轉型存在懷疑（原話："I wouldn't disagree with any skepticism"）
- 2026-06-11｜Vimal Kapur｜risk：客戶導入需組織調整，影響擴張速度（原話："our scaling is more dependent upon customer adoption"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：目標槓桿率年底前低於 3（原話："leverage ratio to below 3, hopefully by year-end"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：CapEx 約占營收 3%（原話："Our CapEx should be about 3% of sales"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：股利支付率約 35%（原話："Our dividend payout ratio should be about 35%"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：股數每年減少約 1%（原話："we'll focus on about 1% share count reduction"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：補強型併購規模 20–40 億美元（原話："bolt-on is about $2 billion to $4 billion"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：維持補強併購策略，2027 年前以降債為先（原話："stay on the bolt-on strategy in the optimal size"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：不改變以補強併購為主的策略，不排除任何選項（原話："you never say no to everything"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：下半年自由現金流轉換率逾 95%（原話："We will be 95-plus percent converter in"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：往後自由現金流轉換率約 95%（原話："convinced we are 95% free cash flow converter going forward"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：稅率降至約 19%（原話："tax rate going forward is about 19%"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：Quantinuum 持股帳面價值約 70 億美元（原話："is going to sit on our books at $7"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：適當時機再出售 Quantinuum 持股（原話："it will be the right time for us to monetize our stake"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：未來每年重整費用約 7,000–8,000 萬美元（原話："about $70 million to $80 million of repositioning"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：約 80 座工廠整併，25 座產出 80% 營收（原話："25 facilities will produce 80% of our revenue"）
- 2026-06-11｜Mike Stepniak｜capital_allocation：Process 兩事業今年商業協同效益預計逾 1 億美元（原話："will deliver over $100 million of commercial synergies"）
- 2026-06-11｜Vimal Kapur｜commitment：CEO 稱立場一致、不改變主意（原話："I stay on course. I don't change my mind"）
- 2026-06-11｜Vimal Kapur｜commitment：高階主管薪酬將與承諾連動（原話："compensation should link to what we committed to you"）
- 2026-06-11｜Mike Stepniak｜commitment：對前兩年成果最有信心，最後一年打折（原話："I always discount the last year"）
- 2026-06-11｜Mike Stepniak｜commitment：聚焦未來 18 個月（原話："So it's really about next 18 months"）
- 2026-06-11｜Kenneth West｜commitment：服務由零起算可達數億美元（原話："several hundred million dollars of services business"）
- 2026-06-11｜Vimal Kapur｜commitment：不打算讓流程事業走通路（原話："We are not moving our process"）
- 2026-06-11｜Vimal Kapur｜product：敘事：業務團隊原集中於 Connected Enterprise，後改回四個事業部（原話："It turns out that thesis was wrong"）
- 2026-06-11｜Vimal Kapur｜capital_allocation：不新增工廠，LNG 為唯一例外（原話："with one exception, LNG"）

### 問答異常語氣（迴避／改口／保留）
- HON_Q2_2026_Earnings_Call_20260723.md｜問：Deane Dray 問 JM Catalyst 重新議價降價的情境｜答法：未說明降價原因，稱屬正常談判並表示不想多談，轉而講策略與倍數
- HON_Q2_2026_Earnings_Call_20260723.md｜問：Alexander Virgo 問催化劑量下滑對 margin 的影響幅度及下半年反彈幅度｜答法：未給數字，只說明下半年量較正常及單季 mix 不可預測
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Sprague：已連網並有 ARR 的裝機基礎對有機成長貢獻幾個百分點｜答法：Ken West 以觸媒數位影像、PDH 客戶為例回答，未給成長點數
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Mitchell：IA 準時交貨等營運 KPI 改善速度｜答法：Pete Lau 談客戶滿意與庫存投入，稱以自由現金流利潤率、營業利潤與成長自評，未給 KPI 改善速率
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Coe：ARR 與經常性服務的增量利潤率、PA&T 2029 利潤率為何只到 25%｜答法：Mike 稱軟體增量利潤『really high』未給數字；PA&T 25% 由 Vimal 以 Johnson Matthey 基期作答
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Sprague：離散自動化與野戰儀器空白的策略優先順序｜答法：Vimal 談 IA 補強、垂直型併購與前沿技術，未回應離散自動化
- HON_Analyst_Investor_Day_Honeywell_International_Inc_20260611.md｜問：Linzey：AI 在自家工廠與營運的效益大小｜答法：Vimal 稱『hard for us to put a number on the table』，只說大於預期且高於 0

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
{"date":"20260724","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"PA&T「sharp inflection」是真實結構拐點，非一次性 backlog 錯位","columns":{"2Y 驗證點":"H2 2026 有機營收加速至高個位數","5Y 驗證點":"PA&T 5Y 有機 CAGR ≥ 中個位數，LNG/催化劑 backlog 持續轉換","10Y 驗證點":"能源轉型（renewable fuels/氫）成第二成長腿","具體數字門檻":"PA&T 訂單 +24-25%、BtB &gt;1.2x、LNG 專有設備「賣光 3 年」","來源":"2Y 假設：連 2 季 TTM 偏離 ≥5% → 削弱"}},{"id":"H2","text":"Building Automation 高個位數成長可持續（7 季連續）","columns":{"2Y 驗證點":"資料中心/醫療/hospitality 高成長 vertical 驅動 BA ≥ 中高個位數有機","5Y 驗證點":"BA 佔比提升 + 服務/軟體 ARR 拉高整體 margin","10Y 驗證點":"Niagara/BMS 平台成資料中心/樓宇標準","具體數字門檻":"Q2 BA +9% 有機、訂單 +13%、高成長 vertical 訂單 +50%、margin 27.1%","來源":"連 2 季 BA 有機 &lt; 中個位數 → 削弱"}},{"id":"H3","text":"純自動化重估：市場給 pure-play 自動化倍數（vs 舊 conglomerate 折價）","columns":{"2Y 驗證點":"Fwd PE 站穩 ~25x（peer 中段）而非回落至 conglomerate 18-20x","5Y 驗證點":"3 年 EPS target（~$12 by 2029）兌現支撐倍數","10Y 驗證點":"ROIC/margin 結構性上台階（exit &gt;22% → 24% target）","具體數字門檻":"賣方目標價中位 ≈ $247、Buy 評級;段 margin +90-100bps","來源":"連 4 季 EPS 共識下修 或 PE 回落 conglomerate 檔 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"PA&T H2 拐點跳票（catalyst 出貨/backlog 轉換慢於承諾）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"PA&T 有機營收 QoQ/YoY","警戒閾值":"Q3 未轉正、連 2 季 &lt; 低個位數 → 減觀望信心"}},{"id":"R2","text":"Industrial Automation turnaround 失敗、EMR/ROK 續侵蝕份額","columns":{"對應假設":"H1/H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"IA 有機成長 + 交付績效 %","警戒閾值":"交付績效自 ~80% 回落、有機成長轉負 → moat_trend 降 ↓"}},{"id":"R3","text":"能源 capex 見頂 + 中東地緣升級 + renewable fuels 政策逆風（45Z）","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"油氣資本開支週期 + 中東 collection + 45Z CI 計分規則落地","警戒閾值":"油氣 capex 下行 + 中東惡化 或 45Z 持續不確定使 renewable fuels 催化劑延後 → 需 ≥50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔至 Fwd PE ≤22x FY27（約 $218）或 PA&T Q3/Q4 營收確認高個位數拐點兌現（backlog 轉換 + catalyst 出貨回升）","irr_base_pct":8.0,"ev5y_pct":29.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.8,"ev5y_pct":29.0,"irr_base_pct":8.0,"max_dd_pct":-42.0,"bull_5y_price":416.0,"bear_5y_price":185.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"回檔至 Fwd PE ≤22x FY27（約 $218）或 PA&T Q3/Q4 營收確認高個位數拐點兌現（backlog 轉換 + catalyst 出貨回升）","price_at_dd":246.27,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
