你是 DD 管線 v20 的判斷層閘（gate），標的 LEU（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（49 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝55.5 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income (loss)＝-24.0 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_kpi2_gaap_operating_income_lo`（q1_business）｜GAAP operating income (loss)＝-29.7 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_kpi3_gross_profit_loss`（q1_business）｜Gross profit (loss)＝-10.6 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_kpi4_gaap_net_income`（q1_business）｜GAAP net income＝31.6 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_kpi5_free_cash_flow_derived`（q1_business）｜Free cash flow (derived)＝-126.0 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）；Q2 8-K https://www.sec.gov/Archives/edgar/data/0001065059/000162828026053433/ex991-10q2026_08x05.htm（上半年累計值）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_kpi7_cash_and_cash_equivalent`（q1_business）｜Cash and cash equivalents＝2236.1 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_kpi8_total_backlog`（q1_business）｜Total backlog＝7.0 US$B｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_kpi9_guidance_fy2026_revenue`（q1_business）｜Guidance FY2026 revenue＝450–500 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-04 date｜期間與口徑：2026-11-04／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-04）
- `f_peer_leu_gross_margin_pct`（q2_moat）｜LEU 毛利率＝23.28 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEU.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_leu_operating_margin_pct`（q2_moat）｜LEU 營業利益率＝-1.25 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEU.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_leu_fcf_margin_pct`（q2_moat）｜LEU FCF 利潤率＝-65.02 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEU.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ccj_gross_margin_pct`（q2_moat）｜CCJ 毛利率＝25.49 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CCJ.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ccj_operating_margin_pct`（q2_moat）｜CCJ 營業利益率＝14.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CCJ.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ccj_fcf_margin_pct`（q2_moat）｜CCJ FCF 利潤率＝10.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CCJ.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_uec_gross_margin_pct`（q2_moat）｜UEC 毛利率＝45.36 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UEC.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_uec_operating_margin_pct`（q2_moat）｜UEC 營業利益率＝-357.65 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UEC.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_uec_fcf_margin_pct`（q2_moat）｜UEC FCF 利潤率＝-288.16 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UEC.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bwxt_gross_margin_pct`（q2_moat）｜BWXT 毛利率＝22.61 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWXT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_bwxt_operating_margin_pct`（q2_moat）｜BWXT 營業利益率＝9.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWXT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_bwxt_fcf_margin_pct`（q2_moat）｜BWXT FCF 利潤率＝10.34 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWXT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.7 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝4.44 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.73 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝476.09 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝503.04 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi6_sbc_adjustment_sg_a_and_`（q4_capital）｜SBC adjustment (SG&A) and % of revenue＝1.3 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.centrusenergy.com/news-releases/news-release-details/centrus-reports-third-quarter-2026-results（全文以 SEC 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001065059/000162828026070229/ex991-10q2026_11x04.htm 核對）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：查無（未取得可核實的季度共識）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-1057.3 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 1178.8、現金 2236.1（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝20.62 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝104.6 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝28.27 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 3.7，分子＝快照價 104.6｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝31.04 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝36.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝36.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.75 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝28.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝28.9 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.42 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝8.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝8.1 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝2.31 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝1099.39 USD m｜期間與口徑：2026-11-08／市值 2156.69 ＋ 淨負債 -1057.3｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（3.7 → 3.7）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝7.56 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 3.44 → 3.7（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 104.6 / W52 196.58 / W104 176.23 / W250 97.82 / W250 13週斜率 0.98%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝196.58 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝176.23 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝97.82 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-49.55 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝42.42｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（25 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：BWXT 揭露將申請新濃縮設施執照；UBS 預期競爭壓力在 2030 年代後期累積；General Matter 在肯塔基設濃縮廠（搜尋摘要，未核原文）。
  - 來源：Yahoo Finance: UBS Flags Competitive Headwind for Centrus Energy; Energy Intelligence（as_of 2026-02-01）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：2025年前十大核燃料客戶占總營收約77%，前兩大客戶約31%；客戶減購或財務狀況變化可能影響業績。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：同來源：全球濃縮供給至少到 2030 年代初期仍超過需求（對濃縮廠商偏負面的供需說法，與 LEU 管理層『供需失衡擴大』說法並存）
  - 來源：World Nuclear News: Investment decisions needed to avoid fuel cycle supply gaps（as_of 2025-09-05）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：俄羅斯 TENEX 供貨受制裁、關稅、出口管制與俄方法令影響；加拿大運輸許可證延至 2027 年 3 月，進一步限制可能對業務造成重大負面影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Section 232 關鍵礦物（含鈾）調查後，2026-01-14 公告 11001 要求 180 天談判，視結果可能再考慮加徵部門關稅。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-11）｜affects：thesis.R、triggers
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：2026 年 10-Q 稱至 2027 年預計交付客戶的 LEU 逾半來自 TENEX 合約；未承諾量的豁免是否核准不確定（搜尋摘要，未讀頁面）。
  - 來源：SEC EDGAR 10-Q Q3 2026（搜尋摘要）（as_of 2026-09-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Centrus 依賴與俄羅斯 TENEX 的供應合約履行交貨義務，10-Q 自述此依賴為重大風險
  - 來源：Centrus Form 10-Q (period 2026-09-30)（as_of 2026-11-05）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：DOE 2024 年豁免僅涵蓋已承諾對美國客戶的交貨；2026-2027 未承諾交貨的豁免決定被延後
  - 來源：World Nuclear News / mining.com（as_of 2024-07-19）｜affects：thesis.R、triggers
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 LEU segment revenue $31.8M vs $44.8M (-29%), attributed to contract mix shift; total revenue $55.5M vs $74.9M; contingent LEU+HALEU enrichment backlog $5.4B
  - 來源：Centrus Q3 2026 results (SEC 8-K ex99.1 / oilprice coverage)（as_of 2026-11-04）｜affects：thesis.R、valuation
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Q3 2026 SWU average price +10%, volume +19%; LEU segment revenue down 29%
  - 來源：Centrus Reports Third Quarter 2026 Results（as_of 2026-11-04）｜affects：thesis.R
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：DOE does not currently plan to exercise further options under HALEU operation contract; FY2027 budget omits HALEU cascade funding
  - 來源：Centrus Q2 2026 earnings call highlights (MarketBeat)（as_of 2026-08-08）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：GLE 雷射濃縮（SILEX）：NRC 於 2025-08 受理完整執照申請，2026-03 發布 EIS 草案，首次商業生產目標約 2030 年；2026-01 DOE 選定其最高 2850 萬美元獎助。雷射法被稱有效率與成本潛力，但數十年來未在全球達商業規模。
  - 來源：搜尋摘要彙整（ANS、Energy Intelligence、SMR Intel）（as_of 2026-03-31）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 2026 調整後每股虧損 0.46 美元，遠差於共識約 -0.13（二手摘要）；營收約 5,550 萬美元，與預期約 5,520 萬相近；GAAP 獲利來自認股權證負債重估利益 4,640 萬
  - 來源：247wallst / oilprice 對 Q3 2026 的報導（搜尋摘要）（as_of 2026-11-04）｜affects：valuation、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2026-09-09 公司與 Guggenheim 簽承銷協議，發行 50 萬股普通股、預融資認股權證（最多 2,005,513 股）及普通認股權證（最多 6,992,382 股），有稀釋效果。
  - 來源：SEC EDGAR 8-K（Item 1.01）（as_of 2026-09-11）｜affects：valuation、decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露 McGlone 等人 2019 年起對 Centrus 等 DOE 承包商提起的 Portsmouth 場址外污染集體訴訟仍在進行。
  - 來源：SEC EDGAR 10-K FY2025（Note 17 Legal Matters）（as_of 2026-02-11）｜affects：decision_inputs.bear
- `major_events#4`（major_events｜方向 -｜狀態 ok）：2025-12-01 8-K 含 Item 3.01（上市規則未達標通知）；近 12 個月共 20 份 8-K，其中 14 份含重大項目。
  - 來源：SEC EDGAR 8-K 申報清單（as_of 2025-12-01）｜affects：triggers、decision_inputs.bear
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Urenco USA 現行 70 萬 SWU 擴建：2026 年 6 月底前五組 cascade 上線，2027 初再三組；另一座 210 萬 SWU 新廠預計 2029 動工、2032 首產（搜尋摘要轉述，未核原文）
  - 來源：ANS / Urenco USA news (2026-06)（as_of 2026-06-02）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#1`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Orano Georges Besse II 由 7,500 擴至 10,000 tSWU/y，預計 2028 起生產；Urenco Almelo 2030 前升至約 6,600 tSWU/y（二手來源轉述）
  - 來源：fissilematerials.org, Plans to expand the enrichment capacity（as_of 2026-06-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#4`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Urenco USA 擴建過半、第四組 cascade 上線
  - 來源：Urenco USA news（as_of 2026-06-01）｜affects：thesis.R
- `cyclical_inventory_price_position#2`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：Centrus 2026 Q3 業績（11/4）：營收 55.5 百萬美元（去年同期 74.9）、LEU 部門 31.8 百萬、調整後淨損 9.4 百萬
  - 來源：Centrus Q3 2026 results (SEC 8-K ex99.1)（as_of 2026-11-04）｜affects：valuation、thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：EIA 資料：鈾現貨 2016 年由 1 月 $34.65/lb 跌至 11 月 $17.75/lb，為 2004 年 5 月以來最低月均價；2016–2020 平均低於 $25/lb；美國鈾精礦產量 2014–2016 年減少 40%。
  - 來源：U.S. EIA, Today in Energy (id=31772)（as_of 2017-01-01）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：現貨自 2007 年 6 月高點約 $135/lb 起大致下行；2011 年福島前高點約 $73，其後跌逾一半，2016 年底跌至約 $18（較 2011 年 3 月低約 70%），低迷歷時約 5–9 年（依起點 2011 或 2007）。
  - 來源：Bloomberg via republicofmining / Business Day: World's worst commodity is radioactive for investor portfolios（as_of 2017-01-06）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Centrus 上一輪下行期：2016 全年毛利 $45.1M／營收 $311.3M，毛利率 14.5%（2015 為 16.5%、毛利 $68.9M），淨損 $67.0M；2017 上半年毛損 $6.8M（2016 同期毛利 $21.3M），2017 全年毛利回升至 $56.8M，其中 contract services 毛損 $2.5M。
  - 來源：Centrus Energy 10-K FY2016 / FY2017 and 8-K (SEC)（as_of 2018-03-01）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Centrus 2016 毛利 $45.1M、14.5%
  - 來源：Centrus 8-K Mar 2017（as_of 2017-03-28）｜affects：thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：McGlone 等人 2019 年起的 Portsmouth 污染集體訴訟仍列於 FY2025 10-K；搜尋未見證券詐欺集體訴訟。
  - 來源：SEC EDGAR 10-K FY2025（Note 17 Legal Matters）（as_of 2026-02-11）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":325.0,"bear_5y_price":28.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":43.4,"ev5y_pct":50.2,"irr_base_pct":7.5,"asym_ratio":2.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.7,"pe":28.27,"basis":"FY2026E 共識 EPS 3.70 美元為分母，股價 104.6 美元；與終端倍數同為當年度前瞻口徑，EPS 分母品質有爭議。"},"eps":{"bull":[4.8,4.5,5.0,8.5,13.0],"base":[3.9,3.1,2.6,4.6,7.5],"bear":[2.8,1.2,0.3,0.9,2.0]},"pe":{"bull":25,"base":20,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0},"second_stage":{"bull_cagr_pct":18,"base_cagr_pct":12},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LEU_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Amir Vexler (CEO)｜guidance：CEO 重申 2026 全年營收指引 4.5 億至 5 億美元與資本支出 3.5 億至 5 億美元。（原話："We are reaffirming our 2026 annual guidance for total"）
- 2026-08-06｜Amir Vexler (CEO)｜guidance：Piketon 2026 年淨新增員工指引由 100 以上上調至 175 以上。（原話："from over 100 net new employees to over 175 net new"）
- 2026-08-06｜Todd Tinelli (CFO)｜guidance：CFO 表示不提供逐季指引，也不提供 2026 年以後的資本支出指引。（原話："We're not going to provide"）
- 2026-08-06｜Todd Tinelli (CFO)｜guidance：CFO 預期資本支出與非資本支出的步調會在年內加速。（原話："the pace of our CapEx and non-CapEx spend to accelerate"）
- 2026-08-06｜Amir Vexler (CEO)｜margin：管理層說明單季波動大，因此以年度（含 TTM）結果衡量進展。（原話："we believe our annual results are more indicative of"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：CFO 拆解 SWU 營收：量減 23%，平均價格增 3%。（原話："due to a 23% decrease in volume of SWU sold, partially"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：CFO 說明 SWU 單位成本較去年同期上升 13%，且本季有 5,340 萬美元鈾銷售。（原話："partially offset by a 13% increase in the average cost of"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：本季毛利 4,990 萬美元，去年同期為 5,390 萬美元。（原話："compared to a gross profit of $53.9 million in Q2"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：CFO 說明淨利下滑主因：SG&A 增 1,280 萬美元（股票補償），先進技術成本增 750 萬美元。（原話："$12.8 million increase in SG&A costs, driven by an increase"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：調整後淨利加回先進技術成本 1,060 萬與股票補償 1,770 萬，稅後合計 2,190 萬；預期此類費用持續流經損益表。（原話："we continue to expect to have a certain level of"）
- 2026-08-06｜Todd Tinelli (CFO)｜margin：被問成本為何上升，CFO 以庫存成本、合約組合與會計處理回應，稱利潤率符合預期，未給具體成本拆解。（原話："Our margins are coming in line with"）
- 2026-08-06｜Todd Tinelli (CFO)｜capital_allocation：季末無限制現金 19 億美元，ATM 本季僅募得 5,390 萬美元。（原話："We finished the second quarter with $1.9 billion in"）
- 2026-08-06｜Todd Tinelli (CFO)｜capital_allocation：本季總資本支出 8,220 萬美元，其中 CapEx 7,160 萬、非 CapEx 1,060 萬。（原話："total capital spend of $82.2 million with $71.6"）
- 2026-08-06｜Todd Tinelli (CFO)｜capital_allocation：CFO 稱現金足以應付近期資本需求，並表示或有積壓訂單中的財務或有條件已全數移除。（原話："we believe we are sufficiently funded to meet our near-term"）
- 2026-08-06｜Amir Vexler (CEO)｜capital_allocation：CEO 表示簽署 DOE 濃縮標案帶來非稀釋、非債務資金。（原話："we have unlocked substantial nondilutive, non-debt funding"）
- 2026-08-06｜Amir Vexler (CEO)｜capital_allocation：CEO 表示持續評估供應鏈相關併購機會。（原話："We also continue to evaluate M&A opportunities in our"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：管理層表示打算在未來 HALEU 承購合約持續採用預付款結構。（原話："is a structure we intend to utilize in"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：CEO 宣布 Oak Ridge 第一台離心機預計 2026 年內完成。（原話："we plan to have our first centrifuge completed at our Oak"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：被問商業生產時點，CEO 去掉「後期」字眼，稱目標為 2029 年，可能縮短但無承諾。（原話："I would remove the adjective late and just say in 2029"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：縮短時程方面，CEO 稱正在探索但沒有可宣布事項與承諾。（原話："there is nothing to announce and no commitments at this"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：管理層預告 12 月在 Piketon 舉辦首次 Investor Day。（原話："we are excited to host our first Investor Day in December"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：CEO 說明首個新產能預計 2029 年上線，過渡期正與 DOE 洽談以民營方式營運現有 16 台離心機 HALEU 串級。（原話："the first new capacity from this transition is expected to"）
- 2026-08-06｜Amir Vexler (CEO)｜commitment：已與約 75% 的關鍵供應商完成合約；全年指引為 100%。（原話："We have finalized contracts"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：積壓訂單成長至 45 億美元，延伸至 2040 年；LEU 部門 37 億、技術解決方案 8 億。（原話："We grew our backlog to $4.5 billion"）
- 2026-08-06｜Todd Tinelli (CFO)｜customer：CFO 拆解積壓：LEU/HALEU 濃縮銷售增約 6 億美元；約 30 億濃縮積壓中 24 億已為確定協議。（原話："$3 billion in the segment's enrichment"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：分析師問積壓是否含 DOE 與 LOI，CEO 稱不含 DOE，增加來自商業協議，不提供更多細節。（原話："this does not include the"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：與 Oklo 簽署意向書，自 2029 年起供應 HALEU 給至多 5 座 Aurora powerhouse。（原話："signing of a letter of intent with Oklo for Centrus to"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：宣布與 X-energy 的 HALEU 承購合約，CEO 稱為確定性協議並含預付款。（原話："It's definitive, which is very important, and we're looking"）
- 2026-08-06｜Amir Vexler (CEO)｜customer：CEO 指出客戶願意簽具法律約束力協議的能力提高，Oklo 為朝確定合約推進中。（原話："a much greater ability from our customer base to actually"）
- 2026-08-06｜Todd Tinelli (CFO)｜customer：CFO 稱近期市場上公用事業已因俄羅斯禁令確保部位，目前 RFP 與討論針對未來有產能的期間。（原話："utilities have secured their position."）
- 2026-08-06｜Amir Vexler (CEO)｜customer：CEO 稱與公用事業的洽談並非線性，時間點不規則。（原話："They're lumpy and how they're being delivered."）
- 2026-08-06｜Amir Vexler (CEO)｜competition：CEO 稱 SWU 價格上升來自需求超過供給，且未來 2、3 年才有新產能陸續上線。（原話："you have demand that is outstripping supply."）
- 2026-08-06｜Amir Vexler (CEO)｜competition：CEO 稱長約價格持續攀升，現貨價維持在去年高點。（原話："spot pricing"）
- 2026-08-06｜Amir Vexler (CEO)｜competition：CEO 稱公用事業關注新進入者以確保市場有競爭，且財務或有條件移除後風險較低。（原話："we're getting a lot of advantages"）
- 2026-08-06｜Amir Vexler (CEO)｜competition：CEO 稱 Centrus 現為 HALEU 的首選供應商，並視 HALEU 為額外收益、LEU 為確定性業務。（原話："LEU is the sure business, the sure thing in the market."）
- 2026-08-06｜Amir Vexler (CEO)｜product：CEO 稱已提前兩週完成示範合約下所有 HALEU 生產要求。（原話："2 weeks ahead of schedule."）
- 2026-08-06｜Amir Vexler (CEO)｜product：建設規劃上，LEU 與 HALEU 的建置比例目前不變，依客戶確定承諾決定。（原話："we're not really"）
- 2026-08-06｜Amir Vexler (CEO)｜product：CEO 稱與 Palantir、EPC 夥伴合作降低成本，並鎖定大量訂單以爭取供應商節省，未提供數字目標。（原話："that's not something that we've talked about on this phone"）
- 2026-08-06｜Amir Vexler (CEO)｜product：CEO 稱縮短前置時間可轉為更早實現營收，商業協議要求更快時程。（原話："lead times really translate into enhanced revenue"）
- 2026-08-06｜Amir Vexler (CEO)｜risk：CEO 稱單季因業務性質有顯著波動。（原話："there can be a significant"）
- 2026-08-06｜Amir Vexler (CEO)｜risk：CEO 稱 HALEU 是補充成長機會與預付款資金來源；NNSA 有意向向 Centrus 單一來源採購部分濃縮活動。（原話："its intent to sole source certain enrichment activities"）
- 2026-08-06｜Todd Tinelli (CFO)｜risk：分析師問營運合約資金可能到期，管理層未直接回答該部分在營收指引中的位置，僅重申維持指引。（原話："We're not providing"）

### 問答異常語氣（迴避／改口／保留）
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：UBS：X-energy 交付節奏，以及是否來自示範串級轉商業營運。｜答法：稱無法提供交付與合約條款細節，改談 HALEU 領導地位與預付款。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Citigroup：營運合約資金可能到期，位於營收指引區間何處。｜答法：CFO 未回答該項位置，改談季間波動、維持指引、Piketon 增員；CEO 轉談離心機。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：H.C. Wainwright：SWU 價格增 3% 但成本增約 30%，成本驅動因素為何。｜答法：CFO 未拆解成本，稱為 SWU 與鈾的組合、庫存會計，並說利潤率符合預期。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Needham：承購協議的定價結構（固定或指數）。｜答法：稱受 NDA 限制不評論定價，改談合約為確定性與規模經濟；未回答想簽多少承購量。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Guggenheim：HALEU 與 LEU 完全放量後的獲利能力。｜答法：兩位主管均稱不提供額外指引，CEO 改談示範串級轉商業的技術驗證意義。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Evercore：下半年與 2027 年資本支出節奏。｜答法：CFO 稱不提供 2026 年以後指引；CEO 改談首台離心機，稱不給數字。
- LEU_Q2_2026_Earnings_Call_20260806.md｜問：Craig-Hallum：進一步成本節省的幅度。｜答法：CEO 稱列為優先事項並列舉做法，但未給數字或目標。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 1 | 1 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 5 | 4 |
| cyclical_supply_discipline_capacity | found | 5 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"B 觀望；等估值/MA 修復至 $120-150 + DOE final agreement + Russia 2027 末 waiver 確認後再分批","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"HALEU 商業化執行：Piketon 16-cascade 試線（已運轉）→ 商業擴產（Oak Ridge 製造 + Piketon 安裝）→ 2029 首批新產能上線","columns":{"2Y 驗證點":"2026-Q4 DOE 簽 final $900M agreement；2027 末 Geiger Bros 完成 Piketon 設計","5Y 驗證點":"2029-Q4 首批新產能上線（≥ 12 mt/year HALEU）","10Y 驗證點":"2030-2035 累積 50+ mt/year HALEU 產能 + 商業 ROIC &gt; WACC","具體門檻":"Piketon 2029 上線、12+ mt/year HALEU","信息來源":"DOE 公告 + 10-K MD&amp;A","漂移觸發":"連 2 季 Piketon milestone 延後 ≥ 6 個月 → 削弱"}},{"id":"H2","text":"$2.4B contingent backlog 兌現：商業客戶（utilities）的 contingent contracts 隨 Centrus 募資成功逐步轉為 firm orders","columns":{"2Y 驗證點":"2026 末 $1B+ Capex funding plan 公告；2027 首批 contingent → firm 轉換","5Y 驗證點":"2028-2029 至少 $1.5B contingent 轉 firm","10Y 驗證點":"2030+ 全 $2.4B 訂單 monetized 為 revenue","具體門檻":"2027 末轉換比例 ≥ 30%","信息來源":"Investor Day + 10-K backlog disclosure","漂移觸發":"連 2 quarter backlog YoY 停滯或下滑 → 削弱"}},{"id":"H3","text":"估值倍數收斂至合理區：當前 Fwd PE 45x 預期 5Y 收斂至 25-30x（同 industrial nuclear infra）","columns":{"2Y 驗證點":"2026-2027 共識 EPS 持續上修 + Fwd PE 跌至 30x 以下","5Y 驗證點":"2028-2029 Fwd PE 25-30x，EPS $6-8","10Y 驗證點":"2030+ 進入「成熟 utility」估值區 15-20x","具體門檻":"2027 末 Fwd PE ≤ 30x，EPS ≥ $4.50","信息來源":"sell-side + Bloomberg","漂移觸發":"連 2 quarter 共識 EPS 下修 ≥ 10% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Russia TENEX waiver 2028 切斷未延期，$1.2B Russia 來源 backlog 灰飛煙滅","columns":{"對應假設":"H1 / H2","時間尺度":"⚡ 短期（2027-2028）","監測指標":"DOE waiver 公告；TENEX 出口許可進度","警戒閾值":"2027-Q3 前未獲新 waiver / bridge 合約 → 連 2 季觸發即砍倉"}},{"id":"R2","text":"$3B+ Capex 募資失敗 / dilutive，contingent $2.4B backlog 無法 firm 化","columns":{"對應假設":"H2","時間尺度":"🔥 中期（2026-2027）","監測指標":"10-Q「Liquidity &amp; Capital Resources」段；DOE Loan Programs Office 進度；equity raise SEC filings","警戒閾值":"2026 末未公告 $1B+ funding plan → 削弱；2027 上半年實際 dilution &gt; 25% → 大砍 thesis"}},{"id":"R3","text":"laser enrichment（SILEX / GLE）規模化或 Urenco USA HALEU 商業核照通過","columns":{"對應假設":"H1 / H3","時間尺度":"🐢 長期（2028+）","監測指標":"GE-Hitachi GLE 進度；NRC HALEU 商業核照核發給 Urenco / Orano","警戒閾值":"跨年度 ≥ 50% 機率出現 → 砍倉；單一新聞不觸發"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"🟢","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":179.36,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"LEU","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Centrus Energy Corp."},"oneliner":"濃縮訂單與建廠進度都比半年前好，但獲利多半來自營業外項目與加回項，俄羅斯供貨與新廠總成本都未定案；股價腰斬後不算貴，也沒有安全邊際，等 12 月投資人日揭露總建置成本再決定。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺電力公司與美國政府的濃縮錢；今天的利潤卡在 TENEX 進貨成本與交貨時點，五年後的利潤卡在 Piketon 新產能能否如期建成。","reasoning":"營收分兩塊：Q3 LEU 部門 3,180 萬美元（占 57%，年減 29%），Technical Solutions 2,370 萬美元（占 43%，年減 21%）。LEU 部門下滑主要來自鈾銷量減少，SWU 營收其實增加 340 萬美元。Q3 毛損 1,060 萬美元（毛利率 −19.1%），GAAP 營業損失 2,970 萬美元；TTM 毛利率 23.28%、營業利益率 −1.25%。單季波動極大，全年指引 4.5–5 億美元隱含 Q4 要做 1.42–1.92 億美元。單點依賴：到 2027 年預計交貨的 LEU 逾半來自俄羅斯 TENEX，這是集中度風險，不是護城河。前十大客戶占 77%、前兩大 31%、最大 16%，未到必須逐家拆解的程度。Q3 新增訂單的客戶組合管理層拒絕拆分。可能看錯之處：若 Q4 如指引放量，Q3 的負毛利只是時點問題，本段對當期獲利的疑慮會減輕。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_lo","f_kpi3_gross_profit_loss","f_kpi4_gaap_net_income","f_kpi5_free_cash_flow_derived","f_kpi7_cash_and_cash_equivalent","f_kpi8_total_backlog","f_kpi9_guidance_fy2026_revenue","f_earnings_recency"],"verdict_values":{"revenue_quality":"長約為主但季度極不平均；到 2027 年逾半 LEU 是轉售 TENEX 貨，不是自產；Technical Solutions 靠 DOE 合約，Q3 已年減 21%。","unit_econ_note":"Q3 SWU 量增 19%、單價增 10%、單位成本增 28%；2026-08-06 CFO 揭露 Q2 量減 23%、單價增 3%、單位成本增 13%。由 SWU 營收增 340 萬美元反推，Q3 SWU 營收僅約 1,440 萬美元，單季樣本偏小。SWU 絕對單價事實表未涵蓋。","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"長約大宗品，處於國家資助的建廠期，現有業務靠轉售俄羅斯供貨"},"industry":{"clock_phase":"II","sd_verdict_source":"依據：Q3 SWU 單價年增 10%，TradeTech 鈾長約價 99 美元創紀錄，主要新產能多在 2028–2032 才上線。供需持久性：週期性偏結構，2030 年代初起供給可逆性高；管理層說缺口擴大，WNA 說全球供給到 2030 年代初仍過剩，兩者口徑不同。","bargaining":{"up":"TENEX 是單一重大供應來源，Q3 單位成本漲幅高於售價，顯示價差目前偏向上游；Westerman 收購只處理離心機零組件，不解決 SWU 進貨。","down":"客戶以投資級電力公司為主，採購分散給四大供應商，長約至 2040；新增的反應爐開發商有預付款，但信用較弱。","geo":"俄羅斯制裁、DOE 豁免、加拿大運輸許可（至 2027 年 3 月）共同決定現有業務能否續做；美國自有技術與國安需求則是地緣上的加分。"},"profit_pool_dir":"事實表未涵蓋產業營業利益池數字。方向判斷：西方濃縮環節目前分到更多價值，2030 年代新產能疊加後可能反轉。","tam_table":{"expanded":false,"reason":"事實表未涵蓋全球 SWU 市場規模、美國份額與分段成長，只有 Centrus 全球份額不到 5%、前四大合計逾 95%；無法列表，不推估。"}}}},"q2_moat":{"verdict":"競爭位置穩定：執行力擴大，定價權縮減，兩者相抵。","reasoning":"機制是美國自有、不受外國義務限制的濃縮技術，加上至 2040 年的長約與 DOE 9 億美元固定價合約。執行力證據：2026-08-06 CEO 承諾的年底前第一台離心機在 10 月完成，關鍵供應商合約由約 75% 做到 100%，濃縮訂單由 30 億美元增至 54 億美元。定價權證據相反：連兩季單位成本漲得比售價快；Urenco、Orano 擴產，DOE 也把另外兩張 9 億美元任務單給了其他公司，Centrus 沒拿到 LEU 任務單。同業 ROIC 事實表未涵蓋，以營業利益率代替：LEU −1.25%，CCJ 14.35%，BWXT 9.83%，但 LEU 處於建廠期，差距不能全歸於競爭力。全球份額不到 5%，目前是有條件的優勢，評 C。可能看錯之處：若 NNSA 單一來源合約落地且金額大，國安市場的定價權會明顯高於這裡的評分。","fact_refs":["f_peer_leu_gross_margin_pct","f_peer_leu_operating_margin_pct","f_peer_leu_fcf_margin_pct","f_peer_ccj_gross_margin_pct","f_peer_ccj_operating_margin_pct","f_peer_ccj_fcf_margin_pct","f_peer_uec_gross_margin_pct","f_peer_uec_operating_margin_pct","f_peer_uec_fcf_margin_pct","f_peer_bwxt_gross_margin_pct","f_peer_bwxt_operating_margin_pct","f_peer_bwxt_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"美國自有、不受外國義務限制的離心濃縮技術（管理層自述為國安用途唯一可量產方案，NNSA 2025-11 發出單一來源意向），加上長約與 DOE 固定價合約。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：第一台離心機提前完成、關鍵供應商 100% 簽約、濃縮訂單增 24 億美元。定價權縮減：Q3 單價增 10%、單位成本增 28%，西方對手與受補助新進者在 2028–2032 同期加產能。","competitor_notes":[{"name":"CCJ","strategy_note":"主業在鈾礦與燃料服務，利潤率遠高於 LEU，受惠同一輪鈾價，但不是 SWU 產能的直接對照。"},{"name":"UEC","strategy_note":"仍在早期放量，營業利益率極低，比較價值有限。"},{"name":"BWXT","strategy_note":"既有國防核燃料客戶關係，已揭露將申請新濃縮設施執照，是國安市場最值得盯的潛在對手。"},{"name":"Urenco","strategy_note":"在美國本土已有運轉產能並擴產，是爭奪西方長約最直接的對手。"},{"name":"Orano","strategy_note":"Georges Besse II 擴產預計 2028 起生產，時點早於 Centrus 首批新產能。"},{"name":"General Matter","strategy_note":"新進者，在肯塔基設廠，技術與量產能力事實表未涵蓋。"}],"spread_notes":{"note":"同業 ROIC 事實表未涵蓋，僅能以營業利益率代替，且 LEU 當期受建廠費用影響。"},"peer_na_reason":"事實表只有同業利潤率，沒有投入資本與 ROIC；Urenco、Orano 非本表標的。","threats":[{"level":"🟡","text":"Urenco USA 現行 70 萬 SWU 擴建已過半，另有 210 萬 SWU 新廠預計 2032 首產；Orano 與 Urenco Almelo 同步增產。同產品點對點競爭，影響已計入定價權評分，不重複扣分。","p":"60%","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#4"]},{"level":"🟡","text":"General Matter 設廠、BWXT 申請執照，UBS 預期競爭壓力在 2030 年代後期累積（搜尋摘要，未核原文）。DOE 三張各 9 億美元任務單代表新進者有政府資金。","p":"40%","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#1"]},{"level":"🟡","text":"GLE 雷射濃縮目標約 2030 年首次商業生產，但此法數十年未達商業規模。目前暫列點對點，若完成商業量產且成本占優，升為架構替代並重寫論點。","p":"30%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是核電機組，決策與付款者是電力公司燃料採購；沒有濃縮鈾就不能發電，屬需要而非想要。WNA 預估 2030 年鈾需求較現在高約 28%。HALEU 需求管理層自己也說要看市場成熟與否，強度低於 LEU。"},{"item":"決策層級","level":"🟡","text":"在單一燃料合約層級，電力公司可向四大供應商分散採購，Centrus 全球份額不到 5%，鎖定靠長約而非技術轉換成本。國安且不受外國義務限制的用途替代性最低，但此塊金額未揭露。"},{"item":"價值鏈分配","level":"🟡","text":"目前 Centrus 多為轉售者，Q3 單位成本漲幅 28% 高於售價 10%，價差偏向上游。自產後分配才可能改善，但長約定價受保密條款未揭露。"},{"item":"社會容忍度","level":"🟡","text":"優勢依賴授權與政策：俄羅斯進口禁令與豁免、DOE 資金、NNSA 採購都是政策產物。FY2027 預算未列 HALEU 串級資金，Portsmouth 污染集體訴訟仍在進行。濃縮占發電成本比例事實表未涵蓋，價格上限無法量化。"}],"roiic":"無法計算：新增資本尚未產生營業利益，總建置成本未揭露。","reinvest_rate":"遠高於 100%：FY2026 資本投入指引 3.5–5 億美元，約為 FY2025 營業利益 5,020 萬美元的 7–10 倍（未扣折舊，折舊事實表未涵蓋）。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率。投入資本與增量 ROIC 都缺資料，TTM 營業利益率 −1.25%，當期 NOPAT 接近零，公式沒有意義，不硬算。"}}}},"q3_growth":{"verdict":"長期空間寬：全球份額不到 5%，HALEU 與國安有簽約或政府意向佐證；但 2029 年前不會長在每股盈餘上。","reasoning":"共識 EPS 由 FY2025A 3.90 美元到 FY2028E 3.73 美元，三年 CAGR −1.5%；營收共識 FY2026 4.76 億美元、FY2027 5.03 億美元（18 位分析師），EPS 家數事實表未涵蓋。2029 年前成長主要靠價格與合約組合，2029 年後靠新產能的量。基本情境 FY2026–FY2031 EPS CAGR 15.2%，幾乎全在 FY2030 之後。內生上限算不出來，缺口無法歸因，因此長期信心壓低。衰退訊號亮兩項：毛利率下滑（Q3 −19.1% 對去年同期 −5.7%，TTM 23.28% 低於 FY2025 26.19%；Q2 毛利率事實表未涵蓋），FCF/淨利連年低於 0.75（FY2024 0.45、FY2025 0.40）。滲透率以公司份額衡量很低，但這是空間判斷，不代表產能能如期建成。可能看錯之處：2030 年代初多家新產能疊加，空間可能被對手分走。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_total_backlog"],"verdict_values":{"growth":{"driver_mix":"2029 年前靠價格與合約組合，2029 年後靠新產能的量；併購只有 Westerman，不是主驅動；沒有回購，股本反而擴張。","runway_years":"無法計算：事實表未涵蓋 SWU 市場規模，只知全球份額不到 5%。","runway_post_y5":"🟢","endo_ceiling_basis":"無法計算：當期 NOPAT 接近零，新增資本尚未產生營業利益，總建置成本未揭露。","segments":[{"item":"LEU 部門 Q3 營收","value":"3,180 萬美元，年減 29%，主因鈾銷量減少；SWU 營收增 340 萬美元"},{"item":"Technical Solutions Q3 營收","value":"2,370 萬美元，年減 21%，HALEU 營運合約營收減 1,020 萬美元"},{"item":"總 backlog","value":"70 億美元，至 2040 年；濃縮或有訂單 54 億美元，其中 51 億美元為確定協議"}],"decay_signals":["毛利率下滑：Q3 −19.1% 對去年同期 −5.7%，TTM 低於 FY2025","FCF/淨利連年低於 0.75：FY2024 0.45、FY2025 0.40"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資金充足，但全押一座廠，回報還算不出來；資本配置尚未通過驗證。","reasoning":"現金 22.36 億美元、總債務 11.79 億美元、淨現金 10.57 億美元，季後再付 Westerman 現金 9,500 萬美元。Q3 自由現金流 −1.26 億美元，TTM FCF 利潤率 −65.02%。9 月募資約 5 億美元，發行 50 萬股加預融資權證最多 200.6 萬股，等於約 200 美元一股，現價僅其一半。逐字稿寫權證履約價 2.27 至 3.63 美元，與 699 萬股權證對應 20 億美元（平均約 286 美元）的數量級不符，應為 227 至 363 美元，現價距最低履約價還要漲 117%，這筆資金目前拿不到。由淨利除以稀釋 EPS 粗算，股本 2023 至 2025 約增 29%。預融資權證與 Westerman 股票可能尚未計入 2,062 萬股。現金去向四分、債務到期結構事實表未涵蓋。壓力測試：若 2027–2029 年均資本投入 8 億美元，扣 Westerman 後現金約撐 2.7 年，未計 DOE 里程碑款。可能看錯之處：DOE 款與客戶預付款若比預期多，再增資需求會大幅下降。","fact_refs":["f_kpi6_sbc_adjustment_sg_a_and_","f_kpi7_cash_and_cash_equivalent","f_kpi5_free_cash_flow_derived","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Westerman 於 2026-10-16 完成，1.16 億美元，占市值 5.4%；CFO 稱第一年增厚，但利潤率未揭露，尚無已實現回報可算。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"未回購，資本全投入建廠，近 365 天也無配息。"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"只有兩季資料：Q2 股票補償加回 1,770 萬美元，Q3 為 130 萬美元利益；全年淨稀釋率事實表未涵蓋，不推估。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"沒有回購與配息，成長也不靠併購支撐；真正的資本問題是建廠回報，已在再投資與融資風險處理，近三年現金去向事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要 FY2031 EPS 約 8.4 美元才有 10% 年化，高於基本情境 7.5 美元；不貴，但沒有安全邊際，我不信現在的本益比能當便宜的證據。","reasoning":"推導：104.6 × 1.1^5 ＝ 168.5 美元，除以終端 20 倍得 8.4 美元。Fwd P/E 28.27 倍看似不高，但共識三年 EPS CAGR 為負，PEG 沒有意義。TTM 本益比的分母有爭議，調整後與正規化相差一倍以上。EV/S 2.42 倍在 4 個年度端點中分位 8.1，P/S 分位 28.9，本益比分位 36，都不是五年分位，且 EV 被增資現金壓低。賣方目標價 207–259 美元多為 8 月或未標日期，最高 390 美元是 1 月的舊數字，都早於股價下跌，不支持現在買進。Q3 調整後每股虧損 0.46 美元遠差於約 −0.13 美元的共識（二手摘要），但最新兩份快照 FY1 EPS 仍是 3.70 美元，利空可能尚未進模型。我沒有市場看錯的具體證據，已跌 49.55% 不是安全邊際。可能看錯之處：淨現金占市值 49%，若建廠成本低於預期，現價其實偏低。同業倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_net_debt_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250"],"verdict_values":{"valuation":{"basis":"FY1 前瞻本益比，輔以 EV/S；因分母有爭議，主要看 FY2031 需要多少每股盈餘。","tier":"建廠期核燃料供應商","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，不推估；終端倍數改以自身現值 28.27 倍對照。"},"fwd_pe":28.27,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"基本情境 150 美元，5 年約 7.5% 年化；機率加權約 157 美元，約 8.5% 年化，落在中段偏弱。股價較前份低 42%，但 EPS 分母品質變差，因此判合理而非便宜。五年分位事實表未涵蓋，只有 4 個年度端點，不外推；三年 EPS CAGR 為負，PEG 不適用。","targets":{"short":{"price":111,"basis":"FY2027E 共識 EPS 4.44 美元 × 25 倍，12 個月"},"mid":{"price":124,"basis":"基本情境 FY2031 目標 150 美元以 10% 折現兩年，約 3 年"}},"upside_short_pct":6.1,"upside_mid_pct":18.5,"denominator_disputed":true,"denominator_note":"TTM 正規化淨利 3,440 萬美元、調整後 7,730 萬美元，TTM 營業利益率 −1.25%，獲利主要來自營業外與稅務項目及加回的建廠費用（此為推論，利息收入絕對值事實表未涵蓋）。以 2,062 萬股粗算，正規化約 63 倍、調整後約 28 倍；GAAP TTM 又含 4,640 萬美元權證評價利益。GAAP 與 CFO 正規化口徑在營業損失與淨利兩處都差同一筆 460 萬美元，來源未揭露。便宜論證因此無效。"}}},"q6_how_wrong":{"verdict":"最可能看錯在新廠造價與時點，其次是俄羅斯供貨斷在新產能出來之前；成長是真的，但獲利品質弱。","reasoning":"五年後虧 50% 最可能的故事：俄供貨 2028 前後中斷，新廠延期或超支，現金燒完時股價遠低於權證履約價，只能低價增資。壓力測試五項過兩項：首批延一年現金仍夠、融資窗口關閉時現金可撐約 2.7 年，算通過；SWU 跌 20%、俄供貨 2027 中斷、資本超支 30% 都因單位成本與總建置成本未揭露而無法算過，記未通過。管理層把 Palantir 3 億美元節省的已驗證比例、商用 HALEU 利潤、Westerman 利潤率、2027 資本投入都延到投資人日，2026-08-06 也未拆解成本上升原因。循環位置用建廠循環六訊號：資本投入約為營收的 74–105%（賣）；產能利用率不適用；訂單領先資本投入（買）；交易對手信用混合；情緒偏投降，舊目標價高於現價（買）；量價 Q3 齊升、Q2 量減（中性）。多數落中循環，但訊號互相矛盾，P/B 事實表未涵蓋，反動能檢查不算全過。歷史最大回撤事實表未涵蓋；26 週已跌 49.55%，RSI 42.42，沒有過熱。核心不可守（尚未穿越週期賺錢），適用循環交易紀律。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_kpi3_gross_profit_loss","f_kpi5_free_cash_flow_derived","f_kpi7_cash_and_cash_equivalent"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長是真的，但亮兩項衰退訊號，獲利品質弱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.7,"pe":28.27,"basis":"FY2026E 共識 EPS 3.70 美元為分母，股價 104.6 美元；與終端倍數同為當年度前瞻口徑，EPS 分母品質有爭議。"},"eps":{"bull":[4.8,4.5,5.0,8.5,13.0],"base":[3.9,3.1,2.6,4.6,7.5],"bear":[2.8,1.2,0.3,0.9,2.0]},"pe":{"bull":25,"base":20,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":18,"base_cagr_pct":12},"max_dd":{"lo":-78,"hi":-50,"basis":"過去 26 週已跌 49.55%，顯示單一事件可在半年內腰斬；上緣 −50% 對應再一次財報或建廠壞消息，下緣 −78% 涵蓋空頭情境終點 −73% 加上路徑低點。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"首批新產能如期上線並提前爬坡，國安單一來源採購落地，長約價續升；股價超過履約價，權證行使帶來約 20 億美元與 699 萬新股，股數約 33M。終端 25 倍，因 Y6 起仍在爬坡；事實表未涵蓋同業 Fwd P/E，對照自身現值 28.27 倍。","base":"首批新產能 2029 下半年上線，2030 起按長約交貨；2027–2029 受利息收入下降與建廠費用拖累，EPS 低於共識。FY2031 營收約 10 億美元、淨利約 1.95 億美元、股數約 26M（含預融資權證與後續增發）。終端 20 倍低於現值 28.27 倍，不靠倍數擴張。","bear":"俄供貨 2028 前中斷或新產能延到 2031，毛利壓力延續，DOE 資金縮手，需低價增資；FY2031 淨利約 5,600 萬美元、股數約 28M。終端 14 倍對應成長熄火。機率 30%：西方新產能 2028–2032 疊加，2016 年下行期 Centrus 毛利率僅 14.5% 且虧損；管理層的結構性缺口說法未獲 WNA 全球數字支持，不採信為降低空頭機率的理由。"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"到 2027 年逾半 LEU 來自 TENEX，2026–2027 未承諾量豁免未定；新產能 2029 才有，中間沒有替代來源；目前只完成第一台離心機。","assumption":"俄方與美方在 2028 前不切斷供貨，生產線能從第一台放大到商業規模。","consequence":"收入在新廠上線前掉一半，現金同時燒，權證價外，只能在低價增資，五年後虧損超過 50%。","ruling":"採納，這是最大風險，與唯一致命點部分重疊：致命點看終端年的新產能，本條補上過渡期斷供；機率放入 30% 空頭情境。","watch":"DOE 豁免公告、加拿大運輸許可延期、Oak Ridge 出貨節奏。","evidence_refs":["reg_tariff_export#3","geo_supply_chain#1"],"fact_refs":["f_kpi5_free_cash_flow_derived","f_kpi7_cash_and_cash_equivalent"]},{"view":"論點成功但股東經濟變差","evidence":"長約定價受保密條款未揭露；Q3 已宣布的訂單來自 X-energy、Radiant、Antares 等開發商，管理層拒絕拆分；前十大客戶占 77%；對手產能 2028–2032 同期上線；股本 2023–2025 粗算增 29%。","assumption":"長約價格足以回收新廠投資，且客戶有能力履約。","consequence":"工廠如期完工、訂單也交貨，但增量報酬低於資金成本，每股盈餘被股本擴張吃掉。","ruling":"採納，因此基本情境股數用 26M、終端倍數降到 20 倍，並把總建置成本列為重新進場的唯一約束。","watch":"投資人日總建置成本、預付款金額、開發商融資狀況與 backlog 拆分。","evidence_refs":["customer_concentration_credit#0"],"fact_refs":["f_kpi8_total_backlog","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"跌 49.55% 後 Fwd P/E 仍 28.27 倍；FY2028E EPS 3.73 美元低於 FY2025A 3.90 美元；正規化 TTM 約 63 倍。","assumption":"市場願意在獲利下滑期維持 20 倍以上。","consequence":"若以 15 倍看 FY2028E，得 56 美元，再跌 46%。","ruling":"部分採納：本益比角度仍未便宜，但 EV 僅 11 億美元且淨現金占市值 49%，不算過度反映成功。結論是合理、不追。","watch":"FY2026 正規化每股盈餘、共識是否在 Q3 後下修。","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy3","f_ev_m","f_net_debt_m"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 179.36 → 本次 104.6（-41.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=179.36","side_b":"本次 price_at_dd=104.6","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 179.36 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 179.36 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 179.36 美元：Bull 價 325、Bear 價 28，五年期望值 −12.4%，基準年化 −3.5%，不對稱比 0.8","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.8。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 179.36 美元：五年期望值 −12.4%，基準年化 −3.5%，不對稱比 0.8","side_b":"本次情境、股價 104.6 美元：五年期望值 +50.2%，基準年化 7.5%，不對稱比 2.4","ruling":"再換股價、情境不動：起點價下跌 41.7%，五年期望值多 62.6 個百分點，基準年化多 11.0 個百分點，不對稱比由 0.8 升到 2.4。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價下跌後的估值結論","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份股價 179.36 美元、Fwd P/E 約 45 倍，估值判偏貴，未給機率與回撤範圍。","side_b":"本次股價 104.6 美元、Fwd P/E 28.27 倍，估值改判合理；機率多 25、基 45、空 30，回撤範圍 −50% 至 −78%。","ruling":"股價跌 42% 讓估值結論放寬，但 EPS 分母品質變差，只放寬到合理，不到便宜。","evidence_level":"高","settle_metric":"FY2026 正規化每股盈餘","if_then":["若 FY2026 正規化每股盈餘低於 2 美元，估值結論回到偏貴，不追。","若總建置成本揭露後基本情境 EPS 上修到 8.4 美元以上，重跑研究並可分批反買。"]},{"axis":"訊號與價值陷阱","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份訊號 B、價值陷阱風險中等，當時訂單 24 億美元且資金未到位。","side_b":"本次兩者維持原判，但組成改變：濃縮訂單 54 億美元、現金 22 億美元變好；Q3 負毛利、FCF 惡化變差。","ruling":"好壞相抵，維持觀望等級；不是沒有新資訊，而是新資訊方向相反。","evidence_level":"中","settle_metric":"FY2026 毛利率與投資人日總建置成本","if_then":["若 FY2026 毛利率低於 20%，價值陷阱升一級，減碼。","若毛利率高於 25% 且總成本可被資金涵蓋，重跑研究。"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份這些欄位為空值。","side_b":"本次依新格式補上：競爭位置穩定、長期空間寬、循環大宗品兼特殊情境、中循環。","ruling":"屬於補填，不代表基本面在這些欄位發生變化。","evidence_level":"高","settle_metric":"無","if_then":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等估值/MA 修復至 $120-150 + DOE final agreement + Russia 2027 末 waiver 確認後再分批","side_b":"投資人日或其後財報揭露總建置成本，且現金加 DOE 里程碑款足以付到 2029 首批上線，不需在 227 美元以下再增資。","ruling":"舊條件已過一項：DOE 於 6 月 30 日簽固定價 9 億美元合約。價格區間失效，股價已低於 120 美元。俄羅斯豁免未定，改列減碼條件。現在真正卡住的是回報算不出來，所以綁單一約束。","evidence_level":"中","settle_metric":"總建置成本與資金涵蓋","if_then":["若條件成立，重跑研究後分批反買，首倉不超過 1.5%。","若揭露後仍需低價再增資，不追；若已持有則減碼。"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（欄位為空）。","side_b":"Piketon 首批新增濃縮產能無法在 2029 年底前開始商業交貨，公司正式把時點延到 2030 年以後。","ruling":"新格式要求列出敏感度最大的一項，新產能時點對終端年 EPS 的影響大於俄供貨中斷。","evidence_level":"中","settle_metric":"公司正式時程與里程碑","if_then":["若正式延到 2030 年以後，若持有則清倉，未持有則不建倉。","若 2028 年底前首批串級已完工過半，降低此項機率並重跑研究。"]},{"axis":"清倉與減碼量化門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設量化出場指標（欄位為空）。","side_b":"本次設六項：新產能延到 2030 後清倉；現金低於 10 億美元且首批未上線清倉；俄供貨未解、毛利率低於 20%、濃縮訂單低於 45 億美元、稀釋超過 25% 均減碼。","ruling":"把前份散在風險表的條件改成可追蹤指標，並補上毛利率與現金兩項新證據對應的門檻。","evidence_level":"中","settle_metric":"各指標季度揭露","if_then":["任一清倉條件觸發即清倉。","減碼條件觸發兩項以上，持股減半。"]},{"axis":"融資風險門檻","cause":"新證據","prior_field":["R2"],"side_a":"2026 末未公告 $1B+ funding plan → 削弱；2027 上半年實際 dilution > 25% → 大砍 thesis","side_b":"第一段已達成並退休，現金 22 億美元；保留 2027 上半年實際稀釋超過 25% 即減碼，新增現金低於 10 億美元且首批未上線即清倉。","ruling":"資金已到位，舊的公告條件失去意義，風險轉為總成本與低價增資。","evidence_level":"高","settle_metric":"現金餘額、總建置成本、股本變動","if_then":["若稀釋超過 25%，減碼。","若現金門檻觸發，清倉。"],"evidence_refs":["major_events#2"]},{"axis":"訂單與本益比舊門檻","cause":"新證據","prior_field":["H2","H3"],"side_a":"2027 末轉換比例 ≥ 30%；2027 末 Fwd PE ≤ 30x，EPS ≥ $4.50","side_b":"確定協議占濃縮訂單已達 94%；Fwd P/E 已 28.27 倍。門檻改為總 backlog 不低於 70 億美元、確定協議占比 90% 以上，以及 FY2027 調整後 EPS 不低於 3.5 美元。","ruling":"舊門檻提前達成或因股價下跌而失去鑑別力，EPS 門檻下調是因為利息收入與建廠費用，共識 FY2027 也只有 4.44 美元。","evidence_level":"高","settle_metric":"季度 backlog 揭露與 FY2027 EPS","if_then":["若 backlog 低於 45 億美元濃縮訂單門檻，減碼。"]},{"axis":"供需缺口方向","cause":null,"prior_field":null,"side_a":"管理層：供需缺口持續擴大，現貨與長約 LEU 價格上升。","side_b":"WNA：全球濃縮供給至少到 2030 年代初仍超過需求。","ruling":"可調和，程度差異。全球數字含俄羅斯與中國產能，西方可用供給較緊。但 WNA 是 2025 年 9 月資料，管理層為自述，所以採中間立場：短缺到新廠大量上線前，之後供給可逆性高。","evidence_level":"中","settle_metric":"公司季度 SWU 均價與 WNA 下一版燃料報告","if_then":["若 SWU 均價連 3 季年減，提高空頭機率到 40% 並減碼。","若 WNA 下一版轉為西方短缺延長到 2035 年以後，重跑研究。"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#3"]},{"axis":"負毛利是時點還是結構","cause":null,"prior_field":null,"side_a":"CFO（2026-11-05）：負毛利主要是進貨與交貨時點錯配，要看 TTM；2026-08-06 CFO 也稱利潤率符合預期。","side_b":"Q2 單價增 3%、單位成本增 13%；Q3 單價增 10%、單位成本增 28%，連兩季成本漲得比價快；Q2 被問成本時未拆解。","ruling":"不採信也不否定，列為未證並監測。Q3 SWU 營收基數小，單季數字可能失真，但方向連兩季相同。不可調和前先不動論點，以 Q4 決勝。","evidence_level":"中","settle_metric":"FY2026 全年毛利率與 Q4 單位成本漲幅","if_then":["若 FY2026 毛利率低於 20%，或 Q4 單位成本年增高於單價年增 10 個百分點以上，時點說法證偽，減碼。","若 FY2026 毛利率高於 25%，時點說法成立，解除此風險。"],"evidence_refs":["end_markets#0","end_markets#1","cyclical_inventory_price_position#2","capital_markets_pricing#1"]},{"axis":"政府支持力度","cause":null,"prior_field":null,"side_a":"CEO（2026-11-05）：兩屆政府支持未減，只會更強。","side_b":"DOE 目前不打算行使 HALEU 營運合約後續選擇權，FY2027 預算未列串級資金；Q3 該合約營收減 1,020 萬美元；2026-08-06 CFO 被問合約資金時未回答。","ruling":"可調和：政策支持轉向新建產能，不再付營運費用。對建廠有利，對 Technical Solutions 不利。示範串級的長期協議仍在談，不能算解決。","evidence_level":"中","settle_metric":"DOE 長期協議與 Technical Solutions 季營收","if_then":["若 2027 年中前未簽長期協議且季營收低於 2,000 萬美元，減碼。","若簽約，移除此風險。"],"evidence_refs":["end_markets#3"]},{"axis":"20 億美元權證資金","cause":null,"prior_field":null,"side_a":"CFO：權證全數行使可帶來約 20 億美元，提供額外財務彈性。","side_b":"699 萬股權證對應平均履約價約 286 美元，逐字稿寫的 2.27 至 3.63 美元應為 227 至 363 美元；現價距最低履約價還要漲 117%。","ruling":"這筆錢只有股價翻倍以上才拿得到，也就是最不缺錢時才有；評估資金時不計入。","evidence_level":"高","settle_metric":"股價相對 227 美元與 10-Q 權證條款","if_then":["若資金缺口要靠這批權證才補得上，不追；若已持有則減碼。"],"evidence_refs":["major_events#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價跌 49.55%，淨現金占市值 49%，EV 11 億美元買到 70 億美元 backlog、美國自有濃縮技術與 DOE 9 億美元合約，里程碑連續提前。","side_b":"現金會花在總成本未揭露的工廠上，FY2028 共識 EPS 低於 FY2025，俄供貨未定，Q3 利空可能未進模型；投資人日只剩一個月，等待成本低。","ruling":"等。基本情境年化約 7.5%，不足以補償二元風險；一個月內會有關鍵資料。","evidence_level":"中","settle_metric":"投資人日總建置成本","if_then":["若股價在條件成立前續漲，不追。","若股價續跌但基本面無損，且條件成立，分批反買，首倉不超過 1.5%，合計不超過 3%。","若機械上偏空的訊號證實為對：FY2026 毛利率低於 20%，到 2027 年 3 月底前仍不進場。"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：Q3 SWU 均價增 10%，WNA 2030 需求高約 28%，國安需求受 GAO 報告支持，濃縮訂單增至 54 億美元。","side_b":"競爭惡化：Urenco、Orano 擴產，General Matter、BWXT 進場，DOE 補助多家。其他結構變數：俄羅斯禁令與豁免、Section 232 關稅、FY2027 預算。","ruling":"雙向拉鋸。2029 年前結構轉好占優，2030 年代初競爭惡化占優。","evidence_level":"中","settle_metric":"西方新增產能時程與長約 SWU 價","if_then":["若 Urenco 或 Orano 擴產提前一年以上，空頭機率加 5 個百分點並停止加碼。"],"evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1"]}],"triggers":[{"n":1,"text":"投資人日後重跑研究。","type":"複審日期","maps_to":"H1","metric":"總建置成本、2027 資本投入、Westerman 利潤率","threshold":"三項是否揭露","action":"不追","source_freq":"公司活動，一次","date":"2026-12-07"},{"n":2,"text":"總建置成本可被現金與 DOE 款涵蓋時，才重新考慮進場。","type":"估值rearm","maps_to":"R2","metric":"現金加 DOE 里程碑款相對總建置成本","threshold":"足以付到 2029 首批上線且不需在 227 美元以下增資","action":"分批反買","source_freq":"投資人日與季報","date":null},{"n":3,"text":"新產能正式延期超過目標年份。","type":"Single Thing","maps_to":"H1","metric":"Piketon 首批商業交貨時點","threshold":"延到 2030 年以後","action":"清倉","source_freq":"季報與 8-K","date":"2029-12-31"},{"n":4,"text":"俄羅斯供貨在過渡期沒有保障。","type":"風險","maps_to":"R1","metric":"2026–2027 未承諾量豁免或過渡供貨合約","threshold":"2027-Q3 前未取得，連 2 季","action":"減碼","source_freq":"DOE 公告與 10-Q","date":"2027-09-30","evidence_refs":["reg_tariff_export#0","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1"]},{"n":5,"text":"Piketon 租約到期前未確定續約。","type":"風險","maps_to":"H1","metric":"Piketon 租約狀態","threshold":"2027-10-01 前未續約","action":"停止加碼","source_freq":"10-Q","date":"2027-10-01","evidence_refs":["regulatory_antitrust#0"]},{"n":6,"text":"負毛利的時點說法被證偽。","type":"風險","maps_to":"R4","metric":"FY2026 毛利率與 Q4 單位成本漲幅","threshold":"毛利率低於 20%，或單位成本年增高於單價年增 10 個百分點以上","action":"減碼","source_freq":"年報","date":"2027-Q1","evidence_refs":["end_markets#0","end_markets#1","cyclical_inventory_price_position#2"]},{"n":7,"text":"現金消耗快於建廠進度。","type":"清倉","maps_to":"R2","metric":"無限制現金","threshold":"低於 10 億美元且 2029 首批尚未上線","action":"清倉","source_freq":"季報","date":"2029-12-31"},{"n":8,"text":"濃縮訂單是否維持。","type":"假設驗證","maps_to":"H2","metric":"濃縮或有訂單金額與確定協議占比","threshold":"低於 45 億美元或占比低於 80%","action":"減碼","source_freq":"季報","date":"2027-12-31"},{"n":9,"text":"替代技術或對手 HALEU 執照成真。","type":"風險","maps_to":"R3","metric":"雷射濃縮商業化與 Urenco USA HALEU 商業執照進度","threshold":"跨年度判斷機率達 50% 以上，單一新聞不觸發","action":"清倉","source_freq":"NRC 公告，半年檢視","date":null,"evidence_refs":["substitute_technology#0","competitive_share_entrants#2"]},{"n":10,"text":"鈾部門關稅若落地，用公司損益判斷能否吸收。","type":"風險","maps_to":"R4","metric":"關稅公告後下一季 SWU 單位成本漲幅","threshold":"單位成本年增高於單價年增 10 個百分點以上","action":"減碼","source_freq":"聯邦公告與季報","date":null,"evidence_refs":["reg_tariff_export#2"]},{"n":11,"text":"McGlone 污染集體訴訟，民事案件；受影響金額與結案日事實表未涵蓋。","type":"風險","maps_to":"R2","metric":"集體認證與和解金額","threshold":"集體認證通過且不利和解超過 1 億美元；刑事介入則清倉","action":"減碼","source_freq":"10-K 與 10-Q 法律附註","date":null,"evidence_refs":["major_events#3","lawsuit_class_action#0"]},{"n":12,"text":"進場條件成立後，股價下跌但基本面無損。","type":"加碼","maps_to":"H3","metric":"股價相對 250 週均線與 Q4 毛利率","threshold":"低於 97.82 美元且 Q4 毛利率為正","action":"分批反買","source_freq":"週線與季報","date":null},{"n":13,"text":"證據未到但股價先走。","type":"估值rearm","maps_to":"R2","metric":"股價與總建置成本揭露","threshold":"條件未達而股價漲到 150 美元以上","action":"不追","source_freq":"週線","date":null},{"n":14,"text":"現有賣方模型尚未消化 Q3，首個確認點前不加碼。","type":"減碼","maps_to":"H3","metric":"FY2026 共識 EPS 是否下修","threshold":"FY2026 財報公布前仍未更新","action":"停止加碼","source_freq":"共識快照，月","date":"2027-Q1","evidence_refs":["capital_markets_pricing#1"]}],"kill_metrics":[{"metric":"Piketon 首批新增產能商業交貨時點","bear_threshold":"公司正式延後到 2030 年以後即清倉","window":"至 2029-12-31","source":"10-Q、8-K、投資人日","last_status":"ok"},{"metric":"俄羅斯 TENEX 2026–2027 未承諾量豁免或過渡供貨","bear_threshold":"2027-Q3 前未取得，連 2 季即減碼","window":"至 2027-09-30","source":"DOE 公告、10-Q","last_status":"warning"},{"metric":"年度毛利率","bear_threshold":"FY2026 或 FY2027 低於 20% 即減碼","window":"FY2026–FY2027","source":"10-K","last_status":"warning"},{"metric":"濃縮或有訂單金額與確定協議占比","bear_threshold":"金額低於 45 億美元，或確定協議占比低於 80%，即減碼","window":"至 2027-12-31","source":"季度財報與法說","last_status":"ok"},{"metric":"無限制現金","bear_threshold":"低於 10 億美元且 2029 首批尚未上線即清倉","window":"至 2029-12-31","source":"10-Q","last_status":"ok"},{"metric":"實際股本稀釋","bear_threshold":"2027 上半年累計超過 25% 即減碼","window":"2027-01-01 至 2027-06-30","source":"10-Q、SEC 增資文件","last_status":"ok"}],"evidence_dismissed":[{"ref":"major_events#4","reason":"證據只有 8-K 申報清單的項目標題，沒有通知內容、原因或後續處理，無法判斷涉及財務還是治理；8-K 件數本身也不是負面資訊，近期多為融資、合約與併購公告。"}],"action_conditions":{"rearm_trigger":"投資人日或其後財報揭露總建置成本，且現金加 DOE 里程碑款足以付到 2029 首批上線，不需在 227 美元以下再增資。","exec_line":"條件成立後重跑研究，不直接建倉；首倉不超過 1.5%，第二筆要等 FY2026 毛利率驗證，因為有具名的俄羅斯豁免與建廠成本事件未解。投資人日前不追，Q3 利空進入共識前不加碼。","holding_cap":"合計不超過 3%"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 12 月 7 日投資人日揭露總建置成本，確認現金加 DOE 里程碑款足以付到 2029 首批上線。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"Piketon 首批新增產能 2029 年底前開始商業交貨，離心機從第一台放大到連續量產。","2y":"2027 年底前 Oak Ridge 連續出貨、Piketon 開始安裝；2028 年底前首批串級完工過半。","5y":"2029 年底前首批商業交貨；FY2031 新產能營收達 5 億美元以上。","10y":"2036 年前產能爬坡完成，新增資本回報高於 10%。","threshold":"2029-12-31 前首批商業交貨，時程延後不超過 6 個月。","source":"10-Q、8-K、投資人日、NRC 與 DOE 公告","drift_rule":"里程碑連 2 季延後 6 個月以上為削弱；延到 2030 年以後為反轉。"},{"id":"H2","text":"54 億美元濃縮或有訂單能按約變現，新增訂單不靠尚無營收的開發商撐場。","2y":"2027 年底總 backlog 不低於 70 億美元，確定協議占濃縮訂單 90% 以上。","5y":"FY2031 總營收達 10 億美元。","10y":"2040 年前訂單交貨完畢，沒有重大取消。","threshold":"濃縮訂單不低於 45 億美元，確定協議占比不低於 80%。","source":"季度 backlog 揭露、10-K 客戶集中度","drift_rule":"backlog 連 2 季下滑 5% 以上為削弱；連 3 季下滑 10% 以上為反轉。"},{"id":"H3","text":"過渡期毛利守得住，自產後單位經濟轉好，每股獲利跨過股本擴張。","2y":"FY2026、FY2027 年度毛利率不低於 20%；FY2027 調整後 EPS 不低於 3.5 美元。","5y":"FY2031 EPS 不低於 7.5 美元，自由現金流轉正。","10y":"FY2036 ROIC 高於資金成本，FCF/淨利不低於 0.75。","threshold":"年度毛利率不低於 20%，FY2031 EPS 不低於 7.5 美元。","source":"10-K、10-Q、季度單位成本揭露","drift_rule":"TTM 毛利率連 2 季偏離門檻 5% 以上為削弱；連 3 季偏離 10% 以上為反轉。"}],"R":[{"id":"R1","text":"俄羅斯 TENEX 供貨在新產能上線前中斷：到 2027 年預計交貨的 LEU 逾半來自 TENEX，未承諾量豁免未定，加拿大運輸許可只到 2027 年 3 月。","h_ref":"H1","clock":"⚡","threshold":"2027-Q3 前未獲新豁免或過渡供貨合約，連 2 季觸發即砍倉。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#2"]},{"id":"R2","text":"總建置成本未揭露，資金缺口可能要低價再增資。權證要股價到 227 美元以上才會行使，Q3 自由現金流 −1.26 億美元，2027 資本投入還會加速。","h_ref":"H1","clock":"🔥","threshold":"2027 上半年實際稀釋超過 25%；或現金低於 10 億美元且 2029 首批尚未上線。","evidence_refs":["major_events#2"]},{"id":"R3","text":"競爭產能與替代技術：Urenco、Orano 擴產，General Matter、BWXT 進場，GLE 雷射濃縮目標 2030 年。","h_ref":"H2","clock":"🐢","threshold":"雷射濃縮規模化或 Urenco USA 取得 HALEU 商業執照的機率跨年度達 50% 以上即砍倉，單一新聞不觸發。","evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#4","substitute_technology#0"]},{"id":"R4","text":"單位毛利擠壓：連兩季 SWU 單位成本漲得比售價快，Q3 負毛利，調整後每股虧損遠差於共識。","h_ref":"H3","clock":"⚡","threshold":"FY2026 毛利率低於 20%，或 Q4 單位成本年增高於單價年增 10 個百分點以上。","evidence_refs":["end_markets#0","end_markets#1","cyclical_inventory_price_position#2","capital_markets_pricing#1"]},{"id":"R5","text":"DOE 不打算行使 HALEU 營運合約後續選擇權，FY2027 預算未列串級資金，示範串級轉商業的長期協議未簽。","h_ref":"H1","clock":"🔥","threshold":"2027 年中前未簽長期協議，且 Technical Solutions 季營收低於 2,000 萬美元（Q3 為 2,370 萬美元）。","evidence_refs":["end_markets#3"]},{"id":"R6","text":"濃縮與鈾週期反轉：上一輪鈾現貨低迷歷時 5–9 年，2016 年 Centrus 毛利率 14.5% 且淨損 6,700 萬美元；WNA 認為全球濃縮供給到 2030 年代初仍過剩。","h_ref":"H3","clock":"🐢","threshold":"公司 SWU 均價連 3 季年減，或鈾長約價自 99 美元回落 20% 以上。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","supply_demand_durability#1"]},{"id":"R7","text":"Westerman 收購 1.16 億美元，占市值 5.4%，管理層稱第一年增厚但利潤率未揭露，且表明可能再做併購。","h_ref":"H3","clock":"🔥","threshold":"投資人日未揭露分部利潤率，或 FY2027 累計併購超過 3 億美元而沒有已實現回報數字。","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"Piketon 首批新增濃縮產能無法在 2029 年底前開始商業交貨，公司正式把時點延到 2030 年以後。","why_fatal":"這是情境樹裡敏感度最大的一項。基本情境 FY2031 EPS 7.5 美元幾乎全靠新產能；延兩年，FY2031 EPS 約回到空頭情境的 2 美元，目標價跌幅約 73%。俄供貨中斷主要傷 FY2028–29，不是終端年。54 億美元濃縮訂單也以產能建成為前提。","if_happens":"若持有則清倉，未持有則不建倉。現金繼續燒、權證價外、訂單交期風險會同時出現。","how_monitor":"每季追 Oak Ridge 離心機產出節奏、Piketon 施工包完成數與資本投入；12 月 7 日投資人日時程表；NRC 與 DOE 公告。","probability":"未來 12–24 個月內公司正式宣布延到 2030 年以後的機率約 20%；到 2029 年底未能準時的累計機率約 35%。此為判斷值，沒有外部統計。"}},"appendix_a":{"growth_durability":6,"quality_score":4,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":23.56,"peg_fy2":58.23,"stress":{"pass":2,"total":5},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-11-07）"},"eps_meta":{"base_eps_path":{"FY2025A":3.9,"FY2026E":3.7,"FY2027E":4.44,"FY2028E":3.73},"fy_end_month":12,"eps_basis":"FY2025A 為 yfinance 稀釋 EPS；FY2026E–FY2028E 為 2026-11-07 Koyfin 共識，是否為調整後口徑事實表未註明，兩者口徑可能不同。"},"catalysts":[{"date":"2026-12-07","date_precision":null,"type":"guidance","event":"Piketon 投資人日：總建置成本、2027 資本投入、Westerman 利潤結構與更新指引","impact":"高","watch":"總成本是否在現金加 DOE 款涵蓋範圍內"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"FY2026 年報與 Q4 結果","impact":"高","watch":"Q4 營收是否達 1.42–1.92 億美元，全年毛利率是否高於 20%"},{"date":"2027-03","date_precision":"month","type":"regulatory","event":"加拿大運輸許可到期，需再延期才能續運 LEU","impact":"中","watch":"是否取得延期"},{"date":"2027-Q3","date_precision":"quarter","type":"regulatory","event":"2026–2027 未承諾交貨的俄羅斯豁免或過渡供貨期限","impact":"高","watch":"DOE 是否核准，或公司是否取得替代供貨"},{"date":"2027-10-01","date_precision":null,"type":"regulatory","event":"Piketon 租約到期","impact":"中","watch":"續約條件"},{"date":"2029-Q4","date_precision":"quarter","type":"capacity","event":"Piketon 首批新產能目標上線","impact":"高","watch":"是否開始商業交貨"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-49.55, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
