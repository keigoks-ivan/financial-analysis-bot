你是 DD 管線 v20 的判斷層閘（gate），標的 WDC（20261013）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝3747 USD M｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝1655 USD M（利益率 44.2%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝1563 USD M（利益率 41.7%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_kpi5_non_gaap`（q1_business）｜Non-GAAP 毛利率＝54.4 %（GAAP 54.1%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_kpi6_q1_fy2027_non_gaap`（q1_business）｜管理層指引：Q1 FY2027（non-GAAP）＝營收 4.1B ±100M（YoY +42%~49%）；毛利率 55%~56%；營業費用 390~400M；EPS 4.00 ±0.15 —｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[6]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_peer_wdc_gross_margin_pct`（q2_moat）｜WDC 毛利率＝48.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WDC.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_wdc_operating_margin_pct`（q2_moat）｜WDC 營業利益率＝35.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WDC.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_wdc_fcf_margin_pct`（q2_moat）｜WDC FCF 利潤率＝27.18 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WDC.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sndk_gross_margin_pct`（q2_moat）｜SNDK 毛利率＝71.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_000660_ks_gross_margin_pct`（q2_moat）｜000660.KS 毛利率＝76.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.000660.KS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_gross_margin_pct`（q2_moat）｜005930.KS 毛利率＝57.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.12 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝31.83 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝42.87 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-4.37 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（44.83 → 42.87）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝19270.16 USD m｜期間與口徑：2026-10-13／yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝26358.22 USD m｜期間與口徑：2026-10-13／yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝1281 USD M（營運現金流 1,389，淨資本支出 108）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_kpi4_sbc`（q4_capital）｜SBC＝45 USD M（占 GAAP 營業利益 2.9%、占營收 1.2%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-388.0 USD m｜期間與口徑：2026-10-13／yfinance 最新一季：總債務 1191.0、現金 1579.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝374.32 m shares｜期間與口徑：2026-10-13／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.142 %｜期間與口徑：2026-10-13／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-13）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝386.94 USD｜期間與口徑：2026-10-12（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-12（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝19.75 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 20.12，分子＝快照價 397.28｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝14.37 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／2 個年度端點內的分位＝21.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝21.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝11.21 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝67.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝67.3 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝11.18 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝65.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝7.5 x｜期間與口徑：2026-10-13／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝102.21 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 9.95 → 20.12（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.15 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（20.09 → 20.12）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.25 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（31.75 → 31.83）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝10.57 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-12（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝36.4｜期間與口徑：2026-10-12（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-12（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Nikkei 報導 Toshiba 計畫 HDD 產能於 FY2027 前約倍增，容量份額目標由約 10% 拉到 30%；報導後 2026-10-02 WDC 約跌 10%、STX 約跌 15%，Fool 文章並指 Toshiba 可能以低價搶單壓縮 WD 毛利
  - 來源：Motley Fool, Why Western Digital Stock Just Crashed（as_of 2026-10-02）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：HAMR 進度：Seagate 已有兩家大型 hyperscaler 量產採購 Mozaic 4+；WDC 預計 2026 上半年與一家 hyperscaler 開始認證、年底擴至最多三家，量產爬坡 2027 上半年（3dnews 另稱 2026 年底開始 HAMR 生產，時間不一致）
  - 來源：Nasdaq/Zacks, Seagate vs. Western Digital: Which Storage Stock is the Better Buy Now?（as_of 2026-07-29）｜affects：moat_trend、triggers
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：長期替代風險為 flash（SanDisk、Samsung、Micron、Kioxia）；未找到具名的 HDD 新進入者；WD 已把 SSD 業務分出，專注 HDD
  - 來源：Seeking Alpha, Western Digital: Watch For Technological Threats Following Post-Earnings Sell-Off（as_of 2026-08-01）｜affects：decision_inputs.bear、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：WDC FY2026 10-K：三個客戶分別占 FY2026 淨營收 16%、15%、13%；前十大客戶占 73%（FY2025 68%、FY2024 55%），FY2024 無單一客戶達 10%。
  - 來源：SEC WDC Form 10-K FY2026 (period ended 2026-07-03)（as_of 2026-07-03）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：WDC FY2026 10-K：前 10 大客戶占淨營收 73%（FY2025 68%、FY2024 55%）；三家客戶各占 16%、15%、13%（合計 44%）
  - 來源：SEC EDGAR, WESTERN DIGITAL CORP Form 10-K FY2026 (period ended 2026-07-03)（內容經搜尋摘要轉述）（as_of 2026-07-03）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：傳聞 Toshiba 計畫投資約 600 億日圓（約 3.8 億美元）於菲律賓，於 FY2027 前將 HDD 產出約翻倍，市佔由約 10% 朝 30% 提升；Toshiba 未證實；消息使 Seagate 跌約 10%、WDC 跌約 7%。
  - 來源：247WallSt, Seagate Tumbles 10%, Western Digital Drops 7% as Toshiba Moves to Double Hard Disk Output (2026-10-02)（as_of 2026-10-02）｜affects：decision_inputs.bear、thesis.R、triggers
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Section 232 第二階段可能在貿易談判結束後課「顯著」關稅；商務部與 USTR 須於 2026-04-14 前提交談判更新，搜尋未找到更新內容。
  - 來源：Baker McKenzie Global Import Blog, US President Trump issues Section 232 proclamations on semiconductors and critical minerals（as_of 2026-01-27）｜affects：triggers、decision_inputs.bear
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：DatacenterDisk 分析稱硬碟主要在泰國與馬來西亞組裝，零組件來自日本（碟片）、中國（電子件）、菲律賓（組裝）；對泰、馬、韓、中電子產品的關稅加劇 AI 驅動的缺貨，稅率多次宣布、暫停、修改再恢復。
  - 來源：DatacenterDisk, US tariffs hard drive SSD prices 2026（as_of 2026-03-01）｜affects：decision_inputs.bear、moat_trend
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：有節目簡介稱 WDC 製造足跡高度集中於泰國與馬來西亞，並受新「原產地」解釋審視（二手來源，未對照 10-K）
  - 來源：Audible 2026Q2 Western Digital Corporation (WDC) 節目簡介（as_of 2026-07-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：磁頭獨立供應商僅 TDK 一家，同時供應三大 HDD 廠（引 Bloomberg，經供應商部落格轉述）
  - 來源：Fusion Worldwide blog: How China's export controls are disrupting HDD manufacturing and supply（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：中國稀土出口管制：中重稀土出貨仍需逐案核准，暫停期至 2026-11-10（供應商部落格轉述）
  - 來源：Fusion Worldwide blog: Is Hard Disk Drive Supply the Next Major Infrastructure Bottleneck?（as_of 2026-01-01）｜affects：thesis.R、triggers
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：2026-10-02 報導 Toshiba 計劃投資約 600 億日圓、於 FY2027 前將 HDD 產能倍增；當日 Seagate 股價跌約 10%、WDC 跌約 7%，市場擔憂長期壓抑價格。
  - 來源：24/7 Wall St., Seagate Tumbles 10%, Western Digital Drops 7% as Toshiba Moves to Double Hard Disk Output（as_of 2026-10-02）｜affects：decision_inputs.bear、moat_trend、triggers
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：第三方彙整 WDC FY2026 10-K 風險因子：HAMR 轉換為高風險技術轉換，含毛利壓力與可能觸發客戶合約「epidemic failure」條款的瑕疵風險（非 10-K 原文，需對照）
  - 來源：Autobound: What Western Digital's FY2026 10-K says: 11 signals（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：財報後股價下跌 5.36%，儘管數字優於預期，BingX 摘要稱因 2026 年大幅上漲後預期已被墊高。
  - 來源：BingX: Western Digital (WDC) Q4 FY2026 Earnings Overview（as_of 2026-08-06）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261013/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":900.0,"bear_5y_price":137.5,"p_bull_pct":20,"p_bear_pct":32,"upside_5y_pct":29.3,"ev5y_pct":20.0,"irr_base_pct":5.3,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":20.12,"pe":19.23,"basis":"FY2027E 共識 non-GAAP EPS（FY1 前瞻口徑），終端倍數同為前瞻 EPS 口徑"},"eps":{"bull":[21.5,34.5,46.0,54.0,60.0],"base":[19.8,29.0,34.5,36.5,38.5],"bear":[18.5,21.0,15.0,11.0,12.5]},"pe":{"bull":15,"base":13,"bear":11},"p":{"bull":20,"base":48,"bear":32},"yield_pct":{"dividend":0.142,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### WDC_Q3_2026_Earnings_Call_20260430.md
- 2026-04-30｜CFO Kris Sennesael｜guidance：FQ4 營收指引 36.5 億美元±1 億（原話："revenue to be $3.65 billion plus/minus $100 million"）
- 2026-04-30｜CFO Kris Sennesael｜guidance：FQ4 毛利率指引 51%–52%（原話："Gross margin is expected to be in the range of 51% to 52%."）
- 2026-04-30｜CFO Kris Sennesael｜guidance：FQ4 EPS 指引 3.25 美元±0.15（原話："diluted earnings per share to be $3.25 plus/minus $0.15"）
- 2026-04-30｜CFO Kris Sennesael｜margin：FQ3 毛利率 50.5%，年增 1,040 bp、季增 440 bp（原話："Gross margin for the fiscal third quarter expanded to 50.5%."）
- 2026-04-30｜CFO Kris Sennesael｜margin：管理層用增量毛利率（約 70%–75%）說明毛利率可續升，並強調只指引一季（原話："very strong incremental gross margins in the plus 70%"）
- 2026-04-30｜CFO Kris Sennesael｜margin：毛利率超標的三大來源：定價、產品組合、成本；並稱定價並未全數鎖定（原話："not all the pricing going into the quarter is locked"）
- 2026-04-30｜CEO Irving Tan｜margin：每 EB 成本年降約 10%，並稱此為合理的看待框架（原話："we delivered 10% year-on-year"）
- 2026-04-30｜CFO Kris Sennesael｜margin：被問成本降幅是否加速，CFO 稱新產品改善將隨爬坡期分階段進入（原話："There is going to be an adoption curve, right?"）
- 2026-04-30｜CFO Kris Sennesael｜margin：FQ3 營收 33 億美元、年增 45%，營益率 38.6%（原話："revenue was $3.3 billion, up 45% year-over-year"）
- 2026-04-30｜CFO Kris Sennesael｜customer：雲端占營收 89%，年增 48%（原話："Cloud represented 89% of total revenue at $3 billion"）
- 2026-04-30｜CFO Kris Sennesael｜customer：出貨 222 EB，年增 34%（原話："We delivered 222 exabytes to our customers, up 34% year-"）
- 2026-04-30｜CEO Irving Tan｜customer：四大超大規模客戶需求型態大致相近（原話："No, I would say, in general, the profile is quite similar."）
- 2026-04-30｜CEO Irving Tan｜customer：合約年限已延伸至 2028–2029 年（原話："agreements now extending into calendar year '28 and"）
- 2026-04-30｜CEO Irving Tan｜customer：LTA 以 EB 為基礎並附一定價格；基礎量以外的量適用不同定價機制（原話："those LTAs are exabyte based with a degree of pricing"）
- 2026-04-30｜CFO Kris Sennesael｜customer：製造前置期約一年，採購單多提前一年下；一年後進入 LTA 架構、變動性較大（原話："So there is still a little bit more variability"）
- 2026-04-30｜CEO Irving Tan｜customer：UltraSMR 可擴及二線 CSP 與亞洲部分超大規模業者（原話："expand our reach into Tier 2 CSPs"）
- 2026-04-30｜CFO Kris Sennesael｜product：HAMR 目前有 4 家客戶在驗證，進度略超前原計畫（原話："Still a little bit of work to be done in terms of yield"）
- 2026-04-30｜CFO Kris Sennesael｜product：HAMR 預計 2027 年爬坡，良率與可靠度仍有工作待完成（原話："are on track to start volume production in the"）
- 2026-04-30｜CEO Irving Tan｜product：40TB ePMR 與 44TB HAMR 在驗證中；ePMR 2026 下半年量產（原話："are on track to start volume production in the"）
- 2026-04-30｜CEO Irving Tan｜product：預計 FY27 末約 60% 出貨 EB 採 UltraSMR（原話："close to about 60% of all the exabytes that we ship"）
- 2026-04-30｜CEO Irving Tan｜product：HAMR 取得主流比重的時點取決於可靠度與良率，未給目標數字（原話："We don't have a number that we are putting out there"）
- 2026-04-30｜CEO Irving Tan｜product：ePMR 良率維持在 90% 區間，目前良率與品質無變化（原話："they continue to be in the 90% range, right?"）
- 2026-04-30｜CEO Irving Tan｜product：高頻寬硬碟已送 2 家超大規模客戶試用，另有一家本季開始（原話："currently sampling with 2 hyperscale customers"）
- 2026-04-30｜CEO Irving Tan｜guidance：長期資料儲存成長率維持 25% 以上 CAGR 的信心（原話："growth will be greater than 25% CAGR."）
- 2026-04-30｜CEO Irving Tan｜guidance：每 TB 價格年增 9%，並稱 2026 下半年朝高個位數發展（原話："pricing was up 9% year-on-year."）
- 2026-04-30｜CEO Irving Tan｜competition：HDD 與快閃分工不同，目前未見重大架構轉變（原話："But we don't see any -- at this point, any"）
- 2026-04-30｜CEO Irving Tan｜competition：定價理念強調可預測性而非向上押注（原話："So we're not looking for it to be optimistic"）
- 2026-04-30｜CFO Kris Sennesael｜capital_allocation：賣出 580 萬股 SanDisk，債務減少 31 億美元，剩 16 億可轉債（原話："monetizing 5.8"）
- 2026-04-30｜CFO Kris Sennesael｜capital_allocation：FQ3 自由現金流 9.78 億美元，利潤率 29%（原話："free cash flow generation of $978 million for the quarter"）
- 2026-04-30｜CFO Kris Sennesael｜capital_allocation：股利每季由 0.125 提高 20% 至 0.15 美元（原話："free cash flow generation of $978 million"）
- 2026-04-30｜CFO Kris Sennesael｜capital_allocation：FQ3 買回 7.52 億美元（290 萬股），資本計畫啟動以來已回饋 22 億（原話："we have returned $2.2 billion to our shareholders by way"）
- 2026-04-30｜CFO Kris Sennesael｜commitment：資本配置框架不變：超額自由現金流全數回饋股東（原話："we have returned $2.2 billion to our shareholders by way"）
- 2026-04-30｜CFO Kris Sennesael｜commitment：剩餘 170 萬股 SanDisk 預計 2026 曆年底前以股換股、免稅方式處分（原話："We are returning all the excess free cash flow back"）
- 2026-04-30｜CEO Irving Tan｜commitment：目前不增加單位產能，聚焦面密度；視經濟性可能加碼磁頭與媒體投資（原話："at this juncture, we still do not see any"）
- 2026-04-30｜CEO Irving Tan｜commitment：目標在 2027 曆年底前讓所有主要客戶完成 UltraSMR 驗證（原話："We plan to have all of our major"）
- 2026-04-30｜CFO Kris Sennesael｜risk：新品導入有採用曲線，改善分階段進入，並只指引單季（原話："We plan to have all of our major"）

### WDC_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜CFO｜customer：CFO 表示約 90% 業務來自雲端，並稱不再是傳統週期而是長期成長業務（原話："90% of our business is with the cloud"）
- 2026-09-09｜CFO｜customer：客戶要求簽到 2030、2031 年的長約，但尚未簽署（原話："Customers are asking to sign LTAs all the way till 2030 and"）
- 2026-09-09｜CFO｜risk：被問及 AI 基建消化期，CFO 稱目前看不到消化（原話："So currently, we don't see a digestion."）
- 2026-09-09｜CFO｜guidance：CFO 稱未來 5 年 exabyte 需求年複合成長率大於 25%，目前供給無法超過 25%（原話："We can't supply more than 25% right now year-over-year"）
- 2026-09-09｜CFO｜guidance：CFO 稱營收受供給而非需求限制（原話："my revenue is not gated by the demand, my revenue is gated"）
- 2026-09-09｜CFO｜product：CFO 說明 FY26 exabyte 供給成長約 25%，其中一季為 34%，目前約 22%-23%（原話："we grew exabyte on or about 25% year-over-year"）
- 2026-09-09｜CFO｜product：CFO 稱目前處於兩個產品轉換之間，並列出 ePMR 40TB、HAMR 44TB、50TB+ 三個轉換（原話："We are now somewhat in between the next product transitions"）
- 2026-09-09｜CFO｜product：CFO 稱 80% 資料存於 HDD，並認為高效能 HDD 可侵蝕快閃記憶體領域，KV caching 是機會之一（原話："KV caching is one of the opportunities out there."）
- 2026-09-09｜CFO｜margin：CFO 稱每 TB 價格兩季前年增 9%、上季年增 18-19%，仍有上升空間（原話："Last quarter was up 18%, 19% year-over-year."）
- 2026-09-09｜CFO｜customer：CFO 稱客戶多要求提前 52 週下採購單，FY27 大部分已在長約下，FY28 部分、FY29 更少（原話："I think the vast majority of calendar or fiscal year '27 is"）
- 2026-09-09｜CFO｜customer：CFO 說明長約承諾基本量低於客戶需求，上行部分價格不同（原話："we commit to a certain base volume, which is typically less"）
- 2026-09-09｜CFO｜competition：CFO 稱 HDD 僅佔超大規模業者 capex 的 4%-5%，但為關鍵元件（原話："there is no AI without HDDs"）
- 2026-09-09｜CFO｜commitment：CFO 稱 HAMR 正與 4 家大型超大規模客戶認證，計畫 2027 年上半年開始出貨，Q1 少量、Q2 較多（原話："We're currently in qualification with 4 large hyperscale"）
- 2026-09-09｜CFO｜commitment：CFO 重申 HAMR 出貨時程：2027 曆年上半年起，Q3、Q4 持續放量（原話："we intend to start shipping in the first half of calendar"）
- 2026-09-09｜CFO｜competition：被問及競爭對手已推出 HAMR，CFO 稱客戶已熟悉 HAMR，但認證流程保守嚴謹（原話："It definitely helps a little bit that we are not the first"）
- 2026-09-09｜CFO｜product：40TB ePMR 上季少量出貨，本季開始放量（原話："we shipped a little bit last quarter. It will start ramping"）
- 2026-09-09｜CFO｜product：高頻寬硬碟已向 5 家客戶送工程樣品，目標 2 倍效能，將搭配 50TB 以上機種（原話："We are now targeting a 2x improvement on the performance"）
- 2026-09-09｜CFO｜customer：CFO 稱客戶資料中心規劃超過 5 年，因此想鎖定長達 5 年的供給（原話："This is a planned economy."）
- 2026-09-09｜CFO｜margin：CFO 稱毛利率已達 50% 中段、營業利益率達 40% 中段（原話："we are now in the mid-50s with operating margins now in the"）
- 2026-09-09｜CFO｜margin：CFO 稱看不到毛利率天花板（原話："is there a ceiling to the gross margin?"）
- 2026-09-09｜CFO｜margin：CFO 稱長期每 TB 成本年降約 10%，但並非每年每季，目前處於產品轉換間且 DRAM/NAND 等投入成本上升（原話："we will be able to reduce cost per terabyte on or about 10%"）
- 2026-09-09｜CFO｜risk：CFO 提到硬碟內使用的 DRAM 與 NAND 變貴，供應鏈整體有輸入成本上升（原話："we use a little bit of DRAM and we use a little bit of NAND"）
- 2026-09-09｜CFO｜guidance：CFO 稱近期毛利率仍將以相當快的速度提升（原話："gross margin will continue to increase at a pretty good pace"）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱長期 capex 占營收 4%-6%，過去幾年低於此區間，未來幾年可能略高於（原話："the next couple of years, we might be actually slightly"）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱 capex 主要投向讀寫頭、媒體碟片與自動化（原話："most of the CapEx spending goes to head and media as well"）
- 2026-09-09｜CFO｜commitment：CFO 稱自由現金流率目標為 30% 以上，且已有數季達到該水準（原話："Our target free cash flow margin is plus 30%."）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱已完成 SanDisk 持股變現、清理大部分債務，仍在處理可轉債，目前為淨現金（原話："We've completed the monetization of the SanDisk shares."）
- 2026-09-09｜CFO｜commitment：CFO 稱剩餘可動用自由現金流全數回饋股東，以買回為主、股利為輔，並將持續調升股利（原話："The vast majority of the cash goes to the share buyback"）

### WDC_Special_Call_Western_Digital_Corporation_20260930.md
- 2026-09-30｜Marc Tanguay｜customer：產品行銷經理說明 HDD 是雲端資料中心的容量骨幹，且使用者互動資料很可能存在 WD 硬碟上（原話："HDDs are really the capacity backbone of everything digital"）
- 2026-09-30｜Marc Tanguay｜product：以 15 秒影片範例說明雲端 AI 產出 15MB 檔案需產生約 2GB 資料，約 125 倍（原話："So about 125x the actual output of the file size"）
- 2026-09-30｜Marc Tanguay｜product：說明本地 NAS AI 對儲存需求的影響小於 AI 資料中心（原話："You won't need as much storage at the local AI NAS level."）
- 2026-09-30｜Marc Tanguay｜competition：管理層定位本地 NAS AI 與雲端 AI 為並用而非取代（原話："you're not going to use your NAS AI to replace your cloud AI"）
- 2026-09-30｜Marc Tanguay｜product：說明 NAS 容量規劃方式因 AI 而改變，過去以 10–20% 超額配置估算，現在難以預估（原話："you don't know how much storage space you're actually going"）
- 2026-09-30｜Marc Tanguay｜product：WD Red Pro 與資料中心 Ultrastar 同產線、同硬體，僅韌體（NASware）不同（原話："the same drive that ends up being Ultrastar"）
- 2026-09-30｜Marc Tanguay｜product：Red Plus 規格：2–12TB、最多 8 bay、180TB/年工作負載、3 年保固（原話："It scales in capacity from 2 to 12 terabytes."）
- 2026-09-30｜Marc Tanguay｜product：Red Pro 規格：最高 20TB、550TB/年工作負載、250 萬小時 MTBF、7,200 RPM、5 年保固（原話："up to 2.5 million hours mean time between failure"）
- 2026-09-30｜Marc Tanguay｜customer：管理層稱高容量硬碟正被超大規模客戶大量買走，因此 Red Pro 一般可得最高容量為 20TB（原話："are buying all of our higher-capacity drives"）
- 2026-09-30｜Marc Tanguay｜guidance：對 NAS 通路容量供給的前瞻說法：20TB 將是常態可得的最高容量（原話："will be the highest regularly available capacity"）
- 2026-09-30｜Marc Tanguay｜customer：WD 與 UGREEN、QNAP、Synology 等 NAS 廠合作，並於加州 Irvine 設有 NAS 可靠性測試實驗室（原話："We operate what we call our NAS reliability and test lab."）
- 2026-09-30｜Marc Tanguay｜commitment：管理層表示將持續擴大 Red Pro 在 AI NAS 邊緣場景的使用，並維持與 Newegg 合作（原話："as we continue to grow Red Pro, its use"）

### 問答異常語氣（迴避／改口／保留）
- WDC_Q3_2026_Earnings_Call_20260430.md｜問：JPMorgan 問毛利率超標幅度為何大於營收超標、具體是什麼超預期｜答法：回答列出定價、組合、成本三項槓桿，未量化各項貢獻
- WDC_Q3_2026_Earnings_Call_20260430.md｜問：Goldman 問 2027 年底 HAMR 占出貨 EB 比重｜答法：明確表示不給數字，轉談降低客戶轉換風險的雙軌路線
- WDC_Q3_2026_Earnings_Call_20260430.md｜問：Morgan Stanley／JPMorgan 問毛利率指引是否保守、每 EB 成本降幅是否加速｜答法：兩次均重申只指引一季，以增量毛利率與三項槓桿作答，未給成本降幅加速的數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 4 |
| customer_second_source | found | 3 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 5 | 4 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 1 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：WDC Western Digital antitrust OR monopoly investigation 2026；Western Digital regulation OR regulatory scrutiny Computer Hardware 2026；WDC Western Digital DOJ OR FTC OR EU competition 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260906","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤$350（≤11x FY2028E）且 ASP/TB 年增仍 ≥0 → 衛星首倉 1/3；或 CY2027 定價確認持平＋再有 2 家長約延至 2028 → 重跑 DD 升條件式","irr_base_pct":0.9,"ev5y_pct":7,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.23,"ev5y_pct":7,"irr_base_pct":0.9,"max_dd_pct":-65,"bull_5y_price":928,"bear_5y_price":156,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤$350（≤11x FY2028E）且 ASP/TB 年增仍 ≥0 → 衛星首倉 1/3；或 CY2027 定價確認持平＋再有 2 家長約延至 2028 → 重跑 DD 升條件式","price_at_dd":467.46,"archetype":"品質複利成長","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"WDC","date":"2026-10-13","schema":"v15.2","contract":"v19","company_name":"Western Digital Corporation"},"oneliner":"HDD 漲價循環處於高檔：長約鎖住 2027 年，但 Toshiba 擬倍增產能、HAMR 落後 Seagate，2028 年後每 TB 價格方向成爭點；FY2028E 12 倍本益比建立在高峰毛利率上，Base 五年年化約 5%，不追，等 320 美元或長約鎖價證據。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261013/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261013/scenario.json","answers":{"q1_business":{"verdict":"賺超大規模雲端業者的容量儲存錢：雲端占營收 89%，多年長約鎖基礎量、基礎量以外另議價；錢卡在「每 TB 價格上漲＋每 TB 成本年降約 10%」的剪刀差，產業處過熱初段。","reasoning":"Q4 FY26 營收 37.47 億美元（年增 44%），non-GAAP 毛利率 54.4%、營益率 44.2%，GAAP 營益率 41.7%；Q1 FY27 指引營收 41 億美元±1 億、毛利率 55–56%、EPS 4.00±0.15。分部：雲端約 33 億（89%，年增 43%）、Client 2.25 億（6%，年增 61%）、Consumer 1.87 億（5%，年增 38%），CFO 稱三段毛利率都在 50% 出頭，獲利不靠組合撐。量價：Q4 出貨 231 EB、年增 22%（Q3 為 34%），每 TB 混合價格年增由高個位數升至高十幾%，每 TB 成本年降約 8%。單點依賴：前十大客戶占 FY2026 營收 73%（FY2024 為 55%），三家各占 16%／15%／13%，集中度三年升 18pp，屬集中度風險而非護城河證據。供需持久性：週期性將反轉，時點約 CY2028——需求真實，但供給可逆性中等，Toshiba 擴產與雙寡頭 HAMR 面密度提升會在 2027–28 年加快 EB 供給。產業態勢三軸裁決為雙向拉鋸：競爭面惡化（Toshiba 擬擴產、Seagate HAMR 領先），結構面轉好（2026 產能售罄、長約延至 CY2029、HDD 存放超大規模資料約 80%），其他變數為關稅與原產地認定、客戶集中度上升。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_non_gaap","f_kpi6_q1_fy2027_non_gaap"],"verdict_values":{"revenue_quality":"雲端占 89% 且多在長約下，能見度高；但前十大客戶占 73%、三家合計 44%，集中度三年上升 18pp，買方議價風險同步上升。","unit_econ_note":"Q4 FY26：每 TB 混合價格年增高十幾%、每 TB 成本年降約 8%（長期目標約 10%）；年增量毛利率 84–85%，Q1 FY27 指引隱含約 80%。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營益率由 FY2023 −6.4%（含快閃業務）升至 FY2026 35.6%，振幅來自每 TB 價格隨供需擺動；第三名廠商以擴產回應；長約降低但未消除循環性。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉（約 CY2028）：TrendForce 稱雙寡頭轉 HAMR 後供需逐步趨近平衡、Toshiba 擬倍增產能；反方為 Morgan Stanley 稱加計 Toshiba 至 2028 仍短缺、CFO 稱營收受供給而非需求限制。產能售罄、價格年增加速、競爭者宣布擴產三者並存，屬過熱初段。","bargaining":{"up":"磁頭獨立供應商僅 TDK 一家（二手轉述），WDC 以自製磁頭與碟片為主，資本支出主要投向磁頭、媒體與自動化；CFO 2026-09-09 稱 DRAM 與 NAND 等投入成本上升。","down":"前十大客戶占 73%，三家各占 16%／15%／13%；但 HDD 只占超大規模業者資本支出 4–5%，客戶主動要求長約鎖量，目前賣方議價力偏強。","geo":"組裝集中泰國與馬來西亞（二手來源，未對照年報），面對關稅與原產地認定風險；中國中重稀土逐案核准，暫停期至 2026-11-10。"},"profit_pool_dir":"儲存與記憶體利潤池整體擴大：WDC 毛利率 48.9%（TTM），快閃與記憶體同業 SanDisk 71.5%、SK hynix 76.3%、Samsung 57.5%；WDC 營益率三年由 −6.4% 升至 35.6%。","tam_table":{"expanded":false,"reason":"HDD 為成熟寡占品類，論點不在滲透率或份額擴張而在每 TB 價格；事實表未涵蓋 TAM／SAM 金額與五年前利潤池占比，需求以 EB 年增衡量（管理層稱五年 >25%）。"}}}},"q2_moat":{"verdict":"護城河 B、方向穩定：三家寡占與長約撐住定價力，但 HAMR 落後 Seagate、Toshiba 擬擴產，執行力軸偏弱，兩軸相抵判穩定。","reasoning":"機制：HDD 只剩三家，面密度技術門檻高，超大規模客戶每代平台需一年以上認證並以多年長約鎖量（CFO：客戶提前 52 週下單，FY2027 絕大部分已在長約下）。可證方向：份額 42–48%（2025 Q1 Coughlin 42%、TrendForce 2026 估 48%，口徑不同），未見下滑序列；定價力實證為每 TB 價格年增由 9% 升至高十幾%。執行力 7：40TB ePMR 如期放量、Q4 營收達指引上緣、毛利率與 EPS 超出上緣，但 HAMR 量產比 Seagate 晚約一年，分析師指出 Seagate 毛利率指引高約 200bp。定價力 7：漲價主要來自供給緊張，非轉換成本或品牌，Toshiba 擴產可直接削弱。同業對照缺 Seagate 與 Toshiba，表內快閃與記憶體廠利潤率較高屬不同循環，不作護城河差距解讀。當期 ROIC：投入資本事實表未涵蓋，依營益率 35.6% 與資本支出低於營收 4–6% 推論屬高利益率×高周轉，非實算。","fact_refs":["f_peer_wdc_gross_margin_pct","f_peer_wdc_operating_margin_pct","f_peer_wdc_fcf_margin_pct","f_peer_sndk_gross_margin_pct","f_peer_000660_ks_gross_margin_pct","f_peer_005930_ks_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"三家寡占＋面密度技術門檻＋一年以上客戶認證週期＋多年長約鎖量；定價力目前來自供給緊張，非品牌或轉換成本。","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力偏縮：HAMR 量產落後 Seagate 約一年，TrendForce 預估 Seagate 2028 年成最大供應商；定價力擴大：每 TB 價格年增由高個位數升至高十幾%，長約延至 CY2029。份額 42–48% 未見下滑序列，兩軸方向相反，合併判穩定。若 2027 上半年 HAMR 未出貨或份額序列連兩季下滑，改判向下。","competitor_notes":[{"name":"Seagate（STX）","strategy_note":"HAMR 領先約一年、已在兩家大型超大規模客戶量產，毛利率指引高於 WDC 約 200bp，是最直接的份額威脅；不在事實表同業對照內。"},{"name":"Toshiba","strategy_note":"第三名、份額約 10–17%，傳出約 600 億日圓投資菲律賓使產能倍增，屬供給回應訊號；公司未證實。"},{"name":"SanDisk（SNDK）","strategy_note":"2025 年自 WDC 分拆的快閃廠，TTM 毛利率 71.5%，代表快閃替代與記憶體循環高點，非 HDD 直接對手。"},{"name":"SK hynix（000660.KS）","strategy_note":"記憶體循環高點（毛利率 76.3%），與 HDD 無直接份額競爭，只作利潤池對照。"},{"name":"Samsung（005930.KS）","strategy_note":"快閃與記憶體綜合廠，毛利率 57.5%；QLC 企業級 SSD 為長期替代來源。"},{"name":"Pure Storage（PSTG）","strategy_note":"全快閃陣列推手，事實表無財務資料；WDC 稱企業 OEM 正由全快閃轉回混合式。"}],"peer_na_reason":"事實表同業對照缺 Seagate、Toshiba 兩家直接 HDD 競爭者，表內為快閃與記憶體廠，利潤率差距不可解讀為護城河差距；Pure Storage 無財務資料。","threats":[{"level":"🟡","text":"Toshiba 擬於其 FY2027 前倍增 HDD 產能、容量份額目標由約 10% 拉到 30%，可能以低價搶單；Toshiba 未證實，Citi 認為受碟片與磁頭外購限制。","p":30,"evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"]},{"level":"🟡","text":"Seagate HAMR 已量產、WDC 44TB HAMR 要到 2027 上半年；HAMR 轉換另有良率、可靠度與客戶合約大規模瑕疵條款風險。","p":40,"evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"level":"🟡","text":"快閃長期替代：目前每 TB 價差 5–10 倍，雲端冷資料層未見架構替代；若價差縮到 3 倍內升級為架構替代。","p":15,"evidence_refs":["competitive_share_entrants#4"]},{"level":"🟡","text":"互補零件收斂：磁頭獨立供應只剩 TDK，中國稀土逐案核准；公司稱已建立替代來源。","p":15,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推論，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是超大規模業者，冷資料保存是需要而非想要；HDD 存放超大規模資料約 80%，每 TB 價格比 SSD 低 5–10 倍（公司說法經轉述）。代理讀數：管理層稱 EB 需求五年 >25%，CFO 稱目前看不到消化期。付款時點受資本支出節奏影響，但延後購買的代價是資料無處存放，延後空間有限。"},{"item":"決策層級","level":"🟡","text":"替代決策發生在每家客戶每代平台的認證，不在商品層：認證一年以上、長約多年，但客戶同時認證兩到三家，Seagate HAMR 已先在兩家大型客戶量產，換供應商的成本只是一個認證週期。代理讀數：長約只承諾低於需求的基礎量，上行量另議價。"},{"item":"價值鏈分配","level":"🟡","text":"HDD 只占超大規模業者資本支出 4–5%（CFO 2026-09-09），付款方對價格不敏感，有利 WDC 分得較多；但買方高度集中（前十大 73%），磁頭的獨立供應收斂到 TDK 一家，價值可能向上游與大客戶移轉。快閃與記憶體同業毛利率 57–76%，整條儲存價值鏈的利潤目前在記憶體端較厚。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的資本財，沒有消費者必需品的漲價政治壓力，也不依賴監管授權；政策風險在關稅與原產地認定（Section 232 第二階段未定），屬成本面而非社會容忍度上限。"}],"roiic":"淨值無法實算：投入資本、折舊攤銷與營運資金變動事實表未涵蓋。以下是可複算的界線。FY2025→FY2026 GAAP 營業利益由約 21.3 億增至約 46.0 億美元，增量約 24.7 億。FY2026 營收約 129 億，由營業利益 46.0 億 ÷ 35.6% 與自由現金流 35.11 億 ÷ 27.2% 兩路回推一致。FY2026 全年資本支出事實表未涵蓋，以長期區間 4–6% 代入，約 5.2–7.7 億；即使全數視為新增投入資本，增量報酬仍約 320–480%。營運資金增加未計入，實際值較低。增量主要來自漲價而非新投入資本，不作承重數字。","reinvest_rate":"毛再投資率約 7–17%（可複算，非淨值）。長期口徑：資本支出占營收 4–6%（CFO）÷ FY2026 GAAP 營益率 35.6%，約 11–17%。Q4 FY26 實際：資本支出 1.08 億美元 ÷ GAAP 營業利益約 15.6 億（37.47 億 × 41.7%），約 7%；當季資本支出只占營收約 2.9%，低於長期區間。分母用稅前營業利益，稅率事實表未涵蓋，改用稅後會讓比率上升；分子未扣折舊攤銷與營運資金變動，兩者事實表未涵蓋，所以淨再投資率會低於此值。CFO 稱未來兩年資本支出可能略高於 4–6%。管理層承諾超額自由現金流全數回饋，與再投資需求低一致。","endo_ceiling":25,"formula_note":"增量 ROIC × 再投資率在本例失真。照公式代入，兩者相乘等於營業利益增量 ÷ 本期營業利益（24.7 億 ÷ 46.0 億），約 54%，資本支出假設在乘積中互相抵銷。這只是把 FY2026 漲價帶來的獲利跳升重述一次，不代表可持續的內生成長。因此改用實體上界：EB 供給年增上限約 25%（CFO 2026-09-09：目前供給無法超過 25%）× 長期每 TB 價格持平，得出營收與 EPS 內生上界約 25%。公司選擇不擴單位產能、以面密度換成長，是用短期成長換持續期。"}}}},"q3_growth":{"verdict":"五年後成長空間中等：EB 需求隨資料量複利、管理層稱 >25%，但 HDD 已占超大規模資料約 80%，難再搶份額；第二曲線高頻寬硬碟仍在送樣，且目標由「吞吐量最高 8 倍」改為「效能提升 2 倍」。","reasoning":"成長組成：量（EB 年增 22–25%，供給受限）＋價（每 TB 價格年增高十幾%）＋淨回購，無併購。三年共識 EPS：FY2027E 20.12、FY2028E 31.83、FY2029E 42.87（Koyfin 快照，EPS 家數未揭露；營收共識 FY1 23 位、FY2 22 位分析師），以 non-GAAP FY2026A 10.22 為基期，年複合約 61%；GAAP 基期 26.92 含 SanDisk 持股利益，不可用。內生上界約 25%（見護城河段），缺口約 36pp 可歸因毛利率擴張（每 TB 價格漲、成本降）與淨回購，屬可歸因但高度依賴漲價續航。營運槓桿為正：Q4 營業利益年增 126%、營收年增 44%。FY2029 共識在最近兩份快照之間下修 4.37%，是第一個向下修正。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy3_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量（EB 年增約 22–25%）＋價（每 TB 價格年增高十幾%）＋淨回購；無併購","runway_years":"不適用滲透率口徑：需求隨資料量複利（管理層稱五年 EB 年複合 >25%），HDD 已占超大規模資料約 80%，成長年限取決於價格循環而非滲透率","runway_post_y5":"🟡","endo_ceiling_basis":"EB 供給年增上限約 25% × 長期每 TB 價格持平 → 內生上界約 25%；共識三年 EPS 年複合約 61%，缺口約 36pp 歸因毛利率擴張（每 TB 價格漲、成本年降約 8–10%）與淨回購，無併購。","segments":[{"item":"雲端（Cloud）","value":"Q4 FY26 約 33 億美元，占 89%，年增 43%；FY2026 全年年增 38%"},{"item":"Client","value":"Q4 FY26 2.25 億美元，占 6%，年增 61%，主因漲價"},{"item":"Consumer","value":"Q4 FY26 1.87 億美元，占 5%，年增 38%，主因漲價"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q4 毛利率年增 1,310bp"},{"signal":"核心份額近 12 個月縮減","lit":false,"note":"42–48%，無下滑序列；TrendForce 預估 2028 年被 Seagate 超越屬預測"},{"signal":"提價後銷量下滑","lit":false,"note":"漲價同時 EB 年增 22%"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"共識三年 EPS 年複合約 61%，FY2026→FY2028 營收年複合約 43%，差逾 5pp"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":true,"note":"GAAP 口徑 FY2025 0.69、FY2026 0.38，但 GAAP 淨利含 SanDisk 持股利益，non-GAAP 口徑約 0.9，低權重"},{"signal":"SBC／營收 >5% 且上升","lit":false,"note":"1.2%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"快閃替代屬長期，每 TB 價差 5–10 倍"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"},{"signal":"維護性資本支出占 FCF >60%","lit":false,"note":"Q4 資本支出 1.08 億美元對 FCF 12.81 億"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"不擴單位產能但營收年增 36%"}]}}},"q4_capital":{"verdict":"資本配置紀律好但時點偏高：淨現金、SBC 低、自由現金流全數回饋；回購集中在股價上漲段，若此刻在循環高檔，買回的價值打折。","reasoning":"FY2026 自由現金流 35.11 億美元（利潤率 27.2%），Q4 單季 12.81 億（營運現金流 13.89 億、資本支出 1.08 億）；FY2026 回饋股東 31 億美元。FCF 對 GAAP 淨利僅 0.38，因 GAAP 淨利含 SanDisk 持股處分與評價利益（Q3 法說賣出 580 萬股抵減債務 31 億美元）；以 non-GAAP EPS 10.22 粗估淨利約 38–40 億，轉換率約 0.9。SBC 單季 4,500 萬美元（營收 1.2%）。Q4 末債務 11 億、現金 16 億，淨現金約 4–5 億；股利每季 0.15 美元；CFO 稱長期資本支出占營收 4–6%，未來兩年可能略高，投向磁頭、媒體與自動化。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近三年無收購；Kioxia 合併僅為來源日期不一致的報導，未見協議"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"Q3 FY26 買回 290 萬股、7.52 億美元（均價約 259 美元）；Q4 公開市場約 230 萬股、均價約 292 美元（10 億美元內含 3.28 億可轉債溢價）。以 FY2026 non-GAAP EPS 回算收益率約 3.5–3.9%，以現行 FY2027 共識回算約 7–8%；10 年期公債殖利率事實表未涵蓋，無法判斷是否過關"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 單季 4,500 萬美元（營收 1.2%、GAAP 營業利益 2.9%），年化約 1.8 億美元、約市值 0.1%；同期回購與 SanDisk 換股回收 480 萬股，流通股淨減少"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自量價，非併購；資本回饋以回購為主、股利為輔，管理層承諾超額自由現金流全數回饋（Q3 法說、2026-09-09 Citi 會議 CFO），細節見計分卡"}}}},"q5_valuation":{"verdict":"現價要求 FY2028–29 共識 EPS（31.83／42.87）大致兌現，且市場在高峰毛利率上仍給 12 倍以上；這等於假設每 TB 價格在 Toshiba 擴產與雙寡頭 HAMR 放量下續漲到 2028 年，我只信到 2027 年。","reasoning":"現價 386.94 美元：FY2027E 19.2 倍、FY2028E 12.2 倍、FY2029E 9.0 倍；前瞻 EV／營收 7.5 倍。trailing 本益比 14.4 倍用 GAAP EPS 26.92，含 SanDisk 持股利益，失真不用；P／S 11.2 倍在 4 個年度端點中位於 67%，非五年分位。PEG 以 non-GAAP 三年年複合約 61% 計約 0.31，但循環股在高峰 PEG 偏低屬常態，不作便宜證據。Base（FY2031E EPS 38.5 × 13 倍＝約 500 美元）五年年化約 5%，低於 8% 門檻。12 個月：FY2028E Base EPS 29.0 × 13 倍＝377 美元（−2.6%）；三年：FY2030E 36.5 × 13 倍＝475 美元（+22.6%）。賣方平均目標價 483 美元（20 位）比本裁決樂觀，差異在賣方把漲價外推到 FY2029（共識粗估隱含毛利率約 60% 以上），本裁決認為供給回應會先到。另：FY1 共識近三月 +102% 是財年滾動造成（7 月快照的 FY1 是 FY2026、10 月是 FY2027），同口徑真實修正為 FY1 +0.15%、FY2 +0.25%、FY3 −4.37%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2027E／FY2028E 共識 non-GAAP EPS）；循環股優先尺為股價淨值比，但淨值事實表未涵蓋，改以 FY2028E 本益比交叉","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，缺同業前瞻倍數；直接競爭者 Seagate 與 Toshiba 不在表內，無法建立同級倍數錨"},"fwd_pe":19.23,"peg":0.31,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"表面便宜（FY2028E 12.2 倍），但分母在高峰毛利率上；Base 五年年化約 5%、上下行比約 1.3，不便宜也不貴，判黃。股價 ≤320 美元時 Base 年化約 9%、上下行比約 2，可轉綠。五年分位：事實表只有年度端點分位，不外推。","upside_short_pct":-2.6,"upside_mid_pct":22.6,"denominator_disputed":true,"denominator_note":"便宜論證全落在 FY2028–29 EPS，而這兩年的毛利率假設（約 58–60% 以上）正是循環高峰爭點；trailing 分母又含 SanDisk 一次性利益。分母有爭議，低本益比不構成便宜論證。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是 2028 年後每 TB 價格方向：若長約延到 2031 並含漲價，循環論錯、Bull 成立；若 Toshiba 擴產與 HAMR 放量讓供給追上，現價的 12 倍 FY2028E 就是高峰本益比。","reasoning":"反證三視角與陷阱判斷依據見反證紀錄。衰退訊號亮 2 項：EPS 成長遠高於營收成長；GAAP 自由現金流對淨利連兩年 <0.75，但受 SanDisk 持股利益扭曲，低權重。成長熄火壓力測試以 Base FY2029E 34.5 為起點，之後年增 15%／10%／5% 配 14／12／10 倍，FY2031E 價位約 639／501／380 美元，三案兩案守住現價。最大回撤依據見情境假設。","fact_refs":["f_consensus_rev_fy3_pct","f_week26_return_pct","f_rsi14","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰獲利陷阱：本益比低是因為分母在週期高點"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":20.12,"pe":19.23,"basis":"FY2027E 共識 non-GAAP EPS（FY1 前瞻口徑），終端倍數同為前瞻 EPS 口徑"},"eps":{"bull":[21.5,34.5,46.0,54.0,60.0],"base":[19.8,29.0,34.5,36.5,38.5],"bear":[18.5,21.0,15.0,11.0,12.5]},"pe":{"bull":15,"base":13,"bear":11},"p":{"bull":20,"base":48,"bear":32},"yield_pct":{"dividend":0.15,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":6},"max_dd":{"lo":-72,"hi":-55,"basis":"Bear 終值約 138 美元（FY2031E EPS 12.5 × 11 倍，−64%），路徑上 FY2030 EPS 11 美元時低點約 121 美元（−69%）；上一輪下行 FY2023 營益率 −6.4%、EPS −5.37，顯示獲利可由高峰轉負；近五週股價自 467 跌到 387（−17%），2026-10-02 單日因 Toshiba 擴產消息跌 7–10%。取 −55% 至 −72%。","trigger_time":null},"basis":{"bull":"長約延伸至 CY2031 並含漲價機制、HAMR 2027 上半年如期放量、Toshiba 擴產受零件外購限制；每 TB 價格至 FY2029 年增仍達雙位數，毛利率升向 65%；終端 15 倍介於現價 FY2027E 19.2 倍與 FY2028E 12.2 倍之間，代表市場部分承認循環性降低。","base":"CY2027 價格大致鎖定，CY2028 起漲幅收斂至持平，FY2030 後每 TB 價格隨成本年降約 8–10%，毛利率持平於 58–60%；FY2029 EPS 低於共識約 20%；終端 13 倍對照現價 FY2028E 共識 12.2 倍（同業前瞻本益比事實表未涵蓋）；EPS 路徑已含回購減股，淨回購殖利率填 0 避免重複計入。","bear":"CY2028 Toshiba 倍增產能＋雙寡頭 HAMR 提高 EB 供給，疊加超大規模業者消化期，每 TB 價格年降幅超過成本降幅，毛利率回到約 40%，FY2030 EPS 落到 11 美元；終端 11 倍取成長熄火至 10% 情境的前瞻倍數，低於現價 FY2028E 12.2 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Toshiba 擬於其 FY2027 前倍增產能、份額目標 30%；TrendForce 稱雙寡頭轉 HAMR 後供需趨近平衡；WDC 營益率 FY2023 曾為 −6.4%。","assumption":"長約只鎖基礎量、上行量另議價，CY2028 後的價格機制仍可重談。","consequence":"五年後虧 50% 最可能的故事：CY2028 起 EB 供給增速超過 25%、超大規模業者進入消化期，每 TB 價格年降幅超過成本降幅，毛利率回到約 40%，EPS 自 30 美元以上落到 11–13 美元，市場給 11 倍，股價約 138 美元（−64%）。與唯一致命點是同一變數（每 TB 價格方向）。","ruling":"部分採納：長約延至 CY2027–29 讓崩價最早落在 CY2028 之後，Bear 機率 32% 而非過半。","watch":"每季每 TB 混合價格年增；Toshiba 擴產公告；Seagate 2027–28 定價說法","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"],"fact_refs":["f_consensus_rev_fy3_pct"]},{"view":"論點成功但股東經濟變差","evidence":"Seagate HAMR 已在兩家大型超大規模客戶量產，WDC 要到 2027 上半年；HAMR 轉換有瑕疵與合約賠償條款風險；磁頭獨立供應只剩 TDK；CFO 稱未來兩年資本支出可能略高於營收 4–6%，DRAM／NAND 投入成本上升。","assumption":"AI 資料需求年增 25% 以上成立，但 WDC 分到的份額與每 TB 利潤不一定跟著。","consequence":"產業成長、WDC 份額讓給 Seagate、成本降幅停在 5–8%，毛利率停在 50% 出頭；同時回購在循環高檔大量買入，每股價值成長低於產業。","ruling":"採納為中度風險：反映在 Base 毛利率持平 58–60%（低於共識隱含水準）與 H3 份額門檻。","watch":"HAMR 首批出貨時點；份額序列；每 TB 成本年降幅；回購均價對照股價","evidence_refs":["competitive_share_entrants#2","substitute_technology#2","geo_supply_chain#1"],"fact_refs":["f_kpi5_non_gaap"]},{"view":"價格已反映太多","evidence":"Q4 FY26 營收與 EPS 優於預期，財報後股價仍跌 5.36%；共識 FY2029 EPS 42.87 粗估隱含毛利率約 60% 以上；前瞻 EV／營收 7.5 倍，P／S 11.2 倍在 4 個年度端點中位於 67%。","assumption":"市場用高峰獲利給倍數，而循環股的高峰本益比通常被壓低。","consequence":"即使每 TB 價格續漲到 FY2028，若市場提前定價供給回應，倍數由 FY2028E 12 倍壓到 9–10 倍，股價難漲。","ruling":"採納：這是不追的主因，Base 終端 13 倍、五年年化約 5%。","watch":"FY2028／FY2029 共識修正方向；財報後股價反應","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_ev_s_fwd","f_ps_percentile","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 467.46 → 本次 386.94（-17.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=467.46","side_b":"本次 price_at_dd=386.94","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 467.46 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 467.46 美元：Bull 價 928、Bear 價 156，五年期望值 +7.0%，基準年化 0.9%，不對稱比 1.23","side_b":"本次情境、股價仍用 467.46 美元：Bull 價 900、Bear 價 137.5，五年期望值 −0.7%，基準年化 1.4%，不對稱比 0.82","ruling":"先換情境、股價不動：五年期望值少 7.7 個百分點，基準年化多 0.5 個百分點。不對稱比由 1.23 變為 0.82。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 467.46 美元：五年期望值 −0.7%，基準年化 1.4%，不對稱比 0.82","side_b":"本次情境、股價 386.94 美元：五年期望值 +20.0%，基準年化 5.3%，不對稱比 1.29","ruling":"再換股價、情境不動：起點價下跌 17.2%，五年期望值多 20.7 個百分點，基準年化多 3.9 個百分點，不對稱比由 0.82 升到 1.29。合計五年期望值比前份多 13.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2028 年後供需方向（不可調和）","cause":null,"prior_field":null,"side_a":"結構性：CFO 稱營收受供給而非需求限制、EB 需求五年 >25%，客戶要求簽到 2030–31 年長約；Morgan Stanley 認為加計 Toshiba 新產能至 2028 仍供不應求，Citi 認為 Toshiba 受碟片與磁頭外購限制。","side_b":"週期性：Toshiba 擬於其 FY2027 前倍增產能、份額目標 30%；TrendForce 稱雙寡頭轉 HAMR 後供需逐步趨近平衡；Seagate 執行長稱 2027–28 新產能上線後價格「持平至小幅上漲」；FY2029 共識最近一次下修 4.37%。","ruling":"⚖ 選中間偏週期側：CY2027 價格大致鎖定（CFO：FY2027 絕大部分在長約下），CY2028 起每 TB 漲幅收斂至持平，Base EPS 低於 FY2029 共識約 20%。依據：長約只承諾低於需求的基礎量、上行量另議價（Q4 法說執行長），CY2029 後長約的價格機制管理層仍在談；擴產消息後遠年共識已先下修。利空出現不到一季，只部分進入賣方模型，凍結加碼直到第一個確認數據點。","evidence_level":"雙方皆為管理層說法或二手轉述，無 CY2028 實際價格資料；不可裁決至 2027 年中長約價格揭露","settle_metric":"每季法說揭露的每 TB 混合價格年增；CY2029–31 長約價格機制；Toshiba 菲律賓產能量產時程","if_then":["若連兩季每 TB 價格年增 ≥15% 且 CY2029 後長約揭露含漲價機制 → Bear 機率降到 25%，股價 ≤380 美元時首倉 1/3","若每 TB 價格年增降到個位數且 Toshiba 正式公告擴產時程 → 不建倉，Bear 機率上調至 40%","價格先走證據未到：股價續漲但價格年增未加速 → 不追；股價跌破 320 美元而價格年增仍 ≥0 → 分批反買首倉 1/3"],"evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"]},{"axis":"不追的反面：現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價已自前份 467.46 跌 17% 至 386.94，對 FY2028E 共識僅 12.2 倍、FY2029E 9.0 倍；Q1 FY27 指引營收年增 42–49%、毛利率 55–56%，年增量毛利率約 80%；淨現金、自由現金流全數回饋；RSI 36.4 接近超賣；賣方平均目標價 483 美元。","side_b":"低本益比建立在高峰毛利率上；Base 五年年化約 5%、上下行比約 1.3；賣方目標價以 500–1,050 美元計約 2.1 倍，含疑似過時的 250 美元則達 4.2 倍，共識本身不穩；已跌 17% 不是安全邊際。","ruling":"可調和（程度差異）：基本面動能真實，但價格只反映到 Base 與 Bull 之間，選不追。","evidence_level":"指引與法說為一手，賣方目標價為彙整","settle_metric":"Q1 FY27 實際毛利率與每 TB 價格年增","if_then":["若 Q1 FY27 毛利率 ≥56% 且每 TB 價格年增 ≥20% → 重算 Base，股價 ≤360 美元時首倉 1/3","若毛利率低於 55% 指引下緣 → 不建倉"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"兌現項：Q3 法說（2026-04-30，CFO）指引 FQ4 營收 36.5 億±1 億、毛利率 51–52%、EPS 3.25±0.15。實際營收 37.47 億，約在上緣 37.5 億；毛利率 54.4%、EPS 3.56，皆超過上緣。執行長在 Q3 說價格年增朝高個位數，Q4 實際為高十幾%。","side_b":"落差項：高頻寬硬碟目標在 Q4 法說（2026-08-05，執行長）為吞吐量最高 8 倍，Citi 會議（2026-09-09，CFO）改為效能提升 2 倍，口徑可能不同但目標明顯降低；EB 出貨年增由 Q3 的 34% 降到 Q4 的 22%；每 TB 成本年降約 8%，低於長期約 10%，CFO 稱處於產品轉換之間且 DRAM／NAND 投入成本上升；Q3 法說三次迴避（毛利率超標來源未量化、2027 年底 HAMR 占比拒給數字、成本降幅加速未給數字）。","ruling":"短期財測可信，長期第二曲線與成本曲線說法打折：五年後成長空間不升寬，成本年降 10% 在 HAMR 放量前不當作基準。","evidence_level":"一手逐字稿","settle_metric":"FY2027 每 TB 成本年降幅；高頻寬硬碟首張量產訂單","if_then":["若 FY2027 連兩季每 TB 成本年降 <5% → Base 毛利率下修 2pp、不建倉","若高頻寬硬碟 2027 年內取得量產訂單 → Bull 機率上調至 25%"],"evidence_refs":[]},{"axis":"共識修正口徑","cause":null,"prior_field":null,"side_a":"FY1 共識近三月 +102%（9.95→20.12），表面看是大幅上修。","side_b":"7 月快照的 FY1 為尚未公布的 FY2026（實際 non-GAAP 10.22，接近 9.95），10 月已滾動成 FY2027；同口徑真實修正為 FY1 +0.15%、FY2 +0.25%、FY3 −4.37%。","ruling":"採後者：+102% 是財年滾動，不作上修動能證據；遠年共識實為下修。","evidence_level":"快照數值與法說實際值對照，屬推論","settle_metric":"下次快照 FY1／FY2／FY3 同口徑修正","if_then":["若下次快照 FY2／FY3 再下修 ≥5% → Bear 機率上調至 35%、不建倉"],"evidence_refs":[]},{"axis":"前份漂移：裁決、角色、綜合評級、估值","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-09-06，股價 467.46）：觀望、追蹤，綜合評級 B，估值黃（FY2028E 約 14.7 倍）。","side_b":"本次股價 386.94（−17%），FY2028E 降至 12.2 倍；但便宜來自高峰分母，估值結論仍黃、綜合評級維持 B；裁決與角色由程式依本次輸入重算。前份重啟條件（≤350 美元）未觸發。","ruling":"價格下跌未改變判斷。","evidence_level":"事實表價格與共識","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：護城河方向、陷阱、五年後成長空間、循環位置","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5","cycle_position"],"side_a":"前份：護城河方向穩定、陷阱風險黃、五年後成長空間中等、晚循環。","side_b":"本次新增 Toshiba 擬倍增產能報導（2026-10-02）、TrendForce 預估 Seagate 2028 年成最大供應商（2026-10-07）、CFO 把高頻寬硬碟目標由 8 倍改為 2 倍（2026-09-09）；結論不變，但晚循環證據更充分，執行力軸由穩定轉偏弱。","ruling":"四欄維持原值；若 HAMR 2027 上半年未出貨，護城河方向改判向下。","evidence_level":"二手報導＋一手逐字稿","settle_metric":"HAMR 首批出貨時點；份額季度序列","if_then":["若 HAMR 2027-06-30 前未出貨 → 護城河方向改向下，不建倉、已持有者減碼一半"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","supply_demand_durability#4"]},{"axis":"前份漂移：公司類型","cause":"新證據","prior_field":["archetype"],"side_a":"品質複利成長","side_b":"循環/商品（次要：品質複利成長）","ruling":"改判：營益率由 FY2023 −6.4%（含快閃）到 FY2026 35.6%，獲利振幅來自每 TB 價格；本輪新出現第三名廠商擴產回應與研究機構「供需趨近平衡」看法，供給可逆性比前份假設高。長約降低循環但未消除；前份同時標晚循環，改判讓框架一致。","evidence_level":"財報序列＋二手報導","settle_metric":"CY2028 每 TB 價格方向","if_then":["若 CY2029–31 長約揭露鎖價且 CY2028 每 TB 價格年增仍 >0 → 改回品質複利成長、Bull 機率上調至 25%"],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#4"]},{"axis":"前份漂移：情境機率與最大回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 25%、Bear 30%，最大回撤 −65%（單點）。","side_b":"本次 Bull 20%、Base 48%、Bear 32%，最大回撤區間 −55% 至 −72%。","ruling":"改用循環股框架重建情境：共識三年 EPS 年複合約 61% 超出內生上界約 25%，Bear 機率須 ≥30%；Toshiba 擴產使 Bear 由 30% 升至 32%、Bull 由 25% 降至 20%；回撤改為區間，深端依 Bear 路徑低點約 −69%。","evidence_level":"本次情境推導","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：重啟條件（首倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤$350（≤11x FY2028E）且 ASP/TB 年增仍 ≥0 → 衛星首倉 1/3；或 CY2027 定價確認持平＋再有 2 家長約延至 2028 → 重跑 DD 升條件式","side_b":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","ruling":"首倉價位由 350 降到 320 美元：Toshiba 擴產使 Bear 機率上升，320 美元時 Base 年化約 9%、上下行比約 2，跨過中等門檻；長約條件改為 CY2029 以後，因 Q4 法說已揭露一家長約延至 CY2029，原「再有 2 家延至 2028」已不是約束所在。","evidence_level":"二手報導＋一手逐字稿","settle_metric":"股價；每 TB 價格年增；CY2029 後長約揭露","if_then":["股價 ≤320 美元且每 TB 價格年增 ≥0 → 首倉 1/3"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"前份漂移：清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼門檻（摘要為空）","side_b":"新設：每 TB 混合價格年增轉負 → 清倉；non-GAAP 毛利率連兩季 <50% → 減碼一半；份額連兩季 <38% → 減碼一半；HAMR 2027-06-30 前未出貨 → 減碼一半","ruling":"前份無門檻可對照，本次依唯一致命點與 H2、H3 補設。","evidence_level":"本次判斷","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（摘要為空）","side_b":"Single Thing：任一季法說揭露每 TB 混合價格年增轉負（漲價週期結束）","ruling":"每 TB 價格是 EPS 路徑中數學上最大的單一敏感度項，設為唯一致命點。","evidence_level":"本次判斷","settle_metric":"每季法說每 TB 混合價格年增","if_then":["若發生 → 清倉，Bear 機率上調至 ≥50%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q1 FY27 法說：毛利率是否落在 55–56% 指引、每 TB 混合價格年增是否維持高十幾%","type":"假設驗證","maps_to":"H2","metric":"non-GAAP 毛利率；每 TB 混合價格年增","threshold":"毛利率 ≥55% 且價格年增 >0","action":"未達 → H2 削弱、不建倉；達標且價格年增 ≥20% → 重算 Base","source_freq":"每季法說","date":"2026-Q4（Q1 FY27 財報，確切日期事實表未涵蓋）","evidence_refs":[]},{"n":2,"text":"44TB HAMR 是否於 2027 上半年量產出貨，40TB ePMR 於 FQ3 FY27 是否達近線 EB 50%","type":"假設驗證","maps_to":"H3","metric":"HAMR 首批量產出貨；ePMR 占近線 EB 比重","threshold":"2027-06-30 前出貨；ePMR ≥50%","action":"未達 → 護城河方向改向下、不建倉、已持有者減碼一半","source_freq":"每季法說","date":"2027-06-30","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"n":3,"text":"Toshiba 是否正式公告菲律賓擴產時程，WDC 是否在法說提到價格競爭","type":"風險","maps_to":"R1","metric":"Toshiba 公告；WDC 每 TB 價格年增","threshold":"公告擴產且 WDC 價格年增降到個位數","action":"Bear 機率上調至 40%、不建倉","source_freq":"事件＋每季法說","date":null,"evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"]},{"n":4,"text":"任一季法說揭露每 TB 混合價格年增轉負","type":"Single Thing","maps_to":"Single Thing","metric":"每 TB 混合價格年增","threshold":"<0%","action":"清倉；未持有者不建倉","source_freq":"每季法說","date":null,"evidence_refs":[]},{"n":5,"text":"股價跌到 320 美元以下且每 TB 價格年增仍 ≥0","type":"估值rearm","maps_to":"rearm","metric":"股價；每 TB 混合價格年增","threshold":"≤320 美元（約 FY2028E 共識 10 倍）且年增 ≥0","action":"首倉 1/3，其餘待 HAMR 出貨確認","source_freq":"每日股價＋每季法說","date":null,"evidence_refs":[]},{"n":6,"text":"大客戶延後提貨或長約重談降價","type":"風險","maps_to":"R3","metric":"單季營收季變動；前十大客戶占比","threshold":"單季營收季減 >10%，或前十大占比 >80%","action":"減碼一半；未持有者不建倉","source_freq":"每季財報＋年報","date":null,"evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"n":7,"text":"關稅、原產地認定或磁頭與稀土供應壓縮毛利率","type":"風險","maps_to":"R5","metric":"non-GAAP 毛利率季變動","threshold":"單季下滑 ≥200bp 且公司歸因關稅或零組件","action":"減碼一半","source_freq":"每季法說；Section 232 公告","date":"2026-11-10（稀土暫停期屆滿）","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"n":8,"text":"Q2 FY27 財報後依新資料重跑判斷","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑判斷","source_freq":"一次","date":"2027-Q1","evidence_refs":[]}],"kill_metrics":[{"metric":"每 TB 混合價格年增（公司法說揭露）","bear_threshold":"轉為負值（<0%）→ 清倉","window":"任一季","source":"WDC 季度法說 CFO 說明","last_status":"ok"},{"metric":"non-GAAP 毛利率","bear_threshold":"<50%（較 Q1 FY27 指引 55–56% 低 5pp 以上）→ 減碼一半","window":"連續 2 季","source":"WDC 季度新聞稿","last_status":"ok"},{"metric":"HDD 份額（容量或出貨口徑）","bear_threshold":"<38% → 減碼一半","window":"連續 2 季","source":"TrendForce／Coughlin 產業資料","last_status":"ok"},{"metric":"44TB HAMR 量產出貨","bear_threshold":"2027-06-30 前未開始出貨 → 減碼一半","window":"至 2027-06-30","source":"WDC 法說與新聞稿","last_status":"ok"}],"action_conditions":{"rearm_trigger":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","exec_line":"現價不追；跌至 320 美元以下且每 TB 混合價格年增仍 ≥0 時首倉 1/3，HAMR 2027 上半年如期出貨後再加 1/3；每 TB 價格年增轉負則清倉、未持有者不建倉。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"股價 ≤320 美元（約 FY2028E 共識 10 倍）且每 TB 混合價格年增仍 ≥0；或 CY2029 後長約揭露鎖價機制且 Toshiba 擴產未引發降價","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"觀望","prior_role":"追蹤"},"decision_out":{"role":"追蹤","row_hit":"2→QC-49(觀望)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"QC-49 承繼前次裁決（矩陣機械輸出＝迴避／row2，前次裁決＝觀望，90 天內翻面查無已發火觸發器）","hit":true,"basis":"qc49_inherit_prior=True, prior_verdict='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"AI 推論與代理式工作負載使雲端 EB 需求年增 ≥25%，WDC 出貨 EB 年增維持 ≥20%（供給受限下上限約 25%）","2y":"FY2027 出貨 EB 年增 ≥20%（Q4 FY26 為 22%，FY2026 全年 25%）","5y":null,"10y":null,"threshold":"出貨 EB 年增 <15% 連 2 季即削弱","source":"每季法說 EB 出貨量與年增率","drift_rule":"以年增 25% 為錨：連 2 季偏離 ≥5% 削弱、連 3 季 ≥10% 反轉"},{"id":"H2","text":"價格與成本剪刀差延續：CY2027 長約價格續漲、每 TB 成本年降約 10%，non-GAAP 毛利率站穩 55% 以上","2y":"FY2027 毛利率 ≥55%、每 TB 混合價格年增 >0","5y":null,"10y":null,"threshold":"non-GAAP 毛利率 <53% 或每 TB 價格年增 ≤0","source":"每季新聞稿毛利率；CFO 每 TB 價格與成本說明","drift_rule":"TTM 毛利率相對 55% 錨連 2 季偏離 ≥5% 削弱、連 3 季 ≥10% 反轉"},{"id":"H3","text":"技術路線不失守：40TB ePMR 於 FQ3 FY27 占近線 EB ≥50%，44TB HAMR 於 2027 上半年量產出貨，HDD 份額維持 ≥40%","2y":"ePMR 占近線 EB ≥50%（FQ3 FY27）、HAMR 2027-06-30 前出貨","5y":"HAMR 成為主力平台後份額不低於 40%","10y":null,"threshold":"HAMR 2027-06-30 前未出貨，或份額連 2 季 <40%","source":"法說產品進度；TrendForce／Coughlin 份額資料","drift_rule":"份額連 4 季偏離 ≥5% 削弱、連 6 季 ≥10% 反轉"}],"R":[{"id":"R1","text":"供給回應：Toshiba 擬倍增 HDD 產能、份額目標由約 10% 拉到 30%，可能以低價搶單；Toshiba 未證實，Citi 認為受碟片與磁頭外購限制。","h_ref":"H2","clock":"🔥","threshold":"Toshiba 正式公告擴產時程，且 WDC 每 TB 價格年增連 2 季降到個位數","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"]},{"id":"R2","text":"HAMR 落後與轉換風險：Seagate 已在兩家大型客戶量產，WDC 44TB 要到 2027 上半年；HAMR 有良率、可靠度與合約賠償條款風險，TrendForce 預估 Seagate 2028 年成最大供應商。","h_ref":"H3","clock":"🔥","threshold":"HAMR 2027-06-30 前未出貨，或份額連 2 季 <40%","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"id":"R3","text":"客戶集中：前十大客戶占 73%、三家合計 44%，集中度三年上升 18pp；單一客戶延後提貨或重談價格即影響當季。","h_ref":"H1","clock":"⚡","threshold":"單季營收季減 >10%，或任一大客戶公開延後提貨","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"id":"R4","text":"快閃長期替代：SanDisk、Samsung、Micron、Kioxia 的 QLC 企業級 SSD；目前每 TB 價差 5–10 倍，NAND 供給可能在 2027 下半年轉寬。","h_ref":"H1","clock":"🐢","threshold":"QLC SSD 與近線 HDD 每 TB 價差縮到 3 倍以內","evidence_refs":["competitive_share_entrants#4"]},{"id":"R5","text":"關稅與供應鏈：組裝集中泰國與馬來西亞、Section 232 第二階段可能課顯著關稅、磁頭獨立供應只剩 TDK、中國稀土逐案核准；公司稱已建立替代來源且關稅至今無重大影響。","h_ref":"H2","clock":"🔥","threshold":"non-GAAP 毛利率單季下滑 ≥200bp 且公司歸因關稅或零組件","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R6","text":"Kioxia 合併傳聞：2026-07 報導稱洽談，可能逾 200 億美元、以股票支付；來源日期不一致、未見協議，且 WDC 已把快閃業務分給 SanDisk，交易邏輯存疑。若成真，WDC 重回快閃循環並稀釋股權。反壟斷面：本輪反壟斷相關查詢（美國司法部、聯邦貿易委員會、歐盟）都沒有結果，屬資料缺口。快閃業務已分出，推論與 Kioxia 的直接重疊有限，但跨國交易仍須多地審查，時程與條件事實表未涵蓋。","h_ref":"H2","clock":"🐢","threshold":"簽署最終協議或公司公告","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"任一季法說揭露每 TB 混合價格年增轉負，代表本輪漲價週期結束","why_fatal":"EPS 路徑靠「價格漲＋成本年降約 10%」的剪刀差；價格轉為年降，毛利率停止擴張並回落，FY2029 共識 42.87 的前提失效，Bear 路徑 EPS 約為 Base 的三分之一。每 TB 價格是情境樹中數學上最大的單一敏感度項。","if_happens":"清倉，未持有者不建倉；Bear 機率上調至 ≥50%，重跑判斷","how_monitor":"每季法說 CFO 揭露的每 TB 混合價格年增（Q4 FY26 為高十幾%）；Seagate 同期定價說法；Toshiba 菲律賓產能時程","probability":"12–24 個月內約 20%：FY2027 絕大部分量已在長約下（CFO 2026-09-09），轉負較可能落在 CY2028 下半年以後"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.16,"peg_fy2":0.2,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":10.22,"FY2027E":20.12,"FY2028E":31.83,"FY2029E":42.87},"fy_end_month":6,"eps_basis":"non-GAAP 稀釋 EPS（持續營運）；FY2026A 10.22 取自 Q4 FY26 法說 CFO，GAAP 26.92 含 SanDisk 持股利益不採用；FY2026 季末為 2026-07-03"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"guidance","event":"Q1 FY27 財報：檢查營收 41 億±1 億、毛利率 55–56%、每 TB 價格年增","impact":"高","watch":"毛利率是否 ≥55%；每 TB 價格年增是否維持高十幾%；CY2029 後長約進度"},{"date":"2026-11","date_precision":"month","type":"regulatory","event":"中國中重稀土出口逐案核准暫停期 2026-11-10 屆滿","impact":"中","watch":"是否延長；公司是否提到供應或成本影響"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"44TB HAMR 預計 2027 上半年開始量產出貨（CFO：Q1 少量、Q2 較多）","impact":"高","watch":"首批出貨是否如期；認證客戶數（目前 4 家）"},{"date":null,"date_precision":null,"type":"capacity","event":"Toshiba 擬於其 FY2027 前倍增 HDD 產能（確切月份事實表未涵蓋）","impact":"高","watch":"Toshiba 正式公告；菲律賓產線量產時程；每 TB 價格反應"},{"date":null,"date_precision":null,"type":"other","event":"Kioxia 合併傳聞（未證實，來源日期不一致）","impact":"低","watch":"公司公告"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
