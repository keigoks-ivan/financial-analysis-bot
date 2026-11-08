你是 DD 管線 v20 的判斷層閘（gate），標的 ARM（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（38 條）
- `f_kpi0_total_revenue_gaap`（q1_business）｜Total revenue (GAAP)＝1443 US$M｜期間與口徑：Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Arm 新聞稿 newsroom.arm.com/news/arm-q2-fye27-results；Exhibit 99.2 股東信（numbers.latest_quarter_kpis.items[0]，as_of Q2 FYE27（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝638 US$M（利益率 44.2%）｜期間與口徑：Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Arm 新聞稿；Exhibit 99.2 股東信（numbers.latest_quarter_kpis.items[1]，as_of Q2 FYE27（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝201 US$M（利益率 13.9%）｜期間與口徑：Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Arm 新聞稿；Exhibit 99.2 股東信（numbers.latest_quarter_kpis.items[2]，as_of Q2 FYE27（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi5_guidance_q3_fye27`（q1_business）｜Guidance Q3 FYE27＝營收 1.54bn ± 50M；non-GAAP 營業費用約 825M；non-GAAP EPS 0.56 ± 0.04 US$｜期間與口徑：Q2 FYE27 公告日 2026-11-04／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Exhibit 99.2 股東信（numbers.latest_quarter_kpis.items[5]，as_of Q2 FYE27 公告日 2026-11-04）
- `f_peer_arm_gross_margin_pct`（q2_moat）｜ARM 毛利率＝97.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ARM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-04 date｜期間與口徑：2026-11-04／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-04）
- `f_peer_arm_operating_margin_pct`（q2_moat）｜ARM 營業利益率＝17.02 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ARM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_arm_fcf_margin_pct`（q2_moat）｜ARM FCF 利潤率＝21.5 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ARM.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_qcom_operating_margin_pct`（q2_moat）｜QCOM 營業利益率＝20.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cdns_gross_margin_pct`（q2_moat）｜CDNS 毛利率＝85.68 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CDNS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_avgo_gross_margin_pct`（q2_moat）｜AVGO 毛利率＝68.77 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_snps_gross_margin_pct`（q2_moat）｜SNPS 毛利率＝72.38 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNPS.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.23 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.06 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝4.05 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6092.14 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（39 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝8381.79 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（40 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc_non_gaap`（q4_capital）｜SBC（含雇主稅）占 non-GAAP 營業利益＝66.6 %｜期間與口徑：Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Exhibit 99.2 股東信：SBC 377＋雇主稅 48＝425（US$M）；425÷638 本表自算；占營收 29.5%（numbers.latest_quarter_kpis.items[4]，as_of Q2 FYE27（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi3_non_gaap_free_cash_flow`（q1_business）｜Non-GAAP free cash flow＝110 US$M｜期間與口徑：Q2 FYE27（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Exhibit 99.2 股東信（numbers.latest_quarter_kpis.items[3]，as_of Q2 FYE27（季末 2026-09-30，公告於 2026-11-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-3121.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 500.0、現金 3621.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1070.0 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝174.62 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝78.3 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 2.23，分子＝快照價 174.62｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝200.71 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝26.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝26.7 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝34.2 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝64.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝64.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝33.62 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝63.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝63.7 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝30.16 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝183722.4 USD m｜期間與口徑：2026-11-08／市值 186843.4 ＋ 淨負債 -3121.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（2.23 → 2.23）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 2.23 → 2.23（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝-｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 174.62 / W52 209.64 / W104 174.4 / W250 None / W250 13週斜率 None%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝209.64 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝174.4 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-18.12 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝31.08｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（28 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F 風險因子：x86 與免費開源 RISC-V 為競爭者，許多客戶同時是 RISC-V 支持者，客戶可能改用 RISC-V。
  - 來源：SEC EDGAR 20-F FY2026 Item 3.D（as_of 2026-05-26）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F 風險因子：多家客戶自建 AI 加速器，若工作負載由 CPU 移向加速器，CPU 市場規模與授權費／權利金可能下降。
  - 來源：SEC EDGAR 20-F FY2026 Item 3.D（as_of 2026-05-26）｜affects：thesis.R、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F：Arm 自推 Arm AGI CPU 等量產矽產品，部分授權客戶將面臨與 Arm 直接競爭。
  - 來源：SEC EDGAR 20-F FY2026 Item 4（as_of 2026-05-26）｜affects：moat_trend、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：20-F 風險因素：客戶可能授權 ISA 自行開發處理器而非採用 Arm 預開發產品；最大客戶 Arm China 占 FY2026 營收約 16%（FY2025 17%、FY2024 21%），前五大客戶占約 57%。
  - 來源：SEC EDGAR 20-F FY2026 Item 3（as_of 2026-05-26）｜affects：decision_inputs.bear、moat_trend
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：20-F：Arm 進入自有量產晶片（Arm AGI CPU）可能使傳統授權客戶視為利益衝突，客戶可能改用替代架構或自研架構。
  - 來源：SEC EDGAR 20-F FY2026 Item 3（as_of 2026-05-26）｜affects：decision_inputs.bear、thesis.R
- `customer_second_source#2`（customer_second_source｜方向 -｜狀態 ok）：20-F：中國自給政策可能使陸系客戶自研 IP 或改用競爭對手技術。
  - 來源：SEC EDGAR 20-F FY2026 Item 3（as_of 2026-05-26）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026（截至2026-03-31）前五大客戶（含 Arm China、SoftBank）合計約占營收57%（FY25 56%、FY24 54%）；最大客戶 Arm China 約16%（FY25 17%、FY24 21%）；部分近期營收依賴與 SoftBank 的商業安排。
  - 來源：SEC EDGAR 20-F FY2026 Item 3 風險因子（as_of 2026-05-26）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：Qualcomm 為主要客戶，占 FY2026 營收9%，且與 Arm 有訴訟。
  - 來源：SEC EDGAR 20-F FY2026 Item 3 風險因子（as_of 2026-05-26）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：S&P 2026-03 將 SoftBank 展望由穩定降為負面、維持 BB+，因加碼 OpenAI；Arm 持股為其評等支撐。
  - 來源：pulse.bot Finance News: SoftBank's $30 Billion OpenAI Bet Spurs S&P Credit Outlook Cut（as_of 2026-03-27）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#4`（customer_concentration_credit｜方向 -｜狀態 ok）：Barron's：SoftBank 持有 Arm 約90%，為設計授權業務基石客戶，9月當季占設計授權業務35%。
  - 來源：Barron's: Arm Stock Is Falling. Its Biggest Customer Might Be Masking Larger Problems（as_of 2026-01-15）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：風險面：中國記憶體產能擴張引發過剩疑慮；Deloitte 警告 2027-2028 可能與目前預期大幅偏離；Digitimes 稱若 AI 資本支出放緩可能出現庫存修正（二手摘要）
  - 來源：Deloitte 2026 global semiconductor industry outlook (DQ India)（as_of 2026-01-15）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：20-F 風險因子載明：Arm 受多司法管轄區反壟斷法規約束，過去曾遭反壟斷主管機關調查；Qualcomm 訴訟進行中，Qualcomm 占 FY2026 營收 9%。
  - 來源：SEC EDGAR 20-F FY2026 Item 3.D（as_of 2026-05-26）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Bloomberg 報導 FTC 調查 Arm 授權行為是否試圖壟斷部分晶片市場，並要求 Arm 保存文件；Arm 否認反競爭指控，尚無正式指控。
  - 來源：Bloomberg Law: Arm Is Said to Face US Antitrust Probe Over Chip Technology（as_of 2026-05-15）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Arm 20-F：Neoverse V 系列效能達美英出口管制門檻，對中國出貨需出口許可，且難取得；公司改授權未超門檻的其他 CPU 核心以滿足客戶需求。
  - 來源：SEC EDGAR 20-F FY2026 Item 3 Risk Factors（as_of 2026-05-26）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：20-F：2025 年美國發布先進運算晶片、HBM、GAAFET 等出口管制規則並增列實體清單；公司稱不太可能取得部分高效能 Neoverse 核心的美英出口許可，可能降低營收並使產品路線圖不確定。
  - 來源：SEC EDGAR 20-F FY2026 Item 3 Risk Factors（as_of 2026-05-26）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Arm FY2026 20-F 稱進入量產晶片使其依賴第三方晶圓代工與委外製造商，供應鏈中斷可能對業務造成重大不利影響，另提及記憶體與封裝供應商依賴。
  - 來源：Arm Holdings Form 20-F FY2026 (SEC)（as_of 2026-05-20）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Arm 3nm 資料中心 CPU 由台積電代工，並稱僅取得首批約 10 億美元需求的產能；多家券商點出台積電先進製程晶圓供給為近期瓶頸（二手報導）。
  - 來源：City AM, Arm's AI ambitions hit supply chain reality despite record revenues（as_of 2026-05-21）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：中國約占 Arm 營收 18%（FY2026 摘要），經由 Arm China（Arm 不控制營運）；IPO 文件稱 Arm China 為最大客戶；出口管制限制中國成長。
  - 來源：SCMP / Panabee Arm Q1 2026 summary（as_of 2023-09-05）｜affects：thesis.R、decision_inputs.bear
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：FQ2 FY27 權利金 +8%、資料中心權利金翻倍、edge AI 持平
  - 來源：xenospectrum（as_of 2026-11-05）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Arm 20-F 列明競爭來自 x86 與免費開源的 RISC-V，且部分客戶同時是 RISC-V 的主要支持者。
  - 來源：SEC EDGAR 20-F FY2026 Item 4（as_of 2026-05-26）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Arm 20-F 風險因素：客戶無義務獨家使用 Arm 產品，部分客戶已用含自家設計在內的競爭技術，且多數安排無最低採購義務。
  - 來源：SEC EDGAR 20-F FY2026 Item 3.D（as_of 2026-05-26）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：SHD Group 估 RISC-V 晶片 2024 年市場 520 億美元、滲透率 10.4%，2030 年可能超過 2600 億美元。
  - 來源：Simply Wall St 轉述 SHD Group（as_of 2026-01-01）｜affects：moat_trend、thesis.R
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：Arm 自有晶片與授權客戶（AWS、Google、Microsoft、NVIDIA 等）存在通路衝突疑慮；Meta 為首發客戶。
  - 來源：eWeek: Arm Enters the AI Chip Market With New AGI Processor（as_of 2026-03-25）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#5`（capital_markets_pricing｜方向 -｜狀態 ok）：TIKR：Street 平均目標價 $245 低於當時股價，ARM 2026 年內大漲約 240%。
  - 來源：TIKR（as_of 2026-06-05）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：Arm 與 Qualcomm/Nuvia 訴訟仍在進行，預計 2026 年第四季開庭；Qualcomm 於 2026-03-30 提出修正訴狀新增一項違約主張。
  - 來源：SEC EDGAR 20-F FY2026 Item 3（as_of 2026-05-26）｜affects：thesis.R、decision_inputs.bear、triggers
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2026-05-15 Bloomberg 報導 FTC 調查 Arm 是否試圖非法壟斷部分半導體市場，股價當日跌 8.5% 至 209.16 美元；多家原告律所隨後宣布證券詐欺調查（非已提起之集體訴訟）。
  - 來源：Business Wire：Law Offices of Frank R. Cruz 公告（as_of 2026-05-18）｜affects：thesis.R、decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Qualcomm/Nuvia 訴訟進行中，預計 2026 Q4 開庭。
  - 來源：SEC EDGAR 20-F FY2026 Item 3（as_of 2026-05-26）｜affects：thesis.R、decision_inputs.bear、triggers
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-05 起多家原告律所宣布證券詐欺調查（因 FTC 調查報導後股價跌 8.5%），搜尋結果未見已提起之集體訴訟。
  - 來源：Business Wire：Law Offices of Frank R. Cruz 公告（as_of 2026-05-18）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":367.2,"bear_5y_price":60.0,"p_bull_pct":17,"p_bear_pct":35,"upside_5y_pct":-2.2,"ev5y_pct":-5.3,"irr_base_pct":-0.4,"asym_ratio":0.8,"scenario_tree":{"terminal_label":"FY2032E","start":{"eps":2.23,"pe":78.3,"basis":"FY2027E（FY1）非 GAAP 共識 EPS，與終端倍數同為當前財年口徑，Y1～Y5 為 FY2028E～FY2032E"},"eps":{"bull":[3.3,4.7,6.4,8.5,10.8],"base":[2.85,3.55,4.35,5.2,6.1],"bear":[2.5,2.7,2.85,2.95,3.0]},"pe":{"bull":34,"base":28,"bear":20},"p":{"bull":17,"base":48,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ARM_Q1_2027_Earnings_Call_20260729.md
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 FY27 營收財測（原話："expect revenue of $1.38 billion, plus or minus $50 million"）
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 授權年增約 30%、權利金年增低十幾%（原話："royalty revenue to be up in the low teens year-on-year."）
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 non-GAAP 營業費用約 7.8 億美元（原話："non-GAAP operating expense to be approximately $780 million"）
- 2026-07-29｜Jason Child (CFO)｜guidance：其餘季度營業費用預期逐季成長幅度（原話："mid-single-digit percentage quarter-on-quarter"）
- 2026-07-29｜Jason Child (CFO)｜guidance：全年權利金成長預期由約 20% 下修為接近高十幾%（原話："that's probably somewhere closer to the high teens right now"）
- 2026-07-29｜Jason Child (CFO)｜guidance：先前說法：未來數年（含本年）權利金年增約 20%（原話："around 20% year-on-year for the next few years in royalties"）
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 權利金口徑：此處說低到中十幾%，與 prepared remarks 的 low teens、後段 13% 並陳（原話："we guided to kind of the low to mid-teens for Q2"）
- 2026-07-29｜Jason Child (CFO)｜guidance：Q2 權利金 13%，同時調高授權成長（原話："We're now guiding to 13% royalty growth in Q2."）
- 2026-07-29｜Jason Child (CFO)｜guidance：FY28、FY29 權利金 20%+ 成長維持（原話："I think that's very much still intact."）
- 2026-07-29｜Jason Child (CFO)｜guidance：AGI CPU 超過 10 億美元的更新時點在 Q3 財報（原話："provide an update at our Q3 results"）
- 2026-07-29｜Jason Child (CFO)｜guidance：SoftBank 授權／設計服務季度運行率約 2 億美元（原話："quarterly run rate for the rest of the year to be around"）
- 2026-07-29｜Jason Child (CFO)｜margin：Q1 非 GAAP 營業利益（原話："Non-GAAP operating income was $531 million"）
- 2026-07-29｜Jason Child (CFO)｜margin：Q1 非 GAAP 營業利益率及年增（原話："41%, up 200 basis points year-on-year."）
- 2026-07-29｜Jason Child (CFO)｜margin：Q1 營業費用低於財測約 2,700 萬，歸因時點（原話："This was about $27 million below our guidance due"）
- 2026-07-29｜Jason Child (CFO)｜margin：營業費用差異來自工具（模擬、雲端支出）而非人力（原話："it was really more on kind of the tools that were utilized"）
- 2026-07-29｜Jason Child (CFO)｜margin：Q1 自由現金流（原話："generated free cash flow of $665 million for the quarter"）
- 2026-07-29｜Jason Child (CFO)｜margin：AGI CPU 首代毛利率區間（高 30% 到低 40%）（原話："somewhere in the high 30% range, maybe low 40s percent"）
- 2026-07-29｜Jason Child (CFO)｜margin：AGI CPU 毛利率數年內目標 50%（原話："we do expect to get to 50%, but"）
- 2026-07-29｜Jason Child (CFO)｜margin：授權 ACV 作為底層授權趨勢指標（口徑）（原話："ACV grew 13% year-on-year, maintaining strong momentum."）
- 2026-07-29｜Jason Child (CFO)｜commitment：AGI CPU 營收滿 10% 後獨立列示為第三條線（原話："at least 10% of revenue, we'll break it out"）
- 2026-07-29｜Rene Haas (CEO)｜commitment：AGI CPU 需求超過 20 億美元（原話："Demand now exceeds $2 billion as we continue to add"）
- 2026-07-29｜Jason Child (CFO)｜commitment：對 AGI CPU 超過 10 億美元的信心上升（原話："confidence in achieving more than $1 billion has increased"）
- 2026-07-29｜Jason Child (CFO)｜commitment：內部目標高於對外數字（原話："internally, we do have higher targets"）
- 2026-07-29｜Rene Haas (CEO)｜commitment：TAM 不調整、但認為先前可能保守（原話："we're not changing the numbers at all"）
- 2026-07-29｜Rene Haas (CEO)｜product：AGI CPU 初期產品已交付多家客戶（原話："Initial product has now been delivered to"）
- 2026-07-29｜Rene Haas (CEO)｜product：AGI CPU 目前為 128 核；方向為更多核，路線圖無可說（原話："the direction of travel is more cores"）
- 2026-07-29｜Rene Haas (CEO)｜product：AGI CPU 可連接客製加速器（含 NVLink Fusion）（原話："paths for Arm to connect to custom accelerators"）
- 2026-07-29｜Rene Haas (CEO)｜product：AGI CPU 適用三類應用（傳統伺服器、head node、agentic）（原話："we had folks like Cerebras and OpenAI, which were"）
- 2026-07-29｜Rene Haas (CEO)｜product：Neoverse 出貨累計核數（原話："Neoverse shipments have now surpassed 1.5 billion cores"）
- 2026-07-29｜Rene Haas (CEO)｜customer：資料中心權利金年增超過一倍（原話："Data center royalties more than doubled year-over-year"）
- 2026-07-29｜Rene Haas (CEO)｜customer：NVIDIA Vera 量產（原話："brought Vera into production."）
- 2026-07-29｜Rene Haas (CEO)｜customer：IDC：Arm 加速伺服器平台支出近兩季近倍增（原話："has nearly doubled in the past 2 quarters"）
- 2026-07-29｜Rene Haas (CEO)｜customer：V9／CSS 使 Arm 相對隔離於手機市場衰退（原話："we have moved the vast majority of the customers to V9"）
- 2026-07-29｜Jason Child (CFO)｜customer：記憶體漲價下手機銷量下滑，被較高權利金率抵銷（原話："more than offset the decline in smartphone sales"）
- 2026-07-29｜Jason Child (CFO)｜risk：手機疲弱擴及中高階市場（原話："even some upper and mid-tier being affected"）
- 2026-07-29｜Jason Child (CFO)｜risk：供應鏈未來兩年相當緊（原話："supply chain is pretty tight"）
- 2026-07-29｜Jason Child (CFO)｜risk：供應鏈於日曆 2028–29 放寬（原話："supply chain is going to loosen or at least expand"）
- 2026-07-29｜Rene Haas (CEO)｜risk：回應單一元件缺口風險：無單點失敗（原話："there isn't one single point of failure"）
- 2026-07-29｜Rene Haas (CEO)｜competition：Qualcomm 宣布進入 AI 資料中心 CPU 市場（原話："Qualcomm has also announced plans to enter the AI data"）
- 2026-07-29｜Jason Child (CFO)｜competition：CPU TAM 最新估計 2,200 億美元（先前 1,000 億+）（原話："recent estimate is $220 billion sitting on"）
- 2026-07-29｜Rene Haas (CEO)｜competition：開源模型對 Arm 中性到正面（原話："between a net neutral to a net positive"）
- 2026-07-29｜Rene Haas (CEO)｜capital_allocation：管理層對供給端比 90 天前更樂觀（原話："we are more optimistic than we were 90 days ago"）

### ARM_Shareholder_Analyst_Call_Arm_Holdings_plc_20260324.md
- 2026-03-24｜Rene Haas｜product：CEO 表示 Arm 開始以晶片形式直接供貨，進入新業務（原話："Arm, and we are supplying CPUs as chips."）
- 2026-03-24｜Rene Haas｜customer：CEO 稱做自家晶片的首要原因是夥伴提出需求（原話："reason 0 is our partners have asked us for it."）
- 2026-03-24｜Rene Haas｜product：CEO 給出 CSS 占權利金比重的口徑（原話："represents almost 20% of our royalties and growing."）
- 2026-03-24｜Rene Haas｜product：CEO 估算 agentic AI 下每 GW 所需 CPU 核心數增為 4 倍（原話："120 million CPU cores for that same gigawatt"）
- 2026-03-24｜Rene Haas｜risk：CEO 承認 AI 投資可能放緩、估值可能變動，但主張 AI 不會消失（原話："it may be a financial bubble in the case of investment"）
- 2026-03-24｜Mohamed Awad｜product：產品主管說明 AGI CPU 已可供貨（原話："Arm AGI CPU is available now, and we're so proud of that."）
- 2026-03-24｜Mohamed Awad｜customer：客戶正在評估 AGI CPU（原話："Customers are actually evaluating it as we speak."）
- 2026-03-24｜Mohamed Awad｜commitment：管理層給出 AGI CPU 量產時點（原話："by the end of the year, and we are excited to share"）
- 2026-03-24｜Mohamed Awad｜product：AGI CPU 規格：Neoverse V3 核心數（原話："We pack in 136 of those cores"）
- 2026-03-24｜Mohamed Awad｜product：管理層給出已出貨至資料中心的 Neoverse 核心累計數（原話："over 1.25 billion Arm Neoverse cores"）
- 2026-03-24｜Mohamed Awad｜competition：管理層指稱 x86 業者需過度配置資料中心（原話："data center operators have to overprovision"）
- 2026-03-24｜Rene Haas｜competition：CEO 與 x86 同等結構比較的效能主張（原話："36 kilowatts, 2x the performance in the same power."）
- 2026-03-24｜Rene Haas｜competition：CEO 量化每 GW 額外電力對應的資本支出（原話："it's up to $10 billion of"）
- 2026-03-24｜Rene Haas｜commitment：CEO 承諾 AGI CPU 後續世代產品線（原話："So we are committing to future generations of this product."）
- 2026-03-24｜Santosh Janardhan｜commitment：Meta 方面稱為多世代合作（原話："multigenerational partnership. I just want to emphasize"）
- 2026-03-24｜Santosh Janardhan｜product：Meta 說明首顆合作 CPU 的設計取向（原話："something to minimize risk for this iteration."）
- 2026-03-24｜Rene Haas｜customer：CEO 列出已承諾購買 AGI CPU 的客戶（原話："we have committed customers, Meta, OpenAI, Cloudflare, SAP"）
- 2026-03-24｜Rene Haas｜guidance：CEO 給出 AI 資料中心權利金 TAM 現況口徑（原話："that represents today about a $3 billion TAM."）
- 2026-03-24｜Rene Haas｜guidance：CEO 稱雲端 AI 業務數年內將成最大業務（原話："probably be our largest business in a few years."）
- 2026-03-24｜Rene Haas｜guidance：CEO 給出晶片業務未來 TAM 估計（原話："we think this represents about $100 billion TAM for us"）
- 2026-03-24｜Rene Haas｜guidance：CEO 給出 2030 年前整體可觸及 TAM（原話："greater than a $1 trillion TAM by the end of the decade."）
- 2026-03-24｜Rene Haas｜commitment：CEO 稱 IP／CSS 業務表現優於 IPO 路演時對投資人所說（原話："we're actually ahead of that."）
- 2026-03-24｜Rene Haas｜product：CEO 重申 Arm 現在提供三種型態：IP、CSS、晶片（原話："IP, CSS and chips. IP, CSS and chips."）

### 問答異常語氣（迴避／改口／保留）
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Quatrochi：10億美元以上上調信心的具體來源（晶圓、記憶體？）｜答法：Rene 答「all of the above」，未指出單一項目，也未給數量
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Quatrochi：超過10億美元部分的毛利率結構｜答法：Jason 稱無變化，沿用上季區間，並說漲價仍在消化、定價待定，詳細更新留到 Q3 末
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Mobley：150億美元（FY31）AGI 營收是否已含供應限制｜答法：Rene 未直接回答是／否，轉談 TAM 上調；Jason 談供應鏈放寬時程，未對 FY29–31 需求給數字
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Arya：為何無法再多確保10億美元供給｜答法：Rene 以整體供應吃緊回應，未說明 Arm 具體卡在哪一環，亦未給額外產能數字
- ARM_Q1_2027_Earnings_Call_20260729.md｜問：Naji：手機單位需求與全年權利金展望｜答法：Rene 把數字交給 Jason；Jason 稱全年「if I had to guess」接近高十幾%，Q2 權利金表述在不同段落為 low teens／low to mid-teens／13%，且說下季再更新

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 2 |
| customer_second_source | found | 4 | 1 |
| customer_concentration_credit | found | 5 | 2 |
| supply_demand_durability | found | 7 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"每顆晶片權利金費率的階梯（v8 2.5-3.5% → v9 ~5% → CSS ~10%）持續往上爬，資料中心的量補上行動段的飽和"},{"id":"H2","text":"自製 AGI CPU 兌現訂單，且不嚴重疏離授權客戶，也不把混合毛利率壓到讓估值框架切換"},{"id":"H3","text":"市場願意繼續用「IP 授權年金」的倍數為 Arm 定價，而不是用「半導體公司」的倍數"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"三法域反壟斷同案，攻擊「中立 IP 商」身分。Qualcomm 於 2025-03 同時向美國 FTC、歐盟執委會與南韓 KFTC 遞交反壟斷投訴，指 Arm 在數十年開放授權後開始限制設計取用。三者皆已動作：FTC 於 2026-05-15 開查（Bloomberg 首報，調查焦點是 Arm 是否在自售競品的同時 degrade/deny 對 Apple／Qualcomm／Nvidia 等數百家授權客戶的架構授權；截至 7 月底仍在文件保全／證據蒐集階段，未提訴）；歐盟執委會已開啟自己的調查（cms.law）；KFTC 於 2025-11-19 突襲 Arm 首爾辦公室。若任一法域強制中立授權，CSS 的 ~10% ASP 溢價失去依據——這正是 H1 費率階梯的心臟。歷史罰則對照：歐盟曾對 Qualcomm 支配地位濫用開罰 €997M。"},{"id":"R2","text":"授權客戶一手保住 Arm 授權、一手出資繞開 Arm。Qualcomm 於 2024-12 陪審團與 2025-09-30 法院裁定中勝訴（法院駁回 Arm 剩餘違約主張並否決重審動議），確立其 Nuvia 血統的 Oryon 核心在既有架構授權下合法——Arm 以併購為由終止架構授權的槓桿在司法上被削弱。同時 Qualcomm 2025-12-10 完成收購 Ventana（RISC-V 伺服器 CPU）、2025-12-18 完成收購 Alphawave（$2.3-2.4B，連結 IP），並於 2026-06-24 發表基於 Oryon 的 250 核 Dragonfly C1000（5GHz、2028 商用），首發部署客戶是 Meta——而 Meta 正是 Arm 自製 AGI CPU 的共同開發客戶。Qualcomm 首席工程師稱 Oryon 核心「僅 1% 或更少源自 Arm 原始技術」，意即高階核心上客戶付的是 ISA 相容性、不是 Arm 的設計。"},{"id":"R3","text":"估值框架由「IP 授權年金」切換為「半導體公司」。機制是 Arm 自己的計畫：FY2031 目標 $25B 營收中 $15B 為自製矽晶片（毛利率 35-42%），混合毛利率將由 97.5% 壓向 63%。第一個財報級顯影是合併毛利率單季跌破 90%，預估最早出現於 Q4 FY27。可比組一旦由 CDNS（34.9x／毛利 85.9%）移向 AVGO（19.0x／毛利 76.3%）與半導體中位（28.19x），倍數壓縮 40-60%。此風險不需要任何競爭者出現，也不需要任何假設失敗——它在 thesis 成功的路徑上。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"FY+2 forward PE ≤ 35x（約 $108）→ 重跑完整 DD；≤ 30x（約 $92）Base 5Y IRR 才過 9%/yr。重啟後角色上限衛星 starter、倉位帽 3%","irr_base_pct":-8.2,"ev5y_pct":-36.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":0.18,"ev5y_pct":-36.5,"irr_base_pct":-8.2,"max_dd_pct":-75.0,"bull_5y_price":288.0,"bear_5y_price":56.0,"p_bull_pct":17.0,"p_bear_pct":35.0,"rearm_trigger":"FY+2 forward PE ≤ 35x（約 $108）→ 重跑完整 DD；≤ 30x（約 $92）Base 5Y IRR 才過 9%/yr。重啟後角色上限衛星 starter、倉位帽 3%","price_at_dd":224.89,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ARM","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Arm Holdings plc"},"oneliner":"授權大增與 AGI CPU 上修都是真的，但權利金只年增 8%，比 7 月指引少 5 個百分點；股價跌到 174.62 美元後，基準五年報酬仍接近零，等約 110 美元再重做研究。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺晶片設計公司的錢：設計開始時收授權費，晶片出貨時收權利金。錢卡在指令集與軟體生態這一節。本季成長靠授權，權利金只年增 8%。","reasoning":"Q2 FY27 營收 14.43 億美元，年增 27%。授權及其他 7.73 億美元（占 54%，年增 50%，比公司預期多約 1 億美元），權利金 6.70 億美元（占 46%，年增 8%）。權利金內部：資料中心翻倍，實體 AI 年增 50%，邊緣 AI 約零成長。毛利率 97.44%（TTM），非 GAAP 營益率 44.2%，GAAP 只有 13.9%，差額幾乎都是股份薪酬。單點依賴：前五大客戶占 FY2026 營收約 57%，最大客戶 Arm China 約 16%；SoftBank 本季貢獻 2.09 億美元，占營收 14.5%，同時是持股約 90% 的控股股東；矽業務的 3 奈米產能靠台積電，首要客戶是 Meta。AGI CPU 尚無營收，首批商業出貨在 FQ4 FY27。","fact_refs":["f_kpi0_total_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi5_guidance_q3_fye27","f_peer_arm_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"中等偏弱。授權占 54%，受簽約時點影響，公司自己看的 ACV 只年增 12%；權利金占 46%，年增 8%；SoftBank 2.09 億美元屬關聯方收入。","unit_econ_note":"單顆晶片費率：v8 約 2.5～3.5%，v9 約 5%，CSS 約 10%（前份論點）。CFO 在 2026-11-04 說 v9 採用已過半，費率順風轉弱，後續要靠 CSS 新世代。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"97% 毛利的指令集授權，靠費率階梯和資料中心份額成長，正在加上 30～40% 毛利的自有晶片"},"industry":{"clock_phase":"III","sd_verdict_source":"WSTS 預估 2026 年全球半導體成長 89.9%，主要靠記憶體，屬過熱段；手機段卻因記憶體漲價而量縮。供需持久性：資料中心 CPU 需求結構性持久，供給可逆性中等，CFO 在 2026-07-29 說供應鏈要到日曆 2028～29 才放寬，之後定價順風可能反轉。","bargaining":{"up":"矽業務對台積電、記憶體、載板與測試機議價力弱，CEO 承認這是第一顆產品，規模不如 AMD。IP 業務沒有這個問題。","down":"前五大客戶占 57%，三家合計 42%；客戶無獨家與最低採購義務，但換架構成本高。","geo":"中國約占營收 18%，經由 Arm 不控制營運的 Arm China；高階 Neoverse 受美英出口管制。"},"profit_pool_dir":"機櫃裡的利潤往加速器與記憶體集中。Arm 用 AGI CPU 往下游多拿美元，但毛利率低得多。OI 池五年前後占比事實表未涵蓋。","tam_table":[{"item":"資料中心 CPU 晶片 TAM","value":"2026-03 Rene Haas 稱 2030 年約 1,000 億美元；2026-07-29 Jason Child 引最新估計 2,200 億美元；2026-11-04 Rene Haas 稱 2,000 億美元以上合理"},{"item":"AI 資料中心權利金 TAM","value":"2026-03 Rene Haas 稱當時約 30 億美元"},{"item":"伺服器 CPU 份額（第三方）","value":"Mercury 估 2026 Q2 出貨 13.6%；TrendForce 估 2026 年超過 20%，2027 年約 30%"},{"item":"頂級超大規模業者份額（管理層）","value":"2024 年 15%，2025 年 50% 以上，2026 年底預期超過 60%"},{"item":"PC 份額","value":"管理層稱占全球出貨 20%"},{"item":"手機份額","value":"約 99%（Morningstar）"},{"item":"RISC-V 滲透率","value":"SHD 估 2024 年 10.4%，市場 520 億美元，2030 年可能超過 2,600 億美元"},{"item":"OI 池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向穩定（→）。機制是指令集加軟體生態的轉換成本；份額還在往上，定價工具卻同時受反壟斷挑戰。","reasoning":"客戶換架構要重寫軟體、重新驗證，生態有三千萬開發者。方向證據用份額軸，因為同業 ROIC 差距事實表未涵蓋。本季新簽 3 份 ATA、4 份 CSS，其中一家主要客戶首次簽 ATA。扣分項只有 RISC-V 屬於生態攻擊；Qualcomm 自研核心仍用 Arm 指令集，算點對點競爭。當期 ROIC 只能定性：高毛利、輕資產，但投入資本事實表未涵蓋，GAAP 營益率 17.02% 與非 GAAP 44.2% 的落差全在股份薪酬。再投資主要走研發費用，研發密度 57.28%，矽業務之後會多出存貨與供應預付。","fact_refs":["f_peer_arm_gross_margin_pct","f_peer_arm_operating_margin_pct","f_peer_arm_fcf_margin_pct","f_peer_qcom_operating_margin_pct","f_peer_cdns_gross_margin_pct","f_peer_avgo_gross_margin_pct","f_peer_snps_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"指令集與軟體生態帶來的轉換成本，加上 v9／CSS 費率階梯","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力擴大：管理層稱頂級超大規模業者的 Arm 伺服器份額由 2024 年 15% 升到 2025 年 50% 以上，第三方數字較低但方向相同。定價力穩定：費率階梯仍在，但 v9 採用過半、順風轉弱，反壟斷調查限制 CSS 往上推的空間。兩者合併判穩定。","competitor_notes":[{"name":"QCOM","strategy_note":"既是占 FY2026 營收 9% 的客戶，也是最直接的對手，自研 Oryon 核心繞開 Arm 的設計費，只留指令集關係。"},{"name":"AMD","strategy_note":"x86 最強對手，TrendForce 估 2026 年伺服器份額約 27%，在晶圓與記憶體的採購規模遠大於首次出貨的 Arm。"},{"name":"AVGO","strategy_note":"矽業務成熟後的參照，靠規模把營業利益率做高，是 Arm 混合毛利率下滑後的倍數下錨。"},{"name":"CDNS","strategy_note":"純 IP／軟體型的倍數上錨，Arm 的矽業務比重一升，就離這個參照越遠。"},{"name":"SNPS","strategy_note":"同屬設計工具與 IP，研發密度約為 Arm 的一半，顯示 Arm 目前的研發負擔偏重。"}],"peer_na_reason":"同業 ROIC 差距事實表未涵蓋，只有毛利率、營益率、FCF 率與研發密度，改用份額方向當可比軸。","threats":[{"level":"🔴","text":"RISC-V 屬生態攻擊。免費開源，Arm 許多客戶同時是主要支持者，客戶沒有獨家或最低採購義務；SHD 估 2024 年滲透率 10.4%。","p":"30%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"客戶自建核心與 AI 加速器分流。Qualcomm Oryon 仍依賴 Arm 指令集；加速器若吃掉 CPU 工作負載，市場會變小，但目前 agentic 工作負載反而增加 CPU 需求。","p":"30%","evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"level":"🟡","text":"AGI CPU 與授權客戶直接競爭。20-F 已寫明客戶可能終止或縮減合作、改用替代架構；目前尚未看到實際流失。","p":"35%","evidence_refs":["competitive_share_entrants#3","customer_second_source#1","channel_business_model_shift#1"]},{"level":"🟡","text":"中國自給政策與出口管制限制高階 Neoverse 在中國的銷售，陸系客戶可能自研或改用對手技術。","p":"40%","evidence_refs":["customer_second_source#2","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（定性判斷，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都成立：本季夥伴出貨超過 100 億顆 Arm 晶片。資料中心受電力限制，每瓦效能是需要而不是想要；手機換機可以延後，所以邊緣 AI 權利金約零成長。"},{"item":"決策層級","level":"🟡","text":"決策單位是 SoC 設計案，換指令集成本高，但客戶無獨家與最低採購義務，Qualcomm 已證明高階核心可以自己做。實際續約率事實表未涵蓋，代理讀數是活躍 ATA 超過 60 家。"},{"item":"價值鏈分配","level":"🟡","text":"機櫃價值主要流向加速器與記憶體，2026-03 管理層估 AI 資料中心權利金 TAM 只有約 30 億美元，遠小於晶片 TAM，這也是 Arm 下場賣晶片的原因。矽業務上游由台積電與記憶體廠掌握，首代毛利率只有 30～40%。"},{"item":"社會容忍度","level":"🔴","text":"FTC 調查 Arm 授權行為是否企圖壟斷，前份另記歐盟與南韓也在查。Arm 同時賣晶片給授權客戶的對手，等於替投訴方加了論據，CSS 費率的實際上限可能低於經濟上限。尚無正式指控。"}],"roiic":"事實表未涵蓋投入資本，無法計算。替代讀數：FY2025→FY2026 GAAP 增量營業利益率約 8.5%（營業利益由約 8.31 億增至約 9.08 億美元，營收由 40.07 億增至 49.20 億美元）。","reinvest_rate":"事實表未涵蓋資本支出明細、折舊、營運資金變動與稅後營業利益，無法計算。研發密度 57.28% 是實質再投資，會計上走費用。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。投入資本缺資料，本輪不算上界，也不用替代讀數充當上界。"}}}},"q3_growth":{"verdict":"五年後跑道仍寬（🟢）：伺服器出貨份額仍低於 35%，AGI CPU 是有訂單的第二條曲線。近兩年共識 EPS 年複合 34.8%，比我相信的快。","reasoning":"成長來自量（資料中心、矽業務）與價（v9／CSS 費率），併購與回購幾乎沒有貢獻。共識 FY2027E 到 FY2029E 非 GAAP EPS 由 2.23 美元到 4.05 美元，兩年複合 34.8%。基期 FY2026 只有 GAAP 0.85 美元，和非 GAAP 共識口徑不同，不拿來算三年 CAGR。內生上界算不出來，缺口無法歸因，這段成長依賴 re-rate，長期信心上限為中。FY2027 全年權利金展望在 2026-07-29 還是接近高十幾%，FQ2 實際 8%、FQ3 指引低個位數，代表高成長是往後遞延，不是已經發生。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_q3_fye27"],"verdict_values":{"growth":{"driver_mix":"量為主（資料中心份額、矽業務出貨），價為輔（v9／CSS 費率），併購與回購接近零。","runway_years":"伺服器出貨份額約 1～2 年到 30%（TrendForce 估 2027 年約 30%），按短跑道給倍數；份額以外還有核心數增加與矽業務。","runway_post_y5":"🟢","endo_ceiling_basis":"本輪算不出內生上界，投入資本、折舊與營運資金變動事實表未涵蓋。共識兩年複合 34.8% 按超過上界處理。","segments":[{"item":"權利金","value":"6.70 億美元，年增 8%，占營收 46%；FQ3 指引季增低十幾%、年增低個位數"},{"item":"授權及其他","value":"7.73 億美元，年增 50%，占營收 54%；含 SoftBank 2.09 億美元；ACV 年增 12%"},{"item":"資料中心權利金","value":"年增翻倍，四大客戶為 Amazon、Google、Microsoft、NVIDIA；占權利金比重未揭露"},{"item":"實體 AI 權利金","value":"年增 50%"},{"item":"邊緣 AI 權利金","value":"約零成長，手機量縮被費率抵銷"},{"item":"AGI CPU","value":"尚無營收，FQ4 FY27 開始出貨；FY27＋FY28 最多 20 億美元；首代毛利率 30～40%"}],"decay_signals":["股份薪酬占營收偏高：含雇主稅 29.5%，逐年是否上升事實表未涵蓋，保守算亮燈","毛利率：TTM 97.44%，季度年比事實表未涵蓋，未亮；矽業務出貨後預期下滑","FCF／淨利：FY2025 為 0.20，FY2026 為 1.05，未連 2 年低於 0.75，未亮","EPS 與營收：FY2027→FY2028 共識 EPS 年增 37.2%，營收 37.6%，差距小於 5 個百分點，未亮","其餘六項（市占、提價後銷量、TAM、產業倍數、維護性資本支出、停止投資）：未見證據或事實表未涵蓋"],"trap_rating":"價值陷阱風險🟡（亮 1 項）；長期成長性🟡"}}},"q4_capital":{"verdict":"現金充足，併購風險小，但股份薪酬吃掉非 GAAP 營業利益的三分之二。","reasoning":"淨現金約 31.21 億美元。FCF／淨利：FY2023 為 1.23，FY2024 為 3.09，FY2025 為 0.20，FY2026 為 1.05，波動很大。Q2 非 GAAP 自由現金流只有 1.10 億美元，Q1 為 6.65 億美元，落差原因事實表未涵蓋。股份薪酬加雇主稅 4.25 億美元，占營收 29.5%，占非 GAAP 營業利益 66.6%。稀釋股數由 FY2023 約 10.26 億升到 FY2026 約 10.64 億，年增約 1.2%，還在 1.5% 以內，但股價下跌會讓同樣金額的薪酬換出更多股。近三年現金去向四分、回購紀錄事實表未涵蓋。","fact_refs":["f_kpi4_sbc_non_gaap","f_kpi3_non_gaap_free_cash_flow","f_net_debt_m","f_shares_diluted_m","f_peer_arm_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"唯一近期併購 DreamBig 於 2026-07-01 完成，約 2.65 億美元，約市值 0.14%，尚無已實現報酬資料。"},{"name":"buyback_yield","applicable":null,"passed":null,"input":"回購金額與均價事實表未涵蓋。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"由 financial_history 淨利÷稀釋 EPS 自算，FY2023 到 FY2026 稀釋股數年增約 1.2%，低於 1.5%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，最大一筆 DreamBig 約市值 0.14%；近三年現金去向事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求非 GAAP EPS 五年複合約 33%。我不信到那個程度，基準約 22%，五年報酬接近零。","reasoning":"要年化 10%，在 30 倍終端本益比下，FY2032 非 GAAP EPS 要到約 9.37 美元。我的基準是 6.10 美元。倍數：FY2027E 78.3 倍，FY2028E 57.1 倍，FY2029E 43.1 倍，前瞻 EV／S 30.2 倍。敏感度（本輪自估）：FY2032 權利金由約 66 億美元降到約 43 億美元，EPS 少約 1.7 美元；矽業務由約 75 億美元降到約 30 億美元，EPS 少約 1.0 美元；終端倍數由 28 倍降到 20 倍，股價少 29%。成長熄火測試：FY2029 之後成長率降到 15%、10%、5%，對應 30、20、15 倍，股價約 122、78、56 美元，三種都低於現價。短期上檔用 FY2028 基準 EPS 2.85 美元×60 倍，中期用 FY2030 基準 EPS 4.35 美元×38 倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_ma_state","f_ma_w52","f_ma_w104"],"verdict_values":{"valuation":{"basis":"非 GAAP Forward P/E，以 FY2027E 為當前財年，FY2028E 為輔","tier":"高毛利 IP 型，正往半導體設計公司過渡","peers":[{"item":"CDNS Forward P/E","value":"34.9 倍，毛利率 85.9%（前份摘要 2026-07-30 讀數，本輪事實表未涵蓋新值）"},{"item":"AVGO Forward P/E","value":"19.0 倍，毛利率 76.3%（前份摘要 2026-07-30 讀數）"},{"item":"半導體中位 Forward P/E","value":"28.19 倍（前份摘要 2026-07-30 讀數）"},{"item":"ARM Forward P/E","value":"78.3 倍（2026-11-07 快照）"}],"fwd_pe":78.3,"peg":2.25,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2027E 78.3 倍除以 FY2027E→FY2029E EPS 年複合 34.8%，PEG 2.25；FY2028E 口徑 1.64。基準五年年化約 −0.4%，低於 8% 的弱門檻，所以維持偏貴。五年分位事實表未涵蓋，只有 4 個年度端點（本益比 26.7、P/S 64.0、EV／S 63.7），不當五年分位用。","upside_short_pct":-2.1,"upside_mid_pct":-5.3,"denominator_disputed":true,"denominator_note":"共識 EPS 是非 GAAP，排除占非 GAAP 營業利益 66.6% 的股份薪酬與雇主稅；GAAP 本益比 200.71 倍。分母本身就是爭點，78 倍不能當便宜的論據。"}}},"q6_how_wrong":{"verdict":"看空可能錯在權利金基期轉易後直接回到 20% 以上；看多可能錯在權利金連 15% 都到不了。","reasoning":"26 週報酬 −18.12%，RSI 31.08，動能沒有過熱，股價貼著 104 週均線 174.4 美元。賣方目標價區間 125～500 美元，高低差 4 倍，且多數早於 11-04 財報，我的基準比賣方平均悲觀。反證、矛盾裁定與觸發條件集中在反證紀錄，這裡不重寫。","fact_refs":["f_week26_return_pct","f_rsi14","f_price_at_dd","f_ma_w104","f_kpi4_sbc_non_gaap"],"verdict_values":{"trap":{"verdict":"🟡","label":"亮燈一項：股份薪酬占營收 29.5%，矽業務上線後毛利率也將下滑"}}}},"scenario_inputs":{"terminal_label":"FY2032E","start":{"eps":2.23,"pe":78.3,"basis":"FY2027E（FY1）非 GAAP 共識 EPS，與終端倍數同為當前財年口徑，Y1～Y5 為 FY2028E～FY2032E"},"eps":{"bull":[3.3,4.7,6.4,8.5,10.8],"base":[2.85,3.55,4.35,5.2,6.1],"bear":[2.5,2.7,2.85,2.95,3.0]},"pe":{"bull":34,"base":28,"bear":20},"p":{"bull":17,"base":48,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-70,"hi":-45,"basis":"已實現跌幅：52 週高點 428 美元（TIKR，2026-06-05 區間）到 174.62 美元，跌 59%。往下：52 週低點 100 美元對現價 −43%，空方終點 60 美元對現價 −66%。取 −45%～−70%。","trigger_time":null},"basis":{"bull":"權利金年增約 25%，矽業務 FY2032 約 160 億美元，等於公司 FY2031 計畫晚一年達成，第二代毛利率到 50%。終端 34 倍，對照 CDNS 34.9 倍（2026-07-30）。","base":"權利金年增約 18%，FY2032 約 66 億美元；授權約 39 億美元；矽業務約 75 億美元、毛利率約 45%；合併毛利率約 75%，非 GAAP 營業利益率約 43%，股數約 11.5 億。終端 28 倍，對照半導體中位 28.19 倍（2026-07-30）。","bear":"權利金年增停在 8%，授權回落，矽業務卡在 30 億美元且毛利率不到 40%，反壟斷限縮 CSS。終端 20 倍，對照 AVGO 19.0 倍（2026-07-30）與成長降到 10% 的情境。空方機率 35% 依據：權利金連續落後、內生上界算不出來、三法域調查未決。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FQ2 權利金年增 8%，FQ3 指引低個位數；手機約占營收 40～45%；RISC-V 和客戶自建持續推進。","assumption":"費率階梯還有空間，手機回穩後權利金回到 20% 以上。","consequence":"五年後虧 50% 最可能的路徑：權利金年增卡在 10% 以下，FY2029 共識落空，本益比由 78 倍壓到 20 倍，股價約 60 美元。","ruling":"採納。這條與 Single Thing 是同一件事，不另立門檻，機率放進空方 35%。","watch":"FQ4 FY27 起的單季權利金年增，以及 FY2028 全年數字。","evidence_refs":["end_markets#4","substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"],"fact_refs":["f_consensus_eps_fy3","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"FTC 調查 Arm 授權是否企圖壟斷，Bloomberg 報導後股價單日跌 8.5%。Qualcomm 案預計 2026 年第四季開庭，屬民事個案，Qualcomm 占 FY2026 營收 9%，約 4.4 億美元。原告律所僅宣布調查，未見已提起的集體訴訟。","assumption":"調查不會限制 CSS 定價，也不會強制中立授權。","consequence":"CSS 約 10% 的費率失去依據，費率階梯斷掉。社會容忍度本輪判紅，是經濟上限之外的第二個天花板。","ruling":"採納但不放進基準。FTC 尚未起訴，現有證據的時間窗蓋不到裁決日，風險未解，2026 年第四季開庭前不可裁決。","watch":"Qualcomm 案判決、FTC 起訴與否、歐盟異議聲明。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#1","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1","customer_concentration_credit#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"首代 AGI CPU 毛利率 30～40%；FY2031 目標 150 億美元矽業務會把混合毛利率由 97.5% 壓向 63%（前份論點）；公司已簽供應合約；Q2 非 GAAP 自由現金流只有 1.10 億美元。","assumption":"營業利益率守得住，市場不把公司改用半導體倍數。","consequence":"矽業務愈成功，倍數愈低。CDNS 34.9 倍到 AVGO 19.0 倍（2026-07-30）之間，代工與記憶體漲價也可能吃掉毛利。","ruling":"採納，基準終端 28 倍就是這個結果。","watch":"合併毛利率、非 GAAP 營業利益率、存貨與供應預付。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"],"fact_refs":["f_kpi1_non_gaap_operating_incom","f_kpi3_non_gaap_free_cash_flow"]},{"view":"論點成功但股東經濟變差","evidence":"股份薪酬加雇主稅 4.25 億美元，占非 GAAP 營業利益 66.6%。SoftBank 持股約 90%，S&P 在 2026-03 將其展望降為負面，授權及設計服務每季約 2 億美元；前五大客戶占 57%。","assumption":"股份薪酬占比隨規模下降，控股股東與小股東利益一致。","consequence":"非 GAAP EPS 高估股東實拿；SoftBank 若需要現金，減持賣壓與關聯方收入回落都會傷害小股東。","ruling":"部分採納。股份薪酬放進 H3 門檻；SoftBank 目前只是評等壓力，沒有減持證據，列為風險監測。","watch":"股份薪酬占營收、SoftBank 評等與持股變動、SoftBank 季度授權金額。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","customer_concentration_credit#4"],"fact_refs":["f_kpi4_sbc_non_gaap"]},{"view":"價格已反映太多","evidence":"FY2027E 本益比 78.3 倍，FY2028E 57.1 倍，前瞻 EV／S 30.2 倍。賣方平均目標價 213～272 美元都早於 11-04 財報。","assumption":"高點回落 59% 代表便宜。","consequence":"已跌多少不是安全邊際。現價要年化 10%，EPS 要年複合約 33%，基準只有約 22%。","ruling":"採納。價格是目前唯一卡住的條件。","watch":"FY2028 共識 EPS 本益比。","evidence_refs":[],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_ev_s_fwd","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 224.89 → 本次 174.62（-22.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=224.89","side_b":"本次 price_at_dd=174.62","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 224.89 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 224.89 美元：Bull 價 288、Bear 價 56，五年期望值 −36.5%，基準年化 −8.2%，不對稱比 0.18","side_b":"本次情境、股價仍用 224.89 美元：Bull 價 367.2、Bear 價 60，五年期望值 −26.4%，基準年化 −5.4%，不對稱比 0.42","ruling":"先換情境、股價不動：五年期望值多 10.1 個百分點，基準年化多 2.8 個百分點。不對稱比由 0.18 變為 0.42。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 224.89 美元：五年期望值 −26.4%，基準年化 −5.4%，不對稱比 0.42","side_b":"本次情境、股價 174.62 美元：五年期望值 −5.3%，基準年化 −0.4%，不對稱比 0.82","ruling":"再換股價、情境不動：起點價下跌 22.4%，五年期望值多 21.2 個百分點，基準年化多 4.9 個百分點，不對稱比由 0.42 升到 0.82。合計五年期望值比前份多 31.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"跌 22% 之後該不該買（現在就買的最強論證）","cause":"價格變動","prior_field":["signal","val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"現在就買的最強論證：股價由高點 428 美元跌到 174.62 美元，跌 59%；RSI 31；AGI CPU 能見度由 10 億美元以上提高到最多 20 億美元；授權年增 50%，12～24 個月後轉成權利金；手機基期 2027 年初轉易；FY2029E 本益比只剩 43 倍。","side_b":"現價要有年化 10%，在 30 倍終端本益比下，EPS 五年複合要約 33%。基準只有約 22%，五年目標約 171 美元，等於不賺。","ruling":"不買，卡住的只有價格。股價由 224.89 美元跌到 174.62 美元，只是從明顯過高回到仍偏貴，結論與偏貴判斷不變。機率維持多 17、中 48、空 35：AGI 上修與權利金落空方向相反，強度相抵。最大回撤區間隨股價下移。","evidence_level":"自算加一手法說","settle_metric":"FY2028 共識 EPS 本益比與 FQ4 FY27 權利金年增","if_then":["如果股價先漲過 52 週均線 209.64 美元而權利金年增仍低於 12%，不追。","如果股價跌到 110 美元以下且權利金年增沒有低於 8%，重跑研究後分批反買，上限 3%。","反向條件：FQ4 FY27 權利金年增 ≥20% 且矽業務確認達 20 億美元，重啟價位上調到 FY2028 共識 EPS 的 45 倍（約 138 美元），建倉上限 3%。"],"evidence_refs":[]},{"axis":"權利金落空與授權大增，護城河與跑道的判斷有沒有變","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"權利金年增 8%，FQ3 指引低個位數；ACV 年增 12%；v9 順風轉弱。","side_b":"資料中心權利金翻倍，主要客戶首次簽 ATA，AGI CPU 訂單延伸到日曆 2027 年，第三方份額持續上升。","ruling":"三項判斷都不改。權利金落空主要來自手機量縮，還沒有證據顯示份額或費率受損；基期轉易後若仍不回升，再下調。","evidence_level":"一手法說、20-F、第三方份額","settle_metric":"基期轉易後兩季的邊緣 AI 權利金年增","if_then":["如果 FQ4 FY27 與 FQ1 FY28 邊緣 AI 權利金連 2 季沒有轉正，護城河方向改為縮減，停止加碼。","反向條件：如果資料中心權利金連 2 季維持翻倍且總權利金年增 ≥20%，定價面改判擴大，重啟價位上調到 45 倍。"],"evidence_refs":["end_markets#4"]},{"axis":"公司類型沿用","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份歸為品質複利成長，未標循環位置。","side_b":"矽業務即將出貨，權利金也受手機週期影響。","ruling":"本輪方法沿用，歸類不變。截至 FQ2 FY27 矽業務營收仍為零，毛利率 97%。2026-07-29 Jason Child 承諾矽業務營收占比到 10% 時獨立列示，屆時改看半導體設計公司的倍數。","evidence_level":"一手法說","settle_metric":"矽業務占營收比重","if_then":["如果矽業務占營收達 10%，基準終端倍數上限由 28 倍降到 25 倍，不追。","反向條件：如果矽業務占比達 10% 而合併營業利益率仍 ≥45%，倍數維持 28 倍。"],"evidence_refs":[]},{"axis":"估值重啟門檻調整（重跑研究與建倉條件）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"FY+2 forward PE ≤ 35x（約 $108）→ 重跑完整 DD；≤ 30x（約 $92）Base 5Y IRR 才過 9%/yr。重啟後角色上限衛星 starter、倉位帽 3%","side_b":"FY2028 共識 EPS 本益比 ≤36 倍（約 110 美元，基準五年年化約 9%）→重跑完整研究；重啟後倉位上限 3%","ruling":"AGI CPU 能見度上修後，基準五年目標由約 155 美元升到約 171 美元，基準年化 9% 對應的價位由約 92 美元升到約 110 美元，兩段門檻併成一段。重跑研究與建倉上限 3% 不變。","evidence_level":"自算加一手法說","settle_metric":"FY2028 共識 EPS 本益比","if_then":["如果本益比 ≤36 倍，重跑完整研究，通過後分批反買。","反向條件：如果 FQ3 FY27 下修矽業務展望到 15 億美元以下，門檻降回 30 倍。"],"evidence_refs":[]},{"axis":"Single Thing 由空白改為 FY2028 權利金年增率","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空值。","side_b":"FY2028 全年權利金年增率低於 15%（2028 年 5 月前後公布）","ruling":"本輪依敏感度選定。權利金落空同時打擊 EPS 與終端倍數，影響大於矽業務落空，也大於單一訴訟事件。","evidence_level":"自算","settle_metric":"FY2028 全年權利金年增","if_then":["如果低於 15%，清倉；未持有者不建倉。","反向條件：如果 ≥20%，重啟價位上調到 45 倍。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空值。","side_b":"本次設六條門檻，含 FY2028 權利金低於 15% 清倉，FTC 起訴或歐盟異議聲明減碼。","ruling":"前份只有風險敘述，沒有結構化門檻；本次把前份合併毛利率跌破 90% 的條件保留下來，其餘新設。","evidence_level":"方法調整","settle_metric":"各門檻首次讀數","if_then":["如果任一清倉條件成立，清倉。","反向條件：如果兩季內所有門檻都未觸發且權利金年增 ≥20%，取消減碼預案。"],"evidence_refs":[]},{"axis":"權利金財測與實際","cause":"新證據","prior_field":null,"side_a":"2026-07-29 Jason Child：Q2 權利金年增 13%，全年接近高十幾%，FY2028、FY2029 的 20% 以上成長不變。","side_b":"2026-11-04 實際 Q2 年增 8%，FQ3 指引低個位數。Jason Child 未再重申 20%，只對手機相關業務說明年至少兩位數。","ruling":"採信實際數字，不採信路徑不變的說法。管理層把落空歸因記憶體漲價，這個歸因標未證，要用基期轉易後的數字檢驗。基準 FY2028 EPS 因此低於共識 7%。","evidence_level":"兩場法說逐字稿","settle_metric":"FQ4 FY27、FQ1 FY28 邊緣 AI 權利金年增","if_then":["如果基期轉易後連 2 季邊緣 AI 權利金沒有轉正，記憶體歸因證偽，基準 EPS 下修 10%，不追。","反向條件：如果 FQ4 FY27 總權利金年增 ≥20%，基準 FY2028 EPS 上調到共識 3.06 美元。"],"evidence_refs":["end_markets#4"]},{"axis":"三段權利金描述和總額對不上","cause":"新證據","prior_field":null,"side_a":"管理層描述：資料中心翻倍，實體 AI 年增 50%，邊緣 AI 約零成長；CFO 又說資料中心去年接近權利金的 20%。","side_b":"自算：權利金由約 6.20 億增至 6.70 億美元，只多約 5,000 萬美元。資料中心若占去年 20%，翻倍增量約 1.24 億美元，邊緣 AI 至少要衰退約 15%，不可能約零成長；若邊緣真的約零成長，資料中心去年不到權利金的 8%。","ruling":"不可裁決至 FQ3 FY27 財報。兩種讀法都偏空：要嘛資料中心比講的小，要嘛手機比講的差。裁決前採保守讀法，資料中心占權利金低於 15%，FY2028 翻倍也只貢獻約 15 個百分點。","evidence_level":"法說數字自算，公司未揭露絕對金額","settle_metric":"資料中心權利金絕對金額或占比","if_then":["如果揭露占比 ≥25%，代表邊緣 AI 實際明顯衰退，下修手機段假設，不追。","如果揭露占比 ≤15%，FY2028 基準權利金年增由 20% 下修到 16%，不追。","反向條件：如果占比 ≥25% 且 FQ4 FY27 邊緣 AI 年增轉正，FY2028 基準權利金年增上修到 25%。"],"evidence_refs":["end_markets#4"]},{"axis":"授權年增 50% 與 ACV 年增 12%","cause":"新證據","prior_field":null,"side_a":"2026-11-04 Rene Haas：授權年增 50% 是未來權利金的領先指標；授權比預期多約 1 億美元。","side_b":"同場 Jason Child：單季授權受時點與會計影響，ACV 才是底層趨勢；ACV 年增 12%，Q1 為 13%。","ruling":"看 ACV。授權大增有真實需求，但單季 50% 不能外推，基準授權 FY2032 只給約 39 億美元。","evidence_level":"一手法說","settle_metric":"ACV 年增","if_then":["如果 ACV 年增連 2 季 ≥15%，授權視為結構性上修，FY2028 基準 EPS 上調到 3.06 美元。","反向條件：如果 ACV 年增連 2 季 <8%，授權按時點性收入處理，不追。"],"evidence_refs":[]},{"axis":"AGI CPU 毛利率與營收措辭","cause":"新證據","prior_field":null,"side_a":"2026-07-29 Jason Child：首代毛利率高 30% 到低 40%；營收「超過 10 億美元」的信心上升。","side_b":"2026-11-04 Jason Child：先重複高 30% 到低 40%，接著說首代可能再低一點，建議用 30% 到 40%；營收改說「最多 20 億美元」。Rene Haas 同場說不擔心毛利。","ruling":"採 30～40%。金額上修是真的，但「最多」是上限不是下限，基準 FY27＋FY28 累計用約 15 億美元。","evidence_level":"兩場法說逐字稿","settle_metric":"FQ4 FY27 首次出貨毛利率；FQ3 FY27 更新的累計營收","if_then":["如果首代毛利率低於 30%，基準矽業務毛利率由 45% 下修到 40%，不追。","反向條件：如果首代毛利率 ≥40% 且累計確認 20 億美元，基準矽業務 FY2032 上修到 100 億美元。"],"evidence_refs":["geo_supply_chain#1"]},{"axis":"伺服器份額口徑","cause":"新證據","prior_field":null,"side_a":"管理層：頂級超大規模業者份額 2025 年 50% 以上，2026 年底超過 60%。","side_b":"Mercury：2026 Q2 出貨份額 13.6%；TrendForce：2026 年超過 20%；Mercury 也認為 AGI CPU 賣到 20 億美元，整體份額仍是低個位數。","ruling":"可調和，分母不同。方向採管理層，規模與 TAM 計算採第三方。","evidence_level":"管理層與第三方研究","settle_metric":"Mercury 與 TrendForce 下一期份額","if_then":["如果第三方份額兩期內沒有增加，下修資料中心權利金路徑，不追。","反向條件：如果 2027 年第三方份額超過 30%，基準資料中心權利金上修。"],"evidence_refs":[]},{"axis":"雙引擎互相強化，還是自家晶片疏離客戶","cause":"新證據","prior_field":null,"side_a":"2026-11-04 Rene Haas 以 OCI 為例，同時提供 NVIDIA Vera 與 AGI CPU 實例，兩項業務互相強化；本季有主要客戶首次簽 ATA。","side_b":"20-F 寫明授權客戶可能縮減合作或轉向替代架構；前份記 Qualcomm 的 Oryon 伺服器晶片首發部署客戶是 Meta，而 Meta 也是 AGI CPU 的主要客戶。","ruling":"目前採 A 側。尚無客戶實際流失的證據；衝突是慢變數，用 ATA 數量與客戶路線圖追蹤。","evidence_level":"法說與 20-F，缺實際流失資料","settle_metric":"活躍 ATA 家數、前五大客戶公開路線圖","if_then":["如果活躍 ATA 連 2 季下降，或前五大客戶公開轉向 RISC-V，減碼一半。","反向條件：如果矽業務占比升到 10% 時 ATA 仍持續增加，把這條風險降級。"],"evidence_refs":["customer_second_source#1","channel_business_model_shift#1"]},{"axis":"共識修正讀數是否可信","cause":null,"prior_field":null,"side_a":"Koyfin 兩份快照 FY1、FY2、FY3 修正全為 0.0%，90 天間距也是 2.23 美元對 2.23 美元。","side_b":"Chartmill 在 2026-10-17 顯示 FY2027 EPS 2.25 美元，近 3 個月上修約 2.13%；11-04 財報後的權利金落空也不可能完全沒反映。","ruling":"視為資料缺口，不當成沒有修正的證據。11-04 的利空推定還沒進賣方模型，下一份快照前凍結任何加碼判斷。","evidence_level":"資料品質問題","settle_metric":"11-04 後 30 天的共識快照","if_then":["如果 30 天後 FY2028 共識下修超過 5%，不追，重啟價位依新共識重算。","反向條件：如果共識上修，維持本輪基準，不因上修提前建倉。"],"evidence_refs":[]},{"axis":"賣方目標價與本輪基準","cause":null,"prior_field":null,"side_a":"賣方平均目標價約 213～272 美元，區間 125～500 美元，多數評等買進。","side_b":"本輪基準五年目標約 171 美元，12 個月約 171 美元。","ruling":"比共識悲觀，理由是市場把 FY2029 EPS 建立在權利金回到 20% 以上，並用 IP 倍數看待 30～40% 毛利的矽業務。賣方全距 4 倍，且多數早於財報，參考價值低，本輪信心也因此只給中。","evidence_level":"聚合站資料，日期不一","settle_metric":"財報後新目標價與權利金實績","if_then":["如果 FQ4 FY27 權利金年增 ≥20%，承認共識較對，基準 EPS 上調。","反向條件：如果權利金年增仍低於 12%，共識下修，不追。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：AMD 上調伺服器 CPU 業務，TrendForce 估 2026 年份額約 27%；Qualcomm 進入資料中心 CPU。","side_b":"結構：x86 頭節點轉向 Arm，Google、NVIDIA 已有實例；其他結構變數是三法域反壟斷與出口管制。","ruling":"雙向拉鋸。需求結構轉好，同時競爭加劇、監管收緊；依據是 11-04 法說與 TrendForce、Bloomberg 報導。","evidence_level":"法說與第三方","settle_metric":"第三方伺服器份額、反壟斷進度","if_then":["如果 FTC 正式起訴，減碼一半。","反向條件：如果 FTC 結案且份額持續上升，定價面改判擴大。"],"evidence_refs":["regulatory_antitrust#1"]}],"triggers":[{"n":1,"text":"股價進入重啟區","type":"估值rearm","maps_to":"價格","metric":"FY2028 共識 EPS 本益比","threshold":"≤36 倍（約 110 美元）","action":"重跑完整研究，通過後分批反買，上限 3%","source_freq":"每日收盤","date":null},{"n":2,"text":"FY2028 權利金年增低於 15%","type":"Single Thing","maps_to":"Single Thing","metric":"FY2028 全年權利金年增","threshold":"<15%","action":"清倉；未持有者不建倉","source_freq":"季度股東信","date":"2028-05"},{"n":3,"text":"FQ3 FY27 財報檢查權利金與資料中心占比","type":"假設驗證","maps_to":"H1","metric":"FQ3 FY27 權利金年增","threshold":"<1%","action":"不追，基準 EPS 下修 5%","source_freq":"季度股東信","date":"2027-02"},{"n":4,"text":"基期轉易後第一個讀數","type":"假設驗證","maps_to":"H1","metric":"FQ4 FY27 權利金年增","threshold":"<12% 為失敗，≥20% 為超標","action":"<12% 不追並下修基準 EPS 10%；≥20% 重啟價位上調到 45 倍","source_freq":"季度股東信","date":"2027-05"},{"n":5,"text":"矽業務累計營收更新","type":"假設驗證","maps_to":"H2","metric":"FY27＋FY28 矽業務累計營收展望","threshold":"低於 15 億美元","action":"不追，重啟門檻降回 30 倍","source_freq":"季度法說","date":"2027-02"},{"n":6,"text":"Qualcomm 案與反壟斷里程碑","type":"風險","maps_to":"R2","metric":"判決或正式指控","threshold":"法院限制 CSS 或授權條款、FTC 起訴、歐盟發出異議聲明，任一成立","action":"減碼一半；未持有者不追，重啟門檻降到 30 倍","source_freq":"法院文件、FTC 公告、6-K","date":"2026-Q4","evidence_refs":["major_events#1","regulatory_antitrust#1"]},{"n":7,"text":"矽業務稀釋開始顯影","type":"風險","maps_to":"R3","metric":"合併毛利率與非 GAAP 營業利益率","threshold":"毛利率 <90% 且營業利益率 <40%","action":"減碼一半","source_freq":"季度股東信","date":"2027-05","evidence_refs":["geo_supply_chain#1"]},{"n":8,"text":"授權客戶開始轉向","type":"風險","maps_to":"R4","metric":"活躍 ATA 家數與前五大客戶路線圖","threshold":"ATA 連 2 季下降，或前五大客戶公開轉向 RISC-V","action":"減碼一半","source_freq":"季度法說、客戶公告","date":null,"evidence_refs":["customer_second_source#1"]},{"n":9,"text":"控股股東壓力","type":"風險","maps_to":"R7","metric":"SoftBank 評等與持股","threshold":"S&P 降到 BB 以下，或公告減持 Arm","action":"不追","source_freq":"評等公告、6-K","date":null,"evidence_refs":["customer_concentration_credit#3"]},{"n":10,"text":"下次財報後複審","type":"複審日期","maps_to":"全部假設","metric":"日期","threshold":"FQ3 FY27 財報公布後","action":"更新情境樹與重啟價位","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"FY2028 全年權利金年增","bear_threshold":"<15%","window":"2028-05 公布","source":"Arm 季度股東信","last_status":"warning"},{"metric":"FY27＋FY28 矽業務累計營收","bear_threshold":"<10 億美元","window":"至 2028-03","source":"Arm 季度法說","last_status":"ok"},{"metric":"合併毛利率與非 GAAP 營業利益率","bear_threshold":"毛利率 <90% 且營業利益率 <40%","window":"FQ4 FY27 起逐季","source":"Arm 季度股東信","last_status":"ok"},{"metric":"ACV 年增","bear_threshold":"連 2 季 <8%","window":"逐季","source":"Arm 季度股東信","last_status":"ok"},{"metric":"FTC 起訴或歐盟異議聲明","bear_threshold":"任一發生","window":"未來 24 個月","source":"FTC、歐盟執委會公告","last_status":"unknown"},{"metric":"股份薪酬含雇主稅占營收","bear_threshold":"連 4 季 >30%","window":"逐季","source":"Arm 季度股東信","last_status":"warning"}],"evidence_dismissed":[{"ref":"capital_markets_pricing#5","reason":"這則 245 美元均值對應的是 2026-06-05 股價 393 美元；股價已跌到 174.62 美元，目標價低於股價的前提不再成立，資料已過期。"}],"action_conditions":{"rearm_trigger":"FY2028 共識 EPS 本益比 ≤36 倍（約 110 美元，基準五年年化約 9%）→重跑完整研究；重啟後倉位上限 3%","exec_line":"未持有者現價不建倉。已持有者不加碼，等 FQ4 FY27 權利金讀數；FY2028 權利金年增低於 15% 就清倉。","holding_cap":"重啟後上限 3%"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方把 FY2029 EPS 4.05 美元建立在權利金回到 20% 以上，並用 IP 公司的倍數看待矽業務；本季權利金年增 8%，矽業務毛利率 30～40%，兩點都還沒被證實。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 FY2028 共識 EPS 本益比降到 36 倍以下（約 110 美元），再重跑完整研究。","qc48_result":"fail","qc48_note":"Bull 情境缺少從出貨量與單價推到 EPS 的算式，成長跑道判綠也撐不住：資料中心的份額已經很高，AGI CPU 尚無營收，所以這條爆發候選的 Bull 依據不成立。"},"thesis":{"H":[{"id":"H1","text":"資料中心權利金繼續翻倍、手機費率往上，帶動全公司權利金在 FY2028 回到年增 20% 以上","2y":"FY2028 權利金年增 ≥20%","5y":"FY2032 權利金約 66 億美元，五年年增約 18%","10y":null,"threshold":"單季權利金年增：FQ4 FY27 ≥12%，FY2028 各季 ≥20%；資料中心權利金年增 ≥100%","source":"Arm 季度股東信與法說；第三方份額看 Mercury Research、TrendForce","drift_rule":"單季年增低於 20% 路徑 5 個百分點以上連 2 季算削弱，低於 10 個百分點以上連 3 季算反轉"},{"id":"H2","text":"AGI CPU 按時放量，授權客戶沒有因此大規模轉向","2y":"FY27＋FY28 累計營收 ≥15 億美元，首代毛利率 ≥30%","5y":"FY2032 矽業務約 75 億美元，毛利率約 45%","10y":null,"threshold":"累計營收 ≥15 億美元；活躍 ATA 不低於 60 家；前五大授權客戶沒有公開把資料中心 CPU 轉到 RISC-V","source":"Arm 季度法說、矽業務獨立列示後的財報、客戶公告","drift_rule":"累計營收展望低於路徑 5% 以上連 2 季算削弱，低於 10% 以上連 3 季算反轉"},{"id":"H3","text":"矽業務拉低毛利率之後，營業利益率還守得住，股份薪酬占比也降下來，才配得上 28 倍終端本益比","2y":"FY2028 非 GAAP 營業利益率 ≥42%","5y":"FY2032 非 GAAP 營業利益率 ≥40%，股份薪酬含雇主稅占營收 ≤20%","10y":null,"threshold":"非 GAAP 營業利益率 ≥40%；股份薪酬含雇主稅占營收逐年下降","source":"Arm 季度股東信的非 GAAP 調節表","drift_rule":"營業利益率低於路徑 5% 以上連 4 季算削弱，低於 10% 以上連 6 季算反轉"}],"R":[{"id":"R1","text":"權利金重新加速落空。2026-07-29 Jason Child 指引 Q2 年增 13%，實際 8%，FQ3 指引低個位數；半導體庫存修正也可能拖累。","h_ref":"H1","clock":"🔥","threshold":"FQ4 FY27 權利金年增 <12%，或 FY2028 前兩季平均 <15%","evidence_refs":["end_markets#4","supply_demand_durability#5"]},{"id":"R2","text":"反壟斷與 Qualcomm 訴訟打的是費率階梯本身。FTC 已在調查，Qualcomm 案預計 2026 年第四季開庭，受影響營收約 4.4 億美元；證券求償目前只到律所調查階段。","h_ref":"H1","clock":"🔥","threshold":"FTC 起訴、歐盟發出異議聲明，或法院限制 CSS 與授權條款，任一成立","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#1","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1","customer_concentration_credit#2"]},{"id":"R3","text":"矽業務成功反而壓低估值倍數。首代毛利率 30～40%，3 奈米產能靠台積電，公司也開始承擔供應鏈中斷風險。","h_ref":"H3","clock":"🔥","threshold":"合併毛利率單季 <90% 且非 GAAP 營業利益率 <40%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"自家晶片與授權客戶形成通路衝突，客戶可能縮減合作或保留路線圖資訊。","h_ref":"H2","clock":"🐢","threshold":"活躍 ATA 連 2 季下降，或前五大客戶公開縮減 Arm 路線圖合作","evidence_refs":["competitive_share_entrants#3","customer_second_source#1","channel_business_model_shift#1"]},{"id":"R5","text":"RISC-V、客戶自建核心與加速器分流，長期壓縮 CPU 權利金基礎。","h_ref":"H1","clock":"🐢","threshold":"RISC-V 進入任一大型雲端業者的主力伺服器 CPU，或旗艦手機 SoC 改用 RISC-V","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"id":"R6","text":"中國自給與出口管制。Arm China 占 FY2026 營收約 16%，Arm 不控制其營運，高階 Neoverse 許可難取得。","h_ref":"H1","clock":"🐢","threshold":"Arm China 占營收單年下降 4 個百分點以上，或出口管制擴及更低階核心","evidence_refs":["customer_second_source#2","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2"]},{"id":"R7","text":"對 SoftBank 與少數大客戶的依賴。SoftBank 持股約 90%，授權及設計服務每季約 2 億美元，S&P 展望負面；前五大客戶占 57%。","h_ref":"H3","clock":"🔥","threshold":"SoftBank 單季授權 <1.5 億美元，或評等降到 BB 以下，或公告減持 Arm","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","customer_concentration_credit#4"]}],"single_thing":{"description":"FY2028 全年權利金年增率低於 15%（2028 年 5 月前後公布）","why_fatal":"權利金毛利率最高，也是授權大增能否變現的驗證。本輪自估：五年權利金年增由 18% 降到 8%，FY2032 EPS 少約 1.7 美元（約 −28%），終端倍數也會由 28 倍往 20 倍掉，合計跌幅約 49%，大於矽業務落空的影響。","if_happens":"共識 FY2029 EPS 4.05 美元失去基礎，五年目標由約 171 美元降到約 88 美元。持有者清倉，未持有者取消重啟條件，直到權利金連 2 季回到 20% 以上。","how_monitor":"看每季股東信的權利金總額與三段增速，先看 FQ3 FY27，再看基期轉易後的 FQ4 FY27，後者應回到 12% 以上。","probability":"約 35%，12～24 個月，主觀估計。Q2 落後指引 5 個百分點、Q3 指引更低；但基期 2027 年初轉易，資料中心翻倍也提供支撐。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":57.07,"peg_fy2":1.64,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":0.85,"FY2027E":2.23,"FY2028E":3.06,"FY2029E":4.05},"fy_end_month":3,"eps_basis":"基期為 GAAP 稀釋 EPS，非 GAAP 全年基期事實表未涵蓋；共識三年為 Koyfin 非 GAAP。兩者口徑不同，成長率以 FY2027E→FY2029E 兩年複合 34.8% 為準。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"regulatory","event":"Qualcomm／Nuvia 案預計開庭","impact":"高","watch":"法院是否限制 Arm 的授權條款或 CSS 安排"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FQ3 FY27 財報，公司承諾更新 AGI CPU 展望","impact":"高","watch":"權利金年增、資料中心占比、矽業務累計營收"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"AGI CPU 首批商業出貨（FQ4 FY27）","impact":"高","watch":"出貨是否如期、客戶是否超出 Meta"},{"date":"2027-Q2","date_precision":"quarter","type":"guidance","event":"下一次 Arm Everywhere 活動，CFO 稱約在 2027 年上半年更新長期目標","impact":"中","watch":"FY2029 之後的矽業務目標與毛利率路徑"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FQ4 FY27 財報，手機基期轉易後第一個完整讀數","impact":"高","watch":"權利金年增是否 ≥12%，合併毛利率是否跌破 90%"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方把 FY2029 EPS 4.05 美元建立在權利金回到 20% 以上，並用 IP 公司的倍數看待矽業務；本季權利金年增 8%，矽業務毛利率 30～40%，兩點都還沒被證實。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=-18.12, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 情境缺少從出貨量與單價推到 EPS 的算式，成長跑道判綠也撐不住：資料中心的份額已經很高，AGI CPU 尚無營收，所以這條爆發候選的 Bull 依據不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
