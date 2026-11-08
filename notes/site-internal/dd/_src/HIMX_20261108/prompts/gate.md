你是 DD 管線 v20 的判斷層閘（gate），標的 HIMX（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（39 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝246.8 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Himax Q3 2026 新聞稿（2026-11-05）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi1_gaap`（q1_business）｜GAAP 毛利率＝34.2 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Himax Q3 2026 新聞稿（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：公司指引約 34%，符合
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝9.2 %（營業利益 22.7m USD）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Himax Q3 2026 新聞稿；營業費用 61.8m（QoQ +21.9%，含員工獎金 11.9m 對 Q2 的 0.2m）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi3_ads`（q1_business）｜稅後淨利／每 ADS 盈餘＝18.6 USD m；EPS 10.7 美分／ADS｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Himax Q3 2026 新聞稿（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：高於公司指引 8.0–10.0 美分
- `f_kpi5_q4_2026`（q1_business）｜管理層指引：Q4 2026＝營收 QoQ −22% 至 −26%（約 182.6–192.5m USD，由 Q3 回推）；毛利率持平至微升；EPS 4.5–6.5 美分／ADS（不含預計 Q4 完成的出售利益，稅前約 23–24m、稅後約 19–20m） 區間｜期間與口徑：Q3 2026（公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Himax Q3 2026 新聞稿（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（公告於 2026-11-05））
- `f_peer_himx_gross_margin_pct`（q2_moat）｜HIMX 毛利率＝31.07 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HIMX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_himx_operating_margin_pct`（q2_moat）｜HIMX 營業利益率＝4.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HIMX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3034_tw_gross_margin_pct`（q2_moat）｜3034.TW 毛利率＝39.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3034.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3034_tw_operating_margin_pct`（q2_moat）｜3034.TW 營業利益率＝19.03 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3034.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_himx_fcf_margin_pct`（q2_moat）｜HIMX FCF 利潤率＝3.25 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HIMX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3034_tw_fcf_margin_pct`（q2_moat）｜3034.TW FCF 利潤率＝14.97 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3034.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝0.47 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.3 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝2.45 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（0.47 → 0.47）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（1.3 → 1.3）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（2.45 → 2.45）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝949.39 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（2 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1230.6 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（2 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_23_9m_3_9m`（q4_capital）｜自由現金流（營業現金流 23.9m − 資本支出 3.9m，推算值，公司未報）＝20.0 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Himax Q3 2026 新聞稿（OCF、capex）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi6`（q1_business）｜現金及其他金融資產＝285.3 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Himax Q3 2026 新聞稿（期間派發股利 44m）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝351.51 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 636.83、現金 285.32（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.968 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝174.43 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝8.49 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝18.06 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 0.47，分子＝快照價 8.49｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝40.43 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.69 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.09 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.93 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝1832.39 USD m｜期間與口徑：2026-11-08／市值 1480.88 ＋ 淨負債 351.51｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-51.44 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝28.68｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 8.49 / W52 11.71 / W104 9.87 / W250 7.58 / W250 13週斜率 0.2%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝7.58 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 0.47 → 0.47（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）

### findings_digest 中方向為負或來源衝突的條目（23 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F 風險因素：中國大陸面板廠扶植本土 IC 供應商的政策對 Himax 構成重大挑戰且可能加劇競爭；部分對手隸屬面板客戶，具早期取得產品藍圖與 design-in 優先權的優勢。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-03-27）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：20-F 風險因子：數家面板廠具自行設計能力，若客戶自研可替代產品將減少或停止採購。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-03-27）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：2025年Customer A（含關係企業）占營收24.0%（2023年28.7%、2024年26.4%）；Customer C 占7.8%；前兩大合計逾33%，前十大合計71.3%。
  - 來源：SEC EDGAR 20-F FY2025, Item 4 Customers（as_of 2026-03-27）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：2025年底對Customer A應收帳款5,780萬美元，占應收帳款淨額約28.8%；公司自述集中度提高信用風險，且曾對部分客戶延長付款條件。
  - 來源：SEC EDGAR 20-F FY2025, Item 3.D Risk Factors（as_of 2026-03-27）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2025年約73.8%營收來自總部在中國的客戶（2024年73.4%）。
  - 來源：SEC EDGAR 20-F FY2025, Item 3.D Risk Factors（as_of 2026-03-27）｜affects：thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Himax 管理層表示 AI 需求使成熟製程的晶圓代工、封裝、測試產能吃緊，推升製造與採購成本、拉長交期
  - 來源：Himax Q4 2025 / 2026 earnings call coverage (MarketBeat)（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：Himax Q1 2026 營收年減 7.5% 至 1.99 億美元，近兩年營收年均下滑 5.2%（StockStory 式分析）
  - 來源：Barchart, Himax Q1 coverage（as_of 2026-05-08）｜affects：thesis.H、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：20-F 提及部分產品或技術對特定客戶可能需額外出口許可，受美國商務部 BIS 的 EAR 管轄（出口管制屬產業特定監管風險）。
  - 來源：搜尋摘要（轉述 Himax FY2025 20-F）（as_of 2026-03-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Himax 20-F 風險因子：產品／技術對部分客戶可能需額外 EAR 出口許可；若客戶或晶圓代工、封測供應商被列入 BIS Entity List，公司可能須暫停銷售或服務，並可能出貨延遲。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-03-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：Himax 20-F 風險因子：美國或他國可能對台灣公司產品課新關稅，並可能促使客戶將半導體供應鏈移出高地緣風險地區。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-03-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 大尺寸驅動 IC 營收年減 28.0% 至 $90.7M，公司歸因於關稅與地緣不確定性等弱總體環境；中小尺寸年減 8.0% 至 $575.1M，智慧手機與平板受關稅相關不確定性影響。
  - 來源：SEC EDGAR 20-F FY2025 Item 5（as_of 2026-03-27）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Himax 20-F(FY2019)揭露 TSMC 與 Vanguard 歷來製造其絕大部分晶圓，晶圓代工集中於台灣。
  - 來源：Himax Form 20-F FY2019 (SEC)（as_of 2020-03-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Himax 20-F(FY2017)揭露部分產品只在單一晶圓廠生產，更換晶圓廠或製程需數季驗證。
  - 來源：Himax Form 20-F FY2017 (SEC)（as_of 2018-03-31）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：20-F 風險因素：數家面板廠具自行設計能力，若客戶成功自研可替代本公司產品的半導體，將減少或停止採購。
  - 來源：SEC EDGAR 20-F FY2025 Item 3 Risk Factors（as_of 2026-03-27）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：20-F 競爭章節：產業特徵為持續技術變遷、標準演進與平均售價下滑。
  - 來源：SEC EDGAR 20-F FY2025 Item 4 Competition（as_of 2026-03-27）｜affects：moat_trend
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：二手評論稱 Largan 成立 CPO 緊急產線、定位為 Himax 在光學元件上的替代者；FOCI 稱 Himax 目前是其 FAU 唯一供應商，長期不排除第二來源
  - 來源：hntrbrk.com Himax: Stealth Supplier for Nvidia's Optics Revolution（as_of 2026-06-01）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：公司 2026-11-05 公布 Q4 指引：營收季減 22%～26%、毛利率持平至略升、EPS 每 ADS 4.5～6.5 美分（不含 7 月宣布之擬議資產出售可能利得）
  - 來源：Himax Form 6-K Exhibit 99.1 (Q3 2026 results)（as_of 2026-11-05）｜affects：valuation、thesis.R
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：TSMC 預計 2028 年前將 Fab14 12 吋成熟製程產能減少 15–20%（Counterpoint 估約 5 萬片/月），騰出空間給先進封裝；VIS 承接部分成熟製程
  - 來源：rallies.ai: TSMC to Slash Fab14 Capacity by 15–20% and Deploy $52–56 B Capex Overseas（as_of 2026-01-25）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#1`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Himax 管理層表示成熟製程晶圓代工、封裝、測試產能吃緊，限制平板 IC 出貨並推升成本
  - 來源：Himax Q2 2026 Earnings Call Transcript (Webull)（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#2`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：DRAM 合約價 1Q26 季增約 90–95%、2Q 已鎖定約 +30%；TrendForce 稱 AI 擠壓成熟製程產能，8/12 吋晶圓代工價可能高檔到 2027（未找到現貨價序列，最新資料約 2026-06）
  - 來源：iconnect007 / TrendForce — AI Server Demand to Drive Memory Contract Price Increases in 2Q26（as_of 2026-04-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Himax 2023 全年毛利率 27.9%，前一年 40.5%；2023 Q2 單季毛利率 21.7%（Q1 28.1%），Q4 回升至 30.3%（來源為搜尋摘要轉述，未讀原頁）
  - 來源：Himax Q4 2023 earnings call / press release (alphaspread, SEC 6-K exh_991)（as_of 2024-02-08）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：SOX 2022 年自年初高點跌約 36%（盤中最深約 42–44%），高點約 2022 年 1 月初、谷底約 2022 年 10 月，約 9 個月
  - 來源：247wallst, Chip Stocks Are Bleeding Today. The 2018 and 2022 Selloffs（as_of 2026-05-12）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Himax 2023 Q2 毛利率 21.7%、全年 27.9% vs 40.5%
  - 來源：SEC 6-K exhibit 99.1 Q4 2023（as_of 2024-02-08）｜affects：thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":28.5,"bear_5y_price":3.6,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":40.9,"ev5y_pct":45.4,"irr_base_pct":7.1,"asym_ratio":2.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":0.47,"pe":18.06,"basis":"FY2026E 共識 EPS（2026-11-07 快照，未隨 Q4 指引調整），P/E 為現價除以當年度 EPS，與終端年倍數同為當年度口徑。"},"eps":{"bull":[0.8,1.2,1.5,1.75,1.9],"base":[0.48,0.6,0.72,0.83,0.92],"bear":[0.28,0.2,0.2,0.25,0.3]},"pe":{"bull":15,"base":13,"bear":12},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":2.968,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":4},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HIMX_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Karen Tiao｜guidance：Q3 營收季增 7% 至 11% 的財測（原話："We expect Q3 revenue to increase 7% to 11%"）
- 2026-08-06｜Karen Tiao｜guidance：Q3 毛利率財測約 34%，視產品組合而定（原話："Gross margin is expected to be around 34%, depending on the"）
- 2026-08-06｜Karen Tiao｜guidance：Q3 每稀釋 ADS 獲利財測 0.08 至 0.10 美元（原話："attributable to shareholders is estimated to be in the"）
- 2026-08-06｜Karen Tiao｜margin：Q3 員工獎金費用估 1,180 萬美元、每 ADS 稅前 0.068 美元，已含在 EPS 財測內；前三季每季約 20 萬（原話："be $11.8 million, representing $0.068 per diluted ADS"）
- 2026-08-06｜Karen Tiao｜margin：Q2 毛利率 33.1%，高於財測約 32%（原話："Gross margin was 33.1%,"）
- 2026-08-06｜Karen Tiao｜margin：Q2 營業利益率 10.8%（前季 5.1%），管理層歸因於營收與毛利率提高（原話："representing an operating margin of 10.8%"）
- 2026-08-06｜Jordan Wu｜margin：管理層與客戶協商調價以分攤成本，部分已在 Q2 生效（原話："Some adjustments took effect in the second quarter"）
- 2026-08-06｜Jordan Wu｜margin：2027 毛利率方向：管理層相信今年改善的趨勢明年可能延續（非正式財測）（原話："and we believe the trend is likely to continue next year."）
- 2026-08-06｜Jordan Wu｜risk：成熟製程晶圓代工、封測產能吃緊，成本上升（原話："we are experiencing higher manufacturing and procurement"）
- 2026-08-06｜Jordan Wu｜risk：管理層預期供應環境近期仍具挑戰（原話："We expect the supply environment to remain challenging in"）
- 2026-08-06｜Jordan Wu｜risk：明年晶圓廠仍將漲價，管理層稱需持續管理（原話："indicating further price hikes next year, certainly all"）
- 2026-08-06｜Karen Tiao｜risk：Q2 營運現金流含台灣新政策遞延約 1,100 萬美元稅款一年；不含遞延約 650 萬美元（原話："defer approximately $11.0 million of this payment for 1 year"）
- 2026-08-06｜Karen Tiao｜capital_allocation：Q3 現金將因 7/10 支付 4,400 萬美元年度股利而下降（原話："the payment of the $44 million for the annual dividend to"）
- 2026-08-06｜Karen Tiao｜capital_allocation：擬處分一家權益法被投資公司，預計稅前利得約 2,300 萬至 2,400 萬美元，預計 Q4 完成，尚待法規核准（原話："recognize a pretax gain of approximately $23 million to $24"）
- 2026-08-06｜Karen Tiao｜capital_allocation：約一年前調整庫存策略，選擇性備貨；庫存 1.515 億美元，與前季持平（原話："selectively building inventory in anticipation of the"）
- 2026-08-06｜Jordan Wu｜guidance：Q3 大尺寸驅動 IC 預期季減個位數（原話："driver IC sales are expected to decline by single digit"）
- 2026-08-06｜Jordan Wu｜guidance：Q3 中小尺寸驅動 IC 預期季增高個位數（原話："display IC business is expected to increase by high single"）
- 2026-08-06｜Jordan Wu｜guidance：2026 全年車用驅動 IC 預期雙位數成長（原話："We expect our full year 2026 automotive IC sales"）
- 2026-08-06｜Jordan Wu｜guidance：管理層表示不提供超過一季的正式財測，但對明年營收成長有信心（原話："robust sales growth for next year with continuously"）
- 2026-08-06｜Jordan Wu｜guidance：2027 展望明確排除 CPO 貢獻（原話："So what I'm about to say below does not include"）
- 2026-08-06｜Jordan Wu｜guidance：2027 非驅動 IC 占營收預期由約 20% 升至接近 30%（不含 CPO）（原話："revenue contribution approaching 30% from around 20% at"）
- 2026-08-06｜Jordan Wu｜guidance：2027 車用展望的前提假設：全球車輛出貨持平（原話："we are assuming a flattish year for global vehicle shipment"）
- 2026-08-06｜Karen Tiao｜margin：數字口徑：車用事業（DDIC、TDDI、Tcon、OLED IC）占 Q2 營收超過 50%（原話："representing well over 50% of total"）
- 2026-08-06｜Jordan Wu｜commitment：CPO 2027 出貨預期顯著高於 2026（原話："we expect our shipments in 2027 to be significantly higher"）
- 2026-08-06｜Jordan Wu｜commitment：CPO 2026 下半年主要目標為量產準備與客戶認證，Gen 1、Gen 2 於 Q3 開始工程量產爬坡（原話："have begun engineering production ramps as scheduled in the"）
- 2026-08-06｜Jordan Wu｜commitment：CPO 2027 成長基期低；即使最保守情境仍有實質貢獻，貢獻幅度取決於客戶量產時程（原話："significant growth next year, but we'll be comparing with"）
- 2026-08-06｜Jordan Wu｜commitment：CPO 最保守情境下 2027 起對財務（尤其獲利）有實質貢獻（原話："make a meaningful contribution to our financials"）
- 2026-08-06｜Jordan Wu｜guidance：CPO 2026 全年營收貢獻仍有限（原話："revenue contribution during this year will still be limited."）
- 2026-08-06｜Jordan Wu｜product：CPO 敘事：管理層稱對量產成功的信心較一季前又升一級（原話："It has surely risen to another level compared to even just"）
- 2026-08-06｜Jordan Wu｜competition：CPO 競爭：管理層稱自己據其所知是唯一採晶圓級光學的供應商（原話："providing optics using wafer-level optics or wafer-based"）
- 2026-08-06｜Jordan Wu｜competition：管理層認為 CPO 市場夠大，數年後不會只有 Himax 與 FOCI 一家供應商（原話："and FOCI will be the only player, the only vendor in the"）
- 2026-08-06｜Jordan Wu｜competition：車用 HUD Tcon 等進階功能被管理層稱為對抗競爭者的護城河（原話："strong moat that helps fend off competitors."）
- 2026-08-06｜Jordan Wu｜competition：Q&A 稱 Himax 是 LTDI 解決方案目前市場上的獨家供應商（原話："exclusive supplier of the solution in the market right now"）
- 2026-08-06｜Jordan Wu｜product：準備稿口徑：超大尺寸車用面板每片 LTDI 用量（Q&A 另稱至少 5 顆含 1 顆 Tcon）（原話："4 or more LTDI chips and in some cases, more than 10"）
- 2026-08-06｜Jordan Wu｜product：車用 OLED 大量放量預期落在明年下半年起並延伸至 2028（原話："major ramping expected starting from probably second half"）
- 2026-08-06｜Jordan Wu｜product：LCoS 目前仍在爭取設計案，管理層稱明年不會是量產題材；WiseEye 才是明年題材（原話："win. So that is not going to be a mass production story for"）
- 2026-08-06｜Jordan Wu｜customer：一家全球領導品牌已推出採用 WiseEye 的智慧眼鏡（原話："Recently, a leading global brand just launched a smart"）
- 2026-08-06｜Jordan Wu｜customer：含超大規模雲端業者在內的新客戶進入智慧眼鏡，部分專案 2027 量產（原話："are now entering smart glasses market with some projects"）
- 2026-08-06｜Jordan Wu｜commitment：智慧眼鏡營收量化時程：管理層稱再給 2 季以上才能較好量化（原話："give us 2 or more quarters, we should be able to quantify"）
- 2026-08-06｜Jordan Wu｜customer：Q3 平板 IC 預期季減，原因為產能限制（原話："are expected to decrease sequentially as capacity"）
- 2026-08-06｜Karen Tiao｜customer：Q2 大尺寸驅動 IC 下滑，管理層歸因於面板廠先前提前拉貨（原話："panel makers pulling forward their inventory purchases for"）

### 問答異常語氣（迴避／改口／保留）
- HIMX_Q2_2026_Earnings_Call_20260806.md｜問：Nomura 追問『2027 CPO meaningful 如何定義』並請提供 2027 整體展望｜答法：不給 CPO 數字，稱 meaningful 即 meaningful、非低個位數百分比；2027 整體展望只給定性、並將 CPO 排除在外；稱公司通常不提供超過一季的財測
- HIMX_Q2_2026_Earnings_Call_20260806.md｜問：Morgan Stanley 追問 CPO 競爭者與 Himax 的關鍵優勢｜答法：稱公司政策是不評論競爭，並稱不公開談技術優劣比較；改談市場夠大、聚焦自身驗證與量產
- HIMX_Q2_2026_Earnings_Call_20260806.md｜問：線上問題：2027 智慧眼鏡營收走勢與量｜答法：稱主要客戶尚未回饋晶片需求數量，不給量化；表示需 2 季以上才能量化

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 1 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 2 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 2 | 3 |
| cyclical_supply_discipline_capacity | found | 2 | 2 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260703","verdict":"觀望","role":"候選/追蹤池","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"車用顯示領先（TDDI 50%+）維持，單車搭載量成長帶動基本盤溫和復甦","columns":{"2Y 驗證點":"車用 IC FY26 YoY &gt; +10%；Q2-Q4 26 GM 回升至 32%+","5Y 驗證點":"車用 IC 占比 ≥ 55%；OLED/LTDI TDDI 接棒第二成長曲線","具體數字門檻":"車用 IC FY26 &gt; $460M（+10% YoY）；GM FY27 ≥ 33%","漂移觸發（QC-35 分級）":"車用 IC 連 4 季 YoY &lt; +5% → 削弱（5Y 假設連 4 季）"}},{"id":"H2","text":"WLO/LCoS/CPO/WiseEye AI 期權至少一項變現（binary、時程未證實）","columns":{"2Y 驗證點":"2H26 AR 眼鏡量產客戶點名 + WLO/LCoS 季營收 &gt; $10M；或 CPO 進 Nvidia 供應鏈","5Y 驗證點":"2028-30 光學/CPO 段占營收 ≥ 15%","具體數字門檻":"2026 光學/CPO 占比 ≥ 3%；2028 ≥ 10%","漂移觸發（QC-35 分級）":"連 3 季量產時程再滑動 + 無客戶點名 → 期權折現率上調（Bull 機率下修）"}},{"id":"H3","text":"正常化毛利率結構性 ~31-33%（不回 40% 峰值），正常化 ROIC 8-10%","columns":{"2Y 驗證點":"循環中段 GM 穩定 31-33%、OM 回到 10-12%","5Y 驗證點":"穿越週期 GM 中樞 ~32%、ROIC ~9%","具體數字門檻":"FY27 GM &gt; 32%；正常化 OM &gt; 10%","漂移觸發（QC-35 分級）":"連 4 季 TTM GM &lt; 30% 且同業持平 → 結構性侵蝕（Bear 上調）"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":5.2,"ev5y_pct":30.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"候選/追蹤池","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.9,"ev5y_pct":30.0,"irr_base_pct":5.2,"max_dd_pct":-55.0,"bull_5y_price":27.0,"bear_5y_price":6.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":13.15,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"HIMX","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Himax Technologies, Inc."},"oneliner":"車用顯示驅動龍頭遇上庫存急修正，Q4 營收指引季減兩成多；現價大致只付了本業，CPO 仍待量產驗證，等 2027 年初的訂單與出貨資料再談進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺面板廠與車用一階供應商的錢，產品是顯示驅動與時序控制晶片，利潤卡在晶圓代工漲價與面板廠議價之間。Q3 毛利率 34.2%、營益率 9.2%，Q4 營收指引季減 22% 至 26%。","reasoning":"2026 Q3 營收 246.8m 美元：中小尺寸驅動 IC 176.8m（71.6%），非驅動 IC 51.0m（20.7%），大尺寸驅動 IC 19.0m（7.7%）。營益率 9.2% 被 Q3 認列的員工獎金 11.9m 壓低，加回約 14.0%。Q4 指引約 182.6m 至 192.5m，主因面板廠急砍車用驅動 IC 訂單。全年營收推算約 861m（Q1 199m、Q2 約 227.5m、Q3 246.8m、Q4 中點約 187.6m），比 FY2025 的 832m 多約 3.5%。單點依賴屬集中度風險，不是護城河證據：客戶 A 占 2025 年營收 24.0%，前十大 71.3%，中國總部客戶 73.8%。供需耐久性判為週期性將反轉：Q2、Q3 的車用拉貨已經反轉；成熟製程吃緊較持久，但對 Himax 是成本壓力，不是需求順風。產業時鐘判收縮，依據是 10 月車用訂單急修正與中國內銷前九月年減 22.4%，不是股價。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_ads","f_kpi5_q4_2026"],"verdict_values":{"revenue_quality":"產品銷售為主，沒有訂閱或長約收入；DSO 93 天，一年前 87 天，收款條件略為拉長。","unit_econ_note":"無晶圓廠模式，Q3 資本支出 3.9m，占營收約 1.6%；研發密度 TTM 19.88%，真正的再投資走費用。","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"需求量循環：營收由 FY2022 的 1,201m 連三年降到 FY2025 的 832m，年度毛利率在 27.9% 到 40.5% 之間擺動；不符合商品型的兩項以上條件。CPO 是另外一條未驗證的成長線，不隨循環判讀。"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉：管理層 2026-11-05 稱面板廠在中國十一長假後急砍 Q4 預測；中汽協資料顯示前九月內銷年減 22.4%、出口年增 65.8%，歐盟貿易壁壘與新能源車退稅下調使出口轉弱。","bargaining":{"up":"對晶圓代工與封測弱勢：2027 年漲價已公告，公司把確保產能列為第一優先。","down":"對面板廠議價中等：前十大客戶占 71.3%，部分面板廠可自研；成本由雙方分攤，2026 Q2 起部分調價生效。","geo":"中國總部客戶占 73.8%，供應鏈以台灣為主，同時受出口管制與關稅影響。"},"profit_pool_dir":"事實表未涵蓋五年利潤池序列；方向上車用時序控制與區域調光的利潤占比上升，消費性驅動 IC 下降。","tam_table":{"expanded":false,"reason":"事實表沒有 TAM、SAM、滲透率與利潤池序列。CPO 屬新品類本應展開，但證據包未涵蓋，標為資料缺口。"}}}},"q2_moat":{"verdict":"護城河方向穩定，等級偏低：車用時序控制與區域調光的領先在擴大，消費性驅動 IC 與本土替代在侵蝕，兩者相抵。","reasoning":"機制是車規認證週期長，加上面板廠、車廠與一階供應商的雙層關係，換供應商要重走驗證。20-F 稱車用 DDIC 約 40%、TDDI 過半、區域調光 Tcon 更高。同業落差明顯：TTM 毛利率 31.07% 對聯詠 39.10%，營益率 4.94% 對 19.03%，低 14.09 個百分點；事實表只有單期 TTM，無法判斷落差是否收窄。最大客戶占比由 28.7% 降到 24.0%，不能判為擴大。管理層用車用成長贏過全球汽車出貨來論證未失份額，這個比較沒有對照同業，且 Q2、Q3 含客戶超額拉貨，不足以證明份額。CPO 的領先只在工程驗證階段，尚無量產營收。當期 ROIC 無法計算，投入資本明細事實表未涵蓋。","fact_refs":["f_peer_himx_gross_margin_pct","f_peer_himx_operating_margin_pct","f_peer_3034_tw_gross_margin_pct","f_peer_3034_tw_operating_margin_pct","f_peer_himx_fcf_margin_pct","f_peer_3034_tw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"車規認證與長設計週期形成的轉換成本，加上車用時序控制、區域調光與 HUD 去畸變的功能整合；換供應商要在下一個車款重走驗證。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"擴大面：車用時序控制 2026 年預估成長逾 40%，Q4 再季增低雙位數，2026-08-06 Jordan Wu 稱 LTDI 為目前市場獨家供應。縮減面：客戶 A 占比由 28.7%、26.4% 降到 24.0%，FY2025 大尺寸驅動 IC 年減 28.0%、中小尺寸年減 8.0%，20-F 指中國面板廠導入本土 IC 已構成重大挑戰。執行力穩定，定價力穩定偏弱，合併判穩定。","competitor_notes":[{"name":"3034.TW","strategy_note":"聯詠是最直接的驅動 IC 對手，TTM 營益率高出約 14 個百分點，也正在加壓車用市場。"},{"name":"SIMO","strategy_note":"儲存控制晶片業者，業務不同，只當無晶圓廠獲利結構參考，不是份額對手。"},{"name":"AMBA","strategy_note":"邊緣 AI 視覺晶片與 WiseEye 部分重疊，高毛利仍虧損，說明邊緣 AI 要有規模才撐得起研發。"},{"name":"LSCC","strategy_note":"低功耗 FPGA，毛利率與現金流都高，是小型利基晶片的利潤結構參考，不是直接對手。"}],"threats":[{"level":"🔴","text":"中國面板廠扶植本土驅動 IC，隸屬面板客戶的對手能更早拿到產品藍圖。2025 年 73.8% 營收來自中國總部客戶，曝險最大。","p":"35%","evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#2"]},{"level":"🟡","text":"數家面板廠具自行設計能力，成功自研就會減少或停止採購。","p":"20%","evidence_refs":["customer_second_source#1","substitute_technology#0"]},{"level":"🟡","text":"產業長期平均售價下滑，前兩大客戶合計逾三成，對客戶 A 的應收占 28.8%，公司曾延長付款條件。","p":"50%","evidence_refs":["substitute_technology#1","customer_concentration_credit#0","customer_concentration_credit#1"]},{"level":"🟡","text":"CPO 光學元件已有對手正面競爭，二手評論指 Largan 切入、FOCI 長期不排除第二來源，管理層也承認長期不會有人獨占。","p":"40%","evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"低利益率×高周轉（投入資本事實表未涵蓋，周轉方向依無晶圓廠模式推定）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"車主用車、車廠與一階供應商定規格、面板廠付款，三環節都成立。每車顯示器與 IC 含量上升較確定，但整車需求正在轉弱，中國內銷前九月年減 22.4%。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一車款的設計案衡量：量產中車款換供應商要重新驗證，轉換成本高；下一車款就可重選，本土供應商有機會切入。重新認證週期的數字事實表未涵蓋。"},{"item":"價值鏈分配","level":"🔴","text":"上游代工與封測已公告 2027 年漲價，台積電也在縮減成熟製程產能；下游前十大客戶占 71.3%，部分具自研能力。Himax 夾在中間，TTM 營益率只有 4.94%，成本只能與客戶分攤。"},{"item":"社會容忍度","level":"🟢","text":"驅動 IC 占整車成本比重低，不是民生必需品定價，沒有社會或監管對漲價的限制；出口管制另列為風險項。"}],"roiic":"FY2022 至 FY2025 營收減少約 369m，營業利益減少約 213m，增量報酬為負，不具外推意義；投入資本明細事實表未涵蓋。","reinvest_rate":"FY2023 至 FY2025 自由現金流（129.3m、102.8m、119.5m）都高於淨利（50.6m、79.8m、43.9m），有形再投資率為負；成長靠費用化研發，折舊與營運資金明細事實表未涵蓋。","endo_ceiling":null,"formula_note":"內生成長率等於增量報酬乘以再投資率；兩項輸入都缺，故不給數字，只判定共識成長遠超任何由歷史再投資能支撐的水準。"}}}},"q3_growth":{"verdict":"五年後成長空間中等：車用時序控制與 LTDI 仍在滲透，CPO 是未經量產驗證的第二曲線，尚不足以判為寬。","reasoning":"共識三年 EPS 成長率以 FY2025 每 ADS 0.252 美元為基期、到 FY2028 的 2.45 美元，約 113%；這個數字不能用。基期是低點，FY2026 共識營收 949.39m 比已報三季加 Q4 指引中點約 861m 高約 10%，而三個年度的 EPS 共識近期修正都是 0，代表 Q4 利空尚未反映。缺口主要來自毛利率擴張與 CPO 貢獻，不是歷史再投資能支撐的成長。管理層稱 2027 年雙位數成長且不含 CPO，但要達到 +10%（約 947m），全年平均季營收要比 Q4 指引中點高約 26%。滲透率數字事實表未涵蓋，因此不給年數。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_q4_2026"],"verdict_values":{"growth":{"driver_mix":"量為主，來自車用顯示顆數與單車 IC 含量；價的部分是與客戶分攤代工漲價；併購與回購沒有貢獻。","runway_years":"車用時序控制與 LTDI 的滲透率事實表未涵蓋，不給年數。","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界無法給數字：增量報酬過去四年為負，有形再投資率為負，投入資本與折舊明細事實表未涵蓋。共識成長即使用較高基期 0.504 美元計算也約 69%，判定超過上界。","segments":[{"item":"大尺寸驅動 IC","value":"Q3 19.0m，占 7.7%；Q4 指引季增低雙位數，來自電視與顯示器舊產品出貨。"},{"item":"中小尺寸驅動 IC","value":"Q3 176.8m，占 71.6%；Q4 指引雙位數季減，車用、平板、手機都下滑。"},{"item":"非驅動 IC","value":"Q3 51.0m，占 20.7%；Q4 持平至略降；管理層目標 2027 年占比接近 30%，不含 CPO。"},{"item":"車用時序控制","value":"Tcon 占營收逾 10%，其中車用過半；2026 年預估成長逾 40%，Q4 季增低雙位數。"},{"item":"LTDI","value":"Q4 預期占營收逾 5%，季增個位數。"},{"item":"CPO","value":"工程量產爬坡中，2026 年貢獻有限；管理層稱 2027 年起有實質貢獻，但不給數字。"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 為 33.1% 對去年同期 31.2%，Q3 再升到 34.2%。"},{"item":"核心市占近 12 個月縮減","lit":null,"note":"事實表沒有份額時間序列，客戶 A 占比下滑不等於市占下滑。"},{"item":"提價後銷量下滑","lit":null,"note":"部分調價 Q2 生效，Q4 量縮主因客戶庫存，無法拆分。"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"共識三年 EPS 成長遠高於營收成長，差距超過 5 個百分點。"},{"item":"自由現金流對淨利連 2 年低於 0.75","lit":false,"note":"FY2023 至 FY2025 約為 2.56、1.29、2.72 倍。"},{"item":"員工股權費用占營收高於 5% 且上升","lit":false,"note":"2026 年獎金授予 13.3m，約占全年推算營收 1.5%。"},{"item":"市場萎縮或被替代技術壓縮","lit":false,"note":"車用顯示 IC 含量仍上升；面板廠自研是風險，尚未見營收侵蝕數字。"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數序列。"},{"item":"維持性資本支出占自由現金流高於 60%","lit":false,"note":"Q3 資本支出 3.9m，自由現金流約 20.0m。"},{"item":"停止投資且營收 3 年內下滑","lit":true,"note":"FY2023 至 FY2025 營收連三年下滑；無晶圓廠不適用新產能這一半，保守算亮燈。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置穩健但沒有創造額外價值：FY2023 至 FY2025 自由現金流都高於淨利，股利幾乎發光全年淨利，稀釋低，沒有併購與明顯回購。","reasoning":"FY2025 自由現金流 119.5m，淨利 43.9m，2026 年發放股利 44m，約等於 FY2025 全年淨利。TTM 自由現金流利潤率只有 3.25%，以約 877m 營收粗估不到 30m，低於股利所需，因存貨與應收增加；Q3 自由現金流約 20.0m。Q4 預計收到約 80m 的處分款可補足。事實表淨負債 351.51m（總債務 636.83m 含租賃，現金 285.32m），債務到期結構、利率與受限資金事實表未涵蓋，法說只談現金。近三年現金去向四分事實表也未涵蓋。","fact_refs":["f_kpi4_23_9m_3_9m","f_kpi6","f_net_debt_m","f_dividend_yield_ttm","f_peer_himx_fcf_margin_pct","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"過去 12 個月沒有併購，唯一重大交易是以約 80m 美元出售約 31% 權益法持股，屬處分。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"Q3 流通 ADS 174.5m，與上季幾乎相同；近年回購金額與均價事實表未涵蓋。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"2026 年員工獎金授予 13.3m，其中 11.8m 立即既得，約當市值 1,480.88m 的 0.9%，低於每年 1.5%；ADS 數量近季未增。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"過去 12 個月沒有併購，成長也不靠併購；現金回饋只有年度股利，近三年現金去向明細事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求 FY2031 每 ADS 盈餘約 0.9 美元、以 13 倍計價才有年化約一成的報酬，這接近基本情境，價格合理但沒有安全邊際。CPO 若完全落空，本業約 0.70 美元乘 13 倍約 9.1 美元，大致等於現價。","reasoning":"表面 Fwd P/E 18.06 倍的分母有爭議：FY2026 共識 0.47 美元未隨 Q4 指引調整，且公司 Q4 指引不含約 0.11 美元的處分利益。以 Q1 營益率粗估約 0.046 美元，加 Q2 0.114、Q3 0.107、Q4 指引中點 0.055，全年扣除處分利益約 0.32 美元，對應約 26 倍。用基本情境 FY2027 的 0.48 美元計算約 17.7 倍。賣方 FY2027 共識 1.30 美元對應 6.53 倍，但需要 1,230.6m 營收，不採信。TTM 本益比 40.43 倍隱含每 ADS 0.21 美元，低於 Q2、Q3 兩季合計 0.221 美元，顯示分母落後，也不採用。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy2_m","f_ev_m","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"循環修正中的當年度與次年度本益比，並以 FY2022 至 FY2025 平均每 ADS 盈餘約 0.59 美元對照。","tier":"小型無晶圓廠顯示 IC","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或 EV/S；終端倍數本應附同業現值對照，證據包未涵蓋，標為資料缺口。"},"fwd_pe":18.06,"peg":0.16,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"五年分位無法計算，資料只有 4 個年度端點；P/E、P/S、EV/S 都在這 4 點的最高位，但分母偏低，只作為不便宜的提醒。現價約為平均盈餘的 14.4 倍、FY2027 基本情境的 17.7 倍。PEG 0.16 來自偏低基期與未更新的共識，不能當便宜證據；以基本情境三年成長約 15% 計算約 1.2。12 個月機率加權約 8.8 美元（+4%），3 年約 10.5 美元（+23%）。結論為合理。","upside_short_pct":4,"upside_mid_pct":23,"denominator_disputed":true,"denominator_note":"FY2026 共識 0.47 美元未隨 Q4 指引調整，可能含也可能不含約 0.11 美元的一次性處分利益；同年度共識營收 949.39m 比指引推算約 861m 高約 10%。便宜論證不採用這個分母。"}}},"q6_how_wrong":{"verdict":"最可能看錯三處：車用修正持續超過一季、最大客戶轉單、CPO 量產延後或毛利被第二來源攤薄。反方向的錯誤是修正真的只有一季，而 CPO 比預期更快放量。","reasoning":"這次利空不到一週，賣方共識還沒動，Q1 2027 才有第一個驗證點。股價 26 週跌 51.44%、RSI 28.68，反映悲觀，但過去的 2022 年費半跌約 36%，本股已跌更深不等於見底。AI 不會取代這些實體晶片，它的影響是搶走成熟製程產能並推高成本。空方最強數字、歷史最大回撤與訴訟金額事實表未涵蓋；20-F 無重大訴訟。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w250","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"價值陷阱風險中等：衰退訊號亮 2 項，修正深度仍未知。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":0.47,"pe":18.06,"basis":"FY2026E 共識 EPS（2026-11-07 快照，未隨 Q4 指引調整），P/E 為現價除以當年度 EPS，與終端年倍數同為當年度口徑。"},"eps":{"bull":[0.8,1.2,1.5,1.75,1.9],"base":[0.48,0.6,0.72,0.83,0.92],"bear":[0.28,0.2,0.2,0.25,0.3]},"pe":{"bull":15,"base":13,"bear":12},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":2.97,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":4},"max_dd":{"lo":-65,"hi":-40,"basis":"以現價起算。參考本輪 26 週已跌 51%，2022 年費半自高點跌約 36%、盤中最深約 42% 至 44%，悲觀情境五年終點 3.6 美元相當現價約 −58%，再加上循環過度下跌的空間。下緣約 3.0 美元，上緣約 5.1 美元。","trigger_time":null},"basis":{"bull":"CPO 2027 下半年放量，FY2031 營收約 400m 且維持高毛利，本業約 1,400m、毛利率約 36%；每 ADS 1.90 美元，15 倍，同業倍數事實表未涵蓋。","base":"FY2027 營收約 970m（本業 +8% 至 +10%，CPO 約 30m），毛利率 33.5%；FY2031 營收約 1,300m、毛利率約 36%、CPO 約 150m；每 ADS 0.92 美元，13 倍，同業倍數事實表未涵蓋。","bear":"車用修正延長到 2027 年底，本土替代與面板自研持續，CPO 未量產或被攤薄；營收 850m 至 900m，毛利率約 30%；每 ADS 0.30 美元，12 倍。機率 35% 依據是共識成長超過內生上界、Q4 訂單急修正與客戶集中。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FY2022 至 FY2025 營收由 1,201m 降到 832m，營益率由 21.4% 降到 5.3%；2025 年 73.8% 營收來自中國總部客戶；20-F 指中國面板廠導入本土 IC 已構成重大挑戰。","assumption":"車用是避風港，份額與毛利守得住。","consequence":"若車用走上消費性驅動 IC 的路，FY2031 每 ADS 盈餘約 0.30 美元，股價約 3.6 美元，虧損近六成。","ruling":"部分採納，悲觀情境機率提高到 35%。這個故事與唯一致命點重疊，最大客戶轉單是第一張骨牌。","watch":"FY2026 20-F 的客戶 A 占比與車用份額，每季車用 DDIC 與 TDDI 季增率。","evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#2","customer_second_source#1","reg_tariff_export#2"]},{"view":"論點成功但股東經濟變差","evidence":"CPO 由 FOCI 出資約 100m 美元擴產，Himax 只供特定光學元件；管理層承認已有對手正面競爭，長期不會有人獨占；代工與封測 2027 年漲價。","assumption":"光學元件的高毛利可持續，本業成本可轉嫁。","consequence":"營收達標但毛利被攤薄，價值由模組廠或客戶取走；代工漲價也吃掉非驅動 IC 占比提升的好處。","ruling":"採納，這是基本情境只給 CPO 小幅貢獻的原因。","watch":"CPO 開始貢獻後全公司毛利率能否站上 35%，第二來源何時出現。","evidence_refs":["substitute_technology#2","cyclical_supply_discipline_capacity#0","cyclical_inventory_price_position#2"]},{"view":"價格已反映太多","evidence":"股價 26 週跌 51.44%，但 TTM 本益比 40.43 倍，P/S 1.69、EV/S 2.09 都在 4 個年度端點的最高位；現價約為 FY2027 基本情境的 17.7 倍。","assumption":"跌深就是便宜。","consequence":"若 FY2027 每 ADS 低於 0.40 美元，現價仍不便宜，還有下跌空間。","ruling":"部分採納，估值結論只給合理，不給便宜；股價下跌不算安全邊際。","watch":"Q4 財報後賣方 FY2027 共識下修的落點。","evidence_refs":["capital_markets_pricing#0","cyclical_prior_downcycle_behavior#1"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 13.15 → 本次 8.49（-35.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=13.15","side_b":"本次 price_at_dd=8.49","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 候選/追蹤池 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=候選/追蹤池","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 B→C、估值 🟠→🟡、均線 ✅→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 13.15 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 13.15 美元：Bull 價 27、Bear 價 6，五年期望值 +30.0%，基準年化 5.2%，不對稱比 1.9","side_b":"本次情境、股價仍用 13.15 美元：Bull 價 28.5、Bear 價 3.6，五年期望值 −6.1%，基準年化 −1.9%，不對稱比 0.92","ruling":"先換情境、股價不動：五年期望值少 36.1 個百分點，基準年化少 7.1 個百分點。不對稱比由 1.9 變為 0.92。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 13.15 美元：五年期望值 −6.1%，基準年化 −1.9%，不對稱比 0.92","side_b":"本次情境、股價 8.49 美元：五年期望值 +45.4%，基準年化 7.1%，不對稱比 2.34","ruling":"再換股價、情境不動：起點價下跌 35.4%，五年期望值多 51.5 個百分點，基準年化多 9.0 個百分點，不對稱比由 0.92 升到 2.34。合計五年期望值比前份多 15.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訊號評級與結論","cause":"新證據","prior_field":["signal"],"side_a":"前份訊號評級 B，結論觀望，列在候選名單。","side_b":"本次訊號評級降到 C，結論傾向維持觀望。","ruling":"Q4 營收指引季減 22% 至 26%，車用訂單急修正，短線基本面比前份差；等待條件改成事件，不是價位。","evidence_level":"一手：公司 2026-11-05 新聞稿與法說","settle_metric":"2027 Q1 營收指引","if_then":["若 Q1 指引季增或持平，且車用止跌或 CPO 開始量產出貨：重做研究，首筆不超過 2%","若 Q1 營收低於 175m 且車用續跌：不追，持有者減碼一半"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 13.15 美元，估值偏貴。","side_b":"本次股價 8.49 美元，下跌約 35.4%，估值合理。","ruling":"變動來自股價，不是盈餘上修；基本情境的盈餘路徑其實比賣方低很多。","evidence_level":"事實表股價","settle_metric":"FY2027 共識下修後的本益比","if_then":["若共識下修後 FY2027 本益比高於 20 倍：估值結論轉回偏貴，不追"],"evidence_refs":[]},{"axis":"陷阱風險、護城河方向、成長空間","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"前份陷阱風險中等，護城河方向穩定，五年後成長空間中等。","side_b":"本次三項結論不變，但證據更新：車用時序控制更強、CPO 擴產更具體，同時車用急修正、代工漲價。","ruling":"正反證據相抵，結論不動。","evidence_level":"一手法說與 20-F","settle_metric":"FY2026 20-F 客戶占比與車用份額","if_then":["若車用份額確認下滑：護城河方向改為縮減，不追，持有者清倉"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"研究框架與機率","cause":"方法變動","prior_field":["archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這兩項分類空白，樂觀與悲觀機率各 25%，最大回撤 −55%。","side_b":"本次按需求量循環解讀，判晚循環；樂觀 20%、悲觀 35%，最大回撤範圍 −40% 至 −65%。","ruling":"共識成長超過內生上界，悲觀機率不得低於 30%；車用急修正再支持上調。循環位置按五項訊號多數決，三項偏賣、一項偏買、一項因分母偏低不明；訊號仍有矛盾，所以不給建立部位的姿態。","evidence_level":"方法約束加一手資料","settle_metric":"Q1、Q2 2027 營收與存貨","if_then":["若 Q1、Q2 2027 營收回到 190m、225m 以上：循環位置改判早循環，分批反買"],"evidence_refs":[]},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未載明重啟條件（空值）。","side_b":"2027 年 2 月公布的 Q1 營收指引季增或持平為必要條件，另需車用驅動 IC 止跌或 CPO 量產出貨其一。","ruling":"重啟條件綁事件，因為約束來自論點未決，不是估值。","evidence_level":"判斷","settle_metric":"2027 Q1 營收指引","if_then":["若條件成立：重跑完整研究再建立部位"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未載明減碼與清倉門檻（空值）。","side_b":"毛利率連 2 季低於 30% 就減碼一半；2027 年營收年增低於 5% 且年底 CPO 未量產就清倉。","ruling":"新設門檻，對應本次車用修正、代工漲價與 CPO 三個主要風險。","evidence_level":"判斷","settle_metric":"季度毛利率、年度營收、CPO 量產公告","if_then":["若門檻成立：依表減碼或清倉，不等下一次研究"],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未載唯一致命點（空值）。","side_b":"最大客戶（含關係企業，2025 年占營收 24.0%）把主力驅動 IC 大幅轉給本土供應商或自研，全年採購砍半以上。","ruling":"按每 ADS 盈餘敏感度排序，這項大於 CPO 落空，所以列為唯一致命點。","evidence_level":"20-F 客戶揭露加推算","settle_metric":"FY2026 20-F 客戶 A 占比","if_then":["若發生：改用悲觀情境並清倉"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"三項論點的門檻","cause":"新證據","prior_field":["H1","H2","H3"],"side_a":"前份：FY2026 車用 IC 高於 460m、FY2027 毛利率至少 33%；2026 年光學與 CPO 占比至少 3%，2H26 AR 眼鏡量產或 CPO 進入主要客戶供應鏈；正常化毛利率 31% 至 33%。","side_b":"本次：FY2027 營收至少 947m；FY2027 毛利率至少 33% 且非驅動 IC 至少 27%；2027 年 CPO 占比至少 5%。","ruling":"全年車用約 +10%，僅勉強碰到前份門檻。LCoS 已被 2026-08-06 Jordan Wu 排除在明年量產題材之外，CPO 2026 年貢獻也有限，所以光學路徑改寫成只看 CPO。毛利率已高於前份區間，但 2027 年代工漲價，門檻維持 33%。","evidence_level":"一手法說","settle_metric":"FY2027 營收、毛利率、CPO 占比","if_then":["若三項中兩項未達：基本情境下修，停止加碼"],"evidence_refs":[]},{"axis":"管理層 2027 成長說法與 Q4 跌幅","cause":null,"prior_field":null,"side_a":"2026-11-05 Jordan Wu：Q4 是短期修正，2027 年營收雙位數成長，不含 CPO，前提是全球車輛出貨持平。","side_b":"同場承認訂單能見度受限，客戶急煞車也讓公司意外；要達到 +10%，FY2027 平均季營收要比 Q4 中點高約 26%。","ruling":"可調和，屬程度差異。一次性歸因不採信也不否定，標為未證。基本情境本業只取 +8% 至 +10%。若 Q1、Q2 2027 分別低於 190m、225m，短期修正的說法視為證偽。","evidence_level":"一手法說，未來說法尚未驗證","settle_metric":"Q1、Q2 2027 營收","if_then":["若兩季都達標：H1 維持，分批反買","若兩季都未達：H1 削弱，下修基本情境，停止加碼"],"evidence_refs":["capital_markets_pricing#0","supply_demand_durability#4"]},{"axis":"賣方共識與指引","cause":null,"prior_field":null,"side_a":"賣方 FY2027 每 ADS 1.30 美元、營收 1,230.6m；3 位分析師目標價平均 30.2 美元，低 17.4、高 43。","side_b":"指引推算 FY2026 營收約 861m；不含 CPO 的 2027 年 +10% 約 947m，要到賣方數字 CPO 需貢獻約 280m。","ruling":"採後者。比共識悲觀的原因是成長基準已過時：FY2026 營收共識高於指引約 10%，三年 EPS 近期修正都是 0。利空還沒進模型，所以凍結加碼到第一個確認資料點；目標價高低差 2.47 倍，家數又少，不作依據。","evidence_level":"一手指引對二手彙整","settle_metric":"2027 年 2 月後的共識修正","if_then":["若下修後 FY2027 EPS 仍高於 0.80 美元：上調基本情境，分批反買","若下修到 0.40 美元以下：不追"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-08-06 Jordan Wu：毛利率改善趨勢明年可能延續；Q3 平板 IC 下滑原因是產能限制；CPO 在最保守情境下 2027 年也有實質貢獻。","side_b":"2026-11-05 Karen Tiao 把平板下滑歸因於上半年提前拉貨；Jordan Wu 改說毛利率相對穩定或略為改善，CPO 從明年某個時點開始，量產時間由終端客戶決定。","ruling":"語氣下修，不是方向翻轉。兩次平板歸因可能同時成立，但說明管理層的歸因不穩定，H2 與 H3 只用實際數字驗證。","evidence_level":"逐字稿對照","settle_metric":"FY2027 毛利率與 CPO 量產公告","if_then":["若 2027 年上半年毛利率低於 33%：H2 削弱，停止加碼"],"evidence_refs":["cyclical_supply_discipline_capacity#1"]},{"axis":"CPO 領先與未量產","cause":null,"prior_field":null,"side_a":"管理層稱處於最先進驗證階段，FOCI 通過新台幣 33.3 億元擴產，晶圓級光學路線獨特。","side_b":"尚未正式量產，仍在改善良率，不給營收數字，對手已正面競爭，目前只與 FOCI 合作。","ruling":"可調和。基本情境只放 2027 年約 30m，到 FY2031 約 150m；大幅成功只放在樂觀情境。","evidence_level":"一手說法，二手競爭資訊","settle_metric":"2027 全年 CPO 占營收比重","if_then":["若 2027 年占比至少 5%：樂觀機率上調至 30%，分批反買","若 2027 年底未量產：樂觀機率降到 10%，不追"],"evidence_refs":["substitute_technology#2"]},{"axis":"份額是否流失","cause":null,"prior_field":null,"side_a":"2026-11-05 Jordan Wu：車用成長贏過全球汽車出貨，證明未失份額。","side_b":"20-F 稱本土替代已構成重大挑戰，客戶 A 占比連降，聯詠與新進者加壓車用。","ruling":"不可裁決至 FY2026 20-F 公布。管理層的比較沒有對照同業；客戶 A 下滑也可能來自消費性產品。暫不判份額流失，也不接受份額無虞。","evidence_level":"公司自述對風險揭露，缺份額序列","settle_metric":"FY2026 20-F 車用 DDIC 與 TDDI 份額","if_then":["若車用 DDIC 份額低於 35%：護城河方向改為縮減，不追，持有者清倉"],"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0","customer_second_source#1"]},{"axis":"存貨與應收","cause":null,"prior_field":null,"side_a":"管理層稱存貨健康，理由是產業交期拉長，也需要確保 2027 年產能。","side_b":"存貨 159.8m，季增 5.5%、年增 16.3%，Q4 營收卻要季減約兩成多；粗估存貨天數由約 90 天升到約 119 天。DSO 93 天，一年前 87 天。","ruling":"部分採信，車用客戶確實要求供應穩定，但急修正期存貨有跌價風險，應收又集中在客戶 A。以存貨季增率與營收季增率的差距當領先指標。","evidence_level":"一手數字加推算","settle_metric":"Q4 2026、Q1 2027 存貨與 DSO","if_then":["若兩季差距都大於 10 個百分點：停止加碼"],"evidence_refs":["customer_concentration_credit#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價半年跌 51%，現價大致只付本業；CPO 工程量產中且 FOCI 擴產；車用時序控制 +40%；股息約 3%；約 80m 處分款入帳；賣方最低目標價 17.4 美元。","side_b":"利空不到一週，訂單能見度低，賣方模型還沒改；現價約 FY2027 基本情境的 17.7 倍，週線跌破 52 週與 104 週均線。","ruling":"暫不買。等待成本有限，下一個驗證點在 2027 年 2 月；若論點正確，錯過的幅度可接受，論點錯誤則還有四成以上下跌。","evidence_level":"一手資料加判斷","settle_metric":"2027 Q1 營收指引","if_then":["若股價先漲、Q1 指引未出：不追","若股價跌破 250 週均線 7.58 美元，但 Q1 指引確認止跌：分批反買，首筆不超過 2%","若 Q1 營收低於 175m 且車用續跌：不追"],"evidence_refs":["major_events#0"]},{"axis":"淨負債口徑","cause":null,"prior_field":null,"side_a":"法說只揭露現金及其他金融資產 285.3m。","side_b":"事實表總債務 636.83m（含租賃），淨負債 351.51m，企業價值 1,832.39m。","ruling":"EV 採事實表，但受限資金與債務條件未涵蓋，所以 EV 倍數只作參考，本次估值以本益比為主。","evidence_level":"事實表，明細缺口","settle_metric":"FY2026 20-F 債務與受限資金附註","if_then":["若受限資金能抵銷大部分借款：EV 倍數下修，估值結論不變"],"evidence_refs":[]},{"axis":"每股盈餘資料不一致","cause":null,"prior_field":null,"side_a":"事實表 financial_history.years[3] 的 FY2025 稀釋 EPS 為 0.504 美元。","side_b":"同列淨利 43.937m 除以 174.43m ADS 約 0.252 美元，前三年 EPS 都與淨利除以 ADS 相符。","ruling":"採 0.252 美元，0.504 美元與淨利不符；TTM 本益比 40.43 倍隱含 0.21 美元，也低於最近兩季合計 0.221 美元，因此不作依據。","evidence_level":"事實表內部對照","settle_metric":"20-F 的每 ADS 盈餘","if_then":["若 20-F 確認 0.504 美元：共識成長率改為約 69%，結論不變"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：中國本土替代與面板廠自研加劇，聯詠與新進者加壓車用。","side_b":"結構：車用顯示含量上升，時序控制與 LTDI 領先；其他變數是成熟製程漲價、關稅與出口管制。","ruling":"雙向拉鋸：20-F 指本土替代已是重大挑戰，法說顯示車用時序控制 2026 年成長逾 40%，兩邊都有一手證據。","evidence_level":"一手","settle_metric":"FY2027 車用營收與毛利率","if_then":["若車用成長且毛利率至少 33%：改判結構性轉好中，分批反買","若車用年減且毛利率低於 30%：改判競爭惡化中，清倉"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","reg_tariff_export#0"]}],"triggers":[{"n":1,"text":"Q1 指引與車用或 CPO 同時轉好，才重新研究進場。","type":"估值rearm","maps_to":"H1","metric":"2027 Q1 營收指引季增率","threshold":"不低於 0%，另需車用驅動 IC 止跌或 CPO 量產出貨其一","action":"重跑完整研究，首筆不超過 2%","source_freq":"公司法說，每季","date":"2027-02","evidence_refs":["capital_markets_pricing#0"]},{"n":2,"text":"2027 全年營收驗證短期修正的說法。","type":"假設驗證","maps_to":"H1","metric":"FY2027 營收","threshold":"至少 947m 美元","action":"未達標則下修基本情境，樂觀機率減 5 點，停止加碼","source_freq":"季度新聞稿","date":"2028-02","evidence_refs":["supply_demand_durability#4"]},{"n":3,"text":"毛利率與產品組合驗證能否抵消漲價。","type":"假設驗證","maps_to":"H2","metric":"FY2027 毛利率與非驅動 IC 占比","threshold":"毛利率至少 33%，非驅動 IC 至少 27%","action":"未達標則停止加碼","source_freq":"季度新聞稿","date":"2028-02","evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"CPO 是否真的量產。","type":"假設驗證","maps_to":"H3","metric":"2027 全年 CPO 占營收比重","threshold":"至少 5%，約 50m 美元","action":"達標則樂觀機率上調至 30%；年底未量產則降到 10%","source_freq":"法說與 FOCI 公告","date":"2028-02","evidence_refs":["substitute_technology#2"]},{"n":5,"text":"存貨成長超前營收。","type":"風險","maps_to":"R1","metric":"存貨季增率減營收季增率","threshold":"連 2 季大於 10 個百分點","action":"停止加碼","source_freq":"季度新聞稿","date":"2027-05","evidence_refs":["customer_concentration_credit#1"]},{"n":6,"text":"最大客戶大幅轉單。","type":"Single Thing","maps_to":"R3","metric":"客戶 A 占營收比重與車用 DDIC 年增率","threshold":"FY2026 20-F 客戶 A 不高於 20%，且車用 DDIC 年減","action":"清倉","source_freq":"20-F，每年","date":"2027-03","evidence_refs":["customer_concentration_credit#0","customer_second_source#1","substitute_technology#0"]},{"n":7,"text":"代工漲價轉嫁失敗。","type":"減碼","maps_to":"R2","metric":"GAAP 毛利率","threshold":"連 2 季低於 30%；2023 年 Q2 的 21.7% 含終止代工合約的一次性影響，以全年 27.9% 作底線","action":"減碼一半","source_freq":"季度新聞稿","date":"2027-08","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_inventory_price_position#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#3"]},{"n":8,"text":"本業與 CPO 同時失敗。","type":"清倉","maps_to":"H1","metric":"FY2027 營收年增率與 CPO 量產狀態","threshold":"年增低於 5% 且年底 CPO 未量產","action":"清倉","source_freq":"季度新聞稿與法說","date":"2028-02","evidence_refs":["substitute_technology#2"]},{"n":9,"text":"關稅或出口管制衝擊未能吸收。","type":"風險","maps_to":"R5","metric":"毛利率季變動與管制名單","threshold":"主要客戶或供應商列入實體清單，或毛利率季減至少 2 個百分點且公司歸因於關稅","action":"減碼一半","source_freq":"BIS 公告、法說","date":"2027-05","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"n":10,"text":"連續兩季過關才加到上限。","type":"加碼","maps_to":"H1","metric":"Q2 2027 營收與毛利率","threshold":"營收至少 225m，毛利率至少 33%","action":"分批加到 3% 上限","source_freq":"季度新聞稿","date":"2027-08","evidence_refs":[]},{"n":11,"text":"Q4 財報與 Q1 指引公布後全文複審。","type":"複審日期","maps_to":"H1","metric":"複審","threshold":"2027 年 2 月財報日","action":"依重啟條件決定是否進場","source_freq":"一次性","date":"2027-02","evidence_refs":[]},{"n":12,"text":"半導體族群系統性下跌與供應集中事件。","type":"風險","maps_to":"R6","metric":"費半回檔幅度、主要代工或封測斷供","threshold":"費半自高點回落至少 30%，或斷供達 1 季","action":"停止加碼","source_freq":"市場資料與公司公告","date":"2027-05","evidence_refs":["cyclical_prior_downcycle_behavior#1","geo_supply_chain#0","geo_supply_chain#1"]}],"kill_metrics":[{"metric":"季營收","bear_threshold":"Q1 2027 低於 175m 美元，或 Q2 2027 低於 205m 美元","window":"2027-08 前","source":"公司季度新聞稿","last_status":"warning"},{"metric":"GAAP 毛利率","bear_threshold":"連 2 季低於 30%","window":"未來 4 季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"FY2027 車用 IC 營收年增率","bear_threshold":"低於 +5%","window":"2028-02 前","source":"公司法說","last_status":"unknown"},{"metric":"CPO 占營收比重","bear_threshold":"2027 全年低於 3%，或年底仍未量產","window":"2028-02 前","source":"公司法說與 FOCI 公告","last_status":"unknown"},{"metric":"客戶 A 占營收比重","bear_threshold":"FY2026 不高於 20%，且車用 DDIC 年減","window":"2027-03 的 20-F","source":"20-F Item 4","last_status":"warning"},{"metric":"存貨季增率減營收季增率","bear_threshold":"連 2 季大於 10 個百分點","window":"Q4 2026 與 Q1 2027","source":"公司季度新聞稿","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027 年 2 月公布的 Q1 營收指引季增或持平為必要條件，另需車用驅動 IC 止跌或 CPO 量產出貨其一。","exec_line":"條件成立後先重跑完整研究，首筆不超過 2%；Q2 2027 營收至少 225m 且毛利率至少 33% 才加到 3%。股價先漲而資料未到時不追。","holding_cap":"3%"}},"decision_inputs":{"signal":"C","ma":"🟠","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不等價位，等 2027 年 2 月財報：Q1 營收指引季增或持平，另加車用驅動 IC 止跌或 CPO 量產出貨其一。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"車用驅動 IC 這次修正是客戶庫存調整，不是需求斷層或份額流失，2027 年營收恢復雙位數成長。","2y":"FY2027 營收至少 947m 美元，Q1 2027 至少 190m，Q2 2027 至少 225m。","5y":null,"10y":null,"threshold":"FY2027 營收與車用 IC 年增都至少 10%","source":"公司季度新聞稿與法說，20-F 客戶揭露","drift_rule":"TTM 營收連 2 季低於路徑至少 5% 視為削弱，連 3 季低於至少 10% 視為反轉"},{"id":"H2","text":"非驅動 IC 占比升到接近 30%，足以抵消 2027 年代工與封測漲價，毛利率守在 33% 以上。","2y":"FY2027 毛利率至少 33%，非驅動 IC 占比至少 27%。","5y":"FY2031 毛利率中樞約 36%，營益率至少 13%。","10y":null,"threshold":"FY2027 毛利率至少 33%，非驅動 IC 占比至少 27%","source":"公司季度新聞稿與法說","drift_rule":"TTM 毛利率連 2 季低於路徑至少 5% 視為削弱，連 3 季低於至少 10% 視為反轉"},{"id":"H3","text":"CPO 的 FAU 光學元件 2027 年進入量產，2028 年成為有份量的第二條成長線。","2y":"2027 全年 CPO 占營收至少 5%，約 50m 美元。","5y":"FY2031 CPO 占營收約 10% 以上，毛利率高於公司平均，第二來源出現後仍守住主要份額。","10y":null,"threshold":"2027 全年至少 5%，2028 全年至少 10%","source":"公司法說、FOCI 公告","drift_rule":"連 4 季低於路徑至少 5% 視為削弱，連 6 季低於至少 10% 或 2027 年底仍未量產視為反轉"}],"R":[{"id":"R1","text":"車用庫存修正超過一季，Q1 2027 續弱；這次中國出口與面板廠拉貨反轉，能見度低。","h_ref":"H1","clock":"⚡","threshold":"Q1 2027 營收低於 175m，或 Q2 2027 低於 205m","evidence_refs":["capital_markets_pricing#0","supply_demand_durability#4"]},{"id":"R2","text":"代工與封測漲價吃掉毛利，台積電縮減成熟製程產能使供給更緊。2023 年全年毛利率 27.9% 是參考底線。","h_ref":"H2","clock":"🔥","threshold":"連 2 季毛利率低於 30%","evidence_refs":["supply_demand_durability#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_inventory_price_position#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#3"]},{"id":"R3","text":"中國本土替代與面板自研，加上客戶與應收集中，主力驅動 IC 的客戶基礎被侵蝕。","h_ref":"H1","clock":"🐢","threshold":"客戶 A 占比不高於 20%，或 FY2027 車用 DDIC 年減","evidence_refs":["competitive_share_entrants#0","customer_second_source#1","substitute_technology#0","substitute_technology#1","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R4","text":"CPO 量產延後，或第二來源攤薄毛利。量產時間由終端客戶決定。","h_ref":"H3","clock":"🔥","threshold":"2027 年底未量產，或 2028 年占比低於 5%","evidence_refs":["substitute_technology#2"]},{"id":"R5","text":"關稅與出口管制衝擊中國客戶與供應鏈，FY2025 大尺寸與中小尺寸驅動 IC 已受關稅不確定性影響。","h_ref":"H1","clock":"🔥","threshold":"主要客戶或供應商列入實體清單，或毛利率季減至少 2 個百分點且公司歸因於關稅","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R6","text":"晶圓代工集中台灣，部分產品單一晶圓廠，更換要數季驗證。來源為 FY2019 與 FY2017 的 20-F，年代較舊，公司 2025 年稱已擴展到中國、韓國與新加坡。","h_ref":"H1","clock":"🐢","threshold":"任一主要代工或封測廠斷供達 1 季","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R7","text":"半導體族群系統性下跌，股價在基本面確認前再受壓。2022 年費半自高點跌約 36%。","h_ref":"H1","clock":"⚡","threshold":"費半自高點回落至少 30%","evidence_refs":["cyclical_prior_downcycle_behavior#1"]}],"single_thing":{"description":"最大客戶（含關係企業，2025 年占營收 24.0%）把主力驅動 IC 大幅轉給本土供應商或自研，全年採購砍半以上。","why_fatal":"這是單一最大敏感度。客戶 A 約 207m 營收（861m 乘 24.0%），砍半少約 104m，以 33.5% 毛利率與 0.82 稅後比推算，每 ADS 少約 0.16 美元，約為基本情境 FY2027 的三分之一；CPO 完全落空在 FY2027 約少 0.07 美元（假設 50% 毛利率）。2025 年底對其應收 57.8m，占 28.8%，也會同時打擊現金。","if_happens":"改用悲觀情境並清倉，不因股價已低而加碼。","how_monitor":"每年 3 月 20-F 的客戶占比與應收集中度，每季法說的車用 DDIC 與 TDDI 季增率，面板廠是否公開導入本土 IC。","probability":"12 至 24 個月約 15%"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":6.53,"peg_fy2":0.06,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":0.252,"FY2026E":0.47,"FY2027E":1.3,"FY2028E":2.45},"fy_end_month":12,"eps_basis":"每 ADS，IFRS 稀釋。FY2025A 由事實表 financial_history.years[3] 淨利 43.937m 除以 174.43m ADS 得 0.252 美元；同列 diluted_eps 0.504 與淨利不符，未採用。FY2026E 至 FY2028E 取 Koyfin 2026-11-07 快照，未隨 Q4 指引調整，分析師家數未載明。"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"other","event":"出售權益法持股交割，現金約 80m，稅後利益約 19m 至 20m。","impact":"中","watch":"是否如期取得主管機關核准，以及 2027 年股利政策。"},{"date":"2027-01","date_precision":"month","type":"capacity","event":"代工與封測 2027 年漲價生效。","impact":"中","watch":"Q1 毛利率指引與客戶分攤比例。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 Q1 2027 指引。","impact":"高","watch":"Q1 營收指引、車用驅動 IC 訂單、存貨。"},{"date":"2027-03","date_precision":"month","type":"other","event":"FY2026 20-F 公布客戶占比與車用份額。","impact":"中","watch":"客戶 A 占比、應收集中度、車用 DDIC 與 TDDI 份額。"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"CPO FAU 預期進入量產，時間由終端客戶決定。","impact":"高","watch":"量產公告、FOCI 擴產進度、第二來源消息。"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"車用 OLED 預期自下半年放量，智慧眼鏡專案量產。","impact":"中","watch":"非驅動 IC 占比是否接近 30%。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟡', moat_trend='→', week26=-51.44, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
