你是 DD 管線 v20 的判斷層閘（gate），標的 MTSI（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（33 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝424.8 USD M｜期間與口徑：Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：MACOM Q4 FY26 earnings release, 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001493594/000149359426000041/ex99_1earningsreleaseq4fy26.htm（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：未查得
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝38.2 % (營業利益 162.3 USD M)｜期間與口徑：Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：同上 8-K Ex.99.1 adjusted operating income 調節表（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：未查得
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝31.6 % (營業利益 134.2 USD M)｜期間與口徑：Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：同上 8-K Ex.99.1（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：未查得
- `f_kpi4_adjusted_eps_q4_non_gaap`（q1_business）｜Adjusted EPS (Q4, non-GAAP)＝2.09 USD/股｜期間與口徑：Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：同上 8-K Ex.99.1（GAAP EPS 1.78；adjusted gross margin 61.3%、GAAP 59.9%）（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：未查得
- `f_kpi5_guidance_q1_fy2027_reven`（q1_business）｜Guidance: Q1 FY2027 revenue＝450–460 USD M（季末 2027-01-01）｜期間與口徑：Q4 FY2026 財報（公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：同上 8-K Ex.99.1 outlook（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026 財報（公告於 2026-11-05））
  - 註記：未查得
- `f_kpi6_guidance_q1_fy2027_adjus`（q1_business）｜Guidance: Q1 FY2027 adjusted gross margin / adjusted EPS＝62.0–63.0% / 2.21–2.29 % / USD｜期間與口徑：Q4 FY2026 財報（公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：同上 8-K Ex.99.1（假設 non-GAAP 稅率 6%、稀釋股數 79.0M）（numbers.latest_quarter_kpis.items[6]，as_of Q4 FY2026 財報（公告於 2026-11-05））
  - 註記：未查得
- `f_peer_mtsi_gross_margin_pct`（q2_moat）｜MTSI 毛利率＝57.13 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTSI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_swks_gross_margin_pct`（q2_moat）｜SWKS 毛利率＝40.75 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SWKS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_qrvo_gross_margin_pct`（q2_moat）｜QRVO 毛利率＝48.22 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QRVO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_adi_gross_margin_pct`（q2_moat）｜ADI 毛利率＝65.8 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_cohr_gross_margin_pct`（q2_moat）｜COHR 毛利率＝38.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mtsi_operating_margin_pct`（q2_moat）｜MTSI 營業利益率＝18.97 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTSI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝1939.58 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝2283.65 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝8.54 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝10.11 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝12.48 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_kpi3_stock_based_compensation`（q1_business）｜Stock-based compensation（調節表列示）＝23.9 USD M（占營收約 5.6%；占 non-GAAP 營業利益約 14.7%）｜期間與口徑：Q4 FY2026（季末 2026-10-02，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：同上 8-K Ex.99.1 營業利益調節表；占比為本 agent 以 23.9/424.8、23.9/162.3 計算（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-10-02，公告於 2026-11-05））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-385.47 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 406.94、現金 792.41（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝76.37 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_mtsi_fcf_margin_pct`（q2_moat）｜MTSI FCF 利潤率＝9.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTSI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝210.98 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝24.7 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 8.54，分子＝快照價 210.98｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝48.95 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／2 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝12.14 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝11.85 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝8.11 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-41.37 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝38.03｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝262.51 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝194.8 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝125.25 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝54.99 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 5.51 → 8.54（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出主要競爭者（ADI、Broadcom、Credo、Marvell、MaxLinear、Microchip、NXP、Qorvo、Semtech、Skyworks、Sumitomo），並提到中國公司競爭加劇；亦點出客戶自研與低成本矽製程大廠為潛在替代
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 稱主要與客戶內部設計資源及其他高性能類比半導體供應商競爭，預期有新進入者，且未來有採低成本矽製程之大量製造商的替代技術競爭
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2025-11-14）｜affects：moat_trend、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2025 10-K：無單一直接客戶占營收 10% 以上，前十大直接與經銷客戶合計 56.7%；採購為 PO 制無最低採購量，主要客戶可能無預警終止、減少訂單、轉向競爭對手或自行開發產品（in-house）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：前十大客戶占營收 FY2025 57%、FY2024 56%、FY2023 48%，集中度上升；Customer A 12%、B 11%，應收帳款三家各11%
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：採購以訂單為基礎、無最低採購量，主要客戶可無預警終止；中國占營收28.4%
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：LightCounting：需求超過供給 30%，短缺預計 2026 年底消退，2027-2031 市場成長趨緩，與雲端 capex 週期高度相關。
  - 來源：LightCounting LightTrends Newsletter April 2026（as_of 2026-04-01）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2025 對中國銷售占 28.4%、亞太 11.5%；10-K 提示美國 BIS 出口管制（2022、2023 年新增）為風險。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 中國占營收 28.4%、亞太 11.5%，美國以外銷售占 56.3%；10-K 列示關稅、出口許可與貿易限制為風險，並稱多數產品受 EAR 管制，部分需 BIS 出口許可。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 指出部分產品需出口許可、出口管制改革已造成部分國家與客戶出貨困難，並承認持續面臨合規挑戰。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：MACOM 10-K 披露：特定製程晶圓通常僅經單一代工廠取得，並倚賴該廠供應該製程全部晶圓；另述可能對各類材料使用單一供應來源。
  - 來源：MACOM 10-K FY2025 (SEC)（as_of 2025-10-03）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：MACOM 10-K 披露：供應商若原料庫存不足、倒閉、產能受限或暫時停工，公司面臨供應鏈中斷風險；緩解方式為多源認證、改設計、增加庫存。
  - 來源：MACOM 10-K FY2025 (SEC)（as_of 2025-10-03）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：10-Q FY2026：砷化鎵等關鍵材料可能因地緣政治與出口管制而短缺；自有廠位於Lowell、Ann Arbor、RTP、法國Limeil-Brévannes
  - 來源：MACOM 10-Q (quarter ended 2026-01-02)（as_of 2026-02-01）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：公司 FY2025 10-K 自述：預期未來會有採用替代技術的公司（含使用低成本矽製程的大量製造商）帶來更多競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2025-11-14）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：未來競爭可能來自新替代技術、更高整合度的 IC 廠商，且客戶與供應商可能自行開發競品或取代本公司產品。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：搜尋摘要：有評論文章指出，若超大規模業者透過矽光子/CPO 把光學子系統內製，MACOM 的離散光電二極體、TIA、DFB 雷射市場可能縮小；該風險在財報會議未被量化，且未找到 CPO 已減少其 TIA/驅動器出貨量的硬數據。CPO 大量部署預估 2027-2028。
  - 來源：WebSearch 摘要（聚合多來源，其中看空論述為意見文章）（as_of 2026-05-01）｜affects：moat_trend、decision_inputs.bear、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":607.5,"bear_5y_price":127.5,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":61.6,"ev5y_pct":56.5,"irr_base_pct":10.1,"asym_ratio":3.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":8.54,"pe":24.7,"basis":"FY1（FY2027E）共識 EPS 8.54 美元，與終端倍數同為當年度 EPS 口徑；共識偏舊，修正後約 22 倍"},"eps":{"bull":[10.2,13.3,16.5,19.5,22.5],"base":[9.4,11.0,12.5,14.0,15.5],"bear":[8.6,7.5,6.8,7.6,8.5]},"pe":{"bull":27,"base":22,"bear":15},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MTSI_Q3_2026_Earnings_Call_20260806.md
- 2026-08-06｜CEO Stephen Daly｜guidance：FQ4 毛利率財測 60%–61%（原話："gross margin is expected to be in the range of 60% to 61%"）
- 2026-08-06｜CEO Stephen Daly｜guidance：FQ4 調整後 EPS 財測區間（原話："per share is expected to be between $1.97 and $2.03"）
- 2026-08-06｜CEO Stephen Daly｜guidance：FQ4 資料中心季增財測約 35%（原話："approximately 35% sequential growth in Data Center"）
- 2026-08-06｜CFO John Kober｜guidance：FQ4 調整後營業利益率預期約 37%（原話："approximately 37% for the fourth fiscal quarter."）
- 2026-08-06｜CFO John Kober｜guidance：FQ4 營運現金流預期超過 1 億美元（原話："operations will be in excess of $100 million."）
- 2026-08-06｜CFO John Kober｜guidance：FY26 CapEx 預估 6,000–6,500 萬美元（原話："CapEx to be in the range of $60 million to $65 million."）
- 2026-08-06｜CEO Stephen Daly｜guidance：FQ4 財測中點年化後 FY27 公司成長約 27–28%（原話："20s, 27%, 28% as a company."）
- 2026-08-06｜CEO Stephen Daly｜guidance：同樣算法下資料中心 FY27 約 50% 成長，管理層稱為 base case（原話："that number then trends to 50% year-over-year growth."）
- 2026-08-06｜CEO Stephen Daly｜guidance：電信今年預期雙位數成長，明年類似或更好（原話："similar performance or better performance next year."）
- 2026-08-06｜CFO John Kober｜guidance：稅率預告：FY27 逐步由 3% 升至個位數中段（原話："we anticipate our adjusted tax rate will begin to rise"）
- 2026-08-06｜CFO John Kober｜margin：Q3 調整後毛利 2.042 億、毛利率 59.7%（原話："was $204.2 million or 59.7% of revenue"）
- 2026-08-06｜CFO John Kober｜margin：管理層預期毛利率於 FY26 餘季與 FY27 逐季改善（原話："ongoing quarterly sequential gross margin improvements"）
- 2026-08-06｜CFO John Kober｜margin：CFO 對 FY27 毛利率改善幅度給出每季 25–50bp 的口徑(較 FY26 的速度放緩)（原話："25 basis points to 50 basis points per quarter"）
- 2026-08-06｜CEO Stephen Daly｜margin：FY27 營業利益率目標為突破 40%（原話："or breach the 40% operating margin level."）
- 2026-08-06｜CEO Stephen Daly｜margin：投入成本上漲(人工、電力、原料),不一定能轉嫁客戶（原話："We try to pass those costs on to customers"）
- 2026-08-06｜CEO Stephen Daly｜margin：管理層稱近一年通膨上升期間毛利率仍擴張（原話："we've been able to expand our gross margins"）
- 2026-08-06｜CEO Stephen Daly｜margin：產品組合：PD/雷射晶片小，少量晶圓可產出大量元件;管理層稱組合效應將在 FY27 改善（原話："These PD laser devices, as an example, are quite small."）
- 2026-08-06｜CFO John Kober｜margin：CFO 預計 OpEx 每季增加數百萬美元（原話："adding a couple, $3 million"）
- 2026-08-06｜CEO Stephen Daly｜product：Q3 資料中心季增約 40%（原話："Data Center increased approximately 40% sequentially"）
- 2026-08-06｜CEO Stephen Daly｜product：200G PD 已量產放量，400G PD 獲正面回饋（原話："200G photodetectors, which are ramping in volume production"）
- 2026-08-06｜CEO Stephen Daly｜product：400G PD 已在約一打客戶手上（原話："perhaps a dozen customers"）
- 2026-08-06｜CEO Stephen Daly｜product：75mW CW 雷射仍在認證，尚未宣告成功（原話："while we cannot declare success yet"）
- 2026-08-06｜CEO Stephen Daly｜product：CW 雷射 HTOL 測試後半段，管理層稱數據優異（原話："we are building our confidence that we have a winner"）
- 2026-08-06｜CEO Stephen Daly｜commitment：CW 雷射預計最早 2027 年底開始量產(準備小額 CapEx 與廠房空間)（原話："a potential start to production in late calendar 2027"）
- 2026-08-06｜CEO Stephen Daly｜product：Q&A 中 CW 雷射量產時點以 2028 表述（原話："If we're able to bring a CW laser into production in 2028"）
- 2026-08-06｜CEO Stephen Daly｜product：25G DFB 雷射因磷化銦 DFB 全產業短缺而需求增加（原話："Customers are coming to us with urgency"）
- 2026-08-06｜CEO Stephen Daly｜product：NPO 有 10–20 個開發專案，營收預期 2028 年起;部分專案不會量產（原話："somewhere between 10 and 20 active NPO development projects"）
- 2026-08-06｜CEO Stephen Daly｜product：NPO 專案部分不會進入量產（原話："Some of these programs will never make it to production"）
- 2026-08-06｜CEO Stephen Daly｜product：資料中心定位為晶片供應商，不做光引擎/模組（原話："we are not going to be building engines and supplying"）
- 2026-08-06｜CEO Stephen Daly｜product：一家大型超大規模業者將部署線性等化器 cable 方案，預期參與（原話："hyperscaler that is looking to deploy that type of"）
- 2026-08-06｜CEO Stephen Daly｜product：公司目前不推被動銅纜方案（原話："do not promote passive copper solutions"）
- 2026-08-06｜CEO Stephen Daly｜product：歐洲防務營收預期 2028 年起成長（原話："sometime in '28, that Defense number will start to grow."）
- 2026-08-06｜CEO Stephen Daly｜product：MESC 預期取得該廠史上最大訂單之一(英國防務客戶)（原話："one of the largest orders in MESC's history"）
- 2026-08-06｜CEO Stephen Daly｜product：衛星光通訊平台新案;管理層稱確立 MACOM 為策略夥伴（原話："This new award establishes MACOM as a strategic"）
- 2026-08-06｜CEO Stephen Daly｜product：車用業務今年預期營收翻倍（原話："is expected to double its"）
- 2026-08-06｜CEO Stephen Daly｜customer：Q3 book-to-bill 創紀錄 1.6:1（原話："Our Q3 book-to-bill ratio was a record 1.6:1"）
- 2026-08-06｜CEO Stephen Daly｜customer：年收入逾 1,000 萬美元的客戶由兩年前約 8 家增至逾 20 家（原話："we have over 20 customers above $10 million"）
- 2026-08-06｜CEO Stephen Daly｜customer：前 10 大終端客戶占比低於 40%（原話："still represent less than 40% of our total revenue"）
- 2026-08-06｜CEO Stephen Daly｜customer：資料中心成長來自美國超大規模業者與企業/運算 OEM（原話："driven by U.S. hyperscalers as well as the enterprise"）
- 2026-08-06｜CEO Stephen Daly｜customer：資料中心年成長：2024 35%、2025 48%、今年約 74%（原話："we're trending towards about 74% this year"）
- 2026-08-06｜CEO Stephen Daly｜customer：防務業務去年成長 19%,今年預期約 25%（原話："And this year, we expect it to grow by approximately 25%."）
- 2026-08-06｜CEO Stephen Daly｜customer：電信中有線纜基礎建設約 +40%、都會長程 +50% 以上（原話："year-over-year will be around 40% growth"）
- 2026-08-06｜CEO Stephen Daly｜competition：兩家 5G 競爭對手退出，公司預期取得部分市占（原話："We would expect to pick up some of that market share."）
- 2026-08-06｜CEO Stephen Daly｜competition：5G MIMO 目前業務很少，管理層稱有機會使 5G 營收翻倍以上（原話："perhaps more than double our 5G revenue"）
- 2026-08-06｜CEO Stephen Daly｜competition：與部分收發模組廠在某些業務領域互為競爭者（原話："we actually compete with."）
- 2026-08-06｜CEO Stephen Daly｜competition：Wolfspeed 關閉 Durham 廠，MACOM 低價取得設備（原話："equipment at pennies on the dollar"）
- 2026-08-06｜CEO Stephen Daly｜risk：針對中國模組廠禁令傳聞：預期客戶組合移轉而非流失（原話："I think we would see a customer mix shift"）
- 2026-08-06｜CEO Stephen Daly｜risk：對禁令傳聞回應為照常營運（原話："we're keeping our head down and it's business as usual"）
- 2026-08-06｜CEO Stephen Daly｜risk：中國無製造據點，約 85 名員工（原話："We have no manufacturing today in China."）
- 2026-08-06｜CEO Stephen Daly｜risk：產能利用率上升使交期拉長（原話："quoting longer lead times for products that are manufactured"）
- 2026-08-06｜CEO Stephen Daly｜risk：CHIPS 協議條款中有對公司『無法接受』者，談判中（原話："are sort of nonstarters for us"）
- 2026-08-06｜CEO Stephen Daly｜capital_allocation：重新向 CHIPS Office 提交改寫後的計畫（原話："we have resubmitted it to The CHIPS Office"）
- 2026-08-06｜CEO Stephen Daly｜capital_allocation：FY27 CapEx 預期與今年相近約 6,000 萬美元，含雷射量產基建（原話："sort of in that $60 million range"）
- 2026-08-06｜CFO John Kober｜capital_allocation：新增產能 CapEx 通常一年內上線（原話："installed and online in less than 1 year"）
- 2026-08-06｜CFO John Kober｜capital_allocation：投資 IQE 6,100 萬美元，說明為強化供應鏈韌性（原話："the $61 million investment we made in IQE"）
- 2026-08-06｜CFO John Kober｜capital_allocation：淨現金約 3.225 億美元（原話："approximately $322.5 million as of July 3"）
- 2026-08-06｜CEO Stephen Daly｜capital_allocation：現金哲學（原話："our philosophy is you can never have enough cash"）
- 2026-08-06｜CFO John Kober｜capital_allocation：CFO 列出現金用途：還債、內部投資、tuck-in 併購（原話："We've done a number of tuck-in type acquisitions"）
- 2026-08-06｜CEO Stephen Daly｜commitment：R&D 費用自 2023 年約 1.32 億增至今年近 2.5 億（原話："we've doubled the amount of R&D spending"）
- 2026-08-06｜CEO Stephen Daly｜commitment：將持續擴編設計中心以追逐 SAM（原話："we will continue to build-out and staff our design"）
- 2026-08-06｜CEO Stephen Daly｜commitment：擬於下季(財年末)提供 FY27 base case 並隨產能與設計案量產上/下調（原話："modulate up or down our Data Center business"）
- 2026-08-06｜CEO Stephen Daly｜commitment：SAM 上修：2027 約 150 億(I&D 60、資料中心 60、電信 30),較 26 年增 20–30%（原話："that's up about 20% to 30% from '26 to '27."）
- 2026-08-06｜CEO Stephen Daly｜commitment：承認對市場數字做了重設(上修 I&D 與資料中心)（原話："a bit of a reset on some of our market-based numbers"）

### 問答異常語氣（迴避／改口／保留）
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Tom O'Malley:FY27 成長軌跡｜答法：稱現在談 FY27 太早，但改以 FQ4 財測中點年化給出約 27–28% 與資料中心 50%,稱為 base case
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Quinn Bolton:資料中心 FY27 要再加速需要什麼｜答法：延後至下季回答，稱『not sure I'm really completely answering your question』
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Karl Ackerman:資料通訊是否會成為最大機會｜答法：先稱對方誤解其說法，改以 I&D 與資料中心 SAM 各約 60 億回答
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Tim Savageaux:雷射/偵測器內容是否大於 TIA/驅動｜答法：不同意前提，表示從未公開比較兩者 SAM,不給數字
- MTSI_Q3_2026_Earnings_Call_20260806.md｜問：Tim Savageaux:PD 是否已貢獻數千萬美元｜答法：稱不想拆分產品線營收(競爭考量),僅說『more meaningful』且將顯著成長

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 2 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B（衛星觀望·thesis 完整｜Q2 FY26 Adj EPS $1.09 beat + DC +48% FY25 至 $293M + 800G/1.6T 200G/lane photodetector 全 module maker design wins + Adj GM 58.5% 目標 60%；但 Fwd PE FY26 76x / FY27 56x 已 stretched + BB 107.9% 上突破 + 52w +127%，等回測 $290-330 或 BB 中軌 $257 區再評估）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"800G/1.6T optical migration + AI infra capex 持續推升 DC segment","columns":{"2Y 驗證點（2026-27）":"Q3-Q4 FY26 DC YoY 維持 +35-40%；FY27 DC revenue ≥ $450M（+50% from $293M FY25）","5Y 驗證點（2026-30）":"FY28-30 DC revenue ≥ $750M（從 2025 $293M ramp 2.5x）；DC 占公司營收 ≥ 50%","10Y 驗證點（2026-35）":"DC TAM 維持 $5B+ at 2030 + MTSI 維持 top-tier supplier 地位","具體數字門檻":"DC segment YoY 連 2 季 ≥ +35%（FY26 Q3-Q4）；FY27 DC ≥ $450M","信息來源":"Q2 FY26 法說會（5/7）+ Stifel / Needham research notes + 800G transceiver shipment forecasts","漂移觸發條件":"連 2 季 TTM 偏離 -10% → 削弱；連 3 季 -10% → 反轉"}},{"id":"H2","text":"Adj GM 達 60% 目標 + Adj OpM 達 30%","columns":{"2Y 驗證點（2026-27）":"FY26 Q3-Q4 Adj GM ≥ 58.5%；FY26 全年 Adj GM ≥ 59%；Adj OpM ≥ 28%","5Y 驗證點（2026-30）":"FY27-30 Adj GM 維持 60%+；Adj OpM ≥ 30%","10Y 驗證點（2026-35）":"FY28+ Adj GM 達 62%+（vertical integration 全效益兌現）","具體數字門檻":"Adj GM 連 2 季 ≥ 58.5%；Adj OpM 連 2 季 ≥ 28%","信息來源":"Q2 FY26 法說會 + IR guidance update","漂移觸發條件":"Adj GM 連 2 季環比 -1pp → 削弱；連 4 季環比 -1pp → 反轉"}},{"id":"H3","text":"200G/lane photodetector design-in 領先優勢維持，pricing power 不被侵蝕","columns":{"2Y 驗證點（2026-27）":"FY27 前無第二家 200G/lane photodetector 商業量產","5Y 驗證點（2026-30）":"2028-2030 仍維持 top-tier 200G/lane 供應商地位 + 400G/lane R&D 領先","10Y 驗證點（2026-35）":"2030+ 1.6T/3.2T+ photonic IC 系列產品線維持","具體數字門檻":"無 Coherent / Lumentum / Sumitomo 200G/lane 量產 announcements；季度 design-win 數量持續增加","信息來源":"analyst sell-side reports + Q4 法說會 competitive review","漂移觸發條件":"第二家 200G/lane 量產 → 削弱；3 家以上量產 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AI capex 2027 H1 air pocket → DC ramp 推遲 + 800G/1.6T cycle 延後 6-12 個月","columns":{"對應假設":"H1","時間尺度標記":"⚡ 短期（1-2 季可觸發）","監測指標":"hyperscaler capex YoY；NVIDIA Blackwell shipment；800G+ transceiver shipment","警戒閾值":"連 2 季 hyperscaler capex YoY &lt; 15% → 削弱"}},{"id":"R2","text":"200G/lane photodetector competitor entry → MTSI pricing power 受壓","columns":{"對應假設":"H2, H3","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"Coherent / Lumentum / Sumitomo competitive announcements；MTSI Adj GM 變化","警戒閾值":"連 2 季 Adj GM 環比 -1pp + 競爭者量產 announcement → 削弱"}},{"id":"R3","text":"大型 M&A 失敗 / Wolfspeed integration cost 持續拖累 GAAP earnings","columns":{"對應假設":"H2","時間尺度標記":"🐢 長期（2+ 年慢變數）","監測指標":"GAAP vs Adj EPS gap；one-time charge frequency；M&A track record","警戒閾值":"GAAP NI 連 3 年不及 Adj NI 60% → 質疑 Adj EPS 信任度"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":385.98,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MTSI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"MACOM Technology Solutions Holdings, Inc."},"oneliner":"MACOM 基本面加速，股價半年卻跌 41%：FY27 資料中心 base case 年增 80%，營益率站上 40%，前瞻本益比 24.7 倍但分母偏舊；爭點是 2028 訂單會不會回吐，Base 年化約 10%，宜分批小量進場，不重押。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺雲端光互連、國防射頻與衛星通訊客戶的錢，錢卡在高速類比與化合物半導體這一節；第四季資料中心占營收 44%、工業國防 39%、電信 17%。","reasoning":"FY26 營收 13.3 億美元、年增 37%，調整後 EPS 5.60 美元、年增 61%。第四季營收 4.248 億美元，調整後毛利率 61.3%、營益率 38.2%，GAAP 營益率 31.6%。FY27 第一季指引營收 4.5–4.6 億美元、調整後毛利率 62–63%、EPS 2.21–2.29 美元。收錢方式是賣標準與客製晶片、模組，外加晶圓代工服務，法國廠約一半是代工。訂單以採購單為主、沒有最低採購量，靠設計導入與長交期維持能見度，第四季當季接單當季出貨僅占營收 7%。經銷商占 FY25 營收 32.3%。單點依賴有兩處：特定製程晶圓通常只有一家代工來源，資料中心的 SiGe 大多委外；需求面則繫於超大規模業者的資本支出。反例：管理層稱三個市場彼此不相關，但 FY26 三個市場同步成長，還沒有下行期可以驗證這個說法。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi4_adjusted_eps_q4_non_gaap","f_kpi5_guidance_q1_fy2027_reven","f_kpi6_guidance_q1_fy2027_adjus"],"verdict_values":{"revenue_quality":"採購單制、無最低採購量，法律上不具約束力；當季接單當季出貨僅 7%，代表短期能見度高，但 2028 之後沒有合約保障。","unit_econ_note":"毛利擴張來自營收放大後的稼動率、新品組合與良率。公司不揭露分部毛利，單價與量的拆分事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"三大終端市場的類比與化合物半導體公司，擁有自有晶圓廠；FY23 營收僅年減 4% 仍維持 59.5% 毛利率，但資料中心占比快速上升，週期性正在抬高。"},"industry":{"clock_phase":"II","sd_verdict_source":"擴張期依據：FY26 訂單出貨比 1.5、第四季 1.4，交期拉長，SiGe 代工開始要求確定承諾。供需判斷為週期性將反轉，時間點在 2027 之後：Lumentum 稱磷化銦雷射緊到 2027，但 LightCounting 指光模組需求與雲端資本支出週期高度相關，2027–2031 成長趨緩。","bargaining":{"up":"SiGe 代工（Tower、ST、GlobalFoundries）開始要求確定承諾，議價權往代工廠移動；特定製程通常單一代工來源。","down":"管理層預期超大規模業者會把份額分給多家供應商；FY25 前十大直接與經銷客戶占 56.7%，終端前十大低於 40%（2026-08-06 法說，執行長）。","geo":"中國占 FY25 營收 28.4%，多數產品受出口管制；美國自有晶圓廠在國防與本土 5G 構成優勢。"},"profit_pool_dir":"利潤池往光互連遷移，公司搭上順風；若全整合 CMOS 在 NPO 勝出，利潤會流向大型整合廠。各環節營業利益占比事實表未涵蓋。","tam_table":[{"item":"2027 SAM 合計","value":"約 150 億美元（管理層估計，2026-11-05 法說）"},{"item":"SAM 結構","value":"工業國防 60 億、資料中心 60 億、電信 30 億美元（2026-08-06 法說，執行長）"},{"item":"SAM 年增","value":"2026 到 2027 約 20–30%；管理層承認對市場數字做過重設"},{"item":"隱含滲透率","value":"FY27 共識營收 19.4 億 ÷ 150 億，約 13%"},{"item":"資料中心成長","value":"2024 年 +35%、2025 年 +48%、FY26 +74%、FY27 base case +80%"},{"item":"營業利益池占比 5 年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向 →：執行力在擴大，定價力只算穩定，矽整合與新進者的威脅抵銷了製程廣度的優勢，等級 B。","reasoning":"機制是化合物半導體製程廣度加上設計導入後的重新認證成本。TTM GAAP 毛利率 57.1%，高於 SWKS 40.8%、QRVO 48.2%、COHR 38.2%，低於 ADI 65.8%；研發密度 23.2% 為同業最高，代表優勢要靠持續投入維持。第四季財報對 2026-08-06 指引全數達標或超過：營收 4.248 億美元落在 4.15–4.25 億上緣，EPS 2.09 美元高於 1.97–2.03，毛利率 61.3% 高於 60–61%。定價力打 7 分的原因是 GAAP 毛利率仍低於 FY22 的 60.2%，尚未證明結構性突破，且現在是短缺期，轉嫁成本比平時容易。對最強同業的 ROIC 差距事實表未涵蓋，改用毛利率比較。反例：若 FY27 毛利率真的走到中段 60% 並維持到短缺結束，應上修為擴大。","fact_refs":["f_peer_mtsi_gross_margin_pct","f_peer_swks_gross_margin_pct","f_peer_qrvo_gross_margin_pct","f_peer_adi_gross_margin_pct","f_peer_cohr_gross_margin_pct","f_peer_mtsi_operating_margin_pct","f_kpi6_guidance_q1_fy2027_adjus"],"verdict_values":{"moat":{"mechanism":"化合物半導體製程廣度（GaN、InP、GaAs）與 SiGe 高速類比設計，加上設計導入後的重新認證成本；美國自有晶圓廠在國防與本土供應具稀缺性。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：FY26 調整後營益率升 660 基點至 32%，第四季各項指引達標或超過。定價面穩定：第一季毛利率指引 62–63% 與管理層稱成本大致可轉嫁，但 TTM GAAP 毛利率 57.1% 仍低於 FY22 的 60.2%，且發生在短缺期。分析師在 2026-11-05 法說點名 Astera Labs 跨入 TIA 與驅動器，管理層也承認全整合 CMOS 不是公司的領域。","competitor_notes":[{"name":"SWKS","strategy_note":"手機射頻為主，毛利率 40.8%，與公司高階非手機定位重疊有限。"},{"name":"QRVO","strategy_note":"毛利率 48.2%，國防與基礎建設射頻直接競爭，獲利能力低於公司最新一季水準。"},{"name":"ADI","strategy_note":"毛利率 65.8%、營益率 35.7%，規模與產品廣度最強，是公司中段 60% 毛利率目標的標竿。"},{"name":"COHR","strategy_note":"毛利率 38.2%，光模組垂直整合廠，既是客戶也可能是競爭者；FCF 利潤率 −23.3% 反映重資本投入。"},{"name":"Marvell／Broadcom","strategy_note":"10-K 列名競爭者，擁有全整合方案，是 NPO 世代對公司最大的架構威脅。"}],"peer_na_reason":"事實表同業資料只有毛利率、營益率、FCF 利潤率與研發密度，沒有 ROIC，故改用利潤率比較。","threats":[{"level":"🔴","text":"矽整合、CPO 與 NPO：若全整合 CMOS 勝出，分離式 TIA、驅動器與光偵測器的市場會縮小；目前沒有出貨量受損的硬數據，大量部署預估 2027–2028。","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"]},{"level":"🟡","text":"既有對手與新進者搶 TIA 與驅動器份額，10-K 另提中國公司競爭加劇。","p":"40%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"客戶內製或轉單；採購單制下沒有違約成本，目前查無具體案例。","p":"25%","evidence_refs":["customer_second_source#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（暫判，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是光模組廠，決策者是超大規模業者的架構與採購團隊，付款來源是雲端資本支出。需求急迫，持久性未證：FY26 訂單出貨比 1.5，但 LightCounting 指需求與資本支出週期高度相關。國防端有美歐預算支撐，較持久。"},{"item":"決策層級","level":"🟡","text":"單一插槽一旦導入，重新認證成本高；但管理層預期超大規模業者會分給多家，跨世代的黏著度較弱。國防平台認證週期長，美國僅公司生產這類線性化器，黏著度明顯較高。"},{"item":"價值鏈分配","level":"🟡","text":"短缺期超額利潤主要落在雷射環節，Lumentum 稱出貨比需求低約 30%；SiGe 代工要求確定承諾，顯示上游議價權上升。各環節採購金額占比事實表未涵蓋。"},{"item":"社會容忍度","level":"🟢","text":"終端是資料中心、國防與衛星，不是民生必需品，沒有社會對漲價的上限；CHIPS 補助與出口管制屬政策依賴，已另列風險。"}],"roiic":"資料缺口：事實表無投入資本與全年營運資金變動。可見的是 FY26 調整後營業利益增加約 1.79 億美元（FY25 約 2.46 億，FY26 約 4.25 億，由 32% 營益率與年增 660 基點推得），同期資本支出 6,440 萬美元、IQE 投資 6,100 萬美元。增量報酬看起來很高，但主要來自稼動率與短缺期，不宜外推。","reinvest_rate":"資料缺口：FY26 資本支出 6,440 萬美元、第四季折舊 920 萬美元，FY27 資本支出升到 1.0–1.1 億美元；全年營運資金與收購淨額事實表未涵蓋，無法依公式計算。真正的再投資是研發，FY27 約 3 億美元。","endo_ceiling":null,"formula_note":"當期 ROIC 與內生成長上界都因投入資本缺資料而未計算；情境樹一律當作超出上界處理。"}}}},"q3_growth":{"verdict":"成長跑道寬：FY27 營收約 19.4 億美元只占管理層估的 150 億 SAM 約 13%，NPO 與 CW 雷射是下一條曲線，但都要到 2028 才有營收。","reasoning":"成長主要來自量，併購與回購貢獻趨近零。管理層 FY27 base case 為資料中心 +80%、工業國防 30% 以上、電信低雙位數，加總約 19 億美元，與共識 19.4 億一致。第一季資料中心指引約 2.16 億美元，之後每季只要季增約 4% 就能達到 +80%，FY27 風險不大。三年共識 EPS CAGR 30.6%（FY26A 5.60 到 FY29E 12.48），高於營收成長的部分來自營業槓桿，稅率由 3% 升到 6% 會抵銷一部分。若 SAM 年增 10–20%、公司維持 37% 年增，約 4–6 年滲透率到 30%。反例：SAM 是管理層定義，且已上修過；若整合方案勝出，可服務市場反而縮小。","fact_refs":["f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi5_guidance_q1_fy2027_reven"],"verdict_values":{"growth":{"driver_mix":"量為主（1.6T、200G／lane、磷化銦產能），新品組合與稼動率推升毛利；近 12 個月無併購重大項目，也沒有回購。","runway_years":5,"runway_post_y5":"🟢","endo_ceiling_basis":"事實表無投入資本序列，無法以增量報酬乘再投資率算出上界，因此保守視為超出，Bear 機率取 30%。缺口歸因為營業利益率擴張，不靠併購或回購。","segments":[{"item":"資料中心","value":"FY26 約 5.0–5.1 億美元、年增 74%，占 38%；第四季 1.881 億美元；FY27 base case +80%，第一季指引季增約 15%"},{"item":"工業國防","value":"FY26 年增 27.8%，占 40%；第四季 1.646 億美元；FY27 目標 30% 以上"},{"item":"電信","value":"FY26 年增約 11%，占約 20%；第四季 7,210 萬美元；FY27 目標超過 3 億美元，上半年受 PON 與寬頻拖累"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY26 調整後 EPS +61% 對營收 +37%，差 24 個百分點，主要是營業槓桿。"},{"signal":"替代技術壓縮市場","lit":false,"note":"尚無出貨受損的硬數據，列為觀察。"},{"signal":"毛利率連兩季年減","lit":false,"note":"毛利率仍在上升。"},{"signal":"FCF 對淨利低於 0.75 連兩年","lit":false,"note":"FY25 GAAP 淨利為負，無法連續比較；第四季 FCF 對調整後淨利 0.85 倍。"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"第四季 5.6%，高於 5%，但逐年趨勢事實表未涵蓋。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金累積快、紀律尚可，沒有回購與股息；下一步的考驗是 50 億美元目標要靠多少併購。","reasoning":"FY26 營運現金流 3.57 億美元、資本支出 6,440 萬美元，FCF 約 2.93 億美元，利潤率約 22%。第四季 FCF 1.38 億美元，對調整後淨利 1.633 億美元為 0.85 倍。同業表的 TTM FCF 利潤率 9.44% 與法說數字對不上，這裡採法說。第四季 SBC 2,390 萬美元，占營收 5.6%，年化約占市值 0.6%。淨現金 4.517 億美元（現金及短投 7.924 億扣可轉債帳面 3.407 億，2029-12 到期），含租賃口徑為 3.855 億。管理層明言目前沒有回購或股息計畫，現金留給併購與景氣下行。現金去向四分的全年數字事實表未涵蓋。","fact_refs":["f_kpi3_stock_based_compensation","f_net_debt_m","f_shares_diluted_m","f_peer_mtsi_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"併購已實現報酬事實表未涵蓋；可見證據只有 FY24 GAAP 毛利率從 59.5% 降到 54.0%，以及管理層對 Linearizer 案的定性說法。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"沒有回購，2026-11-05 法說執行長稱目前沒有回購或股息計畫。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第四季 SBC 2,390 萬美元年化約 9,560 萬，占市值 161 億美元約 0.6%。限制：由淨利與 EPS 反推股數，FY23 約 7,150 萬到現在 7,637 萬，年增約 2.2%，其中含可轉債交換，無法單獨拆出 SBC。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"目前成長靠內部研發與產能，近 12 個月 8-K 沒有併購重大項目，也沒有回購與股息，無資本回報可展開。"}}}},"q5_valuation":{"verdict":"現價要賺 10% 年化，需要 FY31 EPS 約 15.5 美元且本益比維持 22 倍；我相信 FY27，FY28 之後保留。","reasoning":"現價 210.98 美元。FY1 前瞻本益比 24.7 倍，但 EPS 8.54 美元偏舊：共識營收 19.4 億美元配上第一季指引的 40% 營益率、6% 稅率與 7,900 萬股，約 9.5 美元，換算約 22 倍。TTM GAAP 本益比 48.95 倍，FY1 EV/S 8.11 倍。PEG 依 FY26A 到 FY29E 的 30.6% CAGR 約 0.81；扣掉 FY27 的跳升，用 FY27 到 FY29 的 20.9% 則約 1.18，後者較能代表現價買到的成長。上檔試算：12 個月以 FY28 Base EPS 11.0 美元乘 23 倍約 253 美元（+20%）；3 年以 FY30 Base EPS 14.0 美元乘 22 倍約 308 美元（+46%）。成長熄火測試：第四年起 EPS 年增降到 15%、10%、5%，分別乘 20、15、11 倍，FY31 價格約 331、227、152 美元，前兩者高於現價。賣方平均目標 377.56 美元（2026-08-01）高於現價 79%，但屬舊倍數環境，不單獨採用。五年分位在事實表只有 2–3 個年度端點，不具分位意義，留空；同業前瞻倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_ps_current","f_ev_s_current","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy3","f_rev_consensus_fy1_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比與 PEG，以 FY1 為口徑，輔以 EV/S 對照","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻倍數，無法做倍數對照。"},"fwd_pe":24.7,"peg":0.81,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 24.7 倍，修正 EPS 後約 22 倍，PEG 0.81–1.18，遠低於前份的 56 倍；但分母是否為週期高點正是爭點，因此結論是合理，不到便宜。反例：若 FY28 共識 EPS 跌破 9 美元，現價等於 23 倍以上而成長消失，應改判偏貴。","upside_short_pct":20,"upside_mid_pct":46,"denominator_disputed":true,"denominator_note":"FY1 共識 8.54 美元偏舊，低於第一季指引年化的 9.0 美元；更關鍵的是 FY27–FY28 EPS 是否為週期高點，正是市場爭點，所以 24.7 倍不能當作便宜的證據。"}}},"q6_how_wrong":{"verdict":"最可能看錯在 FY28：訂單沒有約束力，供給一鬆就可能出現重複下單回吐，這不是傳統價值陷阱，而是盈餘高點風險。","reasoning":"第一，股價 26 週跌 41%、RSI 38，市場已在定價 2028 消化，而我的 FY27 判斷可能正確卻無關緊要。第二，共識 FY1 三個月上修 55% 是財年滾動造成的假象，舊快照的 FY2、FY3 與新快照的 FY1、FY2 完全相同，不能當作上修動能。第三，NPO 贏單時程在 2026-11-05 法說拒答，光偵測器營收與分部毛利也不拆，第二條曲線的證據主要來自管理層口述。第四，2026-08-06 法說稱 NPO 部分專案不會量產，CW 雷射至今未宣告成功。法律面 10-K 無重大未決訴訟，近 12 個月 8-K 沒有重大事項。歷史最大回撤與空方最強數字事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_ma_w250","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"盈餘高點風險，非傳統價值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":8.54,"pe":24.7,"basis":"FY1（FY2027E）共識 EPS 8.54 美元，與終端倍數同為當年度 EPS 口徑；共識偏舊，修正後約 22 倍"},"eps":{"bull":[10.2,13.3,16.5,19.5,22.5],"base":[9.4,11.0,12.5,14.0,15.5],"bear":[8.6,7.5,6.8,7.6,8.5]},"pe":{"bull":27,"base":22,"bear":15},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-60,"hi":-40,"basis":"−40% 對應 250 週均線約 125 美元，也接近 Bear 五年終值；−60% 對應谷底 EPS 6.8 美元乘 12.5 倍約 85 美元。過去 26 週已跌 41%，顯示這種幅度並非極端。事實表未涵蓋歷史最大回撤，此處由情境推得。","trigger_time":null},"basis":{"bull":"NPO 與 CW 雷射 2028 起放量，FY31 營收約 52 億美元，營益率約 42%，稅率升到 15%；終端 27 倍，事實表未涵蓋同業倍數，以公司現值 24.7 倍為對照。","base":"FY27 營收 19.4–20 億美元，FY28 消化但不衰退，FY31 營收約 36 億美元、年增約 16%，營益率 40% 上下，稅率升到約 14%；EPS 已含股數稀釋，終端 22 倍低於現值 24.7 倍。","bear":"雲端資本支出 FY28 消化加上重複下單回吐，資料中心衰退 30–40%，FY29 EPS 谷底 6.8 美元，FY31 僅回到 8.5 美元；終端 15 倍對應成長降到 10% 的情境。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"訂單是採購單、無最低採購量；FY26 訂單出貨比 1.5，第四季當季接單當季出貨僅 7%，交期拉長；LightCounting 指 2027–2031 成長趨緩且與雲端資本支出高度相關。","assumption":"FY28 資料中心營收不衰退。","consequence":"若重複下單回吐，FY29 EPS 谷底約 6.8 美元，五年終值約 127 美元，較現價跌約 40%。","ruling":"採納，作為 Bear 主軸，機率 30%，與唯一致命點是同一件事。2026-11-05 法說對 2028 的回覆只有長期觀點，沒有數字，證據時間窗蓋不到風險窗。","watch":"訂單出貨比、資料中心季增率、雲端資本支出指引。","evidence_refs":["supply_demand_durability#1","customer_concentration_credit#2","customer_second_source#0"]},{"view":"論點失敗","evidence":"10-K 自述未來會有採低成本矽製程與高整合度的競爭；管理層在 2026-11-05 法說承認全整合 CMOS 不是公司的領域；評論文章指 CPO 內製可能縮小分離式元件市場。","assumption":"NPO 世代仍需要多功能或單功能的高效能 SiGe 元件。","consequence":"資料中心第二條曲線落空，FY31 EPS 落在 Base 以下，終端倍數同步下修。","ruling":"部分採納。目前沒有出貨受損的硬數據，且 448G 驅動器已針對矽光子與 NPO 設計，但 NPO 贏單未揭露，機率取 35%。","watch":"NPO 首筆量產營收時點、超大規模業者的 NPO 方案選擇。","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"]},{"view":"論點失敗","evidence":"FY25 中國占營收 28.4%，多數產品受出口管制，10-K 稱已造成部分出貨困難；2026-08-06 法說回應中國模組廠禁令傳聞時，執行長預期客戶組合移轉而非流失。","assumption":"中國模組廠的份額可由其他地區補回。","consequence":"若禁令實施且補位落後，FY27–FY28 資料中心至少延遲數季。","ruling":"部分採納。管理層的移轉說法未經驗證，列為短期風險，以下季指引作為吸收失敗的判準。","watch":"出口管制公告、次季營收指引、10-K 中國營收占比。","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1"]},{"view":"論點成功但股東經濟變差","evidence":"執行長在 2026-11-05 法說稱 2030 年想成為 50 億美元公司，需要更多技術、人員與新市場，暫無回購與股息；FY27 資本支出升到 1.0–1.1 億美元；SiGe 代工要求確定承諾，公司表示願意簽。","assumption":"營收成長能以現有紀律換成每股價值。","consequence":"若靠大型併購達標，或簽下確定承諾後遇到需求下滑，營收達標但 FCF 轉換率與資本報酬下降。","ruling":"部分採納。目前併購仍是小型補強，但 FY24 GAAP 毛利率曾從 59.5% 降到 54.0%，大型案的風險要預先設門檻。","watch":"單筆併購占市值比重、代工承諾金額、GAAP 與調整後淨利差距。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"view":"價格已反映太多","evidence":"TTM 本益比 48.95 倍，P/S 12.14 倍與 EV/S 11.85 倍都是三個年度端點內最高；FY1 倍數建立在可能是週期高點的盈餘上。","assumption":"FY27 不是盈餘高點。","consequence":"若 FY27–FY28 就是高點，現在的 22–25 倍其實偏貴，本益比最低的時候往往不是買點。","ruling":"反駁一半。Base 情境本益比由 24.7 倍降到 22 倍，年化約 10% 全靠盈餘，不依賴倍數擴張；但股價已跌 45% 本身不是安全邊際。","watch":"FY28 共識 EPS 是否跌破 9 美元。","evidence_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 385.98 → 本次 210.98（-45.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=385.98","side_b":"本次 price_at_dd=210.98","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 385.98 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 385.98 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 385.98 美元：Bull 價 607.5、Bear 價 127.5，五年期望值 −14.4%，基準年化 −2.4%，不對稱比 0.57","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.57。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 385.98 美元：五年期望值 −14.4%，基準年化 −2.4%，不對稱比 0.57","side_b":"本次情境、股價 210.98 美元：五年期望值 +56.5%，基準年化 10.1%，不對稱比 3.17","ruling":"再換股價、情境不動：起點價下跌 45.3%，五年期望值多 71.0 個百分點，基準年化多 12.5 個百分點，不對稱比由 0.57 升到 3.17。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 385.98 美元，FY26／FY27 前瞻本益比 76／56 倍，結論偏貴。","side_b":"本次股價 210.98 美元，FY1 前瞻本益比 24.7 倍，結論合理。","ruling":"可調和。股價跌 45% 是主因，FY27 盈餘上修是次因；分母是否為週期高點仍有爭議，所以只升到合理。","evidence_level":"高","settle_metric":"財報後第一份完整共識的 FY27 與 FY28 EPS","if_then":["若 FY28 共識 EPS 跌破 9 美元，停止加碼","若股價漲回 280 美元以上而訂單證據未到，不追"],"evidence_refs":[]},{"axis":"整體評等與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評等 B，陷阱風險低。","side_b":"本次評等 B，陷阱風險中等。","ruling":"FY26 EPS 成長 61% 遠高於營收 37%，衰退信號亮一顆，陷阱風險由低升到中等。股價大跌沒有換來更高評等，因為 FY28 能見度仍低，Base 年化約 10% 只算中等。","evidence_level":"中","settle_metric":"FY27 第三季財報的訂單出貨比","if_then":["若連續兩季訂單出貨比不低於 1.2，加碼至 6%","若連續兩季低於 1.0，減碼一半"],"evidence_refs":[]},{"axis":"前份空白欄位首次填入","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位為空白。","side_b":"本次護城河方向為 →，成長跑道寬，屬品質複利成長、中循環，機率 20／50／30，回撤範圍 −40% 到 −60%。","ruling":"沒有舊值可比，屬首次填入，不代表判斷改變。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"清倉與減碼門檻首次設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（欄位空白）。","side_b":"清倉：資料中心營收連續兩季季減。減碼：訂單出貨比連續兩季低於 1.0，或調整後毛利率低於 60%。","ruling":"新設門檻，因為前份的風險條件只寫到削弱與反轉，沒有對應動作。","evidence_level":"中","settle_metric":"每季資料中心營收與訂單出貨比","if_then":["資料中心營收連續兩季季減，清倉","訂單出貨比連續兩季低於 1.0，減碼一半"],"evidence_refs":[]},{"axis":"重新進場門檻首次設定","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設門檻欄，只在結論寫等回測 290–330 美元或布林中軌 257 美元。","side_b":"現價 230 美元以下建第一筆；FY27 第一季資料中心季增 ≥10% 且訂單出貨比 ≥1.0 才加碼","ruling":"舊等待價位已被穿越，不再適用。新條件把價格與訂單證據分開：價格只決定第一筆，加碼要看訂單。","evidence_level":"中","settle_metric":"FY27 第一季財報","if_then":["達標則加碼至 4%","股價跌到 170–195 美元而基本面未破，分批反買"],"evidence_refs":[]},{"axis":"Single Thing 首次設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未列唯一致命點（欄位空白）。","side_b":"FY28 結束前，資料中心營收出現連續兩季季減。","ruling":"新設。這是情境樹中最大的單一敏感項：Base 與 Bear 的 FY29 EPS 相差 46%，本益比再從 22 倍壓到 15 倍。","evidence_level":"中","settle_metric":"每季資料中心營收","if_then":["事件發生，清倉"],"evidence_refs":[]},{"axis":"共識上修幅度","cause":"方法變動","prior_field":null,"side_a":"事實表顯示 FY1 共識三個月上修 55%。","side_b":"舊快照 FY2 8.54、FY3 10.11 美元，與新快照 FY1、FY2 完全相同，這是財年滾動；FY27 共識在兩份快照之間沒有變動。","ruling":"採後者。55% 不是真實上修，不作為動能證據。8.54 美元也低於第一季指引年化 9.0 美元，說明快照尚未反映最新財報。","evidence_level":"高","settle_metric":"財報後第一份完整共識的 FY27 EPS，接近 9.5 美元才算真上修","if_then":["若完整共識 FY27 EPS 仍低於 9 美元，重新檢視營益率假設，停止加碼"],"evidence_refs":[]},{"axis":"FCF 利潤率口徑","cause":"方法變動","prior_field":null,"side_a":"同業表 TTM FCF 利潤率 9.44%。","side_b":"法說 FY26 營運現金流 3.57 億美元、資本支出 6,440 萬美元，FCF 約 2.93 億美元，利潤率約 22%。","ruling":"採法說口徑。同業表差異原因無法在本包查證，所以同業 FCF 比較不作為論據。","evidence_level":"中","settle_metric":"FY26 10-K 現金流量表","if_then":[],"evidence_refs":[]},{"axis":"短缺持續時間與 2028 能見度","cause":"新證據","prior_field":null,"side_a":"LightCounting（2026 年 4 月）：短缺預計 2026 年底消退，2027–2031 成長趨緩。","side_b":"Lumentum（2026 年 8 月）稱 EML 產能訂到 2027；公司 2026-11-05 法說稱積壓訂單創新高、交期拉長。","ruling":"短缺時間點採後者，資料較新。2028 需求不可裁決，要到 FY27 第三季財報（約 2027-08）才有第一批訂單證據；在此之前不得稱風險已解除，所以倉位上限先壓在 4%。","evidence_level":"中","settle_metric":"FY27 第三季訂單出貨比與 FY28 排程訂單","if_then":["訂單出貨比連續兩季不低於 1.2，加碼至 6%","訂單出貨比連續兩季低於 1.0，減碼一半"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"管理層口徑對帳","cause":"新證據","prior_field":null,"side_a":"2026-08-06 法說：執行長稱 FY27 資本支出約 6,000 萬美元、資料中心 base case +50%，CW 雷射最早 2027 年底量產，同場問答又說 2028。","side_b":"2026-11-05 法說：財務長稱 FY27 資本支出 1.0–1.1 億美元；執行長稱資料中心 base case +80%，CW 雷射目標 2028，尚未宣告成功。","ruling":"資本支出上修與訂單同向，可以解釋，但三個月內上修七成，顯示能見度不如口徑穩定。CW 雷射時程偏向 2028，FY28 前不計入 Base 的放量。","evidence_level":"高","settle_metric":"Phase 2 擴產是否於 2027 年中啟動","if_then":["Phase 2 延到 2028，H3 視為削弱，停止加碼"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":"新證據","prior_field":null,"side_a":"賣方論證：股價低於 52 週均線 262.51 美元，26 週跌 41%，市場在定價 2028 消化；FY27 可能就是週期高點，高點時本益比最低，低本益比不是買點。","side_b":"不賣論證：第一季指引營益率 40%，FY26 工業國防占 40%，FY27 目標年增 30% 以上；淨現金 4.5 億美元。","ruling":"不賣，但只分批小量建立。Base 年化約 10%、Bear 機率 30%，賠率不足以重押。","evidence_level":"中","settle_metric":"FY27 第三季訂單出貨比","if_then":["若資料中心連續兩季季減，清倉","若股價先跌而基本面無損，分批反買"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭：10-K 列 11 家競爭者並提到中國公司競爭加劇，分析師點名 Astera Labs 跨入 TIA 與驅動器。其他結構：CPO 與 NPO 架構變動，出口管制持續。","side_b":"結構轉好：NXP 退出 5G 射頻功率 GaN，部分雷射廠退出 25G DFB，公司是唯一美國本土 5G 功率放大器供應商。","ruling":"雙向拉鋸。射頻與國防的供給面在改善，資料中心的競爭與架構風險在升高。","evidence_level":"中","settle_metric":"調整後毛利率與 NPO 量產案","if_then":["毛利率低於 60%，減碼至 1%"],"evidence_refs":["competitive_share_entrants#0","geo_supply_chain#2"]},{"axis":"客戶集中度口徑","cause":"新證據","prior_field":null,"side_a":"10-K：前十大客戶占比由 FY23 的 48% 升到 FY25 的 57%。","side_b":"2026-08-06 法說，執行長：前十大終端客戶低於 40%，年收入超過 1,000 萬美元的客戶由約 8 家增到逾 20 家。","ruling":"可調和。10-K 計入經銷商，經銷占比升到 32.3%；終端口徑只有管理層口述，無法驗證，風險仍保留。","evidence_level":"中","settle_metric":"FY26 10-K 客戶集中度揭露","if_then":["前十大客戶占比超過 60%，停止加碼"],"evidence_refs":["customer_concentration_credit#1"]}],"triggers":[{"n":1,"text":"FY27 第一季資料中心季增未達 10%","type":"假設驗證","maps_to":"H1","metric":"資料中心營收季增率","threshold":"低於 10%（指引約 15%）","action":"停止加碼","source_freq":"季度法說","date":"2027-02"},{"n":2,"text":"訂單出貨比連續兩季低於 1.0","type":"減碼","maps_to":"R1","metric":"公司整體訂單出貨比","threshold":"連續 2 季低於 1.0","action":"減碼一半","source_freq":"季度法說","date":"2027-05","evidence_refs":["supply_demand_durability#1","customer_concentration_credit#2","customer_second_source#0"]},{"n":3,"text":"資料中心營收連續兩季季減","type":"Single Thing","maps_to":"Single Thing","metric":"資料中心營收季增率","threshold":"連續 2 季為負","action":"清倉","source_freq":"季度法說","date":null},{"n":4,"text":"現價 230 美元以下建第一筆","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"230 美元以下，約 Base FY27 EPS 的 24.5 倍","action":"建第一筆 2%","source_freq":"每日收盤","date":null},{"n":5,"text":"第一季達標，或股價跌到 104 週均線附近而基本面未破","type":"加碼","maps_to":"H1","metric":"資料中心季增率、訂單出貨比、股價","threshold":"季增 ≥10% 且訂單出貨比 ≥1.0；或股價 170–195 美元且 H1 未破","action":"加碼至 4%","source_freq":"季度法說與每日收盤","date":"2027-02"},{"n":6,"text":"毛利率回落且競爭者量產","type":"減碼","maps_to":"H2","metric":"調整後毛利率","threshold":"低於 60%，或連續 2 季環比下滑 1 個百分點以上","action":"減碼至 1%","source_freq":"季度 8-K","date":null,"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#1"]},{"n":7,"text":"中國出口限制升級","type":"風險","maps_to":"R3","metric":"中國模組廠禁令與下季營收指引","threshold":"禁令實施，且下季指引低於前季營收 5% 以上","action":"減碼一半","source_freq":"事件與季度法說","date":null,"evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1"]},{"n":8,"text":"代工或關鍵材料造成出貨受限","type":"風險","maps_to":"R4","metric":"營收對指引下緣、揭露的代工承諾金額","threshold":"營收低於指引下緣且歸因供應；或代工承諾超過年營收 20%","action":"停止加碼","source_freq":"季度法說與 10-Q","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"n":9,"text":"NPO 或 CPO 改採全整合 CMOS 方案","type":"風險","maps_to":"R2","metric":"超大規模業者方案選擇、公司 NPO 營收","threshold":"主要業者量產採全整合方案，且公司 FY28 NPO 無營收","action":"減碼至 1%","source_freq":"產業新聞與季度法說","date":"2028-09","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"]},{"n":10,"text":"FY27 第三季財報提供第一批 FY28 訂單證據，到期複審","type":"複審日期","maps_to":"H1","metric":"訂單出貨比與 FY28 排程訂單","threshold":"到期即複審","action":"訂單出貨比 ≥1.2 加碼至 6%；低於 1.0 減碼一半","source_freq":"季度法說","date":"2027-08"}],"kill_metrics":[{"metric":"資料中心營收季增率","bear_threshold":"連續兩季季減（清倉）","window":"FY27–FY28 每季","source":"MACOM 季度法說與 8-K","last_status":"ok"},{"metric":"公司整體訂單出貨比","bear_threshold":"連續兩季低於 1.0（減碼一半）","window":"FY27–FY28 每季","source":"MACOM 季度法說","last_status":"ok"},{"metric":"調整後毛利率","bear_threshold":"低於 60%，或連續兩季環比下滑 1 個百分點以上（減碼）","window":"FY27–FY28 每季","source":"MACOM 季度 8-K","last_status":"ok"},{"metric":"FY28 共識 EPS","bear_threshold":"低於 9 美元（停止加碼）","window":"至 FY28 財報","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"NPO 與 CW 雷射量產營收","bear_threshold":"FY28 結束前兩者皆無量產營收（減碼）","window":"至 2028-09","source":"MACOM 季度法說","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"現價 230 美元以下建第一筆；FY27 第一季資料中心季增 ≥10% 且訂單出貨比 ≥1.0 才加碼","exec_line":"分三筆：230 美元以下先建 2%；FY27 第一季財報達標加到 4%；FY27 第三季財報確認 FY28 訂單延伸後才到 6%。股價先漲到 280 美元以上而證據未到，不追；股價下跌而基本面無損，分批反買。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把全公司當成 AI 資本支出的單一賭注，26 週跌 41%；但 FY26 工業國防占 40%、FY27 目標年增 30% 以上，且 FY27 共識 EPS 8.54 美元低於第一季指引年化 9.0 美元。市場對 2028 的疑慮有道理，錯在把折扣也套到與 AI 較無關的業務。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"資料中心完成 FY27 base case，FY28 不衰退","2y":"FY27 資料中心營收 ≥9 億美元，FY28 年增為正","5y":"FY31 資料中心營收 ≥18 億美元，約占公司一半","10y":null,"threshold":"FY27 第一季季增 ≥10%；FY27 資料中心營收 ≥9 億美元；公司訂單出貨比 ≥1.0","source":"MACOM 季度法說與 8-K","drift_rule":"TTM 偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"利潤率提升有一部分是結構性，短缺結束後仍能守住","2y":"FY27 調整後毛利率 ≥62.5%、營益率 ≥40%","5y":"FY31 調整後毛利率 ≥62%、營益率 ≥38%","10y":null,"threshold":"FY27 第一季調整後毛利率 62–63%、營益率約 40%；之後每季毛利率增加 25–50 基點","source":"MACOM 季度 8-K 與法說","drift_rule":"TTM 偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H3","text":"NPO 與 CW 雷射在 2028 成為第二條曲線，接住資料中心放緩","2y":"CW 雷射完成認證，Lowell 第二階段於 2027 年中啟動","5y":"FY31 NPO 與 CW 雷射合計營收 ≥5 億美元","10y":null,"threshold":"FY28 結束前至少一項有量產營收；第二階段擴產不晚於 2027 年底啟動","source":"MACOM 法說；2026-08-06 法說執行長稱 NPO 有 10–20 個開發案，部分不會量產","drift_rule":"TTM 偏離連 4 季 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉；第二階段延到 2028 視為削弱"},{"id":"H4","text":"工業國防提供資料中心以外的地板","2y":"FY27 工業國防年增 ≥30%，營收約 6.9 億美元","5y":"FY31 工業國防營收 ≥12 億美元","10y":null,"threshold":"FY27 年增 ≥30%；RTP 廠產能擴充按計畫進行","source":"MACOM 季度法說","drift_rule":"TTM 偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"雲端資本支出消化與重複下單：訂單無最低採購量，交期拉長時客戶傾向多下單，供給一鬆就回吐","h_ref":"H1","clock":"🔥","threshold":"訂單出貨比連 2 季低於 1.0；或資料中心季增轉負；五大雲端資本支出年增連 2 季低於 15%（目前讀值事實表未涵蓋）","evidence_refs":["supply_demand_durability#1","customer_concentration_credit#2","customer_second_source#0"]},{"id":"R2","text":"架構替代：全整合 CMOS 在 NPO 或 CPO 勝出，分離式 TIA、驅動器與光偵測器的市場縮小","h_ref":"H3","clock":"🐢","threshold":"主要超大規模業者量產採全整合方案，且公司 FY28 NPO 無營收","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"]},{"id":"R3","text":"中國與出口管制：FY25 中國占營收 28.4%，管理層預期客戶組合移轉的說法未經驗證","h_ref":"H1","clock":"⚡","threshold":"中國模組廠禁令實施，且下季指引低於前季營收 5% 以上","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R4","text":"代工與關鍵材料：SiGe 委外、特定製程單一來源，資料中心成長 80% 依賴代工配合；簽下確定承諾後，下行時彈性變小","h_ref":"H1","clock":"🔥","threshold":"營收低於指引下緣且歸因供應；或揭露的代工承諾超過年營收 20%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R5","text":"競爭與客戶集中度：新進者搶 TIA 與驅動器份額，10-K 前十大客戶占比由 48% 升到 57%","h_ref":"H2","clock":"🔥","threshold":"調整後毛利率連 2 季環比下滑 1 個百分點以上，且競爭者宣布 200G／lane 光偵測器量產；或前十大客戶占比超過 60%","evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#1"]},{"id":"R6","text":"併購失誤：2030 年 50 億美元目標需要新技術與新市場，現金累積後大型併購的機率上升","h_ref":"H2","clock":"🐢","threshold":"單筆併購超過市值 10%；或 GAAP 淨利連 3 年低於調整後淨利 60%","evidence_refs":[]}],"single_thing":{"description":"FY28 結束前，資料中心營收出現連續兩季季減。","why_fatal":"資料中心 FY27 約占營收 47%，也是增量獲利的主要來源；Base 與 Bear 的 FY29 EPS 相差 46%，本益比再從 22 倍壓到 15 倍，是情境樹中最大的單一敏感項。","if_happens":"清倉，等訂單出貨比連續兩季回到 1.0 以上再重做研究。","how_monitor":"每季法說的資料中心營收與季增率、訂單出貨比，輔以雲端資本支出指引。","probability":"30%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.87,"peg_fy2":1.0,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":5.6,"FY2027E":8.54,"FY2028E":10.11,"FY2029E":12.48},"fy_end_month":9,"eps_basis":"調整後（Non-GAAP）稀釋 EPS；FY26A 5.60 美元來自 2026-11-05 法說，FY27E–FY29E 為 2026-11-07 Koyfin 共識，財報後尚未完整更新"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第一季財報","impact":"高","watch":"資料中心季增約 15%、毛利率 62–63%、訂單出貨比"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"CHIPS 最終協議可能簽署","impact":"中","watch":"2026-08-06 法說提到有無法接受的條款，留意最終條件與補助金額"},{"date":"2027-06","date_precision":"month","type":"capacity","event":"Lowell 第二階段擴產預計啟動，視 CW 雷射表現而定","impact":"中","watch":"是否如期啟動，以及 CW 雷射可靠度結果"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27 第三季財報，FY28 訂單能見度的第一批證據","impact":"高","watch":"訂單出貨比、FY28 排程訂單、管理層對 2028 的量化說法"},{"date":"2028-Q1","date_precision":"quarter","type":"product","event":"NPO 與 CW 雷射預期開始貢獻營收","impact":"高","watch":"首筆量產營收與客戶數"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把全公司當成 AI 資本支出的單一賭注，26 週跌 41%；但 FY26 工業國防占 40%、FY27 目標年增 30% 以上，且 FY27 共識 EPS 8.54 美元低於第一季指引年化 9.0 美元。市場對 2028 的疑慮有道理，錯在把折扣也套到與 AI 較無關的業務。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-41.37, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
