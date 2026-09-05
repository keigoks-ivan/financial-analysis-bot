你是 stock-analyst v17 判斷 agent，標的 CDNS（20260905）。你**只做一件事**：把證據包收斂成定案的判斷物（judgment.json／scenario.json）。你不寫散文、不碰 HTML、不產表格。流程內的驗收由機械閘與**跨模型閘（gate）**承接，不是你自己複核——你把判斷寫對、寫滿即可，不必自評。

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

- `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260905/judgment.json`（schema：`scripts/dd_schema/judgment.schema.json`；欄位語意見 bundle 內 schema 速查）
- `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260905/scenario.json`（`dd_scenario.py` 輸入格式）

兩檔寫完後，**一次複合 Bash** 跑：

```
python3 scripts/ddreport.py judge check CDNS 20260905
```

這支會依序跑 `dd_scenario.py`（產 e11.html／scenario_meta.json）、`dd_decision.py run`（產 audit.html 並回填 judgment）、`validate_judgment.py --evidence --fix --report`，把三支的結果一次回給你，你不需要也不得自行分別呼叫這三支腳本。

FAIL → **只准改被點名的欄位**、重跑同一條 `judge check`，**≤1 輪**。不得為湊過驗證而編造缺證據的數字（FAIL 通常指欄位缺失或內部恆等式不符，不是「證據不夠」）；不得整段改寫判斷。一輪後仍 FAIL 就照實回報，交給 orchestrator 處置。

## 禁（token 紀律）

- WebSearch／WebFetch：證據不足 → 在對應 judgment 欄位標「證據包未涵蓋」，不得自搜補洞；回報 orchestrator 是否需回 Stage 0 補軸。
- Read `docs/dd/` 任何既有報告。
- 重讀自己寫過的檔——judgment.json／scenario.json 寫完即以 context 內版本為準；要看驗證結果就看 `judge check` 的輸出，不要 cat 回自己的產物。
- 每檔一次 `Write`；`Edit` 只在 FAIL 後改被點名的 JSON 欄位時允許。
- 寫 `prose/`、跑 `gen_dd_tables.py`／`dd_prose_budget.py`／`render_dd.py`。

**輪次上限 `10` 輪**（含 `judge check` 與修正輪）。逼近上限時停下，把當下狀態照實回報，不得為了收尾而略過負向證據處置或漂移歸因。

## 最終回報（≤200 字）

① `judge check` 最後一次的 `validate_judgment.py --report` 原文（成功也附）
② `decision_out` 的 verdict／role／row_hit／requires_critic[]
③ 哪些覆蓋軸標了「證據包未涵蓋」（若有）
④ `evidence_dismissed[]` 的條數與各條 ref（沒有就寫 0）


===== BUNDLE =====

## ① 任務頭

標的：CDNS　日期：20260905　角色：stock-analyst v16.2 三步制的判斷（judge） agent。

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
- `$.thesis.R[].evidence_refs`（選填）：type=array
- `$.thesis.R[].evidence_refs[]`（必填）：type=string
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
- `$.moat.threats[].evidence_refs`（選填）：type=array
- `$.moat.threats[].evidence_refs[]`（必填）：type=string
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
- `$.triggers[].evidence_refs`（選填）：type=array
- `$.triggers[].evidence_refs[]`（必填）：type=string
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
- `$.contradictions[].evidence_refs`（選填）：type=array
- `$.contradictions[].evidence_refs[]`（必填）：type=string
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

ticker=CDNS　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 292.7, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-07-27", "trading_days_since": 30, "flag_within_3d": false, "note": null}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 4, "current": 60.6, "high": {"value": 78.92, "date": "2024-12-31"}, "low": {"value": 51.67, "date": "2022-12-31"}, "current_percentile_within_annual_points": 32.8}, "ps": {"n_points": 4, "current": 13.83, "high": {"value": 17.93, "date": "2024-12-31"}, "low": {"value": 12.33, "date": "2022-12-31"}, "current_percentile_within_annual_points": 26.8}, "ev_s": {"n_points": 4, "current": 14.02, "high": {"value": 17.91, "date": "2024-12-31"}, "low": {"value": 12.33, "date": "2022-12-31"}, "current_percentile_within_annual_points": 30.3}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-20", "price_used": 373.59, "fy1_eps": 7.95, "fwd_pe": 46.99}, {"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 374.93, "fy1_eps": 7.95, "fwd_pe": 47.16}, {"snapshot_date": "2026-06-04", "price_used": 376.19, "fy1_eps": 7.95, "fwd_pe": 47.32}, {"snapshot_date": "2026-06-23", "price_used": 377.27, "fy1_eps": 7.96, "fwd_pe": 47.4}, {"snapshot_date": "2026-07-16", "price_used": 330.11, "fy1_eps": 7.96, "fwd_pe": 41.47}, {"snapshot_date": "2026-07-30", "price_used": 340.02, "fy1_eps": 8.15, "fwd_pe": 41.72}, {"snapshot_date": "2026-08-13", "price_used": 324.82, "fy1_eps": 8.14, "fwd_pe": 39.9}, {"snapshot_date": "2026-08-28", "price_used": 292.7, "fy1_eps": 8.14, "fwd_pe": 35.96}, {"snapshot_date": "2026-09-04", "price_used": 292.7, "fy1_eps": 8.14, "fwd_pe": 35.96}], "current": 35.96, "high": 47.4, "low": 35.96, "current_percentile_within_window": 0.0, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 9 份快照（2026-05-20 ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": -22.19, "return_26w_pct": -1.43, "excess_return_13w_pct": -26.73, "excess_return_26w_pct": -15.95, "benchmark": "^GSPC", "rsi14": 31.05, "rsi14_usable": true, "distance_from_52w_high_pct": -29.71, "distance_from_52w_low_pct": 10.18, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 8.14, "fy2": 9.54, "fy3": 11.14}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 8.14, "fy2": 9.54, "fy3": 11.14}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 7.95, "fy2": 9.38, "fy3": 10.92}, "fy1": {"revision_pct": 0.0, "from": 8.14, "to": 8.14, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": 0.0, "from": 9.54, "to": 9.54, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 0.0, "from": 11.14, "to": 11.14, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 2.39, "fy2_revision_90d_pct": 1.71, "fy3_revision_90d_pct": 2.01, "stale": false, "note": null}, "peer_financials": {"CDNS": {"gross_margin_pct": 85.87, "operating_margin_pct": 30.82, "fcf_margin_pct": 28.64, "rd_intensity_pct": 33.02, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "SNPS": {"gross_margin_pct": 73.47, "operating_margin_pct": 9.73, "fcf_margin_pct": 30.35, "rd_intensity_pct": 32.11, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "ARM": {"gross_margin_pct": 97.54, "operating_margin_pct": 17.3, "fcf_margin_pct": 28.55, "rd_intensity_pct": 57.49, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "QCOM": {"gross_margin_pct": 54.23, "operating_margin_pct": 23.28, "fcf_margin_pct": 23.64, "rd_intensity_pct": 22.45, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "688521.SH": {"gross_margin_pct": null, "operating_margin_pct": null, "fcf_margin_pct": null, "rd_intensity_pct": null, "fiscal_period_as_of": null, "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "quarterly_income_stmt 無資料"}}, "edgar_concentrations": {"filing_type": "10-Q", "filing_date": "2026-07-29", "url": "https://www.sec.gov/Archives/edgar/data/813672/000081367226000092/cdns-20260630.htm", "excerpt": "No single customer accounted for 10% or more of total revenue during the three and six months ended June 30, 2026 or June 30, 2025. Recurring revenue includes revenue recognized over time from Cadence’s Core EDA software licensing arrangements, services, royalties, maintenance on IP licenses and hardware, and operating leases of hardware. Other recurring revenue includes revenue recognized at a point in time for short-term software arrangements that are typically renewed at least annually and revenue recognized at varying points in time over the term of other arrangements with non-cancelable commitments, whereby the customer commits to a fixed dollar amount over a specified period of time that can be used to purchase from a list of products. Arrangements that require future decisions on the performance obligations to be delivered do not meet the definition of a revenue contract until the customer executes a separate selection form to identify the products and services that they are purchasing. Each separate selection form under the arrangement is treated as an individual contract and accounted for based on the respective performance obligations. The remainder of Cadence’s revenue is recognized at a point in time and is characterized as up-front revenue. Up-front revenue is primarily generated by sales of hardware, individual IP licenses and SD&A software licenses with a term greater than one year. The percentage of Cadence’s recurring and up-front revenue in any single fiscal period is primarily impacted by delivery of hardware and IP products to its customers. The following table shows the percentage of Cadence’s revenue that is classified as recurring or up-front for the three and six months ended June 30, 2026 and June 30, 2025: Three Months Ended Six Months Ended June 30, 2026 June 30, 2025 June 30, 2026 June 30, 2025 Revenue recognized over time 72 % 73 % 72 % 75 % Other recurring revenue 6 % 5 % 6 % 5 % Recurring revenue 78 % 78 % 78 % 80 % Up-front revenue 22 % 22 % 22 % 20 % Total revenue 100 % 100 % 100 % 100 % 10 Significant Judgments Cadence’s contracts with customers often include promises to transfer to a customer multiple software and/or IP licenses and services, including professional services, technical support services, and rights to unspecified updates. Determining whether licenses and services are distinct performance obligations that should be accounted for separately, or not distinct and thus accounted for together, requires significant judgment.", "note": null}, "latest_quarter_kpis": {"_required": true, "quarter": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "items": [{"metric": "營收（GAAP）", "value": 1584, "unit": "百萬美元", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": "consensus ≈$1.58B（Zacks Consensus Estimate，來源：web_search 財報前瞻報導）；實際超出約0.5%", "prior_quarter": "Q2 2025: $1,275M（YoY +24.2%）；Q1 2026: $1,474M（QoQ +7.5%）"}, {"metric": "Non-GAAP 營業利益率", "value": 45.5, "unit": "%", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": "公司自身 Q2 guidance 43.5–44.5%（於 Q1 2026 法說給出）；實際 45.5% 優於高標", "prior_quarter": "Q1 2026: 44.7%；Q2 2025: 42.8%（YoY +270bp）"}, {"metric": "GAAP 營業利益率", "value": 28.4, "unit": "%", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": null, "prior_quarter": "Q1 2026: 29.3%；Q2 2025: 19.0%（YoY +940bp）"}, {"metric": "自由現金流（FCF）", "value": 582.3, "unit": "百萬美元（FCF margin ≈36.8%；估算值＝6個月YTD OCF $990.7M－Q1 OCF $355.8M，減6個月YTD capex $101.4M－Q1 capex $48.8M，因新聞稿只揭露YTD累計現金流量表、未單獨拆分單季）", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx（Q2單季為YTD減去Q1新聞稿揭露值換算，Q1 OCF $355.8M／capex $48.8M／FCF $307.0M）", "vs_consensus": null, "prior_quarter": "Q1 2026: $307.0M（FCF margin ≈20.8%）"}, {"metric": "SBC 占營收／占GAAP營業利益比", "value": 9.3, "unit": "%（SBC $146.9M ÷ 營收 $1,584M＝9.3%；SBC ÷ GAAP營業利益 $449.9M＝32.7%）", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": null, "prior_quarter": "Q1 2026: SBC $138.2M／營收$1,474M＝9.4%"}, {"metric": "管理層財測（Q3 2026 及 FY2026，Q2財報時給出）", "value": "Q3 2026: non-GAAP EPS $2.01–$2.07、non-GAAP營業利益率43.5–44.5%、GAAP營業利益率27.5–28.5%；FY2026（上修）: 營收$6.26–$6.34B（≈+19% YoY）、non-GAAP營業利益率43.75–44.75%、non-GAAP EPS $8.05–$8.15", "unit": "guidance range", "as_of": "公告於 2026-07-27，隨Q2 2026財報發布", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": null, "prior_quarter": "Q1 2026法說時的FY2026原guidance：營收$6.125–$6.225B（≈+17% YoY）、non-GAAP EPS $7.85–$7.95 → 本次全面上修"}, {"metric": "Backlog／12個月RPO（SaaS類遞延收入代理指標，Cadence未揭露NRR或ARR客戶數）", "value": "Backlog $8.1B（record）；未來12個月將認列的RPO $4.2B", "unit": "billion USD", "as_of": "Q2 2026（季末 2026-06-30，公告於 2026-07-27）", "source": "公司新聞稿 https://investor.cadence.com/news/news-details/2026/Cadence-Reports-Second-Quarter-2026-Financial-Results/default.aspx", "vs_consensus": null, "prior_quarter": "Q1 2026: Backlog $8.0B；12個月RPO $4.0B"}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | 0 | 2025-06-01 | 2024 年全球 EDA 市場份額：Synopsys 約 31%、Cadence 約 30%、Siemens EDA 約 13%，三家合計逾九成營收，為高度集中的雙強＋一（Cadence/Synopsys/Siemens）格局，2025-2026 未見結構性洗牌。 | EDA Market Primer (SemiAnalysis newsletter, newsletter.semianalysis.com/p/eda-market-primer) | moat_trend,thesis.H |
| competitive_share_entrants#1 | + | 2026-04-01 | Cadence 核心 EDA 業務 FY2026 Q1 年增 18%，公司上調 2026 全年營收指引至 $6.26-6.34B（原 $6.125-6.225B），股價因 18.7% 年增營收、$8B 積壓訂單（多與 AI 需求相關）而上漲，顯示 Cadence 在整體 EDA 市場擴張中維持份額並受惠於 AI 驅動需求擴大。 | Cadence Raises 2026 Outlook as AI Agents Drive Broader EDA Demand (Yahoo Finance, finance.yahoo.com/technology/ai/articles/cadence-raises-2026-outlook-ai-164000799.html) | thesis.H,moat_trend |
| competitive_share_entrants#2 | + | 2026-01-01 | Cadence 在多代工廠（TSMC／Samsung／Intel／Rapidus）動態上被評為比 Synopsys 更有利卡位，其半導體 IP 營收 FY2025 Q1 年增達 40%；相對地 Synopsys 已承認 FY26 IP 業務將是清淡的一年（muted year），顯示 IP 這一子區隔 Cadence 相對競爭對手份額走強。 | Synopsys and Cadence: The $160B Unsung Giants of Semiconductor Design (datagravity.dev/p/synopsys-and-cadence-the-160b-unsung) | thesis.H,moat_trend |
| competitive_share_entrants#3 | 0 | 2026-06-01 | 2026 年 DAC（Design Automation Conference）Chips to Systems 大會上，Synopsys、Cadence、Siemens 三大既有對手同步發表全自主 agentic 晶片設計工作流（Synopsys 全自主長流程 agentic workflow、Cadence AuraStack AI Super Agent／ChipStack AI、Siemens 自我驗證 agentic workflow）；查無具規模的全新進入者（non-incumbent new entrant）對 Cadence 構成搶單威脅，2026 年競爭仍集中在既有三大廠之間的 AI 能力軍備競賽。 | Synopsys, Cadence, and Siemens Take Agentic Chip Design Autonomous at DAC (Futurum Group, futurumgroup.com/insights/synopsys-cadence-and-siemens-take-agentic-chip-design-autonomous-at-dac/) | moat_trend,thesis.H |
| customer_second_source#0 | 0 | 2026-01-01 | Intel 為 Cadence 最大單一客戶帳戶（single largest account），且歷史上 Cadence 在 Intel 的滲透相對其在 TSMC／Samsung 的地位偏弱；2026 年 Cadence 正嘗試在 Intel 拓展業務灘頭（gain traction），意味這是一個仍待鞏固而非已鎖定的客戶關係。 | Hudson Labs: Cadence Design Systems (CDNS) Equity Initiation Report (hudson-labs.com/research/cadence-design-systems-cdns-equity-initiation-report) | thesis.R,decision_inputs.bear |
| customer_second_source#1 | + | 2026-04-16 | 超大規模業者（hyperscalers，如 Apple／Amazon／Google／Microsoft）與 Tesla 等正加速建立自有晶片設計團隊、發展客戶自有工具（COT, Customer-Owned Tooling）自研晶片；但查得的證據顯示這些內部設計團隊是**擴大採用並整合** Cadence／Synopsys 既有工具（而非以自研工具取代之），例如某大型超大規模業者已採用 Cadence 數位全流程（digital full flow）完成其首次全 COT AI 晶片流片，Cadence 與 Google 亦整合 Gemini AI 平台與 ChipStack AI Super Agent；查無證據顯示主要客戶正以自製 in-house EDA 工具取代 Cadence 授權，內部晶片設計團隊擴張反而被引述為推升 EDA 授權需求的正面驅動力。 | The Embrace Of AI In Design Transforms Cadence And Its Customers (The Next Platform, nextplatform.com/ai/2026/04/16/the-embrace-of-ai-in-design-transforms-cadence-and-its-customers/5217962) | moat_trend,thesis.R,decision_inputs.bear |
| customer_second_source#2 | - | 2026-01-01 | Cadence 業務揭露其最大風險之一為對少數大型半導體與超大規模運算客戶的營收集中度（customer concentration），主要客戶帳戶延遲或流失重大專案會直接衝擊財報表現；公司未單獨揭露特定客戶佔營收百分比等具體集中度數字。 | Hudson Labs: Cadence Design Systems (CDNS) Equity Initiation Report (hudson-labs.com/research/cadence-design-systems-cdns-equity-initiation-report) | thesis.R,decision_inputs.bear,valuation |
| customer_second_source#3 | + | 2026-07-14 | Cadence FY2026 硬體（emulation／prototyping，即 Dynamic Duo）業務創紀錄，新增 30 家以上客戶、既有客戶回購需求大增，前十大硬體客戶中有 7 家同時採用模擬（emulation）與原型（prototyping）雙產品，顯示 Cadence 在硬體驗證這一環對主要客戶的滲透（而非被 second-source）正在加深，未見主要客戶導入第二供應商替代 Cadence 硬體產品線的證據。 | Cadence Design Systems vs. Synopsys: Which Technology Stock Is a Better Buy in 2026? (The Motley Fool, fool.com/coverage/better-buy/2026/07/14/cadence-design-systems-vs-synopsys-which-technology-stock-is-a-better-buy-in-2026/) | moat_trend,thesis.H |
| customer_concentration_credit#0 | 0 | 2025-09-30 | Cadence 2025 Q3 10-Q 揭露：截至 2025-09-30 無單一客戶占應收帳款 10% 以上；相較截至 2024-12-31 時有一名客戶占應收帳款約 11%，顯示客戶集中度已略降但曾一度接近門檻（此為應收帳款集中度，非營收集中度，10-K 本身未查到具體營收占比數字）。 | Cadence Design Systems Q3 2025 10-Q filing (投資人關係 PDF, s206.q4cdn.com) | thesis.R,decision_inputs.bear |
| customer_concentration_credit#1 | - | 2025-08-05 | Fitch 於 2025-08-05 將 Intel 長期信評自 BBB+ 下調至 BBB、展望負向，原因為獲利能力預期未來 12-18 個月持續疲弱、核心 client/data center 市占流失、晶圓代工業務營運虧損；Intel 為 Cadence 主要 EDA 客戶之一（歷史上位列前幾大客戶）。Fitch 同時指出 Intel 帳上仍有 $212 億現金及短期投資、$70 億未動用循環信貸額度，流動性尚屬穩健。 | CNBC "Intel's credit rating downgraded by Fitch on demand challenges" | thesis.R,decision_inputs.bear |
| customer_concentration_credit#2 | - | 2024-12-11 | S&P 於 2024-12-11 將 Intel 信評自 BBB+ 下調至 BBB，Moody's 亦將 Intel 高級無擔保信評下調至 Baa2（自 Baa1），皆反映 Intel 財務體質動盪，距投資等級底線（junk）僅剩兩級。 | The Register "Intel turmoil prompts S&P Global to downgrade chipmaker's credit rating" | thesis.R |
| customer_concentration_credit#3 | - | 2025-11-13 | Samsung 晶圓代工（Foundry）部門財務壓力預期持續至 2027 年，市場對其獲利轉正時點的預期已由 2027 年遞延至 2028 年（此為部門層級虧損，非 Samsung Electronics 集團整體信評遭下調）。Samsung 為 Cadence 主要客戶之一。 | TrendForce "Samsung Reportedly Eyes Foundry Profitability by 2027 with 20% Market Share"（後續 AnySilicon 報導指出時點已遞延至 2028） | thesis.R |
| customer_concentration_credit#4 | + | 2026-Q1 | Samsung 晶圓代工稼動率於 2026 年第一季升破 80%，為一年高點，顯示該客戶端接單動能回升，部分抵銷部門獲利壓力的負面訊號。 | SemiWiki "More Clients Leads to 80% Utilization at Samsung Foundry in 1Q2026" | thesis.R |
| supply_demand_durability#0 | + | 2026-07-27 | Cadence FY2026 Q2（財報日 2026-07-27）：營收 $15.84 億、年增 24.2%；創紀錄 backlog $81 億；IP 業務年增逾 40%、Core EDA 年增 18%、System Design and Analysis 年增 37%；公司同步上修 2026 全年營收展望至 $62.60-63.40 億、Non-GAAP EPS 展望至 $8.05-8.15。值得注意的是 2026 為公司三年更新週期中續約金額相對較低的一年，backlog 仍創新高顯示需求動能非僅來自續約時點，而是新增業務（本季新增 12 個新客戶）。 | Cadence 8-K CFO commentary (SEC EDGAR, cfocommentary07272026ex9902.htm) / Zacks "Cadence Q2 Earnings Top Estimates on AI Demand, Backlog Hits $8.1B" | thesis.H,decision_inputs.bear,triggers |
| supply_demand_durability#1 | + | 2026 | 產業研究機構預測全球 EDA 市場規模將自 2026 年約 $182 億成長至 2033 年 $335 億（CAGR 9.1%），成長動能歸因於設計複雜度上升、AI/ML 晶片普及、sub-5nm 製程滲透（報告稱逾 65% 新設計案已採用 FinFET/GAAFET 架構），論述定位為結構性而非景氣循環驅動。 | Persistence Market Research "Electronic Design Automation (EDA) Market Size & Forecast, 2033" | thesis.H |
| supply_demand_durability#2 | + | 2026 | 半導體設備業界預期 AI 驅動資本支出持續至 2027 年、晶片設備銷售將創 $1,560 億歷史新高，JPMorgan 與 Goldman Sachs 預估 2027 年 AI 資本支出達 $1 兆以上規模。 | EE Times "AI Drives CapEx Chip Equipment to Record $156B in 2027" | thesis.H |
| supply_demand_durability#3 | - | 2026 | 市場評論警示 AI 基礎建設投資與實際軟體端營收之間存在顯著落差，永續性測試可能於 2027 年（多數大型專案完工、設備銷售觸頂之際）浮現；分析估計 AI 產業需在 2030 年前達到約 $2 兆年營收方能支撐當前投資水準，若 Agentic AI 轉型未能兌現對應生產力增益，行業恐面臨類似 2000 年代初網路泡沫的急遽收縮。 | Pine Tree Macro Research (Substack) "The AI Capex Bubble: Bigger Than You Think" | thesis.R,decision_inputs.bear |
| regulatory_antitrust#0 | 0 | 2025-07 | 公開搜尋未查得任何鎖定 Cadence（CDNS）本身的 2026 年正式反壟斷調查、拆分程序或 DOJ/FTC/EU 競爭調查報導；EDA 產業近期唯一重大競爭結構變動是對手 Synopsys 完成收購 Ansys（約 350 億美元交易），該案在多國（含中國 SAMR）經過延長反壟斷審查後於 2025 年 7 月完成交割，形成首個垂直整合的 device-to-system 設計堆疊，但此案標的為 Synopsys/Ansys 非 Cadence，未見對 Cadence 本身的監管動作 | SemiAnalysis newsletter "EDA Market Primer" (newsletter.semianalysis.com/p/eda-market-primer) | decision_inputs.bear,moat_trend |
| regulatory_antitrust#1 | 0 | 2025-12 | EDA 市場呈現寡占結構：前五大廠商（Synopsys、Cadence、Siemens EDA、Keysight、Zuken）合計約占 AI EDA 市場 70-85% 份額；Cadence 本身約占全球 EDA 市場 30%，與 Synopsys 並列兩大主導廠商——此高集中度本身是產業特性（非近期監管介入結果），但為未來潛在反壟斷關注的市場背景 | MarketsandMarkets "Synopsys, Inc. (US) and Cadence Design Systems, Inc. (US) are Leading Players in the AI EDA Market" (marketsandmarkets.com/ResearchInsight/ai-eda-companies.asp); MatrixBCG competitor analysis (matrixbcg.com/blogs/competitors/cadence) | moat_trend,decision_inputs.bear |
| reg_tariff_export#0 | - | 2025-07-28 | 美國商務部 BIS 對 Cadence 因非法出口 EDA 硬體/軟體與半導體設計技術給 Entity List 上（涉及中國軍事最終用途）的實體，處以 9,500 萬美元行政罰款；同時司法部（DOJ）併行協議追加 4,500 萬美元沒收金，合計逾 1.4 億美元，Cadence 對出口管制違規事實表示認罪 | BIS press release "Cadence Design Systems to Pay $95 Million Penalty to BIS..." (bis.gov/press-release); BIS Final Order (bis.gov/media/documents/cadence-design-systems-final-order-7.28.2025.pdf); San Jose Inside "Cadence Design Systems Admits Selling Design Tools to China, Will Pay Over $140M in Penalties" | decision_inputs.bear,thesis.R,triggers |
| reg_tariff_export#1 | 0 | 2025-07-02 | 2025 年 5 月 23 日 BIS 曾通知 Cadence，其 EDA 軟硬體技術（ECCN 3D991/3E991）出口、再出口或境內轉讓至中國或中國軍事最終用戶方須取得許可證；但 BIS 於同年 7 月 2 日隨即撤銷該許可證要求，即時生效 | Crowell & Moring LLP "Joint Criminal and Civil Export Controls Enforcement: Lessons from the Cadence Case" (crowell.com/en/insights/client-alerts) | thesis.R,triggers |
| reg_tariff_export#2 | 0 | 2025-11-11 | 2025 年 9 月 BIS 發布過渡最終規則，將出口限制擴大適用至由 Entity List 或 Military End-User List 實體持股 50% 以上的關聯公司（俗稱「50% 規則」）；但 BIS 於 2025 年 11 月 11 日公告將該新規則暫停實施一年，目前預定於 2026 年 11 月 9 日到期恢復 | Crowell & Moring LLP client alert; BIS press releases referenced therein | thesis.R,triggers,decision_inputs.bear |
| reg_tariff_export#3 | - | 2025-12-31 | 依 Cadence FY2025 10-K 揭露，中國市場占公司總營收約 13%（2024 年約 12%、2023 年約 17%），為呈現波動但持續重大的地區集中度；公司在風險因子章節將出口管制進一步收緊列為可能大幅移除此營收來源且短期難以替代的風險 | SEC EDGAR, CADENCE DESIGN SYSTEMS INC Form 10-K FY2025 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | decision_inputs.bear,thesis.R,valuation |
| reg_tariff_export#4 | 0 | 2026-01-15 | 2026 年 1 月 15 日生效的美國 Section 232 半導體關稅（對特定先進半導體徵收 25% 從價稅，鎖定符合特定 Tensor Processing Performance 與 DRAM 頻寬門檻的高效能晶片，如 NVIDIA H200、AMD MI325X）條文與豁免範圍（美國境內資料中心、研發、新創、維修、非資料中心消費/工業用途、公部門）鎖定實體晶片產品，公開資料未見將 EDA 設計軟體本身納入課徵範圍的規定 | White & Case LLP "President Trump orders narrowly targeted 25% Section 232 tariff on certain advanced semiconductor articles"; Z2Data "The Section 232 Semiconductor Tariff, Explained" | decision_inputs.bear |
| geo_supply_chain#0 | - | 2026-02 | Cadence 10-K（FY2025）風險因子揭露：公司對美中地緣政治與經貿不確定性存在重大曝險，包括現行及未來美中貿易法規、關稅與其他貿易限制的未知影響，並特別點名台灣作為科技產業供應鏈核心樞紐的地緣政治風險。 | SEC EDGAR: Cadence Design Systems Form 10-K FY2025 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | thesis.R,decision_inputs.bear |
| geo_supply_chain#1 | - | 2025-07-02 | 美國商務部 BIS 於 2025-05-23 通知 Cadence，對中國或中國軍事最終用戶交易涉及特定 ECCN 分類之 EDA 軟體與技術的出口/再出口/境內轉移須申請許可；2025-07-02 BIS 通知該許可要求即刻撤銷，Cadence 已恢復受影響中國客戶的 EDA 軟體與技術存取。公司揭露該段暫時性許可要求已對同期中國區營收造成負面影響。 | Cadence 10-K FY2025 risk factors, as summarized in company SEC filing disclosure (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | thesis.R,decision_inputs.bear,moat_trend |
| geo_supply_chain#2 | - | 2026-02 | Cadence 於 10-K 明確揭露前瞻風險：鑑於美中持續談判，美國未來可能考慮對 Cadence 之 EDA 軟體與技術或其他產品服務重新施加或擴大此類（或額外）出口管制限制，屬於未解除的政策不確定性。 | Cadence 10-K FY2025 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | thesis.R,decision_inputs.bear,triggers |
| geo_supply_chain#3 | 0 | 2025-12-31 | 中國區營收於 FY2025 為 $679.97M，占公司總營收 5.31%（同期美洲區占 19.38%、除中日以外亞洲區占 13.17%，皆為對總營收之占比而非互斥地理分組加總 100%）。 | Cadence 10-K FY2025 geographic revenue disclosure, as reported via StockTitan SEC filing summary (stocktitan.net/sec-filings/CDNS/10-k-cadence-design-systems-inc-files-annual-report-6bcef311af10.html) | thesis.R,valuation |
| geo_supply_chain#4 | - | 2025-07-28 | Cadence 因 2015-2021 年間對中國國防科技大學（NUDT，美國 Entity List 軍方大學）非法出口 EDA 設計工具與技術一案，就一項共謀違反出口管制罪名向 DOJ 認罪，並與商務部 BIS 達成民事和解，合計裁罰逾 $140M；此為出口管制刑事/民事執法紀錄，顯示公司過去在中國/軍方終端客戶合規把關上曾出現漏洞。 | DOJ Office of Public Affairs press release (justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting); BIS press release (bis.gov/press-release/cadence-design-systems-pay-95-million-penalty-bis-unauthorized-exports-chinese-entities-tied-development) | thesis.R,decision_inputs.bear,moat_trend |
| end_markets#0 | + | 2026-04 | Cadence FY2026 Q1 營收結構：Core EDA 占 71%（年增 18%，主要動能為在指標型客戶的滲透擴大及硬體模擬〔emulation〕創單季歷史新高，由 AI 與 HPC 客戶帶動）；半導體 IP 占 14%（年增 22%，由 AI／HPC／車用工作負載加速需求帶動，並與一家主要晶圓代工客戶簽下鎖定 2 奈米製程節點的創紀錄規模 IP 訂單）；System Design and Analysis 占 15%（年增 18%，3D-IC 與多物理模擬動能強勁，受 AI 驅動的系統複雜度上升帶動）。 | TIKR.com blog: 'Cadence Design Systems Stock Q1 2026 Earnings: Every Segment Grew Double Digits' (tikr.com/blog/cadence-design-systems-stock-q1-2026-earnings-every-segment-grew-double-digits) | thesis.H,moat_trend |
| end_markets#1 | + | 2026-07-27 | 公司將 2026 全年營收展望上修至 $6.125B–$6.225B（GAAP／non-GAAP 營業利益率 27.5–28.5%／43.5–44.5%），Q2 FY2026 營收 $1.584B、年增 24.2%，優於預期；管理層將成長歸因於超大規模業者（hyperscaler）基礎設施與 physical AI 相關的廣泛系統架構設計活動。 | Yahoo Finance: 'Cadence Q2 Earnings Top Estimates, 2026 Revenue Outlook Raised' (finance.yahoo.com/markets/stocks/articles/cadence-q2-earnings-top-estimates-145000369.html) | thesis.H,valuation |
| end_markets#2 | + | 2026-07 | Cadence 進入 2026 年時的訂單積壓（backlog）達創紀錄的 $7.8B；管理層將 agentic AI（如 ChipStack）列為長期持續性成長動能，Q2 新增 12 家硬體客戶並擴大與多家 hyperscaler 及 AI 業者的合作，反映 hyperscaler 自研晶片（custom silicon）趨勢加速，Cadence 同時提供 EDA 工具與 IP 兩端服務。 | Yahoo Finance: 'Cadence Raises 2026 Outlook as AI Agents Drive Broader EDA Demand' (finance.yahoo.com/technology/ai/articles/cadence-raises-2026-outlook-ai-164000799.html) | thesis.H,moat_trend |
| end_markets#3 | 0 | 2026-01 | 全球 EDA 工具市場 2026 年規模約 $20.78B，預估以 CAGR 8.10% 成長至 2031 年 $30.67B（另一機構估算基期不同：EDA 軟體市場 2025 年 $14.28B，以 CAGR 11.5% 成長至 2034 年 $38.05B）；市場集中度高，Synopsys、Cadence、Siemens 三家合計約占全球營收 70%，其中 Synopsys 約 31%、Cadence 約 30% 市占。 | Mordor Intelligence: 'Electronic Design Automation Tools (EDA) Market Analysis'; Precedence Research: 'Electronic Design Automation Software Market Size to Hit USD 34.71 Billion by 2035' | valuation,moat_trend |
| substitute_technology#0 | - | 2026-08-18 | CDNS 股價捲入市場對 AI 顛覆傳統軟體公司獲利模式疑慮所引發的更廣泛軟體股拋售潮，市場憂心 AI 可能自動化部分晶片設計工作流程、降低公司長期可觸及市場的成長率。 | CNBC - "Cadence is a chip stock left behind by the AI boom. Why the CEO says that's a mistake" (https://www.cnbc.com/2026/08/18/cadence-is-a-chip-stock-left-behind-by-the-ai-boom-why-the-ceo-says-thats-a-mistake.html) | thesis.R,decision_inputs.bear,valuation |
| substitute_technology#1 | 0 | 2026-08-18 | Cadence CEO Anirudh Devgan 公開回應軟體股拋售疑慮，主張設計先進晶片需要精確的物理與數學運算，AI 本身無法取代公司核心工具，並將公司基礎工具比喻為「V6/V8 引擎」、AI 為輔助而非替代。 | CNBC - "Cadence is a chip stock left behind by the AI boom. Why the CEO says that's a mistake" (https://www.cnbc.com/2026/08/18/cadence-is-a-chip-stock-left-behind-by-the-ai-boom-why-the-ceo-says-thats-a-mistake.html) | moat_trend,thesis.H |
| substitute_technology#2 | - | 2026-03-26 | Siemens EDA 於 2026 年 Semicon China 展示其 Fuse EDA AI Agent，採用 RAG 框架與多模態 EDA 資料基礎設施，能自主協調前端設計、驗證與量產簽核跨流程工作，主張可將晶片設計週期縮短一半，對 Cadence 傳統 EDA 工具形成競爭壓力。 | Digitimes - "Semicon China 2026: Siemens EDA pushes agentic AI to cut chip design cycles in half" (https://www.digitimes.com/news/a20260326VL206/siemens-eda-design-semicon-china-2026-ic.html) | moat_trend,thesis.R |
| substitute_technology#3 | + | 2026-04-16 | 系統廠商（含 hyperscaler）現占 Cadence EDA 需求的 45%，較兩年前的 40% 上升；一家指標性 hyperscaler 已採用 Cadence 數位全流程完成其首顆全 COT（Customer-Owned Tooling）AI 晶片流片，驗證 Cadence 在最高難度客戶端的數位競爭力，且多筆 COT 流片仍在進行中。 | The Next Platform - "The Embrace Of AI In Design Transforms Cadence And Its Customers" (https://www.nextplatform.com/ai/2026/04/16/the-embrace-of-ai-in-design-transforms-cadence-and-its-customers/5217962) | moat_trend,thesis.H |
| channel_business_model_shift#0 | 0 | 2026-02-05 | EDA 產業雲端部署區隔預期成長最快，雲端運算彈性擴展正拓寬客戶對進階驗證工具的取用管道，但因 IP 敏感性，仍有 69.60% 的設計流程留在地端（on-premise），顯示通路／部署模式轉移速度受限。 | GlobeNewswire - "Electronic Design Automation Tools (EDA) Research Report 2026: Market Share Analysis, Industry Trends & Statistics, Growth Forecasts Report 2025-2031" (https://www.globenewswire.com/news-release/2026/02/05/3233268/28124/en/Electronic-Design-Automation-Tools-EDA-Research-Report-2026-Market-Share-Analysis-Industry-Trends-Statistics-Growth-Forecasts-Report-2025-2031.html) | thesis.R,moat_trend |
| channel_business_model_shift#1 | + | 2026-04-16 | Cadence 銷售通路組合為高接觸度直接企業銷售（針對頂層客戶的專屬客戶團隊與現場應用工程師深入嵌入設計週期）搭配擴大中的雲端與合作夥伴通路以觸及中型市場與區域成長；系統廠商／hyperscaler 客戶占比持續上升（見 substitute_technology 軸 F4：45% 較兩年前 40%），為公司主動朝大型系統廠商直接經營的通路重心轉移。 | The Next Platform - "The Embrace Of AI In Design Transforms Cadence And Its Customers" (https://www.nextplatform.com/ai/2026/04/16/the-embrace-of-ai-in-design-transforms-cadence-and-its-customers/5217962) | moat_trend,thesis.H,triggers |
| capital_markets_pricing#0 | + | 2026-07-27 | Cadence 於 2026-07-27 公布 Q2 2026 財報後上修 FY2026 財測：營收指引由 $6.13-6.23B 上修至 $6.26-6.34B（中值年增 19%）、non-GAAP EPS 指引由 $7.85-7.95 上修至 $8.05-8.15，Q2 本身營收 $1.584B／EPS $2.11 均優於分析師預期，且 backlog 創紀錄達 $8.1B。 | Benzinga — "Cadence Design Systems Beats Q2 Estimates, Raises 2026 Outlook"（investor.cadence.com Q2 2026 財報稿佐證） | thesis.H,valuation,decision_inputs.bear |
| capital_markets_pricing#1 | 0 | 2026-07-28 | 上修後的 FY2026 指引中值（營收 $6.30B／EPS $8.10）仍略低於當時賣方共識（營收 $6.329B／EPS $8.12），顯示公司指引雖上修但未超越市場預期。 | Simply Wall St News — "Cadence Design Systems (CDNS) Lifts 2026 Outlook, Is The Stock Fully Priced?" | valuation,thesis.R |
| capital_markets_pricing#2 | + | 2026-07-28 | Q2 財報後賣方目標價全面上修：BofA Securities 由 $400 調升至 $420（維持 Buy）、KeyBanc 調升至 $425、Stifel 重申 Buy 並維持 $432 目標價。 | ChartMill.com — "Cadence Design Systems (NASDAQ:CDNS) Upgrades Guidance as a High Growth Stock Powered by AI"；Investing.com — "Stifel reiterates Cadence Design stock rating on strong margins" | valuation,decision_inputs.bull |
| capital_markets_pricing#3 | + | 2026-09-02 | 近期（2026-09-01~02）25 位華爾街分析師中位數 12 個月目標價為 $405（區間 $300-$470），對 `numbers.price_at_dd`（$292.7）隱含約 +32% 上檔空間；買進評等占比達 84%。 | WallStreetZen — "Cadence Design Systems Stock Forecast & Predictions: 1Y Price Target $385.00"；Simply Wall St — "Cadence Design Systems (NasdaqGS:CDNS) Stock Forecast & Analyst Predictions" | valuation |
| capital_markets_pricing#4 | 0 | 2026-07-28 | 儘管賣方目標價共識偏多（多數 Buy／Strong Buy），Zacks 量化模型評等維持 Zacks Rank #3（Hold），與賣方分析師普遍樂觀評等形成落差。 | Simply Wall St / 綜合報導引用之 Zacks Rank 資料（見 CDNS 分析師評等彙整頁） | thesis.R,decision_inputs.bear |
| major_events#0 | 0 | 2026-02-23 | Cadence 完成收購 Hexagon 旗下設計與工程（D&E）事業，交易金額約 €2.7B／$3.2B，2026-02-23 完成交割；公司預期該業務 2026 年貢獻約 $160M 營收，非 GAAP 基礎下對 2026 EPS 稀釋約 28 美分，2027 年轉為增益。 | Cadence newsroom press release: 'Cadence Completes Acquisition of Hexagon's Design and Engineering Business, Advancing Leadership in Physical AI and Multiphysics' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-completes-acquisition-of-hexagons-design-and-engineering.html) | thesis.H,decision_inputs.bear,moat_trend |
| major_events#1 | + | 2026-03-05 | Cadence 收購 EMA Design Automation（金額未揭露），強化其 PCB 設計領域布局，2026-03-05 完成。 | Tracxn deal brief: 'Cadence Acquires EMA' (tracxn.com/d/insights/merger-acquisition-deals-brief/cadence-acquires-ema/__2GFeel2DERN2Huua_VuEI8_1eWy4KiZTZGAH09AhLl4) | moat_trend |
| major_events#2 | + | 2025-08-27 | Cadence 完成收購 Arm 的 Artisan foundation IP 業務（標準元件庫、記憶體編譯器、先進製程節點 GPIO），2025-08-27 完成交割，公司表示對 2025 年營收/獲利影響不重大。 | Cadence newsroom press release: 'Cadence Completes Acquisition of Arm Artisan Foundation IP Business' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-completes-acquisition-of-arm-artisan-foundation-ip.html) | moat_trend,thesis.H |
| major_events#3 | + | 2025-11-03 | Cadence 完成收購 Secure-IC（嵌入式資安 IP 廠商），2025-11-03 完成交割，鎖定車用/資料中心/航太國防/行動/IoT 等終端的嵌入式安全需求。 | Cadence newsroom press release: 'Cadence Completes Acquisition of Secure-IC' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-completes-acquisition-of-secure-ic.html) | moat_trend |
| major_events#4 | - | 2025-07-28 | Cadence 就 2015-2021 年間銷售 EDA 工具與 IP 予中國國防科技大學（NUDT，美國商務部 Entity List 上的中國軍方大學）一案，與美國 DOJ／商務部 BIS 達成和解：對美國母公司刑事一項共謀違反出口管制罪名認罪，支付刑事罰金約 $72M＋沒收 $45M（DOJ 側），另與 BIS 達成民事和解支付逾 $95M，合計對外揭露總額約 $140M（多家媒體引用 $140.6M 淨額），並承諾三年緩刑期內強化出口合規計畫與年度稽核。（註：此為 DOJ／BIS 出口管制刑事與民事執法案件，非 SEC 調查亦非財報重編，性質上最接近本軸「監管調查」類別故一併揭露。） | DOJ Office of Public Affairs press release: 'Cadence Design Systems Agrees to Plead Guilty and Pay Over $140 Million for Unlawfully Exporting Semiconductor Design Tools to a Restricted PRC Military University' (justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting); BIS press release (bis.gov/press-release/cadence-design-systems-pay-95-million-penalty-bis-unauthorized-exports-chinese-entities-tied-development) | thesis.R,decision_inputs.bear,moat_trend |
| major_events#5 | + | 2026-05-31 | Cadence 與 NVIDIA 於 Computex 2026 發表業界首個全自主（Level-5）虛擬工程師 AI agent（ChipStack AI Super Agent 擴展版），結合 NVIDIA Nemotron 模型與 OpenShell runtime，宣稱可將典型五週的驗證流程縮短至一天內、RTL 驗證加速逾 40 倍；Level-5 自主能力預計 2026 下半年提供早期存取客戶。 | Cadence newsroom press release: 'Cadence Unveils Industry's First Fully Autonomous Virtual Engineer for Chip Design, powered by NVIDIA' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-unveils-industrys-first-fully-autonomous-virtual.html) | thesis.H,moat_trend |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "found",
  "queries_run": [
   "Cadence Design Systems acquisition merger 2025 2026",
   "Cadence completes acquisition Arm Artisan foundation IP business date 2025",
   "Cadence Secure-IC acquisition completed date 2025"
  ],
  "findings": [
   {
    "claim": "Cadence 完成收購 Hexagon 設計與工程（D&E）事業，約 €2.7B／$3.2B，2026-02-23 交割完成，預期 2026 年貢獻約 $160M 營收、非 GAAP EPS 稀釋約 28 美分（2027 年轉增益）。",
    "source": "Cadence newsroom: 'Cadence Completes Acquisition of Hexagon's Design and Engineering Business' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2026/cadence-completes-acquisition-of-hexagons-design-and-engineering.html)",
    "as_of": "2026-02-23",
    "direction": "0",
    "affects": [
     "thesis.H",
     "decision_inputs.bear",
     "moat_trend"
    ]
   },
   {
    "claim": "Cadence 收購 EMA Design Automation（PCB 設計領域），2026-03-05 完成，金額未揭露。",
    "source": "Tracxn deal brief: 'Cadence Acquires EMA' (tracxn.com/d/insights/merger-acquisition-deals-brief/cadence-acquires-ema/__2GFeel2DERN2Huua_VuEI8_1eWy4KiZTZGAH09AhLl4)",
    "as_of": "2026-03-05",
    "direction": "+",
    "affects": [
     "moat_trend"
    ]
   },
   {
    "claim": "Cadence 完成收購 Arm Artisan foundation IP 業務（標準元件庫/記憶體編譯器/GPIO），2025-08-27 交割，對 2025 年營收獲利影響不重大。",
    "source": "Cadence newsroom: 'Cadence Completes Acquisition of Arm Artisan Foundation IP Business' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-completes-acquisition-of-arm-artisan-foundation-ip.html)",
    "as_of": "2025-08-27",
    "direction": "+",
    "affects": [
     "moat_trend",
     "thesis.H"
    ]
   },
   {
    "claim": "Cadence 完成收購嵌入式資安 IP 廠商 Secure-IC，2025-11-03 交割。",
    "source": "Cadence newsroom: 'Cadence Completes Acquisition of Secure-IC' (cadence.com/en_US/home/company/newsroom/press-releases/pr/2025/cadence-completes-acquisition-of-secure-ic.html)",
    "as_of": "2025-11-03",
    "direction": "+",
    "affects": [
     "moat_trend"
    ]
   }
  ],
  "note": ""
 },
 "lawsuit_class_action": {
  "status": "none",
  "queries_run": [
   "Cadence Design Systems class action lawsuit securities fraud",
   "Cadence Design Systems shareholder derivative lawsuit export control settlement 2025"
  ],
  "findings": [],
  "note": "僅查得 1999 年（Spett v. Cadence，1999 Q1 財報相關，已被法院駁回）與 2008-2009 年（$38M 和解，2008 股價重挫相關）兩起歷史證券集體訴訟，均非近 12 個月事件；亦未查得因 2025-07 出口管制和解而起的股東衍生訴訟報導。"
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Cadence Design Systems acquisition merger 2025 2026",
   "Cadence Design Systems new product launch 2025 2026 AI chip design platform"
  ],
  "findings": [],
  "note": "非藥品/醫療器材業務（Cadence 為半導體電子設計自動化 EDA 軟體公司），已查證無相關臨床試驗/FDA 監管動作；上述查詢及其餘 6 條本輪搜尋亦均未出現任何臨床/FDA 相關訊息。"
 },
 "product_recall_warning": {
  "status": "none",
  "queries_run": [
   "Cadence Design Systems new product launch 2025 2026 AI chip design platform",
   "Cadence Design Systems acquisition merger 2025 2026"
  ],
  "findings": [],
  "note": "近 12 個月查得的產品相關新聞均為新品發表（ChipStack AI Super Agent／Level-5 自主虛擬工程師／ViraStack／InnoStack／AgentStack），未查得任何產品下架、召回或監管警告信事件。"
 },
 "sec_investigation_restatement": {
  "status": "found",
  "queries_run": [
   "Cadence Design Systems SEC investigation restatement China export",
   "Cadence Design Systems SEC subpoena investigation 2025 2026"
  ],
  "findings": [
   {
    "claim": "Cadence 因 2015-2021 年間對中國國防科技大學（NUDT，美國商務部 Entity List 上之中國軍方大學）銷售 EDA 軟硬體與 IP，遭美國 DOJ 與商務部 BIS 調查；2025-07-28 達成和解，母公司就一項共謀違反出口管制罪名認罪，DOJ 側罰金+沒收約 $117M（$72M 罰金＋$45M 沒收），另與 BIS 民事和解逾 $95M，對外揭露合計約 $140M（部分媒體引用淨額 $140.6M），並承諾三年緩刑期內強化出口合規與年度稽核。查無獨立的 SEC 會計調查或財報重編事件——此案主體機關為 DOJ／商務部 BIS，非 SEC，且不涉及財報重編，列於本欄位係因五分類中無獨立「出口管制執法」桶、性質最相近之政府調查/裁罰事件。",
    "source": "DOJ Office of Public Affairs: 'Cadence Design Systems Agrees to Plead Guilty and Pay Over $140 Million for Unlawfully Exporting Semiconductor Design Tools to a Restricted PRC Military University' (justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting); BIS press release (bis.gov/press-release/cadence-design-systems-pay-95-million-penalty-bis-unauthorized-exports-chinese-entities-tied-development)",
    "as_of": "2025-07-28",
    "direction": "-",
    "affects": [
     "thesis.R",
     "decision_inputs.bear",
     "moat_trend"
    ]
   }
  ],
  "note": "本條實為 DOJ/BIS 出口管制刑事+民事執法案件，非 SEC 證券監理調查、亦非財報重編；因五分類無專屬桶而歸類於此，判斷層引用時應正確標註機關與性質，不得誤寫為「SEC 調查」或「會計重編」。"
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_CDNS_20260504.html",
 "date": "20260504",
 "schema": "v12.3",
 "dca_verdict": null,
 "dca_role": null,
 "price_at_dd": 340.94,
 "revlog": {
  "status": "ok",
  "text": "版本修訂紀錄\n\n版本 | 日期 | 變更\nv12.2（Inception） | 2026-05-04 | CDNS 首次 v12.2 DD（Q1 26 4/27 Beat 後重新評估）。下次年度對照 2027-05-04。\nv12.3 upgrade | 2026-05-16 | Schema 升至 v12.3（win-20260516-1833-654b）。§9 護城河二維化（execution 8 / pricing power 9）；§5.F Single Thing 新增（Hyperscaler in-house Agentic EDA binary event）；§8.B 定價 vs 量拆分 + 有機/無機 3Y 趨勢；§8.H 客戶結構深度（top-5/10% + 關係類型 + 議價風險）；§11 議價權三段獨立（對上游 / 對下游 / 地緣）；§12 M&A 5Y track record + SBC 剔除 EPS CAGR 計算；§13.4 peer tier 修正（EDA Oligopoly，SNPS 唯一 anchor，移除誤引 AVGO 等）；§10 FCF lumpiness 新增；dd-meta schema → v12.3，stress → 2/2，moat_execution=8, moat_pricing_power=9；§2.E QC-29 4 情境表砍除；§13.0/13.3/13.5/§7 低估值四問砍除。Verdict 維持 A（§1 / §2 H / §13 三處一致）。"
 },
 "prior_meta": {
  "ticker": "CDNS",
  "company": "Cadence Design Systems",
  "date": "2026-05-04",
  "schema": "v12.3",
  "price_at_dd": 340.94,
  "currency": "USD",
  "signal": "A",
  "trap": "🟢",
  "trap_label": "非陷阱",
  "moat": "A",
  "moat_score": 9,
  "moat_execution": 8,
  "moat_pricing_power": 9,
  "val": "🟡",
  "ma": "✅",
  "benchmark_regime": "正常",
  "fpe_fy1": 43.16,
  "fpe_fy2": 35.89,
  "pct_5y": 53,
  "peg_3y": 1.86,
  "peg_fy2": 1.55,
  "rr_short": -0.39,
  "rr_mid": 0.2,
  "rr_long": 1.22,
  "target_short": 277,
  "target_mid": 361,
  "target_5y": 540,
  "upside_short_pct": -19,
  "upside_mid_pct": 6,
  "upside_5y_pct": 58,
  "stress": {
   "pass": 2,
   "total": 2
  },
  "growth_durability": 9,
  "quality_score": 9,
  "ai_risk": "🟢",
  "long_term_confidence": "高",
  "verdict": "A（核心候選·Q1 Beat + 上修 FY 指引 + Backlog 8B record 強化 thesis；4 週 +22% 接近警戒，等回測 BB 中軌 ~303）",
  "inception_dd": "DD_CDNS_20260504.html",
  "inception_date": "2026-05-04",
  "next_yoy_review": "2027-05-04",
  "oneliner": "Q1 26 Rev 1.47B(+19%)+EPS 1.96 Beat+OPM 44.7%+Backlog 8B／FY26 raised 6.12-6.22B EPS 7.85-7.95／護城河A EDA雙寡占+Agentic AI／FPE 36-43x PEG 1.55 估值🟡／MA✅但4w+22%／A 等回測303"
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
    "text": "EDA 雙寡占穩定，CDNS 維持 ~33% 市佔",
    "columns": {
     "Sourced Floor": "Backlog ≥ 7B 兩季（§6 Backlog $8B record，Q1 26 earnings call）；CDNS 市佔 33% 估算基於 Gartner/IDC EDA TAM $15B × Rev $5.3B",
     "2Y 驗證點": "Backlog 持續 ≥ 7B",
     "5Y 驗證點": "FY30 Rev 8-9B，CAGR 15%",
     "10Y 驗證點": "2036 Rev 12B+，雙寡占未被瓦解"
    }
   },
   {
    "id": "H2",
    "text": "AI Super Agent + Agentic AI 推動 ARR 從 ~80% → 90%（2030）",
    "columns": {
     "Sourced Floor": "ARR 基期 80% 估算來自 §8 訂閱模式說明；AgentStack 2025 發布（Cadence press release 2025）",
     "2Y 驗證點": "FY27 mgmt 揭露 AI 工具 ARR 佔比",
     "5Y 驗證點": "AI 工具占 Rev 30%+",
     "10Y 驗證點": "持續為 EDA 主要 ASP 驅動"
    }
   },
   {
    "id": "H3",
    "text": "Non-GAAP OPM 從 44% → 47% 擴張",
    "columns": {
     "Sourced Floor": "Q1 26 OPM 44.7% record（earnings release）；FY26 mgmt guide 43.5-44.5%；漂移觸發：連 2 季 OPM",
     "2Y 驗證點": "FY27 OPM ≥ 45%",
     "5Y 驗證點": "FY30 OPM 47%",
     "10Y 驗證點": "maintain 45%+"
    }
   }
  ]
 },
 "R": {
  "status": "unavailable"
 },
 "triggers": {
  "status": "unavailable"
 },
 "inception_dd": {
  "path": "docs/dd/DD_CDNS_20260504.html",
  "date": "20260504",
  "schema": "v12.3"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_CDNS_20260504.html",
  "date": "20260504",
  "days_from_365d_mark": 241
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "CDNS",
 "current_verdict": {
  "verdict": null,
  "fundamental_grade": "A",
  "date": "2026-05-04",
  "freshness": "aging",
  "source": "docs/dd/DD_CDNS_20260504.html"
 },
 "decision_history": [
  {
   "date": "2026-05-04",
   "verdict": null,
   "role": null,
   "price_at_decision": 340.94,
   "fundamental_grade": "A",
   "to_date_pct": -19.3,
   "days": 119,
   "source_report": "docs/dd/DD_CDNS_20260504.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/CDNS.md\n[internal-note] 2026-05-17  Cold Review — CDNS v12.3 品質稽核\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_v12_3_CDNS_20260517.md\n[dca] 2026-05-11  DCA|CDNS Cadence Design Systems|2026-05-11\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_CDNS_20260511.md\n[dca] 2026-05-07  DCA · CDNS · 2026-05-07\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_CDNS_20260507.md\n[dd] 2026-05-04  DD|CDNS Cadence Design Systems|2026-05-04\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_CDNS_20260504.md"
}
```

### canonical_id（原樣）
```json
{
 "status": "ok",
 "primary": {
  "theme": "AI EDA + IP",
  "path": "docs/id/ID_AIEDAIP_20260427.html",
  "skill_version": "v2.3",
  "as_of": "2026-04-27",
  "facts": {
   "status": "ok",
   "sections": {
    "supply": "PART III · SUPPLY SIDE\n 供給側：三寡占之上，多了一條 收費模式遷移 暗線\n EDA 的供給故事過去是「SNPS／CDNS／Siemens 三寡占誰工具強」；2025-26 起多了一條暗線——收費模式從 per-seat 跳 per-tapeout／token，把 EDA 廠的營收與 AI 晶片設計活動量直接綁定，同時 ARM 把 IP 從藍圖升級成子系統。\n\n 供給端是 Synopsys（龍頭，~31% 份額、併 Ansys 後寬口徑 ~44%）＋ Cadence（純 EDA pure play，~30%）＋ Siemens EDA（~13%）的三寡占，毛利集體高檔（CDNS non-GAAP op margin ~45%、SNPS 軟體業 GM 80%+）。瓶頸（對後進者而言）是三重鎖定：① foundry 強制簽核工具（Calibre／PrimeTime）；② 多年 ELA 與遷移成本（一顆先進晶片綁定整套工具鏈，換工具＝重跑驗證）；③ AI agent 平台的客戶 NRE lock-in。任一鬆動才可能破寡占，而三者 2026 全部 binding。這是賣方市場的結構基礎，也是「估值有支撐但有機增速要看模式兌現」的同一枚硬幣兩面。\n\n \n Inference · 供給\n 收費模式從 per-seat 跳 per-tapeout／token，把 EDA 的成長天花板拆掉\n 前提：AgentEngineer／AgentStack early-access（H2 2026）＋ Synopsys 續約 ~20% 漲價靠 token ＋ Cerebrus 消費型 SaaS ＋ AI ASIC／chiplet 推升 tapeout 量\n 當收費基底從「設計師人頭」變成「設計活動量」，EDA 營收第一次與 AI 晶片被設計出來的數量直接掛鉤——一個團隊跑更多 AI agent、更多 tapeout＝付更多錢，而不再被「客戶招幾個工程師」封頂。這把 2000 式「下游晶片投資放緩 → EDA 訂單跟著崩」的劇本變難複製（短期靠 backlog 與 ELA 緩衝），同時打開「使用量隨 AI 設計爆發非線性成長」的新天花板。\n 可證偽條件：若 2026-2027 續約漲幅回落至個位數、Synopsys 有機核心 EDA 增速連兩季 &lt; +8%、AI 工具的 token／消費型營收占比不見上升，則「收費模式重定價」只是行銷話術而非定價權，estimate 與估值都要下修——這正是 PART I 監測點 1 的設計理由。\n \n\n \n 利潤池遷移 · 毛利率／成長為各家最新季 T1 實際值 / 區間\n \n環節 | 代表玩家 / 體質 | 遷移 | 搶 / 被搶\nEDA 工具（雙寡占） | SNPS ~31% / CDNS ~30% 份額 | ↑ | AI 工具＋multiphysics 拉高 wallet share\nEDA AI 平台（新層） | AgentStack / AgentEngineer（消費型） | ↑ | 新環節，per-tapeout／token 重定價\nIP 授權（CSS 升級） | ARM CSS royalty rate ~10%（v9 兩倍） | ↑ | 從「賣藍圖」搶到「賣子系統」溢價\n連結 IP（chiplet/SerDes） | Alphawave（已併入 QCOM 2025-12） | ↑ | 224G/UCIe 被高通整併進資料中心\n實體驗證簽核（鎖喉） | Siemens Calibre ~85%+（foundry 強制） | → | 結構性 tenure，難被替代\nAI 晶片設計（買方） | NVDA / AVGO / hyperscaler ASIC | ↓ | EDA/IP 是 COGS；自研設計反壓 IP 議價\n\n \n 怎麼讀：利潤往「EDA 雙寡占＋ARM IP」集中（同享高檔毛利且都在 ↑），但 2025 起出現兩條新分支——EDA AI 平台層把收費從人頭重定價成活動量、ARM CSS把 IP 從藍圖升級成子系統。binary 競爭軸：Synopsys 用 Ansys 開 multiphysics 全 stack 護城河（Cadence／Siemens 落後 18-24 月）vs Cadence 用 AgentStack＋NVIDIA Nemotron 拼 agentic 自動化速度。誰能把「按使用量收費」坐實成定價權，誰就拿到下一輪 wallet share——這是「EDA 從 per-seat 變 per-activity」的供給側證據。對 Siemens Calibre 而言是 small-but-permanent 的 foundry tenure（簽核鎖喉），但非成長主軸。",
    "demand": "PART IV · DEMAND SIDE\n 需求側：AI tapeout 爆發是真的，capex 增速減速也是真的\n 最不可替代的是 hyperscaler 自研 ASIC 與 chiplet 拼接帶來的 tapeout 與 IP 用量爆發（一顆先進 ASIC 的 EDA＋IP 投資從 $50-200M 飛到 $400-600M+）；最脆弱的是「AI capex 持續加速」這個前置訂單邏輯的隱含假設。\n\n 需求源頭是 AI 晶片設計活動：hyperscaler（AWS Graviton／Google Axion／MSFT Cobalt／Meta MTIA）大規模自研 ASIC，疊加 NVDA／AMD 每代加速器，把每顆先進晶片的 EDA＋IP 投資從 2020 的 ~$50-200M（單晶片）推到 2026 的 ~$200-400M（chiplet 跨代拼接），2028+ 同代雙拼 ~$400-600M——這不是「漲價」，是 chiplet 拼接讓每個 chip 的設計／驗證／整合量乘倍。下游出錢方是四大 hyperscaler，2026 AI capex 合計約 $725B。需求廣度（NVDA＋AMD＋hyperscaler ASIC＋主權 AI）稀釋了單一買家放緩的傳導，但增速本身在減速，且大客戶自研設計能力反向壓 IP 議價（AVGO 等 ASIC 大戶內製設計）——這是裁決從純「結構性多」打成「賣方市場但有 kill 未排除」的根源。\n\n \n 需求三角驗證 · top-down vs bottom-up 對帳（口徑不同，量級判斷）\n \n視角 | 數值 | 口徑 / 來源\n下游 AI capex（top-down） | 四大 ~$725B（2026） | 各家曆年 guidance 聚合（個別法說 T1）\nEDA+IP TAM（中游加總） | 純 EDA ~$18B(2025) → ~$28-31B(2030) | SemiAnalysis / 市研機構，CAGR ~8-11%（純 EDA）\n三家頭部 run-rate（bottom-up） | SNPS FY26 ~$9.7B / CDNS ~$6.2B / ARM ~$5B+ | 全公司 rev（含 Ansys／IP／系統），非純 EDA-only\n\n \n 怎麼讀：三家全公司 run-rate（~$21B）大於純 EDA TAM（~$18B）——缺口來自口徑（含 Ansys simulation／IP／系統設計／emulation 硬體），&gt;20% 差異已由「寬 vs 窄口徑」解釋，採信窄口徑純 EDA 算份額、寬口徑算 TAM 上限。真正要對帳的是「capex $725B 能不能持續」——EDA 的 tapeout 用量建立在 AI 設計活動持續爆發上；若 2027 capex 增速顯著降檔甚至反轉，tapeout 量會延後 6-12 個月傳導、續約漲幅與 token 收入都會被重談。短期採信下游 capex（法說承諾最硬＋backlog $8B 鎖死），但這是「採信」不是「確定」。\n\n \n Inference · 需求\n backlog 把短期鎖死，但鎖的是「合約量」不是「續約定價權」\n 前提：CDNS backlog $8B（覆蓋 FY26 rev ~67%）＋ 多年 ELA ＋ hyperscaler 2026 AI capex ~$725B（高基期）但 2027 預期增速降檔 ＋ 大客戶內製設計\n backlog 與多年 ELA 讓 2026-2027 的營收底幾乎是確定事件（合約量已綁），這是 12M 裁決「賣方市場」的硬底。但 backlog 的續約定價假設客戶會持續加碼 tapeout 與 AI 工具用量；一旦 capex 增速反轉或大客戶把設計能力內製，2027-28 的續約漲幅與 token 收入就是談判變數，而非保證。\n 可證偽條件：① 任一 Big-4 hyperscaler 宣布 2027 AI capex YoY 跌破 +20% 甚至負增長；② AVGO／hyperscaler 把更多 IP／設計流程內製、壓 ARM/Synopsys IP 議價；③ 續約出現實質降價或 ELA 縮表。任一發生，「backlog 保護」由緩衝變裂縫。\n \n\n \n 多空為何都對\n 多頭測的是賣方市場黏性（backlog $8B、遷移成本、licensing +29%），空頭測的是定價權兌現與 capex 增速（收費模式能否坐實、AI ROI、capex 能否續加速）——兩者測的不是同一件事，可同時為真：EDA/IP 確實被多年 ELA 鎖死（多頭對），但鎖死不代表續約能永遠雙位數漲價（空頭對）。本報告因此把判斷重心放在「收費模式能否兌現定價權、capex 何時減速」，而非「EDA 估值貴不貴 yes/no」。"
   }
  },
  "machine": {
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "priced_in": null,
   "conviction": "high",
   "for_stage2_only": true
  }
 },
 "candidates": [
  {
   "theme": "AI EDA + IP",
   "path": "docs/id/ID_AIEDAIP_20260427.html",
   "skill_version": "v2.3",
   "as_of": "2026-04-27",
   "sd_verdict": "shortage",
   "clock_phase": "II",
   "conviction": "high",
   "priced_in": null,
   "for_stage2_only": true
  }
 ],
 "note": null
}
```


---

## ④ 最新一季逐字稿全文

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/CDNS/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
  ],
  "items": [
    {
      "topic": "guidance",
      "claim": "CEO announces the company is raising its full-year 2025 outlook to approximately 14% revenue growth and 18% EPS growth.",
      "quote": "raising our full year outlook to approximately 14%",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives Q4 2025 revenue guidance range.",
      "quote": "revenue in the range of $1.405 billion to $1.435 billion",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO gives updated full-year 2025 revenue guidance range.",
      "quote": "revenue in the range of $5.262 billion and $5.292 billion",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO explicitly declines to give FY2026 guidance on this call, deferring to a later date.",
      "quote": "we won't guide FY '26 today",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "margin",
      "claim": "CFO gives updated full-year 2025 GAAP operating margin guidance range.",
      "quote": "GAAP operating margin in the range of 27.9% to 28.9%.",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "margin",
      "claim": "CFO states Q3 2025 actual GAAP operating margin.",
      "quote": "GAAP operating margin was 31.8%",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "margin",
      "claim": "CFO explains Q4 opex is partly offset by new expenses from recently closed acquisitions.",
      "quote": "offset a little in Q4 by some new expenses",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "competition",
      "claim": "Analyst asks how Cadence's strong IP growth squares with a competitor's publicly expressed concerns about its own IP business.",
      "quote": "because your competitor expressed",
      "speaker": "Vivek Arya (Analyst, BofA Securities)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "competition",
      "claim": "CEO argues Cadence's IP business is more profitable than the general IP industry, differentiating it from competitors.",
      "quote": "I think it's much more profitable",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "customer",
      "claim": "CEO cites Q3 expansion of the Samsung partnership across core EDA and system software.",
      "quote": "we meaningfully expanded our partnership with Samsung",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "customer",
      "claim": "CEO cites deepened collaboration with OpenAI on the Palladium emulation platform in Q3.",
      "quote": "We deepened our overall collaboration with OpenAI",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "product",
      "claim": "CEO cites Samsung's SF2 tape-out using Cadence Cerebrus AI Studio as a customer productivity win.",
      "quote": "Samsung U.S. taped out a SF2 design using Cadence Cerebrus",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "product",
      "claim": "CEO cites customer-reported verification throughput gains from Verisium SimAI, highlighted by NVIDIA, Samsung and Qualcomm at CadenceLIVE India.",
      "quote": "5x to 10x improvement in verification throughput",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "risk",
      "claim": "CFO states the 2025 outlook assumes today's export control regulations remain substantially similar for the rest of the year.",
      "quote": "export control regulations that exist today remain",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "risk",
      "claim": "When asked about China tariff-related risk to guidance, CFO says reports suggest geopolitical tensions are lower than commonly expected.",
      "quote": "geopolitical tensions are lower than people expect",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO states Q3 2025 share repurchase amount.",
      "quote": "we used $200 million to repurchase Cadence shares",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO confirms the definitive agreement to acquire Hexagon's D&E business, including its MSC Software unit.",
      "quote": "signed a definitive agreement to acquire Hexagon's D&E",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO reiterates the 2025 outlook includes using at least 50% of annual free cash flow for buybacks.",
      "quote": "our annual free cash flow to repurchase Cadence shares",
      "speaker": "John Wall (CFO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO states the combined SD&A business run rate should cross $1 billion in 2026 once the Hexagon acquisition closes.",
      "quote": "$1 billion in 2026 if the acquisition closes.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO states he would be surprised if the IP business does not grow faster than the corporate average given its profitability profile.",
      "quote": "our IP business does not grow better than Cadence average",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-10-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO John Wall 給出 2026 全年營收指引區間。",
      "quote": "revenue in the range of $5.9 billion to $6 billion",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO John Wall 給出 Q1 2026 營收指引區間。",
      "quote": "revenue in the range of $1.420 billion to $1.460 billion",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO John Wall 表示 2026 財年經常性營收佔比預期維持在約 80%，與 2025 一致。",
      "quote": "recurring revenue mix to remain around 80% in fiscal '26",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "margin",
      "claim": "CFO John Wall 引用 2025 年實現的增量營益率數字。",
      "quote": "we achieved incremental margin of 59%, I think",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "margin",
      "claim": "CFO John Wall 給出 2026 年非 GAAP 營業利益率指引區間。",
      "quote": "non-GAAP operating margin in the range of 44.75% to 45.75%",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "risk",
      "claim": "CEO Anirudh Devgan 回應分析師關於客戶用 AI 取代 EDA/IP 工具的疑慮，表示沒有看到客戶減少使用的討論。",
      "quote": "no discussion with customers of reducing the usage",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "risk",
      "claim": "CFO John Wall 說明 2026 指引已內建的假設：出口管制法規維持與現況大致相同。",
      "quote": "export control regulations that exist today remain",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "risk",
      "claim": "CFO John Wall 給出 2026 年中國營收佔比預期區間，與過去兩年相近。",
      "quote": "expect it will be in a similar range, 12% to 13% for 2026",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "competition",
      "claim": "CEO Anirudh Devgan 回應對新創公司的看法，強調對自身研發團隊的信心。",
      "quote": "we are very confident in our own R&D",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "competition",
      "claim": "CEO Anirudh Devgan 表示公司在多個產品線的競爭地位有所改善。",
      "quote": "our competitive position has improved",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "competition",
      "claim": "CEO Anirudh Devgan 表示公司在硬體、IP 等多個主要產品線都在取得市佔率。",
      "quote": "we are taking share in all our major product segments",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "product",
      "claim": "CEO Anirudh Devgan 描述 ChipStack AI Super Agent 帶來的生產力提升幅度。",
      "quote": "provides up to 10x productivity improvement",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "product",
      "claim": "CEO Anirudh Devgan 描述 3D-IC 平台在多晶片架構轉型中的角色。",
      "quote": "a key enabler for the industry's transition to multichip",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "customer",
      "claim": "CEO Anirudh Devgan 列舉 ChipStack 已獲得的客戶背書名單。",
      "quote": "endorsements from Qualcomm, NVIDIA, Altera and Tenstorrent",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "customer",
      "claim": "CEO Anirudh Devgan 引用 Samsung U.S. 使用 Cadence Cerebrus AI Studio 流出 SF2 設計的生產力成果。",
      "quote": "achieving 4x productivity improvement",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "customer",
      "claim": "CEO Anirudh Devgan 引用一家大型跨國電子暨電動車客戶使用 AI 驅動設計遷移得到的佈局效率成果。",
      "quote": "reported a 30% layout efficiency gain",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO John Wall 給出 2026 年自由現金流用於庫藏股回購的預期比例。",
      "quote": "of our free cash flow to repurchase Cadence shares in 2026",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO John Wall 陳述 2025 全年實際用於庫藏股回購的金額。",
      "quote": "used $925 million to repurchase Cadence shares",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO Anirudh Devgan 陳述 2026 年開年時的在手訂單積壓（backlog）金額創新高。",
      "quote": "we began 2026 with a record backlog of $7.8 billion",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO John Wall 揭露 2026 年營收中來自期初在手訂單積壓的占比透明度指標。",
      "quote": "around 67% of 2026 revenue is coming from beginning backlog",
      "speaker": "CFO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO Anirudh Devgan 回應分析師關於 AI 時代合約年期是否會像 2000 年代那樣縮短的提問，表示目前未見合約年期變化。",
      "quote": "not seeing any change in the duration, so which is good",
      "speaker": "CEO",
      "date": "2026-02-17",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO 表示上修 2026 全年營收成長展望至 17%",
      "quote": "raising our 2026 revenue growth outlook to 17%",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 給出 2026 全年營收區間指引",
      "quote": "$6.125 billion to $6.225 billion",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 給出 2026 全年 Non-GAAP 營益率指引區間",
      "quote": "Non-GAAP operating margin in the range of 43.5% to 44.5%.",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 說明 Hexagon 併購對 2026 EPS 造成稀釋",
      "quote": "We expect it to be dilutive to the tune of about $0.28.",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 說明近期有機成長的邊際利潤率水準",
      "quote": "closer to 60% these days than 50%.",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 針對 AI 是否威脅 EDA 基礎工具可防禦性，表態對自身基礎工具地位有信心",
      "quote": "very confident in our position in the base tool",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "competition",
      "claim": "CEO 評論基礎工具的競爭地位仍屬業界最佳",
      "quote": "our competitor of the base tool is anyway best-in-class",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "product",
      "claim": "CEO 說明新推出的三個 AI Super Agent（含 ChipStack）串連整個晶片設計流程",
      "quote": "Together, these solutions span the entire chip design flow",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "product",
      "claim": "CEO 介紹 AgentStack 作為 AI Super Agent 的頭部代理框架",
      "quote": "AgentStack, the head agent framework for our AI Super Agent",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 提及與某全球晶圓代工大廠簽下 IP 業務史上最大單一合約",
      "quote": "closed a record deal with a leading global foundry",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 提及某半導體設計大廠大幅增加 Innovus 用量",
      "quote": "significantly increased their Innovus usage",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "customer",
      "claim": "CEO 提及一家指標型 AI 基礎設施公司擴大採用簽核解決方案",
      "quote": "a marquee AI infrastructure company expanded their usage",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 指出 2026 財測假設出口管制法規維持現狀不變",
      "quote": "export control regulations that exist today remain",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 說明中國占 Q1 營收比重及全年預期",
      "quote": "China, it was 13% of Q1 revenue",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 揭露 Q1 已動用 2 億美元庫藏股回購",
      "quote": "we used $200 million to repurchase Cadence shares",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 指引 2026 全年約用 50% 自由現金流回購股票",
      "quote": "approximately 50% of our free cash flow to repurchase",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO 說明 Hexagon 收購的股票/現金支付結構",
      "quote": "we paid 30% of the acquisition price in shares and 70%",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO 預期 Hexagon 併購案將於 2027 年轉為增益",
      "quote": "We'd expect it to be accretive in 2027.",
      "speaker": "John Wall, CFO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO 承諾 2030 年前推出下一代硬體平台 Z4",
      "quote": "we'll have a Z4 system before 2030.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2026-04-27",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 稱對 2026 年的能見度與過去持平或更好，過去在軟體端一向能見度較強",
      "quote": "as good, if not better than what we've had before.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 稱過去 3-5 年平均營收成長約 14%，其中約 2% 來自併購、12% 為有機成長",
      "quote": "we've probably been averaging around 14% revenue growth",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "guidance",
      "claim": "CFO 稱公司通常以兩位數成長編列預算，實際結果常落在低雙位數(low teens)",
      "quote": "we budget for double-digit revenue growth",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 稱有機業務目標為 50% 以上增量利潤率，實際約達 60%",
      "quote": "We're probably hitting 60% organically.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 稱 2024 年未達成 50% 增量利潤率目標，原因是 BETA 併購太晚導致時間不足",
      "quote": "in 2024, we missed that 50% incremental margin target",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "margin",
      "claim": "CFO 稱若合併看 2024-2025 兩年，增量利潤率約落在公司長期平均的 53%-54%",
      "quote": "you're probably getting incremental margin of about 53%, which is kind of 53%, 54%",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 稱 MSC（自 Hexagon 拆分之 Design and Engineering 業務）獨立年收入約 2.8 億美元",
      "quote": "I think they were doing about $280 million of revenue stand-alone",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 稱若將 MSC 多年合約全部轉為年約，年化營收約 2 億美元",
      "quote": "probably a run rate of about $200 million a year",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 稱 MSC 併購後需 12-15 個月萃取綜效",
      "quote": "it will take us 12 to 15 months to extract those",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO 稱 MSC 是公司歷來最大的一筆併購案，未來 1-2 年 M&A 重心將放在整合 MSC，其餘僅為小型 tuck-in",
      "quote": "MSC is the biggest thing we've probably ever done",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "product",
      "claim": "CFO 稱硬體模擬更新周期仍處早期階段，因設計複雜度大增使硬體模擬更關鍵",
      "quote": "it still feels like early innings because everything has become so much more complex",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "product",
      "claim": "CFO 稱硬體需求強勁，客戶即使拿不到 Z3 也會要求 Z2 系統",
      "quote": "Customers are asking for our Z2s if we can't get them to Z3.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "product",
      "claim": "CFO 稱硬體交期目標落在 8 到 22 週之間，目前落在中段位置",
      "quote": "We tried to aim for somewhere between 8 and 22 weeks of lead time.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "customer",
      "claim": "CFO 稱與台積電關係一向很強，近期在三星、英特爾的合作明顯增加",
      "quote": "we're very, very strong at TSMC, but we've been increasingly engaged in places like Samsung and Intel",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "customer",
      "claim": "CFO 稱非 AI 半導體客戶今年出現較大型合作案，似已觸底",
      "quote": "this year, we're seeing bigger engagements and I think they've probably found their base now at this point",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "customer",
      "claim": "CFO 稱對中國客戶需求韌性感到意外，限制鬆綁後客戶急欲拿到硬體積壓訂單",
      "quote": "we're surprised with the resilience of China customers",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 稱中國缺乏先進製程帶來的 AI 拉動效應，預期未來 3-5 年成長率略低於公司平均",
      "quote": "we don't see the same AI pull-through there as we're seeing in other regions",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "risk",
      "claim": "CFO 稱優先出貨中國硬體積壓訂單，使 Q3、Q4 末硬體積壓中中國占比將明顯低於平常",
      "quote": "there'll be much less of a percentage of China in it than there normally is",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "competition",
      "claim": "CFO 稱觀察到競爭對手 Synopsys 近年在 IP 業務上作風變得更偏交易型",
      "quote": "Synopsys maybe over the last few years have become more transactional",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "competition",
      "claim": "CFO 稱客戶不想被 Synopsys 或 ARM 綁死，希望有更多 IP 選擇，預期公司在 IP 市場競爭將隨業務下推而增加",
      "quote": "there'll probably be more competition from us",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO 稱公司在 IP 業務上採長期夥伴模式，自稱是「農夫不是獵人」",
      "quote": "We're farmers, not hunters.",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "commitment",
      "claim": "CFO 稱回測過去十年，僅一年 Q4 訂單量未超過 Q4 營收，本季度延續強勁開局，預期將以創紀錄的積壓訂單收尾今年",
      "quote": "there's only 1 year where Q4 bookings didn't exceed Q4 revenue",
      "speaker": "John Wall",
      "date": "2025-11-18",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO confirms record backlog reported at end of Q3.",
      "quote": "We had record backlog.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO says all indications point to Q4 ending with another record backlog.",
      "quote": "that we should end up with another record",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states current-year revenue growth is 14%, framed as a combined growth+margin \"rule of 58%\".",
      "quote": "revenue growth is 14%, okay? So that's a rule of 58%.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "margin",
      "claim": "CEO says the company has raised margin every year for the past 5-10 years and expects to keep doing so.",
      "quote": "increased margin every year for the last 5, 10 years",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "margin",
      "claim": "CEO flags that 2026 incremental margin may run lower before accelerating in 2027.",
      "quote": "in '26. Our incremental margin is a little lower, but '27",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO states the company continues to target 50%+ incremental margin.",
      "quote": "we are always shooting for 50% plus incremental margin.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO states the buyback is sized to ensure no net dilution from stock-based comp.",
      "quote": "we want to make sure that there is no dilution",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO reiterates the company returns 50% of cash flow to buy back stock.",
      "quote": "We will take 50% of our cash flow and we buy back our stock",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO says remaining cash may go to opportunistic M&A but the financial model is unchanged.",
      "quote": "it does not change our model, which we have done",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "competition",
      "claim": "CEO responds to the Synopsys-Ansys deal by saying Cadence already competes with them separately.",
      "quote": "already competing with them separately.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "competition",
      "claim": "CEO says the system business has grown roughly 25% a year for the last 5-6 years, pointing to the silicon-system merger thesis he pursued since 2018.",
      "quote": "our system business has grown like, I don't know, 25% a year",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "product",
      "claim": "CEO says applying AI to Cadence's own products can deliver at least 10x productivity improvement.",
      "quote": "there's at least 10x productivity improvement we can deliver",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes the Palladium hardware-software emulation systems as core to modern chip design.",
      "quote": "Palladium and these hardware systems became basically",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "product",
      "claim": "CEO says the emulator verifies chip designs roughly 1,000x faster than regular silicon.",
      "quote": "it will verify the design like 1,000x faster",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "product",
      "claim": "CEO says IP segment is performing well across all reported areas.",
      "quote": "IP is performing well.",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "customer",
      "claim": "CEO says roughly 45% of business now comes from system companies rather than traditional semiconductor customers.",
      "quote": "business is coming from system companies",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "customer",
      "claim": "CEO says China's share of EDA/software business has declined from about 16-17% a few years ago to about 11-12% now.",
      "quote": "Now it's like 11%, 12%. Still good",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "risk",
      "claim": "CEO says some China business shifted from Q2 to Q3 this year due to restrictions, now resolved.",
      "quote": "some of our business moved from Q2",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "risk",
      "claim": "CEO says geopolitical conditions are hard to predict but currently look stable for China design activity.",
      "quote": "geopolitical, but seems stable for now",
      "speaker": "Anirudh Devgan, CEO",
      "date": "2025-12-02",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_UBS_Global_Technology_and_AI_Conference_2025_20251202.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO says China revenue came in better than the earlier prudent 'flat' guide, growing this year instead.",
      "quote": "China is growing this year, which is good.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO gives China's current share of total revenue and notes it is down from a few years ago.",
      "quote": "China will be in 11%, 12% of revenue",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO states last year's revenue growth rate while discussing the growth+margin 'rule of X' framework.",
      "quote": "our revenue growth last year is 14%.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states this year's operating margin figure.",
      "quote": "our operating margin. This year is about 44.5%",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "margin",
      "claim": "CEO defines 'real margin' as operating margin minus stock-based compensation.",
      "quote": "real margin is, of course, operating margin minus SBC.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states incremental margin on the organic business.",
      "quote": "incremental margin on our organic business is close to 60%.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "margin",
      "claim": "CEO restates the company's long-standing incremental margin goal.",
      "quote": "our goal, of course, is a 50% plus incremental margin",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO says buybacks funded by cash flow exceed the SBC percentage, aimed at avoiding dilution.",
      "quote": "So if we do like 8%, 9% SBC, we buy back more than that.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO states the primary strategic rationale for the Hexagon acquisition.",
      "quote": "the reason for Hexagon was, is primarily for physical AI.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes the acquired Hexagon simulation asset as the market leader in multibody dynamics simulation.",
      "quote": "the best multibody dynamic simulator, #1 in the market.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "product",
      "claim": "CEO says Cadence now has all five key advanced-node IP categories (UCIe, HBM, DDR, PCIe, SerDes).",
      "quote": "we have all the 5 key IPs at the most advanced nodes.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "competition",
      "claim": "Analyst references a recent stumble by a rival IP vendor as context for the question on Cadence's IP positioning.",
      "quote": "misstep perhaps with a rival recently in this space",
      "speaker": "Unknown Analyst",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "competition",
      "claim": "CEO characterizes the NVIDIA business relationship as expanding.",
      "quote": "our business with NVIDIA is growing.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "competition",
      "claim": "Analyst asks about a reported nonexclusive collaboration deal between NVIDIA and Synopsys.",
      "quote": "a nonexclusive deal done or collaboration with Synopsys",
      "speaker": "Unknown Analyst",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "risk",
      "claim": "CEO acknowledges Cadence was subject to a China-related export ban lasting six weeks during the year.",
      "quote": "we were banned for 6 weeks and all that.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "risk",
      "claim": "CEO notes a quarter-to-quarter revenue timing shift tied to the China situation.",
      "quote": "some revenue moved from Q2 to Q3.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "customer",
      "claim": "CEO gives the current split of customers between system companies and semiconductor companies.",
      "quote": "about 45% of our customers are now system companies",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "customer",
      "claim": "CEO states the concentration of revenue among a small set of large customers.",
      "quote": "70% of revenue is coming from about 60 companies",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO commits to a systems business run-rate target, conditioned on M&A closing.",
      "quote": "we will cross like $1 billion run rate in systems",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO commits that no future M&A will be allowed to undermine the company's margin-expansion financial model.",
      "quote": "we'll not do any M&A that destroy this fundamental financial",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "risk",
      "claim": "Analyst raises margin pressure from the shift to annual subscriptions in the SD&A (systems) business as a topic needing explanation.",
      "quote": "a little bit of margin pressure as you transition to annual",
      "speaker": "Unknown Analyst",
      "date": "2025-12-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "topic": "product",
      "claim": "CEO 把 ChipStack Super Agent 定位為全新產品類別，非既有 GenAI 工具延伸",
      "quote": "This is a new product category, okay?",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "product",
      "claim": "ChipStack 首次讓公司具備自動寫 RTL 與 test bench 的能力，過去從未做到",
      "quote": "we have never done is ability to write RTL or test bench",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "product",
      "claim": "Hexagon 併購帶來最準確的機器人模擬器 Adams，用來補強 physical AI 的 sim-to-real 精度",
      "quote": "Hexagon had the most accurate robotic simulator with Adams",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "product",
      "claim": "CEO 說 physical AI 用的矽（車用、機器人）與 data center AI 用的矽不同，偏混合訊號與低功耗",
      "quote": "physical AI is different than the silicon for data center AI",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "去年整體營收成長約 14%、EPS 成長約 20%",
      "quote": "we grew like 14% and EPS grew around 20%, right?",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "margin",
      "claim": "公司近年 Rule of 40 落在高 50 幾，CEO 的目標是要突破 60",
      "quote": "we are in the high 50s, right, last few years",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "margin",
      "claim": "CEO 明確設定目標：Rule of 40 要跨越 60 這個門檻",
      "quote": "my goal is to crack 60.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "margin",
      "claim": "去年營業利益率 45%，但增量利潤率達 59%，即多增 1 億營收可多賺 5,900 萬利潤",
      "quote": "our margin last year was 45%, but incremental margin was 59%",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Hexagon 併購今年對財務有影響，但主要落在融資面（稀釋/新增債務）而非營運面",
      "quote": "it is on financing side because there is some dilution",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO 預期 Hexagon 併購明年就能轉為加值（accretive）",
      "quote": "And next year, it should be accretive.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "HBM IP 是透過向 Rambus 收購取得，CEO 稱是一筆好收購",
      "quote": "we did acquire from Rambus. That's a great acquisition.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "customer",
      "claim": "除既有大型半導體客戶外，Tesla、Rivian、BYD 等 OEM 廠自研晶片也成為客戶",
      "quote": "now with OEM players like Tesla and Rivian or BYD",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "customer",
      "claim": "中國今年設計活動熱絡、physical AI 需求大，環境比去年初更穩定",
      "quote": "the environment seems more stable than beginning of '25",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "competition",
      "claim": "面對中國本土 EDA 業者競爭，CEO 稱一直都有競爭",
      "quote": "there's always some competition, I think.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "product",
      "claim": "Palladium 硬體事業已連續 6 年寫下創紀錄成長",
      "quote": "we have like 6 years in a row of record growth in Palladium",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "risk",
      "claim": "CEO 對今年 Palladium 展望偏樂觀，但公司年初給假設時一貫採取保守態度",
      "quote": "we are more prudent in the assumption",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "risk",
      "claim": "針對 AI 是否顛覆傳統軟體商業模式的疑慮，CEO 回應這是放大而非顛覆",
      "quote": "for us, it's not disruption, it is amplification",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "commitment",
      "claim": "Agentic EDA（ChipStack）貨幣化模式將採 token-based 計費",
      "quote": "yes, I think it will be token-based",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "commitment",
      "claim": "公司希望新 agent 產品採基礎訂閱費加 token 用量的計費結構",
      "quote": "we would hope to have a base subscription plus tokens",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO 表示 IP 業務已是連續第三年強勁成長，且公司不會提前宣稱未驗證的趨勢",
      "quote": "it's the third year of very good growth we will have",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-03-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Morgan_Stanley_Technology_20260304.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO states Cadence sets guidance one year at a time and characterizes the current year as very strong.",
      "quote": "we guide 1 year at a time.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states Cadence crossed the 'Rule of 60' this year.",
      "quote": "We crossed the rule of 60 this year.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "margin",
      "claim": "CEO cites Cadence's incremental margin at 60%.",
      "quote": "Our incremental margin was 60%, okay?",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states operating margin is roughly 44-45%, contrasted with the higher 60% incremental margin.",
      "quote": "our operating margin is about 44%, 45%",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "competition",
      "claim": "CEO asserts Cadence leads in both agentic AI tools and base EDA.",
      "quote": "Agentic, we are ahead. Base EDA, we are ahead.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "competition",
      "claim": "CEO states Cadence is taking market share in IP.",
      "quote": "IP, we are taking share.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "competition",
      "claim": "CEO describes Cadence's overall competitive position as the best it has ever been.",
      "quote": "we are in the best position we have ever been.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes focus on building the best 'super agents' across the ChipStack, ViraStack, and InnoStack product lines.",
      "quote": "super agents for ChipStack, ViraStack, this is InnoStack",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "product",
      "claim": "CEO cites Palladium as a unique hardware platform in Cadence's portfolio.",
      "quote": "Hardware, we have a unique platform with Palladium.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "product",
      "claim": "CEO quantifies internal AI-driven productivity target as at least 30% headcount reduction per project.",
      "quote": "at least 30% reduction in headcount per project",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "customer",
      "claim": "CEO describes customer concentration: roughly 60-70 large companies drive 60-70% of Cadence's revenue.",
      "quote": "big 60, 70 companies that drive 60%, 70% of our revenue.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "customer",
      "claim": "CEO references NVIDIA's Jensen Huang publicly discussing Cadence at COMPUTEX.",
      "quote": "Jensen talked about Cadence at COMPUTEX.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "risk",
      "claim": "CEO acknowledges the physical AI/robotics market trajectory could still move either direction.",
      "quote": "This may correct, may not correct.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "risk",
      "claim": "CEO states the exact timing of physical AI market adoption is hard to predict.",
      "quote": "exact timing is very difficult to say",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO commits to continued hiring in the IP group despite AI-driven productivity gains reducing per-person headcount need.",
      "quote": "we will hire more, but they should be at least.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO sets an internal target of at least 2x productivity improvement in the IP R&D group from applying agentic AI.",
      "quote": "I am expecting at least a 2x productivity from the IP group.",
      "speaker": "Anirudh Devgan (CEO)",
      "date": "2026-06-03",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "topic": "guidance",
      "claim": "管理層說今年營收成長已加速到 17% YoY。",
      "quote": "the revenue has accelerated to 17% year-over-year growth",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "margin",
      "claim": "管理層說 non-GAAP 營業利益率將推升至 44%。",
      "quote": "op margin is going to push and reach 44%",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "margin",
      "claim": "管理層說今年將超越 Rule of 60，是公司歷史紀錄。",
      "quote": "exceeding the Rule of 60 this year",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "margin",
      "claim": "管理層重申目標是遞增利潤率北向 50%（含 -- 停頓語氣）。",
      "quote": "drive 50% -- north of 50% incremental margin, okay?",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "competition",
      "claim": "管理層說公司在各業務線都在全面搶市占。",
      "quote": "We are gaining share across the board.",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "competition",
      "claim": "管理層說公司目前是公司史上競爭力最強的時期。",
      "quote": "We're the strongest ever in our company history.",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "product",
      "claim": "管理層說 IP 策略聚焦在他們稱為「star IP」的高價值高成長 IP。",
      "quote": "we call it star IP, the high-value, high-growth IP",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "product",
      "claim": "管理層說過去幾個月已推出 3-4 個 super agent（agentic AI 產品）。",
      "quote": "3 or 4 super agents launched in the past couple of months",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "customer",
      "claim": "管理層說前 60-70 大客戶約占公司多數營收（60%-70%）。",
      "quote": "our top, say, 60, 70 customers, which is maybe a majority",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "customer",
      "claim": "管理層提到前一天剛宣布與 Intel 在 14A 製程上的合作。",
      "quote": "collaborate with Intel on its 14A journey yesterday",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "管理層說資本配置哲學一貫是有機投資優先。",
      "quote": "organic is the first order of business, okay?",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "管理層說要持續將自由現金流的 50% 以上用於股票回購。",
      "quote": "more than 50% of the free cash flow for share repurchases",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "管理層說不做大型變革性併購交易（且無支撐這類交易的 EBITDA 規模）。",
      "quote": "we don't do major transformative deals",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "commitment",
      "claim": "管理層說沒有意圖偏離既有的成長／利潤率／回購三重財務紀律。",
      "quote": "we don't have any intention to deviate from that philosophy",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "risk",
      "claim": "管理層說客戶端設計需求與工程師人力供給之間存在巨大落差。",
      "quote": "demand from our customers and the engineering supply",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "risk",
      "claim": "管理層引述 TSMC 對未來五年電晶體數量成長 48-50 倍的說法，指出設計複雜度壓力。",
      "quote": "48 to 50x kind of transistor growth in the next 5 years",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    },
    {
      "topic": "guidance",
      "claim": "管理層說隨著矽與系統整合，SD&A／模擬的 TAM 有潛力隨時間翻倍。",
      "quote": "it could double the TAM over time",
      "speaker": "Richard Gu (VP of IR, Executives)",
      "date": "2026-06-09",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
    }
  ],
  "qa_flags": [
    {
      "question": "Joseph Quatrochi (Wells Fargo) asked why Q3 opex came in better than expected but Q4 opex looks worse, and whether that relates to Artisan deal timing.",
      "response_pattern": "John Wall's first answer discussed broad-based execution and demand across product categories without addressing the opex timing question; the analyst had to re-ask ('I guess maybe just a question on the OpEx...') and John Wall asked him to repeat the question before giving a specific answer.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "question": "Charles Shi / Yu Shi (Needham) asked directly whether hardware growth could decelerate in year 3 of the current Z3/X3 upgrade cycle, as it did in year 3 of the prior Z2/X2 cycle.",
      "response_pattern": "John Wall responded 'We're trying to unpack it' and pivoted to general commentary on backlog, pipeline strength and revenue-curve shape across quarters, without directly confirming or denying a year-3 deceleration comparable to the prior cycle.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q3_2025_Earnings_Call_20251027.md"
    },
    {
      "question": "Gary Mobley (Loop Capital) 追問：SD&A 轉向一年期授權合約是否是 2025 年 SD&A 營收僅成長 13% 的原因？併入 Hexagon（原年化 $240M 營收水準）時是否也會因同樣的合約年期轉換而受限？",
      "response_pattern": "John Wall 承認 BETA 子公司 2025 年刻意轉向年度訂閱、影響年增率比較基期，但未直接量化該轉換對 SD&A 成長率的拖累幅度；對 Hexagon 僅給出約 $200M 年化營收的粗估數字，隨即表示『我們還沒有任何確定數字』並聲明本次指引未納入 Hexagon，未正面回應 $240M 數字是否因授權年期轉換而被下修。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "question": "Charles Shi / Yu Shi (Needham) 詢問：那家首次流出 COT 晶片的指標型雲端服務商，未來會如何在其他晶片項目上擴大 COT 比重？目前有多少雲端服務商正在做 COT？",
      "response_pattern": "Anirudh Devgan 明確表示『不會談論特定客戶的細節』，轉而用產業層級的通用敘事（大型雲端服務商自研晶片趨勢日益確立）回答，未直接回應該特定客戶的擴散節奏或時間表這個具體問題。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "question": "Gianmarco Conti (Deutsche Bank) 一次問了三個子問題：(1) ChipStack 與 Cerebrus 未來是否會有功能重疊/蠶食；(2) 在 AI 模型開發領域是否看到來自新創的競爭增加；(3) 在更高設計規模下同時跑更多 agent，是否會遇到算力方面的硬性限制。",
      "response_pattern": "Anirudh Devgan 開場先說線路有雜訊、『可能沒有聽全所有重點』，隨後回答了 ChipStack/Cerebrus 分工與新創競爭兩個子問題，但全程未觸及第三個子問題（更多 agent 並行時的算力限制）。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q4_2025_Earnings_Call_20260217.md"
    },
    {
      "question": "Andrew DeGasperi 追問 physical AI／agentic 貨幣化時程是否已提前於原先講的兩個合約週期",
      "response_pattern": "CEO 先鬆口說有可能提前於 2 個合約週期，隨即補一句「I don't want to predict too much」收回具體時程承諾，未給出可證偽的時間點",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Q1_2026_Earnings_Call_20260427.md"
    },
    {
      "question": "AI 對 EDA 業務的貢獻能否量化，是否比之前更接近能給出數字的階段？",
      "response_pattern": "CFO 未給出量化數字，改以「很難拆分」帶過，轉談 AI 工具帶動的授權使用量與遞延／分期認列營收的質性描述，未正面回答是否更接近量化。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "question": "非 AI 半導體客戶的 EDA 支出是否會在明年加速？",
      "response_pattern": "CFO 以「很難說」開頭迴避直接判斷，隨即轉向設計複雜度上升、工具日益不可或缺的一般性說法，未針對「是否加速」給出明確答案。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Wells_Fargo_s_9th_Annual_TMT_Summit_20251118.md"
    },
    {
      "question": "And should we focus on that nonexclusivity in that deal when thinking about yourselves?",
      "response_pattern": "Management answered at length about the NVIDIA partnership's growth and gave a brief, sentence-cut-off mention of ongoing Intel discussions, but never addressed the specific question about the Synopsys deal's nonexclusivity.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "question": "What sort of margin pressure should we expect?",
      "response_pattern": "Management gave a qualitative, non-quantified answer ('there might be some 1-year impact... not going to be that significant given our scale') rather than a specific margin-pressure figure.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_53rd_Annual_Nasdaq_Investor_Conference_20251209.md"
    },
    {
      "question": "Has increased design complexity and AI tool adoption actually improved Cadence's pricing power versus history?",
      "response_pattern": "CEO reframes the answer around 'delivering value' and volume-driven growth philosophy without citing any specific pricing power data, price increases, or realized price/value capture metrics.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "question": "How much design activity is Cadence seeing in physical AI/robotics/edge AI, and should investors pay more attention now?",
      "response_pattern": "CEO expresses long-standing directional optimism ('big fan of physical AI... 3 to 7 years') but hedges specifics with 'exact timing is very difficult to say' and 'this may correct, may not correct', avoiding a concrete revenue or timing commitment.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_Bank_of_America_2026_Global_Technology_Conference_20260603.md"
    },
    {
      "question": "分析師追問 agentic AI（super agents）產品的變現與營收貢獻，特別是「timing」（潛在時點）該如何預期。",
      "response_pattern": "管理層通篇談定價模式構想（訂閱＋消費制類比租車）、TAM 擴張與早期訊號「非常令人鼓舞」，但全程未給出具體變現時間表或營收貢獻數字，只以「we can be patient in terms of monetizing the top layer」帶過分析師具體問的 timing 提問。",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/CDNS/CDNS_54th_Nasdaq_Jefferies_Investor_Conference_20260609.md"
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

