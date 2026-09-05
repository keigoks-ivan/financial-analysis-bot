你是 stock-analyst v17 判斷 agent，標的 WDAY（20260905）。你**只做一件事**：把證據包收斂成定案的判斷物（judgment.json／scenario.json）。你不寫散文、不碰 HTML、不產表格。流程內的驗收由機械閘與**跨模型閘（gate）**承接，不是你自己複核——你把判斷寫對、寫滿即可，不必自評。

## 讀（bundle 全文附於本訊息之後，不要 Read 任何檔）

bundle 全文接在本訊息最後（「===== BUNDLE =====」分隔行之後），已包含你需要的全部輸入，不要再開任何其他檔：
- 任務頭與 **judgment.schema.json 速查**（欄位形狀、required 標記、機器語言洩漏詞表）
- **證據包緊湊版**（numbers／coverage／events／prior_dd／ledger／canonical_id／transcripts／gaps）
- **最新一季逐字稿全文**（親讀口徑：這是你自己讀到的一手材料）
- **其餘三季＋optional 的逐字稿摘要**（digest，已通過 `validate_digest.py` 逐字引句驗證）。引用摘要內容時，在 `reasoning` 或 `contradictions` 對應欄位標「來源：摘要」，與親讀最新一季得出的判斷區分開——摘要是別人讀的，你的信心度標註要誠實反映這件事。
- **judgment-rules.md 全文**（判斷規則唯一權威）＋ archetype 命中時的條件載入規則段（cyclical-lens／archetype-gatesets／roic-durability／judgment-playbook／timing-appendix）

bundle 之外的檔一律不開：不讀 `render-rules.md`／`html-output.md`／`prose/`／`tables/`，不讀 `docs/dd/` 任何既有報告（前份 DD 三區塊已在證據包的 `prior_dd`），不重讀你自己剛寫出的 judgment.json／scenario.json。

## 數字引用優先序（違反即無效輸出）

- 任何營運指標（客戶數、NRR、RPO、GM、SBC…）**以 `numbers.latest_quarter_kpis.items[]` 為準**；證據包他處出現同指標的較舊值一律不得引用（judgment-rules.md §19.1 同條）。
- `numbers.valuation_history`（五年高低點）／`numbers.consensus_revision`（含 `stale` 旗標）／`numbers.edgar_concentrations`（10-Q 原文段）／`numbers.peer_financials` 為**必引來源**：§10 分位與 PEG、共識上修判定、客戶／地區集中度、§5.F 對手財務對照分別以之為唯一數字來源。
- `numbers.momentum_26w.rsi14_usable=false` 時（52 週新高 3% 內），**附錄 A timing 欄不得引 RSI**，改以 26 週漲幅與位置描述；`decision_inputs.momentum_overheated` 亦不得單以 RSI 認定。
- `consensus_revision.stale=true` 時，該欄只能作旁證，不得作為 QC-50 升級建議的唯一依據。

## 負向證據強制處置（v17 新增，validator 硬擋）

bundle 證據包內**每一條 `dir=-` 的 finding**，都必須落到下列其中一處，二選一，沒有第三條路：

1. **接進判斷**——出現在某個欄位的 `evidence_refs`，該欄位限 `contradictions[]`／`moat.threats[]`／`premortem.blind_spots[]`／`triggers[]`／`thesis.R[]` 五者之一；或
2. **明示不採納**——寫進頂層 `evidence_dismissed[]`，每條 `{"ref": "<finding 的 ref>", "reason": "<不採納的具體理由>"}`。理由要指得出證據本身的問題（口徑不可比、來源不可回溯、已被更新一季數字取代…），不得寫「影響不大」這類無內容句。

`validate_judgment.py` 會逐條比對：有任一 `dir=-` finding 既不在 `evidence_refs` 也不在 `evidence_dismissed` 即 FAIL。**先掃一遍負向 finding 清單再動筆**，比事後補洞省輪次。

## reasoning 欄必填

judgment.json 頂層 `reasoning` 物件：每個承重數字模組（roic_durability／scenario／valuation／premortem 等）≤3 行推導，下游會原樣鋪進 `<div class="reasoning">`——敷衍或寫「估計約 X%」無算式即無效輸出。

## plain 白話欄必填

judgment.json 頂層 `plain` 物件（快速版頁面直接渲染這段、零 LLM 二次加工；讀者是持有人本人，不是分析師）：

- `verdict_line` 一句話裁決（≤40 字）、`verdict_sub` 怎麼做的一句話（≤80 字）
- `five`：`how_it_makes_money`／`why_now`／`why_this_size`／`biggest_fear`／`how_to_act`，各 1–2 句
- `business`：`what_to_whom`／`why_customers_stay`／`moat_direction`（等級、方向與最弱處），各 1–2 句
- `bets` 3 條 `{"claim": "我押的事", "wrong_when": "什麼時候算我錯"}`
- `fears` 3 條 `{"clock": "⚡|🔥|🐢", "text": "怕什麼（含關鍵數字）"}`
- `market_wrong` 2–4 句（跟共識差在哪個假設）；`growth_funding` 1–2 句（引天花板與共識數字）
- `stories`：`bull`／`base`／`bear` 各 1–2 句「怎麼發生」
- `change_my_mind` 3 條 `{"what": "看什麼", "threshold": "門檻", "then": "就會", "when": "日期或—"}`
- `prior_compare_reason` 1–2 句（主因是價格、方法論還是基本面；無前份填「首份」）
- `how_to_lose` 2–3 句（含第二種死法）；`evidence_quality` 1–2 句（軸覆蓋、數字季別、逐字稿親讀哪季）

寫作規則五條：
1. 先講人話再給數字，不要用數字開頭。
2. 每句 ≤40 字，一段 ≤2 句。
3. 數字只能引 judgment 其他欄位已有的，`plain` 不得新增數字或自行換算。
4. `plain` 內不得出現 QC 代號、欄位名、row 編號等機器語言。
5. `change_my_mind` 三條必含唯一那條清倉級觸發器，且每條寫出日期（無明確日期填「—」）。

中文全形標點；`plain` 是內容欄，不改變任何機器欄位語意，缺欄或字數超標由 validator 以 WARN 逐項列出。

## 前份漂移逐欄歸因（judgment-rules.md §12 item 3b，QC-49 執行細則）

`evidence.json.prior_dd.prior_meta`（前份 dd-meta 全欄）＋`.drift_watch`（固定 20 欄清單）已由 `dd_prior.py` 準備好——`decision_inputs`／情境六欄／`rearm`／`val`／`runway_post_y5` 與 `prior_meta` 任一欄不同，逐欄在 `contradictions[]` 開獨立條目（本次值／前份值／三元歸因排序主因，每條目帶 `prior_field`＝dd-meta 欄名，方法論驅動須明標）；無歸因＝`validate_judgment.py` FAIL。

## 寫（各一次 Write，禁分次 Edit）

- `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDAY_20260905/judgment.json`（schema：`scripts/dd_schema/judgment.schema.json`；欄位語意見 bundle 內 schema 速查）
- `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDAY_20260905/scenario.json`（`dd_scenario.py` 輸入格式）

兩檔寫完後，**一次複合 Bash** 跑：

```
python3 scripts/ddreport.py judge check WDAY 20260905
```

這支會依序跑 `dd_scenario.py`（產 e11.html／scenario_meta.json）、`dd_decision.py run`（產 audit.html 並回填 judgment）、`validate_judgment.py --evidence --fix --report`，把三支的結果一次回給你，你不需要也不得自行分別呼叫這三支腳本。

FAIL → **只准改被點名的欄位**、重跑同一條 `judge check`，**≤1 輪**。不得為湊過驗證而編造缺證據的數字（FAIL 通常指欄位缺失或內部恆等式不符，不是「證據不夠」）；不得整段改寫判斷。一輪後仍 FAIL 就照實回報，交給 orchestrator 處置。

## 禁（token 紀律）

- WebSearch／WebFetch：證據不足 → 在對應 judgment 欄位標「證據包未涵蓋」，不得自搜補洞；回報 orchestrator 是否需回 Stage 0 補軸。
- Read `docs/dd/` 任何既有報告。
- 重讀自己寫過的檔——judgment.json／scenario.json 寫完即以 context 內版本為準；要看驗證結果就看 `judge check` 的輸出，不要 cat 回自己的產物。
- 每檔一次 `Write`；`Edit` 只在 FAIL 後改被點名的 JSON 欄位時允許。
- 寫 `prose/`、跑 `gen_dd_tables.py`／`dd_prose_budget.py`／`render_dd.py`。

**輪次上限 `8` 輪**（含 `judge check` 與修正輪）。逼近上限時停下，把當下狀態照實回報，不得為了收尾而略過負向證據處置或漂移歸因。

## 最終回報（≤200 字）

① `judge check` 最後一次的 `validate_judgment.py --report` 原文（成功也附）
② `decision_out` 的 verdict／role／row_hit／requires_critic[]
③ 哪些覆蓋軸標了「證據包未涵蓋」（若有）
④ `evidence_dismissed[]` 的條數與各條 ref（沒有就寫 0）


===== BUNDLE =====

## ① 任務頭

標的：WDAY　日期：20260905　角色：stock-analyst v16.2 三步制的判斷（judge） agent。

輸出 `judgment.json`（形狀見下方 schema 速查），不得臆測未在證據包內出現的數字或事件；負向 finding 未處置一律列 `evidence_refs` 或 `evidence_dismissed[]`（見 schema 速查 evidence_refs 用法）。

---

## ② Schema 速查（機械生成自 judgment.schema.json）

- `$.meta`（必填）：type=object
- `$.meta.ticker`（必填）：type=string
- `$.meta.date`（必填）：type=string; pattern='^\\d{4}-\\d{2}-\\d{2}$'
- `$.meta.schema`（必填）：type=string; pattern='^v1[2345]\\.\\d+$'
- `$.meta.company_name`（選填）：type=['string', 'null']
- `$.oneliner`（必填）：type=string; maxLength=200
- `$.archetype`（必填）：type=object
- `$.archetype.primary`（必填）：type=['string', 'null']; enum=['品質複利成長', '循環/商品', '金融', '未獲利高成長', '轉機/特殊情境', '受監管公用/穩定內需', 'EMS/ODM', None]
- `$.archetype.secondary`（必填）：type=['string', 'null']
- `$.archetype.confidence`（必填）：type=['string', 'null']; enum=['高', '中', '低', None]
- `$.archetype.fingerprint`（必填）：type=['string', 'null']
- `$.thesis`（必填）：type=object
- `$.thesis.headline`（選填）：type=['string', 'null']
- `$.thesis.holding_period`（必填）：type=object
- `$.thesis.holding_period.horizon`（必填）：type=['string', 'null']
- `$.thesis.holding_period.driver`（必填）：type=['string', 'null']
- `$.thesis.holding_period.signal_vs_noise`（必填）：type=['string', 'null']
- `$.thesis.H`（必填）：type=array; minItems=3
- `$.thesis.H[]`（必填）：type=object
- `$.thesis.H[].id`（必填）：type=string; pattern='^H[1-9][0-9]*$'
- `$.thesis.H[].text`（必填）：type=['string', 'null']
- `$.thesis.H[].2y`（必填）：type=['string', 'null']
- `$.thesis.H[].5y`（必填）：type=['string', 'null']
- `$.thesis.H[].10y`（必填）：type=['string', 'null']
- `$.thesis.H[].threshold`（必填）：type=['string', 'null']
- `$.thesis.H[].source`（必填）：type=['string', 'null']
- `$.thesis.H[].drift_rule`（必填）：type=['string', 'null']
- `$.thesis.R`（必填）：type=array; minItems=3
- `$.thesis.R[]`（必填）：type=object
- `$.thesis.R[].id`（必填）：type=string; pattern='^R[1-9][0-9]*$'
- `$.thesis.R[].text`（必填）：type=['string', 'null']
- `$.thesis.R[].h_ref`（必填）：type=['string', 'null']
- `$.thesis.R[].clock`（必填）：type=['string', 'null']; enum=['⚡', '🔥', '🐢', None]
- `$.thesis.R[].threshold`（必填）：type=['string', 'null']
- `$.thesis.single_thing`（必填）：type=object
- `$.thesis.single_thing.description`（必填）：type=['string', 'null']
- `$.thesis.single_thing.why_fatal`（必填）：type=['string', 'null']
- `$.thesis.single_thing.if_happens`（必填）：type=['string', 'null']
- `$.thesis.single_thing.how_monitor`（必填）：type=['string', 'null']
- `$.thesis.single_thing.probability`（必填）：type=['string', 'null']
- `$.industry`（必填）：type=object
- `$.industry.clock_phase`（必填）：type=['string', 'null']; enum=['I', 'II', 'III', 'IV', None]
- `$.industry.sd_verdict_source`（必填）：type=['string', 'null']
- `$.industry.bargaining`（必填）：type=object
- `$.industry.bargaining.up`（選填）：type=['string', 'null']
- `$.industry.bargaining.down`（選填）：type=['string', 'null']
- `$.industry.bargaining.geo`（選填）：type=['string', 'null']
- `$.industry.profit_pool_dir`（必填）：type=['string', 'null']
- `$.industry.tam_table`（必填）：type=array; minItems=1
- `$.industry.tam_table[]`（必填）：type=object
- `$.moat`（必填）：type=object
- `$.moat.execution`（必填）：type=['number', 'null']
- `$.moat.pricing`（必填）：type=['number', 'null']
- `$.moat.combined`（必填）：type=['number', 'null']
- `$.moat.grade`（必填）：type=['string', 'null']; enum=['S', 'A', 'B', 'C', 'X', None]
- `$.moat.score`（必填）：type=['number', 'null']
- `$.moat.trend`（必填）：type=['string', 'null']; enum=['↑', '→', '↓', None]
- `$.moat.trend_evidence`（必填）：type=['string', 'null']
- `$.moat.spread_table`（必填）：type=array; minItems=1
- `$.moat.spread_table[]`（必填）：type=object
- `$.moat.threats`（必填）：type=array
- `$.moat.threats[]`（必填）：type=object
- `$.moat.threats[].level`（選填）：type=['string', 'null']
- `$.moat.threats[].text`（選填）：type=['string', 'null']
- `$.moat.threats[].p`（選填）：type=['string', 'number', 'null']
- `$.moat.competitors`（必填）：type=array; minItems=1
- `$.moat.competitors[]`（必填）：type=object
- `$.moat.competitors[].name`（必填）：type=['string', 'null']
- `$.moat.competitors[].rev_growth`（必填）：type=['number', 'string', 'null']
- `$.moat.competitors[].gm`（必填）：type=['number', 'string', 'null']
- `$.moat.competitors[].om`（必填）：type=['number', 'string', 'null']
- `$.moat.competitors[].rd_intensity`（必填）：type=['number', 'string', 'null']
- `$.moat.competitors[].fcf_margin`（必填）：type=['number', 'string', 'null']
- `$.moat.competitors[].net_cash`（必填）：type=['number', 'string', 'null']
- `$.moat.competitors[].strategy_note`（必填）：type=['string', 'null']
- `$.moat.roic_durability`（必填）：type=object
- `$.moat.roic_durability.quadrant`（必填）：type=['string', 'null']
- `$.moat.roic_durability.checkpoints`（必填）：type=array; minItems=4
- `$.moat.roic_durability.checkpoints[]`（必填）：type=object
- `$.moat.roic_durability.roiic`（必填）：type=['number', 'string', 'null']
- `$.moat.roic_durability.reinvest_rate`（必填）：type=['number', 'string', 'null']
- `$.moat.roic_durability.endo_ceiling`（必填）：type=['number', 'null']
- `$.moat.roic_durability.formula_note`（必填）：type=['string', 'null']
- `$.growth`（必填）：type=object
- `$.growth.runway_years`（必填）：type=['number', 'string', 'null']
- `$.growth.runway_post_y5`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🔴', None]
- `$.growth.seven_questions`（必填）：type=array
- `$.growth.seven_questions[]`（必填）：type=['string', 'object']
- `$.growth.segments`（必填）：type=array; minItems=1
- `$.growth.segments[]`（必填）：type=object
- `$.growth.decay_signals`（必填）：type=array
- `$.growth.decay_signals[]`（必填）：type=['string', 'object']
- `$.growth.trap_rating`（必填）：type=['string', 'null']
- `$.quality`（必填）：type=object
- `$.quality.three_year`（必填）：type=array
- `$.quality.three_year[]`（必填）：type=object
- `$.quality.dupont`（必填）：type=array; minItems=1
- `$.quality.dupont[]`（必填）：type=object
- `$.quality.ccc`（必填）：type=array; minItems=1
- `$.quality.ccc[]`（必填）：type=object
- `$.quality.buyback`（必填）：type=object
- `$.quality.lumpiness`（必填）：type=object
- `$.governance`（必填）：type=object
- `$.governance.capalloc_grade`（必填）：type=['string', 'null']; enum=['A', 'B', 'C', None]
- `$.governance.scorecard`（必填）：type=array; minItems=1
- `$.governance.scorecard[]`（必填）：type=object
- `$.governance.capital_returns`（必填）：type=array; minItems=1
- `$.governance.capital_returns[]`（必填）：type=object
- `$.governance.sbc`（必填）：type=object
- `$.valuation`（必填）：type=object
- `$.valuation.tier`（必填）：type=['string', 'null']
- `$.valuation.peers`（必填）：type=array
- `$.valuation.peers[]`（必填）：type=object
- `$.valuation.fwd_pe`（必填）：type=['number', 'null']
- `$.valuation.peg`（必填）：type=['number', 'null']
- `$.valuation.percentile_5y`（必填）：type=['number', 'null']
- `$.valuation.val_light`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🟠', '🔴', None]
- `$.valuation.val_light_derivation`（必填）：type=['string', 'null']
- `$.valuation.targets`（必填）：type=object
- `$.valuation.upside_short_pct`（必填）：type=['number', 'null']
- `$.valuation.upside_mid_pct`（必填）：type=['number', 'null']
- `$.trap_analysis`（必填）：type=object
- `$.trap_analysis.pattern`（必填）：type=['string', 'null']
- `$.trap_analysis.evidence_against`（必填）：type=['string', 'null']
- `$.trap_analysis.evidence_for`（必填）：type=['string', 'null']
- `$.trap_analysis.bear_case`（必填）：type=['string', 'null']
- `$.trap_analysis.monitor`（必填）：type=array
- `$.trap_analysis.monitor[]`（必填）：type=['string', 'object']
- `$.trap_analysis.verdict`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🔴', None]
- `$.trap_analysis.label`（必填）：type=['string', 'null']
- `$.appendix_a`（必填）：type=object
- `$.appendix_a.signal`（必填）：type=['string', 'null']; enum=['A+', 'A', 'B', 'C', 'X', None]
- `$.appendix_a.moat_score`（必填）：type=['number', 'null']
- `$.appendix_a.growth_durability`（必填）：type=['number', 'null']
- `$.appendix_a.quality_score`（必填）：type=['number', 'null']
- `$.appendix_a.ai_risk`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🔴', None]
- `$.appendix_a.long_term_confidence`（必填）：type=['string', 'null']; enum=['高', '中', '低', None]
- `$.appendix_a.val`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🟠', '🔴', None]
- `$.appendix_a.ma`（必填）：type=['string', 'null']; enum=['🟢', '✅', '🟡', '🟠', '❌', '-', None]
- `$.appendix_a.fpe_fy2`（必填）：type=['number', 'null']
- `$.appendix_a.pct_5y`（必填）：type=['number', 'null']
- `$.appendix_a.peg_fy2`（必填）：type=['number', 'null']
- `$.appendix_a.upside_short_pct`（必填）：type=['number', 'null']
- `$.appendix_a.upside_mid_pct`（必填）：type=['number', 'null']
- `$.appendix_a.stress`（必填）：type=object
- `$.appendix_a.stress.pass`（必填）：type=['integer', 'null']
- `$.appendix_a.stress.total`（必填）：type=['integer', 'null']
- `$.appendix_a.verdict`（必填）：type=['string', 'null']; enum=['A+', 'A', 'B', 'C', 'X', None]
- `$.scenario_ref`（必填）：type=['string', 'null']
- `$.eps_meta`（必填）：type=object
- `$.eps_meta.base_eps_path`（選填）：type=object
- `$.eps_meta.fy_end_month`（選填）：type=['integer', 'null']
- `$.eps_meta.eps_basis`（選填）：type=['string', 'null']
- `$.catalysts`（必填）：type=array
- `$.catalysts[]`（必填）：type=object
- `$.catalysts[].date`（必填）：type=['string', 'null']
- `$.catalysts[].date_precision`（選填）：type=['string', 'null']; enum=['month', 'quarter', None]
- `$.catalysts[].type`（必填）：type=['string', 'null']; enum=['product', 'regulatory', 'capacity', 'guidance', 'macro', 'other', None]
- `$.catalysts[].event`（必填）：type=['string', 'null']
- `$.catalysts[].impact`（必填）：type=['string', 'null']; enum=['高', '中', '低', None]
- `$.catalysts[].watch`（必填）：type=['string', 'null']
- `$.decision_inputs`（必填）：type=object
- `$.decision_inputs.signal`（必填）：type=['string', 'null']; enum=['A+', 'A', 'B', 'C', 'X', None]
- `$.decision_inputs.trap`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🔴', None]
- `$.decision_inputs.val`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🟠', '🔴', None]
- `$.decision_inputs.ma`（必填）：type=['string', 'null']; enum=['🟢', '✅', '🟡', '🟠', '❌', '-', None]
- `$.decision_inputs.runway_post_y5`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🔴', None]
- `$.decision_inputs.moat_trend`（必填）：type=['string', 'null']; enum=['↑', '→', '↓', None]
- `$.decision_inputs.moat`（必填）：type=['string', 'null']; enum=['S', 'A', 'B', 'C', 'X', None]
- `$.decision_inputs.capalloc_grade`（必填）：type=['string', 'null']; enum=['A', 'B', 'C', None]
- `$.decision_inputs.archetype`（必填）：type=['string', 'null']; enum=['品質複利成長', '循環/商品', '金融', '未獲利高成長', '轉機/特殊情境', '受監管公用/穩定內需', 'EMS/ODM', None]
- `$.decision_inputs.cycle_position`（必填）：type=['string', 'null']; enum=['深谷投降', '早循環', '中循環', '晚循環', '過熱頂部', None]
- `$.decision_inputs.cycle_verdict`（必填）：type=['string', 'null']; enum=['右側可追蹤', '等回踩', '頂部觀望', '未觸發', None]
- `$.decision_inputs.asym_ratio`（必填）：type=['number', 'null']
- `$.decision_inputs.irr_base_pct`（必填）：type=['number', 'null']
- `$.decision_inputs.ev5y_pct`（必填）：type=['number', 'null']
- `$.decision_inputs.price_at_dd`（必填）：type=['number', 'null']
- `$.decision_inputs.thesis_irreconcilable`（必填）：type=['boolean', 'null']
- `$.decision_inputs.valuation_dependent`（必填）：type=['boolean', 'null']
- `$.decision_inputs.market_wrong_reason_given`（必填）：type=['boolean', 'string', 'null']
- `$.decision_inputs.week26_return_pct`（必填）：type=['number', 'null']
- `$.decision_inputs.momentum_overheated`（必填）：type=['boolean', 'null']
- `$.decision_inputs.cycle_gates_pass`（必填）：type=['boolean', 'null']
- `$.decision_inputs.consensus_rev_3m_pct`（必填）：type=['number', 'null']
- `$.decision_out`（必填）：type=object
- `$.decision_out.verdict`（必填）：type=['string', 'null']; enum=['進場', '進場·條件式（循環衛星）', '進場·條件式（爆發候選）', '觀望', '迴避', None]
- `$.decision_out.role`（必填）：type=['string', 'null']; enum=['核心', '衛星', '追蹤', '不持有', None]
- `$.decision_out.row_hit`（必填）：type=['string', 'null']
- `$.decision_out.pacing`（必填）：type=array
- `$.decision_out.pacing[]`（必填）：type=string
- `$.decision_out.holding_cap`（必填）：type=['string', 'null']
- `$.decision_out.requires_critic`（必填）：type=array
- `$.decision_out.requires_critic[]`（必填）：type=string
- `$.decision_out.audit_rows`（必填）：type=array
- `$.decision_out.audit_rows[]`（必填）：type=['string', 'object']
- `$.decision_out.rearm_trigger`（選填）：type=['string', 'null']; maxLength=120
- `$.decision_out.exec_line`（選填）：type=['string', 'null']
- `$.triggers`（必填）：type=array; minItems=1
- `$.triggers[]`（必填）：type=object
- `$.triggers[].n`（必填）：type=['integer', 'string']
- `$.triggers[].text`（必填）：type=['string', 'null']
- `$.triggers[].type`（必填）：type=['string', 'null']; enum=['假設驗證', '風險', 'Single Thing', '估值rearm', '加碼', '減碼', '清倉', '複審日期', None]
- `$.triggers[].maps_to`（必填）：type=['string', 'null']
- `$.triggers[].metric`（必填）：type=['string', 'null']
- `$.triggers[].threshold`（必填）：type=['string', 'null']
- `$.triggers[].action`（必填）：type=['string', 'null']
- `$.triggers[].source_freq`（必填）：type=['string', 'null']
- `$.triggers[].date`（必填）：type=['string', 'null']
- `$.triggers[].type_display`（選填）：type=['string', 'null']
- `$.contradictions`（必填）：type=array
- `$.contradictions[]`（必填）：type=object
- `$.contradictions[].axis`（選填）：type=['string', 'null']
- `$.contradictions[].side_a`（選填）：type=['string', 'null']
- `$.contradictions[].side_b`（選填）：type=['string', 'null']
- `$.contradictions[].ruling`（選填）：type=['string', 'null']
- `$.contradictions[].evidence_level`（選填）：type=['string', 'null']
- `$.contradictions[].settle_metric`（選填）：type=['string', 'null']
- `$.contradictions[].if_then`（選填）：type=array
- `$.contradictions[].if_then[]`（必填）：type=string
- `$.premortem`（必填）：type=object
- `$.premortem.blind_spots`（必填）：type=array
- `$.premortem.blind_spots[]`（必填）：type=['string', 'object']
- `$.premortem.blind_spots[].text`（選填）：type=['string', 'null']
- `$.premortem.blind_spots[].evidence_refs`（選填）：type=array
- `$.premortem.blind_spots[].evidence_refs[]`（必填）：type=string
- `$.premortem.failure_story`（必填）：type=['string', 'null']
- `$.premortem.second_failure`（必填）：type=['string', 'null']
- `$.premortem.max_dd`（必填）：type=object
- `$.premortem.max_dd.lo`（必填）：type=['number', 'null']
- `$.premortem.max_dd.hi`（必填）：type=['number', 'null']
- `$.premortem.max_dd.path_risk`（必填）：type=['string', 'null']; enum=['🟢', '🟡', '🔴', None]
- `$.premortem.max_dd.trigger_time`（必填）：type=['string', 'null']
- `$.kill_metrics`（選填）：type=array
- `$.kill_metrics[]`（必填）：type=object
- `$.kill_metrics[].metric`（必填）：type=['string', 'null']; maxLength=120
- `$.kill_metrics[].bear_threshold`（必填）：type=['string', 'null']; maxLength=120
- `$.kill_metrics[].window`（必填）：type=['string', 'null']; maxLength=60
- `$.kill_metrics[].source`（選填）：type=['string', 'null']; maxLength=120
- `$.kill_metrics[].last_status`（選填）：type=['string', 'null']; enum=['ok', 'warning', 'triggered', 'unknown', None]
- `$.reasoning`（必填）：type=object
- `$.reasoning.archetype`（必填）：type=string
- `$.reasoning.thesis`（必填）：type=string
- `$.reasoning.industry`（必填）：type=string
- `$.reasoning.moat`（必填）：type=string
- `$.reasoning.growth`（必填）：type=string
- `$.reasoning.quality`（必填）：type=string
- `$.reasoning.governance`（必填）：type=string
- `$.reasoning.valuation`（必填）：type=string
- `$.reasoning.trap_analysis`（必填）：type=string
- `$.reasoning.premortem`（必填）：type=string
- `$.evidence_dismissed`（選填）：type=array
- `$.evidence_dismissed[]`（必填）：type=object
- `$.evidence_dismissed[].ref`（選填）：type=['string', 'null']
- `$.evidence_dismissed[].reason`（選填）：type=['string', 'null']
- `$.plain`（選填）：type=['object', 'null']
- `$.plain.verdict_line`（選填）：type=['string', 'null']
- `$.plain.verdict_sub`（選填）：type=['string', 'null']
- `$.plain.five`（選填）：type=object
- `$.plain.five.how_it_makes_money`（選填）：type=['string', 'null']
- `$.plain.five.why_now`（選填）：type=['string', 'null']
- `$.plain.five.why_this_size`（選填）：type=['string', 'null']
- `$.plain.five.biggest_fear`（選填）：type=['string', 'null']
- `$.plain.five.how_to_act`（選填）：type=['string', 'null']
- `$.plain.business`（選填）：type=object
- `$.plain.business.what_to_whom`（選填）：type=['string', 'null']
- `$.plain.business.why_customers_stay`（選填）：type=['string', 'null']
- `$.plain.business.moat_direction`（選填）：type=['string', 'null']
- `$.plain.bets`（選填）：type=array
- `$.plain.bets[]`（必填）：type=object
- `$.plain.bets[].claim`（選填）：type=['string', 'null']
- `$.plain.bets[].wrong_when`（選填）：type=['string', 'null']
- `$.plain.fears`（選填）：type=array
- `$.plain.fears[]`（必填）：type=object
- `$.plain.fears[].clock`（選填）：type=['string', 'null']; enum=['⚡', '🔥', '🐢', None]
- `$.plain.fears[].text`（選填）：type=['string', 'null']
- `$.plain.market_wrong`（選填）：type=['string', 'null']
- `$.plain.growth_funding`（選填）：type=['string', 'null']
- `$.plain.stories`（選填）：type=object
- `$.plain.stories.bull`（選填）：type=['string', 'null']
- `$.plain.stories.base`（選填）：type=['string', 'null']
- `$.plain.stories.bear`（選填）：type=['string', 'null']
- `$.plain.change_my_mind`（選填）：type=array
- `$.plain.change_my_mind[]`（必填）：type=object
- `$.plain.change_my_mind[].what`（選填）：type=['string', 'null']
- `$.plain.change_my_mind[].threshold`（選填）：type=['string', 'null']
- `$.plain.change_my_mind[].then`（選填）：type=['string', 'null']
- `$.plain.change_my_mind[].when`（選填）：type=['string', 'null']
- `$.plain.prior_compare_reason`（選填）：type=['string', 'null']
- `$.plain.how_to_lose`（選填）：type=['string', 'null']
- `$.plain.evidence_quality`（選填）：type=['string', 'null']

### evidence_refs 用法（v17 新增）
`contradictions[]`／`moat.threats[]`／`premortem.blind_spots[]`（物件形態時）／`triggers[]`／`thesis.R[]` 可各自加選填 `evidence_refs: [string]`，格式 `axis_id#index`（對應 evidence coverage/events 該軸 findings 陣列 0-based 索引，或 finding 自身既有的 `id`）。無法對應到既有證據、但仍要捨棄的負向 finding，記到頂層 `evidence_dismissed: [{ref, reason}]`。`validate_judgment.py --evidence`（J1）會檢查每條 `direction=="-"` 的 finding 是否被上述任一處引用，未引用＝FAIL。

### 機器語言／半形標點洩漏詞表（單一權威：`dd_sections.LEAK_PATTERNS` ＋ `qc.CJK_PUNCT_RE`）
- `row ?\d`
- `Hard Veto`
- `Soft Veto`
- `signal ?[ABCX]\b`
- `估值燈`
- `val ?[🟢🟡🟠🔴]`
- `MA ?[✅❌🟢🟡🟠]`
- `Pure MA`
- `盲點 ?\d`
- `PREREG`
- `dd-meta`
- `runway_post_y5`
- `capalloc`
- `QC-\d`
- `archetype`
- `metadata`
- `硬接線`
- `接線[:：]`
- `Guardrail`
- `校驗紀錄`
- `判定規則`
- `\bgate\b`
- `\bF2\b`
- `row 8[ab]`
- `爆發候選路徑`
- `循環衛星進場路徑`
- CJK 字元後接半形 `,` `.` `:`（正則 `[㐀-䶿一-鿿豈-﫿][,.:]`）——一律應為全形 ，。：

---

## ③ Evidence 緊湊版

ticker=WDAY　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 195.79, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-08-27", "trading_days_since": 7, "flag_within_3d": false, "note": null}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 3, "current": 42.2, "high": {"value": 139.43, "date": "2025-01-31"}, "low": {"value": 56.57, "date": "2024-01-31"}, "current_percentile_within_annual_points": 0.0}, "ps": {"n_points": 4, "current": 4.65, "high": {"value": 10.77, "date": "2024-01-31"}, "low": {"value": 4.57, "date": "2026-01-31"}, "current_percentile_within_annual_points": 1.2}, "ev_s": {"n_points": 4, "current": 4.68, "high": {"value": 10.95, "date": "2024-01-31"}, "low": {"value": 4.82, "date": "2026-01-31"}, "current_percentile_within_annual_points": 0.0}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 146.19, "fy1_eps": 10.72, "fwd_pe": 13.64}, {"snapshot_date": "2026-06-04", "price_used": 144.28, "fy1_eps": 10.73, "fwd_pe": 13.45}, {"snapshot_date": "2026-06-23", "price_used": 124.21, "fy1_eps": 10.73, "fwd_pe": 11.58}, {"snapshot_date": "2026-07-16", "price_used": 144.78, "fy1_eps": 10.74, "fwd_pe": 13.48}, {"snapshot_date": "2026-07-30", "price_used": 160.34, "fy1_eps": 10.77, "fwd_pe": 14.89}, {"snapshot_date": "2026-08-13", "price_used": 198.68, "fy1_eps": 10.77, "fwd_pe": 18.45}, {"snapshot_date": "2026-08-28", "price_used": 195.79, "fy1_eps": 10.76, "fwd_pe": 18.2}, {"snapshot_date": "2026-09-04", "price_used": 195.79, "fy1_eps": 11.06, "fwd_pe": 17.7}], "current": 17.7, "high": 18.45, "low": 11.58, "current_percentile_within_window": 89.1, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 8 份快照（2026-05-26 (incremental updates over 2026-05-25 base) ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": 35.7, "return_26w_pct": 29.63, "excess_return_13w_pct": 31.17, "excess_return_26w_pct": 15.11, "benchmark": "^GSPC", "rsi14": 56.13, "rsi14_usable": true, "distance_from_52w_high_pct": -20.95, "distance_from_52w_low_pct": 74.04, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 11.06, "fy2": 13.21, "fy3": 15.42}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 10.76, "fy2": 12.64, "fy3": 14.67}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 10.73, "fy2": 12.64, "fy3": 14.66}, "fy1": {"revision_pct": 2.79, "from": 10.76, "to": 11.06, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": 4.51, "from": 12.64, "to": 13.21, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 5.11, "from": 14.67, "to": 15.42, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 3.08, "fy2_revision_90d_pct": 4.51, "fy3_revision_90d_pct": 5.18, "stale": false, "note": null}, "peer_financials": {"WDAY": {"gross_margin_pct": 75.77, "operating_margin_pct": 11.73, "fcf_margin_pct": 30.16, "rd_intensity_pct": 27.62, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "PLTR": {"gross_margin_pct": 84.8, "operating_margin_pct": 42.8, "fcf_margin_pct": 54.55, "rd_intensity_pct": 10.42, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "CRM": {"gross_margin_pct": 77.64, "operating_margin_pct": 21.87, "fcf_margin_pct": 34.23, "rd_intensity_pct": 14.38, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "MSFT": {"gross_margin_pct": 67.94, "operating_margin_pct": 46.78, "fcf_margin_pct": 20.19, "rd_intensity_pct": 10.72, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "NOW": {"gross_margin_pct": 74.77, "operating_margin_pct": 11.4, "fcf_margin_pct": 31.03, "rd_intensity_pct": 22.14, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}}, "edgar_concentrations": {"filing_type": "10-Q", "filing_date": "2026-08-27", "url": "https://www.sec.gov/Archives/edgar/data/1327811/000132781126000044/wday-20260731.htm", "excerpt": "Subscription services revenues accounted for approximately 93% of our total revenues for the three and six months ended July 31, 2026, and represented 97% of our total unearned revenue as of July 31, 2026. Subscription services revenues are driven primarily by the number of customers, the number of workers at each customer, the specific applications subscribed to by each customer, and the price of our applications. The mix of applications to which each customer subscribes can affect our financial performance due to price differentials in our applications. Pricing for our applications varies based on many factors, including the complexity and maturity of the application and its acceptance in the marketplace. New products or services offerings by competitors in the future could also impact the mix and pricing of our offerings. Subscription services revenues are recognized over time as services are delivered, beginning on the date our service is made available to the customer. Our subscription contracts typically have a term of three years or longer and are generally noncancelable. We generally invoice our customers annually in advance for subscription services. We may provide certain customers flexible payment terms and the timing of revenue recognition may differ from the timing of invoicing to our customers. Our professional services consulting engagements are billed on a time and materials or fixed price basis. We generally invoice our customers as the work is performed for time and materials arrangements, and in advance for fixed price arrangements. For contracts billed on a time and materials basis, revenues are recognized over time as the professional services are performed. For contracts billed on a fixed price basis, revenues are recognized over time based on the proportion of the professional services performed. In some cases, we supplement our consulting teams by subcontracting resources from our service partners and deploying them on customer engagements. As the Workday-related consulting practices of our partner firms continue to develop, we expect these partners to increasingly contract directly with our subscription customers for services engagements. Subscription Revenue Backlog Our subscription revenue backlog, which is also referred to as remaining performance obligations for subscription contracts, represents contracted subscription services revenues that have not yet been recognized and includes billed and unbilled amounts.", "note": null}, "latest_quarter_kpis": {"_required": true, "quarter": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "items": [{"metric": "總營收（GAAP）", "value": 2649, "unit": "$M", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿 investor.workday.com/news-and-events/press-releases/news-details/2026/Workday-Announces-Fiscal-2027-Second-Quarter-Financial-Results", "vs_consensus": "YoY +12.8%；consensus 約 $2.63B（Zacks，經 finance.yahoo.com 報導轉引），實際超出約 0.6%", "prior_quarter": "Q1 FY2027（季末 2026-04-30）：$2.542B，YoY +13.5%；QoQ +4.2%"}, {"metric": "Non-GAAP 營業利益率", "value": 31.1, "unit": "%", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（Non-GAAP operating income $824M／revenue $2.649B）", "vs_consensus": "無揭露單獨市場一致預期；公司同時將 FY27 全年 non-GAAP 營業利益率財測由 Q1 時的 30.5% 上修至 31.0%", "prior_quarter": "Q1 FY2027：31.8%（non-GAAP op income $809M／revenue $2.542B）"}, {"metric": "GAAP 營業利益率", "value": 11.8, "unit": "%", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（GAAP operating income $313M／revenue $2.649B；去年同期 $248M／10.6%）", "vs_consensus": null, "prior_quarter": "Q1 FY2027：13.3%（GAAP op income $338M／revenue $2.542B）"}, {"metric": "自由現金流（FCF）", "value": 460, "unit": "$M", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（營運現金流 $520M 減資本支出）", "vs_consensus": null, "prior_quarter": "Q1 FY2027：FCF $616M（營運現金流 $696M）；FY27 全年 FCF 財測（Q1 時）約 $3.18B（營運現金流 $3.45B－capex 約 $270M），Q2 未見更新財測數字"}, {"metric": "SBC 占總營收 %", "value": 17.44, "unit": "%", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "自算：公司新聞稿揭露 SBC $462M ÷ 總營收 $2.649B", "vs_consensus": null, "prior_quarter": "查無 Q1 FY2027 SBC 金額（未列入本輪 web_search 結果，未填造）"}, {"metric": "FY2027 全年財測（訂閱營收／non-GAAP 營業利益率，隨 Q2 財報上修）", "value": "訂閱營收 $9.940–9.950B（+13% YoY）；non-GAAP 營業利益率 31.0%", "unit": "guidance", "as_of": "Q2 FY2027 財報隨附財測，公告於 2026-08-27", "source": "公司新聞稿 investor.workday.com Q2 FY27 press release", "vs_consensus": null, "prior_quarter": "Q1 FY2027 時財測（2026-05-21）：訂閱營收 $9.925–9.950B（+13%），non-GAAP 營業利益率 30.5%"}, {"metric": "Q3 FY2027 財測（訂閱營收／non-GAAP 營業利益率）", "value": "訂閱營收 $2.515B（+12% YoY）；non-GAAP 營業利益率 30.0%", "unit": "guidance", "as_of": "Q2 FY2027 財報隨附財測，公告於 2026-08-27", "source": "公司新聞稿 investor.workday.com Q2 FY27 press release", "vs_consensus": null, "prior_quarter": null}, {"metric": "cRPO（12個月訂閱營收 backlog）", "value": 9.034, "unit": "$B", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（12-month subscription revenue backlog，YoY +14.2%）", "vs_consensus": null, "prior_quarter": "Q1 FY2027：$8.806B，YoY +15.5%（YoY 成長率於 Q2 由 15.5% 降至 14.2%，屬減速訊號）"}, {"metric": "Total RPO（訂閱營收 backlog 總額）", "value": 27.403, "unit": "$B", "as_of": "Q2 FY2027（季末 2026-07-31，公告於 2026-08-27）", "source": "公司新聞稿（Total subscription revenue backlog，YoY +8.0%）", "vs_consensus": null, "prior_quarter": "Q1 FY2027：$27.294B，YoY +10.9%（YoY 成長率於 Q2 由 10.9% 降至 8.0%）"}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | + | 2026-09-02 | Workday named a Leader in the 2026 Gartner Magic Quadrant for Cloud HCM Suites for 1,000+ Employee Enterprises for the eleventh consecutive year | Workday Newsroom press release, "Workday Named a Leader in 2026 Gartner Magic Quadrant for Cloud HCM Suites...Eleventh Consecutive Year" (newsroom.workday.com) | moat_trend,thesis.H |
| competitive_share_entrants#1 | - | 2026-08 | In the mid-market segment, Workday most often loses competitive deals to Rippling, HiBob, and Dayforce | Yahoo Finance, "Workday (WDAY) Faces an AI Threat. Is the Investment Case Broken?" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#2 | - | 2026-08 | Some net-new large-enterprise deals are taking longer to close, particularly in Federal, state/local/education (SLED), healthcare, and parts of the commercial market; market is pricing in a software-wide AI reset after Workday's own FY2027 subscription revenue growth guidance slowed to 12%-13% | Yahoo Finance, "Workday (WDAY) Faces an AI Threat. Is the Investment Case Broken?" (citing Workday FY2027 guidance commentary) | thesis.R,decision_inputs.bear,triggers |
| competitive_share_entrants#3 | - | 2026 | Andreessen Horowitz published an essay titled "Workday's Last Workday?" arguing AI agents (that can automate HR/finance workflows directly) pose a structural threat to seat-based SaaS incumbents like Workday | a16z.com, "Workday's Last Workday?" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#4 | + | 2026 | Workday holds roughly 19.8%-23.2% share of the dedicated Human Capital Management (HCM) software market, well ahead of SAP SuccessFactors HCM's ~5% share, per 6sense install-base tracking; FY2026 (ended Jan 2026) subscription revenue reached approximately $8.0 billion, growing ~16% YoY | 6sense, "Workday - Market Share, Competitor Insights in Human Capital Management" (6sense.com/tech/human-capital-management/workday-market-share) | moat_trend,thesis.H |
| competitive_share_entrants#5 | 0 | 2026 | In the broader ERP category (not just HCM), Workday's tracked install-base share (12.81%) trails Microsoft Dynamics (23.59%), SAP ERP (10.97% for legacy ECC) and SAP S/4HANA (9.96%) is close behind | 6sense, "Workday - Market Share, Competitor Insights in Enterprise Resource Planning (ERP)" | moat_trend |
| competitive_share_entrants#6 | 0 | 2026 | SAP SuccessFactors and Workday are described as the two enterprise HRIS finalists in most 2026 RFPs, with Workday generally winning on unified HR+Finance data model and payroll, while SuccessFactors wins where the buyer already runs SAP S/4HANA (ecosystem lock-in) | Redress Compliance, "SAP SuccessFactors vs Workday 2026. HRIS Decision" | moat_trend,thesis.R |
| customer_second_source#0 | 0 | 2026-08 | Workday's gross revenue retention rate remained stable at 97% through Q4 FY2026 and again at 97% in Q2 FY2027, indicating no broad-based customer attrition, second-sourcing, or in-housing trend among the existing customer base during this period | Workday Q4 FY2026 earnings call transcript (Motley Fool, fool.com) and Workday Q2 FY2027 investor materials (investing.com, "Workday Q2 FY27 slides: AI drives 25% of new sales, margins expand") | moat_trend,decision_inputs.bear |
| customer_second_source#1 | 0 | 2026-09-05 | No named large enterprise customer of Workday (e.g. Walmart, CVS Health, McKesson, Apple) was found to have publicly announced adding a second HCM/ERP vendor alongside Workday or moving core HR/Finance systems in-house in 2026 | Multiple queries against news/press-release indexes (erpresearch.com customer list, appsruntheworld.com Workday HCM customer database) returned no such announcement | decision_inputs.bear |
| customer_concentration_credit#0 | 0 | 2025-11-26 | WDAY Q3 FY2026 10-Q（期末2025-10-31）揭露：無單一客戶占總營收比重超過10%，三個月與九個月期間（2025或2024同期）皆同一結論 | https://investor.workday.com/files/doc_financials/2026/q3/WDAY-Workday-Inc-10-Q-2025-11-26-pdf_.pdf | decision_inputs.bear,moat_trend |
| customer_concentration_credit#1 | 0 | 2025-08-21 | WDAY Q2 FY2026 10-Q（期末2025-07-31）揭露：無單一客戶占應收帳款淨額或總營收超過10%（截至2025-07-31或2025-01-31止，及三/六個月期間2025或2024同期） | https://investor.workday.com/files/doc_financials/2026/q2/a690cd13-1e99-40eb-aff7-7e8efb886f75.pdf | decision_inputs.bear,moat_trend |
| supply_demand_durability#0 | - | 2026-05-21 | Cantor Fitzgerald 於2026-05將WDAY目標價由$200下修至$160（維持Overweight），理由為『市場預期偏保守且通路查核顯示中性偏負面』 | https://au.investing.com/news/earnings/workday-faces-earnings-test-as-ai-fears-weigh-on-hcm-market-93CH-4450147 | thesis.R,valuation,decision_inputs.bear |
| supply_demand_durability#1 | - | 2026-05-21 | 同篇報導指出結構性疑慮：能自動化HR/財務任務的AI agent可能侵蝕WDAY傳統『按員工人數計費』的訂閱模式；企業正將支出從傳統企業應用重新配置到AI專案 | https://au.investing.com/news/earnings/workday-faces-earnings-test-as-ai-fears-weigh-on-hcm-market-93CH-4450147 | thesis.R,moat_trend,decision_inputs.bear |
| supply_demand_durability#2 | - | 2026-05-21 | WDAY股價截至2026-05-21約較年初下跌40%，遠期FY2027本益比約12.3倍，較整體軟體類股折價，反映市場已部分計入AI破壞疑慮 | https://au.investing.com/news/earnings/workday-faces-earnings-test-as-ai-fears-weigh-on-hcm-market-93CH-4450147 | valuation,decision_inputs.bear |
| supply_demand_durability#3 | + | 2026-05-21 | WDAY FY2027 Q1（期末2026-04-30，發布於2026-05-21）實績：訂閱營收$23.54億，年增14.3%；12個月訂閱訂單餘額$88.06億，年增15.5%；總訂閱訂單餘額$272.94億，年增10.9%——目前需求動能尚未出現AI替代造成的萎縮跡象 | https://newsroom.workday.com/2026-05-21-Workday-Announces-Fiscal-2027-First-Quarter-Financial-Results | thesis.H,decision_inputs.bear |
| supply_demand_durability#4 | 0 | 2026-05-21 | WDAY FY2027全年財測（2026-05-21發布）：訂閱營收指引$99.25-99.50億，年增12-13%，非GAAP營業利益率上修至30.5% | https://newsroom.workday.com/2026-05-21-Workday-Announces-Fiscal-2027-First-Quarter-Financial-Results | thesis.H |
| supply_demand_durability#5 | 0 | 2026 | 產業研究機構（NextMSC）評估：ERP/HCM雲端＋AI轉型現階段被定性為結構性擴張期而非週期性反彈，美國ERP市場規模預估自2026年約690億美元成長至2030年1180-1250億美元（CAGR 13-14%），但2024-2026年年成長率已降至5%以下，稱為『加速前的暫緩期』 | https://www.nextmsc.com/blogs/how-is-ai-cloud-surge-redrawing-the-2026-erp-software-market | thesis.H,decision_inputs.bear |
| regulatory_antitrust#0 | - | 2026-03-01 | 在 Mobley v. Workday 集體訴訟中，聯邦法官於 2026 年 3 月初裁定原告的《反年齡就業歧視法》(ADEA) 集體訴訟指控可繼續進行，指控 Workday 的 AI 求職者篩選工具對 40 歲以上求職者造成歧視性拒絕。 | The Mobley v. Workday Case Didn't End. It Escalated. Here's Where It Stands. (aigovernanceforhr.com) | decision_inputs.bear,thesis.R |
| regulatory_antitrust#1 | - | 2026-06-22 | 加州法官於 2026 年 6 月 22 日裁定原告在 Mobley v. Workday 案中的加州州法（FEHA）歧視指控可繼續進行，Workday 未能駁回該部分訴訟；法院文件指出 Workday 的求職篩選軟體在涵蓋期間處理約 11 億份工作申請，使單一演算法訴訟可能擴大為大規模集體訴訟。 | Workday can't shake California AI discrimination claims (HR Dive, hrdive.com) | decision_inputs.bear,thesis.R,moat_trend |
| reg_tariff_export | - | - | (status=none；無 findings) |  |  |
| geo_supply_chain#0 | - | 2026-07-31 | Workday 於 SEC 申報（10-Q，期末 2026-07-31）揭露其在全球依賴第三方代管基礎設施夥伴（含 AWS、Google LLC、Microsoft Corporation）提供服務，任一夥伴發生中斷或干擾都可能影響其營運，此列為公司自揭露之風險因子（'Infrastructure Provider Concentration'）。 | Workday, Inc. Form 10-Q FY2026 (SEC EDGAR, https://www.sec.gov/Archives/edgar/data/0001327811/000132781126000044/wday-20260731.htm) | thesis.R,decision_inputs.bear |
| geo_supply_chain#1 | + | 2026-07-31 | 為降低單一設施中斷風險，Workday 將應用程式代管於美國、加拿大、歐洲及亞太地區多個第三方資料中心，並有內部程序可在單一設施發生災難時將服務轉移至其他地區——屬多地理區域分散揭露，非單一地緣風險區域集中。 | Workday, Inc. Form 10-Q FY2026 (SEC EDGAR, https://www.sec.gov/Archives/edgar/data/0001327811/000132781126000044/wday-20260731.htm) | thesis.R,decision_inputs.bear |
| end_markets#0 | + | 2025 | [HCM 終端市場] Workday 在 2025 年 HCM（人力資本管理）軟體市場的全球市占率約 22%；Workday、SAP SuccessFactors、Oracle HCM Cloud 三家合計囊括該市場近 58% 營收，Workday 為單一最大廠商。 | Workday 官方引用頁 'Workday US Leads in HCM and Payroll Market Shares'（forms.workday.com）及產業市場研究彙整（Fortune Business Insights／Polaris Market Research HCM market reports） | moat_trend,thesis.H |
| end_markets#1 | + | 2026 | [HCM 終端市場] 全球 HCM 軟體市場規模預估由 2026 年約 $37.52B 成長至 2034 年 $77.37B，2026–2034 CAGR 約 8.5%，成長動能來自 AI 整合與企業雲端採用擴大。 | Fortune Business Insights, 'Human Capital Management (HCM) Market Size, Share'（fortunebusinessinsights.com） | thesis.H,growth,valuation |
| end_markets#2 | + | 2025 | [Financial Management 終端市場] Workday Financial Management 所屬之財務管理軟體市場規模預估由 2025 年約 $3.92B 成長至 2034 年 $10.47B，2026–2034 CAGR 約 11.5%；北美為最大區域市場，2025 年規模約 $1.50B（占 38.2%）。 | Verified Market Reports, 'Global Workday Financial Management Service Market Size, Industry Share, Growth Trends & Forecast 2026-2034'（verifiedmarketreports.com） | thesis.H,growth |
| end_markets#3 | + | 2026-01-31 | [整體訂閱營收] Workday 整體訂閱服務營收（涵蓋 HCM 與 Financial Management 等產品線，公司未於申報中拆分個別產品線營收）FY2026 較 FY2025 成長 14.45%，自 $7.72B 增至 $8.83B。 | Bullfincher, 'Workday Revenue Breakdown By Segment'（bullfincher.io）；與 Workday FY2026 全年財報新聞稿一致 | thesis.H,growth,valuation |
| end_markets#4 | + | 2025-11-25 | [AI/Illuminate 產品線] Workday FY2026 Q3 財報（發布日 2025-11-25）法說指出 Illuminate AI agents 與企業端解決方案為當季營收成長動能之一，公司該季財報優於分析師預期並上修全年 non-GAAP 營益率展望。 | Workday newsroom, 'Workday Announces Fiscal 2026 Third Quarter Financial Results'（newsroom.workday.com, 2025-11-25）；InfotechLead, 'Workday AI Powers Q3 Fiscal-2026 Revenue Growth with Illuminate Agents and Enterprise Solutions' | thesis.H,growth |
| end_markets#5 | + | 2025-09-16 | [Adaptive Planning / Illuminate 產品線] Workday 於 2025-09-16 宣布擴大 Illuminate AI agents 陣容至 HR、Finance 與特定產業；其中 Adaptive Planning 的 Planning Agent 在早期使用客戶端可將資料探索與分析所需時間減少約 30%（約每月 100 小時）。 | Workday newsroom, 'Workday Illuminate™ Expands with New AI Agents for HR, Finance, and Industry'（newsroom.workday.com, 2025-09-16）；CFO Shortlist, 'Workday Adaptive Guide 2026: Enterprise FP&A' | thesis.H,growth |
| end_markets#6 | + | 2026-05-21 | [AI ARR 整體] Workday AI 相關年化經常性收入（AI ARR）已突破 $400M，年增率達三位數（triple-digit YoY）；報導與公司近期一次 Q1 財報（法說會 2026-05-21）AI agent 動能揭露同期。 | ERP Today, 'Workday's AI Agent Push Started Showing Up in its Q1 Earnings Numbers'（erp.today） | thesis.H,growth,valuation |
| substitute_technology#0 | - | 2026-02-25 | Workday stock fell sharply despite beating Q4 estimates as investors priced in fears that agentic AI could erode the seat-based licensing model underlying Workday's HCM/finance suite. | FinancialContent/MarketMinute, "The SaaSpocalypse of 2026: Workday Stock Plummets as Agentic AI Fears Overshadow Q4 Beat" | thesis.R,decision_inputs.bear,moat_trend |
| substitute_technology#1 | - | 2026-02-24 | Analyst commentary framed early 2026 as an 'AI inflection point' for Workday, with post-earnings volatility driven by questions over whether agentic AI substitutes could take over HR/Finance workflow tasks Workday currently monetizes per seat. | FinancialContent/Finterra, "The AI Inflection Point: A Deep Dive into Workday (WDAY) Amid Post-Earnings Volatility" | thesis.R,valuation |
| substitute_technology#2 | - | 2025-08-26 | Commentary noted that AI tools can automate tasks previously performed by employees, which directly threatens Workday's seat-based pricing model since licensing revenue is linked to headcount that AI adoption could shrink. | The Motley Fool, "Workday: Are AI Disruption Fears Real? Should You Buy the Stock?" | thesis.R,moat_trend,decision_inputs.bear |
| channel_business_model_shift#0 | + | 2025-11-19 | Workday announced an expansion of Workday GO, an all-in-one packaged offering aimed at businesses of all sizes (not just large enterprise), with the next release (Deployment Agent, Workday GO Global Payroll, Workday GO Partner Network integrations) rolling out February 2026 across the U.S., Canada, U.K., Ireland, Germany and additional regions — a structural shift from Workday's historical large-enterprise direct-sales motion toward a packaged, partner-resold mid-market channel. | Workday Newsroom press release, "Workday Expands Workday GO, the All-in-One 'Workday for All' Solution, to Support Businesses of All Sizes" | thesis.H,valuation |
| channel_business_model_shift#1 | 0 | 2025-11-21 | The Workday GO Partner Network launch includes named implementation/resale partners (TopBloc, Benefit Harbor, BNB, HR Path, Kainos, OneSource Virtual, Remote, Three Link Solutions) selling a lighter version of Workday to mid-market companies that don't need the full enterprise suite, indicating Workday is deliberately building a partner-led go-to-market layer distinct from its traditional direct enterprise sales force. | Enterprise Times, "Workday targets medium sized businesses to Grow with Workday Go" | thesis.H,decision_inputs.bear |
| capital_markets_pricing#0 | + | 2026-08-27 | Workday 2026-08-27公布FY2027第二季財報時上修FY2027訂閱營收指引至$9.940B–$9.950B(年增13%)，並將FY2027 non-GAAP營業利益率指引上修至31.0%；當季agentic AI產品新增ACV逾$100M，占當季全部新簽ACV逾25%。 | Workday newsroom press release 'Workday Announces Fiscal 2027 Second Quarter Financial Results' (newsroom.workday.com), 2026-08-27 | thesis.H,decision_inputs.bear,valuation |
| capital_markets_pricing#1 | 0 | 2026-08-27 | 財報公布當日(2026-08-27)股價收$193.57(+1.48%)，盤後波動輕微；報導解讀為市場視此次優於預期結果為『穩健執行』而非驚喜，反應偏中性。 | Investing.com, 'Workday Q2 FY27 slides: AI drives 25% of new sales, margins expand' | valuation,triggers |
| capital_markets_pricing#2 | 0 | 2026-09-01 | 財報後約一週內(2026年8月底至9月初)賣方目標價出現同時上修與下修：BTIG降評至中立(原買進)並撤回原$175目標價；Deutsche Bank降評至持有並下修目標價至$145(原$185)；Goldman Sachs上修目標價至$164(原$151)；Cantor Fitzgerald維持增持評等但下修目標價至$205(原$220)；Bernstein上修目標價至$238並維持優於大盤評等，理由為利益率展望轉正與FY2027指引更新。目標價區間$145–$238 vs numbers.price_at_dd，顯示賣方對本次財報後估值方向的分歧擴大。 | Investing.com/Yahoo Finance/Benzinga analyst-ratings coverage aggregated in 'These Analysts Revise Their Forecasts On Workday Following Q2 Results' (Benzinga) and 'Cantor Fitzgerald cuts Workday stock price target on guidance miss' (Investing.com) | valuation,thesis.R,decision_inputs.bear |
| capital_markets_pricing#3 | 0 | 2026-09-05 | 不同資料源對賣方目標價共識落差異常大：一來源引S&P Global統計41位分析師均值目標價$188.21、共識評等Buy；另一來源(51位分析師)則引中位數目標價達$280(區間$92–$326)。兩者中樞相差逾$90，反映Q2財報後賣方對合理估值的看法高度不一致，目標價區間本身 vs numbers.price_at_dd 需謹慎解讀。 | MarketScreener 'Workday Inc.: Target Price Consensus and Analysts Recommendations'; stockanalysis.com 'Workday (WDAY) Stock Forecast & Analyst Price Targets' | valuation,decision_inputs.bear |
| major_events#0 | + | 2026-08-13 | Reuters 於 2026-08-13 報導私募股權公司 Silver Lake 正與 Workday 洽談收購，消息帶動股價一度盤中飆漲近 30%、觸發交易暫停，市值一度推升至逾 $51B；Reuters Breakingviews 模擬每股 $227（30% 收購溢價）的假設性報價，隱含約 $53.8B 估值（約 2027E 營收 5 倍），交易仍在洽談中未有定案 | CNBC "Workday shares post best day in 10 years on Silver Lake takeover report" (2026-08-13); Axios "Silver Lake eyes Workday take-private" (2026-08-14) | triggers,capital_markets_pricing,decision_inputs.bear |
| major_events#1 | 0 | 2025-09-16 | Workday 於 2025-09-16 簽署最終協議以約 $1.1B 收購 AI 招募新創 Sana，預計於 Workday FY2026 第四季（截至 2026-01-31）完成交割 | Workday Newsroom "Workday Signs Definitive Agreement to Acquire Sana"; Workday Form 8-K (SEC EDGAR, filed 2025-09-16) | moat_trend,thesis.H |
| major_events#2 | 0 | 2025-11-01 | Workday 另收購求職者體驗 AI agent 公司 Paradox（AI 招募），預計於 Workday FY2026 第三季（截至 2025-10-31）完成交割；同期間亦於 2025 年 11 月收購雲端 API 整合平台 Pipedream | TipRanks "Workday announces acquisition of AI firm Paradox"; SeekingAlpha "Workday to acquire candidate experience AI agent Paradox"; Tracxn acquisitions list | moat_trend,thesis.H |
| major_events#3 | - | 2025-08-26 | Workday 於 2025-08-23 確認發生資料外洩事件，起因於第三方應用程式 Salesloft Drift（串接 Salesforce）遭駭客竊取 OAuth 憑證並用於在客戶 Salesforce 環境內執行搜尋；外洩範圍限於商業聯絡資訊、支援案件細節、租戶屬性（如 tenant/data center 名稱、產品名稱、服務、訓練紀錄、事件日誌），Workday 強調核心客戶租戶本身未被直接存取或入侵；此為波及逾 700 家組織的供應鏈級外洩事件（Salesloft Drift OAuth 憑證遭竊），Google、Salesloft 等多家公司同批受影響 | cybersecuritynews.com "Workday Confirms Data Breach"; BlackFog "The Salesforce Breach Wave Of 2025" | thesis.R,decision_inputs.bear |
| major_events#4 | - | 2025-09-01 | 因 2025 年 Salesloft Drift／Salesforce 資料外洩事件，已有消費者集體訴訟指控 Workday 與 Salesforce 未能妥善保護消費者個資，該訴訟於加州聯邦法院提出 | topclassactions.com "Workday, Salesforce class action claims companies failed to protect consumer data" | thesis.R,decision_inputs.bear |
| major_events#5 | - | 2026-08-19 | 受 Silver Lake 潛在收購案消息影響，多家股東權益律所（Kaskela Law、Schall Brown & Schwartz LLP、SBS Law）於 2026-08 中旬起宣布對 Workday 展開調查，主旨在確認若公司出售給 Silver Lake，董事會是否已善盡受託責任、股東是否能取得足額對價；此類為律所徵求潛在原告的訴前調查公告，非法院已受理之集體訴訟判決，且與傳統財報不實型證券詐欺求償性質不同 | BusinessWire "WDAY Investors Have Opportunity to Join Workday, Inc. Fraud Investigation with SBS Law" (2026-08-16); BusinessWire "Kaskela Law Firm Announces Investigation of Workday, Inc. (WDAY)" (2026-08-19) | triggers,decision_inputs.bear |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "found",
  "queries_run": [
   "Workday WDAY acquisition merger 2025 2026",
   "Workday Silver Lake acquisition talks buyout August 2026"
  ],
  "findings": [
   {
    "claim": "Reuters 於 2026-08-13 報導私募股權公司 Silver Lake 正與 Workday 洽談收購（take-private），消息帶動股價盤中一度飆漲近 30%、觸發交易暫停，市值一度推升至逾 $51B；Breakingviews 模擬假設性報價每股 $227（30% 溢價）隱含約 $53.8B 估值，若成交將為軟體業史上最大收購案之一，交易仍在洽談中、無成交保證",
    "source": "CNBC \"Workday shares post best day in 10 years on Silver Lake takeover report\" (2026-08-13); Axios \"Silver Lake eyes Workday take-private\" (2026-08-14)",
    "as_of": "2026-08-13",
    "direction": "+",
    "affects": [
     "triggers",
     "capital_markets_pricing",
     "decision_inputs.bear"
    ]
   },
   {
    "claim": "Workday 於 2025-09-16 簽署最終協議以約 $1.1B 收購 AI 招募新創 Sana（預計 FY2026 Q4 交割），另收購 Paradox（AI 求職者體驗 agent，預計 FY2026 Q3 交割）與 Pipedream（雲端 API 整合平台，2025-11 完成），為近 12 個月內三筆已公告/完成之併購案",
    "source": "Workday Newsroom \"Workday Signs Definitive Agreement to Acquire Sana\" (2025-09-16); TipRanks \"Workday announces acquisition of AI firm Paradox\"",
    "as_of": "2025-09-16",
    "direction": "0",
    "affects": [
     "moat_trend",
     "thesis.H"
    ]
   }
  ],
  "note": ""
 },
 "lawsuit_class_action": {
  "status": "found",
  "queries_run": [
   "Workday WDAY class action lawsuit securities fraud",
   "Workday data breach 2025 Salesforce Drift customer data compromised"
  ],
  "findings": [
   {
    "claim": "因 2025 年 Salesloft Drift／Salesforce 資料外洩事件，已有消費者集體訴訟指控 Workday 與 Salesforce 未能妥善保護消費者個資，該訴訟於加州聯邦法院提出",
    "source": "topclassactions.com \"Workday, Salesforce class action claims companies failed to protect consumer data\"",
    "as_of": "2025-09-01",
    "direction": "-",
    "affects": [
     "thesis.R",
     "decision_inputs.bear"
    ]
   },
   {
    "claim": "受 Silver Lake 潛在收購案消息影響，多家股東權益律所（Kaskela Law、Schall Brown & Schwartz LLP、SBS Law）於 2026-08 中旬起宣布對 Workday 董事會展開受託責任調查（訴前徵求潛在原告階段，尚非已受理之集體訴訟），聚焦股東若出售給 Silver Lake 是否取得足額對價",
    "source": "BusinessWire \"WDAY Investors Have Opportunity to Join Workday, Inc. Fraud Investigation with SBS Law\" (2026-08-16); BusinessWire \"Kaskela Law Firm Announces Investigation of Workday, Inc. (WDAY)\" (2026-08-19)",
    "as_of": "2026-08-19",
    "direction": "-",
    "affects": [
     "triggers",
     "decision_inputs.bear"
    ]
   }
  ],
  "note": ""
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Workday WDAY FDA clinical trial approval drug device 2025 2026",
   "Workday clinical trial FDA approval 2025 2026"
  ],
  "findings": [],
  "note": "非藥品/器材業務，已查證無相關監管動作（Workday 為人力資本/財務管理雲端軟體公司，非藥廠或醫材商，查無 FDA 或臨床試驗相關事項）。"
 },
 "product_recall_warning": {
  "status": "none",
  "queries_run": [
   "Workday WDAY product recall outage warning letter regulatory 2025 2026",
   "WDAY product launch recall warning letter"
  ],
  "findings": [],
  "note": "查無 Workday 產品召回或主管機關警告信紀錄；唯一相關資安事件（Salesloft Drift 第三方外洩）已列入 lawsuit_class_action 與 major_events 軸，性質為資料外洩非產品召回。"
 },
 "sec_investigation_restatement": {
  "status": "none",
  "queries_run": [
   "Workday WDAY SEC investigation restatement",
   "Workday accounting restatement SEC enforcement action 10-K amendment"
  ],
  "findings": [],
  "note": "查無 Workday 遭 SEC 正式調查或財報重編紀錄；股東權益律所所稱之「investigation」為私人律所徵求潛在原告之訴前調查（與 Silver Lake 收購案受託責任相關），非 SEC 主管機關調查，已另列於 lawsuit_class_action。"
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_WDAY_20260522.html",
 "date": "20260522",
 "schema": "v12.4",
 "dca_verdict": null,
 "dca_role": null,
 "price_at_dd": 121.85,
 "revlog": {
  "status": "unavailable"
 },
 "prior_meta": {
  "ticker": "WDAY",
  "schema": "v12.4",
  "date": "2026-05-22",
  "price_at_dd": 121.85,
  "currency": "USD",
  "market_cap_b": 30.4,
  "signal": "B",
  "trap": "🟢",
  "trap_label": "非陷阱",
  "moat": "B",
  "moat_score": 8.0,
  "moat_execution": 7,
  "moat_pricing_power": 9,
  "val": "🟢",
  "ma": "🟠",
  "ai_risk": "🟡",
  "industry_wind": "🟡",
  "fpe_fy1": 11.58,
  "fpe_fy2": 9.79,
  "pct_5y": 3,
  "peg_fy2": 0.93,
  "peg_3y": 0.71,
  "peg_5y": 0.64,
  "eps_cagr_3y": 16.4,
  "eps_source": "yfinance (FY+1/+2 consensus, FY+3 §8 logic; not in Excel snapshot)",
  "fcf_margin": 29.1,
  "nrr": 110,
  "rr_short": 2.1,
  "rr_mid": 3.76,
  "rr_5y": 9.87,
  "stress": {
   "pass": 2,
   "total": 2
  },
  "upside_short_pct": 47,
  "upside_mid_pct": 84,
  "upside_5y_pct": 220,
  "target_short": 178.8,
  "target_mid": 224.1,
  "target_5y": 390.0,
  "bear_price": 94.7,
  "growth_durability": 8,
  "quality_score": 8,
  "long_term_confidence": "高",
  "verdict": "B 觀望（thesis 完整、估值極便宜，但 Pure MA 🟠 暫不；待站回 W104 後 4 週確認）",
  "inception_dd": "DD_WDAY_20260522.html",
  "inception_date": "2026-05-22",
  "oneliner": "WDAY 5Y 分位 3%／PEG 0.71／Q1 FY27 Op Margin 1.8%→13.3%＋cRPO +15.5%加速＋Bhusri 回鍋 reset．護城河 B(8) 估值🟢+1→A；MA ❌→🟠盲點2救援．訊號 B 觀望，等站回 W104($220) 後 4 週進場．"
 },
 "drift_watch": [
  "dca_verdict",
  "dca_role",
  "signal",
  "val",
  "ma",
  "trap",
  "moat_trend",
  "runway_post_y5",
  "asym_ratio",
  "ev5y_pct",
  "irr_base_pct",
  "max_dd_pct",
  "bull_5y_price",
  "bear_5y_price",
  "p_bull_pct",
  "p_bear_pct",
  "rearm_trigger",
  "price_at_dd",
  "archetype",
  "cycle_position"
 ],
 "H": {
  "status": "ok",
  "format": "table",
  "rows": [
   {
    "id": "H1",
    "text": "cRPO（12 個月 sub rev backlog）持續加速 — Workday 業務動能未被 AI native 蠶食，enterprise 換代週期仍持續",
    "columns": {
     "2Y 驗證點": "Q2-Q4 FY27 cRPO YoY ≥ 13.5%（公司 guide）",
     "5Y 驗證點": "FY29 cRPO 達 -B+（從 FY26 .85B 起算 18% CAGR）",
     "10Y 驗證點": "FY31 sub rev .5-22B（10Y 從 FY26 .4B 起算 12% CAGR）",
     "具體數字門檻": "FY27 全年 cRPO 退出 ≥ 14% YoY；FY28 sub rev guide 仍 ≥ +11%",
     "信息來源": "WDAY Q1 FY27 8-K + 5/21 earnings call",
     "漂移觸發條件": "連 2 季 cRPO YoY &lt; 12% → 削弱（2Y 假設適用 QC-34 季節性、QC-35 漂移分級）"
    }
   },
   {
    "id": "H2",
    "text": "Non-GAAP Operating Margin 持續擴張至 35%+ — operational leverage 兌現，Bhusri reset 後 OpEx 紀律",
    "columns": {
     "2Y 驗證點": "FY27 退出 Non-GAAP OpMargin ≥ 31%（vs guide 30.5%）",
     "5Y 驗證點": "FY29 Non-GAAP OpMargin ≥ 33-34%",
     "10Y 驗證點": "FY31 Non-GAAP OpMargin 達 35%+ steady state",
     "具體數字門檻": "FY27 退出率 ≥ 30.5%；FY28 入場 guide ≥ 31%；R&D opex YoY ≤ rev YoY",
     "信息來源": "WDAY FY27 guide raised + 5/21 earnings call",
     "漂移觸發條件": "連 2 季 Non-GAAP OpMargin YoY 下降 ≥ 100bp → 削弱"
    }
   },
   {
    "id": "H3",
    "text": "Illuminate Agents 平台從 4,000 → 10,000+ active 客戶 — AI 戰略 兌現，pricing power 護城河加深",
    "columns": {
     "2Y 驗證點": "Q4 FY27 Illuminate active customer ≥ 8,000（QoQ 持續加倍）",
     "5Y 驗證點": "FY29 全客戶基數中 ≥ 60% 用 Illuminate（vs 現 ~20%）",
     "10Y 驗證點": "Illuminate ARR 成為獨立 line item 揭露 ≥ -B",
     "具體數字門檻": "連 2 季 Illuminate active customer QoQ &lt; 50% growth → 削弱；連 2 季客戶數絕對下降 → 反轉",
     "信息來源": "5/21 earnings call Bhusri 開場聲明",
     "漂移觸發條件": "2Y 假設適用 connected 2 quarter rule；5Y 假設適用 4 季滯後"
    }
   }
  ]
 },
 "R": {
  "status": "ok",
  "format": "table",
  "rows": [
   {
    "id": "R1",
    "text": "AI native HRIS 突破 enterprise 上岸戰，連續 3 季搶下大型客戶",
    "columns": {
     "對應假設": "H1",
     "時間尺度": "🔥 中期（4-6 季）",
     "監測指標": "競爭對手公開報導的 enterprise wins；Workday 新客戶 ACV 趨勢",
     "警戒閾值": "Rippling/Deel 任一拿下 ≥ -50M ACV 公開案例 ≥ 2 件；Workday 新客戶 ACV 連 2 季 YoY 下降"
    }
   },
   {
    "id": "R2",
    "text": "OpEx 紀律失守，Bhusri 在「AI reset」名義下擴張研發費用",
    "columns": {
     "對應假設": "H2",
     "時間尺度": "⚡ 短期（1-2 季）",
     "監測指標": "R&D / Sales OpEx YoY% vs Revenue YoY%",
     "警戒閾值": "連 2 季 R&D + S&M OpEx YoY% &gt; Rev YoY%；FY27 退出 Non-GAAP OpMargin &lt; 29%"
    }
   },
   {
    "id": "R3",
    "text": "Bhusri 接班 / 治理連續性失效，hyperscaler 自建 in-house HCM agent",
    "columns": {
     "對應假設": "H3",
     "時間尺度": "🐢 長期（2+ 年慢變數）",
     "監測指標": "2027/2 FY28 sub rev guide 是否仍能 raise；Apple/MSFT/AMZN 是否公告 in-house HCM",
     "警戒閾值": "Bhusri 在 2027/2 前未公布 permanent successor（≥ 50% 機率才砍倉）；任一 hyperscaler 公告 in-house HCM 計畫"
    }
   }
  ]
 },
 "triggers": {
  "status": "unavailable"
 },
 "inception_dd": {
  "path": "docs/dd/DD_WDAY_20260522.html",
  "date": "20260522",
  "schema": "v12.4"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_WDAY_20260522.html",
  "date": "20260522",
  "days_from_365d_mark": 259
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "WDAY",
 "current_verdict": {
  "verdict": null,
  "fundamental_grade": "B",
  "date": "2026-05-22",
  "freshness": "aging",
  "source": "docs/dd/DD_WDAY_20260522.html"
 },
 "decision_history": [
  {
   "date": "2026-05-22",
   "verdict": null,
   "role": null,
   "price_at_decision": 121.85,
   "fundamental_grade": "B",
   "to_date_pct": 52.79,
   "days": 101,
   "source_report": "docs/dd/DD_WDAY_20260522.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/WDAY.md\n[dd] 2026-05-22  DD|WDAY Workday|2026-05-22|v12.4\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_WDAY_20260522.md\n[dca] 2026-05-22  DCA|WDAY Deep Conviction Analysis|2026-05-22\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_WDAY_20260522.md"
}
```

### canonical_id（原樣）
```json
{
 "status": "ok",
 "primary": {
  "theme": "生產力 Copilot / AI 辦公整合",
  "path": "docs/id/ID_ProductivityCopilot_20260427.html",
  "skill_version": "v2.3",
  "as_of": "2026-04-27",
  "facts": {
   "status": "ok",
   "sections": {
    "supply": "PART III · SUPPLY SIDE\n 供給側：分發玩家矩陣，利潤往捆綁與資料集中\n 反直覺但可操作的結論：生產力 AI 的利潤往「握分發通路 + 專屬資料 + 成功轉型計費」的 incumbent 集中——純單點工具被免費捆綁與 agent 取代。\n\n 供給端是「分發 incumbent + 垂直專屬資料 + 受脅單點」三層。分發 incumbent：Microsoft（365 Copilot，345M 席次基底的捆綁）、Google（Workspace + Gemini 免費捆綁）——它們把 AI 內建進已有的 office suite，分發成本近零。垂直專屬資料：Salesforce（Slack + Agentforce per-action）、Adobe（Acrobat AI）、Atlassian（Rovo）、Workday（Illuminate HR/財務）、DocuSign（Iris 合約）——靠專屬資料與工作流守住。受脅單點：Zoom（AI Companion 免費送）、HubSpot（mid-market 被擠）——難對 AI 單獨收費。利潤明顯往「分發 + 專屬資料 + 成功轉計費」集中。\n\n \n Inference · 供給\n 分發 incumbent 與專屬資料者贏，純單點工具被吞\n 前提：分發 incumbent 近零成本捆綁 AI（MSFT/GOOGL）+ 專屬資料/workflow 高轉換成本（CRM/ADBE/WDAY）+ 單點工具無護城河、被免費捆綁/agent 取代 + 計費轉 consumption → 利潤往分發端 + 專屬資料端集中\n 當 AI 變成 suite 的內建功能，分發 incumbent（MSFT/GOOGL）靠既有席次基底近零成本獲客；握專屬資料與工作流者（CRM/ADBE/WDAY/TEAM）有高轉換成本、且能轉 consumption/outcome 計費；純單點工具（會議、筆記、mid-market CRM）對 AI 功能很難單獨收費，被免費捆綁與 agent 取代。MSFT 365 Copilot 20M 席次（產品有機成長、非併購灌入）證明分發捆綁的威力。\n 可證偽條件：若某純 AI-native 生產力新創用「跨 suite、AI-first」獨立長成大廠（不被捆綁吞），或開源/通用 agent 讓專屬資料優勢被抹平，則「分發+資料集中」論的某一面失效。\n \n\n \n 分發玩家矩陣 · 定位與動能\n \n玩家 | 定位 / 最新動能 | 遷移 | 角色\nMSFT | 365 Copilot 20M 席次、Cowork 計量計費 | ↑ | 分發王（捆綁 + 轉 consumption）\nGOOGL | Workspace + Gemini 免費捆綁 | ↑ | 分發 + 多雲 agentic\nCRM / ADBE / TEAM | Agentforce per-action / Acrobat AI / Rovo | ↑ | 專屬資料 + 轉型計費先驅\nDOCU / BOX / WDAY | 合約 / 文件 / HR 專屬資料 AI | ↑ | 垂直專屬資料\nZM / HUBS | AI Companion 免費 / mid-market 被擠 | ↓ | 單點受脅（捆綁/agent）\n\n \n 怎麼讀：分發 incumbent（MSFT/GOOGL）與專屬資料者（CRM/ADBE/TEAM/DOCU/BOX/WDAY）在 ↑，純單點工具（ZM/HUBS）在 ↓（被免費捆綁/agent 擠）。成本曲線省略說明：軟體無實體產能成本曲線；但有關鍵變動成本——Copilot 背後的推論 token 成本（見子題「Token 經濟學」），這正是逼著計費從 per-seat 轉 consumption 的根源。",
    "demand": "PART IV · DEMAND SIDE\n 需求側：採用爆發 vs ROI gap 的落地缺口\n 需求最剛性的是「員工已經在用 AI」——88% 員工常用、20M 付費席次；但最大的變數是「用了不等於有 ROI」——僅 39% 認得到可量化 EBIT 影響，落地門檻高。\n\n 第一引擎：採用爆發（現需）。需求已從試點變成普及：MSFT 365 Copilot 付費席次破 2,000 萬、單季 +500 萬、逾 60% Fortune 500 有 ≥1 萬席、Copilot 每用戶查詢數季增近 20%、每週使用黏著度已達 Outlook 等級。員工要的是「嵌在既有工作流裡、自動做掉雜事」。第二引擎：ROI gap（反需求/篩選器）。同時微軟自己的 Work Trend Index 顯示：88% 員工常用 AI、但只有 39% 認得到可量化的 EBIT 影響（49pp 落差）；AI 工具的「licensed 席次 vs active 使用」落差是所有軟體裡最大的。這個缺口既篩掉「買了沒用」的虛胖席次，也創造「證明 ROI、變更管理、agent 治理」的新需求。\n\n \n 需求三角驗證 · 採用 vs 營收 vs ROI\n \n視角 | 數值 | 口徑\n採用（bottom-up） | M365 Copilot 20M 付費席次（T1）、60% F500 ≥10k 席（第三方） | MSFT 法說 + 第三方統計\n營收 run-rate | ~$7.2B 年化（折扣後估 $1.5–2.5B real） | 推估（折扣 40–60%）\n落地篩選器 | 88% 用 AI / 僅 39% 有 EBIT 影響（49pp） | MSFT Work Trend Index\n\n \n 怎麼讀：採用（20M 席次）證明需求真實、分發 incumbent 吃得到；但 run-rate 名目（$7.2B）與折扣後實際（$1.5–2.5B）差很大、ROI gap（88%/39%）說明「用了不等於有價值」。採信「付費席次 + EBIT 兌現」作需求真實性的最硬證據，而非名目 run-rate。\n\n \n 多空為何都對\n 多頭測的是採用需求（20M 席次、88% 用、黏著度等同 Outlook），這幾乎沒爭議；空頭測的是商業模式與 ROI（per-seat→consumption 相變、seat compression、ROI gap 49pp）。兩者可同時為真：採用是真爆發（多頭對），但 per-seat 模式被自家 agent 侵蝕、且多數企業還沒兌現 EBIT（空頭對）。本報告因此把重心放在「模式相變下誰捕獲價值」，而非「Copilot 會不會被採用」。"
   }
  },
  "machine": {
   "sd_verdict": "balanced",
   "clock_phase": "II",
   "priced_in": null,
   "conviction": "high",
   "for_stage2_only": true
  }
 },
 "candidates": [
  {
   "theme": "生產力 Copilot / AI 辦公整合",
   "path": "docs/id/ID_ProductivityCopilot_20260427.html",
   "skill_version": "v2.3",
   "as_of": "2026-04-27",
   "sd_verdict": "balanced",
   "clock_phase": "II",
   "conviction": "high",
   "priced_in": null,
   "for_stage2_only": true
  },
  {
   "theme": "Agentic AI 平台",
   "path": "docs/id/ID_AgenticAIPlatform_20260903.html",
   "skill_version": "v4.0",
   "as_of": "2026-09-03",
   "sd_verdict": "split",
   "clock_phase": "II",
   "conviction": "mid",
   "priced_in": "mid",
   "for_stage2_only": true
  }
 ],
 "note": "primary 由 conviction desc + publish_date desc 排序機械選出，非人工裁定——ticker 掛在多個產業主題下時，Stage 1 判斷層應覆核 candidates 是否有更貼題者。"
}
```


---

## ④ 最新一季逐字稿全文

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/WDAY/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
  ],
  "items": [
    {
      "topic": "guidance",
      "claim": "Workday raised FY26 subscription revenue guidance to $8.815 billion, 14% growth, reflecting the Paradox acquisition impact.",
      "quote": "FY '26 subscription revenue guidance to $8.815 billion",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "guidance",
      "claim": "Zane Rowe gave Q3 FY26 subscription revenue guidance of approximately $2.235 billion, also 14% growth.",
      "quote": "expect Q3 FY '26 subscription revenue to be approximately",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "guidance",
      "claim": "Zane Rowe guided Q3 cRPO growth of 15%-16%, explicitly excluding the Paradox acquisition impact.",
      "quote": "We expect cRPO to increase between 15% and 16% in Q3.",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "margin",
      "claim": "Carl Eschenbach stated Q2 non-GAAP operating margin was 29%, alongside 14% subscription revenue growth.",
      "quote": "non-GAAP operating margin of 29%",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "margin",
      "claim": "Zane Rowe raised FY26 non-GAAP operating margin guidance to approximately 29%, citing ongoing efficiencies.",
      "quote": "our FY '26 non-GAAP operating margin to approximately 29%",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "margin",
      "claim": "Zane Rowe guided Q3 non-GAAP operating margin of 28%, and noted GAAP margins run ~17-21 points lower.",
      "quote": "For Q3, we expect non-GAAP operating margin of 28%.",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Workday repurchased $299 million of shares during the quarter.",
      "quote": "repurchased $299 million of our shares during the quarter",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Workday ended the quarter with $8.2 billion in cash and marketable securities.",
      "quote": "$8.2 billion in cash and marketable securities",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Workday had $1.2 billion in remaining buyback authorization as of July 31.",
      "quote": "$1.2 billion in remaining authorization as of July 31",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "product",
      "claim": "Workday signed a definitive agreement to acquire Paradox, a conversational-AI candidate experience agent, expected to close in Q3.",
      "quote": "signed a definitive agreement to acquire Paradox",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "product",
      "claim": "Carl Eschenbach disclosed Workday also recently acquired Flowise, a low-code platform for building AI agents.",
      "quote": "we also recently acquired Flowise, a leading low-code",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "product",
      "claim": "Workday launched Workday Government as a wholly owned subsidiary dedicated to the U.S. government sector.",
      "quote": "we launched Workday Government, a wholly owned subsidiary",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "competition",
      "claim": "Responding to a question about AI-driven SaaS disruption, Carl Eschenbach called the negative impact on seat-based models overblown.",
      "quote": "impact on seat-based models are completely overblown",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "competition",
      "claim": "Carl Eschenbach cited winning customers in Germany located near larger competitors' home base as evidence of international competitive strength.",
      "quote": "right in the backyard of some of our bigger competitors",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "risk",
      "claim": "Carl Eschenbach acknowledged a headwind in the state and local government portion of the SLED business.",
      "quote": "we did see a little bit of headwind in that market",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "risk",
      "claim": "Carl Eschenbach flagged that higher education customers are under funding pressure, including loss of federal funding.",
      "quote": "higher ed is clearly under pressure",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "risk",
      "claim": "Despite analyst questions about tariffs and geopolitical cross-currents, Carl Eschenbach said Workday has not seen international macro headwinds this quarter.",
      "quote": "we haven't necessarily seen any blowback or headwinds",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "customer",
      "claim": "Carl Eschenbach stated Workday serves more than 65% of the Fortune 500.",
      "quote": "We are proud to serve more than 65% of the Fortune 500",
      "speaker": "Carl Eschenbach (CEO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "customer",
      "claim": "Zane Rowe reported gross revenue retention remained healthy at 97%.",
      "quote": "gross revenue retention rates remained healthy at 97%.",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "commitment",
      "claim": "Zane Rowe reaffirmed Workday is tracking well against deliverables tied to the previously flagged DIA (Defense Intelligence Agency) contract.",
      "quote": "talked all year long about the deliverables tied to the DIA",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "commitment",
      "claim": "Zane Rowe said management will host a Financial Analyst Day on September 16 to share the framework for future growth and margin expansion.",
      "quote": "our upcoming Financial Analyst Day on September 16",
      "speaker": "Zane Rowe (CFO)",
      "date": "2025-08-21",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 給出 FY26 訂閱營收指引 $8.828B、成長 14%",
      "quote": "FY '26 subscription revenue of $8.828 billion, growth of 14%",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 給出 Q4 訂閱營收指引 $2.355B、成長 15%",
      "quote": "subscription revenue of $2.355 billion, growth of 15%",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 重申 FY27 訂閱營收成長約 13%（與 9 月 Analyst Day 一致）",
      "quote": "subscription revenue growth of approximately 13%",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 說明 Q3 non-GAAP 營益率為 28.5%",
      "quote": "a non-GAAP operating margin of 28.5%",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 給出全年 non-GAAP 營益率指引約 29%",
      "quote": "approximately 29% for the full year",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 說明 Q3 執行庫藏股買回 $803M",
      "quote": "repurchasing $803 million of our shares during the quarter",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 說明未來將再買回 $3.6B，累計達 $5B 總回購目標",
      "quote": "leading to $5 billion in total repurchases",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 揭露截至 10/31 現有授權額度剩餘 $4.4B",
      "quote": "$4.4 billion remaining under our current authorization",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 上修 FY26 營運現金流指引至 $2.90B",
      "quote": "operating cash flow outlook to $2.90 billion",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "product",
      "claim": "CEO 說明超過 75% 核心客戶正在使用 Workday Illuminate AI",
      "quote": "our core customers are using Workday Illuminate AI",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "product",
      "claim": "CEO 提到今年平台上 AI actions 已超過 10 億次",
      "quote": "well over 1 billion AI actions on the Workday platform",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 指出 Q3 一半以上全球新簽約同時包含 HR 與財務模組",
      "quote": "all net new global deals in Q3 included both HR and finance",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 指出客戶端員工人數持續溫和成長",
      "quote": "our customers' headcount levels continued to grow modestly",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 在 Q&A 重申客戶群整體人數年增率為正",
      "quote": "the headcount of our customer base is up year-over-year",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "risk",
      "claim": "CEO 承認高度依賴聯邦補助的機構（主要是高等教育）出現個別衝擊",
      "quote": "institutions that rely heavily on federal grants",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 承認聯邦與 SLED 業務因財政資金問題受到一些衝擊",
      "quote": "did see some impact in Fed and SLED tied to fiscal funding",
      "speaker": "Zane Rowe",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 回應分析師關於 AI 新創威脅的提問，重申上季說法是對的",
      "quote": "a completely overblown narrative, and I thought it was flat",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 主張客戶最終還是回頭選擇他們信任的既有供應商",
      "quote": "they're ultimately coming back to the vendors they trust",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO 舉例一家保險公司回頭簽下全套 10 年合約",
      "quote": "choosing our full suite with a 10-year commitment",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO 提到正就 DIA 平台擴大合作進行下一階段洽談",
      "quote": "negotiating a follow-on to take that platform to the next",
      "speaker": "Carl Eschenbach",
      "date": "2025-11-25",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives FY27 subscription revenue guidance range.",
      "quote": "$9.925 billion to $9.950 billion, growth of 12% to 13%",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives Q1 FY27 cRPO growth guidance range.",
      "quote": "cRPO to increase between 14.5% and 15.5% in Q1",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "margin",
      "claim": "CFO gives FY27 non-GAAP operating margin guidance.",
      "quote": "non-GAAP operating margin of approximately 30%",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "margin",
      "claim": "CFO says the FY27 margin outlook reflects stepped-up AI investment spend.",
      "quote": "an accelerated pace of AI investment",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "margin",
      "claim": "CFO attributes part of Q4 margin strength to a slower hiring ramp.",
      "quote": "a slightly slower ramp in hiring",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses Q4 share repurchase amount.",
      "quote": "We repurchased $1.5 billion of our shares",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses remaining buyback authorization at quarter end.",
      "quote": "$2.9 billion in remaining authorization",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses year-end cash and marketable securities balance.",
      "quote": "$5.4 billion in cash and marketable securities",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "product",
      "claim": "President of Products cites full-year AI action volume across the platform.",
      "quote": "1.7 billion AI actions across the Workday platform",
      "speaker": "Gerrit Kazmaier",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "product",
      "claim": "President of Products states the count of new organic role-based agents moving to GA.",
      "quote": "12 new organically developed role-based agents",
      "speaker": "Gerrit Kazmaier",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "product",
      "claim": "President of Products states the GA date for Sana Core and Sana Enterprise.",
      "quote": "Sana Core and Sana Enterprise went into GA on February 15",
      "speaker": "Gerrit Kazmaier",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "product",
      "claim": "President of Products states current ARR run-rate from emerging AI solutions.",
      "quote": "ARR from these solutions is now over $400 million",
      "speaker": "Gerrit Kazmaier",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "competition",
      "claim": "CEO describes some third-party vendors as free-riding on Workday's underlying system of record.",
      "quote": "at some level, parasites on Workday",
      "speaker": "Aneel Bhusri",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "competition",
      "claim": "CEO names AI leaders that run Workday as part of an argument that AI is built on top of cloud incumbents rather than replacing them.",
      "quote": "Anthropic, Google and OpenAI, all run Workday",
      "speaker": "Aneel Bhusri",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "customer",
      "claim": "President and Chief Commercial Officer names customer expansions in the quarter.",
      "quote": "customers like Anthropic, Ally Financial and Otis Elevator",
      "speaker": "Robert Enslin",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "customer",
      "claim": "CFO states gross revenue retention rate for the period.",
      "quote": "Gross revenue retention rates remained strong at 97%",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "commitment",
      "claim": "President and Chief Commercial Officer names early adopters of the new Flex Credits pricing model.",
      "quote": "Accenture, Nike and Merck are among the first",
      "speaker": "Robert Enslin",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "risk",
      "claim": "President and Chief Commercial Officer flags elongation in large enterprise deal closing.",
      "quote": "large enterprise deals are taking longer to close",
      "speaker": "Robert Enslin",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "risk",
      "claim": "President and Chief Commercial Officer names the segments most affected by deal elongation.",
      "quote": "particularly in Fed, SLED and health care",
      "speaker": "Robert Enslin",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "risk",
      "claim": "CFO notes average contract duration declined year-over-year.",
      "quote": "contract duration in the quarter was down year-over-year",
      "speaker": "Zane Rowe",
      "date": "2026-02-24",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "topic": "customer",
      "claim": "CEO cites gross retention of 97-98% across the >11,000-customer installed base as evidence customers are not leaving.",
      "quote": "a gross retention rate of 97% to 98%.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "customer",
      "claim": "CEO states Workday software sits on the desktop of 73 million end users.",
      "quote": "We are on the desktop of 73 million users, 73 million users.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "customer",
      "claim": "CEO states 75% of customers already use AI features bundled into the core platform subscription, without an added AI upcharge.",
      "quote": "75% of our customers are using AI that's in the platform",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes Workday's AI differentiation as building first-party, enterprise-focused domain-specific agents.",
      "quote": "we're building first-party agents, our own agents",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "product",
      "claim": "CEO says Workday has announced 13 first-party AI agents to be showcased at the upcoming user conference.",
      "quote": "We have 13 of them we've announced.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "product",
      "claim": "CEO frames the Agent System of Record as the orchestration layer for onboarding third-party AI agents like employees.",
      "quote": "the Agent System of Record as the orchestration layer",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "competition",
      "claim": "CEO recalls repeated existential threats to VMware from open-source hypervisors that never materialized, drawing a parallel to today's AI-disruption narrative.",
      "quote": "We were going out of business.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "competition",
      "claim": "Discussion references the earlier market debate that AWS would commoditize software as a historical analogue to the current AI-commoditization fear.",
      "quote": "AWS is going to commoditize software debate",
      "speaker": "Kasthuri Rangan, Analyst",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "competition",
      "claim": "CEO says Workday is model-agnostic and treats LLM providers as interchangeable rather than betting on one winner.",
      "quote": "they're interchangeable for us from an LLM perspective.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO states Workday has acquired 4 AI companies in the last 1.5 years as part of an inorganic AI build-out.",
      "quote": "in the last 1.5 years, we bought now 4 AI companies",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO confirms the most recent acquisition is Paradox, a conversational AI platform aimed at frontline workers.",
      "quote": "we announced an acquisition of a company called Paradox",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO describes launching a dedicated Workday Government subsidiary to invest in and target the U.S. federal market.",
      "quote": "we launched actually the Workday Government subsidiary",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "risk",
      "claim": "CEO acknowledges AI will drive further economies of scale, implying pressure on customer headcount/seat growth even as he disputes it being AI-driven job cuts.",
      "quote": "AI will drive further economies of scale",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "risk",
      "claim": "CEO gives an ambiguous, self-qualifying statement on customer headcount growth trend immediately before saying overall headcount still grows.",
      "quote": "It's moderating. It's not growing.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO says Workday will provide a further update on its AI pricing and monetization strategy at the upcoming Financial Analyst Day.",
      "quote": "we'll provide a further update on our AI pricing strategy",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO states the AI business is growing 100% year-over-year.",
      "quote": "our AI business 100% year-over-year",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO repeatedly defers quantification of the AI book of business to the following week's Financial Analyst Day.",
      "quote": "Come next week.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO commits to keeping Flowise, the acquired agent-building platform, open source going forward.",
      "quote": "we are going to keep an open source platform.",
      "speaker": "Carl Eschenbach, CEO",
      "date": "2025-09-10",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 公布 FY28 財務框架，訂閱營收 CAGR 依低/中/高情境設定區間。",
      "quote": "that ranges from 12% to 15% in each of these scenarios",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "guidance",
      "claim": "同一 FY28 框架下，非 GAAP 營業利益率區間為 33%-36%。",
      "quote": "and that ranges from 33% to 36%.",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "guidance",
      "claim": "管理層設定 FY28 非 GAAP rule of 48% 目標（成長+利潤率合計）。",
      "quote": "our target here is a non-GAAP rule of 48%.",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO 特別把分析師注意力錨定在 FY27 訂閱營收成長 13%（框架中值下緣）。",
      "quote": "And I want to anchor you to the 13% number.",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 說明 FY28 財務框架不含近期宣布的 Sana Labs 收購案。",
      "quote": "none of the guidance you see here includes our most recent",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "margin",
      "claim": "本財年非 GAAP 營業利益率預期較去年提升 3 個百分點至 29%。",
      "quote": "climb 3 points on a year-over-year basis to 29%",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "margin",
      "claim": "股權薪酬占營收比重本財年降至 17%，較去年下降 1 個百分點。",
      "quote": "expecting 17%, off 1 point year-over-year",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "margin",
      "claim": "FY28 目標為非 GAAP rule 扣除 SBC 後之 rule of 35%。",
      "quote": "committing a target rule of 35%",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "董事會核准新增 40 億美元庫藏股額度，累計至 FY27 將執行 50 億美元回購。",
      "quote": "we're going to be buying back $5 billion through FY '27.",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "資本配置哲學第一順位是有機投資（尤其 AI），其次才是併購與庫藏股。",
      "quote": "primary focus is organic investment, in particular, in AI",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "公司設定 FY28 每股自由現金流目標為 15 美元。",
      "quote": "targeting free cash per share of $15 in FY '28.",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 直接反駁「AI 正在吞噬軟體業」的市場敘事，稱其過度渲染。",
      "quote": "AI is eating the software world is completely overblown",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "competition",
      "claim": "面對 AI 原生新創威脅的提問，產品長主張 Workday 上萬名工程師用 AI 工具提速後可壓過小型新創。",
      "quote": "outrun any start-up with 10 people going 10x faster.",
      "speaker": "Gerrit Kazmaier",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "competition",
      "claim": "回應「SaaS 將被 AI 架構取代」的看法時，產品長主張是既有業務流程驅動 AI、而非反過來。",
      "quote": "It's not like the AI is driving the process",
      "speaker": "Gerrit Kazmaier",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "CEO 定位 Sana Labs 收購案為 Workday 全新 AI 原生入口／使用者介面。",
      "quote": "This is the new front door. The new UI for Workday is AI.",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "公司發表 Flex Credits，一種以用量計費的新定價模式。",
      "quote": "Flex Credits, a consumption-based pricing model",
      "speaker": "Gerrit Kazmaier",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "CTO 說明開放平台策略中，agent 對外介面採用 MCP 協議標準。",
      "quote": "For agents, we're embracing MCP.",
      "speaker": "Peter Bailis",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "過去一年 AI 相關營收動能自 2.5 億美元成長至逾 4.5 億美元。",
      "quote": "from over $250 million to greater than $450 million",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "特定 agentic AI SKU 的 ARR 在過去一年自不到 5,000 萬美元成長至逾 1.5 億美元。",
      "quote": "less than $50 million to more than $150 million in ARR",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 強調公司在 11,000 個客戶基礎與 97% 留存率上具有獨特定位以迎接 AI 轉型。",
      "quote": "11,000 customers, 97% retention rate",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 說明其財務框架的低情境假設是總體經濟轉弱、成長引擎放緩。",
      "quote": "a stable macro similar to what we're experiencing today",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "risk",
      "claim": "回應分析師提問時，CFO 表示若成長放緩，公司會在未見到預期回報的領域收回投入資源。",
      "quote": "we'll continue to find opportunities to pull back",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "commitment",
      "claim": "被問及 2023 年裁員後回聘承諾時，CFO 表示目前仍在招募，但強調招募地點與方式會改變。",
      "quote": "We are hiring right now, and how we hire and where we hire",
      "speaker": "Zane Rowe",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO 說明即便持續下修股權薪酬占比，仍須用股票留才以吸引頂尖人才。",
      "quote": "leverage equity and stock to get them to join Workday.",
      "speaker": "Carl Eschenbach",
      "date": "2025-09-16",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "topic": "product",
      "claim": "Kazmaier sizes Workday's total addressable market at roughly $200 billion.",
      "quote": "the TAM that we're operating in is roughly $200",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "product",
      "claim": "Kazmaier says a roughly $3 billion frontline-work market segment exists where Workday currently has a narrow offering.",
      "quote": "on the planet are falling in the frontline work category",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "customer",
      "claim": "Kazmaier says Workday's mid-market win rates are roughly the same as its large-enterprise win rates.",
      "quote": "specifically in mid-market, we actually -- we have the same",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "guidance",
      "claim": "Kazmaier says Workday will increase margin per the framework it previously guided, by realizing more operating leverage.",
      "quote": "we guided in the framework that we gave out",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "margin",
      "claim": "Kazmaier says Workday has lots of operating leverage across its entire operating expense base.",
      "quote": "we have lots of operating leverage across everything",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "margin",
      "claim": "Kazmaier says Workday delivered on its margin goals while also investing in organic innovation.",
      "quote": "delivered on our margin goals, and we invested",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Kazmaier says Workday pursued aggressive M&A in the same period it delivered on its margin goals.",
      "quote": "We pursued aggressive M&A.",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Kazmaier says Workday acquired Sana because it is a leading AI experience.",
      "quote": "Now we acquired Sana because it is truly a",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "competition",
      "claim": "Responding to a question framing rivals as newer, Kazmaier says many competitors are actually older than Workday.",
      "quote": "Actually, many of them are older, right?",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "competition",
      "claim": "Kazmaier says accuracy is the number one criterion that defines enterprise acceptance of AI.",
      "quote": "There is one #1 criteria which defines the acceptance of AI",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "customer",
      "claim": "Kazmaier says customers are seeing fantastic results (reduced service-center contact rates) from AI-driven employee service delivery.",
      "quote": "they're seeing fantastic results with that, right?",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "risk",
      "claim": "Kazmaier frames the debate over the future of SaaS/system-of-record vendors as a path from system of record to system of action.",
      "quote": "path is from system of record to system of action.",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "commitment",
      "claim": "Kazmaier commits to Workday remaining acquisitive going forward.",
      "quote": "And we're going to remain acquisitive, right? I'm",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "product",
      "claim": "Kazmaier says Workday launched \"Flex Credits\" as a new usage-based monetization concept for AI features.",
      "quote": "So what we launched is a concept called Flex Credits.",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "topic": "product",
      "claim": "Kazmaier describes a new no-code agent builder letting people quickly build agentic automation, paired with the Pipedream acquisition for connectivity.",
      "quote": "people can build very quickly in a nontechnical way, agentic",
      "speaker": "Gerrit Kazmaier (President, Product & Technology)",
      "date": "2025-12-11",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    }
  ],
  "qa_flags": [
    {
      "question": "Kash Rangan (Goldman Sachs) followed up asking for Carl Eschenbach's viewpoint on Sam Altman/OpenAI's comment about entering SaaS.",
      "response_pattern": "Carl Eschenbach did not engage with the substance, saying he had no viewpoint because he did not know what OpenAI meant, then pivoted to a generic line that 'AI is software' rather than addressing the competitive implication raised.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "question": "Karl Keirstead (UBS) asked Zane Rowe to roughly size the basis-point upside to cRPO from elevated early renewals in the quarter.",
      "response_pattern": "Zane Rowe did not give a specific bps figure, instead saying it was 'probably above the range' and that early renewals were 'a big contributor,' avoiding quantification of the specific number requested.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "question": "Raimo Lenschow (Barclays) pressed Zane Rowe to reconcile the math: a Q2 beat of roughly $9 million plus $15 million from Paradox should imply a larger guidance raise than what was given.",
      "response_pattern": "Zane Rowe did not directly reconcile the arithmetic the analyst laid out, instead repeating general reassurance ('a lot that goes into our forecast,' 'we feel great about the year') without addressing the specific dollar gap questioned.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q2_2026_Earnings_Call_20250821.md"
    },
    {
      "question": "Karl Keirstead 追問 Q4 cRPO 15%-16% 中約 2.25 個百分點來自 tenant/Paradox/Sana 一次性因素的拆解算法是否正確",
      "response_pattern": "Zane Rowe 只用「sort of generally in line」等模糊字眼確認方向，未逐項驗證或訂正精確拆解數字，隨後轉談另一個指標（Sana/Paradox 對訂閱營收成長的貢獻）而非直接答 cRPO 拆解",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q3_2026_Earnings_Call_20251125.md"
    },
    {
      "question": "John DiFucci (Guggenheim) pressed on why the Q1 FY27 subscription guide implies roughly a $25 million sequential decline when the previously disclosed DIA nonrecurring benefit was only about $15-20 million, saying the math does not add up for a subscription model.",
      "response_pattern": "Zane Rowe repeated the DIA contract roll-off and fewer-days-in-Q1 explanations across two consecutive answers without reconciling the specific dollar gap DiFucci pointed to; on the second follow-up he closed with 'nothing more than that' rather than walking through a numeric bridge.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "question": "Alex Zukin (Wolfe Research) asked directly whether the 35% FY28 operating margin target set at the prior Financial Analyst Day is still on the table.",
      "response_pattern": "Zane Rowe did not confirm or deny the 35% figure; he deflected to 'update later on in the year at our next financial analyst update' and reframed the priority as driving growth over hitting the operating margin target, without restating or affirming the number.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "question": "Michael Turrin (Wells Fargo) asked if there is a way to size the cRPO impact from the Q4 large-deal elongation Rob Enslin described in his prepared remarks.",
      "response_pattern": "Robert Enslin did not give a number or range for the cRPO impact; he said the deals are 'elongated' rather than lost and pivoted to discussing nonorganic agent sales and Flex Credits consumption momentum instead of quantifying the impact asked about.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Q4_2026_Earnings_Call_20260224.md"
    },
    {
      "question": "Analyst asks whether seat-based/headcount growth pressure tied to AI is structural or just a correction from pandemic-era overhiring (noted as the same question asked on the earnings call three weeks earlier).",
      "response_pattern": "CEO calls the narrative 'completely overblown', pivots to an anecdote about a Fortune 10 CIO and a TAM-expansion argument rather than giving specific seat/logo growth figures, and gives internally inconsistent phrasing ('It's moderating. It's not growing.') immediately before stating overall customer headcount continues to grow.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "question": "Analyst asks the CEO to quantify the AI book of business, referencing that peer SaaS companies already disclose such a metric.",
      "response_pattern": "CEO declines to give any current figure and instead responds twice with 'Come next week', deferring quantification to the Financial Analyst Day rather than answering on the spot.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Goldman_Sachs_Communacopia_Technology_Conference_2025_20250910.md"
    },
    {
      "question": "Karl Keirstead (UBS)：把 FY27 成長目標從 15% 下修到 13%，是因為聽取建議想更保守，還是環境真的變得比預期更艱難？",
      "response_pattern": "CFO 未直接回答「是否環境變艱難」這個二選一問題，改談框架設計哲學、傾聽建議、以及對數字有信心，全程未正面承認或否認總體環境轉差。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "question": "Brent Thill (Jefferies)：公司裁員 1,750 人中已回聘約 1,000 人，是否仍承諾回聘剩餘人數，或會放慢招募步調？",
      "response_pattern": "CFO 回答「目前仍在招募」但自承先前對回聘時程「說得比較模糊」，未給出具體剩餘人數的回補時間表或是否維持原承諾。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Analyst_Investor_Day_Workday_Inc_20250916.md"
    },
    {
      "question": "Analyst (Raimo Lenschow) asked how management balances pressure to deliver margin expansion against the amount of work still needed on Workday's technology/product side, after having earlier raised the same worry as a joke about Kazmaier's R&D budget getting cut.",
      "response_pattern": "Kazmaier's first response to the earlier framing of this concern was a joking deflection (\"All investors as concerned as you are about my well being. I love it.\") rather than a direct answer; the analyst had to restate the question before Kazmaier gave a substantive response.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    },
    {
      "question": "Analyst asked, using a P-times-Q framing, whether AI/agents reducing the number of employee seats could create a revenue offset problem given Workday's historically per-employee pricing model.",
      "response_pattern": "Kazmaier answered qualitatively (asserted it will not be a black-and-white/tectonic shift and cited the global market index still showing growth) without providing any quantified split, percentage, or offset estimate between seat-based and usage-based (Flex Credits) revenue.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/WDAY/WDAY_Barclays_23rd_Annual_Global_Technology_Conference_20251211.md"
    }
  ]
}

```

---

## ⑥ judgment-rules.md 全文

# stock-analyst v16.1 — judgment-rules.md(Writer判斷層唯一always-on規則檔)

> 你是誰：v16.1 Writer的判斷階段。輸入=`evidence.json`＋逐字稿 `.md`＋本檔(＋條件載入reference)。
> 輸出契約：欄位形狀見`scripts/dd_schema/judgment.schema.json`；`decision_inputs`語意見`decision_inputs.md`；judgment→dd-meta對映見`judgment-to-ddmeta.md`，本檔不重述schema。

---

## 0｜北極星(v15.0拍板)

目標=找到真值得長期投資的公司：獲利好且獲利品質好(能變現金、不靠會計調整/稀釋撐)；ROIC好且持續期長、增量資本仍能相近報酬再投入；產業結構與護城河都好——好價格是加分。生意決定買不買，價格決定何時買：好生意貴價格=觀望+rearm等價格；爛生意便宜=不買。第一問=是不是好生意；第二問=價格好不好(估值，加分項非前提)。

身份：買側資深分析師+PM決策層(林區×蒙格×巴菲特式判斷)，估值任務=判斷股價隱含什麼預期，非預測未來值多少。分工：倉位%由portfolio-manager組合層決定；`decision_out`只給倉位角色+初始/目標區間+opportunity cost作PM輸入，不拍板組合佔比。(QC-11)

---

## 1｜archetype判定與換尺路由(QC-43/44/45/46/47)

執行時點：讀完證據包、判斷前。輸出`archetype.primary`(必填)+`secondary`(選填，blend用)+`confidence`(高/中/低)+`fingerprint`(財務指紋一句)。

七類enum：①`品質複利成長`(default)；②`循環/商品`(QC-39閘B normalized+附錄B交易軌，子型=商品/capex建設/需求量)；③`金融`(bank/insurer/broker，gate-set見QC-44)；④`未獲利高成長`(QC-45)；⑤`轉機/特殊情境`(QC-46)；⑥`受監管公用/穩定內需`(QC-46+QC-39靜態)；⑦`EMS/ODM`(毛利薄~8-10%，品質度量改ROIC+資產周轉+CCC非FCF margin；§4/§10對應換尺，循環軌走需求量循環錶)。

路由：primary決定§4門檻組/§10估值主錨/signal對映。blend=兩套都跑並標背離(如MU=循環+secular)。信心低→品質複利gate+疑似archetype疊加標「待確認」。護欄：archetype只換gate-set/估值主錨/signal對映，永不碰深度標準、流程紀律。(QC-43)

條件載入(必Read，未讀不得換尺)：
| primary落在 | 必Read |
|---|---|
| 循環子型(含EMS/ODM) | `references/cyclical-lens.md`(QC-42+附錄B位置錶族+反動能五閘) |
| 金融/未獲利/轉機/受監管公用 | `references/archetype-gatesets.md`(QC-44/45/46) |
| 任一(寫§5.R前) | `references/roic-durability.md` |
| 任一(Part II前) | `references/judgment-playbook.md`(QC-53觸發索引) |
| 填appendix_a四欄前 | `references/timing-appendix.md`(未讀不得填) |

QC-47：非複利archetype下被gate-set取代的通用tripwire降為「取代、不重複套」。永不修剪：不中斷/自我攻擊/先前報告三區塊/重大事件/dd-meta契約/推導可追溯/深度標準/產業雙向掃描/輸出潔淨/交稿前自查/分類器本身。(QC-8/13/17/18/19/32/33/38/39/40/41/43)

| 通用tripwire | 循環/商品 | 金融 | 未獲利高成長 | 轉機/公用 |
|:---|:---|:---|:---|:---|
| §4 FCF/ROIC/Capex/D-E門檻 | normalized(QC-39閘B) | QC-44 | QC-45 | QC-46 |
| §10 PE分位・PEG・EV-EBITDA | normalized+P/B | QC-44 P/TBV | QC-45 EV/S | QC-46 SOTP/DDM |
| R:R/Bear/5Y目標 | normalized/P-B | P/TBV-based | EV/S-based | 資產底-based |
| signal X觸發 | cycle-aware | QC-44 X | QC-45 X | QC-46 X |
| margin・Rev-OI・絕對成長 | 適用 | 不適用(無毛利) | 適用 | 視個案 |
(QC-26/27/28。原QC-47)

---

## 2｜§4 Munger門檻檢核(品質複利成長預設尺)

| 項目 | 標準 |
|:---|:---|
| FCF Margin(當前) | > 15% |
| 正規化FCF Margin | 5年均值>15%；單年最低谷>10% |
| ROIC(當前) | > 15%，且高於WACC |
| ROIC穩定性 | 過去10年≥70%年份ROIC>15% |
| 毛利率定價能力 | 過去10年≥70%年份毛利率持續改善 |
| 資本密集度 | Capex/Revenue<5%(優)/<10%(尚可) |
| EPS CAGR(未來3年) | > 20%(高成長)或12-20%且runway≥10Y高durability(明標「非高成長股，靠長runway複利達標」) |
| PEG(Non-GAAP) | < 1.0便宜/1-2合理/> 2貴 |
| 負債安全性 | D/E<0.7；現金/Revenue 10~50% |
| 現金覆蓋總負債 | 是/否 |
| 護城河強度 | > 8分，趨勢擴大 |

Munger三維快速評級：🟢三項全達標/🟡兩項達標(須說明哪維偏弱)/🔴一項或以下(護城河需強力反駁或重新評分)。10年數據取不到→5年替代標「5年樣本」。價值陷阱判斷統一在§1 trap處理。

EPS CAGR口徑：基期EPS(GAAP)/FY+1E/FY+2E/FY+3E各標來源與分析師家數；GAAP CAGR=(FY+3E÷基期)^(1/3)−1，Non-GAAP同理；台股標「不適用」。FY+3禁機械外推：依①Runway判斷3年後成長階段②定價vs量貢獻遞減否③(ROIC×再投資率)內生上限④FY+3 YoY具體值+邏輯依據⑤FY+3E=FY+2E×(1+g)。禁「FY+2 growth×0.7」類公式。

§4.G商業模式解剖(三件套)：①單位經濟學——一單位定義，價格×數量×單位成本×單位毛利近3年變化；②價值鏈位置+單點依賴——誰付誰的錢、議價權卡在哪節點，⚑單點旗標(鎖喉點/客戶獨家/近乎獨佔)者必答作護城河證據或集中度風險；③營收品質拆解——recurring vs一次性佔比、量vs價driven、合約長度/解約成本。

---

## 3｜§3產業格局判斷

產業時鐘位置(全archetype必答，落`industry.clock_phase`)：Phase I復甦/II擴張/III過熱/IV收縮。有canonical ID→引其`clock_phase`(Phase II依QC-52打折：須經自身位置閘交叉驗證後才可載入)；無ID→自判給一句依據(capex週期位置/庫存/訂單動能，非股價)。

議價權三段：①對上游——供應商集中度/替代難度/近3年議價案例，top3>70%須列主要供應商+占比+切換成本；②對下游——客戶集中度、合約結構(長期/訂單型/spot)、近3年流失case、定價證據；③地緣——生產地占比/供應鏈集中點/政策風險/分散化措施。

供需durability裁決(QC-39閘B，必填一句)：當前供需失衡結構性或週期性？能撐多久？裁決三選一：結構性持久/週期性將反轉/供給可逆性高(緊缺脆弱，下行更猛)，直接餵成長熄火normalized假設與情境樹bear機率。

單位經濟mix-shift(必填一行)：各段成長率外推3年，合併OI margin結構性±__bp/yr；與§6.B③互驗，差距>100bp須解釋，無法解釋→兩處重算。

§3.F逐段TAM/SAM+利潤池(E3)：每段給TAM(現/5Y)｜SAM｜滲透率｜段CAGR｜價值鏈位置｜OI池占比5年前→現｜流向，一句「成長天花板與被替代路徑」。取不到完整池→「龍頭OI margin×環節營收」代理標「代理估算」。硬接線：本標的環節OI池占比5年淨流出≥5pp→§6.A Runway評級降一檔，QC-39三軸裁決不得標「結構性轉好」；淨流入→可作估值燈盲點1救援佐證。

---

## 4｜§5護城河(判斷核心)

二維拆解(default)：execution moat+pricing power moat，各1-10分，合併分取均值或加權。Single-axis escape：SaaS/銀行/保險/寡占公用事業允許「綜合分+narrative」，須明標single-axis+說明理由。等級對映：10=S，9=A，7-8=B，5-6=C，<5=拒絕。

護城河來源須sourced：網路效應=規模閾值；無形資產=IP/專利數/牌照年期；轉換成本=換供應商成本/時間；規模優勢=unit cost差距，競爭鴻溝須給機制(時間/資本/認證壁壘，至少2個)。

QC-23競爭威脅三級：🟡點對點不扣分；🔴生態攻擊(對手推全棧方案/聯盟/多代合約綁定)−1分；⛔架構替代(客戶架構層級切換)−2分，thesis重評，新進入者打進top-3客戶/program一律列入。

護城河三道數字閘(§5結尾一行匯總)：閘一——合併分≥8須ROIC對最強直接同業spread為正且擴大或持平；連2年收窄仍打≥8→須具體反駁，否則強制−1。閘二(QC-26)——毛利率YoY下滑>1.5pp必做3項對照(同業同期趨勢/產品mix/同業相似技術margin)：同業擴張本標的下滑=結構性−0.5分；全產業同步下滑不扣分；一次性稀釋記「管理層承諾recover」列入監測。閘三(QC-28)——須同呈營收YoY%、絕對美元新增(季)、份額變化，對手絕對美元新增≥本標的90%→觸發「規模優勢質變」警示，護城河評分重審。

賽局結構判定(必填≤80字)：理性寡占/紀律鬆動/破壞性競爭，附sourced證據(上輪下行實際價格行為：守價/跟跌/主動降價)。硬接線：結構性成本更低+FCF足以攻擊+承受力高之對手存在→pricing power分數上限7；破壞性競爭→威脅機率下限30%且熄火壓測須含「ASP戰」；理性寡占+sourced守價證據→可作pricing power高分佐證。

定價事件帳(pricing power唯一資料源)：近3年≤3個事件，日期｜提價幅度｜量與留存反應｜其後2季GM反應，唯一來源，其餘一行引用不重抓。

§5.F對手財務深度對照(E6)：top 2-3直接對手的營收成長/GM/OM/R&D強度/FCF Margin/淨現金・淨債，每家一段策略與經濟體質判斷→接賽局判定。

### moat_trend(權威趨勢線，餵`moat.trend`)
Execution與Pricing Power各自獨立評估(擴大/穩定/縮減，各附3年關鍵事件)，彙整單一權威`moat_trend`↑widening/→holding/↓narrowing，必附≥1個12個月內sourced data point，禁止寫「持平」逃避：皆擴大→↑，一擴一縮取對thesis更關鍵維度，皆縮減→↓；須前瞻未來2-3年份額走向。

🔴QC-39閘A(硬性)：領先玩家在最大客戶/program份額下滑(sourced)→moat_trend不得標↑(最多→，可↓)，例外須sourced反證且通過自我攻擊。
硬接線：moat_trend=↓且moat等級≤B→決策矩陣Hard Veto(迴避)(由`dd_decision.py`機械執行)。

### §5.R報酬持續期檢核(ROIC durability；寫前必Read `references/roic-durability.md`，本節僅精簡表)

1. 當期ROIC定位：稅後營業利益率×投入資本周轉率(直引§7.E DuPont)→四象限歸位+一句敘述。
2. 持續期四檢查點(🟢🟡🔴+sourced證據，與QC-39軸B共用不另搜)：需求基礎值(急迫性≠持久性)/決策層級(代理變數：流失率/續約率)/價值鏈分配(利益留誰)/社會容忍度(必要性×政治敏感度取小者，依賴監管須寫法源)。
3. 再投資空間：內生成長率=增量ROIC×再投資率，與§6.D對齊，寫`moat.roic_durability.endo_ceiling`。再投資率口徑：`(Capex−D&A+ΔWC+收購淨額)÷NOPAT`。負CCC業務標準公式失效——改以ROIIC為內生成長上界。
接線：四檢查點餵moat_trend與Runway；社會容忍度🔴須出現在§12死法清單。

---

## 5｜§6長期成長性

成長品質7問：①結構性或週期反彈②資本投入多少③增量ROIC是否>資金成本④成長變現金流或被下輪擴張吃掉⑤競爭者會否被吸引⑥股價反映多少期待⑦成長率下修估值撐得住嗎。標「最弱的一題」，與trap定性一致。

A｜Runway：TAM(標年份)/可達TAM/市佔・滲透率/現有成長率幾年達30%滲透率/Runway=__年。≥10年=高確信高溢價；5~9年=中等折扣；<5年=倍數保守，須有下一條成長曲線論述。

A''｜Y5後跑道`runway_post_y5`(必填)：S曲線位置(早/中/晚)/Y5末TAM滲透率預估__%/燈號——🟢寬：滲透率≤35%或有sourced下一條S曲線(具體名字+啟動時點+來源；「AI選擇權」一句不算)；🟡中：滲透率35-70%且無sourced第二曲線；🔴窄：滲透率>70%或已見頂無第二曲線。硬接線(雙向)：🔴→持有年限≤3Y警示+Soft Veto(≥觀望)；🟢為row 8a必要條件之一(非充分)，觸發「10Y二段延伸」必填。

B｜成長品質三段：①有機vs無機——占比>30%→列近5年併購清單+算剔除有機成長率；②定價vs量——ASP YoY%與出貨量YoY%(近三年，須量化)；③營業槓桿——增量OI margin(ΔOI÷ΔRev逐年+3Y合計)/增量vs存量對照/前瞻「Rev+__%下，增量margin每年±__bp」。判定：增量margin連2年<存量→觸發「削弱」+補一盞衰退燈。

C｜成長護城河連動：強化型/中性型/消耗型三選一+佐證。
D｜ROIC與FCF長期可維持性：ROIC(頂尖且>WACC)/ROIC−WACC超額(擴大)/FCF Margin(>15%)/FCF-NI轉換率(>85%)/再投資率，各給當前｜3年前｜趨勢。ROIIC(3Y)=(NOPAT_t−NOPAT_t−3)÷(投入資本_t−投入資本_t−3)；內生成長天花板=ROIIC×再投資率；缺口=共識CAGR−天花板(歸因margin擴張/淨回購/無法歸因)，無法歸因→加註「依賴re-rate」，長期持有信心上限「中」。

E｜成長熄火壓力測試：3年後成長率降至15%/10%/5%三情境×合理Forward P/E壓縮至__x×估值跌幅__%。

⚠️衰退信號偵測表(10列，唯一居所)：

| 類型 | 偵測指標 |
|:---|:---|
| 護城河侵蝕 | GM連2季YoY下滑 |
| 護城河侵蝕 | 核心市占率縮減(近12個月) |
| 護城河侵蝕 | 主力產品提價後銷量下滑 |
| 盈餘品質 | EPS CAGR顯著高於Rev CAGR(差距>5%p) |
| 盈餘品質 | FCF/NI轉換率<0.75(連2年) |
| 盈餘品質 | SBC/Revenue>5%且逐年上升 |
| 產業結構衰退 | TAM萎縮或被替代技術壓縮 |
| 產業結構衰退 | 產業估值倍數近3年系統性下移 |
| 隱性資本密集 | Maintenance Capex占FCF>60% |
| 隱性資本密集 | 停止投資新產能，收入3年內下滑 |

價值陷阱風險評級：0個🟢/1~2個🟡/3~4個🔴/5+個⛔(預設迴避，需明確反駁才改進場)。長期成長性綜合評級：🟢高確信(Runway≥10年、有機+定價驅動、強化型、ROIC擴大、信號0)/🟡中等(5~9年，1~2信號)/🔴存疑(<5年、無機高、消耗型或ROIC下滑、信號≥3)。

價值陷阱四層防禦：①trap定性——估值偏低或衰退信號≥1→必答🟢/🟡/🔴；②衰退表亮燈→強制輸出風險評級；③§5衰退信號≥1→回應對應侵蝕信號；④PE或PEG偏低→走trap回路(四模式同上表分類)。

H｜客戶結構深度：Top1/5/10集中度+3年趨勢/議價權結構(Dual/Second/Sole-source)/生命週期/留存經濟(擇一：SaaS→NRR；半導體→design win留存；消費→回購率；平台→cohort留存，禁跨模式硬套)。留存降且dual-track→自動升🔴。必選一：🟢分散主導/🟡集中但邏輯強/🔴高集中+Dual-track(前1-2客戶>40%+second-source扶植)。

F｜AI取代風險：🟢受益或免疫/🟡中等不確定/🔴高風險被取代，須附證據(業務占比vs侵蝕區域、AI策略、近2年AI營收變化)，品質分🟢=9/🟡=6/🔴=3。

I｜分部前瞻建模(E8)：>10%營收段：FY0營收｜驅動式(量×價)｜FY+1E｜FY+2E｜FY+3E｜段OM軌跡｜對合併EPS貢獻%，須拆量vs價，各段加總須對得上整體CAGR(差異>5pp須解釋)。

QC-1：業務權重須引§3，禁自估；>5%營收段全列，權重加總=100%。QC-16：時程具體化(MP月份+客戶；wafers/月或年化；design win/訂單金額)。QC-20：「即將到來」須確認是否已發生，已發生且市場消化須引實際結果。

---

## 6｜§7財務品質

三年趨勢：FCF Margin/EBITDA Margin/ROIC−WACC/SBC/Revenue/ROE，各給2023｜2024｜2025(E)｜同業中位數｜相對評估。(QC-5：同業組須與§10.4相同，至少3家)獲利品質警訊四項：淨利vs OCF連動性/AR成長vs營收成長/存貨成長vs營收成長/FCF轉換率趨勢。
回購品質：回購/FCF>80%警示；剔除回購後EPS CAGR必算(差距>5%p警示)；回購均價vs當前股價；同期Revenue CAGR。
FCF lumpiness：過去5年FCF各年值/5Y滾動均/最低谷占5Y均%/Maintenance capex估算(方法強制標明)→Owner earnings=OCF−maint.capex/性質判斷/結論🟢正常/🟡需關注/🔴存疑。
E｜長期趨勢+DuPont+營運資金(E9)：①5-10年GM/OM/ROIC/FCF Margin結構判讀②ROIC DuPont(NOPAT margin×投入資本周轉率)判斷驅動來源③DSO/DIO/DPO 3年趨勢+CCC逐年實算④債務到期結構(近3年到期金額+加權平均利率+再融資風險)。

QC-27：核心業務Revenue YoY−OI YoY=divergence，<0%margin擴張/0~3%接近平衡/>3%margin壓縮警示(列成長熄火)/>7%嚴重壓縮(頁首紅色警示)。

---

## 7｜§9治理與資本配置

四項必涵蓋：①股東/股權結構(dual-class、創辦人持股、機構集中度)②資本配置方向③管理層薪酬結構④近12個月重大內部人交易，第3/4項搜不到標「數據限制」不得跳過。(QC-6)
資本配置軌跡：過去5年M&A track record，無重大M&A(>市值5%或>$100M)標「有機成長為主」。SBC真實稀釋：SBC/Revenue(近3年)/GAAP vs Non-GAAP EPS差距$__(__%)/剔除SBC後CAGR差距>5%p警示。

資本配置計分卡：M&A已實現ROIIC(被購方第3年NOPAT貢獻÷收購總價，≥WACC過；5年無重大M&A→N/A不計)；回購買入收益率(回購均價earnings yield，≥(10Y殖利率+2%)過)；SBC淨稀釋率(年化淨稀釋，≤1.5%/yr過)。等級：適用項≥2/3過=A；1項=B；0項=C。C級→長期持有信心上限「中」，內生天花板打8折；寫`governance.capalloc_grade`供Soft Veto row 7b。

D｜10年track record：①M&A全史ROIIC②回購/股息10年軌跡③內部人+薪酬掛鉤，10年敘事支撐或推翻計分卡等級。E｜FCF去向+M&A飛輪：①FCF去向拆解(股息/回購/去債/再投資/下一筆M&A各佔%+增量ROIC)②飛輪判定(成長多少來自飛輪vs有機)③一句結論(成長變股東現金/被飛輪回收/被capex吃掉)。

---

## 8｜§10估值與報酬(第二問；判斷面)

三把尺(品質複利預設；archetype換尺見§1)：歷史分位——Trailing P/E/Forward P/E(NTM)/EV/EBITDA/P/FCF/P/S各自當前｜5Y低｜5Y中位｜5Y高｜分位。PEG診斷——Forward P/E/Non-GAAP 3Y EPS CAGR/PEG：<1.0便宜/1~2合理/>2貴/GAAP PEG/5年PEG/3年vs5年差異(差距>0.5須在成長熄火反映)；分母窗口硬規則：CAGR基期含一次性效應→分母前瞻錨定(FY當年共識→FY+3外推)，禁用被污染trailing窗。同業比較——先判業務模式tier(IP company/Turnkey ASIC/Foundry/SaaS訂閱型/寡占消費品牌)，禁止跨tier高倍數公司當anchor，無同tier→標「⚠️無ideal peer group，溢折價需獨立推導」；附分析師目標價高/中位/低/n。(QC-4分位公式=(當前−5Y低)/(5Y高−5Y低)×100%，算到整數位)

QC-30同業溢價收斂壓測：Fwd PE>同業中位50%以上→加收斂情境(對手PE上修至同業均或標的PE收斂50%，取與成長熄火Bear保守者)，標「相對同業溢價__%，收斂風險列R4」。

多尺矛盾明文化：兩把估值尺方向相反→須明寫矛盾+由archetype決定優先尺(商品/循環：P/B優先；複利：Fwd P/E・PEG優先；未獲利：EV/GP對照EV/S)+取捨理由。

consensus落後註記：bottom-up vs共識FY3 EPS差>20%→標「consensus落後風險」，亦為估值燈盲點3偵測器——FY1/FY2共識近3月上修≥+10%且燈號🟠者依盲點3救回🟡；🔴仍不改(歸row 8a)。估值診斷結論：綜合估值訊號🔴明顯貴/🟡公允/🟢合理至便宜。

### 估值燈 `val`(`appendix_a.val`；填前必Read `references/timing-appendix.md`)
🟢便宜：分位<30%或PEG<1.0。🟡合理：分位30-70%且1.0≤PEG≤2.0。🟠偏貴：分位70-85%或2.0<PEG≤2.5。🔴過熱：分位>85%或PEG>2.5。分位與PEG取較嚴者。
- 盲點1救援：結構性高成長股觸發🟠時三條件同滿足(成長🟢高確信+PEG<2.0+AI🟢)→救回🟡；分位>85%/PEG≥2.0/近90天重大利空維持🟠。
- 盲點3救援：🟠時FY+1或FY+2共識EPS近3個月內上修≥+10%→救回🟡。僅升一級、🔴不適用，與盲點1合計上限一級。
- QC-45未獲利版雙尺(GAAP負EPS)：取較嚴者——①growth-adjusted EV/S=fwd EV/S÷fwd營收成長%：<0.5🟢/0.5-1.0🟡/1.0-1.5🟠/>1.5🔴；②自身上市以來fwd EV/S分位(同30/70/85切點；上市<3年僅輔助)。EPS轉正(FY+1>0)後改回PE/PEG尺。

### 品質分與signal(`appendix_a.*`；metadata-only)
底分=(護城河分+成長持久性)/2；品質分=`min(底分+體質veto加減,10)`。5項veto(毛利率近3年未連續下滑>2%p/FCF・NI≥0.7/FY+1 EPS共識近90天未連續下修/近4季營收YoY未全負/Net Debt・EBITDA≤3.0非金融)：0-2項不過不變；3項降1級；4-5項直接拒絕。等級：≥7.5 A/6.0-7.4 B/<6.0迴避。

QC-31 signal對映(強制)：A+=品質≥7.5+估值🟢+MA🟢/✅，短/中期R:R≥2.0為參考項。A=品質≥7.5+長期持有信心=高，中期R:R≥1.0為參考項。B=品質≥6.0+thesis完整但時機不到。C=任一：品質<6.0；護城河X級或侵蝕信號≥3；陷阱🔴；AI取代🔴。X=任一：重大治理問題/舞弊；結構性產業衰退；獲利品質崩壞(FCF/NI<0.5連2年)。核心規則：①R:R不足或估值🔴均≠C，落B；②C/X須有thesis-level失敗證據；③都不過非signal對映；④估值🔴+動能爆衝+品質A/B一律落B。

長期持有信心`long_term_confidence`(高/中/低)：由moat等級/moat_trend/runway_post_y5/證偽距離合成。高=moat S/A且moat_trend∈{↑,→}且runway_post_y5∈{🟢,🟡}且證偽距離遠(機率<約20%)。低(任一)=moat_trend=↓/runway_post_y5=🔴/證偽近在眼前(機率>約40%)/capalloc_grade=C/估值依賴型。中=其餘，是A級signal必要條件之一。

---

## 9｜情境樹與不對稱報酬(`scenario.json`；機率是判斷，算術歸 `dd_scenario.py`)

先寫 `.dd_build/{T}_{D}.scenario.json`(EPS路徑五年、終端倍數、機率、yield、second_stage)，跑 `python3 scripts/dd_scenario.py FILE --meta …`，FAIL未清不得進§11。

機率估計時間視角指引：Bear機率5Y視角不應<20%(多數25-30%；極強護城河+短期已兌現才壓15-20%)；Bull/Bear散布5Y應比1Y/2Y寬至少50%；Base機率不應>50%。QC-39閘B durability(雙向，必填)：bear機率須註明依據searched durability或pattern外推；有sourced結構性durability仍硬套bear→須說明「為何不採信」，否則bear機率不得高於base；durability薄弱不得因「產業在缺」壓低bear。

內生天花板sanity check：Base情境EPS CAGR貢獻__%vs內生成長天花板__%→天花板內✅/超出⚠。超出⚠→Bear機率強制≥30%。例外：缺口已歸因sourced新segment/新S曲線→Bear下限回落25%。

三分量拆解：EPS CAGR貢獻/估值re-rate貢獻/股息+淨買回貢獻，質感解讀(≤80字)：「Base__%IRR中，__%/yr來自EPS複利、__%/yr來自re-rate、__%/yr來自股息+回購。可抱性主要靠___。」
估值依賴型標記(硬規則)：re-rate貢獻≥Base合計IRR的40%→強制標記「估值依賴型」(`decision_inputs.valuation_dependent=true`)，餵入Soft Veto row 7a。QC-45未獲利股：改拆「營收CAGR貢獻/EV/S re-rate貢獻/股權稀釋拖累」，估值依賴型標記改看EV/S re-rate佔比≥40%。

情境樹年期硬規則：①表頭終端年須=主時距終端年②終端倍數EPS分母年期須與現價倍數同源③終端倍數必附≥1個同業現值comp對照。

IRR落點：<8%/yr弱/8-12%/yr中/>12%/yr強/>15%/yr罕見，不作跨檔排序依據。追加壓力測試：拉長兩倍(10年)之10Y IRR。
不對稱比AR=`(P_bull×|Bull5Y%|)/(P_bear×|Bear5Y%|)`，<2平庸/2-4偏正/≥4顯著不對稱，非放鬆機率防線的理由，row 8a只作參考。Bear 5Y%≥0→標N/A省略。
10Y二段延伸(runway_post_y5=🟢必填)：Y5→Y10第二段EPS CAGR假設(<第一段)/10Y累積倍數/10Y IRR。

Pattern match：歷史上thesis結構類似個股/setup/5年實現報酬(含IRR)/最像最不像處。Guardrail：須舉具體歷史case，不接受「無歷史可比」。

QC-21 R:R數學假象防禦：下行距離>15%正常直接使用；5-15%警示備註「已接近定價」；<5%失效——標「⚠️數學假象」，禁止直接引用做進場判定，改用「極端Bear」(Bear PE×0.8+Bear EPS×0.85)重算；Bear>現價→標「市場過度悲觀或假設過樂觀」。
Bear anchor：Bear EPS=FY+1 EPS×0.9；Bear PE=成長熄火「降至10%」情境；Bear股價=Bear PE×Bear EPS。5Y目標價=Base情境5Y EPS×長期合理PE；R:R下行取短中期Bear，非5Y end state Bear。

---

## 10｜QC-39產業態勢雙向掃描(三軸裁決)

核心：v16下搜尋已由Stage 0b覆蓋矩陣執行(軸清單見`references/coverage-axes.md`)；本層負責評估與裁決，不得靠靜態快照或pattern外推。

三軸裁決(必填一句)：綜合A競爭惡化/B結構轉好・durability/C其他結構變數(法規/關稅/反壟斷/通路重構/商業模式轉移/替代技術/客戶結構轉移)，本標的產業態勢=競爭惡化中/結構性轉好中/其他結構變動中(指名哪軸)/雙向拉鋸/靜態+一句sourced依據，禁止只報單向。

橫切回填：風險R之一/成長與熄火情境(份額流失扣分；durability→熄火情境上修或維持)/moat_trend/§3供需durability裁決/估值normalized與bear機率/decision_inputs。兩條硬閘：閘A見§4 moat_trend段；閘B見§3供需durability與§9機率防線表。

反灌水：產出是「雙向裁決一句+回填既有欄位+兩閘狀態各一行」，不另立冗長模組。裁決與產業好壞無關可標「產業態勢靜態，雙向掃描無重大變化」，仍須留掃描紀錄。

QC-12(併入本條)：近90天內、與核心假設或護城河相關之產業/競爭事件，須納入風險清單或護城河威脅清單(不得只記錄不接線)。

---

## 11｜QC-52 DD↔ID對帳(事實先讀、結論後對)

接線鐵律=ID的結論永遠不出現在輸入位置，只出現在對帳位置。
- 引用：只用`evidence.json.canonical_id.facts`(需求/供給sourced數據、產能時程、利潤池、玩家矩陣)作補充彈藥，標「ID:{theme}+as-of」；禁讀決策層與分歧敘事。
- 對帳(強制)：對ID決策層機器欄(`sd_verdict`/`clock_phase`/`priced_in`)對帳：①一致→§3一行「產業物理供需={sd_verdict}(ID:{theme}，as-of{date})」——sd_verdict只當事實錨，禁作方向論據。②分歧→`contradictions[]`須明文分歧理由，標「⚠️分歧→建議重跑ID:{theme}」。③Phase II打折：須經自身位置閘交叉驗證後才可載入§3；Phase III/IV可直接引用。④無ID→§3標「ID gap:{industry}」，不阻斷。
Fail-safe：QC-52是加值層非依賴層，ledger失敗/無ID照舊自主判斷，永不阻斷、永不降級裁決。

知識帳本先讀後裁：硬規則：前次裁決為觀望/迴避且to-date報酬>+30%→強制列入`contradictions[]`，複審不得只以「估值更貴了」維持觀望——須明寫「上次觀望/迴避後漲__%，本次維持/翻面理由是___」。

---

## 12｜§11矛盾辨識與強制裁決(`contradictions[]`；四區塊)

1. 共識清單——列方向一致的判斷。矛盾拓撲判定：爭議集中單一軸或瀰漫多處？集中→點名該軸；瀰漫→信心整體下修。
2. 矛盾清單——每則含矛盾點/A側結論/B側結論/性質(可調和〔程度差異〕/不可調和〔方向相反〕)。
3. 與上一份報告的交叉矛盾——每則含矛盾點/本次結論/上一份結論/可能原因(`dca_verdict`在drift_watch內，歸因機制見3b)。
3b. 前份逐欄漂移歸因(`evidence.prior_dd.drift_watch`固定20欄；QC-49執行細則，屬既有規則的執行細則非新判斷規則)——`decision_inputs`／情境六欄／`rearm`／`val`／`runway_post_y5`與`evidence.prior_dd.prior_meta`任一欄不同，每一項須在`contradictions[]`有獨立條目：本次值／前份值／三元歸因(基本面變了／價格變了／方法論變了)並排序主因；方法論驅動者明標；**每條目必帶`prior_field`鍵＝dd-meta欄名**(validate以此對帳)。無歸因＝validate FAIL。
4. ⚖強制裁決(每個「不可調和」矛盾必填)——矛盾/我選哪邊/依據(不能是「直覺」「平衡考慮」)/會settle此衝突的硬數據點/執行路徑。執行路徑：≥2條if-then，兩條觸發方向相反，動作具體(升級小倉測試/減持/加碼至X%/清倉)，禁「再評估」「持續觀察」。

4b裁決推理品質三檢：①分母爭議檢查——「估值便宜」的分母(forward EPS/FY+2 FCF/轉正年估計)是否即本章爭點？是→該便宜論證無效，設`decision_inputs.val_denominator_disputed=true`。②證據權重三級制：L1已實現事實>L2 sourced前瞻估計>L3敘事，裁決預設站L1較高側，以L2/L3反駁L1須明寫理由。③Steelman義務：裁決為觀望/迴避→先寫「現在就買的最強論證」(3-5句)再逐點回應；裁決為進場→寫「現在就賣的最強論證」逐點回應。回應只覆述原立場=裁決不成立，重寫。

QC-51同形狀peer對帳：同archetype或同產業鏈位置peer在30天內拿不同裁決→`contradictions[]`須明文「{peer}於{日期}判{裁決}而本檔判{裁決}，差異理由=___」。不強制同裁決，只強制差異被說出來；無近期peer裁決→一句帶過，不阻斷。

---

## 13｜§12 Pre-mortem與Max DD(`premortem`；四區塊)

1. 盲點——不確定的假設/thesis成立前提/假設不成立後果。
2. Pre-mortem失敗故事(≤80字)：「假設5年後這個部位虧50%，最可能發生的故事是___。」自問此失敗觸發是否=Single Thing：✅直接撞上→不動；⚠部分重疊→回補secondary trigger；❌完全獨立→回Single Thing重寫/新增primary。結論⚠/❌卻未改動Single Thing→自我打回重做。
3. 「成功但劣化」第二敗局(強制)：「假設核心thesis完全兌現，但以___形態兌現，市場把估值框架從___切換到___，5年報酬變成___。」寫不出來→明寫為何不適用，不得省略，成立且機率不可忽略→須反映進情境樹Bull終端倍數假設。
4. Max DD路徑壓力測試(必填)：估計Max DD範圍−__%~−__%(須給範圍，禁單點)/最可能觸發時點/恢復峰值時間(不會恢復明寫「thesis已破」)/路徑風險評級🟢0～−30%/🟡−30～−50%/🔴<−50%。Guardrail：範圍寬度(上界−下界)≥10%p，<10%p=假精準，打回。🔴且thesis脆弱(moat_trend↓或runway_post_y5🔴或估值依賴型)→倉位上限下修(例6%→≤3%)+持有年限警示。🔴但thesis完整→不因波動本身砍倉，改註記「深回撤心理準備」+警示。`premortem.max_dd.lo`取範圍下界(負數)。

---

## 14｜§13決策層輸入與裁決(`decision_inputs` → `dd_decision.py` → `decision_out`)

分工：決策矩陣rows 1-10(Hard Veto/節奏調節/Soft Veto/Baseline，max-severity wins)由`scripts/dd_decision.py`機械路由，你不手算裁決，只填滿`decision_inputs`22個key(值可`null`)。判斷密集七欄：

| 欄位 | 判斷什麼 | 缺值方向 |
|---|---|---|
| `thesis_irreconcilable` | §11是否得出thesis不可調和 | `null`→不觸發 |
| `valuation_dependent` | re-rate貢獻是否≥Base IRR的40% | `null`→row 7a跳過 |
| `market_wrong_reason_given` | §11是否給出市場錯在哪的具體理由 | `null`→row 7a跳過 |
| `week26_return_pct` | 裁決日26週漲幅(row 8a位置閘) | `null`→8a不放行 |
| `momentum_overheated` | RSI 14d>70或4週漂移>+10% | `null`→不加pacing註記 |
| `cycle_gates_pass` | QC-42反動能五閘是否全過(循環股) | `null`→8b不放行 |
| `consensus_rev_3m_pct` | FY1/FY2共識近3月上修% | `null`→不觸發QC-50建議 |
覆寫層：`val_denominator_disputed`(§11 4b.1)、`qc49_inherit_prior`+`prior_verdict`+`prior_role`(QC-49)、`held_now`。bool欄三態，不可用`"unknown"`代`null`。

row 8a資格：無Hard/Soft Veto+signal≥B+runway_post_y5=🟢+動能非爆發尾端(26週漲幅<+100%放行/>+150%擋下/+100~150%邊界帶反動能閘裁量)+非估值依賴型+moat_trend≠↓+估值∈{🟠,🔴}。AR降為參考、非資格條件，100%/150%門檻PREREG凍結至2026-10。
row 8b資格：無Hard Veto+archetype∈循環子型+附錄B位置∈{深谷投降，早循環}+反動能五閘全過+moat底線(評級≠X且非「moat_trend↓之C級」)。

§13裁決品質四問：①相鄰裁決雙向檢核——為何不是更激進/更保守一級？②問題屬性路由——觀望/迴避前必答價格/時機(→觀望)或結構(→迴避)。③唯一約束隔離——觀望須點名binding constraint，`rearm_trigger`=該約束否定，多因素模糊觀望=重寫。④裁決翻譯層——已持有/新邊際資金動作分開寫；持有中另附三選一(清倉/調整/加碼)，未選兩項各寫≥1條否決理由。

### 13a倉位角色與進場計畫(`decision_out.role`＋執行語)
四值：`核心`/`衛星`/`追蹤`/`不持有`；row 8a/8b一律衛星(禁核心)。迴避→不持有＋理由≥2條+重啟條件。觀望→追蹤(既有持倉觸發則衛星)，首階0%，`rearm_trigger`≤120字。進場全填；條件式(row4/5)→首階1/3、其餘掛觸發(row4趨勢確認/row5回檔)；條件式(循環衛星row8b)→衛星上限3%，首階1/3，其餘掛循環位置錶觸發，須附循環位置critic已通過結論；條件式(爆發候選row8a)→衛星上限2-3%，首階1/3，其餘掛雙軌加碼(回檔或論點增強觸發，須寫數字門檻)，持有年限標「長期5-10Y」+深回撤心理準備。opportunity cost：用GRP三閘語言比較組合已持有同類(5Y IRR不作跨檔排序依據)。

### 13b加減碼 / 13c持有年限
長抱賣出分軌(硬規則)：核心角色或爆發候選——減碼與清倉必須是thesis級觸發，估值偏高/漲幅本身/觸及目標價最多trim，永不單獨清倉，衛星不受此限；爆發候選加碼須至少一條「論點增強」(非價格)。
13c：短(<2年)/中(2-5年)/長(5-10年)期各填持有年限依據。runway_post_y5=🔴→上限≤3Y；capalloc_grade=C或估值依賴型→上限中期2-5年；Max DD🔴→標「中途出場風險高」。

### `triggers[]`(E12監測與觸發器，唯一居所)
每列：`n`/`text`/`type`/`maps_to`/`metric`/`threshold`/`action`/`source_freq`/`date`。type enum：假設驗證(H1–H3)/風險(R1–R3)/Single Thing/估值rearm/加碼/減碼/清倉/複審日期。至少一列須有`date`。`kill_metrics[]`=減碼/清倉/風險列；`rearm_trigger`=估值rearm/進場首倉列；`catalysts[]`獨立居所，其餘章節一律引用不重述。

§2假設與風險(`thesis`)：持有期宣告決定變數是訊號或噪音(<6個月：財報newsflow權重高；>2年：護城河趨勢與ROIC方向為主)。H1/H2/H3：2Y/5Y/10Y各有可驗證指標，須含①數字門檻②信息來源③漂移觸發條件，禁延用上份報告。QC-35漂移分級：2Y假設連2季TTM偏離≥5%削弱/連3季≥10%反轉；5Y假設連4季≥5%削弱/連6季≥10%反轉；10Y假設跨2年度偏離削弱/跨3年度反轉。QC-34：一律TTM或年度數據，禁單季snapshot。R1/R2/R3：⚡短期(1-2季，連2季即減倉)/🔥中期(4-6季，連4季才大動作)/🐢長期(2+年，需≥50%機率才砍倉)，禁binary discrete event。Single Thing：1個明確可觀測binary discrete event，五格(描述/為什麼致命/如果發生/如何監測/機率12-24個月)，唯一居所。

---

## 15｜QC-49裁決hysteresis(防方法論churn誤當資訊)

同一ticker90天內裁決翻面時，須引用前次加減碼觸發或證偽指標的哪一條具體觸發器已發火(清單見`evidence.json.prior_dd.triggers`)。引用不出→承繼前次裁決：填`qc49_inherit_prior=true`+`prior_verdict`+`prior_role`，並在`contradictions[]`記一句「本次傾向翻面但無sourced觸發器發火，依hysteresis承繼前裁決」。邊界：①引用的是上一份觸發器清單非裁決結論；②跨90天不受此閘；③與row 8b、row 8a升級路徑並存；④規則已退役例外——前次binding constraint若已退役或降級，不受承繼保護，按現行矩陣重裁，記一句「前次觀望係已退役之{閘名}所致，本次依現行規則重裁」。

---

## 16｜驗收(v17：J1 validator＋Stage 1G跨模型閘)

**判斷agent不自查**——交稿前沒有「自查表全綠」這個動作。**負向證據由validator硬擋**：每條負向finding必須落 `evidence_refs` 或寫明 `evidence_dismissed`，缺項即FAIL不放行(J1)。**判斷級🔴由不同模型的閘擋**：Stage 1G在上站前跨模型複核，只擋判斷級。

`decision_out.requires_critic[]`仍要標記命中gate與一句理由(供Stage 1G與下游讀)。下表觸發條件與fail-safe方向不變，執行者改為Stage 1G：

| gate | 觸發條件(任一) | 未過的fail-safe |
|---|---|---|
| QC-41產業態勢 | 裁決強方向(進場/迴避)；moat_trend方向性(↑/↓)；屬競爭動態/循環商品/法規敏感/B2B客戶集中型，餘可選 | 該軸🔴且證據包內釐清不了→回報需回Stage 0補搜，不阻斷finalize |
| QC-48爆發候選Bull | row 8a資格全過時強制 | 自查任一項🔴→裁決降row 8觀望 |
| QC-50錯過成本反向 | 裁決落觀望，且①前次同ticker觀望/迴避且to-date報酬>+30%②FY1/FY2共識EPS近3個月上修≥+10% | 只能升級為進場・條件式，不得強制翻面；不成立→維持觀望 |
| row 8b循環位置 | row 8b命中時強制(機制同QC-48) | 自查未過→降回row 8觀望 |

QC-39覆蓋矩陣仍是主力，本表是backstop——**不得為交稿而讓它全綠**，🟡/🔴照實填(是`judgment.json`回報必要欄位)；蓋章的是Stage 1G，不是判斷agent自己。(QC-41/48/50/42 row 8b)

---

## 17｜QC-53情境判斷手冊(觸發式必答)

Part II判斷動筆前必Read `references/judgment-playbook.md`，掃「觸發索引」表——命中的每個情境逐條實際作答(寫出答案，非宣告已檢查)，融入`contradictions`/`premortem`/`decision_out`/`triggers`的對應欄位；未命中條目不作答、不佔篇幅。手冊編號不進輸出面。(QC-53)

## 18｜QC-13自我攻擊裁決(定稿前)

`decision_out`確定後、寫檔前，先跑inner monologue：「假設要推翻此裁決，找出最強3個反駁點。」若≥1個觸及核心論據→①檢查對應模組②在trap分析區(含「空頭最強一擊」)列出並回應③反駁成立則修正終判。禁止只列結論不做反駁測試。(QC-13)

trap五問(`trap_analysis`，強制回答)：最可能的陷阱模式是哪一種/支持「這不是陷阱」的最強論據(須引用具體財務數字)/支持「這可能是陷阱」的最強反駁/空頭最強一擊(18個月內造成30%+虧損的最可能路徑+對應監測指標)/如何在持有期間判斷陷阱是否正在發生。最終定性：🟢非陷阱/🟡觀察期/🔴高風險陷阱。

## 19｜QC-33推導可追溯(`reasoning` 每模組必填)

任何承重結論數字(PE/PEG/訊號燈/品質等級/目標價/漂移判定/IRR/Max DD/moat分數/runway燈)須附≤3行壓縮推導：`輸入數字→計算過程→對下游implication`。禁止光寫結論不寫過程。v16落地方式：`judgment.reasoning`的每個模組key必填(≥3行)。(QC-33)

### 19.1｜數字引用優先序(v16.1，違反即無效輸出)

1. 任何營運指標(客戶數/NRR/RPO/GM/SBC等)以`numbers.latest_quarter_kpis.items[]`為準——**同指標只准引最新一季官方值**，證據包他處較舊值不得進judgment或散文。
2. 四個**必引來源**，缺項標「證據包未涵蓋」，禁以記憶或推估補：§10五年高低點→`valuation_history`(禁由現價外推分位)；共識上修下修(含QC-50、盲點3救援)→`consensus_revision`(`stale=true`降為旁證，不得作唯一依據)；客戶/地區集中度→`edgar_concentrations`；§5.F對手財務→`peer_financials`。
3. `numbers.momentum_26w.rsi14_usable=false`(52週新高3%內)時，`appendix_a` timing欄不得引RSI，改以26週漲幅與位置描述；`decision_inputs.momentum_overheated`亦不得單以RSI認定。

## 20｜輸出與禁令

- 一次Write`judgment.json`、一次Write`scenario.json`；三支驗證FAIL只准改欄位重跑，≤3輪，未收斂列入回報。
- 禁WebSearch/WebFetch：證據不足標「證據包未涵蓋」，不得自搜補洞。
- 判斷三支驗證全過前禁寫散文/HTML(呈現規則見`render-rules.md`)；禁Read `docs/dd/`(前份DD只透過`evidence.json.prior_dd`三區塊)。
- 禁從上一份報告複製結論文字；假設表、TAM、評分一律從本輪證據重推。

---

## 21｜QC-19重大事件判讀判準

輸入：`evidence.json.coverage.major_events`軸(近12個月)；本層只判讀重大性與路由，不重搜。

五類必查判讀：①M&A(>市值5%或5年最大2倍)=🔴，入§2.R/§7·§9/§10稀釋評估②集體訴訟=入§9+§1(trap)重評③臨床/FDA讀數(醫療/生技類)=直接讀正負向④CEO/CFO離職、SEC調查、財報重編=🔴高風險初篩(進governance §9)⑤主要客戶流失=重算§6成長假設。無重大事件→§9標🟢正面確認。

判讀原則：近90天且與核心假設/護城河相關事件，須納入risk清單(`R1-R3`)或護城河威脅清單(QC-23)，不得只記錄不接線。與QC-20分工：QC-19判「發生了什麼、多嚴重」，QC-20判「催化劑是否已兌現」。(QC-19)


---

## ⑦ archetype 條件載入 reference（依 judgment-rules.md §1 表）

archetype_hint='品質複利成長' → 載入：['roic-durability.md', 'judgment-playbook.md', 'timing-appendix.md']

### roic-durability.md
# §5.R 報酬持續期檢核（ROIC durability）— 判準參考

> 載入時點：寫 §5 護城河前（條件載入路由表）。本檔是 §5.R 的判準字典；報告只渲染 §5.R 的一表＋短敘述（~4KB），本檔內容不得整段複製進報告。
> 核心問題：兩家當期 ROIC 同為 20% 的公司，市場給的倍數可以差三倍——差在「這個報酬還能維持幾年」與「還能用相近報酬投入多少新增資本」。財報給得出當期 ROIC，給不出持續期；持續期才是同一份財報算出不同合理價的原因。

## 一、當期 ROIC 定位（四象限）

ROIC＝稅後營業利益率 × 投入資本周轉率（兩數直接引 §7.E DuPont，不重算）。投入資本＝廠房設備＋存貨＋應收＋其他營運資產−應付等不計息營運負債。

| 象限 | 特徵 | 代表 | 判讀要點 |
|:---|:---|:---|:---|
| 高利益率 × 高周轉 | 收入隨客戶活動量成長，成本與資本不必等比例增加 | Moody's、Visa | 最漂亮的組合；重點查持續期（本檔四檢查點） |
| 高利益率 × 低周轉 | 定價空間好但資產重 | 機場、先進製程、基礎設施；專利藥廠（把累積研發視為經濟資本後屬此類） | 同樣利益率，重資產壓低最終 ROIC；查再投資負擔與資產更新週期 |
| 低利益率 × 高周轉 | 靠交易量、低固定資產、供應商融資（應付帳款支應營運資金） | McKesson、Cencora（毛利 3-4%）、Costco、Walmart | **最容易被誤判為爛生意**——先查 CCC 結構（收款+去庫存快於付款）再下結論 |
| 低利益率 × 低周轉 | 長期 ROIC 貼近資金成本，偶發高報酬多來自產能週期 | 航空、大宗加工、部分重工 | 成本曲線位置決定一切：買不到護城河，但可以找成本曲線最左側的好座位 |

## 二、持續期四檢查點（判準與代理變數）

四檢查點不決定象限，決定「當下的利益率與周轉率能維持多久」。每點輸出 🟢🟡🔴＋一個 sourced 證據＋代理變數讀數；證據與 QC-39 軸 B 共用，不另起搜尋。

### 1. 需求基礎值——客戶為什麼買這類產品

- **先分開三個角色**：使用者／決策者／付款者（醫療：病人用、醫師選、保險付；B2B：使用者／部門主管／採購／預算負責人）。任一環節不成立，再強的需求也轉不成收入。
- **想要 vs 需要＝延後購買的代價**：不買只是少一點快樂/身分/新鮮感＝想要；不買會讓生活受阻、工作停擺、風險升高＝需要。想要型的成本重心在刺激與塑造需求（注意力、品牌、通路、文化相關性）；需要型在供應能力與履約（產能、庫存、物流、可靠性）。
- **急迫性 ≠ 持久性**：限量球鞋、熱門演唱會票急迫但未必持久；持續期分析只關心後者。
- **分開判斷「客戶要解決的問題」與「公司目前的解決方案」**：需要型的基礎需求量穩定，但滿足它的技術仍可能被替代。

### 2. 決策層級——客戶在哪一層做選擇

- 替代性要在**決策的最小單位**上衡量，不是在商品層：Costco 的衛生紙處處買得到，但客戶的決定涵蓋整趟採購（年費沉沒＋選品信任＋省下金額＋習慣→通路層黏性，續約率長年 >90%）。便利商店先選店再選飲料；券商每筆交易可替代但搬整個帳戶涉及部位/稅務/資料/時間成本。
- 供給者數量描述產業結構，**不足以**衡量客戶眼中的替代性。
- **可事前觀察的代理變數**：漲價後流失率與使用量變化、分客群續約率、資料遷移所需時間、合約年限與違約條款、重新認證/驗證週期、換產品要重訓多少員工。

### 3. 價值鏈分配——經濟利益留在誰手上

- 先估整條價值鏈創造多少經濟利益，再判斷哪些環節最難被取代；總量固定時某環節多拿＝其他環節少拿。長期反映在相對利益率、付款條件、存貨負擔、資本需求。
- 觀察面：各環節創造價值、採購金額占比、合約週期、產能狀況、買方集中度、客戶自建替代方案的能力。
- **互補品**：重要互補品從多家供應收斂到單一供應，公司自身產品沒變也會失去定價空間（手機廠×作業系統、內容平台×流量入口）。
- 反例原型：航空——服務本身有價值，但上游集中（機身雙寡頭）、稀缺起降資源、高固定成本票價戰，整鏈利益只有一小部分留在航空公司。長期需求存在 ≠ 環節內公司能賺錢。

### 4. 社會容忍度——社會願意讓你收多久

- 必需品價格彈性低，但社會對大幅漲價的容忍度也可能低——兩者同時成立就形成需求曲線上看不見的價格天花板。**實際定價上限＝經濟上限與政治/社會上限中較小者**；產品越急迫經濟空間越大，涉及公共利益越高政治空間越小。
- 奢侈品漲價可能強化稀缺；專利藥、支付、任務關鍵基礎設施漲價引來媒體、政策干預與客戶反制。案例：EU 2015 交換費上限（debit 0.2%/credit 0.3%）、澳洲央行 2003 起管制、美國 2011 起限大型發卡機構 debit 交換費——被管制費用甚至不直接屬於支付網路，主管機關仍能改變整個生態系的利益分配。
- 高必要×高敏感的公司，**刻意不把價格推到經濟上限＝保費**：降低監管介入、大客戶扶植替代者、新技術加速進場三件事的機率。
- 依賴監管授權的優勢＝政策風險：必查授權法源、寫在哪部法規、修法程序、政策討論中是否已出現替代方案——比市占率有用（市占率說現在誰贏，政策風險說裁判會不會改規則）。

## 三、再投資空間（增量 ROIC）

- **內生成長率＝增量 ROIC × 再投資率**。必須用**增量**：過去資產拿高報酬不代表下一筆新增投資拿得到。（增量 ROIC 20%×再投資 70%＝14% 成長；增量 40%×再投資 20%＝8% 成長但每元創造的經濟利益更多、可分配現金更多。）
- 高 ROIC ≠ 高成長。高 ROIC×低再投資空間仍可能是高價值公司——價值主要來自既有業務現金流，複利貢獻少；**無法以良好報酬率再投資的現金，留在公司不創造價值，配回股東才是合理配置**（→ §9.D 檢核配發紀律）。
- 刻意限制供給＝用短期成長換持續期（Hermès 按工匠培訓與稀缺性可承受的速度擴產）；用稀缺換成長（擴店、放寬授權、低價線）則賭客群/產品/通路能否區隔。兩者都是管理層的權衡，判讀時寫明公司選了哪邊、代價是什麼。
- 結果寫入 dd-meta `endo_growth_ceiling`，與 §6.D 內生天花板對齊，供 §10.6 IRR sanity check。

## 四、輸出紀律

- 企業喜歡把「想要」說成「需要」；投資人容易把「暫時稀缺」看成「不可替代」——兩者都讓成長顯得比實際持久。四檢查點的存在就是拆這兩個偏誤。
- 分開判斷三件事並分別給結論：當期 ROIC（象限）、超額報酬持續時間（四檢查點）、新增資本報酬（增量 ROIC×再投資率）——才能看出漂亮損益表來自可延續的產業位置，還是一段剛好有利的時間。


### judgment-playbook.md
# stock-analyst v14.10 — judgment-playbook.md（情境判斷手冊，QC-53 消費）

> 2026-07-08 自 18 份 v14.x DD 決策層反萃取的強模型判斷動作（Fable 5 蒸餾，四個挖掘 agent＋去重）。**用法（QC-53）**：Part II 動筆前掃「觸發索引」，命中情境的條目**逐條實際作答**（非宣告已檢查）；未命中不作答、不佔篇幅。每條格式＝觸發｜必答｜原型。條目個別可審計：2026-10 校準時逐條統計「觸發後是否改變過任何裁決/倉位/觸發器」，純儀式條目降選做或刪（rule_ledger）。

## 觸發索引（掃這張表，命中 → 跳對應條目）

| 情境 | 條目 |
|---|---|
| 寫任何觀望/迴避的重啟或升級條件 | 1, 2, 3, 4 |
| 本報告推翻了任何機械訊號（screener/燈/MA） | 5 |
| 關鍵矛盾的決勝數據尚不存在 | 6 |
| 建議分批/保留倉/trim | 7, 8 |
| 品質指標處於歷史高檔（ROTCE/GM/NIM 等） | 9 |
| 風險指標為落後型（NPL/庫存/DSO） | 10 |
| 裁決依賴管理層對負面數據的「一次性」歸因 | 11 |
| 報告期內單日 >8% 價格事件 | 12 |
| §9 出現內部人賣出 | 13 |
| 引用知名投資人 13F/持股變動 | 14 |
| 消費品牌轉機/衰退判讀 | 15 |
| §12a 有 ≥3 個不確定假設 | 16, 17 |
| §12b 有 ≥2 條失敗向量 | 18 |
| §2.C 含 FX/關稅/監管宏觀風險 | 19 |
| 存在未決訴訟/監管程序/給付變更 | 20 |
| C-suite 交接中或已預告 | 21 |
| 防禦/價值型標的算 Max DD 存活 | 22 |
| §13 引用賣方共識/目標價 | 23, 24 |
| 本裁決比賣方共識更悲觀 | 25 |
| 關鍵利空證據 sourced 日期 < 1 季 | 26 |
| sourced 競爭證據挑戰 moat_trend | 27, 28 |
| thesis 依賴產業主題順風 | 29 |
| 標的有 AI 曝險（受惠或受害） | 30 |
| moat_trend ↓ 或共識連續下修中 | 31 |
| 讀者持有中且考慮頂部/波動處置 | 32 |

## 一、裁決與觸發器設計

**1. 觸發錨型路由**（ADBE/VIK/SE/ISRG 對照）｜觀望的根本理由是哪一類——估值貴 → 價格錨（如 Fwd PE ≤32x）；thesis 未決 → 事件錨（**不設進場價位**，價格錨會誘導接刀）；趨勢未確認 → 技術錨；理由有兩個 → AND 連接（如 VIK「<$87 且 river yield 確認」）。錨型與理由不匹配＝重寫。

**2. 第三分支＋反向分支**（VIK/TT/SE/PLTR）｜if-then 必含「價格先走、證據未到」分支：續漲但未驗證 → 動作（不追/停止加碼，事前繳械 FOMO）；下跌但基本面檢核無損 → 動作（分批反買窗口，非停損），明寫檢核用哪些指標。動作從 {不追/停止加碼/分批反買/減碼/清倉} 明確選一。

**3. 重啟條件三自由度**（BSX/SNDK/NKE）｜① k-of-n 結構——嚴重度越高越合取（Hard Veto 級迴避＝3-of-3 AND；週期谷底＝2-of-3）；② 觸發後動作＝**重跑 DD 流程**，非直接建倉；③ 重啟後倉位角色自動降級（≤衛星 starter），必要時重定義部位性質（如 SNDK「重啟＝循環交易 <1% 投機倉，非投資」）。

**4. 觸發型態分流進場價**（NKE/STZ）｜升級條件含多類觸發時，各類對應的進場價規則分開寫：基本面確認觸發 → 現價亦可；技術止穩觸發 → 等指定線（如站回 W104）。

**5. Override 必附「機器對了」分支**（WLDN）｜凡推翻機械訊號（screener fail/估值燈/MA），§11 執行路徑必含一條「該訊號被證實為對」的分支——指明數據點、期限、對應動作（如「FY26 全年 OCF/NI < 1.0 → screener 對了 → 清倉」）。把 override 變成可證偽的 bet。

**6. 「不可裁決至{時點}」是合法輸出**（VIK）｜強制裁決前先答：能 settle 此矛盾的數據今天存在嗎？不存在 → 何時到達？現有支持證據的時間窗是否覆蓋風險發生窗（VIK：booking 領先數據不覆蓋 2027 運力洪水高峰）？不覆蓋 → 禁止用它宣稱風險已解，裁決寫「不可裁決至{時點}」＋為此付滿價=不對稱。

**7. 分批理由歸因＋具名彈藥倉**（GOOGL/GLW）｜任何分批/trim 必標理由類別：動能過熱/估值/具名 binary 事件/波動（**最後者禁止**）。保留 tranche 必須綁定具名事件與解鎖條件（如「2-3% 待 AdX 裁決」），禁止泛泛「等回檔」。

**8. 估值 trim 天花板數值預承諾**（ISRG >55x / TT >35x）｜適用長抱分軌的檔，估值過熱 trim 的觸發倍數事前寫成具體數字，從該檔自身倍數分布校準（各檔不同）。無數字的「最多 trim」＝臨場拉扯。

## 二、證據品質

**9. 精英指標結構/週期拆解**（NU ROTCE 29%）｜headline 品質指標處於歷史高檔且未穿越完整週期時，逐項拆「結構性成分/週期性成分/無法拆的殘差」——殘差不選邊，**定價進 Bear 機率與倉位**（NU：未穿越信用週期 → Bear 25%＋衛星倉）。「未經壓測」的優良數字不得滿額計分。

**10. 領先導數 tripwire**（SE）｜落後型風險指標（NPL/庫存/DSO）必配一個「導數級」領先閘：兩個相關量的成長率之差（如撥備增速 vs 貸款簿增速，連 2 季超前＝觸發）——早於水位惡化 1-2 季。只監測水位不合格。

**11. 管理層歸因 escrow**（DECK/UBER）｜管理層把負面數據歸因「一次性/timing」時，禁止採信也不否定——標「未證、監測」＋預登記「連 N 季 X 則歸因證偽」的期限閘與對應倉位動作。

**12. 單日暴跌歸因閘**（JBL 7/2 −11%）｜單日 >8-10% 價格事件先歸因：機械/flow（指數調整、shelf 發行、被動賣壓）vs 基本面重估。未歸因前禁止讓價格事件改變裁決；歸因為技術性 ≠ 無害（JBL：shelf 仍保留為 pre-mortem 尾部）。

**13. 內部人賣出三步模板**（WLDN）｜① 機制歸因（行權稅務 vs 主動減持）；② 留存持股比例校準訊號強度；③ 升級觸發設計為「**不同角色的內部人在更低價位跟進**」（CFO 於 <$80 跟賣 → conviction 重評）——那無法用稅務解釋。

**14. 名人持股降權**（STZ/Berkshire）｜① 申報先查證（實體/數字）；② 歸類為驗證/情緒層、非 thesis 錨；③ 反轉時只調背書權重、不得單獨改裁決。

**15. 消費品牌末端動銷層級**（STZ/NKE）｜裁決 settle 數據必用末端動銷（depletions/sell-through/絕對量），必答：本季改善有多少是通路回補或相對份額效應？sell-in 回補與類別內份額都不是反轉證據。

**16. 樞紐變數識別**（NU 資本充足性）｜必答：是否存在一個變數，其惡化會**同時打到 ≥2 個核心假設**（NU：CET1 惡化 → 放緩放貸打 H1 或增資稀釋打 H3）？有 → 該變數監測優先級高於任何單假設指標，§13a 寫入對應煞車。

**17. 敏感度排序選 Single Thing**（DECK）｜附「每個不確定假設 → Y5 EPS/目標價量化衝擊」一表；§2.F Single Thing 必須是最大單一敏感度項（數學上最傷，非最戲劇性），偏離須說明。

**18. 多失敗向量共同 tell**（UBER take rate）｜≥2 條失敗向量時必答：① 它們是否獨立（決定 bear 機率加總邏輯）；② 是否存在一個共同的財報級顯影指標？有 → 該 tell 進 §1 監測首位（N 條收斂為 1 條高槓桿數字）。

**19. 宏觀風險收斂公司損益閘**（ONON GM ≥64.5% / DECK GM <55%）｜FX/關稅/監管風險禁止寫宏觀預測——指定一個公司損益層指標＋門檻作為「吸收失敗」判定閘，把「宏觀對不對」轉換成「公司吸收力守沒守住」。

**20. 監管/訴訟：量化＋程序階梯**（BSX CMS −35% RVU / TT 訴訟）｜① 受影響營收/給付量給具體數字＋來源＋settle 事件與日期（禁定性一句話）；② 程序性質先查證（民事/刑事、個案/集體）；③ 程序里程碑映射動作階梯（集體認證+不利和解→半倉；刑事介入→清倉），docket 進 §14 監測。

**21. 管理層交接真空**（ADBE 雙真空）｜C-suite 交接期與 thesis 關鍵戰略窗重疊時，「任命完成」設為**有日期**的 §14 複審事件（非模糊「關注管理層」）。

**22. 持有期 carry 進 Max DD 存活**（STZ/NKE 股息 3-4%）｜防禦/價值型的「能否撐到復原」校驗必列持有期 carry（股息率、beta）為補償項。

## 三、共識與市場結構

**23. 共識三件套**（TT/SNDK/GOOGL/ONON）｜① 共識目標價先二次查核（API 可能滯後，用分析師計數交叉驗證）；② 現價 vs 共識均值方向與幅度一行必答＋「此對照支持還是反對本裁決」（價 ≥ 均值 → 續漲需要共識上修＝結構逆風，加碼須指明市場尚未定價的是哪一項）；③ 目標價全距 max/min > 2.5x → 說明離散反映哪個假設的兩極分歧，並下調自身 IRR/AR 點估計信心與倉位角色。

**24. 賣方分歧層級：事實 vs 框架**（DECK）｜賣方集體降評而本檔進場時必答：分歧在事實層還是框架層？框架層 → 指明賣方原多頭框架為何、與本檔論點是否同一個（賣方為你不持有的論點辦喪事＝降評潮製造你的進場價）。

**25. 反向 priced-in＋跌幅≠便宜**（ISRG −29%）｜本裁決比共識更悲觀時，義務對稱：市場的具體錯誤假設是哪一條（倍數 regime/成長基準/單一模型依賴）？「已跌 X%」不是安全邊際——基準重定為「降檔後成長對應的合理倍數」後再答便不便宜。

**26. 利空新鮮度→倉位**（UBER 1.5-2%）｜關鍵利空證據 sourced < 1 季時必答「已進賣方模型了嗎」——未進 → 初始倉位下修一級＋凍結加碼至該證據軸首個確認/否證數據點（估值便宜 ≠ 利空已定價）。

## 四、競爭、護城河與 AI

**27. 護城河三分解＋記帳紀律**（PLTR/NU/ADBE）｜競爭證據挑戰 moat_trend 時禁止只答箭頭：分別裁決「方向受損？速度放緩？哪個客群範圍失守？」＋量化攻擊者資本相對本公司量級（PLTR：對手 ~100x 資本 → trend 設 → 非 ↑）。每條負面證據只記帳一次——記 level 或記 trend，禁止兩邊重複扣（ADBE：A 級＋trend↓，A 使其不觸 Hard Veto——記帳紀律直接決定觀望 vs 迴避）。

**28. 對手方分層 fungibility**（UBER）｜thesis 依賴「供給端可替代」時，按頭部與長尾分層分別檢驗（頭部 AV 系統性繞過 Uber、fungibility 只對長尾成立）——分層後常得出「中期成立、長期頭部裂縫」的可執行結論。

**29. 主題≠份額：規模對比**（TT vs Vertiv / JBL）｜主題順風的存在與公司吃到順風是獨立命題。用跨尺度規模對比一行戳破（Vertiv 單一分部 backlog $15B ≫ TT 全公司 $10.7B）；mix 佔比高與絕對量 minority 可同時為真，分開記。份額未證實時，主題強度最多支撐觀望、不支撐付溢價。

**30. AI 淨增量會計＋附著點判別**（ADBE/ISRG）｜① 淨增量檢驗式：新 AI ARR > 被指認的被蠶食收入線才算加分，蠶食用客戶級距/席位遷移抓（$660 → $120 降級），不看 AI 營收 top-line；② 附著點：AI 長在公司自有資產之上（裝機/資料）＝強化，繞過該資產＝替代，各給分界年。「估值便宜」的分母在 AI bear 下重算一次。

**31. Bear 地板非平穩→AR 失效**（BSX）｜moat_trend ↓ 或共識連續下修中必答：Bear 錨平穩嗎？每次下修都下移 Bear 地板 → AR/正不對稱數字明文標失效、禁作進場依據（「便宜是護城河侵蝕的帳單，正不對稱是陷阱誘餌」；12x 不是底——MDT 停 12-14x 十年）。

**32. 核心可守測試**（SNDK vs CRDO/TSM）｜持有中標的頂部處置前必答：有沒有「核心可守」（thesis 完整＋through-cycle 賺錢）？有 → 波動保護紀律適用（§13b 賣出分軌）；無（價值 100% 來自循環位置）→ 波動保護不適用，改循環交易紀律（分批落袋＋移動停損）。這是賣出分軌的前置資格審查。


### timing-appendix.md
# references/timing-appendix.md｜附錄 A 擇時全節（條件載入）

> **載入時點**：填 dd-meta `signal`／`val`／`ma`／`long_term_confidence` 四個必填欄之前，一律必 Read（未讀不得填這四欄）。核心 SKILL.md 只留附錄 A 的定位聲明（INFORMATIONAL ONLY、不主導 §13、❌ 只作 row 4 節奏調節）。
> **本檔為 v15.1 文本層拆分的搬移件——條文逐字未動**（品質分 veto 門檻、final_signal 六步、估值燈四色與三個盲點救援、週線六態與 W250 斜率定義、大盤豁免係數、long_term_confidence 映射、R:R 與 `stress`=2/2 一字未改）。

---

### B / H｜基本面評級機制（品質分等級＝B 錨點、綜合訊號 final_signal＝H 錨點，metadata-only）
品質分：底分 = (護城河 §5 + 成長持久性 §6) / 2;品質分 = min(底分 + 體質 veto 加減，10)。體質檢核 5 項 veto 制（毛利率近 3 年未連續下滑 >2%p／FCF·NI ≥ 0.7／FY+1 EPS 共識近 90 天未連續下修／近 4 季營收 YoY 未全部為負／Net Debt·EBITDA ≤ 3.0 非金融）：0-2 項不過 等級不變;3 項 降 1 級;4-5 項 直接拒絕。品質等級 ≥ 7.5 A 級／6.0-7.4 B 級／< 6.0 迴避。
**final_signal = A+/A/B/C/X**：依 quality × 估值燈 × 週線結構過濾 × 大盤豁免 × trap 組合;**權威定義以 QC-31 為準**，本表與 QC-31 衝突時以 QC-31 為準;R:R 為參考項不作硬條件。**輸出進 dd-meta `signal`/`verdict`**。

| 步驟 | 條件 | 輸出 |
|:---|:---|:---|
| 1 拒絕檢核 | trap 🔴 或 gate 🔴 或 quality 拒絕（**MA ❌ 不列入拒絕檢核**） | X（但 QC-31 cross-check：thesis 完整、僅估值過熱 → 降為 B） |
| 2 高強度 | quality S/A + gate 🟢 + MA 🟢/✅ + trap 🟢 + 大盤正常 | A+ |
| 3 中高強度 | quality S/A + gate 🟡 + MA ✅ + trap 🟢 | A |
| 4 衛星級 | quality B + gate 🟢/🟡 + trap 🟢/🟡;或 S/A 有一項訊號減半 | B |
| 5 時機不到（thesis 完整） | gate 🟠 + MA stretched，或多項訊號減半但無 QC-31 C 觸發 | B（非 C） |
| 6 thesis 失敗 | 觸發 QC-31 任一：品質 < 6.0;護城河侵蝕 ≥ 3;陷阱 🔴;AI 風險 🔴 | C |

### D｜估值燈（FY+1/+2 共識輸入 + 盲點救援）
Fwd PE 5Y 分位 = (當前 − 5Y 低)/(5Y 高 − 5Y 低)×100%;PEG = 當前 Fwd PE ÷ 3Y EPS CAGR（§4）。

| 燈號 | 條件 | 邏輯 |
|:---:|:---|:---|
| 🟢 便宜 | 分位 < 30% 或 PEG < 1.0 | 歷史少見便宜 |
| 🟡 合理 | 30-70% 且 1.0 ≤ PEG ≤ 2.0 | 正常估值 |
| 🟠 偏貴 | 70-85% 或 2.0 < PEG ≤ 2.5 | 偏高位置 |
| 🔴 過熱 | > 85% 或 PEG > 2.5 | 透支未來 |

優先序：分位與 PEG 取**較嚴**者。**輸出進 dd-meta `val`**。
- **盲點 1 救援**：結構性高成長股觸發 🟠 時，三條件同時滿足（§6 綜合 🟢 高確信 + PEG < 2.0 + §6.F AI 🟢）→ 🟠 救回 🟡;不適用情境（分位 > 85% / PEG ≥ 2.0 / QC-19 近 90 天重大利空）維持 🟠。須在附錄 A 明確標註。
- **盲點 3 救援（上修救援）**：🟠 時若 FY+1 或 FY+2 共識 EPS **近 3 個月內上修 ≥ +10%**（資料源：dd-screener eps-estimates snapshots 跨期對照、步驟零' Excel revision 欄、或 sourced 券商共識追蹤;**引不出可溯數字＝不觸發，不得以敘事代替**）→ 🟠 救回 🟡。邏輯：5Y 分位的分母在共識快速上修時系統性過時，燈號懲罰的是「還沒印進共識的成長」。**僅升一級、🔴 不適用**（🔴 的條件路徑歸 row 8a），與盲點 1 合計救援上限一級。§10 結論段 consensus 落後註記是本救援的觸發偵測器——命中時**必查**上修資料，不得只留註記。須在附錄 A 明確標註。（校準證據見 references/changelog.md）
- **QC-45 未獲利高成長版估值燈**：GAAP 負 EPS 時 PE 分位與 PEG 全 undefined，但 `val` 是必填 enum 且 §13 baseline row 依賴它。改用雙尺取**較嚴**者：① **growth-adjusted EV/S** = fwd EV/S ÷ fwd 營收成長%：< 0.5 🟢 / 0.5-1.0 🟡 / 1.0-1.5 🟠 / > 1.5 🔴;② **自身上市以來 fwd EV/S 分位**（同 30/70/85 切點;上市 < 3 年僅輔助不單獨定色）。毛利率 < 50% 的硬體/服務型須另列 EV/gross-profit 對照（防高 EV/S 低毛利被 growth-adjust 美化）。燈色推導須寫明。EPS 轉正（FY+1 > 0）後改回 PE/PEG 尺。

### F｜週線結構趨勢過濾（週線 W52 / W104 / W250，SMA）
> 把「價相對長期均線的結構位置」量化成 §13 row 4 節奏訊號 + dd-meta `ma`（必填欄，8 條下游管線在讀，欄名不動）。**不輸出倉位乘數**——倉位歸 PM（QC-11），狀態只調節節奏（❌ → 分批接刀，非封鎖）。

| 狀態 | 條件 |
|:---:|:---|
| 🟢 最佳進場 | 價 < W52 且 價 > W104 且 W52/W104/W250 三條斜率全正 |
| ✅ 強勢進場 | 價 > W52 > W104 > W250 且 W250 斜率正 |
| 🟡 減半進場 | 四條件過但 W250 斜率持平（\|13 週變化\| < 3%） |
| 🟡 觀察池 | 剛站回 W104（站上 < 4 週） |
| 🟠 暫不進場 | 價 < W104 但 > W250，W250 斜率仍正 |
| ❌ 系統失效 | 價 < W250 或 W250 斜率轉負（→ §13 row 4 節奏調節，分批 starter，非封鎖裁決） |

W250 斜率定義：當週 W250 vs 13 週前 W250（正 > +3% / 持平 −3~+3% / 負 < −3%）。**盲點 2 救援**：MA ❌ 但三條件全滿足（附錄 A I 長期持有信心高 + §6 綜合 🟢 + 護城河 §5 ≥ 8）→ 降級為「🟠 暫不進場（追蹤池）」;例外失效（大盤破 W104 / QC-19 重大利空 / W250 斜率 < −10%）。**狀態判定 Python 實作（接續批量採集腳本的 closes / w52 / w104 / w250 / slope_pct）見 `references/data-collection.md`。** **輸出進 dd-meta `ma`**。
**「過熱」定義註記**：本附錄之過熱（RSI > 70 / 4 週漂移 +10%）只管 §13 進場節奏;GRP P 閘（週線布林 +2σ）與 picks 爆發 🔥（12M > +250%）各自獨立定義，不互相覆蓋。

### G｜大盤豁免層（系統性風險）
大盤週收 < 自身 W104 → 系統性風險。對應大盤：美股 SPX、台股 TAIEX、ADR/跨市場 母市場 + 上市市場取保守。係數 × 1.0（正常）/ × 0.5（破 W104）。此係數為 final_signal 的減半輸入（metadata），不主導 §13。

### I｜長期持有信心（dd-meta `long_term_confidence`，必填 enum 高/中/低）
**定義**：「值不值得抱穿 5-10 年」的綜合信念，由四個既有訊號合成（非另搜）：moat 等級（§5 合併分 → S/A/B/C）／moat_trend（§5 權威，↑→ 佳、↓ 扣）／runway_post_y5（§6.A''，🟢 佳、🔴 扣）／§12 證偽距離（失敗故事離發生多遠 + §2.F 機率）。
- **高**：moat S/A **且** moat_trend ∈ {↑, →} **且** runway_post_y5 ∈ {🟢, 🟡} **且** 證偽距離遠（§2.F 12-24M 機率 < ~20%）。
- **低**（任一）：moat_trend = ↓;runway_post_y5 = 🔴;§12 證偽近在眼前（§2.F 機率 > ~40% 或 §12b 失敗故事已在發生）;§9 capalloc_grade = C;§10.6 估值依賴型。
- **中**：其餘。
**接線**：寫 dd-meta `long_term_confidence`、進頁首儀表板、且是 QC-31 A 級必要條件之一。其他章節對「長期持有信心上限『中』」的硬接線（§6.D 內生天花板無法歸因、§9 capalloc_grade C）依上表收斂。

### R:R 三時距（資訊性，3 個數字 + 1 行 Bear anchor）
合理 P/E 參考自 §5 護城河分數 + §6 成長評級決定的倍數基準。短期（1 年）＝FY+1 EPS × 合理 P/E;中期（2 年）＝FY+2 EPS × 合理 P/E;5Y ＝ §6.E Base 5Y EPS × 長期合理 PE;各給目標價與 R:R。
**Bear anchor（1 行）**：Bear EPS = FY+1 EPS × 0.9;Bear PE = §6.E 成長熄火「降至 10%」情境;Bear 股價 = $__（現價下行 __%）。**dd-meta `stress`** 記錄 2/2（base + bear 兩情境，QC-29）;`upside_short_pct`/`upside_mid_pct` 取短/中期 R:R 對應 upside。QC-21 R:R 數學假象防禦適用。

