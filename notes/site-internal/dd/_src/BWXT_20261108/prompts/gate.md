你是 DD 管線 v20 的判斷層閘（gate），標的 BWXT（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝953.0 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-02））
  - 註記：未查證（僅二手 Quiver 稱略低於共識，未採）
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益＝149.7 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-02））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝132.1 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-02））
- `f_kpi6_backlog`（q1_business）｜Backlog＝8556.2 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-02））
- `f_kpi7_book_to_bill`（q1_business）｜Book-to-bill（自算＝訂單÷營收，非公司揭露）＝0.56 x｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-02））
- `f_peer_bwxt_gross_margin_pct`（q2_moat）｜BWXT 毛利率＝22.61 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWXT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_bwxt_operating_margin_pct`（q2_moat）｜BWXT 營業利益率＝9.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWXT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lmt_gross_margin_pct`（q2_moat）｜LMT 毛利率＝11.73 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LMT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rtx_gross_margin_pct`（q2_moat）｜RTX 毛利率＝21.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RTX.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_noc_gross_margin_pct`（q2_moat）｜NOC 毛利率＝20.02 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gd_gross_margin_pct`（q2_moat）｜GD 毛利率＝15.42 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GD.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lmt_operating_margin_pct`（q2_moat）｜LMT 營業利益率＝11.78 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LMT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rtx_operating_margin_pct`（q2_moat）｜RTX 營業利益率＝11.77 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RTX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_noc_operating_margin_pct`（q2_moat）｜NOC 營業利益率＝10.61 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gd_operating_margin_pct`（q2_moat）｜GD 營業利益率＝10.37 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GD.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝4.75 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝5.17 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝5.86 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝3795.92 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝4097.34 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝150.5 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-02））
- `f_kpi4_sbc`（q4_capital）｜SBC（九個月累計，季度未單獨揭露）＝29.9 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 http://investors.bwxt.com/3Q2026-release（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-02））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1453.35 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 2021.88、現金 568.53（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝119.52 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝25.16 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 4.75，分子＝快照價 119.52｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝29.37 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝26.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝26.9 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.21 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 4.74 → 4.75（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-0.51 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（5.89 → 5.86）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.887 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-41.62 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 119.52 / W52 182.05 / W104 158.59 / W250 107.29 / W250 13週斜率 1.25%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝107.29 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_rsi14`（q5_valuation）｜RSI(14)＝34.91｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝12404.39 USD m｜期間與口徑：2026-11-08／市值 10951.04 ＋ 淨負債 1453.35｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null

### findings_digest 中方向為負或來源衝突的條目（7 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：無法保證現有技術維持競爭力或不被競爭技術顛覆。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-23）｜affects：decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：美國政府占 FY2025 合併營收約 68%（FY2024 76%、FY2023 75%）；無單一非政府客戶超過 10%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-23）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：加拿大競爭局調查 BWXT 以 5.25 億美元收購 Kinectrics 是否實質減損加拿大核醫學領域競爭；2025-11 聯邦法院核准擴大調查令，納入 Novartis 及其子公司。搜尋未見 2026 年結案或挑戰的消息；未見美國 DOJ/FTC 或歐盟行動。
  - 來源：Law360 Canada: Competition Bureau seeks Novartis data in BWX–Kinectrics merger probe（搜尋摘要）（as_of 2025-11-01）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2025 年報：行政命令 EO 14372 可能限制關鍵國防承包商發放股息、買回庫藏股、調薪及激勵指標，預期以新 DFARS 條款實施。
  - 來源：BWXT FY2025 Annual Report to Shareholders (ARS)（as_of 2026-03-01）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：BWXT 10-K 風險因素揭露：在加拿大有重型核能組件與醫用同位素製造，產品可能售予美國客戶，新增或提高關稅會推升產品、零組件與原料成本、壓縮毛利；最終影響取決於關稅實施與否、時點、合約條款與範圍。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-23）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：BWXT 10-K 風險因素自述：無法保證現有技術維持競爭力，也無法保證競爭技術不會衝擊業務；醫用同位素領域可能出現替代技術的競爭者，且可能更早商業化或有成本優勢。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-23）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：搜尋摘要：TRISO 燃料供應商少，X-energy 旗下 TRISO-X 為最接近的競爭者，Oak Ridge TX-1 於 2026-02-13 取得 NRC 許可；DOE 2025-09 同時有條件選定 TRISO-X 與 Valar Atomics 進入燃料產線試點。
  - 來源：Sacra 分析（搜尋摘要）（as_of 2026-02-13）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 12 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":294.0,"bear_5y_price":87.6,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":53.9,"ev5y_pct":48.1,"irr_base_pct":9.0,"asym_ratio":3.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":4.75,"pe":25.16,"basis":"FY2026E 共識 EPS，現價 119.52 美元除以 FY1，與終端倍數同為當年度前瞻口徑"},"eps":{"bull":[5.35,6.3,7.5,8.9,10.5],"base":[5.15,5.8,6.5,7.25,8.0],"bear":[4.95,5.0,5.05,5.1,5.15]},"pe":{"bull":28,"base":23,"bear":17},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.887,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BWXT_Q2_2026_Earnings_Call_20260803.md
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：全年自由現金流財測上調 $30M，區間 $345M–$360M（原話："to a range of $345 million to $360 million"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：全年調整後 EBITDA 財測中點上調 $10M，區間 $662M–$672M（原話："adjusted EBITDA guidance by $10 million at the midpoint"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：全年營收財測約 $3.8B，高十位數成長（原話："We now expect revenue of approximately $3.8 billion"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：政府業務營收成長財測由低十位數下修為高個位數（原話："our previous expectation of low teens growth."）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：管理層說明政府業務營收下修原因：成本表現較佳，依會計規則使認列營收較低，但經濟結果有利（原話："lower reported revenue, but an overall favorable"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：政府業務調整後 EBITDA 利潤率財測上調至約 20.5%（原為 >19%）（原話："adjusted EBITDA margin guidance to approximately 20.5% from"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：商業業務營收成長財測上調至約 45%（原約 30%）（原話："revenue growth outlook to approximately 45% from"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：商業業務 EBITDA 利潤率財測約 13%（原約 14%）（原話："adjusted EBITDA margin of approximately 13%"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：商業業務利潤率下修原因為美國產能擴張（含 PCG）與加拿大持續投資（原話："The revision reflects incremental investments in U.S."）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：2026 非 GAAP EPS 財測 $4.70–$4.80，上調全由營運獲利推動（原話："of $4.70 to $4.80. The increase from our prior guidance is"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：下半年獲利約 55% 落在第四季（原話："we expect approximately 55% of second half earnings to be"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：管理層建模口徑：出售的醫療業務 2026 年化營收約 $130M，利潤率略高於商業部門平均（原話："modestly accretive to the Commercial segment average"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：出售後保留的少數股權將以權益法收益認列、無相關營收（原話："retained minority interest through equity income"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：Q2 調整後 EBITDA 數字口徑：逐字稿本身標註 $156M 為誤，應為 $155M（原話："$156 million (sic) [ $155 million ]"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：Q2 政府業務調整後 EBITDA 利潤率 20.9%（原話："resulting in an adjusted EBITDA margin of 20.9%"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：Q2 商業業務利潤率 11.9%，量增與執行抵銷擴產投資（原話："quarter was 11.9% as higher volume and strong execution"）
- 2026-08-03｜CEO Rex Geveden｜margin：CEO 表示投資將使近期利潤率擴張趨緩（原話："will moderate near-term margin expansion"）
- 2026-08-03｜CFO Michael Fitzgerald｜margin：政府業務仍在消化舊定價安排的在手訂單（原話："working off backlog associated with older pricing"）
- 2026-08-03｜CFO Michael Fitzgerald｜commitment：CFO 預期舊定價在手訂單於 2026 年底前消化完畢（原話："that to be done by the end of '26."）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：CFO 表示目前不設定 2027 年財測（原話："I'm not setting '27 guidance at this point."）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：CFO 預期 2027 年商業業務利潤率將有較明顯提升（原話："as we go into '27, we'll see more of a"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：全年資本支出約占營收 6%，下半年美國商業產能投資增加（原話："of approximately 6% of sales with increased investment"）
- 2026-08-03｜CFO Michael Fitzgerald｜guidance：未來幾年資本支出可能接近營收 7%（原話："capital expenditures could approach 7% of sales in future"）
- 2026-08-03｜CEO Rex Geveden｜commitment：CEO 稱至少有一張新建核電設備訂單有機會在年底前取得（原話："opportunity to secure at least one new build nuclear"）
- 2026-08-03｜CEO Rex Geveden｜commitment：CEO 稱預期未來數月內對美國商業製造擴產做出最終投資決定（原話："we expect to reach a final investment decision in the coming"）
- 2026-08-03｜CEO Rex Geveden｜commitment：CEO 稱擴產目前只剩選址（紐澤西、印第安納與另一處）待定，且很快決定（原話："just a matter of site selection at this point"）
- 2026-08-03｜CEO Rex Geveden｜commitment：CEO 預告 9 月投資人日（原話："our upcoming Investor Day in September"）
- 2026-08-03｜CEO Rex Geveden｜capital_allocation：宣布以最高 $800M 估值出售醫療業務給 Nordic Capital（敘事變化：聚焦核心）（原話："sale of our medical business to Nordic Capital"）
- 2026-08-03｜CEO Rex Geveden｜capital_allocation：CEO 稱該資產原本並未待售，是買方主動接洽（原話："that asset wasn't for sale"）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：交易對價 $750M，另有共享經濟機制可達 $800M（原話："the deal includes $750 million of consideration"）
- 2026-08-03｜CEO Rex Geveden｜capital_allocation：BWXT 保留醫療資產 20% 股權（原話："we will maintain a 20% equity stake in"）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：出售所得用途尚未確定；優先順序為內部投資（資本支出 6–7%）、併購、還債（原話："So not exactly."）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：CFO 稱併購管線很充足，但篩選嚴格（原話："we have a very robust M&A pipeline"）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：2026 年無計畫中的庫藏股買回（原話："we don't have any planned repurchases"）
- 2026-08-03｜CEO Rex Geveden｜capital_allocation：TRISO 商業設施資本支出規模為數億美元至最高 $500M，與夥伴分攤並有懷俄明州補助（原話："a few hundred million dollars, up to $500 million."）
- 2026-08-03｜CFO Michael Fitzgerald｜capital_allocation：CFO 稱 Janus 決標是 TRISO 投資決定的關鍵里程碑，預期今年授標（原話："expecting an award this year"）
- 2026-08-03｜CEO Rex Geveden｜risk：CEO 稱 TRISO 需求仍高度不確定，尚未準備好全面資本承諾（原話："we're not yet ready to make a full capital commitment on it"）
- 2026-08-03｜CEO Rex Geveden｜risk：CEO 解釋 AP1000 尚無確定訂單：公用事業在觀望政府主權交易結果（原話："the utilities are sort of rightly waiting to see how"）
- 2026-08-03｜CEO Rex Geveden｜risk：濃縮業務自製供應鏈須使用美國來源（無義務）設備，CEO 稱存在商業可行性疑問（原話："there's a question about the commercial viability of"）
- 2026-08-03｜CEO Rex Geveden｜risk：供應鏈目前無問題，原料（鋯管、大型鍛件）取得順利（原話："zirconium tubes, large forgings, whatever we need"）
- 2026-08-03｜CEO Rex Geveden｜risk：勞動力整體可控，加拿大鋼鐵工人略缺（原話："challenges finding steel workers in Canada right now"）
- 2026-08-03｜CEO Rex Geveden｜customer：期末在手訂單 $8.4B（原話："We ended the quarter with backlog of $8.4 billion"）
- 2026-08-03｜CEO Rex Geveden｜customer：在手訂單較上季略減，管理層歸因於大型多年期合約的授標時點（原話："Although backlog was modestly lower than last quarter"）
- 2026-08-03｜CEO Rex Geveden｜customer：近 12 個月 book-to-bill 為 1.7x（原話："our book-to-bill is a robust 1.7x"）
- 2026-08-03｜CEO Rex Geveden｜customer：海軍新造艦計畫將福特級航艦採購節奏加快為 4 年（原話："Ford-class aircraft carriers to a 4-year procurement"）
- 2026-08-03｜CEO Rex Geveden｜customer：CEO 稱福特級 4 年節奏對業務的量體影響比核動力戰艦更大（原話："actually more important to our business."）
- 2026-08-03｜CEO Rex Geveden｜customer：核動力戰艦長交期採購預期 2028 年開始進入 BWXT 工廠（原話："long lead procurements would begin in '28 as we"）
- 2026-08-03｜CEO Rex Geveden｜customer：加拿大核能策略：聯邦支持至 2040 年最多 10 座大型反應爐（原話："federal support for up to 10 large reactors by 2040"）
- 2026-08-03｜CEO Rex Geveden｜customer：加拿大大型反應爐對 BWXT 營收的影響預期落在 2030 年代初（原話："very positive way in the early 2030s."）
- 2026-08-03｜CEO Rex Geveden｜customer：DOE 宣布 $17.5B 貸款承諾，支持 AP1000 長交期設備採購（原話："$17.5 billion loan commitment"）
- 2026-08-03｜CEO Rex Geveden｜customer：CEO 預期下半年會拿到一張訂單，來源涵蓋 SMR、AP1000、X300 等（原話："second half order among the opportunities"）
- 2026-08-03｜CEO Rex Geveden｜product：濃縮專案：離心機原型機預計今年交付，進度符合時程（原話："on schedule to deliver an operational prototype centrifuge"）
- 2026-08-03｜CEO Rex Geveden｜product：高純度貧鈾（HPDU）新廠預期下半年對政府業務營收有顯著貢獻（原話："This program should contribute meaningfully to"）
- 2026-08-03｜CEO Rex Geveden｜product：mPower 授權：BWXT 保留製造權、權利金權與智慧財產（原話："exclusive manufacturing rights, royalty rights"）
- 2026-08-03｜CEO Rex Geveden｜product：CEO 稱無意自行將 mPower 推向市場，仍維持 merchant supplier 定位（原話："it's not our intention to bring"）
- 2026-08-03｜CEO Rex Geveden｜product：CEO 稱 mPower 授權等於將自家 IP 變現（原話："monetizing our IP"）
- 2026-08-03｜CEO Rex Geveden｜product：PCG 整合與產能納入需時，預期未來數季逐步展開（原話："will unfold over the next few quarters"）
- 2026-08-03｜CEO Rex Geveden｜competition：CEO 自述在供應鏈廠商中居於頂端，擁有北美最大元件製造廠（原話："we sit right at the top"）
- 2026-08-03｜CEO Rex Geveden｜competition：CEO 稱產能與能力上全球無人更佳（原話："I don't think there's any one better on the globe."）
- 2026-08-03｜CEO Rex Geveden｜competition：CEO 說明 PCG 無法生產最大型元件（如 AP1000 反應爐壓力容器）（原話："PCG is not capable of producing the largest components"）
- 2026-08-03｜CEO Rex Geveden｜competition：CEO 稱海軍核反應爐業務讓 BWXT 擁有競爭對手沒有的天然優勢（原話："natural advantages that our competitors did not"）

### BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2030 年營收目標 55~60 億美元（較 2026 年低雙位數年增）（原話："we're targeting $5.5 billion to $6 billion in 2030"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2030 年調整後 EBITDA 目標 11~12 億美元（原話："we're targeting $1.1 billion to $1.2 billion"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2030 年自由現金流目標 5.25~5.75 億美元（原話："targeting free cash flow of $525 million to $575 million"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：調整後 EBITDA 利潤率由 2026 年 17.5% 走向 2030 年約 20%（原話："approximately 20% by 2030"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：CFO 說明 20% 目標不假設產品組合變好，靠執行、生產力、價值捕捉與規模（原話："20% doesn't assume that mix is going to be more favorable"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：CFO 拆解利潤率改善空間約 300 個基點（營運卓越、定價、規模）（原話："This represents about 300 basis points of opportunity"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：CFO 說明政府部門近年利潤率小幅受壓，原因為產品組合（原話："primarily been driven by mix"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年初步框架：營收高個位數成長（原話："calls for high single-digit revenue growth"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年政府部門特殊材料預期強勁雙位數成長（原話："robust double-digit special materials growth"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年政府部門利潤率預期持平至小幅上升（原話："We expect government margins to be flat to modestly higher"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年商業部門有機成長高個位數（原話："we expect high single-digit organic growth in 2027"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年商業部門報告營收成長低個位數（PCG 併入、醫療出售互抵）（原話："expected to be low single digits"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 年商業部門利潤率預期擴張 50~100 基點（原話："commercial margins to expand 50 to 100 basis points"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：重申 2026 年財測（原話："we are reaffirming our 2026 guidance"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2026 年自由現金流指引 3.45~3.6 億美元（原話："$345 million to $360 million based on our current guidance"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2027 框架假設醫療事業 2026 年底完成出售（原話："we're assuming that Medical closes at the end of 2026"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜guidance：商業部門 2030 年前營收年複合成長高十位數百分比（原話："high teens revenue CAGR over the period to 2030"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜margin：商業部門 EBITDA 利潤率由約 13% 到 2030 年高十位數（原話："go from about 13% now into the high teens by 2030"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜guidance：政府部門 2030 年營收中至高個位數年複合成長（相較現在）（原話："mid- to high single-digit CAGR as compared to today"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜margin：政府部門 2026 年利潤率由年初 19% 升至約 20.5%（原話："raise that margin above 20% to about 20.5%"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜guidance：海軍核動力 4%~6% 年複合成長（原話："So all in all, 4% to 6% CAGR growth over this time period."）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜guidance：戰艦核心未列入預測，因海軍尚未承諾採購（原話："This isn't in our forecast"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜risk：CFO：戰艦未納入 2030 預測，仍須撥款與其他關卡（原話："has to go through appropriations and a number of hurdles"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：福特級航母採購節奏已加快並納入預測，影響約在 2030 前後（原話："that did accelerate, and we have incorporated that"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：海軍核反應爐不按艘報價，因固定成本大、依總艘數定價（原話："we don't sell specific price per reactor"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：$45 億積壓訂單預計轉為營收（2027 年底前）（原話："$4.5 billion of our backlog is expected to convert"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：接單出貨比近 12 個月（至第二季）1.7 倍（原話："we're 1.7x on a trailing 12-month basis"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：營收成長中約一半多來自既有核心（原話："That represents a little over half of the growth forecast"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜commitment：CFO：成長路徑非直線，單一年度節奏可能不同（原話："I would not expect this to happen in a growth"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜commitment：CFO：不需贏下所有機會就能達標（原話："we don't need to win every opportunity discussed"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：CFO：新商業核電建設拐點在 2028、2029（原話："you're going to see that inflection in '28 and '29"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜guidance：商業大型機組訂單轉換時點：今年稍晚或 2027 年初（原話："either later this year or early in 2027"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：每座 CANDU 反應爐可觸及營收 3.5~7 億美元（原話："between $350 million and $700 million per reactor of revenue"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：每座 SMR 可觸及營收約 5000 萬至 1 億美元（原話："about $50 million to $100 million per reactor"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：加拿大國家核能策略：10 座大型機組目標（原話："deploy 10 large reactors, 2 under construction by 2035"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：預期加拿大新大型機組帶來零組件訂單於本十年結束前（原話："orders for components before the end of this decade"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：Westinghouse 正在對 BWXT 做零組件資格認證（原話："working through qualifying us for all of the components"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜customer：Bruce C 與 Wesleyville 預計新機組數量（原話："probably 8 reactors at that site"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜product：蒸汽產生器產能由每月 1 台提升至 1.5 台以上（原話："operating at a pace of over 1.5 steam generators a month"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜product：服務營收由 2020 年約 7000 萬增至今年逾 6 億美元（原話："to more than $600 million this year"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜competition：BWXT 自稱技術中立的 merchant supplier（原話："we're technology agnostic"）
- 2026-09-29｜Rex Geveden (CEO)｜competition：CEO 稱 TRISO 競爭對手雜音多但出貨量小（原話："noisy competitors that are delivering very modest amounts"）
- 2026-09-29｜Rex Geveden (CEO)｜competition：CEO 指出無鈾濃縮的商業端有天然競爭劣勢（Urenco 等）（原話："a natural competitive disadvantage to that capability"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：特殊材料成長 24% 年複合，持續到 2030（原話："large growth, 24% CAGR"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：田納西州 Jonesborough 的 HPDU 設施規劃產能上限 300 公噸（原話："manufacture up to 300 metric tons of high-purity depleted"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜customer：去年 9 月取得 15 億美元濃縮鈾合約（原話："awarded the contract in September of last year for $1.5"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜capital_allocation：國防燃料設施初期投資後由政府出資（原話："Beyond that, it's been a government investment."）
- 2026-09-29｜Rex Geveden (CEO)｜customer：CEO：有機會贏下高豐度低濃縮鈾的大部分甚至全部（原話："a chance to win a good chunk of that, if not all of it"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：mPower 授權給 Applied Atomics 與 CORE POWER，BWXT 保留 IP 與製造權（原話："We have licensed them this technology."）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：微反應爐 BANR 由 BWXT 自己設計並製造整座反應爐（原話："manufacture not just the fuel, but the entire reactor"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜customer：Kairos 為 TRISO 的大型需求訊號，有 Google 支持（原話："Kairos has a big demand signal for TRISO in the near future"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：TRISO 擴產資本已含在 CapEx 目標內（原話："TRISO expansion capital within those targets"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：尚未決定 TRISO 新建全新廠房，需看 HALEU 供應（原話："we have not made a decision on a new greenfield facility"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜risk：俄羅斯鈾進口禁令即將生效（原話："an impending ban on import of Russian uranium"）
- 2026-09-29｜Rex Geveden (CEO)｜risk：CEO：核能與造艦的政治支持跨黨派，選舉結果不太影響（原話："the support for nuclear has endured"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜commitment：CFO：維持股利並持續增加，回購保留為選項（原話："maintain a consistent and growing dividend"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：CFO：沒有足夠再投資機會時將把多餘資本還給股東（原話："we will return incremental capital to shareholders"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：到 2030 年可動用資本約 55 億美元（淨槓桿 2~3 倍）（原話："$5.5 billion of available capital to deploy through 2030"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：扣除 CapEx、股利後仍有約 35 億美元額外部署能力（原話："approximately $3.5 billion of additional capital"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：淨槓桿目標區間 2~3 倍（原話："net leverage within our targeted 2 to 3x range"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：Fitch 給予投資等級評等（原話："Fitch had assigned us an investment-grade rating"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：去年 11 月發行 12.5 億美元零息可轉債（原話："we issued $1.25 billion of convertible notes at a 0% coupon"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：CapEx 目標占營收 5%~6%（原話："we are targeting CapEx at 5% to 6% of revenue"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：維護性資本支出占營收 3.5%~4%（成長性另 1.5%~2%）（原話："3.5% to 4% for maintenance capital"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2026~2030 累計自由現金流超過 20 億美元（原話："over $2 billion of cumulative free cash flow"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：2030 前自由現金流低雙位數成長（原話："we're targeting low double-digit free cash flow growth"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜margin：CFO：自由現金流過去高成長來自低基期，不假設持續（原話："not assuming that, that's going to continue indefinitely"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：併購門檻：NPV 為正含可達成綜效（原話："We expect positive NPV, including achievable synergies"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：併購要求第一年 EPS 增益（排除一次性攤銷與整合成本）（原話："We target EPS accretion in year 1"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：CFO：併購規模不再受限於過去交易大小（原話："we're not anchored to the same size of transactions"）
- 2026-09-29｜Rik Geiersbach (Chief Strategy Officer)｜capital_allocation：策略長：併購範圍含小型補強、中型與可能的轉型型交易（原話："some potentially more transformative plays"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜capital_allocation：CFO：2030 目標不依賴併購（原話："not beholden to M&A in order to hit our growth outlook"）
- 2026-09-29｜Rex Geveden (CEO)｜capital_allocation：出售多數醫療事業，保留約 20% 權益（原話："We are keeping 20% of that business"）
- 2026-09-29｜Michael Fitzgerald (CFO)｜guidance：相較前次投資人日改為提供 2030 年具體目標而非 3~5 年成長率（原話："provide specific 2030 targets for revenue"）
- 2026-09-29｜Rex Geveden (CEO)｜guidance：CEO 說明 2024 年以來營收複合成長 15%，其中有機 8.5%（原話："a 15% revenue CAGR, of which 8.5% is organic"）
- 2026-09-29｜Rex Geveden (CEO)｜margin：CEO：新業務造成利潤率逆風，先不對利潤率達標下定論（原話："new businesses that have created some margin headwinds"）
- 2026-09-29｜Rex Geveden (CEO)｜margin：CEO：利潤率目標先不明確承諾（原話："we won't stick a spear in the ground on that one just yet"）
- 2026-09-29｜John MacQuarrie (President, Commercial Operations)｜guidance：商業部門 EBITDA 2030 前年複合成長超過 20%（原話："greater than 20% over that period"）
- 2026-09-29｜Rex Geveden (CEO)｜risk：CEO：HEU 庫存正在消耗（原話："So we're burning that stockpile down"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜customer：政府部門積壓訂單近 70 億美元（原話："almost $7 billion of that is in Government Operations"）
- 2026-09-29｜Rex Geveden (CEO)｜product：CEO：2026 年營收預計 38 億美元（原話："we'll do $3.8 billion in sales this year"）
- 2026-09-29｜Rex Geveden (CEO)｜customer：總積壓訂單由 40 億增至 84 億美元（原話："$4 billion in backlog when I was last standing here"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜customer：技術服務幾乎贏下所有投標（原話："we've won just about every contract that we bid"）
- 2026-09-29｜Rex Geveden (CEO)｜commitment：CEO：以新機組需求類比 70~90 年代，認為未來可能蓋 1,000 座大型機組（原話："It wouldn't surprise me if we build 1,000 large reactors"）
- 2026-09-29｜Joseph Miller (President, Government Operations)｜product：太空機會：NASA SR-1 Freedom 為追蹤指標（原話："I would track that one as the space opportunity"）

### 問答異常語氣（迴避／改口／保留）
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Ron Epstein：EBITDA 財測上調中有機與非有機各占多少？｜答法：僅回答 "It's mostly organic."，未給數字
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Jeffrey Campbell：醫療業務出售所得是否已決定用途？｜答法：回答 "So not exactly"，列出內部投資、併購、還債、買回等可能方向，未給具體分配
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Matt Akers：政府業務利潤率 2027 年是否可續升？｜答法：表示不設定 2027 財測，稱需持續維持績效，並說原預期 2027 的表現已提前在 2026 出現，未給 2027 數字
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Andre Madrid：Janus 結果不同（OE 或供應商）對經濟效益與貢獻的影響？｜答法：CEO 說 "maybe I'll hold comments on that one"，待談判階段結束後再說明，未給任何經濟面資訊
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Scott Deuschle：預期年底前的新設備訂單是吉瓦級大型還是 SMR？｜答法：未指明單一類型，列出 SMR、Darlington、AP1000、X300 等多種機會，改談政府交易與客戶動能
- BWXT_Q2_2026_Earnings_Call_20260803.md｜問：Tomo Sano：mPower 授權的變現模式與下一個里程碑？｜答法：僅提 BWXT 有權利金與製造權；對合作方的變現模式稱 "I'm not clear"，未回答里程碑
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Bianchi（TD Cowen）：請說明 2030 年服務／燃料／大型零組件組成的圓餅圖會長怎樣｜答法：CFO 表示不會有太大變化，並說明刻意不量化各項機會，不想被綁在單一路徑
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Ciarmoli（Guggenheim）：成長預測是否已含併購？Westinghouse 訂單金額是否已確定、是否改變成長斜率｜答法：CFO 表示併購放在額外成長機會、沒拆開；Westinghouse 訂單時點與執行未定，稱不想超前，細節留到 Q3；MacQuarrie 只講關係良好、在做資格認證，未給金額
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Engelbrecht（Baird）：特殊材料（HPDU、離心機）長期利潤率與人力｜答法：Miller 說利潤率會與其他政府客戶類似，但表示現在預測太早，沒給數字
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Ciarmoli：TRISO 全速量產年市場規模、每公斤成本與營收｜答法：Miller 直接說「不回答這些問題」，改談微反應爐燃料成本占比與 AP1000 比較
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Chase（線上）：CapEx 2027 年是否仍高於 5~6%｜答法：CFO 表示先前曾示意可能到 7%，現在 2027 目標改為 6%，並拒絕給更細的區間；2027 正式財測幾週後公布
- BWXT_Analyst_Investor_Day_BWX_Technologies_Inc_20260929.md｜問：Madrid（BTIG）：戰艦與 AUKUS 的上緣有多大、福特級節奏是否可能加速｜答法：CFO 表示未給戰艦與 AUKUS 上緣數字，也不給單艘價格，稱合約上固定成本決定最終價格

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 3 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260905","verdict":"進場·條件式（爆發候選）","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"第二階 1/3：回檔 ≤$130（前瞻本益比 ≤27 倍）或投資人日隱含 FY2028 EPS ≥$6.40／商用利潤率目標 ≥15%；第三階：Q3 政府部門年增 ≥5% 且商用利潤率 ≥12.5%","irr_base_pct":6.2,"ev5y_pct":32.6,"drift_watch_prior":{"dca_verdict":"進場·條件式（爆發候選）","dca_role":"衛星","signal":"B","val":"🔴","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.79,"ev5y_pct":32.6,"irr_base_pct":6.2,"max_dd_pct":-50,"bull_5y_price":307.2,"bear_5y_price":104.0,"p_bull_pct":25,"p_bear_pct":25,"rearm_trigger":"第二階 1/3：回檔 ≤$130（前瞻本益比 ≤27 倍）或投資人日隱含 FY2028 EPS ≥$6.40／商用利潤率目標 ≥15%；第三階：Q3 政府部門年增 ≥5% 且商用利潤率 ≥12.5%","price_at_dd":157.59,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"BWXT","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"BWX Technologies, Inc."},"oneliner":"美國海軍核反應爐的主要供應商，股價半年跌 41.6%、共識幾乎沒動；基本情境年報酬約一成，勝負看海軍新定價與首張新建訂單。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的主要是美國政府的錢，錢卡在核級製造資格與設施這一節點。","reasoning":"3Q26 營收 9.53 億美元，政府部門 6.391 億美元（67%），商業部門 3.142 億美元（33%）；FY2025 美國政府占合併營收約 68%。利潤更集中：3Q26 分部調整後 EBITDA 政府 1.44 億美元、商業 0.41 億美元，政府占 78%。TTM 毛利率 22.61%，3Q26 GAAP 營業利益 1.321 億美元、non-GAAP 1.497 億美元，營益率 13.9%／15.7%。在手訂單 85.6 億美元，其中約 5 億美元是 7 月併入的 PCG。單點依賴：美國政府單一客戶超過 40%，它同時是護城河來源與最大集中風險。產業時鐘在擴張期，依據是全球重型零組件產能仍緊（2026-11-02，CEO）與已簽的特殊材料合約，不是股價。反例：新建機組需求至今沒有變成美國訂單，擴張期的商業段仍是預期。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi6_backlog","f_kpi7_book_to_bill","f_peer_bwxt_gross_margin_pct"],"verdict_values":{"revenue_quality":"約三分之二來自美國政府長約，能見度高，但買方只有一個。45 億美元在手訂單預計 2027 年底前轉為營收（2026-09-29，CFO），約等於 FY2027 共識營收的 1.1 倍。","unit_econ_note":"海軍依總艘數定價、不按艘報價，固定成本大，量愈高吸收愈好（2026-09-29，CFO）。商業端服務與零組件利潤率不同，單位經濟事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"單一買方長約、核級資格、政府出資設施，加上尚未兌現的新建機組選擇權"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：CEO 說全球這類零組件產能仍不足（2026-11-02），Deloitte 與 Bain 指國防航太供應鏈緊張延續到 2027，但後兩者不是核能專屬資料。","bargaining":{"up":"上游目前無瓶頸，鋯管與大型鍛件取得順利，加拿大鋼鐵工人略缺（2026-08-03，CEO）。","down":"海軍是單一買方，新定價還在談；商業端由 Westinghouse 決定零組件分配，Doosan、IHI 會競爭（2026-11-02，CEO）。","geo":"加拿大 Cambridge 廠的產品可能賣回美國，受關稅影響；波蘭投資要有確定訂單才做。"},"profit_pool_dir":"事實表未涵蓋利潤池占比。方向上，政府段由舊定價轉向新定價與特殊材料，商業段仍在投入期。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM、滲透率與利潤池占比；逐字稿只有單機可觸及金額（CANDU 3.5～7 億美元、SMR 0.5～1 億美元），不足以組成市場表。"}}}},"q2_moat":{"verdict":"護城河穩定：海軍核心地位沒變，新領域的競爭比舊領域多。","reasoning":"海軍反應爐沒有揭露第二來源，法規與資本門檻把競爭者擋在外面。事實表沒有同業投入資本，方向改用客戶份額判斷。毛利率 22.61% 高於四家國防同業（11.73%～21.10%），TTM 營益率 9.83% 卻低於四家（10.37%～11.78%）；3Q26 公司口徑 GAAP 營益率為 13.9%，差距可能來自資料商未把權益法收益計入營業利益，事實表無法確認。執行力給 8 分，依據是 3Q26 政府部門利潤率 22.6%、Cambridge 擴產略低於預算完工。定價力給 7 分，因為買方單一、新定價協議還沒簽，商業端 CEO 也說一定有價格壓力（2026-11-02）。反例：海軍若引入第二來源或新約大幅讓利，這個判斷就錯。","fact_refs":["f_peer_bwxt_gross_margin_pct","f_peer_bwxt_operating_margin_pct","f_peer_lmt_gross_margin_pct","f_peer_rtx_gross_margin_pct","f_peer_noc_gross_margin_pct","f_peer_gd_gross_margin_pct","f_peer_lmt_operating_margin_pct","f_peer_rtx_operating_margin_pct","f_peer_noc_operating_margin_pct","f_peer_gd_operating_margin_pct","f_kpi0_gaap","f_kpi2_gaap"],"verdict_values":{"moat":{"mechanism":"核級製造資格、政府授權設施與長期海軍合約。換供應商要重建設施與資格，實際轉換時間事實表未涵蓋。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：3Q26 政府部門利潤率 22.6%，Cambridge 產能增約 50%。定價面穩定：舊定價 2026 年底消化完，新多年期定價仍在談。兩者合併判穩定。客戶份額未見下滑，美國政府占營收由 76% 降到 68% 是商業段變大，不是份額流失。","competitor_notes":[{"name":"LMT","strategy_note":"毛利率約為 BWXT 一半，營益率較高，屬系統整合商，未列在 10-K 摘要的核部件對手。"},{"name":"RTX","strategy_note":"毛利率 21.10% 最接近 BWXT，研發密度高於 BWXT，業務重疊有限，只作國防利潤率參考。"},{"name":"NOC","strategy_note":"10-K 列為政府核部件對手，營益率略高於 BWXT，沒有證據顯示切入海軍反應爐。"},{"name":"GD","strategy_note":"未列在 10-K 摘要的核部件對手，FCF 利潤率與 BWXT 接近，只作現金轉換參考。"},{"name":"Westinghouse","strategy_note":"既是對手也是客戶，AP1000 零組件分配由它決定，正在對 BWXT 做資格認證。"},{"name":"Doosan","strategy_note":"AP1000 零組件的直接競爭者，影響的是價格與份額，不影響海軍核心。"}],"spread_notes":null,"peer_na_reason":"事實表只給同業利潤率，沒有 ROIC 與投入資本，無法算對最強同業的報酬差距，改看毛利率差與客戶份額。","threats":[{"level":"🟡","text":"TRISO-X 的 Oak Ridge TX-1 於 2026-02-13 取得 NRC 許可，DOE 也把 TRISO-X 與 Valar 納入燃料試點。攻擊範圍限於 TRISO，不碰海軍核心。BWXT 的 Lynchburg 線年產約兩百公斤，可至少擴到四倍（2026-11-02，CEO）。攻擊者資本量級事實表未涵蓋。","p":"40%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"AP1000 零組件要跟 Doosan、IHI 競爭，CEO 同時說全球產能不夠分。影響在價格，不在資格。","p":"60%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"10-K 提到現有技術可能被顛覆，醫用同位素也有替代技術。這是通用揭露，沒有具體對手；醫療事業出售後只留 20%，曝險變小。","p":"30%","evidence_refs":["competitive_share_entrants#2","substitute_technology#0"]}],"roic_durability":{"quadrant":"暫列低利益率×高周轉。營益率約 10%～14%，部分設施由政府出資；投入資本事實表未涵蓋，當期 ROIC 無法計算。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"海軍使用、NNSA 決策、國會付款，三個角色都成立，且屬既定計畫，預算延宕時約可拿前一年 95%（2026-11-02，CEO）。商業新建段的風險分配還沒談定，只算黃燈。"},{"item":"決策層級","level":"🟢","text":"海軍的替代性要看反應爐資格層，沒有第二來源揭露。商業端替代性高得多，Westinghouse 可在 BWXT、Doosan、IHI 之間分配。"},{"item":"價值鏈分配","level":"🟡","text":"舊定價換新讓政府利潤率由年初 19% 升到約 20.5%，但下一份多年期協議還沒簽。單一買方對固定成本結構很清楚，分配結果要看這次談判。"},{"item":"社會容忍度","level":"🟡","text":"獲利依賴聯邦預算與法規授權。EO 14372 可能限制關鍵國防承包商的股息、回購與高管薪酬指標，顯示政治上限已經出現；核能支持目前跨黨派。"}],"roiic":"約 14.7%（FY2022→FY2025 實現，含 Kinectrics）；管理層 2030 目標隱含超過 50%，不採用","reinvest_rate":"約 72.3%（同口徑含併購）；不含併購約 11%","endo_ceiling":10.6,"formula_note":"淨利增 0.908 億美元；投入＝FY2023～FY2025 淨利 8.567 億－FCF 7.625 億＋Kinectrics 5.25 億＝6.192 億美元。以淨利代 NOPAT，PCG 與其他併購未計，Kinectrics 併入時點事實表未涵蓋。2030 目標隱含值被政府出資與預收款墊高，所以只用已實現數字。"}}}},"q3_growth":{"verdict":"跑道寬，但五年後那段要靠還沒簽的訂單。","reasoning":"成長以量為主。共識 EPS 由 FY2026E 4.75 美元到 FY2028E 5.86 美元，年增 11.07%；FY2027 只增 8.8%，部分因年底出售醫療事業。內生上限 10.6%，缺口 0.5 個百分點，歸因利潤率擴張（2026-09-29，CFO 給合併 EBITDA 利潤率 17.5%→約 20%）。第一條曲線是海軍 4～6% 年複合；第二條是特殊材料 24% 年複合，HPDU 16 億美元與濃縮 15 億美元合約已簽；第三條是新建機組、Janus 與 TRISO，還沒變成大額訂單。超過一半成長來自既有核心（2026-09-29，CFO），戰艦未列入預測。反例：特殊材料長期利潤率 Miller 未給數字，若明顯低於政府平均，量長了獲利不一定長。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi6_backlog","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主（特殊材料、海軍、商業零組件），定價次之（海軍舊約換新），併購第三（2024 年以來 15% 年複合裡有機 8.5%），回購不計。","runway_years":"滲透率事實表未涵蓋；海軍合約能見度據稱 6～8 年","runway_post_y5":"🟢","endo_ceiling_basis":"沿用護城河段的 14.7% × 72.3%＝10.6%。共識 FY2026E→FY2028E 年增 11.07% 略高於上限，缺口可歸因利潤率擴張。FY2025A 只有 GAAP 基期，混口徑的 17.9% 不採用。","segments":[{"item":"政府部門 3Q26","value":"營收 6.391 億美元，年增 3.6%；調整後 EBITDA 利潤率 22.6%"},{"item":"商業部門 3Q26","value":"營收 3.142 億美元，年增 25%，有機 15%；調整後 EBITDA 利潤率 13.2%"},{"item":"2027 初步展望","value":"政府營收與 EBITDA 高個位數至低雙位數；商業有機高個位數、報告數低個位數，利潤率增 50～100 基點"},{"item":"2030 架構","value":"營收 55～60 億美元，調整後 EBITDA 11～12 億美元，自由現金流 5.25～5.75 億美元"}],"decay_signals":[{"item":"毛利率連兩季年減","status":"亮","note":"季度資料事實表未涵蓋；年度 24.86%→24.23%→22.91%，TTM 22.61%，以年度趨勢計入。"},{"item":"核心市占縮減","status":"未亮","note":"海軍沒有第二來源揭露。"},{"item":"提價後銷量下滑","status":"未亮","note":"無此類資料。"},{"item":"EPS 年增高於營收逾 5 個百分點","status":"未亮","note":"FY2022～FY2025 EPS 11.3%、營收 12.7%。"},{"item":"FCF／淨利連兩年低於 0.75","status":"未亮","note":"FY2024 與 FY2025 皆約 0.90。"},{"item":"SBC／營收超過 5% 且上升","status":"未亮","note":"年化約 1%。"},{"item":"TAM 萎縮或被替代","status":"未亮","note":"有 TRISO 競爭，未見市場萎縮。"},{"item":"產業倍數三年系統性下移","status":"未亮","note":"同業倍數事實表未涵蓋，無法判定。"},{"item":"維護性資本支出占 FCF 超過 60%","status":"未亮","note":"營收 3.5%～4% 約 1.3～1.5 億美元，占 FCF 約四成。"},{"item":"停止投資新產能且收入下滑","status":"未亮","note":"仍在擴產。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金轉換好，併購報酬還看不到，回購只抵銷稀釋。","reasoning":"FY2024 與 FY2025 的 FCF／淨利都約 0.90。前九個月 SBC 2,990 萬美元，年化約占營收 1%。現金去向四分事實表未涵蓋，只有片段：Kinectrics 5.25 億美元，PCG 金額未見，醫療事業以 7.5～8 億美元出售並保留 20%。2026 無回購計畫，2027 小幅回購只抵銷稀釋（2026-11-02，CFO）。2025-11 發 12.5 億美元零息可轉債，2026-11-04 發 5 億美元 2034 優先債並收購舊票據，目前淨負債約 14.5 億美元。反例：約 35 億美元可部署資金若用在大型併購，這個判斷要重寫。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Kinectrics 與 PCG 各自的投入與獲利未揭露，單案已實現報酬事實表未涵蓋。含併購的整體粗估約 14.7%，不能代表單案。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"2026 無計畫回購（2026-08-03，CFO），2027 只小幅回購抵銷稀釋（2026-11-02，CFO），回購均價事實表未涵蓋。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 年化約 4,000 萬美元，除以市值 109.5 億美元約 0.36%，低於 1.5%。零息可轉債的潛在稀釋未計，轉換價事實表未涵蓋。"}]},"governance":{"capital_returns":[{"item":"FY2023～FY2025 自由現金流合計","value":"7.62 億美元"},{"item":"2024 年以來營收年複合成長","value":"15%，其中有機 8.5%（2026-09-29，CEO）"},{"item":"Kinectrics 收購","value":"5.25 億美元"},{"item":"醫療事業出售","value":"對價 7.5 億美元，最高 8 億美元，保留 20%"},{"item":"到 2030 年可動用資金","value":"約 55 億美元，扣資本支出與股利後約 35 億美元"},{"item":"股息","value":"TTM 殖利率 0.887%，管理層稱維持並增加"}]}}},"q5_valuation":{"verdict":"現價要求 FY2031 EPS 到約 8.0 美元、終端 23 倍；我信前半，後半要看海軍定價。","reasoning":"要賺 10% 年報酬，FY2031 EPS 要到約 8.0 美元（年增 11%）。管理層 2030 調整後 EBITDA 中點 11.5 億美元，按 2026 年淨利對 EBITDA 約 65% 換算，FY2030 EPS 約 8.2 美元，現價要求的進度比目標晚一年以上。FY2028 共識 5.86 美元有合約支撐，FY2029 之後要靠海軍定價與新建訂單。同業倍數事實表未涵蓋，這是本次估值最大限制；真正的五年分位也沒有，只有 4 個年度端點分位。反例：倍數若向 17 倍靠，EPS 達標股價仍會跌。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy3_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"FY1 共識 EPS 前瞻本益比","tier":"核能國防核心供應商，事實表沒有同層級同業倍數","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或 EV 倍數，無法做倍數對照。終端倍數因此只錨公司自身現值與成長率。"},"fwd_pe":25.16,"peg":2.27,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 25.16 倍、PEG 2.27（25.16 ÷ 11.07），PEG 偏貴；Trailing P/E 在 4 個年度端點的 26.9 分位，基本情境年報酬約一成且不靠倍數擴張，結論為合理偏高。五年分位事實表未涵蓋。短期：FY2027E 5.15 × 25 倍＝128.8 美元，＋7.7%；三年：FY2029E 6.50 × 23.5 倍＝152.8 美元，＋27.8%。","upside_short_pct":7.7,"upside_mid_pct":27.8,"denominator_disputed":false,"denominator_note":"FY2026E EPS 含年底出售的醫療事業，年化營收約 1.3 億美元，占比小，分母不是主要爭點。"}}},"q6_how_wrong":{"verdict":"最可能看錯三處：海軍新定價、新建訂單時程、股價下跌的真正原因。","reasoning":"管理層迴避的題目集中在單位經濟：Janus 經濟效益（2026-08-03，CEO）、TRISO 每公斤成本（2026-09-29，Miller）、特殊材料長期利潤率（2026-09-29，Miller）、Westinghouse 訂單金額（2026-09-29，CFO）。這四項正是第二條曲線的獲利依據，所以基本情境不計入超額利潤率。歷史最大回撤與空方報告事實表未涵蓋；訴訟、臨床、召回、SEC 調查四項搜尋無結果。","fact_refs":["f_week26_return_pct","f_ma_state","f_ma_w250","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"核心穩，後段成長與利潤率尚未驗證"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":4.75,"pe":25.16,"basis":"FY2026E 共識 EPS，現價 119.52 美元除以 FY1，與終端倍數同為當年度前瞻口徑"},"eps":{"bull":[5.35,6.3,7.5,8.9,10.5],"base":[5.15,5.8,6.5,7.25,8.0],"bear":[4.95,5.0,5.05,5.1,5.15]},"pe":{"bull":28,"base":23,"bear":17},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.887,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"max_dd":{"lo":-46,"hi":-30,"basis":"從現價起算。下緣：FY2026E 共識打九折 4.28 美元 × 15 倍＝64 美元，約 −46%。上緣：FY2027 Bear EPS 4.95 美元 × 17 倍＝84 美元，約 −30%。近 26 週已跌 41.6%，從高點算的累計回撤會更深；歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"2030 目標上緣達成，2027 年中後新建訂單連續進帳，Erwin 範圍擴及 LEU 與 HALEU，FY2031 EPS 10.5 美元，年複合 17.2%。終端 28 倍高於現值 25.16 倍，同業現值倍數事實表未涵蓋。","base":"沿 2027 初步展望與共識到 FY2028，之後年增約 11%，FY2030 比目標中點換算值 8.2 美元低約一成。政府利潤率留在約 20.5%，不外推 3Q26 的 22.6%。終端 23 倍低於現值 25.16 倍，同業現值倍數事實表未涵蓋。","bear":"海軍新定價讓政府利潤率回到 19% 以下，新建訂單延到 2028 年後，FY2027 EPS 4.95 美元低於展望下緣，之後幾乎不長。成長降到 10% 以下，前瞻倍數按 PEG 1.7 算約 17 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"下一份海軍多年期定價協議還在談（2026-11-02，CEO），3Q26 政府部門占分部調整後 EBITDA 78%。","assumption":"新定價至少維持全年約 20.5% 的政府利潤率。","consequence":"五年後虧 50% 最可能的路徑：新定價讓利、新建訂單延到 2028 年後、美國新廠已開工。EPS 停在 4.3 美元、倍數 14 倍，股價約 60 美元。","ruling":"採納。這條與唯一致命點是同一件事，不另立，Bear 機率 30% 已反映。","watch":"新定價協議公告、政府部門季度利潤率","evidence_refs":["customer_concentration_credit#0"],"fact_refs":["f_kpi0_gaap","f_price_at_dd"]},{"view":"論點失敗","evidence":"股價 26 週跌 41.6%，共識幾乎沒動，事實表沒有記錄下跌的直接原因。","assumption":"跌幅主要是主題溢價退潮，不是獲利出事。","consequence":"若市場提前知道海軍或合約的壞消息，目前共識就是落後指標，基本情境會高估。","ruling":"無法反駁，只能用倉位處理。本次只買一個級距，下一筆要等基本面數字。","watch":"賣方下修 FY2027 EPS 的幅度、2026Q4 財報","fact_refs":["f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy3_pct"]},{"view":"論點成功但股東經濟變差","evidence":"2027 自由現金流持平到小增，獲利卻高個位數到低雙位數成長（2026-11-02，CFO）。美國新廠不看確定訂單也要蓋（2026-11-02，CEO），金額未揭露。資本支出說法由可能近 7%（2026-08-03）回到 5～6%（2026-09-29）。約 35 億美元可部署資金，策略長提到轉型型併購。EO 14372 可能限制股息與回購。","assumption":"新投資的增量報酬維持 15% 以上，多餘現金會回到股東手上。","consequence":"2030 目標達成，但股東拿到更多資本、更低報酬率與可轉債稀釋，每股價值成長低於 EBITDA 成長。","ruling":"部分採納。基本情境不計淨回購，終端倍數壓到 23 倍。","watch":"FCF／淨利低於 0.75、資本支出超過營收 7%、單筆併購超過市值 15%","evidence_refs":["regulatory_antitrust#1"],"fact_refs":["f_kpi3_fcf","f_ev_m"]},{"view":"價格已反映太多","evidence":"前瞻本益比 25.16 倍，同口徑 EPS 年增 11.07%，PEG 2.27。賣方平均目標價 193 美元是 7 月底的舊數字，現價已低於它 38%，不能當上檔依據。","assumption":"公司仍配得上較高倍數；同業現值倍數事實表未涵蓋。","consequence":"倍數若向 17 倍靠，就算 FY2027 達共識 5.17 美元，股價約 88 美元，下跌 26%。","ruling":"反駁一半。現價不便宜，但基本情境已用 23 倍終端，結論只到合理偏高。","watch":"前瞻本益比回到 30 倍以上時不追","fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 157.59 → 本次 119.52（-24.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=157.59","side_b":"本次 price_at_dd=119.52","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場·條件式（爆發候選） → 本次 進場","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場·條件式（爆發候選）","side_b":"本次 dca_verdict=進場","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份裁決：估值 🔴→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 157.59 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 157.59 美元：Bull 價 307.2、Bear 價 104，五年期望值 +32.6%，基準年化 6.2%，不對稱比 2.79","side_b":"本次情境、股價仍用 157.59 美元：Bull 價 294、Bear 價 87.55，五年期望值 +12.4%，基準年化 3.1%，不對稱比 1.3","ruling":"先換情境、股價不動：五年期望值少 20.2 個百分點，基準年化少 3.1 個百分點。不對稱比由 2.79 變為 1.3。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 157.59 美元：五年期望值 +12.4%，基準年化 3.1%，不對稱比 1.3","side_b":"本次情境、股價 119.52 美元：五年期望值 +48.1%，基準年化 9.0%，不對稱比 3.64","ruling":"再換股價、情境不動：起點價下跌 24.2%，五年期望值多 35.8 個百分點，基準年化多 5.9 個百分點，不對稱比由 1.3 升到 3.64。合計五年期望值比前份多 15.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與進場結論","cause":"價格變動","prior_field":["val"],"side_a":"2026-09-05：股價 157.59 美元，前瞻本益比約 33 倍，估值偏貴，條件式進場。","side_b":"2026-11-08：股價 119.52 美元，前瞻本益比 25.16 倍，FY1 共識只由 4.74 升到 4.75 美元，估值轉為合理偏高。","ruling":"可調和。變動來自股價，不是獲利數字。下跌已打到前份的價格條件，進場結論維持條件式，不因跌幅放大倉位。","evidence_level":"實測數字","settle_metric":"前瞻本益比與 FY2027 共識 EPS","if_then":["若股價反彈到 150 美元以上而政府部門與訂單都還沒驗證，不追","若股價再跌而 FY2027 共識 EPS 維持 5.0 美元以上，分批反買"]},{"axis":"情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 與 Bear 各 25%，最大回撤 −50%。","side_b":"本次：Bull 20%、Bear 30%，從現價起算最大回撤 −30%～−46%。","ruling":"可調和。本次用已實現數字算內生上限 10.6%，共識與基本情境都略高，Bear 機率拉到 30%。Bull 降到 20%，因為首張新建訂單還沒落地。前份回撤的起算口徑摘要未載，本次明確從現價起算。","evidence_level":"推導","settle_metric":"FY2027 EPS 與政府部門利潤率","if_then":["若 2027 全年 EPS 低於 4.95 美元，Bear 機率上調到 40%，停止加碼","若首張新建訂單落地且政府利潤率 ≥20%，Bull 機率回到 25%，分批加碼"]},{"axis":"品質、陷阱、護城河與跑道結論","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：評等 B、陷阱風險中等、護城河持平、五年後跑道寬、品質複利成長、未標循環位置。","side_b":"本次六項結論不變。新增證據有投資人日 2030 目標、2027 初步展望、Janus 與 Antares 合約，以及有機在手訂單連兩季下滑。","ruling":"可調和。正反證據互抵，結論不動。合約勝利強化第二條曲線，訂單下滑與利潤率未驗證壓住上調空間。","evidence_level":"公司揭露","settle_metric":"海軍新定價與首張新建訂單","if_then":["若海軍新定價使政府利潤率 ≥21%，護城河定價分上調，分批加碼","若海軍新定價使政府利潤率低於 19%，護城河轉為縮減，減碼至半倉"],"evidence_refs":["end_markets#0","channel_business_model_shift#0"]},{"axis":"加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"第二階 1/3：回檔 ≤$130（前瞻本益比 ≤27 倍）或投資人日隱含 FY2028 EPS ≥$6.40／商用利潤率目標 ≥15%；第三階：Q3 政府部門年增 ≥5% 且商用利潤率 ≥12.5%","side_b":"第三階 1/3：4Q26 政府部門年增 ≥8% 且利潤率 ≥20%，或 2027-06-30 前取得首張美國新建訂單；價格條件 ≤$107（前瞻約 22.5 倍）","ruling":"前份加碼第二階已發火：現價 119.52 美元低於 130 美元，前瞻 25.16 倍低於 27 倍，商業利潤率 2030 目標為高十位數也過 15%。第三階沒過：3Q26 政府部門年增 3.6%，低於 5%；商業利潤率 13.2% 過關，但兩項要同時成立。新門檻把政府年增拉到 8%，因為 2027 初步展望由高個位數起跳。","evidence_level":"實測數字","settle_metric":"2026Q4 政府部門年增與利潤率","if_then":["若 2026Q4 條件成立，加碼第三個 1/3","若 2026Q4 政府部門年增低於 5%，停止加碼到海軍新定價公布"]},{"axis":"Single Thing 前份缺值","cause":"方法變動","prior_field":["single_thing"],"side_a":"null（前份摘要未留存唯一致命點）","side_b":"下一份海軍多年期定價協議的利潤率低於舊約換新後水準，使政府部門調整後 EBITDA 利潤率跌破 19%。","ruling":"前份摘要沒有這一欄，本次依單一敏感度最大項重新選定。","evidence_level":"推導","settle_metric":"海軍新定價協議與政府部門利潤率","if_then":["若政府部門利潤率連兩季低於 19%，減碼至半倉"]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"null（前份摘要未留存停損指標）","side_b":"政府部門利潤率連兩季低於 19% 減碼；在手訂單連兩季低於 80 億美元減碼；海軍引入第二來源清倉。","ruling":"前份摘要沒有這一欄，本次新訂，門檻都能從季報直接驗證。","evidence_level":"推導","settle_metric":"季報揭露的政府部門利潤率與在手訂單","if_then":["若海軍確認引入第二來源，清倉"]},{"axis":"新建機組訂單時程滑動","side_a":"2026-08-03 CEO：年底前有機會拿到至少一張新建設備訂單，並預期下半年會有一張。2026-09-29 MacQuarrie：今年稍晚或 2027 年初。","side_b":"2026-11-02 CEO：年底前仍有可能，但不晚於 2027 年上半年；若落空，2030 目標仍有多條路。","ruling":"可調和，屬時點後移。三場說法依序往後，基本情境採較晚時點。CFO 說新建拐點在 2028～2029 年，晚半年對 FY2027 影響小，對 FY2029 之後影響大。決勝數據今天不存在，2027-06-30 前不可裁決。","evidence_level":"管理層說法","settle_metric":"2027-06-30 前首張美國新建機組零組件訂單","if_then":["若 2027-06-30 前拿到訂單，加碼第三個 1/3","若 2027-06-30 前仍無訂單，停止加碼，Bear 機率上調到 35%"],"evidence_refs":["end_markets#3"]},{"axis":"政府部門利潤率是結構性還是峰值","side_a":"2026-11-02 CFO：海軍業務效率大幅提升，舊定價逐步消化，3Q26 政府部門利潤率 22.6%。","side_b":"全年指引約 20.5%，2027 EBITDA 成長與營收大致同步（2026-11-02，CFO）；原預期 2027 的表現已提前出現（2026-08-03，CFO）。投資人日 CFO 給 2030 年約 20% 合併利潤率，CEO 同場卻說先不下定論（2026-09-29，摘錄無完整上下文）。","ruling":"拆三塊：年初 19% 到 20.5% 是舊定價換新，算結構性；20.5% 到 22.6% 的 2.1 個百分點含權益法收益與專案超額，當殘差，不進基本情境，反映在 Bear 機率。CFO 把政府營收偏低歸因於成本表現好使完工比例法認列較少，這點不採信也不否定，先標未證。","evidence_level":"公司揭露","settle_metric":"2026Q4 與 2027Q1 政府部門營收年增","if_then":["若 2026Q4 與 2027Q1 政府部門營收年增連兩季低於 8%，判定會計歸因不成立，停止加碼","若連兩季利潤率 ≥21% 且營收年增 ≥8%，分批加碼"]},{"axis":"需求湧現與有機在手訂單","side_a":"2026-11-02 CEO：需求環境異常強，正把機會轉成有意義的新訂單，涓流將成洪流。","side_b":"在手訂單 87 億（1Q26）→84 億（2Q26）→85.6 億美元（3Q26）。3Q26 含併購帶進的約 5 億美元，扣掉約 80.6 億美元，有機連兩季下滑；3Q26 接單出貨比 0.56 倍。","ruling":"可調和，但管理層沒有主動講這件事。大型多年期合約本來就不連續，2Q26 底近 12 個月接單出貨比 1.7 倍就是例子。近期訊號採信在手訂單這一側，需求說法要用海軍定價協議與首張新建訂單驗證。","evidence_level":"公司揭露","settle_metric":"期末在手訂單與季度接單出貨比","if_then":["若連兩季在手訂單低於 80 億美元，減碼至半倉","若海軍定價協議入帳使在手訂單回到 90 億美元以上，分批加碼"],"evidence_refs":["end_markets#2","supply_demand_durability#3"]},{"axis":"股價與共識背離（現在就賣的最強論證）","side_a":"股價 26 週跌 41.6%，低於 52 週與 104 週均線。","side_b":"FY1 共識近三個月 ＋0.21%，FY2 ＋0.19%，FY3 −0.51%，2027 初步展望微升，Fitch 給投資等級。","ruling":"可調和，方向相反但差在倍數。現在就賣的最強論證：25 倍前瞻本益比對應約 11% 成長，PEG 2.27 不便宜；FY3 共識已開始下修；事實表沒有下跌原因，市場可能定價了我們沒看到的事。反駁：超過一半成長來自既有核心（2026-09-29，CFO），管理層只計入小幅新建訂單（2026-11-02，CEO）。採基本面這一側，但只買一個級距。","evidence_level":"實測數字＋管理層說法","settle_metric":"週收盤相對 250 週線、政府部門利潤率、FY2027 共識","if_then":["若週收盤跌破 250 週線 107.29 美元且政府部門利潤率低於 20%，趨勢訊號證實為對，停止加碼到 2027-06-30","若跌破 250 週線而政府部門利潤率 ≥20%、共識未下修，分批反買","若未驗證就反彈回 104 週線 158.59 美元，不追"]},{"axis":"產業態勢三軸","side_a":"競爭：海軍核心沒有第二來源揭露；新領域 TRISO-X 已取得 NRC 許可，AP1000 零組件要和 Doosan、IHI 競爭。","side_b":"結構：全球重型零組件產能仍緊（2026-11-02，CEO），主權資金與跨黨派支持。其他：EO 14372、關稅與加拿大競爭審查。","ruling":"裁決：結構性轉好中。依據是已簽的特殊材料合約與 Cambridge 擴產約 50%，競爭惡化只出現在尚未貢獻獲利的新領域。","evidence_level":"公司揭露＋二手資料","settle_metric":"首張新建訂單的價格與利潤率","if_then":["若商業部門利潤率連兩季低於 12.5%，停止加碼"],"evidence_refs":["substitute_technology#1","competitive_share_entrants#0","supply_demand_durability#0"]}],"triggers":[{"n":1,"text":"2026Q4 政府部門營收年增至少 8%、利潤率至少 20%，才買第三個 1/3。","type":"加碼","maps_to":"H1","metric":"政府部門季度營收年增與調整後 EBITDA 利潤率","threshold":"營收年增 ≥8% 且利潤率 ≥20%","action":"加碼第三個 1/3","source_freq":"季報，每季","date":"2027-Q1"},{"n":2,"text":"股價跌到 107 美元以下，但政府利潤率與共識都沒壞，分批反買。","type":"估值rearm","maps_to":"H1","metric":"股價、政府部門利潤率、FY2027 共識 EPS","threshold":"≤107 美元，利潤率 ≥20%，FY2027 共識 ≥5.0 美元","action":"分批反買","source_freq":"每週","date":null},{"n":3,"text":"海軍新定價簽定後，政府部門利潤率連兩季低於 19%。","type":"Single Thing","maps_to":"R2","metric":"政府部門調整後 EBITDA 利潤率","threshold":"連兩季低於 19%","action":"減碼至半倉；若首張新建訂單也落空則清倉","source_freq":"季報與 8-K","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":4,"text":"2027-06-30 前沒有首張美國新建機組零組件訂單。","type":"假設驗證","maps_to":"H2","metric":"美國新建機組訂單","threshold":"2027-06-30 前為零","action":"停止加碼","source_freq":"法說與新聞稿","date":"2027-06-30"},{"n":5,"text":"第四季沒有如期跳升。","type":"風險","maps_to":"R1","metric":"FY2026 調整後 EPS 與自由現金流","threshold":"EPS 低於 4.72 美元或自由現金流低於 3.5 億美元","action":"停止加碼","source_freq":"季報","date":"2027-Q1"},{"n":6,"text":"在手訂單連兩季低於 80 億美元。","type":"減碼","maps_to":"R3","metric":"期末在手訂單","threshold":"連兩季低於 80 億美元","action":"減碼至半倉","source_freq":"季報","date":null},{"n":7,"text":"EO 14372 的 DFARS 條款定案，且適用 BWXT 的合約。","type":"風險","maps_to":"R4","metric":"DFARS 最終條款與公司揭露","threshold":"股息或回購受限","action":"停止加碼","source_freq":"聯邦公報與 10-Q","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":8,"text":"關稅或擴產成本吸收失敗。","type":"風險","maps_to":"R5","metric":"商業部門調整後 EBITDA 利潤率","threshold":"連兩季低於 12.5%","action":"停止加碼","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#0"]},{"n":9,"text":"海軍確認引入第二來源。","type":"清倉","maps_to":"R2","metric":"海軍反應爐供應商結構","threshold":"出現第二來源","action":"清倉","source_freq":"10-K 與 NNSA 公告","date":null},{"n":10,"text":"首張新建訂單期限到期，整份論點重看一次。","type":"複審日期","maps_to":"H2","metric":"訂單、政府利潤率、在手訂單","threshold":"到期日","action":"重跑完整研究","source_freq":"一次性","date":"2027-06-30"}],"kill_metrics":[{"metric":"政府部門調整後 EBITDA 利潤率","bear_threshold":"連兩季低於 19%","window":"2027-03 至 2028-03 各季","source":"BWXT 季報與法說","last_status":"ok"},{"metric":"期末在手訂單","bear_threshold":"連兩季低於 80 億美元","window":"2027 全年各季","source":"BWXT 季報","last_status":"warning"},{"metric":"首張美國新建機組零組件訂單","bear_threshold":"2027-06-30 前仍為零","window":"至 2027-06-30","source":"BWXT 法說與新聞稿","last_status":"warning"},{"metric":"FY2027 調整後 EPS","bear_threshold":"低於 4.95 美元","window":"FY2027","source":"BWXT 年度財報","last_status":"unknown"},{"metric":"商業部門調整後 EBITDA 利潤率","bear_threshold":"連兩季低於 12.5%","window":"2027 全年各季","source":"BWXT 季報","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"第三階 1/3：4Q26 政府部門年增 ≥8% 且利潤率 ≥20%，或 2027-06-30 前取得首張美國新建訂單；價格條件 ≤$107（前瞻約 22.5 倍）","exec_line":"現價符合前份第二階條件，可買第二個 1/3；第三個 1/3 依上述條件。週收盤跌破 250 週線且政府利潤率低於 20% 時停止加碼。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"FY1 共識近三個月只動 ＋0.21%，2027 初步展望反而微升，跌幅幾乎全來自倍數。市場把新建訂單延後當成 2030 目標落空，但管理層只計入小幅新建訂單，超過一半成長來自既有核心。下跌的直接原因事實表未涵蓋。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"舊定價消化完後，政府部門靠特殊材料放量維持高個位數以上成長，利潤率守住 20%。","2y":"2027 全年政府部門營收年增 ≥8%，調整後 EBITDA 利潤率 ≥20%","5y":null,"10y":null,"threshold":"2027 年政府部門營收年增 ≥8% 且利潤率 ≥20%","source":"BWXT 季報與法說（2026-11-02 CFO 的 2027 初步展望）","drift_rule":"TTM 連兩季偏離 ≥5% 算削弱，連三季 ≥10% 算反轉"},{"id":"H2","text":"商業部門把新建機組需求轉成確定訂單，2030 年達管理層目標下緣。","2y":null,"5y":"FY2030 營收 ≥55 億美元、調整後 EBITDA ≥11 億美元、商業部門利潤率 ≥15%","10y":null,"threshold":"FY2030 營收 ≥55 億美元，調整後 EBITDA ≥11 億美元，商業部門利潤率 ≥15%","source":"BWXT 年報、季報與 2026-09-29 投資人日目標","drift_rule":"連四季偏離 ≥5% 算削弱，連六季 ≥10% 算反轉"},{"id":"H3","text":"先進核能與濃縮長成第二條獲利曲線，降低對海軍單一計畫的依賴。","2y":null,"5y":null,"10y":"2036 年前濃縮與先進核能合計占營收 ≥20%，微反應爐至少 3 座商業機組交付","threshold":"濃縮與先進核能合計占營收 ≥20%（現值事實表未涵蓋），商業微反應爐交付 ≥3 座","source":"BWXT 年報分部揭露、DOE／NNSA 公告、Janus 里程碑","drift_rule":"跨兩個年度未達階段里程碑算削弱，跨三個年度算反轉"}],"R":[{"id":"R1","text":"第四季獲利要跳一階。2026-08-03 CFO 說下半年約 55% 獲利落在第四季，以 3Q26 調整後 EPS 1.26 美元反推第四季約 1.54 美元；全年商業部門約 45% 成長也靠第四季。2026-11-02 CFO 說沒有特殊項目。","h_ref":"H1","clock":"⚡","threshold":"FY2026 調整後 EPS 低於 4.72 美元或自由現金流低於 3.5 億美元"},{"id":"R2","text":"美國政府占 FY2025 營收約 68%，下一份海軍多年期定價是最大的單一談判，新約若讓利會直接打到獲利核心。","h_ref":"H1","clock":"🔥","threshold":"政府部門利潤率連兩季低於 19%","evidence_refs":["customer_concentration_credit#0"]},{"id":"R3","text":"有機在手訂單連兩季下滑，新建訂單時程三場說法依序後移，2030 目標的後段因此更集中。","h_ref":"H2","clock":"🔥","threshold":"2027-06-30 前無美國新建訂單，或在手訂單連兩季低於 80 億美元"},{"id":"R4","text":"EO 14372 可能限制關鍵國防承包商的股息、回購、高管加薪與部分激勵指標，預期以新 DFARS 條款實施，會直接限制資本回饋。","h_ref":"H2","clock":"🔥","threshold":"DFARS 最終條款適用 BWXT 且股息或回購受限","evidence_refs":["regulatory_antitrust#1"]},{"id":"R5","text":"加拿大廠的重型零組件可能賣回美國，新增關稅會壓毛利，最終影響要看合約條款。這裡不預測關稅，只看商業部門利潤率是否吸收得住。","h_ref":"H2","clock":"🔥","threshold":"商業部門利潤率連兩季低於 12.5%","evidence_refs":["reg_tariff_export#0"]},{"id":"R6","text":"加拿大競爭局調查 Kinectrics 收購對核醫競爭的影響，2025-11 法院核准擴大調查令並納入 Novartis，2026 年未見結案。受影響範圍主要是年化營收約 1.3 億美元的醫療事業，出售完成後曝險縮小，但出售案本身可能受影響，結案日事實表未涵蓋。","h_ref":"H2","clock":"🐢","threshold":"競爭局提出挑戰，或醫療事業出售延到 2027-03-31 之後","evidence_refs":["regulatory_antitrust#0"]},{"id":"R7","text":"資本先於訂單。美國新廠不看確定訂單也要蓋（2026-11-02，CEO），金額未揭露，2027 自由現金流持平到小增。","h_ref":"H2","clock":"🔥","threshold":"資本支出超過營收 7% 且美國新建訂單仍為零"}],"single_thing":{"description":"下一份海軍多年期定價協議的利潤率低於舊約換新後水準，使政府部門調整後 EBITDA 利潤率跌破 19%。","why_fatal":"政府部門占 3Q26 分部調整後 EBITDA 78%，海軍占比事實表未涵蓋。以政府年營收約 26 億美元、稅率約兩成粗算，利潤率每少 1 個百分點，EPS 少約 0.23 美元，約 FY2026E 的 5%。由全年約 20.5% 跌破 19%，EPS 至少少 0.34 美元，倍數也會同步往下。新建訂單落空的影響分散在多張單與 2028 年後，不是最大單一敏感度。","if_happens":"減碼至半倉；若首張新建訂單也落空則清倉。","how_monitor":"海軍定價協議公告與金額（8-K、法說），每季政府部門調整後 EBITDA 利潤率。","probability":"12～24 個月約 15%"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.12,"peg_fy2":2.09,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":3.58,"FY2026E":4.75,"FY2027E":5.17,"FY2028E":5.86},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識，對應公司調整後 EPS 指引 4.72～4.77 美元；FY2025A 只有 GAAP 稀釋 EPS 3.58 美元，non-GAAP 基期事實表未涵蓋，所以三年年複合 17.9% 混口徑不採用，改用 FY2026E→FY2028E 的 11.07%。EPS 預估家數事實表未涵蓋。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"capacity","event":"美國商業重型零組件新廠最終投資決定","impact":"中","watch":"投資金額，是否推高資本支出超過營收 6%"},{"date":"2026-12","date_precision":"month","type":"product","event":"離心機原型機測試","impact":"中","watch":"是否如期運轉，LEU 與 HALEU 是否納入範圍"},{"date":"2026-12","date_precision":"month","type":"other","event":"醫療事業出售完成","impact":"中","watch":"實收金額與資金用途"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"2026Q4 財報與 2027 正式財測","impact":"高","watch":"政府部門年增與利潤率，第四季 EPS 是否達約 1.54 美元"},{"date":"2027-06","date_precision":"month","type":"other","event":"管理層所說首張美國新建機組訂單的最晚窗口","impact":"高","watch":"機組類型與單筆金額"},{"date":"2027-06","date_precision":"month","type":"other","event":"Y-12 鋰處理設施下一階段選商","impact":"低","watch":"是否入選"},{"date":null,"date_precision":null,"type":"other","event":"下一份海軍多年期定價協議","impact":"高","watch":"總金額與政府部門利潤率"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=FY1 共識近三個月只動 ＋0.21%，2027 初步展望反而微升，跌幅幾乎全來自倍數。市場把新建訂單延後當成 2030 目標落空，但管理層只計入小幅新建訂單，超過一半成長來自既有核心。下跌的直接原因事實表未涵蓋。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-41.62, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"requires_critic":[]}}
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
