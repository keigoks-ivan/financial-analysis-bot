你是 stock-analyst **v20 判斷 agent**，標的 TSM（20260916）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
        *clock_phase: str|null enum[I,II,III,IV,None]
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
        *grade: str|null enum[S,A,B,C,X,None]
        *trend: str|null enum[↑,→,↓,None]
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
        *runway_post_y5: str|null enum[🟢,🟡,🔴,None]
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
          *name: str enum[ma_roiic,buyback_yield,sbc_dilution]
          *applicable: bool|null
          *passed: bool|null
          *input: str|null
        grade: str|null enum[A,B,C,None]
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
        *val_light: str|null enum[🟢,🟡,🟠,🔴,None]
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
        *verdict: str|null enum[🟢,🟡,🔴,None]
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
    last_status: str|null enum[ok,warning,triggered,unknown,None]
  evidence_dismissed[]: arr
    ref: str|null
    reason: str|null
  *action_conditions
    *rearm_trigger: str|null ≤120
    *exec_line: str|null
    holding_cap: str|null
*decision_inputs
  *signal: str|null enum[A+,A,B,C,X,None]
  *ma: str|null enum[🟢,✅,🟡,🟠,❌,-,None]
  *cycle_position: str|null
  *cycle_verdict: str|null
  *thesis_irreconcilable: bool|null
  *valuation_dependent: bool|null
  *market_wrong_reason_given: bool|str|null
  *momentum_overheated: bool|null
  *cycle_gates_pass: bool|null
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
    *clock: str|null enum[⚡,🔥,🐢,None]
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
  *ai_risk: str|null enum[🟢,🟡,🔴,None]
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
  date_precision: str|null enum[month,quarter,None]
  *type: str|null enum[product,regulatory,capacity,guidance,macro,other,None]
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
{"meta":{"ticker":"TSM","date":"2026-09-16","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20260916/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20260916/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"營收（GAAP，合併）","value":40.2,"period":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","unit":"US$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","citation":"公司新聞稿 investor.tsmc.com 2Q26 Earnings Release（https://investor.tsmc.com/english/quarterly-results/2026/q2；同文件 SEC 6-K https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000451/a2q26e_withguidancexfinal.htm）"},"note":"consensus 約 US$39.5–40.04B（來源：web_search 綜合媒體報導，非單一權威資料庫），實際 $40.20B 落在自結指引上緣、beat consensus 約 1.4%"},{"id":"f_kpi1_tsm_taiwan_ifrs_gaap_non","label":"營業利益率（TSM 採 Taiwan-IFRS 單一口徑，未如美股公司分列 GAAP／Non-GAAP——此為結構性差異，不強行拆成兩筆數字）","value":60.3,"period":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","citation":"公司新聞稿 2Q26 Earnings Release（同上 URL），創歷史新高"},"note":"毛利率 consensus 67.1% vs 實際 67.7%（beat）；營業利益率未查到明確 sell-side consensus 數字"},{"id":"f_kpi4_guidance_q3_2026_2026","label":"管理層 guidance（下一季 Q3 2026 ＋ 全年 2026）","value":"Q3'26 營收 $44.6–45.8B／毛利率 65–67%／營業利益率 56–58%；FY26 營收成長上修至「40%以上」YoY（前次為 30%以上）；FY26 capex 上修至 $60–64B（另加碼美國亞利桑那 $100B 投資）","period":"公告於 2026-07-16 法說會","unit":"guidance range（text）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"公告於 2026-07-16 法說會","citation":"公司新聞稿 2Q26 Earnings Release ＋ 法說會逐字稿（web_search 綜合多家媒體轉引，非官方逐字稿原文）"},"note":"N/A"},{"id":"f_kpi5_archetype","label":"產能利用率（archetype=硬體/設備 追加項；定性描述，公司未揭露具體利用率百分比）","value":null,"period":"Q2 2026 法說會（2026-07-16）","unit":"qualitative","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q2 2026 法說會（2026-07-16）","citation":"web_search 法說會逐字稿摘要：管理層表示毛利率 QoQ +150bp 部分來自成本改善與「整體產能利用率提高」，未給出具體利用率數字"},"note":"N/A","needs_sonnet":true},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-07-16","period":"2026-07-16","unit":"date","basis":"距今 44 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-07-16"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_tsm_gross_margin_pct","label":"TSM 毛利率","value":64.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsm_operating_margin_pct","label":"TSM 營業利益率","value":56.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsm_fcf_margin_pct","label":"TSM FCF 利潤率","value":25.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amd_gross_margin_pct","label":"AMD 毛利率","value":53.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_operating_margin_pct","label":"AMD 營業利益率","value":15.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_fcf_margin_pct","label":"AMD FCF 利潤率","value":20.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mu_gross_margin_pct","label":"MU 毛利率","value":72.57,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_mu_operating_margin_pct","label":"MU 營業利益率","value":65.67,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_mu_fcf_margin_pct","label":"MU FCF 利潤率","value":28.99,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi2_fcf","label":"自由現金流（FCF）","value":287.36,"period":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","unit":"NT$ billion","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）","citation":"web_search 綜合法說會揭露：營運現金流 NT$783B － 資本支出 NT$496B"},"note":"無明確 sell-side FCF consensus 可查"},{"id":"f_kpi3_tsm_sbc_sbc","label":"員工酬勞性現金紅利占營收%（TSM 依台灣公司法走員工利潤分配現金紅利，非美式股權 SBC，口徑不同、不可直接類比美股公司 SBC%）","value":2.93,"period":"H1 2026 累計（非單季，查無單季拆分數字）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"H1 2026 累計（非單季，查無單季拆分數字）","citation":"web_search／SEC 6-K：H1 2026 員工酬勞金 NT$70.35B（YoY +54.3%）÷ H1 2026 營收 NT$2,404.48B"},"note":"不適用"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":413.75,"period":"2026-09-15（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-09-15（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":19.87,"period":"2026-09-15（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-09-15（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":45.54,"period":"2026-09-15（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-09-15（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.59,"period":"2026-09-09","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（16.95 → 17.05）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-09-09","citation":"DD_universe_EPS_estimates_20260909.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.67,"period":"2026-09-09","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（22.4 → 22.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-09-09","citation":"DD_universe_EPS_estimates_20260909.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.7,"period":"2026-09-09","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（28.45 → 28.65）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-09-09","citation":"DD_universe_EPS_estimates_20260909.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":17.05,"period":"2026-09-09","unit":"USD/share","basis":"Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-09-09","citation":"DD_universe_EPS_estimates_20260909.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":22.55,"period":"2026-09-09","unit":"USD/share","basis":"Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-09-09","citation":"DD_universe_EPS_estimates_20260909.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":28.65,"period":"2026-09-09","unit":"USD/share","basis":"Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-09-09","citation":"DD_universe_EPS_estimates_20260909.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":9.65,"period":"2026-06-04 → 2026-09-09","unit":"%","basis":"FY1 共識 EPS 15.55 → 17.05（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-09-09","citation":"DD_universe_EPS_estimates_20260909.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":30.97,"period":"2026-09-15（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-09-15（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-09-15（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-09-15（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":0.48,"period":"2026-09-15（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-09-15（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-09-15（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-09-15（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":-0.07,"period":"2026-09-15（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝0.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-09-15（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":0.0,"period":"2026-09-15（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-09-15（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":25.41,"period":"2026-09-09","unit":"x","basis":"分母＝FY1 EPS 17.05，分子＝快照價 433.24","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-09-09"}},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"🟡","period":"2026-09-16","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-16","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 413.75 / W52 360.08 / W104 280.01 / W250 176.53 / W250 13週斜率 2.91%"},{"id":"f_ma_w52","label":"52 週均線","value":360.08,"period":"2026-09-16","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-16","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":280.01,"period":"2026-09-16","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-16","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":176.53,"period":"2026-09-16","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-16","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":2.91,"period":"2026-09-16","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-09-16","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"TrendForce 資料顯示 TSMC 全球晶圓代工市佔率在 2026 Q2 攀升至歷史新高 72.5%（Q1 為 72.3%），三星以 5.9% 居次，兩者差距擴大至 12.3 倍；2nm 首季貢獻營收，帶動出貨量與 ASP 同步上升。","source":"techsoda substack, \"Global Market Watch: TSMC's Global Foundry Market Share Inches Up to 72.5%\", https://techsoda.substack.com/p/global-market-watch-tsmcs-global","as_of":"2026-09-10","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"英特爾在川普政府公開表態支持其代工野心後，被視為對三星代工復甦計畫的新威脅；三大廠（台積電、三星、英特爾）皆已進入 2nm 量產階段，先進製程需求量已達台積電可供產能的 110–120%，代表三星與英特爾不需搶下台積電客戶即可受惠，只要能承接台積電產能不足的溢出需求。","source":"Semiwiki, \"TSMC vs Intel Foundry vs Samsung Foundry 2026\", https://semiwiki.com/semiconductor-manufacturers/tsmc/366523-tsmc-vs-intel-foundry-vs-samsung-foundry-2026/","as_of":"2026-06-19","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"華爾街日報於 2026 年 5 月報導，Apple 與 Intel Foundry Services 已達成初步協議，Apple 將以 Intel 18A 製程（電晶體密度與電性可比台積電 2nm 級製程）生產部分 Apple Silicon 晶片，可能結束 Apple 近乎完全依賴台積電代工的局面；Apple 仍自行設計晶片，Intel 僅負責製造。","source":"Investing.com, \"Apple-Intel Chip Manufacturing Deal Reshapes Foundry Race\", https://www.investing.com/analysis/appleintel-chip-manufacturing-deal-reshapes-foundry-race-200682398","as_of":"2026-06-18","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Apple(蘋果，TSM 長期最大單一客戶)正探索讓部分低階處理器改由 TSMC 以外廠商生產，與 Intel、Samsung 進行早期洽談；Intel 18A-P 製程(預計 2026 年底量產)被視為 2016 年 Apple 離開 Samsung 以來第一個理論上可行的替代方案，但分析師認為 Intel 短期內較可能是策略備援或低量次要供應商，而非主力代工廠。","source":"MacRumors, 'Apple May Break a 10-Year Chip Strategy' (引述 Wall Street Journal 報導)","as_of":"2026-02-01","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"0","claim":"Apple 近年持續擴大自研晶片(insourcing)範圍，含 M 系列處理器與自製 C1/C1X 蜂巢數據機，晶片設計團隊擴增至數千工程師；但這是 Apple 把設計從第三方晶片商(如 Qualcomm)收回自研，成品仍需委外晶圓代工，未見明確跡象顯示 Apple 打算自建先進製程晶圓廠取代 TSMC 的代工角色。","source":"CNBC, 'Apple's elevation of silicon head Johny Srouji signals sprint to build in-house chips for all devices'","as_of":"2026-04-21","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"TSMC's ten largest customers accounted for 78% of FY2025 net revenue, up from 76% in FY2024; the single largest customer accounted for roughly 19% of FY2025 revenue (up from 12% in FY2024).","source":"TSMC 2025 Annual Report (20-F) customer concentration disclosure, summarized by StockTitan (https://www.stocktitan.net/sec-filings/TSM/20-f-taiwan-semiconductor-manufacturing-co-ltd-files-annual-report-fo-e7792df70159.html) and ExploreSemis (https://exploresemis.substack.com/p/tsmcs-top-10203040-customers-who)","as_of":"2025-12-31","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Nvidia overtook Apple to become TSMC's largest customer in FY2025 (~19% of revenue, up from 12% in FY2024), while Apple's share fell to ~17% from 22%.","source":"MacRumors, \"Nvidia Overtakes Apple as TSMC's Biggest Customer\" (https://www.macrumors.com/2026/01/28/nvidia-replaces-apple-as-biggest-tsmc-customer/); CNBC (https://www.cnbc.com/2026/01/26/nvidia-set-to-supplant-apple-as-tsmcs-largest-customer.html)","as_of":"2026-01-26","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"S&P Global Ratings upgraded Nvidia's credit rating from 'AA-' to 'AA', citing strong AI-driven growth; this follows an earlier upgrade from 'A+' to 'AA-' on 2024-04-30. TSM's largest customer's credit profile is strengthening, not deteriorating.","source":"S&P Global Ratings, \"Nvidia Corp. Upgraded To 'AA' On Strong AI-Driven...\" (https://www.spglobal.com/ratings/en/regulatory/article/-/view/type/HTML/id/3579353); Yahoo Finance (https://finance.yahoo.com/markets/stocks/articles/p-global-ratings-upgrades-nvidia-211417548.html)","as_of":"2026-06-11","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"TSMC執行長C.C. Wei表示，AI晶片短缺可能持續到2027年及更後期；他指出新建晶圓廠需要2-3年，擴建產能還要再1-2年，沒有捷徑，顯示此為結構性而非短期週期性缺口","source":"TweakTown, 'TSMC can't keep up with AI chip demand, with shortages projected to last beyond 2027' (引用 eetimes.itmedia.co.jp)","as_of":"2026-04-21","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Broadcom警示2026年晶片供應吃緊，TSMC先進封裝(CoWoS)產能為次要瓶頸，2025年底排定的產能擴充恐無法在短期內緩解壓力，分析師建議客戶重新檢視長期供應合約，暗示屬中期結構性問題而非單純週期性","source":"Astute Group, 'Broadcom flags 2026 chip supply squeeze as TSMC capacity tightens under AI demand'","as_of":"2026-03-24","affects":["moat_trend","thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Nvidia約佔TSMC CoWoS先進封裝產能近60%，已鎖定TSMC 2026-2027年CoWoS擴產計畫的一半以上；前三大客戶(Nvidia、Broadcom、AMD)合計控制超過85%產能，3奈米製程為業界最搶手的稀缺資源，三星與Intel在3奈米進度上明顯落後","source":"Sanie Institute, 'The Wafer Allocation Decision No Foundry Customer Can Postpone'","as_of":"2026-01","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"全球晶片投資過去多年集中投向先進製程(3奈米、2奈米、未來1奈米)，成熟製程投資相對不足，但電動車、再生能源、醫療、國防等領域對成熟製程晶片的依賴仍在上升，形成結構性錯配而非單純景氣循環","source":"SemiWiki forum, 'Global semiconductor market faces shortages as AI demand strains supply chains'","as_of":"2026","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#none","axis":"regulatory_antitrust","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美國對特定先進邏輯半導體課徵 25% Section 232 關稅，2026-01-15 生效；同日美台框架協議約定，台灣廠商在美新建產能可豁免此關稅，直接惠及 TSMC 亞利桑那擴廠（12 座廠、1650 億美元投資承諾）。","source":"EY Global Tax News, 'US Section 232 proclamation imposes 25% tariff on certain semiconductors'; Global Policy Watch, 'A Month in Semiconductor Policy'","as_of":"2026-01-15","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"美國商務部核發 TSMC 南京廠一年期年度出口許可（取代 2025-12-31 到期的 VEU 資格），允許美製晶片製造設備持續供應南京廠，免逐案審批；南京廠為成熟製程（16nm 及以上），約占 TSMC 整體營收 2.4%。","source":"CNBC, 'U.S. grants TSMC annual licence to import U.S. chipmaking tools into China'; Benzinga, 'TSMC Secures One-Year US Export License'","as_of":"2026-01-01","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"台灣政府於 2026 年 6 月研議收緊 AI 晶片對中國出口管制，擬將限制範圍從僅涵蓋華為等受制裁對象擴大至所有中國客戶，並首度賦予刑事追訴權；若定案將限縮 TSMC 對中國先進製程客戶的銷售，尚未拍板。","source":"Bloomberg, 'Taiwan Weighs Tighter AI Chip Export Controls Targeting China to Align with US'; UPI, 'Taiwan weighs tighter rules for AI chip exports to China'","as_of":"2026-06-09","affects":["thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"台灣生產全球約92%的最先進邏輯晶片（5奈米以下），台積電先進製程產能高度集中在台灣本島，海外廠（美國亞利桑那、日本、歐洲）尚無法承接同等先進製程規模。","source":"Simply Wall St News, 'Blockade Risk Puts TSMC's Taiwan Hub And Tech Supply Chain In Focus'","as_of":"2026-05-20","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"台積電亞利桑那廠在2027年前是其海外唯一具備先進邏輯製程（5奈米以下）量產能力的據點，海外產能達到有意義規模預計要到2028年以後才會出現，短中期地緣風險仍高度集中於台灣。","source":"Simply Wall St News（彙整報導，同上主題）","as_of":"2026-05-20","affects":["thesis.R","triggers"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"晶片製造耗電量約占台灣全國總發電量18%，台灣本地電力供應若不穩定，可能直接影響在製晶圓批次良率與交期，成為供應鏈單點失效的具體傳導管道之一。","source":"Simply Wall St News, 'Taiwan Semiconductor Puts Global Tech Supply Chains Under Geopolitical Scrutiny'","as_of":"2026-05-20","affects":["thesis.R"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"美、歐、日政府正合計規劃約2000億美元投資以分散半導體供應鏈地理集中度，但進度緩慢，市場評估風險與韌性之間的落差至少要到2028年才會顯著收斂。","source":"Simply Wall St News（彙整報導，同上主題）","as_of":"2026-05-20","affects":["thesis.R","moat_trend"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"TSMC HPC (High Performance Computing) platform grew 20% QoQ in Q2 2026 to reach 66% of total revenue ($40.20B quarterly revenue), driven by AI/cloud accelerator demand.","source":"Investing.com, 'TSMC Q2 2026 slides: AI demand drives record margins, HPC surges 20%'","as_of":"2026-07-17","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"TSMC raised FY2026 revenue growth guidance to 'slightly above 40%' YoY in USD terms (up from prior guidance of 'more than 30%'), and raised 2026 capex target to $60-64B, citing sustained AI accelerator demand and faster advanced-node ramps.","source":"Bloomberg, 'TSMC Hikes Sales, Spending Outlook to Catch AI Megatrend'","as_of":"2026-07-16","affects":["thesis.H","valuation","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"0","claim":"Smartphone platform revenue rose 11% QoQ in Q4 2025 to 32% of quarterly revenue; full-year 2025 smartphone platform revenue grew 11% YoY.","source":"TSMC 4Q2025 earnings management report / transcript (investor.tsmc.com)","as_of":"2026-01-15","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"+","claim":"IoT platform revenue rose 3% QoQ in Q4 2025 to 5% of quarterly revenue; full-year 2025 IoT platform revenue grew 15% YoY.","source":"TSMC 4Q2025 earnings management report / transcript (investor.tsmc.com)","as_of":"2026-01-15","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Automotive chip demand is showing a 2026 recovery across smart cockpit, ADAS, analog IC and display-driver IC segments among Taiwan IC design firms and foundry customers, but near-term recovery pace is being constrained by macro headwinds (tariffs, interest rates, energy costs); long-term automotive semiconductor outlook remains positive.","source":"Digitimes, 'Taiwan chip designers see automotive demand rebound'","as_of":"2026-08-20","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"substitute_technology#none","axis":"substitute_technology","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"台積電首度將部分 CoWoS 先進封裝製程委外給專業封測廠（OSAT，日月光投控、矽品等），因 CoWoS 產能仍追不上 AI 晶片需求缺口；此前 CoWoS 幾乎全數自製，屬供應/生產模式的結構性轉變。","source":"壹蘋新聞網《CoWoS擴產仍追不上需求！台積電歡迎替代方案 OSAT喜迎外溢商機》 https://news.nextapple.com/finance/20260816/9A442EB83257B351C3CEF24B8EC35606","as_of":"2026-08-16","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"2026年CoWoS市場需求估達約100萬片，台積電最多可供應約60至70萬片，缺口延續至2027年底，帶動日月光等OSAT廠承接外溢訂單（含CPO、Fan-out、SiP等技術）。","source":"TechNews 科技新報《台積電 CoWoS 先進封裝擴產仍難滿足市場，OSAT 業者持續受惠外溢訂單》 https://finance.technews.tw/2026/01/29/tsmcs-cowos-advanced-packaging-capacity-expansion-still-falls-short-of-market-demand/","as_of":"2026-01-29","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"台積電正將先進封裝技術從單一 CoWoS 擴展為多技術陣列（2.5D CoWoS、扇出型 InFO、3D SoIC），公司角色從純晶圓代工延伸至封裝平台整合商；CoWoS 產能至2026年底將擴增至月產13萬片規模，訂單已全數售罄至2026年底。","source":"Troy Technical《TSMC CoWoS Advanced Packaging Becomes Critical Bottleneck in AI Chip Supply, Sold Out Through 2026》 https://troy-technical.com/2026/08/09/tsmc-cowos-advanced-packaging-becomes-critical-bottleneck-in-ai-chip-supply-sold-out-through-2026/","as_of":"2026-08-09","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"18 位分析師對 TSM 的共識目標價為 $554.45，較當時股價 $433.24 有約 28% 上檔空間；另一來源（20 位分析師，S&P Global 彙整）平均目標價 $552.38，評等 Strong Buy；目標價區間最低 $440、最高 $700","source":"stockanalysis.com/stocks/tsm/forecast","as_of":"2026-09-15","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"TSMC 在 2026 Q2 法說會（2026-07-17）將 2026 年美元營收成長 guidance 從先前「30% 以上」上調至「略高於 40%」，高於市場先前 35% 的共識預估","source":"Yahoo Finance - TSMC Targets 40%+ Sales Growth, Lifts 2026 Capex to $64 Billion","as_of":"2026-07-17","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"同場法說會 TSMC 將 2026 年資本支出指引由先前預測上修至 $60-64 billion 區間，較先前預測增加至少 $4 billion","source":"Yahoo Finance - TSMC Targets 40%+ Sales Growth, Lifts 2026 Capex to $64 Billion","as_of":"2026-07-17","affects":["thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026 Q1 法說會（2026-04-16 前後）TSMC 首次上修 2026 全年營收成長 guidance，優於先前預期，帶動當季淨利年增 77.4%、優於 NT$632.6 billion 的分析師預估","source":"Bloomberg - TSMC Raises 2026 Outlook in Sign of Confidence in AI Demand","as_of":"2026-04-16","affects":["thesis.H"],"status":"ok"},{"id":"major_events#none","axis":"major_events","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"ma_merger#none","axis":"ma_merger","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"lawsuit_class_action#none","axis":"lawsuit_class_action","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 8 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"TSM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.23,"operating_margin_pct":56.1,"fcf_margin_pct":25.33,"rd_intensity_pct":6.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AMD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.2,"operating_margin_pct":15.71,"fcf_margin_pct":20.34,"rd_intensity_pct":22.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"MU","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.57,"operating_margin_pct":65.67,"fcf_margin_pct":28.99,"rd_intensity_pct":5.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU","as_of":"TTM ending 2026-05-31（4季加總）"}}],"subject":"TSM"}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/TSM/TSM_Q2_2026_Earnings_Call_20260716.md）

# Q2 2026 Earnings Call
2026-07-16

Q2 2026 Earnings Call
Taiwan Semiconductor Manufacturing Company Limited | Earnings Calls | 2026-07-16
Jeff Su (Executives)
Good afternoon, everyone. And welcome to TSMC's Second Quarter 2026 Earnings Conference and
Conference Call. This is Jeff Su, TSMC's Director of Investor Relations and your host for today.
Today's event is being webcast live through TSMC's website at www.tsmc.com, where you can also
download the earnings release materials. [Operator Instructions]
The format for today's event will be as follows: First, TSMC's Senior Vice President and CFO, Mr.
Wendell Huang, will summarize our operations in the second quarter 2026, followed by our guidance
for the third quarter 2026. Afterwards, Mr. Huang and TSMC's Chairman and CEO, Dr. C.C. Wei, will
jointly provide the company's key messages. Then we will open both the floor and the line for the
question-and-answer session.
As usual, I'd like to remind everybody that today's discussions may contain forward-looking statements
that are subject to significant risks and uncertainties, which could cause actual results to differ
materially from those contained in the forward-looking statements. Please refer to the safe harbor
notice that appears in our press release.
And now I would like to turn the microphone over to TSMC's CFO, Mr. Wendell Huang, for the
summary of operations and the current quarter guidance.
Jen-Chau Huang (Executives)
Thank you, Jeff. Good afternoon, everyone. Thank you for joining us today. My presentation will start
with financial highlights for the second quarter of 2026. After that, I will provide the guidance for the
third quarter of 2026.
Now let's move on to revenue by technology. 2-nanometer process technology contributed 3% of wafer
revenue in the second quarter; 3-nanometer, 5-nanometer and 7-nanometer accounted for 30%, 33%
and 11%, respectively; advanced technology, defined as 7-nanometer and below, accounted for 77% of
wafer revenue.
Moving on to revenue contribution by platform. HPC increased 20% quarter-over-quarter to account
for 66% of our second quarter revenue. Smartphone decreased 4% to account for 22%. IoT increased
4% to account for 5%. Automotive increased 15% to account for 4%. DCE increased 5% to account for
1%.
Moving on to the balance sheet. We ended the second quarter with cash and marketable securities of
TWD 3.5 trillion or USD 110 billion. On the liability side, current liabilities increased by TWD 144
billion quarter-over-quarter, mainly due to the increase of TWD 58 billion in accounts payable and the
increase of TWD 48 billion in accrued liabilities and others.
In terms of financial ratios, accounts receivable days increased by 3 days to 29 days. Inventory days
increased 7 days to 87 days, primarily due to the ramp of N2 technology.
Regarding cash flow and CapEx. During the second quarter, we generated about TWD 783 billion in
cash from operations, spent TWD 496 billion in CapEx and distributed TWD 156 billion for third

quarter 2025 cash dividend. Overall, our cash balance increased TWD 99 billion to TWD 3.1 trillion at
the end of the quarter.
In U.S. dollar terms, our second quarter capital expenditures totaled USD 15.7 billion.
I finished my financial summary. Now let me -- let's turn to the current quarter guidance. Based on the
current business outlook, we expect our third quarter revenue to be between USD 44.6 billion and USD
45.8 billion, which represents a 12% sequential increase or a 37% year-over-year increase at the
midpoint.
Based on the exchange rate assumption of USD 1 to TWD 32, gross margin is expected to be between
65% and 67%, operating margin between 56% and 58%. This concludes my financial presentation.
Now let me turn to our key messages. I will start by talking about our second quarter '26 and third
quarter '26 profitability. Compared to the first quarter, our second quarter gross margin increased by
150 basis points sequentially to 67.7%, slightly ahead of our guidance, primarily due to cost
improvement efforts and a slightly higher overall capacity utilization rate, partially offset by dilution
from our overseas fabs.
We have just guided our third quarter gross margin to decrease by 1.7 percentage points to 66% at the
midpoint, primarily as we expect the steep ramp-up of our 2-nanometer technology to dilute our gross
margin by about 3 to 4 percentage points. This dilution is expected to be partially offset by very strong
demand for our leading-edge technologies and continued cost improvement efforts, including
productivity gains and across node capacity optimization.
Looking at the second half of the year, given the 6 factors that determine our profitability, there are a
few puts and takes that I would like to share.
First, we expect the steep ramp-up of our 2-nanometer to dilute our gross margin by about 3 to 4
percentage points in the second half of the year. Furthermore, as the scale of our overseas expansion
grows, we continue to forecast the gross margin dilution from the ramp-up of overseas fabs in the next
several years to be 2% to 3% in the early stages and widen to 3% to 4% in the latter stages.
On the other hand, demand for our leading-edge technologies is very strong. In addition, we continue
to leverage our manufacturing excellence to generate more wafer output and drive greater across node
capacity optimization in our fab operations to support our profitability.
Finally, we have no control over the foreign exchange rate, but that may be another factor.
Next, let me talk about our 2026 capital budget. At TSMC, a higher level of capital expenditures is
always correlated to higher growth opportunities in the following years. With our strong technology
leadership and differentiation, we are well positioned to capture the multiyear structural demand from
the industry megatrends of 5G, AI, and HPC.
Given the continued strong structural demand from our customers, including the newly emerging
Agentic AI market, we have decided to raise our full year 2026 capital budget to be between USD 60
billion and USD 64 billion as we continue to invest heavily to support our customers' growth. We
always collaborate closely with the tool suppliers well in advance to prepare the capacity, whether it is a
strong up cycle or down cycle, just like our customers collaborate with us well in advance to plan our
capacity. Thus, we do not foresee any bottlenecks to our capacity expansion plans.
About 70% to 80% of the 2026 capital budget will be allocated for advanced process technologies.
About 10% will be spent for specialty technologies and about 10% to 20% will be spent for advanced

packaging, testing, mask-making and others.
Even as we invest for the future growth with this level of CapEx spending in 2026, we remain
committed to delivering profitable growth to our shareholders. We also remain committed to a
sustainable and steadily increased cash dividend per share on both an annual and quarterly basis.
In 2025, we paid TWD 467 billion in cash dividends, up 28.6% year-over-year as TSMC shareholders
received a total of TWD 18 cash dividend per share. In 2026, they will receive TWD 24 per share, up
another 33% year-over-year, and we expect a continued and increasing cash dividends per share in
2027 as well.
Now let me turn the microphone over to C.C.
C.C. Wei (Executives)
Thank you, Wendell. Good afternoon, everyone. First, let me start with our near-term demand outlook.
We concluded our second quarter with revenue of USD 40.2 billion at the high end of our guidance in
U.S. dollar terms driven by strong demand for our leading-edge process technologies.
Moving into third quarter, we expect our business to be supported by continued strong demand for our
leading-edge process technologies, including the steep ramp of our 2-nanometer technology.
Looking ahead, we observe consumer and price-sensitive end market segments are being challenged
due to the impact of rising component prices and macroeconomic uncertainties. As such, we are being
prudent in our business planning while focusing on our fundamentals of our business to further
strengthen our competitive position.
Having said that, AI-related demand continues to be extremely robust. The AI megatrend continues to
drive the need for more and more computation, which supports the robust demand for leading-edge
silicon. Our customers and customers' customers, who are mainly the cloud service providers, continue
to provide us with a very strong signal and positive outlook. Thus, our conviction in the multi-year AI
megatrend remains very high. Supported by our robust technology differentiation and the broad
customer base, we now expect our full year 2026 revenue growth to be slightly above 40% year-over-
year in U.S. dollar terms.
Now let me talk about the acceleration of Agentic AI. The AI market continues to be very dynamic. The
emergence of Agentic AI is leading to a resurgence in the role of CPUs in AI data centers, which drives
more silicon demand in addition to AI accelerators. We believe this is positive for TSMC as no matter
what CPU approach is taken, whether it's x86, ARM-based, or RISC-V architecture, they are almost all
TSMC's customers. We are already collaborating closely with our CPU customers and working to
support them with the most advanced technologies and necessary capacity, so they can capture the
Agentic AI market opportunities.
Next, let me talk about TSMC's capacity expansion strategies. To address the structural increase in
overall long-term semiconductor market demand profile, TSMC collaborates closely with our
customers and our customers' customers to plan our capacity.
Given the fundamental complexity of leading-edge technologies and the design-in and lead time
involved, we also have a very good idea of their multiyear product road map and production plans. This
is important because it takes more than 5 years to develop the technology and product, prepare the
capacity, and ramp it up to high-volume production.

Internally, TSMC employs a disciplined capacity planning system to assess the market demand from
both a top-down and bottom-up approach. This is a continuous and ongoing process. Based on our
assessment, we are stepping up our CapEx investment to increase our capacity, to support our
customers' future growth.
Now with a strong collaboration and support from our leading U.S. customers and the U.S. federal state
and city governments, we would like to announce an additional USD 100 billion investment in Arizona.
This is to build several more semiconductor logical wafer fab for 2-nanometer and below technologies
as well as advanced packaging fabs to support the strong multiyear demand from our leading U.S.
customers.
We believe this investment will help to further foster the development of the U.S. semiconductor
ecosystem, strengthen the supply chain, and support an increasing number of high-tech, high-paying
jobs in the United States. At the same time, we are building 13 leading-edge and advanced packaging
fab in Taiwan over the next several years, and we will continue to further invest in Taiwan.
Therefore, TSMC's semiconductor technology and manufacturing work continue to play a pivotal role
in supporting the global semiconductor industry while unleashing our customers' innovation.
Now let me talk about the current N3 capacity expansion. We are executing well on our global plan to
add 3 additional 3-nanometer fabs, one in Taiwan, one in Arizona, and one in Japan to support the
robust multiyear pipeline of demand for 3-nanometer technologies.
In addition to all the new fabs, we continue to convert 5-nanometer tools to support 3-nanometer
capacity in Taiwan. We are also leveraging our manufacturing excellence to drive greater productivity
across our fab in all locations to generate more wafer output. We are also focusing on capacity
optimization across node, which including flexible capacity support among N7, N5 and N3 nodes.
In summary, we are using multiple levers to do everything we can, wherever we can, however we can to
maximize the support to all our customers.
Now let me talk about our mature node strategies. TSMC's strategy at mature node has not changed.
Our first priority is to fully support our customers. And now we continue to increase, not decrease our
mature node capacity in the higher value-added segment. For example, we are increasing our mature
node capacity through JASM Fab 1 in Japan for CMOS image sensor application and ESMC in Germany
for automotive and industrial applications.
In today's market, outside of specific areas such as power management IC and CMOS image sensor, the
mature node demand in other commodity area is not that strong. Thus TSMC will continue to focus on
the higher value-added and strategic segment by ensuring we have a necessary capacity to support our
customers' growth.
Finally, let me talk about our A14 status. As I mentioned a few minutes ago, the complexity of leading-
edge technology continue to increase. The lead time to develop a new technology such as A14, building
the capacity, and then ramping it up now takes 5 to 7 years. There are no shortcuts.
Our A14 technology representing the second generation of nanosheet transistors and deliver another
full node stride from N2 with performance and power benefit to address the incessant need for high-
performance and energy-efficient computing.
Compared with N2, A14 will provide 10 to 15 speed improvement at the same power or 25 to 30 power
improvement at the same speed and close to 20% chip density gain. A14 technology development is on

track and progressing well.
Internal product-like vehicle demonstrated close to 90% device performance and close to 90% 256
megabits SRAM yield. We are observing a strong level of customer interest and engagement from both
smartphone and HPC AI applications and customer now tape-out activity is ongoing and ahead of
schedule. Pre-production will start in 2027 and volume production is scheduled for 2028.
With our strategy of continuous enhancement, we also introduced A13 and A12 as extension of the A14
family. A13 represents a further advancement of A14, achieving an over 6% die area saving through an
innovative 97% optical shrink. Through continuous design technology co-optimization, A13 also drive
further performance and power efficiency improvement. A13 design rule are backward compatible with
A14 to ensure smooth IP migration.
We also introduced A12, which will bring our innovative superpower rail technology to the A14
platform for superior performance, power, and area benefit. Both A13 and A12 are scheduled for
volume production in 2029. We believe A14 and its derivative technologies will propel our A14 family to
be an even larger and long-lasting node for TSMC than N2. Just like 2-nanometer technology is a larger
and longer-lasting node than 3-nanometer, and here further extend our technology leadership position
well into the future.
This concludes our key messages, and thank you for your attention.
Jeff Su (Executives)
Thank you, C.C. So this does conclude our prepared statements. [Operator Instructions] Please note
that we will conclude today's meeting at around 3:10 or so. So we will try to get in as many participants
your questions as possible. But if we're not able to, we do apologize in advance, and thank you,
everyone, for your patience.
So operator, well, let's begin the Q&A session. We'll take the first 2 questions from the floor, and then
we'll go online. Maybe again, left, center, right. Maybe we'll take the first question, Sunny Lin from
UBS, please.
Sunny Lin (Analysts)
Congrats on the very strong performance and outlook. So number one, I want to double-click on the
CapEx. So, very encouraging CapEx outlook. And I do think it's essential that TSMC showcase a
stronger determination in capacity expansion, given the stronger demand and the very tight supply.
And so beyond 2026, I think every large client also wonder how aggressive TSMC is planning for
CapEx. And so back in the COVID super cycle, TSMC did provide a 3-year CapEx outlook back then.
And so I wonder, at this point, will it be possible for you to share any color, maybe for the coming 3
years CapEx? Thank you.
Jeff Su (Executives)
Okay. So Sunny's first question is regarding CapEx. She does believe it's important, essential to show
our determination to support our customers with these large CapEx investments. So she wants to know,
do we have a 3-year CapEx guidance '26, '27, '28, similar to what we did back in 2021?
Jen-Chau Huang (Executives)

Okay. Sunny, we do not have a number to share with you. But as you know, we invest CapEx this year
for the future business opportunity. And as long as there are business opportunities, we will not
hesitate to invest. As you can hear from our prepared remarks that we -- our conviction in the
megatrend, AI megatrend multiyear is very strong, and we are stepping up the CapEx, including
increasing this year's CapEx. Last time, we said our CapEx in the next 3 years will be significantly
higher than the CapEx in the past 3 years. Now is the -- the CapEx in the next 3 years will be even more
significantly higher than the past 3 years.
Sunny Lin (Analysts)
Yes. Sorry, maybe let me follow up on CapEx from another...
Jeff Su (Executives)
Second question.
Sunny Lin (Analysts)
Yes, sure. So you just announced additional $100 billion CapEx in the U.S., and I think that's pretty
important for you to secure the business in the U.S. as well. And so now with total $265 billion CapEx
in Arizona, what's your current plan to bring on the capacities in Arizona in the coming few years?
Jeff Su (Executives)
Okay. So Sunny's second question is on to, C.C. said, investing additional $100 billion in Arizona based
on the strong demand from our customers. So the total investment now is $265 billion. What is the
schedule time frame or the plan for this investment? Is that correct, Sunny? Yes. Okay.
C.C. Wei (Executives)
Sunny, the schedule will depend on the market situation. You know that. So today's situation, the
megatrend is so strong so that we announced additional $100 billion investment in Arizona. How many
fabs? Many. So actually, let me say that, say probably, additional 4 more fabs will be built.
Sunny Lin (Analysts)
And that's combining front- and back-end?
C.C. Wei (Executives)
Yes.
Jeff Su (Executives)
Okay. Thank you. Let's go to the middle. We have Charlie Chan from Morgan Stanley. We'll go left,
middle, right from where I sit.
Charlie Chan (Analysts)
So first of all, congrats for a very strong outlook. My first question is really about the foundry
competition. I understand that there's no shortcut for a newcomer like TerraFab, but how about like
Samsung Foundry, right? They got a huge profit from memory business. Intel got a U.S. policy support.
So I'm not sure how TSMC is going to address those competition, because apparently, several U.S.

companies are engaging with those industry peers. And recently, actually yesterday, ASML just
announced to expand the EUV capacity for 2028. Would TSMC worry that your competitors to take
more slots and build a large capacity in the future to compete with you in the leading-edge business?
Jeff Su (Executives)
Okay. So Charlie's question is competition from 2 angles. One, he does note, C.C. said foundry
competition, no shortcuts, but he says according to the news, many of our customers are engaging with
our foundry competitors. One of them in Korea is making huge amounts of money these days. Another
one may have the U.S. government policy support. So the first part of his question, how do we see the
competition and threat of customers moving to our competitors, number one.
C.C. Wei (Executives)
Well, let me say that. Yes, one of my competitors in South Korea, they make a huge amount of money,
and I'm jealousy about it. And then the other one in the U.S., they got a very strong U.S. government
support. We also got the government support, by the way, although we don't announce it.
However, let me share with you, as we said, there is no shortcut. What does that mean? Meaning that in
the semiconductor industry, you have to go back to fundamental. Government's help is welcome.
Really, we also appreciate that. A lot of money, of course, that's nice to have.
But the most important thing as we continue to say is the technology, manufacturing, and customer
trust. These 3 fundamental never change. For my 30-some years, 40 years career, it's always the most
important thing. And that's always the TSMC's secret recipe to win the business.
So from my -- from the competition point of view, choosing a technology, ramping it up is not buying a
milk from 7-Eleven. Well, I'm using that -- I'm quoting the sentence for my customer, anyway. It says
that you're choosing a kind of a technology partner, it is no shortcut. You need to understand the
technology. You need to really utilize it using the test chip, and then something, and work together, and
then prepare the capacity and ramp it up. That's why I would say, it takes about 5 years. It's not that
today, you think this milk is better, you go to the next store, it's a 7-Eleven. You don't like it, you go to
another store. No. So that's my answer, Charlie, is it's -- agree?
Charlie Chan (Analysts)
Yes. So I hope you can buy more milk, so other people can get it. Yes. So let me switch gears to a more
exciting side. C.C. just said you see a very strong signals from customers, customers' customers. You
also revised up the full year revenue guide. Are you ready to revise up the 5-year revenue CAGR,
especially this AI semi CAGR? I remember it was like high 50%. But here comes the question, right,
that Agentic AI demand is so strong, CPU is a great opportunity for TSMC. But how about those kind of
memory cost increase, right? It's kind of a big chunk of this kind of AI CapEx. So, what's the update of
the AI semi CAGR? And how should we look at the contents of this AI semi related to TSMC's growth?
Jeff Su (Executives)
Okay. So Charlie's second question is regarding the AI-related demand. We do continue to see very
strong and positive signals from our customers, customers' customers. We revised up our full year. So
his question is around our AI CAGR guidance that we gave in January on a 5-year period, mid- to high-

50s CAGR growth. He's wondering if there's any update to that. Agentic AI, a new opportunity, what is
our definition of AI accelerator? Do we include that? And what is the CAGR?
C.C. Wei (Executives)
Charlie, if you read our message that we continue to invest more. We increased the CapEx with a good
reason. So if you're asking about the AI's CAGR, let me give you not a number, but it's stronger and
stronger and stronger. So we don't give you the number today because it continue to increase. So we
don't know how to answer this question, but stronger than what we said before.
Jeff Su (Executives)
Thank you, Charlie. All right. Let's move to this side. Maybe we'll take the question from Arthur from
Macquarie.
Yu Jang Lai (Analysts)
First, congrats on the strong execution and performance. My question is regarding the new advanced
packaging technology. We noticed that especially the EMIB-T is gaining traction. So how will TSMC
react this request?
Jeff Su (Executives)
Okay. Sorry. So Arthur's first question is on advanced packaging and competition. I guess, very simply
put, EMIB-T, in his view, is gaining traction. So how do we see the competitive threat from this?
C.C. Wei (Executives)
Well, let me say that, our packaging capacity is so tight that now it's limited by customers' growth. So
we welcome that additional flexibility in the market. And so that will help TSMC's front-end wafer
business growth, which is a majority part of TSMC's business. The technology looks good, according to
the newspaper. And we hope they will be successful and so that share some of the loading from TSMC.
Today, we're working very hard to shorten the gap between the demand and the capacity. And so as I
said, we welcome to have this additional alternatives, and so the flexibility for my customer.
Yu Jang Lai (Analysts)
That makes a lot of sense. So a follow-up. So as this is a new technology, right? So if your clients, they
ask your support, and our value is support our customers' success, right, how TSMC will handle this
special request?
Jeff Su (Executives)
Sorry, your question is...
Yu Jang Lai (Analysts)
So if these technologies have some small problem, and then ask our company to support. So how our
company accommodate it?
Jeff Su (Executives)

So Arthur's question is, if there is some issues with this technology, do we have a -- are we -- I don't
know how to say it. Is there an alternative plan?
C.C. Wei (Executives)
Let me answer the question. Our #1 is to support our customers' success. So whatever that we can hear
about our customers' business, we want to win. Does that answer your question?
Yu Jang Lai (Analysts)
Okay.
Jeff Su (Executives)
Let's come back. We'll take one more here, and then we'll go online and then back to the room. Gokul?
Gokul Hariharan (Analysts)
First question on, maybe since you are not wanting to give a longer-term numerical guidance, could you
talk a little bit about the philosophy of how you are expanding capacity? Obviously, customer feedback,
customers' customers feedback is important. Do you also consider competitive pressure? Because as an
outright market leader, having like undersupply for a very long period of time is not really desirable for
TSMC, right? You probably want a market which is more balanced. So when you think about your
capacity expansion, like how long do you think it takes to fulfill the demand as you see right now?
That's one.
And second, chips, obviously, is the current shortage. But there is also a lot of discussion about data
center delay, power capacity being available. So could you also share some thoughts on how you are
layering in that kind of concerns because you don't want your chips to be available, but having to wait
for the data center deployment to happen. So just to understand how that goes into your planning
framework as well.
Jeff Su (Executives)
Yes. Thank you. So Gokul's first question is, again, how do we plan our capacity and determine the
capacity expansion plan. Certainly, we take into consideration the demand, multiyear demand from our
customers and customers' customers. But do we also consider the competitive pressures from
competitors building capacity? Is that part of our calculus to expand the capacity, one? And then also,
what about things outside of chips like data center delays or power, these type of deals?
C.C. Wei (Executives)
Gokul, that's a good question. Definitely, every time when we think about the business, we consider the
competition. That's number one. And then, we look at where we are. And then we decide a bottom-up
and then top-down's assessment of those demand. Those are the typical thing, I mean, in our daily life.
So we make a lot of judgment and then we'd be more careful. We talk to customers and customers'
customer. Those are the CSPs. And then, we get all their input for the demand. And then we make a
judgment.
Now remember that I believe every customer tell me the truth, everyone. You put all the truths
together, it's not the truth. So we have to make some of the judgment. You know what I mean, since you

are laughing. Because all the customers are very aggressive, right? That's the CEO's job. CEO got to be
aggressive.
So they give me the number of their demand, and I believe they try their best to tell me the truth. So I
put all together, all the truths together is not a truth. Mark down that word.
So yes, we do a very careful judgment. May not be correct, may not be correct, but we did carefully and
because this is a big money, right? This year, we say we increased the CapEx from $52 billion to $56
billion, now $60 billion to $64 billion. And you bet, that will continue to increase. It's a big money. So
we do it carefully.
So we did all the assessment and that lead to your second question. Are we sure that we deliver the
chips to our customer, and they were not put into inventory? So we -- actually, we are checking the AI
data centers progress, the building, the location, the demand, the racks, we're checking all that to make
sure that TSMC chips will not be put in inventory. That answer your question?
Gokul Hariharan (Analysts)
Yes, that's clear. So C.C., so do you -- you still believe even end of next year, we are still going to be
running short of supply even with this elevated capacity build-out plans?
C.C. Wei (Executives)
You want me to give you a guarantee, right? Let me say that, I believe from this day on all the way to
probably 2029, 2030, the demand is very strong. Whether in between there's a dip or not, I'm not very
sure. But the trend is so robust that I believe we are witnessing a kind of a new industry. I would like to
say the new industry called AI industry, which is so common in our daily life because it's going to affect
our automotive, affect the humanoids, robot, and also impact to all the industry. So by the amount of
money we put in, I mean, including all the CSPs, this alone is a very important new industry to the
world. And so the demand will be there. And the fundamental thing is semiconductor chips, and most
of them in TSMC.
Gokul Hariharan (Analysts)
My second question is on your profitability. So C.C., you joke that you are definitely jealous of your
memory competitor on their margins. But it definitely feels like profitability-wise, longer-term foundry,
especially leading-edge foundry should be higher than memory, looking at number of competitors out
there. So as you are investing for a lot of your customers, how is that discussion going? Because you are
no longer the most profitable semiconductor manufacturing company at this point in time. So you
probably have less pressure in terms of passing on your value and capturing your value right now
compared to maybe 1 year back.
Jeff Su (Executives)
Okay. So Gokul's second question is on profitability and pricing to a certain extent. Of course, some of
the memory makers are making very good profitability and margins today, but he notes the role of
foundry could be even more value in TSMC's role as well. So what should be the right way to think
about the long-term profitability for your foundry? Should it be better? And then I guess, really pricing
into this, what type of pricing approach do we want to take?

C.C. Wei (Executives)
Yes, Gokul, your question actually is simple. What is the wafer pricing strategy for TSMC, and what
kind of gross margin we should have?
The higher, the better, of course. But we are a partner, a partner meaning that I said many times, our
customers got to be successful. I don't want to squeeze them out from the market. And besides, we are a
very trustable company with our customers. So we don't suddenly increase our price by, which I like to
have, 4x or 5x. You cannot survive for that kind of -- for your customer to survive for that kind of a price
increase.
So we earn our value, and we make sure that our profit, our gross margin is enough for our long-term
sustaining expansion. That's to the benefit of my customer and TSMC also. That's our philosophy. So
yes, I'm really jealous about the memory companies, 86% gross margin. 86%? About 68%, I would be
happy about that. But all right. Anyway, so I answered the question. We are very trustable.
Jeff Su (Executives)
Thank you. Operator, can we take the next 2 questions from participants on the line, please?
Operator (Operator)
Yes. Now it's James Fontanelli from Arete.
Jim Fontanelli (Analysts)
Yes. Could I ask about the risk that you see around customer concentration, as AI demand continues to
significantly outgrow other end markets? I think your exposure to your top 5 customers is becoming
meaningfully larger than at any point in your history. So I'd just like to understand how you see that
risk.
Jeff Su (Executives)
Okay. So Jim's first question is risk around customer concentration. We have large customers that are
getting larger. Are we worried that we have too many big customers or the customer concentration?
C.C. Wei (Executives)
No, that's not our concern. Besides what you say the customers are growing bigger and bigger, we are
very happy about it. And some of the customers also growing very fast. So it's not -- Jim, it's not what
you said that the bigger customer is growing bigger and bigger. No. I mean that's -- there's a lot of new
player in the AI industry.
Jeff Su (Executives)
Do you have a second question?
Jim Fontanelli (Analysts)
Yes. So we're seeing your direct customers put capital into both financing, investing and investing in AI
demand. Is that something that TSMC is considering?
Jeff Su (Executives)

So Jim's second question, he knows some of our customers are helping to invest in their customers.
Jim, if I understand you right correctly, you're asking if TSMC, if this is an approach we would take to
invest in our customers. Is that correct? Or financing and investing?
Jim Fontanelli (Analysts)
Yes, in the end-to-end customers, not your direct customers.
Jeff Su (Executives)
Right. So in customers' customers as well.
C.C. Wei (Executives)
To answer, Jim, to answer your question directly, every company has a different consideration and
every company has a different strategy. So far, no, TSMC don't do this kind of financial arrangement
because of, we think we are working with current customer with the current model smoothly and also
successfully.
Jeff Su (Executives)
Okay. Thank you, operator. Can we move on to the next participant on the line, then we'll come back to
the floor.
Operator (Operator)
Next one to ask question, Mehdi Hosseini from SFG.
Mehdi Hosseini (Analysts)
Two, from my end. I want to go back to the $100 billion investment in U.S. Is there any way you can
give us some time line? Is it over the next 3 years, 5 years? How should we think about the progression
of this $100 billion investment in the U.S.? And I have a follow-up.
Jeff Su (Executives)
So Mehdi's first question is around the announcement today, additional $100 billion investment in the
U.S. In terms of the CapEx time frame, is it in the next 3 years, in the 5 years? Do you have any
schedule or time frame to share about this additional $100 billion?
C.C. Wei (Executives)
We do have a plan, but let me share with you actually the progress or the schedule. Most of the time, it
depends on the market situation and our customers' demand. So if you ask me to give you a firm
schedule, no, we don't have it today. But we do have a plan. And we speed it up. We try to speed it up as
fast as possible.
Mehdi Hosseini (Analysts)
So the message is, you're flexible, but also you're expediting the investment in U.S. Is that correct?
Jeff Su (Executives)

So -- well, I think C.C. said we're trying to move as fast as we can, but everything is based on our
customer needs.
C.C. Wei (Executives)
Yes. We're also moving the new fabs and the facilities in Taiwan as fast as possible. And the same thing,
we try to bring up a new fab in the Japan as fast as possible. Because of the situation today is the
demand and the supply, the gap is so big. So we are working very hard to narrow the gap.
Jeff Su (Executives)
Do you have?
Mehdi Hosseini (Analysts)
I want to as a follow-up. Actually, I want to dive into the compute part of HPC. And I want to ask you
about networking switches. And in that context, when should we expect the COUPE platform to have a
material contribution to your top line?
Jeff Su (Executives)
So Mehdi's second question, very specific. He wants to know for our COUPE platform, when will it have
a very meaningful contribution to the business?
C.C. Wei (Executives)
We start the production right now, and it will be ramped up. As time goes by, I think the AI data center
need to lower down the power consumption and increase the bandwidth of the communication
channel. So I believe the COUPE will continue to increase the demand, and then will become a fairly
important technology in the next few years.
Jeff Su (Executives)
Okay. Thank you. Let's come back to the floor. We'll take the next question from Citibank, Laura Chen.
Chia Yi Chen (Analysts)
And my first question is also about a very promising outlook as TSMC raised the CapEx and also the
growth outlook for this year. And particularly, I think C.C., you mentioned about the Agentic AI and the
CPU growth potential. But can you give us more update among that AI, different kind of chips between
GPU, accelerators or CPU? What you see the growth potential and your visibility?
Jeff Su (Executives)
So Laura's first question is around sort of the outlook. We obviously raised the CapEx and growth
outlook for this year. She wants to know within the AI, the outlook for Agentic AI and CPUs versus AI
accelerators, GPUs, et cetera. How do we see these segments?
C.C. Wei (Executives)
Laura, I don't think I can give you a very specific number. But let me share with you. All of them are in
TSMC. And they're also using the same kind of leading-edge technologies. We're working with our
customers to allocate the wafer, the supply to balance the CPU, GPU, XPUs ratio, okay?

Chia Yi Chen (Analysts)
Okay. That's -- yes, that makes sense. And then my second question is also about the advanced
packaging. We know that during the symposium, TSMC previously already announced a 14x reticle
CoWoS road map to enable larger AI packaging. But at the same time, we also noted that TSMC, maybe
last month in Japan, you showed the substrate development for CoWoS to enable some of the glass
technology. So I'm just wondering if you can give us more like technologies progress update on the
different kind of technology for glass core or glass substrates or glass carrier. What's the progress at
TSMC right now?
Jeff Su (Executives)
So Laura's second question is on advanced packaging. She notes, as we said, we road map to even larger
than 14x reticle size with CoWoS. But she also wants to know the technology process in newer areas like
glass substrates, glass cores, what is the progress and status?
C.C. Wei (Executives)
We are -- let me say that. Today, the majority is still CoWoS, right? And we are developing that
alternative to try to lower down the cost. And we also work with substrate vendor so that our customer
can have their product be in the market. The progress, we're building a pilot line that I announced a few
quarters ago. And it takes about another 1 year to be mature, so we can put it into the production with
our customer. Okay.
Jeff Su (Executives)
Thank you. Let's move to this side of the room. Bank of America, Haas Liu.
Haas Liu (Analysts)
And congrats on the great results. My first question is regarding your CapEx and sales. You gave pretty
solid CapEx outlook for this year and also said the CapEx outlook in the next couple of years will
continue to be pretty significant. And you also raised this year at 40% plus. So would you be able to
provide your next couple of years' sales growth outlook, try to quantify it?
And relatedly, I think also on that topic is whether you can just try to break down which part of the
demand you are seeing as the key driver for you to raise your CapEx and also for this year's demand? Is
it still mostly driven by cloud computing or it is proliferating to edge computing? Or to some extent, is
it also related to your equipment supply chain is raising their price as well?
Jeff Su (Executives)
Okay. That's several questions in one. So I'm going to take that as 1.5 questions at least. But basically,
Haas is asking, with the CapEx increase and the revenue increase this year, I think he's trying to look at
intensity, but he wants to know what about the revenue guidance for the next several years. Yes, I'll stop
there for now.
C.C. Wei (Executives)
Okay. Let me answer that question. Because of the revenue corresponding to our investment, right,
because we know we forecast our demand, and then we make an assessment, and then we do the
CapEx. Next few years is going to be a very good business for TSMC. That's all I can say.

Jeff Su (Executives)
And then the other part, so what's the key driver? Is it cloud AI? Is it edge AI? Is it cloud vendors are
increasing the price?
C.C. Wei (Executives)
It's all AI related, everything.
Haas Liu (Analysts)
Okay. Yes.
Jeff Su (Executives)
Do you have a quick follow-up?
Haas Liu (Analysts)
Yes. I think it is more on your long-term strategy because a lot of people have actually been asking
about your CapEx and also competition on the front-end. But I would actually say that if on the back-
end competition is rising, especially coming from Intel EMIB-T, are you worried that your value add for
your overall foundry business across front-end manufacturing to the back-end packaging business, the
value add could actually be cannibalized with growing competition?
Jeff Su (Executives)
Okay. So Haas's second question is around the competition in advanced packaging. If our competitors
are able to gain traction or business with things like EMIB-T, would that be the gateway or an entry way
into more competitive threat on the front-end logic wafer side? So does advanced packaging lead to
front-end wafer?
C.C. Wei (Executives)
Haas, let me answer that. The front-end's wafer business and the back-end's business are 2 different
things, right? If they are the same, then you can expect ASE become the front-end competitor also. It's
2 different things. And I also say that since our capacity in the back-end is so in shortage mode, the gap
is bigger. And so, I welcome that the competitor offers some of the flexibility to my customer so that
their front-end wafer can be put into the package, and that help TSMC's front-end wafer business.
That's our attitude.
Jeff Su (Executives)
Operator, let's take one more from the online, and then we'll wrap up with back in person.
Operator (Operator)
Next one to ask question, Robert Sanders from Deutsche Bank.
Robert Sanders (Analysts)
You recently stated that High-NA tools are too expensive. But could you please discuss how your
customers are considering the impact of die stitching challenges from a smaller field size with High-NA.

Could that actually slow the adoption of High-NA even if the tech improves or the tech gets more
productive? And I have a follow-up.
Jeff Su (Executives)
Well, Rob's first question is a very specific technology around High-NA adoption. He wants to know the
customers' feedback on the challenges with die stitching. Is this an impediment or barrier to High-NA
adoption in our view?
C.C. Wei (Executives)
You got a very detailed understanding of the High-NA. Today, the fuel size is only one half. And we put
that one into our consideration of the manufacturing cost and something. Again, let me answer this
question quickly. We are -- whether we use a High-NA or not, actually, one High-NA is a very good tool.
Let's assume that, right? We understand it's a very high performance. But then, TSMC make it clear
that we work with ASML and try to make it more suitable for manufacturing in terms of the cost and in
terms of the maturity. So we always consider that technology maturity and the cost, and whether we use
it or not, okay?
Jeff Su (Executives)
Okay. Thank you, C.C. Do you have a second question, Robert?
Robert Sanders (Analysts)
Yes. Just a quick follow-up. I think all of us on this call are assuming that the unconstrained demand
for 3-nanometer and below is sort of 30% to 50% above your ability to supply. Is it, in fact, much larger
than 30% to 50% above? It feels like it might be based on what you're saying because I think all of us
are assuming it sort of solvable over the next 3, 4 years, but it sounds like the number could be much
larger.
Jeff Su (Executives)
Well, those are your numbers, but Robert is asking the demand in excess of supply. Is it 30% to 50%? Is
it something even larger? Do we have a number to share?
C.C. Wei (Executives)
No, we don't have a number to share because of -- let me say that, the gap is very big. Sorry, I don't
want to make a comment on the memory, but a very big gap.
Jeff Su (Executives)
Okay. We have about 9 minutes left. We'll come back to the floor with any questions. Let's take one
from here. Evelyn Yu from Goldman.
Evelyn Yu (Analysts)
Because we mentioned a lot on that we're going to step up our capacity growth. I'm just trying to
quantify here because I noticed that during your symposium that you actually mentioned about 2-
nanometer family capacity growth will be growing at around 70% CAGR from '26 to '28 and N3 plus
and N5 to grow by 25% CAGR from '22 to '27. So I was just wondering, are those numbers still right

assumptions today? Are we seeing actually any changes over the past quarter? And how should we
compare with the non-supporting demand out there?
Jeff Su (Executives)
Okay. So Evelyn's first question is around capacity growth. She knows during the symposium, we did
share some 5-year CAGR growth numbers for 2-nanometer around 70% CAGR and then 3-nanometer
around, I guess, I can't remember the exact, but 25%. So are those numbers still the same? Or has it
changed now that our CapEx and stuff?
C.C. Wei (Executives)
Did we say that in Technology Symposium? We showed the chart. Okay. Now it's bigger. That's what I
say.
Jeff Su (Executives)
Do you have a second question?
Evelyn Yu (Analysts)
Okay. Very good direction. All right. My another question touched based on the advanced packaging
side. Because you always bundle the advanced packaging CapEx together with testing, mask making,
and others, that's around 10% to 20% of total CapEx.
And so one thing I'm trying to figure out here is that how much of that actually goes to advanced
packaging alone? And because given that advanced packaging is capital intensive, less capital intensive
versus front-end, so how should we think about the gap between its pricing revenue share and its
CapEx share over the next few years?
And well, I think finally is that, as it becomes more important, how should we think of -- maybe you
should consider breaking it out as a separate CapEx item going forward?
Jeff Su (Executives)
Okay. So Evelyn's question is around advanced packaging. She wants to know when we guide for the
CapEx, of course, we guided in a bucket of packaging, testing, mask making and others together. Why
do we not separate out just into packaging specifically? Her suggestion is, we should. But I think more -
- so that's part of it, number one, the CapEx breakdown.
C.C. Wei (Executives)
Evelyn, let me say that. We try very hard to make sure that our CapEx number is correct, but with the
flexibility between the front-end and the back-end. Sometimes we have a bottleneck. So we put more
money to buy the bottleneck tools. And sometimes it is in the front-end, sometimes it's in the back-end.
But in the ballpark, the percentage is just like a Wendell share with everybody.
For long term, I mean, that's the back end, is about...
Jeff Su (Executives)
10% to 20%.
C.C. Wei (Executives)

10% to 20%, that's a big range anyway. So that we -- what I can say is that's still 10% to 20%. Because of
-- as I said, actually, I'm very honest to tell you that as time goes by, some of the customers' product
need more tester. You cannot believe that. I mean, so the tester in shortage, so we have to put more
CapEx in the tester or in the packaging or in other areas. So that's why we cannot very specifically say
which area we put how much of the CapEx.
Jeff Su (Executives)
That's too specific. Yes. Okay. With the last participant, KGI, Felix Pan, thank you for being patient.
Junhong Pan (Analysts)
So my first question is regarding to the CapEx revision. So from year-to-date, so TSMC raised the
CapEx guidance by almost USD 10 billion. So can you give me some color where is the upside from?
How you guys see the difference from 6 months ago? Is that from like CPU accelerator or memory
components or back-end CoWoS expansion? Just the upside, how we see things differently from 6
months ago?
Jeff Su (Executives)
Okay. So Felix is noting in January, we guided for $52 billion to $56 billion. In April, we said closer to
$56 billion, now $60 billion to $64 billion. So we have increased the CapEx guidance. What is driving
this? Is it Agentic AI only? Is it packaging? Is it AI accelerator?
C.C. Wei (Executives)
Well, simply put, the most important reason is because of the demand continued to increase, and we
feel the pressure from the customer to drive TSMC, not drive actually, to cooperate with TSMC for the
capacity increase. That's one of the major reasons. The second reason is inflation. Now we buy the tools
with inflation price, okay? You understand what I say.
Junhong Pan (Analysts)
Okay. So my second question is about the mature node. So people always focus on AI leading nodes, but
it seems like mature nodes also seeing a very strong demand recovery and also some supply issue as
well. So how do you guys see the demand-supply dynamic and pricing for the mature node? Because
apparently, there's some impact from the AI crowding out effect. But mature nodes still largely depends
on the consumer demand. So customer demand is still weak. So how do you guys see the demand
supply dynamic for mature nodes?
Jeff Su (Executives)
Thank you. So Felix's second question is on mature node. He notes there's lots of talk that mature
nodes are seeing a strong demand recovery and the supply is very tight. So mature node pricing is very
favorable or strong. So he wants to know how do we see the mature node supply-demand situation?
C.C. Wei (Executives)
Actually, the mature node cover a lot of different segments. Only the one which related to AI is in
shortage, which is the most important one, is the #1 is power management IC, because all the AI data

centers need a lot of power management. And those are the mature node technology like 0.18 micron,
90-nanometer or something like that. Those are in shortage definitely.
And also the sensor portion because of -- you need a lot of sensor to detect the environmental
information and put into the AI data center to analyze it. Other than that, other area, just like you
pointed out, the consumer product is not in a high demand. And so other segment is not so strong
demand. And as I pointed out in my statement, other area, no, it's not so much of, say, in a lot of
shortage, not at all.
Jeff Su (Executives)
Okay. Thank you. Thank you, C.C. Thank you, Wendell. Thank you, everyone. This does conclude our
Q&A session. Before we conclude today's conference, please be advised that the replay of the conference
will be accessible within 30 minutes from now. The transcript will become available 24 hours from
now, and both are going to be available through our website, again at www.tsmc.com.
If some of you were not able to ask your question, please feel free to reach out to TSMC IR, and we will
follow up with you. So thank you, everyone, for joining us today. We hope everyone continues to stay
well.
Have a good summer, and we hope you'll join us again next quarter. Thank you, and have a good day.


---

## ④ 判斷卡（judge_card.md）

<!-- source: .claude/skills/stock-analyst/references/v16/judgment-rules-v19.md sha256:342f7c06bb0a97e9 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->

# 判斷卡（v20 judge，Fable 單輪無工具）

你是買側資深分析師＋PM決策層，估值任務＝判斷股價隱含什麼預期非預測未來值多少；好生意（獲利品質好、ROIC持續期長、護城河產業結構好）優先於好價格，好價格是加分項非前提 [§0]。輸入＝bundle全文(facts.json事實表＋最新一季逐字稿＋本卡＋archetype條件載入段)，之外不開。
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

**`contradictions[]`**：先列一致判斷，再列矛盾(矛盾點/A側/B側/性質：可調和=程度差異、不可調和=方向相反)；⚖不可調和矛盾必填裁決：選哪邊/依據(非「直覺」)/硬數據點/執行路徑(≥1 if-then＋1反向條件，動作具體如加碼至X%/清倉，禁「再評估」)；Steelman義務：觀望迴避寫「現在就買的最強論證」，進場寫「現在就賣的最強論證」。前份漂移歸因：`drift_watch`20欄按`cause`三選一(`價格變動`/`新證據`/`方法變動`)分組，`prior_field`填涵蓋欄名陣列，漏一欄＝FAIL；門檻或Single Thing與前份不同須歸因「舊→新＋理由」，`rearm_trigger`不得寫「相同」；觀望須點名binding constraint，`rearm_trigger`=該約束的否定，多因素模糊觀望=重寫 [§5]；前次觀望/迴避且報酬>+30%須明寫翻面理由；90天內翻面須引用前次觸發器已發火，引不出填`qc49_inherit_prior=true`+`prior_verdict`+`prior_role` [§4]。

**負向證據強制處置（硬擋）**：`findings_digest[]`每條`direction="-"`的finding必落於`contradictions[]`/`blind_spots[]`/`triggers[]`/`moat.threats[]`/`thesis.R[]`之`evidence_refs`，或寫進`evidence_dismissed[]`(`{"ref":…,"reason":…}`，理由需指出證據本身問題，禁「影響不大」)。`triggers[]`每列`n`/`text`/`type`/`maps_to`/`metric`/`threshold`/`action`/`source_freq`/`date`；type僅八值(假設驗證/風險/Single Thing/估值rearm/加碼/減碼/清倉/複審日期)，H1-H3或R1-R3寫`maps_to`不塞`type`。`kill_metrics[]`陣列，每條`metric`/`bear_threshold`/`window`＋`source`；`rearm_trigger`=估值rearm/進場首倉列；`catalysts[]`type英文六值`product`/`regulatory`/`capacity`/`guidance`/`macro`/`other`(禁中文)。QC-39產業態勢三軸(必填一句)：A競爭惡化/B結構轉好與durability/C其他結構變數(法規/關稅/反壟斷/通路/商模/替代技術/客戶結構)→裁決=競爭惡化中/結構性轉好中/其他結構變動中(指名哪軸)/雙向拉鋸/靜態＋一句sourced依據，禁只報單向 [§6]。重大事件：M&A(>市值5%)/集體訴訟/臨床或FDA讀數/CEO或CFO離職或SEC調查/客戶流失皆🔴，涉核心假設或護城河須入`thesis.R`或`moat.threats` [§5][§6]。

**必答項**：三視角blind_spots各至少一條、不可調和矛盾的⚖裁決、`evidence_dismissed[]`(若有負向finding未落點)、`kill_metrics[]`、`rearm_trigger`。

---

## ⑤決策輸入與行動條件

**`decision_inputs`**（值可`null`，`dd_decision.py`機械路由裁決）七欄：`thesis_irreconcilable`(§4不可調和)｜`valuation_dependent`(re-rate貢獻≥Base IRR 40%)｜`market_wrong_reason_given`(市場錯在哪的具體理由)｜`week26_return_pct`(26週漲幅)｜`momentum_overheated`(RSI 14d>70或4週漂移>+10%)｜`cycle_gates_pass`(反動能五閘全過，循環股)｜`consensus_rev_3m_pct`(FY1/FY2共識近3月上修%)，缺值`null`。覆寫層：`val_denominator_disputed`/`qc49_inherit_prior`+`prior_verdict`+`prior_role`/`held_now`(bool三態不可`"unknown"`代`null`)；`asym_ratio`/`irr_base_pct`/`ev5y_pct`一律`null` [§5]。

**問五｜估值**：判斷句＝現價要求未來發生什麼才划算，我信不信。`valuation.percentile_5y`(=(當前−5Y低)÷(5Y高−5Y低)×100%，必引`valuation_history`禁外推)｜`valuation.peg`(Non-GAAP 3年EPS CAGR，<1.0便宜/1~2合理/>2貴)｜`val_light`+`val_light_derivation`｜`upside_short_pct`/`upside_mid_pct`。分母含一次性效應→改前瞻錨定，若分母正是爭點→`val_denominator_disputed=true`且便宜論證無效並填`val_denominator_note`。條件式加尺：同業tier禁跨tier當anchor，依archetype定優先尺(商品循環P/B；複利Fwd P/E・PEG；未獲利EV/GP對照EV/S)。`appendix_a`四欄(`val`/`signal`/`ma`/`long_term_confidence`，全文見timing-appendix.md)：估值🔴+動能爆衝+品質A/B落B；`long_term_confidence`上限「中」：問三缺口無法歸因、或`capalloc_grade`=C [§2問五]。

**問四｜現金與資本配置**：判斷句＝`governance.capalloc_grade`；FCF/NI轉換率、SBC/營收、現金去向四分為最小交付。計分卡(唯一決定`capalloc_grade`)：M&A已實現ROIIC(≥WACC過)｜回購買入收益率(≥10Y殖利率+2%過)｜SBC淨稀釋率(≤1.5%/yr過)；≥2/3過=A、1項=B、0項=C。C級→信心上限「中」、天花板打8折。營運槓桿：Rev YoY−OI YoY，>3%壓縮列成長熄火。`governance.capital_returns`(成長靠併購撐時展開，未展開見共用約定) [§2問四]。

**必答項**：`decision_inputs`七欄、`governance.capalloc_grade`、`valuation.percentile_5y`、`valuation.peg`、`val_light`、`upside_short_pct`/`upside_mid_pct`、`appendix_a`四欄、`eps_meta`。

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
{"date":"20260808","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1：AI/HPC 對先進製程需求持續超過供給至 2027-2028","text":"3nm 稼動率、CoWoS 產能瓶頸表態、hyperscaler 資本支出年增","columns":{"門檻":"3nm 稼動率跌破 90%，或 hyperscaler 合計資本支出年增 &lt;15%","來源":"Q2 FY26 法說（CoWoS「持續是產業瓶頸」）、TSMC 官方 2024-2029 AI 加速器 CAGR guide 中高 50%","漂移觸發":"2 季連續稼動率下滑"}},{"id":"H2：製程/良率領先維持定價權","text":"N2 良率 vs Intel 18A／Samsung SF2；sub-5nm 5-10% 提價吸收情況","columns":{"門檻":"良率差距收斂至 &lt;3pp 且客戶開始轉單","來源":"N2 良率 65-75%（機構估，公司未官方揭露量產良率數字）vs Intel 18A 55-75%~85%（techtimes.com 2026-07-15 引述 85% vs 2026-06 CNBC／VLSI Symposium 實測 55-75%，來源分歧）","漂移觸發":"單一旗艦客戶轉單 &gt;20% 配額"}},{"id":"H3：地緣/關稅風險可控、非存續性","text":"Section 232 框架協議執行、出口管制調查結果、Arizona 進度","columns":{"門檻":"罰款 &gt;$20 億或新增全面出口限制","來源":"美台 2026-01-15 框架協議（commerce.gov）、Sophgo 調查（doccredit.world 2026）","漂移觸發":"調查結果公布或立法通過"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔至 Fwd PE(FY27) ≤16x（約 $346）或連兩季 GM 低於 65% 之外的加碼窗口","irr_base_pct":13.0,"ev5y_pct":93.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":8.0,"ev5y_pct":93.0,"irr_base_pct":13.0,"max_dd_pct":-45.0,"bull_5y_price":1300.0,"bear_5y_price":288.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"回檔至 Fwd PE(FY27) ≤16x（約 $346）或連兩季 GM 低於 65% 之外的加碼窗口","price_at_dd":420.04,"archetype":"品質複利成長","cycle_position":null}}
```

---

## ⑦b 前份漂移歸因（機械閘逐欄對帳）

上面前份摘要的 `drift_watch_prior` 列了 20 欄前份值。`counter_evidence.contradictions[]` 內必須有條目的 `prior_field` 陣列**合起來涵蓋這 20 個欄名的每一個**（含程式稍後才會算的 asym_ratio／bull_5y_price／bear_5y_price／p_bull_pct／p_bear_pct／ev5y_pct／irr_base_pct／max_dd_pct，把它們歸進 `cause`=`價格變動` 或 `方法變動` 那條即可），每條 `cause` 三選一（`價格變動`／`新證據`／`方法變動`），漏一欄＝FAIL。`kill_metrics`／`rearm_trigger`／Single Thing 的門檻與前份不同時，另開一條 `cause`∈{`新證據`,`方法變動`}、`side_a`=舊門檻原文、`side_b`=新門檻原文，條目文字要含該動作名（如「清倉」「減碼」）；唯一致命點變動的那條文字要含「Single Thing」字樣，`side_a`=前份唯一致命點原文、`side_b`=本次原文。

`decision_inputs.ma`（週線均線六態）由程式從週線均線算出，值在事實表 `f_ma_state`：**照抄該值**，不得自判、不得填 ✅ 或「-」；程式落檔時會強制覆寫成事實表的值。

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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20260916/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
