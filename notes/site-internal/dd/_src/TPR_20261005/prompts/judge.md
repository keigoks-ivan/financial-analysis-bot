你是 stock-analyst **v20 判斷 agent**，標的 TPR（20261005）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"TPR","date":"2026-10-05","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261005/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261005/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP）","value":1876.6,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"}},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":19.3,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"}},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":23.6,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"}},{"id":"f_kpi5","label":"管理層指引","value":null,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":null,"basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"},"needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-08-13","period":"2026-08-13","unit":"date","basis":"距今 37 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-08-13"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tpr_gross_margin_pct","label":"TPR 毛利率","value":77.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpr_operating_margin_pct","label":"TPR 營業利益率","value":23.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_tpr_fcf_margin_pct","label":"TPR FCF 利潤率","value":22.64,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mc_gross_margin_pct","label":"MC 毛利率","value":34.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MC.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mc_operating_margin_pct","label":"MC 營業利益率","value":18.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MC.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_mc_fcf_margin_pct","label":"MC FCF 利潤率","value":27.54,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MC.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"id":"f_peer_cfr_fcf_margin_pct","label":"CFR FCF 利潤率","value":23.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CFR.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3","label":"自由現金流","value":469.0,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm"}},{"id":"f_kpi4_sbc","label":"SBC 占營業利益","value":7.0,"period":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）","citation":"公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm（Schedule 8）"}}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":118.12,"period":"2026-10-02（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-02（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":-15.79,"period":"2026-10-02（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-02（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":46.91,"period":"2026-10-02（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-02（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（7.97 → 7.97）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（8.9 → 8.9）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.0,"period":"2026-09-26","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（10.21 → 10.21）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":7.97,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":8.9,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":10.21,"period":"2026-09-26","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":14.35,"period":"2026-06-23 → 2026-09-26","unit":"%","basis":"FY1 共識 EPS 6.97 → 7.97（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-26","citation":"DD_universe_EPS_estimates_20260926.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":16.25,"period":"2026-10-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝6.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":6.2,"period":"2026-10-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-02（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":2.93,"period":"2026-10-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝65.2","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":65.2,"period":"2026-10-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-02（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":3.28,"period":"2026-10-02（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝64.1","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-02（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":64.1,"period":"2026-10-02（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-02（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":14.82,"period":"2026-09-26","unit":"x","basis":"分母＝FY1 EPS 7.97，分子＝快照價 118.12","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-26"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":1.408,"period":"2026-10-05","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-05"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-10-05","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 117.31 / W52 132.32 / W104 105.36 / W250 64.41 / W250 13週斜率 2.01%"},{"id":"f_ma_w52","label":"52 週均線","value":132.32,"period":"2026-10-05","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":105.36,"period":"2026-10-05","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":64.41,"period":"2026-10-05","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.01,"period":"2026-10-05","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-05","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Coach 財年 Q3 FY2026 固定匯率營收 +29%；北美 +27%、大中華 +58%、歐洲 +27%，報導稱優於產業趨勢、持續取得份額；該季新客約 200 萬，Gen Z 加速。","source":"ouispeakfashion.com — Coach Momentum Accelerates Globally: Tapestry, Inc. Delivers Double-Digit Growth in Q3 FY2026","url":"https://ouispeakfashion.com/2026-05-07-tapestry-inc/","excerpt":null,"as_of":"2026-05-07","retrieved_at":"20261005","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"財經內容稿稱 2025–2026 年 Tapestry 持續從歐洲對手（因大幅漲價疏遠嚮往型客群）手中取得份額；Ralph Lauren 同為雙位數成長，Capri 與 LVMH 時尚皮件表現較分歧。屬二手聚合稿，無一手份額數據。","source":"FinancialContent — The Reinvention of American Luxury: A Deep Dive into Tapestry, Inc. (TPR)","url":"https://markets.financialcontent.com/stocks/article/finterra-2026-4-3-the-reinvention-of-american-luxury-a-deep-dive-into-tapestry-inc-tpr","excerpt":null,"as_of":"2026-04-03","retrieved_at":"20261005","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Michael Kors（Capri）為 Coach 在輕奢手袋的主要對手；Polene、Jacquemus 等小眾品牌透過社群與稀缺性吸引年輕客群，轉售平台（The RealReal、Vestiaire）形成間接競爭。來源為彙整型文章，非一手數據。","source":"retailboss.co / Morningstar 搜尋結果彙整（Coach Is Now 89% Of Tapestry…）","url":"https://retailboss.co/coach-is-now-89-of-tapestry-inside-the-two-brand-portfolio-that-is-quietly-reshaping-accessible-luxury/","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261005","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"MediaPost 報導 Coach 近 10 億美元行銷飛輪帶動 31% 成長（標題）。","source":"MediaPost — Near-$1B Marketing Flywheel Drives Coach's 31% Gain 05/27/2026","url":"https://www.mediapost.com/publications/article/415316/near-1b-marketing-flywheel-drives-coachs-31-gai.html?edition=142731","excerpt":null,"as_of":"2026-05-27","retrieved_at":"20261005","affects":["moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"0","claim":"FY2026 10-K（截至 2026-06-27）：沒有任何單一客戶占各分部淨銷售額逾 10%；批發約占總淨銷售額 12%，客戶為百貨、專賣店與第三方數位夥伴。","source":"SEC Form 10-K FY2026, Tapestry, Inc.","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":null,"as_of":"2026-06-27","retrieved_at":"20261005","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"FY2026 10-K（截至 2026-06-27）：沒有任何單一客戶占各部門淨銷售額超過 10%；批發約占總淨銷售額 12%。","source":"Tapestry Form 10-K FY2026（搜尋摘要轉述）","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":null,"as_of":"2026-06-27","retrieved_at":"20261005","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Tapestry 對百貨與批發客戶評估信用並控管授信條件以降低呆帳；批發占 FY2024 淨營收約 18%（第三方彙整，非 10-K 原文）。","source":"growthsharematrix.com Tapestry SWOT Analysis／搜尋摘要","url":"https://growthsharematrix.com/products/tapestry-swot-analysis","excerpt":null,"as_of":"2024-12-31","retrieved_at":"20261005","affects":["thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Tapestry FY2026 Q4 call: CEO says FY26 results show the strategy's power and growth from a higher base within the long-term algorithm; CFO says FY27 guidance does not require holding the same growth level for the rest of the year.","source":"Yahoo Finance, Tapestry Inc (TPR) Q4 2026 Earnings: Key Takeaways","url":"https://finance.yahoo.com/markets/stocks/articles/tapestry-inc-tpr-q4-2026-231010449.html","excerpt":"fiscal 2026 results demonstrated the power of the strategy and that the company is growing from a higher base while maintaining its long-term algorithm.","as_of":"2026-08-14","retrieved_at":"20261005","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Coach handbag AUR rose mid-teens in Q4 and for FY26, with units up low double digits; Tabby expected to show no slowdown; platforms expanding in the $200-$500 price range.","source":"Yahoo Finance, Tapestry Inc (TPR) Q4 2026 Earnings: Key Takeaways","url":"https://finance.yahoo.com/markets/stocks/articles/tapestry-inc-tpr-q4-2026-231010449.html","excerpt":"Increased at a mid-teens rate in Q4; for the year, rose mid-teens with units up low double digits.","as_of":"2026-08-14","retrieved_at":"20261005","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"FY2027 guidance: revenue $8.4-8.5B, operating margin up about 50bp to nearly 24%, EPS $7.80-7.90.","source":"Yahoo Finance, Tapestry Inc (TPR) Q4 2026 Earnings: Key Takeaways","url":"https://finance.yahoo.com/markets/stocks/articles/tapestry-inc-tpr-q4-2026-231010449.html","excerpt":"$8.4 billion to $8.5 billion","as_of":"2026-08-14","retrieved_at":"20261005","affects":["valuation","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Search summary of industry reports: global luxury market expected to grow 1-3% a year 2024-2027; 3-5% in 2026; US 4-6% 2025-2027. Specific report dates not confirmed; aggregated from multiple secondary sources.","source":"WebSearch results: 'luxury demand outlook 2027 2028 consensus' (McKinsey State of Luxury, Fashion Dive and others)","url":"https://www.mckinsey.com/industries/retail/our-insights/state-of-luxury","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261005","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"FTC 於 2024-04-23 起訴阻止 Tapestry 收購 Capri（約 85 億美元），法院其後核准初步禁制令，交易被擋下；屬過往併購反壟斷案，非對 TPR 現有業務的調查。","source":"WUSTL Law Review: Is Dealmaking Going Out of Fashion? The Impact of the FTC-Tapestry, Inc. Litigation on M&A Activity in the Fashion Industry","url":"https://wustllawreview.org/2026/02/25/is-dealmaking-going-out-of-fashion-the-impact-of-the-ftc-tapestry-inc-litigation-on-ma-activity-in-the-fashion-industry/","excerpt":"following an investigation and 5-0 approval vote by FTC commissioners, the FTC sued on April 23, 2024.","as_of":"2026-02-25","retrieved_at":"20261005","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"法學評論稱 FTC 勝訴形成先例，可能限制「輕奢」層級未來的併購整合。","source":"WUSTL Law Review (2026-02-25)","url":"https://wustllawreview.org/2026/02/25/is-dealmaking-going-out-of-fashion-the-impact-of-the-ftc-tapestry-inc-litigation-on-ma-activity-in-the-fashion-industry/","excerpt":"The FTC's successful challenge of the Capri merger has set a precedent that will likely limit future consolidation within the \"accessible luxury\" tier.","as_of":"2026-02-25","retrieved_at":"20261005","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"Tapestry 預估美國關稅將使 FY2026 成本增加約 1.6 億美元，預期 2028 年前完全抵銷；FY2026 EPS 指引 5.30–5.45 美元，其中約 0.60 美元缺口來自關稅（含取消 de minimis 免稅）。","source":"Mexico Business News: Coach Owner Warns US Tariffs May Cost US$160 Million in FY2026（發布日以 2025-08-14 財報日近似，頁面日期未讀取）","url":"https://mexicobusiness.news/ecommerce/news/coach-owner-warns-us-tariffs-may-cost-us160-million-fy2026","excerpt":"Tapestry, the parent company of Coach and Kate Spade, warned that US tariffs could cost the company about US$160 million in fiscal 2026, with full offset expected by 2028.","as_of":"2025-08-14","retrieved_at":"20261005","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"手袋多在越南、柬埔寨、菲律賓、印度生產，搜尋結果未顯示中國為主要關稅暴露來源；另已累計逾 2 億美元 IEEPA 與對等關稅成本。","source":"同上搜尋彙整（Mexico Business News／Inside Retail Asia，2025-08）","url":"https://mexicobusiness.news/ecommerce/news/coach-owner-warns-us-tariffs-may-cost-us160-million-fy2026","excerpt":"Most of Tapestry's handbags are manufactured in Vietnam, Cambodia, the Philippines, and India.","as_of":"2025-08-14","retrieved_at":"20261005","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"搜尋摘要稱：越南、柬埔寨、菲律賓合計佔 Tapestry 約 70% 生產；Coach 與 Kate Spade 多數手袋在越南、柬埔寨、菲律賓、印度製造（東南亞集中）。","source":"Inside Retail Asia - Can Coach carry the weight as tariffs bear down on Tapestry?","url":"https://insideretail.asia/2025/08/18/can-coach-carry-the-weight-as-tariffs-bear-down-on-tapestry/","excerpt":null,"as_of":"2025-08-18","retrieved_at":"20261005","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"搜尋摘要稱：中國僅佔 Tapestry 約 10% 採購；三大生產國面臨 10% 關稅，關稅衝擊 FY2026 約 1.6 億美元。","source":"Inside Retail Asia / Mexico Business News (Coach Owner Tapestry Sees US$160 Million Profit Hit from Tariffs)","url":"https://mexicobusiness.news/ecommerce/news/coach-owner-tapestry-sees-us160-million-profit-hit-tariffs","excerpt":null,"as_of":"2025-08-18","retrieved_at":"20261005","affects":["valuation","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"搜尋摘要稱：Tapestry 在 FY2026 10-K 列美中關係不確定性與貿易協定參與變動為風險因子；國際業務約佔淨銷售 40%。10-K 全文未讀，as_of 取會計年度結束日。","source":"SEC Form 10-K FY2026 (period ending 2026-06-27)","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":null,"as_of":"2026-06-27","retrieved_at":"20261005","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"搜尋摘要稱：Greater China 為 FY26 Q3 最強國際成長動能（固定匯率 +55%）；中國同時是銷售市場，與生產端分離。","source":"Yahoo Finance - Tapestry's International Growth Accelerates on China & Europe Gains","url":"https://finance.yahoo.com/markets/stocks/articles/tapestrys-international-growth-accelerates-china-124200007.html","excerpt":null,"as_of":"2026-05-01","retrieved_at":"20261005","affects":["thesis.H","thesis.R"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"FY2026 全年營收 $8.00B（+14%）；Coach $6.91B（+24%）；Kate Spade $1.07B（-10%）。","source":"Ouispeakfashion: Tapestry Reports 14% Revenue Growth in Fiscal 2026 as Coach Sales Rise 24%（搜尋摘要）","url":"https://ouispeakfashion.com/tapestry-fiscal-2026-earnings/","excerpt":"Tapestry's fiscal 2026 revenue increased 14% to $8.00 billion, led by 24% growth at Coach, which generated $6.91 billion in full-year revenue. In contrast, Kate Spade New York reported annual revenue of $1.07 billion, down 10%.","as_of":"2026-08-13","retrieved_at":"20261005","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Kate Spade 前九個月淨銷售 -11.1% 至 $839.8M；Q4 -7% 至 $235.1M；管理層稱精簡動作對營收的拖累大於預期。","source":"SEC 10-Q (tpr-20260328) 與 WWD: Tapestry Q4 earnings（搜尋摘要）","url":"https://wwd.com/business-news/financial/tapestry-q4-earnings-coach-kate-spade-1239117671/","excerpt":"Kate Spade net sales decreased 11.1% or $104.7 million to $839.8 million in the first nine months of fiscal 2026. The decline continued through the full year, with Kate Spade slipping 7 percent to $235.1 million in the fourth quarter.","as_of":"2026-08-13","retrieved_at":"20261005","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Kate Spade 任命 Jonathan Saunders 為創意總監，作為轉型計畫一環。","source":"WWD / 搜尋摘要","url":"https://wwd.com/business-news/financial/tapestry-q4-earnings-coach-kate-spade-1239117671/","excerpt":"The brand named Scottish fashion designer Jonathan Saunders as its creative director last month, as part of a turnaround plan that includes improvements in product design and visual identity.","as_of":"2026-08-13","retrieved_at":"20261005","affects":["thesis.H","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"Coach 在 18–27 歲族群品牌偏好排名第一，FY2026 新增近九百萬客戶，Gen Z 為主要來源。","source":"Fortune: How Coach became Gen Z's favorite affordable luxury handbag brand（搜尋摘要）","url":"https://fortune.com/2026/05/19/coach-handbags-comeback-millennials-gen-z/","excerpt":"Coach now ranks #1 in brand preference among 18-27 year olds, completely overtaking similarly priced competitors like Michael Kors and Kate Spade. The brand attracted more than two million new customers during the quarter and nearly nine million during fiscal 2026, with Gen Z leading customer acquisition.","as_of":"2026-05-19","retrieved_at":"20261005","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Coach Q4 手袋平均單價（AUR）成長中十位數百分比，銷量大致持平；做法是減少促銷日而非加大折扣。","source":"Retail Insider: Coach Expands Store Investment as Gen Z Drives Global Growth（搜尋摘要）","url":"https://retail-insider.com/retail-insider/2026/08/coach-expands-store-investment-as-gen-z-drives-global-growth/","excerpt":"Handbag average unit retail increased at a mid-teens rate during the fourth quarter while unit volumes were roughly in line with the previous year, reflecting a decision to reduce promotional days rather than pursue additional discounting.","as_of":"2026-08-31","retrieved_at":"20261005","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Tapestry FY2026 10-K 風險因素稱：消費者愈來愈常用 AI 購物助理來探索商品、比價、下單，可能改變商務並影響公司吸引並留住數位平台客戶的能力（as_of 為 FY2026 財年結束日，實際申報日未確認）","source":"Tapestry Inc. Form 10-K FY2026 (SEC EDGAR)","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":null,"as_of":"2026-06-27","retrieved_at":"20261005","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"二手奢侈品市場估計 2026 年約 416 億美元（2025 年約 379 億），成長速度約為一手市場三倍；Gen Z 衣櫃 45% 的手袋為二手（來源為聚合文章，數字未回溯至原始報告）","source":"Luxury Resale Market: 2026 Gen Z $41B Boom Disrupts Status (editorialge.com)；Forbes Resale Market 2026 (2025-12-16)","url":"https://editorialge.com/luxury-resale-market-2026/","excerpt":null,"as_of":"2025-12-16","retrieved_at":"20261005","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"+","claim":"Tapestry 與 Adobe Firefly 合作以自有素材訓練客製生成式 AI 模型，用於手袋設計流程；FY2026 取得首件 AI 專利","source":"Adobe Business Blog: Coach reimagines handbag design process with Adobe Firefly；搜尋摘要","url":"https://business.adobe.com/blog/coach-reimagines-handbag-design-process-with-adobe-firefly-generative-ai","excerpt":null,"as_of":"2026-06-27","retrieved_at":"20261005","affects":["moat_trend"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"FY2026 DTC約佔總淨銷售87%；DTC營收Q4成長11%、全年成長16%，數位營收全年高個位數後段（high-teens）成長、門店營收中高個位數（mid-teens）成長。","source":"Tapestry Form 10-K FY2026（搜尋摘要）","url":"https://www.sec.gov/Archives/edgar/data/0001116132/000111613226000018/tpr-20260627.htm","excerpt":"DTC revenues were approximately 87% of total net sales in fiscal 2026","as_of":"2026-06-27","retrieved_at":"20261005","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"批發占比FY2025約13%；摘要稱計畫持續關閉不賺錢門店並退出批發合作，以維持價格完整性（此段為搜尋摘要彙整，未逐項對到原文，as_of為FY2026 10-K期末日）。","source":"Tapestry Form ARS FY2025／搜尋摘要","url":"https://www.sec.gov/Archives/edgar/data/1116132/000114036125036305/ny20053837x3_ars.pdf","excerpt":"Wholesale represented approximately 13% of our total net sales for fiscal 2025","as_of":"2025-08-01","retrieved_at":"20261005","affects":["moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"FY2027 EPS 指引 7.80–7.90 美元，中點略高於共識 7.84；FY27 營收指引 84–85 億美元，中點 84.5 億低於分析師預期 84.7 億；Q1 FY27 EPS 指引約 1.55 對共識 1.48。","source":"MarketBeat／StockStory 等，Tapestry Updates FY 2027 Earnings Guidance","url":"https://www.marketbeat.com/instant-alerts/tapestry-nysetpr-updates-fy-2027-earnings-guidance-2026-08-13/","excerpt":"For fiscal 2027, Tapestry issued EPS guidance of $7.80 to $7.90, with a midpoint of $7.85 slightly above the consensus of $7.84. For the first quarter of fiscal 2027, Tapestry projects EPS of approximately $1.55, exceeding the consensus of $1.48.","as_of":"2026-08-13","retrieved_at":"20261005","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"-","claim":"營收指引低於共識是財報後股價大跌主因，2026-08-13 盤中跌逾 14%。","source":"MarketBeat／StockStory 等，Tapestry Updates FY 2027 Earnings Guidance","url":"https://www.marketbeat.com/instant-alerts/tapestry-nysetpr-updates-fy-2027-earnings-guidance-2026-08-13/","excerpt":"The company's revenue outlook of $8.4 billion to $8.5 billion, with a midpoint of $8.45 billion, fell short of the $8.47 billion analyst estimate. This revenue shortfall was the primary driver of the negative market reaction, with Tapestry shares falling sharply on August 13, 2026, declining more than 14% intraday.","as_of":"2026-08-13","retrieved_at":"20261005","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"分析師目標價共識均價約 175.12–175.13 美元，高 232、低 138；21 家覆蓋，共識評等 Moderate Buy。","source":"MarketBeat，Tapestry, Inc. Stock Has Average Price Target of $175.12","url":"https://www.marketbeat.com/instant-alerts/consensus-tapestry-inc-nyse-tpr-stock-has-average-price-target-of-17512-2026-09-25/","excerpt":"The average price target for Tapestry is $175.13, with a high of $232.00 and low of $138.00","as_of":"2026-09-25","retrieved_at":"20261005","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"財報後目標價分歧：UBS 232（自230）、Barclays 185（自182）、Bernstein 185（自180）上調；Wells Fargo 160（自165）、Morgan Stanley 159（自164）下調。Daiwa 8/17 由 Hold 升 Strong-Buy。","source":"MarketBeat TPR forecast／搜尋彙整","url":"https://www.marketbeat.com/stocks/NYSE/TPR/forecast/","excerpt":"Morgan Stanley lowering its price target from $164.00 to $159.00 on 8/14/2026, while Sanford C. Bernstein raised its target from $180.00 to $185.00.","as_of":"2026-08-17","retrieved_at":"20261005","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"FY2026 全年指引在年內連續上調：Q3 時營收約 79.5 億、非 GAAP EPS 約 6.95（前次 6.40–6.45）。","source":"Chartmill，Tapestry Soars After Blowout Q3 Earnings Beat and Raised FY2026 Guidance","url":"https://www.chartmill.com/news/TPR/Chartmill-47633-Tapestry-NYSETPR-Soars-After-Blowout-Q3-Earnings-Beat-and-Raised-FY2026-Guidance","excerpt":"The updated outlook includes revenue of approximately $7.95 billion and non-GAAP EPS in the area of $6.95, representing growth of over 35% year-over-year and a significant increase from prior guidance of $6.40 to $6.45.","as_of":"2026-05-01","retrieved_at":"20261005","affects":["thesis.H","valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"Capri 併購案於 2024-11-13 簽終止協議（FTC 取得初步禁制令後）；Tapestry 補償 Capri 費用 4,510 萬美元。距今超過 12 個月，列為背景。","source":"Tapestry 10-Q / 官方新聞稿 'Tapestry, Inc. Announces Termination of Merger Agreement With Capri Holdings Limited'","url":"https://tapestry.gcs-web.com/news-releases/news-release-details/tapestry-inc-announces-termination-merger-agreement-capri","excerpt":"on November 13, 2024, the parties entered into a Termination Agreement and agreed to terminate the Merger Agreement effective immediately. Tapestry agreed to reimburse Capri for its expenses in an amount equal to $45.1 million in cash on November 14, 2024.","as_of":"2024-11-13","retrieved_at":"20261005","affects":["thesis.R","valuation"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"Capri 併購案 2024-11-13 終止（背景，超過 12 個月）；搜尋未見近 12 個月新併購。","source":"Tapestry 官方新聞稿 Termination of Merger Agreement With Capri","url":"https://tapestry.gcs-web.com/news-releases/news-release-details/tapestry-inc-announces-termination-merger-agreement-capri","excerpt":"on November 13, 2024, the parties entered into a Termination Agreement and agreed to terminate the Merger Agreement effective immediately.","as_of":"2024-11-13","retrieved_at":"20261005","affects":["thesis.R"],"status":"ok"},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"同業對照缺度量：rd_intensity_pct","question":"q2_moat","why":"evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。","tried":["evidence.numbers.peer_financials"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"}],"rows":[{"name":"TPR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":77.82,"operating_margin_pct":23.92,"fcf_margin_pct":22.64,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TPR","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true,"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"RMS","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.RMS"},"note":"quarterly_income_stmt 無資料"},{"name":"MC","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":34.36,"operating_margin_pct":18.4,"fcf_margin_pct":27.54,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MC","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"CFR","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":23.55,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.CFR","as_of":"TTM ending 2026-06-30（4季加總）"},"note":"Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"},{"name":"KER","period":null,"basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":null,"operating_margin_pct":null,"fcf_margin_pct":null,"rd_intensity_pct":null},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.KER"},"note":"quarterly_income_stmt 無資料"}],"subject":"TPR"},"financial_history":{"ticker":"TPR","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2023-06-30","revenue":6660900000.0,"revenue_yoy_pct":null,"gross_margin_pct":70.78,"operating_margin_pct":17.6,"net_income":936000000.0,"diluted_eps":3.88,"free_cash_flow":791000000.0,"fcf_margin_pct":11.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2023-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-06-30","revenue":6671200000.0,"revenue_yoy_pct":0.15,"gross_margin_pct":73.29,"operating_margin_pct":17.09,"net_income":816000000.0,"diluted_eps":3.5,"free_cash_flow":1146700000.0,"fcf_margin_pct":17.19,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2024-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-06-30","revenue":7010700000.0,"revenue_yoy_pct":5.09,"gross_margin_pct":75.44,"operating_margin_pct":18.11,"net_income":183200000.0,"diluted_eps":0.82,"free_cash_flow":1093900000.0,"fcf_margin_pct":15.6,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2025-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2026-06-30","revenue":8004200000.0,"revenue_yoy_pct":14.17,"gross_margin_pct":77.82,"operating_margin_pct":23.92,"net_income":1527700000.0,"diluted_eps":7.27,"free_cash_flow":1812500000.0,"fcf_margin_pct":22.64,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2026-06-30","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TPR/TPR_Q4_2026_Earnings_Call_20260813.md）

# Q4 2026 Earnings Call
2026-08-13

Q4 2026 Earnings Call
Tapestry, Inc. | Earnings Calls | 2026-08-13
Operator (Operator)
Good day, and welcome to this Tapestry conference call. Today's call is being recorded. [Operator
Instructions] At this time, for opening remarks and introductions, I would like to turn the call over to
the Global Head of Investor Relations, Christina Colone.
Christina Colone (Executives)
Good morning. Thank you for joining us. With me today to discuss our fourth quarter and full year
results, our strategies and our outlook are Joanne Crevoiserat, Tapestry's Chief Executive Officer; and
Scott Roe, Tapestry's Chief Financial Officer and Chief Operating Officer.
Before we begin, we must point out that this conference call will involve certain forward-looking
statements within the meaning of the Private Securities Litigation Reform Act. This includes
projections for our business in the current or future quarters or fiscal years. Forward-looking
statements are not guarantees, and our actual results may differ materially from those expressed or
implied in the forward-looking statements. Please refer to our annual report on Form 10-K, the press
release we issued this morning and our other filings with the Securities and Exchange Commission for a
complete list of risks and other important factors that could impact our future results and performance.
Non-GAAP financial measures are included in our comments today and in our presentation slides. For
a full reconciliation to corresponding GAAP financial information, please visit our website,
www.tapestry.com/investors, and then view the earnings release and the presentation posted today.
Now let me outline the speakers and topics for this conference call. Joanne will begin with highlights
for Tapestry and our brands. Scott will continue with our financial results, capital allocation priorities
and our outlook going forward. Following that, we will hold a question-and-answer session where we
will be joined by Todd Kahn, CEO and Brand President of Coach. After Q&A, Joanne will conclude with
brief closing remarks.
I'd now like to turn it over to Joanne Crevoiserat, Tapestry's CEO.
Joanne Crevoiserat (Executives)
Good morning. Thank you, Christina, and welcome, everyone. Fiscal 2026 was a defining year for
Tapestry. We meaningfully exceeded expectations, achieving the 3-year revenue, operating margin and
earnings per share commitments we established at our Investor Day 2 years ahead of plan. We
delivered strong growth and record results while continuing to invest in our brands, our people and the
capabilities that will shape our future. More important than what we accomplished is what we've built.
Through intentional choices, disciplined execution and a deep understanding of the consumer, we have
built a stronger, more focused organization who every day bring our Amplify strategy to life, delivering
creativity, value and relevance at scale, strengthening our connections with consumers. These efforts
continue to compound, extending our competitive advantage while driving durable growth and long-
term shareholder value. In a world where consumer expectations, technology and competitive
dynamics continue to evolve, the combination of our direct consumer relationships, data-driven

decision-making, global scale and agile operating model has become increasingly valuable and
differentiated.
With that, let me touch on some highlights for the year. We achieved revenue of $8 billion, growing 17%
on a pro forma constant currency basis, expanded operating margin by 340 basis points to over 23%
and increased earnings per share by 38% to $7.05. Growth was fueled by customer acquisition as we
welcomed 11 million new customers to our brands, led by Gen Z. Importantly, we accelerated growth in
our core leather goods category with AUR and unit growth. Luxury leather goods remains one of the
most attractive categories within the consumer space because of its enduring demand, compelling
economics and significant runway for growth. In addition, we delivered broad-based double-digit
growth across key regions, gaining share and expanding the market.
Our agile direct-to-consumer-led operating model drove double-digit revenue growth and increasing
profitability across both digital and stores. Further, Tapestry is committed to embracing AI to enhance
the magic of our people and our brands. To that end, we continue to build proprietary technology and
AI capabilities that differentiate how we operate and empower our teams. During the year, we secured
our first AI patent, building on our previously patented data fabric technology. Together, they reflect
our culture of innovation and more than a decade of investment in data, decision intelligence and
enterprise technology. Overall, our fiscal year '26 results demonstrate the power of our approach to
brand building. We continue to win with consumers at the point of market entry, welcoming younger
customers who transact at higher AURs, have stronger retention and influence purchasing behavior
across generations. This reinforces our confidence that our greatest opportunities lie ahead.
Now moving to our results by brand. Coach delivered another strong quarter with constant currency
revenue growth of 14% and increasing profitability. This capped an exceptional year and reinforced the
enduring strength of our iconic 85-year-old brand. Several factors underscore the durability of our
growth. We drove new customer acquisition around the world, welcoming over 2 million new
consumers in the quarter and nearly 9 million for the full year. Growth was led by Gen Z, whose
influence extended across generations. At the same time, existing customers continue to drive strong
sales. Underpinning these results is Coach's consumer-led approach, consistently translating deep
consumer insights into action to build lasting emotional connections with the brand.
Our core leather goods assortment continued to lead in Q4, with handbag AUR increasing at a mid-
teens rate and unit volumes roughly in line with the prior year, both consistent with expectations and
our deliberate strategy to prioritize brand health and reduce promotions. For the year, handbag AUR
rose mid-teens and units increased low double digits, demonstrating the multifaceted nature of our
growth. Looking ahead, we continue to see opportunity to grow both AUR and units while staying true
to the values and the value proposition that define Coach. Further, our strong results continued across
key geographies in the fourth quarter, including North America up 10%, Greater China rising 30% and
Europe increasing 25%, highlighting the global resonance of the brand. Coach is bringing new
consumers into the category and growing the market. Given the strength of the brand and our large
addressable market, we continue to see a clear path to Coach becoming a $10 billion brand.
Now to cover our fourth quarter results in more detail. Our creative teams continue to execute with
clarity and purpose, delivering product innovation that is resonating with consumers. Our icons
continued to outperform, consistent with our strategy with broad-based strength across the assortment.
The New York family, including Brooklyn, Empire and Chelsea, along with the Tabby and Teri families,

drove strong Gen Z acquisition and reinforced Coach's leadership in its core category with a robust
innovation pipeline ahead. Structurally, we concentrate product innovation behind core families that
build over time while remaining disciplined in our pursuit of growth.
More broadly, our results reflect the strategic choices we've made to strengthen the brand. Perhaps the
most significant has been our One Coach strategy. By deliberately blurring the traditional industry lines
between retail and outlet channels, bringing collection product at full price into outlet and unifying our
digital experience through a single coach.com, we've aligned our approach with how consumers shop
today, creating a stronger, more consistent global expression of the brand. This has driven customer
acquisition, higher AURs and growth around the world. Next, turning to footwear. We delivered high
teens growth in the quarter with increasing demand from Gen Z. Sneakers continued to fuel the growth
driven by the success of the Soho family, along with continued strength of Margot. Footwear remains a
long-term growth opportunity for Coach, given our brand strength, low share of the market and the
category's relevance to our target consumer.
Turning to marketing. Our strategic investments continue to generate compounding benefits this
quarter. We increased marketing spend by approximately 20% versus the prior year with a continued
shift toward top-of-funnel brand building to support sustained customer acquisition. Coach's Explore
Your Story campaign continued to resonate, supporting increased unaided awareness and reinforcing
Coach's top-of-mind presence among Gen Z. Building on this momentum, we launched &Coach, a
campaign co-created with Gen Z that celebrates moments of becoming and the confidence a Coach bag
can champion along the way.
Additionally, our partnerships extended Coach's reach into new communities and cultural
conversations as we launched the second season of our WNBA partnership, strengthening the brand's
connection at the intersection of fashion, sports and culture. Collectively, these actions are reinforcing
Coach's cultural relevance and driving customer acquisition. More importantly, they strengthen a
competitive advantage, a deep understanding of the consumer and an ability to consistently translate
those insights into demand creation at scale. And finally, we deepen consumer engagement through
distinctive brand experiences.
We continue to roll out our expressive luxury store concept globally. These stores are driving higher
traffic and longer dwell times, particularly among Gen Z consumers, supporting our plan to expand the
concept to impact approximately 80% of our traffic by fiscal year '30. In addition, Coach Play continues
to serve as both a destination for consumers and a source of inspiration for our broader store strategy.
New Coach Play locations in Chicago, Atlanta and Le Marais in Paris are helping build brand desire
with our target consumers. Together, these investments reflect our conviction that physical retail
remains one of our most powerful opportunities to express the brand as consumers invite us into their
world to share important moments in their life, extending the connection well beyond a transaction.
In closing, my confidence in the future of Coach is grounded in the combination of an iconic brand, a
deep understanding of today's consumer and an organization that continues to thoughtfully steward
and evolve the brand, preserving what makes it distinctive while ensuring it remains relevant for new
generations of consumers. I believe that combination positions Coach for continued leadership,
meaningful growth and long-term value creation.
Turning to Kate Spade. Our strategy for Kate Spade has been deliberate and phased: streamlining the
business, solidifying the foundation and positioning the brand to scale. At its core, that means building

greater brand desire and relevance to drive sustainable, profitable growth. In fiscal year '26, we remain
disciplined in executing that strategy, making choices that improve the quality of the business.
Although top line progress was more gradual than we planned, our experience has given us greater
clarity on where consumers are responding, where our investments are driving results and where we
need to focus going forward.
Now turning to our strategic pillars and fourth quarter results. First, we are committed to fueling brand
desirability supported by marketing. During the fourth quarter, we focused on increasing the reach and
relevance of our full funnel marketing activities, which resulted in higher brand consideration among
Gen Z in our latest U.S. Brand Health Tracker. In addition, our first creator-led YouTube campaign
drove an increase in purchase intent well ahead of the platform benchmark, showing traction in our
work. We also know that we need more consumers to engage with our content as unaided brand
awareness more broadly has not yet improved, and this is a key part of driving acquisition and
ultimately growth.
As we enter fiscal year '27, we'll build on these learnings through creator partnerships and activations
that drive brand awareness and desire. We're also pleased to welcome Allison Badea as Chief Marketing
Officer, who brings deep brand-building experience from the luxury and beauty industries. Next, we
continue to build a more focused assortment grounded in consumer insights. Our handbag
blockbusters, led by the Margot, 454 and Duo families, contributed to continued improvement in
handbags and drove customer acquisition, particularly among Gen Z consumers. We welcomed over
450,000 new customers during the quarter and approximately 2 million for the full year, with these
consumers transacting at higher AURs than the balance of the customer base, a foundational element
of our strategy.
Finally, we continue to focus on creating compelling omnichannel experiences. Our light-touch
renovation program, designed to bring more color and emotion to our stores, continued to drive a lift in
sales through improvements in conversion and average transaction value, and we're expanding those
learnings across additional locations. Looking ahead, as we move from streamlining to solidifying our
foundation and preparing to scale, we're focused on further strengthening our creative execution and
product and storytelling. The appointment of Jonathan Saunders as Executive Creative Director,
working alongside Eva, will advance our efforts to bring uplifting luxury to life for a new generation of
consumers with the distinctiveness of joy and femininity inherent in this iconic brand.
To close, Kate Spade has significant long-term potential, and our conviction in that opportunity
remains unchanged. We'll continue focusing our efforts and investment behind the initiatives that are
strengthening the brand and positioning it for sustainable, profitable growth over time.
Before turning it over to Scott, I'd like to come back to Tapestry's vision: to give more people the power
to bring their own style and story into the world. Throughout fiscal 2026, we realized that vision by
welcoming millions of new consumers to our brands, deepening our relationships with existing
consumers and delivering the creativity, value and relevance that inspire self-expression across
generations and geographies. Our success is by design. We will continue to stay curious, remain focused
and earn the trust of consumers every day. This is how we will continue to build advantages that
compound, delivering durable growth and long-term shareholder value.
With that, I'll now hand it to Scott.

Scott Roe (Executives)
Thanks, Joanne, and good morning, everyone. As Joanne highlighted, we achieved the financial
commitments we established at Investor Day 2 years ahead of plan, driving a step change in our
earnings power and cash flow generation. From this stronger foundation, we enter fiscal 2027 confident
in our ability to deliver mid-single-digit annual revenue growth, continued operating margin expansion
and low double-digit EPS growth, consistent with our long-term commitments. Importantly, our
competitive advantages translate into a differentiated financial model. We operate in an attractive
category with durable demand and compelling margin characteristics. As we continue to welcome new
customers to our brands and category, we generate higher quality growth and strong cash flow,
supported by disciplined capital allocation. That combination gives us the power and flexibility to
consistently invest in the business while returning meaningful capital to shareholders.
With that, let me walk through our fourth quarter results in more detail, starting with revenue trends
on a pro forma constant currency basis. Sales increased 11% compared to the prior year, highlighted by
strong global momentum. North America sales rose 7% compared to the prior year, driven by a 10%
increase at Coach, where we continue to drive healthy growth at expanding gross margins. In Europe,
revenue grew 19% versus last year, fueled by continued strength in our direct business and robust new
customer acquisition, particularly among Gen Z. Local consumers continue to drive growth,
contributing to meaningful market share gains in the region. Given our relatively low penetration, we
believe Europe remains a compelling long-term growth opportunity.
Now turning to Greater China. Revenue rose 28%, driven by broad-based growth across channels, led
by digital and strong customer acquisition. We are winning with Gen Z consumers through compelling
creativity and relevant activations, contributing to significant market share gains. Given the size of the
opportunity and the momentum we're seeing in the business, we're continuing to make strategic
investments in the region, positioning us for long-term growth in this important market. In Other Asia,
revenue increased 22%, led by growth in South Korea and Australia. And in Japan, sales declined 4%,
as expected, reflecting our intentional pullback in promotions.
Now touching on revenue by channel for the quarter. Our D2C-led model continued to drive strong
results, with direct-to-consumer revenue increasing 11%. Digital sales grew approximately mid-single
digits, while global brick-and-mortar sales increased in the mid-teens. Importantly, all channels
delivered strong and increasing profitability.
Moving down the P&L, we continue to drive healthy gross margin expansion, delivering a fourth
quarter gross margin of 78.1%, up 180 basis points versus last year. This was driven by an operational
increase of 170 basis points as well as a favorable 60 basis point impact from the divestiture of Stuart
Weitzman. These benefits more than offset a tariff and duty headwind of approximately 60 basis
points, including approximately 30 basis points at Coach and approximately 250 basis points at Kate
Spade. Overall, our strong gross margin remains a core element of our value creation model, supported
by an agile supply chain that enables us to deliver craftsmanship at scale, one of Tapestry's key
competitive advantages.
Turning to SG&A. Expenses increased 8%, while leveraging 80 basis points versus last year. This was
inclusive of a 130 basis point increase in marketing, which represented 14% of sales in the quarter.
Together, this reflects strong operational discipline and our continued ability to invest behind growth
while expanding profitability. Overall, operating margin expanded 250 basis points in the quarter,

driving a 25% increase in operating income and exceeding our expectations. Fourth quarter EPS of
$1.32 increased 28% versus last year, also exceeding our guidance despite a headwind of more than
$0.05 from a higher tax rate versus plan due to a number of discrete items.
Now turning to shareholder returns. In fiscal '26, we returned $1.7 billion to shareholders. This
included $326 million in dividends and $1.35 billion in share repurchases, representing approximately
11.5 million shares at an average price of $118 per share. Turning to fiscal '27, we expect to return
another $1.7 billion to shareholders. Our Board approved a 16% increase in the dividend to an
annualized rate of $1.85 per share, and we expect to repurchase approximately $1.35 billion of shares,
underscoring our confidence in the future. Our ability to return significant capital to shareholders while
continuing to invest for growth reflects the strength of our business and the consistency of our free cash
flow.
And now, before turning to the details of our balance sheet and cash flows, I'd like to reiterate our
capital allocation priorities, which are unchanged. We have 2 foundational commitments: first, to
invest in our brands and business to support long-term sustainable growth; and to return capital to
shareholders via our dividend, with the goal over time to increase the dividend at least in line with
earnings growth. Beyond these 2 foundational commitments, our robust cash flow generation provides
us with balance sheet flexibility for value creation. This includes the opportunity for share repurchase
activity under our previously announced share repurchase authorization.
And finally, utilizing our rigorous 4-lens framework, we consistently evaluate opportunities for strategic
portfolio management. Importantly, and as previously communicated, before moving forward with any
acquisitions, we will ensure Coach remains strong and Kate Spade has returned to sustainable top line
growth. These clear capital allocation priorities are underpinned by our firm commitment to a solid
investment-grade rating and maintaining our long-term gross leverage target of below 2.5x.
Now turning to the details of our balance sheet and cash flows. We ended the year with nearly $1.2
billion in cash and short-term investments and total borrowings of $2.4 billion, representing net debt
of $1.2 billion. Our gross debt to adjusted EBITDA leverage ratio was 1.1x, more than a full turn below
our long-term target. Adjusted free cash flow totaled $1.86 billion for the year, and CapEx and cloud
computing costs were $217 million. Inventory levels at year-end were 4% below prior year, slightly
below expectations due to a shift in receipt timing into Q1. For fiscal '27, we expect inventory levels to
increase year-over-year in support of our growth ambition.
Now moving to our guidance for fiscal '27, which is provided on a non-GAAP and comparable 52-week
versus 52-week basis. Our full year guidance remains consistent with the long-term financial algorithm
we established at Investor Day. Now turning to the details. For the fiscal year, we expect revenue of
$8.4 billion to $8.5 billion, representing mid-single-digit growth on a nominal and constant currency
basis. FX is expected to be a 40 basis point tailwind for the year.
Touching on sales details by region on a constant currency basis. As we've previously discussed, our
long-term algorithm contemplates disciplined growth in North America and an increasing contribution
from international markets, where our brands remain underpenetrated and we see substantial
opportunity over time. In North America, we expect revenue to increase low single digits. In both
Europe and Greater China, we expect growth of mid-teens. In Japan, we're forecasting a return to
growth. And in Other Asia, we anticipate high single-digit gains. By brand, this guidance incorporates
high single-digit growth at Coach and a high single-digit decline at Kate Spade.

In addition, our outlook assumes operating margin expansion of 50 basis points to nearly 24%, driven
by both an increase in gross margin and SG&A leverage. This reflects our continued ability to invest
behind our brands while expanding profitability. We expect gross margin to increase by approximately
30 basis points, driven by operational improvements and favorable geographic and brand mix.
Embedded in our outlook is the assumption for a mid-20s percent tariff rate on U.S. imports for fiscal
'27, resulting in a roughly net neutral P&L impact year-over-year, including mitigating actions.
On SG&A, we expect approximately 20 basis points of leverage, reflecting disciplined expense
management while continuing to invest behind brand growth. For some texture on operating profit by
brand, we expect Coach to maintain its best-in-class operating margin of nearly 36%. At Kate Spade, we
expect a modest operating loss, reflecting continued investment in the brand. Corporate expenses are
expected to leverage for the year, a trend we expect to continue.
Moving to below-the-line expectations for the year. Net interest expense is expected to be
approximately $55 million. The tax rate is expected to be approximately 18.5%, and our weighted
average diluted share count for the year is expected to be approximately 203 million shares. Taken
together, we expect EPS of $7.80 to $7.90, representing low double-digit growth versus the prior year.
As a reminder, our guidance is provided on a comparable 52-week basis. Fiscal 2027 includes a 53rd
week, which is expected to contribute approximately 1 percentage point of annual revenue growth and
have neutral impact on operating margin.
Moving on, we anticipate adjusted free cash flow to approach $1.7 billion. And finally, we expect CapEx
and cloud computing costs to be in the area of $300 million or 3% to 4% of revenue. This reflects a
step-up in investment to support future growth, including incremental investment in Coach's store fleet
through new openings and renovations. Approximately 70% of our spend will be related to growing and
enhancing our fleet, with the balance primarily supporting our ongoing technology and digital
investments.
Before turning to the first quarter, let me briefly comment on our approach to guidance and the shape
of the year. Our current quarter guidance reflects our latest thinking, while the balance of the year
embeds in aggregate the long-term financial algorithm we've established. On the phasing of the year,
keep in mind that we continue to operate in an environment of macro uncertainty and evolving tariff
dynamics alongside shifts in the cadence of our marketing investments. As a result, quarterly
profitability will be uneven, with tariffs providing a modest benefit in the first half of the year before
becoming a headwind in the second half.
Generally, revenue is forecasted to grow high single digits in the first half of the year and mid-single
digits in the second half, with Q4 above Q3 given prior year compares. From an EPS standpoint, we're
incorporating low double-digit growth in both the first and second half.
Touching on Q1 guidance specifically. We expect revenue growth of high single digits on both a nominal
and constant currency basis versus prior year pro forma revenue. This includes low teens growth at
Coach, which represents mid-30s growth on a 2-year stack basis. And at Kate Spade, we've embedded a
low double-digit decline. Turning to margins. We expect gross margin to increase by 120 basis points in
Q1, offset by higher SG&A due entirely to continued increases in marketing, resulting in operating
margin in line with prior year. Taken together, Q1 EPS is forecasted to be approximately $1.55, a low
teens increase.

In closing, fiscal 2026 demonstrated both the quality and potential of our business. We achieved
Tapestry's revenue, operating margin and EPS commitments established at our Investor Day 2 years
ahead of plan while continuing to invest in our brands, capabilities and future growth and returning
$1.7 billion to shareholders. We enter fiscal 2027 with confidence. Our outlook is consistent with the
long-term financial algorithm we established at Investor Day, reflecting the durability of our model and
the quality of our growth. The strength of our category, our brands and our operating model gives us
the power and flexibility to consistently invest for growth while returning meaningful capital to
shareholders. These advantages continue to compound, driving durable growth and long-term
shareholder value.
I'd now like to open it up for your questions.
Operator (Operator)
[Operator Instructions] We'll take our first question from Matthew Boss with JPMorgan.
Matthew Boss (Analysts)
Congrats on a nice quarter. So Joanne, you delivered a very strong fiscal '26 and are guiding the first
quarter to continued strong growth, particularly at Coach. But the full year outlook does embed some
moderation as the year progresses. Could you just walk us through how you're thinking about the setup
for fiscal '27, including current demand at the Coach brand relative to that low teens guide for the first
quarter? And what gives you confidence in the durability of growth in the back half and beyond from
here?
Joanne Crevoiserat (Executives)
Matt, we're incredibly confident in the durability of our growth. And as we think about the setup for
fiscal '27, I'll just step back and provide a little context. As you mentioned, we had a strong fiscal '26,
where we achieved our Investor Day commitments 2 years ahead of plan while strengthening the
company for the long term. And this is a critical point because we see that our greatest opportunities
are still ahead of us. In fiscal '27 and beyond, we're growing from a higher base while maintaining our
algorithm. The algorithm that we rolled out at our Investor Day, we're maintaining that algorithm for
durable growth into the future.
And more important than the results we delivered last year, which are incredible, it's the business we
built to deliver them. Over the last several years, we've strengthened our brands, we've deepened our
direct-to-consumer relationships, and we've expanded our global reach and built differentiated
capabilities, as I said in my prepared remarks, in data, decision intelligence and AI. We also
meaningfully improved profitability and cash generation, which increases our capacity to invest behind
future growth. These are the capabilities that matter because they extend beyond a single quarter. They
help us translate those consumer insights to action at scale and deliver that creativity, the value and the
relevance to consumers around the world.
So as we enter fiscal '27, we see that strength continuing, led by Coach, where our performance remains
strong across new and existing customers and in our core category, our core leather goods category. So
the takeaway is that fiscal '26 demonstrated the power of our strategy and our Q1 and fiscal '27 outlook
reinforces our confidence in the durability of what we've built into the future.
But I'll turn it over to Scott to cover the details and the cadence of our guidance.

Scott Roe (Executives)
Just building on what Joanne just said, we had a great '26, and we're a bigger business, we're more
profitable, we're generating more cash, which really puts us in a position of strength as we think about
our entry into '27 in the guide. And our outlook reflects that confidence, but also discipline in how we
give guidance and how we plan. Q1 does capture our current estimates for the business. We expect low
teens revenue growth at Coach. That's consistent with what we delivered in Q4. So the momentum
continues. And importantly, our full year guide doesn't require us to keep that same level of growth at
Coach for the balance of the year. So we believe, as we sit here today, that's a prudent approach.
For fiscal '27, we expect mid-single-digit revenue growth, continued operating margin expansion and
low double-digit EPS growth. At Tapestry, that's consistent with the long-term framework we
established at our Investor Day from a meaningfully higher base. At Coach, we continue to expect
growth above our brand's Investor Day framework at best-in-class margins. So we're comping the
comp. So put simply, Q1 reinforces our confidence. We've built the full year outlook to reflect the
breadth, flexibility and discipline of the model that we built.
Operator (Operator)
We'll move on now to Alex Straton with Morgan Stanley.
Alexandra Straton (Analysts)
Congrats on a great quarter. I wanted to focus from a guidance perspective on what you're assuming
from a unit versus AUR perspective after such strong AUR growth in recent years. And can you also just
dive into -- in the fourth quarter, if units were flat and kind of what was driving that?
Todd Kahn (Executives)
I'll start and participate with Scott. We love the mix on AUR and units that we delivered in the fourth
quarter. And I think, again, what's important is the quality of our sales. We are very focused on
durability and quality. And what you saw in the fourth quarter is a lot of our growth came from AUR,
and we were in line on units, which was by design. We had fewer promotion days in the fourth quarter.
And one of our strategies that we talk a lot about, you heard it in Joanne's prepared remarks, is our One
Coach strategy. Remember what One Coach allows us to do. It recognizes the consumer sees brands
and not channels. So that has allowed us to put our collection product in our outlet stores, attaining
higher AURs and full price.
And you're going to continue to see that. So throughout the year ahead, we'll see AUR gains across the
globe, and you'll also see unit gains. But what we're not going to do, we have no need to do is churn
units to make our numbers. And you see that in this world-class gross margin that we're maintaining.
So I feel very good about our mix. And ultimately, as we continue to bring new customers into the
category because remember, Coach is growing the category globally. That will, over time, increase our
unit counts as well.
Scott Roe (Executives)
Yes. And I'll just make a quick build on Todd's comment, Alex. First of all, Q4 came exactly like we
expected as it relates to units. Remember, we had some shifting of timing of promotional events and
also we had exceptional sell-through in Q3, which took some of those units from Q4 to Q3. So as it

relates to the unit dynamic, it occurred exactly as we expected. Actually, we beat the guide in total and
actually did a little bit better on an overall basis for Coach. And I just want to reiterate going forward,
our expectation, what's embedded in our guidance assumes both unit and AUR growth in '27 and
beyond.
Operator (Operator)
We'll move on now to Ike Boruchow with Wells Fargo.
Irwin Boruchow (Analysts)
A couple of questions. I'll fit into one question on North America. So basically, at Coach North America,
you guys have been moderating off of the big growth rates that you put up pretty smoothly. I think it
was mid-20s in the first half, mid-teens in the back half. I'm just curious how you're thinking about the
normalization of domestic growth at Coach. And to that point, up 10% in the fourth quarter, how much
of a headwind was there to North America growth on some of the shifts you had called out last quarter?
And then what kind of North America growth underpins that first quarter low teens global Coach guide
you guys gave?
Todd Kahn (Executives)
Yes. We love the position we have at Coach in North America. And again, when -- Scott just indicated,
some of the North America foundational, we had an outstanding third quarter and took a lot of units.
And then in the fourth quarter, we intentionally reduced our promotion days. So we feel very good
about our North America growth. We're going to -- you're going to see us grow. We grew beyond the
category in the fourth quarter. So that's an important milestone.
And what we love is what we said we were going to do. We're 2 years ahead of our plan. We are
delivering something on a much higher base. We took the global floor up from mid-single digits to high
single digits for this year. And remember what we told you we would do: 70% of our growth is coming
internationally. That said, we love our North America position, and you're going to continue to see us
grow in North America. But we're going to -- we're growing on a very large base, and we're going to
grow very intentionally, not degrading the brand, not degrading our margin and continuing to focus on
bringing new customers into the category.
Scott Roe (Executives)
Yes. And a quick build on the numbers, Ike. If you look at the Coach guide for North America, again, as
Todd said, it's really above our Investor Day expectations for '27. And a little bit more on that. If you
look at the 2-year stack for North America Coach in both Q4, Q1 and the full year guide, it's about 30%,
right? So we're comping the comp. We're consolidating the exceptional growth from last year and
compounding that as we look forward into '27, and that's embedded in our guide here. So the strong
momentum in Coach continues, and we have a lot of confidence in our growth, not only in Coach
overall, but in Coach North America specifically.
Operator (Operator)
We'll move on now to Michael Binetti with Evercore.
Michael Binetti (Analysts)

First off, let me just say thanks for bringing us out to headquarters tomorrow. Look forward to seeing
you guys learning about AI. Scott, can I just ask a little clarification on Ike's question? Should we think
about a 30% 2-year stack on the North America Coach business in the first quarter and then we just
kind of pencil that through the rest of the year to kind of hold that stability against those tough
compares that continue through the year?
And then maybe just a little bit on the gross margin bridge. I think it implies almost no expansion after
first quarter despite, I think, a lot of the growth coming from the Coach brand, from China, from the
high gross margin categories. Maybe just a bit of a bridge on the growth throughout the year.
Scott Roe (Executives)
Yes. So we can't wait for you guys to come. A couple of dozen of our closest friends going to see what
we're doing in the AI world and really talk about how this is really a competitive advantage for
Tapestry. Joanne mentioned it, and we're excited to talk about it because we think it's truly part of the
moat of what makes Tapestry special. Yes. So for gross margins, listen, it's going to be a little lumpy
through the year. We also talked in my prepared remarks about the impacts of tariffs, which are a net
benefit in the first half and that tailwind in the second half, kind of a push on a year-on-year basis. I
think the important thing to take away here is we are growing gross margin about 30 bps for the year.
It's implied in our guidance.
And the structural drivers of gross margin, which we've talked about over and over, the strength of our
brands, AUR, AUC, the fact that international margins are higher and we're growing more outside the
U.S., all those structural drivers are unchanged and remain just as true today as they have been. As we
sit here today, we think the guidance we've given is prudent looking how much real estate we have. But
don't take away from that any change in terms of those structural growth drivers. They're still in place.
Michael Binetti (Analysts)
Okay. And then the North America?
Scott Roe (Executives)
In terms of North America, well, I think you reiterated what I said in terms of -- we see low single-digit
growth in North America, overall, that's consistent with our long-term algorithm. But as I said earlier,
Coach at mid-single digit in both Q1 and for the full year is really above our expectations and really
continues the momentum that we've seen in North America specifically.
Operator (Operator)
We'll move on now to Bob Drbul with BTIG.
Robert Drbul (Analysts)
I was just wondering if we could shift a bit and spend some time just expanding on the international
growth, I guess, specifically in Europe and in China, sort of what you're seeing in both markets and just
the expectations on how to drive those businesses forward in fiscal '27 and beyond.
Joanne Crevoiserat (Executives)
Thanks, Bob. Maybe I'll start and then toss it to Todd for some color. We just reported a strong fourth
quarter and an amazing fiscal year. Our business was strong around the world, and we're seeing broad-

based strength. We just talked a lot about the strength we're seeing in North America, and we see that
continuing for Coach with further growth ahead. But as we look forward, international does become a
larger contributor to our growth, and we see continued opportunity.
So in China, as an example, we delivered over 30% growth on the year in China. We're driving that
through new customer acquisition. That growth is broad-based across the market. And we are well
outpacing the industry in China, and we see tremendous opportunity as we move forward in China to
continue to drive growth just based on our relatively low brand awareness in the market and the
opportunity that we see for further penetration, more new customer acquisition and the traction that
we have, particularly with this young consumer. And if I shift to Europe, the opportunity is the same.
We have relatively low penetration in the market. We are gaining traction with a local and younger
consumer, and we have an opportunity to continue to drive growth in Europe as well.
But maybe, Todd, I send it to you for a little bit more color on how you're thinking about that growth.
Todd Kahn (Executives)
Thanks, Joanne. Let's -- I'll kick off where you left off Europe. I mean we've had multiple years of
double-digit growth, and we truly early innings. When we even talk about Europe, we're only
penetrated in any material way into the U.K. and some wholesale and some marketplace. We now are
taking France. We opened a new store in Le Marais, a Coach Play store, which is the heart of where
young people shop. It's a good beacon for our brand. But the 35, 40 countries that we can still tackle in
Europe gives us a huge runway.
And what's important about the Coach brand positioning in Europe and in China is the value and value
proposition. The absolute underlying value of our product, our bags is cutting through, and it's clear.
That's why we're winning, and that's why we're competing. And we're supporting that by incredible
storytelling and marketing. And if I go to China now, we underinvested in China over the years. Today,
we're trying to bring our marketing in line with our overall marketing expense. And that is the fuel that
creates demand in the market. So our marketing is a driver of business.
And what I love is our position in China. Again, I'll remind everybody, we've been there for 25 years.
We have deep roots in China. We have rich teams in China who understand the culture. We make sure
that our brand, our product offering resonates with that customer. And we're also not limited because
of our expressive luxury position to simply go where traditional European luxury goes. We go where the
Gen Z customers want to shop. That's a huge unlock for us, and you're going to see us grow materially
in China, in Europe and continue to grow in rest of Asia as well.
Operator (Operator)
We'll move on now to Jay Sole with UBS.
Jay Sole (Analysts)
You talked a lot about your confidence in maintaining the momentum at Coach brand. Can you talk a
little bit more about product? I'd say the Brooklyn family has been such a great product franchise for
the brand. Can you talk about some of the ideas you have that you have confidence in, in the future and
what we're going to see from a product standpoint that give you that confidence that the momentum
can continue?

Todd Kahn (Executives)
Sure. I'll even open the aperture up just a little bit about my confidence because I want to remind
everybody, we're an 85-year-old brand. And even as an 85-year-old brand, this last year, we recruited 9
million new customers. That's powerful. But we're not resting on our history or relying on our
momentum. What gives me confidence overall is the clarity that we bring to all facets of our business,
the clarity on our purpose, our customers, our product, our marketing, our people and our culture. And
I will say that clarity is greater today than any time in my 19 years here at Coach and quite honestly,
greater than anything I've seen in 30 years in this industry. And it does start with our purpose.
And I know sometimes, with this crowd, in the investment crowd, talking about purpose, your eyes
sometimes glaze over, but it matters. Our purpose and our courage to be real and our aspiration of
being the most inclusive, authentic and loved fashion brand matters to our people, and it is a rallying
cry, and it drives outcomes. That leads to our customers. We have clarity of who we are designing for
this point of market entry, what you heard Joanne and Scott talk about, which is a large TAM that we
can go after, 25 million women turning 18 every year in the markets we play that can afford our bags,
which leads back to your -- the essence of your question, which is our product.
And what Stuart Vevers and our design teams and our merchant teams are doing is phenomenal. We
are building on diverse yet very clear platforms of product. We talk about our icon, Tabby. We have a
lot of runway to continue to evolve Tabby, and we have not seen any slowdown in Tabby. Similarly, our
New York family, Brooklyn, is doing extraordinarily well. And again, it's a multichannel concept that we
sell at full price across many different -- frankly, all of our different avenues of sale. And even under the
New York family, we've expanded ideas like our Chelsea bag, which all of a sudden was only a year old
and is now appearing on the top 10. So these very large platforms, as well as Teri, we sometimes refer to
them as TNT here, which has led to this explosive growth. We feel very good about our product offering
and our assortment backed by our marketing stories.
So net-net, the product is strong. The clarity of our messaging is strong. And I think we have an
incredible setup, not just for the year ahead, but for our aspirations of $10 billion. And I'm starting to
think about how much further we go beyond $10.
Operator (Operator)
We'll move on now to Adrienne Yih with Barclays.
Adrienne Yih-Tennant (Analysts)
Congrats. Very nicely done. Todd and/or Joanne, I'm going to stay on that topic. When I look at the
metrics that you reported, I expected the ones on the P&L, the one that really surprised -- was nicely to
-- surprising was the customer acquisition. To me, that represents sort of future demand and kind of
gives me some confidence about this flywheel. So that being said, can you talk about just the white
space in pricing, entry level pricing, the Gen Z that you're going after and then geographies? Because
when I look at it, I just don't -- I can't come up with a really good competitor on any of those fronts. So
can you talk about how you think? Who do you look over your shoulder and you're worried about, just
to talk about that?
And then also, for Scott, what's the implied advertising as a percent of sales for the FY '27 because that's
kind of also helping the flywheel. And then also on the guidance, is Coach North America for mid-single
digit, is that for Q1? Or is that for the year? Or for both Q1 and the year?

Joanne Crevoiserat (Executives)
You've got a lot in there, Adrienne. I'm going to kick it off. I think this will be a 3-part. I'll kick it off, and
I'll toss it to Todd for a little bit of color if there's anything left after I talk, and then Scott will clean it up
with some of your guidance questions. You're hitting on the kernel that is driving our growth, and that
is new customer acquisition. We have become just obsessed with our customer. This customer
obsession starts with understanding them and then delivering product and marketing and storytelling
and experiences that are relevant to our target customer. And that muscle -- that brand-building
muscle that we're building at Tapestry, it's a playbook that is repeatable. We continue to invest in the
capabilities to deepen our understanding of the consumer and then move from insight to action. And
that's where it matters for our customers, to deliver something that our customers -- that resonates
with them, that they fall in love with.
And these new customers who we're acquiring, we talked about 11 million new customers in the last
fiscal year, are joining at higher-than-average AUR. They're a younger consumer base. This point of
market entry strategy that we have not only is an opportunity to retain these customers and drive
lifetime value, but what we're finding and what we know, I think we all know that the young consumer,
the youngest generation influences all generations, and we're seeing that play out in our business
because our existing customer base is also growing. So this flywheel of driving new customer
acquisition and then giving them such a terrific experience that they come back. We're seeing those
retention rates among the highest retention rates in our customer file.
So they're loving our brands. They're staying with our brands, and they're influencing all generations.
And we're continuing to invest behind those capabilities so that we can continue to drive that flywheel.
It's happening in North America. We spent a lot of time talking about North America growth today, but
we also see a tremendous opportunity in international markets to drive new customer acquisition.
We're bringing more customers into the market. So we're growing the market, and we're growing our
share. And that's a phenomenal place to be.
Todd, I don't know if there's anything you want to add from a color perspective.
Todd Kahn (Executives)
You touched on so many good things, but I do want to tackle the one thing you didn't talk about, which
is competition. And for me, there are no barriers of entry in our space. That's just the truism that we
recognize every day. It almost doesn't matter. What we -- the moats we are building are about that
connective tissue to our customer. When we spend 12% on advertising -- and I think my marketing
team will be mad at me because I use the word advertising. It's not advertising. It's story building. It's
brand driving. It's not just go buy our bag. It's a richness that makes it compelling.
When we say we're going to invest in our store fleet and refurbish, we are going to tackle 80% by traffic
of our store fleet between now and FY '30. That's an investment into the future that makes us relevant
and continues to attract that younger consumer globally. And that's why we're so excited about this
rollout of expressive luxury. So couple that with the fact that we are an 85-year-old brand. September,
Stuart is going to a fashion show, celebrating our 85th anniversary. Those are things that are hard to
replicate. And that's why finally, I go back and talk to a lot about our culture. Our winning culture, a
team that understands, a team that's been together. We have stability of leadership. We have stability of
design. Those are important drivers of long-term profitability.

So I love our setup. We are going to be very focused on that $200 to $500 space. Yes, we have some
amazing bags above that, but that clarity of brand positioning is what is driving our customer
acquisition and retention.
Scott, I don't know if I left you anything.
Scott Roe (Executives)
All right. You left me a little bit. There was a spoiler alert. He threw out the 12% is indeed percent of
demand creation that's both in -- we hit that in '26, and we're building upon that. It's the flywheel we
talked about, right? We grow gross margins. We have discipline across the rest of the business so we
can invest back in things like demand creation, which are the engine that drive our new customer
acquisition, doing all of that with 50 basis points of operating margin expansion. So 12%, another data
point there. It's about $1 billion in advertising. So you think about where we were 5 years ago versus
today in terms of demand creation, that's a big number because, to Todd's point, while there's no
barriers to entry, there are barriers to scale, and those barriers are getting higher. And companies who
have a business model that can reinvest and create demand in the way that we can, well, this is the
moment we prepared for, for a long time, really sets us apart and is a competitive advantage.
And I'm glad you asked for clarification on Coach. I want to try to be very clear here. So Coach, we
expect in Q1 to grow mid-single digits. We also expect full year Coach to grow at mid-single digits. And
the point I made earlier is we're comping the comp or compounding on the growth. So whether we look
at North America Q4 last year, Q1 this year or full year this year, that's about a 30% 2-year comp for
North America. So not only are we a much bigger business, we're growing significantly on top of that
big business. And when you think about, Todd, you got a huge North American business, over $4
billion, we can talk about percentages. This is real growth. And at our margins and at the flow-through
that we have based on the efficiency of the model, it's a really important part of our financial story. And
one of the reasons we have confidence is our North American Coach business.
Todd Kahn (Executives)
And just to be abundantly clear because I want to make sure we're talking mid-single digits in North
America for the Coach brand. We're talking in the first quarter, low teens. And for the full year, for the
Coach brand overall, we are talking high single digits. I didn't want any of my BU heads to think they
got off the hook on this phone call. So those are the floors that we've set for this year. And I think our
track record of beating out the floors are quite substantial.
Adrienne Yih-Tennant (Analysts)
Your track record is great indeed.
Operator (Operator)
We'll move on now to Mark Altschwager with Baird.
Mark Altschwager (Analysts)
Just first on marketing, it did not delever as much as you had guided in the fourth quarter. Could you
just clarify how much of that is a shift in timing versus realizing some greater efficiencies and how that
then plays into fiscal '27? And then separately, the CapEx step-up, the reinvestment in the fleet, how

should we be modeling or thinking about net door growth for Coach in fiscal '27? And how does that
play out by region?
Scott Roe (Executives)
Yes. So I'll take the first part of that, Mark. Yes, listen, with marketing, there's always a little bit of
timing. And we've created a model, I'll go back to the flywheel, that allows us the flexibility to be
opportunistic and lean in when the data tells us we have opportunities, but we don't just spend to
spend. Also timing of things like production and whatnot can be a little bit different on a quarter-by-
quarter basis. So you're right, we came in with a little more leverage in marketing. We still spend a lot
of money, and I'll remind you, we spent 12% of sales in 2026.
I think the much bigger issue as you look going forward is we are and will continue to invest in
marketing as a key part of our demand creation, and it's a key part of driving unaided brand awareness,
which is a key to new customer acquisition. So the flywheel is intact, and we will continue to invest in
marketing. And I think Todd is going to want to say something about the fleet, but just to give you some
numbers, between 40 and 50 doors is our expectation on a net basis at Coach. And you're right, we have
stepped up a bit our CapEx, but still, as we look at our overall guidance or our overall expectations from
Investor Day, still very much in line as we look at our forward CapEx spending. And I'll remind you,
we've got a lot more cash, too. So our free cash flow is significantly higher even with these investments.
But Todd, to you, maybe a little color on what you're doing.
Todd Kahn (Executives)
Yes. I love that this year, we will go over the 1,000 door count for Coach globally. And 75% of those 50
doors that Scott talked about will be international, 25% will be domestic. But remember what we're
doing, we are elevating the fleet with our expressive luxury design. We started a design that we
introduced in the first 6 months of last year. We paused, which was really smart. What we did was we
listened to the consumer, we evolved our thinking. And now based on that data and that input, we're
able to go roll it out, sometimes slow to smooth, smooth to fast. We're going to be able to go much
faster now that we have clarity of what the design looks like, how it operates and how the consumer
responds.
In addition, we're adding one per MSA, no more than one per MSA, what we call our Play concepts.
And you'll see the most recent version of that was in Paris. You have a new one that we did in Chicago,
one in Atlanta. So again, these beacons of Coach, which allows the consumer to interact, some of those
Play ideas then evolve into expressive luxury. So I feel very good about investing in the fleet. One of the
things we know, Gen Z love being in the real world. And if our stores -- and I want our stores to be as
engaging as the product, and that's what the expressive luxury design is doing for us. So I'm very
excited about the future growth of being a direct-to-retailer and seeing our stores, and I hope you get to
visit many of them in the upcoming year.
Operator (Operator)
Thank you. That concludes our Q&A. I will now turn it over to Joanne Crevoiserat for some concluding
remarks.
Joanne Crevoiserat (Executives)

Thanks, Leo. I want to close by reiterating my confidence in the future. The strength of our results and
more importantly, the strength of our organization are driving durable growth and long-term
shareholder value. Our advantages continue to compound, and I believe our greatest opportunities are
ahead of us.
To our global teams, thank you for the creativity, focus and commitment you bring every day. Your
work is reflected in everything we've accomplished and in the opportunities we're creating for the
future. And to everyone who joined us today, thank you for your interest in Tapestry. Have a great day.
Operator (Operator)
This concludes Tapestry's earnings conference call. We thank you for your participation.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TPR_Q3_2026_Earnings_Call_20260507.md
- 2026-05-07｜Scott Roe｜guidance：FY26 營收財測上調至約 79.5 億美元，pro forma 固定匯率成長 16%（原話："we now expect revenue to be in the area of $7.95 billion"）
- 2026-05-07｜Scott Roe｜guidance：FY26 EPS 財測約 6.95 美元，高於先前 6.40–6.45（原話："we now expect EPS to be in the area of $6.95"）
- 2026-05-07｜Scott Roe｜guidance：FY26 營業利益率財測約 23%，比先前展望高 120 bps（原話："an operating margin of approximately 23%, which is up"）
- 2026-05-07｜Scott Roe｜guidance：FY26 區域財測：北美中十位數、歐洲約 20%、大中華逾 30%、日本高個位數衰退（原話："in Greater China, we now expect to achieve growth of over 30%"）
- 2026-05-07｜Scott Roe｜guidance：Q4 財測：Coach 低十位數成長、kate spade 高個位數衰退、EPS 約 1.20 美元（原話："And Q4 EPS is forecasted to be approximately $1.20"）
- 2026-05-07｜Scott Roe｜guidance：kate spade FY26 財測為低雙位數衰退（原話："At kate spade, we now expect a low double-"）
- 2026-05-07｜Scott Roe｜guidance：財測納入現行美國貿易政策，不含 IEEPA 關稅退款（原話："This outlook embeds current U.S. trade policies and excludes any potential"）
- 2026-05-07｜Scott Roe｜margin：Q3 毛利率 76.9%，年增 80 bps，營運面擴張約 190 bps、Stuart Weitzman 出售貢獻 70 bps（原話："gross margin of 76.9%, 80 basis points above our prior"）
- 2026-05-07｜Scott Roe｜margin：Q3 關稅與稅負逆風約 180 bps，其中 Coach 150 bps、kate spade 440 bps（原話："a 150 basis point negative"）
- 2026-05-07｜Scott Roe｜margin：Q3 毛利率比內部預測好 180 bps，約一半來自營運、一半來自較低關稅（原話："approximately half of the upside due to stronger operational performance and half due to lower tariffs"）
- 2026-05-07｜Scott Roe｜margin：Q3 SG&A 費用率槓桿 410 bps，含行銷增加 160 bps（占營收 12%）（原話："leveraged by 410 basis points, inclusive of 160 basis"）
- 2026-05-07｜Scott Roe｜margin：FY26 毛利率預期增約 110 bps，營運面擴張約 190 bps，主要來自 AUR 改善（原話："operational gross margin expansion of roughly 190 basis points"）
- 2026-05-07｜Scott Roe｜margin：FY26 行銷費用率預期增約 190 bps，較先前財測多 60 bps，接近營收 13%（原話："an increase of 60 basis points from our prior guidance and now approaching 13% of revenue"）
- 2026-05-07｜Scott Roe｜margin：Q4 營業利益率預期擴張約 60 bps，毛利率增約 130 bps，行銷增逾 300 bps（原話："an increase of over 300 basis points in marketing to drive long-term"）
- 2026-05-07｜Scott Roe｜margin：管理層列出毛利率驅動：AUR（價格帶 200–500 美元內）與 AUC；稱價格約與 15 年前相當（原話："they're just about where they were 15 years ago and there's a lot of room to run"）
- 2026-05-07｜Scott Roe｜margin：管理層表示尚未為因應關稅而直接漲價（原話："we have not implemented any price increases in direct response to tariffs"）
- 2026-05-07｜Joanne Crevoiserat｜customer：Q3 全球新增逾 240 萬名新客，Gen Z 增加帶動（原話："acquiring over 2.4 million new customers globally in the quarter"）
- 2026-05-07｜Joanne Crevoiserat｜customer：Gen Z 客群留存率高於其他客群（原話："our Gen Z consumers have higher retention"）
- 2026-05-07｜Joanne Crevoiserat｜customer：Coach Q3 固定匯率營收成長 29%，新增 200 萬新客（原話："Coach welcoming 2 million new customers to the brand"）
- 2026-05-07｜Joanne Crevoiserat｜product：Coach 核心皮件銷量增逾 20%、AUR 低雙位數成長（原話："unit volumes increasing over 20% and AUR growing at a low double-"）
- 2026-05-07｜Joanne Crevoiserat｜product：Coach 鞋類成長約 20%，由 Soho 運動鞋帶動（原話："We delivered accelerated growth of approximately 20% in the quarter"）
- 2026-05-07｜Joanne Crevoiserat｜customer：Coach 區域成長：北美 27%、大中華 58%、歐洲 27%（原話："Greater China, rising 58%; and"）
- 2026-05-07｜Joanne Crevoiserat｜competition：Coach 在龐大 TAM 中市占率不到 1%（原話："with a large TAM, we have under 1% share"）
- 2026-05-07｜Joanne Crevoiserat｜competition：管理層估計北美手袋與皮件市場成長中至高個位數（原話："grew mid to high single digits"）
- 2026-05-07｜Joanne Crevoiserat｜product：kate spade Q3 營收衰退 11%，趨勢較上季改善但略低於預期，含減少促銷的壓力（原話："revenue declined 11%. Top line trends improved sequentially,"）
- 2026-05-07｜Joanne Crevoiserat｜risk：kate spade 品牌無輔助知名度尚未改善，管理層擴大行銷觸及（原話："unaided brand awareness more broadly has not yet improved"）
- 2026-05-07｜Scott Roe｜risk：中東占營收不到 1%，管理層預期無重大直接影響（原話："we do not anticipate a material direct impact to our business at this"）
- 2026-05-07｜Scott Roe｜risk：原物料通膨目前影響不大，僅燃油附加費有輕微成本壓力（原話："So, so far, Laurent, not much."）
- 2026-05-07｜Scott Roe｜capital_allocation：FY26 預計回饋股東約 16 億美元，約為調整後自由現金流 100%；回購由 12 億上調至 13 億（原話："approximately 100% of our expected adjusted free cash flow to shareholders"）
- 2026-05-07｜Scott Roe｜capital_allocation：年初至今回購 10.5 億美元，約 930 萬股，均價約 112 美元（原話："approximately 9.3 million shares repurchased at an average stock"）
- 2026-05-07｜Scott Roe｜commitment：併購前提：須確保 Coach 穩健且 kate spade 回到可持續營收成長（原話："we will ensure Coach remains strong and kate spade has returned to sustainable top line"）
- 2026-05-07｜Scott Roe｜commitment：維持投資等級評等與長期總槓桿低於 2.5 倍的目標；Q3 槓桿 1.1 倍（原話："maintaining our long-term gross leverage target of below 2.5x"）
- 2026-05-07｜Scott Roe｜commitment：股利目標：長期至少與盈餘成長同步增加（原話："the goal over time to increase the dividend at least in line with"）
- 2026-05-07｜Joanne Crevoiserat｜commitment：長期成長目標：中個位數營收成長為下限，今年已提前兩年達成 Investor Day 目標（原話："mid-single-digit revenue growth as a floor, well ahead of the category"）
- 2026-05-07｜Scott Roe｜commitment：成長算法：Tapestry 中個位數、Coach 至少中個位數為下限；AUR 至少通膨加 1 點，新店貢獻 1–2 點（原話："AUR growth of at least inflation plus a point"）
- 2026-05-07｜Joanne Crevoiserat｜commitment：Coach 長期 100 億美元營收品牌目標、維持最佳同業利潤率（原話："Coach will be a $10 billion brand over time with best-in-class margins"）
- 2026-05-07｜Todd Kahn｜commitment：新式 expressive luxury 門市預計未來幾年改造多數店面（原話："We're going to touch a majority of the fleet over the next couple"）
- 2026-05-07｜Joanne Crevoiserat｜commitment：kate spade 輕改裝格式預計財年底前擴及更多北美門市（原話："We plan to expand this format to additional locations in North America by fiscal year-end."）
- 2026-05-07｜Scott Roe｜guidance：季初至今 Q4 走勢與財測一致（原話："Quarter-to-date, we're right in line with the guide that we just gave."）
- 2026-05-07｜Scott Roe｜margin：Q4 Coach 成長較 Q3 放緩的口徑：Q3 受農曆新年、較早復活節及粉色簽名款銷售提前影響（原話："Q3 had the benefit of the Lunar New Year outperformance, a little earlier timing of"）
- 2026-05-07｜Todd Kahn｜competition：Coach 行銷年支出接近 10 億美元，管理層稱同業少有能匹敵（原話："Coach is approaching $1 billion annual spend in marketing"）
- 2026-05-07｜Todd Kahn｜competition：歐洲已連續 11 季雙位數成長，管理層稱仍有大量空間（原話："I think we've had 11 quarters of double-digit"）


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
{"date":"20260806","verdict":"觀望","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Coach 的符號溢價可延續：Tabby 老化後有接棒（Brooklyn／New York／Empire），Gen Z 復購穩定","columns":{"2Y／5Y 驗證點":"2Y：organic 連 8 季 ≥ +12%5Y：Coach 由約 $6.9B 走向 $10B","具體門檻與信息來源":"YoY ≥ +12%／季、新客 ≥ 2.0M／季、GM 守 75%。來源：Q3 FY26 法說（+29% CC、2.0M 新客）；Piper Sandler 青少年調查 Coach 手袋首選 43%（前次 23%，次級來源）","漂移觸發":"連 2 季 &lt; +10% ＝ 削弱；連 2 季 &lt; +5% ＝ 反轉"}},{"id":"H2","text":"中國二三線滲透與 Gen Z 對入門奢的 trade-down 使中國成為結構性第二引擎","columns":{"2Y／5Y 驗證點":"2Y：中國連 8 季 ≥ +20%5Y：中國成為 Coach 第二大市場","具體門檻與信息來源":"Greater China YoY ≥ +20%／季。來源：Q3 FY26 +55% CC；Bain 中國個人奢侈品 2025 −2.7%（2024 −8.8%），2026 預估 +2.5%（大摩）至 +5%","漂移觸發":"連 2 季 &lt; +15% ＝ 削弱；連 1 季 &lt; 0% ＝ 結構性反轉"}},{"id":"H3","text":"市場願持續給 17-21x Forward PE（品牌升級成功者的倍數，非停滯 mall 品牌的 10x）","columns":{"2Y／5Y 驗證點":"2Y：Fwd PE 維持 ≥ 17x 達 12 個月5Y：倍數被 EPS 兌現追上而非被壓縮","具體門檻與信息來源":"Fwd PE(FY27) ∈ [17, 21]。來源：自算 5Y NTM 區間 6.1-20.8x；RL 21.0x／LVMH 20.0x 對照錨（2026-08-06）","漂移觸發":"跌破 15x 連 2 個月 ＝ 開始 reversion；跌破 12x ＝ H3 失敗"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"it-bag 週期反轉：Tabby 老化而接棒品未達同等聲量，AUR 成長靠漲價而非需求","columns":{"時間尺度":"⚡ 短期（Q4 FY26，2026-08-13 首測）","對應假設":"H1","監測指標／警戒閾值":"Coach organic／件數成長；連 2 季 &lt; +10%","本次狀態":"🟡 未觸發但已進測試窗——Tabby 約 3 年，正是 2012 年 Coach 的相同位置"}},{"id":"R2","text":"關稅政策逆轉已確認不會發生：Section 301 強迫勞動關稅 2026-07-24 生效（越南／菲律賓 12.5%，柬埔寨／印度 10%）","columns":{"時間尺度":"⚡ 短期（已發生）","對應假設":"H1 + H3","監測指標／警戒閾值":"FY27 指引中的關稅假設；共識 EPS 中約 $0.5 的政策成分","本次狀態":"🔴 已觸發——見 §6.I。本報告據此把 Base FY27 EPS 由 $7.55 下修至 $7.35"}},{"id":"R3","text":"美國入門奢消費降級：Conference Board 信心 90.8（7 月，三連跌）；off-price 強勢（TJX 同店 +6%、Ross +17%）＝ trade-down 訊號","columns":{"時間尺度":"🔥 中期（4-6 季）","對應假設":"H1","監測指標／警戒閾值":"北美 organic；轉負即觸發","本次狀態":"🟡 部分活躍——服飾零售銷售仍 +5.7%(5月)／+13.7%(6月)，訊號矛盾未收斂"}},{"id":"R4","text":"單一品牌集中永久化：Coach 約 88% 營收，且 Kate Spade 已被公司自己減損 $855M","columns":{"時間尺度":"🐢 長期（2+ 年）","對應假設":"H1 + §2.F","監測指標／警戒閾值":"Kate Spade 分部營益率是否 FY27 轉正","本次狀態":"🔴 已惡化——前作記為「集中風險」，本次因減損入帳而升級為已實現的結構事實"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(FY27) ≤17.3x（約 $130，Base IRR 回到 10%/yr）；或 Kate Spade 分部營益率轉正連 2 季 ＋ Coach organic 連 2 季 ≥+12%，base g 上調後逢回","irr_base_pct":4.7,"ev5y_pct":17.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"衛星","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.4,"ev5y_pct":17.2,"irr_base_pct":4.7,"max_dd_pct":-60.0,"bull_5y_price":300.5,"bear_5y_price":79.1,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE(FY27) ≤17.3x（約 $130，Base IRR 回到 10%/yr）；或 Kate Spade 分部營益率轉正連 2 季 ＋ Coach organic 連 2 季 ≥+12%，base g 上調後逢回","price_at_dd":163.01,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261005/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
