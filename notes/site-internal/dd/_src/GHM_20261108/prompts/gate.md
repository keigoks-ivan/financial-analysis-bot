你是 DD 管線 v20 的判斷層閘（gate），標的 GHM（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝69.76 USD M｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.grahamcorp.com Q2 FY27 press release（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得可驗證的共識數字，省略
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝28.2 %｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q2 FY27（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝5.83 USD M（利益率 8.4%）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q2 FY27（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_kpi7_backlog`（q1_business）｜Backlog＝561.3 USD M｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q2 FY27（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_kpi8_book_to_bill`（q1_business）｜Book-to-bill／訂單＝1.1 x（訂單 73.7M）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q2 FY27（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_peer_ghm_gross_margin_pct`（q2_moat）｜GHM 毛利率＝23.29 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GHM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ghm_operating_margin_pct`（q2_moat）｜GHM 營業利益率＝5.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GHM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cw_gross_margin_pct`（q2_moat）｜CW 毛利率＝38.07 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cw_operating_margin_pct`（q2_moat）｜CW 營業利益率＝19.06 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ese_gross_margin_pct`（q2_moat）｜ESE 毛利率＝42.01 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ESE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_dco_gross_margin_pct`（q2_moat）｜DCO 毛利率＝27.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DCO.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.81 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.28 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝290.82 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（6 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝322.0 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（6 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_ocf_capex`（q4_capital）｜自由現金流（OCF 減 capex，推算，公司未報）＝44.5 USD M｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q2 FY27：OCF 46.7M、capex 2.2M；FCF 為自行相減（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_kpi5_sbc_equity_based_compens`（q4_capital）｜SBC（equity-based compensation）占營收＝1.12 %（0.782M；占 GAAP 營業利益 13.4%）｜期間與口徑：Q2 FY2027（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q2 FY27 Adjusted EBITDA 調節表（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2027（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-65.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 6.43、現金 71.43（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝11.74 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_ghm_fcf_margin_pct`（q2_moat）｜GHM FCF 利潤率＝-2.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GHM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝78.02 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝43.1 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.81，分子＝快照價 78.02｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝67.84 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝88.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（1.81 → 1.81）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.12 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 1.79 → 1.81（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.81｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-20.54 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝86.01 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝88.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝91.6 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝81.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（9 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：公司在所有市場面臨競爭，部分對手資源更大或因地理／匯率具成本優勢，可能因低成本對手而失去份額、價格轉變。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-06-08）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 前十大客戶占合併營收 60%（FY2025 60%、FY2024 57%），公司預期少數客戶仍將占大部分營收；FY2026 有兩家客戶各占逾 10%。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-06-08）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：國防占營收 60%（FY2025 58%、FY2024 54%），分散於多個承包商但最終客戶同為美國海軍，公司自述有資金中斷風險。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-06-08）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：競爭對手近期獲 General Dynamics 與 Huntington Ingalls 獎項，管理層表示有信心；Batavia 新 ERP 於 FY27 Q3 上線有暫時性生產／開票中斷風險（二手摘要）
  - 來源：Nasdaq, Graham Q1 earnings call highlights（as_of 2026-08-01）｜affects：decision_inputs.bear、triggers
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：GIPL（印度子公司）吹哨者調查已自願通報印度主管機關、美國 DOJ 與 SEC，公司持續配合；公司認為剩餘影響不重大。屬反貪腐性質，非反壟斷。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-06-08）｜affects：decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 10-K：關稅使毛利增加約 $1,000 千美元的額外成本（相對 FY2025）；毛利率 23.5%，下滑主因為產品組合（國防比重較高）。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-06-08）｜affects：valuation、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：風險因子：關稅可能影響電子元件、高階鋼材等原料成本，並使產品對海外客戶較不具吸引力。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-06-08）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：管理層對關稅衝擊的估計逐季上調：FY2026 全年增量約 $1.0–1.5 百萬美元（Q3 財報）；Q1 時稱不重大。
  - 來源：Barchart/BusinessWire: Graham Corporation Reports Third Quarter Fiscal 2026 Results（as_of 2026-02-05）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子載明：競爭者可能開發性能更佳的新技術，若 Graham 跟不上，產品可能過時、需求下降、失去份額或面臨價格壓力（該段寫的是 bladeless mixer 產業）。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-06-08）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":156.8,"bear_5y_price":37.8,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":10.5,"ev5y_pct":14.5,"irr_base_pct":2.0,"asym_ratio":1.6,"scenario_tree":{"terminal_label":"FY2032E","start":{"eps":1.81,"pe":43.1,"basis":"FY2027E（3 月底財年）共識調整後 EPS；終端倍數同為當年度調整後 EPS 的預估本益比"},"eps":{"bull":[2.45,3.05,3.65,4.25,4.9],"base":[2.25,2.58,2.85,3.15,3.45],"bear":[1.85,1.9,1.98,2.05,2.1]},"pe":{"bull":32,"base":25,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GHM_Q1_2027_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：FY27營收財測$285–295M，與上季相同（原話："revenue to be in the range of $285 million to $295 million"）
- 2026-08-06｜CFO｜guidance：FY27財測整體維持不變（原話："which remains unchanged from last quarter"）
- 2026-08-06｜CFO｜guidance：FY27毛利率財測24.5%–25.5%（原話："We continue to expect gross margin to be between 24.5%"）
- 2026-08-06｜CFO｜guidance：SG&A占營收16.5%–17.5%（原話："to be between 16.5% and 17.5% of sales"）
- 2026-08-06｜CFO｜guidance：FY27調整後EBITDA財測$35–40M（原話："adjusted EBITDA to be between $35 million and $40 million,"）
- 2026-08-06｜CFO｜guidance：FY27資本支出財測$18–22M（原話："expenditures to be between $18 million and $22 million"）
- 2026-08-06｜CFO｜guidance：積壓訂單35–40%於未來12個月轉營收（原話："approximately 35% to 40% of backlog to convert into revenue"）
- 2026-08-06｜CFO｜guidance：CFO稱太空營收當季水準為新常態（原話："revenue for the quarter is the new norm."）
- 2026-08-06｜CFO｜guidance：第三財季因假日通常最低（原話："typically the third quarter is the lowest"）
- 2026-08-06｜CFO｜guidance：三年框架：有機營收年增8–10%（原話："organic revenue growth of approximately 8% to 10% annually"）
- 2026-08-06｜CFO｜guidance：FY2029調整後EBITDA利潤率14–16%（原話："margins to expand into the 14% to 16% range by fiscal 2029"）
- 2026-08-06｜CFO｜margin：毛利率年減，管理層歸因於產品組合（原話："decline in gross margin primarily reflects the mix of sales"）
- 2026-08-06｜CFO｜margin：毛利率較上季增加230bp（原話："our gross margin percentage increased 230 basis points."）
- 2026-08-06｜CFO｜margin：國防占營收58%（上季60%、去年53%），毛利率與國防占比直接相關（原話："about 58% of our revenue this quarter was in Defense"）
- 2026-08-06｜CFO｜margin：管理層欲將國防與商業組合拉近50-50（原話："we want to get closer to that 50-50 mix"）
- 2026-08-06｜CFO｜margin：調整後EBITDA利潤率12.3%與去年同期持平（原話："representing an adjusted EBITDA margin of 12.3%,"）
- 2026-08-06｜CFO｜margin：GAAP淨利減少至$3.9M、每股$0.33（原話："$3.9 million or $0.33 per diluted share"）
- 2026-08-06｜CEO｜margin：雷達／雷射專案以市場定價而非認證成本定價（原話："market-bearing prices on those programs"）
- 2026-08-06｜CEO｜margin：競爭性標案允許較高毛利（原話："competitive and they allow for healthier margins"）
- 2026-08-06｜CEO｜margin：潛艦主力為單一來源、TINA成本定價（原話："That's sole sourced and under TINA cost and pricing."）
- 2026-08-06｜CEO｜commitment：管理層稱強勁開局使達成FY27目標處於有利位置（原話："2027 positions us well to achieve those targets."）
- 2026-08-06｜CEO｜commitment：重申FY27營收成長18%、EBITDA成長44%的指引（原話："18% revenue growth and 44% adjusted EBITDA growth"）
- 2026-08-06｜CEO｜commitment：重心由建置產能轉向運用產能（原話："building capabilities to leveraging those capabilities."）
- 2026-08-06｜CEO｜capital_allocation：新投資以高於20% ROIC門檻為目標（原話："target returns above our 20% ROIC hurdle rate"）
- 2026-08-06｜CFO｜capital_allocation：Arvada興建新廠房（原話："a new 30,000-square-foot manufacturing facility in"）
- 2026-08-06｜CFO｜capital_allocation：T. Rowe Price $50M策略投資，約$13M償債（原話："previously announced $50 million strategic investment"）
- 2026-08-06｜CFO｜capital_allocation：季末無負債（原話："million of cash on hand, no outstanding debt"）
- 2026-08-06｜CFO｜capital_allocation：營運現金流為負$12.7M（原話："operating activities during the quarter was $12.7 million"）
- 2026-08-06｜CEO｜customer：國防營收年增40%（原話："Defense revenue increased 40% during the quarter"）
- 2026-08-06｜CEO｜customer：MK48為單一來源續約選項年，非新增範圍（原話："MK48 is a sole sourced award and that is a follow-on"）
- 2026-08-06｜CEO｜customer：MK19為競爭性標案勝出，範圍擴大（原話："was a competitive solicitation and it was a good win"）
- 2026-08-06｜CEO｜customer：MK19與MK48合計約$43M（原話："totaled approximately $43 million."）
- 2026-08-06｜CEO｜customer：潛艦管線仍強（原話："the pipeline remains strong"）
- 2026-08-06｜CEO｜customer：執行力為擴大業務關鍵（原話："Just execution, period."）
- 2026-08-06｜CFO｜customer：售後市場訂單出貨比1.1（原話："aftermarket was 1.1 during the quarter."）
- 2026-08-06｜CFO｜customer：售後成長多來自國防售後（原話："growth though was driven by our Defense aftermarket."）
- 2026-08-06｜CEO｜risk：煉油與石化大型資本專案持續延後（原話："ongoing pushouts in large capital"）
- 2026-08-06｜CFO｜risk：太空訂單可能起伏，不預期每季維持此水準（原話："So we don't expect this level every quarter."）
- 2026-08-06｜CEO｜risk：北美煉油廠稼動率約96%（原話："about 96% utilization in refineries in North America"）
- 2026-08-06｜CEO｜risk：新能源市場仍處商業化早期（原話："remain relatively early in their commercialization"）
- 2026-08-06｜CEO｜product：太空訂單$14.4M，出貨比2.3x（原話："representing a book-to-bill of 2.3x"）
- 2026-08-06｜CEO｜product：FlackTek為第三大核心技術平台（原話："processing as Graham's 3rd core technology platform"）
- 2026-08-06｜CEO｜product：飛彈領域：Graham原非傳統市場（原話："Missiles had not been a conventional market for Graham."）
- 2026-08-06｜CEO｜product：透過FlackTek進入飛彈生產（原話："our early entry into missiles was through FlackTek"）
- 2026-08-06｜CEO｜product：MEGA平台涉及固態火箭發動機關鍵開發（原話："the MEGA being involved in some critical developments on"）
- 2026-08-06｜CEO｜competition：在過去有競爭對手的標案中亦獲勝（原話："we're also today winning opportunities where we did"）
- 2026-08-06｜CFO｜guidance：有機營收年增17%（原話："On an organic basis, revenue was up an impressive 17%."）
- 2026-08-06｜CFO｜guidance：當季訂單$96M，出貨比1.3x（原話："First quarter orders were $96 million"）

### GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 重申 FY27 營收財測區間（約 +18% at midpoint，含全年 FlackTek）（原話："be in the range of $285 million to $295 million"）
- 2026-06-18｜CFO Christopher Thome｜guidance：FY27 營收財測中點對應的成長幅度（原話："$285 million to $295 million, which represents an 18%"）
- 2026-06-18｜CFO Christopher Thome｜margin：FY27 毛利率財測區間，並列舉改善來源（原話："gross margin to be between 24.5% to 25.5%"）
- 2026-06-18｜CFO Christopher Thome｜guidance：FY27 SG&A 占營收比財測（原話："SG&A expense is expected to be between 16.5% and 17.5%"）
- 2026-06-18｜CFO Christopher Thome｜margin：SG&A 財測內含約 250 萬美元人員、技術、商業化的增量投入（原話："approximately $2.5 million of incremental investments"）
- 2026-06-18｜CFO Christopher Thome｜guidance：FY27 調整後 EBITDA 財測區間（原話："adjusted EBITDA to be between $35 million and $40 million"）
- 2026-06-18｜CFO Christopher Thome｜margin：CFO 說明 FlackTek 目前調整後 EBITDA 利潤率低於公司平均（原話："currently, FlackTek is a 10% adjusted EBITDA margin business"）
- 2026-06-18｜CFO Christopher Thome｜guidance：三年長期目標：有機營收成長 8%–10%（原話："growth continuing at the 8% to 10% rate for the next"）
- 2026-06-18｜CFO Christopher Thome｜guidance：三年長期目標：FY2029 調整後 EBITDA 利潤率 14%–16%（原話："EBITDA margin to continue to expand to the 14% to 16%"）
- 2026-06-18｜CFO Christopher Thome｜guidance：FY29 營收規模目標（連同約 $50–55M 調整後 EBITDA）（原話："$340 million to $350 million revenue company"）
- 2026-06-18｜CFO Christopher Thome｜margin：FY29 之後的終極目標：同業前四分之一，EBITDA 利潤率 17%–18%（原話："margins in the 17% to 18% range"）
- 2026-06-18｜CEO Matthew Malone｜margin：CEO 說明利潤率目標從追平同業進一步邁向同業前四分位（敘事升級）（原話："the top quartile within our peer group"）
- 2026-06-18｜CEO Matthew Malone｜margin：CEO 說明 Barber-Nichols 收購使利潤率承受約 200 基點的衝擊（earn-out 全額支付，回饋 1,200 萬美元給員工）（原話："and it's a tough 200-point basis hit"）
- 2026-06-18｜CEO Matthew Malone｜margin：CEO 提到 earn-out 全額支付的金額（原話："give back $12 million by hitting the max earn-out"）
- 2026-06-18｜CEO Matthew Malone｜guidance：CEO 重申 8%–10% 有機成長，並稱有機會加速就會加速（原話："focus on 8% to 10% organic investment -- organic growth"）
- 2026-06-18｜CEO Matthew Malone｜guidance：管理層訂 ROIC 目標：單案 >20%、公司整體層級 14%（原話："when I say 14%, that's at the aggregated corporate level"）
- 2026-06-18｜CEO Matthew Malone｜guidance：三年目標未納入併購（原話："we have not built in M&A"）
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 回答分析師：新計畫（商業化、售後等）的貢獻大部分已納入長期目標；FY26 約 1,000 萬、FY29 預期超過 5,000 萬（原話："expecting that to grow to north of $50 million"）
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 說明納入目標的口徑：只納入有相當把握的專案，其餘為潛在上檔（原話："ones where we felt fairly certain that we were going to get"）
- 2026-06-18｜CEO Matthew Malone｜guidance：CEO 說明新計畫納入目標時採加權方式，馬達控制器能否放量尚待驗證（原話："taken a weighted approach to how we're factoring that in"）
- 2026-06-18｜CFO Christopher Thome｜guidance：積壓訂單規模與國防占比（原話："85% of our $533 million backlog is to the defense industry"）
- 2026-06-18｜CFO Christopher Thome｜guidance：積壓訂單轉營收的時程（原話："35% to 40% of our backlog is expected to convert to"）
- 2026-06-18｜CFO Christopher Thome｜guidance：回應分析師：約 30% 積壓訂單要 2 年以上才到期，管理層稱不擔心 5.33 億積壓（原話："roughly 30% of our backlog isn't due until 2-plus years out"）
- 2026-06-18｜CFO Christopher Thome｜guidance：年度 book-to-bill 目標口徑為 1.1x（原話："goal is to achieve a book-to-bill ratio of 1.1x each year"）
- 2026-06-18｜CFO Christopher Thome｜risk：CFO 說明單季 book-to-bill 波動很大（原話："ranging from 0.5x to 2.4x in any given quarter"）
- 2026-06-18｜CFO Christopher Thome｜customer：CFO 給的 FY26 太空訂單成長數字（原話："our space orders increased 76% over the prior year"）
- 2026-06-18｜CFO Christopher Thome｜customer：CFO 給的 FY26 新能源（SMR、氫能）訂單成長數字（原話："energy orders were up 185%."）
- 2026-06-18｜Charlie Straka (BN Engineering Director)｜customer：Barber-Nichols 工程總監給的太空訂單成長數字（FY25 到 FY26），口徑與 CFO 的 76% 不同（原話："a 70% increase just from FY '25 to FY '26"）
- 2026-06-18｜CEO Matthew Malone｜customer：CEO 說明太空營收占比與訂單／營收脫節的解釋（原話："why is revenue flat? Well, orders are not"）
- 2026-06-18｜CEO Matthew Malone｜customer：CEO 說明國防占公司業務約六成（原話："60% of the portfolio today"）
- 2026-06-18｜Michael Dixon (BN GM)｜customer：國防營收 5 年成長軌跡（約 6,200 萬到 1.47 億，CAGR 24%）（原話："grown from approximately $62 million to $147"）
- 2026-06-18｜Michael Dixon (BN GM)｜competition：國防營收中獨家供應或有顯著競爭優勢的占比（原話："more than 80% of our defense revenue is sole sourced"）
- 2026-06-18｜Michael Dixon (BN GM)｜guidance：管理層列出潛在營收機會 18 億美元（至 2056）（原話："platforms shown here represent approximately $1.8 billion"）
- 2026-06-18｜Michael Dixon (BN GM)｜guidance：管理層稱 18 億機會數字被低估（原話："we believe it understates the future"）
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 說明 18 億機會的計算口徑（以當前價格，未計通膨）（原話："$1.8 billion is at today's prices without any inflation"）
- 2026-06-18｜CEO Matthew Malone｜guidance：CEO 回應分析師：未給數字，僅稱高於簡報所列（原話："it's a number north of what we presented"）
- 2026-06-18｜CEO Matthew Malone｜product：宣布取得 Virginia-class 新增內容的 2,200 萬美元 PO（尚未定價）（原話："$22 million PO, and that PO is undefinitized at this time"）
- 2026-06-18｜CEO Matthew Malone｜competition：此新增內容過去由單一供應商獨家供應，Graham 現在成為競爭者（原話："this has been sole sourced with a single vendor"）
- 2026-06-18｜Michael Dixon (BN GM)｜customer：Dixon 說明 Virginia-class 後續兩艘船訂單已下（原話："Virginia-class subs for orders for the next 2 boats already"）
- 2026-06-18｜CEO Matthew Malone｜customer：CEO 說明目前新內容的量體（2 艘船、4 個冷凝器）（原話："we have 2 boats, which ends up being 4 condensers"）
- 2026-06-18｜Michael Dixon (BN GM)｜capital_allocation：客戶補助金額（供應商開發資金）（原話："our customers of over $29 million"）
- 2026-06-18｜Charlie Straka (BN Engineering Director)｜competition：太空市場競爭節奏：不再是 NASA 式長週期開發（原話："it's a competitive market now. These aren't NASA programs."）
- 2026-06-18｜Charlie Straka (BN Engineering Director)｜product：太空推進市場規模說法（原話："propulsion market alone, $30 billion by 2030"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜product：SMR 對 Graham 的可取得市場規模：大型核電（1GW）（原話："$15 million to $30 million per reactor"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜product：SMR 對 Graham 的可取得市場規模：300MW SMR（原話："somewhere between $5 million and $15 million"）
- 2026-06-18｜CEO Matthew Malone｜guidance：CEO 對 SMR 貢獻時程的說法（原話："that's sort of 5 to 10 years out before it's a"）
- 2026-06-18｜CEO Matthew Malone｜competition：CEO 稱 Graham 在美國真空系統的市占（原話："80% market share in the U.S. on vacuum systems"）
- 2026-06-18｜Royce Roemisch (customer, Delek)｜competition：客戶（煉油專家）估計 Graham 在美國主要真空塔的裝機占比（原話："Graham probably has 85% to 90% installed base"）
- 2026-06-18｜Royce Roemisch (customer, Delek)｜product：客戶描述把競爭對手舊真空系統改裝成 Graham 新技術的成果（原話："was able to get about 25% more capacity going from a"）
- 2026-06-18｜Royce Roemisch (customer, Delek)｜customer：客戶描述美國煉油業的需求型態：以改裝取代新建（原話："They're not building any new refineries in the"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜customer：Will 引用煉油資本支出中用於升級與維護的占比（原話："85% of the capital budgets over the next 20 years are"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜commitment：Will 描述售後市場模式轉變：從被動等電話改為主動出擊（原話："we wait for the phone to ring, we say, what do you need"）
- 2026-06-18｜William Zmyndak (GM, Graham Manufacturing)｜product：新世代噴嘴（NextGen Nozzle）已有安裝（原話："we have the NextGen Nozzle out there"）
- 2026-06-18｜CEO Matthew Malone｜commitment：Malone 稱階段轉換：穩定期結束，進入改善與成長期（敘事）（原話："the stabilized phase is behind us"）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 稱過去四年皆達成對股東的期望（原話："delivered on every expectation that we set for our"）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 稱除 Batavia ERP 外，過去五年計畫項目皆按時按預算完成（原話："which is coming online in August"）
- 2026-06-18｜CIO Keith Oufnac｜commitment：CIO 稱 IT 投資已納入 CapEx 財測並預期報酬率高於 20%（原話："we expect them to generate returns exceeding 20% ROI"）
- 2026-06-18｜CIO Keith Oufnac｜commitment：CMMC 合規時程承諾（原話："We are on track to be compliant by year-end"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CFO 說明 FY26 營運現金流的調整口徑（一次性交易獎金視為購買價格的減項）（原話："operations for fiscal '26 was closer to $20 million"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：FlackTek 原股東交易獎金由 Graham 代付（原話："$4 million of transaction bonuses that were awarded"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：四年財務成長率口徑（營收 CAGR 19%、調整後 EBITDA CAGR 45%）（原話："achieving 19% revenue compounded growth, 45% adjusted"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CFO 說明資本支出投資原則：確信贏得營收才投（原話："only invest in new buildings and equipment"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：FY27 CapEx 財測區間，主因是 Barber-Nichols 新廠（原話："$18 million to $22 million of CapEx spend"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：將在 Arvada 動工興建新廠（原話："break ground on a new 30,000 square foot manufacturing"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：4 月 5,000 萬美元 PIPE 完成並還清負債（原話："the recent $50 million PIPE transaction"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：目前無負債（原話："we are now debt-free as the proceeds from the transaction"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：流動性規模（原話："provides us with over $100 million in liquidity"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CapEx 占營收比的長期原則（原話："spend 7% to 10% of revenue on capital expenditures"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：R&D 占營收比將逐步提高（原話："current 0.5% of revenue to the 1% to 2% of revenue level"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CFO 稱不需要併購就能達成成長目標（原話："need acquisitions to grow"）
- 2026-06-18｜CFO Christopher Thome｜capital_allocation：CFO 描述過去併購節奏（原話："a strategic acquisition every 12 to 18 months"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 說明資本部署的限制：決定因素在領導團隊的承載量，成長若超出 10% 會失去資本部署的紀律（原話："if we exceed that 10% number"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 表示 ROIC 高於 20% 的專案一律執行（原話："the answer is we're going to go do"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 稱限制在於領導團隊承載量而非資本或點子（原話："think it is the capacity of the leadership team to go do"）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 描述 CEO／CFO／董事會的分工，作為資本紀律的說明（原話："I'm the gas. Chris is the break."）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 說明未來將增聘售後加速與全球銷售職位（原話："We have opened the position for the aftermarket"）
- 2026-06-18｜CEO Matthew Malone｜commitment：CEO 說明銷售策略從被動接單轉為主動出擊（商業化）（原話："we are going to go on the offensive with the"）
- 2026-06-18｜Paul Nistler (Motor Controller BU leader)｜product：馬達控制器業務目標：五年內成為獨立事業單位的規模（原話："turn into a $30 million to $50 million business unit"）
- 2026-06-18｜CEO Matthew Malone｜product：電力電子與控制器業務將從 Barber-Nichols 分拆成獨立板塊（原話："controller business out of Barber-Nichols"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜product：FlackTek Mega 機型產能，作為可跟客戶進入量產的新能力（原話："2,000 kilos an hour in our mega machine"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜customer：FlackTek Mega 機型的客戶 Anduril（原話："centerpiece of Anduril's rocket motor production facility"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜customer：FlackTek 裝機基數（原話："over 2,500 machines in the field already"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜competition：FlackTek 稱客戶一旦指定其系統，轉換成本很高（原話："a really high switching cost to get out of that system"）
- 2026-06-18｜Matthew Gross (FlackTek GM)｜customer：FlackTek 耗材（容器）的出貨量（原話："shipped over 3 million containers last year"）
- 2026-06-18｜Daniel Thoren (Business Development)｜risk：國際擴張中的風險：民族主義趨勢與品牌／品質管控（原話："The nationalistic trends are a challenge in some areas."）
- 2026-06-18｜Daniel Thoren (Business Development)｜risk：Thoren 提到在海外營運可能失去品牌、流程與品質掌控（原話："control of our brand and our process and our quality"）
- 2026-06-18｜Daniel Thoren (Business Development)｜commitment：Thoren 稱未來必須在當地設廠（原話："We're just going to have to build in those markets"）
- 2026-06-18｜CEO Matthew Malone｜customer：CEO 說明全球化策略重心在能源與製程（原話："strategy is most focused around energy and process"）
- 2026-06-18｜CFO Christopher Thome｜customer：CFO 說明國防占比偏高的原因，並指出能源與製程的大型資本專案偏慢（原話："large capital projects in our Energy and Process business"）
- 2026-06-18｜CFO Christopher Thome｜guidance：CFO 的長期結構目標：國防與商用各半（原話："have a 50-50 split between defense and commercial"）
- 2026-06-18｜CEO Matthew Malone｜risk：CEO 說明採預收款降低新開發案風險，不先投入自有資本（原話："we're asking for more payment upfront"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 說明目前專案選擇性很高，需求超出可承接量（原話："highly selective of what opportunities we pursue"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 說明事業單位組織願景：5 到 7 個利基事業單位（原話："5 to 7 business units, niche, world-class at what they do"）
- 2026-06-18｜CEO Matthew Malone｜capital_allocation：CEO 提到 Xdot 軸承收購補強 Barber-Nichols 能力（原話："we made the Xdot Bearing acquisition"）

### 問答異常語氣（迴避／改口／保留）
- GHM_Q1_2027_Earnings_Call_20260806.md｜問：Russell Stanley問上週GD與HII大型潛艦合約有多少已在Graham積壓訂單中｜答法：回答「some of them in, some of them not」，未給數字，並表示「I'll keep it high level there」
- GHM_Q1_2027_Earnings_Call_20260806.md｜問：Russell Stanley問彈藥短缺帶來的機會與對Graham的順風程度｜答法：未量化，改談魚雷與FlackTek，稱「I can't talk in too much detail」、「I'll keep it kind of high level」
- GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md｜問：William Blair 的 Jed Dorsheimer 問是否像 GE Vernova 採較高訂金與里程碑付款，以避免閒置產能風險｜答法：CEO 稱「exact same strategy」並說明方向（預收款、國防專案當銀行），未給訂金比例或具體條款數字
- GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md｜問：Northland 的 Bobby Brooks 問若再納入現有能力可承接的其他內容，國防機會（簡報 18 億美元）粗估會多大｜答法：CEO 未給數字，稱「north of what we presented」，並表示需靠執行、數字交給 Will 的團隊去實現；CFO 補充 18 億是以現價、未計通膨
- GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md｜問：Bobby Brooks 追問 FlackTek Mega 機型是否價格很高｜答法：CEO 改談 ROI 與客戶價值（「price is all relative」），未給價格或單台金額，也稱無法談 Anduril 產線的生產數字
- GHM_Analyst_Investor_Day_Graham_Corporation_20260618.md｜問：Bobby Brooks 問 FlackTek 加入後的近期訂單勝利如何加速、具體是什麼｜答法：CEO 說「I can't get into the exact specifics」，列出招聘與關閉管線中的案子，未給金額或客戶名

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 1 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 4 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 4 | 1 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 5 | 2 |
| major_events | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260714","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"國防（Navy）多年 backlog 提供高能見度成長","columns":{"2Y 驗證點":"book-to-bill ≥ 1.0x、backlog 維持 &gt; $450M","5Y 驗證點":"Columbia/Virginia 量產件持續轉收入，國防營收 CAGR ≥ 10%","10Y 驗證點":"下一代平台（SSN(X)/DDG(X)）承接首件","具體數字門檻":"backlog $532.6M、orders $359.4M、book-to-bill 1.5x（FY26）","信息來源":"FY26 8-K（2026-06-08）；10-K FY2026","漂移觸發":"連 2 季 book-to-bill &lt; 1.0x → 削弱（QC-35 2Y 假設）"}},{"id":"H2","text":"Margin 沿多年路徑爬向 mid-teen Adj EBITDA","columns":{"2Y 驗證點":"FY27 Adj EBITDA 12-14% 兌現","5Y 驗證點":"FY29 Adj EBITDA 14-16%（管理層 3 年計畫）","10Y 驗證點":"結構性穩定於 15%+，operating leverage 兌現","具體數字門檻":"FY27 指引 $35-40M（12.1-13.8%）；FY29 目標 14-16%；FY27 GM 指引 24.5-25.5%","信息來源":"FY2027 guidance 8-K；法說（2026-06-08）","漂移觸發":"連 2 季 Adj EBITDA ≤ 10% → 削弱；連 4 季 TTM 偏離 ≥ 5% → 反轉（5Y 假設）"}},{"id":"H3","text":"市場願意為國防超級週期＋margin 兌現維持溢價倍數（估值假設）","columns":{"2Y 驗證點":"Fwd PE 維持 &gt; 35x","5Y 驗證點":"倍數隨成長成熟 de-rate 但守住 &gt; 22x","10Y 驗證點":"穩定於工業複利 20-25x","具體數字門檻":"現價 Fwd PE 45.6x（FY28）；同業/歷史 96th 分位","信息來源":"yfinance 2026-07-13；valueinvesting.io EV/EBITDA 分位","漂移觸發":"倍數壓縮至 &lt; 25x 且 margin 未兌現 → thesis H3 破（估值假設是本案最脆弱一環）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"估值均值回歸：45x → 22-25x 校準（不需基本面惡化）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Fwd PE / EV-EBITDA 分位、共識修正方向","警戒閾值":"共識連 2 季下修 + 倍數破 35x → 減碼訊號（若已持有）"}},{"id":"R2","text":"margin 兌現落後：FlackTek ~10% 稀釋 + 國防 mix 拉低 GM，FY27 Adj EBITDA 停在 10-11%","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 Adj EBITDA margin、GM 軌跡","警戒閾值":"連 2 季 Adj EBITDA ≤ 10% → 大動作重評"}},{"id":"R3","text":"Navy 造艦排程延遲外溢：Columbia 12-16 月、Virginia 24-36 月延遲（CBO/GAO 2026）拖慢 backlog 轉換節奏；及能源大型專案續軟","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"12M-forward 營收 / backlog 比、能源新訂單","警戒閾值":"轉換率 &lt; 35% 且能源訂單連 2 季負 → 下修成長軌跡"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE 回落≤30x（約$68）或 Adj EBITDA margin 連2季≥14% 兌現","irr_base_pct":-0.9,"ev5y_pct":-7.6,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.7,"ev5y_pct":-7.6,"irr_base_pct":-0.9,"max_dd_pct":-62.0,"bull_5y_price":147.0,"bear_5y_price":46.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE 回落≤30x（約$68）或 Adj EBITDA margin 連2季≥14% 兌現","price_at_dd":102.7,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GHM","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Graham Corporation"},"oneliner":"造艦訂單紮實、利潤率正在改善，但 12 個月積壓轉換比例由 35–40% 降到 30–35%，現價 78 美元約為本年度調整後 EPS 43 倍，基準五年年化報酬僅約 2%，等 59 美元以下再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GHM_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺美國海軍造艦預算的錢，錢卡在主承包商下游的單一來源關鍵零組件節點；位置穩，但核心訂單採成本定價，利潤空間有上限。","reasoning":"第二財季營收 69.76M，國防占 66%，積壓訂單 561.3M，其中 83% 屬國防。毛利率 28.2%、GAAP 營業利益率 8.4%，CFO 明說高於正常水準，主因是去年同期約 10M 低毛利物料收入造成低基期。營收年增 6% 全部來自 FlackTek 的 9.5M，扣掉後有機衰退約 9%（60.3M 對 66.0M）；再扣掉去年約 10M 物料收入，有機約增 8%。單點依賴：最終客戶主要是美國海軍，FY2026 前十大客戶占營收 60%，這同時是護城河證據與集中度風險。產業態勢裁決：結構性轉好中，依據是國防積壓 85% 已撥款、造艦為數十年週期；能源與製程營收年減 17%，大型資本專案偏軟，是另一邊的拖累。事實表未涵蓋分部毛利率與前兩大客戶確切占比。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi7_backlog","f_kpi8_book_to_bill"],"verdict_values":{"revenue_quality":"積壓訂單提供高能見度，但單季營收受專案里程碑與物料收入時點影響大。售後銷售 8.6M，占營收約 12%，當季訂單 18.3M，年增 91%，屬品質較好的收入。","unit_econ_note":"許多合約可先向客戶請款買料，營運資金部分由客戶墊付；單一來源潛艦訂單受成本與定價資料法規（TINA）約束，競爭性標案才有較高毛利。","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"營業利益率由 FY2023 的 0.8% 升到 FY2026 的 6.1%，積壓屬多年期，但投入資本報酬事實表未涵蓋，複利品質尚未驗證。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：造艦為數十年週期、國防積壓 85% 已撥款，景氣位置屬擴張；風險在交付節奏拉長，不在需求消失。來源為 2026-11-05 法說。","bargaining":{"up":"原料多元，訂單到手才下單鎖價，上游議價壓力有限；關稅仍會影響高階鋼材與電子元件成本。","down":"海軍與主承包商議價力強，獨家潛艦訂單採成本定價；前十大客戶占營收 60%。","geo":"FY2026 營收 15% 來自美國以外，公司在中國與印度設有銷售與工程支援辦公室。"},"profit_pool_dir":"事實表未涵蓋利潤池資料。","tam_table":{"expanded":false,"reason":"事實表未涵蓋市場規模與滲透率的一致口徑，只有管理層引用的機會金額，無法組成五年利潤池對照。"}}}},"q2_moat":{"verdict":"護城河方向持平：認證與設計導入的地位在加強，定價能力尚未被證明同步擴大。","reasoning":"機制是潛艦零組件的長週期認證與設計導入。Barber-Nichols 總經理在 2026-06-18 投資人日稱逾八成國防營收屬獨家或具顯著優勢；CEO 同日稱美國真空系統市占 80%，客戶 Delek 專家估裝機占比 85–90%。可證方向：MK19 競標勝出、Virginia 級新增內容取得 22M 尚未定價訂單，該內容過去由單一供應商獨家，顯示公司在搶份額。定價端相反：CEO 在 2026-08-06 法說明說潛艦主力是獨家供應但受 TINA 成本定價約束，較高毛利靠競爭性標案。公司毛利率與營業利益率都低於 CW、ESE、DCO，故不給持續擴大。投入資本事實表未涵蓋，無法計算 ROIC 與對最強同業的利差，是本題最大缺口。","fact_refs":["f_peer_ghm_gross_margin_pct","f_peer_ghm_operating_margin_pct","f_peer_cw_gross_margin_pct","f_peer_cw_operating_margin_pct","f_peer_ese_gross_margin_pct","f_peer_dco_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"潛艦與魚雷零組件的長週期認證、設計導入與測試設施，加上美國煉油真空系統裝機基礎帶來的售後收入。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：積壓連七季創高、MK19 競標勝出、Virginia 級新增內容取得訂單。定價面穩定：獨家訂單受成本定價約束，第二財季毛利率上升的主因依 CFO 說法是物料收入基期，定價貢獻尚未量化。兩者合併判為持平。","competitor_notes":[{"name":"CW","strategy_note":"海軍與核電泵閥的大型對手，利潤率遠高於公司，是利潤率上緣參照，但規模與組合不同，不能直接當可達目標。"},{"name":"ESE","strategy_note":"組合偏測試與濾波，利潤率差距主要反映產品組合，參考價值有限。"},{"name":"DCO","strategy_note":"規模與航太國防零組件屬性最接近，毛利率只略高於公司，現金轉換同樣偏弱，說明這類生意的現金流本來就不穩。"}],"peer_na_reason":"投入資本事實表未涵蓋，暫以毛利率與營業利益率差距代替 ROIC 利差。","threats":[{"level":"🟡","text":"低成本或具匯率優勢的對手以價格競爭，主要落在能源與製程的海外專案，海軍獨家品項不受直接影響。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"海軍為擴充工業基礎引入第二來源。Graham 在 Virginia 級新增內容是受益方，同一機制也可能用在自家獨家品項；10-K 也提到客戶可能擔心供應商集中。","p":"25%","evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"低利益率，周轉率事實表未涵蓋；FY2026 營業利益率 6.1%，客戶預付可能拉高周轉，須補投入資本才能定象限。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是海軍，決策者是計畫辦公室與主承包商，付款者是國會撥款。潛艦與魚雷屬必要需求，國防積壓 85% 已撥款；時點會變，需求本身難以延後到消失。"},{"item":"決策層級","level":"🟡","text":"替代要在單一艦級零件層重新認證，週期長，逾八成國防營收屬獨家或具顯著優勢。但 Graham 取得 Virginia 級原獨家內容，證明海軍願意開放來源，這個機制對公司也可逆。"},{"item":"價值鏈分配","level":"🟡","text":"公司站在難取代的環節，但獨家訂單採成本定價，客戶也提供逾 29M 的供應商開發資金，超額利潤多留在買方與主承包商；競爭性雷達與雷射專案才有市場定價。"},{"item":"社會容忍度","level":"🟢","text":"造艦有兩黨支持，定價上限已由 TINA 制度化，公司不靠大幅漲價獲利，出現社會反彈的空間小。"}],"roiic":"事實表未涵蓋實測值；暫以管理層公司層級目標 14% 當上界代理，單案門檻 20% 同屬目標，未見實績。","reinvest_rate":"事實表未涵蓋折舊、營運資金與收購淨額，無法計算；上界代理取 100%。","endo_ceiling":14,"formula_note":"內生成長上界＝14%×100%＝14%，是目標值推出的代理上限，不是實績。公司可靠外部融資或利潤率提升超過此數，但那部分不算內生。基準路徑 EPS 年複合 13.8%，已貼近上界。"}}}},"q3_growth":{"verdict":"跑道中等：未來五年靠積壓與利潤率，第二曲線已有訂單，但規模還撐不起五年後的成長。","reasoning":"上半年營收年增 16%，其中約 13 個百分點來自 FlackTek（16.1M），有機僅約 3%（125.0M 對 121.3M）；管理層三年框架是有機 8–10%，下半年要明顯加速。共識只有兩年：FY1 1.81 美元、FY2 2.28 美元，年增 26%，第三年事實表未涵蓋。對內生上限 14% 的缺口約 12 個百分點，歸因是利潤率擴張，不是再投資。12 個月轉換比例下修後，中值對應金額由約 209M 降到 182M，FY2028 共識營收卻要 322M。第二曲線方面，太空上半年訂單 25M、訂單出貨比 2 倍、積壓年增 108%，但上半年銷售約 12.5M，只占營收 9%；管理層引用的 2030 年推進市場 300 億美元與公司規模相差三個數量級，不能當份額證據。新計畫營收 FY26 約 10M，CFO 目標 FY29 逾 50M；SMR 則由 CEO 自己定位在 5–10 年後。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi0_gaap","f_kpi7_backlog"],"verdict_values":{"growth":{"driver_mix":"上半年以併購為主：16% 成長中約 13 個百分點來自 FlackTek，有機約 3%。框架期內以量與組合為主，定價次之，股數小幅增加。","runway_years":"事實表未涵蓋滲透率，無法換算；造艦屬數十年週期，管理層列出至 2056 年約 18 億美元機會。","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊、營運資金與收購淨額事實表未涵蓋，無法用實測增量報酬×再投資率。改用上界代理：2026-06-18 投資人日公司層級 ROIC 目標 14%×再投資率上限 100%，得 14%，屬目標值而非實績。","segments":[{"item":"國防","value":"第二財季占營收 66%，年增 12%；占積壓 83%，國防積壓年增 10%，已撥款 85%"},{"item":"太空","value":"第二財季營收年增 59%，訂單 10.6M，訂單出貨比 1.7 倍；積壓年增 108%"},{"item":"能源與製程","value":"第二財季營收年減 17%，大型資本專案偏軟，美國以外銷售下降"},{"item":"售後（跨國防與能源）","value":"銷售 8.6M，年減 3%；訂單 18.3M，年增 91%"},{"item":"FlackTek（併入各市場）","value":"第二財季營收 9.5M，第一財季 6.6M；上半年訂單出貨比 1.3 倍"}],"decay_signals":["亮燈：EPS 成長顯著高於營收成長。FY2027 到 FY2028 共識 EPS 增 26%，營收增約 11%，差距來自利潤率假設。","亮燈：自由現金流對淨利轉換率連兩年低於 0.75。FY2025 約 0.44，FY2026 約 −0.01。","未亮燈：毛利率未連兩季年減，第一財季下滑、第二財季上升；SBC 占營收約 1.1%。","事實表未涵蓋：核心市占的量化序列、產業倍數三年趨勢、維護性資本支出占比。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置方向合理，但現金轉換與併購報酬都還沒有可驗證的成績。","reasoning":"FY2026 自由現金流 −0.12M，FY2025 為 5.36M，對淨利轉換率約 −1% 與 44%；CFO 在投資人日稱扣除一次性獎金後營運現金流接近 20M，這項歸因未證，持續監測。第二財季自由現金流 44.5M，管理層自己歸因於應收回收與客戶預付，也說付款時點可讓各季差 5–10M，不能外推。SBC 占營收 1.12%。資金順位是內部投資優先，其次併購，沒有配息或回購。2026-04 以每股 83.36 美元私募 50M，約 13M 還債，目前現金 71M、循環額度可用 75M。FY2027 資本支出展望已調整，新數字不在本包內；上半年只花 4.9M，原指引為 18–22M。FY2026 營收增 16.9%，營業利益由約 15.2M 微降到約 15.0M，營運槓桿為負，本財年上半年才反轉。","fact_refs":["f_kpi4_ocf_capex","f_kpi5_sbc_equity_based_compens","f_net_debt_m","f_shares_diluted_m","f_peer_ghm_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"FlackTek 收購價與收購後投入資本事實表未涵蓋，無法計算已實現增量報酬。投資人日時 CFO 說其調整後 EBITDA 利潤率約 10%，低於公司平均。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"公司沒有回購，2026-04 反而增發 599,808 股。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第二財季 SBC 0.782M，年化約 3.1M，對市值 915.8M 約 0.34%，低於每年 1.5% 上限；私募增發約 5% 屬融資，另行揭露。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"公司無配息與回購，併購金額事實表未涵蓋，無法組成回報表。"}}}},"q5_valuation":{"verdict":"現價要求五年後調整後 EPS 到 4.6 美元才有 8% 年化，接近多頭路徑，我不把它當基準。","reasoning":"78.02 美元對應本年度共識 EPS 43.1 倍、下年度 34.2 倍。以終端 25 倍計，要賺年化 8%，FY2032 調整後 EPS 需約 4.6 美元，五年複合 20%，接近多頭情境的 4.90 美元；管理層框架外推的基準路徑只有 3.45 美元。賣方目標價 81.67 到 135 美元都高於現價，但最新資料點仍早於這次法說，且各來源時點不一，不足以支持現在進場。共識快照在財報後兩天取得且沒有變動，可能尚未反映 12 個月轉換比例下修。RSI 54.81 未過熱，26 週跌 20.54%，股價低於 52 週均線 86.01；四週漂移事實表未涵蓋，所以過熱欄留空。同業預估倍數事實表也未涵蓋，終端倍數缺少同業現值對照。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_rsi14","f_week26_return_pct","f_ma_w52","f_pe_percentile","f_ps_percentile","f_ev_s_percentile"],"verdict_values":{"valuation":{"basis":"調整後 EPS 的預估本益比，FY2027E 為起點、FY2032E 為終端，兩端同口徑。","tier":"小型利基國防零組件","peers":{"expanded":false,"reason":"事實表的同業表只有利潤率，沒有同業預估倍數，無法組成同層級估值對照。"},"fwd_pe":43.1,"peg":2.6,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"43.1 倍本年度調整後 EPS，PEG 約 2.6，高於 2 倍的偏貴線；成長率用基準路徑 FY2027 到 FY2030 年複合 16.3%，因共識沒有第三年。基準五年年化約 2%，機率加權終值約 89 美元，高於現價 14%，上下行比約 1.6。較前份的很貴改善，但仍未達 8% 最低要求，故判偏貴。真正五年分位事實表沒有，只有 3 到 4 個年度端點的分位 81 到 92，不能當五年分位。","targets":{"short":{"price":67.5,"basis":"FY2028 基準 EPS 2.25 美元×30 倍"},"mid":{"price":79.8,"basis":"FY2030 基準 EPS 2.85 美元×28 倍"}},"upside_short_pct":-13.5,"upside_mid_pct":2.3,"denominator_disputed":true,"denominator_note":"共識 1.81 美元應屬調整後口徑，這是推論：上半年 GAAP EPS 僅 0.72 美元，指引隱含下半年調整後 EBITDA 中值 18.4M，低於上半年 19.1M，全年不可能到 GAAP 1.81 美元。43.1 倍與 Trailing 67.84 倍口徑不同。公司約每 12–18 個月併購一次，攤銷與整合費用的加回具重複性，便宜論點不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯的方向有兩個：低估利潤率持續性，或低估積壓拉長的傷害；目前判價值陷阱風險中等。","reasoning":"看錯在偏空的一邊：若舊單出清與競爭性專案使毛利率長期站上 26%，基準 EPS 太低。看錯在偏多的一邊：12 個月轉換比例下修如果代表造艦交付延後，FY2028 共識營收 322M 就過高。敏感度：FY2032 利潤率每 100 個基點影響 EPS 約 0.21 美元，目標價約 5 美元；每年有機成長每 1 個百分點影響目標價約 4 美元；終端倍數每 1 倍影響約 3.5 美元。第二財季法說中，分析師問非海軍國防訂單占比，CFO 改談售後與太空，沒有回答；轉換比例下修也沒有解釋。前一季對 GD 與 HII 合約納入積壓的比例同樣未給數字。歷史最大回撤與投入資本事實表未涵蓋。","fact_refs":["f_kpi7_backlog","f_kpi4_ocf_capex","f_net_debt_m","f_price_at_dd","f_rev_consensus_fy2_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度：成長由併購與利潤率預期支撐，現金轉換待驗證"}}}},"scenario_inputs":{"terminal_label":"FY2032E","start":{"eps":1.81,"pe":43.1,"basis":"FY2027E（3 月底財年）共識調整後 EPS；終端倍數同為當年度調整後 EPS 的預估本益比"},"eps":{"bull":[2.45,3.05,3.65,4.25,4.9],"base":[2.25,2.58,2.85,3.15,3.45],"bear":[1.85,1.9,1.98,2.05,2.1]},"pe":{"bull":32,"base":25,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":8},"max_dd":{"lo":-65,"hi":-45,"basis":"以調整後 EPS 回算：本年度 EPS 1.81 美元×25 倍約 45 美元，跌 42%；空頭 EPS 1.63 美元×18 到 20 倍約 29 到 33 美元，跌 58% 到 63%；空頭終點跌約 52%。範圍取 −45% 到 −65%。歷史最大回撤事實表未涵蓋，前份單點估計為 −62%。","trigger_time":null},"basis":{"bull":"FY2032 營收約 520M，太空與 FlackTek 放量，調整後 EBITDA 利潤率達 18%，以 32 倍計；同業預估倍數事實表未涵蓋。","base":"FY2029 達管理層框架中段，之後營收年增 7–8%，FY2032 營收約 431M、利潤率 16.5%，以 25 倍計；同業預估倍數事實表未涵蓋。","bear":"轉換拉長、利潤率停在 12–13%，營收年增 5–6%，FY2032 EPS 2.10 美元，以 18 倍計；機率 30% 反映共識成長超過內生上限與 12 個月轉換比例下修。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"12 個月轉換比例由 35–40% 降到 30–35%；上半年有機成長約 3%；第二財季毛利率 28.2% 被 CFO 說成高於正常水準；國防占積壓 83%。","assumption":"多頭假設轉換拉長只是訂單結構問題，利潤率提升可以延續。","consequence":"五年後虧 50% 最可能的路徑：利潤率停在 12–13%、營收年增 5–6%、EPS 約 2.10 美元、倍數回到 18 倍，股價約 38 美元。","ruling":"採納，列入 30% 空頭機率，與唯一致命點屬同一條故事線，不另立事件。","watch":"12 個月轉換金額、調整後 EBITDA 利潤率、FY2029 框架措辭","evidence_refs":[],"fact_refs":["f_kpi1_gaap","f_kpi7_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"FY2026 營收增 16.9%，自由現金流 −0.12M；截至 2026-06 的 TTM 自由現金流利潤率 −2.34%。管理層原則是資本支出占營收 7–10%、併購約每 12–18 個月一件；潛艦主力受成本定價約束；2026-04 增發約 5% 股本。","assumption":"成長與利潤率達標就會轉成每股現金。","consequence":"營收與利潤率都達標，但資本支出、併購與增發吃掉現金，每股自由現金流落後調整後 EPS，投資人買到的是加回攤銷後的數字。","ruling":"部分採納。第二財季現金流反彈多為時點因素，不足以反駁；終端倍數壓到 25 倍已反映此項。","watch":"兩個完整財年合計自由現金流對淨利轉換率是否達 0.75 以上；併購的已實現報酬","evidence_refs":[],"fact_refs":["f_peer_ghm_fcf_margin_pct","f_kpi4_ocf_capex"]},{"view":"價格已反映太多","evidence":"本年度調整後 EPS 43.1 倍，Trailing GAAP 67.84 倍；股價 26 週跌 20.54% 後，基準路徑五年年化仍約 2%。","assumption":"市場會繼續為國防長週期與利潤率提升支付高倍數。","consequence":"即使 FY2029 框架全數達成，倍數回到 25 倍也會吃掉大部分 EPS 成長：EPS 年複合 13.8%，倍數年化約 −10%。","ruling":"採納，這是本次不追的唯一約束。","watch":"下年度本益比與 59 美元價位","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 102.7 → 本次 78.02（-24.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=102.7","side_b":"本次 price_at_dd=78.02","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 102.7 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 102.7 美元：Bull 價 147、Bear 價 46，五年期望值 −7.6%，基準年化 −0.9%，不對稱比 0.7","side_b":"本次情境、股價仍用 102.7 美元：Bull 價 156.8、Bear 價 37.8，五年期望值 −13.0%，基準年化 −3.4%，不對稱比 0.69","ruling":"先換情境、股價不動：五年期望值少 5.4 個百分點，基準年化少 2.5 個百分點。不對稱比由 0.7 變為 0.69。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 102.7 美元：五年期望值 −13.0%，基準年化 −3.4%，不對稱比 0.69","side_b":"本次情境、股價 78.02 美元：五年期望值 +14.5%，基準年化 2.0%，不對稱比 1.63","ruling":"再換股價、情境不動：起點價下跌 24.0%，五年期望值多 27.5 個百分點，基準年化多 5.5 個百分點，不對稱比由 0.69 升到 1.63。合計五年期望值比前份多 22.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率改善來源","cause":"新證據","prior_field":null,"side_a":"CEO（2026-11-05 法說）：執行改善、舊低毛利單出清、定價轉好與組合共同貢獻。","side_b":"CFO（2026-11-05 法說）：毛利率高於正常水準，影響最大的是物料收入減少，全年會回到較正常水準；全年指引只上調 50 個基點。","ruling":"程度差異，可調和，採 CFO 版本，執行改善列為未證、持續監測。指引隱含下半年毛利率約 24.5%，低於上半年 26.6%。CFO 在 2026-06-18 投資人日說 FlackTek 調整後 EBITDA 利潤率約 10%，低於公司平均；最新法說講的是對毛利率有加分，EBITDA 層是否轉為增益，事實表未涵蓋。","evidence_level":"管理層原話與指引推算","settle_metric":"第三、四財季毛利率","if_then":["若第三、四財季毛利率都在 26% 以上，上修基準 EPS 並重算進場價，價格未到仍不追。","若連兩季低於 25%，視同執行改善的歸因被證偽，空頭機率升到 35%，不追。"],"evidence_refs":[]},{"axis":"積壓創高與近端轉換下修","cause":"新證據","prior_field":null,"side_a":"CFO（2026-06-18 與 2026-08-06）：積壓 35–40% 在 12 個月內轉營收；投資人日稱約 30% 要 2 年以上。","side_b":"CFO（2026-11-05）：改為 30–35%，1–2 年 20–25%，其餘超過 2 年，隱含 40–50%；法說沒有解釋，也沒有分析師追問。","ruling":"可調和但對股東不利：訂單還在，只是更長。中值算 12 個月金額由約 209M 降到 182M，對 FY2028 共識營收 322M 幫助變小。前份造艦延遲風險的條件中，轉換率低於 35% 已成立，能源訂單連兩季負事實表未涵蓋。這項利空只有三天，賣方模型多半未反映，判斷下修一級，第三財季法說前不加碼。","evidence_level":"管理層原話與推算","settle_metric":"12 個月轉換比例與對應金額","if_then":["若連兩季低於 180M，下修 FY2028 營收與基準 EPS，不追。","若回到 200M 以上且第三財季營收達 65M 以上，上修基準路徑後重算進場價。"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1"]},{"axis":"現在就買的最強論證","cause":"價格變動","prior_field":null,"side_a":"股價自前份下跌 24%，第二財季調整後 EBITDA 利潤率 14.8%，已進入 FY2029 目標區間；積壓連七季創高，國防積壓 85% 已撥款；淨現金 65M；T. Rowe Price 帳戶四月以 83.36 美元認購，高於現價。","side_b":"14.8% 含物料收入基期效果；指引隱含下半年僅約 12.3%；基準五年年化約 2%，要賺 8% 得靠接近多頭路徑的 EPS；機構認購價不是估值依據。","ruling":"可調和，差異在價格，不在公司品質。裁定不追，約束只有股價。","evidence_level":"財報、指引推算與情境樹","settle_metric":"股價相對 59 美元，以及連兩季利潤率","if_then":["價格先走證據未到：股價續漲而利潤率與轉換比例沒有改善，不追。","股價跌到 59 美元以下且基本面無損，重跑分析後分批反買。","反向條件：連兩季利潤率 14% 以上且 12 個月轉換金額回到 200M 以上，上修基準路徑後重算進場價。"],"evidence_refs":[]},{"axis":"GD 與 HII 合約的性質","cause":"新證據","prior_field":null,"side_a":"二手法說摘要把 GD 與 HII 的獎項寫成競爭對手得標，列為負面。","side_b":"2026-08-06 法說問答中，分析師問的是 GD 與 HII 大型潛艦合約有多少已進 Graham 積壓，CEO 答部分在內、部分不在，未給數字。","ruling":"採後者，兩家在此是潛艦合約方，屬客戶鏈上游，不把此項當份額流失。納入積壓的金額仍是資料缺口。同一摘要提到的 Batavia ERP 切換風險另列觸發條件。","evidence_level":"二手摘要與問答紀錄對照，原文未附","settle_metric":"公司揭露相關合約納入積壓的金額","if_then":["若後續揭露競爭對手確實取得 Graham 原有品項，護城河方向改判下降，不追。"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"估值與裁決漂移","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份：股價 102.7 美元，估值很貴，裁決觀望，綜合評等 B。","side_b":"本次：股價 78.02 美元，下年度本益比由 45.6 倍降到 34.2 倍，估值降為偏貴，綜合評等維持 B。","ruling":"改善來自股價下跌，不是盈餘預期大幅上修；FY1 共識近三個月僅上修 1.12%。基準報酬仍低於 8%，不足以改變不追的結論。","evidence_level":"事實表價格與共識","settle_metric":"基準五年年化報酬是否達 8%","if_then":["股價到 59 美元以下才重跑分析。"],"evidence_refs":[]},{"axis":"護城河、成長跑道與價值陷阱漂移","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap"],"side_a":"前份：護城河持平、成長跑道中等、價值陷阱風險中等。","side_b":"本次三項結論不變。新增正面證據是 Virginia 級新增內容與太空訂單；新增負面證據是轉換拉長與上半年有機成長偏低。","ruling":"正負相抵，維持原結論。太空只占上半年營收 9%，還不足以把跑道調升。","evidence_level":"法說與投資人日","settle_metric":"太空年訂單、新計畫營收、自由現金流轉換率","if_then":["若 FY2029 新計畫營收達 50M 以上且太空年訂單達 50M 以上，跑道改判寬。"],"evidence_refs":[]},{"axis":"情境機率與回撤範圍漂移","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 25%、空頭 30%、最大回撤單點 −62%。","side_b":"本次：多頭 25%、空頭 30%、最大回撤改為 −65% 到 −45% 的範圍。","ruling":"機率不變，因為利潤率改善與轉換拉長相互抵銷；回撤改用範圍表達，下緣依調整後 EPS 與空頭倍數回算。","evidence_level":"情境推算，歷史回撤事實表未涵蓋","settle_metric":"實際回撤與空頭路徑 EPS","if_then":["若 12 個月轉換金額連兩季低於 180M，空頭機率升到 35%。"],"evidence_refs":[]},{"axis":"公司分類與循環位置漂移","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份：品質複利成長，未設循環位置。","side_b":"本次分類不變，信心列為中；仍不適用循環位置。","ruling":"分類維持，因為其他類別更不貼近；但投入資本報酬未驗證，所以不給高信心。","evidence_level":"財務史與事實表缺口","settle_metric":"補齊投入資本後的 ROIC","if_then":["若實測 ROIC 長期低於 10%，改列轉機類重新評估。"],"evidence_refs":[]},{"axis":"進場首倉條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"Fwd PE 回落≤30x（約$68）或 Adj EBITDA margin 連2季≥14% 兌現","side_b":"股價回落至 59 美元以下（約 FY2028 共識 EPS 26 倍，基準五年年化報酬升到 8%）後重跑分析，再建首倉","ruling":"舊門檻 68 美元對應基準年化僅約 5%，改用 8% 最低報酬反推。利潤率連兩季達標改列假設驗證，用來上修基準路徑，不再單獨構成建首倉條件，因為 14.8% 含基期效果。","evidence_level":"情境推算","settle_metric":"股價與基準五年年化報酬","if_then":["觸發後重跑分析，不直接建倉。"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）。","side_b":"管理層下修或撤回 FY2029 三年框架（營收 340–350M、調整後 EBITDA 50–55M）","ruling":"本次補上單一事件。框架下修同時影響利潤率與倍數這兩個最大敏感項。","evidence_level":"投資人日與法說框架","settle_metric":"法說對框架的措辭與 FY2028 指引","if_then":["框架下修時，未持有就移出名單並重做分析；已持有則減碼一半，下一季再確認就清倉。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設量化出場指標；風險門檻為共識連 2 季下修且倍數破 35 倍、連 2 季 Adj EBITDA ≤10%、轉換率低於 35% 且能源訂單連 2 季為負。","side_b":"本次：共識連 2 季下修且下年度本益比破 30 倍；連 2 季調整後 EBITDA 利潤率低於 12%；12 個月轉換金額連 2 季低於 180M；國防積壓已撥款比例低於 75%；FY2029 框架下修。","ruling":"下年度本益比已 34.2 倍，舊的 35 倍線已穿過而共識未下修，失去警示力，故改 30 倍。利潤率門檻由 10% 提高到 12%，因 FY2027 指引區間已高於舊線。轉換率改用金額，因比例已低於 35%，而能源訂單資料事實表未涵蓋。達門檻時依各條規定不追、減碼或清倉。","evidence_level":"法說與事實表","settle_metric":"各量化指標","if_then":["轉換金額與利潤率兩項同時觸發時，已持有部位減碼一半。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回落到基準五年年化報酬達 8% 的價位，重跑分析後才建首倉。","type":"估值rearm","maps_to":"R1","metric":"股價","threshold":"59 美元以下","action":"重跑分析後分批反買，第一筆小倉位","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"利潤率連兩季達到框架區間，用來上修基準路徑。","type":"假設驗證","maps_to":"H2","metric":"調整後 EBITDA 利潤率","threshold":"連 2 季 14% 以上；第一財季 12.3%、第二財季 14.8%","action":"上修基準 EPS 並重算進場價，價格未到仍不追","source_freq":"每季財報","date":"2027-02","evidence_refs":[]},{"n":3,"text":"近端積壓轉換是否恢復。","type":"假設驗證","maps_to":"H1","metric":"12 個月積壓轉換金額","threshold":"200M 以上為恢復；連 2 季低於 180M 為轉弱","action":"轉弱時不追並下修 FY2028 營收；恢復時重算進場價","source_freq":"每季法說","date":"2027-02","evidence_refs":[]},{"n":4,"text":"Batavia ERP 切換造成開票延後，營收過度集中到第四財季。","type":"風險","maps_to":"R5","metric":"第三財季營收","threshold":"低於 65M，或全年營收指引下修","action":"不追；已持有且指引下修則減碼一半","source_freq":"每季財報","date":"2027-02","evidence_refs":["supply_demand_durability#2"]},{"n":5,"text":"關稅成本吸收失敗。FY2026 增量成本約 1M，管理層先前估計曾由不重大上調到 1.0–1.5M，10-K 也列出鋼材與電子元件風險。","type":"風險","maps_to":"R2","metric":"FY2027 毛利率與全年關稅增量","threshold":"毛利率低於 25%，或關稅增量高於 2M","action":"停止加碼並下修 FY2028 EPS","source_freq":"每季財報與 10-K","date":"2027-06","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0"]},{"n":6,"text":"印度子公司吹哨者案已自願通報當地主管機關、美國 DOJ 與 SEC；受影響營收與結案時點事實表未涵蓋。","type":"風險","maps_to":"R6","metric":"執法程序性質與和解金額","threshold":"進入刑事程序或承包資格受限；民事和解超過 6.5M","action":"刑事程序或資格受限即清倉；民事和解超過門檻則減碼一半","source_freq":"10-Q、10-K 與 8-K","date":null,"evidence_refs":["regulatory_antitrust#0"]},{"n":7,"text":"管理層下修或撤回 FY2029 三年框架。","type":"Single Thing","maps_to":"Single Thing","metric":"FY2029 營收與調整後 EBITDA 目標","threshold":"低於 340M 或 50M，或撤回框架","action":"未持有則移出名單；已持有則減碼一半，下一季再確認就清倉","source_freq":"法說與投資人日","date":"2027-06","evidence_refs":[]},{"n":8,"text":"海軍撥款或造艦計畫中斷。國防占營收約六成，最終客戶高度集中。","type":"風險","maps_to":"R3","metric":"國防積壓已撥款比例","threshold":"低於 75%；目前 85%","action":"已持有則減碼一半；未持有則不追","source_freq":"每季法說","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":9,"text":"第三財季財報後複審毛利率、轉換比例與營收。","type":"複審日期","maps_to":"H1","metric":"第三財季財報","threshold":"財報後一週內完成","action":"依結果維持不追或重算進場價","source_freq":"一次性","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"12 個月積壓轉換金額（積壓×轉換比例中值）","bear_threshold":"連 2 季低於 180M","window":"2 季","source":"每季財報法說","last_status":"warning"},{"metric":"調整後 EBITDA 利潤率","bear_threshold":"連 2 季低於 12%","window":"2 季","source":"每季新聞稿","last_status":"ok"},{"metric":"全年訂單出貨比","bear_threshold":"全年低於 1.0 倍","window":"1 財年","source":"每季新聞稿","last_status":"ok"},{"metric":"國防積壓已撥款比例","bear_threshold":"低於 75%","window":"每季","source":"每季法說","last_status":"ok"},{"metric":"FY2029 三年框架","bear_threshold":"下修或撤回","window":"12–24 個月","source":"法說與投資人日","last_status":"ok"}],"evidence_dismissed":[{"ref":"substitute_technology#0","reason":"這段是 10-K 的通用風險文字，只寫 bladeless mixer 產業，沒有指名任何技術、對手或流失案例；同軸另一筆搜尋也未見取代蒸汽噴射器的技術報導。"}],"action_conditions":{"rearm_trigger":"股價回落至 59 美元以下（約 FY2028 共識 EPS 26 倍，基準五年年化報酬升到 8%）後重跑分析，再建首倉","exec_line":"現價 78.02 美元不追，約束只有價格。跌到 59 美元以下且基本面無損，才重跑分析並分批建倉；第三財季法說前不加碼。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方目標價都早於 2026-11-05 法說，推論模型多半還用 35–40% 的 12 個月轉換比例與較高倍數；本分析認為近端營收與終端倍數都偏樂觀。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不追，等股價回落至 59 美元以下並重跑分析；若連兩季利潤率 14% 以上且 12 個月轉換金額回到 200M 以上，先上修基準路徑再重算進場價。"},"thesis":{"H":[{"id":"H1","text":"國防與太空積壓訂單能按期轉成營收，有機成長回到 8–10%。","2y":"FY2027 營收落在 285–295M，FY2028 達 315M 以上，全年訂單出貨比不低於 1.1 倍。","5y":"FY2032 營收達 430M，國防營收年複合 8% 以上。","10y":"下一代潛艦平台取得首件內容，投資人日所列約 18 億美元機會持續轉成訂單。","threshold":"12 個月轉換金額不低於 200M，目前 182M；有機營收年增 8–10%，上半年約 3%。","source":"每季新聞稿與法說；2026-11-05 CFO 轉換比例；2026-06-18 投資人日框架","drift_rule":"2 年目標連 2 季偏離 5% 以上為削弱，連 3 季偏離 10% 以上為反轉。"},{"id":"H2","text":"利潤率提升來自舊低毛利單出清與執行改善，不只是物料收入基期。","2y":"FY2027 調整後 EBITDA 35–40M，FY2028 利潤率達 14% 以上。","5y":"FY2029 利潤率 14–16%（50–55M），FY2032 達 16.5%。","10y":"長期穩定在 17–18%，符合管理層所說同業前四分之一。","threshold":"下半年毛利率不低於指引隱含的 24.5%；連兩季調整後 EBITDA 利潤率 14% 以上，第一財季 12.3%、第二財季 14.8%。","source":"每季新聞稿；2026-11-05 CFO 毛利率說明；2026-06-18 投資人日","drift_rule":"5 年路徑 TTM 利潤率連 4 季偏離 5% 以上為削弱，連 6 季偏離 10% 以上為反轉。"},{"id":"H3","text":"太空、FlackTek 與售後形成第二曲線，撐起 FY2029 之後的成長。","2y":"太空年訂單 50M 以上；FlackTek 訂單出貨比不低於 1.1 倍；售後單季訂單維持 10M 以上。","5y":"新計畫營收 FY2029 超過 50M，FY2026 約 10M；國防占積壓由 83% 降到 70% 以下。","10y":"國防與商用接近各半。","threshold":"太空上半年訂單 25M；FlackTek 上半年訂單出貨比 1.3 倍；第二財季售後訂單 18.3M。","source":"每季法說；2026-06-18 投資人日 CFO 與 FlackTek 總經理發言","drift_rule":"5 年目標連 4 季偏離 5% 以上為削弱，連 6 季偏離 10% 以上為反轉。"}],"R":[{"id":"R1","text":"倍數回落：不需要基本面惡化，43 倍也可能回到 25–30 倍。","h_ref":"H2","clock":"⚡","threshold":"FY1 共識連 2 季下修，且下年度本益比跌破 30 倍。","evidence_refs":[]},{"id":"R2","text":"利潤率只是基期效果：第二財季 28.2% 回落後，執行改善不如管理層所說。","h_ref":"H2","clock":"🔥","threshold":"連 2 季調整後 EBITDA 利潤率低於 12%，或 FY2027 毛利率低於 25%。","evidence_refs":[]},{"id":"R3","text":"海軍單一終端客戶：撥款或造艦進度中斷，FY2026 前十大客戶占 60%，國防占營收 60%。","h_ref":"H1","clock":"🐢","threshold":"國防積壓已撥款比例低於 75%，或前十大客戶占比升到 70% 以上。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R4","text":"積壓拉長：總額持續創高，但 12 個月內可認列金額下降。","h_ref":"H1","clock":"🔥","threshold":"12 個月轉換金額連 2 季低於 180M。","evidence_refs":[]},{"id":"R5","text":"Batavia 系統切換與下半年營收後段集中。CEO 在 2026-06-18 投資人日說 ERP 八月上線，2026-08-06 法說摘要改為第三財季，2026-11-05 法說未更新進度。","h_ref":"H1","clock":"⚡","threshold":"第三財季營收低於 65M，或 FY2027 營收指引下修。","evidence_refs":["supply_demand_durability#2"]},{"id":"R6","text":"印度子公司吹哨者案演變成正式執法，影響國防承包資格。","h_ref":"H1","clock":"🐢","threshold":"進入刑事程序或承包資格受限。","evidence_refs":["regulatory_antitrust#0"]}],"single_thing":{"description":"管理層下修或撤回 FY2029 三年框架（營收 340–350M、調整後 EBITDA 50–55M）","why_fatal":"框架下修同時打到最大的兩個敏感項：利潤率每 100 個基點影響 FY2032 目標價約 5 美元，倍數每 1 倍影響約 3.5 美元。一旦確認，基準路徑會滑向 EPS 2.10 美元與 18 倍的空頭路徑。","if_happens":"未持有就移出名單並重做分析；已持有則減碼一半，下一季再確認就清倉。","how_monitor":"每季法說的框架措辭、2027 年 6 月前後的 FY2028 指引、12 個月轉換比例。","probability":"未來 12–24 個月約 20%"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":34.2,"peg_fy2":2.1,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":1.12,"FY2027E":1.81,"FY2028E":2.28},"fy_end_month":3,"eps_basis":"FY2026A 為 GAAP 稀釋 EPS；FY2027E 與 FY2028E 為共識，依上半年 GAAP 0.72 美元與指引推論屬調整後口徑，基期與預估口徑不同。第三年共識事實表未涵蓋。"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"Batavia 新 ERP 第三財季切換期","impact":"中","watch":"開票是否延後、第三財季營收是否低於 65M"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第三財季財報，全年指引是否維持","impact":"高","watch":"營收、毛利率是否守住 24.5%、12 個月轉換比例"},{"date":"2027-06","date_precision":"month","type":"guidance","event":"FY2027 全年財報與 FY2028 指引","impact":"高","watch":"FY2028 營收指引與共識 322M 的落差、三年框架措辭"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方目標價都早於 2026-11-05 法說，推論模型多半還用 35–40% 的 12 個月轉換比例與較高倍數；本分析認為近端營收與終端倍數都偏樂觀。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=-20.54, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
