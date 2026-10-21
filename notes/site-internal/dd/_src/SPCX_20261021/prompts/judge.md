你是 stock-analyst **v20 判斷 agent**，標的 SPCX（20261021）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"SPCX","date":"2026-10-21","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPCX_20261021/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPCX_20261021/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":14575,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m（YoY +161%、QoQ +86.5%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"},"note":"共識約 12.6–12.7B（二手媒體轉述 LSEG，未採一手）"},{"id":"f_kpi1_gaap","label":"GAAP 營業利益","value":2791,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m（營業利益率 19.1%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi2_ebitda_non_gaap_non_gaap","label":"調整後 EBITDA（公司揭露之 non-GAAP 利潤指標，無 non-GAAP 營業利益）","value":8809,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m（占營收 60.4%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi3","label":"淨利","value":4404,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m（稀釋 EPS $0.35）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi4_pp_e","label":"資本支出（PP&E 購置）","value":19593,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m（SI 16,444／Connectivity 1,543／Space 1,606）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi8_starlink","label":"Starlink 消費者訂戶","value":13.6,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"百萬（QoQ +1.6、YoY +6.4）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[8]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi9_starlink_arpu","label":"Starlink 消費者 ARPU","value":69,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD/月","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[9]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi10_nameplate_compute","label":"名牌算力 nameplate compute","value":1.7,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"GW","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[10]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi11_si","label":"SI 分部營收／營業利益","value":7560,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m；營業利益 431（含收購相關 SBC 1,217）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[11]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi12_connectivity","label":"Connectivity 分部營收／營業利益","value":5248,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m（YoY +69%）；營業利益 2,367","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[12]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-20","period":"2026-10-20","unit":"date","basis":"距今 1 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-20"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_spcx_gross_margin_pct","label":"SPCX 毛利率","value":50.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPCX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_spcx_operating_margin_pct","label":"SPCX 營業利益率","value":-13.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPCX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_spcx_fcf_margin_pct","label":"SPCX FCF 利潤率","value":-157.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPCX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rklb_gross_margin_pct","label":"RKLB 毛利率","value":37.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RKLB.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rklb_operating_margin_pct","label":"RKLB 營業利益率","value":-29.06,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RKLB.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_rklb_fcf_margin_pct","label":"RKLB FCF 利潤率","value":-48.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RKLB.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asts_gross_margin_pct","label":"ASTS 毛利率","value":39.17,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASTS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asts_operating_margin_pct","label":"ASTS 營業利益率","value":-410.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASTS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_asts_fcf_margin_pct","label":"ASTS FCF 利潤率","value":-1506.12,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASTS.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pl_gross_margin_pct","label":"PL 毛利率","value":55.42,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PL.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_pl_operating_margin_pct","label":"PL 營業利益率","value":-27.16,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PL.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_pl_fcf_margin_pct","label":"PL FCF 利潤率","value":4.96,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PL.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_irdm_gross_margin_pct","label":"IRDM 毛利率","value":71.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IRDM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_irdm_operating_margin_pct","label":"IRDM 營業利益率","value":23.76,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IRDM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_irdm_fcf_margin_pct","label":"IRDM FCF 利潤率","value":32.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IRDM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi5","label":"營業現金流（前九個月累計；本稿未揭露單季）","value":13097,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi6_13_097_pp_e_48_069","label":"自由現金流（前九個月累計，= 營業現金流 13,097 − PP&E 購置 48,069，本表自算）","value":-34972,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}},{"id":"f_kpi7_sbc","label":"SBC（含收購相關）","value":2363,"period":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","unit":"USD m（占營收 16.2%；占 GAAP 營業利益 84.7%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[7]","as_of":"Q3 2026（季末 2026-09-30，公告於 2026-10-20）","citation":"公司 8-K Ex-99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/1181412/000162828026066482/spaceexplorationtechnologi.htm（IR：ir.spacex.com）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":147.79,"period":"2026-10-20（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-8.07,"period":"2026-10-20（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":45.84,"period":"2026-10-20（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-164.29,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（0.14 → -0.09）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":10.92,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（1.74 → 1.93）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":11.17,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（4.03 → 4.48）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":-0.09,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":1.93,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":4.48,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-145.0,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 0.2 → -0.09（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_ps_current","label":"P/S（現值）","value":84.54,"period":"2026-10-20（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝1.7","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-20（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":1.7,"period":"2026-10-20（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":81.92,"period":"2026-10-20（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-20（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-10-20（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-20（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":1135.43,"period":"2026-09-26","unit":"x","basis":"分母＝FY1 EPS 0.14，分子＝快照價 158.96","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-26"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-60301.0,"period":"2026-10-21","unit":"USD m","basis":"yfinance 最新一季：總債務 39708.0、現金 100009.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-21"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":13181.78,"period":"2026-10-21","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-21"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":1887834.19,"period":"2026-10-21","unit":"USD m","basis":"市值 1948135.19 ＋ 淨負債 -60301.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-21"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":45329.43,"period":"2026-10-21","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（24 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-21"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":117480.72,"period":"2026-10-21","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（25 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-21"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":41.65,"period":"2026-10-21","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-21"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"-","period":"2026-10-21","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-21","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 147.79 / W52 None / W104 None / W250 None / W250 13週斜率 None%"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"SpaceX 2025 年 Falcon 9 發射 165 次；Blue Origin、Relativity、Stoke、Firefly 都在擴產能，但業界認為有意義的替代方案仍需數年","source":"The Motley Fool, spacex competitors","url":"https://www.fool.com/investing/how-to-invest/stocks/spacex-competitors/","excerpt":"Competitors like Rocket Lab and Blue Origin offer viable alternatives in the commercial space market. Loading paragraph... Loading company_card... Loading paragraph...","as_of":"2026-06-26","retrieved_at":"20261021","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Rocket Lab Neutron（約 13 噸 LEO、對標 Falcon 9）首飛由 2026 年中延至 Q4 2026","source":"fourweekmba, Blue Origin vs Rocket Lab","url":"https://fourweekmba.com/blue-origin-vs-rocket-lab/","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261021","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Space Force added Impulse Space and Relativity Federal to the national-security launch provider pool competing alongside SpaceX, Blue Origin and others (pool of seven in Phase 3 Lane 1)","source":"Defense One / Air & Space Forces Magazine, Space Force Adds 2 New Launch Providers","url":"https://www.defenseone.com/business/2026/07/space-force-adds-two-startups-militarys-growing-list-national-security-launch-providers/414685","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261021","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Bloomberg Government: Pentagon accounted for nearly 43% of SpaceX contracting dollars FY2023-2025; NASA and DoD are main buyers","source":"Bloomberg Government, Starlink, Satellite Launches Drive SpaceX's Sales to US Agencies","url":"https://news.bgov.com/bloomberg-government-news/starlink-satellite-sales-drive-spacex-sales-to-federal-agencies","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261021","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#2","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Space Force adds two launch providers (Impulse Space, Relativity Federal)","source":"Air & Space Forces Magazine","url":"https://www.airandspaceforces.com/space-force-two-new-launch-providers/","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261021","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"SEC 申報檔集中度附註：單一重大客戶「Customer A」占 2025 年營收約 20.9%（2024：24.2%、2023：25.2%），營收橫跨三個分部；無其他客戶超過 10%。申報檔未具名；Yahoo Finance 文章解讀為美國政府。","source":"SEC Form FWP 摘錄（經搜尋摘要）；Yahoo Finance『One Number From SpaceX's Pre-IPO Disclosures…』","url":"https://finance.yahoo.com/economy/policy/articles/one-number-spacex-pre-ipo-112835397.html","excerpt":"Customer A .... 20.9 % 24.2 % 25.2 % Revenue from this customer relates to all three segments. No other customers represented more than 10% of consolidated revenue during the years ended December 31, 2025, 2024 and 2023.","as_of":"2026-06-01","retrieved_at":"20261021","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"2026 年 6 月三大評等機構給予投資等級：Moody's Baa1、Fitch BBB+、S&P BBB，展望皆穩定；S&P 預期自由現金流為負至 2029 年，需更多債務與股權融資。","source":"Euronews / Treasury & Risk（經搜尋摘要）","url":"https://www.euronews.com/business/2026/06/19/spacex-lands-investment-grade-credit-ratings-as-shares-tumble-from-record-high","excerpt":null,"as_of":"2026-06-19","retrieved_at":"20261021","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"SEC 申報檔：Customer A 占 2025 年營收 20.9%","source":"SEC Form FWP","url":"https://www.sec.gov/Archives/edgar/data/0001181412/000162828026041365/eu_interviewtranscript06.htm","excerpt":"from a significant customer is as follows: Year Ended December 31, 2025 2024 2023 Customer A .................................................................................... 20.9 % 24.2 % 25.2 % Revenue from this customer relates to all three segments. No other customers represented more than 10% of consolidated revenue during the years ended December 31, 2025, 2024 and 2023.","as_of":"2026-06-01","retrieved_at":"20261021","affects":["decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"A&D 採購分析認為需求為結構性：民航積壓訂單超過十年、國防積壓 7,470 億美元；FY2026 國防預算 9,616 億美元（+13.4%）；FY2027 1.5 兆美元僅為提案、未通過。","source":"Unite 'aerospace defence indirect procurement 2026'（引 PwC 2025）","url":"https://unite.eu/en-gb/resources/stories-and-insights/aerospace-defence-indirect-procurement-2026","excerpt":"The demand signal is structural, not cyclical. Commercial backlogs now stretch beyond a decade.","as_of":"2026-01-01","retrieved_at":"20261021","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"PwC/AIA 調查：需求升至現有 1.25 倍時 85% 受訪者稱 18 個月內可交付，升至 2 倍降為 47%；Bain 分析 15 個國防計畫，87% 公司認為供應鏈問題比勞力、工程、設備更具影響。","source":"PwC State of the Ramp；Bain 'Aerospace and Defense: Winning the Race to Scale'","url":"https://www.bain.com/insights/aerospace-and-defense-winning-the-race-to-scale/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261021","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"KGI 2026-07 研究報告：SPCX 分 Space／Connectivity／AI 三個部門，Starlink 目前是唯一 EBIT 為正的現金來源；Starship 商業發射預計 2H26，2025 年 165 次發射，預估 2031 年 1,500 次。","source":"KGI HK 'SpaceX' 2026-07-13","url":"https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/hk-quarterly/2026-07-13-spacex.pdf","excerpt":null,"as_of":"2026-07-13","retrieved_at":"20261021","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"PwC/AIA 產能爬坡調查：1.25 倍需求 85% 可於 18 個月內交付，2 倍 47%","source":"PwC State of the Ramp","url":"https://www.pwc.com/us/en/industries/industrial-products/library/assets/pwc-state-of-the-ramp.pdf","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261021","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"澳洲 ACCC 將審查 SpaceX 全資收購 Anysphere（Cursor）的提案；屬併購審查，非壟斷調查。","source":"MLex (2026-07-01 item)","url":"https://www.mlex.com/mlex/articles/2495897","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261021","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"2025-12 華倫參議員與卡薩眾議員致函 DOJ 反壟斷部與 FCC，要求嚴查 AT&T 與 SpaceX 向 EchoStar 購買頻譜；未查到正式 DOJ 行動。","source":"Sen. Warren office, letter dated 2025-12-18","url":"https://www.warren.senate.gov/?p=26998","excerpt":null,"as_of":"2025-12-18","retrieved_at":"20261021","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"MLex 2026-08-28：SpaceX 促請 FCC 在審查 Rocket Lab 相關交易時檢視 Iridium 對競爭衛星業者的行為；SpaceX 不反對該交易。","source":"MLex (2026-08-28 item)","url":"https://www.mlex.com/mlex/articles/2519102","excerpt":null,"as_of":"2026-08-28","retrieved_at":"20261021","affects":["moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"2026-01 FCC 核准 SpaceX 再發射 7,500 顆 Starlink Gen2 衛星，Gen2 總授權達 15,000 顆；核准附帶遵守該程序日後規則的條件。","source":"搜尋摘要所述 FCC 核准（2026-01）","url":null,"excerpt":null,"as_of":"2026-01-15","retrieved_at":"20261021","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"SpaceX 曾向美國貿易代表署請求豁免兩項中國製工廠設備（工業焊錫系統、電路板印刷機，用於 Starlink 終端製造）的關稅，稱暫無國內替代品（2025 年事件，非 2026 新增）","source":"Deccan Herald / Reuters: Elon Musk's SpaceX pleads with Trump for tariff exemptions","url":"https://www.deccanherald.com/amp/story/world%2Felon-musks-spacex-pleads-with-trump-for-tariff-exemptions-3471960","excerpt":"The company told the agency it had no domestic alternative for now","as_of":"2025-04-01","retrieved_at":"20261021","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"Expeditors 頁面稱 2026-07-09 公告結束 Section 232 航太調查、未加徵額外關稅（摘要被截斷，細節未證實）","source":"Expeditors: Section 232 Aerospace Investigation Results in No Tariffs","url":"https://info.expeditors.com/newsflash/topic/aerospace","excerpt":"Section 232 Aerospace Investigation Results in No Tariffs","as_of":"2026-07-09","retrieved_at":"20261021","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"路透報導：SpaceX 要求台灣供應商將生產移出台灣（越南、泰國），理由為地緣政治考量","source":"Business Standard (Reuters)","url":"https://www.business-standard.com/world-news/after-spacex-s-requests-taiwanese-suppliers-move-manufacturing-abroad-124110500431_1.html","excerpt":"company requested they move their manufacturing from Taiwan to Thailand for new orders \"mostly due to geopolitical considerations\". It did not elaborate. The sources declined to be identified because the information was not public. SpaceX did not reply to requests for comment. Also Read Foxconn subsidiary seeks $80 mn Vietnam investment for integrated circuits","as_of":"2024-11-05","retrieved_at":"20261021","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Deloitte：關鍵礦物與稀土為航太國防供應鏈戰略咽喉，引擎、鑄鍛件、鈦為產能瓶頸","source":"Deloitte midyear update aerospace and defense industry outlook","url":"https://www.deloitte.com/us/en/insights/industry/aerospace-defense/midyear-update-aerospace-and-defense-industry-outlook.html","excerpt":"Critical minerals and rare earths have become a strategic chokepoint for the industry. These are essential for critical defense products and capabilities such as advanced aircraft, munitions, naval systems, satellites, and secure communications. However, the sector continues to rely on foreign-controlled supply chains, leaving it exposed to geopolitical disruptions.7 Engines, electronics, castings","as_of":"2026-08-02","retrieved_at":"20261021","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q2 2026 營收 $7.8B（年增 92%）；Connectivity（Starlink）$4.3B 年增 66%，ARPU $66/月，與上季持平、前一年同期為 $85；Space（發射）$962M 年增 29%；AI $2.6B 年增 247%","source":"Nasdaq, SpaceX Q2 Earnings Call Highlights（搜尋摘要）","url":"https://www.nasdaq.com/articles/spacex-q2-earnings-call-highlights","excerpt":null,"as_of":"2026-08-04","retrieved_at":"20261021","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Falcon 9 公開牌價由 $61.2M 逐步漲至 2024 年 $69.75M，2026 年初約 $74M；對手 Vulcan、Ariane 6 牌價約 $110M；2026 年市佔數據未找到","source":"Nasdaq／AOL, SpaceX Will Be Even More Profitable After Its 2026 IPO（觀點文，搜尋摘要）","url":"https://www.aol.com/articles/spacex-even-more-profitable-2026-092500153.html","excerpt":null,"as_of":"2026-02-15","retrieved_at":"20261021","affects":["moat_trend","valuation"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"全球太空經濟 2026 年約 $462B–$468B，長期 CAGR 約 7%–8.7%（Business Research Company、Global Market Insights）；GlobalData（2025/05）預測僅 4.0% CAGR","source":"Business Research Company／Global Market Insights／GlobalData（搜尋摘要）","url":"https://www.gminsights.com/industry-analysis/space-economy-market","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261021","affects":["thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Amazon Leo(Kuiper)星座為 Starlink 主要點名的競爭者，已發射約 300 顆衛星、尚未提供商用服務（二手摘要，未核原文）","source":"Nasdaq: SpaceX IPO warning: Amazon poses real threat","url":"https://nasdaq.com/articles/spacex-ipo-warning-amazon-poses-real-threat","excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261021","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Rocket Lab Neutron 定位直接對標 Falcon 9，預估單次約 5000 萬美元對 SpaceX 約 6700 萬；運載力 13 噸低軌對 Falcon 9 約 23 噸（二手摘要，未核原文，日期為估計）","source":"Aerospace America (AIAA): Rocket Lab's next step","url":"https://aerospaceamerica.aiaa.org/features/rocket-labs-next-step/","excerpt":null,"as_of":"2025-01-01","retrieved_at":"20261021","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Blue Origin New Glenn 為可重複使用重型火箭（低軌 45 噸），客戶含 Amazon、NSSL Phase 3 合約 24 億美元（二手摘要，未核原文，日期為估計）","source":"Blue Origin vs Rocket Lab (fourweekmba)","url":"https://fourweekmba.com/blue-origin-vs-rocket-lab/","excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261021","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"SpaceX 於 Q2 財報電話會議稱將把 Starlink 星座定位為完整行動電信業者（直接面對 Verizon、AT&T、T-Mobile），並已購入 EchoStar 頻譜，由批發漫遊轉向自有頻譜平台","source":"SatNews: SpaceX reports strong Q2 results and details direct mobile telco strategy","url":"https://satnews.com/2026/08/05/spacex-reports-strong-q2-results-and-details-direct-mobile-telco-strategy/","excerpt":"Shotwell stated that SpaceX is positioning its Starlink satellite constellation to operate as a full-fledged mobile telecommunications carrier. The strategy targets market share among the primary U.S. wireless carriers—Verizon, AT&T, and T-Mobile—a group that generates approximately $600 billion (€520 billion) in annual revenue.","as_of":"2026-08-05","retrieved_at":"20261021","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"SpaceX 自 2026-06 起不再透過通訊社發布財報，改在投資人關係網站與 X 帳號發布；另報導 2026-05 Starlink 方案漲價最多 $10/月","source":"BYDFi: SpaceX drops wire services for earnings disclosures","url":"https://www.bydfi.com/en/crypto-news/spacex-drops-wire-services-for-earnings-disclosures-14742","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261021","affects":["triggers"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026 營收 $7.8B（年增 91.9%），高於 Visible Alpha 共識 14.6%；公司未給正式 Q3/FY2026 guidance，僅重申年底 $100B 年化營收 run-rate 目標。","source":"S&P Global Market Intelligence, Research — August 14, 2026","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/08/spacex-postq-ai-growth-drives-earnings-beat-as-capex-expectations-surge","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261021","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"財報後 Visible Alpha 共識：Q3 營收預期 $13B（較財報前高 4.8%），FY2026 營收預期上修 14.3% 至 $45.9B，FY2026 毛利預期上修 16.3%。","source":"S&P Global Market Intelligence, Research — August 14, 2026","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/08/spacex-postq-ai-growth-drives-earnings-beat-as-capex-expectations-surge","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261021","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"MarketBeat：42 位分析師共識「Moderate Buy」（27 Buy／8 Hold／7 Sell），平均目標價 $221.20，區間 $75–$800。","source":"MarketBeat SPCX forecast","url":"https://www.marketbeat.com/stocks/NASDAQ/SPCX/forecast/","excerpt":null,"as_of":"2026-09-04","retrieved_at":"20261021","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"StockHub 報導共識目標價由 $225 降至 $202（-10%）；評級 Strong Buy 12／Buy 20／Hold 7／Sell 1。","source":"StockHub news_49e56b7b56b9","url":"https://stockhub.kr/en/news/news_49e56b7b56b9","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261021","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"GLJ Research 的 Gordon Johnson 指 SPCX Q2 自由現金流燒掉 $15.95B，銷售倍數約 77 倍（個別分析師看法，非共識）。","source":"WebSearch result summarizing Walnut/TradersUnion/StockHub items (SPCX sell-side revision query)","url":"https://tradersunion.com/news/market-voices/show/2900494-spcx-afterhours-drop-loss/","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261021","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-16 簽署併購 Anysphere（Cursor）合併協議，隱含股權價值 600 億美元，以 Class A 普通股支付；原預期 2026 年第三季完成。","source":"SEC EDGAR 8-K Item 1.01（2026-06-16）","url":"https://www.sec.gov/Archives/edgar/data/1181412/000162828026043411/spaceexplorationtechnologi.htm","excerpt":"Space Exploration Technologies Corp. (the “Company”), X67 Inc., a wholly owned subsidiary of the Company (“Merger Sub”), and Anysphere, Inc. (“Cursor”) entered into an Agreement and Plan of Merger (the “Merger Agreement”)","as_of":"2026-06-16","retrieved_at":"20261021","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"2026-08-14 Cursor 合併生效，共發行 389,289,254 股 Class A 普通股，隱含 Cursor 股權價值 600 億美元。","source":"SEC EDGAR 8-K Item 2.01（2026-08-14）","url":"https://www.sec.gov/Archives/edgar/data/1181412/000162828026056945/spcx-20260814.htm","excerpt":"on August 14, 2026 (the “Effective Time”), the Merger became effective, and (i) the shares of Cursor’s common stock and the shares of Cursor’s preferred stock outstanding immediately prior to the Effective Time were automatically converted into the right to receive an aggregate of 389,289,254 shares of the Company’s Class A common stock","as_of":"2026-08-14","retrieved_at":"20261021","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"0","claim":"2026-06-26 發行 250 億美元高級無擔保票據（2031/2033/2036/2046/2056 到期，票面 5.350%–6.650%）。","source":"SEC EDGAR 8-K Item 8.01（2026-06-26）","url":"https://www.sec.gov/Archives/edgar/data/1181412/000162828026045763/spcx-closing8xkjune2026.htm","excerpt":"the Company issued $7.0 billion aggregate principal amount of its 5.350% Senior Notes due 2031 (the “2031 Notes”), $6.0 billion aggregate principal amount of its 5.650% Senior Notes due 2033","as_of":"2026-06-26","retrieved_at":"20261021","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"公司章程要求股東爭議送德州商業法院，並以強制仲裁排除集體訴訟；未見已提起的證券集體訴訟。","source":"Bloomberg Law《SpaceX Maps Texas Strategy to Dodge Securities Class Actions》","url":"https://news.bgov.com/class-action/spacex-maps-texas-strategy-to-dodge-securities-class-actions","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261021","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_nrr_rule40_band#0","axis":"unprofitable_nrr_rule40_band","section":"coverage","direction":"0","claim":"FY2025 營收 $18.7B、年增 33.2%，調整後 EBITDA $6.6B（Hudson Labs）","source":"Hudson Labs SPCX stock analysis","url":"https://hudson-labs.com/research/spcx-stock-analysis","excerpt":"Financial Profile: FY25 revenue $18.67B (+33.2% YoY), Adjusted EBITDA $6.58B, but net loss $(4.94)B due to heavy AI investment; Q1 2026 revenue $4.69B, Adjusted EBITDA $1.13B, net loss $(4.28)B.","as_of":"2026-07-08","retrieved_at":"20261021","affects":["valuation"],"status":"ok"},{"id":"unprofitable_nrr_rule40_band#1","axis":"unprofitable_nrr_rule40_band","section":"coverage","direction":"0","claim":"Argus 表列 SpaceX 調整後 EBITDA 利潤率 35.3%，並與大型科技同業並列成長與利潤率","source":"Argus Research ActionAlert 2026-08-09","url":"https://www.argusresearch.com/assets/doc/20260809_ActionAlert.pdf","excerpt":"SpaceX had $22 billion in long-term debt, $24.7 billion in cash, and total equity of $2.5 billion as of December 31, 2025. The debt-to-total capitalization ratio was a steep 89.8%. However, the company generates healthy cash flow. The 2025 the adjusted EBITDA margin was 35.3%.","as_of":"2026-08-09","retrieved_at":"20261021","affects":["valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#0","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"2026年4–6月加權平均基本與稀釋股數同為58.64億股，上半年為48.79億股；基本與稀釋相同，潛在稀釋證券因反稀釋而排除。","source":"SpaceX 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001181412/000162828026052535/spcx-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261021","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#1","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"0","claim":"2026年Q1因xAI合併，公司向xAI現任與前任員工回購25.4百萬股、金額24.13億美元，已全數註銷。","source":"SpaceX 10-Q (period ended 2026-06-30)","url":"https://www.sec.gov/Archives/edgar/data/0001181412/000162828026052535/spcx-20260630.htm","excerpt":"During the three months ended March 31, 2026, the Company repurchased $2,413 million or 25.4 million shares of SpaceX Common Stock from eligible current and former xAI employees as part of the xAI Merger.","as_of":"2026-06-30","retrieved_at":"20261021","affects":["valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#2","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"聚合站資料：2025年SBC為19.47億美元（較2024年+148.34%）；2025年營收約186.74億美元（PitchBook），SBC約佔營收10.4%（此比率為查詢者以兩來源相除，非單一來源直接陳述）；2026Q1 SBC 6.39億美元（Macrotrends）。未核對公司申報文件。","source":"Macrotrends SPCX stock-based compensation／TickerLeague SBC expense／PitchBook","url":"https://www.macrotrends.net/stocks/charts/SPCX/spacex/stock-based-compensation","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261021","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#3","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"0","claim":"聚合站稀釋加權股數：2023年27.6億、2024年99.6億、2025年29.3億；最新一期38.8億（期間未確認）；各站股數口徑彼此不一致（13.08億／75.7億等），無法對上10-Q的48.8–58.6億。","source":"TickerLeague／AlphaQuery SPCX shares outstanding","url":"https://tickerleague.com/companies/SPCX/financials/shares-outstanding","excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261021","affects":["valuation"],"status":"ok"},{"id":"unprofitable_dilution_trajectory#4","axis":"unprofitable_dilution_trajectory","section":"coverage","direction":"-","claim":"Plus500稱全股票收購Anysphere帶來額外稀釋。","source":"Plus500 SpaceX stock price prediction","url":"https://www.plus500.com/en/forecasts/spacex-stock-price-prediction-2026-spcx-forecast","excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261021","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"unprofitable_path_to_profitability#0","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"-","claim":"搜尋摘要：未找到公司自身的 FCF 轉正時程指引；分析師估計 FCF 轉正約 2031，Morgan Stanley 預測 2035 前無 FCF 為正年度，S&P Global Ratings 預期 FCF 至 2029 年仍為負。","source":"The Motley Fool, spacex profitable 2029 billion debt stock","url":"https://www.fool.com/investing/2026/06/30/spacex-profitable-2029-billion-debt-stock/","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261021","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"unprofitable_path_to_profitability#1","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"+","claim":"S&P Global Q2 後共識：總營業利益率由今年 6.8% 升至明年 20.5%；分析師預期 Space 與 AI 部門營業利益於 FY2027 轉正；公司未提供 FY2026 正式指引，長期目標毛利率約 70%、淨利率約 45%（路演）。","source":"S&P Global Market Intelligence, SpaceX post-Q2 research","url":"https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/08/spacex-postq-ai-growth-drives-earnings-beat-as-capex-expectations-surge","excerpt":null,"as_of":"2026-08-14","retrieved_at":"20261021","affects":["thesis.H","valuation"],"status":"ok"},{"id":"unprofitable_path_to_profitability#2","axis":"unprofitable_path_to_profitability","section":"coverage","direction":"-","claim":"聚合站資料：2026Q2 FCF 約 -$15.9B（資本支出 $18.4B），Q1 約 -$9.1B；現金約 $93.5–100B、債務 $36.8B；數字來源為聚合站，需對 SEC 文件核對。","source":"VCP Scanner SPCX cash-flow / balance-sheet 等聚合站","url":"https://vcpscanner.com/stock/spcx/cash-flow","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261021","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"2026-08-14 完成以全股票收購 Cursor（Anysphere），隱含價值 600 億美元，發行 389,289,254 股 Class A。","source":"SEC EDGAR 8-K Item 2.01（2026-08-14）","url":"https://www.sec.gov/Archives/edgar/data/1181412/000162828026056945/spcx-20260814.htm","excerpt":"on August 14, 2026 (the “Effective Time”), the Merger became effective, and (i) the shares of Cursor’s common stock and the shares of Cursor’s preferred stock outstanding immediately prior to the Effective Time were automatically converted into the right to receive an aggregate of 389,289,254 shares of the Company’s Class A common stock","as_of":"2026-08-14","retrieved_at":"20261021","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"SPCX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":50.95,"operating_margin_pct":-13.63,"fcf_margin_pct":-157.52,"rd_intensity_pct":51.23},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SPCX","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"RKLB","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":37.26,"operating_margin_pct":-29.06,"fcf_margin_pct":-48.25,"rd_intensity_pct":40.62},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RKLB","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ASTS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":39.17,"operating_margin_pct":-410.26,"fcf_margin_pct":-1506.12,"rd_intensity_pct":249.67},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ASTS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"PL","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":55.42,"operating_margin_pct":-27.16,"fcf_margin_pct":4.96,"rd_intensity_pct":33.86},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PL","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"IRDM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.85,"operating_margin_pct":23.76,"fcf_margin_pct":32.61,"rd_intensity_pct":2.46},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.IRDM","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"SPCX"},"financial_history":{"ticker":"SPCX","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-12-31","revenue":10387000000.0,"revenue_yoy_pct":null,"gross_margin_pct":41.18,"operating_margin_pct":4.88,"net_income":-4628000000.0,"diluted_eps":-0.436316,"free_cash_flow":105000000.0,"fcf_margin_pct":1.01,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":14015000000.0,"revenue_yoy_pct":34.93,"gross_margin_pct":42.95,"operating_margin_pct":5.29,"net_income":791000000.0,"diluted_eps":0.00198,"free_cash_flow":-5387000000.0,"fcf_margin_pct":-38.44,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":18674000000.0,"revenue_yoy_pct":33.24,"gross_margin_pct":49.39,"operating_margin_pct":-11.05,"net_income":-4937000000.0,"diluted_eps":-0.51,"free_cash_flow":-14121000000.0,"fcf_margin_pct":-75.62,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/SPCX/SPCX_Q3_2026_Earnings_Call_20261020.md）

# Q3 2026 Earnings Call
**Space Exploration Technologies Corp.** | Earnings Calls | 2026-10-20

**Andrea Williams** (Executives):
Hello, everyone. We are coming to you live from our Starlink factory and future Starmind production site here in Bastrop, Texas. I'm Andrea Williams, Head of Investor Relations, and thank you for joining us for SpaceX's Third Quarter 2026 Earnings Presentation. 
Joining us are Elon, Gwynne, and Bret, and we are live streaming on X. Our third quarter financial results were announced just after 3:00 p.m. Texas time, and all relevant materials have been published to our Investor Relations website at ir.spacex.com. For today's presentation, our prepared remarks will be followed by a question-and-answer session. We will take live Q&A from equity analysts and then move to questions directly from our investors that were polled on our dedicated earnings Q&A platform, which the SpaceX team built with Grok. 
During this webcast, we will discuss our business outlook and make forward-looking statements. These statements are based on our predictions and expectations as of today. Actual events or results could differ materially due to a number of risks and uncertainties including those mentioned in our earnings release and the most recent filings with the SEC, including our final prospectus. During the presentation, we may discuss certain non-GAAP financial measures. In today's earnings release and our filings with the SEC, you can find additional disclosures regarding these non-GAAP measures, including all of the reconciliations with comparable GAAP measures. For the third quarter of 2026, we announced the following financial results as compared to the prior year period. revenues of $14.6 billion, up 161% from $5.6 billion; net income of $4.4 billion, an improvement of $5.5 billion from a net loss of $1.1 billion and adjusted EBITDA of $8.8 billion, up 306% from $2.2 billion.
With that, I'll hand the call over to Elon.

**Elon Musk** (Executives):
Thank you. So we are in an inflection moment for SpaceX across launch connectivity and Super Intelligence. Starting with Starship, Flight 14 was a critical milestone. Starship made it to orbit for the first time and deployed operational Starlink V3 satellites. I think we have a recap video we're going to play. 
[Presentation] 
All right. For Flight 15, which we expect to happen next month, we're going to attempt to catch both the booster and the ship. This will be the -- if we succeed, it will be the first time that an orbital launch vehicle has been fully recovered. This is a massive technology milestone. The only way that we can extend consciousness beyond Earth on a sustained basis is with a fully reusable orbital launch vehicle. So this is -- I think this is a profound technology milestone in the history of civilization consciousness. So let's look at what simulation of Flight 15 would look like if we succeed. If we don't succeed in Flight 15, we'll get there. So success is not guaranteed on these first flights, but I'd say it's more likely than not that this succeeds next flight. And if not, we have a steady stream of Starship flight attempts through the end of this year and then accelerating next year. So with that, the Flight 15 simulation. 
[Presentation]
We've also announced the development of the Louisiana spaceport. So that's going to be an incredible asset to the country and to the world that will, I think, at some point, probably have on the order of 20 or more launch towers and enable the transport of millions of tonnes per year to orbit and beyond. So that's really going to be a big deal. 
We expect Starship to fly weekly at some point in the first half next year and then second half next year, twice weekly or maybe even more frequently than that by the end of next year. The rate at which we launch Starship will increase dramatically as we solve the rapid and complete reusability. So we'll have complete reusability. Then at first, there will be a little bit of refurbishment that's needed between each flight, and we'll iron out the need for any refurbishment such that you can immediately land the rocket and launch it again just like an airplane. As I said, this is a profound technology milestone that most people in the world don't realize how important it is, but it will be obvious in hindsight. 
Starlink is also just getting started. Flight 14 deployed 26 terabits per second of Starlink bandwidth. That's equivalent to 10 Falcon 9 launches. So a single starship launch, which wasn't even fully loaded. It was about maybe half loaded, and it did the equivalent of 10 Falcon 9 launches. So what I expect over time is, not in the distant future, probably within three years is that we will have about 100x the bandwidth of the current Starlink constellation. So because we will have launched satellites with an order of magnitude more bandwidth, and we will place into orbit an order of magnitude more Starlink satellites. So probably something on the order of 100,000 satellites, each of which have more than 10x the bandwidth of the current Starlink system. 
So I think revenue for Starlink will be at least somewhat proportionate to the total bandwidth delivered. And we will also have direct-to-sell, high-bandwidth direct-to-sell capability, and we will be building out our terrestrial network. So there's broad-based connectivity anywhere that space like Starlink are allowed to operate. So anywhere in the world that we're allowed to operate. And I think the demand for bandwidth is going to be dramatically higher than it is today. I think in three to five years, there's probably a demand for 1,000x more bandwidth than there is currently because AI or SI agents will on a per agent basis, use far more bandwidth than a person, and there will be far more agents than there are people. So this ends up requiring a several order of magnitude increase in communication bandwidth in order to satisfy that communication demand.
So talking about SpaceX Super Intelligence, SpaceX SI sexy, whatever. So as I think people are starting to realize the constraint on deployment of super intelligence is more in power and cooling and infrastructure than it is in chips. So what we've done at SpaceX is we've taken a team that has been able to achieve a market share in mass to orbit that is almost 90% of all mass to orbit of earth, where China is about, I think, roughly 6% and the rest of the world combined, including the rest of the U.S. is about 4%. So a team that has been able to achieve results that are in order of magnitude greater than the rest of our -- of all competitors in space combined and applied that same team to the deployment of terrestrial compute. So this is a bit like the New York Yankees playing in Little League. It's not fair. But the net result is being able to deploy power cooling infrastructure at a rate that is vastly faster than anyone else and may, at some point, be faster than everyone else combined. So I just let that sink in for a minute. 
So I've been spending personally a lot of my time in Memphis, often four days a week, night and day, just getting the Memphis Supercompute cluster Colossus II online. We're tracking to be able to bring roughly 200,000 GB300s online per month for every month for the remainder of this year and continuing that pace next year. With next year being primarily Rubin, Vera Rubin compute. At this point, I would say -- I would say I'm fairly confident of being able to bring an incremental 10 gigawatts of compute online in 2027. That would be in addition to the roughly 3 gigawatts, maybe 2.5 to 3 gigawatts that we'll have online by the end of this year. So I put it this way. I would be surprised if we brought on less than 13 gigawatts of compute by the end of next year. 
And as I mentioned earlier, we're -- power cooling, electrical equipment infrastructure is somewhat of a limiting factor. So to make sure that, that is not a constraint for our build-out, we're actually going to aim for an incremental 20 gigawatts of power cooling and infrastructure next year. So that the amount of power and cooling that we have is far in excess of what is needed for -- to turn the GPUs on. So there's a non-zero possibility. Maybe it's a small possibility at this point, but it's not zero, of having -- of SpaceX having over 20 gigawatts of Super Intelligence compute online next year. A small possibility, but it used to be zero, it's not zero anymore. 
We're also planning to have the most powerful training cluster online by the end of Q2, which will be 440,000 Vera Rubin computers deployed for optimal training. This will, I think, be extremely helpful for getting Grok to be potentially the best model, but certainly to be extremely competitive. So on the Grok bot side, we're seeing the fastest growth of a product that I've ever seen in my life for Grok bot. I've never seen anything grow this fast. 
We're also seeing that the usage of Grok bot grows over time per user, it does not decline. So as we make Grok bot more useful, it's actually -- we're seeing users use it more per week, not use it less. And we'll be deploying Grok Bot at scale for enterprise customers, which is a very big deal, so they can be used effectively in teams by companies as though we're a virtual human. We already are in early deployment with some trusted customers, and we expect to be in wide deployment within a few weeks for enterprise customers for Grok bot. I think Grok bot may end up being what uses most of our Super Intelligence compute. 
So I mean in a nutshell, what this implies for SpaceX annual recurring revenue by the end of '27 is somewhere between $500 billion and $1 trillion.
Bret? Are you going next, sorry.

**Elon Musk** (Executives):
Sorry. I thought on that crazy note, I thought.

**Gwynne Shotwell** (Executives):
On that crazy note.

**Elon Musk** (Executives):
Yes, I don't want to give Bret a heart attack.

**Gwynne Shotwell** (Executives):
Thanks, Elon. So we had an exceptional execution and quarter again. And today, I'll focus both on the operational and the commercial highlights as well as talk about the priority initiatives for next quarter. 
Showing a slide with the KPIs, and I'll go ahead and walk through it. Starting with our Space business. We remain the leading launch provider for the world, flying the vast majority of payload mass to orbit. During the third quarter, our 35 launches included 21 flights of Starlink on Falcon 9, 2 flights of Starship, a Falcon Heavy, which I'll talk about in a second; and 12 high-profile customer missions, including the Falcon Heavy launch, which we flew NASA's Roman Space Telescope into deep space. We also flew six national security space launch missions. We've also secured important new business, winning three additional human space flight missions on Dragon, which will take us through 2028, along with the Starlink Communications contract on NASA's Artemis III mission. In addition, we signed 18 new national.
Security space launch missions, a contract to deliver payload to the lunar surface with Starship and three new Starfall missions on Starship. We just did a Starfall mission today, by the way, on Falcon 9. Starfall is our space capsule, which provides routine access -- routine relatively low-cost access to microgravity environments for scientific research, including improving our understanding of diseases like cancer and diabetes and developing better protocols for patients here on Earth.
During the final week of the quarter, we flew Starship Flight 14 to orbit, as Elon talked about, followed just after on October 1 by a triple header. We threw three Falcon missions across our three Falcon launch sites in just 13 hours. Crew-13, we brought safely to the International Space Station, a Falcon-heavy NRO mission and a rideshare mission flying 130 payloads. It's incredible display of what we can deliver in a single day across crew, commercial and national security missions. 
We're also incredibly excited for what's ahead for Starship, flying the largest payloads to help build the space economy in orbit and on other planets and the moon. As Elon said, Starship's Flight 14 was a major technical milestone, and we remain on track with our goals to bring back both the first and second stages to the tower this year, refly the second stage by early next year and ramp our launch cadence as we make progress towards rapid reusability. We'll attempt an on-orbit refueling early next year, and we'll begin flying Mobile V2 and Starmind satellites in 2027. 
We have had significant constructive engagement with the FAA, and we expect the license for our Flight 15 to include return to launch site and tower catch for both stages. I'm also extremely excited about expanding the Starship operations to Louisiana with the second Louisiana purchase. The geography of Louisiana, the community and their work ethic is so aligned for an amazing Starship future. 
Moving on to Starlink. We had another standout quarter, driven by continued growth across both our consumer, enterprise and government businesses. We ended the quarter active in 174 markets, including new market launches for Vietnam and Uganda. Looking at subscriber growth, we added 1.6 million consumers, not total users, but consumers in the quarter, reaching just under 14 million global broadband consumer subscribers. As I mentioned, this number does not include additional hundreds of thousands of enterprise subscribers and aviation customers. We remain incredibly inspired by the impact of Starlink on communities around the world, including providing service to hundreds of thousands of students and teachers in schools globally as well as for emergency response during natural disasters.
Over the third quarter, Starlink's rapid response capabilities enabled support across 25 crises, including the Venezuela earthquake, the earthquake in Western Colombia and Hurricane Lowell in Hawaii. In Venezuela alone, Starlink donated over 1,400 kits to response agencies, providing critical Starlink broadband connectivity to over 250,000 people. 
As we mentioned last quarter, we continue to see significant growth opportunities on the enterprise and government side of the business with aviation a continuing major focus and fixed site gaining momentum. Starlink is now contracted for roughly 12,000 planes, almost 1/4 of the available aircraft, and we're expanding quickly with both new and existing customers. We signed agreements with three of the four major U.S. carriers, along with a growing list of leading international airlines. During the quarter, Lufthansa, Swiss, Copa Airlines, Korean Air, Austrian Airlines and Asiana Airlines all flew their first Starlink-equipped aircraft. To keep pace with this demand, we've quadrupled aviation production rate since the beginning of the year, and we expect to double before the end of the year. 
Our aviation partners report that Starlink has become a key reason customers choose to fly with them, both business travelers who increasingly rely on full connectivity in the skies or even individuals who want to stay connected all the time everywhere. Our data shows Starlink and frankly, our customers tell us that Starlink equipped flights carry higher load factors on the planes and full connectivity is quickly becoming table stakes for passengers. 
On the government side, Starshield continues to deliver unique mission-critical capabilities, and we see further room for growth. We remain on pace for enterprise and government revenues to exceed consumer connectivity revenues in the future, each. The successful deployment of the operational V3 broadband satellites on Starship's Flight 14 marks an important step and an inflection point for Starlink. The increased capability from these satellites, as Elon talked about, and the Starship launcher itself will provide additional capacity across markets and enable new sales in high-demand areas. We expect the market for communications to grow far beyond just human communication that we traditionally think about. Connecting cars, robots and the adoption of Super Intelligence will increase communication demands, not in percentages, but in many orders of magnitudes. In the years ahead, we expect Starlink will represent a significant -- Starlink alone to represent a significant portion of global Internet traffic. 
In mobile, we continue to expand international partnerships, turning on service with new carriers across multiple countries in the third quarter, including Uganda, the Democratic Republic of Congo, Kazakhstan and Costa Rica. We surpassed 22 million monthly users on Starlink Mobile as of the end of the quarter, up 37% quarter-over-quarter. Our near-term priority remains flying the mobile V2 constellation through next year and integrating our spectrum purchases to turn on service in early 2028. Just a few weeks ago, we received approval from the FCC to launch 15,000 mobile V2 sats and announced an agreement to acquire a portfolio of low-band spectrum, which will pave the way for Starlink Mobile to become a major mobile carrier in the U.S. 
Moving to Super Intelligence. The industry continues to demand ever more massive amounts of compute. We're rapidly expanding capacity to meet both our own needs as Grok and related products scale and those of our cloud service customers. Enterprise feedback on recent model releases has been positive and Grok bot, in particular, is seeing strong adoption out of the gate. Grok bot, our Agentic Assistant, launched in August, and we already had paid weekly users of 800,000 earlier this month, more than doubling over the last month. B2B is our fastest-growing category with companies increasingly using Grok bot as a force multiplier across sales, marketing, IT and engineering, treating it as an always-on teammate for complex end-to-end workflows. 
We're also accelerating our Grok model release cadence with significant performance gains expected in the near term -- well, have been and more in the near term. At the same time, the integration of Cursor continues to progress well, strengthening both our product capabilities and our go-to-market reach with a scaled enterprise sales force. Early evidence of this momentum is already visible. Grok Enterprise customers with more than $1 million in run rate revenue, including Cursor, were up 50% quarter-over-quarter on a pro forma basis. Last week, we further integrated the portfolio by announcing a new scheme that brings together Grok, Grok bot, Cursor and X Premium on a single plan. 
In review, our business is experiencing extremely strong momentum across all three segments, our engineering teams are scaling Starship and next-generation satellites across broadband, mobile and Starshield, while our commercial teams expand Starlink across aviation, enterprise, government and global markets. At the same time, we're scaling our Super Intelligence business in the key areas of critical compute infrastructure, leveraging our hardware expertise. 
Now Bret, you get to go.

**Bret Johnsen** (Executives):
Thank you, Gwynne. We delivered another strong quarter in Q3. Revenue grew an impressive 161% year-over-year to $14.6 billion, fueled by the continued momentum in the connectivity business and our clear inflection point in the Super Intelligence or SI business. Adjusted EBITDA once again grew faster than revenue to $8.8 billion, up 306% year-over-year. The combination of our launch leadership, recurring Starlink revenue and the significant expansion of our SI infrastructure business have combined to drive meaningful operating leverage in the business. Our balance sheet remains very strong, and our focus on capital allocation continues to keep us in a position to accelerate the pace of innovation that underpins the significant revenue opportunity across all of our businesses.
I'll now walk through the financials by segment. The space revenues of $1.8 billion were up 84% sequentially and up 6% year-over-year, anchored by a favorable customer mix. We're on track to deliver strong growth for the year based on our robust customer manifest for Falcon and Dragon vehicles. As far as capital allocation, we continued to invest in our Starship program, accelerating Raptor engine and vehicle production, advancing Gigabay construction and progressing multiple launch pads at both Starbase and the Cape. And importantly, we secured the location for the next phase of United States space launch leadership in Louisiana. These investments remain essential to unlocking the step change in cost and capacity that Starship will deliver. 
Connectivity, again delivered robust revenue growth and profitability with revenues of $5.2 billion, up 69% year-over-year and 22% sequentially. As Gwynne mentioned, we reached 13.6 million Starlink consumer subscribers, adding 1.6 million subscribers just in Q3 alone, driven by growth in more developed markets. During the quarter, we began ramping production of our V5 kits, which supported our progress on alleviating inventory constraints. We strategically managed our channel distribution and prioritized delivery of kits to retail channels ahead of the holiday season, which we expect will lead to increased activations in Q4. 
Starlink consumer average revenue per user, or ARPU, monthly average revenue per user increased 5% sequentially to $69 per month, benefiting from a favorable customer mix dynamic in the quarter. Enterprise and government revenues grew 91% year-over-year and 18% sequentially, highlighted by growth in our Starshield program with the United States government and the continued momentum in the aviation industry. Aviation remains a major growth opportunity as we're still early in the installation phase with many of the largest carriers worldwide and have line of sight into an accelerated activation path into '27 for our key partners. 
Connectivity gross profits doubled year-over-year with gross margins of 55%, including a onetime benefit of roughly 3%, primarily driven by tariff refunds in the quarter. Excluding the onetime benefits, though, adjusted EBITDA margins expanded roughly 2% year-over-year. Looking ahead, the satellite road map is a key driver of both the capacity and capability of our Connectivity segment. Through the end of the year and throughout 2027, we expect to deploy V3 broadband satellites in meaningful volume with each Starship launch ramping towards a payload that delivers over 20x the downlink capacity of the current generation of Falcon 9 launches today. In parallel, we will ramp Starlink Mobile V2 satellites on Starship starting in 2027 and leverage our newly enhanced wireless spectrum portfolio to expand our direct-to-sell service and become a major mobile carrier, as Gwynne mentioned, in the United States. Across all three of our connectivity applications, Starlink Broadband, Starlink Mobile and Starshield, the launch cadence on Starship is expected to drive a step change in total capacity coverage and service quality. 
SI or Super Intelligence was again the standout growth driver for the quarter. segment revenue increased substantially to $7.6 billion, up $5 billion quarter-over-quarter and $6.7 billion year-over-year, primarily powered by the ramp of our cloud services agreements. We meaningfully improved the segment's profitability profile as we monetize newly deployed capacity and delivered powerful operating leverage for the business. We ended the third quarter with 1.7 gigawatts of nameplate compute capacity with additional data halls already online in early October.
For SI Solutions and Infrastructure, revenues were $7 billion, of which $608 million came from the Cursor acquisition closed roughly mid-quarter. And even excluding Cursor, SI Solutions and Infrastructure revenues grew 192% sequentially, driven primarily by the activation of new cloud services agreements. There are many customers asking for compute, and we're actively building the supply to meet both internal and external demand. We expect to have additional new customers in future deals and we'll continuously evaluate the highest margin usage for our compute assets across both new and existing cloud service agreements and serving inference for our own SI products.
What we're seeing in the market is extraordinary. At current pricing, new compute deployments are generating a payback of less than a year. Pricing is currently tracking slightly above the high end of the $30 to $50 per watt range we were discussing just last quarter, which further supports the attractiveness of these terrestrial SI compute investments. We'll continue to be demand-led and prudent in the pace of deployment, matching our disciplined and proactive capital planning for procurement of semiconductor supply to the near-term customer demand. Our current customer contracts for SI compute have the benefit of allowing us to flexibly manage our capacity for our own model training purposes as well as be able to monetize for our SI cloud service agreements revenue at favorable pricing as the market availability continues to tighten. 
Advertising revenues grew 19% year-over-year as we build more momentum on the new advertising tech platform that we rolled out just last quarter in Q2. 
SI segment adjusted EBITDA was $5 billion, up $3.8 billion quarter-over-quarter and $5.4 billion year-over-year, driven primarily by higher-margin cloud service agreements. SI segment operating income was $431 million, but excluding the $1.2 billion of stock-based compensation expense related to the Cursor acquisition, the segment delivered $1.6 billion of operating profit just in Q3. Double-clicking on the share-based compensation expenses, of the $60 billion equity value for Cursor when we purchased it, $23 billion was attributed towards retaining key employees and replacing outstanding equity awards, including revesting agreements for key executives. These equity awards will be recognized as stock-based compensation over roughly the next 3-year vesting period. 
Total company capital expenditures in the third quarter were $19.6 billion, primarily in support of our SI compute build-out, starship infrastructure and satellite production. 
We ended the quarter with substantial backlog totaling $63 billion as of September 30, of which $17.5 billion was recognized as deferred revenue. Approximately $42 billion of this backlog is expected to be recognized within the next year. 
Looking ahead, demand remains robust across all three segments, particularly in our cloud services business. We remain on track to deliver our previously stated goal of $100 billion in ARR by the end of this year, defined as annualized revenue based on the month of December. SI infrastructure continuing to come online at Memphis and   Southaven gives us visibility into an accelerated build path through the remainder of this year. As a result, we're on track to reach nearly 2.2 gigawatts of nameplate compute at the end of this month alone in October and have a clear line of sight, as Elon highlighted, to nameplate compute in the range of 2.5 to 3 gigawatts just by the end of this quarter. Because of the additional capacity coming online this quarter, we expect fourth quarter capital expenditures to now be in the range of $35 billion to $40 billion for this quarter. 
We also expect total company gross margins in Q4 to be more consistent with the second quarter given some onetime benefits and customer mix that we highlighted in Q3. Given the increased visibility into our compute contract pipeline over the next 6 months, we have the opportunity to provide additional look-forward guidance on the acceleration we see in our business in Q1 2027. We now see total company revenues in the range of $33 billion to $37 billion for Q1 of 2027. 
In closing, we are in a transformative phase for the company's financial profile. We're investing aggressively across SI compute, Starship development and production and next-generation Starlink broadband and mobile constellations, the three areas we believe will generate the highest long-term returns. These are demand-led investments in markets with visible, tangible returns in the near term. We're building the infrastructure of the future with discipline, focused on capital efficiency, strong returns on invested capital and maintaining a strong investment-grade balance sheet while still moving with the velocity to capture the opportunity in front of us. The combination of our diversified earnings base, focus on extreme vertical integration and the robust demand in the market for Super Intelligence gives us conviction in the path ahead. 
With that, I'll turn it back to Andrea.

**Andrea Williams** (Executives):
Thanks, Bret. We're now going to begin the Q&A section. [Operator Instructions]. We will take the first question from Adam Jonas at Morgan Stanley.

**Adam Jonas** (Analysts):
First, Elon, thank you for making flying cars real.

**Elon Musk** (Executives):
You're welcome.

**Adam Jonas** (Analysts):
That was freaking insane. It's my first comment.

**Elon Musk** (Executives):
[indiscernible], and that's one of them.

**Adam Jonas** (Analysts):
It's super inspiring for people all over the world, especially young people that want to build. I got a two-part question on Terafab. You want to make chips. You want to make crazy amounts of chips onshore or in a safe and secure place. So, first, can you confirm if SpaceX has placed orders for EUV machines? If so, when do you expect delivery? 
And just as a second part to the question, when you take a first principles approach to the semi fab supply chain, I know you've toured TSMC, ASML, AMD, Lam, these are very impressive companies, as I'm sure you'd agree. Where do you see the biggest areas to improve their processes and supply chain when you do it your way?

**Elon Musk** (Executives):
Well, I mean, we're just figuring out chip fabrication. So but I'll give it -- I'll tell you what our internal expectations are, which obviously, I put big error bars on this because we don't know if we will actually achieve this or not. But it's what we're aiming for internally is to make our first sort of test chip functional in approximately May or June of next year. That's just a kind of a SRAM chip something that basically test the line. That's at the research fab in Austin. And we're aiming to -- our aspiration is to reach volume production around Q3 of '28 at Terafab at Gibbons Creek, the main Terafab location. 
Now these are very aggressive dates, and we're very appreciative of ASML and all of our other suppliers in accelerating equipment deliveries in order to achieve this outcome. Let's just say that, that outcome of achieving volume production is at least in a set of possible outcomes for Q3 or Q4 of '28. So these are obviously like insanely fast time frames for chip production. 
We do have, I think, some significant potential breakthroughs in chip fabrication, but I don't think I should discuss that on an earnings call. Let's not give away the shop here. But I am optimistic that we will dramatically accelerate chip production and that Terafab will ultimately do what the name suggests, which is to make a terawatt of super intelligence chips per year.

**Andrea Williams** (Executives):
We'll take our next question from Doug Anmuth at JPMorgan.

**Douglas Anmuth** (Analysts):
Great. Elon, can you talk more about just how you're working through those constraints in power cooling and infra and just what gets you comfortable with the 13 gigawatts ending '27? 
And then, Bret, if you could also help us understand how you're thinking about the funding requirements just as you look out to that kind of capacity?

**Elon Musk** (Executives):
Yes. Well, I mean 3 gigawatts of that or very close to 3 gigawatts is what we expect to have done just in the next few months. So you can just look at the rate at which we are actually deploying and turning on compute. 
What I think you hear from, I guess, other hyperscalers is you don't hear a lot of detail about how many GPUs they're actually turning on every month. And with us, you are. I'm being very as precise as possible about this. It's absolutely insane to be deploying providing the power and all the electrical equipment, the cooling, the batteries, the networking and everything else that's needed to turn on 20,000 GB300s a month but that is actually what we're doing right now. And that pace will obviously accelerate next year. We're not going to slow down.  
I don't think -- again, I don't want to -- some of this -- if you say like how we're going to get all this power, let's just say like we actually -- we do have a plan that gets to 20 gigawatts of power and cooling by the end of next year. But that is not something that I should spell out. That is highly proprietary because if I tell you about it, others are going to try to do the same thing. And I'm not saying we'll have 20 gigawatts of power. I'm saying we have a plan where if everything goes right, we'll have 20 gigawatts of incremental power, I should say, next year. So 23 gigawatts roughly in total.
Now I don't expect everything to go right. That's why I said I'm confident of 10, highly confident of 10 next year. And 20 is difficult but not impossible. And I mean, some of the things we're doing, I have mentioned publicly. So we're casting the blades and vanes for the turbines. So SpaceX already has a very advanced castings capability that was developed for rocket engines. So we have, I think, actually the most advanced casting capability on earth because the demands for castings for rocket engines exceed the demands for everything and anything else you could possibly imagine. 
So taking that incredible team that has, I think, objectively, the most advanced casting technology in the world and saying, hey, can you guys also make some blades and veins for terrestrial turbines is much easier than what they have done in the past. And when we talk to the turbine suppliers, they tell us that the blades and vanes are 12 to 18 months behind the rest of the turbine, meaning they can deliver everything except the blades and vanes 12 to 18 months before they can deliver the blades vein. So casting is this really difficult bottleneck. And if anything, it seems to be getting worse. 
So that means that we can bring power online 12 to 18 months faster than anyone else. That's the kind of advantage that's difficult to replicate. Unless someone else is doing advanced casting -- is building an advanced casting shop, they will be unable to compete with SpaceX in this regard. And we're looking at many different sources of power, not just gas turbines. There's -- we obviously want to use solar, wind and every other source of power that we can obtain.
We think there's also a lot of opportunity for inference compute if you manufacture modular inference compute at the factory level and then such that it's -- the power and cooling are built in at the factory and then you distribute modular inference compute clusters all over the country, if not all over the world. That's about as much as I should say about scaling power and cooling. But like I said, at this point, I would say I feel highly confident of 10 gigawatts incremental next year, so 13 total. And some number over 20 is -- the probability of achieving that is rising rapidly.

**Bret Johnsen** (Executives):
Doug, the second part of your question related to funding. I think we certainly have the advantage related to others in that we are investment grade, have a very strong balance sheet. And there are a number of available pools of debt capital that we are talking to at the moment related to funding this incredible growth. 
The other really important thing to emphasize is the payback period is very short. And so this capability starts to fund itself in a pretty near-term situation. And so the fact even that we're finishing this quarter with more capability starts the funding mechanism even into the first half of next year. So you have your operational cash flows, first and foremost. You have multiple pools of capital available in the debt market, especially because of our investment-grade status and strong balance sheet. And then you also have the opportunity from what we've seen to partner with, I would say, the whole value chain related to -- on the vendor and customer side. 
So there's nothing easy about SpaceX for sure. And so might as well have the finance piece be part of the challenge at the same time. But we have a lot of conviction that we were going to be able to do this in a very measured fashion and continue to keep ourselves in that IG status along the way.

**Elon Musk** (Executives):
And certainly, if you look at our track record with respect to capital efficiency, Starship and all of our other projects, you'd be hard-pressed to find any company in the world that is as good at capital efficiency as SpaceX.

**Bret Johnsen** (Executives):
Exactly.

**Andrea Williams** (Executives):
Next question from Edison Yu at Deutsche Bank.

**Xin Yu** (Analysts):
I'll echo Adam's enthusiasm about the Roadster. So there's been a lot of reporting, a lot of anticipation of a merger with Tesla. I realize maybe you may be limited on what you can say. But if we take a step back, how do you think about the pros and cons of a potential combination? And as part of that framework, are there any roadblocks that you would need to address before embarking on it?

**Elon Musk** (Executives):
I mean this is definitely kind of a question where I feel like I'm tap dancing through a mine field. But -- so I have to be thoughtful about what I say here. I think -- so both SpaceX and Tesla have formed special committees to discuss this idea at the request of shareholders. And these special committees are consist of independent directors. And because I'm a conflicted party, I can't actually be in the discussions of the special committees. So it's sort of -- it's an odd kabuki dance where two groups of people are talking, and I can't be in the conversation. 
I mean I don't think we should necessarily assume that -- I think some people out there assume that a SpaceX and Tesla merger is a certainty. And I think that would be overstating it. Do I think it would be a good idea, yes. But at the end of the day, the shareholders have to be supportive of this. And particularly on the Tesla side, we will need a 50% vote of all shares, not just those who vote, but of all shareholders. And that's quite a high hurdle to try to achieve. 
So and I can just say at this point that the special committees have not reached agreement on the terms of any transaction. And obviously, there's no guarantee that they will. But I do think there's a lot of merit to combining the companies as we are pretty much in the super intelligence singularity. And -- and there's a lot to be gained from cooperating on developing super intelligent software, chip design, the Terafab, obviously, robotics, mass to orbit with the Starmind constellation.

**Gwynne Shotwell** (Executives):
Connectivity.

**Elon Musk** (Executives):
Connectivity. So I think it will be a good idea, but it's really up to the special committees of both companies. Like they've got to come up with something, and then that's got to be put to the shareholders as a vote.

**Andrea Williams** (Executives):
Next question from Kutgun Maral at Evercore.

**Kutgun Maral** (Analysts):
I wanted to ask about Starlink Mobile, which has come a long way in a short time, including the recent low-band deal. Even so, there's still some uncertainty about how your spectrum portfolio, even though it's much improved and possibly will continue to grow, can compete with incumbents in the U.S. And part of the unknown for us on the outside is how much coverage and capacity the satellite layer can really provide to bridge the terrestrial gap to peers. So what roles do you expect the satellite and terrestrial parts of the network will play? And how should we think about the traffic mix between them and delivering a 5G-like experience in the U.S.? And maybe more broadly, how much of the connectivity focus is on traditional retail wireless versus what could be a massive physical AI opportunity?

**Gwynne Shotwell** (Executives):
Yes. Let me, Elon can fill in some details, but let me point out that the vast majority of mobile connectivity is actually WiFi, right? I think it's something between 85% and 93% is done through WiFi. And keep in mind, Starlink Broadband does a lot of WiFi work as well. 
As far as the mix goes, I think we expect that the S-band spectrum will provide the majority. And then obviously, you need the low-band spectrum, the 800 megahertz spectrum to basically penetrate buildings. So if you're not on WiFi, you can still receive the signal. So I think -- and by the way, I'll correct myself if I'm wrong afterwards, but I think the S-band will carry the majority and then the low-band spectrum will carry less, but provide a critical piece, by the way. 
And also, we talked last quarter at the last earnings call about smaller kind of not quite tower capable, but smaller radios that we would -- we could put on already installed homes for Starlink, businesses for Starlink, towers as well. So it's not just the spectrum that we've talked about with the S-band. We will basically leverage the real estate from Starlink installs and other towers.

**Elon Musk** (Executives):
Yes. I think we probably should do a longer presentation on the game plan for Starlink connectivity and why we think it will ultimately be a business that generates several hundred billion dollars in revenue a year because you are missing some of the pieces that we know about internally. I can say we do see a clear path to several hundred billion dollars a year in connectivity revenue. But I think we should probably describe that in more detail in a forum that's not limited to a few minutes at an earnings call.

**Andrea Williams** (Executives):
In fact, we have three minutes left, right?

**Elon Musk** (Executives):
Well, we can go a little longer.

**Andrea Williams** (Executives):
I'll take the next question from Eric Sheridan at Goldman Sachs.

**Eric Sheridan** (Analysts):
Maybe if I could turn to the scaling of compute you laid out at the beginning part of the call. When you think about a framework for applying that compute to the external opportunity that presents itself from cloud services relative to the internal needs of that compute for scaling Cursor and Grok bot, how has your view evolved about striking the right balance in that mix? And how to think through the output from a monetization standpoint of what that mix might produce for the business in the next 12 to 18 months?

**Elon Musk** (Executives):
Well, the allocation -- the relative allocation of compute to third parties versus internal is something that's going to change from one month to the next. I guess as a rough approximation. Our goal is to kind of split it 50-50, more or less, where half of the compute is used internally and half of it is rented to others. But that number could shift 60-40 one way or the other. It could -- it's going to be dynamic. And obviously, our approach is to rent at the -- effectively the spot market rate as opposed to sign these long-term deals.
Our belief is that the value of compute per watt will increase over time, not decrease. And the reason for that, I think it should be obvious to people really is that as you improve the AI software, as the models get better and better, they're able to -- you get more useful intelligence per watt. And the value of that compute is proportionate to the useful intelligence per watt. And that's why you see things like even old computers like H100s renting for more than they rented when they were new. And I think that's likely to continue. 
I think we're going to face a shortage of super intelligence compute. And that shortage is going to remain for a long time. So I think the smart move is to do short-term contracts and to and essentially to make -- to place the bet on useful intelligence per watt increasing rapidly, which obviously has done. So that's what's happened so far.
And also, if you look at, say, how are our short-term contracts renewing? Are they renewing at higher dollars per watt or lower? And we see them renewing at higher dollars per watt, not lower dollars per watt. We are also, frankly, hounded relentlessly by every hyperscaler and by dozens of smaller companies to rent more of our compute. So we could rent out our compute several times over if we said yes to everyone. That's just the situation here. That's why I posted that sort of video, video me of the Monty Python cheese shop sketch where the guy goes into a cheese shop to get some cheese and they actually have no cheese. And so he goes like, what about this kind of cheese? What about that kind of cheese? And they really just don't have any cheese. 
So we've actually tried to offload some of our inference compute to other cloud providers so that we can use more compute for training. And we get the cheese shop sketch. They'll say like, well, we'll ask them about what about some GB300s, don't have any of those. What about some GB 200s, don't have any of those. What about some TPUs? Now what about some trains? No, what about some -- okay, how about some H100s. And like, well, we might have some overseas somewhere, and then they'll check and come back and say, no, we don't have that either. So it's like it's ridiculous. Yes. So I don't think we're going to have a demand issue here. And like it's not impossible. I'm not saying this will happen. It's not impossible that we will have a six-month payback period for compute next year.

**Andrea Williams** (Executives):
We're now going to turn to some questions from individual investors that were posted directly on to our public Q&A platform. So we've talked a lot about compute deployment terrestrially, let's move to a question on V3 sats. So when will capacity gains from V3 satellites actually show up as meaningfully higher speeds and lower latency for users? How many V3 sats are needed before the network feels noticeably better in high-demand areas?

**Gwynne Shotwell** (Executives):
I think we'll need a few hundred V3 satellites for people to really feel the impact because right now, with very few satellites, you'll get an impact and then 10 minutes later, it won't be there. So a few hundred satellites, and I think we can achieve that by mid next year.

**Andrea Williams** (Executives):
Take #6, which is, can you provide an update on Starbase Louisiana? What's the time line? And what's your current confidence level in achieving a first starship launch from the site as early as 2029?

**Elon Musk** (Executives):
Well, our internal aspiration for first launch from Louisiana is actually in two years. So '28 would be -- is our goal. But I think '29 is highly likely. I think we'll be at scale launching from Louisiana at scale in '29. Highly confident.

**Andrea Williams** (Executives):
Thanks, everyone. This wraps up the Q3 2026 earnings report. Thank you all for tuning in, and we will see you next quarter.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SPCX_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Bret Johnsen｜guidance：CFO 稱含 Cursor 貢獻，預期年底以 12 月營收年化計達 1,000 億美元 ARR（原話："to reach $100 billion of ARR or annualized revenue run rate"）
- 2026-08-04｜Elon Musk｜guidance：Musk 稱 ARR 目標屬保守情境，可能高於該數字（原話："I think it may be higher than that"）
- 2026-08-04｜Bret Johnsen｜guidance：CFO 指引未來兩季資本支出與本季相近（原話："the next 2 quarters are very similar to the"）
- 2026-08-04｜Elon Musk｜guidance：年底運算容量目標超過 2 GW（原話："we expect to end this year with over 2 gigawatts of compute"）
- 2026-08-04｜Elon Musk｜guidance：Musk 開場稱 2027 年底累計運算將數倍於年底水準，約 10 GW 而非 5 GW（原話："compute online by the end of next year will be several times"）
- 2026-08-04｜Elon Musk｜guidance：被問 10 GW 的把握時，Musk 改談電力冷卻端 20 GW 暫定目標，並自承不會全達成（原話："Now I don't think we're going to achieve 20 gigawatts"）
- 2026-08-04｜Elon Musk｜guidance：內部 1 兆美元營收目標由 2031 提前至 2030（IPO 前為 2031）（原話："have moved up from 2031 to 2030"）
- 2026-08-04｜Elon Musk｜guidance：Musk 稱 2029 達成 1 兆營收亦有非零機率（原話："And there's a non-zero chance of that being in 2029."）
- 2026-08-04｜Elon Musk｜guidance：Musk 預期內部 Grok 訓練僅占約 10% 運算量（原話："So I would expect maybe 10% of our"）
- 2026-08-04｜Bret Johnsen｜margin：管理層稱新增運算資本支出回收期不到一年（原話："turned adjusted EBITDA positive for the segment in the"）
- 2026-08-04｜Bret Johnsen｜margin：Connectivity 營業利益成長快於營收，營業利潤率擴張近 3 點（原話："Space adjusted EBITDA was a loss of $205 million"）
- 2026-08-04｜Bret Johnsen｜margin：Space 板塊調整後 EBITDA 虧損 2.05 億美元，歸因於 Starship R&D（原話："Space adjusted EBITDA was a loss of $205 million for the"）
- 2026-08-04｜Bret Johnsen｜margin：AI 板塊調整後 EBITDA 轉正為 11 億美元（原話："The incremental revenue from new hosting deals generated"）
- 2026-08-04｜Bret Johnsen｜margin：新增代管協議帶來高增量 EBITDA 利潤率（Q2 貢獻 16 億美元增量 AI 基礎設施營收）（原話："our geographic expansion may drive down blended ARPU over"）
- 2026-08-04｜Bret Johnsen｜margin：管理層預告地理擴張可能壓低混合 ARPU（Q2 ARPU 持平於 66 美元）（原話："my guess would be somewhere between $30 and $50"）
- 2026-08-04｜Elon Musk｜margin：Musk 對 Rubin 每瓦變現金額的猜測區間（自稱僅是猜測）（原話："my guess would be somewhere between $30 and $50"）
- 2026-08-04｜Gwynne Shotwell｜customer：Q2 Starlink 消費者淨增訂戶超過 170 萬，前季為 140 萬（原話："scale at least comparable, but likely exceed our Consumer"）
- 2026-08-04｜Gwynne Shotwell｜customer：企業與政府營收規模有望至少相當、可能超過消費者業務（原話："we won more than $6 billion in U.S. contracts in Q2"）
- 2026-08-04｜Gwynne Shotwell｜customer：Q2 取得逾 60 億美元美國政府合約（原話："contracted an additional $6.7 billion of cloud services"）
- 2026-08-04｜Gwynne Shotwell｜customer：企業客戶黏著度：稱從未流失企業客戶（原話："We have never lost an enterprise customer."）
- 2026-08-04｜Bret Johnsen｜customer：Q3 前幾週已新簽 67 億美元雲服務合約，為期 6 個月，10 月起認列（原話："raising approximately $85.7 billion in net proceeds"）
- 2026-08-04｜Bret Johnsen｜capital_allocation：IPO 淨募資約 857 億美元（原話："Total company capital expenditures in the second quarter"）
- 2026-08-04｜Bret Johnsen｜capital_allocation：Q2 總資本支出約 184 億美元，其中約 158 億用於 AI 運算（原話："paid out $856 million during the quarter under our spectrum"）
- 2026-08-04｜Bret Johnsen｜capital_allocation：Q2 依頻譜信貸協議支付 8.56 億美元（EchoStar 交易）（原話："Our capital allocation priorities remain clear and"）
- 2026-08-04｜Bret Johnsen｜capital_allocation：資本配置優先順序：Starship、下一代 Starlink、AI 運算三項積極投入（原話："Our capital allocation priorities remain clear and"）
- 2026-08-04｜Elon Musk｜capital_allocation：宣布 AI 運算今後僅採用 NVIDIA（原話："So we're exclusive to NVIDIA."）
- 2026-08-04｜Elon Musk｜competition：Musk 稱鼓勵競爭者複製、不以專利阻擋（原話："we actually encourage our competitors to copy us"）
- 2026-08-04｜Elon Musk｜product：Musk 稱下一次飛行（預定本月底）將在取得監管核准下嘗試塔架接船（原話："we'll attempt to catch the ship with the tower on the next"）
- 2026-08-04｜Elon Musk｜product：Musk 稱隔熱盾問題已視為解決（原話："I think I'd consider the heat shield problem solved at this"）
- 2026-08-04｜Elon Musk｜product：Grok 迭代時程：4.6 下週、4.7 約 3–4 週後（原話："Grok 4.6 coming out probably next week"）
- 2026-08-04｜Elon Musk｜product：Grok 5 預計年底前推出並納入 SpaceX 全部歷史資料訓練（原話："we will be incorporating the entire corpus of SpaceX data"）
- 2026-08-04｜Elon Musk｜commitment：Musk 稱約一年後 Starship 每天至少一次飛行（原話："we will be doing at least 1 flight a day, possibly more."）
- 2026-08-04｜Elon Musk｜commitment：V3 衛星需約 1,000 顆臨界量才顯著改善服務，預計明年第二季達到（原話："probably at least on the order of about 1,000"）
- 2026-08-04｜Gwynne Shotwell｜commitment：Starlink Mobile 明年開始發射衛星，明年底開始提供服務（原話："start to fly the satellites next year, and we will start"）
- 2026-08-04｜Elon Musk｜risk：Musk 稱目前運算的限制因素是記憶體（原話："The limiting factor currently is memory."）
- 2026-08-04｜Elon Musk｜risk：Cursor 收購尚待監管完成，Musk 不願提前談產品路線圖（原話："But we don't want to jump the gun on regulators for the"）

### 問答異常語氣（迴避／改口／保留）
- SPCX_Q2_2026_Earnings_Call_20260804.md｜問：Evercore 問美國行動業務若成第四大電信商的資本支出，以及自建／MVNO／收購的取捨｜答法：Shotwell 明確拒絕給出行動業務資本支出數字，改談小型基地台構想並稱「會很節省資本」
- SPCX_Q2_2026_Earnings_Call_20260804.md｜問：Morgan Stanley 確認 2027 年底 10 GW 並問許可、晶片、渦輪的把握度｜答法：Musk 未直接回答 10 GW 把握度，改談電力冷卻端 20 GW 暫定目標，自承約 1/4 專案可能延遲、實際約 15 GW，且未談許可與渦輪細節
- SPCX_Q2_2026_Earnings_Call_20260804.md｜問：股東提問：Cursor 收購完成後的合併產品路線圖｜答法：Musk 不回答路線圖，稱稍後在法說會外另行說明，並以監管未完成為由

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

## ⑥ 條件附卡（archetype_hint='未獲利高成長' 命中）：judge_addendum_archetype.md

<!-- source: .claude/skills/stock-analyst/references/archetype-gatesets.md sha256:d173785f92087f36 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary ∈ {金融，未獲利高成長，轉機/特殊情境，受監管公用/穩定內需} -->

# archetype 換尺 gate-set 附卡（QC-44/45/46）

## QC-44 金融（bank／insurer／broker）
archetype=金融時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：ROTCE(替FCF Margin) >15%穿越循環｜ROE且>COE~10%(替ROIC) ROE>12-15%｜跨信用循環ROTCE穩定含2008/2020壓力年(替10Y ROIC穩定) 壓力年仍正/不破底｜NIM趨勢+效率比cost/income(替毛利率定價) 效率比<~60%｜Capex/Rev不適用→operating leverage/效率比改善｜EPS+TBVPS複合+股息總回報(替EPS CAGR>20%) ~10-12%即優｜P/TBV vs ROTCE(替PEG)：Warranted P/TBV=(ROTCE−g)/(COE−g)，實際P/TBV≤warranted｜CET1 ratio(替D/E<0.7) >監管要求+緩衝(~11-13%)｜NPL/NCO趨勢+撥備覆蓋+CET1緩衝(替負債安全性)：信用品質穩、撥備足。[§QC-44]
§10估值主錨：P/TBV分位+P/E，用Warranted P/TBV判貴賤；EV/EBITDA拿掉。QC-31 signal：X改ROTCE跨循環<COE／CET1跌破監管／NPL·NCO結構惡化／重大舞弊，移除FCF·NI、EV-EBITDA、Capex觸發。§6跑道：放款·存款·AUM成長+費收業務+市佔，非TAM滲透。[§QC-44]
子型：bank＝CET1/NIM/效率比/NPL·NCO/ROTCE/P-TBV｜insurer(注意US掛牌ALV=Autoliv汽車安全件循環工業，非保險，勿誤歸)＝combined ratio<100%/float/Solvency II ratio/book value/ROE，不看NIM/CET1｜broker·交易所＝ARPU/AUC/take rate/活躍戶，常與未獲利高成長blend｜支付網絡不歸金融，走品質複利。[§子型]
batch補搜：`[ticker] CET1 ratio NIM efficiency ratio ROTCE`(bank)／`[ticker] combined ratio Solvency II book value`(insurer)；yfinance .info 給不出 CET1/NIM/效率比/NPL/ROTCE/TBV。[§batch]

## QC-45 未獲利高成長
archetype=未獲利高成長時，§4/§10/QC-31/§6 改用下列 gate-set：
§4 門檻組：Rule-of-40(營收成長%+FCF margin%，替EPS CAGR>20%) ≥40｜EV/S÷營收成長growth-adjusted或EV/gross-profit(替PEG<2)｜NRR+毛利率+增量OI margin改善軌跡(替ROIC>15%，GAAP負無意義) NRR>110%/GM>65-70%｜FCF margin+轉正軌跡(替FCF Margin>15%；已正看margin升，未正看跑道+轉正路徑)｜NI負時FCF/NI比無意義→改看FCF margin絕對值+淨現金+跑道，FCF正或跑道>12個月。[§QC-45]
§10估值主錨：EV/S(+EV/gross-profit)+Rule-of-40-adjusted，轉正後接forward P/E；trailing PE/PEG拿掉。**情境樹同步改走EV/S（2026-10-12）**：FY1共識EPS≤0時程式自動切`valuation_basis=sales_multiple`，`scenario_inputs`填營收路徑×終端EV/S×終端淨負債×終端股數（形狀見尾段），不再用EPS×本益比；負債重者(淨負債/EV>30%)Bear的`net_debt_y5`須如實反映融資缺口，股權價值為負即歸零。QC-31 signal：不因GAAP NI負觸發X；X改NRR跌破100%／Rule-of-40<20連2季／毛利結構崩／現金跑道<12個月無轉正路徑／SBC稀釋失控(股數>10%/yr無營收槓桿)。§6跑道：NRR+淨增客戶+TAM滲透+SBC-adjusted轉正時程。blend：fintech broker常＝金融×未獲利，兩套都跑、標背離。[§QC-45]

## QC-46 轉機／受監管公用（輕量尺，不展開大表）
轉機/特殊情境：§4/§10主錨→資產重估/SOTP/normalized earning power/P-TBV，非成長外推；EPS-CAGR/PEG不適用。Single Thing→轉機觸發(債務重組完成/出售虧損部門/新管理層/catalyst里程碑)，非「moat擴張」。§6/§5→「為何現在會轉」catalyst+下行保護(資產底/清算價值)。QC-31 X→流動性危機(跑道<12個月+無再融資)/重整失敗/治理舞弊。[§QC-46轉機]
受監管公用/穩定內需：§4/§10主錨→DDM/殖利率+股息成長/regulated ROE(rate base×allowed ROE)/P/B；PEG/高成長門檻不適用。§6成長→rate base成長+費率案(rate case)+准許ROE，非TAM滲透。§5護城河→監管特許/天然獨佔(single-axis)。QC-31 X→准許ROE結構下調/費率案連敗/監管轉敵/過度槓桿(利率敏感)。[§QC-46受監管]
此兩類不強制長表，但換尺與catalyst/下行保護須sourced。[§QC-46]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260805","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Starlink 維持 LEO 寬頻的實質獨占，並在 ARPU 下滑中以量補價，把分部營收推到 FY27 約 $29B、營益率 ≥40%"},{"id":"H2","text":"AI 運算租賃把約 $41B 的年化已簽約基礎轉為認列營收，並在初始合約期後以不低於 $35/W·年的單價續約"},{"id":"H3","text":"2027 年約 $100B 量級的資本缺口能以投資級債務完成融資，不觸發降評、不需大幅股權稀釋"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"鎖定期解禁的股權供給洪水：2026-08-06 首波約 9.115 億股解禁（現流通約 2.81 億股／媒體口徑約 5.55 億股，即現 float 的 1.6-3.2 倍），其後 70/90/105/120/135 天各約 7% 分批、Q3 財報後約 28%、2026-12-08 全面解禁。價格條款（財報前 10 個交易日中 5 日收在 $175.5 以上）未達成，故額外 10% 不解鎖"},{"id":"R2","text":"AI 客戶集中度 × 90 天終止條款 × 租賃單價通縮：三大客戶佔已簽約基礎 100%，且 Anthropic 與 Google 皆為 Grok 的直接競爭對手、同時自研 TPU／Trainium 以逃離外租市場；Google 合約自 2026-12-31 起雙方 90 天可終止（公開條款）"},{"id":"R3","text":"多星系同時進入 Starlink 的擴張市場：Kuiper 392 顆（已錯過 FCC 2026-07-30 的 1,616 顆里程碑，取得有條件豁免、2029-07-30 終期未變）＋ 中國 Guowang 約 177 顆／Qianfan 逾 200 顆（2026 目標各 310／324，以巴西為首個海外商用市場）＋ AST SpaceMobile 取得 FCC 248 顆授權與逾 60 家 MNO。這些對手鎖定的正是 Starlink 用來擴張訂戶的低 ARPU 新興市場"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤$82（隱含 AI 分部 ≤35x FY27E EBITDA）且 H1/H2 監測未惡化；或 Q3 AI 分部營收 ≥$6.0B ＋ Google/Anthropic 合約展期，則 ≤$110 可建 starter","irr_base_pct":-3.0,"ev5y_pct":-0.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.3,"ev5y_pct":-0.3,"irr_base_pct":-3.0,"max_dd_pct":-70.0,"bull_5y_price":260.7,"bear_5y_price":37.6,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"股價 ≤$82（隱含 AI 分部 ≤35x FY27E EBITDA）且 H1/H2 監測未惡化；或 Q3 AI 分部營收 ≥$6.0B ＋ Google/Anthropic 合約展期，則 ≤$110 可建 starter","price_at_dd":125.33,"archetype":"未獲利高成長","cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名中除程式欄以外的每一個**（程式稍後才會算的 p_bull_pct／p_bear_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。**`ma`、`price_at_dd` 兩欄的漂移歸因由程式生成條目，你不要為它們開條目**；`asym_ratio`／`ev5y_pct`／`irr_base_pct`／`bull_5y_price`／`bear_5y_price` 的漂移歸因同樣由程式生成條目（程式用本次情境、依先換情境後換股價的順序拆量），你不要為它們開條目；裁決／角色若因 ma 變動而被矩陣改列，也由程式歸因。你只歸因基本面欄位（signal／val／trap／moat_trend／runway／archetype／情境輸入／門檻）。`oneliner` 不寫倉位角色字樣（核心／衛星／追蹤），角色由程式事後算。

**給讀者看的文字欄不准出現內部代號**：`thesis.H[]`／`thesis.R[]` 的各欄（信息來源／漂移觸發條件等）、`triggers[].text`、`counter_evidence.contradictions[]` 各欄、`answers.*.verdict`／`answers.*.reasoning` 這類文字，一律不得出現事實表 id（`f_` 開頭，如 `f_consensus_rev_3m_fy1_pct`）或軸／finding id（`軸名#n`，如 `competitive_share_entrants#0`）——這些是程式內部代號，不是給讀者的話。要引用哪個事實或哪個軸，寫進對應的 `fact_refs[]`／`evidence_refs[]` 陣列，文字欄本身只寫人話。

---

## 尾段：scenario_inputs 形狀與回覆格式

**本檔 FY1 共識 EPS ≤ 0（虧損），程式已把估值口徑定為 `sales_multiple`：情境樹用營收路徑 × 終端 EV/S，不用 EPS × 本益比。** 口徑由程式決定，你填什麼 `valuation_basis` 都會被覆寫。`scenario_inputs` 的鍵名與形狀必須完全照下面這份（不得增刪改名；程式據此產生 `dd_scenario.py` 的輸入檔，寫錯鍵名就是整段判斷失效）：

```json
{
  "valuation_basis": "sales_multiple",
  "terminal_label": "FY20XXE",
  "start": {"rev": <FY+1 共識營收，百萬，報告幣別；抄事實表 f_rev_consensus_fy1_m>, "ev_s": <目前 EV/S（EV÷FY+1 共識營收）；抄事實表 f_ev_s_fwd>, "basis": "<起點口徑一句話：營收取哪一年、EV/S 的分母是哪一年，須與終端 EV/S 分母同口徑>"},
  "rev": {"bull": [<Y1>, <Y2>, <Y3>, <Y4>, <Y5>], "base": [五個數], "bear": [五個數]},
  "ev_s": {"bull": <終端 EV/S>, "base": <倍數>, "bear": <倍數>},
  "net_debt_y5": {"bull": <終端年淨負債，百萬，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "shares_y5": {"bull": <終端年稀釋股數，百萬股，或 null＝沿用目前>, "base": <…>, "bear": <…>},
  "p": {"bull": <機率整數>, "base": <整數>, "bear": <整數>},
  "yield_pct": {"dividend": <股息殖利率 %>, "net_buyback": <淨回購殖利率 %>},
  "max_dd": {"lo": <負數 %>, "hi": <負數 %>, "basis": "<範圍怎麼推出來的，見判斷卡③情境樹假設段>", "trigger_time": null},
  "basis": {"bull": "<這支路徑的假設一句>", "base": "…", "bear": "…"},
  "endo_ceiling_exceeded": <true|false，共識 CAGR 是否超過 §5.R 內生天花板>
}
```

（**不要**填 `eps`、`pe`、`second_stage`、`peer_max_fpe`；`eps_meta` 仍照常寫共識三年 EPS。現價、目前淨負債（`f_net_debt_m`）、目前股數（`f_shares_diluted_m`）由程式從事實表帶進 `scenario.json`。）

**終端每股價＝max(0, (終端營收 × 終端 EV/S − 終端淨負債) ÷ 終端股數)**，股權價值為負就是 0（Bear 情境債務吃光股權時，要如實寫出讓它歸零，不要為了好看調高倍數）。`net_debt_y5` 要反映該情境下的現金流與融資（虧損公司的淨負債通常會變大，不是沿用目前值）；`shares_y5` 要反映該情境下的增資與稀釋；兩者填 null 才是沿用目前值，不是預設答案。`ev_s` 是終端年 EV ÷ 終端年營收，須與 `start.ev_s` 同口徑（前瞻 vs trailing 不可混）。

`dd_scenario.py` 會擋：`rev` 各路徑長度 ≠ 5、終端營收非 Bear＜Base＜Bull、三機率加總 ≠ 100、`p.bear` ＜ 20、`endo_ceiling_exceeded=true` 且 `p.bear` ＜ 30、`p.base` ＞ 50。另有機械閘：Bull 前兩年營收不得與 Base 相同（情境退化）、`|max_dd.lo|` 不得小於任一情境終點跌幅。機率與路徑是你的判斷，算術（IRR／倍數貢獻／AR）全由腳本算，不要自己填結果欄。

**回覆全文即 `judgment.json` 內容**：緊湊 JSON（`json.dumps(obj, separators=(",", ":"))` 等效格式），陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）。不寫 `scenario.json`（程式從 `scenario_inputs` 產生）。不填不歸你的欄（`decision_inputs` 的機械欄、`reasoning`／`plain` 頂層、`moat.spread_table`／`competitors`、`contradictions`／`triggers` 等舊形狀頂層欄）——填了機械閘會擋。`decision_inputs.asym_ratio`／`irr_base_pct`／`ev5y_pct` 一律填 `null`，由腳本從 scenario 機械算回。

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPCX_20261021/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
