你是 stock-analyst **v20 判斷 agent**，標的 JNJ（20261018）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"JNJ","date":"2026-10-18","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JNJ_20261018/evidence.json","digest_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JNJ_20261018/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap_reported_sales","label":"營收（GAAP reported sales）","value":25399,"period":"Q3 FY2026（公告於 2026-10-13）","unit":"USD M","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（公告於 2026-10-13）","citation":"公司新聞稿 jnj.com Q3 2026 press release（8-K Ex.99.1）"},"note":"未查得"},{"id":"f_kpi1_non_gaap_adjusted_income","label":"Non-GAAP 稅前利益率（adjusted income before tax / sales；JNJ 不揭露 non-GAAP 營業利益，以此代替）","value":30.2,"period":"Q3 FY2026（公告於 2026-10-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（公告於 2026-10-13）","citation":"公司新聞稿 adjusted income before tax 7,672 ÷ 營收 25,399（自算）"},"note":"未查得"},{"id":"f_kpi2_gaap_sm_a_r_d_ipr_d_othe","label":"GAAP 營業利益／利益率（自算：毛利−SM&A−R&D−IPR&D減損−重組；不含 Other expense 5,780 的 talc 等一次性項目）","value":23.0,"period":"Q3 FY2026（公告於 2026-10-13）","unit":"%","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（公告於 2026-10-13）","citation":"公司新聞稿損益表自算：17,302−6,285−4,652−339−181＝5,845M"},"note":"未查得"},{"id":"f_kpi4_2026_10","label":"管理層全年指引（2026，10 月上調）","value":"adjusted EPS $11.05–$11.15（中點 $11.10）","period":"Q3 FY2026（公告於 2026-10-13）","unit":"USD","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（公告於 2026-10-13）","citation":"公司新聞稿 guidance 表"},"note":"consensus FY1 EPS 11.08（dd_numbers_extra.py consensus_revision，2026-10-08 快照）"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-10-13","period":"2026-10-13","unit":"date","basis":"距今 4 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-10-13"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_jnj_gross_margin_pct","label":"JNJ 毛利率","value":67.91,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JNJ.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jnj_operating_margin_pct","label":"JNJ 營業利益率","value":26.81,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JNJ.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_jnj_fcf_margin_pct","label":"JNJ FCF 利潤率","value":22.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JNJ.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mrk_gross_margin_pct","label":"MRK 毛利率","value":72.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mrk_operating_margin_pct","label":"MRK 營業利益率","value":10.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_mrk_fcf_margin_pct","label":"MRK FCF 利潤率","value":24.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lly_gross_margin_pct","label":"LLY 毛利率","value":83.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lly_operating_margin_pct","label":"LLY 營業利益率","value":49.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_lly_fcf_margin_pct","label":"LLY FCF 利潤率","value":17.02,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_gross_margin_pct","label":"ABBV 毛利率","value":71.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_operating_margin_pct","label":"ABBV 營業利益率","value":33.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_abbv_fcf_margin_pct","label":"ABBV FCF 利潤率","value":28.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bsx_gross_margin_pct","label":"BSX 毛利率","value":69.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bsx_operating_margin_pct","label":"BSX 營業利益率","value":21.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_bsx_fcf_margin_pct","label":"BSX FCF 利潤率","value":8.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_fcf","label":"自由現金流（FCF，前三季累計，非單季）","value":15100,"period":"2026 前三季累計（估計，截至 2026-10-13 公告）","unit":"USD M（約）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"2026 前三季累計（估計，截至 2026-10-13 公告）","citation":"公司新聞稿 overall financial results 表（~$15,100M；腳註為 YTD 估計）"},"note":"未查得"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":255.56,"period":"2026-10-16（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":10.3,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":43.83,"period":"2026-10-16（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.09,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（11.07 → 11.08）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":0.33,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（12.14 → 12.18）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":4.23,"period":"2026-10-08","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（14.2 → 14.8）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":11.08,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":12.18,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":14.8,"period":"2026-10-08","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":-4.15,"period":"2026-07-16 → 2026-10-08","unit":"%","basis":"FY1 共識 EPS 11.56 → 11.08（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-08","citation":"DD_universe_EPS_estimates_20261008.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":38.78,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":6.2,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":6.48,"period":"2026-10-16（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-16（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-16（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-16（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":23.6,"period":"2026-10-08","unit":"x","basis":"分母＝FY1 EPS 11.08，分子＝快照價 261.44","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-08"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":2.066,"period":"2026-10-18","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-18"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":28278.0,"period":"2026-10-18","unit":"USD m","basis":"yfinance 最新一季：總債務 49036.0、現金 20758.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":2409.9,"period":"2026-10-18","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":644151.64,"period":"2026-10-18","unit":"USD m","basis":"市值 615873.64 ＋ 淨負債 28278.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":101222.92,"period":"2026-10-18","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":107904.34,"period":"2026-10-18","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":6.36,"period":"2026-10-18","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-18"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Q2 2026 10-Q 稱 TREMFYA 成長來自各適應症的份額增加與 IBD 上市動能；J&J 稱 Tremfya 在 UC 與 Crohn's 的 IL-23 類新病人起始（induction share）居首。","source":"JNJ Form 10-Q FY2026 (period ended 2026-06-28)","url":"https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000153/jnj-20260628.htm","excerpt":null,"as_of":"2026-06-28","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Stelara 2026 Q1 銷售 6.56 億美元、年減約 59–60%，因生物相似藥進入；Q2 10-Q 預期 biosimilar 持續衝擊，Q2 約 -55.7%。Simponi 生物相似藥已於 2026 Q2 進入歐洲，美國可能 2026 年稍後出現。","source":"JNJ Form 10-Q Q2 FY2026; Nasdaq 'Johnson & Johnson Q2 earnings call highlights'","url":"https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000153/jnj-20260628.htm","excerpt":null,"as_of":"2026-06-28","retrieved_at":"20261018","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"MedTech 2026 Q2 放緩：心血管受電生理競爭（脈衝電場消融 PFA）壓力與 Abiomed 銷售 -2%（英國研究使 Impella 使用放緩，J&J 稱為暫時）拖累，Shockwave 仍雙位數成長；電生理銷售 +3.1%。","source":"Nasdaq/Zacks 'J&J's MedTech Performance Slows in Q2: Will Sales Improve in H2?'","url":"https://www.nasdaq.com/articles/jjs-medtech-performance-slows-q2-will-sales-improve-h2","excerpt":null,"as_of":"2026-06-28","retrieved_at":"20261018","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"FDA 近期核准 J&J OTTAVA 手術機器人系統；搜尋結果未提供其對 Intuitive 等的份額數字。","source":"Nasdaq/Zacks 同上文","url":"https://www.nasdaq.com/articles/jjs-medtech-performance-slows-q2-will-sales-improve-h2","excerpt":null,"as_of":"2026-06-28","retrieved_at":"20261018","affects":["thesis.H","triggers"],"status":"ok"},{"id":"customer_second_source#none","axis":"customer_second_source","section":"coverage","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"-","claim":"FY2025 10-K：三大批發商分別約占總毛營收 21.8%、15.5%、11.1%（合計約 48.4%），FY2024 為 20.5%/15.6%/12.3%，集中度上升","source":"JNJ Form 10-K FY2025","url":"https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm","excerpt":"In fiscal year 2025, the Company utilized three wholesalers distributing products for both segments that represented approximately 21.8%, 15.5% and 11.1% of the total gross revenues.","as_of":"2026-02-01","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"S&P 在 2025-04 確認 J&J AAA 並移出 CreditWatch；2026-06 報導仍稱 J&J 為僅有兩家獲 S&P AAA 的美國企業之一；未見 2026 年降評或 Moody's 評等行動","source":"Bloomberg 2025-04-25；24/7 Wall St 2026-06-10","url":"https://247wallst.com/investing/2026/06/10/got-1000-1-healthcare-king-to-buy-and-never-sell-that-is-safer-than-a-treasury-bond/","excerpt":null,"as_of":"2026-06-10","retrieved_at":"20261018","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"2026 Q2 Stelara 銷售年減 55.2%，LOE 拖累創新藥部門成長 760bp、總營收 460bp；Darzalex +18.9% 至 $4.21B，Tremfya +72.5% 至 $2.05B。","source":"Nasdaq/Zacks: J&J's Innovative Medicine Unit Proves Its Resilience in Q2","url":"https://www.nasdaq.com/articles/jjs-innovative-medicine-unit-proves-its-resilience-q2","excerpt":"In the second quarter of 2026, Stelara's sales fell 55.2%, and the loss of exclusivity negatively impacted the Innovative Medicines segment's growth by 760 basis points and total revenues by 460 basis points in the second quarter.","as_of":"2026-07-15","retrieved_at":"20261018","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"Simponi 與 Opsumit 於 2026 起面臨學名藥壓力；J&J 預期腫瘤業務年底前達 $50B 年銷售（高於華爾街預估）。","source":"搜尋摘要彙整（Nasdaq/BioSpace 系列報導）","url":"https://www.nasdaq.com/articles/jjs-innovative-medicine-unit-proves-its-resilience-q2","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261018","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"J&J 美國 $55B 投資計畫（至 2029 初）；佛州 Jacksonville ACUVUE 廠 >$1B 預計 2028 全面營運；賓州細胞治療廠 >$1B（2026-02 宣布）；北卡 Wilson 生物藥廠約 $2B；2025 年底已投入約 $12B。","source":"Plastics Today / Fierce Pharma / MedTech Dive 彙整","url":"https://www.fiercepharma.com/manufacturing/johnson-johnson-reveals-55b-investment-us-which-includes-3-new-manufacturing-sites","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Guggenheim 升評 Buy、目標價 $206，認為 J&J 已順利度過 Stelara LOE，創新藥將推動下一階段成長。","source":"TipRanks/The Fly: Guggenheim upgrades Johnson & Johnson on growth post Stelara expiry","url":"https://www.tipranks.com/news/the-fly/guggenheim-upgrades-johnson-johnson-on-growth-post-stelara-expiry-thefly","excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261018","affects":["thesis.H","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"FTC 於 2026 年 6 月向第四巡迴上訴法院提交 amicus brief，主張地方法院駁回 CareFirst 對 J&J 以專利延遲 Stelara 生物相似藥競爭之反壟斷訴訟時，適用了錯誤的法律標準（應看競爭效果而非意圖）。這是私人訴訟，非 FTC 對 J&J 的調查。","source":"GENE ONLINE / PSCA 'FTC Weighs in on Pharmaceutical Anti-Trust Case'","url":"https://www.psca.org/news/psca-news/2026/6/ftc-weighs-in-on-pharmaceutical-anti-trust-case/","excerpt":"The FTC made that argument in an amicus brief filed Monday in the Fourth Circuit Court of Appeals, contending that a district court applied an incorrect legal standard when it dismissed an antitrust claim against Johnson & Johnson over its use of patents to delay biosimilar competition to Stelara.","as_of":"2026-06-01","retrieved_at":"20261018","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"J&J 向第四巡迴法院陳述不應復活 CareFirst 的 Stelara 壟斷訴訟；下級法院原已判 J&J 勝訴（另有親商基金會 2026-08-19 發文支持該勝訴）。","source":"MLex 'J&J Says No To Reviving Stelara Case'","url":"https://www.mlex.com/healthcare-authority/policy-compliance/articles/2513168/j-j-says-no-to-reviving-stelara-case","excerpt":null,"as_of":"2026-08-19","retrieved_at":"20261018","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Biosense Webster（J&J 旗下）在 Innovative Health 的心導管再處理案中遭陪審團判反壟斷敗訴，法官將損害賠償三倍至 4.42 億美元；J&J 其後聲請推翻判決，搜尋未找到後續結果。","source":"MassDevice 'Johnson & Johnson seeks to have $442 million antitrust verdict tossed out'","url":"https://www.massdevice.com/johnson-johnson-seeks-to-have-442-million-antitrust-verdict-tossed-out/","excerpt":null,"as_of":"2025-12-31","retrieved_at":"20261018","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"regulatory_antitrust#3","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"比利時競爭主管機關因『教科書式』的反競爭品類管理，對 J&J Consumer、Boehringer Ingelheim 與 Haleon 合計罰款 1,120 萬歐元。","source":"Global Competition Review 組織頁 Johnson & Johnson","url":"https://globalcompetitionreview.com/organisations/johnson-johnson","excerpt":null,"as_of":"2025-11-30","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"regulatory_antitrust#4","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"J&J FY2025 10-K 與 2026 Q2 10-Q 的風險因素載明：產品行銷、定價與銷售受 FDCA、虛假申報法等監管，並面臨聯邦機構與州檢察長調查及可能的民刑事處罰。屬一般性揭露，未指出新的具體調查。","source":"J&J Form 10-K FY2025 / 10-Q Q2 2026","url":"https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm","excerpt":"The marketing, pricing and sale of the Company's products are subject to regulation, investigations and legal actions including under the Federal Food, Drug, and Cosmetic Act.","as_of":"2026-07-23","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"J&J 於 2026-01-08 宣布與美國政府達成協議，其藥品可豁免潛在的 Section 232 關稅，協議與最惠國（MFN）藥價掛鉤。","source":"Global Trade Alert — Agreement with Johnson & Johnson on most-favoured-nation drug pricing and tariff exemption","url":"https://globaltradealert.org/intervention/153967-united-states-of-america-agreement-with-johnson-johnson-on-most-favoured-nation-drug-pricing-and-tariff-exemption","excerpt":"On 8 January 2026, Johnson & Johnson announced reaching an agreement with the U.S. Administration. The agreement provides the company's pharmaceutical products an exemption from potential Section 232 tariffs","as_of":"2026-01-08","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"2026-04-02 總統令對專利藥品及成分課 Section 232 關稅（最高 100%）；承諾 MFN 藥價與美國本土製造的公司，零稅率可至 2029-01-20。","source":"JD Supra — Section 232 Tariffs on Pharmaceuticals: 100% Duties on Patented Drugs and APIs Starting July 31, 2026；Crowell client alert","url":"https://www.jdsupra.com/legalnews/section-232-tariffs-on-pharmaceuticals-9663434/","excerpt":"companies that commit to both Most Favored Nation (MFN) drug pricing with HHS and domestic manufacturing with the Department of Commerce face a zero percent rate through January 20, 2029","as_of":"2026-04-02","retrieved_at":"20261018","affects":["thesis.R","valuation"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"一份顧問報告指出，截至 2026 年 6 月，Pfizer、J&J、GSK 仍無已確認的 Commerce 在地製造協議（與 J&J 1 月宣布的 MFN／關稅豁免協議的關係，搜尋結果未釐清）。","source":"Exiger／intuitionlabs 等搜尋摘要（Pharma Tariffs 2026: Supply Chain & Manufacturing Impacts）","url":"https://intuitionlabs.ai/articles/pharma-tariffs-2026-supply-chain-onshoring","excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261018","affects":["decision_inputs.bear","triggers"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"J&J 2025 年關稅成本預估由約 4 億美元降至約 2 億美元，主要集中於醫療器材（MedTech）；2025 年 7 月 CFO 表示 2026 年關稅影響尚難預測。","source":"Reuters via TradingView — Johnson & Johnson lifts 2025 forecast, halves tariff cost outlook","url":"https://tw.tradingview.com/news/reuters.com%2C2025%3Anewsml_L4N3TD0R5%3A0-johnson-johnson-lifts-2025-forecast-halves-tariff-cost-outlook","excerpt":null,"as_of":"2025-07-16","retrieved_at":"20261018","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#4","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"J&J 2026 年 Q2 10-Q（期末 2026-06-28）風險揭露稱，公司可能進一步受到任何司法管轄區採行偏袒本國企業的關稅或貿易保護措施影響；摘要未見中國專屬數字。","source":"SEC Form 10-Q FY2026 (period ended 2026-06-28)","url":"https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000153/jnj-20260628.htm","excerpt":null,"as_of":"2026-06-28","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"J&J FY2025 10-K 風險因子列出國際營運曝險：貿易保護措施、進出口許可、外國資產被徵收，以及戰爭、武裝衝突等地緣事件；未見特定單一地緣區域集中的描述（僅為搜尋摘要所見）","source":"SEC Form 10-K FY2025 (Johnson & Johnson)","url":"https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm","excerpt":null,"as_of":"2025-12-28","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"J&J 財務長表示 2025 年關稅成本約 4 億美元，其中以中國關稅及中國報復性關稅為最大部分；2026 年影響當時尚難預測","source":"MedTech Dive: J&J tariff costs $400 million 2025","url":"https://www.medtechdive.com/news/jnj-tariff-costs-400-million-2025/745357","excerpt":null,"as_of":"2025-10-14","retrieved_at":"20261018","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"歷史單點失效案例：2010 年 McNeil Fort Washington 工廠因品質違規停工逾兩年；2021 年 Emergent Baltimore 廠（合約製造）混料致約 1,500 萬劑 J&J 新冠疫苗報廢。均為舊事件，非現況集中度證據","source":"AboutResilience; Risk & Insurance; NPR (2021-04-01)","url":"https://riskandinsurance.com/johnson-johnsons-vaccine-supply-chain-pitfall-where-was-the-risk-management/","excerpt":null,"as_of":"2021-04-01","retrieved_at":"20261018","affects":["decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"+","claim":"Q3 2026 Innovative Medicine 銷售 $16.76B，+7.7%（營運 +7.9%）；成長來自 Tremfya、Darzalex、Carvykti、Tecvayli、Erleada，Stelara 下滑拖累約 690bp","source":"J&J Q3 2026 results press release / search summary","url":"https://www.jnj.com/media-center/press-releases/johnson-johnson-reports-q3-2026-results-raises-2026-guidance","excerpt":"Innovative Medicine sales increased 7.7% to $16.76 billion, with operational growth of 7.9%.","as_of":"2026-10-13","retrieved_at":"20261018","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"-","claim":"Q3 2026 MedTech 營運成長 2.5%，低於管理層預期；弱點在國際心血管、外科與 Abiomed；Vision +5.1%","source":"J&J Q3 2026 results (search summary)","url":"https://www.jnj.com/media-center/press-releases/johnson-johnson-reports-q3-2026-results-raises-2026-guidance","excerpt":"MedTech delivered 2.5% operational sales growth, below management's expectations. Weakness was concentrated in international cardiovascular and surgery operations, alongside Abiomed.","as_of":"2026-10-13","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"2026 全年指引上調：銷售 $101.0–101.4B、調整後 EPS $11.05–11.15；Q3 全公司銷售 $25.4B（+5.9%）","source":"J&J Q3 2026 results (search summary)","url":"https://www.jnj.com/media-center/press-releases/johnson-johnson-reports-q3-2026-results-raises-2026-guidance","excerpt":"raised its full-year sales forecast to a range of $101.0 billion to $101.4 billion","as_of":"2026-10-13","retrieved_at":"20261018","affects":["valuation","triggers"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"-","claim":"Q2 2026 Stelara 因生物相似藥銷售下滑 59.7% 至 $656.0M；公司預期生物相似藥持續衝擊；Tremfya 首度單季破 $2B","source":"J&J 10-Q (Q2 2026) / MarketBeat Q2 call highlights","url":"https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000153/jnj-20260628.htm","excerpt":"The Company expects STELARA biosimilars to continue to negatively impact the Company's sales of STELARA.","as_of":"2026-07-15","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"+","claim":"Q1 2026 Darzalex 銷售 $3,964M，總成長 22.5%","source":"J&J 10-Q Q1 2026","url":"https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000087/jnj-20260329.htm","excerpt":"DARZALEX sales were $3,964 million, up 22.5% in total","as_of":"2026-04-14","retrieved_at":"20261018","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"電生理面臨 PFA 導管競爭壓力；中國量採（VBP）為跨部門持續逆風；骨科預計 2027 年中前分拆 DePuy Synthes，2026 年相關分拆成本 $0.4B","source":"J&J 10-Q Q2 2026 (search summary)","url":"https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000153/jnj-20260628.htm","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261018","affects":["thesis.R","moat_trend","triggers"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"0","claim":"IQVIA 預測全球藥品市場至 2030 年年增約 5–8%、達約 $2.6 兆；美國淨價成長 4–7%/年，低於過去五年淨 CAGR 9.4%","source":"IQVIA Institute, Global Medicine Use Trends 2026 blog","url":"https://www.iqvia.com/blogs/2026/03/iqvia-institutes-2026-forecast-global-medicine-use-stays-strong-despite-headwinds","excerpt":null,"as_of":"2026-03-20","retrieved_at":"20261018","affects":["valuation","thesis.H"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"J&J FY2025 10-K 列為風險因素：新產品/製程/技術的研發競爭可能造成產品與製程過時；專利到期後會有學名藥、生物相似藥進入（通用條款，未點名特定替代技術）","source":"SEC Form 10-K FY2025 (JNJ)","url":"https://www.sec.gov/Archives/edgar/data/200406/000020040626000016/jnj-20251228.htm","excerpt":"Competition in research and development of new and improved products, processes and technologies, which can result in product and process obsolescence","as_of":"2025-12-28","retrieved_at":"20261018","affects":["decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"substitute_technology#1","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Stelara 2026 年第一季銷售衰退快於公司預期，預期全年加劇；Amgen、Teva、Samsung Bioepis/Sandoz 等生物相似藥已在美上市；Simponi、Opsumit 預期 2026 起受學名藥衝擊","source":"Zacks: can jnj sustain growth amid patent legal and china risks","url":"https://www.zacks.com/stock/news/2932920/can-jnj-sustain-growth-amid-patent-legal-and-china-risks","excerpt":null,"as_of":"2026-04-30","retrieved_at":"20261018","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"substitute_technology#2","axis":"substitute_technology","section":"coverage","direction":"-","claim":"2026-04-14 第三巡迴上訴法院裁定 J&J 未能證明三星 Bioepis 第二個 Stelara 生物相似藥上市會損害其業務，J&J 敗訴","source":"Bloomberg Law: J&J Loses Appeal to Block Samsung's Stelara Biosimilar Drug Copy","url":"https://news.bloomberglaw.com/ip-law/j-j-loses-appeal-to-block-samsungs-stelara-biosimilar-drug-copy","excerpt":null,"as_of":"2026-04-14","retrieved_at":"20261018","affects":["thesis.R","triggers"],"status":"ok"},{"id":"substitute_technology#3","axis":"substitute_technology","section":"coverage","direction":"0","claim":"Stelara 專利失效使 2025 年創新藥業務成長減少 10.4%；Darzalex、Tremfya、Erleada 抵銷部分，創新藥季銷售連續兩季逾 150 億美元","source":"Zacks / FiercePharma 彙整","url":"https://www.fiercepharma.com/pharma/jj-flexes-15b-quarter-innovative-drugs-biosimilars-continue-chip-away-stelara","excerpt":null,"as_of":"2026-04-14","retrieved_at":"20261018","affects":["thesis.H","valuation"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"J&J 於 2026-03-04 推出 J&J Direct 網站，向無保險或自費的美國病患直售部分藥品，目前列 3 款（Invokana、Invokamet、Xarelto）；為 Reuters 報導。","source":"Reuters via AOL: Johnson & Johnson launches website for direct-to-consumer sales","url":"https://www.aol.com/johnson-johnson-launches-website-direct-230749742.html","excerpt":"The website, called J&J Direct, lists three drugs: diabetes treatments Invokana and Invokamet and blood thinner Xarelto.","as_of":"2026-03-04","retrieved_at":"20261018","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"J&J 於 2026-01-08 與川普政府達成自願協議（降價換關稅豁免），含參與 TrumpRx.gov 直接面向病患銷售，並將可比國際價格延伸至 Medicaid。","source":"Pharmaceutical Commerce / J&J press release: Johnson & Johnson joins TrumpRx (2026-01-09)","url":"https://www.pharmaceuticalcommerce.com/view/johnson-johnson-joins-trumprx","excerpt":null,"as_of":"2026-01-08","retrieved_at":"20261018","affects":["valuation","decision_inputs.bear"],"status":"ok"},{"id":"channel_business_model_shift#2","axis":"channel_business_model_shift","section":"coverage","direction":"0","claim":"MedTech 自 2026-01-01 起由區域制改為事業單位主導架構（MassDevice 報導）。","source":"MassDevice: Johnson & Johnson MedTech shift business unit structure","url":"https://www.massdevice.com/johnson-johnson-medtech-shift-business-unit-structure/","excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261018","affects":["moat_trend"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"JNJ 於 2026-10-13 公布 Q3 並上調 2026 指引：Q3 銷售 +5.9% 至 254 億美元；全年報告銷售指引中點約 1012 億美元（7/29 為 1011 億）；調整後 EPS 指引中點上調 0.06 至 11.10 美元。","source":"Johnson & Johnson 新聞稿 'Johnson & Johnson reports Q3 2026 results, raises 2026 guidance'（jnj.com）","url":"https://www.jnj.com/media-center/press-releases/johnson-johnson-reports-q3-2026-results-raises-2026-guidance","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261018","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Q3 調整後 EPS 2.59 美元，高於分析師共識 2.53 美元（Benzinga 列 Q3 共識 2.53、Q4 共識 3.02；營收共識 Q3 252.3 億、Q4 265.2 億）。","source":"Capital.com 報導 'Johnson & Johnson Q3 sales rise on MedTech growth, lifts 2026 outlook'；Benzinga earnings-forecasts","url":"https://capital.com/en-ae/news/johnson-johnson-q3-sales-rise-on-medtech-growth-lifts","excerpt":null,"as_of":"2026-10-13","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Q2 後（2026-07-29）公司指引為調整後 EPS 11.60–11.75 美元、營收 1008–1014 億美元（來源為二手整理）。此數字與 Q3 稿所述「中點 11.10」不一致，基準（含/不含某些項目）待判斷層核對一手新聞稿。","source":"SentiSense 'Johnson & Johnson Tops Q2 Earnings Estimates, Boosts FY 2026 Guidance'","url":"https://app.sentisense.ai/stories/johnson-johnson-tops-q2-earnings-estimates-boosts-fy-2026-guidance-07152026","excerpt":null,"as_of":"2026-07-15","retrieved_at":"20261018","affects":["valuation","triggers"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"目標價分布：Benzinga（2026 年 8 月底）18 位分析師、12 Buy／6 Hold，平均目標價約 254 美元；Guggenheim 8/6 升至 287、Wells Fargo 8/3 升至 282。另一聚合站（2026 年 8 月）22 位分析師、平均 271.05、16 Buy／6 Hold／1 Sell，近六個月 9 升 0 降；TD Cowen 7 月由 250 升至 300。兩來源平均值不同，屬二手聚合。","source":"Benzinga JNJ price-targets；Walnut Invest JNJ forecast","url":"https://walnutinvest.com/stocks/jnj/forecast","excerpt":null,"as_of":"2026-08-31","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"2026 年 1 月（Q4 2025 財報後）公司初始指引 EPS 11.43–11.63 美元，略高於當時市場 11.45 美元；Barchart 1 月稿共識 EPS 約 11.54 美元（26 位分析師，Moderate Buy）。","source":"Yahoo Finance 'Guggenheim Lifts Johnson & Johnson (JNJ) Outlook After Solid Q4 and 2026 Guide'；Barchart","url":"https://finance.yahoo.com/news/guggenheim-lifts-johnson-johnson-jnj-102211196.html","excerpt":null,"as_of":"2026-01-30","retrieved_at":"20261018","affects":["valuation"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"0","claim":"J&J 完成收購 Firefly Bio 並與 Sail Biomedicines 簽策略協議；兩案合計預計使 2026 調整後 EPS 減少約 $0.64（Firefly 約 $0.46、Sail 約 $0.18）；資產收購、Q3 2026 認列約 $10 億 IPR&D 費用。","source":"SEC Form 8-K FY2026 (jnj-20260729)","url":"https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000163/jnj-20260729.htm","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261018","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"-","claim":"美國最高法院 2026-04-20 駁回 J&J 對滑石粉證券集體訴訟（class certification）的上訴請求；第三巡迴法院 2025-07 維持集體認證，2025-10 駁回 en banc 重審。","source":"Mealey's / Harris Martin 報導","url":"https://www.harrismartin.com/publications/26/Talc/articles/90588/us-supreme-court-denies-chance-to-weigh-in-on-talc-related-securities-dispute/","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"FDA 於 2026-03 核准口服 IL-23 乾癬藥 icotrokinra（ICOTYDE）；另有 Tecvayli+Darzalex 前線多發性骨髓瘤組合核准，及 IMAAVY 於 2026-08-24 核准用於溫抗體型自體免疫溶血性貧血（日期來自聚合站，二手）。","source":"Simply Wall St 彙整；J&J Q1 2026 results (Seeking Alpha PR)","url":"https://simplywall.st/stocks/us/pharmaceuticals-biotech/nyse-jnj/johnson-johnson/news/did-multiple-fda-approvals-just-shift-johnson-johnsons-jnj-i/amp","excerpt":null,"as_of":"2026-08-24","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"0","claim":"J&J 完成 Firefly Bio 收購並與 Sail Biomedicines 簽策略協議；合計預計減少 2026 調整後 EPS 約 $0.64；約 $10 億 IPR&D 費用於 Q3 2026。宣布日 2026-06-08 僅見聚合站記載。","source":"SEC Form 8-K FY2026 (jnj-20260729)","url":"https://www.sec.gov/Archives/edgar/data/0000200406/000020040626000163/jnj-20260729.htm","excerpt":null,"as_of":"2026-07-29","retrieved_at":"20261018","affects":["valuation","thesis.H"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"滑石粉石棉揭露不實之證券集體訴訟（2018 起，股東期間 2013-02-22 至 2018-12-13）：最高法院 2026-04-20 駁回 J&J 上訴請求，集體認證確立，案件朝審判或和解推進。","source":"Harris Martin Talc","url":"https://www.harrismartin.com/publications/26/Talc/articles/90588/us-supreme-court-denies-chance-to-weigh-in-on-talc-related-securities-dispute/","excerpt":null,"as_of":"2026-04-20","retrieved_at":"20261018","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"clinical_fda#0","axis":"clinical_fda","section":"events","direction":"+","claim":"FDA 於 2026-03 核准 icotrokinra（ICOTYDE）用於乾癬；Tecvayli+Darzalex 前線組合核准；IMAAVY 於 2026-08-24 核准用於 wAIHA（二手來源）。","source":"Simply Wall St；Seeking Alpha J&J Q1 2026 PR","url":"https://simplywall.st/stocks/us/pharmaceuticals-biotech/nyse-jnj/johnson-johnson/news/did-multiple-fda-approvals-just-shift-johnson-johnsons-jnj-i/amp","excerpt":null,"as_of":"2026-08-24","retrieved_at":"20261018","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#none","axis":"sec_investigation_restatement","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"JNJ","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":67.91,"operating_margin_pct":26.81,"fcf_margin_pct":22.7,"rd_intensity_pct":15.42},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.JNJ","as_of":"TTM ending 2026-06-30（4季加總）"},"is_subject":true},{"name":"MRK","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.97,"operating_margin_pct":10.49,"fcf_margin_pct":24.13,"rd_intensity_pct":45.75},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MRK","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"LLY","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":83.4,"operating_margin_pct":49.72,"fcf_margin_pct":17.02,"rd_intensity_pct":18.32},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.LLY","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"ABBV","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":71.48,"operating_margin_pct":33.94,"fcf_margin_pct":28.28,"rd_intensity_pct":15.09},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.ABBV","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"BSX","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":69.92,"operating_margin_pct":21.0,"fcf_margin_pct":8.6,"rd_intensity_pct":10.25},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.BSX","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"JNJ"},"financial_history":{"ticker":"JNJ","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-12-31","revenue":79990000000.0,"revenue_yoy_pct":null,"gross_margin_pct":69.25,"operating_margin_pct":26.27,"net_income":17941000000.0,"diluted_eps":6.73,"free_cash_flow":17185000000.0,"fcf_margin_pct":21.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-12-31","revenue":85159000000.0,"revenue_yoy_pct":6.46,"gross_margin_pct":68.82,"operating_margin_pct":25.84,"net_income":35153000000.0,"diluted_eps":13.72,"free_cash_flow":17778000000.0,"fcf_margin_pct":20.88,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-12-31","revenue":88821000000.0,"revenue_yoy_pct":4.3,"gross_margin_pct":69.07,"operating_margin_pct":23.92,"net_income":14066000000.0,"diluted_eps":5.79,"free_cash_flow":18059000000.0,"fcf_margin_pct":20.33,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-12-31","revenue":94193000000.0,"revenue_yoy_pct":6.05,"gross_margin_pct":67.88,"operating_margin_pct":27.17,"net_income":26804000000.0,"diluted_eps":11.03,"free_cash_flow":19313000000.0,"fcf_margin_pct":20.5,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-12-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/JNJ/JNJ_Q3_2026_Earnings_Call_20261013.md）

# Q3 2026 Earnings Call
**Johnson & Johnson** | Earnings Calls | 2026-10-13

**Operator** (Operator):
Good morning, and welcome to Johnson & Johnson's Third Quarter 2026 Earnings Conference Call. [Operator Instructions] This call is being recorded. [Operator Instructions] I will now turn the conference call over to Johnson & Johnson. You may begin.

**Ryan Koors** (Executives):
Hello, everyone. This is Ryan Koors, Vice President of Investor Relations for Johnson & Johnson. Welcome to our company's review of business results for the third quarter of 2026 and our financial outlook for the full year. First, a few logistics. As a reminder, today's presentation and associated schedules are available on the Investor Relations section of the Johnson & Johnson website at investor.jnj.com.
Please note that this presentation contains forward-looking statements regarding, among other things, the company's future operating and financial performance, market position and business strategy. You are cautioned not to rely on these forward-looking statements, which are based on the current expectations of future events using the information available as of the date of this recording. They are subject to certain risks and uncertainties that may cause the company's actual results to differ materially from those projected. The description of these risks, uncertainties and other factors can be found in our SEC filings, including our 2025 Form 10-K, which is available at investor.jnj.com and on the SEC's website. Additionally, several of the products and compounds discussed today are being developed in collaboration with strategic partners or licensed from other companies. This slide acknowledges those relationships.
Moving to today's agenda. Joaquin Duato, our Chairman and CEO, will discuss our business performance and growth drivers. I will then review the third quarter sales and P&L results. Joe Wolk, our CFO, will then close by sharing an overview of our capital allocation priorities and updated guidance for 2026. Tom Cavanaugh, Executive Vice President, Worldwide Chairman, Innovative Medicine; John Reed, Executive Vice President, Innovative Medicine, Research and Development; and Tim Schmid, Executive Vice President, Worldwide Chairman of MedTech, will be joining us for Q&A. To ensure we provide enough time to address your questions, we anticipate the webcast will last approximately 60 minutes. With that, I will now turn the call over to Joaquin.

**Joaquin Duato** (Executives):
Thank you, Ryan, and good morning, everyone. Our strong performance in the third quarter reinforces our confidence in 2026 as a year of accelerated growth and impact for Johnson & Johnson. In Q3, we reported operational sales growth of 6% ahead of analyst consensus and increased sequential growth compared to the second quarter. With 6 strategic focus areas: oncology, immunology, neuroscience, cardiovascular, surgery and vision, we are leading in areas of high unmet need where innovation can make the greatest difference for patients. Our powerful combination of Innovative Medicine and MedTech expertise strengthens our competitiveness. 29 of our products and platforms now generate at least $1 billion in annual sales.
Our marketed portfolio continued to perform. Our launches are gaining significant traction, and we are advancing our new product pipeline that will sustain our growth into the next decade. With sales in the quarter of more than $25 billion, we are on track to meet our guidance and exceed $100 billion in annual revenue for the first time in our company's 140-year history. As we advance our differentiated portfolio and pipeline, we have a clear path to double-digit growth by the end of the decade. In Innovative Medicine, we delivered operational sales growth of 7.9%, with 8 brands growing double digits. 
Let's start with oncology. We are making progress to redefine cancer care from treatment to cure. In the third quarter, our oncology business grew approximately 17%. Our multiple myeloma portfolio and pipeline are unmatched with 80% of patients receiving a Johnson & Johnson therapy as part of their treatment journey. And we continue to strengthen the body of evidence supporting our recently launched multiple myeloma therapies and combination regimens. New Phase III results announced in July demonstrated that the combination of TECVAYLI plus TALVEY reduced the risk of disease progression or death by 89% as early as the second line of treatment. In solid tumors, sales of RYBREVANT increased by 64%, reflecting its strength in lung cancer. And by the end of the year, we expect to receive U.S. FDA approval for RYBREVANT FASPRO in advanced head and neck cancer, a disease with significant unmet needs.
In bladder cancer, INLEXZO has rapidly emerged as a market leader for new patient share just 1 year after its launch. Nearly 1 in 3 eligible patients started on an INLEXZO regimen in the third quarter, demonstrating its growing role in transforming care in high-risk, non-muscle invasive disease. During the quarter, we also invested to bolster our oncology pipeline. We completed our acquisition of Firefly Bio, adding a promising new degrader antibody conjugate platform that targets drivers of difficult-to-treat cancers, including KRAS. Our ambition is to become the #1 oncology company by 2030, with sales projected to exceed $50 billion.
Turning to immunology. We are building on our 25-year legacy to drive industry-leading innovation for patients. TREMFYA delivered exceptional sales growth of 68% in the quarter, reflecting strong momentum across its indications. In the U.S., it is now the #1 IL-23 inhibitor in new to brand share in Crohn's disease, ulcerative colitis and psoriatic arthritis. And we continue to generate evidence that reinforces TREMFYA's clinical differentiation. Based on the landmark STAR study, TREMFYA is the first and only IL-23 inhibitor to demonstrate positive outcomes in axial disease clinical trials, including significant improvement in spinal pain, stiffness and inflammation in patients with psoriatic arthritis. This momentum reinforces our conviction in TREMFYA as a foundational medicine in inflammatory bowel and psoriatic diseases, and our belief that it can grow into a $10 billion-plus franchise.
ICOTYDE, our first-in-class targeted oral peptide for plaque psoriasis, continues to outpace the recent competitors' launches. More than 20,000 patients have initiated therapy through nearly 9,000 prescribers since ICOTYDE's launch in the U.S. We continue to make strong progress on commercial access, with ICOTYDE now broadly covered across all national plans. Also this quarter, IMAAVY was approved as the first advanced treatment specifically for warm autoimmune hemolytic anemia, a rare life-threatening disease that causes severe anemia and fatigue. This new indication builds on IMAAVY's momentum in generalized myasthenia gravis and reflects its broad potential across autoantibody diseases. And we continue to pursue next-generation therapies. In July, we announced a collaboration with Sail Biomedicines to advance in vivo CAR-T approaches for immune-mediated diseases. 
Next, in neuroscience, we aim to transform the future of brain health by addressing complex nervous system disorders. Today, we are the definitive leader in neuropsychiatry. CAPLYTA reached $1 billion in year-to-date sales, making it our 29th billion-dollar platform. Driven by strong uptake as an adjunctive treatment for major depressive disorder, CAPLYTA is now the fastest-growing oral branded therapy in this space. And last month, we presented pivotal Phase III data that show CAPLYTA significantly and rapidly improves symptoms of bipolar mania. SPRAVATO also delivered impressive growth of 36% this quarter, reflecting strong demand in treatment-resistant depression.
Now let's turn to MedTech, where we delivered Q3 operational sales growth of 2.5%. While we fell short of our expectations for the segment, our conviction in our future direction has not changed. Starting with cardiovascular, we continue to invest in heart recovery, circulatory restoration and heart rhythm disorders to address the leading global cause of death. This was another strong quarter for Shockwave, our circulatory restoration business, which grew 17%. The ongoing global launch of Shockwave C2 Aero continues to broaden the reach of our intravascular lithotripsy platforms.
VARIPULSE, our pulsed field ablation platform, reached a major milestone this quarter with more than 100,000 AFib patients treated worldwide. VARIPULSE Pro, which delivers 5 times faster ablation speed, has been very well received in Europe, where it is driving double-digit growth. And just last week, we received approval for VARIPULSE Pro in Japan. With increasing clinical experience, we are seeing differentiated benefits from VARIPULSE. In a recent retrospective analysis, VARIPULSE demonstrated a 68% lower risk of adverse cardiac events compared to a competing pulsed field ablation platform. And in heart recovery, while physician selectivity continued to affect Abiomed performance, we remain confident in the technology and focused on supporting appropriate patient selection.
In surgery, we are poised to shape the next era of care through robotics, digital innovation and advanced instrumentation. In July, the U.S. FDA granted De Novo authorization for OTTAVA, the world's first table-integrated soft tissue robotic system. This is one of the most significant MedTech innovations we will bring to market this decade. OTTAVA's unique architecture, automated features and next-generation robotic instruments help address surgeon needs for operating room space and better surgical workflows. Its connection to our open digital ecosystem, Polyphonic, turns procedure data into actionable insights for clinicians. We already signed our first commercial customer for OTTAVA, and we are progressing our development program. Our investigational device exemption trial is already underway in inguinal hernia repair, with future plans for indication expansion into urology and gynecology. 
Finally, in vision, we are advancing lifelong eye health to bring better sight to more than 40 million people each year. The recent U.S. launch of TECNIS PureSee further strengthened our portfolio of intraocular lenses. During the quarter, TECNIS PureSee and TECNIS Odyssey surpassed 1 million implants worldwide, reflecting continued surgeon adoption and our leadership in personalized vision solutions. We also received CE marking for ACUVUE OASYS MAX 2-Week reusable lenses, expanding our ACUVUE portfolio in Europe.
Overall, this quarter's strong results demonstrate the impact of the choices we have made to build a foundation for durable growth. We sharpened our portfolio to focus on innovation with the greatest potential to change lives. We proved our ability to grow through a significant loss of exclusivity. Our strategic investments in high-growth areas are delivering results, and our innovation engine continues to drive breakthroughs for patients. That is why we have the confidence to say that we will finish 2026 strong and that 2027 will be an even better year for Johnson & Johnson. I will now turn the call back over to Ryan.

**Ryan Koors** (Executives):
Thank you, Joaquin. Moving to our financial results. Unless otherwise stated, the percentages quoted represent operational results and therefore exclude the impact of currency translation. Starting with Q3 2026 sales results. Worldwide sales were $25.4 billion for the quarter, increasing 6%. Growth in the U.S. was 9.1% and 1.8% outside the U.S. Acquisitions and divestitures had a net negative impact on worldwide growth of 10 basis points.
Now turning to earnings. For the quarter, net earnings were $210 million and diluted earnings per share were $0.09 versus $2.12 a year ago. Results in the quarter were impacted by the proposed talc litigation resolution as well as expenses associated with the Firefly Bio transaction and Sail Biomedicines collaboration amounting to approximately $7 billion. Adjusted net earnings for the quarter were $6.3 billion, and adjusted diluted earnings per share were $2.59, representing a decrease of 6.8% and 7.5%, respectively, compared to the third quarter of 2025. Adjusted earnings in the quarter were also impacted by expenses associated with the Firefly Bio transaction and Sail Biomedicines collaboration.
I will now comment on business sales results in the quarter, focusing on the 6 key areas where meaningful innovation and strong commercial execution are driving our performance and fueling long-term growth. Beginning with Innovative Medicine, where our financial results reflect the depth of our expertise and innovation in areas of high unmet need across oncology, immunology and neuroscience. Worldwide sales of $16.8 billion increased 7.9%, which underscores the continued strength of our key brands and new launches. Growth in the U.S. was 11.1% and 3% outside the U.S. Divestitures had a negative impact of 10 basis points on worldwide growth.
In oncology, starting with multiple myeloma, DARZALEX growth was 15.6% primarily driven by strong share gains of 5 points across all lines of therapy with 10 points in the frontline setting as well as continued market growth, partially offset by OUS pricing headwinds. CARVYKTI achieved growth of 35.2%, driven by share gains across earlier lines of therapy and continued site expansion. TECVAYLI growth was 77.3%, driven by launch uptake and share gains across earlier lines of therapy following last quarter's approval in the U.S. for TECVAYLI plus DARZALEX FASPRO, with U.S. growth greater than 100%. 
TALVEY growth was 42.1%, driven by share gains due to increased depth of prescribing in the community setting. In lung cancer, RYBREVANT plus LAZCLUZE delivered growth of 63.5%, with strong share gains in the first and second lines driven by continued launch uptake in all regions, along with rapid uptake in RYBREVANT FASPRO. In prostate cancer, ERLEADA delivered growth of 9.4%, with continued share gains and market growth partially offset by unfavorable patient mix. 
Within immunology, TREMFYA delivered impressive growth of 68.2% driven by continued momentum from the IBD launch, with 4 points of share growth in both ulcerative colitis and Crohn's disease alongside continued market growth. STELARA declined 54%, which reflects continued competitive pressures from biosimilars and the ongoing shift towards novel classes. Growth in other immunology is driven by IMAAVY and ICOTYDE launch uptake in the U.S. 
In neuroscience, SPRAVATO grew 36%, driven by continued share gains reflecting strong physician adoption and increased patient demand. CAPLYTA showed significant growth of 66.1%, driven by strong continued launch momentum in adjunctive major depressive disorder and continued demand increases across bipolar disorder and schizophrenia.
Now moving to MedTech. Worldwide sales of $8.6 billion increased 2.5% with growth of 4.8% in the U.S. and 0.1% outside the U.S. Overall cardiovascular grew 4.1%, including 20 basis points related to acquisitions. Electrophysiology delivered growth of 4.4%, driven by procedure expansion, commercial execution and new product performance, partially offset by competitive PFA pressures, which were more pronounced in AsPac this quarter as well as the lapping of prior year OUS inventory dynamics. 
Abiomed saw a decline of 1.5% due to lower patient volume. There are encouraging signals in the U.S. performance with improvement in the quarter, supported by acute myocardial infarction, cardiogenic shock and Impella 5.5 continuing to gain adoption. Shockwave grew double digits at 17.2%, driven by continued adoption of coronary and peripheral products as well as new product launches and the reimbursement in the office-based lab setting within the U.S. 
Surgery saw a decline of 1%, including a negative impact of approximately 30 basis points from divestitures. The decline is more notably driven by ongoing expansion of VBP in China, surgery transformation program outcomes across the portfolio and Middle East disruption, which impacted tender timing and ordering patterns. The decline was partially offset by portfolio strengths, driven by recent innovations such as ETHICON 4000 and DUALTO as well as commercial execution in biosurgery. 
In vision, growth was 5.1%, driven by premium innovation, strong execution and global reach. Contact lenses and other products grew 4.3%, driven by strong performance in the ACUVUE OASYS 1-Day family of products, further solidifying our leadership position, partially offset by U.S. inventory dynamics. Surgical vision delivered growth of 7.1%, driven by new product innovations, robust demand for premium IOLs and strong commercial execution, partially offset by market-specific factors such as disruptions in the Middle East. 
Orthopedics growth for the quarter was 3.4%, primarily driven by new product launches such as VOLT in trauma and EMPHASYS in hips, including strong commercial execution in VELYS pull-through in knees.
Now turning to our consolidated statement of earnings for the third quarter of 2026. I'd like to highlight a few noteworthy items that have changed compared to the same quarter of last year. Cost of goods sold deleveraged by 150 basis points, driven by unfavorable product sales mix and increased intangible asset amortization expense in the Innovative Medicine segment for Intra-Cellular, partially offset by the impact of tariff recoveries in the MedTech business.
Selling, marketing and administrative expenses were flat as a percent of sales, reflecting consistent commercial investments in the Innovative Medicine business. We continue to invest strategically in research and development, deploying approximately $4.7 billion or 18.3% of sales, which includes $1 billion related to the acquisition of Firefly Bio. In-process research and development impairment costs of $339 million in the quarter is related to the write-off of preCARDIA, a noncore asset acquired as part of the broader Abiomed transaction.
Other income and expense was a net expense of $5.8 billion as compared to $478 million of income in the third quarter of 2025, with the change primarily driven by the proposed talc litigation resolution and orthopedic separation-related costs. The tax rate was a small net benefit in the quarter, primarily related to the positive tax effect associated with the accrual for the proposed talc litigation resolution. More information can be found in our upcoming 10-Q for changes in taxes.
Lastly, I'll direct your attention to the box section of the slide where we have also provided our income before tax, net earnings and earnings per share adjusted to exclude the impact of intangible amortization expense and special items. Now let's look at the adjusted income before tax by segment for the quarter. Innovative Medicine margin declined from 44.3% to 35.4%, primarily due to acquired in-process research and development expense of approximately $1 billion related to the acquisition of Firefly Bio, transaction costs for Sail Biomedicines, and unfavorable product sales mix and cost of products sold.
MedTech margin increased from 21% to 22.9%, driven by the impact of tariff recoveries, partially offset by increased strategic investments in commercial capabilities. As a result, adjusted income before tax for the enterprise as a percentage of sales decreased from 35.2% to 30.2%. This concludes the sales and earnings portion of the call, and I will now turn the call over to Joe.

**Joseph Wolk** (Executives):
Thanks, Ryan. Hello, everyone, and thank you for joining us today. As you heard from Joaquin and Ryan, our third quarter results were driven by the strength of our Innovative Medicine business. This performance more than offset headwinds in certain areas of MedTech, enabling us to exceed expectations on both the top and bottom line while continuing to invest in our pipeline and future growth. We are clear on where MedTech performance needs to improve, specifically cardiovascular and surgery outside the U.S. and are taking action to strengthen results. 
While disappointing, the underlying fundamentals of the MedTech business remain strong, supporting our confidence in the long term for that business. Across Johnson & Johnson, the drivers underpinning our outlook remain firmly in place. As a result, we are raising our guidance for 2026 versus our most recent update in July. The depth of our portfolio, momentum from new product launches and upcoming pipeline catalysts further reinforce our conviction in achieving double-digit growth by the end of this decade, with sustainable growth beyond.
Turning to financial metrics and our cash position. We ended the third quarter with approximately $17 billion of cash and marketable securities and approximately $45 billion of debt for a net debt position of approximately $28 billion, generating more than $6 billion in free cash flow in the third quarter. We remain confident in our full year free cash flow guidance of approximately $21 billion. During the quarter, we completed the $1 billion acquisition of Firefly Bio, deepening capabilities in oncology with next-generation antibody engineering to address complex tumor biology. As Joaquin referenced earlier, we also entered into a collaboration with Sail Biomedicines to advance in vivo CAR-T therapies for immune-mediated diseases. 
Our disciplined approach to capital allocation is principled on prioritizing investments that support key commercial launches, accelerating future innovation, increasing our annual dividend and strengthening our pipeline through strategic value-creating inorganic opportunities. In July, we announced an agreement for a resolution of the ovarian talc litigation for $5.5 billion, which is reflected in our third quarter GAAP results. The agreement is conditioned upon the express participation of at least 95% of the remaining ovarian claims. We are trending to meet the 95% threshold.
Let me now turn to full year 2026 guidance. As always, our outlook reflects what we know today regarding foreign exchange rates, the broader macroeconomic environment and other external factors. Based on our year-to-date performance and expectations for the fourth quarter, we are raising the midpoint and tightening the range of our operational sales guidance. We now expect full year operational sales growth in the range of 6.7% to 7.1%, which represents operational sales of $100.7 billion at the midpoint or growth of 6.9%. We do not speculate on future currency movements. As of last week, the euro spot rate to the U.S. dollar was $1.12. However, the average rate for the fiscal year stands at $1.15. Based on that average rate, we estimate reported sales growth of 7.2% to 7.6%, with a midpoint of $101.2 billion or 7.4%. Assuming the current spot rate holds into next year, you could expect currency to be a headwind.
Turning now to other items of the P&L. Regarding operating margin, we now expect a decline of approximately 60 basis points. This is an improvement from the 75 basis points decline reflected in our updated July guidance that included the impact of the Firefly Bio and Sail Biomedicines transactions, which had an unfavorable impact of 150 basis points. Absent those deals, we continue to deliver base margin improvement. As a reminder, our pretax adjusted operating margin outlook also reflects the costs associated with the 53rd week of operations and our previously announced agreement with the U.S. government to improve access to medicines.
For net interest expense, we are lowering our guidance to $150 million to $200 million. We are also tightening the range of our effective tax rate guidance. Based on our year-to-date results, we now expect a full year effective tax rate of 17.0% to 17.5%. Given those updates, we now expect adjusted operational earnings per share in the range of $10.95 to $11.05 or 2% at the midpoint. We expect reported adjusted earnings per share of $11.05 to $11.15 with a midpoint of $11.10 or growth of 2.9%. Excluding the impact of Firefly Bio and Sail Biomedicines transactions of $0.64, reported EPS growth would approach 9%. As a reminder, for your 2027 modeling, we expect Firefly Bio and Sail Biomedicines to have a combined dilutive impact of $1.36 per share on a full year adjusted earnings per share next year. We will provide more details on our 2027 outlook later this year at our enterprise business review. 
Let me now highlight several upcoming developments that reinforce our growth outlook and performance for the remainder of the year. In oncology, we expect several important data readouts in the fourth quarter. These include data for pasritamig, a first-in-class bispecific antibody in patients with advanced prostate cancer who have progressed after multiple lines of therapy. We also expect data for JNJ-6143, an investigational first-in-class, once-daily oral therapy for metastatic castration-resistant prostate cancer. We continue to see strong adoption for INLEXZO with year-to-date sales of approximately $200 million and expect to build on that momentum with a data readout in high-risk non-muscle invasive bladder cancer later this year. We also expect U.S. approval of RYBREVANT FASPRO in advanced head and neck cancer.
In immunology, as Joaquin referenced earlier, ICOTYDE is off to a strong start and we look forward to presenting data in psoriatic arthritis later this year. In MedTech, we expect U.S. approval of VARIPULSE Pro in the fourth quarter, further complementing last week's approval in Japan. In heart recovery, we are taking corrective action to improve Abiomed's performance. We continue to invest in clinical evidence and expect results from the HRPCI PROTECT IV trial in 2027. The trial will have 1,252 patients, 4 times more than the CHIP-BCIS3 study. This large-scale study will evaluate the safety and efficacy of Abiomed's Impella CP pump during high-risk percutaneous coronary intervention.
In surgery, we are focused on commercializing OTTAVA following its recent FDA De Novo authorization. We expect adoption and revenue contribution to build over time, with the goal of establishing OTTAVA as a significant pillar of our surgery portfolio by the end of the decade. Regarding orthopedics, we remain on track for the planned separation of DePuy Synthes by mid-2027. I'm really proud of the team working to evaluate all separation vehicles and all options are better positioned today than when we announced our intentions with this business. Given the way DePuy Synthes is performing and the momentum Namal Nawana and his team are generating, we are leaning towards a spin as being the best option to create long-term value for Johnson & Johnson shareholders. That has always been our base plan, and we are confident that it can be successfully executed. We will provide additional updates as appropriate and when there is more information to share.
Finally, I am really looking forward to and hope you join us for the Enterprise Business Review on December 8. At that event, we will provide additional perspective on our 2027 outlook and the key drivers that reinforce our conviction in achieving double-digit growth by the end of the decade. Perhaps more importantly, we will highlight our earlier-stage pipeline and how it represents the next wave of growth into the next decade. Attendees will also have the opportunity to experience firsthand some of our latest innovations, such as OTTAVA. 
2026 is on track for another successful year, exceeding expectations set at the beginning of the year. We look forward to closing out 2026 strong and setting up 2027 for continued success. Thank you to our colleagues whose dedication and commitment continue to advance innovation, improve patient outcomes and create long-term value for shareholders. With that, we are ready to answer your questions. Kevin, can you please open the call for Q&A?

**Operator** (Operator):
[Operator Instructions] Our first question today is coming from Asad Haider from Goldman Sachs.

**Asad Haider** (Analysts):
And congrats on all the progress. Just one point of clarification. On the double-digit growth by the end of the decade, the vocabulary in the press release references the progress in the underlying business, "Together with strategic investments." Just want to be clear that, that refers to internal investments and not M&A. That's a question we're getting this morning. And then, Joe, on your comments that you aren't satisfied with MedTech performance and are taking action to strengthen that growth, is the implication there that you now feel more urgency to add to higher-growth areas via M&A in MedTech? Or do you think that you have the product portfolio today to drive the improved performance you're looking for?

**Joseph Wolk** (Executives):
Yes, Asad, thank you for your questions. On the first aspect, that is correct. Your interpretation of that being internal strategic investments is what will propel us to double-digit growth by the end of this decade, in the coming years with increasing performance. So that is the correct interpretation. It does not assume any inorganic additions at this moment in time. We always are on lookout for strategic drivers that could complement our business that makes sense to be in our hands versus where the asset would currently reside, but also creates value for the risk we're bearing on behalf of shareholders. With respect to the urgency, it's an urgency to fix what we currently have. We like the portfolio and the construct that currently exists with the 3 focus areas of vision care, of surgery as well as cardiovascular.
I think you're very familiar, and maybe I'll even hand it over to Tim to talk about some of the things we're doing in heart recovery specifically, to address that, what I would say is now a stable business, but we want to catalyze back to double-digit growth. We're very excited what's on the horizon for surgery with the addition of OTTAVA over time. That will be a significant contributor to growth by the end of the decade. And then, as I mentioned earlier, vision seems to be functioning well both on the surgery side as well as the contact lens side, where we are the market leader. But Tim, maybe you want to offer a comment or 2 around Abiomed?

**Tim Schmid** (Executives):
Sure, Joe. So Asad, ultimately, Abiomed remained in a temporary headwind, as you saw in Q3, but our conviction in the long-term opportunity has not changed at all. The slowdown we're seeing continues to be the same issue we highlighted in the quarter before, which is this study outside of the U.S. focused on high-risk PCI. And importantly, we do not view these challenges as structural in nature, and one that will drive a long-term impact on the business. We're not seeing any changes in the patient need nor to reimbursement access or any meaningful competitive pressures. We also have highlighted some questions we have around the study as to whether best practices were used in the study, and so our focus today is really on education and advancing the clinical evidence base to show the incredible impact that Impella has in both saving and improving lives. And so we believe it's a short-term headwind.
It's important to recognize that in any emerging area of science, there's always going to be debate and discussion, and our responsibility is to continue to advance the evidence base to support what's in the best interest of patients. And in the case of Abiomed, we're doing exactly that. And so a short-term headwind, but we are very confident this is going to be a strong platform for growth for Johnson & Johnson for the future.

**Operator** (Operator):
Next question today is coming from Larry Biegelsen from Wells Fargo.

**Larry Biegelsen** (Analysts):
Joe, I wanted to ask about the 2027 comments you made at Deutsche Bank. On the top line, you said you expect reported sales growth to be similar to 2026 after adjusting 100 basis points for the extra week in both years, which I think would mean about 5.4% reported growth next year. And on EPS, how should we think about your ability to grow earnings excluding IPR&D? And just remind us of how much the Firefly and Sail dilution is IPR&D this year and next year?

**Joseph Wolk** (Executives):
So for this year, the IPR&D dilution is $0.64. And for next year, the combination of those deals is $1.36. And the way I would think about that, Larry, and you've covered us long enough where you know that typically our income growth or our EPS growth will be a little bit better than our sales growth. That's how you can think about that next year after adjusting for the $1.36 adjustment. So we'll continue to look at margin improvement as part of the orthopedic separation, looking more holistically at our business. 
Some of the advances we're getting with technology and getting us more efficient across all parts of our business, but that's probably a good way to kind of frame in your thinking now for 2027. But we'll be a little bit more explicit on December 8 at our Investor Day. We will outline specifically kind of the components to that, and then even probably provide a pro forma with respect to the orthopedic separation should that occur at some point next year as well as a longer-term outlook.

**Operator** (Operator):
Our next question is coming from Chris Schott from JPMorgan Chase.

**Christopher Schott** (Analysts):
Just wanted to touch base on ICOTYDE. So just 2-part question here. First, can you just give us an update in terms of what you're seeing in terms of patient uptake as we think about new to biologic versus oral switches versus injectable switches? And then bigger picture for the drug. You're talking about this as a $10 billion-plus asset, but when you think about this very strong launch we've seen so far in psoriasis, you got a number of additional indications pending. I guess, how do you think about -- could this be a much larger asset than $10 billion as you think about the peak sales opportunity for ICOTYDE?

**Tom Cavanaugh** (Executives):
Great. Chris, it's Tom. Good to hear from you. First, I do want to start by recognizing Jennifer Taubert and thanking her for her tremendous leadership and partnership. Jennifer leaves Innovative Medicine incredibly well positioned, as you see from our quarterly earnings, with strong momentum, outstanding portfolio and pipeline, and most importantly, a great team. We're fortunate to build on that foundation she established, and I'm excited about what's ahead. And really, what I'm excited about is what you're touching on right now is ICOTYDE. We do foresee ICOTYDE to be one of our biggest assets in Innovative Medicine, and it is off to an incredibly great start. 
As you highlighted, and as Joaquin highlighted on the call this morning, I think getting into some of the launch performance, you heard it from Joaquin already to date, we've seen over 20,000 patients initiated on therapy with over 8,000 prescribers or nearly 9,000 prescribers, I would say. So absolutely tracking better than some of most all launches in psoriatic diseases. I think early prescribing trends is what you wanted to get at, kind of as we think about -- and we are expanding the systemic marketplace. Approximately 60% of the patients are systemic naive, so they haven't received any systemic therapy. And roughly the 40% remaining, 20% are sourced from orals and 20% are sourced from other treatments, most likely biologics as we dig into the data.
So I can say, as you're seeing with regards to the launch performance earlier, a bit expansion of the marketplace and absolutely an opportunity to continue to drive that. Highlighted as well, as Joaquin highlighted earlier, I think it's important to point out, we do have broad commercial access now and preferred access in place on all national commercial plans are actively engaged to expand that to the Medicare population. So I would say we're fairly -- very excited about the launch to date as equally as excited about the future. And we do foresee this to be one of our largest assets. As I pointed out, we're excited about the upcoming data readouts, both with the PsA and Phase III data as well as the head-to-head STELARA data for ASCEND that we should be releasing in the coming months. And as we look to expand beyond that, and we'll get into more of this at the EBR in IBD and expansions into UC and CD, expecting similar results with regards to launch performance as we go into those other indications.

**Operator** (Operator):
The next question is coming from Joanne Wuensch from Citi.

**Joanne Wuensch** (Analysts):
I want to focus a little bit on MedTech here. When you use the phrase underlying fundamentals in MedTech are solid, I want to confirm that you're thinking about all the good stuff, the patient volumes, the CapEx spending from the hospitals, and then what you're seeing in terms of just general flows. And then as a sister question to that, how do you -- or what do you think needs to be done to improve the J&J franchise?

**Tim Schmid** (Executives):
Joanne, it's Tim. Thank you very much for the question. Let me start by really putting the overall MedTech Q3 results in context for you and all on the call. And to be clear, our performance is below the standard we have set internally and below the expectations we previously communicated to investors. Simply put, we can do better and we absolutely will. And right now, we are focused solely on the actions needed to deliver stronger results in the fourth quarter and beyond. And that said, when -- to your question, when we break down our results, you will see that the pressure was primarily concentrated actually in 2 very distinct areas.
Firstly, our performance outside of the U.S. And secondly, Abiomed globally, which we already touched on. And to put it in perspective, growth in the U.S., which, as you know, is the most important market, was in fact robust in the quarter and accelerated to almost 5%. Our performance outside of the U.S. was a challenge, and it reflected a combination of mostly known headwinds, which we have discussed previously. For example, in surgery, the expected impact of the transformation program and the ongoing expansion of volume-based procurement in China. In electrophysiology, competitive intensity, especially in Asia Pacific, which is a region that you know is still relatively early in the adoption of PFA. We did introduce a new headwind, which is really the incremental pressure that we're seeing on the business due to the conflict in the Middle East.
But when you actually step back and you look deeper into these results, we're seeing several encouraging indicators which give us confidence in a stronger Q4 and outlook beyond that. For example, in electrophysiology, in markets like Europe, where we've already launched VARIPULSE Pro, which, by the way, is a faster and easier-to-use catheter, we're back to double-digit growth. And we will launch VARIPULSE Pro in Japan shortly after receiving regulatory approval last week. You can also anticipate a U.S. launch by the end of this year.
I think at Abiomed, we've already touched on the study in high-risk PCI, a study where we actually believe that the methodology employed did not follow well-established practices, an issue which we're addressing through education. We think we're going to get through that because the evidence base is so solid, especially in areas like AMI cardiogenic shock, and we're still seeing tremendous performance of 5.5. We did, by the way, already see some improvement sequentially throughout the quarter, and we do believe that, that business will be back to growth in short order.
Now, while Q3 for MedTech was not a strong quarter, this should not distort the whole picture. As mentioned, the issues are primarily concentrated in the 2 areas I mentioned. It's also worth reinforcing to your question that the underlying procedure environment remains stable across our key markets. I know there has been a lot of debate about that. Our job now is to make sure that we convert that demand into more consistent performance. And so we remain confident in the combination of the momentum we're seeing in the U.S. and the moderation of these near-term headwinds, which will support improved performance in Q4 while positioning us for stronger performances in 2027 and beyond. And as you've already heard from Joaquin and Joe, we'll share more detail around what that looks like for '27 and beyond, specifically with a focus on new innovations like OTTAVA when we come together on December 8.

**Operator** (Operator):
Next question today is coming from Jason Gerberry from Bank of America.

**Richard Wagner** (Analysts):
This is Richard Wagner for Jason. I had a question regarding the ICOTYDE psoriasis launch. Are there lessons that can be learned that would be useful when ICOTYDE launches in IBD? Specifically, in IBD, competitors are developing high-efficacy combination programs and wondering how that could affect the efficacy perception by physicians of ICOTYDE.

**Tom Cavanaugh** (Executives):
Richard, this is Tom addressing your question. A couple of things I'd point out, and I'd obviously turn it over to John if he has any further remarks with regards. I'll say a couple of things. We absolutely know the space very well, whether it be in psoriasis or IBD. And you could tell by the launch that we had with TREMFYA in IBD, it's off to an incredibly great start. As you can see, over 70% growth year-over-year and heavily penetrated in becoming the -- actually the fastest-growing biologic across all indications, in particular, in IBD new patient starts. So we know the space very well.
With that said, I will say there's still significant unmet need in a large amount of patients that are untreated or not treated earlier in the course of their diseases. And we do see that to be a great opportunity for not only market expansion as we're seeing in psoriatic disease or psoriasis with ICOTYDE, but the profile of the product fits beautifully in that spot, I would say. And obviously, the data will depend on how we look at it in the positioning once it becomes on the marketplace. But I will tell you, we'll have early access as one of the other keys, and we'll see rapid uptake once we get the data results. John?

**John Reed** (Executives):
Yes, maybe just to build on that a little bit. I think the reason that we've had such a great start in psoriasis is because of that trifecta biologics-like efficacy, coupled with placebo-like safety, combined with the convenience of a once-a-day pill, and we think that will play very well across all indications, including IBD, where, as Tom referenced, still a large percentage of patients are not on an advanced therapy.
The data in our Phase II study were quite encouraging and look like ICOTYDE can deliver on par with the current monotherapies. Of course, we're very aware that some patients need something more that they need a combination therapy, and that's why we're developing 4804, which pairs our guselkumab, our IL-23 inhibitor, with golimumab, our TNF inhibitor, and that is in Phase III studies now after really compelling Phase II data that show that in that refractory population that have failed 2 or more prior advanced therapies. This really delivers superior efficacy to the monotherapy. So we're actively pursuing that for those patients where monotherapy is not enough and could see then that opportunity to migrate patients if needed beyond the monotherapies to the dual therapies with our co-antibody therapeutic 4804.

**Operator** (Operator):
Our next question is coming from Vamil Divan from Guggenheim Securities.

**Vamil Divan** (Analysts):
Great. Maybe one just follow-up and then one actual question. Following up on the ICOTYDE. I appreciate the comments you've made so far. Just curious if you would be willing to provide any commentary around the actual net sales in the quarter or kind of how it compares to where consensus was. We're just getting some questions from investors on that specifically. And then my other question is just around INLEXZO, so I appreciate the comments there you made around the sales so far. I'm wondering if you can just quantify, I know you have the data coming up later this year as well, how you see the market opportunity for that expanding based on the current indication? And then what sort of the SunRISe-5 data, what's the size of that opportunity is relative to what you have currently?

**Tom Cavanaugh** (Executives):
Yes. Obviously, we haven't disclosed any sales for ICOTYDE, but I'm confident we're going to be doing that next year, just based on the momentum and the progress that we're seeing with the launch of ICOTYDE. Turning over to INLEXZO, also another exciting product that we have or even a platform as we think about TAR-210 as well, and the opportunity that exists for us. We're off to an incredibly great start. Joe disclosed that we're nearly $200 million in net trade sales for year-to-date. And quite honestly, we haven't reported quarterly sales, but I could say that Q3 was north of $90 million. So we're seeing great sequential growth. This quarter, we saw new patient inserts grow 45% versus the previous quarter. And I wanted to point out that this is in a population in non-muscle invasive bladder cancer, high risk with carcinoma in situ. It represents roughly 4,000 patients in totality, so relatively small in nature. And we're still seeing 1 in 3 patients being put on INLEXZO in this patient population.
You touched on SunRISe-5, which is a broader patient population, roughly 15,000 patients, and what we call SunRISe-3, which is the BCG naive population, roughly 50,000. This is where we absolutely see a greater opportunity for us to live into the number of $5 billion-plus for the platform, and I do believe we will do just that and above that given the unmet medical need, the simplicity of INLEXZO delivers and high response -- high durable complete remission rates that we are delivering with INLEXZO as we look to expand in the population. Maybe I'll turn it to John to touch on a little bit of the clinical development program.

**John Reed** (Executives):
Indeed. As you know, the approval currently is for the CIS type of nonmuscle-invasive bladder cancer, which spreads laterally. But the more common is the papillary, and in our so-called SunRISe-1 study, we had a cohort devoted to patients with papillary cancers where those lesions which project outward from the bladder wall are excised by the urologist and then INLEXZO is applied, and one tries to prevent recurrence. And we show nearly 75% of patients had no recurrence after 1 year, and that over 95% had no progression of their disease. In other words, they did not progress to more invasive types of disease. So based on that, the use of INLEXZO in that papillary form of the disease, which is by far the more common, is already in the NCCN guidelines, and the FDA has invited us to submit for an expansion of our label into that population.

**Joaquin Duato** (Executives):
Both ICOTYDE and INLEXZO are going to be, together with RYBREVANT, key drivers of our growth acceleration, driving to double-digit growth. So they will become one of our largest products, both of them.

**Operator** (Operator):
Our next question is coming from Michael Yee from UBS Securities.

**Michael Yee** (Analysts):
Maybe 2 pipeline science questions. On ICOTYDE, obviously you have great data in psoriasis, a little bit lower than biologics, but great data. In IBD, the UC data was quite strong. I'm just wondering if you think that would be replicated to biologic-like efficacy as an oral, and that differentiation there due to the release in the gut is a reason for the potentially stronger data in IBD, which could be a bigger driver. Second part question is on milvexian. I know you share in that partnership, but SSP data is coming up, and I just wanted to check in on your confidence that, that should be similar to asundexian, and that should be a fairly derisked indication as a Factor XI.

**John Reed** (Executives):
John Reed here. Thanks for your questions. I'll start off, and then maybe Tom will want to supplement. But on ICOTYDE and IBD, we get that question all the time, asking might we see even greater efficacy with an oral because of the gut absorption. All I can say is to be determined. We were quite pleased with the Phase II data in ulcerative colitis.
I would also say the Phase III studies, as we saw with our psoriasis and psoriatic arthritis studies, are enrolling briskly. In the prior studies, they enrolled in about 1/3 the time that it normally takes us to enroll in those indications, reflecting, I think, the real enthusiasm that both physicians and patients have for this oral option. So that theory about oral absorption and improved efficacy to be determined by the data.
Moving to milvexian. We remain confident in the studies underway, particularly with the secondary stroke because of the asundexian data. As we know, in vitro, milvexian is a more potent inhibitor of Factor XI. We also have been able to have a safety margin that allows us to push that dose to ranges that we're confident are quite effective. So we remain confident in the results and expect that perhaps the secondary stroke data will be available even this year. It's event-driven, the study. The atrial fibrillation, the larger population, will be next year.
It will be exciting for us if we can prevail in both those indications because about 25% of patients who are candidates for secondary stroke have atrial fibrillation. That's probably why they had the stroke in the first place. And so if we can benefit both of those populations, that will be exciting. We are confident in the atrial fibrillation study as well. There, we were able to push the dose 4 times higher, given our safety margin in the drug, and feel from monitoring of the anticoagulation status of the blood with laboratories, that we're in the right range to benefit patients and prevent thrombosis. So thank you for the question.

**Tom Cavanaugh** (Executives):
Yes, I'd just reinforce what John has said. There's an absolute need for highly effective oral anticoagulation therapy with a reduced bleeding risk. In AFib alone, approximately 40% of the patients eligible for oral anticoagulants are not receiving oral anticoagulants, typically due to the concerns on potential safety and the bleeding risk associated with the current DOACs.

**Operator** (Operator):
Our next question is coming from Jayson Bedford from Raymond James.

**Jayson Bedford** (Analysts):
Just I want to go back to the international MedTech business. Is there any way to quantify the impact of the dynamics in the Mid East and VBP? And then, Tim, I wanted to ask about international surgery. First, just to confirm your view, is that there's been no change to the underlying demand profile internationally? And then second, I think Joe mentioned taking actions internationally for surgery. What are those actions?

**Tim Schmid** (Executives):
Thank you, Jayson. Let me try to get to all of those. Let me start with the Middle East, and clearly we've highlighted that as a new risk that has broadened over time. And really, the effect is no longer limited to a handful of markets as we initially thought. We've seen increased disruption to ordering patterns, tender timing and hospital spending decisions across a wider group of countries, unfortunately. And we've also seen governments and health care systems become more cautious in their spending priorities, with some funding and procurement decisions taking longer than what we normally would expect.
That has created a more meaningful impact on purchasing behavior than we saw earlier in the year. That said, I think it's important that we see this really as a short-term factor. I mean the underlying issues have not changed. The clinical need remains intact, and we'd expect many of these opportunities to be deferred rather than permanently lost. I think that's an important factor as it relates to any form of conflict and certainly what we're seeing in the Middle East.
On surgery, as I mentioned, we're actually really excited about the performance of the business in the U.S. Our issue really was outside of the U.S. And as you know, primarily driven by factors we've discussed before, such as the transformation program and volume-based procurement. And then, of course, the incremental pressure that we've just mentioned throughout the Middle East. I will say that despite those headwinds, we're focused on where we can have an impact, and we have a lot of opportunities. Wound closure growth continued to benefit. This is a category where we absolutely dominate, and that growth has been driven by innovation such as STRATAFIX and Plus Sutures. Biosurgery, another north of billion-dollar platform, delivered solid growth driven by key brands like SURGIFLO, SURGICEL and VISTASEAL. And we continue to see good traction with our endomechanical innovation, such as ETHICON 4000 and DUALTO. And so we are confident that we will see continued growth in the U.S.
And to your question, we will see acceleration in EMEA and return to growth overall in the fourth quarter. I do think it's also worth mentioning our confidence in this business going forward. This was the core to how we started Johnson & Johnson MedTech, and we are absolutely committed to it for the long term. I'd say the biggest reason for confidence is the fact that we will be entering the surgical robotic space and combined with our leadership positions across wound closure, biosurgery and advanced instrumentation, we believe that OTTAVA gives us an opportunity to participate more fully in one of the most attractive and underpenetrated areas of surgery. 
And so as we continue to execute our portfolio transformation, advance innovation across the existing business and prepare for the launch of OTTAVA, we remain confident in the long-term trajectory of the surgery franchise. We do get a lot of questions on OTTAVA, and rest assured that when you come together for the meeting on December 8, we will provide perspective on the outlook for that innovation and further build your confidence in what we believe will be a material contributor to Johnson & Johnson's growth over the long term.

**Operator** (Operator):
Our final question today is coming from Alex Hammond from Wolfe Research.

**Alexandria Hammond** (Analysts):
So I guess as the CARTITUDE-5 and 6 trials have advanced in newly diagnosed multiple myeloma, how is J&J preparing to educate physicians and treatment centers for the potential shift to use it earlier into the treatment journey? And I guess how should investors think about potential to capture share from these existing frontline regimens?

**Tom Cavanaugh** (Executives):
Alex, it's Tom. Thanks for the question. I think first and foremost, yes, we're anxiously awaiting for those trials to read out. I would say we're already doing that right now with CARTITUDE-4 across the globe. CARTITUDE -- CARVYKTI is available in over 20 markets, and we're seeing substantial share growth in the earlier line settings. And I would say roughly in the U.S., 50% of the utilization of CARVYKTI lies in lines 2 and 3. So there's becoming more familiarity with the product and access to the product and excitement about it, predominantly due to the unmatched overall survival as early as line 2 of therapy that we've seen versus standard of care. So we're already educating health care providers on the product and how they can utilize it earlier. Some of the education that is centered around is appropriate patient selection, and the earlier the better, as well as proper bridging, getting the patients to the highest level MRD negativity to be effectively treated with CARVYKTI.

**John Reed** (Executives):
Maybe just to remind on top of that, that at the recent myeloma meetings, we showed 5-year follow-up data from the CARTITUDE-2 study that's in second line, showing that about half of those patients enjoyed complete remission out to 5 years with no further treatment. So a one and done in 5 years of continued disease-free survival. So very exciting data.

**Ryan Koors** (Executives):
Great. Thank you, John, and thank you, Alex, for the question. And thanks to everyone for your questions and continued interest in our company. I will now turn the call over to Joaquin for some brief closing remarks.

**Joaquin Duato** (Executives):
Thank you for your questions and your engagement in today's call. As you can see, we continue to build momentum. Growth improved sequentially in the third quarter, and we expect further acceleration in 2027 with a clear path to double-digit growth by the end of the decade. In Innovative Medicine, growth will come from both our existing portfolio, including DARZALEX and TREMFYA, and newer products such as ICOTYDE, RYBREVANT and INLEXZO, as they begin to contribute more meaningfully. We see similar opportunities in MedTech, the potential from our cardiovascular launches, including next-generation PFA and IVL catheters. Additional data supporting Impella and OTTAVA in robotic surgery are not yet fully reflected in our growth. Taken together, these drivers position Johnson & Johnson as one of the cleanest growth stories in health care. We will provide more details about our portfolio and later-stage pipeline at our Enterprise Business Review later in December. Thank you very much, and enjoy the rest of your day.

**Operator** (Operator):
Thank you. This concludes today's Johnson & Johnson's Third Quarter 2026 Earnings Conference Call. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### JNJ_Q2_2026_Earnings_Call_20260715.md
- 2026-07-15｜CFO Joseph Wolk｜guidance：CFO 將 2026 全年營運銷售成長財測調升 $4 億，區間 6.5%–7.1%（原話："range of 6.5% to 7.1% with a midpoint of $100.6 billion"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：調整後營運 EPS 區間上調，中點增 $0.18（原話："range to $11.50 to $11.65, which equates to an increase"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：CFO 稱下半年營運銷售成長將改善（原話："sales growth to improve in the second half of the year"）
- 2026-07-15｜CFO Joseph Wolk｜margin：稅前營業利益率改善預期由原先逾 50bp 調為約 75bp（原話："We now expect approximately a 75 basis point"）
- 2026-07-15｜CFO Joseph Wolk｜margin：利益率改善的支撐之一是關稅相關成本的減少與追回（原話："recoupment of certain tariff-related costs"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：全年有效稅率預期下調至 17.0%–18.0%（原話："expected to be lower in a range of 17.0% to 18.0%"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：財測不含 Firefly Bio 等待完成的併購（原話："Our current outlook does not include the impact of any"）
- 2026-07-15｜Ryan Koors｜margin：創新藥 adjusted 稅前利益率由 42.7% 降至 42.5%，原因為產品組合與上市投入（原話："declined from 42.7% to 42.5%, primarily driven by"）
- 2026-07-15｜Ryan Koors｜margin：醫療科技 adjusted 稅前利益率由 22.2% 降至 22%（原話："declined from 22.2% to 22%, primarily driven by"）
- 2026-07-15｜Ryan Koors｜margin：銷管費用因新產品上市投入而去槓桿 60bp（原話："administrative expenses deleveraged by 60 basis points"）
- 2026-07-15｜Ryan Koors｜margin：營運銷售成長 5.6% 已吸收約 460bp 的 STELARA 逆風（原話："despite an approximate 460 basis point headwind from STELARA"）
- 2026-07-15｜Ryan Koors｜risk：電生理成長受中國庫存調整影響，管理層估計拖累 400bp（原話："China inventory, which we estimate to be 400 basis points"）
- 2026-07-15｜Ryan Koors｜competition：電生理成長被 PFA 競爭壓力部分抵銷（原話："partially offset by competitive PFA pressures"）
- 2026-07-15｜Ryan Koors｜competition：STELARA 下滑 55.7%，歸因於生物相似藥競爭（原話："driven by share loss due to biosimilar competition"）
- 2026-07-15｜Ryan Koors｜product：DARZALEX 成長 17.6%，各線治療市佔提升（原話："strong share gains of 5 points across all lines of therapy"）
- 2026-07-15｜CFO Joseph Wolk｜risk：CFO 承認醫療科技心血管（主要是心臟復原）表現未達公司標準（原話："standards in cardiovascular, primarily heart recovery"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：CFO 對 Abiomed 下調預期，復原要到明年，在 PROTECT IV 前僅溫和成長（原話："more modest growth until our PROTECT IV data comes out"）
- 2026-07-15｜CFO Joseph Wolk｜commitment：管理層重申本十年末達雙位數成長的能見度（原話："of sight to double-digit growth by the end of the decade"）
- 2026-07-15｜CEO Joaquin Duato｜commitment：CEO 稱 2026 年營收將首度突破 $1,000 億（原話："on track to meet our 2026 target of more than $100 billion"）
- 2026-07-15｜CEO Joaquin Duato｜commitment：CEO 設定 2030 年成為腫瘤第一大公司、銷售額逾 $500 億（原話："on track to be the #1 oncology company by 2030"）
- 2026-07-15｜CFO Joseph Wolk｜capital_allocation：資本配置優先順序不變；併購是成長推手但非必要條件（原話："but they are not a requirement to deliver on our"）
- 2026-07-15｜CFO Joseph Wolk｜capital_allocation：預計第三季完成 Firefly Bio 收購，補強 KRAS 實體瘤平台（原話："recently announced agreement to acquire Firefly Bio"）
- 2026-07-15｜CFO Joseph Wolk｜capital_allocation：股東回饋以股息為主（原話："committed to returning capital directly to shareholders"）
- 2026-07-15｜CFO Joseph Wolk｜capital_allocation：全年自由現金流展望維持接近 $210 億（原話："full year free cash flow outlook approaching $21 billion"）
- 2026-07-15｜CFO Joseph Wolk｜commitment：骨科（DePuy Synthes）分拆維持 2027 年中時程（原話："on track for a mid-2027 separation"）
- 2026-07-15｜CFO Joseph Wolk｜commitment：將於 12 月 8 日企業業務回顧說明策略與長期展望（原話："Enterprise business review on December 8"）
- 2026-07-15｜Jennifer Taubert｜customer：ICOTYDE 上市處方與患者數更新（原話："over 18,000 prescriptions have been written"）
- 2026-07-15｜Jennifer Taubert｜customer：ICOTYDE 90 天內取得逾半商業保險覆蓋（原話："within 90 days we already have over 50% of"）
- 2026-07-15｜Jennifer Taubert｜product：管理層稱 ICOTYDE 未拖慢 TREMFYA 在乾癬領域的表現（原話："has not slowed down TREMFYA in psoriatic disease at all"）
- 2026-07-15｜Jennifer Taubert｜commitment：ICOTYDE 加碼投入，直接面對消費者廣告前一日開播（原話："started our direct-to-consumer advertising yesterday"）
- 2026-07-15｜Jennifer Taubert｜product：INLEXZO 本季銷售較上季成長逾一倍並優於市場預期（未單獨揭露）（原話："we more than doubled sales in second quarter versus"）
- 2026-07-15｜Jennifer Taubert｜product：TREMFYA 在潰瘍性結腸炎 IL-23 誘導期市佔 58%（原話："58% share of induction"）
- 2026-07-15｜John Reed｜risk：milvexian 為事件驅動試驗，讀數時點可能在年底或明年初，無法給具體時程（原話："towards the end of this year, beginning of next year"）
- 2026-07-15｜John Reed｜risk：對 milvexian 房顫適應症的語氣為審慎樂觀（原話："we're cautiously optimistic, but are waiting for the"）
- 2026-07-15｜Tim Schmid｜risk：MedTech 管理層稱未見廣泛性手術量放緩（原話："not seeing evidence of a broad-based slowdown in demand"）
- 2026-07-15｜Tim Schmid｜risk：管理層稱 ACA 補貼到期尚未觀察到對手術量的實質影響（原話："observed any meaningful impact on procedure volumes"）
- 2026-07-15｜Tim Schmid｜risk：MedTech 負責人承認心血管本季成長低於公司自身預期（原話："frankly, it's not where we wanted it"）
- 2026-07-15｜Tim Schmid｜competition：Abiomed 稱目前沒有已商業化的競爭對手（原話："no current commercialized competitors"）
- 2026-07-15｜Tim Schmid｜commitment：PROTECT IV 預計 2027 年讀數（原話："which we expect to read out in 2027"）
- 2026-07-15｜Tim Schmid｜guidance：Abiomed 預期未來數季逐步回到雙位數成長（原話："back to double-digit growth over the coming quarters"）
- 2026-07-15｜Tim Schmid｜commitment：今年預計推出兩項機器人手術產品（OTTAVA、MONARCH 泌尿），以取得核准為前提（原話："committed to 2 large robotic launches this year"）
- 2026-07-15｜CEO Joaquin Duato｜commitment：CEO 稱機器人平台在本十年末將成為醫療科技成長的重要貢獻者（原話："contributor to MedTech growth by the end of the decade"）

### 問答異常語氣（迴避／改口／保留）
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Goldman Sachs 問 ICOTYDE 處方醫師數較 6 月更新、試用品/免費藥、納保談判及何時分拆銷售｜答法：回答了處方數、保險覆蓋與 DTC，但未回應試用品/免費藥規模與何時單獨揭露銷售
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Wells Fargo 問 2026 全年（不含額外一週）MedTech 是否仍會比去年成長更快｜答法：回答聚焦於手術量穩定與下半年加速，未直接回答排除第 53 週後的全年成長率
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Guggenheim 問 INLEXZO 患者/處方醫師數、社區 vs 學術使用，及 SunRISe-5 數據預期｜答法：給出市佔與新患者插入成長比例，未提供患者或處方醫師絕對數，亦未設定 SunRISe-5 預期
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Raymond James 問 Abiomed 新的成長預期（先前認為是中段兩位數成長）及除等 PROTECT IV 外的對策｜答法：未給出新的成長率數字，只說下半年強於上半年並逐步回到雙位數，也未說明先前中段兩位數預期是否調整
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Wolfe Research 問 milvexian 房顫的信心程度與是否仍在年底前讀數｜答法：稱事件驅動無法給讀數時點，信心以審慎樂觀表述，未給成功機率

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
{"date":"20260716","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"新藥引擎（Darzalex／Tremfya／Carvykti ＋ 新上市 icotrokinra／Rybrevant／Caplyta）淨接棒 Stelara 懸崖，IM operational 成長 6-8%","columns":{"2Y（FY26-27）":"IM operational ≥ +6%；Darzalex 年化 $17B+、Tremfya $8B+、Carvykti $2.5B+","5Y（FY28-30）":"腫瘤 franchise 2030 目標 $50B；IM 2025-30 CAGR 5-7%","10Y（FY31-35）":"2030 後次世代 pipeline 銜接，避免第二輪懸崖","具體門檻":"Q2 2026 IM +6.8% operational；Darzalex Q2 $4.21B(+18.9%)、Tremfya $2.05B(+72.5%)、Carvykti $657M(+49.4%)","來源":"JNJ Q2 2026 法說＋ Enterprise Business Review","漂移觸發":"連 2 季 TTM IM ex-Stelara &lt; +6% → 削弱"}},{"id":"H2","text":"MedTech operational 恢復至中個位數＋、OI margin 守 ~24%，且 DePuy Synthes 骨科（~29% MedTech 營收）分拆／出售乾淨執行","columns":{"2Y（FY26-27）":"FY2026 MedTech operational ≥ +4%（Q2 +3.6% borderline）；核心心血管／外科／視力 re-rate","5Y（FY28-30）":"分拆後留存組合 OI margin 對標 ABT 24.5%／MDT 25.8%","10Y（FY31-35）":"心血管介入＋機器人外科為 MedTech 主引擎","具體門檻":"Q2 2026 MedTech +3.6% operational（miss ~$8.97B 估）；Cardiovascular $2.4B(+3.1%)","來源":"JNJ FY25 10-K 分部揭露；Bloomberg 2026-02 $20B+ 出售探詢","漂移觸發":"連 2 季 TTM MedTech operational &lt; +3% 或分拆對價／時程惡化 → 削弱"}},{"id":"H3","text":"Talc 逐案訴訟＋潛在全球和解控制在有限責任（準備金 ~$10-13B，最壞 &lt; $35B），不被迫 mega-settlement；Section 232 藥品關稅豁免落實","columns":{"2Y（FY26-27）":"2026H2-2027 個案判決可控；準備金無跳升","5Y（FY28-30）":"2027-2028 若達全球和解，總額 ≤ $30B（分 5-8 年支付、年化 hit ≤ $5B）","10Y（FY31-35）":"2030 後 talc 大致 cleared，僅留 contingent reserve","具體門檻":"單筆和解 ≤ $30B（現金流 $19B 的 ~1.6x）；再啟破產策略或 $40B+ → H3 反轉","來源":"MDL 2738；JNJ 10-Q Note；Reuters／Law360","漂移觸發":"連 2 季準備金新增 &gt; $3B，或一次性付 $35B+ → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Section 232 藥品關稅落地：100% 專利藥／API 關稅豁免未於生效日前定案，落在 Innovative Medicine（65% 營收）進口品項；與已實現的醫材關稅（Q1 曾拖累 OI margin）機制不同、規模未定價","columns":{"對應假設":"H3／H1","時間尺度":"⚡ 短期（生效日 ~2026-07-31）","監測指標":"① MFN 定價協議簽署狀態 ② USTR/Commerce Annex III 名單與豁免細則 ③ 法說對關稅假設的量化","警戒閾值":"豁免未落實且關稅生效 → 連 2 季監測 IM COGS 上升／margin 壓縮即減碼考量"}},{"id":"R2","text":"MedTech 恢復失速＋分拆執行風險：Abiomed（Impella 2026 多起 FDA 召回／安全警示）、電生理 VARIPULSE（2026 初暫停約 5 週、PFA 份額落後 BSX Farapulse）拖累；DePuy Synthes 骨科分拆時程／對價不確定","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"① MedTech 分部 operational 成長 ② Cardiovascular 子分部成長 ③ 分拆進度公告","警戒閾值":"連 2 季 MedTech operational &lt; +3%（Q1/Q2 已 borderline）→ MedTech moat 重評，§9 sub-score 下調"}},{"id":"R3","text":"Talc 訴訟黑天鵝：第三次破產策略（Red River Talc）已被否，轉逐案訴訟；被迫 $35-50B 全球和解或連續 mega-verdict（如 2025-12 巴爾的摩 $1.5B 間皮瘤判決）大幅消耗 FCF","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"① 法院指定調解進展 ② 10-Q 法律準備金新增 ③ 重大個案判決趨勢","警戒閾值":"單一情境總額 ≥ $35B ＋ 準備金連 2 季新增 &gt; $3B"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE 回落 ≤18x（約 $210-220）或 PEG ≤2；或 talc 全球和解定案 ≤$30B；或 Section 232 藥品關稅豁免正式確認","irr_base_pct":7.7,"ev5y_pct":33.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.9,"ev5y_pct":33.0,"irr_base_pct":7.7,"max_dd_pct":-38.0,"bull_5y_price":420.0,"bear_5y_price":210.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE 回落 ≤18x（約 $210-220）或 PEG ≤2；或 talc 全球和解定案 ≤$30B；或 Section 232 藥品關稅豁免正式確認","price_at_dd":247.02,"archetype":"品質複利成長","cycle_position":null}}
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

此回覆內容之後由程式存為 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JNJ_20261018/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
