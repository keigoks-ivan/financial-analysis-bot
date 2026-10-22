你是 stock-analyst **v20 判斷 agent**，標的 TXN（20261022）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TXN","date":"2026-10-22","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20261022/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20261022/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":5463,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","citation":"公司新聞稿 investor.ti.com \"TI reports second quarter 2026 financial results and shareholder returns\" (https://investor.ti.com/news-releases/news-release-details/ti-reports-second-quarter-2026-financial-results-and-shareholder)"},"note":"consensus 約 US$5.24B（來源：Q2 FY26 earnings call 前市場預期彙整，Investing.com transcript 摘要引用，非公司揭露）；實際 $5.463B 超出約 4.3%"},{"id":"f_kpi1_gaap","label":"GAAP 營業利益／利益率","value":42.28,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","citation":"公司新聞稿 investor.ti.com Q2 FY26 press release（Operating profit US$2,310M / Revenue US$5,463M）。註：TI 未另外揭露 Non-GAAP 營業利益／利益率，本季亦無 non-GAAP 財報揭露欄位（僅 FCF 為官方 non-GAAP 指標），故通用必填第2、3項合併為此欄"},"note":"查無市場對 GAAP 營業利益率之獨立 consensus 數字"},{"id":"f_kpi4_q3_fy2026_guidance_eps","label":"管理層 Q3 FY2026 guidance（營收／EPS 區間）","value":null,"period":"公告於 2026-07-22（隨 Q2 FY2026 財報同步發布）","unit":"營收 US$5.65B–6.15B（中值 US$5.90B）；GAAP EPS US$2.23–2.57（中值 US$2.40）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"公告於 2026-07-22（隨 Q2 FY2026 財報同步發布）","citation":"公司新聞稿 investor.ti.com Q2 FY26 press release"},"note":"查無公告當下市場對 Q3 guidance 的獨立 consensus 對照","needs_sonnet":true},{"id":"f_kpi5_inventory_days","label":"存貨天數（inventory days，半導體週期性參考指標）","value":196,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","unit":"天","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","citation":"Q2 FY26 earnings call CFO 評論（媒體 transcript 轉述，非新聞稿正文；Investing.com \"Earnings call transcript: Texas Instruments beats Q2 2026 estimates\"），信心層級較低，建議 writer 交叉確認"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-21","period":"2026-10-21","unit":"date","basis":"距今 1 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-21"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_txn_gross_margin_pct","label":"TXN 毛利率","value":58.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_txn_operating_margin_pct","label":"TXN 營業利益率","value":38.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_txn_fcf_margin_pct","label":"TXN FCF 利潤率","value":27.53,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_gross_margin_pct","label":"2308.TW 毛利率","value":35.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_operating_margin_pct","label":"2308.TW 營業利益率","value":16.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_2308_tw_fcf_margin_pct","label":"2308.TW FCF 利潤率","value":11.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_vrt_gross_margin_pct","label":"VRT 毛利率","value":38.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_operating_margin_pct","label":"VRT 營業利益率","value":19.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_vrt_fcf_margin_pct","label":"VRT FCF 利潤率","value":25.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_etn_gross_margin_pct","label":"ETN 毛利率","value":35.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_operating_margin_pct","label":"ETN 營業利益率","value":17.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_etn_fcf_margin_pct","label":"ETN FCF 利潤率","value":13.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi2_fcf_chips_act","label":"自由現金流（FCF，公司定義：營運現金流減資本支出＋CHIPS Act 激勵）","value":2738,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","unit":"US$M（本季）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","citation":"公司新聞稿 investor.ti.com Q2 FY26 press release（Operating cash flow US$2,703M；本季 FCF US$2,738M；TTM FCF US$6,534M，約當 TTM 營收 33.6%，YoY+271%）"},"note":"查無單季 FCF 之市場 consensus 資料"},{"id":"f_kpi3_sbc_gaap","label":"SBC（股票薪酬）占營收／占 GAAP 營業利益 %","value":2.32,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","unit":"% of revenue（另：占 GAAP 營業利益 5.50%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-22）","citation":"公司新聞稿 investor.ti.com Q2 FY26 press release（Stock compensation US$127M；US$127M/US$5,463M=2.32%；US$127M/US$2,310M=5.50%）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":284.65,"period":"2026-10-21（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":21.69,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":55.82,"period":"2026-10-21（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.59,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.49 → 8.44）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.09,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.64 → 10.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":4.0,"period":"2026-10-21","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（13.0 → 13.52）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":8.44,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":10.65,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":13.52,"period":"2026-10-21","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":8.21,"period":"2026-07-16 → 2026-10-21","unit":"%","basis":"FY1 共識 EPS 7.8 → 8.44（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-21","citation":"DD_universe_EPS_estimates_20261021.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":43.33,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":13.36,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":13.73,"period":"2026-10-21（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-21（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-21（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-21（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":33.73,"period":"2026-10-21","unit":"x","basis":"分母＝FY1 EPS 8.44，分子＝快照價 284.65","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-21"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.995,"period":"2026-10-22","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-22"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":7051.0,"period":"2026-10-22","unit":"USD m","basis":"yfinance 最新一季：總債務 14052.0、現金 7001.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":913.25,"period":"2026-10-22","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":267006.95,"period":"2026-10-22","unit":"USD m","basis":"市值 259955.95 ＋ 淨負債 7051.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":21972.06,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（30 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":25183.36,"period":"2026-10-22","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（30 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":12.15,"period":"2026-10-22","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-22"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-22","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 284.65 / W52 238.21 / W104 209.39 / W250 179.8 / W250 13週斜率 1.1%"},{"id":"f_ma_w52","label":"52 週均線","value":238.21,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":209.39,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":179.8,"period":"2026-10-22","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.1,"period":"2026-10-22","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-22","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"TI held an estimated 17.8%-19% share of the global analog semiconductor market in 2025, the industry-leading position ahead of ADI and Infineon.","source":"Analog Semiconductors Market Size & Share 2026-2035 (gminsights.com)","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"TI began production at the first module of its Sherman, TX 300mm fab in December 2025 (65nm/130nm analog nodes for smartphone power-management ICs) and announced in February 2026 a second cleanroom module adding 20,000 wafer starts/month by 2028, expanding low-cost in-house capacity ahead of the industry.","source":"BingX/TI newsroom coverage of Sherman fab expansion","url":null,"excerpt":null,"as_of":"2026-02-01","retrieved_at":"20261022","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Over the past five years, Chinese domestic analog vendors (e.g., SG Micro, 3Peak) have gradually eroded overseas incumbents' (including TI's) share in telecom and consumer-electronics segments, driven by geopolitical friction and China's domestic-substitution push, though their overlap is concentrated in TI's mid-to-low-end part numbers rather than the full portfolio.","source":"Chinese analog chip vendors brace for impact as Texas Instruments slashes prices (jw.ijiwei.com); Citrini Research \"Semis Memo: Supply Chain Inheritance\"","url":null,"excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261022","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"TI, NXP and Infineon raised analog IC prices effective April 2026 (TI hikes up to 85% on select parts), and TI announced a third sweeping price increase in May 2026 effective July 1, 2026. Analysts flagged that end customers seeking to avoid TI's price hikes may accelerate adoption of Chinese domestic alternatives, especially in long-cycle industrial and automotive sectors.","source":"BigGo Finance: \"Texas Instruments' Third Price Hike in Six Months Ignites New Analog Chip Cycle, Opening Triple-Bonanza Window for China's Domestic Substitution\"","url":null,"excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Hudson Labs' 2026 TXN peer comparison notes TI has recently gained share in China (roughly 22% of TI's total revenue) even as local Chinese competition becomes faster and more capable, describing the China dynamic as a net share gain for TI so far.","source":"Texas Instruments Competitors: TXN Peers 2026 (hudson-labs.com)","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"TI's revenue base is structurally diversified: no single customer accounts for more than 10% of sales, TI sells to more than 100,000 customers, and over 40% of revenue comes from outside its top 100 customers — a structural mitigant against single-customer second-sourcing or in-house insourcing risk that would materially move total revenue.","source":"Texas Instruments 2025 Annual Report / Notice of 2026 Annual Meeting (SEC filing, investor.ti.com)","url":null,"excerpt":null,"as_of":"2026-03-01","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"TXN FY2025 Form 10-K (filed with SEC 2026-02-06) discloses TI sells to over 100,000 customers, with roughly half of total revenue coming from customers outside its top 50 — i.e. no material single-customer or small-group revenue concentration disclosed.","source":"Texas Instruments FY2025 Form 10-K, SEC EDGAR (filed 2026-02-06)","url":null,"excerpt":null,"as_of":"2026-02-06","retrieved_at":"20261022","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"TI's FY2025 10-K states more than 80% of 2025 revenue was direct (including TI.com), a continued shift away from distributor-based sales that increases TI's visibility into true end-customer demand and reduces distributor-channel inventory opacity.","source":"Texas Instruments FY2025 Form 10-K, SEC EDGAR","url":null,"excerpt":null,"as_of":"2026-02-06","retrieved_at":"20261022","affects":["decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"TI Q1 2026 results (reported 2026-04-22): automotive revenue grew ~5% YoY to approximately $797M, the first YoY automotive growth after seven consecutive quarters of decline; management attributed the inflection to completed customer destocking and low customer inventory levels across auto/industrial end markets.","source":"TI Q1 2026 earnings release and earnings call, investor.ti.com","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261022","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"TI management cautioned in Q1 2026 commentary that customer inventory depletion appears complete but 'any renewed economic weakness could trigger another destocking phase' — i.e. end-customer macro-demand risk (not a TI-specific customer credit event) has not been eliminated.","source":"TI Q1 2026 earnings commentary (Yahoo Finance / Globe and Mail republication of TI investor materials)","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261022","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Industry commentary argues current oversupply in legacy/mature-node semiconductors (including analog) is masking a structural supply deficit expected to emerge in 2026-2027, driven by inventory correction from prior overordering plus years of capex concentrated in advanced logic nodes (3nm/2nm at TSMC/Samsung/Intel) while mature-node capacity needed for automotive/industrial was underinvested.","source":"Future Digest News (Substack), \"Mature Semiconductors: The Silent Shortage Blocking Everything\"","url":null,"excerpt":null,"as_of":"2026 (approx)","retrieved_at":"20261022","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TI Q2 FY2026 earnings call: above-seasonal Q3 2026 revenue guidance ($5.65B-$6.15B) combined with the company's first price increases 'in years' across analog products; Futurum Group's analysis frames this combination as a signal that the current recovery is a broad industry upcycle rather than a pure inventory-restocking bounce.","source":"Futurum Group, \"Texas Instruments Q2 FY 2026 Earnings Climb on Broad-based Analog Growth\"","url":null,"excerpt":null,"as_of":"2026-07 (approx)","retrieved_at":"20261022","affects":["thesis.H","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TI's six-year, $20B+ capacity buildout (new fabs in Sherman, TX and a retooled embedded-processing fab in Lehi, UT, part of a $60B announced US manufacturing investment) is now complete; 2026 capex guidance was cut sharply to $2-3B (down from peak-cycle spend) even as demand recovers broadly — TI is not re-accelerating capacity investment despite the upturn.","source":"TechTarget / Manufacturing Dive coverage of TI's $60B US semiconductor manufacturing investment; TI Q1/Q2 2026 earnings guidance","url":null,"excerpt":null,"as_of":"2026 (approx)","retrieved_at":"20261022","affects":["thesis.H","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TI Q2 FY2026 results showed broad-based demand recovery: data-center revenue roughly doubled YoY, industrial demand recovered, and automotive re-accelerated — described by Futurum Group as the recovery broadening 'beyond data-center infrastructure and initial industrial restocking' into a company-wide upcycle; gross margin rose 340bp sequentially on higher factory loadings.","source":"Futurum Group, \"Texas Instruments Q2 FY 2026 Earnings Climb on Broad-based Analog Growth\"","url":null,"excerpt":null,"as_of":"2026-07 (approx)","retrieved_at":"20261022","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"TI 與 Silicon Labs 於 2026-02-04 簽署確定協議，TI 以每股 $231.00 現金收購 Silicon Labs，企業價值約 $75 億；雙方於 2026-03-20 向 FTC／DOJ 提交 HSR 併購前申報。","source":"TI.com newsroom \"Texas Instruments to acquire Silicon Labs\" (2026-02-04); MLex \"Texas Instruments, Silicon Labs filed US premerger notifications on March 20\"","url":null,"excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"TI-Silicon Labs 併購案的 HSR 等待期已於 2026-05-22 屆滿並取得美國反壟斷結清（未收到二次請求），美方反壟斷程序已通關。","source":"MLex \"Texas Instruments' $7.5 billion acquisition of Silicon Labs receives HSR clearance\"","url":null,"excerpt":null,"as_of":"2026-05-22","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"截至 2026-06 該併購案在中國市場監管總局（SAMR）的申報尚未被正式受理（filing not yet accepted），中國反壟斷結清仍是交易能否完成的關鍵未決條件；TI 中國營收占比約 20%、Silicon Labs 約 15%，中國政府過去曾用反壟斷審查程序卡關美系半導體併購案。","source":"MLex \"Texas Instruments, Silicon Labs merger filing not yet accepted in China\" (2026-06)","url":null,"excerpt":null,"as_of":"2026-06-01","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"交易預計於 2027 上半年完成，尚待包含中國在內的監管核准及 Silicon Labs 股東同意；除此併購案的申報審查外，未查得針對 TXN 本身業務（既有產品線／市場份額）的獨立反壟斷或拆分調查。","source":"TI investor relations news release \"Texas Instruments to acquire Silicon Labs\"","url":null,"excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國半導體行業協會（CSIA）發布通知，明確以晶圓廠（wafer fabrication facility）所在地認定晶片原產地以適用對美關稅；由於 TI 晶片多在美國本土廠生產，被認定為對中國關稅特別敏感的美系晶片廠之一，TXN 股價當日重挫 9% 至 $142.66，為 2020 年 3 月以來單日最大跌幅。","source":"Investing.com \"US semiconductor manufacturer stocks fall on China tariff concerns\"; barchart.com \"why texas instruments txn stock is falling today\"","url":null,"excerpt":null,"as_of":"2026-01","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國對美進口商品加徵 34% 全面關稅（貿易戰升級），對高度依賴中國需求的美系晶片廠（含 TI）構成利潤率壓縮與市占流失風險；委外代工（outsource manufacturing）的美系晶片廠則被中國官方協會排除在報復性關稅之外，形成自有晶圓廠（IDM，如 TI）相對代工客戶的競爭劣勢。","source":"stocktwits.com \"US Chipmakers Who Outsource Manufacturing To Be Exempt From China Tariffs, Says State-Backed Association\"","url":null,"excerpt":null,"as_of":"2026-01","retrieved_at":"20261022","affects":["thesis.R","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"TI 已提供「特殊產品流程」（specialized product flows），以現有產品組合內的替代料號（alternate part numbers）因應潛在關稅衝擊；同時公司持續推進 300mm 美國本土晶圓廠擴產計畫，目標降低單位成本並提升工業、車用與 AI 應用的供應韌性。","source":"TI.com import details page; Yahoo Finance \"Texas Instruments (TXN) Stock Trades Down, Here Is Why\"","url":null,"excerpt":null,"as_of":"2026-01","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"TI 約 90% 產品自製於自有晶圓廠，晶圓製造據點以美國本土為主；2025-12-17 剛於德州 Sherman 開始量產最新 300mm 晶圓廠（SM1），該園區未來規劃擴充至最多四座聯結晶圓廠。相較多數同業依賴台灣／中國代工，TI 對海外地緣風險區域的製造依賴度明顯較低，形成相對同業的地緣政治隔絕優勢。","source":"TI.com newsroom \"Texas Instruments begins production at its newest 300mm semiconductor manufacturing facility in Sherman, Texas\"; TI.com \"Worldwide manufacturing\"","url":null,"excerpt":null,"as_of":"2025-12-17","retrieved_at":"20261022","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"TI 終端客戶總部設於中國的營收占比約 20%（依 TI 最新年報揭露），為公司在中國市場政策／需求面的主要地緣曝險來源；公司財報並揭露面臨關稅、進出口管制、貿易禁運與制裁等地緣政治貿易障礙的一般性風險敘述。","source":"Texas Instruments 2024 Annual Report / Notice of Annual Meeting (investor.ti.com)","url":null,"excerpt":null,"as_of":"2025","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"TXN Analog segment revenue accelerated from $3.9B (+22% YoY) in Q1 2026 to $4.37B (+26% YoY) in Q2 2026.","source":"TI reports first quarter 2026 financial results (investor.ti.com press release); Texas Instruments Q2 FY 2026 Earnings Climb on Broad-based Analog Growth (Futurum)","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261022","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"TXN Embedded Processing segment revenue grew from $723M (+12% YoY) in Q1 2026 to $788M (+16% YoY) in Q2 2026 — smaller and growing slower than the Analog segment.","source":"TI reports first quarter 2026 financial results (investor.ti.com); Texas Instruments Q2 FY 2026 Earnings Climb on Broad-based Analog Growth (Futurum)","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"Texas Instruments held the largest analog semiconductor market share at 17.8% in 2025, positioning it as market leader ahead of peers.","source":"Analog Semiconductors Market Size & Share 2026-2035 (GMInsights)","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"In the broader analog semiconductor market, unit shipment growth (6.98% CAGR 2026-2031) is projected to outpace revenue growth, indicating persistent price pressure in commodity analog categories.","source":"Analog Semiconductor Market Size, Share & Research Report (Coherent Market Insights / GMInsights)","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"TI is expanding its Sherman, Texas 300mm analog fab with a second cleanroom module, adding 20,000 wafer starts per month by 2028, reinforcing its scale-driven cost-leadership position in analog/power management.","source":"Analog Semiconductors Market Size & Share 2026-2035 — competitive positioning section (GMInsights)","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"TXN's Industrial end market grew ~30% YoY in Q1 2026, driven by depletion of customer inventory and ramp of new systems with higher secular content.","source":"Texas Instruments Q1 FY 2026: Data Center and Industrial Demand Lift Outlook (Futurum)","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261022","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"TXN's Automotive end market returned to mid-teens YoY growth in Q2 2026 (upper-single-digit sequential), an inflection led by China EV/hybrid demand and customers replenishing inventory from unsustainably low levels.","source":"Texas Instruments Incorporated Q2 2026 Earnings Call Summary (Yahoo Finance / Investing.com transcript)","url":null,"excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261022","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"0","claim":"TXN's Personal Electronics end market was flat YoY in Q2 2026 (up low-single-digits sequentially), the weakest of TXN's end markets.","source":"Texas Instruments Incorporated Q2 2026 Earnings Call Summary (Yahoo Finance)","url":null,"excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"+","claim":"TXN's Communications Equipment end market grew ~25% YoY and more than 30% sequentially in Q2 2026.","source":"Texas Instruments Incorporated Q2 2026 Earnings Call Summary (Yahoo Finance)","url":null,"excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#9","axis":"end_markets","section":"coverage","direction":"+","claim":"Data center demand (within Enterprise Systems) surged ~90% YoY in Q1 2026 and TI's data center revenue doubled YoY in Q2 2026, driven by GPU power-delivery content; TI's addressable analog+embedded data center TAM is estimated to grow from $7.5B in 2025 to $12.5B in 2026, with TI's ~$1.5B 2025 data center revenue implying roughly 20% share of that TAM.","source":"Texas Instruments Q1 FY 2026: Data Center and Industrial Demand Lift Outlook (Futurum); Texas Instruments Stock Up 58% This Year as Data Center Revenue Grows 90% Year Over Year (TIKR.com)","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261022","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#10","axis":"end_markets","section":"coverage","direction":"+","claim":"Management guided to \"outgrow the market\" across industrial, data center and automotive markets in both 2026 and 2027, without committing to a fixed numerical growth rate.","source":"Earnings call transcript: Texas Instruments Q1 2026 beats forecasts (Investing.com)","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#11","axis":"end_markets","section":"coverage","direction":"-","claim":"In the competing microcontroller/embedded segment, Infineon Technologies led global market share at 21.3% in 2024, ahead of TXN — unlike its #1 analog position, TXN is not the share leader in embedded/MCU.","source":"What is Competitive Landscape of Texas Instruments Company? (MatrixBCG.com)","url":null,"excerpt":null,"as_of":"2024-12-31","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Texas Instruments 正將 GaN（氮化鎵）晶片產能自 6 吋晶圓廠轉往 8 吋晶圓廠（Dallas 與日本會津擴產），並將 GaN 定位為自身產品線的一部分而非純威脅；GaN 成本已低於 SiC（碳化矽），TI 預期擴產完成後價格優勢將進一步擴大，市場滲透率可望提升。","source":"TrendForce, \"Texas Instruments Plans Large-Scale Transition of GaN Chip Production from 6-inch to 8-inch Wafers\" (https://www.trendforce.com/news/2024/03/25/news-texas-instruments-plans-large-scale-transition-of-gan-chip-production-from-6-inch-to-8-inch-wafers/); Digitimes, \"US chip kingpin Texas Instruments tells reporters about GaN automotive opportunities\" (https://www.digitimes.com/news/a20240307PD206/gan-power-supply-sic-taiwan-texas-instruments.html)","url":null,"excerpt":null,"as_of":"2024-03-25","retrieved_at":"20261022","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"TI 表示 AI 資料中心 800V 高壓供電架構預期於 2027 年開始放量，業界仍在評估多種功率轉換架構（power-conversion architecture）尚未收斂為單一標準，代表資料中心電源設計正處於世代轉換節點。","source":"randtech.com, \"AI Is Colliding With the Analog Semiconductor Supply Chain\" (https://randtech.com/ai-analog-power-semiconductor-shortage/)","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261022","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"2025 年 TI 超過 80% 營收來自直接通路（含 TI.com），較 2022 年約 70% 直接營收比重持續提升；TI 近年持續投資訂單履行服務、庫存計畫、物流與 TI.com 電商能力以強化直接客戶關係，目的是取得更即時的終端需求訊號並提升設計導入（design-win）機會。","source":"Texas Instruments 2025 Annual Report / Notice of 2026 Annual Meeting (https://investor.ti.com/static-files/fc9d9346-cf77-40db-902a-e9961e9c5736); TEXAS INSTRUMENTS INC Form 10-K FY2025 (https://www.sec.gov/Archives/edgar/data/97476/000009747626000059/txn-20251231.htm)","url":null,"excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261022","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"TI 仍維持一個全球性通路商（single worldwide distributor）與少數區域型通路商（如日本市場的 Tokyo Electron Device、Macnica）作為訂單履行輔助管道，而非完全消滅通路商角色；Arrow Electronics、Digi-Key 等仍是關鍵全球通路夥伴。","source":"TEXAS INSTRUMENTS INC Form 10-K FY2024 (https://www.sec.gov/Archives/edgar/data/97476/000009747625000007/txn-20241231.htm)","url":null,"excerpt":null,"as_of":"2024-12-31","retrieved_at":"20261022","affects":["thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TI 於 2026-07-22 公布 Q2 後，Q3 指引營收 $5.65B–$6.15B、EPS $2.23–$2.57，中點高於分析師平均；Q2 實績營收 $5.46B（年增 23%）、稀釋 EPS $2.14；盤後股價下跌。","source":"Benzinga TXN earnings-forecasts／Insider Finance","url":"https://www.benzinga.com/quote/TXN/earnings-forecasts","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Benzinga 統計 2022-10-25 至 2026-07-22 間 TI 共 16 次指引更新，9 次上修、5 次下修。","source":"Benzinga TXN earnings-forecasts","url":"https://www.benzinga.com/quote/TXN/earnings-forecasts","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Investing.com 共識頁：31 位分析師平均 12 個月目標價約 $319.71，高 $400、低 $225；17 買／17 持有／2 賣；頁面最新動作為 2026 年 7 月下旬，可能未反映最新。","source":"Investing.com TXN consensus estimates","url":"https://ca.investing.com/equities/texas-instru-consensus-estimates","excerpt":null,"as_of":"2026-07-31","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"TickerLeague（2026 年 7 月）：共識 Buy，目標價共識約 $296、中位數 $300（僅 6 位分析師樣本）；Morgan Stanley 於 2026-07-20 重申 Underweight。與 Investing.com 的 $319.71 不一致，樣本與來源不同。","source":"TickerLeague TXN estimates","url":"https://tickerleague.com/companies/TXN/estimates","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20261022","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q1 2026 財報（2026-04）後 FY2026 EPS 共識 30 日內上修 19.1% 至 $7.60；2026 資本支出預估年增 12% 至 $3.2B。來源為 Zacks 風格轉載文，可靠度低。","source":"轉載文（ocpartnership.org 等鏡像站）","url":"https://www.ocpartnership.org/expert-time/Texas-Instruments-Incorporated-TXN-Fundamental-Analysis-of-the-Trending-Semiconductor-Stock-Ahead-of-NearTerm-Catalysts-11-2895","excerpt":null,"as_of":"2026-04-29","retrieved_at":"20261022","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"TI 於 2026-02-04 宣布以每股 231 美元全現金收購 Silicon Labs，交易價值約 75 億美元；預計 2027 上半年完成，為 TI 自 2011 年收購 National Semiconductor 以來最大併購。","source":"SEC EDGAR 8-K（TI 併購公告新聞稿附件）；搜尋摘要彙整 Bloomberg Law／Channelchek 報導","url":"https://www.sec.gov/Archives/edgar/data/97476/000119312526036727/d100130dex991.htm","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261022","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"經查 SEC EDGAR 一手紀錄：近 12 個月 10 份 8-K 中含重大項目者 0 份；FY2025 10-K 法律程序章節僅稱日常業務範圍內的查詢與程序，預期無重大不利影響。","source":"SEC EDGAR 8-K 清單與 10-K FY2025 Item 3","url":"https://www.sec.gov/Archives/edgar/data/97476/000009747626000059/txn-20251231.htm","excerpt":"We are involved in various inquiries and proceedings that arise in the ordinary course of our business. We believe that the amount of our liability, if any, will not have a material adverse effect upon our financial condition, results of operations or liquidity.","as_of":"2026-02-06","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"TI 於 2026-02-04 宣布以每股 231 美元全現金收購 Silicon Labs，交易價值約 75 億美元；預計 2027 上半年完成。","source":"SEC EDGAR 8-K 新聞稿附件；Bloomberg Law 報導","url":"https://www.sec.gov/Archives/edgar/data/97476/000119312526036727/d100130dex991.htm","excerpt":null,"as_of":"2026-02-04","retrieved_at":"20261022","affects":["valuation","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"經查 SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 10 份 8-K，含重大項目（含 4.02 非可信賴財報）者 0 份；搜尋亦未見 SEC 調查，僅見 1999 年舊案重編。","source":"SEC EDGAR 8-K 申報清單（近12個月）","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000097476&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-22 至 2026-10-22 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 0 份。","as_of":"2026-10-22","retrieved_at":"20261022","affects":["thesis.R"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TXN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":58.33,"operating_margin_pct":38.07,"fcf_margin_pct":27.53,"rd_intensity_pct":10.71},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TXN","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"2308.TW","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.69,"operating_margin_pct":16.78,"fcf_margin_pct":11.7,"rd_intensity_pct":8.65},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.2308.TW","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"VRT","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":38.04,"operating_margin_pct":19.4,"fcf_margin_pct":25.47,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.VRT","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"ETN","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":35.9,"operating_margin_pct":17.71,"fcf_margin_pct":13.1,"rd_intensity_pct":2.81},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ETN","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"SU.PA","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.SU.PA"},"note":"quarterly_income_stmt 無資料"}],"subject":"TXN"},"financial_history":{"ticker":"TXN","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":20028000000.0,"revenue_yoy_pct":null,"gross_margin_pct":68.76,"operating_margin_pct":51.91,"net_income":8749000000.0,"diluted_eps":9.41,"free_cash_flow":5923000000.0,"fcf_margin_pct":29.57,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":17519000000.0,"revenue_yoy_pct":-12.53,"gross_margin_pct":62.9,"operating_margin_pct":41.85,"net_income":6510000000.0,"diluted_eps":7.07,"free_cash_flow":1349000000.0,"fcf_margin_pct":7.7,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":15641000000.0,"revenue_yoy_pct":-10.72,"gross_margin_pct":58.14,"operating_margin_pct":34.15,"net_income":4799000000.0,"diluted_eps":5.2,"free_cash_flow":1498000000.0,"fcf_margin_pct":9.58,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":17682000000.0,"revenue_yoy_pct":13.05,"gross_margin_pct":57.02,"operating_margin_pct":34.72,"net_income":5001000000.0,"diluted_eps":5.45,"free_cash_flow":2603000000.0,"fcf_margin_pct":14.72,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TXN/TXN_Q3_2026_Earnings_Call_20261021.md）

# Q3 2026 Earnings Call
**Texas Instruments Incorporated** | Earnings Calls | 2026-10-21

**Mike Beckman** (Executives):
Welcome to the Texas Instruments Third Quarter 2026 Earnings Conference Call. I'm Mike Beckman, Head of Investor Relations, and I'm joined by our Chief Executive Officer, Haviv Ilan; and our Chief Financial Officer, Julie Knecht. For any of you who missed the release, you can find it on our website at ti.com/ir. This call is being broadcast live over the web and can be accessed through our website.
In addition, today's call is being recorded and will be available via replay on our website. This call will include forward-looking statements that involve risks and uncertainties that could cause TI's results to differ materially from management's current expectations. We encourage you to review the notice regarding forward-looking statements contained in the earnings release published today as well as TI's most recent SEC filings for a more complete description.
Today, we'll provide the following updates. First, Haviv will start with a quick overview of the quarter. Next, he will provide insight into third quarter revenue results with some details on what we are seeing with respect to our end markets. And lastly, Julie will cover the financial results and give an update on capital management as well as share the guidance for fourth quarter 2026.
With that, let me turn it over to Haviv.

**Haviv Ilan** (Executives):
Thanks, Mike. Let me start with a quick overview of the third quarter. Revenue was $6.1 billion, an increase of 11% sequentially and an increase of 28% year-over-year. Analog and Embedded Processing both grew sequentially and year-on-year. Analog revenue grew 32% year-on-year and Embedded Processing grew 21%. Our Other segment declined 6% from the year ago quarter.
During the quarter, we saw broad demand with revenue growth across all end markets and regions. Secular growth of semiconductor content is continuing alongside a strong cyclical recovery. We are working closely with our customers to support them during this time of increased demand. We are executing to our long-term manufacturing plan and our investments have positioned us to ramp our factories to support revenue growth. Now I'll share some additional insights into third quarter revenue by end market.
First, industrial increased more than 40% year-on-year and was up about 10% sequentially. Automotive increased mid-teens year-on-year and increased about 10% sequentially. Data center was up about 95% year-on-year and grew about 20% sequentially. Personal electronics was about flat year-on-year and grew upper single digits sequentially. And lastly, communications equipment grew both year-on-year and sequentially.
With that, let me turn it over to Julie to review profitability and capital management.

**Julie Knecht** (Executives):
Thanks, Haviv, and good afternoon, everyone. As Haviv mentioned, third quarter revenue was $6.1 billion. Gross profit in the quarter was $3.9 billion or 64% of revenue. Sequentially, gross profit margin increased 280 basis points. Operating expenses in the quarter were $1 billion. On a trailing 12-month basis, operating expenses were $4 billion or 19% of revenue. Operating profit was $2.9 billion in the quarter or 47% of revenue, and it was up 73% from the year ago quarter. Net income in the quarter was $2.4 billion or $2.62 per share. Earnings per share included a $0.01 reduction not in our original guidance due to discrete tax items.
Let me now comment on our capital management results, starting with our cash generation. Cash flow from operations was $3.4 billion in the quarter and $9.9 billion on a trailing 12-month basis. Capital expenditures were $463 million in the quarter and $2.6 billion over the last 12 months. Free cash flow on a trailing 12-month basis was $8.4 billion, up from $2.4 billion in the third quarter of 2025. Free cash flow in the trailing 12 months includes $1.6 billion of CHIPS Act incentives, which includes both the investment tax credit and direct funding. In the quarter, we paid $1.3 billion in dividends.
In September, we announced we would increase our dividend by 7% to $1.52 per share, marking our 23rd consecutive year of dividend increases. This reflects our continued commitment to return all free cash flow to owners over time. In total, we returned $5.8 billion to our owners in the past 12 months. Our balance sheet remains strong with $8.1 billion of cash and short-term investments at the end of the third quarter. In the quarter, we repaid $500 million of debt. Total debt outstanding is $13.65 billion with a weighted average coupon of 4.11%. Inventory at the end of the quarter was $4.7 billion, up $67 million from the prior quarter, and days were 194, down 2 days sequentially.
Turning to our outlook for the fourth quarter. We expect TI's revenue in the range of $5.8 billion to $6.3 billion and earnings per share to be in the range of $2.45 to $2.79. We expect our effective tax rate to be about 13% in the fourth quarter. And for 2027, we expect it to be about 13% to 14%. In closing, we will stay focused in the areas that add value in the long term. We continue to invest in our competitive advantages, which are manufacturing and technology, a broad product portfolio, reach of our channels and diverse and long-lived positions. We will continue to strengthen these advantages through disciplined capital allocation and by focusing on the best opportunities, which we believe will enable us to continue to deliver free cash flow per share growth over the long term.
With that, let me turn it back to Mike.

**Mike Beckman** (Executives):
Thanks, Julie. Operator, you can now open the line for questions. [Operator Instructions] Operator?

**Operator** (Operator):
[Operator Instructions] And our first question comes from the line of Joe Moore with Morgan Stanley.

**Joseph Moore** (Analysts):
I was a little surprised that the gross margins kind of incremental gross margins of about 90% on incremental revenue. I know the long-term target is lower than that. Can you just give us a sense for what went right there and how sustainable that may be?

**Julie Knecht** (Executives):
Sure. Thanks, Joe. Yes, our margins in third quarter were really driven by higher revenue. That's the largest reason for that increase. But we also did have some benefit from pricing, loadings and some product and end market mix.

**Mike Beckman** (Executives):
Do you have a follow-up, Joe?

**Joseph Moore** (Analysts):
No, I'm good. So that looks like about comparable gross margins embedded in the guidance. Is that kind of the right way to think of it?

**Julie Knecht** (Executives):
So I think over the long term, the way to model continues to be looking at 75% to 85% ex-depreciation fall-through. It's better -- it's easier to look at that more over a longer time horizon, so year-over-year. But of course, there's puts and takes in this. For modeling, I would also share that OpEx for the fourth quarter, we're expecting to be flat to slightly up. Acquisition charges should look about similar to what we saw in third quarter, same with net OI&E.

**Operator** (Operator):
Our next question comes from the line of Harlan Sur with JPMorgan.

**Harlan Sur** (Analysts):
Great job on the quarterly execution. Both short time -- both short lead time orders and longer-term duration orders have been positive for the TI team over the past few quarters. Lead times, I assume, are probably expanding a bit. So you're getting a bit more orders placed further out in time as well. Did the TI team drive another quarter of positive book-to-bill in Q3? And was the order activity pretty broad-based?

**Haviv Ilan** (Executives):
Harlan, this is Haviv. Let me say a few words, and I'll let Mike offer some more comments. So look, we are seeing, as I said, the broadening of the demand coming across the 3 main markets that we focus on for the long term, industrial, automotive and data center. But in general, demand was strong across the board, across markets, sectors and regions. That does put pressure on lead times, but I think they may be ticked a little bit higher. I'll let Mike comment. But I still believe that TI is best positioned to support that growing demand. I think we are still the most competitive supplier in terms of lead time.
Mike, I don't know if you can offer anything else here?

**Mike Beckman** (Executives):
I think you characterized it right. And I'd just also add the investments that we've made in inventory and capacity do position us to support growing demand, and we'll continue to ramp our factories to support revenue growth moving forward.
Do you have a follow-up?

**Harlan Sur** (Analysts):
I appreciate the answer. Last quarter, Haviv, you talked about the potential for broader positive pricing initiatives as you hold your annual pricing negotiations for next year. That would overlay not just on your Analog and Power products, but also on your Embedded products as well. Can you give us an update here? I mean, industry supply dynamics feel like they're getting worse, not better. TI is in a great position to support customers' supply requirements. And I think they do value the team supply capability. And I assume they're willing to pay a premium for the assurance and predictability you offer, but I wanted to get an update from you there on annual pricing negotiations.

**Haviv Ilan** (Executives):
Yes. First, a high-level picture, Harlan, as you mentioned, there is a stronger demand environment right now. And if you look at the area of foundational chips, as I call it, but specifically Analog, there hasn't been a lot of addition into capacity in the last 4 years since the previous peak of the market during the COVID days.
So especially if you do care about geopolitically dependable capacity, meaning usually factories outside of China and Taiwan. So in this case, TI has a good position. We are seeing our customers value our investment and also our capacity to continue to grow them, not only in the next quarters, but also in the foreseeable future. So that's a good characterization of the situation we are in.
Regarding pricing specifically, look, most of our pricing discussions are done once a year with our customers, but we did see some areas in the middle of the year where we had the opportunity to talk to customers that wanted more supply more urgently. And in this case, and Julie indicated in her answer, we did see some price movement, I would say, mainly on the Analog side in the second half. I would just characterize it the second half of 2026 after a flat pricing environment year-over-year in the first half of '26.
So we are seeing a little bit of an uptick, not very significant for this year. For '27, yes, we are now engaged in the discussions you just mentioned. We are looking at the customers' demand and what type of supply they want to guarantee, if you will, or to get supported from TI, and that has a pricing element to it. So I think we will report more of it when we provide our results, mainly our guidance during the January call.

**Operator** (Operator):
Our next question comes from Stacy Rasgon with Bernstein Research.

**Stacy Rasgon** (Analysts):
I wanted to ask about the end market outlook that's embedded in guidance. Usually, Q4 just seasonally is down, I don't know, mid-single to high single, maybe even more sometimes. And I get it, calculators and personal electronics, typically. You're guiding flattish, which is well above. It will be one of your stronger Q4s in quite a while probably since the COVID cycle. What is embedded there, the puts and takes on end markets given those sort of typical seasonal patterns? And what are you seeing across the markets now that's driving things stronger?

**Haviv Ilan** (Executives):
Stacy, I'll take a stab at it again. We're not going to guide by market. As you know, we don't. But I will just give a little bit of color. The data center market, it's a market that we see strong secular growth. I don't think it's influenced by seasonality. The demand continues to be strong and growing. So -- and it's just a bigger part of our business now. I think it was about 13% of revenue in Q3 or so. So I think just you see that coming in and just helping, if you will, the transition from Q3 to Q4.
But on top of it, I'm very excited about what we are seeing on the industrial market. We are seeing a very strong momentum in industrial across the sectors, but specifically in areas like aerospace and defense, energy infrastructure, test and measurement, the robotics sector. So this is where we see a combination of secular growth, but also sequential or cyclical recovery, I would say. So this is why we were seeing an above seasonal forecast from TI. We also saw the automotive customers waking up, if you will, with higher demand in Q3, and I think that may continue into Q4. So again, the top 3 markets, industrial, automotive and data center, are the ones that are driving our guide into Q4.

**Mike Beckman** (Executives):
Do you have a follow-up, Stacy?

**Stacy Rasgon** (Analysts):
I do. I wanted to ask about CapEx. So you've been talking about you'll be near the higher end of the $2 billion to $3 billion range for the year. And are you still going to be tracking there in the one quarter that we have left? And I guess, in addition to that, you talked about continuing to invest in manufacturing to support demand. So like how do we think about CapEx in '27 relative to '26, given that statement?

**Haviv Ilan** (Executives):
Yes. Let me start with '26 right now, Stacy. And of course, we'll give some more color during our February call for capital management about what we're seeing. But high level, you're right, we are aiming to continue to invest right now in '26, somewhere between $2 billion and $3 billion. And yes, we want to aim higher, but also we are seeing lead times extending on tools and everything, especially on the back-end side. So that is very tactical situation, but we do want to expand capacity.
As you know, we have plenty of clean room, and we are seeing strong demand, leaving -- this quarter, we grew in the high 20s. So you do want to make sure you continue to fill that clean room with tools, both on the back end, but also later on, on the front-end side. So we are leaning in. And again, now when you talk about CapEx, it's when tools are coming in, delivered by our suppliers, and that's what influences more or less the result. But you should expect somewhere between $2 billion to $3 billion this year and maybe on the higher end if we get that execution as planned.
Now regarding '27, I won't say anything right now about the numbers, but I do think it's a function of demand and what our aspiration of growth, Stacy. I think we have given a framework at the time of what CapEx will do as a function of the expected longer-term revenue growth. Of course, we are investing ahead of demand, right? So there is a certain CapEx level to support a 10% growth versus a higher CapEx plan to support a mid-teens growth, for example. And this is where we want to provide some more color in our February call.
I will say that we have the -- we are in a position to control our destiny. We have taken care of the long lead time investments on clean rooms, including all the subfab and all the -- to be fair, the equipment that takes right now a very long time to get and build and get qualified. So I'm very excited about that. We do have the slots reserved for '27 and beyond, and we are going to modulate the incoming rate based on the revenue growth we would like to support, okay?

**Operator** (Operator):
Our next question comes from the line of Chris Caso with Wolfe Research.

**Christopher Caso** (Analysts):
First question was to dig in a little more on the industrial market. And that market has been in recovery for some time now. You're seeing it up 40% year-on-year in the quarter. I guess the question is, what's your level of conviction that when this recovers? How much of that recovery do you think was -- has been driven by cyclical factors as opposed to secular factors such as the growth in some of those individual segments?

**Haviv Ilan** (Executives):
Yes. So let me start and Mike, maybe you can offer some more color on the sectors inside industrial. But high level, the excitement I have about industrial is growing very fast, but only now in Q3 2026, it reached the same level of revenue we had in Q3 2022. So this is the first time we created a new peak in industrial after 4 years.
I do believe that systems that are being designed by our customers 4 years later than the COVID peak are much more rich with content. We are seeing end equipment by end equipment, sector by sector that there is just more content per system as customers want to achieve higher precision, higher speed, higher quality, more throughput, whatever they want to drive, right? So that is there.
I also believe our portfolio has done very well in terms of -- we've built more and more parts in the last several years, invested in R&D, and I think we won a larger share per system based on our portfolio. So I'm excited about that as well. Now there is also some secular areas of growth like aerospace and defense and also data center-induced sectors. I'll let Mike comment there about the different sectors. Some of them, by the way, have not reached their previous peak yet. So we are in the early innings.

**Mike Beckman** (Executives):
Right. So some of the sectors, as you probably know, that have had industry level unit demand like aerospace and defense or the ones that are more closely adjacent to data center, like energy infrastructure, test and measurement, make all new highs over time. But even areas like industrial automation that are going through recovery have also had, as Haviv, you described, 4 years of content increase, gen-to-gen secular content growth. So as we look at the industrial end market, we see opportunity ahead there. And as Haviv mentioned, it's just now reached a little bit above its previous peak. But again, that's 4 years of content expansion. So we look forward to serving that market well in the quarters ahead.
So do you have a follow-up?

**Christopher Caso** (Analysts):
I do. The follow-up question is on Embedded. And now that, I guess, the second Lehi shell will be ready by the end of the year. Maybe talk about how you intend to deploy that as you go into next year? And as you said, it does seem like industry capacity is getting tighter. What benefit does that bring to you? What are your plans for next year? And does that have any margin impact?

**Haviv Ilan** (Executives):
Yes. So on the Embedded side, I am -- we are seeing that our investment in Lehi, Lehi 1 and Lehi 2 is extremely beneficial. On Lehi 1, as you remember, we have transferred a lot of our foundry-based business into Lehi 1, but we still have plenty of clean room in Lehi 1. So we are going to grow into that. That will carry us at least in the -- in the coming quarters. But we do have Lehi 2, as you mentioned, there to continue to grow Embedded at the rate which demand will indicate. So we are right now looking at the numbers.
I think that the Embedded business in general, I think this is not only a TI comment, but in terms of the cyclical recovery, I would call it maybe a year later than Analog. We saw that -- the Embedded business peaked in 2023, while Analog for TI -- while Analog peaked in 2022. I also believe that the supply-demand mismatch is higher in Analog because some of the Analog supply, to be fair, went offline in the last few years and more is coming out as some of the foundries are transitioning their supply base to support non-Analog portfolio parts. So with that sense, I think the pressure is now higher, and this is why you're seeing higher growth on Analog.
Having said that, Embedded is well positioned. Our portfolio is growing. We have a clean room in LFAB1. We have the shell in LFAB2 that is in the last stages of completion. So we can modulate now tool installations according to what demand says. Last but not least, I want to mention our plan with the Silicon Labs acquisition. That's another clean room that will serve the transitioning of the portfolio that right now is running in foundries into -- again, into Lehi.
From a gross margin perspective, we are seeing a strong progress. I think we've seen it in the last several quarters. Julie, right? Is it a couple of points per quarter that you are seeing lately?

**Julie Knecht** (Executives):
Yes.

**Haviv Ilan** (Executives):
And I think about 10 points year-over-year or something. So I do see that the Embedded has room to grow in the sense of not only top line growth, but also gross margins as well.

**Operator** (Operator):
Our next question comes from the line of Joe Quatrochi with Wells Fargo & Company.

**Joseph Quatrochi** (Analysts):
I wanted to ask about the auto demand commentary you provided talking about you're seeing customers, kind of, wake up a little bit. Can you give a little bit more color? Is that broad-based demand that you're seeing? And are you seeing customers add more inventory? And is that across Analog and Embedded or more concentrated?

**Haviv Ilan** (Executives):
Yes, I will start. But in automotive, I think I will describe the demand we are seeing in automotive as such that keeping -- demand is coming in pretty strong in Q3. We did see a nice sequential growth. We are seeing mid-teens year-over-year growth. But I think customers have not had -- not kept a lot of inventory on their side. So when they saw maybe demand growing, maybe a little bit of more EV as fuel prices went up, they were not well positioned compared to customers we've seen in other markets. So we are now supporting these customers as they're trying to ramp their production.
I don't see any inventory buildup. On the contrary, I wish they had a little bit more. But we are positioned to grow. Of course, the fabs are, you cannot switch -- flip a switch, sorry, to get the output at the right mix immediately. And this is where we help some customers with the existing inventory we've built ahead, but some of the parts are more unique, and we need to react to customer demand. So that's what I'm seeing right now.
In terms of region, can you add a little bit, Mike?

**Mike Beckman** (Executives):
Yes. So similar to last quarter, you may recall that we saw China and the U.S. averaging up the overall growth. We continue to see that in third quarter as well. And the comment around EV mix, you can see it clearly in our sectors as well. So the hybrid electric and powertrain systems sector grew about twice as fast as the overall did. So that just gives you a sense of the mix that has shifted toward EV inside of that.
So with that, do you have a follow-up?

**Joseph Quatrochi** (Analysts):
Yes. And then just as we think about it, I think you talked about back-end tools, lead times kind of starting to extend and things, capacity, obviously tight. Does that change any of your plans and how you're thinking about just moving more of your capacity on the back-end side to internal? Are you trying to flex some of your external capacity a bit more just given the pretty significant increase in demand you're seeing?

**Haviv Ilan** (Executives):
Yes. I think I commented before earlier this year, we have done it throughout the year. So we are not getting as much as we wanted from our OSAT partners. And I think it's also just tightness of supply, as you mentioned. So we do have a new site in Malaysia that we are ramping very quickly. It's our largest AT site newly built. And I'm very glad we have it. The parts are being qualified and ramped. So we can continue and increase capacity every quarter, thanks to the clean room we have.
The rate at which we could go is a function of how quickly we add tools, and that's also a function of the demand, I would say. But in general, I'm very pleased with our situation, both front end and back end because we control our destiny here. And we have done the work during the down cycle, again, when lead times are very short on this type of equipment to get ahead and to be ready for a range of scenarios. This scenario right now is a very strong demand scenario.

**Operator** (Operator):
Our next question comes from the line of Tore Svanberg with Stifel.

**Tore Svanberg** (Analysts):
Congratulations on the results. Just zooming in a little bit on data center, I think it almost doubled year-over-year. I think in the past, you've talked about your exposure to data center still kind of being more building block components, but I do know you have some newer products that are starting to get designed in. So how should we think about that in the context of the almost double year-over-year growth rate?

**Haviv Ilan** (Executives):
Yes. Look, I'm very excited about the market in the sense of -- you guys know exactly what's going on there. But what I would like to share is that we see a very high breadth of opportunity, and we are continuing to invest. I mean, customers want new solutions to get more -- I mean, these are very expensive assets if you think about the compute rack or networking rack and it needs a lot of telemetry and cooling, and efficiency is critical. Power density is critical.
So we are seeing customers being very, very innovative on how they add parts that are mainly coming from our portfolio of foundational chips of Analog and Embedded chips to do all of that. So just a growing opportunity in terms of diversity of part numbers. We reviewed it earlier this week, and we have about 10,000 different GPNs or generic part numbers that we are selling into this market, and it's growing every quarter. So that's a very exciting opportunity.
Now our focus is, again, we are a company that is trying to -- breadth of our portfolio is one of our competitive advantages. But of course, we also pay attention to the more application-specific sockets. We have developed the technology for that. I think I've mentioned it. It's now early ramps in Sherman. I think the execution is going well. So I'm excited about continuing to expand our portfolio in data center, assuming the investments in data center continues in the U.S. And by the way, it's not only in the U.S. We are seeing it worldwide, but the U.S. is leading.

**Mike Beckman** (Executives):
You have a follow-up, Tore?

**Tore Svanberg** (Analysts):
Yes. So in industrial, which is a little more than 1/3 of your revenue, I know you talked about the cyclical growth and the secular growth. But I'm just also curious, if you look at all the subsegments there, how much of that, let's say, 35% of revenue is potentially being impacted by the data center build-out as well?

**Haviv Ilan** (Executives):
So I think we have about 9 or 10 sectors over there in industrial. The last one is kind of what we call other, all other end equipment. But of the 9, I think 2 are very much data center-specific, energy infrastructure and also test and measurement. But I think I see a lot of robustness there. I mean, people are building memories and GPUs for the foreseeable future. They need to test them. That has been a very fast-growing sector for us, and we are doing well over there.
And then the energy infrastructure, I think that the world is rebuilding its grid, and it's a very -- it's -- the content is very rich with semiconductors. So that has been a very good sector growth for us. I think data center influences it, but the world needs more energy, I think, in general, if you think about automation and later on physical AI and robotics and aerospace and defense, everything needs more energy, and I think that's going to continue. So I'm very excited about the progress over there.
Now we are seeing, as Mike mentioned before, we just see other secular trends that are not -- I don't think they may be related to data center because they help accelerate them. But what's going on in the aerospace and defense with autonomous end equipment, if you will, that are very content-rich in the type of parts we make. Very early on the robotics side, but I think '27 is going to be a great year of ramps. Our content over there is actually -- for example, per humanoid is very high. I would say, somewhere between $500 to $1,000 per content for TI won on this type of systems. So I don't know how many they'll build next year, but definitely, the demand is -- they want to grow.
So all of that is putting a lot of -- providing a lot of tailwind on our industrial business, which I'm excited about because it also helps you. There was a question before on margins. This is our best market in terms of diversity and longevity, but also in terms of margins. So a very lucrative market.

**Operator** (Operator):
Our next question comes from the line of William Stein with Truist Securities.

**William Stein** (Analysts):
I'm hoping you can comment on customer inventory levels and their ability to complete kits. We've heard some feedback from industry contacts that this is becoming a challenge the way it was a few years ago in the so-called golden screw era. I wonder to what degree you're seeing this? And what is your ability to perhaps help customers deal with those challenges?

**Haviv Ilan** (Executives):
Yes. First, we all hear -- I lived through the previous up cycle during the COVID days. I would not compare the situation. I think also we are earlier right now in terms of where the cycle is. So we'll have to see. But again, from a TI perspective, we are much better prepared in terms of -- we have -- we can grow our capacity every quarter, and we've built inventory during the down cycle.
Now as you have a very rapid fast growth in some of the customers or markets and especially where customers have not prepared and did not have enough inventory on their side, you can run into situations like that. I think I gave an example before on the automotive market. That's the one place I would say that I see it right now versus in capital -- in the COVID cycle, we did see a much broader situation across almost every customer or every end market. So I would not compare them yet.
I will say that, yes, they have come for help many times. We have been the solution many times right now in other markets. So some of our industrial customers, some of our data center customers have asked for help. And many times, we had the inventory and could also commit capacity or growth into '27 and beyond. So we are seeing early anecdotal feedback that we can help our customers, but we need to see how the situation develops.
I will say, as I said before, in terms of capacity addition outside of China, mainly on the Analog side, it's not -- we don't see a lot of clean room and a lot of new capacity added in the last 4 years. And as I mentioned, the cycle time to build from moving dirt to getting output from a fab, it's about 4 years, not to mention about full ramp of the fab. So I think TI is in an advantaged position here versus the rest of the market.

**Mike Beckman** (Executives):
I do think that customers in the context of the question on kitting and making sure they have all the products they need, they will come to us and say, I need to make sure I have what I need from your portion to meet -- as I get what I need and maybe another area where they're having a challenge getting it. So this is all part of what we're seeing in our markets overall. But I think we are in a good position to be able to help and work with our customers to help them as they grow.
So Will, do you have a follow-up?

**William Stein** (Analysts):
Yes. I appreciate that helpful answer. And the next one, you might have discussed it already, but can you talk about where lead times might have changed in the last quarter and what your customers' willingness and ability to place backlog with you has been? Has the backlog duration extended materially in the last quarter?

**Mike Beckman** (Executives):
So I'd characterize the backlog as consistent with the overall demand environment that we're seeing. And we have seen an uptick in lead times. And there are areas where you'll see just as you would expect in an environment like this, where there may be more or less tightness in certain areas. But in terms of where we are from a lead time perspective, we're competitive right now. And again, we're in a position where we can make investments into the clean room and the assembly and test facilities that we have to be able to support growth for our customers, and we'll continue to ramp those as we move into this quarter and beyond.

**Operator** (Operator):
Our next question comes from the line of Nabeel Aziz with Rothschild & Company.

**Nabeel Aziz** (Analysts):
I just had a question on supply-demand tightness through the quarter and what you're seeing in terms of socket wins and your engagements with customers there and whether you've started to see incremental market share gains through the quarter?

**Haviv Ilan** (Executives):
Yes, Nabeel, I think we -- when it goes to market share, we don't like to measure it. Of course, we look at the results internally, but I think we should look at it through the cycle as -- again, if we are indeed better positioned than some of the competition to support demand and if demand continues, we should be able to translate it to market share gains, but that -- we cannot measure it yet. So I think we have to wait through the cycle, see when the next peak is. It will arrive one day and then see where we are. But I'm pleased with the momentum we are building. I'm pleased with the ability to continue to ramp our supply, and let's see how we do over the long term.

**Mike Beckman** (Executives):
You have a follow-up, Nabeel?

**Nabeel Aziz** (Analysts):
Yes. Just a follow-up on the back-end tool comments. Could you just confirm, is there a potential that back-end tool availability could at all bottleneck your growth and whether that is a gating factor for you over the next couple of quarters?

**Haviv Ilan** (Executives):
I don't want to talk about the gating items because the gate is when you don't have the clean room, right? A gate when you now are stuck for a couple of years to build your shell and to build the clean room and all the infrastructure behind it. We don't have a gating item like that. I think this is just simple blocking and tackling, as we say, or execution of getting the equipment on time. Our suppliers also need -- their supply chain is complex, and they have to get through it. It's just a period of high demand all over. And everybody is going through their challenges, but there is a very large opportunity to expand capacity, and we are.
I would say that I don't see -- between front end and back end, we are going to be balanced. Of course, the higher investment we need to make when you think about CapEx for the longer term is always on the front end. This is where the CapEx is more expensive and also where the lead times are always longer with the supply chain over there. And this is why we are not playing only in '27 and '28. We are actually thinking through the rest of the decade, what is our plan and how are we going to slot our future tools and even new clean rooms so we can continue to support a range of scenarios that the market may present to us.

**Operator** (Operator):
And our last question comes from the line of Vijay Rakesh with Mizuho Securities.

**Vijay Rakesh** (Analysts):
Just a quick question. I see your data center side is growing pretty strongly. It's almost like a $2.5 billion run rate this year annualized. Just wondering, as we look at '27, do you expect that growth rate to continue and double from here? And a quick follow-up.

**Haviv Ilan** (Executives):
Yes. I mean, we are watching, like everyone, the CapEx investment into the data center market. It doesn't have -- it doesn't signal right now any -- we are not seeing any slowdown. We are seeing continuing demand, actually growing demand. As I mentioned before, our portfolio is growing. That's my -- that's where I'm excited about our investment. We are not sitting still. We are creating new parts. We are continuing to attack new subsystems. So we want to continue not only to grow with the market, but also play more sockets and ultimately gain market share. So, so far, so good. We'll see how the demand continues to develop into the next year.

**Mike Beckman** (Executives):
And Vijay, just zooming out, when there's more power, there's more opportunity for TI. When there's more power density, there's more opportunity for TI. When there's higher voltages, there's more opportunity for TI. And obviously, these are things that are all being worked on very heavily in this end market. And again, we look forward to supporting.
So do you have a follow-up?

**Vijay Rakesh** (Analysts):
Agreed. And just a quick one. On the commentary on the EV side, is this more of a -- does TI have more exposure on China, kind of China export EV market as well? Like how would you characterize the EV strength just globally across regions?

**Haviv Ilan** (Executives):
No. As we -- I talked many times over in the last several years, China industry for the automotive industry and especially EVs is leading in many ways, and they are not only building for their domestic market. This is why a supplier like TI was always something that was very, very important to them. We are a global company, very diverse supply chain across the globe. And we've continued to design in our parts into their systems.
I think I am excited about the fact that China is growing faster than their export business because these are usually just in terms of content, just higher content and also higher share for us there. So that also is driving the growth. Mike has mentioned before that automotive business for TI in Q3 was driven by China and the U.S., and we are excited about our position there.

**Mike Beckman** (Executives):
All right. With that, I'm going to have Haviv close this out for the call.

**Haviv Ilan** (Executives):
Okay. So let me wrap up with what we've said previously. At our core, we are engineers, and technology is the foundation of our company. But ultimately, our objective and the best metric to measure progress and generate value to our owners is the long-term growth of free cash flow per share. Thank you, and have a good evening.

**Operator** (Operator):
Thank you. And this concludes today's conference, and you may disconnect your lines at this time. We thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TXN_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜Rafael Lizardi｜guidance：CFO 給 Q3 營收區間（56.5–61.5 億美元）（原話："We expect TI's revenue in the range of $5.65 billion to"）
- 2026-07-22｜Rafael Lizardi｜guidance：Q3 EPS 區間 2.23–2.57 美元（原話："earnings per share to be in the range of $2.23 to $2.57."）
- 2026-07-22｜Haviv Ilan｜guidance：CEO 稱 Q3 高於季節性的貢獻來自所有市場（原話："I expect strong demand across the board."）
- 2026-07-22｜Rafael Lizardi｜margin：Q2 毛利率 61%，季增 340 bp（原話："or 61% of revenue. Sequentially, gross profit margin"）
- 2026-07-22｜Rafael Lizardi｜margin：Q2 EPS 含 0.05 美元未列入原財測的離散稅務利益（原話："Earnings per share included a $0.05 benefit not in our"）
- 2026-07-22｜Rafael Lizardi｜margin：Q3 OpEx、其他收支、併購費用預期與 Q2 持平（原話："you should expect all of those to be flat second quarter"）
- 2026-07-22｜Julie Knecht｜margin：新任 CFO 稱 Q3 增量毛利率（不含折舊）70%–85% 為建模參考（原話："that 70% to 85% is a good placeholder."）
- 2026-07-22｜Haviv Ilan｜margin：CEO 補充 Q3 毛利率不會持平，應略高（原話："But it shouldn't be flat. It should be a little higher."）
- 2026-07-22｜Mike Beckman｜margin：資料中心毛利率目前與公司平均相近，不預設偏向（原話："it's been pretty similar to the overall corporate average."）
- 2026-07-22｜Haviv Ilan｜customer：資料中心 Q2 年增一倍、季增約 20%（原話："Data center doubled year-on-year and grew around 20%"）
- 2026-07-22｜Haviv Ilan｜customer：工業 Q2 年增約 30%、季增約 10%（原話："increased around 30% year-on-year and was up about 10%"）
- 2026-07-22｜Haviv Ilan｜customer：車用需求於季內逐步堆高，以中國為首（4 月電話會時能見度不同）（原話："It built up as we went through the quarter, led by China."）
- 2026-07-22｜Haviv Ilan｜customer：管理層稱處於範圍很廣的循環起點（原話："we are in the start of a cycle that is very, very broad."）
- 2026-07-22｜Haviv Ilan｜customer：個人電子 Q3 預期季增但幅度低於常態，客戶受缺貨壓力（原話："We are seeing challenges in PE as some shortages are"）
- 2026-07-22｜Haviv Ilan｜customer：工業仍低於 2022 年高峰約 5–6 個百分點（原話："5 or 6 points"）
- 2026-07-22｜Haviv Ilan｜customer：工業復甦歸因於客戶庫存去化結束與新世代系統（原話："New systems that were designed in the last 4 or 5 years."）
- 2026-07-22｜Haviv Ilan｜guidance：Q3 成長絕大部分為出貨量，漲價貢獻幾乎不顯著（原話："the vast majority of it is just unit growth and"）
- 2026-07-22｜Haviv Ilan｜risk：上半年價格持平（符合先前預期）（原話："And as we predicted, pricing was stable"）
- 2026-07-22｜Haviv Ilan｜commitment：管理層稱已開始執行漲價（上季為討論可能性）（原話："we have started executing price increases, yes."）
- 2026-07-22｜Haviv Ilan｜commitment：漲價逐客戶談判，Q3 起部分生效並延續至 Q4 及明年（原話："Some of it will start to play in, in Q3"）
- 2026-07-22｜Haviv Ilan｜risk：交期原低於 13 週（原話："They were below 13 weeks, in Q2"）
- 2026-07-22｜Haviv Ilan｜risk：交期小幅拉長約數週，因需求成長（原話："Maybe a couple of weeks higher"）
- 2026-07-22｜Mike Beckman｜guidance：訂單與遠期 backlog 於季內皆增加（原話："we did see backlog build"）
- 2026-07-22｜Mike Beckman｜guidance：backlog 增加已反映在財測中（原話："And it's reflected in the guide."）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：2026 資本支出維持 20–30 億，不偏向低端（原話："I would not skew it or bias it lower on the lower end"）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：未來資本支出偏重美國以外的封測，該部分無 ITC（原話："disproportionately placed in the assembly test operation"）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：資本支出經驗法則：以成長率 1.2 倍估算資本密集度（原話："the framework we've given you, 1.2x the"）
- 2026-07-22｜Julie Knecht｜capital_allocation：產能：Q2 稼動率提高並於季內持續上升（原話："So our loadings did increase from first to second quarter."）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：TTM 自由現金流含 16 億 CHIPS Act 獎勵（原話："cash flow in the trailing 12 months includes $1.6 billion"）
- 2026-07-22｜Rafael Lizardi｜capital_allocation：庫存 46 億美元（天數 196 天，季減 13 天）（原話："Inventory at the end of the quarter was $4.6 billion"）
- 2026-07-22｜Haviv Ilan｜commitment：自由現金流框架（營收 200 億對 80–90 億、220 億對 90–100 億）仍有效（原話："So that framework is still valid, Jim."）
- 2026-07-22｜Haviv Ilan｜commitment：目標為超越市場而非設定資料中心成長率，2026 預期達成（原話："to outgrow the market. I believe we will do it in 2026,"）
- 2026-07-22｜Haviv Ilan｜commitment：潔淨室與產能足以支應未來約三年；2027 資本支出細節留待二月（原話："we are good for the next 3 years, okay?"）
- 2026-07-22｜Julie Knecht｜commitment：Silicon Labs 交易預計明年上半年完成（原話："We still expect to close in the first half of next year."）
- 2026-07-22｜Haviv Ilan｜competition：稱競爭對手 52 週交期對 TI 是新設計機會（原話："competition talks about lead times that are 52 weeks away"）
- 2026-07-22｜Haviv Ilan｜competition：稱可能在較大內容量機會上拿到市占（需時間驗證）（原話："we grew share on the larger content opportunity"）
- 2026-07-22｜Haviv Ilan｜competition：800V 架構視為 TAM 擴大、轉換級數增加（原話："higher growth of the TAM, more conversion stages"）
- 2026-07-22｜Haviv Ilan｜product：資料中心優勢含供貨能力，強調地緣政治可靠產能（原話："geopolitical dependable capacity like we hold"）
- 2026-07-22｜Haviv Ilan｜risk：Q3 成敗在執行：提高產能稼動並追逐需求（原話："We are ramping our factories. We are going after it."）

### TXN_Shareholder_Analyst_Call_Texas_Instruments_Incorporated_20260416.md
- 2026-04-16｜Unknown Attendee（Chevedden 代表）｜risk：股東提案代表指出 TI 召開股東臨時會需持有 25% 流通股（治理面，非營運面）。（原話："requires the backing of 25% of all shares outstanding"）
- 2026-04-16｜Unknown Attendee（Chevedden 代表）｜commitment：提案人主張以書面同意讓股東在年會之間採取行動（提案 4）。（原話："take action between annual meetings"）
- 2026-04-16｜Haviv Ilan（Chairman）｜commitment：董事長宣布初步投票結果：公司提案全數通過，股東提案未通過。（原話："all company proposals have passed"）

### 問答異常語氣（迴避／改口／保留）
- TXN_Q2_2026_Earnings_Call_20260722.md｜問：Stacy Rasgon 追問個人電子 Q3 年增是持平或下滑｜答法：IR 表示不提供各終端市場財測，僅重申 Q2 觀察，未回答方向
- TXN_Q2_2026_Earnings_Call_20260722.md｜問：Vivek Arya 詢問 2027、2028 後資料中心合理成長率｜答法：CEO 先說 I don't think I can help there，不給數字，改談超越市場的目標
- TXN_Q2_2026_Earnings_Call_20260722.md｜問：Vivek Arya 要求量化漲價對 Q3 約 8% 季增的貢獻及 Q4 能否再漲｜答法：僅答 Q3 漲價貢獻幾乎不顯著，未直接回答 Q4 是否再漲

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
{"date":"20260907","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"capex 過峰後 FCF/share 由 2025 $3.23 重建至 2026 &gt;$8，並回到約 10% CAGR 趨勢線","columns":{"2Y驗證點":"2026 FCF/share ≥$8、2027 ≥$9；2026 capex $2–3B、折舊 $2.2–2.4B","5Y驗證點":"FCF/share CAGR ≥10%、FCF 利潤率 ≥30%","10Y驗證點":"FCF/share 複利 10% 且股數持續淨減","具體數字門檻":"2026 FCF/share &lt;$8 削弱；&lt;$7 反轉","信息來源":"年報（2027-01）／資本管理會（2027-02）","漂移觸發條件":"連 4 季 TTM FCF/share 偏離軌道 ≥5% 削弱；連 6 季 ≥10% 反轉"}},{"id":"H2","text":"工業／車用復甦為多年上行週期而非單季回補：GM 從 56% 回到 60% 以上、GAAP 營益率守 40%+","columns":{"2Y驗證點":"TTM GM ≥60%；工業營收距 2022 峰值缺口由 25% 收斂至 &lt;10%","5Y驗證點":"GM 穩定 62–65%（稼動率 80–90% 甜蜜區）","10Y驗證點":"類比份額由 17.8–19% 續升","具體數字門檻":"TTM GM 連 4 季 &lt;60% 削弱；&lt;58% 反轉","信息來源":"季報","漂移觸發條件":"連 2 季 TTM GM 偏離 ≥5%（相對）削弱；連 3 季 ≥10% 反轉"}},{"id":"H3","text":"資料中心成為第二曲線：可觸及市場 $7.5B→$12.5B（+65%），TI 約 20% 份額、營收年增 &gt;50%","columns":{"2Y驗證點":"資料中心營收年增 ≥30%（2027）","5Y驗證點":"資料中心占營收 ≥15%","10Y驗證點":"800V 架構下 GaN＋控制 IC 份額守住","具體數字門檻":"連 2 季 &lt;30% 削弱；&lt;15% 反轉","信息來源":"季報（資料中心自 2026 起獨立揭露）","漂移觸發條件":"連 2 季年增 &lt;30% 削弱；連 3 季 &lt;15% 反轉"}},{"id":"H4","text":"中國約 20% 營收守得住：本土替代只吃中低階料號，TI 2025 在中國仍取得份額（來源：摘要）","columns":{"2Y驗證點":"中國營收占比 ≥18%","5Y驗證點":"≥15% 且中國以外成長補足","10Y驗證點":"美中脫鉤基準情境下仍能出貨類比與嵌入式","具體數字門檻":"連 4 季合計 −3pp 或 &lt;17% 削弱；&lt;15% 反轉","信息來源":"年報／季報地區揭露","漂移觸發條件":"連 4 季合計偏離 ≥3pp 削弱；連 6 季 ≥5pp 反轉"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已進場核心；加碼＝回檔 $230–245 且 Q3 指引不弱；減碼＝FY2 P/E >32x 或工業／汽車連 2 季轉負；清倉＝GM 連 4 季 <58% 且 2027 FCF/share <$8","irr_base_pct":8.5,"ev5y_pct":44.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":4.8,"ev5y_pct":44.7,"irr_base_pct":8.5,"max_dd_pct":-45,"bull_5y_price":546.0,"bear_5y_price":208.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"已進場核心；加碼＝回檔 $230–245 且 Q3 指引不弱；減碼＝FY2 P/E >32x 或工業／汽車連 2 季轉負；清倉＝GM 連 4 季 <58% 且 2027 FCF/share <$8","price_at_dd":258.44,"archetype":"品質複利成長","cycle_position":"中循環"}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TXN_20261022/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
