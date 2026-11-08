你是 DD 管線 v20 的判斷層閘（gate），標的 CAMT（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（41 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝161.3 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income＝47.5 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi2_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝29.5 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi8_gaap_gross_margin`（q1_business）｜GAAP gross margin＝50.0 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi9_guidance_q4_2026_revenue`（q1_business）｜Guidance: Q4 2026 revenue＝180 USD M（約數，~+40% YoY）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：FY2026 營收指引約 595 vs yfinance FY1 共識 596.38（dd_numbers_extra capital_structure）；FY2027 指引 >800 vs 共識 804.17
- `f_peer_camt_gross_margin_pct`（q2_moat）｜CAMT 毛利率＝50.03 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAMT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_camt_operating_margin_pct`（q2_moat）｜CAMT 營業利益率＝23.15 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAMT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_onto_gross_margin_pct`（q2_moat）｜ONTO 毛利率＝50.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONTO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_onto_operating_margin_pct`（q2_moat）｜ONTO 營業利益率＝13.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONTO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvmi_gross_margin_pct`（q2_moat）｜NVMI 毛利率＝57.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVMI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_nvmi_operating_margin_pct`（q2_moat）｜NVMI 營業利益率＝30.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVMI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_klac_gross_margin_pct`（q2_moat）｜KLAC 毛利率＝61.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_klac_operating_margin_pct`（q2_moat）｜KLAC 營業利益率＝42.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.63 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝5.09 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝5.92 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝596.38 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（10 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝804.17 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_operating_cash_flow`（q1_business）｜Operating cash flow＝71.1 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi6_share_based_compensation`（q1_business）｜Share-based compensation＝5.7 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi7_cash_deposits_marketable`（q1_business）｜Cash, deposits & marketable securities＝877.1 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 PR Newswire（Camtek IR 發布）Q3 2026 results，https://www.prnewswire.com/il/news-releases/camtek-announces-results-for-the-third-quarter-of-2026-302929209.html（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-117.34 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 489.18、現金 606.52（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝46.73 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝4417.34 USD m｜期間與口徑：2026-11-08／市值 4534.68 ＋ 淨負債 -117.34｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝97.05 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝26.74 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 3.63，分子＝快照價 97.05｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝36.48 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝23.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝23.3 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝8.33 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝59.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝59.7 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝8.12 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝51.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝51.6 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝7.41 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.55 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 3.61 → 3.63（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-52.78 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝30.21｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 97.05 / W52 147.54 / W104 115.43 / W250 77.86 / W250 13週斜率 1.56%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝147.54 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝115.43 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝77.86 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F FY2025 風險因素：市場高度競爭，對手有些資源更多；市場成長可能吸引新進入者；另有本地小型競爭者主攻低階市場、以較低價格供貨；競爭可能壓低價格與毛利。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-03-19）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F 風險因素：另有本地小型競爭者鎖定低階市場並以較低價格供貨。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-03-19）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：2025 年亞太占營收約 91%，其中中國占 49%。
  - 來源：SEC EDGAR 20-F FY2025 Item 3（as_of 2026-03-19）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Camtek進階封裝營收高度依賴HPC及少數chiplet/HBM客戶，客戶減少資本支出或自製會造成衝擊（集中度風險）
  - 來源：Simply Wall St community narrative on Camtek（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Camtek 20-F 揭露：2025 年亞太區占營收約 91%，中國占 49%；出口管制（含 2022 年 10 月起、2025 年加強的美國商務部規則）可能間接壓低中國半導體設備需求；美國對進口（含中國）加徵關稅帶來不確定性並可能增加成本。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D Risk Factors（as_of 2026-03-19）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：20-F 指出即使美國出口管制不直接適用，也可能影響需求；若有美國連結（含美國原產成分、美國受控技術），非美國公司亦可能受管制。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D Risk Factors（as_of 2026-03-19）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：20-F（FY2020 版，較舊）揭露依賴單一／有限來源供應商與分包商（Key Suppliers）提供關鍵零組件與子系統
  - 來源：Camtek Form 20-F FY2020 (SEC)（as_of 2021-03-31）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Q2 2026 財報電話會議摘要：管理層預期中國占 2026 年營收約 45%（前一年 49%）
  - 來源：MarketBeat, Camtek Q2 earnings call highlights（as_of 2026-08-10）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：Simply Wall St 敘事指亞洲市場與客戶集中帶來地緣風險
  - 來源：Simply Wall St narrative（as_of 2026-06-01）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Camtek 20-F 風險因素自述：市場技術變動快，若未能預測或跟上技術變化或競爭對手產品，營收可能受損；採用新技術也可能造成存貨沖銷。未點名特定替代技術。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D Risk Factors（as_of 2026-03-19）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：APCNDT 2026 摘要（Applied Materials）描述以 3D X-ray CT 與 laminography 檢查 hybrid bonding 界面、對位偏差與空洞，為光學檢測以外的技術路線
  - 來源：APCNDT 2026 abstract (airdrive.eventsair.com)（as_of 2026-01-01）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":286.0,"bear_5y_price":61.5,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":71.0,"ev5y_pct":69.7,"irr_base_pct":11.3,"asym_ratio":4.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.63,"pe":26.74,"basis":"FY2026E 共識 EPS（依季度數字判斷為非 GAAP），終端倍數同樣用當年度 EPS"},"eps":{"bull":[5.4,6.6,8.2,9.5,11.0],"base":[4.95,5.9,6.9,7.0,8.3],"bear":[4.3,3.6,3.1,3.5,4.1]},"pe":{"bull":26,"base":20,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CAMT_Q2_2026_Earnings_Call_20260810.md
- 2026-08-10｜CEO｜guidance：CEO 給 Q3 營收區間 1.58～1.60 億美元（原話："range of $158 million to $160 million"）
- 2026-08-10｜CFO｜guidance：CFO 重述 Q3 財測，並說 Q4 季增雙位數、2027 持續成長（原話："sequential double-digit growth in Q4 and further growth into 2027."）
- 2026-08-10｜CEO｜guidance：CEO 說今年初至今累計訂單超過 6 億美元（原話："orders received year-to-date to more than $600 million"）
- 2026-08-10｜CEO｜guidance：CEO 預期下半年先進封裝業務較上半年成長約 45%（原話："expected to drive approximately 45% growth"）
- 2026-08-10｜CEO｜guidance：CEO 預期 Q4 先進封裝營收約比 Q1 高 70%（原話："approximately 70% higher than the first quarter"）
- 2026-08-10｜COO｜guidance：COO 說年底先進封裝約占營收 80%（原話："80% of our revenues will go towards Advanced Packaging"）
- 2026-08-10｜COO｜guidance：COO 被問全年先進封裝成長，答「成長 70%」（原文脈絡為今年）（原話："The Advanced Packaging will grow by 70%"）
- 2026-08-10｜CFO｜guidance：CFO 澄清 2025 到 2026 先進封裝與 AI 相關業務成長區間（原話："anywhere between 35% to 45% between the Advanced Packaging"）
- 2026-08-10｜CFO｜risk：CFO 提醒去年是紀錄年，今年基期高（原話："Bear in mind that last year was a record"）
- 2026-08-10｜CFO｜guidance：CFO 預期今年中國營收占比約 45%（去年 49%）（原話："China to be anywhere between 45 -- 45-ish kind of"）
- 2026-08-10｜CFO｜margin：CFO 給年底毛利率目標 52.5%～53%（Q2 為 51.4%）（原話："anywhere between 52.5% to 53% exiting the year"）
- 2026-08-10｜CFO｜margin：CFO 給年底營業利益率 30%～32%（Q2 為 27%）（原話："operating margin of between 30% to 32%"）
- 2026-08-10｜CFO｜margin：CFO 說獲利指標將隨產品組合與槓桿逐步改善（原話："improvement across all profitability metrics in the next few quarters"）
- 2026-08-10｜CFO｜commitment：CFO 說費用會增加，但幅度不會超過營收成長（原話："definitely plan to see some increase in our OpEx level"）
- 2026-08-10｜CFO｜commitment：CFO 說毛利率與營業利益率都計畫改善，營業利益率幅度更大（原話："but even more the operating margin levels"）
- 2026-08-10｜CEO｜margin：CEO 報 Q2 營收紀錄 1.33 億美元（原話："Second quarter revenue reached a record of $133 million"）
- 2026-08-10｜CEO｜product：CEO 說 Q2 系統營收約一半來自新一代平台 Eagle G5 與 Hawk（原話："approximately 50% of our systems revenue"）
- 2026-08-10｜COO｜product：COO 說客戶從 Eagle 轉換到 Gen5（原話："want to stay with the Eagle, switching over to the Gen5"）
- 2026-08-10｜COO｜product：COO 說 ASP 會隨產品組合改善，但無法拆解數字（原話："there is going to be an improvement in ASPs as we go along"）
- 2026-08-10｜CEO｜product：CEO 說 Hawk 搭配光學與 AI 技術，可切入更多製程步驟（含混合鍵合）（原話："enabling us to penetrate additional process steps"）
- 2026-08-10｜COO｜product：COO 說 NanoProf 目標擴大量測市場版圖（原話："significantly increase our footprint in the metrology area"）
- 2026-08-10｜CEO｜customer：CEO 拆解訂單：約 80% 為先進封裝（原話："80% of these orders are Advanced Packaging applications"）
- 2026-08-10｜CEO｜customer：CEO 說 OSAT 占訂單逾 50%（原話："OSATs accounted for more than 50% of our total order intake"）
- 2026-08-10｜COO｜customer：COO 說 6 億美元訂單中 HBM 廠商占逾 20%（原話："20% is from HBM players"）
- 2026-08-10｜COO｜customer：COO 說光子學占 6 億美元訂單 5%（原話："orders that we talked about, 5% is photonics."）
- 2026-08-10｜COO｜guidance：COO 預期 2027 光子學訂單占比高於 5%（原話："'27 will be more than the 5% I just mentioned"）
- 2026-08-10｜COO｜customer：COO 說非先進封裝業務穩定（原話："the business is stable"）
- 2026-08-10｜COO｜customer：COO 說有顯著的 CMOS 影像感測器訂單（原話："have some orders for CMOS Image Sensors that are significant"）
- 2026-08-10｜COO｜customer：COO 說中國業務過去幾年穩定（原話："our China business has been, I would say, stable"）
- 2026-08-10｜COO｜competition：COO 回應競爭者說法，稱在 OSAT 市場居主導地位（原話："dominant position in the OSATs market"）
- 2026-08-10｜COO｜competition：COO 說部分領域在搶市占（原話："I think we are gaining share in certain areas"）
- 2026-08-10｜COO｜competition：COO 說未來一年成長與 WFE 相當或更好（原話："I believe that we will be doing similar or better than the WFE"）
- 2026-08-10｜COO｜risk：COO 說 2027 預測尚早，完整輪廓需再 1～2 季（原話："at least 1 more quarter to 2 quarters"）
- 2026-08-10｜COO｜commitment：COO 說供應鏈與產能就緒，無阻礙（原話："we don't see any issues or obstacles when we discuss capacity"）
- 2026-08-10｜COO｜guidance：COO 說 2026 的新訂單很少，多數為 2027 交期（原話："'26, yes, but there are very few."）
- 2026-08-10｜CEO｜capital_allocation：CEO 說持續擴充製造產能（原話："expanding our manufacturing capacity"）
- 2026-08-10｜CFO｜capital_allocation：CFO 說 R&D 增加源於 Visual Layer 收購以強化 AI（原話："the Visual Layer acquisition in order to strengthen our AI offering"）
- 2026-08-10｜CFO｜capital_allocation：CFO 報現金與有價證券餘額（原話："June 30, 2026, were $815.8 million"）
- 2026-08-10｜CFO｜risk：CFO 報 DSO 升至 105 天（原話："DSO increased to 105 days"）
- 2026-08-10｜CFO｜capital_allocation：CFO 預期存貨將增加以支應營收成長（原話："grow in the coming quarters to support the forecasted"）

### CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md
- 2026-10-14｜Rafi Amit｜guidance：Q3 營收預告區間（原話："Revenue expected in Q3 is $160 million to $161 million."）
- 2026-10-14｜Rafi Amit｜guidance：2027 營收展望超過 $800M，首次提前一年給（原話："Revenue outlook for 2027 is more than $800 million."）
- 2026-10-14｜Rafi Amit｜guidance：3 年內營收翻倍至 $1.2B，CAGR 約 26%（原話："reaching $1.2 billion representing a CAGR about 26%"）
- 2026-10-14｜Rafi Amit｜guidance：$1.2B 目標屬純有機成長（原話："this target is based on organic growth without factoring in"）
- 2026-10-14｜Moshe Eisenberg｜guidance：年初至今新增訂單累計超過 $800M，動能持續（原話："the order momentum continues"）
- 2026-10-14｜Moshe Eisenberg｜guidance：新增訂單中先進封裝占約 80%（原話："80% comes for advanced packaging"）
- 2026-10-14｜Moshe Eisenberg｜customer：訂單中 OSAT 占略超過五成（原話："a little over 50% came from OSATs"）
- 2026-10-14｜Moshe Eisenberg｜margin：營業利益率由 30% 到 $1.2B 時 34–36%（原話："the operating margin from 30% last year to 34% to 36%"）
- 2026-10-14｜Moshe Eisenberg｜margin：毛利率目標 55–56%（原話："Gross margin goes from 51% to 52% nowadays to 55% to 56%"）
- 2026-10-14｜Moshe Eisenberg｜margin：產品組合拆解：加 3.4 點毛利（原話："they will add around 3.4 points to the profitability"）
- 2026-10-14｜Moshe Eisenberg｜margin：SG&A 槓桿貢獻 2.4 點（原話："this will contribute around 2.4 points"）
- 2026-10-14｜Moshe Eisenberg｜margin：R&D 投入拿回略多於 1 點（原話："take back a little over 1 point from the profitability"）
- 2026-10-14｜Moshe Eisenberg｜margin：模型假設 R&D 約占營收 10%（原話："we assume that R&D will account for around 10% of the mix"）
- 2026-10-14｜Moshe Eisenberg｜guidance：成長三引擎：檢測與量測主業貢獻約 $380M（原話："will contribute around $380 million to the growth"）
- 2026-10-14｜Moshe Eisenberg｜guidance：軟體與服務由 $28M 增至 $140M 以上、占 12%（原話："to over $140 million, which will be 12% of the mix"）
- 2026-10-14｜Ramy Langer｜product：軟體產品 2027 起產生營收（原話："we plan to generate revenues from this product starting 2027"）
- 2026-10-14｜Moshe Eisenberg｜product：2025 年服務營收成長 40%（原話："we grew 40% the service revenue"）
- 2026-10-14｜Moshe Eisenberg｜commitment：管理層稱 3 年模型非明確承諾、為基準情境（原話："we didn't commit to specific 3 years"）
- 2026-10-14｜Eyal Segev｜guidance：IR 與分析師口徑：2027 為 outlook 非 guidance（原話："this is not a guidance. This is an outlook."）
- 2026-10-14｜Ramy Langer｜commitment：管理層稱歷來預測保守且未失手（原話："we ever missed one of our forecast in the last few years"）
- 2026-10-14｜Ramy Langer｜guidance：WFE 更強則難以現在調整數字（原話："it's too early now to give a different number"）
- 2026-10-14｜Moshe Eisenberg｜guidance：2027 中國預期不低於今年（原話："at least as strong as it is this year in 2027"）
- 2026-10-14｜Rafi Amit｜customer：中國約占營收 45%（原話："China is around 45% of our business"）
- 2026-10-14｜Rafi Amit｜risk：本地競爭者在中國增加（原話："competition more and more from the locals"）
- 2026-10-14｜Moshe Eisenberg｜risk：WFE 可能進入資本支出消化期（原話："the WFE will get into a CapEx digestion period"）
- 2026-10-14｜Ramy Langer｜competition：競爭對手宣布 OSAT 訂單，公司稱收到不遠小於的同客戶大單（原話："we have received a very significant order"）
- 2026-10-14｜Ramy Langer｜competition：預期 2028 年份額更大（原話："I'm expecting that our share in '28 will be larger."）
- 2026-10-14｜Ramy Langer｜competition：台灣 OSAT 份額預期至少 50%（原話："I expect that our share is at least 50%"）
- 2026-10-14｜Ramy Langer｜competition：否認客戶對 3D 凸塊量測有猶豫（原話："we do not see this hesitancy"）
- 2026-10-14｜Ramy Langer｜competition：大型對手進入 2D 檢測是競爭（原話："we will need to address and work very hard"）
- 2026-10-14｜Ramy Langer｜competition：2D 檢測占 2026 年出貨 85%（原話："85% of our tools were sold for inspection applications"）
- 2026-10-14｜Eyal Segev｜product：第 10 代凸塊高度感測器明年推出（原話："next-generation sensor, which will be released next year"）
- 2026-10-14｜Eyal Segev｜product：HBM5 仍沿用凸塊而非混合鍵合（敘事變化）（原話："It's going to continue to be based on bumps."）
- 2026-10-14｜Eyal Segev｜product：混合鍵合進度慢於預期（原話："it's ramping up slower than we expected"）
- 2026-10-14｜Ramy Langer｜product：2030 年 SAM 約 $6B（原話："an increased SAM of about $6 billion in 2030"）
- 2026-10-14｜Ramy Langer｜customer：訂單約 5% 來自光子（原話："about 5% are going to photonics"）
- 2026-10-14｜Ramy Langer｜customer：光子主要放量在 2028 年之後（原話："more of a '28 and onwards"）
- 2026-10-14｜Ramy Langer｜customer：2027 全年交貨檔期已在排（原話："we are getting to a slot for all of '27"）
- 2026-10-14｜Moshe Eisenberg｜capital_allocation：現金超過 $800M 用於成長與併購（原話："We have over $800 million to support the growth"）
- 2026-10-14｜Lior Aviram｜capital_allocation：過去 1.5 年看過逾百件併購機會（原話："we've looked at over 100 opportunities"）
- 2026-10-14｜Rafi Amit｜capital_allocation：併購不分散管理層對核心有機成長的注意力（原話："extremely careful not to divert management attention"）
- 2026-10-14｜Lior Aviram｜capital_allocation：Visual Layer 整合完成（原話："the PMI has already been completed"）
- 2026-10-14｜Ramy Langer｜risk：上調空間尚無法量化（原話："it's too early to size the upside"）
- 2026-10-14｜Rafi Amit｜commitment：產能不構成限制、可供應更多（原話："Our operational infrastructure will be able to supply more"）

### 問答異常語氣（迴避／改口／保留）
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Brian Chin 問 Hawk/Gen5 占比提高下，下半年 30%+ 成長中 ASP 貢獻如何拆解｜答法：COO 稱事前沒算、無法給準確答案，只說 ASP 會改善
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Matt Prisco 問 2027 能見度與成長是否可持續｜答法：COO 稱現在給預測太早，不給 2027 數字，只說客戶樂觀
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Matt Prisco 問中國營收走勢與競爭環境｜答法：COO 只說穩定、持續投資，並稱「這大致是我現階段能評論的」，未答競爭
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Shane Brett 追問全年先進封裝成長（約 30%）與 HPC 成長｜答法：COO 先答先進封裝今年成長 70%，經 CFO 追問後改為 35%～45%，數字前後不一致
- CAMT_Q2_2026_Earnings_Call_20260810.md｜問：Jim Schneider 問 DRAM／HBM 曝險與中國業者（如 CXMT）｜答法：COO 給 HBM 占訂單比例，但對 CXMT 等客戶名稱未回答，稱不能談客戶名
- CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md｜問：Auguste Richard（Northland）：把 2027 年 $800M 依預測／訂單／預付三層拆分，並問交貨檔期｜答法：未給拆分數字，稱 backlog 為 meaningful number 但 We did not say the numbers，改談 pipeline 定義與公司歷來預測紀錄
- CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md｜問：Blayne Curtis（Jefferies）：CPO 與 MPO 時程及公司在 PIC 的定位｜答法：只答訂單約 5% 為光子、放量在 2028 後，未直接談 MPO 或時程判斷
- CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md｜問：Matt Prisco（Cantor）：若 2027 有上調空間，來源排序與能否供應｜答法：稱有 potential upside 但表示太早量化，要等 1–2 季，未給排序或數字
- CAMT_Analyst_Investor_Day_Camtek_Ltd_20261014.md｜問：Charles Shi（Needham）：客戶對專用 3D 凸塊量測有猶豫、HBM 降規格｜答法：直接否認看到猶豫並質疑資訊來源，同時承認 NVIDIA 等傾向降低單模組記憶體密度

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 3 | 3 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260906","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤ $125（FY2027E 本益比約 25.5 倍、Base 五年年化 ≥ 12%）且 Q3 營收 ≥ $158M 兌現→首倉 1/3；或 FY2027 共識 EPS 上修 ≥ 10% 且股價未過 $165→重跑","irr_base_pct":8.7,"ev5y_pct":42.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"-","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.59,"ev5y_pct":42.8,"irr_base_pct":8.7,"max_dd_pct":-55,"bull_5y_price":330.0,"bear_5y_price":86.4,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤ $125（FY2027E 本益比約 25.5 倍、Base 五年年化 ≥ 12%）且 Q3 營收 ≥ $158M 兌現→首倉 1/3；或 FY2027 共識 EPS 上修 ≥ 10% 且股價未過 $165→重跑","price_at_dd":145.72,"archetype":"品質複利成長","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CAMT","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Camtek Ltd."},"oneliner":"股價半年跌 53%、共識沒動，FY2027 本益比 19 倍買的是 8 億美元展望能否兌現；管理層不拆在手訂單，毛利率也沒做到 8 月的說法，下一個驗證點是 2026 Q4 財報。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺先進封裝客戶為守良率付的檢測與量測錢，利潤卡在專用機台與約 4,000 台裝機基礎；Q3 約八成營收來自先進封裝，多數由 AI 需求帶動。","reasoning":"Q3 營收 1.613 億美元，年增 28%，GAAP 毛利率 50.0%，非 GAAP 毛利率 51.1%、營益率 29.5%；Q2 到 Q3 增量營益率約 41%（營業利益多 1,150 萬美元，營收多 2,810 萬美元）。先進封裝約占八成，其中手機等一般封裝平均每季約 15%；OSAT 占訂單略高於五成。單點依賴不在單一客戶，FY2025 最大客戶僅 11%，而在 AI 資本支出與中國：亞洲占 Q3 營收 95%，中國 2026 年約 45%。產業時鐘在擴張期：年初至 10 月中訂單逾 8 億美元，對前三季營收約 4.15 億美元，訂單出貨比約 1.9 倍（期間不完全對齊），客戶把檔期排到 2027，零組件短缺與調價同時出現，已有擴張後段的特徵。可能看錯之處：訂單金額是管理層自述，且沒有拆出確定訂單與預測。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_non_gaap_operating_margi","f_kpi8_gaap_gross_margin","f_kpi9_guidance_q4_2026_revenue"],"verdict_values":{"revenue_quality":"以設備一次性銷售為主，服務 2026 年約 4,000 萬美元，約占營收 7%，年增 35%～40%；軟體目前接近零，2027 Q1 才開始。交貨檔期排到 2027，但管理層未揭露在手訂單金額。","unit_econ_note":"單機 ASP 與出貨量事實表未涵蓋。Hawk 與 Eagle G5 占系統營收約 57%，高於 Q2 的約 50%，這是毛利率的主要上行來源；3 年目標毛利率 55%～56%、營益率 34%～36%。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"FY2022～FY2025 營收 3.21 億增至 4.96 億美元，只有 FY2023 小跌 1.72%，毛利率 46.81%～50.46%；盈利能力穩，但 2027 成長高度綁 AI 封裝資本支出，帶循環性。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久，但 2027 檔期搶訂帶週期成分：SEMI 2026 年中預測設備銷售到 2028 年仍成長，CFO 在 2026-10-14 投資人日也提醒可能進入資本支出消化期；這是 Bear 機率取 30% 的依據之一。","bargaining":{"up":"通用零組件（記憶體、CPU、搬運機構件）短缺漲價，Q3 已壓到毛利率；COO 說多數有雙來源，單一來源比例事實表未涵蓋。","down":"客戶分散，FY2025 最大客戶 11%；COO 說客戶已理解因零組件調價，幅度未揭露，能否轉嫁要看 2027 毛利率。","geo":"亞洲占 Q3 營收 95%，中國約 45%；製造與研發集中在以色列，歐洲擴產作對沖。"},"profit_pool_dir":"利潤往 AI 先進封裝移動；5 年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"可服務市場（2027）","value":"20 億美元以上，較目前增約 5 億美元（二手摘要，管理層口徑）"},{"item":"可服務市場（2030）","value":"約 60 億美元（2026-10-14 投資人日，COO），未經第三方驗證"},{"item":"CAMT 滲透率（2027）","value":"8 億÷20 億＝約 40%"},{"item":"CAMT 滲透率（目標口徑）","value":"12 億（約 2029 年）÷60 億（2030 年）＝約 20%，年份不完全對齊，且前提是新增市場都打得進去"},{"item":"營業利益池 5 年占比變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"穩定：裝機基礎與專用機台還守得住，但大型同業已在 OSAT 拿到訂單，漲價能力要到 2027 才看得出來。","reasoning":"機制是專為先進封裝客製的 2D 檢測與 3D 凸塊量測，加上約 4,000 台裝機與放量期不願換機的認證成本。可比軸用利潤率，因為事實表沒有 ROIC：毛利率 50.03%，低 NVMI 7.35 個百分點、低 KLAC 11.44 個百分點、與 ONTO 差 0.33 個百分點；GAAP 營益率 23.15%，高 ONTO 9.34 個百分點、低 NVMI 6.89 個百分點（ONTO 為截至 6 月的資料）。份額數字全部是公司自述，不足以支持溢價。2026-10-14 COO 預期台灣 OSAT 份額至少 50%，同時承認對手在同一客戶拿到訂單，這是客群開始多家供應，還不是份額下滑的證據；若之後 OSAT 占訂單跌破 45%，我的方向判斷就錯了。產業態勢裁決為雙向拉鋸：競爭者變多，需求與檢測步驟也在增加。AI 軟體長在自家機台上，屬強化而非替代，2027 才有營收，尚無法算淨增量。","fact_refs":["f_peer_camt_gross_margin_pct","f_peer_camt_operating_margin_pct","f_peer_onto_gross_margin_pct","f_peer_onto_operating_margin_pct","f_peer_nvmi_gross_margin_pct","f_peer_nvmi_operating_margin_pct","f_peer_klac_gross_margin_pct","f_peer_klac_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"先進封裝專用檢測與量測機台＋約 4,000 台裝機基礎＋放量期的認證黏著度","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力穩定：Q3 營收高於指引，Hawk 與 Eagle G5 占系統營收升到約 57%，過去 17 次指引調整有 13 次上調。定價力穩定但未獲證實：調價才開始，Q3 毛利率 51.1% 還低於預期。競爭屬客群範圍開始被多家供應，不是方向受損；沒有來源指出最大客戶份額下滑。","competitor_notes":[{"name":"ONTO","strategy_note":"毛利率與 CAMT 幾乎相同，營益率低 9 個百分點，是量測與檢測的直接對手；是否為投資人日提到的 OSAT 得標者，事實表未涵蓋。"},{"name":"NVMI","strategy_note":"毛利率與營益率都高於 CAMT，顯示製程控制有更好的定價空間，CAMT 的 55%～56% 目標並非行業天花板。"},{"name":"KLAC","strategy_note":"規模與利潤率遠高於 CAMT，COO 承認大型對手正進入 2D 檢測；關鍵在能否把前段關係帶進 OSAT。"},{"name":"中國本土設備商","strategy_note":"主攻低階並低價供貨；2026-10-14 CEO 說本地競爭增加，2026-11-04 管理層說看不到威脅，要用中國訂單驗證。"}],"peer_na_reason":"事實表同業對照只有利潤率與研發密度，沒有 ROIC 與投入資本，改用毛利率與營業利益率比較。","threats":[{"level":"🟡","text":"大型同業切入 OSAT 的 2D 檢測。2D 占 2026 年出貨約 85%，對手已在同一客戶拿到訂單；目前是單點競爭，若第二家主要 OSAT 也開始多家採購，升為生態攻擊。","p":"40%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"中國本土業者以低價攻低階市場。2026-10-14 CEO 說本地競爭增加，2026-11-04 管理層說看不到威脅，並稱中國 2027 訂單至少持平。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"X-ray CT 等路線切入混合鍵合檢測，加上技術快速變動可能造成存貨沖銷。證據只有一份會議摘要，混合鍵合 2028 後才有規模，目前不構成架構替代。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"無法判定：事實表未涵蓋投入資本","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是封裝產線工程師，決策者是良率與製程主管，付款者是 OSAT 與晶片廠的資本支出預算。良率損失代價高，屬於需要而非想要，但機台可以延後買：COO 2026-11-04 說有些客戶提前下單只是為了確保檔期。需求持久，時點會波動。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一製程步驟衡量。COO 2026-11-04 說部分客戶在快速放量時不願換機重新認證，這是轉換成本的證據；但同一 OSAT 已向對手下單，代表新增步驟可以多家供應。重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"毛利率 50.03% 低於 NVMI 與 KLAC，上游零組件漲價先吃到毛利，調價要到 2027 才見效。客戶以大型 OSAT 為主，能否多拿價值取決於新機種帶來的新功能。"},{"item":"社會容忍度","level":"🟢","text":"這是企業資本財，沒有社會定價壓力；政治限制來自出口管制，已列入中國風險處理。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。缺投入資本、折舊與營運資金變動，不自行推估；Q3 營業現金流 7,110 萬美元，現金季增 6,130 萬美元，顯示資本需求低，但不足以算出上界。"}}}},"q3_growth":{"verdict":"中等：以 2027 年 8 億美元對 20 億美元以上的可服務市場算，滲透率已約 40%，後面要靠管理層口徑的新市場，混合鍵合又比預期慢。","reasoning":"成長以量為主，Hawk 與 Eagle G5 組合與 2027 開始的調價是第二層，併購與回購幾乎沒有貢獻。FY2026E 到 FY2028E 共識 EPS 兩年年化 27.7%（3.63 到 5.92 美元）；FY2025 只有 GAAP 1.04 美元，當年營業利益率沒降、淨利卻減半，判斷受非營業項目壓低（事實表未拆），不能當基期，所以三年年化不採用。FY2027 共識營收年增 34.8%、EPS 年增 40.2%，差距來自營業槓桿。內生上界因事實表未涵蓋投入資本而算不出，缺口無法歸因，長期信心上限取中。第二條曲線目前都還不夠硬：混合鍵合 2027 貢獻有限、2028 起才有意義，投資人日也承認比預期慢；光子約占訂單 5%，主要放量在 2028 後；軟體與服務目標 3 年 1.4 億美元，其中軟體 4,000 萬美元是估計值。衰退信號只亮一項，逐季毛利率同比與份額屬資料缺口，沒有計入；TTM 毛利率 50.03% 低於 FY2025 的 50.46%，值得盯。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi9_guidance_q4_2026_revenue","f_peer_camt_gross_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量為主；新機種組合與 2027 起的調價為輔，併購與回購幾乎沒有貢獻。","runway_years":"已過 30%：FY2027 展望 8 億美元對可服務市場 20 億美元以上，約 40%","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋投入資本、折舊與營運資金，無法推算；情境樹按超出內生上界處理，Bear 機率取 30%。","segments":[{"item":"先進封裝（Q3 營收占比）","value":"約 80%，多數由 AI 需求帶動"},{"item":"一般封裝（手機等）","value":"平均每季約 15%，COO 2026-11-04 說未見走弱"},{"item":"HBM","value":"占 6 億美元訂單逾 20%（2026-08-10 COO）；兩家客戶 2026～2027 合計逾 2.6 億美元"},{"item":"光子","value":"約占訂單 5%，主要放量在 2028 後"},{"item":"服務","value":"2026 年約 4,000 萬美元，年增 35%～40%"},{"item":"軟體","value":"目前接近零，2027 預期達雙位數百萬美元，3 年目標約 4,000 萬美元"}],"decay_signals":["EPS 成長高於營收成長逾 5 個百分點：FY2027 共識 EPS 年增 40.2%、營收年增 34.8%，差 5.4 個百分點；原因是營業槓桿，若毛利率沒回升，這段差距會先消失。"]}}},"q4_capital":{"verdict":"現金多、紀律待驗：8.77 億美元現金主要留給成長與併購，近一年沒有配息，SBC 稀釋輕。","reasoning":"FCF 對淨利轉換率 FY2022 至 FY2025 依序 0.62、0.90、0.94、2.51 倍，FY2025 偏高是因淨利被壓低，不是現金變好。Q3 SBC 570 萬美元，占營收 3.5%，年化約 2,280 萬美元，對市值 45.35 億美元約 0.50%。現金 8.771 億美元，以稀釋股數 5,150 萬股算每股約 17 美元，占股價約 17.5%。事實表的現金 6.07 億美元沒有包含公司口徑的全部存款與有價證券，用公司口徑算 EV 約 41.5 億美元，比表上 44.2 億美元低約 6%。可轉債條款與現金去向四分事實表未涵蓋，轉換價若高於現價，這筆債要還現金而不是轉股，所以現金不能全部算成安全邊際。併購看過逾百件，Visual Layer 金額未揭露、整合已完成，報酬還要等 2027 軟體營收。","fact_refs":["f_kpi5_operating_cash_flow","f_kpi6_share_based_compensation","f_kpi7_cash_deposits_marketable","f_net_debt_m","f_shares_diluted_m","f_ev_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"Visual Layer 金額未揭露，2027 才有軟體營收，已實現報酬無從計算。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購紀錄；近 365 天無配息。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 570 萬美元，年化 2,280 萬美元，對市值 45.35 億美元約 0.50%，低於 1.5%；以 SBC 金額代替淨稀釋股數，股數變動事實表未涵蓋。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"近 365 天無配息，回購與現金去向四分事實表未涵蓋，目前成長也不靠併購支撐，無資料可展開。"}}}},"q5_valuation":{"verdict":"現價要 FY2027 約 5 美元的盈餘站得住，FY2031 還要做到約 8.5 美元才有年化 12%；我相信前者，後者要看毛利率與 12 億美元目標。","reasoning":"要年化 12%，五年後股價要到約 171 美元；用 20 倍終端本益比，FY2031 EPS 要約 8.55 美元，從 FY2026E 3.63 美元算是年化 18.7%。我的 Base 是 8.30 美元，略差一點。FY2026E 本益比 26.74 倍、FY2027E 19.07 倍，兩年年化 27.7% 下 PEG 0.97。Trailing 本益比 36.48 倍在 4 個年度端點的 23.3 分位，但 P/S 8.33 倍在 59.7 分位、EV/S 8.12 倍在 51.6 分位，股價砍半後按營收看並不便宜，便宜只出現在盈餘口徑。五年歷史分位事實表未涵蓋。賣方目標價多在 8 月以前（均值約 187.58 美元，現價低於均值 48%），早於這波下跌，不拿來支持裁決；各來源最高 220 美元對最低 80 美元，全距約 2.75 倍，信心相應下調。12 個月上檔用 FY2027E 4.95 美元×22 倍＝108.9 美元，約 +12.2%；3 年用 FY2029E 6.90 美元×20 倍＝138 美元，約 +42.2%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"Fwd P/E 為主，用 FY2026E 與 FY2027E 共識 EPS；事實表未涵蓋同業倍數。","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率與研發密度，沒有本益比或 EV/S，無法做倍數比較，需補資料。"},"fwd_pe":26.74,"peg":0.97,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2026E 本益比 26.74 倍、FY2027E 19.07 倍，PEG 0.97 數字上便宜；FY2027E 本益比對 FY2028E 成長 16.3% 的 PEG 則是 1.17。P/S 仍在 4 個年度端點的 59.7 分位，便宜只出現在盈餘口徑，而盈餘分母正是爭點，所以評為中性，不給便宜。五年分位事實表未涵蓋，留空。","upside_short_pct":12.2,"upside_mid_pct":42.2,"denominator_disputed":true,"denominator_note":"FY2025 GAAP EPS 1.04 美元被壓低，不能當基期，已改用前瞻口徑。FY2027E 5.09 美元依賴 8 億美元展望，這是展望不是財測，管理層也沒拆在手訂單；市場砍半股價而共識未動，分母本身就是爭點，便宜的論證不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把 2027 搶檔期的訂單當成真實需求。","reasoning":"衰退信號亮一項，價值陷阱風險列中等。週線收在 104 週均線下、250 週均線上（97.05 對 115.43 與 77.86），26 週跌 52.78%，RSI 30.21，動能沒有過熱，也沒有止跌訊號。事實表沒有解釋這波下跌的原因，也沒有同業同期股價，這是本次最大的資料缺口。核心可守：FY2023 下行時營收只跌 1.72%、GAAP 營益率仍有 20.74%，但樣本只有一次，當時的 AI 封裝占比事實表未涵蓋。波動按深回撤準備，不因波動本身砍倉。法說上 TCB 延遲的提問，COO 只說沒看到變化，沒有正面解釋。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"一項衰退信號亮燈，FY2027 盈餘分母待驗證"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.63,"pe":26.74,"basis":"FY2026E 共識 EPS（依季度數字判斷為非 GAAP），終端倍數同樣用當年度 EPS"},"eps":{"bull":[5.4,6.6,8.2,9.5,11.0],"base":[4.95,5.9,6.9,7.0,8.3],"bear":[4.3,3.6,3.1,3.5,4.1]},"pe":{"bull":26,"base":20,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"max_dd":{"lo":-55,"hi":-35,"basis":"Bear 谷底 FY2029E EPS 3.10 美元×15～18 倍＝46.5～55.8 美元，對現價跌 42%～52%；較淺的 −35% 約 63 美元，對應 FY2028E Bear EPS 3.60 美元×17.5 倍。250 週均線 77.86 美元是約 −20% 的第一道支撐；近 26 週已跌 52.78%，說明這個深度並非極端。","trigger_time":null},"basis":{"bull":"2029 年前達成 12 億美元目標、營益率 35%～36%，混合鍵合與軟體接棒；終端 26 倍對應仍有雙位數成長。事實表未涵蓋同業本益比，無法附同業現值對照。","base":"2027 約 8 億美元，12 億美元目標晚約兩年達成，FY2030 有一年消化期，營益率 33%～34%，稀釋股數由 5,150 萬股緩升；終端 20 倍低於現在 FY2026E 的 26.74 倍，事實表未涵蓋同業本益比。","bear":"2027 檔期取消或遞延，營收低於 7.5 億美元，FY2029 谷底 EPS 3.10 美元；大型同業分走 2D 份額、中國自給率上升。機率 30%：內生上界無法驗證、訂單未拆分、CFO 自己提過資本支出消化期。終端 15 倍對應成長降至 10% 的倍數。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"COO 2026-11-04 說部分客戶提前一年下單，並非現在就需要機台，只是要確保檔期；投資人日未把 8 億美元拆成預測、訂單與預付；CFO 提過資本支出消化期；Needham 分析師點出 HBM 封裝的 TCB 延遲。","assumption":"2027 的檔期訂單大多是確定需求，不會遞延或重複下單。","consequence":"若訂單遞延，FY2027 營收低於 7.5 億美元，FY2029 EPS 谷底約 3.10 美元，五年後股價約 61.5 美元，約 −37%；若再疊加中國受限，虧損接近 50%。","ruling":"採納。與唯一致命數字同源，Bear 機率 30%，首倉只放 1/3。","watch":"預收款與合約負債、存貨成長率減營收成長率、FY2027 展望","evidence_refs":["supply_demand_durability#2"]},{"view":"論點失敗","evidence":"中國 FY2025 占營收 49%、2026 約 45%，COO 說 2027 至少持平；20-F 提醒出口管制即使不直接適用也可能壓低需求；CEO 2026-10-14 承認本地競爭增加。","assumption":"中國需求與份額 2027 不掉。","consequence":"中國營收少 30%，以 FY2027 約 3.6 億美元估算少 1.08 億美元，EPS 約少 0.96 美元，約 19%。","ruling":"採納為 Bear 的成分，不設為唯一致命數字：這需要一次政策轉折，FY2027 展望下修的傳導更直接。","watch":"中國營收占比與絕對金額、美國商務部新規","evidence_refs":["customer_concentration_credit#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"view":"論點失敗","evidence":"26 週跌 52.78%，FY1 共識近 3 個月卻上修 0.55%，背離原因與同業同期股價事實表都未涵蓋。","assumption":"這波下跌主要是週期恐懼，不是市場掌握了尚未反映在共識的壞消息。","consequence":"若賣壓來自未公開的訂單遞延或份額流失，FY2027 共識會補跌，現價不是底部。","ruling":"採納。不可裁決至 2027 年 2 月財報，在此之前只放首倉，不因低價加碼。","watch":"Q4 財報後的共識修正、賣方目標價更新"},{"view":"論點成功但股東經濟變差","evidence":"Q3 毛利率 51.1% 低於 CFO 8 月給的年底 52.5%～53% 路徑，CFO 歸因零組件與謝克爾升值；管理層另有 8 億美元以上現金用於成長與併購，過去 1.5 年看過逾百件。","assumption":"營收達 12 億美元時毛利率能到 55%～56%，現金不會買貴。","consequence":"毛利率少 4 個百分點，12 億美元營收下 EPS 約少 0.8 美元，約一成；一筆高價併購會再傷報酬。","ruling":"部分採納。Base 營益率只給 33%～34%，低於目標 34%～36%。","watch":"季度非 GAAP 毛利率、單筆併購是否超過市值 5%","evidence_refs":["geo_supply_chain#1"]},{"view":"價格已反映太多","evidence":"股價砍半後 P/S 8.33 倍仍在 4 個年度端點的 59.7 分位，EV/S 約在中位；FY2026E 本益比 26.74 倍還高於我給的終端 20 倍。","assumption":"高成長期間本益比能守住 20 倍以上。","consequence":"若市場繼續用週期頂部盈餘定價，FY2027E 4.95 美元×15 倍＝74 美元，還有約 24% 下檔。","ruling":"部分採納。估值結論只給中性，不給便宜；Base 已假設本益比由 26.74 倍降到 20 倍。","watch":"FY2027E 本益比、Q4 財報後的共識修正"}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 145.72 → 本次 97.05（-33.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=145.72","side_b":"本次 price_at_dd=97.05","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 145.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 145.72 美元：Bull 價 330、Bear 價 86.4，五年期望值 +42.8%，基準年化 8.7%，不對稱比 2.59","side_b":"本次情境、股價仍用 145.72 美元：Bull 價 286、Bear 價 61.5，五年期望值 +13.0%，基準年化 2.6%，不對稱比 1.39","ruling":"先換情境、股價不動：五年期望值少 29.8 個百分點，基準年化少 6.1 個百分點。不對稱比由 2.59 變為 1.39。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 145.72 美元：五年期望值 +13.0%，基準年化 2.6%，不對稱比 1.39","side_b":"本次情境、股價 97.05 美元：五年期望值 +69.7%，基準年化 11.3%，不對稱比 4.43","ruling":"再換股價、情境不動：起點價下跌 33.4%，五年期望值多 56.7 個百分點，基準年化多 8.7 個百分點，不對稱比由 1.39 升到 4.43。合計五年期望值比前份多 26.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前次進場條件已達成，重訂首倉門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤ $125（FY2027E 本益比約 25.5 倍、Base 五年年化 ≥ 12%）且 Q3 營收 ≥ $158M 兌現→首倉 1/3；或 FY2027 共識 EPS 上修 ≥ 10% 且股價未過 $165→重跑","side_b":"股價 ≤ $100 且 2027 營收展望 ≥ $800M→首倉 1/3；2026 Q4 毛利率 ≥ 51% 且展望不降→加至 2/3；股價 > $125 而財報未驗證不追","ruling":"前次首倉條件的兩項都已發生：股價 97.05 美元低於 125 美元，Q3 營收 1.613 億美元高於 1.58 億美元，所以本次重做判斷。Q3 已兌現，下一個未驗證的是 8 億美元展望與毛利率，首倉與加碼門檻改掛這兩項。","evidence_level":"公司新聞稿（一手）","settle_metric":"FY2027 營收展望、2026 Q4 非 GAAP 毛利率","if_then":["若 2026 Q4 毛利率 ≥ 51% 且展望 ≥ 8 億美元，加碼至計畫倉位 2/3","若股價先漲過 125 美元而財報還沒出，不追"]},{"axis":"毛利率說法改口","cause":"新證據","prior_field":null,"side_a":"2026-08-10 CFO：年底毛利率 52.5%～53%、營益率 30%～32%。","side_b":"2026-11-04 CFO：Q3 毛利率 51.1%，低於預期，改說 2027 Q1 起逐步改善，沒有給 Q4 數字。","ruling":"可調和，屬時間延後。零組件與匯率的一次性歸因不採信也不否定，標為未證；若 2027 年 8 月財報毛利率仍低於 52%，這個歸因就不成立。匯率不做預測，只看毛利率有沒有吸收掉。","evidence_level":"公司法說（一手）","settle_metric":"2027 Q1、Q2 非 GAAP 毛利率","if_then":["若 2027 Q1 毛利率 ≥ 52%，加碼至滿倉","若 2027 Q1 與 Q2 都低於 51%，減碼一半，定價力評分下調 1 分"]},{"axis":"供應鏈說法前後不一","cause":"新證據","prior_field":null,"side_a":"2026-08-10 COO：討論產能時看不到問題或障礙；2026-10-14 CEO：營運基礎能供應更多。","side_b":"2026-11-04 COO：部分供應商產能不足，要 3～6 個月解決，但自己說只是感覺、不確定。","ruling":"可調和：自家產能沒問題，卡在外部零組件。但三個月內說法轉向，管理層的時程只當參考，以 2027 年 5 月財報是否仍提短缺為準。","evidence_level":"公司法說（一手）","settle_metric":"2027 年 5 月財報的短缺說法與交期","if_then":["若 2027 年 5 月仍提短缺或錯過交期，停止加碼","若短缺解除且毛利率回升，維持原加碼節奏"],"evidence_refs":["geo_supply_chain#1"]},{"axis":"OSAT 主導地位與對手得標","cause":"新證據","prior_field":null,"side_a":"2026-11-04 COO：在 OSAT 居主導地位，大型對手很難進入。","side_b":"2026-10-14 COO：對手宣布 OSAT 訂單，公司只稱也拿到大單；台灣 OSAT 份額預期至少 50%；大型對手進 2D 要努力應對，而 2D 占 2026 年出貨約 85%。","ruling":"可調和，屬程度差異。市場變大時客戶開始多家採購，方向維持穩定；份額全是公司自述，所以不給溢價。","evidence_level":"公司法說（一手，自述）","settle_metric":"OSAT 占訂單比重、Yole 年度份額","if_then":["若 OSAT 占訂單低於 45%，減碼一半並重做競爭判斷","若 2028 年份額如 COO 所說變大，定價力評分上調 1 分"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"股價與訂單方向相反","cause":"新證據","prior_field":null,"side_a":"股價 26 週跌 52.78%，週線跌破 52 週與 104 週均線。","side_b":"年初至今訂單逾 8 億美元，檔期排到 2027 下半年，FY1 共識近 3 個月上修 0.55%。","ruling":"性質是市場與公司資料方向相反，但不是論點內部的矛盾。裁定偏向訂單，但證據不足以下重注：Q3 高於指引與 2027 展望是公司明文，下跌原因事實表未涵蓋。決勝數據今天不存在，最早 2027 年 2 月才有，在此之前只放首倉。現在就賣的最強論證：訂單未拆分、毛利率已失約一次、競爭者已進門，股價仍是當年盈餘的 26.74 倍，跌 53% 不等於安全邊際。","evidence_level":"訂單為管理層自述，未拆分；股價為市場事實","settle_metric":"FY2027 展望、預收款與訂單拆分","if_then":["若 FY2027 展望下修到 7.2 億美元以下，清倉","若展望上修到 8.5 億美元以上且股價仍低於 125 美元，加碼至滿倉","若股價先漲過 125 美元而財報未驗證，不追","若股價跌破 78 美元而展望未降，分批反買，不停損"]},{"axis":"估值結論與裁決的變動","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 145.72 美元，估值結論為最貴一級，觀望。","side_b":"本次股價 97.05 美元，跌 33%，FY2027E 本益比 19.07 倍，估值結論降到中性。","ruling":"前次觀望的主因是估值偏高，這個理由已隨股價消失，討論轉為小倉位試單；基本面只小幅變化，不是公司變好。"},{"axis":"價值陷阱風險上升","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱風險為低。","side_b":"本次為中等：EPS 成長高於營收成長 5.4 個百分點，毛利率低於管理層說法。","ruling":"只亮一項信號，列中等；毛利率逐季同比與份額是資料缺口，補上後可能再升。"},{"axis":"看過新證據後維持的欄位","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份評級 B、護城河穩定、後段成長中等、品質複利成長、中循環。","side_b":"本次相同。","ruling":"12 億美元目標與 2027 展望偏正面，毛利率、競爭與混合鍵合延後偏負面，兩邊相抵，不足以改變評級。搶檔期與零組件短缺已是後段特徵，若 2027 訂單放緩就改列晚循環。"},{"axis":"機率與最大回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"Bull 25%、Bear 30%、最大回撤 −55%。","side_b":"Bull 25%、Bear 30%、最大回撤 −55%～−35%。","ruling":"機率不變，因為訂單上修與毛利率失約互相抵銷。回撤改成範圍，並以現價 97.05 美元為起點重算，同樣的 −55% 對應的價位已低很多。"},{"axis":"Single Thing 與清倉指標前份無紀錄","cause":"方法變動","prior_field":["single_thing","kill_metrics"],"side_a":"前份摘要的唯一致命點與清倉指標均為 null。","side_b":"FY2027 營收展望被下修到 7.2 億美元以下（較 8 億美元少 10%）。","ruling":"前份摘要沒有保留這兩欄，無從比較；本次首次留下 Single Thing 與清倉門檻。"}],"triggers":[{"n":1,"text":"股價不高於 100 美元且 2027 營收展望維持 8 億美元以上，建立首倉","type":"估值rearm","maps_to":"H1","metric":"股價、2027 營收展望","threshold":"股價 ≤ $100 且展望 ≥ $800M","action":"首倉 1/3","source_freq":"每日股價，每季財報","date":"2026-11-09 起"},{"n":2,"text":"2026 Q4 非 GAAP 毛利率不低於 51% 且 2027 展望不降，加到計畫倉位 2/3","type":"加碼","maps_to":"H1","metric":"非 GAAP 毛利率、2027 營收展望","threshold":"≥ 51% 且展望 ≥ $800M","action":"加碼至 2/3","source_freq":"每季財報","date":"2027-02"},{"n":3,"text":"2027 Q1 非 GAAP 毛利率達 52% 以上，加到計畫倉位上限","type":"加碼","maps_to":"H2","metric":"非 GAAP 毛利率","threshold":"≥ 52%","action":"加碼至滿倉","source_freq":"每季財報","date":"2027-05"},{"n":4,"text":"股價跌破 250 週均線附近而 2027 展望未降，分批反買，不停損","type":"加碼","maps_to":"H1","metric":"股價、2027 營收展望","threshold":"股價 < $78 且展望 ≥ $800M","action":"分批反買","source_freq":"每週收盤，每季財報","date":"持續"},{"n":5,"text":"股價先漲過 125 美元而財報還沒驗證，不追","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"> $125 且財報未驗證","action":"不追","source_freq":"每日","date":"2027-02 前"},{"n":6,"text":"2027 連兩季毛利率低於 51%，減碼一半","type":"減碼","maps_to":"R1","metric":"非 GAAP 毛利率","threshold":"連 2 季 < 51%","action":"減碼一半","source_freq":"每季財報","date":"2027-08"},{"n":7,"text":"2027 營收展望下修到 7.2 億美元以下，清倉","type":"Single Thing","maps_to":"Single Thing","metric":"FY2027 營收展望","threshold":"< $720M","action":"清倉","source_freq":"每季財報","date":"2027-12 前每季","evidence_refs":["supply_demand_durability#2"]},{"n":8,"text":"OSAT 占訂單低於 45%，或管理層不再重申台灣 OSAT 份額至少 50%，減碼一半","type":"風險","maps_to":"R3","metric":"OSAT 占訂單比重","threshold":"< 45%","action":"減碼一半","source_freq":"法說揭露時","date":"持續","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"n":9,"text":"中國營收年減逾 20%，或美方新規直接涵蓋檢測量測機台，減碼一半","type":"風險","maps_to":"R4","metric":"中國營收、美國出口管制規則","threshold":"年減 > 20% 或新規涵蓋","action":"減碼一半","source_freq":"每季財報，規則公告時","date":"持續","evidence_refs":["customer_concentration_credit#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":10,"text":"2027 年 5 月財報仍提零組件短缺，或任一季錯過交期，停止加碼","type":"風險","maps_to":"R6","metric":"短缺說法、交期","threshold":"2027-05 仍短缺或錯過交期","action":"停止加碼","source_freq":"每季法說","date":"2027-05","evidence_refs":["geo_supply_chain#1"]},{"n":11,"text":"2026 Q4 財報後重做判斷","type":"複審日期","maps_to":"H1","metric":"毛利率、2027 展望、下跌原因資料","threshold":"財報公告後","action":"重做判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"FY2027 營收展望","bear_threshold":"低於 7.2 億美元","window":"2026 Q4 至 2027 Q3 每季財報","source":"公司新聞稿與法說","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"2027 連 2 季低於 51%","window":"2027 Q1 起每季","source":"公司新聞稿","last_status":"warning"},{"metric":"OSAT 占訂單比重","bear_threshold":"低於 45%","window":"管理層每次揭露","source":"法說與投資人日","last_status":"ok"},{"metric":"中國營收","bear_threshold":"年減逾 20%，或美方新規直接涵蓋檢測量測機台","window":"每季；規則公告時即時","source":"公司新聞稿、20-F、美國商務部公告","last_status":"ok"},{"metric":"存貨成長率減營收成長率","bear_threshold":"連 2 季高於 10 個百分點","window":"每季資產負債表","source":"6-K 財報","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤ $100 且 2027 營收展望 ≥ $800M→首倉 1/3；2026 Q4 毛利率 ≥ 51% 且展望不降→加至 2/3；股價 > $125 而財報未驗證不追","exec_line":"分三批：第一批不超過計畫倉位 1/3；第二批等 2026 Q4 財報（預計 2027 年 2 月）；第三批等 2027 Q1 毛利率達 52%。","holding_cap":"Q4 財報驗證前不超過總資產 2%，通過後不超過 4%；要有再跌 35%～55% 的心理準備。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 FY2027 盈餘當週期頂點定價：26 週股價跌 52.78%，FY1 共識近 3 個月卻上修 0.55%，FY2027 本益比只剩 19 倍。但管理層給了 8 億美元以上展望，檔期已排到 2027 下半年，單季毛利率落空不等於週期結束。下跌的確切原因事實表未涵蓋，此判斷待 2026 Q4 財報驗證。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"FY2027 營收達到管理層 8 億美元以上展望，非 GAAP 營益率回到 31% 以上。","2y":"FY2027 營收 ≥ 8 億美元、非 GAAP 營益率 ≥ 31%、非 GAAP EPS ≥ 4.95 美元","5y":null,"10y":null,"threshold":"營收 ≥ 8 億美元且非 GAAP 營益率 ≥ 31%","source":"公司季度新聞稿與法說","drift_rule":"TTM 營收或 EPS 較路徑偏離連 2 季 ≥ 5% 視為削弱，連 3 季 ≥ 10% 視為反轉"},{"id":"H2","text":"先進封裝 2D 檢測與 3D 凸塊量測的份額守住，毛利率走向 54% 以上。","2y":null,"5y":"FY2029 非 GAAP 毛利率 ≥ 54%，OSAT 仍占訂單 45% 以上","10y":null,"threshold":"OSAT 占訂單 ≥ 45%、台灣 OSAT 份額 ≥ 50%、FY2029 非 GAAP 毛利率 ≥ 54%","source":"法說訂單拆分、Yole 年度報告、季度毛利率","drift_rule":"連 4 季偏離 ≥ 5% 視為削弱，連 6 季偏離 ≥ 10% 視為反轉"},{"id":"H3","text":"封裝複雜度讓檢測步驟持續增加，軟體與服務、混合鍵合、光子成為第二條曲線。","2y":null,"5y":null,"10y":"軟體、服務與新製程合計占營收 ≥ 25%","threshold":"FY2029 軟體加服務 ≥ 1.4 億美元；FY2030 混合鍵合加光子占訂單 ≥ 10%","source":"投資人日、法說、年報","drift_rule":"跨 2 個年度低於路徑視為削弱，跨 3 個年度視為反轉"}],"R":[{"id":"R1","text":"毛利率回升落空：零組件與匯率壓力延續，調價轉嫁不足。","h_ref":"H1","clock":"⚡","threshold":"2027 Q1 與 Q2 非 GAAP 毛利率連 2 季低於 51%","evidence_refs":[]},{"id":"R2","text":"2027 檔期訂單遞延或重複下單，AI 資本支出進入消化期；少數 HPC 與 HBM 客戶減少支出時衝擊集中。","h_ref":"H1","clock":"🔥","threshold":"2027 展望低於 7.2 億美元，或存貨成長率高於營收成長率 10 個百分點連 2 季","evidence_refs":["supply_demand_durability#2"]},{"id":"R3","text":"大型同業進入 OSAT 2D 檢測，本土業者攻低階，份額與價格同時受壓。","h_ref":"H2","clock":"🔥","threshold":"OSAT 占訂單低於 45%，或管理層不再重申台灣 OSAT 份額至少 50%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"id":"R4","text":"中國約占營收 45%，出口管制或本土替代造成需求下滑。","h_ref":"H1","clock":"🔥","threshold":"中國營收年減逾 20%，或美方新規直接涵蓋檢測量測機台","evidence_refs":["customer_concentration_credit#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R5","text":"X-ray 等非光學路線在混合鍵合取得主要地位，第二條曲線被截斷。","h_ref":"H3","clock":"🐢","threshold":"主要客戶以非光學方案作為混合鍵合主要檢測，或 FY2030 混合鍵合加光子占訂單低於 10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R6","text":"關鍵零組件短缺超過管理層估的 3～6 個月，影響交期。","h_ref":"H1","clock":"⚡","threshold":"2027 年 5 月財報仍提短缺，或任一季錯過交期","evidence_refs":["geo_supply_chain#1"]}],"single_thing":{"description":"FY2027 營收展望被下修到 7.2 億美元以下（較 8 億美元少 10%）。","why_fatal":"這是盈餘最敏感的一項：營收少 10%，毛利約少 4,100 萬美元，費用不動時 EPS 約少 0.7 美元，約 14%；毛利率少 1 個百分點只影響約 2.8%。下修同時證明檔期訂單不夠硬，12 億美元目標與目前本益比都會被一起重估。","if_happens":"清倉，等訂單拆分與需求重新驗證後再重做判斷。","how_monitor":"每季財報與法說的 2027 展望、預收款與合約負債、存貨與營收成長率差、主要客戶資本支出。","probability":"20%（12～24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":19.07,"peg_fy2":1.17,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.04,"FY2026E":3.63,"FY2027E":5.09,"FY2028E":5.92},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin 共識，依季度非 GAAP 稀釋 EPS（Q2 0.78、Q3 0.99 美元）判斷為非 GAAP；FY2025A 1.04 美元是 GAAP，事實表沒有非 GAAP 值，兩者口徑不同，不可直接計算成長率。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 Q4 財報與 2027 展望更新（日期依去年 2 月 18 日公告推估）","impact":"高","watch":"非 GAAP 毛利率是否 ≥ 51%、8 億美元展望是否維持、訂單有無拆分"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"2027 Q1 財報","impact":"高","watch":"非 GAAP 毛利率是否 ≥ 52%、調價效果"},{"date":"2027-05","date_precision":"month","type":"capacity","event":"零組件短缺解除的最晚時點（COO 估 3～6 個月）","impact":"中","watch":"是否仍提短缺、有無錯過交期"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"AI 軟體產品開始貢獻營收","impact":"中","watch":"2027 全年是否達雙位數百萬美元、認列為訂閱或一次性授權"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 FY2027 盈餘當週期頂點定價：26 週股價跌 52.78%，FY1 共識近 3 個月卻上修 0.55%，FY2027 本益比只剩 19 倍。但管理層給了 8 億美元以上展望，檔期已排到 2027 下半年，單季毛利率落空不等於週期結束。下跌的確切原因事實表未涵蓋，此判斷待 2026 Q4 財報驗證。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-52.78, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
