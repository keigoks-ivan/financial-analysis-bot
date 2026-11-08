你是 DD 管線 v20 的判斷層閘（gate），標的 NVMI（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（26 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝254.96 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi2_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝33 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi4_gaap_operating_margin`（q1_business）｜GAAP operating margin＝30 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-05 date｜期間與口徑：2026-11-05／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-05）
- `f_peer_nvmi_gross_margin_pct`（q2_moat）｜NVMI 毛利率＝57.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVMI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_nvmi_operating_margin_pct`（q2_moat）｜NVMI 營業利益率＝30.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVMI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_klac_operating_margin_pct`（q2_moat）｜KLAC 營業利益率＝42.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_onto_operating_margin_pct`（q2_moat）｜ONTO 營業利益率＝13.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONTO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_camt_operating_margin_pct`（q2_moat）｜CAMT 營業利益率＝23.15 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAMT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.67 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝13.66 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝16.59 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝1077.7 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1360.2 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（7 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_free_cash_flow_40_92_cap`（q4_capital）｜Free cash flow（推算＝營運現金流 40.92 − capex 2.49；公司未揭露 FCF）＝38.42 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）；FCF 為依新聞稿現金流量表推算（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi6_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝8.9 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi3_gaap_operating_income`（q1_business）｜GAAP operating income＝76.19 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝313.18 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝29.35 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 10.67，分子＝快照價 313.18｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝35.87 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝67.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝67.5 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝9.68 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝53.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝8.99 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-39.91 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 10.67 → 10.67（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ma_w250`（q5_valuation）｜250 週均線＝212.61 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：客戶信用：搜尋僅得 Intel（客戶身分推測未經 Nova 確認，客戶未具名）2025 年遭 Fitch 降至 BBB 負向展望、S&P 降至 BBB；未找到 2026 年評等動作。Nova 客戶實際身分未於本軸證實。
  - 來源：Fitch/S&P Intel downgrade coverage (bondblox, tweaktown)（as_of 2025-01-01）｜affects：decision_inputs.bear
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：風險面：分析師指出若先進封裝投資放緩，WMC／Prism 等工具可能利用率不足；另有先進節點大客戶撤單的集中度風險；NAND 仍處長期下行。
  - 來源：Quartr — Nova Citi 2026 TMT summary／搜尋摘要（as_of 2026-09-30）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Nova FY2025 20-F 風險因子提及對中國晶圓廠的出口管制與關稅，美國對先進製程設備與中國實體管制收緊，歐日新制度；未見針對 Nova 的調查
  - 來源：STOCK TITAN｜Nova Ltd 20-F 摘要（as_of 2026-02-17）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Nova FY2025 20-F 風險因素：貿易限制、關稅變動與進出口許可可能使受影響國家的銷售大幅減少；主要客戶位於台灣、日本、南韓、中國與美國。
  - 來源：NOVA LTD. Form 20-F FY2025 (SEC)（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：中國占 Nova 營收約 35%（2025 上半年），2024 年為 39%；管理層預期中國占比下降。來源為第三方 PESTLE 分析（2026-04 更新），非公司文件。
  - 來源：dcf-analysis.com Nova Ltd. (NVMI) PESTLE Analysis [Apr-2026 Updated]（as_of 2026-04-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：Section 122 全球替代關稅 10%、後升至 15%，自 2026-02-24 生效，可能波及半導體供應鏈（出自 SEALSQ 424B5，非 Nova 專屬）。
  - 來源：SEALSQ Corp Form 424B5 FY2026 (SEC)（as_of 2026-02-24）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Nova 2025 20-F 摘要列出營運集中於以色列、美國、德國的製造設施，並提及對中國晶片廠銷售受出口管制與關稅影響。
  - 來源：StockTitan, Nova Ltd 20-F annual report summary（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Nova 2026年8月（Q2 2026）投資人簡報風險項列有依賴有限數量供應商，以及每條產品線依賴單一製造設施；FY2024 20-F 亦稱對有限供應商、部分情況為唯一供應商。
  - 來源：Nova investor presentation Q2 2026 / Nova 20-F FY2024 (SEC)（as_of 2026-08-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：中國占 Nova 營收：2024年約39%（分析師於法說會提問）；第三方稱2025上半年約35%，預期占比下降但名目仍小幅成長（二手來源）。
  - 來源：fintool.com NVMI research; dcf-model.com PESTLE（as_of 2025-11-01）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：Nova Q1 2026 前瞻聲明列示外國政治經濟風險，含供應鏈困難及可能限制營運的制裁與出口限制。
  - 來源：Nova Q1 2026 call date PDF / VCP Scanner NVMI（as_of 2026-04-01）｜affects：thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Q2 2026 毛利率 56.5%，低於 Q1 2026 的 57.7% 與 Q2 2025 的 57.8%。
  - 來源：Nova Q2 2026 results (2026-08-06), 搜尋彙整（as_of 2026-08-06）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Onto 的 Atlas G6 OCD 系統（2025-09 發表）瞄準第二代 GAA 邏輯與 HBM 用垂直閘 DRAM，已取得多家邏輯與記憶體廠量產訂單；光學量測仍是主流路線，同業在同一賽道推新平台。
  - 來源：Business Wire：Onto Innovation Launches Next Generation OCD Metrology Platform to Enable Process Control for Advanced AI Devices（as_of 2025-09-09）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Benzinga 2026-09-03 快照：10 位分析師平均目標價約 491，高 640、低 240（Jefferies）；Citigroup 8/10 由 595 降至 550，Needham 8/7 由 640 降至 570
  - 來源：Benzinga NVMI sentiment page（as_of 2026-09-03）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":806.0,"bear_5y_price":218.8,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":57.9,"ev5y_pct":56.3,"irr_base_pct":9.6,"asym_ratio":4.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.67,"pe":29.35,"basis":"FY2026E 共識（Koyfin 2026-11-07，非 GAAP），與終端倍數同為當年度 EPS 口徑；FY2026 已走完三季。"},"eps":{"bull":[15.0,19.5,23.0,27.0,31.0],"base":[13.7,16.2,16.7,19.0,21.5],"bear":[12.2,11.4,9.8,11.0,12.5]},"pe":{"bull":26,"base":23,"bear":17.5},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.7},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NVMI_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：Q3 2026 營收財測區間 277–287 百萬美元（原話："between $277 million and $287 million."）
- 2026-08-06｜CFO｜guidance：Q3 non-GAAP EPS 財測區間 2.70–2.85（原話："Non-GAAP earnings per diluted share to range from $2.70 to $2.85."）
- 2026-08-06｜CEO｜guidance：CEO 表示預期今年再一年雙位數成長（原話："we expect to deliver another year of double-digit growth"）
- 2026-08-06｜CFO｜guidance：Q3 營業費用（non-GAAP）預計增至約 68 百萬美元（原話："increase to approximately $68 million;"）
- 2026-08-06｜CFO｜guidance：Q3 有效稅率預期約 17%（原話："Effective tax rate is expected to be approximately 17%"）
- 2026-08-06｜CEO｜guidance：CEO 對全年先進封裝占產品營收比重的說法：原預估 20–25%，現靠近 25%（原話："we projected it initially to be between 20% and 25%."）
- 2026-08-06｜CEO｜guidance：CEO 回應分析師 2027 年 WFE 成長 40% 的說法：太早判斷，但預期 2027 為成長年（原話："It's too early to say whether 2027 will grow 40%."）
- 2026-08-06｜CEO｜guidance：CEO 說明今年記憶體約占營收 30%（原話："be about 30% for us this year."）
- 2026-08-06｜CFO｜margin：Q3 毛利率財測中點：GAAP 約 57%、non-GAAP 約 59%（原話："approximately 59% on a non-GAAP basis."）
- 2026-08-06｜CFO｜margin：CFO 回答 Q2 毛利率低於財測的原因為產品組合（原話："Yes. So the main reason is product mix."）
- 2026-08-06｜CFO｜margin：CFO 給上半年毛利率口徑：約 59%（原話："first half of 2026, gross margin was approximately 59%."）
- 2026-08-06｜CFO｜margin：CFO 預期全年毛利率約 59%（原話："full year gross margin to be approximately 59%"）
- 2026-08-06｜CFO｜margin：CFO 稱記憶體在 BOM 中占比不大，對毛利率結構無重大改變（原話："Our proportion of memory portion of our BOM is not significant."）
- 2026-08-06｜CFO｜margin：CFO 重申目標模型毛利率區間 57–60% 完好（原話："target model of 57% to 60% is well intact."）
- 2026-08-06｜CFO｜margin：Q2 non-GAAP 營業利益率 33%，位於目標模型 28–33% 上緣（原話："on the upper range of our target model of 28% to 33%."）
- 2026-08-06｜CEO｜commitment：CEO 承諾維持毛利率模型，今年與明年皆然（原話："we are maintaining our gross margin model"）
- 2026-08-06｜CEO｜commitment：管理層稱有機成長目標可望比原計畫提前達成（原話："objectives sooner than originally planned"）
- 2026-08-06｜CEO｜commitment：下一階段長期成長策略將於 2027 Q1 投資人日公布（原話："upcoming Investor Day during the first quarter of 2027."）
- 2026-08-06｜CEO｜capital_allocation：研發投入約占營收 15%（原話："invest approximately 15% of revenue in research"）
- 2026-08-06｜CFO｜capital_allocation：現金與投資超過 17 億美元（原話："more than $1.7 billion in cash and"）
- 2026-08-06｜CFO｜capital_allocation：CFO 提及將尋求選擇性併購（原話："pursue selective M&A opportunities"）
- 2026-08-06｜CEO｜capital_allocation：加州無塵室擴建使美國產能加倍（原話："our recent clean room expansion in California, which doubles"）
- 2026-08-06｜CEO｜product：先進邏輯相關營收季增超過一倍（原話："more than doubled sequentially"）
- 2026-08-06｜CEO｜product：先進封裝創紀錄，占產品營收近 1/4（原話："record sales contributing nearly 1/4"）
- 2026-08-06｜CEO｜product：Nova WMC 獲領先晶圓代工客戶選為先進封裝 tool of record（原話："a recent tool of record selection"）
- 2026-08-06｜CEO｜product：推出軟體平台 Nova Hub（原話："we introduced Nova Hub, a scalable platform"）
- 2026-08-06｜CEO｜product：CEO 稱混合鍵合是先進封裝成長的額外加速層（原話："We see the hybrid bonding as an additional"）
- 2026-08-06｜CEO｜product：Metrion／Elipson 目標是每個廠多台，複製 XPS 模式（原話："we're currently working on having multiple tools per fab."）
- 2026-08-06｜CFO｜customer：產品營收分布：邏輯／晶圓代工 73%、記憶體及其他 27%（原話："73% from logic and foundry and 27% from memory"）
- 2026-08-06｜CFO｜customer：兩家客戶各占產品營收 10% 以上（原話："two customers and four territories"）
- 2026-08-06｜CEO｜customer：客戶已下 2027 年訂單並規劃交貨（原話："already receiving orders and planning the 2027 deliveries."）
- 2026-08-06｜CEO｜customer：CEO 提到客戶拉貨（pull-in）影響上半年與下半年（原話："We did see some pull-ins by the way, that"）
- 2026-08-06｜CEO｜customer：記憶體：DRAM 需求強、3D NAND 需求偏弱（原話："strong demand from DRAM, somehow muted demand"）
- 2026-08-06｜CEO｜customer：CEO 拒絕評論個別客戶（Terafab）（原話："I am a bit reluctant to relate to specific customers"）
- 2026-08-06｜CEO｜competition：CEO 稱本輪循環的客戶能見度與親密度前所未有，與過往循環不可比（原話："it's an unprecedented cycle"）
- 2026-08-06｜CEO｜competition：ancosys 化學計量受惠於既有客戶深化與市占提升（原話："continued market share gains at"）
- 2026-08-06｜CEO｜competition：CEO 稱最重要指標為客戶採用、市占與技術勝出（原話："the most important indicators are customer adoption"）
- 2026-08-06｜CEO｜risk：CEO 承認供應鏈吃緊（原話："They are stretched, but we are managing production"）
- 2026-08-06｜CEO｜risk：交期依產品線介於 4 至 12 個月（原話："between 4 to 12 months at the latest"）
- 2026-08-06｜CEO｜risk：NAND 對 Nova 目前偏弱，成長來自升級而非擴產（原話："NAND at this point is a bit muted for us"）
- 2026-08-06｜CEO｜risk：CEO 說明今年記憶體占比預期略升（2025 為 70-30）（原話："this year's memory share is expected to grow slightly"）

### 問答異常語氣（迴避／改口／保留）
- NVMI_Q2_2026_Earnings_Call_20260806.md｜問：Barclays：2027 WFE 若成長 40%（約 2100–2150 億美元），Nova 能否支應或需要什麼｜答法：未回答能否支應 40% 情境，改談客戶規劃與訂單能見度，並稱太早判斷、供應鏈吃緊
- NVMI_Q2_2026_Earnings_Call_20260806.md｜問：Citi：定價策略、是否有旋鈕把目標毛利率模型調高｜答法：CEO 補充談與客戶長期夥伴關係並維持毛利率模型，未直接回答是否調價或提高目標區間
- NVMI_Q2_2026_Earnings_Call_20260806.md｜問：Evercore：交期現在與過去三個月相比如何變化｜答法：未給比較數字，回以「almost similar」並給 4–12 個月寬區間
- NVMI_Q2_2026_Earnings_Call_20260806.md｜問：Jefferies：Terafab 這類新建廠與一般擴廠相比的量測密集度與機會｜答法：明確表示不評論特定客戶，只給通用的新建廠量測密集度較高說法

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 4 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 4 | 3 |
| supply_demand_durability | found | 5 | 3 |
| regulatory_antitrust | found | 1 | 2 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 4 | 4 |
| end_markets | found | 10 | 4 |
| substitute_technology | found | 4 | 4 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | none | 0 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **channel_business_model_shift**（none）：Nova NVMI business model transition subscription OR platform OR distribution channel 2026；Nova Ltd go-to-market change direct sales distributors 2026 metrology
- **major_events**（none）：Nova Ltd NVMI acquisition merger 2026；Nova Ltd NVMI class action lawsuit securities fraud；Nova Ltd NVMI SEC investigation restatement warning letter recall

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261012","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"第四季財報或 2027 年投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上，且非 GAAP 毛利率 ≥58%","irr_base_pct":7.9,"ev5y_pct":40.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.9,"ev5y_pct":40.2,"irr_base_pct":7.9,"max_dd_pct":-50,"bull_5y_price":770.0,"bear_5y_price":234.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"第四季財報或 2027 年投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上，且非 GAAP 毛利率 ≥58%","price_at_dd":353.0,"archetype":"品質複利成長","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"NVMI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Nova Ltd."},"oneliner":"Q3 營收年增 28%、非 GAAP 毛利率 59.1%，但增量主要來自記憶體，邏輯／晶圓代工按比例回推季減；現價約 29 倍當年 EPS，報酬靠 EPS 複利，等第四季財報與 3 月投資人日驗證 2027 年跑贏 WFE。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺晶圓廠與封裝廠製程控制預算的錢，錢卡在先進製程每增加一道複雜步驟就必須多量一次的量測節點。","reasoning":"Q3（2026-11-05 法說）營收 2.878 億美元，年增 28%、季增 13%；GAAP 毛利率 57.7%、非 GAAP 59.1%，GAAP 營益率 32%、非 GAAP 35.5%。產品營收中邏輯／晶圓代工 61%、記憶體及其他 39%（Q2 為 73%／27%）。先進封裝約占四分之一，中國約三成。服務 Q2 為 5350 萬美元，約占營收 21%，Q3 創新高但金額未揭露。事實表的季度 KPI 停在 Q2，Q3 數字取自逐字稿。產業處於擴張期：SEMI 預測 WFE 2026 年增 23.1%、2027 年增 21.8%，客戶已下 2027 年訂單，增速放緩預期落在 2028 年（14.1%）。單點依賴有兩處：每條產品線各靠單一製造廠，部分零組件只有有限或唯一供應商。客戶面未過度集中，Q3 四家各占產品營收 10% 以上，2025 年揭露的 Customer B 為 10%。","fact_refs":["f_kpi0_revenue_gaap","f_kpi2_non_gaap_operating_margi","f_kpi4_gaap_operating_margin","f_earnings_recency"],"verdict_values":{"revenue_quality":"設備銷售為主，服務約兩成；2023–2025 累計 FCF 為淨利的 94%，獲利含金量高。","unit_econ_note":"單台設備單價與毛利事實表未涵蓋；XPS 每廠最高已到 9 台，增值服務年增約 50%，裝機基礎帶動後續收入。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"WFE 敞口高，但 2023 年營收減 9.25% 時 GAAP 營益率仍 25.54%、FCF 利潤率 20.53%，下行年仍賺錢。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：GAA、HBM 與先進封裝提高量測強度（Yole、2026-11-05 法說）；擴產量本身屬週期性，SEMI 預測 2028 年 WFE 增速降至 14.1%。","bargaining":{"up":"對上游偏弱：2026-11-05 法說承認供應鏈被拉長，需要管理層積極介入，關鍵零組件來源有限。","down":"對下游中等：大型晶圓廠議價力強，Nova 靠新功能調價，毛利率留在 57–60% 模型內，區間未調高。","geo":"中國約三成，受出口管制牽動。"},"profit_pool_dir":"事實表未涵蓋五年利潤池分布；方向上量測與檢測約占 WFE 14%，GAA 的量測強度較 FinFET 約高 30%。","tam_table":[{"item":"量測與檢測設備（Yole）","value":"2025 年逾 180 億美元，年增 15%，約占 WFE 14%"},{"item":"製程控制設備（GMI）","value":"2025 年 126 億、2026 年 135 億美元，CAGR 8.1%"},{"item":"製程控制設備（TBRC）","value":"2025 年 82.9 億、2026 年 88.2 億美元，CAGR 6.4%，定義不同不可直接比較"},{"item":"Nova 份額","value":"管理層轉述 Gartner：薄膜、SIMS 與關鍵尺寸量測再增約 400bp，排名第二；第三方估製程控制約 18%，無方法論"},{"item":"利潤池五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向穩定：執行面在擴大，定價面持平，XPS 新對手尚未到場。","reasoning":"機制是量測模型與製程配方綁定，加上整合式量測嵌入客戶機台，裝機基礎再帶來服務與升級。方向證據：管理層轉述 Gartner，薄膜、SIMS 與關鍵尺寸量測份額再增約 400bp，連兩年提升，排名第二；Metrion 已進入五大客戶中四家；AncoScene 通過一家領先晶圓代工廠的量產驗收。定價面只能算穩定：非 GAAP 毛利率留在 57–60% 模型內，2026-08-06 Citi 問能否調高區間時管理層未正面回答。對最強同業 KLA 的營益率仍低約 12.6 個百分點，事實表沒有同業 ROIC，無法驗證超額報酬差距是否擴大，因此評分不給到 8 分以上。","fact_refs":["f_peer_nvmi_gross_margin_pct","f_peer_nvmi_operating_margin_pct","f_peer_klac_operating_margin_pct","f_peer_onto_operating_margin_pct","f_peer_camt_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"量測模型與製程配方綁定，整合式量測嵌入客戶機台，換供應商要重新驗證；裝機基礎帶來服務與升級收入。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大（Gartner 份額再增約 400bp、Metrion 進入五大客戶中四家），定價面穩定（非 GAAP 毛利率 59.1%、模型區間未調高）；兩者合併為穩定，未因尚未到場的 XPS 對手下修。","competitor_notes":[{"name":"KLAC","strategy_note":"製程控制龍頭，也是前段化學量測的唯一對手，獲利能力仍明顯高於 Nova。"},{"name":"ONTO","strategy_note":"OCD 直接對手，以 Atlas G6 搶第二代 GAA 與 HBM 用 DRAM，並與 Rigaku 合作結合 X 光；是否就是法說提到的 XPS 新對手，證據包未涵蓋。"},{"name":"CAMT","strategy_note":"主攻先進封裝檢測，與 Nova 的封裝量測相鄰，目前未見直接搶份額的證據。"}],"peer_na_reason":"事實表沒有同業 ROIC，改用營益率差距與份額方向判讀。","threats":[{"level":"🟡","text":"XPS 新對手最快 2027 下半年進場，僅限 XPS，管理層加碼新一代產品因應。","p":"40%","evidence_refs":[]},{"level":"🟡","text":"Onto Atlas G6 OCD 瞄準第二代 GAA 與 HBM 用 DRAM，已取得多家量產訂單，同賽道直接競爭。","p":"35%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉率為定性判斷，事實表未涵蓋投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"量測是良率的必要投入，使用者、決策者與付款者都在晶圓廠內；Q3 增值服務年增約 50%，客戶追求產能最大化，提高稼動與升級需求。"},{"item":"決策層級","level":"🟡","text":"替代要看每一道製程的量測點；OCD 已有 KLA 與 Onto 可選，XPS 最快 2027 下半年出現第二來源。重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"量測與檢測約占 WFE 14%，買方集中，Q3 四家客戶各占產品營收 10% 以上；毛利率守在模型內，但管理層未回答能否調高區間。"},{"item":"社會容忍度","level":"🟢","text":"產品不是民生必需，沒有社會對漲價的上限；政治風險來自出口管制而非價格，已列入風險。"}],"roiic":"事實表未涵蓋投入資本，無法計算。代理觀察：2022 至 2025 年營收增加 3.10 億美元，Q2 資本支出僅 249 萬美元，資本負擔輕。","reinvest_rate":"事實表未涵蓋折舊、營運資金與收購淨額，無法按公式計算。代理觀察：2023–2025 累計 FCF 為淨利的 94%，但 FCF 含股權報酬加回，只能看方向。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩項輸入都缺，不給數字。"}}}},"q3_growth":{"verdict":"跑道寬：滲透率低且有多條下一段成長曲線，但 2026 年只跟上 WFE，超額成長要到 2027 年才能驗證。","reasoning":"成長以量為主（新廠擴產與每廠設備台數），其次是量測強度上升（GAA 較 FinFET 約高 30%），價格隨新功能小幅調整，併購不列入。共識 EPS FY2026E 至 FY2028E 年複利 24.7%（Koyfin，家數未揭露；營收共識 7 位分析師），若以 FY2025 GAAP EPS 為基期則為 27.7%，但基期口徑不同。內生上界無法計算，共識與內生的缺口無法歸因，加註依賴 re-rate，長期信心上限為中；基準情境實際是倍數下修，報酬靠 EPS 複利。跑道寬的依據：以 Yole 2025 年逾 180 億美元市場計，Nova 2026 年營收約當 6%，且有 GAA、HBM 封裝、混合鍵合、前段化學量測與 4F² 等下一段曲線。弱點是 2026 年營收約年增 24%，僅與 SEMI 的 WFE 增速 23.1% 相當，2026 年 9 月 Citi 會議摘要也提到今年超額成長較少。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主（新廠擴產、每廠設備台數），量測強度次之，價格隨新功能小幅調整，併購不列入。","runway_years":"≥10（Nova 營收約當 Yole 市場 6%，僅作方向參考）","runway_post_y5":"🟢","endo_ceiling_basis":"無法計算：事實表缺投入資本與再投資明細。公司輕資產且手握 18 億美元現金與投資，成長的限制在需求與份額，不在資本。","segments":[{"item":"邏輯／晶圓代工（占產品營收）","value":"Q2 73%，Q3 61%"},{"item":"記憶體及其他（占產品營收）","value":"Q2 27%，Q3 39%"},{"item":"先進封裝","value":"2025 年約占產品營收 20%，2026 年接近 25%"},{"item":"服務","value":"Q2 5350 萬美元；Q3 創新高但金額未揭露，增值服務年增約 50%"},{"item":"中國（占營收）","value":"2024 年約 39%，2025 上半年約 35%（第三方），2026 年約 30%，管理層稱長期 25–30%"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 GAAP 56.5% 低於去年同期 57.8%；Q3 回到 57.7%，去年同期基期事實表未涵蓋。"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"管理層轉述 Gartner 份額再增約 400bp。"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"未見證據。"},{"item":"EPS CAGR 高於營收 CAGR 逾 5 個百分點","lit":true,"note":"2022–2025 EPS 年複利 21.8%，營收 15.6%，差 6.2 個百分點；共識下一年差距約 1.8 個百分點。"},{"item":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2024 年 119%，2025 年 84%。"},{"item":"SBC／營收超過 5% 且上升","lit":false,"note":"Q2 推算約 2.7%。"},{"item":"TAM 萎縮或被替代","lit":false,"note":"未見具體替代技術證據。"},{"item":"產業倍數三年系統性下移","lit":false,"note":"事實表未涵蓋。"},{"item":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"Q2 資本支出僅 249 萬美元。"},{"item":"停止投資新產能且收入下滑","lit":false,"note":"加州無塵室已擴建，亞洲新無塵室預計年底啟用。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金生成強、稀釋輕，回購與併購的報酬仍無法驗證。","reasoning":"FY2025 FCF 為淨利的 84%，2024 年 119%；2026 前三季 FCF 約 2.06 億美元（Q3 1.32 億）。以 Q2 推算 SBC 約 678 萬美元，約占營收 2.7%，年化稀釋約 0.3%，低於 1.5%。現金去向四分、回購均價與債務到期結構事實表未涵蓋。已知 Q3 回購 3850 萬美元，2026 年 9 月宣布 2 億美元授權，期末現金與投資 18 億美元。情境樹的淨回購殖利率 0.7%：假設授權分兩年用完，每年約占市值 1.0%，扣除 SBC 約 0.3%。股息事實表未涵蓋，以 0 計。併購待驗證：Q3 營業費用含策略評估成本，2026-08-06 CFO 提到尋求選擇性併購。","fact_refs":["f_kpi5_free_cash_flow_40_92_cap","f_kpi6_sbc_gaap","f_kpi3_gaap_operating_income","f_kpi0_revenue_gaap"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事實表未涵蓋歷次併購金額與貢獻，無法計算已實現報酬。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與 10 年期公債殖利率事實表未涵蓋；以現價算 FY2026E 盈餘殖利率約 3.4%。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q2 SBC 約 678 萬美元，年化約 2710 萬美元，占市值約 0.3%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要靠內生設備出貨，併購不構成主力；現金去向四分事實表也未涵蓋，無法展開。"}}}},"q5_valuation":{"verdict":"現價要靠 EPS 五年複利約 15.5% 才有一成年化報酬，倍數還要從 29 倍降到 23 倍；我相信大方向，但 2027 年超額成長尚未驗證。","reasoning":"以 FY2026E 共識 EPS 10.67 美元計，本益比 29.35 倍；FY2027E 為 22.93 倍。要得到 10% 年化，終端 23 倍下 FY2031E EPS 需約 21.9 美元，五年複利約 15.5%，與基準路徑 21.5 美元接近。PEG 以 FY2026E 至 FY2028E 年複利 24.7% 計約 1.19，屬合理區間。Trailing 本益比 35.87 倍位於 4 個年度端點的 67.5 分位，這不是五年分位，五年分位事實表未涵蓋。同業現值倍數事實表也未涵蓋，終端倍數只能以自身現值 29.35 倍對照，這是本次估值的明確缺口。半年跌四成不等於有安全邊際。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ev_s_current","f_ev_s_fwd","f_week26_return_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"FY1 非 GAAP 本益比，輔以 FY2 本益比與 PEG；不用 EV/S 當主尺，因公司已穩定獲利，且事實表現金口徑低估。","tier":"中型製程控制設備","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法做倍數對照。"},"fwd_pe":29.35,"peg":1.19,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"PEG 1.19 屬合理，基準年化約一成屬中段，Trailing 本益比位於年度端點中上，綜合為中性。短期：FY2027E 13.7 美元×26 倍＝356 美元，上行 13.7%；中期：FY2028E 16.2 美元×25 倍＝405 美元，上行 29.3%。","upside_short_pct":13.7,"upside_mid_pct":29.3,"denominator_disputed":false,"denominator_note":"EPS 為非 GAAP，Q3 較 GAAP 高約 8%；財務收入每季約 1870 萬美元，約占稅前 14%，不是一次性，但會隨現金運用變動。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把記憶體帶動的 Q3 當成全面加速，以及低估中國管制與 XPS 競爭同時發生的機率。","reasoning":"負向證據與處置都在反證紀錄。價值陷阱風險為低到中度：十類衰退信號亮一項，即 2022–2025 年 EPS 複利高於營收 6.2 個百分點。歷史最大回撤事實表未涵蓋，僅知近 26 週跌 39.91%，回撤區間以 Bear 路徑與 250 週均線推估。2026-08-06 法說有四題未正面回答：2027 年 WFE 若成長 40% 能否支應、是否調高毛利率區間、交期相對三個月前的變化、特定新建廠客戶的量測機會。","fact_refs":["f_week26_return_pct","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"低到中度，一項衰退信號亮燈"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.67,"pe":29.35,"basis":"FY2026E 共識（Koyfin 2026-11-07，非 GAAP），與終端倍數同為當年度 EPS 口徑；FY2026 已走完三季。"},"eps":{"bull":[15.0,19.5,23.0,27.0,31.0],"base":[13.7,16.2,16.7,19.0,21.5],"bear":[12.2,11.4,9.8,11.0,12.5]},"pe":{"bull":26,"base":23,"bear":17.5},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.7},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"max_dd":{"lo":-50,"hi":-35,"basis":"現價 313.18 美元。下緣：Bear 路徑最低 EPS 9.8 美元×17.5 倍＝171.5 美元（−45%），再留 5 個百分點給情緒過度，取 −50%。上緣：跌到 250 週均線 212.61 美元約 −32%，取 −35%。事實表未涵蓋歷史最大回撤，僅知近 26 週已跌 39.91%。","trigger_time":null},"basis":{"bull":"2027 年 WFE 成長接近 40%，GAA 強度與份額雙升，記憶體與封裝延續，FY2027 營收約 15 億美元、非 GAAP 營益率約 37%，五年內沒有明顯循環回落；26 倍低於現值 29.35 倍，同業現值倍數事實表未涵蓋。","base":"FY2027 貼近共識，FY2028 略低於共識（XPS 競爭與 WFE 放緩），FY2029 為消化年，之後隨製程控制市場與份額複利；倍數由 29 倍降到 23 倍，同業現值倍數事實表未涵蓋，僅以自身現值對照。","bear":"記憶體循環先反轉，中國受限，XPS 被分食，FY2029 EPS 跌到 9.8 美元，五年後僅回到 12.5 美元；17.5 倍是成長降到約一成時的判斷倍數，同業現值倍數事實表未涵蓋。"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"五年虧五成最可能的路徑是兩件事疊加：中國約三成營收遇到管制擴大，同時記憶體循環回落。Q3 記憶體及其他占比由 27% 升到 39%，邏輯／晶圓代工按比例回推季減至少約 3%。","assumption":"2027 年 GAA 投資能接手記憶體，中國維持 25–30%。","consequence":"FY2029 EPS 落到約 10 美元，倍數 17.5 倍，股價約 170 美元，較現價跌約 45%；管制若全面擴大則更低。","ruling":"採納為 Bear 主線，Bear 機率 30%；與 Single Thing 部分重疊，中國管制是最大單一項，記憶體回落是放大器。","watch":"每季邏輯／晶圓代工金額、記憶體占比、中國占比。","evidence_refs":["supply_demand_durability#4","reg_tariff_export#1"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營業費用含策略評估成本，2026-08-06 CFO 提到尋求選擇性併購，帳上現金與投資 18 億美元；同時加州無塵室與亞洲新無塵室都在擴產。","assumption":"現金會以高於資金成本的報酬配置，擴產不會在下行期變成固定成本負擔。","consequence":"營收與份額都達標，但大型併購或閒置產能壓低每股價值，股東報酬落後於營運成績。","ruling":"部分採納：基準情境不含併購，淨回購殖利率只算 0.7%，併購超過市值 5% 列為風險條件。","watch":"併購金額、兩年後報酬、營業費用增速。","evidence_refs":[]},{"view":"價格已反映太多","evidence":"FY2026E 本益比 29.35 倍，Trailing 35.87 倍，位於年度端點 67.5 分位；賣方目標在 8 月後仍被下調。","assumption":"FY2027 EPS 達到 13.66 美元，市場願意給 25 倍以上。","consequence":"FY2027 EPS 只有 12.2 美元且倍數 20 倍時，股價約 244 美元，跌約 22%。","ruling":"部分採納：股價已跌四成，但倍數仍不便宜，不能把跌幅當安全邊際。","watch":"FY2027 共識方向與本益比。","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile"]},{"view":"論點失敗","evidence":"2026-11-05 法說確認 XPS 新對手最快 2027 下半年進場，共識快照三個年度修正皆 0%，這項利空是否進入賣方模型無法確認。","assumption":"Nova 的性能與持有成本領先足以守住 XPS 的單價與份額。","consequence":"XPS 每廠最高已到 9 台，若第二供應商切入，材料量測業務最先受影響；XPS 營收占比事實表未涵蓋，無法量化。","ruling":"採納：出現首個客戶採用或否證的數據點之前，凍結加碼。","watch":"領先客戶採用對手 XPS 的消息與毛利率。","evidence_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 353.0 → 本次 313.18（-11.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=353.0","side_b":"本次 price_at_dd=313.18","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 353 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 353 美元：Bull 價 770、Bear 價 234，五年期望值 +40.2%，基準年化 7.9%，不對稱比 2.9","side_b":"本次情境、股價仍用 353 美元：Bull 價 806、Bear 價 218.75，五年期望值 +38.7%，基準年化 7.0%，不對稱比 2.81","ruling":"先換情境、股價不動：五年期望值少 1.5 個百分點，基準年化少 0.9 個百分點。不對稱比由 2.9 變為 2.81。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 353 美元：五年期望值 +38.7%，基準年化 7.0%，不對稱比 2.81","side_b":"本次情境、股價 313.18 美元：五年期望值 +56.3%，基準年化 9.6%，不對稱比 4.35","ruling":"再換股價、情境不動：起點價下跌 11.3%，五年期望值多 17.6 個百分點，基準年化多 2.6 個百分點，不對稱比由 2.81 升到 4.35。合計五年期望值比前份多 16.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與機率","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 353 美元，估值中性，Bull 機率 25%、Bear 機率 30%，最大回撤 −50%。","side_b":"本次股價 313.18 美元，估值仍中性，Bull 25%、Base 45%、Bear 30%，回撤區間 −50% 至 −35%。","ruling":"股價較前份跌約 11%，FY2026E 本益比仍 29.35 倍、PEG 約 1.19，尚未進入便宜區，估值結論與機率都不變。","evidence_level":"高","settle_metric":"FY2026E 本益比與 FY2027 共識方向","if_then":["若股價漲過 FY2027E 30 倍（約 410 美元）而驗證未到，則不追","若股價跌破 FY2027E 18 倍（約 246 美元）且基本面無損，則分批反買"],"evidence_refs":[]},{"axis":"護城河、陷阱風險、跑道與公司類型","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5","archetype"],"side_a":"前份：護城河方向穩定，陷阱風險中度，跑道寬，屬品質複利成長。","side_b":"本次四項結論相同；新增事實包括 XPS 新對手時程（2027 下半年）、Metrion 進入五大客戶中四家、Q3 非 GAAP 毛利率 59.1%。","ruling":"正負新證據相抵，四項維持。XPS 對手尚未到場，不提前下修方向，改列為觸發條件。","evidence_level":"中","settle_metric":"領先客戶是否量產採用對手 XPS","if_then":["若任一前五大客戶量產採用對手 XPS，則護城河方向下修為縮減，已持有部位減碼一半"],"evidence_refs":[]},{"axis":"綜合評等與觀望約束","cause":"新證據","prior_field":["signal"],"side_a":"前份觀望，綜合評等 B，約束是 2027 年超額成長未驗證。","side_b":"本次綜合評等仍 B，約束未解除，前份留存的重啟條件尚未發火；Q3 高於指引上緣，但沒有 2027 年營收與 WFE 的數字對照。","ruling":"現在就買的最強論證：股價半年跌四成，FY2027E 僅 22.93 倍，Q3 高於指引上緣，Q4 指引中點高於 8 月共識，2027 年訂單已進來，現金與投資 18 億美元。不買的理由：Q3 增量主要來自記憶體，邏輯／晶圓代工按比例回推季減，2027 年超額成長仍是管理層口頭說法。等待的代價是股價可能先反彈，可以接受，因為 4 個月內有兩個驗證點。","evidence_level":"中","settle_metric":"第四季財報與 2027-03-09 投資人日的 2027 年展望","if_then":["若驗證條件成立，則重做完整研究後以不超過 3% 建首倉","若股價先漲但證據未到，則不追","若股價續跌而基本面無損，則分批反買","若 2027 年營收成長低於 WFE 且邏輯／晶圓代工未回升，則已持有部位清倉"],"evidence_refs":[]},{"axis":"循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"前份：中循環。","side_b":"本次：中循環，但出現偏晚跡象。","ruling":"SEMI 預測 2027 年 WFE 仍增 21.8%，客戶排定 2027 年交貨，尚未見砍單。供應鏈吃緊、2026-08-06 CEO 提到客戶拉貨、Q3 記憶體急升，都是週期中後段現象。沒有訂單下滑或庫存上升的證據，因此維持中循環。","evidence_level":"中","settle_metric":"2028 年 WFE 預測、公司訂單與庫存","if_then":["若 2027 年 WFE 預測被下修或記憶體占比連 2 季回落，則停止加碼"],"evidence_refs":[]},{"axis":"首倉與加碼條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"第四季財報或 2027 年投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上，且非 GAAP 毛利率 ≥58%","side_b":"第四季財報或 2027-03-09 投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上、非 GAAP 毛利率 ≥58%，且邏輯／晶圓代工產品營收恢復季增","ruling":"舊→新：保留 WFE 差距與毛利率兩條，新增邏輯／晶圓代工恢復季增。理由是 Q3 增量來自記憶體，若邏輯不回升，跑贏 WFE 也可能只是記憶體循環，不代表 GAA 論點成立。","evidence_level":"中","settle_metric":"第四季邏輯／晶圓代工占比×產品營收","if_then":["若三項條件同時成立，則重做研究後建首倉","若只有 WFE 差距成立而邏輯未回升，則不追"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空，無原文可對照。","side_b":"美國或以色列把對中國的設備出口限制擴大到成熟製程，Nova 的中國營收（約占三成）大部分無法出貨。","ruling":"本次補上。選此事件是因為它的單一敏感度最大：約三成營收受影響，按 FY2027E 共識估 EPS 少約 5.8 美元（−42%）。發生時清倉。","evidence_level":"中","settle_metric":"出口管制公告與季度中國占比","if_then":["若規定生效且影響中國營收一半以上，則清倉"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空，無原文可對照。","side_b":"本次新設五項：毛利率、邏輯／晶圓代工營收、中國占比、XPS 對手採用、2027 年營收與 WFE 差距。","ruling":"前份留存不足，本次重建門檻；觸及毛利率、邏輯或 XPS 門檻就減碼，觸及 Single Thing 就清倉。","evidence_level":"中","settle_metric":"五項指標的季度讀數","if_then":["若兩項以上同時觸及，則已持有部位清倉"],"evidence_refs":[]},{"axis":"管理層對記憶體占比的說法","cause":"新證據","side_a":"2026-08-06 CEO：今年記憶體約占 30%，比重僅略升。","side_b":"2026-11-05 CFO：Q3 記憶體及其他占產品營收 39%；Morgan Stanley 分析師推算記憶體年增逾 60%，CEO 未否認，只說強勁雙位數成長。","ruling":"可調和，屬程度差異：39% 是單季且含其他。全年比重可能高於 8 月說法，代表成長組合比管理層當時描述的更偏記憶體，週期敏感度也更高。","evidence_level":"中","settle_metric":"第四季記憶體占比與 2027 年組合展望","if_then":["若 2027 上半年記憶體及其他占比維持 35% 以上而邏輯未回升，則停止加碼"],"evidence_refs":[]},{"axis":"邏輯／晶圓代工是否走弱","cause":"新證據","side_a":"2026-11-05 CEO 回應 BofA：不算疲弱，先進與成熟製程都有實質成長。","side_b":"Q2 邏輯／晶圓代工約 1.47 億美元（2.015 億×73%）。Q3 服務創新高，產品營收必低於 2.343 億，乘以 61% 不到 1.43 億，季減至少約 3%。","ruling":"可調和但尚未驗證：全年可能仍成長，單季確實下滑。要到第四季財報才能判斷這是 GAA 切換前的空檔還是份額問題。","evidence_level":"中（由揭露比例回推）","settle_metric":"第四季邏輯／晶圓代工占比×產品營收","if_then":["若第四季仍季減，則不追","若連 3 季季減，則已持有部位減碼一半"],"evidence_refs":[]},{"axis":"毛利率是否下滑","cause":"新證據","side_a":"Q2 GAAP 毛利率 56.5%，低於 Q1 的 57.7% 與去年同期 57.8%；2026-08-06 CFO 歸因於產品組合。","side_b":"Q3 GAAP 57.7%、非 GAAP 59.1%，Q4 指引非 GAAP 約 59%。CFO 說未見逆風，但 Q4 之後成本上升，要靠效率、量與調價抵銷。","ruling":"可調和：Q2 屬單季組合，Q3 已回升，8 月全年約 59% 的承諾目前做到。組合歸因未完全證實，若記憶體占比高時毛利率再跌，就證偽。","evidence_level":"中","settle_metric":"TTM 非 GAAP 毛利率","if_then":["若非 GAAP 毛利率連 2 季低於 58%，則停止加碼","若連 4 季低於 56%，則已持有部位減碼一半"],"evidence_refs":["end_markets#2"]},{"axis":"現金與稀釋口徑","cause":"新證據","side_a":"事實表淨現金 2.75 億美元（現金 10.77 億、總債務 8.02 億），股數 3181 萬股。","side_b":"2026-11-05 CFO：現金、銀行存款與有價證券共 18 億美元。由 Q4 指引中點回推非 GAAP 稀釋股數約 3460 萬股。","ruling":"採公司現金口徑，差額約 7.2 億美元的組成事實表無法證實。情境樹用 EPS×本益比，不受影響；EV 類倍數偏高。稀釋市值約 108 億美元，高於事實表 99.6 億，差額可能來自選擇權或可轉債。","evidence_level":"中","settle_metric":"下一份資產負債表與稀釋股數揭露","if_then":["若第四季稀釋股數高於 3600 萬股，則下修每股 EPS 路徑並停止加碼"],"evidence_refs":[]},{"axis":"賣方目標與現價","cause":"新證據","side_a":"2026 年 9 月 Benzinga：10 位分析師平均目標價約 491 美元，高 640、低 240，全距 2.67 倍；Citi 由 595 降至 550，Needham 由 640 降至 570。","side_b":"現價 313.18 美元，低於平均目標價約 36%，近 26 週跌 39.91%。","ruling":"不採用平均目標價當上行依據：快照早於股價後段下跌，全距超過 2.5 倍，代表賣方對週期定位分歧很大，因此下調對上下行比的信心。本次比賣方保守，但沒有足夠證據說市場錯在哪裡，證據包也未說明股價下跌的原因。","evidence_level":"中","settle_metric":"第四季財報後的目標價與 FY2027 共識","if_then":["若目標價續降而 FY2027 EPS 共識未降，則分批反買的條件才算成立","若 FY2027 EPS 共識下修超過 10%，則不追"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"共識快照是否可用","cause":"新證據","side_a":"共識修正三個年度皆 0%，近 90 天 FY1 由 10.67 到 10.67。","side_b":"Q3 已高於指引上緣；Q1 至 Q3 實績加 Q4 指引中點，全年營收約 10.89 億美元，高於 FY1 共識 10.777 億。","ruling":"快照可能未更新，0% 不能解讀為分析師看法不變，本次不把共識修正當正面或負面依據。","evidence_level":"中","settle_metric":"下一次共識快照","if_then":["若下一次快照 FY2027 EPS 仍未變動，則視為資料缺口，不追"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","side_a":"競爭：XPS 新對手 2027 下半年進場，Onto 推新 OCD 平台。","side_b":"結構：GAA 量測強度約高 30%，HBM 與封裝擴大，WFE 連兩年兩成以上。其他：出口管制與關稅持續。","ruling":"雙向拉鋸：結構順風目前大於競爭壓力，但競爭壓力要到 2027 下半年才開始顯現，出口管制是獨立的尾端風險。","evidence_level":"中","settle_metric":"Gartner 年度份額與毛利率","if_then":["若份額下滑且毛利率跌破 57%，則已持有部位減碼一半"],"evidence_refs":["substitute_technology#1"]}],"triggers":[{"n":1,"text":"2027 年營收成長相對 WFE 的差距","type":"假設驗證","maps_to":"H1","metric":"FY2027 營收年增率減全年 WFE 年增率","threshold":"≥5 個百分點","action":"成立且另兩項條件達成，則重做研究後建首倉；低於 0 則已持有部位減碼一半","source_freq":"季報、投資人日、SEMI 更新","date":"2027-03-09"},{"n":2,"text":"毛利率守在模型內","type":"假設驗證","maps_to":"H2","metric":"TTM 非 GAAP 毛利率","threshold":"≥57%","action":"連 2 季低於 57% 則停止加碼","source_freq":"每季財報","date":"每季"},{"n":3,"text":"下行年仍維持獲利","type":"假設驗證","maps_to":"H3","metric":"WFE 下行年的 GAAP 營益率與 FCF 利潤率","threshold":"營益率 ≥25%、FCF 利潤率 ≥20%","action":"跌破則已持有部位減碼一半","source_freq":"年報","date":"下一次 WFE 下行年"},{"n":4,"text":"XPS 第二來源進入領先客戶","type":"風險","maps_to":"R1","metric":"前五大客戶量產採用對手 XPS","threshold":"任一家","action":"減碼一半","source_freq":"法說、Gartner 年度報告","date":"2027-07 至 2028-12","evidence_refs":["substitute_technology#1"]},{"n":5,"text":"邏輯接不上記憶體","type":"風險","maps_to":"R2","metric":"邏輯／晶圓代工產品營收季變化、總營收季變化","threshold":"邏輯連 3 季季減，或季營收連 2 季季減逾 5%","action":"減碼一半","source_freq":"每季法說","date":"每季","evidence_refs":["supply_demand_durability#4"]},{"n":6,"text":"中國營收受管制衝擊","type":"風險","maps_to":"R3","metric":"中國占營收比重","threshold":"單季低於 20% 且管理層歸因於管制","action":"減碼一半","source_freq":"每季法說、年報","date":"每季","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":7,"text":"供應鏈限制出貨","type":"風險","maps_to":"R4","metric":"季營收相對指引下緣、交期上緣","threshold":"低於下緣且歸因供應，或交期上緣超過 12 個月","action":"停止加碼","source_freq":"每季法說","date":"每季","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":8,"text":"大型併購","type":"風險","maps_to":"R5","metric":"單筆併購金額","threshold":"超過市值 5%（約 5 億美元）","action":"停止加碼，直到併購報酬可驗證","source_freq":"公司公告","date":"事件驅動"},{"n":9,"text":"出口管制擴及成熟製程","type":"Single Thing","maps_to":"Single Thing","metric":"管制範圍與中國營收影響","threshold":"規定生效且影響中國營收一半以上","action":"清倉","source_freq":"法規公告、每季法說","date":"事件驅動"},{"n":10,"text":"首倉條件","type":"估值rearm","maps_to":"H1","metric":"2027 年營收與 WFE 差距、非 GAAP 毛利率、邏輯／晶圓代工季變化","threshold":"差距 ≥5 個百分點、毛利率 ≥58%、邏輯恢復季增，三項同時成立","action":"重做完整研究後以不超過 3% 建首倉","source_freq":"第四季財報、投資人日","date":"2027-03-09"},{"n":11,"text":"驗證後加碼","type":"加碼","maps_to":"H1","metric":"FY2027 EPS 共識修正與邏輯／晶圓代工占比","threshold":"共識上修 ≥10% 且占比回到 65% 以上","action":"加碼至 5%","source_freq":"共識快照、每季法說","date":"2027-Q2"},{"n":12,"text":"估值過高減碼","type":"減碼","maps_to":"H1","metric":"FY2027E 本益比","threshold":"高於 35 倍（約 478 美元）","action":"減碼三分之一","source_freq":"每日股價","date":"持續"},{"n":13,"text":"投資人日後完整複審","type":"複審日期","maps_to":"H1","metric":"新五年計畫與 2027 年展望","threshold":"不適用","action":"更新情境樹與結論","source_freq":"投資人日","date":"2027-03-15"}],"kill_metrics":[{"metric":"TTM 非 GAAP 毛利率","bear_threshold":"連 4 季低於 56%","window":"2027–2028 年","source":"公司季報","last_status":"ok"},{"metric":"邏輯／晶圓代工產品營收（占比×產品營收）","bear_threshold":"連 3 季季減","window":"連續 4 季","source":"每季法說","last_status":"warning"},{"metric":"中國占營收比重","bear_threshold":"單季低於 20% 且歸因於管制","window":"未來 12 個月","source":"每季法說、年報","last_status":"ok"},{"metric":"前五大客戶量產採用對手 XPS","bear_threshold":"任一家","window":"至 2028 年底","source":"法說、Gartner 年度報告","last_status":"ok"},{"metric":"FY2027 營收成長減 WFE 成長","bear_threshold":"低於 0 個百分點","window":"FY2027","source":"公司財報、SEMI","last_status":"unknown"}],"evidence_dismissed":[{"ref":"customer_concentration_credit#3","reason":"證據把 Intel 當成 Nova 客戶是推測，Nova 未具名客戶，評等動作也是 2025 年資料，無法連到 Nova 的應收帳款或訂單。"},{"ref":"reg_tariff_export#4","reason":"來源是 SEALSQ 的證券發行文件，談該公司的供應鏈，未提 Nova 的出貨或成本，也沒有 Nova 關稅影響的數字。"}],"action_conditions":{"rearm_trigger":"第四季財報或 2027-03-09 投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上、非 GAAP 毛利率 ≥58%，且邏輯／晶圓代工產品營收恢復季增","exec_line":"目前不建倉。條件成立後重做完整研究，再以小倉起步；股價先漲但證據未到就不追，股價續跌而基本面無損可分批反買。","holding_cap":"條件成立前不建倉，起步倉不超過 3%"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"不設進場價，等事件：第四季財報與 2027-03-09 投資人日能否驗證 2027 年營收成長高於 WFE 5 個百分點、非 GAAP 毛利率 ≥58%，且邏輯／晶圓代工產品營收恢復季增。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"觀望","prior_role":"追蹤"},"thesis":{"H":[{"id":"H1","text":"2027 年營收成長跑贏 WFE：GAA 投資比重上升、記憶體擴產延續，Nova 從 2026 年只跟上 WFE 轉回超額成長。","2y":"FY2027 營收達 13.6 億美元以上，成長率高於全年 WFE 5 個百分點以上","5y":null,"10y":null,"threshold":"FY2027 營收年增率減 WFE 年增率 ≥5 個百分點","source":"公司季報、2027-03-09 投資人日、SEMI 更新值","drift_rule":"TTM 營收連 2 季低於共識路徑 5% 以上視為削弱，連 3 季低於 10% 以上視為反轉"},{"id":"H2","text":"份額與定價守得住：面對 XPS 新對手與 Onto 新 OCD 平台，非 GAAP 毛利率留在 57–60%，份額不掉。","2y":null,"5y":"2031 年前 Gartner 口徑份額不低於 2025 年水準，年度非 GAAP 毛利率 ≥57%","10y":null,"threshold":"年度非 GAAP 毛利率 ≥57%；Gartner 薄膜、SIMS 與關鍵尺寸量測份額年度不降","source":"公司季報；Gartner 年度報告（目前僅有管理層轉述）","drift_rule":"TTM 非 GAAP 毛利率偏離 59% 中樞，連 4 季達 5% 以上（低於約 56%）視為削弱，連 6 季達 10% 以上（低於約 53%）視為反轉"},{"id":"H3","text":"全週期賺錢能力：WFE 下行年仍有 GAAP 營益率 25% 以上、FCF 利潤率 20% 以上，現金足以支撐研發與回購。","2y":null,"5y":null,"10y":"下一次 WFE 衰退年的 GAAP 營益率 ≥25%、FCF 利潤率 ≥20%（2023 年為 25.54%、20.53%）","threshold":"WFE 下行年 GAAP 營益率 ≥25%、FCF 利潤率 ≥20%","source":"公司年報與季報","drift_rule":"跨 2 個年度低於門檻視為削弱，跨 3 個年度視為反轉"}],"R":[{"id":"R1","text":"XPS 新對手 2027 下半年進場，Onto 新 OCD 平台同步搶量，份額與定價受壓。","h_ref":"H2","clock":"🔥","threshold":"前五大客戶任一家量產採用對手 XPS，或 TTM 非 GAAP 毛利率連 4 季低於 56%","evidence_refs":["substitute_technology#1"]},{"id":"R2","text":"記憶體與先進封裝擴產放緩，Q3 靠記憶體帶動的成長反轉，WMC 等設備利用率下滑，大客戶撤單。","h_ref":"H1","clock":"🔥","threshold":"邏輯／晶圓代工連 3 季季減，或季營收連 2 季季減逾 5%","evidence_refs":["supply_demand_durability#4"]},{"id":"R3","text":"中國約三成營收受出口管制與關稅牽動，第三方資料顯示占比已由 2024 年約 39% 降到 2025 上半年約 35%，Q3 占比回升。","h_ref":"H1","clock":"⚡","threshold":"單季中國占營收低於 20% 且管理層歸因於管制，或因管制下修當季指引 5% 以上","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R4","text":"製造集中在以色列、美國與德國，每條產品線靠單一廠區，部分零組件來源有限，Q3 法說承認供應鏈被拉長。","h_ref":"H1","clock":"⚡","threshold":"季營收低於指引下緣且歸因供應，或交期上緣超過 12 個月","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R5","text":"併購用掉現金但報酬低於資金成本；Q3 營業費用已含策略評估成本。","h_ref":"H3","clock":"🐢","threshold":"單筆併購超過市值 5%（約 5 億美元），兩年後報酬低於資金成本","evidence_refs":[]}],"single_thing":{"description":"美國或以色列把對中國的設備出口限制擴大到成熟製程，Nova 的中國營收（約占三成）大部分無法出貨。","why_fatal":"這是最大的單一敏感度：FY2027E 共識營收 13.6 億美元的三成約 4.1 億，按 59% 毛利、營業費用不變、稅率 17%、稀釋股數約 3460 萬股推算，EPS 少約 5.8 美元，約為 13.66 美元的 42%。","if_happens":"清倉，確認剩餘營收的獲利能力後才重新研究。","how_monitor":"美國商務部與以色列出口管制公告；每季法說的中國占比與當季指引。","probability":"12–24 個月約 10%，為主觀判斷；證據包僅有風險因子，未見針對 Nova 的具體行動。"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.93,"peg_fy2":0.93,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":7.96,"FY2026E":10.67,"FY2027E":13.66,"FY2028E":16.59},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 2026-11-07 共識，對照季度指引判定為非 GAAP；FY2025A 7.96 美元為 yfinance GAAP 稀釋 EPS，事實表未涵蓋 FY2025 非 GAAP EPS，基期口徑不一致。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"capacity","event":"亞洲新無塵室預計年底啟用","impact":"低","watch":"對毛利率與供應彈性的影響"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"第四季財報與 2027 年展望","impact":"高","watch":"邏輯／晶圓代工金額、記憶體占比、非 GAAP 毛利率"},{"date":"2027-03-09","type":"guidance","event":"紐約投資人日，公布下一階段策略","impact":"高","watch":"2027 年相對 WFE 的成長目標與新財務模型"},{"date":"2027-Q3","date_precision":"quarter","type":"product","event":"XPS 新對手最快進場","impact":"高","watch":"領先客戶評估與採用進度"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-39.91, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='不設進場價，等事件：第四季財報與 2027-03-09 投資人日能否驗證 2027 年營收成長高於 WFE 5 個百分點、非 GAAP 毛利率 ≥58%，且邏輯／晶圓代工產品營收恢復季增。'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：channel_business_model_shift（通路／商業模式轉移）、major_events（重大事件（QC-19））（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
