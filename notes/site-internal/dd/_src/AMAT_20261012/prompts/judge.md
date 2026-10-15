你是 stock-analyst **v20 判斷 agent**，標的 AMAT（20261012）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
  *eps
    *bull[]: arr ≥1 num
    *base[]: arr ≥1 num
    *bear[]: arr ≥1 num
  *pe
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
{"meta":{"ticker":"AMAT","date":"2026-10-12","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMAT_20261012/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMAT_20261012/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_revenue_gaap","label":"Revenue (GAAP)","value":9115,"period":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","citation":"公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release（經 mfn.se 轉載全文取數）"},"note":"未查得共識營收，省略"},{"id":"f_kpi1_non_gaap_operating_margi","label":"Non-GAAP operating margin","value":34.0,"period":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","citation":"公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；Non-GAAP 營業利益 $3,096M"},"note":"未查得共識，省略"},{"id":"f_kpi2_gaap_operating_margin","label":"GAAP operating margin","value":33.7,"period":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","citation":"公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；GAAP 營業利益 $3,075M"},"note":"n/a"},{"id":"f_kpi3_non_gaap_free_cash_flow","label":"Non-GAAP free cash flow","value":2330,"period":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","citation":"公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；營運現金流 $3,037M、資本支出 $707M；FCF 占營收約 25.6%"},"note":"n/a"},{"id":"f_kpi4_share_based_compensation","label":"Share-based compensation","value":169,"period":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","citation":"公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；占營收約 1.85%、占 GAAP 營業利益約 5.5%（自算）"},"note":"n/a"},{"id":"f_kpi5_guidance_q4_fy2026_reven","label":"Guidance: Q4 FY2026 revenue","value":"10,250 ± 500","period":"Q3 FY2026 新聞稿（公告於 2026-08-13），指引對象 Q4 FY2026","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 FY2026 新聞稿（公告於 2026-08-13），指引對象 Q4 FY2026","citation":"公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release"},"note":"未查得共識，省略"},{"id":"f_kpi6_guidance_q4_fy2026_non_g","label":"Guidance: Q4 FY2026 non-GAAP diluted EPS","value":"4.02 ± 0.20","period":"Q3 FY2026 新聞稿（公告於 2026-08-13），指引對象 Q4 FY2026","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 FY2026 新聞稿（公告於 2026-08-13），指引對象 Q4 FY2026","citation":"公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；含 $0.01 SBC 正常化稅務利益與 $0.05 集團內無形資產移轉淨稅務利益"},"note":"未查得共識，省略"},{"id":"f_kpi7_contract_liabilities_bac","label":"Contract liabilities (backlog 替代指標)","value":3271,"period":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）","citation":"公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；新聞稿未揭露 backlog、book-to-bill、產能利用率，此為最接近的指標"},"note":"n/a"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-13","period":"2026-08-13","unit":"date","basis":"距今 42 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-13"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_amat_gross_margin_pct","label":"AMAT 毛利率","value":49.4,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amat_operating_margin_pct","label":"AMAT 營業利益率","value":31.09,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amat_fcf_margin_pct","label":"AMAT FCF 利潤率","value":18.23,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_2330_tw_gross_margin_pct","label":"2330.TW 毛利率","value":64.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_operating_margin_pct","label":"2330.TW 營業利益率","value":56.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2330_tw_fcf_margin_pct","label":"2330.TW FCF 利潤率","value":25.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_asml_gross_margin_pct","label":"ASML 毛利率","value":52.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asml_operating_margin_pct","label":"ASML 營業利益率","value":35.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asml_fcf_margin_pct","label":"ASML FCF 利潤率","value":24.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":507.03,"period":"2026-10-09（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":27.21,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":54.57,"period":"2026-10-09（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.79 → 12.79）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.11,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（18.45 → 18.47）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.6 → 23.6）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":12.79,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":18.47,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":23.6,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":4.32,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 12.26 → 12.79（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":43.75,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":13.05,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":12.99,"period":"2026-10-09（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-09（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-09（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-09（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":39.64,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 12.79，分子＝快照價 507.03","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.391,"period":"2026-10-12","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-12"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Castellano 通訊稿標題主張 AMAT 於 2025 年在多個關鍵設備區段失去份額（全文付費牆，僅見摘要；Lam、KLA、ASML 在各自 SAM 擴大）","source":"Dr. Robert Castellano's Semiconductor Deep Dive Newsletter - Applied Materials lost share across","url":"https://drrobertcastellano.substack.com/p/applied-materials-lost-share-across","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Mizuho 2025 年 9 月降評至 Neutral：中國本土 OEM（Naura、AMEC）在 PVD、成熟 28nm 蝕刻與電漿 CVD 持續拿份額","source":"Finviz news - Applied Materials (AMAT) stock downgraded to neutral as competition rises in China; Barron's 同一報告","url":"https://finviz.com/news/167978/applied-materials-amat-stock-downgraded-to-neutral-as-competition-rises-in-china","excerpt":null,"as_of":"2025-09-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Reuters 經 247WallSt 轉述：中國要求晶圓廠新增產能至少 50% 使用國產設備，有利 Naura、AMEC","source":"247wallst - Applied Materials' China Problem Is Getting Worse","url":"https://247wallst.com/investing/2026/08/26/applied-materials-china-problem-is-getting-worse/","excerpt":null,"as_of":"2026-08-26","retrieved_at":"20261012","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"AMAT FY2025 10-K 風險揭露：中國本土設備商因地方政府誘因與出口管制，競爭可能加劇","source":"SEC EDGAR AMAT FY2025 10-K","url":"https://www.sec.gov/Archives/edgar/data/6951/000162828025056742/amat-20251026.htm","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261012","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"AMAT 法說稱預期在先進邏輯 GAA 與配線（含背面供電）served market 取得逾 50% 份額；Q1 2026 稱競爭態勢穩定","source":"AMAT Q4 FY2025 / Q1 FY2026 earnings call (alpha-sense / allmind 摘要)","url":"https://allmind.ai/earnings/event/bt_AMAT_2026_Q1","excerpt":null,"as_of":"2026-02-12","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"UBS 預期 AMAT 受益產品組合與 DRAM 需求，未來兩年有機會奪回部分份額；Lam 在 DRAM／NAND 導體蝕刻取得多家客戶","source":"UBS via itiger - Applied Materials to Reap Benefits of Upcoming Demand Surge for DRAM WFE","url":"https://www.itiger.com/news/2586472274","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"中國晶圓廠使用國產設備占比 2025 年達 35%（2024 年 25%），蝕刻與薄膜沉積等關鍵製程替代率據報逾 40%；屬客戶端導入國產第二來源的產業層證據，未點名 AMAT 客戶。","source":"TrendForce News 2026-01-12 China's domestic chip equipment adoption beats 2025 target at 35%","url":"https://www.trendforce.com/news/2026/01/12/news-chinas-domestic-chip-equipment-adoption-beats-2025-target-at-35-led-by-naura-amec/","excerpt":null,"as_of":"2026-01-12","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"AMEC 5nm 蝕刻機據報已進入 TSMC 先進製程產線驗證；中國監管據報要求新增產能設備至少 50% 採國產。","source":"TrendForce News 2026（搜尋摘要，未取得原文）","url":"https://www.trendforce.com/news/2026/01/12/news-chinas-domestic-chip-equipment-adoption-beats-2025-target-at-35/","excerpt":null,"as_of":"2026-01-12","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"0","claim":"第三方摘要稱 AMAT 財年 2025 兩家客戶各占淨營收約 19% 與 15%，約 89% 營收來自美國以外（中國、台灣、韓國為主）；需對照 10-K 原文。","source":"搜尋摘要引第三方對 FY2025 10-K 的整理","url":"https://dcf-analysis.com/products/amat-porters-five-forces-analysis","excerpt":"roughly 89% of fiscal 2025 net revenue came from customers outside the U.S., with the majority of products and services delivered to China, Taiwan and Korea, and two customers alone made up about 19% and 15% of net revenue","as_of":"2025-12-01","retrieved_at":"20261012","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：兩家客戶分別占淨營收約 19% 與 15%（FY2024 為約 12% 與 11%）；客戶未具名。","source":"Applied Materials Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/6951/000162828025056742/amat-20251026.htm","excerpt":"During fiscal 2025, two customers accounted for approximately 19% and 15%, respectively, of our net revenue.","as_of":"2025-12-01","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2025 約 89% 淨營收來自美國以外客戶；中國約 30%（約 85.3 億美元，二手來源）。","source":"Applied Materials Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/6951/000162828025056742/amat-20251026.htm","excerpt":"Approximately 89% of Applied Materials' fiscal 2025 net revenue was to customers outside the U.S.","as_of":"2025-12-01","retrieved_at":"20261012","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 2025-12 預測：總設備銷售 2026 $145B、2027 $156B；成長主要來自 AI 相關支出，中國產能擴建亦有貢獻。","source":"SEMI press release: Global Semiconductor Equipment Sales Projected to Reach a Record of $156 Billion in 2027","url":"https://semi.org/en/semi-press-release/global-semiconductor-equipment-sales-projected-to-reach-a-record-of-156-billion-dollars-in-2027-semi-reports","excerpt":null,"as_of":"2025-12-16","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"SEMI 2026-04：300mm 晶圓廠設備支出 2027 年首度突破 $150B；2027–2029 記憶體設備支出累計 $175B（DRAM $111B、3D NAND $62B），邏輯/微元件 $228B；SEMI 稱持續高投資應有助緩衝傳統記憶體週期下行。","source":"SEMI press release: SEMI Projects Double-Digit Growth in Global 300mm Fab Equipment Spending for 2026 and 2027","url":"https://www.semi.org/en/semi-press-release/semi-projects-double-digit-growth-in-global-300mm-fab-equipment-spending-for-2026-and-2027","excerpt":null,"as_of":"2026-04-01","retrieved_at":"20261012","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2026年2月，AMAT 與美國商務部 BIS 就 2020年11月至2022年7月對中國客戶出貨未遵守出口管制規定達成和解，支付 2.525 億美元；此為出口管制事項，非反壟斷。","source":"Applied Materials press release: Applied Materials Reaches Resolution with the U.S. Department of Commerce","url":"https://www.appliedmaterials.com/us/en/newsroom/press-releases/021126-applied-materials-reaches-resolution-us-department-commerce.html","excerpt":"Applied Materials, Inc. today announced that it has reached a settlement agreement with the U.S. Department of Commerce, Bureau of Industry and Security (BIS).","as_of":"2026-02-11","retrieved_at":"20261012","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"美國司法部與 SEC 已通知 AMAT 結案相關調查、未採取行動；和解要求內部出口管制稽核與合規訓練。後續 10-Q（2026年7月）載明款項已於 FY2026 第二季付清。","source":"Applied Materials press release 2026-02-11; Form 10-Q for quarter ended 2026-07-26","url":"https://www.sec.gov/Archives/edgar/data/0000006951/000162828026058235/amat-20260726.htm","excerpt":"The U.S. Department of Justice (DOJ) and the U.S. Securities and Exchange Commission (SEC) have notified Applied that they have closed their related investigations without action.","as_of":"2026-02-11","retrieved_at":"20261012","affects":["thesis.R","triggers"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2025年10月美國商務部將出口黑名單擴及列管公司的多數持股子公司；AMAT 預告此規則將使 FY2026 營收減少約 6 億美元，其中 FY Q4 約 1.1 億美元。","source":"Yahoo Finance／Reuters: Applied Materials flags $600 million revenue hit in 2026 on broader chip export curbs","url":"https://finance.yahoo.com/news/applied-materials-flags-600-million-224151556.html","excerpt":"Applied Materials said the change would make it more difficult to export some products and supply specific parts and services to select China-based customers without a license. It forecast a $600 million hit to fiscal 2026 revenue, and expects an impact of about $110 million on fourth-quarter revenue.","as_of":"2025-10-01","retrieved_at":"20261012","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"該 affiliates 規則在美中領袖會談後暫停；管理層稱全年約 6 億美元銷售得以恢復，1.1 億美元延遲出貨將於至 1 月的三個月內出貨並已納入預測（次級報導，需以公司財報材料核對）。","source":"Yahoo Finance: Applied Materials forecasts strong quarterly (search summary, KuCoin/Yahoo)","url":"https://www.kucoin.com/news/flash/applied-materials-faces-600m-revenue-hit-from-china-export-controls","excerpt":"That affiliate rule was suspended after talks between U.S. President Donald Trump and Chinese President Xi Jinping. Executives said the suspension will re-enable about $600 million in sales for the full fiscal year.","as_of":"2025-11-13","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"2026年2月報導 AMAT 就向中芯國際（SMIC）違規出口晶片設備達成約 2.52 億美元和解／罰款；設備經南韓子公司轉運，SMIC 於 2020年12月被列入實體清單之後出貨開始。","source":"TrendForce News: US reportedly hits Applied Materials with $252M penalty for illegally sending chip equipment to SMIC","url":"https://www.trendforce.com/news/2026/02/12/news-us-reportedly-hits-applied-materials-with-252m-penalty-for-illegally-sending-chip-equipment-to-smic/","excerpt":"SMIC's shipments reportedly began after the U.S. Commerce Department added SMIC to its \"Entity List\" in December 2020.","as_of":"2026-02-12","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026年1月14日公告對特定先進半導體及衍生品課 25% 第232條關稅（1/15 生效），涵蓋範圍文字含半導體製造設備；豁免含美國資料中心、研發、新創、維修等用途；後續可能擴大並配套關稅抵減計畫。未找到說明 AMAT 設備是否被課徵之來源。","source":"White & Case: President Trump orders narrowly targeted 25% Section 232 tariff on certain advanced semiconductor articles","url":"https://www.whitecase.com/insight-alert/president-trump-orders-narrowly-targeted-25-section-232-tariff-certain-advanced","excerpt":"Any potential future tariffs would include a tariff offset program for companies investing in US semiconductor manufacturing capacity.","as_of":"2026-01-15","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國占 AMAT 營收比重：聚合站稱 FY Q3 中國營收 25.1 億美元、占 28%（去年同期 35%）；CFO 稱限制影響相當於 FY2024 中國市場約 10%、FY2025 逾兩倍（次級聚合來源，未核對公司申報）。","source":"Yahoo Finance／Reuters 摘要: Applied Materials sees weaker China spending in 2026 on tighter US curbs","url":"https://finance.yahoo.com/news/applied-materials-forecasts-strong-quarterly-210625673.html","excerpt":null,"as_of":"2025-11-13","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"公司稱美國出口管制預計使 FY2026 營收減少約 6 億美元（Q4 減 1.1 億）；另有報導引述 7.1 億美元口徑","source":"Reuters 經 Yahoo Finance：Applied Materials sees weaker China spending in 2026 on tighter US curbs","url":"https://finance.yahoo.com/news/applied-materials-forecasts-strong-quarterly-210625673.html","excerpt":"The new rules are expected to reduce Applied Materials' fourth-quarter revenue by $110 million and 2026 revenue by $600 million","as_of":"2025-11-13","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"中國營收占比由近 40% 降至 20% 中段；CEO 指非美系設備商不受同等限制，受限客戶可轉向對手（日期為推定，原文發布日未於摘要中確認）","source":"Reuters 經 Korea JoongAng Daily：Applied Materials sees weaker China spending in 2026 on tighter US curbs","url":"https://www.koreajoongangdaily.com/world/applied-materials-sees-weaker-china-spending-in-2026-on-tighter-us-curbs/12050111","excerpt":"Non-U.S. equipment companies don't have the same restrictions, and so restricted customers can buy from those companies, even if they would rather buy from Applied,","as_of":"2025-11-13","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"FQ3 2026（2026-08-13 公布）半導體系統營收約 $7.04B，年增 27%，營業利益率 37.7%（前年同期 33%）；其中 DRAM（含 HBM 封裝）年增 52%。","source":"Futurum：Applied Materials Q3 FY 2026: Advanced Packaging and DRAM Accelerate Growth","url":"https://futurumgroup.com/insights/applied-materials-q3-fy-2026-advanced-packaging-and-dram-accelerate-growth/","excerpt":"Semiconductor Systems revenue was $7.04 billion, up 27% YoY.","as_of":"2026-08-13","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"FQ3 2026 AGS 營收約 $1.78B 年增 22%，營業利益率 30.1%；Other（主要為 Display）$294M，去年同期 $275M。","source":"Futurum / Zacks 對 AMAT FQ3 2026 財報之整理","url":"https://futurumgroup.com/insights/applied-materials-q3-fy-2026-advanced-packaging-and-dram-accelerate-growth/","excerpt":"Other revenue was $294 million (Q3 FY 2025: $275 million).","as_of":"2026-08-13","retrieved_at":"20261012","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"FQ4 2026 指引：總營收 $10.25B ±$0.5B；半導體系統約 $7.9B、AGS 約 $1.84B、Other 約 $510M。","source":"247WallSt：Applied Materials Q3 2026: Record Revenue With a $10.25B Q4 Outlook","url":"https://247wallst.com/cards/applied-materials-q3-2026-earnings-amat-01kzybvthd5qqamwrtqk59k25x","excerpt":null,"as_of":"2026-08-13","retrieved_at":"20261012","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"AMAT 稱先進邏輯／代工、DRAM、先進封裝貢獻 2026 年 WFE 年增量的 80% 以上，2027 年結構類似；Citi 指 NAND 仍處長期下行。","source":"Nasdaq / Citi 2026 Global TMT Conference 摘要（Quartr）","url":"https://quartr.com/events/nova-ltd-nvmi-citi-s-2026-global-tmt-conference_FG2AxEM9","excerpt":null,"as_of":"2026-09-01","retrieved_at":"20261012","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Morgan Stanley（2026-07）將 WFE 預測上調：2027 年 $202B（原 $191B）、2028 年 $227B（原 $215B）；TechInsights 預測 2026 WFE 年增 24.5%（前一季為 9.6%）。as_of 為摘要中 MS 調升時點，TechInsights 發布日未確認。","source":"Morgan Stanley 經 itiger；TechInsights WFE Forecast","url":"https://www.itiger.com/news/2649678863","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"UBS 預估 2026 年 WFE 支出年增逾 20% 至 $136.5B，DRAM 貢獻增量逾半，並視 AMAT 為最大受惠者；AMAT 被描述為 ASML 之後第二大 DRAM 設備供應商，管理層稱過去十年 DRAM 設備份額增約 10 個百分點。","source":"MT Newswires 經 itiger：Applied Materials to Reap Benefits of Upcoming Demand Surge for DRAM WFE, UBS Says；Hudson Labs 引 FQ2 法說","url":"https://www.itiger.com/news/2586472274","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"-","claim":"中國：AMAT 中國占系統與服務營收比重 FY2025 降至 28%，預期 2026 中國 WFE 支出下降且限制無實質放寬；FQ2 FY26 中國約占營收 24%；Mizuho 預期持續流失份額，UBS 認為中國需求被低估。","source":"Nasdaq/Zacks；Hudson Labs AMAT Earnings Preview Memo","url":"https://www.hudson-labs.com/research/applied-materials-q3-2026-earnings-preview-amat-guidance-preview","excerpt":null,"as_of":"2026-08-10","retrieved_at":"20261012","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"AMAT 2026 財報新聞稿的風險因子僅泛稱新技術導入與技術轉換時點，未點名任何具體替代技術。","source":"SEC 8-K, Applied Materials Q2 FY2026 earnings release (Exhibit 99.1)","url":"https://www.sec.gov/Archives/edgar/data/0000006951/000162828026035071/exhibit991q22026earningsre.htm","excerpt":"the introduction of new and innovative technologies, and the timing of technology transitions","as_of":"2026-05-14","retrieved_at":"20261012","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"SEMI 預估 300mm 晶圓廠設備支出 2026 年成長 18% 至 1,330 億美元、2027 年再成長 14% 至 1,510 億美元；本次搜尋未找到取代現行 WFE 工具的顛覆性替代技術。","source":"SEMI 300mm fab equipment spending forecast (via EMSNow)","url":"https://www.emsnow.com/category/analysis/page/28/","excerpt":"Worldwide 300mm fab equipment spending is expected to increase 18% to $133 billion in 2026 and 14% to $151 billion in 2027","as_of":"2026-01-01","retrieved_at":"20261012","affects":["thesis.H","valuation"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Intel 18A 為其首個採 GAA 電晶體並搭配背面供電的製程，已隨 Panther Lake 出貨；TSMC 規劃 A16 導入 Super Power Rail 背面供電（製程架構轉換屬同一設備商須跟上的技術節點轉換，非取代 AMAT 產品的替代方案）。","source":"TechInsights, 2026 Compute – Process Analysis Briefing 1; All About Circuits TSMC Q&A","url":"https://www.techinsights.com/ja/node/61672","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261012","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FQ3 2026 財報電話會：AGS 營收創高 $18 億、年增 22%，由訂閱式服務成長與交易型零件需求帶動；公司預期 2026 曆年 AGS 成長逾 20%，中長期維持中雙位數年成長。未見公司明述整體轉為訂閱商業模式，僅是經常性服務基數擴大。","source":"MarketBeat, Applied Materials Q3 earnings call highlights","url":"https://www.marketbeat.com/instant-alerts/applied-materials-q3-earnings-call-highlights-2026-08-13/","excerpt":null,"as_of":"2026-08-13","retrieved_at":"20261012","affects":["moat_trend","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"EPIC Center（矽谷客戶共創研發設施）預期 2026 上半年啟用，客戶工程師（TSMC、Samsung、SK hynix、Micron、Broadcom 等）進駐共同開發；來源多為公司公告或舊分析稿，未能確認實際啟用與商業條款。","source":"Finviz, AMAT's New R&D Hub in 2026: Will EPIC Push It Ahead in Chips?","url":"https://finviz.com/news/92281/amats-new-rd-hub-in-2026-will-epic-push-it-ahead-in-chips","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261012","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"AMAT 2026-05-14 指引 FQ3 營收 $8.45B–$9.45B（前次 $7.15B–$8.15B）、non-GAAP EPS $3.16–$3.56；同期共識 EPS 約 $3.38–3.39、營收約 $9.01B，略高於指引中點（EPS ~$3.36、營收 ~$8.95B）。","source":"Benzinga AMAT earnings-forecasts; TIKR","url":"https://www.benzinga.com/quote/AMAT/earnings-forecasts","excerpt":null,"as_of":"2026-05-14","retrieved_at":"20261012","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-05 管理層稱半導體設備事業今年成長逾 30%（原約 20%）；Benzinga 統計 2022-08 至 2026-05 共 18 次指引更新，上調 9 次、下調 4 次；未查到 2026 年下調報導。","source":"Benzinga; 搜尋彙整（Dolphin Research/36Kr）","url":"https://www.benzinga.com/quote/AMAT/earnings-forecasts","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261012","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布：Investing.com 平均約 $639（高 $900／低 $358，36 位分析師；33 買、7 持有、0 賣）；Benzinga 平均 $649（25 位，24 買 1 持有）；StockAnalysis 平均 $623.06（39 位）；TIKR 平均 $619（35 位）。各來源 as-of 不一。","source":"Investing.com AMAT consensus estimates; Benzinga; StockAnalysis; TIKR","url":"https://www.investing.com/equities/applied-matls-inc-consensus-estimates","excerpt":null,"as_of":"2026-09-28","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"近期個別調整：UBS 9/1 目標價升至 $695；Mizuho 8/25 降至 $590；Citi 9/8 目標 $710；Morgan Stanley 9/28 Hold、目標 $563。","source":"Investing.com AMAT consensus estimates","url":"https://www.investing.com/equities/applied-matls-inc-consensus-estimates","excerpt":null,"as_of":"2026-09-28","retrieved_at":"20261012","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Seeking Alpha 3 月快照：過去三個月 31 次 EPS 上修、0 次下修；30 次營收上修、0 次下修。","source":"Seeking Alpha AMAT earnings revisions","url":"https://seekingalpha.com/symbol/AMAT/earnings/revisions","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261012","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"TIKR 報導：AMAT 股價 2026-07-20 最大回撤 27%，儘管指引上調。","source":"TIKR","url":"https://www.tikr.com/blog/wall-street-sees-17-more-upside-in-applied-materials-stock-heres-the-math","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20261012","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-02-11 AMAT 與美國商務部 BIS 和解，支付 2.525 億美元；DOJ 與 SEC 通知已無行動結案相關調查（原為對中國/SMIC 出貨之出口管制調查）","source":"Applied Materials press release: Applied Materials reaches resolution with U.S. Department of Commerce","url":"https://www.appliedmaterials.com/us/en/newsroom/press-releases/021126-applied-materials-reaches-resolution-us-department-commerce.html","excerpt":"Applied has agreed to pay $252.5 million to the Department of Commerce. In addition, the U.S. Department of Justice and the U.S. Securities and Exchange Commission (SEC) have notified Applied that they have closed their related investigations without action.","as_of":"2026-02-11","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"+","claim":"2026-05 宣布以約 1.2 億美元現金收購 ASMPT 旗下 NEXX 先進封裝（面板級電鍍）業務；完成日期來源間不一致，未證實","source":"MarketScreener / MFN: Applied Materials broadens advanced packaging portfolio with acquisition of NEXX","url":"https://mfn.se/all/a/applied-materials/applied-materials-broadens-advanced-packaging-portfolio-with-acquisition-of-nexx-0422810c","excerpt":null,"as_of":"2026-05-03","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"+","claim":"2026-05 宣布以約 1.2 億美元現金收購 ASMPT 旗下 NEXX 先進封裝業務；完成日期來源間不一致，未證實","source":"MarketScreener / MFN: Applied Materials broadens advanced packaging portfolio with acquisition of NEXX","url":"https://mfn.se/all/a/applied-materials/applied-materials-broadens-advanced-packaging-portfolio-with-acquisition-of-nexx-0422810c","excerpt":null,"as_of":"2026-05-03","retrieved_at":"20261012","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"原告律所發佈 AMAT 投資人調查公告（2023-11 至 2024-08），2024-10-15 股價單日跌 10.69% 至 191.02 美元；搜尋結果僅見律所招攬，未見確認已提起的集體訴訟（超出近 12 個月，僅供背景）","source":"Pomerantz via SDxCentral: Pomerantz investigates claims from Applied Materials investors","url":"https://www.sdxcentral.com/press-releases/pomerantz-investigates-claims-from-applied-materials-investors/","excerpt":"Applied Materials' stock price fell $22.87 per share, or 10.69%, to close at $191.02 per share on October 15, 2024","as_of":"2024-10-16","retrieved_at":"20261012","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"2026-02-11 SEC 與 DOJ 通知 AMAT 已無行動結案相關調查（2024-02 起之傳票，涉中國出貨與聯邦補助申請）；搜尋結果未見財報重編","source":"Applied Materials press release: Applied Materials reaches resolution with U.S. Department of Commerce","url":"https://www.appliedmaterials.com/us/en/newsroom/press-releases/021126-applied-materials-reaches-resolution-us-department-commerce.html","excerpt":"the U.S. Department of Justice and the U.S. Securities and Exchange Commission (SEC) have notified Applied that they have closed their related investigations without action.","as_of":"2026-02-11","retrieved_at":"20261012","affects":["decision_inputs.bear","triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"AMAT","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.4,"operating_margin_pct":31.09,"fcf_margin_pct":18.23,"rd_intensity_pct":12.88},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMAT","as_of":"TTM ending 2026-07-31（4季加總）"},"is_subject":true},{"name":"2330.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.23,"operating_margin_pct":56.1,"fcf_margin_pct":25.33,"rd_intensity_pct":6.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2330.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"ASML","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":52.73,"operating_margin_pct":35.42,"fcf_margin_pct":24.27,"rd_intensity_pct":13.68},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASML","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"AMAT"},"financial_history":{"ticker":"AMAT","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-10-31","revenue":25785000000.0,"revenue_yoy_pct":null,"gross_margin_pct":46.51,"operating_margin_pct":30.19,"net_income":6525000000.0,"diluted_eps":7.44,"free_cash_flow":4612000000.0,"fcf_margin_pct":17.89,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-10-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-10-31","revenue":26517000000.0,"revenue_yoy_pct":2.84,"gross_margin_pct":46.7,"operating_margin_pct":28.86,"net_income":6856000000.0,"diluted_eps":8.11,"free_cash_flow":7594000000.0,"fcf_margin_pct":28.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-10-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-10-31","revenue":27176000000.0,"revenue_yoy_pct":2.49,"gross_margin_pct":47.46,"operating_margin_pct":28.95,"net_income":7177000000.0,"diluted_eps":8.61,"free_cash_flow":7487000000.0,"fcf_margin_pct":27.55,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-10-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-10-31","revenue":28368000000.0,"revenue_yoy_pct":4.39,"gross_margin_pct":48.67,"operating_margin_pct":29.86,"net_income":6998000000.0,"diluted_eps":8.66,"free_cash_flow":5698000000.0,"fcf_margin_pct":20.09,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-10-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/AMAT/AMAT_Q3_2026_Earnings_Call_20260813.md）

# Q3 2026 Earnings Call
2026-08-13

Q3 2026 Earnings Call
Applied Materials, Inc. | Earnings Calls | 2026-08-13
Operator (Operator)
Welcome to the Applied Materials Third Quarter of Fiscal 2026 Earnings Call. [Operator Instructions]
I would now like to turn the call over to Mike Sullivan, Corporate Vice President of Investor Relations.
Please go ahead.
Michael Sullivan (Executives)
Good afternoon, everyone, and thank you for joining today's call. With me are Gary Dickerson, our
President and CEO; and Brice Hill, our Chief Financial Officer.
Before we begin, I'd like to remind you that today's call includes forward-looking statements, which are
subject to risks and uncertainties that could cause our actual results to differ. Information concerning
these risks and uncertainties is discussed in our most recent Form 10-Q and other filings with the SEC.
Today's call also includes non-GAAP financial measures. Reconciliations to GAAP measures can be
found in today's earnings press release and in our quarterly earnings materials, which are available on
our website at ir.appliedmaterials.com.
In addition, any comments regarding calendar 2026 refer to Q2 of this fiscal year through Q1 of fiscal
2027, which will be a 14-week quarter.
Next, I'd like to remind you about our 2 special events during SEMICON West. On Monday afternoon,
October 12, we will host an unveiling of the new EPIC Center in Silicon Valley, California. And on
Tuesday morning, October 13, we hope you'll join Gary, Brice and our business unit leaders for our
investor breakfast presentation at the Yerba Buena Center in San Francisco. You can join us in person
or on a live webcast.
And with that introduction, I'd now like to turn the call over to Gary Dickerson.
Gary Dickerson (Executives)
Thank you, Mike. In our third fiscal quarter of 2026, Applied Materials delivered another set of record-
breaking results, including the highest quarter-on-quarter revenue growth in the company's history.
The rapid global build-out of AI infrastructure combined with Applied's leadership positions in the
most enabling and highest value technologies for AI computing provides the company with an
exceptionally strong foundation for multiyear revenue and profit growth. As 2026 has progressed,
customers have found new ways to address clean room space constraints and significantly increased
their demand for tool deliveries. In the past 3 months, we have again made upward revisions to our
revenue growth forecast for the year, and we are confident we will grow faster than the overall market.
As AI computing drives unprecedented demand for semiconductors, there is a large gap between
demand and supply for advanced chips. To ensure our supply chain and field teams can support their
ramps, our largest customers are giving us longer-term commitments and rolling 8-quarter forecasts.
This increased demand visibility gives us high confidence that 2027 will be another strong growth year
for Applied Materials. As customers move quickly to bring new fab capacity online, while

simultaneously optimizing yield and output of their existing production facilities, we also see strong
incremental demand for our advanced service solutions.
In my prepared remarks, I will share my views on how AI is resizing and reshaping the semiconductor
industry and its ability to realize the value of advanced technology. I will describe the increasing value
applied to delivering to our customers by accelerating their technology road maps, optimizing existing
production capacity and helping ramp new fabs faster. And I'll provide a brief update on our EPIC
strategy as we prepare to start operations in our new EPIC Center in Silicon Valley.
As I have said before, I strongly believe that AI is the biggest and most consequential technology
inflection of our lifetimes. While we are still in the early innings of deployment, AI is reshaping the
global economy and becoming fundamental to the relative competitiveness of companies. What I am
seeing at Applied Materials is a great case study in AI's real-world impact. Our investments in AI are on
track to deliver compelling returns by accelerating our revenue growth and operating profit margins. In
R&D and services, we are using AI to create highly differentiated products, significantly speed up
product development time lines and create valuable new service solutions for customers. In operations,
supply chain and our corporate functions, AI is helping us ramp faster, drive meaningful improvements
in productivity and scale our revenue significantly faster than our head count.
Beyond Applied, we see similar trends playing out across a wide variety of industries. As the
performance and cost of AI computing improves, many new applications will become technically viable
and economically attractive. These expansive opportunities for value creation are fueling an intense
global competition for AI leadership, which can be described as two concurrent races. The first race is
for technology leadership. AI data center returns are determined by the number of tokens generated
per second and the total cost of ownership, which is dominated by energy consumption. Improvements
in token per second per watt are primarily driven by innovations in semiconductor devices and
systems. This can be seen in the value the semiconductor and semiconductor equipment industries are
generating from their most advanced technologies.
The second race is for capacity as demand for advanced semiconductors to support AI infrastructure
scaling far exceeds supply. As a result, chipmakers are intensely focused on increasing output and
yields of their existing factories while rapidly building new ones. For Applied, the technology race and
the capacity race are fueling new opportunities to create and capture value. In the race for technology
leadership, leading edge foundry-logic, DRAM and advanced packaging have the greatest impact on AI
computing performance, power efficiency and cost. Together, we expect these areas to represent
around 80% of wafer fab equipment growth in 2026 and 2027. These three areas are also where
Applied has strong leadership positions, where we identified key AI inflections early, and where we've
shifted our investments to build an innovative pipeline of next-generation solutions.
In the past quarter alone, we have announced six new products, including our Centura Prime Epitaxy
system, designed specifically for high-performance DRAM, Producer Avila that enables higher
performance and higher layer count high-bandwidth memory, Nokota VMax, our next-generation
plating system and Opta Quad CMP for advanced packaging and two new e-beam systems also for
advanced packaging that expand on our e-beam leadership in the front end.
Advanced packaging is one of the most important areas for AI compute innovation, and we see very
strong multiyear growth for Applied. Applied is the overall leader in this market with strong positions
in high bandwidth memory and 3D chiplet stacking, and we now expect our overall packaging revenues

to grow more than 70% in calendar 2026. We are also well positioned for future packaging inflections
as the industry moves to new architectures and larger-sized panel formats. We have built a broad
portfolio of next-generation technologies for panel, including digital lithography, deposition, etch and
e-beam review.
In the global race to add semiconductor manufacturing capacity, our customers' ability to increase yield
and output in their existing production fabs is incredibly valuable. This creates expanded opportunities
for Applied to deliver new innovations in three key areas: Services, process diagnostics and control, and
new products that increase wafer output per area of fab space. Our advanced service solutions enable
customers to better optimize performance of their high-volume manufacturing operations. We already
have more than 37,000 chambers in the field connected to our proprietary AIx software capabilities
and use AI-powered monitoring, diagnostics and predictive analytics. Our advanced services are
delivering yield improvements for customers and helping us drive higher growth rates in Applied
Global Services. We now expect AGS to grow more than 20% in calendar 2026 and to deliver a
sustainable long-term annual growth rate in the mid-teens.
Our metrology and inspection product portfolio is also enabling customers to accelerate fab yields and
output improvements. The most advanced logic and DRAM devices require more e-beam steps that can
provide sub-nanometer resolution for high aspect ratio structures. Applied has unique e-beam
technology and is the leader in this growing market. In parallel, we are introducing new optical
inspection products, which enable us to increase application share in these markets as well. As a result,
we expect to grow our process diagnostics and control business more than 50% in calendar 2026, and
we have a strong pipeline of new products that will fuel growth in 2027 and beyond.
Finally, we are developing a new portfolio of output innovation products that increase the wafers that
can be processed per square foot of clean room space. One example is our new Epitaxy system for
DRAM that not only increases device performance, but also uses 20% less clean room space than our
earlier products. We have multiple output innovation products in qualification at customer sites that
will provide significant increases in output per unit area. With incredibly strong customer pull for next-
generation technology and unprecedented demand for semiconductor manufacturing capacity, the
value of time to market has never been greater.
Our EPIC strategy is designed to increase innovation and commercialization velocity by creating earlier
and deeper engagements with our customers and partners and co-locating key innovators. For chip
makers, EPIC provides much earlier access to Applied's new product innovations that are at the
foundation of future AI compute architectures. The output from EPIC will be more mature technology
that can deliver high yields faster in volume manufacturing. For Applied, EPIC co-innovation programs
will enable us to be designed in to new chip and packaging architecture inflections, increased R&D
productivity and value sharing and provide better multi-node visibility to guide our investments and
resource allocation.
Since our last earnings call, we announced that Broadcom will join EPIC as an innovation partner to
accelerate the development of advanced chip packaging technologies for next-generation AI systems.
We also signed EPIC partnership agreements with SCREEN and UC Berkeley. This brings our total
number of announced EPIC engagements to 11, spanning system companies, leading chip makers, top
research universities and innovation partners. The centerpiece of our EPIC platform is our brand-new

EPIC Center in Silicon Valley. We will move the first R&D tool into the clean room next week and we
are on track to start operations in the coming months.
Before I hand over to Brice, let me briefly summarize. Demand for advanced semiconductors and
semiconductor equipment continues to strengthen, and as customers find new ways to address clean
room space constraints, we see higher demand for 2026 tool deliveries. With support from our supply
chain, we have again increased our expectations for 2026 revenue, and we are confident we will grow
faster than the overall market this calendar year.
In the race for AI technology leadership, leading-edge foundry-logic, DRAM and advanced packaging
have the greatest impact on AI computing performance, power efficiency and cost. These are areas
where Applied has strong leadership positions and an innovative pipeline of next-generation solutions,
supporting strong revenue and margin growth in 2027 and beyond. And we're working closely with our
customers to optimize yield, outputs and fab ramp times with valuable new innovations in services,
process diagnostics and control and output innovation products.
Brice, over to you.
Brice Hill (Executives)
Thanks, Gary. I'm pleased to share that Applied delivered another quarter of double-digit sequential
and year-over-year growth in revenue, operating profit and non-GAAP earnings per share. Fiscal Q3
also marks our 13th consecutive quarter of year-over-year gross margin expansion, which demonstrates
how we are benefiting from the tremendous value our products and services bring to our customers and
the entire AI ecosystem.
Our fiscal Q4 guidance demonstrates continued strong year-over-year momentum. And in the second
half of the calendar year, we expect particularly strong growth in DRAM as well as leading-edge
foundry-logic and the advanced packaging for both. On today's call, I'll update you on the demand
environment, discuss how we're scaling our operations for continued growth, demonstrate how value
creation is expanding our gross margins, summarize our Q3 results and provide our Q4 guidance. Over
the past quarter, the demand outlook has strengthened across all the leading indicators we track. Cloud
service providers continue to increase their investments in AI infrastructure. Importantly, many of
these companies are already generating positive returns on their investments. And so are their
enterprise customers, including Applied.
As Gary described, we are accelerating the pace of new product development, increasing revenue and
generating new efficiencies in our support functions. In fact, G&A as a percentage of operating expenses
has declined to the lowest level in our history.
Turning to our direct customers, most leading-edge logic and DRAM fabs are running at full capacity.
Utilization levels are rising across the board, including in ICAPS, where we see strong demand in AI-
related markets like power and optical chips. As a result, our customers have announced more than 10
new fab projects just this quarter. Customers continue to give us longer visibility than we've ever had
with some conversations now extending to 2030. These communications are valuable to our company
and our own supply chain partners who are scaling with us to support our customers' growth forecast.
During the quarter, we officially opened our newest manufacturing center in Singapore, and combined
with other expansions worldwide have nearly doubled our manufacturing space over the past several
years. Based on the longer-term demand signals from our customers, we are now taking this further,

hiring and training new manufacturing and customer support teams so that we have the capacity to
double our quarterly system output from current levels by 2028.
In fact, we add more than 1,500 people this quarter in worldwide manufacturing and AGS customer
support. We are also planning our next manufacturing capacity expansion, ensuring we have the option
to support further increases in demand by 2030.
Next, I'll discuss value creation and sharing. Applied is delivering value to our customers in the AI
ecosystem in more ways than ever before. We've increased R&D every year since Gary joined the
company in 2012. And the investments have broadened from equipment innovations to materials
engineering solutions that result in better chips. More recently, we've significantly increased R&D and
advanced packaging innovations that enable better systems, supplementing our R&D with two small
acquisitions. And today, we're increasing investments in technologies that enable better fab economics
as we accelerate ramps and boost output and yields. All of these technologies will be put to work at the
EPIC Center, where we will co-innovate with our customers and partners to accelerate the AI road map.
In short, we've broadened our focus from making better equipment to enabling better chips and
systems for AI and better fab returns for our customers. These investments have made us a more
valuable partner to our customers and enabled us to share in the value we create. Three years ago, we
implemented a systematic approach to value-based pricing. And today, you can see the benefits
reflected in our strong revenue growth and gross margins which have increased to over 50% for the
company and over 55% in Semiconductor Systems. We have higher pricing and margins in both new
and existing products. At the same time, we remain focused on cost improvements and use them
aggressively to help offset higher input costs. As we look at the many opportunities we have to further
increase the value of chips, systems and fabs, we are confident we will continue to expand gross
margins.
Next, I'll summarize our Q3 results. We generated record revenue of $9.1 billion, up 15% sequentially
and 25% year-over-year. Non-GAAP gross margin increased to 50.4%, up 40 basis points sequentially
and 150 basis points year-over-year. Non-GAAP operating margin expanded to a record 34%, up 190
basis points sequentially and 330 basis points year-over-year. And we delivered record non-GAAP
earnings per share of $3.50, which is up 22% sequentially and 41% year-over-year. Last quarter, I
discussed our focus on increasing operating leverage. We grew revenue much faster than spending in
Q3 on both a sequential and a year-over-year basis and drove OpEx as a percentage of revenue to the
lowest level in nearly 4 years.
Turning to the segments. Semiconductor Systems delivered record revenue of $7 billion, which is up
18% sequentially and 27% year-over-year. The revenue mix was similar to last quarter as capacity
additions in gate-all-around and FinFET drove record foundry/logic revenue. DRAM revenue, which
includes HBM packaging, grew by 52% year-over-year to record levels. As we look ahead to the second
half of the calendar year, we expect a very significant increase in DRAM revenues as our customers
begin to expand clean room capacity. Looking to our individual materials engineering business units,
we had record revenues in deposition in Q3, including in PVD, CVD and epitaxy, which is one of our
fastest-growing businesses this year. In materials modification, we had record sales in thermal and
treatments. In materials removal, we had record revenue in both etch and CMP. We also had records in
process diagnostics and control, which is growing faster than our overall systems business this year.

Segment non-GAAP gross margin increased 190 basis points year-over-year to 55.4%. Non-GAAP
operating profit increased 45% year-over-year to a record $2.7 billion.
Applied Global Services delivered record revenue of $1.8 billion, which was up 22% year-over-year
reflecting both subscription services growth and high transactional parts demand. Ramp readiness is a
major priority, and the team added more than 1,000 customer support engineers. AGS is using AI and
warehouse automation to grow as efficiently as possible, which is reflected in strong gross margin of
35.6%, up 180 basis points year-over-year and operating margin of 30.1%, up 280 basis points year-
over-year.
From a regional perspective, China represented 26% of our Semiconductor Systems plus AGS revenue.
We now expect our China revenue to increase this calendar year, led by investments in 28-nanometer
foundry-logic, where Applied has strong technology differentiation and share. Other revenue of $294
million was in line with our expectations. We generated record operating cash flow of over $3 billion.
Capital expenditures were $707 million, resulting in free cash flow of $2.3 billion. We distributed $860
million to shareholders, including $420 million in dividends and $440 million in stock repurchases.
We have $12.8 billion remaining in our share buyback authorization and continue to expect to
distribute 80% to 100% of free cash flow to shareholders.
Now I'll share our guidance for Q4. We expect company revenue of $10.25 billion, plus or minus $500
million, which is up 51% year-over-year. We expect non-GAAP EPS of $4.02 plus or minus $0.20,
which is up 85% year-over-year. Within this outlook, we expect Semiconductor Systems revenue of
around $7.9 billion, up 62% year-over-year, AGS revenue of about $1.84 billion, up 22% year-over-year
and other revenue of around $510 million, composed primarily of display revenue. I've said previously
that our display business includes new products that could help us drive higher quarterly revenue in
future periods. For modeling purposes, we now expect other revenue to be approximately $400 million
per quarter on average through 2027.
We expect non-GAAP gross margin to be approximately 50.4% in Q4, up 230 basis points year-over-
year. And we expect non-GAAP operating expenses of around $1.58 billion. As a reminder, Q1 of fiscal
2027 will be a 14-week quarter which will result in a higher than average step-up in our Q1 operating
expenses. Finally, we are modeling a non-GAAP tax rate of around 11% and a tax rate of around 13% in
2027 as we absorb the effect of the global minimum tax.
In summary, the rapid adoption of AI that we've been investing for is driving strong growth and record
revenue and profitability for Applied Materials. We are enabling better chips, systems and fab returns
and systematically sharing in the value we create. We see continued record performance in the second
half of the calendar year with a sizable increase in DRAM and leading-edge foundry-logic revenue.
Based on the unprecedented visibility we're receiving from our customers, we expect another strong
record year in 2027 and are making substantial investments to be able to ramp to higher levels beyond
next year.
Now Mike, let's begin the Q&A session.
Michael Sullivan (Executives)
Thanks, Brice. [Operator Instructions] Operator, let's please begin.
Operator (Operator)

[Operator Instructions] And our first question for today comes from the line of C.J. Muse from Cantor
Fitzgerald.
Christopher Muse (Analysts)
Quarter ago, you quantified Semi Systems of 30-plus percent. Curious if there's kind of a framework for
thinking about what the growth outlook looks like now, given your positive commentary. And is there
any sort of framework that we should be thinking about into calendar '27?
Brice Hill (Executives)
Hi, C.J., it's Brice. Thanks for the question. So our key comments there and the way that we're seeing
the business is that demand strengthened again during the quarter. We see new projects being added
by our customers on the factory side. We see CapEx forecast going up by our customers, and we see
strong CapEx from the cloud service providers all and out. So the mid -- the greater than 30% that we
highlighted last quarter, we're saying now that it's greater than that at this point. We don't want to
guide our Q1 at this point. So that's as much information that we're providing. But when we look into
2027, we expect this whole demand function led by AI to continue. So we're saying '27 at this point, we
expect another strong year.
Gary Dickerson (Executives)
Yes, C.J., this is Gary. I would add just that the fastest-growing parts of the market are the leading-edge
foundry-logic, DRAM and advanced packaging. We said that's around 80% of the growth in wafer fab
equipment spending this year, and then we'll see a similar profile in '27. Those are the fastest-growing
parts of the market. Those are areas where we have clear leadership and really well positioned going
forward. So as you said, we increased greater than 20% is what we said year-over-year in February,
then greater than 30% in May. And now we think stronger than that, going forward. And so demand in
all the conversations with the customers is very strong. And what we're hearing from customers with
these 8-quarter rolling forecast is very strong multiyear demand. I really want to thank our supply
chain teams and operations teams. They're doing a great job in responding. But again, customers are
being very creative in how they're able to expand space and take tools earlier. Our teams are reacting
very quickly, and we're in a strong position to outperform this year.
Brice Hill (Executives)
So strong environment, C.J., and we also highlighted that we expect to gain share during the year.
Christopher Muse (Analysts)
Very helpful. And I guess as a follow-up on gross margin, you talked about value-based pricing. And I
think we've heard from most companies around anything expedited service, new tools. But you talked
about like-for-like pricing pushing higher. So could you speak maybe directly to that, and how we
should be thinking about the implications to your overall gross margins as we proceed into fiscal '27
and beyond?
Brice Hill (Executives)
Sure. So over the last three years, approximately 300 basis points increase in our company level gross
margins. One driver for that was our value-based pricing that we do for every single tool. So the issue,

C.J. was when we came through COVID, supply chain crisis, cost of inputs went up, we found ourselves
needing to reprice every tool. So we put that value-based process in place. And that's what we do is
examine the value of every single tool and put a new price on every single tool. And we think that's
required in an environment where the input cost change constantly. And then looking forward, we
expect to be able to continue to improve our gross margins. We're already over 55% for our -- at the
semi systems level and value-based pricing will continue to be a part of that.
Gary Dickerson (Executives)
Yes. C.J., I would add that I think our ability to create value for customers has never been stronger. This
race to bring new AI architectures to market is what every one of our single customers is focused on.
Applied has the most enabling technologies, as I said, in the fastest-growing parts of the market. So we
have a tremendous opportunity for creating value there. And I also talked about yield and output
innovation. So all of our customers, they are racing to be first to market with these new architectures
and then also ramping as fast as possible optimizing yield and output. So that puts us in a position
where our products are extremely valuable. Our services are also more valuable. That's driving the
greater than 20% service growth that we're seeing. We talked also about greater than 50% growth in
our PDC business that also is related to yield optimization. And then our pipeline of new products is
also very strong, and all of those have higher margins, and that will give us a tailwind going forward.
Operator (Operator)
And our next question comes from the line of Vivek Arya from Bank of America Securities.
Vivek Arya (Analysts)
So Gary, many of your memory customers are saying that they have 3- to 5-year long-term agreements
with good visibility into units and pricing? I know you mentioned you have 8 quarters of visibility. But
as you look at your customers who are signing up for a greater level of alignment with their end
customers. How is that kind of translating into your longer-term visibility beyond these 8 quarters?
Brice Hill (Executives)
Yes. I can start on that, Vivek. It's Brice. So what we have from customers, of course, the large
customers, we actually have visibility to the road map. So we have a perspective on probably 5 years of
visibility for our largest customers. We asked them for the detail at a detailed level for the 8 quarters
that we've been speaking about, so we can aggregate that and get it to our supply chain. And other
things that have changed, we get longer lead time POs from our customers so that the details are agreed
from a longer lead time perspective. And then we also have some charges that have moved into this
environment like cancellation charges and expedite charges that help with -- that help navigate the
environment. So there's been a number of changes, and I think visibility is significantly increased from
prior periods.
Gary Dickerson (Executives)
Yes, Vivek, this is Gary. Certainly, everybody can see that there is a gap between supply and demand.
DRAM, especially with AI as we're expanding from training to inference to agentic AI to physical.
Memory demand continues to go higher, and I'd say especially DRAM. DRAM this is going to be a very
strong growth year for Applied, more second half weighted in terms of our DRAM growth, but very

strong growth in DRAM. And I think, as you know, we've expanded our DRAM share significantly over
the last several years, and we continue to see strong growth in our DRAM business going into '27. And
as you said, as we're in all of these conversations with customers, they're talking about multiyear
growth and significant demand that we're increasing our capacity to meet.
And then for us, relative to our position in DRAM, we are the #1 process equipment provider in DRAM.
We're the leader in the CMOS periphery logic to upgrade transistors for higher performance and power
including, I talked earlier on the call about very strong epi growth, HBM packaging. We're the leader in
materials deposition for wiring and patterning, conductor etch, e-beam technologies, and we're in deep
partnerships with customers also for future DRAM architectures, innovations in 6F2, 4F2, and we're
very well positioned for 3D DRAM in the future. So I have high confidence that we're going to continue
to drive significant growth and gain share in this segment.
Vivek Arya (Analysts)
Got it. For my follow-up, one more on gross margins. If I go back from calendar '21 to '25, your gross
margins and those of your U.S. peer were about the same. In fact, Applied was slightly ahead. But in the
near term, they are about 150 basis points higher. So I understand mix for every company is different.
But I'm curious how come the gross margins were so aligned in those 5 years, yet they are kind of
lagging a little bit. So just what's the prospect, Brice, for expanding gross margins to more of this
industry level going forward?
Brice Hill (Executives)
Yes, Vivek, I don't know if I have a great reason to think about comparisons. But from our perspective,
we've made tremendous progress from a gross margin advancement. We talked about our value pricing
and really it's the portfolio. The portfolio continues to strengthen as we target the R&D and the
collaborations with our customers at the most valuable inflection solutions that need to be developed.
And so the pricing really is just demonstrating the value of that portfolio. And yes, we expect to be able
to continue that. Of course, we have some other elements in our portfolio like the display business that
we've talked about when that grows faster, that has a different effect on the corporate gross margin. So
the portfolios are different between the two companies, but we expect to be able to continue to improve
our gross margin and grow the value over time.
Gary Dickerson (Executives)
Yes. Again, I would also add, we have been driving margin growth, pretty significant margin growth.
We talked about 13 consecutive quarters of year-over-year growth, 190 basis points in our Semi
business in the last year. And I have high confidence we're going to continue to drive margins higher,
continuing the growth that we've seen over the last few years.
Operator (Operator)
And our next question comes from the Stacy Rasgon from Bernstein Research.
Stacy Rasgon (Analysts)
I have one more on gross margins as well. And look, I feel a little bad harping on it because they're
actually really good. They're well over 50%, and they are coming in higher than you had expected. But
I'm just wondering, you are guiding them flat at these current levels, at least in the near term on a

pretty sizable revenue increase, and just given all the commentary around portfolio and pricing and
everything, I was just a little surprised. Why is it? Is that just a function of the display business growing
sequentially just mix between the businesses? Or is there something else going on in the near term?
Brice Hill (Executives)
Hi, Stacy, Brice. Yes, thanks for pointing out the growth in display is certainly a factor in the recipe. But
really, it's just a ramp headwind as with the growth, we're ramping a lot of customer service engineers.
We have a lot of resources that we're adding in the Semi business. And so yes, we get the benefit of
strong segment mix with semi growing so strongly and we get the benefit of more volume. But we do
have some ramp costs that are in the forecast. So we feel good about in our guided quarter, we feel good
about having a flattish margin at the company level. And then like we said, as you look longer term,
we'll expect to be able to continue to grow the margin.
Stacy Rasgon (Analysts)
Got it. So I guess to follow up on that then. So if there's ramp costs now, I guess how long do those last?
Are you still ramping up more engineers and other costs like into subsequent quarters? Or are you all in
this quarter? And then as we think about the pace of that expansion, like what does it look like? I think
you talked about last quarter thinking about something like 10 bps or something sequentially kind of
going forward. Is that still the trajectory or given some of the other drivers, do you think it can come in
better than that?
Brice Hill (Executives)
No, I think the continued pace of improvement, we called that slow in the past. I think slow
improvement is the right way to think about it. We do expect to improve it over the longer horizon. So I
think we will continue to add employees over the next few quarters, but I think that headwind will
recede as the revenues continue to grow.
Operator (Operator)
our next question comes from the line of Timothy Arcuri from UBS.
Timothy Arcuri (Analysts)
Brice, I want to go back to the systems guidance for the year. So you said up more than 30% last call,
things have gotten better since then. But even if you go 40%, that implies a pretty big decel, into
December. So you go from 18% in July to 12% in October to then 6% in January, and that gets you to
like 40%. And Lam was talking about WFE being up like 38%. So if you're going to outgrow, you have to
be at least 40%, if you believe their numbers. So would you commit to be to growing systems 40% or
more?
Brice Hill (Executives)
Hi, Tim. Thanks for the question. We are committing that we expect to outgrow. We think that's
already happened so far this year, and we expect to have that happen. Wherever we land from a growth
perspective as we get through the year. And I think you've got the dynamics right. We first guided
greater than 20%. We raised that after customers added clean room projects. We raised it to greater
than 30%, and we're saying it's even higher now. And so yes, we'll expect -- we're not giving that

number because we're not guiding that out quarter, but those are the right dynamics. I guess the last
thing I'll add there is we do expect sequential growth in our Q1, the calendar Q4, but not guiding that at
this point.
Timothy Arcuri (Analysts)
Okay, Brice. And then maybe asked a different way. So the comment about manufacturing capacity
doubling. So should I just take that kind of face value and so you're shipping roughly your revenue and
roughly $7 billion in the July quarter. So at face value does that mean that sometime during calendar
'28, you'd be revenue at $14 billion, or is it more nuanced than that?
Brice Hill (Executives)
It is more nuanced. I think you should take it explicitly. It's capacity. So it's not a revenue forecast for
2028. What we have to do with long lead investments like clean room is make sure we have the clean
room in place with a profitable business or any demand forecast demand reality in that environment.
And so we're just communicating because partially we're communicating to our suppliers also. We're
putting the capacity in place to be able to support a wide range of output requirements in 2028. And as
far as that goes the years after also. So no, it's not a revenue forecast, but yes, it's giving you an
indication of what we will be prepared for.
Operator (Operator)
And our next question comes from the line of Krish Sankar from TD Cowen.
Sreekrishnan Sankarnarayanan (Analysts)
I just want to follow up on Tim's question. Gary, or Brice, it seems like your customer conversation
seems to have shifted from annual price discussions to basically delivering and meeting requirements
basically time to market with a 2-year visibility. I'm just wondering, does this give you some freedom on
pricing? Or does it add more burden on expenses on setting up your capacity and the supply chain for
the upcoming ramp? And if you have the visibility of 2 years, why not give a Jan quarter qualitative
outlook? And then I have a follow-up.
Brice Hill (Executives)
Hi, Krish. Yes, the customers definitely -- especially the large customers, we've got very strong visibility.
And you're right, they are becoming more and more interested in scheduled delivery and hitting the
schedules, which is why they're collaborating, cooperating on specificity of the orders and the 8-quarter
visibility that we're also sharing with our suppliers. So I think that dynamic has improved the situation
for us in the planning environment dramatically from the prior year. So I think all those things are true.
I guess that's our perspective at this point.
Sreekrishnan Sankarnarayanan (Analysts)
Got you. Got you. And then maybe, Brice, I think in your prepared comments, you kind of spoke about
certain customers giving you visibility into 2030. I'm just curious, are those conversations about
technology, or is that still about capacity to scale up and meet that demand?
Brice Hill (Executives)

Well, yes, it's definitely about technology. So especially with the large customers or mature customers,
we know the fab projects that are on the road map. We know the technology that's planned and even if
it's a new technology, we have a perspective of our positions in those technology. So we do have the
ability to plan in a detailed manner for 5 years. And then what happens at the 8 quarter out is we get
very specific about the node and the tool types that need to be built so that we can pass that information
along to the suppliers. And we do have...
Gary Dickerson (Executives)
Yes, Krish, we are -- I'm in many of those conversations with the CEOs of our largest customers. And
for sure, they're giving us visibly -- detailed visibility for the 8 quarters, but even beyond that, I think
they have communicated they see strong multiyear demand in their business. And so they're wanting us
to be ready to support that demand. And as you know, it takes time for us to get the supply chain ready
to support those levels. So we are getting the visibility relative to capacity needs beyond the 8 quarters.
On the technology, I would say that those discussions go out maybe 10 years in the future because
Applied is the most enabling for those key architecture inflections. We have the most broad, the most
connected, the most unique portfolio to enable the new transistors, the wiring, the DRAM
architectures, new packaging architectures and it takes time to bring those innovations to market. So
Applied is unique in the portfolio we have. We have the most enabling technologies. If you looked at the
top 5 or 10 technologies you need to enable these new architectures. Applied has, by far, the majority of
those technologies. And so very deep co-innovation relationships with customers where we're
cocreating those architectures. So that technology visibility goes beyond 5 years in these deep co-
innovation relationships with the customers.
Operator (Operator)
And our next question comes from the line of Harlan Sur from JPMorgan.
Harlan Sur (Analysts)
The team previously guided your global ICAPS business to be flat to slightly up this year. Outside of
China, I mean, we are seeing a strong cyclical recovery in automotive, industrial, for your analog power
microcontroller customers, right? They are also articulating an environment of tight supply as well.
Utilizations are rising meaningfully, Brice, as you articulated. But are these global customers also
starting to pick up their spending? And do you see your total ICAPS business growing this year?
Brice Hill (Executives)
Harlan, thanks for the question. So I'll start here. Yes, in pointing this out, we do see a change in the
ICAPS dynamic. So you called out the increasing utilization across those customers. That's a positive.
Our view of China is that it will grow this year, and it will grow next year. That's a big part of our ICAPS
portfolio. And we do think that ICAPS overall will grow this year and will grow next year. So the
digestion, we're hopeful that the digestion that we've talked about on the equipment side in the past is
expiring, and we can return to growth. And then specifically, for our non-China customers as we look
into next year, we think there'll be positive growth for those customers. We see bright spots in power
and photonics in other areas. So it's looking much more positive than it has the last couple of years.
Harlan Sur (Analysts)

I appreciate the color there. And another quarter of strong revenue growth and growth in operating
margin profitability in AGS, right? 30% operating margins, I think that's the highest level, I think, in
two years. Plus your incremental gross margins, I think for the last couple of quarters have been well
above 40%. So strong -- and also have been delivering strong incremental operating margins as well. I
know the team has historically thought that they could drive AGS operating margins longer term into
the low 30% range. But on your strong incremental margin profile, could we see gross margins
approaching the 40% range and operating margins in the mid-30s as AGS revenues continue to scale
higher, advanced services becomes a bigger part of the mix kind of over the long term?
Brice Hill (Executives)
Yes. Thanks, Harlan. So I think not different from the Semi business. We do expect that we have the
opportunity to improve gross margins over time in the services business. And what's happening there is
that solutions like the information solutions that come from AI are allowing us to develop new products
and be more efficient in the services that we're providing. That, combined with the growing installed
base, gives us good growth there. And then this year, we had the benefit of significant increase in
utilization, which grows the spares business more quickly than in prior years. So that helps us from a
gross margin perspective. That -- from that point, you can only grow to 100% utilization once. So that
sort of slows down. But we do expect we'll be able to improve gross margins over time in the services
business.
Gary Dickerson (Executives)
Yes, Harlan, I would add that for customers right now, optimizing output and yield is incredibly
important in a supply-constrained environment, and that's going to go on for some period of time. So
the value of services that optimize yield is incredibly valuable. And the good news is we have a lot of
new innovations there. We talked about over 37,000 chambers connected to our AIx servers. We have
AI-enabled applications for preventative maintenance or chamber matching. Those are incredibly
valuable services that will drive our top line growth, our service contract growth faster and also enable
us to capture value more quickly. So actually, I am more positive on growth in the AGS business, both
top line and bottom line than I've ever been.
Operator (Operator)
And our next question comes from the line of Blayne Curtis from Jefferies.
Blayne Curtis (Analysts)
I want to ask on NAND. It doubled in the quarter, obviously, off a small base. Just curious what you're
seeing in that market. And then you did mention it in October. I'm assuming maybe that's a small
dollar that's why you didn't call it out, but is it continuing to grow?
Brice Hill (Executives)
Hi, Blayne. Yes, good growth in NAND this year from a percentage perspective, small base, like you say,
but we think this year is a strong year of growth for NAND. As we look forward, into our next year, we
think the dynamic is that really that AI dynamic that we've called out before and Gary mentioned
earlier, leading-edge logic and DRAM and advanced packaging will be the fast growers. ICAPS should
return to growth for us, NAND should grow but will be the slower grower in the out year.

Blayne Curtis (Analysts)
And then, Brice, maybe on CapEx. You talked about the expansion of spending for 2030. I don't know if
that's going to hit now. I'm just kind of curious if you can comment on what you expect OpEx to be in
October? And then just any perspective next year? I think EPIC rolls off. So I think the prior was that it
would go down. But now with the strength in the business, I'm just curious how you're thinking about
that spend.
Brice Hill (Executives)
Yes, that's a great question because you're right, on the strength of the business, of course, we have
more additions that we want to do. This is a CapEx comment. We want to -- we will be putting
equipment inside EPIC as well as other investments. So what I would say about CapEx, it will still be a
CapEx year that's higher than normal, but it will decline as a percentage of revenue as we go into '27. So
that's our perspective at this point.
Operator (Operator)
And our next question comes from the line of Jim Schneider from Goldman Sachs.
James Schneider (Analysts)
I was wondering if you can maybe comment, given the strength you're seeing across your focus areas.
As you look into fiscal '27 or calendar '27, would you care to rank order where you see the incremental
strength between foundry-logic, DRAM spending and advanced packaging?
Brice Hill (Executives)
Yes. Jim, this is Brice. I'll start. We actually don't distinguish between them. We think the system-level
pull that AI provides is similar across those different end markets. So I wouldn't call the difference
enough to distinguish between them. So it will be strong for leading logic. It will be strong for DRAM. It
will be strong for advanced packaging. And what's new for us now is that we also think that ICAPS will
grow next year. So that's another difference from our previous 90 days.
Gary Dickerson (Executives)
Yes, Jim, thanks for the question. Yes, I think we talked earlier about 80% of WFE growth in those
three segments in '26. And we see a similar profile, maybe even a better profile. But right now, we'd say
similar profile in '27. Those three segments, as Brice talked about, we see those as the fastest-growing
segments in '26 and '27 and frankly, over the next several years.
James Schneider (Analysts)
That's helpful. And then just given the first half versus second half dynamic we're seeing in calendar
'26. Is there any reason why in calendar '27, you wouldn't see an accelerating growth rate for overall
revenue? Is there anything you see on the horizon that would give you pause?
Brice Hill (Executives)
I think a lot of people ask, Jim, about what is governing growth. I think as you move into the longer
term, what governs growth is clean room from our perspective. So customers continue to add clean
room projects. That's why we raised our forecast this year. Some of those will add incremental clean

room space next year. And of course, it gets larger as the out years come into focus because those
projects usually take a number of years. But anyway, I think it will be the availability of clean room at a
high level that will determine what we can all ship next year.
Operator (Operator)
And our next question comes from the line of Mehdi Hosseini from Susquehanna International.
Mehdi Hosseini (Analysts)
Yes. I just have a couple of follow-ups maybe for Gary. Forget about the near-term trend, but I want to
better understand how you're thinking about your targeted revenue, gross and operating margin for a
scenario where WFE will be $150 billion to $175 billion. Any color would be great.
Gary Dickerson (Executives)
Hi, Mehdi. Thanks for the question. Yes, I think when we have the October investor event, we'll give
more color relative to growth rates. What I would say is that if I look at the setup relative to compute
demand going forward. We see this as a strong multiyear growth driver and the fastest-growing
segment of market, what we talked about earlier, the most valuable parts of the market leading-edge
foundry-logic, DRAM, advanced packaging. We're #1, and we're positioned to gain share going forward
in those segments. So I think top line growth, we have a number of really great drivers that will enable
us to outperform in '26, and we look at very strong growth going forward. And I also believe that really
across the board, the value that we're delivering is also increasing.
We are -- we do have the most unique connected portfolio that's creating tremendous value for our
customers, for new chip and packaging architectures. That puts us in a good position to continue to
drive our margins higher going forward. And I mentioned earlier about the innovations and yield and
output. And as you can imagine, Mehdi, every single customer, they're focused on getting as many chips
out per square meter as they possibly can. So that increases the value of our service business, and we're
bringing innovation that really directly address those areas of focus for our customers. So I think
relative to the top line growth, bottom line growth, I'm very optimistic. But we'll give more color,
Mehdi, when we have our October investor meeting.
Brice Hill (Executives)
I'll add -- I'll just do one add, Mehdi. You're really describing this year and scenarios that people are
talking about for this year. So I think we're giving you the ingredients for that with a greater than 20%
services business for the calendar year, something higher than greater than 30% for the semi business.
We talked about our gross margin outlook. We gave you the display item. And then whatever that WFE
number is, we've said we expect to gain share. So I think you have the ingredients needed to have a
perspective on that.
Mehdi Hosseini (Analysts)
Got it. Just a quick follow-up. I think your NAND has been relatively the smallest part of your semi and
I think it's a reflection of more of an upgrade going on within the NAND than wafer capacity add. When
do you think the industry would actually start adding some wafer capacity to offset some of these losses
due to increased migration to a 300-layer count?

Brice Hill (Executives)
Hi, Mehdi. Yes, so for the dynamic here, I think we've described in the past is wafer starts continue to
decline in NAND. So the projects you see are for upgrades, as you described, to get more layers. We
expect the environment to continue the same dynamic for the next few years. The one place that will be
different is new projects in China, I believe. But for the larger customers, it's mostly increased space to
afford those upgrades in layers that you described.
Michael Sullivan (Executives)
Yes. Thanks, Mehdi. And operator, we have time for one more question, please.
Operator (Operator)
Then our final question for today comes from the line of Srini Pajjuri from Royal Bank of Canada.
Srinivas Pajjuri (Analysts)
Gary, a couple of questions on the technology front. You talked about panel-level packaging. And just
curious as to when do you see panel-level packaging becoming mainstream? And compared to your
current position in advanced packaging, what sort of opportunities do you see in that market? And then
also, if you can touch on hybrid bonding. It seems like that's finally happening and what sort of
opportunities you're seeing in the market?
Gary Dickerson (Executives)
Yes. Thanks for the question. So as I talked about earlier on the call, packaging is one of the most
important areas in the industry relative to improving AI compute performance and power, multichip
connectivity, how you move the data, huge focus for all of our existing customers and new customers
that are innovating with new architecture. So over 70% growth this year. We have, by far and away, the
strongest portfolio of technologies. We've also talked about some acquisitions that we've done here
recently that add to our strength in packaging. So I have very high confidence that we will continue to
drive significant growth over many years in packaging.
Relative to new substrates, all of our customers are really focused on connecting as many logic and
memory chips together at the highest performance and power as they can. And so we're in deep co-
innovation relationships with companies, and there is a race for all of these companies to drive these
new architectures to market because there's so much value in performance and power. So I look at that
as a great opportunity when we model our share of those new architectures, we have a great
opportunity to grow our share.
We have new capabilities that will expand our available market as those new architectures are adopted.
And I don't want to give a specific forecast relative to timing. But what I would say is that we will see a
pretty significant growth in next year in our panel revenue. And certainly, it's going to ramp a fair
amount after that going forward. But our positions there are stronger. And then relative to hybrid
bonding, hybrid bonding is a way that every customer, whether it's leading edge foundry-logic or
DRAM or high bandwidth memory, they're all wanting to shorten the wiring length to improve the
performance and power. So it's a very important inflection for all of our customers.
Again, Applied has strong technology in hybrid bonding. We have also very big business in the adjacent
steps around the hybrid bonding. We have the only integrated R&D facility, working with our

customers to enable those new architectures for packaging. So this will be a meaningful growth driver
over time in addition to all the other technologies that we have in advanced packaging. So I'm very
optimistic over 70% growth this year and very strong growth in '27 and going forward.
Srinivas Pajjuri (Analysts)
Then one quick follow-up for Brice. Brice, I understand you don't want to give us FQ1 guidance, but you
did call out that it's a 14-week quarter. I'm just wondering what sort of impact, if any, that will have on
your revenue sequentially?
Brice Hill (Executives)
Sure. What we've seen in prior years when we had a 14th week in the quarter was you get close to a
ratable performance on the services side of the business and not so much on the equipment side. Most
of the planning is done at a quarterly basis on the equipment side. So yes. And then from a spending
perspective, as you might imagine, everybody wants to be paid. And so most of the spending will occur
in the quarter. Thanks, Srini.
Michael Sullivan (Executives)
So thank you, Srini, for your questions. And Brice, would you like to give a little summary before we
close the call?
Brice Hill (Executives)
Thanks, Mike. We're excited that Applied's unique portfolio and strategy are enabling us to grow faster
than the market and increase margins. We look forward to an even stronger second half and to seeing
many of you at our upcoming events. I'll be attending Citi Conference in New York, and Gary will be at
the Goldman Conference in San Francisco. The whole team looks forward to seeing you at the EPIC
Center in October and giving you our longer-term outlook at our investor breakfast at SEMICON West.
Mike, please go ahead and close the call.
Michael Sullivan (Executives)
All right. Well, thank you, Brice, and we'd like to thank everybody for joining us today. A replay of
today's call is going to be available on the IR page of our website by 5:00 Pacific Time, and we'd really
like to thank you for your continued interest in Applied Materials.
Operator (Operator)
Thank you, ladies and gentlemen, for your participation in today's conference. This does conclude the
program. You may now disconnect. Good day.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AMAT_Q2_2026_Earnings_Call_20260514.md
- 2026-05-14｜Brice Hill (CFO)｜guidance：FQ3 營收指引 8.95 億美元（原文單位 billion）±5 億，年增近 23%（原話："company revenue of $8.95 billion plus or minus $500"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：FQ3 non-GAAP EPS 指引 3.36 美元 ±0.20（原話："We expect non-GAAP EPS of $3.36 plus or minus"）
- 2026-05-14｜Brice Hill (CFO)｜margin：FQ3 non-GAAP 毛利率指引約 50.1%，小幅上升（原話："to increase modestly to approximately 50.1%"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：FQ3 non-GAAP 營業費用指引約 14.85 億美元（原話："we expect non-GAAP operating expenses of around $1.485"）
- 2026-05-14｜Gary Dickerson (CEO)｜guidance：半導體設備事業 2026 曆年成長 30% 以上（相較上季上調，因客戶找到更多無塵室空間）（原話："we'll grow 30% or more in the year"）
- 2026-05-14｜Gary Dickerson (CEO)｜guidance：先進封裝營收 2026 曆年成長逾 50%（原話："grow our packaging revenues more than 50% in calendar 2026"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：AGS 成長預期由先前的低雙位數上調為中十位數（mid-teens），今年更高（原話："we are going to raise our expectations for AGS to mid-teens"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：中國與全球 ICAPS 業務曆年預期持平至小幅成長（原話："our ICAPS business worldwide, to be flat to slightly"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：管理層預期 2027 年為產業另一個創紀錄年（原話："we expect 2027 will be another strong,"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：被問 FQ3 後走勢，CFO 稱可假設從 FQ3 指引到 FQ1 以美元計線性成長，不提供逐季明細（原話："it grows linearly from our Q3 guide through Q1"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：回答 2028 是否仍為 WFE 成長年：CFO 表示現在判斷並不嫌早（原話："We don't think it's too early, Krish."）
- 2026-05-14｜Brice Hill (CFO)｜margin：本季營收與營業利益率數字：營業利益率 32.1%（原話："32.1%, up 140 basis points year-over-year"）
- 2026-05-14｜Brice Hill (CFO)｜margin：管理層把毛利率提升歸因於高差異化產品的價值定價（原話："driven by value-based pricing from our most differentiated"）
- 2026-05-14｜Brice Hill (CFO)｜margin：開始分部門揭露毛利率；半導體系統 Q2 為 54.8%（原話："Semi Systems gross margin is 54.8% in Q2"）
- 2026-05-14｜Brice Hill (CFO)｜margin：定價機制：以專案為基礎的長約，變動較慢（原話："our pricing generally works as long-term contracts with"）
- 2026-05-14｜Brice Hill (CFO)｜margin：AGS 毛利率改善驅動因素：備品／交易型業務占比提高（原話："the mix to more transactional and more"）
- 2026-05-14｜Brice Hill (CFO)｜margin：AGS 費用下降部分來自重組（原話："we did some restructuring that helped us with expenses"）
- 2026-05-14｜Gary Dickerson (CEO)｜commitment：CEO 表示對毛利率進展延續高度有信心（原話："I have high confidence that the margin progress that"）
- 2026-05-14｜Brice Hill (CFO)｜commitment：費用成長慢於營收、營業利潤持續增加（原話："we also expect to increase spending more slowly than"）
- 2026-05-14｜Brice Hill (CFO)｜capital_allocation：本季股東回饋 7.65 億美元（原文 million），含股利與買回（原話："We distributed $765 million to shareholders"）
- 2026-05-14｜Brice Hill (CFO)｜capital_allocation：季股利調升 15%（原話："15% increase to the quarterly cash dividend"）
- 2026-05-14｜Brice Hill (CFO)｜capital_allocation：製造產能已近乎倍增（美、歐擴建及新加坡新製造中心）（原話："We've nearly doubled our manufacturing capacity to support"）
- 2026-05-14｜Brice Hill (CFO)｜customer：最大客戶提供滾動 8 季預測（原話："giving us the clearest and longest visibility we've ever had"）
- 2026-05-14｜Brice Hill (CFO)｜customer：追蹤中的晶圓廠專案逾 100 個（原話："tracking over 100 factory projects globally"）
- 2026-05-14｜Gary Dickerson (CEO)｜customer：EPIC 共同開發夥伴新增 TSMC（原話："we announced our EPIC co-development engagement"）
- 2026-05-14｜Brice Hill (CFO)｜customer：NAND 位元成長預測上調，預期仍以升級滿足（原話："we did raise our bit growth forecast for"）
- 2026-05-14｜Brice Hill (CFO)｜customer：ICAPS 面臨既有產能消化期（原話："there'll be some digestion with all the capacity that's been"）
- 2026-05-14｜Gary Dickerson (CEO)｜product：敘事變化：新增 agentic AI 為晶圓廠設備的額外需求來源（原話："they provide an additional tailwind for wafer fab"）
- 2026-05-14｜Gary Dickerson (CEO)｜product：敘事變化：上季稱無塵室空間是投資步調的關鍵因素，本季客戶正找到新空間（原話："the availability of cleanroom space was a key factor pacing"）
- 2026-05-14｜Gary Dickerson (CEO)｜product：3 個領域預期占 2026 年 WFE 成長 80% 以上，2027 類似（原話："account for more than 80% of the year-on-year growth"）
- 2026-05-14｜Gary Dickerson (CEO)｜product：Sym3 為公司史上最快放量產品（原話："Sym3 is the fastest ramping product in Applied's history."）
- 2026-05-14｜Gary Dickerson (CEO)｜competition：宣稱導體蝕刻在先進邏輯 GAA 與 DRAM 均為第一（原話："Sym3 is the fastest ramping product in Applied's history"）
- 2026-05-14｜Gary Dickerson (CEO)｜competition：DRAM 市占過去十餘年增加 10 個百分點（原話："we gained 10 points of overall share in WFE and DRAM"）
- 2026-05-14｜Gary Dickerson (CEO)｜competition：被質疑製程控制市占下滑，CEO 表示不同意該看法（原話："I don't share your view on the perspective on the business."）
- 2026-05-14｜Gary Dickerson (CEO)｜risk：CEO 指出供應鏈是限制，產能擴張受供應鏈回應速度牽制（原話："And it's really supply chain."）
- 2026-05-14｜Gary Dickerson (CEO)｜risk：被問出口管制（華為相關）風險擴大，CEO 拒絕評論，稱已納入指引（原話："I don't really want to comment on that."）

### AMAT_Citi_s_2026_Global_TMT_Conference_20260908.md
- 2026-09-08｜Brice Hill (CFO)｜guidance：CFO 稱明年預期為強勁成長年，驅動力為 AI 投資循環，看不到改變（原話："we expect next year to be a strong growth year"）
- 2026-09-08｜Brice Hill (CFO)｜customer：最大客戶提供的滾動 8 季預測全年持續上升，歸因於 AI 系統需求（原話："rolling 8-quarter forecast we get from our largest"）
- 2026-09-08｜Brice Hill (CFO)｜customer：雲端業者資本支出預測全年上修，美系逾 7,000 億美元、全球近 1 兆（原話："over $700 billion this year for the U.S. companies"）
- 2026-09-08｜Brice Hill (CFO)｜customer：8 季預測因按工廠進單而非線性，呈跳升式成長；管理層看不到見頂點（原話："we don't see a place where it peaks"）
- 2026-09-08｜Brice Hill (CFO)｜customer：追蹤的新廠專案超過 100 座，最近兩季每季新增逾 10 座，作為領先指標（原話："well over 100 factories that we're tracking"）
- 2026-09-08｜Brice Hill (CFO)｜risk：中期受限因素為無塵室，需求大於供給（原話："in the medium term, it's gated by clean room"）
- 2026-09-08｜Brice Hill (CFO)｜product：先進封裝去年營收 14 億美元，今年成長逾 70%，預期與先進邏輯及 DRAM 同步成長（原話："We've said this year, it's growing more than 70%."）
- 2026-09-08｜Brice Hill (CFO)｜guidance：ICAPS 今年預期溫和成長，明年為較正常的成長年（敘事相對過去兩年疲弱有變）（原話："We actually expect some moderate growth in ICAPS this year"）
- 2026-09-08｜Brice Hill (CFO)｜margin：ICAPS 正常成長的口徑：終端元件年增中高個位數，設備最終跟隨（原話："the devices themselves grow at mid- to high single digits"）
- 2026-09-08｜Brice Hill (CFO)｜competition：NAND 位元需求高但層數堆疊使所需晶圓減少，屬升級循環，設備市場較小且預期至少持續數年（原話："it makes that market smaller"）
- 2026-09-08｜Brice Hill (CFO)｜product：面板級封裝目前仍在開發階段，已有設備營收但無量產；近期收購 NEXX（原話："I don't think there's any volume production at this point."）
- 2026-09-08｜Brice Hill (CFO)｜risk：對 HBM 堆疊層數降低（de-speccing）的看法：設備端中性，未見需求減少（原話："we would view that overall as neutral"）
- 2026-09-08｜Brice Hill (CFO)｜competition：管理層否認公司只是跟隨整體設備市場，定位為最具賦能性的整合製程設備組合（原話："We certainly don't view it that way."）
- 2026-09-08｜Brice Hill (CFO)｜capital_allocation：近期收購 X 光檢測公司與 NEXX，用於微凸塊檢測與面板細線互連（原話："We did the NEXX acquisition that I mentioned"）
- 2026-09-08｜Brice Hill (CFO)｜commitment：公司已投資並持續投資，使每季產能達目前系統產量的兩倍；強調為產能陳述而非營收預測（原話："It's not necessarily a revenue forecast"）
- 2026-09-08｜Brice Hill (CFO)｜commitment：將依元件類型彙整客戶 8 季預測並提供給 2,000 多家供應商，提前 8 季預告（原話："so that they're getting 8-quarter advance notice"）
- 2026-09-08｜Brice Hill (CFO)｜margin：近三年毛利率約擴張 300bp，其中相當部分來自定價，但管理層定位為價值反映而非漲價（原話："A lot of that has been on pricing, but it's not -- I don't"）
- 2026-09-08｜Brice Hill (CFO)｜margin：鋁、鋼、晶片、人力成本上升，因此需要往後調整價格（原話："So we do have to adjust prices going forward"）
- 2026-09-08｜Brice Hill (CFO)｜margin：價值定價適用所有產品，新舊不分，每期都須調整（原話："we have to make an adjustment each period"）
- 2026-09-08｜Brice Hill (CFO)｜guidance：服務業務長期成長預期由低雙位數上調至中十位數，因安裝基數成長快於預期（原話："from low double digits to mid-teens"）
- 2026-09-08｜Brice Hill (CFO)｜guidance：服務今年成長逾 20%，因產能利用率近滿載帶動備品採購；明年回到長期成長率（原話："We can't go to 110% next year."）
- 2026-09-08｜Brice Hill (CFO)｜margin：服務成長拆解：安裝基數每年 5–7% 加上每台平均營收提升（含 AI 調校類新服務）（原話："installed base growing every single year. 5%, 6%, 7%"）
- 2026-09-08｜Brice Hill (CFO)｜customer：DRAM 單一年產能由約 160 萬片/月，今年新增 40 萬片，未來數年每年增 30–40 萬片，且為新廠（原話："300,000 to 400,000 additional wafer starts a month"）
- 2026-09-08｜Brice Hill (CFO)｜margin：DRAM 數字口徑：升級廠設備投資約為新建廠的 25%；新建廠約 100 億美元對應 10 萬片/月（原話："about 25% of the equipment investment"）
- 2026-09-08｜Brice Hill (CFO)｜product：製程診斷與控制：電子束檢測需求顯著上升，驅動因素為 3D DRAM、4F²、GAA 到 CFET（原話："So the demand for e-beam is going up significantly"）

### AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 表示 2026 營收成長預測由 2 月 >20%、5 月 >30% 一路上調，目前接近 40%（原話："Now we're approaching 40% revenue growth"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 稱 2026 年 WFE 成長的 80% 來自先進邏輯代工、DRAM（含 HBM）與先進封裝，2027 年起同樣結構（原話："80% of wafer fab equipment growth this year"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 說明客戶提供滾動八季預測與較長期承諾（原話："rolling 8-quarter forecast and longer-term commitments"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：CEO 稱與客戶的討論已延伸到 2030 年（原話："discussions with customers all the way through 2030"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 指 Agentic AI 推高長期 WFE 預測，尤其是 CPU 與 DRAM（原話："driving increase in our longer-term WFE forecast"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：CEO 以先進製程晶圓起量比例說明資料中心需求：未來兩年資料中心對智慧手機達 2:1（原話："it will be 2:1 data center versus smartphone"）
- 2026-09-09｜Gary Dickerson (CEO)｜risk：CEO 回應是否有循環頂部警訊時，強調需求的廣度（原話："I've never seen a driver that's as broad and pervasive"）
- 2026-09-09｜Gary Dickerson (CEO)｜risk：CEO 表示不花時間擔心短期總體因素（原話："I don't really spend time worrying about macro effects"）
- 2026-09-09｜Gary Dickerson (CEO)｜risk：CEO 承認可能出現成長放緩的階段，但稱多年趨勢明確（原話："are there going to be periods of time where it's not growing"）
- 2026-09-09｜Gary Dickerson (CEO)｜risk：被問及客戶的客戶靠資本市場融資支撐資本支出時，CEO 表示不太擔心（原話："I don't worry so much about what you just talked about"）
- 2026-09-09｜Gary Dickerson (CEO)｜margin：CEO 稱服務業務年增逾 20%，服務毛利率提升 180 個基點（原話："Margins are up 180 basis points"）
- 2026-09-09｜Gary Dickerson (CEO)｜margin：CEO 給出半導體系統毛利率口徑：約五十幾％中段，一年增加約 190 個基點（原話："our semi systems gross margin is in the mid-50s"）
- 2026-09-09｜Gary Dickerson (CEO)｜commitment：CEO 對毛利率持續上升表達高度信心（未給數字）（原話："I have very high confidence we're going to continue"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 稱改採不同服務合約時，每台設備營收可超過加倍（原話："we can more than double revenue per tool"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：CEO 稱現場已有逾 3.7 萬個腔體連接至 AI 伺服器（原話："over 37,000 chambers in the field today"）
- 2026-09-09｜Gary Dickerson (CEO)｜commitment：CEO 稱 AI 內部運用主要在營收成長；會增加人力，營收成長快很多倍（原話："we will add headcount, but we're going to grow revenue"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：CEO 稱客戶遷往新地區是服務業務的順風（原話："the regionalization is a tailwind for us in our service business"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：被問 Terrafab 時，CEO 表示不談任何特定客戶（原話："I'm not going to talk about any specific customer"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 稱中國與整體 ICAPS 今年成長，並在可競爭領域小幅取得份額（原話："we're seeing growth this year in China and overall ICAPS"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 給 ICAPS 長期成長口徑為中至高個位數（原話："ICAPS grows at kind of mid- to high single digits"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 稱明年 ICAPS 成長會比今年略快，但仍慢於資料中心相關（原話："Next year, we see that business also growing a little bit faster"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 對 2027 給定性說法，不給具體數字（原話："'27 is going to be a great year for Applied"）
- 2026-09-09｜Gary Dickerson (CEO)｜commitment：CEO 稱 2027 之後成長將非常強勁（原話："beyond '27, growth is going to be very strong"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 稱先進封裝業務今年預計成長逾 70%，規模約 20～30 億美元中點（原話："is forecasted to grow over 70% this year"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 稱檢測量測業務本曆年成長逾 50%（原話："our inspection measurement business is growing over 50% this calendar year"）
- 2026-09-09｜Gary Dickerson (CEO)｜competition：CEO 稱在電子束技術上領先業界幅度大（原話："Applied is the leader in the industry by a large amount"）
- 2026-09-09｜Gary Dickerson (CEO)｜competition：CEO 稱在晶片與封裝的材料創新上規模遠大於最近的競爭對手（原話："Applied is much larger than our nearest competitor"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 稱過程控制中 e-beam 與光學兩類技術今年皆成長逾 50%（原話："growing at a very fast pace, over 50% this year"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 表示將把 80%～100% 現金回饋股東（原話："We'll return 80% to 100% of cash to shareholders"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 稱地緣政治環境下大型併購不可能（原話："it's just not possible to do large M&A"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 提及近期小型併購：面板級電鍍公司（原話："We just acquired a company in panel-level plating"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 提及另一筆 X 光技術小型併購（原話："We acquired another company with X-ray technology"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 提及混合鍵合的策略性投資，結合夥伴技術與應用材料五項技術（原話："combining a partner technology with 5 technologies"）

### 問答異常語氣（迴避／改口／保留）
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Tim Arcuri：設備成長「至少 30%」隱含下半年幾乎不再成長，為何不是 40% 以上？是保守還是有限制？｜答法：CFO 未回答保守與否，只重申 30% 年增並說不給逐季線性度，僅建議假設 FQ3 到 FQ1 以美元計線性；CEO 另指供應鏈是限制
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Tim Arcuri：華為相關限制若擴大到混合廠區，是否擴大影響？｜答法：CEO 拒絕評論限制（'I don't really want to comment on that'），僅稱已納入指引，隨即轉談 AI 運算帶動的混合
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Vivek Arya：未來 1–3 年半導體產業成長來自數量還是價格？｜答法：CEO 兩次表示不推測價格／數量（'I'm not going to speculate on pricing'），改談運算需求與市場地位
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Atif Malik：Terafab 是否在新增專案管線中？｜答法：CFO 更正自己說的是「超過 10 個」並表示無法具體點名任何專案，未回答 Terafab
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Atif Malik：大面板封裝的採用時程？｜答法：CEO 表示不願評論具體時程，改談封裝領導地位與 2026 年逾 50% 成長
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Shane Brett：製程控制市占持續下滑，策略重要性為何？｜答法：CEO 直接反駁分析師前提，未提供市占數字，改談成長與 eBeam 領導地位
- AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：2027 年成長是否優於 2026 年（定性評估）｜答法：只說 2027 會 strong、不給具體數字，且未直接比較 2027 與 2026 的成長快慢
- AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：是否看到成長延續到 2028 年｜答法：未直接回答 2028，改談算力需求與 Agentic／實體 AI 的整體論述
- AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：記憶體是否持續領先成長，或何時由先進邏輯代工接手｜答法：拒絕排序（I don't know I want to handicap one versus the other），也不給數字
- AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：與 Terrafab 的技術與商業合作程度及市場地位｜答法：不談特定客戶，改答對所有客戶的合作與產品組合

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

`scenario_inputs`（EPS路徑五年、終端倍數、機率、yield、second_stage、Max DD範圍與依據）——你不寫`scenario.json`，那份由程式跑`dd_scenario.py`產生。Bear機率5Y不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬≥50%；Base機率不應>50%；bear機率須註明依據，sourced結構性durability仍硬套bear需說明「為何不採信」否則不得高於base [§3]。
- 內生天花板sanity check：Base情境EPS CAGR貢獻vs§5.R內生天花板(同組數字不重算)→天花板內✅/超出⚠(⚠→Bear機率強制≥30%)。成長熄火：3年後成長率降至15%/10%/5%三情境×Forward P/E壓縮→估值跌幅，作Bear PE錨。三分量拆解(≤80字，Base IRR多少來自EPS複利/re-rate/股息淨回購)：re-rate貢獻≥Base合計IRR的40%→標記「估值依賴型」(`decision_inputs.valuation_dependent=true`) [§3]。
- IRR落點：<8%/yr弱、8-12%中、>12%強、>15%罕見，不作跨檔排序依據。AR=`(P_bull×|Bull5Y%|)÷(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著，非放鬆機率防線理由。年期硬規則：①表頭終端年=主時距終端年②終端倍數EPS分母年期與現價倍數同源③終端倍數必附≥1個同業現值comp對照 [§3]。10Y二段延伸(`runway_post_y5`=🟢且終端倍數承重，或Base IRR實質來自Y5後)：Y5→Y10 EPS CAGR/10Y累積倍數/IRR。R:R數學假象：下行>15%正常使用；5-15%警示「已接近定價」；<5%失效標「數學假象」禁引用進場判定，改極端Bear(Bear PE×0.8+Bear EPS×0.85)重算(Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境) [§3]。

**Max DD**(`premortem.max_dd`)：填範圍`lo`/`hi`(禁單點，寬度≥10pp)+`path_risk`(🟢0～−30%/🟡−30～−50%/🔴<−50%)；推導依據須寫`reasoning.premortem`。硬接線：🔴且thesis脆弱(`moat.trend`↓或`runway_post_y5`🔴或估值依賴型)→倉位上限下修(6%→≤3%)；🔴但thesis完整→不因波動砍倉，註記「深回撤心理準備」[§2問六]。

**必答項**：`scenario_inputs`三支EPS路徑、終端倍數、Bear/Base/Bull機率、`premortem.max_dd.lo/hi`、`path_risk`。

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
{"date":"20260626","verdict":"觀望","role":"條件式核心持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI WFE 超級週期兌現（多年·非單年 melt-up）","columns":{"2Y 驗證點":"CY26 WFE +30%·先進封裝 +50%·Q3 $8.95B","5Y 驗證點":"WFE 2027 $156B·延續「similar profile」","10Y 驗證點":"AI 算力 capex 結構需求","數字門檻":"CY26 semicap +30%·8 季客戶 forecast","來源":"AMAT Q2 FY26 法說 + SEMI + Micron $100B 合約","漂移觸發":"連 2 季 capex 下修 → 削弱"}},{"id":"H2","text":"AMAT 廣度龍頭份額 holding（邊緣流失可控）","columns":{"2Y 驗證點":"核心沉積/蝕刻份額穩·先進封裝對 LRCX 不大失","5Y 驗證點":"廣度平台地位鞏固","10Y 驗證點":"材料工程廣度無被複製","數字門檻":"製程控制份額不再大降·ICAPS China 流失可控","來源":"市佔報告（MaximizeMarketResearch/Castellano）","漂移觸發":"核心沉積/蝕刻份額流失 → 削弱"}},{"id":"H3","text":"估值極端 de-rate（de-rating ＝ 進場條件）","columns":{"2Y 驗證點":"fwd PE FY27 回測 ≤ 30x（~$490）/ BB 中軌 $423","5Y 驗證點":"倍數正常化至 10 年均上緣 25-28x","10Y 驗證點":"—","數字門檻":"fwd PE FY27 ≤ 30x","來源":"§11.1（trailing 55x vs 10 年 max 31.9x）","漂移觸發":"fwd PE 維持 &gt;45x → 進場延後"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"China 結構性 mandate + 出口管制：China 24% 營收(~$6-7B)·本土 mandate 50%→2027 70%→100%·NAURA 在 SMIC 28nm 氧化爐 &gt;60%·ICAPS($3B+/yr)結構侵蝕 + MATCH Act 擬禁 DUV 對中","columns":{"對應假設":"H1·H2","時間尺度":"🔥 中期（4-6 季）·結構慢變數","監測指標":"China 本土滲透率、MATCH Act 進度、ICAPS 中國收入 YoY","警戒閾值":"mandate 達 70% 或 MATCH Act 院會通過 或 ICAPS China 收入連 4 季降"}},{"id":"R2","text":"AI WFE 週期見頂：企業 AI 落地 &lt;40% 規模化·2027 消化·hyperscaler capex 可逆·6/25 +13.4% 為單一同業財報驅動（過度解讀風險）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"hyperscaler/記憶體 capex 指引、WFE 修訂","警戒閾值":"連 2 季 capex 下修 或 mgmt 下修 CY26 WFE"}},{"id":"R3","text":"估值極端壓縮：fwd PE 54x（10 年均 19x·+138%）·現價超共識均值 $532 約 25%·melt-up 動能過飽和","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"fwd PE 分位、動能、分析師目標 vs 現價","警戒閾值":"fwd PE 跌破 30x = 進場窗口重開（非賣出）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":2.5,"ev5y_pct":5.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式核心持倉","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":null,"ev5y_pct":5.0,"irr_base_pct":2.5,"max_dd_pct":-65.0,"bull_5y_price":955.24,"bear_5y_price":307.28,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":668.0,"archetype":null,"cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名的每一個**（含程式稍後才會算的 asym_ratio／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct／ev5y_pct／irr_base_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMAT_20261012/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
