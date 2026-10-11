你是 DD 管線 v20 的判斷層閘（gate），標的 6187.TWO（20261011）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP 合併）＝2354.6 百萬 TWD｜期間與口徑：2026Q2（季末 2026-06-30，公告於 2026-08-10）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（對照 wantgoo 損益表 2,354,637 仟元；MOPS 為原文）（numbers.latest_quarter_kpis.items[0]，as_of 2026Q2（季末 2026-06-30，公告於 2026-08-10））
  - 註記：查無
- `f_kpi1`（q1_business）｜毛利率＝54.77 %｜期間與口徑：2026Q2（季末 2026-06-30，公告於 2026-08-10）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（毛利 1,289.7 ÷ 營收 2,354.6）（numbers.latest_quarter_kpis.items[1]，as_of 2026Q2（季末 2026-06-30，公告於 2026-08-10））
  - 註記：查無
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝782.8 百萬 TWD｜期間與口徑：2026Q2（季末 2026-06-30，公告於 2026-08-10）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（對照 wantgoo 783,342 仟元）（numbers.latest_quarter_kpis.items[2]，as_of 2026Q2（季末 2026-06-30，公告於 2026-08-10））
  - 註記：查無
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益率＝33.25 %｜期間與口徑：2026Q2（季末 2026-06-30，公告於 2026-08-10）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（782.8 ÷ 2,354.6；媒體報 33.27%，差異為四捨五入）（numbers.latest_quarter_kpis.items[3]，as_of 2026Q2（季末 2026-06-30，公告於 2026-08-10））
  - 註記：查無
- `f_kpi4_eps`（q1_business）｜稅後淨利（歸屬母公司）／基本 EPS＝8.5 TWD/股（淨利 826.9 百萬；稀釋 EPS 8.29）｜期間與口徑：2026Q2（季末 2026-06-30，公告於 2026-08-10）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt；媒體（經濟日報／中時）報 EPS 8.5 元創單季新高（numbers.latest_quarter_kpis.items[4]，as_of 2026Q2（季末 2026-06-30，公告於 2026-08-10））
  - 註記：查無
- `f_kpi6_backlog`（q4_capital）｜合約負債（硬體訂單預收，backlog 代理）＝299 百萬 TWD｜期間與口徑：2026Q2 季末（2026-06-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：優分析 uanalyze.com.tw 轉述財報（媒體整理，未以 MOPS 原文核對）（numbers.latest_quarter_kpis.items[6]，as_of 2026Q2 季末（2026-06-30））
  - 註記：不適用
- `f_peer_6187_two_gross_margin_pct`（q2_moat）｜6187.TWO 毛利率＝53.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6187.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6187_two_operating_margin_pct`（q2_moat）｜6187.TWO 營業利益率＝28.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6187.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6187_two_fcf_margin_pct`（q2_moat）｜6187.TWO FCF 利潤率＝11.13 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6187.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3131_two_gross_margin_pct`（q2_moat）｜3131.TWO 毛利率＝39.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3131.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3131_two_operating_margin_pct`（q2_moat）｜3131.TWO 營業利益率＝21.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3131.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3583_tw_gross_margin_pct`（q2_moat）｜3583.TW 毛利率＝35.77 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3583.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3583_tw_operating_margin_pct`（q2_moat）｜3583.TW 營業利益率＝14.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3583.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3583_tw_fcf_margin_pct`（q2_moat）｜3583.TW FCF 利潤率＝19.11 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3583.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6640_two_gross_margin_pct`（q2_moat）｜6640.TWO 毛利率＝40.99 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6640.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6640_two_operating_margin_pct`（q2_moat）｜6640.TWO 營業利益率＝19.33 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6640.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2467_tw_gross_margin_pct`（q2_moat）｜2467.TW 毛利率＝46.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2467.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2467_tw_operating_margin_pct`（q2_moat）｜2467.TW 營業利益率＝21.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2467.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2467_tw_fcf_margin_pct`（q2_moat）｜2467.TW FCF 利潤率＝-7.38 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2467.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi5`（q4_capital）｜自由現金流（營業現金流 − 資本支出）＝448.0 百萬 TWD｜期間與口徑：2026Q2（季末 2026-06-30，公告於 2026-08-10）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（OCF 1,219.0 − Capex 771.0）（numbers.latest_quarter_kpis.items[5]，as_of 2026Q2（季末 2026-06-30，公告於 2026-08-10））
  - 註記：查無
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.765 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1525.0 USD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝78.73 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝95.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝95.2 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝23.34 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝22.62 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝74.31 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ma_w104`（q5_valuation）｜104 週均線＝587.72 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）
- `f_ma_w250`（q5_valuation）｜250 週均線＝325.62 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）
- `f_ma_w52`（q5_valuation）｜52 週均線＝813.62 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）

### findings_digest 中方向為負或來源衝突的條目（5 條）
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：報導稱萬潤半導體封測設備占營收約70–80%，客戶以晶圓代工與封測龍頭為大宗（約80%），主要客戶含台系晶圓代工廠與日月光投控；此為2025年3月報導，非2026年精確比重
  - 來源：搜尋結果彙整（2025年3月報導，原文網址未能確認）（as_of 2025-03-31）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：管理層法說稱對2025年訂單掌握度高，但仍投入矽光子及FOWLP新製程研發以降低掉單風險
  - 來源：搜尋結果彙整（財經媒體報導，原文網址未能確認）（as_of 2025-03-31）｜affects：decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：TrendForce：CoWoS 供需缺口預期由約 20% 收斂至 2026 年底約 10%，2027 年進一步改善（短缺趨緩）
  - 來源：TrendForce News (2026-06 報導)（as_of 2026-06-30）｜affects：decision_inputs.bear、thesis.R
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：CPO專案遞延疑慮使股價自4月盤中高點回檔逾29%
  - 來源：搜尋摘要（外資報告報導）（as_of 2026-08-20）｜affects：decision_inputs.bear、triggers
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：高盛將萬潤12個月目標價由1650元下修至1550元，維持買進，因CPO設備產出效率提升而調降相關營收預測；as_of 為依 URL 日期推定，非確證
  - 來源：工商時報/ctee 報導（搜尋摘要轉述）（as_of 2026-07-27）｜affects：valuation、thesis.R

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6187.TWO_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":3496,"bear_5y_price":456,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":-13.4,"ev5y_pct":-4.7,"irr_base_pct":-2.8,"asym_ratio":1.1,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":19.37,"pe":78.73,"basis":"TTM（至 2026Q2）每股盈餘，由現價 1525 元 ÷ TTM 本益比 78.73 倍反推；終端倍數同為 trailing 口徑套在終端年 EPS"},"eps":{"bull":[32,48,66,80,92],"base":[30,38,43,39,44],"bear":[28,30,20,14,19]},"pe":{"bull":38,"base":30,"bear":24},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.765,"net_buyback":-1.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | none | 0 | 3 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 3 | 2 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | none | 0 | 2 |
| reg_tariff_export | found | 1 | 4 |
| geo_supply_chain | none | 0 | 3 |
| end_markets | found | 6 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 2 |
| major_events | none | 0 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **competitive_share_entrants**（none）：萬潤 6187 市占 競爭對手 新進入者 2026；All Ring Tech 6187 market share competitor advanced packaging equipment 2026；萬潤 點膠 高市占 CoPoS CPO 設備 競爭 弘塑 均華 搶單
- **customer_second_source**（none）：萬潤 6187 最大客戶 第二供應商 OR 自製 2026；All Ring Tech 6187 CoWoS equipment TSMC second source in-house 2026
- **regulatory_antitrust**（none）：6187.TWO 萬潤 antitrust OR monopoly investigation 2026；萬潤科技 6187 公平會 OR 法規 OR 出口管制 2026
- **geo_supply_chain**（none）：萬潤 6187 供應鏈 地緣 中國 營收占比 2026；All Ring Tech 6187 manufacturing location geopolitical risk 2026；萬潤 海外供應鏈 擴產 廠房 中國 昆山 先進封裝設備 關鍵零組件 進口
- **major_events**（none）：萬潤科技 6187 併購 收購 2025 2026；萬潤科技 6187 訴訟 集體訴訟 證券；萬潤科技 6187 證交所 調查 重編 財報 更正；All Ring Tech 6187 recall OR warning OR FDA OR investigation 2025 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"6187.TWO","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"萬潤"},"oneliner":"萬潤靠 CoWoS 點膠設備拿到同業最高毛利率，營收正在翻倍；但現價已是 TTM 本益比 79 倍，等於預支 CPO 大成功的情境，加上 2023 年營收腰斬的循環紀錄，不追，等 900 元以下或 CPO 量產兌現再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6187.TWO_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6187.TWO_20261011/scenario.json","answers":{"q1_business":{"verdict":"賺的是 AI 晶片先進封裝擴產的設備錢：封測設備占營收八到九成、兩大客戶約占八成，錢卡在 CoWoS 擴產這一節點；產業在擴張期，但 2027 下半年後有週期反轉風險","reasoning":"營收結構：半導體封測設備占營收八到九成，CoWoS 點膠設備地位強；其餘業務細項事實表未涵蓋。客戶以台系晶圓代工與日月光投控為大宗、約占八成（2025-03 報導，非 2026 年精確比重），屬單點依賴，列為集中度風險；近期報導另稱已切入其他 AI 供應鏈客戶。最新一季（2026Q2）營收 2,354.6 百萬元、毛利率 54.77%、營業利益率 33.25%、基本 EPS 8.5 元；淨利 826.9 百萬元高於營業利益 782.8 百萬元，業外成分事實表未涵蓋。錢卡在哪：AI 晶片封裝產能不足時，擴產支出流向點膠、貼合等關鍵站點設備，設備商拿到價格與交期溢價。產業時鐘在擴張期，依據是訂單而非股價：8 月營收年增 103%，季末合約負債由 0.74 億元增至 2.99 億元，產能滿載並向外預留 2027–2028 年產能。供需持久性屬週期性、2027 下半年後可能反轉：CoWoS 供需缺口預期由約 20% 收斂至 2026 年底約 10%，2027 年片數成長放緩，後續要靠每片設備用量與 CPO、面板級封裝撐。產業態勢三軸：競爭面未見新進者或份額流失報導；結構面是設備用量上升與短缺收斂對拉；其他變數中美國 232 關稅屬產業背景、未見直接暴露，面板級封裝定位為加產能而非取代 CoWoS。裁決為雙向拉鋸。","fact_refs":["f_kpi0_gaap","f_kpi1","f_kpi2_gaap","f_kpi3_gaap","f_kpi4_eps","f_kpi6_backlog"],"verdict_values":{"revenue_quality":"設備一次性銷售、交機驗收後認列，年度波動大（2023 年營收年減 46.4%、2024 年年增 359%、2025 年 −3%）；合約負債 2.99 億元僅約當 8 月單月營收的兩成七，訂單能見度主要靠法說口述","unit_econ_note":"毛利率 54.77%、研發占營收 13.28%（同業 4.7%–7.8%）；單機價格與出貨台數拆分事實表未涵蓋","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收隨客戶擴產劇烈擺盪（2023 年 −46%、2024 年 +359%），但谷底年毛利率仍有 51.81%"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性，2027 下半年後可能反轉：TrendForce 2026-06 缺口收斂預估對照公司 2026-08 法說能見度至 2027Q2","bargaining":{"up":"上游供應商結構事實表未涵蓋","down":"買方高度集中，兩大客戶約八成；短缺期議價力在設備商，缺口收斂後回到客戶端","geo":"台灣生產；美國 232 關稅屬產業背景，未見直接暴露"},"profit_pool_dir":"短缺期利潤池流向先進封裝關鍵站點設備，缺口收斂後預期回流客戶端","tam_table":[{"item":"CoWoS 供需缺口","value":"約 20% → 2026 年底約 10%，2027 年續改善（TrendForce，2026-06）"},{"item":"CoWoS 2027 年月產能","value":"約 18 萬片，片數成長放緩，轉看每片設備用量（鉅亨網，2026-09）"},{"item":"CPO 營收占比預估","value":"高盛：2026／2027／2028 年 3%／29%／69%（2026-09）"},{"item":"CPO 營收預估（另一外資，已下修）","value":"2027 年 21 億元（16%）、2028 年 102 億元（60%）"},{"item":"半導體設備業務成長","value":"美系外資估 2026–2028 年 CAGR 34%"},{"item":"滲透率與營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平：點膠製程綁定帶來同業最高的毛利率，但只能證明現在領先，證明不了差距在擴大，等級 B","reasoning":"機制：點膠製程與客戶製程參數綁定，換供應商要重跑驗證；再把點膠、貼合、自動化、光學檢測整合成整線方案，拉高單站以外的轉換成本。可證方向：TTM（至 2026-06）本公司毛利率 53.27%、營業利益率 28.9%，四家同業最高分別為 46.8% 與 21.9%，領先約 6.5 與 7.0 個百分點；研發占營收 13.28%，同業 4.7%–7.8%。自身毛利率由 2022 年 47.92% 升到 2025 年 54.29%，2023 年營收腰斬時仍有 51.81%（年度財報，yfinance）。執行力 8 分：製程延伸到 CPO、面板級封裝與 SoIC，600mm 面板級點膠設備已交付客戶前導線。定價力 7 分：谷底毛利率不破，但兩大客戶約八成、短缺收斂後議價力回升，CPO 設備產出效率提升也在壓縮機台需求。同業 ROIC 與歷年利差事實表未涵蓋，無法證明差距在擴大，故等級停在 B、方向持平。報酬持續期：投入資本事實表未涵蓋，當期 ROIC 無法計算；四檢查點三黃一綠。","fact_refs":["f_kpi1","f_peer_6187_two_gross_margin_pct","f_peer_6187_two_operating_margin_pct","f_peer_6187_two_fcf_margin_pct","f_peer_3131_two_gross_margin_pct","f_peer_3131_two_operating_margin_pct","f_peer_3583_tw_gross_margin_pct","f_peer_3583_tw_operating_margin_pct","f_peer_3583_tw_fcf_margin_pct","f_peer_6640_two_gross_margin_pct","f_peer_6640_two_operating_margin_pct","f_peer_2467_tw_gross_margin_pct","f_peer_2467_tw_operating_margin_pct","f_peer_2467_tw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"CoWoS 點膠製程的認證與製程參數綁定：設備要跟客戶一起調製程才能進線，換供應商等於重跑驗證；點膠、貼合、自動化、光學檢測整合成整線方案，提高單站以外的轉換成本","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"毛利率 2022→2025 年由 47.92% 升至 54.29%、2026Q2 54.77%，執行面在擴張（新製程前導線已交機）；但同業只有 TTM 單點，利差趨勢無從證明，缺口收斂後定價面難再擴大——執行擴大、定價持平，合判持平","competitor_notes":[{"name":"3131.TWO","strategy_note":"毛利率 39.1%、營益率 21.9%，研發密度約本公司一半，同吃先進封裝擴產但定價力明顯較弱"},{"name":"3583.TW","strategy_note":"毛利率 35.77%、營益率 14.39%，但自由現金流率 19.11% 高於本公司，資本負擔較輕"},{"name":"6640.TWO","strategy_note":"毛利率 40.99%、營益率 19.33%，與本公司差距約 12 與 10 個百分點"},{"name":"2467.TW","strategy_note":"毛利率 46.8% 最接近，但自由現金流率 −7.38%，擴產或營運資金正在吃現金"}],"threats":[{"level":"🟡","text":"客戶集中：台系晶圓代工與日月光投控約占八成，任一大客戶導入第二供應商即壓縮價格；管理層自己也在投入新製程研發以降低掉單風險","p":"30%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"level":"🟡","text":"CoWoS 短缺收斂：供需缺口由約 20% 收斂至 2026 年底約 10%，2027 年續改善，買方議價力回升、急單溢價消失","p":"40%","evidence_refs":["supply_demand_durability#3"]},{"level":"🟡","text":"CPO 設備產出效率提升，單位產能所需機台減少，新曲線的營收天花板被下修，專案亦有遞延疑慮","p":"35%","evidence_refs":["capital_markets_pricing#0","end_markets#4"]}],"roic_durability":{"quadrant":"高利益率×周轉率待查（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是封裝產線，決策者與付款者是台積電與日月光的資本支出，三角色同在客戶端；AI 封裝產能不足時屬「需要」，但擴產可延後——缺口由約 20% 收斂到 2026 年底約 10% 後急迫性下降，急迫不等於持久"},{"item":"決策層級","level":"🟡","text":"替代性要在單一製程站點衡量：CoWoS 點膠站的設備與製程參數綁定，同代製程內轉換成本高；但每一代新製程（面板級封裝、CPO）都重新比稿，管理層也承認要投入新製程研發以降低掉單風險"},{"item":"價值鏈分配","level":"🟡","text":"價值大多留在晶圓代工端，設備只占擴產支出的一小段；兩大客戶約八成營收，買方集中度高。目前毛利率 54.77% 顯示短缺期設備商分得到利潤，短缺收斂後分配會往客戶端移"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的資本設備，無民生價格敏感或監管授權依賴；美國 232 關稅屬產業背景，未見對本公司的直接暴露"}],"roiic":"事實表未涵蓋投入資本與折舊，無法計算","reinvest_rate":"2026Q2 單季資本支出 771.0 百萬元，接近當季營業利益 782.8 百萬元，擴產期再投資偏重；折舊與營運資金變動事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率；兩項輸入皆缺，天花板不估；本段成長來自外生的客戶擴產需求，情境樹視同超出天花板處理"}}}},"q3_growth":{"verdict":"五年後跑道偏寬：CPO 與面板級封裝是有出處的下一條曲線，但兩者都還在交機與驗證前，寬度要看 2027 年是否兌現","reasoning":"成長來源以量為主：客戶先進封裝擴產帶動出貨（2026 年 1–8 月營收 59.29 億元、年增 51%，8 月年增 103%），加上高單價新機種的組合改善與營業槓桿（營業利益率由 2022 年 21.3% 升至 2026Q2 33.25%）；未見併購與回購，股本反而年化擴張約 4%。賣方三年共識 EPS 事實表未涵蓋；僅有 2026-02 的舊估 2026／2027 年 18.14／19.6 元，TTM EPS 已達 19.37 元，舊估過時不採用。本判斷 Base 路徑 FY2025A 15.38 元到 FY2028E 43 元，三年 CAGR 約 41%。內生天花板因投入資本與折舊缺資料無法計算；缺口歸因於循環量能與利潤率擴張，延續性綁在客戶資本支出，不是內部再投資複利。跑道：滲透率資料缺，改以第二曲線判斷——CPO 耦合設備 2026Q4 交貨、2027Q1 放量，高盛估 2026–2028 年占營收 3%／29%／69%；面板級封裝 2027 年開始拉貨、2028 年才可能放大。衰退信號只有現金轉換半亮，其餘未亮或資料缺。","fact_refs":["f_kpi0_gaap","f_kpi3_gaap","f_kpi6_backlog","f_kpi4_eps"],"verdict_values":{"growth":{"driver_mix":"量（客戶先進封裝擴產）為主，價與組合（CPO、面板級封裝等高單價新機種）為輔，另有營業槓桿；無併購、未見回購，反有股本稀釋","runway_years":"事實表未涵蓋滲透率","runway_post_y5":"🟢","endo_ceiling_basis":"投入資本與折舊事實表未涵蓋，內生天花板無法計算；成長來自客戶擴產的外生需求，視同超出天花板","segments":{"expanded":false,"reason":"半導體封測設備占營收八到九成，其餘業務細項事實表未涵蓋；單一分部即決定利潤結構，成長拆解改在 CPO 與 CoWoS 兩條曲線的營收門檻追蹤"},"decay_signals":["FCF／淨利 < 0.75 連 2 年：2023、2024 年約 0.52、0.53 曾亮，2025 年回到 0.96，2026Q2 單季 0.54 再落下，判半亮","EPS CAGR 高於營收 CAGR 逾 5 個百分點：2022–2025 年 EPS 38.3% 對營收 33.6%，差 4.7 個百分點，未亮但貼線","毛利率連 2 季年減：2026Q2 54.77% 高於 2025 年 54.29%，未見下滑；季度年對年資料事實表未涵蓋","TAM 被替代技術壓縮：面板級封裝定位為加產能而非取代 CoWoS，未亮","其餘六項（市占、提價後銷量、員工股酬、估值倍數系統下移、維持性資本支出、停止投資新產能）事實表未涵蓋或未見"],"trap_rating":"價值陷阱風險🟡（半亮一項）、長期成長性🟡"}}},"q4_capital":{"verdict":"股東回饋偏弱：現金股利給得大方，但股本四年擴張約一成六，擴產期現金轉換掉到五成左右","reasoning":"現金轉換：FCF／淨利 2025 年 0.96（1,430.0／1,485.2 百萬元）、2024 年 0.53、2026Q2 單季 0.54（448.0／826.9 百萬元）；第二季資本支出 771.0 百萬元幾乎等於當季營業利益，屬海外拓點與擴產。股東回饋：TTM 殖利率 0.765%，以現價回推每股股利約 11.7 元，約 FY2025 稀釋 EPS 15.38 元的七成六。股本：以淨利÷稀釋 EPS 回推，稀釋股數由 2022 年約 85.8 百萬股、2025 年約 96.6 百萬股增至 2026Q2 約 99.7 百萬股，年化約 4%，成因（員工酬勞、可轉債或增資）事實表未涵蓋。現金去向：擴產資本支出與現金股利為主，未見併購與回購；員工股酬占營收、負債到期結構事實表未涵蓋。","fact_refs":["f_kpi5","f_kpi4_eps","f_kpi2_gaap","f_dividend_yield_ttm","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無併購紀錄，重大併購事件搜尋無結果"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未見回購紀錄，股東回饋以現金股利為主"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"稀釋股數由 2022 年約 85.8 百萬股增至 2026Q2 約 99.7 百萬股（淨利÷稀釋 EPS 回推），年化約 4%，高於 1.5% 上限；成因事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠內部擴產而非併購，未見併購與回購紀錄，股東回饋只有現金股利一條，已在理由中交代"}}}},"q5_valuation":{"verdict":"現價 1525 元要求五年後 EPS 約 82 元並維持 30 倍，等於押 Bull 情境；這條路徑只給兩成機率，不信","reasoning":"現價對應 TTM 本益比 78.73 倍（四個年度端點中 95.2 分位），P/S 23.34 倍與 EV/S 22.62 倍皆為年度端點最高；以本判斷 FY2026E Base EPS 30 元計，前瞻本益比約 50.8 倍。現價要求什麼：要五年年化 10%，以 30 倍終端倍數回推 FY2030 年 EPS 需約 82 元（1525×1.1^5≈2456，÷30），接近 Bull 路徑的 92 元，Base 只有 44 元。PEG 以 TTM 本益比 78.73 ÷ Base 三年 EPS CAGR 約 41% ＝1.92，表面在合理區上緣，但分母是擴產高峰的成長率。賣方目標價 1280–1800 元（最高對最低 1.41 倍），現價已在區間上緣，只有高盛 2026-09 的 1800 元高於現價。同業本益比事實表未涵蓋，不拿利潤率對照當倍數錨；五年分位口徑資料缺，只有四個年度端點分位。短期：FY2027E Base EPS 38 元 × 35 倍＝1330 元，−12.8%；中期：FY2030E 44 元 × 30 倍＝1320 元，−13.4%。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"TTM 本益比為主、自身 Base 路徑前瞻本益比為輔（同業倍數事實表未涵蓋）","peers":{"expanded":false,"reason":"同業本益比事實表未涵蓋，只有利潤率；不拿跨層級同業當倍數錨"},"fwd_pe":50.8,"peg":1.92,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"TTM 本益比 78.73 倍位於四個年度端點 95.2 分位，P/S 23.34 倍與 EV/S 22.62 倍皆為年度端點最高；Base 五年終值約 1320 元低於現價；PEG 1.92 看似合理但分母是擴產高峰成長率——綜合偏貴。五年分位口徑事實表未涵蓋","upside_short_pct":-12.8,"upside_mid_pct":-13.4,"denominator_disputed":true,"denominator_note":"TTM EPS 19.37 元低估近期獲利（營收正在翻倍，FY2026E 約 30 元），但 FY2026–2027 年 EPS 又是客戶擴產高峰的獲利；2026Q2 淨利 826.9 百萬元高於營業利益 782.8 百萬元，業外成分事實表未涵蓋。分母落在循環哪個位置本身就是爭點，任何「前瞻本益比已不貴」的論證都不成立"}}},"q6_how_wrong":{"verdict":"最可能看錯的方向是太保守：若 CPO 依高盛口徑放量、倍數撐在 35 倍以上，五年可翻倍；反方向是低估循環，擴產消化可讓股價回到 104 週均線附近","reasoning":"太保守的路徑：CPO 在 2028 年占營收約七成、面板級封裝 2028 年放大，FY2030 年 EPS 可到 92 元，38 倍下約 3,500 元，五年翻倍以上，機率給 20%。低估循環的路徑：2023 年營收年減 46%、EPS 年減 71%，現價距 104 週均線 587.72 元還有約 61% 的距離。衰退信號只有現金轉換半亮（2023、2024 年 FCF／淨利約 0.52、0.53，2025 年回到 0.96，2026Q2 單季 0.54），價值陷阱風險定黃燈；真正的陷阱不是生意變差，而是把擴產高峰的獲利當成常態給倍數。最強三個反駁點——高盛目標價已上調至 1800 元、營業利益率仍在擴張、谷底年毛利率 51.81% 證明定價力——已併入對質紀錄。","fact_refs":["f_pe_current","f_week26_return_pct","f_ma_w104","f_ma_w250","f_kpi5"],"verdict_values":{"trap":{"verdict":"🟡","label":"擴產高峰估值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":19.37,"pe":78.73,"basis":"TTM（至 2026Q2）每股盈餘，由現價 1525 元 ÷ TTM 本益比 78.73 倍反推；終端倍數同為 trailing 口徑套在終端年 EPS"},"eps":{"bull":[32,48,66,80,92],"base":[30,38,43,39,44],"bear":[28,30,20,14,19]},"pe":{"bull":38,"base":30,"bear":24},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.77,"net_buyback":-1.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-78,"hi":-55,"basis":"2023 年營收年減 46.4%、稀釋 EPS 由 5.82 元跌至 1.66 元（−71%）；現價為 104 週均線 587.72 元的 2.6 倍、250 週均線 325.62 元的 4.7 倍，回到 104 週均線即 −61%、回到 250 週均線約 −79%；2026 年 4 月以來 CPO 遞延疑慮已造成逾 29% 的回檔；Bear 終點約 −70% 落在區間內，故取 −55% 至 −78%","trigger_time":null},"basis":{"bull":"CPO 依高盛 2026-09 口徑放量（2028 年占營收約七成），面板級封裝 2028 年放大，毛利率守 54% 以上；2030 年仍有逾 15% 成長，給 38 倍","base":"2026 年營收約 100 億元（1–8 月 59.29 億元加月營收 11 億元水位），2027 年再增約三成（CPO 採已下修的外資口徑約 21 億元），2028 年放緩，2029 年擴產消化 EPS 回落約一成；終端 30 倍＝成長回到一成上下的設備龍頭。同業本益比事實表未涵蓋，無法附同業現值對照，僅以本身 TTM 78.73 倍為上界參考","bear":"CoWoS 短缺 2027 年收斂、客戶擴產暫停，CPO 遞延到 2028 年後；2029 年 EPS 自高點跌逾五成（2023 年曾跌 71%），2030 年回升至 19 元；終端 24 倍＝成長熄火降至一成的情境"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"CoWoS 供需缺口預期 2026 年底收斂至約 10%、2027 年續改善；CPO 專案遞延疑慮已讓股價自 4 月高點回檔逾 29%；2023 年營收年減 46%、EPS 由 5.82 元跌至 1.66 元","assumption":"2027 下半年客戶擴產消化與 CPO 遞延同時發生","consequence":"2029 年 EPS 跌至 14 元、2030 年回到 19 元，24 倍約 456 元，較現價約 −70%","ruling":"採納：Bear 機率給 35%，高於一般的 25–30%，理由是循環紀錄有實證，且現有訂單能見度只到 2027Q2，蓋不住風險窗；與唯一致命點（台積電擴產放緩）方向一致","watch":"台積電資本支出指引、季末合約負債、月營收年增率","evidence_refs":["supply_demand_durability#3","end_markets#4"],"fact_refs":["f_kpi6_backlog","f_pe_current"]},{"view":"論點成功但股東經濟變差","evidence":"高盛 2026-07 因 CPO 設備產出效率提升下修相關營收、目標價由 1650 降至 1550 元；兩大客戶約占營收八成；稀釋股數年化增約 4%；2026Q2 自由現金流僅為淨利的 0.54 倍","assumption":"CPO 與面板級封裝如期量產，但每單位產能所需機台變少、客戶壓價，擴產又吃掉現金","consequence":"營收成長而每股自由現金流成長落後，EPS 路徑接近 Base 而非 Bull","ruling":"部分採納：Base 已按下修後的外資 CPO 口徑估，淨回購殖利率設為 −1%；若 TTM 毛利率守在 50% 以上，壓價這一半不成立","watch":"TTM 毛利率、稀釋股數、全年 FCF／淨利","evidence_refs":["capital_markets_pricing#0","customer_concentration_credit#0"],"fact_refs":["f_kpi5","f_kpi4_eps"]},{"view":"價格已反映太多","evidence":"TTM 本益比 78.73 倍，P/S 23.34 倍與 EV/S 22.62 倍為年度端點最高；26 週漲 74.31%；現價為 52 週均線 813.62 元的 1.87 倍","assumption":"市場用結構成長的倍數定價擴產高峰的獲利","consequence":"即使 Base 路徑 FY2030 年 EPS 44 元成真，30 倍終值約 1320 元仍低於現價；要年化 10% 需 EPS 約 82 元","ruling":"採納：這是觀望的唯一綁定約束，價格回到 900 元以下才重新評估","watch":"股價對照 FY2027E Base EPS 38 元的倍數","evidence_refs":[],"fact_refs":["f_pe_current","f_ps_current","f_ev_s_current","f_week26_return_pct","f_ma_w52"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1525.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1525.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"CPO 第二曲線的規模與時點","cause":null,"prior_field":null,"side_a":"高盛 2026-09 估 CPO 占營收 2026／2027／2028 年 3%／29%／69%，目標價上調至 1800 元；CPO 耦合設備 2026Q4 交貨、2027Q1 放量","side_b":"高盛 2026-07 曾因 CPO 設備產出效率提升下修營收、目標價由 1650 降至 1550 元；另一外資 CPO 預估已下修，遞延疑慮讓股價自 4 月高點回檔逾 29%","ruling":"不可調和（一方擴大、一方縮小）。選下修側作 Base：設備產出效率提升是每單位產能要更少機台的結構性變化，不是時點問題；高盛口徑只放在 Bull，機率 20%","evidence_level":"賣方預估與媒體轉述，未經公司財測","settle_metric":"2027Q1–Q2 月營收與法說揭露的 CPO 認列","if_then":["若 2027Q2 前法說確認 CPO 量產認列且單季營收 ≥ 35 億元，上調 Base 的 2028 年 EPS 並重跑研究","反向：若 2027Q2 仍未見 CPO 量產出貨，Bull 機率降至 10%，持有者減碼一半"],"evidence_refs":["capital_markets_pricing#0","end_markets#4"]},{"axis":"擴產能見度對照短缺收斂","cause":null,"prior_field":null,"side_a":"公司 2026-08 法說稱能見度至 2027Q2、產能滿載並向外預留 2027–2028 年產能；季末合約負債由 0.74 億元增至 2.99 億元","side_b":"TrendForce 預期 CoWoS 缺口由約 20% 收斂至 2026 年底約 10%，2027 年續改善；2027 年月產能約 18 萬片、片數成長放緩","ruling":"可調和（時間差）：2027Q2 前訂單有底，風險窗在 2027 下半年至 2028 年；現有證據時間窗蓋不住風險窗，不可裁決至 2027Q2 法說","evidence_level":"公司口述加第三方研調","settle_metric":"季末合約負債與月營收年增率","if_then":["若 2027Q1 季末合約負債 ≥ 3 億元且月營收年增仍為正，Bear 機率由 35% 降至 25%","反向：若合約負債連 2 季下滑，持有者減碼至半倉，未持有者不進場"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"營收正在翻倍（8 月年增 103%），營業利益率由 2022 年 21.3% 升至 2026Q2 33.25%；谷底年毛利率 51.81%；高盛最新目標價 1800 元高於現價 18%；CPO 與面板級封裝兩條新曲線都有出處","side_b":"TTM 本益比 78.73 倍、P/S 與 EV/S 為年度端點最高；Base 五年終值約 1320 元低於現價；2023 年 EPS 跌 71% 的循環紀錄","ruling":"不追：即使 Base 路徑 FY2030 年 EPS 44 元成真，30 倍終值仍低於現價；要年化 10% 需 EPS 約 82 元，等於押 Bull","evidence_level":"財報實績加賣方預估","settle_metric":"股價對照 FY2027E Base EPS 38 元的倍數","if_then":["若股價回落至 900 元以下而近 3 個月月營收年增皆為正，重跑研究評估首倉 ≤2%","反向：若股價續漲但 CPO 未見出貨，不追"],"evidence_refs":[]},{"axis":"盈餘品質與現金轉換","cause":null,"prior_field":null,"side_a":"2026Q2 淨利 826.9 百萬元高於營業利益 782.8 百萬元；自由現金流 448.0 百萬元僅為淨利 0.54 倍；資本支出 771.0 百萬元","side_b":"2025 年自由現金流 1,430.0 百萬元、FCF／淨利 0.96，自由現金流率 26.65%","ruling":"可調和：擴產期資本支出與營運資金墊高屬投資期現象；業外成分事實表未涵蓋，FY2026E 以本業獲利估、不外推業外","evidence_level":"財報實績","settle_metric":"2026 全年 FCF／淨利","if_then":["若 2026 全年 FCF／淨利 < 0.5 且 2027 年資本支出未降，Base 終端倍數由 30 倍降至 26 倍"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 900 元以下且月營收年增仍為正，重跑完整研究評估首倉","type":"估值rearm","maps_to":"H1","metric":"股價；月營收年增率","threshold":"股價 ≤ 900 元（約 FY2027E Base EPS 38 元的 24 倍）且近 3 個月月營收年增皆 > 0","action":"重跑研究，通過後首倉 ≤2%","source_freq":"每日股價／每月 10 日月營收","date":null,"evidence_refs":[]},{"n":2,"text":"台積電法說下修或暫緩 2027 年先進封裝擴產","type":"Single Thing","maps_to":"R2","metric":"台積電資本支出指引與 CoWoS 擴產口徑","threshold":"2027 年資本支出指引年減，或明言 CoWoS 擴產放緩","action":"未持有者不進場並把 Bear 機率上調至 45%；持有者減碼一半，當季合約負債同步下滑則清倉","source_freq":"台積電季度法說","date":"2027-01","evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"CPO 設備 2026Q4 交機、2027Q1 放量是否兌現","type":"假設驗證","maps_to":"H2","metric":"法說揭露之 CPO 出貨與月營收","threshold":"2027Q1 平均月營收 ≥ 12 億元且法說確認 CPO 認列","action":"兌現則上調 Base 2027–2028 年 EPS 後重跑研究；未兌現則 Bull 機率降至 10%","source_freq":"每月月營收／每季法說","date":"2027-04","evidence_refs":["end_markets#4","capital_markets_pricing#0"]},{"n":4,"text":"訂單預收連續下滑","type":"風險","maps_to":"R2","metric":"季末合約負債","threshold":"連 2 季下滑且低於 1.5 億元","action":"持有者減碼至半倉；未持有者 Bear 機率上調至 45%","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":5,"text":"定價力鬆動","type":"風險","maps_to":"R3","metric":"TTM 毛利率","threshold":"< 50%","action":"護城河等級重評，持有者減碼一半","source_freq":"季報","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":6,"text":"FY2026 年報與 2027 年第一季月營收出齊後複審","type":"複審日期","maps_to":null,"metric":"FY2026 EPS 對照 Base 30 元","threshold":"偏離 ≥10%","action":"重跑研究","source_freq":"年報","date":"2027-04-15","evidence_refs":[]}],"kill_metrics":[{"metric":"季末合約負債","bear_threshold":"連 2 季下滑且 < 1.5 億元","window":"2026Q4–2027Q2","source":"季報資產負債表","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連 3 個月 < 0","window":"2027 全年","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"TTM 毛利率","bear_threshold":"< 50%","window":"未來 4 季","source":"季報","last_status":"ok"},{"metric":"CPO 設備量產認列","bear_threshold":"2027Q2 前未見量產出貨","window":"2026Q4–2027Q2","source":"法說會","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤ 900 元且近 3 個月月營收年增皆為正","exec_line":"現價不追；900 元以下且營收未轉弱才重跑研究評估首倉；持有者以合約負債連 2 季下滑為減碼線、台積電擴產轉向為清倉線","holding_cap":"首倉 ≤2%，須有 −55% 以上回撤的心理準備"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把客戶擴產高峰的成長當成可延續的結構成長，給 TTM 79 倍；2023 年營收年減 46%、EPS 年減 71% 的紀錄顯示這段成長會隨擴產消化中斷，現價等於押 CPO 大成功","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 900 元以下（約 FY2027E Base EPS 的 24 倍）且月營收年增未轉負；或 2027Q1 法說確認 CPO 量產認列後重估","qc48_result":"fail","qc48_note":"Bull 的每股盈餘路徑只有 CPO 占營收比例的敘事，沒有出貨量乘單價的算式，成長跑道也押在尚未兌現、且已被下修過的 CPO 預估上，所以 Bull 依據不成立。"},"thesis":{"H":[{"id":"H1","text":"先進封裝擴產帶動營收翻倍並延續到 2027 年上半年","2y":"2026 年營收約 100 億元、2027 年再成長兩成以上","5y":null,"10y":null,"threshold":"2027 上半年單季營收 ≥ 30 億元，季末合約負債維持 ≥ 2 億元","source":"公開資訊觀測站月營收、季報、法說會","drift_rule":"兩年期：營收較路徑連 2 季偏離 ≥5% 視為削弱、連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"矽光子（CPO）與面板級封裝成為第二條成長曲線","2y":null,"5y":"2028 年 CPO 營收占比 ≥ 30%","10y":null,"threshold":"2027 年 CPO 相關營收 ≥ 15 億元","source":"法說會、外資報告、月營收","drift_rule":"五年期：連 4 季偏離 ≥5% 削弱、連 6 季 ≥10% 反轉"},{"id":"H3","text":"點膠製程綁定帶來的定價力在短缺收斂後仍能維持","2y":null,"5y":"毛利率維持 50% 以上、營業利益率領先同業最高者 5 個百分點以上","10y":null,"threshold":"TTM 毛利率 ≥ 50%","source":"本公司與同業季報","drift_rule":"五年期：連 4 季偏離 ≥5% 削弱、連 6 季 ≥10% 反轉"}],"R":[{"id":"R1","text":"CPO 專案遞延，或設備產出效率提升使機台需求下修","h_ref":"H2","clock":"⚡","threshold":"2027Q1 法說仍未確認 CPO 量產認列","evidence_refs":["end_markets#4","capital_markets_pricing#0"]},{"id":"R2","text":"CoWoS 短缺收斂後客戶擴產消化，2027 下半年起訂單空窗","h_ref":"H1","clock":"🔥","threshold":"合約負債連 2 季下滑且月營收年增轉負","evidence_refs":["supply_demand_durability#3"]},{"id":"R3","text":"兩大客戶約占八成，導入第二供應商或壓價","h_ref":"H3","clock":"🔥","threshold":"TTM 毛利率 < 50%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"id":"R4","text":"股本持續擴張稀釋每股價值","h_ref":"H3","clock":"🐢","threshold":"稀釋股數年增 > 2%","evidence_refs":[]}],"single_thing":{"description":"台積電宣布 2027 年先進封裝擴產放緩或資本支出年減","why_fatal":"封測設備占營收八到九成且客戶集中，現價 79 倍 TTM 本益比假設擴產至少延續到 2028 年；擴產一停，營收可能像 2023 年一樣年減四成以上，倍數同時壓縮","if_happens":"Bear 機率升至 45% 以上；未持有不進場，持有者減碼一半，合約負債同步下滑則清倉","how_monitor":"台積電每季法說資本支出指引、萬潤月營收年增與季末合約負債","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":15.38,"FY2026E":30,"FY2027E":38,"FY2028E":43},"fy_end_month":12,"eps_basis":"稀釋 EPS（GAAP）；事實表未涵蓋賣方共識，三年錨以本判斷 Base 路徑代填，非共識"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026Q3 財報與 10 月月營收","impact":"中","watch":"毛利率是否守 54%、淨利與營業利益差距（業外成分）"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"CPO 耦合設備首批交機","impact":"高","watch":"法說或月營收是否確認交機"},{"date":"2027-01","date_precision":"month","type":"capacity","event":"台積電 2027 年資本支出與先進封裝擴產指引","impact":"高","watch":"CoWoS 擴產口徑是否放緩"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"CPO 設備放量（2027Q1）","impact":"高","watch":"2027Q1 平均月營收 ≥ 12 億元"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"面板級封裝量產設備拉貨起點","impact":"中","watch":"面板級點膠設備是否由驗證轉量產訂單"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把客戶擴產高峰的成長當成可延續的結構成長，給 TTM 79 倍；2023 年營收年減 46%、EPS 年減 71% 的紀錄顯示這段成長會隨擴產消化中斷，現價等於押 CPO 大成功"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='→', week26=74.31, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 的每股盈餘路徑只有 CPO 占營收比例的敘事，沒有出貨量乘單價的算式，成長跑道也押在尚未兌現、且已被下修過的 CPO 預估上，所以 Bull 依據不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":["QC-48"]}}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
