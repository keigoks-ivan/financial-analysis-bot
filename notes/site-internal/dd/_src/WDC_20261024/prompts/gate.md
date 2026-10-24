你是 DD 管線 v20 的判斷層閘（gate），標的 WDC（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-22 date｜期間與口徑：2026-10-22／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-22）
- `f_peer_wdc_fcf_margin_pct`（q2_moat）｜WDC FCF 利潤率＝27.18 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WDC.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sndk_gross_margin_pct`（q2_moat）｜SNDK 毛利率＝71.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sndk_operating_margin_pct`（q2_moat）｜SNDK 營業利益率＝61.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_000660_ks_operating_margin_pct`（q2_moat）｜000660.KS 營業利益率＝68.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.000660.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_operating_margin_pct`（q2_moat）｜005930.KS 營業利益率＝36.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝24.84 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝39.21 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝50.71 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝19.37 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（20.81 → 24.84）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝16.01 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（33.8 → 39.21）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝15.8 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（43.79 → 50.71）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝1281 USD M（營運現金流 1,389，淨資本支出 108）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_kpi4_sbc`（q4_capital）｜SBC＝45 USD M（占 GAAP 營業利益 2.9%、占營收 1.2%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000106040/000162828026053305/a4ex991-pressreleaseq426.htm（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-08-05））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.16 %｜期間與口徑：2026-10-24／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-24）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝343.67 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝13.84 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 24.84，分子＝快照價 343.67｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝149.4 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 9.96 → 24.84（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-14.88 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_rsi14`（q5_valuation）｜RSI(14)＝35.75｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟢｜期間與口徑：2026-10-24／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
  - 原文：「price 343.67 / W52 362.33 / W104 212.22 / W250 110.32 / W250 13週斜率 4.95%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝362.33 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
- `f_ma_w104`（q5_valuation）｜104 週均線＝212.22 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
- `f_ma_w250`（q5_valuation）｜250 週均線＝110.32 USD｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝4.95 %｜期間與口徑：2026-10-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-24）

### findings_digest 中方向為負或來源衝突的條目（18 條）
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
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Toshiba (Nikkei 報導)計畫投資約 600 億日圓（約 3.8 億美元）擴建菲律賓廠，目標在 FY2027 前把 AI／雲端 HDD 產能加倍；FY2027 指到 2028 年 3 月；Toshiba 容量市占略高於 10%，中期目標約 30%。
  - 來源：Blocks & Files, Distant third HDD maker Toshiba spending $380 million to catch up（as_of 2026-10-06）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2Q23（2023-01 公布）營收年減 36% 至 $31.07 億，GAAP 毛利率 17.0%（前年同期 32.8%），非 GAAP 17.4%（前年 33.6%），Flash 毛利率 15%（前年 36%）；FY3Q23 指引非 GAAP 毛利率 9.0%–11.0%
  - 來源：Zacks via Nasdaq, Why Is Western Digital (WDC) Down 12% Since Last Earnings Report?（as_of 2023-03-01）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2023 10-K：HDD 出貨 501EB（FY2022 645EB、FY2021 541EB）；HDD 營收年減 31%，主因 exabyte 約降 26% 與 ASP 下滑，雲端客戶消化庫存
  - 來源：WDC Form 10-K FY2023 (SEC)（as_of 2023-08-18）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2022-09 管理層稱 NAND 環境可能是過去 10–15 年最艱困，單週股價跌 13.8%；2022-12 Goldman 降評 Sell，預估 2023 非 GAAP 毛利率由約 28% 降至約 17%、NAND ASP 降約 38%
  - 來源：Motley Fool 2022-09-16; Benzinga 2022-12-30（as_of 2022-12-30）｜affects：decision_inputs.bear、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":930.0,"bear_5y_price":165.0,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":18.7,"ev5y_pct":24.3,"irr_base_pct":3.5,"asym_ratio":1.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":24.84,"pe":13.84,"basis":"FY1（FY2027E，6月制財年）Non-GAAP共識前瞻EPS；終端倍數同為前瞻口徑，套在Y5的EPS上"},"eps":{"bull":[26.0,41.0,52.0,58.0,62.0],"base":[24.5,34.0,36.0,33.0,34.0],"bear":[23.0,26.0,18.0,12.0,15.0]},"pe":{"bull":15,"base":12,"bear":11},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.16,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":3},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### WDC_Q4_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：FY27 Q1 營收財測 41 億美元±1 億（原話："We expect revenue to be $4.1 billion, plus/minus $100"）
- 2026-08-05｜CFO｜guidance：FY27 Q1 毛利率財測 55%–56%（原話："range of 55% to 56%."）
- 2026-08-05｜CFO｜guidance：FY27 Q1 EPS 財測（原話："we expect diluted earnings per share to be $4, plus/minus"）
- 2026-08-05｜CEO｜guidance：管理層稱需求年增 25% 以上的 exabyte 成長軌跡（原話："we see demand growing at above 25%, right,"）
- 2026-08-05｜CFO｜margin：Q4 毛利率 54.4%，年增 1,310 bps（原話："Gross margin expanded 1,310 basis points year-over-year"）
- 2026-08-05｜CFO｜margin：每 TB 均價年增幅由高個位數升至高十幾%（原話："digits last quarter to high teens this quarter"）
- 2026-08-05｜CFO｜margin：Q4 年增增量毛利率口徑 84–85%（原話："Ending in Q4 with incremental gross margin year-over-year,"）
- 2026-08-05｜CFO｜margin：CFO 看年增而非季增的增量毛利率（原話："I look more on my incremental gross margins"）
- 2026-08-05｜CFO｜margin：Q4 每 TB 成本年減約 8%（原話："approximately 8% year-over-year."）
- 2026-08-05｜CFO｜margin：中長期每 TB 成本年降約 10%（原話："is on or about 10% year-over-year."）
- 2026-08-05｜CFO｜margin：nearline 與非 nearline 毛利率差距不大（原話："it's all in the same ballpark right now in the 5 zip code"）
- 2026-08-05｜CFO｜margin：FY26 營收與毛利率口徑（原話："36% to $12.9 billion, while expanding gross margins"）
- 2026-08-05｜CEO｜margin：解釋季度毛利率波動來源之一（原話："There are always quarter-to-quarter variations"）
- 2026-08-05｜CFO｜customer：Q4 交付 231 EB，年增 22%（原話："We delivered 231 exabytes to our customers, up 22%"）
- 2026-08-05｜CEO｜customer：客戶採購不均導致 exabyte 季間波動（原話："they don't buy on a very linear basis."）
- 2026-08-05｜CEO｜customer：約 80% 超大規模資料中心資料存於 HDD（原話："Today, roughly 80% of data stored in a hyperscale data"）
- 2026-08-05｜CEO｜customer：新雲、前沿 AI 實驗室需求（原話："Actually, even frontier AI labs are coming to us for supply."）
- 2026-08-05｜CEO｜customer：自駕車客戶 2027 年 exabyte 需求倍增（原話："calendar year '27 has increased multiple fold, right?"）
- 2026-08-05｜CEO｜customer：企業 OEM 轉回混合式儲存（原話："There's a shift back towards hybrid systems"）
- 2026-08-05｜CEO｜competition：對中國開源模型的看法（原話："So we view it very positively for demand going forward."）
- 2026-08-05｜CEO｜product：44TB HAMR 預計 2027 上半年出貨（原話："ship our 44-terabyte HAMR product in the first half"）
- 2026-08-05｜CEO｜product：40TB ePMR 進入兩家客戶量產（原話："are now entering volume production with two customers."）
- 2026-08-05｜CEO｜product：UltraSMR 佔比目標（原話："we expect that UltraSMR will make up around 60% of"）
- 2026-08-05｜CEO｜product：高頻寬硬碟送樣（原話："We are targeting up to 8x the throughput of today's"）
- 2026-08-05｜CEO｜product：40TB 佔 nearline bits 50% 的時點（原話："Right now, we are very much on track to hit 50% of nearline"）
- 2026-08-05｜CEO｜commitment：正在談 2029–2031 長約（原話："customers to establish LTAs for calendar '29, '30 and '31"）
- 2026-08-05｜CEO｜commitment：已有一份大客戶長約到 2029（原話："one LTA of a large customer all the way up to calendar"）
- 2026-08-05｜CEO｜commitment：可預測定價策略（原話："very consistent in talking about predictable pricing"）
- 2026-08-05｜CEO｜risk：LTA 含基準價與基準量，超額部分另訂（原話："base price associated to a base volume."）
- 2026-08-05｜CEO｜risk：非 nearline 價格漲幅較快（原話："a bit more ability to drive more rapid price increases"）
- 2026-08-05｜CFO｜capital_allocation：FCF 全數回饋股東策略不變（原話："No change there to our strategy and our commitment"）
- 2026-08-05｜CFO｜capital_allocation：承諾股息與回購兩項計畫（原話："we're fully committed"）
- 2026-08-05｜CFO｜capital_allocation：Q4 回購 230 萬股共 10 億美元（原話："shares of our common stock for a total of $1 billion."）
- 2026-08-05｜CFO｜capital_allocation：回購數字含 3.28 億美元可轉債溢價現金結算（原話："describing on this call include $328"）
- 2026-08-05｜CFO｜capital_allocation：不為增加單位產能而投資 CapEx（原話："This does not require spending CapEx to add unit capacity"）

### 問答異常語氣（迴避／改口／保留）
- WDC_Q4_2026_Earnings_Call_20260805.md｜問：Reitzes 問 FY27 Q1 是否為營收與增量毛利率的低點｜答法：CFO 稱只給一季財測，未正面回答低點問題，改談需求與產品節奏
- WDC_Q4_2026_Earnings_Call_20260805.md｜問：Woodring 問長約是否有逐季價格調升條款且加速｜答法：CEO 稱『over extrapolating』，只說基準價/基準量結構，不給調升幅度
- WDC_Q4_2026_Earnings_Call_20260805.md｜問：Karl Ackerman 問未來 12 個月有多少比例 nearline 長約重新定價｜答法：CFO 只回答毛利率差距，未回答重新定價比例
- WDC_Q4_2026_Earnings_Call_20260805.md｜問：Muse 問為何財測成長與毛利率低於主要競爭對手｜答法：CEO 以季間波動、長約時點與產品換代回應，未直接對比競爭對手或給數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 4 |
| customer_second_source | found | 3 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 1 | 2 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 5 | 4 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 1 | 5 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 3 | 2 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261013","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","irr_base_pct":5.3,"ev5y_pct":20.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.3,"ev5y_pct":20.0,"irr_base_pct":5.3,"max_dd_pct":-72,"bull_5y_price":900.0,"bear_5y_price":137.5,"p_bull_pct":20,"p_bear_pct":32,"rearm_trigger":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","price_at_dd":386.94,"archetype":"循環/商品","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"WDC","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Western Digital Corporation"},"oneliner":"HDD雙寡頭之一，漲價與高容量換代把毛利率推到58%，但盈餘處在循環高檔，Toshiba擴產與HAMR落後是價格反轉的引信，現價沒有給足安全邊際","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261024/scenario.json","answers":{"q1_business":{"verdict":"賺的是超大規模雲端業者與AI資料中心買近線硬碟的錢，雲端占營收88%。利潤卡在磁頭與碟片的面密度節點，目前價和量都在漲，但利潤主要來自漲價。","reasoning":"2026年9月季（逐字稿2026-10-22財務長）營收44億美元，年增55%。雲端39億美元占88%、年增54%；Client 3.2億美元占7%、年增119%；Consumer 1.93億美元占5%、年增19%。毛利率58.1%，營業利益率49.1%。每TB均價年增28%，EB出貨年增22%，增量毛利率逾80%。事實表的最新季數字仍停在2026年6月季：營收37.47億美元、Non-GAAP營益率44.2%、毛利率54.4%。8月給的9月季指引是營收41億美元、毛利率55%～56%、EPS 4.00，三項都超過。產業時鐘判在III過熱，依據不看股價：毛利率創紀錄並指引再升到60%～61%，近線交期拉長到逾52週，第三名Toshiba開始擴產，價格漲幅還在加速。供需耐久度判週期性將反轉。雙寡頭不增單位產能、長約延到2027～2028年屬結構面，但財務長自承越遠期的長約，價格條款覆蓋越少。Toshiba擴產與雙寡頭HAMR放量會在2028年前後讓供給追上，供給可逆性中等。議價權方面，上游的高容量平台磁頭與碟片自製，但DRAM與NAND投入成本上漲，壓縮每TB成本降幅；下游前十大客戶占73%，三家各占16%、15%、13%，買方高度集中。單點依賴：前三大客戶合計44%，任一家調整供應比例就是集中度風險；護城河證據是重新認證週期與長約。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_non_gaap","f_kpi6_q1_fy2027_non_gaap","f_peer_wdc_gross_margin_pct","f_peer_wdc_operating_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"雲端占88%，集中在超大規模客戶。部分出貨量在長約內（基準量加上修量），長約外的量隨現貨價波動。Client與Consumer的成長由漲價帶動。","unit_econ_note":"每TB均價年增28%（6月季為18%）。每TB成本近期只年減約4%～5%，長期目標約10%，近期受DRAM與NAND投入成本拖累。增量毛利率逾80%。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"近五年有兩個GAAP虧損年度（FY2023、FY2024）；毛利率由22%擺到58%，擺幅逾30個百分點；營收主要由每TB價格驅動"},"industry":{"clock_phase":"III","sd_verdict_source":"逐字稿2026-10-22財務長：越遠期越少出貨量受長約價格條款覆蓋。TrendForce（2026-10-07）：雙寡頭轉HAMR後供需逐步趨近平衡。","bargaining":{"up":"高容量平台的磁頭與碟片自製，外購只用在低容量機種；DRAM與NAND投入成本上漲，是近期的成本壓力","down":"前十大客戶占73%，前三大占44%。長約採基準價加基準量，超額量另行議價，買方集中、議價力強","geo":"組裝集中在泰國與馬來西亞，碟片來自日本，受關稅與原產地認定影響"},"profit_pool_dir":"近兩年利潤池從客戶端流向HDD雙寡頭；2028年供給追上後的方向待驗","tam_table":{"expanded":false,"reason":"HDD已承載超大規模資料中心約八成資料，不屬低滲透或新品類情境；需求用EB年增逾25%衡量即可，承重變數是價格而不是TAM"}}}},"q2_moat":{"verdict":"護城河方向判持平。自製磁頭碟片帶來的面密度是真機制，但EB出貨成長落後Seagate約10個百分點，HAMR也晚一步；目前的定價力強，主要是供需吃緊帶來的。","reasoning":"執行力給8分。9月季營收、毛利率、EPS全數超過8月指引；40TB ePMR是史上最快的一次換代，預計12月季占近線出貨約30%、3月季約50%；首代HAMR預計2027年第一季完成兩家超大規模客戶認證。定價力給6分。眼前每TB均價年增28%，但FY2023同一事業毛利率曾低到22%，說明定價力撐不過整個循環；長約只鎖基準量，越遠期價格覆蓋越少。合計約7分，評B。同業ROIC差距無法呈現：事實表的同業都是快閃記憶體廠，沒有Seagate與Toshiba，所以改用份額軸。2026年9月季EB年增22%，法說會上UBS分析師指出同業約在三成中段，管理層沒有否認，只說會在6～8季內加速；TrendForce預期Seagate在2028年成為最大供應商。執行面判穩定，定價力短期擴大但不能認定可持續，合判持平。威脅三項都是點對點：Toshiba擴產、HAMR落後、快閃長期替代。","fact_refs":["f_peer_wdc_gross_margin_pct","f_peer_wdc_operating_margin_pct","f_peer_wdc_fcf_margin_pct","f_peer_sndk_gross_margin_pct","f_peer_sndk_operating_margin_pct","f_peer_000660_ks_operating_margin_pct","f_peer_005930_ks_operating_margin_pct","f_kpi5_non_gaap"],"verdict_values":{"moat":{"mechanism":"自製磁頭與碟片，加上韌體與伺服機構整合，提高面密度。不增加單位產能，靠每顆硬碟的容量增加EB供給，給客戶最低的總持有成本；超大規模客戶每次換代都要重新認證，形成轉換摩擦。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"EB出貨年增22%（2026年9月季），落後同業約10個百分點（法說會UBS提問，管理層未否認）；TrendForce預期Seagate在2028年居首。同期毛利率58.1%創高。執行力穩定，定價力短期擴大但屬供需所賜，合判持平。","competitor_notes":[{"name":"Seagate","strategy_note":"HDD主要對手。HAMR已有兩家大型超大規模客戶量產採購，EB成長快WDC約10個百分點，是份額方向的主要壓力。"},{"name":"Toshiba","strategy_note":"第三名，計畫在2028年3月前讓HDD產能倍增，份額目標由約10%拉到30%。磁頭與碟片依賴外部供應，是價格下壓的來源。"},{"name":"SNDK","strategy_note":"前子公司，做快閃記憶體。TTM毛利率71%、營益率62%，遠高於WDC，反映NAND漲價高峰；長期是容量層的替代者，不是HDD的直接對手。"},{"name":"000660.KS","strategy_note":"SK海力士。記憶體高峰期營益率68%，和WDC同樣受AI資本支出循環驅動，但產品層不同，不能當HDD的錨。"},{"name":"005930.KS","strategy_note":"三星。營益率36.9%，和WDC的35.6%相近；同時供應SSD，是快閃替代硬碟的主要來源之一。"},{"name":"PSTG","strategy_note":"全快閃儲存陣列廠，事實表沒有財務數字；它的論點是用快閃取代資料中心硬碟。"}],"spread_notes":null,"peer_na_reason":"事實表同業表沒有Seagate與Toshiba，列出的是快閃記憶體與全快閃陣列廠，ROIC差距不可比，所以改用EB份額方向判讀","threats":[{"level":"🟡","text":"Toshiba擴產加上低價搶單，壓低2028年後的每TB價格。擴產本身尚未經Toshiba證實，但屬破壞性競爭，機率取下限以上。","p":"35%","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5","cyclical_supply_discipline_capacity#0"]},{"level":"🟡","text":"HAMR落後Seagate約一年；首代HAMR轉換若出現大規模瑕疵，可能觸發客戶合約的瑕疵條款並壓縮毛利率。","p":"30%","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"level":"🟡","text":"快閃在容量層長期替代硬碟。目前HDD與SSD每TB價差約5～10倍，五年內架構性替代的機率低。","p":"10%","evidence_refs":["competitive_share_entrants#4"]},{"level":"🟡","text":"客戶集中度由FY2024的55%升到FY2026的73%，單一客戶議價或轉單的衝擊放大。","p":"25%","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]}],"roic_durability":{"quadrant":"高利益率；周轉率待查（事實表未涵蓋投入資本，資本支出約占營收4%～6%，屬輕資產更新）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是超大規模業者，三角色一致。超大規模資料中心約八成資料存在HDD上（2026-08-05執行長），HDD每TB價格只有SSD的五到十分之一。AI推論日誌、檢查點、影片讓保存需求屬於需要而非想要；前七大客戶需求能見度到2030～2031年（2026-10-22執行長）。"},{"item":"決策層級","level":"🟡","text":"替代性要在超大規模客戶的認證層級看。每代平台都要重新認證，換供應商要等一個認證週期，這是摩擦。但市場只有雙寡頭加Toshiba，客戶每次換代都能重新分配份額；長約只鎖基準量，上修量另議。"},{"item":"價值鏈分配","level":"🟡","text":"目前HDD廠拿走的價值偏多：毛利率58%，客戶仍接受每TB均價年增28%。但前十大客戶占73%，買方集中；DRAM與NAND投入成本上漲，正把部分價值移向上游。磁頭獨立供應商只有TDK，這點對自製能力弱的Toshiba約束較大。"},{"item":"社會容忍度","level":"🟢","text":"屬企業對企業的儲存採購，沒有監管價格上限，也沒有授權依賴。10-K只有一般性反壟斷揭露，未點名具體調查。政策風險在關稅與稀土管制，屬成本面，不屬社會對漲價的容忍。"}],"roiic":"事實表未涵蓋投入資本。FY2025到FY2026營業利益由約21.3億美元增到約46.0億美元，增加約24.7億美元，期間淨資本支出每季約1億美元，增量報酬極高，但增量主要來自漲價，不是新增投資。","reinvest_rate":"事實表未涵蓋折舊與營運資金變動，無法算出。已知管理層承諾自由現金流全數回饋股東，五年資本支出平均占營收4%～6%，未來兩年略高，再投資率偏低。","endo_ceiling":null,"formula_note":"內生成長率等於增量ROIC乘以再投資率。本公司的成長來自價格與面密度，不靠新增資本，以再投資率推算的天花板無法量化；共識三年EPS成長遠超任何以再投資支撐的上界，缺口歸因於利益率擴張。"}}}},"q3_growth":{"verdict":"成長跑道中等。EB需求年增逾25%可信，但五年後的成長要靠價格延續，第二曲線（高頻寬硬碟、實體AI）還沒有營收。","reasoning":"成長拆解是價格大於量：每TB均價年增28%，EB出貨年增22%，回購是次要因素，沒有併購。共識EPS由FY2027的24.84元、FY2028的39.21元到FY2029的50.71元，FY2027到FY2029年化約43%。若以FY2026基期約9.96元計（2026-07-30快照，當時FY1仍指FY2026），三年年化約72%，遠超以再投資支撐的內生上界。缺口歸因於利益率擴張，也就是漲價延續，屬依賴價格的成長。財務長稱未來3～4季每TB均價仍有上漲空間，之後會放緩。衰退訊號亮兩項：核心份額落後同業，EPS成長顯著高於營收成長。高頻寬硬碟仍在送樣、商業定價結構未定，實體AI只有客戶需求的描述，都不能算成已驗證的第二曲線。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_kpi6_q1_fy2027_non_gaap"],"verdict_values":{"growth":{"driver_mix":"價格（每TB均價年增28%）大於量（EB年增22%）；回購次要；無併購","runway_years":"管理層稱EB需求年增逾25%；HDD已承載約八成超大規模資料，滲透率口徑不適用。以價格成長可持續的年數估，約2～3年","runway_post_y5":"🟡","endo_ceiling_basis":"見護城河段的再投資空間：成長主要來自價格與面密度，不靠新增資本；投入資本與折舊事實表未涵蓋，內生天花板無法用再投資率量化","segments":[{"item":"雲端","value":"39億美元，占88%，年增54%（2026年9月季）"},{"item":"Client","value":"3.2億美元，占7%，年增119%"},{"item":"Consumer","value":"1.93億美元，占5%，年增19%"}],"decay_signals":[{"signal":"核心市占近12個月縮減","lit":true,"evidence":"EB出貨年增22%，落後同業約10個百分點；TrendForce預期Seagate在2028年居首"},{"signal":"EPS成長顯著高於營收成長","lit":true,"evidence":"2026年9月季EPS年增161%，營收年增55%，差距來自漲價帶動的利益率擴張"},{"signal":"毛利率連2季年減","lit":false,"evidence":"毛利率58.1%，年增1,420個基點"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"不增單位產能但持續投資磁頭與碟片，營收年增55%"}],"trap_rating":"🟡（亮兩項）"}}},"q4_capital":{"verdict":"資本配置中上。自由現金流幾乎全數回饋股東，股本緩降，SBC稀釋低；沒有併購可評，回購是否買在循環高檔待驗。","reasoning":"6月季自由現金流12.81億美元（營運現金流13.89億、淨資本支出1.08億）。9月季自由現金流14億美元，回饋股東11億美元；季配息由0.15元調高17%到0.175元。期末淨現金5億美元，2028年到期的可轉債已大幅減少。SBC單季4,500萬美元，占營收1.2%。稀釋股數由3.83億股降到12月季指引的3.80億股。FY2026的GAAP淨利93億美元含非營業利得，自由現金流對淨利的轉換率不具意義；改看TTM自由現金流利潤率27.18%對營業利益率35.6%，轉換正常。風險有兩點：在高峰價位大量回購，若循環反轉，回購的價值會打折；Kioxia合併若以股票支付逾200億美元，約占市值15%，會稀釋股本並重新引入NAND循環。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_peer_wdc_fcf_margin_pct","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近三年無重大併購；Kioxia合併僅是報導中的洽談，未見最終協議"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"前瞻盈餘殖利率7.2%（1÷13.84）；事實表未涵蓋10年期公債殖利率，無法判定是否過關"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC單季4,500萬美元、占營收1.2%；稀釋股數由3.83億股降到指引的3.80億股，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；資本回饋以回購為主，管理層承諾自由現金流全數回饋，2026年9月季回饋11億美元"}}}},"q5_valuation":{"verdict":"現價要FY2028每股盈餘接近共識的39元，而且2029年後不明顯回落才划算。我只信到34元左右，估值合理偏貴。","reasoning":"股價343.67元，是FY2027共識24.84元的13.84倍、FY2028共識39.21元的8.8倍。8.8倍要算便宜，前提是這組盈餘屬於中循環；但毛利率創紀錄、還指引再升，分母本身就是爭點，所以便宜的論證不成立。事實表沒有同業估值倍數，5年估值分位也查不到。賣方平均目標價483元，比現價高約40%；主要分布在500～1,050元，最高與最低相差2.1倍，若含疑似過時的250元則達4.2倍，分歧大，因此下調自身信心。12個月基準取FY2028每股盈餘34元乘11倍，得374元，上檔+8.8%。五年基準取FY2031每股盈餘34元乘12倍，得408元，上檔+18.7%，年化不到4%。共識近三個月修正149%是財年切換造成的假象，真正的FY1上修是19.37%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1，FY2027E Non-GAAP共識）；循環股本應優先看股價淨值比，但事實表未涵蓋","tier":"HDD雙寡頭（事實表無同tier同業）","peers":{"expanded":false,"reason":"事實表同業表沒有估值倍數，列出的也是快閃記憶體廠，不是HDD可比公司，不能當估值錨"},"fwd_pe":13.84,"peg":0.19,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比13.84倍、FY2028共識8.8倍看似便宜，但分母建在紀錄高毛利率上，屬分母爭議，便宜論證不成立。PEG 0.19是高峰期的成長率造成，不代表便宜。基準情境12個月374元（+8.8%）、五年408元（+18.7%），年化不到4%，判黃色。事實表未涵蓋5年估值分位。","upside_short_pct":8.8,"upside_mid_pct":18.7,"denominator_disputed":true,"denominator_note":"FY2027與FY2028共識盈餘建立在毛利率58%～61%與每TB均價年增約三成之上，FY2023同一事業毛利率只有22%；分母是高峰還是中循環，正是本檔的核心爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把高峰盈餘當成中循環。若2028年供給追上後價格循環反轉，股價可能回撤五到七成。","reasoning":"回撤推導如下。現價343.67元，距104週均線212.22元約−38%，距250週均線110.32元約−68%。FY2023同一硬碟事業EB年減26%、營收年減31%，毛利率掉到22%。本輪Bear終點是165元，約−52%。據此把最大回撤區間定在−50%到−70%。股價26週已跌14.88%，RSI 35.75，沒有過熱。8月財報優於預期，股價仍下跌5%，顯示預期已被墊高。8月法說會有四題未正面回答：營收是否見底、長約是否逐季調價、未來12個月多少近線長約要重新定價、指引為何低於競爭對手。10月執行長改口，承認長約有合約內漲價條款，但重新定價的比例仍未揭露。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰盈餘陷阱風險（價格驅動）"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":24.84,"pe":13.84,"basis":"FY1（FY2027E，6月制財年）Non-GAAP共識前瞻EPS；終端倍數同為前瞻口徑，套在Y5的EPS上"},"eps":{"bull":[26.0,41.0,52.0,58.0,62.0],"base":[24.5,34.0,36.0,33.0,34.0],"bear":[23.0,26.0,18.0,12.0,15.0]},"pe":{"bull":15,"base":12,"bear":11},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.2,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":3},"max_dd":{"lo":-70,"hi":-50,"basis":"現價距104週均線約−38%、距250週均線約−68%；FY2023同一硬碟事業EB年減26%、營收年減31%，毛利率掉到22%；Bear終點約−52%，作為區間上緣依據，回到250週均線附近作為下緣","trigger_time":null},"basis":{"bull":"漲價延續到FY2029、HAMR如期放量讓EB年增追上同業、Toshiba擴產被需求吸收；接近共識路徑後持平，終端15倍","base":"12月季指引年化約23元，FY2028升到34元（低於共識39元）；2028年Toshiba與HAMR供給到位後價格放緩，FY2030小幅回落；EPS已是每股口徑並含回購減股，淨回購不另計，終端12倍","bear":"2027年中漲價見頂，2028年供給追上，長約到期後重議價格回落，毛利率退到40%以下，FY2030每股盈餘約12元，終端11倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FY2023同一硬碟事業EB年減26%、營收年減31%，毛利率掉到22%並出現營業虧損；Toshiba計畫在2028年3月前讓產能倍增，份額目標30%；雙寡頭的HAMR也在2027～2028年放量","assumption":"本輪不增單位產能與長約延伸，能讓價格在供給追上時不反轉","consequence":"五年後虧五成最可能的路徑：2028年EB供給成長超過需求，長約到期重議，每TB價格年減，毛利率回到40%以下，EPS落到15元以下，倍數同步壓縮","ruling":"採納，用Bear 35%定價。和唯一致命點（每TB均價年增轉負）完全重疊，不另立","watch":"每季每TB均價年增率、Toshiba正式擴產公告、長約續約價格","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","supply_demand_durability#2","cyclical_supply_discipline_capacity#0"],"fact_refs":["f_ma_w250","f_peer_wdc_gross_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"前十大客戶占比由55%升到73%，三家各占16%、15%、13%。第三方彙整的10-K風險因子指出，HAMR轉換可能觸發客戶合約的大規模瑕疵條款。另有報導稱公司與Kioxia洽談以股票支付的合併，規模可能逾200億美元","assumption":"漲價成功時，超額利潤留在股東手上","consequence":"需求與價格都成立，但利潤可能被單一大客戶議價、HAMR瑕疵賠償，或以股票併購NAND廠稀釋，重新引入快閃循環","ruling":"部分採納。客戶集中與HAMR瑕疵列為風險觸發；Kioxia合併在簽約前不定價，簽約就重跑判斷","watch":"單一客戶營收占比、HAMR良率與退貨、Kioxia最終協議","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","substitute_technology#2"],"fact_refs":["f_kpi3_fcf"]},{"view":"價格已反映太多","evidence":"股價由250週均線110元漲到344元；8月財報優於預期，股價仍下跌5%，顯示預期已被墊高","assumption":"市場以FY2028共識39元為基準","consequence":"若FY2028只達基準34元、倍數回到10倍，股價約340元，現價沒有上檔","ruling":"部分採納。FY2028共識8.8倍已含部分循環折價，所以不是貴到要迴避；但以本輪基準看，現價沒有安全邊際","watch":"12月季每TB均價年增與2027年3月季指引","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"長期替代風險是快閃（SanDisk、三星、美光、鎧俠）；硬碟在泰國與馬來西亞組裝，零件來自日本、中國、菲律賓，對這些地區課徵的關稅多次變動","assumption":"HDD與SSD每TB價差維持5～10倍，關稅可以轉嫁","consequence":"若價差縮小或關稅吃進毛利，HDD在容量層的角色會被侵蝕","ruling":"反駁五年內的架構替代，因為價差仍大；關稅列風險觸發，以毛利率是否吸收失敗來判定","watch":"HDD與SSD每TB價差、232條款第二階段的涵蓋品項、單季毛利率","evidence_refs":["competitive_share_entrants#4","reg_tariff_export#3","geo_supply_chain#0"],"fact_refs":["f_kpi5_non_gaap"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 386.94 → 本次 343.67（-11.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=386.94","side_b":"本次 price_at_dd=343.67","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 386.94 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 386.94 美元：Bull 價 900、Bear 價 137.5，五年期望值 +20.0%，基準年化 5.3%，不對稱比 1.3","side_b":"本次情境、股價仍用 386.94 美元：Bull 價 930、Bear 價 165，五年期望值 +10.4%，基準年化 1.1%，不對稱比 1.4","ruling":"先換情境、股價不動：五年期望值少 9.6 個百分點，基準年化少 4.2 個百分點。不對稱比由 1.3 變為 1.4。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 386.94 美元：五年期望值 +10.4%，基準年化 1.1%，不對稱比 1.4","side_b":"本次情境、股價 343.67 美元：五年期望值 +24.3%，基準年化 3.5%，不對稱比 1.88","ruling":"再換股價、情境不動：起點價下跌 11.2%，五年期望值多 13.9 個百分點，基準年化多 2.4 個百分點，不對稱比由 1.4 升到 1.88。合計五年期望值比前份多 4.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"結構性需求對循環高檔","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：12月季指引EPS 5.80元，年化約23元，即使停在這個水準，15倍也有348元；FY2028共識只有8.8倍；股價跌破52週均線但仍在104週均線之上，屬回檔區；前七大客戶需求能見度到2030～2031年；雙寡頭不增單位產能，長約延到2027～2028年","side_b":"毛利率58.1%創紀錄並指引升到60%～61%，FY2023曾只有22%；每TB均價年增由高個位數加速到28%；Toshiba擴產指向2028年；財務長說越遠期越少出貨量受長約價格覆蓋","ruling":"不可調和（方向相反），選循環側。依據有三：能見度是量，不是價（2026-10-22財務長）；價格增速還在加速，正是高檔特徵；同一事業FY2023下行時EB年減26%。執行上觀望，等價格或價格證據","evidence_level":"中：一手法說會與10-K歷史；Toshiba擴產為報導，尚未證實","settle_metric":"2028年上半年每TB均價年增率與毛利率","if_then":["若FY2028上半年每TB均價年增仍≥+10%、毛利率≥55%，結構側成立，重跑判斷，可首倉1/3","若任一季每TB均價年增轉負，循環側成立；未持有不碰，持有者清倉","若股價先走、證據未到：反彈回52週均線362元以上但每TB均價年增放緩，不追","若股價跌到320元以下而每TB均價年增仍≥+10%，屬基本面無損的下跌，首倉1/3分批買"],"evidence_refs":["cyclical_prior_downcycle_behavior#1","supply_demand_durability#2","cyclical_supply_discipline_capacity#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：Toshiba計畫在2028年3月前讓產能倍增、份額目標30%；WDC的EB成長落後Seagate約10個百分點，HAMR晚一步","side_b":"結構轉好：雙寡頭不增單位產能，長約加接單生產取代現貨，需求能見度到2030～2031年。其他結構變數：關稅與稀土管制，客戶集中度升到73%","ruling":"雙向拉鋸。結構轉好與競爭惡化同時發生，交會點是每TB價格；2028年前看不出哪邊勝出","evidence_level":"中","settle_metric":"Toshiba正式擴產與2028年長約續約價格","if_then":["若Toshiba正式公告擴產且長約重議價格下調，判競爭惡化中，凍結進場","若Toshiba擴產後兩季每TB均價年增仍≥+10%，判結構性轉好中，重跑判斷"],"evidence_refs":["competitive_share_entrants#0","reg_tariff_export#2","customer_concentration_credit#0"]},{"axis":"每TB成本降幅前後說法","cause":null,"prior_field":null,"side_a":"2026-08-05財務長：6月季每TB成本年減約8%，中長期約年減10%","side_b":"2026-10-22財務長：DRAM與NAND投入成本上漲，近期每TB成本年減低於10%，9月季約4%～5%，靠價值工程逐步抵銷","ruling":"可調和，屬程度差異。長期目標沒改，但近期成本降幅減半，代表毛利率擴張更依賴漲價","evidence_level":"高：一手法說會","settle_metric":"2027年3月季每TB成本年減幅度","if_then":["若連兩季每TB成本年減<5%而漲價放緩，毛利率指引會先轉弱，Bear機率上調到40%"],"evidence_refs":[]},{"axis":"HAMR時程","cause":null,"prior_field":null,"side_a":"2026年7月報導：2026年上半年開始與一家超大規模客戶認證，年底擴到最多三家，2027年上半年量產爬坡","side_b":"2026-10-22執行長：兩家超大規模客戶在2027年第一季完成認證，2027年上半年量產；另兩家在2027年上半年才開始認證；第二代HAMR在2027年下半年開始認證","ruling":"可調和。量產時點沒變，但年底三家改成兩家；Seagate已有兩家量產採購，落後約一年","evidence_level":"高：一手法說會對照二手報導","settle_metric":"2027年3月底是否完成兩家認證","if_then":["若認證延後到2027年第二季以後，Bull機率下調到15%，維持觀望"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"長約漲價條款說法","cause":null,"prior_field":null,"side_a":"2026-08-05：分析師問長約是否逐季調價，執行長說對方過度外推，只講基準價加基準量","side_b":"2026-10-22：執行長說一批長約在進入不同期間時有合約內漲價，週年時依新平台的總持有成本調價","ruling":"新說法較正面，但沒給幅度，也沒給重新定價的比例，不改基準情境","evidence_level":"中：管理層口述，無數字","settle_metric":"長約覆蓋比例與重新定價比例是否揭露","if_then":["若揭露2028年以後長約有鎖價條款且覆蓋過半出貨，Bear機率下調到30%並重跑判斷"],"evidence_refs":[]},{"axis":"共識修正數字的口徑","cause":null,"prior_field":null,"side_a":"事實表列FY1共識近三個月修正+149.4%（9.96元到24.84元）","side_b":"9月季EPS 4.64元加12月季指引5.80元，上半年已達10.44元，所以9.96元不可能是FY2027共識，應是財年切換前的FY2026","ruling":"149%是財年切換造成的假象，不當成上修動能；真正的FY1上修採兩份快照之間的+19.37%","evidence_level":"高：用事實表與逐字稿數字互證","settle_metric":"下一份快照的同財年比較","if_then":["若之後同財年的共識連兩次下修，視為循環轉折的早期訊號，凍結進場"],"evidence_refs":[]},{"axis":"FY2026盈餘基期","cause":null,"prior_field":null,"side_a":"年度財報GAAP稀釋EPS 26.92元、淨利93億美元","side_b":"同年營業利益約46億美元，淨利遠高於營業利益，含非營業利得；Non-GAAP基期約10元","ruling":"成長與估值一律用Non-GAAP口徑，GAAP的26.92元不能當基期，也不用來算自由現金流轉換率","evidence_level":"高","settle_metric":"10-K非營業項目明細（事實表未涵蓋）","if_then":["若非營業利得被證實可重複發生，再改用GAAP口徑重估"],"evidence_refs":[]},{"axis":"前份漂移：股價下跌後的估值與結論","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份：股價386.94元，估值黃色，品質B，觀望追蹤","side_b":"本次：股價343.67元（−11.2%）；FY2028共識由33.8元升到39.21元，倍數降到8.8倍，但分母爭議沒解，估值維持黃色、品質B、結論維持觀望","ruling":"價格下跌加上共識上修都讓倍數變便宜，但便宜來自高峰分母，結論不因價格改變","evidence_level":"高","settle_metric":"每TB均價年增率","if_then":["若股價跌到320元以下而每TB均價年增≥+10%，首倉1/3"],"evidence_refs":[]},{"axis":"前份漂移：基本面判讀","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：陷阱風險黃、護城河持平、跑道黃、循環/商品、晚循環","side_b":"2026-10-22季報：營收、毛利率、EPS全面超過8月指引，每TB均價年增加速到28%，前七大客戶能見度到2030～2031年；但EB年增22%仍落後同業，HAMR認證仍在2027年第一季","ruling":"新證據強化短期盈餘，也讓循環位置更靠高檔（價格加速、毛利率再創高），五欄都維持不變","evidence_level":"高：一手法說會","settle_metric":"12月季每TB均價年增與EB年增","if_then":["若12月季EB年增回到25%以上且HAMR認證如期，護城河方向重評為擴大"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"前份漂移：情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 20%、Bear 32%，最大回撤−72%單點","side_b":"本次：Bull 20%、Base 45%、Bear 35%；最大回撤改為區間−50%到−70%","ruling":"共識三年成長遠超以再投資支撐的天花板，Bear機率下限30%；價格加速屬高檔訊號，Bear再上調3點。回撤改用區間，並以104週、250週均線與FY2023下行幅度定界","evidence_level":"中","settle_metric":"每TB均價年增率","if_then":["若FY2028上半年每TB均價年增仍≥+10%，Bear機率回調到30%"],"evidence_refs":[]},{"axis":"前份漂移：進場重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","side_b":"股價≤$320（約9.4倍基準FY2028每股盈餘34元）且最新一季每TB均價年增≥+10%→首倉1/3；或HAMR量產後連兩季每TB均價年增≥+10%→重跑判斷","ruling":"價格門檻320元不變，但錨改為本輪基準34元的約9.4倍：共識FY2028已升到39.21元，沿用舊錨的10倍會變成392元，等於用上修後的高峰數字放寬門檻。價格條件由年增≥0收緊到≥+10%，因為漲價已加速到28%，掉到10%以下就是循環轉折。第二條改看HAMR量產後的價格，因為法說會表明越遠期長約的價格覆蓋越少，CY2029以後的鎖價揭露不會出現","evidence_level":"高","settle_metric":"股價與每TB均價年增率","if_then":["若兩條都未觸發，維持觀望到2027年1月財報再複審"],"evidence_refs":[]},{"axis":"前份漂移：減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標","side_b":"本次設四項：每TB均價年增連2季<+5%或任一季轉負→清倉；毛利率連2季年減且<50%→減碼一半；EB年增在FY2027下半年仍<20%→不加碼；HAMR認證延後到2027年第二季以後→維持觀望","ruling":"前份只有進場條件，本次補上持有後的減碼與清倉線，讓循環高檔的出場有數字可依","evidence_level":"中","settle_metric":"每季法說會","if_then":["若任一清倉條件觸發，持有者當季清倉"],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設Single Thing（空白）","side_b":"某一季每TB平均售價年增率由正轉負（價格循環反轉）","ruling":"價格是毛利率與EPS在數學上最大的敏感度項（增量毛利率逾80%），比Toshiba擴產或HAMR延誤這類中間變數更直接，所以把Single Thing定在價格","evidence_level":"高","settle_metric":"每季每TB均價年增率","if_then":["若轉負，持有者清倉；未持有不碰"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到320元以下，且最新一季每TB均價年增仍≥+10%：盈餘分母的爭議由價格補償","type":"估值rearm","maps_to":"H1","metric":"股價與每TB均價年增率","threshold":"股價≤$320且每TB均價年增≥+10%","action":"首倉1/3目標倉","source_freq":"每日股價、每季法說會","date":null},{"n":2,"text":"某一季每TB平均售價年增率由正轉負","type":"Single Thing","maps_to":"Single Thing","metric":"每TB均價年增率","threshold":"任一季<0%","action":"未持有不碰；持有者清倉","source_freq":"每季法說會","date":null},{"n":3,"text":"Toshiba正式確認菲律賓擴產，且公司揭露長約重議價格下調","type":"風險","maps_to":"R1","metric":"Toshiba公告與長約價格","threshold":"擴產經正式公告且任一季每TB均價年增<+10%","action":"凍結進場；持有者減碼一半","source_freq":"新聞與每季法說會","date":"2028-03","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5","cyclical_supply_discipline_capacity#0"]},{"n":4,"text":"首代HAMR如期完成兩家超大規模客戶認證，且量產不折價","type":"假設驗證","maps_to":"H2","metric":"HAMR認證與量產時點","threshold":"2027年3月底前完成兩家認證，2027年上半年量產出貨","action":"如期則重跑判斷；延後一季以上則不追，Bull機率降到15%","source_freq":"每季法說會","date":"2027-03","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"n":5,"text":"中國中重稀土出口逐案核准的暫停期到期","type":"風險","maps_to":"R4","metric":"稀土管制與公司供應揭露","threshold":"暫停期未延長，且公司揭露供應中斷或毛利率單季下滑>2個百分點","action":"凍結進場","source_freq":"公告與每季法說會","date":"2026-11-10","evidence_refs":["geo_supply_chain#2"]},{"n":6,"text":"232條款第二階段關稅涵蓋硬碟，或泰國、馬來西亞產地加稅","type":"風險","maps_to":"R4","metric":"關稅範圍與單季毛利率","threshold":"關稅涵蓋硬碟，且毛利率單季下滑>2個百分點","action":"凍結進場；持有者減碼一半","source_freq":"政府公告與每季財報","date":null,"evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0"]},{"n":7,"text":"與Kioxia簽署合併最終協議","type":"風險","maps_to":"H3","metric":"併購協議","threshold":"簽約且交易規模>市值5%","action":"重跑判斷，完成前不建倉","source_freq":"公司公告","date":null},{"n":8,"text":"毛利率連兩季年減且跌破50%","type":"減碼","maps_to":"H1","metric":"Non-GAAP毛利率","threshold":"連2季年減且<50%","action":"持有者減碼一半","source_freq":"每季財報","date":null},{"n":9,"text":"單一客戶占比或前十大客戶占比再升","type":"風險","maps_to":"R3","metric":"10-K客戶集中度","threshold":"單一客戶占年營收>20%，或前十大>80%","action":"Bear機率上調到40%並重跑判斷","source_freq":"每年10-K","date":"2027-08","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"n":10,"text":"2026年12月季財報複審","type":"複審日期","maps_to":"H1","metric":"EPS對指引5.80元、每TB均價年增、EB年增","threshold":"EPS≥5.60元、每TB均價年增≥+20%、EB年增≥22%","action":"重跑判斷","source_freq":"季度","date":"2027-01"}],"kill_metrics":[{"metric":"每TB平均售價年增率","bear_threshold":"連2季<+5%或任一季轉負→清倉","window":"每季財報","source":"公司法說會（財務長揭露）","last_status":"ok"},{"metric":"Non-GAAP毛利率","bear_threshold":"連2季年減且<50%→減碼一半","window":"每季財報","source":"公司財報新聞稿","last_status":"ok"},{"metric":"EB出貨年增率","bear_threshold":"FY2027下半年仍<20%→不加碼","window":"至2027年7月FY2027第四季","source":"公司法說會","last_status":"warning"},{"metric":"首代HAMR兩家超大規模客戶認證","bear_threshold":"延後到2027年第二季以後→維持觀望","window":"2027年3月至6月","source":"公司法說會","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#1","reason":"來源是通路商部落格二手轉引Bloomberg。2026-10-22法說會執行長一手說明：高容量領先平台全用自製磁頭，外購磁頭只用在低容量機種。這項依賴對自製能力最弱的Toshiba約束更大，不構成本公司的供應單點"}],"action_conditions":{"rearm_trigger":"股價≤$320（約9.4倍基準FY2028每股盈餘34元）且最新一季每TB均價年增≥+10%→首倉1/3；或HAMR量產後連兩季每TB均價年增≥+10%→重跑判斷","exec_line":"觀望。卡住的是盈餘分母爭議（高峰或中循環）：等股價到320元以下且價格證據仍在，或等HAMR量產後的價格證據；未持有不追，持有者以每TB均價年增轉負為清倉線","holding_cap":"循環股倉位上限3%，首倉1/3"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"等股價≤$320且最新一季每TB均價年增≥+10%，或HAMR量產後連兩季每TB均價年增≥+10%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"觀望","prior_role":"追蹤"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-14.88, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"漲價延續：到FY2028（2028年6月），每TB均價維持年增，毛利率守在55%以上","2y":"FY2028結束時毛利率≥55%，每TB均價年增≥+5%","5y":null,"10y":null,"threshold":"每季每TB均價年增≥+5%，且Non-GAAP毛利率≥55%","source":"每季財報新聞稿與法說會（財務長揭露每TB均價年增）","drift_rule":"毛利率較門檻低5%以上連2季為削弱；低10%以上連3季為反轉"},{"id":"H2","text":"換代補回出貨量：40TB ePMR與HAMR讓EB年增回到25%以上，與Seagate的差距收斂","2y":"FY2028上半年EB年增≥25%","5y":null,"10y":null,"threshold":"2027年3月底前完成兩家超大規模客戶HAMR認證；FY2027第四季起EB年增≥25%","source":"每季法說會的EB出貨數字與HAMR里程碑","drift_rule":"自2027年3月季起計：EB年增連2季低於23.75%為削弱；連3季低於22.5%為反轉"},{"id":"H3","text":"結構改變縮小下行：雙寡頭不增單位產能、長約延伸，下一次下行的營收跌幅小於FY2023的31%","2y":null,"5y":"下一次需求或價格下行時，年營收跌幅<20%，毛利率不低於40%","10y":null,"threshold":"下行年度營收年減<20%，且毛利率≥40%","source":"10-K年度營收與毛利率；同業產能公告","drift_rule":"TTM營收較高點低5%以上連4季為削弱；低10%以上連6季為反轉"}],"R":[{"id":"R1","text":"Toshiba擴產加上低價搶單，2028年後每TB價格成長放緩甚至轉負","h_ref":"H1","clock":"🔥","threshold":"Toshiba正式公告擴產，且每TB均價年增連2季<+10%","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5","cyclical_supply_discipline_capacity#0"]},{"id":"R2","text":"HAMR落後Seagate，EB份額持續流失；HAMR轉換若出現大規模瑕疵，會觸發合約條款","h_ref":"H2","clock":"🔥","threshold":"HAMR認證延後到2027年第二季以後，或EB年增連4季落後同業10個百分點以上","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"id":"R3","text":"客戶集中加上超大規模業者資本支出循環：下行時EB量縮，FY2023曾年減26%","h_ref":"H3","clock":"🐢","threshold":"單一客戶占年營收>20%，或任一季EB季減>15%","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R4","text":"泰國、馬來西亞生產集中，加上關稅與稀土管制，吃進毛利","h_ref":"H1","clock":"⚡","threshold":"關稅或稀土因素使毛利率單季下滑>2個百分點","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#2"]},{"id":"R5","text":"快閃在容量層長期替代硬碟","h_ref":"H3","clock":"🐢","threshold":"HDD與SSD每TB價差縮到3倍以內","evidence_refs":["competitive_share_entrants#4"]}],"single_thing":{"description":"某一季每TB平均售價年增率由正轉負（價格循環反轉）","why_fatal":"毛利率由22%擺到58%，幾乎全由價格驅動，增量毛利率逾80%；價格轉負時，利益率下修的槓桿同樣放大。FY2023曾營收年減31%並轉為營業虧損","if_happens":"基準情境失效，改走Bear路徑（FY2030每股盈餘約12元）；持有者清倉，未持有不碰，等下一輪投降訊號","how_monitor":"每季法說會揭露的每TB均價年增率（2026年6月季18%、9月季28%），並追長約續約價格、Toshiba擴產進度、HAMR放量","probability":"12～24個月內約25%：財務長稱未來3～4季仍有漲價空間、之後放緩；Toshiba擴產目標在2028年3月前"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":8.76,"peg_fy2":0.3,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2026A":9.96,"FY2027E":24.84,"FY2028E":39.21,"FY2029E":50.71},"fy_end_month":6,"eps_basis":"Non-GAAP稀釋每股盈餘（Koyfin共識，6月制財年）。FY2026A用2026-07-30快照的FY1共識9.96元代理：該快照在財年切換前，指的是FY2026。GAAP的26.92元含非營業利得，不能當基期"},"catalysts":[{"date":"2026-11-10","date_precision":null,"type":"regulatory","event":"中國中重稀土出口逐案核准的暫停期到期","impact":"中","watch":"是否延長；公司是否揭露供應影響"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"2026年12月季財報（指引營收51億美元、EPS 5.80元）","impact":"高","watch":"每TB均價年增、EB年增、2027年3月季指引"},{"date":"2027-03","date_precision":"month","type":"product","event":"首代HAMR完成兩家超大規模客戶認證","impact":"高","watch":"是否如期、是否折價"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"首代HAMR量產出貨（CY2027上半年）","impact":"高","watch":"EB年增是否回到25%以上"},{"date":"2028-03","date_precision":"quarter","type":"capacity","event":"Toshiba菲律賓擴產的目標期限（其FY2027）","impact":"高","watch":"Toshiba正式公告與報價行為"}]}
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
