你是 DD 管線 v20 的判斷層閘（gate），標的 SEZL（20261005）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、裁決、角色）。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_total_revenue_gaap`（q1_business）｜Total revenue (GAAP)＝149.7 USD million｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：市場彙整稿稱優於預期約 $14.6M（預期約 $135.1M；二手來源，未經 IR 稿驗證）
- `f_kpi1_gaap_operating_income`（q1_business）｜GAAP operating income＝55.0 USD million｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：查無
- `f_kpi2_net_income_gaap`（q1_business）｜Net income (GAAP)＝40.8 USD million｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：查無
- `f_kpi3_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司未揭露 Non-GAAP 營業利益，以此代替）＝58.0 USD million｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：查無
- `f_kpi7_active_subscribers`（q1_business）｜Active subscribers＝854000 人｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：查無
- `f_kpi8_gross_merchandise_volume`（q1_business）｜Gross merchandise volume (GMV)＝1.3 USD billion｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：查無
- `f_kpi6_full_year_2026_guidance`（q1_business）｜Full-year 2026 guidance（上調）＝185.0 USD million（Adjusted net income）｜期間與口徑：Q2 FY2026（公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026（公告於 2026-08-06））
  - 註記：Adjusted EPS 指引 $5.25 vs 站內共識 FY1 EPS $5.26（consensus_revision，口徑未必相同）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-06 date｜期間與口徑：2026-08-06／距今 42 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-06）
- `f_peer_sezl_gross_margin_pct`（q2_moat）｜SEZL 毛利率＝72.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SEZL.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_sezl_operating_margin_pct`（q2_moat）｜SEZL 營業利益率＝37.78 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SEZL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_sezl_fcf_margin_pct`（q2_moat）｜SEZL FCF 利潤率＝51.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SEZL.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_afrm_gross_margin_pct`（q2_moat）｜AFRM 毛利率＝68.07 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AFRM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_afrm_operating_margin_pct`（q2_moat）｜AFRM 營業利益率＝20.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AFRM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_afrm_fcf_margin_pct`（q2_moat）｜AFRM FCF 利潤率＝23.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AFRM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pypl_gross_margin_pct`（q2_moat）｜PYPL 毛利率＝45.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pypl_operating_margin_pct`（q2_moat）｜PYPL 營業利益率＝18.41 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pypl_fcf_margin_pct`（q2_moat）｜PYPL FCF 利潤率＝19.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.26 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-09-26）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.65 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-09-26）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝7.95 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-09-26）
- `f_kpi4_free_cash_flow`（q1_business）｜Free cash flow（僅上半年累計，無單季）＝140.4 USD million｜期間與口徑：H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[4]，as_of H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06））
  - 註記：查無
- `f_kpi5_stock_based_compensation`（q1_business）｜Stock-based compensation（僅上半年累計）＝3.4 USD million｜期間與口徑：H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Sezzle Reports Second Quarter 2026 Results（GlobeNewswire）（numbers.latest_quarter_kpis.items[5]，as_of H1 FY2026（2026-01-01 至 2026-06-30，公告於 2026-08-06））
  - 註記：查無
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝110.85 USD｜期間與口徑：2026-10-05（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-05（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝24.31 x｜期間與口徑：2026-10-05（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-05（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-05（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-05（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝7.02 x｜期間與口徑：2026-10-05（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-05（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-05（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-05（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝7.1 x｜期間與口徑：2026-10-05（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-05（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-05（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-05（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.42 x｜期間與口徑：2026-09-26／分母＝FY1 EPS 5.26，分子＝快照價 107.41｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-09-26）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-09-26／兩份 Koyfin 快照之間的 EPS 修正幅度（5.26 → 5.26）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-09-26）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝3.14 %｜期間與口徑：2026-06-23 → 2026-09-26／FY1 共識 EPS 5.1 → 5.26（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-09-26）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝68.46 %｜期間與口徑：2026-10-05（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-05（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝37.57｜期間與口徑：2026-10-05（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-05（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：2026 Q2 財報優於預期但警告下半年營收成長放緩，盤前股價跌 23%（as_of 為約略月份，確切日期未讀到）
  - 來源：Yahoo Finance: Sezzle Shares Tumble Despite Strong Quarter as Growth Outlook Disappoints（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：競爭威脅：搜尋摘要指 Chase、Citi 等銀行發展 BNPL 產品（信用卡額度轉分期、固定手續費），以及 Apple、PayPal 等大型科技整合先買後付；Affirm、Klarna、Afterpay 規模與零售整合較深（二手彙整，未見具名 2026 新進入者）
  - 來源：搜尋彙整（businessmodelcanvastemplate 等）（as_of 2026-08-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Sezzle 8-K（2026-05）披露的融資concentration limit：單一商家（Target Corporation 除外）上限 15.0%，Target 上限 35.0%，顯示 Target 為最大商家集中點。
  - 來源：Sezzle Inc. Form 8-K FY2026 (ex10.1, 2026-05-07)（as_of 2026-05-07）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Sezzle 面臨企業級商家費率的顯著競爭壓力；2025-03 Klarna 取代 Affirm 成為 Walmart 獨家 BNPL 供應商，顯示供給端競爭仍在重分配。
  - 來源：CSIMarket SEZL Competitors／Business Strategy Hub 彙整搜尋摘要（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R、moat_trend
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：有律所公告調查 Sezzle 等 BNPL 業者是否就逾期費、付款時點、透支風險或分期真實成本誤導消費者（非政府機關調查）。
  - 來源：Migliaccio & Rathod LLP: Sezzle Buy Now Pay Later Investigation（as_of 2026-07-07）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：多家律所2026-05公告調查 Sezzle 及部分高管／董事是否涉證券詐欺或其他不當行為（證券訴訟調查，非反壟斷）。
  - 來源：Pomerantz Law Firm via Morningstar/PR Newswire（as_of 2026-05-14）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：SEZL 10-K 風險因子：與發卡銀行夥伴的協議為非獨家，且在特定事件發生時發卡夥伴可終止（融資/發卡環節的單點依賴）。
  - 來源：Sezzle Inc. Form 10-K FY2025（SEC EDGAR）（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：SEZL 10-K 風險因子：重要供應商含雲端資料儲存、IT 方案與支付處理；服務中斷或供應商錯誤可能使其無法處理交易或入帳。
  - 來源：Sezzle Inc. Form 10-K FY2025（SEC EDGAR）（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：SEZL 10-K 風險因子：相當比重的業務與交易量集中在少數大型電商平台，任一平台不再合作或轉投競爭者會不成比例地衝擊公司。
  - 來源：Sezzle Inc. Form 10-K FY2025（SEC EDGAR）（as_of 2025-12-31）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Sezzle 風險揭露稱 BNPL 與其他替代支付產品的採用增加，可能吸引大型金融機構、卡網與科技公司進入，對方規模與品牌較強，可能迫使 Sezzle 降低商家費率或加碼誘因。
  - 來源：gloom.sh Sezzle 2026 risk factors（搜尋摘要，轉述 Sezzle 風險因子）（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-04-30 起多家律所（Pomerantz、Schall、Levi & Korsinsky、Block & Leviton、Lowey Dannenberg 等）公告調查 Sezzle 是否涉證券詐欺；為調查公告，非已提起之集體訴訟
  - 來源：Pomerantz 新聞稿（Morningstar/PR Newswire）（as_of 2026-04-30）｜affects：decision_inputs.bear、thesis.R
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2026-04-09 SEC 文件揭露董事 Karen Webster（審計與風險、薪酬、提名治理委員會成員）立即請辭，理由為與管理層在公司方向、關鍵決策與治理上的觀點分歧
  - 來源：Sezzle 8-K（2026-04-09）／律所公告引述（as_of 2026-04-09）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：多家律所自 2026-04 起公告調查 Sezzle 證券詐欺；本次搜尋未見已提起之集體訴訟
  - 來源：Pomerantz 新聞稿（Morningstar/PR Newswire）（as_of 2026-04-30）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261005/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":276.0,"bear_5y_price":54.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":40.7,"ev5y_pct":40.2,"irr_base_pct":7.1,"asym_ratio":2.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.26,"pe":21.07,"basis":"FY2026E 共識 EPS（Koyfin 2026-09-26）；終端倍數套在終端年當年度 EPS，口徑同為 FY1"},"eps":{"bull":[6.9,8.5,10.2,12.0,13.8],"base":[6.5,7.6,8.6,9.55,10.4],"bear":[5.3,5.0,5.2,5.6,6.0]},"pe":{"bull":20,"base":15,"bear":9},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.6},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SEZL_Q1_2026_Earnings_Call_20260506.md
- 2026-05-06｜CEO Charles Youakim｜guidance：全年營收成長財測由 25–30% 上調至 30–35%（原話："from 25% to 30% to a new range of 30% to 35%."）
- 2026-05-06｜CEO Charles Youakim｜guidance：調整後淨利財測上調 1,000 萬美元至 1.8 億美元（原話："adjusted net income guidance by $10 million to $180 million"）
- 2026-05-06｜CEO Charles Youakim｜guidance：調整後 EPS 財測由 4.70 升至 5.10，管理層稱部分來自第一季回購（原話："$5.10 from $4.70 with some benefit from repurchase activity"）
- 2026-05-06｜CFO Lee Brading｜guidance：CFO 說明財測不含開發中新產品的預測（原話："guidance does not reflect any projections for new products"）
- 2026-05-06｜CEO Charles Youakim｜guidance：CEO 說明財測含 Pay-in-5，但 Sezzle Mobile 不在預測內（原話："that's not anything we're projecting at this point"）
- 2026-05-06｜CFO Lee Brading｜guidance：CFO 說下一季營收收益率的比較基期較容易（原話："we'll have an easier comp from a revenue yield"）
- 2026-05-06｜CFO Lee Brading｜margin：管理層目標：信用損失提列佔 GMV 2.5%–3%（原話："provision for credit losses in the 2.5% to 3% of GMV range"）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 提醒 74% 單位經濟毛利率因季節性不可年化（原話："annualize a unit economic margin of 74%, we can't."）
- 2026-05-06｜CFO Lee Brading｜margin：營收減交易相關成本的長期目標區間 55%–65%（原話："transaction-related costs in the 55% to 65% range."）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 稱該利潤率一直落在區間偏高端（原話："we've definitely been trending on the higher end of that"）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 稱未必會把本季這種信用損失優於預期的幅度計入未來（原話："necessarily booking in that same kind of outperformance"）
- 2026-05-06｜CEO Charles Youakim｜margin：CEO 解釋本季提列受前期高估估計回沖影響（原話："we had overestimation leaks in the first quarter"）
- 2026-05-06｜CEO Charles Youakim｜margin：CEO 重申全年提列率計畫維持 2.5%–3%（原話："still to see 2.5% to 3% for the provision for the year"）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 說 Pay-in-5 初期損失率可能略高（原話："initially a little higher loss rates on that as well"）
- 2026-05-06｜CFO Lee Brading｜margin：CFO 拆解年增收益率下滑 80bp 的原因（原話："revenue yield declined 80 basis points due to the mix"）
- 2026-05-06｜CFO Lee Brading｜commitment：CFO 稱預期持續提高非交易相關營運費用的槓桿（原話："continue to leverage our nontransaction-related OpEx"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱行銷支出預期逐季上升（原話："we expect it to continue to rise quarter-on-quarter"）
- 2026-05-06｜CFO Lee Brading｜commitment：CFO 稱預計 2026 年年中提交銀行執照申請（原話："We anticipate submitting our application"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱現金流管理產品預計三個月內較大規模推出（原話："we plan to launch here in the next few months"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱支票帳戶產品也將在未來幾個月內推出（原話："that's another product coming in the next few months as well"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱路線圖產品預計 2027 年底前完成推出並放量（原話："launched and scaling by the end of 2027"）
- 2026-05-06｜CEO Charles Youakim｜commitment：CEO 稱到 2027 年底一定會有存款帳戶（原話："We'll definitely have the deposit accounts in place by then."）
- 2026-05-06｜CFO Lee Brading｜capital_allocation：第一季回購 2,480 萬美元普通股（原話："repurchasing $24.8 million worth of common stock"）
- 2026-05-06｜CFO Lee Brading｜capital_allocation：季末現金 1.474 億美元（含受限現金 2,690 萬）（原話："we ended the quarter with $147.4 million in cash,"）
- 2026-05-06｜CFO Lee Brading｜capital_allocation：信貸額度明年四月到期，正進行再融資（原話："refinancing our current credit facility, which matures next April."）
- 2026-05-06｜CFO Lee Brading｜capital_allocation：行銷支出年增超過一倍（原話："spend more than doubled year-over-year in the quarter."）
- 2026-05-06｜CEO Charles Youakim｜capital_allocation：CEO 稱行銷回收期仍短於 6 個月（句子接下一行）（原話："we continue to see a payback period of less"）
- 2026-05-06｜CEO Charles Youakim｜capital_allocation：銀行執照可把銀行夥伴的變動成本轉為固定成本（原話："it does move a variable cost stream to a fixed cost stream"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 認為 Pay-in-5 是未來一年最重要的產品，因已有成效（原話："it's already proven to have results for us"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 稱 Sezzle Mobile 設計目的在留存而非營收（原話："not really designed to drive revenue, gross margin"）
- 2026-05-06｜CEO Charles Youakim｜product：加拿大虛擬卡尚未完整上線，加拿大約占 10% 交易量（原話："it's also in Canada, which is 10% of our volume"）
- 2026-05-06｜CFO Lee Brading｜product：Pagaya 合作為按交易量收取費率，Sezzle 不分擔風險（原話："We're not sharing in the risk on that product"）
- 2026-05-06｜CEO Charles Youakim｜product：AI 客服機器人解決約六到七成對話無需轉人工（原話："approximately 60% to 70% of the chats without escalation"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 稱約八成程式碼由 AI 產出、人工審閱（原話："upwards of 80% of our code"）
- 2026-05-06｜CEO Charles Youakim｜product：管理層稱 AI 讓費用成長維持遠低於營收成長（原話："while keeping expense growth well below revenue growth"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 說自己不再只是 Pay-in-4 公司（敘事擴張）（原話："we are no longer just a Pay-in-4 company"）
- 2026-05-06｜CEO Charles Youakim｜product：CEO 說 2026 年策略是不再只在結帳時被想到（原話："moving beyond being a product consumers think about"）
- 2026-05-06｜CEO Charles Youakim｜competition：CEO 預期 BNPL 像信用卡一樣從封閉迴路走向開放迴路（原話："more and more and more open loop"）
- 2026-05-06｜CFO Lee Brading｜competition：CFO 稱特約商戶已成為較不重要的業務，主要作為獲客管道（原話："it's becoming a less important part of our"）
- 2026-05-06｜CFO Lee Brading｜risk：CFO 稱反壟斷訴訟進行中、無法進一步說明（原話："Our antitrust suit is currently ongoing"）
- 2026-05-06｜CFO Lee Brading｜risk：CFO 稱銀行執照程序漫長且不保證成功（原話："We recognize this process is long and not guaranteed"）
- 2026-05-06｜CEO Charles Youakim｜risk：CEO 稱部分州與監管機關在削弱銀行夥伴模式（原話："chopping away at the bank partnership model"）
- 2026-05-06｜CFO Lee Brading｜risk：CFO 稱未見消費者異常壓力（原話："we are not seeing any unusual strains on the consumer"）
- 2026-05-06｜CEO Charles Youakim｜customer：訂閱用戶增加 4.4 萬至 71.4 萬（原話："total subscribers increasing by 44,000 to"）
- 2026-05-06｜CEO Charles Youakim｜customer：每季平均購買頻率達 7.1 次（去年同期 6.1 次）（原話："reaching 7.1x in the quarter"）
- 2026-05-06｜CEO Charles Youakim｜customer：CEO 稱客群在數字中看不到宏觀壓力（回應油價問題）（原話："we're just not seeing anything"）
- 2026-05-06｜CEO Charles Youakim｜customer：管理層稱主要獲客管道包含連網電視廣告的擴張（原話："We're pushing more into connected TV"）

### 問答異常語氣（迴避／改口／保留）
- SEZL_Q1_2026_Earnings_Call_20260506.md｜問：Kyle Peterson（Needham）問信用損失優於預期，有沒有上行空間、何時回到區間｜答法：CEO 與 CFO 都以季節性、前期估計回沖、新用戶與 Pay-in-5 為由重申 2.5%–3%，未給任何超出區間的數字或上行空間；語氣為 comfortable
- SEZL_Q1_2026_Earnings_Call_20260506.md｜問：Hoang Nguyen（TD Cowen）問銀行執照能讓 Sezzle 推出哪些現在做不到的產品｜答法：CEO 回答 Not necessarily，改談監管防禦與成本結構（變動轉固定），未直接列出可新增的產品
- SEZL_Q1_2026_Earnings_Call_20260506.md｜問：Hal Goetsch（B. Riley）問低收入客群面對油價與可負擔性壓力，即時看到什麼｜答法：CEO 以自己的推測回應（自稱 just postulating），未給具體即時數據

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 3 |
| customer_second_source | found | 2 | 3 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 3 | 4 |
| regulatory_antitrust | found | 4 | 3 |
| reg_tariff_export | none | 0 | 2 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 1 | 5 |
| substitute_technology | found | 2 | 4 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **reg_tariff_export**（none）（沿用 SEZL_20261005，0d）：Sezzle SEZL tariff 2026；Sezzle buy now pay later merchants tariff impact consumer spending 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260710","verdict":"觀望","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"BNPL 信用週期不反轉，SEZL 承保維持品質：provision/GMV 維持在低檔，不因放款簿老化爆雷","columns":{"2Y 驗證點":"FY26-27 連季 provision/GMV ≤ 2.0%；30+ DPD","5Y 驗證點":"2027-2030 穿越一次完整信用週期，provision peak","10Y 驗證點":"跨多次週期維持 net loss ratio 低且承保演算法持續優化","具體數字門檻":"Q1 FY26 provision 1.2% of GMV（$13.7M）；漂移門檻 provision/GMV 連 2 季 ≥ 2.0%","信息來源":"Q1 FY26 press release／8-K；AFRM/PYPL 歷史 peer benchmark；TransUnion 2026 Q1 次級信用趨勢","漂移觸發":"連 2 季 TTM provision/GMV ≥ 2.0% → 削弱；連 3 季 ≥ 3.0% 或撥備增速連 2 季超前 GMV 增速 → 反轉"}},{"id":"H2","text":"訂閱＋購買頻率動能持續，subscription pivot moat 兌現，且不被監管壓垮","columns":{"2Y 驗證點":"FY26-27 Active Subscribers YoY ≥ +30%；購買頻率維持 7x+","5Y 驗證點":"訂閱佔營收比顯著提升、ARPU 上行，且 NY／州級監管未把訂閱費實質納入利率上限","10Y 驗證點":"訂閱成為結構性黏著層，會員基數規模化","具體數字門檻":"Q1 FY26 Active Subscribers +48.4%、購買頻率 7.1x（+1.0x YoY）、MODS 887K（+34.8%）","信息來源":"Q1 FY26 press release；NY DFS BNPL 規則草案（2026-02，Davis Wright／Orrick 法律分析）","漂移觸發":"Active Subscribers YoY"}},{"id":"H3","text":"Utah ILC 銀行牌照開放存款第二曲線，把 funding cost 從 ~12% revolving 降到 ~4% deposit","columns":{"2Y 驗證點":"2026 正式向 Utah DFI 送件；FDIC 接受文件","5Y 驗證點":"FY28-29 charter approval、checking/savings 上線","10Y 驗證點":"完整銀行 stack ＋自有存款 funding base","具體數字門檻":"截至 2026-04，CEO 表示「尚未正式送件、不預期今年內獲批」；同業 ILC 案審核期常 2-3 年","信息來源":"Banking Dive（2026）ILC 報導；Youakim 公開表態","漂移觸發":"2026 年底前未送件 → 削弱；申請被拒 → 反轉。時程已較前次 DD「18 個月內」大幅拉長，本假設降權為選擇權而非基準"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"信用週期正常化——BNPL loss rate 升向 3-4%；次級放款簿老化使 vintage 違約現形","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"provision/GMV；30+ DPD；撥備增速 vs GMV 增速差","警戒閾值":"provision/GMV 連 2 季 ≥ 2.0%；單季 ≥ 3.0%；30+ DPD > 5%"}},{"id":"R2","text":"監管——NY／州級把訂閱費納入 16% 利率上限，壓縮 H2 訂閱引擎的 take rate；其他州跟進","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"NY DFS 規則定稿內容與生效時點（定稿後 180 天生效）；其他州立法","警戒閾值":"NY 定稿把訂閱費實質納入 APR；≥2 個大州跟進"}},{"id":"R3","text":"治理升級——集體訴訟正式起訴並取得程序進展、SEC 執法、或 CEO 質押強平引發賣壓","columns":{"對應假設":"H1+H2","時間尺度":"🐢 長期（2+ 年慢變數）／⚡ 質押強平為短期尾部","監測指標":"訴訟 docket 進展；SEC 動作；股價相對 CEO 質押抵押水位","警戒閾值":"任一集體訴訟通過程序認證；SEC 正式調查；股價急跌觸發保證金追繳"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"估值回落至 Fwd PE ~20x（$130-140），或治理與監管明朗（集體訴訟撤銷＋NY BNPL 規則以可承受形式定稿＋Utah ILC 正式送件）","irr_base_pct":6.0,"ev5y_pct":29.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"核心","signal":"B","val":"🟠","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.9,"ev5y_pct":29.0,"irr_base_pct":6.0,"max_dd_pct":-65.0,"bull_5y_price":388.0,"bear_5y_price":83.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"估值回落至 Fwd PE ~20x（$130-140），或治理與監管明朗（集體訴訟撤銷＋NY BNPL 規則以可承受形式定稿＋Utah ILC 正式送件）","price_at_dd":177.08,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SEZL","date":"2026-10-05","schema":"v15.2","contract":"v19","company_name":"Sezzle Inc."},"oneliner":"交易量與訂閱戶仍在高速成長，股價三個月跌 37% 後 FY2 本益比約 17 倍；真正的考題是下半年新客湧入後的信用損失，等第三季提列守住全年 3% 再進場","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261005/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261005/scenario.json","answers":{"q1_business":{"verdict":"向商家收交易費、向消費者收訂閱費與服務費；錢卡在承保這一節——營收扣掉交易成本、信用損失與利息後還剩 63.5%，賺多賺少取決於新客的損失率","reasoning":"第二季（2026-06 季末）營收 1.497 億美元（年增 51.7%）、GAAP 營業利益 5,500 萬（營益率 36.7%）、淨利 4,080 萬（27.2%）、調整後 EBITDA 5,800 萬；交易量 13 億美元（年增 37.9%），活躍訂閱戶 85.4 萬（年增 76.4%）。TTM 毛利率 72.4%、營益率 37.8%。收益率（營收÷交易量）11.7%，公司預估全年回到 2025 年的 11.4%，第四季是季節低點。公司不揭露營收分部，訂閱與隨選的營收拆分事實表未涵蓋。單點依賴：2025、2024 年無單一對象占營收 10% 以上，但 2026-05 信用額度合約把 Target 的應收上限訂在 35%、其他單一商家 15%，Target 是最大商家集中點；發卡銀行夥伴非獨家且特定事件可終止，是另一個單點。產業時鐘判在擴張期（II）：美國先買後付市場 2026 年預估 +14.7%、2027 年 +11.9%，仍有雙位數成長但逐年放緩，來源稱放緩來自成熟而非景氣。供需持久性：需求面結構性持久（資金吃緊的消費者需要把支出攤平），但信用供給可逆性高——承保一收緊交易量就會掉，這是空頭機率的來源。","fact_refs":["f_kpi0_total_revenue_gaap","f_kpi1_gaap_operating_income","f_kpi2_net_income_gaap","f_kpi3_adjusted_ebitda_non_gaap","f_kpi7_active_subscribers","f_kpi8_gross_merchandise_volume","f_kpi6_full_year_2026_guidance","f_earnings_recency","f_peer_sezl_gross_margin_pct","f_peer_sezl_operating_margin_pct"],"verdict_values":{"revenue_quality":"商家交易費＋消費者訂閱與服務費；收益率 11.4–11.7%，第一季高、第四季低的季節性明確；SezzleCash 與 Pagaya 合作會拉低收益率但利潤率相近（第二季法說 CFO）","unit_econ_note":"行銷回收期低於 6 個月是管理層自述，事實表未獨立驗證；第二季行銷 1,940 萬美元是刻意測試上限，管理層說第三季核心行銷會降","archetype":{"primary":"品質複利成長","secondary":"金融","confidence":"中","fingerprint":"高利潤率＋短天期消費信貸，盈餘品質跟信用週期連動"},"industry":{"clock_phase":"II","sd_verdict_source":"美國先買後付市場 2026 年 1,116 億美元（+14.7%）、2027 年 1,248 億美元（+11.9%），成長率自 2025 年 20.4% 逐年放緩（eMarketer 彙整）","bargaining":{"up":"上游是發卡銀行夥伴（非獨家、特定事件可終止）、新的 3 億美元信用額度、支付處理與雲端供應商；銀行執照若取得可把銀行夥伴的變動成本轉為固定","down":"商家可同時上架多家先買後付，企業商家壓費率（Klarna 拿下 Walmart 獨家為例）；消費者端靠訂閱綁住，回購用戶占訂單 97.2%","geo":"以美國為主，加拿大約占一成交易量（第一季法說）"},"profit_pool_dir":"CEO 稱份額主要從區域銀行與信用合作社拿，而非同業；屬管理層說法，事實表沒有獨立份額數據","tam_table":[{"item":"美國先買後付市場 2026E","value":"1,116 億美元，年增 14.7%（eMarketer 彙整）"},{"item":"美國先買後付市場 2027E","value":"1,248 億美元，年增 11.9%"},{"item":"2025 年六大業者放款總額","value":"1,567 億美元；Afterpay 537 億、Affirm 413 億、PayPal 265 億、Klarna 239 億、Sezzle 39 億（約 2.5%）"},{"item":"口徑提醒","value":"放款總額含較長天期貸款，與市場規模口徑不同，兩組數字不能直接相除算滲透率"},{"item":"利潤池占比 5 年前→現","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向穩定（→）：執行面在擴大，訂閱戶年增 76%、購買頻率 7.2 次；定價面持平偏受壓，全年收益率持平、企業商家壓費率，兩者相抵判穩定","reasoning":"機制：訂閱制把一次性結帳工具變成每月付費的關係，加上短天期承保資料與低成本營運。可證方向：同業 ROIC 事實表未涵蓋，改用利潤率對照——TTM 營業利益率 Sezzle 37.8% 對 Affirm 20.4%、PayPal 18.4%，FCF 利潤率 51.1% 對 23.3%、19.3%；自身營益率從 2023 年 13.9%、2024 年 25.3%、2025 年 36.2% 升到 TTM 37.8%，但同業歷史值事實表未涵蓋，無法判斷差距是否擴大。執行力 8 分：產品節奏快（SezzleCash 六月分階段上線、Sezzle Send 預定八月上線，後者大部分由 AI 寫成），AI 客服分流 68% 消費者進線。定價力 6 分：全年收益率持平於 11.4%，管理層用隨選方案給薄利企業商家較低價格換取上架，新產品收益率較低。產業態勢判雙向拉鋸：競爭面 Klarna 取得 Walmart 獨家、銀行與大型科技把分期內嵌進卡片與錢包；結構面商家改為多家並列（總裁 Paradis 稱過去兩三年開始和其他業者並列上架），訂閱讓 Sezzle 往開放式支付走、對單一平台依賴下降；其他面 Shopify 反壟斷案核心主張續行、證據開示到 2027 年，州級監管在削弱銀行夥伴模式。威脅都在點對點層級，不扣分。","fact_refs":["f_peer_sezl_gross_margin_pct","f_peer_sezl_operating_margin_pct","f_peer_sezl_fcf_margin_pct","f_peer_afrm_gross_margin_pct","f_peer_afrm_operating_margin_pct","f_peer_afrm_fcf_margin_pct","f_peer_pypl_gross_margin_pct","f_peer_pypl_operating_margin_pct","f_peer_pypl_fcf_margin_pct","f_kpi7_active_subscribers"],"verdict_values":{"moat":{"mechanism":"訂閱綁定（每月付費＋信用額度隨使用累積）＋短天期承保資料＋低成本營運","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行擴大：活躍訂閱戶 85.4 萬（+76.4%）、季購買頻率 7.2 次（去年 6.1）、新增 Poshmark、Gymshark、Debenhams 等企業商家；定價受壓：全年收益率預估持平 11.4%、企業商家費率競爭、新產品收益率較低。未見最大客戶份額下滑的證據（Target 續約、導入第二家或自建的報導都查無）","competitor_notes":[{"name":"AFRM","strategy_note":"2025 年放款 413 億美元，規模約 Sezzle 十倍；營業利益率 20.4% 約為 Sezzle 一半，跟 Sezzle 正面交鋒在企業商家通路"},{"name":"PYPL","strategy_note":"Pay in 4 內建在錢包裡，2025 年放款 265 億美元；毛利率 45.8%，靠錢包分發取勝，是結帳端與錢包端的主要對手"},{"name":"Klarna","strategy_note":"2025-03 取代 Affirm 成為 Walmart 獨家供應商，說明大商家獨家權仍在重新分配；2025 年放款 239 億美元"},{"name":"Afterpay（Block）","strategy_note":"2025 年放款 537 億美元，六家中最大"},{"name":"Chase、Citi 等銀行","strategy_note":"把信用卡額度轉成固定手續費分期，主攻有卡族；CEO 稱 Sezzle 的份額主要從區域銀行拿，客群重疊有限，但屬管理層說法"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋；Klarna、Afterpay 無利潤率資料，只以放款規模對照","threats":[{"level":"🟡","text":"大型電商平台集中：10-K 稱相當比重交易量集中在少數大平台，任一平台終止或改投對手會不成比例衝擊；Sezzle 控告 Shopify 壟斷說明平台擠壓已發生。訂閱與虛擬卡讓依賴下降，CFO 稱特約商戶已成次要的獲客管道","p":"25%","evidence_refs":["geo_supply_chain#2"]},{"level":"🟡","text":"銀行、卡網與大型科技把分期內嵌進信用卡與錢包，品牌與規模較強，可能逼 Sezzle 降商家費率或加碼誘因；屬破壞性競爭，機率取下限 30%","p":"30%","evidence_refs":["competitive_share_entrants#4","substitute_technology#0"]},{"level":"🟡","text":"企業商家費率競爭：Klarna 拿下 Walmart 獨家；Sezzle 以較低價格爭取企業商家，收益率承壓","p":"35%","evidence_refs":["supply_demand_durability#2"]},{"level":"🟡","text":"最大商家集中：信用額度合約允許 Target 應收占比達 35%，Target 若導入第二家或自建分期，交易量與應收同時受衝擊；目前查無相關報導","p":"10%","evidence_refs":["customer_second_source#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（營益率 37.8%；投入資本事實表未涵蓋，周轉率未量化，短天期應收結構支持高周轉）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者與付款者分開看：消費者付訂閱與服務費、商家付交易費，兩端都在付錢。需求是把支出攤平的現金流需要，屬「需要」而非「想要」；購買頻率 7.2 次、回購訂單占 97.2%、約一成新訂閱戶第一筆就用 SezzleCash，代理變數都指向持續使用。急迫性不等於持久性——景氣轉弱時需求更高、還款能力卻更差"},{"item":"決策層級","level":"🟡","text":"替代性要看消費者這一層：同時下載幾家先買後付很容易，轉換摩擦主要是月訂閱與累積的信用額度；商家層已改成多家並列，總裁稱企業商家過去只選一家、現在加第二第三家。漲價後流失率、分客群訂閱續訂率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"淨交易利潤率 63.5% 說明 Sezzle 目前留下大部分價值，但關鍵互補環節集中：發卡銀行夥伴非獨家且可終止、資金端靠信用額度、大平台握有結帳入口（Shopify 訴訟即為例）。國家銀行執照若在 12–18 個月內取得，可把銀行夥伴環節收回自己手上"},{"item":"社會容忍度","level":"🟡","text":"客群是重視價格、資金吃緊的消費者，產品正從購物分期擴到現金預支（SezzleCash）與點對點轉帳分期，這類收費最容易被監管與訴訟盯上：有律所調查是否誤導逾期費與真實成本，CFPB 已向六大業者取得資料，CEO 也說部分州在削弱銀行夥伴模式。CFPB 撤回限制性規則讓壓力暫緩，所以判黃不判紅；依賴授權的部分要看銀行執照與州法走向"}],"roiic":"事實表未涵蓋（投入資本、應收帳款餘額未收錄）；二手轉述 ROE 91.9% 只作方向參考","reinvest_rate":"事實表未涵蓋（應收帳款擴張的現金流分類、回購總額皆未收錄）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩個輸入都缺，不推估。替代觀察：2024→2025 淨利增加 5,461 萬美元（7,852 萬→1.3313 億），同期營收增加 1.79 億，增量淨利率約 30%，顯示新增業務的報酬沒有被稀釋"}}}},"q3_growth":{"verdict":"長期跑道中等（🟡）：美國先買後付市場成熟放緩、Sezzle 份額約 2.5%，第二曲線（SezzleCash、Sezzle Send、銀行執照）方向明確但財測完全沒算進去，還不能當成下一條成長曲線","reasoning":"成長主要靠量：交易量年增 37.9%、訂閱戶年增 76.4%；價為輔：每位變現用戶季營收年增 16.2%。分析師拆算第二季營收成長約三分之二來自用戶數、三分之一來自單用戶營收，CEO 未否認但說不看這個拆法。回購貢獻小（第一季 2,480 萬美元）。共識 EPS：FY2026E 5.26、FY2027E 6.65、FY2028E 7.95，以 2025 年 GAAP 稀釋 EPS 3.72 為基期，三年年複合 28.8%（7.95÷3.72 開三次方減 1）；Koyfin 共識家數事實表未載，評等端約 6–7 位分析師。內生上界算不出（投入資本與再投資率事實表未涵蓋），缺口無法歸因，依規則標為依賴重估、長期信心上限中；但基準情境終端倍數低於現值，報酬不靠倍數擴張。2026 年 EPS +41% 對營收 +35%，差 6pp，亮起一個衰退信號（來自利潤率擴張與回購）。下半年營收成長從第二季 51.7% 降到約 30%，CFO 歸因於第二季收益率低基期，交易量增速才是需求的真實速度。跑道年數：先買後付占電商支付的滲透率事實表未涵蓋，無法算到 30% 的年數。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi7_active_subscribers","f_kpi8_gross_merchandise_volume","f_kpi6_full_year_2026_guidance","f_kpi0_total_revenue_gaap"],"verdict_values":{"growth":{"driver_mix":"量為主（訂閱戶、購買頻率）、價為輔（每位變現用戶季營收 +16.2%）；無併購、回購小","runway_years":"事實表未涵蓋（滲透率資料缺）","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、應收帳款餘額與再投資率事實表未涵蓋，內生上界不推估；替代觀察為 2024→2025 增量淨利率約 30%（淨利增 5,461 萬÷營收增 1.79 億）","segments":{"expanded":false,"reason":"公司不揭露營收分部，營收以交易量×收益率呈現；訂閱與隨選的拆分事實表未涵蓋，無法展開"},"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差逾 5pp）","lit":true,"evidence":"2026 年共識 EPS +41%（3.72→5.26）對營收財測 +35%"},{"signal":"毛利率連兩季年減","lit":false,"evidence":"第二季淨交易利潤率年增 240bp 至 63.5%"},{"signal":"FCF／淨利低於 0.75 連兩年","lit":false,"evidence":"2024 年 1.65 倍、2025 年 1.56 倍（現金流分類未驗證）"},{"signal":"SBC／營收高於 5% 且上升","lit":false,"evidence":"上半年 SBC 340 萬美元，僅第二季營收就有 1.497 億"},{"signal":"TAM 萎縮或被替代","lit":false,"evidence":"美國市場仍 +11.9%～+14.7%，放緩但未萎縮"},{"signal":"核心市占近 12 個月縮減","lit":null,"evidence":"事實表未涵蓋份額時間序列"},{"signal":"產業估值倍數三年系統性下移","lit":null,"evidence":"事實表未涵蓋"}]}}},"q4_capital":{"verdict":"資本配置中等：股權稀釋很低是唯一可判定的加分，回購效益資料不足、無併購","reasoning":"現金轉換：2024 年 FCF／淨利 1.65 倍、2025 年 1.56 倍，上半年 FCF 1.404 億美元；但 FCF 口徑是否已扣除應收帳款擴張事實表未涵蓋，不拿來當再投資證據。SBC 上半年 340 萬美元，年化約 680 萬，對約 39 億美元市值（110.85 美元×約 3,520 萬股，股數由調整後淨利 1.85 億÷EPS 5.25 推得）約 0.2%，稀釋過關。回購：第一季買回 2,480 萬美元（第一季法說 CFO），回購均價與十年期殖利率事實表未涵蓋，效益無法判定。併購：無。資產負債：季末流動性逾 2.05 億美元（現金＋新的 3 億美元信用額度可用額度），總負債÷TTM 調整後 EBITDA 0.5 倍、負債÷股東權益 0.5 倍；舊額度原訂 2027 年 4 月到期，已換成新額度。現金去向四分的三年數字事實表未涵蓋。","fact_refs":["f_kpi4_free_cash_flow","f_kpi5_stock_based_compensation","f_kpi2_net_income_gaap","f_kpi6_full_year_2026_guidance"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"無併購"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"第一季回購 2,480 萬美元；回購均價與十年期殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"上半年 SBC 340 萬美元，年化對市值約 0.2%，遠低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有放款與訂閱，沒有併購；回購金額小（第一季 2,480 萬美元），不承重"}}}},"q5_valuation":{"verdict":"現價要求 2027–2028 年 EPS 大致照共識走（6.65、7.95）且終端倍數不低於 15 倍，才有年化 7–8% 的報酬；我信成長，但不信目前的信用損失率能原封不動延續，所以判合理、不便宜","reasoning":"現價 110.85 美元，FY1 本益比 21.1 倍、FY2 16.7 倍、trailing 24.3 倍，市銷率 7.0 倍、EV／營收 7.1 倍；trailing 本益比與市銷率都在 3–4 個年度端點的最高位置，但樣本太少，不代表五年分位。PEG 0.73（21.1 倍÷28.8%），改用 FY1→FY3 共識年複合 22.9% 算為 0.92，兩種算法都低於 1。FY1 共識近三個月上修 3.1%，最近兩份快照之間持平。賣方平均目標價各站 146.5–171.6 美元（日期不一），現價低於全部區間，方向上不支持更悲觀的看法；最高最低比 196÷150＝1.3 倍，不需下調信心。26 週報酬 +68.5%、RSI 37.6，動能不過熱。分母口徑：淨利與調整後淨利差距小，分母不是爭點，但分母對提列率很敏感。同業倍數事實表未涵蓋，終端倍數改以自身現值錨定。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"FY1／FY2 本益比與 PEG，並給消費金融折價","peers":{"expanded":false,"reason":"事實表同業對照只含利潤率，未含同業本益比，不以 AFRM、PYPL 倍數當錨"},"fwd_pe":21.07,"peg":0.73,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 21.1 倍（110.85÷5.26）、FY2 16.7 倍；PEG 0.73 屬便宜區。但 trailing 本益比、市銷率都在年度端點最高位置，盈餘來自信用損失偏低的順風期、未經壓力測試，給消費金融折價後判合理。五年分位無法計算：事實表只有 3–4 個年度端點，不外推。一年上檔：FY2027E 基準 EPS 6.50×19.5 倍＝126.8 美元，+14.4%；五年上檔：FY2031E 基準 EPS 10.40×15 倍＝156 美元，+40.7%","upside_short_pct":14.4,"upside_mid_pct":40.7,"denominator_disputed":false,"denominator_note":"淨利與調整後淨利差距小（CFO 稱主要是個別稅項），分母口徑不構成爭點；但提列每多 1pp GMV 約吃掉兩成淨利，分母對信用週期高度敏感"}}},"q6_how_wrong":{"verdict":"最可能看錯在信用：下半年創紀錄的新客與兩項新放款產品把提列推出全年 2.5–3% 區間；其次是治理雜音從律所調查變成正式訴訟","reasoning":"反證都寫在反證紀錄：論點失敗看信用與治理、股東經濟變差看收益率與費率、價格已反映看盈餘分母。第一季法說有三處沒正面回答：信用損失優於預期有無上行空間（只重申 2.5–3%）、銀行執照能新增哪些產品（CEO 回答不一定，改談監管防禦）、低收入客群面對油價壓力的即時數據（CEO 自稱只是推測），三題都指向同一件事——管理層對信用與監管的說法缺少可驗證數字。價值陷阱風險判中：衰退信號只亮一個，但信用週期未經壓力測試、審計委員會成員以治理分歧辭職。","fact_refs":["f_kpi6_full_year_2026_guidance","f_price_at_dd","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"信用週期未經壓力測試＋治理雜音"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.26,"pe":21.07,"basis":"FY2026E 共識 EPS（Koyfin 2026-09-26）；終端倍數套在終端年當年度 EPS，口徑同為 FY1"},"eps":{"bull":[6.9,8.5,10.2,12.0,13.8],"base":[6.5,7.6,8.6,9.55,10.4],"bear":[5.3,5.0,5.2,5.6,6.0]},"pe":{"bull":20,"base":15,"bear":9},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.6},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-70,"hi":-55,"basis":"空頭終點 −51%（6.00×9 倍＝54 美元）是區間上緣參考；過去三個月股價由 177.08 美元跌到 110.85 美元（−37%），第二季財報後盤前單日 −23%；短天期消費信貸、上市歷史短，提列區間一旦上調會同時壓 EPS 與倍數，路徑回撤可比終點更深，取 −55%～−70%。屬深回撤，論點未破時不因波動砍倉","trigger_time":null},"basis":{"bull":"訂閱戶維持 30% 以上成長、SezzleCash 與 Sezzle Send 進入財測、2028 年前取得銀行執照降低資金成本；EPS 年增 31%→15%，終端 20 倍（不高於現值 FY1 21 倍）","base":"FY2027–2028 略低於共識（提列回到區間中上、行銷常態化、收益率向 11% 收斂），之後增速 13%→9%；終端 15 倍，較現值 FY2 16.7 倍再壓縮","bear":"新客 cohort 遇景氣轉弱，提列升到 4–5%，2027–2028 EPS 停滯並下滑，2031 年修復到 6.00；終端 9 倍（信用壓力下的消費金融倍數；同業倍數事實表未涵蓋）"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"第二季淨增 14 萬訂閱戶創紀錄，CFO 說新客損失率較高、單季提列可能超過 3%；第一季 CFO 說 Pay-in-5 初期損失率略高；SezzleCash 現金預支與 Sezzle Send 對非訂閱戶放款剛上線；發卡銀行夥伴非獨家、特定事件可終止","assumption":"管理層 2.5–3% 的全年提列區間已把新客與新產品效應算進去","consequence":"5 年後虧 50% 最可能的故事：2026 下半年到 2027 年的新客 cohort 遇上景氣轉弱，提列走到 4–5%，發卡夥伴或州法同時收緊，EPS 停滯、本益比掉到個位數，對應空頭情境 54 美元、−51%","ruling":"採納為最大風險，與唯一致命點是同一件事（撞上，不另立）；目前沒有已發生的證據，兩季法說都稱未見消費者壓力","watch":"每季提列／GMV、淨交易利潤率、全年提列指引","evidence_refs":["geo_supply_chain#0"],"fact_refs":["f_kpi7_active_subscribers","f_kpi6_full_year_2026_guidance"]},{"view":"論點成功但股東經濟變差","evidence":"企業商家費率競爭激烈，Klarna 取代 Affirm 成為 Walmart 獨家；CFO 說 SezzleCash 與 Pagaya 會拉低收益率；Target 在信用額度合約中可占應收 35%，議價力在大商家手上；銀行與科技公司內嵌分期","assumption":"訂閱與交易量照計畫成長，收益率守在 11% 以上","consequence":"量長、錢被分走：收益率往 10% 掉、淨交易利潤率從 63.5% 回到目標中值 60%，加上銀行執照的資本與合規成本，營收成長但 EPS 落後共識","ruling":"部分採納：全年收益率持平的財測已反映一部分，但 63.5% 在目標區間上緣，向中值回歸是常態，已放進基準情境（FY2027–2028 略低於共識）","watch":"收益率低於 10.5%、淨交易利潤率低於 58%","evidence_refs":["supply_demand_durability#2","customer_second_source#0","competitive_share_entrants#4"],"fact_refs":["f_kpi0_total_revenue_gaap"]},{"view":"價格已反映太多","evidence":"trailing 本益比 24.3 倍、市銷率 7.0 倍、EV／營收 7.1 倍都在年度端點最高位置；盈餘來自信用損失偏低的順風期","assumption":"FY1 21 倍的分母可以延續","consequence":"若提列比指引上緣 3% 再多 0.5pp，以每 1pp GMV 約占淨利兩成換算，FY1 EPS 約少 11%，實際本益比從 21 倍升到約 24 倍，便宜論證打折","ruling":"部分反駁：股價已從 7 月 177 美元跌到 110.85 美元，FY2 16.7 倍、PEG 0.73；年度端點只有 3–4 個樣本，不代表五年位置；賣方平均目標價全在現價之上。但分母敏感度是真的，所以只判合理不判便宜","watch":"FY2 共識是否下修、提列指引","evidence_refs":[],"fact_refs":["f_pe_current","f_pe_percentile","f_ps_percentile","f_fwd_pe_latest","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"審計與風險委員會成員 Karen Webster 以治理分歧立即辭職（2026-04-09）；2026-04-30 起多家律所公告調查證券詐欺，尚未見正式起訴","assumption":"治理雜音停在調查階段","consequence":"若正式起訴並揭露內控或揭露問題，信任折價會讓倍數長期壓低，訴訟也分散管理層精力","ruling":"列為監測：辭職是實質警訊，律所公告屬股價大跌後的招攬性質、尚無起訴；倉位上限先打折","watch":"法院案卷、10-K 審計意見、董事會人事","evidence_refs":["major_events#2","major_events#1","regulatory_antitrust#3","lawsuit_class_action#0"],"fact_refs":[]},{"view":"論點失敗","evidence":"有律所調查 Sezzle 是否就逾期費、付款時點、透支風險或分期真實成本誤導消費者；CEO 第一季說部分州在削弱銀行夥伴模式；產品往現金預支延伸","assumption":"CFPB 撤回限制性規則後，聯邦監管壓力暫緩","consequence":"州級把訂閱費或預支費視為利息，或銀行夥伴模式在關鍵州被限制，訂閱引擎的收費基礎直接受損","ruling":"採納為中期風險，但目前只有律所調查、沒有政府行動；紐約州規則進度本輪事實表未涵蓋，列資料缺口","watch":"州監管公告、消費者集體訴訟、銀行執照進度","evidence_refs":["regulatory_antitrust#2","geo_supply_chain#0"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 177.08 → 本次 110.85（-37.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=177.08","side_b":"本次 price_at_dd=110.85","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層承諾兌現（一致判斷）","cause":null,"prior_field":null,"side_a":"第一季法說（2026-05-06）：營收成長財測 30–35%、調整後淨利 1.8 億、EPS 5.10；現金流管理產品幾個月內推出；信用額度明年四月到期、正在再融資；提列 2.5–3%；支票帳戶產品幾個月內推出","side_b":"第二季法說（2026-08-06）：營收成長瞄準 35% 上緣、調整後淨利上修到 1.85 億、EPS 5.25；SezzleCash 六月上線；新的 3 億美元信用額度到位；提列區間不變。支票帳戶產品本季未再提","ruling":"一致：財測與產品承諾大多兌現，支票帳戶產品進度列為待查","evidence_level":"公司新聞稿與兩季逐字稿","settle_metric":"第三季法說是否交代支票帳戶產品與銀行執照送件","if_then":["若第三季仍未提支票帳戶產品且銀行執照未送件 → 第二曲線假設降權，不動基準情境"],"evidence_refs":[]},{"axis":"成長敘事與下半年財測","cause":null,"prior_field":null,"side_a":"CEO：成長曲線像 2020–2021 年，五月交易量就超過十二月旺季","side_b":"全年營收成長 35% 意味下半年約 30%，遠低於第二季 51.7%；財報後盤前跌 23%","ruling":"可調和（程度差異）：第二季營收成長有收益率低基期加持（去年約 10% 出頭、今年 11.7%），CFO 在第一季就預告；交易量 +37.9% 才是需求的真實速度，下半年 30% 左右的營收成長與此相容","evidence_level":"兩季逐字稿＋第二季新聞稿","settle_metric":"第三季交易量年增率與營收年增率","if_then":["若第三季交易量年增 ≥30% 且營收年增 ≥28% → 減速屬基期效果，維持判斷","若第三季交易量年增低於 25% → 需求確實放緩，基準情境下修並啟動減碼條件"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"行銷支出說法改口","cause":null,"prior_field":null,"side_a":"第一季法說 CEO：行銷支出預期逐季上升","side_b":"第二季法說 CEO：第二季 1,940 萬美元是刻意測試、不是新常態，第三季核心行銷會降；但新產品需要知名度支出","ruling":"可調和：第二季確實衝高，第三季降溫是測試後收手。風險在於管理層用「回收期低於 6 個月」自我授權加碼，而回收期只有公司自述；若第三季行銷仍高、淨增訂閱戶卻放緩，代表邊際回收在變差","evidence_level":"兩季逐字稿","settle_metric":"第三季行銷支出與淨增訂閱戶","if_then":["若第三季行銷支出高於 1,940 萬美元而淨增訂閱戶低於 10 萬 → 視為獲客效率下滑，暫停加碼"],"evidence_refs":[]},{"axis":"治理：公司說法與董事辭職、律所調查","cause":null,"prior_field":null,"side_a":"CFO：損益表調整項極少，是同業中最乾淨之一；本輪事實表查無 SEC 調查或財報重編","side_b":"2026-04-09 董事 Karen Webster（審計與風險、薪酬、提名委員會成員）以「與管理層在公司方向、關鍵決策與治理上看法分歧」立即辭職；2026-04-30 起多家律所公告調查證券詐欺，尚未正式起訴","ruling":"可調和（不同命題）：調整項乾淨講的是會計口徑，董事辭職講的是治理決策，兩者不直接衝突。審計委員會成員因治理分歧離開是實質警訊，但律所公告屬招攬性質，沒有起訴就沒有可裁決的事實；裁定未證、監測，倉位上限先打折","evidence_level":"8-K 與律所新聞稿（二手、招攬性質）","settle_metric":"法院案卷是否出現正式起訴；10-K 審計意見；後續董事會人事","if_then":["若集體訴訟正式起訴並通過駁回動議 → 減碼至半倉","若 SEC 正式調查或財報重編 → 清倉","反向：若 2027-06 前仍無起訴且年報審計意見無保留 → 解除倉位上限折扣"],"evidence_refs":["major_events#2","major_events#1","regulatory_antitrust#3","lawsuit_class_action#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"等第三季：新客與新放款產品把提列推高的風險還沒驗證","side_b":"現在就買：股價已跌破前份設定的進場價（130–140 美元），FY2 16.7 倍、PEG 0.73；獲利財測兩季連升、FY1 共識三個月上修 3.1%；提列上升已被管理層預告、市場已知；等財報可能錯過財報後的反彈","ruling":"維持等待：基準情境年化報酬只有 7–8%，不夠補償提列上調時的下檔（空頭終點 −51%）；等一個月換到最大敏感項的第一手數據，代價可接受","evidence_level":"事實表估值數據＋法說指引","settle_metric":"第三季提列／GMV 與淨交易利潤率","if_then":["若第三季提列守在指引內 → 進場首倉，即使股價已反彈也照做","若股價先跌破 95 美元而信用指標未惡化 → 不等財報，分批反買"],"evidence_refs":[]},{"axis":"股價下跌帶動的估值與報酬重算","cause":"價格變動","prior_field":["val","asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份 2026-07-10 股價 177.08 美元，以現行共識回算 FY1 本益比約 34 倍，估值偏貴；裁決觀望；基準年化報酬 6.0%、五年期望 +29%、多空比 1.9","side_b":"現價 110.85 美元（−37%），FY1 21.1 倍、FY2 16.7 倍，估值改判合理；報酬類數字由程式依新價與新情境樹重算，裁決與角色由程式依新輸入重新路由","ruling":"估值結論由偏貴改為合理，主因是價格下跌而非基本面轉好；同期獲利財測反而上修","evidence_level":"事實表股價與共識","settle_metric":"FY1／FY2 本益比","if_then":["若股價回到 140 美元以上而共識未上修 → 估值回到偏貴區，不追"],"evidence_refs":[]},{"axis":"情境樹終端倍數與回撤區間重設","cause":"方法變動","prior_field":["bull_5y_price","bear_5y_price","max_dd_pct"],"side_a":"前份多頭五年價 388 美元、空頭 83 美元、最大回撤 −65%（單點）","side_b":"本次多頭 FY2031E EPS 13.80×20 倍＝276 美元、空頭 6.00×9 倍＝54 美元；回撤改填區間 −55%～−70%","ruling":"多頭終端倍數以現值 FY1 21 倍為上限，不給高於現值的倍數；空頭改用信用壓力下的消費金融倍數 9 倍並讓 EPS 在 2028 年下滑，下檔比前份深；回撤由單點改區間，中值與前份相近","evidence_level":"方法調整，無新外部證據","settle_metric":"不適用（方法變動）","if_then":["若取得同業倍數資料顯示信用壓力期消費金融本益比高於 12 倍 → 空頭倍數上修"],"evidence_refs":[]},{"axis":"第二季新證據檢視後維持的欄位","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct"],"side_a":"前份：綜合訊號 B、價值陷阱風險中（🟡）、護城河方向穩定（→）、長期跑道中等（🟡）、品質複利成長型、未判景氣位置、多頭機率 25%、空頭 30%","side_b":"本次全部維持：訂閱戶 +76.4%、購買頻率 7.2 次支持護城河執行面，但收益率持平、企業商家壓費率抵銷；市場放緩、第二曲線未進財測，跑道維持中等；信用週期未經壓力測試＋董事辭職，陷阱風險維持中；非景氣循環股，不判景氣位置；新客 cohort 風險與獲利上修相抵，多空機率不變","ruling":"新證據兩面都有，淨方向不足以改判","evidence_level":"第二季新聞稿與逐字稿","settle_metric":"第三季提列與淨增訂閱戶","if_then":["若第三季訂閱戶年增仍 ≥50% 且提列守住 → 多頭機率上調至 30%","若提列區間上調 → 空頭機率上調至 40%"],"evidence_refs":[]},{"axis":"進場條件改寫（前份估值腿已觸發）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"估值回落至 Fwd PE ~20x（$130-140），或治理與監管明朗（集體訴訟撤銷＋NY BNPL 規則以可承受形式定稿＋Utah ILC 正式送件）","side_b":"第三季財報提列／GMV 守在全年 2.5–3% 指引內且淨交易利潤率 ≥55% → 進場首倉；股價先跌破 95 美元而信用指標未惡化 → 分批反買","ruling":"前份進場條件的估值腿已觸發（股價 110.85 美元低於 130–140 美元），本次即觸發後重跑。價格下跌伴隨新證據——下半年營收減速財測、第二季行銷衝高帶來的創紀錄新客將在下半年墊高提列——把卡住進場的條件從估值換成信用驗證；治理與監管腿保留為監測，不再當進場前提","evidence_level":"事實表股價＋第二季逐字稿","settle_metric":"第三季提列／GMV、淨交易利潤率","if_then":["若第三季兩項都過關 → 進場首倉（半倉）","若提列區間上調 → 不進場，等兩季數據"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"Single Thing 唯一致命點新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"管理層在季報把全年提列區間從 2.5–3% of GMV 上調到 3% 以上（單一離散事件）；發生則減碼至半倉，淨交易利潤率同時跌破 55% 則清倉","ruling":"補上前份缺漏：提列率是 EPS 最大單一敏感項（每 1pp GMV 約占調整後淨利兩成），用管理層自己給的區間當離散觸發點","evidence_level":"第二季法說提列指引","settle_metric":"每季全年提列指引","if_then":["若指引上緣上調 → 減碼至半倉"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標（空白）","side_b":"淨交易利潤率低於 55% 連兩季 → 清倉；TTM 提列／GMV 高於 3.5% 連兩季或指引上調 → 減碼；訂閱戶年增低於 20% → 減碼；發卡夥伴終止無替代 → 清倉；集體訴訟通過駁回動議 → 減碼","ruling":"把前份散在風險表裡的警戒線收斂成可執行的清倉與減碼清單，門檻對齊管理層公開指引","evidence_level":"方法調整","settle_metric":"每季財報","if_then":["任一清倉條件成立 → 清倉，不等複審"],"evidence_refs":[]},{"axis":"信用門檻重新校準（前份 2.0% 警戒線）","cause":"方法變動","prior_field":["thesis.H1","thesis.R1"],"side_a":"連 2 季 TTM provision/GMV ≥ 2.0% → 削弱；連 3 季 ≥ 3.0% 或撥備增速連 2 季超前 GMV 增速 → 反轉；單季 ≥ 3.0%、30+ DPD > 5% 警戒","side_b":"TTM 提列／GMV 連 2 季高於 3.15% → 削弱；連 3 季高於 3.3% 或淨交易利潤率跌破 55% → 反轉；單季高於 3.5%、提列年增率連 2 季超前交易量年增率 10pp 以上、30 天以上逾期率高於 5% 列風險","ruling":"前份 2.0% 以第一季（全年最低點 1.2%）為基準，但管理層兩季都指引全年 2.5–3%，第一季本就是季節低點，2.0% 會被季節性機械觸發、不代表信用轉壞，改用 TTM 口徑並對齊區間上緣；撥備增速超前的領先警訊保留並加上 10pp 幅度。第二季單季提列率事實表未涵蓋，前份單季 3.0% 警戒線是否已觸發無法確認，CFO 說單季可以超過 3%，第三季需逐季核對；逾期率仍是資料缺口","evidence_level":"兩季逐字稿","settle_metric":"TTM 提列／GMV","if_then":["若第三季 TTM 提列／GMV 高於 3.0% → 停止加碼並開始削弱計數"],"evidence_refs":[]},{"axis":"第二曲線路徑改變：州 ILC 改為國家銀行執照","cause":"新證據","prior_field":["thesis.H3"],"side_a":"前份：Utah ILC 銀行牌照，2026 正式向 Utah DFI 送件；FY28-29 獲批","side_b":"第二季法說：計畫本季（2026 第三季）送出國家銀行執照申請，OCC 約 120 天作出有條件決定，再加 FDIC、Fed 核准，總時程 12–18 個月；第一季原說年中送件，進度略延","ruling":"路徑改走聯邦、時程比前份短，但仍未確認送件，CFO 第一季也說不保證成功；維持為選擇權，不進基準情境","evidence_level":"兩季逐字稿","settle_metric":"送件公告與 OCC 公開紀錄","if_then":["若 2026 年底前未送件 → 第二曲線降為更遠期選擇權","若取得有條件核准 → 多頭機率上調至 30%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"第三季財報檢查信用：提列季節性上升的幅度","type":"假設驗證","maps_to":"H1","metric":"第三季提列／GMV、淨交易利潤率、全年提列指引","threshold":"全年提列仍守 2.5–3% 指引且淨交易利潤率 ≥55%","action":"兩項過關 → 進場首倉（半倉）；未過 → 不追，續看第四季","source_freq":"季報（每季）","date":"2026-11"},{"n":2,"text":"管理層把全年提列區間上調到 3% 以上","type":"Single Thing","maps_to":"R1","metric":"全年提列／GMV 指引上緣","threshold":"高於 3.0%","action":"持有則減碼至半倉；未持有則不進場，等兩季新客損失數據","source_freq":"季報與法說","date":null},{"n":3,"text":"首倉後訂閱與信用雙雙過關再補足","type":"加碼","maps_to":"H2","metric":"活躍訂閱戶年增率＋全年提列／GMV","threshold":"訂閱戶年增 ≥30% 且 2026 全年提列 ≤3.0%","action":"加碼至目標倉位","source_freq":"季報","date":"2027-02"},{"n":4,"text":"信用失守","type":"清倉","maps_to":"R1","metric":"淨交易利潤率","threshold":"低於 55% 連兩季","action":"清倉","source_freq":"季報","date":null},{"n":5,"text":"成長減速超出基期解釋","type":"減碼","maps_to":"R5","metric":"營收年增率與交易量年增率","threshold":"營收年增連兩季低於 20%，或第三季交易量年增低於 25%","action":"減碼至半倉","source_freq":"季報","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":6,"text":"證券訴訟從調查變成正式起訴","type":"風險","maps_to":"R4","metric":"法院案卷、SEC 動作","threshold":"集體訴訟正式起訴並通過駁回動議；SEC 正式調查或財報重編","action":"起訴 → 停止加碼；通過駁回動議 → 減碼至半倉；SEC 介入或重編 → 清倉","source_freq":"持續（8-K、案卷）","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#3","major_events#2"]},{"n":7,"text":"發卡夥伴或州法規收緊","type":"風險","maps_to":"R3","metric":"發卡銀行合約、州級規則、消費者訴訟","threshold":"發卡夥伴終止且 90 天內無替代；州法把訂閱費或預支費納入利率上限；消費者集體訴訟正式起訴","action":"規則收緊或消費者訴訟 → 減碼；發卡夥伴終止且無替代 → 清倉","source_freq":"8-K、州監管公告","date":null,"evidence_refs":["geo_supply_chain#0","regulatory_antitrust#2"]},{"n":8,"text":"大商家與平台集中風險","type":"風險","maps_to":"R2","metric":"Target 與大型電商平台合作狀態、收益率","threshold":"Target 導入第二家或終止合作；任一大平台終止合作；全年收益率低於 10.5%","action":"停止加碼並重估情境樹","source_freq":"8-K、季報","date":null,"evidence_refs":["customer_second_source#0","geo_supply_chain#2","supply_demand_durability#2","competitive_share_entrants#4","substitute_technology#0"]},{"n":9,"text":"國家銀行執照送件","type":"假設驗證","maps_to":"H3","metric":"送件公告","threshold":"2026-12-31 前送件","action":"未送件 → 第二曲線降為更遠期選擇權，不動倉位","source_freq":"8-K、OCC 公開紀錄","date":"2026-12"},{"n":10,"text":"股價先跌、信用未惡化時分批反買","type":"估值rearm","maps_to":null,"metric":"股價＋提列指引","threshold":"股價低於 95 美元（FY2 約 14 倍，接近 52 週均線 95.35 美元）且提列仍在指引內","action":"分批反買首倉","source_freq":"每日股價、季報","date":null},{"n":11,"text":"第四季財報複審","type":"複審日期","maps_to":null,"metric":"2026 全年提列實績、2027 財測","threshold":"財報公布即複審","action":"重跑完整判斷","source_freq":"年報","date":"2027-02"}],"kill_metrics":[{"metric":"淨交易利潤率（營收減交易相關成本占營收）","bear_threshold":"低於 55% 連兩季 → 清倉","window":"每季，2026Q3 起","source":"季度財報新聞稿與法說簡報","last_status":"ok"},{"metric":"TTM 提列／GMV 與全年提列指引","bear_threshold":"高於 3.5% 連兩季，或指引上緣調到 3% 以上 → 減碼至半倉","window":"每季，2026Q3–2027Q4","source":"季度財報與法說","last_status":"ok"},{"metric":"活躍訂閱戶年增率","bear_threshold":"低於 20% → 減碼","window":"每季至 2027 年底","source":"季度財報新聞稿","last_status":"ok"},{"metric":"發卡銀行夥伴關係","bear_threshold":"終止或不續約且 90 天內無替代 → 清倉","window":"持續","source":"8-K 與 10-Q 風險揭露","last_status":"ok"},{"metric":"證券集體訴訟與 SEC 動作","bear_threshold":"起訴並通過駁回動議 → 減碼；SEC 正式調查或重編 → 清倉","window":"至 2027 年底","source":"法院案卷、8-K、律所公告","last_status":"warning"}],"evidence_dismissed":[{"ref":"geo_supply_chain#1","reason":"10-K 通用風險因子樣板，未附任何實際中斷事件、發生頻率或影響金額，也沒有可監測的指標，無法轉成論點變數"}],"action_conditions":{"rearm_trigger":"第三季財報提列／GMV 守在全年 2.5–3% 指引內且淨交易利潤率 ≥55% 即進場首倉；股價先跌破 95 美元而信用未惡化則分批反買","exec_line":"現在不追；第三季財報（2026-11）兩項信用指標過關 → 首倉半倉；第四季財報（2027-02）訂閱戶年增 ≥30% 且全年提列 ≤3.0% → 補足；提列指引上調 → 減碼至半倉；淨交易利潤率低於 55% 連兩季 → 清倉；股價先跌破 95 美元而信用未惡化 → 分批反買"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把下半年營收減速當成需求放緩，但減速主要是第二季收益率低基期消退，交易量仍 +37.9%、獲利財測連兩季上修；信用面市場的擔心可能是對的，要等第三季驗證","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等 2026 年 11 月第三季財報：提列／GMV 守在全年 2.5–3% 指引內、淨交易利潤率 ≥55%；或股價先跌破 95 美元（FY2 約 14 倍）而信用指標未惡化","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把下半年營收減速當成需求放緩，但減速主要是第二季收益率低基期消退，交易量仍 +37.9%、獲利財測連兩季上修；信用面市場的擔心可能是對的，要等第三季驗證"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=68.46, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='-'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='-'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='-'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2026 年 11 月第三季財報：提列／GMV 守在全年 2.5–3% 指引內、淨交易利潤率 ≥55%；或股價先跌破 95 美元（FY2 約 14 倍）而信用指標未惡化'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"新客湧入下信用品質守得住：全年提列落在管理層 2.5–3% 區間、淨交易利潤率守在 55% 以上","2y":"FY2026–2027 全年提列／GMV ≤3.0%，淨交易利潤率 ≥55%","5y":null,"10y":null,"threshold":"第二季淨交易利潤率 63.5%；全年提列指引 2.5–3% of GMV；警戒＝TTM 提列／GMV 高於 3.0% 或淨交易利潤率低於 55%","source":"季度財報新聞稿、法說簡報（提列與淨交易利潤率）","drift_rule":"TTM 提列／GMV 連 2 季高於 3.15% → 削弱；連 3 季高於 3.3% 或淨交易利潤率跌破 55% → 反轉；提列年增率連 2 季超前交易量年增率 10pp 以上 → 列為領先警訊"},{"id":"H2","text":"訂閱飛輪：用戶數與使用頻率同時上升，每位變現用戶營收持續成長","2y":null,"5y":"2030 年前活躍訂閱戶維持雙位數年增、季購買頻率 ≥7 次、每位變現用戶季營收年增為正","10y":null,"threshold":"第二季活躍訂閱戶 85.4 萬（+76.4%）、購買頻率 7.2 次、每位變現用戶季營收 +16.2%、回購用戶訂單占 97.2%；警戒＝訂閱戶年增低於 20%","source":"季度財報新聞稿與法說簡報（訂閱戶、購買頻率、每位變現用戶季營收）","drift_rule":"訂閱戶年增連 4 季低於 19%（20% 門檻下偏 5%）→ 削弱；連 6 季低於 18% 或出現季減 → 反轉"},{"id":"H3","text":"第二曲線：國家銀行執照＋非結帳產品（SezzleCash、Sezzle Send）把 Sezzle 從結帳工具變成日常理財入口，並把銀行夥伴的變動成本轉為固定成本","2y":null,"5y":"2028 年前取得國家銀行執照（含 FDIC、Fed 核准），2027 年底前存款帳戶上線（CEO 第一季承諾）；新產品貢獻進入財測","10y":null,"threshold":"第二季法說：計畫本季送件，總時程 12–18 個月；新產品目前未計入或極少計入財測；Sezzle Send 等候名單約 10 萬人；約一成新訂閱戶首筆交易是 SezzleCash","source":"OCC 公開申請紀錄、8-K、季度法說","drift_rule":"2026 年底仍未送件 → 削弱；送件後 24 個月未獲有條件核准、撤件或被拒 → 反轉；此假設是選擇權，不進基準情境"}],"R":[{"id":"R1","text":"信用正常化：創紀錄新客、Pay-in-5 與 SezzleCash 的初期損失率較高，下半年提列季節性上升可能超出指引","h_ref":"H1","clock":"⚡","threshold":"TTM 提列／GMV 高於 3.0% 連兩季或單季高於 3.5%；淨交易利潤率低於 55%；30 天以上逾期率高於 5%（事實表未涵蓋，資料缺口）"},{"id":"R2","text":"競爭與集中：企業商家費率壓力、大型電商平台與 Target 集中、銀行與大型科技內嵌分期","h_ref":"H2","clock":"🔥","threshold":"全年收益率低於 10.5%（2025 年 11.4% 下滑約 1pp）；Target 導入第二家或任一大平台終止合作；營收年增連兩季低於 20%","evidence_refs":["competitive_share_entrants#4","supply_demand_durability#2","geo_supply_chain#2","substitute_technology#0","customer_second_source#0"]},{"id":"R3","text":"監管與發卡夥伴：州級削弱銀行夥伴模式、發卡銀行可終止、消費者端收費被訴","h_ref":"H1+H3","clock":"🔥","threshold":"發卡銀行夥伴終止且 90 天內無替代；州法或聯邦規則把訂閱費、現金預支費納入利率上限，或紐約州規則定稿把訂閱費實質納入年利率且兩個以上大州跟進（本輪事實表未涵蓋紐約規則進度，資料缺口）；消費者集體訴訟正式起訴","evidence_refs":["geo_supply_chain#0","regulatory_antitrust#2"]},{"id":"R4","text":"治理升級：董事以治理分歧辭職後，證券詐欺調查轉成正式訴訟或監管行動","h_ref":"H1+H2","clock":"🐢","threshold":"證券集體訴訟正式起訴並通過駁回動議或取得集體認證；SEC 正式調查或財報重編；再有獨立董事或財務長離職；股價觸及 CEO 質押保證金追繳（質押水位事實表未涵蓋，資料缺口）","evidence_refs":["major_events#1","major_events#2","regulatory_antitrust#3","lawsuit_class_action#0"]},{"id":"R5","text":"成長減速超出基期效果：下半年營收減速不只是收益率回落，而是交易量真的放緩","h_ref":"H2","clock":"⚡","threshold":"2026 全年營收成長低於 30%（財測 35%）；第三季交易量年增低於 25%","evidence_refs":["competitive_share_entrants#3"]}],"single_thing":{"description":"管理層在季報把全年提列區間從 2.5–3% of GMV 上調到 3% 以上（單一離散事件）","why_fatal":"提列每多 1pp GMV，稅前少約 5,400 萬美元（2026 年交易量約 54 億＝2025 年 39.4 億×1.38），稅後約 4,000 萬（以第二季淨利÷營業利益 74% 換算），約占 2026 調整後淨利指引 1.85 億的兩成；這是 EPS 路徑上最大的單一敏感項，區間一旦上調，市場會同時下修 EPS 與倍數","if_happens":"持有則減碼至半倉，未持有則不進場；淨交易利潤率同時跌破 55% 則清倉，等兩季新客損失數據再重跑判斷","how_monitor":"每季財報的提列／GMV、淨交易利潤率與全年提列指引；下一個檢查點是 2026 年 11 月第三季財報","probability":"15%（12–24 個月）：管理層已預告下半年提列上升、單季可能超過 3%，新客創紀錄且兩項新放款產品剛上線；但兩季法說都稱未見消費者壓力"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.67,"peg_fy2":0.73,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":3.72,"FY2026E":5.26,"FY2027E":6.65,"FY2028E":7.95},"fy_end_month":12,"eps_basis":"共識為調整後稀釋 EPS（Koyfin 2026-09-26；公司調整後淨利與 GAAP 淨利差距小）；FY2025A 用 GAAP 稀釋 EPS 3.72，調整後值事實表未涵蓋"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報：提列季節性上升幅度、全年提列指引、行銷支出回落程度","impact":"高","watch":"提列／GMV、淨交易利潤率、淨增訂閱戶"},{"date":"2026-11","date_precision":"month","type":"regulatory","event":"確認國家銀行執照申請是否已送出（原定 2026 第三季）","impact":"中","watch":"OCC 公開紀錄或 8-K"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"Sezzle Send 上線後的使用與拉新成效、SezzleCash 開始對外行銷","impact":"中","watch":"等候名單轉換、非訂閱戶轉訂閱"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年財測","impact":"高","watch":"全年提列實績、2027 EPS 指引對共識 6.65"},{"date":"2027-12","date_precision":"quarter","type":"regulatory","event":"Shopify 反壟斷案證據開示預計持續到 2027 年","impact":"低","watch":"和解或簡易判決動議"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
