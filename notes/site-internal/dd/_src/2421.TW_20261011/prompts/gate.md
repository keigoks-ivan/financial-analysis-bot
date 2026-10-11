你是 DD 管線 v20 的判斷層閘（gate），標的 2421.TW（20261011）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（33 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP 合併）＝5418.6 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（轉錄 MOPS 合併財報）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝31.25 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（毛利 1,693.4 ÷ 營收 5,418.6）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝15.44 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（營業利益 836.6 百萬 ÷ 營收 5,418.6 百萬）；玩股網 Q1 營業利益 788.4 百萬與 yfinance 783.2 百萬略有差異（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無
- `f_peer_2421_tw_gross_margin_pct`（q2_moat）｜2421.TW 毛利率＝31.89 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2421.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2421_tw_operating_margin_pct`（q2_moat）｜2421.TW 營業利益率＝15.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2421.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_gross_margin_pct`（q2_moat）｜3017.TW 毛利率＝28.87 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_operating_margin_pct`（q2_moat）｜3017.TW 營業利益率＝23.56 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_gross_margin_pct`（q2_moat）｜3324.TWO 毛利率＝27.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-07 date｜期間與口徑：2026-08-07／距今 46 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-07）
- `f_peer_2421_tw_fcf_margin_pct`（q2_moat）｜2421.TW FCF 利潤率＝5.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2421.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_fcf_margin_pct`（q2_moat）｜3017.TW FCF 利潤率＝24.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_operating_margin_pct`（q2_moat）｜3324.TWO 營業利益率＝15.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_fcf_margin_pct`（q2_moat）｜3324.TWO FCF 利潤率＝-13.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3653_tw_gross_margin_pct`（q2_moat）｜3653.TW 毛利率＝42.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3653.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3653_tw_operating_margin_pct`（q2_moat）｜3653.TW 營業利益率＝33.06 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3653.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3653_tw_fcf_margin_pct`（q2_moat）｜3653.TW FCF 利潤率＝15.18 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3653.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6230_tw_gross_margin_pct`（q2_moat）｜6230.TW 毛利率＝15.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6230.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6230_tw_operating_margin_pct`（q2_moat）｜6230.TW 營業利益率＝-0.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6230.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6230_tw_fcf_margin_pct`（q2_moat）｜6230.TW FCF 利潤率＝-4.08 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6230.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi3_eps`（q4_capital）｜稀釋 EPS＝2.41 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt；technews 報 2.42 元（四捨五入差）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無（2421.TW 不在最新 EPS 估值快照）
- `f_kpi4`（q4_capital）｜自由現金流（營業現金流−資本支出）＝208.2 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（營業現金流 611.8 − 資本支出 403.7 百萬）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：不適用
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝3.119 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝168.0 USD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝17.54 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝82.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝82.2 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝2.37 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.09 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝27.24 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-08（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.7｜期間與口徑：2026-10-08（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ma_w104`（q5_valuation）｜104 週均線＝123.71 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）
- `f_ma_w250`（q5_valuation）｜250 週均線＝91.37 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）

### findings_digest 中方向為負或來源衝突的條目（1 條）
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：AI 伺服器 GB200 採液冷架構，CPU/GPU 用水冷板，其餘部分仍以氣冷風扇為主（混合式，部分取代）
  - 來源：搜尋結果引述 2024 年研究報告（cmoney 筆記）（as_of 2024-12-31）｜affects：moat_trend、decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":387.0,"bear_5y_price":83.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":20.8,"ev5y_pct":26.8,"irr_base_pct":3.9,"asym_ratio":2.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.75,"pe":15.63,"basis":"FY1：法人 2026 年 EPS 區間 10.6–10.9 元取中值，168 元÷10.75 元；終端倍數同以當年度 EPS 為分母"},"eps":{"bull":[13.2,15.8,17.8,19.8,21.5],"base":[12.0,13.0,12.3,13.5,14.5],"bear":[9.6,7.6,7.0,7.6,8.3]},"pe":{"bull":18,"base":14,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":3.119,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | none | 0 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | none | 0 | 4 |
| geo_supply_chain | none | 0 | 4 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | none | 0 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：建準 2421 最大客戶 第二供應商 OR 自製 散熱 2026；Sunon 2421.TW customer concentration liquid cooling second source 2026
- **customer_concentration_credit**（none）：建準 2421 主要客戶 營收比重 客戶集中 2026；Sunon 2421.TW top customer revenue concentration AI server cooling 2026
- **regulatory_antitrust**（none）：2421.TW 建準 antitrust OR monopoly investigation 2026；建準電機 Sunon regulation OR regulatory scrutiny cooling fan 2026；2421.TW 建準 DOJ OR FTC OR EU competition 2026
- **reg_tariff_export**（none）：建準 2421 關稅 2026 散熱風扇 美國 出口；Sunon cooling fan tariff section 232 2026；建準 越南 中國 產能 關稅 貿易限制 2026；thermal management cooling tariff exposure supply chain Taiwan 2026
- **geo_supply_chain**（none）：建準 2421 Sunon manufacturing location geopolitical risk 2026；建準電機 2421 越南 中國 生產基地 產能 2026；Sunon cooling fan supply chain concentration risk 2026；建準 散熱風扇 生產基地 中國 越南 關稅 地緣
- **channel_business_model_shift**（none）：建準 2421 液冷 散熱 通路 商業模式 轉型 2026；Sunon 建準 2421.TW business model transition liquid cooling data center 2026
- **major_events**（none）：建準電機 2421 併購 收購 2026；建準 2421 Sunon lawsuit OR 訴訟 OR 集體訴訟；建準 2421 重大訊息 調查 OR 重編 OR 裁罰 OR 召回 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2421.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"建準電機"},"oneliner":"建準靠伺服器風扇把毛利率推上近 32%，但液冷轉型落後奇鋐、雙鴻；168 元約為法人今年 EPS 的 15.6 倍，Base 五年年化約 7%，液冷營收證據出來前不追。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 伺服器、筆電與車用散熱風扇的錢，錢卡在高轉速伺服器風扇的平台設計認證這一節；散熱價值正往水冷板與 CDU 移，建準在新節點還沒站穩。","reasoning":"營收結構（2026 年 3 月口徑，可能非最新）：伺服器網通與 AI 48%、筆電與 PC 22%、車用 12%、工業與醫療 10%、其他 8%。最新一季（2026 年第二季，8 月 7 日公告）營收 5,418.6 百萬元、毛利率 31.25%、營業利益率 15.44%。毛利率高於奇鋐 28.87% 與雙鴻 27.85%，但 TTM 營益率 15.85% 低於奇鋐 23.56%。產業時鐘判擴張期，依據是出貨量而非股價：2026 前 8 月營收 145.32 億元、年增 21.08%，7 月年增 31.65%。供需持久性：週期性將反轉的風險中等，需求綁在雲端業者 AI 資本支出，TrendForce 仍預估 2027 年 GPU 機櫃出貨增逾 30%，但風扇的單位含量正被液冷壓縮。單點依賴：前一至兩大客戶占比與供應商集中度事實表未涵蓋，無法判定是護城河證據還是集中度風險，列資料缺口。最新一季逐字稿缺，管理層說法只能用法說摘要與媒體轉述。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_peer_2421_tw_gross_margin_pct","f_peer_2421_tw_operating_margin_pct","f_peer_3017_tw_gross_margin_pct","f_peer_3017_tw_operating_margin_pct","f_peer_3324_two_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"按件計價的硬體零組件出貨，沒有經常性合約；伺服器網通與 AI 約占 48%（2026 年 3 月口徑，原始出處未確認），需求跟著雲端業者資本支出走","unit_econ_note":"毛利率 FY2022 22.55%→TTM 31.89%、營益率 7.96%→15.85%；研發占營收 6.05% 高於奇鋐 3.36%，與奇鋐的營益率差距主要在費用端而非毛利","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收隨 PC 與 AI 伺服器週期擺動：FY2023 年減 8.17%、FY2025 年增 27.72%；毛利率隨產品組合與稼動率從 22.55% 升到 31.89%，高點落在 AI 週期內"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性：TrendForce（2026-08）預估 2027 年 GPU 機櫃出貨仍年增逾 30%、AI 晶片液冷滲透率近 60%，Kyber NVL144 可能延後；需求綁雲端業者 AI 資本支出，消化期來時會反轉","bargaining":{"up":"上游為馬達、IC、塑料等通用零件，供應商集中度事實表未涵蓋","down":"下游為伺服器 ODM 與雲端業者，買方集中、每代平台重開設計案；前幾大客戶占比事實表未涵蓋","geo":"菲律賓新廠擴產（2026 資本支出上調至 15 億元以上）分散產地；關稅與出口管制查無資料"},"profit_pool_dir":"散熱利潤池往水冷板、CDU 與液冷一條龍廠商移動；建準風扇段利益率創高，液冷段份額未證","tam_table":[{"item":"AI 晶片液冷滲透率 2026E","value":"53%（TrendForce，2026-08）"},{"item":"AI 晶片液冷滲透率 2027E","value":"接近 60%（TrendForce）"},{"item":"GPU 機櫃出貨 2027E 年增","value":"逾 30%（TrendForce；Kyber NVL144 可能延後）"},{"item":"建準 AI 伺服器風扇市占","value":"約 30%（報導未標年份）；2025 年 3 月分析稱全球第二大散熱風扇廠"},{"item":"風扇專屬 TAM／SAM 與段 CAGR","value":"事實表未涵蓋"},{"item":"散熱營業利益池占比 5 年前→現","value":"事實表未涵蓋，利潤池流出幅度無法量化"}]}}},"q2_moat":{"verdict":"→ 穩定：風扇段利益率續創新高，液冷段落後奇鋐與雙鴻，兩股力量相抵","reasoning":"機制是高轉速伺服器風扇須通過 NVIDIA 參考設計與 ODM 散熱驗證，換供應商要重新驗證，但每個平台世代都重開設計案，轉換成本只在世代內有效。可證方向：對最強同業奇鋐，毛利率高 3.0pp、營益率低 7.7pp、FCF 利潤率低 18.5pp；ROIC 對照所需的投入資本事實表未涵蓋，改用利益率軸。份額：AI 伺服器風扇市占約 30% 的報導無年份，份額消長無直接證據，最大客戶份額方向也查無。執行面 6 分：風扇段創新高，但液冷落後雙鴻、奇鋐，TTM FCF 利潤率只有 5.65%。定價面 6 分：毛利率是直接同業最高，但查無漲價證據，液冷段議價未建立，摩根士丹利因液冷貢獻待放大降目標價。報酬持續期：當期 ROIC 無法計算；四個檢查點三黃一綠，需求還在、解法在換。","fact_refs":["f_peer_2421_tw_gross_margin_pct","f_peer_2421_tw_operating_margin_pct","f_peer_2421_tw_fcf_margin_pct","f_peer_3017_tw_gross_margin_pct","f_peer_3017_tw_operating_margin_pct","f_peer_3017_tw_fcf_margin_pct","f_peer_3324_two_gross_margin_pct","f_peer_3324_two_operating_margin_pct","f_peer_3324_two_fcf_margin_pct","f_peer_3653_tw_gross_margin_pct","f_peer_3653_tw_operating_margin_pct","f_peer_3653_tw_fcf_margin_pct","f_peer_6230_tw_gross_margin_pct","f_peer_6230_tw_operating_margin_pct","f_peer_6230_tw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"高轉速伺服器風扇須通過 NVIDIA 參考設計與 ODM 散熱驗證，加上磁浮馬達技術；轉換成本只在單一平台世代內有效，每代重開設計案","execution":6,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行面穩定：風扇段創新高（毛利率 FY2022 22.55%→TTM 31.89%、營益率 7.96%→15.85%），但液冷進度落後雙鴻、奇鋐，一升一落；定價面穩定：毛利率高於直接同業，但查無漲價或份額擴張證據，摩根士丹利 2026 年 4 月因液冷貢獻待放大把目標價由 175 降到 165 元；AI 伺服器風扇市占約 30% 的報導無年份，份額方向無直接證據","competitor_notes":[{"name":"3017.TW 奇鋐","strategy_note":"液冷一條龍領先者，營益率 23.56%、FCF 利潤率 24.1% 都遠高於建準，是建準液冷轉型最直接的對手"},{"name":"3324.TWO 雙鴻","strategy_note":"液冷擴產期以現金換份額，FCF 利潤率 −13.66%、毛利率 27.85% 低於建準，但液冷進度領先建準"},{"name":"3653.TW 健策","strategy_note":"產品線不同，不是風扇直接對手；毛利率 42.63%、營益率 33.06%，只作散熱零組件利益率的上緣參考"},{"name":"6230.TW 尼得科超眾","strategy_note":"營益率 −0.88%、FCF 利潤率 −4.08%，散熱模組的落後者賺不到錢，說明這行份額落後的代價"}],"threats":[{"level":"🔴","text":"液冷替代：GB200 的 CPU／GPU 已改用水冷板，風扇只負責其餘元件；AI 晶片液冷滲透率 2027 年近 60%，每機櫃風扇含量被壓縮。目前是部分替代（氣液混合），尚未到全面架構替代","p":"35%","evidence_refs":["substitute_technology#0","supply_demand_durability#1","substitute_technology#2"]},{"level":"🟡","text":"奇鋐、雙鴻在液冷段先行，水冷板與 CDU 設計案先被拿走，建準液冷 2026 年第三季小量送驗、2027 年才放量","p":"40%","evidence_refs":["end_markets#2"]},{"level":"🟡","text":"台達、尼得科等大型馬達廠在伺服器風扇點對點競爭；具名設計定案與新進者搶單的證據查無","p":"20%","evidence_refs":["competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知：營益率 15.85% 屬中高，投入資本事實表未涵蓋，周轉率與當期 ROIC 無法計算","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心、決策者是 NVIDIA 參考設計與 ODM 散熱工程、付款者是雲端業者，三環都成立，散熱是不能延後的需求。但客戶要解決的是發熱，風扇只是目前解法之一：GB200 的 CPU／GPU 已改水冷板，液冷滲透率 2027 年近 60%，需求在、解法在換"},{"item":"決策層級","level":"🟡","text":"替代性在每個平台世代的散熱設計案衡量，不在風扇這個品類；公司自述為 GB200／GB300 推薦供應商，但每代平台都重開設計案，轉換成本只在世代內有效。流失率、重新認證週期等代理變數事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"機櫃價值大頭在 GPU，散熱環節內的價值正往水冷板與 CDU 移；建準毛利率 31.89% 高於奇鋐、雙鴻，但營益率 15.85% 低於奇鋐 23.56%，在散熱利潤池分到的比例不是最大；採購收斂到液冷一條龍廠商時，建準議價會轉弱"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的零組件，不是民生必需品，沒有漲價的社會或政治上限，也不依賴監管授權"}],"roiic":"事實表未涵蓋（投入資本、折舊攤銷、營運資金變動皆缺），無法推導","reinvest_rate":"盈餘保留率約 34%：TTM 殖利率 3.119%×168 元＝每股股息約 5.24 元，對 FY2025 EPS 7.89 元配發約 66%；資本支出口徑的再投資率事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；增量 ROIC 缺，天花板留空，情境樹不以內生上界替 Base 成長背書，Base EPS 年化約 6% 只靠產業量能與利益率持平"}}}},"q3_growth":{"verdict":"🟡 中：風扇是成熟產品，液冷這條第二曲線在產業層已經成形，建準的份額還沒有營收證據","reasoning":"成長以量為主（AI 機櫃出貨），加上高轉速風扇與風扇牆的組合升級、菲律賓新廠產能，沒有併購與回購貢獻。三年共識：只有法人 FY2026E 10.6–10.9 元（較 FY2025 的 7.89 元增約 34–38%），FY2027E、FY2028E 事實表未涵蓋，三年 CAGR 不可得；內生天花板也因增量 ROIC 缺而不可得，缺口無法歸因，長期信心上限為中。FY2022–FY2025 EPS 年化約 22%、營收年化約 10%，差 12pp 來自利益率擴張，不可外推。Runway：AI 晶片液冷滲透率 2026 年已達 53%，產業層的液冷不是早期市場；建準液冷營收占比未揭露，第二曲線存在但份額沒有證據，所以判中不判寬。衰退信號亮兩項：EPS 成長高於營收成長逾 5pp、液冷壓縮風扇單位含量。FCF÷淨利 FY2024 為 0.74、FY2025 回到 1.07，未連兩年，列觀察。","fact_refs":["f_kpi0_gaap","f_kpi3_eps","f_peer_2421_tw_operating_margin_pct","f_peer_2421_tw_fcf_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量（AI 伺服器機櫃出貨）為主，加上組合（高轉速伺服器風扇、風扇牆）與產能（菲律賓新廠）；無併購與回購貢獻","runway_years":"約 5 年（中等折扣）：以液冷第二曲線為前提，建準液冷營收占比未揭露，滲透進度無法量測","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 不可得，內生天花板留空；FY2022–FY2025 自由現金流每年為正（11.1–23.2 億元），成長期間未出現現金缺口，只能作為自籌成長的旁證","segments":[{"item":"伺服器網通與 AI","value":"48%"},{"item":"IT（筆電／PC）","value":"22%"},{"item":"車用電子","value":"12%"},{"item":"工業與醫療","value":"10%"},{"item":"其他","value":"8%（以上為 2026 年 3 月口徑，原始出處未確認，可能非最新）"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q2 2026 毛利率 31.25%，TTM 31.89% 高於 FY2025 31.06%；去年同季值事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"份額消長無直接證據，屬資料缺口而非否證"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"查無提價紀錄"},{"signal":"EPS 成長顯著高於營收成長（差逾 5pp）","lit":true,"note":"FY2022–FY2025 EPS 年化約 22%、營收年化約 10%，差約 12pp，來自利益率擴張"},{"signal":"FCF÷淨利連 2 年低於 0.75","lit":false,"note":"FY2024 0.74、FY2025 1.07，未連兩年；TTM FCF 利潤率 5.65% 偏弱，列觀察"},{"signal":"SBC 占營收逾 5% 且逐年上升","lit":false,"note":"SBC 事實表未涵蓋；稀釋股數三年增 8.6%，來源待查"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"note":"水冷板接手 CPU／GPU 散熱，每機櫃風扇含量下降"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"P/S 與 EV/S 在 4 個年度端點最高，方向相反"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"維持與擴張資本支出拆分事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"菲律賓新廠擴產中，營收連兩年成長"}],"trap_rating":"價值陷阱風險中、長期成長性中（亮兩項）"}}},"q4_capital":{"verdict":"資本主要用在現金股利（配發約六成五）與菲律賓擴產；沒有併購與回購紀錄，股數三年增 8.6% 的來源待查，配置紀律證據不足以給高評價","reasoning":"現金轉換：FCF÷淨利 FY2022 1.61、FY2023 1.39、FY2024 0.74、FY2025 1.07；TTM FCF 利潤率 5.65%，Q2 營業現金流 611.8 百萬元、資本支出 403.7 百萬元、FCF 208.2 百萬元，2026 資本支出上調至 15 億元以上投入菲律賓新廠。股東回饋：TTM 殖利率 3.119%，換算每股股息約 5.24 元，對 FY2025 EPS 7.89 元配發約 66%。併購與回購：證據包查無。股數：以淨利÷稀釋 EPS 推算，FY2022 約 2.53 億股、FY2025 約 2.75 億股，三年增 8.6%、年化約 2.8%，來源（員工酬勞、可轉債或盈餘轉增資）事實表未涵蓋，無法判斷是否屬經濟性稀釋。SBC 占營收、債務到期與利率、現金去向四分事實表未涵蓋。","fact_refs":["f_kpi4","f_kpi3_eps","f_dividend_yield_ttm","f_peer_2421_tw_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"證據包查無併購紀錄（重大併購軸查無）"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表與證據包查無回購紀錄"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"以淨利÷稀釋 EPS 推算稀釋股數 FY2022 約 2.53 億股→FY2025 約 2.75 億股，年化約 2.8%；股權激勵金額與股數增加來源事實表未涵蓋，無法判定是否超過 1.5%／年的稀釋門檻"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長沒有靠併購撐，回饋以現金股利為主；分年股利、回購與增資明細事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價 168 元要求今年 EPS 做到法人的 10.6 元以上、明年再成長，且市場繼續給 15 倍以上本益比；風扇段做得到，液冷段沒有證據，只信一半","reasoning":"現價 168 元（事實表單位標為 USD，實為新台幣，與 EPS 同幣別，倍數自洽）。trailing 本益比 17.54 倍，在近 4 個年度端點中排第 82 分位；P/S 2.37 倍、EV/S 2.09 倍都是 4 個端點最高。以法人 FY2026E 中值 10.75 元計，前瞻本益比約 15.6 倍，和法人 8 月底在 179.5 元時算的 16.5–17 倍一致。賣方：4 位分析師全數買進，目標價均值 194 元（180–214），摩根士丹利 4 月中性、165 元。短期上檔取 Base FY2027E 12.0 元×15 倍＝180 元（+7.1%），中期取 Base 五年終值 14 倍×14.5 元＝203 元（+20.8%）。同業本益比事實表未涵蓋，不以產品線不同的健策當估值錨。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"前瞻本益比（法人 FY2026E 中值 10.75 元）為主，trailing 本益比與 P/S 的年度端點分布為輔","peers":{"expanded":false,"reason":"同業本益比事實表未涵蓋，只有利益率對照；健策產品線不同，不跨產品線當估值錨"},"fwd_pe":15.63,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比約 15.6 倍對年增兩成的營收不算貴，但分子是週期高檔利益率，營收倍數已在 4 年端點頂部；三年共識 EPS 事實表未涵蓋、PEG 不可得，五年分位也不可得（只有 4 個年度端點）。綜合判合理偏滿：不便宜，也沒到過熱","upside_short_pct":7.1,"upside_mid_pct":20.8,"denominator_disputed":false,"denominator_note":"分母用法人 FY2026E 中值 10.75 元；Q2 單季 2.41 元年化約 9.6 元，差距要靠下半年營收與利益率同時上升，屬程度差異，沒有一次性項目"}}},"q6_how_wrong":{"verdict":"最可能看錯在液冷份額：拿不下時利益率回到 FY2023–24 的 11–12%、本益比 10 倍，股價約 70–85 元；拿下時本份 Base 太保守","reasoning":"往下的故事見反證紀錄第一條：液冷份額拿不下與 AI 資本支出消化同時發生，EPS 回到 7–8 元。Max DD 範圍 −35% 至 −60% 由情境推導，歷史最大回撤事實表未涵蓋。成長熄火壓力測試：以 Base FY2028E 13.0 元計，成長降到 15%／10%／5% 對應本益比約 17／14／10 倍，股價 221／182／130 元，前兩個不跌破現價，第三個跌約 23%。往上：若建準在 Vera Rubin 世代拿下水冷板與 CDU，Base 年化約 6% 的 EPS 成長明顯太低。訴訟、監管、重大事件各軸查無紀錄。","fact_refs":["f_price_at_dd","f_ma_w104","f_ma_w250","f_peer_2421_tw_operating_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"價值陷阱風險中：EPS 成長靠利益率擴張、風扇含量受液冷壓縮兩項亮燈"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.75,"pe":15.63,"basis":"FY1：法人 2026 年 EPS 區間 10.6–10.9 元取中值，168 元÷10.75 元；終端倍數同以當年度 EPS 為分母"},"eps":{"bull":[13.2,15.8,17.8,19.8,21.5],"base":[12.0,13.0,12.3,13.5,14.5],"bear":[9.6,7.6,7.0,7.6,8.3]},"pe":{"bull":18,"base":14,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":3.1,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"max_dd":{"lo":-60,"hi":-35,"basis":"下緣 −60%：Bear 谷底 FY2029E EPS 7.0 元×熄火倍數 10 倍＝70 元（−58%），再留約 2pp 情緒超跌；上緣 −35%：AI 資本支出短暫消化但液冷有進展，股價跌破 104 週均線 123.7 元（−26%）到約 110 元（−35%）。歷史最大回撤事實表未涵蓋，範圍由情境推導；超過 −50% 屬深回撤，論點未破前不因波動砍倉","trigger_time":null},"basis":{"bull":"建準在 Vera Rubin 世代拿下水冷板與 CDU 訂單，液冷占比 2028 年達兩成以上，風扇在混合架構中續成長；營益率升到 17% 以上，終端 18 倍約為現在的 trailing 本益比","base":"風扇段隨 AI 機櫃成長到 2028 年，液冷小幅貢獻；2029 年 AI 資本支出消化一年後恢復，EPS 五年年化約 6%；終端 14 倍＝成長降至約 10% 的中段倍數，低於現在前瞻 15.6 倍。同業現值本益比事實表未涵蓋，以自身 trailing 17.54 倍與法人前瞻 16.5–17 倍為對照","bear":"液冷份額拿不下、風扇單位含量被壓，加上 AI 資本支出消化，營益率回到 FY2023–24 的 11–12%，EPS 回到 7–8 元；終端 10 倍＝成長降至 5% 的熄火倍數。機率 30% 依據：液冷落後同業有多方來源，公司端說法未附營收數字，不採信其結構性樂觀"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"GB200 的 CPU／GPU 已改水冷板，風扇只負責其餘元件；建準液冷進度落後雙鴻、奇鋐，液冷產品 2026 年第三季才小量送驗、2027 年放量；摩根士丹利 4 月因液冷貢獻待放大把目標價由 175 降至 165 元","assumption":"氣液混合仍是未來數年主流，建準能在 Vera Rubin 世代拿下水冷板或 CDU 的量產訂單","consequence":"液冷拿不下時，AI 段只剩風扇且單位含量被壓，EPS 回到 7–8 元、本益比 10 倍，股價約 70–85 元，五年虧損約一半","ruling":"採納為 Bear 主路徑，機率 30%；與唯一致命事件是同一條故事，兩者一致","watch":"法說揭露的液冷營收占比；單季毛利率是否守在 29% 以上","evidence_refs":["substitute_technology#0","end_markets#2","supply_demand_durability#0"],"fact_refs":["f_peer_2421_tw_gross_margin_pct","f_peer_3017_tw_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"TTM 自由現金流利潤率 5.65%，FY2025 為 12.4%；Q2 營業現金流 611.8 百萬元中 403.7 百萬元用於資本支出；2026 資本支出上調至 15 億元以上；稀釋股數 FY2022 約 2.53 億股、FY2025 約 2.75 億股，三年增 8.6%","assumption":"液冷放量後利益率不被拉低，擴產回收期合理，股數不再增加","consequence":"營收成長但每股自由現金流不增：液冷整合方案利益率可能低於高階風扇，擴產占用現金，股數年增約 3%，每股價值成長落後營收","ruling":"部分採納：FCF 轉換率與股數變化是本份最大資料缺口，Base 情境 EPS 年化只給約 6%，不給液冷放量的利益率加分","watch":"年度 FCF÷淨利是否回到 0.8 以上；稀釋股數年增是否壓到 1.5% 以下","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_kpi4","f_peer_2421_tw_fcf_margin_pct","f_kpi3_eps"]},{"view":"價格已反映太多","evidence":"P/S 2.37 倍、EV/S 2.09 倍都是近 4 個年度端點最高，trailing 本益比 17.54 倍在第 82 分位；同期毛利率 31.89%、營益率 15.85% 也在最高，等於用高檔倍數買高檔利益率","assumption":"利益率在 AI 週期後仍能維持 FY2025 的水準","consequence":"利益率回到 FY2023–24 的 11–12% 且倍數回到中段，股價下修 30–40%","ruling":"部分採納：以法人 FY2026E 計 15.6 倍並不極端，但營收倍數在頂端；Base 終端倍數取 14 倍，不給再評價","watch":"P/S 與營益率是否同步回落；法人 FY2026E 是否在第三季財報後下修","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_ps_current","f_ps_percentile","f_pe_current","f_pe_percentile","f_ev_s_current","f_ev_s_percentile"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 168.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=168.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"液冷轉型進度","cause":null,"prior_field":null,"side_a":"公司端：氣液混合設計未來數年仍是主流，建準為 GB200／GB300 推薦供應商；水冷板預計第四季放量，2026 資本支出上調至 15 億元以上","side_b":"外部：液冷進度落後雙鴻、奇鋐，另一資料稱液冷 2026 年第三季小量送驗、2027 年放量；摩根士丹利因液冷貢獻待放大降目標價至 165 元；沒有液冷營收占比數字","ruling":"可調和（時程與幅度差異）。採外部側為基準：公司說法沒有附營收數字，推薦供應商身分屬公司自述；液冷營收占比揭露前，Base 不計液冷份額","evidence_level":"雙方都是法說摘要與媒體轉述，非逐字原文；外部側有券商與產業研究兩個獨立來源","settle_metric":"法說揭露的液冷營收占比；Vera Rubin 世代水冷板或 CDU 量產出貨","if_then":["若 2027 年第二季前法說揭露液冷營收占比 ≥10% 且單季毛利率 ≥29%，重跑本份，通過後首倉 3%","反向：若 2027-06-30 前仍無量產出貨證據，持有者清倉，未持有者移出觀察並把 Bear 機率上調至 40% 重跑"],"evidence_refs":["end_markets#2","substitute_technology#2","supply_demand_durability#0","capital_markets_pricing#2"]},{"axis":"法人今年 EPS 與實際跑速","cause":null,"prior_field":null,"side_a":"法人預估 2026 全年 EPS 10.6–10.9 元（8 月底），4 位分析師全數買進、目標價均值 194 元","side_b":"Q2 單季 EPS 2.41 元，年化約 9.6 元；7–8 月營收月均約 20.5 億元，比 Q2 月均約 18.1 億元高約 13%，營收面只補得了一部分，其餘要靠下半年利益率再擴張","ruling":"可調和（程度差異）。本份把 10.75 元當上緣，不在其上再加成長；賣方目標價全距 180–214 元，最高÷最低約 1.2 倍，分歧小、方向比本份樂觀，市場假設是風扇段的高檔利益率可延續","evidence_level":"法人預估為媒體轉述；Q2 EPS 與月營收為已實現數字","settle_metric":"2026 年第三季單季 EPS 與毛利率","if_then":["若第三季單季 EPS ≥2.8 元且毛利率 ≥31%，上調 Base 2027 年 EPS，仍等液冷證據","反向：若第三季單季 EPS <2.5 元，法人全年估值須下修，Bear 機率上調至 35% 重跑"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#0","end_markets#0"]},{"axis":"觀望或現在就買","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：前 8 月營收年增 21%、液冷滲透率 2027 年近 60%、GPU 機櫃出貨仍增逾 30%；以法人 FY2026E 計本益比約 15.6 倍、殖利率 3.1%，毛利率高於奇鋐與雙鴻","side_b":"Base 五年年化報酬約 7%（股價約 3.9%＋股息 3.1%），低於 8% 的及格線；液冷份額沒有營收證據，Bear 情境下跌約一半","ruling":"選觀望。約束只有一條：液冷份額沒有證據。這條被否定（液冷營收占比揭露達一成，或量產出貨確認）就重跑；股價本身不是約束","evidence_level":"Base 報酬為本份情境推導；液冷份額缺口有券商與媒體兩方來源","settle_metric":"液冷營收占比或 Vera Rubin 世代量產出貨確認","if_then":["若液冷營收占比 ≥10% 揭露，重跑本份，Bull 機率可上調至 35%，通過後首倉 3%","價格先走、證據未到：股價先漲過 194 元而液冷證據未到，不追","價格先走、基本面無損：股價跌到 130 元以下而月營收年增仍 ≥15%，Base 年化回到約 13%，重跑本份評估分批反買"],"evidence_refs":["end_markets#0","supply_demand_durability#1","end_markets#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：TrendForce 預估 AI 晶片液冷滲透率 2026 年 53%、2027 年近 60%，GPU 機櫃出貨 2027 年仍年增逾 30%；摩根士丹利認為液冷需求延續到 2027 年","side_b":"其他結構變數（替代技術）：水冷板接手 CPU／GPU 散熱，風扇單位含量下降。競爭面：奇鋐、雙鴻在液冷領先，台達、尼得科的具名搶單證據查無","ruling":"雙向拉鋸：需求面結構轉好，替代技術軸對風扇本業不利，淨效果取決於建準能否把風扇客戶帶進液冷產品","evidence_level":"產業研究與券商報告，皆為轉述","settle_metric":"風扇與液冷的產品別營收","if_then":["若 2027 年液冷滲透率升到 60% 時風扇相關營收仍年增，代表混合架構撐住，替代風險降級","反向：若 2027 年風扇相關營收年減，替代風險升為架構替代，Bear 機率上調至 40% 重跑"],"evidence_refs":["supply_demand_durability#1","substitute_technology#0","competitive_share_entrants#2","supply_demand_durability#0"]}],"triggers":[{"n":1,"text":"月營收年增維持兩位數，驗證 AI 機櫃帶動風扇出貨","type":"假設驗證","maps_to":"H1","metric":"月營收年增率（3 個月移動）","threshold":"≥15%","action":"論點維持；跌破 10% 連 2 個月改走第 6 條","source_freq":"公開資訊觀測站月營收，每月 10 日前","date":"2026-11-10","evidence_refs":["end_markets#0"]},{"n":2,"text":"液冷營收占比揭露並達一成，第二曲線成形","type":"假設驗證","maps_to":"H2","metric":"液冷產品營收占比","threshold":"2027 年底前 ≥10%，2028 年 ≥20%","action":"達標即重跑本份，評估首倉 3%","source_freq":"法說會，每季","date":"2027-12-31","evidence_refs":["end_markets#2"]},{"n":3,"text":"毛利率跌破 29% 連兩季，代表液冷替代與份額落後開始吃到風扇本業","type":"減碼","maps_to":"R2","metric":"單季毛利率（GAAP）","threshold":"<29% 連 2 季","action":"持有者減碼一半；未持有者撤回首倉條件","source_freq":"季報，每季","date":null,"evidence_refs":["substitute_technology#0"]},{"n":4,"text":"Single Thing：Vera Rubin 世代液冷量產出貨期限","type":"Single Thing","maps_to":"Single Thing","metric":"建準水冷板或 CDU 進入 Vera Rubin 世代機櫃量產出貨","threshold":"2027-06-30 前未見量產出貨證據","action":"持有者清倉；未持有者移出觀察，Bear 機率上調至 40% 重跑","source_freq":"法說會與公司公告，每季","date":"2027-06-30","evidence_refs":["end_markets#2","supply_demand_durability#0"]},{"n":5,"text":"重啟條件：液冷份額出現證據","type":"估值rearm","maps_to":"H2","metric":"液冷營收占比或量產出貨確認","threshold":"法說揭露液冷營收占比 ≥10%，或確認 Vera Rubin 世代水冷板或 CDU 已量產出貨","action":"重跑本份；通過後首倉 3%，下一季毛利率 ≥29% 再加到 5%","source_freq":"法說會，每季","date":null},{"n":6,"text":"出貨遞延：AI 專案受記憶體、PCB、晶片供應延後","type":"風險","maps_to":"R1","metric":"月營收年增率（3 個月移動）","threshold":"<10% 連 2 個月","action":"持有者減碼三分之一，凍結加碼到下一份季報","source_freq":"公開資訊觀測站月營收，每月","date":null,"evidence_refs":["end_markets#2"]},{"n":7,"text":"擴產吃現金：自由現金流長期低於淨利","type":"風險","maps_to":"R4","metric":"年度自由現金流÷淨利","threshold":"<0.75 連 2 年","action":"暫停加碼，Base 終端倍數下調 1 倍重跑","source_freq":"年報，每年","date":"2027-03-31","evidence_refs":["capital_markets_pricing#2"]},{"n":8,"text":"第三季財報複審：檢查法人全年 EPS 是否站得住（日期為推估，前一季於 8 月 7 日公告）","type":"複審日期","maps_to":"H3","metric":"2026 年第三季單季 EPS 與毛利率","threshold":"EPS ≥2.8 元且毛利率 ≥31% 為達標；EPS <2.5 元為不達標","action":"不達標時 Bear 機率上調至 35% 重跑；達標維持等液冷證據","source_freq":"季報","date":"2026-11-14"}],"kill_metrics":[{"metric":"單季毛利率（GAAP）","bear_threshold":"連 2 季低於 29%","window":"2026 年第三季至 2027 年第四季","source":"公開資訊觀測站季報","last_status":"ok"},{"metric":"月營收年增率（3 個月移動）","bear_threshold":"連 2 個月低於 10%","window":"2026-10 至 2027-12","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"Vera Rubin 世代水冷板或 CDU 量產出貨","bear_threshold":"2027-06-30 前未見量產出貨證據","window":"至 2027-06-30","source":"法說會、公司公告","last_status":"unknown"},{"metric":"年度自由現金流÷淨利","bear_threshold":"連 2 年低於 0.75","window":"FY2026–FY2027","source":"年報現金流量表","last_status":"warning"},{"metric":"TTM 營業利益率","bear_threshold":"低於 12% 且營收年增轉負","window":"2027–2029","source":"公開資訊觀測站季報","last_status":"ok"}],"action_conditions":{"rearm_trigger":"法說揭露液冷產品營收占比達一成以上，或確認 Vera Rubin 世代水冷板或 CDU 已量產出貨","exec_line":"重啟條件成立後先重跑本份；仍成立則首倉 3%，下一季毛利率守 29% 以上再加到 5%；條件未到前股價上漲不追，下跌只在基本面無損時重算","holding_cap":"首倉 3%，液冷證實後上限 5%；回撤區間 −35% 至 −60% 屬深回撤，須有心理準備"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場（4 位分析師全數買進、目標價均值 194 元）假設風扇段的高檔利益率可延續、液冷會順利接棒；本份認為液冷份額沒有營收證據，P/S 已在 4 年端點最高，市場把週期高點的利益率當成常態","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不追 168 元；等法說揭露液冷營收占比達一成，或 Vera Rubin 世代水冷板或 CDU 量產出貨確認後重跑","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場（4 位分析師全數買進、目標價均值 194 元）假設風扇段的高檔利益率可延續、液冷會順利接棒；本份認為液冷份額沒有營收證據，P/S 已在 4 年端點最高，市場把週期高點的利益率當成常態"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=27.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='不追 168 元；等法說揭露液冷營收占比達一成，或 Vera Rubin 世代水冷板或 CDU 量產出貨確認後重跑'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 伺服器與氣液混合散熱帶動風扇、風扇牆出貨，2026–2027 年營收維持雙位數成長","2y":"FY2026 營收年增 ≥18%（約 220 億元），FY2027 再增 ≥12%","5y":null,"10y":null,"threshold":"月營收 3 個月移動年增 ≥15%；FY2026 營收 ≥220 億元","source":"公開資訊觀測站月營收（每月 10 日前）與季報","drift_rule":"2 年期：TTM 營收偏離門檻路徑 ≥5% 連 2 季＝削弱，≥10% 連 3 季＝反轉"},{"id":"H2","text":"液冷產品（水冷板、CDU、Sidecar、水泵）在 Vera Rubin 世代量產，成為第二條成長曲線","2y":null,"5y":"液冷營收占比 2028 年 ≥20%、2030 年 ≥30%","10y":null,"threshold":"液冷營收占比 2027 年底 ≥10%、2028 年 ≥20%","source":"法說會產品別營收說明、年報","drift_rule":"5 年期：連 4 季偏離 ≥5%＝削弱，連 6 季偏離 ≥10%＝反轉；占比連 4 季未揭露視同削弱"},{"id":"H3","text":"產品組合升級抵銷液冷初期的低利益率，營業利益率守在歷史高檔附近","2y":null,"5y":"FY2026–FY2030 營業利益率平均 ≥14%、毛利率 ≥29%","10y":null,"threshold":"TTM 營業利益率 ≥14%；單季毛利率 ≥29%","source":"公開資訊觀測站季報","drift_rule":"5 年期：TTM 營業利益率連 4 季低於門檻 5% 以上（<13.3%）＝削弱，連 6 季低於 10% 以上（<12.6%）＝反轉"}],"R":[{"id":"R1","text":"AI 伺服器專案受記憶體、PCB、晶片供應延後，出貨遞延","h_ref":"H1","clock":"⚡","threshold":"月營收 3 個月移動年增 <10% 連 2 個月","evidence_refs":["end_markets#2"]},{"id":"R2","text":"液冷替代壓縮每機櫃風扇含量，而建準液冷份額落後，毛利率下滑","h_ref":"H2","clock":"🔥","threshold":"單季毛利率 <29% 連 2 季，或 2027 年底液冷營收占比仍 <10%","evidence_refs":["substitute_technology#0","end_markets#2","supply_demand_durability#0"]},{"id":"R3","text":"AI 資本支出進入消化期，營收轉負、利益率回到 FY2023–24 的 11–12%","h_ref":"H3","clock":"🐢","threshold":"TTM 營業利益率 <12% 且營收年增轉負","evidence_refs":["supply_demand_durability#2"]},{"id":"R4","text":"菲律賓新廠與液冷擴產吃掉現金，自由現金流長期低於淨利","h_ref":"H3","clock":"🔥","threshold":"年度自由現金流÷淨利 <0.75 連 2 年","evidence_refs":["capital_markets_pricing#2"]}],"single_thing":{"description":"2027 年 6 月底前，建準的水冷板或 CDU 沒有進入 NVIDIA Vera Rubin 世代機櫃的量產出貨","why_fatal":"AI 晶片液冷滲透率 2027 年近 60%，拿不到液冷訂單時建準在 AI 機櫃只剩風扇，且每櫃風扇含量被水冷板壓縮；EPS 路徑由 Base 落到 Bear（FY2031E 14.5→8.3 元），倍數同時由 14 倍降到 10 倍，是本份對終值影響最大的單一變數","if_happens":"持有者清倉；未持有者移出觀察，Bear 機率由 30% 上調至 40% 重跑","how_monitor":"每季法說的液冷營收占比與出貨說明、月營收是否出現液冷貢獻的跳升、菲律賓新廠稼動","probability":"35%（12–24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":7.89,"FY2026E":10.75,"FY2027E":null,"FY2028E":null},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS。FY2025A 取年報 7.89 元；FY2026E 取法人預估 10.6–10.9 元中值（MoneyWeekly，2026-08-31，家數未揭露）；FY2027E、FY2028E 共識事實表未涵蓋，留空不推估"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026 年第三季財報與法說會（日期為推估，前一季於 8 月 7 日公告）","impact":"高","watch":"單季 EPS 是否 ≥2.8 元、毛利率是否守 31%、液冷營收占比是否揭露"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"水冷板預計第四季放量（法說摘要）","impact":"高","watch":"11 月至隔年 1 月月營收是否出現液冷貢獻的跳升"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"2026 年全年財報與股利政策","impact":"中","watch":"全年 FCF÷淨利、稀釋股數變化、2027 年資本支出"},{"date":"2027-06","date_precision":"month","type":"product","event":"Vera Rubin 世代液冷量產出貨檢查點","impact":"高","watch":"水冷板或 CDU 是否已量產出貨"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
