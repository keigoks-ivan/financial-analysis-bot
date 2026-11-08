你是 DD 管線 v20 的判斷層閘（gate），標的 COHR（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（29 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝2370.3 USD million｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q1 FY27（GlobeNewswire 2026-11-04，finviz 轉載全文）（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（本次未取得可靠共識營收數字）
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝23.2 %（營業利益 550.3 百萬美元）｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q1 FY27（GlobeNewswire 2026-11-04，finviz 轉載全文）（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝15.9 %（營業利益 377.9 百萬美元）｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q1 FY27（GlobeNewswire 2026-11-04，finviz 轉載全文）（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無
- `f_kpi5_guidance_q2_fy2027_non_g`（q1_business）｜Guidance: Q2 FY2027 營收／non-GAAP EPS＝營收 2,550–2,750 百萬美元；non-GAAP 毛利率 40%–42%；non-GAAP 營業費用 430–450 百萬美元；non-GAAP 稅率 18%–20%；non-GAAP EPS 2.28–2.48 USD｜期間與口徑：Q1 FY2027 新聞稿（公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 Q1 FY27（GlobeNewswire 2026-11-04，finviz 轉載全文）（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027 新聞稿（公告於 2026-11-04））
  - 註記：媒體稱優於華爾街預期（technews 2026-11-05），具體共識數字查無
- `f_peer_cohr_gross_margin_pct`（q2_moat）｜COHR 毛利率＝38.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cohr_operating_margin_pct`（q2_moat）｜COHR 營業利益率＝14.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cohr_fcf_margin_pct`（q2_moat）｜COHR FCF 利潤率＝-23.28 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lite_gross_margin_pct`（q2_moat）｜LITE 毛利率＝45.91 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lite_operating_margin_pct`（q2_moat）｜LITE 營業利益率＝23.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lite_fcf_margin_pct`（q2_moat）｜LITE FCF 利潤率＝9.52 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝9.42 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝13.97 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝19.13 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝11163.49 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝15504.21 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow_capex`（q4_capital）｜Free cash flow (營業現金流 − capex，自行推算，新聞稿未直接揭露)＝-868.2 USD million｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿現金流量表：營業現金流 -92.7、PP&E 增加 -775.5（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無
- `f_kpi4_sbc_non_gaap`（q4_capital）｜SBC 占 Non-GAAP 營業利益 %＝13.3 %（SBC 73.2 百萬美元；占營收 3.1%）｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q1 FY27；比率為 73.2/550.3 自行推算（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-11-04））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝2592.05 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 4346.98、現金 1754.93（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝40567.65 USD m｜期間與口徑：2026-11-08／市值 37975.6 ＋ 淨負債 2592.05｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝192.81 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.47 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 9.42，分子＝快照價 192.81｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-0.42 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 9.46 → 9.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝196.96 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝39.92 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／1 個年度端點內的分位＝50.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝44.1 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝41.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-42.49 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w104`（q5_valuation）｜104 週均線＝181.49 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝105.98 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2026 風險因素：公司承認可能面臨更激烈競爭，且可能誤判客戶或競爭對手向後整合、取代公司的意願與能力；未量化份額消長。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-14）｜affects：decision_inputs.bear、moat_trend
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：中文報導稱 Innolight 將拿下 2027 年 2.4T 新世代約 60–70% 量，Coherent 約 20–30 萬件（單一來源估計）。
  - 來源：36kr（as_of 2026-09-15）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：非獨立 bear-case 研究頁稱某大客戶約占 D&C 營收 25–35%，並提及 NVDA 可能於 CY2028+ 自製 CPO 光源雷射（未核實）
  - 來源：cohr-research.pages.dev bear case（as_of 2026-11-01）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 10-K：一家主要客戶占合併營收 20%（FY2025、FY2024 各 10%），第二大客戶占 12%；主要來自 Datacenter & Communications 部門。
  - 來源：SEC EDGAR 10-K FY2026 Item 8 Major Customers（as_of 2026-08-14）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 風險因素：兩家客戶在 FY2026 各占營收逾 10%，預期集中度將持續。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-14）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：FQ4 capex 5.56億美元（去年同期1.31億）；Zacks指出現金轉換偏弱、多項ramp重疊；工業部門疲弱
  - 來源：Zacks/Nasdaq 摘要（搜尋結果彙整）（as_of 2026-08-15）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：美國對半導體、關鍵礦物及衍生電子產品啟動 Section 232 調查，可能新增關稅；公司在美國與海外製造採購，自認可能比國際化程度低的企業更易受影響；並提及 AI／資料中心相關產品可能出現新出口管制。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-14）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：美國政府持續擴充實體清單，已對公司營收及銷售能力造成不利影響；若出口管制在產能與採購承諾後加嚴，可能需認列庫存與不可取消採購義務的鉅額費用。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-14）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：中國對美鎵鍺銻出口禁令於 2025-11-09 暫停，期限至 2026-11-27（Fastmarkets、CIRS 報導）；與 COHR 的直接關聯未見公司揭露
  - 來源：Fastmarkets: China suspends export prohibition on gallium, germanium, antimony, superhard materials to US（as_of 2025-11-10）｜affects：decision_inputs.bear、triggers
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：產業層面：磷化銦(InP)基板供應集中，中國出口管制使供應不確定（IQE CEO 說法）；未找到 Coherent 自身 InP 採購揭露
  - 來源：TheNextWeb: China has 70% of a material AI needs, IQE's CEO warns, Bloomberg reports（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：FY2026 Industrial 段營收年減10%（-2.11億），主因出售航太國防與慕尼黑業務
  - 來源：Coherent FY2026 Form ARS (SEC)（as_of 2026-09-30）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K FY2026 風險因子自述：產品可能因替代或更具成本效益的技術推出而競爭力下降；亦有客戶/競爭對手向後整合而取代公司的風險。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-14）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：CPO 被視為可插拔收發器（含 DSP）的結構性替代；Coherent 路線圖稱 1.6T/3.2T 可插拔可能延後 CPO 損益平衡至 2028 年後，並同時展示多種 CPO 技術（OFC 2026）。
  - 來源：DatacenterDynamics 分析：Optical illusion – is co-packaged optics the savior（as_of 2026-05-01）｜affects：moat_trend、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：多家原告律所（Schall、Pomerantz、Rosen）於 2025-09 至 2025-10 公告調查 COHR；導火線是 2025-08-13 的 A&D 出售消息，股價 2025-08-14 單日跌 19.6%。這是律所徵求原告的調查公告，搜尋未找到已提起的集體訴訟案號。
  - 來源：Pomerantz 調查公告（Barchart／Placera 轉載）（as_of 2025-10-28）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：多家原告律所公告調查 COHR（Pomerantz 2025-10-28），起因為 2025-08 A&D 出售消息後股價大跌；未找到已提起的集體訴訟案號。
  - 來源：Pomerantz 調查公告（Barchart）（as_of 2025-10-28）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":756.0,"bear_5y_price":112.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":98.4,"ev5y_pct":104.7,"irr_base_pct":14.7,"asym_ratio":5.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":9.42,"pe":20.47,"basis":"FY1（FY2027E）共識 EPS 9.42 美元，股價 192.81 美元；終端倍數同為當年度 EPS 口徑。事實表未涵蓋同業前瞻本益比，只能對照公司自身 FY1 20.47 倍與 FY2 13.80 倍。"},"eps":{"bull":[10.6,16.5,23.5,30.0,36.0],"base":[10.0,14.0,17.5,20.0,22.5],"bear":[9.2,11.5,8.5,7.0,8.0]},"pe":{"bull":21,"base":17,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### COHR_Q4_2026_Earnings_Call_20260812.md
- 2026-08-12｜CFO｜guidance：FY27 Q1 營收財測區間 $2.2–2.4B（原話："$2.2 billion and $2.4 billion."）
- 2026-08-12｜CFO｜guidance：FY27 Q1 non-GAAP EPS 財測區間 $1.85–2.05（原話："between $1.85 and $2.05 on a non-GAAP basis."）
- 2026-08-12｜CFO｜guidance：FY27 Q1 non-GAAP 營業費用財測 $400–420M（原話："operating expenses of between $400 million and $420 million"）
- 2026-08-12｜CEO｜guidance：CEO 預期 FY27 底前出現首個營收逾 $3B 的季度（原話："our first quarter with over $3 billion of revenue"）
- 2026-08-12｜CEO｜guidance：CEO 稱本季資料中心年增率預期超過 80%（下一句接雷射已備妥）（原話："certainly got the lasers this quarter to make that happen"）
- 2026-08-12｜CFO｜margin：Q4 non-GAAP 毛利率 40.2%（原話："Our Q4 non-GAAP gross margin was 40.2%"）
- 2026-08-12｜CFO｜margin：毛利率改善來源：良率與效率（另有 6 吋 InP、定價優化）（原話："improved manufacturing yields and efficiencies"）
- 2026-08-12｜CFO｜margin：CFO 說 6 吋晶圓產出為 3 吋 4 倍、成本約一半，毛利率效益來自成本結構而非良率（原話："right, 4x, but it's at half the cost."）
- 2026-08-12｜CFO｜margin：管理層稱公司仍處毛利率擴張策略早期（原話："we are early in our strategy for gross margin expansion"）
- 2026-08-12｜CFO｜commitment：毛利率目標大於 42%（分析師提 42.5%，CFO 答投資人日目標為 >42%）（原話："it was greater than 42%."）
- 2026-08-12｜CFO｜commitment：CFO 承諾達標後會調高毛利率目標（原話："greater than 42%, we will no doubt raise the target."）
- 2026-08-12｜CFO｜margin：CFO 稱 Q1 財測中點營業費用已低於 18% 目標模型（原話："in fact, of 18% for OpEx."）
- 2026-08-12｜CFO｜margin：SG&A 共享服務效益超出原預期，預期 FY27 續增（原話："exceeded our original expectations"）
- 2026-08-12｜CFO｜capital_allocation：資料中心投資回收期約 18 個月（原話："have a roughly 18-month payback period."）
- 2026-08-12｜CFO｜capital_allocation：預期 Q1 資本支出再季增（原話："capital expenditures to increase sequentially again"）
- 2026-08-12｜CFO｜capital_allocation：FY26 償還債務 $513M，槓桿降至 0.7x（原話："we made $513 million in debt payments"）
- 2026-08-12｜CEO｜commitment：承諾本季末內部 InP 產能年增一倍，較原計畫提前一季（原話："double our internal indium phosphide output capacity"）
- 2026-08-12｜CEO｜commitment：承諾 CY27 底前 InP 產能再翻倍以上（原話："more than double our internal indium phosphide output"）
- 2026-08-12｜CEO｜product：蘇黎世 6 吋 InP 產線預計 CY27 上半年開始生產（原話："begin 6-inch production in Zurich during"）
- 2026-08-12｜CEO｜product：1.6T 拉貨比三個月前預期更快（原話："1.6T is ramping incredibly fast"）
- 2026-08-12｜CEO｜product：CPO 超高功率 CW 雷射收入預期 12 月季開始（原話："We expect in our December quarter."）
- 2026-08-12｜CEO｜product：PhotonLink 平台初期收入預期自 12 月季開始（原話："initial revenue from PhotonLink-related products"）
- 2026-08-12｜CEO｜product：OCS 可及市場估計逾 $4B（原話："OCS represents more than $4 billion of"）
- 2026-08-12｜CEO｜product：OCS TAM 於 OFC 由 $2B 上調至逾 $4B，且稱可能仍偏保守（原話："we doubled it from $2 billion to over $4 billion"）
- 2026-08-12｜CEO｜product：Multi-rail 收入預期 CY27 上半年起跑（原話："revenue to ramp in the first half of calendar '27"）
- 2026-08-12｜CEO｜product：Thermadite XPU 散熱收入預期 CY27 下半年起跑（原話："revenue to begin ramping in the second half of calendar '27"）
- 2026-08-12｜CEO｜product：CPO 用於 scale-up 的收入時程為 CY27 下半年，管理層稱時程一貫（原話："start to flow in the second half of calendar '27"）
- 2026-08-12｜CEO｜customer：管理層稱 CPO 需求沒有遞延，反而被提前（原話："we've seen absolutely no pushout of CPO demand"）
- 2026-08-12｜CEO｜customer：FY27 訂單已全數排滿（原話："Fiscal '27 is basically completely booked out."）
- 2026-08-12｜CEO｜customer：客戶訂單已延伸到 CY28（原話："Customer orders now extend into calendar '28"）
- 2026-08-12｜CEO｜customer：管理層稱無需求衰減跡象（原話："no signs of attenuation in customer demand"）
- 2026-08-12｜CEO｜customer：LTA 含最低需求保證（take-or-pay）（原話："take-or-pay agreements"）
- 2026-08-12｜CEO｜customer：LTA 幾乎都載明協議價格，期間最長至本十年末（原話："the pricing is set for, I think, all or almost all"）
- 2026-08-12｜CEO｜customer：進口限制報導促使部分客戶來談製造選項與供給（原話："spurred some new customer demand and supply discussions"）
- 2026-08-12｜CEO｜customer：稱幾乎所有產品線都供給受限（原話："any product line we're not supply constrained on"）
- 2026-08-12｜CEO｜customer：漲價（含 LTA 內約定調價）為 $3B 季度驅動因素之一（原話："pricing improvements that we're driving"）
- 2026-08-12｜CEO｜competition：近期不會對外銷售 InP 雷射（原話："I don't see any time in the near future"）
- 2026-08-12｜CEO｜competition：長期仍有部分資料通訊收發器使用外部來源（原話："supported by external sources"）
- 2026-08-12｜CEO｜risk：進口限制報導被稱為臆測，公司認為若成真將受惠（原話："report is speculative at this point"）
- 2026-08-12｜CEO｜risk：工業部門其他市場持續疲弱（原話："continued weakness across broader industrial markets"）
- 2026-08-12｜CEO｜risk：目前主要限制是 InP 產出爬坡（逐字稿原句開頭疑有轉錄錯誤），組裝測試產能不受限（原話："We're really just constrained by the ramp of the"）

### 問答異常語氣（迴避／改口／保留）
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Vivek Arya：9 月季財測毛利率有何特殊因素、FY27 增量毛利率如何看｜答法：CFO 未給增量毛利率數字，改談成本與定價時程不一、新產品推升，並轉向營業費用已低於 18% 目標模型
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Meta Marshall：明年毛利率改善中良率、產品組合、定價各占多少｜答法：CFO 未拆分比重，改談 6 吋成本結構（4 倍產出、一半成本），CEO 補充 6 吋良率高於 3 吋
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Karl Ackerman：$3B 季度營收中 1.6T、OCS、multi-rail、積壓訂單、價格各占多少｜答法：CEO 列出驅動因素但未給任何分項金額或比重
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Karl Ackerman：CY28 LTA 的承諾量是否高於 CY27、近 90 天承諾量改善多少｜答法：CEO 稱各年供給一般遞增，但未給量化承諾數字或近 90 天變化
- COHR_Q4_2026_Earnings_Call_20260812.md｜問：Simon Leopold：毛利率目標（分析師引述過去 42.5%）更新，CEO 轉交 CFO｜答法：CEO 先稱進展良好後轉交；CFO 稱投資人日目標為 >42%，Q1 中點 40.5%，未給時間表

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 3 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 5 | 2 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 5 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260901","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 資料中心光互連需求結構性持續（DCC 段量＋mix 雙升，且四個新引擎陸續貢獻）","columns":{"2Y 驗證點":"DCC YoY 維持 >30%，OCS／CPO 開始認列營收","5Y 驗證點":"3.2T／多軌系統／熱管理接棒，DCC 段營收季度化突破 $30 億","10Y 驗證點":"光互連仍是 AI 算力擴張的物理必要層","數字門檻":"DCC YoY ≥ +30%；FY27 Q4 單季營收 >$30 億（管理層自訂目標）","來源":"Coherent 法說、2026-08-12 財報稿","漂移觸發條件":"連 2 季 TTM DCC YoY 跌破 +25% → 削弱"}},{"id":"H2","text":"毛利率結構性擴張持續（6 吋磷化銦成本結構＋定價優化＋新產品組合）","columns":{"2Y 驗證點":"Non-GAAP GM 站穩 40%+","5Y 驗證點":"GM 邁向管理層目標 >42%，營運槓桿放大 EPS","10Y 驗證點":"垂直整合維持結構性成本優勢","數字門檻":"Non-GAAP GM ≥ 39%（現 40.2%，Q1 FY27 guide 39.5-41.5%）","來源":"Coherent Q4 FY26 財報、法說","漂移觸發條件":"連 4 季 TTM GM 偏離 ≥ 5% → 削弱（5Y 假設）"}},{"id":"H3","text":"資本支出暴增係產能超前建置而非資本紀律鬆動，FY2027 內 OCF／FCF 應見回升軌跡","columns":{"2Y 驗證點":"FY2027 各季 OCF 較 FY26Q4 低點回升","5Y 驗證點":"FCF margin 回到正值並向歷史常態（3-4%）靠攏","10Y 驗證點":"資本配置紀律維持（無重大 M&A 失控、SBC 稀釋可控）","數字門檻":"FY2027 全年 OCF 由 FY26 的 $0.08B 轉正並成長","來源":"Coherent 10-K/10-Q、法說 capex 指引","漂移觸發條件":"FY2027 全年 OCF 未轉正 → 反轉（10Y 假設，因涉及資本紀律根本判斷提前列入反轉門檻）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"CPO 蠶食 pluggable：NVIDIA 自家 Spectrum-X Photonics 已於 2026 下半年進入商用部署（CoreWeave／Lambda／OCI 為早期客戶），若標準化與量產速度快於 Coherent 在 CPO socket 拿到的份額，DCC 段每季 pluggable 飯碗（現約 $16 億）可能被稀釋而 CPO 補不回缺口","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"NVIDIA CPO 部署滲透率 >30% 且 Coherent CPO 營收未同步補上 pluggable 流失"}},{"id":"R2","text":"AI 資本支出消化期：超大雲廠 capex 指引連續下修，同時 Coherent 自身超前建置的產能（FY26 資本支出 $11.1 億，capex/revenue 15.6%）若利用率不如預期，會同時打擊營收成長與 FCF 轉正時程","columns":{"對應假設":"H1／H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"連 2 季雲廠 capex 指引下修 >20%，或 FY2027 全年 OCF 仍未轉正"}},{"id":"R3","text":"Merchant 競爭、磷化銦原料成本與中國反制：中國 Innolight／Eoptolink 在 1.6T 世代的全球份額（約 50-70%）較 800G 世代（35-40%）不降反升；中國 2025 年 2 月起的磷化銦出口許可制度已使 6 吋晶圓價格上漲約 250%（約 $1,400→$5,000/片）；若 FCC 對中國光模組的進口禁令正式生效，不排除中國以磷化銦／鎵出口許可進一步收緊作為反制（中國官方已表態「必要時將回應」），使 Coherent 的「垂直磷化銦」原料成本曝險進一步惡化","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"連 4 季 GM 下滑（原料成本傳導），或 Coherent 在 1.6T 世代對主要客戶份額續降（sourced），或磷化銦出口許可再度收緊"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已達進場門檻，本欄示意持有期加碼觸發：GM連2季>41.5%或CPO/OCS單季合計營收破$300M","irr_base_pct":14.8,"ev5y_pct":88.9,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":5.1,"ev5y_pct":88.9,"irr_base_pct":14.8,"max_dd_pct":-60.0,"bull_5y_price":843.0,"bear_5y_price":168.0,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":"已達進場門檻，本欄示意持有期加碼觸發：GM連2季>41.5%或CPO/OCS單季合計營收破$300M","price_at_dd":277.83,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"COHR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Coherent Corp."},"oneliner":"AI 光通訊缺貨與多年長約讓 CY27 訂單近滿，毛利率目標上調到 45% 以上；但最新一季自由現金流 −8.68 億美元。股價 26 週跌 42% 後，FY29 共識兌現就有報酬，爭點在 CY28 以後的供需。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺雲端與 AI 客戶擴建光互連的錢，利潤卡在磷化銦雷射這一節：有自家雷射產能的廠商才拿得到單、守得住毛利。","reasoning":"Q1 FY27 營收 23.7 億美元，季增 16%、年增 50%（扣除已處分業務為年增 56%）。資料中心與通訊段占 82%，年增 79%，其中資料中心年增 85%、通訊年增 84%；工業段持平。非 GAAP 毛利率 40.6%、營業利益率 23.2%，GAAP 營業利益率 15.9%，兩者差 7.3 個百分點。Q2 財測營收 25.5～27.5 億美元、EPS 2.28～2.48 美元。對照 2026-08-12 CFO 財測，Q1 營收落在 22～24 億美元區間上半，EPS 2.09 美元高於 2.05 美元上緣。單點依賴在客戶：FY26 最大客戶占 20%（前兩年各 10%），第二大占 12%。另有非獨立研究頁稱某客戶占該段 25～35%，未核實。分部毛利率事實表未涵蓋。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi5_guidance_q2_fy2027_non_g"],"verdict_values":{"revenue_quality":"能見度高：CY27 訂單接近排滿，客戶開始下 CY28 的單，長約多到本十年底，幾乎每份都有預付或 NRE。要打折的地方有兩個：前兩大客戶占 FY26 營收 32%；2026-08-12 CEO 說長約含 take-or-pay，11-04 改以高品質長期預測描述，最低承諾比例沒有數字。","unit_econ_note":"Q1 非 GAAP 毛利率季增 37 個基點、年增 184 個基點，CFO 歸因於定價優化、投入成本下降與良率提升。內部與外部磷化銦用量比例一年沒變（CEO 11-04），6 吋的成本好處大多還沒進損益。SBC 占營收 3.1%。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"低","fingerprint":"需求有長約、毛利率上行，但 FY23、FY24 仍虧損，FY26 自由現金流為負，品質還沒有被現金證明，盈餘也仍受 AI 資本支出週期主導。"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高。幾乎所有資料中心產品線仍受磷化銦限制（2026-08-12 CEO），FQ2 資料中心訂單出貨比超過 4 倍；但公司 CY27 底前內部產能再翻倍以上，且已規劃 2027 年後續擴，法說上已有分析師問 CY28 過剩。判斷擴張期的依據是訂單與產能，不是股價。4 倍訂單出貨比可能含重複下單，事實表未涵蓋拆分。","bargaining":{"up":"基板供應商超過 5 家，多家已簽長約，CEO 稱足以支應 CY27 擴產；公司自身的中國來源比例事實表未涵蓋。","down":"前兩大客戶占 32%，買方議價力上升；缺貨讓公司目前仍能調價，長約價格多已約定。","geo":"實體清單與 232 關稅調查不利；FCC 若禁中國光模組對公司有利，但僅單一來源，公司 2026-08-12 也稱該報導屬臆測。"},"profit_pool_dir":"往上游雷射與整合光學移動；雷射產能鬆動後，利潤可能回流模組廠與客戶。五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"2026 年 AI 光收發模組市場","value":"約 260 億美元（TrendForce，次級來源）"},{"item":"2030 年資料中心與通訊可及市場","value":"約 900 億美元（管理層 11-04 估計，未獨立驗證）"},{"item":"其中 CPO、NPO、晶片間光互連","value":"約 300 億美元（2030 年，管理層估計）"},{"item":"OCS 可及市場","value":"至少 40 億美元（2030 年，管理層估計）"},{"item":"公司滲透率","value":"23.7 億美元×82%×4≈78 億美元年化，對 900 億美元約 9%"},{"item":"五年營業利益池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河仍在擴大，來源是磷化銦垂直整合與多年長約；但擴大幅度有多少來自缺貨還分不開，等級只給 B。","reasoning":"優勢在雷射端：內部磷化銦產能較原計畫提前一季翻倍，CY27 底前再翻倍以上；400 毫瓦 CW 雷射 CEO 稱只看到一家競爭者；新簽 200 億美元、五年的 PhotonLink 長約。弱點在利潤率：TTM 毛利率 38.16%，低於 Lumentum 的 45.91%；營業利益率 14.11% 對 23.35%；自由現金流利潤率 −23.28% 對 9.52%。同業 ROIC 序列事實表未涵蓋，無法證明對最強同業的差距在收斂，所以綜合評分不到 8。向上判斷的反例有三：內部雷射比例一年未變、毛利率提升相當部分來自缺貨期定價、2.4T 世代有單一來源稱中國廠拿 60～70%。當期 ROIC 因投入資本未涵蓋無法計算，增量報酬用 FY26 損益與自由現金流代理，推導見公式欄。","fact_refs":["f_peer_cohr_gross_margin_pct","f_peer_cohr_operating_margin_pct","f_peer_cohr_fcf_margin_pct","f_peer_lite_gross_margin_pct","f_peer_lite_operating_margin_pct","f_peer_lite_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"自家 6 吋磷化銦雷射產能、完整光鏈產品組合與多年長約。CFO 2026-08-12 稱 6 吋產出為 3 吋 4 倍、成本約一半；CEO 11-04 稱德州與瑞典 6 吋良率高於 3 吋。客戶願意預付並簽到本十年底，轉換成本落在重新認證與設計卡位。","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：內部磷化銦產能提前一季翻倍。定價面擴大：Q1 毛利率年增 184 個基點，定價優化是主要來源之一，目標由 42% 以上上調到 CY28 底前 45% 以上。反例：內部雷射比例一年未變，成本優勢尚未進損益；Lumentum 利潤率仍明顯較高。若 2027 年中前內部比例仍未上升，或出現主要客戶份額下滑的可靠來源，方向改為持平。","competitor_notes":[{"name":"Lumentum","strategy_note":"毛利率與營業利益率都高於公司，是最強對手；擬與 Marvell 合併，公司 DSP 採購來源事實表未涵蓋，合併後的供應影響待查。"},{"name":"Ciena","strategy_note":"營業利益率與公司接近、自由現金流為正；公司在 scale-across 往線卡與完整方案走，與設備商客戶可能產生通路衝突。"},{"name":"AAOI","strategy_note":"毛利率 28.92%、營業利益率為負，現金流大幅流出，目前還不構成成本威脅。"},{"name":"MACOM","strategy_note":"毛利率 57.13%，所處環節與公司互補多於正面競爭，不宜作為利潤率基準。"},{"name":"Innolight","strategy_note":"單一來源稱將拿下 2.4T 世代 60～70% 出貨；若美國限制中國模組則受衝擊，雙向都未定案。"}],"peer_na_reason":"同業 ROIC 序列事實表未涵蓋，改用毛利率、營業利益率與自由現金流利潤率比較。","threats":[{"level":"🔴","text":"大客戶向後整合或自製 CPO 光源雷射。10-K 自承可能誤判客戶向後整合的能力；CY2028 以後自製的說法來自非獨立研究頁，未核實。","p":"20%","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"]},{"level":"🔴","text":"CPO 與 NPO 替代可插拔收發模組。公司有 PhotonLink 對沖，但內容價值與份額可能和模組時代不同。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"中國模組廠在下一代產品份額擴大，2.4T 單一來源估計公司僅 20～30 萬件。","p":"30%","evidence_refs":["competitive_share_entrants#4"]},{"level":"🔴","text":"Lumentum 擬併 Marvell，對手可能同時掌握雷射與晶片；CEO 主張客戶更需要獨立供應商，尚無訂單數據驗證。","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×低周轉（暫定，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"用光取代銅線是頻寬與距離的實際需要，但採購量取決於 AI 資本支出；法說已有分析師提出資料中心融資與建置許可疑慮。代理讀數：CY27 訂單近滿。"},{"item":"決策層級","level":"🟢","text":"替代要看單一插槽與客戶認證。長約多到本十年底並含預付，200 億美元長約為期五年。反例：2026-08-12 被問 CY28 承諾量時沒有給數字。"},{"item":"價值鏈分配","level":"🟡","text":"缺貨期利潤往雷射端移，但前兩大客戶占 32%，且有能力與動機自製或扶植第二來源，產能鬆動後分配可能反轉。"},{"item":"社會容忍度","level":"🟢","text":"產品是企業基礎建設零組件，消費者不直接付費，價格上限主要來自客戶議價；出口管制與關稅另列風險。"}],"roiic":"16.9%","reinvest_rate":"241%","endo_ceiling":40.7,"formula_note":"代理估算，D&A 與營運資金明細事實表未涵蓋。FY26 營業利益增量＝7,118×12.67%−5,810×9.21%≈367 百萬美元；稅率取財測中位 19%，稅後增量≈297；NOPAT≈731；淨再投資以 NOPAT−FCF≈731+1,031＝1,761 代理；增量 ROIC≈16.9%，再投資率≈241%，內生上界≈40.7%。再投資率超過 100% 靠舉債、處分資產與客戶預付，只用自有現金時上界約 17%。資本支出領先營收 1～2 年，這個增量報酬可能低估；CFO 稱 18 個月回收，目前無法驗證。"}}}},"q3_growth":{"verdict":"五年後仍有跑道：公司年化營收約占管理層 2030 年市場估計的 9%，整合光學已有長約；但以目前速度約四年就到 30% 滲透率，倍數不宜給高。","reasoning":"成長以量為主，價與產品組合為輔，沒有併購或回購。共識 EPS FY27 9.42 美元、FY29 19.13 美元，兩年年化約 42.5%；共識營收 FY27 111.6 億美元、FY28 155.0 億美元，年增 38.9%。內生上界 40.7%，缺口約 1.8 個百分點，可歸因於毛利率與營業費用槓桿。基本情境 EPS 年化約 19%（9.42→22.5 美元），在上界之內，但高於只用自有現金時的約 17%，代表仍需外部資金或客戶預付。CY27 前的跑道有訂單支撐，五年後的判斷依賴管理層的市場規模估計。滲透率推算：78 億美元以年增約 40% 成長，到 270 億美元約需 3.7 年。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主（1.6T、800G、scale-across、PhotonLink、OCS），價與產品組合為輔；沒有併購或回購貢獻。","runway_years":4,"runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段內生上界 40.7%（增量 ROIC 約 16.9%×再投資率約 241%）；共識 FY27→FY29 EPS 年化約 42.5%，超出約 1.8 個百分點，歸因於毛利率與營業費用槓桿。","segments":[{"item":"資料中心與通訊段","value":"Q1 占營收 82%，季增 21%、年增 79%"},{"item":"資料中心","value":"Q1 季增 17%、年增 85%"},{"item":"通訊","value":"Q1 季增 34%、年增 84%；scale-across 超過 2 億美元"},{"item":"工業段","value":"Q1 pro forma 季比與年比持平，訂單強，管理層預期本季恢復成長"},{"item":"PhotonLink","value":"管理層目標：3 月季超過 1 億美元，CY27 底前每季超過 2.5 億美元"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":false,"evidence":"Q1 年增 184 個基點"},{"name":"核心市占近 12 個月縮減","lit":false,"evidence":"沒有可靠份額序列，2.4T 僅單一來源，列為資料缺口"},{"name":"主力產品提價後銷量下滑","lit":false,"evidence":"定價優化期間量仍成長"},{"name":"EPS 成長顯著高於營收成長","lit":true,"evidence":"FY27→FY28 共識 EPS 年增 48.3%、營收 38.9%，差 9.4 個百分點；Q1 年增 80% 對 50%"},{"name":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"FY26 為負、FY25 約 3.9 倍，尚未連 2 年；FY27 續負就亮燈"},{"name":"SBC／營收超過 5% 且逐年上升","lit":false,"evidence":"Q1 為 3.1%"},{"name":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"CPO 有替代風險，但公司已取得 PhotonLink 長約"},{"name":"產業估值倍數 3 年系統性下移","lit":false,"evidence":"事實表未涵蓋"},{"name":"維持性資本支出占 FCF 超過 60%","lit":false,"evidence":"FCF 為負，無法計算"},{"name":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"資本支出仍在增加"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本幾乎全押擴產，最新一季自由現金流 −8.68 億美元；稀釋可控，併購與回購沒有可評紀錄，配置能力要等現金回收才算數。","reasoning":"FY26 自由現金流 −10.3 億美元、淨利 8.05 億美元，轉換率為負。Q1 FY27 營業現金流 −92.7 百萬美元，資本支出 775.5 百萬美元，占營收 32.7%，CFO 說本季還會再增加。現金由 25.9 億美元降到 23.4 億美元，只少 2.5 億美元，差額約 6.2 億美元的來源事實表未涵蓋；槓桿由 0.7 倍升到 1.1 倍。FY26 償債 5.13 億美元，股利與回購沒有紀錄。CFO 稱資料中心投資約 18 個月回收，尚無現金流驗證。事實表現金 17.5 億美元與法說 23.4 億美元不同，淨負債可能高估約 5.9 億美元，約占 EV 1.4%，不改變結論。","fact_refs":["f_kpi3_free_cash_flow_capex","f_kpi4_sbc_non_gaap","f_net_debt_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事實表未涵蓋過去併購投入與報酬；近 12 個月沒有併購完成項目，只有處分航太國防與慕尼黑業務。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"法說與事實表都沒有回購紀錄，現金優先用於擴產與還債。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q1 SBC 73.2 百萬美元×4≈293，除以市值 37,976≈0.77%／年，低於 1.5%；實際股數變化序列事實表未涵蓋。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠內部擴產與長約，不靠併購；股利與回購沒有紀錄，沒有可展開項目。"}}}},"q5_valuation":{"verdict":"現價只要求 FY29 共識大致兌現、之後不再快速成長。我相信到 FY28 的數字，FY29 以後打折看待。","reasoning":"現價 192.81 美元，FY1 本益比 20.47 倍，FY2 13.80 倍。以 10% 要求報酬、15 倍終端本益比反推，FY31 EPS 要約 20.7 美元，只比 FY29 共識 19.13 美元高 8%。若營收停在 FY28 共識 155 億美元、營業利益率回到 18%，未計利息的 EPS 約 11.5 美元，16 倍約 184 美元，接近現價，代表價格已計入部分高峰疑慮。基本情境 FY29 EPS 17.5 美元，低於共識 8.5%。12 個月以 FY28 EPS 14.0 美元×18 倍得 252 美元，上行 30.7%；24 個月以 FY29 EPS 17.5 美元×17 倍得 297.5 美元，上行 54.3%。FY1 共識 9.42 美元可能偏舊：Q1 實績 2.09 美元加 Q2 財測中位 2.38 美元已達 4.47 美元，下半年每季只需 2.48 美元，約等於 Q2 財測上緣，而管理層指向 FY27 底單季 30 億美元以上。FY28 共識以 19% 稅率與 197 百萬股反推，稅前利益率約 22%，低於 Q1 非 GAAP 營業利益率 23.2%，可能還沒計入毛利率擴張，也可能混用口徑。賣方目標價僅見德銀 400 美元（2026-09-01），均值與全距事實表未涵蓋，不作依據。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_rev_consensus_fy2_m","f_shares_diluted_m","f_pe_current","f_ps_percentile","f_ev_s_percentile"],"verdict_values":{"valuation":{"basis":"FY1 共識 EPS 的前瞻本益比，搭配隱含預期反推；trailing 本益比含處分利得且分位只有一個年度端點，不採用。","tier":"光通訊零組件與雷射","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比；系統商與類比晶片也不宜跨層當錨。"},"fwd_pe":20.47,"peg":0.48,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"FY1 本益比 20.47 倍（192.81÷9.42）；FY1→FY3 EPS 年化約 42.5%，PEG 約 0.48，只作參考。主要依據是隱含預期：10% 報酬率與 15 倍終端本益比下，FY31 EPS 約 20.7 美元即可。基本情境五年年化約 14.7%，全部來自盈餘成長，倍數由 20.47 倍降到 17 倍。反例：自由現金流為負，非 GAAP 口徑排除 SBC 與攤提；若營業利益率回到 18%，現價接近合理價，沒有明顯便宜。五年分位事實表未涵蓋，只有年度端點分位（P/S 44.1、EV/S 41.2），因此留空。","upside_short_pct":30.7,"upside_mid_pct":54.3,"denominator_disputed":false,"denominator_note":"FY1 與 FY2 有訂單與長約支撐，當期分母不是爭點；爭點在 FY29 以後能否持續，已放進下行情境。trailing 分母含處分利得（FY26 慕尼黑處分利得 1.24 億美元），因此改用前瞻錨定。"}}},"q6_how_wrong":{"verdict":"最可能看錯 CY28 以後的定價與客戶承諾：缺貨期的條件不會自動延續。","reasoning":"最強的空方數字是 Q1 自由現金流 −8.68 億美元與前兩大客戶占 32%。壓力測試 5 項過 3 項：最大客戶量減半仍獲利、毛利率退回 36% 仍獲利、出口管制加嚴但未斷料仍可經營，這三項通過；AI 資本支出下滑 30% 時 FY28 EPS 約少六成，不通過；現金 23.4 億美元只夠支應約 2.7 季目前的流出速度，循環額度事實表未涵蓋，不通過。FY31 基本情境敏感度：營業利益率每差 1 個百分點，EPS 約差 0.84 美元，目標價約差 14 美元；股數多 5%，目標價約少 18 美元；終端本益比每差 2 倍，目標價約差 45 美元。歷史最大回撤與訴訟金額事實表未涵蓋。2026-08-12 法說管理層沒有正面回答增量毛利率、毛利率改善拆分、30 億美元季度的營收組成、CY28 承諾量，毛利率目標時間表則到 11-04 才補上。","fact_refs":["f_kpi3_free_cash_flow_capex","f_week26_return_pct","f_ma_w104","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"現金轉換未驗證"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":9.42,"pe":20.47,"basis":"FY1（FY2027E）共識 EPS 9.42 美元，股價 192.81 美元；終端倍數同為當年度 EPS 口徑。事實表未涵蓋同業前瞻本益比，只能對照公司自身 FY1 20.47 倍與 FY2 13.80 倍。"},"eps":{"bull":[10.6,16.5,23.5,30.0,36.0],"base":[10.0,14.0,17.5,20.0,22.5],"bear":[9.2,11.5,8.5,7.0,8.0]},"pe":{"bull":21,"base":17,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-60,"hi":-45,"basis":"Bear 谷底 FY30 EPS 7 美元×12～16 倍約 84～112 美元，相對 192.81 美元跌 42%～56%，加上融資壓力的尾部取 −60%。上緣取回到 250 週均線 105.98 美元，約 −45%。公司歷史最大回撤事實表未涵蓋，本輪 26 週已跌 42.49%。","trigger_time":null},"basis":{"bull":"FY31 營收約 320 億美元，約占管理層 2030 年 900 億美元市場 30% 再加工業段；營業利益率約 30%，PhotonLink 成為數十億美元產品線，股數約 210 百萬股。","base":"FY28 貼近共識，FY29 較共識低 8.5%，之後成長放緩到一成多；FY31 營收約 220 億美元、營業利益率約 27%，股數約 212 百萬股。","bear":"CY28 起 AI 資本支出消化加上磷化銦過剩，長約部分重談，FY30 EPS 谷底 7 美元，毛利率退回 36% 左右。機率 30% 的依據：再投資率超過 100%、前兩大客戶占 32%、共識成長超過內生上界。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"前兩大客戶 FY26 占 32%，FQ2 資料中心訂單出貨比超過 4 倍，法說上有分析師直接問 CY28 磷化銦過剩與資料中心融資。","assumption":"長約與預付在需求放緩時仍會被客戶照約履行。","consequence":"最大客戶量減半時 FY28 EPS 約少 20%，產能與債務不會同步下降，股價可能回到 250 週線 105.98 美元附近，虧損接近 50%。","ruling":"採納為下行情境，機率 30%。CEO 說看不到過剩的期限只到 CY28，且是賣方單方說法，不足以排除風險。","watch":"剩餘履約義務、合約負債、主要客戶占比與內部磷化銦稼動率。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0"],"fact_refs":["f_ma_w250"]},{"view":"論點成功但股東經濟變差","evidence":"Q1 營收年增 50%，但營業現金流 −92.7 百萬美元、資本支出 775.5 百萬美元；槓桿由 0.7 倍升到 1.1 倍，本季資本支出還要增加。","assumption":"資料中心投資約 18 個月回收（CFO 2026-08-12）。","consequence":"需求成立但現金被擴產吃掉，公司必須舉債或增資，每股價值被稀釋。","ruling":"採納。基本情境股數由 197 百萬股升到約 212 百萬股，並另設增資與槓桿的減碼門檻。","watch":"營業現金流、資本支出、長期負債與增資公告。","evidence_refs":["supply_demand_durability#2"],"fact_refs":["f_kpi3_free_cash_flow_capex"]},{"view":"價格已反映太多","evidence":"跌 42% 後仍是 FY1 20.47 倍、trailing 39.92 倍，而自由現金流為負。","assumption":"FY29 共識 19.13 美元大致可達成。","consequence":"若 FY29 EPS 只有共識七成（13.4 美元），15 倍約 201 美元，五年幾乎沒有報酬。","ruling":"反駁已過度定價：現價只要求 FY29 水準能維持。但採納另一點：已跌 42% 本身不是安全邊際。","watch":"FY2、FY3 共識修正方向與非 GAAP 毛利率。","evidence_refs":[],"fact_refs":["f_pe_current","f_fwd_pe_latest","f_week26_return_pct"]},{"view":"論點失敗","evidence":"產業層面磷化銦基板供應集中，中國出口管制帶來不確定；對美鎵鍺銻出口禁令的暫停期到 2026-11-27；10-K 提到 232 調查與實體清單風險。","assumption":"超過 5 家基板供應商足以分散風險。","consequence":"6 吋擴產若延遲，毛利率路徑與 2027 年放量都會受影響；若管制在擴產承諾後加嚴，可能認列庫存與採購義務費用。","ruling":"部分採納。CEO 稱 CY27 擴產基板已確保，但沒有揭露中國來源比例，因此保留損益層監測，不預測政策結果。","watch":"暫停期是否延長，單季毛利率下降是否達 100 個基點且公司歸因於管制或關稅。","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 277.83 → 本次 192.81（-30.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=277.83","side_b":"本次 price_at_dd=192.81","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 277.83 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 277.83 美元：Bull 價 843、Bear 價 168，五年期望值 +88.9%，基準年化 14.8%，不對稱比 5.1","side_b":"本次情境、股價仍用 277.83 美元：Bull 價 756、Bear 價 112，五年期望值 +42.1%，基準年化 6.6%，不對稱比 2.4","ruling":"先換情境、股價不動：五年期望值少 46.8 個百分點，基準年化少 8.2 個百分點。不對稱比由 5.1 變為 2.4。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 277.83 美元：五年期望值 +42.1%，基準年化 6.6%，不對稱比 2.4","side_b":"本次情境、股價 192.81 美元：五年期望值 +104.7%，基準年化 14.7%，不對稱比 5.81","ruling":"再換股價、情境不動：起點價下跌 30.6%，五年期望值多 62.6 個百分點，基準年化多 8.1 個百分點，不對稱比由 2.4 升到 5.81。合計五年期望值比前份多 15.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與進場結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 277.83 美元，估值偏便宜，結論進場。","side_b":"本次股價 192.81 美元，FY1 本益比 20.47 倍，估值仍偏便宜。","ruling":"估值結論維持，差別主要來自股價下跌 30.6%；FY1 共識三個月只變動 −0.42%。進場結論與倉位角色由本次均線狀態與情境結果決定。","evidence_level":"高","settle_metric":"FY1、FY2 共識 EPS 修正與股價相對 52 週線位置","if_then":["若股價續漲但毛利率與現金流未改善，則不追","若股價下跌但訂單與毛利率無損，則分批反買"],"evidence_refs":[]},{"axis":"價值陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份為綠色，認定資本支出暴增是超前建置。","side_b":"本次為黃色：Q1 自由現金流 −8.68 億美元，FY27→FY28 共識 EPS 成長高於營收成長 9.4 個百分點。","ruling":"下調一級。現金轉換尚未驗證，FY27 全年若續為負，第二個衰退訊號會亮燈。","evidence_level":"高","settle_metric":"FY27 全年營業現金流","if_then":["若 FY27 全年營業現金流高於 0.8 億美元，則回到綠色","若 FY27 全年營業現金流為負，則減碼至一半"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"評級、護城河方向、跑道與公司類型","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","archetype"],"side_a":"前份綜合評級 B、護城河向上、五年後跑道寬、屬品質複利成長。","side_b":"本次四項不變：磷化銦產能提前、毛利率目標上調、200 億美元長約支持方向；公司類型的信心給低。","ruling":"維持。新證據支持方向，但自由現金流與同業利潤率差距讓等級停在 B。","evidence_level":"中","settle_metric":"內部磷化銦比例、毛利率與主要客戶份額","if_then":["若 2027 年中前內部比例仍未上升，則護城河方向改為持平"],"evidence_refs":[]},{"axis":"機率、回撤與循環位置","cause":"方法變動","prior_field":["max_dd_pct","p_bull_pct","p_bear_pct","cycle_position"],"side_a":"前份 Bull 30%、Bear 30%，最大回撤 −60%，循環位置留空。","side_b":"本次 Bull 25%、Base 45%、Bear 30%，回撤區間 −60%～−45%，循環位置仍留空。","ruling":"Bull 下調 5 點，因 FY29 以後依賴 CY28 後的持續性，共識也超過內生上界。回撤改用區間表達。本次仍不按循環股處理，但把 CY28 過剩放進下行情境。","evidence_level":"中","settle_metric":"CY27 底毛利率與雷射報價","if_then":[],"evidence_refs":[]},{"axis":"加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"已達進場門檻，本欄示意持有期加碼觸發：GM連2季>41.5%或CPO/OCS單季合計營收破$300M","side_b":"Q2 FY27 毛利率 ≥41.5% 且營業現金流轉正才加碼第二批；或跌破 181 美元且訂單與毛利率無損時分批反買。","ruling":"加入現金流條件，因 Q1 自由現金流明顯惡化；OCS 未單獨揭露，舊條件的合計金額無法驗證，改看 PhotonLink 3 月季是否超過 1 億美元。","evidence_level":"高","settle_metric":"Q2 FY27 毛利率與營業現金流","if_then":["若兩項同時達成，則加碼第二批"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics","triggers"],"side_a":"前份未設清倉與減碼的量化門檻；毛利率下限為 Non-GAAP GM ≥ 39%。","side_b":"減碼：資料中心與通訊段年增連 2 季低於 30%、毛利率連 2 季低於 40%、FY27 全年營業現金流為負，或增資超過 5%。清倉：唯一致命事件發生且毛利率連 2 季年減。","ruling":"補上數字門檻。毛利率下限由 39% 提高到 40%，因 Q2 財測下緣為 40%，再低就代表擴張論點失效。","evidence_level":"高","settle_metric":"每季財報","if_then":["若任一減碼條件成立，則減碼至一半","若清倉條件成立，則清倉"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點欄位為空（null）。","side_b":"前兩大客戶之一在 CY28 前下修或延後長約承諾量（含改用自製雷射或轉單）。","ruling":"本輪補上。依敏感度排序，最大客戶全部流失的影響約占 FY28 共識 EPS 的 41%，是單一項目中最大。","evidence_level":"中","settle_metric":"主要客戶占比、剩餘履約義務與合約負債","if_then":["若確認下修或延後，則一週內減碼一半"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"長約的約束力","cause":"新證據","prior_field":null,"side_a":"CEO 2026-08-12：長約含 take-or-pay，價格幾乎都已約定。","side_b":"CEO 2026-11-04：強調高品質長期預測與預付，200 億美元只說總值；2026-08-12 被問 CY28 承諾量也沒有給數字。","ruling":"屬程度差異，採保守解讀，視為部分約束，基本情境未把 200 億美元全額算入。","evidence_level":"中","settle_metric":"10-Q 剩餘履約義務與合約負債","if_then":["若兩項連 2 季增加，則 Bear 機率下調到 25%","若客戶延後且公司修改長約條款，則減碼至一半"],"evidence_refs":[]},{"axis":"CY28 磷化銦供需","cause":"新證據","prior_field":null,"side_a":"CEO 2026-11-04：看不到 CY28 過剩，公司內部雷射全部自用，外部過剩不影響。","side_b":"分析師提到 CY28 EML 過剩的討論；公司 CY27 底前內部產能再翻倍以上，且規劃 2027 年後續擴。","ruling":"方向相反，今天沒有決勝數據，不可裁決至 2027 年底。全部自用的說法不足以免疫：外部雷射降價會縮小內部成本優勢，客戶也會壓低模組價格。因此保留 30% 下行情境，不當作風險已解除。","evidence_level":"中","settle_metric":"非 GAAP 毛利率、EML 報價與內部雷射比例","if_then":["若 2027-12 季毛利率 ≥43% 且內部比例上升，則加碼至倉位上限","若 EML 報價連 2 季下跌且毛利率連 2 季年減，則減碼一半","若股價續漲但證據未到，則不追"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#4"]},{"axis":"毛利率擴張的來源","cause":"新證據","prior_field":null,"side_a":"CFO 2026-11-04：毛利率擴張具結構性，也受益於 6 吋轉換。","side_b":"CEO 同場：內外部雷射比例一年沒變，6 吋最大的好處還在後面；本季主因是定價、投入成本與良率。","ruling":"屬程度差異。目前提升以定價為主，尚未證明是結構性；45% 目標依賴未來比例轉換與新產品。依管理層歸因歸類，分項金額未揭露。","evidence_level":"中","settle_metric":"內部雷射比例與非 GAAP 毛利率","if_then":["若 2027-06 季毛利率低於 42%，則停止加碼"],"evidence_refs":[]},{"axis":"scale-up 收入時程","cause":"新證據","prior_field":null,"side_a":"CEO 2026-08-12：CPO scale-up 收入 CY27 下半年開始，時程一貫。","side_b":"CEO 2026-11-04 問答：接近 CY27 底開始，NPO 可能到 2028 年初。","ruling":"小幅後移，不影響 FY27，但會影響 PhotonLink 放量節奏，先記錄，不調整情境。","evidence_level":"中","settle_metric":"PhotonLink 單季營收","if_then":["若 CY27 底前每季未達 2.5 億美元，則停止加碼"],"evidence_refs":[]},{"axis":"共識與實績節奏","cause":"新證據","prior_field":null,"side_a":"FY1 共識 9.42 美元，近三個月 −0.42%，最新快照無變動。","side_b":"Q1 實績加 Q2 財測中位已達 4.47 美元，下半年每季只需 2.48 美元，而管理層目標 FY27 底單季 30 億美元以上。","ruling":"共識可能偏舊，或口徑不一，基本情境 FY27 取 10.0 美元。這只影響近一年，對五年報酬的影響小於 FY29 持續性。","evidence_level":"中","settle_metric":"下一次共識快照","if_then":[],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭惡化：單一來源稱中國廠拿 2.4T 世代 60～70%，Lumentum 擬併 Marvell。","side_b":"結構轉好：CY27 訂單近滿、長約到本十年底；其他結構變數包括 232 關稅與出口管制。","ruling":"雙向拉鋸。需求與合約面轉好有公司揭露支持，競爭惡化目前多為單一來源或尚未落地的交易。","evidence_level":"中","settle_metric":"主要客戶份額與毛利率","if_then":[],"evidence_refs":["competitive_share_entrants#4"]},{"axis":"現在就賣的最強論證","cause":"新證據","prior_field":null,"side_a":"賣方論點：每季自由現金流流出近 9 億美元，資本支出還在升，缺貨與預付常見於週期後段；股價跌破 52 週線，趨勢已轉弱。","side_b":"持有論點：CY27 訂單近滿，毛利率目標上調，現價只要求 FY29 共識維持。","ruling":"不賣，但不一次買足。分批以現金流與毛利率的下一個數據點為條件，下行 30% 機率已反映在情境。","evidence_level":"中","settle_metric":"Q2 FY27 營業現金流","if_then":["若 Q2、Q3 營業現金流皆為負且資本支出續增，則減碼至一半"],"evidence_refs":["supply_demand_durability#2"]}],"triggers":[{"n":1,"text":"第二批進場：Q2 FY27 財報確認毛利率與現金流。","type":"估值rearm","maps_to":"H2／H3","metric":"非 GAAP 毛利率、營業現金流","threshold":"毛利率 ≥41.5% 且營業現金流 >0","action":"加碼第二批至目標倉位 2/3","source_freq":"公司季報，每季","date":"2027-02"},{"n":2,"text":"第三批進場：PhotonLink 開始放量。","type":"加碼","maps_to":"H1／H2","metric":"PhotonLink 單季營收與非 GAAP 毛利率","threshold":"3 月季營收 >1 億美元且毛利率 ≥42%","action":"加碼至倉位上限","source_freq":"公司季報，每季","date":"2027-05"},{"n":3,"text":"驗證 FY27 底單季營收目標。","type":"假設驗證","maps_to":"H1","metric":"FY27 Q4 營收","threshold":"≥30 億美元","action":"未達則停止加碼","source_freq":"公司季報，每季","date":"2027-08"},{"n":4,"text":"驗證資本支出是否開始回收。","type":"假設驗證","maps_to":"H3","metric":"FY27 全年營業現金流","threshold":">0.8 億美元","action":"未達則減碼至一半","source_freq":"10-K，每年","date":"2027-08","evidence_refs":["supply_demand_durability#2"]},{"n":5,"text":"中國對美鎵鍺銻出口禁令暫停期到期。","type":"風險","maps_to":"R5","metric":"暫停期是否延長、下一季毛利率","threshold":"到期未延長，且下一季毛利率季減 ≥100 個基點","action":"減碼三分之一","source_freq":"官方公告與公司季報","date":"2026-11-27","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2"]},{"n":6,"text":"關稅與出口管制是否吸收失敗。","type":"風險","maps_to":"R5","metric":"非 GAAP 毛利率","threshold":"單季下降 ≥100 個基點且公司歸因於關稅或出口管制","action":"停止加碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":7,"text":"前兩大客戶之一下修或延後長約承諾量。","type":"Single Thing","maps_to":"R1","metric":"主要客戶占比、剩餘履約義務與合約負債","threshold":"確認下修或延後，或最大客戶占比由 20% 降到 10% 以下","action":"一週內減碼一半","source_freq":"10-K、10-Q 與法說","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":8,"text":"融資壓力超過可接受範圍。","type":"減碼","maps_to":"R3","metric":"增資比例與槓桿倍數","threshold":"股權增資超過 5%，或槓桿超過 2 倍","action":"減碼至一半","source_freq":"8-K 與公司季報","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":9,"text":"客戶承諾與毛利率同時失守。","type":"清倉","maps_to":"H1／H2","metric":"長約變動與非 GAAP 毛利率","threshold":"唯一致命事件已發生，且毛利率連 2 季年減","action":"清倉","source_freq":"公司季報與法說","date":null},{"n":10,"text":"下一次財報後重跑完整研究。","type":"複審日期","maps_to":"H1／H2／H3","metric":"Q2 FY27 財報","threshold":"財報公布","action":"更新情境與倉位條件","source_freq":"每季","date":"2027-02"}],"kill_metrics":[{"metric":"資料中心與通訊段營收年增率","bear_threshold":"連 2 季低於 30%","window":"每季","source":"公司財報與法說","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"連 2 季低於 40%","window":"每季","source":"公司財報","last_status":"ok"},{"metric":"FY27 全年營業現金流","bear_threshold":"全年為負","window":"至 2027-08 年報","source":"10-Q、10-K 現金流量表","last_status":"warning"},{"metric":"最大客戶占營收比與長約承諾","bear_threshold":"承諾下修或延後，或占比由 20% 降到 10% 以下","window":"每季至 CY28","source":"10-K、10-Q、法說","last_status":"unknown"},{"metric":"股權增資與槓桿倍數","bear_threshold":"增資超過 5%，或槓桿超過 2 倍","window":"每季","source":"8-K 與公司財報","last_status":"ok"}],"evidence_dismissed":[{"ref":"end_markets#1","reason":"這筆 10% 下滑來自航太國防與慕尼黑業務處分，屬合併範圍改變；Q1 FY27 pro forma 季比與年比持平，不代表同口徑需求下滑。"},{"ref":"major_events#2","reason":"這是原告律所徵求當事人的公告，查無案號、求償金額或法院程序，無法作為可量化的風險證據。"},{"ref":"lawsuit_class_action#0","reason":"來源為律所調查公告，搜尋未找到已提起的集體訴訟案號，也沒有受影響金額。"}],"action_conditions":{"rearm_trigger":"Q2 FY27 毛利率 ≥41.5% 且營業現金流轉正才加碼第二批；或跌破 181 美元且訂單與毛利率無損時分批反買。","exec_line":"首批三分之一可在 192.81 美元附近建立；第二批等 2027-02 財報確認毛利率與現金流；第三批等 PhotonLink 3 月季超過 1 億美元。證據未到前，站回 271 美元也不追價。","holding_cap":"總資產 5% 以內；槓桿超過 2 倍或毛利率低於 40% 時降到 3% 以內。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 26 週 −42% 定價 CY28 過剩與融資風險，但 CY27 訂單近滿、長約多含預付，現價只要求 FY29 共識大致兌現且之後不再快速成長。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"進場","prior_role":"衛星"},"thesis":{"H":[{"id":"H1","text":"AI 光互連需求到 FY28 有訂單與長約支撐，資料中心與通訊段維持高成長。","2y":"FY27 Q4 單季營收超過 30 億美元，FY28 內出現單季 40 億美元。","5y":"PhotonLink 成為數十億美元產品線，接替可插拔模組放緩的部分。","10y":null,"threshold":"FY27 Q4 營收 ≥30 億美元；資料中心與通訊段年增 ≥30%","source":"公司季報與法說，每季","drift_rule":"段營收年增相對 30% 門檻連 2 季偏離 5% 以上（低於 28.5%）為削弱；連 3 季偏離 10% 以上（低於 27%）為反轉。"},{"id":"H2","text":"毛利率擴張由定價轉向成本：內部 6 吋磷化銦比例上升，單季非 GAAP 毛利率超過 45%。","2y":"2027-06 季毛利率 ≥42%，內部雷射比例開始上升。","5y":"CY28 底前單季超過 45%，新產品占比提高後仍能維持。","10y":null,"threshold":"非 GAAP 毛利率不低於 40%；CY28 底前單季 >45%","source":"公司季報與法說，每季","drift_rule":"TTM 毛利率連 4 季低於規劃路徑 5% 以上為削弱，連 6 季低於路徑 10% 以上為反轉。"},{"id":"H3","text":"這輪資本支出能轉成現金回報，不需要大幅稀釋股東。","2y":"FY27 全年營業現金流高於 FY26 的 0.8 億美元，FY28 全年自由現金流轉正。","5y":"自由現金流利潤率高於 FY23～FY25 的 3～4%。","10y":null,"threshold":"FY27 全年營業現金流 >0.8 億美元；FY28 自由現金流 >0；槓桿 ≤2 倍","source":"10-Q、10-K 現金流量表","drift_rule":"FY27 全年營業現金流未轉正為反轉；FY28 自由現金流為負且資本支出占營收超過 20% 為削弱。"}],"R":[{"id":"R1","text":"客戶集中與向後整合：前兩大客戶占 32%，大客戶可能自製雷射或扶植第二來源。","h_ref":"H1","clock":"🔥","threshold":"最大客戶占比由 20% 降到 10% 以下，或有可靠來源確認自製雷射導致轉單","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0","competitive_share_entrants#0"]},{"id":"R2","text":"AI 資本支出消化與 CY28 磷化銦過剩，同時打擊營收、定價與產能利用率。","h_ref":"H1／H3","clock":"🔥","threshold":"非 GAAP 毛利率連 2 季年減，或 EML 報價連 2 季下跌，或雲端資本支出指引連 2 季下修超過 20%","evidence_refs":["supply_demand_durability#2"]},{"id":"R3","text":"現金流與融資：資本支出持續上升，現金只夠支應約 2.7 季目前的流出速度。","h_ref":"H3","clock":"⚡","threshold":"Q2 FY27 營業現金流仍為負且資本支出再增，或股權增資超過 5%，或槓桿超過 2 倍","evidence_refs":["supply_demand_durability#2"]},{"id":"R4","text":"CPO 替代可插拔模組，以及中國廠在下一代模組份額擴大。","h_ref":"H1／H2","clock":"🐢","threshold":"CPO 滲透率超過 30% 且 PhotonLink 未達每季 2.5 億美元，或可靠來源顯示公司在主要客戶份額下滑","evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#4"]},{"id":"R5","text":"出口管制、關稅與磷化銦基板供應。","h_ref":"H2","clock":"🔥","threshold":"非 GAAP 毛利率單季下降 ≥100 個基點且公司歸因於關稅或管制，或基板出口許可收緊","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]}],"single_thing":{"description":"前兩大客戶之一在 CY28 前下修或延後長約承諾量（含改用自製雷射或轉單）。","why_fatal":"FY26 最大客戶占營收 20%。以 FY28 共識營收 155 億美元估約 31 億美元，毛利率 45% 時少 14 億美元毛利，稅後約 11 億美元，每股約 5.7 美元，占 FY28 共識 EPS 13.97 美元約 41%。同期高資本支出與負自由現金流不會同步下降。","if_happens":"確認後一週內減碼一半；若毛利率同時連 2 季年減，清倉。","how_monitor":"10-K、10-Q 的主要客戶占比、剩餘履約義務與合約負債，法說對長約的描述，以及供應鏈報導。","probability":"15%～20%（12～24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.8,"peg_fy2":0.32,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2026A":4.12,"FY2027E":9.42,"FY2028E":13.97,"FY2029E":19.13},"fy_end_month":6,"eps_basis":"FY27～FY29 為 Koyfin 共識，研判屬非 GAAP，EPS 家數事實表未涵蓋。基期 FY26 只有 GAAP 稀釋 EPS 4.12 美元，含處分利得；FY26 非 GAAP 全年數事實表未涵蓋，因此基期不能與共識直接算複合成長。"},"catalysts":[{"date":"2026-11-27","date_precision":null,"type":"regulatory","event":"中國對美鎵鍺銻出口禁令暫停期到期","impact":"中","watch":"是否延長，以及下一季毛利率"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q2 FY27 財報","impact":"高","watch":"毛利率、營業現金流與資本支出"},{"date":"2027-05","date_precision":"month","type":"product","event":"Q3 FY27 財報確認 PhotonLink 3 月季營收","impact":"高","watch":"是否超過 1 億美元"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"蘇黎世 6 吋磷化銦產線開始生產","impact":"中","watch":"是否在 CY27 上半年如期投產"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27 Q4 財報與全年現金流","impact":"高","watch":"單季營收是否達 30 億美元，全年營業現金流是否轉正"},{"date":"2027-12","date_precision":"month","type":"capacity","event":"內部磷化銦產能再翻倍以上的目標期限","impact":"高","watch":"內部雷射比例與毛利率"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 26 週 −42% 定價 CY28 過剩與融資風險，但 CY27 訂單近滿、長約多含預付，現價只要求 FY29 共識大致兌現且之後不再快速成長。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟢', moat_trend='↑', week26=-42.49, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"requires_critic":[]}}
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
