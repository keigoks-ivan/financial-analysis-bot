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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP 合併）＝5418.6 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（轉錄 MOPS 合併財報）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝31.25 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（毛利 1,693.4 ÷ 營收 5,418.6）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝15.44 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（營業利益 836.6 百萬 ÷ 營收 5,418.6 百萬）；玩股網 Q1 營業利益 788.4 百萬與 yfinance 783.2 百萬略有差異（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-07 date｜期間與口徑：2026-08-07／距今 46 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-07）
- `f_peer_2421_tw_gross_margin_pct`（q2_moat）｜2421.TW 毛利率＝31.89 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2421.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2421_tw_operating_margin_pct`（q2_moat）｜2421.TW 營業利益率＝15.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2421.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2421_tw_fcf_margin_pct`（q2_moat）｜2421.TW FCF 利潤率＝5.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2421.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_gross_margin_pct`（q2_moat）｜3017.TW 毛利率＝28.87 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_operating_margin_pct`（q2_moat）｜3017.TW 營業利益率＝23.56 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_fcf_margin_pct`（q2_moat）｜3017.TW FCF 利潤率＝24.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_gross_margin_pct`（q2_moat）｜3324.TWO 毛利率＝27.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_operating_margin_pct`（q2_moat）｜3324.TWO 營業利益率＝15.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_fcf_margin_pct`（q2_moat）｜3324.TWO FCF 利潤率＝-13.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3653_tw_gross_margin_pct`（q2_moat）｜3653.TW 毛利率＝42.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3653.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3653_tw_operating_margin_pct`（q2_moat）｜3653.TW 營業利益率＝33.06 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3653.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6230_tw_operating_margin_pct`（q2_moat）｜6230.TW 營業利益率＝-0.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6230.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.85 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-09）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝13.4 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-09）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝16.28 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-09）
- `f_kpi3_eps`（q4_capital）｜稀釋 EPS＝2.41 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt；technews 報 2.42 元（四捨五入差）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無（2421.TW 不在最新 EPS 估值快照）
- `f_kpi4`（q4_capital）｜自由現金流（營業現金流−資本支出）＝208.2 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（營業現金流 611.8 − 資本支出 403.7 百萬）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：不適用
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝3.119 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝168.0 TWD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.48 x｜期間與口徑：2026-10-09／分母＝FY1 EPS 10.85，分子＝快照價 168.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-09）
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

### findings_digest 中方向為負或來源衝突的條目（1 條）
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：AI 伺服器 GB200 採液冷架構，CPU/GPU 用水冷板，其餘部分仍以氣冷風扇為主（混合式，部分取代）
  - 來源：搜尋結果引述 2024 年研究報告（cmoney 筆記）（as_of 2024-12-31）｜affects：moat_trend、decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":399.5,"bear_5y_price":95.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":35.4,"ev5y_pct":32.2,"irr_base_pct":6.3,"asym_ratio":2.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.85,"pe":15.48,"basis":"FY2026E 共識 EPS（會計年度已過四分之三），與終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[14.0,17.0,19.5,21.5,23.5],"base":[13.0,15.0,15.5,16.5,17.5],"bear":[12.0,9.0,8.5,9.0,9.5]},"pe":{"bull":17,"base":13,"bear":10},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":3.119,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"valuation_dependent":false}}
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
- **customer_second_source**（none）（沿用 2421.TW_20261011，0d）：建準 2421 最大客戶 第二供應商 OR 自製 散熱 2026；Sunon 2421.TW customer concentration liquid cooling second source 2026
- **customer_concentration_credit**（none）（沿用 2421.TW_20261011，0d）：建準 2421 主要客戶 營收比重 客戶集中 2026；Sunon 2421.TW top customer revenue concentration AI server cooling 2026
- **regulatory_antitrust**（none）（沿用 2421.TW_20261011，0d）：2421.TW 建準 antitrust OR monopoly investigation 2026；建準電機 Sunon regulation OR regulatory scrutiny cooling fan 2026；2421.TW 建準 DOJ OR FTC OR EU competition 2026
- **reg_tariff_export**（none）（沿用 2421.TW_20261011，0d）：建準 2421 關稅 2026 散熱風扇 美國 出口；Sunon cooling fan tariff section 232 2026；建準 越南 中國 產能 關稅 貿易限制 2026；thermal management cooling tariff exposure supply chain Taiwan 2026
- **geo_supply_chain**（none）（沿用 2421.TW_20261011，0d）：建準 2421 Sunon manufacturing location geopolitical risk 2026；建準電機 2421 越南 中國 生產基地 產能 2026；Sunon cooling fan supply chain concentration risk 2026；建準 散熱風扇 生產基地 中國 越南 關稅 地緣
- **channel_business_model_shift**（none）（沿用 2421.TW_20261011，0d）：建準 2421 液冷 散熱 通路 商業模式 轉型 2026；Sunon 建準 2421.TW business model transition liquid cooling data center 2026
- **major_events**（none）（沿用 2421.TW_20261011，0d）：建準電機 2421 併購 收購 2026；建準 2421 Sunon lawsuit OR 訴訟 OR 集體訴訟；建準 2421 重大訊息 調查 OR 重編 OR 裁罰 OR 召回 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2421.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"建準電機"},"oneliner":"建準：AI 伺服器風扇主要供應商，營收連創新高、本益比 15.5 倍不貴，但利潤率處在四年高點、液冷第二曲線尚無營收證據；現價不追，等液冷營收占比揭露再進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 伺服器平台的散熱預算，錢卡在「風扇與風扇牆進入 GPU 平台參考設計與 ODM 供應名單」這一節點；伺服器網通與 AI 約占營收 48%，最新一季毛利率 31.25%、營益率 15.44%。","reasoning":"營收結構（2026 年 3 月報告，原始出處未確認、可能非最新）：伺服器網通與 AI 48%、NB／PC 22%、車用電子 12%、工業與醫療 10%、其他 8%；超過一成的分部是伺服器、NB／PC、車用三塊，各分部成長率事實表未涵蓋。最新一季（2026 年第二季）營收 54.19 億元、毛利率 31.25%、營益率 15.44%。收錢方式是按件出貨的 B2B 零組件，進入 GPU 平台參考設計與 ODM 供應名單後拿下整個平台世代的量，所以錢卡在平台認證這一節點。產業時鐘判為擴張期：TrendForce 預估 GPU 機櫃出貨年增逾 30%、液冷滲透率由 2026 年 53% 升到 2027 年近 60%，需求可見度到 2027 年。供需持久性屬週期性：2027 年之後隨 AI 資本支出消化有反轉風險，散熱供給端有奇鋐、雙鴻、台達、日本電產等多家，供給可逆性高。產業態勢屬雙向拉鋸：散熱總預算擴大，但晶片端液冷壓縮氣冷用量。單點依賴：AI 伺服器平台認證（推薦供應商身分為公司說法）；前幾大客戶與供應商集中度事實表未涵蓋，列資料缺口。本輪未附逐字稿，管理層過去的財測與承諾無法對照。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_earnings_recency"],"verdict_values":{"revenue_quality":"按件出貨的 B2B 零組件，量隨平台世代認證取得，無經常性合約收入；伺服器占比約五成，使營收隨 AI 資本支出擺動（2023 年營收年減 8.17%）","unit_econ_note":"TTM 毛利率 31.89% 高於奇鋐 28.87%、雙鴻 27.85%，但研發密度 6.05% 與費用較重，營益率 15.85% 低於奇鋐 23.56%；單價與出貨量的拆分事實表未涵蓋","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"營收隨 AI 伺服器資本支出擺動（2023 年年減 8.17%、2025 年年增 27.72%），獲利成長主要來自產品組合推升的利潤率，而非自有定價權"},"industry":{"clock_phase":"II","sd_verdict_source":"TrendForce 2026-08（液冷滲透率、GPU 機櫃出貨）；摩根士丹利 2026-04（液冷需求延續至 2027 年）","bargaining":{"up":"上游原物料與零件供應商集中度事實表未涵蓋","down":"下游為伺服器 ODM 與品牌客戶，規格由 GPU 大廠參考設計主導，買方議價力強；前 1–2 大客戶占比事實表未涵蓋","geo":"2026 年資本支出上調至 15 億元以上，主要投入菲律賓新廠"},"profit_pool_dir":"散熱利潤池往液冷與高階散熱件移動；建準強項在氣冷，液冷進度落後奇鋐、雙鴻","tam_table":[{"item":"AI 晶片液冷滲透率","value":"2026 年 53%、2027 年接近 60%（TrendForce，2026-08）"},{"item":"GPU 機櫃出貨","value":"預期年增逾 30%，Kyber NVL144 的 2027 年時程可能延後（同上）"},{"item":"建準 AI 伺服器風扇份額","value":"約 30%（報導未標年份）；另一份 2025-03 分析稱其為全球第二大散熱風扇供應商"},{"item":"液冷營收占比","value":"公司未揭露；水冷板首批已出貨，液冷產品 2027 年放量（法說摘要，未逐字取得）"},{"item":"散熱營業利益池占比 5 年前→現","value":"事實表未涵蓋，無法檢查利潤池是否淨流出 5pp 以上"}]}}},"q2_moat":{"verdict":"→ 穩定：風扇本業份額未見消長、毛利率守在四年高點，但液冷新賽道落後奇鋐與雙鴻；護城河為 C 級，來自平台認證與量產規模，不來自定價權。","reasoning":"機制：風扇與風扇牆的設計量產能力，加上平台世代認證（公司稱為 GB200／GB300 推薦供應商，屬公司說法）。可證方向：同業投入資本未入事實表，ROIC 差距無法計算，改用利潤率可比軸——毛利率 31.89% 高於奇鋐 28.87%，但營益率 15.85% 比奇鋐低 7.7pp、FCF 利潤率 5.65% 比奇鋐低 18.5pp。執行面 7 分：營收連創新高、份額約 30% 未見流失，但液冷進度落後；定價面 5 分：買方集中、風扇有台達與日本電產等多家可替，毛利率上升主要來自產品組合。AI 曝險屬淨增量：伺服器需求直接長在建準的風扇產品上，但晶片端液冷繞過風扇，分界年約在 2027 年（液冷滲透率近 60%）。威脅：液冷部分取代屬生態攻擊級（扣 1 分，機率 30%），風扇點對點競爭不扣分。","fact_refs":["f_peer_2421_tw_gross_margin_pct","f_peer_2421_tw_operating_margin_pct","f_peer_2421_tw_fcf_margin_pct","f_peer_3017_tw_gross_margin_pct","f_peer_3017_tw_operating_margin_pct","f_peer_3017_tw_fcf_margin_pct","f_peer_3324_two_gross_margin_pct","f_peer_3324_two_operating_margin_pct","f_peer_3324_two_fcf_margin_pct","f_peer_3653_tw_gross_margin_pct","f_peer_3653_tw_operating_margin_pct","f_peer_6230_tw_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"風扇與風扇牆設計量產規模＋每個 GPU 平台世代的供應名單認證；轉換成本只鎖一個平台世代","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面穩定（份額無消長證據、營收創高，但液冷落後）、定價面穩定（毛利率 TTM 31.89% 對 2025 年 31.06% 微升，最新一季 31.25% 略低於 TTM）；兩者都不是擴大也不是縮減","competitor_notes":[{"name":"3017.TW","strategy_note":"奇鋐是液冷與整合散熱的領先者，營益率 23.56%、FCF 利潤率 24.1% 都遠高於建準，是液冷份額的主要對手"},{"name":"3324.TWO","strategy_note":"雙鴻液冷先行投入，營益率 15.3% 與建準相當，但 FCF 利潤率 −13.66%，顯示液冷擴產非常吃資本"},{"name":"3653.TW","strategy_note":"健策做均熱片與封裝散熱件，毛利率 42.63%、營益率 33.06%，產品不直接與風扇競爭，只作散熱環節利潤率上限參照"},{"name":"6230.TW","strategy_note":"超眾以熱管為主，營益率 −0.88%，說明散熱產業不是人人受惠，沒有 AI 伺服器份額就沒有利潤"}],"threats":[{"level":"🔴","text":"液冷架構部分取代氣冷：晶片端改用水冷板，風扇只留在機櫃其他部位；建準自身液冷進度落後奇鋐、雙鴻。因混合散熱仍為主流、公司也在布局液冷，定為生態攻擊級而非全面架構替代","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#2","end_markets#2"]},{"level":"🟡","text":"風扇本業點對點競爭：奇鋐、台達、日本電產都供應伺服器風扇，每次平台換代重新比價；目前未見具名丟單或新進入者搶單","p":25,"evidence_refs":["competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"營益率中高（TTM 15.85%）×投入資本周轉率事實表未涵蓋，象限無法定案；2022–2025 年淨利倍增而累計淨再投資接近零，當期報酬偏向低資本需求型態，但 2026 年擴產後周轉率可能下降","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端業者的 AI 機櫃、決策者是 GPU 大廠參考設計與 ODM 散熱團隊、付款者是 ODM，三角色都成立，散熱是需要不是想要。但客戶要解決的是晶片發熱，風扇只是解法之一：GB200 晶片端已改水冷板、其餘部位仍用風扇，需求在、解法在移轉（代理讀數：液冷滲透率 2026 年 53%→2027 年近 60%）"},{"item":"決策層級","level":"🟡","text":"替代性在每個平台世代的供應名單這一層決定，不在風扇品項；GB200→GB300→Vera Rubin 每次換代都重新認證，轉換成本只鎖 1–2 年。公司稱為 GB200／GB300 推薦供應商（公司說法），AI 伺服器風扇份額約 30%（報導未標年份），未見具名丟單證據"},{"item":"價值鏈分配","level":"🟡","text":"散熱在 AI 機櫃中金額占比小、買方集中，價值大多被晶片端拿走；散熱環節內利潤往液冷與高階散熱件集中——健策營益率 33.06%、奇鋐 23.56%、建準 15.85%，超眾 −0.88% 說明沒卡到好位置就賺不到錢"},{"item":"社會容忍度","level":"🟢","text":"B2B 工業零組件，無監管授權、無民生必需品的社會漲價壓力；定價上限由客戶議價決定，不受社會容忍度約束"}],"roiic":"投入資本未入事實表，無法直接計算。代理讀數：2023–2025 年累計淨利 49.9 億、自由現金流 52.9 億，淨再投資約 −3 億，同期淨利由 2022 年 10.9 億增至 2025 年 21.7 億，過去的增量報酬來自產品組合與產能利用率，不是新投入資本；2026 年起的新投入（菲律賓廠、液冷）報酬未知，取 20% 作判斷假設","reinvest_rate":"約 0.54（TTM）：以 FY2025 淨利÷營業利益≈0.77 把 TTM 營益率 15.85% 折成稅後約 12.2%，扣掉 FCF 利潤率 5.65% 的差額視為淨再投資，（12.2−5.65）÷12.2≈0.54","endo_ceiling":10.7,"formula_note":"內生成長上限＝增量報酬 20%（判斷假設）×再投資率 0.54≈10.7%；20% 低於歷史隱含值，理由是液冷同業雙鴻 TTM FCF 利潤率 −13.66%，顯示新業務資本密集"}}}},"q3_growth":{"verdict":"🟡 中：AI 伺服器散熱需求可見到 2027 年，但風扇本業不是低滲透市場，液冷第二曲線還沒有營收占比證據；共識三年 EPS 年複合 27.3% 遠高於內生上限 10.7%，缺口靠利潤率擴張撐。","reasoning":"成長是量為主、組合次之，無併購與回購。共識 EPS：FY2026E 10.85、FY2027E 13.4、FY2028E 16.28 元（Koyfin 快照美元值依 2026-10-09 匯率換算新台幣，家數事實表未涵蓋），對 FY2025A 7.89 元的三年年複合＝（16.28÷7.89）^(1/3)−1≈27.3%。內生上限 10.7%（見護城河段），缺口約 16.6pp 歸因於利潤率擴張與營運槓桿：2022–2025 年 EPS 年複合 22.3%、營收只有 9.9%，淨再投資接近零，利潤增加來自組合與產能利用率；這類缺口能維持多久取決於 AI 週期，不是可複利的再投資。跑道判讀：本業已過低滲透期，第二曲線（水冷板、CDU、Sidecar、水泵）還在送樣到小量出貨，沒有可驗證的營收占比，因此給中等跑道。衰退信號亮兩盞（EPS 成長遠高於營收成長、替代技術壓縮氣冷用量），長期成長性與價值陷阱風險皆為中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_peer_2421_tw_fcf_margin_pct","f_peer_2421_tw_operating_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量為主：AI 伺服器出貨帶動（2026 年前 8 月營收年增 21.08%）；組合次之：伺服器占比上升把毛利率由 2022 年 22.55% 拉到 2025 年 31.06%；無併購、無回購","runway_years":"不適用滲透率口徑：風扇本業不是低滲透市場；AI 伺服器需求可見度約到 2027 年，液冷第二曲線尚無營收占比，有效成長期暫估 2–3 年","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段報酬持續期推導：增量報酬假設 20%×再投資率約 0.54≈10.7%；共識三年 EPS 年複合 27.3% 超出約 16.6pp，缺口歸因於利潤率擴張與營運槓桿","segments":[{"item":"伺服器網通與 AI 應用","value":"48%（2026 年 3 月報告，出處未確認）；分部利潤率事實表未涵蓋，公司毛利率由 2022 年 22.55% 升到 2025 年 31.06%，與伺服器占比上升同期"},{"item":"IT（NB／PC）","value":"22%"},{"item":"車用電子","value":"12%"},{"item":"工業與醫療","value":"10%"},{"item":"其他","value":"8%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":null,"evidence":"單季年比資料事實表未涵蓋；最新一季 31.25% 略低於 TTM 31.89%"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"未見份額消長的直接證據"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"無提價後量縮證據"},{"signal":"EPS 成長顯著高於營收成長（差距逾 5pp）","lit":true,"evidence":"2022–2025 年 EPS 年複合 22.3%、營收 9.9%，差 12.4pp"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 0.74、2025 年 1.07，未連續；2026 年擴產後有再度跌破風險"},{"signal":"SBC／營收逾 5% 且逐年上升","lit":null,"evidence":"事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"evidence":"晶片端改用水冷板，氣冷單機用量被部分取代；風扇專屬需求的量化資料查無"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"P/S、EV/S 位於四個年度端點最高位置，倍數上移"},{"signal":"維護性資本支出占 FCF 逾 60%","lit":null,"evidence":"折舊與維護性資本支出事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"2026 年資本支出上調至 15 億元以上"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置計分卡三項中兩項不適用（無併購、無回購）；唯一適用的股數稀釋項因股數增加來源不明，無法驗證通過，因此按 C 級計，持有年限上限為中期 2–5 年。這和本判斷的循環屬性不做長抱一致。2026 年現金轉向擴產，最新一季自由現金流只占營業現金流約三分之一。","reasoning":"FCF／淨利：2022 年 1.61、2023 年 1.39、2024 年 0.74、2025 年 1.07（年度財報）。最新一季營業現金流 6.118 億、資本支出 4.037 億，FCF 2.082 億，TTM FCF 利潤率降到 5.65%，主因 2026 年資本支出上調至 15 億元以上（菲律賓新廠）。股東回饋以現金股息為主，殖利率 3.119%；事實表未見回購、未見併購。以淨利÷稀釋 EPS 推算的股數由 2022 年約 2.53 億股增至 2025 年約 2.75 億股（年均約 2.8%，但 2024→2025 不變），增加來源（員工酬勞、可轉債轉換或盈餘轉增資）事實表未涵蓋，無法判定是否屬股權酬勞稀釋。SBC／營收與現金去向四分事實表未涵蓋。營運槓桿：2025 年營收年增 27.72%、營業利益年增約 67.5%，屬擴張而非壓縮。","fact_refs":["f_kpi3_eps","f_kpi4","f_dividend_yield_ttm","f_peer_2421_tw_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事件掃描未見併購，無已實現併購報酬可評"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未見回購；股東回饋以現金股息為主（殖利率 3.119%）"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"推算股數 2022 年約 2.53 億→2025 年約 2.75 億（年均約 2.8%，2024→2025 不變）；增加來源事實表未涵蓋，無法認定為股權酬勞稀釋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長未靠併購支撐；現金回饋以股息為主（殖利率 3.119%），回購紀錄與現金去向四分事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價 168 元要求 FY2027–2028 達成共識 13.4、16.28 元，且 2028 年後不出現循環回落；前兩年我信，之後的延續不信——這是合理價，不是便宜價。","reasoning":"現價 168 元、Fwd P/E 15.48 倍（FY2026E 10.85 元）、FY2027E 12.54 倍；三年共識 EPS 年複合 27.3%，PEG 0.57。賣方：4 位分析師全數買進，平均目標 194 元（高 214、低 180，2026-07-27 快照），現價比平均低約 13%、也低於最低目標，全距倍數 1.19，方向支持不貴；摩根士丹利 2026-04 把目標價由 175 降至 165 元、評中性，與現價接近。反方向：P/S 2.37 倍、EV/S 2.09 倍皆位於四個年度端點的最高位置，本益比在四個年度端點的分位為 82.2（不是五年口徑，五年高低點事實表未涵蓋）。現價隱含什麼：若五年後倍數回到 13 倍，FY2031 EPS 只要約 12.9 元（較 FY2026E 年增約 3.6%）就能保本，所以風險不在成長不夠，而在 2028 年之後的循環回落與營益率回到 11–12%。同業 Forward P/E 事實表未涵蓋，無法做倍數對照。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_dividend_yield_ttm","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY2026E 共識 EPS 10.85 元）＋PEG；循環屬性下輔以 P/S、EV/S 在四個年度端點的位置","peers":{"expanded":false,"reason":"同業 Forward P/E 事實表未涵蓋（同業對照只有利潤率），無法做倍數對照；改以本身 Fwd P/E 15.48 倍、2026-08 高點 16.5–17 倍與賣方目標 180–214 元為尺"},"fwd_pe":15.48,"peg":0.57,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Fwd P/E 15.48 倍、FY2027E 12.54 倍、PEG 0.57（FY2025A 7.89→FY2028E 16.28 元，年複合 27.3%）表面便宜；但 P/S 2.37 倍與 EV/S 2.09 倍都在四個年度端點最高位置、營益率在四年高點，便宜建立在週期高檔利潤率上。兩者相抵，判為合理","upside_short_pct":15.5,"upside_mid_pct":35.4,"denominator_disputed":false,"denominator_note":"FY2026E 分母未見一次性項目；爭點在利潤率是否處於週期高點，已反映在情境樹倍數，不屬分母爭議"}}},"q6_how_wrong":{"verdict":"🟡：最可能看錯的是把 AI 週期高點的利潤率當成新常態；壓力測試四題過三題，唯一不過的是 2028 年資本支出消化的循環年。","reasoning":"壓力測試以 Base 路徑 FY2028E 15.0 元為起點，之後三年 EPS 年增降到 15%／10%／5% 並分別配 14／12／10 倍，五年後股價約 319／240／174 元，三題都高於現價 168 元；第四題循環下行（FY2031E 9.5 元×10 倍＝95 元）不過，四題過三題。最大回撤推導：歷史最大回撤事實表未涵蓋；下界取 Bear 路徑谷底 FY2029E 8.5 元×9 倍≈77 元（約 −54%），再留 4pp 超跌空間至 −58%；上界取 EPS 停在 FY2026E 10.85 元、本益比由 15.48 倍壓到 10 倍（約 −35%），加 3pp 至 −38%。價值陷阱信號亮兩盞（EPS 成長遠高於營收成長、替代技術壓縮氣冷用量），判為中等。","fact_refs":["f_peer_2421_tw_operating_margin_pct","f_fwd_pe_latest","f_consensus_eps_fy1","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點利潤率被當成新常態"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.85,"pe":15.48,"basis":"FY2026E 共識 EPS（會計年度已過四分之三），與終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[14.0,17.0,19.5,21.5,23.5],"base":[13.0,15.0,15.5,16.5,17.5],"bear":[12.0,9.0,8.5,9.0,9.5]},"pe":{"bull":17,"base":13,"bear":10},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":3.119,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"max_dd":{"lo":-58,"hi":-38,"basis":"歷史最大回撤事實表未涵蓋。下界：Bear 路徑谷底 FY2029E 8.5 元×9 倍≈77 元（約 −54%），再留 4pp 超跌空間至 −58%；上界：EPS 停在 FY2026E 10.85 元、本益比由 15.48 倍壓到 10 倍（約 −35%），加 3pp 情緒面至 −38%。觸發情境為 AI 資本支出消化或失去下一世代平台資格","trigger_time":null},"basis":{"bull":"保住 Vera Rubin 世代風扇與風扇牆份額，液冷 2027 年起放量成第二支柱，營益率守在 16% 以上；FY2027–2028 略高於共識 13.4、16.28 元。終端 17 倍＝2026-08 漲停時 16.5–17 倍的上緣（同業現值倍數事實表未涵蓋）","base":"FY2027–2028 略低於共識（液冷貢獻慢於預期），FY2029 進入資本支出消化、EPS 只小幅成長，之後隨散熱單機價值溫和成長，五年 EPS 年複合約 10%，落在內生上限 10.7% 之內。終端 13 倍低於現值 15.48 倍，反映成長降速","bear":"2027 年需求仍在，2028 年 AI 資本支出消化疊加液冷壓縮氣冷用量，營收下滑、營益率回到 2023–2024 年 11–12%，EPS 回到 8.5–9.5 元。終端 10 倍取自成長熄火情境：三年後成長降到 5% 時配 10 倍，較現值 15.48 倍壓縮約 35%"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"TTM 營益率 15.85% 高於 2023–2024 年 11.49–11.85%；2022–2025 年 EPS 年複合 22.3% 而營收只有 9.9%，獲利成長主要來自利潤率；GB200 晶片端已改水冷板，風扇只留在其餘部位","assumption":"市場假設 AI 伺服器需求與產品組合紅利延續到 2028 年之後","consequence":"若 2028 年進入資本支出消化期，營收下滑、營益率回到 11–12%，EPS 回到 8.5–9.5 元，倍數同步壓到 9–10 倍，股價落在 76–95 元，五年虧損約 45%","ruling":"採納為 Bear 情境主軸，機率 30%；與唯一致命點部分重疊（失去下一世代平台資格是這條路徑的加速版），已回補至觸發器","watch":"TTM 營益率是否跌破 12%；月營收年增是否連 3 個月轉負","evidence_refs":["substitute_technology#0"],"fact_refs":["f_peer_2421_tw_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"最新一季營業現金流 6.118 億、資本支出 4.037 億，自由現金流只剩 2.082 億；TTM FCF 利潤率 5.65%，低於 2025 年 12.4%；2026 年資本支出上調至 15 億元以上；液冷先行者雙鴻 TTM FCF 利潤率 −13.66%","assumption":"營收成長會等比例轉成股東可分配的現金","consequence":"營收照共識成長，但液冷與擴產的新投入報酬偏低，FCF／淨利長期低於 0.75，股息成長停滯，終端倍數應下修","ruling":"部分採納：內生成長上限已用 20% 增量報酬保守估計，Base 終端倍數 13 倍低於現值；若 FCF／淨利連 2 年低於 0.75，終端倍數再下修 1 倍","watch":"FY2026、FY2027 年度 FCF／淨利","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_kpi4","f_peer_2421_tw_fcf_margin_pct","f_peer_3324_two_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"26 週漲 27.24%；P/S 2.37 倍、EV/S 2.09 倍都在四個年度端點最高位置；摩根士丹利 2026-04 目標價 165 元、評中性","assumption":"現價已計入 2026 年營收創高與 2027 年延續","consequence":"若 2027 年成長只達共識，股價缺乏上修空間","ruling":"反駁：以本益比看，Fwd 15.48 倍低於 2026-08 漲停時的 16.5–17 倍，FY2027E 只有 12.54 倍，股價也低於 4 位賣方最低目標 180 元；價格沒有過度反映，問題在利潤率持續性而不在倍數","watch":"股價若在共識未上修下漲過 194 元（賣方平均目標）則不追","evidence_refs":["supply_demand_durability#0","capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_ps_percentile","f_ev_s_percentile","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"事件掃描在七個面向都查無資料：客戶二供、客戶集中度與信用、反壟斷與監理、關稅與出口管制、地緣與供應鏈、通路與商業模式轉變、重大事件。事實表也未涵蓋前幾大客戶占比、應收帳款集中度、生產基地分布與對美出貨比重。這一塊唯一已知的事實是：2026 年資本支出上調至 15 億元以上，主要投入菲律賓新廠","assumption":"假設前 1–2 大客戶占比未超過 40%，下一世代平台沒有導入第二供應商分食份額，關稅、出口管制與地緣事件也不改變平台認證結構","consequence":"客戶集中與二供：若單一 ODM 或 GPU 大廠占比過高，或下一世代改採雙供應商，失去一個平台世代的衝擊會大於 Bear 情境。客戶信用：買方集中時，單一客戶延遲付款會放大擴產期已偏低的自由現金流壓力。關稅與出口管制、地緣與供應鏈：若生產基地集中在單一受管制地區，加徵關稅會壓縮毛利，或迫使客戶轉單。菲律賓新廠可以部分分散這個風險，但投產時點事實表未載。通路與商業模式：若散熱採購由逐項採購零組件轉向機櫃級整合方案，決策權會移往整合能力強的同業，建準以單一零組件身分議價會更弱。反壟斷與監理：B2B 工業零組件，有台達、日本電產、奇鋐等多家供應商，沒有監理授權門檻，屬低相關。重大事件：火災停工、訴訟、經營層異動皆查無","ruling":"列為資料缺口，不採信也不否定，逐項處置如下。反壟斷與監理判為低相關，不調整。通路與商業模式轉變的風險方向和液冷替代威脅、唯一致命點相同，已由兩者涵蓋，不另調機率。重大事件查無，不調整。客戶集中與二供、客戶信用、關稅與出口管制、地緣與供應鏈四項在揭露前不計入 Bear 機率；只要出現以下任一情況，Bear 機率上調至 35% 並重跑情境樹：年報揭露單一客戶占比超過 40%、確認下一世代導入第二供應商、確認主要產能落在被加徵關稅或出口管制的地區","watch":"年報前十大客戶與應收帳款集中度揭露；法說會生產基地分布與菲律賓廠投產時點；美國對伺服器零組件的關稅與出口管制公告；下一世代平台供應名單是否出現第二家風扇供應商","evidence_refs":[],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 168.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=168.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：2027 年前的需求","cause":null,"prior_field":null,"side_a":"月營收前 8 月年增 21.08%、7 月 31.65%；TrendForce 預估 GPU 機櫃出貨年增逾 30%、液冷滲透率 2027 年近 60%；摩根士丹利認為液冷需求延續到 2027 年","side_b":"無反向證據","ruling":"一致：2027 年前的需求不是爭點，爭點在 2028 年之後的循環與液冷份額","evidence_level":"公告月營收＋第三方產業預估","settle_metric":"2027 年月營收累計年增率","if_then":["若 2027 年上半年累計年增仍 ≥15% → 維持 Base 情境不動","若累計年增跌破 5% → Base 的 FY2027 EPS 下修至 12 元並重跑情境樹"],"evidence_refs":["end_markets#0","end_markets#3","supply_demand_durability#1","supply_demand_durability#0"]},{"axis":"營收創高 vs 液冷落後","cause":null,"prior_field":null,"side_a":"營收連創新高、4 位賣方全數買進、平均目標 194 元；公司稱為 GB200／GB300 推薦供應商，水冷板首批已出貨","side_b":"液冷進度落後奇鋐、雙鴻，液冷產品 2026 年第三季才小量送驗、2027 年放量；摩根士丹利因液冷貢獻待放大把目標價由 175 元降到 165 元","ruling":"可調和（程度差異）：近兩年營收靠風扇本業，液冷落後影響的是 2028 年之後的份額與利潤池；以液冷營收揭露為裁決點，在此之前論點只支撐觀望，不支撐溢價","evidence_level":"A 側為公告數據與賣方評等；B 側為法說摘要與賣方報告（未取得逐字原文）","settle_metric":"法說會揭露的液冷產品營收占比","if_then":["若 2027 年上半年液冷營收占比 ≥5% 且月營收年增 ≥15% → 首倉 2%，之後逐季加碼至 4%","若 2027 年底液冷仍停在送樣、沒有營收占比 → 不進場，Bull 機率由 20% 降到 10% 重跑情境樹"],"evidence_refs":["end_markets#2","supply_demand_durability#0","capital_markets_pricing#0","competitive_share_entrants#1","substitute_technology#1"]},{"axis":"表面便宜 vs 週期高檔利潤率","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：Fwd P/E 15.48 倍、FY2027E 12.54 倍，三年共識 EPS 年複合 27.3%、PEG 0.57，股價低於賣方最低目標 180 元，殖利率 3.1% 墊底","side_b":"便宜建立在四年高點的利潤率上：營益率由 2022 年 7.96% 升到 TTM 15.85%，P/S 與 EV/S 在四個年度端點最高位置；循環型公司在利潤率高點的低本益比不構成安全邊際","ruling":"不可調和（方向相反），選 B 側。依據：2022–2025 年 EPS 年複合比營收高約 12pp，成長來自利潤率擴張而非營收，且液冷會壓縮氣冷單機用量；因此 Base 終端倍數取 13 倍、Bear 取 10 倍，不用現值倍數外推","evidence_level":"公司年度財報＋現值倍數","settle_metric":"TTM 營益率與 2027 年營收年增","if_then":["若 TTM 營益率連 2 季低於 14% 而股價仍在 160 元以上 → 不進場，持有者減碼一半","反向：若 2027 年營益率守住 16% 以上且營收年增 ≥15%，證明利潤率結構性抬升 → Base 終端倍數上調至 15 倍重跑，並以首倉 2% 進場"],"evidence_refs":["substitute_technology#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：液冷滲透率 2026 年 53%、2027 年近 60%，GPU 機櫃出貨年增逾 30%，散熱總預算擴大","side_b":"替代技術：晶片端改水冷板，風扇只留在其餘部位；競爭面未見新進入者搶單或份額流失證據；風扇專屬需求量化資料查無","ruling":"雙向拉鋸：散熱總預算擴大與氣冷單機用量被壓縮同時發生，對建準的淨效果取決於液冷份額","evidence_level":"第三方產業預估＋研究報告引述","settle_metric":"伺服器網通與 AI 營收占比","if_then":["若伺服器營收占比由 48% 升到 55% 以上 → 判定結構轉好占上風，Bull 機率上調至 25%","若占比跌破 40% → 視同唯一致命點發生，清倉"],"evidence_refs":["supply_demand_durability#1","substitute_technology#0","competitive_share_entrants#2","supply_demand_durability#2"]}],"triggers":[{"n":1,"text":"2027 年月營收累計年增維持 15% 以上，驗證 AI 散熱需求延續","type":"假設驗證","maps_to":"H1","metric":"月營收累計年增率","threshold":"≥15%","action":"維持觀察，不因單月波動調整","source_freq":"公開資訊觀測站月營收／每月","date":"2027-01 起每月"},{"n":2,"text":"TTM 毛利率與營益率守住擴產期水準","type":"假設驗證","maps_to":"H2","metric":"TTM 毛利率／TTM 營益率","threshold":"≥29%／≥14%","action":"跌破任一項則停止加碼","source_freq":"季報／每季","date":"2026-11 起每季"},{"n":3,"text":"液冷產品營收占比首次揭露達 5% 以上，且利潤率與營收成長同時守住","type":"估值rearm","maps_to":"H3","metric":"液冷產品營收占比＋TTM 營益率＋月營收年增率","threshold":"≥5%／≥15%／≥15%","action":"重跑研究後首倉 2%","source_freq":"法說會／每季","date":"2027-03 前後"},{"n":4,"text":"月營收年增率連 2 個月低於 10%，供應鏈延後或需求放緩","type":"風險","maps_to":"R1","metric":"月營收年增率","threshold":"連 2 個月 <10%","action":"停止加碼","source_freq":"公開資訊觀測站月營收／每月","date":"2026-11 起每月","evidence_refs":["end_markets#2"]},{"n":5,"text":"毛利率連 4 季低於 29% 且伺服器占比下降，顯示液冷壓縮氣冷用量","type":"減碼","maps_to":"R2","metric":"TTM 毛利率／伺服器網通與 AI 營收占比","threshold":"<29% 連 4 季，且占比較前一年下降","action":"減碼一半","source_freq":"季報與法說會／每季","date":"2026-11 起每季","evidence_refs":["substitute_technology#0"]},{"n":6,"text":"TTM 營益率跌破 12%，利潤率回到上一輪循環水準","type":"減碼","maps_to":"R3","metric":"TTM 營業利益率","threshold":"<12%","action":"減碼一半；連 2 季未回升則清倉","source_freq":"季報／每季","date":"2027-01 起每季"},{"n":7,"text":"Vera Rubin 世代主力機櫃的風扇供應資格旁落","type":"Single Thing","maps_to":"Single Thing","metric":"法說會平台出貨說明／伺服器網通與 AI 營收占比","threshold":"公司確認未取得資格，或伺服器營收占比 <40%","action":"清倉","source_freq":"法說會與月營收／每季","date":"2027 年上半年起"},{"n":8,"text":"股價先跌、基本面未損時分批反買","type":"加碼","maps_to":"H1","metric":"股價／月營收年增率","threshold":"≤135 元／≥15%","action":"分批反買，首倉 2%","source_freq":"日線收盤＋月營收／每日","date":"即日起"},{"n":9,"text":"年度 FCF／淨利連 2 年低於 0.75，擴產吃掉現金","type":"風險","maps_to":"R4","metric":"年度 FCF／淨利","threshold":"<0.75 連 2 年（FY2026–FY2027）","action":"停止加碼並將終端倍數下修 1 倍重跑","source_freq":"年報現金流量表／每年","date":"2028-03","evidence_refs":["capital_markets_pricing#2"]},{"n":10,"text":"FY2026 年報與法說會後複審","type":"複審日期","maps_to":null,"metric":"FY2026 EPS 對共識 10.85 元","threshold":"偏離 ±5%","action":"重跑情境樹","source_freq":"年報／每年","date":"2027-03-31"}],"kill_metrics":[{"metric":"月營收年增率","bear_threshold":"連 3 個月 <0%","window":"2027-01～2028-12","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"TTM 營業利益率","bear_threshold":"<12%（回到 2023–2024 年水準）","window":"2026 年第三季～2028 年第四季","source":"季報損益表","last_status":"ok"},{"metric":"伺服器網通與 AI 營收占比","bear_threshold":"<40%","window":"每次法說會至 2028 年","source":"法說會簡報","last_status":"unknown"},{"metric":"年度 FCF／淨利","bear_threshold":"<0.75 連 2 年","window":"FY2026～FY2027","source":"年報現金流量表","last_status":"warning"},{"metric":"液冷產品營收占比","bear_threshold":"2027 年底仍未揭露或 <5%","window":"至 2027-12","source":"法說會產品別營收說明","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"法說會揭露液冷產品營收占比 ≥5%，且 TTM 營益率 ≥15%、月營收年增 ≥15%","exec_line":"現價 168 元不追。液冷占比證實後首倉 2%；若股價先跌到 135 元以下而月營收年增仍 ≥15%，分批反買首倉 2%；伺服器營收占比跌破 40% 或確認失去下一世代資格則清倉","holding_cap":"液冷第二曲線證實前單檔上限 3%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等法說會揭露液冷產品營收占比 ≥5% 且 TTM 營益率 ≥15% 再進場；現價不追","qc48_result":null,"qc48_note":null},"decision_out":{"role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=27.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等法說會揭露液冷產品營收占比 ≥5% 且 TTM 營益率 ≥15% 再進場；現價不追'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"AI 伺服器散熱需求延續到 2027 年，營收維持雙位數成長","2y":"2027 全年營收年增 ≥15%","5y":null,"10y":null,"threshold":"2027 年月營收累計年增率 ≥15%","source":"公開資訊觀測站月營收公告（每月）","drift_rule":"TTM 營收低於年增 15% 路徑 5% 以上連 2 季＝削弱；低於 10% 以上連 3 季＝反轉"},{"id":"H2","text":"伺服器產品組合撐住利潤率，擴產與折舊上升期間不跌回 2023–2024 年水準","2y":"TTM 毛利率 ≥29%、營益率 ≥14%","5y":null,"10y":null,"threshold":"TTM 毛利率 ≥29% 且 TTM 營益率 ≥14%","source":"季報損益表（每季）","drift_rule":"TTM 毛利率低於門檻 5%（約 27.6%）連 2 季＝削弱；低於門檻 10%（約 26.1%）連 3 季＝反轉"},{"id":"H3","text":"液冷產品（水冷板、CDU、Sidecar、水泵）成為第二支柱，補上氣冷被壓縮的用量","2y":null,"5y":"FY2030 液冷營收占比 ≥15%","10y":null,"threshold":"FY2028 液冷營收占比 ≥10%、FY2030 ≥15%","source":"法說會產品別營收說明與年報（每季／每年）","drift_rule":"揭露占比低於路徑 5% 以上連 4 季＝削弱；低於 10% 以上連 6 季或持續不揭露＝反轉"}],"R":[{"id":"R1","text":"AI 伺服器專案受記憶體、PCB、晶片供應延後，月營收短期失速","h_ref":"H1","clock":"⚡","threshold":"月營收年增率連 2 個月 <10%","evidence_refs":["end_markets#2"]},{"id":"R2","text":"液冷壓縮每台機櫃的風扇用量，氣冷營收被部分取代，利潤率先受壓","h_ref":"H2","clock":"🔥","threshold":"TTM 毛利率 <29% 連 4 季，且伺服器營收占比較前一年下降","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"id":"R3","text":"2028 年後 AI 資本支出進入消化期，營益率回到上一輪 11–12%","h_ref":"H2","clock":"🐢","threshold":"TTM 營益率 <12%","evidence_refs":["supply_demand_durability#0"]},{"id":"R4","text":"菲律賓擴產與液冷投資吃掉自由現金流，新投入資本報酬偏低","h_ref":"H3","clock":"🔥","threshold":"年度 FCF／淨利 <0.75 連 2 年（FY2026–FY2027）","evidence_refs":["capital_markets_pricing#2"]}],"single_thing":{"description":"Vera Rubin 世代主力機櫃的伺服器風扇（含風扇牆）未取得主要 ODM 或 GPU 大廠參考設計的供應資格","why_fatal":"伺服器網通與 AI 約占營收 48%，是 FY2027–2028 共識 EPS 13.4、16.28 元的主要來源；失去一個平台世代等於 18–24 個月的營收缺口，而液冷尚無法補位","if_happens":"EPS 路徑改走 Bear（FY2028 約 9 元），終端倍數 10 倍、價值約 95 元；清倉，不等財報確認","how_monitor":"每月營收年增率與法說會平台出貨說明；伺服器營收占比跌破 40% 視同發生","probability":"約 15%（12–24 個月）：公司稱為 GB200／GB300 推薦供應商（公司說法），風扇份額約 30% 未見流失證據，但每次平台換代都重新認證"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.54,"peg_fy2":0.46,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":7.89,"FY2026E":10.85,"FY2027E":13.4,"FY2028E":16.28},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識為 Koyfin 快照美元值依 2026-10-09 匯率（×31.912）換算新台幣"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報與法說會（液冷出貨進度、2027 年資本支出）","impact":"高","watch":"毛利率是否守住 29%、液冷營收是否首度量化"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"水冷板放量（法說摘要稱第四季放量）","impact":"中","watch":"10–12 月月營收年增是否維持 20% 以上"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026 年報與股利政策","impact":"中","watch":"FY2026 EPS 對共識 10.85 元、年度 FCF／淨利"},{"date":"2027","date_precision":null,"type":"capacity","event":"液冷產品放量與菲律賓新廠投產（投產確切時點事實表未載）","impact":"高","watch":"液冷營收占比揭露、折舊上升後的營益率"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
