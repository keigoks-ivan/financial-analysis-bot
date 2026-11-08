你是 DD 管線 v20 的判斷層閘（gate），標的 ALAB（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（40 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝392.4 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益率＝39.1 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
- `f_kpi5_non_gaap`（q1_business）｜Non-GAAP 毛利率＝73.7 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
- `f_kpi6_non_gaap_eps`（q1_business）｜Non-GAAP EPS＝0.8 USD｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
  - 註記：consensus 0.69（來源：web_search，MarketBeat／Benzinga 2026-08-04）
- `f_kpi7_q3_fy2026`（q1_business）｜下一季指引（Q3 FY2026）＝營收 540–560M；GAAP/Non-GAAP 毛利率約 72%；Non-GAAP opex 156–160M；Non-GAAP EPS 1.16–1.21；GAAP EPS 0.87–0.92；稀釋股數約 185M 文字｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-03 date｜期間與口徑：2026-11-03／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-03）
- `f_peer_alab_gross_margin_pct`（q2_moat）｜ALAB 毛利率＝73.89 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALAB.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_alab_operating_margin_pct`（q2_moat）｜ALAB 營業利益率＝25.52 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALAB.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_alab_fcf_margin_pct`（q2_moat）｜ALAB FCF 利潤率＝22.15 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALAB.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_nvda_gross_margin_pct`（q2_moat）｜NVDA 毛利率＝74.67 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_nvda_operating_margin_pct`（q2_moat）｜NVDA 營業利益率＝65.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_gross_margin_pct`（q2_moat）｜AVGO 毛利率＝68.77 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_operating_margin_pct`（q2_moat）｜AVGO 營業利益率＝48.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_crdo_gross_margin_pct`（q2_moat）｜CRDO 毛利率＝67.07 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRDO.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_crdo_operating_margin_pct`（q2_moat）｜CRDO 營業利益率＝31.74 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRDO.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_crdo_fcf_margin_pct`（q2_moat）｜CRDO FCF 利潤率＝27.57 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRDO.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_mrvl_gross_margin_pct`（q2_moat）｜MRVL 毛利率＝52.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝4.39 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.94 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝8.61 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝2027.27 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝3353.93 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝8.93 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 4.03 → 4.39（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF，上半年累計；新聞稿無單季）＝134.2 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
- `f_kpi4_sbc`（q4_capital）｜SBC 占營收＝16.3 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001736297/000173629726000033/q226exhibit991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-1333.25 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 44.99、現金 1378.24（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝174.78 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝190.71 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝43.44 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 4.39，分子＝快照價 190.71｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝75.38 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／1 個年度端點內的分位＝50.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝15.78 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝20.56 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝21.42 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝50.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-4.54 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝29.11｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝236.29 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝178.69 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（21 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：對手可能較易取得設計導入（design wins），CXL 與 UALink 仍在早期採用，若大廠不支持同一標準或出現競爭標準，公司可能失去份額。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-20）｜affects：decision_inputs.bear、moat_trend
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Zacks 稱 Credo 在光學 DSP 持續拿下份額，Astera 同時面對 Broadcom 與 Credo 的競爭。
  - 來源：Zacks: ALAB benefits from PCIe demand, can it stay ahead of its competitors（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2025 年報揭露客戶高度集中：前三大終端客戶約占營收 86%，風險揭露稱單一終端客戶超過 2025 年營收 70%（經搜尋摘要轉述，未直接讀原文頁面）。
  - 來源：Astera Labs, Inc. Form ARS FY2025 (SEC)（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K（搜尋摘要轉述）：五家客戶各占營收 10% 以上——A 20%、B 20%、C 17%、D 16%、E 11%，合計約 84%；最大單一客戶 20%。數字來自搜尋摘要對 10-K 表格的轉述，未逐字讀頁面。
  - 來源：Astera Labs, Inc. Form 10-K FY2025 (SEC EDGAR)（as_of 2026-02-28）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2024 10-K：客戶 A 占營收 36%、B 24%、C 11%；客戶 F 占 2024 年底應收帳款 31%。
  - 來源：Astera Labs, Inc. Form 10-K FY2024 (Financial_Report, SEC EDGAR)（as_of 2025-02-28）｜affects：decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：TrendForce：2026年NAND供給短缺4-5%，2027下半年供給位元成長將超過需求成長（二手轉載）。
  - 來源：TrendForce via itiger: NAND Flash Supply Shortage Expected to Ease in Second Half of 2027（as_of 2026-07-01）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：SEMI：300mm晶圓月產能至2028年底達1110萬片，年複合成長7%；先進製程(7nm以下)CAGR 14%。
  - 來源：The Machine Maker: SEMI Projects 69% Growth in Advanced Semiconductor Capacity by 2028 Driven by AI Demand（as_of 2026-06-01）｜affects：decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Astera Labs FY2025 10-K 與年報列出出口管制風險：若被認定違反貿易制裁或出口規則，可能面臨喪失出口權及罰款；亦提及美國商務部對先進運算晶片的限制持續修訂。屬一般性風險揭露，非特定進行中調查。（內容取自搜尋摘要轉述，未讀原文頁面）
  - 來源：Astera Labs, Inc. Form 10-K FY2025 (SEC EDGAR)（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Astera FY2025 10-K 風險揭露：Chinese customers facing tariffs may build their own products or buy from competitors, and may cancel or delay orders; prolonged or expanded export restrictions would hurt revenue and results.
  - 來源：Astera Labs, Inc. Form 10-K FY2025 (SEC)（as_of 2026-02-28）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：Astera S-1 揭露：美國對部分中國客戶的銷售限制，使部分銷售可能需出口許可，且不保證獲准；並提及中國不可靠實體清單風險。
  - 來源：Astera Labs, Inc. Form S-1 (SEC)（as_of 2024-02-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K 稱半導體關稅可能降低產品需求，美國對關鍵礦物的關稅可能推高投入成本。
  - 來源：Astera Labs, Inc. Form 10-K FY2025 (SEC)（as_of 2026-02-28）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：ALAB 10-K 揭露其主要製造商台積電的晶圓廠與主要經銷商皆位於台灣
  - 來源：Astera Labs Form 10-K FY2025 (SEC)（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險揭露：若台積電無法供應足量晶圓，ALAB 出貨與營收會受損
  - 來源：Astera Labs Form 10-K FY2025 (SEC)（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2024 10-K 稱製造夥伴、經銷商與多數營收集中於台灣、中國、南韓；FY2025 年報再加入新加坡，且多數營收來自東亞
  - 來源：Astera Labs Form 10-K FY2024 / Form ARS FY2025 (SEC)，經搜尋摘要轉述（as_of 2024-12-31）｜affects：decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：IPO 招股書指出台灣地震風險因晶圓廠鄰近斷層帶而顯著，且可能無法以合理條件取得替代產能
  - 來源：Astera Labs Form 424B4 (SEC)（as_of 2024-03-20）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#4`（geo_supply_chain｜方向 -｜狀態 ok）：第三方彙整站 policyrisk.com 評 ALAB 製造曝險為高，稱約 73% 不動產及設備位於台灣，且 2025 年單一終端客戶占營收逾 70%、前三大約 86%（第三方轉述，非原始 filing 逐字）
  - 來源：policyrisk.com ALAB company profile（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：競爭風險：BofA 初始報告指出 Nvidia NVLink 與 Broadcom scale-up Ethernet 交換器的競爭可能拖累成長；Scorpio-X 對應 AWS 部署的 2026-29 年機會約 $2.5B。
  - 來源：Nasdaq/Zacks, ALAB articles citing BofA initiation（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：分析師指出 Nvidia NVLink 與 Broadcom Scale-Up Ethernet(SUE) 交換器的競爭可能拖累成長並限制估值倍數擴張；Broadcom 亦已推出 PCIe Gen 6 retimer/交換器，Marvell、Credo 為競爭者。
  - 來源：Yahoo Finance, Astera Labs Battles Nvidia And Broadcom As AI Chip Market Heats Up; ServeTheHome, Broadcom Fires a Shot at Astera Labs with New PCIe and CXL Retimers（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：公司 2026 年 10-Q 風險因素列示競爭、產業整併、依賴第三方技術及產品價格隨時間下降；搜尋未發現 2026 年有具體替代品奪取份額的報告。
  - 來源：Astera Labs Form 10-Q (period ended 2026-06-30)（as_of 2026-06-30）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：財報後股價下跌約 12%（Trefis 歸因於財報前已先漲）；Q3 躍升取決於 Scorpio X-Series 320-lane fabric switch 的單一部署時程。另有 Q3 EPS 指引 Benzinga 列 $1.16–$1.21（非GAAP），Simply Wall St 列 GAAP $0.87–$0.92，兩者口徑不一致、未能釐清。
  - 來源：Trefis 2026-08-06; Benzinga earnings-forecasts（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 指引毛利率約 73%（Q1 為 76.4%），約 200bp 下滑來自與關鍵客戶的非現金 warrant 協議（TIKR）。
  - 來源：TIKR blog（as_of 2026-07-28）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":660.0,"bear_5y_price":106.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":76.2,"ev5y_pct":82.5,"irr_base_pct":12.0,"asym_ratio":4.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":4.39,"pe":43.44,"basis":"FY2026E 共識 non-GAAP EPS，現價 190.71 除以當年度預估，與終端倍數同為當年度 EPS 分母。"},"eps":{"bull":[8.0,11.0,14.8,18.5,22.0],"base":[7.0,8.8,10.7,12.5,14.0],"bear":[5.3,4.7,5.0,5.4,5.9]},"pe":{"bull":30,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ALAB_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Desmond Lynch｜guidance：Q3營收財測區間下緣$540M（上緣$560M，中點季增40%）（原話："We expect revenue to be in the range of $540 million"）
- 2026-08-04｜Desmond Lynch｜guidance：Q3 non-GAAP毛利率財測約72%（原話："third quarter non-GAAP gross margin to be approximately 72%."）
- 2026-08-04｜Desmond Lynch｜guidance：Q3 non-GAAP營業利益率財測約43%，季增400bp（原話："approximately 43%, up 400 basis points sequentially"）
- 2026-08-04｜Desmond Lynch｜guidance：Q3 non-GAAP營業費用財測$156–160M（原話："between $156 million and $160 million."）
- 2026-08-04｜Desmond Lynch｜guidance：Q3 non-GAAP稀釋EPS財測$1.16–$1.21，稀釋股數約1.85億（原話："non-GAAP fully diluted earnings per share to be between"）
- 2026-08-04｜Jitendra Mohan｜guidance：Scorpio Q3成為最大產品線，比先前預期早一季（原話："Scorpio to become our largest product family in Q3, which is"）
- 2026-08-04｜Sanjay Gajendra｜guidance：Scorpio X領先客戶Q3量產爬坡並超越Scorpio P營收（原話："at least for a lead opportunity and lead"）
- 2026-08-04｜Desmond Lynch｜margin：Q2 non-GAAP毛利率73.7%，高於財測73%（原話："gross margin for the second quarter was 73.7%, above our"）
- 2026-08-04｜Desmond Lynch｜margin：Q2 non-GAAP營業利益率39.1%（原話："Non-GAAP operating margin for the second quarter was 39.1%,"）
- 2026-08-04｜Desmond Lynch｜margin：Scorpio平均毛利率大致與公司整體相當（原話："margin profile broadly in range with our sort of corporate"）
- 2026-08-04｜Desmond Lynch｜margin：毛利率長期目標78%（原話："trend towards a long-term target of 78% from here"）
- 2026-08-04｜Desmond Lynch｜margin：毛利率區間擴大，主因矽片對模組營收組合（原話："a wider range of gross margins with the main impacts being"）
- 2026-08-04｜Desmond Lynch｜capital_allocation：Q2 non-GAAP營業費用$135.8M，季增10%（原話："were $135.8 million, up 10% sequentially,"）
- 2026-08-04｜Desmond Lynch｜capital_allocation：現金及有價證券$1.25B，較Q1增$68.5M（原話："totaling $1.25 billion, up $68.5 million from Q1"）
- 2026-08-04｜Sanjay Gajendra｜capital_allocation：CXL方向持續重押投資（原話："we are investing heavily in coming out with"）
- 2026-08-04｜Jitendra Mohan｜product：PCIe 6占Q2營收逾50%（Q1約1/3）（原話："representing more than 50% of our total revenue driven"）
- 2026-08-04｜Sanjay Gajendra｜product：Scorpio X單獨內容價值預期遠超每XPU $1,000（原話："alone to grow well beyond $1,000 per XPU"）
- 2026-08-04｜Jitendra Mohan｜product：新200G Taurus產品使Taurus TAM於2030年超過$40億（原話："portfolio market opportunity to over $4 billion by 2030."）
- 2026-08-04｜Sanjay Gajendra｜product：Gen 5 Aries持續時間超出預期（原話："the surprise is how long Gen 5 has continued, and"）
- 2026-08-04｜Jitendra Mohan｜product：COSMOS由遙測診斷擴展為編排層（原話："now we are becoming part of the orchestration layer."）
- 2026-08-04｜Jitendra Mohan｜product：CXL新增一個美國超大規模客戶標準Leo設計案（原話："we closed a new design win with our standard Leo memory"）
- 2026-08-04｜Sanjay Gajendra｜commitment：UALink版Scorpio X交付時程2027（原話："on track to deliver UALink-enabled Scorpio X-Series"）
- 2026-08-04｜Sanjay Gajendra｜commitment：NPO晶片組目標2027量產（原話："targeted for 2027 production."）
- 2026-08-04｜Sanjay Gajendra｜commitment：客製方案首批出貨2027（原話："custom design wins to commence in 2027."）
- 2026-08-04｜Jitendra Mohan｜commitment：2027對兩家美國超大規模客戶量產出貨Leo CXL（原話："we expect to ship both standard and custom Leo CXL memory"）
- 2026-08-04｜Sanjay Gajendra｜customer：Scorpio X有逾10家客戶接洽（原話："We have over 10 customers engaged on the Scorpio X itself."）
- 2026-08-04｜Jitendra Mohan｜customer：中國營收絕對值增加但占比維持個位數（原話："they will continue to be in the single digit."）
- 2026-08-04｜Sanjay Gajendra｜customer：主要超大規模客戶有多個平台設計導入（原話："even with the lead hyperscaler we have,"）
- 2026-08-04｜Jitendra Mohan｜competition：提及其他廠商已推出或宣布UALink相關產品（原話："Some of the other vendors have also introduced their"）
- 2026-08-04｜Jitendra Mohan｜risk：機櫃內scale-up本世代與下一代仍以銅為主，光學用於機櫃間（原話："within a rack will continue to be copper."）

### 問答異常語氣（迴避／改口／保留）
- ALAB_Q2_2026_Earnings_Call_20260804.md｜問：Barclays（Trip Smith）問Scorpio毛利率變化與Amazon warrant影響如何建模｜答法：CFO回答Q3毛利率約72%、Scorpio平均毛利率與公司整體相當、長期78%，未回應Amazon warrant影響
- ALAB_Q2_2026_Earnings_Call_20260804.md｜問：Citi（Papa Sylla）問Scorpio X逾$1,000是否為UALink前指標，及目前每加速器內容價值與未來2–3年走向｜答法：回答『multiple thousands of dollars』與『targeting multiple thousands』，未給目前具體數字或是否為UALink前指標

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 2 | 4 |
| customer_concentration_credit | found | 5 | 4 |
| supply_demand_durability | found | 7 | 4 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 5 | 3 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 2 | 1 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261013","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價≤200美元且FY2027E共識EPS≥6.39；或最大客戶外≥2家Scorpio X量產且股價≤260美元；任一成立重跑判斷再定首倉","irr_base_pct":1.5,"ev5y_pct":14.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"-","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.6,"ev5y_pct":14.0,"irr_base_pct":1.5,"max_dd_pct":-70,"bull_5y_price":665.0,"bear_5y_price":120.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價≤200美元且FY2027E共識EPS≥6.39；或最大客戶外≥2家Scorpio X量產且股價≤260美元；任一成立重跑判斷再定首倉","price_at_dd":308.85,"archetype":"品質複利成長","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ALAB","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Astera Labs"},"oneliner":"第三季營收 584.9M、第四季指引中點 740M，基本面仍在加速；股價較前份判斷跌 38% 後回到合理區，但 2027 年 EPS 站不站得住，要看最大客戶第一代平台放緩後新客戶能否接上。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺超大型雲端業者 AI 機櫃內連線的錢，錢卡在加速器之間的 scale-up 交換與訊號調節節點，量目前主要靠單一終端客戶撐住。","reasoning":"公司只有一個報告部門，按產品線看：Scorpio 交換器第三季成為最大產品線，年化營收超過 10 億美元，X 系列已超過 P 系列；Aries 重定時器靠 PCIe Gen 6 續創新高；Taurus 800G 開始量產；Leo 記憶體控制器 2027 年中才放量（2026-11-03 法說，Jitendra Mohan、Desmond Lynch）。第三季營收 584.9M、季增 49%、年增 154%，non-GAAP 毛利率 72.4%、營益率 44.7%、EPS 1.32，營收與 EPS 都高於 8 月指引（540–560M、1.16–1.21）；第四季指引營收 730–750M、毛利率約 72%、營益率約 45%、EPS 1.62–1.66。單點依賴：2025 年單一終端客戶逾七成、前三大約 86%（年報摘要轉述，未讀原文），這同時是量產驗證的來源和最大的集中度風險。事實表的最新一季 KPI 停在第二季，第三季數字取自逐字稿。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi5_non_gaap","f_kpi6_non_gaap_eps","f_kpi7_q3_fy2026","f_earnings_recency"],"verdict_values":{"revenue_quality":"硬體出貨型收入，隨客戶平台世代起落，不是合約經常性收入。第三季成長主力是 Scorpio X 對領先客戶的量產，管理層稱客戶更分散但沒給占比。","unit_econ_note":"高配系統每顆加速器內容價值已超過 1,000 美元，資料速率每升一代單價約升 20–30%（2026-11-03，Jitendra Mohan）。管理層目標每代內容價值倍增，尚未實現。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"毛利率 73.9%、幾乎無負債、營收年增三位數，但單一終端客戶占比高，複利特徵要等第二家客戶量產才算驗證。"},"industry":{"clock_phase":"II","sd_verdict_source":"供需持久性：偏結構但帶週期性。Gartner、ASML、Wolfe 都指向吃緊延續到 2027–28，但這些證據講的是整體半導體與記憶體，不是 scale-up 交換器本身；管理層稱晶圓、電力、記憶體仍受限（2026-11-03）。","bargaining":{"up":"晶圓依賴台積電，10-K 列為單點風險，替代產能難以合理條件取得。","down":"最大終端客戶 2025 年逾七成營收，又以認股權證（最多 326 萬股、履約價 142.82 美元，對應最多 65 億美元採購，至 2033 年）綁定採購，議價權在客戶端。平均每年約 9 億美元，不到 FY2027 共識營收三成，是誘因不是採購承諾。","geo":"製造與主要經銷商在台灣；中國營收維持個位數占比（2026-08-04，Jitendra Mohan）。"},"profit_pool_dir":"五年利潤池占比事實表未涵蓋。方向上利潤往加速器與 scale-up 網路集中，ALAB 毛利率高於多數連線同業。","tam_table":[{"item":"scale-up 光學互連（2030）","value":"400 億美元，管理層估計，滲透率事實表未涵蓋"},{"item":"Taurus 市場（2030）","value":"超過 40 億美元，管理層 2026-08-04"},{"item":"Scorpio X 於 AWS 部署機會（2026–29）","value":"約 25 億美元，BofA 2026-05；第三季 Scorpio 年化已逾 10 億美元，此估計可能偏舊"},{"item":"五年營業利益池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河在擴大，靠的是量產經驗與 COSMOS 軟體，定價力只算穩定；第二家客戶量產前，這個方向只有一家大客戶的驗證。","reasoning":"優勢有兩層。一層是量產經驗：Scorpio X 有業界最大的 320 lane 配置，第三季出貨兩家客戶、多個平台。另一層是 COSMOS 軟體，從元件診斷擴到機櫃與網路管理，客戶換供應商要重做系統驗證。同業對照：過去 12 個月毛利率 73.9%，高於 AVGO 68.8%、CRDO 67.1%、MRVL 52.2%，接近 NVDA 74.7%；GAAP 營益率 25.5% 低於 CRDO 31.7%，因為研發占營收 33.8%，高於四家同業。ROIC 差距取不到，改看內容價值與毛利率：每顆加速器內容價值已超過 1,000 美元，下一代僅交換器就要再加 1,000 美元以上；毛利率卻從第一季 76.4% 降到第四季指引約 72%，部分來自 Amazon 認股權證的非現金影響，部分來自模組組合。所以執行面在擴大，定價力只算穩定。反例：若 2027 年底仍只有最大客戶量產，向上的方向就站不住。","fact_refs":["f_peer_alab_gross_margin_pct","f_peer_alab_operating_margin_pct","f_peer_alab_fcf_margin_pct","f_peer_nvda_gross_margin_pct","f_peer_nvda_operating_margin_pct","f_peer_avgo_gross_margin_pct","f_peer_avgo_operating_margin_pct","f_peer_crdo_gross_margin_pct","f_peer_crdo_operating_margin_pct","f_peer_crdo_fcf_margin_pct","f_peer_mrvl_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"量產驗證過的交換器與重定時器組合加 COSMOS 軟體，讓客戶換供應商要重做系統驗證；Hypercast 與網內運算讓產品直接參與 AI 工作負載。","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"第三季 X 系列已出貨兩家客戶，第四季另有多家客戶排單，P 系列在兩家美國超大型雲端業者放量（2026-11-03 法說）；本包沒有來源顯示最大客戶份額下滑。第二家客戶仍在試產，方向只有部分驗證。","competitor_notes":[{"name":"NVDA","strategy_note":"NVLink Fusion 既是合作也是封閉生態的延伸，營益率 65.2%，資本量級遠大於 ALAB，是最難防的生態競爭者。"},{"name":"AVGO","strategy_note":"Scale-Up Ethernet 交換器與 PCIe Gen 6 重定時器直接重疊，營益率 48.5%，可用規模與客製晶片關係綁售。"},{"name":"CRDO","strategy_note":"在光學 DSP 與主動電纜拿份額，FCF 利潤率 27.6% 高於 ALAB，主要重疊在 Taurus 線。"},{"name":"MRVL","strategy_note":"毛利率 52.2% 較低，但與 Lumentum 的合併若成局，矽光整合會直接對準 ALAB 的光學新線。"}],"peer_na_reason":"同業與 ALAB 的投入資本事實表未涵蓋，無法算 ROIC 差距，改用毛利率、營益率與內容價值方向對照。","threats":[{"level":"🔴","text":"NVLink 生態與 Broadcom Scale-Up Ethernet 爭奪 scale-up 交換插槽，對手可能較易取得設計導入，CXL、UALink 仍在早期。","p":35,"evidence_refs":["end_markets#3","substitute_technology#1","competitive_share_entrants#1"]},{"level":"🟡","text":"Credo 在光學 DSP 持續拿份額，壓縮 ALAB 在主動電纜與光學的空間。","p":30,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"銅轉光與產品價格隨時間下降，2028 年後機櫃內重定時器可能被光學架構取代；管理層稱光學內容價值更高，尚無營收驗證。","p":25,"evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（僅方向判斷：上半年資本支出約 28M、占營收 4%；投入資本事實表未涵蓋，周轉率未算）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"客戶要解決的問題是加速器之間的高頻寬低延遲連線，付款者與決策者都是超大型雲端業者，需求明確；但目前的解法由 PCIe 走向 UALink 與其他協定，問題持久不代表 ALAB 現有解法持久。"},{"item":"決策層級","level":"🟡","text":"替代性在每一代平台的插槽層級決定。同一代內換供應商要重做系統驗證，轉換成本高；跨世代會重新比稿，最大客戶下一代的選擇尚未揭露。"},{"item":"價值鏈分配","level":"🟡","text":"毛利率 72% 以上顯示目前分得到價值，但買方極度集中且以認股權證換採購，NVIDIA 掌握關鍵互補品，最大客戶也有自研能力。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的零組件，沒有消費者或政治上的漲價天花板；監管面主要是出口管制與關稅，列在風險項處理。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"需要資本支出、折舊、營運資金變動與投入資本。事實表只有上半年營業現金流 162.3M 與自由現金流 134.2M，差額約 28M 為資本支出，不足以算增量報酬。真正的再投資走研發費用，過去 12 個月占營收 33.8%，帳面口徑的內生上界會失真。情境輸入把成長標為超過內生上界，是算不出上界時取保守一側的假設，不是算出來的結果。"}}}},"q3_growth":{"verdict":"跑道寬，第二條 S 曲線有來源但還沒有營收，五年後的成長要靠 2027 下半年起的新客戶與新產品接力。","reasoning":"成長來自量與價，沒有併購或回購撐。量：機櫃與叢集變大，附掛率提高；價：資料速率每升一代單價約升 20–30%（2026-11-03，Jitendra Mohan）。共識 EPS FY2026E 4.39、FY2027E 6.94、FY2028E 8.61，兩年複合 40.0%；FY2025 只有 GAAP 1.22，口徑不同，不算三年複合。FY2027 共識營收 3,354M 只比第四季指引中點年化 2,960M 高 13%，相當於每季平均增約 5%，共識已部分反映放緩。內生上界因投入資本與再投資數字事實表未涵蓋而算不出來，共識與內生上界的缺口無法歸因，因此加註依賴 re-rate，長期信心上限為中；但 Base 情境本益比由 43.4 倍收縮到 24 倍，五年報酬實際靠 EPS 複利。光學、記憶體、客製、機櫃平台四條線都有時程，全部還沒有營收，2027 年下半年才開始驗證。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"量價齊揚，量靠機櫃與叢集擴大，價靠世代升級與內容價值增加，沒有併購或回購貢獻。","runway_years":"事實表未涵蓋滲透率，無法算到 30% 的年數","runway_post_y5":"🟢","endo_ceiling_basis":"投入資本、折舊與營運資金變動事實表未涵蓋，內生上界算不出來，情境樹按超過上界的保守一側處理。","segments":[{"item":"Scorpio（AI 交換）","value":"第三季最大產品線，年化逾 10 億美元，X 系列超過 P 系列；第四季 P 系列預期維持雙位數季增"},{"item":"Aries（重定時器）","value":"第三季創紀錄，每升一代單價約升 20–30%，Gen 7 已發表"},{"item":"Taurus（主動電纜）","value":"800G 第三季開始量產，2030 市場逾 40 億美元（管理層）"},{"item":"Leo（記憶體控制器）","value":"Leo 2 已出試產量，2027 年中放量"},{"item":"光學、客製、Orion","value":"光學 2027 下半年、客製 2027 年底首批 2028 放量、Orion 2027 起；單機櫃內容逾 10 萬美元"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":true,"text":"第一季 76.4%、第二季 73.7%、第三季 72.4%、第四季指引約 72%，季季走低，都低於 2025 全年 75.69%；同季年比事實表未涵蓋。"},{"item":"核心市占近 12 個月縮減","lit":false,"text":"本包沒有份額下滑的來源。"},{"item":"EPS 成長高於營收成長逾 5 個百分點","lit":false,"text":"FY2027E EPS 增 58%，營收增 65%；FY2028 共識營收事實表未涵蓋。"},{"item":"FCF 對淨利低於 0.75 連 2 年","lit":false,"text":"FY2025 為 1.29 倍；FY2024 淨利為負，不適用。"},{"item":"SBC 占營收逾 5% 且逐年上升","lit":false,"text":"第二季 16.3%，遠高於 5%；逐年方向事實表未涵蓋，未亮燈但列監測。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金留在帳上投研發，沒有回購也沒有配息，稀釋偏高。","reasoning":"第三季末現金及有價證券 1.38B，季增 125.3M，營業現金流 179.2M 創高，總債務 45M。FY2025 自由現金流 281.8M 對 GAAP 淨利 219.1M，轉換率 1.29 倍；第三季營業現金流只有 non-GAAP 淨利 243.4M 的 74%，放量期營運資金在吃現金。近三年現金去向四分事實表未涵蓋。SBC 第二季占營收 16.3%，稀釋股數由第三季指引 185M 升到第四季指引 187M，年化約 4.4%。管理層 2026-11-03 說員工一年翻倍，長期營業費用率約 30%。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_peer_alab_fcf_margin_pct","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"aiXscale 收購條款未揭露，尚無營收，無法計算已實現報酬。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"本包未見回購紀錄。"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"稀釋股數 185M 到 187M，一季增 1.1%，年化約 4.4%，高於每年 1.5%；SBC 占營收 16.3%（第二季）。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，公司未回購也未配息，現金累積到 1.38B，沒有資本回饋可展開。"},"sbc":{"note":"第二季 SBC 占營收 16.3%；Amazon 認股權證最多 326 萬股，約為第四季稀釋股數的 1.7%。"}}}},"q5_valuation":{"verdict":"現價要求 2031 年 EPS 約 12.8 美元才有 10% 年報酬，相當於 FY2028E 共識之後每年再長 14%，這個要求不高；問題是 FY2028E 共識本身還沒有定論。","reasoning":"現價 190.71 對應 FY2026E 43.4 倍、FY2027E 27.5 倍、FY2028E 22.1 倍，EV 對 FY2026E 營收 15.8 倍。要有 10% 年報酬，五年後需 307 美元，以 24 倍算 FY2031 EPS 約 12.8 美元。這個推論建立在 FY2027、FY2028 共識成立之上，而這正是爭點。PEG 用 FY2026E 本益比 43.4 除以兩年複合 40.0% 得 1.09，FY2027E 口徑為 0.69。non-GAAP 排除的費用約占四分之一：第三季指引 GAAP EPS 0.87–0.92 對 non-GAAP 1.16–1.21，換算接近 GAAP 的 FY2027E 本益比約 36 倍。同業前瞻本益比事實表未涵蓋，只能以自身倍數對照。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_ev_s_fwd","f_ev_s_current","f_ps_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_kpi7_q3_fy2026"],"verdict_values":{"valuation":{"basis":"Forward P/E 與 PEG。12 個月上檔用 FY2027E Base 7.00 乘 30 倍得 210 美元，約 +10.1%；中期用 FY2028E Base 8.80 乘 28 倍得 246 美元，約 +29.2%。","tier":"高成長 AI 連線半導體","peers":{"expanded":false,"reason":"事實表同業表只有利潤率，沒有同業前瞻本益比，無法做倍數對照。"},"fwd_pe":43.44,"peg":1.09,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"相對前份 308.85 美元，價格降 38%、FY2027E 共識上升，估值由偏貴回到合理；但分母有爭議，便宜的說法不成立，只到合理。五年分位事實表未涵蓋（上市未滿三年，年度端點只有 1–4 點），不計算。","upside_short_pct":10.1,"upside_mid_pct":29.2,"denominator_disputed":true,"denominator_note":"FY2027、FY2028 EPS 取決於最大客戶第一代平台放緩的幅度和第二家客戶接力的速度：FY2027 Bull 8.00、Base 7.00、Bear 5.30，差距大到本益比便宜的論證不能用，判斷改看 FY2031 的 EPS 區間。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把最大客戶第一代平台放緩當成短暫停頓，結果下一代插槽丟失。","reasoning":"最可能看錯三處。第一，第一代平台放緩其實是下一代插槽流失的前兆，這是唯一致命點。第二，新產品線時程滑動，客製案已從 2027 收窄到年底並把放量放到 2028。第三，股價在兩次判斷之間跌 38%，事實表沒有下跌原因，可能存在本包未涵蓋的負面資訊。本包沒有訴訟、SEC 調查或重編紀錄。衰退信號只有毛利率一項亮燈，陷阱風險中等。歷史最大回撤事實表未涵蓋。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104"],"verdict_values":{"trap":{"verdict":"🟡","label":"毛利率季季走低，其他衰退信號未亮"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":4.39,"pe":43.44,"basis":"FY2026E 共識 non-GAAP EPS，現價 190.71 除以當年度預估，與終端倍數同為當年度 EPS 分母。"},"eps":{"bull":[8.0,11.0,14.8,18.5,22.0],"base":[7.0,8.8,10.7,12.5,14.0],"bear":[5.3,4.7,5.0,5.4,5.9]},"pe":{"bull":30,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"max_dd":{"lo":-65,"hi":-45,"basis":"從現價 190.71 起算。淺端 −45% 是 Bear 五年終值約 106 美元的跌幅；深端 −65% 取 Bear FY2028 EPS 4.70 乘 15 倍約 70 美元（−63%）再加市場過度反應。股價自前份 308.85 美元以來已跌 38%，說明這種回撤幅度真實可能。","trigger_time":null},"basis":{"bull":"2027 年底前最大客戶外兩家以上量產，下一代內容價值倍增兌現，四條新線 2028 年起貢獻；FY2031 營收約 120 億美元、non-GAAP 營益率約 42%，稀釋股數約 205M；30 倍對應當年成長接近 20%。","base":"第一代平台 2027 上半年放緩，新平台與新客戶下半年接上；FY2031 營收約 80 億美元，營益率約 41%（毛利率約 71% 減管理層長期營業費用率 30%），稀釋股數約 205M；24 倍對照 ALAB 自身 FY2028E 22.1 倍，同業前瞻本益比事實表未涵蓋。","bear":"最大客戶下一代 scale-up 插槽流失或明顯分食，2027–28 營收下滑，FY2031 營收約 36 億美元、營益率約 36%；18 倍取成長熄火到 10% 的情境。Bear 機率 30%：最大終端客戶逾七成、第二家仍在試產、內生上界算不出來，按保守一側處理；Gartner、ASML 的吃緊證據只到 2027–28，蓋不到下一代插槽的決定，所以不因此降低機率。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2025 年單一終端客戶逾七成營收；CFO 說初始 Scorpio X 平台已完成大部分初始部署（2026-11-03），第二家超大型客戶仍在試產。","assumption":"最大客戶下一代平台的 scale-up 插槽仍由 Astera 拿到，或新客戶能補上缺口。","consequence":"FY2028 EPS 落向 4.70，五年價格約 106 美元，較現價跌 44%。這與唯一致命點是同一件事，兩處對帳一致。","ruling":"採納，列為最大風險，Bear 機率給 30%。","watch":"第一季財測、2026 年 10-K 終端客戶占比、最大客戶新平台公開設計。","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1","capital_markets_pricing#3"],"fact_refs":["f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"論點成功但股東經濟變差","evidence":"第四季營業費用指引 194–200M，較第三季 162M 再增約 21%，員工一年翻倍；毛利率由 76.4% 降到約 72%；管理層長期營業費用率約 30%；SBC 占營收 16.3%；Amazon 認股權證以股權換採購。","assumption":"營收成長能維持營業槓桿，新產品線不會稀釋利潤率，股數增幅放緩。","consequence":"營收達標但營益率回落到 40% 上下，稀釋年化約 4%，non-GAAP EPS 達標而每股實質價值落後。","ruling":"部分採納。Base 營益率只給 41%，低於第四季指引 45%；Orion 機櫃平台管理層稱會提高毛利，尚無數字，不採信。","watch":"non-GAAP 毛利率、營業費用率、稀釋股數季增幅。","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_kpi4_sbc","f_kpi7_q3_fy2026"]},{"view":"價格已反映太多","evidence":"下跌後過去 12 個月 P/S 仍 21.4 倍、FY2026E 本益比 43.4 倍，接近 GAAP 的 FY2027E 本益比約 36 倍。","assumption":"FY2028E 共識 8.61 大致成立，且終端倍數能守住 24 倍。","consequence":"若 2031 年 EPS 只到 Bear 5.90，即使倍數 24 倍也只有 142 美元，仍低於現價。","ruling":"反駁為主因：FY2028E 22.1 倍、要求的 2028 年後成長約 14%，價格不算透支；但前提是共識成立，故只給合理，不給便宜。","watch":"FY2028E 共識 EPS 是否跌破 8.00。","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_ps_current","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 308.85 → 本次 190.71（-38.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=308.85","side_b":"本次 price_at_dd=190.71","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 308.85 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 308.85 美元：Bull 價 665、Bear 價 120，五年期望值 +14.0%，基準年化 1.5%，不對稱比 1.6","side_b":"本次情境、股價仍用 308.85 美元：Bull 價 660、Bear 價 106.2，五年期望值 +12.7%，基準年化 1.7%，不對稱比 1.44","ruling":"先換情境、股價不動：五年期望值少 1.3 個百分點，基準年化多 0.2 個百分點。不對稱比由 1.6 變為 1.44。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 308.85 美元：五年期望值 +12.7%，基準年化 1.7%，不對稱比 1.44","side_b":"本次情境、股價 190.71 美元：五年期望值 +82.5%，基準年化 12.0%，不對稱比 4.63","ruling":"再換股價、情境不動：起點價下跌 38.3%，五年期望值多 69.8 個百分點，基準年化多 10.3 個百分點，不對稱比由 1.44 升到 4.63。合計五年期望值比前份多 68.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價下跌後的估值與部位結論","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份 308.85 美元，估值偏貴，結論為等待。","side_b":"本次 190.71 美元，估值回到合理；FY2027E 共識 6.94 高於前份門檻 6.39。","ruling":"估值結論改善來自價格。Bull 25%、Bear 30% 維持前份，第三季正反證據大致抵銷；Max DD 區間 −65% 至 −45%，比前份 −70% 淺，因為起點已低 38%。","evidence_level":"事實表價格與共識","settle_metric":"股價與 FY2027E、FY2028E 共識 EPS","if_then":["若股價續跌而第一季財測不低於第四季實績，分批反買","若股價先反彈超過 260 美元而第一季財測未出，不追"]},{"axis":"基本面欄位複核","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：訊號等級 B、陷阱風險中等、護城河向上、五年後跑道寬、品質複利成長、中循環。","side_b":"本次六欄都不變。第三季法說帶來正面證據（X 系列出貨兩家客戶、多家第四季排單、營收超過指引上緣），也帶來負面證據（初始平台部署大致完成、營業費用超指引、毛利率續降）。","ruling":"新證據沒有推翻任何一欄。分母爭議使訊號等級不因價格下跌而升級。","evidence_level":"2026-11-03 法說原話","settle_metric":"第一季財測與最大客戶外量產家數","if_then":["若 2027 年底最大客戶外仍無量產客戶，護城河方向下修為穩定，第三筆取消"]},{"axis":"首倉與加碼的重新評估條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價≤200美元且FY2027E共識EPS≥6.39；或最大客戶外≥2家Scorpio X量產且股價≤260美元；任一成立重跑判斷再定首倉","side_b":"第一季財測中點不低於第四季實績；或股價≤150 美元且 FY2028E 共識 EPS≥8.00；任一成立重跑判斷定下一筆","ruling":"前份第一支條件已成立（股價 190.71 不高於 200、FY2027E 共識 6.94 不低於 6.39），本次就是那次重跑。重跑結果是價格條件達成，但 FY2027、FY2028 EPS 仍有爭議，本次不建首倉，維持追蹤。首倉改綁第一季財測，因為決定性數據已經不是價格。","evidence_level":"事實表價格與共識","settle_metric":"第一季營收財測中點對第四季實績","if_then":["若第一季財測中點不低於第四季實績，重跑判斷定首筆，部位上限總資產 4%","若未達標，不建倉，續列追蹤"]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未留存清倉或減碼門檻。","side_b":"最大客戶外量產家數 2027 年底仍為 0、季營收連 2 季合計跌逾 15%、non-GAAP 毛利率連 2 季低於 70%、FY2028E 共識 EPS 跌破 7.00。","ruling":"前份摘要這一欄為空，本次新設清倉與減碼門檻，全部對應情境樹的 Bear 路徑。","evidence_level":"判斷設定","settle_metric":"四項門檻逐季對照","if_then":["毛利率連 2 季低於 70%，減碼到 2%","量產家數與營收兩項同時觸發，清倉"]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未留存唯一致命點。","side_b":"最大終端客戶下一代加速器平台的 scale-up 交換器，多數插槽改由 Broadcom、NVLink 方案或自研承接。","ruling":"Single Thing 本次新設，選它是因為它對 FY2028 EPS 的敏感度最大（Base 8.80 對 Bear 4.70）。","evidence_level":"法說與年報摘要，無客戶端確認","settle_metric":"最大客戶下一代平台供應商","if_then":["若證實多數插槽由他家或自研承接，清倉"],"evidence_refs":["customer_second_source#0"]},{"axis":"2027 上半年營收形狀","cause":null,"side_a":"管理層：初始 Scorpio X 平台已完成大部分初始部署，之後維持規模貢獻，新平台與新客戶在 2027 年陸續疊加（2026-11-03，Desmond Lynch）。","side_b":"賣方提問：最大客戶本世代建置 2027 年第一季見頂，下一代要到接近 2028（Barclays），Morgan Stanley 也問是否進入高原期；CFO 拒談客戶量。FY2027 共識營收僅比第四季年化高 13%。","ruling":"可調和，屬程度差異：第一代放緩與新平台接力可以同時成立，差別在缺口多大、多久。決勝數據是 2027 年 2 月的第一季財測，今天還不存在，風險未解，到那時才能裁決。","evidence_level":"管理層原話與賣方提問，無客戶端數據","settle_metric":"第一季營收財測中點對第四季實績","if_then":["若財測中點不低於第四季實績，加碼到總資產 4%","若季減超過 10%，停止加碼，等第二季財測","若季減超過 20% 且管理層未點名接力平台，減碼一半","若訊號證實放緩只是一季，第二季財測恢復季增，把第二筆補回"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"客戶集中度口徑","cause":null,"side_a":"10-K 客戶表：五家各占 10% 以上，最大 20%，合計約 84%。","side_b":"年報風險揭露與第三方彙整：單一終端客戶逾 2025 年營收 70%，前三大約 86%。","ruling":"可調和：合理解讀是前者為下單的直接客戶與經銷商，後者為實際用貨的終端客戶，投資判斷用終端口徑。兩份都是搜尋摘要轉述，未讀原文。第三季法說稱客戶更分散但沒給數字，而第三季成長主力是領先客戶的 X 系列，集中度可能不降反升。","evidence_level":"二手摘要","settle_metric":"2026 年 10-K 最大終端客戶占比","if_then":["若占比低於 60%，第二家客戶的論點算得到驗證","若高於 75%，取消第三筆加碼"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#0","geo_supply_chain#4"]},{"axis":"長期毛利率目標","cause":null,"side_a":"2026-08-04 法說摘錄：毛利率長期目標 78%（Desmond Lynch）。","side_b":"2026-11-03 法說 Susquehanna 提問用長期目標 70%，管理層未更正；實績由第一季 76.4% 走到第四季指引約 72%。","ruling":"兩個數字對不上，本包無法查原文，不採信 78%。情境樹用約 71%，配長期營業費用率約 30%，長期營益率約 41%，低於第四季指引 45%。","evidence_level":"法說摘錄與賣方提問","settle_metric":"下一次管理層對長期毛利率的明確表述","if_then":["若 non-GAAP 毛利率連 2 季低於 70%，減碼到 2%"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"管理層承諾對照","cause":null,"side_a":"2026-08-04：客製方案首批 2027、NPO 目標 2027 量產、Leo 2027 對兩家超大型客戶量產、UALink 版 Scorpio X 2027 交付；第三季營收指引 540–560M、營業費用 156–160M。","side_b":"2026-11-03：客製收窄為 2027 年底首批、2028 放量；NPO 營收 2027 下半年；Leo 放量 2027 年中；UALink 只說變化不大，未重申交付時點；第三季營收 584.9M 超過上緣，營業費用 162M 也超過上緣。","ruling":"短期財務指引守信，新產品時程尚未失約，但客製放量已後移。UALink 時點未重申，標為未證、監測。問答中另有未正面回答：2026-08-04 CFO 未回應 Amazon 認股權證對毛利率的影響，也未給當時每顆內容價值的具體數字；2026-11-03 CFO 拒談 2027 客戶量。","evidence_level":"兩場法說原話對照","settle_metric":"UALink 版 Scorpio X 的交付時點與客戶","if_then":["若連兩季未重申 2027 交付，內容價值倍增的 Base 假設下修，取消第三筆加碼"]},{"axis":"產業態勢三軸","cause":null,"side_a":"競爭：Broadcom、NVIDIA、Credo、Marvell 都在加碼，Marvell 與 Lumentum 整合矽光（2026-11-03 問答）。","side_b":"結構：AI 半導體短缺預期延續到 2027，ASML 產能賣到 2027，scale-up 走向多協定；其他結構變數是 2028 年後銅轉光與最大客戶自研能力。","ruling":"雙向拉鋸：需求面結構轉好，競爭同步變強，銅轉光是下一個結構變動點。","evidence_level":"第三方研究與賣方摘要","settle_metric":"下一代平台設計導入與 2028 年光學出貨","if_then":["若 2028 年光學營收占比仍低於 5%，H3 下修"],"evidence_refs":["end_markets#3","substitute_technology#1"]},{"axis":"現在就買與現在就賣的最強論證","cause":null,"side_a":"買：FY2028E 22.1 倍，第四季營收指引再季增 27%，FY1 共識三個月上修 8.9%，前份設定的價格與共識條件都已達成；10% 年報酬只需 2031 年 EPS 約 12.8 美元。","side_b":"賣：第一代平台放緩是 CFO 親口說的，逾七成終端營收集中一家，下一代插槽未定；股價跌 38% 而事實表沒有下跌原因，可能有本包未涵蓋的資訊。","ruling":"現在不買，維持追蹤：賠率夠但 FY2027、FY2028 EPS 未定，第一季財測才驗得出來。首筆綁第一季財測，後續部位綁第二家客戶量產。","evidence_level":"事實表與法說","settle_metric":"第一季財測","if_then":["若第四季財報前股價跌破 150 美元且 FY2028E 共識仍不低於 8.00，重跑判斷定首筆","若 FY2028E 共識跌破 7.00，取消首筆計畫，重跑判斷"]}],"triggers":[{"n":1,"text":"第一季財測驗證第一代平台放緩的幅度","type":"假設驗證","maps_to":"H1","metric":"第一季營收財測中點相對第四季實績","threshold":"不低於 0%","action":"加碼到總資產 4%","source_freq":"季度財報","date":"2027-02","evidence_refs":["capital_markets_pricing#3"]},{"n":2,"text":"最大客戶以外的 Scorpio X 客戶進入量產","type":"加碼","maps_to":"H1","metric":"最大客戶外 Scorpio X 量產客戶數","threshold":"至少 1 家","action":"加碼到總資產 6%","source_freq":"季度法說","date":"2027-08","evidence_refs":[]},{"n":3,"text":"第一季財測大幅季減且說不出接力平台","type":"減碼","maps_to":"R1","metric":"第一季營收財測中點相對第四季實績","threshold":"季減超過 20% 且未點名接力平台","action":"減碼一半，停止加碼","source_freq":"季度財報","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":4,"text":"最大客戶下一代平台插槽流失","type":"Single Thing","maps_to":"Single Thing","metric":"最大客戶下一代平台 scale-up 交換器供應商","threshold":"證實多數插槽由他家或自研承接","action":"清倉","source_freq":"事件驅動，法說與 10-K","date":"2027-12","evidence_refs":["customer_second_source#0"]},{"n":5,"text":"毛利率跌破管理層口中的長期區間","type":"風險","maps_to":"R2","metric":"non-GAAP 毛利率","threshold":"連 2 季低於 70%","action":"減碼到總資產 2%","source_freq":"季度財報","date":"2027-05","evidence_refs":["capital_markets_pricing#4"]},{"n":6,"text":"價格跌到 Bear 倍數附近而共識未破","type":"估值rearm","maps_to":"H1","metric":"股價與 FY2028E 共識 EPS","threshold":"股價≤150 美元且共識≥8.00","action":"分批反買","source_freq":"每日股價、月度共識","date":null,"evidence_refs":[]},{"n":7,"text":"第二家客戶沒有出現且營收下滑","type":"清倉","maps_to":"H1","metric":"最大客戶外量產家數與季營收","threshold":"2027 年底仍為 0 家且季營收連 2 季合計跌逾 15%","action":"清倉","source_freq":"季度財報","date":"2028-02","evidence_refs":[]},{"n":8,"text":"第四季財報後全面複審","type":"複審日期","maps_to":"H1","metric":"全套判斷","threshold":"第四季財報發布","action":"重跑判斷","source_freq":"季度","date":"2027-02","evidence_refs":[]},{"n":9,"text":"年報揭露的終端客戶集中度","type":"風險","maps_to":"R1","metric":"2026 年 10-K 最大終端客戶占比","threshold":"高於 75%","action":"取消第三筆加碼","source_freq":"年度 10-K","date":"2027-02","evidence_refs":["customer_concentration_credit#1"]}],"kill_metrics":[{"metric":"最大客戶外 Scorpio X 量產客戶數","bear_threshold":"2027 年底仍為 0 家","window":"至 2027-12-31","source":"季度法說","last_status":"ok"},{"metric":"季營收","bear_threshold":"連 2 季季減合計超過 15%","window":"2027 全年","source":"季度財報","last_status":"ok"},{"metric":"non-GAAP 毛利率","bear_threshold":"連 2 季低於 70%","window":"滾動 2 季","source":"季度財報","last_status":"warning"},{"metric":"FY2028E 共識 EPS","bear_threshold":"跌破 7.00","window":"未來 12 個月","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[{"ref":"supply_demand_durability#1","reason":"這則談 NAND 位元供需，ALAB 不賣 NAND，證據對象與公司產品不同，無法推導 scale-up 連線的需求。"},{"ref":"supply_demand_durability#5","reason":"這則只給晶圓產能增速，沒有需求或稼動率對照，單獨無法支持供過於求的結論。"}],"action_conditions":{"rearm_trigger":"第一季財測中點不低於第四季實績；或股價≤150 美元且 FY2028E 共識 EPS≥8.00；任一成立重跑判斷定下一筆","exec_line":"現價不建倉，維持追蹤：FY2027、FY2028 EPS 未定，等 2027 年 2 月第一季財測。財測中點不低於第四季實績，或股價≤150 美元且 FY2028E 共識 EPS≥8.00，才重跑判斷定首筆；財測未出前續漲不追。本文的 2%、4%、6% 是重跑後轉為可進場時的部位上限，不是現在的動作。","holding_cap":"首筆 2%，第一季財測達標加到 4%，最大客戶外 Scorpio X 量產才到 6%。"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把第一代平台放緩當成整條成長線見頂：第二家超大型客戶已在試產，第四季另有多家客戶排單，FY2027 共識只要求每季平均增約 5%。這是判斷不是證實，股價下跌的真正原因事實表未涵蓋，第一季財測才驗得出來。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"Scorpio X 在最大客戶之外放量，第一代平台放緩後營收不出現斷層。","2y":"FY2027 營收達共識水準，且最大客戶外至少 2 家量產。","5y":null,"10y":null,"threshold":"FY2027 營收≥3,350M，最大客戶外 Scorpio X 量產客戶≥2 家。","source":"季度財報與法說、10-K 終端客戶揭露。","drift_rule":"TTM 偏離連 2 季≥5% 削弱，連 3 季≥10% 反轉。"},{"id":"H2","text":"每顆加速器內容價值逐代倍增，營益率守住 40% 以上。","2y":null,"5y":"FY2031 營收約 80 億美元、non-GAAP 營益率約 41%。","10y":null,"threshold":"下一代每顆加速器內容價值≥2,000 美元；FY2031 營收≥8,000M、non-GAAP 營益率≥40%。","source":"法說揭露的內容價值、季度財報。","drift_rule":"TTM 偏離連 4 季≥5% 削弱，連 6 季≥10% 反轉。"},{"id":"H3","text":"協定從 PCIe 轉向 UALink、銅轉向光之後，ALAB 仍保住 scale-up 插槽並拿到光學新市場。","2y":null,"5y":null,"10y":"scale-up 光學成為第二條主要營收線。","threshold":"2030 年 scale-up 光學營收≥20 億美元，約為管理層 400 億美元市場估計的 5%。","source":"法說產品線揭露、產業研究機構數據。","drift_rule":"跨 2 個年度低於進度削弱，跨 3 個年度反轉。"}],"R":[{"id":"R1","text":"最大客戶第一代平台放緩後，新平台與新客戶接不上，2027 年營收出現斷層。","h_ref":"H1","clock":"⚡","threshold":"第一季財測中點季減超過 20%，或連 2 季季減合計超過 15%。","evidence_refs":["capital_markets_pricing#3","customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R2","text":"毛利率與費用同時走差，營收達標但利潤率回落。","h_ref":"H2","clock":"🔥","threshold":"non-GAAP 毛利率連 2 季低於 70%，或營業費用率高於 30% 而營收年增低於 30%。","evidence_refs":["capital_markets_pricing#4"]},{"id":"R3","text":"Broadcom、NVLink 生態與多協定轉換吃掉 scale-up 插槽，銅轉光後重定時器被取代。","h_ref":"H3","clock":"🐢","threshold":"下一代每顆加速器內容價值未達 2,000 美元，或公開設計中 ALAB 插槽減少。","evidence_refs":["end_markets#3","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1","competitive_share_entrants#3"]},{"id":"R4","text":"製造與經銷集中台灣，晶圓供應或地緣事件中斷出貨。","h_ref":"H1","clock":"🐢","threshold":"10-Q 揭露晶圓不足造成出貨遞延，或台灣事件中斷出貨達一季。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#4"]},{"id":"R5","text":"出口管制與關稅影響需求或成本。","h_ref":"H2","clock":"🔥","threshold":"法說揭露出口許可或關稅影響當季營收 5% 以上，或毛利率因此下降 200bp 以上。","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3"]}],"single_thing":{"description":"最大終端客戶下一代加速器平台的 scale-up 交換器，多數插槽改由 Broadcom、NVLink 方案或自研承接。","why_fatal":"2025 年單一終端客戶占營收逾七成，第三季成長主力又是領先客戶的 X 系列量產；這是情境樹裡對 FY2028 EPS 影響最大的單一變數，Base 8.80 對 Bear 4.70。","if_happens":"FY2028 EPS 落向 4.70，股價按 16–18 倍看 75–85 美元，清倉。","how_monitor":"每季法說對下一代平台的表述、2026 年 10-K 終端客戶占比、Amazon 認股權證歸屬進度、最大客戶公開的新平台設計。","probability":"25%（12–24 個月），主觀估計：第二家客戶試產與多平台設計導入壓低機率，但管理層未揭露下一代插槽已拿到。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":27.48,"peg_fy2":0.69,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.22,"FY2026E":4.39,"FY2027E":6.94,"FY2028E":8.61},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識，EPS 家數事實表未涵蓋（營收共識 20–23 位分析師），與公司 non-GAAP 季度數字對得上（第二季 0.80、第三季 1.32、第四季指引中點 1.64）。FY2025A 1.22 是 GAAP 稀釋，事實表沒有 non-GAAP 年度值，口徑不同，不拿來算三年複合；共識成長用 FY2026E 到 FY2028E 兩年複合 40.0%。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與第一季財測，管理層也承諾補充 Orion 對損益的影響","impact":"高","watch":"第一季營收財測中點對第四季實績"},{"date":"2027-06","date_precision":"month","type":"product","event":"Leo 2 量產放量（管理層稱 2027 年中）","impact":"中","watch":"兩家超大型客戶是否如期出貨"},{"date":"2027-09","date_precision":"month","type":"product","event":"NPO 光學元件與多家 Scorpio X 客戶開始貢獻營收（2027 下半年）","impact":"高","watch":"最大客戶外量產家數"},{"date":"2027-12","date_precision":"month","type":"product","event":"客製方案首批出貨（管理層稱 2027 年底）","impact":"中","watch":"是否再往後延"}],"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把第一代平台放緩當成整條成長線見頂：第二家超大型客戶已在試產，第四季另有多家客戶排單，FY2027 共識只要求每季平均增約 5%。這是判斷不是證實，股價下跌的真正原因事實表未涵蓋，第一季財測才驗得出來。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='↑', week26=-4.54, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望"}}
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
