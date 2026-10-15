你是 DD 管線 v20 的判斷層閘（gate），標的 GFS（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1786 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
  - 註記：高於公司自家指引區間上緣（CEO 說法）；Earnings Whispers 共識約 $1.76B（二手來源，未經 IR 驗證）
- `f_kpi1_non_ifrs`（q1_business）｜Non-IFRS 營業利益率＝16.7 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝9.7 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_kpi6_q3_2026`（q1_business）｜下一季（Q3 2026）指引：營收＝1885 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-05 date｜期間與口徑：2026-08-05／距今 48 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-05）
- `f_peer_gfs_gross_margin_pct`（q2_moat）｜GFS 毛利率＝27.14 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gfs_operating_margin_pct`（q2_moat）｜GFS 營業利益率＝11.59 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gfs_fcf_margin_pct`（q2_moat）｜GFS FCF 利潤率＝11.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2330_tw_operating_margin_pct`（q2_moat）｜2330.TW 營業利益率＝56.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2330.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2303_tw_gross_margin_pct`（q2_moat）｜2303.TW 毛利率＝30.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2303_tw_operating_margin_pct`（q2_moat）｜2303.TW 營業利益率＝20.13 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2303_tw_fcf_margin_pct`（q2_moat）｜2303.TW FCF 利潤率＝23.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_intc_operating_margin_pct`（q2_moat）｜INTC 營業利益率＝7.55 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.INTC.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_operating_margin_pct`（q2_moat）｜005930.KS 營業利益率＝36.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.96 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.63 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.56 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝3.16 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 1.9 → 1.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_kpi3`（q4_capital）｜營業現金流＝405 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_kpi4_non_ifrs`（q4_capital）｜調整後自由現金流（Non-IFRS）＝-3 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝49.4 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GlobalFoundries Q2 2026 財報新聞稿（6-K 附件）https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000218/globalfoundries2q2026earni.htm（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-05））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝48.24 USD｜期間與口徑：2026-10-09（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-09（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝24.61 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 1.96，分子＝快照價 48.24｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝37.69 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-09（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.88 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝72.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝72.5 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝3.78 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝62.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝62.2 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（1.96 → 1.96）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.38 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（2.62 → 2.63）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.28 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（3.55 → 3.56）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-08）
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.498 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-1.02 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-09（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝50.83｜期間與口徑：2026-10-09（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-09（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（26 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Counterpoint 純晶圓代工季度份額：GFS 由 2024Q4 約 5% 降至 2025 年 4%，2026Q1 為 3%；TSMC 2026Q1 佔 73%，產業年增 30%（AI GPU/ASIC 驅動）。
  - 來源：Counterpoint Research, Global Pure Foundry Market Share: Quarterly（as_of 2026-03-31）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：Simply Wall St 社群敘事（非公司/機構資料）主張 GFS 先進製程落後 TSMC/Samsung，且在地化要求與客戶垂直整合為風險；未找到 2026 針對 GFS 的具名新進入者報導。
  - 來源：Simply Wall St community narrative（as_of 2026-01-01）｜affects：decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2024 20-F：兩個匿名客戶各超過營收 10%，Customer A 2024 年占 16%（$1,061M）、Customer B 占 11%（$722M）；客戶名稱未揭露。
  - 來源：GLOBALFOUNDRIES Form 20-F FY2024 (SEC EDGAR)（as_of 2024-12-31）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2021 20-F：前十大客戶占晶圓出貨量 2019/2020/2021 年約 73%/73%/67%；公司預期營收仍將集中在少數客戶。
  - 來源：GLOBALFOUNDRIES Form 20-F FY2021 (SEC EDGAR)（as_of 2021-12-31）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：12 吋擴產近 70% 來自中國晶圓廠，其餘地區擴產溫和；TSMC 縮減 12 吋成熟產能預期將轉單給其他代工廠
  - 來源：TrendForce／iconnect007（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：TrendForce 2023 年預測中國成熟製程產能占比 2027 年達 39%，並警告 CIS、DDI、PMIC、功率離散元件可能價格競爭（舊預測，早於 2026 年緊俏）
  - 來源：TrendForce press 2023-12-14（as_of 2023-12-14）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：GF 2026 Q2 財報電話會議：車用與智慧行動營收轉弱，家用與工業 IoT 改善
  - 來源：GlobalFoundries Q2 2026 earnings call highlights (MarketBeat)（as_of 2026-08-05）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#7`（supply_demand_durability｜方向 -｜狀態 ok）：消費性電子受記憶體漲價與零組件成本拖累，2026 下半年出貨承壓，部分客戶希望延後漲價
  - 來源：TrendForce DRAMeXchange weekly research（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：2024-11 美國商務部 BIS 就 GFS 2021-02 至 2022-10 間向實體清單中國公司出口晶圓的違規予以處罰（GFS 承認違反 EAR）；屬過往出口管制執法。
  - 來源：Linklaters: Due Diligence in China's Semiconductor Value Chain - Lessons from the GlobalFoundries Enforcement Case（as_of 2024-11-07）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2024-11-01 BIS 對 GFS 處以50萬美元和解罰款：2021–2022年向實體清單公司 SJ Semiconductor 出貨約1,710萬美元晶圓未取得許可；GFS自行揭露並合作，歸因於交易篩查系統資料輸入錯誤。
  - 來源：Manufacturing Dive / BIS 執法案（as_of 2024-11-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：據 policyrisk.com 對 SEC 申報的摘要，GF 對單一 SOI 晶圓供應商（摘要指為 Soitec）的採購占比為 2025 年 71.4%、2024 年 60.9%、2023 年 63.0%；替換該供應商需時甚長。部分原料（稀土、天然氣）亦有單一來源，價格與供應受美中貿易緊張及烏克蘭、中東衝突影響。（二手摘要，未核對申報原文）
  - 來源：policyrisk.com GFS company page（SEC 申報摘要）（as_of 2026-02-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：GF 申報文件的風險語言提及其業務可能受地緣政治狀況影響，例如與中國的政治與貿易緊張（2024 年 6-K 與投資人文件；非 2026 專屬揭露）。
  - 來源：GLOBALFOUNDRIES Form 6-K 3Q2024 earnings（as_of 2024-11-12）｜affects：decision_inputs.bear、thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Q2 2026 智慧行動裝置段營收年減 5.7%（上半年 -5.3%），歸因記憶體價格導致智慧手機疲弱；居家與工業 IoT 段 Q2 +10.3%、上半年 -6.7%，管理層上調 IoT 展望。
  - 來源：GLOBALFOUNDRIES Form 6-K (Q2 2026); MarketBeat Q2 call highlights（as_of 2026-08-05）｜affects：thesis.R、decision_inputs.bear
- `end_markets#6`（end_markets｜方向 -｜狀態 ok）：Counterpoint 純代工市佔表：GF 2026 Q1 約 3%，2024 Q4 為 5%；TSMC 73%。
  - 來源：Counterpoint Research Global Pure Foundry Market Share: Quarterly（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `end_markets#7`（end_markets｜方向 -｜狀態 ok）：IDC 2026 年 2 月預測 2026 智慧手機出貨年減 12.9% 至約 11.2 億支、2027 年 +2%；後續（約 2026 年 6 月，二手報導）修正為 2026 年 -13.9% 至約 10.9 億支、2027 年 -1.1%、2028 年 +5.5%。IDC 預期記憶體晶片價格 2027 年中趨穩。
  - 來源：eeNews Europe / Gigazine (IDC Feb 2026); IT Brief (IDC revision, secondary)（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：FY2023 20-F 載明技術與服務價格隨時間下滑，未推出新技術可能迫使既有技術降價。
  - 來源：SEC GLOBALFOUNDRIES Form 20-F FY2023（as_of 2024-03-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：中國成熟製程晶圓廠持續擴張：Nexchip 28nm 邏輯平台於 2026-03-11 完成開發，Silan、Hua Hong 亦擴產與製程升級（競爭壓力，非替代技術）。
  - 來源：TrendForce News 2026-03-26 Nexchip, Silan and Hua Hong mature node（as_of 2026-03-26）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 營收指引發布後 Chartmill 報導盤前約下跌 5.5%，稱 Q3 營收預測略低於市場預期；Benzinga 則稱營收預測較前次區間 17.4–17.8 億上調，兩來源對「上調或略低」解讀不一
  - 來源：Chartmill: GlobalFoundries Dips After Q3 Revenue Forecast Trails Estimates; Benzinga earnings forecasts（as_of 2026-08-05）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#6`（capital_markets_pricing｜方向 -｜狀態 ok）：Axelrod Research 2026-10-07 筆記評級 HOLD，稱 2026-10-06 收盤 48.63 美元，對比 2026-05-09 的 74.12 美元（該筆記依 5 月營運快照，非新財報修正）
  - 來源：Axelrod Research: GFS the foundry thesis survives（as_of 2026-10-07）｜affects：valuation、decision_inputs.bear
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：TrendForce 報導：12 吋成熟製程擴產約 70% 由中國晶圓廠驅動；SMIC、華虹、晶合（Nexchip）新廠陸續投產，Nexchip 合肥四期 51 億美元擴 28nm。
  - 來源：TrendForce News / Tom's Hardware（搜尋摘要轉述）（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#1`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：TrendForce 2026年4月：成熟製程價格或在2026回升，但庫存過剩與中國同業競爭仍構成壓力。
  - 來源：TrendForce News, Mature node prices may rebound in 2026 but inventory overhang and China competition weigh（as_of 2026-04-03）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2024 營收 67.5 億美元，較 FY2023 的 73.92 億下降 9%（-6.42 億）
  - 來源：GlobalFoundries Reports Fourth Quarter 2024 and Fiscal Year 2024 Financial Results（as_of 2025-02-11）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2024 GAAP 毛利率 24.5%，較 FY2023 的 28.4% 下滑 390bp；非 IFRS 毛利率 25.3% vs 29.1%（搜尋摘要之轉述，未取得逐字原文）
  - 來源：GlobalFoundries Q4/FY2024 earnings release (6-K)（as_of 2025-02-11）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2024 年季度調整後毛利率：Q2 25.2%（年減 440bp）、Q3 24.7%、Q4 25.4%；去庫存壓力來自客戶庫存偏高，Q2 營收年減 12%
  - 來源：Benzinga: GlobalFoundries Exceeds Q2 Projections, Navigates High Inventory Levels In Chip Market（as_of 2024-08-06）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2024 年 9 月 GFS 股價單月下跌 13.8%，年初至 9 月累計約 -36%，同期 TSMC +73%
  - 來源：Motley Fool: Why GlobalFoundries Stock Fell 14% Last Month（as_of 2024-10-04）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#4`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Q4 2024 另認列 9.35 億美元與 Malta, NY 產能相關減損，毛利率收縮、展望低於市場預期
  - 來源：Benzinga: GlobalFoundries Q4 Earnings: Revenue And EPS Beat, Margins Shrink, Revenue Outlook Disappoints Street（as_of 2025-02-11）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 12 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":117.6,"bear_5y_price":28.8,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":39.3,"ev5y_pct":41.5,"irr_base_pct":6.9,"asym_ratio":3.0,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":1.96,"pe":24.61,"basis":"FY2026E 共識 Non-IFRS EPS 1.96 美元（Koyfin 2026-10-08），現價 48.24 美元÷1.96＝24.6 倍；終端倍數同樣套在當年度 Non-IFRS EPS"},"eps":{"bull":[2.0,2.85,3.9,4.8,5.6],"base":[1.96,2.55,3.25,3.75,4.2],"bear":[1.9,2.05,1.75,2.05,2.4]},"pe":{"bull":21,"base":16,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.498,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GFS_Q1_2026_Earnings_Call_20260505.md
- 2026-05-05｜Sam Franklin (CFO)｜guidance：Q2 營收指引 17.6 億美元 ±2,500 萬（原話："to be $1.76 billion, plus or minus $25 million."）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：Q2 毛利率指引約 28.5%（原話："We expect gross margin to be approximately 28.5%, plus"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：Q2 營業利益率指引 15.7%（±180bp）（原話："operating margin to be in the range of 15.7%"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：下半年季度營業費用維持與 Q2 指引相近水準（原話："operating expense run rate in the second half of 2026"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：CID 全年成長由約 30% 上調至高 30%（原話："achieve high 30s percent year-over-year revenue growth"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：車用 2026 年營收低雙位數成長（原話："deliver low double-digit growth in 2026"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：智慧行動裝置 2026 年預期高個位數衰退，略優於智慧手機大盤（原話："slightly outperform the overall smartphone market"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：IoT 2026 年預期為成長年（Q1 下滑屬出貨時點、Q2 回補）（原話："we continue to expect 2026 to be a growth year for"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：技術服務佔 2026 年營收比重趨近原 10–12% 區間高端（原話："comprise a greater proportion of our total 2026 revenue"）
- 2026-05-05｜Timothy Breen (CEO)｜guidance：矽光子 2026 年營收約翻倍（原話："roughly double our silicon photonics revenue in '26"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：全年淨資本支出佔營收 15–20% 維持不變（原話："CapEx to be in the range of 15% to 20% of revenue."）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：2026 全年調整後自由現金流率約 10%，下半年偏重（原話："adjusted free cash flow margin of approximately 10%"）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：MIPS 2026 年營收貢獻 6,000 萬至 1 億美元區間維持（原話："That range still holds."）
- 2026-05-05｜Sam Franklin (CFO)｜guidance：MIPS 預訂趨勢高於區間中點（未含 Synopsys ARC）（原話："trending towards above the midpoint of"）
- 2026-05-05｜Timothy Breen (CEO)｜guidance：短期定價部位將調價，預期落在 2026 下半年尾端並延續至 2027（原話："price adjustments on that part of the portfolio."）
- 2026-05-05｜Sam Franklin (CFO)｜commitment：承諾 2026 年底毛利率達 30% 以上（原話："still to exit 2026 at or above a 30% gross margin."）
- 2026-05-05｜Timothy Breen (CEO)｜commitment：矽光子營收運行率目標：2028 年底超過 10 億美元（原話："photonics revenue run rate exiting 2028."）
- 2026-05-05｜Sam Franklin (CFO)｜margin：Q1 毛利率創第一季紀錄，年增逾 500bp（原話："our gross margin achieved a first quarter record"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：管理層稱 Q1 毛利率年增的最大來源為產品組合（原話："driver there was mix and mix falls into 2 categories."）
- 2026-05-05｜Sam Franklin (CFO)｜margin：Q1 毛利率優於指引中點 200bp 中，約 1 點來自 AMF 成本綜效（原話："about 1 point of that came through cost synergies that"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：中東衝突相關氣體與化學品備貨成本，預期每季約影響 0.5 點毛利率（原話："has about 0.5 point of margin impact for each quarter"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：Q1 自由現金流受有利營運資金變動推升，管理層預期 Q2 回轉（原話："favorable working capital movements in the first quarter"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：Q1 非智慧行動裝置終端市場加技術服務佔比創歷史高點約 2/3（原話："that came in at the highest level"）
- 2026-05-05｜Sam Franklin (CFO)｜margin：定價以對毛利結構的貢獻衡量，而非單看 ASP；舊閒置費用已大致結束（原話："That is largely in the rearview mirror."）
- 2026-05-05｜Timothy Breen (CEO)｜capital_allocation：針對吃緊產能談客戶預付款，搭配資本支出加速（原話："advanced payments to secure capacity"）
- 2026-05-05｜Sam Franklin (CFO)｜capital_allocation：下一波產能投資預期伴隨客戶預付款與政府補助（原話："capacity investments will be accompanied by customer"）
- 2026-05-05｜Sam Franklin (CFO)｜capital_allocation：Q1 回購 4 億美元，授權額度剩約 1 億美元（原話："we repurchased $400 million of our shares"）
- 2026-05-05｜Timothy Breen (CEO)｜capital_allocation：資本支出主要加裝工具於既有廠區，並有政府支持（原話："the ROI is very strong because we're adding tools"）
- 2026-05-05｜Sam Franklin (CFO)｜capital_allocation：下半年加碼 R&D 方案（原話："We are ramping R&D programs in the second half of 2026 to"）
- 2026-05-05｜Timothy Breen (CEO)｜competition：被問 CID 成長是否落後同業，答稱各子市場未見流失、多處有份額增加（原話："we don't see share loss. In fact, we see share gain"）
- 2026-05-05｜Timothy Breen (CEO)｜competition：矽光子設計導入前四大可插拔光模組廠中的三家（原話："GF is now designed in at 3 of the top 4 pluggable optical"）
- 2026-05-05｜Sam Franklin (CFO)｜competition：管理層稱此前定價環境較 2025 更具建設性（原話："GF is now designed in at 3 of the top 4 pluggable"）
- 2026-05-05｜Timothy Breen (CEO)｜product：SCALE 稱為業界首個符合 OCI MSA 的平台（原話："the industry's first OCI MSA capable platform"）
- 2026-05-05｜Timothy Breen (CEO)｜product：共封裝光學仍視為 2028 年的故事（原話："co-packaged optics is a 2028 story."）
- 2026-05-05｜Timothy Breen (CEO)｜product：SiGe 於 Vermont 廠產能超額認購至 2027（原話："the industry's first OCI MSA capable platform"）
- 2026-05-05｜Timothy Breen (CEO)｜customer：Q1 設計案較去年同期增加 50%（原話："co-packaged optics is a 2028 story."）
- 2026-05-05｜Timothy Breen (CEO)｜customer：Renesas 多十億美元策略合作（原話："announced a multibillion-dollar strategic partnership"）
- 2026-05-05｜Timothy Breen (CEO)｜customer：Apple 與 Cirrus Logic 合作將新製程帶至 Malta 廠（原話："bring new process technologies to our Malta, New York fab."）
- 2026-05-05｜Timothy Breen (CEO)｜customer：在地化帶動客戶接洽與設計案增加（原話："a meaningful increase in customer engagements"）
- 2026-05-05｜Sam Franklin (CFO)｜risk：中東衝突影響供應鏈，已提前備貨關鍵氣體與化學品（原話："how the conflict in the Middle East impacts supply chain"）
- 2026-05-05｜Sam Franklin (CFO)｜product：營收類別更名：晶圓營收改稱製造服務（原話："revenue previously referred to as wafer revenue"）

### GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md
- 2026-03-10｜Michael Hogan｜guidance：矽光子營收 2025 年翻倍、2026 年再近乎翻倍（原話："revenue doubled in 2025 is set to nearly double again in"）
- 2026-03-10｜Michael Hogan｜guidance：矽光子 2028 年底年化營收達 10 億美元以上（原話："a clear line of sight to a $1 billion-plus run rate"）
- 2026-03-10｜Michael Hogan｜commitment：10 億美元年化目標有實際營收客戶支撐、稱產能超額認購（原話："is actually supported by real revenue customers"）
- 2026-03-10｜Michael Hogan｜margin：目標營收口徑：2028 年約 1/3 來自 CPO，其餘為可插拔（原話："we model about maybe 1/3 of that"）
- 2026-03-10｜Michael Hogan｜guidance：CPO 若較慢，目標不變、改出更多可插拔（原話："We'll just ship more pluggables as CPO catches up."）
- 2026-03-10｜Michael Hogan｜risk：管理層承認 CPO 放量時程可能較晚（原話："if CPO takes a little longer, we still stick by that"）
- 2026-03-10｜Michael Hogan｜guidance：2030 年 GF 通訊基建與資料中心可服務市場約 110 億美元（原話："than doubles to approximately $11 billion."）
- 2026-03-10｜Michael Hogan｜guidance：光網路 SAM 同期放大逾五倍（原話："the optical networking SAM more than quintuples"）
- 2026-03-10｜Michael Hogan｜guidance：光網路 SAM 至 2030 年約 40% CAGR（原話："optical networking SAM will grow something like 40% CAGR"）
- 2026-03-10｜Michael Hogan｜competition：自稱矽光子代工最大業者（原話："we think we're the largest player in silicon photonics"）
- 2026-03-10｜Michael Hogan｜competition：併入 AMF 後自稱市佔第一，現今 SAM 約 10 億美元（原話："we're the #1 guy in the market"）
- 2026-03-10｜Michael Hogan｜commitment：預期市佔將持續提高（原話："our share will actually continue to grow"）
- 2026-03-10｜Kevin Soukup｜customer：前五大可插拔收發器廠中四家與 GF 合作（原話："4 out of 5 of the top pluggable transceiver players are"）
- 2026-03-10｜Gregg Bartlett｜competition：對 TSMC COUPE 的回應：主張開放生態、雙向相容（原話："We are very much in support of an open ecosystem."）
- 2026-03-10｜Michael Hogan｜capital_allocation：在既有無塵室空間內擴產，由美國與新加坡政府夥伴支持（原話："GlobalFoundries is scaling within existing clean room space"）
- 2026-03-10｜Michael Hogan｜capital_allocation：矽光子每增加一美元資本支出的營收效率提高（原話："revenue per dollar of incremental CapEx is meaningfully"）
- 2026-03-10｜Gregg Bartlett｜capital_allocation：Malta 矽光子與先進封裝廠預期提供整合流程至良品光模組（原話："expected to deliver a fully integrated silicon"）
- 2026-03-10｜Kevin Soukup｜capital_allocation：AMF 併購預期帶來營收與成本綜效（原話："we expect to unlock further revenue and cost"）
- 2026-03-10｜Michael Hogan｜product：銅線於每通道 200G 以上面臨根本挑戰（原話："Using copper becomes fundamentally challenged"）
- 2026-03-10｜Michael Hogan｜product：光互連使 XPU 使用率由十幾趴升至 80% 以上（原話："from as low as mid-teens to north of 80%"）
- 2026-03-10｜Gregg Bartlett｜product：晶圓對晶圓鍵合可縮小 RF 開關晶粒面積（原話："reduce the effective die size by as much as 45%."）
- 2026-03-10｜Michael Hogan｜guidance：前述 10 億美元目標由 2030 年提前至 2028 年底前年化（原話："we pulled in the expectation of sort of $1 billion-plus"）
- 2026-03-10｜Michael Hogan｜customer：稱 10 億美元年化目標已有客戶爭搶產能（原話："this is an oversubscribed corridor, right?"）
- 2026-03-10｜Gregg Bartlett｜product：非光學先進封裝各線暫無個別 TAM（原話："here's what the TAM is going to be for each of these."）
- 2026-03-10｜Gregg Bartlett｜product：各非光學封裝應用成長不及 CPO 光模組（原話："None of these are likely to grow at the rate that"）
- 2026-03-10｜Michael Hogan｜risk：管理層明說暫不提供先進封裝 TAM（原話："we're not ready to put a particular TAM on that"）
- 2026-03-10｜Eric Chow｜commitment：將於 2026 年 5 月 7 日在紐約舉辦投資人日（原話："we will be hosting an Investor Day on Thursday, May 7"）
- 2026-03-10｜Eric Chow｜guidance：近期營運問題延後到 Q1 財報後再答（原話："We will be happy to address near-term questions"）

### GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md
- 2026-05-07｜Sam Franklin (CFO)｜guidance：CI&D 市場長期成長目標 30% 以上（原話："we feel very comfortable with the target of 30-plus percent"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2025 CI&D 營收年增 29%（原話："We delivered 29% year-over-year revenue growth"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：車用目標：低雙位數成長（原話："our target to deliver low double-digit percentage growth"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：IoT 目標：中段十幾%成長（原話："we believe that a target growth rate of mid-teens"）
- 2026-05-07｜Michael Hogan｜guidance：智慧手機（SMD）預期大致持平（原話："we'll probably look to stay relatively flat in SMD"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：矽光子營收目標：2028 年底年化 10 億美元（原話："$1 billion run rate by the exit of 2028"）
- 2026-05-07｜Gregg Bartlett｜guidance：矽光子 2030 營收可達 20 億美元（原話："we can actually achieve $2 billion in revenue by 2030"）
- 2026-05-07｜Gregg Bartlett｜guidance：電源業務 2030 前增量營收 10 億美元（原話："targeting an incremental $1 billion of revenue in our power"）
- 2026-05-07｜Gregg Bartlett｜guidance：MIPS／客製矽業務 2030 年化營收 10 億美元（原話："we see an opportunity to achieve a $1 billion run rate"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2026 年底毛利率目標約 30%（原話："with a 30% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底毛利率目標 40%（原話："we expect to achieve a 40% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期毛利率目標 45%（原話："a line of sight to a 45% gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底營業利益率約 25%（原話："delivering approximately 25% operating margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期營業利益率約 35%（原話："support an operating margin of approximately 35% longer term"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2028 年底 EPS 約 4 美元、長期 6 美元（原話："approximately $4 of EPS exiting 2028, and $6 of longer-term"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：自由現金流率目標約 10%（原話："to target approximately 10% free cash margin"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：2026 年資本支出占營收 15% 至 20%（原話："We're targeting about 15% to 20%"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：長期資本支出強度約 20%，且為淨額目標（原話："we think of that as a net target"）
- 2026-05-07｜Sam Franklin (CFO)｜guidance：技術服務占比 2026 全年預期靠近 12%（原話："we're going to be closer to that 12% end of the"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：毛利率 40% 橋接：組合貢獻 5 至 6 點（原話："6 points of margin opportunity over the next 3 years"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：製造成本與每層光罩現金成本改善貢獻 1 至 2 點（原話："can deliver 1 to 2 points of margin growth as well"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：折舊上升在未來幾年約構成一點左右的逆風（原話："probably is a point or so of headwind"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：模型未預設大幅漲價，毛利改善來自組合（原話："price increases just associated with supply and demand"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：毛利率與營業利益率差距維持約 15 點，2028 後才縮至 10 點（原話："that sort of 15-point delta to the gross margin"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：OpEx 成長速度約為營收 CAGR 的一半（原話："we expect our OpEx to grow at roughly half the"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：2026 Q1 毛利率年增 510 bps（原話："gross margin, up 510 basis points year-over-year"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：不按終端市場拆毛利，因產線設備可互換（原話："we don't break out the gross margin by end market"）
- 2026-05-07｜Sam Franklin (CFO)｜margin：上市以來毛利率擴張超過 1,000 bps（原話："over 1,000 basis points of margin expansion"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：宣布首次季度現金股息（原話："initiation of a quarterly cash dividend of $0.12 per share"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：資本配置框架：回饋最多 50% 投資後自由現金流（原話："returning up to 50% of free cash flow after investments"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：預期可回收 30% 至 50% 的合格支出（原話："recover anywhere between 30% and 50% of eligible spending"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：第四筆併購預計未來幾個月內完成（原話："We have a fourth, which we expect to close in the next"）
- 2026-05-07｜Sam Franklin (CFO)｜commitment：10 億美元軟體與服務目標已含 ARC（原話："That's included."）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：最近五年資本支出強度約 22%，略高於前一版模型（原話："marginally higher than the prior model we shared"）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：未來自由現金流預期維持 10% 以上區間（原話："over the next 5 years in the 10-plus percent range"）
- 2026-05-07｜Timothy Breen (CEO)｜capital_allocation：美國將占成長投資的大宗（原話："that will be the lion's share of our growth investments"）
- 2026-05-07｜Sam Franklin (CFO)｜capital_allocation：正式併購 ARC IP 業務（原話："we're seeking to acquire the ARC IP business"）
- 2026-05-07｜Gregg Bartlett｜product：SCALE 為業界首個支援 OCI 的方案（原話："solution is the industry's first OCI capable solution"）
- 2026-05-07｜Gregg Bartlett｜product：CPO 材料級放量預期 2028 開始（原話："material volume in co-packaged optics will start"）
- 2026-05-07｜Gregg Bartlett｜product：CPO 顯著放量時點預估 2028 下半年（原話："probably the second half of '28"）
- 2026-05-07｜Sam Franklin (CFO)｜product：2028 前矽光子成長主要來自可插拔（原話："principally pluggables revenue growth focused"）
- 2026-05-07｜Michael Hogan｜product：車用毫米波雷達：FDX 靈敏度較 bulk CMOS 高 75%（原話："FDX is 75% more sensitive than the same solution"）
- 2026-05-07｜Gregg Bartlett｜product：量子運算目前為 NRE 型業務（原話："This is an NRE business for the foreseeable future"）
- 2026-05-07｜Sam Franklin (CFO)｜product：新增營收分類：製造服務與技術服務（原話："manufacturing services and revenue from technology services"）
- 2026-05-07｜Gregg Bartlett｜competition：可插拔光學方案低插入損耗光纖貼合（原話："We have a very elegant solution that has the lowest loss"）
- 2026-05-07｜Timothy Breen (CEO)｜competition：CEO 對 CPO 地位：預期為前二（原話："GF will be one of the top 2."）
- 2026-05-07｜Timothy Breen (CEO)｜competition：管理層預期車用小幅取得市占（原話："net-net, probably will gain a little bit of share"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：2025 設計案 500 件，95% 為單一來源（原話："95% of those wins were awarded to GF on a sole-source"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：2025 年再在岸化帶來 30 億美元設計案（原話："We had $3 billion of design wins in 2025 alone"）
- 2026-05-07｜Michael Hogan｜customer：車用營收由期初 1 億美元增至期中 14 億美元（原話："$100 million at the beginning of the decade, $1.4"）
- 2026-05-07｜Michael Hogan｜customer：IoT 優於市場主要來自市占提升（原話："I think it's mostly share gain."）
- 2026-05-07｜Timothy Breen (CEO)｜customer：與現代汽車集團簽署合作（原話："we announced a partnership with Hyundai Motor Group"）
- 2026-05-07｜Timothy Breen (CEO)｜customer：CSP 預計計畫後段轉向更直接參與（原話："the latter part of the plan into more direct work"）
- 2026-05-07｜Sam Franklin (CFO)｜risk：高效能 SiGe 產能超額認購至 2027 上半年（原話："seeing oversubscription in high-performance SiGe"）
- 2026-05-07｜Sam Franklin (CFO)｜risk：手機市場成長受限，管理層不倚賴其成長（原話："no longer reliant on the growth of smart mobile devices"）
- 2026-05-07｜Timothy Breen (CEO)｜risk：全球一半關鍵半導體產能在中國與台灣（原話："50% of essential semiconductor capacity"）

### GFS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：CEO says company is in a supply-chasing phase; capex rising this year and again next year, gated by tool install/qualification.（原話："We are clearly in a chasing supply moment today."）
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：Capex increases this year vs last and further next year; pace depends on tool readiness.（原話："We'll be increasing further again next year"）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Next year's growth is gated by supply (tool installation/qualification), not demand.（原話："We don't see a demand-based reason"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Customers co-invest financially alongside GF in some capacity ramps.（原話："they're also co-investing alongside us"）
- 2026-09-08｜Timothy Breen (CEO)｜product：Silicon photonics customer count.（原話："We have more than 40 customers in photonics today"）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：States ability to scale photonics capacity 10x inside existing US and Singapore fabs.（原話："10x our photonic capacity within our existing 4-wall"）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：On the $1B (2028) / $2B (2030) photonics targets, says industry adoption needed is already in place.（原話："the industry adoption needed to reach those targets"）
- 2026-09-08｜Timothy Breen (CEO)｜risk：Photonics demand exceeds supply from current installed base; mentions balancing capacity lead against long-term profitability.（原話："much more demand than we can supply"）
- 2026-09-08｜Timothy Breen (CEO)｜product：Pluggables alone reach the first photonics milestone; co-packaged optics would be upside beyond targets.（原話："Pluggables gets you pretty much all the way there."）
- 2026-09-08｜Timothy Breen (CEO)｜competition：Notes former copper proponents have entered optical, so participants in optical have broadened.（原話："everyone who was touting copper 2 years ago"）
- 2026-09-08｜Timothy Breen (CEO)｜product：GaN products already shipping to data center; BCD 55nm in new conversion stages.（原話："We're shipping GaN products to the data center today."）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Power/BCD pull-through to business not yet seen; expected in 2027 and more in 2028, with capacity added then.（原話："We have yet to see the real pull-through for the business"）
- 2026-09-08｜Timothy Breen (CEO)｜margin：Mobile share of revenue defined: from >50% to mid-30s, long-term model mid-20s.（原話："that's down to the mid-30s today"）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：Medium-term plan does not depend on mobile growth.（原話："we do not rely on it growing to achieve our medium-term plan"）
- 2026-09-08｜Timothy Breen (CEO)｜risk：Describes mobile as a tough year, especially at the low end; GF more exposed to higher-end handsets.（原話："It is indeed a tough year."）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Mobile customers are asking to secure 2027 and 2028 supply even if units are down low double digits.（原話："I need my supply for '27, I need my supply for '28"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Automotive share of revenue went from 2% five years ago to the 20s today.（原話："We were, sort of 5 years ago, 2%. It's now in the 20s."）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Auto double-digit growth expected to continue this year, next year and beyond, driven by content not units.（原話："will continue this year, next year and beyond"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：GM cited as having secured capacity itself with GF as part of NCNT/US-for-US sourcing push in auto.（原話："securing that capacity themselves as GM did with us"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Reshoring: NCNT now the rule in procurement, whereas footprint was previously not a differentiator.（原話："NCNT is the rule, not a nice-to-have, right?"）
- 2026-09-08｜Timothy Breen (CEO)｜product：Physical AI described as early stage, not yet materially hitting the business.（原話："We haven't seen that really materially hit the business yet."）
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：About six acquisitions in two years; IP acquisitions (MIPS, RISC-V, Synopsys ARC) framed by customer reaction test.（原話："We've done about 6 acquisitions in the last 2 years."）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：IP/software/custom silicon revenue stated at $100–120M this year with $1B exit run-rate target by end of decade.（原話："between $100 million and $120 million of revenue this year"）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：Expresses confidence in the $1B end-of-decade IP run-rate.（原話："very confident for that end of decade kind of $1 billion"）
- 2026-09-08｜Timothy Breen (CEO)｜margin：Describes IP acquisitions as accretive revenue with very good margins.（原話："accretive revenue, very good margins, very good growth"）
- 2026-09-08｜Timothy Breen (CEO)｜competition：Claims position as second-largest processor IP supplier after the incumbent.（原話："probably the second largest processor IP supplier"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Synopsys ARC acquisition brought a 300-customer base GF is now engaging.（原話："it came with 300 customers"）
- 2026-09-08｜Timothy Breen (CEO)｜customer：Names Lockheed Martin (defense) as an IP-related engagement.（原話："we had an announcement with Lockheed Martin about that"）
- 2026-09-08｜Timothy Breen (CEO)｜product：Quantum: bottleneck framed as high-volume manufacturing.（原話："the bottleneck is not quantum science, it's high-volume manufacturing"）
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：US government quantum deal completed; accelerates investment in tooling and infrastructure.（原話："we completed the deal that we announced earlier in the year"）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Comm infrastructure/data center end-market running 60% in Q2 vs long-term target in the 30s; auto in line, IoT slightly ahead.（原話："We're doing 60% in Q2."）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：Says no demand constraint to meeting and exceeding the long-term plan.（原話："I don't see a demand constraint to meeting and exceeding"）
- 2026-09-08｜Timothy Breen (CEO)｜guidance：Next couple of years described as supply-constrained rather than demand-constrained, barring environment changes.（原話："supply-constrained, not demand-constrained"）
- 2026-09-08｜Timothy Breen (CEO)｜capital_allocation：Government partnerships provide capex acceleration tools with significant recovery rates.（原話："accelerate CapEx at significant recovery rates"）
- 2026-09-08｜Timothy Breen (CEO)｜commitment：Says diversification gives confidence; long-term plan numbers may look conservative.（原話："may even make those numbers look a bit conservative"）

### 問答異常語氣（迴避／改口／保留）
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Harlan Sur 問年底毛利率是否可接近 33–35%｜答法：未回應該區間，改談年增表現、營收增量對應毛利增量，並重申年底 30% 以上目標
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Vivek Arya 問 CID 成長相對同業 50–100% 是否在流失份額｜答法：未給份額數字，以三大子市場分述並稱未見流失
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Vivek Arya 問年初與現在的定價假設及每片營收持續下滑｜答法：未給定價數字，改談混合與毛利貢獻，稱以毛利結構為重
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Krish Sankar 問 SCALE 與 TSMC COUPE／Tower 的比較與製程節點｜答法：未給節點或規格比較，延後至 Investor Day
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Ross Seymore 問 2Q 各終端市場與子類別方向性指引｜答法：僅給年增方向與 IoT 回補，未給各市場 Q2 數字
- GFS_Q1_2026_Earnings_Call_20260505.md｜問：Ross Seymore 問智慧行動裝置相對大盤的長期差距｜答法：未回答，延後至 Investor Day，僅談新形態裝置的順風
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Bryson：競爭對手稱握有逾 80% 矽光子市佔、營收與 GF 相近，如何解釋落差｜答法：Hogan 回「You can talk to the Tower about what they think」，未回應落差，改談自身十年投資與三大支柱
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Garrigan：目前與 3 至 5 年後的市佔為何｜答法：未給市佔百分比，只講自身為第一、SAM 約 10 億美元、預期市佔續升
- GFS_Shareholder_Analyst_Call_GLOBALFOUNDRIES_Inc_20260310.md｜問：Hosseini：光學以外先進封裝機會與 TAM 數字｜答法：Bartlett 與 Hogan 皆明說暫不給 TAM，改談產品組合與「stay tuned」
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Ted Kang（Craig Group）請按事業別拆分 2030 毛利率，並問何以營業利益率槓桿不如毛利率｜答法：管理層明確不拆毛利率（理由為產線設備可互換），改以組合與成本層次回覆；營業利益率差距以技術服務 R&D 密集解釋。
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Charles Shi（Needham）請拆分毛利率改善中組合與效率占比，以及基礎晶圓代工毛利目標與補貼貢獻｜答法：CFO 給組合 5 至 6 點、成本 1 至 2 點等區間，但未提供基礎晶圓代工的毛利目標，也未量化補貼對毛利的貢獻。
- GFS_Analyst_Investor_Day_GLOBALFOUNDRIES_Inc_20260507.md｜問：Matt Bryson（Wedbush）問 1 百萬量子位元系統的含量或 TAM，及 IonQ 收購 SkyWater 的影響｜答法：Gregg 未給含量或 TAM 數字，改說之後有網路研討會，對 IonQ 事件僅說不評論；Tim 補充當日市場在找數字。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 4 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 8 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 3 |
| geo_supply_chain | found | 5 | 4 |
| end_markets | found | 9 | 6 |
| substitute_technology | found | 5 | 4 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 7 | 4 |
| major_events | found | 1 | 4 |
| cyclical_supply_discipline_capacity | found | 5 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 6 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：GlobalFoundries largest customer second-source OR in-house 2026；GlobalFoundries single-source risk customer diversify supplier Qualcomm Apple AMD 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260710","verdict":"觀望","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"成熟製程週期復甦真實，稼動率與 Non-IFRS GM 結構性回升","columns":{"2Y 驗證點":"FY26-27 Non-IFRS GM 達 30%+、稼動率近 90%","5Y 驗證點":"through-cycle GM 站穩 28-32%（vs 谷底 22%）","10Y 驗證點":"長期 GM 目標 40% 可達性","具體數字門檻":"Non-IFRS GM 30%+（Q1'26 29%、Q2 guide 28.5%）；稼動率 8 吋 80%→90%","信息來源":"公司 4Q25/1Q26 法說、TrendForce 成熟製程漲價報告","漂移觸發條件":"連 2 季 TTM GM &lt; 27% 或稼動率回落 → 削弱（TTM 季節性過濾）"}},{"id":"H2","text":"特殊製程第二曲線（車用/矽光子/功率）成長引擎兌現","columns":{"2Y 驗證點":"矽光子 2026 翻倍、車用 +low-double、Comms/DC +25%+","5Y 驗證點":"矽光子 $1B run-rate（2028）、功率 $1B 增量軌道（2030）","10Y 驗證點":"特殊製程營收占比由 ~30% 升向 50%+","具體數字門檻":"矽光子 FY26 +100%（$200M→$400M+）；車用 FY25 $1.4B +17%","信息來源":"公司 Investor Day 2026、SiPh Cisco/Sivers 合作、AMF 收購","漂移觸發條件":"矽光子連 2 季 &lt; +50% 或車用 &lt; +8% → 削弱"}},{"id":"H3","text":"ROIC 隨稼動率回升結構性改善、資本效率提升","columns":{"2Y 驗證點":"FY26-27 ROIC 由 ~7% 升向 9-10%（周轉率改善）","5Y 驗證點":"ROIC 持續站上 WACC（~9-10%）","10Y 驗證點":"through-cycle ROIC &gt; WACC 的複利可維持性","具體數字門檻":"投入資本周轉率由 0.52x 升；Capex/Rev 控制在 ≤12%","信息來源":"yfinance 三表自算、公司 capex 指引","漂移觸發條件":"FY26-28 連 3 年 ROIC &lt; 9% → 結構性低 ROIC 確認、H3 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"成熟製程循環二次反轉：中國新產能（Nexchip/CanSemi）壓低 ASP + 車用/工業庫存二次修正 → 稼動率回落、GM 壓回","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度稼動率、wafer 出貨 YoY、同業 UMC/VIS/SMIC 成熟製程價量","警戒閾值":"連 2 季稼動率 &lt; 80% 且 GM YoY 下滑 &gt; 3pp"}},{"id":"R2","text":"客戶集中 + 中國本地化侵蝕：前二大客戶占晶圓收入 ~30.3%（2025 20-F）；China-for-China 車用授權策略稀釋自身產能訂單；2028 Qualcomm LTA 重議","columns":{"對應假設":"H1+H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"客戶 IR、中國本土代工拿單、LTA 續約條件、全球代工市佔","警戒閾值":"市佔跌破 3.0%，或任一大客戶轉單 &gt; 30% 訂單，或 LTA 重議量縮"}},{"id":"R3","text":"ROIC 結構性低於 WACC：capital-intensive foundry 投入資本周轉率長期壓 ROIC → 多年複利價值毀滅","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"年度 ROIC、Capex/Rev、投入資本周轉率、同業資本效率","警戒閾值":"FY26-28 連 3 年 ROIC &lt; 9%（WACC 之下）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(FY+2) 回落至 ≤22x（約 $55-58）；或連 2 季 Non-IFRS GM ≥30% 且 SiPh 全年翻倍兌現；Section 232 Phase 2 若對進口類比/RF/功率 IC 課稅為額外上行催化","irr_base_pct":6.3,"ev5y_pct":31.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"衛星","signal":"B","val":"🟠","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.3,"ev5y_pct":31.0,"irr_base_pct":6.3,"max_dd_pct":-60.0,"bull_5y_price":143.0,"bear_5y_price":43.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE(FY+2) 回落至 ≤22x（約 $55-58）；或連 2 季 Non-IFRS GM ≥30% 且 SiPh 全年翻倍兌現；Section 232 Phase 2 若對進口類比/RF/功率 IC 課稅為額外上行催化","price_at_dd":69.71,"archetype":"循環/商品","cycle_position":"早循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GFS","date":"2026-10-12","schema":"v15.0","contract":"v19","company_name":"GLOBALFOUNDRIES Inc."},"oneliner":"成熟與特殊製程代工，資料中心光學（矽光子＋SiGe）帶動毛利率一年拉升近 5 點；股價三個月跌三成、FY2027E 本益比 18 倍，但扣回股權報酬約 22 倍，現價押的是 2027 漲價與組合讓毛利率站穩 30% 以上。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GFS_20261012/scenario.json","answers":{"q1_business":{"verdict":"賺晶片設計商外包製造的錢：約 89% 是按晶圓計價的製造服務，11% 是 IP 與工程服務。利潤卡在 SiGe、矽光子、FDX、BCD 這類特殊製程的產能與認證，不在先進製程。","reasoning":"Q2 2026 營收 17.86 億美元（季增 9%、年增 6%），Non-IFRS 營益率 16.7%、GAAP 營益率 9.7%，Non-IFRS 毛利率 29.9%（年增 4.7 點）；Q3 營收指引 18.85 億美元，毛利率約 30.5%。收錢方式：製造服務約 89%（按晶圓計價，Q2 出貨約 62.5 萬片 12 吋約當，年增 8%），技術服務約 11%（IP、授權、光罩、工程服務，毛利率顯著高於公司平均）。終端市場（Q2 占比／年增）：智慧行動約 36%／−6%，車用約 19%／−10%，家用與工業 IoT 約 19%／+10%，通訊基建與資料中心約 16%／+62%。錢卡在特殊製程平台的產能與認證：SiGe 超額認購至 2027，矽光子供不應求，2027 起多條技術線的漲價入帳。這些都不在先進製程，所以 TTM 營益率 11.6% 約為台積電 56.1% 的五分之一。單點依賴：上游 SOI 晶圓約 71% 來自單一供應商（二手摘要，未核申報原文），這是集中度風險，不是護城河；下游兩大客戶 FY2024 各占 16%、11%，前十大約占出貨三分之二（2021），未見單一客戶超過四成。產業時鐘在擴張期：8 吋稼動率由 2025 年約 80% 升向 2026 年近 90%，2026 Q1→Q2 成熟製程報價漲 5–15%，GF 自身稼動率在高 80% 區，仍有約 10 點空間。","fact_refs":["f_kpi0_gaap","f_kpi1_non_ifrs","f_kpi2_gaap","f_kpi6_q3_2026","f_earnings_recency"],"verdict_values":{"revenue_quality":"中：晶圓長約與單一來源設計案提供能見度，但手機占約 36% 且全年年減十幾 %；2027 漲價已談定，尚未入帳","unit_econ_note":"每片晶圓營收由組合驅動；CFO 稱 Q2 營收年增約 1 億美元，調整後毛利也增約 1 億美元，增量幾乎全數落到毛利","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"FY2024 GAAP 淨利為負、屬晶圓代工、2026 淨資本支出占營收 15–20%，三項命中商品型特徵；但營收不由商品報價驅動，另有資料中心光學的長期成長段"},"industry":{"clock_phase":"II","sd_verdict_source":"供需以週期性為主，帶結構性成分。台積電與三星削減 8 吋、8 吋產能負成長至 2027 上半年，屬結構性（TrendForce 2026-06-30、IDC 2026-03-30）；但 12 吋成熟擴產約七成來自中國，供給可逆性高，2027 下半年起轉鬆的風險實在。","bargaining":{"up":"上游：SOI 晶圓約 71% 來自單一供應商（二手摘要指為 Soitec，2025 年，未核申報原文），部分氣體與稀土亦為單一來源；GF 對上游議價弱","down":"下游：兩大匿名客戶 FY2024 各占 16%、11%，前十大約占出貨三分之二（2021）；特殊製程設計案 95% 單一來源，2027 漲價已與客戶談定，下游議價屬拉鋸","geo":"製造在美國（Malta、Vermont）、德國、新加坡；在地採購成為客戶規則是順風，美中緊張與關稅是風險"},"profit_pool_dir":"代工利潤池往先進製程與 AI 集中（台積電純代工份額 73%、營益率 56%）；GF 只在光學互連、SiGe、電源等利基分到增量","tam_table":[{"item":"GF 通訊基建與資料中心可服務市場（公司估）","value":"2030 年約 110 億美元（2026-03-10 分析師會，管理層說法）"},{"item":"光網路可服務市場年化成長（公司估）","value":"至 2030 年約 40%"},{"item":"矽光子代工現今可服務市場（公司估）","value":"約 10 億美元；GF 自稱第一，Tower 自稱逾 80%，管理層未回應落差"},{"item":"GF 矽光子營收目標","value":"2028 年底年化 10 億美元、2030 年 20 億美元"},{"item":"純晶圓代工份額（Counterpoint）","value":"2024Q4 約 5% → 2025 年 4% → 2026Q1 約 3%；產業年增 30% 主要由 AI 先進製程帶動"},{"item":"營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平（→），等級 C。特殊製程設計案多為單一來源、光學與 SiGe 產能供不應求，這些是真的；但利潤率長期低於同為成熟製程的聯電，純代工份額也由 5% 降到 3%，不足以標擴大。","reasoning":"機制是特殊製程平台的設計導入與多年認證所形成的轉換成本，再加上美國在地可信賴代工資格。方向證據：2025 年 500 件設計案中 95% 為單一來源（2026-05-07 投資人日 CEO）；2026 Q1 設計案年增 50%；Q2 新增 7 件光網路設計案；矽光子客戶逾 40 家（2026-09-08 CEO）。但利潤率對照同業顯示定價力有限：GF 的 TTM 毛利率 27.1%、營益率 11.6%、FCF 利潤率 11.5%，聯電分別為 30.6%、20.1%、23.6%，台積電營益率 56.1%。同業 ROIC 未收，改以營益率差代替，GF 對聯電落後約 8.5 點。份額方面，Counterpoint 純代工份額 2024Q4 約 5% → 2026Q1 約 3%，主因是 AI 先進製程把產業規模拉高 30%，但這仍是有來源的份額下降，所以趨勢不標擴大。評分：執行力 7（Q2 營收與毛利率高於指引上緣，提前達成 30% 毛利率）；定價力 5（2027 漲價已談定，但 2022–25 缺貨高峰年度毛利率也不超過 28.4%）。當期報酬屬低利益率×低周轉：TTM 營益率 11.6%，稅率十幾 %，稅後營業利益約占營收 10%；投入資本事實表未涵蓋。","fact_refs":["f_peer_gfs_gross_margin_pct","f_peer_gfs_operating_margin_pct","f_peer_gfs_fcf_margin_pct","f_peer_2330_tw_operating_margin_pct","f_peer_2303_tw_gross_margin_pct","f_peer_2303_tw_operating_margin_pct","f_peer_2303_tw_fcf_margin_pct","f_peer_intc_operating_margin_pct","f_peer_005930_ks_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"特殊製程平台（SiGe、矽光子、FDX、BCD、RF-SOI）的設計導入與多年認證轉換成本，加上美國在地可信賴代工資格","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：2025 年設計案 95% 單一來源，2026 Q1 設計案年增 50%，Q2 新增 7 件光網路設計案，矽光子客戶逾 40 家。定價力穩定：2027 漲價已談定，但 2022 缺貨高峰年度毛利率也只有 27.6%，TTM 27.1% 仍低於聯電 30.6%。Counterpoint 份額下降雖有 AI 分母效應，仍是有來源的下滑，不能標擴大。","competitor_notes":[{"name":"台積電（2330.TW）","strategy_note":"TTM 營益率 56% 對 GF 11.6%；正在縮減 8 吋與部分 12 吋成熟產能，短期把訂單讓給對手，但在矽光子以 COUPE 平台正面競爭"},{"name":"聯電（2303.TW）","strategy_note":"最可比的成熟製程同業，毛利率 30.6%、營益率 20.1%、FCF 利潤率 23.6%，全面高於 GF；分析師預期 2026 下半年與 2027 各漲價 5–10%"},{"name":"Intel（INTC）","strategy_note":"營益率 7.6%、研發密度 23%，代工業務仍在爬坡，對 GF 的美國可信賴代工定位是潛在對手，但尚未形成份額威脅"},{"name":"三星（005930.KS）","strategy_note":"獲利主要由記憶體撐起；代工端與台積電一起削減 8 吋，對 GF 的成熟製程是供給面利多"},{"name":"Tower","strategy_note":"矽光子直接對手，自稱逾 80% 矽光子份額、營收與 GF 相近，GF 管理層 2026-03-10 未回應落差；GF 已向 ITC 提出專利侵權申訴，尚無裁決"},{"name":"中國代工（中芯、華虹、晶合）","strategy_note":"12 吋成熟擴產約七成來自中國，晶合 28nm 平台 2026-03 完成並擴廠，是 2027 後價格壓力的主要來源"}],"peer_na_reason":"同業 ROIC 事實表未涵蓋，改以營業利益率與 FCF 利潤率比較","threats":[{"level":"🔴","text":"中國成熟製程擴產壓價：12 吋擴產約七成來自中國，晶合 28nm 完成，華虹無錫月增約 3 萬片；公司 20-F 自承技術價格除極度缺貨期外會隨時間下跌","p":35,"evidence_refs":["supply_demand_durability#2","cyclical_supply_discipline_capacity#0","substitute_technology#3","substitute_technology#1","cyclical_inventory_price_position#1"]},{"level":"🟡","text":"矽光子點對點競爭：台積電 COUPE、Tower 擴產，客戶可多源；GF 純代工整體份額 5% → 3%","p":30,"evidence_refs":["competitive_share_entrants#0","end_markets#6"]},{"level":"🟡","text":"上游 SOI 晶圓約 71% 集中單一供應商（二手摘要），替換需時甚長","p":15,"evidence_refs":["geo_supply_chain#0"]}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是光模組與 XPU 系統，決策者是收發器廠與超大規模業者，付款者是晶片設計商，三者方向一致。銅線在每通道 200G 以上受限（2026-03-10 管理層），客戶要求鎖定 2027–28 產能，SiGe 超額認購至 2027。手機段需求是因記憶體漲價而延後，不是消失。"},{"item":"決策層級","level":"🟡","text":"設計導入以製程平台為單位，2025 年設計案 95% 單一來源，車用重新認證週期長；但矽光子客戶可多源。CEO 被問多源可行性時沒有給數據，只說客戶分散（逾 40 家）。資料缺口：客戶是否已替同一顆晶片建立第二代工來源，本輪兩次查證都沒找到第三方或申報資料。95% 單一來源是公司自述的設計案統計，只說明 GF 拿單時多為獨家，不證明客戶換廠的成本高。對判斷的處理：轉換成本只算到設計導入這一層，不當作下行保護，這是護城河維持 C、方向不標擴大的理由之一。熊市機率 30% 由成熟製程週期與中國擴產推得，原本就沒有因客戶綁定而調低，所以不另外上調。客戶轉向多源的風險已列在矽光子競爭威脅（機率 30%），追蹤兩條門檻：通訊基建與資料中心年增連 2 季低於 30%，前五大收發器客戶合作家數降到 3 家以下。若後續查到主要客戶已雙源量產，護城河方向與熊市機率重新評估。"},{"item":"價值鏈分配","level":"🟡","text":"光學鏈的錢主要落在 XPU 與光模組設計端；GF 即使在 2022 缺貨高峰，年度毛利率也只有 27.6%，TTM 27.1% 低於聯電 30.6%。上游 SOI 晶圓約 71% 集中單一供應商，下游兩大客戶各占 16%、11%；2027 漲價已被客戶接受，是改善跡象。"},{"item":"社會容忍度","level":"🟡","text":"美國在地產能是政策順風（矽光子 3 億美元意向書、量子 3.75 億美元補助、可信賴代工資格）。但這部分優勢依賴補助與在地採購規則，屬政策風險；晶片漲價未見社會反彈，Section 232 目前未涉及其業務。"}],"roiic":"事實表未涵蓋（投入資本、折舊未收）","reinvest_rate":"事實表未涵蓋；再投資強度：2026 淨資本支出約占營收 15–20%（CFO 稱偏高端），2025 年為 8%","endo_ceiling":null,"formula_note":"內生成長＝增量 ROIC × 再投資率。稅後營業利益約占營收 10%（TTM 營益率 11.6% 扣十幾 % 稅），淨資本支出約為其 1.5–2 倍；折舊未收，無法算淨再投資率。上界推演（假設值，非事實）：增量 ROIC 取 15%、再投資率取 100%，內生成長上限約 15%，低於共識三年 EPS 年化約 31%，差額要靠毛利率擴張補。資料缺口：投入資本、折舊、增量 ROIC 事實表都未涵蓋，內生上界不填正式值。判斷不拿這個假設值支撐估值；基準情境 FY2028 EPS 取 3.25 美元，低於共識 3.56 美元，這個差距就是對毛利率擴張打的折扣。"}}}},"q3_growth":{"verdict":"五年後跑道中等（🟡）。資料中心光學與技術服務是有來源的第二曲線，但合計占營收不到三成；共識三年 EPS 年化約 31%，大半靠毛利率由 30% 往 40% 擴張，而非再投資。","reasoning":"成長拆解：以量（Q2 晶圓出貨年增 8%）＋組合（資料中心光學與技術服務毛利率較高）為主；價格 2027 才入帳；併購（MIPS＋ARC）貢獻技術服務增量 1.0–1.2 億美元，約占 2026 營收 1.5%；回購在 Q1 4 億美元後，授權只剩約 1 億美元。共識 EPS：FY2026E 1.96、FY2027E 2.63、FY2028E 3.56（Koyfin 2026-10-08，近 3 個月 FY1 上修 3.2%）。以 FY2025A GAAP 稀釋 EPS 1.59 為基期，年化約 30.8%（口徑不一致，會高估）；以 FY2026E 起算，兩年年化約 34.8%。同期營收：2026 全年推估約 74 億美元（Q1 由 Q2 季增 9% 回推，Q4 依 CFO 認可的約一成季增推估），較 2025 年 67.9 億增約 9%。缺口：共識約 31% 減內生上界約 15%（假設值），約 16 點，歸因毛利率擴張。管理層的橋接是 2026 約 30% → 2028 年底 40%：組合 5–6 點、成本 1–2 點、折舊約 −1 點（2026-05-07 投資人日）。這可以歸因，不屬於依賴重新評價；但它是管理層目標，不是已實現。跑道：CEO 稱 2030 年資料中心光鏈約七成光學化，GF 估 2030 年通訊基建與資料中心可服務市場約 110 億美元、矽光子 2030 目標 20 億美元；滲透率數據事實表未涵蓋，跑道年數無法計算。衰退訊號亮 2 個：核心市占縮減、EPS 成長遠快於營收。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi6_q3_2026"],"verdict_values":{"growth":{"driver_mix":"量＋組合為主，價格 2027 起入帳；併購約占 2026 營收 1.5%；淨回購可忽略","runway_years":"事實表未涵蓋（無滲透率資料）","runway_post_y5":"🟡","endo_ceiling_basis":"共識三年 EPS 年化約 31%（FY2025A GAAP 1.59 → FY2028E 3.56，口徑不一致）；內生上界在寬鬆假設下約 15%；缺口歸因毛利率擴張（管理層 30% → 40% 橋接）","segments":[{"item":"智慧行動裝置","value":"Q2 占營收約 36%，年減 6%；全年預期年減十幾 %（5 月原預期高個位數衰退）"},{"item":"車用","value":"約 19%，Q2 年減 10%（客戶出貨時點）；全年維持低雙位數成長，偏重 Q4"},{"item":"家用與工業 IoT","value":"約 19%，年增 10%；全年上修至 10–15%（原中個位數）"},{"item":"通訊基建與資料中心","value":"約 16%，年增 62%；全年上修至 50–60%（原高 30%）；SiGe 規模大於矽光子"},{"item":"技術服務","value":"約 11%，全年趨近 10–12% 區間高端，毛利率顯著高於公司平均"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q1 年增逾 5 點，Q2 年增 4.7 點"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"Counterpoint 純代工份額 2025 年約 4% → 2026Q1 約 3%"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"漲價 2027 才入帳，尚無數據"},{"signal":"EPS 成長顯著高於營收成長（差 >5 點）","lit":true,"evidence":"共識三年 EPS 年化約 31%，2026 營收年增約 9%"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":false,"evidence":"FY2025 約 1.14；2026 資本支出翻倍後有轉弱風險"},{"signal":"SBC／營收 >5% 且逐年上升","lit":false,"evidence":"Q2 約 4.8%，Q3 指引約 4%；逐年序列事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"手機出貨 2026 年減約 14%，屬記憶體漲價造成的週期性下修，非替代"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"evidence":"事實表未涵蓋"},{"signal":"維護性資本支出占 FCF >60%","lit":null,"evidence":"事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"2026 資本支出加倍，德勒斯登擴產"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：股數四年大致持平，也開始配息；但 2026 資本支出翻倍到營收 15–20% 高端，ARC 併購的增量營收只夠抵銷新增研發，Q1 回購 4 億美元的買入收益率偏低。","reasoning":"現金流：Q2 營業現金流 4.05 億美元，淨資本支出（扣政府補助）4.08 億美元，約占營收 23%，調整後 FCF −300 萬美元。CFO 維持 2026 全年調整後 FCF 利潤率約 10%，資本支出偏 15–20% 高端；CEO 稱 2027 再增。FCF／淨利：FY2025 約 1.14（10.09÷8.85 億美元）；FY2024 淨利為負，不適用；FY2023 約 0.31。股權報酬：Q2 占 GAAP 營業利益 49.4%，約營收 4.8%；Q3 指引約 0.76 億美元（約營收 4%）。2026 年迄今現金去向：資本支出、Q1 回購 4 億美元、ARC 併購 4.55 億美元（含現金 4.4 億）、7 月起季配 0.12 美元（年化約 2.7 億美元）。資產負債：現金與有價證券約 33 億美元，負債 11 億美元，10 億美元循環額度未動用。三項計分：併購已實現報酬未過，回購收益率未過，股數淨稀釋過。資本回饋框架是最多回饋 50% 投資後 FCF。","fact_refs":["f_kpi3","f_kpi4_non_ifrs","f_kpi5_sbc_gaap","f_peer_gfs_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"ARC 對價 4.55 億美元（含現金 4.4 億，2026-06 完成）；MIPS＋ARC 使 2026 技術服務增量由 0.6–1.0 億上修到 1.0–1.2 億美元。CFO 稱增量營收大致只抵銷新增研發，已實現增量營業利益接近零，報酬低於資金成本"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q1 回購 4 億美元，均價事實表未涵蓋。以 FY1 前瞻 24.6 倍推，買入收益率約 4%；以 Trailing 37.7 倍推，約 2.7%。門檻是 10 年期殖利率＋2 點；10 年期殖利率事實表未涵蓋，只要高於約 2.1%，門檻就高於 4%，判未過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數（淨利÷稀釋 EPS 推算）：FY2022 約 5.53 億、FY2023 約 5.57 億、FY2025 約 5.57 億，2026 Q2–Q3 約 5.56 億；四年淨變動不到 +1%，但要靠 Q1 4 億美元回購抵銷每季約 0.8 億美元股權報酬"}]},"governance":{"capital_returns":{"expanded":false,"reason":"併購貢獻 2026 營收約 1.0–1.2 億美元，占全年推估營收不到 2%；成長主體是晶圓量與組合，不靠併購撐"}}}},"q5_valuation":{"verdict":"現價要求 FY2028 Non-IFRS EPS 約 3.5 美元兌現，毛利率 2027 起續升。我只部分相信：資料中心光學與漲價有來源，但 40% 毛利率仍是管理層目標，基準年化約 7–8%，價格合理，不便宜。","reasoning":"現價 48.24 美元：FY2026E 24.6 倍，FY2027E 18.3 倍（48.24÷2.63），FY2028E 13.6 倍（÷3.56）。Trailing 37.7 倍是三個年度端點中最高；P/S 3.88 倍、EV/S 3.78 倍分別落在四個年度端點的 72.5 與 62.2 分位（非五年連續分位，五年分位事實表未涵蓋）。PEG：FY1 前瞻 24.6 倍 ÷ 三年 EPS 年化約 30.8，約 0.80；但這段成長來自毛利率而非量，分母又含股權報酬，不能當便宜依據。分母爭點：Q2 股權報酬約占 GAAP 營業利益 49%。以 Q3 指引約 0.76 億美元年化、5.56 億股計，每股稅前約 0.55 美元、稅後約 0.47 美元；扣回後 FY2027E 約 2.16 美元，本益比約 22 倍。短期（12 個月）：FY2027E 基準 2.55 美元 × 20 倍＝51 美元，+5.7%。中期（3 年）：FY2028E 基準 3.25 × 18 倍＝58.5 美元，+21.3%。賣方 21 位平均目標價 80.24 美元（高 125、低 60，全距約 2.1 倍），高於現價 66%，方向較樂觀；但各聚合站快照不一（Benzinga 平均 63），不作依據。共識近 3 個月 FY1 上修 3.2%，FY2、FY3 微幅上修，股價卻自 5 月 74 美元跌三成以上，屬投資人日後的倍數回吐，不是盈餘下修。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_dividend_yield_ttm","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"FY2027E 共識前瞻本益比為主，PEG 對照；循環股輔以自身倍數區間","tier":"成熟／特殊製程代工","peers":{"expanded":false,"reason":"事實表同業對照只收毛利率、營益率、FCF 利潤率、研發密度，未涵蓋同業倍數，無法展開；終端倍數改以自身前瞻倍數與成長熄火情境錨定"},"fwd_pe":24.61,"peg":0.8,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2027E 共識 18.3 倍已低於前份 22 倍重啟線，PEG 約 0.8。但扣回股權報酬後約 22 倍，Trailing 37.7 倍在自身年度端點最高，P/S 3.88 倍在年度端點 72.5 分位；情境基準年化約 7–8%，期望值為正但不寬，循環位置在中段。故判合理（🟡），而非便宜","upside_short_pct":5.7,"upside_mid_pct":21.3,"denominator_disputed":true,"denominator_note":"共識 EPS 推定為 Non-IFRS，排除股權報酬；Q2 股權報酬約占 GAAP 營業利益 49%，GAAP 營益率 9.7% 對 Non-IFRS 16.7%。以 Q3 指引約 0.76 億美元年化、5.56 億股計，每股稅前約 0.55 美元；扣回後 FY2027E 本益比由 18 倍升到約 22 倍，以 18 倍論證便宜不成立"}}},"q6_how_wrong":{"verdict":"最可能看錯在把週期高點的毛利率當成結構水準：2027–28 中國 12 吋成熟產能放量、手機持續疲弱時，資料中心光學這塊不到兩成的營收，撐不住整體稼動率。","reasoning":"看錯的三條路已寫進反證紀錄。一、2027–28 二次下行：2024 年營收 −9%、毛利率 −390bp、Malta 減損 9.35 億美元，是前例。二、成長兌現，卻被資本支出與股權報酬吃掉。三、30% 毛利率已高於 2022–25 任一年度，可能是週期高點而非新底。價值陷阱評估亮兩燈（核心份額縮減、EPS 遠快於營收），給 🟡。回撤參照：2024 年初至 9 月 −36%；2026-05 至 10 月約 −34%，期間共識未下修。","fact_refs":["f_price_at_dd","f_kpi1_non_ifrs","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"兩項衰退訊號亮燈：核心份額縮減、EPS 成長遠快於營收"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":1.96,"pe":24.61,"basis":"FY2026E 共識 Non-IFRS EPS 1.96 美元（Koyfin 2026-10-08），現價 48.24 美元÷1.96＝24.6 倍；終端倍數同樣套在當年度 Non-IFRS EPS"},"eps":{"bull":[2.0,2.85,3.9,4.8,5.6],"base":[1.96,2.55,3.25,3.75,4.2],"bear":[1.9,2.05,1.75,2.05,2.4]},"pe":{"bull":21,"base":16,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-60,"hi":-45,"basis":"歷史實例：2024 年循環下行，年初至 9 月 −36%（同期台積電 +73%）；2026-05 至 10 月由 74 美元跌到 48 美元，約 −34%，期間共識未下修。本次若疊加成熟製程二次下行（2024 年度毛利率年減約 4 點的前例）與資本支出高峰，自現價再跌 45–60%（約 19–27 美元）屬合理區間；觸發時點以 2027 下半年漲價效應消退後為主","trigger_time":null},"basis":{"bull":"資料中心光學維持 30% 以上成長，2027–28 漲價與組合把毛利率推到 2028 年底 40%；FY2030 EPS 5.6 美元，接近管理層長期 6 美元。配 21 倍，為自身 FY1 前瞻 24.6 倍略打折；同業前瞻倍數事實表未涵蓋","base":"FY2026–27 貼近共識（1.96／2.55）；FY2028 取 3.25，低於共識 3.56，反映毛利率 2028 年到 36–37% 而非 40%；之後年增約 12–15%，FY2030 4.2 美元。終端 16 倍，對應循環中段的成熟代工","bear":"2027 下半年起成熟製程二次下行（中國 12 吋擴產＋消費電子去庫存），FY2028 EPS 回到 1.75 美元，FY2030 2.4 美元。12 倍介於成長熄火降至 10%（約 14 倍）與 5%（約 11 倍）之間。機率 30%：共識三年成長超過內生上界，2024 下行才剛發生，中國 12 吋擴產集中在 2026–27"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2024 年下行實例：營收 −9%，年度毛利率由 28.4% 降到 24.5%，季度調整後毛利率低到 24.7%；Q4 認列 Malta 減損 9.35 億美元，股價年初至 9 月 −36%。本輪中國 12 吋成熟擴產約占七成，晶合擴廠 51 億美元。","assumption":"資料中心光學（約 16%）與技術服務（約 11%）的成長，抵得過其餘約七成營收的週期下行","consequence":"FY2028 EPS 回到 1.75 美元左右，倍數 11–12 倍，股價落在 20 美元區（−55～−60%）","ruling":"部分採納：熊市機率給 30%，最大回撤給 −45～−60%。不全盤採納，因為台積電與三星正在削減 8 吋與部分 12 吋成熟產能，GF 2027 漲價已談定，SiGe 與矽光子供不應求","watch":"公司稼動率（Q2 高 80% 區）、季度 Non-IFRS 毛利率、聯電報價、中國新廠投產時程","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","cyclical_prior_downcycle_behavior#4","supply_demand_durability#2","cyclical_supply_discipline_capacity#0"],"fact_refs":["f_kpi1_non_ifrs"]},{"view":"論點失敗","evidence":"Tower 自稱逾 80% 矽光子份額、營收與 GF 相近，GF 管理層 2026-03-10 未回應落差；台積電推 COUPE；CEO 2026-08-05 承認對手積極進入矽光子","assumption":"GF 是矽光子最大代工，2028 年底年化 10 億美元目標可達","consequence":"矽光子目標延後，通訊基建與資料中心成長回落到 20% 以下，多頭情境失效","ruling":"暫不可裁決：雙方說法都沒有第三方份額數據可驗，ITC 專利案也尚無裁決；以通訊基建與資料中心年增 30% 作驗證門檻","watch":"通訊基建與資料中心季度年增、前五大收發器客戶合作家數、ITC 裁決","evidence_refs":["competitive_share_entrants#0","end_markets#6"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"光學成長兌現，但 2026 淨資本支出升至營收 20% 高端，Q2 調整後 FCF −300 萬美元；ARC 4.55 億美元併購的增量營收只夠抵銷研發；Q2 股權報酬約占 GAAP 營業利益 49%","assumption":"管理層所稱 FCF 利潤率約 10%，與回饋 50% 投資後 FCF，能同時成立","consequence":"每股 FCF 不隨營收成長，GAAP EPS 長期落後 Non-IFRS 約 0.5 美元","ruling":"採納：估值分母以扣回股權報酬後的 FY2027E 約 22 倍看待，不用 18 倍當便宜論證","watch":"調整後 FCF 利潤率、股權報酬占營收、稀釋股數","evidence_refs":[],"fact_refs":["f_kpi3","f_kpi4_non_ifrs","f_kpi5_sbc_gaap"]},{"view":"價格已反映太多","evidence":"Trailing 本益比 37.7 倍在自身年度端點最高；FY2028E 共識 3.56 美元已約為管理層 2028 年底 4 美元年化目標的 89%；Q3 營收指引公布後盤前跌約 5.5%（一說低於預期，一說較前次區間上調）","assumption":"市場已把 40% 毛利率路徑算進共識，現價只剩情境中位數的報酬","consequence":"即使論點兌現，基準年化也只有約 7–8%","ruling":"部分採納：價格已不貴（FY2027E 18 倍，扣回股權報酬約 22 倍），但也不便宜。從 5 月 74 美元跌到 48 美元，主要是投資人日後的倍數回吐，共識 EPS 同期上修 3.2%；價格沒有反映太多，也沒有給足安全邊際","watch":"Q3 財報後 FY2027E 共識是否下修，以及股價對應的 FY2027E 倍數","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#6"],"fact_refs":["f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 69.71 → 本次 48.24（-30.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=69.71","side_b":"本次 price_at_dd=48.24","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 -→❌。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷","cause":null,"prior_field":null,"side_a":"公司：通訊基建與資料中心 2026 年增 50–60%，SiGe 超額認購至 2027，CEO 稱未來兩年受供給限制","side_b":"第三方：TrendForce 估 8 吋稼動率近 90%、8 吋產能負成長至 2027 上半年；UBS 認為成熟製程進入上行週期","ruling":"兩側一致：資料中心光學與 8 吋成熟製程 2026–27 供給偏緊，這是本輪判斷的共同底","evidence_level":"公司揭露＋產業研究機構","settle_metric":"公司稼動率、通訊基建與資料中心年增","if_then":[],"evidence_refs":[]},{"axis":"估值與期望報酬重算：估值隨股價變動，期望報酬兼受情境樹重建影響","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 69.71 美元，估值結論偏貴（🟠），基準年化 6.3%，五年期望值 +31%，不對稱比 2.3，裁決觀望","side_b":"本次：股價 48.24 美元（−31%），同期 FY1 共識 EPS 上修 3.2%，FY2027E 本益比 18.3 倍，估值結論改為合理（🟡）。期望報酬與不對稱比的變動有兩個來源，方向相反。起點價下跌把它們往上推，屬價格變動。情境樹重建把多頭五年價由 143 美元降到約 118 美元、空頭由 43 美元降到約 29 美元，把它們往下拉，屬方法變動（見「情境樹重建」條）。新數值由程式依新情境重算","ruling":"拆開歸因。估值結論由偏貴改為合理，幾乎全來自價格下跌，共識並未下修。不對稱比、五年期望值、基準年化是價格與方法共同變動，拆量見「期望報酬拆解：情境樹重建」與「期望報酬拆解：股價下跌」兩條。Q3 營收指引的市場解讀分歧（盤前跌約 5.5%）。裁決不會只因價格下跌就轉為進場，要看毛利率路徑的證據","evidence_level":"價格與共識快照＋方法調整","settle_metric":"FY2027E 共識與 2026 Q3 毛利率","if_then":["若 2026 Q3 毛利率 ≥30% 且 Q4 指引 ≥31% → 重跑判斷後進場首倉 1.5%","若股價先漲回 60 美元以上而毛利率證據未到 → 不追","若股價續跌但毛利率路徑無損 → 分批反買，不視為停損訊號"],"evidence_refs":["capital_markets_pricing#6","capital_markets_pricing#1"]},{"axis":"期望報酬拆解：情境樹重建（股價固定在前份 69.71 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份情境、股價 69.71 美元：五年期望值 +31%，基準年化 6.3%，不對稱比 2.3","side_b":"本次情境、股價仍用 69.71 美元：五年期望值 −2.1%，基準年化 −0.7%，不對稱比 1.0","ruling":"先換情境、股價不動：多頭與空頭五年價同時下修，五年期望值少 33 個百分點，基準年化少 7.0 個百分點，不對稱比由 2.3 降到 1.0。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"FY2027E 共識與 2026 Q3 毛利率","if_then":[],"evidence_refs":[]},{"axis":"期望報酬拆解：股價下跌（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 69.71 美元：五年期望值 −2.1%，基準年化 −0.7%，不對稱比 1.0","side_b":"本次情境、股價 48.24 美元：五年期望值 +41.5%，基準年化 6.9%，不對稱比 3.0","ruling":"再換股價、情境不動：起點價跌 31%，五年期望值多 43.6 個百分點，基準年化多 7.6 個百分點，不對稱比由 1.0 升到 3.0。期望報酬比前份好，全部來自股價下跌，情境本身比前份差。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"FY2027E 共識與 2026 Q3 毛利率","if_then":[],"evidence_refs":[]},{"axis":"情境樹重建","cause":"方法變動","prior_field":["bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭五年價 143 美元，空頭 43 美元，機率多頭 25／空頭 30，最大回撤 −60%","side_b":"本次：重建 EPS 路徑。基準貼近共識 FY2026–27，FY2028 取 3.25（低於共識 3.56）；多頭 FY2030 5.6 美元 × 21 倍，約 118 美元；空頭 2.4 美元 × 12 倍，約 29 美元；機率維持 25／45／30；最大回撤區間 −45～−60%","ruling":"多頭價下修，是因不再把管理層長期 6 美元 EPS 配成長股倍數；空頭價下修，是納入中國 12 吋擴產與資本支出翻倍後的下行深度。機率不變，因新證據正反抵銷","evidence_level":"方法調整","settle_metric":"2027 全年 Non-IFRS 毛利率","if_then":["若 2027 全年毛利率 ≥34% → 多頭機率上調至 30%","若 2027 上半年毛利率年減 → 熊市機率上調至 35%"],"evidence_refs":[]},{"axis":"循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"前份：早循環","side_b":"本次：中循環。Q2 Non-IFRS 毛利率 29.9% 創同季紀錄，Q3 指引 30.5%，稼動率高 80% 區，2027 漲價已談定，CEO 2026-09-08 稱處於追供給階段。商品型六訊號分歧：量增領先（出貨年增 8%）、賣方目標高於股價，偏買；毛利率高於自身年度區間上緣、存貨備抵由 0.9 億增至 1.4 億美元，偏賣；供給紀律分歧；市淨率事實表未涵蓋。反面：2026 全年營收推估約 74 億美元，仍低於 2022 年 81 億美元","ruling":"裁中循環。訊號分歧時不硬給進場姿態，對應持有不加；循環判讀只套約七成的週期性營收，資料中心光學段另計，不隨循環賣","evidence_level":"公司揭露＋產業研究機構","settle_metric":"公司稼動率與季度毛利率","if_then":["若稼動率升到 90% 以上且 2027 漲價入帳 → 改判晚循環，停止任何新建立","若稼動率連 2 季回落到 80% 以下 → 改判下行，等深谷訊號再評估進場"],"evidence_refs":["cyclical_inventory_price_position#1"]},{"axis":"綜合訊號與品質判斷維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份：綜合訊號 B；價值陷阱 🟡；護城河方向持平；五年後跑道中等；循環/商品","side_b":"本次維持。正面新證據：設計案年增 50%、矽光子客戶逾 40 家、通訊基建與資料中心上修到 50–60%、2027 漲價已談定；負面新證據：Counterpoint 純代工份額 5% → 3%、手機全年年減十幾 %","ruling":"正反證據相抵，方向與等級不變。護城河不升為擴大，因有來源的份額下降；也不降，因設計案與客戶數擴大，漲價被客戶接受","evidence_level":"公司揭露＋產業研究機構","settle_metric":"通訊基建與資料中心年增、Counterpoint 份額","if_then":["若 Counterpoint 份額連 2 季低於 3.0% 且通訊基建與資料中心年增低於 30% → 護城河方向改判縮減"],"evidence_refs":["competitive_share_entrants#0","end_markets#6","end_markets#2"]},{"axis":"估值重啟條件改寫（進場）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE(FY+2) 回落至 ≤22x（約 $55-58）；或連 2 季 Non-IFRS GM ≥30% 且 SiPh 全年翻倍兌現；Section 232 Phase 2 若對進口類比/RF/功率 IC 課稅為額外上行催化","side_b":"2026 Q3 實績 Non-IFRS 毛利率 ≥30% 且 Q4 指引 ≥31%、通訊基建與資料中心全年年增 50% 以上維持 → 重跑判斷後進場首倉","ruling":"前份的價格條件已在 48.24 美元觸發（FY2027E 18.3 倍 ≤22 倍），毛利率條件尚未觸發（Q2 29.9%，差 0.1 點）。新證據顯示分母含每股稅前約 0.55 美元股權報酬，扣回後約 22 倍，價格條件的便宜判斷不成立。觀望的唯一約束改為毛利率路徑，因此重啟改用事件錨、不設價格線，觸發後重跑判斷再進場首倉","evidence_level":"公司揭露","settle_metric":"2026 Q3 Non-IFRS 毛利率與 Q4 指引","if_then":["若 Q3 毛利率 ≥30% 且 Q4 指引 ≥31% → 重跑判斷後進場首倉 1.5%","若 Q3 毛利率 <29.5% → 維持觀望，重啟條件延到 2027 Q1"],"evidence_refs":[]},{"axis":"清倉與減碼門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics；前份風險門檻為：連 2 季稼動率 <80% 且毛利率年減 >3 點；市佔跌破 3.0% 或任一大客戶轉單 >30%；FY26–28 連 3 年 ROIC <9%","side_b":"本次 kill_metrics 六條：沿用上述稼動率、市佔、ROIC 三條；新增 2027 上半年任一季毛利率 <30%（減碼）、通訊基建與資料中心連 2 季年增 <30%（減碼）、調整後 FCF 利潤率連 2 年 <5%；稼動率與毛利率雙破則清倉","ruling":"新增三條，是因本輪論點改以資料中心光學與毛利率路徑為核心。市佔門檻：Counterpoint 2026Q1 已在 3% 附近，列為警示但不單獨觸發減碼，因分母被 AI 先進製程膨脹（產業年增 30%）。ROIC 門檻沿用，但投入資本事實表未涵蓋，列資料缺口","evidence_level":"方法調整","settle_metric":"各 kill 指標","if_then":["若稼動率連 2 季 <80% 且毛利率年減 >3 點 → 清倉","若 2027 上半年任一季毛利率 <30% → 減碼至半倉以下"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"2027 上半年任一季 Non-IFRS 毛利率低於 30%（漲價已入帳仍無法讓毛利率年增）","ruling":"毛利率是數學上最大的單一敏感度：每 1 點約影響每股 0.11 美元，共識 FY2028 增量幾乎全來自毛利率擴張，故設為 Single Thing；發生時減碼至半倉以下，同季稼動率 <80% 則清倉","evidence_level":"方法調整","settle_metric":"2027 Q1–Q2 Non-IFRS 毛利率","if_then":["若發生 → 減碼至半倉以下並凍結加碼","若 2027 Q1 毛利率年增 ≥3 點 → 加碼至 3%"],"evidence_refs":[]},{"axis":"管理層手機展望改口","cause":null,"prior_field":null,"side_a":"2026-05-05 CFO：智慧行動 2026 高個位數衰退，略優於大盤；2026-05-07 投資人日 Hogan：大致持平","side_b":"2026-08-05 CFO：全年年減十幾 %（記憶體漲價與缺貨）","ruling":"可調和（程度差異）。三個月內兩次下修手機，但同季把通訊基建與資料中心上修到 50–60%、IoT 上修到 10–15%，Q3 營收指引仍高於 Q2；手機下修屬終端需求面，同季仍拿下 MediaTek 首個電源管理晶片設計案，不是份額流失。記入可信度扣分：手機展望已連續下修","evidence_level":"公司法說原話","settle_metric":"智慧行動季度年增","if_then":["若 2026 Q4 智慧行動年減 >15% → 熊市機率上調 5 點"],"evidence_refs":["end_markets#2","supply_demand_durability#5","end_markets#7"]},{"axis":"供需方向：追供給 vs 庫存與中國產能","cause":null,"prior_field":null,"side_a":"2026-09-08 CEO：處於追供給階段，未來兩年受供給限制而非需求；客戶要求鎖定 2027–28 產能","side_b":"TrendForce：2026 下半年電視與筆電提前備貨，有庫存疑慮；消費電子出貨承壓；成熟製程仍受庫存與中國競爭壓力","ruling":"可調和（分段差異）。供給吃緊集中在 SiGe、矽光子與 8 吋；消費性與 12 吋成熟製程（中國擴產區）偏鬆。GF 約 36% 營收在手機，兩邊都碰得到，以公司稼動率作裁決數據","evidence_level":"公司揭露 vs 產業研究機構","settle_metric":"公司稼動率與季度 Non-IFRS 毛利率","if_then":["若稼動率連 2 季 <80% 且毛利率年減 >3 點 → 清倉","若 2027 Q1 稼動率 ≥90% → 維持判斷，不因庫存新聞減碼"],"evidence_refs":["supply_demand_durability#7","cyclical_inventory_price_position#1","cyclical_supply_discipline_capacity#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：中國 12 吋成熟擴產約占七成，晶合 28nm 平台完成並擴廠 51 億美元；Counterpoint 份額 5% → 3%","side_b":"結構轉好：台積電與三星削減 8 吋，台積電 2028 前削減 Fab14 成熟產能 15–20%，8 吋稼動率近 90%，2026 Q1→Q2 報價漲 5–15%。其他結構變數：在地採購成為客戶規則；Section 232 目前未涉 GF；對中國半導體關稅據報 2027-06 生效","ruling":"雙向拉鋸。8 吋與特殊製程結構轉好，12 吋成熟製程競爭惡化，兩者同時成立；GF 同時有 8 吋（Vermont SiGe）與 12 吋產能，惡化軸的時點落在 2027–28","evidence_level":"產業研究機構（TrendForce、IDC、Counterpoint）","settle_metric":"公司每季稼動率與 Non-IFRS 毛利率","if_then":["若 2027 上半年毛利率年增 <1 點 → 認定惡化軸佔上風，熊市機率上調至 35%"],"evidence_refs":["substitute_technology#3","cyclical_supply_discipline_capacity#0","competitive_share_entrants#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：前份重啟價格條件已觸發；FY2027E 18.3 倍，FY2028E 13.6 倍；Q2 營收與毛利率高於指引上緣，通訊基建與資料中心指引由高 30% 上修到 50–60%，2027 漲價已談定；賣方 21 位平均目標價 80 美元；共識 3 個月上修 3.2%，股價卻跌三成","side_b":"再等一季：扣回股權報酬後 FY2027E 約 22 倍；Q2 毛利率 29.9% 已高於 2022–25 任一年度（年度最高 28.4%，口徑略異），循環位置在中段；基準年化約 7–8%；Q3 財報 2026-11 即揭曉毛利率路徑","ruling":"採再等一季：等待成本是一季，錯判成本是買在毛利率高點。但若 Q3 達標，就不再以價格為由拖延","evidence_level":"公司揭露＋共識快照","settle_metric":"2026 Q3 Non-IFRS 毛利率與 Q4 指引","if_then":["若 Q3 毛利率 ≥30% 且 Q4 指引 ≥31% → 重跑判斷後進場首倉 1.5%","若 Q3 毛利率 <29.5% 或通訊基建與資料中心全年指引下修 → 維持觀望，基準 FY2027E 下修至 2.4 美元"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2026 Q3 財報確認毛利率路徑","type":"假設驗證","maps_to":"H2","metric":"季度 Non-IFRS 毛利率與 Q4 指引","threshold":"Q3 ≥30% 且 Q4 指引 ≥31%","action":"達標 → 重跑判斷後進場首倉 1.5%；Q3 <29.5% → 維持觀望，基準 FY2027E 下修至 2.4 美元","source_freq":"季報（每季）","date":"2026-11"},{"n":2,"text":"資料中心光學成長延續","type":"假設驗證","maps_to":"H1","metric":"通訊基建與資料中心營收年增","threshold":"2026 全年 ≥50%；2027 起每季 ≥30%","action":"連 2 季 <30% → 減碼至半倉，多頭機率降到 15%","source_freq":"季報終端市場揭露（每季）","date":"2027-05"},{"n":3,"text":"唯一致命點：漲價入帳後毛利率仍跌破 30%","type":"Single Thing","maps_to":"Single Thing","metric":"2027 上半年季度 Non-IFRS 毛利率","threshold":"任一季 <30%","action":"減碼至半倉以下並凍結加碼；同季稼動率 <80% 則清倉","source_freq":"季報（每季）","date":"2027-08"},{"n":4,"text":"成熟製程二次下行：稼動率與毛利率雙破","type":"風險","maps_to":"R1","metric":"公司稼動率與 Non-IFRS 毛利率年變動","threshold":"稼動率連 2 季 <80% 且毛利率年減 >3 點","action":"清倉","source_freq":"法說稼動率說法＋季報（每季）","date":null,"evidence_refs":["supply_demand_durability#2","cyclical_inventory_price_position#1"]},{"n":5,"text":"車用 Q4 補回失敗","type":"風險","maps_to":"R2","metric":"車用全年營收年增","threshold":"2026 全年 <5%（指引低雙位數）","action":"停止加碼，熊市機率上調 5 點","source_freq":"年度財報","date":"2027-02","evidence_refs":["supply_demand_durability#5"]},{"n":6,"text":"客戶、供應或出口管制出事","type":"風險","maps_to":"R4","metric":"前兩大客戶營收、出口管制處分、SOI 供應","threshold":"任一大客戶營收年減 >30%，或新的出口管制處分，或 SOI 供應中斷","action":"減碼至半倉","source_freq":"年報 20-F（每年）、BIS 公告（不定期）","date":"2027-03","evidence_refs":["customer_concentration_credit#0","geo_supply_chain#0"]},{"n":7,"text":"重啟進場條件","type":"估值rearm","maps_to":"估值重啟","metric":"2026 Q3 毛利率、Q4 指引、通訊基建與資料中心全年展望","threshold":"Q3 ≥30%、Q4 指引 ≥31%、通訊基建與資料中心全年 ≥50% 維持","action":"重跑判斷後進場首倉 1.5%","source_freq":"季報","date":"2026-11"},{"n":8,"text":"價格先走、毛利率未跟上","type":"減碼","maps_to":"H2","metric":"股價對應 FY2028E 共識本益比","threshold":"≥21 倍（約 75 美元）且 2027 毛利率仍 <32%","action":"減碼三分之一","source_freq":"每日股價＋每月共識快照","date":null},{"n":9,"text":"漲價首季入帳確認","type":"加碼","maps_to":"H2","metric":"2027 Q1 Non-IFRS 毛利率年增","threshold":"≥3 點且管理層確認漲價已入帳","action":"加碼至 3%","source_freq":"季報","date":"2027-05"},{"n":10,"text":"年度複審","type":"複審日期","maps_to":null,"metric":"FY2026 年報與 2027 全年展望","threshold":"財報公布","action":"重跑完整判斷","source_freq":"年度","date":"2027-02"}],"kill_metrics":[{"metric":"公司稼動率（法說揭露）","bear_threshold":"連 2 季 <80% 且 Non-IFRS 毛利率年減 >3 點","window":"連 2 季","source":"公司季度法說與新聞稿","last_status":"ok"},{"metric":"季度 Non-IFRS 毛利率","bear_threshold":"2027 上半年任一季 <30%","window":"2027 Q1–Q2","source":"公司季報新聞稿","last_status":"ok"},{"metric":"通訊基建與資料中心營收年增","bear_threshold":"連 2 季 <30%","window":"2027 起每季","source":"公司季報終端市場揭露","last_status":"ok"},{"metric":"全球純晶圓代工份額","bear_threshold":"跌破 3.0%（沿用前份）","window":"連 2 季","source":"Counterpoint Research 純代工份額季報","last_status":"warning"},{"metric":"ROIC（稅後營業利益÷投入資本）","bear_threshold":"FY2026–28 連 3 年 <9%（沿用前份）","window":"年度","source":"年報自算；投入資本事實表未涵蓋，資料缺口","last_status":"unknown"},{"metric":"調整後 FCF 利潤率","bear_threshold":"全年 <5% 連 2 年","window":"年度","source":"公司季報與年報","last_status":"ok"}],"evidence_dismissed":[{"ref":"competitive_share_entrants#5","reason":"Simply Wall St 社群使用者撰寫的敘事，不是公司或研究機構資料，未附任何數據；該則也自承未找到 2026 年針對 GF 的具名新進入者。可查證的部分已由 Counterpoint 份額與 TrendForce 中國擴產兩項機構證據涵蓋"}],"action_conditions":{"rearm_trigger":"2026 Q3 實績 Non-IFRS 毛利率 ≥30% 且 Q4 指引 ≥31%、通訊基建與資料中心全年年增 50% 以上維持 → 重跑判斷後進場首倉","exec_line":"觸發後首倉 1.5%；2027 Q1 漲價入帳、毛利率年增 ≥3 點再加到 3%。股價先跌但毛利率路徑無損，則分批反買，不停損；股價先漲而證據未到，則不追","holding_cap":"3%"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2026 Q3 實績（2026-11）確認 Non-IFRS 毛利率 ≥30% 與 Q4 指引 ≥31%；不設價格線，股價先漲回 60 美元以上而證據未到則不追"},"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-1.02, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"資料中心光學（矽光子＋SiGe）成為第二成長曲線，帶動通訊基建與資料中心段 2026 年增 50–60%，2027 起維持 30% 以上","2y":"2026 全年通訊基建與資料中心年增 ≥50%，矽光子營收翻倍以上；2027 年增 ≥30%","5y":"矽光子 2028 年底年化營收 ≥10 億美元，2030 年約 20 億美元","10y":null,"threshold":"通訊基建與資料中心年增：2026 全年 ≥50%、2027 每季 ≥30%；矽光子 2028 年底年化 ≥10 億美元","source":"季報終端市場揭露；2026-08-05 法說（CFO 上修至 50–60%，CEO 稱矽光子進度可能超前）；2026-05-07 投資人日目標","drift_rule":"2027 起季度年增低於 28.5%（偏離門檻 5%）連 2 季 → 削弱；低於 27%（偏離 10%）連 3 季，或管理層下修 2028 矽光子目標 → 反轉"},{"id":"H2","text":"毛利率結構性抬升：2026 全年約 30%，2028 年底走向 40%（組合轉移＋2027 漲價＋成本改善）","2y":"2027 全年 Non-IFRS 毛利率 ≥32%","5y":"2028 年底季度 Non-IFRS 毛利率 ≥38%（管理層目標 40%）","10y":null,"threshold":"季度 Non-IFRS 毛利率 ≥30% 且年增為正；2027 全年 ≥32%","source":"季報新聞稿；2026-05-07 投資人日毛利率橋接（組合 5–6 點、成本 1–2 點、折舊約 −1 點）；2026-08-05 CFO 稱 2027 起漲價入帳","drift_rule":"TTM 毛利率低於年度門檻 5% 以上（約 1.6 點）連 2 季 → 削弱；低於 10% 以上（約 3.2 點）連 3 季 → 反轉"},{"id":"H3","text":"重押資本支出拿得回報：2026–27 淨資本支出升至營收 20% 上下，同時調整後 FCF 利潤率維持約 10%，營益率 2028 年底走向 25%","2y":"2026、2027 調整後 FCF 利潤率 ≥8%；2027 Non-IFRS 營益率 ≥19%","5y":"2028 年底 Non-IFRS 營益率 ≥22%（目標約 25%）；稀釋股數不高於 5.6 億","10y":null,"threshold":"調整後 FCF 利潤率年度 ≥8%；Non-IFRS 營益率 2027 全年 ≥19%","source":"季報現金流量與營益率；2026-08-05 CFO（全年 FCF 利潤率約 10%，資本支出偏 15–20% 高端）；2026-09-08 CEO 稱 2027 資本支出再增","drift_rule":"5 年期：TTM 營益率偏離軌道 ≥5% 連 4 季 → 削弱，≥10% 連 6 季 → 反轉；FCF 利潤率年度低於 5% → 直接削弱"}],"R":[{"id":"R1","text":"成熟製程二次下行：中國 12 吋成熟擴產約占七成、晶合 28nm 平台完成，加上 2026 下半年消費電子提前備貨與庫存壓力，2027–28 稼動率與報價回落；公司 20-F 自承技術價格除極度缺貨期外會隨時間下跌","h_ref":"H2","clock":"🔥","threshold":"公司稼動率連 2 季 <80% 且 Non-IFRS 毛利率年減 >3 點（沿用前份）；或 2027 漲價入帳後毛利率仍未年增","evidence_refs":["supply_demand_durability#2","supply_demand_durability#3","supply_demand_durability#7","substitute_technology#1","substitute_technology#3","cyclical_supply_discipline_capacity#0","cyclical_inventory_price_position#1","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R2","text":"手機與車用拖累稼動率：智慧行動（約 36%）2026 年減十幾 %，IDC 預期 2027 手機出貨再減 1.1%；車用 Q2 年減 10%，全年低雙位數成長押在 Q4","h_ref":"H2","clock":"⚡","threshold":"車用 2026 全年年增 <5%，或智慧行動 2027 上半年仍年減 >10%","evidence_refs":["supply_demand_durability#5","end_markets#2","end_markets#7"]},{"id":"R3","text":"矽光子份額與定價受攻擊：台積電 COUPE、Tower（自稱逾 80% 矽光子份額）擴產，客戶可多源；GF 純代工整體份額 2024Q4 約 5% → 2026Q1 約 3%","h_ref":"H1","clock":"🔥","threshold":"通訊基建與資料中心年增連 2 季 <30%；或前五大收發器客戶合作家數由 4 家降到 3 家以下；或 Counterpoint 份額跌破 3.0%（沿用前份）","evidence_refs":["competitive_share_entrants#0","end_markets#6"]},{"id":"R4","text":"客戶、供應與地緣集中：兩大客戶 FY2024 各占 16%、11%，前十大約占出貨三分之二；SOI 晶圓約 71% 來自單一供應商（二手摘要）；2021–22 曾向實體清單公司出貨，遭 BIS 處分；與中國的政治貿易緊張列為風險","h_ref":"H1+H2","clock":"🐢","threshold":"任一大客戶營收年減 >30% 或轉單 >30%（沿用前份）；或新的出口管制處分；或 SOI 供應中斷","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","geo_supply_chain#0","geo_supply_chain#1","regulatory_antitrust#2","reg_tariff_export#2"]},{"id":"R5","text":"資本支出翻倍遇上需求轉弱：2026 淨資本支出到營收 15–20% 高端，2027 再增；若需求回落，會形成閒置產能（2024 Q4 Malta 減損 9.35 億美元是前例），ROIC 長期低於資金成本","h_ref":"H3","clock":"🐢","threshold":"FY2026–28 連 3 年 ROIC <9%（沿用前份；投入資本事實表未涵蓋）；或調整後 FCF 利潤率連 2 年 <5%；或再認列產能減損","evidence_refs":["cyclical_prior_downcycle_behavior#4"]}],"single_thing":{"description":"2027 上半年任一季 Non-IFRS 毛利率低於 30%：漲價已入帳，毛利率仍無法年增","why_fatal":"共識 FY2028 EPS 3.56 美元的增量，幾乎全來自毛利率由 30% 往 40% 擴張。毛利率每 1 點約影響每股 0.11 美元（2026 推估營收約 74 億美元 × 1 點 × 稅後 ÷ 5.56 億股）。漲價入帳後仍跌破 30%，代表組合轉移被稼動率下滑抵銷，FY2028 EPS 將落在 2.7 美元以下，熊市情境成立","if_happens":"已持有者減碼至半倉以下並凍結加碼，同季稼動率也低於 80% 則清倉；未持有者撤銷進場計畫","how_monitor":"每季財報 Non-IFRS 毛利率與 CFO 對漲價入帳的說法；同業聯電季度毛利率與報價","probability":"約 20%（12–24 個月）：Q3 指引 30.5%±1 點已站上 30%，2027 漲價已談定；風險在於手機與消費電子若到 2027 上半年仍弱，會拖低稼動率"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.34,"peg_fy2":0.6,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":1.59,"FY2026E":1.96,"FY2027E":2.63,"FY2028E":3.56},"fy_end_month":12,"eps_basis":"共識（Koyfin 2026-10-08 快照）推定為 Non-IFRS 稀釋 EPS，估計家數事實表未涵蓋；FY2025A 1.59 取 yfinance GAAP 稀釋 EPS，FY2025 Non-IFRS 實際值事實表未涵蓋，基期口徑不一致會高估三年年化成長"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026 Q3 財報與 Q4 指引","impact":"高","watch":"毛利率 ≥30%、通訊基建與資料中心全年 50–60% 是否維持、車用 Q4 是否補回"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 財報與 2027 展望","impact":"高","watch":"2027 毛利率展望、漲價幅度、資本支出占營收、FCF 利潤率"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"2027 Q1 財報（漲價首季入帳）","impact":"高","watch":"毛利率年增幅度與稼動率"},{"date":"2027-06","date_precision":"month","type":"regulatory","event":"對中國半導體關稅據報生效（Wedbush 轉述，未核政府原文）","impact":"中","watch":"美國客戶轉向在地代工的訂單變化"},{"date":"2027","date_precision":null,"type":"product","event":"近封裝光學開始放量（CEO 時程）","impact":"中","watch":"SCALE 平台設計案轉量產的件數"},{"date":null,"date_precision":null,"type":"regulatory","event":"ITC 對 Tower 製晶片的專利侵權調查裁決","impact":"中","watch":"排除令是否成立"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
