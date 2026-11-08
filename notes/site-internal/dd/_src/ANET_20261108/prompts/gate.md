你是 DD 管線 v20 的判斷層閘（gate），標的 ANET（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝3657.6 USD million｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：consensus 約 $3.31B（來源：web_search／earningswhispers，次級來源）；公司 Q3 指引 $3.3B
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝1795.8 USD million；margin 49.1%｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi3_gaap_gross_margin`（q1_business）｜GAAP gross margin＝63.6 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi8_deferred_revenue`（q1_business）｜Deferred revenue（流動＋非流動）＝6839.5 USD million（流動 5,102.2；非流動 1,737.3）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi9_q4_fy2026_guidance_reven`（q1_business）｜Q4 FY2026 guidance：revenue＝3900～4000 USD million｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-03 date｜期間與口徑：2026-11-03／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-03）
- `f_peer_anet_gross_margin_pct`（q2_moat）｜ANET 毛利率＝62.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ANET.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_anet_operating_margin_pct`（q2_moat）｜ANET 營業利益率＝43.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ANET.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_anet_fcf_margin_pct`（q2_moat）｜ANET FCF 利潤率＝42.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ANET.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_csco_gross_margin_pct`（q2_moat）｜CSCO 毛利率＝64.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSCO.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_csco_operating_margin_pct`（q2_moat）｜CSCO 營業利益率＝25.36 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSCO.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_csco_fcf_margin_pct`（q2_moat）｜CSCO FCF 利潤率＝20.16 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSCO.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_hpe_gross_margin_pct`（q2_moat）｜HPE 毛利率＝36.73 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HPE.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_hpe_operating_margin_pct`（q2_moat）｜HPE 營業利益率＝7.84 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HPE.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_cien_gross_margin_pct`（q2_moat）｜CIEN 毛利率＝44.07 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CIEN.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_cien_operating_margin_pct`（q2_moat）｜CIEN 營業利益率＝14.12 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CIEN.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_cls_gross_margin_pct`（q2_moat）｜CLS 毛利率＝11.46 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CLS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝4.28 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝5.64 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝6.99 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝13383.87 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝18699.44 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi6_stock_based_compensation`（q1_business）｜Stock-based compensation（占 GAAP 營業利益 8.4%；占營收 3.8%）＝138.1 USD million｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi7_free_cash_flow`（q1_business）｜Free cash flow（僅有前九月，單季未揭露）＝3792.5 USD million（9M 2026：營業現金流 3,977.4 − 資本支出 184.9）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026（arista.com/en/company/news/press-release/25025-pr-20261103；SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001596532/000159653226000252/ex991q326-earningsrelease.htm）（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-14359.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 0.0、現金 14359.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1263.4 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝170.8 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝45.79 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝76.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝76.8 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝39.91 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 4.28，分子＝快照價 170.8｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-1.38 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（4.34 → 4.28）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝4.44 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（5.4 → 5.64）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.14 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 4.11 → 4.28（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 170.8 / W52 157.84 / W104 134.3 / W250 84.89 / W250 13週斜率 2.7%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝157.84 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_rsi14`（q5_valuation）｜RSI(14)＝43.36｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝20.48 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝18.15 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝77.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝16.94 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝70.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（21 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2025 列出競爭對手：Cisco 長期主導，另有 Dell/EMC、Extreme、HPE（已收購 Juniper）、Huawei、Nvidia 與白牌廠商；並指新進入者與替代技術可能造成降價壓力。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-17）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：競爭已造成降價壓力、可能損失份額；AI Ethernet 產品需與較成熟的 InfiniBand 及他廠 AI Ethernet 競爭，品牌認知尚未廣泛建立。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：IDC：1Q26 Nvidia 成為資料中心乙太網路交換器營收第一，Arista 資料中心份額 20.7%
  - 來源：IDC Markets and Trends 2026-06-17（as_of 2026-06-17）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：IDC：2Q26 Arista 資料中心份額 18.7%、整體 13.4%；Nvidia 20.4%
  - 來源：IDC Markets and Trends 2026-09-11（as_of 2026-09-11）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：Meta 與 Nvidia 簽多年 Spectrum-X 乙太網路部署合約，Arista 股價下跌
  - 來源：rallies.ai（as_of 2026-02-18）｜affects：moat_trend、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2025 10-K 風險因子：大型系統廠商越來越多提供垂直整合的雲端網路方案，作為 Arista 產品的替代；white box 網路廠商（開源 OS）列為競爭者。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：decision_inputs.bear、moat_trend
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：Next Platform 報導：Microsoft 與 Meta 並非獨家向 Arista 採購交換器，並促使 Arista 支援其 SONiC 與 FBOSS 網路作業系統（多供應商）。
  - 來源：The Next Platform, The current AI networking wave will be a tsunami of money by 2027（as_of 2026-02-13）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 兩大終端客戶占營收 26% 與 16%（合計 42%）；FY2024 為 20%／15%，FY2023 為 18%／21%。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-17）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：公司自述客戶集中度與下單時點每季/每年會波動；前兩大經銷商占 2025 年底應收帳款 52%（2024 年底 50%）。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-17）｜affects：thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：S&P 2026-10-30 將 Meta 評等展望調為負面（AA- 維持），理由為資本支出與租賃推升槓桿。
  - 來源：ppc.land: Meta faces S&P downgrade as 2027 AI capex forecast tops 225bn（as_of 2026-10-31）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：業界分析稱記憶體供需缺口為結構性，2027 可能惡化並延續至 2028；製造商優先供應 AI 基建而非傳統網通硬體
  - 來源：Alpha-Sense: AI memory super cycle; telecomcauliffe: chip shortages expected through 2027（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 揭露：美國自2025年2月起依IEEPA及Section 232等授權加徵關稅，另有對中國的Section 301關稅；關稅成本可能無法完全轉嫁，供應鏈調整未必成功。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 揭露：產品含加密技術，出口須政府授權；中國對鍺、鎵等材料實施出口管制（2025年5月起部分放寬），可能影響元件採購與成本。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-17）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：最新10-Q（2026Q3）稱若關稅或非關稅措施升級，毛利率可能進一步受影響；產品營業成本含運費與關稅。
  - 來源：SEC EDGAR 10-Q 2026-09-30（as_of 2026-10-30）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Arista 製造全數外包，合約製造夥伴在馬來西亞、越南、墨西哥生產；關稅與非關稅貿易措施涉及美、墨、中等可能影響零件供應
  - 來源：Arista 10-K FY2024（as_of 2025-02-20）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Arista 對 Broadcom 交換晶片高度依賴，且與零件供應商通常無書面供貨保證、無關鍵零件獨家權
  - 來源：Arista 10-K FY2024（as_of 2025-02-20）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Q3 2026 10-Q 列台灣為可能對通訊設備加徵關稅/非關稅壁壘的政府之一
  - 來源：Arista 10-Q Q3 2026（as_of 2026-11-04）｜affects：thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：IDC：2Q26 Arista 資料中心乙太網交換器份額 18.7%（1Q26 為 20.7%），營收約 $2.5B、年增 37.6%；NVIDIA 同季 20.4%，1Q26 起居資料中心乙太網交換器營收第一
  - 來源：IDC Worldwide Ethernet Switch tracker 部落格/新聞稿（as_of 2026-09-11）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 自述：新進者與客戶正開發基於開源 NOS 的白盒網通產品，或採拆解式採購搭配自有軟體，替代技術快速被採用可能造成降價壓力、流失銷售。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-17）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：若無法預期技術變化並及時推出新產品，產品可能過時；800GbE AI 乙太網產品能否維持競爭力取決於交付時程與客戶接受度。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-17）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Fierce Network：Arista 居資料中心交換第一，但 Nvidia 以 Spectrum-X 逼近。
  - 來源：Fierce Network 'AI tailwind keeps Arista at No. 1 spot in data center switching — now Nvidia looms'（as_of 2026-06-01）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":480.0,"bear_5y_price":93.5,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":52.2,"ev5y_pct":55.2,"irr_base_pct":8.8,"asym_ratio":3.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":4.28,"pe":39.91,"basis":"FY1（FY2026E）共識 EPS 4.28 美元、現價 170.8 美元；終端倍數同樣配終端當年度 EPS。"},"eps":{"bull":[6.4,8.6,10.8,13.0,15.0],"base":[5.9,7.2,8.4,9.5,10.4],"bear":[5.2,4.7,4.6,5.0,5.5]},"pe":{"bull":32,"base":25,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ANET_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CEO｜guidance：CEO 說這是今年第三次上調財測（2026 營收約 126 億美元、年增 40%）（原話："we are excited to increase our guidance for the third time"）
- 2026-08-04｜CFO｜guidance：CFO 給 Q3 毛利率與營業利益率指引（原話："operating margin between 48% and 49%"）
- 2026-08-04｜CFO｜guidance：CFO 給全年校園營收目標（原話："our 2026 campus revenue goal is at least $1.25 billion"）
- 2026-08-04｜CFO｜guidance：CFO 給全年 AI fabrics 目標（至少 35 億美元；CEO 另處講 AI target 至少 36 億）（原話："is at least $3.5 billion."）
- 2026-08-04｜CEO｜guidance：CEO 提到 AI 目標至少 36 億美元，其中 scale-across 約占 30%（原話："30% of our overall AI target of at least $3.6 billion"）
- 2026-08-04｜CFO｜margin：CFO 維持全年毛利率區間 62%–64%，含供應鏈成本上升（原話："maintaining the range for the fiscal year of 62% to 64%"）
- 2026-08-04｜CFO｜margin：CFO 上調全年營業利益率目標至 48%–49%（原話："operating margin target now at a range of 48% to 49%"）
- 2026-08-04｜CFO｜margin：CFO 拆解 Q2 毛利率對比指引：關稅退款 20–30 bps，其餘為客戶組合（原話："20 to 30 bps of tariff refund and the remainder more of a"）
- 2026-08-04｜CFO｜margin：CFO 表示毛利率目前尚未計入漲價效果（原話："I wouldn't put anything in there yet due to a price increase"）
- 2026-08-04｜CEO｜margin：CEO 說漲價效果要到年底或明年才反映，因仍在消化積壓訂單（原話："price increases will really help or affect us only towards"）
- 2026-08-04｜CFO｜margin：CFO 說明 Q2 毛利率 63.4%，年減因客戶組合（原話："gross margin in Q2 was 63.4%, down from 65.6% in the prior"）
- 2026-08-04｜CFO｜margin：CFO 報 Q2 營業利益率（原話："operating income for the quarter was $1.5 billion or 49.9%"）
- 2026-08-04｜CFO｜guidance：CFO 報 Q2 營收約 30 億美元，年增 37.7%（原話："revenues in Q2 were just over $3 billion, up 37.7%"）
- 2026-08-04｜CEO｜commitment：CEO 說明多年期採購承諾由 36 億增至約 97 億（原話："now almost tripling from a year ago at $3.6 billion"）
- 2026-08-04｜CFO｜commitment：CFO 報 Q2 末採購承諾 97 億美元，上季 89 億（原話："commitments at the end of the quarter were $9.7 billion"）
- 2026-08-04｜CEO｜commitment：CEO 對全年各項數字的口徑：不給 AI/校園新數字，但稱都會上調（原話："we can most certainly say all numbers are"）
- 2026-08-04｜CEO｜commitment：CEO 表示預期 1 到 2 個 10% 以上客戶（原話："I fully expect there to be 1, maybe 2 10%"）
- 2026-08-04｜CEO｜customer：CEO 說全年增幅 10 億美元以上，微軟與 Meta 仍為最長期夥伴（原話："we're going to increase the number by $1 billion or more"）
- 2026-08-04｜CEO｜customer：CEO 提到 Etherlink AI 客戶累計數（原話："now exceeds 100 cumulative customers"）
- 2026-08-04｜CEO｜customer：CEO 說 scale-across 已延伸至數家 Neocloud（原話："we're already seeing it apply to several Neoclouds"）
- 2026-08-04｜CEO｜customer：CEO 對核心資料中心前端的說法：不會持平（原話："it isn't going to be flat"）
- 2026-08-04｜CEO｜risk：CEO 稱供應鏈問題是產業性的兩年問題（原話："The industry is going to have a 2-year problem."）
- 2026-08-04｜CFO｜risk：CFO 說庫存可能出現高檔季度，影響營運現金流時點（原話："could result in quarters of elevated inventory balances"）
- 2026-08-04｜CFO｜risk：CFO 說明遞延收入波動來自客戶特定驗收條款增加（原話："increased customer-specific acceptance clauses"）
- 2026-08-04｜CFO｜risk：CFO 說指引依有把握取得供應的量來訂（原話："guiding based on what we're confident we can get the supply"）
- 2026-08-04｜CFO｜risk：CFO 說客戶能見度仍維持約兩季（原話："we still have the same kind of 2 quarters of"）
- 2026-08-04｜COO｜product：COO 說記憶體 2026 年供應已確保（原話："Our memory supply has been secured for 2026"）
- 2026-08-04｜COO｜product：COO 說已建立液冷供應鏈（原話："we've now established a liquid cooling supply chain"）
- 2026-08-04｜CEO｜product：CEO 說 1.6T 將於下半年試用，2027 才量產（原話："we will be in trials in the second half of this year"）
- 2026-08-04｜CEO｜product：CEO 說 1.6T 量產在 2027（原話："the real production will still be in 2027"）
- 2026-08-04｜CEO｜product：CEO 預估 2026 scale-across 市場規模約 30–40 億美元，將快速成長（原話："still maybe $3 billion to $4 billion"）
- 2026-08-04｜CEO｜competition：CEO 說白盒是戰術性方案，用於簡單情境（原話："white box is certainly a tactical solution"）
- 2026-08-04｜CEO｜competition：CEO 說在供應與人力稀缺下 Arista 系統級方案勝出（原話："Arista is really winning out with the system-wide approach"）
- 2026-08-04｜CEO｜competition：CEO 說 NVIDIA 場景（NVLink scale-up）轉換需要較長時間（原話："In the NVIDIA cases, it's going to take a bit longer."）
- 2026-08-04｜CEO｜competition：CEO 說 CPO 方面多數仍為可插拔光學與銅線（原話："will still remain pluggable optics and copper"）
- 2026-08-04｜CFO｜capital_allocation：CFO 說本季未回購股票（原話："repurchase our common stock."）
- 2026-08-04｜CFO｜capital_allocation：CFO 說 Santa Clara 擴建預計 2026 年底完工（原話："we expect construction to be completed by the"）

### 問答異常語氣（迴避／改口／保留）
- ANET_Q2_2026_Earnings_Call_20260804.md｜問：UBS Vogt：為何全年財測大幅上調但 AI 目標沒變、僅動校園｜答法：CEO 稱數字都會上調，但拒絕給具體數字，理由是看出貨組合
- ANET_Q2_2026_Earnings_Call_20260804.md｜問：Melius Reitzes：AI 實驗室客戶進展與第四季潛在 10% 客戶｜答法：CEO 改談安全網路研討會與模型多元，未直接回答客戶進展與 10% 客戶
- ANET_Q2_2026_Earnings_Call_20260804.md｜問：Wells Fargo Rakers：是否新增 10% 客戶、微軟與 Meta 是否仍為 10% 以上｜答法：CEO 只說預期 1 到 2 個 10% 客戶，並稱要保留彈性，未指名
- ANET_Q2_2026_Earnings_Call_20260804.md｜問：Raymond James Leopold：增加的 10 億美元來源組成｜答法：CEO 稱涵蓋所有產品線，出貨後才知道確切組成，未給拆分

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 2 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 1 | 1 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 1 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260805","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 基建超級週期持續，且 Arista 可服務的 scale-out／scale-across 段不被 scale-up 邊緣化"},{"id":"H2","text":"系統層贏單守得住 — Arista 在超大規模客戶的份額不被 NVIDIA 矽晶片、白牌 ODM 與客戶自有 NOS 結構性侵蝕"},{"id":"H3","text":"市場維持對 Arista 的成長溢價倍數 — 不 de-rate 至硬體同業區間"}],"extra_text":"假設 | vs Inception（2026-05-06，$146.65）累積漂移\nH1 | 🟢 兌現。Inception 時 FY26 指引 $10.5B、AI 目標 $3.25B→$3.5B；今日指引 $12.6B、AI $3.5B。總營收路徑大幅超前（+20%），但 AI 分項零漂移 — 累積漂移的方向是「總量超交付、AI 分項原地」。\nH2 | 🟡 削弱。Inception 時的疑慮是 Spectrum-X 已贏 Meta＋Oracle；今日 IDC 確認 NVIDIA 已取走資料中心乙太網第一，且 Meta 的 Minipack3N 白牌交換機直接建在 NVIDIA Spectrum-4 ASIC 上（Meta Engineering，2025-10-13）。份額壓力自「訂單層」下沉到「客戶內部矽來源層」。惟 Meta 同時仍在 DSF 架構中部署 Arista 7700R4，未見主體切換。\nH3 | 🔴 反向漂移（對持有人不利方向）。Inception 時 Fwd PE（FY+2）約 32x；今日 42.1x。股價 +43.5%，倍數擴張貢獻約三分之二。H3 從「假設」變成「已經被市場超額給付」 — 這正是本份裁決留在觀望的原因。"},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"大客戶內部矽來源替代：NVIDIA Spectrum ASIC 滲透進客戶自研白牌（Meta Minipack3N＝Spectrum-4 ASIC＋Accton 代工）、Microsoft 以自有 SONiC 取代 EOS 差異化（Azure 近七成 aggregation 交換機）。這比「訂單份額」更結構 — 即使營收金額仍成長，差異化正被壓回硬體層"},{"id":"R2","text":"AI 資本支出進入消化期 → 42x 倍數快速 de-rate。此風險的形狀是「基本面還好、股價先崩」，因為 H3 是三個假設中證據等級最低的一個"},{"id":"R3","text":"垂直整合參考系統繞過系統 OEM 層（本次新增）：Broadcom Tomahawk 6-Davisson（102.4Tbps CPO 交換器，自有 ASIC＋自有光引擎）自 2025-10-08 起已出貨。管理層在法說談的是「開放 CPO 2028-2029」，但非開放的垂直整合 CPO 整機今天就可以買 — 若超大規模業者願意直接採購晶片商參考系統，擠壓時點遠早於 2028"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(NTM) ≤ 35x（以現行 NTM EPS $4.61 計約 $161，隨共識上修同步上移）；週線布林中軌現位 $160.55 同區","irr_base_pct":3.9,"ev5y_pct":12.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":1.1,"ev5y_pct":12.0,"irr_base_pct":3.9,"max_dd_pct":-65.0,"bull_5y_price":421.0,"bear_5y_price":81.0,"p_bull_pct":22.0,"p_bear_pct":32.0,"rearm_trigger":"Fwd PE(NTM) ≤ 35x（以現行 NTM EPS $4.61 計約 $161，隨共識上修同步上移）；週線布林中軌現位 $160.55 同區","price_at_dd":210.51,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ANET","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Arista Networks"},"oneliner":"Arista 把 2027 年營收財測抬到約 185 億美元，股價卻比 8 月低 19%，FY2 本益比降到 30 倍；AI 需求與系統層優勢仍在，但份額被 Nvidia 超過、毛利率年減，適合分批，不宜一次買足。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺雲端巨頭與大型企業的網路預算，錢卡在交換器系統與 EOS 軟體這一節；上游有 Broadcom 與記憶體，下游有微軟與 Meta，兩頭都不弱。","reasoning":"Q3 FY2026 營收 36.58 億美元，年增 58.5%，GAAP 毛利率 63.6%，非 GAAP 營業利益率 49.1%。正式營收分部事實表未涵蓋；法說給的目標是 2026 年 AI 35 億美元、園區 12.5 億美元，其餘約 85.5 億美元由總數倒算，2027 年三塊約為 70 億、20 億、95 億美元。訂閱型服務與軟體在 Q4 2025 法說占營收約 17%，其餘主要是產品出貨。單點依賴有兩個：FY2025 前兩大客戶占 42%（26%、16%），主力晶片靠 Broadcom 且沒有書面保供。集中度是風險，不是護城河證據；2026-11-03 CEO 預期 10% 以上客戶增加到 3～4 家，方向改善，要等 FY2026 10-K 驗證。供需持久性：缺貨至少延續到 2027 年，屬結構性；需求高度靠客戶擴大資本支出，屬週期性，消化時會反轉。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi3_gaap_gross_margin","f_kpi8_deferred_revenue","f_kpi9_q4_fy2026_guidance_reven","f_earnings_recency"],"verdict_values":{"revenue_quality":"產品為主、服務約 17%（Q4 2025 法說）；AI 訂單帶客戶特定驗收條款，產品遞延收入隨新品波動，季度認列時點受驗收影響。","unit_econ_note":"Q3 銷售費用占營收 3%、行政費用 0.7%，研發 11.2%；法說口徑毛利率（判讀為非 GAAP，事實表 Q3 GAAP 為 63.6%）由 Q2 的 63.4% 回升到 64%，CFO 歸因於客戶組合，單位經濟的逐客戶資料事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"營業利益率近 50%、零負債、股本幾乎不膨脹，但需求綁在 AI 資本支出，營收節奏帶循環性。"},"industry":{"clock_phase":"III","sd_verdict_source":"零組件缺貨、廠商簽多年採購約（Arista 承諾 114 億美元）、S&P 預估 Meta 2026～2028 年自由營運現金流為負，需求強但資金來源開始吃緊，屬過熱期特徵；此判斷不看股價。供需持久性：缺貨到 2027 年屬結構性，需求高度屬週期性。","bargaining":{"up":"偏弱：Broadcom 為主要晶片來源且無保供合約，靠採購承諾換貨。","down":"偏弱：前兩大客戶占 42%，微軟與 Meta 同時採購他廠，並推 SONiC、FBOSS。","geo":"製造外包在馬來西亞、越南、墨西哥等地，關稅成本可能無法完全轉嫁。"},"profit_pool_dir":"利潤池往 AI 後端與跨資料中心骨幹移動；Nvidia 以 GPU 加網路的整套方案分走訓練叢集那一塊。五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"管理層 2030 年可觸及市場","value":"超過 2,000 億美元（2026-11-03 法說，管理層口徑，未經第三方驗證）"},{"item":"FY2026 營收財測占 2030 年市場","value":"約 6.7%（133 億÷2,000 億）"},{"item":"IDC 2Q26 資料中心乙太網路份額","value":"18.7%（1Q26 為 20.7%）"},{"item":"IDC 2Q26 整體乙太網路交換器份額","value":"13.4%"},{"item":"五年前份額、分段 CAGR、營業利益池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向維持不變：EOS 帶來的執行力仍在擴大，定價力穩定，但資料中心份額已被 Nvidia 超過，不能往上調。","reasoning":"機制是一套作業系統從資料中心延伸到園區，品質與不停機升級讓企業客戶換機成本高。可驗證的方向有三個。第一，對 Cisco 的 TTM 營業利益率 43.83% 比 25.36%，FCF 利潤率 42.2% 比 20.16%，毛利率 62.88% 卻略低於 64.52%，領先來自費用效率與規模；同業 ROIC 事實表未涵蓋，只能用利潤率代替。第二，IDC 資料中心份額 1Q26 為 20.7%，2Q26 為 18.7%，Nvidia 2Q26 為 20.4%，領先者份額下滑，方向不能上調。第三，公司 Q3 營收年增 58.5%，明顯加速，但 IDC 3Q26 份額要到 12 月左右才有。Nvidia 的攻擊集中在訓練叢集，屬客群範圍失守，不是整體方向受損；這項負面只記在威脅，不再重複扣方向。三件事分開看：當期屬高利益率、高周轉；四項持續期檢查三黃一綠，超額報酬撐過這輪建置的把握較高，五年後要看份額；增量報酬因投入資本接近零無法計算。反例：若 3Q26 份額繼續下跌，且微軟或 Meta 占比下降，方向就該改成縮減。","fact_refs":["f_peer_anet_gross_margin_pct","f_peer_anet_operating_margin_pct","f_peer_anet_fcf_margin_pct","f_peer_csco_gross_margin_pct","f_peer_csco_operating_margin_pct","f_peer_csco_fcf_margin_pct","f_peer_hpe_gross_margin_pct","f_peer_hpe_operating_margin_pct","f_peer_cien_gross_margin_pct","f_peer_cien_operating_margin_pct","f_peer_cls_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"單一作業系統 EOS 加 CloudVision，靠品質、低漏洞數、不停機升級與跨資料中心大型系統建立轉換成本；AI 時代再加上對多種加速器的中立性。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Q3 非 GAAP 營業利益率 49.1%，2026 年財測四度上調。定價力穩定：毛利率年減但仍在 62%～64% 區間，2026-08-04 CEO 說漲價效果要到年底或明年才反映。IDC 資料中心份額由 20.7% 降到 18.7%，領先者份額下滑，因此不往上調。","competitor_notes":[{"name":"Nvidia","strategy_note":"以 Spectrum-X 綁 GPU 整套銷售，1Q26 起資料中心乙太網路營收第一，並拿到 Meta 多年合約，是最大對手；利潤率資料事實表未涵蓋。"},{"name":"CSCO","strategy_note":"毛利率與 Arista 接近，營業利益率只有 25.36%，費用結構較重；Arista 在企業與園區搶的是長期主導者的存量。"},{"name":"HPE","strategy_note":"併入 Juniper 後規模變大，但毛利率 36.73%、研發密度 8.85%，都低於 Arista，短期較難靠研發追趕。"},{"name":"CIEN","strategy_note":"毛利率 44.07%、營業利益率 14.12%，獲利不在同一級；事實表沒有它與 Arista 直接競爭的證據。"},{"name":"CLS","strategy_note":"毛利率 11.46%，是代工型利潤結構，可當白牌路線的成本參照，與 Arista 不是同一層競爭。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，價差改用營業利益率與 FCF 利潤率。","threats":[{"level":"🔴","text":"Nvidia 以 Spectrum-X 綁 GPU 銷售，已居資料中心乙太網路第一，並進入 Arista 最大客戶之一的多年部署。","p":"40%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","competitive_share_entrants#4","end_markets#2","substitute_technology#2"]},{"level":"🟡","text":"白牌硬體加 SONiC、FBOSS，加上大型系統廠的垂直整合方案，讓大客戶保有多供應商議價力；2026-08-04 CEO 稱白牌是戰術性方案，適用簡單情境。","p":"30%","evidence_refs":["competitive_share_entrants#0","customer_second_source#0","customer_second_source#1","substitute_technology#0"]},{"level":"🟡","text":"下一代架構：CPO、NPO 與 NVLink 主導的 scale-up；管理層稱 CPO 要到 2028～2030 年，scale-up 2028 年才量產，若交付落後會失去位置。","p":"30%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是網路維運、決策者是基建主管、付款者是資本支出預算，三者都成立，AI 叢集不能沒有網路。急迫不等於持久：2026-11-03 CFO 說能見度仍是兩季，S&P 預估 Meta 2027 年資本支出超過 2,250 億美元，同時自由營運現金流為負。"},{"item":"決策層級","level":"🟡","text":"企業客戶以整張網路為決策單位，園區更新週期長，替代性低；大型雲端以網路分層為單位，微軟與 Meta 多供應商採購，替代性高。續約率、漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"稀缺在 GPU、交換晶片與記憶體，Arista 夾在 Broadcom 與大客戶之間，毛利率仍守住 62%～64%。採購承諾由 97 億增到 114 億美元，等於用承諾買供應；若 Nvidia 把網路併入整櫃方案，這段價值會被重新分配。"},{"item":"社會容忍度","level":"🟢","text":"屬企業採購的基礎設施，沒有民生定價壓力；FY2025 10-K 未點名針對 Arista 的反壟斷調查，近十二個月 8-K 也無重大項目。"}],"roiic":"無法計算：投入資本接近零或為負，增量資本的分母沒有意義，事實表也沒有歷年投入資本。","reinvest_rate":"TTM 接近零（FCF 利潤率 42.2% 高於稅後營業利益率約 34.6%）；Q3 單季約 69%（存貨增 7 億、遞延收入減約 1 億、資本支出 1.01 億美元，除以稅後營業利益 12.99 億美元，未計折舊與應收應付變動）。","endo_ceiling":null,"formula_note":"投入資本用 Q3 法說的存貨 32 億美元、DSO 59 天、應付 48 天與遞延收入 68.4 億美元粗算約 −20 億美元，未含固定資產（事實表未涵蓋），ROIC 算術失真。稅後營業利益率 34.6%＝43.83%×（1−21%），投入資本小於 TTM 營收時 ROIC 高於此數。"}}}},"q3_growth":{"verdict":"五年後跑道仍寬：份額不到兩成，園區與 scale-up 是有來源的下一條曲線；成長上限是供給與客戶預算，不是 Arista 的資金。","reasoning":"成長以量為主，來自 AI 部署與新客戶；2026-08-04 CFO 說毛利率尚未計入漲價，併購與回購也不是來源。共識 EPS 由 FY2025A 2.75 美元到 FY2028E 6.99 美元，三年年化 36.5%，但基期是 GAAP，共識口徑未標明；FY1 到 FY3 年化 27.8%。EPS 家數事實表未涵蓋，營收共識為 23 位分析師。內生上界無法計算，缺口也就無法量化，長期信心上限為中。可歸因的部分是：FY2025 到 FY2027 共識 EPS 年化 43.2%、營收年化 44.1%，成長來自營收本身，不是利潤率或回購。跑道估算：FY2027 約 185 億美元，以 25% 年增達到 2,000 億美元市場的 30%，約需 5.3 年，屬中等，且市場規模是管理層數字。成長熄火測試：三年後成長率降到 15%、10%、5%，以 FY2029E 8.4 美元配 22、17、13 倍，股價約 185、143、109 美元，對現價 +8%、−16%、−36%。十項衰退訊號亮兩項，另有六項未亮，提價後銷量與產業倍數走勢兩項資料不足。2027 年其餘業務由總數倒算只增約 11%，AI 倍增的基期還不可靠。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"以量為主：AI 部署與新客戶；價格尚未反映；併購與回購不是來源。","runway_years":5.3,"runway_post_y5":"🟢","endo_ceiling_basis":"增量 ROIC 乘再投資率的上界無法計算，因投入資本接近零或為負。實際上限是 114 億美元採購承諾能換到的供給、客戶資本支出與份額。","segments":[{"item":"AI fabrics","value":"FY2026 目標 35 億美元，FY2027 約 70 億美元（+100%，基期可能偏低）"},{"item":"園區","value":"FY2026 目標 12.5 億美元，FY2027 約 20 億美元（+60%）"},{"item":"其餘（資料中心前端、服務等）","value":"約 85.5 億美元到約 95 億美元（+11%，由總數倒算）"}],"decay_signals":["毛利率連兩季年減：Q2 63.4% 對 65.6%，Q3 64% 對 65.2%","核心市占縮減：IDC 資料中心份額 1Q26 20.7%、2Q26 18.7%，Nvidia 升至第一"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金配置中等偏保守：股本幾乎不膨脹、零負債，現金累積到 144 億美元，但回購動作少，併購與回購的報酬拿不到證據。","reasoning":"FCF／淨利 FY2024 為 1.29、FY2025 為 1.21，獲利轉現金沒有問題；2026 年前九月 FCF 37.93 億美元。Q3 股權獎勵 1.381 億美元，占營收 3.8%。稀釋股數由 FY2023 約 12.69 億（淨利÷稀釋 EPS 倒算）到 Q3 12.78 億，年化約 0.26%。現金去向：2026-08-04 CFO 說 Q2 未回購，2026-11-03 CFO 說 15 億美元授權尚餘 8.179 億美元；Q3 存貨增至 32 億美元，資本支出 1.007 億美元，採購承諾 114 億美元。三年現金去向四分比例事實表未涵蓋。Q3 營業現金流約 12 億美元，低於非 GAAP 淨利 15.3 億美元，CFO 歸因於刻意備貨。營業利益率由 FY2022 的 34.86% 升到 FY2025 的 42.82%，沒有營業利益成長落後營收的壓縮現象。","fact_refs":["f_kpi6_stock_based_compensation","f_kpi7_free_cash_flow","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近十二個月沒有重大併購；VeloCloud（2025-06-30 完成）的金額與貢獻事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與十年期公債殖利率事實表未涵蓋，無法判定；Q2 未回購，授權尚餘 8.179 億美元。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數 FY2023 約 12.69 億到 Q3 FY2026 12.78 億，年化約 0.26%，低於 1.5%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，近十二個月 8-K 沒有併購項目，這一欄不承重。"}}}},"q5_valuation":{"verdict":"現價要的是 FY2031 EPS 約 10.4 美元、終端 25 倍，五年年化才有 8.8%。FY2027 財測已走完前面一大段，這個要求我相信；想拿 15% 以上就要靠樂觀情境。","reasoning":"FY1 本益比 39.91 倍、FY2 30.3 倍；trailing 45.79 倍落在 4 個年度端點的 76.8 分位，不是五年分位。NTM EPS 約 5.44 美元（FY1 權重 14.6%、FY2 權重 85.4%），NTM 本益比約 31.4 倍，低於前份要求的 35 倍。淨現金 143.59 億美元約每股 11.4 美元，扣現金後 FY2 本益比 28.3 倍。財測推得 FY2027 EPS 約 5.9 美元（185 億×49%，加其他收入約 5.5 億，稅率 21%，12.8 億股），比 FY2 共識 5.64 美元高約 5%，我不把這 5% 當便宜的主要論據。FY1 最後一次快照下修 1.38%，與 Q3 大幅優於財測方向相反，較可能是彙整口徑雜訊；近 3 個月仍上修 4.14%。賣方目標價多在財報前：8 月均值約 238 美元、最高 289 美元，聚合站有 185 美元，最高對最低 289÷164 為 1.76 倍，現價低於均值支持分批方向，但資料偏舊。近端推算：12 個月以 FY2027E 5.9 美元配 33 倍為 195 美元，+14%；24 個月以 FY2028E 7.2 美元配 30 倍為 216 美元，+26.5%。同業本益比事實表未涵蓋。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_3m_fy1_pct","f_net_debt_m","f_shares_diluted_m","f_rev_consensus_fy2_m","f_ma_state","f_ma_w52"],"verdict_values":{"valuation":{"basis":"FY1 本益比為主，FY2 本益比與 PEG 輔助；終端倍數配終端當年度 EPS，與起點同口徑。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比，無法做倍數對照。"},"fwd_pe":39.91,"peg":1.09,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"由偏貴降到合理偏高：NTM 本益比由前份約 45.7 倍（210.51÷4.61）降到約 31.4 倍。PEG 1.09＝39.91÷36.5%，基期是 GAAP；換成 FY1 到 FY3 的 27.8% 則為 1.44，兩者都在 1～2 的合理區。基準情境五年年化 8.8%，屬中等。沒有到便宜，因為 trailing 本益比仍在 4 個年度端點的 76.8 分位，報酬也沒到 12%。五年分位所需資料事實表未涵蓋，留空。","upside_short_pct":14.0,"upside_mid_pct":26.5,"denominator_disputed":false,"denominator_note":"分母不是爭點。Q3 GAAP EPS 1.22 美元略高於非 GAAP 1.20 美元，差異含股權獎勵的稅務效果，未放大前瞻分母；財測推得 5.9 美元與共識 5.64 美元差約 5%，方向偏保守。"}}},"q6_how_wrong":{"verdict":"最可能看錯的不是今年的數字，而是 2028 年：AI 建置進入消化期時，114 億美元採購承諾、兩大客戶占四成營收與 30 倍本益比會同時反向。","reasoning":"壓力測試五項過三項。FY2027 營收少一成，EPS 約 5.1～5.4 美元，仍高於 FY1 的 4.28 美元，過關。毛利率掉到 60%，EPS 約少 6%，過關。最大客戶採購減半，營收約少 13%，仍賺錢，過關。採購承諾一半賣不掉，損失約 57 億美元，接近 FY2027 推算淨利的四分之三，不過關，但這是極端假設，因承諾含多年期合約。FY2 本益比壓到 20 倍，股價 113 美元，−34%，不過關。動能沒有過熱：RSI 43.36，26 週報酬 20.48%；4 週漂移事實表未涵蓋。歷史最大回撤與空方具體數字事實表未涵蓋，2026-08-04 法說有四題管理層未正面回答，都與 AI 組成或 10% 客戶有關，已併入矛盾裁定。","fact_refs":["f_price_at_dd","f_consensus_eps_fy2","f_kpi8_deferred_revenue","f_rsi14","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長真實但週期風險未消：毛利率連兩季年減、核心份額下滑兩項訊號亮起。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":4.28,"pe":39.91,"basis":"FY1（FY2026E）共識 EPS 4.28 美元、現價 170.8 美元；終端倍數同樣配終端當年度 EPS。"},"eps":{"bull":[6.4,8.6,10.8,13.0,15.0],"base":[5.9,7.2,8.4,9.5,10.4],"bear":[5.2,4.7,4.6,5.0,5.5]},"pe":{"bull":32,"base":25,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":8},"max_dd":{"lo":-60,"hi":-40,"basis":"下行情境谷底 FY2028 EPS 4.7 美元配 18～22 倍，約 85～103 美元，對現價 −50%～−40%；若先回到 8 月約 210 美元再跌，高點回撤約 −60%。歷史最大回撤事實表未涵蓋，此範圍由情境推算。","trigger_time":null},"basis":{"bull":"FY2027 營收約 200 億美元，超出財測 8%；2028 年 scale-up 量產、份額回到兩成以上，FY2031 營收約 500 億美元，占 2,000 億美元市場四分之一，營業利益率約 46%，成長約 15%，終端 32 倍。","base":"FY2027 依財測推得 5.9 美元；之後營收成長 25%、18%、14%、11%，FY2031 約 345 億美元；營業利益率由 49% 降到 45%，股本小幅增加，淨現金累積。終端 25 倍對應約 10% 成長；同業現值本益比事實表未涵蓋，無法做同業對照。","bear":"2028 年 AI 消化，FY2027 營收約 170 億美元，FY2028 年減約 5%，營業利益率降到 42% 左右；FY2031 EPS 5.5 美元，終端 17 倍採三年後成長率降到 10% 的錨。機率 30% 的依據是客戶集中 42%、能見度兩季、S&P 調降 Meta 展望與產業過熱；不高於基準，是因缺貨與長約至少撐到 2027 年。"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FY2025 前兩大客戶占 42%，前兩大經銷商占應收帳款 52%；S&P 2026-10-30 把 Meta 展望調負，預估 2026～2028 年自由營運現金流赤字 220 億、710 億、390 億美元。","assumption":"假設大型客戶願意繼續舉債擴建，2028 年仍維持高資本支出。","consequence":"五年後虧 50% 最可能的故事：2028 年消化，AI 營收年減，微軟或 Meta 移向 Spectrum-X，採購承諾變損失，本益比由 30 倍降到 17 倍。下行情境終端 93.5 美元，−45%。","ruling":"部分採納，下行機率定 30%。這個故事與唯一致命數字部分重疊，後者是它第一個可量化的訊號。S&P 同時預估 Meta 2027 年資本支出超過 2,250 億美元，近端需求反而支持財測，風險落在 2028 年以後。此信用訊號尚未反映在賣方下修上，因此第一批之後的加碼綁定 IDC 與 Q4 財報。","watch":"微軟與 Meta 資本支出指引；10-K 的 10% 客戶揭露；2028 年首版財測。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 毛利率 64% 低於去年同期 65.2%，FY2027 區間 62%～64%；業界分析認為記憶體缺口 2027 年可能惡化；Broadcom 無保供；關稅可能無法完全轉嫁；研發季增 47%。","assumption":"假設營收翻倍時，毛利率維持 62%～64%、營業利益率維持 49%。","consequence":"AI 贏了，但增量利潤被晶片、記憶體與整櫃夥伴分走。營業利益率每少 1 點，FY2027 EPS 約少 1.9%；降到 44% 約少 10%。","ruling":"採納。基準情境把營業利益率由 49% 逐年降到 45%，不外推當下高點；49% 中有多少屬缺貨期的週期性紅利無法精確拆分，這段不確定性放進下行機率。CFO 把研發跳升連到專案投入，CTO 稱原型費高，列為未證、監測；若研發占營收連兩季高於 11%，這個一次性說法視為不成立。","watch":"毛利率、研發占比、採購承諾與整櫃出貨模式揭露。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","supply_demand_durability#2","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"view":"價格已反映太多","evidence":"FY1 本益比 39.91 倍、trailing 45.79 倍；P/S 18.15 倍、EV/S 16.94 倍，都在 4 個年度端點的 70～77 分位；股價 26 週仍漲 20.48%。","assumption":"假設市場在成長降到 10% 左右時，仍願意給 25 倍。","consequence":"若終端只有 20 倍，基準情境終端 208 美元，五年年化約 4%。","ruling":"部分採納。FY2 本益比 30.3 倍、扣現金 28.3 倍，相對 38%～40% 的財測不算離譜；但基準報酬只有中等，所以只買第一批，不一次買足。","watch":"NTM 本益比 35 倍（約 190 美元）以上不追。","fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 210.51 → 本次 170.8（-18.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=210.51","side_b":"本次 price_at_dd=170.8","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 觀望 → 本次 進場","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=觀望","side_b":"本次 dca_verdict=進場","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 追蹤 → 本次 衛星","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=追蹤","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 210.51 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 210.51 美元：Bull 價 421、Bear 價 81，五年期望值 +12.0%，基準年化 3.9%，不對稱比 1.1","side_b":"本次情境、股價仍用 210.51 美元：Bull 價 480、Bear 價 93.5，五年期望值 +25.9%，基準年化 4.3%，不對稱比 1.92","ruling":"先換情境、股價不動：五年期望值多 13.9 個百分點，基準年化多 0.4 個百分點。不對稱比由 1.1 變為 1.92。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 210.51 美元：五年期望值 +25.9%，基準年化 4.3%，不對稱比 1.92","side_b":"本次情境、股價 170.8 美元：五年期望值 +55.2%，基準年化 8.8%，不對稱比 3.33","ruling":"再換股價、情境不動：起點價下跌 18.9%，五年期望值多 29.3 個百分點，基準年化多 4.5 個百分點，不對稱比由 1.92 升到 3.33。合計五年期望值比前份多 43.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與裁決隨股價變動","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 210.51 美元，NTM 本益比約 45.7 倍，估值偏貴，結論為觀望。","side_b":"本次：股價 170.8 美元，較前份 −18.9%；NTM 本益比約 31.4 倍，估值合理偏高。","ruling":"變動主要來自股價下跌與共識上修，不是風險消失。裁決與倉位以本次情境重新決定。","evidence_level":"事實表股價與共識。","settle_metric":"NTM 本益比"},{"axis":"價值陷阱評級由綠轉黃","cause":"新證據","prior_field":["trap"],"side_a":"前份：價值陷阱風險低。","side_b":"本次：毛利率連兩季年減，IDC 2Q26 資料中心份額再降到 18.7%，兩項衰退訊號亮起。","ruling":"採納新證據，評級調為黃色。營收、現金流與股本仍健康，尚未到紅色。","evidence_level":"公司法說原話與 IDC 第三方資料。","settle_metric":"毛利率年增減與 IDC 份額","if_then":["若毛利率連兩季低於 62%，則減碼三分之一。","若 3Q26 份額回到 18.7% 以上且毛利率年減幅收斂，則維持分批計畫。"],"evidence_refs":["competitive_share_entrants#3","end_markets#2"]},{"axis":"維持不變的基本面欄位","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合評等為第二級，護城河方向不變，五年後跑道寬，屬品質複利型，未標循環位置。","side_b":"本次全部維持：Q3 財報與 2027 年財測偏正面，IDC 份額與毛利率偏負面，兩邊相抵。","ruling":"估值改善，但護城河仍是 B、長期信心為中、基準報酬只有中等，綜合評等不上調。園區目標 60% 成長與 2028 年 scale-up 支持跑道維持寬。","evidence_level":"法說與事實表。","settle_metric":"IDC 3Q26 份額；FY2026 Q4 財報"},{"axis":"重新進場門檻已達成","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE(NTM) ≤ 35x（以現行 NTM EPS $4.61 計約 $161，隨共識上修同步上移）；週線布林中軌現位 $160.55 同區","side_b":"NTM 本益比 ≤35 倍（現約 31.4 倍，約 190 美元內）可建首批；IDC 3Q26 份額 ≥18.7% 且年底遞延收入年增才加碼。","ruling":"倍數門檻 35 倍不變，舊門檻已達成，價格錨因 NTM EPS 由 4.61 上修到約 5.44 美元而由 161 美元移到約 190 美元。布林中軌資料本次沒有，取消這個錨。新增份額與遞延收入作為加碼條件。","evidence_level":"事實表共識與股價推算。","settle_metric":"NTM 本益比","if_then":["若股價先漲過約 190 美元，而 IDC 與年底遞延收入都還沒驗證，則不追。","若股價跌破 52 週均線 157.84 美元，且基本面門檻都沒觸發，則分批反買。"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份無唯一致命點（欄位為空）。","side_b":"2027 年 11 月法說給出的 2028 年首版營收成長指引低於 15%。","ruling":"本次依新格式首次設定。選這個數字是因為它同時反映 AI 消化、大客戶移轉與份額流失，也是敏感度最大的一項。","evidence_level":"判斷，依情境敏感度推算。","settle_metric":"FY2028 首版營收成長指引"},{"axis":"減碼與清倉門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份無此項門檻（欄位為空）。","side_b":"毛利率連兩季低於 62% 減碼三分之一；2028 年首版成長低於 15% 減碼至半倉；微軟或 Meta 占比跌破 10% 且營收成長低於 15% 清倉。","ruling":"本次依新格式首次設定，以財測下緣與情境敏感度定門檻。","evidence_level":"判斷，門檻來自公司財測區間。","settle_metric":"毛利率、首版財測、10-K 客戶占比"},{"axis":"AI 目標與管理層 8 月說法","cause":"新證據","side_a":"2026-08-04 CEO 稱 AI 目標至少 36 億美元，並說各項數字都會上調。","side_b":"2026-11-03 CFO 回答 AI 仍是 35 億美元、園區 12.5 億美元，全年營收卻由約 126 億上調到 133 億美元；CEO 說實際數字要等年底出貨後才知道。","ruling":"可調和，屬揭露保守，不是需求落差。但 AI 倍增到 70 億美元的基期不可靠：若 2026 年實際 AI 高於 35 億美元，2027 年成長就低於 100%。我只採信總營收 185 億美元，不採信倍增這個說法。","evidence_level":"法說原話，基期待 Q4 揭露。","settle_metric":"FY2026 實際 AI 營收與 2027 年 AI 目標是否同步上修","if_then":["若 FY2026 AI 營收 ≥45 億美元，而 2027 年目標仍是 70 億美元，則停止加碼。","若 FY2026 AI 營收在 35～45 億美元，且 2027 年目標維持或上調，則依計畫加第二批。"]},{"axis":"遞延收入與營收加速","cause":"新證據","side_a":"Q3 營收季增 20.5%，2027 年財測 38%～40%，管理層稱需求是任內最好。","side_b":"遞延收入由約 69 億降到 68.4 億美元，產品遞延收入季減 8,600 萬美元；Bank of America 分析師問兩者是否脫鉤，CEO 未給拆分。","ruling":"可調和。CFO 說流進流出都大，並預期年底餘額高於去年底。這個說法列為未證、監測，不採信也不否定。","evidence_level":"法說原話；2025 年底餘額事實表未涵蓋。","settle_metric":"FY2026 年底遞延收入對 FY2025 年底","if_then":["若年底餘額低於去年底，則停止加碼。","若年底餘額高於去年底，且 Q4 營收達 39 億美元以上，則加第二批。"]},{"axis":"採購承諾與能見度","cause":"新證據","side_a":"2026-11-03 CFO 稱能見度兩季，下半年靠客戶對話與趨勢推估；COO 也說不是每筆訂單都已下。","side_b":"採購承諾 114 億美元（季增 17.5%）、存貨 32 億美元（季增 28%），都快過 Q4 財測季增約 8%，且含多年期記憶體協議。","ruling":"可調和但風險不對稱：缺貨時多訂是理性，消化時就變損失。114 億美元約為 FY2027 推算銷貨成本 68 億美元的 1.7 倍，雖含多年期，仍是最大的表外風險。存貨增速減營收增速，Q3 為 7.5 個百分點。","evidence_level":"法說原話與推算。","settle_metric":"存貨季增率減營收季增率","if_then":["若差距連兩季超過 10 個百分點，則停止加碼。","若 Q4 差距回到 5 個百分點內且營收達標，則維持分批計畫。"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"份額下滑與營收加速","cause":"新證據","side_a":"IDC：Nvidia 自 1Q26 居資料中心乙太網路第一，Arista 份額由 20.7% 降到 18.7%，Meta 與 Nvidia 簽多年合約。","side_b":"Arista：Q3 年增 58.5%，上市以來最快；Etherlink 客戶超過 100 家；7800 跨資料中心平台差異化；企業持續搶份額。","ruling":"可調和：市場擴張且分層。Nvidia 拿 GPU 綁定的訓練叢集，Arista 拿跨資料中心骨幹與企業，份額下降沒有傷到絕對金額。一個季度的變動可能來自出貨時點，所以方向不下調，但列為首要風險。","evidence_level":"第三方季度資料，一季變動。","settle_metric":"IDC 資料中心份額，3Q26 約 2026 年 12 月","if_then":["若 3Q26 與 4Q26 連兩季低於 17%，則停止加碼，護城河方向改為縮減。","若 3Q26 回到 18.7% 以上，則加第二批。"],"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","competitive_share_entrants#4","end_markets#2"]},{"axis":"產業態勢三軸","cause":"新證據","side_a":"競爭惡化：Nvidia 升至第一，白牌與客戶自有作業系統保持壓力。","side_b":"結構轉好：AI 網路由 InfiniBand 轉向乙太網路，加速器變多有利中立供應商，管理層稱 2030 年市場超過 2,000 億美元。","ruling":"雙向拉鋸。其他結構變數中，記憶體缺貨與關稅是主要壓力，反壟斷與通路未見結構變動。","evidence_level":"IDC、10-K、10-Q 與法說。","settle_metric":"IDC 份額與毛利率","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#2","reg_tariff_export#2"]},{"axis":"買賣兩方最強論證","cause":"價格變動","side_a":"現在就買的最強論證：股價比 8 月低 19%，而 2027 年財測高出街頭 10%～15%，FY2 本益比 30 倍已低於前份進場門檻，公司今年四度上調財測。","side_b":"現在就賣的最強論證：這可能是週期高點的獲利。缺貨、長約、漲價與客戶舉債同時出現，兩季能見度卻給了全年財測，份額還在流失。","ruling":"先買三分之一。買方論證有硬數據，賣方論證要到 2028 年才能驗證；但賣方論證無法排除，所以後兩批綁定具名事件。","evidence_level":"事實表與法說，週期判斷不可裁決至 2027 年 11 月。","settle_metric":"FY2028 首版營收成長指引","if_then":["若 2028 年首版成長低於 15%，則減碼至半倉。","若首版成長 ≥20%，且毛利率守住 62%，則維持持股。"]},{"axis":"牛熊機率與最大回撤重新推算","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：牛熊機率 22／32，最大回撤 −65%。","side_b":"本次：牛熊機率 25／30，最大回撤範圍 −40%～−60%。","ruling":"這三欄是情境重建後的判斷，不是股價下跌的機械結果。樂觀機率上調 3 點，依據是 2027 年營收財測約 185 億美元，推得 EPS 約 5.9 美元，比 FY2 共識 5.64 美元高約 5%，差距不大，所以只上調 3 點；下行機率由 32 降到 30，降幅有限，因風險落在 2028 年以後。回撤範圍改由下行情境推算：谷底 FY2028 EPS 4.7 美元配 18～22 倍，約 85～103 美元，對現價 −50%～−40%；若先回到 8 月約 210 美元再跌，約 −60%。對現價的部分會隨起點價下跌而變淺，不代表風險變小。","evidence_level":"機率為判斷，回撤範圍由情境推算；歷史最大回撤事實表未涵蓋。","settle_metric":"FY2028 首版營收成長指引"}],"triggers":[{"n":1,"text":"NTM 本益比在 35 倍以內，先買第一批，目標倉位的三分之一。","type":"估值rearm","maps_to":"H1","metric":"NTM 本益比","threshold":"≤35 倍（現約 31.4 倍，約 190 美元內）","action":"建第一批三分之一","source_freq":"共識與股價，每週","date":"2026-11"},{"n":2,"text":"IDC 3Q26 份額止穩，且 FY2026 年底遞延收入高於 2025 年底，加第二批。","type":"加碼","maps_to":"H2","metric":"IDC 資料中心份額；年底遞延收入","threshold":"份額 ≥18.7% 且遞延收入年增","action":"加第二批至目標倉位三分之二","source_freq":"IDC 每季；公司季報","date":"2027-02"},{"n":3,"text":"股價跌破 52 週均線，但基本面門檻都沒觸發，用最後一批反買。","type":"加碼","maps_to":"R2","metric":"週收盤價","threshold":"<157.84 美元（均線隨時間移動），且第 4、5、6、7 條未觸發","action":"分批反買第三批","source_freq":"週線","date":null},{"n":4,"text":"IDC 份額連兩季低於 17%，不再加碼，護城河方向改為縮減。","type":"風險","maps_to":"R1","metric":"IDC 資料中心乙太網路份額","threshold":"連兩季 <17%","action":"停止加碼","source_freq":"IDC 每季","date":"2027-03","evidence_refs":["competitive_share_entrants#3","end_markets#2"]},{"n":5,"text":"毛利率連兩季低於財測下緣，視為成本轉嫁失敗。","type":"減碼","maps_to":"R3","metric":"非 GAAP 毛利率","threshold":"連兩季 <62%","action":"減碼三分之一","source_freq":"季報","date":"2027-05","evidence_refs":["reg_tariff_export#2","supply_demand_durability#2"]},{"n":6,"text":"存貨成長連兩季明顯快過營收，採購承諾開始變成負擔。","type":"風險","maps_to":"R2","metric":"存貨季增率減營收季增率","threshold":"連兩季 >10 個百分點（Q3 為 7.5）","action":"停止加碼","source_freq":"季報","date":"2027-05"},{"n":7,"text":"2027 年 11 月法說給的 2028 年首版營收成長低於 15%。","type":"Single Thing","maps_to":"Single Thing","metric":"FY2028 首版營收成長指引","threshold":"<15%","action":"減碼至半倉","source_freq":"公司法說","date":"2027-11"},{"n":8,"text":"微軟或 Meta 任一家占營收跌破 10%，同時公司營收成長低於 15%，論點失效。","type":"清倉","maps_to":"H2","metric":"10-K 前兩大客戶占比；營收年增","threshold":"任一家 <10% 且營收年增 <15%","action":"清倉","source_freq":"10-K 每年","date":"2028-02","evidence_refs":["customer_concentration_credit#0"]},{"n":9,"text":"NTM 本益比回到 42 倍以上且獲利預估未同步上修，賣掉部分倉位；前份偏貴時約為 45.7 倍。","type":"減碼","maps_to":"H1","metric":"NTM 本益比","threshold":"≥42 倍","action":"減碼三分之一","source_freq":"共識與股價，每週","date":null},{"n":10,"text":"FY2027 累計營收相對 185 億美元路徑落後 5%，暫停加碼。","type":"假設驗證","maps_to":"H1","metric":"FY2027 累計營收對財測路徑","threshold":"連兩季落後 ≥5%","action":"停止加碼","source_freq":"季報","date":"2027-08"},{"n":11,"text":"FY2026 Q4 財報當週重跑完整判斷。","type":"複審日期","maps_to":"H1","metric":"FY2026 Q4 財報與 2027 年分段財測","threshold":"不適用","action":"重跑完整判斷","source_freq":"法說","date":"2027-02"}],"kill_metrics":[{"metric":"FY2028 首版營收成長指引","bear_threshold":"<15%","window":"2027 年 11 月法說","source":"公司法說","last_status":"unknown"},{"metric":"非 GAAP 毛利率","bear_threshold":"連兩季 <62%","window":"2026 Q4 起逐季","source":"公司季報","last_status":"ok"},{"metric":"IDC 資料中心乙太網路份額","bear_threshold":"連兩季 <17%","window":"每季，約落後一季","source":"IDC 季度追蹤","last_status":"warning"},{"metric":"存貨季增率減營收季增率","bear_threshold":"連兩季 >10 個百分點","window":"每季","source":"公司季報與法說","last_status":"ok"},{"metric":"微軟或 Meta 占營收比重","bear_threshold":"任一家 <10% 且營收年增 <15%","window":"每年 10-K","source":"SEC 10-K","last_status":"ok"}],"action_conditions":{"rearm_trigger":"NTM 本益比 ≤35 倍（現約 31.4 倍，約 190 美元內）可建首批；IDC 3Q26 份額 ≥18.7% 且年底遞延收入年增才加碼。","exec_line":"現價附近買目標倉位的三分之一；IDC 3Q26 與 FY2026 Q4 財報都過關再加三分之一；股價跌破 52 週均線且基本面門檻未觸發，用最後三分之一反買；漲過 NTM 35 倍（約 190 美元）不追。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Nvidia 在訓練叢集的勝利外推到整個資料中心與園區，股價比 8 月低 19%；但 Q3 營收年增 58.5%，份額下降沒有傷到絕對金額，FY2 共識 5.64 美元也低於財測推得的約 5.9 美元，差約 5%。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"AI 後端與跨資料中心網路需求撐住 2027 年財測。","2y":"FY2027 營收 ≥180 億美元，AI fabrics ≥65 億美元。","5y":null,"10y":null,"threshold":"FY2027 營收 ≥180 億美元；AI fabrics ≥65 億美元","source":"公司季報與法說，每季","drift_rule":"累計營收相對 185 億美元路徑，連 2 季偏離 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉。"},{"id":"H2","text":"Nvidia 拿走訓練叢集份額，但 Arista 在跨資料中心骨幹、前端與企業仍靠 EOS 勝出，五年內資料中心乙太網路份額不跌破 15%。","2y":null,"5y":"FY2031 資料中心份額 ≥15%，前兩大客戶維持 10% 以上，或由新客戶補上。","10y":null,"threshold":"IDC 資料中心份額近端 ≥17%，五年 ≥15%","source":"IDC 季度追蹤；10-K 客戶集中度","drift_rule":"份額相對門檻連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉。"},{"id":"H3","text":"園區與企業資料中心形成第二條曲線，AI 消化期時整體營收不會年減。","2y":null,"5y":"FY2030 園區營收 ≥40 億美元。","10y":null,"threshold":"FY2027 園區 ≥20 億美元，FY2030 ≥40 億美元","source":"公司法說與年報；若停止揭露則標資料缺口","drift_rule":"園區營收相對路徑連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉。"}],"R":[{"id":"R1","text":"Nvidia 與白牌路線侵蝕大客戶份額：Spectrum-X 進到 Meta，微軟與 Meta 用 SONiC、FBOSS 保持多供應商。","h_ref":"H2","clock":"🔥","threshold":"IDC 資料中心份額連兩季 <17%，或 10-K 揭露任一大客戶占比跌破 10%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","competitive_share_entrants#3","competitive_share_entrants#4","customer_second_source#0","customer_second_source#1","substitute_technology#0","substitute_technology#2","end_markets#2"]},{"id":"R2","text":"AI 資本支出進入消化期：客戶集中、能見度兩季，採購承諾與存貨在高點時需求反轉。","h_ref":"H1","clock":"⚡","threshold":"FY2028 首版營收成長 <15%，或存貨季增減營收季增連兩季 >10 個百分點","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R3","text":"供應與成本壓縮毛利率：記憶體缺貨、Broadcom 依賴、關稅無法完全轉嫁，製造地也暴露在貿易措施下。","h_ref":"H1","clock":"🔥","threshold":"毛利率連兩季 <62%","evidence_refs":["supply_demand_durability#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R4","text":"產品世代與架構替代：CPO、NPO 與 NVLink 主導的 scale-up；2026-11-03 CEO 稱 CPO 要到 2028～2030 年，scale-up 2028 年量產，交付落後會失去位置。","h_ref":"H2","clock":"🐢","threshold":"2028 年底 scale-up 仍未量產；CPO 滲透率事實表未涵蓋，屆時以法說與第三方追蹤為準","evidence_refs":["substitute_technology#1","competitive_share_entrants#1"]}],"single_thing":{"description":"2027 年 11 月法說給出的 2028 年首版營收成長指引低於 15%（若公司延續今年提前給隔年財測的做法）。","why_fatal":"這個數字同時反映 AI 消化、大客戶移轉與份額流失。FY2028 營收每少 10%，EPS 約少 12%，再疊加本益比由 30 倍降到 20 倍以下，股價可跌 40%～50%；相較之下毛利率每少 1 點，EPS 只少約 2%。","if_happens":"減碼至半倉；若同時有大客戶占比跌破 10% 且營收成長低於 15%，則清倉；不再用 2028 年以後的 scale-up 當續抱理由。","how_monitor":"領先指標看採購承諾（114 億美元）、存貨周轉（1.6）、產品遞延收入、微軟與 Meta 資本支出指引及 IDC 份額；事件日約在 2027 年 11 月第一週。","probability":"25%（12～24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":30.28,"peg_fy2":1.09,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.75,"FY2026E":4.28,"FY2027E":5.64,"FY2028E":6.99},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin 共識快照，事實表未標明 GAAP 或非 GAAP；FY2025A 只有 GAAP 稀釋 EPS 可引用，三年年化 36.5% 可能偏高。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"IDC 公布 3Q26 乙太網路交換器追蹤（依前兩季時點推估）","impact":"高","watch":"Arista 資料中心份額是否回到 18.7% 以上，與 Nvidia 的差距"},{"date":"2026-12","date_precision":"month","type":"product","event":"Arista 年度最大客戶活動","impact":"低","watch":"園區進展與 AVA 定價模式"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 Q4 財報與 10-K","impact":"高","watch":"FY2026 實際 AI 營收、年底遞延收入、10% 以上客戶家數"},{"date":"2027-11","date_precision":"month","type":"guidance","event":"FY2027 Q3 法說，預期給出 2028 年首版財測","impact":"高","watch":"2028 年營收成長是否低於 15%"}],"decision_out":{"role":"衛星","row_hit":"9","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Nvidia 在訓練叢集的勝利外推到整個資料中心與園區，股價比 8 月低 19%；但 Q3 營收年增 58.5%，份額下降沒有傷到絕對金額，FY2 共識 5.64 美元也低於財測推得的約 5.9 美元，差約 5%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=20.48, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"verdict":"進場"}}
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
