你是 DD 管線 v20 的判斷層閘（gate），標的 TTMI（20261025）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1203.855 USD M；YoY +60%（Q3 2025 752.7）；QoQ 約 +20%（Q2 約 1,005，由 adj. EBITDA 166.8÷16.6% 反推）｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
  - 註記：公司 Q3 指引 1,100–1,140，實績高於區間上緣
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝208.996 USD M；利益率 17.4%｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝162.253 USD M；利益率 13.5%（Q3 2025: 71.9）｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
- `f_kpi5_q4_2026`（q1_business）｜管理層指引：Q4 2026＝net_sales_B 1.42–1.44；non_gaap_eps 1.77–1.83 USD｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
- `f_kpi7_fy2027`（q1_business）｜管理層初步 FY2027 預測＝net_sales_B 6.5–6.75；non_gaap_eps 8.10–8.90 USD｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
  - 註記：yfinance FY2 營收共識 6,587M（落在區間內）
- `f_kpi8_book_to_bill`（q1_business）｜Book-to-bill＝2.13 倍｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
- `f_kpi9_a_d_backlog`（q1_business）｜A&D 專案 backlog＝2.0 USD B｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
- `f_kpi10`（q1_business）｜終端市場占比：資料中心與網通＝41 %（Q3 2025: 30%）｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
- `f_peer_ttmi_gross_margin_pct`（q2_moat）｜TTMI 毛利率＝21.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TTMI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ttmi_operating_margin_pct`（q2_moat）｜TTMI 營業利益率＝9.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TTMI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ttmi_fcf_margin_pct`（q2_moat）｜TTMI FCF 利潤率＝-0.45 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TTMI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2368_tw_operating_margin_pct`（q2_moat）｜2368.TW 營業利益率＝26.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2368.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_operating_margin_pct`（q2_moat）｜3037.TW 營業利益率＝10.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sanm_operating_margin_pct`（q2_moat）｜SANM 營業利益率＝5.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SANM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝4.96 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝8.34 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝10.06 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝4474.05 USD m｜期間與口徑：2026-10-25／yfinance revenue_estimate 0y 平均（5 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6586.72 USD m｜期間與口徑：2026-10-25／yfinance revenue_estimate +1y 平均（5 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝74.79 USD M（營業現金流 154.7 − 淨資本支出 79.9）｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
- `f_kpi4_sbc`（q4_capital）｜SBC＝24.09 USD M；占營收 2.0%、占 GAAP 營業利益 14.8%（由 SBC÷數值自算）｜期間與口徑：Q3 FY2026（季末 2026-09-28，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（SEC，同步 investors.ttm.com） https://www.sec.gov/Archives/edgar/data/0001116942/000119312526428263/d282109dex991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-28，公告於 2026-10-22））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝767.52 USD m｜期間與口徑：2026-10-25／yfinance 最新一季：總債務 1643.87、現金 876.35（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝80.11 USD｜期間與口徑：2026-10-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝16.15 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 4.96，分子＝快照價 80.11｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝32.04 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／3 個年度端點內的分位＝50.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝50.8 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝81.3 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝82.0 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝22.77 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 4.04 → 4.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝9207.02 USD m｜期間與口徑：2026-10-25／市值 8439.5 ＋ 淨負債 767.52｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-46.24 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝33.07｜期間與口徑：2026-10-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（18 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：公司承認可能因競爭失去份額，且新興技術可能帶來新進入者。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Zacks 稱 Sanmina 以其北美、歐洲、亞洲製造足跡，對 TTMI 的歐洲擴張構成直接挑戰。
  - 來源：Zacks：TTMI's Europe expansion adds capabilities, can it drive growth（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：Zacks 稱 Sanmina 擴充高階 PCB 產能（AI、航太國防），為 TTMI 在先進應用更直接的 PCB 對手；Amphenol 透過 Wilder Technologies 強化高速電子。
  - 來源：Zacks：TTMI 競爭相關文章（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 前五大 OEM 客戶占淨銷售約 44%（2024 年 42%、2023 年 41%），兩家客戶合計占 23%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：前十大客戶占淨銷售 55%（2025），高於 2024 年 42% 與 2023 年 41%。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-17）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2025 年底有一家客戶占應收帳款 14%；2024 年底無客戶達 10%。公司不要求擔保品。
  - 來源：SEC EDGAR 10-K FY2025 附註3（as_of 2026-02-17）｜affects：decision_inputs.bear
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：二手來源整理：TTM 兩大客戶占 2025 年營收 23%、前五大 44%；Penang 與 Syracuse 擴產需數億美元資本支出，需求若放緩（資料中心建置趨緩或 AI 硬體架構改變）則產能利用率與毛利有風險（Simply Wall St 敘事，未對照公司文件）
  - 來源：Simply Wall St: Is AI Infrastructure Demand Quietly Reshaping TTM Technologies' Long-Term Competitive Moat?（as_of 2026-10-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：TTM 10-K 披露約 50% 淨銷售來自非美國營運，大量製造材料來自國際供應商；美中兩國均已將 PCB 列入進口關稅項目，可能影響營收與獲利。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：TTM 在中國有重大製造據點，面臨美中地緣風險；已透過擴充馬來西亞與美國產能部分緩解
  - 來源：CB Insights TTM profile（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：部分背板與 PCB 組裝零件為有限或單一供應來源，有時因客戶指定；覆銅板為主要原料且多數材料有多家供應商
  - 來源：TTM FY2018 10-K（as_of 2019-03-01）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：TTM 10-K 風險因素自述：PCB 產業競爭激烈、高度分散且快速變動；新興技術可能帶來新競爭者；製程技術通常不受重大專利保護；若無法因應快速技術變化，可能無法有效競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Benzinga 2026-09-25 快照：4 位分析師皆 Buy，平均目標價 $167；最近動作為 Needham 於 2026-09-21 將目標價由 $220 降至 $175。
  - 來源：Benzinga TTMI price targets（as_of 2026-09-25）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-09-24 完成 5 億美元 6.750% 2034 年到期優先票據私募，併同增貸用於支付 Epiq 收購價，並可能還循環信貸以支付 Swiss Technology Group AG 收購。
  - 來源：SEC EDGAR 8-K（2026-09-24，Item 1.01）（as_of 2026-09-24）｜affects：decision_inputs.bear、thesis.R
- `cyclical_supply_discipline_capacity#2`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：同業大幅擴產：勝宏科技 2026 Q1 資本支出約 RMB 36 億（去年同期 7.3 億）；中國逾 20 家 PCB 廠於 2026 上半年宣布積極擴產計畫。
  - 來源：TrendForce: China's PCB Makers Post Record-High Investment on AI Demand（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：臻鼎董事長稱 2026 年資本支出將超過 NT$800 億，13 座新廠興建中、16 座規劃中，產能 2026–2030 分階段開出；並主張高階產能需超前投資。
  - 來源：Technews: Zhen Ding invests 80 billion in major capacity expansion（as_of 2026-08-16）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：TTM 毛利率由 2008 年 20.2% 降至 2009 年 17.7%（庫存沖銷、固定成本吸收下降）
  - 來源：TTM Technologies Form 10-K FY2009（as_of 2010-03-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：TTM 2019 全年毛利率 14.9%，低於 2018 年 16.1%
  - 來源：TTM Technologies Form 10-K FY2019（as_of 2020-02-28）｜affects：decision_inputs.bear、thesis.R
- `ma_merger#1`（ma_merger｜方向 -｜狀態 ok）：Epiq 收購資金來自 5 億美元 6.750% 優先票據加 3 億 TLA、8 億 TLB 增貸。
  - 來源：SEC EDGAR 8-K（2026-09-24，Item 1.01）（as_of 2026-09-24）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":217.5,"bear_5y_price":50.0,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":67.1,"ev5y_pct":51.4,"irr_base_pct":10.8,"asym_ratio":2.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":4.96,"pe":16.15,"basis":"FY2026E 共識 non-GAAP EPS 4.96（與公司指引 4.97–5.03 一致），前瞻口徑；終端倍數乘 FY2031E non-GAAP EPS，同為前瞻口徑"},"eps":{"bull":[8.9,11.0,12.5,13.6,14.5],"base":[8.3,9.5,9.0,9.6,10.3],"bear":[7.2,5.6,4.2,4.6,5.0]},"pe":{"bull":15,"base":13,"bear":10},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":-0.6},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TTMI_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO Daniel Boehle｜guidance：Q3 2026 non-GAAP EPS 指引區間（營收 $1.10–1.14 billion）（原話："a range of $1.21 to $1.27 per diluted share"）
- 2026-08-05｜CFO Daniel Boehle｜guidance：全年 2026 營收指引上調至約 $4.4 billion（原話："full year 2026 sales of approximately $4.4 billion"）
- 2026-08-05｜CFO Daniel Boehle｜guidance：全年 2026 non-GAAP EPS 預期逼近 $5（原話："non-GAAP earnings to approach $5 per diluted share."）
- 2026-08-05｜CFO Daniel Boehle｜guidance：Q4 預期營收較 Q3 再往上（原話："net sales growth should continue with a sequential uptick"）
- 2026-08-05｜CFO Daniel Boehle｜guidance：財測口徑：指引不含待完成併購的貢獻或影響（原話："exclude any contribution or impact from pending"）
- 2026-08-05｜CFO Daniel Boehle｜guidance：Q3 SG&A 佔營收比重指引（原話："SG&A expense to be approximately 7% of net sales"）
- 2026-08-05｜CEO Edwin Roks｜guidance：Q3 資料中心與網通佔營收比重指引（原話："we expect this end market to represent 49% of net sales"）
- 2026-08-05｜CEO Edwin Roks｜guidance：全年資料中心與網通市場營收預期（原話："sales in this end market to more than double year-on-year"）
- 2026-08-05｜CEO Edwin Roks｜guidance：全年航太國防營收成長預期（原話："sales in this end market to grow in the low to mid-teens year-on-year."）
- 2026-08-05｜CEO Edwin Roks｜guidance：全年醫療／工業／儀器市場成長預期（原話："sales in this end market to grow 35% to 40% year-on-year"）
- 2026-08-05｜CEO Edwin Roks｜guidance：全年車用市場預期仍為中個位數衰退（原話："we continue to expect sales in this end market to decrease in"）
- 2026-08-05｜CEO Edwin Roks｜commitment：管理層重申 2027、2028 年有機營收成長目標（原話："achieve 15% to 20% organic revenue growth for 2027 and 2028"）
- 2026-08-05｜CEO Edwin Roks｜commitment：下一季將就遠期年度提供更新的長期計畫說明（原話："further clarity on these out years next quarter"）
- 2026-08-05｜CEO Edwin Roks｜commitment：明年也會繼續提供全年 EPS 指引（原話："We plan to do that next year as well."）
- 2026-08-05｜CEO Edwin Roks｜commitment：2026 營收預計明顯高於先前承諾的 $4 billion 門檻（原話："plan to achieve at least $4 billion in net sales in 2026"）
- 2026-08-05｜CEO Edwin Roks｜commitment：Syracuse 超高密度互連（Ultra-HDI）廠 Q3 起爬坡，2028 達滿產（原話："to reach full capacity run rate at 2028."）
- 2026-08-05｜CEO Edwin Roks｜commitment：Penang 預計接近損益兩平的時點（原話："breakeven number, which we hope to get, let's say, late Q3, Q4"）
- 2026-08-05｜CEO Edwin Roks｜product：N+M 不對稱互連板下半年約 $600 million 的出貨量（原話："$600 million of that technology, which is a really nice technology"）
- 2026-08-05｜CFO Daniel Boehle｜product：N+M 下半年 $600 million 在 Q3、Q4 的拆分（原話："About 1/3 of that's in Q3 and then 2/3 in Q4"）
- 2026-08-05｜CEO Edwin Roks｜product：N+M 良率比預期好（原話："Yields are much better than we thought"）
- 2026-08-05｜CEO Edwin Roks｜product：Penang 也在做 N+M，支援資料中心客戶（原話："doing N+M and indeed, supporting some of our data center and networking customers"）
- 2026-08-05｜CEO Edwin Roks｜product：Syracuse 廠 Ultra-HDI 產品 Q3 開始初期爬坡（原話："begin the initial stages of ramping up volume for Ultra-HDI"）
- 2026-08-05｜CFO Daniel Boehle｜margin：N+M 良率改善帶動 Q3、Q4 毛利率／EBITDA 利潤率改善，但不量化（原話："I won't quantify exactly what it will have."）
- 2026-08-05｜CFO Daniel Boehle｜margin：管理層稱 Q3、Q4 利潤率皆會改善（口徑為 adjusted EBITDA margin）（原話："it will improve the margins in both the third quarter and"）
- 2026-08-05｜CEO Edwin Roks｜margin：Adjusted EBITDA margin 16.6% 的年增／季增歸因於產品組合（原話："largely reflecting positive mix impacts"）
- 2026-08-05｜CFO Daniel Boehle｜margin：毛利率年增 100bp 的拆解：量與組合，點名資料中心與航太國防（原話："favorable product mix, particularly in the data center and networking"）
- 2026-08-05｜CFO Daniel Boehle｜margin：營業利益率改善歸因於毛利率與營運槓桿（原話："gross margin as well as operating leverage"）
- 2026-08-05｜CFO Daniel Boehle｜margin：Q2 自由現金流數字（原話："Free cash flow in the second quarter of 2026 was $46.0 million"）
- 2026-08-05｜CFO Daniel Boehle｜margin：GAAP 含 $14 million 非現金未實現匯率交換損失（因併購未完成無法適用避險會計）（原話："recognized a noncash pretax unrealized loss in the amount of $14 million"）
- 2026-08-05｜CEO Edwin Roks｜customer：資料中心與網通 Q2 年增 91%（原話："experienced 91% year-on-year growth in the second quarter"）
- 2026-08-05｜CEO Edwin Roks｜customer：商用端除既有 10% 客戶外，另有一家接近 10%（原話："it's getting a bit crowded, so there is another one"）
- 2026-08-05｜CEO Edwin Roks｜customer：前五大醫療客戶表現超出內部預期一倍以上（原話："top 5 medical customers' performance have more than doubled"）
- 2026-08-05｜CEO Edwin Roks｜customer：航太國防 Q2 book-to-bill 與在手訂單（原話："which led to a total program backlog of $1.7 billion"）
- 2026-08-05｜CEO Edwin Roks｜customer：航太國防合格潛在商機管道規模（原話："over $7 billion of potential business currently qualified"）
- 2026-08-05｜CEO Edwin Roks｜customer：90 天訂單積壓金額（可取消）（原話："backlog, which is subject to cancellations, was $901 million"）
- 2026-08-05｜CEO Edwin Roks｜competition：CEO 稱在美國航太國防部分有時是唯一供應商（原話："And it looks like sometimes we are the only"）
- 2026-08-05｜CEO Edwin Roks｜risk：車用業務因 CCL 供應商轉向高階材料而面臨材料供應壓力（原話："which reflects slight pressure in supply chain materials availability"）
- 2026-08-05｜CEO Edwin Roks｜risk：供應鏈問題僅出現在較低階業務，管理層稱高階不受影響（原話："if we are suffering a bit with our supply chain"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：STG 與 ILFA 併購預計貢獻低於 5% 增量營收（原話："expected to contribute less than 5% of incremental sales"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：管理層表示未來仍會機會性尋找歐洲併購標的（原話："to continue to be opportunistic in the future for businesses"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：董事會剛核准另一筆擴產資本投資（原話："we approved another capital investment"）
- 2026-08-05｜CFO Daniel Boehle｜capital_allocation：全年資本支出區間上下限各上調約 $45 million（原話："went up around $45 million at the top and bottom end"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：威斯康辛 Eau Claire 廠不急著投入，取得成本低於 $20 million（原話："We only paid less than $20 million for"）
- 2026-08-05｜CEO Edwin Roks｜capital_allocation：淨槓桿比率 0.9x（原話："net leverage ratio of 0.9x"）

### TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：CFO 說 2026 全年營收可達約 40 億美元（原話："revenue for 2026 could reach about $4 billion"）
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：CFO 說 Q1、Q2 約成長 30%，全年隱含 38% 成長（原話："we're growing at about 30%. So that implies 38%"）
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：CFO 說明全年成長偏下半年加速（原話："expectation of accelerated growth in the second half"）
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：2026 營業利益率指引由 11.7% 升到 13%–15%，並說比先前長期目標 11%–13% 高（原話："from 11.7% last year to a range of 13% to 15%"）
- 2026-05-27｜Daniel Boehle (CFO)｜guidance：2026 調整後 EBITDA 利益率指引 16%–18%（先前 15%–17%）（原話："adjusted EBITDA margin, 16% to 18%"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：管理層把 EBITDA 利益率只升 100bps（營業利益率升 200bps）的差距歸因於美元走弱的匯損，約 100bps（原話："driven this year by the weakening of the U.S. dollar"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：CFO 指 N+M 技術帶動較高 ASP，進而帶動較高毛利率（原話："that will result in higher gross margins for us"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：CFO 說 Penang 的毛利拖累全年少於 80bps（原話："That should be less than 80 bps for the year"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：回答分析師對增量利潤率的提問，CFO 說下半年良率仍待執行（原話："We do have yield expectations or yield performance we still"）
- 2026-05-27｜Daniel Boehle (CFO)｜margin：CFO 說利潤率區間的高低端取決於 N+M 良率，主要驅動為營收組合（原話："Revenue mix is what's going to drive the majority of it"）
- 2026-05-27｜Rob Farrell｜margin：Rob Farrell 說新一代程式的 ASP 是前代的 2–3 倍（原話："replacements are 2 or 3x what they were in past generations"）
- 2026-05-27｜Catherine Gridley｜margin：Gridley 說 A&D 2025 EBITDA 利益率 17.2%，年增 120bps（原話："17.2% EBITDA margin, which was 120 basis points growth"）
- 2026-05-27｜Catherine Gridley｜margin：Gridley 說多數合約以固定價格投標（原話："largely bid in a firm fixed"）
- 2026-05-27｜Gregory Fortier｜margin：Fortier 說新採購方式（市集式）利潤較好，但部分專案仍受認證成本與定價規範（原話："subject to certified cost and pricing"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 重申未來三年營收年複合成長 15%–20%（原話："The 15% to 20% is still pretty accurate."）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 重申 2025 到 2027 年獲利翻倍的目標仍然適用（原話："doubling the earnings from 25 to 27"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說公司近幾個月才改為提供全年指引，過去只給下一季（原話："we decided now to give full guidance for the year"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說 A&D 成長預期為高個位數（原話："in the foreseeable future, high single digit"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說資料中心與網路業務今年可能翻倍（原話："to double that business."）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說醫療、工業、儀器業務預期成長約 25%–30%（原話："we expect to grow about 25% to 30% going"）
- 2026-05-27｜Edwin Roks (CEO)｜guidance：Roks 說車用預期年減約 10%（Q1 僅減 2%）（原話："we expect a decline of, let's say, 10% year-over-year"）
- 2026-05-27｜Catherine Gridley｜guidance：Gridley 說四座北美廠擴產讓 2028 年前可增加約 5 億美元營收的產能（原話："for $500 million in additional revenue growth"）
- 2026-05-27｜Douglas Soder｜guidance：Doug Soder 估計 N+M 長期營收機會為 45 億美元（原話："revenue opportunity over the future for N+M at $4.5 billion"）
- 2026-05-27｜Rob Farrell｜guidance：Farrell 說 N+M 量產爬坡在今年夏天與下半年（原話："place this summer and into the second half of the year"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說 2026 資本支出 3 億至 3.2 億美元，並預期現金流略為正（原話："increased the capital expenditures for the current year"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 預期今年自由現金流為小幅正值（原話："continue to get slightly positive in the current year"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說 2027、2028 資本支出占營收約 6%–7%（原話："between 6% and 7% of revenue, with growing revenue"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 與歷史資本支出占比（約 4%–5%）相比較高（原話："higher than our historical, which is about 4% to 5%"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說正在擴大並重新定價 Term Loan B，約 3.4 億增至 4 億美元（原話："$340 million to $400 million on upsize"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說以多幣別循環信貸取代現有 ABL，額度最高 10 億美元（原話："commitments on that up to $1 billion"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說擴大的借款額度預期主要用在併購（原話："is most likely going to be used for M&A"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 提到地理擴張與小型策略併購機會，並說 CEO 想去歐洲（原話："my boss seems to want to be there"）
- 2026-05-27｜Edwin Roks (CEO)｜capital_allocation：Roks 說歐洲 A&D 要求至少 60% 歐洲在地含量，是併購切入角度（原話："there needs to be 60-plus percent European content"）
- 2026-05-27｜Douglas Soder｜capital_allocation：Soder 說近年已在商用部門投入 10 億美元擴廠（原話："invested $1 billion in this commercial sector footprint"）
- 2026-05-27｜Douglas Soder｜capital_allocation：Soder 說 N+M 在 2025–2027 預計投入 4.5 億美元資本支出（原話："anticipating $450 million of capital investments in N+M"）
- 2026-05-27｜Douglas Soder｜capital_allocation：Soder 說在既有廠區旁擴產（棕地）比新建（綠地）快一倍以上（原話："to market for our customers in half the time or less"）
- 2026-05-27｜Douglas Soder｜capital_allocation：Soder 說已在檳城附近取得土地，適當時可建第二座廠（原話："land nearby so that we have the opportunity"）
- 2026-05-27｜Daniel Boehle (CFO)｜capital_allocation：CFO 說 N+M 這 4.5 億美元約換來 45 億營收（10 倍），並稱不是所有資本支出的基準（原話："gave basically a 10x on that $450 million"）
- 2026-05-27｜Rob Farrell｜commitment：Farrell 說已承諾專案到明年中約有近 100% 產能覆蓋（原話："almost 100% coverage by probably the middle of next year"）
- 2026-05-27｜Rob Farrell｜commitment：Farrell 說保留部分產能給非策略夥伴的新客戶（原話："I would say we are holding some capacity"）
- 2026-05-27｜Douglas Soder｜commitment：Soder 說正與大客戶討論長約，內容含產能保證與工程合作（原話："agreements for capacity guarantees, engineering engagement"）
- 2026-05-27｜Edwin Roks (CEO)｜commitment：Roks 說歐洲擴張在規劃管線中（原話："So that's in the pipeline."）
- 2026-05-27｜Catherine Gridley｜competition：Gridley 說 A&D 最大的競爭來自主承包商自行內製（原話："our biggest competition really is the primes"）
- 2026-05-27｜Rob Farrell｜competition：Farrell 說 N+M 的競爭格局受限，僅少數業者（原話："the competition landscape is it's restricted"）
- 2026-05-27｜Rob Farrell｜competition：Farrell 說目前 N+M 受到一定程度的保護（原話："we're somewhat protected at this point"）
- 2026-05-27｜Douglas Soder｜competition：Soder 說資料中心 SAM 中有大量商品化業務，公司不想做，所以市占只有 9%（原話："There's a lot of commodity business in that number"）
- 2026-05-27｜Douglas Soder｜competition：Soder 說資料中心網路可服務市場約 100 億美元，公司市占約 9%（原話："about $10 billion, and we're at about 9% market"）
- 2026-05-27｜Daniel Boehle (CFO)｜competition：CFO 說 9% 是回頭看的數字，未來視所選技術可能上升或下降（原話："looking at the 9%, you're looking in the rear"）
- 2026-05-27｜Douglas Soder｜customer：Doug Soder 說資料中心與網路 2025 年約 9 億美元，年增 40%（原話："up 40% year-on-year"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說 A&D 在手訂單 16 億美元，管線 72 億美元（原話："the $7.2 billion pipeline, and that pipeline is growing"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說 72 億美元管線到 5 月已顯著成長（原話："has already significantly grown just up through May"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說已接到再製造回流（onshoring）訂單（原話："we are already fielding orders for onshoring and reshoring"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說新創主承包商（neo primes）興趣顯著加速（原話："we're now seeing a significant acceleration in that interest"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說商用太空快速加速（原話："We are seeing a rapid acceleration in commercial space"）
- 2026-05-27｜Gregory Fortier｜customer：Fortier 說已收到 Golden Dome 的首張訂單（原話："received our first order very, very quickly"）
- 2026-05-27｜Gregory Fortier｜customer：Fortier 說已收到感知與迴避雷達（先進空中運輸）的首張訂單（原話："we've received the first order here in this market as well"）
- 2026-05-27｜Gregory Fortier｜customer：Fortier 引述總統 2027 預算七條預算線共 2350 億美元（原話："$235 billion dedicated to just 7 budget lines"）
- 2026-05-27｜Gregory Fortier｜customer：Fortier 說國防合約授標由 600 天縮到 30–45 天（原話："a 600-day process to award a contract"）
- 2026-05-27｜Rob Farrell｜customer：Farrell 說愈來愈多客戶要求中國以外的方案（原話："more and more of them want solutions outside of China"）
- 2026-05-27｜Catherine Gridley｜customer：Gridley 說商業太空客戶的採購決策尚待定，直接影響 ramp 時程（原話："that will directly impact what our ramp-up"）
- 2026-05-27｜Douglas Soder｜product：Soder 說公司的板子與晶片種類無關（晶片中立）（原話："processing unit agnostic or chip agnostic"）
- 2026-05-27｜Douglas Soder｜product：Soder 說 N+M 正進入量產（原話："now entering into mass production with N+M technology"）
- 2026-05-27｜Rob Farrell｜product：Farrell 說早期 3.2T 設計尚未納入光學（原話："the early 3.2 designs we have do not include optics yet"）
- 2026-05-27｜Edwin Roks (CEO)｜product：Roks 說銅不會很快消失，光學是補充（原話："copper is not going away, okay? It's not going away soon."）
- 2026-05-27｜Edwin Roks (CEO)｜product：Roks 被問光學方向時承認目前沒有太多資訊（原話："Do we have a lot of color right now"）
- 2026-05-27｜Edwin Roks (CEO)｜risk：Roks 承認 AI 浪潮終將下滑，時點不知（原話："When it will come down, we don't know."）
- 2026-05-27｜Edwin Roks (CEO)｜risk：Roks 說波浪會下來，要做好準備（原話："we better be prepared for that"）
- 2026-05-27｜Catherine Gridley｜risk：Gridley 說國防端成長時程取決於採購核准時程（原話："it takes time to qualify these products"）
- 2026-05-27｜Edwin Roks (CEO)｜risk：Roks 說 80% 的業務由 AI 與國防兩大趨勢驅動（原話："80% of our business is basically driven by these megatrends"）

### 問答異常語氣（迴避／改口／保留）
- TTMI_Q2_2026_Earnings_Call_20260805.md｜問：Truist 的 William Stein 問明年 N+M 增量營收是否約 $1 billion、利潤率影響為何｜答法：未確認數字，稱明年規模仍為規劃中（'a work in progress'），僅說 'it could be in the ballpark you mentioned'，利潤率影響未正面回答
- TTMI_Q2_2026_Earnings_Call_20260805.md｜問：B. Riley 的 Mike Crawford 問 STG／ILFA 收購價格、年化營收貢獻與擴充空間｜答法：CEO 明說無法談營收與價格（'I cannot do that'），僅重述低於 5%，CFO 表示 '交割時再提供'，改談興奮與監管流程
- TTMI_Q2_2026_Earnings_Call_20260805.md｜問：Needham 的 Jim Ricchiuti 問 N+M 爬坡對 Q3 營收與利潤率的影響｜答法：給了下半年 $600 million 與 1/3、2/3 拆分，但利潤率影響明說不量化（'I won't quantify'），僅稱 Q3、Q4 都會改善
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：Steven Fox 問為何指引隱含的增量利潤率只有約 20%，是否過於保守｜答法：CFO 未給出增量利潤率數字，改談匯率逆風與下半年良率仍待執行，再補充營收組合與 N+M 良率
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：Steven Fox 問 A&D 為何只講高個位數成長，哪裡有雙位數上行空間｜答法：Gridley 沒給成長數字，改談資格認證時間、國防部採購時程與商用太空客戶採購決策尚待定
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：William Stein 問 2027、2028 年營收成長與利潤率擴張的方向｜答法：Roks 只重申 15%–20% 與 EPS 翻倍，未給新數字，並說 'So we'll see. We'll see.' 以及有變化會通知分析師
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：James Ricchiuti 問 72 億美元管線一年前的規模與主要組成｜答法：Gridley 說無法提供對比，也不談管線細項，只說已顯著成長且偏向國防
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：Remington Johnson 問 5 億美元增量營收潛力在四座廠間如何分配｜答法：Gridley 拒絕按廠拆分，只說 Syracuse 最大
- TTMI_Analyst_Investor_Day_TTM_Technologies_Inc_20260527.md｜問：James Ricchiuti 問 Eau Claire 何時裝機、如何放量｜答法：管理層回說沒有明確時程，只談客戶區域分散與中國加一等需求驅動

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 4 | 1 |
| supply_demand_durability | found | 7 | 3 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 2 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | none | 0 | 3 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 3 | 5 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 1 | 3 |
| cyclical_prior_downcycle_behavior | found | 2 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **channel_business_model_shift**（none）：TTM Technologies distribution channel shift business model 2026；TTM Technologies 10-K distributors direct sales customer mix aerospace defense data center 2026；TTM Technologies 業務模式 通路 轉型 2026 PCB 美國 國防 資料中心

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"觀望偏進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Penang + Syracuse ramp 順利 → 公司 Gross Margin 從 21.4% 擴至 26%+，OI Margin 從 12.8% 擴至 16%+","columns":{"2Y 驗證（28 年內）":"Penang 達 OCF breakeven (Q3 26)；Syracuse 啟動量產 (late 26)；FY26 全年 GM 22%+","5Y 驗證（28-30 年）":"FY29 全年 GM 26%+；OI Margin 16-18%；TTMI 整體 OCF $700M+","10Y 驗證（30-35 年）":"FY32 維持 GM 26%+ 並繼續往 28% 邁進；單站 ROIC > 15%","驗證指標":"Quarterly GM / OI Margin、Penang quarterly revenue (target $30-35M Q3, $80M Q4)","來源":"§8.A Runway, §6 quarterly"}},{"id":"H2","text":"A&amp;D 段持續 +12-15% YoY 至 2028，backlog 維持 1.4-1.6x book-to-bill","columns":{"2Y 驗證（28 年內）":"2026 A&amp;D 段 +11-13%（Q1 已驗證 +11%）；backlog $1.6B → $1.9B","5Y 驗證（28-30 年）":"FY29 A&amp;D revenue $1.6B+（vs 2025 ~$1B）；占比維持 38-42%","10Y 驗證（30-35 年）":"FY32 A&amp;D $2.5B；Syracuse + Telephonics + 既有產線 三引擎","驗證指標":"季度 A&amp;D revenue、book-to-bill、backlog 絕對額","來源":"§11 議價權, §8 路線圖"}},{"id":"H3","text":"市場給予 forward PE 25-30x（vs 商用 EMS 同業 18-22x）的 premium，反映 A&amp;D moat + AI 結構性成長","columns":{"2Y 驗證（28 年內）":"FY26 Fwd PE 維持 25-30x（不破 20x），股價區間 $90-180","5Y 驗證（28-30 年）":"FY29 PE 25x，EPS $7.5+，股價 $185+","10Y 驗證（30-35 年）":"FY32 進入成熟期 PE 20x，EPS $10+，股價 $200+","驗證指標":"Fwd PE 5Y rolling、PEG、vs Sanmina/Jabil 同業溢價幅度","來源":"§13.1/§13.4"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"🔥 Penang ramp 延後 + Capex 失控：若 Q4 26 Penang 仍未達 OCF breakeven、且 FY27 Capex 拉到 $350M+，FCF 連續 3 年負，市場開始質疑 capital allocation","columns":{"對應假設":"H1","時間尺度":"🔥 中期（2-3 年）","監測指標":"Penang quarterly revenue + OCF；FY27 Capex guidance","警戒閾值":"Q3 26 Penang revenue FY27 Capex guidance > $350M（連續第三年增加）"}},{"id":"R2","text":"⚡ A&amp;D backlog 萎縮 + 國防預算延後：美國 CR (continuing resolution) 延長 / 債限政治 → DoD 凍結 program timing；backlog QoQ 連續兩季下滑","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（12 月內）","監測指標":"季度 A&amp;D revenue、backlog、book-to-bill；DoD FY27/28 budget 進度","警戒閾值":"book-to-bill A&amp;D backlog QoQ"}},{"id":"R3","text":"⚡ 估值倍數壓縮 + 內部人賣壓擴大：FPE 從 33x 修正至 25x（即使 EPS 未變，股價 −24%）；Tom Edman 從 10b5-1 schedule 切換至「機會式賣股」or 新 CEO 加入賣方","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（12 月內）","監測指標":"Fwd PE 5Y 分位（baseline 92%）、SPX 整體 P/E 收斂、Form 4 揭露","警戒閾值":"Fwd PE > 40x（超越 5Y 高）OR Fwd PE OR 6 個月內部人賣股 > $20M"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":167.35,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TTMI","date":"2026-10-25","schema":"v15.0","contract":"v19","company_name":"TTM Technologies, Inc."},"oneliner":"AI 資料中心 N+M 板與國防訂單把 TTM 推上紀錄獲利，股價卻半年腰斬；2027 年有訂單與指引撐腰，2028 年中國新產能開出與舉債併購是還沒解的兩個問題。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/scenario.json","answers":{"q1_business":{"verdict":"TTM 賺的是 AI 資料中心客戶與美國國防主承包商的高層數印刷電路板與射頻次系統的錢。錢卡在高階產能與 N+M 良率這一節點；上游材料漲價、下游客戶集中，議價空間兩頭受擠。","reasoning":"Q3 FY2026 營收 12.04 億美元，年增 60%，高於公司指引上緣 11.4 億。GAAP 營益率 13.5%，non-GAAP 17.4%。終端市場結構：資料中心與網通占 41%（年增 115%）、航太國防 34%（年增 21%）、醫療工業儀器 18%（年增 97%）、車用 7%。管理層預估 Q4 資料中心占比升到約 49%。訂單出貨比 2.13，A&D 專案 backlog 20 億美元創新高。Q4 指引營收 14.2–14.4 億美元；2027 年初步指引營收 65–67.5 億美元、non-GAAP EPS 8.10–8.90，其中約 5 億美元營收來自收購。產業時鐘判為擴張期：訂單仍在加速，新增供給多在 2027–2029 年才開出。供需持久性判為週期性將反轉，因為多方來源都指出吃緊只延續到 2027–2028 年，供給可逆性高。單點依賴有兩處：一是客戶集中，FY25 前十大客戶占 55%、兩家合計 23%，一家客戶占應收 14%；二是 N+M 有三個大型專案，其中一個已延後。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_q4_2026","f_kpi7_fy2027","f_kpi8_book_to_bill","f_kpi9_a_d_backlog","f_kpi10"],"verdict_values":{"revenue_quality":"Q3 營收年增 60%，四個終端市場全部成長。90 天 backlog 13 億美元（年增 111%）與 A&D 2027 年約 65% 營收能見度撐住 2–3 季，但 90 天 backlog 可以取消，資料中心營收受客戶專案時程左右（Q3 比前季給的占比指引低約 10%）。","unit_econ_note":"CEO 稱 N+M 板 ASP 約為傳統架構的 4 倍，CFO 稱其毛利率顯著高於公司平均；Q3 non-GAAP 毛利率 24.8%，年增 330bp。材料成本上升目前由客戶吸收。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"需求量循環：AI 資料中心建置帶動高層數板量價齊升，國防長約與向上整合（射頻、光學次系統）部分抵銷週期"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉。依據：多方產業來源指 AI 用 PCB 與上游玻纖布、覆銅板吃緊延續到 2027–2028 年，中國綠地建廠 13–15 個月，新產能 2027 年底至 2029 年分批開出；中國逾 20 家同業 2026 上半年宣布擴產。","bargaining":{"up":"上游覆銅板與玻纖布吃緊，Kingboard 2026 年已漲價八次，部分元件為有限或單一來源；公司稱交期 12–24 週，目前漲價由客戶吸收。","down":"FY25 前五大 OEM 客戶占 44%、前十大占 55%、兩家合計 23%，一家占應收 14% 且不要求擔保；資料中心客戶每個專案都有多家供應商。","geo":"約一半淨銷售來自美國以外的營運，中國廠是 N+M 主要產能；美中兩國都把 PCB 列入進口關稅；歐洲與以色列、羅馬尼亞透過併購擴點。"},"profit_pool_dir":"利潤池往高層數 AI 板與上游材料端移動（材料商連續漲價）；營業利益池五年變化事實表未涵蓋。","tam_table":[{"item":"資料中心與網通可服務市場","value":"約 100 億美元，TTM 市占約 9%（2026-05-27 投資人日 Soder；CFO 稱此為回頭看的數字）"},{"item":"N+M 長期營收機會","value":"約 45 億美元（投資人日 Soder）；2027 年 N+M 預計占資料中心營收約 50%（Q3 法說 CEO）"},{"item":"超大型雲端業者 PCB 供應份額","value":"2025 年 10–15%，2026 年預期超過 15%（第三方 Substack 估計，非公司揭露）"},{"item":"A&D 合格潛在商機","value":"逾 70 億美元（2026-08-05 Q2 法說 CEO）；專案 backlog 20 億美元"},{"item":"利潤池五年流向","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"→","reasoning":"機制：美國本土高階產能、國防受限專案資格與 N+M 製程良率三者疊加。商用段靠的是先行者優勢，不是專利，10-K 自承製程技術通常不受重大專利保護。執行面在擴大：N+M 良率比預期好（Q2 法說），Q3 調整後 EBITDA 利益率 20.1% 創紀錄，國防受限專案難以被替換，第三方分析也稱 TTM 是美國唯一在 ASIC 領域具相當產能的 PCB 廠。定價面持穩：材料漲價能轉嫁，醫療工業儀器段有調價，但客戶集中限制議價。同業對照方面，台灣高階同業的營業利益率遠高於 TTM，TTM 對最強同業的報酬差為負，所以合併分不到 8。兩面相抵，趨勢判為持穩。最大威脅是中國同業 2026–2030 年的擴產潮。投入資本事實表未涵蓋，當期 ROIC 無法計算。","fact_refs":["f_peer_ttmi_gross_margin_pct","f_peer_ttmi_operating_margin_pct","f_peer_ttmi_fcf_margin_pct","f_peer_2368_tw_operating_margin_pct","f_peer_3037_tw_operating_margin_pct","f_peer_sanm_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"美國本土高階 PCB 產能，加上國防受限專案資格（認證、安全許可、重新認證週期長）與 N+M 不對稱板的製程良率領先；商用段屬先行者優勢，無專利保護","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：N+M 良率優於預期，Q3 調整後 EBITDA 利益率 20.1% 年增 400bp，A&D 訂單出貨比約 1.6，backlog 20 億美元創新高，受限專案黏著度高。定價面持穩：Kingboard 年內八次漲價由客戶吸收，但第三方指客戶集中使定價權有限；TTM 營業利益率約 9.9%（近四季），遠低於台灣高階同業約 26%。中國同業 2027 年起的新產能可能削弱商用段。","competitor_notes":[{"name":"SANM","strategy_note":"EMS 為主、利潤率比 TTM 低一截，但正在擴充 AI 與國防用高階 PCB 產能，並以北美、歐洲、亞洲製造足跡直接挑戰 TTM 的歐洲擴張"},{"name":"2368.TW","strategy_note":"台灣高階板同業，毛利率與營業利益率都明顯高於 TTM，是 AI 伺服器板最強的報酬標竿；TTM 對它的報酬差為負"},{"name":"3037.TW","strategy_note":"台灣載板與 PCB 大廠，利潤率與 TTM 相近、近四季自由現金流同樣為負，反映整個產業都處在擴產吃現金的階段"}],"threats":[{"level":"🔴","text":"中國與台灣同業 2026–2030 年大舉擴產：勝宏 2026 Q1 資本支出約 36 億人民幣（去年同期 7.3 億），臻鼎 2026 年資本支出逾新台幣 800 億、13 座新廠興建中。2027–2029 年產能開出後，高階板價格與稼動率可能回落","p":"35%","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#1"]},{"level":"🟡","text":"Sanmina 擴充高階 PCB 產能（AI、航太國防），以三大洲製造足跡挑戰 TTM 歐洲擴張；Amphenol 透過併購強化高速電子","p":"30%","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#4"]},{"level":"🟡","text":"PCB 產業高度分散且變化快，製程技術多無重大專利保護；玻璃基板與共封裝光學可能帶來新進入者，但目前尚無量產時程","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×周轉率未知（近四季營業利益率約 9.9%，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是超大型雲端業者與國防主承包商，三角色都成立。AI 加速器要更高層數與 N+M 板，屬「需要」；但需求屬建置期，CEO 在投資人日自承 AI 浪潮終將下滑、時點不知。急迫性高，持久性未證。國防端有預算順風且 2027 年約 65% 營收已有能見度。"},{"item":"決策層級","level":"🟡","text":"決策單位是單一專案、單一世代。國防受限專案的重新認證週期長、難替換，CEO 稱美國部分國防產品有時是唯一供應商。資料中心客戶每個專案都有多家供應商，Q3 法說 CEO 也說每家都得在同一技術窗口，換代時份額會重新分配。"},{"item":"價值鏈分配","level":"🟡","text":"上游覆銅板與玻纖布吃緊、連續漲價，目前能轉嫁；下游客戶高度集中。台灣高階同業的利益率遠高於 TTM，表示這條價值鏈裡 TTM 不是拿得最多的環節。一旦 2027 年後供給放鬆，價值可能回流給客戶。"},{"item":"社會容忍度","level":"🟢","text":"產品是企業與政府採購的中間財，沒有消費者端的漲價政治壓力。國防部分合約受認證成本與定價規範、多以固定價格投標（投資人日 Gridley、Fortier），這限制的是利潤上限，不構成政策風險。"}],"roiic":"事實表未涵蓋投入資本與增量投入資本，無法計算已實現增量 ROIC。投資人日 CFO 稱 N+M 4.5 億美元資本支出對應約 45 億美元營收機會（約 10 倍），並說明這不是全部資本支出的基準；這是管理層預期，不是已實現數字","reinvest_rate":"高於 100% 的稅後營業利益：近四季自由現金流利潤率約 −0.45%（資本支出大於營業現金流）。2026 年資本支出約 3–3.2 億美元（投資人日），Q2 再上調約 4,500 萬；2025–2029 年承諾逾 13 億，另加 4 億 N+M 擴產；同期以 11 億現金收購 Epiq、6.5 億收購 Ophir（待交割）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。再投資率輸入（資本支出、折舊、營運資金變動、收購淨額）只有部分在逐字稿，增量投入資本不在事實表，因此天花板留空，不以推估補數字"}}}},"q3_growth":{"verdict":"🟡","reasoning":"成長由三部分組成：量（N+M 與高層數板出貨、A&D 訂單）、價（N+M ASP 較高、材料漲價轉嫁）、併購（2027 年約 5 億美元營收來自收購）；沒有回購。共識 EPS FY26 4.96、FY27 8.34、FY28 10.06，兩年年化約 42%。FY25 non-GAAP 基期事實表未涵蓋，GAAP 稀釋 EPS 為 1.68，口徑不同不直接算三年 CAGR。共識營收 FY26 44.7 億、FY27 65.9 億，增約 47%，同期 EPS 增約 68%，差距來自 N+M 組合推高利益率。內生天花板因投入資本未涵蓋而無法計算。缺口歸因：毛利結構改善與收購可以說清楚一部分，剩下的無法歸因，長期信心上限為中。跑道方面，資料中心可服務市場約 100 億、市占約 9%，N+M 長期機會約 45 億；2027 年 N+M 約占資料中心一半，按此推估約 3–5 年會吃到大半機會。國防向上整合（Epiq、Ophir）是靠收購補的第二條腿，不是自己長出的下一條 S 曲線，所以五年後跑道判為中。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_fy2027","f_kpi10"],"verdict_values":{"growth":{"driver_mix":"量（N+M 與高層數板、A&D 訂單）＋價（N+M 單價約傳統板 4 倍、材料漲價轉嫁）＋併購（2027 年約 5 億美元營收）；無回購","runway_years":"約 3–5 年","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋投入資本與增量投入資本，內生天花板無法計算。共識 FY26→FY28 EPS 年化約 42%，缺口部分歸因於 N+M 組合帶來的利益率擴張與收購，其餘無法歸因、依賴重新評價，長期信心上限為中","segments":[{"item":"資料中心與網通","value":"Q3 占 41%、年增 115%；Q4 預估占約 49%（約 6.7–7 億美元），N+M 約占三成，2027 年升到約五成"},{"item":"航太國防","value":"Q3 占 34%、年增 21%；backlog 20 億美元、訂單出貨比約 1.6；Q4 預估占約 31%"},{"item":"醫療工業儀器","value":"Q3 占 18%、年增 97%（含調價與 AI 車用測試設備需求）；Q4 預估占約 14%"},{"item":"車用","value":"Q3 占 7%、年增 11%；全年由原估中個位數衰退改為中個位數成長"}],"decay_signals":["EPS 成長顯著高於營收成長：共識 FY26→FY27 EPS 約 +68%，營收約 +47%，差距超過 5pp，亮","FCF 對淨利低於 0.75：FY25 自由現金流約為零、淨利 1.77 億；FY24 約 0.91，只有一年未達、未連兩年，暫不亮，列監測","毛利率連兩季年減：未亮（Q3 non-GAAP 毛利率年增 330bp）","核心市占縮減：未亮（第三方估超大型雲端業者份額上升）","SBC 占營收逾 5%：未亮（Q3 約 2.0%）","維護性資本支出占 FCF 逾 60%：事實表未涵蓋"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏激進：在獲利高峰期舉債做大型併購，同時承諾 16 億美元以上擴產，自由現金流還很薄。","reasoning":"現金轉換弱：FY25 自由現金流約為零（淨利 1.77 億），近四季自由現金流利潤率約 −0.45%；Q3 單季回到 7,480 萬。SBC 2,410 萬，占營收 2.0%。稀釋股數 FY26 約 1.075 億、FY27 約 1.081 億，年稀釋約 0.6%。現金去向：一是資本支出（2025–2029 年承諾逾 13 億，另加 4 億）；二是併購（Epiq 11 億現金於 9/30 完成、Ophir 6.5 億待 2027Q2、STG 已完成、ILFA 將完成、英國兩家小廠）；三是無股息、無回購的證據。資金來源是 5 億美元 6.75% 2034 年到期票據，加 3 億 TLA、8 億 TLB 增貸，Q4 利息支出指引 3,390 萬美元，Q3 為 1,210 萬。淨槓桿由 Q2 的 0.9 倍升到 Ophir 交割時的「低於 2 倍」。事實表的淨負債 7.68 億是最新一季數字，可能未含 9/30 增貸與待交割的 Ophir。併購已實現的增量報酬目前沒有數據；Ophir 約 10 倍 2027 年 EBITDA 的價格，管理層自稱保守。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_peer_ttmi_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Epiq 9/30 才完成、Ophir 待交割，已實現增量報酬無數據；過往併購報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"證據包未見回購；稀釋股數逐年上升"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數 FY26 約 1.075 億、FY27 約 1.081 億，年稀釋約 0.6%，低於 1.5%；Q3 SBC 占營收 2.0%"}]},"governance":{"capital_returns":[{"item":"股息","value":"事實表未涵蓋；法說會未提股息政策"},{"item":"回購","value":"證據包未見；CFO 說明 2027 年現金優先用於資本支出與還債"},{"item":"併購支出","value":"Epiq 11 億美元現金（2026-09-30 完成）、Ophir 6.5 億美元（預計 2027Q2）、STG 已完成、ILFA 接近完成、英國 Merlin 旗下兩家小廠"},{"item":"資本支出承諾","value":"2025–2029 年逾 13 億美元，另加 4 億 N+M 擴產（2026Q4 至 2028 初）"},{"item":"融資","value":"5 億美元 6.75% 2034 年票據＋3 億 TLA＋8 億 TLB；Q4 利息支出指引約 3,390 萬美元"}]}}},"q5_valuation":{"verdict":"現價 80.11 美元，約為 FY26 共識 16.2 倍、FY27 約 9.6 倍。要划算，只需 2027 年獲利大致兌現，且 2028 年不腰斬。我信前一半：2027 年有訂單與指引撐。後一半要看中國新產能開出後的價格，現在無從驗證。","reasoning":"前瞻本益比 16.15 倍（分母 FY1 4.96），trailing 本益比 32.0 倍，落在自身 3 個年度端點的約五成分位。trailing P/S 2.2 倍、EV/S 2.41 倍，在自身 4 個年度端點的八成以上分位。年度端點太少，不是五年分位，五年分位留空。PEG：FY26→FY28 共識 EPS 年化約 42%，16.15÷42≈0.38；但週期股在高峰期 PEG 失真，不作便宜依據。分母本身就是爭點：FY27 8.34 是 AI 建置高峰的獲利，而且淨負債可能未含 9/30 增貸 11 億與待交割 Ophir 6.5 億，EV 偏低。所以便宜論證打折，估值結論給黃。短期上行：2027 年 EPS 8.3×12 倍約 100 美元，約 +24%。中期上行用 Base 五年終點約 134 美元，約 +67%。同業前瞻本益比事實表未涵蓋，無法做倍數對照。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct","f_net_debt_m","f_ev_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY26／FY27 共識 non-GAAP EPS）","tier":"美國高階 PCB 與國防電子","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業前瞻本益比，無法做倍數對照；終端倍數改以自身前瞻與 trailing 倍數為錨"},"fwd_pe":16.15,"peg":0.38,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"數字上便宜（FY26 16.2 倍、FY27 約 9.6 倍）；但 trailing P/S 與 EV/S 落在自身年度端點八成以上分位，分母是 AI 建置高峰獲利，淨負債可能低估約 17.5 億美元的新增債務與待付併購款，所以結論給黃，不給綠","upside_short_pct":24,"upside_mid_pct":67,"denominator_disputed":true,"denominator_note":"便宜論證靠 FY27 共識 EPS 8.34，這是 AI 建置與材料吃緊高峰的獲利，2028 年中國新產能開出後能否守住正是爭點；另外最新一季淨負債可能未含 9/30 Epiq 交割時的 11 億定期貸款與待交割 Ophir 6.5 億"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把高峰獲利當常態：2028 年中國新產能開出、AI 建置放緩時，資料中心板價格與稼動率一起回落，加上舉債併購放大損益波動。","reasoning":"股價 26 週跌 46%、RSI 33，可是同期 FY1 共識三個月上修約 23%。市場在折價的是 2028 年以後，不是 2027 年。過去下行期 TTM 毛利率 2009 年降 2.5pp、2019 年降 1.2pp，跌幅不大；但這次資料中心占營收近半、N+M 毛利遠高於平均，營運槓桿大很多。Q4 N+M 規模約只有前季說法的一半，管理層歸因客戶時程延後，未證。三視角的反證與裁定見反證紀錄。","fact_refs":["f_week26_return_pct","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰獲利期的低本益比可能是陷阱；FCF 薄、舉債併購"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":4.96,"pe":16.15,"basis":"FY2026E 共識 non-GAAP EPS 4.96（與公司指引 4.97–5.03 一致），前瞻口徑；終端倍數乘 FY2031E non-GAAP EPS，同為前瞻口徑"},"eps":{"bull":[8.9,11.0,12.5,13.6,14.5],"base":[8.3,9.5,9.0,9.6,10.3],"bear":[7.2,5.6,4.2,4.6,5.0]},"pe":{"bull":15,"base":13,"bear":10},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":-0.6},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":5},"max_dd":{"lo":-58,"hi":-38,"basis":"近 26 週已實際下跌 46%（股價 80.11，52 週均線 116.38），證明這檔半年內就能跌掉四成以上。Bear 路徑 EPS 由 2027 年約 7.2 美元落到 2029 年約 4.2 美元，本益比壓到 10 倍，終點約 −38%；週期底部通常再超跌 15–20pp，得出 −38% 到 −58%","trigger_time":null},"basis":{"bull":"N+M 五到十個專案全數放量，2027 年達指引上緣；材料與產能吃緊延續到 2028 年，國防向上整合推高利益率，Ophir、Epiq 綜效兌現","base":"2027 年約達共識；2028 年中國新產能開出、AI 建置放緩，2029 年 EPS 小幅回落後由國防與醫療工業段撐住，終端 13 倍低於現行 FY26 前瞻 16 倍","bear":"第三個 N+M 專案與主要客戶持續延後，2027 年低於指引下緣；2028–2029 年中國產能洪水使高階板價格與稼動率雙降，毛利率回到 2019 年水準附近，利息負擔放大跌幅；供給吃緊雖有來源支持，但只到 2027–2028 年，所以不壓低 Bear 機率"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"中國逾 20 家 PCB 廠 2026 上半年宣布擴產，勝宏 Q1 資本支出約 36 億人民幣，臻鼎 13 座新廠興建中、產能 2026–2030 年分批開出；第三方整理指資料中心建置若放緩，Penang 與 Syracuse 擴產的稼動率與毛利有風險；過去下行期毛利率 2009 年由 20.2% 降到 17.7%，2019 年由 16.1% 降到 14.9%","assumption":"Base 假設 2029 年 EPS 只小幅回落、毛利結構大致守住","consequence":"若 N+M 在 2028 年被中國產能削價，資料中心利益率退回傳統板水準，EPS 可能回到 4–5 美元，股價約 50 美元，五年虧約四成","ruling":"採納：Bear 機率給 35%，高於一般的 25–30%；同時列入毛利率年減的減碼門檻","watch":"non-GAAP 毛利率年增減、中國同業高階板報價、超大型雲端業者資本支出指引","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","supply_demand_durability#5"],"fact_refs":["f_kpi1_non_gaap"]},{"view":"論點失敗","evidence":"FY25 前十大客戶占 55%（2024 年 42%），兩家合計 23%，一家占應收 14% 且不要求擔保；Q3 資料中心比前季占比指引低約 10%，Q4 N+M 約為前季說法的一半，管理層歸因一家客戶專案延後","assumption":"三個 N+M 大專案在 2027 年都正常放量","consequence":"一家主要 AI 客戶削減或轉單，2027 年 EPS 成長的最大來源就會斷掉","ruling":"採納：列為唯一致命點，並設資料中心連兩季低於指引的減碼門檻","watch":"季度資料中心營收對指引、N+M 占資料中心比重、應收集中度","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"],"fact_refs":["f_kpi10"]},{"view":"論點成功但股東經濟變差","evidence":"8 月起以 5 億美元 6.75% 票據加 11 億定期貸款完成 Epiq 收購，另以現金加循環信貸付 Ophir 6.5 億；CFO 稱利息每季增加約 2,000 萬美元；資本支出承諾逾 16 億；FY25 自由現金流約為零","assumption":"N+M 與國防都成功，獲利就會留給股東","consequence":"營運成功的果實被高價併購、利息與持續擴產吃掉，每股自由現金流長期偏薄，股東報酬落後獲利成長","ruling":"採納：併購已實現報酬沒有數據，資本配置不給高分，長期信心上限為中","watch":"2027 年自由現金流、Ophir 交割後淨槓桿、是否再宣布大型併購","evidence_refs":["major_events#1","ma_merger#1"],"fact_refs":["f_kpi3_fcf","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"賣方雖然都給買進，Needham 已於 2026-09-21 把目標價由 220 降到 175；trailing P/S 與 EV/S 仍在自身年度端點八成以上分位；FY1 共識三個月上修約 23%，週期股在上修高峰時本益比往往最低","assumption":"16 倍前瞻、9.6 倍 FY27 已經夠便宜","consequence":"若市場改用週期中位獲利來定價，即使 2027 年兌現，股價也可能停在原地","ruling":"部分反駁：前瞻倍數已由前份的 25–30 倍以上降到約 16 倍，價格已經消化很大一塊週期風險；但用銷售倍數看仍在自身區間上緣，不構成安全邊際，所以不追","watch":"FY27 共識是否開始下修、P/S 是否回到自身區間中位","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 167.35 → 本次 80.11（-52.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=167.35","side_b":"本次 price_at_dd=80.11","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 167.35 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 167.35 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 167.35 美元：Bull 價 217.5、Bear 價 50，五年期望值 −27.5%，基準年化 −4.4%，不對稱比 0.24","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.24。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 167.35 美元：五年期望值 −27.5%，基準年化 −4.4%，不對稱比 0.24","side_b":"本次情境、股價 80.11 美元：五年期望值 +51.4%，基準年化 10.8%，不對稱比 2.61","ruling":"再換股價、情境不動：起點價下跌 52.1%，五年期望值多 78.9 個百分點，基準年化多 15.2 個百分點，不對稱比由 0.24 升到 2.61。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與機率（前份漂移）","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-05-18：股價 167.35，前瞻本益比約 25–30 倍以上，估值結論黃；前份第三條假設要求前瞻本益比守住 20 倍、股價落在 90–180 美元","side_b":"本次股價 80.11，FY26 前瞻約 16.2 倍、FY27 約 9.6 倍；前份第三條假設已破（倍數與股價雙雙跌破下限）","ruling":"股價腰斬是倍數壓縮，不是獲利下修（FY1 共識三個月上修約 23%）。估值結論維持黃，因為便宜建立在 AI 建置高峰的獲利上，分母本身就是爭點。情境機率與回撤範圍按本次股價重估：Bear 35%，回撤 −38% 到 −58%","evidence_level":"事實表股價、共識與倍數","settle_metric":"2027 年各季 non-GAAP EPS 是否守住指引下緣 8.10 的年化路徑","if_then":["若 Q4 財報資料中心營收達約 6.7 億美元且第三個 N+M 專案量產，重跑研究考慮小倉位試單","若資料中心營收連兩季低於指引 10% 以上，維持不買，已持有者減碼"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"品質與陷阱評等（前份漂移）","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份品質評等 B、價值陷阱風險黃","side_b":"本次品質評等 B、價值陷阱風險黃，但理由換了。品質一側：Q3 紀錄獲利（non-GAAP 營益率 17.4%）與訂單出貨比 2.13。陷阱一側：FY25 自由現金流約為零、EPS 成長遠快於營收、舉債併購讓利息每季多約 2,000 萬美元","ruling":"評等不變，組成換了：營運面變好、資產負債表變差，兩者抵銷","evidence_level":"財報新聞稿、法說會、8-K","settle_metric":"FY2027 自由現金流與淨槓桿","if_then":["若 2027 年自由現金流轉正且淨槓桿降到 1.5 倍以下，陷阱評等降為綠","若 2027 上半年自由現金流仍為負，陷阱評等升為紅"],"evidence_refs":["major_events#1","ma_merger#1"]},{"axis":"新增欄位（前份漂移）","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份為舊格式，護城河趨勢、五年後跑道、公司類型、週期位置與定期定額結論皆未填","side_b":"本次護城河趨勢持穩、五年後跑道黃、類型循環與商品、週期位置中循環；定期定額結論本流程不產出","ruling":"首次填寫，不代表判斷翻轉","evidence_level":"流程改版","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"行動門檻（重啟、減碼、清倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件，也沒有清倉或減碼門檻（兩欄皆空白）","side_b":"本次重啟：Q4 財報資料中心營收約 6.7 億美元、第三個 N+M 專案量產、FY26 自由現金流轉正。減碼：資料中心營收連兩季低於指引 10% 以上，或 non-GAAP 毛利率連兩季年減。清倉：主要 AI 客戶削減 N+M 下單，資料中心單季營收季減逾 20%","ruling":"新增門檻都來自本季新證據：Q3 資料中心比前季指引低約 10%，Q4 N+M 金額約為前季說法的一半，公司又已舉債併購","evidence_level":"法說會逐字稿、8-K","settle_metric":"Q4 2026 資料中心營收與 N+M 占比","if_then":["若 Q4 達成重啟三條件，重跑研究","若 Q4 資料中心營收再低於指引 10% 以上，維持不買"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（Single Thing 空白）","side_b":"主要 AI 客戶在 2027 年削減或轉單 N+M 專案，使資料中心單季營收季減逾 20%","ruling":"新設。資料中心約占 Q4 營收 49%，兩大客戶占 FY25 營收 23%，N+M 毛利遠高於公司平均，是 2027 年 EPS 成長最大的單一敏感項","evidence_level":"10-K 客戶集中度、法說會","settle_metric":"季度資料中心營收","if_then":["若發生，清倉","若 2027 上半年 N+M 占資料中心比重升向 50%，下調此風險機率"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"axis":"風險門檻改寫","cause":"新證據","prior_field":["R1","R2","R3"],"side_a":"前份：FY27 資本支出指引超過 3.5 億美元；A&D backlog 季減；前瞻本益比超過 40 倍，或半年內部人賣股逾 2,000 萬美元","side_b":"本次：資料中心營收連兩季低於指引 10%（減碼）；non-GAAP 毛利率連兩季年減（減碼）；Ophir 交割後淨槓桿高於 2 倍（減碼）；關稅使毛利率單季降逾 150bp","ruling":"舊門檻失效。資本支出已承諾 2025–2029 年逾 13 億再加 4 億，3.5 億門檻沒有鑑別力；前瞻本益比已降到約 16 倍，40 倍門檻沒有意義；A&D backlog 創新高 20 億。風險重心移到資料中心專案時程、中國新產能與舉債","evidence_level":"法說會、8-K","settle_metric":"季度資料中心營收、毛利率、淨槓桿","if_then":["若三條減碼門檻任兩條同時亮起，已持有者減碼一半"],"evidence_refs":["cyclical_supply_discipline_capacity#2","major_events#1"]},{"axis":"N+M 放量規模：管理層前後說法","cause":"新證據","prior_field":null,"side_a":"2026-08-05 Q2 法說 CFO：下半年 N+M 約 6 億美元，三分之一在 Q3、三分之二在 Q4（Q4 約 4 億）；同場 CEO 指引 Q3 資料中心占營收 49%","side_b":"2026-10-22 Q3 法說 CEO：Q3 資料中心占 41%；Q4 N+M 約占資料中心 30–32%，資料中心約 6.7–7 億美元，換算 N+M 約 2.1 億，CEO 卻又說「略低於 4 億」","ruling":"不可調和，兩組數字不能同時成立。採百分比口徑，因為 CEO 兩次回答都給出約三成占比與 6.7–7 億的資料中心金額，換算 Q4 N+M 約為前季說法的一半。公司把落差歸因於一家客戶專案時程延後：未證，列監測；若 Q1 2027 第三個專案仍未全面量產，視為歸因不成立","evidence_level":"兩場法說逐字稿","settle_metric":"Q4 2026 財報揭露的 N+M 營收或占比","if_then":["若 Q4 實際 N+M 接近 4 億美元，撤回本條並上調第一條假設的信心","若 Q1 2027 第三個 N+M 專案仍未全面量產，不買，已持有者減碼至半倉"],"evidence_refs":["customer_concentration_credit#1"]},{"axis":"併購規模：投資人日說法與實際","cause":"新證據","prior_field":null,"side_a":"2026-05-27 投資人日 CFO：地理擴張與小型策略併購機會，擴大的借款額度主要用於併購","side_b":"8 月起宣布或完成 Epiq 11 億美元現金收購、Ophir 6.5 億美元（待 2027Q2）、STG、ILFA 與英國兩家小廠；Q3 法說 CFO 稱大型併購到此告一段落","ruling":"採實際行為這一側：四個月內併購金額約占市值兩成，資金靠 6.75% 票據與 11 億定期貸款。併購已實現報酬沒有數據，資本配置不給高分","evidence_level":"8-K、逐字稿","settle_metric":"2027 年淨槓桿與 Epiq 營收貢獻","if_then":["若 2027 年再宣布 3 億美元以上併購，減碼","若 2027 年底淨槓桿降到 1.5 倍以下且自由現金流轉正，上調資本配置評價"],"evidence_refs":["major_events#1","ma_merger#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：中國逾 20 家 PCB 廠 2026 上半年宣布擴產，勝宏 Q1 資本支出約 36 億人民幣，臻鼎 13 座新廠興建中，產能 2026–2030 年分批開出","side_b":"結構轉好：多方來源指 AI 板與上游材料吃緊延續到 2027–2028 年，玻纖布新產能 2027 年後才到位，客戶要求中國以外的產能。其他結構變數：美中都把 PCB 列入關稅，約一半營收來自美國以外","ruling":"雙向拉鋸：2027 年以前結構性吃緊占上風，2028 年起新產能開出後，競爭惡化可能翻轉優勢","evidence_level":"產業新聞與 10-K","settle_metric":"中國同業高階板報價與稼動率、TTM 毛利率年增減","if_then":["若 2027 下半年 non-GAAP 毛利率轉為年減，判定競爭惡化占上風，不買"],"evidence_refs":["cyclical_supply_discipline_capacity#3","reg_tariff_export#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY27 公司指引 EPS 8.10–8.90，現價約 9.6 倍。訂單出貨比 2.13；90 天 backlog 13 億美元，年增 111%；A&D backlog 20 億，2027 年 A&D 營收約 65% 已有能見度。賣方平均目標價約為現價兩倍，股價仍在 104 週均線之上","side_b":"便宜靠的是高峰獲利；Q4 N+M 規模約只有前季說法一半；舉債併購與 16 億資本支出承諾都在週期中段加碼；近四季自由現金流為負","ruling":"不追。2027 年能見度足以支撐「不賣」，不足以支撐在 N+M 規模與資產負債表釐清之前建倉；等 Q4 財報這個具名事件","evidence_level":"財報、法說會、賣方目標價","settle_metric":"Q4 2026 財報（2027-02）","if_then":["若 Q4 達成重啟條件，重跑研究","若股價先漲但證據未到，不追","若股價下跌但重啟條件成立，分批反買"],"evidence_refs":["capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"Q4 財報確認 N+M 放量與現金轉正，才重啟研究","type":"估值rearm","maps_to":"H1","metric":"Q4 2026 資料中心營收、第三個 N+M 專案量產狀態、FY26 自由現金流","threshold":"資料中心營收約 6.7 億美元以上、第三個 N+M 專案進入量產、FY26 自由現金流大於零","action":"重跑完整研究，成立才以小倉位試單","source_freq":"季報與法說會","date":"2027-02","evidence_refs":[]},{"n":2,"text":"2027 年 N+M 組合推升利益率","type":"假設驗證","maps_to":"H1","metric":"調整後 EBITDA 利益率、non-GAAP EPS","threshold":"2027 年各季調整後 EBITDA 利益率不低於 20.1%，全年 non-GAAP EPS 不低於 8.10","action":"未達則下調 Base 路徑、不加碼","source_freq":"每季","date":null,"evidence_refs":[]},{"n":3,"text":"資料中心營收再度低於公司指引","type":"減碼","maps_to":"R1","metric":"資料中心營收相對公司當季指引口徑","threshold":"連兩季低於指引 10% 以上（Q3 已低約 10%）","action":"不買，已持有者減碼一半","source_freq":"每季","date":"2027-05","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","supply_demand_durability#5"]},{"n":4,"text":"中國新產能開出後毛利率轉弱","type":"風險","maps_to":"R2","metric":"non-GAAP 毛利率年增減","threshold":"連兩季年減（基準 Q3 2026 為 24.8%）","action":"減碼","source_freq":"每季","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#1","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"n":5,"text":"主要 AI 客戶削減或轉單 N+M","type":"Single Thing","maps_to":"R1","metric":"資料中心單季營收季增減","threshold":"單季季減逾 20%，且管理層歸因客戶下單減少","action":"清倉","source_freq":"每季","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":6,"text":"舉債併購後槓桿降不下來","type":"風險","maps_to":"R3","metric":"淨負債對近 12 個月調整後 EBITDA","threshold":"Ophir 交割後高於 2 倍，或 2027 年底未降到 1.5 倍以下，或再宣布 3 億美元以上併購","action":"減碼","source_freq":"每季","date":"2027-08","evidence_refs":["major_events#1","ma_merger#1"]},{"n":7,"text":"關稅或出口管制吃掉毛利","type":"風險","maps_to":"R4","metric":"non-GAAP 毛利率季增減與管理層歸因","threshold":"單季季減逾 150bp，且管理層歸因關稅或出口限制","action":"停止加碼","source_freq":"每季","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","geo_supply_chain#1"]},{"n":8,"text":"Q4 財報後複審","type":"複審日期","maps_to":null,"metric":"全部門檻","threshold":"Q4 2026 財報公布","action":"重跑研究","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"資料中心與網通營收相對公司指引","bear_threshold":"連兩季低於公司當季指引口徑 10% 以上","window":"2026Q4–2027Q1","source":"季度財報新聞稿與法說會","last_status":"warning"},{"metric":"non-GAAP 毛利率年增減","bear_threshold":"連兩季年減（基準 Q3 2026 為 24.8%）","window":"2027 全年","source":"季度財報新聞稿","last_status":"ok"},{"metric":"淨負債對近 12 個月調整後 EBITDA","bear_threshold":"Ophir 交割後高於 2 倍，或 2027 年底未降到 1.5 倍以下","window":"2027Q2–2027Q4","source":"10-Q 與法說會","last_status":"unknown"},{"metric":"A&D 訂單出貨比與專案 backlog","bear_threshold":"訂單出貨比連兩季低於 1.0 且 backlog 低於 18 億美元","window":"2027 全年","source":"季度法說會","last_status":"ok"}],"action_conditions":{"rearm_trigger":"Q4 財報（2027-02）資料中心營收約 6.7 億美元以上、第三個 N+M 專案量產、FY26 自由現金流轉正，三者同時成立","exec_line":"觀望不追。三項重啟條件同時成立才重跑研究；股價先漲但證據未到不追；股價下跌而重啟條件成立則分批反買；資料中心連兩季低於指引則維持不買。"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 Q4 2026 財報（2027-02）：資料中心營收約 6.7 億美元以上、第三個 N+M 專案量產、FY26 自由現金流轉正","qc48_result":null,"qc48_note":null,"trap":null,"val":null,"moat":null,"moat_trend":null,"runway_post_y5":null,"capalloc_grade":null,"archetype":null,"price_at_dd":null,"week26_return_pct":null,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":null,"val_denominator_note":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-46.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"N+M 不對稱板放量：資料中心營收中 N+M 占比由約三成升到 2027 年約五成，帶動調整後 EBITDA 利益率在 2027 年再升 200bp 以上","2y":"FY2027 non-GAAP EPS 不低於 8.10（指引下緣），各季調整後 EBITDA 利益率不低於 Q3 2026 的 20.1%","5y":null,"10y":null,"threshold":"2027 年各季調整後 EBITDA 利益率 ≥20.1%，全年 non-GAAP EPS ≥8.10","source":"季度財報新聞稿與法說會（N+M 占資料中心比重由 CEO 口頭揭露）","drift_rule":"兩年期：近四季獲利較指引路徑連兩季偏離 5% 以上視為削弱，連三季偏離 10% 以上視為反轉"},{"id":"H2","text":"國防與航太訂單續強：專案 backlog 不低於 20 億美元、訂單出貨比不低於 1.0；向上整合（Epiq、Ophir）讓高毛利長週期營收占比上升","2y":null,"5y":"FY2030 A&D 營收維持雙位數年增，backlog 持續高於 20 億美元","10y":null,"threshold":"A&D 訂單出貨比四季平均 ≥1.0，且專案 backlog ≥20 億美元","source":"季度法說會","drift_rule":"五年期：連四季偏離 5% 以上視為削弱，連六季偏離 10% 以上視為反轉"},{"id":"H3","text":"大型併購告一段落，2027 年自由現金流轉正並開始還債：Ophir 交割時淨槓桿低於 2 倍，2027 年底降到 1.5 倍以下","2y":"FY2027 自由現金流大於零；2027 年底淨槓桿 ≤1.5 倍；2027 年內沒有新的 3 億美元以上併購","5y":null,"10y":null,"threshold":"FY2027 自由現金流 >0，且 2027 年底淨槓桿 ≤1.5 倍","source":"10-Q、10-K 與法說會","drift_rule":"兩年期：自由現金流或槓桿連兩季偏離目標路徑視為削弱，連三季視為反轉"}],"R":[{"id":"R1","text":"資料中心專案時程與客戶集中：三個 N+M 大專案有一個延後，Q3 資料中心低於前季指引約 10%，Q4 N+M 約為前季說法一半；前十大客戶占 55%","h_ref":"H1","clock":"⚡","threshold":"資料中心營收連兩季低於公司指引 10% 以上","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","supply_demand_durability#5"]},{"id":"R2","text":"中國與台灣同業 2026–2030 年擴產潮，2028 年起高階板價格與稼動率回落，重演 2009、2019 年的毛利下滑但幅度更大","h_ref":"H1","clock":"🔥","threshold":"non-GAAP 毛利率連兩季年減","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#4","substitute_technology#0","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R3","text":"舉債併購：Epiq 11 億、Ophir 6.5 億，靠 6.75% 票據與 11 億定期貸款支應，利息每季多約 2,000 萬美元；併購報酬未證","h_ref":"H3","clock":"🔥","threshold":"Ophir 交割後淨槓桿高於 2 倍，或 2027 年再宣布 3 億美元以上併購","evidence_refs":["major_events#1","ma_merger#1"]},{"id":"R4","text":"地緣與關稅：約一半營收來自美國以外，中國是主要製造據點；美中都把 PCB 列入關稅，部分元件為有限或單一來源","h_ref":"H1","clock":"🐢","threshold":"毛利率單季季減逾 150bp，且管理層歸因關稅或出口限制","evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","geo_supply_chain#1"]}],"single_thing":{"description":"主要 AI 客戶在 2027 年削減或轉單 N+M 專案，使資料中心單季營收季減逾 20%","why_fatal":"資料中心約占 Q4 營收 49%，兩大客戶占 FY25 營收 23%；N+M 毛利遠高於公司平均，2027 年 EPS 由約 5 美元升到 8 美元以上，主要靠它","if_happens":"2027 年 EPS 落到指引下緣以下，市場改用週期谷底倍數定價，股價可能再跌三到五成","how_monitor":"每季資料中心營收對指引、CEO 揭露的 N+M 占資料中心比重、10-K／10-Q 客戶與應收集中度","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":9.61,"peg_fy2":0.47,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.68,"FY2026E":4.96,"FY2027E":8.34,"FY2028E":10.06},"fy_end_month":12,"eps_basis":"基期 FY2025A 為 GAAP 稀釋 EPS（事實表年度財報；non-GAAP 基期未涵蓋）；FY2026E–FY2028E 為 Koyfin non-GAAP 共識，口徑不一致，共識成長率以 FY26→FY28 兩年計"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年分終端市場指引","impact":"高","watch":"資料中心營收是否達約 6.7 億美元、N+M 占比、FY26 自由現金流"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"第三個 N+M 大專案全面量產（CEO 稱 Q4 下半爬坡、Q1 全面生產）","impact":"高","watch":"Q1 2027 法說是否確認全面量產"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"Ophir Optics 6.5 億美元收購預計交割","impact":"中","watch":"交割後淨槓桿是否低於 2 倍"},{"date":"2028-03","date_precision":"quarter","type":"capacity","event":"新增 4 億美元 N+M 擴產開始貢獻 2028 年營收","impact":"中","watch":"同期中國同業新產能開出與報價"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：channel_business_model_shift（通路／商業模式轉移）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
