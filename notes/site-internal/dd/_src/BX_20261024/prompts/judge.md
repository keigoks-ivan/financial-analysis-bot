你是 stock-analyst **v20 判斷 agent**，標的 BX（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"BX","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BX_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BX_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_total_revenues","label":"GAAP total revenues","value":3062.9,"period":"3Q'26（公告於 2026-10-22）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"3Q'26（公告於 2026-10-22）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"未查得"},{"id":"f_kpi1_gaap_income_before_taxes","label":"GAAP income before taxes","value":1531.0,"period":"3Q'26（公告於 2026-10-22）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"3Q'26（公告於 2026-10-22）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"未查得"},{"id":"f_kpi2_gaap_net_income_attribut","label":"GAAP net income attributable to Blackstone / EPS","value":0.83,"period":"3Q'26（公告於 2026-10-22）","unit":"USD per share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"3Q'26（公告於 2026-10-22）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"未查得"},{"id":"f_kpi3_fee_related_earnings_fre","label":"Fee Related Earnings (FRE，管理層口徑 non-GAAP 營業獲利代理)","value":1572.1,"period":"3Q'26（公告於 2026-10-22）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"3Q'26（公告於 2026-10-22）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"未查得"},{"id":"f_kpi4_distributable_earnings_d","label":"Distributable Earnings (DE)","value":1715.7,"period":"3Q'26（公告於 2026-10-22）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"3Q'26（公告於 2026-10-22）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"未查得"},{"id":"f_kpi5_net_accrued_performance_","label":"Net Accrued Performance Revenues","value":7263,"period":"3Q'26 季末（公告於 2026-10-22）","unit":"USD million","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"3Q'26 季末（公告於 2026-10-22）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"不適用"},{"id":"f_kpi6_total_aum","label":"Total AUM","value":1368.3,"period":"3Q'26 季末（公告於 2026-10-22）","unit":"USD billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"3Q'26 季末（公告於 2026-10-22）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"不適用"},{"id":"f_kpi7_gross_inflows","label":"Gross inflows","value":63.3,"period":"3Q'26（公告於 2026-10-22）","unit":"USD billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"3Q'26（公告於 2026-10-22）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"不適用"},{"id":"f_kpi8_quarterly_dividend","label":"Quarterly dividend","value":1.12,"period":"3Q'26（公告於 2026-10-22；記錄日 2026-11-02、發放日 2026-11-09）","unit":"USD per share","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"3Q'26（公告於 2026-10-22；記錄日 2026-11-02、發放日 2026-11-09）","citation":"BX 3Q'26 earnings press release（8-K Ex.99.1）"},"note":"不適用"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_bx_fcf_margin_pct","label":"BX FCF 利潤率","value":40.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kkr_gross_margin_pct","label":"KKR 毛利率","value":22.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KKR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kkr_operating_margin_pct","label":"KKR 營業利益率","value":7.84,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KKR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_kkr_fcf_margin_pct","label":"KKR FCF 利潤率","value":11.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KKR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_apo_gross_margin_pct","label":"APO 毛利率","value":95.45,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APO.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_apo_operating_margin_pct","label":"APO 營業利益率","value":24.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APO.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_apo_fcf_margin_pct","label":"APO FCF 利潤率","value":26.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APO.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ares_gross_margin_pct","label":"ARES 毛利率","value":55.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARES.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ares_operating_margin_pct","label":"ARES 營業利益率","value":18.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARES.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_ares_fcf_margin_pct","label":"ARES FCF 利潤率","value":13.96,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARES.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_blk_gross_margin_pct","label":"BLK 毛利率","value":47.15,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BLK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_blk_operating_margin_pct","label":"BLK 營業利益率","value":32.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BLK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_blk_fcf_margin_pct","label":"BLK FCF 利潤率","value":12.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BLK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":117.97,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-1.13,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":53.51,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.51,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（5.89 → 5.92）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.14,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.39 → 7.38）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-1.49,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.03 → 7.91）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":5.92,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":7.38,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":7.91,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":19.93,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 5.92，分子＝快照價 117.97","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":4.433,"period":"2026-10-24","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-24"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟠","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 117.97 / W52 127.68 / W104 140.56 / W250 116.0 / W250 13週斜率 0.08%"},{"id":"f_ma_w52","label":"52 週均線","value":127.68,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":140.56,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":116.0,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.08,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"BX 10-K 稱資產管理業競爭激烈，傳統資管機構已自建私募股權與私人財富平台；私人財富與保險通路有競爭者以較低費用或較高分銷費搶募資，且費用與附帶權益存在下降風險。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"certain traditional asset managers have developed their own private equity and private wealth platforms and are marketing other asset allocation strategies as alternatives to hedge fund investments.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"BX 10-K 稱私人財富與保險通路募資競爭，部分對手願收較低費用或付較高分銷費。","source":"SEC EDGAR 10-K FY2025 Item 1. Business","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"competition for fundraising in the private wealth and insurance channels is also driven by the willingness of certain of our competitors to charge lower fees or pay higher or different types of distributors fees.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"BX 2025 私人財富募資年增53%至$43B，私人財富AUM $300B；CFO引述分析稱BX約占主要另類資管私人財富營收50%（公司引述估計）。","source":"AltsWire 'Private wealth push propels Blackstone to record 2025 performance'","url":"https://altswire.com/private-wealth-push-propels-blackstone-to-record-2025-performance/","excerpt":null,"as_of":"2026-01-29","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K 主要客戶揭露：BCRED 於 2025 年貢獻管理與顧問費及激勵費合計 12 億美元（2024：9.806 億；2023：7.626 億）；BREIT 僅 2023 年達主要客戶門檻（8.399 億）。","source":"SEC EDGAR 10-K FY2025 Item 8 Major Customer Information","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"For the years ended December 31, 2025, 2024 and 2023, Blackstone Private Credit Fund (“BCRED”) accounted for an aggregate of $ 1.2 billion, $ 980.6 million and $ 762.6 million of Management and Advisory Fees, Net and Incentive Fees, respectively.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"BCRED 在投資人申請贖回約 10% 股份時限制贖回（首次設限）","source":"Bloomberg Law: Blackstone’s BCRED Caps Redemptions After Investors Seek 10%","url":"https://news.bloomberglaw.com/private-equity/blackstones-bcred-caps-redemptions-after-investors-seek-10-2","excerpt":"Blackstone’s BCRED Caps Redemptions After Investors Seek 10% (2) June 4, 2026, 4:26 PM UTC Olivia Fishlow Blackstone Inc.","as_of":"2026-06-04","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Blackstone 稱 BCRED 贖回申請在 Q3 初明顯下降","source":"Alternative Credit Investor: Blackstone says BCRED redemption requests have fallen","url":"https://alternativecreditinvestor.com/2026/07/23/blackstone-private-credit-strategy-returns-6-8pc-in-12-months/","excerpt":"Blackstone says BCRED redemption requests have fallen Laura Purkess News, Top 3 Blackstone","as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"BCRED 2026年Q2首次限縮贖回：投資人申請約10%，基金只兌付5%；前一季曾全額兌付7.9%申請","source":"Bloomberg Tax/Law, Blackstone's BCRED Caps Redemptions After Investors Seek 10%","url":"https://news.bloombergtax.com/private-equity/blackstones-bcred-caps-redemptions-after-investors-seek-10-2","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Stanger資料（CoStar引用）：2026年4月信用類募資年減63%至約37億美元，BDC募資年減74%；非上市BDC贖回首度超過募資","source":"CoStar, 私人信用贖回潮考驗Blackstone旗艦基金","url":"https://www.costar.com/article/1018750950/la-vague-de-remboursements-de-credits-prives-met-a-lepreuve-le-fonds-phare-de-blackstone","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"機構端需求仍在：Capital Opportunities Fund V於2026年4月達100億美元以上硬頂","source":"Pulse2, Blackstone: $10 Billion Raised For Opportunistic Credit Fund V At Hard Cap","url":"https://pulse2.com/blackstone-10-billion-raised-for-opportunistic-credit-fund-v-at-hard-cap/amp/","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Q2財報電話會：Gray稱BCRED贖回申請明顯下降（管理層自述，季初）；全球直接貸款本季流入133億美元","source":"Alternative Credit Investor, Blackstone says BCRED redemption requests have fallen","url":"https://alternativecreditinvestor.com/2026/07/23/blackstone-private-credit-strategy-returns-6-8pc-in-12-months/","excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261024","affects":["thesis.H","triggers"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"10-K 風險因子揭露：公司經常受到 SEC 及其他監管機關的資訊要求、查詢與非正式或正式調查，過去調查曾導致罰款與制裁；同時面臨 AI 法規（EU AI Act）、資料隱私與 Regulation S-P 的合規成本上升。","source":"SEC EDGAR 10-K FY2025 Item 1A Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"We regularly are subject to requests for information, inquiries and informal or formal investigations by the SEC and other regulatory authorities, with which we routinely cooperate, and which have included review of historical practices that were previously examined. Such investigations have previously and may in the future result in penalties and other sanctions.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"美國眾議院金融服務委員會民主黨議員就私募信貸向 Blackstone、Ares、KKR 等發函詢問","source":"Bloomberg 轉載：Blackstone, Ares Rivals Grilled by Congress Over Private Credit","url":"https://www.ebsco.com/articles/history/bac00083-ad7b-5ce1-9954-16977fd37afa/blackstone-ares-rivals-grilled-by-congress-over-private-credit","excerpt":"The article focuses on the Democratic members of the House Financial Services Committee investigating major private credit firms, including Blackstone Inc., Ares Management Corp., Apollo Global Management Inc., BlackRock Inc., Blue Owl Capital Inc., Carlyle Group Inc., and KKR & Co.","as_of":"2026-04-01","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Blackstone 子公司 LivCor 與九州就租金合謀反壟斷案以 700 萬美元和解","source":"Law360：Blackstone's LivCor Cuts $7M Rent-Fixing Deal With 9 States","url":"https://www.law360.co.uk/amp/articles/2491505","excerpt":"Blackstone's LivCor Cuts $7M Rent-Fixing Deal With 9 States By Dorothy Atkins June 18, 2026, 6:49 PM EDT Blackstone subsidiary LivCor LLC has agreed to pay North Carolina, California and seven other states $7 million in penalties to resolve allegations against it in a sprawling antitrust lawsuit alleging major...","as_of":"2026-06-18","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 風險因素：關稅與報復性關稅可能提高被投資組合公司成本、壓縮利潤並降低競爭力，已對部分在美國有大量實體商品銷售的公司造成不利影響；2026年2月最高法院裁定多項關稅越權，政府隨後改以其他法律課徵全球關稅，後續走向不明。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"Increased tariffs on goods imported from China, Canada, Mexico and other countries could further increase, costs, decrease margins and reduce the competitiveness of products and services offered by our portfolio companies. This has and could further adversely impact the revenues and profitability of select companies that have substantial sales of physical goods in the U.S.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"10-K 指出美國對中國實體的制裁與出口管制，以及美中貿易戰升級，可能影響投資機會與全球成長，進而影響各基金被投資組合公司的營收與獲利。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"Further escalation of the “trade war” between the U.S. and China, the countries’ inability to reach further trade agreements, or the continued use of reciprocal sanctions by each country, may negatively impact opportunities for investment as well as the rate of global growth, particularly in China","as_of":"2026-02-27","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Blackstone 亞洲私募基金募得131億美元超過目標，重心在印度、日本等市場","source":"International Finance: Blackstone raises USD 13.1 billion for its Asia fund, exceeds target","url":"https://internationalfinance.com/asset-management/blackstone-raises-usd-13-1-billion-for-its-asia-fund-exceeds-target/","excerpt":"Markets like Japan and India, known for offering a steady pipeline of buyout and growth opportunities, have been a major focus area for global asset managers.","as_of":"2026-06-04","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"-","claim":"Real Estate 段 3Q26 營收 $893.3M、年減 6%；FRE $499.2M 年減 9%；季流入 $6.3B；AUM $309.0B 年減 4%","source":"Blackstone 3Q26 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001393818/000119312526428297/d160590dex991.htm","excerpt":"inflows of $6.3 billion in the quarter","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.R","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Private Equity 段 3Q26 營收 $1,349.8M 年減 6%；FRE $618.9M 年增 26%；季流入 $12.6B；AUM 年增 18% 至 $465.4B","source":"Blackstone 3Q26 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001393818/000119312526428297/d160590dex991.htm","excerpt":"inflows of $12.6 billion in the quarter","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Credit & Insurance 段 3Q26 營收 $783.9M 年增 2%；FRE 年減 1%；季流入 $35.8B；AUM 年增 11% 至 $480.0B","source":"Blackstone 3Q26 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001393818/000119312526428297/d160590dex991.htm","excerpt":"inflows of $35.8 billion in the quarter","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Multi-Asset Investing 段 3Q26 營收 $189.5M 年增 25%；FRE 年增 26%；季流入 $8.6B；AUM 年增 22% 至 $113.9B","source":"Blackstone 3Q26 earnings release (8-K Ex.99.1)","url":"https://www.sec.gov/Archives/edgar/data/0001393818/000119312526428297/d160590dex991.htm","excerpt":"inflows of $8.6 billion in the quarter","as_of":"2026-10-22","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"PitchBook 2Q26：私募債 TTM 募資 $309.1B 年增 14.0%；不動產募資 $90.7B 年減 32.5%；私募資本總額 $1,348.0B 年減 12.7%","source":"PitchBook Q2 2026 Global Private Market Fundraising Report","url":"https://pitchbook.brightspotcdn.com/74/45/4f36da844589a606c5cea79f2aeb/q2-2026-global-private-market-fundraising-report.pdf","excerpt":"$90.7 -32.5% 357 -39.1% Real assets $137.3 -26.2% 99 -52.4% Private debt $309.1 14.0% 259 -39.6% Fund of funds $26.5 -57.2% 92 -66.1% Secondaries $95.1 -20.6% 73 -30.5% Co-investment $37.5 -18.3% 206 -46.4% Private capital $1,348.0","as_of":"2026-07-15","retrieved_at":"20261024","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"Preqin：預期 2030 年私募信貸 AUM 達 $4.5tn；2026 不動產募資反彈","source":"Preqin Global Reports 2026 key findings","url":"https://www.preqin.com/insights/research/reports/preqin-global-reports-2026-key-findings","excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"-","claim":"BCRED 1Q26 贖回申請 7.9%、淨流出約 $1.4B，被分析師視為 BX 費用與 FRE 的壓力點","source":"Simply Wall St narrative (via search)","url":"https://simplywall.st/narratives/bip-expansion-and-global-wealth-will-create-new-opportunities","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"BX 10-K 風險因素自述：AI 技術可能大幅顛覆其商業模式、投資策略、營運流程與所處市場，並使 BX 及投組公司面臨更高競爭、法律監管風險與合規成本；部分同業在 AI 平台上可能比 BX 更成功。","source":"SEC EDGAR 10-K FY2025 Item 1A","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"AI Technologies could significantly disrupt the business models, investment strategies, operational processes, and markets in which we operate. Similarly, AI Technologies could significantly disrupt our portfolio companies’ businesses and markets.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Morningstar：對 AI 顛覆軟體公司的擔憂與私募信貸疑慮壓抑另類資管股價；BCRED 當季募資 10 億美元，低於前季 19 億與去年同期 37 億。","source":"Morningstar Financial Services: Concerns About AI Disruption and Private Credit Weigh on Sector","url":"https://www.morningstar.com/stocks/financial-services-concerns-about-ai-disruption-private-credit-weigh-sector","excerpt":"We downgraded many of our economic moat ratings on software firms in response to rapidly improving AI capabilities, with flow-through impacts on those firms’ pricing power, long-term growth prospects, and valuations.","as_of":"2026-04-01","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"10-K 稱 Blackstone 業務已從機構投資人擴及透過多種通路銷售給高淨值與大眾富裕個人的產品；私人財富通路占總 AUM 比重逐年上升，預期延續，並在拓展 401(k)等 DC 通路。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"In recent years, capital from the private wealth channel has represented an increasing portion of our Total Assets Under Management, and we expect this trend to continue as we continue to undertake initiatives focused on this market segment.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"-","claim":"10-K 指出私人財富與保險通路競爭激烈，部分競爭者願收較低費用或付較高分銷費。","source":"SEC EDGAR 10-K FY2025 Item 1","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"In addition, competition for fundraising in the private wealth and insurance channels is also driven by the willingness of certain of our competitors to charge lower fees or pay higher or different types of distributors fees.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"私人財富通路 AUM 於 2026-06-30 達 $324B（2026-03-31 為 $310B）；Q2 2026 私人財富 AUM 年增 16%，BXPE NAV 逾 $25B。","source":"Blackstone BXINFRA 基金頁；Nasdaq「Blackstone Q2 earnings call highlights」","url":"https://www.nasdaq.com/articles/blackstone-q2-earnings-call-highlights","excerpt":"Blackstone's private wealth AUM grew 16% year-over-year to a record $324 billion.","as_of":"2026-07-23","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#3","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"Blackstone 於 2026-01-14 加入 Empower 私募市場夥伴計畫，經集合投資信託(CIT)與顧問管理帳戶切入 401(k)；2025-10 已成立專屬退休解決方案部門。","source":"Alternative Credit Investor「Blackstone partners with Empower in 401(k) push」","url":"https://alternativecreditinvestor.com/2026/01/14/blackstone-partners-with-empower-in-401k-push/","excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 頁面顯示 BX 分析師平均目標價約 $156（27 位）、最高 $195、最低 $122；Wells Fargo 於 2026-10-02 以 Equal-Weight、$122 啟動覆蓋。","source":"Benzinga BX sentiment page","url":"https://www.benzinga.com/quote/BX/sentiment","excerpt":"Avg Consensus PT $156, Highest Price Target $195, Lowest Price Target $122","as_of":"2026-10-02","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"S&P Global 彙整（StockAnalysis，2026-07）：22 位分析師共識評級 Buy，平均目標價 $142.7。","source":"StockAnalysis BX forecast","url":"https://www.stockanalysis.com/stocks/bx/forecast/","excerpt":"According to 22 analysts polled by S&P Global, Blackstone stock has a consensus rating of \"Buy\" and an average price target of $142.7.","as_of":"2026-07-15","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"BX 3Q'26 Total Segment Distributable Earnings 為 $19 億，低於 2Q'26 的 $22 億；未找到 3Q'26 分析師共識 EPS 與公司 guidance 對照。","source":"Blackstone 8-K Ex.99.1 (3Q'26)","url":"https://www.sec.gov/Archives/edgar/data/0001393818/000119312526428297/d160590dex991.htm","excerpt":null,"as_of":"2026-10-23","retrieved_at":"20261024","affects":["valuation","thesis.R"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Blackstone Infrastructure 以每股 $61.25 現金收購 TXNM Energy（EV $11.5B，2025-05 宣布）；股東 2025-08 通過，PUCT／FERC／FCC 已核准，NRC 與新墨西哥 PRC 未決；終止日延至 2027-05-31，預計 2027 上半年交割。","source":"pulse2.com：TXNM Energy And Blackstone Infrastructure Extend Merger Agreement To May 2027","url":"https://pulse2.com/txnm-energy-and-blackstone-infrastructure-extend-merger-agreement-to-may-2027/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261024","affects":["valuation","triggers"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Blackstone 旗下基金 2026-07-20 宣布投資韓國致動器供應商 Futronic（媒體報導估值約 1 兆韓元／約 $675M），創辦人留任；官方稿未列價格。","source":"Blackstone 新聞稿：Blackstone Announces Investment in FUTRONIC","url":"https://www.blackstone.com/news/press/blackstone-announces-investment-in-futronic-koreas-leading-actuator-and-motion-control-technology-provider/","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Kentucky 退休基金（KRS）相關訴訟：2025-01 的 $82.5M 和解因法院拒絕核發核准令而終止，雙方仍在討論，尚無新和解。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"In May 2025, the Court declined to enter an approval order, holding that the Court’s approval is unnecessary and stating that the parties may settle as they see fit. Because an approval order was a condition to the settlement, the settlement agreement was terminated.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 11 份 8-K 中重大項目 3 份，皆為 2025-10/11 的優先債券發行（1.01／8.01），無 4.02（重編）項目。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001393818&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Blackstone Infrastructure 收購 TXNM Energy（$61.25/股現金、EV $11.5B）仍待 NRC 與新墨西哥 PRC，終止日延至 2027-05-31。","source":"pulse2.com：TXNM Energy And Blackstone Infrastructure Extend Merger Agreement To May 2027","url":"https://pulse2.com/txnm-energy-and-blackstone-infrastructure-extend-merger-agreement-to-may-2027/","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261024","affects":["valuation","triggers"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"2026-07-20 宣布投資韓國 Futronic（約 $675M 估值，媒體報導）。","source":"Blackstone 新聞稿：Blackstone Announces Investment in FUTRONIC","url":"https://www.blackstone.com/news/press/blackstone-announces-investment-in-futronic-koreas-leading-actuator-and-motion-control-technology-provider/","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Kentucky KRS 相關訴訟：$82.5M 和解於 2025-05 因法院未核發核准令而終止，尚無新和解；搜尋未見針對 BX 的新證券集體訴訟。","source":"SEC EDGAR 10-K FY2025 Item 8","url":"https://www.sec.gov/Archives/edgar/data/1393818/000119312526082531/d48618d10k.htm","excerpt":"While the parties are continuing their discussions, they have not reached a new settlement.","as_of":"2026-02-27","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 8-K 清單無 Item 4.02（重編）；搜尋僅見 2015 年舊 SEC 和解，未見近期 SEC 調查或重編。","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001393818&type=8-K","excerpt":"SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 11 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 3 份。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]},{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"BX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":40.3,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BX","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KKR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":22.49,"operating_margin_pct":7.84,"fcf_margin_pct":11.11,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KKR","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"APO","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":95.45,"operating_margin_pct":24.85,"fcf_margin_pct":26.39,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.APO","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ARES","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.81,"operating_margin_pct":18.08,"fcf_margin_pct":13.96,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ARES","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"BLK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":47.15,"operating_margin_pct":32.99,"fcf_margin_pct":12.88,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BLK","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"BX"},"financial_history":{"ticker":"BX","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":7132632000.0,"revenue_yoy_pct":null,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":1747631000.0,"diluted_eps":2.36,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":7006649000.0,"revenue_yoy_pct":-1.77,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":1390880000.0,"diluted_eps":1.84,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":10930540000.0,"revenue_yoy_pct":56.0,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":2776508000.0,"diluted_eps":3.62,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":12410012000.0,"revenue_yoy_pct":13.54,"gross_margin_pct":null,"operating_margin_pct":null,"net_income":3019214000.0,"diluted_eps":3.87,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/BX/BX_Q3_2026_Earnings_Call_20261022.md）

# Q3 2026 Earnings Call
**Blackstone Inc.** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Good day, and welcome to the Blackstone Third Quarter 2026 Investor Call. Today's call is being recorded. [Operator Instructions]
At this time, I'd like to turn the conference over to Weston Tucker, Head of Shareholder Relations. Please go ahead.

**Weston Tucker** (Executives):
Great. Thanks, Katie, and good morning, and welcome to Blackstone's third quarter conference call.
Joining me today are Steve Schwarzman, Chairman and Chief Executive Officer; Jon Gray, President and Chief Operating Officer; and Michael Chae, Vice Chairman and Chief Financial Officer.
Earlier this morning, we issued a press release and slide presentation, which are available on our website. We expect to file our 10-Q in a few weeks.
We'd like to remind you that today's call may include forward-looking statements, which are uncertain and may differ from actual results materially. We do not undertake any duty to update these statements. For a discussion of some of the factors that could affect results, please see the Risk Factors section of our 10-K. We'll also refer to non-GAAP measures, and you'll find reconciliations in the press release on the shareholders page of our website. Also note that nothing on this call constitutes an offer to sell or a solicitation of an offer to purchase an interest in any Blackstone fund. This audio cast is copyrighted material of Blackstone and may not be duplicated without consent.
On results, we reported GAAP net income for the quarter of $1.3 billion. Distributable earnings were $1.7 billion or $1.32 per common share, and we declared a dividend of $1.12 per share, which will be paid to holders of record as of November 2.
With that, I'll now turn the call over to Steve.

**Stephen Schwarzman** (Executives):
Third quarter of 2026 represented a highly complex environment, characterized by an historic increase in bond yields globally, including U.S. Treasury yields hitting the highest level in decades, alongside continued geopolitical turbulence, wars in the Middle East and Ukraine, inflation concerns, high oil prices, sovereign debt worries, uncertainty over the U.S. midterm elections, and other challenges. These challenges have continued post quarter end. On the one hand, the artificial intelligence revolution is powering robust growth in many areas, while on the other hand, a higher cost of capital has negatively impacted investor sentiment and transaction activity and triggered significant volatility in the markets. 
The S&P 500 Index rose slightly in the third quarter with gains concentrated in the largest tech companies and the energy sector, although most individual stocks declined and the median stock is now 15% below its recent high. Against this challenging backdrop, Blackstone reported strong distributable earnings of $1.7 billion in the quarter, underpinned by continued year-over-year growth in fee-related earnings, notwithstanding fewer realizations as we indicated would be the case on our last call. Inflows reached $63 billion in the quarter, reflecting sustained momentum across our major fundraising channels and exceeded $270 billion for the last 12 months, the highest level in 4 years. 
Most importantly, in terms of investment performance, our flagship strategies outperformed the relevant market indices in the third quarter, led by infrastructure and our energy holdings. Overall, the unparalleled breadth of our firm and the leading platforms we've established across asset classes have allowed us to navigate changing market conditions, deploy capital in the most compelling areas and continue to build value for our limited partners. For shareholders, the firm's underlying earnings power continues to expand substantially, and we are moving towards what we expect will be an outstanding 2027. 
Stepping back, the economy is strong today. The key catalyst, as I mentioned, is the historic level of investment taking place to facilitate the development of AI, including data centers, chips, equipment, power generation, construction and engineering services and many other related areas. This engine is supporting exceptional corporate earnings momentum as well as momentum in our own portfolio. We also believe we're in the earliest stages of an AI-driven uplift in productivity and consequently, an additional multiyear tailwind for corporate earnings and value creation. 
Rising productivity over time is also a potential mitigant for inflation. Over the past few weeks, however, we've seen an increased focus in the market on the sustainability and risks of AI-related investment, the significant financing needs of companies involved in the AI build-out in the context of higher interest rates and the levels of valuations. As we've stated before, we believe the transformative power of AI has precedent in the industrial revolution and the commercialization of electricity, and we are in the earliest stages of its development. Demand for compute is accelerating, and we see no signs of that slowing down as AI use cases ramp for both businesses and consumers and the world increasingly engages with the vast potential of this technology. 
At the same time, there's a critical scarcity of supply that is only intensifying. Seldom in my career have I seen such a supply-constrained market of this scale. Current public attitudes towards data centers will likely only amplify this scarcity. Over time, as the public comes to understand the advancements that have occurred in data center operations and construction, including with respect to water usage and the funding for electricity, these attitudes should change. We also anticipate new laws and regulations codifying these advancements will be implemented. Of course, there are risk factors to consider. There will be situations where investors don't have sufficient capital and projects can't procure power, equipment or the necessary approvals. 
At Blackstone, we approach investments in this area with the same rigor and focus on risk-adjusted returns that have defined our investment process for 4 decades. In AI infrastructure, for example, our data center portfolio is built on durable long-term contracts with highly creditworthy counterparties. Overall, we keep coming back to the fundamental supply-demand imbalance, which supports our conviction that this is the right place to invest significant capital. As the AI revolution progresses, the rising demand for capital is creating generational opportunities for those with the platform, relationships, capabilities and discipline to meet this demand. Blackstone has become one of the most important capital providers in the AI ecosystem. 
We started with our data center development business, focused on serving the major hyperscalers, which provided the foundation for deep partnership with many of today's AI leaders. And we've been teaming up with them in multiple ways. We've previously announced the launch of Crux, our partnership with Google to help address the shortage of compute. We've also created Ode with Anthropic to drive enterprise adoption of AI. And in August, NVIDIA named Blackstone as one of the small group of managers to work with to deploy $500 billion of large-scale GPU financing. At the same time, in the energy area, electrification, reindustrialization and of course, AI are leading to accelerating demand for power following decades of static demand. With one of the largest private energy investing platforms across debt and equity, Blackstone is at the center of this megatrend as well. 
We are actively investing across generation, transmission, storage equipment and services and more. In the third quarter, we invested in a leading developer of renewable projects in Europe and committed to acquire a supplier of components for data center cooling systems. In August, our portfolio company, Lancium, which is providing energy infrastructure to OpenAI's flagship data center in Texas, announced a strategic investment from NVIDIA to help fund its development of low-cost scale power. And in credit, our energy business backed approximately 15% of solar and storage projects in the entire United States last year. And together with our equity business has supported nearly 50% of LNG export capacity. 
Of course, it's much more than AI and energy driving our firm forward. Blackstone has established leading platforms to address other paradigm shifts we see shaping the economy and markets. Private credit is becoming a crucial source of financing for the real economy, and we manage the world's largest third-party focused private credit business. Advancements in drug development are accelerating, and we've built the largest sponsor-backed life sciences platform. India continues its ascent as the fastest-growing major economy, and we are one of the country's largest private investors. Private markets themselves remain on a strong growth trajectory, leading to significant opportunities in secondaries, where we oversee one of the largest businesses. And defense is an area that's in critical need of global capital, and we've been highly active here as well, addressing this need in numerous ways. 
The firm's positioning across these and other areas powers our deployment, fuels fundraising and ultimately translates to greater earnings for shareholders, the virtuous circle underpinning our business. And as always, the Blackstone innovation engine continues to fire, and we are investing today in the leading platforms of tomorrow. Despite the firm's extraordinary record of growth over 4 decades and our unique positioning in the alternative sector, Blackstone's stock, along with the other alternative managers has been under pressure. This is due to some of the factors I discussed earlier, along with AI disruption and private credit concerns. Over the past 2 years, while our shares are down meaningfully, our earnings have grown nearly 50% with commensurate growth in our dividend. In my experience, disconnects of this type don't typically last. 
We've seen similar drawdowns for Blackstone's stock before. And each time, our shares ultimately recovered and dramatically outperformed any index comparison on the way back up, following the fundamental trajectory of our business. I have learned the most important thing during these periods is to keep our focus on delivering great results for limited partners, pioneering new markets for investment and expanding our fundraising channels, all of which are occurring now. Our firm has enormous earnings power, and we expect outstanding results in the years ahead. I believe the future for Blackstone will be remarkable. 
And with that, I'll turn it over to Jon.

**Jonathan Gray** (Executives):
Thank you, Steve, and good morning, everyone. In a world where demand for capital is rising, private markets are more critical than ever, helping to bridge the funding gap and support continued technological innovation. Steve discussed our unique positioning across the world's most important investment themes, which is driving our results. At the same time, the markets from which we raise capital are expanding significantly, including in the vast wealth and insurance channels. Meanwhile, in our institutional business, investor confidence in Blackstone remains extremely high, which is translating to greater capital commitments in many areas. I will focus my remarks on these growing sources of inflows for the firm. 
Starting with private wealth, where we delivered another outstanding quarter. Our total AUM in the channel grew 15% year-over-year to a record $330 billion with nearly $9 billion of sales in the quarter. Fundraising for our perpetual strategies was up materially from Q2 despite the slowdown in credit, and we launched a number of new products. Our private equity flagship in the wealth channel, BXPE, reported record sales in the third quarter of $2.9 billion, bringing its NAV to $29 billion in less than 3 years, the largest platform of its kind in the world. Of course, it's all about investment performance and BXPE has delivered, achieving an 18% net annualized return since inception. 
BREIT grew 9% year-over-year to $58 billion and saw its best regular way net flows in 4 years in the third quarter. BREIT has generated 21 consecutive months of positive returns and approximately 11% net over the last 12 months for its largest share class. And BXINFRA reported its highest quarterly sales since launch nearly 2 years ago at $1.1 billion, bringing NAV to over $7 billion, underpinned by a 17% annualized net return for its largest share class. The exceptional portfolio positioning of these strategies continues to power our returns. For BCRED, gross sales were nearly $750 million in the third quarter. Repurchase requests were 10% of NAV, above the 5% quarterly limit, largely driven by carryover requests from Q2. We fulfilled approximately 50% of total requests, resulting in net outflows of $1.4 billion in the third quarter. 
Investors who requested a redemption each of these 2 quarters of proration received 75% of their capital back in about 90 days, another illustration of the semi-liquid structure working as designed. Meanwhile, our innovation in the wealth channel is accelerating. Our new perpetual hedge fund product, BXHF, had a strong start out of the gates, raising approximately $400 million, including October 1 subscriptions. This strategy adds another core building block to our suite of solutions. We also launched a new vehicle outside of the U.S. that invests across our wealth strategies, Blackstone Private Markets Funds, or BXPM, which we refer to as Blackstone in a Box. And the first 2 funds in our alliance with Wellington and Vanguard went live in the third quarter, including WVB Blackstone All Privates Fund, which gives investors in the U.S. access to Blackstone's platform in a single allocation. The opportunity in private wealth continues to expand for the firm. 
Moving to the insurance channel, where our AUM grew 14% year-over-year to more than $300 billion. Insurance companies continue to turn to private markets for excess spread, and they're turning to Blackstone for our open architecture multi-client model and access to differentiated deal flow. We've established the largest non-captive insurance platform in our industry, including 40 clients in our dedicated insurance solutions area, representing leading global firms, of which over half expanded their relationship with us in the past 12 months. Our investment-grade private credit platform specifically grew 24% year-over-year to nearly $150 billion. This platform is comprised primarily of insurance capital today, but our engagement with pensions, sovereign wealth funds and other LPs is growing. 
Stepping back, there are 2 key developments underpinning the massive secular shift underway toward investment-grade private credit. First, the build-out of digital energy and transportation infrastructure is creating compelling deployment opportunities of very significant scale. Second, large IG-rated corporates are increasingly looking to private markets for bespoke nondilutive capital solutions backed by specific assets to support their balance sheet objectives and fund growth. And Blackstone is well positioned to be the partner of choice given the breadth of our platform capabilities and reputation. Our recent activity includes large-scale financings in numerous sectors around the world, including communications infrastructure and an airline loyalty program in Canada, residential real estate in Australia and digital and energy infrastructure globally. 
For our clients, we are originating high-quality, long-duration investments with favorable counterparty risk, all while generating a premium yield over comparably rated liquid credit. At the same time, our noninvestment-grade credit platform continues to perform quite well. Our flagship funds reported healthy returns in the third quarter, which Michael will discuss. In direct lending, AUM grew 10% year-over-year to nearly $170 billion despite muted flows for BCRED. Inflows from our institutional LPs remain robust, and they're looking to deploy in a lending backdrop that has become more attractive. Overall, our institutional business continues to show solid momentum with AUM up 7% year-over-year. In infrastructure, our dedicated platform grew a remarkable 40% year-over-year to $97 billion. We are approaching the $100 billion milestone only 8 years after launch achieved entirely organically, underpinned by 19% net annual returns since inception in the commingled BIP strategy. 
Our multi-asset investing business, BXMA, has reemerged as a growth engine for the firm. AUM increased 22% year-over-year to $114 billion with record organic net inflows in Q3. BXMA delivered its 26th consecutive quarter of positive returns for its largest strategy. In our drawdown fund area, it was another active quarter of fundraising. We held additional closings for our new private equity flagship secondaries vehicle with over $16 billion raised to date toward a target of at least $22 billion, along with our real estate secondaries vehicle. We also raised additional capital for our fifth private equity energy transition fund, BETP V, which hit its $8.7 billion hard cap post quarter end, more than 50% larger than the prior fund. This represents the fourth major drawdown fund at Blackstone to hit its hard cap this year, all of which were meaningfully larger than predecessors and had excess demand. And we expect a fifth, our asset-based finance drawdown vehicle in credit, to hit its $4.2 billion hard cap soon. 
Institutional investor interest clearly remains strong for high-performing Blackstone strategies. Looking forward, we launched fundraising for our new credit energy transition and infrastructure vehicle, targeting a larger size than the prior $7.1 billion vintage, and we'll soon begin raising our third longer-dated core private equity vintage. 
I'll finish my remarks today with a comment on real estate, where we've been navigating a volatile interest rate environment. In the third quarter, we increased valuation cap rates across our holdings in response to the increase in base rates, which led to depreciation in our opportunistic real estate funds. Importantly, while higher rates are a headwind to the sector's recovery, strengthening fundamentals are a tailwind. In 2022, in contrast, when the Fed began its rate hiking cycle, cash flow growth was decelerating across many areas of commercial real estate due to meaningful new supply coming online. Today, there are 3 positive dynamics that didn't exist in 2022. First, demand is accelerating in key sectors, including data centers, where we expect a threefold increase in leasing this year across our global platform, and logistics, where our U.S. holdings saw record leasing activity in Q3. These 2 sectors represent 54% of our global real estate portfolio. 
Second, new supply has fallen to a decade-plus low across many types of real estate, while the cost to build continues to increase, with development further accelerated by higher rates and crowding out from the AI infrastructure build. And third, real estate debt markets have remained resilient, unlike in '22, with the availability of debt up sharply this year. This doesn't mean there won't be legacy equity and debt investments in real estate that will face renewed pressure from higher rates, particularly in lower growth sectors. But in this cycle, as with past cycles, we believe we are in a differentiated position overall given where we've concentrated our capital and the quality of our portfolio. 
In closing, the firm's commitment to our clients is as strong as ever, and we are laser-focused on delivering for them. For shareholders, Blackstone remains brand-heavy asset-light manager with minimal net debt and a compelling recurring revenue model, and we firmly believe with lots of growth ahead. 
With that, I will turn things over to Mr. Chae.

**Michael Chae** (Executives):
Thanks, Jon, and good morning, everyone. Firm delivered resilient financial results and overall fund performance in the third quarter and for the first 9 months of the year, generated double-digit year-over-year growth across fee revenues, fee-related earnings, realized performance revenues and distributable earnings, all against a backdrop of significant external volatility. 
Starting with results. The firm's expansive breadth lifted AUM to new record levels. Total AUM rose 10% year-over-year to approximately $1.4 trillion with double-digit growth across 3 of our 4 segments, including robust momentum in private equity and BXMA and healthy growth in credit, notwithstanding declines in real estate, as we've discussed. Total fee revenues for the firm rose 8% year-over-year to $2.7 billion. Base management fees reached a record $2 billion in the quarter, trending on the path we previously outlined, underpinned by year-over-year growth of 13% in private equity and 22% in BXMA. Transaction and advisory fees increased 34% year-over-year to $210 million in Q3, reflective of the continued expansion of the firm's platform. Fee-related performance revenues grew 19% year-over-year to $540 million with contribution from 10 perpetual strategies, including BREIT in real estate, BCRED in credit, BIP and BXINFRA in Infrastructure and BXPE in private equity. Fee-related earnings were $1.6 billion in the quarter, up 6% year-over-year, equating to $1.26 per share. 
Distributable earnings were $1.7 billion or $1.32 per share, underpinned by the strong FRE generation. With respect to net realizations, we said on our last call that we expected a sequential decline in Q3 and net realizations were down 20% quarter-over-quarter. Even so, we were able to execute a number of dispositions with the largest source for multiple exits in our Asia portfolio, specifically in Japan and India. 
Stepping back, the firm has delivered strong financial performance in 2026 despite the year's considerable geopolitical disruptions and market volatility. For the year-to-date period through Q3, total fee revenues and FRE both grew 17% year-over-year. Realized performance revenues were up 12% and DE increased 12% as well, all while seeing positive momentum across fundraising, investment activity and fund appreciation, the key leading indicators of future financial performance. And as we move towards year-end and into 2027, the setup is quite favorable. First, with respect to Q4, we anticipate a significant step-up in net realizations in the fourth quarter, including the sales of multiple companies. In addition, BXMA crystallizes performance revenues in the fourth quarter of each year for most of its open-ended strategies with strong returns year-to-date as do a number of strategies across the credit complex. 
As we look ahead to 2027, we expect to return to double-digit year-over-year growth in base management fees with key drivers including the onset of fees from multiple new drawdown funds in private equity, continued expansion of our perpetual platform, growth in credit and insurance and the very positive momentum in BXMA. At the same time, the firm's increasingly diversified and scaled base of fee-related performance revenues is a source of strength, including notably our institutional infrastructure strategy, which will see its next large-scale crystallization of these revenues in 2027 in the context of its remarkable investment performance and the surface area for generating transaction fees continues to expand, an underappreciated engine of fee revenue growth for the firm. Meanwhile, the firm's embedded realization potential has continued to build. The net accrued performance revenue receivable on our balance sheet, the firm's store of value now stands at $7.3 billion, up 12% year-over-year, equating to nearly $6 per share. 
Nearly 1/3 of the receivable in corporate private equity is public and liquid, while the receivable in our private equity energy business has more than doubled year-over-year. This brings me to investment performance. Amid rising interest rates and significant market volatility, nearly all of our flagship strategies generated positive appreciation in the third quarter and outperformed comparable indices. Our dedicated infrastructure platform appreciated 6.4% in Q3, underpinned by continued extraordinary leasing momentum in our global data center portfolio, as Jon highlighted. For the last 12 months, our infrastructure platform appreciated a remarkable 29% compared to a 4% return for the global Infrastructure Index over the same period. 
The private equity funds appreciated 2.8% in the third quarter and 15% for the last 12 months, with our holdings in power and electrification representing the largest gains in the quarter. Overall, our private equity operating companies continue to report healthy underlying fundamentals, including low double-digit revenue growth and strength in margins. In credit, our noninvestment-grade private credit strategies reported a gross return of 2.6% in the quarter and 7% for the last 12 months, reflecting stable underlying credit performance across the vast majority of our holdings alongside steady current income. Meanwhile, BXMA reported a 0.5% gross return for the absolute return composite in Q3 compared to a decline in the HFRX Hedge Fund Index and 13% for the LTM period, which was more than double the hedge fund index. BXMA seeks to outperform liquid markets over time with less volatility, and it has done just that, beating the traditional 60-40 portfolio by 170 basis points per year since the start of 2020. 
Finally, in real estate, the Core+ funds reported positive appreciation of 1.6% in the third quarter, while the BREP opportunistic funds declined 3.2%. Widening cap rates were partially offset by leasing momentum in data centers as well as interest rate hedges. Areas with lower growth were more impacted, including our multifamily housing portfolio. Despite the cost of capital headwinds, favorable portfolio positioning led to positive performance across all 3 of the most recent vintages of our BREP strategies in Q3, global, Asia and Europe and double-digit appreciation in these funds over the last 12 months, including 17% LTM appreciation for our latest BREP global fund, 24% for Asia and 13% for Europe. 
In closing, the firm continues to demonstrate resiliency and fundamental strength. In a very challenging environment, we've delivered double-digit growth across AUM, revenue and earnings, and we believe we are very well positioned for the road ahead. 
Thank you for joining today's call, and we would like to open it up now for questions.

**Operator** (Operator):
[Operator Instructions] We will take our first question from Michael Cyprys with Morgan Stanley.

**Michael Cyprys** (Analysts):
So the market seems to be reacting to perceived risks from AI-related investments in the context of a higher cost of capital backdrop. Just curious how sensitive in your view is this financing build-out to higher rates more broadly, where are you seeing risks here? And how are you protecting your capital from risk of lower-than-expected returns with the AI complex? I know you've talked about long-term contracts, high-quality counterparties. But what risk do those contracts not protect you against?

**Jonathan Gray** (Executives):
Well, Mike, obviously, it's an area the market is very focused on today. I would start with where we've really focused, which is on providing compute, which seems to be the area where there are the greater constraints. We continue to see very significant demand at our companies; spending it on models is up 20-fold over the last year. We see all sort of productive uses continuing to expand across our portfolio, and we think demand will grow. And the challenge, of course, is chips and data centers and our -- and amassing capital at scale. And we think at Blackstone were very unique because we can provide integrated solutions. We can provide power solutions, we can provide financing solutions. We can obviously provide data center solutions. And the vast majority of what we're doing is long-term contracted.  
And in the case of the data centers, as you pointed out, these are assets with 15- to 20-year contracts with companies who have $2.5 trillion market caps on average. So I would say for our data center business, in particular, the fact that we wait until we have these long-term contracts before we put the vast majority of capital on the ground, that seems to be a very disciplined approach to deploying capital. And if anything, all the pushback and the squeeze on capital availability and a bit of the shakeout that we're seeing puts us in, I think, a pretty unique space. The fact that we have expertise and that we can amass capital, we can do very interesting things. It's happening in credit. It's obviously happening in real estate and infrastructure here for us.  
So we're aware of the risk whenever you have this kind of large investment boom, which is why we focus so much on the picks and shovels while we focus so much on long-term contracted assets, while we focus on not doing things on a speculative basis, all of that makes us feel very good. And if anything, as I said, the shortage of compute is growing and that's making what we build, the entitled sites we have that are powered, they're actually more valuable today. And I think we'll begin to see even larger sites, more concentrated and more integrated with some of our energy solutions. 
So we understand that it's a world where people are focused, but the CapEx cycle and the need for compute will continue. There seems to be fewer players who can do this, and that puts us and our investors, we think, in a very good spot.

**Operator** (Operator):
We'll take our next question from Bart Dziarski with RBC Capital Markets.

**Bart Dziarski** (Analysts):
Just wanted to ask around the private wealth fundraising momentum that you're seeing. We're seeing acceleration in 3 of the 4 asset classes. Maybe you can talk through -- I know performance was mentioned, but some of the key drivers and momentum sustaining into 2027. And an early read on BXPM would be great.

**Jonathan Gray** (Executives):
So the drivers, as always, are the performance that's the key thing. The brand, of course, and the reach of our wealth team around the world and our relationships. That is a very powerful combination. Performance, and it was in the numbers you heard exceptional performance really across the board, if you look at what we've done in private equity relative to the marketplace, infrastructure, same story, real estate, our gap versus other competitors is incredibly wide in credit where there was all this talk of some sort of private credit apocalypse earlier this year. Of course, none of that has come to pass. And so we're delivering for the customers, and that's the key thing. And this market, as you know, is very underpenetrated. Investors globally are probably about 1% allocated to private assets. 
And then to the expansion point, we've got a new hedge fund product that we're excited about, had a very good start out of the box. And it's super early days in some of these multi-asset approaches that will take time because it's a new offering. People are used to buying individual products. We're going to have to educate the market about this. But we've done this before. When we started BREIT, when we started BCRED, the early days, took some time. I'd expect here, the reaction from the marketplace has been positive, but it's going to take some time to build those particular products.

**Operator** (Operator):
We'll take our next question from Craig Siegenthaler with Bank of America.

**Craig Siegenthaler** (Analysts):
Our question is on the evolution of Blackstone's Capital Markets business. You're still keeping it capital-light at the holdco while expanding across asset class and geography with investment-grade private credit an increasingly important driver as we just saw on the Broadcom transaction. Could you update us on how the business has evolved and how we should think about the long-term growth of transaction fees?

**Jonathan Gray** (Executives):
Well, I'll just start -- yes, I would just say, generally, what we see, Craig, is as our platform grows, there's just more transaction activity connected to it, more debt and equity offerings as our wealth business grows as our institutional business grows. So it's associated with the overall growth of our AUM and our activity, and we're helping our clients get better execution by using our scale. 
And then the second component of this is in private credit specifically, some of these large bespoke solutions in real assets require -- we're using our very large now $300-plus billion insurance platform some of our institutional clients, particularly on the junior pieces, but in some cases, we distribute a bit as well. And so that's growing as that business grows. So we're continuing with this capital-light approach, that's what we think is the best way for our shareholders. But we're still, at the same time, seeing this pretty rapid growth in transaction and advisory fees.

**Operator** (Operator):
We'll take our next question from Alex Blostein with Goldman Sachs.

**Alexander Blostein** (Analysts):
I was hoping to go back to the AI discussion and maybe just double clicking to the first question for Mike. Obviously, we've seen wider credit spreads and CDS levels move up for Neo clouds and to some extent, some of the more established players. Can you help us just understand to what extent that kind of capital markets move impact your own valuation, whether it's on the equity side in things like data centers or anything you guys are doing on the debt financing. 
And as a follow-up, I guess, to that, as public markets become more constrained, I was hoping you could frame the fundraising opportunity you see across Blackstone to fill some of that gap.

**Jonathan Gray** (Executives):
So from a valuation standpoint, there's a little bit of an impact, obviously, on the present value of stabilized assets, which we tend to carry pretty conservatively. So it impacts the multiples a bit. Interestingly, Alex, on the new assets that you haven't yet leased, I think you'll be able to command a higher yield to absorb this, and you may end up actually in a better spot because it's getting harder to deliver, particularly at scale. So we don't really see a massive impact. When we commit to these large-scale projects, we line up the financing at the same time. We're very disciplined on how we think about financing this. 
For the Neo clouds, I think the key is, will they be able to deliver on their compute promises. We have done a number of things in that area, providing financing on a secured basis against long-term contracts with the biggest hyperscalers. We're creating a Neo cloud but that business is just getting off the ground.  
The key for those businesses is the deliverability. Compute prices are actually up 50% year-on-year. There's a lot of value in legacy H100 chips. Before, people thought they would depreciate much more quickly. So for us, in a lot of ways, a world where capital is more constrained and where we have the scale, the expertise and access to capital, and this gets to the end of your question, that should be beneficial for us. And the ultimate finished product in a world where there's more scarcity of compute should be worth more. And so in terms of fundraising, we're continuing to be able to raise capital. Obviously, investors are asking the same questions around AI. But what we continue to see is demand and usage of the AI going up faster than the compute. 
And again and again, what we're focused on is what we think of the most senior part of the stack, either lending or investing against the energy, which is a very large area for us, the electrical equipment and the data centers, that sort of physical infrastructure that's supporting what's happening that we really like the risk return. And if anything, I think the yields will be going up because it's getting harder to deliver that both physically and because of the need to aggregate financial capital to your point, which is getting tougher.

**Operator** (Operator):
We'll take our next question from Chris Kotowski with Oppenheimer.

**Christoph Kotowski** (Analysts):
Yes. Following up on that last point. I mean people talk about data center finance, like it's all one thing and you have all these different assets with different risk-reward profiles, the land, the envelope of the building, the power source, the chips that go inside. And I guess, how do you see like the next 3 to 5 years playing out? I mean, it seems to me like your role in all this as being kind of the matchmaker between the capital needs and the capital sources. And do you see more of the opportunity on the like investment grade, drawdown funds, opportunistic side? Or is it -- or is it investment grade and to insurance companies or all of the above? If you could just flesh that out a bit more.

**Jonathan Gray** (Executives):
That's funny. That's what I was going to say all of the above because the needs of capital here are so enormous. It's unprecedented in our lifetimes. The amount of capital and so much of it has to come from the private markets because so much of this is development it's not cash flowing. And so having the ability to do chip financings, either on a junior basis, potentially with one of the big model companies or on a senior basis wrapped by one of the big hyperscalers or chip companies themselves. We're doing that at scale. We're obviously providing financing to utilities and pipeline companies, LNG, renewable developers, all of that's part of this. They need enormous amounts of capital, and that again is on both the debt and equity side. And then in the data centers and some of the equipment that goes inside, there's an enormous need for capital. 
So as long as the productivity continues that we see at our companies, their ability to serve their customers much more efficiently to create new products and their demand continues to grow. Then I think there's going to be a continued pull for the need of this compute. And we see ourselves as this holistic solution provider. One of the great benefits of Blackstone is that we can play in all these different areas, from investment-grade for more opportunistic equity. We can do it in the U.S., Europe and Asia. We've got all different platforms. We have expertise. We've obviously got relationships with the big hyperscalers, the model companies, the chip companies, and we're utilizing all that ultimately in our core mission, which is to deliver great returns for our customers.
And despite all the negative things you're reading about AI today, when we look across our business, this continues to be the area where we're driving the highest returns. In the AI infrastructure, a little bit, of course, in the model companies as well. So being able to speak at scale with the key counterparties and be a solution provider from everything from energy through to chips, debt to equity, we think that is a very good place to be. And doing it, I would just add that in a very disciplined way.

**Michael Chae** (Executives):
And I'd just add to that, from a risk-reward standpoint, the consistent common denominator, whether it's our equity or our lending activities in this AI infrastructure area are tenants on our leases and customers on our customer contracts who are the largest, most creditworthy counterparties in the world.

**Christoph Kotowski** (Analysts):
I'm just curious, just as a follow-up, in the coming years, should we expect things like drawdown funds for -- to finance GPUs for various providers? Or do you anticipate that most of the funding is going to come in kind of within the traditional real estate and for private equity kind of fund structures and be commingled with other kinds of investments?

**Jonathan Gray** (Executives):
It's possible here, we'll have a bit of both. I would say in the credit area, we're doing things on a senior basis on investment-grade counterparties, that's being done with a range of insurance companies and pension funds. Those are obviously highly rated underlying securities. And then we're taking a little more risk on the junior side of some of these transactions. In some cases, there are separate SMAs, and you could see us have something focused, for instance, in chip financing specifically. But again, the breadth of what we have in credit, $500-plus billion, that enables us to do a lot. And so I think you could see some dedicated products. But at the same time, customers also want some diversification. And we spent a lot of time, obviously, talking about AI in this infrastructure. 
If you look across our $1.4 trillion of assets today between debt and equity, it's about 7% of our total, which is still a very large number, given our scale. But our clients also want other things. They want exposure to defense. They want exposure to life sciences. They want exposure to India and Japan. They want exposure to sports. There's warehouses, hotels and travel. So we've got to be mindful of delivering everything. There will be, in some cases, make sense to have dedicated vehicles, but in many cases, it will be in broader commingled vehicles.

**Operator** (Operator):
We'll take our next question from Glenn Schorr with Evercore.

**Glenn Schorr** (Analysts):
You definitely partially just answered this, but let me ask it anyway because I think there's a little more color to have. So recognizing this amazing AI CapEx super cycle might be once in a lifetime and huge demand for compute and the capital. I am curious on as you pursue going all in on this and I get it, how you balance the potential of technological obsolescence and then concentration limits for both the fund level and the firm. And I'm just curious how that comes up in your LP conversations. Because when you say 7% of $1.4 trillion, I'm like, no big deal anyway.

**Jonathan Gray** (Executives):
Yes. We spent a lot of time, Glenn, thinking about that. I do think to emphasize the importance of our focus on the physical infrastructure and the focus on long-term contracted assets. So the vast majority of that 7% is in data centers that have 15- to 20-year lease terms at initiation with 96% investment-grade counterparties with an average market cap of $2.5 trillion. So when we think about risk, that doesn't feel particularly risky to us. There are things we do with model companies. Some of what we're doing in our BXN1 area with application software companies and what we've done in our private equity vehicle for individual investors has involved some exposure to the underlying technology. Now to date, that has worked out incredibly well, but we recognize there are risks. But we're playing across this entire space. 
And at the same time, we have a huge push into energy, which is benefiting from the data centers. It will benefit from robotics, autonomous vehicles, but also just from this large reindustrialization we're seeing and really the electrification of everything. And again, lots of what we do there is long-term contracted -- building power plants off our utilities, the financings that we're doing for energy companies, for LNG companies. So I would say this is a place that focus a ton on risk, on downside. Steve's always stressed the importance of not losing capital. We are very wide eyed about what we're doing here. And the way we're deploying capital, the contracted nature of most of what we're doing and the scale and creditworthiness of the counterparties, all of that gives us a lot of comfort.

**Operator** (Operator):
We will take our next question from Bill Katz with TD Cowen.

**William Katz** (Analysts):
Love hearing the substantial increase in realizations into the fourth quarter and the affirmation of the double-digit base management fee growth for next year. Maybe unpack or click into that maybe one more level. Where do you see the opportunity in the realizations? And then, Michael, as you think about the double-digit growth, is there any way to sort of frame that range out a little bit and/or which segments you really see the greatest opportunity when you look across the businesses?

**Michael Chae** (Executives):
Sure. Thank you, Bill. On the realization part, just to flesh that out a bit more, as we mentioned, let's take the fourth quarter first. We do have -- we're in the middle of the quarter now. We have high visibility into a significant step-up in net realizations in the quarter. That's driven by closings on a number of previously announced sales, primarily in private equity. And I would say that what we have under contract that is expected to close in terms of carry realizations alone in the fourth quarter is expected to surpass the total net realization levels for the firm from the third quarter. So that's a positive. 
And then as you know, we have the scheduled year-end crystallizations in BXMA in the context of very strong year-to-date performance as well as a number of year-end crystallizations in our credit drawdown funds. So that's a very constructive outlook for the fourth quarter, and we see that as well for 2027. But I would just step back and say broadly, whether it's the fourth quarter or next year, in an exit environment that's not been easy, obviously, for the broader industry, we feel like we really do benefit from how we position the portfolio around areas the market wants. So whether it's energy, as we've talked about, power and electrification, our energy private equity NAPR balance more than doubling year-over-year, as we mentioned, Life sciences, Japan, India and Europe actually, we'll see a pretty robust slate of exits this year recently in the leisure and gaming area. And then from a public market standpoint, in an IPO market that's been open but highly selective, we've completed, as you know, 9 IPOs since the summer of 2025, 5 this year. 
The pipeline remains strong. And that's allowed us to liquefy a good portion of our carry receivables, especially in private equity and to be able to be opportunistic going forward if we find windows in the market with particular securities to monetize our position. So that's a bit of the backdrop. There's obviously an inherent lumpiness with realizations quarter-to-quarter as you're seeing and you'll be seeing throughout this year. But overall, the underlying realization potential, we think, remains substantial. And just stepping back further versus other firms, the evolution of our firm towards more perpetual capital means about half of or nearly half of our invested performance revenue eligible AUMs in perpetual vehicles, which, as you know, generate incentive fees without requiring asset sales. So that, we think, is a fundamental advantage for our model. 
On base management fees, I would just step back and say that in terms of the path ahead, there are a handful of key drivers, and I hit those in my remarks. There's a full year benefit next year of private equity drawdowns. The third Asia fund was activated in September. The fifth energy -- private equity energy fund hit its hard cap just after the end of the third quarter. We're finishing the SP X fundraise. So we expect the contribution of management fees from these new funds to build through the first half of next year as the holidays conclude and remaining fundraises progress in areas like SP. That's #1. 
Second, this powerful expansion of perpetual strategies. Our Infra AUM is up 40% year-over-year. Our BXPE NAV is up nearly double year-over-year, BXINFRA NAV 2.5x year-over-year. and strong momentum in BXMA, fee AUM there up 24% year-over-year, record organic net flows in Q3. Strong growth in credit insurance across the institutional insurance channels alongside an inevitable and eventual stabilization of retail flows in the BDC area. And then the fifth piece is ultimately a stabilization of real estate. So I think when you take those pieces together, those are the building blocks, and that's why we feel like we're well positioned in terms of the path ahead.

**Operator** (Operator):
We'll take our next question from Dan Fannon with Jefferies.

**Daniel Fannon** (Analysts):
I wanted to follow up on your comments around the real estate environment, obviously, higher rates. So curious just a little bit more detail around the fundamentals and what you're seeing in that asset class.

**Jonathan Gray** (Executives):
So there really are, Dan, some crosscurrents underway here. Obviously, rates went up, and that has an impact, particularly on slower-growing assets, multifamily in the U.S., some of the assets in Europe. But at the same time, we're seeing accelerating fundamentals. So the sharp drop-off in supply that started, call it, 3 years ago is now beginning to show up. And when that limited new supply of real estate meets a very healthy economy, so strong demand, you're seeing cash flows growing nicely. In logistics, we had a 45% increase in leasing in our U.S. platform, which is quite large. It's our largest holding in our real estate business. 
Hotels nationally, same-store sales are up 6% this year. The industry was flat last year. Obviously, data center leasing very strong across our various platforms. We're going to do 6 gigawatts this year, we think, which is triple what we did last year. And those 3 categories, when you look at Blackstone real estate, that's over 60% of our exposures are in those 3 asset classes. So that is very helpful there. At the same time, the debt market, which 3 years ago was facing a lot of challenges in real estate has been healthier. There are legacy deals that may be challenged, of course. And as I said, slower growth assets will be more hit by the rise in rates. But overall, the underlying fundamentals mean there is going to be a recovery here over time. That's really the key thing. And so that's what -- I think that's the reason why the REIT market, despite the rising rates is still up double digit in the public REIT market. So as I said, crosscurrents, but accelerating fundamentals.

**Operator** (Operator):
We'll take our next question from Devin Ryan with Citizens Bank.

**Devin Ryan** (Analysts):
A question on the Vanguard and Wellington products now that they've launched. I appreciate it's small today. But curious how to think about these partnerships and how to think about kind of the expansion for Blackstone into kind of new markets and new customers and kind of making sure that it's incremental versus kind of cannibalistic. But one thing kind of thinking about is whether this could meaningfully kind of increase exposure into retirement and other advised assets that have historically been pretty difficult for private markets to reach. So I'm just curious kind of the bigger picture of kind of where partnerships like this could be going.

**Jonathan Gray** (Executives):
Well, I think it's very incremental because in many cases, we're trying to get to customers we haven't accessed. Some of it is structural. So a number of our products to give them maximum flexibility in investing, are QP, qualified purchaser limited and therefore, accredited investors cannot access them. When you put these in a vehicle with a third party, in this case, Wellington sitting on top, you have a broader universe of investors you can sell to. That's obviously helpful. There are some advisers and we think underlying customers who want to be able to push an easy button to not have to subscribe to 4 different funds or different funds plus different liquid products. So we're trying to access that market. And then you point out in retirement, being able to give holistic integrated solutions with best-in-class products, we think that is very helpful. 
Now we're still -- the administrative process is still going through in D.C. We do think when we get some clarity on that, that will help the retirement space. Again, that's going to be a bit of a journey. But being able to make it easier to access alternatives is a path we've really been on for a quarter century with individual investors. And 10 years ago, it took a step function up when we created these perpetual products. We've been moving obviously, globally now, and we have a lot of strength in places like Canada, Australia, Japan, Hong Kong, Singapore, Middle East, even Europe. Now this is another sort of leg on that journey. We're expanding the products. We're making them easier to access this sort of one-stop shopping. So I think this is just another step on that journey. It's still early days, but we do think there's a lot of expansion potential here.

**Operator** (Operator):
We'll take our question from Dan Welden with Wells Fargo.

**Daniel F. Welden** (Analysts):
The insurance segment was running mid-teens, and you mentioned today more than 20 clients have expanded their relationships in the past 12 months. Could you talk about the competitive backdrop and the ability to sustain this growth? And then also maybe touch on the fee rate of the incremental mandate in insurance versus the existing portfolio.

**Jonathan Gray** (Executives):
So I'll let you handle the fee part, Michael. On the competitive dynamic in the market overall, we really like our position in the insurance market because we are independent and we're not insurance companies ourselves selling products against others, and our focus is on being a third-party investment manager, it gives us a pretty big universe to serve. And what we're seeing with our clients is they're starting in one area with a separately managed account and then broadening. We're continuing to get more and more exposure. And it really started with sort of the Big 4 strategic accounts. What's growing the fastest today are the rest of the clients who are getting more and more exposure. 
And what they're finding is that as capital intensity is going up in the economy, the ability to access these investments from someone like us, an independent third-party manager who has expertise in underwriting data centers or energy infrastructure or all sorts of companies and hard assets and the fact that we can aggregate that at scale and deliver them call it, 150 basis point premium for comparably rated public credit, they're finding that highly attractive. 
And I would say the openness to what we're doing with insurance clients, not just in the U.S., but in Europe and Asia increasingly, that is really growing. So we think that scale in this market is important. It's hard to enter because you've got to be -- have the ability to write multibillion-dollar checks. We have that ability with our model, and we're doing it, as you know, on an asset-light basis. And so I just think this is -- it's something that the insurance market from a competitive standpoint is now recognizing that they need to have this capability. When they're looking for third-party managers, there are -- there's not a big universe of people doing this at scale. And the other alternative managers who have different models to own insurance companies, they're obviously very capable. They are competitors in this field. But it's a pretty limited universe of who can write checks and underwrite these transactions. And so we would expect we'll continue to see growth in this insurance space and continue to see a lot of growth around asset-based financing. 
And by the way, one other thing I'd add is the fact that we have such a robust institutional business for the junior piece of these transactions is a very helpful component when we're out there competing.

**Michael Chae** (Executives):
On the fee rate part, there's a range, of course, and it's client-specific and it's strategy specific, and we have IMAs and SMAs, as you know. as well as sort of what the scale of the relationship is. Overall, I would say it averages in the range of 40 to 50 basis points. But again, there's variability there. The margins are attractive, and it is very scalable. We talked about crossing the $300 billion AUM mark. And more importantly, our ability to originate and deliver excess spread to our clients scales as well.

**Operator** (Operator):
We'll take our next question from Brian Bedell with Deutsche Bank.

**Brian Bedell** (Analysts):
Maybe, Michael, just to go back to following up on Bill's question on the base management fee growth, in particular, the double-digit range. Just, I guess, in terms of -- you laid out all the different conditions that are going to contribute to that, which is great. One -- a couple I wanted to touch on were the dry powder in credit, which is now -- has expanded pretty substantially, the potential for deployment to contribute to that fee growth. And then what would hold it back from getting into, say, the mid-teens, I guess, on a year-over-year basis? 
And then just to the extent that you are able to generate solid double-digit base management fee growth, how do you view scaling the FRE margin earlier in this decade, obviously, that we had sort of very robust margin expansion along with really strong base management fee growth. So would you expect to see a better scaling in the next 1 to 2 years versus the prior 2 to 3 years?

**Michael Chae** (Executives):
Brian, a few parts to that. From -- in terms of credit and deployment, you mentioned the dry powder balance, it is substantial. It's $87 billion just for the BXCI portion. If you include BREIT, it's $96 billion. And I think you're seeing particularly in the infrastructure and asset-based credit area, which overlaps heavily with private investment grade, that deployment, and we talked about the qualitative drivers behind that really is -- it's a robust environment. We do see acceleration there. The AUM in our IABC area was up 31% year-over-year and that will come more and more into fee-earning AUM as invested. The opportunity set is broad, and obviously, we continue to fundraise there. 
So I think that's how to think about the dynamics in credit. I think in terms of what could sort of constrain it one way or the other, I think it's fair to say the -- a bunch of that is embedded. Obviously, those drawdown funds that are going to have full year fees next year. Those are more in the private equity side, in particular, those are more or less built in. The big portion, that perpetual fund fee growth, that tremendous sort of, again, built-in NAV growth, broader base entering 2027, one variable at the margin one way or the other is obviously somewhat market dependent around performance and flows in the course of the year. 
And then finally, a factor is clearly the sort of stabilization and inflection point around the real estate segment as it relates to base management fees and also the BDC portion of credit. So the timing of that, we know -- we believe we know what the end game is, which is stabilization and inflection, but the timing of that is a variable as well. And then I just think on scalability and margins, we see it as scalable with the operating leverage built into that, that we've seen across our firm over the long-term.

**Operator** (Operator):
We'll take our next question from Brennan Hawken with BMO Capital Markets.

**Brennan Hawken** (Analysts):
I actually, Michael, have another follow-up on that. So you just activated your secondary flagship. You spoke to robust fundraising that you expect through next year. So that's going to contribute some catch-up fees. Is the low double-digit expectation on a core basis? Or would that include the catch-up fees? 
And then also earlier in the year, you guys spoke to 4Q potentially benefiting from some of these great things that you had highlighted in driving that. Will 4Q -- how will 4Q bridge us as we get into 2027? Last quarter, you had given a lot of clarity on this quarter. So should we see a step up? And what kind of order of magnitude would that be?

**Michael Chae** (Executives):
Sure. On the second part in terms of Q4, I think we expect to see, I would call it, modest sequential growth quarter-over-quarter before this acceleration into 2027. And I think I mentioned earlier, especially as these drawdown funds start to season in, you'll see in the middle of the year, I think that step up even further. And then in terms of your other question, the first question.

**Weston Tucker** (Executives):
Yes. It was really around the step-up, the shape management.

**Michael Chae** (Executives):
I'm sorry, yes. Yes, that's a simple answer, which is when we talk about low double digits, we're talking about the full year of base management fees over the full year in 2026.

**Brennan Hawken** (Analysts):
Okay. So inclusive of all of the above. Got it.

**Michael Chae** (Executives):
Yes.

**Operator** (Operator):
We will take our next question from Mike Brown with UBS.

**Michael Brown** (Analysts):
Can you just talk a little bit more about the retail channel right now? Just what are you kind of seeing in terms of demand across the platform? And as we think about this higher rate backdrop, what are you observing in terms of asset allocation shifts in terms of new dollars being put to work? And then on some of these newer perpetual products, any view into how these could scale relative to some of your other successful products like BXPE and BXINFRA?

**Jonathan Gray** (Executives):
What we've seen overall has been more resilience than I think market participants expected. We had all this noise around private credit and the flows into that area obviously slowed in response and yet we raised $9 billion in wealth in the third quarter. There was also a lot of volatility on the screen. And our AUM in the space is up 15% year-on-year. So to me, that says there's a lot of desire for the type of products we're offering with the structure and the performance we're delivering. If markets go down a lot, that can impact things, if headlines are tough. But what we've been watching here is steady growth. And we expect this growth to continue. We think it will be more and more global. It will be through the wirehouses and the RIAs, and it will be new products. 
I think the hedge fund product is particularly exciting. Again, it speaks to the scale and breadth of Blackstone that we're the leader in that space globally, for institutions. Now we can offer something very targeted for individual investors. And again, what we have to do is deliver strong performance and in that case, limited volatility. And if we do that, that can scale and grow to be a large product. And I think there's more we can do over time. This platform we have is remarkable and the strength of the Blackstone brand is remarkable. And it's what enabled us to run a business on a capital-light basis since we started. Since Steve created this firm, we use very limited capital for what we do, and we rely on our expertise, our people our track record and delivering strong performance. And in the wealth channel, I think we've done that exceptionally well across asset classes, and that bodes well both for the existing products and for new products we'll create.

**Michael Chae** (Executives):
I might just also add to put a fine point on that. BXINFRA, it's -- I would say it's "only $7 billion." Our distribution strategy around that has been intentional and selective globally. And so the performance has been terrific. The asset class is obviously so large on a global basis. So I think we see a lot of runway on that to scale. Jon mentioned the hedge fund area, where I would just add, the hedge fund area, I think, broadly has come back into favor with a lot of investors. I think that's been driven particularly by multi-strategy strategies that have shown you can deliver double-digit absolute returns with less correlation, more market neutrality. And a lot of what we're doing are our version of that, leveraging our platform and I think very compelling fees and liquidity provision. 
So -- and that's an area that's been hard to access in terms of that performance. So we're very bullish about that. As Jon said, there's other white space. There are things in the lab around new flagship strategies. And then this multi-asset space is -- that is a long-term game, but ultimately very scalable.

**Operator** (Operator):
We'll take our next question from Benjamin Budish with Barclays Capital.

**Benjamin Budish** (Analysts):
I wanted to follow up on -- I think this was Glenn's question from earlier. I think he had asked about Blackstone's concentration in AI. I'm curious if you could talk about how your insurance LPs are thinking about concentration in AI-related debt. It seems like the press and some of the kind of industry data out there would suggest it's small but growing very rapidly. So as AI CapEx infrastructure financing is picking up, how much like incremental appetite is there from your insurance clients? And to the extent that they may start to get tapped out, is this where the sort of third-party kind of traditional institutional IG credit narrative comes into play? Or how else do you think about placing all of that -- all of those assets?

**Jonathan Gray** (Executives):
Well, it's an important question. For our insurance clients, their exposure, as you would imagine, are to the biggest hyperscalers. What we're seeing them do in a number of cases is potentially sell liquid corporate bonds in exchange for some of the asset-backed. So you have exposure to Microsoft or Meta or so forth, and they're thinking about their exposure to an individual name. And when they look at what we're doing in asset-based financing and the additional spread they can earn for the same underlying credit as well as the support of the physical asset, they think about that as an attractive trade. So we're seeing some of that. But yes, they're mindful of their exposure. 
One thing that I think will evolve over time is an understanding that the compute itself has value. When you look at the airline business, lending against aircraft is an investment-grade business, not because Spirit Airlines or an emerging market airline has great credit themselves, but it's because of the shortage of commercial aviation in the world. Today, when it comes to compute, be it data centers or chips, people are not putting much value on the underlying assets. They're solely looking at the credit of the counterparties. I think that will evolve over time, which will expand some of the capacity these insurance companies have. But I do think it's fair to say today, right now, there is focus on that. I do think that means a broadening of markets. I do think for us, it means pension funds and wealth funds starting to look at the excess spread in the private investment-grade market. 
I think over time, obviously, there'll be more ownership by mutual funds and others as well. So I think this does need to broaden. But I do think the most positive thing here is the underlying asset class has a lot of value, and we haven't yet tapped into that. There's really just focus on the underlying name without any credit for the actual assets themselves.

**Operator** (Operator):
We will take our next question from Ken Worthington with JPMorgan.

**Kenneth Worthington** (Analysts):
Multi-asset, strong inflows in 3Q, I think, by far, a record. Can you give us more color on the sales success you had for the quarter? And then what does the organic growth look like as we think about 2027? And can you expand the fee rate from here?

**Jonathan Gray** (Executives):
Yes. This is really exciting for us. Our absolute return or hedge fund business, BXMA, had been pretty flat for a long time. And under Joe Dowling, new leadership there, not so new anymore, 6-plus years, he's done an extraordinary job turning around performance. The fact that we've beaten 60-40 over that period of time by nearly 200 basis points annually and doing it without any down quarters in the flagship strategy is extraordinary. And clients are responding to that. And we're seeing that growth, to your question, in sort of the general absolute return business that we have there. We're seeing strong performance in the multi-strat business. We've begun to build a very high-end wealth business there for a select group of clients that's also performing incredibly well. 
And then we have a liquid business, Harvest, focused on MLPs and energy infrastructure that's doing exceptionally well. And now we have a new engine here with BXHF. And so when we look at this aggregately, this feels like a business that should continue to grow. I don't know what the right number is. Is it 20-plus percent a year? It's obviously a function of what happens inside of the business in terms of returns, but strong returns with less in the way of net outflows, more in inflows. All of that makes us feel like this is a business that is on a path again to really start to scale.

**Michael Chae** (Executives):
And I'd just add, Ken, you asked about sort of fee rate and pricing. As Jon mentioned, different component businesses and what you see in aggregate is a blend -- but it's a very positive picture at the individual division level. In our absolute return area, you have seen versus historical trends, the stabilization of average fee rate. That's both because the commingled portion of that has, I think, resurged in popularity at a higher blended fee relative to customized. In the multi-strat area, we're seeing flows growth there and performance growth, and that is, given the nature of the strategy at a higher fee rate. And then you have things like our total portfolio management wealth area, which on average comes obviously at a lower fee rate but very good growth. So the output of that, I think, is a positive and a positive versus sort of what the dynamics were around fees and pricing a number of years ago.

**Operator** (Operator):
We will take our next question from Arnaud Giblat with BNP Paribas.

**Arnaud Giblat** (Analysts):
A quick housekeeping question for me. You've got a number of funds coming up to their 10-, 11-, 12-year anniversaries, which is usually the end of their investment period. Should we expect some step-downs in the coming quarters?

**Michael Chae** (Executives):
Yes. Arnaud, that it's obviously sort of -- that's been built into our results for many years. You saw actually in this quarter in the BREP area last quarter, in the middle of the quarter, BREP VIII reached the end of its fund life. So there's a termination that actually -- we had a full quarter of that this quarter, which actually was the biggest factor in sort of the management fee quarter-over-quarter dynamics. And then there's other dynamics around that across the suite of older legacy funds in our business. But that would be the most notable one. But it's just -- it's -- I would say it's -- that will occur as it has been for years in our business. But when there are meaningful developments like the one I just mentioned, we'll expect to call it out for you.

**Operator** (Operator):
We'll take our next question from Patrick Davitt with Autonomous Research.

**Patrick Davitt** (Analysts):
Question is on direct lending dynamics. You mentioned institutions leaning into what looks like a better deployment opportunity, but broader deployment data, we can see remains pretty constrained. So could you give a bit more specifics on how direct lending pipelines are looking? And to what extent the improved spread in terms many players have been talking about has continued and/or improved through today?

**Jonathan Gray** (Executives):
So Patrick, what I'd say is as transaction activity slowed in the third quarter with the volatility, obviously, that had a direct impact on direct lending activity. So I don't think that is a surprise. On the pricing, what's been beneficial has been the rise in base rates in both the U.S. and Europe. We haven't seen a lot of spread widening. Spreads have hung in there pretty well. And it's tied to the fact that underlying portfolios are really strong. I mean we saw in our BCRED portfolio, double-digit EBITDA growth for our borrowers. Debt service coverage ratios are 2.3x. We're just seeing -- there is a tail of some of the legacy older deals, but that's a small minority. Overall, we're seeing pretty good credit health out there. And on new deals, it is competitive. I'd say it's balanced in terms of capital. So benefit from higher base rates, but spreads, I'd say, pretty constant.

**Patrick Davitt** (Analysts):
Are you seeing any improvement in pipelines?

**Jonathan Gray** (Executives):
I wouldn't say as of now. I mean, I think, again, all the volatility has slowed the deal business, but there is a desire, I think, for a lot of transaction activity. And as we've talked about, companies are performing really well. I mean, if you look across the Blackstone portfolio, double-digit revenue growth. So I think as soon as we get a little bit of terra firma in the overall sort of geopolitical world, I think you will see a step function increase in transaction activity.

**Operator** (Operator):
We'll take our next -- I'm sorry, we'll take our final question from Crispin Love with Piper Sandler.

**Crispin Love** (Analysts):
Can you dig into the real estate management fee trajectory? [ AUM ] was flat there, but management fees were down. And I appreciate that the transaction and other fees was a driver of total fees. But what's the outlook for the base management fees in that segment? What needs to happen for those to stabilize and turn positive? Just curious on some of the puts and takes there.

**Michael Chae** (Executives):
Yes. Actually, Crispin, just for the -- in terms of the third quarter and sequentially on the dynamics there. I think with Arnaud's question that the biggest factor there was this fund termination of BREP VIII late in the second quarter, which we had a full quarter effect of this quarter. We mentioned before with, I think, to a lesser extent this quarter, BPP, where there have been headwinds there around lower NAV and certain fee incentives to encourage duration of capital. So those are some of the dynamics there. 
I think in terms of the outlook, -- we'd expect real estate base management fees to remain broadly stable through year-end and into 2027. And then -- and sort of the structural dynamics, as you know, we're currently in a period between major drawdown fundraises, which has its effect on that sequential growth and then the Core+ institutional headwinds I mentioned. But offsetting that, the BREIT being back in growth mode with improving flows and obviously strong performance. So I go back to in terms of the outlook, we see from here sequential stability in the coming quarters.

**Operator** (Operator):
That will conclude our question-and-answer session. At this time, I'd like to turn the call back over to Weston Tucker for any additional or closing remarks.

**Weston Tucker** (Executives):
Great. Thank you, everyone, for joining us today, and we look forward to speaking after the call. Take care.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BX_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Michael Chae｜guidance：CFO 預期第三季基礎管理費年增率與第二季相近，2027 年回到雙位數成長（原話："in the third quarter as in Q2 with a return to double-digit"）
- 2026-07-23｜Michael Chae｜guidance：CFO 預期第三季淨實現收益環比放緩，第四季與 2027 年強勁（原話："deceleration in net realizations in the third quarter"）
- 2026-07-23｜Michael Chae｜guidance：CFO 列出 2027 年雙位數基礎管理費成長的建構項之一：房地產基礎費趨勢明年穩定（原話："we see stabilization in the real estate base fee trends next year"）
- 2026-07-23｜Michael Chae｜guidance：CFO 稱信用業務未動用資金（dry powder）達 840 億美元，為管理費成長的蓄勢來源（原話："$84 billion of dry powder"）
- 2026-07-23｜Michael Chae｜guidance：CFO 表示交易費用下半年有相當的待辦案源，但季度間會有波動（原話："considerable pipeline in place for the second half"）
- 2026-07-23｜Jonathan Gray｜guidance：Gray 表示公司對年底與 2027 年實現收益回升有信心（原話："I think we know where this is heading"）
- 2026-07-23｜Michael Chae｜margin：被問 2027 利潤率時，CFO 不給具體看法，只說結構上喜歡目前的利潤率位置（原話："we're not going to give a specific viewpoint on that"）
- 2026-07-23｜Michael Chae｜margin：CFO 說明交易與顧問費近乎翻倍至紀錄的 3.21 億美元，並稱其為被低估的費收引擎（原話："doubled in the second quarter to a record $321 million"）
- 2026-07-23｜Michael Chae｜margin：CFO 拆解費相關績效收入年增 68% 至 7.93 億美元，來自常青型策略規模化（原話："increased 68% year-over-year to $793"）
- 2026-07-23｜Michael Chae｜margin：CFO 披露帳上淨應計績效收入（stored value）為 75 億美元、每股 6 美元，為四年高點（原話："now stands at $7.5 billion or $6 per share"）
- 2026-07-23｜Michael Chae｜capital_allocation：CFO 重申資本政策：長期將現金盈餘 100% 返還股東（原話："returning 100% over time of our cash earnings"）
- 2026-07-23｜Michael Chae｜capital_allocation：被問是否調整股利與回購比重，CFO 稱有空間但強調維持既定政策（原話："We certainly have scope to look at that over time"）
- 2026-07-23｜Stephen Schwarzman｜capital_allocation：Schwarzman 稱公司股價偏低、是參與此大趨勢最便宜的方式之一（原話："our stock is on sale today"）
- 2026-07-23｜Jonathan Gray｜capital_allocation：Gray 稱品牌使公司成長無需借款或大規模動用自身資本（原話："without having to borrow money or utilize capital at scale"）
- 2026-07-23｜Stephen Schwarzman｜product：與 Google 合作成立以 TPU 為基礎的新 AI 雲端業者，初期最多投入 50 億美元（原話："investing up to $5 billion initially"）
- 2026-07-23｜Stephen Schwarzman｜product：與 Broadcom 設立融資平台，初期 350 億美元，被形容為史上最大私募信用投資（原話："the largest private credit investment in history"）
- 2026-07-23｜Stephen Schwarzman｜product：新推公開 REIT BXDC，募資 20 億美元，被稱為史上最大盲池 REIT IPO（原話："the largest blind pool REIT IPO in history"）
- 2026-07-23｜Stephen Schwarzman｜product：管理層認為穩定運營資料中心的長期持有市場目前仍初期，但可能成長到一兆美元（原話："we think it could grow to $1 trillion over time and beyond"）
- 2026-07-23｜Stephen Schwarzman｜product：資料中心平台總價值達 1,850 億美元（含在建），年初為 1,300 億（原話："grown to $185 billion of total value"）
- 2026-07-23｜Stephen Schwarzman｜product：預期今年出租的容量超過任何一年的三倍（原話："We expect to lease over 3x more capacity this year"）
- 2026-07-23｜Stephen Schwarzman｜product：若管線順利執行，資料中心平台未來數年可能翻倍（原話："our data center platform could double over the next"）
- 2026-07-23｜Jonathan Gray｜product：Nippon Life 新夥伴關係，未來數年部署約 100 億美元私募信用（原話："we will deploy approximately $10 billion in private credit"）
- 2026-07-23｜Jonathan Gray｜product：亞洲 PE 旗艦基金最終募得 131 億美元，規模為前一期的兩倍以上（原話："more than double the previous vintage"）
- 2026-07-23｜Jonathan Gray｜product：三檔機構型基金今年已達募資上限，第四檔能源轉型旗艦預計很快跟進（原話："Three of these funds hit their hard cap so far in"）
- 2026-07-23｜Jonathan Gray｜product：公司目前有 8 件 IPO 在審，今年以來已執行 3 件（原話："we have 8 IPOs on file"）
- 2026-07-23｜Stephen Schwarzman｜risk：Schwarzman 承認 AI 領域可能有過度亢奮的風險，稱公司是挑選過的布局（原話："we're mindful of the potential for excessive exuberance"）
- 2026-07-23｜Jonathan Gray｜risk：BCRED 第二季買回請求超過 5% 上限，約 50% 獲滿足（原話："repurchase requests remain elevated"）
- 2026-07-23｜Jonathan Gray｜risk：BCRED 第二季淨流出 12 億美元（原話："resulting in net outflows of $1.2 billion"）
- 2026-07-23｜Jonathan Gray｜risk：Gray 稱第三季初 BCRED 贖回請求顯著下降（原話："redemption requests are down materially"）
- 2026-07-23｜Jonathan Gray｜risk：Gray 把贖回壓力下降歸因於媒體雜訊降低與投資人溝通（原話："a lot of people were calling for this massive calamity"）
- 2026-07-23｜Jonathan Gray｜risk：Gray 指出房地產短期受利率上升拖累（原話："near-term headwinds slowing things down"）
- 2026-07-23｜Jonathan Gray｜risk：Gray 指白領服務、資訊服務、軟體類資產因不確定性高，買方趨於保守、流動性較差（原話："high quotient of uncertainty"）
- 2026-07-23｜Jonathan Gray｜risk：Gray 澄清軟體在全公司曝險約佔 6%（原話："Software for us as a firm is around 6% of our exposures"）
- 2026-07-23｜Jonathan Gray｜risk：私人財富通路第二季銷售在伊朗衝突情緒最差的 4、5 月放緩（原話："sentiment related to the Iran conflict was most negative"）
- 2026-07-23｜Jonathan Gray｜competition：Gray 稱全球運算力短缺，需求超過投入資金（原話："We definitely see today a global shortage of compute."）
- 2026-07-23｜Jonathan Gray｜competition：Gray 稱公司握有已取得許可與電力的資料中心用地，作為稀缺資源（原話："15 gigawatts of sites globally"）
- 2026-07-23｜Jonathan Gray｜competition：Gray 指在保險私募投資級信用領域，目前主要是自家與少數私募同業在競爭（原話："it's really us and some of our"）
- 2026-07-23｜Jonathan Gray｜customer：保險 AUM 達 2,900 億美元、年增 15%（原話："Our insurance AUM reached $290 billion in the second quarter"）
- 2026-07-23｜Jonathan Gray｜customer：私人財富 AUM 年增 16% 至創紀錄 3,240 億美元（原話："record $324"）
- 2026-07-23｜Jonathan Gray｜customer：保險夥伴通常以約 5 億美元起步，部分已成長到數十億（原話："We typically start with, call it, $500 million."）
- 2026-07-23｜Stephen Schwarzman｜commitment：Schwarzman 稱 AI 相關投資是業績的最主要驅動（原話："large-scale investments we made"）
- 2026-07-23｜Jonathan Gray｜commitment：Gray 稱房地產物流租賃強勁，Link Logistics 上半年租賃量年增 26%（原話："up 26% in leasing volume"）

### 問答異常語氣（迴避／改口／保留）
- BX_Q2_2026_Earnings_Call_20260723.md｜問：Fannon：基於管理費展望，2027 年利潤率如何看待｜答法：CFO 稱對營收有信心與能管理費用，但明講不給 2027 利潤率的具體看法，只說結構上喜歡現況
- BX_Q2_2026_Earnings_Call_20260723.md｜問：Katz：股價大跌，是否調整配息率或加大回購｜答法：CFO 回到既定政策，稱有空間但未表態任何調整，語氣保留
- BX_Q2_2026_Earnings_Call_20260723.md｜問：Davitt：電視訪談『非 AI 公司交易將持續低迷』的說法｜答法：Gray 表示標題需更正，改說僅白領服務、資訊服務與軟體類（約佔 PE 市場 30–40%）活動較少
- BX_Q2_2026_Earnings_Call_20260723.md｜問：Chubak：保險業務成長是否持續或加速｜答法：Gray 描述結構性趨勢但稱難以給出具體成長率
- BX_Q2_2026_Earnings_Call_20260723.md｜問：Bedell：募資動能能否延續到 2027 年之後｜答法：Gray 稱難以具體預判，改談各通路現況與品牌，並將前景繫於戰爭結束與降息

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
{"date":"20260724","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"費用相關獲利（FRE）以中個位數到低雙位數持久複利——即使 realization 永遠不回來，AUM 淨流入 + 永續資本 + 費用相關績效收入使 FRE 自身複利"},{"id":"H2","text":"被壓抑四年的獲利兌現／績效收入週期在 2026-2027 復甦——IPO 市場重開、利率下行、退出通道解凍"},{"id":"H3","text":"估值從產業 de-rating 的便宜區修復——市場重新給 BX 規模×永續資本×通道廣度的溢價"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Realization 週期再度延後——利率高檔 + IPO 窗口因地緣再關，FY2027 DE 共識 miss"},{"id":"R2","text":"私人信貸循環轉向 + BCRED 贖回螺旋 + Level-3 mark 可信度——半流動性零售產品被迫賤賣、績效費崩、私人財富淨流入轉負；且底層私人信貸的 mark-to-model 可信度是活的問題（BCRED 整體 mark 96.1，但底部 5% mark 至 68.3；2026 有 BDC 錯報 NAV 訴訟、DOJ SDNY 關注私募估值）"},{"id":"R3","text":"私人信貸系統性監管收緊 + 利率高檔使退出通道萎縮——Fed 要求銀行揭露私人信貸曝險（2026-04）、Treasury 設保險曝險評估團隊、FSB 發脆弱性警告（2026-05）、OFR 對手方曝險簡報（2026-03）；若導致銀行資本處理或保險資本費率改變，直接威脅 BX 保險連結永續資本引擎；疊加利率高檔使 realization 結構性下移"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼＝回檔至 $105-112（貼 52 週低區）或 Credit 分部 DE YoY 轉正＋BCRED 贖回續降（確認 Q3 改善）＋Q4 realization 放量；減碼＝BCRED 贖回持續超 5% 上限惡化、或 Credit 分部 DE 連 2 季 YoY 下滑＋mark 減記擴大","irr_base_pct":12.5,"ev5y_pct":76.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.1,"ev5y_pct":76.0,"irr_base_pct":12.5,"max_dd_pct":-55.0,"bull_5y_price":297.0,"bear_5y_price":74.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"加碼＝回檔至 $105-112（貼 52 週低區）或 Credit 分部 DE YoY 轉正＋BCRED 贖回續降（確認 Q3 改善）＋Q4 realization 放量；減碼＝BCRED 贖回持續超 5% 上限惡化、或 Credit 分部 DE 連 2 季 YoY 下滑＋mark 減記擴大","price_at_dd":124.5,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BX_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
