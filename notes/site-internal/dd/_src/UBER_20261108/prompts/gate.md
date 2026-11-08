你是 DD 管線 v20 的判斷層閘（gate），標的 UBER（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝14766 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得共識營收，省略
- `f_kpi2_gaap_income_from_operati`（q1_business）｜GAAP income from operations＝1447 USD m（占營收 9.8%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得，省略
- `f_kpi5_gross_bookings`（q1_business）｜Gross Bookings＝59819 USD m（YoY +20% 固定匯率；Mobility 29,512 +18%、Delivery 28,539 +22%、Freight 1,768 +35%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得，省略
- `f_kpi6_adjusted_ebitda`（q1_business）｜Adjusted EBITDA＝2963 USD m（占 GB 5.0%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得，省略
- `f_kpi7_mapcs_trips_archetype`（q1_business）｜MAPCs／Trips（平台 archetype）＝215 M MAPCs（YoY +14%）；Trips 4,061M（YoY +16%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得，省略
- `f_peer_uber_gross_margin_pct`（q2_moat）｜UBER 毛利率＝43.21 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UBER.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_uber_operating_margin_pct`（q2_moat）｜UBER 營業利益率＝12.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UBER.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dash_operating_margin_pct`（q2_moat）｜DASH 營業利益率＝5.55 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DASH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lyft_operating_margin_pct`（q2_moat）｜LYFT 營業利益率＝-1.77 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LYFT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_grab_operating_margin_pct`（q2_moat）｜GRAB 營業利益率＝10.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GRAB.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_uber_fcf_margin_pct`（q2_moat）｜UBER FCF 利潤率＝18.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UBER.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_kpi9_guidance_q4_2026`（q1_business）｜Guidance：Q4 2026 展望＝Gross Bookings 63.25–65.25B（固定匯率 +18% 至 +22%，匯率約 1 個百分點逆風）；Adjusted EBITDA 3.13–3.23B；Non-GAAP EPS 0.95–0.99（YoY +34% 至 +39%） 區間｜期間與口徑：Q3 FY2026（公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）；另提及年底約 700 輛全無人駕駛車上線、2027 年超過 2,000 輛（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（公告於 2026-11-04））
  - 註記：未查得，省略；公司未提供全年指引
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.36 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝4.41 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝5.5 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝57814.28 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（46 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝67017.55 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（48 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝2535 USD m（營運現金流 2,639；FCF 占營收約 17.2%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）；TTM FCF 約 10.4B 取自 Quartr 摘要（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得，省略
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝40.8 %（SBC 591m ÷ GAAP 營業利益 1,447m；占營收 4.0%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SBC 591m 取自新聞稿現金流量表；比率為本 agent 計算。Adjusted EBITDA 調節表口徑為 529m（不含併購、重組、舊獎勵結算相關 SBC），若用此口徑為 36.6%（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝7669.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 17737.0、現金 10068.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝68.59 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.41 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 3.36，分子＝快照價 68.59｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝147722.79 USD m｜期間與口徑：2026-11-08／市值 140053.79 ＋ 淨負債 7669.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝40.35 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝50.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝50.3 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝48.1 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝47.1 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（3.36 → 3.36）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（4.41 → 4.41）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（5.5 → 5.5）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 3.36 → 3.36（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 68.59 / W52 75.29 / W104 78.49 / W250 59.83 / W250 13週斜率 0.74%」

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：Uber 稱 mobility／delivery／logistics 低進入門檻、低轉換成本，預期未來有新進入者；AV 對手含 Alphabet(Waymo)、Amazon(Zoox)、Tesla。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 自述負面媒體報導使競爭對手募資、加碼投入並提升品類地位與市占。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Schwab Network 影片摘要：UBER 面臨 DASH、LYFT、Waymo 加速搶市占的逆風。
  - 來源：Schwab Network（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Mobility growth ran 1–2 points below management expectations due to elevated fuel prices and tighter driver supply in some international markets (supply-side constraint); trends improved in October.
  - 來源：Uber Q3 26 Prepared Remarks（as_of 2026-11-04）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素：Uber 目前受 DOJ、FTC 及其他聯邦、州、地方與外國政府機關多項詢問、調查與資料要求，不利結果可能傷害業務；反壟斷申訴已在美國與巴西等地提出。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 列示：歐盟、美國、巴西、印度等主要市場競爭法執法趨嚴，焦點含定價平價、操縱價格與濫用市場力；主管機關可罰款、強制剝離資產或限制定價模式。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-13）｜affects：thesis.R、moat_trend
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：FTC 於 2025-04 起訴 Uber One 訂閱做法（ROSCA），21 州加 DC 於 2025-12 加入；搜尋結果顯示 Uber 否認並主張為 first-party biller。
  - 來源：CBT News / SAN 等（搜尋摘要）（as_of 2025-04-22）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Uber 10-K 風險因子指出，近期關稅推高新舊車零件價格，增加司機與貨運業者成本，可能使其減少在平台上的工時或另尋收入來源；未見自身產品出口管制或直接進口關稅暴露的記載。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：MarketBeat 分析：Uber 司機自備並維修車輛，汽車零件關稅可能推高其維修成本。
  - 來源：MarketBeat（as_of 2026-01-01）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 風險因素提及中東與俄烏衝突，可能涉及制裁與區域不穩，影響無法預測，可能對業務、營運結果與股價造成重大損害（搜尋摘要轉述，未讀原文）。
  - 來源：Uber Technologies Form 10-K FY2025 (SEC)（as_of 2026-02-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2026年5月報導：Uber 預期Q2訂單穩健，但受中東衝突、燃料成本與地緣緊張壓力（搜尋摘要轉述）。
  - 來源：Boursorama (Reuters 法文轉載)：Uber prévoit des réservations solides au T2 malgré le conflit au Moyen-Orient（as_of 2026-05-06）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：自駕供應集中度：Uber 持有 Lucid 約11% 股權，訂購至少3.5萬輛搭載 Nuro 系統的 robotaxi 車輛；Waymo 計畫2028年1月起在奧斯汀與亞特蘭大自營，現有合約至少到2028年5月（二手整理，未核原文）。
  - 來源：letsdatascience：Uber Reengages Partnerships To Rebuild Autonomy（as_of 2026-07-27）｜affects：moat_trend、decision_inputs.bear
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 Mobility Gross Bookings +17% cc (~$29.5B reported); Mobility revenue -2% to $7.5B; management cited international driver supply constraints for growth short of expectations (搜尋摘要彙整，未逐字核原文)
  - 來源：Uber Announces Results for Third Quarter 2026 / Uber Q3 26 Prepared Remarks（as_of 2026-11-04）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 列出自駕車業者 Alphabet(Waymo)、Amazon(Zoox)、Tesla 為正在或可能與 Uber Mobility 競爭的對手
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：AI 助理等新技術可能使 Uber 與消費者的關係被中介化，需求轉向競爭者
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 2026 non-GAAP EPS $0.88 低於共識 $0.90（差 2.54%），營收 $14.77B 高於預期 0.63%；EPS 落差與股權投資重估虧損 $476M 有關。
  - 來源：Zacks: Uber Q3 earnings miss estimates on investment loss, revenue beat（as_of 2026-11-04）｜affects：valuation、decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露公司涉多項訴訟與政府調查，含集體訴訟（如澳洲計程車業集體訴訟已和解、無承認責任）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K FY2025 揭露多項個人、多原告及集體訴訟；Item 3 稱除 Note 14 所述外，預期無重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-13）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：FTC 2025-04 起訴 Uber One 訂閱計費與取消做法，2025-12 修正起訴有 21 州＋DC 加入；搜尋未見 2026 已提起的證券集體訴訟，僅有原告律所調查公告（Portnoy，2026-03-03）。
  - 來源：WebSearch（FTC Release 轉載、Portnoy Law Firm 公告）（as_of 2025-12-01）｜affects：decision_inputs.bear、thesis.R
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：搜尋未見 Uber 自身 2026 產品召回；NHTSA 於 2026-05-08 調查 Uber 自駕夥伴 Avride（Dallas 16 起 robotaxi 事故），屬調查而非召回。
  - 來源：WebSearch 結果摘要（NHTSA / Avride）（as_of 2026-05-08）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":236.9,"bear_5y_price":51.6,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":94.6,"ev5y_pct":83.0,"irr_base_pct":14.2,"asym_ratio":5.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.36,"pe":20.41,"basis":"FY2026E 非 GAAP 共識 EPS，現價 68.59 美元；終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[4.55,5.75,7.1,8.6,10.3],"base":[4.25,5.2,6.1,7.0,7.85],"bear":[3.75,3.95,4.1,4.2,4.3]},"pe":{"bull":23,"base":17,"bear":12},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### UBER_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Balaji Krishnamurthy｜guidance：CFO重申美國全年逐季加速的預期（原話："we expect the U.S. to accelerate through this year."）
- 2026-08-05｜Balaji Krishnamurthy｜guidance：CFO稱對下半年維持原預期（原話："We continue to hold our expectation for the remainder"）
- 2026-08-05｜Dara Khosrowshahi｜guidance：CEO給AV上線城市目標：年底15個市場（原話："We'll be in 15 markets by the end of the year."）
- 2026-08-05｜Balaji Krishnamurthy｜guidance：CFO談Q3外送：Turkey併購交接對報告成長為淨逆風（原話："it is a headwind to Delivery reported growth"）
- 2026-08-05｜Balaji Krishnamurthy｜guidance：CFO稱Q3外送有機成長加速（原話："our organic Delivery business is accelerating quite nicely"）
- 2026-08-05｜Dara Khosrowshahi｜margin：CEO報Q2總預訂量成長與規模（原話："bookings grew 22% year-on-year to more than $58 billion"）
- 2026-08-05｜Dara Khosrowshahi｜margin：CEO報TTM自由現金流首度超過100億美元（原話："trailing 12-month free cash flow exceeding $10 billion"）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO拆解Mobility收入take rate降幅（原話："nearly 500 basis points decline year-on-year"）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO稱其中約400bp為英國商業模式變更的帳面影響（原話："it's an optical impact."）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO報Mobility營業利益率（原話："operating income margin remains very strong at 7.6% as well"）
- 2026-08-05｜Dara Khosrowshahi｜margin：CEO稱巴西二輪車業務利潤低、未衝擊獲利但影響趟次（原話："it's certainly not hitting the bottom line"）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO稱AI與組織精簡使人力增速放緩，部分組織減編10-20%（原話："headcount by about 10% to 20%"）
- 2026-08-05｜Balaji Krishnamurthy｜margin：CFO稱工程師程式產出倍增（原話："a doubling in the code output per engineer"）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO稱巴西外送競爭（DiDi Food、Meituan）新增（原話："DiDi has introduced DiDi Food."）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO稱巴西份額持平、流量由Mobility移向Delivery（原話："we continue to hold our share in Brazil"）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO談Waymo：不想依賴單一夥伴（原話："we're not dependent on one partner."）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO稱Austin與Atlanta明年續營運（原話："We believe we'll continue to operate next year"）
- 2026-08-05｜Dara Khosrowshahi｜competition：CEO稱AV目前占總趟次比重（原話："even less than 0.5% of our overall trip volume"）
- 2026-08-05｜Balaji Krishnamurthy｜competition：CFO稱美國AV運營城市外仍是主要成長與獲利來源（原話："Only 30% of our U.S. gross bookings and 25% of our profits"）
- 2026-08-05｜Dara Khosrowshahi｜product：CEO談AV單車使用率（原話："often mid- to high 20s, low 30s in terms"）
- 2026-08-05｜Dara Khosrowshahi｜product：CEO談AV Labs：自建數百輛蒐集資料（原話："we're building out hundreds of cars"）
- 2026-08-05｜Dara Khosrowshahi｜product：CEO談AI預期：許多小改善而非單一大突破（原話："I wouldn't look for like one giant hit from AI."）
- 2026-08-05｜Balaji Krishnamurthy｜product：CFO談B2B產品U4B成長（原話："U4B, in particular, we saw 40% year-on-year growth"）
- 2026-08-05｜Dara Khosrowshahi｜risk：CEO談AV監管，主張放慢以換取可持續法規（原話："We're very much pro AV"）
- 2026-08-05｜Dara Khosrowshahi｜risk：CEO談Lucid新CEO與合作訂單（原話："it's a big order with kind of guaranteed volume"）
- 2026-08-05｜Balaji Krishnamurthy｜customer：CFO稱美國稀疏市場滲透率低（原話："eligible consumers in our sparse markets have used Uber"）
- 2026-08-05｜Dara Khosrowshahi｜customer：CEO稱跨平台用戶占比（原話："only 20% of our consumers at this point use both Rides and"）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO說明AV投資規模（原話："the $10 billion of AV investments we're talking about here"）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO稱夥伴每1美元獲Uber投資後另募2.5美元（原話："raise an additional $2.50 from other investors."）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO稱Q2因買進Delivery Hero股票轉向併購（原話："We deployed about $4 billion of capital in the second"）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO重申自由現金流約50%用於回購（原話："deploying about 50% of our free cash flows"）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO稱今年已回購約35億美元（原話："bought back about $3.5 billion of our stock this year."）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO給回購恢復時程（原話："I don't think this is a year away."）
- 2026-08-05｜Balaji Krishnamurthy｜capital_allocation：CFO說明Delivery Hero整合時程假設（原話："assuming we close in the second half of 2027"）
- 2026-08-05｜Balaji Krishnamurthy｜commitment：CFO承諾Delivery Hero綜效（原話："we remain committed to delivering the synergies"）
- 2026-08-05｜Balaji Krishnamurthy｜commitment：CFO稱12萬輛車承諾（原話："120,000 vehicle commitments that we are looking to deliver"）
- 2026-08-05｜Balaji Krishnamurthy｜commitment：CFO稱AV投資損益影響之後再揭露（原話："we will give you more visibility into that as"）

### 問答異常語氣（迴避／改口／保留）
- UBER_Q2_2026_Earnings_Call_20260805.md｜問：Justin Post：AV百億美元投資如何流入損益表、對利潤率的影響｜答法：未給數字，稱隨部署逐步提供損益影響的可視度
- UBER_Q2_2026_Earnings_Call_20260805.md｜問：Doug Anmuth：媒體報導Uber與Waymo關係，請釐清｜答法：稱Waymo是重要夥伴、Austin/Atlanta續營運，但未直接回應報導內容，轉談不依賴單一夥伴
- UBER_Q2_2026_Earnings_Call_20260805.md｜問：Mark Mahaney：能否量化AI對消費者轉換與支出的提升｜答法：未給整體量化，只舉cart builder購物車約兩倍與3/4目的地建議等例子，稱不要期待單一大突破

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 1 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 1 | 0 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 2 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 3 |
| major_events | found | 4 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260808","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"N/A（裁決為進場，非觀望）","irr_base_pct":16.6,"ev5y_pct":94.3,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"🟠","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.65,"ev5y_pct":94.3,"irr_base_pct":16.6,"max_dd_pct":-58.0,"bull_5y_price":264.0,"bear_5y_price":55.0,"p_bull_pct":20.0,"p_bear_pct":35.0,"rearm_trigger":"N/A（裁決為進場，非觀望）","price_at_dd":74.21,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"UBER","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Uber Technologies, Inc."},"oneliner":"Q3 訂單仍年增 20%、外送加速，現價約今年非 GAAP EPS 20 倍，FCF 隱含永續成長僅 2～3%；最大不確定是自營自駕車隊是否繞過平台，以及 Mobility 供給缺口能否在 Q4 收斂。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UBER_20261108/scenario.json","answers":{"q1_business":{"verdict":"Uber 向乘客、餐客與商家收款後抽取撮合費，錢卡在即時配對這一節點；Q3 的 598 億美元訂單轉成 148 億美元營收。","reasoning":"Q3 營收占訂單約 24.7%（14,766÷59,819）。依 10-Q，固定匯率訂單成長為 Mobility 17%（295 億美元）、Delivery 23%（285 億美元）、Freight 35%（18 億美元）。Mobility 營收約 75 億美元、Delivery 約 55 億美元（搜尋摘要，未逐字核），Freight 約 18 億美元為餘數，三塊都超過營收 10%。最新一季 GAAP 營業利益率 9.8%，季度毛利率事實表未涵蓋，TTM 為 43.21%。需求端極度分散，2023 至 2025 年無單一客戶占營收 10% 以上。單點依賴在供給側：司機與外送員時數決定訂單能否成交，Q3 的國際市場缺口就來自這裡；自駕車隊若集中到少數技術方，依賴會更明顯。","fact_refs":["f_kpi0_revenue_gaap","f_kpi2_gaap_income_from_operati","f_kpi5_gross_bookings","f_kpi6_adjusted_ebitda","f_kpi7_mapcs_trips_archetype","f_peer_uber_gross_margin_pct"],"verdict_values":{"revenue_quality":"抽成與會員費為主，重複使用率高；Uber One 約 5,500 萬人，貢獻過半訂單，外送部分達 70%。Q2 法說 CFO 稱 Mobility take rate 下滑多為英國商業模式改變的帳面影響，Q3 Mobility 營收年減 2% 的原因本包未逐字核實，判斷成長時以訂單為準。","unit_econ_note":"Adjusted EBITDA 占訂單 5.0%，非 GAAP 營業利益占訂單 3.9%。Q3 起把乘客補貼移給司機，乘客實付價格可能上升。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"輕資產雙邊平台；FCF 利潤率由 FY2022 的 1.2% 升至 TTM 18.4%；GAAP 營業利益率仍只有 12.4%"},"industry":{"clock_phase":"II","sd_verdict_source":"擴張期，依據是 MAPC 年增 14%、趟次年增 16%。需求屬結構性持久；短期受限於司機與外送員供給，這部分可用補貼修復，可逆性高，但移民因素可能較持久。來源為 Q3 法說與 10-Q。","bargaining":{"up":"對司機與外送員的議價力有限，油價與移民壓力下需把補貼轉給供給端。","down":"10-K 自述消費者切換成本低，Uber One 部分抵銷；商家因 DoorDash 與 Instacart 可能合併而尋求替代通路，對 Uber 有利。","geo":"巴西、印度受油價影響最大，加拿大受移民政策影響。"},"profit_pool_dir":"利潤池往會員、外送與雜貨延伸；自駕放量後，Mobility 利潤可能部分移往車隊與技術方。五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"前十大市場可服務人口滲透率","value":"約 10%，過去 5 年翻倍（CFO，Q3 法說）"},{"item":"美國稀疏市場近 12 個月使用率","value":"低於 10%，密集市場為 50%（CFO，Q3 法說）"},{"item":"雜貨與零售","value":"年化 150 億美元、年增 40%；管理層稱 TAM 為 10 兆美元，未獨立查證"},{"item":"自駕占總趟次","value":"低於 0.5%（CEO，2026-08-05）"},{"item":"五年營業利益池變化","value":"事實表未涵蓋，無法檢查利潤池是否流出"}]}}},"q2_moat":{"verdict":"護城河方向持平：訂單密度與會員帶來的規模優勢仍在擴大，定價權則受司機供給與自駕新供給牽制，兩者相抵。","reasoning":"機制是雙邊密度：乘客與餐客多，司機與外送員等待時間短，會員再把兩個業務綁在一起。可驗證的方向有三個。第一，MAPC 2.15 億人年增 14%，趟次年增 16%，規模仍在擴大。第二，TTM 營業利益率 12.44%，高於 DoorDash 5.55%、Grab 10.95%、Lyft −1.77%，但同業 ROIC 事實表未涵蓋，無法判斷差距擴大或收窄。第三，定價權沒有變強：10-K 自承切換成本低，Q3 把乘客補貼轉給司機，CEO 也承認乘客可能付更高價格。美國外送份額最新資料停在 2024 年底，Uber Eats 26.1%、DoorDash 60.7%，近 12 個月份額事實表未涵蓋。","fact_refs":["f_kpi7_mapcs_trips_archetype","f_peer_uber_operating_margin_pct","f_peer_dash_operating_margin_pct","f_peer_lyft_operating_margin_pct","f_peer_grab_operating_margin_pct","f_peer_uber_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"雙邊網路密度加跨業務會員：需求越密，供給等待時間越短，Uber One 再提高兩項業務的使用頻率。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：連續五季訂單成長 20% 以上，TTM FCF 達 104 億美元創新高。定價面持平：Uber One 約 5,500 萬人，但補貼轉向司機，10-K 自承切換成本低。前份同為持平。","competitor_notes":[{"name":"DoorDash","strategy_note":"美國外送龍頭，2024 年底份額 60.7%，TTM 營業利益率 5.55%；若併 Instacart 將強化線上雜貨份額，是外送最強對手。"},{"name":"Lyft","strategy_note":"TTM 營業利益率 −1.77%、FCF 率 16.43%，品類與地域較窄，主要影響美國部分市場的價格與司機補貼。"},{"name":"Grab","strategy_note":"TTM 營業利益率 10.95%、FCF 率 −0.45%，作為同模式利潤率對照，與 Uber 的直接競爭關係事實表未涵蓋。"},{"name":"Booking","strategy_note":"TTM 營業利益率 32.78%、FCF 率 32.84%，代表成熟中介平台的利潤上緣，商業模式不同，只作遠期參照。"},{"name":"Waymo","strategy_note":"在奧斯汀與亞特蘭大透過 Uber 營運，二手資料稱 2028 年 1 月起在兩地自營，是自駕最大變數。"},{"name":"Tesla","strategy_note":"10-K 列為競爭者；CFO 稱其新市場單車日趟次只有低十幾趟，該數字未獨立查證。"}],"spread_notes":{"note":"ROIC 差距事實表未涵蓋，改以 TTM 營業利益率比較：Uber 高於 DoorDash 6.89 個百分點；前期差值未入表，無法判斷擴大或收窄。"},"peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋。","threats":[{"level":"🔴","text":"自駕自營：Waymo 與 Tesla 自建 App 與車隊，可能繞過平台；Waymo 計畫 2028 年 1 月起在奧斯汀與亞特蘭大自營（二手資料，未核原文）。目前自駕不到總趟次 0.5%，傷害要到 2028 年後才可能反映。","p":35,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","geo_supply_chain#2"]},{"level":"🟡","text":"外送對手：DoorDash 若併 Instacart 將集中線上雜貨份額，巴西有 DiDi Food 與美團進場。10-K 自述對手曾趁負面報導增資搶份額；第三方 App 使用量的說法未附數字，只作方向參考。","p":30,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3"]},{"level":"🟡","text":"AI 助理中介：10-K 列為風險。萬聖節當週約 3.2 億趟中，代理程式僅約 500 筆外送與 4 趟乘車，尚無實質影響。資料、會員與履約長在自有資產上，屬強化；第三方代理若成主要入口才算替代，分界年抓 2028 年。","p":15,"evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉（周轉率事實表未涵蓋，依輕資產結構判斷）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者與付款者多為同一人，需求由通勤、用餐與日常採購構成。MAPC 年增 14%，公司稱受限於供給而非需求，前十大市場滲透率僅約 10%。"},{"item":"決策層級","level":"🟡","text":"替代性在每一趟、每一單決定，10-K 自承切換成本低。75% 乘車一鍵完成、Uber One 占過半訂單可降低比價，但僅約 20% 用戶同時使用乘車與外送。"},{"item":"價值鏈分配","level":"🟡","text":"目前 Uber 掌握配對節點。自駕放量後，技術方與車隊可能分走利潤；管理層目標只是自駕毛利與人類司機相當，尚未驗證。"},{"item":"社會容忍度","level":"🟡","text":"FTC 與 21 州加 DC 控告 Uber One 計費與取消做法，DOJ、FTC 另有多項調查，主要市場競爭法趨嚴；定價上限受監管與司機待遇爭議限制。"}],"roiic":"事實表未涵蓋（投入資本與收購淨額未入表）","reinvest_rate":"事實表未涵蓋（折舊、營運資金與收購淨額未入表）","endo_ceiling":null,"formula_note":"Q3 資本支出約 104 百萬美元（營運現金流 2,639 減 FCF 2,535），低於 Adjusted EBITDA 與非 GAAP 營業利益的差額 659 百萬美元，有機再投資率接近零甚至為負。已知外部投入為 Q2 購入 Delivery Hero 股票約 40 億美元、自駕 100 億美元承諾，增量報酬尚未揭露。"}}}},"q3_growth":{"verdict":"成長跑道寬：前十大市場滲透率約 10%，雜貨與零售是已起量的第二曲線。","reasoning":"成長以量為主。共識 EPS 由 FY2026 的 3.36 美元到 FY2028 的 5.50 美元，年化 27.9%，EPS 分析師家數事實表未涵蓋；FY2025 非 GAAP 基期未入表，因此以兩年計算。FY2027 共識營收僅成長 15.9%，相差 12 個百分點，歸因於利潤率擴張與股數下降，其中稀釋股數 FY2025 年減約 1.7%，其餘主要靠利潤率。Q4 指引 18% 至 22%，下緣已低於連續五季 20% 以上的紀錄。前十大市場滲透率過去 5 年翻倍至約 10%，以年增約 15% 推算，約 8 年可達 30%，屬中等確信。Delivery Hero 預計 2027 下半年交割，是否納入共識事實表未涵蓋。","fact_refs":["f_kpi5_gross_bookings","f_kpi7_mapcs_trips_archetype","f_kpi9_guidance_q4_2026","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主：Q3 趟次年增 16%、MAPC 年增 14%，單趟訂單額約增 3.4%；併購貢獻有限，Delivery Hero 尚未計入；股數下降約 1.7%。","runway_years":8,"runway_post_y5":"🟢","endo_ceiling_basis":"內生上界無法計算，投入資本、折舊與收購淨額未入表。有機業務資本支出極低，公式不具約束力；共識成長主要靠利潤率與股數，不靠再投資，情境樹按超出處理，Bear 機率維持 30% 以上。","segments":[{"item":"Mobility","value":"訂單 295 億美元，固定匯率年增 17%；分部營業利益率 Q2 為 7.6%，Q3 分析師引述約 8%"},{"item":"Delivery","value":"訂單 285 億美元，固定匯率年增 23%，美國有機成長連兩季加速"},{"item":"Freight","value":"訂單 18 億美元，年增 35%，連三季加速"},{"item":"雜貨與零售","value":"年化 150 億美元，年增 40%"},{"item":"企業與高階產品","value":"U4B 年增近 50%，高階產品年增 35%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"季度毛利率事實表未涵蓋；年度由 39.4% 升至 39.75%"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"近 12 個月份額事實表未涵蓋；CEO 2026-08-05 稱巴西份額持平"},{"signal":"提價後銷量下滑","lit":false,"note":"Q3 減少乘客補貼，Mobility 低於預期 1 至 2 個百分點，公司歸因供給，列監測"},{"signal":"EPS 成長高於營收成長 5 個百分點以上","lit":true,"note":"共識 EPS 年化 27.9%，FY2027 營收成長 15.9%，差 12 個百分點"},{"signal":"FCF 對淨利連 2 年低於 0.75","lit":false,"note":"FY2024 為 0.70，FY2025 為 0.97"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"Q3 為 4.0%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"自駕不到總趟次 0.5%，尚未壓縮"},{"signal":"產業倍數近 3 年系統性下移","lit":false,"note":"同業倍數歷史事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"Q3 資本支出約 1.04 億美元，占 FCF 約 4%"},{"signal":"停止投資新產能且營收下滑","lit":false,"note":"營收仍在成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置評 B：股數持續下降，但併購與回購報酬缺資料，無法給更高評分。","reasoning":"FCF 對淨利的轉換率 FY2025 為 97%（9,763÷10,053）、FY2024 為 70%（6,895÷9,856），淨利受稅務與投資重估影響，FCF 較可靠。SBC 占 Q3 營收 4.0%、占 GAAP 營業利益 40.8%。現金去向方面，CFO 2026-08-05 稱約 50% FCF 用於回購，今年當時已回購約 35 億美元，Q2 另以約 40 億美元購入 Delivery Hero 股票。Q3 法說稱明年重心轉向有機成長、自駕與伺機回購，併購放緩。Delivery Hero 總對價事實表未涵蓋，已知融資包括 €45 億票據與定期貸款，後者使過橋額度減少 €40 億。淨負債 7,669 百萬美元，約年化 Adjusted EBITDA 的 0.65 倍，尚未含收購對價。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc_gaap","f_kpi6_adjusted_ebitda","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"已實現併購 ROIIC 事實表未涵蓋；管理層稱併購標的高於交易預期，未給數字。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與十年期殖利率事實表未涵蓋。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"由淨利除以稀釋 EPS 反推 FY2023 至 FY2025 稀釋股數約 2,169、2,161、2,125 百萬股，年變動 −0.4%、−1.7%，淨稀釋低於 1.5%。"}]},"governance":{"capital_returns":[{"item":"TTM FCF","value":"約 104 億美元"},{"item":"回購","value":"CFO 稱約 50% FCF；2026-08-05 前當年約 35 億美元"},{"item":"Delivery Hero","value":"每股 €41.50 現金收購，Q2 已購股約 40 億美元；總對價事實表未涵蓋"},{"item":"收購融資","value":"€45 億票據；定期貸款使過橋額度減少 €40 億"},{"item":"自駕投資","value":"100 億美元承諾，損益影響未揭露"}]}}},"q5_valuation":{"verdict":"現價只要求 FCF 永續成長約 2～3% 就合理，我認為要求不高，前提是自駕不在 2030 年前吃掉 Mobility 的利潤池。","reasoning":"現價 68.59 美元，FY2026E 非 GAAP 本益比 20.41 倍，FY2027E 15.55 倍。TTM FCF 約 104 億美元，對 EV 147,723 百萬美元的殖利率約 7.0%；扣年化 SBC 2,364 百萬美元後約 5.4%。以 9% 折現率反推，永續成長率只需約 1.8%～3.4%，而 Q3 訂單仍成長 20%。風險在自駕與 Delivery Hero 的現金需求尚未計入。賣方九月中平均目標價約 101 至 103 美元，區間 75 至 150 美元，高低比 2.0 倍；快照早於 Q3 財報，只作方向參考。FY1 至 FY3 共識修正全部為 0.0%，財報前後完全不動並不合理，可能是快照未更新，不能當作賣方未下修的證據。短期空間以 FY2027E Base EPS 4.25 美元乘現行倍數，中期以 FY2029E 6.10 美元乘 17 倍計算。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_ev_m","f_kpi3_free_cash_flow","f_kpi4_sbc_gaap","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"FY2026E 非 GAAP 前瞻本益比，以扣 SBC 後的 FCF 殖利率交叉檢查","tier":"大型獲利平台","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法作為估值錨。"},"fwd_pe":20.41,"peg":0.73,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"FY2026E 本益比 20.41 倍除以兩年 EPS 年化 27.9%，PEG 為 0.73，低於 1。扣股份報酬後對市值的 FCF 殖利率仍有 5.7%，結論是便宜。五年分位事實表未涵蓋，只有少量年度端點分位：本益比 50.3、P/S 48.1、EV/S 47.1，不當作五年分位使用。","upside_short_pct":26.5,"upside_mid_pct":51.2,"denominator_disputed":false,"denominator_note":"非 GAAP EPS 未扣 SBC，扣除年化每股約 1.16 美元（未計稅盾）後本益比約 31 倍；TTM GAAP 本益比 40.35 倍又含重估損益。便宜的結論改由扣 SBC 後的 FCF 殖利率支撐，不依賴這個分母。Delivery Hero 的對價與 EPS 貢獻尚未反映在 EV 內。"}}},"q6_how_wrong":{"verdict":"最可能看錯在三處：自駕的資本與利潤分配、Delivery Hero 的價格與整合、Mobility 供給問題變成結構性。","reasoning":"衰退信號亮 1 個，即共識 EPS 成長高於營收 12 個百分點，評為中等。成長熄火壓力測試以 Base 的 FY2029E EPS 6.10 美元為起點，後兩年成長 15%、10%、5%，終端 16、13、10 倍，FY2031E 股價約 129、96、67 美元，三種情境中兩種高於現價。管理層迴避點：自駕 100 億美元對損益的影響，Q2 與 Q3 都沒給數字；Q2 問到 Waymo 媒體報導時未正面回應；AI 對消費者轉換的整體提升也未量化。歷史最大回撤與空方數字事實表未涵蓋。","fact_refs":["f_price_at_dd","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy2_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"中等，一項衰退信號亮燈"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.36,"pe":20.41,"basis":"FY2026E 非 GAAP 共識 EPS，現價 68.59 美元；終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[4.55,5.75,7.1,8.6,10.3],"base":[4.25,5.2,6.1,7.0,7.85],"bear":[3.75,3.95,4.1,4.2,4.3]},"pe":{"bull":23,"base":17,"bear":12},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":10},"max_dd":{"lo":-58,"hi":-35,"basis":"情境內推算：Bear 的 FY2027E EPS 3.75 美元乘 10 至 12 倍，得 37.5 至 45 美元，相對現價 −45% 至 −34%；下緣沿用前份 −58%，代表倍數進一步壓縮。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"自駕放量且維持需求入口地位，Delivery Hero 綜效兌現，雜貨起量；EPS 年化 25%；終端 23 倍，高於現值 20.41 倍，因仍有中雙位數成長與第二曲線。股數下降已含在 EPS 路徑，淨回購不另計。","base":"FY2027E 與 FY2028E 較共識低 3.6% 與 5.5%，計入自駕投資與 Mobility 補貼，之後成長降到十幾%；EPS 年化 18.5%；終端 17 倍，低於現值 3.4 倍。同業現值倍數事實表未涵蓋，只以自身現值 20.41 倍對照。","bear":"自駕自營在美國大都會分走份額，Mobility 補貼常態化，Delivery Hero 整合不順；EPS 年化約 5%；終端 12 倍，取 3 年後成長降至 10%（約 13 倍）與 5%（約 10 倍）之間。機率 35% 依據是自駕風險窗尚無證據覆蓋，且內生上界無法驗證。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"五年後虧 50% 最可能的故事：Waymo 與 Tesla 的自營車隊在美國大都會達到成本優勢，Uber 的自駕城市 Mobility 訂單轉負，市場把 20 倍倍數降到 10 倍出頭。","assumption":"自駕放量時需求仍走 Uber，且管理層宣稱的利用率優勢持久。","consequence":"Bear 終端 EPS 4.30 美元、12 倍，股價約 52 美元；倍數再壓縮時，回撤可達 −58%。","ruling":"採納，列為唯一致命項。目前自駕不到總趟次 0.5%，風險窗在 2028 年後，現有證據蓋不到這段時間，不能宣稱風險已解。","watch":"自駕城市 Mobility 訂單年增率、Waymo 2028 年合約走向","evidence_refs":["substitute_technology#0","geo_supply_chain#2"],"fact_refs":["f_price_at_dd"]},{"view":"論點成功但股東經濟變差","evidence":"自駕成功但資本與利潤外流：100 億美元投資承諾、早期車輛放在自己的資產負債表，Delivery Hero 全現金收購，再加上補貼常態化。Q2 與 Q3 分析師問自駕損益與資本回報，管理層都沒有給數字。","assumption":"第三方資金會接手車隊，Delivery Hero 的報酬高於資金成本。","consequence":"訂單照長，但每股 FCF 被折舊、利息與夥伴分潤吃掉，EPS 趨近 Bear 路徑。","ruling":"部分採納。Base EPS 已低於共識 3.6% 與 5.5%，資本回流風險列入長期風險。","watch":"首筆自駕融資條款、Delivery Hero 交割後淨負債倍數","evidence_refs":["major_events#0","major_events#1","ma_merger#0"],"fact_refs":["f_net_debt_m","f_kpi6_adjusted_ebitda"]},{"view":"價格已反映太多","evidence":"20.41 倍的分母未扣股份報酬，扣除年化每股約 1.16 美元後約 31 倍；TTM GAAP 本益比 40.35 倍；共識 EPS 年化 27.9% 遠高於營收 15.9%，需要利潤率持續擴張。","assumption":"非 GAAP EPS 能代表股東實得，且利潤率擴張持續到 FY2028。","consequence":"若利潤率擴張提前結束，FY2029E EPS 可能低於 Base 的 6.10 美元，倍數也難維持。","ruling":"反駁。TTM FCF 對市值殖利率 7.4%，扣股份報酬後 5.7%，以 9% 折現率只隱含永續成長 2～3%，遠低於目前成長。GAAP 本益比含 Q3 股權重估虧損 476 百萬美元，不適合單獨當錨。","watch":"Adjusted EBITDA 占訂單；GAAP 營業利益增速","fact_refs":["f_fwd_pe_latest","f_pe_current","f_kpi4_sbc_gaap","f_kpi3_free_cash_flow"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 74.21 → 本次 68.59（-7.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=74.21","side_b":"本次 price_at_dd=68.59","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 74.21 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 74.21 美元：Bull 價 264、Bear 價 55，五年期望值 +94.3%，基準年化 16.6%，不對稱比 5.65","side_b":"本次情境、股價仍用 74.21 美元：Bull 價 236.9、Bear 價 51.6，五年期望值 +69.1%，基準年化 12.5%，不對稱比 4.11","ruling":"先換情境、股價不動：五年期望值少 25.2 個百分點，基準年化少 4.1 個百分點。不對稱比由 5.65 變為 4.11。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 74.21 美元：五年期望值 +69.1%，基準年化 12.5%，不對稱比 4.11","side_b":"本次情境、股價 68.59 美元：五年期望值 +83.0%，基準年化 14.2%，不對稱比 5.66","ruling":"再換股價、情境不動：起點價下跌 7.6%，五年期望值多 13.9 個百分點，基準年化多 1.8 個百分點，不對稱比由 4.11 升到 5.66。合計五年期望值比前份少 11.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"美國 Mobility 成長的前後說法","cause":"新證據","prior_field":["signal"],"side_a":"2026-08-05 CFO Balaji Krishnamurthy：預期美國全年逐季加速。","side_b":"2026-11-04 CFO：美國 Q3 成長略為放緩，但比國際市場穩。","ruling":"採 B 側事實，上季說法已落空。兩者可調和，放緩幅度小，加州與稀疏市場仍強，訊號等級維持前份的 B。供給因素的歸因標為未證、持續監測；連 2 季 Mobility 低於 15% 即視為歸因不成立。","evidence_level":"高，同一講者兩季逐字稿","settle_metric":"Q4 Mobility 固定匯率訂單成長是否回到 17% 以上","if_then":["如果 Q4 Mobility 固定匯率成長達 17% 以上，則買第二批","如果 Mobility 連 2 季低於 15%，則停止加碼"],"evidence_refs":["supply_demand_durability#1","end_markets#0"]},{"axis":"價值陷阱評估","cause":"新證據","prior_field":["trap"],"side_a":"前份結論為 🟢。","side_b":"本次為 🟡：共識 EPS 年化 27.9%，高於 FY2027 營收成長 15.9%，差距超過 5 個百分點；Q3 起補貼由乘客轉給司機。","ruling":"採 B。差距可由利潤率擴張與股數下降解釋，故只到 🟡。","evidence_level":"中","settle_metric":"Adjusted EBITDA 占訂單是否維持 5.0% 附近","if_then":["如果 Adjusted EBITDA 占訂單連 2 季低於 4.6%，則停止加碼","如果占訂單升至 5.5% 以上且 GAAP 營業利益同步成長，則回到 🟢"]},{"axis":"護城河方向與成長跑道","cause":"新證據","prior_field":["moat_trend","runway_post_y5"],"side_a":"前份為持平與寬跑道。","side_b":"本次維持。新增正面：Uber One 約 5,500 萬人、外送有機加速。新增負面：Mobility 供給、Delivery Hero 整合、DoorDash 與 Instacart 可能合併。","ruling":"正負相抵，結論不變。","evidence_level":"中","settle_metric":"Uber One 占訂單比重、前十大市場滲透率","if_then":["如果 Uber One 會員數連 2 季下降，則護城河方向下調並減碼","如果自駕城市訂單成長持續高於美國平均，則維持原倉位計畫"]},{"axis":"估值結論與情境機率","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 74.21 美元，估值結論 🟢，機率 20／45／35，最大回撤 −58%。","side_b":"本次股價 68.59 美元，FY2026E 本益比 20.41 倍，結論維持 🟢，機率不變，最大回撤範圍 −58% 至 −35%。","ruling":"股價下跌 7.6% 使估值略為改善，但新增的負面證據抵銷了降低 Bear 機率的理由，因此機率不動。","evidence_level":"高","settle_metric":"FY2027E 共識 EPS 修正方向","if_then":["如果股價跌破 59.83 美元而 Q4 訂單成長達 18% 以上，則分批反買","如果股價先漲而 Q4 數據未到，則不追"]},{"axis":"裁決、角色與公司類型","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份裁決進場、角色衛星、品質複利成長、無循環定位。","side_b":"本次裁決與角色由程式依本輪輸入決定；公司類型維持品質複利成長；非循環股，循環定位仍為空白。","ruling":"公司類型與循環定位沒有新證據足以改變。","evidence_level":"中","settle_metric":"無","if_then":["如果 FCF 利潤率回落到 10% 以下，則重新檢查公司類型並停止加碼"]},{"axis":"加碼條件新增，減碼條件見觸發器","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"N/A（裁決為進場，非觀望）","side_b":"Q4 財報固定匯率訂單成長達 18% 以上，且 Mobility 固定匯率成長回到 17% 以上，才買第二批；否則停止加碼","ruling":"前份未設條件。Mobility 利空出現不到一季，能否進入賣方模型無法確認，因此第二批等 Q4 數據。減碼與清倉條件另列於觸發器。","evidence_level":"中","settle_metric":"2027 年 2 月 Q4 財報","if_then":["如果 Q4 達標，則買第二批","如果 Q4 訂單成長低於 18%，則停止加碼"]},{"axis":"監控門檻新增（含減碼與清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要未記載（null）","side_b":"訂單年增低於 15% 連 2 季；Mobility 低於 13% 連 2 季減碼；Adjusted EBITDA 占訂單低於 4.6% 連 2 季；自駕城市訂單轉負連 2 季清倉；淨負債倍數高於 2.5 倍減碼。","ruling":"前份摘要沒有門檻，本次首次明訂，數字依 Q3 實際值與情境路徑設定。","evidence_level":"中","settle_metric":"每季財報","if_then":["如果任一減碼門檻觸發，則減碼一半","如果自駕城市訂單轉負連 2 季，則清倉"]},{"axis":"Single Thing 新增","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未記載（null）","side_b":"公司或第三方數據證實，美國自駕已營運城市的 Uber Mobility 訂單年增率連續兩季轉負。","ruling":"前份摘要此欄為空，本次首次明訂 Single Thing，取情境樹最大的單一敏感項。","evidence_level":"中","settle_metric":"自駕城市 Mobility 訂單年增率","if_then":["如果事件發生，則清倉","如果到 2028 年底未發生，則下調 Bear 機率並重做情境樹"]},{"axis":"自駕：夥伴或替代者","cause":"新證據","prior_field":null,"side_a":"CFO 2026-11-04：Uber 混合部署單車日趟次為高 20 趟，Waymo 與 Tesla 新市場只有低十幾趟，利用率優勢持久。","side_b":"10-K 列 Waymo、Zoox、Tesla 為競爭者；Waymo 計畫 2028 年 1 月起在奧斯汀與亞特蘭大自營（二手資料）。","ruling":"不可調和的部分要到 2028 年才能驗證。裁定 2027 年前採 A，但不採信其持久性：利用率是管理層自選的比較，對手新市場也非成熟值。Bear 機率維持 35%。","evidence_level":"中","settle_metric":"自駕營運城市 Mobility 訂單年增率；Waymo 2028 年合約走向","if_then":["如果自駕城市 Mobility 訂單連 2 季轉負，則清倉","如果 2028 年底自駕城市成長仍高於美國平均，則 Bear 機率降到 25%，並加碼至目標倉位上限","如果股價先漲但上述數據未出現，則不追"],"evidence_refs":["substitute_technology#0","geo_supply_chain#2"]},{"axis":"自駕車隊由誰出資","cause":"新證據","prior_field":null,"side_a":"CFO 2026-11-04：長期應由第三方資金支應，不用 Uber 的資產負債表。","side_b":"CEO 2026-11-04：殘值尚未建立，早期會把車輛放在自己的資產負債表。","ruling":"可調和，早期自擔、長期外包。第三方融資尚未成形，CFO 也表示還不能多說，資本回流風險列入長期風險。","evidence_level":"中","settle_metric":"2027 年首筆自駕車隊融資條款與 Uber 擔保比例","if_then":["如果 2028 年車隊融資仍以 Uber 資產負債表為主，則減碼一半","如果第三方資金承擔過半車隊成本，則維持原倉位計畫"]},{"axis":"Q3 非 GAAP EPS 是否低於預期","cause":"新證據","prior_field":null,"side_a":"Zacks：0.88 美元低於共識 0.90 美元，並歸因股權重估虧損 476 百萬美元。","side_b":"公司 Q3 指引 0.84 至 0.88 美元，實際落在上緣；事實表未查得共識值。","ruling":"採 B 作為判斷基礎。事實表把該筆虧損列在 GAAP EPS 內，A 的歸因存疑；0.90 美元只有單一來源，無法交叉核對。","evidence_level":"低","settle_metric":"Q4 非 GAAP EPS 對 0.95 至 0.99 美元指引的落點","if_then":["如果 Q4 EPS 低於 0.95 美元，則停止加碼","如果 Q4 EPS 達 0.99 美元以上，則維持第二批計畫"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢（競爭、結構、其他）","cause":"新證據","prior_field":null,"side_a":"競爭惡化：DoorDash 與 Instacart 可能合併，巴西有 DiDi Food 與美團進場，自駕自營增加。","side_b":"結構轉好：會員占過半訂單，雜貨年增 40%，美國保險成本順風。其他結構變數為監管，FTC 訴訟與競爭法趨嚴。","ruling":"雙向拉鋸。依據是 Q3 外送有機加速，但 Mobility 供給與自駕競爭同時升溫。","evidence_level":"中","settle_metric":"Delivery 與 Mobility 的固定匯率成長差","if_then":["如果 Delivery 成長連 2 季低於 18%，則停止加碼","如果兩項業務同時回到 20% 以上，則維持原倉位計畫"],"evidence_refs":["competitive_share_entrants#3","regulatory_antitrust#1"]},{"axis":"現在就賣與現在就買的最強論證","cause":"新證據","prior_field":null,"side_a":"賣：便宜來自未扣股份報酬的分母，Mobility 供給問題由巴西擴大到印度與加拿大，上季說美國加速卻放緩，Delivery Hero 對價未知，股價低於 52 與 104 週線。","side_b":"買：扣股份報酬後 FCF 殖利率仍有 5.7%，訂單成長 20%，Q4 EPS 指引年增 34% 至 39%，自駕仍不到總趟次 0.5%。","ruling":"不賣。賣方論點多數是風險窗在 2028 年後或需要 Q4 驗證，現價已反映部分疑慮；因此分兩批建立，第二批等 Q4。","evidence_level":"中","settle_metric":"2027 年 2 月 Q4 財報","if_then":["如果 Q4 訂單與 Mobility 達標，則買第二批","如果股價跌破 59.83 美元但基本面無損，則分批反買","如果股價先漲而 Q4 數據未到，則不追"],"evidence_refs":["end_markets#0"]}],"triggers":[{"n":1,"text":"Q4 財報驗證訂單成長與利潤率","type":"假設驗證","maps_to":"H1","metric":"總訂單固定匯率年增率；Adjusted EBITDA 占訂單","threshold":"18% 以上；不低於 4.6%","action":"達標則買第二批","source_freq":"公司季報，每季","date":"2027-02"},{"n":2,"text":"Mobility 成長放緩","type":"風險","maps_to":"R1","metric":"Mobility 固定匯率訂單年增率","threshold":"低於 15% 連 2 季","action":"停止加碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["supply_demand_durability#1","end_markets#0"]},{"n":3,"text":"Mobility 惡化到需要降低部位","type":"減碼","maps_to":"R1","metric":"Mobility 固定匯率訂單年增率；分部營業利益率","threshold":"低於 13% 連 2 季，或利潤率低於 7%","action":"減碼一半","source_freq":"公司季報，每季","date":null},{"n":4,"text":"自駕城市訂單轉負","type":"Single Thing","maps_to":"R3","metric":"美國自駕已營運城市 Mobility 訂單年增率","threshold":"轉負連續 2 季","action":"清倉","source_freq":"法說分城市說明與第三方數據，每季","date":"2028-12","evidence_refs":["substitute_technology#0","geo_supply_chain#2"]},{"n":5,"text":"Delivery Hero 槓桿與時程","type":"風險","maps_to":"R2","metric":"淨負債對年化 Adjusted EBITDA；交割時間","threshold":"高於 2.5 倍，或交割延後超過 2027 年底","action":"減碼一半","source_freq":"公司季報與 8-K，每季","date":"2027-12","evidence_refs":["major_events#0","ma_merger#1"]},{"n":6,"text":"Uber One 訴訟進展","type":"風險","maps_to":"R4","metric":"法院命令或和解內容；會員數","threshold":"須變更計費與取消流程且會員數季減；或出現刑事介入","action":"民事不利結果減碼一半，刑事介入清倉","source_freq":"法院文件與公司季報，事件驅動","date":null,"evidence_refs":["regulatory_antitrust#2","lawsuit_class_action#1"]},{"n":7,"text":"油價與關稅未能吸收","type":"風險","maps_to":"R5","metric":"Adjusted EBITDA 占訂單","threshold":"低於 4.6% 連 2 季","action":"停止加碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]},{"n":8,"text":"價跌而基本面無損","type":"加碼","maps_to":"H1","metric":"股價；總訂單固定匯率年增率","threshold":"股價低於 59.83 美元，且訂單年增 18% 以上","action":"分批反買","source_freq":"每日股價與季報","date":null},{"n":9,"text":"第二批買進條件","type":"估值rearm","maps_to":"H1","metric":"Q4 訂單與 Mobility 固定匯率成長","threshold":"訂單 18% 以上，Mobility 17% 以上","action":"買第二批","source_freq":"公司季報","date":"2027-02"},{"n":10,"text":"股價超過自身合理倍數","type":"減碼","maps_to":"H1","metric":"股價對 FY2027E 共識 EPS 的倍數","threshold":"26 倍，約 114.66 美元","action":"減碼三分之一","source_freq":"每日股價","date":null},{"n":11,"text":"年度複審","type":"複審日期","maps_to":"H2","metric":"自駕車隊規模與融資條款","threshold":"2027 年底 2,000 輛進度","action":"重做情境樹","source_freq":"年度","date":"2027-11-08"}],"kill_metrics":[{"metric":"總訂單固定匯率年增率","bear_threshold":"低於 15% 連 2 季","window":"2027 全年","source":"公司季報","last_status":"ok"},{"metric":"Mobility 固定匯率訂單年增率","bear_threshold":"低於 13% 連 2 季則減碼","window":"2027 全年","source":"公司季報與 10-Q","last_status":"warning"},{"metric":"Adjusted EBITDA 占訂單","bear_threshold":"低於 4.6% 連 2 季","window":"2027 全年","source":"公司季報","last_status":"ok"},{"metric":"美國自駕已營運城市 Mobility 訂單年增率","bear_threshold":"轉負連 2 季則清倉","window":"至 2028 年底","source":"法說說明與第三方數據","last_status":"unknown"},{"metric":"淨負債對年化 Adjusted EBITDA","bear_threshold":"高於 2.5 倍則減碼","window":"Delivery Hero 交割後 4 季","source":"公司季報","last_status":"ok"}],"action_conditions":{"rearm_trigger":"Q4 財報固定匯率訂單成長達 18% 以上，且 Mobility 固定匯率成長回到 17% 以上，才買第二批；否則停止加碼","exec_line":"現價附近先買目標部位的一半；2027 年 2 月 Q4 財報達標再買另一半。股價跌破 59.83 美元而訂單成長仍達 18% 則分批反買，未經驗證的上漲不追。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2028 年後才能驗證的自駕替代風險，連同 Mobility 的短期供給問題一起壓進倍數；現價只隱含 FCF 永續成長 2～3%，而 Q3 訂單仍成長 20%、Q4 EPS 指引年增 34% 至 39%。","momentum_overheated":false,"cycle_gates_pass":null},"thesis":{"H":[{"id":"H1","text":"訂單維持高成長，利潤率繼續提升。","2y":"FY2027 非 GAAP EPS 達 4.0 美元以上，訂單固定匯率成長維持 15% 以上。","5y":null,"10y":null,"threshold":"訂單固定匯率年增 15% 以上；Adjusted EBITDA 占訂單不低於 4.6%；FY2027 EPS 達 4.0 美元（約共識 4.41 美元的九成）。","source":"公司季報與法說","drift_rule":"TTM 偏離門檻連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"},{"id":"H2","text":"自駕放量後，Uber 仍是主要需求入口。","2y":null,"5y":"到 2031 年自駕趟次利潤率與人類司機相當，車隊資金以第三方為主。","10y":null,"threshold":"2027 年底 2,000 輛以上；2028 年起車隊資金以第三方為主；自駕城市 Mobility 訂單維持年增；單車利用率高於自營 30%。","source":"公司法說與簡報；Waymo 與 Tesla 營運數據","drift_rule":"連 4 季偏離 5% 為削弱，連 6 季偏離 10% 為反轉。"},{"id":"H3","text":"滲透率提升與品類延伸支撐長期成長。","2y":null,"5y":null,"10y":"2036 年前十大市場滲透率達 20% 以上，雜貨與零售成為重要獲利來源。","threshold":"滲透率 20% 以上（現約 10%）；Uber One 占訂單維持 50% 以上。","source":"公司法說與年報","drift_rule":"跨 2 個年度偏離為削弱，跨 3 個年度為反轉。"}],"R":[{"id":"R1","text":"Mobility 供給缺口由巴西擴大到印度與加拿大，補貼轉向司機後可能壓低成長與利潤。管理層的短期歸因未證，連 2 季未改善即視為歸因不成立。","h_ref":"H1","clock":"⚡","threshold":"Mobility 固定匯率訂單年增低於 13% 連 2 季，或分部營業利益率低於 7%。","evidence_refs":["supply_demand_durability#1","end_markets#0"]},{"id":"R2","text":"Delivery Hero 全現金收購金額超過市值 5%，交割預計 2027 下半年，需反壟斷核准；總對價事實表未涵蓋，整合與槓桿風險未定價。","h_ref":"H1","clock":"🔥","threshold":"交割後淨負債對年化 Adjusted EBITDA 高於 2.5 倍，或交割延後超過 2027 年底。","evidence_refs":["major_events#0","major_events#1","major_events#2","ma_merger#0","ma_merger#1"]},{"id":"R3","text":"自駕的資本與安全負擔回到 Uber：早期車輛自擔，100 億美元承諾的損益影響未揭露；合作夥伴 Avride 遭 NHTSA 調查 16 起事故，代表夥伴安全事件會牽動平台。","h_ref":"H2","clock":"🐢","threshold":"自駕投入超過 100 億美元承諾，或 2028 年車隊融資仍以 Uber 資產負債表為主。","evidence_refs":["product_recall_warning#0"]},{"id":"R4","text":"監管與訴訟：FTC 加 21 州與 DC 控告 Uber One，屬民事案件，Uber One 占過半訂單；DOJ、FTC 另有多項調查，競爭法趨嚴。和解時點與金額事實表未涵蓋。","h_ref":"H1","clock":"🔥","threshold":"法院或和解要求變更 Uber One 計費與取消流程且會員數季減；或出現刑事介入。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#3","lawsuit_class_action#0","lawsuit_class_action#1"]},{"id":"R5","text":"油價、零件關稅與地緣衝突推高司機成本，減少供給時數，影響在新興市場最明顯。不預測油價，以公司損益是否吸收為判準。","h_ref":"H1","clock":"⚡","threshold":"Adjusted EBITDA 占訂單低於 4.6% 連 2 季。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]}],"single_thing":{"description":"公司或第三方數據證實，美國自駕已營運城市的 Uber Mobility 訂單年增率連續兩季轉負。","why_fatal":"這是情境樹最大的單一敏感項：Base 與 Bear 的終端 EPS 差 3.55 美元、終端倍數差 5 倍，主要取決於自駕是否繞過平台。CFO 2026-08-05 稱相關城市占美國訂單 30%、獲利 25%，一旦負成長，市場會把其他城市按相同路徑定價。","if_happens":"清倉，並重做情境樹，不等下一季確認。","how_monitor":"每季法說的美國分城市說明；第三方 App 與信用卡數據；Waymo 與 Tesla 單車日趟次；Waymo 2028 年 1 月起的奧斯汀與亞特蘭大安排。","probability":"12 至 24 個月內約 15%"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":15.55,"peg_fy2":0.56,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":4.73,"FY2026E":3.36,"FY2027E":4.41,"FY2028E":5.5},"fy_end_month":12,"eps_basis":"共識來自 Koyfin 快照；依 Q3 的 0.88 美元與 Q4 指引 0.95 至 0.99 美元反推，口徑應為非 GAAP。FY2025A 的 4.73 美元為 GAAP 稀釋 EPS，含稅務與投資重估，非 GAAP 基期事實表未涵蓋，不可與 FY2026E 相比計算成長率。EPS 分析師家數事實表未涵蓋；營收共識為 46 與 48 家。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Zoox 在拉斯維加斯上線 Uber，Motional 隨後轉為全無人營運","impact":"中","watch":"單車日趟次與上線時程"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年展望","impact":"高","watch":"訂單成長 18% 以上、Mobility 17% 以上、EPS 0.95 至 0.99 美元"},{"date":"2027-Q3","date_precision":"quarter","type":"regulatory","event":"Delivery Hero 反壟斷審查與交割，公司預期 2027 下半年完成","impact":"高","watch":"總對價、處分條件、交割後淨負債倍數"},{"date":"2027-12","date_precision":"month","type":"product","event":"全無人車輛達 2,000 輛以上的目標期限","impact":"中","watch":"車輛數、利用率與第三方融資進度"},{"date":"2028-01","date_precision":"month","type":"other","event":"Waymo 計畫在奧斯汀與亞特蘭大自營（二手資料，未核原文）","impact":"高","watch":"Uber 在兩地的 Mobility 訂單年增率"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2028 年後才能驗證的自駕替代風險，連同 Mobility 的短期供給問題一起壓進倍數；現價只隱含 FCF 永續成長 2～3%，而 Q3 訂單仍成長 20%、Q4 EPS 指引年增 34% 至 39%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟢', moat_trend='→', week26=-9.09, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
