你是 DD 管線 v20 的判斷層閘（gate），標的 DDOG（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

## 任務

依 bundle 內 `gate_card.md` 的 ①–⑧ checklist 逐條複核 `judgment.json`，只揪判斷級的錯，不判斷寫得好不好。判斷級 🔴 限三形狀：①證據包已有而判斷未接；②算術或機率防線失守；③裁決與自身輸入矛盾。資料級問題（facts.json 本身缺料、來源不夠新、某軸查不到）不算 🔴，最多 🟡；無實質問題給 🟢。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：`gate_card.md`（①–⑧ checklist 全文與 🔴／🟡／🟢 口徑）、被引用事實與負向條目子集（核對 `fact_refs` 用）、`scenario_meta.json`（情境樹權威值，對帳 `decision_inputs.irr_base_pct`／`ev5y_pct` 用）、`judgment.json` 全文（被審對象，原樣）。

## 禁

- 禁 WebSearch／WebFetch、禁開 bundle 以外任何檔（包含 `docs/dd/`、`.dd_build/` 下的其他產物）。
- 禁跑任何腳本（`validate_judgment.py`／`dd_decision.py`／`dd_scenario.py` 已在判斷端跑過，機械層不歸你）。
- 禁提整段改寫判斷、禁自己動手修補 `judgment.json`——你只出稽核，修補是另一支流程的事。
- 證據包裡沒有的東西不得臆測補白，只講證據包內找得到依據的話。


===== BUNDLE =====

## ① gate_card.md（判斷層閘卡）

<!-- source: scripts/dd_prompts/gate_contract.md sha256:90928128665c694a; .claude/skills/stock-analyst/references/critic-gates.md sha256:8dff4ac45280acfd git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->
<!-- 2026-10-20 ⑤ 改程式判定；來源 gate_contract §⑤／critic-gates ⑤ 同日改成同一條規則（核心軸 none 🔴、非核心 🟡）；重新濃縮時以本卡 ⑤ 為準 -->

你是 DD 管線 v20 的判斷層閘（gate），sonnet，單輪、無工具。你未參與寫判斷，這是一次跨模型冷讀。
輸入：`judgment.json`（待審判斷物）＋ `facts.json`（事實表，每軸 finding 帶 source／as_of／direction）。
任務只有一件：依下列 checklist 逐條複核 `judgment.json`，只揪**判斷級**的錯，不判斷寫得好不好。
判斷級 🔴 限三形狀：①證據包已有而判斷未接；②算術或機率防線失守；③裁決與自身輸入矛盾。資料級（facts.json 本身缺料、來源不夠新、某軸查不到）不算 🔴，最多 🟡。
禁 WebSearch／WebFetch、禁讀輸入以外任何檔、禁改 `judgment.json`，只出稽核清單。

## checklist（①–⑧ 全出，不得跳號、不得「同上」帶過）

① 競爭惡化——份額流失／新進入者／客戶 second-source／大客戶轉單。查 facts.json 對應軸（competitive_share_entrants／customer_second_source／customer_concentration_credit）裡負向、或應被引用的 finding，核對 judgment.json 的 `moat.threats`／`moat.competitors`／`contradictions[]`／`decision_inputs.bear` 是否接住；被引用=N 卻是負向的 finding 即漏接。[gate_contract §①]

② 供需 durability——緊缺或過剩是結構還是週期，供給可逆性是否寫進 bear 機率。facts.json 的 supply_demand_durability 軸負向 finding，若未被引用且未列 `evidence_dismissed`，須在 `premortem`／`decision_inputs.bear` 找到對應處理，找不到即 🔴。[gate_contract §②]

③ 其他結構變數（開放軸）——法規／政策／關稅／反壟斷／補貼、通路重構、商業模式轉移、替代技術、客戶結構轉移。找 facts.json 覆蓋總覽裡「有 finding 卻沒人接住」的軸，對照 `contradictions[]`／`premortem.blind_spots`／`triggers[]`；閘禁搜尋，不重新查有沒有漏掉的產業變化。[gate_contract §③]

④ priced-in——共識與賣方目標價 vs 現價，裁決是否只是把市場已知的事再說一次。看 `decision_inputs.market_wrong_reason_given` 是否有具體內容（非空泛套話），對照 facts.json 的 `latest_quarter_kpis[].vs_consensus` 與 `valuation_current`。判斷寫「不追／等價格」而裁決是進場、`decision_inputs.wait_for_price` 卻沒填 true ＝ 矛盾；填了 true 時裁決落觀望是規則結果，不算矛盾，只看 `wait_for_price_condition` 是否具體可驗。[gate_contract §④]

⑤ 覆蓋面掃描——**燈號由程式判定**（核心軸 none→🔴；只有非核心軸 none→🟡；全 found／not_applicable→🟢），bundle 附程式結果，你回的 ⑤ 燈號會被覆寫。你只評論：facts.json 點名 status="none"／"not_applicable" 的軸，查詢是否切題（不以查詢次數計）、判斷有沒有交代缺口對結論的影響；不得因缺軸自行升 🔴。

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤（燈號由程式判定，你只評論）。
(b) 量化模組完整性抽查：ROIC×再投資率真算與否、內生天花板對帳共識 CAGR、情境樹 Bull/Base/Bear EPS 價差是否實質、IRR 內部對帳，做法同 checklist ⑥。
(c) 數字可回溯：判斷引用的歷史數字逐一核對 facts.json 原文的期間與單位；反證條目要查採納理由與後果是否成立，不能只因編號存在就算過。[gate.md.tmpl 2026-09-11 註腳]

## 🔴／🟡／🟢 口徑

判斷級 🔴 限下列三種形狀：

1. **證據包已有而判斷未接**——證據包內存在的 finding／數字，判斷物完全沒接進 `contradictions`／`moat.threats`／`premortem`／`triggers`／`thesis.R`，也沒寫進 `evidence_dismissed[]`；
2. **算術或機率防線失守**——推導不可複算、內部恆等式不對帳、情境樹退化、機率與其自身依據矛盾；
3. **裁決與自身輸入矛盾**——`decision_inputs`／`scenario_meta`／`decision_out` 三者互斥，或裁決與判斷物自己寫下的理由相反。

**資料級不算 🔴**（證據包本身缺料、來源不夠新、某軸查不到）——那是 Stage 0 的問題，最多給 🟡 並在附註點名。無實質問題給 🟢；有實質但不改裁決方向的給 🟡。

## 輸出格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```


---

## ②b 被引用的事實與負向條目（v19；閘要查數字時不必猜）

### 判斷檔 `fact_refs` 引到的事實（30 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝1121.454 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；YoY +35.6%（去年同期 826.760）、QoQ +11.4%（+115.0M，公司稱為史上最大單季增量）（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：Zacks 共識約 1.08B，超出約 3.8%（來源：Yahoo Finance／Zacks 轉載）；也高於公司自家 Q2 指引上緣 1.08B（指引 1.07–1.08B）
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation（占營收／占 non-GAAP 營業利益）＝220.251 USD M（占營收 19.6%；占 non-GAAP 營業利益 85.7%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；分項：營收成本 9.256M、R&D 131.682M、S&M 47.098M、G&A 32.215M。GAAP 營業利益僅 5.5M，故不以 GAAP 為分母（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_kpi9_customers_with_arr_100k`（q1_business）｜Customers with ARR ≥ $100k＝4720 家（占 ARR 約 91%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release；占 ARR 比率出自 Q2 財報電話會（numbers.latest_quarter_kpis.items[9]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_kpi12_net_revenue_retention_tr`（q1_business）｜Net revenue retention（trailing 12 個月）／gross revenue retention＝NRR 低 120%（low 120s）；GRR 中後段 90%（mid- to high 90s） %（公司只給區間，未給精確值）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CFO 準備稿（2026-08-06）（numbers.latest_quarter_kpis.items[12]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_kpi15_ai_yoy`（q1_business）｜非 AI 客戶營收 YoY 成長＝高 20%（high 20s） %（公司只給區間）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CEO／CFO 準備稿（2026-08-06）（numbers.latest_quarter_kpis.items[15]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-04 date｜期間與口徑：2026-11-04／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-04）
- `f_peer_ddog_gross_margin_pct`（q2_moat）｜DDOG 毛利率＝79.58 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DDOG.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ddog_operating_margin_pct`（q2_moat）｜DDOG 營業利益率＝2.3 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DDOG.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ddog_fcf_margin_pct`（q2_moat）｜DDOG FCF 利潤率＝25.93 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DDOG.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dt_operating_margin_pct`（q2_moat）｜DT 營業利益率＝13.55 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dt_fcf_margin_pct`（q2_moat）｜DT FCF 利潤率＝26.53 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.55 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.98 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.76 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝4521.48 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（46 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝5530.37 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（46 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝278.704 USD M（FCF 利益率 24.9%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；營業現金流 315.872M，扣 capex 與資本化軟體後（Q2 單季由上半年累計減 Q1 推得約 9.9M + 27.3M）（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未查得共識
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-3926.36 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 1307.23、現金 5233.59（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝361.04 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝179.04 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝70.21 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 2.55，分子＝快照價 179.04｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝13.43 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝248.67 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝25.3 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝28.28｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-10.55 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 179.04 / W52 188.17 / W104 160.4 / W250 128.27 / W250 13週斜率 1.09%」
- `f_kpi13_rpo_current_rpo`（q1_business）｜RPO／current RPO＝3470 USD M（YoY +43%；cRPO YoY 約 +40%，RPO 期間拉長）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CFO 準備稿（2026-08-06）；公司稱營收比 billings／RPO 更能反映業務趨勢（numbers.latest_quarter_kpis.items[13]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未查得 RPO 共識
- `f_kpi14_billings`（q1_business）｜Billings＝1180 USD M（YoY +38%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CFO 準備稿（2026-08-06）（numbers.latest_quarter_kpis.items[14]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未查得共識

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：FinancialContent 評論文章稱：Palo Alto Networks 收購 Chronosphere、Snowflake 收購 Observe，是把資料儲存、資安與監控合併成單一平台的趨勢，文章形容為對 Datadog 的「Pincer」夾擊威脅；並稱 Dynatrace 是企業市場「chief rival」（Davis AI 歷來被視為較成熟，但 Bits AI 推出後差距縮小），Cisco 正把 Splunk 的日誌優勢與網通硬體整合、主攻傳統企業。此為第三方評論文章的描述，非份額數據。
  - 來源：FinancialContent：Datadog (DDOG) and the 2026 Observability Frontier: Navigating the AI Re-Architecting Phase — https://www.financialcontent.com/article/finterra-2026-1-27-datadog-ddog-and-the-2026-observability-frontier-navigating-the-ai-re-architecting-phase（as_of 2026-01-27）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Datadog's largest customer renewed a nine-figure agreement but reduced its usage; per the search summary of the TheStreet article, this affected the company's Q3 and full-year 2026 forecasts. Article body not retrieved (WebFetch returned 403), so the exact contract figures and whether the usage cut involved in-house or a second vendor are not confirmed.
  - 來源：TheStreet, 'Datadog's largest customer renews deal but cuts usage' https://www.thestreet.com/investing/stocks/datadogs-largest-customer-renews-deal-but-cuts-usage（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear、valuation、triggers
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：SaaStr states 'OpenAI is Datadog's biggest single customer' (analyst assessment, not a company-named disclosure), and that the AI-native cohort including it grew only 'high single digits' in Q1 2026.
  - 來源：SaaStr, 'Datadog Stock Is Up +66%. Here Are 5 Reasons Why...' https://www.saastr.com/datadogup/（as_of 2026-05-25）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#4`（customer_second_source｜方向 -｜狀態 ok）：Per the same secondary source, one large AI-native customer's decision in early 2024 to scale down and partially re-platform its observability stack onto internal tooling drove the public growth deceleration that began with the Q1 2024 print.
  - 來源：Mungomash, 'Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail' https://mungomash.com/orgs/datadog/financials/（as_of 2024-05-07）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：Q2 2026 法說會：管理層不點名最大客戶，只說是「一家領先的 AI 公司」，使用 17 項 Datadog 產品，剛完成一筆「九位數美元」的續約。續約後用量有下降（usage reduction），已納入 Q3 與 FY2026 財測；CEO Pomel 稱今年剩餘時間的財測已「fully derisked」。
  - 來源：The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/（as_of 2026-08-13）｜affects：thesis.R、decision_inputs.bear、valuation、triggers
- `customer_concentration_credit#5`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K（2026-02-18 提交）有「AI-native cohort」一詞，並註明該客群「包含我們最大的客戶」；該客群對 2025 年 12 月底當季營收年增的貢獻約 7 個百分點。（二手來源轉述，未讀到 10-K 原文；未查到 10-K 是否列出單一客戶占營收 ≥10% 的具體百分比。）
  - 來源：mungomash.com「Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail」（搜尋摘要轉述 FY2025 10-K；頁面 WebFetch 回 404，未能直接驗證）（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Gartner's observability report says more than 40 vendors compete in the space (20 evaluated in the Magic Quadrant), that 'questions about total cost of ownership are now standard', and that leading platforms must offer granular data retention controls, tiered storage and usage-based pricing.
  - 來源：Network World, 'In crowded observability market, Gartner calls out AI capabilities, cost optimization, DevOps integration' https://www.networkworld.com/article/4032218/in-crowded-observability-market-gartner-calls-out-ai-capabilities-cost-optimization-devops-integration.html（as_of 2025-08-06）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `supply_demand_durability#7`（supply_demand_durability｜方向 -｜狀態 ok）：Grafana Labs reached $400M+ ARR with 7,000 customers as of September 2025 (competitor scale figure cited in a vendor comparison blog; blog publish date not shown, as_of day set to the first of the stated month).
  - 來源：OpenObserve blog, '10 Best Datadog Competitors & Alternatives in 2026' https://openobserve.ai/blog/datadog-competitors/（as_of 2025-09-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：最大客戶出現用量下滑（同時簽了九位數美元續約）；管理層稱已把此影響完整反映在 Q3 與全年 2026 指引，並稱排除該客戶後整體趨勢與加速一致。
  - 來源：Motley Fool, Datadog Q2 2026 Earnings Call Transcript（WebFetch 摘要）https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/ ；GuruFocus Q2 2026 highlights（as_of 2026-08-06）｜affects：decision_inputs.bear、thesis.R、triggers
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：指引：Q3 營收 $1.135B–$1.145B（年增 28%–29%，低於 Q2 的 36%）；全年 2026 營收 $4.45B–$4.47B（年增約 30%）。
  - 來源：GuruFocus, Datadog Q2 2026 Earnings Call Highlights https://www.gurufocus.com/news/9014386/datadog-inc-ddog-q2-2026-earnings-call-highlights-revenue-surges-36-to-112b-aidriven-growth-accelerates（as_of 2026-08-06）｜affects：valuation、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：groundcover（Datadog 競品廠商）2026-07-29 的指南結論稱：2026 年可觀測性品類的轉變是架構面的——以 eBPF 取代語言 agent、以 BYOC（資料留在客戶自己的 VPC）取代純 SaaS、以「依基礎設施計價」取代「依用量計價」。此為競品自家行銷文章的說法，非中立第三方量測。
  - 來源：groundcover, 'Datadog Alternatives for Full-Stack Observability in 2026', https://www.groundcover.com/guides/datadog-alternatives-for-full-stack-observability（as_of 2026-07-29）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：IT Connection（Currentanalysis）2026 年觀測性預測稱：應用開發工具類新創將透過在自家產品組合內增加可觀測性功能，對整個可觀測性市場產生破壞性影響（標題：Makers of Dev Tools to Disrupt Space）。搜尋摘要只取得此論點，未取得內文細節與具體廠商名單。
  - 來源：IT Connection / Currentanalysis, 'Observability Predictions 2026: Makers of Dev Tools to Disrupt Space', https://itcblogs.currentanalysis.com/2026/01/29/observability-predictions-2026-makers-of-dev-tools-to-disrupt-space/（as_of 2026-01-29）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 13 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":436.3,"bear_5y_price":82.6,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":43.4,"ev5y_pct":39.3,"irr_base_pct":7.5,"asym_ratio":2.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":2.74,"pe":65.34,"basis":"FY2026 全年 non-GAAP EPS 指引中位（2026-11-04 法說會 CFO，2.73–2.75），與終端倍數同為當年度 non-GAAP EPS 口徑；事實表共識 2.55 低於指引下緣，視為舊快照不採用。"},"eps":{"bull":[3.7,4.83,6.17,7.6,9.09],"base":[3.4,4.11,4.87,5.7,6.42],"bear":[2.7,2.6,2.7,2.82,2.95]},"pe":{"bull":48,"base":40,"bear":28},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":16,"base_cagr_pct":13},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DDOG_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：Q3 營收財測 11.35–11.45 億美元，年增 28–29%（原話："to be in the range of $1.135 billion to $1.145 billion"）
- 2026-08-06｜CFO｜guidance：全年營收財測 44.5–44.7 億美元，年增約 30%（原話："to be in the range of $4.45 billion to $4.47 billion"）
- 2026-08-06｜CFO｜margin：全年 non-GAAP 營業利益財測 10.1–10.3 億美元，營業利益率約 23%（原話："which implies an operating margin of 23%"）
- 2026-08-06｜CFO｜guidance：最大客戶用量下降，已納入 Q3 與全年財測（原話："we have seen a usage reduction,"）
- 2026-08-06｜CEO｜customer：CEO 披露與領先 AI 公司簽 9 位數續約，但 Q3 起用量下降（原話："albeit with a user reduction starting in Q3"）
- 2026-08-06｜CEO｜guidance：管理層說明對最大客戶採完全去風險的財測處理方式（原話："fully derisk the guidance for the rest of the year"）
- 2026-08-06｜CEO｜guidance：CEO 說明這次對最大客戶的權重與平常不同，其餘保守度不變（原話："we also weighted this one"）
- 2026-08-06｜CFO｜guidance：CFO 稱財測方法論不變，以近幾個月趨勢為基礎並隱含保守（原話："we base our guidance on trends observed in recent months"）
- 2026-08-06｜CEO｜customer：CEO 稱剔除最大客戶後成長率與其餘業務相同，其餘業務已連續 5 季加速（原話："5 quarters of continuous acceleration"）
- 2026-08-06｜CEO｜customer：非 AI 客戶營收成長加速至高 20% 區間，前季為 20% 中段，去年同期 18%（原話："to the high 20s percent year-over-"）
- 2026-08-06｜CFO｜customer：Q2 營收 11.2 億美元年增 36%，單季新增營收 1.15 億美元為紀錄（原話："added of $115 million is a record by a significant margin"）
- 2026-08-06｜CFO｜margin：毛利率 79.6%，前季 80.2%、去年同期 80.9%，管理層稱預期不變（原話："There's no change in our expectations for"）
- 2026-08-06｜CFO｜margin：Q2 營業費用年增 26%，DASH 大會成本約 1,500 萬美元（原話："the event cost about $15 million"）
- 2026-08-06｜CFO｜margin：Q2 自由現金流 2.79 億美元，利潤率 25%（原話："$279 million for a free cash flow margin of 25%"）
- 2026-08-06｜CFO｜capital_allocation：全年資本支出加資本化軟體占營收 4–5%；現金部位 50 億美元（原話："in the 4% to 5% of revenue range in fiscal 2026"）
- 2026-08-06｜CEO｜capital_allocation：宣布收購 Adaptive ML 以加速 AI 研究，預計 6 月完成（原話："acquisitions of Adaptive ML, which will close"）
- 2026-08-06｜CFO｜customer：淨營收留存率低 120%，總營收留存中高 90%（原話："net revenue retention percentage was in the low 120s"）
- 2026-08-06｜CFO｜customer：新客戶貢獻的年增營收占比由 Q1 25% 升至 Q2 約 30%（原話："was about 30% in Q2, up from 25% in Q1"）
- 2026-08-06｜CFO｜customer：AI 客戶群 750 家，含 31 家年支出逾 100 萬美元、其中 8 家逾 1,000 萬美元，並納入超大規模雲端業者內部 AI 實驗室（原話："hyperscalers using Datadog for in-house AI labs"）
- 2026-08-06｜CFO｜customer：CFO 稱 RPO 與帳單不如營收能反映業務趨勢；RPO 34.7 億美元年增 43%（原話："revenue is a better indication of our business trends"）
- 2026-08-06｜CFO｜customer：客戶總數約 33,400，新增客戶數被分析師指為歷來最弱；CFO 稱毛新增穩定，差異來自免費與合約邊界的低端（原話："customer additions continue to be strong and on trend line"）
- 2026-08-06｜CEO｜product：RUM 年化營收超過 2 億美元，成長加速至逾 50%（原話："now exceeds $200 million in ARR"）
- 2026-08-06｜CEO｜product：多產品採用率上升：使用 4 款以上產品的客戶 58%，去年同期 52%（原話："58% of our customers now use 4 or more products"）
- 2026-08-06｜CEO｜product：Bits AI 擴大接觸面，並改採 AI credits 新計價包裝模式（原話："we have a new model with AI credits that we're rolling"）
- 2026-08-06｜CEO｜product：Infinite Cardinality Metrics 以不同的指標包裝方式解決基數導致帳單不可預測的問題，仍屬早期（原話："by packaging our metrics a little bit differently"）
- 2026-08-06｜CEO｜product：MCP 工具呼叫次數季增四倍，較 2025 Q4 成長逾 22 倍（原話："MCP tool calls quadrupling again quarter-over-quarter"）
- 2026-08-06｜CEO｜product：將 Bits Security Analyst 從自家 SIEM 分離，可搭配其他 SIEM，朝 AI SOC 方向（原話："separated the agent from our SIEM"）
- 2026-08-06｜CEO｜competition：資安產品需整合重做，CEO 稱整合式平台符合其做法（原話："So it's a complete rebuild for most of the industry."）
- 2026-08-06｜CEO｜competition：Fortune 100 健保客戶案，管理層稱 HIPAA 合規與 PII 處理使其勝出競爭方案（原話："differentiate and win over competitive solutions."）
- 2026-08-06｜CEO｜customer：逾 3,000 萬美元 TCV 的多年約，取代 4 套商業與內部工具，含迄今最大 BYOC 案（原話："displacing 4 commercial and internal tools"）
- 2026-08-06｜CEO｜risk：客戶關注點由驗證正確性轉向 AI 成本控制；分析師提出 CFO 對 Datadog 帳單的抱怨（原話："the focus has moved quite a bit towards cost."）
- 2026-08-06｜CEO｜risk：分析師問 Bits AI 自動化是否減少消耗量；CEO 稱不是零和（原話："it's not a zero-sum game."）
- 2026-08-06｜CEO｜commitment：管理層稱持續投資研發與業務團隊，因尚未達理想的涵蓋規模（原話："still not at the scale we want to be"）
- 2026-08-06｜CFO｜commitment：管理層稱非 AI 成長可持續，並將部分成長歸因於擴編業務配額（原話："We've successfully expanded quota capacity, the"）

### DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md
- 2026-02-12｜David Obstler (CFO)｜guidance：毛利率規劃維持在正負 80% 左右，並保留彈性投資平台、資料中心與產品（原話："planning our gross margins plus or minus 80%"）
- 2026-02-12｜David Obstler (CFO)｜commitment：重申長期營業利益率目標 25% 以上，並稱與上一次投資人日所說相同（原話："long-term target of an operating margin at 25% plus"）
- 2026-02-12｜David Obstler (CFO)｜margin：R&D 占營收比重的目標約 30%，並稱有波動（原話："this has been our target around 30%"）
- 2026-02-12｜David Obstler (CFO)｜margin：稱 AI 的使用可能成為 R&D 占比的槓桿之一，未量化（原話："some things about the use of AI that might be levers here"）
- 2026-02-12｜David Obstler (CFO)｜margin：銷售與行銷費用占營收比重，原文下一行接「roughly the mid-20s range」（原話："keep that sales and marketing as a percentage of revenues"）
- 2026-02-12｜David Obstler (CFO)｜margin：G&A 占營收約 5%（原話："Thank you for all the hard work you do there at around 5%"）
- 2026-02-12｜David Obstler (CFO)｜margin：去年 non-GAAP 營業利益率 22%；前一句稱現金流利潤率 27%（原話："So, it's all non-GAAP, and it was 22%"）
- 2026-02-12｜David Obstler (CFO)｜margin：解釋營業利益率有波動：消費型模式的變動快過招聘速度（原話："that changes faster than we can hire people"）
- 2026-02-12｜Unknown Executive｜margin：答覆 $10M 客戶與 $10 萬客戶的獲利結構差異時，改談加權平均後毛利率大致不變（原話："maintain our margins the same at the gross"）
- 2026-02-12｜David Obstler (CFO)｜capital_allocation：淨股數稀釋目標為 2.5% 至 3%（原話："our target in net share dilution, which is 2.5% to 3%"）
- 2026-02-12｜David Obstler (CFO)｜capital_allocation：併購策略強調審慎，過去聚焦補技術能力（前後文提到 Eppo、Metaplane）（原話："a thoughtful and disciplined acquisition strategy"）
- 2026-02-12｜Olivier Pomel (CEO)｜capital_allocation：長期以約 30% 營收投入 R&D，2025 年超過 $10 億、約 4,000 名工程師（原話："we've invested about 30% of revenues into R&D"）
- 2026-02-12｜Sean Walters (CRO)｜capital_allocation：宣布開始試行資安專屬銷售團隊（原話："we decided to start a pilot of security-focused sales teams"）
- 2026-02-12｜Adam Blitzer (COO)｜competition：稱 R&D 支出約為最接近同業的 3 倍（原話："about 3x the R&D spend of our next closest peer"）
- 2026-02-12｜Sean Walters (CRO)｜competition：稱資安市場的競爭對手正在整併（原話："competitors in this space consolidating"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：承認事後排查類需求用 Claude Code 這類工具也能得到不錯結果（逐字稿拼作 Cloud Code）（原話："you can get a pretty good result if you ask Cloud Code"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱預防性、主動式場景無法靠通用 coding agent 完成，因資料不會流經它們（原話："that just doesn't work at all because the data doesn't flow"）
- 2026-02-12｜Michael Whetten｜competition：回應通用 LLM 的程式碼資安能力：稱自家優勢是看得到程式碼在正式環境的部署狀況（原話："we can see how that code is deployed in production"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱 coding agent 會持續存在且做更多，公司定位是補充而非取代（原話："the agents are here to stay and they're going to do more"）
- 2026-02-12｜Alexis Le-Quoc (CTO)｜competition：被問進入門檻時，承認小模型沒有明確的資金門檻，護城河放在資料品質（原話："don't think there's a clear financial barrier of entry"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：回應 OpenTelemetry：稱資料收集從來不是護城河（原話："The collection has never been the moat"）
- 2026-02-12｜Adam Blitzer (COO)｜competition：自我定位為觀測市場中的高價位產品（原話："Datadog is a premium product"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱觀測市場占有率仍只在十幾個百分點中段（原話："our market share is still only in the mid-teens"）
- 2026-02-12｜David Obstler (CFO)｜competition：觀測市場規模 $300 億以上；擴大到資安、軟體交付等後 TAM 稱超過 $1,000 億（原話："a $30 billion-plus market"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：基礎設施監控 ARR 達 $16 億，日誌與 APM 各超過 $10 億（原話："$1.6 billion of ARR in infrastructure monitoring"）
- 2026-02-12｜Tim Knudsen｜product：資安產品 ARR 已超過 $1 億（原話："we've now surpassed $100 million in ARR"）
- 2026-02-12｜Tim Knudsen｜product：百萬美元客戶中 70% 用至少一項資安產品，但資安只占其 Datadog 支出 2%（原話："together is only 2% of their Datadog spend"）
- 2026-02-12｜Yrieix Garnier｜product：Flex Logs 的 ARR 接近 $1 億且快速成長（原話："approaching $100 million ARR and growing very rapidly"）
- 2026-02-12｜Yrieix Garnier｜product：BYOC（自帶雲）已有大型公司在預覽，並預期打開更多機會（原話："engaged with very large companies and previewing BYOC"）
- 2026-02-12｜Yanbing Li (CPO)｜product：Bits AI SRE 一月單月就有超過 2,000 家客戶跑調查（原話："more than 2,000 customers run investigation with Bits AI"）
- 2026-02-12｜Yuka Broderick｜product：Bits AI SRE 公開定價為每 20 次調查 $500（原話："Bits AI SRE $500 per 20 investigations"）
- 2026-02-12｜Yanbing Li (CPO)｜product：MCP server 自推出後用量呈指數式成長（原話："we've seen also exponential adoption and growth"）
- 2026-02-12｜David Obstler (CFO)｜product：LLM Observability 的 span 量一年增加 10 倍（原話："the last year, that has increased 10x"）
- 2026-02-12｜Alexis Le-Quoc (CTO)｜product：訓練時序模型 Toto 2025 年花費約 $75 萬（原話："We spent about $750,000 to train this"）
- 2026-02-12｜David Obstler (CFO)｜product：數位體驗監控（DEM）已大到公司也稱之為第四支柱（原話："we are also calling that a fourth pillar"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：承認對功能旗標與實驗平台的看法改變（過去視為商品化）（原話："we've changed our minds quite a bit on the topic"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：資料可觀測性過去被視為周邊市場，現在升到優先清單前列（原話："We thought also this was an interesting market"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：被問自主營運何時到來，稱無法判斷是一年或三年（原話："hard to tell whether we get there in a year or in 3 years"）
- 2026-02-12｜Unknown Executive｜product：被問自主營運的計價模式時，稱距離談定價還太遠（原話："too far away to be talking about pricing models"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：預期今年會有相當多公司把 AI 寫程式的轉換推進（原話："I would expect quite a bit of that to happen this year"）
- 2026-02-12｜Unknown Executive｜guidance：把財測保守度歸因於用量計價模式（原話："some of the conservatism we put in guidance"）
- 2026-02-12｜Unknown Executive｜commitment：稱對中期走勢很有信心，短期用量則不確定（原話："we're very confident about where we'll be in the midterm"）
- 2026-02-12｜Sean Walters (CRO)｜commitment：銷售團隊剛開完年度啟動會，稱全面投入 AI 銷售並已訓練每位業務（原話："we are going all in on AI"）
- 2026-02-12｜Unknown Executive｜risk：承認短期用量走勢無法確知（原話："how the usage is going to trend in 1 month from now"）
- 2026-02-12｜Unknown Executive｜risk：承認客戶會定期做用量優化，有時是公司主動建議（原話："we do see optimization on a regular basis"）
- 2026-02-12｜Olivier Pomel (CEO)｜risk：稱多數公司仍處於 AI 寫程式轉換的早期（原話："most companies are still early in the transition there"）
- 2026-02-12｜David Obstler (CFO)｜customer：新增客戶貢獻每年 ARR 成長約四分之一（原話："about 1/4 of that ARR growth each"）
- 2026-02-12｜David Obstler (CFO)｜customer：ARR 成長其餘約四分之三來自既有客戶多用產品與交叉銷售（原話："the remaining approximately 3/4 comes from"）
- 2026-02-12｜David Obstler (CFO)｜customer：客戶數超過 32,000，占約 50 萬目標客戶的邏輯數僅 7%（原話："that's a penetration in logos of only 7%"）
- 2026-02-12｜David Obstler (CFO)｜customer：百萬美元客戶今年成長到超過 600 家（原話："our $1 million customers, which this year grew to over 600"）
- 2026-02-12｜David Obstler (CFO)｜customer：首度揭露年花費超過 $1,000 萬的客戶指標；逐字稿數字為「over 60% growth, and that's now 34%」，未給明確客戶數，原文口徑不清（原話："growing quite rapidly, over 60% growth, and that's now 34%"）
- 2026-02-12｜David Obstler (CFO)｜customer：AI 原生客戶去年底占營收約 11%（原話："at the end of last year was about 11% of revenues"）
- 2026-02-12｜Adam Blitzer (COO)｜customer：前 20 大 AI 原生公司中有 14 家用 Datadog，AI 原生客戶群超過 650 家（原話："14 of the top 20 AI native companies are using Datadog"）
- 2026-02-12｜David Obstler (CFO)｜customer：整體毛留存率 97% 以上（企業 98% 以上，中小與中型 96% 以上）（原話："retention percentage. It's 97% plus in the company"）
- 2026-02-12｜David Obstler (CFO)｜customer：只有約一半客戶同時使用三大支柱（原話："only about half of our customers use all three pillars"）
- 2026-02-12｜David Obstler (CFO)｜customer：三大支柱都用的客戶，花費是其他客戶的 15 倍（原話："In fact, they spend 15x more"）
- 2026-02-12｜David Obstler (CFO)｜customer：一半客戶用 4 項以上產品，用 10 項以上的僅 9%（原話："half of our customers have 4-plus products"）
- 2026-02-12｜Sean Walters (CRO)｜customer：Key accounts 業務第二年的目標從開會數轉向營收與成交（原話："goals are shifted much more to revenue and closing deals"）
- 2026-02-12｜Sean Walters (CRO)｜customer：Key accounts 2025 年有比預期快的成交，且正快速擴張（原話："wins that are already expanding very rapidly"）
- 2026-02-12｜Sean Walters (CRO)｜customer：財星 500 大客戶的花費中位數不到 $50 萬（原話："is still modest at less than $0.5 million per customer"）
- 2026-02-12｜Sean Walters (CRO)｜customer：拉美約占營收 5%，成長遠快於整體（原話："they're growing far faster than our overall revenue"）
- 2026-02-12｜Sean Walters (CRO)｜customer：只稱 2025 訂單表現「stellar」，未給金額（原話："shows our bookings by year, including a stellar 2025"）
- 2026-02-12｜Adam Blitzer (COO)｜customer：計價為用量基礎並有量、承諾、多產品、期限等折扣，稱客戶越成長曲線越彎（原話："We have volume-based pricing"）
- 2026-02-12｜Unknown Executive｜customer：解釋客戶 ARR 出現短期下滑：簽更長期承諾換折扣時可能暫時下降（原話："it might drop you temporarily from where you were"）
- 2026-02-12｜Unknown Executive｜customer：承認過去幾年偏重從既有大客戶擴張，較少花力氣從零開發新客戶（原話："bit victims of our own success"）

### 問答異常語氣（迴避／改口／保留）
- DDOG_Q2_2026_Earnings_Call_20260806.md｜問：Sanjit Singh：最大客戶新合約的期限是否相近？用量下降是單價降低還是流失／降級，且是否延續至全年？｜答法：CEO 稱不評論個別客戶、「there's not a lot more we can share」；CFO 只談財測方法，未回答合約期限與降量原因
- DDOG_Q2_2026_Earnings_Call_20260806.md｜問：Alex Zukin：最大客戶續約的期限、折扣費率卡或產品數是否讓合約更黏？｜答法：CFO 稱「I won't comment on this」，改談一般企業客戶的年約加承諾加用量模式；CEO 僅說續約「a lot of continuity」
- DDOG_Q2_2026_Earnings_Call_20260806.md｜問：Brad Reback：剔除最大客戶的季減後，核心財測是否會高 300–400 bp？｜答法：CEO 稱「I can't speculate」，改談剔除該客戶後成長率相同與整體加速，未給數字
- DDOG_Q2_2026_Earnings_Call_20260806.md｜問：KeyBanc：Q3 財測的季增幅低於過去 Q3 的指引水準，趨勢與假設為何？｜答法：CFO 回答重複財測方法論與保守原則及最大客戶下降，未提供具體假設數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Sanjit Singh (Morgan Stanley)：自主營運一年後、三年後長什麼樣？是否需要自己掌握軟體交付管線（build vs buy）？｜答法：Olivier Pomel 稱時程 'hard to tell whether we get there in a year or in 3 years'，未給具體里程碑；build vs buy 只點名功能旗標與資料可觀測性兩個已改變看法的領域，並稱 'a few other areas... I'm not going to tell you about it'
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Fatima Boolani (Citi)：自主營運商業化後，計價模式是否會根本改變（結果導向計價）？｜答法：回答 'too far away to be talking about pricing models'、'It doesn't mean we have a pricing packaging in mind just yet'，未給計價方向，改談用量計價較容易適應
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Fatima Boolani (Citi)：$1,000 萬客戶與 $10 萬客戶的增量獲利／單位經濟是否有實質差異？｜答法：Unknown Executive 只答量折扣與加權平均後毛利率大致不變，未直接拆解大客戶的獲利結構差異
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Andrew Sherman (TD Cowen)：三大支柱使用率 53% 通常缺哪一塊產品？未來幾年會到多少？｜答法：Sean Walters 稱每個客戶情境不同、不強推三支柱，Yuka Broderick 補 'I wouldn't think of it as one particular pillar that's missing'；兩人都沒給未來使用率數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Keith Bachman (BMO)：資安產品組合的邊界在哪、哪些領域不打？｜答法：Tim Knudsen 談既有成熟預算與統一平台優勢、AI 帶來新領域，未指出任何不打的領域
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Ittai Kidron (Oppenheimer)：小模型成本只要 $75 萬，第三方進入門檻多高？AI 對公司業務的風險是什麼？｜答法：Alexis Le-Quoc 談資料與評測集的護城河、並承認沒有明確的資金門檻；Olivier Pomel 補 R&D 投入金額；兩人都沒列出 AI 對業務的具體風險
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Koji Ikeda (BofA)：財星 500 大客戶如何把花費中位數拉高？2025 年 TCV 訂單（分析師稱 $45 億以上）中大客戶與中型客戶各占多少？｜答法：Unknown Executive 談長銷售週期、工具整併與 key accounts，未拆分 TCV 訂單的客群貢獻，也未確認分析師提出的 $45 億數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Eric Heath (KeyBanc)：BYOC 的可服務客群、何時廣泛推出、進入市場策略？｜答法：Yrieix Garnier 稱已在預覽並有付費客戶，客群點名資料在地化與合規產業、超大規模客戶；未給一般上市時程
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Arti Vula (JPMorgan)：目前 AI 產生的程式碼量能否量化、是否已進到正式環境並帶動用量？｜答法：Unknown Executive 只做定性回答（訊號與開源都顯示程式碼變多），稱多數公司仍在早期，未給量化數字；改以 'we should see where we are at the end of the year' 收尾

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 4 |
| customer_second_source | found | 5 | 4 |
| customer_concentration_credit | found | 8 | 4 |
| supply_demand_durability | found | 8 | 4 |
| regulatory_antitrust | found | 1 | 1 |
| reg_tariff_export | found | 1 | 4 |
| geo_supply_chain | found | 5 | 4 |
| end_markets | found | 11 | 6 |
| substitute_technology | found | 3 | 4 |
| channel_business_model_shift | found | 1 | 4 |
| capital_markets_pricing | found | 5 | 2 |
| major_events | found | 2 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260924","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","irr_base_pct":1.4,"ev5y_pct":4.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.1,"ev5y_pct":4.3,"irr_base_pct":1.4,"max_dd_pct":-70,"bull_5y_price":450.0,"bear_5y_price":94.4,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","price_at_dd":251.49,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"DDOG","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Datadog, Inc."},"oneliner":"Datadog 非 AI 客戶連五季加速，最大客戶已按合約下限估入指引；但 179 美元買進的 Base 年化只有約 7.5%，股權激勵又占營收近兩成，等 175 美元以下再談分批。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20261108/scenario.json","answers":{"q1_business":{"verdict":"向企業收雲端與 AI 系統的監控、資安用量費，錢卡在「生產環境資料集中到同一平台」這一節。","reasoning":"收費方式是年度承諾加實際用量，客戶用得越多、產品越多，付得越多。2026 年 Q3（2026-11-04 法說會 CFO 準備稿）營收 11.97 億美元，年增 35%；non-GAAP 毛利率 81.2%、營業利益率 28%。公司不揭露營收分部，只給 ARR：基礎設施監控超過 20 億美元、年增 30% 中段，日誌與 APM 在 2025 年底各超過 10 億美元。單點依賴是最大客戶：公司未點名，外界指為 OpenAI，屬媒體推測。它已簽九位數續約但降低用量，Q4 指引只按合約下限估入。AI 原生客群在 2025 年底約占營收 11%（2026-02-12 投資人日 CFO），最新占比與最大客戶單獨占比事實表未涵蓋。事實表的季度 KPI 停在 Q2，Q3 數字皆取自法說會逐字稿。","fact_refs":["f_kpi0_revenue_gaap","f_kpi4_stock_based_compensation","f_kpi9_customers_with_arr_100k","f_kpi12_net_revenue_retention_tr","f_kpi15_ai_yoy","f_earnings_recency"],"verdict_values":{"revenue_quality":"用量計價加承諾下限，毛留存率 90% 中後段、淨留存率 120% 出頭（2026-11-04 CFO）。短期能見度低：最大客戶 Q3 用量遠高於下限，Q4 指引只算下限，季增數字會跟著波動。","unit_econ_note":"約 4,860 家年付 10 萬美元以上客戶貢獻約 91% ARR（2026-11-04）。使用六項以上產品的客戶占 41%，一年前 31%。公司對大客戶給量價折扣；投資人日被問到千萬美元客戶的單位經濟差異時，只答加權毛利率大致不變，未拆解。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"營收年增 30% 上下、non-GAAP 利益率改善、FCF 利潤率 26%，但 GAAP 營業利益率只有 2.3%，複利品質要扣掉股權激勵才算數。"},"industry":{"clock_phase":"II","sd_verdict_source":"供需持久性判斷為結構性持久。雲端遷移與 AI 上線同時增加監控資料量，非 AI 客戶連五季加速（2026-11-04 CEO）；可逆的部分集中在少數 AI 原生大客戶，他們會用折扣和自建壓低用量，這部分反映在 Bear 機率。景氣位置的依據是客戶用量與新簽金額，不是股價。","bargaining":{"up":"上游雲端與模型供應商的成本與條款事實表未涵蓋。Bits AI 定價貼近推論成本（2026-11-04 CEO），AI 層的價值多半留給模型供應商或回饋客戶。","down":"一般企業客戶分散，議價力弱；頂端 AI 原生客戶議價力強，提前續約換更好單價，最大客戶可把用量降到合約下限。","geo":"10-K 未見半導體或中國供應鏈依賴（程式抽取結果，非逐頁確認）；約 44% 全職員工在美國以外，其中 34% 在法國。"},"profit_pool_dir":"利潤池方向事實表未涵蓋。定性看，AI 層的增量利潤偏向模型與算力供應商，觀測層靠用量以及資安、軟體交付的擴張來補。","tam_table":[{"item":"公司口徑觀測市場","value":"300 億美元以上（2026-02-12 投資人日 CFO）"},{"item":"公司口徑含資安、軟體交付後 TAM","value":"超過 1,000 億美元（同上）"},{"item":"第三方 2026 年估計","value":"33.5 億至 341 億美元，相差十倍，CAGR 11%–16%；最低值比 Datadog 自身營收還小，只能是窄口徑"},{"item":"Gartner 2028 年觀測平台市場","value":"142 億美元（2025-08 報導）"},{"item":"公司自述份額","value":"十幾個百分點（2026-11-04 CEO 引產業分析師）"},{"item":"客戶家數滲透率","value":"約 7%，目標客戶約 50 萬家（2026-02-12 CFO）"},{"item":"利潤池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河持平：執行面在擴大，定價面被頂端客戶的折扣抵銷，整體不標上升。","reasoning":"機制是把指標、日誌、追蹤、資安和 AI 監控放進同一份生產環境資料，產品越多、工具越難拆。可證方向：使用四項以上產品的客戶由 54% 升到 61%，十項以上由 8% 升到 16%（2026-11-04 CEO），毛留存穩在 90% 中後段。Ramp 採用率 34%、年持平，沒有份額流失，也沒有明顯擴大。不標上升的原因有二：最大客戶用量下降，提前續約的大客戶也拿到更好單價。同業 ROIC 事實表未涵蓋，改以留存與產品滲透當比較軸；利潤率上，FCF 利潤率與 Dynatrace 接近，GAAP 營業利益率低約 11 個百分點，主要差在研發密度 42.6% 對 23.8%。AI 曝險：附著點在自家生產資料，屬強化；通用 coding agent 繞過事後排查的部分屬替代（2026-02-12 CEO 承認事後排查用通用工具也有不錯結果），分界年約 2028。公司未揭露 AI 產品 ARR，淨增量無法計算。","fact_refs":["f_peer_ddog_gross_margin_pct","f_peer_ddog_operating_margin_pct","f_peer_ddog_fcf_margin_pct","f_peer_dt_operating_margin_pct","f_peer_dt_fcf_margin_pct","f_kpi12_net_revenue_retention_tr"],"verdict_values":{"moat":{"mechanism":"同一份生產環境資料支撐多項產品，工具整併後拆分成本高，資料與工作流程構成轉換成本。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Gartner 連六年列領導者、非 AI 客戶連五季加速、多產品滲透上升。定價面由穩定轉向略縮：2026-11-04 法說會證實多家大客戶提前續約換更好單價，Flex Logs 與 Infinite Cardinality Metrics 也在降低客戶單位成本。兩者抵銷，判持平。","competitor_notes":[{"name":"SNOW","strategy_note":"毛利率低約 12.6 個百分點，靠收購 Observe 從資料平台切入監控，威脅在資料層綑綁，尚無份額數據。"},{"name":"DT","strategy_note":"企業市場主要對手，GAAP 獲利較好、研發密度低很多；Datadog 的差異在平台廣度與新品速度。"},{"name":"ESTC","strategy_note":"日誌與搜尋起家，FCF 利潤率低約 6.6 個百分點，Flex Logs 搶的正是這類日誌預算。"},{"name":"NOW","strategy_note":"工作流程平台，不是直接監控對手；在 IT 維運入口與 AI agent 層有重疊，FCF 利潤率高約 4.9 個百分點。"}],"spread_notes":null,"peer_na_reason":"同業 ROIC 與份額事實表未涵蓋，只能比利潤率與研發密度。","threats":[{"level":"🔴","text":"資料、資安與監控合併成單一平台：Palo Alto 收購 Chronosphere、Snowflake 收購 Observe、Cisco 整合 Splunk。受損方向在傳統企業與資安綑綁預算；來源是第三方評論，尚無份額流失數據，攻擊者投入金額事實表未涵蓋。","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"頂端 AI 原生客戶自建或部分遷移：2024 年已有一家縮減並部分改用內部工具，最大客戶 2026 年再降用量。受損範圍集中在少數超大客戶，一般企業沒有自建的工程量。","p":"35%","evidence_refs":["customer_second_source#4"]},{"level":"🟡","text":"架構與計價替代：eBPF、資料留在客戶 VPC、按基礎設施計價，加上超過 40 家廠商競爭下總持有成本成為標準問題，Grafana ARR 已超過 4 億美元。架構替代的說法出自競品行銷文，Datadog 也已推 BYOC，CEO 稱資料收集從來不是護城河；本次視為點對點壓價，不是架構取代。","p":"25%","evidence_refs":["substitute_technology#0","supply_demand_durability#1","supply_demand_durability#7"]},{"level":"🟡","text":"開發工具與通用 coding agent 往下吃監控功能。第三方預測只取得論點，缺內文與廠商名單；CEO 於 2026-02-12 承認事後排查用通用工具也有不錯結果，但主動偵測需要生產資料流，通用工具碰不到。","p":"30%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（未經投入資本驗算，只以資本支出占營收 3–4% 推定周轉高；扣股權激勵後利益率僅個位數）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是工程團隊，決策者是平台與技術主管，付款者是財務長；三者都需要知道正式環境出了什麼事。毛留存 90% 中後段是代理讀數。Q2 法說會分析師提到財務長抱怨帳單，表示問題在花多少，不在要不要用。"},{"item":"決策層級","level":"🟡","text":"客戶的替代決策落在每種資料的保留層級，不是整個平台。Q3 CEO 承認大客戶續約時會調整資料層級；最大客戶可把用量降到下限。反方向證據是客戶持續整併三到五套工具進 Datadog。"},{"item":"價值鏈分配","level":"🟡","text":"頂端買方集中且議價力強，提前續約換更低單價；AI 層定價貼近推論成本，價值流向模型供應商或客戶。自研 Scout 模型降低推論成本，是公司保留價值的做法，貢獻尚未量化。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的工具軟體，沒有民生價格上限問題；監管面只見 10-K 列出的歐盟 AI Act 與隱私法規一般風險，未見反壟斷事項。"}],"roiic":"無法計算：事實表未涵蓋投入資本、折舊與營運資金變動。GAAP 代理：FY2023 到 FY2025 營收增加約 13 億美元，GAAP 營業利益由約 −0.33 億美元變為約 −0.44 億美元，扣股權激勵後的增量利潤接近零。","reinvest_rate":"無法按公式計算。可得代理：FY2026 資本支出加資本化軟體占營收 3–4%；真正的再投資走損益表，TTM GAAP 研發密度 42.6%。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，所需的折舊、營運資金與收購淨額都不在證據包內，不以推估代入。"}}}},"q3_growth":{"verdict":"五年後仍有跑道：以公司口徑份額十幾個百分點計，第五年滲透率仍低於 35%，資安與 AI 監控是第二條曲線。","reasoning":"成長主要靠量：既有客戶多用、多買產品，新客戶貢獻約 30% 年增量；價格不是推力，頂端客戶還在拿折扣；併購與回購都不重要。共識 EPS 年複合 21.4%（FY2026 的 2.55 到 FY2028 的 3.76，兩個跨度，Koyfin 快照），但 2.55 低於 11-04 指引下緣，以指引中位 2.74 為基期則是 17.1%。內生上界無法計算，缺口列為無法歸因，長期信心上限為中。定性看，差距靠利益率由 24% 升到 28–30%，沒有靠回購。市場分母要小心：Mordor 的 33.5 億美元比 Datadog 自身營收還小，只能是窄口徑；公司口徑 300 億美元以上和 CEO 說的十幾個百分點份額對得上。若採 Gartner 2028 年 142 億美元，份額會高得多，跑道判斷要下修，這是本結論最可能出錯的地方。以 27% 對市場 14% 的相對增速，份額翻倍到 30% 約需 6 年。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主，產品滲透次之，價格為負向；併購與回購貢獻可忽略。","runway_years":6,"runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本與再投資明細，內生上界無法計算，不以推估代入。","segments":[{"item":"基礎設施監控","value":"ARR 超過 20 億美元，年增 30% 中段（2026-11-04）"},{"item":"日誌管理","value":"ARR 超過 10 億美元，年增 30% 中段（2025 年底）"},{"item":"APM","value":"ARR 超過 10 億美元，年增 30% 中段（2025 年底）"},{"item":"RUM","value":"ARR 超過 2 億美元，年增逾 50%（2026-08-06）"},{"item":"資安產品","value":"ARR 超過 1 億美元（2026-02-12）；百萬美元客戶的資安支出只占其 Datadog 支出 2%"},{"item":"Flex Logs","value":"ARR 接近 1 億美元（2026-02-12）"},{"item":"GPU 監控","value":"裝置數今年增 8 倍，CEO 稱尚未廣泛收費，不在目前成長內"}],"decay_signals":["股權激勵占營收 19.6%（2026 Q2），高於 5%；逐年序列事實表未涵蓋，保守計為亮起。其餘九項未亮或無資料。"]}}},"q4_capital":{"verdict":"資本配置偏弱：沒有回購證據，股權激勵的淨稀釋目標高於 1.5% 的及格線，併購報酬無法驗證。","reasoning":"FY2025 FCF 9.15 億美元對 GAAP 淨利 1.08 億美元，轉換率約 8.5 倍，高得不尋常的原因是股權激勵不花現金：2026 Q2 單季股權激勵 2.20 億美元，占營收 19.6%、占 non-GAAP 營業利益 85.7%。CFO 的淨稀釋目標是每年 2.5–3%（2026-02-12 投資人日）。現金及有價證券 52 億美元，扣債務後淨現金約 39 億美元；FY2026 資本支出加資本化軟體降到營收 3–4%。營運槓桿正向：Q3 營業費用年增 25%，低於營收 35%。現金去向四分、回購紀錄與債務到期結構事實表未涵蓋。","fact_refs":["f_kpi4_stock_based_compensation","f_kpi3_free_cash_flow","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"Adaptive ML 收購價未揭露，歷次併購的已實現報酬事實表未涵蓋。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"證據包內沒有回購紀錄。"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"CFO 淨稀釋目標每年 2.5–3%（2026-02-12 投資人日），高於 1.5%；實際逐年序列事實表未涵蓋。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購或回購撐，且證據包沒有現金去向明細，展開也沒有數字可填。"}}}},"q5_valuation":{"verdict":"現價要求 EPS 五年複利約 19% 才賺得到 8% 年化；這條路徑我相信走得到，但價格沒有留失誤空間。","reasoning":"現價 179.04 美元對 FY2026 指引中位 2.74 是 65.3 倍，對事實表舊共識 2.55 是 70.2 倍。以終端 40 倍推回，要賺 8% 年化需要 FY2031 EPS 約 6.58 美元，五年複利約 19%；Base 是 18.6%。估值也不便宜：前瞻 EV/S 13.4 倍，扣股權激勵後的現金流殖利率不到 1%（TTM FCF 約 11 億美元減約 8 億美元股權激勵，後者以 Q2 的 19.6% 外推，屬估計）。賣方平均目標 271.57 美元（8 月 MarketBeat）比現價高 52%，方向上反對不追，但這是財報前數字，全距未知，不調整判斷。我與賣方的差別在終端倍數，不在盈餘：Base 的 FY2027 EPS 3.40 美元高於舊共識 2.98 美元。同業現值倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_ev_s_fwd","f_pe_current","f_pe_percentile","f_ev_s_percentile","f_rsi14","f_week26_return_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"non-GAAP 前瞻本益比搭配 PEG，以前瞻 EV/S 與扣股權激勵的現金流殖利率交叉檢查。","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率與研發密度，沒有同業前瞻本益比或 EV/S，無法做同級倍數對照。"},"peg":3.28,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 65–70 倍，PEG 3.28（70.21 倍除以共識年複合 21.4%），以指引基期計約 3.8，都高於 2 的昂貴線；Base 年化約 7.5%，略低於 8%。比前份便宜一級，因為股價跌約 29%，但還沒到合理。五年分位無資料：事實表只有 3–4 個年度端點，不能當五年分位。短期上檔以 FY2027 EPS 3.40 美元乘 60 倍估一年，中期以 FY2029 EPS 4.87 美元乘 50 倍估三年。","upside_short_pct":13.9,"upside_mid_pct":36.0,"denominator_disputed":true,"denominator_note":"non-GAAP EPS 排除占營收近兩成的股權激勵，GAAP 本益比 248.7 倍，兩個分母差三倍以上。共識 FY2026 的 2.55 又低於新指引下緣。因此不用低本益比或 PEG 主張便宜。"}}},"q6_how_wrong":{"verdict":"最可能看錯在非 AI 加速只是階段性回補，或股權激勵讓每股價值跟不上報表成長。","reasoning":"完整反證見反證紀錄。產業態勢為雙向拉鋸：競爭面，資安與資料平台收購監控廠商；結構面，AI 工作負載與工具整併讓領先平台受益，Gartner 連六年列領導者；客戶結構面，AI 原生集中度是新變數。最大客戶的合約期限、折扣與降量原因在 2026-08-06 法說會遭迴避，2026-11-04 仍未說明；投資人日對大客戶單位經濟與 AI 業務風險也未正面回答，這些是資料缺口。歷史最大回撤、空方最強數字事實表未涵蓋。","fact_refs":["f_kpi4_stock_based_compensation","f_kpi13_rpo_current_rpo","f_kpi14_billings","f_kpi15_ai_yoy"],"verdict_values":{"trap":{"verdict":"🟡","label":"一項衰退訊號亮起（股權激勵），領先指標放緩待驗"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":2.74,"pe":65.34,"basis":"FY2026 全年 non-GAAP EPS 指引中位（2026-11-04 法說會 CFO，2.73–2.75），與終端倍數同為當年度 non-GAAP EPS 口徑；事實表共識 2.55 低於指引下緣，視為舊快照不採用。"},"eps":{"bull":[3.7,4.83,6.17,7.6,9.09],"base":[3.4,4.11,4.87,5.7,6.42],"bear":[2.7,2.6,2.7,2.82,2.95]},"pe":{"bull":48,"base":40,"bear":28},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":16,"base_cagr_pct":13},"max_dd":{"lo":-65,"hi":-45,"basis":"上緣 −45%：FY2026 指引 EPS 2.74 美元乘 36 倍，約 99 美元。下緣 −65%：Bear 低點 FY2028 EPS 2.60 美元乘 24 倍，約 62 美元，倍數取終端 28 倍再打約 15% 恐慌折價。前份估 −70%。本股六週已跌 29%；事實表沒有完整歷史回撤，未用歷史值。","trigger_time":null},"basis":{"bull":"非 AI 客戶維持 high 20s 以上、AI 原生客群擴散到更多大客戶：FY2031 營收約 133 億美元，non-GAAP 利益率 34%，股數年增 2.5%；終端 48 倍。","base":"FY2027 營收約 56 億美元（共識 55.3 億美元略上修），之後增速逐年降到 14%，FY2031 營收約 107.5 億美元；non-GAAP 利益率 26% 升到 29.5%，淨利息收入 2–3.3 億美元，稅率 21%，股數年增 2.75%，稀釋已含在 EPS 內。終端 40 倍對應之後 EPS 年增約 13%；同業現值倍數事實表未涵蓋，只能對照自身現值 65 倍。","bear":"非 AI 客戶增速掉到 20% 以下、最大客戶與頂端 AI 客戶壓用量：FY2031 營收約 76 億美元，利益率 19.5%，EPS 約 2.95 美元；終端 28 倍來自成長熄火測試。測試以 Base FY2029 EPS 4.87 美元計算：年增降到 15%／10%／5% 時倍數 35／28／20 倍，跌幅 −5%／−24%／−46%，跌幅小於 30% 算通過，三項過兩項。機率 30% 的依據是領先指標放緩、最大客戶揭露不足、內生上界無法驗證，Q3 超預期不足以下調。"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"帳單年增 30%、RPO 年增 38%，都比上季放緩；Q4 指引季增持平；非 AI 客戶一年前年增只有約 20%。","assumption":"非 AI 客戶連五季加速是結構性的，AI 寫程式帶來更多軟體和監控量。","consequence":"若只是雲端優化結束後的回補，加上 AI 預算排擠，非 AI 年增掉回 20% 以下，FY2031 EPS 約 2.95 美元，乘 28 倍約 83 美元，五年虧 54%。","ruling":"採納為 Bear 主路徑，機率 30%，與唯一致命點同一件事。目前毛留存穩定、產品滲透上升，尚無惡化跡象。","watch":"每季非 AI 客戶年增區間、cRPO 年增。","evidence_refs":["end_markets#3"],"fact_refs":["f_kpi13_rpo_current_rpo","f_kpi14_billings","f_kpi15_ai_yoy"]},{"view":"論點失敗","evidence":"CEO 於 2026-02-12 承認事後排查用通用工具也有不錯結果；CTO 同日承認小模型沒有明確資金門檻，自家時序模型訓練只花約 75 萬美元。","assumption":"生產資料是 AI 時代的護城河。","consequence":"若通用 agent 能直接讀取客戶自有遙測，Datadog 會從工作入口退回資料管線，產品溢價下降。","ruling":"部分採納，列為長期風險。Bits AI 是公司史上採用最快的產品，Scout 降低推論成本，短期是加分；但 AI 產品 ARR 未揭露，淨增量未證。","watch":"AI 產品客戶比率上升時，淨留存是否跌破 115%。","fact_refs":["f_kpi12_net_revenue_retention_tr"]},{"view":"論點成功但股東經濟變差","evidence":"股權激勵 2026 Q2 占營收 19.6%、占 non-GAAP 營業利益 85.7%；TTM GAAP 營業利益率 2.3%；CFO 目標淨稀釋每年 2.5–3%；Bits AI 定價貼近推論成本。","assumption":"non-GAAP 利益率提升會轉成每股價值。","consequence":"營收達到 Base，股數卻每年增約 2.75%，利潤大部分歸員工；AI 層價值交給模型供應商，單位收入下降。","ruling":"採納。終端倍數定 40 倍，Base EPS 已用稀釋後股數，並把 FY2027 股權激勵占營收列入監測。","watch":"TTM 股權激勵占營收、稀釋股數年增。","fact_refs":["f_kpi4_stock_based_compensation","f_peer_ddog_operating_margin_pct"]},{"view":"價格已反映太多","evidence":"FY2026 指引中位 65.3 倍，PEG 3.3 以上，前瞻 EV/S 13.4 倍。","assumption":"跌 29% 後定價已合理。","consequence":"要賺 8% 年化需 EPS 五年複利約 19%，Base 18.6%，沒有留失誤空間；倍數往 40 倍靠攏，盈餘成長大部分會被吃掉。","ruling":"採納，這就是不追的約束條件，股價到 175 美元以下才解除。","watch":"收盤價對 175 美元；FY2027 指引後的 Base EPS。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_ev_s_fwd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 251.49 → 本次 179.04（-28.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=251.49","side_b":"本次 price_at_dd=179.04","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 251.49 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 251.49 美元：Bull 價 450、Bear 價 94.4，五年期望值 +4.3%，基準年化 1.4%，不對稱比 1.1","side_b":"本次情境、股價仍用 251.49 美元：Bull 價 436.32、Bear 價 82.6，五年期望值 −0.8%，基準年化 0.4%，不對稱比 0.91","ruling":"先換情境、股價不動：五年期望值少 5.1 個百分點，基準年化少 1.0 個百分點。不對稱比由 1.1 變為 0.91。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 251.49 美元：五年期望值 −0.8%，基準年化 0.4%，不對稱比 0.91","side_b":"本次情境、股價 179.04 美元：五年期望值 +39.3%，基準年化 7.5%，不對稱比 2.22","ruling":"再換股價、情境不動：起點價下跌 28.8%，五年期望值多 40.1 個百分點，基準年化多 7.1 個百分點，不對稱比由 0.91 升到 2.22。合計五年期望值比前份多 35.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"Q4 指引季增持平對排除最大客戶仍加速","cause":"新證據","prior_field":null,"side_a":"Q4 營收指引 11.9–12.0 億美元，對 Q3 的 11.97 億美元幾乎零季增，年增降到 25–26%；上一季的 Q3 指引也曾顯示年增由 36% 降到 28–29%。","side_b":"CFO 稱排除最大客戶，Q4 隱含年增在 30% 低到中段，並把季增放緩歸因於最大客戶只算合約下限、提前續約折扣、12 月季節性三件事。","ruling":"可調和的程度差異，採 B 側但打折。上一季同樣保守的 Q3 指引實際超出上緣 4.5%，保守是真的。管理層稱全是好消息，本次不全採信：提前續約的單價折讓是實際收入損失，標為未證、監測；若 2027 年上半年連兩季季增低於 4%，這項一次性歸因視為不成立。","evidence_level":"公司法說會（2026-11-04 CFO、CEO）；三項因素的金額拆分公司未提供","settle_metric":"2027 年 Q1、Q2 營收季增率與排除最大客戶年增","if_then":["若 2027 年 Q1 季增 ≥5% 且排除最大客戶年增 ≥30%，上調 Base 路徑，價格在新門檻內就分批反買首批","若連兩季季增 <4%，停止加碼並下修 Base 路徑 5%","若股價先漲過 215 美元而上述數字未到，不追"],"evidence_refs":["end_markets#3"]},{"axis":"帳單、RPO 放緩對營收維持 35%","cause":"新證據","prior_field":null,"side_a":"帳單年增由 Q2 的 38% 降到 30%，RPO 由 43% 降到 38%，cRPO 由約 40% 降到 30% 中段；Q3 淨增客戶只有約 100 家（33,400 到 33,500）。","side_b":"CFO 連兩季強調營收比帳單與 RPO 更能反映趨勢；RPO 年限略拉長，年付 10 萬美元以上客戶增加約 140 家。","ruling":"可調和，但偏向 A 側警示。降幅和最大客戶降量、折扣續約的說法相符，不是新的惡化來源；不過 cRPO 增速已貼近營收，下一季要看是否止穩。","evidence_level":"公司法說會（2026-08-06、2026-11-04 CFO）","settle_metric":"cRPO 年增","if_then":["若 cRPO 年增連兩季低於 25%，減碼一半並停止加碼","若 cRPO 年增回到 35% 以上且價格在門檻內，分批反買首批"]},{"axis":"管理層前後說法：財測去風險與最大客戶揭露","cause":"新證據","prior_field":null,"side_a":"2026-08-06 CEO 稱今年剩餘財測已完全去風險，2026-11-04 CEO 又說提前續約是與上季唯一不同的新逆風；最大客戶的合約期限、折扣與降量原因兩次法說都沒有回答。","side_b":"同期實績超指引：全年營收指引由 44.5–44.7 億美元升到 45.15–45.25 億美元，全年 non-GAAP 營業利益率由 23% 升到 24%。","ruling":"結果站 B 側，揭露站 A 側。指引品質可信，客戶集中度的能見度不足，所以 Bear 機率維持 30%，不因 Q3 超預期下調。","evidence_level":"公司法說會逐字稿；最大客戶占比為資料缺口","settle_metric":"下次續約承諾金額與期限（公司未揭露）","if_then":["若 10-K 揭露單一客戶占營收 ≥10% 且降幅大於指引隱含值，減碼一半","若 FY2027 指引列明最大客戶按下限估算，且非 AI 年增仍為 high 20s，分批反買首批"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#5"]},{"axis":"FY2026 EPS 分母：舊共識對新指引","cause":"方法變動","prior_field":null,"side_a":"事實表共識 2.55（2026-11-07 Koyfin 快照），前瞻本益比 70.2 倍。","side_b":"2026-11-04 全年指引 2.73–2.75；營收共識 45.2 億美元已跟上新指引。","ruling":"採 B 側。快照值低於指引下緣，應是未隨財報更新，FY2027、FY2028 也可能偏低。情境起點改用指引中位 2.74，共識欄位照錄但不承重。","evidence_level":"公司指引優先於未更新的聚合快照","settle_metric":"下一期共識快照的 FY2026 是否 ≥2.73","if_then":["若新快照 FY2027 共識 ≥3.30，維持 Base 第一年 3.40 美元，門檻 175 美元不動","若 FY2026 已更新而 FY2027 共識仍 <3.00，下修 Base 路徑 5%，門檻同比下調到約 166 美元"]},{"axis":"現在就買的最強論證（本次不追）","cause":"價格變動","prior_field":null,"side_a":"非 AI 客戶連五季加速、Q3 超指引 4.5%、non-GAAP 利益率 28%、最大客戶有合約下限兜底；股價六週內由 251 美元跌到 179 美元，RSI 28。前份約定的 185 美元已觸發，當時也說共識上修要上調門檻。","side_b":"已跌多少不是安全邊際。Base 年化約 7.5%，未到 8%；股權激勵占營收近兩成，扣掉後現金流殖利率不到 1%；Q4 才是第一個最大客戶落到下限的季度，FY2027 指引還沒出。","ruling":"站 B 側，但差距只有幾個百分點。這不是看壞，是價格還差一點，股價再跌約 2% 就進入分批範圍。兩側不是不可調和，差別在時點與價格。","evidence_level":"法說會與情境試算","settle_metric":"收盤價對 175 美元","if_then":["若股價收在 175 美元以下，重跑判斷並分批反買首批","若股價未到 175 美元就漲過 215 美元且 FY2027 指引未出，不追"]},{"axis":"前份漂移：價格帶動的欄位","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份 251.49 美元，估值在最高警示級，最大回撤估 −70%，Bull 25%、Bear 30%。","side_b":"本次 179.04 美元，前瞻本益比由約 98.6 倍降到 65 倍，估值降一級為偏貴；最大回撤估 −45% 至 −65%，Bull 25%、Bear 30%。","ruling":"估值改善主要因價格下跌約 29%，FY2026 EPS 上修只占小部分。機率不因價格而動，Bear 主路徑沒有被排除。","evidence_level":"事實表價格與法說會指引","settle_metric":"前瞻本益比","if_then":["若股價收在 175 美元以下，分批反買首批","若股價回到 215 美元以上且基本面未上修，不追"]},{"axis":"前份漂移：基本面欄位","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：時機評級 B、陷阱低風險、護城河持平、五年後跑道寬、品質複利成長、無景氣位置，結論觀望。","side_b":"本次：時機評級 B、陷阱升為中度、護城河持平、跑道寬、品質複利成長、無景氣位置，結論仍是不追。","ruling":"只有陷阱一欄變動：帳單與 RPO 放緩、提前續約折價是 2026-11-04 才確認的新證據，加上股權激勵超標，由低風險升為中度。其餘欄位維持，因 Q3 的加速與折價相互抵銷。","evidence_level":"2026-11-04 法說會","settle_metric":"cRPO 年增與非 AI 客戶年增","if_then":["若 cRPO 連兩季低於 25%，減碼一半","若非 AI 年增掉回 20% 以下，清倉"]},{"axis":"行動門檻變動：分批重啟價位","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","side_b":"股價收盤回落至175美元以下（Base五年年化約8%）才重跑判斷分批；FY2027指引後按Base EPS同比調整","ruling":"舊門檻已觸發（179.04 美元低於 185 美元），本次就是觸發後的重跑。重跑結果 Base 五年目標約 257 美元，低於前份回推的約 270 美元：EPS 上修，但終端倍數下調到 40 倍，反映提前續約折價與股權激勵，8% 年化對應價由 185 美元改為 175 美元。動作仍是分批反買，未觸發前不追，不是減碼。","evidence_level":"情境試算；前份目標價由前份年化報酬回推，前份倍數未留存","settle_metric":"收盤價對 175 美元","if_then":["若收在 175 美元以下，重跑判斷並分批反買首批","若收在 175 美元以上，不追"]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空，原文未留存。","side_b":"FY2027 任一季，非 AI 客戶營收年增掉回 20% 以下。","ruling":"前份未留存，無法比較舊門檻。本次選非 AI 客戶年增，因為這個群組少 10 個百分點成長，兩年的累積衝擊就超過最大客戶完全流失。","evidence_level":"2026-11-04 法說會與投資人日 AI 原生占比","settle_metric":"非 AI 客戶營收年增","if_then":["若掉回 20% 以下，清倉","若維持 high 20s，門檻不動"]},{"axis":"清倉與減碼門檻變動","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空，原文未留存。","side_b":"清倉：非 AI 客戶年增掉回 20% 以下。減碼：排除最大客戶年增連兩季低於 25%、cRPO 年增連兩季低於 25%、毛留存跌出 90% 中後段。","ruling":"前份未留存，本次重建，門檻取自 Bear 路徑與 Q3 現況的距離。","evidence_level":"2026-11-04 法說會","settle_metric":"上述四項指標","if_then":["任一減碼條件成立，減碼一半","清倉條件成立，清倉"]}],"triggers":[{"n":1,"text":"股價收盤跌破 175 美元，重跑判斷後分批反買首批。","type":"估值rearm","maps_to":"H1","metric":"收盤價","threshold":"≤175 美元","action":"重跑判斷，通過後分批反買首批","source_freq":"每日收盤","date":null},{"n":2,"text":"非 AI 客戶營收年增維持 25% 以上。","type":"假設驗證","maps_to":"H1","metric":"非 AI 客戶營收年增","threshold":"連兩季降到 mid-20s 以下","action":"停止加碼","source_freq":"每季法說會","date":"2027-02"},{"n":3,"text":"非 AI 客戶年增掉回 20% 以下，論點失效。","type":"Single Thing","maps_to":"H1","metric":"非 AI 客戶營收年增","threshold":"<20%","action":"清倉","source_freq":"每季法說會","date":null},{"n":4,"text":"最大客戶下次續約承諾低於本次或不續約。","type":"風險","maps_to":"R1","metric":"最大客戶續約承諾","threshold":"低於本次九位數承諾或不續約","action":"減碼一半","source_freq":"法說會與 10-K，到期日公司未揭露","date":null,"evidence_refs":["customer_second_source#0","customer_concentration_credit#0","end_markets#2"]},{"n":5,"text":"提前續約折價擴散，cRPO 或毛利率走弱。","type":"風險","maps_to":"R2","metric":"cRPO 年增、non-GAAP 毛利率","threshold":"cRPO 連兩季 <25%，或毛利率連兩季 <78%","action":"減碼一半並停止加碼","source_freq":"每季法說會","date":null},{"n":6,"text":"排除最大客戶的成長跌破 25%，加速敘事不成立。","type":"減碼","maps_to":"H1","metric":"排除最大客戶營收年增","threshold":"連兩季 <25%","action":"減碼一半","source_freq":"每季法說會","date":null},{"n":7,"text":"持有首批後，FY2027 指引確認基本面才加第二批。","type":"加碼","maps_to":"H1","metric":"FY2027 指引隱含的排除最大客戶年增","threshold":"≥25%，且毛留存維持 90% 中後段","action":"分批反買第二批","source_freq":"2027 年 2 月財報","date":"2027-02"},{"n":8,"text":"第四季財報與 FY2027 指引出爐後全面複審。","type":"複審日期","maps_to":"H1","metric":"Base EPS、門檻價","threshold":"按新指引重算 8% 年化對應價","action":"依重算價更新門檻，股價在門檻內分批反買，門檻外不追","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"非 AI 客戶營收年增","bear_threshold":"掉回 20% 以下，清倉","window":"FY2027 任一季","source":"每季法說會 CFO 準備稿","last_status":"ok"},{"metric":"排除最大客戶營收年增","bear_threshold":"連兩季低於 25%，減碼","window":"2027 年 Q1 至 Q3","source":"每季法說會與指引說明","last_status":"ok"},{"metric":"毛營收留存率","bear_threshold":"跌出 90% 中後段，減碼","window":"連兩季","source":"每季法說會 CFO 準備稿","last_status":"ok"},{"metric":"cRPO 年增","bear_threshold":"連兩季低於 25%，減碼","window":"2027 年各季","source":"每季法說會 CFO 準備稿","last_status":"warning"},{"metric":"TTM 股權激勵占營收","bear_threshold":"FY2027 全年仍高於 19%，不加碼","window":"FY2027","source":"每季 8-K 與 10-Q；Q3 數字事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價收盤回落至175美元以下（Base五年年化約8%）才重跑判斷分批；FY2027指引後按Base EPS同比調整","exec_line":"觸發後重跑判斷再分兩批：首批在 175 美元以下，第二批等 FY2027 指引確認排除最大客戶年增仍在 25% 以上。未觸發前不追。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"股價收盤在 175 美元以下，Base 五年年化才到約 8%；2027 年 2 月 FY2027 指引若改變 Base EPS，門檻同比例調整。","qc48_result":"pass","qc48_note":"Bull 的盈餘路徑以總營收成長率和利益率推算，沒有分部的量價拆解。runway 的滲透率推導依賴公司自己的分母，換成 Gartner 口徑就站不住。兩點都有缺口，但沒有查到足以否定的反證，整體屬於證據不完整，不是被推翻。"},"thesis":{"H":[{"id":"H1","text":"非 AI 客戶維持高成長，證明加速不是雲端優化結束後的短暫回補，而是 AI 帶動軟體量與平台擴張。","2y":"FY2027 各季非 AI 客戶營收年增維持 25% 以上。","5y":null,"10y":null,"threshold":"非 AI 客戶營收年增 ≥25%（現況 high 20s）","source":"每季法說會 CFO 準備稿，公司只給區間","drift_rule":"公司只給區間，依用語判斷：連兩季降到 mid-20s 以下為削弱，連三季降到 low-20s 以下為反轉。"},{"id":"H2","text":"規模與研發效率讓 non-GAAP 利益率上升，同時股權激勵占營收下降，股東實得利潤跟著增加。","2y":null,"5y":"FY2031 non-GAAP 營業利益率約 29.5%，股權激勵占營收 13% 以下。","10y":null,"threshold":"FY2029 前 non-GAAP 營業利益率 ≥28%，且 TTM 股權激勵占營收 ≤15%（2026 Q2 單季 19.6%）","source":"每季 8-K 與 10-Q","drift_rule":"TTM 數字連四季偏離 Base 路徑 5% 以上為削弱，連六季偏離 10% 以上為反轉。"},{"id":"H3","text":"平台滲透與份額繼續上升，資安與 AI 監控在核心監控放緩時接上第二條成長曲線。","2y":null,"5y":null,"10y":"2036 年前公司自述全球觀測份額達 25–30%，資安成為占比兩位數的產品線。","threshold":"使用六項以上產品的客戶比率 2029 年 ≥55%（現況 41%），毛留存維持 90% 中後段","source":"每季法說會 CEO 準備稿、投資人日","drift_rule":"跨兩個年度未達路徑為削弱，跨三個年度未達為反轉。"}],"R":[{"id":"R1","text":"最大客戶降用量或到期不續約，頂端 AI 原生客戶跟進。公司兩季都不說合約期限與降量原因；外界指為 OpenAI，屬媒體推測。SaaStr 把該客群 Q1 的貢獻寫成客群成長，與 10-Q 轉述的貢獻點數口徑不同，以後者為準。","h_ref":"H1","clock":"🔥","threshold":"下次續約承諾金額低於本次或不續約","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_second_source#4","customer_concentration_credit#0","customer_concentration_credit#5","end_markets#2"]},{"id":"R2","text":"提前續約的價格折讓從個案變成常態，大客戶用更高承諾換更低單價，營收增速追不上用量增速。","h_ref":"H2","clock":"🔥","threshold":"cRPO 年增連兩季低於 25%，或 non-GAAP 毛利率連兩季低於 78%","evidence_refs":["end_markets#3"]},{"id":"R3","text":"平台綑綁與低價替代同時壓縮預算：資安與資料平台收購監控廠商，超過 40 家廠商競爭，總持有成本成為標準問題，Grafana ARR 已過 4 億美元。","h_ref":"H3","clock":"🐢","threshold":"Ramp 採用率由 34% 跌破 30%，或毛留存跌出 90% 中後段","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#1","supply_demand_durability#7","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"股權激勵不降，帳面成長轉不成每股價值。","h_ref":"H2","clock":"🐢","threshold":"FY2027 全年股權激勵占營收仍高於 19%，或淨稀釋高於 3%"},{"id":"R5","text":"AI 自動化與貼近推論成本的定價壓縮單位收入，產品採用率上升卻換不到淨留存。","h_ref":"H3","clock":"🐢","threshold":"AI 產品客戶比率持續上升，但淨留存跌破 115%"}],"single_thing":{"description":"FY2027 任一季，非 AI 客戶營收年增掉回 20% 以下。","why_fatal":"非 AI 客戶是營收主體（AI 原生客群 2025 年底約占 11%，最新占比事實表未涵蓋）。這個群組少 10 個百分點成長，一年衝擊接近最大客戶完全歸零，兩年就超過，而且逐年累積，Base 的 EPS 複利約 18.6% 也站不住。","if_happens":"Base 改用 Bear 路徑，終端倍數降到 28 倍，五年目標約 83 美元；持股清倉。","how_monitor":"每季法說會 CFO 準備稿的非 AI 客戶年增區間，下一次在 2027 年 2 月。","probability":"20%（12–24 個月）。一年前仍約 20%，已連五季加速，掉回去等於吐回這段加速。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":60.08,"peg_fy2":2.81,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":2.55,"FY2027E":2.98,"FY2028E":3.76},"fy_end_month":12,"eps_basis":"non-GAAP 稀釋 EPS，Koyfin 2026-11-07 快照。FY2025A 的 non-GAAP EPS 事實表未涵蓋，留空；財報表的 GAAP 0.31 口徑不同，不拿來當基期。FY2026E 2.55 低於 2026-11-04 全年指引 2.73–2.75，FY2027E、FY2028E 可能同樣未更新。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"AWS re:Invent 期間的產品發表","impact":"低","watch":"Bits AI 與 Agent Observability 的收費數字是否揭露"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 FY2027 指引","impact":"高","watch":"最大客戶的估算方式、排除最大客戶年增、非 AI 客戶年增、cRPO"},{"date":"2027-Q3","date_precision":"quarter","type":"other","event":"最大客戶可能的下次續約（公司未揭露到期日，僅依分析師假設的一年期推算）","impact":"高","watch":"承諾金額是否低於本次、是否轉向自建"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=-10.55, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 的盈餘路徑以總營收成長率和利益率推算，沒有分部的量價拆解。runway 的滲透率推導依賴公司自己的分母，換成 Gartner 口徑就站不住。兩點都有缺口，但沒有查到足以否定的反證，整體屬於證據不完整，不是被推翻。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價收盤在 175 美元以下，Base 五年年化才到約 8%；2027 年 2 月 FY2027 指引若改變 Base EPS，門檻同比例調整。'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
