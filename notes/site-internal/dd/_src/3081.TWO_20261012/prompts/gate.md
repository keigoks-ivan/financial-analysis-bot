你是 DD 管線 v20 的判斷層閘（gate），標的 3081.TWO（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
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

### 判斷檔 `fact_refs` 引到的事實（27 條）
- `f_kpi0`（q1_business）｜營收（合併）＝1221.2 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，法說 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt；優分析法說報導 https://uanalyze.com.tw/articles/6110153300（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，法說 2026-08-12））
  - 註記：查無
- `f_kpi1`（q1_business）｜毛利率＝57.45 %｜期間與口徑：Q2 2026（季末 2026-06-30，法說 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance（毛利 701.6／營收 1221.2）；優分析報導 57%（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，法說 2026-08-12））
  - 註記：查無
- `f_kpi2_gaap_non_gaap`（q1_business）｜營業利益／利益率（GAAP；台股無 Non-GAAP 口徑，兩者同）＝572.6 百萬 TWD（利益率 46.9%）｜期間與口徑：Q2 2026（季末 2026-06-30，法說 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt；優分析報導 營益率約 47%（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，法說 2026-08-12））
  - 註記：查無
- `f_kpi3_eps`（q1_business）｜稅後淨利／EPS＝468.5 百萬 TWD；EPS 約 4.62（法說自結；yfinance 稀釋 4.18，股本口徑不同；另有媒體報 4.31）｜期間與口徑：Q2 2026（季末 2026-06-30，法說 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance；優分析報導 淨利 4.68 億、EPS 4.62，上半年 EPS 7.75（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，法說 2026-08-12））
  - 註記：查無
- `f_kpi6`（q1_business）｜管理層指引＝無數字指引：矽光需求「非常強勁」，未來數季出貨續增；2027 年產能約為 2026 年 2.5 倍；近三季已公告資本支出近 60 億元，今年另有追加支出待董事會核准 定性｜期間與口徑：Q2 2026 法說會（2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：優分析法說報導 https://uanalyze.com.tw/articles/6110153300（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026 法說會（2026-08-12））
  - 註記：未給 Q3／全年營收或 EPS 區間
- `f_kpi7_datacom`（q1_business）｜產品組合（DataCom 占營收）＝80–85%（矽光為最大塊；電信 5–10%，其他約 5%）；1.6T 已量產、3.2T 與客戶開發中 占營收｜期間與口徑：Q2 2026 法說會（2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：優分析法說報導 https://uanalyze.com.tw/articles/6110153300（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026 法說會（2026-08-12））
  - 註記：不適用
- `f_peer_3081_two_gross_margin_pct`（q2_moat）｜3081.TWO 毛利率＝54.53 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3081.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3081_two_operating_margin_pct`（q2_moat）｜3081.TWO 營業利益率＝41.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3081.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2455_tw_gross_margin_pct`（q2_moat）｜2455.TW 毛利率＝37.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2455.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2455_tw_operating_margin_pct`（q2_moat）｜2455.TW 營業利益率＝21.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2455.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_lite_gross_margin_pct`（q2_moat）｜LITE 毛利率＝41.67 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_lite_operating_margin_pct`（q2_moat）｜LITE 營業利益率＝17.79 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi4`（q4_capital）｜自由現金流（營業現金流 − 資本支出）＝-479.3 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，yfinance 季度現金流量表）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（OCF 268.6 百萬、Capex 748.0 百萬）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，yfinance 季度現金流量表））
  - 註記：不適用
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝19.61 TWD/share｜期間與口徑：2026-10-12／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-12）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝39.39 TWD/share｜期間與口徑：2026-10-12／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-12）
- `f_kpi5_sbc`（q4_capital）｜SBC 占營業利益＝1.6 %｜期間與口徑：Q2 2026（SBC 9.06 百萬 ÷ 營業利益 572.6 百萬；占營收 0.7%）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow SBC；自算（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（SBC 9.06 百萬 ÷ 營業利益 572.6 百萬；占營收 0.7%））
  - 註記：不適用
- `f_peer_3081_two_fcf_margin_pct`（q2_moat）｜3081.TWO FCF 利潤率＝-2.46 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3081.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.099 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝3025.0 TWD｜期間與口徑：2026-10-12（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝306.8 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／2 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝84.28 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝83.89 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝43.67 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-12（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝56.08｜期間與口徑：2026-10-12（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-12（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：Quartr 摘要稱 2025 年底三家客戶占應收帳款 74%（為應收集中度，非營收占比）；2025 年銷售市場為中國 71%、美國 21%、台灣 3%。
  - 來源：Quartr, LandMark Optoelectronics (3081) Q4 2025 earnings summary（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：InP 基板供應仍緊；中國出口管制若延續至 8 月後且無新增來源，中長期供應風險仍須關注（聯亞已建庫存）
  - 來源：聯亞(3081)外資報告報導（搜尋摘要）（as_of 2026-08-10）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Marketscreener 頁面於2026-06-11有標題指中國對磷化銦出口管制威脅AI資料中心建置（產業層級，未說明對聯亞影響）
  - 來源：Marketscreener LandMark 頁面（as_of 2026-06-11）｜affects：thesis.R
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：高盛2026年3月報告提示風險：矽光子滲透率可能慢於預期、競爭加劇、IDM自行供應磊晶。
  - 來源：uanalyze/搜尋彙整（高盛報告）（as_of 2026-03-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#2`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：InP基板供應仍緊；外資稱中國出口管制短期不衝擊產出因已有緩衝，但若限制延續至8月後且無新供應來源，中長期供應風險仍須關注
  - 來源：聯亞逆勢大盤而漲停 外資點名這麼說（udn money）（as_of 2026-03-26）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：聯亞上一輪下行（2023–1H24）毛利率低點約8–10%：1H24毛利率10%（前年同期16%），9M24為16%（前年同期8%），Q4 2023約20%
  - 來源：Quartr LandMark Optoelectronics (3081) earnings summaries (Q2 2024／Q3 2024／Q4 2023)（as_of 2024-11-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023年7月營收年減74.2%（消費性需求疲弱、中國基建標案未回溫），分析認為股價有下壓；2023-10-26盤中一度跌7.36%至98.2元
  - 來源：CMoney 投資快訊：聯亞(3081)公告7月營收大幅衰退7成不如預期；聯亞(3081-TW)26日股價報98.2元（as_of 2023-10-26）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023年每股虧損2.31元，主因中國電信客戶幾乎消失、訂單大減、產能利用率低提列閒置損失；2024年8月起股價急漲達3倍
  - 來源：優分析 uanalyze：聯亞(3081)2023年每股虧損2.31元，但Q4毛利率開始優於預期；CPO & 矽光子|聯亞股價大漲（as_of 2024-12-31）｜affects：decision_inputs.bear、thesis.R

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":4140,"bear_5y_price":484,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-53.7,"ev5y_pct":-40.2,"irr_base_pct":-14.3,"asym_ratio":0.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":19.61,"pe":154.3,"basis":"FY2026E 共識 EPS（FY1）；終端倍數同樣乘終端年度 EPS"},"eps":{"bull":[42,56,68,80,92],"base":[37,44,42,46,50],"bear":[32,28,20,18,22]},"pe":{"bull":45,"base":28,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.099,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 3 | 3 |
| supply_demand_durability | found | 6 | 3 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 2 | 4 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 2 | 4 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：3081.TWO LandMark Optoelectronics largest customer second-source OR in-house 2026；聯亞光電 3081 客戶 第二供應商 自製 2026；LandMark Optoelectronics single-source risk customer diversify supplier
- **regulatory_antitrust**（none）：3081.TWO LandMark Optoelectronics antitrust OR monopoly investigation 2026；LandMark Optoelectronics regulation OR regulatory scrutiny 2026；3081.TWO LandMark Optoelectronics DOJ OR FTC OR EU competition 2026
- **channel_business_model_shift**（none）：LandMark Optoelectronics 3081 distribution channel shift 2026；聯亞光電 3081 商業模式 轉型 通路 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3081.TWO","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"聯亞光電"},"oneliner":"賣 InP 磊晶片與 CW 雷射給矽光模組廠，缺貨讓毛利率衝上 57%；現價是 FY2027 共識 EPS 的 76.8 倍，已預支缺貨延續與新產能全數賣光，不追，等報價與估值同時回到合理區。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261012/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 資料中心光模組廠的錢：營收八成以上來自矽光用 CW 雷射與 InP 磊晶片，錢卡在 InP 基板供應與磊晶產能兩個節點；Q2 毛利率 57.45%、營益率 46.9%，是公司史上最高。","reasoning":"Q2 2026 營收 1,221.2 百萬元，毛利率 57.45%，營業利益 572.6 百萬元（營益率 46.9%），稅後淨利 468.5 百萬元；EPS 口徑不一（法說自結約 4.62、yfinance 稀釋 4.18），本份以 yfinance 口徑為準。產品組合：DataCom 占 80–85%（矽光最大），電信 5–10%，其他約 5%；1.6T 已量產、3.2T 與客戶開發中。管理層未給數字財測，只說矽光需求非常強勁、2027 年產能約為 2026 年的 2.5 倍；媒體轉述 Q3 營收季增約 20% 的財測。產業時鐘判在擴張期：7 月營收年增 176.54%、基板與磊晶片 2025Q4 起多次漲價、全產業擴產。供需持久度：週期性將反轉——缺口目前逾三成且業界預期延續到 2027 之後，但同業新產能 2026 至 2028 陸續上線、公司自身 2027 產能 2.5 倍，供給可逆性高。產業態勢判雙向拉鋸：結構轉好軸（InP 雷射缺貨、客戶由 7–8 家增至 10 家以上）對上競爭惡化軸（同業兩度倍增 InP 產線、高盛點名 IDM 自行供應磊晶）。單點依賴：上游 InP 基板（中國出口管制、住友電工五年長約）與下游集中（2025 年底三家客戶占應收帳款 74%、2025 年銷售 71% 在中國）；單一客戶營收占比事實表未涵蓋。","fact_refs":["f_kpi0","f_kpi1","f_kpi2_gaap_non_gaap","f_kpi3_eps","f_kpi6","f_kpi7_datacom"],"verdict_values":{"revenue_quality":"營收 80–85% 來自資料中心矽光產品，2025 年銷售 71% 在中國、21% 在美國；三家客戶占應收帳款 74%，單一客戶營收占比事實表未涵蓋。","unit_econ_note":"Q2 2026 毛利率 57.45%、營益率 46.9%；年度財報序列顯示 2023 年毛利率 13.08%、營益率 −26.53%，利潤率高度隨產能利用率與報價擺動。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"近四個年度有兩年虧損（2023、2024），毛利率由 13.08% 擺到 57.45%，擺幅逾 40pp；擴產期資本支出大於營業現金流。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：Lumentum 稱缺口逾三成、TrendForce 預期失衡延續到 2027 之後（皆二手轉述）；但 Coherent 兩度倍增 InP 產線、Lumentum 美國新廠、聯亞 2027 產能 2.5 倍，新供給 2026–2028 上線，供給可逆性高。","bargaining":{"up":"上游 InP 基板強勢：2025Q4 起已漲三次、Q4 評估再漲逾一成；聯亞以住友電工 2026–2030 長約與安全庫存緩衝。","down":"客戶由 7–8 家增至 10 家以上，但三家客戶占應收帳款 74%，且主要客戶本身有自建 InP 能力。","geo":"2025 年銷售 71% 在中國；基板受中國出口管制影響，已推動日本與歐洲供應商認證。"},"profit_pool_dir":"缺貨期利潤池往雷射與磊晶環節移動，能否留住取決於 2027–2028 新產能上線後的報價。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率或利潤池占比；只有 800G 以上出貨由 2,400 萬增至 6,300 萬的二手引述，不足以建滲透率表。"}}}},"q2_moat":{"verdict":"護城河 B 級、方向持平：開放式 InP 磊晶市占逾六成與客戶擴張是真的，但現在的定價力主要來自缺貨，2023 年毛利率曾掉到 13%，證明它不是結構性定價權。","reasoning":"機制是磊晶製程經驗加上客戶的雷射重新認證週期：模組廠換磊晶來源要重驗，這給了黏性；住友電工 2026–2030 基板長約鎖住核心材料。利潤率對比：TTM 毛利率 54.53%、營益率 41.72%，高於全新（37.27%／21.72%）與 Lumentum（41.67%／17.79%），但同業 ROIC 事實表未涵蓋，只能比利潤率，且對比落在缺貨高峰。執行力給 8 分（1.6T 量產、3.2T 送驗、客戶擴到 10 家以上），定價力給 6 分（2023 年營收年減 55.65%、毛利率 13.08%、全年虧損，缺貨一退報價就守不住）。方向判持平而非擴大：執行面在擴大，但定價面受三股力量夾擊——基板廠 Q4 再漲逾一成吃掉利潤、Coherent 與 Lumentum 自建 InP 產線、IDM 自行供應磊晶。ROIC 只能拆一半：稅後營業利益率高，投入資本周轉率事實表未涵蓋；再投資率約 200%（Q2 稅後淨利 468.5 百萬元減自由現金流 −479.3 百萬元，得再投資約 948 百萬元，以淨利代稅後營業利益），增量 ROIC 無法推導。","fact_refs":["f_peer_3081_two_gross_margin_pct","f_peer_3081_two_operating_margin_pct","f_peer_2455_tw_gross_margin_pct","f_peer_2455_tw_operating_margin_pct","f_peer_lite_gross_margin_pct","f_peer_lite_operating_margin_pct","f_kpi3_eps","f_kpi4"],"verdict_values":{"moat":{"mechanism":"磊晶製程經驗＋客戶雷射重新認證週期＋InP 基板長約；替代性的決策單位是客戶每一代模組的雷射認證，不是磊晶片這個商品。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大（客戶 7–8 家增至 10 家以上、1.6T 量產、開放式 InP 磊晶市占逾六成）；定價面僅穩定（漲價來自全產業缺貨，同業倍增產能與 IDM 自製在 2027–2028 壓回），合判持平。","competitor_notes":[{"name":"全新光電 2455.TW","strategy_note":"同為磊晶廠，TTM 毛利率 37.27%、營益率 21.72%，均低於聯亞，產品組合較分散，屬點對點競爭。"},{"name":"Lumentum LITE","strategy_note":"既是客戶也是潛在自製者：自有 InP 雷射產能並在美國新建廠，TTM 營益率 17.79%；其擴產直接壓縮外購磊晶需求。"},{"name":"Coherent","strategy_note":"不在對照表；報導將於今年與 2027 年底前兩度倍增 Sherman InP 產線，是 2028 年供給增量最大來源之一。"},{"name":"IQE.L","strategy_note":"事實表無財務資料，無法比較；屬開放式磊晶同業。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能以毛利率與營益率對比；IQE.L 財報資料缺。","threats":[{"level":"🔴","text":"IDM 自行供應磊晶加上 Coherent、Lumentum 自建 InP 產能，2027–2028 削弱外購磊晶需求與報價。","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#3"]},{"level":"🟡","text":"InP 基板受中國出口管制，限制延續且無新增來源時中長期供應受限；已有長約與安全庫存緩衝。","p":"20%","evidence_refs":["supply_demand_durability#3","geo_supply_chain#2"]},{"level":"🟡","text":"全新等開放式磊晶同業擴產搶單，屬點對點競爭。","p":"25%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋，擴產期資本密集度上升，推測偏低周轉）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是雲端資料中心、決策者是光模組廠、付款者是模組廠；AI 叢集光互連是需要不是想要，800G 以上出貨由 2,400 萬增至 6,300 萬（二手引述）。急迫性不等於持久性，需求強度已反映在報價。"},{"level":"🟡","item":"決策層級","text":"替代性要在客戶每一代雷射認證衡量：換磊晶來源需重驗，黏性存在；但 Lumentum、Coherent 有能力自製，IDM 自行供應已被賣方點名，重新認證週期隨 3.2T 換代可能成為轉單窗口。"},{"item":"價值鏈分配","level":"🟡","text":"缺貨期利潤往雷射與磊晶環節移動，但上游基板已漲三次、Q4 再評估漲逾一成，下游客戶集中（三家占應收 74%）且可自建，聯亞夾在兩個強勢環節之間，需求存在不等於這一環能長期多拿。"},{"item":"社會容忍度","level":"🟢","text":"企業間零組件，無監管定價或社會漲價天花板；唯一政策面是基板出口管制，屬供應風險而非價格上限。"}],"roiic":"事實表未涵蓋（無投入資本序列，無法算增量 ROIC）","reinvest_rate":"約 200%（Q2 2026：淨利 468.5 百萬元 − 自由現金流 −479.3 百萬元 ＝ 再投資約 948 百萬元，以淨利代稅後營業利益）","endo_ceiling":null,"formula_note":"再投資＝淨利−自由現金流＝資本支出−折舊＋營運資金增加；單季數字，擴產高峰期偏高。"}}}},"q3_growth":{"verdict":"成長跑道中等：矽光與 1.6T／3.2T 世代切換讓量至少成長到 2027，但滲透率事實表未涵蓋，且 2028 年起同業新產能湧入，五年後成長取決於報價能否守住。","reasoning":"成長來源以量為主（2027 產能 2.5 倍、客戶擴到 10 家以上），價為輔（基板與磊晶片 2025Q4 起多次漲價），無併購、無回購。共識 EPS：FY2025 實際 4.21 元、FY2026E 19.61 元、FY2027E 39.39 元，兩年年化約 206%；FY2028E 共識事實表未涵蓋，無法算三年 CAGR。內生上界：增量 ROIC 推不出，再投資率約 200% 且已靠私募與可轉債補資金，共識成長顯然超過內部資金可支撐的速度。缺口歸因毛利率擴張（2025 年 42.7% → Q2 2026 57.45%）與漲價，不是回購或併購；這部分會隨供需反轉回吐。第二曲線有線索（3.2T、延伸到 EML 與接收端 PD，公司稱與 CW 雷射並非互相取代），但沒有量化依據，故不給寬燈。衰退信號亮一盞：EPS 成長遠快於營收成長（差距來自毛利率擴張）；自由現金流轉負但只一年，未達連兩年門檻。","fact_refs":["f_kpi6","f_kpi7_datacom","f_kpi1","f_consensus_eps_fy1","f_consensus_eps_fy2"],"verdict_values":{"growth":{"driver_mix":"量為主（2027 產能 2.5 倍）＋價為輔（基板與磊晶片多次漲價）；無併購、無回購。","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 無法從事實表推導；再投資率約 200% 且靠私募（上限 4,500 張）與 12 億元可轉債補資金，共識 FY2025→FY2027 EPS 年化約 206% 遠超內部資金可支撐速度，缺口歸因毛利率擴張與漲價。","segments":[{"item":"DataCom（矽光為主）","value":"占營收 80–85%"},{"item":"電信","value":"占營收 5–10%"},{"item":"其他","value":"約 5%"}],"seven_questions":[],"decay_signals":["EPS 成長顯著高於營收成長（毛利率由 42.7% 擴張至 57.45% 推動）：亮","自由現金流／淨利 < 0.75：2026 年轉負但只一年，未達連兩年：未亮","毛利率連兩季年減：未亮","TAM 被替代技術壓縮：公司稱 EML 與 CW 雷射各有應用，未見替代報導：未亮"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置屬擴產期：自由現金流轉負、靠私募與可轉債補錢，沒有回購，股東稀釋風險大於員工酬勞稀釋。","reasoning":"FCF／淨利：2025 年 626.8／428.4 百萬元約 1.46 倍，轉換良好；2026 起擴產，Q2 營業現金流 268.6 百萬元、資本支出 748.0 百萬元，自由現金流 −479.3 百萬元，TTM FCF 利潤率 −2.46%；營業現金流低於淨利，反映在製品與基板安全庫存堆高。近三季已公告資本支出近 60 億元，董事會另通過不超過 22.7 億元設備、向 Aixtron 購置約 8.37 億元設備；資金來源包括 2026 年 1 月通過的私募（上限 4,500 張，以 900 元計約 40.5 億元，約占現有股本 4%）與 6 月通過的 12 億元有擔保可轉債，是否完成與實際價格事實表未涵蓋。股票酬勞占營收 0.7%、占營業利益 1.6%，很低。股息殖利率 0.099%，無回購。","fact_refs":["f_kpi4","f_kpi5_sbc","f_peer_3081_two_fcf_margin_pct","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"無併購"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"無回購；反向有私募普通股上限 4,500 張與 12 億元有擔保可轉債"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"股票酬勞占營收 0.7%、占營業利益 1.6%（Q2 2026）"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，現金去向集中在擴產資本支出；近三年現金去向四分事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求缺貨報價延續到 2028 年以後、2.5 倍產能全數以現價賣光、毛利率守在 55% 以上，而且市場繼續給高成長倍數；四件事同時成立的機率我不信。","reasoning":"FY1 本益比 154.3 倍、FY2 76.8 倍（3,025 元分別除以 19.61、39.39），P/S 84.28 倍、EV/S 83.89 倍，trailing 本益比 306.8 倍，各自都在可得年度端點的最高位。賣方均值目標價約 3,136 元（10 位、資料日期未明），只比現價高約 3.7%，區間 900–4,500 元，最高最低相差 5 倍，共識本身分歧大；另一來源 469 元疑為過期快照，不採用。PEG 以 FY1 本益比除以 FY2026→FY2027 共識成長 100.9% 得 1.53；若用 FY2025 起算的兩年年化約 206% 會得到更低的數字，但基期是虧損後復甦年，便宜論證不成立。同業現值本益比事實表未涵蓋，終端倍數無法附同業對照。分母爭點：FY2027 共識 EPS 隱含缺貨報價與新產能全數售出，屬循環高點盈餘。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"Fwd P/E（FY2027E 共識 EPS）＋P/S 年度端點對照","tier":"AI 光通訊上游元件（磊晶與雷射）","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比或 EV 倍數，無法建同層級倍數錨。"},"fwd_pe":154.3,"peg":1.53,"percentile_5y":100,"val_light":"🔴","val_light_derivation":"FY2 本益比 76.8 倍，對一家四年內兩年虧損、毛利率擺幅逾 40pp 的公司過高；P/S 以四個年度端點計現值高於所有端點（分位 100，非連續五年分位）；判紅。","upside_short_pct":3.7,"upside_mid_pct":-53.7,"denominator_disputed":true,"denominator_note":"FY2027E 共識 EPS 39.39 元隱含缺貨期報價與 2.5 倍產能全數售出，是循環高點盈餘；以它算出的倍數與 PEG 低估真實價格，便宜論證不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是把缺貨期毛利率當成新常態；陷阱風險中等。","reasoning":"反證集中在三件事：上一輪下行實績（2023 年營收年減 55.65%、毛利率 13.08%、EPS −2.10，股價 2023 年 10 月低見 98.2 元）、2027–2028 同業新產能與 IDM 自製、基板受中國出口管制。衰退信號亮一盞（EPS 成長遠快於營收），自由現金流轉負只一年。反方向也可能看錯：若 3.2T 與 CPO 讓缺貨延續到 2029，本份的 Base 過於保守。細節見反證紀錄。","fact_refs":["f_kpi1","f_kpi4","f_pe_current"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環高點盈餘陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":19.61,"pe":154.3,"basis":"FY2026E 共識 EPS（FY1）；終端倍數同樣乘終端年度 EPS"},"eps":{"bull":[42,56,68,80,92],"base":[37,44,42,46,50],"bear":[32,28,20,18,22]},"pe":{"bull":45,"base":28,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.099,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-85,"hi":-55,"basis":"上一輪下行（2023）營收年減 55.65%、毛利率由 31.88% 掉到 13.08%、全年轉虧，股價 2023 年 10 月低見 98.2 元；本次起點倍數更高（FY1 154 倍），Bear 終點跌幅約 84%、Base 約 54%，故範圍取 −55% 至 −85%。","trigger_time":null},"basis":{"bull":"缺貨延續到 2028 年後、3.2T 與 CPO 接棒，2.5 倍產能滿載且毛利率守 55% 以上；終端 45 倍給 AI 光通訊高成長溢價。","base":"2027 年大致達成共識，2028 年量增抵銷降價、2029 年同業新產能上線報價下修拖累一年，毛利率回到約 40%；終端 28 倍。","bear":"2027 下半年起報價轉跌、IDM 自製與同業倍增產能，毛利率回到 25–30%，重演 2023 型態但不轉虧；終端 22 倍取成長熄火降至一成的倍數。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"上一輪下行 2023 年營收年減 55.65%、毛利率 13.08%、EPS −2.10；Coherent 兩度倍增 InP 產線、Lumentum 美國新廠、高盛點名 IDM 自行供應磊晶。","assumption":"本份假設 2027 年前缺貨不退。","consequence":"2028 年新產能到位、報價轉跌，毛利率回到 25–30%，EPS 腰斬、倍數由成長股壓到循環股，五年後虧損逾 80%。","ruling":"採納：Bear 機率給 30%，與唯一致命點部分重疊（報價轉跌是同一事件的觸發點），終端倍數與 EPS 路徑已反映。","watch":"單季毛利率、磊晶片報價方向、同業擴產進度","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_supply_discipline_capacity#3"],"fact_refs":["f_kpi1"]},{"view":"論點失敗","evidence":"2025 年底三家客戶占應收帳款 74%，2025 年銷售 71% 在中國；基板受中國出口管制。","assumption":"客戶擴到 10 家以上已分散風險。","consequence":"單一大客戶轉自製或中國客戶縮單，單季營收可能季減逾一成五。","ruling":"採納為中期風險，列入假設風險清單；客戶營收占比事實表未涵蓋，無法量化。","watch":"年報客戶揭露、月營收季減幅度","evidence_refs":["customer_concentration_credit#0","geo_supply_chain#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Q2 自由現金流 −479.3 百萬元；近三季資本支出近 60 億元，靠私募（上限 4,500 張）與 12 億元可轉債補錢；基板 Q4 再漲逾一成。","assumption":"需求兌現就等於股東賺錢。","consequence":"需求兌現但新產能報酬率低於舊產能、股本擴張約 4–5%，每股盈餘成長落後營收成長。","ruling":"部分採納：股本稀釋規模有限，但擴產報酬率無法驗證，資本配置不給加分。","watch":"自由現金流轉正時點、私募完成價格與股數","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2"],"fact_refs":["f_kpi4"]},{"view":"價格已反映太多","evidence":"FY1 本益比 154.3 倍、FY2 76.8 倍、P/S 84.28 倍；賣方均值目標價約 3,136 元與現價相近；美系外資 3 月即以評價已反映利多降評。","assumption":"市場會持續用成長股倍數看待 2027 年盈餘。","consequence":"即使 Bull 路徑五年報酬約 +37%，Base 約 −54%，期望值為負。","ruling":"採納：這是本份不追的主要約束。","watch":"股價對 FY2027 共識 EPS 倍數","evidence_refs":[],"fact_refs":["f_pe_current","f_ps_current","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 3025.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=3025.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"供需持久度","cause":null,"prior_field":null,"side_a":"業界預期 InP 供需失衡延續到 2027 之後，Lumentum 稱產能訂滿到 2028、缺口逾三成（二手轉述）。","side_b":"Coherent 兩度倍增 Sherman InP 產線、Lumentum 美國新建廠、聯亞 2027 產能 2.5 倍，新供給 2026–2028 陸續上線；賣方點名 IDM 自行供應磊晶。","ruling":"不可調和（對 2028 年報價方向相反）。裁決偏向供給追上：供給增量是已公告的實體擴產，需求面多為二手引述且只看到 2028。決定性數字是 2027 下半年磊晶片報價方向。","evidence_level":"中（多為二手報導）","settle_metric":"磊晶片與 CW 雷射報價方向、單季毛利率","if_then":["若 2027 上半年磊晶片報價仍上調且單季毛利率 ≥55%，股價回到 FY2027 共識 EPS 35 倍以下時建立首倉 2%","若出現首次降價報導，未持有者不碰，持有者清倉"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#5","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"7 月營收年增 176.54%、Q3 財測季增約 20%、2027 產能 2.5 倍、客戶擴到 10 家以上，FY2027 共識 EPS 較 FY2026 翻倍；若 2028 仍缺貨，EPS 再上一層，倍數可被成長消化。","side_b":"即使 Bull 路徑（2031 年 EPS 92 元、45 倍）五年總報酬也只約 +37%，Base 約 −54%；現價已定價最好情境。","ruling":"可調和（程度差異）：生意好與價格貴同時成立，裁決不追。","evidence_level":"中","settle_metric":"單季毛利率與月營收年增率","if_then":["若 2027 年前兩季毛利率 ≥55% 且月營收年增 ≥80%，上修 Base 終端 EPS 並重跑研究","若股價先漲而報價證據未到，不追"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#2"]},{"axis":"賣方共識與本份分歧","cause":null,"prior_field":null,"side_a":"賣方 10 位均值目標價約 3,136 元，8 買 1 持有 1 賣，Macquarie 目標價 3,345 元。","side_b":"本份 Base 五年終值約 1,400 元，期望報酬為負。","ruling":"分歧屬框架層：賣方以 12 個月內 FY2027 盈餘乘倍數，本份以五年內含一次報價下行的盈餘定價；市場錯在把缺貨期毛利率當常態。全距最高最低相差 5 倍，本份對 Base 路徑的信心也下調。","evidence_level":"中","settle_metric":"2027 下半年單季毛利率","if_then":["若 2027 下半年毛利率仍 ≥55% 且無降價報導，本份框架錯，上修 Base 機率並重跑研究","若毛利率跌破 50%，維持不碰"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"擴產吸收驗證：2027 年起月營收年增率","type":"假設驗證","maps_to":"H1","metric":"月營收年增率","threshold":"連續 3 個月 < 30%","action":"持有者減碼一半；未持有者維持不追","source_freq":"公開資訊觀測站，每月","date":null},{"n":2,"text":"磊晶片或 CW 雷射報價首次調降","type":"Single Thing","maps_to":"Single Thing","metric":"磊晶片報價方向","threshold":"首次出現降價報導","action":"清倉","source_freq":"產業報導、法說會，每季","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#3"]},{"n":3,"text":"毛利率跌破缺貨期水準","type":"風險","maps_to":"R1","metric":"單季毛利率","threshold":"< 50%","action":"減碼一半","source_freq":"季報，每季","date":null,"evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2"]},{"n":4,"text":"大客戶轉自製或導入第二來源","type":"風險","maps_to":"R3","metric":"前三大客戶採購動向","threshold":"任一宣布自製或第二來源","action":"減碼一半","source_freq":"產業報導、年報，不定期","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":5,"text":"估值回到可進場區且毛利率未破","type":"估值rearm","maps_to":"H2","metric":"股價對 FY2027 共識 EPS 倍數","threshold":"≤ 35 倍（約 1,380 元）且單季毛利率 ≥50%","action":"重跑研究後首倉 ≤2%","source_freq":"每日股價、每季毛利率","date":null},{"n":6,"text":"Q3 2026 財報與法說複審","type":"複審日期","maps_to":"H1","metric":"Q3 營收季增率與毛利率","threshold":"季增 ≥20%、毛利率 ≥55%","action":"未達則下修 Base 路徑","source_freq":"季報","date":"2026-11"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"連兩季 < 45%","window":"2027Q1–2028Q4","source":"公司季報","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連三個月轉負","window":"2027–2028","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"磊晶片報價方向","bear_threshold":"首次降價報導","window":"未來 12–24 個月","source":"產業報導（經濟日報、TrendForce）與法說會","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,380 元）且單季毛利率仍 ≥50%","exec_line":"不追；未持有者等上述價位並重跑研究，首倉 ≤2%；已持有者毛利率跌破 50% 減碼一半，報價轉跌清倉。","holding_cap":"3%"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把缺貨期 57% 毛利率與 2.5 倍產能全數售出當成常態，忽略 2027–2028 同業 InP 產線倍增、IDM 自製與 2023 年毛利率 13% 的先例。","momentum_overheated":false,"cycle_gates_pass":false,"wait_for_price":true,"wait_for_price_condition":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,380 元）且單季毛利率仍 ≥50%"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把缺貨期 57% 毛利率與 2.5 倍產能全數售出當成常態，忽略 2027–2028 同業 InP 產線倍增、IDM 自製與 2023 年毛利率 13% 的先例。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=43.67, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"矽光需求吸收 2027 年 2.5 倍產能：2027 年營收至少為 2026 年的 2 倍","2y":"2027 年營收 ≥ 2026 年 2 倍","5y":null,"10y":null,"threshold":"2027 年月營收年增率維持 ≥50%，全年營收 ≥2026 年 2 倍","source":"公開資訊觀測站月營收、季報、法說會","drift_rule":"營收連 2 季低於上述路徑 ≥5% 判削弱，連 3 季 ≥10% 判反轉"},{"id":"H2","text":"基板漲價下毛利率仍守 50% 以上，代表報價權在缺貨期留在磊晶環節","2y":"2027 年各季毛利率 ≥50%","5y":null,"10y":null,"threshold":"單季毛利率 ≥50%（Q2 2026 為 57.45%）","source":"季報、法說會","drift_rule":"毛利率連 2 季較基準低 ≥5% 判削弱，連 3 季低 ≥10% 判反轉"},{"id":"H3","text":"開放式 InP 磊晶市占與客戶基礎在同業擴產與 IDM 自製下守住","2y":null,"5y":"2031 年客戶數仍 ≥10 家、前三大客戶無一轉自製","10y":null,"threshold":"客戶數 ≥10 家；開放式 InP 磊晶市占 ≥50%","source":"年報客戶揭露、產業報導","drift_rule":"任一前三大客戶公開轉自製或連 4 季營收年增落後同業 ≥5% 判削弱；兩家轉自製或連 6 季落後 ≥10% 判反轉"}],"R":[{"id":"R1","text":"InP 基板供應受中國出口管制與基板廠漲價擠壓，出貨與毛利同時受限","h_ref":"H2","clock":"⚡","threshold":"單季營收季減且公司歸因缺料，或單季毛利率 < 50%","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2","geo_supply_chain#2"]},{"id":"R2","text":"2027–2028 同業倍增產能與 IDM 自製帶來報價反轉，重演 2023 年毛利率崩落","h_ref":"H2","clock":"🔥","threshold":"磊晶片報價首次調降，或毛利率連 2 季年減","evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R3","text":"客戶與地區集中：三家客戶占應收 74%、2025 年銷售 71% 在中國","h_ref":"H3","clock":"🔥","threshold":"任一前三大客戶宣布自製或第二來源，或單季營收季減 ≥15%","evidence_refs":["customer_concentration_credit#0"]},{"id":"R4","text":"擴產靠外部資金，自由現金流長期為負並稀釋股本","h_ref":"H1","clock":"🐢","threshold":"2028 年自由現金流仍為負，或股本較 2025 年底增加 >8%","evidence_refs":[]}],"single_thing":{"description":"磊晶片或 CW 雷射報價由漲轉跌（首次出現降價報導）","why_fatal":"EPS 路徑建立在缺貨期報價上；2023 年報價與稼動率一退，毛利率由 31.88% 掉到 13.08% 並轉虧。擴產 2.5 倍後固定成本更高，報價下跌對毛利率的槓桿比上一輪更大，是 EPS 最大的單一敏感項。","if_happens":"持有者清倉，未持有者不碰；Bear 機率上調並重跑研究。","how_monitor":"每季毛利率、月營收與產能的落差、產業媒體與 TrendForce 報價報導、同業產線上線時點","probability":"12–24 個月約 35%"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":76.8,"peg_fy2":0.76,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":4.21,"FY2026E":19.61,"FY2027E":39.39,"FY2028E":null},"fy_end_month":12,"eps_basis":"新台幣稀釋 EPS；FY2025A 為年度財報稀釋 EPS 4.209，FY2026E／FY2027E 為 yfinance 分析師共識平均，FY2028E 共識事實表未涵蓋"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026 財報與法說，驗證季增約 20% 財測","impact":"高","watch":"單季毛利率是否 ≥55%、Q4 展望與追加資本支出"},{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"InP 基板廠評估 Q4 再漲價逾一成","impact":"中","watch":"磊晶片是否同步第三次漲價、毛利率是否被吃掉"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"2027 年 2.5 倍產能上線節奏","impact":"高","watch":"月營收能否隨產能放大"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"Coherent Sherman InP 產線第二次倍增目標時點","impact":"高","watch":"磊晶片報價方向"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
