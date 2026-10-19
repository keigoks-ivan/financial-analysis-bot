你是 DD 管線 v20 的判斷層閘（gate），標的 SNPS（20261019）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑤ 覆蓋面掃描（強制）——facts.json 逐軸點名 status="none"／"not_applicable" 的每一軸：理由站得住嗎？查詢是否切題且足以支撐該軸結論（不以查詢次數計）？**缺軸本身即 🔴，不需先證明結論錯**。[gate_contract §⑤]

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤，缺軸本身即 🔴。
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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝2476.8 USD M｜期間與口徑：Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 news.synopsys.com Q3 FY26 results（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-07-31，公告於 2026-08-26））
  - 註記：新聞稿稱高於財測區間上緣；共識數字未查
- `f_kpi1_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝41.6 %｜期間與口徑：Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 news.synopsys.com Q3 FY26 results（adjusted segment operating income $1,030.4M）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-07-31，公告於 2026-08-26））
  - 註記：未查
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝14.4 %｜期間與口徑：Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 news.synopsys.com Q3 FY26 results（營業利益 $357.5M）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-07-31，公告於 2026-08-26））
  - 註記：未查
- `f_kpi6_guidance_fy2026`（q1_business）｜Guidance FY2026 全年＝營收 $9,690–9,740M；non-GAAP EPS $15.04–15.10；GAAP EPS $3.84–4.08；non-GAAP 營業利益率中點約 41.5%；GAAP 約 10.4%；FCF 約 $2,600M；capex 約 $225M text｜期間與口徑：公告於 2026-08-26／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 news.synopsys.com Q3 FY26 results（numbers.latest_quarter_kpis.items[6]，as_of 公告於 2026-08-26）
  - 註記：yfinance FY1 營收共識 $9,722M、EPS $15.14（見 capital_structure／consensus_revision）
- `f_kpi5_guidance_q4_fy2026`（q1_business）｜Guidance Q4 FY2026＝營收 $2,530–2,580M；non-GAAP EPS $4.10–4.16；GAAP EPS $0.60–0.85 text｜期間與口徑：公告於 2026-08-26／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 news.synopsys.com Q3 FY26 results（numbers.latest_quarter_kpis.items[5]，as_of 公告於 2026-08-26）
  - 註記：未查
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-26 date｜期間與口徑：2026-08-26／距今 38 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-26）
- `f_peer_snps_gross_margin_pct`（q2_moat）｜SNPS 毛利率＝72.38 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNPS.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_snps_operating_margin_pct`（q2_moat）｜SNPS 營業利益率＝11.03 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNPS.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_snps_fcf_margin_pct`（q2_moat）｜SNPS FCF 利潤率＝29.18 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNPS.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_cdns_gross_margin_pct`（q2_moat）｜CDNS 毛利率＝85.87 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CDNS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_cdns_operating_margin_pct`（q2_moat）｜CDNS 營業利益率＝30.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CDNS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_cdns_fcf_margin_pct`（q2_moat）｜CDNS FCF 利潤率＝28.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CDNS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_arm_operating_margin_pct`（q2_moat）｜ARM 營業利益率＝17.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ARM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_qcom_operating_margin_pct`（q2_moat）｜QCOM 營業利益率＝23.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝15.14 USD/share｜期間與口徑：2026-10-19／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-19）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝18.67 USD/share｜期間與口徑：2026-10-19／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-19）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝9722.26 USD m｜期間與口徑：2026-10-19／yfinance revenue_estimate 0y 平均（22 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝11049.98 USD m｜期間與口徑：2026-10-19／yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc`（q4_capital）｜SBC 占營收＝9.35 %｜期間與口徑：Q3 FY2026（季末 2026-07-31，公告於 2026-08-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿：SBC $231.6M ÷ 營收 $2,476.8M（自算）；占 GAAP 營業利益約 64.8%（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-07-31，公告於 2026-08-26））
  - 註記：n/a
- `f_kpi3_free_cash_flow_ytd_9`（q1_business）｜Free cash flow (YTD 9個月，非單季)＝2142.5 USD M｜期間與口徑：前三季累計至 2026-07-31，公告於 2026-08-26／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿現金流量表：營業現金流 $2,298.6M 減資本支出 $156.1M（FCF 為自算，新聞稿未直接列示）（numbers.latest_quarter_kpis.items[3]，as_of 前三季累計至 2026-07-31，公告於 2026-08-26）
  - 註記：全年 FCF 指引約 $2,600M
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝7234.12 USD m｜期間與口徑：2026-10-19／yfinance 最新一季：總債務 10841.79、現金 3607.67（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝191.64 m shares｜期間與口徑：2026-10-19／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝94357.88 USD m｜期間與口徑：2026-10-19／市值 87123.76 ＋ 淨負債 7234.12｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝454.63 USD｜期間與口徑：2026-10-16（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝80.32 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝9.25 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝0.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.2 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝10.02 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝16.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝16.6 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝9.71 x｜期間與口徑：2026-10-19／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：DAC 2026 上 AI 原生新創（Bronco AI、ChipAgents.ai、Verkor.io）展示驗證／除錯與 agent 設計指標，均為廠商自述、未經獨立驗證；文中另述 Synopsys 與 OpenAI 合作 GPT-Synopsys。
  - 來源：ecosistemastartup.com, OpenAI y Synopsys crean GPT-Synopsys para diseñar chips con IA（as_of 2026-07-01）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：36Kr 報導 Kimi K3 模型在不使用 Cadence／Synopsys 商用授權軟體下，48 小時自主完成晶片設計實驗；同文稱要取代仍非常遙遠。
  - 來源：36Kr, Kimi K3 chip design experiment（as_of 2026-07-01）｜affects：decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Pitchgrade 研究筆記把熊市情境描述為晶片設計走向參數化 AI 原生流程、超大型雲端業者自建 EDA 能力而侵蝕 Synopsys 最高價值客戶的份額；定性為長期情境，非現況。
  - 來源：Pitchgrade, synopsys ai margin pressure（as_of 2026-06-01）｜affects：decision_inputs.bear、moat_trend
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：投資人文章稱 Cadence 在數位實作（Innovus 對 Fusion Compiler）逐步取得進展，屬意見文章、非實測份額數據；同彙整稱美國出口管制限制兩家對中國先進節點工具銷售、中國本土對手成長但短期全球取代不太可能。
  - 來源：inpractise.com, Synopsys vs Cadence digital design tool competition and market share（as_of 2026-07-01）｜affects：moat_trend
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2025 年 Q3 財報 Synopsys 因 Design IP 放緩與一家大型晶圓代工客戶困難而低於預期；執行長未點名，Yahoo/Reuters 報導推測為 Intel。2026 年 Q2 展望低於分析師預期（$2.23–2.28B），原因含中國出口管制與主要代工客戶需求較弱。
  - 來源：Yahoo Finance: Synopsys set to wipe out 2025 gains as shares tank on China business woes（as_of 2025-09-10）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：2025-05-29 Synopsys received a BIS letter imposing a license requirement on certain EDA exports to China; it halted new China orders; restrictions were lifted in July 2025.
  - 來源：Synopsys FY2025 ARS (SEC) / TrendForce / DCD search summaries（as_of 2025-05-29）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 annual report says Synopsys expects a challenging near-term environment, including in China, due to macroeconomic factors and Trade Restrictions.
  - 來源：Synopsys Form ARS FY2025 (SEC)（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Feb 2026 (exact day not in snippet): Synopsys guided Q2 revenue $2.23-2.28B, below consensus $2.24B, citing China export restrictions preventing customers from starting new design projects; shares fell >5% after hours.
  - 來源：Techleap feed / Yahoo Finance summary of Synopsys guidance（as_of 2026-02-01）｜affects：valuation、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2023 10-K 風險因素列入中台關係變化，屬海外政經不確定性之一
  - 來源：Synopsys Form 10-K FY2023（as_of 2023-10-31）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2024 10-K：受關稅／出口限制影響的客戶可能自行開發產品或替換 Synopsys 方案
  - 來源：Synopsys Form 10-K FY2024（as_of 2024-10-31）｜affects：moat_trend、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Trefis 9月評論認為「AI 自行設計晶片而繞過 EDA 工具」的威脅可能存在但緩慢，已公布數字尚未證實；管理層仍在摸索 AI agent 以訂閱或用量計價。
  - 來源：Trefis: What Happens To Synopsys Stock If AI Learns To Design Chips Without It?（as_of 2026-09-22）｜affects：decision_inputs.bear、moat_trend
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Pitchgrade 筆記指 AI 多半嵌入 EDA 工具而非取代；真正風險在設計服務與工具使用強度（每案工程師減少可能縮小授權池）。數字未對照一手來源。
  - 來源：Pitchgrade: synopsys ai margin pressure（as_of 2026-09-22）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#6`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 財報後股價下跌約 9.2%（量約 3 倍），理由為 IP 復甦、Ansys 成長持續性與中國出口限制疑慮（單一聚合來源）
  - 來源：FN2 SNPS FY2026 Q2（as_of 2026-05-21）｜affects：decision_inputs.bear、thesis.R
- `major_events#0`（major_events｜方向 -｜狀態 ok）：Kim v. Synopsys (No. 3:25-cv-09410, N.D. Cal.) 證券集體訴訟，class period 2024-12-04 至 2025-09-09，依 Exchange Act 10(b)/20(a)；起因為 FQ3 2025 財報後股價單日跌約 36%；另有 New England Teamsters Pension Fund v. Synopsys (No. 25-cv-10201) 於 2025-10-31 提起，後續修正訴狀增列與併購相關的 Securities Act 主張。原告律所指控未證實。
  - 來源：Hagens Berman / Labaton / Levi Korsinsky 新聞稿（Barchart、hbsslaw.com）（as_of 2025-10-31）｜affects：decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Kim v. Synopsys (No. 3:25-cv-09410, N.D. Cal.)，class period 2024-12-04 至 2025-09-09，指控未揭露 AI 客製化侵蝕 Design IP 經濟性；股價 2025-09-10 單日跌 35.8%。另有 No. 25-cv-10201（2025-10-31）。尚無法院裁決資訊。
  - 來源：Hagens Berman 新聞稿（as_of 2025-10-31）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 8 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNPS_20261019/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1218.0,"bear_5y_price":296.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":80.5,"ev5y_pct":63.4,"irr_base_pct":12.5,"asym_ratio":3.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":15.14,"pe":30.03,"basis":"FY2026E 共識 non-GAAP EPS（財年 10 月底結束，判斷日距年終不到兩週，近似 TTM）；終端倍數同樣套在終端年當年的 non-GAAP EPS"},"eps":{"bull":[19.1,23.6,29.2,36.0,43.5],"base":[18.6,21.9,25.6,29.7,34.2],"bear":[17.6,17.0,17.4,18.0,18.5]},"pe":{"bull":28,"base":24,"bear":16},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SNPS_Q2_2026_Earnings_Call_20260527.md
- 2026-05-27｜CFO｜guidance：全年營收財測區間更新，由三因素構成（上半年表現、Ansys 通路毛額認列、處分 Processor IP）（原話："updated revenue range of $9.625 billion to $9.705 billion"）
- 2026-05-27｜CFO｜guidance：全年 non-GAAP EPS 財測與較前次中點上調幅度（原話："non-GAAP earnings of $14.72 to $14.80 per share"）
- 2026-05-27｜CFO｜guidance：第三季營收目標區間（原話："Total revenue between $2.41 billion and $2.46 billion."）
- 2026-05-27｜CFO｜guidance：全年自由現金流財測上調 1 億美元至約 20 億（原話："free cash flow of approximately $2 billion"）
- 2026-05-27｜CFO｜margin：全年 non-GAAP 營業利益率財測中點 41%，較前次上調 50bp（原話："non-GAAP operating margin of 41% at the midpoint"）
- 2026-05-27｜CFO｜margin：第二季營收含 Ansys 通路改毛額認列的 1250 萬美元，費用等額增加，對 EPS 與現金流中性（原話："added $12.5 million to revenue and an equal amount to expense"）
- 2026-05-27｜CFO｜margin：全年通路會計影響 6000 萬美元營收，並預期逐季成長（原話："you can think about that growing through the year"）
- 2026-05-27｜CFO｜margin：第二季各部門數字：IP 營收年減約 6%、季增 12%，EDA 年增略高於 8%（原話："down approximately 6% year-over-year and up 12% sequentially"）
- 2026-05-27｜CEO｜margin：CEO 說明今年營業利益率較去年底提高逾 300bp（原話："we're raising our operating margin by more than 300 basis points"）
- 2026-05-27｜CFO｜margin：CFO 解釋 Ansys 季節性：Ansys 原 Q4 對應 SNPS 的 Q1，故 Q1 成長偏高（原話："their strongest quarter always being a Q1"）
- 2026-05-27｜CFO｜margin：CFO 說明積壓訂單降至 110 億符合預期，與續約時點有關（原話："We build and then we burn"）
- 2026-05-27｜CEO｜commitment：管理層承諾 IP 今年逐季成長，並稱 Q1 為谷底（原話："Q1, we hit the bottom."）
- 2026-05-27｜CEO｜commitment：預期 FY2026 IP 成長仍低迷，但下半年逐季改善（原話："we continue to expect muted IP growth for fiscal year 2026"）
- 2026-05-27｜CEO｜commitment：到本財年底將有少數客戶簽下新 IP 商業模式合約（原話："we will have few customers with signed agreements"）
- 2026-05-27｜CFO｜commitment：財年底前達成約一半承諾的成本綜效，其餘時程留待投資人日說明（原話："we will have achieved about half of our committed synergies"）
- 2026-05-27｜CFO｜commitment：人力縮減 10% 的承諾維持，多數已完成（原話："we are still committed to the 10%"）
- 2026-05-27｜CEO｜commitment：Synopsys-Ansys 聯合產品的營收綜效從 FY27 開始，4 億美元目標維持（原話："FY '27, because the -- we released to limited set of partners"）
- 2026-05-27｜CEO｜commitment：Multiphysics Fusion 預計 2026 下半年開始商業化放量（原話："will begin ramping into commercial availability in the second half of 2026"）
- 2026-05-27｜CEO｜commitment：管理層表示將改變變現與商業模式，細節留待 9 月 30 日投資人日（原話："we will capture different value and different business model"）
- 2026-05-27｜CFO｜capital_allocation：啟動 2.5 億美元加速股票回購，並另有 5000 萬美元公開市場回購（原話："we initiated a $250 million accelerated share repurchase in March"）
- 2026-05-27｜CFO｜capital_allocation：期末總債務約 100 億美元，並已提前償還部分定期貸款（原話："Total debt at the end of Q2 was approximately $10 billion."）
- 2026-05-27｜CEO｜capital_allocation：宣布與 Elliott 合作協議，Jesse Cohn 出任獨立董事（原話："a cooperation agreement with Elliott Management"）
- 2026-05-27｜CEO｜capital_allocation：Processor IP Solutions 處分預計很快完成，影響本財年營收約 4000 萬美元（原話："expect to close the pending sale of the Processor IP Solutions business shortly"）
- 2026-05-27｜CEO｜product：Multiphysics Fusion 早期結果：收斂速度最高 3 倍（原話："up to 3x faster design closure with higher ECO success rates"）
- 2026-05-27｜CEO｜product：GPU 加速 EDA 已出現早期變現跡象（原話："we're seeing early signs of monetization with GPU-accelerated EDA"）
- 2026-05-27｜CEO｜product：agentic EDA 有 20 家客戶評估，涵蓋逾 25 個專門 AI agent（原話："20 customers now evaluating solutions across more than 25 specialized AI agents"）
- 2026-05-27｜CEO｜product：agent 時代授權構想：由人類訂閱加上 agent 用量計費，仍在早期探索（原話："subscription plus consumption for the agents"）
- 2026-05-27｜CEO｜product：PCIe 7.0 IP 勝率逾 90%，新增 18 份授權（原話："PCIe 7.0 IP achieved a greater than 90% win rate"）
- 2026-05-27｜CEO｜product：發表業界首款 HBM4 IP 測試晶片（原話："we also delivered the industry's first HBM4 IP test chip"）
- 2026-05-27｜CEO｜product：硬體輔助驗證為 Design Automation 主要成長動能（原話："Hardware-assisted verification remained the key growth driver"）
- 2026-05-27｜CEO｜competition：CEO 稱所有自研晶片（COT）客戶都用到其 EDA、HAV、IP 與 S&A（原話："There are none of the COT that does not use the EDA, HAV, IP and S&A."）
- 2026-05-27｜CEO｜competition：先進節點完整流程技術勝利逾 30 件（原話："over 30 full-flow technical wins in the quarter"）
- 2026-05-27｜CEO｜risk：中國設計啟動環境仍受限，財測對中國維持務實（原話："the design start environment in China remains challenged"）
- 2026-05-27｜CEO｜risk：工業與車用領域設計啟動仍偏弱，與 AI 相關領域分化（原話："still fairly muted design start activity in that domain"）
- 2026-05-27｜CFO｜risk：GAAP 費用高於預期，主因重組成本提前認列，GAAP EPS 僅 0.09 美元（原話："primarily due to the accelerated timing of restructuring costs"）
- 2026-05-27｜CEO｜customer：英特爾 18A／14A 等新製程目前財測未計入任何上行，需待從評估轉量產才付費（原話："we're not accounting or taking into account in our guidance any upside"）
- 2026-05-27｜CEO｜customer：Multiphysics Fusion 客戶仍在評估階段，尚未變現（原話："the monetization of that is not happening yet"）
- 2026-05-27｜CEO｜customer：超大規模雲端客戶推動 HAV 與自研晶片需求，一家 HPC 業者已用其方案完成 AI 加速器 tape-out（原話："a leading HPC provider successfully taped out"）

### SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md
- 2026-09-30｜Shelagh Glaser｜guidance：CFO 給 FY27 營收財測：成長 15% 至 111.5 億美元（中點）（原話："We expect to grow revenue 15% to $11.15 billion"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY27 營業利益率擴張 250 bp 至 44%（中點）（原話："expand operating margin 250 basis points to 44%"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY27 EPS 財測 19.08 美元（中點）（原話："to grow EPS even faster at '27 to $19.08"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY27 自由現金流約 31 億美元（原話："free cash flow will be approximately $3.1 billion"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY26 營收預期 97 億美元（原話："for '26, we anticipate revenue of $9.7 billion"）
- 2026-09-30｜Sassine Ghazi｜guidance：長期成長展望：2030 前整體年複合成長率中高個位數（mid-teens），先前為雙位數（原話："the long-term growth outlook is mid-teens CAGR through 2030"）
- 2026-09-30｜Sassine Ghazi｜guidance：長期目標上調 IP 成長：由 mid-teens 到 high teens（原話："from the mid-teens to high teens for IP"）
- 2026-09-30｜Sassine Ghazi｜guidance：長期目標上調 EDA 成長：由雙位數到 mid-teens（原話："from double-digit to mid-teens growth"）
- 2026-09-30｜Shelagh Glaser｜guidance：各業務長期成長下限：EDA 13%（原話："mid-teens growth for EDA with a floor of 13%"）
- 2026-09-30｜Shelagh Glaser｜guidance：各業務長期成長下限：模擬與分析（S&A）10%（原話："double-digit S&A growth with a floor of 10%"）
- 2026-09-30｜Shelagh Glaser｜guidance：各業務長期成長下限：設計 IP 17%（原話："design IP with a floor of 17%"）
- 2026-09-30｜Sassine Ghazi｜guidance：S&A 長期雙位數成長為有機成長，高於 ANSYS 獨立時的有機表現（原話："the long-term double-digit growth, that's organic"）
- 2026-09-30｜Shelagh Glaser｜guidance：EPS 與自由現金流長期以 mid-20s 成長（原話："we will grow EPS and free cash in the mid-20s"）
- 2026-09-30｜Sassine Ghazi｜guidance：AoIP 2030 年營收目標 10 億美元，管理層稱以現有合約為依據（原話："The projected growth for AoIP by 2030 will be $1 billion"）
- 2026-09-30｜Shelagh Glaser｜guidance：FY27 沒有版稅收入，版稅自 FY28 起才進入（原話："There's specifically no royalty in 2027"）
- 2026-09-30｜Sassine Ghazi｜guidance：FY27 營收財測在 9 月提前公布（原本 12 月）（原話："FY '27 outlook at 15% year-over-year growth"）
- 2026-09-30｜Shelagh Glaser｜margin：FY26 全年營業利益率預期 41.5%（原話："our expectation for full year '26 is 41.5%"）
- 2026-09-30｜Shelagh Glaser｜margin：FY26 較 FY25 營業利益率改善 420 bp（原話："420 basis points improvement from fiscal year 2025"）
- 2026-09-30｜Shelagh Glaser｜margin：長期營業利益率目標約 50%（FY2030）（原話："approximately 50% by fiscal year 2030"）
- 2026-09-30｜Shelagh Glaser｜margin：50% 目標高於先前的 mid-40s 預期（原話："That's up from our prior expectation of mid-40s"）
- 2026-09-30｜Shelagh Glaser｜margin：CFO 說明版稅被視為近乎全額利潤，是新的利潤率槓桿（原話："the royalty as being 100% pure margin over time"）
- 2026-09-30｜Shelagh Glaser｜margin：回答 AI 對毛利率影響：與客戶合作時成本不變（原話："our cost doesn't really change"）
- 2026-09-30｜Shelagh Glaser｜margin：營業利益率目標已含投入 AoIP 工廠的成本（原話："does include investing in AIOP (sic) [ AOIP ]"）
- 2026-09-30｜Sassine Ghazi｜margin：CEO 表示不會為了把利潤率從 44% 推到 45–46% 而犧牲成長機會（原話："We will not trade off growth opportunities"）
- 2026-09-30｜Shelagh Glaser｜margin：FY27 起報告口徑改變：半導體事業單位自 ANSYS 移入 EDA（約佔 ANSYS 營收 10%）（原話："move the semiconductor business unit from ANSYS"）
- 2026-09-30｜Sassine Ghazi｜margin：AoIP 三層收費：授權費、客製化費（非 NRE）、版稅（原話："you see here it's different than an NRE"）
- 2026-09-30｜Shelagh Glaser｜commitment：成本綜效 4 億美元提前一年於 FY27 完成（原話："$400 million run rate synergies in fiscal year 2027"）
- 2026-09-30｜Shelagh Glaser｜commitment：FY27 結束時營收綜效年化超過 1 億美元（原話："greater than $100 million run rate in revenue synergies"）
- 2026-09-30｜Shelagh Glaser｜commitment：維持營收綜效 2029 年達 4 億美元年化的承諾（原話："achieve the $400 million run rate synergies by 2029"）
- 2026-09-30｜Sassine Ghazi｜commitment：AoIP 目標為版稅營收大於授權營收（原話："royalty revenue is greater than the license revenue"）
- 2026-09-30｜Sassine Ghazi｜commitment：CEO 回應版稅爬坡期營收是否下滑：不會下滑（原話："there is no dip"）
- 2026-09-30｜Sassine Ghazi｜commitment：FY27 預期出現 AI 營收（原話："for FY '27, we will see revenue from AI"）
- 2026-09-30｜Sassine Ghazi｜commitment：2027 起 ANSYS 與 Synopsys 整合的多物理融合產品開始貢獻營收綜效（原話："In 2027, we will see revenue synergy from that first wave"）
- 2026-09-30｜Sassine Ghazi｜commitment：CEO 收尾承諾（原話："we do what we say and say what we do"）
- 2026-09-30｜Shelagh Glaser｜capital_allocation：股東回報框架：最多將自由現金流的 50% 還給股東（原話："return up to 50% of free cash flow to shareholders"）
- 2026-09-30｜Shelagh Glaser｜capital_allocation：宣布未來數月內回購 10 億美元股票（原話："intent to repurchase $1 billion in Synopsys shares"）
- 2026-09-30｜Shelagh Glaser｜capital_allocation：股權報酬（SBC）佔營收比目標 FY2030 降至 8%（原話："targeting 8% SBC as a percent of revenue by fiscal year 2030"）
- 2026-09-30｜Shelagh Glaser｜capital_allocation：優先順序之一：維持投資等級評等，已提前還清定期貸款（原話："pay off the term loans early"）
- 2026-09-30｜Sassine Ghazi｜product：AoIP（原稱 Factory 2）：與客戶早期共同定義系統並共同設計 IP；Factory 1 持續投資（原話："We'll continue investing in this factory"）
- 2026-09-30｜Sassine Ghazi｜product：亞馬遜協議的 10 億美元為授權費，涵蓋三款晶片的多世代（原話："The $1 billion is a license fee"）
- 2026-09-30｜Sassine Ghazi｜product：版稅時程：設計到量產約 14 個月後才開始放量（原話："14-ish months of design to tape out and production"）
- 2026-09-30｜Sassine Ghazi｜product：下一代 ZeBu 硬體系統代號 Artemis，預計 FY27 上半年（原話："first half of '27, the code name is Artemis"）
- 2026-09-30｜Sassine Ghazi｜product：宣布與 OpenAI 多年合作，推出以 Synopsys 工具後訓練的 GPT-Synopsys（原話："a partnership multiyear with Synopsys and OpenAI"）
- 2026-09-30｜Sassine Ghazi｜product：CEO 說明 GPT-Synopsys 後訓練成本由 OpenAI 負擔（原話："OpenAI will have to invest hundreds of millions of dollars"）
- 2026-09-30｜Sassine Ghazi｜product：第三種模式的營收與 OpenAI 分成，依成果計價（原話："revenue share split between us and OpenAI"）
- 2026-09-30｜Sassine Ghazi｜product：Agent 工程師平台使 VCS／Verdi 授權使用量增加的示例（原話："5 to 10x more VCS and Verdi licenses"）
- 2026-09-30｜Shankar Krishnamoorthy｜product：AI 代理工程師已與頂尖客戶展開 50 個以上合作（原話："Over 50 engagements with all the top customers"）
- 2026-09-30｜Sassine Ghazi｜product：目前客戶 AI 合作多落在第二種模式（客戶自建平台＋買 Synopsys 代理），其次全堆疊，再其次前沿模型（原話："most of our customer engagements are in 2, then 1, then 3"）
- 2026-09-30｜Sassine Ghazi｜competition：CEO 回應「AI 模型可取代 EDA」的外界推論（原話："extrapolation cannot be more far off than reality"）
- 2026-09-30｜Sassine Ghazi｜competition：回答 AI 是否能繞過 EDA：否（原話："not be a point where you can bypass EDA completely"）
- 2026-09-30｜Sassine Ghazi｜competition：客戶對 AI 的立場摘要語（原話："In AI, we believe, but in physics, we trust."）
- 2026-09-30｜Sassine Ghazi｜competition：CEO 提到投資人曾反覆詢問 Intel 流失問題，並回應 Synopsys 與 Intel 持續合作（原話："You've lost Intel. Are you at Intel?"）
- 2026-09-30｜Sassine Ghazi｜competition：CEO 論述 IP 在晶圓代工中的必要性（原話："be in the foundry business without having Synopsys IP"）
- 2026-09-30｜Sassine Ghazi｜risk：中國市場 IP 需求放緩，原因為先進製程受限（原話："the China opportunity as it relates to IP has slowed down"）
- 2026-09-30｜Sassine Ghazi｜risk：客戶在續約時不願簽 3 年固定容量，因為尚不知需多少容量（原話："not going to commit for 3 years at a certain level"）
- 2026-09-30｜Sassine Ghazi｜risk：現階段客戶仍偏好訂閱制而非用量計費（原話："primarily the customer comfort zone is subscription"）
- 2026-09-30｜Sassine Ghazi｜customer：ANSYS 併購使客戶基數擴大 10 倍（原話："expanded the Synopsys customer base by 10x"）

### 問答異常語氣（迴避／改口／保留）
- SNPS_Q2_2026_Earnings_Call_20260527.md｜問：Quatrochi 問 3,500 萬美元財測上調中 EDA 與 IP 各占多少｜答法：CEO 未拆分數字，改談 AI 半導體需求與全產品線強度
- SNPS_Q2_2026_Earnings_Call_20260527.md｜問：Panigrahi 問剩餘成本綜效的規模與時程｜答法：CFO 只重申年底達一半，剩餘綜效時程與規模推到投資人日再談，未給數字
- SNPS_Q2_2026_Earnings_Call_20260527.md｜問：Celino 問 Ansys 季增中段十幾 % 對比財測約 10% 的下半年減速原因｜答法：CEO 先談整合與需求，CFO 以 Ansys 會計年度重編的季節性機械因素回答，未直接量化下半年減速
- SNPS_Q2_2026_Earnings_Call_20260527.md｜問：Tilton 問成長率能否提升或僅是持久性，及成長形狀｜答法：CEO 未給成長率數字或形狀，強調變現模式轉變並推到投資人日
- SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md｜問：Jay Vleeschhouwer：核心 EDA 近年低至中個位數成長、甚至有季減，如何達到 mid-teens？｜答法：CEO 以續約洽談中客戶要更多 AI 容量與多物理融合為由，稱 FY27 為由下而上推估且信心高，未回應核心 EDA 單獨的成長數字或所需增量
- SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md｜問：Vivek Arya：請量化明年及 2030 模型中的版稅金額｜答法：CFO 稱 FY27 無版稅、AoIP 10 億含授權與版稅，並表示 We didn't give a split，未給比例
- SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md｜問：Jason Celino：若替代方案的成果比 GPT-Synopsys 更好，客戶仍會付費嗎？｜答法：CEO 轉談三種客戶選擇與工具需求，未直接回答成果較差時是否付費
- SNPS_Analyst_Investor_Day_Synopsys_Inc_20260930.md｜問：Joshua Tilton：Factory 2 後續客戶管線為何；OpenAI 合作是否對 Synopsys 獨家｜答法：CEO 未給管線規模，稱對話進行中；獨家性問題回稱不偏袒、其他模型商是否跟進由對方決定

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 4 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 4 | 4 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 4 | 4 |
| capital_markets_pricing | found | 7 | 3 |
| major_events | found | 2 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Synopsys largest customer in-house EDA OR second source 2026；Synopsys customer concentration risk largest customer Intel percent of revenue 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SNPS","date":"2026-10-19","schema":"v15.0","contract":"v19","company_name":"Synopsys, Inc."},"oneliner":"AI 讓晶片設計更複雜，工具用量隨之增加。Synopsys 連兩季超預期並上調財測，FY27 共識前瞻約 24 倍、PEG 約 1，價格合理；關鍵在核心 EDA 年增能否從 8.5% 拉到 13% 以上，並守住 FY27 財測。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNPS_20261019/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNPS_20261019/scenario.json","answers":{"q1_business":{"verdict":"Synopsys 賺的是全球晶片設計研發預算：EDA 軟體訂閱（多年期授權）、硬體驗證設備、介面 IP 授權（正轉向授權加版稅），再加上 Ansys 的模擬軟體。錢卡在簽核精度與晶圓代工製程認證這一節點，客戶要投片就繞不過去。","reasoning":"營收分部（Q3 FY26 法說）：Design Automation 約 20 億美元，約占 81%，內含 Ansys 約 7.11 億，調整後營業利益率 45.2%；Design IP 4.74 億美元，約占 19%，年增約 11%，調整後營業利益率 26.5%。最新一季營收 24.77 億美元，non-GAAP 營業利益率 41.6%，GAAP 只有 14.4%，差距主要來自 Ansys 無形資產攤提、SBC 與重組費用。FY26 全年財測營收 96.9–97.4 億美元、non-GAAP EPS 15.04–15.10；積壓訂單 109 億美元，約一年營收，收入能見度高。產業位置屬擴張期：管理層說 AI 設計啟動持續加速，非 AI 設計啟動近兩季止穩，Q3 硬體驗證營收創紀錄。供需屬結構性持久：多晶粒與先進封裝讓每個案子的工具用量上升，EDA 產業年複合成長 13%，高於半導體研發支出的 7%。單點依賴：FY2023 10-K 揭露單一客戶占營收 12.4%，FY2018 前點名為 Intel；併入 Ansys 後客戶數擴大 10 倍，集中度應已稀釋，但最新年度數字事實表未涵蓋。議價權：上游供應商議價弱，主要成本是人才；下游 hyperscaler 自研晶片客戶的議價力上升，續約時不願承諾三年固定容量。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_margi","f_kpi2_gaap_operating_income_ma","f_kpi6_guidance_fy2026","f_kpi5_guidance_q4_fy2026","f_earnings_recency"],"verdict_values":{"revenue_quality":"以多年期訂閱授權為主，積壓訂單 109 億美元（Q3 FY26，因處分處理器 IP 季減）；硬體驗證與 IP 授權認列較不平均。","unit_econ_note":"每個先進製程設計案需要的工具授權數與驗證容量隨複雜度上升；管理層稱 agent 工作流讓 VCS／Verdi 授權用量增加 5–10 倍（投資人日 2026-09-30，公司自述，未經獨立驗證）。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高毛利設計軟體寡占，正從大型併購後修復利潤率"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：AI 設計啟動加速、非 AI 兩季止穩（Q3 FY26 法說 CEO）；EDA 年複合 13% 高於半導體研發 7%（SemiAnalysis primer）。","bargaining":{"up":"上游以人才與運算資源為主，與 NVIDIA 是 GPU 加速合作關係，沒有供應商卡脖子。","down":"FY2023 單一客戶占 12.4%；hyperscaler 自研晶片客戶議價力上升，續約時不願承諾三年固定容量（投資人日 CEO）。","geo":"中國約占季營收 10%（2025-04 季，第三方估計），受出口管制影響；韓國今年營收占比接近 20%（Q3 FY26 法說分析師提問）。"},"profit_pool_dir":"利潤池往設計前段集中：多物理模擬與 IP 客製化讓 EDA 廠在晶片研發預算的占比上升；但 OpenAI 合作採營收分成，部分價值要讓給模型商。","tam_table":[{"item":"CY2025 EDA 營收規模","value":"Synopsys 約 80 億美元（含 Ansys）、Cadence 53.0 億、Siemens EDA 約 22–25 億（SemiAnalysis，2026）"},{"item":"三大廠合計市占","value":"逾 85%；Synopsys 與 Cadence 各約 30%（Barchart 引述分析師）"},{"item":"產業成長","value":"EDA 年複合 13%，半導體研發支出 7%"},{"item":"新品類：IP 客製化加版稅","value":"管理層目標 2030 年營收 10 億美元，FY27 沒有版稅，FY28 起才開始（投資人日）"},{"item":"新品類：AI agent 用量計費","value":"50 個以上客戶合作進行中；計價方式仍在早期探索，客戶目前偏好訂閱"},{"item":"OI 池五年遷移","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河穩定（→），等級 B。機制是簽核精度加上晶圓代工製程認證造成的轉換成本，三家寡占合計逾 85%；但對最強同業的報酬差距目前為負，定價能否延伸到 agent 用量仍未證明。","reasoning":"機制：先進製程投片動輒數億美元，客戶要求工具結果準確、可重現，加上與晶圓代工共同認證的製程設計套件，形成轉換成本（投資人日 CEO：「In AI, we believe, but in physics, we trust.」）。IP 端 PCIe 7 勝率逾 95%、車用設計勝率連三季逾 90%、die-to-die 累計逾 100 個設計勝利，顯示介面 IP 地位未動搖。方向證據：Synopsys 與 Cadence 各約 30% 市占，搜尋未找到 2026 年客戶從對手轉向 Synopsys 的具名案例，也未見反向流失；Cadence 在數位實作推進只出自意見文章。同業比較：TTM GAAP 營業利益率 Synopsys 11.0%、Cadence 30.8%，毛利率 72.4% 對 85.9%，差距主因是 Ansys 攤提與產品組合。差距為負，合併分不能給到 8 以上，因此落在 B。FCF 利潤率 29.2% 對 28.6%，現金面兩家相當。執行力 8：連兩季超預期並上調財測，成本綜效提前一年；但 2025 年 9 月 IP 低於預期曾讓股價單日跌 35.8%。定價力 7：AI 讓工具用量增加，但客戶續約不願承諾三年固定容量、偏好訂閱而非用量計費，中國 IP 需求也放緩。產業態勢屬雙向拉鋸：A 競爭面 AI 原生新創與 Cadence 推進都屬自述或意見，尚未證實；B 結構面 EDA 成長快於研發支出，屬結構性轉好；C 出口管制與商業模式轉向用量計費仍是變數。","fact_refs":["f_peer_snps_gross_margin_pct","f_peer_snps_operating_margin_pct","f_peer_snps_fcf_margin_pct","f_peer_cdns_gross_margin_pct","f_peer_cdns_operating_margin_pct","f_peer_cdns_fcf_margin_pct","f_peer_arm_operating_margin_pct","f_peer_qcom_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"簽核精度與晶圓代工製程認證造成的轉換成本，加上 silicon-proven 介面 IP 的規模優勢；三家寡占合計逾 85%。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"市占兩家各約 30%，三家寡占逾 85%，沒有具名客戶轉移；IP 關鍵標準勝率逾 90–95%。GAAP 營業利益率 11.0% 對 Cadence 30.8% 主要是併購攤提，不是份額流失。Cadence 數位實作推進屬意見文章，不足以判為下降；AI 帶來的用量增加尚未轉成可驗證的定價提升，也不足以判為上升。","competitor_notes":[{"name":"CDNS","strategy_note":"最直接對手，市占約 30%，GAAP 營業利益率與毛利率都高於 Synopsys；有文章稱其數位實作工具推進，但沒有份額數據。"},{"name":"ARM","strategy_note":"處理器 IP 授權加版稅模式；Synopsys 已出售處理器 IP，雙方直接重疊縮小，ARM 主要作為版稅模式的參照。"},{"name":"QCOM","strategy_note":"既是客戶也是授權模式的可比公司，毛利率 54% 含硬體，只當作授權變現的參照，不當護城河對照。"},{"name":"688521.SH","strategy_note":"中國本土 IP 與設計服務廠，事實表無財務資料；可作為出口管制下中國客戶尋找替代的觀察點。"}],"peer_na_reason":null,"threats":[{"level":"🟡","text":"Cadence 在數位實作逐步推進，屬點對點競爭；目前只有意見文章，沒有份額數據。","p":"30%","evidence_refs":["competitive_share_entrants#5"]},{"level":"🔴","text":"Hyperscaler 自建設計能力與 AI 原生流程，可能侵蝕最高價值客戶；10-K 也承認受管制影響的客戶可能自行開發或改用替代方案。屬生態攻擊，目前定性為長期情境。","p":"30%","evidence_refs":["competitive_share_entrants#3","geo_supply_chain#2","competitive_share_entrants#1"]},{"level":"🔴","text":"AI 讓每個設計案需要的工程師變少，授權總數可能隨之縮小；管理層的反論是 agent 呼叫工具的頻率更高。若改用用量計費卻談不攏，就會變成減量。","p":"30%","evidence_refs":["substitute_technology#2","substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（推論：Ansys 約 350 億美元收購讓投入資本大增；投入資本實際數字事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是設計工程師，決策者是研發主管，付款者是晶片公司，三個角色都成立。客戶要解決的是「投片一次成功」，延後購買的代價是投片失敗與上市延誤；AI 與先進封裝讓設計啟動加速，非 AI 兩季止穩（Q3 FY26 法說）。"},{"item":"決策層級","level":"🟢","text":"替代要在整套流程與製程認證的層級發生，不是單一工具；管理層稱所有自研晶片客戶都用到其 EDA、硬體驗證、IP 與模擬（Q2 FY26 法說）。反例：Cadence 數位實作推進，代表單點工具層級仍可被替換；客戶也不願承諾三年固定容量。"},{"item":"價值鏈分配","level":"🟡","text":"EDA 占半導體研發支出的比重上升（13% 對 7%），但 hyperscaler 客戶議價力增強，OpenAI 合作採營收分成，GPU 加速的部分價值歸 NVIDIA；客戶自建 agent 的能力正在形成。"},{"item":"社會容忍度","level":"🟡","text":"屬政策風險而非價格天花板：2025-05 美國商務部曾對中國 EDA 出口加授權要求，同年 7 月解除；FTC、歐盟與英國對 Ansys 併購都要求剝離資產，三家寡占持續受反壟斷關注。"}],"roiic":"事實表未涵蓋投入資本與 Ansys 分部營業利益，無法計算。僅能指出：Ansys 約 350 億美元收購，FY26 貢獻營收約 29.8 億，營收對收購價約 8.5%。","reinvest_rate":"有機再投資率低：FY26 資本支出指引約 2.25 億美元，對比 FCF 約 26 億（約 9%）。研發費用化占營收約 30.6%，這才是實質再投資；D&A 與營運資金變動事實表未涵蓋。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。有機實體再投資很少，研發又全數費用化，公式算出的天花板會偏低；共識 EPS 成長主要靠利潤率擴張與併購綜效，不是靠新增投入資本。"}}}},"q3_growth":{"verdict":"Runway 中等（🟡）：EDA 本身已高度寡占、滲透率高，第二條曲線（IP 客製化加版稅、AI agent 用量、多物理整合）都有具名合約與時程，但 FY27 沒有版稅，agent 計價也尚未定案，營收還沒看到。","reasoning":"成長來源：量（設計啟動數、每案工具用量）為主，加上併購（Ansys 併入使 Q3 營收年增約 42%）與利潤率擴張；回購貢獻小。共識 EPS 只有兩年：FY26E 15.14、FY27E 18.67，年增 23.3%；同期共識營收 97.2 億到 110.5 億，年增 13.7%，EPS 比營收快約 9.6 個百分點，差距來自利潤率擴張（管理層 FY26 41.5%→FY27 44%→2030 約 50%）與 4 億美元成本綜效。第三年共識事實表未涵蓋；管理層長期框架是 EPS 年增 mid-20s 到 2030。缺口歸因：利潤率擴張，加上研發費用化使公式天花板失真，不屬無法歸因。為什麼不是 🟢：第二條曲線有 Amazon 逾 10 億美元授權與 OpenAI 合作佐證，但版稅要到 FY28，客戶目前偏好訂閱；分析師在投資人日問到核心 EDA 近年只有低至中個位數成長，管理層沒有回答單獨的成長數字。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_guidance_fy2026"],"verdict_values":{"growth":{"driver_mix":"量（設計啟動數與每案工具用量）為主，併購（Ansys）與利潤率擴張次之，淨回購很小。","runway_years":"事實表未涵蓋滲透率數據；EDA 三家寡占逾 85%，核心市場滲透已高，延伸空間在多物理模擬與 IP 版稅。","runway_post_y5":"🟡","endo_ceiling_basis":"有機實體再投資率約 9%（資本支出對 FCF），投入資本與 ROIIC 事實表未涵蓋，無法給數值天花板。共識 EPS 23% 年增明顯高於有機再投資能支撐的幅度，差額由利潤率擴張與綜效解釋，因此視為超出天花板。","segments":[{"item":"Design Automation（含 Ansys 約 7.11 億）","value":"Q3 FY26 約 20 億美元，調整後營業利益率 45.2%；其中 EDA 年增 8.5%（去年同期基期 16%），Q4 與全年預期雙位數"},{"item":"Design IP","value":"Q3 FY26 4.74 億美元，年增約 11%，調整後營業利益率 26.5%；長期下限 17%（投資人日）"},{"item":"Ansys（模擬與分析）","value":"FY26 貢獻約 29.8 億美元，長期下限 10%；FY27 起半導體業務約占 Ansys 營收 10%，將改列入 EDA"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":true,"note":"年度毛利率 80.6%→79.7%→77.0%，TTM 72.4%，主因 Ansys 組合與攤提"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"只有意見文章，沒有份額數據"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"事實表未涵蓋"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY27 共識 EPS +23.3% 對營收 +13.7%"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"note":"FY24 0.56、FY25 1.01，未連續"},{"signal":"SBC／營收逾 5% 且逐年上升","lit":false,"note":"Q3 為 9.35%，逾 5%；是否逐年上升事實表未涵蓋，管理層目標 2030 年降至 8%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"AI 替代屬推論，尚無數據"},{"signal":"產業估值倍數近三年系統性下移","lit":false,"note":"事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"資本支出約 2.25 億對 FCF 約 26 億"},{"signal":"停止投資新產能且營收三年內下滑","lit":false,"note":"不適用"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：Ansys 收購的報酬尚未證明高於資金成本，回購的盈餘收益率也偏低；SBC 毛稀釋約每年 1%，可以接受。","reasoning":"現金去向（近兩年）：一是 Ansys 約 350 億美元收購，現金加股票，其中約 100 億用債務融資；二是提前還清定期貸款，Q3 末總債務約 100 億、現金及短投 36 億；三是回購，Q2 啟動 2.5 億 ASR 與 0.5 億公開市場回購，投資人日再宣布數月內回購 10 億；四是股息，事實表未列，本包只提回購。股東回報框架為最多 FCF 的 50%。FCF 轉換：FY25 FCF 13.5 億對淨利 13.3 億，約 1.0 倍；FY26 指引 FCF 約 26 億，遠高於 GAAP 淨利，差額主要是攤提與 SBC。SBC 占營收 9.35%，換算每年約 9.3 億美元，管理層目標 2030 年降至 8%。","fact_refs":["f_kpi4_sbc","f_kpi3_free_cash_flow_ytd_9","f_kpi6_guidance_fy2026","f_net_debt_m","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"Ansys FY26 營收約 29.8 億÷收購價約 350 億＝約 8.5%；即使套用公司整體 non-GAAP 營業利益率 41.5%，稅前報酬也只有約 3.5%，低於合理資金成本。Ansys 分部營業利益事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"以 454.63 美元回購，FY26E non-GAAP 盈餘收益率 15.14÷454.63＝3.3%，GAAP 約 0.9%；10 年期公債殖利率事實表未涵蓋，但只要高於 1.3%，3.3% 就達不到殖利率加 2 個百分點。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 2.316 億×4≈9.3 億÷市值 871 億≈1.1%／年毛稀釋，扣除回購後更低；股數歷史事實表未涵蓋，淨額無法精算。"}]},"governance":{"capital_returns":[{"item":"Ansys 收購","value":"約 350 億美元，現金加股票，約 100 億債務融資，2025-07-17 完成；光學事業群依監管要求剝離給 Keysight"},{"item":"償債","value":"定期貸款提前還清；Q3 FY26 總債務約 100 億，淨負債 72.3 億（含租賃）"},{"item":"回購","value":"Q2 FY26 2.5 億 ASR 加 0.5 億公開市場；投資人日宣布未來數月回購 10 億"},{"item":"回報框架","value":"最多 FCF 的 50% 還給股東，並維持投資等級評等"},{"item":"處分","value":"處理器 IP 業務於 Q3 FY26 出售，FY26 營收約減 4000 萬"}]}}},"q5_valuation":{"verdict":"現價要求 FY27 財測兌現（營收年增 15%、EPS 19 美元上下），之後 EPS 每年維持高十幾 % 成長。在不計 AI 版稅大爆發的前提下，我大致相信，因此估值合理，但談不上便宜。","reasoning":"FY27 共識 EPS 18.67 對應前瞻 24.4 倍，FY26E 為 30.0 倍；FY26→FY27 共識 EPS 年增 23.3%，PEG 約 1.05。P/S 9.25 倍，落在四個年度端點的最低端；EV/S 10.0 倍，分位 16.6。GAAP trailing P/E 80 倍，因為攤提與 SBC 被計入。non-GAAP 排除的 SBC 稅前約每股 4.8 美元，把它當成真實成本，倍數就更滿，所以不判便宜。賣方平均目標價約 564–571 美元（2026 年 7–9 月三份彙整），比現價高約 24–26%，方向支持合理偏低的判斷。短期上檔：FY27 EPS 18.67×27 倍≈504 美元，約 +11%。中期上檔：本案基本情境 FY29 EPS 25.6×25 倍≈640 美元，約 +41%。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"valuation":{"basis":"前瞻 non-GAAP P/E 與 PEG；P/S、EV/S 作為輔助","tier":"高毛利設計軟體","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業倍數，無法當作估值錨；Cadence 前瞻倍數事實表未涵蓋。"},"fwd_pe":24.35,"peg":1.05,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY27 前瞻 24.4 倍÷FY27 共識 EPS 年增 23.3%＝PEG 約 1.05，屬合理區間。P/S 在四個年度端點的低端（分位 0.2），EV/S 分位 16.6，偏便宜；但 non-GAAP 排除稅前每股約 4.8 美元的 SBC，GAAP P/E 80 倍，又抵銷一部分。五年分位事實表未涵蓋（只有四個年度端點），結論是合理，不是便宜。","upside_short_pct":11,"upside_mid_pct":41,"denominator_disputed":false,"denominator_note":"GAAP 與 non-GAAP 差距大（FY26 GAAP EPS 3.84–4.08 對 non-GAAP 15.04–15.10），主要是 Ansys 攤提（非現金）、SBC 與重組費用。本案用前瞻 non-GAAP，但把 SBC 視為真實成本，所以不據此主張便宜。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方：把管理層剛上調的長期框架當成既定事實。核心 EDA 近兩季只有約 8%，FY27 卻要做到 13% 以上；一年前 IP 低於預期曾讓股價單日跌 36%。","reasoning":"衰退信號亮兩個：毛利率下滑、EPS 成長遠快於營收成長，兩者都可由併購攤提與利潤率擴張解釋，不是需求衰退，屬中度風險。三個視角的反證與裁定見反證紀錄。","fact_refs":["f_peer_snps_gross_margin_pct","f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"兩個衰退信號亮起，皆屬併購與利潤率結構造成，需求面尚未見衰退"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":15.14,"pe":30.03,"basis":"FY2026E 共識 non-GAAP EPS（財年 10 月底結束，判斷日距年終不到兩週，近似 TTM）；終端倍數同樣套在終端年當年的 non-GAAP EPS"},"eps":{"bull":[19.1,23.6,29.2,36.0,43.5],"base":[18.6,21.9,25.6,29.7,34.2],"bear":[17.6,17.0,17.4,18.0,18.5]},"pe":{"bull":28,"base":24,"bear":16},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"max_dd":{"lo":-50,"hi":-35,"basis":"2025-09-10 IP 低於預期，股價單日跌 35.8%；Q2 FY26 財報後又跌約 9%。熊市路徑下倍數由 30 倍壓到 16 倍、EPS 不成長，就是約 −35%；再疊加財報跳空與大盤修正，下緣延伸到 −50%。","trigger_time":null},"basis":{"bull":"照管理層長期框架：營收年增 mid-teens，營業利益率 2030 年約 50%，EPS 年增 mid-20s，AI 版稅 FY28 起放量；終端 28 倍。","base":"EPS 年增約 18%：FY27 略低於共識，之後營收低雙位數成長，利潤率往 45% 左右走，不計版稅大幅放量；終端 24 倍，接近目前 FY27 前瞻倍數。","bear":"AI agent 沒有轉成新增授權，中國再受管制，IP 停在個位數成長，EPS 從 FY27 起幾乎不動；倍數壓到 16 倍，對應成長熄火到 10% 以下的情境。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"AI 讓每個設計案需要的工程師變少，授權總數可能縮小；AI 原生新創與 Kimi K3 展示不用商用 EDA 的設計實驗；hyperscaler 可能自建能力。","assumption":"AI agent 會大量呼叫既有工具，用量增加抵銷人數減少，而且 Synopsys 能把增量變現。","consequence":"若授權按人頭縮減，用量計費又談不攏，EDA 成長掉到個位數，EPS 停滯，倍數壓到 16 倍，五年虧損逾三成。","ruling":"部分採納：目前替代證據多為廠商自述或推論，Kimi K3 文章本身也說取代還很遙遠；Q3 硬體驗證創紀錄、EDA 財測上調，與替代說法方向相反。但計價模式未定是實質風險，列入熊市機率 30%。","watch":"FY27 各季 EDA 有機年增是否維持 13% 以上；管理層是否揭露 agent 或用量計費營收。","evidence_refs":["substitute_technology#2","substitute_technology#0","competitive_share_entrants#1","competitive_share_entrants#2"],"fact_refs":["f_rev_consensus_fy2_m"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 占營收 9.35%；Ansys 收購報酬遠低於資金成本；GAAP 營業利益率 11%，Cadence 為 31%；OpenAI 合作採營收分成。","assumption":"營收成長會轉成每股經濟價值，而不是被 SBC、利息與分成吃掉。","consequence":"營收如期成長，但 GAAP 盈餘與每股自由現金流成長落後 non-GAAP EPS，股東實得報酬比帳面成長低。","ruling":"採納一半：FCF 指引由 20 億上調到 26 億，FY27 約 31 億，現金面確實改善；但 SBC 與併購報酬是真實成本，因此資本配置只給中等，估值不判便宜。","watch":"SBC 占營收是否朝 8% 下降；FY27 FCF 是否達約 31 億美元。","evidence_refs":[],"fact_refs":["f_kpi4_sbc","f_peer_snps_operating_margin_pct","f_peer_cdns_operating_margin_pct","f_kpi3_free_cash_flow_ytd_9"]},{"view":"價格已反映太多","evidence":"管理層剛把長期目標從雙位數上調到 mid-teens，現價已隱含 FY27 營收年增 15%、EPS 19 美元；Q2 FY26 財測低於預期後股價跌 9%，2025 年大型晶圓代工客戶問題導致單季失準。","assumption":"一年前才失準的管理層，這次的長期框架可信。","consequence":"FY27 只要一季未達，估值就會從 24 倍往 18–20 倍修正。","ruling":"反駁大半：24 倍對應 23% EPS 成長，PEG 約 1，P/S 在四年低端，價格並未反映版稅與 agent 放量；但財測可信度是唯一致命點，所以設下財測下修即清倉的條件。","watch":"2026 年 12 月 Q4 FY26 財報是否維持 FY27 財測；IP 是否連續季增。","evidence_refs":["capital_markets_pricing#6","customer_concentration_credit#2"],"fact_refs":["f_pe_current","f_ps_percentile","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 454.63","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=454.63","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"核心 EDA 能否由 8.5% 加速到 13% 以上","cause":null,"prior_field":null,"side_a":"管理層（Q3 FY26 法說、2026-09-30 投資人日 CFO）：Q4 與全年 EDA 雙位數，長期 mid-teens、下限 13%。","side_b":"Q2、Q3 FY26 EDA 年增都在 8–8.5%；投資人日分析師指出核心 EDA 近年低至中個位數，CEO 沒有回答單獨的成長數字。","ruling":"程度差異，可以調和：Q3 的 8.5% 是對上去年 16% 的高基期，硬體驗證創紀錄、Q4 財測隱含加速。但 13% 下限尚無一季實績，判斷暫採管理層方向，信心中等。","evidence_level":"管理層指引對比已實現季度數字","settle_metric":"FY27 前兩季 EDA 有機年增","if_then":["若 FY27 前兩季 EDA 有機年增都 ≥13% 且財測未下修，加碼到上限","若 FY27 任一季 EDA 有機年增 <10% 且全年財測未上修，減碼一半","若股價先漲到 FY27 EPS 30 倍以上但 EDA 數字還沒出來，不追"],"evidence_refs":[]},{"axis":"AI 對 EDA 是增量還是替代","cause":null,"prior_field":null,"side_a":"管理層：agent 讓 VCS／Verdi 授權用量增加 5–10 倍，50 個以上客戶合作進行中，OpenAI 出資後訓練 GPT-Synopsys。","side_b":"研究筆記與評論：每案工程師減少會縮小授權池；Kimi K3 不用商用工具完成設計實驗；客戶目前偏好訂閱，不想用量計費。","ruling":"方向尚未定論，目前偏向增量：已實現數字（硬體驗證紀錄、EDA 財測上調）支持增量，替代面只有實驗與推論。但結論在 FY27 揭露 AI 營收以前不可裁決，列為長期風險。","evidence_level":"已實現財報數字對比實驗與推論","settle_metric":"FY27 管理層揭露的 AI 相關營收，以及續約時用量條款的採用情況","if_then":["若 FY27 揭露 AI 營收並維持 EDA 13% 以上，視為增量論點成立，可加碼","若 FY27 積壓訂單年減且 EDA 年增 <10%，視為替代開始，減碼一半"],"evidence_refs":["substitute_technology#0","substitute_technology#2","competitive_share_entrants#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"前瞻 24 倍、PEG 約 1、P/S 在四年低端；連兩季超預期並上調財測，FCF 指引上調 6 億；FY27 EPS 指引 19.08 高於共識 18.67；10 億回購。","side_b":"核心 EDA 加速尚未實現，FY27 是新長期框架的第一年，一年前曾單日跌 36%。","ruling":"可調和：估值不構成阻礙，限制條件是財測可信度。所以以小倉起步，用 FY27 前兩季的 EDA 數字決定加碼或撤出，不等更低價格。","evidence_level":"估值數字對比執行紀錄","settle_metric":"2026 年 12 月 Q4 FY26 財報是否維持 FY27 財測","if_then":["若 Q4 FY26 財報維持或上調 FY27 財測，維持首倉","若 FY27 財測下修，清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY27 各季 EDA 有機年增檢驗長期 13% 下限","type":"假設驗證","maps_to":"H1","metric":"EDA 有機營收年增率（季）","threshold":"連兩季 ≥13% 為通過；任一季 <10% 為警示","action":"通過則加碼到上限；警示則停止加碼","source_freq":"季報新聞稿與法說，每季","date":"2027-02","evidence_refs":[]},{"n":2,"text":"美國對中國 EDA 或 IP 出口再度要求授權，或公司停接中國新單","type":"風險","maps_to":"R1","metric":"官方出口管制公告／公司對中國營收說明","threshold":"再次發出出口授權要求函，或財測因中國下修 ≥2%","action":"減碼一半","source_freq":"事件驅動，公告即查","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#1"]},{"n":3,"text":"Single Thing：FY27 財測被下修","type":"Single Thing","maps_to":"Single Thing","metric":"FY27 營收與 non-GAAP EPS 指引中點","threshold":"營收中點 <109.3 億美元（較 111.5 億低逾 2%），或 EPS 中點 <18.70","action":"清倉","source_freq":"季報，每季","date":"2026-12","evidence_refs":[]},{"n":4,"text":"大型晶圓代工客戶或 IP 再度低於預期","type":"風險","maps_to":"R2","metric":"Design IP 營收年增率（季）","threshold":"連兩季 <5%","action":"減碼一半","source_freq":"季報分部揭露，每季","date":null,"evidence_refs":["customer_concentration_credit#2","capital_markets_pricing#6"]},{"n":5,"text":"AI 替代開始反映在訂單：積壓訂單下滑加上 EDA 放緩","type":"風險","maps_to":"R3","metric":"積壓訂單年增率與 EDA 有機年增率","threshold":"積壓訂單年減，且 EDA 年增 <10%，同一季出現","action":"減碼一半","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","geo_supply_chain#2","substitute_technology#2"]},{"n":6,"text":"證券集體訴訟進展（2025 年 IP 揭露爭議）","type":"風險","maps_to":"R2","metric":"集體認證裁定與和解金額","threshold":"集體認證通過且和解金額逾 5 億美元；若有刑事或 SEC 調查介入","action":"前者減碼一半；後者清倉","source_freq":"法院文件與公司 10-Q，每季","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":7,"text":"股價回落但論點未破時加倉","type":"估值rearm","maps_to":"H1","metric":"股價對 FY27 共識 EPS 倍數","threshold":"股價 ≤400 美元（約 21 倍）且 FY27 財測未下修","action":"分批反買到上限","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":8,"text":"Q4 FY26 財報與 FY27 財測確認後重新檢查","type":"複審日期","maps_to":null,"metric":"FY27 財測、積壓訂單、IP 季增","threshold":"財報公布","action":"重跑判斷","source_freq":"一次性","date":"2026-12","evidence_refs":[]}],"kill_metrics":[{"metric":"EDA 有機營收年增率","bear_threshold":"FY27 起連兩季 <10%","window":"FY27 各季","source":"Synopsys 季報新聞稿與法說","last_status":"warning"},{"metric":"FY27 營收指引中點","bear_threshold":"<109.3 億美元","window":"FY27 各季財報","source":"Synopsys 季報新聞稿","last_status":"ok"},{"metric":"Design IP 營收年增率","bear_threshold":"連兩季 <5%","window":"未來四季","source":"Synopsys 季報分部揭露","last_status":"ok"},{"metric":"non-GAAP 營業利益率（年度）","bear_threshold":"FY27 <42%（指引 44%）","window":"FY27 全年","source":"Synopsys 年度財報與指引","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"FY27 前兩季 EDA 有機年增 ≥13% 且財測未下修；或股價 ≤400 美元且財測未下修","exec_line":"現價可小倉起步，不追高；FY27 前兩季 EDA 數字兌現再加碼，財測下修即清倉。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把「AI 會繞過 EDA」當成現況折價，P/S 落在四年低端；但 Q3 硬體驗證創紀錄、EDA 財測上調、Amazon 與 OpenAI 合作，都顯示 AI 目前在增加工具用量。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"qc48_result":null,"qc48_note":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把「AI 會繞過 EDA」當成現況折價，P/S 落在四年低端；但 Q3 硬體驗證創紀錄、EDA 財測上調、Amazon 與 OpenAI 合作，都顯示 AI 目前在增加工具用量。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=1.12, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"FY27 財測兌現：營收年增約 15%，non-GAAP 營業利益率擴張到約 44%，EDA 有機年增回到 13% 以上。","2y":"FY27 營收 ≥109 億美元、non-GAAP EPS ≥18.5","5y":null,"10y":null,"threshold":"FY27 營收 ≥109 億美元，non-GAAP EPS ≥18.5，EDA 有機年增連兩季 ≥13%","source":"Synopsys 季報新聞稿、法說與財測","drift_rule":"營收或 EPS 連兩季落後財測路徑 ≥5% 視為削弱，連三季 ≥10% 視為反轉"},{"id":"H2","text":"IP 從 FY26 低迷回到高十幾 % 成長，客製化 IP 由授權轉成授權加版稅，2030 年達 10 億美元。","2y":null,"5y":"Design IP 年增 ≥15%（FY27–FY28），FY28 起出現版稅營收","10y":null,"threshold":"Design IP 年增 ≥15%，FY28 年報揭露版稅營收","source":"季報分部揭露、投資人日更新","drift_rule":"連四季年增低於 10% 視為削弱，連六季低於 5% 視為反轉"},{"id":"H3","text":"AI agent 讓每個設計案呼叫更多工具，是增量而不是替代；Synopsys 透過訂閱加用量或成果分成拿到這部分價值。","2y":null,"5y":null,"10y":"EDA 長期年增 ≥13%，AI 相關營收從 FY27 開始揭露且逐年成長","threshold":"EDA 年增維持 ≥13%，積壓訂單不出現年減","source":"季報、年度財報、投資人日","drift_rule":"跨兩個年度 EDA 年增 <10% 視為削弱，跨三個年度視為反轉"}],"R":[{"id":"R1","text":"中國出口管制反覆，中國客戶無法啟動新設計案；中國約占營收 10%。","h_ref":"H1","clock":"⚡","threshold":"再度出現出口授權要求，或財測因中國下修 ≥2%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#1"]},{"id":"R2","text":"大型晶圓代工客戶（媒體推測為 Intel）需求轉弱或 IP 執行失準，重演 2025 年 9 月單日跌 36%；相關證券集體訴訟仍未裁決。","h_ref":"H2","clock":"🔥","threshold":"Design IP 連兩季年增 <5%","evidence_refs":["customer_concentration_credit#2","capital_markets_pricing#6","major_events#0","lawsuit_class_action#0"]},{"id":"R3","text":"AI 原生設計、hyperscaler 自建與每案工程師減少，侵蝕授權池。","h_ref":"H3","clock":"🐢","threshold":"積壓訂單年減且 EDA 年增 <10% 同季出現","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","substitute_technology#0","substitute_technology#2","geo_supply_chain#2"]},{"id":"R4","text":"Cadence 在數位實作搶占份額。","h_ref":"H1","clock":"🐢","threshold":"出現具名大客戶整套流程轉向 Cadence，或 EDA 成長連四季低於 Cadence","evidence_refs":["competitive_share_entrants#5"]}],"single_thing":{"description":"FY27 財測（營收約 111.5 億、non-GAAP EPS 約 19.08）在 FY27 任一季財報被下修，營收中點低於 109.3 億或 EPS 中點低於 18.70。","why_fatal":"現價 24 倍是建立在新長期框架第一年就兌現的前提上；管理層一年前已失準一次，再失準會讓市場改用個位數成長的倍數評價，這是 EPS 與倍數同時下修的最大單一敏感項。","if_happens":"清倉，等新財測至少穩定兩季後再重跑判斷。","how_monitor":"每季財報的 FY27 指引中點、EDA 有機成長、IP 季增與積壓訂單。","probability":"約 25%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":24.35,"peg_fy2":1.05,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":15.14,"FY2027E":18.67,"FY2028E":null},"fy_end_month":10,"eps_basis":"non-GAAP 稀釋 EPS（yfinance 共識）。FY2025 non-GAAP 實際值事實表未涵蓋（只有 GAAP 8.04）；FY2028E 共識事實表未涵蓋（只有兩個年度）。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q4 FY26 財報，確認 FY27 財測","impact":"高","watch":"FY27 營收與 EPS 指引中點是否維持；IP 是否續季增"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q1 FY27 財報，首次檢驗 EDA 13% 下限","impact":"高","watch":"EDA 有機年增、AI 相關營收揭露"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"下一代 ZeBu 硬體驗證系統 Artemis 上市","impact":"中","watch":"硬體驗證營收是否延續紀錄"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"Multiphysics Fusion 由評估轉量產，開始貢獻營收綜效","impact":"中","watch":"營收綜效年化是否朝 FY27 末逾 1 億美元前進"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
