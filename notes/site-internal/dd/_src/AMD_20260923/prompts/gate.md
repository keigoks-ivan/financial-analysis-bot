你是 DD 管線 v20 的判斷層閘（gate），標的 AMD（20260923）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝11536 USD million｜期間與口徑：Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results, https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-27，公告於 2026-08-04））
  - 註記：Street 共識約 $11.31B，實際 $11.536B（beat）（來源：web_search 彙整多家財經媒體引述 LSEG/Wall St. 共識，非公司原始揭露）
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝27 %｜期間與口徑：Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-27，公告於 2026-08-04））
  - 註記：未查得明確 Street 共識營業利益率數字；EPS 端可比對：non-GAAP EPS $1.66 vs 共識 $1.62（beat，來源：web_search 多家財經媒體）
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝17 %｜期間與口徑：Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-27，公告於 2026-08-04））
  - 註記：N/A（Street 通常僅追蹤 non-GAAP 口徑，未查得 GAAP 營業利益率共識）
- `f_kpi5_q3_fy2026_guidance`（q1_business）｜管理層 Q3 FY2026 財測 guidance＝營收約 $13.0B ± $300M；non-GAAP 毛利率約 56% text｜期間與口徑：發布於 2026-08-04，指引對象為 Q3 FY2026／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results（numbers.latest_quarter_kpis.items[5]，as_of 發布於 2026-08-04，指引對象為 Q3 FY2026）
  - 註記：公司指引中值 $13.0B 高於彼時 LSEG 共識 $12.52B（來源：web_search 財經媒體引述）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-04 date｜期間與口徑：2026-08-04／距今 36 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-04）
- `f_peer_amd_gross_margin_pct`（q2_moat）｜AMD 毛利率＝53.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amd_operating_margin_pct`（q2_moat）｜AMD 營業利益率＝15.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amd_fcf_margin_pct`（q2_moat）｜AMD FCF 利潤率＝20.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvda_gross_margin_pct`（q2_moat）｜NVDA 毛利率＝74.67 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_nvda_operating_margin_pct`（q2_moat）｜NVDA 營業利益率＝65.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_nvda_fcf_margin_pct`（q2_moat）｜NVDA FCF 利潤率＝41.92 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_operating_margin_pct`（q2_moat）｜AVGO 營業利益率＝48.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_mrvl_operating_margin_pct`（q2_moat）｜MRVL 營業利益率＝16.81 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_3661_tw_fcf_margin_pct`（q2_moat）｜3661.TW FCF 利潤率＝-10.46 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3661.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝7.58 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-09-19）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝15.57 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-09-19）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝22.27 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-09-19）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝2.85 %｜期間與口徑：2026-06-23 → 2026-09-19／FY1 共識 EPS 7.37 → 7.58（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-09-19）
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝1558 USD million｜期間與口徑：Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-27，公告於 2026-08-04））
  - 註記：未查得 Street FCF 共識數字
- `f_kpi4_sbc`（q4_capital）｜SBC 占營收 %＝4.36 %｜期間與口徑：Q2 FY2026（季末 2026-06-27，公告於 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.amd.com — AMD Reports Second Quarter 2026 Financial Results（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-27，公告於 2026-08-04））
  - 註記：N/A（無此項共識追蹤）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝623.77 USD｜期間與口徑：2026-09-22（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-09-22（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝82.29 x｜期間與口徑：2026-09-19／分母＝FY1 EPS 7.58，分子＝快照價 623.77｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-09-19）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝156.33 x｜期間與口徑：2026-09-22（RTH 收盤，UTC）／4 個年度端點內的分位＝43.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-09-22（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝43.3 %｜期間與口徑：2026-09-22（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-09-22（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝24.65 x｜期間與口徑：2026-09-22（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-09-22（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-09-22（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-09-22（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝24.44 x｜期間與口徑：2026-09-22（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-09-22（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-09-22（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-09-22（RTH 收盤，UTC））
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-09-19／兩份 Koyfin 快照之間的 EPS 修正幅度（15.57 → 15.57）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-09-19）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝203.69 %｜期間與口徑：2026-09-22（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-09-22（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝✅｜期間與口徑：2026-09-23／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-23）
  - 原文：「price 623.77 / W52 339.87 / W104 235.31 / W250 165.31 / W250 13週斜率 3.99%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝339.87 USD｜期間與口徑：2026-09-23／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-23）
- `f_ma_w104`（q5_valuation）｜104 週均線＝235.31 USD｜期間與口徑：2026-09-23／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-23）
- `f_ma_w250`（q5_valuation）｜250 週均線＝165.31 USD｜期間與口徑：2026-09-23／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-23）

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：Custom ASIC silicon from hyperscalers (Broadcom AI ASIC revenue $20B+ in FY2025, Google TPU, AWS Trainium) is characterized as a larger and faster-growing competitive threat to Nvidia's AI accelerator dominance than AMD is, positioning custom silicon rather than AMD as the more significant new-entrant pressure in AI accelerators.
  - 來源：SemiAnalysis, "Can AMD break the CUDA Moat? AMD Advancing AI 2026" (cited via siliconanalysts.com search summary)（as_of 2026-01-01）｜affects：thesis.bear、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Meta（AMD 6GW Instinct GPU 合約的客戶）在簽下輝達與 AMD 大單數週後，宣布擴大自研 AI 晶片 MTIA（in-house）部署
  - 來源：CNBC, "Meta rolls out in-house AI chips weeks after massive Nvidia, AMD deals", https://www.cnbc.com/2026/03/11/meta-ai-mtia-chip-data-center.html（as_of 2026-03-11）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：Broadcom 被證實是 Google TPU、Meta MTIA、Microsoft Maia，以及 2026 年初起 OpenAI／Anthropic Titan 自研 AI 晶片專案的設計夥伴——顯示 AMD 多個大型 AI 客戶同時在推進自製晶片路線
  - 來源：Tom's Hardware, "The custom AI ASIC state of play (May 2026)", https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia（as_of 2026-05）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#2`（customer_second_source｜方向 -｜狀態 ok）：Microsoft 自研 AI 晶片 Maia 200 於 2026 年 1 月開始部署（台積電 3nm 製程），號稱比現有機隊每美元效能高 30%——微軟同時也是 AMD Instinct 的客戶之一
  - 來源：Windows News, "AI Compute Crunch: How Meta and Microsoft's Chip Deals Shape the 2026 Race", https://windowsnews.ai/article/ai-compute-crunch-how-meta-and-microsofts-chip-deals-shape-the-2026-race.411832（as_of 2026-01）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：AMD's forward customer base is concentrating around a small number of AI hyperscalers: AMD and Meta signed a 5-year, up-to-$60B, 6GW Instinct GPU supply agreement (with AMD issuing Meta a performance-based warrant for 160M shares), and combined with the OpenAI 6GW agreement AMD has ~12GW of committed deployments; these agreements are multi-year and milestone-based, meaning most of the associated revenue is not yet contracted, shipped, or paid.
  - 來源：CNBC / Tom's Hardware / AMD IR press release on AMD-Meta strategic partnership（as_of 2026-02-24）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：OpenAI, a counterparty to AMD's Instinct GPU supply agreement, reported a Q1 2026 net loss of $21.3B, carries roughly $665B in long-term compute purchase commitments not reflected as balance-sheet debt, and faces a projected financing gap of about $130B over the next two years.
  - 來源：TradingKey / IFR (International Financing Review) reporting on OpenAI Q1 2026 financials（as_of 2026-05）｜affects：decision_inputs.bear、thesis.R、triggers
- `customer_concentration_credit#4`（customer_concentration_credit｜方向 -｜狀態 ok）：S&P Global downgraded Oracle's credit rating from BBB to BBB- (one notch above junk), explicitly naming OpenAI as a 'key credit risk' for Oracle due to Oracle's large compute-supply exposure to OpenAI — illustrating rating-agency concern about OpenAI's counterparty credit quality that is also relevant to AMD's own OpenAI compute agreement.
  - 來源：the-decoder.com / TradingKey reporting on S&P Global Oracle downgrade（as_of 2026）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：記憶體晶片（DRAM/NAND，含 HBM 上游）短缺預期持續到 2027 年，SK海力士高層警告短缺可能延續到 2030 年之後，因 AI 資料中心需求排擠傳統記憶體供給
  - 來源：CNBC, "Memory chip shortage to last through 2027, semiconductor boss says", https://www.cnbc.com/2026/01/26/memory-chip-shortage-synopsys-lenovo-ai-data-centers.html（as_of 2026-01-26）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：美國總統於2026年1月14日簽署行政公告，對輸往中國、非用於美國供應鏈之先進AI晶片(含AMD MI325X等級產品)課徵25%從價關稅，作為前述放行規則的配套限制。
  - 來源：Mayer Brown, 'Administration Policies on Advanced AI Chips Codified' https://www.mayerbrown.com/en/insights/publications/2026/01/administration-policies-on-advanced-ai-chips-codified（as_of 2026-01-14）｜affects：valuation、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：President Trump's Proclamation 11002 imposed a 25% Section 232 tariff on advanced semiconductors and derivative products effective January 15, 2026; AMD's Instinct MI325X is specifically named in the annex. Exemptions apply to products supporting US data centers, R&D, startups, repairs, and non-data-center consumer/industrial uses.
  - 來源：President Trump Announces Section 232 Tariffs on Semiconductors and their Derivative Products, International Trade & Supply Chain Insights (internationaltradeinsights.com/2026/01/president-trump-announces-section-232-tariffs-on-semiconductors-and-their-derivative-products/)（as_of 2026-01-15）｜affects：thesis.R、decision_inputs.bear、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：TSMC controls roughly 90% of the world's most advanced-node chip production (3nm/5nm) and is AMD's main foundry for leading-edge chiplet processors; this production is concentrated in Taiwan, ~100 miles from mainland China.
  - 來源：Mapshock, "TSMC Taiwan Geopolitical Risk: Concentration and Resilience Planning" (mapshock.com); FourWeekMBA, "AMD and TSMC: What a Reported Foundry Cost Rise Reveals About the Fabless Supply Layer"（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear、triggers
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：On 2026-01-14, the US administration signed a proclamation imposing a 25% duty/revenue-share on advanced computing chips (e.g. H200, MI325X) shipped to China, with mandatory third-party testing and a volume cap; AMD CEO Lisa Su stated China still accounts for about 20% of AMD's revenue despite export controls.
  - 來源：Introl Blog, "BIS Export Policy Shift" (introl.com/blog/bis-export-policy-h200-mi325x-china-case-by-case-2026); Cryptobriefing, "AMD CEO Lisa Su says China still accounts for about 20% of revenue despite GPU export controls"（as_of 2026-01-14）｜affects：thesis.R、decision_inputs.bear、valuation
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：AMD had previously forecast about $1.5 billion in 2025 revenue loss and taken an $800 million charge tied to halted AI-chip shipments to China (inventory write-downs, cancelled purchases) due to tightened US export restrictions.
  - 來源：Astute Group, "AMD Flags $1.5 Billion Revenue Blow from Tightened Export Curbs"; Motley Fool, "AMD Stock Declines as Earnings Drop 30% on Government Restricting Advanced AI Chip Sales to China"（as_of 2025-08-06）｜affects：thesis.R、decision_inputs.bear
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：NVIDIA holds an estimated 70-75% of data-center AI accelerator market revenue vs. AMD's estimated 6-8%; hyperscaler custom silicon collectively ~15-20%
  - 來源：Silicon Analysts https://siliconanalysts.com/analysis/nvidia-ai-accelerator-market-share-2024-2026（as_of 2026-08-01）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `end_markets#11`（end_markets｜方向 -｜狀態 ok）：Gaming segment revenue was $779M in Q2 2026, down 31% YoY, primarily due to lower semi-custom (console) revenue and higher component costs weighing on GPU demand at this late stage of the console cycle; AMD guided H2 2026 gaming revenue to be >20% lower than H1 2026
  - 來源：Tom's Hardware https://www.tomshardware.com/tech-industry/amd-doubles-data-center-revenue-year-over-year-but-gaming-revenue-plunged-by-31-percent-ceo-lisa-su-says-prices-have-weighed-on-consumer-demand-but-is-optimistic-about-client-market（as_of 2026-08-04）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：AMD 2026 SWOT 分析指出，AMD 部分大客戶正自行開發內部處理器與加速器（客製化晶片/ASIC），可能壓縮 AMD 的可觸及市場（addressable market）。
  - 來源：AMD SWOT Analysis 2026 - The Strategy Story (https://thestrategystory.com/blog/amd-swot-analysis-2026/)（as_of 2026-09-21）｜affects：moat_trend、thesis.R、decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20260923/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1500.0,"bear_5y_price":280.0,"p_bull_pct":22,"p_bear_pct":32,"upside_5y_pct":38.3,"ev5y_pct":30.9,"irr_base_pct":6.7,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":7.58,"pe":82.29,"basis":"FY2026E 共識 EPS（前瞻一年口徑），與終端 FY2031E 前瞻倍數同口徑"},"eps":{"bull":[17.5,27.0,35.0,43.0,50.0],"base":[15.0,21.0,26.0,30.5,34.5],"bear":[12.0,13.0,11.0,12.5,14.0]},"pe":{"bull":30,"base":25,"bear":20},"p":{"bull":22,"base":46,"bear":32},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AMD_Q1_2026_Earnings_Call_20260505.md
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 表示 server CPU TAM 現預期年增率大於 35%，2030 年前規模超過 1,200 億美元。（原話："TAM to grow at greater than 35% annually"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 回顧去年 11 月分析師日的 server CPU 市場預期：未來 3 至 5 年年增約 18%。（原話："18% annually over the next 3 to 5 years"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 表示 server CPU 營收第二季預期年增超過 70%，並持續到下半年與 2027 年。（原話："more than 70% year-over-year in the second quarter"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 說明正與供應鏈夥伴合作，大幅擴充晶圓與後段產能以支應 CPU 需求。（原話："we are working closely with our supply chain partners"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 給第二季營收指引約 112 億美元，正負 3 億美元。（原話："We expect revenue to be approximately $11.2 billion"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 表示第二季營收預期季增約 9%，由 Data Center 與 Embedded 雙位數成長帶動，Client and Gaming 小幅成長。（原話："9% driven by double-digit growth in both our Data Center"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 給第二季 non-GAAP 毛利率指引約 56%。（原話："gross margin to be approximately 56%"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 給第二季 non-GAAP 營業費用指引約 33 億美元，其他損益為約 6,000 萬美元收益。（原話："non-GAAP operating expenses to be approximately $3.3"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 給第二季 non-GAAP 有效稅率 13%，稀釋股數約 16.6 億股。（原話："effective tax rate to be 13%"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 表示第一季營收 103 億美元，高於指引上緣。（原話："First quarter revenue was $10.3 billion, exceeding"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 說明與 Meta 擴大策略合作，將部署最多 6 GW 的 AMD Instinct GPU，橫跨數個產品世代。（原話："Meta to deploy up to 6 gigawatts of AMD Instinct GPUs"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 將 Meta 與先前公布的 OpenAI 合作並列，稱 AMD 是大型 AI 基礎設施建置商的核心夥伴。（原話："Together with our previously announced OpenAI partnership"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示 MI450 系列已開始送樣，Helios 量產出貨仍維持下半年的時程。（原話："remain on track to ramp Helios production shipments"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 表示主要客戶對 MI450 系列的預測已超過 AMD 原先規劃，且有更多新客戶洽談大規模部署。（原話："lead customer forecasts now exceeding our initial plans"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示對 2027 年 Data Center AI 年營收達數百億美元的信心增強。（原話："annual Data Center AI revenue in 2027 and to exceed our"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 在問答中表示看到路徑可超越原先大於 80% 的 CAGR 目標，時間框為 2027 年。（原話："exceed our original targets of greater than 80% CAGR"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示在策略時間框內每股盈餘目標為超過 20 美元，並稱有路徑超越長期財務目標。（原話："than $20 in EPS over the strategic time frame."）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示第 6 代 EPYC Venice 仍預定今年稍晚推出。（原話："remain on track to launch Venice later this year."）
- 2026-05-05｜Lisa Su｜competition：Lisa Su 表示 Venice 每插槽吞吐量相較領先的 ARM 架構 AI 方案超過 2 倍。（原話："and more than 2x throughput"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 表示第二季 Ryzen 需求預期穩健，但規劃下半年 PC 出貨較低。（原話："we are planning for second half PC shipments to be"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 將下半年 PC 出貨走低歸因於記憶體與零組件成本上升，同時仍預期 Client 營收年增並優於市場。（原話："lower due to higher memory and component costs"）
- 2026-05-05｜Jean Hu｜guidance：Jean Hu 表示下半年 Gaming 營收預期較上半年下滑超過 20%（上一句稱因記憶體與零組件成本）。（原話："second half gaming revenue to decline more than"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示第一季毛利率 55%，較去年同期增加 170 個基點，原因為產品組合有利（含 Data Center 營收占比提高）。（原話："Gross margin was 55%, up 170 basis"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示第一季營業費用 31 億美元，年增 42%。（原話："Operating expenses were $3.1 billion, an increase of 42%"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示第一季營業利益 25 億美元，營業利益率 25%。（原話："representing a 25% operating margin"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示第一季稀釋後每股盈餘 1.37 美元，年增 43%。（原話："diluted earnings per share was $1.37, up 43%"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示 Data Center 部門第一季營業利益 16 億美元、占營收 28%，去年同期為 9.32 億美元、25%。（原話："Data Center segment operating income was $1.6 billion"）
- 2026-05-05｜Jean Hu｜capital_allocation：Jean Hu 表示第一季自由現金流創紀錄的 26 億美元，占營收 25%。（原話："a record $2.6 billion in free cash flow or 25% of revenue"）
- 2026-05-05｜Jean Hu｜capital_allocation：Jean Hu 表示第一季買回 110 萬股，回饋股東 2.21 億美元。（原話："repurchased 1.1 million shares and returned $221 million"）
- 2026-05-05｜Jean Hu｜capital_allocation：Jean Hu 表示季底股票買回授權額度剩 92 億美元。（原話："$9.2 billion authorization remaining"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 Data Center AI 營收年增為「顯著的雙位數百分比」，逐字稿中未給美元金額或確切百分比。（原話："Revenue grew by a significant double-digit percentage"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 表示 Data Center AI 第一季環比小幅下滑，她歸因於 China 的轉換（第四季 China 收入較多）。（原話："Data Center AI was actually down modestly"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 說明 Helios 放量節奏：下半年起步，第三季有初期量，第四季顯著放量。（原話："starting with initial volume in Q3, with a significant ramp"）
- 2026-05-05｜Lisa Su｜guidance：Lisa Su 表示第二季 Data Center 指引為環比雙位數成長，server 與 Data Center AI 兩者都是雙位數。（原話："double digits in both server as well as Data Center AI"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 承認供應鏈吃緊，Data Center 建置也吃緊。（原話："We feel that there is tightness in the supply chain."）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 表示有信心供應所述成長水準，甚至超過該水準。（原話："we are confident in our ability to supply to the levels of"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 表示對 2027 年部署已有精細能見度，細到 GPU 會裝進哪些資料中心。（原話："it's visibility down to which Data Centers are the GPUs"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 被問到 server CPU 市占大於 50% 的目標時，回答對達成該市占的機會有信心。（原話："than 50% share of that market."）
- 2026-05-05｜Lisa Su｜competition：Lisa Su 談 ARM 競爭：稱 ARM 是好架構，但 AMD 視其為點狀產品，相對於 AMD 的完整產品組合。（原話："We view it as more point products relative to a portfolio"）
- 2026-05-05｜Lisa Su｜competition：Lisa Su 回應 ARM 與 x86 競爭時表示，大型超大規模業者會同時使用 x86 與 ARM。（原話："I think you're going to see people actually use x86"）
- 2026-05-05｜Lisa Su｜competition：Lisa Su 談低延遲等專用推論架構：預期會出現不同變體，AMD 稱已準備好因應。（原話："we should expect that there will be different variants"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 Data Center GPU 仍將是絕大部分 TAM 的主要加速器。（原話："Data Center GPUs as the primary accelerator"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 CPU 對 GPU 的配比正從過去的 1:4 或 1:8 主機節點，朝接近 1:1 移動。（原話："getting closer to a 1:1 configuration"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 回答 Vivek Arya 時表示 agentic CPU 需求對整體 AI TAM 大致是加項。（原話："it's largely additive to the TAM"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 把 CPU TAM 拆三類：傳統通用型（低雙位數成長）、AI 主機節點、agentic AI；並稱成長最大的一塊是 agentic AI。（原話："the largest piece of the growth is this agentic AI piece"）
- 2026-05-05｜Lisa Su｜margin：Lisa Su 說明第一季 server 成長中，ASP 與出貨量都年增，但主要由出貨量帶動。（原話："it was actually much more unit-driven."）
- 2026-05-05｜Lisa Su｜margin：Lisa Su 表示第二季與下半年 server 成長多數來自出貨量，ASP 漲幅用來覆蓋通膨壓力。（原話："growth is unit-driven and the ASPs are just really to help"）
- 2026-05-05｜Lisa Su｜margin：Lisa Su 表示供應鏈吃緊帶來成本上升，AMD 與客戶分攤部分成本。（原話："we are sharing some of that with our customers"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示 MI450 第三季開始放量、第四季大幅放量，其毛利率低於公司平均。（原話："That is below corporate average."）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 表示對 2026 年毛利率的整體架構有信心，順風因素可抵銷部分 MI450 的稀釋。（原話："feel really good about the setup of the gross margin"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 重申分析師日訂的長期毛利率區間為 55% 至 58%，並說第一年進展良好。（原話："long-term gross margin in the range of 55% to 58%"）
- 2026-05-05｜Jean Hu｜margin：Jean Hu 被問 Instinct 毛利率時，表示目前聚焦營收成長，營收放量後在 ASP 與成本面有改善空間。（原話："we'll have a lot of opportunities to improve gross margin"）
- 2026-05-05｜Jean Hu｜commitment：Jean Hu 表示今年 R&D 的成長會明顯快於 SG&A。（原話："you should expect us to grow R&D much faster than SG&A."）
- 2026-05-05｜Lisa Su｜capital_allocation：Lisa Su 說明銷售與行銷投資投向企業級 server、商用 PC 與中小企業市場。（原話："the investments are going into enterprise servers"）
- 2026-05-05｜Jean Hu｜capital_allocation：Jean Hu 回應費用一再超出指引的提問時，表示公司正積極投資。（原話："we actually are investing aggressively"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 表示已確保足夠記憶體供應可達成並超越目標，但也說明記憶體環境吃緊。（原話："we have secured enough supply to certainly meet"）
- 2026-05-05｜Lisa Su｜risk：Lisa Su 表示 Client 第一季桌機較軟，因桌機偏消費市場，較受記憶體與零組件漲價影響。（原話："We did see desktops a little bit softer"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 Turin 本季占營收已超過 50%，Milan 出貨已隨時間下降。（原話："crossed over 50% of our revenue being Turin this quarter"）
- 2026-05-05｜Lisa Su｜customer：Lisa Su 表示 Embedded 的設計案動能年增雙位數百分比，新增設計案價值達數十億美元。（原話："with billions of dollars in new wins across markets"）
- 2026-05-05｜Lisa Su｜product：Lisa Su 表示 AMD 大幅加快 ROCm 開發節奏，做法包括增加軟體投資與 agent 式程式開發流程。（原話："we have significantly accelerated our ROCm"）
- 2026-05-05｜Lisa Su｜commitment：Lisa Su 預告將在七月的 Advancing AI 活動分享下一代 Instinct、EPYC、Helios 與客戶合作進展。（原話："our Advancing AI event in July"）
- 2026-05-05｜Jean Hu｜risk：Jean Hu 被追問時表示 China 在第一季收入不重大。（原話："the China revenue in Q1 is not material."）

### AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md
- 2025-11-11｜Matthew Ramsay｜margin：開場聲明：當天幾乎所有數字都是 non-GAAP，GAAP 對帳表在簡報附錄與 SEC 文件。（原話："pretty much every number that we're going to talk about"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱資料中心 AI 營收未來 3 到 5 年的年複合成長率超過 80%。（原話："over 80% AI revenue CAGR over the next 3 to 5 years"）
- 2025-11-11｜Jean Hu｜guidance：Jean 稱 2027 年資料中心 AI 營收軌跡為數百億美元（tens of billion）。（原話："tens of billion dollars of data center AI revenue in 2027"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 提到先前講過 2027 年營收目標為 tens of billions of dollars，並稱進度符合。（原話："So I can say that we're on track to that."）
- 2025-11-11｜Lisa Su｜guidance：全公司營收成長目標以 2025 年約 340 億美元為基期。（原話："a baseline in 2025 of $34 billion"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱全公司營收年複合成長率超過 35%（3 到 5 年框架）。（原話："over 35% CAGR at the total company level"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱核心業務（Client 與 Embedded）年複合成長率超過 10%；資料中心超過 60%。（原話："growing also well ahead of the market at over 10% CAGR"）
- 2025-11-11｜Forrest Norrod｜guidance：Forrest 稱 AMD 資料中心事業未來 3 到 5 年有明確路徑達 60% 年複合成長率。（原話："clear line of sight to 60% CAGR over the next 3 to 5 years"）
- 2025-11-11｜Forrest Norrod｜guidance：Forrest 把 60% 年複合成長率換算為資料中心年營收超過 1000 億美元。（原話："over $100 billion in annual AMD data center revenue"）
- 2025-11-11｜Jean Hu｜guidance：Jean 給長期財務模型：3 到 5 年毛利率區間 55% 到 58%。（原話："expect our gross margin to be in the range of 55% to 58%"）
- 2025-11-11｜Jean Hu｜guidance：Jean 給長期模型：營業利益率超過 35%、稅率 13% 到 15%（同句接續給自由現金流利潤率超過 25%）。（原話："operating margin to be more than 35%, the tax rate of 13%"）
- 2025-11-11｜Jean Hu｜guidance：Jean 稱預測期間每股盈餘超過 20 美元。（原話："per share to be more than $20 in the forecast period"）
- 2025-11-11｜Jean Hu｜guidance：Jean 答毛利問題時提到 Q4 毛利率指引為 54.5%。（原話："We guided Q4 at 54.5%."）
- 2025-11-11｜Jean Hu｜guidance：Jean 稱 MI450 預期 2026 下半年開始放量。（原話："we expect MI450 to start to ramp in second half of 2026"）
- 2025-11-11｜Jean Hu｜guidance：Jean 對 2026 年給的唯一方向：營收成長會高於 OpEx 成長。（原話："one thing I can tell you is revenue growth next"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 回應 Stacy：近年成長率預期高於 80%，且稱對 tens of billions 落在市場想法附近感到 comfortable。（原話："faster than 80%, so greater than greater than 80%."）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱伺服器營收市占目標為 3 到 5 年內超過 50%（目前約 40%）。（原話："path to over 50% revenue share of the server market"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 Client 營收市占目標為 3 到 5 年內超過 40%（目前高 20% 區間）。（原話："a clear path to over 40% client revenue market share"）
- 2025-11-11｜Jack Huynh｜guidance：Jack 稱 Client 營收成長將達市場的 3 倍以上，並把市占推到 40% 以上。（原話："revenue growth at more than 3x the market rate while"）
- 2025-11-11｜Jack Huynh｜guidance：Jack 被問 TAM 時：Client TAM 3 到 5 年預估低到中個位數成長。（原話："we're projecting low to mid-single digit"）
- 2025-11-11｜Salil Raje｜guidance：Salil 稱 Embedded 近期營收成長為市場的 2 倍。（原話："we'll grow our revenue at 2x the market rate"）
- 2025-11-11｜Salil Raje｜guidance：Salil 稱長期隨 semi-custom 與 physical AI 放量，Embedded 成長升到市場的 3 倍。（原話："up to 3x the market rate over the long-term horizon"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 Embedded adaptive 營收市占目標為 3 到 5 年內超過 70%。（原話："over 70% of the embedded adaptive revenue market share"）
- 2025-11-11｜Salil Raje｜guidance：Salil 稱核心 FPGA 業務市占正朝 70% 走（Lisa 講的是 3 到 5 年 embedded adaptive 超過 70%，用詞不同）。（原話："We're also tracking to 70% market share in our core FPGA"）
- 2025-11-11｜Jean Hu｜guidance：Jean 稱資料中心 TAM 從今年 2000 億美元成長到 2030 年超過 1 兆美元。（原話："go from $200 billion this year to over $1 trillion in 2030"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 2030 年 TAM 超過 1 兆美元；此為新口徑（延伸到 2030 年）。（原話："greater than $1 trillion by 2030."）
- 2025-11-11｜Lisa Su｜guidance：Lisa 說明 TAM 口徑擴大：除加速器外，也納入 CPU 與部分網路內容。（原話："but also include CPUs and some of the"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱先前 2028 年 TAM 預測（超過 5000 億美元）現在被大幅上修。（原話："we're seeing that number come up significantly"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 回顧 AI TAM 歷次上修：3000 億、4000 億、再到 5000 億美元。（原話："we updated it to $400 billion and then $500 billion."）
- 2025-11-11｜Daniel McNamara｜guidance：Dan 稱到 2030 年 CPU TAM 增加 300 億美元，約為目前的兩倍。（原話："we're going to add $30 billion in CPU TAM"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 2025 年資料中心營收預估超過 160 億美元、成長率超過 50%。（原話："estimated over $16 billion, over 50% growth rate"）
- 2025-11-11｜Lisa Su｜guidance：Lisa 稱 2025 年全公司營收預估約 340 億美元。（原話："We're now projecting to be about $34 billion this year"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱混合（mix）仍是毛利率的主要驅動因素。（原話："Third is mix, which remain to be the primary driver"）
- 2025-11-11｜Jean Hu｜margin：Jean 談資料中心整體（近半營收）時稱其毛利率較高；後段講 Data Center AI 時口徑不同（見下條）。（原話："what's really most exciting, it has a higher gross margin"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 Data Center AI 業務目前毛利率略低於公司平均。（原話："our gross margin is slightly below corporate average"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱在快速成長的市場，毛利金額最大化是第一優先。（原話："maximizing gross margin dollars is our #1 priority"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 Data Center AI 賣的是 GPU、CPU、有時 DPU，不賣整櫃系統，毛利結構與現在相同。（原話："Our business model is not going to change."）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 Client 毛利率仍遠低於公司平均，有續升空間。（原話："it's still very much lower than corporate average"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱企業市場每多一個百分點的市占，對整體毛利率都明顯加分。（原話："is significantly accretive to our overall gross margin"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 2025 年預期毛利率達 54%。（原話："expect to deliver gross margin of 54% this year"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 2025 下半年 MI350 大量放量，毛利率仍持續擴張。（原話："we are able to continue to expand the gross margin"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 2025 年營運獲利水準超過 33%（稿中原文措辭為 of operating income，未寫 margin）。（原話："deliver over 33% of operating income"）
- 2025-11-11｜Jean Hu｜margin：Jean 稱 2027 年 Data Center AI 放量，若量很大，毛利率可能落在 55% 區間下緣。（原話："it could be closer to the 55% range"）
- 2025-11-11｜Lisa Su｜margin：Lisa 談 HBM：自家主導設計的部分預期有健康毛利，但代為搭載的 HBM 不預期同等毛利。（原話："same margin on HBM. And I think that's fair"）
- 2025-11-11｜Lisa Su｜margin：Lisa 澄清 1 兆美元 TAM 為矽（silicon）TAM，含隨 GPU 搭載的 HBM。（原話："includes the HBMs that go with the GPUs."）
- 2025-11-11｜Forrest Norrod｜margin：Forrest 強調 1 兆美元是矽 TAM，不宜與他人整體方案 TAM 比較。（原話："That's not to be compared to some others"）
- 2025-11-11｜Jean Hu｜margin：Jean 回答 MI450 初期是否稀釋毛利率時稱目前還不知道。（原話："Right now, actually, I don't know yet."）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱 2021 年起已透過買回股票回饋股東 86 億美元。（原話："Since 2021, we have returned $8.6 billion cash to"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱買回股票先抵銷員工股權稀釋，有機會再做額外買回。（原話："offset the employee stock dilution first"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱 2025 年自由現金流預期較去年成長逾一倍。（原話："we expect to more than double our free cash flow"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 以 ZT Systems 為例：收購設計團隊、同時剝離製造業務。（原話："We acquired the ZT design team."）
- 2025-11-11｜Lisa Su｜capital_allocation：Lisa 稱 AMD 現在有更積極的創投投資部門（幾年前沒這麼做）。（原話："a much more active venture investments arm"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱過去累計透過有機投資與併購投入超過 1000 億美元。（原話："we have invested over $100 billion through organic"）
- 2025-11-11｜Jean Hu｜capital_allocation：Jean 稱 2025 年是加碼投資的一年（硬體路線圖、系統軟體、ZT 與軟體併購）。（原話："2025 is an important year for us to invest."）
- 2025-11-11｜Jean Hu｜commitment：Jean 承諾營收成長速度要快於營運費用成長。（原話："But we are very committed to drive revenue"）
- 2025-11-11｜Forrest Norrod｜commitment：Forrest 稱機櫃層級系統也將維持每年一代的節奏（元件同樣維持年度節奏）。（原話："we will continue on annual cadence for the components"）
- 2025-11-11｜Forrest Norrod｜commitment：Forrest 稱 AMD 自己不賣機櫃系統，透過 OEM、ODM 與 ZT 夥伴（Sanmina）推向市場。（原話："AMD is not selling the rack systems."）
- 2025-11-11｜Lisa Su｜commitment：Lisa 談執行力：稱說了要做的事就會做到。（原話："that we're going to do something, we're going to do it."）
- 2025-11-11｜Mark Papermaster｜commitment：Mark 稱 AMD 持續投入開放軟體與開放硬體的 AI 生態系。（原話："commitment to open software and open hardware"）
- 2025-11-11｜Lisa Su｜commitment：Lisa 稱與 OpenAI 的第一個 gigawatt 已說過會在 2026 下半年開始、延續到 2027。（原話："the first gigawatt will start in the second half of '26"）
- 2025-11-11｜Lisa Su｜commitment：Lisa 稱與 Oracle 的合作以 2026 第三季為 MI450 公有雲執行個體的放量目標。（原話："targeting third quarter and '26 as the ramp"）
- 2025-11-11｜Forrest Norrod｜commitment：Forrest 稱 Helios 預計 2026 年 Q3 上市。（原話："when it comes to the market in Q3 of next"）
- 2025-11-11｜Daniel McNamara｜commitment：Dan 稱 Venice 明年上市，採台積電 2 奈米製程。（原話："It's on 2-nanometer TSMC process."）
- 2025-11-11｜Mark Papermaster｜competition：Mark 稱競爭對手在 AI 上走較封閉的專有（walled garden）方案，AMD 走開放。（原話："more proprietary walled garden solutions."）
- 2025-11-11｜Forrest Norrod｜competition：Forrest 稱資料中心現在面對的是另一個不同的主導對手（相對於早年 CPU 市場的對手）。（原話："a new dominant competitor, a different dominant competitor"）
- 2025-11-11｜Lisa Su｜competition：Lisa 估計 ASIC 佔加速器 TAM 約 20% 到 25%，其餘為 GPU。（原話："So ASICs, maybe 20% to 25% of"）
- 2025-11-11｜Lisa Su｜competition：Lisa 說明 ASIC 適用情境：模型與演算法較穩定、下一步可預期時。（原話："ASICs tend to be good if your models -- if your algorithms"）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱標準款 GPU 仍會是最大成長動能，但也可能做客製化 GPU。（原話："I still believe that standard product GPU will be"）
- 2025-11-11｜Forrest Norrod｜competition：Forrest 稱伺服器 CPU 除了對 Intel，也在與 ARM 比 TCO 與效能。（原話："not just with Intel, but also with ARM"）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱 AMD 在伺服器 CPU 已是現任者（incumbent），不把任何市占視為理所當然。（原話："we don't take any share for granted"）
- 2025-11-11｜Daniel McNamara｜competition：Dan 稱市場上有 CPU 被 GPU 蠶食的論點，他說實際看到的是相反。（原話："that CPUs have been cannibalized."）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱今年前曾有 GPU 會吃掉 CPU 工作負載的說法，實際看到相反的情況。（原話："We've actually seen the opposite be true."）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱雲端對通用伺服器的需求增幅出乎 AMD 意料。（原話："demand has actually surprised us."）
- 2025-11-11｜Lisa Su｜competition：Lisa 稱通用運算需求上升是可持續的趨勢（過去兩年 TAM 大致持平）。（原話："This feels like a real durable trend."）
- 2025-11-11｜Daniel McNamara｜competition：Dan 稱伺服器 CPU 營收市占約 40%。（原話："we're hovering around 40% share"）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 給 MI455X 規格：432 GB HBM、19.6 TB/s（同段稱最高 40 petaflops FP4）。（原話："It has 432 gigabytes of HBM memory running at 19.6"）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 引用 InferenceMAX 基準：MI355 在 GPT OSS 上單位 token 服務成本最多較前代降至 1/10 水準（稿中原文 up to 10x benefits）。（原話："MI355 on the GPT OSS model deliver up to 10x benefits"）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 稱 MI500 系列不是漸進式改版，是下一次重大突破。（原話："this is not an incremental step on our road map."）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 介紹新增的 MI430，針對科學運算與主權需求，強調雙精度浮點。（原話："we have built the MI430 product."）
- 2025-11-11｜Vamsi Boppana｜product：Vamsi 談 AI 寫 GPU kernel：稱未來會移除採用 AMD 平台的最後障礙（同段稱目前尚未完全到位）。（原話："and it will take down with it any last remaining barriers"）
- 2025-11-11｜Forrest Norrod｜product：Forrest 稱光學互連預計 2027 到 2029 年間開始轉換，先從機櫃級 scale-up 開始。（原話："we believe in the '27, '28, '29 time frame"）
- 2025-11-11｜Forrest Norrod｜product：Forrest 稱長期走向光學，銅與 SerDes 只會短期並存。（原話："but it's all going optics long term."）
- 2025-11-11｜Lisa Su｜product：Lisa 稱 AMD 已贏得數個資料中心 semi-custom 案。（原話："we have won several data center semi-custom"）
- 2025-11-11｜Lisa Su｜product：Lisa 稱這些資料中心 semi-custom 案偏向系統周邊（含部分網路元件），不是運算單元本身。（原話："not the compute unit itself, but some of the attach"）
- 2025-11-11｜Lisa Su｜product：Lisa 稱 2025 年 AMD 選擇不推機櫃級方案，把資源放在新資料格式與時程，MI450 才備齊各項元件。（原話："We chose not to do Rack Scale solutions"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱與 OpenAI 簽下 5 年 6 gigawatt 合作（準備稿口徑：over 5 years）。（原話："announce a 6-gigawatt deal over 5 years"）
- 2025-11-11｜Lisa Su｜customer：Lisa 在 Q&A 把同一合約期間說成 4 或 5 年（準備稿說 5 年）。（原話："6 gigawatts over 4 or 5 years"）
- 2025-11-11｜Lisa Su｜customer：Lisa 回答客戶集中度：OpenAI 是重要基礎，但稱同期會有多家超大規模客戶。（原話："OpenAI is an important foundation, but we will have"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱 OpenAI 合約結構是逐年檢視需求與供應的紀律式安排。（原話："it's a very disciplined engagement."）
- 2025-11-11｜Lisa Su｜customer：Lisa 承認 OpenAI 是算力預測最積極的客戶之一。（原話："one of the most aggressive when it comes to their compute"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱 MI450 世代預期有多家規模相近（gigawatt 等級）的客戶，供應鏈依此規劃。（原話："We expect to have multiple similar-sized customers"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱首度公開展示與 Meta 合作的 Helios 機櫃方案。（原話："showed for the first time our Helios Rack scale solution"）
- 2025-11-11｜Vamsi Boppana｜customer：Vamsi 舉例：某超大規模客戶一年內在 Instinct 上跑的工作負載超過 70 個。（原話："within 12 months, within 1 year, they now have over 70"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱 MI450 完全放量並通過驗證後，預期轉換多個 gigawatt 等級機會。（原話："we would expect to convert a number of those opportunities"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱客戶說法改變：去年說投資會趨緩，現在說不會趨緩、需要加速。（原話："no, it's actually not going to level off."）
- 2025-11-11｜Lisa Su｜customer：Lisa 回應 OpenAI 資金能力疑慮：稱不會押注反方。（原話："I wouldn't bet against that. I really wouldn't."）
- 2025-11-11｜Jack Huynh｜customer：Jack 稱 Client 營收占比達 28% 的紀錄高點，ASP 兩年成長 50%。（原話："our ASPs to a record 28% revenue share"）
- 2025-11-11｜Jack Huynh｜customer：Jack 稱 Client and Gaming 營收由 96 億美元成長到超過 140 億美元。（原話："50% year-on-year increase in revenue from $9.6 billion to"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱 Embedded 設計訂單 2025 年將超過 160 億美元（2024 年為 140 億美元）。（原話："We're on a path to exceed $16 billion this year."）
- 2025-11-11｜Salil Raje｜customer：Salil 稱 Embedded 累計設計訂單超過 360 億美元（與 Lisa 講的另一組設計訂單數字並列，稿中未說明兩者關係）。（原話："We won thousands of designs totaling $36 billion plus."）
- 2025-11-11｜Salil Raje｜customer：Salil 稱 semi-custom 設計訂單 150 億美元，涵蓋車用、資料中心、航太國防、無線。（原話："$15 billion across automotive, data center"）
- 2025-11-11｜Lisa Su｜customer：Lisa 稱近 12 到 18 個月新簽 semi-custom 設計訂單合計超過 450 億美元（與 Salil 的 150 億美元數字並列，稿中未說明差異）。（原話："now totaling over $45"）
- 2025-11-11｜Salil Raje｜customer：Salil 稱 semi-custom 長期可占 Embedded 事業近三分之一。（原話："scaling up to almost 1/3 of our business"）
- 2025-11-11｜Salil Raje｜customer：Salil 稱 physical AI 市場 2035 年預期超過 2000 億美元。（原話："expected to be $200 billion plus by 2035"）
- 2025-11-11｜Salil Raje｜customer：Salil 稱擴大後的 Embedded 產品線可觸及 300 億美元 TAM。（原話："tap into $30 billion of TAM"）
- 2025-11-11｜Salil Raje｜risk：Salil 稱 Embedded 過去兩年的疲軟來自庫存調整，現已過去、成長回來。（原話："Now that phase is behind us, and growth is returning"）
- 2025-11-11｜Lisa Su｜risk：Lisa 稱最近財報電話會議已把中國從營收預測中拿掉。（原話："China out of our revenue forecast because it's too hard"）
- 2025-11-11｜Lisa Su｜risk：Lisa 稱中國在她所說的 TAM 中占比很小。（原話："it's also a small piece of our TAM"）
- 2025-11-11｜Lisa Su｜risk：Lisa 承認供應環境正在趨緊。（原話："the supply environment is getting tighter"）
- 2025-11-11｜Lisa Su｜risk：Lisa 稱有信心整體供應鏈能支撐所提的成長模型。（原話："feel very confident that we have the overall supply chain"）
- 2025-11-11｜Lisa Su｜risk：Lisa 稱花不少時間研究客戶與全球的電力路線圖，以對照預測。（原話："spending quite a bit of time looking at the power road map"）
- 2025-11-11｜Lisa Su｜risk：Lisa 回應融資疑慮：稱若 AI 使用量如預期成長，會有足夠的融資。（原話："I think there's going to be plenty of financing"）

### 問答異常語氣（迴避／改口／保留）
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：Stacy Rasgon：Q1 Data Center AI 排除 China 後，環比是否仍成長？｜答法：Jean Hu 先重複「DC AI 環比小幅下滑、主因 China 收入較低」，Rasgon 指出未回答後，她只說 China 在 Q1 不重大，仍未回答排除 China 後是否成長。Lisa Su 稍早對 Tom O'Malley 則說 DC AI 下滑是因為 China 轉換、Q4 China 收入較多。
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：Stacy Rasgon：營業費用一再超出 AMD 自己給的指引，為何難預測、今年剩餘時間如何看？｜答法：Jean Hu 改談「積極投資、投資帶動營收動能、營收超標拉高部分費用、支援 DC AI 客戶」，未解釋預測為何偏低，也未給全年費用數字。
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：C.J. Muse：Instinct 產能吃緊，毛利率是否可在 1-3 年內拉近公司平均？｜答法：Jean Hu 回答目前聚焦營收成長，只說「over time」營收放量後在 ASP 與成本面有改善機會，未給目標、時程或數字。
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：Aaron Rakers：為 AI 工作負載優化的 CPU，ASP 是否結構性高於通用 server CPU？｜答法：Lisa Su 明說沒有可提供的相對 ASP 數字，稱取決於工作負載，只說核心數增加時 ASP 會上升。
- AMD_Q1_2026_Earnings_Call_20260505.md｜問：Vivek Arya：AMD 是否已確保足夠記憶體供應，相較對手已揭露大量預付款？｜答法：Lisa Su 答稱與記憶體廠商關係深、已確保足夠供應以達成並超越目標，同時說明記憶體環境吃緊；未回應預付款，也未給數字。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Timothy Arcuri 問零組件成本上漲（記憶體等）如何計入模型，可能傷及 PC 與伺服器 TAM。｜答法：Jean 回答營運團隊與 Forrest 在管控零組件供應與成本可見度，未說明是否或如何計入財務模型，未給數字。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Vivek Arya 與 Joseph Moore 追問 80% 成長對應的資料中心 AI 市占願景（Vivek 自算約中段十幾％）。｜答法：Lisa 說明近期為 bottoms-up、遠期為策略對話，並稱目標為 meaningful double-digit percentage，兩題都未給具體市占數字。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Stacy Rasgon 指出以 80% 成長從約 65 億美元推算 2027 年只有約 200 到 210 億美元，低於市場約 290 到 300 億美元。｜答法：Lisa 稱近年成長會高於 80%，只說對 tens of billions 落在市場想法附近感到 comfortable，未確認或否認市場共識數字。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Joshua Buchalter 問多個 gigawatt 級專案要轉換需要跨過哪些門檻，以及規模與 OpenAI 相比如何。｜答法：Lisa 談與超大規模客戶的關係、供應鏈準備與軟體工作，未列出具體門檻，也未比較與 OpenAI 的規模。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Christopher Rolland 問營運費用成長是否前置、是否高於約 25%，以及市場預期的 2026 年營收成長（中高十幾％）方向是否應上調。｜答法：Jean 說 2026 年度營運計畫仍在制定、沒有明確路徑，只給營收成長會高於 OpEx 成長；未回答是否前置與 2026 營收預期方向。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Benjamin Reitzes 問近期有什麼事讓 AMD 對 OpenAI 6 gigawatt 更有信心。｜答法：Lisa 描述合約為逐年檢視的紀律式結構、首個 gigawatt 時程與多客戶佈局，稱 quite comfortable，未點名新增的具體事件。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：William Stein 問客戶能否取得資金與電力，以及是否預期出現更多類似 OpenAI 的非典型融資交易。｜答法：Lisa 詳談電力路線圖、超大規模客戶資產負債表穩健與 OpenAI 用量成長，稱融資足夠；未直接回答是否還會有其他非典型融資交易。
- AMD_Analyst_Investor_Day_Advanced_Micro_Devices_Inc_20251111.md｜問：Christopher Caso 問既然近期優先最大化毛利金額，如何看 55% 到 58% 長期區間，以及 MI450 初期是否稀釋毛利率。｜答法：Jean 稱近期毛利率與現在相近、55% 到 58% 取決於 mix 與量，MI450 放量期的毛利影響答稱取決於量與節奏並說目前還不知道；未給稀釋幅度。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 8 | 8 |
| customer_second_source | found | 3 | 7 |
| customer_concentration_credit | found | 5 | 8 |
| supply_demand_durability | found | 4 | 8 |
| regulatory_antitrust | found | 2 | 5 |
| reg_tariff_export | found | 4 | 6 |
| geo_supply_chain | found | 4 | 8 |
| end_markets | found | 15 | 12 |
| substitute_technology | found | 2 | 7 |
| channel_business_model_shift | none | 0 | 8 |
| capital_markets_pricing | found | 5 | 7 |
| major_events | found | 4 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **channel_business_model_shift**（none）：AMD distribution channel disruption shift 2026；AMD business model transition subscription platform 2026；semiconductor industry channel disintermediation direct to customer 2026；AMD go-to-market strategy change 2026；AMD distribution channel disruption business model shift 2026；AMD subscription platform business model transition 2026；AMD go-to-market change 2026 direct sales OEM channel restructuring；semiconductor industry channel disintermediation direct sales hyperscaler 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260805","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Instinct 自個位數份額爬向雙位數，MI450／Helios 的 GW 級承諾轉為實際營收","columns":{"2Y 驗證點":"2027 年資料中心 AI 營收落在 $33B 以上；Meta 首個 GW 的認股權證第一批如期 vest","5Y 驗證點":"AI 加速器份額達雙位數；Helios 成為超大規模第二供應的機櫃級標配","10Y 驗證點":"MI500／Verano 世代維持效能與 TCO 競爭力，份額不回落","具體數字門檻":"2027 年 DC AI 營收 ≥ $35B（管理層對分析師 ~$30B 模型明言「大概太低了」）。品質限定：其中由 AMD 自身股權投資所支撐的 Anthropic 分項須單獨揭露，不計入「純需求」驗證","信息來源":"2026-08-04 法說；2026-02-24 特別法說（Meta 6GW 條款）","漂移觸發條件":"連 2 季 GPU 營收 TTM 偏離指引 ≥ 10% → 削弱"}},{"id":"H2","text":"EPYC 伺服器份額續創高，Intel 製程與產品持續弱勢","columns":{"2Y 驗證點":"營收市佔守住 46%；Venice（Zen 6，2nm）於各大雲端如期部署","5Y 驗證點":"x86 伺服器穩居領先，ARM 侵蝕限於自研範圍","10Y 驗證點":"資料中心 CPU TAM 內維持 &gt;50% 增量份額","具體數字門檻":"EPYC 營收市佔維持 ≥ 45%（現 46.2%）","信息來源":"Mercury Research 2026Q1；公司法說","漂移觸發條件":"連 2 季份額回落 ≥ 3pp → 削弱"}},{"id":"H3","text":"市場願為「AI 第二供應商」付溢價，且激進的 EPS 上修真的兌現","columns":{"2Y 驗證點":"FY2026 EPS ~$7.45 兌現；FY2027 共識 $13.9 不下修","5Y 驗證點":"FY2028 EPS ~$20 量級兌現，倍數隨之自然壓回 24–28x","10Y 驗證點":"盈餘力撐起 $768B+ 市值不靠 re-rate","具體數字門檻":"FY2027 共識 EPS 維持 ≥ $12（含權證稀釋路徑）","信息來源":"買方共識 Excel snapshot 2026-07-30（FY26 $7.45／FY27 $13.78／FY28 $20.02）；yfinance 財報後刷新 n=45–46","漂移觸發條件":"連 2 月共識下修 → 估值假設反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"混合稀釋壓過營運槓桿：MI450／Helios 的毛利率低於公司平均，且 Helios 的 HBM 含量高於對手約 50%，正撞上 SK 海力士執行長口中「史上最差」的 2027 記憶體供給年。管理層兩度拒絕指引 2027 毛利率。","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1–2 季可觸發）","監測指標":"單季毛利率 vs 資料中心營收占比的斜率；FY2027 首次毛利率指引","警戒閾值":"資料中心占比 +5pp 而合併毛利率 −50bp 以上；或 FY2027 指引 &lt; 55%"}},{"id":"R2","text":"對手方信用與循環融資：早期 Helios 客戶名單中的 Oracle 據報處於投機等級邊緣（$1,300 億債務、自 2025-09 高點下跌逾六成、並有退休基金就其 2025 年債券發行前隱匿 OpenAI 交易風險提起證券訴訟）；AMD 自身於 2026-07 對 Anthropic 承諾最高 $50 億里程碑條件股權投資，同時取得其最高 2GW 承諾——AMD 已在用自己的資產負債表補貼一部分 2027 指引裡的需求。","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4–6 季）","監測指標":"Oracle 信用評等與 AMD 相關採購揭露；AMD 對 Anthropic 投資的實際撥付進度與其對應營收占比","警戒閾值":"任一早期 Helios 客戶被降至投機等級或公開延後採購；或自身投資支撐的營收占 2027 DC AI 逾 15%"}},{"id":"R3","text":"產業級 AI 資本支出報酬重定價：2026-07 中下旬四篇獨立報導在同一週窗口記錄同一敘事——AI 資本支出報酬遭質疑、資金窄化回 NVIDIA 一家、AMD／Marvell／Intel 同步下跌。AMD 於 7/23 發表會後五日跌 22%、8/4 財報後再跌 9.2%，兩次都不是公司特定利空。","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"四大超大規模業者 2027 資本支出指引方向；產業前瞻倍數帶","警戒閾值":"任兩家 2027 資本支出指引年增率跌破 +20%；或半導體板塊前瞻倍數帶再下移一個標準差"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":10.6,"ev5y_pct":48.6,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.1,"ev5y_pct":48.6,"irr_base_pct":10.6,"max_dd_pct":-68.0,"bull_5y_price":1260.0,"bear_5y_price":216.0,"p_bull_pct":22.0,"p_bear_pct":33.0,"rearm_trigger":null,"price_at_dd":470.79,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"AMD","date":"2026-09-23","schema":"v15.2","contract":"v19","company_name":"Advanced Micro Devices, Inc."},"oneliner":"伺服器 CPU 與 AI 加速器雙線放量是真的，但 623.77 美元已大致定價管理層 2027–28 年計畫；基本情境五年年化約 6–7%，現價不追，回到 490 美元以下或 Helios 放量明顯超標再加。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20260923/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20260923/scenario.json","answers":{"q1_business":{"verdict":"賺的是雲端業者與 AI 實驗室的算力資本支出：資料中心已占營收 58%；錢卡在兩個節點，上游是台積電先進製程與 HBM 供給，下游是少數 GW 級客戶的付款能力。","reasoning":"AMD 賣三類晶片。資料中心（EPYC 伺服器 CPU 加 Instinct GPU）2026Q2 營收 67 億美元，年增 107%，占營收 58%，部門營業利益率 31%；Client 31 億美元（年增 23%）；遊戲 7.79 億美元（年減 31%）；嵌入式 9.77 億美元（年增 19%，利益率 40%）。全公司 Q2 營收 115.36 億美元，高於共識；non-GAAP 營業利益率 27%，GAAP 17%。Q3 指引 130 億美元上下 3 億、毛利率約 56%。單點依賴：FY2025 年報沒有單一客戶占營收 10% 以上，但未來營收正往 OpenAI、Meta、Anthropic 三家 GW 級合約集中，這是集中度風險，不是護城河證據。產業時鐘判第二期擴張：需求預測仍在上修、產能仍在加、交期仍長；但客戶舉債擴建、供應商用權證換訂單，已是過熱前的訊號。產業態勢是雙向拉鋸：CPU 端結構性轉好（Intel 各區隔都在失份額），AI 端競爭與客戶自研晶片在加壓。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_q3_fy2026_guidance","f_earnings_recency"],"verdict_values":{"revenue_quality":"高成長且以資料中心為主；AI 段依賴多年期、按里程碑的合約，大部分尚未簽定出貨；PC 與遊戲受記憶體與零組件漲價拖累。","unit_econ_note":"部門利益率：資料中心 31%、Client 加遊戲 15%（去年 21%）、嵌入式 40%（去年 33%）；資料中心 AI 毛利率低於公司平均（Jean Hu 2026-05-05、2026-08-04）。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"份額擴張加營業槓桿；需求綁在 AI 資本支出循環上"},"industry":{"clock_phase":"II","sd_verdict_source":"需求端屬結構性（推論與代理式工作負載），但眼前的吃緊有一部分是未預期需求加記憶體短缺；Lisa Su 說 2027 年伺服器供給會比 2026 好，所以交期與定價優勢屬週期性，供給可逆性高。","bargaining":{"up":"上游議價強：台積電掌握約九成先進製程，HBM 短缺預期延續到 2027 年以後；AMD 與客戶分攤成本上漲（Lisa Su 2026-05-05）。","down":"下游集中：三家 GW 級客戶，Meta 另取得 1.6 億股績效權證，議價偏向買方。","geo":"中國約占營收兩成（Lisa Su 2026-05）；輸中 AI 晶片須付 25% 關稅並受量能上限；先進製程集中在台灣。"},"profit_pool_dir":"AI 加速器利潤池仍集中在輝達（營業利益率 65% 對 AMD 16%）；伺服器 CPU 利潤池正從 Intel 流向 AMD。","tam_table":[{"item":"AI 加速器市場（管理層，2030 年）","value":"約 1.4 兆美元，年增 45% 以上（2026-08-04 法說）；2025-11-11 時資料中心整體口徑為 2030 年逾 1 兆美元"},{"item":"伺服器 CPU 市場（管理層，2030 年）","value":"約 2,200 億美元、年增 50% 以上（2026-08-04）；2026-05-05 為逾 1,200 億美元、年增 35% 以上；2025-11-11 為年增約 18%"},{"item":"高效能與 AI 運算整體（管理層）","value":"2030 年接近 2 兆美元，年增約 40%；AMD 目標成長高於市場"},{"item":"第三方 AI 資料中心 GPU 市場","value":"2025 年 111.2 億美元到 2030 年 323 億美元、年增 23.8%（GlobeNewswire 報告）；定義與管理層差距極大，不採用"},{"item":"AMD AI 加速器營收份額","value":"約 5–8%；輝達 70–80%；客戶自研晶片合計 15–20%（Silicon Analysts）"},{"item":"AMD 伺服器 CPU 營收份額","value":"46.2%（2026Q1 紀錄），出貨份額約三分之一"},{"item":"AMD x86 Client 出貨份額","value":"30.3%（2026Q2 首度破 30%，一年前 24.1%）"},{"item":"營業利益池占比五年前到現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平：CPU 端在擴大，AI 端被客戶自研晶片與輝達生態夾住，兩邊互抵，所以不能上調。","reasoning":"機制：x86 伺服器 CPU 的設計與小晶片（chiplet，把大晶片拆成多顆小晶片再封裝，新製程用的晶圓較少）成本結構領先，加上年更路線圖的執行紀錄；AI 端靠開放的 ROCm 軟體與較大的記憶體容量，以第二供應商身分切入。執行力給 9：Venice、MI455X 已量產，Helios 本季出貨，伺服器與 Client 份額都創新高。定價力給 7：CPU 端營收份額高於出貨份額、交期逾 30 週、成本上漲可和客戶分攤；AI 端靠每美元 token 數賣、對 Meta 發權證、資料中心 AI 毛利率低於公司平均，拉低整體。對最強同業輝達的利益率差距為負且大（過去四季毛利率 53.2% 對 74.7%、營業利益率 15.7% 對 65.2%），所以不給 A。當期 ROIC 因事實表缺投入資本無法算；四個持續期檢查點中，價值鏈分配最弱。","fact_refs":["f_peer_amd_gross_margin_pct","f_peer_amd_operating_margin_pct","f_peer_amd_fcf_margin_pct","f_peer_nvda_gross_margin_pct","f_peer_nvda_operating_margin_pct","f_peer_nvda_fcf_margin_pct","f_peer_avgo_operating_margin_pct","f_peer_mrvl_operating_margin_pct","f_peer_3661_tw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"x86 伺服器 CPU 設計與小晶片成本結構領先，加上年更路線圖的執行紀錄；AI 端以開放軟體與記憶體容量做第二供應商。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"CPU：伺服器營收份額 46.2%（2026Q1 紀錄）高於出貨份額約三分之一，代表單價溢價；EPYC 交期逾 30 週；x86 整體份額 34.1%、年增 4.7 個百分點。AI：份額 5–8% 在升，但最大客戶 Meta 與微軟擴大自研晶片，屬最大客戶份額下滑的跡象，方向不能上調。","competitor_notes":[{"name":"NVDA","strategy_note":"AI 加速器營收份額 70–80%，營業利益率 65%、自由現金流率 42%，靠 CUDA 軟體與整櫃方案定價；AMD 以每美元 token 數切入，不是正面比毛利。"},{"name":"AVGO","strategy_note":"不直接賣 GPU，但替 Google、Meta、微軟、OpenAI、Anthropic 設計自研晶片，是 AMD 在 AI 加速器最大的間接對手；營業利益率 49%。"},{"name":"MRVL","strategy_note":"客製晶片與網通第二陣營，利益率結構（毛利 52%、營益 17%）與 AMD 接近，代表客製晶片端的價格競爭。"},{"name":"3661.TW","strategy_note":"世芯，客製晶片設計服務，毛利 37%、自由現金流為負；是超大規模業者自研路線的執行者之一，份額擴張會壓縮通用 GPU 的可觸及市場。"},{"name":"INTC","strategy_note":"x86 對手，伺服器出貨份額仍約 67% 但營收份額降到約 54%，各主要區隔都在失份額；Intel 製程若追上，是 CPU 端最大變數。"}],"threats":[{"level":"🔴","text":"超大規模客戶自研 AI 晶片（Broadcom 代為設計）：Meta 在簽下 AMD 與輝達大單數週後擴大 MTIA 部署，微軟 Maia 200 已上線，OpenAI 與 Anthropic 也在做；這是客戶端的生態攻擊，直接壓縮 AMD 在同一批客戶的 GPU 可觸及市場。","p":40,"evidence_refs":["competitive_share_entrants#5","customer_second_source#0","customer_second_source#1","customer_second_source#2","substitute_technology#0"]},{"level":"🟡","text":"輝達的軟體與整櫃生態：加速器營收份額 70–80%，以絕對金額計差距仍在擴大；AMD 靠開放軟體與記憶體容量追趕。","p":30,"evidence_refs":["end_markets#5"]},{"level":"🟡","text":"ARM 架構伺服器 CPU：Lisa Su 2026-05-05 承認大型客戶會 x86 與 ARM 並用；Venice 宣稱每瓦效能是領先 ARM 方案的 3.3 倍，屬點對點競爭。","p":30,"evidence_refs":[]}],"roic_durability":{"quadrant":"投入資本事實表未涵蓋，象限無法判定；利益率端 GAAP 營業利益率 15.7%（過去四季）、non-GAAP 27%（2026Q2）屬中等。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（模型開發與推論服務）、決策者（雲端業者的基礎設施團隊）、付款者（雲端業者與 AI 實驗室）三環都在，推論算力是需要不是想要；但付款環最弱：OpenAI 首季虧 213 億美元、兩年融資缺口約 1,300 億美元。CPU 端付款者（雲端、企業）穩健，交期逾 30 週。"},{"item":"決策層級","level":"🟡","text":"在單一工作負載層級，客戶多家並用：Meta 同時簽輝達、AMD 又擴大自研；CPU 端 x86 相容，Intel 與 AMD 互換成本低，AMD 靠效能與總持有成本贏，不是靠鎖定。代理讀數：伺服器營收份額高於出貨份額，單價溢價仍在。"},{"item":"價值鏈分配","level":"🔴","text":"上游台積電約九成先進製程、HBM 短缺延續到 2027 年以後，兩者都有定價權；下游 GW 級客戶集中、有自研能力，還拿到 1.6 億股權證；AI 加速器利潤池大半留在輝達。AMD 的增量營收正好落在這段被兩頭擠壓的 AI 業務；CPU 段則相反。"},{"item":"社會容忍度","level":"🟡","text":"AI 晶片受美國出口管制與 25% 關稅，中國約占營收兩成；政策可一夜改變可銷售市場（2025 年曾認列 8 億美元相關費用）。價格上限主要是政治上限，授權依賴商務部逐案審查，屬政策風險。"}],"roiic":"事實表未涵蓋（缺投入資本、資本支出、折舊攤銷與營運資金變動）","reinvest_rate":"事實表未涵蓋；可見的再投資是存貨增到約 85 億美元、研發占營收 22.7%（同業對照表，過去四季）、對客戶與新創的股權安排","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。本包缺兩個輸入，不以估計數硬算；情境樹因此把共識成長視為超過可驗證的內生能力，熊市機率不低於 30%。"}}}},"q3_growth":{"verdict":"五年後跑道仍寬：AI 加速器份額只有 5–8%，代理式 CPU 是管理層點名的下一條成長曲線；但共識成長靠營業槓桿與少數大客戶放量，不是可驗證的再投資報酬。","reasoning":"成長以量為主：Q2 伺服器 CPU 量與單價都雙位數成長、量較多（Lisa Su 2026-08-04）；AI GPU 靠 GW 級合約放量；併購與回購不是來源。共識 EPS FY2026 7.58、FY2027 15.57、FY2028 22.27，兩年年化約 71%；FY2025 實際值事實表未涵蓋，無法算三年。近 3 個月 FY2026 共識上修 2.85%。內生天花板因缺投入資本與再投資率無法計算；缺口可部分歸因於營業槓桿（Q2 營收年增 50%、營業費用年增 40%，non-GAAP 營業利益率 27% 往長期模型 35% 以上走），其餘靠錨定客戶放量，所以長期信心上限為中。衰退訊號亮兩個：EPS 成長明顯快於營收、可觸及市場被客戶自研晶片壓縮；價值陷阱風險中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi5_q3_fy2026_guidance","f_kpi0_gaap"],"verdict_values":{"growth":{"driver_mix":"量為主、價為輔：伺服器 CPU 量與單價同步成長、量較多；AI GPU 靠 GW 級合約放量；小型併購與回購不貢獻。","runway_years":"≥10 年（AI 加速器份額 5–8%，離 30% 很遠；伺服器 CPU 營收份額已 46%，這條跑道較短）","runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本與再投資率，內生天花板無法計算；共識 FY2026 到 FY2028 EPS 年化約 71%，主要來自營收放量加營業槓桿，不是再投資報酬。","segments":[{"item":"資料中心（EPYC 加 Instinct）","value":"2026Q2 營收 67 億美元，年增 107%、季增 16%，占營收 58%；部門營業利益率 31%"},{"item":"Client","value":"31 億美元，年增 23%（行動處理器創新高、Ryzen Pro 年增逾 50%）"},{"item":"遊戲","value":"7.79 億美元，年減 31%（主機週期尾聲、零組件漲價）；Client 加遊戲部門營業利益率 15%（去年 21%）"},{"item":"嵌入式","value":"9.77 億美元，年增 19%，部門營業利益率 40%（去年 33%）；全年新設計案有望逾 180 億美元"},{"item":"2027 管理層方向","value":"伺服器 CPU 年增逾 70%、資料中心部門遠超過翻倍；2026 下半年遊戲較上半年少 20% 以上"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"Q2 可比 EPS 年增約 82%、營收年增 50%；來源是營業槓桿，成長放緩時 EPS 會反向放大"},{"signal":"可觸及市場被替代技術壓縮","lit":true,"evidence":"Meta、微軟自研晶片已部署，Broadcom 替多家 AMD 客戶設計自研晶片"},{"signal":"毛利率連兩季年減","lit":false,"evidence":"Q1 55%（年增 170 基點）、Q2 56%（年增 200 基點）"},{"signal":"核心市占縮減","lit":false,"evidence":"伺服器與 Client 份額都創新高"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"只見於遊戲顯卡（產業零組件漲價），非主力"},{"signal":"自由現金流對淨利低於 0.75","lit":false,"evidence":"過去四季自由現金流率 20.3% 高於營業利益率 15.7%"},{"signal":"SBC 占營收逾 5% 且上升","lit":false,"evidence":"2026Q2 為 4.36%"},{"signal":"產業倍數系統性下移","lit":false,"evidence":"事實表未涵蓋"},{"signal":"維持性資本支出占自由現金流逾 60%","lit":false,"evidence":"事實表未涵蓋；委外製造模式"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"正在擴充晶圓、後段封裝與基板產能"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：錢幾乎全數投回研發、擴產與備貨，回購只夠抵銷股權激勵；對大客戶發權證是新的隱性成本。","reasoning":"自由現金流 Q2 15.58 億美元（營收的 13.5%），比 Q1 的 26 億美元少，主因存貨增到約 85 億美元備貨；過去四季自由現金流率 20.3%，高於 GAAP 營業利益率 15.7%，現金轉換好。SBC 占營收 4.36%，稀釋股數指引連兩季都是 16.6 億股，回購（Q1 買回 2.21 億美元、剩餘授權 92 億美元）只抵銷股權激勵。現金去向：主要是研發（研發密度 22.7%，Q2 營業費用年增 40%）、供應鏈擴產與備貨，其次是小型併購（ZT Systems、MK1、FastFlowLM、Taalas）；股息事實表未涵蓋，法說只提回購。給 Meta 的 1.6 億股績效權證約為現有股數一成。季末現金與短期投資 131 億美元。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_peer_amd_fcf_margin_pct","f_peer_amd_operating_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"ZT Systems（2025-03 完成，製造業務 2025-10 賣給 Sanmina）、MK1、FastFlowLM、Taalas（2026-08）；對價與併購後增量營業利益事實表未涵蓋，無法算已實現報酬"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"2026Q1 買回 110 萬股、2.21 億美元（Jean Hu 2026-05-05），年化不到市值 0.1%（市值以判斷日股價乘指引股數 16.6 億估約 1.04 兆美元），遠低於 10 年期殖利率加 2%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占營收 4.36%；稀釋股數指引 Q2、Q3 都是 16.6 億股，股權激勵的稀釋被回購抵銷；Meta 權證不屬股權激勵，另列反證"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：近年併購是團隊與軟體型小案，對價事實表未涵蓋；股東回報只有抵銷稀釋的回購，現金去向已在理由段交代"}}}},"q5_valuation":{"verdict":"現價要求 FY2031 EPS 做到約 40 美元並維持 25 倍，才有年化 10%，比管理層「顯著超過 20 美元」的計畫再多一段；方向我相信，但現價已沒有多餘報酬，估值偏貴。","reasoning":"市場隱含：以 623.77 美元、要年化 10%，FY2031 EPS 需約 40 美元並給 25 倍前瞻本益比，等於共識 FY2028 22.27 之後還要再年增約 21% 三年。基本情境報酬拆解：EPS 複利年化約 35%，倍數由 82 倍壓到 25 倍年化約 -21%，股息與淨回購約 0，合計年化約 6–7%，重估是拖累不是來源。成長熄火測試：FY2028 之後成長降到 15%、10%、5%，分別給 25、20、15 倍，兩年後股價約 640、490、351 美元，三個情境只有一個守住現價。賣方目標價：S&P 彙整 55 位分析師平均 616.51、MarketBeat 565.13，現價已高於兩者；彙整間差距約 1.09 倍，未到要下修信心的程度。動能：26 週漲 204%，股價高出 52 週均線約 84%，距前份判斷 7 週漲 32.5%，約 9 月 21 日另有單日漲 8.8% 創新高的報導，判為過熱；RSI 資料不可用，未採用。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy2_pct","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_ma_state","f_ma_w52"],"verdict_values":{"valuation":{"basis":"前瞻本益比與 PEG（份額擴張型成長股的優先尺），以 FY2027、FY2028 共識為錨","tier":"大型 AI 算力晶片設計","peers":{"expanded":false,"reason":"事實表只收同業利潤率，未收同業前瞻倍數，屬資料缺口；終端倍數改用自身倍數與成長熄火情境校準"},"fwd_pe":82.29,"peg":1.15,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026 共識 7.58 的 82 倍、FY2027 15.57 的 40 倍、FY2028 22.27 的 28 倍；PEG 約 1.15（前瞻本益比 82.29 除以 FY2026 到 FY2028 兩年 EPS 年化約 71%），落在合理區。但 P/S 24.7 倍、EV/S 24.4 倍都在四個年度端點最高，股價高於賣方平均目標價，基本情境年化只有 6–7%。成長本身不貴，貴在已把管理層計畫當成確定，評偏貴。五年連續分位事實表未涵蓋（只有四個年度端點：本益比分位 43、P/S 與 EV/S 分位 100）。","upside_short_pct":-1.2,"upside_mid_pct":38.3,"denominator_disputed":false,"denominator_note":"FY2026 是 Helios 放量前一年，前瞻一年倍數 82 倍偏高是時間差，不是一次性費用；判斷改看 FY2027、FY2028 共識，分母本身不是爭點。過去四季盈餘口徑的本益比 156 倍反映放量前的低基期，不採用。短期上檔以 S&P 平均目標價 616.51 計，中期以基本情境五年終值計。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是錨定客戶的付款能力與自研晶片的速度，不是 AMD 的產品力；看錯時盈餘和倍數會一起往下。","reasoning":"最可能的虧損路徑：錨定客戶延後加上客戶自研擠壓，同時前瞻本益比從 82 倍壓縮；最大回撤範圍 -45% 至 -72%（回到 52 週均線即 -46%）。空方最強數字：股價已高於賣方平均目標價，OpenAI 兩年融資缺口約 1,300 億美元。訴訟與監管：查無 SEC 調查或重大財報重編（FY2025 年報與 2026 各季季報）；監管風險集中在出口管制與關稅。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_ma_w52","f_ma_w104","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長是真的，陷阱在價格與客戶集中"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":7.58,"pe":82.29,"basis":"FY2026E 共識 EPS（前瞻一年口徑），與終端 FY2031E 前瞻倍數同口徑"},"eps":{"bull":[17.5,27.0,35.0,43.0,50.0],"base":[15.0,21.0,26.0,30.5,34.5],"bear":[12.0,13.0,11.0,12.5,14.0]},"pe":{"bull":30,"base":25,"bear":20},"p":{"bull":22,"base":46,"bear":32},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-72,"hi":-45,"basis":"起點 623.77 美元。回到 52 週均線 339.87 為 -46%，回到 104 週均線 235.31 為 -62%，下緣接近 250 週均線 165.31（-73%）；熊市情境終點 -55%；前份單點 -68%。26 週已漲 204%，前份記錄過 AI 資本支出重定價時五個交易日跌 22%，因此取 -45% 至 -72%；走到下緣需錨定客戶延後加產業倍數重定價同時發生。","trigger_time":null},"basis":{"bull":"Helios 放量超預期，AI 加速器份額走到第三方估的 15–20%，伺服器營收份額過 50%；FY2028 EPS 27 美元、FY2031 達 50 美元，終端 30 倍前瞻本益比（屆時成長仍約 16%）。","base":"管理層計畫大致兌現，但權證稀釋與 HBM 成本吃掉一點：FY2027 15.0、FY2028 21.0，之後成長由 24% 降到 13%；終端 25 倍前瞻本益比，同業現值倍數事實表未涵蓋，以成長熄火測試中 15% 成長對應 25 倍校準。","bear":"錨定客戶延後、自研晶片擠壓，AI 資本支出在 2028–29 年轉入消化期：EPS 在 FY2028 13 美元見頂、FY2029 回落到 11、FY2031 回到 14；終端 20 倍，取成長降到 10% 的情境倍數。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"OpenAI 首季虧 213 億美元、兩年融資缺口約 1,300 億美元；S&P 以 OpenAI 曝險為主因把 Oracle 降到 BBB-；GW 級合約多年期、按里程碑，大部分營收尚未簽定出貨；Meta 簽約數週後擴大自研晶片。","assumption":"錨定客戶會照時程把 GW 級合約轉成實際採購。","consequence":"AI 資本支出在 2027–28 年轉入消化期時，AMD 身為第二供應商最先被砍；FY2031 EPS 可能停在 14 美元上下，股價回到約 280 美元（-55%）。這條與唯一致命點部分重疊，唯一致命點取其中最集中的一環（錨定客戶延後）。","ruling":"部分採納：熊市機率給 32%。不全採，因為伺服器 CPU 成長不依賴這幾家 AI 客戶，且 Meta 信用仍強（Moody's 2026-07-24），Anthropic 與微軟是新增分散。","watch":"錨定客戶部署進度、OpenAI 融資消息、評等機構動作","evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#4","customer_second_source#0"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Meta 取得 1.6 億股績效權證，約現有股數一成；Helios 的 HBM 比對手多約 50%，代搭的 HBM 不賺同等毛利（Lisa Su 2025-11-11），記憶體短缺延續到 2027 年以後；資料中心 AI 毛利率低於公司平均；Q2 自由現金流因備貨從 Q1 的 26 億降到 15.58 億美元。","assumption":"營收翻倍會等比例變成每股盈餘。","consequence":"營收照計畫走，但每股盈餘被權證稀釋與毛利組合拉低 10–15%。","ruling":"採納：基本情境 FY2027 EPS 取 15.0，低於共識 15.57，已反映部分稀釋；毛利率 55% 列為停損指標。","watch":"稀釋股數（指引 16.6 億）、non-GAAP 毛利率、存貨","evidence_refs":["customer_concentration_credit#1","supply_demand_durability#0"],"fact_refs":["f_kpi3_fcf","f_kpi4_sbc"]},{"view":"價格已反映太多","evidence":"股價 623.77 高於 S&P 彙整 55 位分析師平均目標 616.51 與 MarketBeat 565.13；前瞻本益比 82 倍（FY2027 約 40 倍）；P/S 24.7 倍在四個年度端點最高；26 週漲 204%，高出 52 週均線約 84%。","assumption":"市場已把管理層 2027–28 年計畫當成確定。","consequence":"基本情境五年總報酬約 38%、年化約 6–7%；Helios 放量只要晚一季，倍數壓縮就會先來。","ruling":"採納：現價不加碼；回到 490 美元以下，或 2026Q4 資料中心季增 ≥20% 且 FY2027 共識升到 17 以上，才重新加。","watch":"股價對 FY2027 共識 EPS 的倍數","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_ps_percentile","f_week26_return_pct","f_ma_w52"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 470.79 → 本次 623.77（+32.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=470.79","side_b":"本次 price_at_dd=623.77","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2027 資料中心 AI 規模","cause":null,"prior_field":null,"side_a":"管理層：2027 資料中心部門遠超過翻倍，分析師估的 Instinct 約 300 億美元「大概太低」，Helios 需求量超過原先預測（2026-08-04 法說，Lisa Su）。","side_b":"GW 級合約多年期、按里程碑，大部分營收尚未簽定出貨；最大對手方 OpenAI 首季虧 213 億美元、兩年融資缺口約 1,300 億美元；S&P 以 OpenAI 曝險為主因把 Oracle 降到 BBB-。","ruling":"可調和（程度差異）：Meta 信用仍強，Anthropic 與微軟是新增分散，2027 翻倍的方向可信；金額上限取決於 OpenAI 能否籌到錢。基本情境 FY2027 EPS 取 15.0，略低於共識 15.57。","evidence_level":"管理層指引加第三方媒體與評等機構","settle_metric":"2026Q4、2027Q1 資料中心部門季增率","if_then":["若 2026Q4 資料中心季增 ≥20% 且 Q1 指引續增，則維持基本情境，股價 ≤490 美元時分兩筆加碼","若任一季季增 <10% 或 OpenAI 公開延後部署，則減碼一半"],"evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#3","customer_concentration_credit#4"]},{"axis":"2027 毛利率","cause":null,"prior_field":null,"side_a":"Jean Hu 2025-11-11：2027 資料中心 AI 量若很大，毛利率可能靠近 55% 區間下緣，MI450 是否稀釋「目前還不知道」；2026-05-05：MI450 毛利率低於公司平均。","side_b":"Jean Hu 2026-08-04：伺服器、嵌入式與 Client 可大致抵銷，但第三次仍不給 2027 毛利率數字；Helios 的 HBM 比對手多約 50%，記憶體短缺預期延續到 2027 年以後。","ruling":"可調和但偏空：管理層三次只給方向不給數字，HBM 成本又由 AMD 承擔，2027 毛利率跌破 55% 的機率不低；以 55% 設為停損指標。","evidence_level":"管理層前後說法加產業新聞","settle_metric":"2026Q4 non-GAAP 毛利率；FY2027 首次毛利率指引","if_then":["若 2026Q4 毛利率 ≥56% 且 FY2027 指引 ≥55%，則把毛利率風險降為觀察","若連兩季 <55%，則減碼三分之一"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"伺服器 CPU 市場規模口徑","cause":null,"prior_field":null,"side_a":"2025-11-11 分析師日：伺服器 CPU 市場未來 3–5 年年增約 18%。","side_b":"2026-05-05 改為年增 35% 以上、2030 年逾 1,200 億美元；2026-08-04 再改為年增 50% 以上、2030 年約 2,200 億美元（Lisa Su）。","ruling":"可調和：上修有實績支撐（Q2 雲端與企業伺服器都年增逾 70%、交期逾 30 週），但九個月內三度上修，市場規模數字不作估值依據，只認已實現的伺服器營收。","evidence_level":"管理層前後說法加已實現營收","settle_metric":"2026 下半年伺服器營收年增是否超過 80%","if_then":["若 2026 下半年伺服器年增 >80%，則 H2 維持，並把 2027 年增 70% 視為底線","若低於 60%，則停止加碼並把 H2 降為削弱"],"evidence_refs":["competitive_share_entrants#3","end_markets#1"]},{"axis":"費用紀律","cause":null,"prior_field":null,"side_a":"Jean Hu 2025-11-11 承諾營收成長快於費用；2026-08-04 再說費用增速會低於營收增速。","side_b":"Q2 營業費用 34 億美元，高於 2026-05-05 給的約 33 億美元；Q1 被問費用一再超過指引時未解釋；Q3 指引再升到 36.5 億美元。","ruling":"可調和：Q2 營收也超過指引約 3%，營收年增 50% 仍大於費用年增 40%，營業槓桿成立；但費用指引準確度差，營業槓桿以實際增速差認定，不看指引。","evidence_level":"公司指引與實際值","settle_metric":"營業費用年增率對營收年增率","if_then":["若營業費用年增連兩季高於營收年增，則 H3 降為削弱並停止加碼","若差距維持 10 個百分點以上，則 H3 維持"],"evidence_refs":[]},{"axis":"現在就賣對現在就買","cause":null,"prior_field":null,"side_a":"現在就賣的最強論證：股價已高於賣方平均目標價（616.51、565.13），前瞻本益比 82 倍、P/S 在四年高點、26 週漲 204%；基本情境五年年化只有 6–7%；只要 Helios 晚一季或毛利率跌破 55%，盈餘和倍數會一起修正。","side_b":"現在就買的最強論證：FY2027 共識自 7 月底 13.78 升到 15.57，30 天內 FY2027 上修 33 次對下修 3 次；管理層暗示分析師的 AI 營收估計太低；若 AI 份額到第三方估的 15–20%，FY2028 EPS 可到 27 美元，現價只有 23 倍。","ruling":"不可調和（估值方向相反，論點本身不矛盾）。裁決：持有，不加也不賣。依據：買方論點建立在尚未出貨的 Helios 量能，賣方論點建立在已經發生的價格；第一個完整放量季（2026Q4）出來前，價格這邊的證據較硬。硬數據點：股價是 FY2027 共識的 40 倍，基本情境五年總報酬約 38%。","evidence_level":"事實表加賣方彙整","settle_metric":"2026Q4 資料中心季增與 FY2027 共識 EPS","if_then":["若 2026Q4 資料中心季增 ≥20% 且 FY2027 共識 ≥17，則加碼至原部位 1.5 倍","若股價 ≥760 美元而 FY2027 共識 <17，則減碼三分之一","反向條件：若股價 ≤490 美元且共識不低於 15，則分兩筆加碼"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#4"]},{"axis":"前份漂移：價格","cause":"價格變動","prior_field":["dca_verdict","dca_role","signal","val","asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份 2026-08-05：股價 470.79 美元，判進場，估值合理，上下檔比 2.1，五年期望報酬 48.6%，基本情境年化 10.6%，訊號等級 B。","side_b":"本次：股價 623.77 美元（+32.5%）；FY2027 共識 15.57（前份 13.78，+13%），FY2028 22.27（前份 20.02，+11%）；股價漲幅約為盈餘上修的 2.5 倍，倍數擴張吃掉預期報酬。","ruling":"估值由合理轉偏貴；上下檔比、期望報酬與基本情境報酬由程式依新情境重算，預期明顯下降；訊號等級維持 B，因為生意品質沒變；裁決與角色若改列，原因是價格，不是基本面轉壞。","evidence_level":"事實表加前份摘要","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若倍數回到 31 倍以內（約 490 美元）且共識不降，則恢復分批加碼","若倍數升到 49 倍以上（約 760 美元）而共識未跟上，則減碼三分之一"],"evidence_refs":[]},{"axis":"前份漂移：情境樹","cause":"方法變動","prior_field":["bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：牛市五年價 1,260 美元、熊市 216 美元，機率牛 22%、熊 33%，最大回撤單點 -68%。","side_b":"本次：終端年改為 FY2031E，與起點同用前瞻一年口徑；熊市終端 EPS 14.0 壓在 FY2027 共識以下，倍數用成長降到 10% 的 20 倍；牛市 50 美元乘 30 倍；機率牛 22%、基本 46%、熊 32%；最大回撤改填範圍 -45% 至 -72%。","ruling":"熊市機率 33% 到 32% 屬微調：客戶自研與融資的負面證據增加，但 Anthropic、微軟兩家新客戶分散了單一對手方風險，大致抵銷；共識成長超過可驗證的內生能力，熊市機率不低於 30%。牛熊五年價由程式依新路徑重算。","evidence_level":"方法說明","settle_metric":"錨定客戶部署進度；2026Q4 資料中心季增","if_then":["若錨定客戶任一延後，則熊市機率上調至 40% 並減碼一半","若 2026Q4 資料中心季增 ≥20%，則牛市機率上調至 28%"],"evidence_refs":[]},{"axis":"前份漂移：品質與結構判斷","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：價值陷阱風險中等、護城河方向持平、五年後跑道寬、品質複利成長型、未判循環位置。","side_b":"本次結論相同，新證據兩面：x86 整體份額 34.1%、伺服器營收份額 46.2%、Client 出貨份額首度破 30%；同時 Meta 簽約數週後擴大自研晶片、微軟 Maia 200 已部署、Broadcom 替 OpenAI 與 Anthropic 設計自研晶片。","ruling":"正負證據互抵，五欄維持：CPU 份額上升，但 AI 端最大客戶在做自研，護城河方向不能上調；AI 份額 5–8% 離飽和很遠，跑道仍寬；成長仍以份額擴張加營業槓桿為主，不改判為循環股，所以不填循環位置。","evidence_level":"產業研究機構份額資料加媒體報導","settle_metric":"伺服器營收份額；AI 加速器份額","if_then":["若 Meta 或微軟公開以自研晶片取代 Instinct 部署，則護城河方向改為下降並減碼三分之一","若 AI 份額在 2027 年底前升過 12%，則護城河方向改為上升"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#0","customer_second_source#1","customer_second_source#2","substitute_technology#0"]},{"axis":"前份漂移：假設與風險門檻","cause":"方法變動","prior_field":["H","R"],"side_a":"前份：H1 2027 資料中心 AI 營收 ≥350 億美元；H2 EPYC 營收份額 ≥45%；H3 FY2027 共識 EPS ≥12；R1 資料中心占比升 5 個百分點而毛利率降 50 基點，或 FY2027 指引 <55%；R2 早期 Helios 客戶降到投機等級或延後，或自身投資支撐的營收占 2027 資料中心 AI 逾 15%；R3 任兩家雲端 2027 資本支出年增跌破 20% 或板塊倍數下移一個標準差。","side_b":"本次：H1 改為資料中心部門 2027 營收翻倍、每季季增 ≥10%；H2 改為伺服器營收份額每季 ≥45% 並朝 2030 年過 50%；H3 改為毛利率 ≥55%、non-GAAP 營業利益率 FY2027 ≥32%；前份 R1、R2 門檻保留在 R1、R2；前份 R3 保留為 R6；新增客戶自研晶片（R3）、中國與台灣（R4）、PC 與遊戲（R5）。","ruling":"H1 改門檻，因為公司不單獨揭露資料中心 AI 營收，無法按季驗證；H3 共識已到 15.57，舊門檻 12 失去鑑別力，改看營業槓桿本身。前份 R2 的自身投資比例、R3 的雲端資本支出與板塊倍數，本包事實表未涵蓋，標資料缺口保留，不退休。","evidence_level":"方法說明","settle_metric":"資料中心部門營收；毛利率；營業利益率","if_then":["若 FY2027 資料中心部門營收未達 FY2026 的 2 倍，則 H1 判反轉並減碼一半","若毛利率連兩季 <55%，則減碼三分之一"],"evidence_refs":[]},{"axis":"停損指標（減碼、清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標（null）。","side_b":"本次設五項：資料中心季增 <10%；毛利率連兩季 <55%；錨定客戶延後或縮減；伺服器份額兩季合計掉 3 個百分點以上；FY2027 共識下修逾 15%。任一觸發減碼三分之一（錨定客戶延後為減碼一半），兩項以上清倉。","ruling":"前份格式沒有這一欄，本次補上；門檻取自管理層 2026-08-04 的放量節奏與長期毛利率區間下緣 55%。","evidence_level":"方法說明","settle_metric":"五項停損指標","if_then":["若任一項觸發，則減碼三分之一","若兩項以上同時觸發，則清倉"],"evidence_refs":[]},{"axis":"重新加碼條件（加碼）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設（null）。","side_b":"股價回落到 490 美元以下（約 FY2027 共識 EPS 的 31 倍）且 FY2027 共識不低於 15 美元，才恢復分批加碼。","ruling":"前份在 470.79 美元已判進場，不需要重啟條件；本次現價的限制是價格，重啟條件就是價格回到基本情境年化約 12% 的位置（基本情境終值 862.5 美元折回五年）。","evidence_level":"情境樹推算","settle_metric":"股價與 FY2027 共識 EPS","if_then":["若股價 ≤490 美元且共識 ≥15，則分兩筆加碼","若共識跌破 13.2，則取消加碼條件，改依停損指標處理"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）。","side_b":"OpenAI、Meta、Anthropic 三個 GW 級錨定客戶中，任一家公開延後或縮減 MI450／Helios 部署。","ruling":"前份格式沒有唯一致命點；本次選這一項，因為它是最大的單一敏感度：每 GW 營收是雙位數十億美元（Lisa Su 2026-08-04），少一家等於 2027 年少掉以百億美元計的營收，毛利率每掉 1 個百分點的影響小一個量級。","evidence_level":"管理層每 GW 營收說法加情境推算","settle_metric":"錨定客戶部署公告","if_then":["若任一家延後兩季以上或縮減，則減碼一半並停止加碼","若兩家以上，則清倉"],"evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2"]}],"triggers":[{"n":1,"text":"2026Q3 財報：資料中心部門季增要到雙位數，且第四季指引的季增要高於第三季","type":"假設驗證","maps_to":"H1","metric":"資料中心部門營收季增率","threshold":"Q3 季增 ≥10%，Q4 指引季增高於 Q3","action":"達標續抱；未達停止加碼","source_freq":"每季財報","date":"2026-11（公司未公告確切日）"},{"n":2,"text":"伺服器 CPU 份額：Venice 世代上市後份額要續升","type":"假設驗證","maps_to":"H2","metric":"Mercury Research 伺服器 CPU 營收份額","threshold":"每季 ≥45%，連兩季合計下滑不超過 3 個百分點","action":"跌破門檻停止加碼；跌破 42% 減碼三分之一","source_freq":"每季","date":null},{"n":3,"text":"毛利率守不住 55%：Helios 放量與 HBM 成本壓過組合改善","type":"風險","maps_to":"R1","metric":"non-GAAP 毛利率","threshold":"單季 <55%，或 FY2027 首次毛利率指引 <55%","action":"減碼三分之一","source_freq":"每季財報","date":"2027-02","evidence_refs":["supply_demand_durability#0"]},{"n":4,"text":"錨定客戶融資與信用：OpenAI 融資結果與評等機構對其相關業者的動作","type":"風險","maps_to":"R2","metric":"OpenAI 大型融資結果；以 OpenAI 曝險為由的降評","threshold":"OpenAI 大型融資失敗，或再有一家 AMD 客戶因 OpenAI 曝險被降到投機等級","action":"停止加碼","source_freq":"事件","date":null,"evidence_refs":["customer_concentration_credit#2","customer_concentration_credit#4"]},{"n":5,"text":"客戶自研晶片擠壓 AMD 在同一批客戶的份額","type":"風險","maps_to":"R3","metric":"AMD AI 加速器份額（第三方估計）；Meta、微軟自研晶片部署公告","threshold":"2027 年底份額仍低於 10%，或 Meta、微軟公開以自研晶片取代 Instinct 部署","action":"減碼三分之一","source_freq":"半年","date":"2027-12","evidence_refs":["customer_second_source#0","customer_second_source#2","substitute_technology#0"]},{"n":6,"text":"唯一致命點：OpenAI、Meta、Anthropic 任一家公開延後或縮減 GW 級部署","type":"Single Thing","maps_to":"H1","metric":"錨定客戶部署公告與公司法說進度","threshold":"任一家延後兩季以上或縮減規模","action":"減碼一半並停止加碼；兩家以上清倉","source_freq":"事件","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":7,"text":"股價回到約 FY2027 共識 EPS 的 31 倍以內，且共識不降","type":"估值rearm","maps_to":"H3","metric":"股價對 FY2027 共識 EPS","threshold":"股價 ≤490 美元且 FY2027 共識 EPS ≥15","action":"分兩筆加碼","source_freq":"每日股價加每月共識快照","date":null},{"n":8,"text":"Helios 放量明顯超標，共識追上","type":"加碼","maps_to":"H1","metric":"2026Q4 資料中心季增；FY2027 共識 EPS","threshold":"Q4 資料中心季增 ≥20% 且 FY2027 共識 ≥17","action":"加碼至原部位 1.5 倍","source_freq":"每季加每月","date":"2027-02"},{"n":9,"text":"股價跑在盈餘前面","type":"減碼","maps_to":"H3","metric":"股價與 FY2027 共識 EPS","threshold":"股價 ≥760 美元（約 FY2027 共識 49 倍）且 FY2027 共識 <17","action":"減碼三分之一","source_freq":"每日","date":null},{"n":10,"text":"停損指標任兩項同時觸發","type":"清倉","maps_to":"H1","metric":"五項停損指標","threshold":"任兩項觸發","action":"清倉","source_freq":"每季","date":null},{"n":11,"text":"FY2026 年報與 FY2027 首次全年指引出來後，重做完整研究","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重做完整研究","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"資料中心部門單季營收季增率","bear_threshold":"2026Q4 或 2027Q1 任一季 <10%","window":"2026Q4 至 2027Q2 財報","source":"公司季報新聞稿","last_status":"ok"},{"metric":"non-GAAP 毛利率","bear_threshold":"連續兩季 <55%","window":"2026Q4 至 2027Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"錨定客戶（OpenAI、Meta、Anthropic）部署進度","bear_threshold":"任一家公開延後兩季以上或縮減規模","window":"2026Q4 至 2027Q4","source":"公司法說、客戶公告","last_status":"warning"},{"metric":"伺服器 CPU 營收份額","bear_threshold":"連兩季合計下滑 3 個百分點以上","window":"每季","source":"Mercury Research","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"較 15.57 下修逾 15%（低於 13.2）","window":"每月快照，至 2027-06","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回落到 490 美元以下（約 FY2027 共識 EPS 的 31 倍）且 FY2027 共識不低於 15 美元，才恢復分批加碼","exec_line":"現價持有，不追也不賣；≤490 美元分兩筆加碼；Q4 資料中心季增 ≥20% 且 FY2027 共識 ≥17 可加到 1.5 倍；≥760 美元而共識未跟上減碼三分之一；錨定客戶延後減碼一半，兩家以上清倉"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=203.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"Helios／MI450 讓 GW 級合約在 2027 年變成實際營收，資料中心部門營收翻倍以上","2y":"FY2027 資料中心部門營收 ≥ FY2026 的 2 倍；2026Q4 起每季季增 ≥10%","5y":"AI 加速器營收份額由 5–8% 升到 12% 以上，錨定三家之外至少再有兩家 GW 級客戶","10y":null,"threshold":"2026Q4、2027Q1 資料中心部門季增各 ≥10%；FY2027 資料中心營收 ≥ FY2026 的 2 倍","source":"公司季報；2026-08-04 法說（Lisa Su、Jean Hu）；第三方 AI 加速器份額估計","drift_rule":"資料中心部門營收連 2 季低於指引中值 5% 以上為削弱；連 3 季低 10% 以上為反轉"},{"id":"H2","text":"EPYC 份額續升：Venice 世代把伺服器 CPU 營收份額推過 50%","2y":"2027 年伺服器 CPU 營收年增 ≥70%；營收份額守住 46% 以上","5y":"伺服器 CPU 營收份額超過 50%（2025-11-11 分析師日目標）","10y":null,"threshold":"Mercury Research 伺服器營收份額每季 ≥45%；2026 下半年伺服器營收年增 >80%","source":"Mercury Research 季度份額；公司法說（2026-05-05、2026-08-04）","drift_rule":"份額連 2 季合計下滑 3 個百分點以上為削弱；跌破 42% 為反轉"},{"id":"H3","text":"營業槓桿兌現：營收成長快於費用，毛利率守住 55% 以上，non-GAAP 營業利益率往 35% 走","2y":"FY2027 non-GAAP 營業利益率 ≥32%；每季毛利率 ≥55%","5y":"FY2029 起 non-GAAP 營業利益率 ≥35%（分析師日長期模型），EPS 顯著超過 20 美元","10y":null,"threshold":"起點：2026Q2 non-GAAP 營業利益率 27%、毛利率 56%；營業費用年增持續低於營收年增","source":"公司季報；2025-11-11 分析師日長期模型；2026-08-04 法說（Jean Hu）","drift_rule":"毛利率連 2 季 <55%，或營業費用年增連 2 季高於營收年增，為削弱；連 3 季為反轉"}],"R":[{"id":"R1","text":"Helios 放量初期良率與 HBM 成本壓毛利率：Helios 的 HBM 比對手多約 50%，記憶體短缺延續到 2027 年以後；管理層至今不給 2027 毛利率","h_ref":"H3","clock":"⚡","threshold":"單季 non-GAAP 毛利率 <55%，或 FY2027 首次毛利率指引 <55%，或資料中心占比升 5 個百分點而毛利率降 50 基點以上","evidence_refs":["supply_demand_durability#0"]},{"id":"R2","text":"錨定客戶信用與集中：GW 級合約多年期、按里程碑，大部分營收未簽定出貨；OpenAI 首季虧 213 億美元、兩年融資缺口約 1,300 億美元；S&P 因 OpenAI 曝險把 Oracle 降到 BBB-；Meta 拿到 1.6 億股績效權證","h_ref":"H1","clock":"🔥","threshold":"任一錨定客戶或早期 Helios 客戶公開延後、縮減採購或被降到投機等級；或 AMD 自身股權投資支撐的營收占 2027 資料中心 AI 逾 15%（本包未收錄該投資，資料缺口）","evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#4"]},{"id":"R3","text":"客戶自研晶片吃掉可觸及市場：Meta MTIA、微軟 Maia 200 已部署，Broadcom 替 Google、Meta、微軟、OpenAI、Anthropic 做自研晶片；輝達仍拿 70–80% 加速器營收","h_ref":"H1","clock":"🐢","threshold":"第三方估計 AMD AI 加速器份額到 2027 年底仍低於 10%，或客戶自研晶片合計份額升過 25%","evidence_refs":["competitive_share_entrants#5","customer_second_source#0","customer_second_source#1","customer_second_source#2","substitute_technology#0","end_markets#5"]},{"id":"R4","text":"中國與台灣：中國約占營收兩成，輸中 AI 晶片須付 25% 關稅並受量能上限；先進製程集中在台灣台積電；2025 年曾因禁令認列 8 億美元費用、損失約 15 億美元營收","h_ref":"H1","clock":"🔥","threshold":"再有針對 AMD 產品的出口限制或關稅擴大，導致單季認列存貨相關費用逾 5 億美元或下修財測","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R5","text":"PC 與遊戲轉弱：記憶體與零組件漲價，遊戲 Q2 年減 31%、下半年較上半年再少 20% 以上，管理層預期下半年 PC 市場走軟","h_ref":"H3","clock":"⚡","threshold":"Client 營收由年增轉為年減連 2 季","evidence_refs":["end_markets#11"]},{"id":"R6","text":"產業級 AI 資本支出報酬重定價：Moody's 已把前所未見的 AI 支出列為超大規模業者整體信用風險；AMD 身為第二供應商，對資本支出放緩的彈性大於輝達","h_ref":"H3","clock":"🐢","threshold":"任兩家超大規模業者 2027 資本支出指引年增跌破 20%，或半導體板塊前瞻倍數帶下移一個標準差（兩項本包未涵蓋，資料缺口）","evidence_refs":["customer_concentration_credit#3"]}],"single_thing":{"description":"OpenAI、Meta、Anthropic 三個 GW 級錨定客戶中，任一家公開延後或縮減 MI450／Helios 部署","why_fatal":"2027 年資料中心部門遠超過翻倍主要靠這三家放量；每 GW 營收是雙位數十億美元（Lisa Su 2026-08-04），少一家等於 2027 年少掉以百億美元計的營收，FY2027 EPS 可能少 15–25%；現價倍數建立在這條路徑上，盈餘和倍數會同時往下","if_happens":"減碼一半並停止加碼；兩家以上清倉","how_monitor":"公司法說的部署進度、客戶公告、OpenAI 融資消息、評等機構對 OpenAI 相關業者的動作","probability":"12–24 個月約 20%：OpenAI 融資缺口是主要來源；Meta 信用仍強（Moody's 2026-07-24），Anthropic 與微軟是新增分散，壓低機率"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":40.1,"peg_fy2":0.93,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":7.58,"FY2027E":15.57,"FY2028E":22.27},"fy_end_month":12,"eps_basis":"推定為 non-GAAP 稀釋 EPS 共識（與 Q1 1.37、Q2 1.66 的 non-GAAP 季 EPS 同量級），Koyfin 2026-09-19 快照；FY2025 實際值事實表未涵蓋，基期留空；FY2026E 到 FY2028E 兩年年化約 71%；共識家數事實表未涵蓋（S&P 評等彙整為 55 位）"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026Q3 財報與 Q4 指引（Helios 首批出貨後第一份數字）","impact":"高","watch":"資料中心季增、毛利率、Q4 指引"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"Helios 第四季放量、Venice 雲端部署開始","impact":"高","watch":"客戶部署公告與出貨節奏"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 年報與 FY2027 首次全年指引（含毛利率）","impact":"高","watch":"毛利率指引是否 ≥55%"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"Anthropic 首個 GW 部署開始（上半年）","impact":"中","watch":"部署進度"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"台積電亞利桑那第二廠 3 奈米目標量產（2027 下半年）","impact":"低","watch":"AMD 是否取得台灣以外的先進製程產能"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
