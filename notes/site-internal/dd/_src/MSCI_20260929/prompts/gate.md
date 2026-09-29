你是 DD 管線 v20 的判斷層閘（gate），標的 MSCI（20260929）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

④ priced-in——共識與賣方目標價 vs 現價，裁決是否只是把市場已知的事再說一次。看 `decision_inputs.market_wrong_reason_given` 是否有具體內容（非空泛套話），對照 facts.json 的 `latest_quarter_kpis[].vs_consensus` 與 `valuation_current`。[gate_contract §④]

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

### 判斷檔 `fact_refs` 引到的事實（37 條）
- `f_kpi0_total_operating_revenue_`（q1_business）｜Total operating revenue (GAAP)＝867.0 $M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com「MSCI Reports Financial Results for Second Quarter and Six Months 2026」（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：consensus 約 $864.08M，實際 $867.0M 略勝（來源：web_search 彙整市場預期，非本站 dd_numbers_extra 結構化欄）
- `f_kpi1_adjusted_ebitda_margin_n`（q1_business）｜Adjusted EBITDA margin (non-GAAP)＝62.1 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（Adjusted EBITDA $538.5M，YoY +13.5%）（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：未查得 sell-side 對 Adj. EBITDA margin 的共識數字
- `f_kpi2_gaap_operating_margin`（q1_business）｜GAAP operating margin＝56.2 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：10-Q（SEC EDGAR msci-20260630.htm）與公司新聞稿一致：營業利益 $487.5M／營收 $867.0M（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：未查得共識數字（GAAP operating margin 非 sell-side 常態追蹤指標）
- `f_kpi3_free_cash_flow_non_gaap`（q1_business）｜Free cash flow (non-GAAP)＝326.4 $M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：未查得共識數字
- `f_kpi5_retention_rate`（q1_business）｜Retention Rate＝95.3 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：不適用（公司自報營運指標，非 sell-side 財務預估項目）
- `f_kpi6_index_analytics_organic_`（q1_business）｜Index／Analytics organic recurring subscription Run Rate growth＝Index 11.1% / Analytics 6.6% %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：不適用
- `f_peer_msci_gross_margin_pct`（q2_moat）｜MSCI 毛利率＝82.97 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSCI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_msci_operating_margin_pct`（q2_moat）｜MSCI 營業利益率＝55.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSCI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_msci_fcf_margin_pct`（q2_moat）｜MSCI FCF 利潤率＝44.77 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSCI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_spgi_gross_margin_pct`（q2_moat）｜SPGI 毛利率＝70.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SPGI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_spgi_operating_margin_pct`（q2_moat）｜SPGI 營業利益率＝41.56 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SPGI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mco_gross_margin_pct`（q2_moat）｜MCO 毛利率＝74.98 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mco_operating_margin_pct`（q2_moat）｜MCO 營業利益率＝46.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fds_operating_margin_pct`（q2_moat）｜FDS 營業利益率＝29.55 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FDS.operating_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi7_fy2026_guidance_q2`（q1_business）｜FY2026 全年財測（管理層 guidance，於Q2財報會議重申／更新）＝Opex $1,535–1,575M；Adjusted EBITDA Expense $1,340–1,370M；Capex $160–170M；Free Cash Flow $1,485–1,545M USD millions（區間）｜期間與口徑：隨 Q2 FY2026 財報發布（2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（numbers.latest_quarter_kpis.items[7]，as_of 隨 Q2 FY2026 財報發布（2026-07-21））
  - 註記：不適用
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝19.74 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-09-26）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝22.5 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-09-26）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝25.54 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-09-26）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-09-28（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-09-28（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-09-28（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-09-28（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-09-28（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-09-28（RTH 收盤，UTC））
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation as % of revenue（推算）＝2.93 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21，推算值）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：推算：Q2 10-Q 現金流量表揭露 H1 FY2026 SBC 累計 $73.1M，減去 Q1 10-Q（三個月至2026-03-31）揭露的 Q1 SBC $47.7M，得 Q2 單季 SBC ≈ $25.4M；MSCI 10-Q 現金流量表僅揭露年初至今累計數，未單獨揭露單季數字（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21，推算值））
  - 註記：不適用
- `f_ps_current`（q5_valuation）｜P/S（現值）＝11.84 x｜期間與口徑：2026-09-28（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-09-28（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝542.72 USD｜期間與口徑：2026-09-28（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-09-28（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝27.49 x｜期間與口徑：2026-09-26／分母＝FY1 EPS 19.74，分子＝快照價 542.72｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-09-26）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝29.64 x｜期間與口徑：2026-09-28（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-09-28（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝13.69 x｜期間與口徑：2026-09-28（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-09-28（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-09-26／兩份 Koyfin 快照之間的 EPS 修正幅度（19.74 → 19.74）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-09-26）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-09-26／兩份 Koyfin 快照之間的 EPS 修正幅度（22.5 → 22.5）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-09-26）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.08 %｜期間與口徑：2026-09-26／兩份 Koyfin 快照之間的 EPS 修正幅度（25.52 → 25.54）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-09-26）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-09-29／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-29）
  - 原文：「price 542.72 / W52 565.73 / W104 564.28 / W250 517.85 / W250 13週斜率 -0.08%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝565.73 USD｜期間與口徑：2026-09-29／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-29）
- `f_ma_w104`（q5_valuation）｜104 週均線＝564.28 USD｜期間與口徑：2026-09-29／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-29）
- `f_ma_w250`（q5_valuation）｜250 週均線＝517.85 USD｜期間與口徑：2026-09-29／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-29）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-0.08 %｜期間與口徑：2026-09-29／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-29）
- `f_rsi14`（q5_valuation）｜RSI(14)＝41.21｜期間與口徑：2026-09-28（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-09-28（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝2.77 %｜期間與口徑：2026-09-28（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-09-28（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：MSCI's FY2023 10-K discloses BlackRock as its largest client organization by revenue, at 9.8% of consolidated operating revenues, with 95.4% of BlackRock's revenue to MSCI coming from asset-based fees on ETFs/non-ETF products using MSCI indexes — a concentration/single-client dependency risk factor.
  - 來源：MSCI Inc. Form 10-K FY2023 (SEC EDGAR)（as_of 2023-12-31）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：BlackRock is MSCI's largest client, accounting for 10.8% of consolidated operating revenues for FY2025; 96.5% of that BlackRock-derived revenue comes from asset-based fees on BlackRock's ETFs and non-ETF products tracking MSCI indexes.
  - 來源：MSCI Inc. 10-K FY2025 (filed 2026)（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear、valuation
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：MSCI discloses risk that its largest clients (including BlackRock) may negotiate lower asset-based fees, stop using MSCI indexes, or cancel/reduce usage, which could have a material adverse effect on results.
  - 來源：MSCI Inc. 10-K FY2025 (filed 2026), Risk Factors（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：BlackRock accounted for 18.7% of MSCI's Index segment operating revenues for FY2025 (vs. 17.4% in FY2022), indicating rising within-segment concentration over time.
  - 來源：MSCI Inc. 10-K FY2025 (filed 2026)（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：MSCI 10-K 揭露：2024 年 11 月歐盟通過 ESG 評等透明度與誠信規範 (EU) 2024/3005，要求在歐盟境內營運的 ESG 評等提供者須於 2026 年 7 月 2 日起取得 ESMA 授權或註冊；MSCI 表示其部分永續與氣候相關產品預期將受此規範管轄。
  - 來源：MSCI Inc. Form 10-K FY2025 (SEC EDGAR)（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：台灣占 MSCI 新興市場指數(EM Index)權重達 24.8%（2026-04-30 資料），為指數內最大權重國家，主因 AI 驅動半導體需求；同期資訊科技板塊權重由 31.8% 升至近 37%。此為 MSCI 旗艦指數產品在地緣風險區域（台灣/中國）的集中曝險。
  - 來源：MSCI - Markets in Motion: Taiwan at the Top, EM Weight Breakdown（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：被動ETF市場2026年估值達$16.8兆，但主動型ETF數量已在2025年6月超越被動型ETF；主動ETF資產達$1.47兆、近三年CAGR 59%，顯示主動策略在ETF資金流結構性搶佔份額，對MSCI核心被動指數授權/資產基礎費成長模型構成潛在逆風。
  - 來源：Active vs. Passive ETFs: How the 2026 Active Surge Changes the Math - etf.com（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：AI/LLM 工具可低成本自動解析企業永續揭露、複製部分 ESG 評等結果；若機構投資人認為 MSCI ESG Ratings 與 AI 生成替代品區隔不足，MSCI 的評等定價溢價可能被侵蝕
  - 來源：PitchGrade Research - "MSCI: Index Licensing and ESG Data Franchises in the Age of AI-Powered Analytics"（as_of 2026-01-29）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：MSCI 2026 Q2 財報後上修 2026 全年費用 guidance：營運費用上修至 $1,535M–$1,575M（原 $1,490M–$1,530M），Adjusted EBITDA 費用上修至 $1,340M–$1,370M（原 $1,305M–$1,335M），主因近期併購（含 First Street）及 AUM 動能超過先前假設
  - 來源：MSCI Reports Financial Results for Second Quarter and Six Months 2026 (businesswire/ir.msci.com)（as_of 2026-07-21）｜affects：thesis.R、valuation、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 2026 財報後，JPMorgan（Alexander Hess）維持 Overweight 但目標價由 $742 下修至 $700；Evercore ISI（David Motemeden）維持 Outperform 但目標價由 $746 下修至 $722，理由是費用上升軌跡導致估值重新校準
  - 來源：BigGo Finance: "MSCI Beats Q2 Estimates but Analysts Slash Price Targets on Rising Costs"（as_of 2026-07-22）｜affects：valuation、thesis.R、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 1 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20260929/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1185.0,"bear_5y_price":401.4,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":51.7,"ev5y_pct":45.1,"irr_base_pct":8.7,"asym_ratio":3.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":19.74,"pe":27.49,"basis":"FY2026E 共識 EPS（Koyfin 2026-09-26 快照），與終端倍數同用當年度 EPS 當分母"},"eps":{"bull":[23.2,27.0,30.8,35.0,39.5],"base":[22.5,25.54,28.35,31.19,34.31],"bear":[20.5,19.4,20.2,21.3,22.3]},"pe":{"bull":30,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":2.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MSCI_Q1_2026_Earnings_Call_20260421.md
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 給 Q2 Analytics 營收年增率指引，因大型 implementation 認列的 nonrecurring 收入不會重複，預期回落到中個位數（原話："Analytics year-over-year revenue growth to be roughly 5%"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 表示因 ABF（asset-based fee）表現強勁及假設下半年市場溫和上漲，全年費用預計落在guidance區間的上半段（原話："in the top half of our expense guidance range."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 給出 Q2 有效稅率區間指引（原話："we expect to have an effective tax rate between 18% and 20%."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 重申全年自由現金流展望維持不變，但提醒 Q2 是季節性現金稅支出最高的季度（原話："The free cash flow outlook for the full year is unchanged"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜guidance：CFO 說明因收購案的無形資產攤銷，上修全年 D&A（折舊攤銷）guidance（原話："we updated our full year outlook on D&A by $5 million"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜margin：CFO 定義 Q1 asset-based fee（依資產規模計費）run rate 成長率為 25%，並說明是被指數連結資金流帶動（原話："Asset-based fee run rate growth was 25%"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜margin：CFO 說明 Analytics 收入成長逾 10%，是因本季認列較高的 implementation 一次性（非經常性）收入（原話："implementations recognized in nonrecurring revenues"）
- 2026-04-21｜Henry Fernandez (CEO)｜competition：CEO 被問及 AI 是否改變 Analytics 業務的競爭態勢時，回答目前尚未看到來自傳統對手或新創的激烈競爭（原話："haven't seen any kind of competition or intense competition"）
- 2026-04-21｜Henry Fernandez (CEO)｜competition：CEO 補充公司並未因此放鬆，仍在密切監控該競爭動態（原話："We're not relaxed, we're monitoring and focused on that"）
- 2026-04-21｜Henry Fernandez (CEO)｜competition：CEO 表示在 sustainability（永續評等）領域正從競爭對手手中搶下顯著市占（原話："taking away from competitors on sustainability."）
- 2026-04-21｜Henry Fernandez (CEO)｜capital_allocation：CEO 揭露年初至今的庫藏股買回金額（原話："we repurchased more than $464 million of MSCI shares"）
- 2026-04-21｜Henry Fernandez (CEO)｜capital_allocation：CEO 提到近期完成三筆小型併購案（bolt-on acquisition），鎖定關鍵成長領域（原話："small bolt-on acquisitions in key growth areas"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜capital_allocation：CFO 說明三筆併購案（Vantager、Compass、PM Insights）對 run rate 與費用的貢獻相對有限（原話："a relatively modest contribution to run rate"）
- 2026-04-21｜Henry Fernandez (CEO)｜product：CEO 表示 IndexAI Insights 連接器自二月底推出以來，已有數百家客戶使用（原話："used IndexAI Insights since our launch in late February"）
- 2026-04-21｜Henry Fernandez (CEO)｜product：CEO 提到收購 Compass Financial Technologies，把客製化指數能力延伸到商品、數位資產、股票衍生品等新資產類別（原話："acquisition of Compass Financial Technologies"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜product：CFO 提到公司已推出 active financial product license，讓客戶用 MSCI 指數運算能力做主動型 ETF，能同時挹注訂閱與 ABF 兩種收入（原話："we have launched our active financial product license."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜risk：CFO 預期 Sustainability 與 Climate 產品線的需求壓力與成長趨緩會持續到近期（原話："Sustainability and Climate to continue in the near term."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜risk：CFO 提到 Real Assets 產品線的不動產交易解決方案仍面臨逆風（原話："headwinds with our property transaction solutions"）
- 2026-04-21｜Henry Fernandez (CEO)｜risk：CEO 被問及市場動盪是否影響業務時，表示除了波灣地區的商談與展示放緩，其他地區未見伊朗戰爭的影響，客戶維持正常營運節奏（原話："effect of the Iran war anywhere else in the world."）
- 2026-04-21｜Andrew Wiechmann (CFO)｜customer：CFO 說明 Index 產品線在對沖基金客群的訂閱 run rate 成長率達 27%（原話："run rate growth within index with hedge funds"）
- 2026-04-21｜Ashish Sabadra (Analyst)｜customer：分析師指出資產管理公司客群訂閱 run rate 成長率從上季 7% 降到本季 6%，詢問後續動能（原話："it moderated a bit from 7%, I believe, last quarter to 6%"）
- 2026-04-21｜Andrew Wiechmann (CFO)｜customer：CFO 回應資產管理公司成長率變動時，提到匯率因素會影響任一客群的成長率數字（原話："FX factors at play with the growth rates"）
- 2026-04-21｜Henry Fernandez (CEO)｜customer：CEO 回答私募信貸市場的信用風險疑慮對 PCS（私募資產解決方案）業務是順風而非逆風（原話："It's definitely a tailwind for us."）
- 2026-04-21｜Henry Fernandez (CEO)｜commitment：CEO 重申公司致力於透過紀律化部署超額資本來極大化價值創造（原話："we are committed to maximizing value creation"）
- 2026-04-21｜Henry Fernandez (CEO)｜commitment：CEO 透露約一年半前公司已把使用 AI 列為聘用員工的條件之一，藉此推動全公司 AI 採用（原話："we made AI a condition of employment at MSCI."）

### MSCI_Barclays_24th_Annual_Global_Financial_Services_Conference_20260914.md
- 2026-09-14｜Andrew Wiechmann (CFO)｜guidance：CFO 給出第三季 adjusted EBITDA 費用區間，因遣散費及 AUM 連動薪酬墊高（原話："the high $330 million"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜guidance：CFO 預告全年費用可能落在原先財測區間的高端（原話："the higher end of our expense ranges"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜guidance：CFO 說明年初至今 recurring net new 較去年同期成長幅度（原話："up 24%, 25% over last year"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜guidance：CFO 量化 BlackRock 新約對基點費率的兩階段調整幅度（原話："to the basis point fees was 0.1 basis point adjustment"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜margin：CFO 定義 AI 帶來的效益是把 run-the-business 費用成長率壓到低個位數（原話："bring that down to low single-digit type of growth rates"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜margin：CFO 拆解 Q1 到 Q2 基點費率下滑的口徑，歸因於低費率大型 ETF 產品的資產成長（原話："extraordinary growth in lower fee hyperscale ETFs"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜competition：CFO 表示公司在爭取新流入 ETF 資產的市佔上具備獨特位置（原話："capture a significant amount of the market share"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜capital_allocation：CFO 定調併購策略聚焦於加速既有業務的小型收購，不追求新事業線（原話："will likely be bolt-on accelerators"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜capital_allocation：CFO 重申會持續在具吸引力價位大力執行庫藏股買回（原話："buy our stock back at attractive prices"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜product：CFO 給出新產品對今年上半年新增經常性銷售的貢獻比例（原話："40% from new products"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜product：CFO 指出 Index 部門經常性訂閱成長率因新產品加速（原話："accelerate from mid-8% to over 11%"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜product：CFO 說明 Private Assets 旗下 PCS（原 Burgiss）業務訂閱成長率最新一季的加速幅度（原話："up to north of 16% in the most recent quarter"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜risk：CFO 針對 Analytics 與 Sustainability 業務被 AI 顛覆的疑慮，明確表態 AI 現階段是機會而非威脅（原話："we don't today see AI as a threat but more of an opportunity"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜customer：CFO 列舉過去一年在 broker-dealer 客群也出現成長加速（原話："We've seen acceleration with broker-dealers."）
- 2026-09-14｜Andrew Wiechmann (CFO)｜customer：CFO 描述傳統主動式資產管理客群是預算壓力最集中之處（原話："is kind of the epicenter of that pressure"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜commitment：CFO 承諾公司財務目標是加速獲利與自由現金流成長，而非單純衝高利潤率（原話："drive faster profitability and free cash flow growth"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜commitment：CFO 說明即使完成多筆併購，過去一年整體人力仍維持大致持平（原話："our headcount has been roughly flat"）
- 2026-09-14｜Andrew Wiechmann (CFO)｜commitment：CFO 承諾把 AI 節省下來的費用再投資，而不是直接讓利潤率跳升（原話："to reinvest them and accelerate that algorithm"）

### 問答異常語氣（迴避／改口／保留）
- MSCI_Barclays_24th_Annual_Global_Financial_Services_Conference_20260914.md｜問：分析師追問遣散費是否集中在特定事業部門，還是廣泛分布｜答法：CFO 先說主要落在 data/technology 與 Analytics、Index 等大部門，但隨即表示「I don't want to be too specific at this point」，未給出具體部門別數字或比例

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | none | 0 | 4 |
| customer_second_source | found | 1 | 4 |
| customer_concentration_credit | found | 4 | 4 |
| supply_demand_durability | found | 2 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | none | 0 | 4 |
| geo_supply_chain | found | 1 | 4 |
| end_markets | found | 5 | 6 |
| substitute_technology | found | 2 | 4 |
| channel_business_model_shift | none | 0 | 4 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 2 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **competitive_share_entrants**（none）：MSCI index provider market share gaining OR losing 2026；MSCI new entrant OR displace threat index providers 2026；MSCI competitor design win asset management analytics 2026；MSCI vs S&P Dow Jones FTSE Russell market share trend 2025 2026
- **reg_tariff_export**（none）：MSCI Inc tariff section 232 2026；MSCI Inc export control entity list index provider 2026；MSCI Inc China index restriction trade tension 2026；financial data index provider tariff exposure supply chain 2026
- **channel_business_model_shift**（none）：MSCI distribution channel disruption OR shift 2026；MSCI business model transition subscription OR platform 2026；index and analytics industry channel disintermediation D2C 2026；MSCI go-to-market change 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MSCI","date":"2026-09-29","schema":"v15.2","contract":"v19","company_name":"MSCI Inc."},"oneliner":"全球投資的記分板：MSCI 靠指數標準收使用費，留存 95.3%、ABF run rate 年增 25%；但大型 ETF 客戶壓費率、費用指引連升，FY1 本益比 27.5 倍、PEG 約 2，好生意、價格合理不便宜。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20260929/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20260929/scenario.json","answers":{"q1_business":{"verdict":"賺的是全球資產管理業的標準使用費：錢卡在指數授權這一節點。資產主把 MSCI 指數寫進基準，基金、ETF 與交易商就得付訂閱費和按資產計的費用。","reasoning":"營收分四段：Index（訂閱加按資產計費 ABF）、Analytics（風險與因子模型訂閱）、Sustainability and Climate、Private Assets。Q2 營收 8.67 億美元，GAAP 營益率 56.2%，調整後 EBITDA 利潤率 62.1%，TTM 毛利率 83.0%。成長主力在 Index：上半年 Index 營收年增 17.6%，其中 ABF 年增 26.6%、訂閱年增 10.3%。ABF run rate 約 9.48 億美元，接近全公司營收年化的三成，這塊跟著掛鉤 ETF 的資產規模上下。Analytics 有機訂閱 run rate 年增 6.6%；Private Assets 段 Q2 營收 7,470 萬美元，有機年增 4.4%。各段占營收比重事實表未涵蓋。產業時鐘在擴張期：掛鉤 MSCI 指數的 ETF 資產逾 2.8 兆美元，Q2 流入近 400 億美元，留存率由 94.4% 升到 95.3%；依據是資金流與留存，不是股價。供需持久度：訂閱需求屬結構性持久，基準一旦寫進投資契約很少換；ABF 屬週期性，跟著股市位階走。單點依賴：BlackRock 占 FY2025 營收 10.8%、占 Index 段 18.7%（FY2022 為 17.4%），其中 96.5% 是按資產計費，集中度在升。產業態勢是雙向拉鋸：被動與系統化投資擴大、交易生態對指數資料的需求上升，屬結構轉好；永續需求週期性下行、歐盟 ESG 評等授權新規、主動 ETF 檔數超過被動，屬其他結構變數。","fact_refs":["f_kpi0_total_operating_revenue_","f_kpi1_adjusted_ebitda_margin_n","f_kpi2_gaap_operating_margin","f_kpi3_free_cash_flow_non_gaap","f_kpi5_retention_rate","f_kpi6_index_analytics_organic_","f_peer_msci_gross_margin_pct"],"verdict_values":{"revenue_quality":"高：訂閱留存 95.3%、Index 留存逾 97%；按資產計費約占營收近三成，品質高但隨股市位階波動","unit_econ_note":"TTM 毛利率 83.0%、營益率 55.7%、FCF 利潤率 44.8%；Q2 GAAP 營益率 56.2%、調整後 EBITDA 利潤率 62.1%、FCF 3.26 億美元；SBC 約占營收 2.9%","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"標準制定者按資產收費加高留存訂閱，輕資產、高利潤率"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：留存率由 94.4% 升到 95.3%（Q2 新聞稿），Q1 掛鉤 ETF 流入逾千億美元、基準資產逾 21 兆美元；ABF 部分屬週期性，隨股市位階波動","bargaining":{"up":"供應端是資料來源與人才，事實表未涵蓋供應商集中度，未見單一供應商依賴","down":"最大客戶 BlackRock 占營收 10.8%、占 Index 段 18.7% 且上升；2025 年底續約時部分產品費率下限調低，財務長稱調整約 0.1 基點（2026-09-14 巴克萊會議）","geo":"台灣占 MSCI 新興市場指數 24.8%（2026-04-30），新興市場產品費率較高，地緣事件會同時打到資產規模與費率組合"},"profit_pool_dir":"利潤池往指數商與超大型 ETF 發行商兩端集中；傳統主動管理人是預算壓力最集中處（2026-09-14 巴克萊會議財務長原話）","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與被動化滲透率；跑道判斷改以管理層揭露的第二曲線成長率為據，未展開屬資料缺口，不是不重要"}}}},"q2_moat":{"verdict":"護城河寬、方向持平：指數基準的網絡效應還在加深（留存上升、交易生態擴張），但大型 ETF 客戶把費率往下壓，兩股力量互相抵銷。","reasoning":"機制：資產主與顧問把 MSCI 指數寫進投資政策與績效基準，基金經理人、ETF 發行商、做市商與對沖基金就得跟著買授權與資料。用的人越多，流動性越集中在 MSCI 指數上，換掉的成本越高。可證方向：同業只有利潤率可比，ROIC 事實表未涵蓋。MSCI TTM 營益率 55.7%，高出 MCO 9.6 個百分點、SPGI 14.1 個百分點、FDS 26.1 個百分點；毛利率 83.0% 對 SPGI 70.9%、MCO 75.0%。只有單期資料，差距擴大或收窄無法判，改看留存：全公司留存 95.3%（去年同期 94.4%），Index 留存逾 97%，對沖基金客群同樣逾 97%（Q2 法說財務長）。執行力 9 分：兩季推出 80 多項新品，Index 訂閱 run rate 由 8% 中段加速到 11% 以上，PCS 加速到 16% 以上。定價力 8 分：調價對新增銷售的貢獻穩定，但 BlackRock 續約調低部分產品費率下限，低費率大型 ETF 資產占比上升，平均基點連兩季下滑，大客戶手上有議價力。執行面擴大、定價面縮減，合起來持平。威脅都屬點對點：AI 複製 ESG 評等只打永續段；自助式指數平台與主動 ETF 分流屬邊緣競爭，公司已用 Foxberry 平台與主動型產品授權回應。","fact_refs":["f_peer_msci_gross_margin_pct","f_peer_msci_operating_margin_pct","f_peer_msci_fcf_margin_pct","f_peer_spgi_gross_margin_pct","f_peer_spgi_operating_margin_pct","f_peer_mco_gross_margin_pct","f_peer_mco_operating_margin_pct","f_peer_fds_operating_margin_pct","f_kpi5_retention_rate","f_kpi6_index_analytics_organic_","f_kpi7_fy2026_guidance_q2"],"verdict_values":{"moat":{"mechanism":"指數基準的網絡效應：資產主選基準，管理人、ETF 與交易生態被迫跟隨，流動性集中讓替換成本逐年升高","execution":9,"pricing":8,"grade":"A","trend":"→","trend_evidence":"執行面擴大：留存率 94.4% 升到 95.3%，Index 訂閱 run rate 加速到 11.1%；定價面縮減：BlackRock 續約調低費率下限，平均基點連兩季下滑；兩者抵銷為持平","competitor_notes":[{"name":"SPGI","strategy_note":"S&P DJI 是指數業最直接的對手，美國大型股基準強；毛利率 70.9%、營益率 41.6%，低於 MSCI，反映評等與資料業務混合；SPICE 自助平台在客製指數正面競爭"},{"name":"MCO","strategy_note":"主業是信評與風險分析，和 MSCI 在氣候、ESG 資料與風險分析有交集，指數業務不重疊；營益率 46.1%，是表中利潤率最接近 MSCI 的同業"},{"name":"FDS","strategy_note":"和 MSCI Analytics 在投資組合分析與因子模型搶同一批資產管理客戶；營益率 29.6%，工作站軟體的成本結構明顯較重"}],"peer_na_reason":"同業 ROIC 事實表未涵蓋，以營益率差距與留存率代替；差距只有單期，趨勢無法判","threats":[{"level":"🟡","text":"AI 低成本複製部分 ESG 評等，永續評等的定價溢價被侵蝕；影響限於 S&C 段","p":0.35,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"主動 ETF 檔數已超過被動，資金若改流向不掛鉤指數的產品，ABF 流入動能放慢；公司已推主動型產品授權回應","p":0.3,"evidence_refs":["end_markets#4"]},{"level":"🟡","text":"最大客戶 BlackRock 要求降費或停用 MSCI 指數，公司風險因子已自承","p":0.2,"evidence_refs":["customer_concentration_credit#1"]},{"level":"🟡","text":"自助式指數設計平台（S&P SPICE、Merqube）降低客製指數門檻；公司 2024 年已收購 Foxberry 平台因應","p":0.3,"evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是投資組合經理與交易員，決策者是資產主董事會與投資顧問，付款者是資產管理公司與 ETF 發行商，三個角色都成立；基準寫進投資契約與法遵要求，是需要不是想要。讀數：留存率 95.3%（去年同期 94.4%），基準資產逾 21 兆美元，Q1 掛鉤 ETF 流入逾千億美元"},{"item":"決策層級","level":"🟢","text":"替代要在資產主選基準這一層決定，換基準牽涉投資政策修訂、績效紀錄銜接與指數基金換倉成本，不是採購部門比價。讀數：Index 留存逾 97%，對沖基金客群同樣逾 97%，調價對新增經常性銷售的貢獻穩定（Q2 法說財務長）"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈是終端投資人到 ETF 發行商再到指數商；ETF 費率戰把壓力往上游推，買方高度集中（BlackRock 占 Index 段 18.7% 且上升），2025 年底續約取得部分產品較低費率下限，平均基點連兩季下滑。長期需求還在，但超大型 ETF 的分成在往發行商那邊移，發行商自編指數是潛在替代"},{"item":"社會容忍度","level":"🟡","text":"指數商的影響力受歐美監管與媒體關注（10-K 風險揭露），MSCI Limited 屬英國 FCA 授權基準管理機構；歐盟 ESG 評等規範自 2026-07-02 起要求取得 ESMA 授權。查無反壟斷調查報導。美國政治對 ESG 的反彈與監管對指數集中度的關注，會限制永續產品與大幅漲價的空間"}],"roiic":"事實表未涵蓋（投入資本、商譽與收購金額未入表）","reinvest_rate":"低：資本支出財測 1.60–1.70 億美元，約為自由現金流財測 14.85–15.45 億美元的一成；收購屬小型補強，金額事實表未涵蓋","endo_ceiling":10,"formula_note":"資本公式（增量 ROIC 乘再投資率）算不出來：投入資本、商譽與收購金額事實表未涵蓋。實體再投資率低，成長靠費用化的產品開發與銷售，公式會低估。改用有機代理：訂閱 run rate 約 8%（全公司 8.1%）與 ABF 長期約 9%（股市上漲加資金流、扣費率拖累，屬判斷值）混合，營收約 9%，加少量營業槓桿，EPS 有機上界取 10%，不含淨回購。當期稅後營業利益率約 45%（TTM 營益率 55.7% 扣 Q2 指引稅率 18–20%），周轉率因投入資本缺值無法計算"}}}},"q3_growth":{"verdict":"五年後跑道寬：核心被動授權趨於成熟，但對沖基金交易生態、私募資產財富管理通路、AI 內容授權三條新曲線已經看得到數字，只是規模還小。","reasoning":"成長來源：量為主（ABF 隨資產規模、訂閱新客與新模組），價為輔（調價貢獻穩定），併購小，淨回購每年約 2%。共識 EPS：FY2026E 19.74、FY2027E 22.5、FY2028E 25.54，兩年年化 13.7%；FY2025 實際值與分析師家數事實表未涵蓋，以兩年代替三年。內生上界取 10%（推導見護城河題）。共識高出約 3.7 個百分點，歸因：淨回購約 2 個百分點，2026 年 ABF 在資產新高時墊高的基期延續約 1 個百分點，其餘靠利潤率小幅擴張。缺口可歸因，但其中一塊要股市不回檔才成立。跑道：被動化滲透率事實表未涵蓋，燈號依第二曲線判斷。Index 對沖基金客群訂閱 run rate 年增 19%，客製指數有機訂閱 run rate 23%，PCS 16% 以上，首份 AI 模型訓練授權已簽（Q2 法說）；CEO 自評對沖與交易生態還在九局的第二、三局。衰退信號亮兩個：自身本益比、市銷率、EV/S 都在近四個年度端點最低；永續段需求收縮（美洲取消多，未來兩季淨新增約零到小負）。","fact_refs":["f_kpi6_index_analytics_organic_","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi7_fy2026_guidance_q2","f_pe_percentile","f_ps_percentile","f_ev_s_percentile"],"verdict_values":{"growth":{"driver_mix":"量為主（ABF 隨掛鉤資產規模、訂閱新客與新模組），價為輔（調價貢獻穩定），小型併購，淨回購每年約 2%","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"有機代理：訂閱 run rate 約 8% 加 ABF 長期約 9% 混合，營收約 9%，利潤率大致持平再加少量營業槓桿，EPS 有機約 10%；資本公式因投入資本與收購金額事實表未涵蓋無法計算","segments":[{"item":"Index","value":"上半年營收年增 17.6%：ABF 年增 26.6%、訂閱年增 10.3%；有機訂閱 run rate 年增 11.1%，ABF run rate 約 9.48 億美元、年增 25%；掛鉤 ETF 資產逾 2.8 兆美元"},{"item":"Analytics","value":"Q1 營收 1.90 億美元、年增 10.3%（含一次性導入收入）；Q2 有機營收年增約 7%，有機訂閱 run rate 年增 6.6%"},{"item":"Sustainability and Climate","value":"氣候 run rate 年增近 12%；永續段美洲取消多，管理層預期未來兩季淨新增約零到小負；First Street 完成後約增 1,000 萬美元訂閱 run rate"},{"item":"All Other–Private Assets","value":"Q2 營收 7,470 萬美元、年增 4.9%（有機 4.4%），有機訂閱 run rate 年增 8.3%；其中 PCS 訂閱 run rate 加速到 16% 以上"},{"item":"分段占比","value":"各段占營收比重事實表未涵蓋"}],"decay_signals":[{"signal":"產業估值倍數近 3 年系統性下移","lit":true,"evidence":"本益比、市銷率、EV/S 都在近四個年度端點最低；同業倍數事實表未涵蓋，以自身代理"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"evidence":"限於永續段：美洲客戶砍預算、AI 可複製部分 ESG 評等；氣候與指數未見"},{"signal":"EPS CAGR 顯著高於 Rev CAGR","lit":false,"evidence":"營收共識事實表未涵蓋，無法判；Q2 調整後 EPS 年增近 19% 對有機營收逾 12%，單季不構成"},{"signal":"SBC/Rev 超過 5% 且逐年上升","lit":false,"evidence":"Q2 推算約 2.9%"},{"signal":"maintenance capex 占 FCF 超過 60%","lit":false,"evidence":"資本支出財測約為 FCF 財測的一成"},{"signal":"毛利率連 2 季 YoY 下滑","lit":false,"evidence":"季度毛利率序列事實表未涵蓋，未能驗證"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"掛鉤 ETF 資金流創新高，財務長稱在新流入資產的市占位置獨特"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：現金大多回給股東、SBC 稀釋低，但回購買在高本益比，收購回報還沒證實。","reasoning":"現金流：Q2 自由現金流 3.26 億美元，TTM FCF 利潤率 44.8%，FY2026 財測 14.85–15.45 億美元；資本支出財測 1.60–1.70 億美元，約自由現金流的一成，屬輕資產。現金去向：今年到 7 月 20 日回購約 6.11 億美元（Q1 法說逾 4.64 億、Q2 法說 1.47 億、均價約 558 美元）；併購多筆小型補強（Vantager、Compass、PM Insights、First Street）；First Street 與回購部分用循環信貸支應，利息費用財測因此上修。股息金額與債務到期結構事實表未涵蓋，情境試算股息記 0、淨回購記 2%，合計低估股東回報。淨回購 2% 的算法：年化回購約 11 億美元，對照市值約 400 億美元（市銷率 11.84 除以 FCF 利潤率 44.8% 得 P/FCF 約 26.4 倍，乘 FCF 財測中位數），約 2.7%，扣 SBC 與舉債支應的部分取 2%。計分：回購，558 美元對 FY2026E EPS 19.74 的買入收益率約 3.5%，要 10 年期殖利率低於 1.5% 才過，判不過（10 年期殖利率事實表未涵蓋）；併購，金額與實現回報事實表未涵蓋，Burgiss 收購後約兩年半才換好團隊，私募資產段 Q2 有機營收只增 4.4%，Fabric 去年沖回或有對價，證據偏負，判不過；SBC 約占市值 0.25%，遠低於每年 1.5%，過。","fact_refs":["f_kpi3_free_cash_flow_non_gaap","f_kpi4_stock_based_compensation","f_kpi7_fy2026_guidance_q2","f_peer_msci_fcf_margin_pct","f_ps_current","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"收購金額與實現回報事實表未涵蓋；Burgiss 收購後約兩年半才換好團隊，私募資產段 Q2 有機營收只增 4.4%，Fabric 去年沖回或有對價，現有證據偏負，判不過"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購均價約 558 美元對 FY2026E EPS 19.74，買入收益率約 3.5%；要 10 年期殖利率低於 1.5% 才過（10 年期殖利率事實表未涵蓋），判不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 約占營收 2.9%，除以市銷率 11.84 約占市值 0.25%，加上持續回購，淨稀釋遠低於每年 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自有機訂閱與按資產計費；Vantager、Compass、PM Insights 對 run rate 貢獻有限，First Street 約增 1,000 萬美元訂閱 run rate，不靠併購撐成長"}}}},"q5_valuation":{"verdict":"現價要的是 EPS 每年複合一成出頭、五年後本益比仍有 24 倍；成長我信，倍數回升我不押，價格合理但不便宜。","reasoning":"FY1 本益比 27.5 倍、FY2 24.1 倍，trailing 29.6 倍；本益比、市銷率 11.8 倍、EV/S 13.7 倍都落在近四個年度端點最低（只有四個年度點，不是五年分位）。PEG：FY1 本益比 27.5 除以兩年 EPS 年化 13.7%，約 2.0，在合理區上緣。共識 EPS 近期幾乎沒動（FY1、FY2 修正 0%，FY3 加 0.08%）。賣方平均目標價約 692 美元、區間 570–760；Q2 後 JPMorgan 由 742 降到 700、Evercore 由 746 降到 722，理由是費用上升。十二個月基本情境：FY2027E 22.5 乘 26 倍約 585 美元，上檔 7.8%；兩到三年：FY2028E 25.54 乘 25 倍約 639 美元，上檔 17.6%。同業前瞻本益比事實表未涵蓋，無法做跨同業倍數對照。結論：價格合理不便宜；倍數已先修正，下檔有一部分已被吃掉。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比與 PEG（品質複利型優先用這兩把尺）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，未收同業前瞻本益比；終端倍數改以自身年度端點與成長熄火情境錨定，屬資料缺口"},"fwd_pe":27.49,"peg":2.0,"percentile_5y":0,"val_light":"🟡","val_light_derivation":"FY1 本益比 27.5 倍、PEG 約 2.0，位於合理區上緣；倍數在近四個年度端點最低（分位 0，非真五年序列）；成長可信但倍數沒有擴張空間，判黃","upside_short_pct":7.8,"upside_mid_pct":17.6,"denominator_disputed":false,"denominator_note":"分母用 FY2026E 共識 19.74，事實表未標 GAAP 或調整後；trailing 29.6 倍用 GAAP 分母，兩者口徑不同不混用。Q2 單季 EPS 對共識是勝是負，各彙整站說法矛盾，但不影響全年共識分母"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方：把 2026 年股市新高帶來的 ABF 高成長當成常態，同時低估大型 ETF 客戶壓費率的力道。","reasoning":"看錯的三條路寫在反證紀錄。技術面：股價 542.72 美元，低於 52 週均線 565.73 與 104 週均線 564.28，高於 250 週均線 517.85；250 週均線 13 週斜率為負 0.08%，長期趨勢走平。RSI 41.2，26 週報酬 2.8%，沒有過熱。歷史最大回撤與空方最強數字事實表未涵蓋。管理層在 2026-09-14 巴克萊會議被問到遣散費落在哪些部門時不願細說，屬資訊保留，併入費用監控。價值陷阱風險判黃：亮兩個衰退信號（自身倍數系統性下移、永續段需求收縮），核心指數與訂閱未見衰退。","fact_refs":["f_price_at_dd","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_rsi14","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"估值下移、永續段縮水；核心指數未見衰退"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":19.74,"pe":27.49,"basis":"FY2026E 共識 EPS（Koyfin 2026-09-26 快照），與終端倍數同用當年度 EPS 當分母"},"eps":{"bull":[23.2,27.0,30.8,35.0,39.5],"base":[22.5,25.54,28.35,31.19,34.31],"bear":[20.5,19.4,20.2,21.3,22.3]},"pe":{"bull":30,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":2.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"max_dd":{"lo":-45,"hi":-25,"basis":"事實表未涵蓋歷史最大回撤，改用壓力推導：ABF run rate 約 9.48 億美元，接近營收年化的三成，隨股市位階走；股市跌三成時 EPS 約降 10–12%，本益比由 27.5 倍壓到 17–21 倍，股價落在負 25% 到負 45%。觸發情境是熊市疊加費用上修。壓力測試四項過三項：大客戶降費、永續段再縮、股市跌三成各自可吸收；三者合併再加倍數壓縮則不過","trigger_time":null},"basis":{"bull":"Index 訂閱 run rate 維持 11% 以上，ABF 每年增 12–15%，私募資產與對沖基金新品放量，營業槓桿回來；終端 30 倍，回到過去年度端點區間（確切值事實表未涵蓋）","base":"FY2027–FY2028 用共識 22.5 與 25.54，之後年增 11%、10%、10%，不假設利潤率擴張；終端 24 倍，低於現行 FY1 27.5 倍，對應成長放緩到一成","bear":"股市修正壓 ABF、大客戶再壓費率、永續段續縮而費用剛性，FY2031 EPS 只到 22.3；終端 18 倍，取成長熄火到一成以下時的倍數；同業前瞻倍數事實表未涵蓋，無法做同業對照"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q1 平均基點因 BlackRock 新約下限下滑，Q2 再因低費率大型 ETF 資產占比上升而下滑；BlackRock 占 Index 段由 17.4% 升到 18.7%；主動 ETF 檔數已超過被動","assumption":"指數基準的黏性足以讓費率只隨組合變動，不隨議價下滑","consequence":"大型 ETF 發行商若每次續約都往下壓，ABF 成長長期落後資產規模 15 個百分點以上，EPS 年增掉到中個位數，本益比落到 18 倍，五年後股價約 400 美元以下","ruling":"部分採納：Q2 下滑主因是資產組合（Q2 法說財務長），BlackRock 新約調整約 0.1 基點（2026-09-14 巴克萊會議），目前是慢性壓力，不是崩壞。和唯一致命點部分重疊：那條是一次性換指數，這條是逐年壓費率的慢性版，已放進 bear 路徑與 30% 機率","watch":"ABF run rate 年增率減期末掛鉤 ETF AUM 年增率","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#2","end_markets#4"],"fact_refs":["f_kpi6_index_analytics_organic_"]},{"view":"論點失敗","evidence":"AI 工具可低成本解析永續揭露、複製部分 ESG 評等；歐盟新規自 2026-07-02 起要求 ESG 評等商取得 ESMA 授權；管理層預期 S&C 段未來兩季淨新增約零到小負，CEO 稱永續需求是拉長的週期性下行","assumption":"永續段只是週期性低迷，不是被替代","consequence":"AI 替代若成真，S&C 段長期負成長，並拖累 Analytics 的定價","ruling":"採納但限縮：衝擊集中在 S&C 段；氣候 run rate 仍年增近 12%，掛永續與氣候指數的指數基金資產約 1.3 兆美元，反而支撐 Index","watch":"S&C 段淨新增經常性銷售、Analytics 有機訂閱 run rate","evidence_refs":["substitute_technology#0","regulatory_antitrust#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"費用指引一路往上：2026-04-21 財務長說落在原區間上半，2026-07-21 上修營運費用區間，2026-09-14 又說落在新區間高端並有遣散費；績效型股酬與獎金跟著資產規模走；回購均價約 558 美元，買入收益率約 3.5%；First Street 與回購動用循環信貸","assumption":"營收加速會帶來營業槓桿","consequence":"營收成長但利潤率不升，EPS 只跟營收同速；加上高價回購與舉債，每股價值成長慢於營收","ruling":"採納：base 路徑 FY2029 起只給 10–11%，不假設利潤率擴張；費用由 R4 監控","watch":"調整後 EBITDA 利潤率、費用年增率對營收年增率","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_kpi1_adjusted_ebitda_margin_n","f_kpi7_fy2026_guidance_q2"]},{"view":"價格已反映太多","evidence":"FY1 本益比 27.5 倍、PEG 約 2.0；ABF 年增 25% 有一段來自股市高位；Q2 後 JPMorgan、Evercore 下修目標價","assumption":"共識兩年 EPS 年化 13.7% 沒有計入股市回檔","consequence":"股市持平一年，ABF 成長回到個位數，FY2027 EPS 低於 22.5，本益比再壓到 23 倍，一年內下跌一成以上","ruling":"部分反駁：倍數已在近四個年度端點最低，26 週只漲 2.8%，市場已先扣掉費用上修；但股市高位帶來的收益沒有被折價，所以不追價，等 474 美元","watch":"FY2027 共識 EPS 修正方向、前瞻本益比","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 542.72","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=542.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"費率下滑是議價權流失還是組合效應","cause":"新證據","side_a":"議價權流失：BlackRock 續約調低部分產品費率下限，Q1 平均基點下滑；BlackRock 占 Index 段由 17.4% 升到 18.7%；公司風險因子自承客戶可能要求降費或停用","side_b":"組合效應：Q2 下滑主因是資金集中流入美國以外已開發市場與全球型的低費率大型 ETF，新興市場流入變少（Q2 法說財務長）；BlackRock 調整約 0.1 基點（2026-09-14 巴克萊會議）；ABF run rate 仍年增 25%","ruling":"可調和，屬程度差異：短期以組合為主，但大客戶下限調低是結構性的，每次續約只會往下；定價力給 8 分不給 9 分","evidence_level":"公司申報加法說原話","settle_metric":"平均基點對照期末掛鉤 ETF AUM 的新興市場占比","if_then":["若 ABF run rate 年增率落後期末掛鉤 ETF AUM 年增率超過 15 個百分點且連 2 季，則停止加碼，H2 判為反轉","反向：若新興市場流入回升且平均基點持平或回升，則維持費率下滑只是組合效應的判斷"],"evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2"]},{"axis":"費用指引前後說法","cause":"新證據","side_a":"管理層：自稱審慎的財務管理者，費用上修是自願加碼投資，手上有調節槓桿（2026-07-21 Q2 法說，CEO 與財務長）","side_b":"指引一路往上：2026-04-21 財務長說落在原區間上半；2026-07-21 上修營運費用區間 4,500 萬美元；2026-09-14 巴克萊會議又說落在新區間高端，Q3 調整後 EBITDA 費用約 3.3 億美元高段並含遣散費；被追問遣散費分布時財務長不願細說","ruling":"可調和，屬程度差異：上修主因是跟資產規模連動的績效股酬與獎金、First Street 併入，和 ABF 收入同向；但管理層已明說 AI 省下的錢要再投資、不讓利潤率跳升，營業槓桿不能指望","evidence_level":"三場管理層原話前後對照","settle_metric":"FY2026 實際調整後 EBITDA 費用對 13.40–13.70 億美元區間；Q4 調整後 EBITDA 利潤率","if_then":["若 FY2026 調整後 EBITDA 費用超過 13.70 億美元上緣且 Q4 利潤率低於 60%，則減碼三分之一並下修 base 路徑","反向：若 Q3 費用在 3.3 億美元高段以內且利潤率守住 61%，則維持"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"管理層指引與交付（一致項）","cause":"新證據","side_a":"2026-04-21 財務長預告 Q2 Analytics 營收年增約 5%，因一次性導入收入不會重複","side_b":"Q2 Analytics 有機營收年增 7%，好於指引；但 Analytics 訂閱銷售偏弱，CEO 歸因於時點不均","ruling":"一致：本季交付不低於自己的指引。訂閱銷售只是時點問題屬未證歸因，登記期限：Q3、Q4 Analytics 有機訂閱 run rate 仍低於 6.6%，歸因就不成立","evidence_level":"法說原話前後對照","settle_metric":"Analytics 有機訂閱 run rate","if_then":["若 Analytics 有機訂閱 run rate 連 2 季低於 6%，則停止加碼，並把 Analytics 移出成長引擎","反向：若回到 7% 以上，視為時點問題已證實"],"evidence_refs":[]},{"axis":"現在買或現在賣的最強論證","cause":"價格變動","side_a":"現在就買：倍數在近四個年度端點最低，26 週只漲 2.8%，RSI 41；管理層在約 558 美元仍在回購，CEO 說願意站在賣股者的對面；Index 訂閱 run rate 加速、留存上升","side_b":"現在就賣：ABF 年增 25% 有一段來自股市高位，費用指引連兩次往上，JPMorgan、Evercore 下修目標價；股價低於 52 週與 104 週均線，週線偏弱；PEG 約 2","ruling":"不可調和，選等價格：生意面站買方（留存與訂閱加速是硬數據），價格面站賣方（基本情境年化約一成、PEG 2.0）。綁住進場的是價格，不是論點","evidence_level":"價格加季報數據","settle_metric":"股價對 FY1 本益比 24 倍（約 474 美元）","if_then":["若股價跌到 474 美元以下且 Index 訂閱 run rate 仍在 10% 以上，則建首批","若股價先漲破 638 美元而 Q3 費用超標，則不追","反向：若 Q3 Index 訂閱 run rate 跌破 9%，即使到價也不建倉"],"evidence_refs":["capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"Index 有機訂閱 run rate 年增率連四季低於 9%，指數標準擴張的論點削弱","type":"假設驗證","maps_to":"H1","metric":"Index 有機訂閱 run rate 年增率","threshold":"低於 9% 連 4 季（現 11.1%）","action":"停止加碼","source_freq":"季報新聞稿／每季","date":"2026-10"},{"n":2,"text":"ABF 成長落後掛鉤 ETF 資產成長太多，代表費率拖累失控","type":"假設驗證","maps_to":"H2","metric":"ABF run rate 年增率減期末掛鉤 ETF AUM 年增率","threshold":"落後超過 10 個百分點連 2 季","action":"停止加碼","source_freq":"季報新聞稿與財報簡報／每季","date":"2026-10"},{"n":3,"text":"新成長曲線沒有接棒，全公司訂閱成長停在 8% 以下","type":"假設驗證","maps_to":"H3","metric":"全公司有機訂閱 run rate 年增率、留存率","threshold":"低於 8% 連 2 季，或留存低於 94.5%","action":"停止加碼","source_freq":"季報新聞稿／每季","date":"2026-10"},{"n":4,"text":"BlackRock 集中度再升且平均基點明顯下滑，大客戶議價轉成實質降費","type":"風險","maps_to":"R1","metric":"BlackRock 占營收比、平均基點年變動","threshold":"BlackRock 占營收超過 12% 且平均基點年降超過 10%","action":"減碼三分之一","source_freq":"10-K 每年；季報每季","date":"2027-02","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":5,"text":"股市修正或新興市場地緣事件讓掛鉤 ETF 資產大跌；訂閱沒壞就分批反買，不停損","type":"風險","maps_to":"R2","metric":"季末掛鉤 ETF AUM 季變動","threshold":"季減超過 15%，同時全公司有機訂閱 run rate 仍在 8% 以上","action":"分批反買","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["geo_supply_chain#0"]},{"n":6,"text":"掛鉤 ETF 資金流入明顯轉弱，主動 ETF 分流開始反映","type":"風險","maps_to":"R3","metric":"掛鉤 MSCI 指數 ETF 單季現金流入","threshold":"連 2 季低於 200 億美元（Q2 近 400 億）","action":"停止加碼","source_freq":"季報法說／每季","date":null,"evidence_refs":["end_markets#4"]},{"n":7,"text":"費用跑贏營收，利潤率連續下滑","type":"風險","maps_to":"R4","metric":"調整後 EBITDA 利潤率年變動","threshold":"連 2 季年減超過 1 個百分點（Q2 62.1%）","action":"減碼三分之一","source_freq":"季報新聞稿／每季","date":"2026-10","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"n":8,"text":"永續段持續失血，AI 替代或監管成本開始吃掉這一段","type":"風險","maps_to":"R5","metric":"S&C 段淨新增經常性銷售","threshold":"連 3 季為負","action":"停止加碼","source_freq":"季報法說／每季","date":null,"evidence_refs":["substitute_technology#0","regulatory_antitrust#1"]},{"n":9,"text":"BlackRock 宣布大型 iShares MSCI 產品改掛其他指數或自編指數","type":"Single Thing","maps_to":"Single Thing","metric":"iShares 產品標的指數變更公告","threshold":"任一大型 iShares MSCI 產品宣布換指數","action":"清倉","source_freq":"BlackRock 與 MSCI 公告／事件","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":10,"text":"價格回到 FY1 本益比 24 倍且指數訂閱仍健康，建首批","type":"估值rearm","maps_to":"H1","metric":"股價、Index 有機訂閱 run rate","threshold":"股價 474 美元以下，且 Index 訂閱 run rate 年增 10% 以上","action":"建首批","source_freq":"每日股價；每季財報","date":null},{"n":11,"text":"價格跌到 FY2 本益比約 18.7 倍而論點未削弱，加第二批","type":"加碼","maps_to":"H1","metric":"股價、H1 至 H3 狀態","threshold":"股價 420 美元以下，且 H1 至 H3 都沒有削弱","action":"加第二批","source_freq":"每日股價；每季財報","date":null},{"n":12,"text":"價格漲到 FY2028E 本益比約 27.4 倍而共識沒有上修，先收一部分","type":"減碼","maps_to":"R4","metric":"股價、FY2028E 共識 EPS","threshold":"股價 700 美元以上，且 FY2028E 共識未上修","action":"減碼三分之一","source_freq":"每日股價；共識每月","date":null},{"n":13,"text":"FY2026 年報與 FY2027 財測出爐後重跑研究","type":"複審日期","maps_to":"H2","metric":"年報客戶集中度、FY2027 費用財測","threshold":"年報發布","action":"重跑研究","source_freq":"年度","date":"2027-02"}],"kill_metrics":[{"metric":"Index 有機訂閱 run rate 年增率","bear_threshold":"低於 7% 連 2 季（現 11.1%）","window":"每季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"全公司留存率","bear_threshold":"低於 93.5%（現 95.3%）","window":"每季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"調整後 EBITDA 利潤率","bear_threshold":"低於 58% 連 2 季（Q2 62.1%）","window":"每季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"BlackRock 占 Index 段營收比","bear_threshold":"超過 22%，或任一大型 iShares 產品換指數","window":"每年（10-K）","source":"MSCI 10-K 客戶集中度揭露","last_status":"warning"},{"metric":"ABF run rate 年增率減期末掛鉤 ETF AUM 年增率","bear_threshold":"落後超過 15 個百分點連 2 季","window":"每季","source":"MSCI 季報新聞稿與財報簡報","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"股價回到 474 美元以下（FY1 本益比 24 倍），且 Index 有機訂閱 run rate 年增仍在 10% 以上","exec_line":"現價基本情境年化約一成，合理不便宜；474 美元以下建首批，420 美元以下加第二批，700 美元以上減碼三分之一，BlackRock 換指數即清倉"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把平均基點下滑當成議價權流失，但 Q2 下滑主因是資金流向低費率大型 ETF 的組合變化，BlackRock 新約調整約 0.1 基點，ABF run rate 仍年增 25%；倍數已壓到近四個年度端點最低","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把平均基點下滑當成議價權流失，但 Q2 下滑主因是資金流向低費率大型 ETF 的組合變化，BlackRock 新約調整約 0.1 基點，ABF run rate 仍年增 25%；倍數已壓到近四個年度端點最低"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=2.77, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"指數標準持續擴張：Index 有機訂閱 run rate 年增維持 9% 以上，Index 留存率維持 96% 以上","2y":null,"5y":"FY2031 前 Index 訂閱 run rate 年增平均不低於 9%","10y":null,"threshold":"年增 9% 以上（現 11.1%）；留存 96% 以上（現逾 97%）","source":"每季財報新聞稿 Index 段 run rate 與留存率","drift_rule":"連 4 季低於 9% 削弱；連 6 季低於 8% 反轉"},{"id":"H2","text":"按資產計費的規模成長勝過費率拖累：ABF run rate 年增率不落後期末掛鉤 ETF AUM 年增率超過 10 個百分點","2y":"FY2028 前每季費率拖累不超過 10 個百分點","5y":null,"10y":null,"threshold":"拖累 10 個百分點以內","source":"每季財報的 ABF run rate、期末掛鉤 ETF AUM、平均基點","drift_rule":"連 2 季拖累超過 10 個百分點削弱；連 3 季超過 15 個百分點反轉"},{"id":"H3","text":"新成長曲線接棒：全公司有機訂閱 run rate 年增升到 9% 以上（現 8.1%），留存率守住 94.5%","2y":"FY2028 前全公司有機訂閱 run rate 達 9%","5y":null,"10y":null,"threshold":"低於 8% 連 2 季，或留存低於 94.5%","source":"每季財報新聞稿全公司訂閱 run rate 與留存率；法說的對沖基金、PCS、客製指數成長率","drift_rule":"連 2 季低於 8% 削弱；連 3 季低於 7% 反轉"}],"R":[{"id":"R1","text":"最大客戶 BlackRock 議價：占營收 10.8%、占 Index 段 18.7% 且逐年升，續約可再壓費率下限，或把產品移到自編指數","h_ref":"H2","clock":"🐢","threshold":"BlackRock 占營收超過 12% 且平均基點年降超過 10%","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R2","text":"ABF 對股市位階的曝險：掛鉤 ETF 資產在歷史高點，股市修正或新興市場地緣事件（台灣占 EM 指數 24.8%）會同時壓資產規模與費率組合","h_ref":"H2","clock":"⚡","threshold":"季末掛鉤 ETF AUM 季減超過 15%","evidence_refs":["geo_supply_chain#0"]},{"id":"R3","text":"主動 ETF 分流：主動 ETF 檔數已超過被動、三年資產年化 59%，資金若轉向不掛鉤指數的產品，ABF 流入動能變慢","h_ref":"H2","clock":"🐢","threshold":"掛鉤 ETF 單季現金流入連 2 季低於 200 億美元","evidence_refs":["end_markets#4"]},{"id":"R4","text":"費用跑贏營收：FY2026 營運費用財測已上修到 15.35–15.75 億美元，Q3 另有遣散費，管理層明說 AI 省下的錢要再投資","h_ref":"H1","clock":"🔥","threshold":"調整後 EBITDA 利潤率連 2 季年減超過 1 個百分點（Q2 62.1%）","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"id":"R5","text":"永續段縮水與替代：AI 能低成本複製部分 ESG 評等，歐盟新規自 2026-07-02 起要求取得 ESMA 授權，美洲客戶持續砍預算","h_ref":"H3","clock":"🔥","threshold":"S&C 段淨新增經常性銷售連 3 季為負","evidence_refs":["substitute_technology#0","regulatory_antitrust#1"]}],"single_thing":{"description":"BlackRock 把大型 iShares MSCI 產品改掛其他指數商或自編指數，或下次續約把費率砍到明顯低於現行下限","why_fatal":"BlackRock 占 Index 段營收 18.7%、占全公司 10.8%，幾乎全是按資產計費，營收少掉這塊幾乎全是利潤，EPS 下修可近兩成（推估）。更要命的是它會打破基準一旦用了就不換的前提，其他 ETF 發行商會跟著議價，倍數跟著重估。股市修正對 ABF 的衝擊金額更大，但會回來；客戶換指數不會","if_happens":"清倉並重跑研究；本益比朝 18 倍靠","how_monitor":"iShares 產品標的指數變更公告、每年 10-K 的最大客戶占比、每季平均基點對照掛鉤 ETF 資產","probability":"約 5%（12–24 個月）；2025 年底剛續約並調整過下限，近期再換的誘因低"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟡","long_term_confidence":"高","fpe_fy2":24.12,"peg_fy2":1.76,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":19.74,"FY2027E":22.5,"FY2028E":25.54},"fy_end_month":12,"eps_basis":"Koyfin 共識 EPS（2026-09-26 快照），事實表未標 GAAP 或調整後；FY2025A 實際值事實表未涵蓋，三年年化改以 FY2026E 到 FY2028E 兩年 13.7% 代替"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"Q3 FY2026 財報：Q3 調整後 EBITDA 費用（財務長給 3.3 億美元高段）、First Street 併入後的 run rate、S&C 淨新增","impact":"高","watch":"Index 訂閱 run rate 是否守住 11%、平均基點走向"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 FY2027 費用財測","impact":"高","watch":"費用成長率對營收成長率、回購節奏"},{"date":"2026-Q4","date_precision":"quarter","type":"regulatory","event":"歐盟 ESG 評等規範 2026-07-02 生效後的 ESMA 授權進度","impact":"低","watch":"S&C 段是否出現合規成本或產品調整"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
