你是 stock-analyst **v20 判斷 agent**，標的 MU（20261020）。本輪單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，你讀完就直接作答，沒有第二輪，不能查證 bundle 以外的任何資料，也不能事後修改自己剛給出的內容。

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
{"meta":{"ticker":"MU","date":"2026-10-20","schema":"facts-v1","generator":"dd_facts.py extract（零 LLM；needs_sonnet 題目待事實表 agent 補）","evidence_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/MU_20261020/evidence.json","digest_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/MU_20261020/digest.json"},"questions":{"q1_business":{"label":"怎麼賺錢","facts":[{"id":"f_kpi0_gaap","label":"GAAP 營收","value":41456,"period":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","unit":"百萬美元","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[0]","as_of":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","citation":"公司新聞稿 investors.micron.com Reports Record Results for the Third Quarter of Fiscal 2026；交叉核對 SEC 8-K exhibit https://www.sec.gov/Archives/edgar/data/723125/000072312526000013/a2026q3ex991-pressrelease.htm 與 10-Q https://www.sec.gov/Archives/edgar/data/723125/000072312526000015/mu-20260528.htm"},"note":"analyst consensus 約 $35.69 billion（來源：news aggregator 彙整之市場預期，非公司揭露，beat 約 16.17%）"},{"id":"f_kpi1_non_gaap","label":"Non-GAAP 營業利益／利益率","value":81.2,"period":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","unit":"%（Non-GAAP operating income $33,681 百萬 ÷ 營收 $41,456 百萬）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[1]","as_of":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","citation":"公司新聞稿 investors.micron.com Q3 FY26 press release（同上 SEC 連結）"},"note":"查無公開 Non-GAAP 營業利益率 consensus 數字，未填造"},{"id":"f_kpi2_gaap","label":"GAAP 營業利益／利益率","value":80.4,"period":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","unit":"%（GAAP operating income $33,318 百萬 ÷ 營收 $41,456 百萬）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[2]","as_of":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","citation":"公司新聞稿 investors.micron.com Q3 FY26 press release；同數字見 SEC 10-Q 損益表"},"note":"查無公開 GAAP 營業利益率 consensus 數字，未填造"},{"id":"f_kpi5_q4_fy2026_guidance","label":"管理層 Q4 FY2026 財測（guidance）","value":"營收 $50.0B ± $1.0B；毛利率約 86%；Non-GAAP EPS $31.00 ± $1.00","period":"Q4 FY2026 展望（公告於 Q3 FY2026 法說會 2026-06-24，Q4 尚未公告實際結果——本站 earnings_recency 顯示最近一次財報仍是 2026-06-24）","unit":"區間","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"guidance","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[5]","as_of":"Q4 FY2026 展望（公告於 Q3 FY2026 法說會 2026-06-24，Q4 尚未公告實際結果——本站 earnings_recency 顯示最近一次財報仍是 2026-06-24）","citation":"公司新聞稿 investors.micron.com Q3 FY26 press release，Business Outlook 表格"},"note":"查無公告當時 Q4 consensus 對照數字，未填造"},{"id":"f_earnings_recency","label":"最近一次財報日","value":"2026-09-30","period":"2026-09-30","unit":"date","basis":"距今 14 個交易日","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.earnings_recency","as_of":"2026-09-30"}}],"needs_sonnet":true,"needs_sonnet_note":"分部與客戶占比、單價與量的結構化值、商業模式收錢方式——evidence.numbers 無此欄位，須由事實表 agent 從 10-K／10-Q／逐字稿補。"},"q2_moat":{"label":"競爭優勢","facts":[{"id":"f_peer_mu_gross_margin_pct","label":"MU 毛利率","value":72.57,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.gross_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_mu_operating_margin_pct","label":"MU 營業利益率","value":65.67,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.operating_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_mu_fcf_margin_pct","label":"MU FCF 利潤率","value":28.99,"period":"TTM ending 2026-05-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU.fcf_margin_pct","as_of":"TTM ending 2026-05-31（4季加總）"}},{"id":"f_peer_nvda_gross_margin_pct","label":"NVDA 毛利率","value":74.67,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_operating_margin_pct","label":"NVDA 營業利益率","value":65.21,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_nvda_fcf_margin_pct","label":"NVDA FCF 利潤率","value":41.92,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_tsm_gross_margin_pct","label":"TSM 毛利率","value":64.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsm_operating_margin_pct","label":"TSM 營業利益率","value":56.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_tsm_fcf_margin_pct","label":"TSM FCF 利潤率","value":25.33,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_avgo_gross_margin_pct","label":"AVGO 毛利率","value":68.77,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.gross_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_operating_margin_pct","label":"AVGO 營業利益率","value":48.52,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.operating_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_avgo_fcf_margin_pct","label":"AVGO FCF 利潤率","value":44.22,"period":"TTM ending 2026-07-31（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO.fcf_margin_pct","as_of":"TTM ending 2026-07-31（4季加總）"}},{"id":"f_peer_amd_gross_margin_pct","label":"AMD 毛利率","value":53.2,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.gross_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_operating_margin_pct","label":"AMD 營業利益率","value":15.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.operating_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}},{"id":"f_peer_amd_fcf_margin_pct","label":"AMD FCF 利潤率","value":20.34,"period":"TTM ending 2026-06-30（4季加總）","unit":"%","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD.fcf_margin_pct","as_of":"TTM ending 2026-06-30（4季加總）"}}],"needs_sonnet":true,"needs_sonnet_note":"護城河機制的量化證據（份額、轉換成本、ROIC 輸入的投入資本口徑）——numbers.peer_financials 只給同業利潤率，其餘須補。"},"q3_growth":{"label":"成長","facts":[],"needs_sonnet":true,"needs_sonnet_note":"TAM 與滲透率、在手訂單、分部三年成長——evidence.numbers 無此欄位，須補；共識三年 EPS 已由 q5 的共識修正條目帶入，成長題引用同一組 id 不重收。"},"q4_capital":{"label":"現金與資本配置","facts":[{"id":"f_kpi3_adjusted_fcf","label":"調整後自由現金流（Adjusted FCF）","value":18304,"period":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","unit":"百萬美元（Operating cash flow $25,388 - net capex $7,084）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[3]","as_of":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","citation":"公司新聞稿 investors.micron.com Q3 FY26 press release"},"note":"查無公開 FCF consensus 數字，未填造"},{"id":"f_kpi4_sbc_gaap","label":"SBC（股票薪酬）占 GAAP 營業利益／占營收 %","value":341,"period":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","unit":"百萬美元（占 GAAP 營業利益 1.02%；占營收 0.82%）","basis":"evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.latest_quarter_kpis.items[4]","as_of":"Q3 FY2026（季末 2026-05-28，公告於 2026-06-24）","citation":"公司新聞稿 investors.micron.com Q3 FY26 press release，Non-GAAP 調節表 Stock-based compensation 341"},"note":"不適用（SBC 無 consensus 概念）"}],"needs_sonnet":true,"needs_sonnet_note":"近三年現金去向四分、債務到期結構與加權平均利率、回購均價——numbers 只有最新一季 KPI，其餘須補。"},"q5_valuation":{"label":"估值","facts":[{"id":"f_price_at_dd","label":"判斷日股價","value":904.9,"period":"2026-10-19（RTH 收盤，UTC）","unit":"USD","basis":"收盤價，與情境樹起點同源","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.price_at_dd","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_week26_return_pct","label":"26 週報酬","value":93.18,"period":"2026-10-19（RTH 收盤，UTC）","unit":"%","basis":"含息前價格報酬，對照基準 ^GSPC","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.return_26w_pct","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_rsi14","label":"RSI(14)","value":34.04,"period":"2026-10-19（RTH 收盤，UTC）","unit":"","basis":"日線 14 期；rsi14_usable=True","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.momentum_26w.rsi14","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_consensus_rev_fy1_pct","label":"FY1 共識修正","value":0.23,"period":"2026-10-17","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（176.15 → 176.55）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy1.revision_pct","as_of":"2026-10-17","citation":"DD_universe_EPS_estimates_20261017.xlsx"}},{"id":"f_consensus_rev_fy2_pct","label":"FY2 共識修正","value":-0.9,"period":"2026-10-17","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（206.33 → 204.47）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy2.revision_pct","as_of":"2026-10-17","citation":"DD_universe_EPS_estimates_20261017.xlsx"}},{"id":"f_consensus_rev_fy3_pct","label":"FY3 共識修正","value":0.09,"period":"2026-10-17","unit":"%","basis":"兩份 Koyfin 快照之間的 EPS 修正幅度（203.15 → 203.33）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.fy3.revision_pct","as_of":"2026-10-17","citation":"DD_universe_EPS_estimates_20261017.xlsx"}},{"id":"f_consensus_eps_fy1","label":"FY1 共識 EPS","value":176.55,"period":"2026-10-17","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1","as_of":"2026-10-17","citation":"DD_universe_EPS_estimates_20261017.xlsx"}},{"id":"f_consensus_eps_fy2","label":"FY2 共識 EPS","value":204.47,"period":"2026-10-17","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy2","as_of":"2026-10-17","citation":"DD_universe_EPS_estimates_20261017.xlsx"}},{"id":"f_consensus_eps_fy3","label":"FY3 共識 EPS","value":203.33,"period":"2026-10-17","unit":"USD/share","basis":"Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy3","as_of":"2026-10-17","citation":"DD_universe_EPS_estimates_20261017.xlsx"}},{"id":"f_consensus_rev_3m_fy1_pct","label":"FY1 共識近 3 個月修正","value":140.63,"period":"2026-07-16 → 2026-10-17","unit":"%","basis":"FY1 共識 EPS 73.37 → 176.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1","as_of":"2026-10-17","citation":"DD_universe_EPS_estimates_20261017.xlsx"}},{"id":"f_pe_current","label":"Trailing P/E（現值）","value":12.17,"period":"2026-10-19（RTH 收盤，UTC）","unit":"x","basis":"3 個年度端點內的分位＝4.4","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe","as_of":"2026-10-19（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_pe_percentile","label":"Trailing P/E 年度端點分位","value":4.4,"period":"2026-10-19（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.pe.current_percentile_within_annual_points","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_ps_current","label":"P/S（現值）","value":7.69,"period":"2026-10-19（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps","as_of":"2026-10-19（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ps_percentile","label":"P/S 年度端點分位","value":100.0,"period":"2026-10-19（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ps.current_percentile_within_annual_points","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_ev_s_current","label":"EV/S（現值）","value":7.4,"period":"2026-10-19（RTH 收盤，UTC）","unit":"x","basis":"4 個年度端點內的分位＝100.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s","as_of":"2026-10-19（RTH 收盤，UTC）","citation":"trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。"}},{"id":"f_ev_s_percentile","label":"EV/S 年度端點分位","value":100.0,"period":"2026-10-19（RTH 收盤，UTC）","unit":"%","basis":"**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points","as_of":"2026-10-19（RTH 收盤，UTC）"}},{"id":"f_fwd_pe_latest","label":"Forward P/E（最近快照）","value":4.98,"period":"2026-10-17","unit":"x","basis":"分母＝FY1 EPS 176.55，分子＝快照價 878.84","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.valuation_history.fwd_recent_window.points[-1]","as_of":"2026-10-17"}},{"id":"f_dividend_yield_ttm","label":"trailing 12個月股息殖利率","value":0.062,"period":"2026-10-20","unit":"%","basis":"trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.dividend_yield_ttm.value_pct","as_of":"2026-10-20"}},{"id":"f_net_debt_m","label":"目前淨負債（總債務－現金及短投）","value":-38255.0,"period":"2026-10-20","unit":"USD m","basis":"yfinance 最新一季：總債務 5179.0、現金 43434.0（含租賃負債口徑）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.net_debt_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_shares_diluted_m","label":"目前股數（百萬股）","value":1131.42,"period":"2026-10-20","unit":"m shares","basis":"yfinance impliedSharesOutstanding（各類股合計）","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.shares_diluted_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_m","label":"目前企業價值 EV（市值＋淨負債）","value":985569.89,"period":"2026-10-20","unit":"USD m","basis":"市值 1023824.89 ＋ 淨負債 -38255.0","kind":"realized","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy1_m","label":"FY1 共識營收（百萬）","value":275504.76,"period":"2026-10-20","unit":"USD m","basis":"yfinance revenue_estimate 0y 平均（41 位分析師）；與 f_consensus_eps_fy1 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy1.avg_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_rev_consensus_fy2_m","label":"FY2 共識營收（百萬）","value":318881.82,"period":"2026-10-20","unit":"USD m","basis":"yfinance revenue_estimate +1y 平均（43 位分析師）；與 f_consensus_eps_fy2 同一財年","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.revenue_consensus.fy2.avg_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ev_s_fwd","label":"EV/S（EV ÷ FY1 共識營收）","value":3.58,"period":"2026-10-20","unit":"x","basis":"f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）","kind":"estimate","source":{"type":"evidence_numbers","ref":"numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m","as_of":"2026-10-20"},"note":"股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null"},{"id":"f_ma_state","label":"週線均線六態（decision_inputs.ma 必須等於此值）","value":"✅","period":"2026-10-20","unit":null,"basis":"timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"},"quote":"price 878.84 / W52 623.18 / W104 366.15 / W250 197.27 / W250 13週斜率 8.15%"},{"id":"f_ma_w52","label":"52 週均線","value":623.18,"period":"2026-10-20","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w104","label":"104 週均線","value":366.15,"period":"2026-10-20","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_w250","label":"250 週均線","value":197.27,"period":"2026-10-20","unit":"USD","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}},{"id":"f_ma_slope_w250_pct","label":"W250 13 週斜率","value":8.15,"period":"2026-10-20","unit":"%","basis":"週線收盤 SMA（yfinance auto_adjust）","kind":"realized","source":{"type":"manual","ref":"ma_snapshot.json","as_of":"2026-10-20","citation":"程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}}],"needs_sonnet":true,"needs_sonnet_note":"同業倍數對照與目標價（若承重）——其餘估值事實已機械抽出。"},"q6_how_wrong":{"label":"可能看錯在哪","facts":[],"needs_sonnet":true,"needs_sonnet_note":"歷史最大回撤幅度、空方最強數字、訴訟與監管的金額與時點——須由事實表 agent 從 findings_digest 與 filing 補。"}},"findings_digest":[{"id":"competitive_share_entrants#0","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Micron's NAND flash market share climbed to 15% in Q2 2026, its strongest position in the period; Samsung still leads but its lead is narrowing as SK Hynix and Micron gain ground amid a NAND price surge.","source":"Counterpoint Research, Global NAND Memory Market Share (Quarterly), via Sammy Fans \"Samsung stays ahead while SK Hynix and Micron capture more NAND share\" (2026-09-04)","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#1","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Micron held 19.9% global DRAM market share, ranking No. 3 behind Samsung and SK Hynix, in Q1 2026.","source":"Counterpoint Research, Global DRAM and HBM Market Share (Quarterly)","url":null,"excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261020","affects":["moat_trend"],"status":"ok"},{"id":"competitive_share_entrants#2","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"SK Hynix retained the top HBM market share position at ~50% in Q2 2026, down from 64% in Q2 2025 — the leader's share is compressing as rivals ramp HBM capacity.","source":"Counterpoint Research, Global DRAM and HBM Market Share (Quarterly)","url":null,"excerpt":null,"as_of":"2026-06-30","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"competitive_share_entrants#3","axis":"competitive_share_entrants","section":"coverage","direction":"0","claim":"Micron held roughly 11% HBM market share as of its December 2025 announcement, when it also said it plans to exit the consumer memory/storage market to prioritize AI data-center customers.","source":"Press coverage summarizing Micron's Dec 2025 announcement (Presenc.ai, \"HBM Market Share 2026: SK hynix 62%, Micron Overtakes Samsung, HBM4 Battle\")","url":null,"excerpt":null,"as_of":"2025-12-01","retrieved_at":"20261020","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#4","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"China's CXMT is projected to reach ~350,000 wafer starts per month of DRAM capacity by end-2026 — only ~25,000 WSPM behind Micron — putting CXMT in 4th place globally in DRAM (behind Samsung, SK Hynix, Micron) and on track to make China the world's second-largest DRAM production base.","source":"Tom's Hardware, \"CXMT close to matching Micron's memory capacity in 2026\"","url":null,"excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261020","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#5","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Some Chinese PC/memory-module brands (cited: Corsair, HP, Dell) have begun sourcing homegrown DDR5 chips from CXMT and YMTC instead of Samsung, Micron and SK Hynix.","source":"Tom's Hardware, \"Chinese memory brands ditch Samsung and Micron for homegrown CXMT and YMTC silicon\"","url":null,"excerpt":null,"as_of":"2026-07-01","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#6","axis":"competitive_share_entrants","section":"coverage","direction":"-","claim":"Micron CEO Sanjay Mehrotra pushed the US Congress to restrict chip-equipment access for CXMT, YMTC and SMIC, warning that Chinese state-backed investment poses a competitive threat comparable to China's dominance of the solar industry.","source":"Taipei Times, \"Micron pushes US Congress to curb Chinese competitors\"","url":null,"excerpt":null,"as_of":"2026-04-23","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"competitive_share_entrants#7","axis":"competitive_share_entrants","section":"coverage","direction":"+","claim":"Micron is certified and in high-volume production as an HBM4 supplier for Nvidia's Vera Rubin AI platform; its entire calendar-2026 HBM4 capacity is committed under binding contracts, including Micron's first five-year customer agreement (unusually long for the sector). Samsung and SK Hynix are also confirmed HBM4 suppliers for Vera Rubin, i.e. Micron is not the exclusive supplier.","source":"Micron Technology investor press release, \"Micron in High-Volume Production of HBM4 Designed for NVIDIA Vera Rubin, PCIe Gen6 SSD and SOCAMM2\"","url":null,"excerpt":null,"as_of":"2026-03-16","retrieved_at":"20261020","affects":["thesis.H","decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_second_source#0","axis":"customer_second_source","section":"coverage","direction":"+","claim":"Micron signed 16 strategic long-term supply agreements with data center, consumer, and automotive customers, most take-or-pay and running from CY2026 through late 2030; 14 of the first 16 total roughly $100B in combined minimum contracted revenue, locking customers into Micron rather than customers qualifying alternate/in-house sources.","source":"The Motley Fool, \"Micron's Customers Are Putting Up $22 Billion, and Its CEO Says Data Centers Want 50% More Memory Than It Can Ship\", https://www.fool.com/investing/2026/08/24/micron-s-customers-are-putting-up-usd22-billion-and-its-ceo-says-data-centers-want-50-more-memory-than-it-can-ship/","url":null,"excerpt":null,"as_of":"2026-08-24","retrieved_at":"20261020","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"customer_second_source#1","axis":"customer_second_source","section":"coverage","direction":"-","claim":"Nvidia CEO Jensen Huang confirmed on 2026-06-05 that Samsung, SK Hynix, and Micron have all passed certification to supply HBM4 for Nvidia's Vera Rubin platform; supply-chain analysts estimate SK Hynix holds roughly 60-70% of Vera Rubin HBM4 volume, Samsung ~25-30%, and Micron the remainder — i.e. Micron's largest AI customer already multi-sources HBM across three qualified suppliers, with Micron as the smallest share.","source":"Yahoo Finance, \"Nvidia certifies Samsung, SK Hynix and Micron for Vera Rubin HBM4 supply\"; TweakTown, \"SK hynix, Samsung, and Micron fighting for NVIDIA supply contracts for new 16-Hi HBM4 orders\", https://finance.yahoo.com/sectors/technology/articles/nvidia-certifies-samsung-sk-hynix-133001560.html","url":null,"excerpt":null,"as_of":"2026-06-05","retrieved_at":"20261020","affects":["moat_trend","thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"customer_concentration_credit#0","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"One undisclosed customer (primarily in the CMBU cloud memory segment) accounted for 17% of Micron's total revenue in fiscal Q1 2026 (quarter ended late Nov 2025).","source":"Micron Form 10-Q FY2026 Q1 filing, https://investors.micron.com/static-files/502c03ac-dd06-4c88-9441-02ebfe6ff6fa","url":null,"excerpt":null,"as_of":"2025-12-18","retrieved_at":"20261020","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#1","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Revenue from that same undisclosed customer (CMBU segment) fell to 13% of total revenue for the first six months of fiscal 2026, versus 15% in the same period of fiscal 2025.","source":"Micron Form 10-Q FY2026 Q2 filing, https://www.sec.gov/Archives/edgar/data/723125/000072312526000006/mu-20260226.htm","url":null,"excerpt":null,"as_of":"2026-02-26","retrieved_at":"20261020","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"customer_concentration_credit#2","axis":"customer_concentration_credit","section":"coverage","direction":"+","claim":"Revenue from that customer further declined to 10% of total revenue for the first nine months of fiscal 2026, versus 16% in the same period of fiscal 2025 — concentration trending down over the fiscal year.","source":"Micron Form 10-Q FY2026 Q3 filing, https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm","url":null,"excerpt":null,"as_of":"2026-05-28","retrieved_at":"20261020","affects":["moat_trend","decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"customer_concentration_credit#3","axis":"customer_concentration_credit","section":"coverage","direction":"0","claim":"Micron's top ten customers together accounted for roughly half of total fiscal 2025 revenue.","source":"Micron FY2025 Form 10-K annual report summary, https://www.stocktitan.net/sec-filings/MU/10-k-micron-technology-inc-files-annual-report-a879767daea7.html","url":null,"excerpt":null,"as_of":"2025-08-28","retrieved_at":"20261020","affects":["moat_trend","thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"supply_demand_durability#0","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"2026年DRAM/NAND供給緊張被業界定性為結構性、非傳統週期性短缺——主因是產能被重新分配去生產HBM（AI用高頻寬記憶體），而非單純供需錯配；新增晶圓廠產能要到2027年底/2028年才有實質產出量。","source":"StorageSwiss.com, 'Memory and Flash Prices Are Not Coming Down (Through 2027)'","url":null,"excerpt":null,"as_of":"2026-05-06","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"supply_demand_durability#1","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"主要NAND/DRAM供應商2026年產能已『結構性售罄』(標題為'Supply: Structurally Sold Out'，屬allocation exhaustion而非傳統缺貨)；廠商已在2025下半年主動縮減產能，且有意延後新增產能到2027年後才釋出，展現供給紀律；雲端服務商長約持續吸走可用供給。","source":"NAND Research, 'Memory & NAND Flash Crisis: May 2026 Update'","url":null,"excerpt":null,"as_of":"2026-05-13","retrieved_at":"20261020","affects":["moat_trend","thesis.H","triggers"],"status":"ok"},{"id":"supply_demand_durability#2","axis":"supply_demand_durability","section":"coverage","direction":"+","claim":"Micron公開表示其HBM產能未來數季已售罄(sold out for the next several quarters)。","source":"TIKR.com, 'Micron Stock Is Up 70% in 2026. Here's Why Analysts Still See More Upside Ahead'","url":null,"excerpt":null,"as_of":"2026-05-02","retrieved_at":"20261020","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"supply_demand_durability#3","axis":"supply_demand_durability","section":"coverage","direction":"0","claim":"2027年記憶體市場走勢分化：DRAM供給持續吃緊（且因產能爬升延後，實質產出增量要等到2028年才明顯），但NAND Flash供給隨新產能逐步開出轉向較平衡，NAND供需比由負轉正，市場性質從供給受限轉為供需較平衡。","source":"TrendForce (via PR Newswire), 'Diverging Memory Market Outlook in 2027 as DRAM Supply Remains Tight While NAND Flash Supply Conditions Ease'","url":null,"excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261020","affects":["thesis.H","thesis.R","valuation"],"status":"ok"},{"id":"regulatory_antitrust#0","axis":"regulatory_antitrust","section":"coverage","direction":"-","claim":"Samsung、SK Hynix、Micron 三家於 2026年6月25日在美國加州北區聯邦法院被 17 名消費者/小型企業提起集體訴訟，指控三家共謀限制commodity DRAM供給、藉擴產HBM為由人為推升價格，四年來漲幅約700%；三家合計約佔全球DRAM營收九成。Micron 否認指控並表示將抗辯。","source":"TrendForce, \"Samsung, SK hynix, Micron Face U.S. Class-Action Lawsuit Over Alleged DRAM Supply Manipulation\", https://www.trendforce.com/news/2026/06/29/news-samsung-sk-hynix-micron-face-u-s-class-action-lawsuit-over-alleged-dram-supply-manipulation/","url":null,"excerpt":null,"as_of":"2026-06-25","retrieved_at":"20261020","affects":["decision_inputs.bear","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#1","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"美國商務部工業與安全局(BIS)於2025年4月14日宣布依《1962年貿易擴張法》第232條，對半導體、半導體製造設備及其衍生品進口展開產業性國家安全調查，範圍涵蓋Micron所屬記憶體產業。","source":"Micron Technology Inc, Form 10-Q FY2026, SEC filing, https://www.sec.gov/Archives/edgar/data/723125/000072312526000006/mu-20260226.htm","url":null,"excerpt":null,"as_of":"2025-04-14","retrieved_at":"20261020","affects":["triggers","thesis.R"],"status":"ok"},{"id":"regulatory_antitrust#2","axis":"regulatory_antitrust","section":"coverage","direction":"0","claim":"查無 DOJ、FTC 或歐盟競爭主管機關在2026年針對 Micron 具體開立之反壟斷調查案件；搜尋僅得一般性美歐反壟斷政策更新（如DOJ/FTC於2026年2月就競爭者合作新指引徵詢公眾意見），未點名 Micron。","source":"Goodwin Law, \"Antitrust & Competition Technology 1H 2026 Update\", https://www.goodwinlaw.com/en/insights/publications/2026/07/insights-technology-antc-antitrust-competition-technology-1h-2026","url":null,"excerpt":null,"as_of":"2026-07-23","retrieved_at":"20261020","affects":["thesis.R"],"status":"ok"},{"id":"reg_tariff_export#0","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"美國於2026年1月14日依Section 232發布公告，對符合特定效能門檻的半導體品項課徵25%進口關稅，2026年1月15日生效；範圍涵蓋先進運算晶片（如Nvidia H200、AMD MI325X）等HTS 8471.50/8471.80/8473.30項下產品。","source":"The White House, Presidential Actions - Adjusting Imports of Semiconductors (whitehouse.gov/presidential-actions/2026/01/adjusting-imports-of-semiconductors...)","url":null,"excerpt":null,"as_of":"2026-01-14","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"reg_tariff_export#1","axis":"reg_tariff_export","section":"coverage","direction":"-","claim":"美光在FY2026 10-Q中揭露：美國商務部BIS已於2025年4月14日對半導體、半導體製造設備及其衍生品發起Section 232國安調查，調查結果未定，公司表示此調查可能導致全產業性額外關稅與貿易限制，並可能對美光業務造成不利影響。","source":"Micron Technology Inc, Form 10-Q FY2026 (SEC EDGAR, sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm)","url":null,"excerpt":null,"as_of":"2026-05-28","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"reg_tariff_export#2","axis":"reg_tariff_export","section":"coverage","direction":"0","claim":"美光正遊說美國國會通過MATCH Act等法案，要求收緊晶片製造設備對中國出口的管制漏洞（含針對中國長鑫存儲CXMT、長江存儲YMTC、中芯國際SMIC等設施的限制），目的是壓制中國記憶體產能擴張。","source":"Idaho Business Review, \"Micron urges Congress to tighten chip tool export rules targeting China\"; Taipei Times, \"Micron pushes US Congress to curb Chinese competitors\"","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"reg_tariff_export#3","axis":"reg_tariff_export","section":"coverage","direction":"+","claim":"美國商務部長Lutnick警告，南韓記憶體廠（三星、SK海力士，合計逾70%全球記憶體供給）若不大幅擴大美國本土產能，可能面臨最高100%關稅；兩家韓廠目前美國投資均未涵蓋記憶體製造，其亞洲出貨的DRAM/NAND仍可能被課稅。美光本身在美國、日本、新加坡設有記憶體生產基地。","source":"sourceability.com, \"Memory shortage and tariff risks collide in AI chip supply\"","url":null,"excerpt":null,"as_of":"2026-08","retrieved_at":"20261020","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#0","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Micron's FY2026 10-Q risk factors disclose that a substantial portion of its manufacturing operations are located in Taiwan (along with Singapore, Japan, Malaysia, China, India), and that trade restrictions, tariffs, export controls, and sanctions involving the U.S., China, Taiwan, and Korea can directly affect what Micron can sell, where, and how it sources materials/equipment.","source":"Micron Technology Inc. Form 10-Q FY2026, SEC EDGAR (mu-20260226.htm)","url":null,"excerpt":null,"as_of":"2026-02-26","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#1","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Investor risk-factor analysis describes Micron as having 'extreme Taiwan dependency,' with Taiwan characterized as the central hub of the global tech supply chain, magnifying the potential for catastrophic disruption to Micron's operations from a regional conflict.","source":"Holdingschannel.com, \"Micron Risk Factors: Key Threats To MU Stock Explained For Investors\"","url":null,"excerpt":null,"as_of":"2026-04-07","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#2","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"China's Cyberspace Administration determined in May 2023 that Micron products posed a national security risk and banned Micron chips from purchase by operators of China's critical information infrastructure; this remains the realized precedent cited in current (2026) risk analyses for Micron's China-market exposure.","source":"TechCrunch, \"China bans Micron\" / PhoneArena, \"China bans shipments from U.S. memory chipmaker Micron Technology\"","url":null,"excerpt":null,"as_of":"2023-05-21","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"geo_supply_chain#3","axis":"geo_supply_chain","section":"coverage","direction":"0","claim":"Micron has been a driving force lobbying the U.S. Congress for the MATCH Act, which a House committee voted to advance in April 2026, aiming to restrict chipmaking-equipment exports to Chinese memory rivals (e.g., CXMT) on national-security grounds.","source":"Idaho Business Review, \"Micron urges Congress to tighten chip tool export rules targeting China\"","url":null,"excerpt":null,"as_of":"2026-04-22","retrieved_at":"20261020","affects":["moat_trend","decision_inputs.bear"],"status":"ok"},{"id":"geo_supply_chain#4","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Micron is acquiring Powerchip Semiconductor Manufacturing Corp's (PSMC) fab site in Tongluo, Taiwan (a 300,000 sq ft cleanroom) for $1.8 billion to expand DRAM and HBM capacity; deal expected to close in 2H2026, with meaningful DRAM wafer output targeted for 2H2027 — this increases, rather than diversifies, Micron's manufacturing footprint concentration in Taiwan.","source":"MarketWise, \"Micron's $1.8B Taiwan Fab Deal: What It Means for AI & Investors\" (also reported by Tom's Hardware)","url":null,"excerpt":null,"as_of":"2026-01-23","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"geo_supply_chain#5","axis":"geo_supply_chain","section":"coverage","direction":"-","claim":"Report on Micron's Taiwan HBM fab workers raising strike-risk concerns and seeking a larger share of pay amid the AI memory supercycle, highlighting labor/operational risk concentrated at Micron's Taiwan production sites.","source":"Tech Times, \"Micron Taiwan Strike Risk: HBM Workers Claim Share of AI Memory Supercycle\"","url":null,"excerpt":null,"as_of":"2026-09-02","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#0","axis":"end_markets","section":"coverage","direction":"0","claim":"Micron FQ2-26（截至約2026年2月，2026-03-18發布）四大業務單位營收：Cloud Memory BU $77.49億、Core Data Center BU $56.87億、Mobile and Client BU $77.11億、Automotive and Embedded BU $27.08億，總營收$238.60億","source":"Micron Q2 FY2026 Press Release (SEC EX-99.1), https://www.sec.gov/Archives/edgar/data/723125/000072312526000004/a2026q2ex991-pressrelease.htm","url":null,"excerpt":null,"as_of":"2026-03-18","retrieved_at":"20261020","affects":["thesis.H","valuation"],"status":"ok"},{"id":"end_markets#1","axis":"end_markets","section":"coverage","direction":"+","claim":"Bank of America 預測2026年DRAM營收年增51%、NAND年增45%，ASP分別上升33%與26%；Omdia更激進版本預測半導體營收年增62.7%，DRAM價值近乎翻倍、NAND可能翻兩倍以上（vs 2025）","source":"Octopart/BofA、Omdia 彙整報導，https://octopart.com/pulse/p/how-ai-broke-memory-market","url":null,"excerpt":null,"as_of":"2026-04","retrieved_at":"20261020","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#2","axis":"end_markets","section":"coverage","direction":"+","claim":"DRAM在AI與伺服器應用的消耗量預估將在2026年占DRAM總產能66%","source":"TrendForce Memory Wall 專題，https://www.trendforce.com/insights/memory-wall","url":null,"excerpt":null,"as_of":"2026","retrieved_at":"20261020","affects":["thesis.H"],"status":"ok"},{"id":"end_markets#3","axis":"end_markets","section":"coverage","direction":"0","claim":"HBM市占：SK hynix穩居約50-62%第一，Samsung約25-40%，Micron從2023年約2%成長至2025年約19%、預估2026年達約20%（第三名但持續成長）","source":"Astute Group／Counterpoint Research 彙整，https://www.astutegroup.com/news/general/sk-hynix-holds-62-of-hbm-micron-overtakes-samsung-2026-battle-pivots-to-hbm4/","url":null,"excerpt":null,"as_of":"2026","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"end_markets#4","axis":"end_markets","section":"coverage","direction":"0","claim":"Nvidia HBM4分配傳聞：SK hynix約50%多、Samsung約20%多、Micron約20%，Micron為明顯第三名但若驗證進度達標仍有上行空間","source":"Silicon Analysts HBM4市占分析，https://siliconanalysts.com/analysis/hbm4-market-share-race-2026","url":null,"excerpt":null,"as_of":"2026","retrieved_at":"20261020","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#5","axis":"end_markets","section":"coverage","direction":"-","claim":"TrendForce將2026年智慧型手機出貨展望下修為年減2%（原預估+0.1%），筆電出貨展望下修為年減2.4%（原預估+1.7%），主因記憶體漲價侵蝕終端需求","source":"TrendForce Press Center, https://www.trendforce.com/presscenter/news/20251117-12784.html","url":null,"excerpt":null,"as_of":"2025-11-17","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#6","axis":"end_markets","section":"coverage","direction":"-","claim":"2026年全球車用產業因DRAM/NAND嚴重短缺面臨供應鏈危機，因記憶體大廠將產能與資本支出轉向高毛利HBM/DDR5，不願維持成熟製程產能，造成車用/工業用舊製程晶片人為稀缺","source":"EE Times, https://www.eetimes.com/automakers-face-memory-shock-as-ai-uses-up-semiconductor-supply/","url":null,"excerpt":null,"as_of":"2026","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear"],"status":"ok"},{"id":"end_markets#7","axis":"end_markets","section":"coverage","direction":"+","claim":"2026年全球DRAM供給成長預估僅16% YoY、NAND僅17% YoY，均低於歷史常態的20-30%區間，為近年最緊供給環境","source":"IDC Blog, https://www.idc.com/resource-center/blog/higher-asps-lower-unit-volumes-how-the-memory-crisis-is-reshaping-the-pc-and-smartphone-outlook/","url":null,"excerpt":null,"as_of":"2025-12","retrieved_at":"20261020","affects":["thesis.H","moat_trend"],"status":"ok"},{"id":"end_markets#8","axis":"end_markets","section":"coverage","direction":"-","claim":"TrendForce（2026-07-30發布）預期2027年DRAM與NAND走勢分化：DRAM因HBM產能持續排擠、伺服器需求強勁維持供給緊張、價格上行；NAND則因新產能開出、消費性需求疲弱，預估2027下半年供給轉為寬鬆，價格承壓","source":"TrendForce Press Center, https://www.trendforce.com/presscenter/news/20260730-13158.html","url":null,"excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261020","affects":["thesis.R","triggers"],"status":"ok"},{"id":"substitute_technology#0","axis":"substitute_technology","section":"coverage","direction":"-","claim":"Samsung 與 SK hynix 據報正在探索超越 HBM（高頻寬記憶體，AI 加速卡用來加速資料存取的記憶體規格，美光靠此打入 AI 供應鏈）的次世代 AI 記憶體架構，可能挑戰 Nvidia 現有記憶體使用方式","source":"TrendForce, \"Beyond HBM: Samsung, SK hynix Reportedly Explore Next-Gen AI Memory That Could Challenge NVIDIA\", https://www.trendforce.com/news/2026/03/10/news-beyond-hbm-samsung-sk-hynix-reportedly-explore-next-gen-ai-memory-that-could-challenge-nvidia/","url":null,"excerpt":null,"as_of":"2026-03-10","retrieved_at":"20261020","affects":["moat_trend","thesis.R"],"status":"ok"},{"id":"channel_business_model_shift#0","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"美光宣布退出 Crucial 消費品牌業務（含零售、電商、經銷商通路），消費通路出貨延續至 FY2026 第二季（2026年2月）結束；企業級 Micron 品牌產品持續透過商用通路銷售給全球客戶。","source":"MarketScreener - \"Micron Technology Inc Announces Exit From Crucial Consumer Business\" (https://in.marketscreener.com/news/micron-technology-inc-announces-exit-from-crucial-consumer-business-ce7d51dede81f52d)","url":null,"excerpt":null,"as_of":"2025-03-12","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"channel_business_model_shift#1","axis":"channel_business_model_shift","section":"coverage","direction":"+","claim":"美光執行長 Mehrotra 將 Strategic Customer Agreements（SCA）定位為公司商業模式的轉型、而非單純商業強化；已簽 16 份多年期 SCA，合計鎖定至少 $100B 營收至 2030年，多為 take-or-pay 結構、固定價或設價格區間，多數合約五年期（汽車業約三年期），目的是提高營收可預測性與韌性、減緩產業傳統景氣循環。","source":"wccftech - \"Micron Signs Up 16 Strategic Customer Agreements For Memory In A 5-Year Plan\" (https://wccftech.com/micron-signs-up-16-strategic-customer-agreements-for-memory-in-a-5-year-plan/); Market Ontology (https://marketontology.com/events/2026-07-04/micron-secures-100b-in-multiyear-strategic-customer-agreements)","url":null,"excerpt":null,"as_of":"2026-07-04","retrieved_at":"20261020","affects":["thesis.H","moat_trend","valuation"],"status":"ok"},{"id":"capital_markets_pricing#0","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-06-24 公司給 FQ4'26 EPS 指引 $30-32，高於當時共識 $24.3；營收指引 $49-51B，較前一季指引區間 $32.75-34.25B 上調（Benzinga 彙整）","source":"Benzinga MU earnings page","url":"https://www.benzinga.com/stock/MU/earnings","excerpt":"The company guided earnings per share in the range of $30 - $32, compared to a consensus EPS estimate of $24.3.","as_of":"2026-06-24","retrieved_at":"20261020","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#1","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Benzinga 統計 2022-09-29 至 2026-06-24 共 18 次指引更新，14 次上調、3 次下調；2026 年內搜尋未見指引下調","source":"Benzinga MU earnings page","url":"https://www.benzinga.com/stock/MU/earnings","excerpt":null,"as_of":"2026-06-24","retrieved_at":"20261020","affects":["valuation","thesis.R"],"status":"ok"},{"id":"capital_markets_pricing#2","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-09-30 FQ1'27 指引：EPS $37.15-39.15（共識 $35.36），營收 $60-63B（Benzinga 彙整，搜尋摘要為轉述，未讀原頁）","source":"Benzinga MU earnings page","url":"https://www.benzinga.com/stock/MU/earnings","excerpt":null,"as_of":"2026-09-30","retrieved_at":"20261020","affects":["valuation","thesis.H"],"status":"ok"},{"id":"capital_markets_pricing#3","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"2026-08 初 Benzinga 快照：約 26 位分析師、共識 Buy（25 Buy／1 Hold）、平均目標價約 $1,308，較當時價 $877.57 高約 49%；7 月 Citi 目標價降至 $1,150、KeyBanc 升至 $1,750","source":"Benzinga MU price targets","url":"https://kr.benzinga.com/quote/MU/price-targets","excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261020","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#4","axis":"capital_markets_pricing","section":"coverage","direction":"0","claim":"Walnut 2026-08 頁面：42 位分析師平均目標價 $1522.26；2026-07-14 KeyBanc 目標價自 $1600 升至 $1750（Overweight）。與 Benzinga 的 $1,308 並列，來源口徑不一致，分布以區間看","source":"Walnut Invest MU forecast","url":"https://walnutinvest.com/stocks/mu/forecast","excerpt":null,"as_of":"2026-08-01","retrieved_at":"20261020","affects":["valuation"],"status":"ok"},{"id":"capital_markets_pricing#5","axis":"capital_markets_pricing","section":"coverage","direction":"+","claim":"Goldman Sachs：Micron 單一公司佔 S&P 500 自「戰爭開始」以來 EPS 上修的 51%","source":"Seeking Alpha news: Micron alone accounts for 51% of all S&P 500 EPS revisions since the war began - Goldman Sachs","url":"https://seekingalpha.com/news/4576710-micron-alone-accounts-for-51-of-all-sp-500-eps-revisions-since-the-war-began-goldman-sachs","excerpt":"Micron alone accounts for 51% of the entire S&P 500's EPS revision since the war began, according to Goldman Sachs Research.","as_of":"2026-04-01","retrieved_at":"20261020","affects":["valuation","thesis.H"],"status":"ok"},{"id":"major_events#0","axis":"major_events","section":"coverage","direction":"-","claim":"2026-06-25 於 N.D. Cal. 提起 DRAM 買方集體反托拉斯訴訟，被告含 Micron、Samsung、SK hynix，指控限制供給與操縱價格（期間自 2022-10-26 起）；2026-07-17 夏威夷聯邦地院另有類似個人訴訟","source":"SEC EDGAR 10-K FY2026 Item 8 Antitrust Matters","url":"https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm","excerpt":"On June 25, 2026, certain individuals and businesses filed a putative class action complaint in N.D. Cal. against Micron, Samsung Electronics Co., Ltd. and one of its subsidiaries, and SK hynix Inc. and one of its subsidiaries, on behalf of a putative class of purchasers of DRAM products, alleging that the defendants conspired to restrict the supply of, and fix prices for, DRAM products in violation of the Sherman Act and various state antitrust and consumer protection laws, for a period beginning October 26, 2022.","as_of":"2026-10-09","retrieved_at":"20261020","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"major_events#1","axis":"major_events","section":"coverage","direction":"0","claim":"YMTC 於 2025-06-07 提 Lanham Act 訴訟，2026-08-13 地院駁回，2026-08-24 YMTC 提上訴","source":"SEC EDGAR 10-K FY2026 Item 8 Other Matters","url":"https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm","excerpt":"On August 13, 2026, the District Court granted the defendants’ motions to dismiss YMTC’s complaint. On August 24, 2026, YMTC filed a notice of appeal to the U.S. Court of Appeals for the District of Columbia Circuit.","as_of":"2026-10-09","retrieved_at":"20261020","affects":["decision_inputs.bear"],"status":"ok"},{"id":"major_events#2","axis":"major_events","section":"coverage","direction":"+","claim":"2026-01 宣布以 18 億美元現金購買力積電 Tongluo P5 晶圓廠之意向書，預期 2026 年第二季底前完成（搜尋摘要未確認是否已交割）","source":"Barchart/Nasdaq 報導 Micron letter of intent PSMC Tongluo","url":"https://www.barchart.com/story/news/37094883/micron-signs-letter-of-intent-to-purchase-tongluo-site-begin-strategic-partnership-with-psmc","excerpt":null,"as_of":"2026-01-17","retrieved_at":"20261020","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#0","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"SK Hynix 董事長警告，全球記憶體供給到 2030 年前可能持續低於需求約 20%；多家供應商雖計畫 2027 年開出新產能，但建廠、設備安裝與原料準備會拖到 2027 下半年才有實質量產，2028 年才會有明顯產出貢獻。","source":"IG International, \"Memory chip supercycle 2026: what is driving the DRAM, HBM rally\" (citing Bank of America research)","url":null,"excerpt":null,"as_of":"2026-07-08","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#1","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"Kioxia 於 1 月確認其 2026 全年 NAND 產出已全數被訂走，部分大型雲端客戶要求延伸至 2027、2028 年的供貨協議；TrendForce 判斷 NAND 有意義的產能擴張要到 2027 年底或 2028 年才會出現。","source":"TrendForce press release, \"Diverging Memory Market Outlook in 2027 as DRAM Supply Remains Tight While NAND Flash Supply Conditions Ease\"","url":null,"excerpt":null,"as_of":"2026-07-30","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#2","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"三星與 SK 海力士（合計約占全球 DRAM 產能 70%）向投資人表態不打算積極擴產，維持紀律性產出以在當前價位下最大化獲利；TrendForce 判斷 2026 年記憶體業維持保守資本支出，對位元供給成長影響有限。","source":"TrendForce press release, \"Memory Industry to Maintain Cautious CapEx in 2026, with Limited Impact on Bit Supply Growth\"","url":null,"excerpt":null,"as_of":"2025-11-13","retrieved_at":"20261020","affects":["moat_trend","thesis.H","decision_inputs.bear"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#3","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"SK 海力士 2026 年資本支出預估達 205 億美元（年增 17%），主要投入 M15X 廠的 HBM4 產能擴充；三星 2026 年資本支出約 200 億美元（年增 11%），聚焦 1c 製程 HBM 產能與小幅擴充 P4L 晶圓產能。兩者新增資本支出多導向 HBM，一般伺服器與消費型 DRAM 的增量產能因此受限。","source":"Global Semi Research Substack, \"2026 Memory Industry Insights\" (citing SK hynix/Samsung capex guidance)","url":null,"excerpt":null,"as_of":"2026-01-01","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"cyclical_supply_discipline_capacity#4","axis":"cyclical_supply_discipline_capacity","section":"coverage","direction":"+","claim":"SK 海力士表示 DRAM 供給緊俏狀況將延續至 2026 下半年；DRAM 業潔淨室產能有限，僅三星與 SK 海力士能小幅擴充產線，其餘同業擴產空間受限。","source":"Suntsu Blog, \"Memory Market Update Q2 2026: Navigating the Shortage\"","url":null,"excerpt":null,"as_of":"2026-05-06","retrieved_at":"20261020","affects":["moat_trend","thesis.H"],"status":"ok"},{"id":"cyclical_inventory_price_position#0","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"TrendForce report: AI server demand driving memory contract price increases in 2Q26; conventional DRAM contract prices forecast to rise 58-63% QoQ, NAND Flash contract prices forecast to rise 70-75% QoQ, as CSPs secure supply via long-term agreements.","source":"TrendForce, \"AI Server Demand to Drive Memory Contract Price Increases in 2Q26 as CSPs Secure Supply via Long-Term Agreements\", https://www.trendforce.com/presscenter/news/20260331-12995.html","url":null,"excerpt":null,"as_of":"2026-03-31","retrieved_at":"20261020","affects":["thesis.H","valuation"],"status":"ok"},{"id":"cyclical_inventory_price_position#1","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce spot price update: DRAM spot prices extending a gradual downtrend on contained selling pressure, with DDR4 spot dropping 1.18% in the week, even as DRAM contract prices continued rising in the same period.","source":"TrendForce, \"[Insights] Memory Spot Price Update: DRAM Extends Gradual Downtrend on Contained Selling Pressure; DDR4 Drops 1.18%\", https://www.trendforce.com/news/2026/04/08/insights-memory-spot-price-update-dram-extends-gradual-downtrend-on-contained-selling-pressure-ddr4-drops-1-18/","url":null,"excerpt":null,"as_of":"2026-04-08","retrieved_at":"20261020","affects":["thesis.H","thesis.R","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#2","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"TrendForce: AI server demand continues to support memory prices into 3Q26, but price gains are moderating versus Q2 as consumer demand weakens and high year-over-year base effects take hold; DRAM contract prices forecast to rise only 13-18% QoQ (vs 58-63% in Q2), NAND Flash contract prices forecast to rise 10-15% QoQ (vs 70-75% in Q2).","source":"TrendForce, \"AI Server Demand Continues to Support Memory Prices in 3Q26, but Gains Moderate as Consumer Demand Weakens and High Base Effects Take Hold\", https://www.trendforce.com/presscenter/news/20260703-13134.html","url":null,"excerpt":null,"as_of":"2026-07-03","retrieved_at":"20261020","affects":["thesis.H","thesis.R","decision_inputs.bear","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#3","axis":"cyclical_inventory_price_position","section":"coverage","direction":"0","claim":"Contract and spot memory prices diverged sharply by mid-2026: DDR4 8Gb contract price rose from $11.50 (January) to $24.00 (July), a 109% YTD increase; 128Gb MLC NAND contract price rose from $9.46 to $30.05, a 218% YTD increase. Meanwhile spot prices lost momentum — DDR4 1Gx8 spot chips rose only 0.17% week-over-week ($42.04→$42.11) and 512Gb TLC wafer spot prices rose 4.55% but on thin trading volume, signaling weak end-demand pull-through even as contract prices (allocation-driven, tied to AI/HBM capacity diversion) hit record highs.","source":"BigGo Finance, \"Memory Price Rally Diverges: Contract Prices Hit Record Highs in July as Spot Market Momentum Fades\", https://finance.biggo.com/news/592b3c55-bfb8-488e-89aa-70632fd3c331","url":null,"excerpt":null,"as_of":"2026-08-05","retrieved_at":"20261020","affects":["thesis.H","thesis.R","decision_inputs.bear","valuation","triggers"],"status":"ok"},{"id":"cyclical_inventory_price_position#4","axis":"cyclical_inventory_price_position","section":"coverage","direction":"+","claim":"Micron Technology 10-Q for the fiscal quarter ended May 28, 2026 (FY2026 Q3): ending inventory was $8.6 billion with days of inventory at 120, reflecting DRAM conditions still below target inventory days industry-wide and supporting continued pricing power across mainstream and AI-optimized parts.","source":"Micron Technology Inc, Form 10-Q FY2026 Q3 (SEC EDGAR filing mu-20260528.htm), https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000015/mu-20260528.htm","url":null,"excerpt":null,"as_of":"2026-05-28","retrieved_at":"20261020","affects":["moat_trend","thesis.H","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#0","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"在 2023 年那波記憶體下行中，DRAM 與 NAND 價格自 2021 年第 3 季高點起分別下跌 57% 與 55%；2023 年 DRAM 市場營收萎縮至 420 億美元（年減 47%），NAND 萎縮至 370 億美元（年減 37%）","source":"StorageNewsletter, 'WW 2023 Memory Market Declining to $42 Billion for DRAM (-47% Y/Y) and $37 Billion for NAND (-37% Y/Y)'","url":null,"excerpt":null,"as_of":"2023-07-21","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#1","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Micron FY2023（截至 2023 年 8 月）毛利轉負，毛利為 -14.16 億美元（營收 155.4 億美元），全年淨損 58.33 億美元","source":"Micron Technology Inc, SEC Form 8-K FY2023 press release","url":null,"excerpt":null,"as_of":"2023-09-27","retrieved_at":"20261020","affects":["thesis.R","decision_inputs.bear","moat_trend"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#2","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"-","claim":"Micron 單季毛利率在 2023 年 8 月觸及近 5 年低點 2.7%","source":"Macrotrends, 'Micron Technology Gross Margin 2012-2026'","url":null,"excerpt":null,"as_of":"2023-08-31","retrieved_at":"20261020","affects":["thesis.R","valuation"],"status":"ok"},{"id":"cyclical_prior_downcycle_behavior#3","axis":"cyclical_prior_downcycle_behavior","section":"coverage","direction":"0","claim":"近三次記憶體週期的高峰到谷底時間：1993-1996 週期約 2 年；2016-2019 週期基本面高峰到谷底約 6-7 季；2020-2023 週期毛利率壓縮期約 6-8 季；歷史上營收跌幅通常落在 25%-40%，毛利率從 50%+ 高點壓縮到 20% 出頭甚至轉負","source":"Uncover Alpha (Substack), 'Every Memory Cycle Ends the Same. Until It Doesn't.'","url":null,"excerpt":null,"as_of":"2026-03-12","retrieved_at":"20261020","affects":["thesis.R","thesis.H","decision_inputs.bear","triggers"],"status":"ok"},{"id":"ma_merger#0","axis":"ma_merger","section":"events","direction":"+","claim":"2026-01 宣布以 18 億美元現金購買力積電 Tongluo P5 晶圓廠之意向書（資產購買，非公司併購），預期 2026 年第二季底前完成；搜尋摘要未確認交割","source":"Barchart/Nasdaq 報導 Micron letter of intent PSMC Tongluo","url":"https://www.barchart.com/story/news/37094883/micron-signs-letter-of-intent-to-purchase-tongluo-site-begin-strategic-partnership-with-psmc","excerpt":null,"as_of":"2026-01-17","retrieved_at":"20261020","affects":["thesis.H","valuation"],"status":"ok"},{"id":"lawsuit_class_action#0","axis":"lawsuit_class_action","section":"events","direction":"-","claim":"2026-06-25 N.D. Cal. DRAM 買方集體反托拉斯訴訟（Micron、Samsung、SK hynix）","source":"SEC EDGAR 10-K FY2026 Item 8 Antitrust Matters","url":"https://www.sec.gov/Archives/edgar/data/723125/000072312526000023/mu-20260903.htm","excerpt":"On June 25, 2026, certain individuals and businesses filed a putative class action complaint in N.D. Cal. against Micron, Samsung Electronics Co., Ltd. and one of its subsidiaries, and SK hynix Inc. and one of its subsidiaries, on behalf of a putative class of purchasers of DRAM products","as_of":"2026-10-09","retrieved_at":"20261020","affects":["decision_inputs.bear","valuation"],"status":"ok"},{"id":"lawsuit_class_action#1","axis":"lawsuit_class_action","section":"events","direction":"+","claim":"證券集體訴訟（2023-2024 需求復甦陳述）經 Kessler Topaz 案件頁：2026-02-03 法院准予駁回動議，2026-04-03 原告自願撤訴，案件結束（律所頁面轉述，未讀原頁）","source":"Kessler Topaz Meltzer & Check 案件頁（搜尋摘要）","url":"https://www.ktmc.com/?p=9958","excerpt":null,"as_of":"2026-04-03","retrieved_at":"20261020","affects":["decision_inputs.bear"],"status":"ok"},{"id":"clinical_fda#none","axis":"clinical_fda","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"product_recall_warning#none","axis":"product_recall_warning","section":"events","direction":null,"claim":null,"status":"none","source":null,"as_of":null},{"id":"sec_investigation_restatement#0","axis":"sec_investigation_restatement","section":"events","direction":"0","claim":"經查 8-K 清單近12個月 10 份，重大項目 2 份均為 Item 8.01 債券要約收購，無 Item 4.02（財報不可信賴）；搜尋亦未見 SEC 調查或重編","source":"SEC EDGAR 8-K 申報清單","url":"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000723125&type=8-K","excerpt":"【程式統計】SEC EDGAR 申報清單，2025-10-20 至 2026-10-20 共 10 份 8-K；其中含重大項目（1.01／1.02／1.03／2.01／2.05／2.06／3.01／4.02／5.01／8.01 等）者 2 份。","as_of":"2026-10-20","retrieved_at":"20261020","affects":["decision_inputs.bear"],"status":"ok"}],"gaps":[{"topic":"法說問答未正面回答項","question":"q6_how_wrong","why":"digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口","tried":["digest.qa_flags"]}],"peer_comparison":{"metrics":[{"key":"gross_margin_pct","label":"毛利率","unit":"%"},{"key":"operating_margin_pct","label":"營業利益率","unit":"%"},{"key":"fcf_margin_pct","label":"FCF 利潤率","unit":"%"},{"key":"rd_intensity_pct","label":"研發密度","unit":"%"}],"rows":[{"name":"MU","period":"TTM ending 2026-05-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":72.57,"operating_margin_pct":65.67,"fcf_margin_pct":28.99,"rd_intensity_pct":5.3},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.MU","as_of":"TTM ending 2026-05-31（4季加總）"},"is_subject":true},{"name":"NVDA","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":74.67,"operating_margin_pct":65.21,"fcf_margin_pct":41.92,"rd_intensity_pct":7.79},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.NVDA","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"TSM","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":64.23,"operating_margin_pct":56.1,"fcf_margin_pct":25.33,"rd_intensity_pct":6.07},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.TSM","as_of":"TTM ending 2026-06-30（4季加總）"}},{"name":"AVGO","period":"TTM ending 2026-07-31（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":68.77,"operating_margin_pct":48.52,"fcf_margin_pct":44.22,"rd_intensity_pct":13.28},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AVGO","as_of":"TTM ending 2026-07-31（4季加總）"}},{"name":"AMD","period":"TTM ending 2026-06-30（4季加總）","basis":"yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）","values":{"gross_margin_pct":53.2,"operating_margin_pct":15.71,"fcf_margin_pct":20.34,"rd_intensity_pct":22.74},"source":{"type":"evidence_numbers","ref":"numbers.peer_financials.AMD","as_of":"TTM ending 2026-06-30（4季加總）"}}],"subject":"MU"},"financial_history":{"ticker":"MU","currency":"USD","method":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。","source":"yfinance income_stmt／cashflow（annual）","note":null,"years":[{"fiscal_year_end":"2022-08-31","revenue":30758000000.0,"revenue_yoy_pct":null,"gross_margin_pct":45.18,"operating_margin_pct":31.57,"net_income":8687000000.0,"diluted_eps":7.75,"free_cash_flow":3114000000.0,"fcf_margin_pct":10.12,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[0]","as_of":"2022-08-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2023-08-31","revenue":15540000000.0,"revenue_yoy_pct":-49.48,"gross_margin_pct":-9.11,"operating_margin_pct":-34.78,"net_income":-5833000000.0,"diluted_eps":-5.34,"free_cash_flow":-6117000000.0,"fcf_margin_pct":-39.36,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[1]","as_of":"2023-08-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2024-08-31","revenue":25111000000.0,"revenue_yoy_pct":61.59,"gross_margin_pct":22.35,"operating_margin_pct":5.2,"net_income":778000000.0,"diluted_eps":0.7,"free_cash_flow":121000000.0,"fcf_margin_pct":0.48,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[2]","as_of":"2024-08-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}},{"fiscal_year_end":"2025-08-31","revenue":37378000000.0,"revenue_yoy_pct":48.85,"gross_margin_pct":39.79,"operating_margin_pct":26.24,"net_income":8539000000.0,"diluted_eps":7.59,"free_cash_flow":1668000000.0,"fcf_margin_pct":4.46,"source":{"type":"evidence_numbers","ref":"numbers.financial_history.years[3]","as_of":"2025-08-31","citation":"年度財報（yfinance annual income_stmt／cashflow，非 TTM），最近 4 個會計年度、舊到新排列；FCF＝Operating Cash Flow + Capital Expenditure（yfinance 的 Capital Expenditure 本身已為負值，相加即等於「營業現金流−資本支出」）。"}}]}}
```

---

## ④ 最新一季逐字稿全文

（來源：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/MU/MU_Q4_2026_Earnings_Call_20260930.md）

# Q4 2026 Earnings Call
**Micron Technology, Inc.** | Earnings Calls | 2026-09-30

**Operator** (Operator):
Hello, everyone. Thank you for joining us, and welcome to Micron's Fourth Quarter Post-Earnings Analyst Call. [Operator Instructions]
I will now hand the conference over to Satya Kumar, Corporate Vice President, Investor Relations and Treasury. Satya, please go ahead.

**Satya Kumar** (Executives):
Thank you, and welcome to Micron Technology's Fiscal Fourth Quarter 2026 Post-Earnings Analyst Call. On the call with me today are Manish Bhatia, President and Chief Operating Officer; Dr. Scott DeBoer, President and Chief Technology and Product Officer; and Mark Murphy, our Chief Financial Officer.
As a reminder, the matters we're discussing today include forward-looking statements regarding market demand and supply, market trends and drivers, and our expected results and guidance and other matters. These forward-looking statements are subject to risks and uncertainties that may cause actual results to differ materially from the statements made today. We refer to the documents that we filed with the SEC, including our most recent Form 10-K and upcoming 10-Q for a discussion of risks that may affect our results. 
Although we believe that the expectations reflected in the forward-looking statements are reasonable, we cannot guarantee future results, levels of activity, performance or achievements. We are under no duty to update any of the forward-looking statements to conform these statements to actual results. We can now open up the call for Q&A.

**Operator** (Operator):
[Operator Instructions] Your first question comes from the line of Ben Reitzes from Melius.

**Benjamin Reitzes** (Analysts):
Congrats on the promotion, Scott. I'm not sure if Manish is on, but congrats. So I wanted to ask about -- congrats, so wanted to talk about 2028, new commentary here regarding '28 and you guys felt compelled to kind of say you see things tighter in '28 than this year as well as '27. I wanted to know a little bit more about what changed and what that means for margins. You gave more margin commentary than you usually do around '27, which was great, by the way, but I just don't see any reason why margins would change in '28 from the level you implied for '27. So just a little more comment around '28 would be great.

**Manish Bhatia** (Executives):
Sure, Ben. I can start, and then if Mark wants to add anything, and thank you for the shout-out. In terms of 2027 and 2028 in our commentary, we are seeing stronger demand drivers than we've seen before. We commented about the server units continuing to grow into '27. And of course, I think everybody is talking about how agentic AI is really growing fast, and that's creating a CPU-driven demand stream as well. And so as we've gone through working on our fiscal year '27 and we commented that we have more than 75% of our shipments committed for the year that shows a strengthening demand and allows us to shift our conversations on allocation with our customers out to 2028.
And so that's one element of our confidence is that '27 is shaping up with stronger demand than maybe we had seen before. And then, of course, as we also have now more SCA conversations with customers, including extensions that we've now negotiated that gives us more confidence in the long term as well. And so the combination of those two things gives us very strong outlook for demand through 2028. 
And then on the supply side, there's still the same structural constraints on supply growth that we've talked about before, which is diminishing returns from technology transitions versus past technology transitions. HBM growing faster than conventional DRAM through 2028, which means that as a portion of the industry's output capability, HBM is growing in terms of that share. And of course, the trade ratio, not just today's trade ratio for HBM, but future more complex HBM having higher trade ratios, that's also going to be constraining supply. 
And then it just takes a long time for these new clean rooms that the whole industry is working on to be able to build and then qualify and then equip and it takes -- even from the time they open, it takes a few quarters for meaningful shipments to come. So that really gave us the combination of that demand outlook and this supply outlook. We made the statement that we really don't have line of sight to when supply and demand balances.

**Mark Murphy** (Executives):
Yes, Ben, I would maybe just add to Manish's comments that as you noted in '27, we had indicated for the balance of the year that we would see margin expansion relative to Q1, a function of continued price increases, albeit at a more moderate pace. And we've said that for some time that eventually price increases would moderate. And then at that point, in addition to just price increases at a lower rate, we would -- we have a better mix of products, and we would work our mix based on our technology and product leadership. 
And the market conditions, as we said, we would expect to remain tight, and that would be supportive through '28. And of course, the partial offset to price and favorable mix would be start-up costs. But these are all things we're managing. We've been managing them, and we would expect to be able to sustain strong financial performance.

**Benjamin Reitzes** (Analysts):
Great. And if I could just sneak one other in. I mean, Sanjay had a great seat at the Trump, I guess, lunch, dinner, whatever, lunch. And just wondering, did he come away feeling good about the industry's ability to grow and self-regulate and the future coming out of that meeting, did that lend a hand any of the upbeat guidance he gave? Or just any color out of that and how he felt coming out and even if memory came up a lot at the meetings.

**Manish Bhatia** (Executives):
Well, Ben, Sanjay is not here, but I'll give you what conversations I am aware of. For sure, we're very happy to participate in that forum. And it does show the importance of memory that Micron was invited there along with the model companies as well as the accelerator companies. I think that the framework that in the white paper or the -- that was published out of that, that many of the model companies have already signed is that, that framework is constructive towards continuing to have advancement in AI infrastructure and AI, in particular, AI hardware infrastructure.
And I know that one of the concepts that got discussed quite a bit was that the way to manage some of the security aspects is to actually have security solutions, which will require more advanced hardware, including higher performance memory, lower latency memory, as part of those security solutions, higher bandwidth memory because if you can imagine, setting up a gateway to be able to manage much of the security aspects that could be proposed in the future, those -- the responsiveness of those gateways are going to depend a lot on the availability of performance and low latency memory.

**Operator** (Operator):
Your next question comes from the line of Melissa Weathers from Deutsche Bank.

**Melissa Weathers** (Analysts):
My congrats as well to the 2 new promotees. On the -- and -- in past quarters, you've given us a view on where you think the HBM total TAM could be by 2028, 2030. Clearly, the pricing environment has changed since those updates. I don't know if you want to give us an official new number for where you think that HBM TAM could go. But like directionally, can you help us sort of try to size like how much is coming from bits and how much is coming from pricing? And just any updated views on how big you think that market could be?

**Manish Bhatia** (Executives):
Sure, Melissa. Thank you again. We are not updating that TAM outlook right now. But what we have said is that HBM shipments, we expect to grow faster than conventional DRAM. That means that HBM will continue to gain -- to grow as a portion of the industry's capacity here through 2028. And the pricing for HBM, at least for us, we did comment that we have increased that pricing significantly for calendar year '27, which will reset at the beginning of the calendar year to narrow the profitability gap with conventional DRAM. But beyond that, we haven't made any comments on the specific outlook for the HBM TAM. It continues to grow. It continues to be a very important enabler. HBM deployments continue to be an important enabler of much of the rest of the AI to be able to reach its potential as well. So it's an important part of the market.

**Melissa Weathers** (Analysts):
Got it. Maybe following up on that. From a market share perspective, any updated view on how you guys are targeting market share for HBM? In the past, you said you want to get it to within the corporate average, kind of low 20s percent market share. So is that still the case? And then I noticed in the prepared remarks, your comments on HBM4E and the engagements with NVIDIA there. So just any more color on 2027, and HBM4E and the progress that you're making there with customers would be great.

**Manish Bhatia** (Executives):
Sure. Sure. I'll take the first and then maybe Scott can take the HBM4E since he is driving that product development. In terms of the HBM market share, about a year ago, we had achieved the milestone that we talked about that our HBM market share reached our broader DRAM market share. And at that time, we said that our goals would then move around based on various different factors. And we haven't really updated exactly our HBM share target other than to say that we do expect our HBM share to be around our broader DRAM market share, but we're not necessarily targeting one number or the other. 
It will move around based on various different factors there. But as I mentioned on the prior question, it's a really important part of the market. It allows us to be very close to the leading edge of the accelerator platforms that many of our customers are designing and then deploying, and it's a key enabler for all the rest of AI to be able to deliver on its promise and its potential.

**Scott DeBoer** (Executives):
And then I can just add a little bit about the work with NVIDIA on what really will be the first major custom HBM product out in the market. And we've been working with NVIDIA for over a year on HBM4E, what's called NVHBM. And we see substantial opportunity there for us in the co-design of that product with obviously a key customer to have this be a product that delivers really substantial value beyond standard HBM4E. And I think it will be a real impact on industry showing where future system [indiscernible] would optimize their products.

**Operator** (Operator):
Your next question comes from the line of Atif Malik from Citi.

**Atif Malik** (Analysts):
The first one on the 26 SCAs, 35% of sales by 2030. Are these for both DRAM and NAND? And if you can just split them out?

**Manish Bhatia** (Executives):
Atif, yes. We're not splitting those out, but the SCA agreements do cover both DRAM and NAND. And it is through 2030, but we're not breaking it out specifically. I can tell you that the DRAM volume is a little bit less than that, approximately 35%, and the NAND bit volume is a little bit more. And as we think about these going forward, we are -- we have more availability. As we said, that this number could get up to be higher in the future as we continue negotiations for SCA.

**Atif Malik** (Analysts):
Understood. And then on the impact of China competition, firstly, if you can confirm that your China sales exposure is fairly minimal. And if Scott can comment on how should we see kind of China competitors kind of closing the gap on technology, if you can provide any color.

**Manish Bhatia** (Executives):
So on the first question, yes, our exposure to China has been reducing over the last couple of years in the last several quarters, and we expect the exposure will be in the single-digit range in fiscal '27.

**Scott DeBoer** (Executives):
Then I could comment a little on the technology side. Currently, our technology leadership is at least 2 nodes ahead of the China competition. I think it's important to say that our focus is on maintaining technology leadership and having true differentiation in our products in how we compete. We're -- as Manish, I think, mentioned earlier and as it was mentioned in the call, our 1-gamma DRAM technology is already the majority of our bits, and it's set up to be the largest node in the company's history. It is dependent on EUV technology. The next-generation 1-delta is well underway, and we're focused on the ramp of that in the second half of next year. EUV technology is critical to all advanced DRAM nodes going forward. And our expertise in that, both from the technology side in partnership with our supplier there as well as mask technology and other things is -- continues to be a key differentiator for Micron.

**Atif Malik** (Analysts):
And Manish, well-deserved for that promotion.

**Manish Bhatia** (Executives):
Thank you, Atif. And can I just clarify that the response in terms of DRAM and NAND was actually a bit comment. Just to make sure that, that was clear. I'm not sure I specified. So making sure it's clear.

**Operator** (Operator):
Your next question comes from the line of Karl Ackerman from BNP Paribas.

**Karl Ackerman** (Analysts):
Yes. You are seeing robust demand across much of your portfolio, but this quarter does appear to be the second quarter in a row that mobile and client segment saw bit shipments decline. Are higher memory prices reducing demand in this area of the market? And while this area of the market has been slow to adopt SCAs, I'm curious if your growth in SCAs is coming from this cohort?

**Manish Bhatia** (Executives):
Thanks, Karl. We did see sequential bit decline in our mobile and client business unit, but we did see revenue growth, obviously, with both higher pricing and favorable mix. I think what's important to note is that the premium segments of the both clients as well as the flagship smartphones do see robust demand for higher content, higher performance solutions. And that's a segment that, of course, we're -- those are the segments that, of course, we're very focused on. And with that wind at their back, we see the PC and mobile industry revenue to be growing even though we do see unit volumes declining. 
And in terms of SCAs, I'll just comment that we do have SCAs across all of our business units, including the mobile and client business unit. And we're not specifically breaking them out, but I will tell you that we have SCAs because it's important for us to be maintaining diversified supply to all our end markets.

**Karl Ackerman** (Analysts):
Got it. Yes. Maybe a question for Scott, if I could. How do you view the competitiveness of your in-house optimized base die on HBM4E versus peers? Certainly, some of these customers are seeing custom solutions. Does the complexity and economic value flow primarily through the compute customers or to the HBM providers?

**Scott DeBoer** (Executives):
So maybe just a little clarification first. On HBM4E, we have co-designed with NVIDIA, but not in-house base die like we use on HBM4. So I think just to be clear on your question, I just wanted to be sure I was answering it in the right way. On HBM4E, this co-design is on a foundry process, both for the customized product and for the JEDEC-specified product. 
Okay, so the -- and then I think maybe to add a little color to that. The differentiation, just as we have demonstrated in the past on HBM, prior HBM products, winds up being in the power and the ultimate speed performance and the margin of the product working with our customers. That in all previous generations hasn't been the same between different suppliers and that we think will continue to be a strength of Micron in terms of quality of the product and the capabilities that we're able to put out.

**Manish Bhatia** (Executives):
And then, Karl, in terms of your question on economic value, HBM is a premium product. And as Scott mentioned, as we look at the NVHBM with customization, we do expect that to be a high-value product as well. And we're confident that HBM will continue to contribute and be a strong ROI product for us.

**Operator** (Operator):
Your next question comes from the line of Jim Schneider from Goldman Sachs.

**James Schneider** (Analysts):
Congratulations, Manish and Scott. I just wanted to maybe get a sense about -- of the 10 new customer SCAs you signed in the quarter, maybe give us a little bit of color on what customers are asking for? Obviously, they want supply, and they want longer-dated supply. But is there any kind of change in the pricing construct either you or they are asking for? Sort of given -- the reason I ask the question is kind of given the expectation about tightness through calendar '27 and '28. Are you maybe a little bit less inclined to call for the fixed ceiling and floor pricing if you think you can capture a little bit more upside over the next couple of years?

**Manish Bhatia** (Executives):
Yes, yes. Well, thanks, Jim. And thanks for the shout out. I would say that the framework of the SCAs that we have is similar. But what's different is that the negotiations reflect current market conditions and outlook for market pricing, right? And so the direction of travel has been for higher pricing. And so those are now factored into the discussions that we're having with customers versus the prior ones, which we had talked about that were set at CQ2 kind of market conditions.
And as I think we gave color that about 3/4 of the SCA have this -- of the SCA revenue has a defined pricing framework and about one quarter is open to periodic negotiations or pricing that move with market dynamics. Of the -- so I guess I would answer that in terms of the overall framework, similar. The majority of the pricing frameworks have floor and ceiling bands, but the newer ones are negotiated with an eye towards the current market conditions and the future market tightness that we see.

**James Schneider** (Analysts):
Got it. I mean just to be clear, does that mean all the pricing ceilings and floors just reset to the higher market conditions you're seeing today? Or is the nature of the pricing condition is actually different, too? And then maybe just to ask, just curious as to whether -- I don't think you've disclosed signing initial hyperscale customers. I'm wondering if those are included in the TAM.

**Manish Bhatia** (Executives):
Yes. So I mean there are multiple different frameworks. What I commented on is that the majority of the frameworks that have pricing are set with floor and ceiling, but there are multiple different frameworks that we're continuing to use. And since the last call in these new 10, we've signed a range of agreements from small to large SCA customers. We're not commenting specifically, even in the previous question, not specifically breaking out which one, just commenting that we now have SCAs across all of our business units, and we have SCAs ranging from small to large, even in the last 10 that we signed. And of course, in the total 26.

**Operator** (Operator):
Your next question comes from the line of Chris Caso from Wolfe Research.

**Christopher Caso** (Analysts):
I guess our first question, if you could address the CapEx and the fab construction CapEx, the construction CapEx as compared to the tool purchases. And what I seem to hear in the comments is that the construction CapEx was increasing faster. And I'm not sure I interpreted that correctly. But understand that there's -- the clean room space constraints are constraining the ability to bring in tools for this year. But the increase in construction CapEx is obviously interesting because it doesn't result in bit production until at least '29, probably beyond that.

**Manish Bhatia** (Executives):
So Chris, I can start and then maybe Mark can add. But I mean, that's exactly right, is that the principal constraint in the industry is on clean room space because we -- the strong growth of AI in this demand vector has come on relatively recently in terms of the time line that it takes to build these clean rooms. So while we're all starting. That's why we're focusing there. And then -- you're right that we did comment that the majority of the construction CapEx increase for fiscal '27 versus our prior plans is for clean rooms that will come online in late '28 and beyond, which shows both how long it takes to build these clean rooms and why we need to get started with the construction investments now.
But also shows our confidence in longer-term demand, both through the observation of the demand trends in the near-term market trends that we're seeing as well as the structure of the SCAs and the discussions we're having with SCAs and customers now extending those commitments beyond 2030. I mean these SCAs are transformational for us in terms of being able to match supply with future demand and to be able to invest with confidence.

**Mark Murphy** (Executives):
Yes. Chris, maybe I can just add that, just to make it clear that the majority of the increase is for construction CapEx. Most of that construction increases to accelerate clean room space availability in '28 and beyond. I mean it is a trend that we would expect to continue to beyond '27. And I think you made a very important point that just the spend there doesn't translate into bits and that these fabs will be made -- we put the equipment in the fabs and produce wafers when needed based on our view of the market and these SCAs are a good way for us to keep a pulse on the market and make sure that we get a return on that CapEx.

**Manish Bhatia** (Executives):
And I can -- just a couple -- just one other point. One other point, Chris, is that we will equip the clean rooms and build capacity to the demand trends that we see. So that's just another important point. And we have been executing long-term supply agreements with equipment suppliers to be able to make sure we have access to equipment as needed. But of course, we'll still equip and build the production capacity in those clean rooms in line with demand trends at the time.

**Christopher Caso** (Analysts):
Of course. Okay. As a follow-up question, I want to ask a question on the impact of CPU strength. On both overall bit demand and your view of supply-demand balance. And obviously, that's probably been the biggest incremental surprise since the beginning of the year. You don't have the same trade ratio effects on CPU as you do on HBM. But I guess the question is, how significant is that in contribution to the supply-demand imbalance?

**Manish Bhatia** (Executives):
I think definitely, the realization that agentic workloads are executed across CPU has been a big driver. There is a large attach rate of both LP as well as DDR memory and SSD to enable those agentic workflows. The -- those agentic workflows are already starting. You're already starting to see multiple ones, whether in the enterprise or consumers being implemented and driving real value. And that's been one of the reasons that server units are growing so strongly, as we noted, in the high teens. And I think the other thing that this shows is that while it's just another vector of logic and logic silicon to grow to be able to take advantage of the AI trends. And so that is driving higher logic silicon and into the overall demand for AI compute and frankly, creating more of a constraint on DRAM and making clear that DRAM is the principal constraint versus logic or power to the data center. 
I mentioned the new -- there are many different software implementations for enterprise agentic workloads that we're all seeing. But seeing how quickly the Meta's Muse has been [indiscernible] just in the last couple of weeks since being released is just an example of how quickly the agentic workloads are realizing -- enabling consumers to realize real value.

**Operator** (Operator):
Your next question comes from the line of Joseph Moore from Morgan Stanley.

**Joseph Moore** (Analysts):
Great. In terms of supply growth decelerating next year, I guess that's a little surprising in the context of the CapEx. And I know you talked about some of the dampening effects of HBM, but I don't think that delta should be changing that much. So I just wonder if you could just kind of explain what the puts and takes are that supply would decelerate given the CapEx that you see.

**Manish Bhatia** (Executives):
Sure, Joe. And you're asking for both DRAM and NAND?

**Joseph Moore** (Analysts):
Yes, but principally DRAM.

**Manish Bhatia** (Executives):
Okay. I mean I think that we gave the color that HBM is growing faster than conventional DRAM. And the trade ratio as you move -- more of the industry is shifting from HBM3 to HBM4 and then towards later in the year in '27 HBM4E and these are increasing trade ratio. So if you just look at both of those two things happening together, that has a dampening effect on the ability for bit growth to be growing. And keep in mind that both the bit growth for us and other industry participants from new technology nodes, both over time as you make more of your transition, you don't have -- the timing of transitions affect how much bit growth you can have as well as the nature of the diminishing returns of each of those newer nodes. 
So these are all the factors that are going to be constraining supply. But of course, the principal one is clean room space for everyone. And even though there's -- we're going to be having first wafer output from our Idaho facility mid-calendar '27 and others in the industry as well, maybe opening clean rooms, meaningful supply growth takes a few quarters after that. So I think that's really the -- those are all the reasons why we see that DRAM is reducing supply industry shipments next year.

**Joseph Moore** (Analysts):
Okay. That's helpful. And then to the extent that if you end up having been conservative on industry supply and there's more supply next year -- can you talk about -- I mean it seems like there's a lot of pent-up demand. There's a lot of appetite to have more supply. We've seen de-speccing out of necessity for some of these AI racks and things like that? It seems like they'll just re-spec to higher levels if there's more supply, but am I too optimistic there? Just how do you think about that?

**Manish Bhatia** (Executives):
Yes. No, I think that's exactly the point that these are -- and Sanjay mentioned this on the main call, we definitely think that our customers are choosing to maximize the compute silicon shipments they can make with the available memory supply that they have. And as -- that does create latent demand for more memory to attach to those, which would then end up delivering higher system performance and improved performance at the end customers. But -- and so yes, that latent demand, I think, is aligned with your concept that were more memory to become available, it would have -- it would easily get put into use in higher content growth in AI workloads, whether attached to accelerators or CPUs.

**Operator** (Operator):
Your next question comes from the line of Mehdi Hosseini from Susquehanna International Group.

**Mehdi Hosseini** (Analysts):
A couple of follow-ons for me. You did highlight your NAND bit shipment in '26 is tracking below industry average. But what should we expect '27 through '28? Would you be able to be growing NAND bit demand or bit shipment in line with the industry average of 25%?

**Manish Bhatia** (Executives):
Mehdi, we're not commenting out that far, frankly, on either DRAM or NAND. We do expect conditions to be tight on NAND overall even as the industry is expected to grow in the mid-20% range in calendar '27 and '28. Some of the factors that account for our supply growth, we did -- we are utilizing some of the clean room space in Singapore now for our advanced R&D line for future NAND growth. We are also preparing for the ramp of our HBM facility in Singapore next year. And so some of the existing clean room with some pilot HBM operations. And so that's some of the reasons why our supply growth grew less than the industry this year. But we feel confident in our technology, and we do expect that our continued ramp to G9 will provide good, very high ROI, cost-effective supply for us as we move forward. And then, of course, we do have the new clean room that we broke ground on earlier this year that will come online in the second half of calendar year '28.

**Mark Murphy** (Executives):
Mehdi, just maybe if I can interject just because of time here. And then if you've got additional -- well, why don't you start with your question and then second question, I'll make a comment after that.

**Mehdi Hosseini** (Analysts):
Sorry, Mark. I didn't mean to interrupt you. But very quickly, I just want to get the team's opinion. When I look at DRAM, especially at the wafer level, the devices are all the same. And I argue that there is a fungibility of DRAM at the wafer level. And then there are some differentiation in the back end. And this fungibility at a wafer level hasn't been seen before because in the past, the cycles were driven by just one product, and there was a significant concentration of customers. So am I right with this assumption that fungibility of the DRAM at the wafer level gives you a better way of managing DRAM costs? Does that make any sense to you?

**Scott DeBoer** (Executives):
Maybe start with one thing. I think there's a bit of what you say, but I actually probably would have gone the other direction. And if you look at the front end variability or what we do differently on the DRAM processes between optimizing for HBM, optimizing for high-performance SOCAMM, LPDRAM and optimizing for DDR6. There's, at this moment in time, probably more difference than ever in the history of DRAM. And the same node, the different kinds of products that we have to build on it and a lot more differentiation built into those. I don't know what you would add, Manish?

**Manish Bhatia** (Executives):
Yes, I mean, I would say that it really helps us with in the near term, the fact that we do run the different products in the same manufacturing lines, it does help us adjust mix. We don't have to run products in different fabs. We can run them on the same lines. But as Scott mentioned, each product has its own vector that it is trying to optimize. Obviously, in HBM, it's bandwidth with the TSVs and that requires unique process steps. In DDR and LP, they each have their own as well process steps that are unique. And so I think the most important part of the fungibility is that we do have the ability to flex wherever demand is or even mix adjustments to try and meet our customers' requirements. I think that's probably the -- all within the same fab, that's probably the most important part. But I wouldn't say that it helps necessarily with cost.

**Mark Murphy** (Executives):
Yes. I think, Mehdi, just I think we're at the end of the call. And I am really happy to hear the nature of the questions being focused on technology and the longer-term strong foundation and performance of the business. And I just -- I thought there'd be a question that let me just do a couple of housekeeping things that I thought would come up earlier. Our first quarter guidance factors in a single-digit sequential bit growth and double-digit for cost for both DRAM and NAND and I wanted to make sure you had that for your modeling. And then also, excluding the incentive comp effects, the year-over-year R&D increase is going to be more than the $1 billion that we said last quarter, will be over $1 billion in '27 as we have added additional R&D activities. So again, I wanted to just make sure we got that out for your modeling.

**Operator** (Operator):
This concludes the Q&A and today's call. Thank you for attending. You may now disconnect.


---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MU_Q4_2026_Earnings_Call_20260930.md
- 2026-09-30｜Mark Murphy｜guidance：CFO 補充 FQ1 指引含的位元成長與成本降幅口徑（DRAM、NAND 皆是）（原話："single-digit sequential bit growth and double-digit for cost"）
- 2026-09-30｜Mark Murphy｜guidance：CFO 說明 FY27 研發費用年增幅（排除獎金效應）將超過上季所說的 10 億美元（原話："more than the $1 billion that we said last quarter"）
- 2026-09-30｜Manish Bhatia｜guidance：COO 表示 FY27 出貨已有超過七成五被承諾，因此配置談判延伸到 2028（原話："more than 75% of our shipments committed for the year"）
- 2026-09-30｜Manish Bhatia｜guidance：COO 對 2028 供需的說法：看不到供需平衡的時點（原話："don't have line of sight to when supply and demand balances"）
- 2026-09-30｜Manish Bhatia｜guidance：COO 說明 FY27 中國營收占比預期降到個位數（原話："exposure will be in the single-digit range in fiscal '27"）
- 2026-09-30｜Manish Bhatia｜guidance：COO 表示業界 DRAM 供給明年出貨下降；Idaho 首批晶圓出貨在 2027 年中（原話："first wafer output from our Idaho facility mid-calendar '27"）
- 2026-09-30｜Mark Murphy｜margin：CFO 拆解 FY27 毛利擴張來源：漲價放緩、產品組合改善，起動成本為部分抵銷（原話："the partial offset to price and favorable mix would be"）
- 2026-09-30｜Mark Murphy｜margin：CFO 說明 FY27 全年相對 Q1 仍有毛利擴張，來自持續但較溫和的漲價（原話："we would see margin expansion relative to Q1"）
- 2026-09-30｜Manish Bhatia｜margin：COO 說明 HBM 2027 曆年價格已大幅調升，以縮小與傳統 DRAM 的獲利差距（原話："to narrow the profitability gap with conventional DRAM"）
- 2026-09-30｜Manish Bhatia｜margin：CTO 回應同製程是否降成本：同產線可調組合，但 COO 稱不一定有助成本（原話："But I wouldn't say that it helps necessarily with cost."）
- 2026-09-30｜Scott DeBoer｜competition：CTO 稱技術領先中國競爭者至少兩個節點（原話："our technology leadership is at least 2 nodes ahead"）
- 2026-09-30｜Manish Bhatia｜competition：COO 對 HBM 市占目標的說法：約等於整體 DRAM 市占，不鎖定單一數字（原話："we do expect our HBM share to be around our broader DRAM"）
- 2026-09-30｜Scott DeBoer｜competition：CTO 稱各代 HBM 的差異在功耗、速度與產品良率，認為將持續是美光強項（原話："the first major custom HBM product out in the market"）
- 2026-09-30｜Scott DeBoer｜product：CTO 說明與 NVIDIA 共同設計 HBM4E（NVHBM），為首款主要客製 HBM 產品（原話："On HBM4E, this co-design is on a foundry process"）
- 2026-09-30｜Scott DeBoer｜product：CTO 澄清 HBM4E 共同設計不是自家基底晶粒，而是晶圓代工製程（與 HBM4 不同）（原話："On HBM4E, this co-design is on a foundry process"）
- 2026-09-30｜Scott DeBoer｜product：CTO 說明 1-gamma 已占多數位元，1-delta 預計明年下半年放量（原話："our 1-gamma DRAM technology is already the majority"）
- 2026-09-30｜Manish Bhatia｜product：COO 稱 DRAM 位元成長受 HBM 轉移與 HBM 交換比率上升壓抑（原話："these are increasing trade ratio"）
- 2026-09-30｜Manish Bhatia｜customer：COO 說明 SCA 涵蓋 DRAM 與 NAND，DRAM 比例略低於約 35%，NAND 略高（原話："the SCA agreements do cover both DRAM and NAND"）
- 2026-09-30｜Manish Bhatia｜customer：COO 說明 SCA 營收約四分之三有明定價格框架，約四分之一隨市場協商（原話："about 3/4 of the SCA have this"）
- 2026-09-30｜Manish Bhatia｜customer：COO 稱新簽 SCA 的談判反映當前市況與漲價方向，不同於先前以 CQ2 市況定價者（原話："the direction of travel has been for higher pricing"）
- 2026-09-30｜Manish Bhatia｜customer：COO 回應手機與 PC：位元出貨連續下滑但營收因價格與組合成長（原話："We did see sequential bit decline in our mobile and client"）
- 2026-09-30｜Manish Bhatia｜customer：COO 稱客戶正在以現有記憶體供給最大化運算晶片出貨，形成潛在需求（原話："customers are choosing to maximize the compute silicon"）
- 2026-09-30｜Manish Bhatia｜customer：COO 說明代理式 AI 帶動 CPU 需求與伺服器單位數成長，並稱 DRAM 是主要限制（原話："server units are growing so strongly"）
- 2026-09-30｜Mark Murphy｜capital_allocation：COO 與 CFO 說明 FY27 資本支出增加主要為廠房建設，多數為 2028 後才投產的無塵室（原話："the majority of the increase is for construction CapEx"）
- 2026-09-30｜Mark Murphy｜capital_allocation：CFO 稱建廠支出不等於位元產出，設備依市場需求與 SCA 配置（原話："SCAs are a good way for us to keep a pulse on the market"）
- 2026-09-30｜Manish Bhatia｜risk：COO 提到新增無塵室從啟用到有意義出貨仍需數季（原話："it takes a few quarters for meaningful shipments to come"）
- 2026-09-30｜Manish Bhatia｜risk：COO 說明 FY26 美光 NAND 供給成長低於業界，因 Singapore 無塵室被研發線與 HBM 試產占用（原話："our supply growth grew less than the industry this year"）
- 2026-09-30｜Manish Bhatia｜commitment：COO 表示不更新 HBM TAM 展望（原話："We are not updating that TAM outlook right now."）
- 2026-09-30｜Manish Bhatia｜commitment：COO 承諾依需求趨勢才為無塵室裝機擴產（原話："we will equip the clean rooms and build capacity to the"）
- 2026-09-30｜Manish Bhatia｜commitment：COO 稱 SCA 占比未來可能提高，持續談判中（原話："this number could get up to be higher in the future"）

### 問答異常語氣（迴避／改口／保留）
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Reitzes 問 2028 為何比 2027 更緊、對毛利意味什麼（認為看不出 2028 毛利會不同於 2027）｜答法：COO 與 CFO 談需求與供給結構與漲價放緩、組合與起動成本，未給 2028 毛利數字或與 2027 的差異
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Weathers 問 HBM TAM 更新數字及位元與價格拆分｜答法：明說不更新 TAM，未拆位元與價格，改談 HBM 成長快於傳統 DRAM
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Weathers 問 HBM 市占目標是否仍為低 20% 區間｜答法：未確認舊目標，改稱約等於整體 DRAM 市占、不鎖定單一數字
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Malik 問 SCA 占 2030 年銷售 35% 中 DRAM 與 NAND 的拆分｜答法：拒絕拆分，只給 DRAM 略低於約 35%、NAND 略高的方向，事後再要求澄清該回答
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Schneider 問 SCA 價格上下限是否整體重設及是否含超大規模客戶｜答法：稱有多種框架、不點名客戶，未直接回答上下限是否整體重設或超大規模客戶是否納入
- MU_Q4_2026_Earnings_Call_20260930.md｜問：Hosseini 問 FY27–28 NAND 位元出貨能否與業界約 25% 持平｜答法：稱不評論那麼遠，只談業界成長與產能因素，未給自家數字

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
{"date":"20260705","verdict":"觀望","role":"條件式衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"本輪記憶體上行因「結構性 AI 需求 + 供給紀律」延長，循環不像過去 ~2 年見頂崩落（最關鍵也最脆弱，依賴循環定價非永續複利）","columns":{"2Y 驗證點":"2026-2027 DRAM/HBM 合約價維持正成長、毛利率守 60%+","5Y 驗證點":"through-cycle normalized 毛利率台階較上輪（~30%）抬升至 40%+","10Y 驗證點":"記憶體不再是純商品，AI 使需求基底結構性黏著","數字門檻":"HBM 2028 達 $100B、CAGR ~40%；2026 產能售罄；AI 吃掉 ~70% 記憶體增量","來源":"Micron 法說、TrendForce、SK 集團主席","漂移觸發":"連 2 季 DRAM 合約價 TTM 偏離 ≥5% 向下 → 削弱"}},{"id":"H2","text":"Micron 在 HBM4／HBM4E 守住 ~20% 份額並改善獲利結構，不被 SK Hynix / Samsung 邊緣化","columns":{"2Y 驗證點":"HBM4 份額 ≥18%、取得 NVIDIA Rubin 平台合格量產（已達成）","5Y 驗證點":"HBM4E（2027 ~40% 市場）份額不低於 HBM4","10Y 驗證點":"在 custom HBM / 先進封裝整合維持三強之一","數字門檻":"HBM4 份額 ~20%（mid-range）；HBM4 11Gbps 送樣、Rubin 合格","來源":"Astute Group、TrendForce 2026/02","漂移觸發":"連 2 季 HBM 份額 TTM 下滑 ≥3pp → 削弱"}},{"id":"H3","text":"估值不在峰值 EPS 上被進一步 re-rate；當前股價已大致反映（甚至超額反映）多頭預期（市場假設）","columns":{"2Y 驗證點":"股價不顯著超越分析師均值目標 ~$1,486、且不再獲得更高倍數","5Y 驗證點":"循環下行時倍數不系統性下移（如 2022-2023 那樣）","10Y 驗證點":"市場願給記憶體龍頭結構性更高倍數","數字門檻":"均值目標 $1,486（42 位，strong_buy）；現價 $976 已在其下 35%，但 P/B 15.2x 峰值","來源":"yfinance targetMeanPrice / TipRanks 共識","漂移觸發":"股價回 $1,255 ATH 上方（再獲更高倍數）→ H3 削弱、R:R 惡化"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"記憶體循環反轉——合約價 QoQ 轉跌、毛利率自峰值回落","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"TrendForce DRAM/HBM 月度合約價","警戒閾值":"連 2 季持平或轉負 → 循環軌了結 / 放棄進場"}},{"id":"R2","text":"HBM 競爭——Samsung HBM4 強勢回歸 + SK Hynix 領先，Micron 份額／獲利結構被壓","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 HBM 份額、HBM4 大客戶合格進度","警戒閾值":"份額連 4 季 TTM 下滑 ≥3pp → moat_trend 降 ↓"}},{"id":"R3","text":"資本密集吞噬報酬——擴產 capex（FY26 &gt;$25B）長期壓低 through-cycle FCF / ROIC；中國供給替代（CXMT/YMTC）加劇","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"capex/營收、through-cycle FCF margin、ROIC−WACC、中國成熟節點份額","警戒閾值":"下一輪低谷 FCF 再度轉負 + ROIC &lt; WACC → 重估產業質地"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd FY26 P/E ≤13x（≈$946）或合約價 QoQ 轉負後 P/B 回落自身中位（循環重置）；HBM4 份額連 2 季淨增則升級評估","irr_base_pct":0.6,"ev5y_pct":6.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式衛星持倉","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.4,"ev5y_pct":6.8,"irr_base_pct":0.6,"max_dd_pct":-70.0,"bull_5y_price":1700.0,"bear_5y_price":470.0,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd FY26 P/E ≤13x（≈$946）或合約價 QoQ 轉負後 P/B 回落自身中位（循環重置）；HBM4 份額連 2 季淨增則升級評估","price_at_dd":975.56,"archetype":"循環/商品","cycle_position":"晚循環"}}
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

此回覆內容之後由程式存為 `/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/MU_20261020/judgment.json`（你不用、也不能動筆存檔，只需回覆內容本身）。
