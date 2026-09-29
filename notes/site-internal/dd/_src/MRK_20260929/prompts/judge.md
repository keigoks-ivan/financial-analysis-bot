你是 stock-analyst **v20 判斷 agent**，標的 MRK（20260929）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MRK","date":"2026-09-29","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20260929/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20260929/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_total_worldwide_sal","label":"營收（GAAP，Total Worldwide Sales）","value":16607,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"公司新聞稿 merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/；細項損益表引自 SEC 8-K exhibit 99.1（sec.gov/Archives/edgar/data/0000310158/000110465926090045/tm2621496d1_ex99-1.htm）"},"note":"consensus 約 $16.41B，實際 $16.607B 為 beat（來源：web_search 彙整分析師預估，非官方一手數字）"},{"id":"f_kpi1_non_gaap_non_gaap_operat","label":"Non-GAAP 稅前利益率（無法拆出獨立 non-GAAP operating income，新聞稿只揭露 non-GAAP pretax income）","value":3.3,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"SEC 8-K exhibit 99.1 reconciliation 表：non-GAAP pretax income $550M / 營收 $16,607M"},"note":"查無官方逐項 consensus 對照"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":-2.6,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"yfinance quarterly_income_stmt（Operating Income -$433M / Revenue $16,607M）"},"note":"查無官方逐項 consensus 對照"},{"id":"f_kpi5_2026_guidance","label":"管理層全年 2026 guidance","value":null,"period":"公告於 2026-08-04（隨 Q2 FY2026 財報同步更新）","unit":"range","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"公告於 2026-08-04（隨 Q2 FY2026 財報同步更新）","citation":"公司新聞稿 merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/"},"note":"營收 guidance 上調：$66.3B–$67.3B（前次 $65.8B–$67B）；Non-GAAP EPS guidance 大幅下修：$2.66–$2.76（前次 $5.04–$5.16），下修原因為 Terns（$2.43/股）與 Cidara 收購一次性費用認列，非營運惡化","needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-04","period":"2026-08-04","unit":"date","basis":"距今 40 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-04"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mrk_gross_margin_pct","label":"MRK 毛利率","value":72.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mrk_operating_margin_pct","label":"MRK 營業利益率","value":10.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mrk_fcf_margin_pct","label":"MRK FCF 利潤率","value":24.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pfe_gross_margin_pct","label":"PFE 毛利率","value":73.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFE.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pfe_operating_margin_pct","label":"PFE 營業利益率","value":26.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFE.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_pfe_fcf_margin_pct","label":"PFE FCF 利潤率","value":17.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFE.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bmy_gross_margin_pct","label":"BMY 毛利率","value":70.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bmy_operating_margin_pct","label":"BMY 營業利益率","value":28.14,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bmy_fcf_margin_pct","label":"BMY FCF 利潤率","value":23.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_gross_margin_pct","label":"ABBV 毛利率","value":71.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_operating_margin_pct","label":"ABBV 營業利益率","value":33.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_fcf_margin_pct","label":"ABBV FCF 利潤率","value":28.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF）","value":4477,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"yfinance quarterly_cashflow（Operating Cash Flow $5,370M − CapEx $893M）；FCF margin = 4477/16607 = 27.0%"},"note":"查無官方逐項 consensus 對照"},{"id":"f_kpi4_sbc","label":"SBC 占營收 %","value":1.79,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）","citation":"yfinance quarterly_cashflow（Stock Based Compensation $298M / Revenue $16,607M）；因 GAAP 營業利益為負，改以占營收表示"},"note":"查無官方逐項 consensus 對照"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":148.69,"period":"2026-09-28（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":27.56,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":57.72,"period":"2026-09-28（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":-0.36,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（2.75 → 2.74）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.21,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（9.55 → 9.53）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":-0.28,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.62 → 10.59）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":2.74,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":9.53,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.59,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":0.0,"period":"2026-06-23 → 2026-09-26","unit":"%","basis":"FY1 共識 EPS 2.74 → 2.74（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":118.95,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝13.9","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":13.9,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":5.51,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.21,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":54.27,"period":"2026-09-26","unit":"x","basis":"分母＝FY1 EPS 2.74，分子＝快照價 148.69","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-26"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-09-29","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 148.69 / W52 115.85 / W104 100.24 / W250 97.43 / W250 13週斜率 1.37%"},{"id":"f_ma_w52","label":"52 週均線","value":115.85,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":100.24,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":97.43,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":1.37,"period":"2026-09-29","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Keytruda/Keytruda Qlex 合併銷售 2026Q1 年增 12%、2026Q2 為 83.6 億美元年增 5%，仍是 PD-1 領域龍頭；對手 BMS Opdivo 2026Q1 銷售 21.5 億美元年減 5%，AstraZeneca Imfinzi 2026Q1 銷售 16.9 億美元年增 30%","source":"Yahoo Finance - Can Keytruda Sustain Merck's Growth in the Second Half of 2026?","url":"https://finance.yahoo.com/healthcare/articles/keytruda-sustain-mercks-growth-second-140000696.html","excerpt":"Combined global sales of Keytruda/Keytruda Qlex grew 12% in the first quarter of 2026... Keytruda/Keytruda Qlex sales were $8.4 billion (5% growth) in the second quarter of 2026... Opdivo generated sales of $2.15 billion in the first quarter of 2026, down 5% year over year... AstraZeneca's Imfinzi generated sales of $1.69 billion in the first quarter of 2026, up 30% year over year","as_of":"2026-08-01","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Keytruda 生物相似藥已於 2025 年在阿根廷等小型國際市場上市，2026 年將擴大至更多小型市場，但公司預期 2026 年生物相似藥侵蝕影響輕微；美國複方專利到 2028 年 12 月到期，兩項組成物專利延至 2029 年，歐洲市場專屬權到 2031 年，實質性衝擊預期在 2028-2029 年才會出現","source":"综合搜尋摘要（含 Merck 10-K FY2025、Pharmacy Times）","url":"https://www.pharmacytimes.com/view/soaring-off-the-patent-cliff-preparing-for-the-next-wave-of-oncology-biosimilars","excerpt":null,"as_of":"2026-02-24","retrieved_at":"20260929","affects":["moat_trend","thesis.R","triggers"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Gardasil 2026Q1 銷售暴跌 22% 至 10.7 億美元，中國市場（佔美國以外銷量 60-70%）需求因經濟放緩疲弱，且面臨中國本土 HPV 疫苗以十分之一價格搶市；Merck 已暫停對中國經銷夥伴智飛生物的出貨以消化通路庫存","source":"BioPharma Dive / Fierce Pharma / Yahoo Finance 綜合搜尋摘要","url":"https://www.fiercepharma.com/pharma/merck-puts-temporary-kibosh-gardasil-shipments-china-local-demand-hpv-vaccine-nosedives","excerpt":"Gardasil sales plunged 22% to $1.07 billion in the first quarter of 2026... China... accounting for 60% to 70% of all sales outside the U.S.... The shot is also facing competition from Chinese companies that sell HPV vaccines at one-tenth of Gardasil's price.","as_of":"2026-05-01","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"皮下劑型卡位戰：BMS 的 Opdivo Qvantig 皮下劑型於 2024 年 12 月搶先上市，早於 Merck 的 Keytruda Qlex（2025 年 9 月上市）；2026Q1 Opdivo Qvantig 營收年增逾 200%（主因 2025 年上市後需求墊高），Keytruda Qlex 則在 2026 上半年貢獻 5.9 億美元","source":"Yahoo Finance / BioPharma Dive 綜合搜尋摘要","url":"https://www.biopharmadive.com/news/merck-keytruda-subcutaneous-cancer-sales-drug-delivery/801889/","excerpt":"Merck launched its subcutaneous Pembrolizumab/Hyaluronidase formulation in September 2025, while BMS launched its Nivolumab/Hyaluronidase-nvhy SC formulation in December 2024... Opdivo Qvantig revenues increased more than 200% during the first quarter of 2026... Keytruda Qlex... contributed $590 million during the first half of 2026.","as_of":"2026-08-01","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"Merck 的三大藥品批發商客戶（McKesson、AmerisourceBergen、Cardinal Health）合計占應收帳款相當高比重，屬產業結構性集中，非新增惡化","source":"Merck & Co., Inc. Form 10-K FY2022","url":"https://www.sec.gov/Archives/edgar/data/310158/000162828023005061/mrk-20221231.htm","excerpt":"The Company's customers with the largest accounts receivable balances are: McKesson Corporation, AmerisourceBergen Corporation and Cardinal Health, Inc., which represented approximately 21%, 20% and 13%, respectively, of total accounts receivable at December 31, 2022.","as_of":"2022-12-31","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Gardasil 在中國因通路庫存偏高＋需求疲軟，Merck 自2025年2月暫停出貨，管理層預期2026年銷售不會回升；文章判斷中國經濟放緩屬暫時性因素，但同時提到日本需求下滑趨勢會持續，顯示週期性與結構性因素並存","source":"Yahoo Finance - Will Weak Gardasil Sales Continue to Weigh on MRK's Top Line in 2026?","url":"https://finance.yahoo.com/news/weak-gardasil-sales-continue-weigh-133500094.html","excerpt":"Lower demand in China resulted in above-normal channel invent","as_of":"2026-03-09","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Merck 2025年2月起暫停對中國出貨；2026年4月與中國經銷夥伴（智飛）簽署修訂後供貨合約；2026年第2季開始恢復有限出貨，但該合約相關營收預期2026年內仍不重大——顯示去化庫存＋需求回補為多季期的結構性過程，非單一季度週期性波動","source":"Merck & Co., Inc. Form 10-Q FY2026 Q2 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"Keytruda（占公司腫瘤營收核心）美國組成物專利2028年到期、用法專利至2029年11月，這是結構性、時程明確的懸崖，非週期性問題；公司揭露此為重大風險因子","source":"Merck & Co., Inc. Form 10-K FY2025 (SEC)","url":"https://www.sec.gov/Archives/edgar/data/310158/000031015826000063/mrk-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","valuation","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"參議員 Hassan（參院財政委員會健保小組資深議員）對 Merck 的 Keytruda 專利策略與 product hopping（劑型轉換）發起國會質詢，指控其藉此延遲低價競爭產品上市","source":"Senator Hassan press release / ICIJ 'Cancer Calculus' investigation","url":"https://www.hassan.senate.gov/news/press-releases/-senator-hassan-presses-big-pharma-company-on-anti-competitive-practices-that-boost-profits-at-the-expense-of-cancer-patients","excerpt":"delay other companies from selling lower cost versions","as_of":"2026-09-13","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Merck 於 2024年6月收到 DOJ 依 False Claims Act 發出的民事調查要求(CID)，就 Steglatro、Januvia 在 Medicaid 藥物回扣計畫下的價格申報，以及病患協助計畫的反回扣法遵規範進行調查","source":"Merck & Co. Form 10-Q (FY2026)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":null,"as_of":"2024-06","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"巴爾的摩市於2023年3月對 Merck 子公司提起反壟斷集體訴訟，指控其利用小兒疫苗市場的壟斷力進行搭售，維持 RotaTeq（輪狀病毒疫苗）市場的壟斷地位並收取超額定價","source":"Merck & Co. Form 10-Q / SEC filings (litigation disclosure)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":null,"as_of":"2023-03","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Merck 對 HHS 提起訴訟，主張 IRA（降低通膨法案）的 Medicare 藥價強制議價機制違憲；Januvia／Janumet 已分別於2023年、2025年被選入該議價名單","source":"The Philadelphia Inquirer","url":"https://www.inquirer.com/business/merck-inflation-reduction-act-lawsuit-20231130.html","excerpt":null,"as_of":"2023-11-30","retrieved_at":"20260929","affects":["thesis.R","valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"默克與美國商務部達成協議，將 Section 232 關稅延後三年課徵，換取默克在美國增加投資、把製造遷回美國。","source":"Merck 8-K exhibit 99-1 (SEC filing)","url":"https://www.sec.gov/Archives/edgar/data/310158/000110465926009495/tm264564d1_ex99-1.htm","excerpt":"The Company reached an understanding with the U.S. Department of Commerce to delay Section 232 tariffs for three years","as_of":"2026-02-03","retrieved_at":"20260929","affects":["moat_trend","thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"川普政府於 2026-04-02 發布 Section 232 公告，對專利藥品及其原料進口課高達 100% 關稅；默克（Merck Sharp & Dohme）被列在 Annex III 的 17 家指名大廠名單中，適用公告發布後 120 天生效（即 2026-07-31），其餘廠商則自 2026-09-29 生效。","source":"白宮 Section 232 藥品關稅公告 Annex 分析（法律事務所/貿易媒體報導彙整，如 McDermott Will & Emery、Mallory Group）","url":"https://www.mcdermottlaw.com/insights/section-232-pharmaceutical-tariffs-what-importers-need-to-know/","excerpt":null,"as_of":"2026-04-02","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"默克執行長 Rob Davis 向國會與川普政府示警，若對美中藥廠交易（dealmaking）設限過嚴，恐使美國自身承受後果；顯示默克在中國授權/併購交易上有政策限制風險暴露。","source":"Endpoints News","url":"https://endpoints.news/merck-ceo-cautions-congress-on-imposing-limits-on-chinese-dealmaking/","excerpt":null,"as_of":"2026-07-22","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"美國眾議院中國問題特別委員會主席 Moolenaar 於 2026-06-30 去函 Merck 與 AbbVie，要求說明在中國（含新疆與解放軍附屬醫院）進行臨床試驗的場址審查、資料保護與安全標準，7/17 前需回覆。","source":"Investing.com (Reuters) — US House committee opens investigation into Merck, AbbVie China drug trials","url":"https://www.investing.com/news/stock-market-news/exclusiveus-house-committee-opens-investigation-into-merck-abbvie-china-drug-trials-4767250","excerpt":"Rep. John Moolenaar, a Michigan Republican who chairs the House Select Committee on China, signed the Monday-dated letters calling on both companies to submit information by July 17 covering how they vet trial locations, protect data, and uphold safety standards — with particular scrutiny on sites in Xinjiang and at hospitals connected to China's military.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Merck 自 2005 年起在中國贊助或參與 224 項臨床研究，其中至少 31 項位於新疆、40 項在解放軍附屬醫院或醫療機構進行，成為本次國會調查的具體規模依據。","source":"GuruFocus — Merck (MRK) Faces National Security Scrutiny Over China Trials","url":"https://www.gurufocus.com/news/8938913/merck-mrk-faces-national-security-scrutiny-over-china-trials?mobile=true","excerpt":"Merck has sponsored or collaborated on 224 clinical studies in China since 2005, including at least 31 in Xinjiang and 40 at military-affiliated hospitals and medical centers.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Keytruda(腫瘤免疫藥)為Merck最大營收段，H1 2026 銷售 $16.40B，年增約4.2%；Q1 +8%、Q2 +5%","source":"Yahoo Finance - Can Keytruda Sustain Merck's Growth in the Second Half of 2026?","url":"https://finance.yahoo.com/healthcare/articles/keytruda-sustain-mercks-growth-second-140000696.html","excerpt":"Keytruda recorded sales worth $16.40 billion in the first half of 2026, up almost 4.2% year over year.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Gardasil(HPV疫苗)段H1 2026合併銷售年減9%，主因中國、日本需求疲弱","source":"SEC 10-Q FY2026 Q2 (Merck & Co.)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":"Combined worldwide sales of Gardasil and Gardasil 9 declined 9% in the first six months of 2026 primarily driven by lower demand in China and in Japan.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"-","claim":"管理層不預期Gardasil在2026年好轉，2026全年財測未計入任何中國出貨（因中國合作夥伴智飛通路庫存過高，先前已暫停出貨至2025年底）","source":"Fierce Pharma - Merck halts Gardasil shipments to China","url":"https://www.fiercepharma.com/pharma/merck-puts-temporary-kibosh-gardasil-shipments-china-local-demand-hpv-vaccine-nosedives","excerpt":"Merck decided to temporarily halt shipments of Gardasil in China to allow Zhifei to burn down existing inventory. The company didn't assume any Gardasil shipments to China in its 2026 full-year guidance, after previously pausing them through the end of 2025.","as_of":"2026-02-01","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"動物保健段H1 2026營收 $3.566B，年增10%（剔除匯率影響+6%）；畜牧+12%、寵物用藥+8%，主要靠Bravecto系列及新品","source":"Merck.com - Our Q2 2026 financial results","url":"https://www.merck.com/stories/our-q2-2026-financial-results/","excerpt":"For the first half of 2026, total Animal Health revenue was $3.566 billion, representing 10% growth, or 6% excluding foreign exchange effects.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Winrevair（肺動脈高壓新藥）H1 2026銷售年增81%、Q2單季+75%，美國滲透持續、日本歐洲剛起步放量；分析師共識峰值銷售估$8-8.5B","source":"SEC 10-Q FY2026 Q2 (Merck & Co.)","url":"https://www.sec.gov/Archives/edgar/data/0000310158/000031015826000212/mrk-20260630.htm","excerpt":"Winrevair sales rose 75% and 81% in the second quarter and first six months of 2026, respectively, largely due to continued uptake in the U.S. and early launch uptake in certain international markets, particularly in Japan and Europe.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"Keytruda 2028年專利懸崖：美國核心化合物專利2028到期，涉及逾$25B年化腫瘤營收；2026年生物相似藥侵蝕預期輕微（僅阿根廷等小型市場上市），但Medicare藥價協商新折扣價將於2028年1月生效，市場預期Keytruda美國銷售2027-28見頂後轉降","source":"Patsnap - Keytruda patent cliff 2028: Merck's strategy","url":"https://www.patsnap.com/resources/blog/articles/keytruda-patent-cliff-2028-mercks-strategy/","excerpt":"Keytruda's 2028 patent cliff puts more than $25 billion in annual oncology revenue at risk, with the drug's core composition-of-matter patent in the United States expected to expire in 2028.","as_of":"2026-01-01","retrieved_at":"20260929","affects":["thesis.R","valuation","triggers","moat_trend"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"PD-1/PD-L1（Keytruda所屬的免疫檢查點抑制劑類別）全球市場規模預估2026年約$73.87B，至2033年成長到$245.25B，CAGR約18.7%","source":"Future Market Insights - PD-1/PDL-1 Inhibitor Market Size, Share & Forecast to 2036","url":"https://www.futuremarketinsights.com/reports/pd1-pdl1-inhibitors-market","excerpt":"the market is estimated to be valued at USD 73.87 billion in 2026 and is expected to reach USD 245.25 billion by 2033, exhibiting a CAGR of 18.7% from 2026 to 2033.","as_of":"2026-01-01","retrieved_at":"20260929","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"中國 Akeso 與 Summit Therapeutics 合作開發的 PD-1xVEGF 雙特異性抗體 ivonescimab，在晚期肺癌頭對頭試驗中擊敗 Keytruda，是 Keytruda 上市十年來首次在此類試驗中落敗。","source":"BioPharma Dive - \"Merck, facing threat to Keytruda, buys into new kind of cancer immunotherapy\"","url":"https://www.biopharmadive.com/news/merck-lanova-pd1-vegf-bispecific-cancer-drug-deal/732906/","excerpt":"This year, one such drug, ivonescimab, from China-based Akeso and development partner Summit Therapeutics, bested Merck's Keytruda in a late-stage trial in lung cancer — the first time that's happened since Keytruda's arrival a decade ago.","as_of":"2024-11-14","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Merck 支付 5.88 億美元現金收購中國 LaNova Medicines 的同類 PD-1xVEGF 雙特異性抗體技術，作為 Keytruda 面臨替代技術與專利懸崖前的下一代免疫療法布局。","source":"BioPharma Dive - \"Merck, facing threat to Keytruda, buys into new kind of cancer immunotherapy\"","url":"https://www.biopharmadive.com/news/merck-lanova-pd1-vegf-bispecific-cancer-drug-deal/732906/","excerpt":"Merck is paying China-based biotech LaNova Medicines $588 million for the same type of bispecific antibody drug that recently bested Keytruda in a clinical trial.","as_of":"2024-11-14","retrieved_at":"20260929","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"FDA 於 2025 年 9 月核准 Keytruda Qlex（皮下注射固定劑量合併 pembrolizumab + berahyaluronidase alfa），涵蓋原 Keytruda 已核准的實體瘤適應症，為 Merck 因應生物相似藥與替代療法威脅的產品調整策略之一。","source":"PharmaVoice / Patsnap coverage of Merck's Keytruda strategy (via search synthesis)","url":null,"excerpt":"Keytruda Qlex, which was initially approved by the FDA in September 2025, is approved in the U.S. in solid tumor indications approved for Keytruda.","as_of":"2025-09","retrieved_at":"20260929","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Cipla 美國子公司已取得 Qilu Pharmaceutical pembrolizumab 生物相似藥 QL2107 的美國獨家銷售權，搶在 Keytruda 核心專利於 2028 年 12 月到期前卡位；報導指出 Keytruda 的生物相似藥倒數計時聲量正在變大。","source":"GuruFocus - \"Merck's $8.4 Billion Keytruda Fortress Gets a 2028 Warning\"","url":"https://www.gurufocus.com/news/9066847/mercks-84-billion-keytruda-fortress-gets-a-2028-warning","excerpt":"Cipla's U.S. subsidiary secured exclusive American commercialization rights to Qilu Pharmaceutical's proposed pembrolizumab biosimilar, QL2107, ahead of Keytruda's expected 2028 core patent expiration.","as_of":"2026-09-03","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#4","axis":"substitute_technology","section":"coverage","direction":"0","claim":"產業分析指出，單株抗體（含次世代 ADC、雙特異性抗體、CAR-T）在 2026 年管線營收預測持續強勁成長，反觀部分被視為顛覆性替代技術的基因療法、mRNA 與其他細胞療法管線營收預測已「停滯」，尚未撼動抗體類藥物的主導地位。","source":"BioPharm International - \"The New BioPharma Playbook: Seven Technologies Defining Drug Development in 2026\"","url":"https://www.biopharminternational.com/view/the-new-biopharma-playbook-seven-technologies-defining-drug-development-in-2026","excerpt":"The dominance of monoclonal antibodies and other therapeutic proteins is likely to continue in 2026 and beyond, however new modalities, such as cell and gene therapies, are getting traction and may eventually dethrone the more \"classic\" biologics. However, analysis of projected pipeline revenues reveals that established new modalities (mAbs, ADCs, BsAbs, recombinants, and CAR-T) continue to demonstrate robust growth, whereas some emerging modalities (gene, mRNA, and other cell therapies) have stalled.","as_of":"2026","retrieved_at":"20260929","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#5","axis":"substitute_technology","section":"coverage","direction":"-","claim":"新創公司 Crescent Biopharma 正開發 PD-1xVEGF 雙特異性抗體 CR-001，其定位明確是要取代 pembrolizumab 作為免疫腫瘤療法的新骨幹用藥，相關臨床試驗於 2026 年啟動。","source":"DIMA Biotechnology - \"2026 ASCO Target Review (Part II): Bispecific and Multispecific Antibodies and Immunotherapy Combinations\"","url":"https://www.dimabio.com/blog/2026-asco-bispecific-antibody-targets","excerpt":"Crescent Biopharma is developing CR-001, a PD-1 x VEGF bispecific antibody designed to bind both PD-1 and VEGF, which has potential to replace pembrolizumab (Keytruda) as the foundational immuno-oncology backbone. Clinical trials for CR-001, CR-002 and CR-003 were anticipated to initiate in 2026 along with the first ADC combination trial.","as_of":"2026","retrieved_at":"20260929","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"Merck 與美國政府達成協議，計畫在美國推出「直接對病人銷售」(direct-to-patient) 通路，以平價提供關鍵產品給符合資格的病人，屬 2026年2月與川普政府藥價協議的一部分。","source":"Merck & Co., Inc. SEC Form 8-K, Exhibit 99.1","url":"https://www.sec.gov/Archives/edgar/data/310158/000110465926009495/tm264564d1_ex99-1.htm","excerpt":"the Company plans to provide key products through a direct-to-patient program at affordable prices for eligible patients in the U.S.","as_of":"2026-02-03","retrieved_at":"20260929","affects":["thesis.H","thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"美國衛生部 (HHS) 於2026年1月27日發布新指引，釐清藥廠如何在不違反聯邦反回扣法的前提下，直接對病人（含 Medicare／Medicaid 參保人）提供低價處方藥，為產業性的直接對消費者(DTC)通路轉移提供法規基礎；聯邦政府另於2026年2月5日上線 TrumpRx.gov 作為導流入口，把病人導向藥廠自營 DTC 網站。","source":"HHS.gov press release; TrumpRx (Wikipedia); Galen Growth analysis","url":"https://www.hhs.gov/press-room/oig-clears-path-for-lower-cost-prescription-drugs.html","excerpt":null,"as_of":"2026-01-27","retrieved_at":"20260929","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Merck 2026年non-GAAP EPS財測由原本$5.04-$5.16大幅下修至$2.66-$2.76，公司說明主因是Cidara Therapeutics與Terns Pharmaceuticals兩筆併購認列的一次性費用，非核心業務惡化","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/merck-co-inc-nysemrk-updates-fy-2026-earnings-guidance-2026-08-04/","excerpt":"earnings per share (EPS) guidance of 2.660-2.760","as_of":"2026-08-04","retrieved_at":"20260929","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"同一次(Q2 2026財報)公司將2026全年營收財測上修並收窄至$66.3B-$67.3B（原區間約$65.8B-$67.0B），對應年增2%-4%","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/merck-co-inc-nysemrk-updates-fy-2026-earnings-guidance-2026-08-04/","excerpt":"revenue guidance of $66.3 billion-$67.3 billion","as_of":"2026-08-04","retrieved_at":"20260929","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"截至2026-08-20，MarketBeat彙整24位分析師，共識目標價為$154.24，共識評等為Moderate Buy","source":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/merck-co-inc-nysemrk-price-target-raised-to-17000-2026-08-20/","excerpt":null,"as_of":"2026-08-20","retrieved_at":"20260929","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026-02-18 Capital.com報導引用30位分析師，當時共識目標價為$128.57，與8月後彙整的$154.24相比存在時間落差（反映Q2財報前後分析師上修目標價）","source":"Capital.com","url":"https://capital.com/en-int/market-updates/merck-stock-forecast-18-02-2026","excerpt":null,"as_of":"2026-02-18","retrieved_at":"20260929","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q2 2026財報後(約2026-08-19起)多家券商上調MRK目標價：BMO Capital Markets由$142上調至$170並維持Outperform、JPMorgan由$140上調至$150並維持Overweight、Guggenheim上調至$146、Argus上調至$145、Daiwa由$120上調至$143並升評至Outperform，主因Keytruda Qlex、Winrevair、Ohtuvayre銷售優於預期","source":"Yahoo Finance（彙整多家券商研究報告）","url":"https://finance.yahoo.com/markets/stocks/articles/merck-mrk-stock-sees-modest-161232154.html","excerpt":null,"as_of":"2026-08-19","retrieved_at":"20260929","affects":["valuation","moat_trend"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Merck acquired Cidara Therapeutics for approximately $9.2 billion in January 2026, gaining MK-1406 (CD388), a long-acting antiviral for influenza prevention.","source":"Tracxn - List of Acquisitions by Merck","url":"https://tracxn.com/d/acquisitions/acquisitions-by-merck/__0z6lV4yciqgs5NwHZxS0VG-6Y6EopsT4RGuZXLg1AqE","excerpt":null,"as_of":"2026-01","retrieved_at":"20260929","affects":["moat_trend","valuation","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"Merck acquired Terns Pharmaceuticals, a clinical-stage oncology company, for $6.8 billion in May 2026.","source":"GuruFocus - Merck (MRK) Continues Aggressive M&A Strategy Amid Strong Pharma Deal-Making Trends","url":"https://www.gurufocus.com/news/8859768/merck-mrk-continues-aggressive-ma-strategy-amid-strong-pharma-dealmaking-trends","excerpt":null,"as_of":"2026-05","retrieved_at":"20260929","affects":["moat_trend","valuation"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"-","claim":"Securities class action Cronin v. Merck (Gardasil China demand allegations) is active: lead plaintiffs appointed Dec 17, 2025; amended complaint filed Feb 20, 2026; Merck's motion to dismiss filed May 1, 2026.","source":"Kessler Topaz - Merck & Co., Inc. Securities Fraud Class Action","url":"https://www.ktmc.com/new-cases/merck-co-inc/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#3","axis":"major_events","section":"coverage","direction":"-","claim":"A new securities fraud class action was filed July 20, 2026 alleging Merck misled investors about links between its canine anti-inflammatory drug Librela and severe adverse events.","source":"GuruFocus - Merck (MRK) Faces Securities Fraud Class Action Lawsuit Over Librela","url":"https://www.gurufocus.com/news/8967468/merck-mrk-faces-securities-fraud-class-action-lawsuit-over-librela?mobile=true","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"major_events#4","axis":"major_events","section":"coverage","direction":"+","claim":"FDA approved LIPFENDRA (enlicitide), the first once-daily oral PCSK9 inhibitor, as an adjunct to diet/exercise to reduce LDL-C, in July 2026.","source":"Merck.com - Q2 2026 Financial Results press release","url":"https://www.merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/","excerpt":"In July, FDA approved LIPFENDRA (enlicitide), the first and only once-daily oral PCSK9 inhibitor, as an adjunct to diet and exercise, to reduce LDL-C in adults with hypercholesterolemia.","as_of":"2026-07","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"major_events#5","axis":"major_events","section":"coverage","direction":"0","claim":"FDA PDUFA target action date of October 10, 2026 for I-DXd in extensive-stage small cell lung cancer, based on Phase 2 IDeate-Lung01 trial results (upcoming, not yet decided).","source":"Merck.com - Q1 2026 Financial Results press release","url":"https://www.merck.com/news/merck-co-inc-rahway-n-j-usa-announces-first-quarter-2026-financial-results-highlights-significant-regulatory-approvals-and-clinical-milestones/","excerpt":null,"as_of":"2026-10-10","retrieved_at":"20260929","affects":["triggers","thesis.H"],"status":"ok"},{"id":"major_events#6","axis":"major_events","section":"coverage","direction":"-","claim":"Merck disclosed receipt of a DOJ Civil Investigative Demand (CID) under the False Claims Act seeking documents on its DEI programs, investigating whether Merck falsely certified compliance with federal antidiscrimination laws in connection with federal contract payments.","source":"Merck & Co., Inc. - Form 10-K FY2025 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/310158/000031015826000063/mrk-20251231.htm","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20260929","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Merck acquired Cidara Therapeutics for approximately $9.2 billion in January 2026 (MK-1406/CD388 long-acting antiviral).","source":"Tracxn - List of Acquisitions by Merck","url":"https://tracxn.com/d/acquisitions/acquisitions-by-merck/__0z6lV4yciqgs5NwHZxS0VG-6Y6EopsT4RGuZXLg1AqE","excerpt":null,"as_of":"2026-01","retrieved_at":"20260929","affects":["moat_trend","valuation","thesis.H"],"status":"ok"},{"id":"ma_merger#1","axis":"ma_merger","section":"events","direction":"0","claim":"Merck acquired Terns Pharmaceuticals, a clinical-stage oncology company, for $6.8 billion in May 2026.","source":"GuruFocus - Merck (MRK) Continues Aggressive M&A Strategy","url":"https://www.gurufocus.com/news/8859768/merck-mrk-continues-aggressive-ma-strategy-amid-strong-pharma-dealmaking-trends","excerpt":null,"as_of":"2026-05","retrieved_at":"20260929","affects":["moat_trend","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"Securities class action Cronin v. Merck (Gardasil China demand allegations, orig. filed Feb 12, 2025) remains active: lead plaintiffs appointed Dec 17, 2025; amended complaint Feb 20, 2026; Merck's motion to dismiss filed May 1, 2026.","source":"Kessler Topaz - Merck & Co., Inc. Securities Fraud Class Action","url":"https://www.ktmc.com/new-cases/merck-co-inc/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"A new securities fraud class action was filed July 20, 2026 alleging Merck misled investors about links between Librela (canine anti-inflammatory) and severe adverse events.","source":"GuruFocus - Merck (MRK) Faces Securities Fraud Class Action Lawsuit Over Librela","url":"https://www.gurufocus.com/news/8967468/merck-mrk-faces-securities-fraud-class-action-lawsuit-over-librela?mobile=true","excerpt":null,"as_of":"2026-07-20","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"FDA approved LIPFENDRA (enlicitide), the first once-daily oral PCSK9 inhibitor, as an adjunct to diet/exercise to reduce LDL-C, in July 2026.","source":"Merck.com - Q2 2026 Financial Results press release","url":"https://www.merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/","excerpt":"In July, FDA approved LIPFENDRA (enlicitide), the first and only once-daily oral PCSK9 inhibitor, as an adjunct to diet and exercise, to reduce LDL-C in adults with hypercholesterolemia.","as_of":"2026-07","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"clinical_fda#1","axis":"clinical_fda","section":"events","direction":"+","claim":"KEYTRUDA QLEX (subcutaneous pembrolizumab combination) generated $463 million in sales in Q2 2026, reflecting initial market uptake following its FDA approval.","source":"Merck.com - Q2 2026 Financial Results press release","url":"https://www.merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/","excerpt":"KEYTRUDA QLEX Sales Were $463 Million","as_of":"2026-06","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"clinical_fda#2","axis":"clinical_fda","section":"events","direction":"+","claim":"FDA approved an additional indication for CAPVAXIVE (pneumococcal 21-valent conjugate vaccine) in children and adolescents aged 2 through 17 at increased risk for pneumococcal disease.","source":"Merck.com - Q2 2026 Financial Results press release","url":"https://www.merck.com/news/merck-highlights-key-regulatory-and-clinical-milestones-across-broad-diverse-pipeline/","excerpt":"FDA approved an additional indication for CAPVAXIVE in Children and Adolescents Aged 2 Through 17 at Increased Risk for Pneumococcal Disease.","as_of":"2026-06","retrieved_at":"20260929","affects":["moat_trend"],"status":"ok"},{"id":"clinical_fda#3","axis":"clinical_fda","section":"events","direction":"0","claim":"FDA PDUFA target action date of October 10, 2026 for I-DXd in extensive-stage small cell lung cancer, based on Phase 2 IDeate-Lung01 trial results (decision still pending as of query date).","source":"Merck.com - Q1 2026 Financial Results press release","url":"https://www.merck.com/news/merck-co-inc-rahway-n-j-usa-announces-first-quarter-2026-financial-results-highlights-significant-regulatory-approvals-and-clinical-milestones/","excerpt":null,"as_of":"2026-10-10","retrieved_at":"20260929","affects":["triggers","thesis.H"],"status":"ok"},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MRK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.97,"operating_margin_pct":10.49,"fcf_margin_pct":24.13,"rd_intensity_pct":45.75},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"PFE","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":73.18,"operating_margin_pct":26.72,"fcf_margin_pct":17.25,"rd_intensity_pct":17.35},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.PFE","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"BMY","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":70.16,"operating_margin_pct":28.14,"fcf_margin_pct":23.26,"rd_intensity_pct":21.8},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BMY","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ABBV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.48,"operating_margin_pct":33.94,"fcf_margin_pct":28.28,"rd_intensity_pct":15.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"MRK"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MRK/MRK_Q2_2026_Earnings_Call_20260804.md）

# Q2 2026 Earnings Call
2026-08-04

Q2 2026 Earnings Call
Merck & Co., Inc. | Earnings Calls | 2026-08-04
Operator (Operator)
Thank you for standing by. Welcome to Merck & Company, Inc., Rahway, New Jersey USA, Second
Quarter Sales and Earnings Conference Call. [Operator Instructions] This call is being recorded. If you
have any objections, you may disconnect at this time.
I would now like to turn the call over to Mr. Peter Dannenbaum, Senior Vice President, Investor
Relations. Sir, you may begin.
Peter Dannenbaum (Executives)
Thank you, Shirley, and good morning, everyone. Welcome to the Second Quarter 2026 Conference
Call for Merck & Company, Inc., Rahway, New Jersey USA. Speaking on today's call will be Rob Davis,
Chairman and Chief Executive Officer; Caroline Litchfield, Chief Financial Officer; and Dr. Dean Li,
President of Research Labs.
Before we get started, I'd like to point out that we have items in our GAAP results such as acquisition-
related charges, restructuring costs and other items that we have excluded from our non-GAAP results.
There is a reconciliation in our press release. I will also remind you that some of the statements that we
make today may be considered forward-looking statements within the meaning of the safe harbor
provision of the U.S. Private Securities Litigation Reform Act of 1995.
Such statements are made based on the current beliefs of our company's management and are subject
to significant risks and uncertainties. If our underlying assumptions prove inaccurate or uncertainties
materialize, actual results may differ materially from those set forth in the forward-looking statements.
Our SEC filings, including Item 1A and the 2025 10-K, identify certain risk factors and cautionary
statements that could cause the company's actual results to differ materially from those projected in
any of our forward-looking statements made this morning. Merck & Company Incorporated Rahway,
New Jersey, USA, undertakes no obligation to publicly update any forward-looking statements. During
today's call, a slide presentation will accompany our speakers' prepared remarks. These slides, along
with the earnings release, today's prepared remarks and our SEC filings are all posted to the Investor
Relations section of our company's website.
With that, I'd like to turn the call over to Rob.
Robert Davis (Executives)
Thank you, Peter. Good morning, and thank you for joining today's call. I remain very pleased with the
substantial progress we're making across our business, driven by strong execution, growing
contributions from new product launches and the continued advancement of the next wave of
innovation from our pipeline.
Earlier this year, we provided insight into greater than $70 billion of commercial opportunity we have
from over 20 new products that we expect will transform our portfolio and, in many cases, the practice

of medicine as well as fuel growth well into the next decade. We also outlined a series of clinical
milestones that represent key events to substantially derisk this opportunity.
Since then, we've made meaningful advancements against that objective, including several important
proof points that have occurred earlier than expected. This progress further bolsters my high
confidence in the future of our company and our ability to create long-term value for patients and
shareholders.
Turning to our second quarter results. We delivered revenue of $16.6 billion, reflecting continued
strength across Oncology and Animal Health as well as increasing contributions from our recent
launches. Importantly, while we're delivering for patients today, we're also making substantial
investments in the next generation of innovative medicines and vaccines. We remain confident in our
outlook for the remainder of the year, which Caroline will discuss in more detail in a moment.
We also achieved several important clinical and regulatory milestones. In Cardiometabolic, the FDA
approved LIPFENDRA, the first and only oral PCSK9 inhibitor to help reduce LDL cholesterol in adults
with hypercholesterolemia along with diet and exercise. We're pleased to have worked with the FDA
through the Commissioner's National Priority Voucher process to bring this important new treatment
option to patients on an accelerated basis. We look forward to providing broad access for patients to
help address elevated LDL-C, a major modifiable risk factor for cardiovascular disease.
In Oncology, we received several approvals that underscore the ongoing impact of KEYTRUDA and the
enduring strength of our oncology portfolio. At ASCO, we presented encouraging data that further
demonstrate the durability of KEYTRUDA and at our investor event, we highlighted advances for a
number of promising candidates across our pipeline. This included the first positive top line results
from our expansive Phase III global clinical development program for sac-TMT, our TROP2-directed
antibody-drug conjugate in certain patients with advanced or recurrent endometrial cancer.
In Immunology, we announced positive Phase III top line induction results for tulisokibart for certain
patients with ulcerative colitis and are starting to see the first of numerous additional trial readouts,
reinforcing our confidence in the potential of this program. And at the AIDS 2026 Congress last week,
we shared compelling data from our broad HIV pipeline, including for islatravir in combination with
lenacapavir, which has the potential to be the first oral once-weekly HIV treatment for virologically
suppressed adults.
We are excited to be returning to the HIV field with an array of important therapies, including the
recent launch of IDVYNSO. Ahead of the meeting, we also announced initial access plans for
Alimatravir, our investigational once-monthly oral HIV prep candidate now in Phase III studies,
underscoring our commitment to help enable broad and sustainable access to this candidate upon its
potential approval. We also continue to augment our portfolio through disciplined business
development.
During the quarter, we completed the acquisition of Terns Pharmaceuticals, adding MK-4208, a novel,
potentially best-in-class therapy for certain patients with chronic myeloid leukemia. This transaction
strengthens our hematology pipeline, adds another promising late-stage growth opportunity and
reflects our continued focus on pursuing science-driven business development that can benefit patients
and enhance long-term shareholder value. This quarter marks my fifth year as CEO. And as I reflect on
the commitments our leadership team made in 2021, our strategy was clear: maximize the
transformative potential of KEYTRUDA, expand, deepen and extend our leadership in Oncology, bring

forward new growth drivers across additional therapeutic areas and advance Merck's mission of using
the power of leading-edge science to save and improve lives around the world.
Today, I'm proud that we are successfully executing on that strategy. Each year, we're making
important progress in building a stronger foundation for our future. We're broadening and diversifying
our pipeline, advancing multiple potential blockbuster opportunities and achieving clinical, regulatory
and commercial milestones that will benefit patients and enhance our long-term growth trajectory.
I believe Merck is substantially stronger, more diversified and better positioned for sustainable growth
than it was just 5 years ago. While more work remains, I'm increasingly confident in Merck's future,
particularly with the rapid pace of clinical and regulatory events now occurring. This confidence is
grounded in the strength of our science, our disciplined approach to capital allocation, including
business development, and the dedication of our colleagues around the world who work every day to
deliver for patients.
I want to extend a special word of thanks to our global team for the substantial progress and for their
commitment and execution on behalf of patients, shareholders, and all of our stakeholders.
And now I'll turn the call over to Caroline.
Caroline Litchfield (Executives)
Thank you, Rob. Good morning. We delivered growth in the quarter, led by continued strength in
Oncology and Animal Health along with increasing contributions from our diverse and compelling new
products across an array of therapeutic areas. Our strong commercial and operational execution
continues to drive near-term performance while we invest in our outstanding pipeline to create long-
term value for patients, customers and shareholders.
Now turning to our second quarter results. Total company revenues were $16.6 billion, an increase of
5% or 4% excluding the impact of foreign exchange. The following revenue comments will be on an ex-
exchange basis. In Oncology, sales of the KEYTRUDA family of products which includes KEYTRUDA
and KEYTRUDA QLEX, increased 4% to $8.4 billion, with global growth driven by strong uptake in
earlier-stage cancers and continued robust demand from metastatic indications.
Strong utilization in tumors that primarily affect women, including breast and cervical cancers and
increased use of KEYTRUDA in combination with Padcev in locally advanced or metastatic urothelial
cancer were key contributors to growth. Sales of KEYTRUDA QLEX were $463 million. We have seen
physician and patient adoption increase since the permanent J-code was established in April.
As expected, early use has been predominantly in patients who are either on monotherapy or in
combination with an oral agent. We remain confident in the trajectory of KEYTRUDA QLEX adoption.
Our broader oncology portfolio delivered another quarter of strong growth. WELIREG sales increased
67% to $271 million, driven by continued uptake from international launches and increased use in
certain U.S. patients with previously treated advanced renal cell carcinoma.
We are excited that certain patients with earlier stage renal cell carcinoma may benefit from adjuvant
treatment with WELIREG following the recent FDA approval of LITESPARK-022. In vaccines and
infectious diseases, GARDASIL sales were $1.2 billion, an increase of 3%. Sales in international markets
grew 6% while the U.S. was roughly flat as lower demand and timing of CDC purchases was largely
offset by price.

In pneumococcal, CAPVAXIVE sales were $184 million an increase of 40%. Growth was primarily
driven by uptake from ongoing launches in certain international markets as well as higher demand in
the U.S. In HIV, we are pleased to have launched IDVYNSO, our once-daily oral 2-drug single-tablet
regimen of doravirine and islatravir for certain virologically suppressed adults.
We have seen encouraging early progress on access and reimbursement and look forward to
broadening access over time. In cardiometabolic and respiratory, WINREVAIR global sales were $588
million, an increase of 75%, reflecting continued strong demand from adults with pulmonary arterial
hypertension.
In the U.S., we saw further progress with more than 1,800 new patients having received a prescription
and an increase in the proportion of patients whose background therapies do not include a prostacyclin.
Outside the U.S., we continue to progress with ongoing launches. OHTUVAYRE sales were $204
million, reflecting continued prescription demand from patients with COPD as well as the benefit from
the timing of specialty pharmacy purchases.
Our Animal Health business delivered another quarter of solid growth with sales increasing 5%.
Livestock sales grew 6%, driven by higher demand for ruminant and poultry products. Companion
animal sales increased 5% due to new product launches. I will now walk you through the remainder of
our P&L, and my comments will be on a non-GAAP basis.
Gross margin was 81.1%, a decrease of 1.1 percentage points, primarily due to higher inventory reserves.
Operating expenses increased to $12.6 billion. There was a $5.7 billion charge for the acquisition of
Terns Pharmaceuticals in the quarter compared with a $200 million business development charge a
year ago.
Excluding these charges, operating expenses grew 7%, reflecting increased investments in support of
our launches as well as our robust early and late-phase pipeline, partially offset by benefits from our
multiyear optimization effort and recognition of a portion of the external funding for sac-TMT
development.
Other expense increased to $290 million, primarily reflecting financing costs related to recent business
development transactions. Our tax provision was $882 million. As a result of the nontax deductible
onetime charge for Terns, our tax rate was 160.3%. Taken together, we reported a loss of $0.13 per
share, which includes a onetime charge of $2.31 per share from the acquisition of Terns.
Now turning to our 2026 non-GAAP guidance. We have raised and narrowed our full year revenue
guidance range to be between $66.3 billion and $67.3 billion, representing growth of 2% to 4%,
including a positive impact from foreign exchange of approximately 1 percentage point using mid-July
rates.
Gross margin is now assumed to be approximately 81%, reflecting higher inventory reserves. Operating
expenses are expected to be between $42 billion and $42.7 billion. This range includes $5.8 billion for
the upfront charge for Terns and investment to advance MK-4208. This guidance does not assume
additional significant potential business development transactions.
Other expense, which now includes the financing costs for Terns, is expected to be approximately $1.4
billion. We now expect a full year tax rate between 35% and 36%, which reflects the nontax deductible
onetime charge for Terns. We assume approximately 2.48 billion shares outstanding. Taken together,

we expect EPS of $2.66 to $2.76 with a midpoint of $2.71, including a positive impact from foreign
exchange of approximately $0.15 using mid-July rates.
This range also includes an upfront charge of $2.31 per share related to the acquisition of Terns as well
as approximately $0.12 per share of ongoing costs to advance MK-4208 and finance the transaction. As
you consider your models, there are a few items to keep in mind for the second half of the year.
First, for OHTUVAYRE. We remain excited about OHTUVAYRE's strong clinical profile and look
forward to achieving its multibillion-dollar commercial potential in the coming years. Third quarter
sales will be impacted by the unwind of specialty pharmacy purchases in the second quarter. We
continue to invest behind our sales force and promotion to reach more physicians and patients in the
U.S. We are also working with our specialty pharmacies to improve patient experience. We expect these
actions to lead to accelerated growth in 2027.
Next, we anticipate that total U.S. KEYTRUDA year-over-year growth will moderate as we increasingly
reach peak penetration across several key indications. Additionally, as a reminder, we benefited by
approximately $250 million due to the timing of wholesaler purchases in the third quarter of 2025,
which will not repeat this year.
For BRIDION, U.S. sales are anticipated to decline at a slower pace than previously expected due to
lower-than-anticipated generic competition. Finally, other revenue in the second half of 2026 is
expected to be significantly higher than the second half of 2025. This increase is primarily due to our
revenue hedging program as well as an expected milestone receipt in the fourth quarter related to an
out-license agreement.
Now turning to capital allocation, where our strategy remains unchanged. We will continue to prioritize
investments that support near- and long-term growth, including our new product launches and robust
pipeline. We remain committed to the dividend with the goal of increasing it over time. Business
development remains a high priority, and we maintain the ability within a strong investment-grade
credit rating to pursue additional science-driven, value-creating transactions. We are on pace for
approximately $3 billion in share repurchases this year, as previously communicated.
To conclude, as we enter the second half of the year, we remain confident in the outlook of our
business, supported by global demand for our innovative medicines and vaccines, including our many
new product launches. The transformation of our portfolio is underway, and we are well positioned to
deliver value for patients, customers and shareholders now and into the future.
With that, I'd like to turn the call over to Dean.
Dean Li (Executives)
Thank you, Caroline. Good morning, everyone. The second quarter was marked by several important
regulatory and clinical milestones. Today, I will provide updates in cardiometabolic disease, HIV,
infectious disease, immunology and oncology. I will conclude with key upcoming milestones as we look
toward the second half of 2026.
First, in cardiometabolic disease, as Rob mentioned, we recently received FDA approval for
LIPFENDRA, the first approved oral PCSK9 inhibitor. In the CORALreef Lipids trial, LIPFENDRA was
shown to be highly effective in lowering LDL cholesterol with up to a 60% reduction when added to a
statin.

Earlier this year, updated U.S. guidelines on the management of dyslipidemia from the American
College of Cardiology and American Heart Association recognize that atherosclerotic cardiovascular
disease remains the leading cause of morbidity and mortality and underscore the need for earlier
intervention to help reduce lifelong risk from prolonged elevated lipoprotein exposure.
Guidelines also reestablished and lowered LDL-cholesterol treatment goals, including to under 55
milligrams per deciliter for individuals with ASCVD who are at very high risk of ASCVD events. The
approval of LIPFENDRA is a major milestone in our effort to make PCSK9 inhibition accessible in a
convenient daily oral option.
As an oral macrocyclic peptide, LIPFENDRA has the potential to extend the reach of this therapeutic
approach globally. Additional regulatory reviews are underway in the European Union and China. We
are also advancing combination approaches designed to further reduce LDL cholesterol and target
additional ASCVD risk factors. Studies are ongoing to support the development of 2 potential fixed-
dose combinations anchored by LIPFENDRA -- one with rosuvastatin and another with MK-7262, our
oral LP(a) inhibitor.
Turning to HIV. Yesterday, we hosted an investor event focused on our HIV program, including new
data presented at AIDS 2026. IDVYNSO provides the foundation of what we believe will be a series of
novel entries into the field. Our late-stage pipeline aims to address unmet needs for those living with or
at risk of HIV through innovative oral options, including 2 once-weekly treatment regimens and a
monthly oral option for pre-exposure prophylaxis.
In collaboration with Gilead, we announced full results of the Phase III ISLEND-1 and 2 trials
evaluating the investigational oral once-weekly regimen of islatravir and Gilead's lenacapavir both
studies demonstrated maintenance of virologic suppression in adults living with HIV who switched to
therapy from a daily standard of care.
These results support the potential for ISL/LEN to become the first approved oral once-weekly
treatment regimen for adults with virologically suppressed HIV. Results were also presented from a
Phase IIb study evaluating the investigational oral once-weekly combination of islatravir and
ulonivirine, an internally developed investigational non-nucleoside reverse transcriptase inhibitor in
adults with virologically suppressed HIV. Based on these results, we plan to advance ISL/ULO into
Phase III studies for people living with HIV who are previously untreated and those with prior
treatment experience. We also continue to evaluate our monthly oral HIV prep option, alimatravir, in 2
Phase III studies anticipated to read out next year.
Next, in infectious disease. We are progressing our Phase III study of MK-1406, an investigational long-
acting strain-agnostic antiviral designed to prevent influenza. Enrollment was completed in the
Southern Hemisphere. Plans are now in place to continue the study through a second Northern
Hemisphere flu season to strengthen our global regulatory submissions. We remain on track for
potential approval in 2029.
Moving to immunology, tulisokibart became the first anti-TL1A monoclonal antibody to demonstrate
positive results in a Phase III trial. In June, we reported on the induction-only study of the ATLAS-UC
trial. In patients with moderately to severely active ulcerative colitis, tulisokibart met the primary
endpoint of clinical remission as well as key secondary endpoint with no new safety concerns identified.
We look forward to the upcoming readout of the larger induction and maintenance study, which
together with the induction-only study would form the basis of a regulatory filing and will be presented

at an upcoming scientific congress. These findings reinforce the potential of targeting TL1A to help
address immunofibrosis, a key driver of disease progression across multiple immune-mediated
inflammatory conditions. We have advanced a broad Phase II development program to further explore
this hypothesis and now have results from 2 of these studies.
In SSc-ILD, the study did not meet its primary end point. In hidradenitis suppurativa, we are pleased to
share that the study met its primary and key secondary endpoints. Results will be shared in due course.
Finally, in oncology, KEYTRUDA continues to generate compelling clinical data and regulatory
approvals, including in earlier stages of disease. Recently, building on the approval of KEYNOTE-905,
the FDA approved an expanded indication for KEYTRUDA and KEYTRUDA QLEX, each with Padcev,
as treatment before and after surgery for adults with muscle-invasive bladder cancer based on the data
from KEYNOTE-B15. This regimen is now approved regardless of cisplatin eligibility and is the first and
only perioperative immunotherapy plus ADC regimen to extend survival for these patients.
We are also pleased that the FDA recently approved KEYTRUDA and KEYTRUDA QLEX in
combination with WELIREG for the adjuvant treatment of certain patients with clear cell renal cell
carcinoma based on the LITESPARK-022 study. This marks WELIREG's first approval in earlier-stage
disease and brings the total number of earlier-stage indications for KEYTRUDA-based regimens to 13.
In June, at our ASCO investor event, we shared updates across our broad and diverse oncology
portfolio. We also highlighted a series of pivotal readouts expected over the next several years. We are
now beginning to see the first of those milestones materialize with the announcement of positive Phase
III results from our global TroFuse development program evaluating sac-TMT. In TroFuse-005, sac-
TMT demonstrated statistically significant and clinically meaningful improvement in both overall
survival and progression-free survival versus chemotherapy in certain patients with advanced or
recurrent endometrial cancer. We plan to apply the National Priority Review Voucher for sac-TMT
towards our filing in endometrial cancer.
These results represent the first readout from our global TroFuse program which includes 17 Phase III
studies. The TroFuse program was intentionally designed to pursue both first-mover opportunities
where sac-TMT can establish early leadership and indications in breast and non-small cell lung cancer
where we can apply novel development approaches. This global effort continues to be informed by
promising results generated by our partner, Kelun from their program evaluating sac-TMT in China.
Positive results from the OptiTROP-Lung05 and, more recently, OptiTROP-Lung06 further
strengthens our confidence in the potential of this differentiated TROP2-directed ADC.
In closing, we anticipate a busy second half of the year. with multiple events and milestones, including
in cardiometabolic and respiratory, the September 21 PDUFA date for WINREVAIR for the label
update based on the Phase III HYPERION study, in immunology for tulisokibart, the second readout
from the ATLAS-UC trial and the presentation of data from the Phase II HS study.
In ophthalmology, data from the Phase III BRUNELLO study of remigromig, also known as MK-3000,
our novel Wnt agonist, being evaluated in patients with diabetic macular edema.
And finally, in oncology, potential approvals for WELIREG plus LENVIMA in advanced renal cell
carcinoma and for I-DXd in extensive stage small cell lung cancer and data presentations from across
our broad oncology portfolio, including detailed results of the Phase III TroFuse-005 study. Please
mark your calendars for the evening of Monday, October 26, where we will host an investor event at the

European Society for Medical Oncology in Madrid. I look forward to providing further updates on our
progress.
And now I will turn the call back to Peter.
Peter Dannenbaum (Executives)
Thank you, Dean. Shirley, we're now ready to begin Q&A. And we kindly request that analysts limit
themselves to 1 question today so we can get to as many questioners in the time that we have. Thank
you.
Operator (Operator)
[Operator Instructions] Our first question comes from Akash Tewari with Jefferies.
Akash Tewari (Analysts)
Dean, you previously stated a biomarker strategy would be the right approach for first-line NSCLC. But
with sac-TMT, we've seen a signal regardless of PD-L1 expression with the OptiTROP-Lung05 and 06
data. What are the chances we could see a broad sac-TMT plus pembro trial that goes head-to-head
against KEYNOTE-189? And is it fair to say we could see sac-TMT combos with both pembro and a PD-
1/VEGF for first-line lung?
Dean Li (Executives)
My simple answer is yes on all accounts, but I'll just step back a little bit, which is for sac-TMT, as we've
stated, we think it's a cornerstone ADC. I mean it's a TROP2 ADC, but it has a novel linker and payload.
And as described in the prepared remarks, we've sort of split the Phase III into 13 first mover where we
go into indications where we thought we could be first. And actually, what we're hoping is the TroFuse-
005 and then endometrial sort of gives validation to that strategy. And as we've noted, it's -- we've
talked to the administration's FDA, and this will be the one that goes for national priority vouchers.
In breast and lung, we've said that we need to be differentiated given other TROP2 ADCs. But as you
point out, the Kelun OptiTROP-Lung05, 06 gives us a lot of confidence in the target and to target it
across the full spectrum of PD-L1. So yes, we are going to rethink KEYNOTE-189, which is KEYTRUDA
plus chemo. And now we have sac-TMT as an ADC as a next-gen chemo. I do think that we're going to
be very thoughtful as to the IO agent and when we should use KEYTRUDA and when we should use
other agents such as MK-2010. And as you might imagine, we're advancing MK-2010 -- with that in
mind, we are moving quite fast in relationship to initiating trials, some that are signal finding, some
that are dose and scheduling to optimize with novel agents, and we're advancing trials that can go from
a Phase II to Phase III seamlessly.
Operator (Operator)
Our next question comes from Umer Raffat with Evercore.
Umer Raffat (Analysts)
Dean, congrats on the HS trial update for the TL1A. I'm just trying to think out loud to what extent as
we go into these new indications, is the activity we're seeing for these TL1As beyond what we would
have expected from a TNF? I'm sure you can appreciate where I'm coming from on this.

Dean Li (Executives)
Yes. Thank you very much. So just to step back a little bit, I think the question is posed in the fact that
TL1A is a member of the TNF superfamily. The TNFs have been really important drugs. They have been
advanced. There is often problems with combining them because of their safety signal. In relationship
to what we've seen so far, clearly, when you think about immunology, you think of 3 buckets, you think
of GI, you think of derm and you think of rheumatology. In GI, clearly, we're very eager to move
forward in ulcerative colitis and Crohn's disease, and we're really eager to see the other half of the UC
study. In the derm sort of space, we have it in HS. And I think that's important as well as we have
psoriatic arthritis. I think the positive readout for HS gives us more confidence in the derm sort of
possibilities for this drug.
And so that's where we're looking at. I still think that within the rheum space, which is, let's say, RA
and to some degree, psoriatic arthritis, we'll have to sort of play that out as the data comes out. But I
can just tell you, for example, for rheumatoid arthritis, we have very clear biomarker data suggesting we
should go after TL1A. And clearly, in something like rheumatoid arthritis, there are animal models in
preclinical where you can guesstimate what your activity is, and we have that data that gives us the
strength to move forward in rheumatoid arthritis.
Operator (Operator)
Our next question comes from Terence Flynn with Morgan Stanley.
Terence Flynn (Analysts)
Two-part for me. I was just wondering, Dean, if you could help us think about ahead of the Astra data
AVANZAR data, what you'd be most interested to see in that data set and implications for your sac-
TMT development strategy?
And then anything you can say, I know it's a Kelun study, but OptiTROP-Lung06 just in terms of
control arm performance in that trial, any comments?
Dean Li (Executives)
Yes. So let me take the last question first. We have a great partner in Kelun. We see very detailed data,
and we are very comfortable with the data that they've shown us, and it gives us great confidence in
moving forward. I would just highlight that some of the data that we saw is why we, for example, moved
quickly to endometrial. So we have a lot of confidence in how they run their clinical trials and their
data. I forgot the first half again.
Peter Dannenbaum (Executives)
AVANZAR.
Dean Li (Executives)
AVANZAR. I think the critical thing is, I think the AVANZAR -- I think we're waiting to see what the
readout looks like. We're looking to see what it looks like in all-comers, what we look like in
relationship to biomarker selected. And that will give us some views as to how do we advance ours, the
need for a biomarker. You can always have a biomarker, but that doesn't mean that you always need it.

And then the other sort of thing is how we think about advancing it in relationship to combination with
an excellent PD-1 like KEYTRUDA or whether or not we should move it forward with an excellent PD-
1/VEGF.
Operator (Operator)
Our next question comes from Michael Yee with UBS.
Michael Yee (Analysts)
On TL1A, 2-part question. You had one positive Phase III in UC, but not a whole lot was said. So how
do you think we should think about the profile in ulcerative colitis, appreciating the second study is
coming? And then it's supposed to be all about fibrosis, but then the SSc study wasn't positive today. So
how does that change your thinking around Crohn's and that fibrosis opportunity?
Dean Li (Executives)
Yes. So thank you very much for that question. In terms of the tulisokibart Study 2, I mean, we're very
eager to see Study 1 because together, that will be the package that we sent to the FDA. And we are
looking forward to that readout as we advance it. Again, in Crohn's disease, there's a signal, a clear
signal, not just from us, but from others, and it's what do we see in Phase III. So I think we're very
interested in moving those forward. You can look at some of the derm and the rheum indications that I
spoke about. They will also have fibrosis component.
In relationship to SSc-ILD, I would just state -- I would just step back. I don't know any anti-cytokine
that has worked. So this was a bold move to move that forward. It's a challenging and refractory
disease. We see no safety concerns. But I will tell you that when we publish that data, as you might
imagine, we will, I look very carefully at the placebo arm. If I see no progression in the placebo arm, it is
in SSc-ILD. But if I have no progression in the placebo arm, the chances that I will be able to show
benefit in a treatment arm becomes much more difficult. So I would not throw out the immunofibrosis
based on the SSc-ILD study not reading out positive in the specific patient population we recruited.
Operator (Operator)
Our next question comes from Geoff Meacham with Citi.
Geoffrey Meacham (Analysts)
Dean, on the LIPFENDRA launch, I wanted to ask how you guys view the pace of maybe initial access. I
wasn't sure what the right reimbursement expectation or if you thought the outcomes trial maybe
would be more needed as a commercial tipping point.
Dean Li (Executives)
So why don't I turn the commercial to Rob, if that's okay. And then I can answer the remaining
questions from a scientific standpoint.
Robert Davis (Executives)
Yes. Great. Thanks for the question, Geoff. If you look at it overall, I would just say we're very pleased
with what we're seeing so far. Obviously, you saw the label. We have a very clean label, one we feel very
good about. And with the fact that we have up to 60% LDL lowering, I think this is going to be a

meaningful treatment. We're seeing very high interest from physicians and patients based on the
approval announcement and ordering has begun last week, and we expect to be able to have it to
pharmacies here shortly. As we look at it from an access perspective, overall, we're, I think, in pretty
good shape. You remember, we really tried to set this up for broad access in the way we priced it and
the way we're going. That said, we do believe it's going to take time to get that access established. So we
are expecting to see the pace not be as fast out of the gate, but with long term, continue to expect to see
this to be definitely a blockbuster opportunity as we move forward.
I'll let Dean speak specifically to the broader question from a science perspective.
Dean Li (Executives)
Yes. So one thing I do want to highlight is there's often a lot of discussion of this FDA or this
administration FDA. I can tell you in our conversations with this administration's FDA, they wanted to
use LIPFENDRA as a cornerstone way to demonstrate what they're trying to do with their priority sort
of review. Most of the programs in that priority review only touch one of the sort of the pillars of what
they're trying to do. But they were very clear to us they want us to touch all of these pillars. And those
pillars is to target public health crisis, an innovative breakthrough, a large unmet need, especially in
chronic disease, which is a pillar of this HHS. They were very clear they want onshoring and supply
chain and resilience in the U.S., and they were very interested in accessibility in relationship to
increasing accessibility. So those 5 sort of pillars, that's what the FDA and us are racing to do as we
launch this important product.
Operator (Operator)
Our next question comes from Chris Schott with JPMorgan.
Christopher Schott (Analysts)
I guess with the pipeline derisking we've seen over the past year, can get any directional views or
updated color on what you're envisioning Merck's earnings profile could look like as we move through
the KEYTRUDA LOE? I know the focus of the company is more on the return to growth as we look out
into the early 2030s. But just would be any thoughts on that transition period of earnings could look
like over that, let's say, 2028 through early 2030s period.
Robert Davis (Executives)
Yes, Chris, thanks for the question. As we've said in the past, we feel very good about the progress we're
making with the over 20 products we have coming, $70 billion of commercial opportunity, and we've
already started to see meaningful clinical derisking happening at a pace faster than we expected as well
as good solid launches from the products that have launched. So as we sit here today, we feel very good,
as I've said in the past, we see that as the LOE period is more of a hill than a cliff. Nothing has changed
in our view. I do think you're going to see a shallow dip with a fast return back to growth.
And candidly, if we look at it on a non-risk-adjusted basis, we still aspire to grow through it. There still
is the potential more to do to achieve it, but we're working to get there. So as I sit here today, I feel very
good about where we are and the progress we're making. Always more to do, but I feel good about the
hand we have right now.
Operator (Operator)

Our next question comes from Courtney Breen with Bernstein.
Courtney Breen (Analysts)
Just one on LIPFENDRA, following up on the comments regarding kind of fixed-dose combinations.
You highlighted rosuvastatin in your own Lp(a). Particularly with rosuvastatin, I would love to hear a
little bit about how you're thinking about which dose you might consider. Is this just for those patients
that need further escalation once they've made it to the 40 mg, recognizing there's some more adverse
events there?
And then secondarily, are you looking at kind of continuing other combinations? We've heard GLP-1
combinations with the PCSK9s from peers and wanted to understand if you're still advancing or
considering this opportunity.
Finally, we haven't seen yet pop up on TumpRx. Just wondering kind of when we can expect that access
channel to begin to become available.
Dean Li (Executives)
Why don't I let the TrumpRx go to Rob and then I'll take the rest of them?
Robert Davis (Executives)
Yes. We're excited about the opportunity. And as you know, in our MFN agreement, we did commit to
putting LIPFENDRA on TrumpRx. Those plans are underway. We're working on obviously getting the
initial launch moving. And as soon as we get that going, we'll get it on TrumpRx. So more to come on
timing there.
Dean Li (Executives)
Yes. In relationship to your combination questions, thank you very much. I mean, right now, we have
an oral PCSK9 that was designed based on the learnings of the antibodies, and we have been able to
achieve up to 60% reduction in LDL cholesterol. We are hoping that with rosuvastatin, we would
provide to be all the doses. But with that combination, we think that we could get up to 80%. I mean if
we could get up to 80% in a combination, that's a good day for medicine. So those are the sort of way
that we think about the rosuvastatin.
For the Lp(a), we'll have to see what the Lp(a) actually does in relationship to the reduction. But we are
hoping that in a patient who has high Lp(a) that our combination will be able to give unprecedented
CVOT outcomes in relationship to that. In relationship to GLP, we have focused and said that we're
focused on oral combinations. And there is clearly the ability to combine GLP and PCSK9. One of the
things that we are very thoughtful about is that for the GLPs, you kind of do the step-up sort of dosing.
There's a lot of nausea and vomiting. So we can combine GLP plus PCSK9. But so far, we have not
announced that, that's a combination that we're actively doing in clinical trials -- in the clinical trials
website at this point.
Operator (Operator)
And this question comes from Jason Gerberry, Bank of America.
Jason Gerberry (Analysts)

Just another LIPFENDRA question. How do you guys think about the opportunity for injectable PCSK9
switch versus the bulk of the opportunity more in PCSK9 naive patients? And one thing that we've
noticed is with injectable PCSK9 relative to statins is pretty low use in the primary care setting. So how
do you see kind of the availability of now an oral when you say democratize access the sort of adoption
dynamics in the primary care setting?
Robert Davis (Executives)
Yes. Thanks for the question. As we've said many times, we are not focusing this market on how do we
take share from the injectable PCSK9. If you look today, injectables only reach about 5% or less of the
total market. We're sitting today here in the United States with 30 million people receiving lipid-
lowering therapies, but -- who are not at their recommended LDL levels and who -- even more who go
untreated. So the potential here is much bigger. What we are about is market expansion and helping
people understand that cardiovascular disease continues to be the #1 silent killer in the United States.
We now have a drug that reduces LDL, which is one of the leading causes of arteriosclerosis leading to
that cardiovascular death by up to 60% on top of statins and everyone who is at risk should be on one of
these medications. So our goal is to expand, build the market, educate the market, and we're doing that
with what we're doing with the guidelines. Obviously, this will all take time because there is inertia
we're working against. But if we are successful, this frankly, should raise the water for all boats and not
be one where we're taking share.
Dean Li (Executives)
Yes. And in relationship to the inertia, I think like, for example, the American Heart Association, the
American College of Cardiology and other important associations realize the inertia. So they specifically
changed the guidelines. And for right now, for example, for secondary ASCVD, they actually said the
vast majority of that secondary ASCVD should be less than 55. There's another patient population that
could be less than 70, but the vast majority of people with secondary ASCVD should be less than 55,
which is consistent with what Europe and other countries do. And in the prepared remarks, I did say
that we are not just advancing this with an approval and a launch in the U.S., but we're under
regulatory sort of discussions and review with the European Union as well as China.
Caroline Litchfield (Executives)
And to add to the comments that Rob and Dean have made, -- what we've seen thus far is extremely
strong feedback from key scientific leaders, understanding the change in the guidelines, understanding
what this product can do to help patients. What we need to do is to translate that to the primary care
setting. So that will take some time for us to do so, but our sales teams will be focused on ensuring the
right education to the primary care setting as well as to patients on the importance of this medicine.
Operator (Operator)
Your next question comes from Mohit Bansal with Wells Fargo.
Mohit Bansal (Analysts)
I have a question regarding the flu drug program, CD388. Can you talk a little bit about -- like what
were the reasons why you decided to add one more season of Northern Hemisphere here? And I think

the big question here is that was this decision based on any data you have seen? Or is this just to satisfy
the regulatory components rather than any confidence or lack of confidence in the data so far?
Dean Li (Executives)
Thank you very much for that question. So just to highlight, this is a first-in-class once-per-season
strain-agnostic antiviral that we're doing for the prevention of flu, especially for those people who are at
high risk. What we have said all along is that we plan to launch in 2029. And that at the same time, I
needed to do CMC work in relationship to getting it from 3 shots to 2 shots. And so that's the rate-
limiting step. I also said that between now and that time, I would do everything to have the most robust
label and the robust packages that would allow us to have a broadened footprint of sites to support a
global registration and allow me to get the right value proposition in ex U.S. markets, especially
something that we have to think in the day and age of MFN.
We've also added key secondary endpoints, which is all-cause hospitalization, which I think will be
critical in that pursuit. And finally, we're collecting data on subgroups and diverse circulating viral
strains throughout the world as we do this. I was also very clear that I did not need and would not take
an interim. I did not take or saw an interim. I am going to maximize what this molecule can do in the
time frame that I need to such that I do nothing to imperil the launch timing of 2029, but that I have
the most robust label as well as robust real-world evidence that will be important for health authorities.
Robert Davis (Executives)
Maybe just to summarize all that, there's no change in our confidence. Nothing we've seen in data. This
is all about strength of filing given the fact that we have the time because we do have to do the bridging
study that Dean mentioned.
Operator (Operator)
Our next question comes from Evan Seigerman with BMO Capital Markets.
Evan Seigerman (Analysts)
Kind of a key theme from this call talked about the $70 billion potential opportunity that you talked
about over the next wave of products. What's the biggest risk to achieving this number? And conversely,
which programs in the past 6 months have increased your confidence?
Robert Davis (Executives)
Yes. Thanks for the question. I mean, obviously, I would say, if you look at where we have confidence
from what we've seen, it's the fact that we're getting readouts faster than expected. When we talked
about this back in January, we had highlighted sac-TMT as well as I-DXd as not having readouts until
we got until 2027. We've now seen positive readouts from both. The Tuli has read out faster than we
expected. Everything is moving. So as we sit here today, my confidence is higher than it was in January
because we are seeing meaningful derisking. As you recall, at that time, we said there were 10 programs
that represented 70% of the $70 billion.
And the fact that so many of those are already having positive data, so we are clinically derisking them,
and we're seeing good launches of those that are underway, including an accelerated launch of
LIPFENDRA by several months. It's hard to frankly point to anything I'm worried about. I'm actually

feeling quite bullish across the board. I got to knock on wood because things are going well. But credit
to our scientific team and the strength of the clinical studies we put in place, I feel very good about
where we are.
Operator (Operator)
Our next question comes from Asad Haider with Goldman Sachs.
Asad Haider (Analysts)
Maybe for Dean, on the PD-1/VEGF bispecific program, just any updates on how the pace of that
development is progressing and how you're thinking about any potential read across from Summit's
HARMONi-3 data coming up? And any update on where you are with potential combination trials with
the PD-1/VEGF and your ADC assets?
And if I can just have a quick follow-up on TL1A. I know it's been discussed a lot already, but I just
appreciate any context or color that you have on where you are with evaluating combination
approaches, which is where the field in IBD seems to be moving towards. So how you thinking about
TL1A as a single agent in terms of its competitiveness versus these combo trials that J&J and AbbVie
are aggressively pursuing?
Dean Li (Executives)
Yes. Thank you very much. In relationship to the PD-1/VEGF sort of story, the way that I think about it
is there's a large body of data in relationship to where PD-1 is active. We ourselves have 44 and other
people have others. So there's that. There's also a body of evidence of where VEGF is active as well. So
you look at that overlap, and that's the place that you would go first. The other sort of thing is that in
some of those tumors, we have unique assets that can be combined and that we know are active. So
we're going to focus our efforts on PD-1/VEGF in those 3 sort of Venn diagrams where we are uniquely
able to move forward. We are very interested in following the Summit Akeso data. We think that, that's
important data for us to follow.
But this is our sort of general strategy of PD-1/VEGF in relationship to PD-1 where VEGF is active and
where we have unique assets that we know are active that could combine. In relationship to
combination, you're exactly right. The whole immunology field is trying to think about how it can go to
combinations. There is -- there has been lots of combinations in the past. TNF and IL-23, there is some
evidence that, that would be important. So when we look at TL1A, we're looking to have one of the most
effective, if not the most effective anti-cytokine in whatever the indication we have. But we think it's
also very important to know that the safety profile is extremely clean, which then makes it possible to
do combinations. The combinations that you would do, for example, in IBD would be different than
that of HS, which would be different than what you might do for rheumatoid arthritis. So for each one
of those indications, we are looking at the profile of our TL1A and also asking what is the ideal
combination for that indication.
Operator (Operator)
Your next question comes from Luisa Hector with Berenberg.
Luisa Hector (Analysts)

It's another one on LIPFENDRA, please. Just the specific wording on the label, which talks about LDL
reduction, but then that cardiovascular outcomes trials have shown to be -- have shown that you get a
reduction in LDL also leads to the reduction in events, specifically for monoclonal antibody PCSK9
inhibitors. So just wanted to check whether that wording is a help or a hindrance as you speak to payers
and as you go about your promotion? And then still on this CVOT topic, what is the timing of your
LIPFENDRA CVOT? And can you comment on how you can ensure that drop in use of incretins for
weight loss won't impact the result? Would you expect that to be balanced across arms if it does
happen?
Dean Li (Executives)
Yes. So let me answer that question. I need to be a little bit careful to talk about what the intention of
the FDA of putting whatever note that they put in the label. I think it's going to be extremely helpful.
We believe that LIPFENDRA should be added on top of statins. So I think that's really important. We
also know that the design principle, the design principles of LIPFENDRA, the agency understood was
informed by the 2 antibodies out there. So I think that it could be helpful from a commercial
standpoint, but I think that was the way that we -- that the FDA and our -- the discussion was. I should
emphasize that we do not have CVOT right now, and we have an ongoing trial that will read out in
2029.
Peter Dannenbaum (Executives)
Great. Thank you, Luisa. We're going to end the call there. I know there's a peer call about to start. So
thank you all for your time and attention this morning. We appreciate it. We look forward to catching
up at your convenience.
Operator (Operator)
Thank you. This does conclude today's conference. We thank you for your participation. At this time,
you may disconnect your lines.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MRK_Q1_2026_Earnings_Call_20260430.md
- 2026-04-30｜Caroline Litchfield｜guidance：2026 revenue guidance narrowed to $65.8B-$67B, growth 1%-3%（原話："revenue to be between $65.8 billion and $67 billion"）
- 2026-04-30｜Caroline Litchfield｜guidance：2026 EPS guidance raised to $5.04-$5.16, includes FX benefit（原話："we expect EPS of $5.04 to $5.16"）
- 2026-04-30｜Caroline Litchfield｜guidance：2026 guidance excludes proposed Terns acquisition and other BD deals（原話："does not include the proposed acquisition of Terns"）
- 2026-04-30｜Caroline Litchfield｜guidance：Terns deal expected to add a onetime R&D charge of ~$5.8B (~$2.35/share)（原話："approximately $5.8 billion or approximately $2.35 per share"）
- 2026-04-30｜Caroline Litchfield｜guidance：TERN-701 investment/financing costs expected to cut EPS by ~$0.12 this year（原話："negatively impact EPS by approximately $0.12 this year"）
- 2026-04-30｜Caroline Litchfield｜guidance：KEYTRUDA Q1 growth aided by purchase timing; offsetting headwind expected in Q3（原話："we will face a corresponding headwind in the third quarter"）
- 2026-04-30｜Caroline Litchfield｜customer：KEYTRUDA US growth included ~$250M benefit from timing of customer purchases（原話："$250 million from the timing of purchases"）
- 2026-04-30｜Caroline Litchfield｜customer：GARDASIL Q1 sales fell 22% on weaker demand in China and Japan（原話："driven by lower demand in China and Japan"）
- 2026-04-30｜Caroline Litchfield｜margin：Q1 gross margin was 81.9%, down 0.3 points year over year（原話："Gross margin was 81.9%, a decrease of 0.3 percentage points."）
- 2026-04-30｜Caroline Litchfield｜margin：Q1 opex rose to $15.2B, including a $9B onetime Cidara acquisition charge（原話："onetime charge related to the acquisition of Cidara"）
- 2026-04-30｜Caroline Litchfield｜margin：Nondeductible Cidara charge pushed Q1 tax rate to negative 43.5%（原話："a tax rate of negative 43.5%"）
- 2026-04-30｜Caroline Litchfield｜capital_allocation：Merck on pace for ~$3B of share repurchases this year, as previously communicated（原話："approximately $3 billion of share repurchases this year"）
- 2026-04-30｜Caroline Litchfield｜capital_allocation：Dividend remains a priority with a goal of increasing it over time（原話："committed to the dividend with the goal of increasing it"）
- 2026-04-30｜Robert Davis｜capital_allocation：BD deal-size sweet spot remains $1B-$15B, with capacity to go bigger for the right deal（原話："anywhere in the $1 billion to $15 billion range"）
- 2026-04-30｜Robert Davis｜commitment：Management states confidence TERN-701 can benefit patients while creating shareholder value（原話："TERN-701 can benefit patients while generating value"）
- 2026-04-30｜Robert Davis｜product：Merck views TERN-701 as having multibillion-dollar commercial potential（原話："TERN-701 has multibillion-dollar commercial potential"）
- 2026-04-30｜Robert Davis｜product：New business unit structure targets a >$70B commercial opportunity by mid-2030s from 20+ new products（原話："commercial opportunity of over $70 billion by the mid-2030s"）
- 2026-04-30｜Robert Davis｜product：FDA approved IDVYNSO as a new treatment for virologically suppressed HIV-1 adults（原話："IDVYNSO as a new treatment option for adults"）
- 2026-04-30｜Robert Davis｜product：FDA granted priority review to I-DXd in previously treated extensive-stage small cell lung cancer（原話："the FDA granted priority review for I-DXd"）
- 2026-04-30｜Dean Li｜risk：LITESPARK-012 combo missed its dual primary endpoint (PFS and OS) vs KEYTRUDA plus Lenvima in first-line RCC（原話："did not meet the dual primary endpoint"）
- 2026-04-30｜Dean Li｜competition：Dean Li says Merck is eager to advance its own PD-1 VEGF asset amid a competitor's PD-1 VEGF data at ASCO（原話："we're eager to move PD-1 VEGF forward in our trials"）
- 2026-04-30｜Caroline Litchfield｜risk：OHTUVAYRE Q1 sales hurt by CMS reimbursement change and Medicare deductible resets, as expected（原話："adversely impacted by the CMS reimbursement change"）
- 2026-04-30｜Robert Davis｜capital_allocation：Rob Davis says BD approach remains science-first, then strategic fit, then value alignment（原話："where we see science and value align, we move"）
- 2026-04-30｜Robert Davis｜product：Rob Davis teases undisclosed immunology pipeline assets beyond TL1A（原話："other assets in the immunology space that you're not seeing"）
- 2026-04-30｜Caroline Litchfield｜customer：WINREVAIR US added more than 1,600 new patients in Q1（原話："more than 1,600 new patients having received a prescription"）

### MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20251110.md
- 2025-11-10｜Dean Li｜guidance：管理層預期enlicitide（口服PCSK9抑制劑）2026年初開始遞交上市申請（原話："We expect filings to begin in early 2026"）
- 2025-11-10｜Joerg Koglin｜guidance：CORALreef Outcomes研究（enlicitide心血管結果研究）預計主要完成日為2029年底（原話："a primary completion date projected in late 2029."）
- 2025-11-10｜Jannie Oosthuizen｜guidance：管理層重申心血管代謝與呼吸道組合到2030年代中期有逾500億美元未經風險調整的營收機會（原話："over $50 billion by the mid-2030s."）
- 2025-11-10｜Jannie Oosthuizen｜guidance：管理層將新加入的Ohtuvayre（COPD吸入藥）定位為數十億美元級營收機會（原話："a multibillion-dollar revenue opportunity."）
- 2025-11-10｜Jannie Oosthuizen｜guidance：管理層對enlicitide上市初期的採用力道表達信心，稱一開始就會有實質性採用（原話："there will be meaningful adoption from the beginning."）
- 2025-11-10｜Jannie Oosthuizen｜commitment：管理層承諾enlicitide在美國的定價策略以取得廣泛可及性為目標（原話："we will price to get broad access in the United States."）
- 2025-11-10｜Dean Li｜commitment：被問及是否考慮改變早晨空腹服藥的規定以縮短禁食時間時，管理層明確表示不會重新配方（原話："we would not want to do something that disturbs that."）
- 2025-11-10｜Joerg Koglin｜product：CORALreef Lipids三期試驗中，經校正後enlicitide對LDL膽固醇的安慰劑校正降幅為59.7%（原話："the placebo-corrected LDL reduction was 59.7%."）
- 2025-11-10｜Joerg Koglin｜product：在家族性高膽固醇血症（HeFH）族群的CORALreef研究中，enlicitide使LDL自基線平均降59.4%（原話："a 59.4% mean reduction in LDL-C from baseline"）
- 2025-11-10｜Joerg Koglin｜risk：管理層稱enlicitide耐受性良好，安全性剖繪與安慰劑組相近（原話："very well tolerated with a safety profile similar to placebo."）
- 2025-11-10｜Joerg Koglin｜risk：CORALreef Lipids研究中有5名患者的基線值因資料處理規則出現生物學上不可能的數值，管理層因此重新分析並提出兩套（原始與校正後）數字（原話："biologically impossible baseline values"）
- 2025-11-10｜Joerg Koglin｜risk：管理層在回答分析師提問時承認，enlicitide在第52週的LDL降幅比第24週略有縮小，屬於降血脂藥物普遍觀察到的療效隨時間小幅衰減現象（原話："a small diminution of treatment effect"）
- 2025-11-10｜Joerg Koglin｜competition：管理層引用Amgen的VESALIUS研究（單株抗體Repatha相關）作為競品對照，該研究使主要心血管不良事件（MACE）降低25%（原話："It provided a 25% reduction in MACE."）
- 2025-11-10｜Courtney Breen (Analyst)｜competition：分析師在提問中指出，競品Amgen的Repatha在患者通路的定價已降至239美元，作為enlicitide未來定價與GLP-1同期上市的競爭背景（原話："Amgen offering Repatha at $239 in the patient channel."）
- 2025-11-10｜Jannie Oosthuizen｜customer：管理層指出美國、歐洲、日本三地合計逾8千萬名接受治療的患者，其LDL-C仍未達治療指引目標，構成enlicitide的潛在市場（原話："80 million treated patients have LDL-C levels"）
- 2025-11-10｜Jannie Oosthuizen｜customer：管理層指出美國近七成接受降血脂治療的患者仍未達LDL-C目標，凸顯add-on療法的市場缺口（原話："are not at their LDL-C goal"）
- 2025-11-10｜Jannie Oosthuizen｜customer：管理層強調enlicitide的口服劑型可將處方醫師基礎從心臟科專科醫師擴大到基層照護醫師（原話："to also include primary care professionals."）
- 2025-11-10｜Joerg Koglin｜product：WINREVAIR（肺動脈高壓藥）的標籤更新為首個納入死亡與肺移植降低的適應症敘述（原話："a reduction of death and the need for lung transplantation"）
- 2025-11-10｜Dean Li｜product：管理層描述LDL之外的心血管風險因子佈局分為發炎、Lp(a)、肥胖三大類，公司在四大類都有藥物，未來將視進度決定是否走複方（原話："LDL, inflammation, LP(a) and obesity."）
- 2025-11-10｜Dean Li｜product：WINREVAIR三項研究的匯總事後分析顯示，複合病態發病與死亡終點風險降低75%（原話："a 75% reduction in the risk of composite morbidity and mortality endpoint."）

### MRK_Wells_Fargo_21st_Annual_Healthcare_Conference_20260909.md
- 2026-09-09｜Caroline Litchfield｜guidance：CFO 給 2027 年主題方向：頂線成長預期溫和（原話："we would expect modest growth"）
- 2026-09-09｜Caroline Litchfield｜guidance：CFO 指出 2027 費用成長預期為中到高個位數（原話："expense growth of around mid- to high single digit"）
- 2026-09-09｜Caroline Litchfield｜risk：CFO 點名 Adempas 今年底到期失去專利保護，為 2027 逆風之一（原話："Adempas that loses LOE at the end of this year"）
- 2026-09-09｜Caroline Litchfield｜margin：CFO 表示毛利率因 KEYTRUDA 權利金到期而改善（原話："roll-off of a royalty on KEYTRUDA"）
- 2026-09-09｜Caroline Litchfield｜competition：CFO 提到德國政策變動帶來 KEYTRUDA 的定價壓力（原話："pricing pressures in the world, specifically in Germany"）
- 2026-09-09｜Dean Li｜product：研發主管說明 sac-TMT 在乳癌/肺癌以外先布局、等待時機再進場的策略（原話："we would strike when the time was right"）
- 2026-09-09｜Dean Li｜product：研發主管稱 sac-TMT 數據具顯著差異化（原話："the data for sac-TMT is substantially differentiated"）
- 2026-09-09｜Dean Li｜product：研發主管稱眼科資產 MK-8748 目標是成為同類最佳抗 VEGF 藥物（原話："ambition is to be superior to it"）
- 2026-09-09｜Dean Li｜commitment：研發主管稱 TL1A 在 GI/皮膚/風濕科的目標是同類最佳且最安全（原話："we are the best, if not the best, but we are the safest"）
- 2026-09-09｜Caroline Litchfield｜capital_allocation：CFO 重申併購甜蜜點為 10 億到 150 億美元交易規模（原話："deals that are in the $1 billion to $15 billion range"）
- 2026-09-09｜Caroline Litchfield｜capital_allocation：CFO 強調公司不急於做交易（原話："We're not desperate to do any deal"）
- 2026-09-09｜Caroline Litchfield｜customer：CFO 引用美國有 3000 萬服用 statin 但未達標的病人做為 LIPFENDRA 潛在市場（原話："30 million people who are taking statins who are not at goal"）
- 2026-09-09｜Caroline Litchfield｜commitment：CFO 表示 LIPFENDRA 初期處方表現良好（原話："initial scripts are looking good"）
- 2026-09-09｜Dean Li｜risk：研發主管指出 MFN 條款下歐洲定價不能比美國低太多，為 CD388 定價風險（原話："we can't have a tenfold discount in Europe"）
- 2026-09-09｜Dean Li｜product：研發主管提到業界原本認為 CD388 打 3 針不利上市，需改成 2 針（原話："you really shouldn't launch it with 3 jabs"）
- 2026-09-09｜Dean Li｜commitment：研發主管重申 CD388 上市時程不會延後（原話："we're not delaying the launch in any way"）
- 2026-09-09｜Dean Li｜competition：研發主管描述 sac-TMT 策略重心已轉回肺癌與乳癌這兩個核心戰場（原話："the Eye of Sauron is moving back into lung and breast"）

### MRK_Morgan_Stanley_24th_Annual_Global_Healthcare_Conference_20260914.md
- 2026-09-14｜Robert Davis (CEO)｜guidance：Davis表示對先前揭露的700億美元近期上市管線總機會存在上調空間（原話："you should assume we see upside to the $70 billion"）
- 2026-09-14｜Robert Davis (CEO)｜commitment：Davis確認公司會上調700億美元的數字，只是時程未定（原話："you're going to see us raise that number"）
- 2026-09-14｜Dean Li (President, Merck Research Labs)｜product：Li說明INT黑色素瘤Phase II五年追蹤數據顯示1年時腫瘤消失的病人多數在3年、5年仍維持無癌狀態（原話："remain largely so at 3 years, were largely so at 5 years"）
- 2026-09-14｜Dean Li (President, Merck Research Labs)｜competition：Li表示sac-TMT分子本身與前兩代TROP2 ADC不同，是差異化關鍵（原話："was different than the previous two"）
- 2026-09-14｜Robert Davis (CEO)｜guidance：Davis預期LIPFENDRA的Medicare覆蓋將在2028年到位（原話："We expect to have Medicare coverage by 2028."）
- 2026-09-14｜Robert Davis (CEO)｜customer：Davis說明LIPFENDRA的目標不是搶現有PCSK9注射針劑5%市占，而是把整體PCSK9合格族群滲透率拉到50%以上（原話："My goal is not to have 5% of people on PCSK9"）
- 2026-09-14｜Dean Li (President, Merck Research Labs)｜product：Li說FDA把LIPFENDRA的biomarker特性與有心血管結果數據的抗體類PCSK9藥物相提並論，視為正面訊號（原話："we view that as all positive movement"）
- 2026-09-14｜Robert Davis (CEO)｜customer：Davis轉述業務代表回報的早期病人端反應正面（原話："The short answer, it's all positive."）
- 2026-09-14｜Robert Davis (CEO)｜commitment：Davis重申公司致力於把免疫學列為重要治療領域（原話："we are committed to playing in immunology"）
- 2026-09-14｜Dean Li (President, Merck Research Labs)｜guidance：Li表示Tulisokibart兩項Phase III會有部分數據在今年秋天釋出（原話："We should be getting some of that data this fall."）
- 2026-09-14｜Robert Davis (CEO)｜capital_allocation：Davis強調公司資產布局不只靠中國，而是全球尋找科學（原話："We source from around the world."）
- 2026-09-14｜Robert Davis (CEO)｜product：Davis舉AI在分子設計與最佳化上的效益為目前最被低估的AI應用案例（原話："molecular design and molecular design optimization"）
- 2026-09-14｜Robert Davis (CEO)｜risk：Davis表示即使340B相關立法推進，對公司財務衝擊不算重大（原話："they're not material to us, frankly"）

### 問答異常語氣（迴避／改口／保留）
- MRK_Q1_2026_Earnings_Call_20260430.md｜問：Umer Raffat (Evercore) asked about incremental Terns/TERN-701 patient data showing an MMR achievement rate as low as ~2 of 10, and whether that changes the drug's profile.｜答法：Dean Li did not address the specific low-rate subset directly; he reframed to a broader ITT estimate ('north of 50%') versus the 75% publicly stated by Terns, without reconciling the analyst's cited drop.
- MRK_Q1_2026_Earnings_Call_20260430.md｜問：Louise Chen (Scotiabank) asked what the Street may be missing about the competitiveness of WINREVAIR given debate over the CADENCE data.｜答法：Dean Li said he was unsure what was being referenced and declined to engage with the competitive framing, redirecting to the unmet-need narrative instead of addressing the specific debate raised.
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20251110.md｜問：Leerink分析師Daina Graybosch追問：試驗中約3%患者服藥不順從，是否足以看出這對療效有負面影響？若現實世界的順從率不如試驗中高，是否構成風險？｜答法：管理層（Joerg Koglin）僅反覆強調臨床試驗內的順從率高達97%且效果持久，未正面回應「若現實世界順從率下降，是否構成療效風險」這個假設情境問題
- MRK_Shareholder_Analyst_Call_Merck_Co_Inc_20251110.md｜問：Daina Graybosch再次追問：CORALreef Lipids研究因5名患者基線值生物學上不可能而需要用兩種數字（55.8%與59.7%）表述效果，除了敘述上尷尬，這是否構成監管挑戰，或意味著這5名患者以外還有其他問題？｜答法：管理層（Joerg Koglin）以「這是很透明的決定」「科學界並未因此提出質疑」等安撫性語句回應，未具體正面回答是否構成監管挑戰
- MRK_Morgan_Stanley_24th_Annual_Global_Healthcare_Conference_20260914.md｜問：Is that a this-year event or a next-year event? (指700億美元管線數字何時上調)｜答法：未給明確時間點，只說「it's coming」與「to be determined in the near term」，語氣保留不承諾時程
- MRK_Morgan_Stanley_24th_Annual_Global_Healthcare_Conference_20260914.md｜問：Maybe just again, any update on when we might see that first set of full Phase III data? Is this something that we could see at the UEGW conference?｜答法：先以「If I could reframe the question a little bit」把焦點從IBD/會議時程轉向更廣的細胞激素節點策略，稍後才簡短回答資料時程
- MRK_Morgan_Stanley_24th_Annual_Global_Healthcare_Conference_20260914.md｜問：what does that mean for your sac-TMT program in the event that, let's say, the biomarker population only is positive?｜答法：未正面給判斷，只說會「look very deeply」並強調要看後續資料，屬條件式保留回答

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

**`decision_inputs`**（值可`null`，`dd_decision.py`機械路由裁決）七欄：`thesis_irreconcilable`(§4不可調和)｜`valuation_dependent`(re-rate貢獻≥Base IRR 40%；程式依你的情境算後覆寫，你填的僅供對照)｜`market_wrong_reason_given`(市場錯在哪的具體理由)｜`week26_return_pct`(26週漲幅)｜`momentum_overheated`(RSI 14d>70或4週漂移>+10%)｜`cycle_gates_pass`(反動能五閘全過，循環股)｜`consensus_rev_3m_pct`(FY1/FY2共識近3月上修%)，缺值`null`。覆寫層：`val_denominator_disputed`/`qc49_inherit_prior`+`prior_verdict`+`prior_role`/`held_now`(bool三態不可`"unknown"`代`null`)；`asym_ratio`/`irr_base_pct`/`ev5y_pct`一律`null` [§5]。

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
{"date":"20260525","verdict":"B 衛星候選（護城河 A 級 8/10 + 估值 🟢 便宜 Fwd PE 12.85x 5Y 分位 ~31.7%；但 Pure MA 🟡 接近 BB 上軌 stretched + Q2 26 Terns IPRD ~$5.8B charge + Keytruda 2028 LOC 已知 known unknown → 建議等回測 BB 中軌 $116 或 Q2 26 IPRD 消化後分批進場）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Keytruda 在 2028 LOC 前維持 +10-15% 年增長，QLEX SC 版本貢獻 ≥ 20% 銷售","columns":{"2Y 驗證點":"2027 末 Keytruda > $35B + QLEX 銷售 > $5B","5Y 驗證點":"2030 Keytruda + QLEX 合計 > $25B（LOC 後 vs LOC 前 ~75-80% retention）","10Y 驗證點":"2035 維持 MRK oncology #1 地位 ≥ 25% 市佔","具體數字門檻":"Keytruda YoY ≥ +10% 連 6 季；QLEX 銷售 FY27 ≥ $2B、FY28 ≥ $5B","信息來源":"Q1 26 8-K / 10-K","漂移觸發條件":"連 2 季 Keytruda YoY"}},{"id":"H2","text":"新藥 pipeline（Verona Ohtuvayre + WINREVAIR + Capvaxive + KEYLYNK 系列 + sacituzumab tirumotecan）合計 FY28 達 $15B+ revenue","columns":{"2Y 驗證點":"2027 末新藥合計 > $8B","5Y 驗證點":"2030 新藥合計 > $20B，填補 Keytruda LOC 缺口","10Y 驗證點":"2035 新藥組合多元化，無單一 > 30%","具體數字門檻":"FY26 新藥合計 ≥ $5B / FY27 ≥ $8B / FY28 ≥ $15B","信息來源":"JPM 2026 update + 法說","漂移觸發條件":"FY27 新藥合計"}},{"id":"H3","text":"估值倍數修復至 5Y 中位 14-15x（vs 當前 12.85x）","columns":{"2Y 驗證點":"2027 末 Fwd PE > 14x","5Y 驗證點":"2030 Fwd PE 14-16x","10Y 驗證點":"10Y 倍數 mean-revert（無需具體閾值）","具體數字門檻":"Fwd PE 12 個月內 > 14x；PEG（normalized）","信息來源":"§13.1 5Y 中位","漂移觸發條件":"連 4 季 Fwd PE"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Keytruda biosimilar 2027 進入提早","columns":{"對應假設":"H1","時間尺度":"🔥 中期 4-6 季","監測指標":"FDA biosimilar approval calendar；major pharma 競爭品 readouts","警戒閾值":"FDA 加速 biosimilar pathway 確認 → 削弱；首支 biosimilar 進場 → 反轉"}},{"id":"R2","text":"Verona / Terns / WINREVAIR pipeline 商業化 / readouts 不順","columns":{"對應假設":"H2","時間尺度":"🔥 中期","監測指標":"季度新藥銷售數字；主要 Phase III readouts","警戒閾值":"Verona Ohtuvayre FY26 銷售"}},{"id":"R3","text":"Gardasil 中國市場結構性消失 + 中國本土生物相似藥對 Keytruda 也構成威脅","columns":{"對應假設":"H1、H3","時間尺度":"🐢 長期 2+ 年","監測指標":"中國 Gardasil 訂單；中國生物相似藥 pipeline","警戒閾值":"連 4 季 Gardasil China 訂單 ≤ $0 → 結構性接受；中國本土 PD-1 進入美國市場 → ⛔"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":122.41,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20260929/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
