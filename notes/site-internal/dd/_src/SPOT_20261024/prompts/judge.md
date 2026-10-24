你是 stock-analyst **v20 判斷 agent**，標的 SPOT（20261024）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SPOT","date":"2026-10-24","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPOT_20261024/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPOT_20261024/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_total_revenue_ifrs","label":"Total revenue (IFRS)","value":4969,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi1_operating_income_ifrs_no","label":"Operating income (IFRS，公司無 non-GAAP 營業利益)","value":672,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi2_operating_margin_ifrs","label":"Operating margin (IFRS)","value":13.5,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi3_gross_margin","label":"Gross margin","value":33.0,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi4_free_cash_flow","label":"Free cash flow","value":735,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi5_share_based_compensation","label":"Share-based compensation expense","value":87,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi6_mau","label":"MAU","value":788,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi7_premium_subscribers","label":"Premium subscribers","value":306,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi8_premium_arpu","label":"Premium ARPU","value":4.95,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"€","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_kpi9_guidance_q4_2026","label":"Guidance Q4 2026","value":"MAU 818M；Premium subs 316M；營收 €5.2B（含約 230bps 匯率順風）；毛利率 33.8%；營業利益 €820M（含約 €6M Social Charges，以 Q3 收盤價 $487.38 計）","period":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","unit":"點估計（公司僅給單點，無區間；無全年指引）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-22）","citation":"公司 Q3 2026 Update（6-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm"},"note":"未取得（本輪未查到可靠共識數字；僅與公司自家指引比較）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-22","period":"2026-10-22","unit":"date","basis":"距今 2 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-22"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_spot_gross_margin_pct","label":"SPOT 毛利率","value":32.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPOT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_spot_operating_margin_pct","label":"SPOT 營業利益率","value":14.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPOT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_spot_fcf_margin_pct","label":"SPOT FCF 利潤率","value":18.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPOT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tme_gross_margin_pct","label":"TME 毛利率","value":44.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TME.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tme_operating_margin_pct","label":"TME 營業利益率","value":29.73,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TME.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tme_fcf_margin_pct","label":"TME FCF 利潤率","value":28.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TME.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_nflx_gross_margin_pct","label":"NFLX 毛利率","value":49.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NFLX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nflx_operating_margin_pct","label":"NFLX 營業利益率","value":29.68,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NFLX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nflx_fcf_margin_pct","label":"NFLX FCF 利潤率","value":23.06,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NFLX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_wmg_gross_margin_pct","label":"WMG 毛利率","value":45.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMG.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmg_operating_margin_pct","label":"WMG 營業利益率","value":16.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMG.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_wmg_fcf_margin_pct","label":"WMG FCF 利潤率","value":3.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMG.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":584.22,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":12.78,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_rsi14","label":"RSI(14)","value":70.61,"period":"2026-10-23（RTH 收盤，日線 fallback）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-23（RTH 收盤，日線 fallback）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":2.05,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.18 → 13.45）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.41,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.17 → 17.24）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.05,"period":"2026-10-24","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（21.99 → 21.98）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":13.45,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":17.24,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":21.98,"period":"2026-10-24","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-7.05,"period":"2026-07-30 → 2026-10-24","unit":"%","basis":"FY1 共識 EPS 14.47 → 13.45（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-24","citation":"DD_universe_EPS_estimates_20261024.xlsx"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":43.44,"period":"2026-10-24","unit":"x","basis":"分母＝FY1 EPS 13.45，分子＝快照價 584.22","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-24"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-24","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 584.22 / W52 517.7 / W104 561.97 / W250 338.95 / W250 13週斜率 1.42%"},{"id":"f_ma_w52","label":"52 週均線","value":517.7,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":561.97,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":338.95,"period":"2026-10-24","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.42,"period":"2026-10-24","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-24","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F 風險因素：Apple、Alphabet、Amazon 的裝置預載或預設其自家音訊串流服務，Spotify 自述處於重大競爭劣勢；並提及 AI 帶來新進入者與新消費方式","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"Some of our competitors, including Apple, Alphabet, and Amazon, have developed, and are continuing to develop, devices for which their audio streaming services are preloaded or may also be set as the default providers, which puts us at a significant competitive disadvantage.","as_of":"2026-02-10","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"20-F：新興技術（含 AI）使競爭者推出新的內容消費方式，可能使年輕用戶轉向其他產品，影響留存","source":"SEC EDGAR 20-F FY2025 Item 3.D","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"Our current and future competitors have introduced, and may continue to introduce, new ways of consuming or engaging with content that cause our users, especially the younger demographic, to switch to another product or service, which would negatively affect our user retention, growth, and engagement.","as_of":"2026-02-10","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Midia：Spotify 2025 年淨增訂閱數為各 DSP 最高；YouTube Music 在 MENA 成為第一，並在未來成長市場加速","source":"Music Business Worldwide","url":"https://www.musicbusinessworldwide.com/the-music-industry-is-closing-in-on-a-billion-global-subscribers-with-spotify-out-in-front/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Digital Music News：美國 YouTube Music 訂閱用戶一年增 45%","source":"Digital Music News Pro","url":"https://www.digitalmusicnews.com/pro/2026-08-04-dmn-pro-wkly-youtube-music-yoy-subscriber/","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"customer_concentration_credit#none","axis":"customer_concentration_credit","section":"coverage","direction":null,"claim":null,"status":"not_applicable","source":null,"as_of":null},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Spotify Q2 2026 reported 300M Premium subscribers and 777M MAUs, up 11% and 12% y/y, though earnings missed expectations.","source":"Tribune (Express Tribune) - Spotify tops 300 million paid subscribers despite earnings miss","url":"https://tribune.com.pk/story/2622030/spotify-tops-300-million-paid-subscribers-despite-earnings-miss","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Q1 2026: Spotify added 3M Premium subscribers to 293M despite US price hikes (individual plan $11.99 to $12.99 from Feb 2026); softer North America subscriber dynamics tied to short-term churn from the January price adjustment.","source":"theatdb - Spotify Q1 revenue rises 8%, premium subscribers inch up to 293 million amid US price hikes","url":"https://www.theatdb.com/news/spotify-q1-revenue-rises-8-premium-subscribers-inch-up-to-293-million-amid-us-price-hikes","excerpt":null,"as_of":"2026-04-28","retrieved_at":"20261024","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Management reported steady retention after price increases across 150+ markets; CFO flagged small churn amount; Q4 net adds guide ~8M.","source":"RSM UK - Spotify results: streaming becomes more expensive, but users keep listening","url":"https://www.rsmuk.com/news/spotify-results-streaming-becomes-more-expensive-users-keep-listening","excerpt":"Those costs are now being passed through to subscribers in the form of price increases, however, Management notes that so far it has had no material impact on subscriber churn.","as_of":"2026-02-10","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"Spotify 20-F：2024 年 3 月歐盟執委會認定 Apple 違反反壟斷規則並罰 €1.84 十億（Spotify 為申訴方）；Apple 已上訴，Spotify 介入支持原決定；2025 年 5 月美國法院禁令後 Apple 允許 app 內連結外部購買頁，但 Spotify 不保證 Apple 不會新增費用。","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"In March 2024, the European Commission found that Apple’s conduct was illegal under the European Union (the “EU”)’s antitrust rules and fined Apple €1.84 billion.","as_of":"2026-02-10","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"土耳其競爭委員會對 Spotify 展開調查（2025 年啟動，涉及對權利人的演算法歧視與掠奪性訂閱定價），官方稱不代表已認定違規；Spotify 否認指控。2026-04-21 GCR 另有一則相關條目，日期未核實。","source":"Digital Policy Alert / Turkish Competition Authority（搜尋摘要）","url":"https://digitalpolicyalert.org/change/15334-competition-board-investigation-into-spotify-over-alleged-violation-of-act-on-protection-of-competition","excerpt":null,"as_of":"2025-08-28","retrieved_at":"20261024","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"經搜尋，未見 2026 年美國 DOJ／FTC 或歐盟針對 Spotify 本身的反壟斷行動。","source":"WebSearch 結果（無相關條目）","url":null,"excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"GCR 列出 Spotify 土耳其反壟斷調查（2026-04-21 條目）","source":"Global Competition Review","url":"https://globalcompetitionreview.com/organisations/spotify?page=1","excerpt":"Spotify probed by Turkish enforcer as government criticism mounts Turkey’s Competition Authority is investigating Spotify, having launched the antitrust probe on the same day that a government minister assailed the music streaming service for","as_of":"2026-04-21","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"美國貿易代表署 2025-12-16 威脅對含 Spotify 在內的九家歐洲公司採取報復措施（費用或限制），與歐盟數位規則相關；僅為威脅，未見已實施。","source":"WebSearch 摘要（引述 USTR 聲明）","url":"https://kr.tradingview.com/chart/SPOT/rxvq556d-Spotify-SPOT-Sustainable-Business-Model-Amid-Tariff-Wars","excerpt":null,"as_of":"2025-12-16","retrieved_at":"20261024","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"20-F 風險因素列示國際營運風險，含各司法管轄區法規差異與政治經濟不穩，未特別點名關稅或出口管制。","source":"SEC EDGAR 20-F FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"application of different laws and regulations of various jurisdictions, including privacy, telecommunications and media, cybersecurity, content, AI, corporate governance, labor and employment, environmental, human rights, health and safety, consumer protection, liability standards and regulations","as_of":"2026-02-10","retrieved_at":"20261024","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"FY2025 20-F 風險因子列有美國進出口管制與經濟制裁法遵、部分國家政治經濟社會不穩定等國際營運風險","source":"Spotify Technology S.A. Form 20-F FY2025","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"Bribery Act, import and export controls and economic sanctions laws imposed by the U.S. government, and similar laws in other jurisdictions; and •reduced or ineffective protection of our intellectual property rights in some countries.","as_of":"2026-02-01","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"2026 年 Q3 6-K 前瞻聲明列有貿易政策與地緣衝突等經濟政治條件風險","source":"Spotify Technology S.A. Form 6-K (2026-09-30)","url":"https://www.sec.gov/Archives/edgar/data/0001639920/000162828026066889/spot-20260930x6xk.htm","excerpt":null,"as_of":"2026-10-01","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026：MAU 7.88 億（+11% YoY，淨增 1,100 萬）、Premium 訂閱 3.06 億（+9%）、總營收 €50 億（+16%，固定匯率 +14%）、毛利率 33.0%、營業利益 €6.72 億","source":"Spotify Form 6-K Q3 2026 earnings release (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0001639920/000114036126040435/ef20084028_ex99-1.htm","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261024","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026：廣告支持版 MAU +14% 至 4.94 億；Premium 營收固定匯率 +16% 至 €43.31 億。Q3 廣告分部數字本次未取得","source":"Spotify Form 6-K Q2 2026 / Music Business Worldwide","url":"https://www.musicbusinessworldwide.com/spotify-hits-300-million-premium-subscribers-in-q2-202/","excerpt":null,"as_of":"2026-07-28","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"美國個人 Premium 自 2026 年 2 月由 $11.99 漲至 $12.99，Duo $18.99、Family $21.99、學生 $6.99；公司稱在 150 多個市場近期漲價後留存穩定","source":"Music Business Worldwide / GSMArena / Deseret","url":"https://www.musicbusinessworldwide.com/spotify-hikes-prices-for-premium-subscribers-in-the-us-other-markets/","excerpt":null,"as_of":"2025-11-25","retrieved_at":"20261024","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Futuresource 預測全球音樂串流訂閱 2027 年底超過 10 億、2029 年 12 億；拉美與亞太為主要成長來源（至 2029 CAGR 14%／10%）；YouTube Music 已超越 Amazon Music 成為全球第三大","source":"Futuresource Consulting","url":"https://www.futuresource-consulting.com/the-source/industry-pulse/global-music-streaming-market-set-to-surpass-1-billion-subscriptions-by-2027/","excerpt":null,"as_of":"2025-06-05","retrieved_at":"20261024","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Spotify 在 FY2025 20-F 風險因素揭露：新興技術（含 AI）帶來新的內容消費方式，可能使用戶（尤其年輕族群）轉向其他產品；Apple、Alphabet、Amazon 可能藉由在裝置或作業系統整合 AI 取得競爭優勢。","source":"SEC EDGAR 20-F FY2025 Item 3.D Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"We also face increasing competition because of new or emerging technologies, including AI, and changes in market conditions. Our current and future competitors have introduced, and may continue to introduce, new ways of consuming or engaging with content that cause our users, especially the younger demographic, to switch to another product or service, which would negatively affect our user retention, growth, and engagement.","as_of":"2026-02-10","retrieved_at":"20261024","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Spotify 與 UMG 合作推出授權 AI 混音／翻唱工具供 Premium 用戶使用，CEO 稱其為相對未授權 AI 內容的替代","source":"Neowin: Spotify CEO defends AI music","url":"https://www.neowin.net/news/spotify-ceo-defends-ai-music-wants-you-to-stop-calling-it-slop/","excerpt":null,"as_of":"2026-05-26","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Premium 訂閱主要直接賣給終端用戶，電信夥伴捆綁為次要通路；新訂戶主要由免費版用戶轉換而來；Premium 訂戶由 2.63 億增至 2.90 億。","source":"SEC EDGAR 20-F FY2025 Item 4","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"The Subscription Offerings are primarily sold directly to end users. The Premium Service is also sold through partners who are generally telecommunications companies that bundle the subscription with their own services or collect payment for the stand-alone subscriptions from their end customers.","as_of":"2026-02-10","retrieved_at":"20261024","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"廣告通路由直銷轉向自動化：2025 年直接音樂通路與播客廣告減 1.16 億歐元，自動化通路增 1.03 億歐元；Spotify Ad Exchange 於 2025-04-01 推出。","source":"SEC EDGAR 20-F FY2025 Item 5","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"This decrease was due primarily to a decrease in our direct music channels and ad sales from podcasts of €116 million due to a decrease in fixed-CPM rates as well as a decrease in music impressions sold. This decrease was partially offset by an increase in our automated sales channels of €103 million driven by an increase in music impressions sold primarily on our biddable offerings.","as_of":"2026-02-10","retrieved_at":"20261024","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"Q2 2026 營業利益 guidance €630M 低於分析師共識 €684M（約 8%）；管理層稱高 OpEx 持續至 Q3 後於 Q4 趨緩","source":"TIKR blog","url":"https://www.tikr.com/blog/spotify-stock-is-down-20-in-2026-but-tikrs-1005-target-implies-115-upside-heres-why","excerpt":"The selloff trigger was Q2 guidance: management guided operating income to €630 million against analyst consensus of €684 million, a gap of roughly 8%.","as_of":"2026-06-22","retrieved_at":"20261024","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價均值約 $594.92（37 位）、低 $410.87、高 $704.34，共識 Buy；資料有效至 2026-10-13","source":"Bullstory SPOT forecast","url":"https://bullstory.io/en/stocks/spot/forecast","excerpt":null,"as_of":"2026-10-06","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 列 Q3'26 共識 EPS $3.26／營收 $5.77B，Q4'26 EPS $3.92／營收 $6.03B；Q2 2026 EPS 未達預期（-7.9%）","source":"Benzinga earnings forecasts","url":"https://www.benzinga.com/quote/SPOT/earnings-forecasts","excerpt":null,"as_of":"2026-10-24","retrieved_at":"20261024","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"FY2025 20-F：MLC 於 2024 年 5 月對 Spotify USA 提起訴訟（授權費／強制授權相關），列為風險因素；法律程序另見財報附註 21、24","source":"SEC EDGAR 20-F FY2025 Item 3 Risk Factors","url":"https://www.sec.gov/Archives/edgar/data/1639920/000162828026006874/ck0001639920-20251231.htm","excerpt":"For example, in May 2024, the Mechanical Licensing Collective (“MLC”), an entity designated to administer a blanket compulsory license available under U.S. law, filed a lawsuit against Spotify USA Inc., alleging that Spotify USA Inc.…","as_of":"2026-02-10","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"Pomerantz 律所於 2026 年 5 月宣布調查 Spotify 是否有證券詐欺，起因為 Q1 財報後股價於 2026-04-28 下跌 12.43%；僅為律所調查通知，搜尋未見已提起的集體訴訟","source":"Barchart／Pomerantz 投資人警示","url":"https://www.barchart.com/story/news/2071558/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-spotify-technology-s-a-spot","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"RBX 就 Drake 灌水串流提起的消費者／版稅集體訴訟，法院於 2026-06-22 准許 Spotify 駁回聲請","source":"Music Business Worldwide","url":"https://www.musicbusinessworldwide.com/spotify-wins-dismissal-of-lawsuit-claiming-it-allowed-billions-of-fraudulent-drake-streams/","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"0","claim":"2025-11 收購 WhoSampled（音樂資料庫，條件未揭露）；搜尋未見 2026 年已確認的併購","source":"PrivSource 交易頁","url":"https://www.privsource.com/acquisitions/deal/WNSLM3","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"0","claim":"近 12 個月 6-K 共 16 份，EDGAR 清單無 Item 編號；搜尋未見 SEC 調查或重編財報","source":"SEC EDGAR 6-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001639920&type=6-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 16 份 6-K（外國發行人以 6-K 公告，無 Item 編號）。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2025-11 收購 WhoSampled（條件未揭露）；搜尋未見 2026 年已確認併購","source":"PrivSource 交易頁","url":"https://www.privsource.com/acquisitions/deal/WNSLM3","excerpt":null,"as_of":"2025-11-01","retrieved_at":"20261024","affects":["thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Pomerantz 律所 2026-05 宣布調查證券詐欺（股價 2026-04-28 跌 12.43%），尚非法院案件","source":"Barchart／Pomerantz 投資人警示","url":"https://www.barchart.com/story/news/2071558/investor-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-spotify-technology-s-a-spot","excerpt":null,"as_of":"2026-05-15","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"+","claim":"RBX Drake 灌水串流集體訴訟於 2026-06-22 獲准駁回","source":"Music Business Worldwide","url":"https://www.musicbusinessworldwide.com/spotify-wins-dismissal-of-lawsuit-claiming-it-allowed-billions-of-fraudulent-drake-streams/","excerpt":null,"as_of":"2026-06-22","retrieved_at":"20261024","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"近 12 個月 6-K 共 16 份，搜尋未見 SEC 調查或重編財報","source":"SEC EDGAR 6-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001639920&type=6-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-24 至 2026-10-24 共 16 份 6-K（外國發行人以 6-K 公告，無 Item 編號）。","as_of":"2026-10-24","retrieved_at":"20261024","affects":["triggers"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SPOT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":32.8,"operating_margin_pct":14.65,"fcf_margin_pct":18.04,"rd_intensity_pct":7.36},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPOT","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"TME","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.32,"operating_margin_pct":29.73,"fcf_margin_pct":28.44,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TME","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"NFLX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":49.12,"operating_margin_pct":29.68,"fcf_margin_pct":23.06,"rd_intensity_pct":7.67},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NFLX","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"UMG.AS","period":"TTM ending 2026-03-31（1季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.UMG.AS","as_of":"TTM ending 2026-03-31（1季加總）"},"note":"Total Revenue 缺失，無法算利潤率；僅 1 季可得，非完整 TTM"},{"name":"WMG","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":45.77,"operating_margin_pct":16.11,"fcf_margin_pct":3.94,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.WMG","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"subject":"SPOT"},"financial_history":{"ticker":"SPOT","currency":null,"method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":11727000000.0,"revenue_yoy_pct":null,"gross_margin_pct":24.95,"operating_margin_pct":-5.62,"net_income":-430000000.0,"diluted_eps":-2.93,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":13247000000.0,"revenue_yoy_pct":12.96,"gross_margin_pct":25.64,"operating_margin_pct":-3.37,"net_income":-532000000.0,"diluted_eps":-2.73,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":15673000000.0,"revenue_yoy_pct":18.31,"gross_margin_pct":30.14,"operating_margin_pct":8.71,"net_income":1138000000.0,"diluted_eps":5.5,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":17186000000.0,"revenue_yoy_pct":9.65,"gross_margin_pct":31.98,"operating_margin_pct":12.79,"net_income":2212000000.0,"diluted_eps":10.51,"free_cash_flow":null,"fcf_margin_pct":null,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SPOT/SPOT_Q3_2026_Earnings_Call_20261022.md）

# Q3 2026 Earnings Call
**Spotify Technology S.A.** | Earnings Calls | 2026-10-22

**Operator** (Operator):
Good day, and welcome to Spotify's Third Quarter 2026 Earnings Call and Webcast. [Operator Instructions] As a reminder, this conference call is being recorded. I would now like to turn the call over to Bryan Goldberg, Head of Investor Relations. Thank you. Please go ahead.

**Bryan Goldberg** (Executives):
All right. Thanks, operator, and welcome to Spotify's Third Quarter 2026 Earnings Conference Call. Joining us today will be our Co-CEOs, Alex Norstrom and Gustav Soderstrom; and our CFO, Christian Luiga. We'll start with opening comments from the team. And afterwards, we'll be happy to answer your questions. Questions can be submitted by going to slido.com and using the code #SpotifyEarningsQ326. Analysts can ask questions directly into Slido, and all participants can then vote on the questions they find the most relevant. 
If for some reason, you don't have access to Slido, you can e-mail Investor Relations at ir@spotify.com, and we'll add in your question. Before we begin, let me quickly cover the safe harbor. During this call, we'll be making certain forward-looking statements, including projections or estimates about the future performance of the company. These statements are based on current expectations and assumptions that are subject to risks and uncertainties. 
Actual results could differ materially because of factors discussed on today's call, in our shareholder deck and in filings with the Securities and Exchange Commission. During this call, we'll also refer to certain non-IFRS financial measures. Reconciliations between our IFRS and non-IFRS financial measures can be found in our shareholder deck, in the Financial section of our Investor Relations website and also furnished today on Form 6-K. And with that, I'll turn it over to Alex.

**Alex Norström** (Executives):
Thank you, Bryan, and hello, everyone. Thanks for joining us. Let me start with the strength of the quarter. We made several commitments last quarter, and they've all landed either in line or better than expected. Our revenue came in right in line with what we guided at about EUR 5 billion, up 14% at constant currency. MAU also landed right on target at 788 million. And as we shared last quarter, we're optimizing our MAU growth across markets to scale our funnel and drive revenue growth over time. 
Subscribers came in ahead at 306 million, beating our guidance by 1 million. That strength shows up where it matters the most. Premium revenue grew 15%, driven by both subscriber growth and higher ARPU. Gross margin also came in ahead of expectations at 33%. This is a significant year-over-year expansion. Over the past 12 months, we've generated EUR 3.2 billion in free cash flow. Ads is one of the areas of our business that I've been -- I've spent time talking about. So I want to share our progress. We've been open with you that we are rebuilding this business, and we said the momentum would start to show in the second half of the year. 
And in Q3, ads grew 9% at constant currency, up from the 3% in each of the first 2 quarters. Further, our automated channels continue to scale and sponsorship products are growing, particularly in podcasts. We're moving in the right direction, and there's more progress ahead. And on OpEx, we told you this would be a year of investment with operating expense growth peaking in Q3 and then moderating from Q4 and on. That's exactly what's happening. Christian will walk you through the details further. But as we know from experience, investing in our product, features and brand strengthens our position, and we can see that playing out right now. 
So to build on this further, I'd like to use the rest of my time on what I think is an underappreciated part of our story, durability. When we went public in 2018, we had 71 million subscribers. Since then, every single year, we've been adding 25 million subs or more. And this year, we expect to reach 316 million subscribers. As I've mentioned before, very few consumer subscription businesses have ever reached the scale and few are still adding at this pace. Through a pandemic, price increases and a changing economy and consumer landscape, this steady growth in subscribers hasn't stopped. And this quarter, that growth came from every region. That's what durability looks like. 
Looking across the broader subscription landscape, you all know that not all subscribers are created equal. Spotify not only enjoys industry-leading engagement, but we also have the most passionate and engaged music, podcast and book fans in the world on our platform. We're not just an app, we're a product sitting on a phone, and that's why we continue to grow and take share. Every time we expand what's on Spotify, we bring in new listeners, and we give existing ones more reasons to come back almost every day. 
And Sweden is a clear demonstration of how high the opportunity can go. In our first and most established market, nearly 50% of the population pays for Spotify. Globally, that figure is still under 4%. And in key markets like the U.K. and Germany, it's between 20% and 25%. Latin America is around 11%. And then across emerging markets, we're less than 3%. What makes our position unique is how balanced it is. In developed markets, we're growing at a -- we're growing a highly engaged monetizing base with a lot more room for growth. 
And in emerging markets, we're still early with hundreds of millions of subs to come. This is a growth engine that compounds, building a bigger recurring revenue base. This is durability at scale. We also kept adding to what a subscription is worth this quarter. We signed a new multiyear agreement with Joe Rogan, whose show remains the world's most popular podcast, and we added Believe and TuneCore as a partner for remixes and covers. Remixes are as old as music itself, and we're working on a version that fans love and rights holders trust with consent, credit and compensation at the core. 
And as we've recently announced, we are expanding audiobooks to more than 180 markets by the end of the year, making Spotify the world's first global audiobook service. This enhances subscriber lifetime value, add-on monetization and will benefit Spotify around the world. Gustav will share more about this. So this was a quarter where we did what we said. We've built a strong business that keeps compounding. We invest when we see a path for growth. Our costs are moderating and there's more runway ahead. And having seen a preview of this year's wrapped, I'm really looking forward to Q4 with a lot of excitement, and I can't wait to see how our fans respond. With that, let me hand it over to Gustav.

**Gustav Söderström** (Executives):
Thank you, Alex. So Alex just spoke about durability at scale, and I want to share how we're creating that. So at our recent Investor Day, I talked about 2 ways to predict the future. You can extrapolate what is already happening or you can anticipate what's about to change. And when the world shifted to mobile in 2007, we needed to do a lot of anticipation, imagining and building for a world that we thought would happen, but that didn't exist yet. This worked out well for us, and we accelerated in that new world. For much of the following decade, we and everyone else could instead largely rely on extrapolation of what already existed. 
So that would be more phones, more ads, more catalog, et cetera, which also got us very far. I don't think it's escaped anyone on this call, but today, we are clearly in an era where anticipation is much more important again. So today, I want to talk about 3 things that we anticipated some time ago that are now becoming real and the effects of those. First up is agents. So on our fourth quarter call back in February, I said that we were building the world's first truly intelligent agentic media platform. That may have sounded a little bit abstract at the time, but it's hopefully becoming clearer now. 
What we meant was an intelligent media service encapsulated as an agent, whether you use it directly through our application or via another agent. We made a bet that consumers using services like ChatGPT would also start demanding intelligence from their media service. So we built for that. Spotify is now an agent that you can not only click on in our app, but talk to, ask questions of and instruct. We can do things today that no other media services can do. For example, you can ask Spotify to go through your listening history, song by song back to 2008, picking your true favorites, beat stretching them by speeding them up or down and then sorting them by key and BPM. 
Then you can ask it to mix them together into the perfect running playlist at your exact cadence. But that's not all you can do, you can also ask Spotify exactly who wrote and performed what on each track. And if you want to shift gears entirely, we can also generate an individual podcast just for you as well as recap the book you're reading up until exactly where you stopped. As we prepared for this agentic world, we also thought through what our ubiquity strategy would mean in an agentic age. Spotify's strategy has always been to be the best experience wherever people listen. As an example, nearly a decade ago, as connected speakers took off, we rebuilt our entire technology stack to make Spotify very easy to integrate across speakers, something called the eSDK. So TVs, gaming, consoles and other devices. 
That investment turned the growth of the connected device industry into a tailwind for Spotify, one that actually continues to pay off even today. So for the agentic age, we are betting on consumers using many agents and that Spotify will be by far the best media platform for licensed content inside and across all these agents. So before most people were regular users, we integrated Spotify into ChatGPT, making Spotify the first service available. This was also the case with Meta Ray-Bans, OpenAI's Dots, and we were the only media service integrated into Meta's Muse at launch. The list goes on and on. We are simply everywhere so that whenever you find a great song, a book or a podcast or even want to create a podcast of your own, it's right there. 
You just save it, playlist it, and it shows up in Spotify in your Morning Commute. Importantly, this is not just a technology strategy. It's also a business strategy. We think Spotify is unusually well positioned for the age of agentic AI. This is because Spotify, unlike most companies, can monetize from the background. Whether you're a premium user or a free user listening to our audio ads, our business model not only works but thrives while Spotify is in the background. This is actually not something new. The Spotify app has been in the background of apps like Waze and Google Maps during the commute for decades now. 
Zooming out, Spotify is in one of the few categories that actually stands to thrive in the agentic age. This is because agents, as I'm sure you know, excel at replacing and taking care of things that people would rather not do, like maybe paying bills, answering e-mails, booking restaurants, checking your kids' school schedule, et cetera. This is where you see services like Muse absolutely thriving. People love getting rid of choice. But entertainment is the opposite. Nobody asked an agent to summarize a song for them. The whole point of getting rid of this choice is to free up even more time for the things that you actually enjoy. 
The second thing that we anticipated was moving Spotify from a passive and single player experience to an interactive and multiplayer experience. You know our multiplayer offerings. We've talked a lot about them, popular features like messaging, Jam, collaborative playlists and comments. So today, I'd like to spend a moment on the interactivity side. The original interactive experience on Spotify was not surprisingly playlisting. Millions and millions of people put songs together and helped organize the world's music library. That became the foundation of our recommendation engine. 
Last quarter, I talked about SongDNA as one of our all-time fastest-growing features. This quarter, mixing tools offers another example of what happens when people can do more with the music. We started rolling mixing tools out about a year ago actually. It was good then. It is much better now. Almost 40 million premium users now listen to mix playlist. Consumption is growing 90% quarter-over-quarter and millions of people create mixes of their own each month. So why does this matter? Well, playlists always told us which songs go well together, but mixing also tells us exactly how and when they fit down to the millisecond. Those signals improve our large taste model, our recommendations and what the Spotify agent can do. 
Better recommendations strengthen retention over time. It also tells us something encouraging about the future of remixing, give people good tools and they will invest in shaping the music themselves. The third thing that we anticipated was the opportunity in books. When we first discussed audiobooks, we said our geography gave us a unique perspective. In Sweden, audiobooks are almost as big as music, and we wondered whether that was purely Swedish behavior or simply early behavior. What we're seeing now suggests the latter. That's why we're expanding audiobooks. We want to grow the market itself by giving hundreds of millions of people a great, affordable way to listen, not just compete for shares of today's market. 
When people adopt audiobooks, they come to Spotify on more days. Audiobooks started as a bet. It's now a global business, and it's still early. All of this connects to how we're building an even stronger subscription business. In addition to the growth of audiobooks and Premium, we're expanding the Spotify partner program, a fan favorite among passionate podcast listeners to 35 more markets this fall. And 2 days ago, we launched creator memberships, so fans can directly support creators and get member-only experiences. 
This is another example of capturing the power law that we discussed at our Investor Day back in May. There is a power law within each creator's audience. Some fans want to go deeper and are willing to spend more, and now they can do that right on Spotify. These offerings will add value as they scale. And where we've offered audiobooks and the Spotify Partner program the longest, they're contributing to acquisition, retention, active days and margin improvement. With that, I'll hand it over to Christian.

**Christian Luiga** (Executives):
Thank you, Gustav, and thanks, everyone, for joining us today. I'll cover the quarter 3 results and then provide some perspective on our outlook. Unless otherwise noted, as always, our reference growth metrics are presented on a year-over-year constant currency basis. We have another solid quarter behind us. Starting from the top, MAU grew in line with our guidance of 11 million to 788 million, up 11% year-over-year. We added 6 million net subscribers during the quarter, growing quarter-over-quarter across all regions. 
We reached 306 million, which was 1 million ahead of our guidance. Our out-performance was broad-based and led by rest of the world and Latin America. Total revenue was EUR 5 billion, growing 14% year-over-year. Premium revenue rose 15% year-over-year, driven by subscriber growth of 9% and ARPU expansion of 7.5%. Ad-supported revenue growth improved to 9%, as Alex said, this quarter, led by strong growth in our automated biddable sales channel. Our gross margin came in at 33%, surpassing guidance by 10 basis points and representing year-over-year expansion of around 140 basis points. 
Operating income of EUR 672 million was a bit above our guidance, delivering on operating margin of 13.5%. Social charges of EUR 22 million were EUR 13 million higher than forecast due to share price movements in the quarter. Excluding the non-forecasted social charges, we came in EUR 15 million above guidance, driven by favorability in marketing, personnel-related costs and gross margin out-performance. Finally, free cash flow was EUR 735 million in the quarter and included unfavorable timing effects in working capital and cash taxes. 
Year-to-date through October 21, we have repurchased 2.2 million shares for USD 1.1 billion. This means that we have neutralized this year's dilution from our employee equity programs, and we have also initiated the return of excess cash. Since we resumed our buybacks in August 2025, we have repurchased about 3 million shares or approximately 1.5% of shares outstanding. Our capital allocation strategy remains focused on attractive return opportunities, first, through organic and inorganic growth initiatives, followed by opportunistic returns to shareholders. 
As of the close of the quarter, we had EUR 9.9 billion in cash and cash equivalents and no debt other than lease liabilities. Looking ahead to quarter 4, we are forecasting MAU of 818 million, an increase of 30 million from quarter 3. Our guidance reflects healthy growth across all regions. Growth is not as high as last year's all-time high, which benefited from a very successful rollout of our new free tier. On subscribers, we're forecasting 316 million for quarter 4 or a net addition of 10 million. We're also forecasting total revenue of EUR 5.2 billion in quarter 4. This reflects a year-over-year ARPU increase of 4.5% to 5%, driven by recent pricing actions and the performance of our Audiobooks+ add-ons. 
This is partly offset by the lapping of prior year pricing actions across more than 150 markets. Our advertising business is coming out of a longer period of single-digit growth. In quarter 4, we expect to continue our progress towards double-digit growth. We anticipate a quarter 4 gross margin of 33.8%, approximately 70 basis points above prior year. Our gross margin outlook includes initial investments in the expansion of audiobooks to more than 180 markets and the Spotify Partner program to more than 50 markets. These rollouts can drive new value for our subscribers and the business, the same way we have seen it over the last 3 years. 
Taken together with the first 9 months of the year, our quarter 4 outlook implies a full year gross margin expansion of approximately 130 basis points compared to 2025. Moving to operating income. We're guiding to EUR 820 million in quarter 4. OpEx growth is now coming down meaningfully, and we expect that moderation to continue into 2027. We see that this year's incremental OpEx is driving multiple benefits to our business. Our marketing investments have helped consumer awareness of the value we deliver, supporting future subscriber growth and monetization. And on AI, our investments have accelerated feature shipping while keeping headcount flat, setting the business up for further engagement and monetization potential. 
Our taste model investments are already paying off. Early deployments show double-digit gains in content discovery and our users are spending more time in select algorithmic sets. As we have said before, we remain focused on striking a clear balance between enhancing LTV and sustainable margin expansion. In conclusion, we're very pleased with how we're tracking into the end of 2026. It's too early to give guidance on 2027. And as I've said before, quarterly progression of our margin can be variable due to seasonality and the timing of investments. We remain confident in our path and expect another year of progress towards delivering on our 2030 goals. We are well positioned to continue compounding growth, profitability and free cash flow. With that, I hand it back to you, Bryan.

**Bryan Goldberg** (Executives):
All right. Thanks, Christian. Again, if you've got any questions, please go to slido.com, #SpotifyEarningsQ326. We'll be reading the questions in the order in which they appear in the queue with respect to how people vote up their preference for questions. And today's first question is going to come from Sean Diffley, and it's on the free tier. Please discuss early learnings in markets like India and Indonesia, where you're adding some friction to the ad-supported tier and how we can think about conversion to paid in those markets?

**Alex Norström** (Executives):
Thanks for the question, Sean. It's been rolling up as the most important question here in the queue. So let's go right at it. So last quarter, I was making a few comments on some changes that we're making to our product and our funnels and in particular, in the emerging markets, and you're mentioning 2 of them here. These changes include things like better data hygiene and our sign-up flows, ad load adjustments and effort around migrating users from lower-end device clients over to a better client that retains you better and thereby giving you high LTV and so on. 
So all these things that we're doing that you're alluding to and I just spoke to are business positive. These are good things for our free tier. These are good things for our subscription tier and thereby also for our revenue. And we have a long track record of durable growth. I just spoke about that in our early -- in our initial remarks here. And this durability that we've been talking about is really the result of a lot of these types of optimizations, and this is just another example of that. And speaking of like India specifically, it's a market where we have 1.4 billion users. We see GDP growth of 7% to 8% several years in a row. What better market is there for us to work on to improve our business growth I think. I see no other. This is an incredible market and tremendous opportunity for us.

**Bryan Goldberg** (Executives):
All right. We're going to have another question from Sean Diffley this time on capital allocation. It appears you've stepped up the pace of share repurchases. Can you discuss how you're approaching capital allocation with free cash flow ramping? And is there room to increase the buyback cadence further?

**Alex Norström** (Executives):
I'll start, and then you can jump in, Christian. So we mentioned during our Investor Day now almost half a year ago that the way we approach this is we will invest in organic opportunities primarily. As we see good return, we will deploy, and you've seen us do that. And with respect to inorganic opportunities, we will do those too. But there's no real change there. You've seen us do that many times before with companies like WhoSampled, who helped us provide a unique data sets to ramp about the song, which is now used by almost 100 million people. 
You saw us acquire Findaway, which helped us accelerate audiobooks. You saw us buy Sonantic, which helped us do AI DJ. So we'll continue to do this as we see opportunity. And then beyond that, if there is excess cash flow, we will start engaging in buying back shares. And you've seen us do that this year. We've mentioned that we're going to buyback shares to counter the dilution that's coming from the stock -- employee stock programs. And we've mentioned that, that's about 1 million shares, and we've done that. We're now up to 2.2 million shares in buybacks, totaling about $1 billion or a little more than $1 billion. And so we're making progress also there. Christian, is there anything you would like to add?

**Christian Luiga** (Executives):
Yes. I just want to wrap it up by saying that we will maintain a degree of strategic flexibility with a strong balance sheet. And so you will see us have a strong balance sheet and a cash balance that makes us be flexible in strategic moves. In the same time, as Alex said, we are -- it's obvious with the cash flow we have, compounding and on the balance sheet that we will start to return excess cash to shareholders, which we've proven this quarter.

**Bryan Goldberg** (Executives):
All right. Our next question is going to come from Jessica Reif Ehrlich on our ubiquity strategy. As listening shifts to third-party AI agents as with the new Muse integration, who owns the customer relationship and the data? And how do you keep that from turning Spotify into a back-end supplier?

**Gustav Söderström** (Executives):
Thank you, Jessica. It's a great question. So I get the chance to talk about things I love. So a few things. First of all, it's important to say that listening is actually not shifting. All the listening is happening through Spotify. We are not sending the music or anything to any of these agents. What is happening is you're talking to that agent with remote control Spotify in the background. So the listening is not shifting. It's actually happening and thus increasing through Spotify. What -- how we think about this, though, is, as I said in my prepared remarks, as another example of the ubiquity strategy. 
So when connected speakers started happening, we try to figure out how we turn that into a tailwind for Spotify and grow with the connected speaker market. As I said, we rebuilt our technology stack, something called the eSDK, the embeddable SDK, making it dead easy for any speaker provider to integrate Spotify. That turned into a great growth vehicle for us. This is why we're ubiquitous today. Thinking the same way about this, we rebuilt Spotify as an agent so that it is dead easy for other agents to integrate us and talk agent to agent. So what this means is that inside an agent like Muse, you can say, I would like to have -- I would like to create a podcast about this and that, that you've been talking to a news agent about. This podcast gets published through Spotify, but only visible to you so that you can listen to it in the Morning Commute. 
Now what happened there is actually that we learn more about you because that podcast is now inside Spotify. So we know things that we wouldn't have known otherwise about your interest. So this is actually a positive data loop for Spotify rather than the other way around. So this is the reason why we made all of these investments. specifically the large taste model. I've gone on and on about it, but this is the reason we built this because this is a value of Spotify. Our agent is the best in the world at understanding your taste across all of these mediums. So we are not sending the data to these partners. They are asking us about something. We do the reasoning over everything we know about you and then decide what to play for you. 
So this is also the reason why we built all of this technology, as I talked about in my prepared remarks, to be able to beat stretch the music, put it together in the right way. As you know, we're also investing in remixes and covers and so forth. So our goal is to be the media service that you use from any agent, really turning the growth of agents into a tailwind rather than a headwind. And that's exactly what we're seeing now. We're seeing really good adoption of Spotify inside these agents. 
And so while other companies are maybe trying to figure out what to do and many are leaning out, we're actually leaning in and participating in the growth instead of standing by the roadside and looking at it. So we're very, very excited about this. This is what we said we were going to be the world's first truly intelligent media service, and this is why we've invested in all of this technology.

**Bryan Goldberg** (Executives):
Okay. We've got another question from Jessica Reif Ehrlich. This time on the Premium business. In the third and fourth quarter, there are many new product rollouts from audiobooks globally to Reserved, Fitness, and the expanded Spotify Partner program, Taste Profile in the U.S., et cetera. What is the 2027 road map for monetizing all of these products and new features, i.e., through new tiers, add-ons or price increases?

**Alex Norström** (Executives):
Jessica, Alex here. I see that we're excited about 2027. I am really excited about '27 as well, but it's going to be premature for me to talk about specificity around next year. But I'll give you a bit of like how Gustav and I think about the underlying recipe here. So really, the work to be done inside Spotify is to add value to our free tier, add value to create a better and better free product. And you've seen us do that. About a year ago, we launched the new Spotify free tier, which is the best free tier out there, and that's kept yielding results over the past 12 to 18 months. 
The other thing we do is, of course, to enrich our premium tier. And I can't -- to your point, I can't really remember a time in Spotify's history where we've added so much value back to the premium tier like this current year here. And then we create products on top of that for the niche audiences and the power law like we've talked about. And then the third step in this is really just to figure out how to monetize all of this value that we add, whether that be by way of advertising sales or price increases, add-ons, more subscriptions and better engagement across more days of the month. This is really like a simple but very powerful recipe that we've followed and deployed for many, many years now.

**Bryan Goldberg** (Executives):
Okay. Our next question is going to come from Eric Sheridan. This time on the ads business. With respect to ads, can you discuss how the third quarter results track relative to your expectations for a second half 2026 growth inflection? Is there any color on the underlying drivers of advertising performance embedded in your overall Q4 revenue commentary?

**Alex Norström** (Executives):
They're tracking really well against our expectations. We have talked about this before. We have been hard at work for some time now in rebuilding the underlying stack and foundation for advertising sales business at Spotify. And I'll tell you this, there's a lot of things that have been changing, but there's these 3 things that have not changed, and they remain why advertisers are interested in coming to Spotify. One is that we have a beloved brand, Second of all, we have high-quality content. It's licensed content. And we also have high-quality engagement. It's not just about the hours, it's also about the moments of the day and the context you're in and as many days in a month as possible. 
We've talked about that before. So these remain the reason for why our special corner of the Internet is still very interesting for advertisers to associate themselves with. Now what then is our job internally? Will this -- in light of this to just make it easier and easier for advertisers to buy the special inventory, whether that be by making for easier automated attachment to Spotify or whether that be creating better measurement or whether that is to broaden the demand for audio specifically, whether it's making it easier for folks out there to create audio ads and so on. All of this is -- are things that is underway. We've done a lot of work already, but this will just continue to improve, and this is what's sort of powering the Q4 guidance.

**Bryan Goldberg** (Executives):
Okay. We got another question from Eric Sheridan, some on investments. Can you discuss how investors should think about the forward trajectory of growth investments, especially across AI and cloud when measured against the potential for scaling AI-led experiences and products on the user side in the coming quarters?

**Gustav Söderström** (Executives):
Yes. Thanks, Eric. This is Gustav. So I'll talk about this from a few different lenses. There is obviously productivity within the organization, then there is cost on the consumer experience. First of all, Alex and Christian and I, we said earlier this year that we were going to invest a little bit ahead because we saw a lot of opportunity. So one question that you didn't ask, but I'm going to answer anyway is like, what did we get for the investment? Well, first of all, we also said that these investments and these costs were going to start moderating in Q4, which they are. 
As Alex said in his opening remarks, this is a quarter of doing what we said we're going to do. So they're moderating in Q4 and into next year, just as we said. But it's still valid to ask what we got. Well, we got a lot of investments in platform that excites us. I've spoken at length about the large taste model, but I also want to talk a little bit about the results of the large taste model that we're now seeing already. So we're seeing double-digit growth in discoveries, which is one of the leading metrics for how exciting you think Spotify is. I think it surprises no one, but if you never find any new music, eventually, you're going to get less excited about this product. So that is a very important metric to us. 
I also want to say, I mean, it's very early. We're just rolling this out, but it is already on track to add billions of listening hours per year. And my experience with these things is you get a lot of incremental improvement as you start iterating on these things. So I'm very excited about what we're seeing because this was a large investment. This also goes to the earlier question of the value we're creating in a world of agents where you interact with Spotify through other agents. This is the value. So we're seeing exactly what we want to see. But more than that, we also invested in a lot of AI features. I talked at length about user control, interactivity, being able to ask for what you actually wanted. 
And this idea that what LLMs allow you to do is to finally talk to Spotify in English. So one question could be, is anyone talking to Spotify? The answer is yes. There are now tens of millions of people speaking to Spotify in English, which I think is remarkable. That doesn't really happen on any other media service yet. So we're very excited about the adoption that we're seeing of these features. Another favorite I mentioned in my opening remarks is mixing tools, which is scaling like crazy. So we're feeling very good about the return of this investment. But I want to reiterate, we said that the costs were going to moderate, and they are moderating now in Q4 and into 2027. 
So I think that covers roughly how you should think about it. On the -- I just want to comment also on the productivity side of our engineering. Not only have you seen large cost cuts from the labs in terms of token costs, et cetera, that are obviously very helpful for us. But we have been investing ourselves in these platforms that you heard about Xirp, et cetera, where we can route between agents, including open source models. We've done a lot of investment in controlling our own costs. And now we're seeing 2 things I'm very excited about. We have very clear cost controls where we can route to the models that we want. 
But we're also finally seeing the next level of productivity. I think most -- many companies have said that they see 100% growth in lines of code, PRs, et cetera, and so have we. But there is a question like does that actually translate into end-user features. And now as we've gone through, we have 6 months development cycles, we are seeing significant acceleration in end-user products. There are shipping what we call DoDs, definitions of done, things that are merged and shipped to end users. 
So we are shipping much more. And then the last part of that question is, well, does that translate into actual value? And I just told you that it does. We see engagement, retention, active days going up, not just across products like audiobooks, but also across discoveries, sales, listening hours, et cetera. So I feel very good about where we are right now. As Christian always asked me to say and always says, we are going to keep being diligent with our costs as you've seen us be for the several last years, but you will also see us take these opportunities when we see them.

**Bryan Goldberg** (Executives):
All right. We've got another question here this time from Rich Greenfield on the Advertising business. While ads growth recovered as you expected, is there a realistic path where advertising actually lifts Spotify's overall revenue growth rate? Could that be a 2027 event?

**Christian Luiga** (Executives):
Thank you, Rich. Christian here. So as you say, we are recovering as expected, as we said for a long time, we will move towards the double-digit growth in the second half of 2026. And in quarter 4, we are also continuing to do our progress towards double-digit growth. This is driven by biddable, which is now up to 40% and also podcast, as Alex alluded to before. So going into 2027 and going into a path journey in the future where we are in double-digit growth, of course, that is important. Even if ad support is only 10% of the revenue today, it's much better to have 10% revenue growth or above than having a low single-digit growth. So that will, of course, drive the revenue growth from the total.

**Bryan Goldberg** (Executives):
Okay. We've got another question from Sean Diffley. This one on our in-house tech. You recently started selling your own internal software tools to other companies as you are becoming an R&D operating system. Can you please discuss the rationale here and how big of an opportunity this can be?

**Gustav Söderström** (Executives):
Yes. So I think the way to think about this right now is mostly as option value. The reason we're doing this is because as we just talked about, we invested quite a bit to be able to be at the very forefront of agentic development. And so then what happened is, not surprisingly, a lot of other companies asked us about that and said we would also like to use this technology. And because we've taken these costs anyway, we could choose to just amortize them over our few thousand developers or we choose to amortize them over more developers. So that's how we're thinking about it. We've taken these costs anyway to stay at the forefront, and this is a way for us to amortize those costs more efficiently. That's how we're thinking about it right now. I'm not going to give any more guidance on this right now. Think about it as option value for the time being.

**Bryan Goldberg** (Executives):
Okay. Our next question is going to come from Jason Bazinet on the family plan. It was recently reported that you're beginning to crack down on family plan subscribers that don't live in the same home. What markets are you pursuing this enforcement? How long before the implementation is complete? And what financial impact do you expect from this?

**Alex Norström** (Executives):
Jason, this is not as much a crackdown as it is actually a routine improvement of our verification methods for our Family Plan. Family Plan has existed for a long while. It's been around for, I think it's now close to 12, 13 years in Spotify history, and it makes up a pretty significant proportion of our subscriber base. And as such, it's important for us to just make sure over time that we improve the verification methods that we have because there are certainly ways to -- over time to find holes around it. So -- and as that happens, we figure out how to improve it over time. This is not something that has an end date. It's not an implementation that's going to complete. This is just ongoing routine.

**Bryan Goldberg** (Executives):
Okay. Our next question is going to come from Justin Patterson on AI investment. Now that you've had nearly 1 year of deploying new tools like Claude Code, could you talk about your view on AI ROI and how that's evolved and shaped your thought on investment levels?

**Gustav Söderström** (Executives):
Thanks, Justin. This is Gustav. I think I already mentioned this. We saw the typical early productivity metrics of lines of code, pull requests, et cetera, that I think everyone is seeing. But I don't think everyone is yet seeing the 2 harder productivity metrics. And we are as we've now had about 2 cycles So with cycles, I mean, 6-month development cycles because we roughly plan in 6-month increments. And then we measure. We decide what we're going to do for 6 months, then we build it and then we can measure how much of that we delivered. And we are seeing very significant acceleration in the last 6-month cycle in actually building and shipping end-user features. 
So I feel very good about that AI ROI. And obviously, as I said, the next step is to figure out, sure, it's great shipping features, but is anyone using them? Are they producing engagement, retention and revenue. And as I said before, it's actually all of the above. It's producing -- we have adoption, producing engagement, increases retention, but it is also, in the case of audiobooks, driving direct ARPU. So we feel very good about what we're seeing right now, which is why you should expect us to sort of remain at these investment levels. 
But as I said before, hopefully, by now, it's becoming clear that we're pretty diligent about these opportunities. We try to understand what the business case is. So you're going to see us roughly at the same levels. We're going to take these opportunities when we see them, and we're going to communicate them the way we have.

**Bryan Goldberg** (Executives):
Okay. We've got another question from Jason Bazinet this time on capital allocation. You've got no debt, nearly EUR 10 billion of cash and cash equivalents. How do you expect to use this cash to create shareholder value?

**Christian Luiga** (Executives):
So Jason, Christian here, thanks for the question again. I will just go back a little bit to what we said before. I mean having a strong balance sheet gives us strategic optionality and flexibility to create shareholder return. And we have said that we will do that by investing in our organic journey, but also inorganic journey. 
And on top of that, as we've been very clear, we think that with this high number of cash pile that we have on top of the cash flow compounding over time, that we will start to return cash to shareholders all the excess cash. And that's what we have started doing in quarter 1. So there's no news on that. And I think it's a quite clear message, and we work very opportunistically in how we invest.

**Bryan Goldberg** (Executives):
Okay. Our next question is going to come from Justin Patterson this time on Studio. While agents and assistants do not seem disruptive to your business, it does seem like something that could encroach upon emerging products like Studio by Spotify, which builds custom podcasts and has assistant-like capabilities. How do you believe the opportunity for this product has changed?

**Gustav Söderström** (Executives):
Yes. So I think the way to think about Studio is back to anticipation. We anticipated that these kind of agents were going to happen. So we built the ability to use Spotify agentically in our desktop client for the sort of hardcore frontier users. And we learned a lot. This is why we have these features like creating podcasts. Then we also built skills for them so that third-party agents could also create them. And as I explained before, it is very valuable when someone creates Spotify content through these third-party agents using their personal context about their life that just makes Spotify more valuable. 
So we think this is definitely a tailwind for us. But you will still be able to create these things inside Spotify as well. I think again the best analogy is our ubiquity strategy that has been very successful for us in the age of connected speakers and devices, where we built this layer where you can use Spotify from any third-party interface, but using Connect, we can still control and understand the playback. That is the way to think about this as well. It is sort of Connect for the agentic age. I think the opportunity is very large for us. I think personalized content is clearly happening, and that's why we invested towards it early.

**Bryan Goldberg** (Executives):
Okay. We've got a question now from Doug Anmuth on our audiobooks expansion. How should we think about the margin impact of expanding audiobooks from 22 markets to more than 180 by year-end? And can you see similar positive benefits as you did in the early launches?

**Alex Norström** (Executives):
We certainly see similar positive benefits, which is why we've decided to go broad and basically have the first global Audiobooks business. And I want to take you back also a little bit to how this started. One very powerful way to detect really what the desirability is of the different types of content is to just follow your users' lead. And this is now almost 3 years ago when Gustav and I saw the uptake of audiobooks in Germany popping just as a -- really as an accident, someone uploaded some audiobooks onto our service and really saw that users were captured by this type of content. And so we started this little project between Gustav and I and a small crack team. We worked at it. We saw that there was tremendous opportunity and that we can make a difference. 
We could certainly be helpful in bringing more book listeners to the world. So we decided to set a sail. And now we're 3 years later, and we've had a good 3 years of real positive benefits. We've increased our audiobooks listenership by 40%. This is even before launching to the rest of the world. And we've seen listening hours grow as well. And the impact -- the way you think about the impact is really that we've increased the number of days that people are active on Spotify, which ultimately drives retention and also lifetime value. 
We've also seen early but very strong indications on add-ons for this type of category really working out. So that taken together, this is great for our users, and this is great for Spotify, and we are super excited about the launch that we're doing right now. And as far as margin goes, the way to think about that is we've set targets at Investor Day, and we're marching towards those targets.

**Bryan Goldberg** (Executives):
Okay. We've got a question from Rich Greenfield on AI agents. As agents like Muse and Instinct take over the interface, they could compare subscription prices, switch services seamlessly or cancel ones that go unused. If the agent owns the relationship, what keeps Spotify from becoming an interchangeable back-end pipe is churn from agents a real risk?

**Gustav Söderström** (Executives):
Thanks, Richard. Excellent question. I'm going to answer in 2 parts. First, I want to, again, push back a little bit on the -- as agents like Muse and Instinct take over the interface. The way to think about it is Spotify has been integrated into, for example, Google Maps and Waze for decades. We haven't talked about it because I didn't want competition to understand, but it's been fantastic for us. So people have been using Spotify through Google Maps and Waze during their commute for years. That has been tremendous growth for us because Spotify and its business model works in the background. 
So that was not negative for us. We didn't get commoditized. We actually grew tremendously. So that is the way to think about this as well. Spotify being integrated is a growth vector for us. As long as we feel comfortable about our differentiation in terms of data and experience, which I've talked at length about, which we feel very comfortable about. So yes, these things are an interface in front of us, but that's been true for some time. And we think it's a good thing. It's driving growth for us. Now on the second part of the question, which I think is excellent, the first thing that Muse as an agent asks you as a user is often like, "Hey, want me to go through your e-mail and try to help you find subscription that you're not using." And the important part of that is the last sentence that you're not using, right? 
So the good thing for Spotify is we will never bet on you forgetting about your subscription. We will never bet on breakage or trying to trick you. In fact, I think Alex has talked about this. We have over 100 million users that use Spotify sort of 28 days of the month. We're one of the most highly engaging services in the world. So when we ask our users -- we're not interested in breakage either. When we ask our users, how many of them subscribe to Spotify without realizing it, it's basically no one. So we think we are one of the best positioned services in the world for this age. 
I actually think this will be helpful for us. It's a bold bet but I think on that list of things that you unsubscribe from, Spotify is going to be the last thing that you unsubscribe from. We know this from -- previously, we've been around for 20 years. We've gone through financial crisis, et cetera. We're one of the most resilient subscriptions that exists. And it is because we never bet on you forgetting about your subscription. I think the other thing, the opposite could also be true. I think these agents are going to help you subscribe to the best music service, to the best podcast service and help you understand that Spotify is actually a better deal.

**Bryan Goldberg** (Executives):
All right. We've got time for about 2 more questions. The next one is going to come from Batya Levi on new product. How has demand been for the new features you've launched this year, Taste Profile, Prompted Playlist, et cetera? And as the product delivers more value, how do you balance raising prices against growing the subscriber base?

**Alex Norström** (Executives):
Thanks for the question, Batya. So we've used the concept of value to price ratio and also the value stick many times. And I'll remind you of this one because this is really how we think about launching product, adding value and then how to price it. It really comes down to us figuring out how the subscriber is going to win, meaning to get an improved value to price ratio over time. Now in the first 15 years of Spotify, we had a lot of investment in just value, better product, better content experiences, just better everything all the time every year. 
And as we sort of grew and got scale, then we started engaging in price increases, which helped us monetize and reinvest that monetization back into the product for more value. So that's the journey we're on. So as you can see us launching more product, adding more content verticals onto the platform, it's just simply us wanting to add more value to subscribers and users so that they can win when it comes to value to price ratio over time. And so that's really how we balance raising price against a growing subscriber base.

**Gustav Söderström** (Executives):
And just to fill in there, I think I covered already the demand. We're very excited about the demand that we see for these AI-based features. We talked about SongDNA, but also features like About the Song is also on its way to 100 million users with tens of millions of people talking to Spotify, several tens of millions of people listening to these agentic sets. So we feel quite good about the demand for them.

**Bryan Goldberg** (Executives):
All right. And our last question today is going to come from Michael Morris on music industry partnerships. Universal Music Group and Warner Music Group agreements reached their 2-year mark in the first quarter of 2027. How do your 2027 pricing plans and the add-on tiers factor into renewal talks on core streaming terms? And do you expect the renewed agreements to be structured like your current deals?

**Alex Norström** (Executives):
Now of course, we don't speak to the specific of agreements with our partners. But I can say this, this is a reoccurring 2-year rhythm that we've more or less had forever in Spotify's lifetime. And to your point, now we're coming up on another one. And we're excited. We're working with our partners and relationship is just improving. And it's improving primarily because our interests are aligned. So when our interests are aligned and growing even more aligned, then that makes it easier for us to create win-win situations.

**Bryan Goldberg** (Executives):
All right. Great. So we've reached the end of today's Q&A session, and I want to turn the call back over to Alex for some concluding remarks.

**Alex Norström** (Executives):
Thank you, Bryan. So to close this out, we are building a durable business at scale with a tremendous amount of opportunity ahead. And as I said at the top of the call, this quarter, we did what we said we would, and that's how we'll keep running the business. Thank you all for joining us.

**Bryan Goldberg** (Executives):
All right. Thank you, everyone, for joining and for your interest in Spotify. A replay of today's call will be available on our website and also on the Spotify app under Spotify Earnings Call Replays. We look forward to speaking with you all soon.

**Operator** (Operator):
This concludes today's conference call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SPOT_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 MAU 預測 7.88 億（原話："we are forecasting MAU of 788 million"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 訂閱數預測 3.05 億（淨增 500 萬）（原話："we are forecasting 305 million for quarter 3"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 營收預測約 50 億歐元、成長 14%（原話："total revenue of approximately EUR 5 billion in quarter 3"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 毛利率預測 32.9%（原話："We anticipate a quarter 3 gross margin of 32.9%"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 給 Q3 營業利益預測 6.7 億歐元（原話："We're guiding to EUR 670 million in quarter 3."）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 重申全年行銷與 AI 投入帶來約 2 億歐元增量營業費用（原話："approximately EUR 200 million in incremental"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 指 Q4 營業費用年增率將趨緩（原話："Quarter 4 is well positioned to see a moderation"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 重申廣告業務下半年轉為雙位數成長（原話："We continue to expect our ads business to inflect"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 表示不給全年毛利率與營業利益率數字，但預期全年皆改善（原話："improve in 2026 on a full year basis"）
- 2026-08-04｜CFO Christian Luiga｜guidance：CFO 預期 2026 年自由現金流有意義成長（原話："meaningful year-over-year growth in free cash flow in 2026"）
- 2026-08-04｜Co-CEO Alex Norström｜commitment：共同 CEO 重申 2030 年目標：毛利率 35% 至 40%、營業利益率高於 20%（原話："of 35% to 40%, operating margin above 20%"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 報告 Q2 毛利率 33.4%，高於財測（原話："Gross margin came in at 33.4%, surpassing"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 說明毛利率優於財測含加拿大數位服務稅一次性迴轉（原話："small onetime benefit from cancellation of the Digital"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 報告 Q2 營業利益 6.55 億歐元（原話："Operating income of EUR 655 million"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 拆解營業利益優於財測中社會費用的貢獻（原話："Social charges contributed to EUR 9 million"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 說明 Q3 營業費用成長（扣除匯率與社會費用）與 Q2 大致相同（原話："roughly consistent with quarter 2"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 說明廣告自動化銷售轉為規模型業務，廣告利潤率目標由 20% 區間往 40%（原話："move from the 20% range we have today towards 40%"）
- 2026-08-04｜Co-CEO Gustav Söderström｜margin：共同 CEO 稱利潤率是管理出來的結果（原話："Our margin is a managed outcome"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 報告廣告營收年增 3%，與 Q1 相同（原話："Our Ad-supported revenue grew 3% year-over-year"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 報告自動化通路占廣告營收近 4 成（原話："represented nearly 40% of our ad-supported revenue in"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 說明直營通路價格優化工作已完成（原話："our price optimization work is now complete"）
- 2026-08-04｜CFO Christian Luiga｜margin：CFO 拆解 Premium 營收成長中的 ARPU 貢獻（原話："ARPU expansion of 7.4% year-over-year"）
- 2026-08-04｜CFO Christian Luiga｜customer：CFO 報告 Q2 MAU 淨增低於預測 100 萬（原話："Our net additions of 16 million were 1 million below"）
- 2026-08-04｜Co-CEO Alex Norström｜customer：共同 CEO 稱超過 1 億訂閱者每月活躍超過 20 天（原話："over 100 million of our subscribers spending more than 20"）
- 2026-08-04｜Co-CEO Alex Norström｜customer：廣告主數量成長（原話："We are now at 33,000 active"）
- 2026-08-04｜Co-CEO Alex Norström｜customer：Reserved 售票數（原話："nearly 100,000 tickets reserved through Spotify"）
- 2026-08-04｜CFO Christian Luiga｜capital_allocation：CFO 報告年初至今庫藏股買回金額（原話："we have repurchased $662 million in shares year-to-date"）
- 2026-08-04｜CFO Christian Luiga｜capital_allocation：CFO 表示即使有併購仍預期回饋股東現金（原話："even with M&A, we expect that we will also return cash"）
- 2026-08-04｜CFO Christian Luiga｜capital_allocation：CFO 報告現金部位（原話："EUR 9.4 billion in cash and cash equivalents"）
- 2026-08-04｜CFO Christian Luiga｜commitment：CFO 表示 2026 年員工人數持平（原話："In 2026, we continue to be flat on the number of employees."）
- 2026-08-04｜Co-CEO Gustav Söderström｜commitment：共同 CEO 稱 Q4 成本趨緩（原話："we are sticking to our cost moderating in Q4"）
- 2026-08-04｜Co-CEO Gustav Söderström｜commitment：共同 CEO 稱過去三年人數未增加（原話："we have not increased head count"）
- 2026-08-04｜Co-CEO Gustav Söderström｜commitment：共同 CEO 表示 AI 成本面也要贏（原話："beneficiary means winning on the cost side, too"）
- 2026-08-04｜Co-CEO Alex Norström｜risk：共同 CEO 承認新興市場調整將反映在 Q3 MAU（原話："Yes, this will show itself in our Q3 MAU"）
- 2026-08-04｜Co-CEO Alex Norström｜risk：共同 CEO 稱新興市場在免費版增加摩擦以推動轉換（原話："carefully increases friction in our free service"）
- 2026-08-04｜Co-CEO Alex Norström｜risk：共同 CEO 稱開始拉動變現槓桿（原話："Now here, we're starting to pull the monetization lever"）
- 2026-08-04｜Co-CEO Alex Norström｜commitment：共同 CEO 稱新興市場調整不影響近期訂閱成長（原話："this will not affect subs"）
- 2026-08-04｜Co-CEO Alex Norström｜commitment：共同 CEO 稱新興市場調整不以訂閱成長為代價（原話："expect it to come at the expense of our subscriber growth"）
- 2026-08-04｜Co-CEO Alex Norström｜product：Prompted Playlists 使用規模（原話："Around 14 million of the"）
- 2026-08-04｜Co-CEO Alex Norström｜product：Audiobooks+ 年化經常性收入（原話："has passed $100 million in annual recurring revenue"）
- 2026-08-04｜Co-CEO Alex Norström｜product：Audiobooks+ 規模自上次揭露翻倍（原話："that has now doubled, which is great"）
- 2026-08-04｜Co-CEO Alex Norström｜product：Reserved 的變現方式目前是提高 Premium 性價比（原話："currently about increasing the value to price ratio"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：Taste Model 驅動的 Autoplay 讓活躍天數上升（原話："active days have increased which is very hard to do"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：Chirp 將對外提供給其他公司（原話："that we will also offer to"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：Large Taste Model 以開源模型為基礎（原話："the Large Taste model is based on open source."）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：Merlin 授權協議納入翻唱與混音（原話："30,000 labels in Merlin's network"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：混音產品需要時間才能成為重大營收來源（原話："it will take time to scale into a material revenue"）
- 2026-08-04｜Co-CEO Gustav Söderström｜product：混音產品將先以研究預覽推出（原話："you should expect to see a research preview"）
- 2026-08-04｜Co-CEO Gustav Söderström｜competition：共同 CEO 稱不需與所有大廠達成協議才推出 AI 音樂服務（原話："we do not need a deal with all the majors"）
- 2026-08-04｜Co-CEO Gustav Söderström｜competition：共同 CEO 談 AI 生成音樂與自家混音產品的差異（原話："Normal generative music will happen with or without us."）
- 2026-08-04｜Co-CEO Alex Norström｜competition：共同 CEO 稱不評論 Apple Music 漲價（原話："We don't comment on other companies' price increases."）
- 2026-08-04｜Co-CEO Alex Norström｜competition：共同 CEO 稱目前樂於當品類價格領導者（原話："we're happy to be the price leader in our category"）
- 2026-08-04｜Co-CEO Alex Norström｜competition：共同 CEO 談長期滲透率（原話："it's not impossible that we'll get to 15% penetration"）
- 2026-08-04｜Co-CEO Alex Norström｜guidance：共同 CEO 稱不評論上線時程（原話："We don't comment on timing for launches"）

### SPOT_Analyst_Investor_Day_Spotify_Technology_S_A_20260521.md
- 2026-05-21｜Alex Norström｜guidance：2030 目標：營收中段兩位數 CAGR、毛利率 35–40%、營業利益率 20% 以上（原話："a mid-teens revenue CAGR, a gross margin of 35% to 40%"）
- 2026-05-21｜Alex Norström｜commitment：重申長期北極星目標（10 億訂閱、1000 億美元營收、毛利率 40% 以上）（原話："we also remain committed to our North Stars, 1 billion"）
- 2026-05-21｜Katie English｜guidance：廣告業務預期 2026 下半年成長加速，之後維持兩位數成長（原話："we expect higher growth in the second half of 2026."）
- 2026-05-21｜Christian Luiga｜guidance：CFO：廣告回到兩位數成長，2026 下半年開始爬升（原話："reaccelerate growth into the double-digit range."）
- 2026-05-21｜Christian Luiga｜margin：CFO：高端以音樂在行銷平台與加購支撐下仍有毛利空間（原話："music has further room to run, supported by marketplace"）
- 2026-05-21｜Christian Luiga｜guidance：2026 Q2、Q3 費用成長墊高，Q4 與 2027 趨緩（原話："quarter 3 before moderating into quarter 4 and 2027."）
- 2026-05-21｜Christian Luiga｜guidance：費用暫時增加約 2 億歐元，用於行銷與研發（原話："EUR 200 million on marketing and R&D."）
- 2026-05-21｜Christian Luiga｜margin：Podcast 毛利率 2026 預期超過 20%，長期路徑 40%（原話："to what we believe will be more than 20% in 2026."）
- 2026-05-21｜Roman Wasenmüller｜margin：Podcast 長期毛利率路徑 40%（原話："we see a path to 40% margins in the long term."）
- 2026-05-21｜Christian Luiga｜guidance：2030 營業利益率至少 20%（原話："All of this points to an operating margin of at least 20%,"）
- 2026-05-21｜Christian Luiga｜margin：廣告業務在重建廣告技術期間仍有 10% CAGR（原話："Our advertising business grew at a 10% CAGR"）
- 2026-05-21｜Christian Luiga｜margin：營運費用 2022 年以來大致持平，因通膨上升被人力縮減抵銷（原話："Operating expense growth has remained essentially flat"）
- 2026-05-21｜Christian Luiga｜margin：全職人力減少 23%（原話："reduction in full-time headcount."）
- 2026-05-21｜Christian Luiga｜guidance：正常化帳面稅率約 22%，2027 年成為完整納稅人（原話："foresee that we will become a full taxpayer by 2027"）
- 2026-05-21｜Christian Luiga｜commitment：每股自由現金流納入未來記分板（原話："will be part of our scorecard going forward."）
- 2026-05-21｜Christian Luiga｜capital_allocation：現金與短期投資 88 億歐元（原話："balance of EUR 8.8 billion today."）
- 2026-05-21｜Christian Luiga｜capital_allocation：CFO：資本不是限制（原話："Simply put, capital is not a constraint."）
- 2026-05-21｜Christian Luiga｜capital_allocation：資本配置偏好自建優先（原話："Our bias remains towards build"）
- 2026-05-21｜Christian Luiga｜capital_allocation：除了抵銷稀釋的回購外，另將返還超額現金（原話："This will be over and above the anti-dilution baseline."）
- 2026-05-21｜Christian Luiga｜capital_allocation：AI 研發支出分為兩塊（大型品味模型前期集中、開發者 AI 工具持續性）（原話："Our AI R&D spend has 2 pieces."）
- 2026-05-21｜Owen Smith｜guidance：Audiobooks+ 預計今年 7 月達年化經常性營收 1 億美元（原話："recurring revenue from Audiobooks Plus only this July."）
- 2026-05-21｜Owen Smith｜commitment：今夏擴充 Audiobooks+ 加購層級（原話："we're expanding Audiobooks+ with new add-on tiers"）
- 2026-05-21｜Roman Wasenmüller｜commitment：今夏推出 podcast 創作者會員制（原話："we're taking the next step by introducing memberships."）
- 2026-05-21｜Maya Prohovnik｜product：所有 Premium 用戶每月有生成個人 podcast 的額度，重度用戶可加購（原話："a monthly allocation of credits to generate podcast"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：巴西 2026 營收成長預期超過 30%（原話："revenue is going to grow with more than"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：印度新高階方案 Premium Platinum 定價約標準版 2 倍（原話："Premium Platinum, priced at just over 2x the cost of our"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：印度訂閱戶已有逾 7% 選高階層（原話："more than 7% of our subscribers are already on this higher"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：美國 Premium 市佔六年增加 8–10 個百分點（原話："grown our U.S. premium market share by 8 to 10"）
- 2026-05-21｜Gustav Gyllenhammar｜customer：全球付費轉換率多年維持約 40%（原話："has actually stayed around 40% for many years"）
- 2026-05-21｜Christian Luiga｜customer：美國客戶終身價值 2022 年以來增加逾 70%（原話："LTV has increased by more than 70% since 2022."）
- 2026-05-21｜Gustav Gyllenhammar｜customer：管理層稱免費用戶成長加速，朝 2030 前 10 億用戶（原話："we are on the right path to reach 1 billion users before"）
- 2026-05-21｜Gustav Söderström｜margin：UMG 授權的加購：預期毛利至少持平到增加（原話："this to be at least margin neutral to accretive for us."）
- 2026-05-21｜Charlie Hellman｜product：與 UMG 簽署授權，讓粉絲合法製作翻唱與混音，作為付費加購（原話："landmark licensing agreements with Universal Music Group"）
- 2026-05-21｜Charlie Hellman｜risk：AI 生成內容湧入，權利人失控風險（管理層稱像狂野西部）（原話："things are starting to feel like the Wild West."）
- 2026-05-21｜Rene（未標示姓氏）｜product：Reserved：Live Nation 為首發夥伴，多年合約（原話："Reserved arrives with Live Nation as our launch"）
- 2026-05-21｜Gustav Söderström｜product：管理層稱 AI 是順風而非逆風（原話："Guess what? It's a tailwind."）
- 2026-05-21｜Gustav Söderström｜competition：Spotify 選擇向公開市場購買通用 LLM，自訓大型品味模型（原話："buying this capability on the open market"）
- 2026-05-21｜Gustav Söderström｜competition：面對 LLM 平台：視為更多通路（ubiquity）（原話："So for us, this is just more ubiquity."）
- 2026-05-21｜Gustav Söderström｜competition：管理層對自身差異化優勢感到安心（個人化資料）（原話："we feel quite comfortable about the unique advantages"）
- 2026-05-21｜Gustav Söderström｜product：AI 不只是成本層，也是產品與變現層（原話："It's a product and monetization layer."）
- 2026-05-21｜Niklas Gustavsson｜product：程式碼貢獻逾 73% 由 AI 輔助（原話："73% of our code contributions are AI-assisted"）
- 2026-05-21｜Gustav Gyllenhammar｜guidance：定價仍是工具箱中的工具，預期持續調價（原話："pricing will continue to be a tool in our toolbox."）
- 2026-05-21｜Alex Norström｜customer：調價後流失率極低，管理層自己也意外（原話："Even us, we were surprised that the churn was so minimal."）
- 2026-05-21｜Katie English｜competition：廣告主動廣告商 Q1 年增 68%（原話："active advertisers grew 68% year-over-year in Q1"）
- 2026-05-21｜Katie English｜product：競價式廣告渠道已占廣告業務逾三分之一（原話："biddable channels have grown to more than 1/3 of our Ads"）
- 2026-05-21｜Katie English｜risk：承認廣告轉型太慢（原話："took us too long to make the shift."）
- 2026-05-21｜Katie English｜risk：過去廣告過度集中於音訊預算（原話："too centered on audio-only budgets"）
- 2026-05-21｜Katie English｜commitment：廣告平台重建工作已結束（原話："The heavy platform rebuild is now behind us."）

### 問答異常語氣（迴避／改口／保留）
- SPOT_Q2_2026_Earnings_Call_20260804.md｜問：Doug Anmuth 追問新產品加價方案上線時程與對 Premium ARPU 下半年與 2027 年的影響｜答法：共同 CEO 說不評論時程、不給 ARPU 指引，改談 Audiobooks+ 翻倍與加價結構
- SPOT_Q2_2026_Earnings_Call_20260804.md｜問：Jason Bazinet 追問唱片公司稱產業 Q2 付費成長放緩，對長期訂閱成長有多大信心｜答法：共同 CEO 答非常有信心，但表示不給長期指引，未回應產業放緩的數據
- SPOT_Q2_2026_Earnings_Call_20260804.md｜問：Jason Helfstein 追問 Apple Music 漲價的啟示與 Spotify 未來漲價想法｜答法：共同 CEO 稱不評論其他公司漲價，未說明自家漲價計畫
- SPOT_Analyst_Investor_Day_Spotify_Technology_S_A_20260521.md｜問：Wells Fargo Steve Cahall 問 UMG 加購的定價、對毛利率的影響、是否全球推出、其他大廠跟進｜答法：Alex 明說不談具體細節；Gustav 只給「至少毛利持平到增加」，未回答定價與推出範圍
- SPOT_Analyst_Investor_Day_Spotify_Technology_S_A_20260521.md｜問：Guggenheim Michael Morris 問去年免費層改版後轉換到 Premium 的進展｜答法：Alex 以 MAU 超預期與互動天數回答，未給轉換率數字；Gustav 談互動與付費相關性
- SPOT_Analyst_Investor_Day_Spotify_Technology_S_A_20260521.md｜問：BofA Jessica Reif Cohen 問各加購層定價、是否有多層超級 Premium，以及日均使用時數｜答法：未給任何定價，講價值對價格比與「多個加購、依意願定價」；日均使用時數完全未回答

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
{"date":"20260711","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"成熟市場（NA/歐洲）Premium 飽和為「成熟非結構崩壞」，新興市場量 + ARPU 二曲線接棒總訂戶淨增","columns":{"2Y 驗證點":"Q2 26 NA Premium 回穩、Q2 總訂戶 299M guide 兌現","5Y 驗證點":"總 Premium 訂戶維持 +8-10%/yr CAGR，新興市場佔淨增 &gt;60%","10Y 驗證點":"Premium 訂戶向 5-6 億邁進（全球逼近 10 億付費）","數字門檻":"總 Premium ≥ +8%/yr；NA 訂戶不連 2 季負","來源":"Q1 26 newsroom；MBW；Music Ally","漂移觸發":"NA（或歐洲）Premium 連 2 季 YoY 負 → 削弱"}},{"id":"H2","text":"毛利率守 33% 且 OM 全年擴張，ARPU 二曲線（podcast/audiobook/super-premium/AI，較音樂高毛利）改善 mix","columns":{"2Y 驗證點":"FY26 GM &gt;33%、OM YoY 擴張（Q2 guide OM 33.1%*）","5Y 驗證點":"GM 向 35% 靠、OM 向高十幾%（規模槓桿）","10Y 驗證點":"OM 進入 20%+ 區間（成熟平台）","數字門檻":"季 GM ≥ 32.8%；FY26 OM YoY 正","來源":"Q1 26 shareholder letter；investing.com","漂移觸發":"連 2 季 GM &lt; 32.8% 或 labels royalty 再 +1pp → 削弱"}},{"id":"H3","text":"估值從 26x Fwd PE（5Y ~30 分位）向合理 26-30x 修復/守穩，報酬由 EPS 複利驅動（非 re-rate 依賴）","columns":{"2Y 驗證點":"FY27 EPS 共識 ≥ $18 守穩、Fwd PE 不破 20x","5Y 驗證點":"EPS 由 FY26 $14.7 → FY28 $22.4（~23% CAGR）兌現","10Y 驗證點":"成熟期 PE 收斂 22-26x、EPS 持續複利","數字門檻":"Fwd PE ≥ 20x；FY27 EPS 共識不連 2 季下修","來源":"Excel snapshot 2026-06-23；stockanalysis","漂移觸發":"FY1/FY2 EPS 共識連 2 季下修 &gt;5% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"成熟市場（NA→歐洲）Premium 結構性飽和蔓延（vs Apple/YouTube Music + subscription fatigue）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"NA/歐洲 Premium 訂戶 YoY","警戒閾值":"NA 連 2 季 YoY 負 → H1 失敗"}},{"id":"R2","text":"labels（UMG/Sony/Warner）供給端議價權持續回收，mechanical royalty 再上調封頂毛利","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 GM、labels 合約重議公告","警戒閾值":"連 2 季 GM &lt; 32.8% 或任一 label royalty +1pp"}},{"id":"R3","text":"EU DMA / Apple App Store 佣金與導流規則（雙向，偏正面）","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"DMA 執行進展、Apple 佣金/CTF 調整","警戒閾值":"7/8 EU 法院已裁 Apple 敗訴、確認 gatekeeper → 對 SPOT 通路成本正面緩衝；若反轉則 −ve"}},{"id":"R4","text":"AI 生成音樂（Suno/Udio）破壞內容經濟與訂閱必要性（critic 補入；賣方砍價明示理由）","columns":{"對應假設":"H1, H2","時間尺度":"🐢 長期結構（2+ 年，但近月有判決催化）","監測指標":"Sony v. Suno 判決、AI 音樂佔串流量、Viral 榜 AI 曲目","警戒閾值":"7 月判 AI 訓練屬合理使用 或 AI 音樂 &gt;10% 串流量 → 結構 reframe"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Q2 2026 NA Premium 訂戶回穩（否則連 2 季負＝結構飽和確認）＋7 月 Sony v. Suno 判決明朗；或回檔至 BB 下軌 ~$420","irr_base_pct":11.5,"ev5y_pct":62.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":4.8,"ev5y_pct":62.0,"irr_base_pct":11.5,"max_dd_pct":-58.0,"bull_5y_price":1224.0,"bear_5y_price":360.0,"p_bull_pct":25.0,"p_bear_pct":32.0,"rearm_trigger":"Q2 2026 NA Premium 訂戶回穩（否則連 2 季負＝結構飽和確認）＋7 月 Sony v. Suno 判決明朗；或回檔至 BB 下軌 ~$420","price_at_dd":479.77,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPOT_20261024/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
