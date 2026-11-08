你是 DD 管線 v20 的判斷層閘（gate），標的 AAPL（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝114.477 十億美元｜期間與口徑：Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-09-26，公告於 2026-11-02））
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝35.631 十億美元｜期間與口徑：Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-09-26，公告於 2026-11-02））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝31.12 %｜期間與口徑：Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（35,631÷114,477 自算）（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-09-26，公告於 2026-11-02））
- `f_kpi3_gaap`（q1_business）｜GAAP 毛利率＝47.9 %｜期間與口徑：Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-09-26，公告於 2026-11-02））
- `f_kpi7_iphone`（q1_business）｜iPhone 營收＝57.583 十億美元｜期間與口徑：Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（numbers.latest_quarter_kpis.items[7]，as_of Q4 FY2026（季末 2026-09-26，公告於 2026-11-02））
- `f_kpi8_services`（q1_business）｜Services 營收＝31.573 十億美元｜期間與口徑：Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（numbers.latest_quarter_kpis.items[8]，as_of Q4 FY2026（季末 2026-09-26，公告於 2026-11-02））
- `f_peer_aapl_gross_margin_pct`（q2_moat）｜AAPL 毛利率＝48.79 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAPL.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_aapl_operating_margin_pct`（q2_moat）｜AAPL 營業利益率＝33.01 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAPL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_aapl_fcf_margin_pct`（q2_moat）｜AAPL FCF 利潤率＝28.41 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAPL.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_msft_operating_margin_pct`（q2_moat）｜MSFT 營業利益率＝47.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_msft_fcf_margin_pct`（q2_moat）｜MSFT FCF 利潤率＝17.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_googl_fcf_margin_pct`（q2_moat）｜GOOGL FCF 利潤率＝4.19 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GOOGL.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amzn_operating_margin_pct`（q2_moat）｜AMZN 營業利益率＝12.89 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMZN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_amzn_fcf_margin_pct`（q2_moat）｜AMZN FCF 利潤率＝-6.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMZN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_sony_gross_margin_pct`（q2_moat）｜SONY 毛利率＝33.03 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SONY.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_sony_operating_margin_pct`（q2_moat）｜SONY 營業利益率＝14.6 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SONY.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝9.5 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝10.65 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝11.82 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝477692.15 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（37 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝569273.41 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（34 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_gaap_eps`（q4_capital）｜GAAP 稀釋 EPS＝2.1 USD｜期間與口徑：Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results；8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-09-26，公告於 2026-11-02））
- `f_kpi5`（q4_capital）｜營運現金流＝28 十億美元｜期間與口徑：Q4 FY2026（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Apple IR 新聞稿 https://apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results（CFO 談話，約數）（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-09-26，公告於 2026-11-02））
- `f_kpi6_sbc_fy2026`（q4_capital）｜SBC 占營業利益（FY2026 全年，非單季）＝8.72 %｜期間與口徑：FY2026 全年（截至 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000024/a8-kex991q4202609262026.htm（13,789÷158,063 自算）（numbers.latest_quarter_kpis.items[6]，as_of FY2026 全年（截至 2026-09-26，公告於 2026-11-02））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝37757.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 94479.0、現金 56722.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝14532.18 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝36.04 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 9.5，分子＝快照價 342.37｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝342.37 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝38.13 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝7.95 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 8.8 → 9.5（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝10.49 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.31 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 342.37 / W52 292.82 / W104 259.47 / W250 208.88 / W250 13週斜率 1.38%」
- `f_ma_w104`（q5_valuation）｜104 週均線＝259.47 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝208.88 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_rsi14`（q5_valuation）｜RSI(14)＝51.46｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=False｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝16.93 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝292.82 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（18 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 自述：競爭對手以激進定價與極低成本結構競爭並模仿產品，部分對手可近乎無利潤甚至虧損銷售。
  - 來源：SEC EDGAR 10-K FY2026 Item 1（as_of 2026-11-03）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：Samsung預期記憶體短缺到2027年會惡化並持續至2028年（AI資料中心搶產能，屬供給面擠壓消費電子）
  - 來源：TechCrunch: Samsung expects memory shortage to worsen through 2027 and last until 2028（as_of 2026-07-31）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：IDC預估2026全球智慧型手機出貨年減12.9%至約11.2億支，2027年預期小幅回升2%，記憶體價格mid-2027趨穩但不會回到先前水準；平均售價預估創高約523美元
  - 來源：IDC via eeNews Europe / fonearena (2026-02)（as_of 2026-02-26）｜affects：thesis.R、valuation
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：後續預測下修2027：Counterpoint 8月預估2027約10.6億支、年減1.4%；Omdia 6月預估年減0.9%；2028預期反彈約+5%（二手彙整，未核原廠）
  - 來源：pctipp.ch: Analysten: Smartphone-Markt wird sich erst 2028 erholen（as_of 2026-08-31）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：IDC：2027年下行風險來自可能的庫存堆積
  - 來源：IDC via fonearena（as_of 2026-02-27）｜affects：thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：歐盟執委會 2025-04-23 依 DMA Art.5(4) 對 Apple 罰 5 億歐元並下令停止限制開發者導流；Apple 已上訴；Art.6(4) 調查已有初步認定，若最終認定違規可罰至全球年淨銷售 10%。
  - 來源：SEC EDGAR 10-K FY2026 Item 3（as_of 2026-11-03）｜affects：thesis.R、decision_inputs.bear、valuation
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：美國 DOJ 與多州 2024-03-21 提起壟斷訴訟（performance smartphones／smartphones），尋求衡平救濟；另有州與聯邦民事訴訟求償。
  - 來源：SEC EDGAR 10-K FY2026 Item 3（as_of 2026-11-03）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：Google 搜尋授權安排受政府調查與訴訟影響；若上訴推翻，DOJ 原提補救（禁止 Google 向 Apple 提供搜尋分發商業條件）可能生效。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-11-03）｜affects：thesis.R、valuation
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：蘋果絕大多數製造由位於中國大陸、印度、日本、南韓、台灣、越南的外包夥伴完成；10-K 風險因素指出貿易限制（關稅與進出口管制）可能對業務與供應鏈造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-11-03）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Apple 處理器由 TSMC 單一供應，地緣衝突、天災或技術故障風險被放大；Apple 約占 TSMC 營收四分之一（較舊報導）。
  - 來源：iMore: Report says Apple's heavy reliance on iPhone chipmaker could be weakness（as_of 2024-01-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Taipei Times（Bloomberg 來源）報導：Apple 供應鏈彈性低於往常、晶片短缺限制成長；TSMC 鳳凰城廠僅產少量 Apple 晶片；Apple 與 Intel、Samsung 有備援代工初步洽談。
  - 來源：Taipei Times 2026-05-06; The Edge Malaysia（as_of 2026-05-06）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Apple 10-K 風險因素自述：市場競爭激烈且技術變化快速，公司必須持續推出新產品、服務與技術並成功管理新技術的轉換與採用。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-11-03）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Apple 服務主管 Eddy Cue 稱 AI 可能在約十年內取代 iPhone
  - 來源：apfelpatient: Eddy Cue from Apple AI could soon make iPhones obsolete（as_of 2025-05-07）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：報導稱 Apple 付費訂閱達 15 億，Services 營收 307 億美元但出現 2022 年以來首次季減，CFO 歸因於手遊、部分國家 App Store 商業模式變動與美國連結外部付款裁決。
  - 來源：ithinkdiff: Apple Hits 1.5 Billion Paid Subscriptions as Services Growth Slows（as_of 2026-07-31）｜affects：moat_trend、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：股東集體訴訟（Siri AI 與 Epic 合規）Apple 於 2026-02 聲請駁回，南韓國民年金為首席原告；無駁回裁定紀錄
  - 來源：MacRumors：Apple Asks Judge to Toss Fraud Claims Over Siri AI, Epic Compliance（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `major_events#2`（major_events｜方向 -｜狀態 ok）：10-K（FY2026）Legal Proceedings：歐盟 DMA 5(4) 調查罰款 5 億歐元並已上訴；6(4) 調查有初步認定；美國 DOJ 反壟斷訴訟進行中
  - 來源：SEC EDGAR 10-K FY2026 Item 3（as_of 2026-11-03）｜affects：decision_inputs.bear、thesis.R、moat_trend
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：股東證券詐欺集體訴訟（Siri AI、Epic 合規）Apple 2026-02 聲請駁回，無裁定紀錄
  - 來源：MacRumors（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K 披露 DOJ 反壟斷訴訟與歐盟 DMA 罰款 5 億歐元（已上訴）
  - 來源：SEC EDGAR 10-K FY2026 Item 3（as_of 2026-11-03）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":544.0,"bear_5y_price":208.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":9.6,"ev5y_pct":7.3,"irr_base_pct":1.9,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":9.5,"pe":36.04,"basis":"FY2027E 共識 EPS 的前瞻口徑；終端倍數同樣乘在情境年度 EPS 上"},"eps":{"bull":[9.8,11.3,13.1,15.0,17.0],"base":[9.3,10.4,11.55,12.7,13.9],"bear":[8.7,8.9,9.3,9.8,10.4]},"pe":{"bull":32,"base":27,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.31,"net_buyback":1.7},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AAPL_Q3_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：CFO 給九月季總營收年增 9%–11%。（原話："company revenue to grow between 9% and 11% year-over-year."）
- 2026-07-30｜CFO｜guidance：CFO 給九月季 iPhone 年增中十位數。（原話："reported growth rate for iPhone to be mid-teens year-over-year."）
- 2026-07-30｜CFO｜guidance：CFO 說九月季 Services 成長率與六月季大致相近（已扣除約 2.5 個百分點匯率逆風的口徑）。（原話："reported growth rate to be largely similar to what we"）
- 2026-07-30｜CFO｜guidance：CFO 給九月季毛利率 47%–48%。（原話："We expect gross margin to be between 47% and 48%."）
- 2026-07-30｜CFO｜margin：九月季毛利率指引含約 1 個百分點關稅退款效益。（原話："approximately 1 percentage point related to tariff refunds."）
- 2026-07-30｜CFO｜guidance：九月季營業費用指引區間。（原話："$19.1 billion and $19.4 billion."）
- 2026-07-30｜CFO｜guidance：CFO 表示九月季以後不提供財測或色彩。（原話："providing any kind of color or guidance beyond the September quarter."）
- 2026-07-30｜CFO｜risk：財測前提：關稅政策維持現況、總經不惡化。（原話："global tariff rates, policies, and their application remain in effect"）
- 2026-07-30｜CFO｜risk：CFO 預期九月季總營收受匯率逆風影響（口徑：對年增率的連續季拖累）。（原話："sequential headwind of about 2.5 percentage points"）
- 2026-07-30｜CFO｜risk：CFO 預期九月季供給限制明顯加重。（原話："impact from supply constraints to increase significantly sequentially."）
- 2026-07-30｜CEO｜risk：CEO 說供給限制主因是 SoC 先進製程節點的可得性。（原話："primarily driven by the availability of the advanced"）
- 2026-07-30｜CEO｜risk：CEO 定性供給問題的根因，並說本季供給端要趕工。（原話："the root cause of it is not a regular supply issue."）
- 2026-07-30｜CEO｜risk：CEO 描述下一季供給端的處境。（原話："we're going to be scrambling on the supply side essentially."）
- 2026-07-30｜CFO｜margin：六月季公司毛利率 50.1%，含關稅退款約 2 個百分點；扣除後落在上季指引中點。（原話："favorable impact of approximately 2 percentage points."）
- 2026-07-30｜CFO｜margin：產品毛利率 40.1%（含關稅退款逾 2.5 個百分點）。（原話："Products gross margin was 40.1%, up 140 basis points sequentially."）
- 2026-07-30｜CFO｜margin：CFO 拆解毛利率連續季下滑：記憶體成本占主要，匯率影響小。（原話："I think that FX was a pretty minimal impact"）
- 2026-07-30｜CEO｜margin：CEO 說九月季記憶體採購成本再升。（原話："For September, we expect to pay even higher memory costs"）
- 2026-07-30｜CEO｜margin：CEO 說九月以後記憶體市價續漲，對公司影響可能加大。（原話："continuing to increase, which could drive an increasing impact on our business"）
- 2026-07-30｜CEO｜margin：CEO 說明 iPad／Mac 調價的原因。（原話："a 100-year flood on the memory pricing"）
- 2026-07-30｜CEO｜margin：CEO 說定價不採單一公式，看長期而非 90 天。（原話："think about it over the long term instead of a 90-day clock."）
- 2026-07-30｜CEO｜risk：CEO 提到 DRAM 只有三家供應商，正評估所有選項。（原話："primarily the DRAM market has 3 suppliers"）
- 2026-07-30｜CFO｜capital_allocation：六月季回購與股利金額。（原話："$4 billion in dividends and equivalents and $25.8 billion"）
- 2026-07-30｜CFO｜capital_allocation：期末現金與有價證券。（原話："$147 billion in cash and marketable securities"）
- 2026-07-30｜CFO｜capital_allocation：董事會宣布每股 $0.27 股利。（原話："cash dividend of $0.27 per share of common stock"）
- 2026-07-30｜CEO｜commitment：CEO 重申對美國 6,000 億美元投資承諾。（原話："we made a $600 billion commitment to the U.S. over 4"）
- 2026-07-30｜CEO｜commitment：CEO 說將把收到的關稅退款再投入美國。（原話："reinvest the tariff refunds we've received into the U.S."）
- 2026-07-30｜CEO｜commitment：Broadcom 多年協議，預期金額超過 300 億美元。（原話："American Manufacturing program is expected to exceed $30"）
- 2026-07-30｜CEO｜commitment：CEO 稱此為最大的美國製造承諾。（原話："our largest ever American manufacturing program commitment"）
- 2026-07-30｜CEO｜commitment：休士頓廠今年稍晚開始生產 Mac mini。（原話："make Mac mini there, too."）
- 2026-07-30｜CEO｜commitment：CEO 宣布這是最後一次法說，由 John Ternus 接手主持。（原話："this will be my final earnings call, and John will lead these calls going forward."）
- 2026-07-30｜CEO｜commitment：CEO 說 Arizona 晶圓廠今年供應的元件數量。（原話："we do source over 100 million components this"）
- 2026-07-30｜CEO｜product：CEO 對 Siri AI 公測回饋的描述。（原話："we are off the charts excited about Siri AI."）
- 2026-07-30｜CEO｜product：Siri AI 運算成本回收方式：iCloud+ 升級方案，但尚無完整計畫。（原話："we will have some kind of upgrade possibilities on iCloud+"）
- 2026-07-30｜CEO｜product：CEO 說 Siri AI 在歐盟尚無法同步推出，仍與歐盟執委會協商。（原話："we're working closely with them to try to get to something"）
- 2026-07-30｜CEO｜product：中國方面僅取得原始 Apple Intelligence 功能的出貨核准，Siri AI 後續仍需工作。（原話："approval to ship sort of the original features of Apple"）
- 2026-07-30｜CEO｜product：CEO 提到 MacBook Neo 需求強、仍在努力補足供給。（原話："we're continuing to work hard to meet demand"）
- 2026-07-30｜CEO｜competition：CEO 談端側 AI 的策略地位。（原話："strategic and sort of a competitive weapon, if you will."）
- 2026-07-30｜John Ternus｜competition：Ternus 被問競爭格局（OpenAI 裝置、SpaceX AI 手機）時的回答。（原話："we're just really focused on our plans and very excited about it."）
- 2026-07-30｜CFO｜customer：CFO 說近一季美國教育機構 MacBook Neo 大單約半數取代 Windows／Chromebook。（原話："about half of the MacBook Neo large purchases"）
- 2026-07-30｜CFO｜customer：付費訂閱數里程碑。（原話："1.5 billion in paid subscriptions."）
- 2026-07-30｜CEO｜customer：CEO 對 iPhone 是否有拉貨的回答：資料上看不出來。（原話："it's not obvious in the data that what you're asking is true."）
- 2026-07-30｜CEO｜customer：CEO 說 iPad／Mac 漲價後的價格彈性尚無定論。（原話："it's just too early to come to a definitive"）
- 2026-07-30｜CFO｜risk：CFO 說 App Store 受手遊疲弱影響，六月季略遜預期。（原話："more softness on mobile gaming in the App Store."）
- 2026-07-30｜CFO｜risk：CFO 提到美國仍受法院對外部連結交易的裁決約束。（原話："we do continue to operate under a court ruling"）
- 2026-07-30｜CFO｜risk：CFO 說最高法院將審理其上訴。（原話："we're pleased that the Supreme Court will hear our appeal."）
- 2026-07-30｜CFO｜guidance：CFO 拆解 Services 匯率逆風：自三月季到九月季約 5 個百分點。（原話："foreign exchange to drive about a 5 percentage point headwind"）
- 2026-07-30｜CFO｜capital_allocation：營業費用年增 23%，主因研發投資。（原話："up 23% year-over-year, driven by investments in R&D"）
- 2026-07-30｜CEO｜capital_allocation：CEO 回答 Siri AI 對資本密集度的影響：成本與 iCloud 升級的平衡尚不確定。（原話："what the balance of that is a bit uncertain at the moment."）

### 問答異常語氣（迴避／改口／保留）
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Reitzes 追問 12 月季供給限制影響與可否給指引｜答法：CFO 明說九月季以後不提供任何色彩或指引，未回應 12 月季的數字
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Wamsi Mohan 問 Ternus 競爭格局是否改變（OpenAI 裝置、SpaceX AI 手機）｜答法：Ternus 未談競爭對手，只說機會很多、專注自己的計畫
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Wamsi Mohan 問 Siri AI 是否改變資本密集度｜答法：CEO 答混合模式、成本與 iCloud 升級的平衡尚不確定，未給數字
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Michael Ng 問 Siri AI 運算成本與 iCloud+ 回收｜答法：CEO 稱還早、沒有完整計畫，只說會有 iCloud+ 升級選項
- AAPL_Q3_2026_Earnings_Call_20260730.md｜問：Reitzes 問是否可能拓寬矽晶圓供應商（含 Arizona 新晶圓廠）｜答法：CEO 改談需求超預期並稱非供應商問題，未回答是否擴大供應商

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 3 |
| customer_second_source | not_applicable | 0 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 5 | 3 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | found | 4 | 0 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 4 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：Apple in-house chip modem C1 OR second source supplier diversify 2026；Apple single-source supplier risk customer diversify Intel foundry OR Samsung image sensor 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260731","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"iPhone 17/18 的 AI 換機週期是結構性升級，不是一次性拉貨"},{"id":"H2","text":"記憶體成本可經由漲價與 mix 轉嫁，公司毛利率在 FY27 守住底線"},{"id":"H3","text":"Services 能在監管切割下維持雙位數成長與約 75% 毛利，市場續給 ≥ 28x 前瞻倍數"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"記憶體成本通膨延續至 FY27，漲價觸及價格彈性 → 量價雙輸。Cook 稱這是「記憶體定價的百年一遇洪水」，且明說九月之後市場價格續漲、對業務的影響「增加中」；抵銷手段（結轉庫存利益、非記憶體零件降價）管理層自己說會遞減。"},{"id":"R2","text":"Services 監管切割：美國 link-out 裁定執行中（最高法院已受理上訴）、EU DMA 使 Siri AI 無法在歐盟的 iPhone/iPad 首發、若干國家 App Store 商業模式已變更、Google 預設搜尋協議因 Mehta 救濟裁定被迫非排他化。"},{"id":"R3","text":"AI 平台層位移：Apple 不擁有前沿模型（法說對模型來源與夥伴全程未揭露，僅稱端側＋私有雲＋「部分第三方雲」的混合架構），且旗艦 AI 功能在歐盟 iPhone/iPad 缺席、中國僅核准原版功能。若 agent 形態繞過 App／Safari 入口，或新形態 AI 裝置成為新入口，分發層租金基礎鬆動。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE（FY27 共識）≤ 27x（約 $261）且剔關稅毛利率連 2 季 ≥ 46%——雙條件 AND，缺一不進場","irr_base_pct":4.2,"ev5y_pct":19.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.8,"ev5y_pct":19.0,"irr_base_pct":4.2,"max_dd_pct":-45.0,"bull_5y_price":512.0,"bear_5y_price":210.0,"p_bull_pct":25.0,"p_bear_pct":28.0,"rearm_trigger":"Fwd PE（FY27 共識）≤ 27x（約 $261）且剔關稅毛利率連 2 季 ≥ 46%——雙條件 AND，缺一不進場","price_at_dd":309.21,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"AAPL","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Apple Inc."},"oneliner":"iPhone 與 Mac 在縮水的市場裡搶到份額，但現價要 36 倍 FY27 EPS，記憶體成本還在漲；好公司太貴，等約 257 美元且毛利率守住 45% 再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是 25 億台裝置持有人的換機錢和過路費，眼下利潤被卡在記憶體這一節。","reasoning":"九月季營收 1,144.77 億美元，iPhone 占 50.3%、Services 27.6%、Mac 9.4%、穿戴 7.3%、iPad 5.4%（Mac、iPad、穿戴金額取自 2026-11-02 法說 CFO Parekh 口述）。公司毛利率 47.9%、營益率 31.1%。Services 營收不到三成，毛利卻占約 44%（315.73 億美元乘 76%，除以總毛利 548.3 億美元，76% 取自同場法說）。單點依賴有兩個：iPhone 占一半營收；系統晶片只靠台積電，DRAM 只有三家供應商。間接通路占淨銷售約 60%，電信業者占應收帳款 33%，單一客戶 13%，這是信用集中，不是需求集中。產業位置判在收縮期，IDC 8 月預測 2026 年手機出貨年減 16.7%、平均售價年增 27.6%，短缺壓量抬價。供需判斷是週期性將反轉，但時間偏晚：Samsung 預期短缺延續到 2028，Counterpoint 預期 2027 年手機再減 1.4%。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_gaap","f_kpi7_iphone","f_kpi8_services"],"verdict_values":{"revenue_quality":"Services 屬經常性收入，付費訂閱超過 15 億；硬體看換機週期，FY26 為高基期。","unit_econ_note":"九月季產品毛利率 37.2%（含約 1 個百分點關稅退款），Services 76%；各產品單位毛利事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"高毛利平台、低資本密度、持續回購"},"industry":{"clock_phase":"IV","sd_verdict_source":"依據 IDC 2026-08-26 預測：手機出貨年減 16.7%、平均售價年增 27.6%。供需屬週期性將反轉，Samsung 2026-07-31 稱短缺延續到 2028。","bargaining":{"up":"上游最強的是 DRAM 三家供應商與台積電。2026-07-30 法說 Cook 稱記憶體定價是百年一遇洪水，2026-11-02 法說 Ternus 稱前所未見，製造採購承諾由六月到九月增加 330 億美元。","down":"下游電信與經銷分散，間接通路約六成，定價權仍在 Apple 手上。","geo":"製造集中在中國大陸、印度、日本、南韓、台灣、越南；印度約占 iPhone 產量四分之一，大中華區 FY26 營收年增 28%。"},"profit_pool_dir":"短期利潤由手機品牌流向記憶體供應商；五年營業利益池占比事實表未涵蓋，不做降檔判斷。","tam_table":[{"item":"全球手機出貨 2026","value":"IDC 8 月預測年減 16.7%"},{"item":"手機平均售價 2026","value":"IDC 預測 581 美元，年增 27.6%"},{"item":"Apple 全球手機份額 2026Q3","value":"Counterpoint 22%，去年同期 18%"},{"item":"全球 PC 2026Q3","value":"IDC 年減 20.1%；Mac 份額 9.5%，去年同期 8.5%"},{"item":"營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河穩定：硬體端擴大，Services 端縮減，兩邊相抵。","reasoning":"機制是 iOS、自研晶片與服務綁在同一個裝置基礎上，活躍裝置超過 25 億台。方向看份額：Counterpoint 2026 年第三季全球手機 22%（去年同期 18%），IDC 的 Mac 份額 9.5%（8.5%），中國手機 17.8%（15.8%）。同業 ROIC 無資料，改看 FCF 利潤率：Apple 28.4%，MSFT 17.3%、GOOGL 4.2%、AMZN −6.4%，對手正把現金投進 AI 基礎建設。反向證據在 Services：九月季 App Store 與去年相近，十二月季指引 8%～9%，監管與第三方授權都在壓。AI 淨增量尚未出現，Siri AI 目前只看到雲端成本進 Services 銷貨成本、硬體遞延增加，付費升級還沒定價；AI 長在自有作業系統上屬強化，agent 若從 App 層繞過入口就是替代，分界年看 2028。兩項評分 8 已含生態攻擊的扣分。FY26 毛利率 48.79% 是四年高點，約 0.7 個百分點來自關稅退款（九月季約 11 億、六月季約 22 億美元，粗估），記憶體結轉庫存也屬短期因素，這些不當結構性。可能看錯的地方：份額上升有一部分來自 Android 缺料，短缺結束後可能回吐。","fact_refs":["f_peer_aapl_gross_margin_pct","f_peer_aapl_operating_margin_pct","f_peer_aapl_fcf_margin_pct","f_peer_msft_operating_margin_pct","f_peer_msft_fcf_margin_pct","f_peer_googl_fcf_margin_pct","f_peer_amzn_operating_margin_pct","f_peer_amzn_fcf_margin_pct","f_peer_sony_gross_margin_pct","f_peer_sony_operating_margin_pct","f_kpi3_gaap"],"verdict_values":{"moat":{"mechanism":"iOS 與自研晶片綁住超過 25 億台裝置，換機與服務都在自家平台結算；換邊要同時放棄資料、App 與跨裝置連動。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力穩定、定價權穩定。份額三項都上升，但 App Store 九月季與去年相近，十二月季 Services 指引降到 8%～9%，CFO 說漲價彈性現在判斷還太早。","competitor_notes":[{"name":"MSFT","strategy_note":"營益率 47.1% 高於 Apple，FCF 利潤率 17.3%，資本壓在 AI 基礎建設；消費端入口不是直接對手。"},{"name":"GOOGL","strategy_note":"同時是 Android 陣營與搜尋授權付款方，FCF 利潤率只剩 4.2%；對 Apple 既帶收入也帶依賴。"},{"name":"AMZN","strategy_note":"營益率 12.9%、FCF 利潤率 −6.4%，資本投入雲端；與 Apple 重疊在內容與裝置，威脅低。"},{"name":"SONY","strategy_note":"毛利率 33.0%、營益率 14.6%，消費電子同業中定價力明顯低於 Apple。"}],"peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，改以份額方向與 FCF 利潤率對照。","threats":[{"level":"🔴","text":"監管與司法切割 Services：歐盟 DMA、美國 DOJ 訴訟、外部連結裁決、Google 搜尋授權。","p":"40%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#2","lawsuit_class_action#1","channel_business_model_shift#1"]},{"level":"🔴","text":"AI agent 繞過 App 與 Safari 入口，分發租金鬆動。目前沒有收入受損證據，所以還不列為架構替代。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"對手可接近零利潤甚至虧損銷售；但本輪短缺中 Android 受傷更深，Apple 份額反而上升。","p":"20%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"系統晶片由台積電單一供應，製造集中亞洲，關稅與地緣事件會直接影響出貨。","p":"15%","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉率事實表未涵蓋，依淨再投資接近零推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多半是同一人；活躍裝置超過 25 億台，九月季升級人數與付費帳戶都創紀錄。"},{"item":"決策層級","level":"🟡","text":"替代要在整個生態系層級衡量，換機成本高；但最關鍵的代理變數是漲價後流失率，CFO 2026-11-02 說現在判斷彈性還太早。"},{"item":"價值鏈分配","level":"🟡","text":"DRAM 三家供應商正在多拿，剔關稅退款毛利率由六月季 48.1% 降到九月季 46.9%，十二月季指引中點 45.5%。若高價延續到 2028 應改判紅。"},{"item":"社會容忍度","level":"🔴","text":"App Store 抽成已碰到政治上限：歐盟罰款 5 億歐元並下令停止限制導流，美國外部連結裁決執行中，DOJ 訴訟進行中。"}],"roiic":"無法計算：FY24～FY26 淨利減 FCF 累計 −57 億美元，淨再投資接近零，分母不成立；投入資本事實表未涵蓋（financial_history.years，yfinance 年報）。","reinvest_rate":"約 7.5%（代理口徑：FY26 淨利減去 FCF 扣 SBC 後的金額，再除以淨利；資本支出與折舊事實表未涵蓋）","endo_ceiling":null,"formula_note":"增量報酬乘再投資率對 Apple 失效，分母接近零時結果沒有意義。成長來自定價、mix 與回購，不是新投入資本。採購承諾與 AI 算力若持續放大，再投資率會上升，需要重算。"}}}},"q3_growth":{"verdict":"五年後跑道中等：手機份額還有空間，第二條成長曲線尚未被財報證明。","reasoning":"成長靠價、mix 和回購，量受供給限制。FY26 營收年增 15.1%、EPS 年增 20%；FY23～FY26 營收 CAGR 7.7%、EPS CAGR 13.6%（financial_history.years，yfinance 年報）。三年共識 EPS CAGR 9.6%（8.98 到 11.82，Koyfin 2026-11-07，分析師家數事實表未涵蓋）。內生上界算不出，保守當作共識已超出。缺口歸因：淨回購每年約 1.7 個百分點，其餘來自定價與 mix，不依賴倍數上升。共識內部有一個待驗的組合：FY27 EPS 9.5 在費用年增 12%、稅率 17%、平均股數約 144 億下，需要毛利額約 2,480 億美元；若營收 5,693 億美元，毛利率約 43.6%，若營收只增 10%，毛利率要 47.1%，高於十二月季指引 45%～46%。跑道判中等：22% 是出貨份額，不是高階客群滲透率，後者事實表未涵蓋，所以不按份額直接給寬；Duo、Siri AI 付費、健康與家庭都還沒有營收證據，不算第二條曲線。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"FY26 量價併進，回購貢獻約 2 個百分點；FY27 以單價與 mix 為主，量受供給限制。","runway_years":"不給年數：高階客群滲透率事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬乘再投資率對 Apple 失效，FY24～FY26 淨利減 FCF 累計 −57 億美元，淨再投資接近零；上界留空，保守當作共識 9.6% 已超出。","segments":[{"item":"iPhone 九月季","value":"575.83 億美元，年增 17%"},{"item":"Services 九月季","value":"315.73 億美元，年增 10%，毛利率 76%"},{"item":"Mac 九月季","value":"108 億美元，年增 24%"},{"item":"穿戴與家庭九月季","value":"83 億美元，年減 8%"},{"item":"iPad 九月季","value":"62 億美元，年減 10%"},{"item":"產品合計九月季","value":"829 億美元，年增 12%，毛利率 37.2%"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"接近成立：剔退款後連兩季季減，去年同季毛利率事實表未涵蓋"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"手機與 Mac 份額都上升"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"iPhone 9 月才漲價；Mac 出貨 IDC 年減 11.3%，但受供給限制"},{"item":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"note":"FY23～FY26 為 13.6% 對 7.7%，差 5.9 個百分點"},{"item":"FCF 對淨利低於 0.75 連 2 年","lit":false,"note":"FY26 為 1.03，FY25 為 0.88"},{"item":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"FY26 為 2.9%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"出貨量萎縮，但金額因單價上升而擴大"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"item":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"事實表未涵蓋"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"未發生"}]}}},"q4_capital":{"verdict":"資本配置穩健，但在 36 倍回購的報酬偏低。","reasoning":"FY26 FCF 1,360.6 億美元對淨利 1,321.8 億美元，轉換率 1.03；SBC 137.9 億美元，占營收 2.9%、占營業利益 8.7%。九月季回饋股東 280 億美元（回購 240 億、股利 39 億），現金與有價證券由六月季 1,470 億降到 1,370 億，總債務 800 億（2026-07-30、2026-11-02 法說 CFO Parekh）。公司已取消淨現金歸零目標，CFO 只說保留彈性，沒有新目標。現金需求正在變大：製造採購承諾季增 330 億美元，美國四年 6,000 億美元承諾，AI 算力需求管理層說還在很早期。以現價回購的盈餘收益率約 2.8%。近三年現金去向四分、回購均價與債務到期結構事實表未涵蓋。事實表淨負債 378 億美元與 CFO 口徑淨現金約 570 億美元的差異，應來自長期有價證券與租賃，看償債能力採 CFO 口徑。","fact_refs":["f_kpi4_gaap_eps","f_kpi5","f_kpi6_sbc_fy2026","f_net_debt_m","f_shares_diluted_m","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"FY26 唯一具規模的收購是 Q.ai，約 20 億美元，占市值約 0.04%，尚無已實現報酬可量。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"以現價計盈餘收益率約 2.8%（1÷36.04）；回購均價與 10 年期殖利率事實表未涵蓋，只要 10 年期高於 0.8% 就不過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"FY26 SBC 137.9 億美元，占市值約 0.28%；FY26 平均稀釋股數較 FY25 減少約 2%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，Q.ai 金額僅占市值約 0.04%，現金去向四分資料事實表也未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求 EPS 五年年增約 16% 才賺得到 8%，我不相信。","reasoning":"現價 342.37 美元等於 36.04 倍 FY27 共識 EPS、38.13 倍 FY26 EPS。五年要賺 8%，終端股價要 503 美元：終端 27 倍需要 EPS 年增約 15.7%，32 倍需要約 11.8%，共識三年 CAGR 只有 9.6%。基準情境五年後約 375 美元，年化約 2%，倍數收斂吃掉大部分 EPS 成長。12 個月目標用 32 倍乘 FY28 Base EPS 10.4，約 333 美元；24 個月用 30 倍乘 FY29 Base EPS 11.55，約 347 美元。賣方平均目標價 327～331 美元低於現價，但資料日是 6 月與 8 月，已舊；高低 400 與 200 美元相差 2 倍，分歧不算極端，小幅支持不追。同業前瞻倍數事實表未涵蓋，終端倍數無法做同業現值對照，以本股現值與 27 倍進場門檻為錨。近 3 個月 FY1 上修 7.95% 應是財年切換造成，不當上修動能。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_ev_s_fwd","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"FY27 共識前瞻本益比與 PEG","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋，事實表只有同業利潤率，無法做倍數對照。"},"fwd_pe":36.04,"peg":3.75,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"36.04 倍 FY27 共識 EPS，PEG 3.75（36.04 除以三年 CAGR 9.6），高於 2 倍的昂貴線；五年基準價約 375 美元，年化約 2%，低於 8%。五年分位事實表未涵蓋，四個年度端點分位 100 不當五年分位。結論為過高。","upside_short_pct":-2.8,"upside_mid_pct":1.2,"denominator_disputed":true,"denominator_note":"trailing 分母 8.98 含關稅退款（九月季 0.05 美元；六月季金額未揭露，按毛利率約 2 個百分點粗估約 0.10 美元）。前瞻分母 9.5 的爭點是記憶體成本。兩個分母都不支持便宜論證。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是低估管理層保守度與 Apple 的稀缺溢價。","reasoning":"最可能看錯三處。一，Base EPS 比共識低約 2%，但上一季指引偏保守，九月季營收與 iPhone 都超過區間，看錯就是錯過上漲。二，倍數可能長期維持 30 倍以上，Apple 的 FCF 利潤率遠高於投入 AI 的同業，市場可能繼續給稀缺溢價。三，記憶體短缺若在 2027 年中緩解，毛利率回升會快過我的路徑。衰退信號成立一項（FY23～FY26 EPS CAGR 高於營收 CAGR 5.9 個百分點），毛利率年減接近成立但去年同季資料事實表未涵蓋，價值陷阱風險判中等。壓力測試三組：FY29 後成長率降到 15%、10%、5%，終端倍數 30、26、18 倍，五年後股價約 458、363、229 美元，兩組不虧。法說迴避項：2026-07-30 Cook 未回答是否拓寬矽供應商，Ternus 未談 OpenAI 裝置與 SpaceX AI 手機；2026-11-02 Khan 兩次被問記憶體採購安排都只回採購承諾，Ternus 未解釋 iPhone 18 標準版缺席。歷史最大回撤事實表未涵蓋。RSI 標示不可用，不引用。","fact_refs":["f_ma_state","f_ma_w104","f_ma_w250","f_fwd_pe_latest","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"高基期加成本上行，估值沒有留緩衝"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":9.5,"pe":36.04,"basis":"FY2027E 共識 EPS 的前瞻口徑；終端倍數同樣乘在情境年度 EPS 上"},"eps":{"bull":[9.8,11.3,13.1,15.0,17.0],"base":[9.3,10.4,11.55,12.7,13.9],"bear":[8.7,8.9,9.3,9.8,10.4]},"pe":{"bull":32,"base":27,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.31,"net_buyback":1.7},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-50,"hi":-35,"basis":"上緣：Bear FY27 EPS 8.7 乘 25 倍約 218 美元，約 −36%，取整到 −35%；中段：250 週均線 208.88 美元約 −39%；下緣：8.7 乘 20 倍約 174 美元，約 −49%，取整到 −50%。歷史回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"Duo 與新機帶動單價，FY27 營收接近共識約 5,690 億美元、毛利率約 44.5%；記憶體 2028 年回落，Siri AI 付費開始貢獻，終端 32 倍。","base":"FY27 營收年增約 12%、毛利率約 45.5%，EPS 9.3，比共識低約 2%；之後每年增約 10%，含回購約 1.7 個百分點。終端 27 倍對應約 10% 成長的成熟平台；同業倍數事實表未涵蓋，以本股現值 36.04 倍與前份 28 倍下限為錨。","bear":"記憶體高價延續到 2028，漲價後需求轉弱，FY27 營收僅增約 10%、毛利率約 44.5%；Services 受監管與授權影響降到個位數低段，終端 20 倍。機率 30%：Samsung 與 Counterpoint 都指向 2027 仍緊，且內生上界算不出，保守當作共識已超出。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Samsung 預期短缺延續到 2028；Counterpoint 預期 2027 年手機再減 1.4%；2026-11-02 法說 Ternus 說記憶體採購價繼續上升、結轉庫存效益遞減；IDC 提示 2027 年庫存堆積風險。","assumption":"漲價補得回成本，需求不因單價上升而縮。","consequence":"五年虧 50% 最可能的故事：毛利額連續下滑，FY31 EPS 只有約 10 美元，市場當低成長硬體股給 18 倍，股價約 180 美元，虧約 47%。","ruling":"採納，列為 Bear 路徑。這與 Single Thing 指向同一件事，不另立事件。","watch":"每季毛利額年增率、製造採購承諾、存貨變化","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","supply_demand_durability#4"],"fact_refs":["f_kpi3_gaap","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"2025-05 Eddy Cue 稱 AI 可能約十年內取代 iPhone；10-K 自述技術變化快。2026-11-02 法說 Daryanani 問客戶關係是否會由裝置轉到 agent，Ternus 只答 iPhone 是個人中樞，並說 Siri 目前仍以請求為主。","assumption":"Agent 必須經過 iOS 才拿得到個人脈絡。","consequence":"入口租金鬆動，Services 與換機同時受傷。","ruling":"部分採納。風險真實但時間窗在 2028 之後，近兩年資料無法裁決，不當作現價的主要否決理由。","watch":"App Store 年增方向、每週造訪人數、付費訂閱數","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"view":"論點成功但股東經濟變差","evidence":"DMA 罰款 5 億歐元與停止令，第 6(4) 條若最終認定可罰至全球年淨銷售 10%，以 FY26 計約 479 億美元；DOJ 尋求衡平救濟；外部連結裁決執行中；Google 上訴若翻案可能禁止商業條件。十二月季指引列第三方授權為逆風，Siri AI 雲端成本進 Services 銷貨成本。","assumption":"Services 76% 毛利率可持續。","consequence":"裝置賣得再好，最肥的利潤仍會變薄。Services 占九月季毛利約 44%，抽成下修會直接打在倍數上。","ruling":"採納。社會容忍度判紅，Base 的 Services 成長只放 8%～10%。","watch":"Services 年增率與毛利率、最高法院裁決、DMA 最終認定","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","channel_business_model_shift#1","major_events#2","lawsuit_class_action#1"],"fact_refs":["f_kpi8_services"]},{"view":"價格已反映太多","evidence":"36.04 倍前瞻本益比、PEG 3.75；26 週上漲 16.9%；股價高於 52 週均線 16.9%。","assumption":"倍數維持 30 倍以上，且 FY27 營收年增約 19%。","consequence":"即使 EPS 達到共識，五年年化也只有個位數低段。","ruling":"採納，這是目前的主要約束。","watch":"FY27 共識前瞻本益比","fact_refs":["f_fwd_pe_latest","f_week26_return_pct","f_ma_w52"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 309.21 → 本次 342.37（+10.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=309.21","side_b":"本次 price_at_dd=342.37","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 309.21 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 309.21 美元：Bull 價 512、Bear 價 210，五年期望值 +19.0%，基準年化 4.2%，不對稱比 1.8","side_b":"本次情境、股價仍用 309.21 美元：Bull 價 544、Bear 價 208，五年期望值 +18.8%，基準年化 4.0%，不對稱比 1.93","ruling":"先換情境、股價不動：五年期望值少 0.2 個百分點，基準年化少 0.2 個百分點。不對稱比由 1.8 變為 1.93。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 309.21 美元：五年期望值 +18.8%，基準年化 4.0%，不對稱比 1.93","side_b":"本次情境、股價 342.37 美元：五年期望值 +7.3%，基準年化 1.9%，不對稱比 1.25","ruling":"再換股價、情境不動：起點價上漲 10.7%，五年期望值少 11.5 個百分點，基準年化少 2.1 個百分點，不對稱比由 1.93 降到 1.25。合計五年期望值比前份少 11.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與等待結論","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份股價 309.21 美元，FY27 前瞻本益比約 32 倍，估值偏貴，結論是等待。","side_b":"現價 342.37 美元，較前份高 10.7%，前瞻本益比 36.04 倍，估值改判過高，品質評級不變。","ruling":"採 B 側，等待結論不變。變動主要來自股價上漲，基本面沒有提供更高倍數的理由。","evidence_level":"高","settle_metric":"FY27 共識前瞻本益比","if_then":["若股價續漲而 FY27 共識未上修，不追","若股價跌到 27 倍附近且基本面無損，分批反買"],"evidence_refs":[]},{"axis":"品質判斷複核","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"前份：陷阱風險中等、護城河穩定、五年後跑道中等。","side_b":"本次三項不變。新證據兩邊都有：份額擴大、中國回升；另一邊剔退款毛利率兩季降約 260 個基點，Services 指引降到 8%～9%。","ruling":"三項維持。硬體端的好消息與 Services 端的壞消息方向相反，幅度還不足以改判。","evidence_level":"中","settle_metric":"手機份額、Services 年增率、毛利額年增率","if_then":["若 Services 連 2 季年增低於 7%，減碼一半","若份額續升且 Services 回到 10% 以上，仍不追，等估值條件"],"evidence_refs":[]},{"axis":"公司分類與週期位置","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份：品質複利成長，週期位置未填。","side_b":"本次相同。","ruling":"未變動。Apple 不按循環股處理，記憶體週期放在毛利情境中反映。","evidence_level":"高","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 25%、Bear 28%、最大回撤 −45%。","side_b":"本次 Bull 25%、Bear 30%、最大回撤範圍 −50%～−35%。","ruling":"內生上界算不出，保守當作共識已超出，Bear 機率提高到 30%；回撤改用範圍表達。","evidence_level":"中","settle_metric":"毛利額年增率","if_then":[],"evidence_refs":[]},{"axis":"重新進場門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE（FY27 共識）≤ 27x（約 $261）且剔關稅毛利率連 2 季 ≥ 46%——雙條件 AND，缺一不進場","side_b":"FY27 共識前瞻本益比 ≤ 27 倍（約 $257）且公司毛利率連 2 季 ≥ 45%，兩項同時成立才重跑研究","ruling":"進場價由 261 美元改 257 美元，因為 FY27 共識由約 9.67 降到 9.5。毛利率由 46% 改 45%，因為十二月季指引 45%～46% 已反映更高的記憶體成本，且多數關稅退款已收回。放寬毛利率的代價是可能太早進場，價格條件不放寬。主要約束是估值，毛利率只用來確認跌價不是論點失敗。","evidence_level":"中","settle_metric":"FY27 共識前瞻本益比、公司毛利率","if_then":["若兩項同時成立，重跑研究，通過後分批反買","若股價到位但毛利率低於 45%，不追"],"evidence_refs":[]},{"axis":"清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標","side_b":"毛利額連 2 季年減；毛利率連 2 季低於 44%；Services 連 2 季低於 7%；第三季手機份額低於 20%；FY27 共識 EPS 低於 9.0","ruling":"新增減碼與清倉指標，讓結論可以被數字否定。門檻取自本次情境：44% 與 9.0 是 Bear 路徑的邊界。","evidence_level":"中","settle_metric":"各季 8-K 與共識快照","if_then":["若毛利額連 2 季年減，減碼一半","若毛利額連 4 季年減且 FY28 共識 EPS 低於 9.5，清倉"],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"剔除關稅退款後，公司毛利額連續兩季年減。","ruling":"新設 Single Thing。選毛利額而不是毛利率，因為成本全額轉嫁時毛利率也會下滑，百分比會誇大傷害。","evidence_level":"中","settle_metric":"每季營收乘毛利率","if_then":["若發生，不建倉，已持有者減碼一半"],"evidence_refs":[]},{"axis":"共識上修是否真實","cause":null,"prior_field":null,"side_a":"資料顯示 FY1 共識近 3 個月上修 7.95%，由 8.8 升到 9.5。","side_b":"8 月的 8.8 較像 FY26 數字：10-17 的 FY26 共識為 9.04；前份進場價隱含 FY27 共識約 9.67（261 除以 27）。同口徑看 FY27 共識約下修 1.8%。","ruling":"採 B 側，把 7.95% 視為財年切換造成。性質：可調和，屬財年口徑差異。可能看錯的地方是前份隱含值與 Koyfin 來源不同，要有同財年歷史快照才能定案。","evidence_level":"中","settle_metric":"FY2027 共識 EPS 的同財年歷史快照","if_then":["若同財年資料證實 3 個月下修超過 3%，不追，Base EPS 再下修","若同財年資料證實上修至少 3%，仍不追，Base EPS 上調到共識"],"evidence_refs":[]},{"axis":"換機高峰或結構升級","cause":null,"prior_field":null,"side_a":"Wedbush 認為週期仍有動能；升級人數創紀錄；2026-07-30 法說 Cook 說資料看不出拉貨。","side_b":"另有報導認為創紀錄季度可能是週期高點；Counterpoint 預期 2027 年手機再減；iPhone 18 標準版未在九月推出，營收認列時點不易比較。","ruling":"不可裁決至 2027 年九月季財報。現有資料涵蓋不到高基期的比較窗，不能說風險已解。本次結論不靠裁決此事，兩種情況下現價都偏貴。","evidence_level":"低","settle_metric":"iPhone 營收對 FY26 高基期的年增率","if_then":["若 iPhone 營收連 2 季年減，減碼一半","若高基期下仍年增 10% 以上，仍不追，上調 Bull 機率"],"evidence_refs":["supply_demand_durability#3","supply_demand_durability#2"]},{"axis":"毛利率與毛利額","cause":null,"prior_field":null,"side_a":"毛利率下滑會被解讀為成本轉嫁失敗。","side_b":"成本全額轉嫁時毛利額不變，毛利率仍會因營收變大而下滑。","ruling":"採 B 側，致命指標用毛利額，毛利率作輔助。性質：可調和。","evidence_level":"高","settle_metric":"毛利額年增率","if_then":["若毛利率下滑但毛利額年增至少 5%，不減碼","若毛利額年減，減碼一半"],"evidence_refs":[]},{"axis":"營收共識的財年標籤","cause":null,"prior_field":null,"side_a":"事實表把 4,776.9 億美元標為與 FY1 EPS 同一財年。","side_b":"FY26 實績 4,788.3 億美元，兩者幾乎相等；十二月季指引年增 7%～10%，這筆不可能是 FY27。5,692.7 億美元才像 FY27，等於年增 18.9%。","ruling":"採 B 側，前瞻 EV/S 10.49 倍的分母很可能晚一年，不引用。本次採 EPS 路徑，不受影響。性質：可調和，屬資料標籤問題。","evidence_level":"中","settle_metric":"營收預估對應的財年","if_then":["若 FY27 共識確為 5,693 億美元，十二月季後其餘三季需年增約兩成以上，低於此節奏就不追"],"evidence_refs":[]},{"axis":"淨負債口徑","cause":null,"prior_field":null,"side_a":"事實表淨負債 377.6 億美元，總債務 944.8 億含租賃，現金 567.2 億。","side_b":"2026-11-02 法說 CFO Parekh：現金與有價證券 1,370 億、總債務 800 億，淨現金約 570 億。","ruling":"看償債能力採 B 側。差額約占企業價值 1.9%，情境樹走 EPS，不受影響。性質：可調和。","evidence_level":"高","settle_metric":"10-K 資產負債表","if_then":[],"evidence_refs":[]},{"axis":"Services 放緩的歸因","cause":null,"prior_field":null,"side_a":"2026-11-02 法說 CFO Parekh 主要歸因匯率：三月到九月季約 4 個百分點，十二月季再 0.5。","side_b":"同場十二月季指引把第三方授權列為主要逆風之一，App Store 九月季與去年相近，手遊疲弱延續，外部連結裁決仍在執行。2026-07-30 法說已提手遊疲弱。","ruling":"匯率歸因未證，持續監測。先登記期限：匯率逆風小於 1 個百分點的季度，Services 年增仍連 2 季低於 9%，匯率歸因就不成立。第三方授權的內容管理層未說明。","evidence_level":"中","settle_metric":"Services 年增率與 CFO 揭露的匯率影響","if_then":["若歸因不成立，下修 Base 的 Services 成長，不追","若匯率消退後回到 10% 以上，仍不追，H3 維持"],"evidence_refs":["channel_business_model_shift#1","regulatory_antitrust#2"]},{"axis":"供給限制的說法變化","cause":null,"prior_field":null,"side_a":"2026-07-30 法說 Cook 說九月季限制主因是系統晶片先進製程，並稱根因不是一般供給問題。","side_b":"2026-11-02 法說 Khan 說先進製程限制正在緩解，十二月季 Mac、iPad 受限主因轉為記憶體。Sankar 與 Mohan 問記憶體採購安排，只得到採購承諾增加 330 億美元的回答。","ruling":"限制已由晶片移到記憶體，問題由產能變成成本與可得性。是否簽長約、鎖價多少未回答，列為資料缺口。性質：可調和。","evidence_level":"中","settle_metric":"10-K 採購承諾、法說對記憶體成本的說法","if_then":["若採購承諾再季增至少 200 億美元且營收指引年增低於 5%，停止加碼"],"evidence_refs":["geo_supply_chain#2","supply_demand_durability#0"]},{"axis":"上季指引對帳","cause":null,"prior_field":null,"side_a":"2026-07-30 CFO Parekh 指引九月季營收年增 9%～11%、iPhone 中十位數、毛利率 47%～48%、營業費用 191～194 億美元。","side_b":"實績為年增 12%、iPhone 年增 17%、毛利率 47.9%、營業費用 192 億美元。","ruling":"管理層指引偏保守，這是看多的真實證據，所以 Base 的 FY27 EPS 只比共識低約 2%，不放更低。","evidence_level":"高","settle_metric":"十二月季實績對指引","if_then":["若十二月季毛利率高於 46%，仍不追，上調 Base EPS"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"裝置超過 25 億台，份額在最差的市場裡擴大，大中華區全年年增 28%，Duo 供不應求；AI 對手燒錢而 Apple FCF 利潤率 28.4%。優質資產少有便宜價，等 257 美元可能等不到。","side_b":"現價要賺 8%，EPS 五年要年增 15.7%（27 倍）或 11.8%（32 倍），共識只有 9.6%；十二月季毛利率指引還低於九月季。","ruling":"採 B 側，不追。等不到的機會成本是真實的，所以保留上移條件：毛利額連 4 季年增至少 8% 且 FY28 共識 EPS 至少 11.5 時重跑情境樹，價格門檻隨 EPS 上移。","evidence_level":"中","settle_metric":"毛利額年增率、FY28 共識 EPS","if_then":["若股價續漲而毛利額證據未到，不追","若股價下跌但基本面無損且條件成立，分批反買"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭面轉好：IDC 8 月預測 Android 年減 20%、iOS 年減 5.2%，Apple 份額擴大。對手仍可接近零利潤銷售。","side_b":"其他結構變數惡化：DOJ 與 DMA 切割 Services，AI 入口未定，記憶體價值鏈移轉。","ruling":"雙向拉鋸。競爭面結構性轉好，法規與價值鏈分配變差。","evidence_level":"中","settle_metric":"手機份額、Services 年增率","if_then":[],"evidence_refs":["competitive_share_entrants#1","regulatory_antitrust#1"]}],"triggers":[{"n":1,"text":"毛利額連兩季年減","type":"Single Thing","maps_to":"H2","metric":"公司毛利額年增率（剔關稅退款）","threshold":"連 2 季低於 0%","action":"不建倉；已持有者減碼一半","source_freq":"每季 8-K","date":"2027-01","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1"]},{"n":2,"text":"估值與毛利率同時達標才重新研究","type":"估值rearm","maps_to":"估值","metric":"FY27 共識前瞻本益比與公司毛利率","threshold":"≤ 27 倍（約 $257）且毛利率連 2 季 ≥ 45%","action":"重跑研究，通過後小倉分批反買","source_freq":"每日股價、每季財報","date":null,"evidence_refs":[]},{"n":3,"text":"FY27 營收檢查","type":"假設驗證","maps_to":"H1","metric":"FY27 營收年增率","threshold":"低於 10%","action":"下修 Base 營收，不追","source_freq":"每季 8-K","date":"2027-11","evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"Services 成長跌破底線","type":"風險","maps_to":"R2","metric":"Services 年增率","threshold":"連 2 季低於 7%","action":"減碼一半，未持有則不追","source_freq":"每季 8-K","date":"2027-01","evidence_refs":["channel_business_model_shift#1"]},{"n":5,"text":"監管或司法出現不利定案","type":"風險","maps_to":"R2","metric":"最高法院外部連結裁決、Google 上訴、DMA 第 6(4) 條認定","threshold":"任一項不利，且 Google 商業條件被禁或公司揭露 Services 受重大影響","action":"減碼一半","source_freq":"事件驅動","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#2","lawsuit_class_action#1"]},{"n":6,"text":"AI 入口開始侵蝕平台","type":"風險","maps_to":"R3","metric":"App Store 年增方向與付費訂閱數","threshold":"App Store 連 2 季年減，或付費訂閱低於 15 億","action":"減碼一半","source_freq":"每季法說","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"n":7,"text":"採購承諾放大而需求轉弱","type":"風險","maps_to":"R1","metric":"製造採購承諾季增額與下季營收指引","threshold":"再季增至少 200 億美元且指引年增低於 5%","action":"停止加碼","source_freq":"每季 10-Q、法說","date":"2027-01","evidence_refs":["supply_demand_durability#4"]},{"n":8,"text":"毛利額持續衰退","type":"清倉","maps_to":"R1","metric":"毛利額年增率與 FY28 共識 EPS","threshold":"毛利額連 4 季年減且 FY28 共識 EPS 低於 9.5","action":"清倉","source_freq":"每季 8-K、共識快照","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":9,"text":"供應鏈或關稅吸收失敗","type":"風險","maps_to":"R4","metric":"營收指引年增率與公司毛利率","threshold":"指引連 2 季低於 5%，或新關稅使毛利率連 2 季低於 44%","action":"減碼一半","source_freq":"每季法說","date":null,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"n":10,"text":"手機份額回吐","type":"風險","maps_to":"R5","metric":"第三季全球手機份額","threshold":"低於 20%","action":"減碼一半，未持有則不追","source_freq":"Counterpoint、IDC 每季","date":"2027-10","evidence_refs":["competitive_share_entrants#1"]},{"n":11,"text":"證券集體訴訟進入不利階段","type":"風險","maps_to":"R6","metric":"Siri AI 與 Epic 合規集體訴訟程序","threshold":"集體認證通過且出現不利和解；刑事介入則清倉","action":"減碼至半倉","source_freq":"事件驅動","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":12,"text":"十二月季財報後複審","type":"複審日期","maps_to":"H2","metric":"十二月季毛利額與毛利率","threshold":"毛利率是否落在 45%～46%","action":"更新情境路徑","source_freq":"每季 8-K","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"公司毛利額年增率（剔關稅退款）","bear_threshold":"連 2 季低於 0%","window":"FY27 各季","source":"每季 8-K 營收與毛利率","last_status":"unknown"},{"metric":"公司毛利率","bear_threshold":"連 2 季低於 44%","window":"FY27 至 FY28","source":"每季 8-K","last_status":"warning"},{"metric":"Services 年增率","bear_threshold":"連 2 季低於 7%","window":"FY27 至 FY28","source":"每季 8-K","last_status":"ok"},{"metric":"第三季全球手機份額","bear_threshold":"低於 20%","window":"2027 年第三季","source":"Counterpoint、IDC","last_status":"ok"},{"metric":"FY27 共識 EPS","bear_threshold":"低於 9.0","window":"未來 12 個月","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"FY27 共識前瞻本益比 ≤ 27 倍（約 $257）且公司毛利率連 2 季 ≥ 45%，兩項同時成立才重跑研究","exec_line":"不追，現價 342.37 美元不建首倉。條件成立後重跑研究，首筆只用小倉。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場同時相信 FY27 營收年增約 19% 和 36 倍本益比；十二月季指引只有 7%～10%、毛利率還在降，五年要賺 8% 需要 EPS 年增約 16%。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 FY27 共識前瞻本益比回到 27 倍（約 $257）以下，且公司毛利率連 2 季 ≥ 45%。"},"thesis":{"H":[{"id":"H1","text":"iPhone 與 Mac 在記憶體短缺時搶到份額，FY27 營收能靠單價與新機組合再成長兩位數。","2y":"FY27 營收年增至少 10%，2027 年第三季全球手機份額至少 20%","5y":null,"10y":null,"threshold":"FY27 營收至少 5,267 億美元；2027 年第三季份額至少 20%","source":"每季財報與 10-Q；Counterpoint、IDC 季度出貨","drift_rule":"TTM 營收偏離路徑連 2 季達 5% 算削弱，連 3 季達 10% 算反轉"},{"id":"H2","text":"漲價與產品組合補得回記憶體成本：毛利率會下滑，但毛利額繼續成長。","2y":"FY27 毛利額年增至少 3%，單季毛利率不連兩季低於 44%","5y":null,"10y":null,"threshold":"FY27 毛利額至少 2,406 億美元；公司毛利率至少 44%","source":"每季 8-K 營收與毛利率；法說對記憶體與結轉庫存的說明","drift_rule":"TTM 毛利額偏離路徑連 2 季達 5% 算削弱，連 3 季達 10% 算反轉"},{"id":"H3","text":"Services 撐過監管與授權壓力，FY28 回到雙位數成長並守住高毛利。","2y":null,"5y":"FY28～FY31 年增至少 10%，毛利率至少 75%","10y":null,"threshold":"FY28 Services 年增至少 10%，毛利率至少 75%","source":"每季 8-K；最高法院、歐盟執委會、Google 案進度","drift_rule":"自十二月季指引起算，連 4 季偏離 5% 算削弱，連 6 季偏離 10% 算反轉"},{"id":"H4","text":"AI 時代 iPhone 仍是個人脈絡的主要入口。","2y":null,"5y":null,"10y":"活躍裝置與付費帳戶持續創高，App Store 維持年增","threshold":"活躍裝置至少 25 億台且持續成長；付費訂閱至少 15 億","source":"每季法說揭露的活躍裝置、付費帳戶、App Store 說法","drift_rule":"跨 2 個年度未創高算削弱，跨 3 個年度算反轉"}],"R":[{"id":"R1","text":"記憶體高價延續，結轉庫存效益遞減，漲價補不回成本；2026-11-02 法說 Ternus 說十二月季之後採購價仍在上升。","h_ref":"H2","clock":"🔥","threshold":"公司毛利率連 2 季低於 44%，或毛利額連 2 季年減","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","supply_demand_durability#4"]},{"id":"R2","text":"Services 被監管與司法切割，受影響基礎為九月季 315.73 億美元的 Services 營收，App Store 占比未揭露；DOJ 屬民事訴訟，定案時間事實表未涵蓋。","h_ref":"H3","clock":"🔥","threshold":"Services 年增連 2 季低於 7%，或毛利率低於 73%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","channel_business_model_shift#1","major_events#2","lawsuit_class_action#1"]},{"id":"R3","text":"Agent 形態繞過 App 與 Safari 入口，或新型 AI 裝置成為新入口。2026-07-30 法說 Ternus 未正面回應 OpenAI 裝置與 SpaceX AI 手機。","h_ref":"H4","clock":"🐢","threshold":"App Store 連 2 季年減，或付費訂閱低於 15 億","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"id":"R4","text":"系統晶片單一供應、製造集中亞洲，地緣或貿易事件直接限制出貨與毛利。","h_ref":"H1","clock":"⚡","threshold":"營收指引連 2 季年增低於 5%，或新關稅使毛利率連 2 季低於 44%","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R5","text":"FY26 是換機高點，漲價後需求轉弱，對手以低價奪回份額。","h_ref":"H1","clock":"🔥","threshold":"iPhone 營收連 2 季年減，或第三季全球份額低於 20%","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#3"]},{"id":"R6","text":"CEO 交接與訴訟風險同時存在：2026-07-30 法說 Cook 宣布交棒，Ternus 2026-11-02 首次主持；Siri AI 與 Epic 合規的證券集體訴訟未有駁回裁定。","h_ref":"H4","clock":"🔥","threshold":"駁回聲請遭否且集體認證通過；或 CFO、COO 於 12 個月內異動","evidence_refs":["major_events#1","lawsuit_class_action#0"]}],"single_thing":{"description":"剔除關稅退款後，公司毛利額連續兩季年減。","why_fatal":"FY27 共識 EPS 9.5 在費用年增 12%、稅率 17%、平均股數約 144 億下，需要毛利額約 2,480 億美元，較 FY26 的 2,336 億多約 6%。毛利率每 1 個百分點約等於 0.27 美元 EPS，約占 FY27 共識 2.9%，是模型裡最大的單一敏感項。毛利額年減代表漲價沒有補回記憶體成本，EPS 成長與高倍數同時失去依據。","if_happens":"不建首倉，Bear 機率由 30% 上調到至少 40%，Base FY27 EPS 下修到 9.0 以下；已持有者減碼一半。","how_monitor":"每季 8-K 的營收乘毛利率，扣掉法說揭露的關稅退款；同時看法說對記憶體採購價與結轉庫存的說法。","probability":"約 25%（12～24 個月）。管理層已說記憶體續漲且結轉庫存效益遞減，但漲價剛開始反映，Android 缺料也有利於份額。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":32.15,"peg_fy2":3.35,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":8.98,"FY2027E":9.5,"FY2028E":10.65,"FY2029E":11.82},"fy_end_month":9,"eps_basis":"GAAP 稀釋 EPS；FY2026A 含關稅退款，九月季 0.05 美元；FY2027E 起為 Koyfin 共識 FY1～FY3"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"十二月季財報與三月季指引","impact":"高","watch":"毛利額年增率、毛利率是否落在 45%～46%、記憶體結轉庫存說法；實際日期待公司公告"},{"date":"2027-06","date_precision":"quarter","type":"macro","event":"IDC 預期記憶體價格 2027 年中趨穩","impact":"高","watch":"公司毛利率指引是否止跌"},{"date":null,"date_precision":null,"type":"regulatory","event":"最高法院審理外部連結裁決上訴","impact":"高","watch":"App Store 抽成能否恢復；開庭與判決日事實表未涵蓋"},{"date":null,"date_precision":null,"type":"regulatory","event":"歐盟 DMA 第 6(4) 條最終認定","impact":"中","watch":"罰款金額與互通性義務"},{"date":null,"date_precision":null,"type":"product","event":"Siri AI 伺服器用量超額付費上線","impact":"中","watch":"定價與 iCloud+ 附著率"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場同時相信 FY27 營收年增約 19% 和 36 倍本益比；十二月季指引只有 7%～10%、毛利率還在降，五年要賺 8% 需要 EPS 年增約 16%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🔴', moat_trend='→', week26=16.93, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
