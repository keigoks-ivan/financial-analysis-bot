你是 stock-analyst v17 判斷 agent，標的 STRL（20260905）。你**只做一件事**：把證據包收斂成定案的判斷物（judgment.json／scenario.json）。你不寫散文、不碰 HTML、不產表格。流程內的驗收由機械閘與**跨模型閘（gate）**承接，不是你自己複核——你把判斷寫對、寫滿即可，不必自評。

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

- `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STRL_20260905/judgment.json`（schema：`scripts/dd_schema/judgment.schema.json`；欄位語意見 bundle 內 schema 速查）
- `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STRL_20260905/scenario.json`（`dd_scenario.py` 輸入格式）

兩檔寫完後，**一次複合 Bash** 跑：

```
python3 scripts/ddreport.py judge check STRL 20260905
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

標的：STRL　日期：20260905　角色：stock-analyst v16.2 三步制的判斷（judge） agent。

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

ticker=STRL　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 486.49, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-08-03", "trading_days_since": 25, "flag_within_3d": false, "note": null}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 4, "current": 33.12, "high": {"value": 34.03, "date": "2025-12-31"}, "low": {"value": 9.19, "date": "2022-12-31"}, "current_percentile_within_annual_points": 96.3}, "ps": {"n_points": 4, "current": 4.33, "high": {"value": 3.97, "date": "2025-12-31"}, "low": {"value": 0.55, "date": "2022-12-31"}, "current_percentile_within_annual_points": 100.0}, "ev_s": {"n_points": 4, "current": 4.29, "high": {"value": 3.95, "date": "2025-12-31"}, "low": {"value": 0.73, "date": "2022-12-31"}, "current_percentile_within_annual_points": 100.0}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-20", "price_used": 732.94, "fy1_eps": 18.72, "fwd_pe": 39.15}, {"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 860.84, "fy1_eps": 18.72, "fwd_pe": 45.99}, {"snapshot_date": "2026-06-04", "price_used": 882.43, "fy1_eps": 18.74, "fwd_pe": 47.09}, {"snapshot_date": "2026-06-23", "price_used": 804.76, "fy1_eps": 18.92, "fwd_pe": 42.53}, {"snapshot_date": "2026-07-16", "price_used": 638.56, "fy1_eps": 19.31, "fwd_pe": 33.07}, {"snapshot_date": "2026-07-30", "price_used": 596.77, "fy1_eps": 19.1, "fwd_pe": 31.24}, {"snapshot_date": "2026-08-13", "price_used": 576.48, "fy1_eps": 20.03, "fwd_pe": 28.78}, {"snapshot_date": "2026-08-28", "price_used": 486.49, "fy1_eps": 20.03, "fwd_pe": 24.29}, {"snapshot_date": "2026-09-04", "price_used": 486.49, "fy1_eps": 20.03, "fwd_pe": 24.29}], "current": 24.29, "high": 47.09, "low": 24.29, "current_percentile_within_window": 0.0, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 9 份快照（2026-05-20 ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": -44.87, "return_26w_pct": 23.13, "excess_return_13w_pct": -49.4, "excess_return_26w_pct": 8.61, "benchmark": "^GSPC", "rsi14": 40.85, "rsi14_usable": true, "distance_from_52w_high_pct": -51.04, "distance_from_52w_low_pct": 71.56, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 20.03, "fy2": 25.4, "fy3": 28.91}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 20.03, "fy2": 25.4, "fy3": 28.91}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 18.74, "fy2": 22.89, "fy3": 20.76}, "fy1": {"revision_pct": 0.0, "from": 20.03, "to": 20.03, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": 0.0, "from": 25.4, "to": 25.4, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 0.0, "from": 28.91, "to": 28.91, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 6.88, "fy2_revision_90d_pct": 10.97, "fy3_revision_90d_pct": 39.26, "stale": false, "note": null}, "peer_financials": {"STRL": {"gross_margin_pct": 23.81, "operating_margin_pct": 18.13, "fcf_margin_pct": 14.02, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}, "EME": {"gross_margin_pct": 19.43, "operating_margin_pct": 9.6, "fcf_margin_pct": 6.3, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}, "FIX": {"gross_margin_pct": 25.66, "operating_margin_pct": 16.45, "fcf_margin_pct": 19.24, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}, "PWR": {"gross_margin_pct": 15.46, "operating_margin_pct": 6.12, "fcf_margin_pct": 7.27, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}, "MTZ": {"gross_margin_pct": 12.91, "operating_margin_pct": 5.14, "fcf_margin_pct": 1.52, "rd_intensity_pct": null, "fiscal_period_as_of": "TTM ending 2026-06-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": "Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）"}}, "edgar_concentrations": {"filing_type": "10-Q", "filing_date": "2026-08-04", "url": "https://www.sec.gov/Archives/edgar/data/874238/000087423826000103/strl-20260630.htm", "excerpt": null, "note": "filing 全文內找不到 concentration／customer concentration 相關段落"}, "latest_quarter_kpis": {"_required": true, "quarter": "Q2 FY2026（三個月期間至 2026-06-30，公告於 2026-08-03）", "items": [{"metric": "營收（GAAP）", "value": 1170.0, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "consensus 約 $963.25M（Yahoo Finance／Zacks 引用之 Wall Street 估計，來源非公司本身）；實際優於估計", "prior_quarter": "Q1 FY2026: $825.7M（QoQ +41.7%）；YoY +90%（原文口徑）"}, {"metric": "Non-GAAP（調整後）營業利益", "value": 251.8, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "查無單獨揭露之 consensus 調整後營業利益", "prior_quarter": "Q1 FY2026: $158.2M"}, {"metric": "Non-GAAP（調整後）營業利益率", "value": 21.6, "unit": "%", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "查無單獨揭露之 consensus 調整後營業利益率", "prior_quarter": "Q1 FY2026: 19.2%"}, {"metric": "GAAP 營業利益", "value": 219.3, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "查無單獨揭露之 consensus GAAP 營業利益", "prior_quarter": "Q1 FY2026: $137.8M"}, {"metric": "GAAP 營業利益率", "value": 18.8, "unit": "%", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "查無單獨揭露之 consensus GAAP 營業利益率", "prior_quarter": "Q1 FY2026: 16.7%"}, {"metric": "自由現金流（FCF，推算）", "value": 112.4, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "推算：六個月營運現金流 $328.0M（公司新聞稿）減六個月資本支出 $69.6M（10-Q，公司未直接揭露單季 FCF），再減去已知 Q1 營運現金流 $165.6M 與 Q1 資本支出 $19.6M 反推 Q2 單季（OCF $162.4M − Capex $50.0M）", "vs_consensus": "查無 consensus FCF", "prior_quarter": "Q1 FY2026: 推算 FCF 約 $146.0M（OCF $165.6M − Capex $19.6M）"}, {"metric": "FCF Margin（推算）", "value": 9.6, "unit": "%", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "推算：FCF $112.4M / 營收 $1,170M", "vs_consensus": null, "prior_quarter": "Q1 FY2026: 約 17.7%（$146.0M / $825.7M）"}, {"metric": "SBC 占營收 %", "value": 0.69, "unit": "%", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿／10-Q：SBC $8.1M；占營收 $1,170M", "vs_consensus": null, "prior_quarter": "Q1 FY2026: SBC $7.5M，占營收 $825.7M ≈ 0.91%"}, {"metric": "全年 2026 財測（管理層指引，本次上修）", "value": "營收 $4.00B–$4.15B；調整後稀釋 EPS $19.70–$20.30；調整後 EBITDA $891M–$916M", "unit": "mixed", "as_of": "隨 Q2 FY2026 財報同步發布，2026-08-03", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "上修前（Q1 財報時，2026-05-04）：營收 $3.70B–$3.80B；調整後稀釋 EPS $18.40–$19.05；調整後 EBITDA $843M–$873M", "prior_quarter": null}, {"metric": "調整後稀釋 EPS", "value": 5.8, "unit": "US$", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "consensus 約 $4.99（Yahoo Finance 引用 Wall Street 估計，非公司揭露）；Beat +$0.81", "prior_quarter": "Q1 FY2026: $3.59"}, {"metric": "簽約在手訂單（Signed Backlog）", "value": 4.33, "unit": "US$ billion", "as_of": "季末 2026-06-30，公告於 2026-08-03", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": null, "prior_quarter": "Q1 FY2026 (2026-03-31): $3.80B；YoY +116%"}, {"metric": "合併在手訂單（Combined Backlog，含未簽約 awarded）", "value": 5.62, "unit": "US$ billion", "as_of": "季末 2026-06-30，公告於 2026-08-03", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": null, "prior_quarter": "Q1 FY2026 (2026-03-31): $5.15B；YoY +150%"}, {"metric": "E-Infrastructure 分部營收", "value": 905.0, "unit": "US$ million", "as_of": "Q2 FY2026（季末 2026-06-30，公告於 2026-08-03）", "source": "公司新聞稿 https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/", "vs_consensus": "YoY +192%；分部調整後營業利益率 23.3%；資料中心／半導體／製造業專案占該分部在手訂單 92%", "prior_quarter": null}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | + | 2026-05-06 | Sterling's E-Infrastructure segment revenue accelerated 174% YoY in Q1 2026 (company-wide revenue +90%); segment is now ~60% of total revenue at ~24% margin and is guided for 40%+ full-year 2026 revenue growth, driven by hyperscaler/AI data-center demand. | Yahoo Finance - "Will Sterling's 125% Data Centre Growth Extend Into 2026?", https://finance.yahoo.com/news/sterlings-125-data-centre-growth-152200180.html | moat_trend,thesis.H,valuation |
| competitive_share_entrants#1 | + | 2026-08-01 | Sterling raised FY2026 revenue guidance to $3.7-3.8 billion (a 20% increase from the prior guidance midpoint); signed backlog climbed 78% YoY to $3.8 billion and combined backlog rose 131% to $5.2 billion, with total visibility near $6.5 billion — management attributes this to Sterling's integrated site-development-plus-electrical positioning (via the CEC acquisition) strengthening its competitive standing as data-center capex expands. | Yahoo Finance - "Sterling and Data Centers: The Integrated Buildout Trade", https://finance.yahoo.com/markets/stocks/articles/sterling-data-centers-integrated-buildout-150700712.html | thesis.H,decision_inputs.bull,valuation,triggers |
| competitive_share_entrants#2 | 0 | 2026-09-01 | Sterling's identified competitors in mission-critical/data-center construction include Quanta Services and EMCOR (both also reporting robust hyperscaler-driven demand), plus Fluor, Granite Construction, Skanska USA, MasTec, AECOM, Kiewit, Webcor and Turner — a broad field of large diversified peers rather than a single disruptive new entrant. | ZoomInfo - "Sterling Infrastructure Competitors & Alternatives (2026)"; Yahoo Finance - "3 Infrastructure Stocks Fueling the Data Center Building Boom" | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#3 | - | 2026-08-15 | YTD 2026 stock performance shows Sterling (STRL) +68.7% vs closest AI-infrastructure comp Comfort Systems (FIX) +77.4%, while Quanta Services +49.5% and EMCOR +22.6% — all outperforming the Zacks Construction sector (+7-11%) and S&P 500 (+10.9-11.8%), but Comfort Systems specifically outpacing Sterling on the same AI-buildout theme. | Zacks via Yahoo Finance - "Sterling vs. Comfort Systems: Which AI Infrastructure Stock Wins?", https://finance.yahoo.com/technology/ai/articles/sterling-vs-comfort-systems-ai-135400134.html | valuation,thesis.R,decision_inputs.bear |
| customer_second_source#0 | - | 2026-05-01 | Sterling's E-Infrastructure customer concentration was last disclosed at 35% of segment revenue from four customers (fiscal 2022); the company has not disclosed updated concentration figures in its Q4 2025 or Q1 2026 earnings materials even though the E-Infrastructure segment has more than doubled in size since, and analysts note customer identities are not disclosed, making single-source risk hard for investors to verify directly. | Beating the Tide - "Sterling Infrastructure (STRL) Q1 2026 Update: Tsunami Confirmed, Asymmetry Spent", https://www.beatingthetide.com/p/sterling-infrastructure-strl-q1-2026-update-target-1010 | thesis.R,decision_inputs.bear,moat_trend |
| customer_second_source#1 | 0 | 2026-09-01 | No direct evidence found of any named Sterling customer actively adding a second/competing site-development or electrical contractor, or bringing that scope of work in-house. The 2026 hyperscale data-center GC market instead remains concentrated among a small set of program managers (Turner, DPR, Mortenson, Hensel Phelps, Holder, Clayco) with specialized MEP subcontractors (e.g., Rosendin Electric) self-performing the electrical package (30-40% of total construction cost) — i.e. the observed industry pattern is trade-specialist self-performance within GC-led teams, not owner-side insourcing away from contractors like Sterling. | Buildermuse - "Top 20 Data Center Construction Contractors in 2026", https://buildermuse.com/commercial/the-top-20-data-center-construction-contractors/; Maktinta - "Who Builds AI Data Centers (and Who's Hiring) in 2026", https://www.maktinta.com/post/ai-data-center-construction-and-hiring-2026 | thesis.R,decision_inputs.bear |
| customer_concentration_credit#0 | + | 2025-12-31 | E-Infrastructure Solutions segment top-4-customer revenue concentration has declined over three years: 40% in FY2023, 31% in FY2024, 27% in FY2025 (per FY2025 10-K disclosure). | Sterling Infrastructure, Inc. Form 10-K FY2025 (filed 2026), sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm | moat_trend,decision_inputs.bear |
| customer_concentration_credit#1 | - | 2025-12-31 | Transportation Solutions segment top-4-customer concentration (state DOTs) has risen: 50% in FY2023, 47% in FY2024, 58% in FY2025. | Sterling Infrastructure, Inc. Form 10-K FY2025 (filed 2026), sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm | thesis.R,decision_inputs.bear |
| customer_concentration_credit#2 | 0 | 2025-12-31 | In FY2025, no single customer accounted for more than 10% of Sterling's consolidated revenue, though the 10-K discloses that loss of a top customer in either segment could have a material adverse effect. | Sterling Infrastructure, Inc. Form 10-K FY2025 (filed 2026), sec.gov/Archives/edgar/data/874238/000087423826000024/strl-20251231.htm | decision_inputs.bear |
| customer_concentration_credit#3 | 0 | 2022-12-31 | Historical baseline: in FY2022, the top four customers accounted for 35% of E-Infrastructure segment revenue (segment has more than doubled in size since, per subsequent 10-K disclosures showing declining concentration ratio). | Simply Wall St News, "Should Data Center-Fueled E-Infrastructure Expansion and CEC Deal Require Action From Sterling Infrastructure (STRL) Investors?", citing Sterling FY2022 10-K | moat_trend |
| customer_concentration_credit#4 | 0 | 2026-07-24 | Moody's (reported by CNBC, 2026-07-24) said 'unprecedented' AI capex spending threatens the credit quality of Amazon, Meta, Alphabet, Microsoft, Oracle and CoreWeave -- all customers/counterparties in the hyperscale data center buildout that Sterling's E-Infrastructure segment serves -- but noted Microsoft, Alphabet, Amazon and Meta retain among the strongest corporate balance sheets globally with no imminent investment-grade downgrade risk. | CNBC, "Moody's says 'unprecedented' AI spending threatens credit quality of Amazon, Meta, Alphabet and others", cnbc.com/2026/07/24/moodys-ai-spending-credit-quality-amazon-meta-alphabet.html | thesis.R,decision_inputs.bear |
| customer_concentration_credit#5 | - | 2025-11-01 | Oracle -- a major hyperscale/AI-infrastructure capex spender -- is the weakest-credit name among large AI capex spenders: rated Baa2 with negative outlook (two notches above junk), net leverage above 3.5x, ~500% debt-to-equity; Barclays warned in November 2025 that Oracle's debt could be downgraded to BBB-, the lowest investment-grade rating before junk status. | 24/7 Wall St, "Bad News for NVIDIA, Amazon, and Microsoft: There's No Longer Enough Cash for AI"; Barclays Oracle debt downgrade coverage | thesis.R,decision_inputs.bear |
| supply_demand_durability#0 | + | 2026-06-30 | At June 30, 2026, Sterling's signed backlog rose 116% year-over-year to $4.3 billion, and combined backlog (signed + awarded not signed) rose 150% year-over-year to $5.6 billion, driven by E-Infrastructure demand. | Zacks (via Globe and Mail / TradingView), "Can Sterling's Backlog Strengthen Its Infrastructure Growth Prospects?" | thesis.H,supply_demand_durability |
| supply_demand_durability#1 | + | 2026-06-30 | In Q2 2026 (quarter ended June 30, 2026), Sterling's E-Infrastructure segment revenue grew 192% year-over-year and signed backlog grew 165% year-over-year, with mission-critical (data center/semiconductor) projects accounting for 92% of the segment's backlog; legacy site development revenue alone grew 111%. | Zacks (via Globe and Mail / TradingView), "Is Sterling's 192% E-Infrastructure Growth Just Getting Started Now?" / "Can Sterling's Backlog Strengthen Its Infrastructure Growth Prospects?" | thesis.H,moat_trend |
| supply_demand_durability#2 | + | 2026-06-30 | Following record Q2 2026 results, Sterling raised full-year 2026 guidance, targeting roughly 25% revenue growth for 2026; management ties the outlook to structurally expanding end markets (large-scale data centers, semiconductor fabs, advanced manufacturing) with hyperscaler customers now scoping campus projects lasting up to 12 years. | PR Newswire, "Sterling Reports Record Second Quarter Results and Raises Full Year 2026 Guidance"; Seeking Alpha, "Sterling Infrastructure Q2 2026 Review: A Triple Beat Sold On The Mix" | thesis.H,decision_inputs.bear |
| supply_demand_durability#3 | - | 2026-07-24 | Moody's (per CNBC, 2026-07-24) flagged 'unprecedented' AI capex spending as a threat to hyperscaler credit quality; separately, analysts note the AI capex cycle (aggregate hyperscaler capex ~$700B in 2026, projected ~$820B in 2027 per Moody's, and up to $1.15T cumulative 2025-2027 per Goldman Sachs) could run ahead of monetization -- the bear case is that Sterling's E-Infrastructure demand durability is contingent on hyperscalers continuing to fund a capex cycle that some analysts flag as increasingly debt- and off-balance-sheet-financed rather than purely cash-flow funded. | CNBC, "Moody's says 'unprecedented' AI spending threatens credit quality of Amazon, Meta, Alphabet and others", cnbc.com/2026/07/24/moodys-ai-spending-credit-quality-amazon-meta-alphabet.html | thesis.R,decision_inputs.bear,triggers |
| regulatory_antitrust | - | - | (status=none；無 findings) |  |  |
| reg_tariff_export#0 | - | 2026-04-06 | 2026年4月2日總統公告重整鋼鐵/鋁/銅第232條關稅，4月6日生效：鋼鐵/鋁/銅製品加徵50%關稅，衍生品加徵25%關稅，且計稅基礎改為進口品全額完稅價值（含衍生品）；6月再調整擴大低稅率適用範圍並將美國原產金屬含量門檻從95%降至85%。 | Perkins Coie "Restructured and Additional Section 232 Tariffs on Aluminum, Steel, and Copper"; White & Case "United States modifies steel, aluminum, and copper Section 232 tariffs" | thesis.R,decision_inputs.bear,valuation |
| reg_tariff_export#1 | - | 2026-08-01 | STRL 為重型土木與混凝土承包商，對瀝青、混凝土、鋼鐵等主要營建原料價格波動高度暴露；在固定價格合約下，原料或人工成本意外上漲會侵蝕毛利並影響專案獲利能力。 | Simply Wall St — Sterling Infrastructure (Nasdaq:STRL) Stock Analysis risk disclosure | thesis.R,decision_inputs.bear |
| reg_tariff_export#2 | + | 2026-08-04 | 儘管面臨關稅逆風，STRL 2026 Q2（2026-08-04 發布）營收年增90%至11.68億美元、調整後EPS年增116%至5.80美元，均優於市場預期（EPS優於預期16.2%、營收優於預期21.5%）；已簽約在手訂單年增116%至43億美元，合併在手訂單達56億美元；E-Infrastructure（資料中心/半導體相關）營收年增192%，利潤率維持24%；公司上修2026全年營收指引至40-41.5億美元。 | Sterling Infrastructure Q2 2026 earnings release/call coverage — Investing.com "Sterling Infrastructure Q2 2026 slides: 90% revenue jump, shares fall"; The Motley Fool Q2 2026 earnings call transcript (2026-08-10) | thesis.H,moat_trend,decision_inputs.bear |
| geo_supply_chain#0 | - | 2026-03-02 | Sterling 的 E-Infrastructure（資料中心）主力專案地理上集中於德州、亞利桑那州與卡羅來納州三個市場,尚未見到全國性分散的揭露,屬國內專案地理集中風險（非離岸地緣風險）。 | FinancialContent/Finterra, 'The Infrastructure Renaissance: A Deep Dive into Sterling Infrastructure (STRL)' | thesis.R,decision_inputs.bear |
| geo_supply_chain#1 | + | 2026-03-02 | 同篇分析指出「friend-shoring」（供應鏈回流美國本土/友岸國家）趨勢對 Sterling 構成長期結構性需求利多,因其資料中心/半導體廠營造工程全數為美國境內施作,不涉及海外製造據點曝險。 | FinancialContent/Finterra, 'The Infrastructure Renaissance: A Deep Dive into Sterling Infrastructure (STRL)' | thesis.H,moat_trend |
| geo_supply_chain#2 | 0 | 2026-08-01 | Sterling 資料中心與晶圓廠營造客戶群為少數超大規模業者（hyperscaler）與半導體廠商,單一專案規模持續擴大,部分園區型專案簽約可長達 12 年。 | Yahoo Finance, 'Sterling Infrastructure (STRL) Is Recasting Its Business Around Data Centers And Chip Plants' | thesis.R |
| end_markets#0 | + | 2026-08-10 | 2026年第2季 E-Infrastructure Solutions 營收年增192%達9.05億美元；公司將2026全年 E-Infrastructure 營收成長指引上修至逾100%（含 CEC 與 Stone Ridge 併購貢獻）；已簽約在手訂單逾90%為資料中心、大型製造與半導體等task-critical工程；管理層重申資料中心需求可望持續。 | PRNewswire, 'Sterling Reports Record Second Quarter Results and Raises Full Year 2026 Guidance'; The Globe and Mail, "Is Sterling's 192% E-Infrastructure Growth Just Getting Started Now?" | thesis.H,growth,valuation |
| end_markets#1 | 0 | 2026-08-10 | 分析師預估 E-Infrastructure 2027年成長率放緩至約25%（較2026年108.6%大幅趨緩），但公司合併在手訂單較去年成長131%達52億美元，並提及「未來階段」可見度上看約65億美元，資料中心專案規模擴大且部分延長至5-8年以上。 | Yahoo Finance, "STRL's Backlog Visibility: What It Means for 2026-2027 Growth" | growth,valuation |
| end_markets#2 | 0 | 2026-08-10 | 2026年第2季 Transportation Solutions 營收年減20%，主因公司主動將資源移轉至毛利率較高的 E-Infrastructure 業務；管理層預期2026全年營收下滑7%至10%；惟該季調整後營業利益率逆勢擴張逾500個基點至19.5%，顯示營收下滑主因是資源配置策略而非單純終端市場需求疲弱。 | Investing.com, 'Earnings call transcript: Sterling Infrastructure beats Q2 2026 estimates, shares fall' | thesis.H,growth |
| end_markets#3 | - | 2026-08-10 | Transportation Solutions季底在手訂單9.69億美元，年增35%，主要反映未簽約backlog轉為已簽約backlog；惟公司合併在手訂單較2025年底下滑11%。 | Investing.com, 'Earnings call transcript: Sterling Infrastructure beats Q2 2026 estimates, shares fall' | thesis.R,growth |
| end_markets#4 | - | 2026-08-10 | 受購屋可負擔性壓力導致住宅需求走弱影響，Building Solutions 2026上半年營業利益由去年同期2220萬美元降至1470萬美元；公司在手訂單維持30.1億美元的紀錄水準，可見度延伸至2027年。 | PRNewswire / strlco.com, 'Sterling Reports Record Second Quarter Results and Raises Full Year 2026 Guidance' | thesis.R,decision_inputs.bear,growth |
| substitute_technology#0 | - | 2026-01 | 全球模組化／預製建築市場預估 2026 年達 1834 億美元、2027 年達 1939 億美元；在資料中心等高成長領域，模組化施工可將專案工期縮短 30%–50%，將部分現場人力工作轉移至工廠端預製。 | Future Market Insights, "Modular & Prefabricated Construction Market" report (亦見 epicflow.com "Key Technology Trends in the Construction Industry in 2026") | moat_trend,thesis.R |
| channel_business_model_shift#0 | + | 2026-08 | STRL 的 Transportation Solutions 分部正從量驅動的低價競標模式，轉為紀律性選案／組合優化，聚焦 design-build、機場、鐵路與另類交付（alternative-delivery）等高技術含量、較高毛利專案；管理層並將德州低價競標高速公路業務的收斂列為毛利改善的結構性驅動因素之一。 | Nasdaq.com, "Sterling's Transportation Margins Rebound: A Structural Shift?" | thesis.H,moat_trend,decision_inputs.bear |
| channel_business_model_shift#1 | + | 2026-Q1 | STRL 以 5.616 億美元收購 CEC Facilities Group，取得專業電氣與機電服務能量，將營運範圍從單純的場地整備（site development）延伸至資料中心、半導體廠、先進製造廠等專案生命週期的更多階段，不再於場地整備完成後即把工作轉交給其他專業承包商；截至 2026 年第一季末，任務關鍵型（mission-critical）專案已占 E-Infrastructure 在手訂單逾 90%。 | TradingView/Zacks, "Can Sterling's Vertical Integration Push Margins Even Higher?" | moat_trend,thesis.H |
| channel_business_model_shift#2 | 0 | 2026-01 | 針對「超大規模業者（hyperscaler）是否正繞過總承包商、直接與專業分包商簽約」的查證，找到的產業資料顯示超大規模資料中心營建仍普遍採傳統多承包商協調模式（含 OFCI／業主自供設備由承包商安裝），未查到 hyperscaler 直接繞過總承包商模式已structurally 成形的證據。 | Giatec Scientific, "Data Center Construction Guide for GCs"；StruxHub, "Hyperscale Data Center Construction Management" | thesis.R |
| capital_markets_pricing#0 | + | 2026-08-03 | STRL 於 2026-08-03 公布 Q2 2026 財報並上修全年 guidance：營收由先前區間上修至 $4.0-4.15B、調整後 EPS 上修至 $19.70-$20.30，高於當時分析師共識 $19.10；營收年增 90%（含 CEC／Stone Ridge 併購貢獻＋約 50% 有機成長），簽約在手訂單年增 116% 至 $4.3B、合併在手訂單年增 150% 至 $5.6B | The Globe and Mail, "Sterling Infrastructure Reports Record Q2 Results, Raises Guidance"; StockTitan 8-K filing summary | thesis.H,valuation,triggers |
| capital_markets_pricing#1 | - | 2026-08-03 | 儘管財報三重優於預期（營收/EPS/guidance 皆上修），STRL 股價於財報公布後仍下跌約 10%，原因是 E-Infrastructure 分部調整後營益率因低毛利電氣工程業務（CEC）佔比上升而下滑約 420 個基點（該分部整體毛利率仍優於 Transportation Solutions，但混合效應稀釋） | ts2.tech, "Sterling Infrastructure (NASDAQ:STRL) Shares Drop 10% After Earnings Report as Electrical Segment Alters Margins" | thesis.R,moat_trend,decision_inputs.bear |
| capital_markets_pricing#2 | - | 2026-08-21 | KeyCorp（KeyBanc）於 2026-08-05 將 STRL 目標價由 $922 下修至 $754（原因與財報後市場對利潤率組合的疑慮同期），同月稍後 DA Davidson 於 2026-08-21 首次覆蓋給予 Buy 評等、目標價 $700 | TipRanks/TheFly, "sterling infrastructure price target raised to 460 from 355 at da davidson" 頁面內含之同批目標價異動記錄（KeyCorp $922→$754 8/5/2026；DA Davidson 首評 $700 8/21/2026） | valuation,decision_inputs.bear |
| capital_markets_pricing#3 | + | 2026-09-04 | 截至查詢當下，8 位分析師（S&P Global 彙整）給予 STRL「Strong Buy」共識評等、平均目標價 $876；另一彙整（15 位分析師）平均目標價 $971.73；Simply Wall St 綜合公允價值估計約 $941.17（較前次 $938.17 微幅上修，引用 KeyBanc 目標價上修至 $922 與 Oppenheimer 首評 $950 為上修理由）——三組目標價估計皆遠高於 `numbers.price_at_dd` $486.49（2026-09-04 收盤），顯示賣方目標價尚未完全反映近月股價修正 | stockanalysis.com STRL forecast page（S&P Global 8-analyst 共識）；WallStreetZen STRL forecast page（15-analyst 平均）；Simply Wall St STRL future page（綜合公允價值） | valuation,thesis.H |
| capital_markets_pricing#4 | - | 2026-08-21 | STRL 股價自 2026-07-22 約 $719 高點下跌，至 2026-08-21 收盤 $516.81（30 日跌幅約 28%），主因為估值與利潤率組合疑慮而非需求或營運面惡化；市場對財報後訂單／利潤率能見度提出更嚴格要求 | Tickeron, "Sterling Infrastructure (STRL) Declines -28% in 30 Days as Valuation Concerns Take Hold"; ts2.tech, "Sterling Infrastructure (NASDAQ:STRL) Faces Tougher Earnings Expectations Following 9.7% Weekly Drop" | thesis.R,decision_inputs.bear,valuation |
| major_events#0 | + | 2025-11-01 | Sterling Infrastructure completed acquisition of CEC Facilities Group (Irving, TX-based specialty electrical and mechanical contractor); upfront purchase price at closing totaled $505 million ($450M cash + $55M Sterling common stock), plus an earn-out contingent on operating income targets through Dec 31, 2029. | Sterling Announces Agreement to Acquire CEC Facilities Group, https://www.strlco.com/news/sterling-announces-agreement-to-acquire-cec-facilities-group/ | moat_trend,thesis.H,valuation |
| major_events#1 | + | 2026-01-01 | Sterling closed acquisition of Stone Ridge Contracting, LLC (Pocatello, ID-based site development contractor), joining Sterling's E-Infrastructure Solutions segment; Stone Ridge projected to generate $180M-$200M revenue for full year 2026 with mid-teens EBITDA margins, and has an earn-out contingent on EBITDA targets through Dec 31, 2031. | Sterling Announces Acquisition of Stone Ridge Contracting, LLC., https://www.strlco.com/news/sterling-announces-acquisition-of-stone-ridge-contracting-llc/ | moat_trend,thesis.H,valuation,decision_inputs.bear |
| major_events#2 | 0 | 2026-09-05 | No securities fraud class action, shareholder litigation, or investor lawsuit specific to Sterling Infrastructure (STRL) was found; search results for 'Sterling' litigation returned only unrelated cases against Sterling Bancorp (NASDAQ: SBT), a different company. | WebSearch aggregate (no STRL-specific litigation source found) | thesis.R,decision_inputs.bear |
| major_events#3 | + | 2026-01-01 | Sterling Infrastructure's 2026 Sustainability Report (covering FY2025 performance) reported a Total Recordable Incident Rate of 0.46 and zero fatalities, described as part of a strengthening safety-first culture; no warning letters, recalls, or safety incidents involving STRL were found. | Sterling Infrastructure (STRL) shows 2025 growth, safer jobsites and stronger ESG focus, https://www.stocktitan.net/sec-filings/STRL/8-k-sterling-infrastructure-inc-reports-material-event-8ab9700aef5a.html | moat_trend,thesis.R |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "found",
  "queries_run": [
   "STRL Sterling Infrastructure acquisition merger 2025 2026",
   "Sterling Infrastructure STRL acquisition merger 2025 2026"
  ],
  "findings": [
   {
    "claim": "Sterling Infrastructure completed acquisition of CEC Facilities Group; upfront purchase price at closing $505 million ($450M cash + $55M Sterling common stock), plus earn-out contingent on operating income targets through Dec 31, 2029.",
    "source": "Sterling Announces Agreement to Acquire CEC Facilities Group, https://www.strlco.com/news/sterling-announces-agreement-to-acquire-cec-facilities-group/",
    "as_of": "2025-11-01",
    "direction": "+",
    "affects": [
     "moat_trend",
     "thesis.H",
     "valuation"
    ]
   },
   {
    "claim": "Sterling closed acquisition of Stone Ridge Contracting, LLC, joining the E-Infrastructure Solutions segment; projected $180M-$200M FY2026 revenue with mid-teens EBITDA margins, earn-out contingent on EBITDA targets through Dec 31, 2031.",
    "source": "Sterling Announces Acquisition of Stone Ridge Contracting, LLC., https://www.strlco.com/news/sterling-announces-acquisition-of-stone-ridge-contracting-llc/",
    "as_of": "2026-01-01",
    "direction": "+",
    "affects": [
     "moat_trend",
     "thesis.H",
     "valuation"
    ]
   }
  ],
  "note": ""
 },
 "lawsuit_class_action": {
  "status": "none",
  "queries_run": [
   "Sterling Infrastructure STRL class action lawsuit securities fraud",
   "\"Sterling Infrastructure\" investor lawsuit OR \"securities litigation\" OR \"shareholder suit\""
  ],
  "findings": [],
  "note": "Search results returned only unrelated litigation involving Sterling Bancorp (NASDAQ: SBT), a distinct, unrelated company; no STRL-specific securities fraud or shareholder class action found."
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Sterling Infrastructure STRL clinical trial FDA approval 2025 2026",
   "Sterling Infrastructure STRL FDA"
  ],
  "findings": [],
  "note": "非藥品/器材業務（STRL 為重型土木／電力基礎設施承包商），已查證無相關監管動作；此軸對本標的不適用（no FDA/clinical exposure in core business lines）。"
 },
 "product_recall_warning": {
  "status": "none",
  "queries_run": [
   "Sterling Infrastructure STRL warning letter recall safety incident 2025 2026",
   "Sterling Infrastructure STRL product launch recall warning letter"
  ],
  "findings": [
   {
    "claim": "Sterling Infrastructure's FY2025 Sustainability Report reported Total Recordable Incident Rate of 0.46 and zero fatalities; no product recalls or regulatory warning letters found for STRL in the search window.",
    "source": "Sterling Infrastructure (STRL) shows 2025 growth, safer jobsites and stronger ESG focus, https://www.stocktitan.net/sec-filings/STRL/8-k-sterling-infrastructure-inc-reports-material-event-8ab9700aef5a.html",
    "as_of": "2026-01-01",
    "direction": "+",
    "affects": [
     "moat_trend"
    ]
   }
  ],
  "note": "No recall/warning-letter events found; the one finding surfaced is a positive safety-record data point, not a recall/warning."
 },
 "sec_investigation_restatement": {
  "status": "none",
  "queries_run": [
   "Sterling Infrastructure STRL SEC investigation restatement",
   "Sterling Infrastructure STRL SEC investigation restatement 2025 2026"
  ],
  "findings": [],
  "note": "No SEC investigation or financial restatement found for STRL; search returned only routine SEC filings (10-K, DEF 14A, 8-K credit facility amendment) with no indication of investigation or restatement."
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_STRL_20260505.html",
 "date": "20260505",
 "schema": "v12.3",
 "dca_verdict": null,
 "dca_role": null,
 "price_at_dd": 529.49,
 "revlog": {
  "status": "unavailable"
 },
 "prior_meta": {
  "ticker": "STRL",
  "name": "Sterling Infrastructure",
  "date": "2026-05-05",
  "schema": "v12.3",
  "price_at_dd": 529.49,
  "inception_dd": "DD_STRL_20260505.html",
  "inception_date": "2026-05-05",
  "next_yoy_review": "2027-05-05",
  "signal": "B",
  "trap": "🟡",
  "trap_label": "觀察期",
  "moat": "B",
  "moat_score": 6.9,
  "moat_execution": 7.5,
  "moat_pricing_power": 6.0,
  "val": "🟡",
  "ma": "✅",
  "regime": "正常",
  "fpe_fy2": 27.2,
  "pct_5y": 68,
  "peg_fy2": 0.68,
  "upside_short_pct": -6,
  "upside_mid_pct": 10,
  "upside_5y_pct": 55,
  "stress": {
   "pass": 2,
   "total": 2
  },
  "growth_durability": 8,
  "quality_score": 7,
  "ai_risk": "🟢",
  "long_term_confidence": "高",
  "verdict": "B（衛星候選 / 觀望偏進場）",
  "oneliner": "Q1 26 三軸強化（Rev+92%/Adj EPS+120%/E-Infra+174%）+FY26 guide+36%／估值🟡 PEG 0.86+MA✅但 BB+19%/4w+57% 動能透支／B 級 moat 6.9（exec 7.5+pricing 6.0）+Cutillo $92M 減持 trap🟡／等回測 $410/$336 進場"
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
    "text": "AI Capex 結構性 super-cycle 持續至 FY28+：Hyperscaler combined capex YoY 維持 25%+ 至 FY28，STRL E-Infra 維持 50%+ YoY",
    "columns": {
     "2Y 驗證點": "FY27 E-Infra Rev > $4.5B（YoY +50%）",
     "5Y 驗證點": "FY30 STRL Total Rev > $8B，E-Infra > $6B",
     "10Y 驗證點": "FY35 AI capex 進入 maintenance 模式但 STRL 已從中累積 $50B+ 累計合約",
     "sourced floor（具體數字 + 來源）": "FY26 Hyperscaler combined capex ≥ $690B（Dell'Oro 2026 base case，CreditSights confirm）；FY27 ≥ $700B（sell-side 共識）；E-Infra Rev YoY 2Y 連 2 季 ≥ 60%（TTM 基）",
     "漂移觸發條件（QC-34 / QC-35）": "連 2 季 TTM E-Infra YoY"
    }
   },
   {
    "id": "H2",
    "text": "CEC turnkey 模式擴大客戶 ARPU + 鎖定：每客戶 Rev 從 $50M / 年擴張至 $150M+（site + electrical 雙包）",
    "columns": {
     "2Y 驗證點": "FY27 CEC 整合營收 > $700M，turnkey 校區數 > 10",
     "5Y 驗證點": "FY30 turnkey 模式涵蓋 80% E-Infra 合約",
     "10Y 驗證點": "FY35 STRL turnkey 為行業 default，類似 GE 全包能源 EPC 地位",
     "sourced floor（具體數字 + 來源）": "CEC 收購 $505M（PRNewswire 2025-09-01）；Q1 26 CEC 貢獻 $156M Rev / 兩個 turnkey 校區交叉銷售（Sterling Q1 26 release）；FY26-27 預期 130-138M / 全年 600M imply",
     "漂移觸發條件（QC-34 / QC-35）": "turnkey 校區 6Q 未達 6 個或 CEC organic + cross-sell Rev 連 2 季"
    }
   },
   {
    "id": "H3",
    "text": "單位經濟拐點不可逆：E-Infra Adj OM 維持 22%+，整體 OM 從 16.6%（FY25）擴張至 18-20%",
    "columns": {
     "2Y 驗證點": "FY27 E-Infra Adj OM 維持 21%+",
     "5Y 驗證點": "FY30 整體 Adj OM 達 19-20%",
     "10Y 驗證點": "FY35 ROIC 持續 > 25%（cycle through）",
     "sourced floor（具體數字 + 來源）": "Q1 26 E-Infra Adj OM 22.4%（Sterling Q1 26 release）；整體 Adj OM 16.6% FY25 → 22% mid FY26 guide；ROIC 22% FY25 vs 14% FY23 趨勢",
     "漂移觸發條件（QC-34 / QC-35）": "連 2 季 E-Infra Adj OM"
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
    "text": "Hyperscaler capex digestion 週期",
    "columns": {
     "對應": "H1",
     "時間尺度": "🔥 中期（4-6 季）",
     "監測指標": "AMZN/MSFT/META/GOOGL 季度 capex guidance、AI workload utilization",
     "警戒閾值": "combined capex YoY"
    }
   },
   {
    "id": "R2",
    "text": "客戶集中度 + 任一 Hyperscaler 退出",
    "columns": {
     "對應": "H1 + H2",
     "時間尺度": "⚡ 短期（1-2 季）",
     "監測指標": "個別客戶 Rev 占比、新客戶簽約速度、bidding pipeline",
     "警戒閾值": "top 1 客戶 Rev 占比 single-quarter > 35% 且 backlog 集中"
    }
   },
   {
    "id": "R3",
    "text": "動能反身性 + estimation reset",
    "columns": {
     "對應": "估值 + 短期",
     "時間尺度": "⚡ 短期（1-2 季）",
     "監測指標": "NTM Fwd PE、4w 漂移、analyst PT 上修速度",
     "警戒閾值": "NTM Fwd PE > 50x 且 PEG > 2.0；或 4w +30%+ 動能透支"
    }
   }
  ]
 },
 "triggers": {
  "status": "unavailable"
 },
 "inception_dd": {
  "path": "docs/dd/DD_STRL_20260505.html",
  "date": "20260505",
  "schema": "v12.3"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_STRL_20260505.html",
  "date": "20260505",
  "days_from_365d_mark": 242
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "STRL",
 "current_verdict": {
  "verdict": null,
  "fundamental_grade": "B",
  "date": "2026-05-05",
  "freshness": "aging",
  "source": "docs/dd/DD_STRL_20260505.html"
 },
 "decision_history": [
  {
   "date": "2026-05-05",
   "verdict": null,
   "role": null,
   "price_at_decision": 529.49,
   "fundamental_grade": "B",
   "to_date_pct": -42.41,
   "days": 118,
   "source_report": "docs/dd/DD_STRL_20260505.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/STRL.md\n[internal-note] 2026-05-17  v12.3 Cold Review Batch 17 — SPOT / STM / STRL / STX / TER\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_v12_3_BATCH17_20260517.md\n[internal-note] 2026-05-17  v12.3 Cold Review — STRL (DD_STRL_20260505.html)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/internal/dd/critic_v12_3_STRL_20260517.md\n[dca] 2026-05-14  STRL Deep Conviction|2026-05-14\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_STRL_20260514.md\n[dd] 2026-05-05  DD_STRL_20260505 — Sterling Infrastructure 深度研究 v12.3\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_STRL_20260505.md"
}
```

### canonical_id（原樣）
```json
{
 "status": "gap"
}
```


---

## ④ 最新一季逐字稿全文

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/STRL/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
  ],
  "items": [
    {
      "topic": "guidance",
      "claim": "CFO announces an increase to full-year 2025 guidance ranges.",
      "quote": "We are increasing our guidance ranges to:",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "New full-year diluted EPS guidance range given.",
      "quote": "diluted EPS of $8.73 to $8.87",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "New full-year EBITDA guidance range given.",
      "quote": "EBITDA of $448 million to $453 million;",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states consolidated gross profit margin expanded year over year in Q3.",
      "quote": "Our gross profit margins expanded 280 basis",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO gives full-year E-Infrastructure segment adjusted operating margin outlook including CEC.",
      "quote": "margins for E-Infrastructure should approximate 25%",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO gives full-year Transportation Solutions adjusted operating margin outlook versus prior year.",
      "quote": "margins in the 13.5% to 14% range compared to 9.6% in 2024.",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO cites a prior tuck-in acquisition (dry conduit business) as an example of margin improvement from combining with site development.",
      "quote": "margins improve 40% just by combining that with the site",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "margin",
      "claim": "CEO states the company will pass on megaprojects if pricing or margins are not right.",
      "quote": "I don't want anybody to be surprised if we pass on one of",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses year-to-date share repurchase amount and average price paid.",
      "quote": "primarily driven by share repurchases of $48.5 million",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO discloses remaining availability under the existing share repurchase authorization.",
      "quote": "existing repurchase authorization is $80.9 million.",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO characterizes the balance sheet position as strong.",
      "quote": "We are in great shape from a balance sheet perspective.",
      "speaker": "Nicholas Grindstaff (CFO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO confirms the CEC acquisition closed during the quarter.",
      "quote": "We are pleased to have closed the CEC acquisition during",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO states permitting timelines have lengthened versus pre-COVID.",
      "quote": "the permitting process certainly is longer today",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO quantifies how much longer permits now take versus historically.",
      "quote": "permit now takes 3 months. Maybe 5 in certain markets.",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO attributes Building Solutions demand weakness to homebuyer affordability challenges.",
      "quote": "potential buyers struggle with affordability challenges.",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO reports a revenue decline in the legacy residential business.",
      "quote": "our legacy residential business declined 17%",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "risk",
      "claim": "CEO notes the current federal transportation funding bill (IIJA) is scheduled to end in September 2026.",
      "quote": "the existing bill ends at the end of September of 2026.",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO describes 'The Sterling Way' as the company's stated commitment covering people, environment, investors and communities.",
      "quote": "The Sterling Way, which is our commitment to take care of",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO expresses confidence in leveraging the combined site development and electrical services capability heading into 2026.",
      "quote": "a high degree of confidence in our ability to leverage the",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "customer",
      "claim": "CEO states customers are discussing multiyear capital deployment plans for data center site development.",
      "quote": "multiyear capital deployment plans and our focus",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "customer",
      "claim": "CEO describes hyperscaler and chip-plant customers as forward-looking in anticipating capacity needs.",
      "quote": "hyperscalers, and even these big chip plants have been",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "competition",
      "claim": "CEO attributes customer value to Sterling's project management and on-schedule delivery capability.",
      "quote": "superior project management and ability to finish jobs",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "product",
      "claim": "CEO describes e-commerce distribution center projects as increasingly resembling data center projects in infrastructure complexity.",
      "quote": "an e-commerce distribution center is starting to look a",
      "speaker": "Joseph Cutillo (CEO)",
      "date": "2025-11-04",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q3_2025_Earnings_Call_20251104.md"
    },
    {
      "topic": "guidance",
      "claim": "Company initiated FY2026 revenue guidance range.",
      "quote": "Revenue of $3.05 billion to $3.2 billion",
      "speaker": "CFO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "Company initiated FY2026 EBITDA guidance range.",
      "quote": "EBITDA of $587 million to $620 million.",
      "speaker": "CFO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO guided E-Infrastructure segment revenue growth for 2026.",
      "quote": "E-Infrastructure revenue growth of 40% or higher.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO guided Transportation Solutions revenue growth for 2026.",
      "quote": "revenue growth in the low to mid-single digits in 2026",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "CEO guided Building Solutions revenue decline for 2026.",
      "quote": "revenue will decline in the high single to low double digits",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "margin",
      "claim": "CEO guided E-Infrastructure adjusted operating margin range for 2026.",
      "quote": "expected to be in the 23% to 24% range.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "margin",
      "claim": "CEO stated FY2025 full-year gross margin and adjusted EBITDA margin levels achieved.",
      "quote": "margins reached 23% and adjusted EBITDA margins exceeded 20%",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "competition",
      "claim": "When asked how Sterling compares to peers on AI adoption, CEO said he does not know where competitors stand.",
      "quote": "I don't know where our peers are.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "product",
      "claim": "CEO described the size of CEC's new modular electrical build facility.",
      "quote": "the new facility is over 300,000 square feet.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "risk",
      "claim": "CEO cited home affordability challenges as impacting Building Solutions demand.",
      "quote": "potential buyers struggle with affordability challenges.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "risk",
      "claim": "CEO said residential market conditions will remain difficult in the first half of 2026.",
      "quote": "I think it's going to be tough,",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "commitment",
      "claim": "CEO described \"The Sterling Way\" as the company's stated commitment to people, environment, investors and communities.",
      "quote": "The Sterling Way, which is our commitment to take care of",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CFO stated remaining availability under the existing share repurchase authorization.",
      "quote": "repurchase authorization is $374 million.",
      "speaker": "CFO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "CEO said capital allocation focus is not on adding a new (\"fourth leg\") business line.",
      "quote": "our focus won't be necessarily on a fourth leg.",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "customer",
      "claim": "CEO said the majority of the $1B+ future phase pipeline is tied to major hyperscaler customers.",
      "quote": "the lion's share of that are with the big name hyperscalers",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "customer",
      "claim": "CEO said future phase work is tied to existing customers, with occasional new customer additions.",
      "quote": "It's tied to existing customers, but we're always getting a",
      "speaker": "CEO",
      "date": "2026-02-26",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "topic": "guidance",
      "claim": "2026 revenue guidance raised to $3.7-3.8B, up 20% at the midpoint from prior guidance.",
      "quote": "Revenue of $3.7 billion to $3.8 billion, which at the midpoint is a 20% increase over previous guidance",
      "speaker": "Nicholas Grindstaff",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "guidance",
      "claim": "2026 adjusted diluted EPS guidance raised to $18.40-$19.05, up 36% at the midpoint from prior guidance.",
      "quote": "Adjusted diluted EPS of $18.40 to $19.05, which at the midpoint is a 36% increase from previous guidance",
      "speaker": "Nicholas Grindstaff",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "guidance",
      "claim": "Full-year 2026 E-Infrastructure segment revenue is guided to grow 80% or higher including CEC.",
      "quote": "For the full year 2026, we expect to deliver E-Infrastructure revenue growth of 80% or higher, including the full year contribution of CEC.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "guidance",
      "claim": "Legacy (ex-CEC) E-Infrastructure business is guided to grow approaching 60% or higher in 2026.",
      "quote": "We anticipate that the legacy business will grow at rates approaching 60% or higher as several of our larger projects accelerate.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "E-Infrastructure adjusted operating profit margin is guided to the mid-20% range for 2026.",
      "quote": "Adjusted operating profit margins for E-Infrastructure are expected to be in the mid-20% range.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "Management expects CEC margins to expand 300-500bp over the next 12-18 months as low-margin end markets are exited.",
      "quote": "we're still extremely bullish that we're going to see 300 to 500 basis points of margin in really 12 to 18 months",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "Q1 2026 adjusted EBITDA margin hit a first-quarter record of 20%, up more than 150bps YoY.",
      "quote": "Adjusted EBITDA more than doubled with margins expanding over 150 basis points year-over-year to reach a new first quarter record of 20%.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "margin",
      "claim": "Management states margin expansion is not coming from raising prices with customers.",
      "quote": "Everybody keeps asking us if we're getting more price. The answer is no, we're not getting more price.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "competition",
      "claim": "CEO describes Sterling's competitive positioning in winning the semiconductor fab campus bid as overwhelming versus other bidders.",
      "quote": "There was no one else in the room that was going to have a chance at this.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "competition",
      "claim": "Management expects to become the preferred site-development partner for future U.S. semiconductor fab projects, similar to its position in data centers.",
      "quote": "we feel very confident that just like in data centers, we will be the supplier of choice for every chip plant that comes out in the future",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Q1 2026 share repurchases totaled $12 million at an average price of $305.14; $362 million remains under the buyback authorization.",
      "quote": "share repurchases of $12 million at an average price of $305.14 per share. Remaining availability under the existing repurchase authorization is $362 million.",
      "speaker": "Nicholas Grindstaff",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Sterling ended Q1 2026 in a net cash position of $224 million ($512M cash vs $287M debt).",
      "quote": "We ended the quarter with $512 million of cash and debt of $287 million for a cash net of debt balance of $224 million.",
      "speaker": "Nicholas Grindstaff",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "capital_allocation",
      "claim": "Management sees a better-quality M&A pipeline now than a year ago and cites balance sheet strength to pursue deals.",
      "quote": "We are seeing more high-quality acquisition targets in the market today than a year ago. Our significant balance sheet firepower positions us to take advantage of these opportunities.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "product",
      "claim": "Sterling signed a lease to triple its modular construction build capacity.",
      "quote": "We just locked down a lease to triple the size of our modular build capabilities.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "product",
      "claim": "An internal AI deployment aimed at project managers yielded roughly a 15% capacity gain.",
      "quote": "The AI project we did first was focused on project managers. We picked up about 15% capacity in project managers.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "risk",
      "claim": "Management emphasizes a risk-averse project selection philosophy as a driver of margin stability.",
      "quote": "We won't take on high-risk jobs that are going to get us in trouble.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "risk",
      "claim": "CEO says the company is turning down customer requests to enter new markets faster than current capacity allows.",
      "quote": "Right now, our biggest challenge is they would like to have us in 2 or 3 or 4 new markets tomorrow. We've had to say no to some of those.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "customer",
      "claim": "Hyperscaler customers are urgently pushing Sterling to expand into new geographies faster than before, citing planned capital spending.",
      "quote": "They're more than pulling now. They're kind of screaming to get into these markets faster with what they see coming in capital spending they're going to do.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "commitment",
      "claim": "Mission-critical projects (data centers, large manufacturing, semiconductor) made up over 90% of E-Infrastructure signed backlog at quarter-end.",
      "quote": "Mission-critical work, including data centers, large manufacturing projects and semiconductor represented over 90% of E-Infrastructure signed backlog at the end of the quarter.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "topic": "commitment",
      "claim": "Signed backlog reached $3.8 billion (+78% YoY) and combined backlog reached $5.2 billion (+131% YoY).",
      "quote": "Signed backlog at the end of the quarter totaled $3.8 billion, a 78% year-over-year increase and combined backlog grew 131% to reach $5.2 billion.",
      "speaker": "Joseph Cutillo",
      "date": "2026-05-05",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    }
  ],
  "qa_flags": [
    {
      "question": "Analyst asked whether a new (\"fourth leg\") business line is something Sterling should be considering as part of its capital allocation, given active buybacks and M&A interest.",
      "response_pattern": "CEO says focus 'won't be necessarily on a fourth leg' but then states 'if the right fourth leg came along, we wouldn't aggressively go after it' — internally inconsistent phrasing (context suggests he meant the opposite), leaving stance on new business-line M&A ambiguous.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q4_2025_Earnings_Call_20260226.md"
    },
    {
      "question": "Given the larger Q1 order intake, how should we think about legacy E-Infrastructure year-over-year growth rates over the remaining 3 quarters to reach the ~60% full-year target?",
      "response_pattern": "CEO declined to give a quarter-by-quarter breakdown, citing timing variability in project starts and repeating 'I just don't -- I don't have that.'",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
    },
    {
      "question": "How much do you expect Texas to account for as a percentage of revenue in the site development business (ex-CEC), and where was it last year?",
      "response_pattern": "CEO declined to give a percentage, saying 'it's really hard to say' and 'I'll only be wrong if I try to give you an answer,' pivoting instead to qualitative commentary about other regions also growing fast.",
      "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/STRL/STRL_Q1_2026_Earnings_Call_20260505.md"
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

