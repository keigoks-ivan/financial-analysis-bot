你是 DD 管線 v20 的判斷層閘（gate），標的 LIN（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝9404 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）
- `f_kpi1_non_gaap_adjusted`（q1_business）｜Non-GAAP（adjusted）營業利益＝2763 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）
- `f_kpi2_non_gaap`（q1_business）｜Non-GAAP 營業利益率＝29.4 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益＝2150 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）
- `f_kpi4_gaap`（q1_business）｜GAAP 營業利益率＝22.9 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）
- `f_kpi7_2026_adjusted_diluted_ep`（q1_business）｜指引：2026 全年 adjusted diluted EPS＝17.82–17.92 USD｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）
- `f_kpi8_project_backlog`（q1_business）｜專案積壓訂單（project backlog）＝11000 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）
- `f_peer_lin_gross_margin_pct`（q2_moat）｜LIN 毛利率＝47.86 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LIN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_lin_operating_margin_pct`（q2_moat）｜LIN 營業利益率＝27.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LIN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lin_fcf_margin_pct`（q2_moat）｜LIN FCF 利潤率＝14.02 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LIN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_apd_gross_margin_pct`（q2_moat）｜APD 毛利率＝32.06 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APD.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_apd_operating_margin_pct`（q2_moat）｜APD 營業利益率＝24.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_apd_fcf_margin_pct`（q2_moat）｜APD FCF 利潤率＝-2.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APD.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝17.89 USD/share｜期間與口徑：2026-11-02／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-02）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝18.2 USD/share｜期間與口徑：2026-11-02／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-02）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝36417.02 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝38173.24 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（25 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_fcf`（q4_capital）｜自由現金流（FCF）＝1777 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Linde Q3 2026 IR 新聞稿 https://www.linde.com/news-and-media/2026/linde-reports-third-quarter-2026-results；表格 https://assets.linde.com/-/media/global/corporate/corporate/documents/press-releases/2026/linde-3q26-earnings-release-tables.pdf（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得（新聞稿無共識；僅 consensus_revision 有 FY EPS 共識 fy1 17.89）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝22755.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 26702.0、現金 3947.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝459.08 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.225 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝514.24 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝34.15 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝67.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝67.5 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.51 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝7.14 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝7.11 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rsi14`（q5_valuation）｜RSI(14)＝69.4｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝1.9 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：葡萄牙競爭機構對 Linde 收購 Acaíl Gas 啟動第二階段深入審查（2026，併購審查非濫用調查）
  - 來源：Global Competition Review Linde 組織頁（as_of 2026-06-01）｜affects：decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Linde 10-K FY2025 風險因素列出貿易衝突、關稅與進出口管制為國際營運風險，可能降低需求、售價或營收；法規面亦含貿易進出口限制與經濟制裁。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-25）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：俄羅斯 Amur 區仲裁法院 2026 年 1 月判 Linde 實體須賠 Amur GPP 800 億盧布，Linde 俄羅斯子公司 2 月提出上訴（俄語媒體報導）
  - 來源：finance.mail.ru：«Дочка» Linde подала апелляцию на взыскание по иску Амурского ГПЗ（as_of 2026-02-15）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：卡達 Ras Laffan 約占全球氦氣 30–38%，2026 年 3 月衝突使約三分之一全球氦氣供應中斷
  - 來源：Exiger：Iran War Disrupts One-Third of Global Helium Supply（as_of 2026-03-15）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#4`（geo_supply_chain｜方向 -｜狀態 ok）：Linde 俄羅斯或有負債約 18 億美元（RCA 11 億、Amur GPP 7 億）
  - 來源：Panabee Linde Q2 2026 report（as_of 2026-07-31）｜affects：decision_inputs.bear、valuation
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：歐洲需求弱：管理層預期歐洲需求與量能持續疲弱；醫療、電子為亮點，化工為最受挑戰的終端市場之一（此為 2025 Q3 call 的說法）。
  - 來源：Linde Q3 2025 earnings call transcript (Motley Fool)（as_of 2025-10-31）｜affects：thesis.R、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Chartmill 顯示 2026-10-17 時 29 位分析師的 FY2026 EPS 共識為 18.05 USD、Q3 EPS $4.56;此共識高於公司當時指引區間上限 $17.90(10/29 新區間 $17.82–17.92 仍低於 18.05;摘要口徑待核)。
  - 來源：Chartmill LIN estimates（as_of 2026-10-17）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：Linde AG 前少數股東在慕尼黑法院的擠出補償價格訴訟：2023-11 法院駁回全部請求，原告已上訴；另與 RCA 的俄羅斯專案糾紛仍在 HKIAC 仲裁中，St. Petersburg 禁令未解除。
  - 來源：SEC EDGAR 10-K FY2025 Item 8 附註（as_of 2026-02-25）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：未見美國證券集體訴訟；既有訴訟為慕尼黑擠出補償價格程序（原告上訴中）與 RCA 俄羅斯專案糾紛（HKIAC 仲裁進行中）。
  - 來源：SEC EDGAR 10-K FY2025 Item 8 附註（as_of 2026-02-25）｜affects：decision_inputs.bear、thesis.R
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：第三方聚合站顯示 Linde Gas & Equipment Inc.（Livingston, TN）2025-07-25 收到 FDA Form 483（NOxBOXi 醫療器材，CAPA 缺失等）；Form 483 非警告信，未見警告信或召回。發布日在12個月窗之外，原文未核。
  - 來源：globalkeysolutions.net FDA 483 紀錄 - Linde Gas & Equipment Inc - July 25, 2025（as_of 2025-07-25）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":820.7,"bear_5y_price":362.0,"p_bull_pct":25,"p_bear_pct":25,"upside_5y_pct":26.4,"ev5y_pct":20.7,"irr_base_pct":4.8,"asym_ratio":2.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":17.89,"pe":28.74,"basis":"FY2026 共識調整後 EPS 17.89 美元（已有三季實績，落在公司指引 17.82–17.92 內）；終端倍數同用當年度調整後 EPS 口徑"},"eps":{"bull":[19.5,21.4,23.5,25.8,28.3],"base":[19.0,20.6,22.3,24.1,26.0],"bear":[17.5,17.2,17.5,17.8,18.1]},"pe":{"bull":29,"base":25,"bear":20},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":1.225,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LIN_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CFO｜guidance：全年 EPS 指引區間更新為 17.70–17.90 美元（原話："The updated full year range is $17.70 to $17.90"）
- 2026-07-31｜CFO｜guidance：第三季 EPS 指引區間 4.45–4.55 美元（原話："Third quarter guidance range is $4.45 to $4.55"）
- 2026-07-31｜CFO｜guidance：指引區間中點假設經濟無改善（原話："the range assumes no economic improvement at the midpoint"）
- 2026-07-31｜CFO｜guidance：基礎量能回升尚未納入下半年指引，需再觀察數季（原話："we'd like a few more quarters under our belt"）
- 2026-07-31｜CFO｜guidance：Q2 到 Q3 排除匯率後 EPS 中點增加 0.05 美元（原話："increase $0.05 at the midpoint when excluding FX"）
- 2026-07-31｜CEO｜guidance：2027 年 EPS 成長以 8%–12% 演算法為基準，不需總經改善；正式指引年底至明年初再給（原話："We're not looking for macro."）
- 2026-07-31｜CEO｜guidance：管理層指 EPS 演算法為 8% 至 12%（原話："we should be delivering 8% to 12%"）
- 2026-07-31｜CFO｜guidance：氦氣假設未變動：指引維持不變（原話："we left the guidance intact"）
- 2026-07-31｜CEO｜guidance：管理層對總經採中立立場，交由投資人自行判斷（原話："we have taken a neutral stand"）
- 2026-07-31｜CFO｜margin：Q2 營業利益率 29.5%，年減 60bp（排除成本轉嫁為 30bp）（原話："Operating margins of 29.5% decreased 60 basis points"）
- 2026-07-31｜CEO｜margin：CEO 表達對本季利益率不滿意（原話："we are not satisfied with our margin performance"）
- 2026-07-31｜CFO｜margin：CFO 說明美國居家醫療（Lincare）拖累美洲利益率，排除後利益率將上升（原話："Excluding this, margins would have increased."）
- 2026-07-31｜CFO｜margin：APAC 利益率下滑歸因於電子客戶的低毛利設備銷售（原話："APAC erosion is mostly due to lower margin equipment sales"）
- 2026-07-31｜CFO｜margin：管理層預期多項利益率逆風為暫時性（原話："we expect many of these margin headwinds to be temporary"）
- 2026-07-31｜CFO｜margin：氦氣定價改善但因調度成本，利潤率層面暫時稀釋；美元貢獻為正（原話："that grossing up effect right now is a little bit dilutive"）
- 2026-07-31｜CFO｜margin：CFO 估 Lincare 拖累約比分析師估算（Q2 約 3,000 萬）高 30%（原話："probably say 30% higher than that number, give or take"）
- 2026-07-31｜CEO｜margin：Lincare 面臨勞動成本通膨與給付環境變化的持續逆風（原話："persistent headwinds, right, from labor cost inflation"）
- 2026-07-31｜CFO｜margin：Q2 價格 +2%，與當地通膨大致同步；Lincare 定價不足（原話："The price increase of 2% was broad-based"）
- 2026-07-31｜CFO｜margin：回測：2025 年上半年利益率強、下半年弱，全年年比較基期有利（原話："I'm fully expecting us to see better year-over-year"）
- 2026-07-31｜CEO｜margin：回溯項目的利益率隨產能利用率爬升而改善（原話："I always expect backlog projects to continue to improve"）
- 2026-07-31｜CEO｜commitment：CEO 承諾第三季利益率環比改善（原話："I fully expect sequential improvement into the third quarter"）
- 2026-07-31｜CFO｜commitment：CFO 表示本季將採取成本行動，並於十月電話會議提供更多細節（原話："we will likely look to take some cost actions this quarter"）
- 2026-07-31｜CFO｜commitment：CFO 預告下次（十月）電話會議將說明已採取的行動（原話："what we've done in the October call"）
- 2026-07-31｜CEO｜commitment：CEO 預期年底 sale-of-gas 在手訂單仍維持 8 開頭（億美元級 80 億以上）（原話："backlog to finish the year with an 8 handle"）
- 2026-07-31｜CEO｜commitment：管理層預期氦氣回收在未來數季反映於利益率（原話："I fully expect that it will over the next couple of quarters"）
- 2026-07-31｜CEO｜commitment：太空市場於 2030 年前達 10 億美元的目標維持不變（原話："we are on track for that $1 billion opportunity"）
- 2026-07-31｜CFO｜commitment：管理層表示組織承諾達成股東期待（原話："We know our owners expect more"）
- 2026-07-31｜CFO｜capital_allocation：年初至今已部署 60 億美元資本（原話："Year-to-date, we've deployed $6 billion of capital"）
- 2026-07-31｜CFO｜capital_allocation：預期已確保成長性資本支出將持續為重大資金用途（原話："we expect this number to remain a significant use of capital"）
- 2026-07-31｜CFO｜capital_allocation：營運現金流因工程業務時點偏弱，預期下半年回升（原話："we expect the second half to step up like prior years"）
- 2026-07-31｜CFO｜capital_allocation：CapEx 預期上調，來自新增專案與商業太空基礎 CapEx（原話："The CapEx number on the estimate was bumped up."）
- 2026-07-31｜CEO｜capital_allocation：投資標準為稅後兩位數無槓桿 IRR（原話："post-tax double-digit IRR -- unlevered IRR perspective"）
- 2026-07-31｜CFO｜capital_allocation：專案決策依 IRR，不依營收或利益率（原話："we make our decisions on IRR"）
- 2026-07-31｜CEO｜capital_allocation：CEO 表示正評估美國居家醫療業務的策略定位（部分或整體）（原話："evaluate the strategic fit of this U.S. homecare business"）
- 2026-07-31｜CEO｜capital_allocation：已有 Lincare 策略選項評估並行於改善行動（原話："evaluating what the strategic options for this business are"）
- 2026-07-31｜CEO｜customer：電子業 Q2 年增 18%，預期動能延續下半年（原話："had 18% growth in second quarter"）
- 2026-07-31｜CEO｜customer：Q2 新增 10 億美元電子業新單，支援美國西部先進製程晶圓廠（原話："we added $1 billion of new electronics wins to the backlog"）
- 2026-07-31｜CEO｜customer：台灣合資公司另有約 8 億美元電子業投資，未計入 backlog（原話："invest approximately $800 million to build, own and operate"）
- 2026-07-31｜CEO｜customer：航太占製造業成長逾 1/3（原話："aerospace accounted for more than 1/3"）
- 2026-07-31｜CEO｜customer：氦氣方面簽下新長約客戶（原話："signed up new customers with long-term contracts"）
- 2026-07-31｜CFO｜customer：電子業營收／CapEx 比與前幾期相似，區間 20%–50%（原話："revenue has ranged anywhere from 20% to 50%"）
- 2026-07-31｜CFO｜competition：部分商業太空客戶有垂直整合（自購工廠）意願，僅限大氣氣體，氫氣側未見（原話："a desire to vertically integrate"）
- 2026-07-31｜CFO｜competition：預期商業太空客戶將混合 sale of gas 與 sale of plant（原話："you'll see a blend of sale of gas and some sale of plant"）
- 2026-07-31｜CEO｜product：氦氣在卡達重啟與供應鏈到位後，預期正常化進度較慢，今年不會正常化（原話："I don't think you will see normalization this year."）
- 2026-07-31｜CEO｜product：亞洲台灣與韓國皆有強勁電子業專案管線（原話："see strong pipelines in Taiwan and Korea as well"）
- 2026-07-31｜CEO｜risk：中東危機使依賴當地碳氫化合物的亞洲國家縮減工業活動（原話："have had to scale back industrial activity"）
- 2026-07-31｜CEO｜risk：地緣政治事件可能影響化學與能源市場（原話："geopolitical events that could impact one way or the other"）

### 問答異常語氣（迴避／改口／保留）
- LIN_Q2_2026_Earnings_Call_20260731.md｜問：Laurent Favre 問美國居家醫療業務目前是否獲利、拖累有多大｜答法：未直接回答是否獲利；改談排除 Lincare 後美洲利益率 +20bp、氣體業務表現良好與硬貨組合
- LIN_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Zekauskas 問是否已決定出售 Lincare、決策時程為何｜答法：未回答是否出售或時程；僅說同步評估策略選項並「with diligence」
- LIN_Q2_2026_Earnings_Call_20260731.md｜問：David Begleiter 追問 2027 年氦氣是否為順風｜答法：未確認順風；僅答氦氣將正常化，並稱需 wait and see，量價組合複雜
- LIN_Q2_2026_Earnings_Call_20260731.md｜問：Duffy Fischer 問荷莫茲海峽解決後一年後的影響｜答法：拒絕推測明年狀況，稱先看海峽問題如何解決

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 1 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 5 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 1 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 2 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"LIN","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Linde plc"},"oneliner":"Linde 靠現場供氣長約、管線密度與隨通膨調價穩定複利，2026 年調整後 EPS 約年增 8%–9%；但現價約 28.7 倍當年 EPS，一年基本情境上檔不到 2%，2027 年 2 月指引能否回到 8% 以上是關鍵，現價不追。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺製造、化工能源、電子與醫療客戶的工業氣體錢：在客戶廠旁或管線網絡上供氣，用長約鎖量、合約條款轉嫁能源成本、隨通膨調價；錢卡在本地供應密度加合約轉嫁條款這一節點。","reasoning":"Q3 2026 營收 94.04 億美元（年增 9%，扣掉匯率、成本轉嫁、併購、工程各約 1% 後基礎 +5%＝價 +3%、量 +2%），調整後營業利益 27.63 億美元、利益率 29.4%（年減 30bp，排除成本轉嫁持平）；GAAP 營業利益 21.5 億美元、22.9%，差額主要是 4.25 億美元重組費用。TTM 毛利率 47.86%。三種配送：現場供氣（能源成本當月轉嫁）、merchant 液態（三至七年需求合約）、瓶裝；另有工程（賣廠）與 Lincare 居家照護（年化營收約 23 億美元，本季移到其他部門並評估策略選項）。Q3 終端市場：化工能源（約 22%）+12%、製造（約 21%）+7%、醫療（約 15%）+2%、金屬礦業（約 12%）+3%、電子（約 10%）+15%、食品飲料（約 9%）+3%。單點依賴：10-K 稱不依賴單一或少數客戶，2025 年約 64% 營收在美國以外；唯一明顯集中點在供給端，氦氣貨源集中卡達。產業時鐘判 I：歐洲量由 12–18 個月前的 −2%～−3% 回到持平、美國化工與金屬走強，但公司指引不假設總經改善。供需持久性：結構性持久，現場長約與管線讓供給難被新進者複製，量則隨工業產出循環。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap_adjusted","f_kpi2_non_gaap","f_kpi3_gaap","f_kpi4_gaap","f_kpi7_2026_adjusted_diluted_ep","f_kpi8_project_backlog","f_peer_lin_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"高：現場供氣長約當月轉嫁能源成本，merchant 液態簽三至七年需求合約；Q3 2026 基礎銷售 +5%（價 +3%、量 +2%，量約一半來自專案積壓）","unit_econ_note":"氣體運輸成本高，利潤取決於工廠與管線周邊的客戶密度；merchant 與瓶裝氣的成本回收落後 3–6 個月，成本急升的季度利潤率先受壓","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"全球寡占、長約加管線、價格隨通膨、調整後 EPS 約 8%–10% 複利、資本密集"},"industry":{"clock_phase":"I","sd_verdict_source":"結構性持久：10-K 對現場供氣、管線網絡與 merchant 三至七年合約的描述；量的週期性由 2026-10-29 電話會議終端市場拆解佐證","bargaining":{"up":"電力與天然氣供應商：現場供氣當月轉嫁，merchant 與瓶裝落後 3–6 個月回收；氦氣貨源集中卡達，議價在供應端","down":"客戶分散、無單一依賴；換供應商要重蓋現場工廠，客戶議價力弱","geo":"約 64% 營收在美國以外；歐洲能源成本結構性偏高、中國內需弱"},"profit_pool_dir":"利潤池集中在少數全球業者；增量在美國灣區化工、電子與太空，歐洲在流失；利潤池占比數字事實表未涵蓋","tam_table":{"expanded":false,"reason":"成熟寡占，不是低滲透、份額擴張或新品類故事，成長來自工業產出、通膨調價與專案積壓；事實表也沒有 TAM 與利潤池占比數字"}}}},"q2_moat":{"verdict":"護城河穩定：現場長約與管線網絡讓 Linde 每季漲價約 3% 仍不掉量，但 2026 年利潤率擴張暫停，Lincare 與工程拖累執行面。","reasoning":"機制：工業氣體運輸成本高，供應半徑以工廠與管線為中心，現場供氣蓋在客戶廠旁、簽長約並當月轉嫁能源成本，merchant 簽三至七年需求合約；10-K 明列管線網絡所在地是競爭優勢。可證方向：對 Air Products 的 TTM 營業利益率高約 2.2pp、毛利率高約 15.8pp、FCF 利潤率一正一負（期間不一致，LIN 至 2026-09、APD 至 2026-06）；ROIC 差距與趨勢事實表未涵蓋，所以給 B 不給 A，升 A 需要對最強同業 ROIC 差距為正且擴大的證據。定價力 9：Q3 價格 +3% 跨各區，量仍 +2%，美洲排除一次性回收後跑速約 4%；氦氣漲價只回收調度成本、刻意不過度漲價。執行力 8：營業利益率 2022→2025 由 19.4% 升到 27.2%，但 2026 年 Q2、Q3 調整後營益率年減 60bp、30bp，CEO 自承 Q2 未達股東期待，Q2 承諾的第三季環比改善也小幅落空（29.5%→29.4%），拖累來自 Lincare 與工程。趨勢判穩定：利潤率擴張暫停但定價力未退。當期 ROIC 因缺投入資本無法計算，以 TTM 營業利益率 27.08% 與資本支出約占營收 15%–16% 看屬高利益率、低周轉，關鍵在再投資報酬。產業態勢：雙向拉鋸——競爭軸靜態（10-K 未點名新進入者，對手仍是 Air Liquide、Air Products、Messer、大陽日酸），結構軸美國灣區化工與電子轉好、歐洲去工業化變差，其他結構變數是俄羅斯訴訟與關稅風險。","fact_refs":["f_peer_lin_gross_margin_pct","f_peer_lin_operating_margin_pct","f_peer_lin_fcf_margin_pct","f_peer_apd_gross_margin_pct","f_peer_apd_operating_margin_pct","f_peer_apd_fcf_margin_pct","f_kpi2_non_gaap"],"verdict_values":{"moat":{"mechanism":"本地供應密度：現場供氣蓋在客戶廠旁並簽長約、管線網絡連接多家大客戶、merchant 三至七年需求合約，換供應商要重蓋工廠","execution":8,"pricing":9,"grade":"B","trend":"→","trend_evidence":"價格 +3% 跨各區且量 +2%（Q3 2026）；營業利益率 2022→2025 由 19.4% 升到 27.2%，2026 年 Q2、Q3 調整後營益率年減 60bp、30bp，排除成本轉嫁為 −30bp、持平：擴張暫停而非逆轉，定價力未見縮減","competitor_notes":[{"name":"Air Products","strategy_note":"TTM 營業利益率 24.85%、FCF 利潤率 −2.39%，正處大型專案資本支出高峰，現金轉換明顯落後 Linde；是唯一能直接比利潤率的同業"},{"name":"Air Liquide","strategy_note":"10-K 點名的全球主要對手；事實表只有 1 季且缺營收，無法比較利潤率"},{"name":"Taiyo Nippon Sanso","strategy_note":"10-K 點名對手；事實表只有 2 季且缺營收，無法比較"},{"name":"Messer","strategy_note":"10-K 點名對手；事實表無財務數字"}],"peer_na_reason":"Air Liquide 只有 1 季、大陽日酸只有 2 季且缺營收，無法算利潤率；Messer 事實表無數字，只能與 Air Products 比","threats":[{"level":"🟡","text":"氦氣：卡達 Ras Laffan 約占全球三到四成，荷莫茲海峽受阻使約三分之一供應中斷；Linde 靠全球貨源調度並漲價，但成本同步上升、利潤率未明顯受惠；海峽恢復後氦氣轉為過剩、價格回落","p":"約 40%（12–24 個月內恢復並回落）","evidence_refs":["geo_supply_chain#1"]},{"level":"🟡","text":"關稅與進出口管制：10-K 風險因子列出可能壓低需求或售價；工業氣體多為當地生產當地賣，直接關稅曝險小，風險在客戶端製造業需求","p":"約 20%","evidence_refs":["reg_tariff_export#0"]},{"level":"🟡","text":"商業太空客戶想自建大氣氣體工廠（2026-07-31 CFO），只限大氣氣體、氫氣端未見；Linde 以賣廠加賣氣混合因應","p":"約 30%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"工業氣體是客戶製程的必需投入（煉油脫硫用氫、晶圓廠大氣氣體、醫療氧），使用者、決策者、付款者多為同一家工廠，屬需要而非想要；10-K 稱不依賴單一或少數客戶，終端市場分散。急迫性高但量隨工業產出循環，代理讀數＝Q3 2026 量 +2%，歐洲持平、中國內需弱"},{"item":"決策層級","level":"🟢","text":"替代性要在單一工廠層看：現場供氣是在客戶廠旁蓋廠的長約，換供應商等於重蓋一座廠；10-K 明列管線網絡所在地為競爭優勢，merchant 合約三至七年。代理讀數＝價格 +3% 下量仍 +2%，未見因漲價流失"},{"item":"價值鏈分配","level":"🟡","text":"最大投入是電力與天然氣：現場供氣當月轉嫁，merchant 與瓶裝落後 3–6 個月才回收，2026 年北美電力與配送成本上升時利潤率受壓；上游氦氣貨源集中卡達，議價在供應端；下游歐洲化工停產、Lincare 受醫療給付方壓價。Linde 掌握本地供應密度，但能源成本那一段要靠合約條款搶回"},{"item":"社會容忍度","level":"🟡","text":"醫療用氧與居家照護屬高必要、高敏感，給付價格受政府與保險壓制，Lincare 正是拖累來源；氦氣短缺時管理層表示刻意不過度漲價、只回收調度成本，屬保留社會容忍度的保費。10-K 揭露例行反壟斷索賠，未見針對性大案"}],"roiic":"事實表未涵蓋（缺投入資本與折舊攤銷）；管理層新專案門檻為稅後兩位數無槓桿 IRR（2026-07-31 CEO），未經驗證","reinvest_rate":"事實表未涵蓋精確值；代理：2026 年前三季部署逾 90 億美元，約一半投入事業（2026-10-29 CFO），全年資本支出約 55–60 億美元","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，再投資率＝（資本支出－折舊攤銷＋營運資金變動＋收購淨額）÷ NOPAT；缺折舊攤銷與投入資本，本輪不出數字"}}}},"q3_growth":{"verdict":"成長跑道中等：成熟寡占，EPS 複利靠價格 3%–4%、量 1%–2%（一半來自專案積壓）與每年約 2% 的減股；電子與太空是增量但規模小。","reasoning":"成長拆解：Q3 2026 基礎銷售 +5%＝價 +3%＋量 +2%，量的一半來自專案積壓，有機量多是亞太與歐洲的設備銷售。共識 EPS：2026 年 17.89 美元、2027 年 18.20 美元（只年增 1.7%，與 2026-07-31 CEO 所說不靠總經的 8%–12% 演算法落差大）；2028 年共識事實表未涵蓋，三年年複合算不出來。內生天花板因缺投入資本與折舊算不出數字；共識成長低於基礎銷售成長，不存在需要歸因的正缺口。基本情境三年 EPS 年複合 7.6% 可拆成價、量與減股，不依賴利潤率擴張或估值重評。跑道：工業氣體不是滲透率故事，電子（占 10%、Q3 +15%，約 20 億美元專案分 2–3 年投產）與太空（2030 年目標 10 億美元）占比小，歐洲（CEO 稱零催化劑）與中國內需拖累；五年後仍是約工業產出加通膨的成長，判中等。衰退信號亮一個：EPS 成長長期高於營收成長；FCF／淨利 2025 年 0.74，再一年就亮第二個。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_project_backlog","f_kpi7_2026_adjusted_diluted_ep"],"verdict_values":{"growth":{"driver_mix":"價格 3%–4%＋量 1%–2%＋淨減股約 2%，利潤率大致持平","runway_years":"不適用：成熟寡占，非滲透率故事","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板＝增量 ROIC × 再投資率；事實表沒有投入資本與折舊攤銷，算不出數字。可用代理：新專案門檻為稅後兩位數無槓桿 IRR（2026-07-31 CEO，未驗證），前三季部署資本約一半投入事業，Q3 量 +2% 中約一半來自專案積壓。基本情境 EPS 年複合拆為價 3%–4%、量 1%–2%、淨減股約 1.5%–2%，不靠利潤率擴張","segments":[{"item":"化工與能源（約占 22%）","value":"Q3 2026 年增 12%：美國灣區與中國量增，加上美洲回收先前成本通膨"},{"item":"製造（約占 21%）","value":"年增 7%：廣泛漲價，美、中、印量增，航太延續"},{"item":"醫療（約占 15%）","value":"年增 2%；排除 Lincare 為中個位數"},{"item":"金屬與礦業（約占 12%）","value":"年增 3%：美洲走強，歐洲與亞太小幅收縮"},{"item":"電子（約占 10%）","value":"年增 15%：亞太與美國有機成長，另有約 20 億美元專案建造中"},{"item":"食品飲料（約占 9%）","value":"年增 3%"},{"item":"占比來源","value":"占比引自投資人簡報的搜尋摘要、未讀原頁；成長率與 2026-10-29 電話會議一致"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差逾 5pp）","lit":true,"evidence":"GAAP 稀釋 EPS 2022→2025 由 8.23 升到 14.61 美元（年複合約 21%），營收由 333.6 億到 339.9 億美元（約 0.6%）；2022 基期偏低，但成長主要來自利潤率與減股而非量"},{"signal":"FCF／淨利低於 0.75 連兩年","lit":false,"evidence":"2024 年 0.750 剛好在線上、2025 年 0.738，再一年就亮"},{"signal":"毛利率連兩季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；調整後營業利益率 Q2、Q3 年減 60bp、30bp，排除成本轉嫁為 −30bp、持平"},{"signal":"核心市占縮減","lit":null,"evidence":"事實表未涵蓋市占"},{"signal":"提價後銷量下滑","lit":false,"evidence":"Q3 2026 價 +3% 量 +2%"},{"signal":"SBC／營收逾 5% 且上升","lit":null,"evidence":"事實表未涵蓋；稀釋股數年減約 2%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"10-K 未提替代技術；歐洲區域萎縮另列風險"},{"signal":"產業估值倍數近三年系統性下移","lit":null,"evidence":"事實表未涵蓋同業倍數"},{"signal":"維修資本支出占 FCF 逾 60%","lit":null,"evidence":"事實表未涵蓋拆分"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"專案積壓約 110 億美元，2026 年共識營收年增約 7%"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀律好但回購買在高倍數：前三季部署逾 90 億美元，約一半投資、一半回饋股東，稀釋股數年減約 2%。","reasoning":"現金：Q3 2026 FCF 17.77 億美元；年度 FCF／淨利 2023 年 0.89、2024 年 0.75、2025 年 0.74，FCF 利潤率由 2022 年 17.1% 降到 TTM 14.0%，主因專案資本支出增加（全年約 55–60 億美元）。去向：前三季部署逾 90 億美元，約一半投入事業、一半以股息與回購回饋股東，精確四分事實表未涵蓋。SBC／營收事實表未涵蓋，但稀釋股數年減約 2%。營運槓桿：Q3 營收 +9%、調整後營業利益 +8%，差 1pp，未到壓縮。資產負債：淨負債約 227.6 億美元，第三方筆記列 S&P 歐元債評等 A。俄羅斯案件二手來源估或有負債約 18 億美元，約每股 3.9 美元。","fact_refs":["f_kpi5_fcf","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_peer_lin_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月無重大併購完成申報，併購只貢獻約 1% 營收成長（2026-10-29 CFO）；已實現併購 ROIIC 事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"以前瞻本益比約 28.7 倍推算回購收益率約 3.5%（trailing 34.15 倍則約 2.9%）；要過關需 10 年期殖利率不高於 1.5%，10 年期殖利率事實表未涵蓋，CFO 於 2026-10-29 稱處於利率上升環境，判不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 金額事實表未涵蓋；以淨利 ÷ 稀釋 EPS 回推稀釋股數 2022 年約 5.04 億股、2025 年約 4.72 億股，年減約 2.1%，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：併購只貢獻約 1% 營收成長，現金去向以專案資本支出、股息與回購為主"}}}},"q5_valuation":{"verdict":"偏貴：現價要求 2027 年起回到約 8% 的 EPS 複利，且市場持續給 25 倍以上；EPS 複利我信，倍數守在 28 倍以上我不信。","reasoning":"前瞻本益比 28.7 倍＝514.24 ÷ 17.89（FY2026 共識，已有三季實績且落在公司指引 17.82–17.92 內）；FY2027 本益比 28.3 倍。三年基本情境 EPS 年複合 7.6%，PEG 約 3.8；以 FY2027 本益比計約 3.7。一年基本情境：2027 年 EPS 19.0 美元 × 27.5 倍＝522.5 美元，上檔約 1.6%；三年：2029 年 22.3 美元 × 26 倍＝579.8 美元，上檔約 12.7%。賣方 2026 年 7–8 月目標均價 548–562 美元（高 600、低 460），比現價高 7%–9%，全距 1.3 倍，支持偏貴但非泡沫。同業本益比事實表未涵蓋，終端倍數無法做同業現值對照，這是本輪估值最大的資料缺口。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_rsi14","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比：FY2026 共識調整後 EPS 17.89 美元，現價 514.24 美元，約 28.7 倍","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有 Air Liquide、Air Products、大陽日酸的本益比，無法做倍數對照"},"fwd_pe":28.7,"peg":3.8,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"P/S 6.51 倍、EV/S 7.14 倍都在近 4 個年度端點最高（分位 100），trailing 本益比 34.15 倍在 67.5 分位；這些不是五年分位，真正五年分位事實表未涵蓋。加上 PEG 約 3.8、一年上檔不到 2%，但品質與現金流穩定、賣方目標仍高於現價，判偏貴、不到極貴","upside_short_pct":1.6,"upside_mid_pct":12.7,"denominator_disputed":false,"denominator_note":"分母用 FY2026 共識 17.89 美元，三季已實現、爭議小；FY2027 共識 18.20 美元只年增 1.7%，與管理層 8%–12% 演算法差距大，原因事實表未涵蓋，估值不以它為錨，待 2027 年 2 月指引確認"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方：把價格與減股撐出的 EPS 複利，當成能長期撐住 28 倍的成長；實際量能只有約 2%，一半來自專案。","reasoning":"壓力測試四項過三項：工業衰退量 −3%——長約與當月轉嫁讓 EPS 大致持平，過；氦氣供應恢復、價格回落——管理層說氦氣漲價被成本吃掉、利潤率未受惠，回落時衝擊有限，過；俄羅斯約 18 億美元或有負債全數認列——約每股 3.9 美元、股價的 0.8%，一次性，過；EPS 兩年持平且倍數回到 22 倍——股價約 −23%，不過。最大回撤以倍數壓縮推估 −20%～−35%，歷史回撤事實表未涵蓋。價值陷阱判中度：亮一個衰退信號（EPS 成長長期高於營收成長），FCF／淨利接近第二個。法說未正面回答的有：Lincare 是否獲利與出售時程、2027 年氦氣是否順風、荷莫茲海峽解決後的影響（皆 2026-07-31 場次）；Q3 只補充 Lincare FCF 為正。","fact_refs":["f_net_debt_m","f_shares_diluted_m","f_pe_current","f_consensus_eps_fy2"],"verdict_values":{"trap":{"verdict":"🟡","label":"價格與減股撐起的複利，量能偏弱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":17.89,"pe":28.74,"basis":"FY2026 共識調整後 EPS 17.89 美元（已有三季實績，落在公司指引 17.82–17.92 內）；終端倍數同用當年度調整後 EPS 口徑"},"eps":{"bull":[19.5,21.4,23.5,25.8,28.3],"base":[19.0,20.6,22.3,24.1,26.0],"bear":[17.5,17.2,17.5,17.8,18.1]},"pe":{"bull":29,"base":25,"bear":20},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":1.2,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":7},"max_dd":{"lo":-35,"hi":-20,"basis":"歷史最大回撤事實表未涵蓋，以倍數壓縮推估：起點約 28.7 倍 FY2026 EPS；EPS 兩年持平且倍數回到 22–23 倍約 −20%～−22%；疊加工業衰退與市場殺估值、倍數落到 19 倍約 −34%，取 −20%～−35%；熊市情境終點約 −30%，下緣涵蓋之","trigger_time":null},"basis":{"bull":"2027 年 Lincare 拖累消失加重組節省，EPS 回到管理層 8%–12% 演算法上半段；Woodside 2028 年滿載、電子約 20 億美元專案陸續投產，五年 EPS 年複合約 9.6%，終端 29 倍接近現值","base":"2027 年受匯率與保守總經假設拖累，成長約 6%，2028 年起回到約 8%：價格 3%–4%＋專案量約 1%＋淨減股，利潤率大致持平；終端 25 倍低於現值 28.7 倍，反映成長只有約 8%；同業本益比事實表未涵蓋；EPS 路徑已含回購減股，淨回購殖利率填 0 避免重複計算","bear":"歐洲去工業化、中國內需疲弱、美國灣區化工的原料優勢隨中東衝突結束消退，加上氦氣恢復後價格回落與成本回收遞延，EPS 五年持平在 17–18 美元；終端 20 倍"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"歐洲：CEO 稱零催化劑、扣除設備銷售後量持平；中國：鋼鐵產量 −2.5%、化工持平、國內電動車購買年減約 11%–12%；美國灣區化工的原料優勢來自中東衝突，衝突結束後可能消退","assumption":"基本情境假設 2028 年起回到約 8% EPS 成長，量每年 +1%–2%","consequence":"若三地同時走弱而價格只跟上通膨，EPS 五年持平、倍數由 28.7 倍落到 18–20 倍，股價約 −30%～−40%","ruling":"部分採納：給 25% 熊市機率；但現場長約與當月成本轉嫁讓 EPS 下行有底，五年虧 50% 需要倍數腰斬，判低機率。與唯一致命點部分重疊：2027 年指引低於 8% 是這個故事的第一個訊號，已用同一觸發器監控","watch":"EMEA 排除設備的基礎量、全公司量能、2027 年 2 月指引","evidence_refs":["end_markets#2"],"fact_refs":["f_kpi7_2026_adjusted_diluted_ep"]},{"view":"論點成功但股東經濟變差","evidence":"FCF／淨利由 2023 年 0.89 降到 2024 年 0.75、2025 年 0.74，FCF 利潤率由 2022 年 17.1% 降到 TTM 14.0%；成長靠每年 55–60 億美元資本支出與約 80 億美元專案積壓，回購在 28–34 倍本益比買進；俄羅斯 Amur GPP 一審判賠 800 億盧布、RCA 仲裁與聖彼得堡禁令未解，二手來源估或有負債約 18 億美元；慕尼黑擠出補償訴訟原告上訴中；Lincare 出售可能認列損失","assumption":"EPS 複利能等比例轉成每股自由現金流","consequence":"EPS 照 8% 成長但每股 FCF 只成長 4%–5%，回購收益率約 3.5% 低於資金成本，股東實得報酬落到中低個位數","ruling":"採納為主要風險之一：基本情境終端倍數給 25 倍不給 28 倍；FCF／淨利連兩年低於 0.75 時再下修倍數；俄羅斯案件約每股 3.9 美元，單獨不致命","watch":"年度 FCF／淨利、資本支出占營收、俄羅斯案件判決與扣押進度","evidence_refs":["geo_supply_chain#0","geo_supply_chain#4","major_events#1","lawsuit_class_action#0"],"fact_refs":["f_peer_lin_fcf_margin_pct","f_kpi5_fcf","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"前瞻本益比約 28.7 倍、trailing 34.15 倍；P/S 6.51 倍、EV/S 7.14 倍都是近 4 個年度端點最高；賣方 7–8 月目標均價 548–562 美元只比現價高 7%–9%；FY2027 共識 18.20 美元只比今年高 1.7%","assumption":"市場願意持續給 28 倍以上","consequence":"就算 EPS 照基本情境走，倍數回到 25 倍會吃掉大半 EPS 成長，五年年化報酬只剩中低個位數","ruling":"採納：現價不追，等 460 美元附近或更強的 2027 年指引","watch":"股價對 2027 年 EPS 的倍數、2027 年 2 月指引","evidence_refs":[],"fact_refs":["f_pe_current","f_ps_percentile","f_ev_s_percentile","f_price_at_dd","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 514.24","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=514.24","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"共識與公司指引","cause":null,"prior_field":null,"side_a":"2026-10-17 第三方網站：29 位分析師 FY2026 EPS 共識 18.05 美元，高於當時指引上限 17.90 美元（口徑待核）","side_b":"2026-10-29 財報後：FY2026 共識 17.89 美元，落在新指引 17.82–17.92 美元內；但 FY2027 共識 18.20 美元只年增 1.7%，遠低於 2026-07-31 CEO 所說的 8%–12%","ruling":"可調和：2026 年的落差在財報後已收斂，屬口徑與時點差異；真正未解的是 2027 年共識與管理層演算法的方向落差，本輪基本情境 2027 年取 19.0 美元（年增約 6%），高於共識、低於演算法下緣，待 2 月指引裁決","evidence_level":"二手共識網站＋一手電話會議","settle_metric":"2027 年 2 月公布的 2027 年調整後 EPS 指引中點","if_then":["若指引中點年增 ≥ 8% → 維持基本情境，股價 ≤ 460 美元時分批建立首倉","若指引中點年增 < 8% → 基本情境 2027 年 EPS 下修到 18.6 美元以下，持股減至半倉","若指引中點年增 < 3% → 清倉檢討"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"管理層利潤率承諾與兌現","cause":null,"prior_field":null,"side_a":"2026-07-31 CEO：預期第三季利益率環比改善；CFO：本季將採取成本行動","side_b":"2026-10-29：Q3 調整後營業利益率 29.4%，低於 Q2 的 29.5%，年減 30bp（排除成本轉嫁持平）；成本行動已兌現為 4.25 億美元重組費用","ruling":"可調和：利潤率承諾小幅落空，但成本行動照預告執行、Q3 EPS 4.59 美元高於 7 月指引 4.45–4.55；判執行力扣分而非論點破裂，執行力給 8 不給 9","evidence_level":"一手（兩場電話會議逐字稿）","settle_metric":"Q4 2026 調整後營業利益率與排除成本轉嫁的年變化","if_then":["若 Q4 營益率再低於 29.4% 且排除成本轉嫁年減 → 執行力降為 7，停止加碼","若 2027 年起排除成本轉嫁營益率年增 ≥ 30bp → 執行力回到 9"],"evidence_refs":["end_markets#3"]},{"axis":"基礎成長數字","cause":null,"prior_field":null,"side_a":"8-K 附件摘要：基礎成長 +9%＝價 6%＋量 3%","side_b":"10-Q 與 2026-10-29 CFO：銷售 +9% 扣掉匯率、成本轉嫁、併購、工程各約 1% 後基礎 +5%（價 3%、量 2%）；6% 是美洲區價格","ruling":"可調和：+9% 是總銷售成長，6% 價格是美洲區數字被誤當全公司；採 +5%","evidence_level":"一手（10-Q＋電話會議逐字稿）","settle_metric":"Q4 2026 財報價量拆解表","if_then":["若 Q4 全公司價格貢獻 < +2% → 停止加碼並重檢定價力分數"],"evidence_refs":["end_markets#0"]},{"axis":"歐洲量能","cause":null,"prior_field":null,"side_a":"Q3 2026 歐洲量 +1%，比 12–18 個月前的 −2%～−3% 改善，比較基期變容易","side_b":"CEO：扣掉設備銷售後持平、零催化劑，看不到歐盟採取讓工業回升的決策，中期不抱期望","ruling":"可調和：程度差異；採 CEO 說法，歐洲不進基本情境的量成長，只當作已觸底的穩定","evidence_level":"一手（電話會議逐字稿）","settle_metric":"EMEA 排除設備銷售的基礎量年增","if_then":["若 EMEA 基礎量連兩季 ≤ −2% → 熊市機率由 25% 升到 30%，停止加碼"],"evidence_refs":["end_markets#2"]},{"axis":"現在買或等回檔","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：Q3 營收、營業利益、EPS 都創季度紀錄且優於 7 月指引；2027 年有重組節省、Lincare 拖累（今年約 1.5%–2% EPS 成長）消失、Woodside 下半年起量、電子約 20 億美元專案四項順風，管理層說 8%–12% 不需總經幫忙；A 級信用、淨負債約 228 億美元相對約 2,588 億美元 EV 很輕；品質複利股很少便宜，等回檔可能等不到","side_b":"等的理由：前瞻約 28.7 倍、P/S 與 EV/S 在近 4 個年度端點最高，一年基本情境上檔約 1.6%；Q4 指引只年增 5%–7%，FY2027 共識僅 18.20 美元；RSI 69.4 接近過熱","ruling":"⚖ 選等：依據是估值不是基本面；硬數據點＝28.7 倍對三年 7.6% 的基本 EPS 複利，PEG 約 3.8。約束只有價格，解除條件＝股價 ≤ 460 美元（約 2027 年基本 EPS 的 24 倍、貼近 104 週均線）；2027 年指引中點不低於 8% 是同時要成立的安全條件","evidence_level":"事實表估值數字＋一手電話會議","settle_metric":"股價對 2027 年基本情境 EPS 19.0 美元的倍數，與 2027 年 2 月指引中點","if_then":["若股價續漲到 560 美元以上而 2027 年指引尚未公布 → 不追","若股價跌到 460 美元以下且 Q4 價格貢獻仍 ≥ +2% → 分批反買，首倉 2%","反向條件：若 2027 年指引中點 < 8% → 即使股價到 460 美元也不買，改等 2027 年 EPS 的 22 倍以下"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"價格引擎是否續航","type":"假設驗證","maps_to":"H1","metric":"全公司價格貢獻與排除成本轉嫁的營業利益率年變化","threshold":"價格 < +2% 或排除成本轉嫁營益率年減","action":"停止加碼","source_freq":"每季財報","date":"2027-02","evidence_refs":[]},{"n":2,"text":"2027 年全年 EPS 指引","type":"Single Thing","maps_to":"H2","metric":"2027 年調整後 EPS 指引中點年增（排除匯率）","threshold":"< 8%","action":"減碼至半倉","source_freq":"一次性（Q4 2026 財報電話會議）","date":"2027-02","evidence_refs":[]},{"n":3,"text":"專案積壓轉成量","type":"假設驗證","maps_to":"H3","metric":"sale of gas 專案積壓與電子終端市場年增","threshold":"積壓 < 70 億美元或電子年增 < 10%","action":"停止加碼","source_freq":"每季電話會議","date":"2027-04","evidence_refs":[]},{"n":4,"text":"俄羅斯法律案件","type":"風險","maps_to":"R2","metric":"俄羅斯案件判決確定、資產扣押與損失認列合計","threshold":"≥ 10 億美元","action":"減碼","source_freq":"10-Q／10-K 或有事項附註，每季","date":"2027-02","evidence_refs":["geo_supply_chain#0","geo_supply_chain#4","major_events#1","lawsuit_class_action#0"]},{"n":5,"text":"歐洲去工業化","type":"風險","maps_to":"R1","metric":"EMEA 排除設備銷售的基礎量年增","threshold":"連兩季 ≤ −2%","action":"停止加碼","source_freq":"每季電話會議","date":"2027-04","evidence_refs":["end_markets#2"]},{"n":6,"text":"成本回收落差與氦氣反轉","type":"風險","maps_to":"R3","metric":"排除成本轉嫁的調整後營業利益率年變化","threshold":"連兩季年減","action":"減碼","source_freq":"每季財報","date":"2027-04","evidence_refs":["geo_supply_chain#1"]},{"n":7,"text":"進場價位","type":"估值rearm","maps_to":null,"metric":"股價與 2027 年指引","threshold":"股價 ≤ 460 美元且 2027 年指引中點年增 ≥ 8%","action":"分批建立首倉","source_freq":"每日股價＋2027 年 2 月指引","date":null,"evidence_refs":[]},{"n":8,"text":"過高價位","type":"減碼","maps_to":null,"metric":"股價","threshold":"≥ 600 美元（約 2027 年基本 EPS 的 31.6 倍）且 2027 年指引未上修","action":"減碼三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":9,"text":"核心引擎失效","type":"清倉","maps_to":"H1","metric":"排除成本轉嫁營業利益率與 2027 年實際調整後 EPS","threshold":"連四季年減且 2027 年 EPS 年增 < 3%","action":"清倉","source_freq":"每季財報","date":"2028-02","evidence_refs":[]},{"n":10,"text":"全面複審","type":"複審日期","maps_to":null,"metric":"Q4 2026 財報與 2027 年指引","threshold":"公布日","action":"重跑完整研究","source_freq":"一次性","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"排除成本轉嫁的調整後營業利益率年變化","bear_threshold":"連兩季年減","window":"2026 Q4–2027 Q2","source":"Linde 季度財報新聞稿與電話會議","last_status":"warning"},{"metric":"2027 年調整後 EPS 指引中點年增（排除匯率）","bear_threshold":"< 8% 減碼；< 3% 清倉檢討","window":"2027 年 2 月","source":"Q4 2026 財報電話會議","last_status":"unknown"},{"metric":"全公司價格貢獻","bear_threshold":"單季 < +2%","window":"每季","source":"季度財報價量拆解","last_status":"ok"},{"metric":"sale of gas 專案積壓","bear_threshold":"< 70 億美元","window":"2026 年底–2027 年中","source":"季度電話會議","last_status":"ok"},{"metric":"俄羅斯案件損失認列或資產扣押","bear_threshold":"≥ 10 億美元","window":"至 2027 年底","source":"10-Q／10-K 或有事項附註","last_status":"warning"},{"metric":"年度 FCF／淨利","bear_threshold":"連兩年 < 0.75","window":"FY2026–FY2027","source":"年度財報現金流量表","last_status":"warning"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#1","reason":"來源是 GCR 的組織索引頁，沒有摘錄、交易金額或審查時程；內容是一樁地區性小型收購的第二階段併購審查，不是違規或濫用調查，證據本身連不到任何營收或利潤數字，無法設門檻或定價"}],"action_conditions":{"rearm_trigger":"股價 ≤ 460 美元（約 2027 年基本情境 EPS 的 24 倍）且 2027 年 2 月指引中點年增 ≥ 8%","exec_line":"現價不追；已持有者續抱不加碼；股價 ≤ 460 美元且指引達標時分批建立首倉；2027 年指引中點 < 8% 則減至半倉"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 460 美元以下（約 2027 年基本情境 EPS 的 24 倍、貼近 104 週均線 461.9 美元），且 2027 年 2 月指引中點年增不低於 8%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=1.9, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='早循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"價格引擎：全公司價格貢獻維持每季約 +3%、跨各區分布，足以蓋過能源與配送成本通膨","2y":"每季價格貢獻 ≥ +2%，排除成本轉嫁的營業利益率不低於去年同期","5y":null,"10y":null,"threshold":"單季價格貢獻 ≥ +2%（Q3 2026 為 +3%）；排除成本轉嫁營益率年變化 ≥ 0bp（Q3 2026 持平）","source":"每季財報新聞稿價量拆解表與電話會議","drift_rule":"兩年期論點：近四季數值連兩季偏離門檻 ≥5% 視為削弱，連三季偏離 ≥10% 視為反轉"},{"id":"H2","text":"非氣體部門修復：Lincare 重組與裁員（Q3 2026 認列 4.25 億美元，回收期約 1.5–2 年，2027 年下半年全額生效）讓 2027 年調整後 EPS 回到年增 8% 以上","2y":"2027 年調整後 EPS ≥ 19.3 美元（2026 年指引中點 17.87 × 1.08）","5y":null,"10y":null,"threshold":"2027 年指引中點年增 ≥ 8%（排除匯率），全年實際 EPS ≥ 19.3 美元","source":"2027 年 2 月全年指引、每季調整後 EPS 與 Lincare 拖累說明","drift_rule":"兩年期論點：近四季數值連兩季偏離門檻 ≥5% 視為削弱，連三季偏離 ≥10% 視為反轉"},{"id":"H3","text":"專案積壓轉成量：sale of gas 積壓約 80 億美元（Woodside 2027 年下半年起量、2028 年滿載；電子專案約 20 億美元分 2–3 年投產），每年貢獻約 1% 的量成長，電子維持兩位數成長","2y":null,"5y":"電子年增 ≥10% 延續到 2029 年、Woodside 2028 年滿載、sale of gas 積壓維持 ≥ 70 億美元","10y":null,"threshold":"電子終端市場年增 ≥10%；sale of gas 積壓年底 ≥ 70 億美元","source":"季度電話會議積壓數字與終端市場拆解","drift_rule":"五年期論點：連四季偏離門檻 ≥5% 視為削弱，連六季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"歐洲去工業化：CEO 稱歐洲零催化劑，Q3 歐洲量 +1% 主要靠設備銷售、扣除後持平，化工停產持續","h_ref":"H3","clock":"🐢","threshold":"EMEA 排除設備銷售的基礎量連兩季年減 ≥ 2%","evidence_refs":["end_markets#2"]},{"id":"R2","text":"俄羅斯法律風險：Amur GPP 案 2026 年 1 月一審判賠 800 億盧布（子公司上訴中），RCA 案 HKIAC 仲裁進行中且聖彼得堡禁令未解除，二手來源估或有負債約 18 億美元（約每股 3.9 美元）；另慕尼黑擠出補償訴訟原告上訴中，未見美國證券集體訴訟","h_ref":null,"clock":"🔥","threshold":"任一案判決確定、資產遭扣押或認列損失合計 ≥ 10 億美元","evidence_refs":["geo_supply_chain#0","geo_supply_chain#4","major_events#1","lawsuit_class_action#0"]},{"id":"R3","text":"成本回收落差與氦氣反轉：merchant 與瓶裝氣成本回收落後 3–6 個月，Q3 美洲價格 +6% 中約 2pp 屬回收、管理層預期 Q4 回落；氦氣漲價被成本吃掉，荷莫茲海峽恢復後氦氣轉為過剩","h_ref":"H1","clock":"⚡","threshold":"排除成本轉嫁的營業利益率連兩季年減","evidence_refs":["geo_supply_chain#1"]},{"id":"R4","text":"Lincare 修復失敗：居家醫療勞動成本通膨與給付環境不利，今年已拖累 EPS 成長約 1.5%–2%；策略選項無法保證成交，出售可能認列損失；醫療器材合規方面，第三方紀錄顯示 2025 年 7 月曾收到 FDA 483 觀察（非警告信、原文未核）","h_ref":"H2","clock":"🔥","threshold":"2027 年 Lincare 拖累 EPS 成長仍 ≥ 1%，或出現 FDA 警告信","evidence_refs":["product_recall_warning#0"]}],"single_thing":{"description":"2027 年 2 月公布的 2027 年調整後 EPS 指引中點（排除匯率）年增低於 8%","why_fatal":"現價約 28.7 倍當年 EPS，倍數要靠 8%–12% 複利延續撐住；中點低於 8% 代表重組節省、Lincare 修復與 Woodside 投產都補不回量能疲弱，2027 年 EPS 落到 18.6 美元以下、倍數往 23–24 倍靠，股價約 −13%～−17%，是所有變數裡對五年報酬敏感度最大的一項","if_happens":"停止加碼，持股減至半倉；基本情境 2027 年 EPS 下修到 18.6 美元以下並重跑情境","how_monitor":"Q4 2026 財報電話會議（預計 2027 年 2 月）的全年指引；先行指標為 Q4 實際 EPS 是否 ≥ 4.45 美元（指引中點）","probability":"約 35%：Q4 指引只年增 5%–7%、公司不假設總經改善；但重組節省與 Lincare 拖累消失是 2027 年順風"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":28.3,"peg_fy2":3.7,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":16.47,"FY2026E":17.89,"FY2027E":18.2,"FY2028E":null},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（non-GAAP）。FY2025A 16.47 為推導值：公司 2026 年指引 17.82–17.92 美元對應年增 8%–9%（二手摘要），17.87 ÷ 1.085 ≈ 16.47，原始數字事實表未涵蓋；GAAP 稀釋 EPS 2025 年為 14.61。FY2026E、FY2027E 為 yfinance 共識；FY2028E 共識事實表未涵蓋（只有兩個年度）"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年全年 EPS 指引","impact":"高","watch":"指引中點年增是否 ≥ 8%（排除匯率）、Lincare 重組與策略選項進度"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"Woodside 氨廠兩組 ATR 氫氣設備分批啟動，下半年開始貢獻、2028 年滿載","impact":"中","watch":"啟動時程是否延後、客戶策略檢討結果"},{"date":null,"date_precision":null,"type":"other","event":"Lincare 策略選項評估結果（管理層未給時程）","impact":"中","watch":"出售價格與是否認列損失"},{"date":null,"date_precision":null,"type":"macro","event":"荷莫茲海峽與卡達氦氣出口恢復","impact":"中","watch":"氦氣價格回落速度與 Linde 長約客戶留存"}]}
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
