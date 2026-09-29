你是 stock-analyst **v20 判斷 agent**，標的 FSLR（20260929）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"FSLR","date":"2026-09-29","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20260929/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20260929/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_net_sales","label":"營收（GAAP net sales）","value":1056.2,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"US$M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/1274494/000127449426000169/ex991pressreleaseq2-2026.htm"},"note":"consensus 約 $1,061M（多家彙整站稱『大致符合／小幅未達』，來源：web_search，非公司原文）"},{"id":"f_kpi1_non_gaap_adjusted_ebitda","label":"Non-GAAP 獲利指標（Adjusted EBITDA；公司本季未單獨揭露 non-GAAP operating income）","value":643.6,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"US$M；margin 61%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿 SEC 8-K Ex.99.1（同上）"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／營業利益率","value":450.4,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"US$M；margin 42.6%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿 SEC 8-K Ex.99.1（同上）"}},{"id":"f_kpi5_fy2026_guidance_q2","label":"FY2026 全年 guidance（隨Q2財報重申，區間未變動）","value":"Net sales $4.9B–$5.2B；Gross profit $2.4B–$2.6B；Opex $610M–$635M；Adjusted EBITDA $2.6B–$2.8B；Capex $0.8B–$1.0B；年底Net cash $1.7B–$2.3B；另單獨給Q3單季 Adjusted EBITDA guide $625M–$775M","period":"公告於 2026-07-30，隨Q2財報重申（非新發guidance，與Q1財報所發一致）","unit":"US$（詳見value欄各分項）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"公告於 2026-07-30，隨Q2財報重申（非新發guidance，與Q1財報所發一致）","citation":"公司新聞稿 SEC 8-K Ex.99.1（同上）"},"note":"營收guidance中值≈$5.05B，市場彙整站稱略低於 street consensus $5.08B（來源：web_search，非公司原文）"},{"id":"f_kpi6_contracted_sales_backlog","label":"Contracted sales backlog（硬體／設備 archetype 追加項）","value":45.1,"period":"截至 2026-06-30，公告於 2026-07-30","unit":"GW；對應合約總值 $13.6B（不含技術調整項），交貨期至2030年","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[6]","as_of":"截至 2026-06-30，公告於 2026-07-30","citation":"公司新聞稿 SEC 8-K Ex.99.1（同上）"}},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-07-30","period":"2026-07-30","unit":"date","basis":"距今 43 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-07-30"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_fslr_gross_margin_pct","label":"FSLR 毛利率","value":44.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_fslr_operating_margin_pct","label":"FSLR 營業利益率","value":33.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_fslr_fcf_margin_pct","label":"FSLR FCF 利潤率","value":27.89,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_csiq_gross_margin_pct","label":"CSIQ 毛利率","value":16.43,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSIQ.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_csiq_operating_margin_pct","label":"CSIQ 營業利益率","value":-0.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSIQ.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_csiq_fcf_margin_pct","label":"CSIQ FCF 利潤率","value":-31.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSIQ.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jks_gross_margin_pct","label":"JKS 毛利率","value":4.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKS.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jks_operating_margin_pct","label":"JKS 營業利益率","value":-6.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKS.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_enph_gross_margin_pct","label":"ENPH 毛利率","value":46.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENPH.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_enph_operating_margin_pct","label":"ENPH 營業利益率","value":8.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENPH.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_enph_fcf_margin_pct","label":"ENPH FCF 利潤率","value":11.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENPH.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF＝營運現金流－資本支出）","value":-306.2,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"US$M；margin -29.0%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿現金流量表僅列 Six Months Ended 欄位，Q2 單季由 H1（營運現金流 -$359.8M／資本支出 -$279.8M）減去 Q1 press release 對應數字（-$214.9M／-$118.5M）反推，非公司原文直接揭露"}},{"id":"f_kpi4_sbc","label":"SBC 占營業利益（及占營收）%","value":1.56,"period":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","unit":"%（占GAAP營業利益）；另占營收 0.67%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q2 FY2026（季末 2026-06-30，公告於 2026-07-30）","citation":"公司新聞稿現金流量表 H1 股權薪酬 $13.826M 減 Q1 press release 三個月數字 $6.781M，反推 Q2 單季 SBC ≈$7.045M，非公司原文直接揭露單季數"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":172.97,"period":"2026-09-28（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-6.35,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":33.18,"period":"2026-09-28（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（17.61 → 17.61）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（23.25 → 23.25）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（29.13 → 29.13）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":17.61,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":23.25,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":29.13,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":1.15,"period":"2026-06-23 → 2026-09-26","unit":"%","basis":"FY1 共識 EPS 17.41 → 17.61（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":10.95,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":0.0,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":3.46,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":0.0,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.17,"period":"2026-09-28（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-28（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-09-28（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-28（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":9.82,"period":"2026-09-26","unit":"x","basis":"分母＝FY1 EPS 17.61，分子＝快照價 172.97","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-26"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"❌","period":"2026-09-29","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 172.97 / W52 229.3 / W104 201.88 / W250 175.48 / W250 13週斜率 0.83%"},{"id":"f_ma_w52","label":"52 週均線","value":229.3,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":201.88,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":175.48,"period":"2026-09-29","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":0.83,"period":"2026-09-29","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-29","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"FSLR Q1 2026 淨銷售 10.4 億美元，年增 24%，主因是賣給第三方的模組出貨量增加","source":"SEC 8-K, First Solar Q1 2026 press release","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000108/ex991pressreleaseq1-2026.htm","excerpt":"Net sales were $1.04 billion for the first quarter of 2026, a 24% increase compared to the first quarter of 2025, driven primarily by an increase in the volume of modules sold to third parties.","as_of":"2026-04-30","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"截至 2026年3月31日，FSLR 合約在手訂單（backlog）47.9 GW","source":"SEC 8-K, First Solar Q1 2026 press release","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000108/ex991pressreleaseq1-2026.htm","excerpt":"Contracted sales backlog of 47.9 GW as of March 31, 2026","as_of":"2026-03-31","retrieved_at":"20260929","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"2025年全球模組出貨量排名：LONGi 約87GW、Jinko約86GW 並列龍頭，FSLR出貨17.5GW創自身紀錄但僅佔全球約2%市佔率，量能上落後中國廠","source":"TaiyangNews / SolarQuarter，2025全球模組出貨排名報導","url":"https://taiyangnews.info/business/solar-module-shipment-2025-ranking","excerpt":null,"as_of":"2026-03-14","retrieved_at":"20260929","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"儘管出貨量僅為中國四大廠（LONGi/Jinko/JA Solar/Trina）合計的三分之一，FSLR的淨利仍高於這四家合計；差異化來自CdTe薄膜技術不依賴矽料供應鏈、美國本土製造適用45X稅收抵免（2025年認列16億美元）、以及50.1GW/150億美元的在手訂單","source":"SurgePV，Top Solar Companies by Revenue 2026","url":"https://www.surgepv.com/blog/top-solar-companies-by-revenue-2026","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20260929","affects":["moat_trend","valuation"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Lightsource bp 與 First Solar 簽署4GW模組供貨協議，2026-28年交貨，為雙方繼2021年最高4.3GW協議後第二筆同類合約，顯示既有客戶持續下單、未被競爭對手取代","source":"PV Tech，Lightsource bp and First Solar ink 4GW module supply agreement for 2026-28","url":"https://www.pv-tech.org/lightsource-bp-and-first-solar-ink-4gw-module-supply-agreement-for-2026-28/","excerpt":"Lightsource bp and First Solar have agreed a 4GW module supply deal for US projects to be delivered between 2026-28.","as_of":"2023-02-28","retrieved_at":"20260929","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"同業／風險因子提及：來自矽晶（crystalline silicon）模組廠的激烈競爭可能壓低平均售價與淨銷售；FSLR 也在CdTe配方中加入鈣鈦礦(perovskite)以提升效率，屬對新興技術威脅的回應","source":"綜合搜尋摘要（PV Tech / CleanTechnica 相關報導）","url":null,"excerpt":null,"as_of":"2026-03-13","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K names two customers each at/above 10% of modules business net sales: Silicon Ranch Corporation and NextEra Energy.","source":"First Solar, Inc. Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449426000021/fslr-20251231.htm","excerpt":"During 2025, Silicon Ranch Corporation and NextEra Energy each accounted for 10% or more of our modules business net sales.","as_of":"2025-12-31","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"For FY2024, no single customer accounted for 10% or more of First Solar's net sales (an improvement in diversification versus 2023 and 2021).","source":"First Solar, Inc. Form 10-K FY2024 (aggregated search summary, not independently page-verified)","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449425000010/fslr-20241231.htm","excerpt":null,"as_of":"2024-12-31","retrieved_at":"20260929","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Historical concentration was higher in earlier years: FY2023 Customer #1 = 10%; FY2022 three customers each >=10% (14%, 10%, 10%); FY2021 Customer #1 = 12%, Customer #2 = 10%. Customers are not named in these older filings, only numbered.","source":"First Solar, Inc. Form 10-K FY2021/2022/2023 (aggregated search summary, not independently page-verified)","url":"https://www.sec.gov/Archives/edgar/data/1274494/000127449424000004/fslr-20231231.htm","excerpt":null,"as_of":"2023-12-31","retrieved_at":"20260929","affects":["moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"2026 US solar bankruptcy wave (100+ companies since 2023, including Freedom Forever Chapter 11 on 2026-04-15) is concentrated in residential/C&I installers; commentary frames First Solar as insulated because it sells utility-scale modules to large developers/utilities rather than to homeowners.","source":"Yahoo Finance / TheStreet: \"One company stands to gain as bankruptcy wave hits solar sector\"","url":"https://finance.yahoo.com/energy/articles/one-company-stands-gain-bankruptcy-033300453.html","excerpt":"Unlike residential solar installers, First Solar does not sell to homeowners and builds large volumes of panels for utility-scale power plants, the kind that feed electricity to the grid.","as_of":"2026-08","retrieved_at":"20260929","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"全球太陽能供應鏈各環節產能相對近期需求嚴重過剩（pv magazine 用「severely overbuilt」形容）","source":"pv magazine USA","url":"https://pv-magazine-usa.com/2026/09/01/oversupply-expanding-tariffs-and-tech-shifts-reshape-u-s-solar-outlook/","excerpt":"Global manufacturing capacity across every segment of the solar value chain remains severely overbuilt relative to near-term demand","as_of":"2026-09-01","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"第三方估算：多晶矽產能約 2,034 GW 對比 2026 年預估裝機 638 GW，模組產能約 1,908 GW，過剩逾 1.2 TW；此為結構性而非暫時性短缺","source":"ICRA / SurgePV 產業分析（經搜尋摘要彙整）","url":null,"excerpt":null,"as_of":"2026-08-28","retrieved_at":"20260929","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"BNEF／pv-tech 觀點：2026 年可能是本輪供應鏈調整的谷底，2027–2029 年成長率可望回升至兩位數（受電動運輸、資料中心、汰舊換新驅動）","source":"pv magazine International / pv-tech The PV Review 2025","url":"https://www.pv-magazine.com/2025/12/23/bnef-flags-potential-global-solar-slowdown-in-2026-as-china-cools/","excerpt":null,"as_of":"2025-12-23","retrieved_at":"20260929","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"中國多晶矽業者 2025 年產量年減 28.4% 至 132 萬噸，價格自 2025 年中低點回升逾 50%（RMB 50–56/kg），為行業自律限產結果；2026 上半年在產產能約 130 萬噸","source":"搜尋摘要彙整（DAQO New Energy 6-K 系列 / 產業報告）","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20260929","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#4","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"中國自 2027-01-01 起實施更嚴格多晶矽單位能耗強制標準（超過 6.3 kgce/kg 須整改或面臨停產），但因高耗能產能多已閒置，對實際供給的立即影響有限","source":"pv magazine Global","url":"https://www.pv-magazine.com/2026/07/24/china-adopts-tougher-mandatory-energy-limits-for-polysilicon-plants/","excerpt":null,"as_of":"2026-07-24","retrieved_at":"20260929","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#5","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"First Solar 2026 Q2 季底合約在手訂單（backlog）達 45.1 GW，交付期涵蓋至 2030 年","source":"First Solar Q2 2026 財報摘要（wedoany 轉載）","url":"https://en.wedoany.com/shortnews/435850.html","excerpt":"As of the end of the quarter, First Solar's contracted backlog stood at 45.1 GW, covering through 2030.","as_of":"2026-08-01","retrieved_at":"20260929","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#6","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"First Solar 技術調整條款（technology adjusters）在合約中最多可為 2028 年前帶來額外約 6 億美元營收，主要落在 2027–2028 年","source":"First Solar Q1 2026 財報電話會議摘要（Yahoo Finance / Motley Fool）","url":null,"excerpt":null,"as_of":"2026-04-30","retrieved_at":"20260929","affects":["thesis.H"],"status":"ok"},{"id":"supply_demand_durability#7","axis":"supply_demand_durability","section":"coverage","direction":"-","claim":"產業預估 2026 年全球 PV 模組需求將自 2025 年的 653–706 GWdc 降至 529–624 GWdc，為近十年來首次年度負成長","source":"搜尋摘要彙整（產業預估報告）","url":null,"excerpt":null,"as_of":"2026-04-30","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#8","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"中期展望（2027–2028）：全球太陽能裝機預估年增 10–20%，2028 年中位數估計達 760 GWdc；美國 EIA 預估太陽能發電 2026 年增 17%、2027 年再增 23%，主要受資料中心用電需求帶動","source":"搜尋摘要彙整（EIA / 產業預估）","url":"https://www.utilitydive.com/news/demand-growth-solar-2027-energy-information-administration/811941/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20260929","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Section 201 進口晶矽太陽能電池／模組安全防護關稅於 2026-02-06 到期，結束長達八年的對低價進口品限制","source":"Beveridge & Diamond (bdlaw.com) - Solar's Momentum At Mid-2026 Will Help It Overcome Snags","url":"https://www.bdlaw.com/publications/solars-momentum-at-mid-2026-will-help-it-overcome-snags/","excerpt":"Most notably, the Section 201 safeguard tariffs on imported crystalline silicon photovoltaic cells and modules expired on Feb. 6, ending an eight-year effort to address low-cost imports that were found to injure U.S. manufacturers.","as_of":"2026-02-06","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"+","claim":"美國川普政府對多晶矽（polysilicon）進口啟動 Section 232 國安調查行動，First Solar 表示此舉有助削弱中國在該供應鏈的掌控，並藉此撤回 USITC 337 條款申訴、轉向聯邦地方法院訴訟追討專利權","source":"Yahoo Finance - First Solar Recalibrates TOPCon IP Enforcement Strategy Following Section 232 Action","url":"https://finance.yahoo.com/energy/articles/first-solar-recalibrates-topcon-ip-000100185.html","excerpt":"The decision follows the Trump Administration's recent national security action on imports of polysilicon and its derivatives under Section 232 of the Trade Expansion Act, a move aimed at loosening China's grip on a critical supply chain. ... The Trump Administration's Section 232 action helps level the playing field at the border, and we are more determined than ever to enforce our IP rights and defend the rule of law here at home.","as_of":"2026-09-16","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"美國於2026年8月6日宣布 Section 232 太陽能關稅：對成品模組設 $0.38/瓦最低進口價、對部分多晶矽衍生品課15%關稅，2026年12月4日生效；First Solar 的 CdTe 模組不含多晶矽，作為最大美國本土模組製造商公開表態支持此措施。","source":"postregister.com — 'First Solar Applauds Comprehensive Section 232 Action on Polysilicon and Derivatives'; oilprice.com — 'Solar Stocks Up 40% YTD as Section 232 Tariff Decision Looms'","url":"https://www.postregister.com/businessreport/government/first-solar-applauds-comprehensive-section-232-action-on-polysilicon-and-derivatives/article_71bfa321-364b-550c-aa94-9e008938381b.html","excerpt":null,"as_of":"2026-08-06","retrieved_at":"20260929","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"中國自2025年2月起收緊含碲（tellurium）等五項關鍵礦物的出口管制，出口商須向中國商務部申請許可；碲是 First Solar CdTe 模組的主要原料之一，中國佔2024年全球精煉碲產量約76.53%。First Solar 10-K/10-Q 揭露已組建跨部門小組監控此風險、申請出口許可並尋求替代供應商。","source":"pv-magazine-india.com — 'China adds export restrictions for minerals used in thin-film solar'; First Solar SEC filings (10-K/10-Q risk factors, 搜尋摘要)","url":"https://www.pv-magazine-india.com/2025/02/11/china-adds-export-restrictions-for-minerals-used-in-thin-film-solar/","excerpt":null,"as_of":"2025-02-11","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"2026年2月20日美國最高法院裁定2025年依 IEEPA 對中國進口加徵的10%關稅違法，川普隨即撤銷該關稅並以 Section 122 全球關稅取代；First Solar 已申請 IEEPA 關稅退款，並於截至2026年6月30日止季度開始收到部分退款款項。","source":"FIRST SOLAR, INC. Form 10-Q for the quarterly period ended June 30, 2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000170/fslr-20260630.htm","excerpt":"In February 2026, the U.S. Supreme Court ruled the IEEPA tariffs unlawful.","as_of":"2026-02-20","retrieved_at":"20260929","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"First Solar 用 CdTe 薄膜技術,不吃矽晶圓/多晶矽那條由中國主導的供應鏈,因此較不受中國關聯的關稅與地緣風險影響","source":"pv magazine USA - Solar Manufacturing USA 2026","url":"https://pv-magazine-usa.com/2026/04/30/solar-manufacturing-usa-2026-production-and-technology-at-the-heart-of-u-s-solar/","excerpt":"First Solar's CdTe thin-film technology is independent from the silicon-polysilicon value chain dominated by Chinese manufacturers, which insulates it from geopolitical tensions, tariffs, and logistical risks affecting crystalline silicon competitors.","as_of":"2026-04-30","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"First Solar 的關鍵原料碲(tellurium)是煉銅的副產品,供應量跟著銅需求走;公司只跟少數幾家供應商採購,換供應商要走很長的資格審查,萬一斷供不容易及時補上","source":"First Solar 10-K (FY2015) 風險因子章節","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449416000067/fslr10-k12x31x2015.htm","excerpt":"First Solar currently purchases these raw materials from a limited number of suppliers, and because suppliers must undergo a lengthy qualification process, the company may be unable to replace a lost supplier in a timely manner and on commercially reasonable terms.","as_of":"2015-12-31","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"+","claim":"First Solar 產能刻意集中在美國本土(Ohio、Alabama、Louisiana),2026 Q1 美國廠稼動率 96%,出貨 3.8GW,公司稱這樣的本土集中讓自己不受全球地緣風險波動影響","source":"pv magazine USA - Solar Manufacturing USA 2026","url":"https://pv-magazine-usa.com/2026/04/30/solar-manufacturing-usa-2026-production-and-technology-at-the-heart-of-u-s-solar/","excerpt":"This deliberate concentration in Ohio, Alabama, and Louisiana creates a domestic industrial base optimized for serving large utility-scale projects and insulated from global geopolitical volatility.","as_of":"2026-04-30","retrieved_at":"20260929","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"因美國政策不確定性、中國模組流入歐洲、印度關稅政策等近期逆風,First Solar 宣布 2025 年把馬來西亞、越南廠的 Series 6 模組產能下修 1GW,重心轉向美國本土擴產","source":"TaiyangNews","url":"https://taiyangnews.info/business/first-solar-lower-1-gw-malaysia-vietnam-module-output","excerpt":"These items create near-term headwinds for our international production","as_of":"2025-03-05","retrieved_at":"20260929","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"截至 2025 年底前後,美國對越南(20%)、印度(25%)、馬來西亞(19%)課對等關稅;印度另以反傾銷/核准名單機制,大幅堵住中國電池模組借道東南亞轉銷印度的路","source":"SurgePV - Solar Import Duty Rates by Country","url":"https://www.surgepv.com/solar-compliance/global/import-duty-rates","excerpt":"Reciprocal tariff rates apply to Vietnam (20%), India (25%), and Malaysia (19%) as of late 2025. Additionally, India's tariff and non-tariff measures against Chinese cells and modules have largely eliminated the country as a destination from Malaysia and Vietnam product, including India's Basic Customs Duty and the Approved List of Models and Manufacturers.","as_of":"2025-12-31","retrieved_at":"20260929","affects":["thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"FSLR 2026 全年財測維持：模組出貨量 17.0–18.2 GW、淨銷售額 $4.90–5.20B（Q1'26 財報重申）。","source":"Gurufocus - First Solar (FSLR) Reports Record Q1 2026 Revenue and Strong Outlook","url":"https://www.gurufocus.com/news/8834541/first-solar-fslr-reports-record-q1-2026-revenue-and-strong-outlook","excerpt":"The company reaffirmed its 2026 outlook with expected module volumes of 17.0–18.2 GW and net sales of $4.90–$5.20 billion.","as_of":"2026-04-30","retrieved_at":"20260929","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"美國公共事業級（utility-scale）市場：Q1'26 起累計新簽 1.9 GW，其中 1.4 GW 為美國 utility-scale，均價 $0.35/W；截至 Q1'26 末在手訂單（backlog）47.9 GW，合約總價 $14.4B（不含技術加價），交付排到 2030 年。","source":"First Solar Q1'26 Earnings Presentation / earnings coverage aggregation","url":"https://s202.q4cdn.com/499595574/files/doc_financials/2026/q1/Q1-26-Earnings-Presentation-vf-Secured.pdf","excerpt":"First Solar secured gross bookings of 1.9 gigawatts, with 1.4 gigawatts booked in the US utility scale market at an average selling price of $0.35 per watt. The company maintains a backlog of 47.9 gigawatts valued at $14.4 billion.","as_of":"2026-04-30","retrieved_at":"20260929","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"截至 2026/6/30（Q2'26 末），backlog 降為 45.1 GW、合約總價 $13.6B，交付仍排到 2030 年——較 Q1'26 末的 47.9 GW / $14.4B 略減，屬正常出貨消耗 backlog。","source":"First Solar Q2'26 10-Q / earnings coverage aggregation","url":"https://www.sec.gov/Archives/edgar/data/0001274494/000127449426000170/fslr-20260630.htm","excerpt":"More recently, as of June 30, 2026, the backlog was 45.1 GW valued at $13.6B through 2030.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"印度市場：Q1'26 新簽 0.8 GW、均價僅 $0.20/W，明顯低於美國 utility-scale 的 $0.35/W，反映印度段定價力較弱、屬較低毛利的地區市場。","source":"First Solar Q1'26 earnings coverage aggregation","url":"https://www.theglobeandmail.com/investing/markets/markets-news/Motley%20Fool/1633246/first-solar-fslr-q1-2026-earnings-transcript/","excerpt":"During Q1 2026, First Solar achieved gross bookings of 1.7 GW during the quarter (0.9 GW U.S. at $0.34/watt average; 0.8 GW India at $0.20/watt average)","as_of":"2026-04-30","retrieved_at":"20260929","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"CURE 技術加價（technology adjuster）預計 2028 年前複製到 Series 6/7 全系列產能，若達成可為 backlog 帶來最多 $600M 額外營收，主要落在 2027–2028 年。","source":"First Solar Q1'26 earnings coverage aggregation","url":"https://www.fool.com/earnings/call-transcripts/2026/04/30/first-solar-fslr-q1-2026-earnings-transcript/","excerpt":"CURE technology is scheduled to be replicated across the Series 6 and 7 fleet through 2028, which, if achieved, supports the potential realization of up to $600 million of additional revenue from technology adjusters in the backlog, with the majority anticipated in 2027 and 2028.","as_of":"2026-04-30","retrieved_at":"20260929","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"+","claim":"美國 utility-scale 太陽能終端需求：2026 年美國公共事業級太陽能發電量預期較 2025 年成長（290 BkWh → 2027 年 424 BkWh），2026 年計劃新增 43.4 GW 公共事業級容量，較前一年增加 60%；本地含量合規模組供給短缺預期至少延續到 2027 年。","source":"EIA - Today in Energy","url":"https://www.eia.gov/todayinenergy/detail.php?id=67205","excerpt":"Utility-scale solar is the fastest-growing source of electricity generation in the United States, increasing from 290 BkWh in 2025 to 424 BkWh by 2027... developers plan to add 43.4 GW of new utility-scale solar capacity in 2026, a 60% increase in capacity additions from last year if realized. Demand for Domestic Content–eligible modules will continue to outstrip available compliant supply through at least 2027.","as_of":"2026-01-01","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"+","claim":"美國本土模組製造產能 2025 年底達 65.5 GW，較 2024 年底 42.5 GW 成長逾 50%，但 Section 232 關稅預期推升美國模組價格至 2027 年（因本土電池片產能多數要到 2026 年底才有意義放量）。","source":"Intertek CEA / SolarStock USA market brief aggregation","url":"https://www.solarstockusa.com/research/market-brief-2026-q2","excerpt":"Intertek CEA forecasts rising U.S. module prices through 2027, driven by potential Section 232 tariffs on polysilicon and constrained domestic cell supply, with most planned U.S. cell factories not expected to ramp meaningfully until late 2026. U.S. domestic solar module manufacturing capacity reached 65.5 GW at the end of 2025, up more than 50% from 42.5 GW at the end of 2024.","as_of":"2026-01-01","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"-","claim":"全球（非 FSLR 所在的關稅保護利基）結晶矽模組市場：2026 年預估為十餘年來全球 PV 需求首次負成長（529–624 GWdc），全球產能逾 1,100 GW 對僅約 650 GW 裝機需求，模組價格崩至約 $0.10/W，遠低於 TOPCon 約 $0.16/W 的生產成本；此為中國結晶矽產能過剩導致，與 FSLR 受美國關稅/本土含量保護的薄膜（CdTe）利基市場性質不同。","source":"InfoLink Consulting / pv magazine aggregation","url":"https://www.infolink-group.com/energy-article/solar-topic-solar-pv-supply-chain-marks-industry-trough-the-beginning-restructuring","excerpt":"2026 is projected to mark the first year of negative growth in global PV demand in over a decade, with module demand forecast to decline to 529–624 GWdc... Global module manufacturing capacity sits above 1,100 GW against roughly 650 GW of installation demand, and polysilicon spot prices have fallen 84% from the 2022 peak... global module prices collapsed to approximately USD 0.10 per watt, a figure that severely undercuts the actual production costs of even the most advanced TOPCon manufacturing lines, which hover around USD 0.16 per watt.","as_of":"2026-01-12","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"0","claim":"FSLR 為全球最大薄膜（CdTe）太陽能模組製造商，佔全球薄膜技術市場約 45%；薄膜技術在印度 2026 年 ALMM 掛牌模組製造產能中僅佔約 2%，印度年產模組中薄膜約估 8–12%。","source":"Statista / IndexBox aggregation","url":"https://www.statista.com/topics/2737/first-solar/","excerpt":"First Solar is the world's largest thin film PV solar module manufacturer, and the company accounts for roughly 45 percent of the market for this solar technology globally... thin-film technology represented 2% of ALMM-listed module manufacturing capacity as of June 2026.","as_of":"2026-06-01","retrieved_at":"20260929","affects":["moat_trend"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"矽晶太陽能效率持續提升、成本下降，可能使 CdTe 與矽晶的效率差距擴大到租稅抵減也難以彌補的程度","source":"FinancialContent - The American Solar Champion: An In-Depth Research Feature on First Solar (FSLR)","url":"https://markets.financialcontent.com/stocks/article/finterra-2026-4-15-the-american-solar-champion-an-in-depth-research-feature-on-first-solar-fslr","excerpt":"If crystalline silicon efficiency continues to climb while costs fall, the \"gap\" between CdTe and silicon might become too wide for tax credits to bridge.","as_of":"2026-04-15","retrieved_at":"20260929","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"+","claim":"First Solar 正開發 CdTe-Perovskite 疊層電池，目標突破 25% 效率門檻；若試產成功，市場可能重新評價其為技術領先者而非單純製造商","source":"FinancialContent - The American Solar Champion: An In-Depth Research Feature on First Solar (FSLR)","url":"https://markets.financialcontent.com/stocks/article/finterra-2026-4-15-the-american-solar-champion-an-in-depth-research-feature-on-first-solar-fslr","excerpt":"By layering its traditional CdTe with a material called Perovskite, the company aims to break the 25% efficiency barrier. Any successful pilot of the CdTe-Perovskite tandem cell could trigger a re-rating of the stock as a technology leader, not just a manufacturing play.","as_of":"2026-04-15","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"0","claim":"First Solar 官方技術頁預告 CdTe 電池效率目標為 2025 年前達 25%、2030 年前達 28%，並規劃結合 CdTe 與 c-Si（結晶矽）半導體技術優點的疊層產品","source":"First Solar - Our Technology (CdTe)","url":"https://www.firstsolar.com/en/Technology/CadTel","excerpt":"forecast a thin film CdTe entitlement of 25% cell efficiency by 2025 and pathways to 28% cell efficiency by 2030; development of CdTe bifacial modules and tandem products that incorporate the best aspects of both CdTe and c-Si semiconductor technologies","as_of":"2026","retrieved_at":"20260929","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#none","axis":"channel_business_model_shift","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"GLJ Research 於 2026-09-23 調降 FSLR 目標價，從 $315 降到 $250（維持 Buy 評等）","source":"ad-hoc-news.de - First Solar stock falls 4.07 percent as GLJ cuts its target","url":"https://www.ad-hoc-news.de/boerse/news/corporate-news/first-solar-stock-falls-4-07-percent-as-glj-cuts-its-target/70178125","excerpt":"GLJ Research kept a Buy rating but cut its price target from USD 315.00 to USD 250.00","as_of":"2026-09-23","retrieved_at":"20260929","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"KeyBanc 分析師 Sophie Karp 於 2026-09-28 將 FSLR 評等從 Underweight 上調至 Sector Weight（未附目標價），理由是估值面","source":"web search aggregation citing KeyBanc rating action (title unclear, e.g. Benzinga/MarketBeat analyst ratings feed)","url":null,"excerpt":null,"as_of":"2026-09-28","retrieved_at":"20260929","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"First Solar 在 2026 年多次法說（Q1、Q2）維持全年財測不變，未上修也未下修","source":"pv magazine USA - First Solar reaffirms 2026 guidance as CuRe launch and record India sales drive Q1 margin expansion","url":"https://pv-magazine-usa.com/2026/05/01/first-solar-reaffirms-2026-guidance-as-cure-launch-and-record-india-sales-drive-q1-margin-expansion/","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20260929","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 2026（2026-07-30 發布）財報，公司全年營收財測中值約 $5.05B，較分析師預估低約 0.7%；EPS $3.92 優於 Zacks 共識 $2.74","source":"StockStory - First Solar (NASDAQ:FSLR) Misses Q2 CY2026 Revenue Estimates","url":"https://stockstory.org/us/stocks/nasdaq/fslr/news/earnings/first-solar-nasdaqfslr-misses-q2-cy2026-revenue-estimates","excerpt":null,"as_of":"2026-07-30","retrieved_at":"20260929","affects":["thesis.H","valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"分析師目標價分布區間曾達 $330（UBS，2026-06-11 給出的高值）至 $150（KeyBanc，2025-10-31 給出的低值）","source":"WallStreetZen - First Solar Stock Forecast & Predictions","url":"https://www.wallstreetzen.com/stocks/us/nasdaq/fslr/stock-forecast","excerpt":null,"as_of":"2026-06-11","retrieved_at":"20260929","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"First Solar 面臨證券詐欺集體訴訟，集體期間為 2025-02-26 至 2026-02-24，指控公司誇大將產能從馬來西亞／越南轉移至美國以規避關稅的能力；多家律所（Schall Law、SBS Law、Gross Law、Levi & Korsinsky）發布投資人徵集公告，求償律師徵集截止日為 2026-08-24。","source":"GlobeNewswire / PRNewswire investor alert press releases","url":"https://www.globenewswire.com/news-release/2026/08/03/3337706/0/en/fslr-investors-have-opportunity-to-lead-first-solar-inc-securities-fraud-lawsuit-with-sbs-law.html","excerpt":"FSLR Investors Have Opportunity to Lead First Solar, Inc. Securities Fraud Lawsuit with SBS Law","as_of":"2026-08-03","retrieved_at":"20260929","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"First Solar 於 2011 年曾就 Topaz Solar Farm 未能如期取得聯邦貸款擔保一事，向 SEC 揭露啟動內部調查（Regulation FD 相關）；該調查已於 2014 年結案，屬歷史事件、不在近 12 個月窗口內。","source":"Probes Reporter, LLC","url":"https://probesreporter.com/news/watch-list-update-undisclosed-sec-investigation-first-solar-now-over","excerpt":"Watch List Update: Undisclosed SEC Investigation of First Solar is Now Over","as_of":"2014-12-01","retrieved_at":"20260929","affects":["thesis.R"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"0","claim":"全球太陽能模組產能在2025年已達約800GW，遠超過同年約450GW的新增裝機量，供過於求局面延續","source":"TheEnergyBrief - PV Module Manufacturers' New Reality 2026","url":"https://www.theenergybrief.org/en/articles/global-solar-pv-module-manufacturing-new-reality-2026","excerpt":"total global PV module capacity reached approximately 800 GW in 2025, while global new installations that year were only about 450 GW","as_of":"2026-07-19","retrieved_at":"20260929","affects":["thesis.bear","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"中國龍頭LONGi與Jinko仍持續擴大電池產能，LONGi的HPBC電池產能預計2026年底達50GW、Jinko的N型TOPCon產能超過60GW，顯示同業並未收縮新產能","source":"TheEnergyBrief - PV Module Manufacturers' New Reality 2026","url":"https://www.theenergybrief.org/en/articles/global-solar-pv-module-manufacturing-new-reality-2026","excerpt":"LONGi Green Energy's HPBC cell capacity expected to reach 50 GW by the end of 2026, and Jinko's N-type TOPCon capacity exceeding 60 GW","as_of":"2026-07-19","retrieved_at":"20260929","affects":["moat_trend"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"中國多晶矽廠商推動協調性「自律」減產與整合，加上出口退稅取消，帶動模組價格在2025Q4至2026H1轉為上漲，顯示部分供給紀律正在形成","source":"搜尋摘要（surgepv／pv-magazine-india 2026年太陽能供應鏈報導）","url":null,"excerpt":"Module prices increased in Q4 2025 and continued to face upward pressure in H1 2026, driven by a combination of Chinese supply-side rationalization, production discipline, consolidation in the polysilicon sector, and the removal of China's photovoltaic export tax rebate.","as_of":"2026-06-30","retrieved_at":"20260929","affects":["moat_trend","thesis.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"美國同業Qcells在喬治亞州Cartersville廠已開始生產矽晶太陽能電池，3.5GW電池線預計2026年第三季達全產能，屬美國本土新增產能","source":"Solar Power World Online","url":"https://www.solarpowerworldonline.com/2026/06/qcells-starts-production-of-solar-cells-in-united-states/","excerpt":"Qcells has begun manufacturing silicon solar cells at its integrated factory in Cartersville, Georgia, and expects to reach full production of the 3.5-GW cell line by Q3 2026","as_of":"2026-06","retrieved_at":"20260929","affects":["moat_trend","thesis.bear","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"-","claim":"美國同業T1 Energy 2026年模組產量預計3.1-4.2GW（2025年為2.79GW），德州Milam County的2.1GW電池廠第一期預計2026年第四季開始投產，屬未來12-24個月內的新增美國本土產能","source":"pv magazine USA","url":"https://pv-magazine-usa.com/2026/05/14/how-t1-energy-is-ramping-up-multi-gigawatt-u-s-solar-manufacturing/","excerpt":"We produced 2.79 GW of modules in 2025. We expect to manufacture between 3.1 and 4.2GW of modules this year... Phase 1 will be a 2.1-gigawatt fab...we remain on track to begin cell production in the fourth quarter of 2026.","as_of":"2026-05-14","retrieved_at":"20260929","affects":["moat_trend","thesis.bear","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"中國太陽能電池庫存持續下降，產業重心轉向需求復甦與庫存去化，但模組價格在 8 月兩輪調漲後又回落","source":"EnergyTrend","url":"https://www.energytrend.com/pricequotes/20260724-51816.html","excerpt":"Cell Production Cuts Begin to Take Effect; Market Focus Shifts to Market Demand Recovery and Inventory Destocking","as_of":"2026-07-24","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"美國模組價格因反傾銷/反補貼稅及 FEOC（受關注外國實體）規定收緊，2026 Q1 中位價來到 $0.28/W，較 2025 年初 $0.25/W 上升；PERC 模組價格 2025/11–2026/2 上漲 20%","source":"pv magazine USA","url":"https://pv-magazine-usa.com/2026/04/03/u-s-solar-module-prices-face-upward-pressure-as-trade-risks-and-feoc-rules-dominate-q1-2026/","excerpt":"median solar module pricing in the United States reached $0.28 per watt as the market adjusted to intensified trade enforcement and new Foreign Entity of Concern compliance requirements","as_of":"2026-04-03","retrieved_at":"20260929","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"中國 TOPCon 模組出口基準價（CMM）2026 年 6 月底維持在 $0.113/W，Q4 2026 及 2027 年遠期交貨報價因下半年需求預期轉弱而下滑","source":"pv magazine Global","url":"https://www.pv-magazine.com/2026/07/03/china-solar-module-forward-prices-ease-amid-softer-europe-demand/","excerpt":"The Chinese Module Marker (CMM) benchmark assessment for TOPCon modules FOB China held steady at $0.113/W with spot price indications ranging between $0.110/W and $0.117/W in late June 2026","as_of":"2026-06-30","retrieved_at":"20260929","affects":["decision_inputs.bear"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"-","claim":"First Solar 合約在手訂單（backlog）截至 2026/6/30 降至 45.1GW、約 $13.6B，較 2025 年底的 50.1GW 下降；當季出貨 7.6GW、新增訂單僅 2.8GW，取消訂單多於新單","source":"PV Tech / Investing.com（First Solar Q2 2026 財報）","url":"https://www.pv-tech.org/first-solar-reaffirms-2026-outlook-as-backlog-reaches-45-1gw/","excerpt":"First Solar's contracted backlog stood at 45.1 GW valued at approximately $13.6 billion as of June 30, 2026, down from 50.1 GW at year-end 2025","as_of":"2026-06-30","retrieved_at":"20260929","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"全球太陽能模組均價在 2011-2013 這輪下行崩跌：2011 年 $1.37/Wp，2012 年跌到 $0.79/Wp（跌 42%），2013 年初再跌 18% 到 $0.65/Wp","source":"pv magazine India - Solar industry faces collapse amid surplus and plunging prices","url":"https://www.pv-magazine-india.com/2024/08/28/solar-industry-faces-collapse-amid-surplus-and-plunging-prices/","excerpt":null,"as_of":"2013-01-01","retrieved_at":"20260929","affects":["cyclical_downside_scenario","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"First Solar 上一次下行谷底在 2022 年：Q1 2022 毛利率驟降到 3.1%，全年僅 2.67%；之後強力回升，2023 年回到 39.19%，2025 全年約 41%","source":"stock-analysis-on.net - First Solar Inc. Analysis of Profitability Ratios","url":"https://www.stock-analysis-on.net/NASDAQ/Company/First-Solar-Inc/Ratios/Profitability","excerpt":null,"as_of":"2022-12-31","retrieved_at":"20260929","affects":["cyclical_downside_scenario","moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"PV 產業上一輪製造業下行約持續 2012-2014 年（2-3 年）；目前這輪下行預期延續到 2026 年，是近 20 年來第二次大型 PV 製造業下行","source":"pv-tech.org - PV manufacturing downturn to extend into 2026","url":"https://www.pv-tech.org/pv-manufacturing-downturn-to-extend-into-2026/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20260929","affects":["cyclical_downside_scenario","triggers"],"status":"ok"},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"證券詐欺集體訴訟，集體期間 2025-02-26 至 2026-02-24，指控公司對關稅因應能力／產能轉移美國之陳述不實；多家律所公告徵集投資人，求償律師徵集截止日 2026-08-24。","source":"GlobeNewswire / PRNewswire / Businesswire investor alerts","url":"https://www.globenewswire.com/news-release/2026/07/24/3332917/0/en/fslr-investors-have-opportunity-to-lead-first-solar-inc-securities-fraud-lawsuit-with-the-schall-law-firm.html","excerpt":"FSLR Investors Have Opportunity to Lead First Solar, Inc. Securities Fraud Lawsuit with the Schall Law Firm","as_of":"2026-07-24","retrieved_at":"20260929","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 1 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"FSLR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":44.02,"operating_margin_pct":33.65,"fcf_margin_pct":27.89,"rd_intensity_pct":5.02},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.FSLR","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"CSIQ","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":16.43,"operating_margin_pct":-0.55,"fcf_margin_pct":-31.42,"rd_intensity_pct":1.67},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CSIQ","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"JKS","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":4.75,"operating_margin_pct":-6.7,"fcf_margin_pct":null,"rd_intensity_pct":1.64},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JKS","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ENPH","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":46.95,"operating_margin_pct":8.72,"fcf_margin_pct":11.49,"rd_intensity_pct":13.85},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ENPH","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"FSLR"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/FSLR/FSLR_Q2_2026_Earnings_Call_20260730.md）

# Q2 2026 Earnings Call
2026-07-30

Q2 2026 Earnings Call
First Solar, Inc. | Earnings Calls | 2026-07-30
Operator (Operator)
Good afternoon, and welcome to First Solar's Second Quarter 2026 Earnings Conference Call. This call
is being webcast live on the Investors section of First Solar's website at investor.firstsolar.com.
[Operator Instructions] And please note that today's call is being recorded. I would now like to turn the
conference over to your host, Byron Jeffers, Head of Investor Relations.
Byron Jeffers (Executives)
Good afternoon, and thank you for joining First Solar's Second Quarter 2026 Earnings Call. With me
today are Mark Widmar, Chief Executive Officer; and Alex Bradley, Chief Financial Officer. Mark will
begin with second quarter highlights, followed by Alex, and then we'll open the line for questions.
Today's discussion contains forward-looking statements. Actual results may differ materially due to
risks and uncertainties as described in our earnings press release and other SEC filings and the
earnings material available at investor.firstsolar.com. We undertake no obligation to update these
statements due to new information or future events. We will also reference certain non-GAAP financial
measures. Reconciliations to the most directly comparable GAAP measures are in our earnings press
release and presentation. This non-GAAP financial information is not intended to be considered in
isolation or as a substitute for financial information presented in accordance with U.S. GAAP. With
that, I will turn it over to Mark.
Mark Widmar (Executives)
Thank you, and good afternoon. Beginning on Slide 4, we delivered both record second quarter and
first half sales volume and improved financial performance relative to the prior year. During the
quarter, we generated over $1 billion in net sales, expanded gross margin to approximately 57% and
delivered strong adjusted EBITDA performance. We also surpassed an important milestone for First
Solar, exceeding 100 gigawatts of cumulative module sales globally. We view this as a reflection of the
trust customers have placed in First Solar over the more than 2.5 decades and the durability of our
technology and manufacturing platform. We ended the quarter with approximately 45.1 gigawatts of
contract backlog, we delivered -- with deliveries extending through the end of the decade,
demonstrating the demand for our differentiated technology platform, domestic manufacturing
footprint and delivery certainty.
Turning to manufacturing. Our U.S. facilities continued to operate at high utilization rates during the
quarter. In South Carolina, the first phase of the finishing facility remains on track to begin production
in the second half of 2026, with equipment installations progressing as expected. For the second phase,
we now expect completion in mid-2027. While the revised timing reflects a number of factors
associated with optimizing the facility's launch, it also enables the earlier incorporation of CuRe
technology. We are pleased with the performance of CuRe, with both high-volume manufacturing at
our Perrysburg facility and performance data from field deployments across multiple climates
exceeding expectations.

We believe incorporating the technology closer to the onset of the facility's commercial launch will
simplify execution, accelerate value realization and enhance customer value and the facility's long-term
financial performance. Once completed, the South Carolina facility is expected to provide up to 3.5
gigawatts of finishing capacity for modules initiated at our international manufacturing sites, giving us
greater flexibility to optimize our supply chain flexibility while also optimizing freight, tariff, domestic
content and Section 45X economics.
With respect to our international manufacturing fleet, production planning and utilization levels in
Malaysia and Vietnam continued to be influenced by U.S. market demand drivers and economics,
including the pending Section 232, polysilicon and derivative investigation and tariffs. We expect
greater policy clarity will help inform the long-term operating profile for the approximately 1.8
gigawatts of fully finished international capacity that remains available after accounting for capacity
being used to produce semi-finished product destined for our new South Carolina finishing line.
A note on manufacturing optimization and allocation. Approximately 41 gigawatts of our 45-gigawatt
backlog includes some form of domestic content requirement. These requirements vary significantly
and range from requiring exclusive supply from U.S. fully integrated factories to blending U.S.-made
supply with both fully integrated domestic factories as well as product from our upcoming South
Carolina finishing line to a domestic content points requirement, which is factory agnostic, allowing
blending of product from across our global fleet. We, therefore, continually balance and refine our
module supply and demand allocation across the fleet to meet customer contractual obligations,
optimize factory throughput and optimize gross margin.
This typically means that over a period of time, we will seek to maximize production and sales, firstly,
from our fully integrated U.S. factories. Secondly, from our South Carolina finishing line. And thirdly,
from our international facilities. As it relates to perovskites, we continue to advance our development
program for this potentially significant technology platform. Our previously announced development
line continues to progress -- to process improved efficiency and reliability attributes on smaller form
factor modules, while our Series 6 form factor pilot line remains on schedule and is expected to reach
operational readiness in the first half of 2027. Our continued progress has given us confidence as we
continue to invest substantial capital in our efforts to realize the commercialization of perovskites.
Earlier today, we published our latest corporate responsibility report, reinforcing our conviction that
how and where solar technology is made matters. The report details how we create enduring value by
developing, sourcing, manufacturing and recycling solar modules domestically, supporting jobs and
communities, strengthening industrial capacity and help ensure the benefits are realized locally. It also
highlights our continued focus on responsible manufacturing, supply chain transparency, workforce
development and resource efficiency. The report reflects the effectiveness of a business model where
corporate responsibility isn't a construct but the default.
Before turning the call over to Alex, I want to briefly address the market and policy environment and
how it is informing our commercial approach. The underlying drivers for utility-scale solar remain
intact, including load growth, data center development, electrification, aging generation assets and the
need for affordable, scalable new capacity. The policy landscape continues to evolve, particularly as it
relates to pending outcome for the Section 232, polysilicon and derivatives investigation as well as final
FEOC regulations. In this environment, we continue to prioritize pricing, contract quality, appropriate
risk allocation and long-term value over short-term bookings volume. Relative to the beginning of the

year, we are seeing increased customer engagement. And as policy clarity improves, we believe First
Solar remains well positioned to capitalize on these opportunities. With that, I'll now turn the call over
to Alex to discuss our bookings, financial results and outlook.
Alexander Bradley (Executives)
Thanks, Mark. Beginning on Slide 5, as of June 30, 2026, our contracted backlog totaled 45.1 gigawatts,
with an aggregate transaction value of $13.6 billion, exclusive of technology adjusters, with scheduled
deliveries extending through 2030. Early this month, Cypress Creek Energy broke ground on the Steel
River Energy Center in Arkansas, a project utilizing First Solar modules and previously included in our
contracted backlog. The initial phase is expected to provide approximately 1.6 gigawatts of solar
generation capacity and 1.9 gigawatt hours of battery storage to support Google's growing energy needs,
with the opportunity for future expansion.
Since our last earnings call, we recorded approximately 1.9 gigawatts of additional U.S. gross bookings
at an average selling price of approximately $0.36 per watt, inclusive of applicable technology
adjusters. While near-term customer activity continues to be influenced by the current policy
environment discussed by Mark, our fully integrated domestic manufacturing fleet remains
substantially committed through 2028, providing a high degree of volume and pricing visibility. Given
the limited amount of uncommitted domestic capacity available over the next several years, we
continue to be disciplined in evaluating incremental contracting opportunities.
We also initiated our first customer notifications related to contractual CuRe adjusters during the
quarter, an important milestone in beginning to translate CuRe's performance benefits from potential
ASP adjusters into backlog value and future revenue realization. We expect the contribution from these
adjusters to increase as CuRe deployment expands across our contracted portfolio. As a reminder, we
expect limited ASP upside from CuRe sales in 2026, largely as a function of contractual notification
deadlines relative to the timing of decision to recommence CuRe production.
Turning to India. Our guidance continues to assume production is largely sold domestically in a short-
cycle book-and-bill market, with the factory operating at a high utilization rate. India gross bookings
during the first half of the year totaled approximately 1.1 gigawatts, an average selling price of
approximately $0.20 per watt. Given the shorter contracting cycle of the domestic India market,
booking economics generally provide a reasonable indicator of near-term revenue realization, subject
to normal foreign currency movements.
Turning to Slide 6. Net sales for the second quarter were approximately $1.06 billion, a decrease of
approximately 4% year-over-year. The decrease was primarily driven by lower revenue associated with
customer contract terminations recognized in the prior year period, partially offset by higher module
volumes sold. Gross margin was approximately 57%, an increase of approximately 12 percentage points
compared to the second quarter of 2025. The increase was primarily driven by an estimated $89
million net IEEPA tariff-related benefit, higher mix of modules qualifying for Section 45X tax credits
and lower logistics costs.
The net IEEPA tariff-related benefit reflects our current estimate of expected recoveries related to
commercial obligations and other tariff-related considerations and remains subject to refinement as
additional information becomes available. These benefits were partially offset by lower termination-
related revenue and higher duties and tariffs. While logistics costs improved year-over-year, the quarter

included higher over-the-road freight costs driven by overall capacity tightening and volatility in diesel
costs. These impacts were partially offset by higher sales freight recovery.
Operating expenses were approximately $155 million, including $76 million of R&D expense. R&D
increased year-over-year, primarily reflecting continued investment in perovskite development and the
impairment of certain R&D equipment that is no longer expected to be used as part of our technology
road map. Net income was $423 million, up approximately 24% year-over-year. Adjusted EBITDA was
$644 million, above the high end of our previously communicated Q2 preview range with an adjusted
EBITDA margin of 61%.
Moving to Slide 7. We ended the quarter with approximately $1.7 billion of net cash, providing
substantial balance sheet strength and financial flexibility while remaining within our targeted long-
term cash range of $1.5 billion to $2 billion. Operating cash outflows year-to-date were $360 million,
reflecting first half working capital dynamics and improved compared to outflows of $458 million
during the first half of 2025. First half capital expenditures were $280 million, primarily supporting
our South Carolina finishing facility and technology investments. We completed the full prepayment of
our India DFC loan during the quarter.
Turning to Slide 8. Our full year 2026 guidance remains unchanged. With that said, our guidance now
assumes a net tariff impact of $60 million to $80 million, with updates including the previously
mentioned net IEEPA recovery and the assumption of Section 301 tariffs in the second half of the year.
We also forecast offsetting updates between production start-up expense and R&D expense as well as
incremental freight costs due to certain nonrecoverable domestic freight expenses above our previously
assumed forecast, largely driven by changes in module delivery locations. And note, in some cases,
domestic freight costs are now approaching international shipping economics.
For the third quarter, we expect volumes sold between 3.9 gigawatts and 4.5 gigawatts and adjusted
EBITDA between $625 million and $775 million. In summary, our first half performance and
reaffirmed outlook reflect the strength of our strategy of reshoring and scaling domestic manufacturing,
progressing our technology road map and maintaining a selective approach to new bookings in light of
key pending trade and policy determinations. As we look ahead, our priorities remain unchanged. We
remain focused on disciplined execution, serving our customers, advancing our technology road map,
managing capital prudently and maintaining financial flexibility. And with that, operator, please open
the line for questions.
Operator (Operator)
[Operator Instructions] Your first question comes from the line of Jon Windham with UBS.
Jonathan Windham (Analysts)
Perfect. Congratulations on the result, and appreciate you taking the questions. So obviously, the FCC
had a ruling about solar inverters a couple of days ago. And I think on one side, it goes along to show
how serious the government is in promoting domestic content within -- especially electrical equipment
hardware, which is obviously very good for you given your position in domestic solar modules. But just
curious if you have any early thoughts on potential impact on broader solar installations and the ability
to work around -- the industry to work around that provision.
Mark Widmar (Executives)

Yes. Thanks, Jon. Look, I think it continues the theme of our U.S. government trying to ensure that we
don't have any overreliance on adversarial countries. And obviously, China being one of them in
particular. I think the good thing about this is that the industry has started to get ahead of trying to find
domestic supply chains, comprehensive domestic supply chains. We obviously were an early industry
leader in that regard of reshoring manufacturing and creating a supply chain here in the U.S. for our
U.S. operations. You're seeing this now really across all components of equipment suppliers, all the way
up even to try to find localizations for the battery supply chain as much as you can.
So I don't see it being a constraint near term. I think the current models that have been shipping into
the U.S. will continue to be allowed to be shipped into the U.S. I do think there is a theme or a message
there, though, that, that scrutiny may be stepped up as we move forward. But I think it just sends
another great signal to domestic manufacturers of, look, we need to move forward. We need domestic --
create domestic supply chain resiliency to enable not only the solar industry to thrive, but really all of
the industries that -- as we reindustrialize the U.S. economy, right? So again, I think it's a good
indicator of a continued theme and message that this administration has, and we fully support it.
Operator (Operator)
Your next question comes from the line of Brian Lee with Goldman Sachs & Co.
Brian Lee (Analysts)
Just had 2. I guess, first, on this Google Steel River project, appreciate you guys commenting on that. I
might have missed it, but how much of the 1.9 gigawatts in U.S. gross bookings came from that one
project in the quarter? And then how much more bookings potential exists on that project site? And
your bigger picture, maybe speak to how you're seeing general interest from the hyperscaler data center
community? And then second question I have is just kind of the customary latest thoughts, timing,
visibility into Section 232, how you're viewing the potential for floor prices in the $0.40 per watt or
higher range? And then how quickly do you move on your bookings funnel and Southeast Asia strategy
once you get clarity on this, presumably, hopefully, in the next few months?
Mark Widmar (Executives)
All right. Brian, I'll try to take kind of the first 2, and Alex will talk maybe a little bit about the views of
Southeast Asia. So make sure it's clear on the project that we announced with our partner, that we
supplied modules to for Cypress Creek. That is already in our bookings, okay? So that was just to
highlight. It's a great project. If you actually look at some of the more recent announcements that have
been made over the last several weeks, I think you kind of see a theme there. You've got a very large
project with Cypress, the one that we referenced that it will be Phase 1 of kind of call it the 1.6 gigawatts,
then it goes to Phase 2, which will be about 2.5 gigawatts. So that's a very large project. And I think the
battery component of that as well is going to be north of 2 gigawatts -- megawatt hours from a battery
standpoint. Really important strategic project. It's there to support Google.
We have 2 other projects that have been announced over the last couple of weeks. One with Terra-Gen,
which was about 1.4 gigawatts. And then we had another one with Panamint, which was another 1
gigawatt plus. So those 3 projects that have been announced recently are about 5 gigawatts of capacity.
The Panamint -- part of the Panamint volume was actually announced last quarter. So when we did the
announcements last week -- last quarter around bookings volumes, which I think we had in total is

around 1.4 gigawatts. Panamint was actually included in that volume. But I think it's a great message
that the demand is there. Half of that volume of that 5 gigawatts I referenced is directly communicated
and tied to Google as a hyperscaler. The other 2.5 gigs, they haven't disclosed the counterparties. But if
you look at the verbiage around the announcements on that, they'll reference a very large corporate
account, one of the largest companies in the U.S. You can kind of get a sense of the likelihood of who
that counterparty is going to be for that project.
So strong demand for -- continued demand for hyperscalers, really strong relationships and
partnerships with First Solar to support those types of strategic projects that really kind of thrive on the
importance of certainty, right? Those projects are strategic. They're important. They obviously include
storage as reflected in the Cypress Creek project. As I've always said, the first thing you need to do as
you're building out your project and derisking is that you need to make sure that you have a reliable
partner who can make sure those photons become electrons. Without that, the whole project can be
considered at risk. And we can deliver that certainty and that great technology and that reliability. So
we're seeing that in the marketplace and continued strong interest driven by, as currently still,
somewhat insatiable demand from hyperscalers.
As it relates to 232, I'll take the pricing piece and then Alex will talk to kind of how we thread that into
our views around Southeast Asia. Look, there's still a lot of views out there. I think everybody has a view
of how the construct may be with minimum import price and maybe with the tariff on top of that.
There's some views of whether there's quotas or not. All I can say is, it is still evolving. And we do
believe it'll be constructive. I don't want to give kind of our internal read of what we think it potentially
could be because there's still a lot of moving pieces. I can say that we're still in constant contact with the
appropriate parties at USTR and Commerce to continue to bring our voice into the conversation. And
we're still optimistic that the outcome will be constructive.
And we've used it as a reason to be disciplined, and we'll see what happens once it's finally announced.
And there's demand that's still sitting there on the sidelines. If you look at our cadence and our
momentum around our bookings, just here in the month of July, we booked almost 2 gigawatts in the
U.S. at very good prices, as Alex indicated. There's about 2 more gigawatts, north of 2 gigawatts that sits
into a contract that's subject to CP. And then I've got another 2 gigawatts of active conversations with
customers that there's a high probability we can close through by the end of the year. So -- and we'll see
how much that gets further catalyzed by a decision around 232.
Alexander Bradley (Executives)
Brian, as it relates to Southeast Asia capacity, we talked on the last couple of calls around looking at this
a bit like an option. So we're running somewhere around $30 million quarter of underutilization. Say,
we're running Southeast Asia manufacturing well below its theoretical capacity, about half of that's
cash, about half noncash. Given that we've been holding through the first half of the year, making a
decision on the long-term future there pending the outcome of 232, it makes sense to continue to do
that. So I'd still view this as we're waiting for the outcome of that policy.
And just to frame the amount, if you were to go back and look at the slides we put out in our February
call, it shows you nameplate capacity of production. So we originally had about 7 gigawatts of total
capacity sitting in Malaysia, Vietnam, about half of that is going to be dedicated to production that will
feed our new finishing line in South Carolina. So there's about 3.5 gigawatts left. Of that, we did take
out some tools, bring them over to the U.S. to reuse in our perovskite work. So ultimately, it leaves us

with about 1.8 gigawatts of end-to-end fully finished capacity that we could ramp up in -- across
Malaysia, Vietnam. So it's about that 1.8 gigawatts that we're talking about, we're thinking -- we're
holding a decision on pending the outcome of the 232.
Operator (Operator)
Your next question comes from the line of Praneeth Satish with Wells Fargo.
Praneeth Satish (Analysts)
Maybe just going back to Section 232, obviously, there's a lot in play and I recognize that. But we've
heard, and you mentioned the potential for waivers or quotas being allowed for certain domestic cell
producers that could exempt them from some of these policy changes. I guess I'm just curious
conceptually, from your perspective, if some of these waivers are granted, do you think that could mute
some of the price upside from Section 232? Or do you still see a constructive supply-demand setup?
Just trying to think conceptually how you think about that.
Mark Widmar (Executives)
I mean obviously, any modifications versus 100% restriction will create some potential dilutive impact
to the strategic intent of the 232. It also depends on if there is a waiver of some type or a quota of some
type, I mean how big is it? And does it scale down over time? I mean is it something that is
implemented initially and then we'll walk down to maybe complete elimination of it? So it's hard to give
you a great insight to the impact. Clearly, we're not -- we're advocating to try to minimize any of those
impacts and as well as they should only be a limited duration to the extent that they're enabled or
allowed at all.
We really want to create a domestic supply chain, and any type of workarounds that you get will
disincentivize the investments that need to be made here in the U.S., right, to scale up those
capabilities. And I think it's much easier for people to understand the policy environment with certainty
versus creating uncertainty by waivers or quotas and those types of things that they can create. So we'll
have to wait and see. We're firm in our positions that we don't believe that they should be allowed, but
we'll have to see how the final outcome is.
Alexander Bradley (Executives)
And there's some history here, too. If you look back at the Section 201 tariffs and the exemption that
was put in place, bifacial technology, it was clear that, that exemption effectively gutted that provision.
So I think the administration has seen how those exemptions can effectively undermine what they're
trying to do. If there's a belief that the 232 provides a need around the national security interest, it
doesn't make a lot of sense to have a carve-out or a quota piece associated with a national security
interest provision.
Praneeth Satish (Analysts)
Got it. That makes sense. And then if we say that Section 232 goes through, you get some kind of
reasonable outcome, a positive outcome. You kind of mentioned that there's 4 gigawatts, it sounds like
4 gigawatts plus of kind of pending deals for the second half. But do you get the sense that there's more
demand sitting on the sidelines that's waiting for policy clarity? And once we get clarity, you could see
that number move up significantly higher. And then just a point of clarification, I guess, again, if

Section 232 goes through, you get a good outcome. On the Southeast Asia capacity, would you bring
that volume into the U.S. as finished products? Or would you -- would it come through as unfinished
and you would expand your U.S. finishing line?
Mark Widmar (Executives)
So I guess on the 232, and I'll let Alex take the other question around how we think through Southeast
Asia and whether it comes in as finished or partially finished or do we expand capacity for finishing
here in the U.S., I'll let Alex take that one. The -- there clearly are customers that are sitting on the
sidelines. There is absolutely no doubt about that. And even some of these that will -- even some of the
stuff subject to CP is somewhat tethered to posting of security. So one of the challenge is that, especially
as you get longer dated in terms of contracting some of this volume, and we are really trying to enforce
having cash liquid security against new bookings. That's been a priority of ours.
In some cases, some of the counterparties can't post the required security now. They're working
towards having that available. And to the extent that the security is posted then, it kind of closes out on
some of the CPs. So that's a piece of it. But there's clearly people sitting on the sidelines waiting to see
what happens. We have a couple of counterparties that are -- they're hedging their [ way ]. They know
that the risk is that ASPs may go up. But at this point in time, they're trying to wait and see how it plays
out. And again, just kind of the conversation last time, are there quotas or not? And what are the
options they have and so forth. So that's all being -- it's in the mix right now. And as we've always said,
the best thing for this industry is we just have clarity and certainty. And 232, we just really need a
decision on that because we can all understand how we move forward.
Alexander Bradley (Executives)
As it relates to what we could do with the Southeast Asia facilities, we could bring fully finished product
in subject to demand and pricing in the U.S. It's not only a function of where the 232 sits, it's also a
function of where other tariff provisions sit. So right now, we have a Section 301 that's just gone into
effect, replacing Section 122 tariffs that were in effect for the first half of this year. Those relate to
forced labor. There is still risk around 301 relating to excess capacity, so that investigation is ongoing.
Pending the outcome of that, obviously, we will determine what the total tariff impact could be then to
product coming in from Malaysia, Vietnam. We could bring some of it in as semi-finished WIP share
product and finish it in our existing U.S. facilities.
There's a limited amount, probably in the couple of hundred megawatt range of incremental capacity at
our finishing lines across existing fleet in Ohio. So we could do a little bit of that, but it's not effective to
run Malaysia at low throughput, as you're seeing with the underutilization costs we're having this year.
So really, what we're looking for is an ability to run that factory at close to full capacity. So then either
it's selling fully finished international product, subject to where tariffs end up or there is the potential
to build another finishing line in the U.S. That's subject, again, to finding available site with power and
the time it would take to build that out. So I think that's less likely, but it is still an option.
Operator (Operator)
Your next question comes from the line of Julien Dumoulin-Smith with Jefferies LLC.
Julien Dumoulin-Smith (Analysts)

Appreciate the opportunity. Quickly, actually, to follow up on that last line of thinking on bookings.
How do you think about the safe harbor having played into the latest quarter here, obviously July 4
being a relevant threshold? And also, again, that being a leading indicator for future sales into the later
part of the decade, how are you thinking about that? Obviously, that's a big part of your open book.
What are you thinking in terms of having safe harbor to acquire your initial customer conversations?
And then as a follow-up on what you were just alluding to there, can you elaborate a little bit more
around the permutations and the time line for that remaining piece in Southeast Asia? I know it's a
little bit of just an extension of the logic you were just delineating there, but can you expand a little bit
on the time line? It sounds like it's not that far off that you'll make a decision. Let me put it more
bluntly.
Alexander Bradley (Executives)
Maybe I'll just take that one. On the Southeast Asia, we're really waiting for the outcome of the 232. We
would expect to evaluate that and have a view shortly thereafter. It doesn't necessarily mean that we
will have an immediate action plan that relates to, say, a shutdown or a full capacity. But once we have
a sense of where the policy is, that'll allow us to evaluate it. It will take a little bit of time, though. We
want to make sure whatever policy comes through, we understand it and our customers also have a
chance to evaluate it and we can have discussions around whether there's a view of long-term offtake
potential from those facilities.
Mark Widmar (Executives)
Yes. And then on the -- I just want to make sure a couple of things. The bookings that we're reporting,
most of the bookings that we reported 1.9 gigawatts in U.S. volume, I think almost all of that was
outside of the quarter close. So most of that happened in July, which would also have been outside of
the safe harbor date. And most -- everyone has safe harbored with transformers. There's really no safe
harbor. I know there was -- I don't know, it was like maybe 10 days left in the quarter where there was a
ruling that was made that the decision that came out in August of the prior year where it said that you
eliminated the ability to use module or 5% CapEx rule to safe harbor. There was a ruling by one of the
courts that came out, I think, I don't know, somewhere like June 20, there was hardly any time left in
the quarter.
And that theory, you could use -- assuming that, that wasn't challenged, the theory you could use
modules to potentially safe harbor projects. But I mean that was really not an opportunity. It just
happened way too late. And most people had already safe harbored with the inverters or transformers,
excuse me, anyways. But as you go forward, it is an important component, especially for anything that
was safe harbored. If you safe harbored the first half of this year with ability to COD out into 2030,
there are stricter requirements from a FEOC standpoint at the project level that have to be met that I
think positions us well to serve that demand as you get out into '29 and '30 for when those projects
most likely could be commissioned.
Plus the other thing I would say is we are seeing -- there's a lot of kind of rigid interpretations a little
bit. And there are some people that are interpreting that even if something was safe harbored, let's say,
in the second half of '25, that if you do anything with a change order or assuming it was something from
an MSA to a PO or until a PO -- purchase order, excuse me, is actually generated, you have to always be

mindful of is there a restriction that you could have to comply with from a foreign entity perspective. So
there's a lot of like very conservative, which is right.
So people want to be airtight and not taking any risk to jeopardize their either ITC or PTC. And I think
there's a view towards maybe being overly conservative, advice they're getting from tax counsel and
others. And I think that's -- if I was in their situation, I clearly would do that as well. I don't want to put
anything at risk. So that safe harbor and those requirements under 48E as it relates to FEOC's
restrictions or requirements, I think will continue to play well for us as we look to book out through the
end of this decade.
Operator (Operator)
Your next question comes from the line of Philip Shen with ROTH Capital Partners.
Philip Shen (Analysts)
Just wanted to follow up on the 232, specifically on timing. We've been thinking it's August, but we've
seen a bunch of delays. The issue is, if it slips past August, then we go into September, and then that
gets closer to the midterms, then there's a chance that decision could push on that. Are they still
August? [Technical Difficulty] has shared that from an authorization standpoint.
Mark Widmar (Executives)
Phil, we're really having a hard time. We're having a really hard time. You're breaking up.
Philip Shen (Analysts)
How's it? Is it better?
Mark Widmar (Executives)
Try it again because it was really hard to get that.
Philip Shen (Analysts)
Okay. [Technical Difficulty] Anyway, we've been thinking it's August but there's a chance the 232 come
out in September or beyond. [Technical Difficulty] I have the policy 232 front and center. And so what's
your view, based on the folks that you guys are in touch with, that this should be August? Or do you
think there's a greater probability that this could slip into the fall or even beyond?
Mark Widmar (Executives)
Phil, I think I got your question. Look -- we share -- look, there's -- I know there's a lot that's in the mix
and what the administration's trying to evaluate when this is implemented. And we also want to make
sure they do, and what is implemented is -- achieves the strategic intent and the spirit of what it was set
out to do. So we are patient. We continue to be engaged. We are anxious as well as you are and others.
And as I indicated, the industry really needs the certainty of understanding. I can't give you any level of
conviction, maybe more than what you have right now. We are still getting signal that decisions will be
made. There are meetings that are being had that would indicate they're close to making a decision.
But we also want to make sure that this is done right. And so to give you some sense of my level of
confidence in August or whether it waits till September, I can't really give you a strong view on that. I
can just tell you we want this to be implemented with the achieving strategic intent and spirit of what it

was set out to do. And that's the most important thing, and we're going to continue to be engaged with
the administration to ensure that, that happens.
Operator (Operator)
Your next question comes from the line of Colin Rusch with Oppenheimer & Co.
Colin Rusch (Analysts)
Guys, are there opportunities for you to reduce input costs on the U.S. manufacturing? And can you
talk a little bit about the supply chain and how that's evolving? I know you'd had some discussions with
glass makers around capacity expansion and the capital needs that they have. But just curious about
how you might be able to look at that trend on a multiyear basis.
Mark Widmar (Executives)
Yes. Colin, I mean, it's -- it is challenging. We're still in this -- and especially in the U.S., as you see
more reshoring, pressure on commodities, the data centers are being built out, everything, obviously, as
you would expect, steel, aluminum, copper. We don't use silver, but obviously our competitors do. I
mean there's just a lot of pressure. Those -- you can look at fuel costs, and you can look at what's
happened in the Middle East. And I see that as more transitory in nature. And then in theory, once
that's resolved, then I think we'll have seen much more competitive fuel prices and what have you. The
electricity prices, at some of the locations in which we operate, we're dealing with some of those same
adverse impacts that others are. So we're in a pretty challenging rising commodity cost environment.
Now are we able to do things like drive more throughput through our operations? Absolutely. We're
focusing on continuing to do that. Are we finding ways to create further automation and capabilities
that can reduce labor costs? So there's levers that we're focused on. There's some redesign of the
product that we're looking at on trying to take costs out of the back rails of the frame. We continue to
look at glass and thickness and other things that we could do from that standpoint. But it's a pretty
challenging environment from a commodity cost standpoint. And our ability to get a lot of cost out, I
think, is probably one of the most challenging times that we've been in.
Now I will say that when you look at it on a cost per watt, not necessarily a cost per module, the great
thing about CuRe is that we have the opportunity to drive the efficiency up. So as we drive the efficiency
up, as we go from kind of where we are right now and add another 10, 15, 20, 30 watts, that'll help the
CPW numbers, right, cost per watt numbers, which is important, right? We need to drive that number
down. And then the ASP, the value uplift because of the energy attributes and the higher efficiency of
CuRe, then that drives to an entitlement for higher ASPs and the like. So that's what we're focused on,
and we're never going to give up on the input costs. We got to do the best we can to get cost out, but it is
a pretty challenging environment right now.
Alexander Bradley (Executives)
I'd also say that the potential to use the balance sheet to work with suppliers who are looking at
expansion or needing funding, there's an option there. We could try and leverage our position of
financial strength to get forward pricing that makes more sense. That has to be done at the right risk --
premium risk profile. And then the other thing I'd say is outside of just bill of material costs, obviously,
we're having a challenging time around period costs going from cost per watt produced over to cost per

watt sold. So again, we're seeing freight challenges as it relates to cost of trucking. And I think I
mentioned in the prepared remarks that we're seeing costs now to deliver product from Perrysburg over
to the West Coast of the U.S. are equivalent of delivering product from Asia to the West Coast of the
U.S. So continue to look how we can optimize our domestic transport routes, freight and try and
optimize between factories so that we can reduce those costs to the greatest extent possible.
Operator (Operator)
Our final question comes from the line of Corinne Blanchard with Deutsche Bank.
Corinne Blanchard (Analysts)
I actually want to come back on the last question regarding M&A and I think you just alluded a little bit
to it. But can you expand a little bit, what are you targeting with the current balance sheet that you
have? And it kind of felt like you were mentioning that you could use M&A to maybe help manage the
input cost but where else do you see maybe an option or a possibility for First Solar?
Alexander Bradley (Executives)
Look, when we talk about uses of cash, M&A is something that's been on the list for us for a long time.
Generally, we focus more on the working capital reserve piece and then growing capacity and
replicating technology. That's where the company has been, if you look over the last decade or so. We've
also put more money into R&D. And I think when you think about M&A, the obvious area for us to
expand into would be, do we spend more on technology and technology adjacent things? Which could
either be companies, it could be buying teams, it could be buying intellectual property. Anything that
could accelerate the technology transition we see going forward as we invest a lot into potential
perovskite development.
So I think there's options there. We're also taking a look at things that are adjacent to technology, but
we want to do it with a disciplined focus around where do we see opportunities where we have a skill set
that we can bring. So something where we look at our strengths in high-volume thin film
manufacturing, a very high throughput efficiency. How can we leverage that set of skills and take it into
an adjacent product, but also look at the overall market environment we'll be playing in. We compete in
a challenging industry where the vast majority of our competitors are Chinese and tend to play by a
different set of rules.
So as we think about how we could move into adjacent areas across M&A, want to evaluate what does
the competitive landscape look like? What does the market that we'll be accessing look like? What does
the policy environment look like? So we are starting to look through that. Clearly, given our position in
the industry, a lot of stuff comes across our desk and has done over the last 10 years or so. We haven't
done a lot on the M&A side. So we are more willing to do that. We're more open to it, but we want to
make sure we do it with a disciplined focus.
Operator (Operator)
We have reached the end of the Q&A session. This concludes today's call. Thank you for attending. You
may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FSLR_Q1_2026_Earnings_Call_20260430.md
- 2026-04-30｜Alexander Bradley (CFO)｜guidance：CFO says full-year 2026 guidance is unchanged after Q1 results.（原話："Our full year 2026 guidance remains unchanged."）
- 2026-04-30｜Alexander Bradley (CFO)｜guidance：CFO gives Q2 volume guidance of 3.4-4 GW and adjusted EBITDA of $400-500M.（原話："we expect volumes sold between 3.4 and 4 gigawatts"）
- 2026-04-30｜Alexander Bradley (CFO)｜margin：CFO states Q1 gross margin was 47%, up ~6pp YoY on 45X tax benefit volume and lower freight costs.（原話："Our gross margin in the first quarter was 47%"）
- 2026-04-30｜Alexander Bradley (CFO)｜margin：CFO reiterates Q2 gross margin guide is flat versus Q1, implying stronger second half.（原話："we're guiding to the same guide that we had in Q1"）
- 2026-04-30｜Alexander Bradley (CFO)｜risk：CFO clarifies the guide assumes no tariff replacement is modeled for finished goods after Section 122 expires.（原話："we're not modeling tariffs beyond that for finished goods"）
- 2026-04-30｜Mark Widmar (CEO)｜risk：CEO says the Section 337 IP investigation is expected to reach an initial determination in about 11 months.（原話："an initial determination within approximately 11 months"）
- 2026-04-30｜Mark Widmar (CEO)｜competition：CEO says headwinds against crystalline silicon competitors (trade remedy, FEOC, IP litigation) continue to build.（原話："headwinds for crystalline silicon continue to build"）
- 2026-04-30｜Mark Widmar (CEO)｜product：CEO describes CuRe's expected lifetime energy yield advantage over crystalline-silicon TOPCon.（原話："CuRe anticipated to deliver up to 8% more lifetime"）
- 2026-04-30｜Mark Widmar (CEO)｜product：CEO says successful CuRe replication across the fleet could unlock up to $0.6B of additional backlog revenue from technology adjusters, mostly in 2027-2028.（原話："up to $0.6 billion of additional revenue from technology"）
- 2026-04-30｜Mark Widmar (CEO)｜commitment：CEO reiterates the company remains well positioned to deliver on its 2026 commitments.（原話："we remain well positioned to deliver on our 2026 commitments"）
- 2026-04-30｜Alexander Bradley (CFO)｜capital_allocation：CFO says quarter-end net cash of $2B sits at the high end of the targeted resilient net cash range.（原話："at the high end of our targeted resilient net cash range"）
- 2026-04-30｜Mark Widmar (CEO)｜customer：CEO says customers are active in M&A/development-acquisition deals, with one option volume tied to a customer's pending acquisition.（原話："We're seeing a lot of M&A activity."）
- 2026-04-30｜Mark Widmar (CEO)｜risk：CEO frames the upcoming CuRe launch in India as the key enabler to manage potential ALMM efficiency-threshold revisions.（原話："the key enabler to make sure we manage through any"）

### FSLR_Shareholder_Analyst_Call_First_Solar_Inc_20260513.md
- 2026-05-13｜Mark Widmar｜commitment：CEO 確認 CuRe 技術已在 Perrysburg 完成導入，首條 Series 6 產線爬坡符合預期（原話："the CuRe launch is complete in Perrysburg"）
- 2026-05-13｜Mark Widmar｜guidance：CuRe 技術調整可望為 backlog 帶來最高 6 億美元額外營收，主要落在 2027-2028 年（原話："$0.6 billion of additional revenue from technology adjusters"）
- 2026-05-13｜Mark Widmar｜customer：CEO 重申技術策略前提：客戶買的是全生命週期發電量，不是單純名牌效率（原話："buy lifetime energy, not just nameplate efficiency"）
- 2026-05-13｜Mark Widmar｜product：Perovskite 技術可靠度已達可比業界最佳 R&D 成果的水準（原話："reliability results that we believe are comparable to"）
- 2026-05-13｜Alexander Bradley｜margin：CFO 確認 2026 年第一季毛利率明顯擴張，帶動單季每股盈餘創紀錄（原話："margin expansion and record Q1 diluted EPS of $3.22"）
- 2026-05-13｜Alexander Bradley｜commitment：CFO 確認南卡羅來納州加工產線進度符合 2026 年第四季排程（原話："Carolina finishing line remains on schedule for Q4 2026"）
- 2026-05-13｜Alexander Bradley｜commitment：CFO 確認路易斯安那州廠已完成試車並啟動商業化生產（原話："initiated commercial production at our Louisiana facility"）

### 問答異常語氣（迴避／改口／保留）
- FSLR_Q1_2026_Earnings_Call_20260430.md｜問：Given the Section 232 decision has already slipped from year-end 2025 into Q2, what is the confidence level it lands in May or June?｜答法：Widmar did not give a firm confidence level; said 'there's still a lot of moving pieces' and that the slide reflects 'the best information we have,' without addressing why prior timelines had already slipped.

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

## ⑥ 條件附卡（archetype_hint='循環/商品' 命中）：judge_addendum_cyclical.md

<!-- source: .claude/skills/stock-analyst/references/cyclical-lens.md sha256:b13d95972edd47ea git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- load-when: archetype.primary 或 secondary ∈ {循環/商品，EMS/ODM}（QC-43 判定，含 capex 建設循環／需求量循環子型） -->

# QC-42 循環交易讀數（附錄 B）附卡

循環股的錢在 Game 2（投降買、延伸賣）。本附卡是平行、明標投機的交易讀數，不改長抱裁決。[§WHY]

## 一、觸發與子型判定
無循環 sleeve（純成長 mis-route）→ 整段省略。[§①]
商品子型（下列≥2命中→用商品 through-cycle 錶）：近5-7年≥1個GAAP虧損年｜peak-to-trough毛利率擺動>~20pp｜營收主由商品ASP驅動(price-taker)｜產業∈{記憶體/DRAM/NAND、礦業/材料/稀土、化工、航運、鋼鐵、太陽能、油氣E&P、部分晶圓/設備}｜capex/rev結構性>15%且ROIC高度擺動。未達≥2仍判循環→依驅動來源選capex建設循環錶或需求量循環錶。[§商品子型]

## 二、循環位置錶族（三選一，錨自身 through-cycle 區間非動能；位置落 深谷投降/早循環/中循環/晚循環/過熱頂部，多數決+sourced 裁決）
商品 through-cycle（MU 型，6 訊號）：P/B vs 自身區間(近1x/下緣=買，>中位2x/上緣=賣)｜量 vs 價(量增領先=買，ASP-only量平降=賣)｜GM vs自身區間(近谷/負=買，近峰=賣)｜供給紀律(減產=買，新產能洪水=賣)｜庫存(去化乾淨=買，通路+公司堆積=賣)｜情緒/部位(投降PT>價=買，狂熱PT<價=賣)。[§B.1商品]
capex 建設循環（ORCL 型，6 訊號）：capex/折舊比(低/正常化=買，遠高於1=賣)｜產能利用率爬坡(低基期回升=買，滿載見頂=賣)｜RPO(backlog)vs capex覆蓋(backlog領先=買，capex超前需求=賣)｜交易對手信用(客戶分散信用強=買，集中燒錢客戶=賣)｜情緒/部位(同上)｜量vs價(量增領先=買，ASP承壓量見頂=賣)。[§B.1capex]
需求量循環（EMS/ODM，JBL 型，5 訊號）：book-to-bill/需求量拐點(>1拐點向上=買，<1量見頂=賣)｜客戶庫存去化(去化乾淨=買，通路+客戶堆積=賣)｜倍數vs自身歷史re-rate均值回歸(近下緣=買，>5Y中位×1.5/貼峰=賣)｜終端·hyperscaler capex週期位置(早週期=買，晚週期見頂=賣)｜情緒/部位(同上)。[§B.1需求量]

## 三、交易姿態 + 反動能硬閘（跨子型通用，逐條檢查，觸發即 override 向保守）
位置→姿態：深谷投降→積極分批建立｜早→分批建立｜中→持有不加｜晚→分批了結｜頂→清光不碰。[§B.2]
閘1 位置=晚/頂→姿態不得為任何「建立」。閘2 成長=ASP-only+量持平/降→最多「持有」。閘3 P/B>自身中位2x→禁新建立。閘4 訊號矛盾→標「位置不明，觀望」不硬給姿態。閘5 TTM/Fwd本益比或EV倍數>自身歷史高區(>5Y中位×1.5、或貼/破歷史峰)→禁新建立。[§閘1-5]

## 四、落欄與 §13 row 8b 接線
`cycle_position`(深谷投降｜早循環｜中循環｜晚循環｜過熱頂部)＋`cycle_verdict`(右側可追蹤｜等回踩｜頂部觀望｜未觸發)；非循環 archetype 不填，整欄省略。[§落欄]
接 §13 row 8b：位置∈{深谷投降，早循環}+五閘全過+moat底線+獨立critic冷讀通過→落「進場・條件式(循環衛星)」(倉位上限3%)；任一不成立→只落研究提名，§13維持觀望。驗證失敗不得升級，只能降回觀望。`trade_stance`僅進HTML不入dd-meta。[§row8b]

## 五、雙制度與兩軌背離
有 secular sleeve + commodity sleeve → 循環鏡頭只套 commodity sleeve，secular sleeve 一句話另計(不隨循環賣)。[§⑤]
投資軌(§13長抱視角) vs 交易軌(本鏡頭位置)：底部背離(長抱視角迴避 + 循環位置深谷投降/早循環)是本鏡頭獨門訊號；頂部多收斂(皆遠離)。[§B.3]


---

## ⑦ 前份判斷摘要（緊湊 JSON，≤ 5000 bytes）

```json
{"date":"20260608","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Section 45X 製造抵免在最終法案中存續（至 2031），是 FSLR 盈餘地基","columns":{"2Y 驗證點":"2026 最終法案保留 45X 製造端","5Y 驗證點":"2027-2030 45X 按原階梯（2030 起 75%）執行，無提前歸零","10Y 驗證點":"2031 後 FSLR 有「ex-45X 自立」獲利能力","具體數字門檻":"45X ≈ $0.17/W；FY 美製出貨 ≥ 14 GW → 抵免 ≥ $2.4B 級","信息來源":"參院 6/5 草案、Q1'26 8-K、公司法說","漂移觸發":"法案文本修改 45X → 立即削弱（binary，見 5.F）"}},{"id":"H2","text":"47.9 GW backlog 如期兌現，FY26-27 量價達標","columns":{"2Y 驗證點":"FY26 出貨 17–18.2 GW、ASP 維持","5Y 驗證點":"backlog 交付至 2030 無重大違約/重議","10Y 驗證點":"新一輪簽約補足耗盡的 backlog","具體數字門檻":"FY26 net sales $4.9-5.2B、adj EBITDA $2.6-2.8B；美國 ASP ≥ $0.30/W","信息來源":"FY26 guidance（Q4'25 8-K）、Q1'26 backlog 揭露","漂移觸發":"連 2 季 TTM 出貨/ASP 偏離 ≥ 5% → 削弱"}},{"id":"H3","text":"市場最終給予 backlog + 立法保護 應有的倍數修復（脫離通縮 c-Si 估值錨）","columns":{"2Y 驗證點":"Fwd PE 從 12x 修復向 16-18x","5Y 驗證點":"政策明朗後 de-risk，倍數穩定於合理區","10Y 驗證點":"不再被當「補貼股」殺估值","具體數字門檻":"FY27 PE 12x → 16x（中期目標 $370）","信息來源":"§13 歷史分位、分析師目標價分布","漂移觸發":"EPS 共識續下修 &gt;10% 或政策利空 → 倍數續壓 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"45X 製造抵免被縮減/加速退場（政策反轉）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季，立法週期）","監測指標":"最終調節法案 45X 條款文本","警戒閾值":"製造抵免被砍或退場提前至 2028-29 → 連結 5.F binary"}},{"id":"R2","text":"EPS 共識持續下修 + 盈餘可預測性惡化 → 倍數壓縮","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"FY26/27 EPS 共識修正方向","警戒閾值":"連 2 季再下修，累計 &gt;10% → 減倉"}},{"id":"R3","text":"全球模組通縮 + backlog 耗盡後 re-pricing（裸模組真相）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"美國 bookings ASP + 淨 backlog 變化","警戒閾值":"連 2 季美國 ASP &lt; $0.30/W 且 backlog 淨流出（需 ≥50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":279.01,"archetype":null,"cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20260929/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
