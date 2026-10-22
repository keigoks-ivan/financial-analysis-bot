你是 DD 管線 v20 的判斷層閘（gate），標的 VICR（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝197.1 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查證
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝68.3 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查證
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝72.1 百萬美元（利益率約 36.6%，由 72.148/197.114 推算）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查證
- `f_kpi5_backlog`（q1_business）｜在手訂單 backlog＝406 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：不適用
- `f_peer_vicr_operating_margin_pct`（q2_moat）｜VICR 營業利益率＝18.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VICR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mpwr_operating_margin_pct`（q2_moat）｜MPWR 營業利益率＝28.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MPWR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_vicr_gross_margin_pct`（q2_moat）｜VICR 毛利率＝56.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VICR.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mpwr_gross_margin_pct`（q2_moat）｜MPWR 毛利率＝55.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MPWR.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝4.12 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.12 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝8.31 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝642.1 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate 0y 平均（4 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝943.02 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate +1y 平均（4 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝34.2 %｜期間與口徑：2026-07-16 → 2026-10-21／FY1 共識 EPS 3.07 → 4.12（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-21）
- `f_kpi4_69_7_16_1`（q4_capital）｜自由現金流（營運現金流 69.7 − 資本支出 16.1，推算）＝53.6 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm（FCF 為自算）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：不適用
- `f_kpi3_gaap_eps`（q4_capital）｜GAAP 淨利／稀釋 EPS＝1.33 美元/股（淨利 63.3 百萬）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查證
- `f_kpi6`（q1_business）｜現金及約當現金＝513.1 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0000751978/000119312526425697/d153882dex991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-505.98 USD m｜期間與口徑：2026-10-22／yfinance 最新一季：總債務 7.16、現金 513.14（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-10-22／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-22）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝46.11 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝213.42 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝51.8 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 4.12，分子＝快照價 213.42｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝55.72 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝7.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝7.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝17.55 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝16.65 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝14.54 x｜期間與口徑：2026-10-22／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-19.46 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ma_w104`（q5_valuation）｜104 週均線＝124.38 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_ma_w250`（q5_valuation）｜250 週均線＝82.75 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：大型對手常以大幅折扣價守住份額與客戶關係，Vicor 可能無法跟進。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-03-02）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：SemiAnalysis 報導 Monolithic Power 在 Nvidia H100 GPU 供電上取代 Vicor（2023 文章）。
  - 來源：SemiAnalysis Newsletter: Energizing AI Power Delivery Competition（as_of 2023-08-01）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 載明 Advanced Products 營收相當大部分來自少數客戶；公司稱此集中反映技術採用早期，策略是先鎖定市場領先創新者。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 風險因素：公司預期銷售將集中於相對更少的客戶，少數客戶的行動可能不成比例地影響經營結果。
  - 來源：SEC EDGAR 10-K FY2025 Item 1/1A（WebFetch 讀取）（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 Section 301 關稅成本約 $7.375M（較 2024 的 $4.189M 增 76.1%），占營收約 1.8%，壓低毛利率；已申請 duty drawback，2025 回收 $907K；2025 年 7 月起加收 10% 關稅附加費。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子指出美國持續擴大實體清單，出口管制規則與中美政府行動的影響不確定，可能對業務造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Vicor 10-K FY2025 稱先進產品與部分半導體由有限數量晶圓代工廠製造，封裝與測試由少數第三方處理；並稱尚未因美中貿易爭端（含 2018 年 Section 301 關稅）出現重大延遲或原料供給減少。
  - 來源：Vicor Form 10-K FY2025 (SEC EDGAR)（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：競爭：ADI（含Empower）、MPS、TXN、Infineon 等；分析稱 Vicor 在部分 Nvidia GPU 平台輸給較低成本的整合方案而失去 socket。未找到市佔或價格趨勢的量化資料。
  - 來源：Chartmill / Easternprogress 二手分析（as_of 2026-07-01）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子載明電源系統產業競爭激烈、技術變動快、產品快速過時，成熟產品有價格侵蝕；公司策略押注差異化 Advanced Products，並稱無法保證新產品獲客戶接受。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：聚合文章稱 Vicor、MPS、Infineon 皆推垂直／封裝上供電設計；並有 ADI 傳聞以約 15 億美元收購 Empower（未證實）。
  - 來源：borecraft.com 報導（as_of 2026-05-19）｜affects：moat_trend、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2024年7月由放空者提起的證券集體訴訟（In re Vicor Securities Litigation），被告於2025年1月20日聲請駁回；10-K 附註16 載明該案。
  - 來源：SEC EDGAR 10-K FY2025 Note 16（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：放空者提起的證券集體訴訟，2025年1月聲請駁回；Foley 稱法院於2025年6月無偏見駁回。
  - 來源：SEC EDGAR 10-K FY2025 Note 16（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":528.0,"bear_5y_price":116.6,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":54.8,"ev5y_pct":47.9,"irr_base_pct":9.1,"asym_ratio":2.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":4.12,"pe":51.8,"basis":"起點用 FY1（FY2026E）共識 EPS 4.12 美元，屬前瞻口徑。終端年 FY2031E 在 2031 年 10 月時同樣是當年度，倍數分母同口徑"},"eps":{"bull":[6.6,9.2,11.8,14.3,16.5],"base":[6.0,7.8,9.3,10.6,11.8],"bear":[3.4,3.8,4.3,4.8,5.3]},"pe":{"bull":32,"base":28,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### VICR_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO｜guidance：CFO 給 Q3 營收約增 10%、2026 全年營收逾 6 億美元（原話："we expect a nearly 10% increase in Q3 revenue"）
- 2026-07-21｜CFO｜guidance：計畫 Advanced Products 產品營收連續季增雙位數（原話："we are planning for double-digit sequential increases in"）
- 2026-07-21｜CFO｜guidance：財測對授權採保守假設，新授權可能要等第二個 ITC 案 2027 年終裁（原話："this guidance is based on conservative assumptions"）
- 2026-07-21｜CFO｜guidance：新授權權利金會計認列：Q2 認列 1,500 萬，Q3 降為 500 萬，之後每季 1,000 萬（原話："contribute $5 million in Q3 and $10 million per quarter"）
- 2026-07-21｜CFO｜margin：Q2 合併毛利率 58%，季增 280 基點（原話："gross profit margin of 58%, a 280 basis point"）
- 2026-07-21｜CFO｜margin：產品毛利率受 fab 內搬移設備的一次性費用拖累，無法資本化（原話："did not get capitalized and cannot be capitalized"）
- 2026-07-21｜CFO｜margin：CFO 稱隨稼動率與吸收提高，產品毛利率將回升（原話："there will be a lift in the GM, product GM going forward"）
- 2026-07-21｜CFO｜margin：Q2 營運費用季增 6.1%，主因授權案的或有律師費大增（原話："substantial increase in contingent legal expenses"）
- 2026-07-21｜CFO｜customer：Advanced Products 營收季增 45% 至 9,420 萬美元（原話："Advanced Products revenue increased 45% sequentially"）
- 2026-07-21｜CFO｜customer：訂單出貨比大於 1，一年期在手訂單季增 26% 至 3.797 億（原話："1-year backlog increased
26% from the prior quarter"）
- 2026-07-21｜CEO｜customer：被問在手訂單增加有多少來自新授權，答相對很少（原話："Relatively little."）
- 2026-07-21｜CEO｜customer：ATE 市場來自關鍵客戶的業務量為過去的數倍，歸因於 AI 建置（原話："a large
multiple of what it has been in past years"）
- 2026-07-21｜Sales VP｜customer：銷售主管稱訂單出貨比低於先前近 2 的水準，但各終端市場強勁（原話："I don't see any weakness at all going forward."）
- 2026-07-21｜Sales VP｜commitment：新財務目標：營收 25 億美元、毛利率 70%、營業利益率 40%，取代 2023 年的 10 億／65%（原話："$2.5 billion in revenues at 70% gross margins"）
- 2026-07-21｜CEO｜capital_allocation：CEO 明言達 25 億營收必須有第二座晶圓廠（原話："It's going to take a second fab to get there."）
- 2026-07-21｜CEO｜capital_allocation：第二廠選址仍在進行，數週內可能決定（原話："we'll probably be making decisions in the next few
weeks"）
- 2026-07-21｜CEO｜capital_allocation：選址對象可支援第一廠的 2 至 3 倍規模（原話："as much as 2x, potentially 3x the first fab."）
- 2026-07-21｜CEO｜capital_allocation：第二廠分階段建置，初期約使產能加倍，避免過早折舊（原話："unnecessary or premature depreciation"）
- 2026-07-21｜CFO｜capital_allocation：Q2 現金 4.536 億美元，7/13 收到 CHIPS 法投資稅額抵減退稅 1,430 萬（原話："Cash and cash equivalents totaled $453.6 million in Q2"）
- 2026-07-21｜CEO｜risk：第一廠接近滿載，但稱尚未售罄，將挑選參與的案子（原話："We're not sold out, but we're approaching capacity"）
- 2026-07-21｜CEO｜risk：第一廠產能上限仍未定，且比一年前的目標高很多（原話："will top out is, I think, yet TBD"）
- 2026-07-21｜CEO｜risk：交期略為拉長，管理層稱與產業趨勢一致（原話："Lead times have stretched out a little bit"）
- 2026-07-21｜CEO｜product：第二代 VPD 基線 3 A/mm² 已完成開發，年底至明年初要超過 5 A/mm²（原話："raising the bar past 5 amps
per square millimeter"）
- 2026-07-21｜Sales VP｜product：本季起向選定客戶提供第二代 VPD 開發系統與工具（原話："development systems and tools starting this quarter"）
- 2026-07-21｜Sales VP｜product：預期明年第三季末至第四季進入量產爬坡（原話："late third quarter, fourth quarter of next year"）
- 2026-07-21｜CEO｜product：有兩家公司找上門，希望 Vicor 提供 IVR 部署所需的關鍵構件（原話："We've been approached by 2
companies wishing us to provide a building block"）
- 2026-07-21｜CEO｜competition：CEO 稱競爭者實際只能做到略高於 1 A/mm²（原話："slightly over 1 amp per square millimeter"）
- 2026-07-21｜CEO｜competition：CEO 稱產業依賴負載點電壓調節器的路線有根本缺陷（原話："That's fundamentally a flawed strategy."）
- 2026-07-21｜CEO｜competition：第二貨源：短期重心轉向自控的第二座晶圓廠，與替代來源討論的時程不符近兩年擴產所需（原話："a shift with respect to relative focus"）
- 2026-07-21｜CEO｜competition：授權對象涵蓋任何 OEM 與超大規模業者，不含競爭者（原話："It does not involve competitors."）
- 2026-07-21｜CEO｜customer：Q2 新授權首兩年不含採購關係，但預期與第二代 VPD 搭配納入未來關係（原話："does not, for the first couple of years, provide for a"）
- 2026-07-21｜CEO｜customer：授權對象公開揭露為多家 OEM、目前一家超大規模業者（原話："a multiplicity of OEM licensees, one hyperscaler as of now"）
- 2026-07-21｜CEO｜commitment：CEO 拒絕預測 25 億目標中授權收入占比，只稱未來數年授權收入將顯著擴大（原話："a significant expansion in licensing income in years to come"）

### VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md
- 2026-06-19｜Philip Davies｜guidance：宣布長期目標營收由10億美元提高到25億美元（原話："target revenue from $1 billion to $2.5 billion"）
- 2026-06-19｜Philip Davies｜margin：新長期目標毛利率與營業利益率（原話："gross margins from 65% to 70% and operating income of 40%"）
- 2026-06-19｜James Schmidt｜guidance：安靜期，不評論Q2及未來財務表現（原話："Vicor is in its quiet period for the second quarter of 2026"）
- 2026-06-19｜Patrizio Vinciarelli｜guidance：CEO談25億目標時程：不願推測（原話："it would be, I think, unwise for me to speculate"）
- 2026-06-19｜Patrizio Vinciarelli｜guidance：CEO稱25億可能很快達成但不給時點（原話："But I won't tell you exactly when for various reasons."）
- 2026-06-19｜Philip Davies｜margin：工業業務2027年底前倍增（原話："well on track to do that by the end of 2027"）
- 2026-06-19｜Philip Davies｜customer：工業設計導入與設計贏單數量以「數千萬」描述（原話："they're tens of millions, okay?"）
- 2026-06-19｜Philip Davies｜customer：ATE領先客戶已下大額早期訂單（原話："has placed large early orders for this chipset"）
- 2026-06-19｜Philip Davies｜product：新ATE晶片組第四季推向其他ATE公司（原話："we'll be launching that chipset out to all the other ATE"）
- 2026-06-19｜Philip Davies｜product：航太國防新增AC-DC，可觸及SAM 8.5億美元（原話："offers us a new $850 million SAM to target"）
- 2026-06-19｜Philip Davies｜competition：航太國防產品功率密度為最近競爭者5到10倍（原話："5 to 10x the nearest competitor"）
- 2026-06-19｜Philip Davies｜customer：衛星聚焦LEO/MEO，不做低成本星鏈類（原話："We're focused on LEO and MEO, where performance matters"）
- 2026-06-19｜Philip Davies｜competition：稱產品功率密度為最近競爭者3到10倍（原話："3 to 10x the power density of our nearest competitor"）
- 2026-06-19｜Philip Davies｜competition：批評NVIDIA與OCP的800V轉6V架構選擇（原話："bad power architecture choice being made by NVIDIA"）
- 2026-06-19｜Philip Davies｜risk：領先客戶時程比去年股東會所示晚約9個月（原話："we're about 9 months later than what we showed you"）
- 2026-06-19｜Philip Davies｜risk：時程延後原因為系統層訊號完整性需新增隔離式電流倍增器（原話："development of a new isolated current multiplier"）
- 2026-06-19｜Philip Davies｜product：2027年Q1電流密度提升47%（原話："a step-up of 47% in current density"）
- 2026-06-19｜Philip Davies｜commitment：領先客戶預量產與早期量產預計2027年Q4末（原話："will probably start towards the end of 4Q '27"）
- 2026-06-19｜Philip Davies｜commitment：第三季向策略客戶提供開發板（原話："development board that will be provided to our strategic cus"）
- 2026-06-19｜Patrizio Vinciarelli｜product：CEO提議以提前投入治具縮短Q1'27時程（原話："we may be able to beat the Q1 '27 time line"）
- 2026-06-19｜Patrizio Vinciarelli｜product：電流倍增比由40:1升到56:1（原話："from 40:1 to 56:1"）
- 2026-06-19｜Patrizio Vinciarelli｜competition：CEO糾正：競品方案昂貴而非真正商品化（原話："it's actually extremely expensive"）
- 2026-06-19｜Patrizio Vinciarelli｜competition：CEO糾正副總對競爭者為商品的說法（原話："he referred to the competition in AI market as commodity"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：第二貨源夥伴尚未定案（原話："on second thoughts, they may not be the best choice"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：第二貨源決策不急（原話："We shouldn't feel compelled to make an instant decision."）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：七月初與更大公司洽談（原話："I'm having some conversations at the beginning of July"）
- 2026-06-19｜Patrizio Vinciarelli｜customer：最新授權客戶約一個月前簽約，談判3到4週（原話："the license came about a month ago"）
- 2026-06-19｜Patrizio Vinciarelli｜commitment：授權結構個案不同，已有談判方法（原話："a structure, a methodology for negotiating these deals"）
- 2026-06-19｜Patrizio Vinciarelli｜customer：授權戶數：最大AI OEM兩份（原話："the largest OEM in AI, we've had 2 licenses"）
- 2026-06-19｜Patrizio Vinciarelli｜risk：ITC第二案進行中，將有更多（原話："The second one is in progress. There's going to be more."）
- 2026-06-19｜Patrizio Vinciarelli｜guidance：Q2財測上調來自產品需求與新授權（原話："The second one is in progress."）
- 2026-06-19｜Patrizio Vinciarelli｜commitment：新產線預計Q3末Q4初投產（原話："operational by the end of Q3, beginning of Q4"）
- 2026-06-19｜Patrizio Vinciarelli｜product：VPD約占今年營收15至20%（原話："In '27, it will jump to a substantially larger percentage."）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：第二廠已洽購土地與建物（原話："We made a number of offers for both plots of land"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：現有聯邦街廠產能今年底明年初到極限（原話："gets to its limits as we get to the end of this year"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：現有廠產能目標由10億擴至15億美元（原話："has been expanded to the $1.5 billion level"）
- 2026-06-19｜Patrizio Vinciarelli｜product：第二代VPD每片面板營收可約倍增（原話："raise the revenue per panel by about 2x"）
- 2026-06-19｜Patrizio Vinciarelli｜product：CS4單顆電流倍增器電流輸出近乎倍增（原話："deliver double the current or nearly double the current"）
- 2026-06-19｜Patrizio Vinciarelli｜commitment：CEO對需求與製造能力表示百分之百有信心（原話："100% confidence both with respect to the demand"）
- 2026-06-19｜Patrizio Vinciarelli｜capital_allocation：產能緊時將更挑選客戶與應用，可能不再接NBM（原話："We may not want to take on more NBM business."）
- 2026-06-19｜Patrizio Vinciarelli｜customer：新授權費率今年為明年一半（原話："the royalty rate this year is half of the royalty rate"）
- 2026-06-19｜Patrizio Vinciarelli｜guidance：授權貢獻2億至3億美元屬保守數字（原話："$200 million, $300 million contribution from licensing"）
- 2026-06-19｜Patrizio Vinciarelli｜commitment：將加快ITC行動節奏（原話："We're going to be accelerating that pace."）
- 2026-06-19｜Patrizio Vinciarelli｜customer：電動車尚無大型OEM平台突破（原話："We haven't had that breakthrough, right, with a big OEM"）
- 2026-06-19｜Patrizio Vinciarelli｜risk：電動車歐洲一家客戶明年量產（原話："going to ramp into production next year"）
- 2026-06-19｜James Schmidt｜capital_allocation：拆股議題僅早期討論（原話："it's a very, very early kind of conversation"）
- 2026-06-19｜Patrizio Vinciarelli｜customer：領先客戶明年占比可能25%至30%（原話："certainly, a significant step-up next year could be 25%, 30%"）
- 2026-06-19｜Unknown Executive｜guidance：明年航太國防加工業約占50%，其餘為高效能運算（原話："it's probably aerospace and defense, industrial, about 50%"）
- 2026-06-19｜Patrizio Vinciarelli｜risk：對太空資料中心持懷疑（原話："I'm a bit skeptical with respect to that"）

### 問答異常語氣（迴避／改口／保留）
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：第二代 VPD 設計定案是否會在 2027 下半年放量｜答法：CEO 明說不對具體日期做承諾，改談客戶興趣與競爭者能力
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：是否仍預期明年 Cerebras 占營收 25%–30%｜答法：CEO 不談客戶具體數字，僅稱關係良好，未回答該比例是否仍成立
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：Cerebras 在 Q2 是否為 10% 客戶｜答法：CEO 反問是否能說；CFO 稱留待 10-Q 揭露，並稱不確定是否達 10%
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：扣除權利金後產品毛利率比前幾季低約數百基點，趨勢是否反轉｜答法：CEO 先以「Jim 提過毛利率會增加」帶過，未給數字，CFO 補述一次性設備搬遷費用與稼動率
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：25 億目標中權利金是否占 50%｜答法：CEO 稱無法對組合做具體預測，改談授權前景
- VICR_Q2_2026_Earnings_Call_20260721.md｜問：OEM 具備第二貨源能力是否成真及進度｜答法：CEO 未直接回答是否會成為第二貨源，改稱重心轉向自控的第二座晶圓廠，並稱「不是長期策略改變」
- VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md｜問：分析師問工業設計導入/贏單的具體數字｜答法：先說有數字但不能展示，拒絕私下提供，僅說「tens of millions」
- VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md｜問：Q2財測上調1400萬美元中多少來自權利金｜答法：CFO稱屬營運問題；CEO只答兩項貢獻（產品需求與新授權），未給比例
- VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md｜問：25億美元目標是3、5或10年｜答法：稱可能很快也可能較久，不願預測時點，「won't tell you exactly when」
- VICR_Shareholder_Analyst_Call_Vicor_Corporation_20260619.md｜問：第二廠何時完成交易、何時預生產｜答法：說不能告知何時成交，只談已出價與產能壓力

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 6 | 4 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 1 |
| capital_markets_pricing | found | 5 | 3 |
| major_events | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Fab 1 ramp 至 $1.5B run-rate：管理層 4/21/26 法說明確路徑，process bottleneck 已識別 + 部分外包 + 收購鄰近建物為過渡","columns":{"2Y 驗證點":"FY27 全年 product revenue（剝離 royalty）≥ $1.2B（Q4 26 run-rate 至少 $300M/季）","5Y 驗證點":"FY30 product revenue $2.5-3.0B（Fab 1 滿載 + Fab 2 ramp 50%）","10Y 驗證點":"10Y 維持 $3B+ 與第二代 VPD 架構替代風險之間取得平衡","具體數字門檻":"FY27 product rev ≥ $1.2B；Q4 26 季 run-rate ≥ $300M","信息來源":"4/21/26 Q1 26 法說、4/22/26 transcript","漂移觸發條件":"連 2 季 product rev YoY &lt; 15% → 削弱；連 3 季 &lt; 10% → 反轉（QC-34 採 TTM 過濾）"}},{"id":"H2","text":"IP licensing 進入結構化年收入 $80-120M run-rate：ITC LEO 強制執行後 hyperscaler 排隊上桌；管理層公開預期 2025-26 settlement contribution ~$300M","columns":{"2Y 驗證點":"FY27 royalty revenue ≥ $80M（FY25 $57.4M 基期）","5Y 驗證點":"FY30 royalty $100-150M（加上對 Delta / Foxconn 二輪訴訟成功）","10Y 驗證點":"10Y 取決於 '761 + '481 專利 2028-2030 到期前能否成功取得下一代 VPD 專利布局","具體數字門檻":"FY27 royalty ≥ $80M；單一 hyperscaler license 公告金額 ≥ $50M","信息來源":"2025/10/20 IP licensing practice press release；2025 IP rev growth +23.2%","漂移觸發條件":"連 4 季 royalty &lt; $15M（即年化 $60M）→ 削弱；單一大客戶 license 終止 → 反轉"}},{"id":"H3","text":"Trailing PE 從 89x 收斂至「FY27 ramp 兌現後」40-50x 區間：EPS 兌現 + 共識 catch-up，市場逐步認可 sustainable 25-30% CAGR 而非 2026 一次性 inflection","columns":{"2Y 驗證點":"FY27 末 trailing PE ~40-45x（股價未來 24 個月可維持平穩 / 緩漲，等 EPS 補上來）","5Y 驗證點":"FY30 trailing PE 25-30x（成長放緩至 15-20% CAGR 對應）","10Y 驗證點":"10Y PE 跟同等 quality 工業 / 半導體公司收斂至 20-25x（如 ADI / TXN tier）","具體數字門檻":"FY27 末 trailing PE ≤ 45x 且 ROIC &gt; 25%","信息來源":"歷史對標 MPWR 2018-2022 / ASML 2014-2018 inflection 期 PE 軌跡","漂移觸發條件":"5Y 假設，連 4 季 TTM 偏離 ≥ 5% 才削弱（QC-35：5Y 假設連 4 季）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"單一大客戶 attribution risk — Cerebras 為 lead customer，集中度極高；若 Cerebras 自身 funding round / NVDA 競爭壓力造成減單，Vicor 短期 product revenue 立即可見","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"季度 product rev QoQ 顯著下滑；管理層在法說提到「one major customer ramp delay」","警戒閾值":"單季 product rev QoQ -10%+；連 2 季觸發即減倉"}},{"id":"R2","text":"Fab 1 capacity 撞牆 + Fab 2 推遲 — process bottleneck 排除進度不如預期，或 Fab 2 建物收購談判破裂，2027 run-rate 卡在 $1B 而非 $1.5B","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"backlog QoQ 從 $300M 平 / 跌；管理層 Q4 26 / Q1 27 法說對 Fab 2 timeline 從 2028H2 改口至 2029","警戒閾值":"backlog 連 2 季 QoQ -5%+ 或單季 -15%+；book-to-bill 跌破 1.3；連 4 季觸發大動作（QC-35：5Y 假設連 4 季）"}},{"id":"R3","text":"NVDA / hyperscaler 扶持替代陣營 — Vicor royalty 索取過度 → NVDA 在 Rubin / Vera Rubin 公開支持 MPWR 或 Infineon 的 next-gen single-stage GaN 方案 → 25% 市佔 2027 目標推遲至 2030+","columns":{"對應假設":"H1, H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"NVDA 法說 / GTC 公開 power partner 名單；OCP power spec 變化；MPWR / Infineon 法說明確宣告 next-gen GPU socket win","警戒閾值":"NVDA Rubin / VeraRubin 公開供應商名單缺 Vicor；MPWR Q2-Q3 26 法說明確點名 attaching to NVIDIA digital power；需 ≥ 50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":267.99,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"VICR","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"Vicor Corporation"},"oneliner":"Vicor 第三季營收年增 78.5%、毛利率 68.3%，但約七成營業利益來自權利金；現價約明年共識 EPS 的 35 倍，產品產能在 2027 年中前受限。先等第四季權利金底數兌現，或股價回到 180 美元以下","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/scenario.json","answers":{"q1_business":{"verdict":"Vicor 賺兩筆錢：一是 AI 運算、ATE、工業與國防客戶的負載點供電，二是向 OEM 收專利權利金。錢卡在負載點電流密度這一節點，目前約七成營業利益來自權利金","reasoning":"第三季營收 1.971 億美元。先進產品（含權利金）1.389 億，占 70.4%，其中權利金 6,660 萬；磚型電源 5,830 萬，占 29.6%。毛利率 68.3%，營益率約 36.6%。客戶面，10-K 稱先進產品營收大部分來自少數客戶，且集中度會再升高；前一兩大客戶的占比事實表未涵蓋，管理層也拒答首要客戶是否達 10%。ATE 客戶年營收逾 1 億美元（管理層口述）。產業處於擴張期，依據是 AI 處理器電流需求逐代倍增，一年期在手訂單 4.06 億美元。產業態勢屬雙向拉鋸：一方面需求與授權結構在轉好，ITC 已立案、首份 VPD 授權已簽；另一方面競爭在惡化，大型 IDM 以折價守份額，MPS 曾在 H100 取代 Vicor，ADI 傳聞布局垂直供電。單點依賴屬集中度風險，不是護城河證據","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi5_backlog"],"verdict_values":{"revenue_quality":"品質中等。產品營收約 1.31 億美元來自出貨，受第一廠產能限制；權利金 6,660 萬含新授權首付，管理層給的經常性底數為每季 4,300 萬","unit_econ_note":"執行長稱第二代 VPD 每片面板營收約可倍增（2026-06-19）。權利金幾乎沒有銷貨成本，但法律費約占權利金 20%。單價趨勢管理層拒答","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"低","fingerprint":"高毛利專利型硬體加授權收入。2024 年 EPS 僅 0.14 美元，獲利曲線剛轉折"},"industry":{"clock_phase":"II","sd_verdict_source":"需求面屬結構性持久：AI 處理器電流需求由數百安培走向數千安培，一年期在手訂單 4.06 億美元，第四季前兩週接單 1 億美元。供給面短期卡在 Vicor 自身產能，對手產能可逆性高。來源為公司季報與 2026-10-20 電話會議","bargaining":{"up":"上游議價力偏弱：先進產品與部分半導體依賴少數代工廠，封裝與測試也只由少數第三方處理","down":"下游客戶集中，每代處理器平台重新議價；但管理層稱多數客戶對 Vicor 為單一來源","geo":"中國含香港約占 2025 年營收 11.9%。產品屬 EAR99，不需出口許可。2025 年 Section 301 關稅約 737.5 萬美元"},"profit_pool_dir":"管理層稱利潤池正往負載點與 IP 授權移動，但 GPU 廠仍拿走價值鏈大部分；第三方量化資料事實表未涵蓋","tam_table":[{"item":"資料中心加速器市場","value":"2025 年 1,708 億美元，2030 年 3,727 億美元，年複合 16.9%（MarketsandMarkets）"},{"item":"800VDC 在新增資料中心容量的採用率","value":"2027 年 16.0%，2030 年 79.1%（Citi）"},{"item":"Vicor 負載點供電滲透率與份額","value":"事實表未涵蓋"},{"item":"營業利益池占比（5 年前與現在）","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平。專利授權變現正在擴大，但在最大 GPU 客戶的產品插座已失守，兩者相抵","reasoning":"機制是三件事的組合：分解式供電（電流倍增）、VPD 專利組合、自有晶圓級封裝製程。管理層稱第二代 VPD 電流密度約 3 A/mm²，目標 5 到 6。同業 ROIC 事實表未涵蓋，改用利潤率比較：截至 2026-06 的 TTM 營益率 Vicor 18.6%，MPWR 28.7%，落後約 10 個百分點。第三季單季營益率 36.6%，但約七成來自權利金。推算方式：權利金 6,660 萬減法律費 1,610 萬約 5,050 萬，對營業利益 7,210 萬，假設權利金幾乎沒有銷貨成本。評分：執行 6 分，因首要客戶時程晚約 9 個月、產能有瓶頸；定價力 8 分，因授權費率可隨 ITC 程序遞增、毛利率 68.3%。方向：授權在擴大，最大 GPU 客戶的產品份額在縮減，合計持平","fact_refs":["f_peer_vicr_operating_margin_pct","f_peer_mpwr_operating_margin_pct","f_peer_vicr_gross_margin_pct","f_peer_mpwr_gross_margin_pct","f_kpi1_gaap","f_kpi2_gaap"],"verdict_values":{"moat":{"mechanism":"分解式供電與 VPD 專利組合，加上自有 ChiP 晶圓級封裝製程；以 ITC 進口禁令為槓桿，收取遞增權利金","execution":6,"pricing":8,"grade":"B","trend":"→","trend_evidence":"擴大的一面：第三季權利金季增 119% 至 6,660 萬美元；首份純 VPD 授權簽給領先 AI OEM；ITC 於 2026-10-09 立案，列 20 家被訴方。縮減的一面：MPS 於 2023 年在 H100 取代 Vicor；二手分析稱部分 Nvidia 平台失守；首要客戶時程比去年說法晚約 9 個月。兩相抵銷，判持平","competitor_notes":[{"name":"MPWR","strategy_note":"TTM 營益率 28.7%，高於 Vicor 的 18.6%；曾在最大 GPU 客戶平台取代 Vicor，也是 ITC 被訴方之一，屬最直接的插座競爭者"},{"name":"2308.TW","strategy_note":"毛利 35.7%、營益 16.8%，以系統電源規模與成本競爭；同列 ITC 被訴方，可能成為授權對象"},{"name":"VRT","strategy_note":"機房層電力設備，自由現金流率 25.5%；不在負載點環節直接競爭，只作 AI 電力鏈獲利參照"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能以利潤率比較；Vicor 最新單季營益率已反超，但含一次性權利金","threats":[{"level":"🔴","text":"大型 IDM（MPS、Infineon 等）以整合式電壓調節器加大幅折價搶 AI 處理器插座，已在最大 GPU 客戶平台取代 Vicor","p":"35%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#3"]},{"level":"🔴","text":"架構替代：IVR、6V 中間匯流排，以及 ADI 傳聞收購 Empower 的垂直供電方案。若在下一代平台夠用，會繞過 Vicor","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"客戶自尋第二貨源；管理層已把重心從第二貨源轉向自建第二廠，第二貨源夥伴仍未定案","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率（最新一季營益率 36.6%）乘上周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（AI 處理器）、決策者（GPU 與系統廠）、付款者（OEM 與超大規模業者）三方都需要更高的負載點電流密度。執行長稱每代處理器電流已從數百安培走向數千安培（2026-10-20）。在手訂單 4.06 億美元，第四季前兩週接單 1 億美元"},{"item":"決策層級","level":"🟡","text":"決策單位是單一處理器平台的供電插座，每代重新競標。Vicor 曾在 H100 平台被 MPS 取代；管理層稱多數客戶對其為單一來源，但重新認證週期約為一代平台"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的經濟利益主要由 GPU 廠與雲端業者拿走，供電占系統成本比例小（金額事實表未涵蓋）。Vicor 以權利金從 OEM 端分一杯羹，但買方集中，對手可由多家供應"},{"item":"社會容忍度","level":"🟡","text":"權利金靠 ITC 進口禁令與遞增費率收取，屬依賴監管救濟的優勢。超大規模業者若集體抵制，或 ITC 裁定不利，費率上限會被壓低"}],"roiic":"事實表未涵蓋（缺投入資本與折舊攤提）","reinvest_rate":"無法精算。第三季資本支出 1,610 萬美元約為淨利 6,330 萬的 25%，折舊與營運資金變動未涵蓋，第二廠金額也尚未揭露","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率，周轉率缺資料。內生成長＝增量 ROIC×再投資率，兩項皆缺，故天花板不給數字。近期成長主要來自毛利率擴張，不是再投資"}}}},"q3_growth":{"verdict":"五年後跑道判寬。AI 負載點供電滲透率仍低，授權是第二條曲線；但 2027 年中以前，產品成長會被產能卡住","reasoning":"成長來源是量加價：量來自產品出貨，受第一廠特定製程瓶頸限制，第四季指引季增約 10%；價來自授權費率隨 ITC 程序每月約遞增 5%。沒有併購，也沒有淨回購。共識 EPS 路徑：2025 年 2.61（含專利和解），2026E 4.12，2027E 6.12，2028E 8.31，三年年複合約 47%；FY1 共識三個月內上修 34%。內生上界因投入資本與折舊未涵蓋，算不出數字。缺口歸因於毛利率擴張（權利金近全額毛利、稼動率提升）與營運槓桿，不是再投資，所以成長對權利金能否延續高度敏感。跑道方面，資料中心加速器市場至 2030 年年增約 17%，每代處理器電流需求倍增；Vicor 份額事實表未涵蓋，但明顯偏低。授權構成第二條曲線，因此五年後跑道判寬。衰退信號亮兩個，價值陷阱風險中等","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_backlog","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"以量為主（產品出貨受產能限制），加上價（授權費率隨 ITC 程序遞增）；無併購、無淨回購","runway_years":"事實表未涵蓋份額，無法換算年數；按 5 到 9 年的中等折扣處理","runway_post_y5":"🟢","endo_ceiling_basis":"內生上界無法以增量 ROIC×再投資率計算，因投入資本與折舊未涵蓋。共識三年 EPS 年增約 47%，遠高於近年資本支出規模所能支撐的內生成長。缺口歸因：毛利率擴張（權利金近全額毛利、稼動率提升）與營運槓桿；沒有淨回購，也沒有收購","segments":[{"item":"先進產品（含權利金）","value":"第三季 1.389 億美元，占 70.4%，季增 47.5%；其中權利金 6,660 萬，季增 119.1%"},{"item":"磚型電源","value":"第三季 5,830 萬美元，占 29.6%，季增 18.4%"},{"item":"ATE 測試客戶","value":"年營收逾 1 億美元（管理層口述）"},{"item":"第四季指引","value":"產品營收季增約 10%，權利金至少 4,300 萬美元（假設無新授權）"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差距超過 5 個百分點）","lit":true,"note":"共識 2025 到 2027 年 EPS 年增約 53%，營收年增約 44%"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"2026-07 二手分析稱部分 Nvidia 平台失守，沒有量化份額"},{"signal":"毛利率連兩季年減","lit":false,"note":"第三季毛利率年增 1,080 基點"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"第三季約 2.7%"},{"signal":"FCF 對淨利低於 0.75 連兩年","lit":false,"note":"2024 年約 4.4，2025 年約 1.0"},{"signal":"其餘五類","lit":false,"note":"TAM 仍在擴張；產業倍數、維持性資本支出、停止投資產能三項未見或事實表未涵蓋"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中上。約 5 億美元淨現金可自籌第二廠，股權酬勞低；回購授權剛核准，還看不到執行","reasoning":"自由現金流對淨利：第三季 5,360 萬÷6,330 萬約 0.85；2025 年 1.19 億÷1.19 億約 1.0，含和解金。股權酬勞第三季約 530 萬美元，占營收 2.7%。現金去向：第三季資本支出 1,610 萬，在建工程尚待支出約 4,860 萬；沒有股息；2026-08-25 核准 1.5 億美元回購，執行金額未涵蓋；沒有併購。資產負債：現金 5.13 億、總債務約 716 萬。管理層稱第二、三廠不需增資，但第二廠資本支出金額尚未揭露，是下一個要看的數字","fact_refs":["f_kpi4_69_7_16_1","f_kpi3_gaap_eps","f_kpi6","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 無併購類項目"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"2026-08-25 核准 1.5 億美元新授權；實際買回股數與均價事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季股權酬勞約 530 萬美元，年化約 2,100 萬，約為市值 98.4 億的 0.2%；完整稀釋股數變化事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月無併購項目；回購授權剛核准，尚無執行數字"}}}},"q5_valuation":{"verdict":"現價要求 2027 到 2028 年 EPS 照共識翻倍，而且權利金被當成經常性收入。我只信一半，估值中性，不追","reasoning":"現價 213.42 美元，等於前瞻本益比 51.8 倍、明年共識 EPS 6.12 美元的 34.9 倍、後年 8.31 美元的 25.7 倍。要划算，需要三件事同時成立：權利金每季至少 4,300 萬美元並延續；第二廠 2027 年第二季上機後，產品營收再增三成以上；毛利率守住 65% 以上。我信產品需求，對權利金只信底數，所以 Base 年報酬約 9%，屬中段。歷史分位兩把尺方向相反：本益比在近四個年度端點只在 7% 分位，因為過去 EPS 低、本益比高；市銷率與企業價值對營收都在 100% 分位。以分母較穩的營收倍數看偏貴。賣方目標價均值約 382 美元，但多為 7 月前的快照，Needham 已由 400 降到 320，不採用。PEG 約為 51.8÷47≈1.1","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_fwd","f_consensus_eps_fy2","f_consensus_eps_fy3","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比與 PEG，以 FY1 共識 EPS 為分母；營收倍數作輔助","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率、沒有同業倍數，無法當估值錨；賣方目標價快照日期不一"},"fwd_pe":51.8,"peg":1.1,"percentile_5y":7.0,"val_light":"🟡","val_light_derivation":"前瞻本益比 51.8 倍，明年共識 EPS 對應約 34.9 倍。三年 EPS 年複合約 47%（2.61 到 8.31，基期含專利和解），PEG 約 1.1，落在合理區。但有兩個反向因素：市銷率 17.6 倍位於近四個年度端點最高；最新一季獲利約七成來自權利金，分母有爭議，不能據以說便宜。綜合判中性。分位值 7 為本益比在四個年度端點內的分位，不是真正的五年分位","upside_short_pct":4,"upside_mid_pct":35,"denominator_disputed":true,"denominator_note":"第三季 EPS 1.33 美元含新授權首付；管理層給的經常性權利金底數為每季 4,300 萬，比第三季的 6,660 萬少約 35%。2025 年 EPS 含 4,500 萬美元專利和解收入。以 Base 估算，權利金淨貢獻約占 2027 年 EPS 四成，分母延續性本身就是爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩處：把權利金當成經常性收入，以及把首要客戶的量產時程當成確定","reasoning":"第一，權利金：最新一季約七成營業利益來自權利金，延續性取決於 ITC 程序與兩年期授權的續約。第二，客戶集中：首要客戶時程已比去年說法晚約 9 個月，管理層拒答其營收占比。第三，競爭：最大 GPU 客戶的插座已被 MPS 拿走，第二代 VPD 在首要客戶以外的導入，業務主管也承認還在早期。股價距 104 週均線約 −42%、距 250 週均線約 −61%，反映這是一檔回撤很深的股票。三視角的反證與裁定寫在反證紀錄","fact_refs":["f_kpi5_backlog","f_week26_return_pct","f_ma_w104","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長真實，獲利組成待驗"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":4.12,"pe":51.8,"basis":"起點用 FY1（FY2026E）共識 EPS 4.12 美元，屬前瞻口徑。終端年 FY2031E 在 2031 年 10 月時同樣是當年度，倍數分母同口徑"},"eps":{"bull":[6.6,9.2,11.8,14.3,16.5],"base":[6.0,7.8,9.3,10.6,11.8],"bear":[3.4,3.8,4.3,4.8,5.3]},"pe":{"bull":32,"base":28,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-65,"hi":-35,"basis":"下緣：回到 250 週均線 82.75 美元約 −61%，再加上權利金腰斬這類單一事件的衝擊，取 −65%。上緣：回到 104 週均線 124.38 美元約 −42%，取 −35% 作為較溫和的財報後修正；現價距 52 週均線約 −7%，距前份判斷時的股價已跌 20%。Bear 終值約 −45%，落在範圍內","trigger_time":null},"basis":{"bull":"產品營收 2031 年達約 20 億美元，權利金 3 億以上，合計約 25 億；營益率 40%，股數約 4,850 萬；終端 32 倍","base":"2031 年營收約 19 億美元，其中權利金約 2.5 億；營益率約 38%，股數約 4,900 萬；成長降到約一成，終端 28 倍","bear":"ITC 不利，權利金降到每年 8,000 萬以下，首要客戶減單；2027 年 EPS 跌到約 3.4 美元，之後年增約一成；成長熄火，終端 22 倍"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"10-K 稱先進產品營收大部分來自少數客戶，而且集中度還會升高；首要客戶時程比去年股東會所示晚約 9 個月；管理層不答首要客戶是否達 10% 營收門檻","assumption":"首要客戶 2027 年照計畫量產，ITC 也帶來新的授權","consequence":"若首要客戶減單與 ITC 初裁不利同時發生，EPS 回到 3 美元附近、本益比 22 倍，股價跌幅約六成以上","ruling":"部分採納。Bear 機率定 30%，ITC 初裁前倉位上限 3%","watch":"一年期在手訂單、季度權利金、10-Q 的客戶集中度揭露","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"],"fact_refs":["f_kpi5_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"法律費約為權利金的 20%；第二、三廠資本支出尚未揭露；10-K 稱大型對手以大幅折價守份額；2025 年關稅約 737.5 萬美元且已加徵；先進產品依賴少數代工與封測","assumption":"營收達 25 億美元時，營益率能到公司目標 40%","consequence":"營收成長兌現，但營益率停在 30% 左右、自由現金流被建廠吃掉，EPS 比 Base 低約兩成","ruling":"部分採納。Base 終值營益率假設約 38%，低於公司 40% 的目標","watch":"第二廠資本支出金額（管理層稱下次電話會議揭露）、法律費占權利金比例、扣除權利金後的產品毛利率","evidence_refs":["competitive_share_entrants#1","reg_tariff_export#0","geo_supply_chain#0"],"fact_refs":["f_kpi1_gaap","f_kpi2_gaap"]},{"view":"價格已反映太多","evidence":"市銷率 17.6 倍、企業價值對營收 16.7 倍，都在近四個年度端點的最高位；前瞻本益比 51.8 倍；FY1 共識 EPS 三個月上修 34%","assumption":"共識上修反映的是經常性獲利","consequence":"若市場剔除第三季權利金的一次性部分，實際前瞻倍數會高於帳面","ruling":"採納。估值中性，不追，等價格或權利金底數兌現","watch":"共識 EPS 修正方向、第四季權利金金額","evidence_refs":[],"fact_refs":["f_ps_current","f_ev_s_current","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]},{"view":"論點失敗","evidence":"10-K 稱產業技術變動快、成熟產品價格侵蝕；有傳聞 ADI 以約 15 億美元收購 Empower 布局垂直供電；MPS、Infineon 同樣在推封裝上供電；開放運算大會聚焦 800V 配電與 6V 中間匯流排","assumption":"負載點電流密度的瓶頸只有 Vicor 的分解式供電能解","consequence":"若 IVR 或整合式電壓調節器在下一代平台夠用，Vicor 產品端只剩首要客戶，授權談判籌碼也會減弱","ruling":"部分採納，列為第三項風險，機率約三成。ADI 收購屬未證實傳聞，不加權","watch":"超大規模業者是否導入第二代 VPD；ADI 與 Empower 的交易是否成立","evidence_refs":["substitute_technology#0","substitute_technology#1"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 267.99 → 本次 213.42（-20.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=267.99","side_b":"本次 price_at_dd=213.42","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 267.99 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 267.99 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 267.99 美元：Bull 價 528、Bear 價 116.6，五年期望值 +17.8%，基準年化 4.3%，不對稱比 1.43","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.43。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 267.99 美元：五年期望值 +17.8%，基準年化 4.3%，不對稱比 1.43","side_b":"本次情境、股價 213.42 美元：五年期望值 +47.9%，基準年化 9.1%，不對稱比 2.71","ruling":"再換股價、情境不動：起點價下跌 20.4%，五年期望值多 30.1 個百分點，基準年化多 4.9 個百分點，不對稱比由 1.43 升到 2.71。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-05-24，股價 267.99 美元）估值判中性","side_b":"本次股價 213.42 美元，FY1 共識 EPS 三個月上修 34%；前瞻倍數下降，但權利金占獲利比重過高，分母有爭議","ruling":"維持中性，不因股價下跌改判便宜","evidence_level":"事實表價格與共識快照","settle_metric":"第四季權利金是否守住 4,300 萬美元","if_then":["若第四季與 2027 年第一季權利金都至少 4,300 萬美元，分母爭議解除，估值可改判偏便宜","若權利金低於 3,000 萬美元，估值改判偏貴，不建倉"],"evidence_refs":[]},{"axis":"前份漂移：訊號與陷阱","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份訊號 B，陷阱風險中等","side_b":"新證據方向不一：第三季毛利率 68.3%、權利金 6,660 萬、ITC 立案、購入第二與第三廠場址；但首要客戶延後約 9 個月，第四季總營收預期季減","ruling":"兩項都維持不變：品質改善由權利金帶動，產品端的不確定性同步上升，兩者相抵","evidence_level":"8-K 與電話會議","settle_metric":"2027 年上半年產品營收季增率","if_then":["若 2027 年第一、二季產品營收季增都至少 8%，陷阱風險可降一級","若產品營收連兩季季增低於 5%，陷阱風險升一級並停止加碼"],"evidence_refs":[]},{"axis":"前份漂移：前份未填欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份上述欄位為空","side_b":"本次依現行判斷流程補上：護城河方向持平，五年後跑道寬，公司類型為品質複利成長（低信心）。本次判定非循環股，循環位置不適用。情境機率與最大回撤由本次情境樹產生；裁決與角色由程式依本次輸入重算","ruling":"屬方法補欄，不代表基本面改變","evidence_level":"方法","settle_metric":"無","if_then":["若之後判定為循環股，再補循環位置","若護城河方向轉為縮減，重寫情境機率"],"evidence_refs":[]},{"axis":"重新進場條件新設","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件","side_b":"股價不高於 180 美元，或 2026 年第四季權利金至少 4,300 萬美元且產品營收季增約 10% 兌現","ruling":"新設。條件成立前不建倉；ITC 初裁不利時，持有者清倉","evidence_level":"判斷","settle_metric":"股價、第四季權利金與產品營收","if_then":["若條件成立且無新的負面證據，分兩批建倉","若 ITC 初裁不利，持有者清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"ITC 第 337 條 VPD 調查的行政法官初裁，認定不侵權或專利無效","ruling":"Single Thing 改為 ITC 初裁。理由：在情境中它是數學上最大的單一敏感項，權利金淨貢獻約占 2027 年 EPS 四成；發生時清倉","evidence_level":"8-K 與電話會議推算","settle_metric":"USITC 初裁公告","if_then":["若初裁不利，持有者清倉，未持有者不建倉","若初裁有利，ITC 階段的倉位上限解除"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標","side_b":"權利金連兩季低於 3,000 萬美元；一年期在手訂單低於 3.5 億美元；ITC 初裁不利；合併毛利率連兩季低於 55%","ruling":"新設。前兩項與第四項任一觸發即減碼一半；ITC 初裁不利則清倉","evidence_level":"判斷","settle_metric":"每季 8-K","if_then":["若任一指標觸發，減碼一半","若 ITC 初裁不利，清倉"],"evidence_refs":[]},{"axis":"論點門檻改寫","cause":"新證據","prior_field":["H1.threshold","H2.threshold"],"side_a":"前份 H1：2027 全年產品營收至少 12 億美元，2026 年第四季單季至少 3 億；前份 H2：2027 年權利金至少 8,000 萬美元","side_b":"本次 H1：2026 年第四季產品營收至少 1.43 億美元，2027 全年至少 7 億；本次 H2：每季權利金至少 4,300 萬，2027 全年至少 1.7 億","ruling":"前份 H1 門檻已無法達成：財務長指引第四季產品營收約季增 10%，約 1.44 億，離 3 億差一倍；首要客戶時程晚約 9 個月，第二廠 2027 年第二季才分段上機。前份 H2 門檻則偏低：第三季單季權利金 6,660 萬，已達全年門檻的八成以上","evidence_level":"8-K 與 2026-10-20 電話會議","settle_metric":"2026 年第四季產品營收與權利金","if_then":["若第四季產品營收低於 1.35 億美元，H1 削弱並下修 Base","若第四季權利金至少 4,300 萬美元，H2 維持"],"evidence_refs":[]},{"axis":"權利金是否屬經常性","cause":"新證據","prior_field":null,"side_a":"財務長：第三季權利金 6,660 萬美元中有一部分是新授權首付，不會重複；第四季底數 4,300 萬","side_b":"執行長：被稱為「不重複」的收入一再出現，應視為經常性；第四季初同一被授權人又下了大單","ruling":"性質屬程度差異，可調和。取兩者交集：4,300 萬美元是可依賴的底數，超出部分當一次性。因此第三季 EPS 1.33 美元高估了經常性獲利","evidence_level":"公司電話會議口述加 8-K","settle_metric":"2026 年第四季與 2027 年第一季權利金","if_then":["若兩季權利金都至少 4,300 萬美元且有新授權，權利金視為經常性，依重新進場條件分批建倉","若任一季低於 3,000 萬美元且無新授權，Base 路徑下修約兩成、不建倉；持有者減碼一半"],"evidence_refs":[]},{"axis":"產能說法與實際成長","cause":"新證據","prior_field":null,"side_a":"管理層稱第一廠年產出可由約 10 億美元升至至少 15 億（2026-05-01、2026-06-19）","side_b":"2026-10-20 指引第四季產品營收只季增約 10%，年化約 5.7 億，受特定製程步驟限制","ruling":"性質屬程度差異。以實際出貨為準：2027 年上半年產品成長受第一廠瓶頸限制。共識 2027 年營收 9.43 億美元，扣掉權利金底數約 1.72 億後，產品營收需比第四季年化再增三成以上；第二廠 2027 年第二季分段上機是關鍵","evidence_level":"電話會議與事實表共識","settle_metric":"2027 年第一、二季產品營收季增率","if_then":["若 2027 年第一季產品營收季增至少 8%，維持 H1","若產品營收連兩季季增低於 5%，H1 削弱，Base 的 2027 年 EPS 下修至 5.5 美元以下，並停止任何加碼"],"evidence_refs":[]},{"axis":"負載點供電競爭","cause":"新證據","prior_field":null,"side_a":"管理層：競品第一代 VPD 侵權、電流密度不足；第二代 VPD 電流密度約為對手的三倍（2026-10-20）","side_b":"第三方報導 MPS 在 H100 取代 Vicor（2023）；二手分析稱 Vicor 在部分 Nvidia 平台輸給低成本整合方案；10-K 自承大型對手以大幅折價守份額","ruling":"性質屬程度差異，可調和：技術領先目前只在首要客戶與授權收入上兌現，最大 GPU 客戶的產品份額已失守。Base 不假設奪回最大 GPU 客戶插座，護城河以授權變現為主","evidence_level":"10-K、第三方報導、二手分析","settle_metric":"首要客戶以外的第二代 VPD 量產訂單","if_then":["若 2027 年底前出現首要客戶以外的第二代 VPD 量產訂單，產品護城河改判擴大，Bull 機率上調至 30%","若 ITC 初裁不利且沒有新客戶，護城河改判縮減，持有者清倉"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#3"]},{"axis":"觀望的反面：現在就買的最強論證","cause":"價格變動","prior_field":null,"side_a":"現在就買的理由：股價半年跌 19%，FY1 共識 EPS 卻三個月上修 34%；明年本益比約 35 倍，對應三年 EPS 年增約 47%；淨現金約 5 億美元可自籌第二廠；ITC 立案後授權費率每月約遞增 5%，時間站在 Vicor 這邊","side_b":"等待的理由：最新一季獲利約七成來自權利金，經常性底數只有 4,300 萬；第四季總營收預期季減；產品產能 2027 年中前受限；Base 年報酬約 9%，不足以補償深回撤","ruling":"選等待。Base 年報酬約 9% 只在中段，分母爭議也還沒解。這是價格與證據雙重約束；約束解除的條件是股價回到 180 美元以下，或第四季底數兌現","evidence_level":"事實表價格與共識、電話會議","settle_metric":"第四季權利金與產品營收；股價","if_then":["若股價不高於 180 美元且無新的負面證據，分兩批建首倉","若第四季底數兌現但股價高於 250 美元，不追，等 2027 年第一季再檢查"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"第四季產品營收是否照指引季增約 10%","type":"假設驗證","maps_to":"H1","metric":"季度產品營收（扣除權利金）","threshold":"2026 年第四季至少 1.43 億美元","action":"達標則維持觀察並檢查進場價位；低於 1.35 億美元則下修 Base 路徑、不建倉","source_freq":"公司季報（每季）","date":"2027-02"},{"n":2,"text":"權利金經常性底數是否守住","type":"假設驗證","maps_to":"H2","metric":"季度權利金","threshold":"每季至少 4,300 萬美元","action":"連兩季達標則視為經常性；低於 3,000 萬美元則減碼一半","source_freq":"公司季報（每季）","date":"2027-02"},{"n":3,"text":"ITC 的 VPD 調查初裁","type":"Single Thing","maps_to":"Single Thing","metric":"ITC 第 337 條 VPD 調查初裁結果","threshold":"認定不侵權或專利無效","action":"持有者清倉；未持有者不建倉","source_freq":"USITC 公告（事件）","date":"2027-H2"},{"n":4,"text":"首要客戶與在手訂單","type":"風險","maps_to":"R1","metric":"一年期在手訂單與先進產品營收","threshold":"在手訂單低於 3.5 億美元，或先進產品（扣權利金）單季季減至少 10%","action":"減碼一半","source_freq":"公司季報（每季）","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":5,"text":"競品或替代架構拿下下一代平台","type":"風險","maps_to":"R3","metric":"主要 GPU 平台與超大規模業者的供電方案","threshold":"下一代平台確認改用競品垂直供電方案，且沒有第二代 VPD 新客戶","action":"減碼至半倉","source_freq":"產業發表與公司電話會議（每季）","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#3","substitute_technology#0","substitute_technology#1"]},{"n":6,"text":"關稅、出口管制或代工受阻導致毛利率失守","type":"風險","maps_to":"R4","metric":"合併毛利率","threshold":"連兩季低於 55%","action":"停止加碼","source_freq":"公司季報（每季）","date":null,"evidence_refs":["geo_supply_chain#0","reg_tariff_export#0","reg_tariff_export#2"]},{"n":7,"text":"證券集體訴訟重新提起","type":"風險","maps_to":"無對應論點（治理事件）","metric":"放空者證券集體訴訟的進度","threshold":"重新提告並獲集體認證，或和解金額超過現金的 10%","action":"減碼一半","source_freq":"10-K 與 10-Q 附註（每季）","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":8,"text":"重新進場條件","type":"估值rearm","maps_to":"H1,H2","metric":"股價與第四季兌現","threshold":"股價不高於 180 美元，或第四季權利金至少 4,300 萬美元且產品營收季增約 10%","action":"分兩批建首倉","source_freq":"每日股價；公司季報","date":null},{"n":9,"text":"第二代 VPD 擴到首要客戶以外","type":"加碼","maps_to":"H3","metric":"第二代 VPD 新客戶量產訂單","threshold":"首要客戶以外至少一家宣布量產，且權利金連兩季至少 4,300 萬美元","action":"加碼至目標倉位，ITC 初裁前上限 3%","source_freq":"公司電話會議（每季）","date":"2027-Q4"},{"n":10,"text":"第四季財報後複審","type":"複審日期","maps_to":"H1,H2,H3","metric":"全部論點門檻","threshold":"財報公布後","action":"重跑判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"季度權利金收入","bear_threshold":"連兩季低於 3,000 萬美元","window":"2027 年各季","source":"公司季報 8-K 新聞稿","last_status":"ok"},{"metric":"一年期在手訂單","bear_threshold":"低於 3.5 億美元","window":"每季","source":"公司季報電話會議","last_status":"ok"},{"metric":"ITC 第 337 條 VPD 調查初裁","bear_threshold":"認定不侵權或專利無效","window":"2027 下半年至 2028 年","source":"USITC 公告","last_status":"unknown"},{"metric":"合併毛利率","bear_threshold":"連兩季低於 55%","window":"每季","source":"公司季報 8-K 新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"$.counter_evidence.triggers","reason":"供給面的負向情況已有監控，只是沒有放在單獨的觸發條目。第一廠特定製程瓶頸由觸發條件 1 追蹤：第四季產品營收低於 1.35 億美元就下修 Base。第二廠延後寫在 R4 的門檻：首批設備延到 2027 年第三季之後。反證紀錄「產能說法與實際成長」一條也定了連兩季季增低於 5% 的處置。閘自己也說沒看到漏接，只是看不到該軸的負向條目子集；再加一條觸發會和觸發 1、R4 重複"},{"ref":"$.decision_inputs.market_wrong_reason_given","reason":"第五問的「不追」講的是等價格，不是說估值偏貴。估值判中性，加上權利金分母有爭議，正好是觀望、等 180 美元或第四季底數兌現的理由，和 wait_for_price 的條件一致。oneliner 原文寫的是「先等」，沒有寫「不追」。閘也認定這裡不是判斷錯誤，所以不改"}],"action_conditions":{"rearm_trigger":"股價不高於 180 美元，或 2026 年第四季權利金至少 4,300 萬美元且產品營收季增約 10% 兌現","exec_line":"條件成立後分兩批建倉，第一批不超過目標倉位一半；ITC 初裁前總倉位不超過 3%；初裁不利即清倉","holding_cap":"ITC 初裁前不超過 3%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 180 美元以下（約明年共識 EPS 的 29 倍），或第四季權利金至少 4,300 萬美元且產品營收季增約 10% 兌現","qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-19.46, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"產品營收（扣權利金）隨第一廠去瓶頸，以及第二廠 2027 年第二季起分段上機而持續成長","2y":"2027 全年產品營收至少 7 億美元","5y":"2031 年產品營收至少 15 億美元（第二廠滿載）","10y":null,"threshold":"2026 年第四季產品營收至少 1.43 億美元（季增約 10%）；2027 全年產品營收至少 7 億美元","source":"2026-10-20 第三季電話會議的財務長指引；公司季報新聞稿","drift_rule":"兩年期：產品營收 TTM 對門檻路徑連兩季偏離至少 5% 為削弱，連三季偏離至少 10% 為反轉"},{"id":"H2","text":"權利金已成經常性收入；ITC 調查促使更多 OEM 與超大規模業者以遞增費率取得授權","2y":"2027 全年權利金至少 1.7 億美元，並至少新增一家超大規模業者授權","5y":"2031 年權利金至少 3 億美元","10y":null,"threshold":"每季權利金至少 4,300 萬美元（無新授權時的底數）","source":"2026-10-20 電話會議的財務長與執行長說法；USITC 2026-10-09 立案公告","drift_rule":"兩年期：權利金 TTM 對門檻路徑連兩季偏離至少 5% 為削弱，連三季偏離至少 10% 為反轉"},{"id":"H3","text":"第二代 VPD 在首要客戶以外取得量產訂單，產品毛利率隨規模回升，整體朝 70% 毛利、40% 營益的長期模型靠攏","2y":"2027 年底前，至少一家首要客戶以外的 OEM 或超大規模業者進入第二代 VPD 量產","5y":"合併毛利率維持至少 65%，營益率至少 35%","10y":null,"threshold":"合併毛利率至少 65%、營益率至少 35%；2027 年底前有首要客戶以外的量產訂單","source":"2026-06-19 股東分析師會議；2026-07-21 與 2026-10-20 電話會議","drift_rule":"五年期：TTM 毛利率或營益率連四季偏離至少 5% 為削弱，連六季偏離至少 10% 為反轉"}],"R":[{"id":"R1","text":"首要運算客戶集中：先進產品營收集中在少數客戶，首要客戶延後或減單會立即反映在產品營收","h_ref":"H1","clock":"⚡","threshold":"一年期在手訂單低於 3.5 億美元，或先進產品（扣權利金）單季季減至少 10%；連兩季即減碼","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R2","text":"權利金延續性：兩年期授權到期需續約，ITC 程序可能延後，被訴方也可能以設計迴避，經常性底數因此下滑","h_ref":"H2","clock":"🔥","threshold":"單季權利金低於 3,000 萬美元且當季無新授權；連四季才大動作，ITC 初裁不利例外","evidence_refs":[]},{"id":"R3","text":"競品與架構替代：整合式電壓調節器、IVR、ADI 與 Empower 的垂直供電若在下一代 AI 平台夠用，第二代 VPD 只停在首要客戶","h_ref":"H3","clock":"🐢","threshold":"2027 年底前沒有首要客戶以外的第二代 VPD 量產訂單，且主要 GPU 平台確認採用競品；機率至少 50% 才砍倉","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#3","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"製造與政策：先進產品依賴少數代工與封測，Section 301 關稅加徵，實體清單擴大；第二廠上機延後會讓產能瓶頸拉長","h_ref":"H1","clock":"🔥","threshold":"合併毛利率連兩季低於 55%，或第二廠首批設備延到 2027 年第三季之後","evidence_refs":["geo_supply_chain#0","reg_tariff_export#0","reg_tariff_export#2"]}],"single_thing":{"description":"ITC 第 337 條 VPD 調查的行政法官初裁，認定不侵權或專利無效","why_fatal":"最新一季約七成營業利益來自權利金。遞增費率與進口禁令是逼 OEM 與超大規模業者簽約的主要槓桿；初裁不利會讓新授權停滯，兩年期授權續約降價，Base 情境約四成 EPS 消失","if_happens":"Base 改走 Bear 路徑；持有者清倉，未持有者放棄進場","how_monitor":"USITC 案件程序表、聽證日期與初裁公告；公司每季權利金金額","probability":"約 25%（12 到 24 個月內出現不利初裁；判斷值，事實表無勝訴率資料）"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":34.9,"peg_fy2":0.83,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":2.61,"FY2026E":4.12,"FY2027E":6.12,"FY2028E":8.31},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識取自 Koyfin 快照。FY2025A 含 2025 年 5 月 4,500 萬美元專利和解收入"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報：權利金是否至少 4,300 萬美元、產品營收是否季增約 10%，並可能揭露第二廠資本支出","impact":"高","watch":"權利金、產品營收、第二廠金額"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"第二廠（Merrimack）2027 年第二季首批設備上機","impact":"中","watch":"產品營收季增率是否回升"},{"date":"2027-08","date_precision":"month","type":"regulatory","event":"ITC 的 VPD 調查進入聽證（依執行長所述立案後約 10 個月推估）","impact":"高","watch":"程序是否延後；是否有被訴方和解並取得授權"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"第二代 VPD 在首要客戶量產爬坡，同時看是否出現第二家客戶","impact":"高","watch":"首要客戶以外的量產訂單"}]}
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
