你是 DD 管線 v20 的判斷層閘（gate），標的 RMBS（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（41 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝218.3 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：高於公司自家指引 210–216
- `f_kpi1_product_revenue`（q1_business）｜Product revenue＝114.3 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：—
- `f_kpi2_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝102.2 USD m（利益率 46.8%，新聞稿四捨五入 47%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：未查得可靠共識值
- `f_kpi3_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝83.7 USD m（利益率 38.3%，新聞稿四捨五入 38%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：未查得可靠共識值
- `f_kpi6_non_gaap_product_gross_m`（q1_business）｜Non-GAAP product gross margin＝60.4 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：落在公司 60–63% 區間低端；管理層稱因供應鏈投入成本
- `f_kpi7_guidance_q4_2026_revenue`（q1_business）｜Guidance Q4 2026 revenue＝227–233 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm；Q4 指引另含 product 127–133、royalties 68–74、contract 26–32、non-GAAP opex 120–124、GAAP EPS 0.68–0.76、non-GAAP EPS 0.84–0.92（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：FY1 營收共識 838.4（yfinance，全年口徑），無單季 Q4 共識值
- `f_peer_rmbs_gross_margin_pct`（q2_moat）｜RMBS 毛利率＝79.14 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RMBS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_rmbs_operating_margin_pct`（q2_moat）｜RMBS 營業利益率＝36.73 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RMBS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_rmbs_fcf_margin_pct`（q2_moat）｜RMBS FCF 利潤率＝39.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RMBS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_688008_ss_gross_margin_pct`（q2_moat）｜688008.SS 毛利率＝65.82 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.688008.SS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_688008_ss_operating_margin_pct`（q2_moat）｜688008.SS 營業利益率＝43.73 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.688008.SS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_688008_ss_fcf_margin_pct`（q2_moat）｜688008.SS FCF 利潤率＝42.26 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.688008.SS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_snps_operating_margin_pct`（q2_moat）｜SNPS 營業利益率＝11.03 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNPS.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_arm_operating_margin_pct`（q2_moat）｜ARM 營業利益率＝17.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ARM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mrvl_operating_margin_pct`（q2_moat）｜MRVL 營業利益率＝16.81 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_kpi4_free_cash_flow`（q1_business）｜Free cash flow＝91.3 USD m（OCF 102.5 − capex 11.2；非公司定義，自行推算；占營收 41.8%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：未查得可靠共識值
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.11 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.88 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝4.89 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝838.42 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1010.31 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（8 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝2.64 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 3.03 → 3.11（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝20.5 %（SBC 17.1m；占營收 7.8%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿（SEC EDGAR）https://www.sec.gov/Archives/edgar/data/0000917273/000119312526431918/rmbs-ex99_1.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：未查得可靠共識值
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-756.69 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 20.22、現金 776.91（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝107.1 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝85.71 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝27.56 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 3.11，分子＝快照價 85.71｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝35.42 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／3 個年度端點內的分位＝55.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝55.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝11.53 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝41.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝41.4 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝10.58 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝29.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝29.5 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝10.05 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝8422.77 USD m｜期間與口徑：2026-11-03／市值 9179.46 ＋ 淨負債 -756.69｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-23.13 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝39.73｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝105.43 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝85.8 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝62.41 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝1.51 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：部分客戶內部評估或開發主張無需向 Rambus 授權的技術；公司無法預測在 AI 等目標市場能取得或維持的市占。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：第三方分析稱 Rambus Q1 2026 產品營收成長約 15% 低於市場成長，Montage、Renesas 在搶市占。
  - 來源：munich-startup insights: Rambus misses Q1 targets as rivals capture AI memory market share（as_of 2026-05-01）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 前五大客戶占合併營收約 66%（2024、2023 皆 62%），公司預期集中度將持續。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：Q3 2026 累計前五大客戶占營收 63%，Customer A 23%、Customer B 18%（二手摘要）。
  - 來源：Panabee: Rambus Earnings Q3 2026 report（as_of 2026-10-26）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：TrendForce：NAND 2026 年供給短缺 4-5%，2027 下半年供給位元成長將超過需求成長。
  - 來源：TrendForce via itiger: NAND Flash Supply Shortage Expected to Ease in Second Half of 2027（as_of 2026-07-20）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Rambus 10-Q（截至2026-06-30）揭露自2026年Q1起正回應美國司法部反壟斷署刑事調查的聯邦大陪審團傳票；可能結果含罰款、改變營運做法或禁制令。
  - 來源：SEC EDGAR 10-Q（期間2026-06-30）（as_of 2026-07-28）｜affects：decision_inputs.bear、thesis.R、moat_trend
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：MLex 報導 Rambus 依 2026-04-28 監管申報為美國司法部刑事反壟斷調查對象。
  - 來源：MLex：Rambus targeted in US DOJ criminal antitrust probe（as_of 2026-04-28）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：公司為無廠半導體，關稅與貿易限制可能影響客戶需求與供應鏈；美國對半導體相關產品出口中國的管制若擴及公司主力產品/市場，可能衝擊公司。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 載明貿易行動（美、中、歐等的關稅、報復性關稅）可能使客戶需求下降並間接降低對公司產品需求；公司無法預測政府行動。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2022 10-K 風險因素：部分第三方為唯一製造商或特定材料唯一來源，可能位於地緣政治不確定地區（例：台灣）。
  - 來源：Rambus Form 10-K FY2022 (SEC)（as_of 2023-02-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 風險因素：第三方製造商/供應商可能位於中台緊張與出口/國安限制影響地區，單一夥伴中斷可能影響出貨；地緣衝突可能限制或延遲產品供應。
  - 來源：Rambus Form 10-K FY2025 (SEC)（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：日本分析認為記憶體成長多來自價格飆升而非量，2027 記憶體成長可能停滯，WSTS 2027 展望偏樂觀（少數觀點）
  - 來源：EE Times Japan 大山聡 業界スコープ(101)（as_of 2026-06-08）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素自述：若替代技術以相當效能、相近或更低成本出現，或被認為需付較低/無權利金，客戶可能採用並推廣；即使認定侵權也未必能不經訴訟談成授權。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 業務章節同樣載明替代技術風險，且專利執行可能需訴訟、結果不確定。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-18）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Q3 2026 法說提及記憶體 de-specing（客戶因記憶體經濟性降低模組容量）為需求風險，並討論 SOCAMM2 模組形式。
  - 來源：Rambus Q3 2026 Earnings Call Transcript (Webull)（as_of 2026-10-26）｜affects：thesis.R、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：MarketBeat 稱 Q1 2026 指引低於預期造成股價重設
  - 來源：MarketBeat, Why Rambus market reset might be the best news bulls get（as_of 2026-02-15）｜affects：decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-02-03 股價單日下跌 13.42%（收 98.45 美元）後，Pomerantz 律所於 2026-02 公告調查 Rambus 及其高管是否涉及證券詐欺；僅為律所調查，搜尋未見已提起的集體訴訟。
  - 來源：Pomerantz 新聞稿（Barchart／Minster Community Post 轉載）（as_of 2026-02-24）｜affects：decision_inputs.bear、triggers
- `major_events#2`（major_events｜方向 -｜狀態 ok）：搜尋摘要提及 Rambus 收到與司法部反壟斷調查相關的聯邦大陪審團傳票（未讀到頁面，待核原文）。
  - 來源：Yahoo Finance Rambus Q1 2026 文章（as_of 2026-04-27）｜affects：decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Pomerantz 律所 2026-02 公告調查 Rambus 是否涉及證券詐欺，起因為 2026-02-03 股價下跌 13.42%；僅為調查，未確認有已提起的集體訴訟。
  - 來源：Pomerantz 新聞稿（Barchart 轉載）（as_of 2026-02-24）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":226.8,"bear_5y_price":55.5,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":69.1,"ev5y_pct":61.7,"irr_base_pct":11.1,"asym_ratio":3.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.11,"pe":27.56,"basis":"FY2026E 非 GAAP 共識 EPS（Koyfin 2026-10-31）；終端倍數同樣套在終端年當年度非 GAAP EPS，口徑一致"},"eps":{"bull":[4.05,5.05,6.05,7.05,8.1],"base":[3.8,4.5,5.1,5.7,6.3],"bear":[3.4,3.0,3.1,3.4,3.7]},"pe":{"bull":28,"base":23,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.8},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### RMBS_Q2_2026_Earnings_Call_20260727.md
- 2026-07-27｜Sumeet Gagneja (CFO)｜guidance：CFO 給 Q3 總營收財測區間 2.10–2.16 億美元（原話："third quarter to be between $210 million and $216 million."）
- 2026-07-27｜Sumeet Gagneja (CFO)｜guidance：CFO 給 Q3 產品營收財測 1.10–1.16 億美元，中點季增 14%（原話："$110 million and $116 million, a sequential increase of 14% at the midpoint of guidance."）
- 2026-07-27｜Sumeet Gagneja (CFO)｜guidance：CFO 給 Q3 權利金營收財測 6,900–7,500 萬美元（Q2 實際為 8,420 萬）（原話："royalties revenue to be between $69 million and $75 million"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜guidance：CFO 給 Q3 非 GAAP EPS 財測 0.75–0.82 美元（原話："non-GAAP earnings per share range between $0.75 and $0.82."）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 表示下半年將強於上半年，並維持逐季給財測、不給一季以後（原話："our second half is going to be stronger than our first half"）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 說明財測僅逐季提供（原話："but we will continue to guide quarter-by-quarter."）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 表示矽智財業務維持年增 10%–15%（原話："we continue to see that business growing 10% to 15% a year"）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 表示 MRDIMM 於 Q4 貢獻極小，較實質貢獻在 2027（原話："The contribution for Q4 is going to be minimal."）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 指出 MRDIMM 較實質貢獻發生在 2027 平台放量時（原話："contribution is going to happen in 2027 when both platforms from the CPU guys"）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 表示新產品占產品營收比重預計到 Q4 底達中雙位數百分比（原話："And that's going to be in the mid double digits"）
- 2026-07-27｜Luc Seraphin (CEO)｜guidance：CEO 說明 Q3 產品營收年增幅度與本季相近（原話："Next quarter, we're going to see the same growth"）
- 2026-07-27｜Luc Seraphin (CEO)｜margin：管理層重申毛利率長期模型 60%–65%，並表示季間會波動（原話："Our model remains 60% to 65%"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜margin：CFO 指出近期毛利率落在 60%–63%（原話："we've been operating in the 60% to 63% gross margin"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜margin：CFO 宣布此後財報與財測只以 ASC 606 營收口徑呈現，不再揭露授權帳單（billings）（原話："guidance on an ASC 606 revenue basis going forward."）
- 2026-07-27｜Sumeet Gagneja (CFO)｜margin：CFO 報告 Q2 營收 2.074 億美元（原話："Revenue for the second quarter was $207.4 million"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 表示 Q2 無產能問題（同時提到供應鏈緊俏、交期拉長）（原話："we didn't have any capacity issue in Q2"）
- 2026-07-27｜Luc Seraphin (CEO)｜commitment：CEO 表示公司想維持或提高 DIMM 市占（標準品無漲價空間）（原話："maintain or continue to increase our share in the DIMM market."）
- 2026-07-27｜Luc Seraphin (CEO)｜commitment：CEO 表示產品投資將集中於標準品，而非 CXL 類客製 ASIC 產品（原話："we'd rather invest into standard products at this point in time."）
- 2026-07-27｜Sumeet Gagneja (CFO)｜commitment：CFO 表明其工作重點之一為審慎配置資本（原話："allocate capital thoughtfully"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜capital_allocation：CFO 報告期末現金及有價證券 8.25 億美元，較 Q1 增加 3,900 萬（原話："marketable securities totaling $825 million, up $39 million from Q1"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜capital_allocation：CFO 說明 Q2 存貨增加 1,600 萬美元，用於支援產品放量與供貨保證（原話："Inventory increased by $16 million during the quarter"）
- 2026-07-27｜Luc Seraphin (CEO)｜capital_allocation：CEO 說明公司對關鍵產品建立策略性庫存（原話："We build strategic inventory for the"）
- 2026-07-27｜Sumeet Gagneja (CFO)｜capital_allocation：CFO 報告 Q2 自由現金流 4,900 萬美元（原話："Free cash flow in the quarter was $49 million."）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 表示 2027 年供應限制仍將存在（原話："the supply constraints will continue to be there in 2027."）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 表示對需求假設有信心，但對平台時程與供應採審慎態度（原話："we are prudent with respect to platform timing and supply"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 指出平台放量歷來比外界預期慢（原話："platform ramps typically take a little bit"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 回答客戶端無過度備貨跡象（原話："We don't see any signs of our customers building inventory"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 表示標準品沒有漲價空間（原話："we don't see any opportunity, I would say, for"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：新任 CFO 在本次法說首度亮相（原話："welcome Sumeet Gagneja to his first earnings call"）
- 2026-07-27｜Luc Seraphin (CEO)｜risk：CEO 提到 Q1 曾有製造問題，仍年增 15%（原話："despite the manufacturing issue we had, it was 15% higher"）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 說明新產品目前占產品營收低雙位數百分比（原話："were in a low double-digit percentage of the product revenue."）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 表示 LPDDR/SOCAMM 短期營收貢獻有限，但策略重要性高（原話："the short run is modest, but the strategic importance is really high for us."）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 認為產業並未轉向 LPDDR，LPDDR 屬增量機會（原話："I wouldn't say that the industry is shifting to LPDDR."）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 說明 MRDIMM 模組上的矽含量為 4 倍（原話："MRDIMM with 4x the silicon content on the module"）
- 2026-07-27｜Luc Seraphin (CEO)｜product：CEO 說明 PCIe 7.0 授權收入在未來幾季出現，不需等終端產品放量（原話："in the coming quarters, because it's a licensing business"）
- 2026-07-27｜Luc Seraphin (CEO)｜competition：CEO 描述 CXL 產品市場呈客製 ASIC、分散化（原話："a custom ASIC business that is fragmented for us"）
- 2026-07-27｜Luc Seraphin (CEO)｜competition：CEO 回應 CXMT：記憶體廠商都需與 Rambus 簽授權（原話："has to have a license agreement with us"）
- 2026-07-27｜Luc Seraphin (CEO)｜competition：CEO 表示伺服器單位成長預期由中高個位數升至雙位數，公司自認成長快於市場（原話："Now it's double-digit growth."）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 揭露與一家美國一線超大規模雲端業者的下一代 HBM 設計案（原話："an exciting design win with a Tier 1 U.S. hyperscaler"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 確認該設計案為 IP 而非晶片產品（原話："It's an IP design win"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 說明該 IP 為授權模式而非按量計價（原話："it's a license or multi-license"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 表示超大規模雲端業者在定義自家架構上角色日增（原話："hyperscalers are playing a growing role"）
- 2026-07-27｜Luc Seraphin (CEO)｜customer：CEO 表示對需求的信心持續增加（原話："I think our confidence is continuing to build."）

### 問答異常語氣（迴避／改口／保留）
- RMBS_Q2_2026_Earnings_Call_20260727.md｜問：Gary Mobley 問 Q4 能見度與上季相比如何｜答法：CEO 說信心增加，但未給 Q4 具體數字，改談 Q3 年增與逐季給財測
- RMBS_Q2_2026_Earnings_Call_20260727.md｜問：Tristan Gerra 問 2027 年成長是否能高於 20%｜答法：CEO 稱不給一季以後的財測，只列正面需求因素並強調供應與平台時程審慎，未給成長數字
- RMBS_Q2_2026_Earnings_Call_20260727.md｜問：Mehdi Hosseini 問拉高市占是否使產品毛利率停在 60% 初段｜答法：CEO 與 CFO 未直接回答取捨，重申 60%–65% 長期模型並說季間波動、宜看年度

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 6 | 3 |
| major_events | found | 3 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260620","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"RMBS 守住 DDR5 RCD co-leader 份額並把領先延伸至 MRDIMM/HBM4","columns":{"2Y 驗證點":"RCD 份額維持 mid-40%；MRDIMM 2026 量產","5Y 驗證點":"HBM4/MRDIMM 成為 product 主要成長源","10Y 驗證點":"不被 Montage 在新一代奪份額","具體數字門檻":"RCD 份額 ≥ 40%；product 年成長 ≥ 15%","信息來源":"Rambus 法說（2026-04-27）+ 產業數據","漂移觸發條件":"product 連 2 季 QoQ 下滑或份額 &lt; 40% → 削弱"}},{"id":"H2","text":"AI 伺服器記憶體內容量價齊升，TAM 從 RCD $800M 擴至 $2B+","columns":{"2Y 驗證點":"MRDIMM + companion chips TAM 開始貢獻","5Y 驗證點":"HBM4/CXL 內容成為新成長曲線","10Y 驗證點":"記憶體介面晶片 TAM 持續擴張","具體數字門檻":"buffer 市場 CAGR ~35%；MRDIMM late 2026 ramp","信息來源":"產業報告（buffer 市場 $866M, CAGR 34.8%）","漂移觸發條件":"MRDIMM/HBM4 ramp 延後 2+ 季 → 削弱"}},{"id":"H3","text":"市場願意給 RMBS 成長溢價倍數（非壓回歷史授權公司倍數）","columns":{"2Y 驗證點":"FY+2 Fwd PE 維持 &gt; 25x","5Y 驗證點":"PEG 隨成長兌現回落至 &lt; 1.5","10Y 驗證點":"RMBS 估值定錨在 AI 記憶體 25-30x","具體數字門檻":"Fwd PE &gt; 25x 持續","信息來源":"§13 歷史分位 + 同業","漂移觸發條件":"Fwd PE 跌破 22x + EPS 共識下修 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Montage 在 MRDIMM/HBM4 新一代搶下份額","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"RCD/MRDIMM 份額、design-win 公告","警戒閾值":"RCD 份額 &lt; 40% 或 MRDIMM 落後 Montage"}},{"id":"R2","text":"DRAM/伺服器記憶體週期回落（庫存修正）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"product 季度 QoQ、DRAM 廠 capex/庫存","警戒閾值":"product 連 2 季 QoQ 下滑"}},{"id":"R3","text":"記憶體架構演進壓縮獨立介面晶片價值（近記憶體運算 / 內建控制）","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"次世代記憶體架構路線圖","警戒閾值":"主要 DRAM/CPU 廠推內建介面方案（需 ≥50% 機率才砍倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":141.17,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"RMBS","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Rambus Inc."},"oneliner":"Rambus 靠伺服器 DDR5 介面晶片與記憶體專利收錢，Q3 再超指引、Q4 產品營收指引年增 34%；股價半年跌兩成多後 FY2027 本益比約 22 倍，估值轉合理，但份額方向、DOJ 刑事調查與 2028 年記憶體循環三件事未解，分批建倉不一次買滿","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺三筆錢：DRAM 廠與模組廠買的伺服器記憶體介面晶片（約五成營收）、所有 DRAM 廠付的專利權利金（約三成五）、晶片設計商付的矽智財授權（約一成二）；錢卡在 JEDEC 標準介面晶片的平台認證節點","reasoning":"Q3 營收 2.183 億美元、年增 22%，高於公司指引 2.10–2.16 億：產品 1.143 億（52%）、權利金 0.770 億（35%）、合約及其他 0.270 億（12%）。最新一季 GAAP 營業利益率 38.3%、非 GAAP 46.8%，非 GAAP 產品毛利率 60.4%，TTM 混合毛利率 79.1%。產業時鐘判 III：上游交期拉長、客戶比過去提早下單、記憶體經濟性迫使客戶降低單模組容量（2026-10-26 法說），依據是供需訊號而非股價。供需持久性：週期性將反轉。AI 推動的記憶體缺貨預期延續到 2027（Gartner；JPMorgan 稱 2028 年初前無顯著新產能），但 TrendForce 預期 NAND 在 2027 下半年供給成長將超過需求，反轉時點落在 2027 下半年到 2028。單點依賴：前五大客戶占 FY2025 營收約 66%、Q3 累計最大客戶 23%、次大 18%，屬集中度風險，不是護城河證據；10-K 也載明部分代工為唯一來源且位在台海風險區。產業態勢三軸：競爭面惡化（Montage 先拿第一代 MRDIMM 設計案）、需求結構轉好（CPU 對 GPU 比例上升、伺服器通道數由 8 增至 12–16）、其他結構變數為 DOJ 反壟斷刑事調查與出口管制，裁決為雙向拉鋸。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_product_revenue","f_kpi2_non_gaap_operating_incom","f_kpi3_gaap_operating_income_ma","f_kpi6_non_gaap_product_gross_m","f_kpi7_guidance_q4_2026_revenue","f_peer_rmbs_gross_margin_pct"],"verdict_values":{"revenue_quality":"三條收入線性質不同：產品看伺服器出貨與世代轉換，循環性中等；權利金為長約、近乎全毛利，但 2026-07-27 起公司不再揭露授權帳單；合約及其他以矽智財為主，靠設計案驅動、年增 10–15%。Q3 三線合計年增 22%，高於指引上緣","unit_econ_note":"產品毛利率約 60–63%，權利金近乎全毛利，TTM 混合毛利率 79.1%；營業費用季約 7,000 萬美元持平，產品放量帶來營業槓桿，Q4 非 GAAP 營業利益指引 1.03–1.13 億","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利、淨現金、FCF 轉換率高於淨利，但產品線隨伺服器與記憶體循環起伏"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：缺貨延續到 2027（Gartner 2026-08、JPMorgan／BofA 2026-09），NAND 供給在 2027 下半年追上需求（TrendForce 2026-07），客戶提早下單屬拉貨訊號（2026-10-26 CEO）","bargaining":{"up":"代工、基板、封測交期拉長、投入成本上升，非 GAAP 產品毛利率壓到 60.4%（區間下緣）；部分供應商為唯一來源","down":"前五大客戶占 FY2025 營收約 66%，Q3 累計最大客戶 23%、次大 18%，以三大 DRAM 廠為主；標準品沒有漲價空間（2026-07-27 CEO）","geo":"2025 年總部在美國以外的客戶占營收 82%；出口管制若擴及主力產品會受衝擊；唯一來源代工位在台海風險區"},"profit_pool_dir":"記憶體價值鏈這一輪利潤集中在缺貨漲價的 DRAM 廠，介面晶片環節分到量、分不到價","tam_table":[{"item":"DDR5 RCD 份額","value":"2025 年底約 mid-40%，高於 2024 年 early 40s（管理層自述，無第三方數據）"},{"item":"MRDIMM 總市場","value":"約 6 億美元，放量比 RCD 世代平緩（2026-10-26 CEO）"},{"item":"新產品占產品營收","value":"年初低雙位數百分比，目標 Q4 底達中雙位數（2026-07-27 CEO）"},{"item":"矽智財業務規模","value":"約 1.3 億美元，年增 10–15% 偏高端（2026-10-26 CFO）"},{"item":"RCD 市場總額、段 CAGR、營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平：RCD 共同領先者靠 JEDEC 平台認證與專利組合守住地位，但標準品沒有定價權、毛利被上游擠壓，Montage 先拿第一代 MRDIMM，份額方向有爭議","reasoning":"機制：DDR5 RCD 是 JEDEC 標準件，每一代平台都要經 CPU 廠與三大 DRAM 廠認證，同世代內換供應商成本高；三十年記憶體介面專利讓所有 DRAM 廠都要付權利金（2026-07-27 CEO：記憶體廠都要簽授權）。方向證據：管理層稱 2025 年底份額約 mid-40%、高於前一年；Q3 產品營收年增 22%、Q4 指引中點年增 34%，快於伺服器出貨的雙位數成長（2026-07-27 CEO）。反向證據：第三方稱 Q1 產品年增約 15% 低於市場、Montage 與 Renesas 搶份額；第一代 MRDIMM 由對手先拿設計案（2026-10-26 法說問答）；標準品不能漲價、產品毛利 60.4% 落在區間下緣。同業比較：同業 ROIC 事實表未涵蓋，改看利潤率；Montage 營業利益率 43.7%、FCF 利潤率 42.3%，都高於 RMBS 的 36.7%、39.3%，RMBS 混合毛利 79.1% 是權利金撐出來的。執行力 8 分（連兩季超指引上緣、第六代 9600 RCD 已廣泛送樣），定價力 6 分（標準品無漲價權、上游擠壓）；等級 B，方向持平：執行穩定、定價小幅縮減，份額爭議在 2027-02 法說揭露前不給擴大。","fact_refs":["f_peer_rmbs_gross_margin_pct","f_peer_rmbs_operating_margin_pct","f_peer_rmbs_fcf_margin_pct","f_peer_688008_ss_gross_margin_pct","f_peer_688008_ss_operating_margin_pct","f_peer_688008_ss_fcf_margin_pct","f_peer_snps_operating_margin_pct","f_peer_arm_operating_margin_pct","f_peer_mrvl_operating_margin_pct","f_kpi6_non_gaap_product_gross_m","f_kpi2_non_gaap_operating_incom","f_kpi4_free_cash_flow"],"verdict_values":{"moat":{"mechanism":"JEDEC 標準介面晶片的世代認證轉換成本，加上所有 DRAM 廠都要授權的記憶體介面專利組合；矽智財在 HBM、PCIe、硬體安全提早進入客戶架構規劃","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定（Q3 營收 2.183 億超指引上緣、第六代 9600 RCD 廣泛送樣）；定價面縮減（產品毛利 60.4% 在區間下緣、標準品不能漲價）；份額面管理層自述上升與第三方 Q1 搶份額報導方向相反，綜合判持平","competitor_notes":[{"name":"Montage Technology（688008.SS）","strategy_note":"營業利益率 43.7%、FCF 利潤率 42.3% 都高於 RMBS，產品純度更高；先拿第一代 MRDIMM 設計案、第三方稱 Q1 搶份額，是最直接的份額威脅"},{"name":"Renesas","strategy_note":"RCD 第三家供應商，事實表無財務數字；第三方稱與 Montage 同步搶份額"},{"name":"Synopsys（SNPS）","strategy_note":"10-K 點名的矽智財對手，毛利 72.4%、營業利益率 11.0%，規模大，在 HBM、PCIe IP 正面競爭"},{"name":"Arm（ARM）","strategy_note":"純授權模式毛利 97.5% 但營業利益率只有 17.3%，說明授權高毛利不保證高營業利益，可對照 RMBS 權利金段"},{"name":"Marvell（MRVL）","strategy_note":"客製 ASIC 與互連領域的對手面，營業利益率 16.8%，不在 RCD 正面競爭"}],"peer_na_reason":"同業 ROIC 事實表未涵蓋，以營業利益率與 FCF 利潤率替代比較","threats":[{"level":"🟡","text":"Montage、Renesas 在第六代 RCD 與 MRDIMM 正面搶份額；Montage 營業利益率高於 RMBS，屬點對點競爭","p":"35%","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#0","customer_second_source#0"]},{"level":"🟡","text":"客戶自行開發主張不需授權的技術，或 DRAM 廠自製介面晶片","p":"15%","evidence_refs":["competitive_share_entrants#1","customer_second_source#1"]},{"level":"🟡","text":"記憶體架構替代：LPDDR／SOCAMM 板載方案與客戶降低單模組容量，壓低每模組價值；管理層稱互補不取代，目前屬增量","p":"20%","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"DOJ 反壟斷刑事調查若帶來營運做法限制，可能削弱授權與銷售條件；調查範圍未揭露","p":"20%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"高利益率×周轉待查：稅後營業利益率約 30.9%（TTM 營業利益率 36.7%×(1−16%)）；投入資本事實表未涵蓋，輕資產推測周轉偏高","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是雲端與 OEM 伺服器，決策者是 CPU 平台與 DRAM 廠的認證流程，付款者是模組廠；每支 DDR5 伺服器模組都要 RCD，屬需要不是想要；通道數由 8 增至 12–16 讓模組數增加，客戶降規格只降單模組容量不降模組數（2026-10-26 CEO）"},{"item":"決策層級","level":"🟡","text":"替代性要在每一代平台認證時衡量：同世代內換供應商要重新認證、轉換成本高，但每次世代轉換都重開競局；第一代 MRDIMM 已由對手先拿設計案，代理變數是各世代設計案歸屬與份額"},{"item":"價值鏈分配","level":"🟡","text":"買方集中（前五大約 66%）、標準品不能漲價，上游代工與封測交期拉長把產品毛利壓到 60.4%；這一輪缺貨利潤留在 DRAM 廠。所有 DRAM 廠都付權利金，撐住整體 79% 毛利"},{"item":"社會容忍度","level":"🟡","text":"專利授權依賴法律執行，10-K 自承執行可能需要訴訟；DOJ 反壟斷刑事調查進行中、範圍未揭露，若涉及授權或定價做法就成為政策上限；目前未見起訴，暫列中性偏負並寫入反證紀錄"}],"roiic":95,"reinvest_rate":18,"endo_ceiling":17,"formula_note":"單位為 %。NOPAT 約 3.43 億＝Q3 非 GAAP 營業利益 1.022 億×(1−16%)×4；再投資＝資本支出年化約 0.4 億（D&A 事實表未涵蓋，淨資本支出取 0～0.4 億）＋存貨每年增加約 0.4 億（Q2 1,600 萬、Q3 1,200 萬、Q4 計畫相近），再投資率 12%～23%，取 18%；增量 ROIC：GAAP 營業利益 FY2024 1.79 億→FY2025 2.60 億，稅後增量約 0.68 億，對照每年再投資約 0.7 億，約 95%；內生上界約 95%×18%≈17%。研發全數費用化，公式低估無形再投資，只當上界參考"}}}},"q3_growth":{"verdict":"五年後成長空間中等：RCD 滲透已到頂，成長靠份額與每模組含量，MRDIMM、SOCAMM2、矽智財等第二曲線有來源但都比 RCD 世代平緩","reasoning":"成長來源：量為主（伺服器出貨轉雙位數成長、通道數增加、周邊晶片放量），價格不貢獻（標準品不漲價），沒有併購，淨回購每年約 1 個百分點。三年共識非 GAAP EPS：FY2026E 3.11、FY2027E 3.88、FY2028E 4.89（Koyfin，家數事實表未涵蓋；營收共識 7–8 位分析師），以 FY2025A 回推約 2.51 計，年化約 24.9%；內生上界約 17%（見護城河段推導），缺口約 8 個百分點，歸因營業槓桿約 7 個百分點（營業費用季約 7,000 萬持平而產品營收放大，Q4 非 GAAP 總成本指引 1.20–1.24 億對營收 2.27–2.33 億）與淨回購約 1 個百分點，不依賴重新評價。成長空間：RCD 已是每支 DDR5 伺服器模組的標配，滲透率天花板已到；第二條曲線有來源但都比 RCD 平緩，MRDIMM 市場約 6 億美元但放量較淺（2026-10-26 CEO），SOCAMM2 約 2028 年上市且屬利基，矽智財約 1.3 億、年增 10–15% 偏高端。衰退信號亮兩個（EPS 成長快於營收逾 5 個百分點、核心份額方向有第三方反證），長期成長性中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi1_product_revenue","f_kpi7_guidance_q4_2026_revenue","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"量為主（伺服器模組數、通道數、周邊晶片含量），價格零貢獻，併購零，淨回購約每年 1 個百分點","runway_years":"RCD 已全面滲透；MRDIMM、SOCAMM 新品類滲透率事實表未涵蓋，以管理層市場規模與放量節奏推估第二曲線約 3～5 年","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段再投資推導：增量 ROIC 約 95%×再投資率約 18%＝約 17%；研發費用化使公式偏低","segments":[{"item":"產品（RCD、周邊晶片、MRDIMM）","value":"Q3 1.143 億，年增 22%、季增 15%；Q4 指引 1.27–1.33 億，中點年增 34%；2026 全年約年增 24%"},{"item":"權利金","value":"Q3 0.770 億（去年同期 0.651 億）；Q4 指引 0.68–0.74 億；近乎全毛利"},{"item":"合約及其他（矽智財為主）","value":"Q3 0.270 億，年增 35%；矽智財總規模約 1.3 億、年增 10–15% 偏高端，部分認列在權利金"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"產品毛利 60.4% 在區間下緣，年比資料事實表未涵蓋；TTM 混合毛利 79.1% 對 FY2025 79.6% 小降"},{"item":"核心市占近 12 個月縮減","lit":true,"note":"第三方稱 Q1 被 Montage、Renesas 搶份額，管理層自述相反，爭議未決先計亮"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"標準品未提價"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"2026 年非 GAAP EPS 約年增 24%、營收約 18%，差 6 個百分點，來自營業槓桿"},{"item":"FCF／淨利 < 0.75 連 2 年","lit":false,"note":"FY2025 為 1.45 倍、FY2024 為 1.11 倍"},{"item":"SBC／營收 > 5% 且逐年上升","lit":false,"note":"Q3 為 7.8%，超過 5%，但逐年趨勢事實表未涵蓋，暫不計亮"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"客戶降低單模組容量但模組數增加"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"item":"維護性資本支出占 FCF > 60%","lit":false,"note":"Q3 資本支出 1,120 萬對 FCF 9,130 萬"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"營收連三年成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：現金轉換強、淨現金充裕、回購大致抵銷稀釋，但回購買在偏高的價位；近一年沒有併購","reasoning":"FCF 轉換：FY2025 FCF 3.33 億對淨利 2.30 億（1.45 倍），FY2024 為 1.11 倍；FY2023 淨利 3.34 億遠高於營業利益約 0.91 億（營收 4.61 億×19.8%），屬非營業或稅務項目，該年轉換率不具代表性（事實表 financial_history，yfinance 年度財報）。Q3 FCF 0.913 億、占營收 41.8%。SBC 單季 1,710 萬、占營收 7.8%、占 GAAP 營業利益 20.5%。現金去向：Q3 營業現金流 1.025 億，回購 1.35 億（含 1 億 ASR），存貨增加 1,200 萬，期末現金及有價證券 7.77 億、淨現金約 7.57 億；公司目標把 FCF 的 40–50% 回饋股東；近一年 8-K 無併購。計分：併購項目不適用；回購買在遠期本益比約三十倍上下，盈餘殖利率約 3～4%，達不到公債殖利率加 2 個百分點；SBC 淨稀釋方面，Q3 稀釋股數約 1.092 億（非 GAAP 淨利 9,170 萬÷EPS 0.84），Q4 指引 1.09 億，回購大致抵銷稀釋，通過。","fact_refs":["f_kpi4_free_cash_flow","f_kpi5_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_kpi3_gaap_operating_income_ma"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近一年 8-K 無併購；ChipAgents 為小額策略投資；歷史併購 ROIIC 事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購均價事實表未涵蓋；以判斷日遠期本益比 27.6 倍換算盈餘殖利率約 3.6%，Q3 回購時價位更高、殖利率更低；門檻要 10 年期殖利率低於約 1.6% 才過（10 年期殖利率事實表未涵蓋），判不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 年化約 6,800 萬（單季 1,710 萬×4），約市值 0.7%；稀釋股數 Q3 約 1.092 億、Q4 指引 1.09 億，淨稀釋接近零"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；回饋以回購為主，Q3 回購 1.35 億（含 1 億 ASR），公司目標回饋 FCF 的 40–50%，期末淨現金約 7.57 億、總債務約 0.2 億"}}}},"q5_valuation":{"verdict":"現價要求 2027–2028 年 EPS 每年增約兩成、倍數不再大幅下修；我大致相信 2027 年，對 2028 年存疑，估值合理但不給便宜結論","reasoning":"現價 85.71 對 FY2026E 共識 EPS 3.11 為 27.6 倍、對 FY2027E 3.88 為 22.1 倍；三年非 GAAP EPS 年化約 24.9%，PEG 約 1.11（27.56÷24.9），落在合理帶。Trailing P/E 35.4 倍、P/S 11.5 倍、EV/S 10.6 倍，在少數年度端點中的分位分別 55、41、30，這不是五年分位，五年高低點事實表未涵蓋，五年分位留空。淨現金 7.57 億約占市值 8%，EV 對 FY2026E 營收 10.1 倍。短期上檔：FY2027E 3.88×25 倍＝97 美元，約 +13%；中期上檔：Base 第三年 EPS 5.10×23 倍＝117 美元，約 +37%。賣方平均目標價約 137～145 美元（2026-04 至 07 快照，Q3 前；區間 90～172，最高最低比 1.9 倍），明顯高於本次判斷；本次比共識保守，理由是共識 2028 年 EPS 年增約 26% 沒有反映記憶體循環轉向。分母為非 GAAP，排除 SBC 與攤銷，Q4 GAAP EPS 指引 0.68–0.76 約比非 GAAP 低 18%，不改變結論方向。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_net_debt_m","f_ev_m"],"verdict_values":{"valuation":{"basis":"遠期本益比（FY2026E 非 GAAP 共識 EPS）搭配 PEG，FY2027E 本益比作對照","peers":{"expanded":false,"reason":"事實表同業表只有利潤率，沒有同業倍數，無法做同級距倍數錨，改用自身歷史年度端點與遠期本益比"},"fwd_pe":27.56,"peg":1.11,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2026E 本益比 27.6 倍、FY2027E 22.1 倍，PEG 約 1.1（合理帶 1～2）；年度端點分位 P/E 55、P/S 41、EV/S 30，偏中低；淨現金約占市值 8%。合理偏便宜，但 EPS 處於循環高段，不給便宜結論","upside_short_pct":13.2,"upside_mid_pct":36.9,"denominator_disputed":false,"denominator_note":"分母為非 GAAP EPS，排除 SBC 與攤銷；GAAP EPS 約低 18%，屬既有口徑差異，不是本次爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯在三處：把 2027 年提早下單當成真需求而忽略 2028 年記憶體循環轉向、Montage 在新一代平台拿走份額、DOJ 刑事反壟斷調查以起訴收場","reasoning":"三種看錯方式的證據與裁定寫在反證紀錄。陷阱判斷中等：衰退信號亮兩個（EPS 成長快於營收逾 5 個百分點、核心份額方向有第三方反證），FCF 轉換與資本支出負擔都健康；SBC 占營收 7.8% 超過 5%，但逐年趨勢事實表未涵蓋。動能：26 週跌 23.1%，RSI 39.7 未到超賣；週線收盤 84.1 低於 52 週均線 105.4、略低於 104 週均線 85.8，仍高於 250 週均線 62.4 且其 13 週斜率 +1.5%，中期趨勢未修復、長期多頭結構未破。歷史最大回撤與空方最強數字事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_kpi6_non_gaap_product_gross_m","f_kpi5_sbc_gaap"],"verdict_values":{"trap":{"verdict":"🟡","label":"營業槓桿讓 EPS 跑贏營收，份額方向有爭議，循環高段盈餘需打折"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.11,"pe":27.56,"basis":"FY2026E 非 GAAP 共識 EPS（Koyfin 2026-10-31）；終端倍數同樣套在終端年當年度非 GAAP EPS，口徑一致"},"valuation_basis":"eps_pe","eps":{"bull":[4.05,5.05,6.05,7.05,8.1],"base":[3.8,4.5,5.1,5.7,6.3],"bear":[3.4,3.0,3.1,3.4,3.7]},"pe":{"bull":28,"base":23,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.8},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-50,"hi":-35,"basis":"較淺端 −35% 取 Bear 終點（15 倍×3.70＝55.5 美元，較現價約 −35%）；較深端 −50% 取路徑風險：自 2026-06-20 判斷日 141.17 跌到 85.71 已回撤約 39%（約四個半月），2026-02-03 曾單日跌 13.42%；若記憶體循環轉向疊加 DOJ 起訴，股價可能在 EPS 落底前先跌到約 14 倍 FY2026E 盈餘（約 43 美元）。歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"伺服器記憶體缺貨延續到 2028，第六代 RCD 與 MRDIMM 份額守住並擴大，新產品占比提升；2027 年 EPS 超共識約 4%，五年年化約 21%；終端 28 倍接近現值遠期本益比 27.6 倍（同業倍數事實表未涵蓋）","base":"2027 年略低於共識（3.80 對 3.88），2028 年記憶體供需轉平使成長放慢（4.50 對共識 4.89），之後回到伺服器出貨加含量的中雙位數成長，五年年化約 15%；終端 23 倍低於現值，倍數不貢獻報酬","bear":"2027 下半年記憶體循環轉向，加上第六代平台份額失守，2028 年 EPS 跌到約 3.00 後緩慢回升，五年終點 3.70 仍低於 FY2027E 共識 3.88；終端 15 倍反映成長熄火到個位數與 DOJ 陰影"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"客戶比過去提早下單、下游庫存看不清（2026-10-26 CEO：很難判斷）；TrendForce 預期 NAND 在 2027 下半年供給成長超過需求；日本分析認為記憶體成長多來自漲價、2027 年可能停滯；Montage 已拿第一代 MRDIMM；最大客戶占營收 23%","assumption":"本論點假設 2027 年訂單是真實需求，且新一代平台份額守得住","consequence":"2028 年產品營收年減兩成以上、毛利跌破 60%，EPS 退回約 3 美元，市場給 15 倍，股價約 45 美元，五年後較現價虧近半","ruling":"部分採納：Bear 機率給 30%，Base 的 2028 年 EPS 低於共識約 8%；與唯一致命點部分重疊（份額失守是這個故事的放大器），唯一致命點保留份額事件，循環轉向另列減碼條件","watch":"產品營收年增率（季）、Q1 指引是否守住正常季節性、RCD 份額年度揭露","evidence_refs":["supply_demand_durability#1","end_markets#5","competitive_share_entrants#3","customer_concentration_credit#3","customer_concentration_credit#0"],"fact_refs":["f_kpi1_product_revenue","f_kpi7_guidance_q4_2026_revenue"]},{"view":"論點成功但股東經濟變差","evidence":"產品線毛利約 60%，遠低於權利金的近乎全毛利，產品占比往上走會稀釋混合毛利；上游投入成本上升而標準品不能漲價；SBC 占營收 7.8%；回購買在高本益比；DOJ 調查若以罰款加民事求償收場會吃掉現金；Pomerantz 律所已在調查證券詐欺","assumption":"營收成長能等比例轉成每股 FCF","consequence":"營收年增兩成，但每股 FCF 只增個位數，FCF 利潤率由 39% 掉到 30% 出頭","ruling":"部分採納：混合毛利下滑是產品成長的代價，營業費用持平帶來的營業槓桿可以抵銷大半；FCF 利潤率 35% 設為第三個假設的門檻，罰款風險用清倉條件處理","watch":"TTM FCF 利潤率、非 GAAP 產品毛利率、稀釋股數、DOJ 法律程序揭露","evidence_refs":["regulatory_antitrust#0","lawsuit_class_action#0","major_events#0"],"fact_refs":["f_kpi6_non_gaap_product_gross_m","f_kpi5_sbc_gaap","f_peer_rmbs_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"FY2027、FY2028 共識 EPS 年增約 25%、26%，已把循環高段的成長寫進去；2026 年 EPS 成長（約 24%）快於營收（約 18%），倍數套在高峰盈餘上並不便宜；Q1 2026 指引不如預期就讓股價重設，對指引高度敏感","assumption":"FY2027E 22 倍本益比是便宜","consequence":"若 2028 年 EPS 持平，現價等於 22 倍持平盈餘，倍數壓到 18 倍就再跌約兩成","ruling":"反駁為主：自 6 月判斷日已跌約 39%，同期 FY1 共識近三個月上修 2.6%；淨現金約占市值 8%；Base 情境倍數由 27.6 倍降到 23 倍仍有約一成年化報酬，報酬不靠倍數擴張。但不給便宜結論","watch":"以未來一年共識 EPS 計算的本益比、共識月度修正方向","evidence_refs":["capital_markets_pricing#3","end_markets#5"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_net_debt_m"]},{"view":"論點失敗","evidence":"10-K 載明部分代工與材料為唯一來源，位在台海緊張與出口管制影響區；美國對中國半導體出口管制若擴及主力產品會受衝擊；各國關稅可能壓低客戶需求；2025 年美國以外總部客戶占營收 82%","assumption":"供應鏈與出口環境維持現狀","consequence":"單一夥伴中斷可讓產品出貨斷一到兩季；管制擴及記憶體介面晶片則失去部分客戶","ruling":"不進 Base，併入 Bear 機率；屬無法預測的政策事件，不寫預測，只設損益層吸收失敗條件：產品營收單季季減超過 20% 且公司歸因供應或管制","watch":"10-K／10-Q 風險因素變動、產品營收季減幅度、非 GAAP 產品毛利率","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":["f_kpi1_product_revenue"]},{"view":"論點失敗","evidence":"10-K 載明部分潛在客戶在評估或開發主張不需向 Rambus 授權的技術；替代技術若以相近成本提供相當效能，客戶可能改採；專利執行可能需要訴訟、結果不確定","assumption":"權利金段每季約 0.7～0.8 億美元可長期維持","consequence":"權利金近乎全毛利，每少 1,000 萬美元季營收約少 0.08 美元季 EPS","ruling":"反駁為主：2026-07-27 CEO 稱記憶體廠都要簽授權，Q3 權利金 0.770 億高於去年同期 0.651 億；屬十年尺度風險，以權利金年營收連 2 年下滑為警戒","watch":"權利金季營收、授權合約到期與續約揭露、專利訴訟","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1"],"fact_refs":["f_kpi0_revenue_gaap"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 141.17 → 本次 85.71（-39.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=141.17","side_b":"本次 price_at_dd=85.71","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 141.17 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 141.17 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 141.17 美元：Bull 價 226.8、Bear 價 55.5，五年期望值 −1.9%，基準年化 0.5%，不對稱比 0.83","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.83。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 141.17 美元：五年期望值 −1.9%，基準年化 0.5%，不對稱比 0.83","side_b":"本次情境、股價 85.71 美元：五年期望值 +61.7%，基準年化 11.1%，不對稱比 3.89","ruling":"再換股價、情境不動：起點價下跌 39.3%，五年期望值多 63.5 個百分點，基準年化多 10.5 個百分點，不對稱比由 0.83 升到 3.89。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"RCD 份額方向","cause":null,"prior_field":null,"side_a":"管理層：2025 年底 DDR5 RCD 份額約 mid-40%，高於前一年 early 40s，預期續升；Q4 產品營收指引中點年增 34%","side_b":"第三方：Q1 2026 產品營收年增約 15% 低於市場，Montage、Renesas 搶份額；第一代 MRDIMM 由對手先拿設計案（2026-10-26 法說問答）","ruling":"可調和，屬程度差異：Q1 有一次性製造問題（2026-07-27 CEO），Q3、Q4 加速；但 MRDIMM 第一代落後是事實。護城河方向只給持平，不給擴大","evidence_level":"管理層自述對單一第三方報導，雙方都缺獨立份額數據","settle_metric":"2027-02 Q4 法說的 RCD 份額揭露；2027 全年產品營收年增是否≥20%","if_then":["若 Q4 法說重申份額不低於 mid-40% 且 Q4 產品營收≥1.27 億 → 加第二批到目標倉位三分之二","若份額揭露低於 40% 或揭露失去任一 DRAM 廠第六代主供應 → 清倉","反向：若管理層不再給份額數字且產品年增跌破 15% → 減碼一半"],"evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#2","end_markets#2"]},{"axis":"2027～2028 年需求：延續還是拉貨","cause":null,"prior_field":null,"side_a":"管理層稱 2027 需求轉強、訂單能見度變好；Gartner 預期缺貨延續到 2027；JPMorgan 稱 2028 年初前無顯著新產能，BofA 預期 2028 仍偏緊","side_b":"TrendForce 預期 NAND 在 2027 下半年供給成長超過需求；日本分析認為記憶體成長多來自漲價；客戶降低單模組容量；客戶提早下單而下游庫存看不清（2026-10-26 CEO）","ruling":"2027 年可調和、2028 年方向相反屬不可調和：2027 年採信 A（有訂單能見度支撐，Base 只比共識低 2%）；2028 年採信 B，依據是 NAND 供給轉折預測與提早下單訊號，反映在 Bear 機率 30% 與 Base 2028 年 EPS 低於共識約 8%","evidence_level":"產業預測對產業預測，加上公司訂單訊號","settle_metric":"2027 年各季產品營收年增率與 Q1、Q2 指引；DRAM 廠資本支出與庫存","if_then":["若 2027 上半年產品營收年增仍≥20% 且管理層維持全年轉強說法 → 維持倉位，2028 年假設上修至共識","若產品營收連 2 季年減 → 減碼一半","反向：若價格先跌而產品營收與份額都未惡化 → 分批反買"],"evidence_refs":["supply_demand_durability#1","end_markets#5","substitute_technology#2","supply_demand_durability#0","supply_demand_durability#2"]},{"axis":"DOJ 反壟斷刑事調查","cause":null,"prior_field":null,"side_a":"公司自 2026 Q1 回應聯邦大陪審團傳票，可能結果含罰款、改變營運做法或禁制令；媒體報導公司為調查對象；Pomerantz 律所以 2026-02-03 單日跌 13.42% 為由調查證券詐欺","side_b":"迄今未見起訴、和解或時程，也未見 FTC、歐盟行動；集體訴訟尚未提起；淨現金約 7.57 億可吸收一般罰款","ruling":"不可裁決至調查出現程序性進展：調查範圍與受影響營收公司未揭露，決勝數據今天不存在，不得稱風險已解；先用分批與清倉條件處理，不計入 Base","evidence_level":"公司 10-Q 一手揭露，影響金額缺口","settle_metric":"10-Q／8-K 法律程序段落：起訴、認罪協議、和解金額或結案","if_then":["若公司或高管遭刑事起訴或簽認罪協議 → 清倉","若以罰款結案、無營運限制且金額低於淨現金一成 → 移除風險折價，允許補滿倉位","反向：若揭露調查涉及權利金或產品定價做法 → 停止加碼並重估權利金段"],"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","major_events#0","lawsuit_class_action#0","regulatory_antitrust#2"]},{"axis":"產品毛利率守不守得住","cause":null,"prior_field":null,"side_a":"CFO：近期毛利 60–63%、長期 60–65%，Q4 可能小升，2026 全年落在區間中段（2026-10-26）","side_b":"Q3 為 60.4% 落在下緣，上游投入成本上升、標準品不能漲價（2026-07-27 CEO）；2026-07-27 法說被問到拉份額是否壓毛利時未正面回答；10-K 提示關稅與唯一來源供應風險","ruling":"可調和，屬程度差異：管理層用內部降本抵銷成本上升，但上游缺貨延續到 2027 時下緣能否守住未證；設連 2 季低於 60% 為減碼條件","evidence_level":"管理層指引對最新一季實績","settle_metric":"Q4 2026 與 2027 各季非 GAAP 產品毛利率","if_then":["若連 2 季低於 60% → 停止加碼並減碼三分之一","反向：若回到 62% 以上且份額不降 → 解除毛利疑慮"],"evidence_refs":["geo_supply_chain#1","reg_tariff_export#1"]},{"axis":"揭露透明度與財務長更替","cause":null,"prior_field":null,"side_a":"新任財務長 2026-07-27 首次主持法說，同場宣布只以 ASC 606 營收口徑給指引、不再揭露授權帳單","side_b":"此後兩季營收都超過指引上緣，逐季指引與回饋 FCF 四到五成的政策延續","ruling":"可調和：未見財務品質問題，但權利金段少了一個領先指標；改用權利金季營收與合約續約揭露監測","evidence_level":"法說逐字稿","settle_metric":"權利金季營收與 10-Q 合約到期揭露","if_then":["若權利金季營收連 2 季低於公司指引下緣 → 停止加碼","反向：若權利金維持指引內 → 不調整"],"evidence_refs":[]},{"axis":"現在進場與否的最強論證對打","cause":null,"prior_field":null,"side_a":"現在就買：FY2027 共識本益比約 22 倍、三年 EPS 年化約 25%、淨現金約占市值 8%、Q2 與 Q3 連續超指引；自 6 月判斷日以來股價跌 39%，同期 FY1 共識上修 2.6%","side_b":"現在就賣：EPS 成長靠營業槓桿與循環高峰，提早下單可能是拉貨，Montage 已在 MRDIMM 先發，DOJ 刑事調查以公司為對象；週線跌破 52 週與 104 週均線，趨勢未修復","ruling":"以 A 為主但分批：基本面與估值站在買方，份額與 DOJ 兩個二元事件未解；首批只建目標倉位三分之一，第二批綁 Q4 財報驗證，DOJ 結案前不補滿","evidence_level":"財報實績與共識對照，兩個二元事件缺決勝數據","settle_metric":"2027-02 Q4 財報與份額揭露；DOJ 程序進展","if_then":["若 Q4 財報驗證通過 → 加到三分之二","若任一清倉條件觸發 → 清倉","反向：若價格再跌 15% 而所有減碼條件都沒觸發 → 分批反買一批"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"估值結論漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份估值結論 🟠（判斷日股價 141.17）","side_b":"本次 🟡（股價 85.71，FY2026E 本益比 27.6 倍、FY2027E 約 22.1 倍）","ruling":"估值改善主因是股價下跌約 39%；以 2026-07-30 快照 FY1 共識 3.03 粗算，前份價位約 46.6 倍，現為 27.6 倍，同期 FY1 共識上修 2.6%，屬價格驅動","evidence_level":"事實表股價與共識快照","settle_metric":"以未來一年共識 EPS 計算的本益比","if_then":[],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"陷阱判斷漂移","cause":"新證據","prior_field":["trap"],"side_a":"前份陷阱判斷 🟢","side_b":"本次 🟡：EPS 成長快於營收逾 5 個百分點（2026 年 EPS 約 +24%、營收約 +18%）；份額方向有第三方反證；MRDIMM 放量比預期平緩、客戶降低單模組容量（2026-10-26 法說）；產品毛利落在區間下緣","ruling":"新證據多數出現在前份之後的兩次法說，降一級合理","evidence_level":"法說逐字稿與第三方報導","settle_metric":"衰退信號亮燈數","if_then":[],"evidence_refs":["substitute_technology#2","competitive_share_entrants#3"]},{"axis":"總評維持","cause":"新證據","prior_field":["signal"],"side_a":"前份總評 B","side_b":"本次維持 B：估值由偏貴轉合理、Q3 與 Q4 營運加速，被份額爭議、產品毛利下緣與 DOJ 刑事調查抵銷","ruling":"正負新證據相抵，總評不變","evidence_level":"財報與法說","settle_metric":"Q4 財報、份額揭露、DOJ 進展","if_then":[],"evidence_refs":["regulatory_antitrust#0"]},{"axis":"新增欄位首次填寫","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未填（舊格式沒有這些欄位）","side_b":"本次：護城河方向 →、五年後成長空間 🟡、公司類型品質複利成長（次類循環/商品）、循環位置晚循環、情境機率 25／45／30、最大回撤 −35%～−50%；裁決與角色由程式依矩陣產生","ruling":"格式改版後首次填寫，沒有可比的前值","evidence_level":"方法變動","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重啟條件首次設定","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重啟條件未填","side_b":"本次：Q4 2026 財報（2027-02）產品營收≥1.27 億美元且管理層重申 DDR5 RCD 份額不低於 mid-40%","ruling":"約束改為事件錨：未解的是份額方向，不是價格；舊份沒有可比門檻","evidence_level":"方法變動","settle_metric":"2027-02 Q4 財報","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點變動","cause":"方法變動","prior_field":null,"side_a":"前份無唯一致命點（Single Thing 未填）","side_b":"本次 Single Thing：下一代平台（第六代 9600 RCD、第二代 MRDIMM）認證中失去任一 DRAM 廠主供應地位、RCD 份額跌破 40%，觸發即清倉","ruling":"產品營收占五成且是唯一高成長線，份額是數學上最大的單一敏感度項，因此設為唯一致命點","evidence_level":"方法變動，依據份額爭議新證據","settle_metric":"每年 2 月法說份額揭露","if_then":[],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"清倉與減碼指標首次設定","cause":"方法變動","prior_field":null,"side_a":"前份無清倉、減碼指標（未填）","side_b":"本次：RCD 份額低於 40% → 清倉；DOJ 起訴公司或高管 → 清倉；產品營收連 2 季年減 → 減碼一半；非 GAAP 產品毛利率連 2 季低於 60% → 減碼三分之一","ruling":"舊份只有論點層門檻，本次補上動作層門檻","evidence_level":"方法變動","settle_metric":null,"if_then":[],"evidence_refs":["regulatory_antitrust#0","supply_demand_durability#1"]},{"axis":"假設與風險門檻改寫","cause":"方法變動","prior_field":["H","R"],"side_a":"前份：H1 產品年成長≥15%、份額≥40%；H2 介面晶片市場由 8 億擴至 20 億美元以上；H3 遠期本益比維持 25 倍以上，跌破 22 倍且共識下修即反轉；R2 產品連 2 季季減","side_b":"本次：H1 2027 年產品年增≥20%、份額≥40%；H2 新產品占產品營收 2028 年≥25%、產品五年年化≥15%；H3 改為 FCF 利潤率≥35%、矽智財年增≥10%；R2 改為產品營收連 2 季年減","ruling":"H1 門檻上調，因 2026 年產品年增已約 24%（2026-10-26 CFO）；H2 改用公司實際揭露的指標（MRDIMM 市場約 6 億、新產品占比）；H3 的估值溢價假設移進情境樹，不再當論點，前份反轉線未觸發（FY1 遠期本益比 27.6 倍、共識上修）；R2 改年減，因上下半年季節性（2026-10-26 CEO）會讓 Q1 季減成為假訊號；前份 R3 架構替代保留為 R6","evidence_level":"方法變動加法說新數據","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q4 2026 產品營收落在指引內並重申份額","type":"假設驗證","maps_to":"H1","metric":"Q4 2026 產品營收；DDR5 RCD 份額自述","threshold":"產品營收≥1.27 億美元且份額不低於 mid-40%","action":"通過則加第二批到目標倉位三分之二","source_freq":"季報 8-K 與法說","date":"2027-02","evidence_refs":["competitive_share_entrants#3"]},{"n":2,"text":"下一代平台認證失守","type":"Single Thing","maps_to":"Single Thing","metric":"DDR5 RCD 份額；三大 DRAM 廠第六代 RCD 主供應地位","threshold":"份額低於 40%，或揭露失去任一 DRAM 廠第六代主供應","action":"清倉","source_freq":"年度（Q4 法說）與設計案公告","date":"2027-02","evidence_refs":["competitive_share_entrants#3","customer_concentration_credit#3"]},{"n":3,"text":"記憶體循環轉向","type":"減碼","maps_to":"R2","metric":"產品營收年增率（季）","threshold":"連 2 季年減","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#1","end_markets#5"]},{"n":4,"text":"DOJ 刑事起訴","type":"清倉","maps_to":"R4","metric":"DOJ 反壟斷調查程序","threshold":"公司或高管遭起訴或簽認罪協議","action":"清倉","source_freq":"10-Q／8-K 法律程序揭露","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2"]},{"n":5,"text":"產品毛利率跌破區間下緣","type":"減碼","maps_to":"R3","metric":"非 GAAP 產品毛利率","threshold":"連 2 季低於 60%","action":"停止加碼並減碼三分之一","source_freq":"季報與法說","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":6,"text":"價格先跌、基本面無損","type":"加碼","maps_to":"H1","metric":"股價對照所有減碼與清倉條件","threshold":"股價約 73 美元以下（較判斷日再跌 15%）且減碼、清倉條件都未觸發","action":"分批反買一批","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":7,"text":"估值過高不追","type":"估值rearm","maps_to":"H2","metric":"以未來一年共識 EPS 計算的本益比","threshold":"≥35 倍停止加碼；≥40 倍減碼三分之一","action":"不追，停止加碼","source_freq":"月度共識快照","date":null,"evidence_refs":[]},{"n":8,"text":"份額訊號轉弱","type":"風險","maps_to":"R1","metric":"產品營收年增率與管理層份額說法","threshold":"管理層停止給份額數字且產品年增低於 15%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":9,"text":"現金流與矽智財驗證","type":"假設驗證","maps_to":"H3","metric":"TTM FCF 利潤率；矽智財年增率","threshold":"FCF 利潤率≥35%；矽智財年增≥10%","action":"未達則停止加碼","source_freq":"季報","date":null,"evidence_refs":[]},{"n":10,"text":"Q4 財報後全份複審","type":"複審日期","maps_to":null,"metric":"全份重跑","threshold":"2027-02 財報公告後一週內","action":"重跑判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"DDR5 RCD 份額（管理層年度揭露）","bear_threshold":"低於 40%，或失去任一 DRAM 廠第六代主供應","window":"2027-02 起每年 Q4 法說","source":"公司法說逐字稿、設計案公告","last_status":"warning"},{"metric":"產品營收年增率（季）","bear_threshold":"連 2 季年減","window":"2027-Q1 至 2028-Q4","source":"公司 8-K 新聞稿","last_status":"ok"},{"metric":"非 GAAP 產品毛利率","bear_threshold":"連 2 季低於 60%","window":"逐季","source":"公司法說與 8-K","last_status":"warning"},{"metric":"DOJ 反壟斷刑事調查","bear_threshold":"公司或高管遭起訴或簽認罪協議","window":"至結案","source":"10-Q／8-K 法律程序揭露","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"Q4 2026 財報（2027-02）產品營收≥1.27 億美元且管理層重申 DDR5 RCD 份額不低於 mid-40%","exec_line":"首批建倉為目標倉位三分之一；Q4 財報驗證通過加到三分之二；DOJ 以無營運限制結案後才補滿；任何清倉條件觸發即出場"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 RMBS 當記憶體價格循環股折價，但產品營收看伺服器模組顆數與每模組晶片數，不看 DRAM 價格；客戶降規格降的是單模組容量不是模組數，Q4 產品指引年增 34%，FY1 共識近三個月上修","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 RMBS 當記憶體價格循環股折價，但產品營收看伺服器模組顆數與每模組晶片數，不看 DRAM 價格；客戶降規格降的是單模組容量不是模組數，Q4 產品指引年增 34%，FY1 共識近三個月上修"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-23.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"RMBS 守住 DDR5 RCD 共同領先地位，第六代 9600 世代轉換與周邊晶片帶動產品營收 2027 年續增兩成以上","2y":"2027 年產品營收年增≥20%、份額≥40%、產品毛利≥60%","5y":null,"10y":null,"threshold":"2027 全年產品營收年增≥20%；管理層揭露 DDR5 RCD 份額≥40%；非 GAAP 產品毛利率≥60%","source":"公司季度 8-K 產品營收；每年 2 月 Q4 法說份額自述","drift_rule":"TTM 產品營收較 20% 成長路徑落後 5% 以上連 2 季為削弱；落後 10% 以上連 3 季為反轉"},{"id":"H2","text":"伺服器記憶體子系統每台晶片含量提高（通道數 8 增至 12–16、MRDIMM、LPDDR／SOCAMM2 電源管理），新產品成為產品線第二成長引擎","2y":null,"5y":"2031 年前新產品占產品營收≥30%，產品營收 2026–2031 年化≥15%","10y":null,"threshold":"新產品（周邊晶片、MRDIMM、SOCAMM）占產品營收 2028 年≥25%、2031 年≥30%；產品營收五年年化≥15%","source":"公司法說新產品占比自述（2026-07-27 CEO：年底達中雙位數）；8-K 產品營收","drift_rule":"TTM 產品營收較 15% 年化路徑落後 5% 以上連 4 季為削弱；落後 10% 以上連 6 季為反轉；公司停止揭露新產品占比即列資料缺口，下次複審降為削弱"},{"id":"H3","text":"權利金與矽智財提供穩定高毛利現金流，支撐 FCF 利潤率與股東回饋","2y":null,"5y":"FCF 利潤率維持≥35%，矽智財年增≥10%，每年回饋 FCF 的 40–50%","10y":null,"threshold":"TTM FCF 利潤率≥35%；矽智財業務年增≥10%；權利金年營收不低於 2025 年水準","source":"8-K 現金流量表與營收分項；CFO 矽智財規模自述（約 1.3 億、年增 10–15%）","drift_rule":"TTM FCF 利潤率低於 35% 門檻達 5% 以上（約 33.3% 以下）連 4 季為削弱；低於 31.5% 連 6 季為反轉"}],"R":[{"id":"R1","text":"Montage、Renesas 在第六代 RCD 與 MRDIMM 搶下份額","h_ref":"H1","clock":"🔥","threshold":"管理層揭露 RCD 份額低於 40%，或產品營收年增連 2 季低於伺服器出貨成長","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#0"]},{"id":"R2","text":"記憶體循環轉向：提早下單變成拉貨，2027 下半年起供給追上需求，客戶降規格壓低模組容量","h_ref":"H1","clock":"⚡","threshold":"產品營收連 2 季年減，或季度指引中點年增轉負","evidence_refs":["supply_demand_durability#1","end_markets#5","substitute_technology#2"]},{"id":"R3","text":"上游投入成本上升而標準品不能漲價，產品毛利率跌破 60%","h_ref":"H1","clock":"🔥","threshold":"非 GAAP 產品毛利率連 2 季低於 60%","evidence_refs":["geo_supply_chain#1","reg_tariff_export#1"]},{"id":"R4","text":"DOJ 反壟斷刑事調查以起訴或營運限制收場，並引發民事求償與證券訴訟","h_ref":"H3","clock":"⚡","threshold":"公司或高管遭起訴、簽認罪協議，或揭露罰款超過淨現金一成（約 7,600 萬美元）","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","major_events#0","lawsuit_class_action#0"]},{"id":"R5","text":"客戶集中：前五大占營收約三分之二、最大客戶 23%，任一 DRAM 廠轉單、自製或改採不需授權的技術","h_ref":"H1","clock":"🔥","threshold":"年度揭露前五大占比超過 70% 且營收年減，或最大客戶占比單年下降 5 個百分點以上","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","competitive_share_entrants#1"]},{"id":"R6","text":"替代技術或架構（板載 LPDDR、免權利金方案）壓縮獨立介面晶片與權利金價值，專利執行需訴訟","h_ref":"H2","clock":"🐢","threshold":"主要 CPU 平台或 DRAM 廠推出不需 RCD 的主流伺服器記憶體方案，或權利金年營收連 2 年下滑；機率達 50% 以上才砍倉","evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"id":"R7","text":"地緣與出口管制：唯一來源代工在台海風險區，82% 營收來自美國以外總部客戶","h_ref":"H1","clock":"🐢","threshold":"出口管制擴及記憶體介面晶片，或產品營收單季季減超過 20% 且公司歸因供應或管制","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#1"]}],"single_thing":{"description":"下一代伺服器平台（DDR5 第六代 9600 RCD 與第二代 MRDIMM）認證中，Rambus 在三大 DRAM 廠之一失去主供應地位，RCD 份額跌破 40%","why_fatal":"產品營收占五成且是唯一高成長線；以 Q4 指引產品營收年化約 5.2 億、RCD 占大宗（假設約八成）粗估，份額每掉 10 個百分點約少 9,000 萬美元營收、約 0.4 美元 EPS（產品毛利 60%、稅率 16%、1.09 億股）；世代認證失守要等下一代約兩年才有機會翻盤","if_happens":"清倉；情境改用 Bear 路徑（終端 EPS 3.70、15 倍）重估","how_monitor":"每年 2 月 Q4 法說的份額自述、產品營收年增率對照伺服器出貨、第六代 RCD 與 MRDIMM 設計案公告、第三方份額報導","probability":"12～24 個月約 20%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.09,"peg_fy2":0.89,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.51,"FY2026E":3.11,"FY2027E":3.88,"FY2028E":4.89},"fy_end_month":12,"eps_basis":"非 GAAP 稀釋 EPS（Koyfin 共識 2026-10-31）；FY2025A 非 GAAP 實際值事實表未直接涵蓋，以 CFO 稱 2026 年非 GAAP EPS 約年增 24%（2026-10-26）與 FY2026E 共識 3.11 回推約 2.51，只作基期；FY2025 GAAP 稀釋 EPS 為 2.11"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報、2027 Q1 指引與 DDR5 RCD 份額揭露","impact":"高","watch":"產品營收是否≥1.27 億美元、份額是否重申 mid-40%"},{"date":null,"date_precision":null,"type":"regulatory","event":"DOJ 反壟斷刑事調查進展（起訴、認罪協議、和解或結案）","impact":"高","watch":"10-Q／8-K 法律程序段落"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"新伺服器平台放量、MRDIMM 隨第二家 CPU 平台放量、第六代 RCD 量產","impact":"中","watch":"新產品占產品營收比重、MRDIMM 設計案歸屬"},{"date":"2027-09","date_precision":"quarter","type":"macro","event":"記憶體供需轉折觀察期（NAND 供給成長預期超過需求）","impact":"中","watch":"客戶下單節奏、DRAM 廠資本支出與庫存"}]}
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
