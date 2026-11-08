你是 DD 管線 v20 的判斷層閘（gate），標的 MSI（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝3376 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-03，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿（IR 發布，SEC 檔）https://www.sec.gov/Archives/edgar/data/0000068505/000006850526000041/msiq32026pressrelease.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-10-03，公告於 2026-11-04））
- `f_kpi1_non_gaap_operating_earni`（q1_business）｜Non-GAAP operating earnings / margin＝1096 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-03，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿（IR 發布，SEC 檔）https://www.sec.gov/Archives/edgar/data/0000068505/000006850526000041/msiq32026pressrelease.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-10-03，公告於 2026-11-04））
- `f_kpi6_backlog`（q1_business）｜Backlog＝16.6 USD B｜期間與口徑：Q3 FY2026（季末 2026-10-03，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿（IR 發布，SEC 檔）https://www.sec.gov/Archives/edgar/data/0000068505/000006850526000041/msiq32026pressrelease.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-10-03，公告於 2026-11-04））
- `f_peer_msi_gross_margin_pct`（q2_moat）｜MSI 毛利率＝52.18 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_msi_operating_margin_pct`（q2_moat）｜MSI 營業利益率＝25.42 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_axon_gross_margin_pct`（q2_moat）｜AXON 毛利率＝59.41 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AXON.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_axon_operating_margin_pct`（q2_moat）｜AXON 營業利益率＝0.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AXON.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_zbra_operating_margin_pct`（q2_moat）｜ZBRA 營業利益率＝16.53 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ZBRA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_tdy_operating_margin_pct`（q2_moat）｜TDY 營業利益率＝20.0 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TDY.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lhx_operating_margin_pct`（q2_moat）｜LHX 營業利益率＝10.69 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LHX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝17.73 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝19.43 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝21.69 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝13048.01 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝14253.14 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_guidance_q4_fy2026_fy202`（q1_business）｜Guidance: Q4 FY2026 / FY2026（本季上調）＝Q4 營收約 +13% YoY、non-GAAP EPS 5.47–5.52；FY2026 營收約 13.05B、non-GAAP EPS 17.94–17.99、營運現金流 3.05B text｜期間與口徑：Q3 FY2026（季末 2026-10-03，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 8-K 新聞稿（IR 發布，SEC 檔）https://www.sec.gov/Archives/edgar/data/0000068505/000006850526000041/msiq32026pressrelease.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-10-03，公告於 2026-11-04））
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝589 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-03，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿（IR 發布，SEC 檔）https://www.sec.gov/Archives/edgar/data/0000068505/000006850526000041/msiq32026pressrelease.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-10-03，公告於 2026-11-04））
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝13.3 %｜期間與口徑：Q3 FY2026（季末 2026-10-03，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿（IR 發布，SEC 檔）https://www.sec.gov/Archives/edgar/data/0000068505/000006850526000041/msiq32026pressrelease.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-10-03，公告於 2026-11-04））
- `f_kpi2_gaap_operating_earnings_`（q1_business）｜GAAP operating earnings / margin＝777 USD M｜期間與口徑：Q3 FY2026（季末 2026-10-03，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿（IR 發布，SEC 檔）https://www.sec.gov/Archives/edgar/data/0000068505/000006850526000041/msiq32026pressrelease.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-10-03，公告於 2026-11-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝9891.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 10665.0、現金 774.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_msi_fcf_margin_pct`（q2_moat）｜MSI FCF 利潤率＝20.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.941 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝514.51 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝29.02 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 17.73，分子＝快照價 514.51｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝41.39 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝60.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝60.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝83.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝98.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.06 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（17.72 → 17.73）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝34.74 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝427.21 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝431.7 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝347.75 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_kpi7_non_gaap_diluted_eps`（q1_business）｜Non-GAAP diluted EPS＝4.69 USD｜期間與口徑：Q3 FY2026（季末 2026-10-03，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K 新聞稿（IR 發布，SEC 檔）https://www.sec.gov/Archives/edgar/data/0000068505/000006850526000041/msiq32026pressrelease.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-10-03，公告於 2026-11-04））

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 稱公司面對數量增加的既有與新競爭者；MCN 主要對手含 Airbus、Hytera、JVCKenwood、L3Harris、Persistent Systems、Sepura、Tait、TrellisWare 等。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-12）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：新技術與新競爭者進入市場的速度比過去快；收購 Silvus 後，在部分產品面對新創與國防承包商的競爭加劇。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：多國政府有計畫將公安通訊從 LMR 轉到公共行動寬頻網路，目前進展有限，若客戶認為寬頻足夠，可能衝擊 MCN 銷售。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因子指出生物辨識、ALPR 等分析產品面臨州法律與 FTC 執法的監管及訴訟風險，預期州 ALPR 立法增加。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：搜尋摘要：英國 CMA 對 Airwave 的價格管制命令已成立，Motorola 上訴失敗，英國上訴法院 2025-01-30 拒絕上訴許可；Home Office 將 Airwave 關停目標延至 2029-12-31，按 Charge Control 費率。
  - 來源：搜尋摘要（引 MSI FY2025 10-K）（as_of 2026-02-12）｜affects：valuation、decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K：MSI 進口的產品、材料與零件適用進口關稅，2025 年美國新增與加徵關稅使其進口關稅提高。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K 風險因素：供應中斷或價格上升可能源於新增／報復性關稅、制裁、進出口限制（含稀土）；美國政府業務受出口管制等合規要求規範。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露：部分材料與零組件來自單一來源供應商，若其產能受限或破產可能造成供應中斷或漲價。
  - 來源：Motorola Solutions FY2025 Form 10-K（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K：多數產品由外部合約製造商生產，據點在墨西哥與馬來西亞（搜尋摘要轉述，非逐字）。
  - 來源：Motorola Solutions FY2025 Form 10-K（as_of 2026-02-01）｜affects：thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2026 Q2/Q3 申報：公司稱與遍布全球的供應商網路合作，以降低對等關稅、記憶體成本與進出口規定的曝險；供應鏈波動與不確定性仍高，庫存預期維持高檔。
  - 來源：Motorola Solutions Q3 2026 Form 10-Q（as_of 2026-10-30）｜affects：thesis.R、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：MSI 10-K 風險因子：多國政府推動公共安全通訊由 LMR 轉向公共行動寬頻網路，目前進展有限；若客戶認為寬頻（可能輔以新興技術）在韌性、覆蓋、控制與成本上足夠，可能不利 MCN 銷售。另提及加密破解技術與對抗環境下的通訊能力風險。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1050.0,"bear_5y_price":368.6,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":41.9,"ev5y_pct":36.4,"irr_base_pct":7.2,"asym_ratio":3.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":17.965,"pe":28.64,"basis":"FY2026 Non-GAAP EPS 財測中點（17.94 至 17.99 美元，2026-11-04），與終端倍數同為當年度口徑；Koyfin 共識 17.73 美元尚未反映上修。"},"eps":{"bull":[20.7,23.9,27.4,31.1,35.0],"base":[19.8,22.0,24.3,26.7,29.2],"bear":[18.6,18.3,18.6,19.0,19.4]},"pe":{"bull":30,"base":25,"bear":19},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.941,"net_buyback":0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":8.5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MSI_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Jason Winkler (CFO)｜guidance：Q3 營收成長指引約 8%（原話："We expect Q3 sales growth of approximately 8%"）
- 2026-08-05｜Jason Winkler (CFO)｜guidance：全年營收指引上調（前次 $12.8B）（原話："revenue of approximately $12.975 billion"）
- 2026-08-05｜Jason Winkler (CFO)｜guidance：全年 non-GAAP EPS 指引區間（前次 $16.87–16.99）（原話："non-GAAP earnings per share between $17.62 and $17.72"）
- 2026-08-05｜Jason Winkler (CFO)｜guidance：$175M 營收上調的拆解：MCN，含 Silvus 約 $100M（原話："including approximately $100 million from Silvus"）
- 2026-08-05｜Jason Winkler (CFO)｜guidance：Silvus 全年營收預期約 $850M（原話："approximately $850 million in full-year revenue"）
- 2026-08-05｜Jason Winkler (CFO)｜guidance：MCN 全年成長指引由 8–9% 上調（原話："MCN is now expected to grow between 10% and 11%"）
- 2026-08-05｜Jason Winkler (CFO)｜guidance：Video 全年成長指引（原話："Video is expected to grow 11%"）
- 2026-08-05｜Gregory Brown (CEO)｜guidance：管理層稱下半年預期未變、一直規劃強勁下半年（原話："the second half as we look, remains unchanged"）
- 2026-08-05｜Gregory Brown (CEO)｜guidance：下半年訂單預期雙位數成長（原話："expected double-digit orders in the second half"）
- 2026-08-05｜Gregory Brown (CEO)｜guidance：LMR 下半年預期成長 10%（原話："to grow in the second half of this year, 10% as well"）
- 2026-08-05｜Gregory Brown (CEO)｜guidance：Q4 強勁的來源之一為 D-Series 基礎建設出貨（原話："infrastructure D-Series that are coming in Q4"）
- 2026-08-05｜John Molloy (COO)｜guidance：UHF 版 D-Series 將於 Q4 開始出貨（原話："UHF will begin shipping in Q4, Jason."）
- 2026-08-05｜Gregory Brown (CEO)｜guidance：全年指引只含現有資產，不含未完成併購（原話："reflect the assets we have today"）
- 2026-08-05｜Jason Winkler (CFO)｜margin：全年營業利益率預期擴張幅度上調（前次 100bp）（原話："now expect approximately 170 basis points of expansion"）
- 2026-08-05｜Gregory Brown (CEO)｜margin：Q2 排除 IEEPA 退款後營業利益率擴張 140bp（原話："operating margin expansion of 140 basis points"）
- 2026-08-05｜Jason Winkler (CFO)｜margin：Q2 含 $60M IEEPA 退款利益（原話："a $60 million benefit from the IEEPA"）
- 2026-08-05｜Jason Winkler (CFO)｜margin：全年關稅影響預期中性（原話："the tariff impact to be neutral for the full year"）
- 2026-08-05｜Jason Winkler (CFO)｜margin：記憶體直接支出全年預期 $150M（去年 $50M）（原話："our direct memory spend to be approximately $150 million"）
- 2026-08-05｜Jason Winkler (CFO)｜margin：全年毛利率預期與去年相當（原話："gross margins to be comparable to last year"）
- 2026-08-05｜Jason Winkler (CFO)｜margin：新增記憶體成本多數落在下半年（原話："part of that's going to be faced in the second half"）
- 2026-08-05｜Jason Winkler (CFO)｜margin：對高記憶體含量的 Video 產品做選擇性漲價（原話："increases on high memory content items in Video"）
- 2026-08-05｜Jason Winkler (CFO)｜margin：記憶體在 Video 比在 LMR 更重要（原話："It's a more material contributor or item in Video."）
- 2026-08-05｜Jason Winkler (CFO)｜risk：記憶體成本為挑戰，供給目前可得（原話："Memory for us is a challenge in what we're having to pay"）
- 2026-08-05｜Jason Winkler (CFO)｜risk：MCN 使用較簡單的 RAM，可替代（原話："greatest high-speed DRAM, and we can substitute it"）
- 2026-08-05｜Gregory Brown (CEO)｜risk：D-Fend 交割待監管核准（原話："We'll work the traps on the regulatory approvals"）
- 2026-08-05｜Jason Winkler (CFO)｜capital_allocation：Q2 回購均價與金額（原話："share repurchases at an average price of $413.53 per share"）
- 2026-08-05｜Jason Winkler (CFO)｜capital_allocation：D-Fend 收購協議（$1.5B，預期下半年交割）（原話："definitive agreement to acquire D-Fend Solutions"）
- 2026-08-05｜Jason Winkler (CFO)｜capital_allocation：為 D-Fend 預計新增約 $1B 負債（原話："we expect to raise approximately $1 billion of incremental"）
- 2026-08-05｜Jason Winkler (CFO)｜capital_allocation：年底淨負債/EBITDA 預期約 2 倍（原話："net debt-to-EBITDA leverage at approximately 2x"）
- 2026-08-05｜Jason Winkler (CFO)｜capital_allocation：Bell Canada LMR 服務業務預計 Q4 末交割（原話："LMR networks services business in late Q4."）
- 2026-08-05｜Gregory Brown (CEO)｜capital_allocation：管理層稱資產負債表讓資本配置有彈性（原話："enable us to be flexible in how we deploy capital"）
- 2026-08-05｜Gregory Brown (CEO)｜capital_allocation：D-Fend 預期營收約 $185M（原話："expect it to be about $185 million in revenue"）
- 2026-08-05｜Gregory Brown (CEO)｜commitment：管理層預期年底產品積壓訂單高於去年（原話："I expect product backlog to be up at the end of this year"）
- 2026-08-05｜John Molloy (COO)｜commitment：Silvus 擴產效益 2027 才顯現，今年指引在現有產能內（原話："we'll start to see the benefit of that in 2027"）
- 2026-08-05｜John Molloy (COO)｜commitment：今年 Silvus 指引受現有產能限制（原話："takes into account our current capacity"）
- 2026-08-05｜Gregory Brown (CEO)｜commitment：Salt Lake City 新廠預計 Q1 上線（原話："that comes online in early Q1"）
- 2026-08-05｜Jason Winkler (CFO)｜commitment：預期 APX NEXT 訂閱用戶年底達 30 萬（原話："We expect 300,000 subscribers by the year-end '26"）
- 2026-08-05｜John Molloy (COO)｜commitment：D-Series 換新週期不只 Q4，將延續到 2030 年代（原話："It won't be just a fourth quarter thing."）
- 2026-08-05｜John Molloy (COO)｜commitment：D-Series 網路更新持續至 2030 年代（原話："refresh networks, quite frankly, into the 2030s."）
- 2026-08-05｜Jason Winkler (CFO)｜product：Q2 Silvus 營收約 $230M（Q1 約 $210M）（原話："in Q1, about $230 million in Q2"）
- 2026-08-05｜Gregory Brown (CEO)｜product：D-Series 為十二年來首次基礎建設升級（原話："first time we've upgraded the infrastructure"）
- 2026-08-05｜Jason Winkler (CFO)｜product：基礎建設占 LMR 業務不到四分之一（原話："infrastructure is a little less than 1/4 of the LMR business"）
- 2026-08-05｜Mahesh Saptharishi (CTO)｜product：VESTA 在 Q2 100% 為含 AI 的 assist 等級（原話："100% of our VESTA emergency call handling solutions in Q2"）
- 2026-08-05｜Mahesh Saptharishi (CTO)｜product：AI 功能使 ASP 全面提高（原話："meaningfully raising our ASPs across the board"）
- 2026-08-05｜John Molloy (COO)｜product：首款通過 NFPA 1930 認證的 APX NEXT 裝置（原話："APX NEXT XN, which actually puts us in the first"）
- 2026-08-05｜John Molloy (COO)｜product：Silvus 在美國國防部反干擾測試成績優異（原話："Silvus received exceptional scoring"）
- 2026-08-05｜Gregory Brown (CEO)｜customer：FHP 與 KC 警局為首次採用隨身攝影與車載影像客戶（原話："both of these large agencies are first-time users"）
- 2026-08-05｜John Molloy (COO)｜customer：FHP 與 KC 為新 RFP 取得，非既有客戶延伸（原話："Those were new RFPs that we secured"）
- 2026-08-05｜John Molloy (COO)｜customer：2027 州與地方公共安全預算成長快於政府預算（原話："public safety budgets are growing faster"）
- 2026-08-05｜Gregory Brown (CEO)｜customer：Q2 期末積壓訂單創高，$15.6B（原話："record Q2 ending backlog of $15.6 billion"）
- 2026-08-05｜Jason Winkler (CFO)｜customer：積壓訂單季減部分來自英國內政部營收認列（原話："recognition for the U.K. Home Office."）
- 2026-08-05｜Gregory Brown (CEO)｜competition：Silvus 成長來自市占而非 TAM 擴張（原話："it's more share-driven actually than TAM-driven"）
- 2026-08-05｜Gregory Brown (CEO)｜competition：描述上述 SPX 勝案為競爭對手替換（原話："And those successes were competitive flips."）
- 2026-08-05｜John Molloy (COO)｜competition：DHS 無人機合約中僅 D-Fend 提供網路接管緩解（原話："only one, D-Fend, that actually provides cyber"）
- 2026-08-05｜Gregory Brown (CEO)｜competition：MSI 稱記憶體採購下仍持續供貨、提前囤庫存（原話："We were thoughtful about getting ahead of memory"）

### 問答異常語氣（迴避／改口／保留）
- MSI_Q2_2026_Earnings_Call_20260805.md｜問：Tindle：產品積壓訂單季減、下半年卻隱含產品成長加速，投資人漏看什麼？｜答法：Greg 轉向年增與轉換速度，未解釋季減；僅表示預期年底產品積壓高於去年，未給數字
- MSI_Q2_2026_Earnings_Call_20260805.md｜問：Zilberman：APX NEXT 占公共安全出貨比重（先前約 25%）有無更新？｜答法：未給更新數字，改談 D-Series、UHF 與轉換
- MSI_Q2_2026_Earnings_Call_20260805.md｜問：Spinola：LMR 中期有無加速成長的驅動因素｜答法：回覆集中於下半年排程與產品週期，未提中期成長率
- MSI_Q2_2026_Earnings_Call_20260805.md｜問：Cardoso：Q4 隱含營收明顯加速，驅動為何｜答法：談 Q2 超預期與 D-Series 出貨驗收，未給 Q4 具體數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 2 | 1 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 2 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 4 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"LMR 公安市場結構壟斷地位維持，backlog 持續擴張","columns":{"2Y 驗證點":"FY26 backlog 維持 +10% YoY（或 ≥ B 絕對水平）","5Y 驗證點":"FY30 LMR 美國市佔仍 ≥ 55%；P25 標準未被取代","10Y 驗證點":"FY35 仍為西方公安 LMR 主導供應商；TAM 達 0B","具體數字門檻":"Backlog YoY 連 2 季","信息來源":"10-K / 每季 earnings call backlog disclosure / G&M Insights LMR market reports","漂移觸發":"2Y 假設：連 2 季 TTM backlog growth 偏離 ≥ 5%（QC-34/35）"}},{"id":"H2","text":"Software & Services 加速至 +18% 為新常態，至 2028 占比達 45%+，推動 margin 結構性 re-rate","columns":{"2Y 驗證點":"FY26/27 S&S 收入 YoY ≥ +15%；S&S 收入占比 ≥ 40%","5Y 驗證點":"FY30 S&S 占比 ≥ 48%；ARR 突破 .5B","10Y 驗證點":"FY35 訂閱型 + 經常性收入占比 ≥ 60%","具體數字門檻":"S&S YoY 連 2 季","信息來源":"每季財報 segment disclosure / earnings call 中 ARR 揭露","漂移觸發":"5Y 假設：連 4 季 TTM 偏離 ≥ 5%（QC-35）"}},{"id":"H3","text":"Silvus 收購成功整合，2027/2028 earnout 全額（M）達成，新增 +-1B 軍用通訊年收入","columns":{"2Y 驗證點":"FY26 Silvus 完成基本整合，year-1 revenue 達 ~M（管理層 guide）","5Y 驗證點":"FY28 Silvus 累計 600M earnout 全達成；MANET 軍用收入 達 0M+","10Y 驗證點":"FY30 國防通訊段 達 .5B + 帶動 margin 至 30%+","具體數字門檻":"FY27 earnout 達成","信息來源":"每季 earnings call M&A integration disclosure / Fitch Rating reaffirmation","漂移觸發":"5Y 假設：跨年度持續未達 milestone（QC-35）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"美國地方政府公安預算同比下調 → Products 段（占 57%）持續疲軟，2Q 26 P&SI 增速 +1% 已是警訊","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Products & SI YoY 成長率 + 北美收入占比","警戒閾值":"P&SI YoY 連 2 季"}},{"id":"R2","text":"UK Airwave 模式擴散：美國州/地方政府引用 CMA 案例要求 MSI 多年合約降價，Software & Services margin 結構性壓縮","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"S&S 毛利率 + 主要州政府合約 renewal 條款","警戒閾值":"S&S 毛利率連 4 季 YoY -1pp → 結構壓縮警訊；任一州合約 renewal 含「年度價格調降」條款 → R2 觸發 50%"}},{"id":"R3","text":"Silvus 整合失敗 — 2027/2028 earnout 觸發率","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"每季 earnings call Silvus 收入 disclosure + Fitch BBB rating watch","警戒閾值":"2027 earnout 部分達成（即"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"🟠","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":404.08,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MSI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Motorola Solutions"},"oneliner":"公安無線電基本盤加上 Silvus 與 D-Fend 兩條新線，訂單與利潤率都在走高，但 Q3 扣除併購只成長約 5%，現價約 29 倍已計入 2027 年的好消息，不追價，等回到 455 美元以下。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺美國州與地方政府及各國公安機關的錢，錢卡在專網基礎建設、無線電換機與其後長達十年的服務合約；Q3 兩大分部營益率都超過 31%。","reasoning":"分部以 Q3 分部營益與營益率回推（法說 2026-11-04，CFO）：產品與系統整合約 21.2 億美元，占 63%，營益率 31.7%；軟體與服務約 12.6 億美元，占 37%，營益率 33.8%。全公司 TTM 毛利率 52.18%，Q3 Non-GAAP 營益率 32.5%。客戶面，美國政府只占 2025 年營收約 8%，沒有單一客戶超過 10%；政府業務多數來自州與地方，資金來自地方稅與 911 費，1,300 個 P25 網路是基本盤（COO，2026-11-04）。產業時鐘判 II 擴張：Q3 訂單年增逾 20%，backlog 166 億美元年增 14%，D-Series 是 12 年來首次基礎建設更新（CEO，2026-08-05），COO 稱延續到 2030 年代。供需判斷：公安部分結構性持久，Silvus 部分帶週期性，無人系統與烏克蘭相關需求可能反轉。單點依賴：部分零組件單一來源，多數產品由墨西哥與馬來西亞代工，屬集中度風險。Q3 標題成長要看成色：營收增加 3.67 億美元，併購貢獻 2.11 億、匯率 0.11 億，扣除後約 5%；產品與系統整合扣除併購只有約 2.7%。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_non_gaap_operating_earni","f_kpi6_backlog","f_peer_msi_gross_margin_pct"],"verdict_values":{"revenue_quality":"軟體與服務 Q3 占 37%，新簽合約多為 6 至 10 年；該分部 backlog 年增 14 億美元，高於產品的 6.35 億美元，能見度高。","unit_econ_note":"基礎建設不到 LMR 的四分之一（CFO，2026-08-05），更新時連帶簽長約服務，CEO 稱新約加入資安與軟體方案；單一網路的經濟數字事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"毛利率由 FY2022 的 46.4% 升到 TTM 52.2%，FY2025 自由現金流為淨利 1.19 倍，無客戶超過 10%。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：公安預算與地方稅、911 費綁定，CEO 於 2026-11-04 稱跨政黨都優先，DHS 資金到 2029 年；Silvus 需求偏週期，單獨打折。","bargaining":{"up":"記憶體漲價由供應商主導，公司付更高價並選擇性轉嫁；單一來源料件議價力弱。","down":"公安客戶更換成本高，但政府採購與英國 CMA 費率管制設了上限。","geo":"墨西哥、馬來西亞代工與稀土限制是地緣曝險。"},"profit_pool_dir":"往軟體、影像與指揮中心移動，五年利潤池數字事實表未涵蓋。","tam_table":[{"item":"可服務市場（管理層口徑）","value":"接近 1,000 億美元（CEO，2026-11-04），無第三方驗證"},{"item":"滲透率","value":"FY2026 財測營收 130.5 億美元，約 13%"},{"item":"美國第一線人員","value":"約 200 萬人；APX NEXT 應用程式用戶 2026 年底約 30 萬，約 15%"},{"item":"分段 CAGR 與營業利益池占比","value":"事實表未涵蓋，無法判斷利潤池是否流出"}]}}},"q2_moat":{"verdict":"護城河穩定：專網安裝基礎與生態綁定守住基本盤，新線的優勢還要時間驗證。","reasoning":"機制是 1,300 個 P25 網路的安裝基礎、十年級服務合約，加上裝置、影像、指揮中心用 Assist 串起來的工作流程。可比軸：TTM 營益率 MSI 25.42%，對 TDY 20.0%、ZBRA 16.53%、LHX 10.69%、AXON 0.74%；毛利率 52.18% 僅低於 AXON 的 59.41%。同業歷史利潤率與 ROIC 事實表未涵蓋，只能看水準，無法判斷差距方向。定價面，Silvus 價格維持且上升、Assist 等級採用率接近 100% 都是管理層口述；英國 CMA 對 Airwave 的費率管制則證明定價有政治上限。執行面今年三度上修，Q3 營益率擴張 200bp，同時吸收記憶體成本。沒有份額或 ROIC 差距的第三方數字，趨勢只能判穩定，不能判擴大。當期 ROIC 無法計算，投入資本事實表未涵蓋；再投資報酬見下方欄位。","fact_refs":["f_peer_msi_gross_margin_pct","f_peer_msi_operating_margin_pct","f_peer_axon_gross_margin_pct","f_peer_axon_operating_margin_pct","f_peer_zbra_operating_margin_pct","f_peer_tdy_operating_margin_pct","f_peer_lhx_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"專網安裝基礎、長約服務與跨產品工作流程綁定，更換需以州級網路為單位決策。","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行面擴大（三度上修、Q3 營益率擴張 200bp），定價面穩定（毛利率上升，但英國費率管制設上限、記憶體只選擇性轉嫁）；合併判穩定。沒有第三方份額或同業 ROIC 差距可證擴大。","competitor_notes":[{"name":"AXON","strategy_note":"影像與指揮軟體的直接對手，研發密度 23.87% 約為 MSI 的 2.85 倍，TTM 營益率僅 0.74%，以投入換份額；份額數字事實表未涵蓋。"},{"name":"ZBRA","strategy_note":"企業行動裝置與掃描，客群不同，營益率 16.53% 僅作硬體利潤率參照。"},{"name":"TDY","strategy_note":"感測與無人系統在國防端有重疊，營益率 20.0%，不構成公安專網對手。"},{"name":"LHX","strategy_note":"列在 10-K 主要競爭者名單，TTM 毛利率 25.55%、營益率 10.69%，但屬綜合國防，口徑不完全可比。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以利潤率代替，只能看水準不能看方向。","threats":[{"level":"🟡","text":"公共行動寬頻取代 LMR，目前進展有限；公司以 APX NEXT 接 5G 與 T-Mobile 衛星，把寬頻納入自家裝置。屬架構層風險，若主要國家真的關閉公安專網就重評。","p":"10 年內 30%，5 年內約 15%","evidence_refs":["competitive_share_entrants#2","substitute_technology#0"]},{"level":"🟡","text":"新競爭者進入加快，Silvus 收購後面對新創與國防承包商；低價消耗型無人機市場擴大，公司推功能較少的 LC 機種應對。","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"影像與指揮中心的跨產品競爭。Q2 法說稱 FHP 與 KC 是翻盤案，對手份額事實表未涵蓋。","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率，周轉率待查（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是第一線員警與消防，決策者是州與地方機關，付款來自地方稅與 911 費，三角色都成立；換機時程可拖，但通訊需求不能取消。Q3 訂單年增逾 20%。"},{"item":"決策層級","level":"🟢","text":"替代要在州級網路層級決定；路易斯安那 10 年、1.39 億美元合約把無線電服務、影像與指揮中心綁在一起。流失率與續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"毛利率四年升近 6 個百分點，但記憶體由 2025 年 5,000 萬美元升到 2026 年約 1.5 億，2027 年可能再倍增，單一來源料件與代工廠分走部分議價力。"},{"item":"社會容忍度","level":"🟡","text":"政府付費的必需品，價格上限由政治決定：英國 CMA 已對 Airwave 實施費率管制且上訴失敗，州層級 ALPR 立法預期增加；美國尚未見費率管制。"}],"roiic":"資料缺口：事實表未涵蓋投入資本與 Silvus 收購金額，無法算整體增量報酬。可算的只有 D-Fend：淨付 13 億美元，FY2027 營收約 2.68 億，假設營益率 33%、稅率 22%，首年報酬約 5.3%。","reinvest_rate":"FY2026 僅 D-Fend 一筆約占稅後營業利益 50%（13 億 ÷〔TTM GAAP 營益率 25.42% × 130.5 億 × 78.25%〕）；資本支出減折舊與營運資金事實表未涵蓋。FY2023 至 FY2025 自由現金流累計 64.97 億美元，高於以 22% 稅率估算的稅後營業利益 62.45 億，有機業務幾乎不需再投入。","endo_ceiling":null,"formula_note":"若用下一年獲利增量除以當年再投資，再乘再投資率，得到的就是獲利預測本身，屬循環論證，因此不填數字。"}}}},"q3_growth":{"verdict":"五年後跑道寬：基本盤更新延續到 2030 年代，另有 Silvus 與 D-Fend 兩條已有營收的曲線，但成長品質要扣掉併購來看。","reasoning":"FY2026 財測營收年增 11.7%，估計併購貢獻約 6 個百分點（Q1 Silvus 2.1 億、Q2 2.3 億、Q3 併購增量 2.11 億、D-Fend 約 0.45 億），有機約 5.8%。FY2027 管理層口頭約 142.5 億美元，年增 9.2%，D-Fend 增量約 2.23 億，占 1.7 個百分點，有機約 7.5%，與管理層稱 2027 有機成長強於 2026 一致；其中 Silvus 年增 30% 貢獻 2.1 個百分點，其餘業務約 5.8%。Bell Canada 是否計入未說明。共識 EPS FY2026 至 FY2028 年化約 10.6%（Koyfin，家數事實表未涵蓋），可拆為營收約 9%、營益率年增約 0.4 個百分點貢獻約 1.2%、股數年減約 0.3%，再扣利息增加。內生天花板算不出，缺口無法量化，長期信心上限定為中，情境裡從嚴當作超過。依管理層 1,000 億美元市場口徑，以 9% 年增率達 30% 滲透約需 9.7 年。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi6_backlog","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_q4_fy2026_fy202"],"verdict_values":{"growth":{"driver_mix":"量為主、價為輔；FY2026 成長約一半靠併購，FY2027 併購占比降到約五分之一。","runway_years":9.7,"runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本與累計併購金額，無法計算；可得部分見增量報酬欄。","segments":[{"item":"產品與系統整合 Q3","value":"年增 12%，其中併購 1.69 億美元，扣除後約 2.7%"},{"item":"軟體與服務 Q3","value":"年增 13%，其中併購 4,200 萬美元，扣除後約 9.4%"},{"item":"Silvus","value":"FY2026 略高於 9 億美元，FY2027 管理層預期年增約 30%"},{"item":"D-Fend","value":"全年口徑 1.85 億美元，FY2026 併入 4,500 萬，FY2027 預期年增 40% 至 50%"},{"item":"Video","value":"2026 年雙位數成長，Q2 法說指引 11%"},{"item":"Command Center","value":"2026 年約 15%（CEO，2026-11-04）"},{"item":"區域 Q3","value":"北美 23 億美元年增 10%，國際 10 億美元年增 18%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"全年毛利率預期上升"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"無反向證據，但份額數字事實表未涵蓋"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"選擇性漲價後未見銷量下滑"},{"signal":"EPS CAGR 高於營收 CAGR 逾 5 個百分點","lit":true,"note":"FY2022 至 FY2025 GAAP 稀釋 EPS 年化 17.1%，營收 8.6%，差 8.5 個百分點；扣除 2025 年 Hytera 回收 1.57 億美元仍差約 6.3 個百分點"},{"signal":"自由現金流對淨利連 2 年低於 0.75","lit":false,"note":"FY2025 為 1.19"},{"signal":"SBC 占營收逾 5% 且上升","lit":false,"note":"Q3 約 3.1%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"寬頻替代目前進展有限"},{"signal":"產業估值倍數 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"signal":"維護性資本支出占自由現金流逾 60%","lit":false,"note":"Q3 全部資本支出 7,300 萬美元，占自由現金流約 12%"},{"signal":"停止投資新產能且營收下滑","lit":false,"note":"正在擴充 Silvus 產能"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置方向正確但證據不齊：股本沒有被稀釋，現金轉換佳，兩筆大併購的報酬還看不出來，回購在高價位明顯縮手。","reasoning":"FY2025 自由現金流對淨利 1.19 倍，TTM 自由現金流利潤率 20.11%。SBC 以 Q3 GAAP 營益 7.77 億乘 13.3% 約 1.03 億美元，占營收約 3.1%。Q3 現金去向：股利 2 億美元、回購 9,400 萬、資本支出 7,300 萬；D-Fend 淨付 13 億美元，8 月新發 9.5 億美元長債。近三年四分法去向與債務到期結構事實表未涵蓋。淨負債 98.91 億美元，CFO 預期年底淨負債對 EBITDA 約 2 倍。年初至今營運現金流約 16 億美元，全年財測 30.5 億，代表 Q4 要貢獻約 14.5 億。計分三項只有股本稀釋能確認通過，併購報酬與回購收益率都是資料缺口。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc_gaap","f_kpi2_gaap_operating_earnings_","f_net_debt_m","f_peer_msi_fcf_margin_pct","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Silvus 收購金額事實表未涵蓋，FY2026 營收略高於 9 億美元，CEO 稱高於商業計畫，Q3 認列 earn-out 增加 8,700 萬美元；D-Fend 淨付 13 億美元，假設營益率 33%、稅率 22%，FY2027 報酬約 5.3%，尚未到可評斷期。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"Q2 回購均價 413.53 美元，以 FY2026 財測中點 17.965 美元算盈餘殖利率約 4.3%；十年期公債殖利率事實表未涵蓋，無法比對門檻。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數由 FY2022 約 171.9 百萬股（淨利 ÷ 稀釋 EPS）降到 FY2026 指引約 168 百萬股，年均約 −0.6%。"}]},"governance":{"capital_returns":[{"item":"Q3 現金股利","value":"2 億美元"},{"item":"Q3 回購","value":"9,400 萬美元"},{"item":"Q2 回購均價","value":"413.53 美元"},{"item":"Q3 資本支出","value":"7,300 萬美元"},{"item":"D-Fend","value":"淨付 13 億美元，2026 年下半年完成"},{"item":"新發長債","value":"2026 年 8 月 9.5 億美元，另再融資 Silvus 定期貸款 3 億美元"},{"item":"回購授權","value":"2026-09-09 增加 20 億美元，累計 200 億美元"},{"item":"近三年現金去向四分","value":"事實表未涵蓋"}]}}},"q5_valuation":{"verdict":"現價要求 FY2031 前 EPS 年增約 10% 且倍數只小幅下修；我相信獲利，不認為這個價位還有足夠補償。","reasoning":"現價 514.51 美元，以 FY2026 財測中點 17.965 美元算約 28.6 倍，以共識 17.73 美元算 29.02 倍，以 FY2027 共識 19.43 美元算 26.48 倍。共識快照在法說後幾乎未動（FY1 僅修正 0.06%），三年成長率以 FY2026 至 FY2028 共識算約 10.6%，PEG 2.74，高於 2 倍的貴價線。歷史位置只有 4 個年度端點：trailing P/E 分位 60.4，P/S 83.2，EV/S 98.4，五年分位事實表未涵蓋，故留空。P/E 在中段而銷售倍數在高點，反映利潤率已大幅提升，倍數能否守住取決於利潤率。Base 情境終端 25 倍，年化約 8%，全靠 EPS 複利，倍數貢獻為負。賣方目標價多取自 8 月，均值約 507 美元，區間 450 至 530 美元，FactSet 527 美元，都早於 Q3，參考性低；方向上接近現價，不支持追高，全距比遠低於 2.5 倍。同業前瞻本益比事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_week26_return_pct","f_kpi5_guidance_q4_fy2026_fy202"],"verdict_values":{"valuation":{"basis":"Non-GAAP FY2026 前瞻本益比搭配 PEG，以品質複利股的盈餘倍數為主尺。","tier":"品質複利","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業前瞻本益比，無法做倍數對照。"},"fwd_pe":29.02,"peg":2.74,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026 約 28.6 至 29 倍、PEG 2.74、短期上行約 4%、Base 年化約 8%。偏貴但未到最貴一檔：盈餘口徑年度端點分位 60.4，Base 不需要倍數上升也有約 8%。股價再漲約 10% 而 EPS 未上修，就進最貴一檔。","upside_short_pct":3.9,"upside_mid_pct":22.8,"denominator_disputed":false,"denominator_note":"FY2026 有三個 Non-GAAP 分母：共識 17.73、財測中點 17.965、扣除 IEEPA 退款後約 17.62，倍數落在 28.6 至 29.2 倍，差距約 2%，不影響結論。計入 SBC（Q3 年化每股約 1.92 美元）約 32 倍；GAAP trailing 41.39 倍含 Silvus earn-out 等費用。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把併購與一次性利益算成內生動能，以及把 29 倍當成新常態。","reasoning":"歷史最大回撤事實表未涵蓋，下行幅度改用均線與倍數推算。Q2 法說有四項未正面回答：產品 backlog 季減、APX NEXT 出貨占比、LMR 中期成長、Q4 加速來源。第一項已由實績回答，Q3 產品 backlog 季增 4.54 億美元；第二項仍無數字；第三項在 Q3 又以 2 月再談帶過（CEO，回答 Zilberman）；第四項在 Q3 又被問（Niknam），CEO 以審慎帶過。訂單增速有三種說法：開場逾 20%、問答稱整體 25%、CFO 稱 25% 是產品訂單，本文只採逾 20%。IEEPA 退款也有三個數字：Q2 法說 6,000 萬、10-Q 約 7,000 萬、Q3 法說約 7,500 萬美元，本文用 7,500 萬。Bell Canada 由 Q4 延到 2027 年 Q1 或 Q2，原因是客戶與監管核准。十類衰退信號亮一類，RSI 標記不可用，未納入動能判斷。","fact_refs":["f_price_at_dd","f_ma_w52","f_ma_w104","f_ma_w250","f_week26_return_pct","f_kpi7_non_gaap_diluted_eps","f_kpi5_guidance_q4_fy2026_fy202"],"verdict_values":{"trap":{"verdict":"🟡","label":"價值陷阱機率低，主要風險是高倍數回落，而非生意變壞；十類衰退信號亮一類。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":17.965,"pe":28.64,"basis":"FY2026 Non-GAAP EPS 財測中點（17.94 至 17.99 美元，2026-11-04），與終端倍數同為當年度口徑；Koyfin 共識 17.73 美元尚未反映上修。"},"eps":{"bull":[20.7,23.9,27.4,31.1,35.0],"base":[19.8,22.0,24.3,26.7,29.2],"bear":[18.6,18.3,18.6,19.0,19.4]},"pe":{"bull":30,"base":25,"bear":19},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.941,"net_buyback":0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":8.5},"max_dd":{"lo":-42,"hi":-30,"basis":"歷史最大回撤事實表未涵蓋，改用價位與倍數推：跌回 250 週均線 347.75 美元為 −32.4%；FY2026 財測中點乘 19 倍為 341 美元，−33.7%；扣除 IEEPA 退款的 17.62 美元乘 17 倍為 300 美元，−41.8%。淺端取 −30%，深端取 −42%。","trigger_time":null},"basis":{"bull":"Silvus 連年 25% 以上、D-Fend 放量、D-Series 加速，FY2027 營收約 146 億美元、營益率年增 100bp 以上，後段 EPS 年增 12% 至 15%；30 倍略高於現值，靠持續雙位數成長支撐。事實表未涵蓋同業前瞻本益比，無同業對照。","base":"FY2027 營收 142.5 億美元（管理層口頭）、營益率年增約 40bp，EPS 19.8 美元；之後營收年增 7% 至 8%、營益率年增 20 至 40bp、股數年減約 0.3%。終端 25 倍為現值 28.6 倍下修約 13%，事實表未涵蓋同業前瞻本益比，無同業對照。淨回購殖利率填 0，因股數減少已計入 EPS。","bear":"Silvus 需求回落、LMR 更新遞延、記憶體成本轉嫁失敗，FY2028 EPS 回落，FY2031 僅 19.4 美元；19 倍對應成長熄火至 5% 以下，較現值下修約 34%。機率 30% 部分來自內生上限算不出而從嚴處理，單看基本面約 25%。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 營收增量扣除併購與匯率後約 5%，產品與系統整合扣除併購約 2.7%；Silvus 隱含 Q4 約 1.6 億美元，低於 Q3 近 3 億；10-K 列明寬頻替代與新競爭者。","assumption":"FY2027 有機成長加速到約 7.5%，靠 LMR 在 Q4 的強勁雙位數與 Silvus 再成長 30% 接力。","consequence":"EPS 停在 19 美元且倍數掉到 13 倍才會腰斬；較可能的壞結果是 370 美元上下，跌約 28%。","ruling":"部分採納：backlog 166 億美元與訂單年增逾 20% 反駁近端失敗，但 Q3 有機成長偏低屬實，已納入 Bear 機率與不追價結論。","watch":"FY2026 Q4 LMR 成長與 FY2027 財測的有機成長口徑。","evidence_refs":["competitive_share_entrants#2","substitute_technology#0","competitive_share_entrants#1"],"fact_refs":["f_kpi0_net_sales_gaap","f_kpi6_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"D-Fend 淨付 13 億美元，FY2027 營收約 2.68 億，首年稅後報酬約 5%；8 月新發 9.5 億美元債，Q3 回購僅 9,400 萬美元；Silvus earn-out 增加 8,700 萬美元，Non-GAAP 全部排除。","assumption":"併購標的長大後報酬高於資金成本，且 Non-GAAP 能代表股東實得。","consequence":"營收與 Non-GAAP EPS 都達標，但 GAAP 獲利與每股自由現金流落後；Q3 SBC 年化每股約 1.92 美元，計入後 FY2026 約 32 倍。","ruling":"採納，資本配置只給到資料允許的程度，估值同時看含 SBC 的倍數。","watch":"GAAP 與 Non-GAAP EPS 差距、年底淨負債對 EBITDA 約 2 倍的承諾、Silvus 併滿週年後揭露是否減少。","evidence_refs":[],"fact_refs":["f_kpi4_sbc_gaap","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"記憶體直接成本由 2025 年 5,000 萬美元升到 2026 年約 1.5 億，CEO 稱 2027 年可能倍增；IEEPA 退款約 7,500 萬美元不再有；部分料件單一來源，代工集中在墨西哥與馬來西亞，庫存預期維持高檔。","assumption":"營運槓桿與選擇性漲價蓋過約 158bp 的成本逆風。","consequence":"每 100bp 營益率約 0.66 美元 EPS，占 FY2027 約 3.4%，且會牽動倍數。","ruling":"部分採納：管理層兩度承諾 2027 年營益率擴張，但沒有給數字，因此列為唯一致命點。","watch":"每季毛利率年變化與記憶體成本揭露。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"],"fact_refs":["f_kpi5_guidance_q4_fy2026_fy202"]},{"view":"價格已反映太多","evidence":"FY2026 約 29 倍，PEG 2.74，26 週上漲 34.74%；自前份以來股價上漲 27%、財測 EPS 上升約 6%，約四分之三來自倍數；FY2027 共識營收已等於管理層口頭的 142.5 億美元。","assumption":"29 倍能維持，且 EPS 上修足以吸收。","consequence":"Base 年化約 8%，倍數回到 25 倍以下時全靠 EPS 硬撐。","ruling":"採納，這是不追價的主因。","watch":"股價相對 455 美元，FY2027 共識 EPS 上修幅度。","evidence_refs":[],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 404.08 → 本次 514.51（+27.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=404.08","side_b":"本次 price_at_dd=514.51","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 404.08 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 404.08 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 404.08 美元：Bull 價 1,050、Bear 價 368.6，五年期望值 +73.6%，基準年化 12.6%，不對稱比 15.17","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 15.17。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 404.08 美元：五年期望值 +73.6%，基準年化 12.6%，不對稱比 15.17","side_b":"本次情境、股價 514.51 美元：五年期望值 +36.4%，基準年化 7.2%，不對稱比 3.06","ruling":"再換股價、情境不動：起點價上漲 27.3%，五年期望值少 37.3 個百分點，基準年化少 5.3 個百分點，不對稱比由 15.17 降到 3.06。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"Q3 超預期與全年上修不成比例","cause":"新證據","prior_field":null,"side_a":"管理層：Q4 將是史上最強，指引只是審慎（CEO，2026-11-04）。","side_b":"Q3 營收 33.76 億美元，高於原指引約 32.5 億，多出約 1.26 億；全年指引只升 7,500 萬，其中 D-Fend 貢獻 4,500 萬。扣除後全年只升 3,000 萬，隱含 Q4 下調約 9,600 萬，CEO 未回答是否有提前認列。","ruling":"可調和，偏向部分提前認列加上保守。提前認列或審慎的說法不採信也不否定，標示未證。","evidence_level":"公司指引與法說口述，需 Q4 實績驗證","settle_metric":"2027 年 2 月公布的 Q4 營收年增率，對照 13% 指引","if_then":["若 Q4 營收年增高於 14%，判定審慎屬實，仍不追價，上調 FY2027 EPS 基準後重算買點。","若 Q4 營收年增低於 12%，判定 Q3 提前認列，停止加碼並維持 Bear 機率 30%。"],"evidence_refs":[]},{"axis":"雙位數成長與有機成長","cause":"新證據","prior_field":null,"side_a":"管理層：兩大分部都雙位數成長。","side_b":"Q3 扣除併購與匯率約 5%，產品與系統整合扣除併購約 2.7%，軟體與服務約 9.4%。","ruling":"可調和，標題數字正確但成色不同；FY2027 有機約 7.5% 要靠 Q4 起的 LMR 加速與 Silvus，尚未發生。","evidence_level":"8-K、10-Q 與法說","settle_metric":"FY2027 財測的有機成長率，門檻 7%","if_then":["若 FY2027 有機成長指引不低於 7%，維持 Base。","若低於 5%，把 FY2027 EPS 下修到 19 美元並停止加碼。"],"evidence_refs":[]},{"axis":"Silvus 需求強勁與競爭升溫","cause":"新證據","prior_field":null,"side_a":"CEO：價格維持且上升，未見需求放緩，FY2027 年增約 30%，繼續拿份額。","side_b":"10-K 指新創與國防承包商競爭加劇；隱含 Q4 約 1.6 億美元；美國國防多在測試階段；為低價市場推出功能較少的 LC。","ruling":"可調和：短期有訂單與擴產支持，長期定價未證，以 FY2027 年增 20% 為檢驗線。","evidence_level":"管理層口述為主，缺第三方份額數字","settle_metric":"FY2027 Silvus 年增率","if_then":["若 FY2027 年增不低於 20%，維持第二曲線假設。","若低於 10%，視為失速並減碼。"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"backlog 166 億美元、FY2027 營收能見度高，有機加速、營益率擴張、Silvus 再成長 30%；共識 19.43 美元落後，我估 19.8 美元，好生意不該等便宜。","side_b":"Base 年化約 8%，短期上行約 4%；記憶體 2027 年可能倍增的訊息 11 月才出現，尚未確認進入共識，下一個驗證點在 2 月。","ruling":"選不追價，綁定限制是價格，455 美元以下 Base 年化約 11%。","evidence_level":"情境計算與法說","settle_metric":"股價相對 455 美元，以及 2027 年 2 月 FY2027 EPS 指引","if_then":["價格先走、證據未到：股價漲破 600 美元而 FY2027 EPS 指引未達 20.5 美元，不追。","跌破 455 美元且 backlog 年增仍不低於 8%，分批反買第一批。","股價未跌但 FY2027 EPS 指引不低於 20.5 美元，重算買點，門檻同比例上調。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：10-K 稱競爭者增加、進入速度加快，Silvus 面對新創與國防承包商，但沒有份額流失的數字。","side_b":"結構：D-Series 更新到 2030 年代，無人系統與反無人機帶來新需求，公安預算穩定；其他變數是 CMA 費率管制、記憶體、關稅與 ALPR 立法。","ruling":"結構性轉好中；競爭軸目前只有文字揭露沒有數字，記憶體與監管是要盯的其他變數。","evidence_level":"10-K 與法說","settle_metric":"backlog 年增與毛利率年變化","if_then":["若 backlog 年增連 2 季低於 5%，改判需求見頂或競爭惡化，停止加碼。"],"evidence_refs":["competitive_share_entrants#0","reg_tariff_export#0","regulatory_antitrust#2"]},{"axis":"前份地方預算風險降位","cause":"新證據","prior_field":null,"side_a":"前份門檻：P&SI YoY 連 2 季偏弱，當時增速 +1%。","side_b":"Q3 P&SI 年增 12%，扣除併購約 2.7%；地方預算未見收縮，CEO 稱 DHS 資金到 2029 年。","ruling":"降位保留：指標改為扣除併購後年增，門檻為連 2 季低於 0%，資料來自 10-Q。","evidence_level":"10-Q 與法說","settle_metric":"產品與系統整合扣除併購後年增","if_then":["若連 2 季低於 0%，停止加碼並重看 LMR 更新假設。"],"evidence_refs":[]},{"axis":"前份軟體服務成長假設下修","cause":"新證據","prior_field":null,"side_a":"Software & Services 加速至 +18% 為新常態，FY26/27 年增 ≥ +15%。","side_b":"Q3 軟體與服務年增 13%，扣除併購約 9.4%；本次門檻改為年增不低於 10%。","ruling":"前份門檻未達，下修並併入營益率假設。","evidence_level":"8-K 與法說","settle_metric":"軟體與服務年增率","if_then":["若連 2 季低於 10%，停止加碼。"],"evidence_refs":[]},{"axis":"前份 Silvus 整合風險換軌","cause":"新證據","prior_field":null,"side_a":"前份門檻：2027 earnout 部分達成視為整合失敗。","side_b":"Silvus FY2026 略高於 9 億美元，CEO 稱高於商業計畫，Q3 認列 earn-out 增加 8,700 萬美元；風險由整合失敗轉為週期與競爭。","ruling":"門檻更換：不再看 earn-out，改看 FY2027 年增 20%。","evidence_level":"法說","settle_metric":"FY2027 Silvus 年增率","if_then":["若 FY2027 年增低於 10%，減碼。"],"evidence_refs":[]},{"axis":"估值結論與情境機率","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 404.08 美元，當時財測中點 16.93 美元，約 23.9 倍，結論偏貴。","side_b":"本次股價 514.51 美元，財測中點 17.965 美元，約 28.6 倍；股價上漲 27%，約四分之三來自倍數。","ruling":"仍在偏貴一檔，但已接近最貴一檔；前份未留機率與最大回撤數值，本次新設。","evidence_level":"事實表價格與公司財測","settle_metric":"FY2026 本益比","if_then":["若股價再漲約 10% 而 EPS 未上修，改列最貴一檔，不追。"],"evidence_refs":[]},{"axis":"整體評級","cause":"新證據","prior_field":["signal"],"side_a":"前份評級 B。","side_b":"本次維持 B：基本面較前份強（三度上修、backlog 166 億美元），但改善已被價格吸收。","ruling":"維持，不因基本面改善而升級。","evidence_level":"財報與法說","settle_metric":"Base 年化報酬是否高於 11%","if_then":["若股價回到 455 美元以下，重跑研究再決定是否升級。"],"evidence_refs":[]},{"axis":"價值陷阱結論","cause":"方法變動","prior_field":["trap"],"side_a":"前份為低風險。","side_b":"本次逐項清點十類衰退信號，EPS 與營收成長差距亮燈一類，結論改為黃。","ruling":"生意未變壞，變動來自檢查項目更完整。","evidence_level":"年度財務歷史","settle_metric":"亮燈類別數","if_then":["若亮燈達 3 類，改列紅並停止加碼。"],"evidence_refs":[]},{"axis":"前份空白欄位首次給值","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份這六欄為空。","side_b":"本次首次給出護城河趨勢、五年後跑道、公司類型與循環位置；裁決與角色由程式得出。","ruling":"屬框架補齊，不代表基本面轉向。","evidence_level":"本次研究","settle_metric":"下次研究對帳","if_then":["若下次任一欄轉差，須指名對應證據後才可調整倉位。"],"evidence_refs":[]},{"axis":"行動門檻新設：重新進場、減碼與清倉","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重新進場條件與停損指標皆為空。","side_b":"重新進場：股價 455 美元以下。減碼：毛利率連 2 季年減、或 Silvus FY2027 年增低於 10%。清倉：美國人口前十大州任一宣布關閉 P25 改採公共寬頻。","ruling":"新設門檻，取代前份只有觀察指標沒有動作的寫法。","evidence_level":"本次研究","settle_metric":"各門檻指標","if_then":["觸發減碼或清倉條件時，依條件動作，不再等下一次研究。"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":null,"side_a":"前份未設唯一致命點（欄位為空）。","side_b":"2027 年 2 月法說給出的 FY2027 全年 Non-GAAP 營益率指引低於 FY2026，管理層 11 月承諾的擴張落空。","ruling":"Single Thing 新設，選營益率是因為它同時影響 EPS 與倍數，敏感度最大。","evidence_level":"法說","settle_metric":"FY2027 營益率指引","if_then":["若指引低於 FY2026，取消建倉計畫；已持有則減碼一半。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 455 美元以下，Base 年化約 11%，才開始第一批建倉。","type":"估值rearm","maps_to":"H1、H2、H3","metric":"MSI 收盤價","threshold":"≤ 455 美元","action":"分批反買第一批，建倉前重跑一次研究","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"FY2027 全年 Non-GAAP 營益率指引低於 FY2026。","type":"Single Thing","maps_to":"H3","metric":"FY2027 Non-GAAP 營益率指引相對 FY2026","threshold":"指引低於 FY2026 實績","action":"未持有則取消建倉計畫，已持有減碼一半","source_freq":"2027 年 2 月法說，一次性","date":"2027-02","evidence_refs":[]},{"n":3,"text":"backlog 年增連 2 季低於 5%，換機週期假設削弱。","type":"假設驗證","maps_to":"H1","metric":"期末 backlog 年增率","threshold":"連 2 季 < 5%","action":"停止加碼","source_freq":"每季 8-K","date":null,"evidence_refs":[]},{"n":4,"text":"Silvus FY2027 年增低於 20%，第二曲線假設削弱；若公司停止揭露，改看 MCN 分部並標資料缺口。","type":"假設驗證","maps_to":"H2","metric":"Silvus 年增率","threshold":"FY2027 < 20%","action":"停止加碼","source_freq":"每季法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":5,"text":"毛利率連 2 季年減，代表記憶體與關稅吸收失敗。","type":"風險","maps_to":"R1","metric":"毛利率年變化","threshold":"連 2 季年減","action":"減碼","source_freq":"每季 8-K","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0"]},{"n":6,"text":"軟體與服務營益率持續下滑，或美國州合約出現年度調降條款，代表英國費率管制模式擴散。","type":"風險","maps_to":"R4","metric":"軟體與服務營益率；州合約續約條款","threshold":"連 4 季年減 ≥ 100bp，或任一州合約含年度調降條款","action":"減碼","source_freq":"每季 8-K 與合約新聞","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":7,"text":"產品與系統整合扣除併購後連 2 季負成長，地方預算風險重新啟動。","type":"風險","maps_to":"H1","metric":"產品與系統整合扣除併購後年增","threshold":"連 2 季 < 0%","action":"停止加碼","source_freq":"每季 10-Q","date":null,"evidence_refs":[]},{"n":8,"text":"股價跌到 400 美元以下而 backlog 仍成長，屬價格先走、基本面無損。","type":"加碼","maps_to":"H1","metric":"收盤價與 backlog 年增","threshold":"≤ 400 美元且 backlog 年增 ≥ 8%","action":"分批反買第二批","source_freq":"每日收盤與每季 8-K","date":null,"evidence_refs":[]},{"n":9,"text":"股價達 FY2027 EPS 約 35 倍時，已超過自身合理上緣。","type":"減碼","maps_to":"H3","metric":"收盤價","threshold":"≥ 690 美元","action":"減碼","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":10,"text":"美國主要州宣布關閉 P25 改採公共寬頻，架構替代成真。","type":"清倉","maps_to":"R3","metric":"州級專網政策","threshold":"美國人口前十大州任一宣布","action":"清倉","source_freq":"事件","date":null,"evidence_refs":["substitute_technology#0","competitive_share_entrants#2"]},{"n":11,"text":"FY2026 Q4 財報與 FY2027 財測公布後一週內複審。","type":"複審日期","maps_to":"H1、H2、H3","metric":"FY2027 財測","threshold":"財報公布","action":"重跑研究","source_freq":"一次性","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"期末 backlog 年增率","bear_threshold":"連 2 季低於 5%","window":"2 季","source":"每季 8-K 新聞稿","last_status":"ok"},{"metric":"FY2027 Non-GAAP 營益率相對 FY2026","bear_threshold":"全年指引或實績低於 FY2026","window":"2027-02 至 2028-02","source":"法說與 8-K","last_status":"unknown"},{"metric":"Silvus 年增率","bear_threshold":"FY2027 低於 20%，低於 10% 視為失速","window":"FY2027","source":"每季法說口述","last_status":"ok"},{"metric":"產品與系統整合扣除併購後年增","bear_threshold":"連 2 季低於 0%","window":"2 季","source":"10-Q 分部說明","last_status":"warning"},{"metric":"軟體與服務營益率","bear_threshold":"連 4 季年減 100bp 以上","window":"4 季","source":"每季 8-K 新聞稿","last_status":"ok"},{"metric":"毛利率年變化","bear_threshold":"連 2 季年減","window":"2 季","source":"每季 8-K 新聞稿","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回到 455 美元以下（Base 年化約 11%）；門檻隨 FY2031 Base EPS 上修同比例調整","exec_line":"現價不追。到 455 美元以下先建第一批並重跑研究；到 400 美元以下且 backlog 年增仍不低於 8% 再加第二批。記憶體倍增的訊息 11 月才出現，2027 年 2 月財測前不加碼。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 455 美元以下","qc48_result":"pass","qc48_note":"Bull 路徑只有 FY2027 有分部算術，其後年份靠成長率假設，跑道依據是管理層自己的 1,000 億美元市場口徑，沒有第三方佐證；也沒有查到可比案例能證明或否定 +15.3% 年化，所以這個 Bull 依據有一部分站得住，但不能當成已驗證的數倍成長依據。"},"thesis":{"H":[{"id":"H1","text":"公安無線電基本盤靠 D-Series 基礎建設與 APX NEXT 換機延長週期，帶動 backlog 持續年增。","2y":"FY2027 第三季 backlog 年增不低於 8%，達 179 億美元以上。","5y":"FY2031 P25 在美國公安仍為主流，MCN 年增維持中單位數。","10y":"FY2036 美國與歐洲公安專網未被公共寬頻全面取代。","threshold":"期末 backlog 年增不低於 8%；FY2026 Q3 為 14%。","source":"每季 8-K 新聞稿與法說 backlog 揭露。","drift_rule":"2 年期假設：連 2 季偏離門檻達 5% 視為削弱，連 3 季偏離達 10% 視為反轉。"},{"id":"H2","text":"Silvus 與 D-Fend 成為有營收的第二曲線，補上 LMR 成熟後的成長缺口。","2y":"FY2027 Silvus 營收不低於 10.8 億美元，D-Fend 不低於 2.5 億美元。","5y":"FY2031 兩者合計營收不低於 25 億美元。","10y":"FY2036 國防與反無人機占營收不低於 15%。","threshold":"FY2027 Silvus 年增不低於 20%，管理層口徑約 30%。","source":"每季法說口述；Silvus 併滿週年後揭露可能變少，若停止揭露改看 MCN 分部成長並標資料缺口。","drift_rule":"2 年期假設：連 2 季偏離門檻達 5% 視為削弱，連 3 季偏離達 10% 視為反轉；5 年期假設：連 4 季偏離達 5% 視為削弱，連 6 季偏離達 10% 視為反轉。"},{"id":"H3","text":"營運槓桿與軟體加值蓋過記憶體與一次性利益消失的逆風，營益率繼續擴張。","2y":"FY2027 Non-GAAP 營益率高於 FY2026 至少 30bp，軟體與服務年增不低於 10%。","5y":"FY2031 自由現金流利潤率不低於 24%。","10y":null,"threshold":"FY2027 Non-GAAP 營益率年變化不低於 +30bp，毛利率不得連 2 季年減。","source":"每季 8-K、法說與 10-Q。","drift_rule":"2 年期假設：連 2 季偏離門檻達 5% 視為削弱，連 3 季偏離達 10% 視為反轉。"}],"R":[{"id":"R1","text":"記憶體成本 2027 年可能再增加約 1.5 億美元，IEEPA 退款約 7,500 萬美元不再有，加上關稅、單一來源料件與代工集中，合計約 158bp 逆風。","h_ref":"H3","clock":"⚡","threshold":"毛利率連 2 季年減，或 FY2027 營益率指引低於 FY2026。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R2","text":"Silvus 是非線性業務，Q4 隱含約 1.6 億美元，低於 Q3 近 3 億；美國國防仍在測試階段，新創與國防承包商競爭加劇。","h_ref":"H2","clock":"🔥","threshold":"FY2027 年增低於 20%，或 MCN 連 2 季年增低於 5%。","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"公共寬頻、衛星或其他新技術被客戶認定足以取代 LMR，新競爭者進入加快。","h_ref":"H1","clock":"🐢","threshold":"美國人口前十大州或歐洲主要國家任一宣布關閉專網轉公共寬頻；事實表範圍內尚無案例。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0"]},{"id":"R4","text":"英國 CMA 對 Airwave 的費率管制成立且上訴失敗，Home Office 將關停目標延至 2029-12-31；若其他政府援引，軟體與服務利潤率受壓。受影響營收事實表未涵蓋。","h_ref":"H3","clock":"🔥","threshold":"軟體與服務營益率連 4 季年減達 100bp，或任一美國州合約續約含年度調降條款。","evidence_refs":["regulatory_antitrust#2"]},{"id":"R5","text":"生物辨識與車牌辨識面臨州法與 FTC 執法，預期州立法增加，影響 Video 與分析產品。受影響營收事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"Video 年增低於 5%，或人口前十大州通過禁用車牌辨識的立法。","evidence_refs":["regulatory_antitrust#1"]}],"single_thing":{"description":"2027 年 2 月法說給出的 FY2027 全年 Non-GAAP 營益率指引低於 FY2026，管理層 11 月承諾的擴張落空。","why_fatal":"現價約 28.6 倍建立在營益率連年擴張上。每 100bp 約等於 0.66 美元 EPS（142.5 億美元 × 1% × 78% ÷ 1.67 億股），更大的傷害來自倍數，擴張中斷後倍數可能退到 23 倍上下。","if_happens":"FY2027 EPS 由 19.8 美元降到約 19 美元，乘 23 倍為 437 美元，較現價約 −15%，Base 路徑要全面下修。","how_monitor":"2027 年 2 月財測，以及每季毛利率與記憶體直接成本揭露。","probability":"約 15%（12 至 24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":26.48,"peg_fy2":2.5,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":12.75,"FY2026E":17.73,"FY2027E":19.43,"FY2028E":21.69},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin Non-GAAP 共識（2026-11-07）；基期 12.75 美元是 GAAP 稀釋 EPS，事實表未涵蓋 FY2025 Non-GAAP EPS，不能拿基期與共識算成長率。FY2026E 共識 17.73 美元低於公司 11 月 4 日上調後財測 17.94 至 17.99 美元，快照尚未反映；分析師家數事實表未涵蓋。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 Q4 財報與 FY2027 正式財測","impact":"高","watch":"營益率指引是否高於 FY2026、有機成長口徑、Silvus 揭露"},{"date":"2027-Q1","date_precision":"quarter","type":"capacity","event":"Salt Lake City 廠上線","impact":"中","watch":"Silvus 交期能否低於 12 至 14 週"},{"date":"2027-Q2","date_precision":"quarter","type":"other","event":"Bell Canada LMR 服務業務交割，預期 Q1 或 Q2","impact":"低","watch":"客戶與監管核准是否再延"},{"date":"2029-12","date_precision":"month","type":"regulatory","event":"英國 Airwave 關停目標 2029-12-31","impact":"中","watch":"Home Office 是否再延，以及費率管制是否被其他政府援引"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=34.74, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 路徑只有 FY2027 有分部算術，其後年份靠成長率假設，跑道依據是管理層自己的 1,000 億美元市場口徑，沒有第三方佐證；也沒有查到可比案例能證明或否定 +15.3% 年化，所以這個 Bull 依據有一部分站得住，但不能當成已驗證的數倍成長依據。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 455 美元以下'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
