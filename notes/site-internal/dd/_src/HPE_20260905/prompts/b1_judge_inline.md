你是 stock-analyst v17 判斷 agent，標的 HPE（20260905）。你**只做一件事**：把證據包收斂成定案的判斷物（judgment.json／scenario.json）。你不寫散文、不碰 HTML、不產表格。流程內的驗收由機械閘與**跨模型閘（gate）**承接，不是你自己複核——你把判斷寫對、寫滿即可，不必自評。

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

- `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HPE_20260905/judgment.json`（schema：`scripts/dd_schema/judgment.schema.json`；欄位語意見 bundle 內 schema 速查）
- `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HPE_20260905/scenario.json`（`dd_scenario.py` 輸入格式）

兩檔寫完後，**一次複合 Bash** 跑：

```
python3 scripts/ddreport.py judge check HPE 20260905
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

標的：HPE　日期：20260905　角色：stock-analyst v16.2 三步制的判斷（judge） agent。

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

ticker=HPE　date=20260905　archetype_hint=品質複利成長　earnings_recency=None

### numbers（原樣 JSON，不縮排）
```json
{"price_at_dd": 52.0, "price_as_of": "2026-09-04（RTH 收盤，UTC）", "earnings_recency": {"last_earnings_date": "2026-09-02", "trading_days_since": 3, "flag_within_3d": true, "note": "距最近財報僅 3 個交易日（≤3）——估值層須用財報後價格（postMarketPrice/preMarketPrice），共識 EPS 標「財報前快照」"}, "valuation_history": {"method": "trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。", "trailing": {"pe": {"n_points": 3, "current": 26.8, "high": {"value": 19.52, "date": "2022-10-31"}, "low": {"value": 9.64, "date": "2023-10-31"}, "current_percentile_within_annual_points": 100.0}, "ps": {"n_points": 4, "current": 1.65, "high": {"value": 0.89, "date": "2025-10-31"}, "low": {"value": 0.6, "date": "2022-10-31"}, "current_percentile_within_annual_points": 100.0}, "ev_s": {"n_points": 4, "current": 1.98, "high": {"value": 1.43, "date": "2025-10-31"}, "low": {"value": 0.92, "date": "2022-10-31"}, "current_percentile_within_annual_points": 100.0}}, "fwd_recent_window": {"points": [{"snapshot_date": "2026-05-20", "price_used": 37.47, "fy1_eps": 2.42, "fwd_pe": 15.48}, {"snapshot_date": "2026-05-26 (incremental updates over 2026-05-25 base)", "price_used": 42.91, "fy1_eps": 2.42, "fwd_pe": 17.73}, {"snapshot_date": "2026-06-04", "price_used": 49.06, "fy1_eps": 3.41, "fwd_pe": 14.39}, {"snapshot_date": "2026-06-23", "price_used": 43.71, "fy1_eps": 3.41, "fwd_pe": 12.82}, {"snapshot_date": "2026-07-16", "price_used": 45.82, "fy1_eps": 3.41, "fwd_pe": 13.44}, {"snapshot_date": "2026-07-30", "price_used": 47.9, "fy1_eps": 3.41, "fwd_pe": 14.05}, {"snapshot_date": "2026-08-13", "price_used": 58.71, "fy1_eps": 3.42, "fwd_pe": 17.17}, {"snapshot_date": "2026-08-28", "price_used": 52.0, "fy1_eps": 3.44, "fwd_pe": 15.12}, {"snapshot_date": "2026-09-04", "price_used": 52.0, "fy1_eps": 3.82, "fwd_pe": 13.61}], "current": 13.61, "high": 17.73, "low": 12.82, "current_percentile_within_window": 16.1, "window_note": "僅涵蓋本站 data/eps-estimates/ 現存 9 份快照（2026-05-20 ~ 2026-09-04），非 5 年歷史，不得引用為『5年分位』"}, "note": null}, "momentum_26w": {"return_13w_pct": 6.0, "return_26w_pct": 148.41, "excess_return_13w_pct": 1.47, "excess_return_26w_pct": 133.89, "benchmark": "^GSPC", "rsi14": 48.79, "rsi14_usable": true, "distance_from_52w_high_pct": -13.07, "distance_from_52w_low_pct": 163.76, "note": null}, "consensus_revision": {"latest_snapshot": {"file": "DD_universe_EPS_estimates_20260904.xlsx", "date": "2026-09-04", "fy1": 3.82, "fy2": 4.56, "fy3": 4.94}, "previous_snapshot": {"file": "DD_universe_EPS_estimates_20260828.xlsx", "date": "2026-08-28", "fy1": 3.44, "fy2": 4.08, "fy3": 4.44}, "snapshot_90d_prior": {"file": "DD_universe_EPS_estimates_20260604.xlsx", "date": "2026-06-04", "fy1": 3.41, "fy2": 4.01, "fy3": 4.26}, "fy1": {"revision_pct": 11.05, "from": 3.44, "to": 3.82, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy2": {"revision_pct": 11.76, "from": 4.08, "to": 4.56, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy3": {"revision_pct": 11.26, "from": 4.44, "to": 4.94, "from_date": "2026-08-28", "to_date": "2026-09-04"}, "fy1_revision_90d_pct": 12.02, "fy2_revision_90d_pct": 13.72, "fy3_revision_90d_pct": 15.96, "stale": false, "note": null}, "peer_financials": {"HPE": {"gross_margin_pct": 33.9, "operating_margin_pct": 5.79, "fcf_margin_pct": 10.28, "rd_intensity_pct": 8.17, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "DELL": {"gross_margin_pct": 19.07, "operating_margin_pct": 8.1, "fcf_margin_pct": 7.05, "rd_intensity_pct": 2.48, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "SMCI": {"gross_margin_pct": 8.39, "operating_margin_pct": 4.48, "fcf_margin_pct": -20.33, "rd_intensity_pct": 2.23, "fiscal_period_as_of": "TTM ending 2026-03-31（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "NTAP": {"gross_margin_pct": 70.74, "operating_margin_pct": 24.48, "fcf_margin_pct": 26.99, "rd_intensity_pct": 14.31, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}, "CSCO": {"gross_margin_pct": 64.33, "operating_margin_pct": 23.72, "fcf_margin_pct": 19.41, "rd_intensity_pct": 15.66, "fiscal_period_as_of": "TTM ending 2026-04-30（4季加總）", "source": "yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）", "note": null}}, "edgar_concentrations": {"filing_type": "10-Q", "filing_date": "2026-09-03", "url": "https://www.sec.gov/Archives/edgar/data/1645590/000164559026000080/hpe-20260731.htm", "excerpt": null, "note": "filing 全文內找不到 concentration／customer concentration 相關段落"}, "latest_quarter_kpis": {"_required": true, "quarter": "Q3 FY2026（季末 2026-07-31，公告於 2026-09-02）", "items": [{"metric": "營收（GAAP net revenue）", "value": 12213, "unit": "US$M", "as_of": "Q3 FY2026（季末 2026-07-31，公告於 2026-09-02）", "source": "公司新聞稿 investors.hpe.com「HPE reports fiscal 2026 third quarter results」PDF（https://investors.hpe.com/~/media/Files/H/HP-Enterprise-IR/documents/q3-2026/q3-2026-earnings-press-release.pdf），Condensed Consolidated Statements of Earnings 表", "vs_consensus": "YoY +33.7%（vs Q3 FY25 $9,136M）、QoQ +14.4%（vs Q2 FY26 $10,678M），皆為公司自揭精確值（新聞稿標題另有四捨五入「+34%」口徑）；對比賣方共識 revenue ~$11.89–11.93B（來源：web_search 綜合財經媒體引述之分析師估計，非單一機構一手數字），本季為 beat ~2.6–2.7%", "prior_quarter": "Q2 FY2026: $10,678M"}, {"metric": "Non-GAAP 營業利益／利益率", "value": 16.2, "unit": "%", "as_of": "Q3 FY2026（季末 2026-07-31，公告於 2026-09-02）", "source": "同上新聞稿 Reconciliation of GAAP to Non-GAAP measures 表；Non-GAAP earnings from operations = $1,979M", "vs_consensus": "較 Q3 FY25 的 8.5% 大幅擴張 770bp、較 Q2 FY26 的 13.3% 擴張 290bp", "prior_quarter": "Q2 FY2026: 13.3%（non-GAAP OP $1,423M）"}, {"metric": "GAAP 營業利益／利益率", "value": 11.4, "unit": "%", "as_of": "Q3 FY2026（季末 2026-07-31，公告於 2026-09-02）", "source": "同上新聞稿 Condensed Consolidated Statements of Earnings；GAAP earnings from operations = $1,393M", "vs_consensus": "較 Q3 FY25 的 2.7% 擴張 870bp、較 Q2 FY26 的 7.0% 擴張 440bp", "prior_quarter": "Q2 FY2026: 7.0%（GAAP OP $747M）"}, {"metric": "自由現金流（FCF）", "value": 958, "unit": "US$M", "as_of": "Q3 FY2026（季末 2026-07-31，公告於 2026-09-02）", "source": "同上新聞稿 Free cash flow reconciliation（cash flow from operations $1,641M − net capex $653M − FX 影響 $30M）", "vs_consensus": "YoY +$168M（vs Q3 FY25 $790M），公司稱為歷年同期（Q3）新高；管理層同時上修 FY26 FCF guidance 至 ≥$3.75B", "prior_quarter": "Q2 FY2026: $915M"}, {"metric": "SBC 占營收 / 占 Non-GAAP 營業利益", "value": 1.35, "unit": "%（占營收）", "as_of": "Q3 FY2026（季末 2026-07-31，公告於 2026-09-02）", "source": "同上新聞稿 Non-GAAP 營業利益 reconciliation；SBC 總額 $165M（其中 $18M 落在 COGS、其餘落在 opex），營收 $12,213M，non-GAAP OP $1,979M", "vs_consensus": "占 non-GAAP 營業利益 8.34%（$165M / $1,979M）；Q2 FY26 SBC $218M 占營收 2.04%／占 non-GAAP OP 15.3%，本季 SBC 稀釋度較上季下降", "prior_quarter": "Q2 FY2026: SBC $218M（占營收 2.04%）"}, {"metric": "管理層指引：Q4 FY2026", "value": null, "unit": "guidance range", "as_of": "公告於 2026-09-02，指引期間 Q4 FY2026（季末約 2026-10-31）", "source": "同上新聞稿「Fiscal 2026 Fourth Quarter Outlook」段", "vs_consensus": "營收 $13.9B–$14.8B；GAAP diluted EPS $1.12–$1.22；Non-GAAP diluted EPS $1.20–$1.30。同時上修 FY26 全年：營收成長率 34%–37%、GAAP EPS $2.93–$3.03、Non-GAAP EPS $3.75–$3.85、FCF ≥$3.75B；並首次揭露 FY2027 框架：營收成長 13%–17%、Non-GAAP EPS 成長 16%–20%（隱含 EPS $4.40–$4.60）、non-GAAP 營業利益率 14%–15%、FCF ≥$5.0B", "prior_quarter": "Q3 FY2026 原始 guidance（Q2 法說會給）：GAAP EPS $0.84–$0.89、Non-GAAP EPS $0.88–$0.93——本季實際 $1.06／$1.11 皆超出上緣"}, {"metric": "訂單成長（Orders growth，硬體/設備 archetype 追加：book-to-bill 代理指標）", "value": 42, "unit": "% YoY（normalized basis，公司口徑）", "as_of": "Q3 FY2026（季末 2026-07-31，公告於 2026-09-02）", "source": "法說會逐字稿（web_search 綜合 investing.com／Benzinga／Seeking Alpha 轉載之逐字稿內容，非公司新聞稿本文——新聞稿本文僅質性描述「orders and backlog at a record level」未揭露總公司訂單成長百分比，屬管理層口頭揭露）", "vs_consensus": "訂單成長顯著快於營收成長（+33.7% YoY），顯示 book-to-bill > 1；子項：Networking 訂單 +36% YoY（成長速度約營收 3.5 倍）、AI 系統訂單本季 $2.4B（QoQ +30%+）、Networks-for-AI 累計訂單 $2.2B（已超越 FY26 目標，目標上修至 $2.5–3.0B）", "prior_quarter": "無公司正式揭露之上季同口徑數字（該指標為法說會口頭揭露，非新聞稿標準表格項目，無法對照 Q2 FY26 精確值）"}, {"metric": "供給端限制／產能利用率代理（硬體/設備 archetype 追加）", "value": null, "unit": "qualitative", "as_of": "Q3 FY2026 法說會，2026-09-02", "source": "法說會逐字稿（web_search 綜合轉載，同上；新聞稿本文未揭露此段）", "vs_consensus": "管理層明確點名 DDR5／DDR4／NAND／晶圓（wafer）產能為限制因子，並預期此供給緊張將延續至 2027；AI 系統 backlog 本季 QoQ +14% 創新高（絕對金額未揭露），Data Center Networking 營收轉換受出貨時程與供給限制影響", "prior_quarter": null}]}}
```

### coverage（逐軸表格）
| id | dir | as_of | claim | source | affects |
|---|---|---|---|---|---|
| competitive_share_entrants#0 | - | 2026-03-19 | IDC 2025年Q4全球伺服器追蹤報告（2026-03-19發布）：HPE排名滑落至第五、市佔3.1%（營收38億美元），較去年同期42.4億美元衰退8.6%；Dell以125億美元營收、約10%份額居冠。IDC分析師指出HPE衰退部分歸因於Dell更廣的產品組合優勢、Lenovo的競爭動作，以及超大規模業者自行設計伺服器（custom servers）分食OEM採購。 | Network World — "IDC: Dell leads server market driven by AI infrastructure needs" (https://www.networkworld.com/article/4147841/idc-dell-leads-server-market-driven-by-ai-infrastructure-needs.html) | moat_trend,thesis.R,decision_inputs.bear |
| competitive_share_entrants#1 | + | 2025-09-16 | 收購Juniper後，HPE網通事業2025財年Q3營收年增54.3%至17.3億美元、營運利益年增43%至3.6億美元（Intelligent Edge營業利益率22.7%），使HPE首度跨入路由器／資料中心網通／防火牆領域與Cisco、Arista正面交鋒（先前僅聚焦校園網通）。 | Yahoo Finance — "HPE's Networking Business Improves: What's Driving the Growth?" (https://finance.yahoo.com/news/hpes-networking-business-improves-whats-142200588.html) | moat_trend,thesis.H |
| competitive_share_entrants#2 | - | 2025-03-31 | IDC 2025年Q1企業WLAN市場資料：Cisco市佔39.5%、HPE Aruba 15.9%、Juniper 5.3%——即便將Juniper併入計算，兩者合計（約21.2%）仍大幅落後Cisco，顯示網通份額消長對HPE仍不利。 | Channel Partners Conference — "HPE-Jupiter's Market Impact" (https://channelpartnersconference.com/article/hpe-jupiter-market-impact/) | moat_trend,thesis.R |
| customer_second_source#0 | - | 2026-03-19 | 同份IDC 2025 Q4伺服器市佔報告（2026-03-19發布）指出，HPE與Dell面臨的挑戰之一是超大規模業者自行設計伺服器（hyperscale providers designing custom servers），此為HPE伺服器市佔下滑的歸因之一，反映客戶端自製（in-house）趨勢正削弱對OEM品牌伺服器供應商的採購依賴。 | Network World — "IDC: Dell leads server market driven by AI infrastructure needs" (https://www.networkworld.com/article/4147841/idc-dell-leads-server-market-driven-by-ai-infrastructure-needs.html) | moat_trend,thesis.R,decision_inputs.bear |
| customer_second_source#1 | - | 2026-01-31 | 白牌／ODM交換器在超大規模雲端業者資料中心的採用率已達埠數／部署量30-40%區間（IDC統計：ODM直售2025年Q3年增逾150%），反映超大規模客戶傾向自行拆解硬體、跑開源NOS，而非採購品牌網通設備（含HPE Aruba/Juniper）——此為客戶端「自製取代品牌供應商」的產業級證據，非HPE個案揭露。 | IEEE ComSoc Technology Blog — "Analysis: Ethernet gains on InfiniBand in data center connectivity market; White Box/ODM vendors top choice for AI hyperscalers" (https://techblog.comsoc.org/2026/01/31/analysis-ethernet-gains-on-infiniband-in-data-center-connectivity-market-white-box-odm-vendors-top-choice-for-ai-hyperscalers/) | moat_trend,thesis.R,decision_inputs.bear |
| customer_second_source#2 | 0 | 2026-09-04 | HPE FY2026 Q3季報後（季末後追加）簽下與單一大型雲端運算公司的35億美元AI伺服器訂單，顯示HPE AI Systems訂單積壓集中於少數超大規模／雲端客戶；報導未揭露該客戶或其他大客戶有導入第二供應商或自製（in-house）的具體行動。 | Futurum Group — "HPE Q3 FY 2026: AI Infrastructure Demand Strengthens Outlook" (https://futurumgroup.com/insights/hpe-q3-fy-2026-ai-infrastructure-demand-strengthens-outlook/) | decision_inputs.bear,thesis.R |
| customer_concentration_credit#0 | + | 2019-10-31 | HPE FY2019 Form 10-K disclosed that no single customer represented 10% or more of HPE's total net revenue in any fiscal year presented; this search did not independently retrieve the equivalent concentration-disclosure text from the current FY2025 10-K to confirm the figure still holds. | Hewlett Packard Enterprise Co, Form 10-K FY2019, SEC EDGAR | decision_inputs.bear,thesis.R |
| customer_concentration_credit#1 | - | 2026-05 | HPE announced (May 2026) a unified global distribution model designating Ingram Micro and TD SYNNEX as its two global distributors covering its full portfolio (networking, cloud, AI, servers, storage, services), consolidating go-to-market from a broader partner base down to two primary channel partners. | StockTitan / CloudNews / Investing.com coverage of HPE global distribution announcement | decision_inputs.bear,thesis.R |
| customer_concentration_credit#2 | 0 | 2026-09-02 | HPE and Oracle announced (2026-09-02) an expanded networking collaboration for a 'gigawatt-scale' AI cloud infrastructure buildout using HPE Juniper switching/routing equipment (Broadcom Tomahawk 6-based QFX, Juniper Express 5-based PTX); per earnings coverage this Oracle contribution sits on top of HPE's existing revenue guidance, i.e. incremental revenue concentrated in a single customer relationship. | HPE press release 2026-09-02; SDxCentral, 'HPE caps stellar Q3 with gigawatt scale networking deal with Oracle' | decision_inputs.bear,thesis.H |
| customer_concentration_credit#3 | 0 | 2026-09-02 | Alongside Q3 FY26 results (reported 2026-09-02), HPE disclosed a new $3.5 billion inferencing deal with an unnamed hyperscaler customer, adding to a small number of very large AI-infrastructure contracts now driving incremental revenue growth. | Investing.com, 'HPE Q3 FY26 slides: record AI demand drives 34% revenue surge' | decision_inputs.bear,thesis.H |
| customer_concentration_credit#4 | - | 2026-09 | Analyst commentary flags that HPE's AI order book exhibits 'lumpiness of large AI system deals,' where a small number of major contracts drive quarter-to-quarter revenue timing, and that HPE is pre-buying scarce components (DDR5 memory, NAND) ahead of shipment — converting revenue-timing risk tied to these concentrated deals into balance-sheet exposure if AI order pricing softens before parts ship. | Yahoo Finance / AOL syndication, 'HPE Cannot Build AI Servers Fast Enough. Is the Stock Still Cheap?' | decision_inputs.bear,thesis.R |
| supply_demand_durability#0 | 0 | 2026-01-26 | Multiple semiconductor industry analysts and executives describe the current DRAM/HBM/NAND memory shortage feeding AI server production as structural rather than cyclical, driven by the three largest memory manufacturers (Samsung, SK Hynix, Micron) reallocating cleanroom capacity toward higher-margin HBM and enterprise DDR5 with no stated plans for aggressive new capacity expansion; data centers are estimated to consume up to 70% of all memory chips produced in 2026, versus under 5% three years earlier. | CNBC, 'Memory chip shortage to last through 2027, semiconductor boss says' (2026-01-26); HBS blog 'AI Memory Shortage 2026' | thesis.H,decision_inputs.bear |
| supply_demand_durability#1 | 0 | 2026-02 | Intel CEO Lip-Bu Tan stated in February 2026 that memory shortages are expected to persist until 2028, a more pessimistic timeline than other industry forecasts pointing to resolution around 2027; separately, meaningful price relief for memory is not expected until 2028-2029 assuming planned fab projects complete on schedule and AI demand growth moderates. | Industry coverage citing Intel CEO comments (reported via CNBC/HBS/Avnet 2026 memory-shortage articles) | thesis.H |
| supply_demand_durability#2 | 0 | 2026 | A Goldman Sachs supply-demand model projects DRAM supply-demand gaps of 5.0%, 5.9%, and 3.9% for 2026-2028 respectively (NAND gaps of 4.4%, 4.6%, and 3.0%), and expects the semiconductor wafer-fab-equipment (WFE) upcycle to extend through at least 2028 as component demand is sustained by delayed AI projects coming online. | BigGo Finance, summarizing Goldman Sachs research, 'AI Capex Resilience Runs Through the Semiconductor Supply Chain, Equipment Upcycle Could Extend to 2028' | thesis.H,triggers |
| supply_demand_durability#3 | + | 2026 | During 2026 earnings calls, hyperscaler executives stated that AI infrastructure demand continues to outpace available capacity: Microsoft described current conditions as an 'extremely extreme moment' of demand exceeding supply; Amazon CEO Andy Jassy said AWS 'will still not have enough capacity to meet all the demand' in 2026 and expects the dynamic to continue into 2027; Alphabet said it expects capex to increase significantly in 2027 because it remains supply-constrained. | Aggregated hyperscaler earnings-call commentary via io-fund.com, Sesame Disk, and AL Capital Advisory 2026 AI-capex research notes | thesis.H,triggers |
| supply_demand_durability#4 | 0 | 2026 | Approximately 30-50% of planned 2026 AI data-center capacity is projected to slip into 2027-2028 due to power-grid interconnection queues and construction bottlenecks, according to industry infrastructure analysis — a supply-side timing constraint distinct from the chip-level shortage. | Accuris blog, 'How AI Data Centers Are Reshaping Electronic Component Supply in 2026' | thesis.H,triggers |
| supply_demand_durability#5 | + | 2026-09-02 | HPE reported record Q3 FY26 revenue of $12.2 billion (+34% YoY, reported 2026-09-02) driven by record AI demand, raised its cumulative Networking-for-AI order guidance to $2.5-3.0 billion by fiscal year-end 2026, and management/analyst commentary describe HPE as currently supply- rather than demand-constrained on AI servers ('cannot build AI servers fast enough'). | Investing.com, 'HPE Q3 FY26 slides: record AI demand drives 34% revenue surge'; Yahoo Finance, 'HPE Cannot Build AI Servers Fast Enough. Is the Stock Still Cheap?' | thesis.H,moat_trend |
| regulatory_antitrust#0 | 0 | 2025-06-27 | DOJ filed suit (2025-01-30, N.D. Cal.) to block HPE's $14B acquisition of Juniper Networks under Clayton Act §7, alleging the merger would let two firms control 70% of the enterprise-grade WLAN market; HPE/Juniper/DOJ settled on 2025-06-27 with HPE agreeing to divest its global Instant On campus/branch WLAN business and license Juniper's Mist AI Ops source code, after which the merger closed. | Gibson Dunn, "Gibson Dunn Wins Approval of HPE's Settlement of DOJ Challenge to $14 Billion Juniper Merger"; American Bar Association, "DOJ Declares Enterprise Wireless Merger Settlement a Victory" | moat_trend,decision_inputs.bear,triggers |
| regulatory_antitrust#1 | - | 2026-03-23 | Twelve state Attorneys General plus D.C. intervened in the Tunney Act review of the HPE/Juniper settlement (motion granted after a 2025-11-18 hearing), alleging the DOJ settlement process was influenced by corporate lobbying that bypassed antitrust staff; a federal judge in the Northern District of California heard arguments in March 2026 on whether the DOJ improperly approved the settlement. | Economic Liberties, "Court Lets States Join HPE-Juniper Case as Allegations of Corrupt DOJ Process and Meddling Mount"; California DOJ (Attorney General Bonta) press release; Axios, "Trump's antitrust regime heads to court" (2026-03-23) | decision_inputs.bear,triggers,thesis.R |
| regulatory_antitrust#2 | + | 2026-08-12 | The U.S. District Court for the Northern District of California approved the HPE/DOJ Juniper settlement on 2026-08-12, over continued opposition from the intervening state Attorneys General. | Gibson Dunn, "Gibson Dunn Wins Approval of HPE's Settlement of DOJ Challenge to $14 Billion Juniper Merger" | decision_inputs.bear,triggers |
| regulatory_antitrust#3 | - | 2026-03-25 | As of March 2026, HPE was struggling to find serious buyers for the DOJ-mandated Instant On divestiture (required within 180 days of the June 2025 settlement); low offers undercut the merger remedy and the business's long-term ownership remained unresolved, per reporting current through the court's August 2026 settlement approval. | Bloomberg, "HPE Struggled With Asset Sale Required in DOJ Antitrust Deal" (2026-03-23); The Star, "Hewlett Packard struggles with asset sale required in antitrust deal"; PYMNTS, "Low Offers for Instant On Undercut HPE's Juniper Merger Remedy" | decision_inputs.bear,triggers |
| regulatory_antitrust#4 | 0 | 2025-01-01 | The European Commission (Case M.11457) reviewed HPE's Juniper acquisition across worldwide WLAN equipment/access points, EEA Ethernet campus switches, and worldwide datacentre switches markets, and cleared the deal, finding HPE and Juniper are not each other's closest competitors and customers retain countervailing buyer power; HPE holds roughly 14.5% global server market share (top-3 position) as of late 2025. | European Commission DG Competition, Case M.11457 - HPE/JUNIPER decision; Digital Watch Observatory, "European Commission approves HPE's acquisition of Juniper Networks" | moat_trend |
| reg_tariff_export#0 | - | 2026-01-15 | White House Proclamation 11002 (2026-01-14, effective 2026-01-15) imposed a 25% Section 232 tariff on a defined set of advanced semiconductors, with carve-outs for data centers, R&D, and startups that kept the initial Phase 1 impact limited. | The White House, Presidential Actions, "Adjusting Imports of Semiconductors, Semiconductor Manufacturing Equipment, and Their Derivative Products Into the United States"; EY Global Tax News, "US Section 232 proclamation imposes 25% tariff on certain semiconductors" | decision_inputs.bear,valuation,thesis.R |
| reg_tariff_export#1 | - | 2026-08-01 | DRAM and NAND now make up over half the bill of materials on a traditional server per industry commentary on HPE's product cost structure, meaning HPE's server line is disproportionately exposed to semiconductor-linked tariff increases; memory-dense configurations (servers, high-RAM workstations, large-storage gear) are flagged as hit hardest. | getuniqcli.com, "Beat the 2026 IT Price Increase: The Federal & Enterprise Buyer's Guide to Ordering Before the August Effective Dates" | decision_inputs.bear,valuation |
| reg_tariff_export#2 | - | 2026-09-02 | Commerce Secretary Howard Lutnick confirmed on 2026-09-02 that the administration is preparing a Phase 2 expansion of Section 232 semiconductor tariffs targeting chips, servers, and polysilicon — categories including servers that were largely sheltered under Phase 1. | TariffLens, "The July 1 Semiconductor Tariff Review: What Happens Next Could Double Your Duty Bill"; ajprotech.com, "Section 232 Phase 2: The Tariff Question Nobody Asks at Hardware Kickoff" | decision_inputs.bear,valuation,triggers |
| reg_tariff_export#3 | 0 | 2026-06-22 | China's Ministry of Commerce added 10 US entities (rare earth/defense-linked companies such as MP Materials and USA Rare Earth) to its dual-use export control list effective 2026-06-22, in response to US expansion of the Pentagon's 1260H China military-industrial entity list; search results do not indicate HPE itself was named on this or any other China export-control/entity list as of the query date. | Global Times, "China adds 10 US entities to export control list following US expansion of 'China military-industrial entity' list"; Arnold & Porter, "China Imposes Export Control and Government Procurement Restrictions on Designated U.S. Companies" | decision_inputs.bear |
| geo_supply_chain#0 | - | 2026-03 (approx，文章無明確發布日，依內容提及 Rubin 世代推估) | HPE 的 AI 伺服器（含 Compute XD700 等）搭載的 Nvidia GPU 全數由 TSMC 於台灣製造，為 AI 供應鏈最大的地緣風險集中點；HBM（SK Hynix 為主）與 CoWoS 先進封裝為另兩個獨立瓶頸，系統整合（HPE 等 OEM）再加 8-16 週交期，採購到上線一般需 3-6 個月 | The GPU Supply Chain: From Silicon Foundry to Server Rack — disintermediate.global | decision_inputs.bear,triggers,moat_trend |
| geo_supply_chain#1 | + | 2026-02-10 | HPE 已完成出脫 H3C（中國合資子公司）多數股權，公司描述為轉型成『更乾淨的西方基礎設施資產』，壓縮中國/地緣風險溢價；董事會與稽核委員會定期收到地緣政治風險簡報並已針對台海等地區實施緩解措施 | Hewlett Packard Enterprise Co - Form DEF 14A FY2025 (SEC, hpe-20260210.htm) | moat_trend,decision_inputs.bear |
| geo_supply_chain#2 | - | 2026-02-10 | 美國對台灣、印度、越南等主要科技製造國加徵 26%-49% 關稅，半導體暫時獲豁免，但仰賴跨國供應鏈的科技公司仍面臨貿易政策不穩定的新風險（HPE 10-Q/proxy 揭露此為風險因子） | Hewlett Packard Enterprise Co - Form DEF 14A FY2025 (SEC, hpe-20260210.htm) | decision_inputs.bear,triggers |
| geo_supply_chain#3 | + | 2026-03-25 | HPE 中國營收暴露極低（H3C 出脫後），相較 Huawei 中國約占其校園交換器營收 40%，形成競爭上的地緣政治保險；HPE-Juniper 併購被定位為協助美方在東南亞、東歐等策略市場提供 Huawei 之外的西方替代方案，屬國安層級戰略 | The Networking Transformation: A Deep Dive into HPE in 2026 — FinancialContent/Finterra | moat_trend,thesis.H |
| geo_supply_chain#4 | + | 2025-07-02 | HPE 收購 Juniper Networks（140 億美元）在美國白宮介入後獲主管機關核准（原先遭部門以國安疑慮攔阻），交易已於 2025 年 7 月完成 | HPE gets approval for $14B acquisition of Juniper — Tom's Hardware | moat_trend,thesis.H |
| geo_supply_chain#5 | - | 2025-02 (approx，裁員公告期) | 關稅衝擊約侵蝕 1.2 億美元毛利，使原訂 3.5 億美元成本節省目標中，須靠裁員彌補的缺口壓力升高至約 2.3 億美元（HPE 已裁員 2500 人） | HPE cuts 2,500 jobs, remains committed to Juniper buy, faces tariff issues — Network World | decision_inputs.bear,valuation |
| end_markets#0 | + | 2026-09-02 | HPE FY2026 Q3（截至 2026-09-02 公布）Cloud & AI 分部營收 90 億美元，年增 25.4%；AI 系統訂單達 24 億美元，季增逾 30%，公司預期 Q4 AI 系統營收將季增，AI 滲透正從雲端服務商擴散到企業端 agentic AI／推論工作負載，同步帶動傳統伺服器、儲存與私有雲需求 | HPE Q3 FY2026 results / Constellation Research / Futurum Group | thesis.H,valuation |
| end_markets#1 | + | 2026-03 (Q1 FY2026 財報期) | Networking 分部（Aruba + Juniper）FY2026 Q1 營收 27.06 億美元、年增 151.5%（主要由 2025 年 7 月完成的 Juniper 併購貢獻），Networking 已占 HPE 整體營收約 30%、卻貢獻超過一半的獲利；FY2026 Q3 Networking 營收進一步達 29 億美元 | SDxCentral (HPE networking revenue soars) / Yahoo Finance (Networking now 30% of HPE revenue) | thesis.H,moat_trend |
| end_markets#2 | 0 | 2026-03 (Q1 FY2026 財報期) | FY2026 起 HPE 將 Server／Storage／Financial Services 合併為單一 Cloud & AI 報表分部；該分部 Q1 FY2026 營收 63 億美元、年減 2.7%，其中伺服器營收 42 億美元、儲存營收 11 億美元；Hybrid Cloud（儲存）業務約占整體營收 16.17%，在外部 OEM 企業儲存市場面對 Dell 與 Pure Storage 競爭 | mlq.ai earnings highlight (Juniper acquisition bolsters HPE's networking) / SDxCentral | thesis.R,valuation |
| end_markets#3 | + | 2026-05-19 (Gartner)；2026-01-20 (TrendForce) | AI 伺服器市場需求展望分歧但普遍看多：TrendForce 預估 2026 年全球 AI 伺服器出貨年增逾 28%、ASIC 系統占比上升；Gartner 預估 2026 年全球 AI 支出年增 47% 達 2.59 兆美元，AI 最佳化伺服器支出未來五年將成長三倍成為最大子項；Grand View Research 估 AI 伺服器市場 2025 年 1317 億美元、2026 年成長至 1570 億美元（CAGR 21.2% 至 2033 年 5981 億美元），另有機構估值差異達數量級（如 Fortune Business Insights 估 2026 年僅 262 億美元），顯示各機構口徑與範圍定義不一致 | TrendForce (Global AI Server Shipments Forecast) / Gartner Newsroom / Grand View Research AI server market report | thesis.H,valuation |
| substitute_technology#0 | - | 2026 | 白牌/解構化交換器(white-box switching)市場快速成長：2025年市場規模US$2.95B、預估2027年達US$3.87B，2026-2035年CAGR 14.6%；近63%大型資料中心正轉向解構化交換方案，58%企業偏好vendor-neutral硬體——直接挑戰Cisco、Juniper、Huawei等傳統專有交換器供應商賴以維生的vendor lock-in商業模式（HPE收購Juniper後亦暴露於此風險）。 | Global Growth Insights / Business Research Insights "White Box Switches Market" market reports | moat_trend,thesis.R |
| substitute_technology#1 | + | 2026-03-25 | HPE-Juniper組合（2025年底完成的US$14B併購）在「AI驅動校園網路」與雲原生網路區隔正在搶市占，對手Cisco仍主導傳統交換器市場；Super Micro因2026年出口管制相關調查/起訴陷入法律與監理麻煩，導致企業客戶「flight to quality」轉單回HPE——顯示HPE短期內受益於對手問題而非被替代技術顛覆。 | FinancialContent "The Networking Transformation: A Deep Dive into HPE (2026)"; IT Pro "HPE's networking push dominated Discover 2026" | moat_trend,thesis.H |
| channel_business_model_shift#0 | + | 2026-05-14 | HPE於2026-05-14宣布全球通路重組，將原本分散的區域經銷體系整併為兩家全球經銷夥伴（Ingram Micro、TD SYNNEX），目的是簡化夥伴介接、統一庫存與支援，以承載Juniper併購後擴大的產品組合與AI/混合雲方案；消息公布後股價當日上漲6.9%。 | Distribution Strategy Group "HPE Restructures Global Distribution Around Ingram Micro, TD SYNNEX"; Yahoo Finance "Why Hewlett Packard Enterprise (HPE) Is Up 6.9% After Reshaping Its Global Distribution Model" | thesis.H,moat_trend |
| channel_business_model_shift#1 | 0 | 2026 | CRN Asia報導HPE正推動通路夥伴從單純轉售(resale)轉向附加價值服務，AI、虛擬化與網路產品組合正在壓縮傳統轉售通路的利潤率結構。 | CRN Asia "HPE pushes partners beyond resale as AI, virtualisation and networking reshape channel margins" | thesis.H,valuation |
| channel_business_model_shift#2 | 0 | 2026-05-04 | HPE GreenLake消費制/訂閱模式FY2026目標營收US$3.5B、平台上約50,000個客戶；但產業評論指出消費制定價已從差異化優勢變成產業標配（不再是HPE獨有賣點），弱化其作為護城河的邊際貢獻。 | TechTarget "What is HPE GreenLake and how does it work?"; news-articles.net "HPE's Strategic Pivot: AI-Native Architecture and the GreenLake Consumption Model" | moat_trend,thesis.R,valuation |
| channel_business_model_shift#3 | 0 | 2026 | ITdaily報導HPE Discover 2026主舞台上GreenLake曝光度明顯低於往年（幾乎未被重點提及），顯示公司對外敘事已從消費制訂閱模式轉向AI基礎設施/網路定位。 | ITdaily "Barely any GreenLake on stage at HPE, and that's actually not such a bad thing - HPE Discover 2026" | thesis.R,moat_trend |
| capital_markets_pricing#0 | + | 2026-09-02 | HPE fiscal 2026 Q3（截至 2026-07-31，2026-09-02 公布）營收 $12.2B（+34% YoY）優於分析師預估約 $11.9B，non-GAAP EPS $1.11 優於共識約 $0.93，全線報喜（beat on every line） | Tickeron - "HPE (HPE) Delivers +34% Revenue Growth in Q3 Fiscal 2026 as AI Demand Accelerates"; StockTitan - "HPE Q3 Earnings: $12.2B Revenue, Outlook Raised" | thesis.H,valuation,decision_inputs.bear |
| capital_markets_pricing#1 | + | 2026-09-02 | HPE 同步上修 FY2026 財測：營收成長由 29%-33% 上修至 34%-37%、non-GAAP EPS 由 $3.35-3.45 上修至 $3.75-3.85、FCF 上修至至少 $3.75B；並首次給出 FY2027 展望：EPS 成長 16%-20%（前次 12%-16%）、營收成長框架 13%-17%、FCF 至少 $5B | HPE newsroom press release - "HPE reports fiscal 2026 third quarter results" (hpe.com/us/en/newsroom); StockTitan - "HPE Q3 Earnings: $12.2B Revenue, Outlook Raised" | thesis.H,valuation,triggers |
| capital_markets_pricing#2 | - | 2026-09-03 | 儘管財測全面上修、財報全線超預期，HPE 股價於財報後仍下跌約 5%，市場解讀為記憶體／CPU／硬碟供給短缺限制出貨能力（supply constraints）蓋過上修財測的利多 | Yahoo Finance / 247wallst.com - "Hewlett Packard Enterprise Falls 5% as Supply Constraints Overshadow Raised Guidance" | thesis.R,decision_inputs.bear,triggers |
| capital_markets_pricing#3 | 0 | 2026-09-02 | 財報後分析師目標價出現明顯分歧：BofA 上調至 $88（自 $82，維持 Buy）；UBS 下調至 $59（自 $65，維持 Neutral）；Piper Sandler 下調至 $57（自 $63，維持 Neutral）——同一份財報後看多與看穩健分析師的目標價差達 $31（$57–$88） | Benzinga - "Hewlett Packard Enterprise Likely To Report Higher Q3 Earnings; These Most Accurate Analysts Revise Forecasts Ahead of Earnings Call" | valuation,thesis.H,thesis.R |
| capital_markets_pricing#4 | 0 | 2026-09-03 | 財報後市場論述出現「利多是否已price in」的分歧觀點：tikr.com 發文標題直指「HPE Q3 全線報喜，但股價上檔空間看似已反映在價格內（upside looks priced in）」 | TIKR - "HPE's Q3 Earnings Beat on Every Line. The Stock's Upside Looks Priced In." | valuation,decision_inputs.bear |
| capital_markets_pricing#5 | 0 | 2026-09-04 | 彙總站（S&P Global／WallStreetZen 等）財報前後的平均目標價落在約 $67.48–$69.81 區間（23 位分析師 $67.48、17 位 $69.18、16 位 $69.81），共識評等為 Buy／Moderate Buy；相對 numbers.price_at_dd $52.00，隱含平均目標價較現價有顯著溢價，但財報後個別分析師目標價已出現 $57–$88 的寬幅分歧（見上一條），彙總平均可能落後最新個別下修/上修 | StockAnalysis.com - HPE Stock Forecast; WallStreetZen - HPE Stock Forecast & Predictions | valuation |
| major_events#0 | 0 | 2025-07-02 | HPE closed its ~$14 billion all-cash acquisition of Juniper Networks ($40.00/share) on July 2-10, 2025, roughly 18 months after the January 2024 deal announcement; the deal doubled the size of HPE's networking business and created HPE Aruba Networking + HPE Juniper Networking brands under former Juniper CEO Rami Rahim. | HPE press release, 'Hewlett Packard Enterprise closes acquisition of Juniper Networks' (hpe.com/us/en/newsroom, July 2025); RCR Wireless 'HPE closes on $14 billion Juniper acquisition' | moat_trend,thesis.H,valuation |
| major_events#1 | - | 2025-06-27 | DOJ's Antitrust Division sued on January 30, 2025 to block the HPE-Juniper deal, alleging it would substantially lessen competition in enterprise-grade WLAN solutions; the case was resolved via a Stipulation and Final Judgment filed June 27, 2025 requiring HPE to divest its Instant On wireless business and license Mist AIOps source code to a rival, allowing the deal to close without an upfront buyer for the divested assets. | DOJ Office of Public Affairs press release 'Justice Department Sues to Block Hewlett Packard Enterprise's Proposed $14 Billion Acquisition...'; Federal Register 'United States v. Hewlett Packard Enterprise Co. and Juniper Networks, Inc.; Proposed Final Judgment' (2025-07-10) | thesis.R,decision_inputs.bear |
| major_events#2 | - | 2025-11-19 | The DOJ's settlement terms drew political controversy: Minnesota AG Keith Ellison moved to intervene in the Tunney Act court review calling it an 'alleged corrupt' settlement, and House Judiciary Committee Democrats publicly rebuked the DOJ's handling of the HPE-Juniper merger settlement, requesting a comprehensive court review; DOJ filed its response to public comments defending the settlement on November 19, 2025. | Minnesota AG press release (ag.state.mn.us, 2025-10-16); House Judiciary Democrats press release (democrats-judiciary.house.gov); Federal Register 'Response of the United States to Public Comments on the Proposed Final Judgments' (2025-11-19) | thesis.R,decision_inputs.bear |
| major_events#3 | - | 2025-10-15 | HPE shares fell ~10% on October 15, 2025 after issuing FY2026 adjusted EPS guidance of $2.20-$2.40 (below the ~$2.40 analyst consensus) despite revenue growth guidance of 17-22%; commentary attributed the miss to margin pressure from a richer AI-systems mix/pricing dynamics and persistent DDR5/DDR4/NAND/wafer supply shortages limiting the company's ability to convert record order backlog into revenue. Stock was reported down as much as ~27% over the trailing month around that guide-down. | CNBC 'HPE stock sinks 10% on weak guidance for fiscal 2026' (2025-10-15); Nasdaq 'HPE Stock Plunges 27% in a Month: Hold Tight or Time to Let Go?' | thesis.H,decision_inputs.bear,triggers |
| major_events#4 | - | 2026-09-03 | In the most recent reported quarter (published around 2026-09-03), HPE shares fell ~5% even after raising guidance, as supply constraints (component shortages) overshadowed the raised outlook. | Yahoo Finance / 24/7 Wall St, 'Hewlett Packard Enterprise Falls 5% as Supply Constraints Overshadow Raised Guidance' (2026-09-03) | thesis.H,triggers |

### events（原樣）
```json
{
 "ma_merger": {
  "status": "found",
  "queries_run": [
   "HPE Juniper Networks acquisition 2025 2026 merger closed",
   "HPE server product recall warning letter DOJ antitrust Juniper 2025"
  ],
  "findings": [
   {
    "claim": "HPE closed its ~$14 billion all-cash acquisition of Juniper Networks ($40.00/share) on July 2-10, 2025, doubling the size of HPE's networking business (combined HPE Aruba Networking + HPE Juniper Networking).",
    "source": "HPE press release (hpe.com/us/en/newsroom, 2025-07); RCR Wireless 'HPE closes on $14 billion Juniper acquisition'",
    "as_of": "2025-07-02",
    "direction": "0",
    "affects": [
     "moat_trend",
     "thesis.H",
     "valuation"
    ]
   },
   {
    "claim": "DOJ sued January 30, 2025 to block the deal on WLAN antitrust grounds; resolved via divestiture (Instant On business) and Mist AIOps source-code licensing settlement filed June 27, 2025, which drew subsequent political controversy (MN AG intervention, House Judiciary Democrats rebuke) over alleged deal favoritism, with DOJ defending the settlement as of November 19, 2025.",
    "source": "DOJ OPA press release; Federal Register proposed/final judgment filings (2025-07-10, 2025-11-19); Minnesota AG press release (2025-10-16)",
    "as_of": "2025-11-19",
    "direction": "-",
    "affects": [
     "thesis.R",
     "decision_inputs.bear"
    ]
   }
  ],
  "note": ""
 },
 "lawsuit_class_action": {
  "status": "none",
  "queries_run": [
   "HPE class action lawsuit securities fraud 2025 2026",
   "Hewlett Packard Enterprise investors lawsuit stock drop guidance miss 2025"
  ],
  "findings": [],
  "note": "搜尋結果中的證券集體訴訟/和解（$39M settlement、equal pay settlement等）標的為 HP Inc.（2015年分拆後獨立上市法人），非 Hewlett Packard Enterprise (HPE)；未查得 HPE 本身近12個月有證券詐欺集體訴訟，即便10月財報guide-down後股價重挫亦未查到對應提告新聞。"
 },
 "clinical_fda": {
  "status": "none",
  "queries_run": [
   "Hewlett Packard Enterprise FDA clinical trial medical device 2025",
   "HPE product recall safety warning 2025 2026 servers"
  ],
  "findings": [],
  "note": "HPE 為企業級運算/網路硬體與雲端服務業者，非藥品/醫療器材業務，已查證無相關臨床試驗或 FDA 監管動作。"
 },
 "product_recall_warning": {
  "status": "none",
  "queries_run": [
   "HPE product recall safety warning 2025 2026 servers",
   "HPE server GreenLake security vulnerability warning FTC investigation 2025 2026"
  ],
  "findings": [],
  "note": "查得的僅為例行性資安漏洞 advisory（如 ProLiant RL300/AMD 系列於2025-10、ProLiant DL/ML/XD Alletra/Synergy 於2025-12、ProLiant DL/ML/XD/XL 於2026-03，均由 Canadian Centre for Cyber Security 轉發），屬廠商例行 patch 公告非產品下架/安全召回，未達重大事件門檻，不列為 finding。"
 },
 "sec_investigation_restatement": {
  "status": "none",
  "queries_run": [
   "Hewlett Packard Enterprise SEC investigation restatement 2025 2026",
   "HPE server GreenLake security vulnerability warning FTC investigation 2025 2026"
  ],
  "findings": [],
  "note": "查得的皆為例行 SEC 申報文件（10-Q/10-K/8-K/ARS），未查得 SEC 調查、傳票或財報重編相關新聞。"
 }
}
```

### prior_dd（原樣）
```json
{
 "status": "ok",
 "path": "docs/dd/DD_HPE_20260602.html",
 "date": "20260602",
 "schema": "v12.4",
 "dca_verdict": null,
 "dca_role": null,
 "price_at_dd": 47.0,
 "revlog": {
  "status": "ok",
  "text": "版本修訂紀錄\n\n2026-06-02（本份，v12.4）：Q2 FY2026 財報（6/1 盤後）後重新評估。verdict 維持 B（衛星候選），但內部組成大幅轉變：①Q2 大 beat（Rev +40%、NG EPS $0.79 +108%）+ FY26 EPS guide 由 $2.30-2.50 大升至 $3.35-3.45（+40%）+ FCF guide ≥$3.5B → thesis 由「待驗證」轉「已驗證」（H1/H2 強化）；②估值燈由上份 🟢 轉 🟠 偏貴（股價自上份 $33.10 已 +42% 至 $47，5Y 分位 ~87%，超多數 analyst PT）；③Networking OpMargin Q2 21.6%（上份監測點，guide FY27 mid-high 20s）。品質天花板維持 B（Server 商品化）。建議等回測 $38-42 再行動，不追 +96% 超漲。\n2026-05-18（上份，v12.4）：$33.10，B 衛星候選，估值燈 🟢，等待 Q2 Networking OpMargin 證據。\nInception DD：DD_HPE_20260518.html（2026-05-18），累積漂移對照基準。\n\n列印為 PDF"
 },
 "prior_meta": {
  "ticker": "HPE",
  "schema": "v12.4",
  "date": "2026-06-02",
  "price_at_dd": 47.0,
  "signal": "B",
  "trap": "🟡",
  "trap_label": "🟡 觀察期",
  "moat": "B",
  "val": "🟠",
  "ma": "✅",
  "regime": "正常",
  "quality_tier": "B",
  "fpe_fy2": 12.1,
  "pct_5y": 87,
  "peg_fy2": 0.92,
  "upside_short_pct": -6.0,
  "upside_mid_pct": 9.0,
  "upside_5y_pct": 40.0,
  "stress": {
   "pass": 1,
   "total": 2
  },
  "moat_score": 7.0,
  "moat_execution": 7.0,
  "moat_pricing_power": 7.0,
  "growth_durability": 6.0,
  "quality_score": 7.0,
  "ai_risk": "🟢",
  "long_term_confidence": "中",
  "verdict": "B",
  "inception_dd": "DD_HPE_20260518.html",
  "inception_date": "2026-05-18",
  "next_yoy_review_date": "2027-05-18",
  "drift_4w_pct": 50.0,
  "oneliner": "Q2FY26 Rev$10.7B+40%YoY beat／NG EPS$0.79+108%／FY26 guide大升$3.35-3.45(原$2.30-2.50+40%)／AI bookings$16.4B／FCF guide≥$3.5B／Fwd PE FY27 12x但5Y分位87%🟠+股價2週+42%遠超analyst PT($33-40)／B 觀望:等回測$38-42"
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
    "text": "Juniper 整合成功，Networking 成為高利潤成長引擎",
    "columns": {
     "2Y 驗證點": "FY27 Networking OpMargin mid-high 20s；synergy >$200M",
     "5Y 驗證點": "Networking 成為利潤主體",
     "10Y 驗證點": "Juniper/Aruba 守住企業網路份額",
     "數字門檻": "FY27 margin mid-high 20s（管理層 6/1）",
     "來源": "連 2 季 OpMargin"
    }
   },
   {
    "id": "H2",
    "text": "AI server + 主權 AI 訂單持續轉化為收入與 FCF",
    "columns": {
     "2Y 驗證點": "FY26 FCF ≥$3.5B；AI backlog 維持 + 轉收入",
     "5Y 驗證點": "FY27 FCF ≥$4.5B framework 兌現",
     "10Y 驗證點": "企業/主權自建 AI 需求結構性存在",
     "數字門檻": "FCF ≥$3.5B FY26 / ≥$4.5B FY27（管理層）",
     "來源": "連 2 季 AI backlog 淨增轉負 或 FCF 顯著落後"
    }
   },
   {
    "id": "H3",
    "text": "估值維持 re-rate（市場接受 HPE 為成長型混合體而非低倍數硬體商）",
    "columns": {
     "2Y 驗證點": "forward PE 維持 low-teens",
     "5Y 驗證點": "若 thesis 兌現，PE 可向 CSCO（中位）靠攏",
     "10Y 驗證點": "不因 cyclical 回落而 de-rate 回 8x",
     "數字門檻": "維持 PE >11x",
     "來源": "PE de-rate 回"
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
    "text": "動能反轉：股價 +42% 超漲後快速回檔",
    "columns": {
     "對應假設": "H3",
     "時間尺度": "⚡ 短期（1-2 季）",
     "監測指標": "股價 vs BB 上軌 / analyst PT",
     "警戒閾值": "跌破 $38（前波突破點）→ 動能破"
    }
   },
   {
    "id": "R2",
    "text": "AI server 毛利稀釋結構化（量增利不增）",
    "columns": {
     "對應假設": "H2",
     "時間尺度": "🔥 中期（4-6 季）",
     "監測指標": "Cloud & AI 段 OpMargin；整體 GM",
     "警戒閾值": "Cloud & AI OpMargin 連 2 季跌破 low-teens 或 GM"
    }
   },
   {
    "id": "R3",
    "text": "AI capex 週期見頂 + Juniper 整合/活動股東風險",
    "columns": {
     "對應假設": "H1/H2",
     "時間尺度": "🐢 長期（2+ 年）",
     "監測指標": "AI backlog 趨勢；Elliott/Irenic 動向；synergy 進度",
     "警戒閾值": "backlog 連 2 季降 或 強迫拆分 Juniper（需 ≥50% 機率才大動作）"
    }
   }
  ]
 },
 "triggers": {
  "status": "unavailable"
 },
 "inception_dd": {
  "path": "docs/dd/DD_HPE_20260518.html",
  "date": "20260518",
  "schema": "v12.3"
 },
 "dd_12m_ago": {
  "path": "docs/dd/DD_HPE_20260518.html",
  "date": "20260518",
  "days_from_365d_mark": 255
 }
}
```

### ledger（原樣）
```json
{
 "status": "ok",
 "canonical_entity": "HPE",
 "current_verdict": {
  "verdict": null,
  "fundamental_grade": "B",
  "date": "2026-06-02",
  "freshness": "aging",
  "source": "docs/dd/DD_HPE_20260602.html"
 },
 "decision_history": [
  {
   "date": "2026-05-18",
   "verdict": null,
   "role": null,
   "price_at_decision": 33.1,
   "fundamental_grade": "B",
   "to_date_pct": 38.78,
   "days": 105,
   "source_report": "docs/dd/DD_HPE_20260518.html"
  },
  {
   "date": "2026-06-02",
   "verdict": null,
   "role": null,
   "price_at_decision": 47.0,
   "fundamental_grade": "B",
   "to_date_pct": 6.0,
   "days": 90,
   "source_report": "docs/dd/DD_HPE_20260602.html"
  }
 ],
 "prior_watch_return_pct": null,
 "qc50_trigger_1": false,
 "falsifiers": [],
 "usernote": "[hub]  /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/entities/HPE.md\n[dd] 2026-06-02  DD|HPE Hewlett Packard Enterprise — v12.4(2026-06-02)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_HPE_20260602.md\n[dca] 2026-06-02  DCA|HPE Hewlett Packard Enterprise — Deep Conviction(2026-06-02)\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_HPE_20260602.md\n[dd] 2026-05-18  HPE 深度研究報告 v12.3|2026-05-18\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dd/DD_HPE_20260518.md\n[dca] 2026-05-18  HPE 深度定見分析 DCA|2026-05-18|Hewlett Packard Enterprise\n        /Users/ivanchang/financial-analysis-bot/knowledge/vault/auto/dca/DCA_HPE_20260518.md"
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

[找不到逐字稿：/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md（已試 ~/Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股/HPE/）]

---

## ⑤ Digest

```json
{
  "source_files": [
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md",
    "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"
  ],
  "items": [
    {"topic": "guidance", "claim": "Q3 revenue up 18% YoY to $9.1B, record", "quote": "Revenue was $9.1 billion, up 18% year-over-year", "speaker": "Antonio Neri", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "guidance", "claim": "FY25 non-GAAP EPS range raised to $1.88-$1.92", "quote": "We are raising our non-GAAP EPS range to $1.88 to $1.92", "speaker": "Marie Myers", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "guidance", "claim": "Q4 FY25 revenue guided to $9.7B-$10.1B", "quote": "we expect revenue to be between $9.7 billion and $10.1", "speaker": "Marie Myers", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "margin", "claim": "Server operating margin of 6.4% in Q3, consistent with outlook", "quote": "Server operating margin of 6.4% was consistent with our", "speaker": "Antonio Neri", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "margin", "claim": "Networking operating margin was 20.8% in Q3, down 160bps YoY", "quote": "Networking operating margin was 20.8%, down 160 basis", "speaker": "Marie Myers", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "competition", "claim": "HPE and Juniper both named leaders in Gartner Magic Quadrant for wired/wireless LAN", "quote": "HPE and Juniper Networks were both recognized again as", "speaker": "Antonio Neri", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "capital_allocation", "claim": "Returned $171M to shareholders via dividends in Q3", "quote": "We returned $171 million to shareholders through dividends", "speaker": "Marie Myers", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "capital_allocation", "claim": "Pro forma combined net leverage ratio at 3.1x post-Juniper close", "quote": "our pro forma combined net leverage ratio was 3.1x", "speaker": "Marie Myers", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "product", "claim": "Launched servers with new NVIDIA RTX PRO 6000 Blackwell/Blackwell Ultra", "quote": "we launched HPE servers with the new NVIDIA RTX PRO", "speaker": "Antonio Neri", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "risk", "claim": "No material demand pull-in observed in Q3 despite tariff backdrop", "quote": "we did not see material demand pull-in.", "speaker": "Marie Myers", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "risk", "claim": "Buybacks paused in Q3 due to possession of material nonpublic information (Juniper-related)", "quote": "we were in possession of material nonpublic information", "speaker": "Marie Myers", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "customer", "claim": "Added ~2,000 new GreenLake customers in Q3, total ~44,000", "quote": "we added approximately 2,000 new customers bringing our", "speaker": "Antonio Neri", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "commitment", "claim": "Reiterated at least $600M Juniper cost synergies over 3 years", "quote": "we are reiterating at least $600 million in cost synergies", "speaker": "Antonio Neri", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "commitment", "claim": "Remains committed to investment-grade credit rating, deleveraging to ~2x by FY27", "quote": "We remain committed to our investment-grade credit rating", "speaker": "Marie Myers", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"topic": "guidance", "claim": "AI systems orders up nearly 100% sequentially in Q3, incl. Middle East sovereign wins", "quote": "AI systems orders increased nearly 100% quarter-over", "speaker": "Antonio Neri", "date": "2025-09-03", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},

    {"topic": "guidance", "claim": "FY26 non-GAAP EPS outlook raised to $2.25-$2.45", "quote": "We are raising our fiscal 2026 non-GAAP diluted net EPS", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "guidance", "claim": "FY26 free cash flow midpoint raised, now expect $1.7B-$2B range", "quote": "now expect a range of $1.7 billion to $2 billion", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "margin", "claim": "Q4 non-GAAP operating margin hit record high of 12.2%", "quote": "Non-GAAP operating margin was a record high at 12.2%", "speaker": "Antonio Neri", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "margin", "claim": "AI systems operating margin delivered ~10% in Q4, consistent with outlook", "quote": "We successfully delivered an operating margin of", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "margin", "claim": "Hybrid cloud operating margin came in at 5% in Q4, down YoY and QoQ", "quote": "Hybrid cloud operating margin for the quarter came in at", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "capital_allocation", "claim": "Returned $171M dividends plus $100M buybacks in Q4", "quote": "we returned $171 million through dividends to common", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "capital_allocation", "claim": "Improved pro forma net leverage from 3.1x to 2.7x via $2B term loan paydown", "quote": "improving our pro forma net leverage ratio from 3.1x to", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "capital_allocation", "claim": "Agreed to sell remaining 19% H3C stake for ~$1.4B, proceeds to deleverage", "quote": "we are selling the entirety of our remaining interest in", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "risk", "claim": "Monitoring DRAM/NAND markets daily amid commodity cost inflation", "quote": "We are monitoring the DRAM and NAND markets daily", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "risk", "claim": "DRAM/NAND costs expected to keep rising in 2026, mostly passed to market", "quote": "We expect DRAM and NAND costs to continue to increase in", "speaker": "Antonio Neri", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "margin", "claim": "Juniper posted an 8-year high operating profit margin in Q4 post-close", "quote": "enabling Juniper to deliver an 8-year high in operating", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "product", "claim": "Announced new Alletra Storage MP X10000 data intelligence nodes for AI pipelines", "quote": "The new HPE Alletra Storage MP X10000 data intelligence", "speaker": "Antonio Neri", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "customer", "claim": "Won contracts for 5 large sovereign supercomputer systems using liquid-cooled Cray tech, incl. DOE exascale system", "quote": "We have already won contracts to build 5 large sovereign", "speaker": "Antonio Neri", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "commitment", "claim": "Committed to at least $3 non-GAAP diluted EPS by FY28", "quote": "we are committed to generating at least $3 in non-GAAP", "speaker": "Antonio Neri", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "guidance", "claim": "Q4 revenue $9.7B, up 14% YoY, slightly below outlook low end due to AI shipment pushout", "quote": "Q4 revenue of $9.7 billion increased 14% year-over-year", "speaker": "Antonio Neri", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"topic": "guidance", "claim": "Management comfortable with mid-single-digit networking pro forma guide for FY26 despite Q4 pro forma outperformance", "quote": "we're comfortable with the guide that we've given you so", "speaker": "Marie Myers", "date": "2025-12-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},

    {"topic": "guidance", "claim": "Q1 FY26 revenue $9.3B, up 18% YoY", "quote": "Q1 revenue was $9.3 billion, up 18%.", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "guidance", "claim": "Q1 results support raising FY26 outlook", "quote": "give us the confidence to raise our fiscal '26 outlook", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "guidance", "claim": "Raised full-year networking revenue growth to 68%-73% reported basis", "quote": "We are raising our full year Networking revenue growth to", "speaker": "Marie Myers", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "margin", "claim": "Q1 networking operating margin 23.7%, slightly above guidance", "quote": "Networking operating margin was 23.7%, slightly above our", "speaker": "Marie Myers", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "margin", "claim": "Q1 total operating margin 12.7%, better than expected", "quote": "Operating margin was better than expected at 12.7%.", "speaker": "Marie Myers", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "margin", "claim": "Cloud & AI Q1 operating margin 10.2%, better than expected on pricing/cost actions", "quote": "resulted in a better-than-expected operating margin of", "speaker": "Marie Myers", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "risk", "claim": "IT market facing sharp acceleration in supply tightness, notably DRAM/NAND", "quote": "is facing a sharp acceleration in supply tightness and", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "risk", "claim": "Elevated component prices expected to persist well into 2027", "quote": "We expect elevated prices to persist well into 2027.", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "risk", "claim": "DRAM and NAND now make up over half of traditional server bill of materials cost", "quote": "DRAM and NAND now make up over half of the bill of", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "capital_allocation", "claim": "Improved pro forma net leverage from 3.1x post-close to 2.6x in Q1", "quote": "We improved our pro forma net leverage ratio from 3.1x", "speaker": "Marie Myers", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "capital_allocation", "claim": "Returned $190M in dividends plus $158M in buybacks in Q1", "quote": "we returned $190 million through dividend to common", "speaker": "Marie Myers", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "product", "claim": "New MX301 router series off to strong start with demand across verticals", "quote": "Our recently introduced MX301 router series is off to a", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "customer", "claim": "Siemens Energy selected HPE for gas-turbine engineering AI inferencing infrastructure", "quote": "Siemens Energy, one of the world's leading global energy", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "commitment", "claim": "Reaffirmed long-term FY28 targets of $3+ EPS, $3.5B+ FCF despite commodity headwinds", "quote": "we remain committed to our long-term fiscal 2028 targets", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "competition", "claim": "HPE now owns entire networking technology stack post-Juniper", "quote": "HPE now owns the entire networking technology stack", "speaker": "Antonio Neri", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "guidance", "claim": "Lowered FY26 Cloud & AI revenue growth to mid-to-high single digit to prioritize higher-margin orders amid supply constraints", "quote": "We are lowering our full year Cloud & AI revenue growth to", "speaker": "Marie Myers", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"topic": "risk", "claim": "Management declined to quantify how much of Q1 order strength was pull-forward demand", "quote": "we haven't quantified the pull-forwards", "speaker": "Marie Myers", "date": "2026-03-09", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},

    {"topic": "guidance", "claim": "Record Q3 revenue exceeding $9B including 1 month of Juniper", "quote": "we had record revenue in excess of $9 billion", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "competition", "claim": "No other company has HPE's combined asset collection (server/storage/networking/cloud)", "quote": "there is nobody that has this collection of assets", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "competition", "claim": "Reiterated no one else has this portfolio of assets", "quote": "there's really nobody else out there who has this portfolio", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "capital_allocation", "claim": "Intensely focused on free cash flow given post-close leverage above 3x", "quote": "we're intensely focused on one key variable, which is", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "capital_allocation", "claim": "Target to get leverage down to 2x by end of FY27", "quote": "get down to a leverage of 2x sort of by the end of '27", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "capital_allocation", "claim": "Continues to buy back shares to manage dilution despite pause last quarter", "quote": "we continue to buy back shares.", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "risk", "claim": "Tariff environment described as somewhat stable, no change to $0.04 impact estimate", "quote": "the tariff environment for us has been somewhat stable", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "risk", "claim": "Guided to ~$0.04 tariff impact for the year, split H1/H2", "quote": "We have guided to about $0.04 in the year in terms of", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "risk", "claim": "Geopolitical situation around sovereign AI deals continues to evolve", "quote": "the geopolitical situation continues to evolve as well", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "commitment", "claim": "Raised Juniper cost synergy target from at least $450M to $600M", "quote": "we raised our outlook from at least $450 million to", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "customer", "claim": "Sovereign transactions disclosed as being in the Middle East, subject to government processes", "quote": "We do have sovereign transactions, some of which I think", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "product", "claim": "Storage business in midst of transition to Alletra MP platform and ratable revenue model", "quote": "we are in the midst of a transition in storage, both in", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "margin", "claim": "More than 50% of operating profit will come from networking segment going forward", "quote": "more than 50% of the operating profit is actually going", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"topic": "guidance", "claim": "Next quarter AI revenue expected down slightly but mix shifting toward sovereign/enterprise", "quote": "we see AI revenue coming down slightly but we see the mix", "speaker": "Marie Myers", "date": "2025-09-04", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},

    {"topic": "commitment", "claim": "Committed to $600M annual Juniper synergies plus $350M Catalyst synergies by 2028", "quote": "we are committed to delivering annual run rate synergies", "speaker": "Antonio Neri", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "commitment", "claim": "Will generate more than $3.5B free cash flow by FY28", "quote": "we will generate more than $3.5 billion in free cash flow", "speaker": "Antonio Neri", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "guidance", "claim": "TAM across portfolio anticipated to grow to over $1.1 trillion by FY28", "quote": "We anticipate the overall total addressable market across", "speaker": "Antonio Neri", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "margin", "claim": "Networking margins expected to reach 25%-28% by FY28 driven by Juniper synergies", "quote": "we expect networking margins to reach 25% to 28% by FY '28", "speaker": "Marie Myers", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "margin", "claim": "Expect overall non-GAAP operating profit CAGR of 11%-17% pro forma over 3 years", "quote": "we expect the overall company non-GAAP operating profit", "speaker": "Marie Myers", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "capital_allocation", "claim": "Will target returning at least 75% of free cash flow to shareholders after deleveraging phase", "quote": "we will target returning at least 75% of our free cash", "speaker": "Marie Myers", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "capital_allocation", "claim": "Announced new $3B share repurchase authorization, total $3.7B", "quote": "we are announcing a new $3 billion share repurchase", "speaker": "Marie Myers", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "capital_allocation", "claim": "Raising annual dividend 10% to $0.57/share starting FY26", "quote": "we are increasing our annual dividend by 10% to $0.57", "speaker": "Marie Myers", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "guidance", "claim": "ARR growth expected to moderate given large existing base; disclosure to become annual", "quote": "AAR growth will moderate due to a combination of factors.", "speaker": "Marie Myers", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "product", "claim": "Introduced next-generation HPE NonStop servers, doubling memory/bandwidth", "quote": "We recently introduced our next generation of HP NonStop", "speaker": "Antonio Neri", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "product", "claim": "Direct liquid cooling systems already deployed in more than 20 countries", "quote": "we already have direct liquid cooling system deployed in", "speaker": "Antonio Neri", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "customer", "claim": "6 of top 10 global retail banks use HPE NonStop for payment processing", "quote": "6 of the top 10 full-service global retail banks use", "speaker": "Antonio Neri", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "customer", "claim": "Inaugurated Isambard-AI, fastest AI system in the UK, with University of Bristol/UK government", "quote": "we inaugurated the fastest AI system in the U.K.", "speaker": "Antonio Neri", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "competition", "claim": "Both HPE and Juniper named leaders in 2025 Gartner Magic Quadrant while long-standing incumbent was not", "quote": "both HPE and Juniper Networks were named leaders while the", "speaker": "Rami Rahim", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "risk", "claim": "Did not bake revenue synergies into FY26 guide, citing integration execution risk", "quote": "We did not bake revenue synergies into 2026 for a specific", "speaker": "Rami Rahim", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"topic": "guidance", "claim": "FY26 revenue growth anticipated at 5%-10% pro forma", "quote": "We anticipate revenue growth of 5% to 10% on a pro forma", "speaker": "Marie Myers", "date": "2025-10-15", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},

    {"topic": "guidance", "claim": "FY26 networking guide anchored around $11B after $300M revenue reclass to Corporate/Other", "quote": "we really anchored the guide around $11 billion", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "guidance", "claim": "Networking growth framed as 65%-70% YoY reported basis", "quote": "that 65% to 70% growth on a year-on-year or", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "margin", "claim": "Core server business back in 10% margin range in Q4/Q1 guide", "quote": "We're back in the core server business back in the 10%", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "margin", "claim": "AI/software businesses carry a much richer gross margin profile supporting overall mix", "quote": "these AI businesses obviously have a much richer gross", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "competition", "claim": "HPE is #2 in Campus and Branch networking space", "quote": "we're #2 in that space", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "competition", "claim": "Juniper brings a beachhead capability in routing that is promising going forward", "quote": "Juniper brings sort of a beachhead capability here", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "capital_allocation", "claim": "Reaffirmed leverage target of 2x by FY27 as the North Star for capital allocation", "quote": "We want to get down to 2x by '27.", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "capital_allocation", "claim": "3-year vision includes returning 80% of free cash flow back to shareholders", "quote": "returning 80% back to our shareholders", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "risk", "claim": "Entering a very volatile period for DRAM/NAND commodity costs", "quote": "we're certainly entering a very volatile period of time", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "risk", "claim": "No doubt server costs will rise from commodity environment in FY26", "quote": "There's no doubt that you're going to face some rising", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "product", "claim": "Announced Helios AI rack-scale architecture combining networking and server scale-up", "quote": "we announced Helios, which is sort of scale up both in", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "product", "claim": "Announced QFX with Tomahawk 6 and liquid cooling, first to market", "quote": "We just announced last week in Barcelona, had some", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "customer", "claim": "GreenLake surpassed 40,000-plus customers", "quote": "we announced 40,000-plus customers in this space.", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "commitment", "claim": "Reaffirmed ARR target of $3.5B by year end", "quote": "we said we get to $3.5 billion", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"},
    {"topic": "guidance", "claim": "Expects bulk of restructuring/synergy work done by end of FY27, benefiting margins into FY27", "quote": "We expect a lot of the hard work on restructuring will be", "speaker": "Marie Myers", "date": "2025-12-10", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"}
  ],
  "qa_flags": [
    {"question": "Samik Chatterjee (JPMorgan): when will networking margins get back to mid-20s given synergy math implies more upside?", "response_pattern": "Marie deferred specifics to the upcoming Security Analyst Meeting rather than answering directly on the call", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q3_2025_Earnings_Call_20250903.md"},
    {"question": "Aaron Rakers (Wells Fargo): why is FY26 networking pro forma growth guided to mid-single-digit when Q4 pro forma growth was low-to-mid teens?", "response_pattern": "Marie repeated qualitative comfort language (\"we're comfortable with the guide\") without quantifying the deceleration drivers", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"question": "Wamsi Mohan (BofA): does the Q4-to-Q1 AI deal pushout mean Q1 seasonality should be much better than normal, and would seasonality have been worse without the pushout?", "response_pattern": "Marie and Antonio answered with multiple qualitative factors (seasonality anchor, back-half AI weighting) but did not isolate or quantify the counterfactual pushout impact", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q4_2025_Earnings_Call_20251204.md"},
    {"question": "George Notter (Wolfe Research): what is the full-year revenue assumption for pull-forward demand and incremental pricing benefit from memory?", "response_pattern": "Marie explicitly declined to quantify pull-forwards, redirecting to the aggregate revenue range instead", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"question": "Erik Woodring (Morgan Stanley): is the 5% sequential Q2 revenue growth guide actually pull-forward demand rather than durable demand?", "response_pattern": "Antonio acknowledged \"there is, of course, demand pull-in from some customers\" but pivoted immediately to broader AI-deployment demand narrative without separating the two magnitudes", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Q1_2026_Earnings_Call_20260309.md"},
    {"question": "Chris Derison (Citi): what do public market investors miss or appreciate most about the HPE story?", "response_pattern": "Marie's answer stayed at a promotional/talking-points level (recapping segment highlights) rather than naming a specific misunderstood variable", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Citi_s_2025_Global_Technology_20250904.md"},
    {"question": "Amit Daryanani (Evercore): why guide networking to low-to-mid-single-digit growth for FY26 when Juniper's order momentum coming out of the year was very strong?", "response_pattern": "Rami stated synergies/momentum were deliberately excluded from the FY26 numbers (\"we were a bit cautious about expecting too much\"), a conservative framing rather than a data-driven answer", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"question": "Louis Miscioscia (Daiwa): given the strength of AI/private cloud/server-modernization assets, what specifically is holding back faster growth and when does it inflect?", "response_pattern": "Antonio gave a broad segmentation narrative (model builders vs. enterprise vs. sovereign) without committing to a specific inflection quarter or half", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Shareholder_Analyst_Call_Hewlett_Packard_Enterprise_Company_20251015.md"},
    {"question": "Tim Long (Barclays): is data-center-switching revenue synergy on a separate timeline from the sales-force integration, or can it happen organically now?", "response_pattern": "Marie reiterated the already-disclosed cost-synergy figure ($600M) and qualitative optimism about bidding jointly on deals, without giving any quantified revenue-synergy figure or timeline", "file": "/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/HPE/HPE_Barclays_23rd_Annual_Global_Technology_Conference_20251210.md"}
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

